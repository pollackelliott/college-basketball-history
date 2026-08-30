#!/usr/bin/env python3
"""Plan and apply Oklahoma historical HOME venue/location remediation.

The tool uses Oklahoma Athletics' official home-facility chronology to enrich an
Oklahoma source assertion only after that assertion is already classified as
SOURCE_PROGRAM_HOME.  It never infers H/A/N from venue or geography.

Canonical enrichment is stricter: canonical venue/location is changed only when
canonical H/A/N is already resolved as Oklahoma home.  Two Oklahoma source rows
whose home assertions were previously rejected at Owner Gate 1 therefore retain
Oklahoma source-side venue evidence without changing canonical H/A/N/site data.
Conversely, one 1942 canonical Oklahoma-home game whose Oklahoma ledger says
"at Kansas" receives canonical Field House data because Owner Gate 1 resolved
that H/A/N conflict in favor of Kansas's official Norman, Oklahoma evidence.

Default mode writes a sealed JSON dry-run plan.  --apply requires the exact plan
SHA-256 and refuses partial application if any unexpected ambiguity remains.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PROGRAM = "oklahoma"
EXPECTED_SOURCE_HOME_GAPS = 634
EXPECTED_CANONICAL_HOME_GAPS = 633
EXPECTED_SOURCE_FACILITY_COUNTS = {
    "lloyd-noble-center": 10,
    "mccasland-field-house": 471,
    "ou-gymnasium": 84,
    "ou-rotc-armory": 69,
}
EXPECTED_CANONICAL_FACILITY_COUNTS = {
    "lloyd-noble-center": 10,
    "mccasland-field-house": 471,
    "ou-gymnasium": 84,
    "ou-rotc-armory": 68,
}
PLAN_VERSION = 2
NORMAN = ("Norman", "OK")
FIELD_HOUSE_FIRST = "1928-01-13"
LLOYD_NOBLE_FIRST = "1975-12-01"
SOURCE_BASIS = (
    "Oklahoma Athletics facilities history / men's basketball historical media guide: "
    "OU Gymnasium home site beginning 1907; R.O.T.C. Armory replaced it in 1919; "
    "OU Field House opened for men's basketball with a 45-19 Kansas win on "
    "1928-01-13 and remained the primary home through 1975; Lloyd Noble Center "
    "became the primary home beginning in December 1975."
)

# Oklahoma's year-by-year ledger does not print dates for 1927-28.  Its rows are
# chronological, and Oklahoma Athletics independently identifies the 45-19 Kansas
# game (OKLRAW-00279) as the Field House's first game on 1928-01-13.  Therefore the
# two home rows before Kansas remain Armory games and the home rows at/after Kansas
# are Field House games.  This is an explicit sequence-based exception, not a
# season-wide guess.
TRANSITION_1927_28_OVERRIDES = {
    "OKLRAW-00274": "ou-rotc-armory",
    "OKLRAW-00275": "ou-rotc-armory",
    "OKLRAW-00279": "mccasland-field-house",
    "OKLRAW-00281": "mccasland-field-house",
    "OKLRAW-00284": "mccasland-field-house",
    "OKLRAW-00285": "mccasland-field-house",
    "OKLRAW-00286": "mccasland-field-house",
    "OKLRAW-00291": "mccasland-field-house",
}

# These two Oklahoma source HOME assertions remain preserved as source evidence,
# including their source-side Oklahoma venue assignment, but Owner Gate 1 explicitly
# resolved canonical H/A/N in favor of the reciprocal source.  Canonical must not be
# changed by the chronology tool.
RECONCILED_NON_OKLAHOMA_HOME = {
    "OKLRAW-00218": {
        "canonical_game_id": "CBBG-0000290",
        "discrepancy_id": "DISC-001890",
        "canonical_site_type": "TEAM_A_HOME",
    },
    "OKLRAW-01226": {
        "canonical_game_id": "CBBG-0004109",
        "discrepancy_id": "DISC-001918",
        "canonical_site_type": "TEAM_A_HOME",
    },
}

# Owner Gate 1 resolved this game as Oklahoma home based on Kansas's official row
# placing it in Norman, despite Oklahoma's conflicting "at Kansas" ledger wording.
CANONICAL_ONLY_OKLAHOMA_HOME = {
    "CBBG-0012117": {
        "source_game_id": "OKLRAW-00524",
        "discrepancy_id": "DISC-001901",
        "facility_key": "mccasland-field-house",
        "canonical_site_type": "TEAM_B_HOME",
    }
}


class OklahomaHomeError(RuntimeError):
    pass


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv_preserving(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    original = path.read_bytes()
    has_bom = original.startswith(b"\xef\xbb\xbf")
    line_ending = "\r\n" if b"\r\n" in original else "\n"
    encoding = "utf-8-sig" if has_bom else "utf-8"
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator=line_ending)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
    temp.replace(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head(repo: Path) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def plan_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def normalize_venue_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").casefold())


def venue_number(value: str) -> int:
    match = re.fullmatch(r"VEN-(\d{6})", value or "")
    return int(match.group(1)) if match else -1


def oklahoma_home(canonical: dict[str, str]) -> bool:
    site = canonical.get("site_type", "").strip()
    return (
        site == "TEAM_A_HOME"
        and canonical.get("team_a_key", "").strip() == PROGRAM
    ) or (
        site == "TEAM_B_HOME"
        and canonical.get("team_b_key", "").strip() == PROGRAM
    )


def facility_key_for(row: dict[str, str]) -> tuple[str | None, str | None]:
    source_id = row.get("source_game_id", "").strip()
    if source_id in TRANSITION_1927_28_OVERRIDES:
        return TRANSITION_1927_28_OVERRIDES[source_id], None

    season = row.get("season_label", "").strip()
    date = row.get("game_date", "").strip()

    if not re.fullmatch(r"\d{4}-\d{4}", season):
        return None, "invalid_season"
    if season <= "1918-1919":
        return "ou-gymnasium", None
    if "1919-1920" <= season <= "1926-1927":
        return "ou-rotc-armory", None
    if season == "1927-1928":
        if not date:
            return None, "1927-28_transition_missing_date_not_in_verified_sequence"
        return (
            "ou-rotc-armory" if date < FIELD_HOUSE_FIRST else "mccasland-field-house",
            None,
        )
    if "1928-1929" <= season <= "1974-1975":
        return "mccasland-field-house", None
    if season == "1975-1976":
        if not date:
            return None, "1975-76_transition_missing_date"
        return (
            "mccasland-field-house" if date < LLOYD_NOBLE_FIRST else "lloyd-noble-center",
            None,
        )

    # Modern Oklahoma intentionally stages some HOME games in McCasland Field House.
    # A later blank therefore requires game-specific evidence rather than a blanket LNC
    # assignment.  The current expected historical gap universe contains no such hold.
    return None, "post_1975_primary_history_not_sufficient"


def resolve_facilities(
    repo: Path,
) -> tuple[dict[str, dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    venue_fields, venues = read_csv(repo / "data/reference/venues.csv")
    by_key = {row.get("venue_key", "").strip(): row for row in venues}
    used_ids = {row.get("venue_id", "").strip() for row in venues}
    next_number = max(venue_number(value) for value in used_ids) + 1

    specs: dict[str, dict[str, str]] = {
        "ou-gymnasium": {
            "venue_key": "ou-gymnasium",
            "display_name": "OU Gymnasium",
            "city": "Norman",
            "state": "OK",
            "opened": "1903",
            "closed": "",
            "date_precision": "YEAR",
            "identity_status": "RESEARCHED_OFFICIAL",
            "source_basis": SOURCE_BASIS,
            "notes": (
                "Oklahoma Athletics says the Gymnasium opened in 1903 and hosted "
                "OU's first basketball game on 1907-12-07; it was replaced as the "
                "home-game site by the R.O.T.C. Armory in 1919."
            ),
        },
        "ou-rotc-armory": {
            "venue_key": "ou-rotc-armory",
            "display_name": "R.O.T.C. Armory",
            "city": "Norman",
            "state": "OK",
            "opened": "1919",
            "closed": "",
            "date_precision": "YEAR",
            "identity_status": "RESEARCHED_OFFICIAL",
            "source_basis": SOURCE_BASIS,
            "notes": (
                "Oklahoma Athletics says the brick R.O.T.C. Armory was completed in "
                "spring 1919 and replaced the Gymnasium as OU's home-game site until "
                "the Field House opened for basketball on 1928-01-13."
            ),
        },
    }

    new_venues: list[dict[str, str]] = []
    new_names: list[dict[str, str]] = []
    resolved: dict[str, dict[str, str]] = {}

    for key in ("ou-gymnasium", "ou-rotc-armory"):
        spec = dict(specs[key])
        existing = by_key.get(key)
        if existing:
            for field in ("display_name", "city", "state"):
                if existing.get(field, "").strip() != spec[field]:
                    raise OklahomaHomeError(f"existing {key} conflicts on {field}")
            spec["venue_id"] = existing["venue_id"].strip()
        else:
            while f"VEN-{next_number:06d}" in used_ids:
                next_number += 1
            spec["venue_id"] = f"VEN-{next_number:06d}"
            used_ids.add(spec["venue_id"])
            next_number += 1
            new_venues.append({field: spec.get(field, "") for field in venue_fields})
            new_names.append(
                {
                    "venue_id": spec["venue_id"],
                    "venue_name": spec["display_name"],
                    "normalized_name": normalize_venue_name(spec["display_name"]),
                    "name_type": "PROJECT_DISPLAY",
                    "valid_from": "",
                    "valid_to": "",
                    "date_precision": "",
                    "source_basis": SOURCE_BASIS,
                    "notes": "",
                }
            )
            if key == "ou-rotc-armory":
                new_names.append(
                    {
                        "venue_id": spec["venue_id"],
                        "venue_name": "ROTC Armory",
                        "normalized_name": normalize_venue_name("ROTC Armory"),
                        "name_type": "HISTORICAL_OR_ALIAS",
                        "valid_from": "",
                        "valid_to": "",
                        "date_precision": "",
                        "source_basis": SOURCE_BASIS,
                        "notes": "Punctuation-free alias for R.O.T.C. Armory.",
                    }
                )
        resolved[key] = spec

    for key in ("mccasland-field-house", "lloyd-noble-center"):
        existing = by_key.get(key)
        if not existing:
            raise OklahomaHomeError(f"global venue registry missing required {key}")
        if (
            existing.get("city", "").strip(),
            existing.get("state", "").strip(),
        ) != NORMAN:
            raise OklahomaHomeError(f"{key} global geography is not Norman, OK")
        resolved[key] = dict(existing)

    return resolved, new_venues, new_names


def site_patch(
    existing: dict[str, str],
    facility: dict[str, str],
    *,
    canonical: bool,
) -> tuple[dict[str, str], str | None]:
    venue_name = facility["display_name"]
    city, state = facility["city"], facility["state"]

    if canonical:
        current_key = existing.get("venue_key", "").strip()
        current_id = existing.get("venue_id", "").strip()
        if current_key and current_key != facility["venue_key"]:
            return {}, f"existing_canonical_venue_key:{current_key}"
        if current_id and current_id != facility["venue_id"]:
            return {}, f"existing_canonical_venue_id:{current_id}"
    else:
        current_name = existing.get("curated_venue_name", "").strip()
        if current_name and normalize_venue_name(current_name) != normalize_venue_name(
            venue_name
        ):
            return {}, f"existing_curated_venue:{current_name}"

    current_city = existing.get("site_city" if canonical else "city", "").strip()
    current_state = existing.get("site_state" if canonical else "state", "").strip()
    if current_city and current_city != city:
        return {}, f"existing_city:{current_city}"
    if current_state and current_state != state:
        return {}, f"existing_state:{current_state}"

    patch: dict[str, str] = {}
    if canonical:
        if not existing.get("venue_key", "").strip():
            patch["venue_key"] = facility["venue_key"]
            patch["venue_id"] = facility["venue_id"]
        if not existing.get("site_city", "").strip():
            patch["site_city"] = city
        if not existing.get("site_state", "").strip():
            patch["site_state"] = state
    else:
        if not existing.get("curated_venue_name", "").strip():
            patch["curated_venue_name"] = venue_name
        if not existing.get("city", "").strip():
            patch["city"] = city
        if not existing.get("state", "").strip():
            patch["state"] = state
    return patch, None


def resolved_site_discrepancy(
    discrepancy_by_id: dict[str, dict[str, str]],
    *,
    discrepancy_id: str,
    canonical_game_id: str,
    canonical_site_type: str,
) -> dict[str, str]:
    row = discrepancy_by_id.get(discrepancy_id)
    if row is None:
        raise OklahomaHomeError(f"missing required reconciliation {discrepancy_id}")
    if row.get("canonical_game_id", "").strip() != canonical_game_id:
        raise OklahomaHomeError(f"{discrepancy_id}: canonical ID drift")
    if row.get("field_name", "").strip() != "site_type":
        raise OklahomaHomeError(f"{discrepancy_id}: expected site_type discrepancy")
    if row.get("status", "").strip() != "RESOLVED":
        raise OklahomaHomeError(f"{discrepancy_id}: site resolution is not RESOLVED")
    if row.get("source_a_program_key", "").strip() != PROGRAM:
        raise OklahomaHomeError(f"{discrepancy_id}: Oklahoma is not source_a_program_key")
    if row.get("canonical_value", "").strip() != canonical_site_type:
        raise OklahomaHomeError(
            f"{discrepancy_id}: canonical site value drift "
            f"({row.get('canonical_value','')!r} != {canonical_site_type!r})"
        )
    if not row.get("resolution_basis", "").strip():
        raise OklahomaHomeError(f"{discrepancy_id}: resolved site conflict lacks basis")
    return row


def build_plan(repo: Path) -> dict[str, Any]:
    facilities, new_venues, new_names = resolve_facilities(repo)
    _, sources = read_csv(repo / "schools/oklahoma/source-games.csv")
    _, assertions = read_csv(repo / "data/evidence/game-assertions.csv")
    _, canonical = read_csv(repo / "data/canonical/games.csv")
    _, discrepancies = read_csv(repo / "data/reconciliation/discrepancies.csv")

    source_gaps = [
        row
        for row in sources
        if row.get("curated_site_type", "").strip() == "SOURCE_PROGRAM_HOME"
        and (
            not row.get("curated_venue_name", "").strip()
            or not row.get("city", "").strip()
            or not row.get("state", "").strip()
        )
    ]
    canonical_gaps = [
        row
        for row in canonical
        if oklahoma_home(row)
        and (
            not row.get("venue_key", "").strip()
            or not row.get("venue_id", "").strip()
            or not row.get("site_city", "").strip()
            or not row.get("site_state", "").strip()
        )
    ]
    if len(source_gaps) != EXPECTED_SOURCE_HOME_GAPS:
        raise OklahomaHomeError(
            f"expected {EXPECTED_SOURCE_HOME_GAPS} Oklahoma source HOME gaps; "
            f"found {len(source_gaps)}"
        )
    if len(canonical_gaps) != EXPECTED_CANONICAL_HOME_GAPS:
        raise OklahomaHomeError(
            f"expected {EXPECTED_CANONICAL_HOME_GAPS} Oklahoma canonical HOME gaps; "
            f"found {len(canonical_gaps)}"
        )

    assertions_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertions:
        if row.get("source_program_key", "").strip() == PROGRAM:
            assertions_by_source[row.get("source_game_id", "").strip()].append(row)
    canonical_by_id = {
        row.get("canonical_game_id", "").strip(): row for row in canonical
    }
    discrepancy_by_id = {
        row.get("discrepancy_id", "").strip(): row for row in discrepancies
    }

    assignments: list[dict[str, Any]] = []
    canonical_only_assignments: list[dict[str, Any]] = []
    holds: list[dict[str, str]] = []
    source_facility_counts: Counter[str] = Counter()
    canonical_facility_counts: Counter[str] = Counter()
    canonical_patched_ids: set[str] = set()
    reconciled_source_conflicts: list[dict[str, str]] = []

    for source in source_gaps:
        source_id = source.get("source_game_id", "").strip()
        key, reason = facility_key_for(source)
        if not key:
            holds.append(
                {
                    "source_game_id": source_id,
                    "season_label": source.get("season_label", "").strip(),
                    "game_date": source.get("game_date", "").strip(),
                    "reason": reason or "chronology_unresolved",
                }
            )
            continue
        facility = facilities[key]
        source_patch, conflict = site_patch(source, facility, canonical=False)
        if conflict:
            holds.append(
                {
                    "source_game_id": source_id,
                    "season_label": source.get("season_label", "").strip(),
                    "game_date": source.get("game_date", "").strip(),
                    "reason": conflict,
                }
            )
            continue

        matches = assertions_by_source.get(source_id, [])
        if len(matches) != 1:
            holds.append(
                {
                    "source_game_id": source_id,
                    "season_label": source.get("season_label", "").strip(),
                    "game_date": source.get("game_date", "").strip(),
                    "reason": f"assertion_count:{len(matches)}",
                }
            )
            continue
        assertion = matches[0]
        assertion_patch, conflict = site_patch(assertion, facility, canonical=False)
        if conflict:
            holds.append(
                {
                    "source_game_id": source_id,
                    "season_label": source.get("season_label", "").strip(),
                    "game_date": source.get("game_date", "").strip(),
                    "reason": "assertion_" + conflict,
                }
            )
            continue

        canonical_id = assertion.get("canonical_game_id", "").strip()
        game = canonical_by_id.get(canonical_id)
        if not game:
            holds.append(
                {
                    "source_game_id": source_id,
                    "season_label": source.get("season_label", "").strip(),
                    "game_date": source.get("game_date", "").strip(),
                    "reason": "canonical_missing",
                }
            )
            continue

        canonical_patch: dict[str, str] = {}
        discrepancy_id = ""
        if oklahoma_home(game):
            canonical_patch, conflict = site_patch(game, facility, canonical=True)
            if conflict:
                holds.append(
                    {
                        "source_game_id": source_id,
                        "season_label": source.get("season_label", "").strip(),
                        "game_date": source.get("game_date", "").strip(),
                        "reason": "canonical_" + conflict,
                    }
                )
                continue
            canonical_patched_ids.add(canonical_id)
            canonical_facility_counts[key] += 1
        else:
            expected = RECONCILED_NON_OKLAHOMA_HOME.get(source_id)
            if expected is None:
                holds.append(
                    {
                        "source_game_id": source_id,
                        "season_label": source.get("season_label", "").strip(),
                        "game_date": source.get("game_date", "").strip(),
                        "reason": f"canonical_not_oklahoma_home:{game.get('site_type','')}",
                    }
                )
                continue
            if expected["canonical_game_id"] != canonical_id:
                raise OklahomaHomeError(f"{source_id}: reconciled canonical ID drift")
            if game.get("site_type", "").strip() != expected["canonical_site_type"]:
                raise OklahomaHomeError(f"{source_id}: reconciled canonical site drift")
            resolved_site_discrepancy(
                discrepancy_by_id,
                discrepancy_id=expected["discrepancy_id"],
                canonical_game_id=canonical_id,
                canonical_site_type=expected["canonical_site_type"],
            )
            discrepancy_id = expected["discrepancy_id"]
            reconciled_source_conflicts.append(
                {
                    "source_game_id": source_id,
                    "canonical_game_id": canonical_id,
                    "discrepancy_id": discrepancy_id,
                    "canonical_site_type": expected["canonical_site_type"],
                }
            )

        marker = (
            f"[OKLAHOMA_HOME_CHRONOLOGY source={source_id};"
            f"venue_key={facility['venue_key']};basis=official-ou-facilities-timeline]"
        )
        source_patch["notes"] = marker
        assertion_patch["notes"] = marker
        if canonical_patch:
            canonical_patch["notes"] = marker

        assignments.append(
            {
                "source_game_id": source_id,
                "canonical_game_id": canonical_id,
                "season_label": source.get("season_label", "").strip(),
                "game_date": source.get("game_date", "").strip(),
                "facility_key": key,
                "venue_id": facility["venue_id"],
                "resolved_site_discrepancy_id": discrepancy_id,
                "source_patch": source_patch,
                "assertion_patch": assertion_patch,
                "canonical_patch": canonical_patch,
            }
        )
        source_facility_counts[key] += 1

    canonical_gap_ids = {
        row.get("canonical_game_id", "").strip() for row in canonical_gaps
    }
    canonical_uncovered = canonical_gap_ids - canonical_patched_ids
    if canonical_uncovered != set(CANONICAL_ONLY_OKLAHOMA_HOME):
        holds.append(
            {
                "source_game_id": "",
                "season_label": "",
                "game_date": "",
                "reason": "canonical_only_universe:" + ",".join(sorted(canonical_uncovered)),
            }
        )
    else:
        for canonical_id in sorted(canonical_uncovered):
            expected = CANONICAL_ONLY_OKLAHOMA_HOME[canonical_id]
            game = canonical_by_id[canonical_id]
            if not oklahoma_home(game):
                raise OklahomaHomeError(f"{canonical_id}: expected canonical Oklahoma home")
            if game.get("site_type", "").strip() != expected["canonical_site_type"]:
                raise OklahomaHomeError(f"{canonical_id}: canonical-only site_type drift")
            resolved_site_discrepancy(
                discrepancy_by_id,
                discrepancy_id=expected["discrepancy_id"],
                canonical_game_id=canonical_id,
                canonical_site_type=expected["canonical_site_type"],
            )
            facility = facilities[expected["facility_key"]]
            patch, conflict = site_patch(game, facility, canonical=True)
            if conflict:
                holds.append(
                    {
                        "source_game_id": expected["source_game_id"],
                        "season_label": game.get("season_label", "").strip(),
                        "game_date": game.get("game_date", "").strip(),
                        "reason": "canonical_only_" + conflict,
                    }
                )
                continue
            marker = (
                f"[OKLAHOMA_HOME_CHRONOLOGY canonical={canonical_id};"
                f"venue_key={facility['venue_key']};"
                f"discrepancy={expected['discrepancy_id']};"
                "basis=official-ou-facilities-timeline]"
            )
            patch["notes"] = marker
            canonical_only_assignments.append(
                {
                    "canonical_game_id": canonical_id,
                    "source_game_id": expected["source_game_id"],
                    "facility_key": expected["facility_key"],
                    "venue_id": facility["venue_id"],
                    "resolved_site_discrepancy_id": expected["discrepancy_id"],
                    "canonical_patch": patch,
                }
            )
            canonical_patched_ids.add(canonical_id)
            canonical_facility_counts[expected["facility_key"]] += 1

    assignments.sort(key=lambda item: item["source_game_id"])
    canonical_only_assignments.sort(key=lambda item: item["canonical_game_id"])
    holds.sort(key=lambda item: (item.get("source_game_id", ""), item.get("reason", "")))
    reconciled_source_conflicts.sort(key=lambda item: item["source_game_id"])

    source_counts = dict(sorted(source_facility_counts.items()))
    canonical_counts = dict(sorted(canonical_facility_counts.items()))
    if not holds and source_counts != EXPECTED_SOURCE_FACILITY_COUNTS:
        raise OklahomaHomeError(
            f"source facility-count universe drift: {source_counts}"
        )
    if not holds and canonical_counts != EXPECTED_CANONICAL_FACILITY_COUNTS:
        raise OklahomaHomeError(
            f"canonical facility-count universe drift: {canonical_counts}"
        )
    if not holds and len(assignments) != EXPECTED_SOURCE_HOME_GAPS:
        raise OklahomaHomeError("source assignment universe is incomplete")
    if not holds and len(canonical_patched_ids) != EXPECTED_CANONICAL_HOME_GAPS:
        raise OklahomaHomeError("canonical assignment universe is incomplete")
    if not holds and len(reconciled_source_conflicts) != 2:
        raise OklahomaHomeError("expected exactly two reconciled source-site conflicts")
    if not holds and len(canonical_only_assignments) != 1:
        raise OklahomaHomeError("expected exactly one canonical-only Oklahoma-home repair")

    guarded = [
        "schools/oklahoma/source-games.csv",
        "schools/oklahoma/venues.csv",
        "data/evidence/game-assertions.csv",
        "data/canonical/games.csv",
        "data/reconciliation/discrepancies.csv",
        "data/reference/venues.csv",
        "data/reference/venue-names.csv",
        "tools/remediate_oklahoma_home_history.py",
    ]
    payload = {
        "plan_version": PLAN_VERSION,
        "git_head": git_head(repo),
        "inputs": {path: sha256_file(repo / path) for path in guarded},
        "expected_source_home_gaps": EXPECTED_SOURCE_HOME_GAPS,
        "expected_canonical_home_gaps": EXPECTED_CANONICAL_HOME_GAPS,
        "source_assignment_count": len(assignments),
        "canonical_assignment_count": len(canonical_patched_ids),
        "canonical_only_assignment_count": len(canonical_only_assignments),
        "reconciled_source_conflict_count": len(reconciled_source_conflicts),
        "hold_count": len(holds),
        "source_facility_counts": source_counts,
        "canonical_facility_counts": canonical_counts,
        "facilities": {
            key: {
                k: v
                for k, v in value.items()
                if k in {"venue_id", "venue_key", "display_name", "city", "state"}
            }
            for key, value in facilities.items()
        },
        "new_venues": new_venues,
        "new_venue_names": new_names,
        "reconciled_source_conflicts": reconciled_source_conflicts,
        "assignments": assignments,
        "canonical_only_assignments": canonical_only_assignments,
        "holds": holds,
    }
    return {"sha256": plan_hash(payload), "payload": payload}


def append_marker(existing: str, marker: str) -> str:
    existing = (existing or "").strip()
    if marker in existing:
        return existing
    return f"{existing} {marker}".strip()


def update_school_venue_rows(repo: Path, plan: dict[str, Any]) -> None:
    path = repo / "schools/oklahoma/venues.csv"
    fields, rows = read_csv(path)
    by_key = {row.get("venue_key", "").strip(): row for row in rows}
    max_index = max(
        (
            int(row.get("index", "-1"))
            for row in rows
            if row.get("index", "").isdigit()
        ),
        default=-1,
    )
    facilities = plan["payload"]["facilities"]

    relationship_specs = {
        "ou-gymnasium": {
            "venue_type": "gymnasium",
            "aliases": "",
            "relationship_type": "PRIMARY_HOME",
            "relationship_start": "1907-12-07",
            "relationship_end": "1919",
            "relationship_date_precision": "EXACT_START_YEAR_END",
            "site_rule": "Oklahoma source HOME during primary-home era.",
            "notes": (
                "Official OU facilities history: first basketball game here was "
                "1907-12-07; replaced as home site by the R.O.T.C. Armory in 1919."
            ),
        },
        "ou-rotc-armory": {
            "venue_type": "armory",
            "aliases": "ROTC Armory",
            "relationship_type": "PRIMARY_HOME",
            "relationship_start": "1919",
            "relationship_end": "1928-01-12",
            "relationship_date_precision": "YEAR_START_EXACT_END",
            "site_rule": "Oklahoma source HOME during primary-home era.",
            "notes": (
                "Official OU facilities history: Armory replaced the Gymnasium in "
                "1919; Field House's first game followed on 1928-01-13."
            ),
        },
        "mccasland-field-house": {
            "relationship_type": "PRIMARY_HOME_THEN_SPECIAL_HOME",
            "relationship_start": "1928-01-13",
            "relationship_end": "1975-11-30",
            "relationship_date_precision": "EXACT_PRIMARY_ERA",
            "site_rule": (
                "Primary Oklahoma home 1928-01-13 through 1975-11-30; later "
                "special home games require game-specific evidence."
            ),
        },
        "lloyd-noble-center": {
            "relationship_type": "PRIMARY_HOME",
            "relationship_start": "1975-12-01",
            "relationship_end": "",
            "relationship_date_precision": "EXACT_START",
            "site_rule": (
                "Primary Oklahoma home beginning 1975-12-01; modern McCasland "
                "special home exceptions remain game-specific."
            ),
        },
    }

    for key, spec in relationship_specs.items():
        facility = facilities[key]
        row = by_key.get(key)
        if row is None:
            max_index += 1
            row = {field: "" for field in fields}
            row.update(
                {
                    "index": str(max_index),
                    "source_program_key": PROGRAM,
                    "venue_key": key,
                    "venue_id": facility["venue_id"],
                    "canonical_name": facility["display_name"],
                    "city": facility["city"],
                    "state": facility["state"],
                    "source_basis": SOURCE_BASIS,
                }
            )
            rows.append(row)
            by_key[key] = row
        else:
            if row.get("venue_id", "").strip() != facility["venue_id"]:
                raise OklahomaHomeError(f"school venue row {key} has venue_id drift")
            for field in ("canonical_name", "city", "state"):
                expected = {
                    "canonical_name": facility["display_name"],
                    "city": facility["city"],
                    "state": facility["state"],
                }[field]
                current = row.get(field, "").strip()
                if current and current != expected:
                    raise OklahomaHomeError(
                        f"school venue row {key} conflicts on {field}: {current!r}"
                    )
                row[field] = expected
            row["source_basis"] = SOURCE_BASIS

        for field, value in spec.items():
            if field in fields:
                row[field] = value

    # Refresh source-assignment counts after source-games.csv has been patched.  Do not
    # manufacture first/last exact dates where early source rows are undated.
    _, sources = read_csv(repo / "schools/oklahoma/source-games.csv")
    for key in relationship_specs:
        row = by_key[key]
        canonical_name = row.get("canonical_name", "").strip()
        assigned = [
            source
            for source in sources
            if normalize_venue_name(source.get("curated_venue_name", ""))
            == normalize_venue_name(canonical_name)
        ]
        if "games_currently_assigned" in fields:
            row["games_currently_assigned"] = str(len(assigned))
        dates = sorted(
            source.get("game_date", "").strip()
            for source in assigned
            if source.get("game_date", "").strip()
        )
        any_missing_date = any(
            not source.get("game_date", "").strip() for source in assigned
        )
        if "first_assigned_game" in fields:
            row["first_assigned_game"] = "" if any_missing_date else (dates[0] if dates else "")
        if "last_assigned_game" in fields:
            row["last_assigned_game"] = dates[-1] if dates else ""

    write_csv_preserving(path, fields, rows)


def apply_patch(row: dict[str, str], patch: dict[str, str], *, label: str) -> None:
    marker = patch.get("notes", "")
    for field, value in patch.items():
        if field == "notes":
            continue
        current = row.get(field, "").strip()
        if current and current != value:
            raise OklahomaHomeError(
                f"{label}: refusing overwrite {field}={current!r} with {value!r}"
            )
        row[field] = value
    if marker:
        row["notes"] = append_marker(row.get("notes", ""), marker)


def apply_plan(
    repo: Path,
    expected_hash: str,
    *,
    run_validation: bool = True,
) -> dict[str, Any]:
    plan = build_plan(repo)
    if not expected_hash or plan["sha256"] != expected_hash:
        raise OklahomaHomeError(
            "sealed plan hash mismatch "
            f"(expected {expected_hash or '[blank]'}, actual {plan['sha256']})"
        )
    payload = plan["payload"]
    if payload["hold_count"]:
        raise OklahomaHomeError(
            f"refusing partial apply while {payload['hold_count']} hold(s) remain"
        )
    if payload["source_assignment_count"] != EXPECTED_SOURCE_HOME_GAPS:
        raise OklahomaHomeError("source assignment universe is not complete")
    if payload["canonical_assignment_count"] != EXPECTED_CANONICAL_HOME_GAPS:
        raise OklahomaHomeError("canonical assignment universe is not complete")
    if payload["reconciled_source_conflict_count"] != 2:
        raise OklahomaHomeError("reconciled source-conflict universe drift")
    if payload["canonical_only_assignment_count"] != 1:
        raise OklahomaHomeError("canonical-only assignment universe drift")

    write_paths = [
        repo / "schools/oklahoma/source-games.csv",
        repo / "schools/oklahoma/venues.csv",
        repo / "data/evidence/game-assertions.csv",
        repo / "data/canonical/games.csv",
        repo / "data/reference/venues.csv",
        repo / "data/reference/venue-names.csv",
    ]
    originals = {path: path.read_bytes() for path in write_paths}

    try:
        source_path, school_venue_path, assertion_path, canonical_path, venues_path, names_path = write_paths
        sf, sources = read_csv(source_path)
        af, assertions = read_csv(assertion_path)
        cf, canonical = read_csv(canonical_path)
        vf, venues = read_csv(venues_path)
        nf, names = read_csv(names_path)

        source_by_id = {
            row.get("source_game_id", "").strip(): row for row in sources
        }
        assertion_by_source = {
            row.get("source_game_id", "").strip(): row
            for row in assertions
            if row.get("source_program_key", "").strip() == PROGRAM
        }
        canonical_by_id = {
            row.get("canonical_game_id", "").strip(): row for row in canonical
        }

        existing_venue_ids = {
            row.get("venue_id", "").strip() for row in venues
        }
        for row in payload["new_venues"]:
            if row["venue_id"] not in existing_venue_ids:
                venues.append(row)
                existing_venue_ids.add(row["venue_id"])

        existing_name_rows = {
            (
                row.get("venue_id", "").strip(),
                row.get("venue_name", "").strip(),
                row.get("name_type", "").strip(),
            )
            for row in names
        }
        for row in payload["new_venue_names"]:
            identity = (row["venue_id"], row["venue_name"], row["name_type"])
            if identity not in existing_name_rows:
                names.append(row)
                existing_name_rows.add(identity)

        for item in payload["assignments"]:
            source = source_by_id[item["source_game_id"]]
            assertion = assertion_by_source[item["source_game_id"]]
            game = canonical_by_id[item["canonical_game_id"]]
            apply_patch(source, item["source_patch"], label=item["source_game_id"])
            apply_patch(
                assertion,
                item["assertion_patch"],
                label=f"assertion:{item['source_game_id']}",
            )
            if item["canonical_patch"]:
                apply_patch(
                    game,
                    item["canonical_patch"],
                    label=item["canonical_game_id"],
                )

        for item in payload["canonical_only_assignments"]:
            game = canonical_by_id[item["canonical_game_id"]]
            apply_patch(
                game,
                item["canonical_patch"],
                label=item["canonical_game_id"],
            )

        write_csv_preserving(venues_path, vf, venues)
        write_csv_preserving(names_path, nf, names)
        write_csv_preserving(source_path, sf, sources)
        write_csv_preserving(assertion_path, af, assertions)
        write_csv_preserving(canonical_path, cf, canonical)
        update_school_venue_rows(repo, plan)

        _, sources_after = read_csv(source_path)
        source_remaining = [
            row
            for row in sources_after
            if row.get("curated_site_type", "").strip() == "SOURCE_PROGRAM_HOME"
            and (
                not row.get("curated_venue_name", "").strip()
                or not row.get("city", "").strip()
                or not row.get("state", "").strip()
            )
        ]
        _, canonical_after = read_csv(canonical_path)
        canonical_remaining = [
            row
            for row in canonical_after
            if oklahoma_home(row)
            and (
                not row.get("venue_key", "").strip()
                or not row.get("venue_id", "").strip()
                or not row.get("site_city", "").strip()
                or not row.get("site_state", "").strip()
            )
        ]
        if source_remaining or canonical_remaining:
            raise OklahomaHomeError(
                "postcondition failed: "
                f"source HOME gaps={len(source_remaining)}, "
                f"canonical HOME gaps={len(canonical_remaining)}"
            )

        # Ensure the two historical site conflicts remain canonically untouched.
        for source_id, expected in RECONCILED_NON_OKLAHOMA_HOME.items():
            game = next(
                row
                for row in canonical_after
                if row.get("canonical_game_id", "").strip()
                == expected["canonical_game_id"]
            )
            if game.get("site_type", "").strip() != expected["canonical_site_type"]:
                raise OklahomaHomeError(
                    f"{source_id}: canonical resolved H/A/N changed unexpectedly"
                )

        if run_validation:
            completed = subprocess.run(
                [sys.executable, "tools/validate_data.py"], cwd=repo
            )
            if completed.returncode != 0:
                raise OklahomaHomeError("repository validation failed")

    except Exception:
        for path, data in originals.items():
            path.write_bytes(data)
        raise

    return {
        "applied_source_rows": payload["source_assignment_count"],
        "applied_canonical_rows": payload["canonical_assignment_count"],
        "plan_sha256": expected_hash,
    }


def write_plan(plan: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def print_plan(plan: dict[str, Any]) -> None:
    payload = plan["payload"]
    print("College Basketball History — Oklahoma historical HOME chronology plan")
    print(f"Git HEAD:                    {payload['git_head']}")
    print(f"Source HOME gaps:            {payload['expected_source_home_gaps']}")
    print(f"Canonical HOME gaps:         {payload['expected_canonical_home_gaps']}")
    print(f"Source assignments:          {payload['source_assignment_count']}")
    print(f"Canonical assignments:       {payload['canonical_assignment_count']}")
    print(f"Canonical-only assignments:  {payload['canonical_only_assignment_count']}")
    print(f"Reconciled source conflicts: {payload['reconciled_source_conflict_count']}")
    print(f"Holds:                       {payload['hold_count']}")
    print(
        "Source facility counts:       "
        + json.dumps(payload["source_facility_counts"], sort_keys=True)
    )
    print(
        "Canonical facility counts:    "
        + json.dumps(payload["canonical_facility_counts"], sort_keys=True)
    )
    print(
        "Facility identities:          "
        + json.dumps(payload["facilities"], sort_keys=True)
    )
    print(f"New global venues:           {len(payload['new_venues'])}")
    print(f"New global venue-name rows:  {len(payload['new_venue_names'])}")
    print(f"Plan SHA-256:                {plan['sha256']}")
    if payload["reconciled_source_conflicts"]:
        print("RECONCILED SOURCE-SITE CONFLICTS (canonical untouched):")
        for row in payload["reconciled_source_conflicts"]:
            print("  " + json.dumps(row, sort_keys=True))
    if payload["canonical_only_assignments"]:
        print("CANONICAL-ONLY HOME REPAIRS:")
        for row in payload["canonical_only_assignments"]:
            compact = {
                key: row[key]
                for key in (
                    "canonical_game_id",
                    "source_game_id",
                    "facility_key",
                    "venue_id",
                    "resolved_site_discrepancy_id",
                )
            }
            print("  " + json.dumps(compact, sort_keys=True))
    if payload["holds"]:
        print("HELD ROWS:")
        for row in payload["holds"]:
            print("  " + json.dumps(row, sort_keys=True))
    print("DRY RUN: no tracked basketball data changed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seal/apply Oklahoma historical HOME venue chronology."
    )
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-plan-sha256", default="")
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = (
        args.repo.resolve()
        if args.repo
        else Path(__file__).resolve().parents[1]
    )
    output = (
        args.output.resolve()
        if args.output
        else repo / ".onboarding/oklahoma-home-remediation/plan.json"
    )
    try:
        if args.apply:
            result = apply_plan(repo, args.expected_plan_sha256)
            print(
                "PASS: applied Oklahoma HOME chronology to "
                f"{result['applied_source_rows']} source row(s) and "
                f"{result['applied_canonical_rows']} canonical row(s); "
                f"sealed plan {result['plan_sha256']}"
            )
            return 0
        plan = build_plan(repo)
        write_plan(plan, output)
        print_plan(plan)
        print(f"Plan artifact:                {output}")
        return 0
    except (
        OklahomaHomeError,
        FileNotFoundError,
        ValueError,
        KeyError,
        StopIteration,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
