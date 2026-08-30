#!/usr/bin/env python3
"""Plan/apply Mississippi State published-HOME site remediation.

The transaction resolves the exact current Mississippi State HOME blocker universe
without inventing unsupported historical venue identities.

Owner-approved policy:
- HOME city/state remain mandatory.
- An exact physical venue may remain blank only under
  RESEARCHED_UNRESOLVED_HOME_VENUE after exhaustive research.
- Venue chronology never infers H/A/N.

Research basis used here:
- Mississippi State official history says the program had no indoor basketball court
  or training facility until 1920 and identifies the Tin Gym as the first permanent
  gymnasium, with the established basketball relationship beginning 1932-01-25.
- McCarthy Gymnasium begins 1950-12-15; Humphrey Coliseum begins 1975-12-01.
- Mississippi State Athletics identifies Mississippi Coliseum in Jackson as the site
  of its Jackson basketball series beginning 1962-12-15.
- Pre-1962 Jackson game locations are established, but the surviving evidence checked
  does not safely identify a specific physical venue.
- UK Athletics' official all-time results marks both 1928-29 Mississippi A&M games as
  Kentucky away games; Mississippi State places the 32-14 game in Jackson. Under the
  existing owner-approved Jackson convention, CBBG-0014851 is Mississippi State HOME,
  not Kentucky HOME at Alumni Gym. Its date conflict remains preserved separately.

Default mode writes an ignored sealed plan. --apply requires the exact plan hash and
refuses partial/conflicting writes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROGRAM = "mississippi-state"
PLAN_VERSION = 1

EXPECTED_SOURCE_HOME_GAPS = 159
EXPECTED_CANONICAL_HOME_GAPS = 168
EXPECTED_SOURCE_EXCEPTIONS = 139
EXPECTED_SOURCE_COLISEUM = 20
EXPECTED_SOURCE_MAPPED_CURRENT_GAPS = 158
EXPECTED_CURRENT_CANONICAL_EXCEPTIONS = 138
EXPECTED_CANONICAL_COLISEUM = 20
EXPECTED_CANONICAL_ONLY = 10
EXPECTED_KENTUCKY_RECONCILIATION = "CBBG-0014851"
EXPECTED_POST_APPLY_GLOBAL_HARD_HOME = 783
EXPECTED_POST_APPLY_MS_EXCEPTIONS = 139

EXCEPTION_STATUS = "RESEARCHED_UNRESOLVED_HOME_VENUE"
EXCEPTION_MARKER = "[RESEARCHED_UNRESOLVED_HOME_VENUE"

MISSISSIPPI_COLISEUM = {
    "venue_key": "mississippi-coliseum",
    "venue_id": "VEN-000343",
    "display_name": "Mississippi Coliseum",
    "city": "Jackson",
    "state": "MS",
}

PRIMARY_FACILITIES = {
    "tin-gym": {
        "venue_key": "tin-gym",
        "venue_id": "VEN-000252",
        "display_name": "Tin Gym",
        "city": "Starkville",
        "state": "MS",
    },
    "mccarthy-gymnasium": {
        "venue_key": "mccarthy-gymnasium",
        "venue_id": "VEN-000250",
        "display_name": "McCarthy Gymnasium",
        "city": "Starkville",
        "state": "MS",
    },
    "humphrey-coliseum": {
        "venue_key": "humphrey-coliseum",
        "venue_id": "VEN-000087",
        "display_name": "Humphrey Coliseum",
        "city": "Starkville",
        "state": "MS",
    },
}

STARKVILLE_EXCEPTION_BASIS = (
    "Mississippi State official record book and institutional basketball/facility history, "
    "known home-venue chronology, reciprocal published evidence, and available archival "
    "material were reviewed. Mississippi State establishes Starkville, MS HOME context; "
    "its history says the program had no indoor basketball court/training facility until "
    "1920 and identifies the later Tin Gym as the first permanent gymnasium. The surviving "
    "record does not safely identify the exact physical home venue for this pre-Tin game."
)
JACKSON_EXCEPTION_BASIS = (
    "Mississippi State official record book/game history, Mississippi State's Jackson-site "
    "history, reciprocal published evidence, and Jackson facility history were reviewed. "
    "Jackson, MS is established and the owner-approved Jackson convention establishes "
    "Mississippi State HOME against an out-of-state opponent, but the surviving pre-1962 "
    "record does not safely identify the exact physical venue. Mississippi Coliseum is not "
    "back-projected before its documented 1962 basketball relationship."
)
COLISEUM_BASIS = (
    "Mississippi State Athletics official Jackson basketball history identifies Mississippi "
    "Coliseum as the Jackson venue beginning with Memphis State on 1962-12-15; Mississippi "
    "Fairgrounds history corroborates the building as a 1962 facility."
)
KENTUCKY_RECONCILIATION_BASIS = (
    "UK Athletics official 1928-29 all-time results marks both Mississippi A&M games as "
    "Kentucky away games; Mississippi State's official ledger places the 32-14 game in "
    "Jackson. Under the owner-approved Mississippi State Jackson convention, the canonical "
    "Kentucky-HOME/Alumni Gym assignment is rejected and Mississippi State HOME in Jackson "
    "controls. The 1929-02-02 versus 1929-02-03 source-date disagreement is preserved and "
    "is not altered by this site-only remediation."
)


class MississippiStateHomeError(RuntimeError):
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


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def plan_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def git_head(repo: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()


def append_note(existing: str, addition: str) -> str:
    existing = (existing or "").strip()
    if addition in existing:
        return existing
    return f"{existing} {addition}".strip()


def require_blank_or_expected(row: dict[str, str], field: str, expected: str, context: str) -> None:
    current = row.get(field, "").strip()
    if current and current != expected:
        raise MississippiStateHomeError(
            f"{context}: refusing conflicting {field}={current!r}; expected {expected!r}"
        )


def canonical_home(row: dict[str, str]) -> bool:
    site = row.get("site_type", "").strip()
    return (
        site == "TEAM_A_HOME" and row.get("team_a_key", "").strip() == PROGRAM
    ) or (
        site == "TEAM_B_HOME" and row.get("team_b_key", "").strip() == PROGRAM
    )


def canonical_home_site_type(row: dict[str, str]) -> str:
    if row.get("team_a_key", "").strip() == PROGRAM:
        return "TEAM_A_HOME"
    if row.get("team_b_key", "").strip() == PROGRAM:
        return "TEAM_B_HOME"
    raise MississippiStateHomeError(
        f"{row.get('canonical_game_id', '[unknown]')}: Mississippi State is not a participant"
    )


def source_gap(row: dict[str, str]) -> bool:
    return (
        row.get("curated_site_type", "").strip() == "SOURCE_PROGRAM_HOME"
        and (
            not row.get("curated_venue_name", "").strip()
            or not row.get("city", "").strip()
            or not row.get("state", "").strip()
        )
    )


def canonical_gap(row: dict[str, str]) -> bool:
    return canonical_home(row) and (
        not row.get("venue_id", "").strip()
        or not row.get("site_city", "").strip()
        or not row.get("site_state", "").strip()
    )


def primary_for_date(game_date: str) -> dict[str, str] | None:
    if not game_date:
        return None
    if "1932-01-25" <= game_date < "1950-12-15":
        return PRIMARY_FACILITIES["tin-gym"]
    if "1950-12-15" <= game_date < "1975-12-01":
        return PRIMARY_FACILITIES["mccarthy-gymnasium"]
    if game_date >= "1975-12-01":
        return PRIMARY_FACILITIES["humphrey-coliseum"]
    return None


def classify_source_gap(row: dict[str, str]) -> tuple[str, dict[str, str] | None, str]:
    city = row.get("city", "").strip()
    state = row.get("state", "").strip()
    date = row.get("game_date", "").strip()
    if (city, state) == ("Jackson", "MS"):
        if date >= "1962-12-15":
            return "ASSIGN_VENUE", MISSISSIPPI_COLISEUM, COLISEUM_BASIS
        return "UNRESOLVED_HOME_VENUE", None, JACKSON_EXCEPTION_BASIS
    if (city, state) == ("Starkville", "MS"):
        facility = primary_for_date(date)
        if facility is not None:
            return "ASSIGN_VENUE", facility, "Established Mississippi State primary-home chronology."
        return "UNRESOLVED_HOME_VENUE", None, STARKVILLE_EXCEPTION_BASIS
    return "HOLD", None, f"unsupported HOME geography {city!r}, {state!r}"


def marker(source_game_id: str) -> str:
    return f"[RESEARCHED_UNRESOLVED_HOME_VENUE source={PROGRAM}/{source_game_id}]"


def build_plan(repo: Path) -> dict[str, Any]:
    _, source_rows = read_csv(repo / "schools/mississippi-state/source-games.csv")
    _, canonical_rows = read_csv(repo / "data/canonical/games.csv")
    _, assertion_rows = read_csv(repo / "data/evidence/game-assertions.csv")
    _, discrepancy_rows = read_csv(repo / "data/reconciliation/discrepancies.csv")
    _, global_venues = read_csv(repo / "data/reference/venues.csv")
    _, school_venues = read_csv(repo / "schools/mississippi-state/venues.csv")

    source_gaps = [r for r in source_rows if source_gap(r)]
    canonical_gaps = [r for r in canonical_rows if canonical_gap(r)]
    canonical_by_id = {
        r.get("canonical_game_id", "").strip(): r
        for r in canonical_rows
        if r.get("canonical_game_id", "").strip()
    }
    canonical_gap_ids = {
        r.get("canonical_game_id", "").strip() for r in canonical_gaps
    }

    assertion_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertion_rows:
        if row.get("source_program_key", "").strip() == PROGRAM:
            assertion_by_source[row.get("source_game_id", "").strip()].append(row)

    errors: list[str] = []
    holds: list[dict[str, str]] = []
    assignments: list[dict[str, Any]] = []

    if len(source_gaps) != EXPECTED_SOURCE_HOME_GAPS:
        errors.append(f"source HOME gap count drift: {len(source_gaps)} != {EXPECTED_SOURCE_HOME_GAPS}")
    if len(canonical_gaps) != EXPECTED_CANONICAL_HOME_GAPS:
        errors.append(
            f"canonical HOME gap count drift: {len(canonical_gaps)} != {EXPECTED_CANONICAL_HOME_GAPS}"
        )

    global_by_id = {r.get("venue_id", "").strip(): r for r in global_venues}
    global_by_key = {r.get("venue_key", "").strip(): r for r in global_venues}
    if MISSISSIPPI_COLISEUM["venue_id"] in global_by_id:
        existing = global_by_id[MISSISSIPPI_COLISEUM["venue_id"]]
        if existing.get("venue_key", "").strip() != MISSISSIPPI_COLISEUM["venue_key"]:
            errors.append(
                f"{MISSISSIPPI_COLISEUM['venue_id']} already belongs to "
                f"{existing.get('venue_key', '').strip()}"
            )
    elif MISSISSIPPI_COLISEUM["venue_key"] in global_by_key:
        errors.append(
            "Mississippi Coliseum key already exists under a different VEN identity: "
            + global_by_key[MISSISSIPPI_COLISEUM["venue_key"]].get("venue_id", "")
        )

    school_by_key = {r.get("venue_key", "").strip(): r for r in school_venues}
    existing_school_coliseum = school_by_key.get(MISSISSIPPI_COLISEUM["venue_key"])
    if existing_school_coliseum and (
        existing_school_coliseum.get("venue_id", "").strip() != MISSISSIPPI_COLISEUM["venue_id"]
    ):
        errors.append("school Mississippi Coliseum venue identity conflicts with planned VEN ID")

    for facility in PRIMARY_FACILITIES.values():
        row = global_by_id.get(facility["venue_id"])
        if row is None:
            errors.append(f"missing global primary venue {facility['venue_id']}")
            continue
        for field in ("venue_key", "city", "state"):
            if row.get(field, "").strip() != facility[field]:
                errors.append(
                    f"global primary venue drift {facility['venue_id']} {field}: "
                    f"{row.get(field, '').strip()!r} != {facility[field]!r}"
                )

    mapped_current: set[str] = set()
    mapped_outside: set[str] = set()
    seen_canonical: set[str] = set()

    for source in sorted(
        source_gaps,
        key=lambda r: (r.get("game_date", ""), r.get("source_game_id", "")),
    ):
        sid = source.get("source_game_id", "").strip()
        action, facility, basis = classify_source_gap(source)
        if action == "HOLD":
            holds.append({"source_game_id": sid, "reason": basis})
            continue
        assertions = assertion_by_source.get(sid, [])
        if len(assertions) != 1:
            holds.append({"source_game_id": sid, "reason": f"assertion_count:{len(assertions)}"})
            continue
        assertion = assertions[0]
        if assertion.get("curated_site_type", "").strip() != "SOURCE_PROGRAM_HOME":
            holds.append({
                "source_game_id": sid,
                "reason": "assertion_not_source_program_home",
            })
            continue
        cid = assertion.get("canonical_game_id", "").strip()
        if not cid or cid not in canonical_by_id:
            holds.append({"source_game_id": sid, "reason": f"canonical_missing:{cid}"})
            continue
        if cid in seen_canonical:
            holds.append({"source_game_id": sid, "reason": f"duplicate_canonical_mapping:{cid}"})
            continue
        seen_canonical.add(cid)
        canonical = canonical_by_id[cid]
        in_current_gap = cid in canonical_gap_ids
        if in_current_gap:
            if not canonical_home(canonical):
                holds.append({"source_game_id": sid, "reason": f"current_gap_not_ms_home:{cid}"})
                continue
            mapped_current.add(cid)
        else:
            mapped_outside.add(cid)
            if cid != EXPECTED_KENTUCKY_RECONCILIATION:
                holds.append({"source_game_id": sid, "reason": f"unexpected_mapping_outside_gap:{cid}"})
                continue
            if {canonical.get("team_a_key", "").strip(), canonical.get("team_b_key", "").strip()} != {
                "kentucky", PROGRAM
            }:
                holds.append({"source_game_id": sid, "reason": "kentucky_reconciliation_participants_drift"})
                continue

        assignments.append({
            "source_game_id": sid,
            "canonical_game_id": cid,
            "season_label": source.get("season_label", "").strip(),
            "game_date": source.get("game_date", "").strip(),
            "opponent_key": source.get("normalized_opponent_key", "").strip(),
            "city": source.get("city", "").strip(),
            "state": source.get("state", "").strip(),
            "action": action,
            "facility": facility,
            "research_basis": basis,
            "in_current_canonical_gap": in_current_gap,
        })

    canonical_only_ids = sorted(canonical_gap_ids - mapped_current)
    canonical_only_assignments: list[dict[str, Any]] = []
    for cid in canonical_only_ids:
        canonical = canonical_by_id[cid]
        facility = primary_for_date(canonical.get("game_date", "").strip())
        if facility is None:
            holds.append({"canonical_game_id": cid, "reason": "canonical_only_outside_primary_chronology"})
            continue
        canonical_only_assignments.append({
            "canonical_game_id": cid,
            "season_label": canonical.get("season_label", "").strip(),
            "game_date": canonical.get("game_date", "").strip(),
            "facility": facility,
        })

    source_action_counts = Counter(a["action"] for a in assignments)
    current_exception_count = sum(
        1 for a in assignments
        if a["in_current_canonical_gap"] and a["action"] == "UNRESOLVED_HOME_VENUE"
    )
    current_coliseum_count = sum(
        1 for a in assignments
        if a["in_current_canonical_gap"]
        and a["action"] == "ASSIGN_VENUE"
        and a["facility"]
        and a["facility"]["venue_key"] == MISSISSIPPI_COLISEUM["venue_key"]
    )

    expected_pairs = [
        ("source exception count", source_action_counts["UNRESOLVED_HOME_VENUE"], EXPECTED_SOURCE_EXCEPTIONS),
        ("source Coliseum count", sum(1 for a in assignments if a["action"] == "ASSIGN_VENUE" and a["facility"] and a["facility"]["venue_key"] == MISSISSIPPI_COLISEUM["venue_key"]), EXPECTED_SOURCE_COLISEUM),
        ("source mapped current gaps", len(mapped_current), EXPECTED_SOURCE_MAPPED_CURRENT_GAPS),
        ("current canonical exception count", current_exception_count, EXPECTED_CURRENT_CANONICAL_EXCEPTIONS),
        ("current canonical Coliseum count", current_coliseum_count, EXPECTED_CANONICAL_COLISEUM),
        ("canonical-only count", len(canonical_only_assignments), EXPECTED_CANONICAL_ONLY),
    ]
    for label, actual, expected in expected_pairs:
        if actual != expected:
            errors.append(f"{label} drift: {actual} != {expected}")
    if mapped_outside != {EXPECTED_KENTUCKY_RECONCILIATION}:
        errors.append(f"mapped-outside universe drift: {sorted(mapped_outside)}")
    if set(canonical_only_ids) != {a["canonical_game_id"] for a in canonical_only_assignments}:
        errors.append("canonical-only gap universe is not fully assignable from established chronology")

    existing_disc = [
        r for r in discrepancy_rows
        if r.get("canonical_game_id", "").strip() == EXPECTED_KENTUCKY_RECONCILIATION
        and r.get("field_name", "").strip() == "site_type"
    ]
    if len(existing_disc) > 1:
        errors.append("multiple existing site_type discrepancies for Kentucky reconciliation game")

    payload = {
        "plan_version": PLAN_VERSION,
        "program": PROGRAM,
        "git_head": git_head(repo),
        "source_home_gap_count": len(source_gaps),
        "canonical_home_gap_count": len(canonical_gaps),
        "source_action_counts": dict(sorted(source_action_counts.items())),
        "mapped_current_count": len(mapped_current),
        "mapped_outside_ids": sorted(mapped_outside),
        "current_canonical_exception_count": current_exception_count,
        "current_canonical_coliseum_count": current_coliseum_count,
        "canonical_only_count": len(canonical_only_assignments),
        "assignments": assignments,
        "canonical_only_assignments": canonical_only_assignments,
        "kentucky_reconciliation_id": EXPECTED_KENTUCKY_RECONCILIATION,
        "existing_kentucky_site_discrepancy_count": len(existing_disc),
        "holds": holds,
        "errors": errors,
    }
    return payload


def write_plan(repo: Path, payload: dict[str, Any]) -> tuple[Path, str]:
    out = repo / ".onboarding/mississippi-state-home-remediation"
    out.mkdir(parents=True, exist_ok=True)
    digest = plan_hash(payload)
    path = out / "plan.json"
    path.write_text(
        json.dumps({"sha256": digest, "payload": payload}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path, digest


def next_discrepancy_id(rows: list[dict[str, str]]) -> str:
    maximum = 0
    for row in rows:
        match = re.fullmatch(r"DISC-(\d+)", row.get("discrepancy_id", "").strip())
        if match:
            maximum = max(maximum, int(match.group(1)))
    return f"DISC-{maximum + 1:06d}"


def append_source_notes(path: Path) -> None:
    marker_text = "## Retroactive HOME-site remediation (2026-08-30)"
    text = path.read_text(encoding="utf-8")
    if marker_text in text:
        return
    addition = f"""

