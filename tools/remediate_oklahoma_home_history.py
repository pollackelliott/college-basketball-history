#!/usr/bin/env python3
"""Plan and apply Oklahoma historical HOME venue/location remediation.

This tool is deliberately Oklahoma-specific.  It uses Oklahoma Athletics' official
four-venue home chronology only after a source/canonical row is independently
classified as Oklahoma HOME.  Venue/geography never establishes H/A/N.

Default mode is a dry-run that writes a sealed JSON plan.  ``--apply`` requires the
exact SHA-256 from that dry-run and refuses to proceed if any chronology row is held
for ambiguity or conflict.
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
PLAN_VERSION = 1
NORMAN = ("Norman", "OK")
FIELD_HOUSE_FIRST = "1928-01-13"
LLOYD_NOBLE_FIRST = "1975-12-01"
SOURCE_BASIS = (
    "Oklahoma Athletics men's basketball facilities timeline: OU Gymnasium "
    "(1907-1919), R.O.T.C. Armory (1919-1928), OU Field House/McCasland "
    "(1928-1975), Lloyd Noble Center (1975-present); Field House first game "
    "1928-01-13 and Lloyd Noble opened for basketball in December 1975."
)


class OklahomaHomeError(RuntimeError):
    pass


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head(repo: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()


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
        site == "TEAM_A_HOME" and canonical.get("team_a_key", "").strip() == PROGRAM
    ) or (
        site == "TEAM_B_HOME" and canonical.get("team_b_key", "").strip() == PROGRAM
    )


def facility_key_for(row: dict[str, str]) -> tuple[str | None, str | None]:
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
            return None, "1927-28_transition_missing_date"
        return ("ou-rotc-armory" if date < FIELD_HOUSE_FIRST else "mccasland-field-house"), None
    if "1928-1929" <= season <= "1974-1975":
        return "mccasland-field-house", None
    if season == "1975-1976":
        if not date:
            return None, "1975-76_transition_missing_date"
        return ("mccasland-field-house" if date < LLOYD_NOBLE_FIRST else "lloyd-noble-center"), None

    # The primary-home chronology alone is not used to fill later blank rows because
    # modern Oklahoma has intentionally staged some HOME games in McCasland Field House.
    # Modern blank rows therefore require game-specific research rather than a blanket
    # Lloyd Noble fallback.
    return None, "post_1975_primary_history_not_sufficient"


def resolve_facilities(repo: Path) -> tuple[dict[str, dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    venue_fields, venues = read_csv(repo / "data/reference/venues.csv")
    _, venue_names = read_csv(repo / "data/reference/venue-names.csv")
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
            "notes": "Oklahoma Athletics identifies this as the Sooners' home venue from 1907 through 1919.",
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
            "notes": "Oklahoma Athletics identifies the R.O.T.C. Armory as the home site after the Gymnasium and before the Field House.",
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
        resolved[key] = spec

    for key in ("mccasland-field-house", "lloyd-noble-center"):
        existing = by_key.get(key)
        if not existing:
            raise OklahomaHomeError(f"global venue registry missing required {key}")
        if (existing.get("city", "").strip(), existing.get("state", "").strip()) != NORMAN:
            raise OklahomaHomeError(f"{key} global geography is not Norman, OK")
        resolved[key] = dict(existing)

    return resolved, new_venues, new_names


def site_patch(existing: dict[str, str], facility: dict[str, str], *, canonical: bool) -> tuple[dict[str, str], str | None]:
    venue_name = facility["display_name"]
    city, state = facility["city"], facility["state"]
    venue_field = "venue_key" if canonical else "curated_venue_name"

    if canonical:
        current_key = existing.get("venue_key", "").strip()
        current_id = existing.get("venue_id", "").strip()
        if current_key and current_key != facility["venue_key"]:
            return {}, f"existing_canonical_venue_key:{current_key}"
        if current_id and current_id != facility["venue_id"]:
            return {}, f"existing_canonical_venue_id:{current_id}"
    else:
        current_name = existing.get("curated_venue_name", "").strip()
        if current_name and normalize_venue_name(current_name) != normalize_venue_name(venue_name):
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


def build_plan(repo: Path) -> dict[str, Any]:
    facilities, new_venues, new_names = resolve_facilities(repo)
    source_fields, sources = read_csv(repo / "schools/oklahoma/source-games.csv")
    _, assertions = read_csv(repo / "data/evidence/game-assertions.csv")
    _, canonical = read_csv(repo / "data/canonical/games.csv")

    source_gaps = [
        row for row in sources
        if row.get("curated_site_type", "").strip() == "SOURCE_PROGRAM_HOME"
        and (
            not row.get("curated_venue_name", "").strip()
            or not row.get("city", "").strip()
            or not row.get("state", "").strip()
        )
    ]
    canonical_gaps = [
        row for row in canonical
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
            f"expected {EXPECTED_SOURCE_HOME_GAPS} Oklahoma source HOME gaps; found {len(source_gaps)}"
        )
    if len(canonical_gaps) != EXPECTED_CANONICAL_HOME_GAPS:
        raise OklahomaHomeError(
            f"expected {EXPECTED_CANONICAL_HOME_GAPS} Oklahoma canonical HOME gaps; found {len(canonical_gaps)}"
        )

    assertions_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertions:
        if row.get("source_program_key", "").strip() == PROGRAM:
            assertions_by_source[row.get("source_game_id", "").strip()].append(row)
    canonical_by_id = {row["canonical_game_id"].strip(): row for row in canonical}

    assignments: list[dict[str, Any]] = []
    holds: list[dict[str, str]] = []
    facility_counts: Counter[str] = Counter()

    for source in source_gaps:
        source_id = source.get("source_game_id", "").strip()
        key, reason = facility_key_for(source)
        if not key:
            holds.append({
                "source_game_id": source_id,
                "season_label": source.get("season_label", "").strip(),
                "game_date": source.get("game_date", "").strip(),
                "reason": reason or "chronology_unresolved",
            })
            continue
        facility = facilities[key]
        source_patch, conflict = site_patch(source, facility, canonical=False)
        if conflict:
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "game_date": source.get("game_date", ""), "reason": conflict})
            continue

        matches = assertions_by_source.get(source_id, [])
        if len(matches) != 1:
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "game_date": source.get("game_date", ""), "reason": f"assertion_count:{len(matches)}"})
            continue
        assertion = matches[0]
        assertion_patch, conflict = site_patch(assertion, facility, canonical=False)
        if conflict:
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "game_date": source.get("game_date", ""), "reason": "assertion_" + conflict})
            continue

        canonical_id = assertion.get("canonical_game_id", "").strip()
        game = canonical_by_id.get(canonical_id)
        if not game:
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "game_date": source.get("game_date", ""), "reason": "canonical_missing"})
            continue
        if not oklahoma_home(game):
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "game_date": source.get("game_date", ""), "reason": f"canonical_not_oklahoma_home:{game.get('site_type','')}"})
            continue
        canonical_patch, conflict = site_patch(game, facility, canonical=True)
        if conflict:
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "game_date": source.get("game_date", ""), "reason": "canonical_" + conflict})
            continue

        marker = (
            f"[OKLAHOMA_HOME_CHRONOLOGY source={source_id};venue_key={facility['venue_key']};"
            f"basis=official-ou-facilities-timeline]"
        )
        source_patch["notes"] = marker
        assertion_patch["notes"] = marker
        if canonical_patch:
            canonical_patch["notes"] = marker

        assignments.append({
            "source_game_id": source_id,
            "canonical_game_id": canonical_id,
            "season_label": source.get("season_label", "").strip(),
            "game_date": source.get("game_date", "").strip(),
            "facility_key": key,
            "venue_id": facility["venue_id"],
            "source_patch": source_patch,
            "assertion_patch": assertion_patch,
            "canonical_patch": canonical_patch,
        })
        facility_counts[key] += 1

    assignments.sort(key=lambda item: item["source_game_id"])
    holds.sort(key=lambda item: item["source_game_id"])

    guarded = [
        "schools/oklahoma/source-games.csv",
        "schools/oklahoma/venues.csv",
        "data/evidence/game-assertions.csv",
        "data/canonical/games.csv",
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
        "assignment_count": len(assignments),
        "hold_count": len(holds),
        "facility_counts": dict(sorted(facility_counts.items())),
        "facilities": {key: {k: v for k, v in value.items() if k in {"venue_id", "venue_key", "display_name", "city", "state"}} for key, value in facilities.items()},
        "new_venues": new_venues,
        "new_venue_names": new_names,
        "assignments": assignments,
        "holds": holds,
    }
    return {"sha256": plan_hash(payload), "payload": payload}


def append_marker(existing: str, marker: str) -> str:
    existing = (existing or "").strip()
    if marker in existing:
        return existing
    return f"{existing} {marker}".strip()


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


def add_school_venue_rows(repo: Path, plan: dict[str, Any]) -> None:
    path = repo / "schools/oklahoma/venues.csv"
    fields, rows = read_csv(path)
    by_key = {row.get("venue_key", "").strip(): row for row in rows}
    max_index = max((int(row.get("index", "-1")) for row in rows if row.get("index", "").isdigit()), default=-1)
    facilities = plan["payload"]["facilities"]
    additions = [
        ("ou-gymnasium", "1907-1919 primary home venue; first OU basketball game there was 1907-12-07."),
        ("ou-rotc-armory", "1919-1928 primary home venue; replaced by OU Field House beginning 1928-01-13."),
    ]
    for key, note in additions:
        facility = facilities[key]
        if key in by_key:
            continue
        max_index += 1
        row = {field: "" for field in fields}
        row.update({
            "index": str(max_index),
            "source_program_key": PROGRAM,
            "venue_key": key,
            "venue_id": facility["venue_id"],
            "canonical_name": facility["display_name"],
            "aliases": "",
            "city": "Norman",
            "state": "OK",
            "venue_type": "gymnasium" if key == "ou-gymnasium" else "armory",
            "source_basis": SOURCE_BASIS,
            "notes": note,
        })
        rows.append(row)
    write_csv_preserving(path, fields, rows)


def apply_plan(repo: Path, expected_hash: str, *, run_validation: bool = True) -> dict[str, Any]:
    plan = build_plan(repo)
    if not expected_hash or plan["sha256"] != expected_hash:
        raise OklahomaHomeError(
            f"sealed plan hash mismatch (expected {expected_hash or '[blank]'}, actual {plan['sha256']})"
        )
    payload = plan["payload"]
    if payload["hold_count"]:
        raise OklahomaHomeError(f"refusing partial apply while {payload['hold_count']} chronology hold(s) remain")
    if payload["assignment_count"] != EXPECTED_SOURCE_HOME_GAPS:
        raise OklahomaHomeError("assignment universe is not the full expected Oklahoma HOME gap set")

    paths = [
        repo / "schools/oklahoma/source-games.csv",
        repo / "schools/oklahoma/venues.csv",
        repo / "data/evidence/game-assertions.csv",
        repo / "data/canonical/games.csv",
        repo / "data/reference/venues.csv",
        repo / "data/reference/venue-names.csv",
    ]
    originals = {path: path.read_bytes() for path in paths}

    try:
        source_path, school_venue_path, assertion_path, canonical_path, venues_path, names_path = paths
        sf, sources = read_csv(source_path)
        af, assertions = read_csv(assertion_path)
        cf, canonical = read_csv(canonical_path)
        vf, venues = read_csv(venues_path)
        nf, names = read_csv(names_path)

        source_by_id = {row.get("source_game_id", "").strip(): row for row in sources}
        assertion_by_source = {
            row.get("source_game_id", "").strip(): row
            for row in assertions if row.get("source_program_key", "").strip() == PROGRAM
        }
        canonical_by_id = {row.get("canonical_game_id", "").strip(): row for row in canonical}

        existing_venue_ids = {row.get("venue_id", "").strip() for row in venues}
        for row in payload["new_venues"]:
            if row["venue_id"] not in existing_venue_ids:
                venues.append(row)
                existing_venue_ids.add(row["venue_id"])
        existing_name_pairs = {(row.get("venue_id", "").strip(), row.get("name_type", "").strip()) for row in names}
        for row in payload["new_venue_names"]:
            pair = (row["venue_id"], row["name_type"])
            if pair not in existing_name_pairs:
                names.append(row)
                existing_name_pairs.add(pair)

        for item in payload["assignments"]:
            source = source_by_id[item["source_game_id"]]
            assertion = assertion_by_source[item["source_game_id"]]
            game = canonical_by_id[item["canonical_game_id"]]
            for row, patch in (
                (source, item["source_patch"]),
                (assertion, item["assertion_patch"]),
                (game, item["canonical_patch"]),
            ):
                marker = patch.get("notes", "")
                for field, value in patch.items():
                    if field == "notes":
                        continue
                    current = row.get(field, "").strip()
                    if current and current != value:
                        raise OklahomaHomeError(
                            f"{item['source_game_id']}: refusing overwrite {field}={current!r}"
                        )
                    row[field] = value
                if marker:
                    row["notes"] = append_marker(row.get("notes", ""), marker)

        write_csv_preserving(venues_path, vf, venues)
        write_csv_preserving(names_path, nf, names)
        add_school_venue_rows(repo, plan)
        write_csv_preserving(source_path, sf, sources)
        write_csv_preserving(assertion_path, af, assertions)
        write_csv_preserving(canonical_path, cf, canonical)

        post = build_plan(repo)
        # After successful application there must be no source/canonical HOME gaps;
        # the pre-apply expected-count guard will naturally no longer hold, so verify
        # directly instead of expecting a second plan build to reproduce the baseline.
    except OklahomaHomeError as exc:
        if "expected 634 Oklahoma source HOME gaps" not in str(exc):
            for path, data in originals.items():
                path.write_bytes(data)
            raise
    except Exception:
        for path, data in originals.items():
            path.write_bytes(data)
        raise

    # Direct postconditions.
    _, sources_after = read_csv(repo / "schools/oklahoma/source-games.csv")
    source_remaining = [
        row for row in sources_after
        if row.get("curated_site_type", "").strip() == "SOURCE_PROGRAM_HOME"
        and (
            not row.get("curated_venue_name", "").strip()
            or not row.get("city", "").strip()
            or not row.get("state", "").strip()
        )
    ]
    _, canonical_after = read_csv(repo / "data/canonical/games.csv")
    canonical_remaining = [
        row for row in canonical_after
        if oklahoma_home(row)
        and (
            not row.get("venue_key", "").strip()
            or not row.get("venue_id", "").strip()
            or not row.get("site_city", "").strip()
            or not row.get("site_state", "").strip()
        )
    ]
    if source_remaining or canonical_remaining:
        for path, data in originals.items():
            path.write_bytes(data)
        raise OklahomaHomeError(
            f"postcondition failed: source HOME gaps={len(source_remaining)}, canonical HOME gaps={len(canonical_remaining)}"
        )

    if run_validation:
        completed = subprocess.run([sys.executable, "tools/validate_data.py"], cwd=repo)
        if completed.returncode != 0:
            for path, data in originals.items():
                path.write_bytes(data)
            raise OklahomaHomeError("repository validation failed; changes rolled back")

    return {"applied_source_rows": len(payload["assignments"]), "plan_sha256": expected_hash}


def write_plan(plan: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def print_plan(plan: dict[str, Any]) -> None:
    payload = plan["payload"]
    print("College Basketball History — Oklahoma historical HOME chronology plan")
    print(f"Git HEAD:                 {payload['git_head']}")
    print(f"Source HOME gaps:         {payload['expected_source_home_gaps']}")
    print(f"Canonical HOME gaps:      {payload['expected_canonical_home_gaps']}")
    print(f"Assignments:              {payload['assignment_count']}")
    print(f"Holds:                    {payload['hold_count']}")
    print("Facility counts:          " + json.dumps(payload["facility_counts"], sort_keys=True))
    print("Facility identities:      " + json.dumps(payload["facilities"], sort_keys=True))
    print(f"New global venues:        {len(payload['new_venues'])}")
    print(f"Plan SHA-256:             {plan['sha256']}")
    if payload["holds"]:
        print("HELD ROWS:")
        for row in payload["holds"]:
            print("  " + json.dumps(row, sort_keys=True))
    print("DRY RUN: no tracked basketball data changed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seal/apply Oklahoma historical HOME venue chronology.")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-plan-sha256", default="")
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    output = args.output.resolve() if args.output else repo / ".onboarding/oklahoma-home-remediation/plan.json"
    try:
        if args.apply:
            result = apply_plan(repo, args.expected_plan_sha256)
            print(
                f"PASS: applied Oklahoma HOME chronology to {result['applied_source_rows']} source row(s); "
                f"sealed plan {result['plan_sha256']}"
            )
            return 0
        plan = build_plan(repo)
        write_plan(plan, output)
        print_plan(plan)
        print(f"Plan artifact:             {output}")
        return 0
    except (OklahomaHomeError, FileNotFoundError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