{marker_text}

The published-site hardening audit identified 168 Mississippi State canonical HOME games with missing venue and/or location. This remediation applies the owner-approved historical-unrecoverable HOME venue policy rather than inventing unsupported physical venue names.

- 139 Mississippi State source HOME rows are exhaustively researched but retain a blank physical venue under `RESEARCHED_UNRESOLVED_HOME_VENUE`; city/state remain complete. This comprises pre-Tin Starkville HOME games plus pre-1962 Jackson alternate-site HOME games, including the reconciled 1929 Kentucky game.
- 20 Jackson HOME rows beginning 1962-12-15 are assigned **Mississippi Coliseum**, supported by Mississippi State Athletics' official Jackson-game history and Mississippi Fairgrounds' 1962 facility history.
- 10 canonical-only HOME gaps are assigned from the already-established Tin Gym / McCarthy Gymnasium / Humphrey Coliseum chronology.
- `CBBG-0014851` is corrected from Kentucky HOME at Alumni Gym to Mississippi State alternate-site HOME in Jackson. UK Athletics' official all-time results marks both 1928-29 Mississippi A&M games as Kentucky away games, while Mississippi State places the 32-14 game in Jackson. The 1929-02-02 vs. 1929-02-03 source-date disagreement is preserved and not altered by this site-only correction.

Primary supporting sources:

- Mississippi State official historical record book / media guide and facility history.
- Mississippi State Athletics, official Jackson basketball breakdown identifying Mississippi Coliseum games beginning 1962-12-15.
- Mississippi Fairgrounds / Mississippi Department of Agriculture and Commerce history identifying Mississippi Coliseum as a 1962 facility.
- UK Athletics official men's basketball all-time results for 1928-29.

The unresolved HOME venue status is a permanent statement of historical uncertainty, not a placeholder for unfinished research. If stronger game-specific physical-venue evidence is later discovered, it should replace the exception.
"""
    path.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def apply_plan(repo: Path, payload: dict[str, Any]) -> dict[str, int]:
    if payload.get("errors") or payload.get("holds"):
        raise MississippiStateHomeError("refusing apply with plan errors/holds")
    if payload.get("source_home_gap_count") != EXPECTED_SOURCE_HOME_GAPS:
        raise MississippiStateHomeError("refusing apply outside exact source gap universe")
    if payload.get("canonical_home_gap_count") != EXPECTED_CANONICAL_HOME_GAPS:
        raise MississippiStateHomeError("refusing apply outside exact canonical gap universe")

    source_path = repo / "schools/mississippi-state/source-games.csv"
    canonical_path = repo / "data/canonical/games.csv"
    assertions_path = repo / "data/evidence/game-assertions.csv"
    discrepancies_path = repo / "data/reconciliation/discrepancies.csv"
    global_venues_path = repo / "data/reference/venues.csv"
    school_venues_path = repo / "schools/mississippi-state/venues.csv"
    source_notes_path = repo / "schools/mississippi-state/source-notes.md"

    source_fields, source_rows = read_csv(source_path)
    canonical_fields, canonical_rows = read_csv(canonical_path)
    assertion_fields, assertion_rows = read_csv(assertions_path)
    discrepancy_fields, discrepancy_rows = read_csv(discrepancies_path)
    global_venue_fields, global_venues = read_csv(global_venues_path)
    school_venue_fields, school_venues = read_csv(school_venues_path)

    for field in ("site_research_status", "site_research_basis"):
        if field not in source_fields:
            source_fields.append(field)
            for row in source_rows:
                row[field] = ""

    source_by_id = {r.get("source_game_id", "").strip(): r for r in source_rows}
    canonical_by_id = {r.get("canonical_game_id", "").strip(): r for r in canonical_rows}
    assertions_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertion_rows:
        if row.get("source_program_key", "").strip() == PROGRAM:
            assertions_by_source[row.get("source_game_id", "").strip()].append(row)

    source_changed = 0
    canonical_changed = 0
    assertion_changed = 0
    exceptions_applied = 0
    coliseum_applied = 0

    for item in payload["assignments"]:
        sid = item["source_game_id"]
        cid = item["canonical_game_id"]
        source = source_by_id[sid]
        assertions = assertions_by_source.get(sid, [])
        if len(assertions) != 1:
            raise MississippiStateHomeError(f"{sid}: assertion count changed")
        assertion = assertions[0]
        source_before = dict(source)
        assertion_before = dict(assertion)

        if item["action"] == "UNRESOLVED_HOME_VENUE":
            require_blank_or_expected(source, "curated_venue_name", "", sid)
            source["site_research_status"] = EXCEPTION_STATUS
            source["site_research_basis"] = item["research_basis"]
            source["notes"] = append_note(source.get("notes", ""), "[RESEARCHED_UNRESOLVED_HOME_VENUE]")
            exceptions_applied += 1
        elif item["action"] == "ASSIGN_VENUE":
            facility = item["facility"]
            require_blank_or_expected(source, "curated_venue_name", facility["display_name"], sid)
            source["curated_venue_name"] = facility["display_name"]
            source["site_research_status"] = ""
            source["site_research_basis"] = ""
            source["notes"] = append_note(
                source.get("notes", ""),
                f"[HOME_VENUE_REMEDIATION {facility['display_name']}]",
            )
            require_blank_or_expected(assertion, "curated_venue_name", facility["display_name"], sid)
            assertion["curated_venue_name"] = facility["display_name"]
            assertion["notes"] = append_note(
                assertion.get("notes", ""),
                f"[HOME_VENUE_REMEDIATION {facility['display_name']}]",
            )
            if facility["venue_key"] == MISSISSIPPI_COLISEUM["venue_key"]:
                coliseum_applied += 1
        else:
            raise MississippiStateHomeError(f"{sid}: unknown action {item['action']}")

        if source != source_before:
            source_changed += 1
        if assertion != assertion_before:
            assertion_changed += 1

        canonical = canonical_by_id[cid]
        canonical_before = dict(canonical)
        if cid == EXPECTED_KENTUCKY_RECONCILIATION:
            if {canonical.get("team_a_key", "").strip(), canonical.get("team_b_key", "").strip()} != {
                "kentucky", PROGRAM
            }:
                raise MississippiStateHomeError("Kentucky reconciliation participant drift")
            canonical["site_type"] = canonical_home_site_type(canonical)
            if "designated_home_team_key" in canonical:
                canonical["designated_home_team_key"] = PROGRAM
            canonical["venue_key"] = ""
            canonical["venue_id"] = ""
            canonical["site_city"] = "Jackson"
            canonical["site_state"] = "MS"
            canonical["notes"] = append_note(canonical.get("notes", ""), marker(sid))
            canonical["notes"] = append_note(
                canonical.get("notes", ""),
                "[SITE_RECONCILIATION Kentucky-away evidence + owner-approved Jackson convention]",
            )
        elif item["in_current_canonical_gap"]:
            if not canonical_home(canonical):
                raise MississippiStateHomeError(f"{cid}: no longer Mississippi State HOME")
            if item["action"] == "UNRESOLVED_HOME_VENUE":
                require_blank_or_expected(canonical, "venue_key", "", cid)
                require_blank_or_expected(canonical, "venue_id", "", cid)
                canonical["site_city"] = item["city"]
                canonical["site_state"] = item["state"]
                canonical["notes"] = append_note(canonical.get("notes", ""), marker(sid))
            else:
                facility = item["facility"]
                require_blank_or_expected(canonical, "venue_key", facility["venue_key"], cid)
                require_blank_or_expected(canonical, "venue_id", facility["venue_id"], cid)
                canonical["venue_key"] = facility["venue_key"]
                canonical["venue_id"] = facility["venue_id"]
                canonical["site_city"] = facility["city"]
                canonical["site_state"] = facility["state"]
                canonical["notes"] = append_note(
                    canonical.get("notes", ""),
                    f"[HOME_VENUE_REMEDIATION {facility['display_name']}]",
                )
        else:
            raise MississippiStateHomeError(f"{cid}: unexpected non-gap assignment")
        if canonical != canonical_before:
            canonical_changed += 1

    for item in payload["canonical_only_assignments"]:
        cid = item["canonical_game_id"]
        canonical = canonical_by_id[cid]
        if not canonical_home(canonical):
            raise MississippiStateHomeError(f"{cid}: canonical-only row no longer MS HOME")
        facility = item["facility"]
        canonical_before = dict(canonical)
        require_blank_or_expected(canonical, "venue_key", facility["venue_key"], cid)
        require_blank_or_expected(canonical, "venue_id", facility["venue_id"], cid)
        canonical["venue_key"] = facility["venue_key"]
        canonical["venue_id"] = facility["venue_id"]
        canonical["site_city"] = facility["city"]
        canonical["site_state"] = facility["state"]
        canonical["notes"] = append_note(
            canonical.get("notes", ""),
            f"[HOME_VENUE_REMEDIATION {facility['display_name']} canonical-only reciprocal gap]",
        )
        if canonical != canonical_before:
            canonical_changed += 1

    # Global Mississippi Coliseum identity.
    global_by_id = {r.get("venue_id", "").strip(): r for r in global_venues}
    global_by_key = {r.get("venue_key", "").strip(): r for r in global_venues}
    if MISSISSIPPI_COLISEUM["venue_id"] not in global_by_id:
        if MISSISSIPPI_COLISEUM["venue_key"] in global_by_key:
            raise MississippiStateHomeError("Mississippi Coliseum key collision at apply")
        global_venues.append({
            "venue_id": MISSISSIPPI_COLISEUM["venue_id"],
            "venue_key": MISSISSIPPI_COLISEUM["venue_key"],
            "display_name": MISSISSIPPI_COLISEUM["display_name"],
            "city": "Jackson",
            "state": "MS",
            "opened": "1962",
            "closed": "",
            "date_precision": "YEAR",
            "identity_status": "RESEARCHED_OFFICIAL",
            "source_basis": COLISEUM_BASIS,
            "notes": "Mississippi State Jackson basketball relationship is explicitly documented beginning 1962-12-15; do not back-project this venue onto earlier Jackson games without game-specific evidence.",
        })

    # School venue relationship.
    school_by_key = {r.get("venue_key", "").strip(): r for r in school_venues}
    if MISSISSIPPI_COLISEUM["venue_key"] not in school_by_key:
        max_index = max((int(r.get("index", "-1")) for r in school_venues if r.get("index", "").isdigit()), default=-1)
        assigned_dates = sorted(
            r.get("game_date", "").strip()
            for r in source_rows
            if r.get("curated_venue_name", "").strip() == MISSISSIPPI_COLISEUM["display_name"]
            and r.get("game_date", "").strip()
        )
        school_venues.append({
            "index": str(max_index + 1),
            "source_program_key": PROGRAM,
            "venue_key": MISSISSIPPI_COLISEUM["venue_key"],
            "venue_id": MISSISSIPPI_COLISEUM["venue_id"],
            "canonical_name": MISSISSIPPI_COLISEUM["display_name"],
            "aliases": "The Big House",
            "city": "Jackson",
            "state": "MS",
            "venue_type": "arena",
            "known_opened": "1962",
            "known_closed": "",
            "venue_date_precision": "year",
            "games_currently_assigned": str(len(assigned_dates)),
            "first_assigned_game": assigned_dates[0] if assigned_dates else "",
            "last_assigned_game": assigned_dates[-1] if assigned_dates else "",
            "relationship_type": "alternate_home",
            "relationship_start": "1962-12-15",
            "relationship_end": "",
            "relationship_date_precision": "exact",
            "site_rule": "Jackson games must already be independently classified under the owner-approved Jackson convention; venue identity never establishes H/A/N.",
            "source_basis": COLISEUM_BASIS,
            "notes": "Mississippi Coliseum is assigned only where official Mississippi State evidence supports the physical building; pre-1962 Jackson HOME games remain researched-unresolved venue identities.",
        })

    # Permanent resolved discrepancy for the Kentucky site correction.
    matches = [
        r for r in discrepancy_rows
        if r.get("canonical_game_id", "").strip() == EXPECTED_KENTUCKY_RECONCILIATION
        and r.get("field_name", "").strip() == "site_type"
    ]
    canonical = canonical_by_id[EXPECTED_KENTUCKY_RECONCILIATION]
    canonical_value = f"{canonical['site_type']} / Mississippi State HOME / Jackson, MS"
    if not matches:
        discrepancy_rows.append({
            "discrepancy_id": next_discrepancy_id(discrepancy_rows),
            "canonical_game_id": EXPECTED_KENTUCKY_RECONCILIATION,
            "field_name": "site_type",
            "source_a_program_key": PROGRAM,
            "source_a_value": "Mississippi State official ledger: Jackson, MS; curated SOURCE_PROGRAM_HOME under owner Jackson convention",
            "source_b_program_key": "kentucky",
            "source_b_value": "UK Athletics official all-time results: both 1928-29 Mississippi A&M games are Kentucky away games",
            "canonical_value": canonical_value,
            "status": "RESOLVED",
            "resolution_basis": KENTUCKY_RECONCILIATION_BASIS,
            "notes": "Site-only correction. Canonical game date remains unchanged; Mississippi State source preserves its conflicting printed date in raw_text.",
        })
    else:
        row = matches[0]
        row["canonical_value"] = canonical_value
        row["status"] = "RESOLVED"
        row["resolution_basis"] = KENTUCKY_RECONCILIATION_BASIS
        row["notes"] = append_note(
            row.get("notes", ""),
            "Site-only correction; date disagreement preserved.",
        )

    append_source_notes(source_notes_path)

    write_csv_preserving(source_path, source_fields, source_rows)
    write_csv_preserving(canonical_path, canonical_fields, canonical_rows)
    write_csv_preserving(assertions_path, assertion_fields, assertion_rows)
    write_csv_preserving(discrepancies_path, discrepancy_fields, discrepancy_rows)
    write_csv_preserving(global_venues_path, global_venue_fields, global_venues)
    write_csv_preserving(school_venues_path, school_venue_fields, school_venues)

    return {
        "source_changed": source_changed,
        "canonical_changed": canonical_changed,
        "assertion_changed": assertion_changed,
        "exceptions_applied": exceptions_applied,
        "coliseum_applied": coliseum_applied,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mississippi State HOME-site remediation")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-plan-sha256", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    try:
        payload = build_plan(repo)
        plan_path, digest = write_plan(repo, payload)
        print("College Basketball History — Mississippi State HOME remediation plan")
        print(f"Git HEAD:                    {payload['git_head']}")
        print(f"Source HOME gaps:            {payload['source_home_gap_count']}")
        print(f"Canonical HOME gaps:         {payload['canonical_home_gap_count']}")
        print("Source action counts:        " + json.dumps(payload["source_action_counts"], sort_keys=True))
        print(f"Mapped current gaps:         {payload['mapped_current_count']}")
        print(f"Mapped outside gap IDs:      {payload['mapped_outside_ids']}")
        print(f"Current exceptions:          {payload['current_canonical_exception_count']}")
        print(f"Current Mississippi Coliseum:{payload['current_canonical_coliseum_count']}")
        print(f"Canonical-only assignments:  {payload['canonical_only_count']}")
        print(f"Holds:                       {len(payload['holds'])}")
        print(f"Errors:                      {len(payload['errors'])}")
        print(f"Plan SHA-256:                {digest}")
        print(f"Plan artifact:               {plan_path}")
        if payload["holds"]:
            print("HOLDS:")
            for item in payload["holds"]:
                print("  " + json.dumps(item, sort_keys=True))
        if payload["errors"]:
            print("ERRORS:")
            for item in payload["errors"]:
                print("  - " + item)
        if payload["holds"] or payload["errors"]:
            print("FAIL: remediation plan is not zero-hold/exact.")
            return 1
        if not args.apply:
            print("PASS: exact zero-hold read-only plan; no tracked basketball data changed.")
            return 0
        if not args.expected_plan_sha256:
            raise MississippiStateHomeError("--apply requires --expected-plan-sha256")
        if args.expected_plan_sha256 != digest:
            raise MississippiStateHomeError(
                f"plan SHA mismatch: expected {args.expected_plan_sha256}, current {digest}"
            )
        result = apply_plan(repo, payload)
        print("APPLIED: " + json.dumps(result, sort_keys=True))
        print("PASS: Mississippi State HOME remediation applied from exact sealed plan.")
        return 0
    except (FileNotFoundError, KeyError, ValueError, MississippiStateHomeError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
