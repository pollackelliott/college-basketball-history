#!/usr/bin/env python3
"""Plan Michigan State early HOME venue/location remediation.

Michigan State institutional history identifies five principal basketball homes:
Armory; the gym now in IM Circle; Demonstration Hall; Jenison Fieldhouse; and
Breslin Center.  The currently published HOME gap universe is confined to
1898-99 through 1928-29.  MSU records date the replacement Gymnasium Building
(now IM Circle) to spring 1918, after the 1917-18 basketball season, and the
portable basketball floor in Demonstration Hall to December 1929.  Therefore
this planner assigns only already-established Michigan State HOME rows as:

- Armory: 1898-99 through 1917-18
- IM Circle Gymnasium: 1918-19 through 1928-29

It never infers H/A/N from venue chronology.  Default mode is read-only except
for an ignored JSON plan under .onboarding/.  Apply support will be added only
after the exact corpus plan is reviewed and zero-hold.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROGRAM = "michigan-state"
EXPECTED_SOURCE_HOME_GAPS = 253
EXPECTED_CANONICAL_HOME_GAPS = 253
PLAN_VERSION = 1
EAST_LANSING = ("East Lansing", "MI")
FACILITIES = {
    "michigan-state-armory": {
        "venue_key": "michigan-state-armory",
        "venue_id": "VEN-000292",
        "display_name": "Armory",
        "city": "East Lansing",
        "state": "MI",
    },
    "michigan-state-im-circle-gymnasium": {
        "venue_key": "michigan-state-im-circle-gymnasium",
        "venue_id": "VEN-000293",
        "display_name": "IM Circle Gymnasium",
        "city": "East Lansing",
        "state": "MI",
    },
}
SOURCE_BASIS = (
    "Michigan State University institutional basketball/facility history: the program's "
    "five principal homes were the Armory, the gym in today's IM Circle complex, "
    "Demonstration Hall, Jenison Fieldhouse, and Breslin Center. MSU Kinesiology "
    "documents the Gymnasium Building as completed in spring 1918; MSU's 1929-30 "
    "facility description documents a portable basketball floor in Demonstration Hall "
    "in December 1929. Venue chronology is applied only after independent HOME classification."
)


class MichiganStateHomeError(RuntimeError):
    pass


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def plan_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def git_head(repo: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()


def is_gap(row: dict[str, str], *, source: bool) -> bool:
    venue_field = "curated_venue_name" if source else "venue_id"
    return not row.get(venue_field, "").strip() or not row.get("city" if source else "site_city", "").strip() or not row.get("state" if source else "site_state", "").strip()


def michigan_state_home(row: dict[str, str]) -> bool:
    site = row.get("site_type", "").strip()
    return (
        site == "TEAM_A_HOME" and row.get("team_a_key", "").strip() == PROGRAM
    ) or (
        site == "TEAM_B_HOME" and row.get("team_b_key", "").strip() == PROGRAM
    )


def facility_for_season(season: str) -> tuple[str | None, str | None]:
    if len(season) != 9 or season[4] != "-":
        return None, "invalid_season"
    try:
        start = int(season[:4])
        end = int(season[5:])
    except ValueError:
        return None, "invalid_season"
    if end != start + 1:
        return None, "invalid_season"
    if 1898 <= start <= 1917:
        return "michigan-state-armory", None
    if 1918 <= start <= 1928:
        return "michigan-state-im-circle-gymnasium", None
    return None, "outside_verified_early_chronology"


def build_plan(repo: Path) -> dict[str, Any]:
    _, source_rows = read_csv(repo / "schools/michigan-state/source-games.csv")
    _, canonical_rows = read_csv(repo / "data/canonical/games.csv")
    _, assertion_rows = read_csv(repo / "data/evidence/game-assertions.csv")
    _, school_venue_rows = read_csv(repo / "schools/michigan-state/venues.csv")

    source_gaps = [
        row for row in source_rows
        if row.get("curated_site_type", "").strip() == "SOURCE_PROGRAM_HOME" and is_gap(row, source=True)
    ]
    canonical_gaps = [
        row for row in canonical_rows
        if michigan_state_home(row) and is_gap(row, source=False)
    ]

    assertion_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertion_rows:
        if row.get("source_program_key", "").strip() == PROGRAM:
            assertion_by_source[row.get("source_game_id", "").strip()].append(row)

    canonical_by_id = {row.get("canonical_game_id", "").strip(): row for row in canonical_rows}
    school_venues = {row.get("venue_key", "").strip(): row for row in school_venue_rows}

    errors: list[str] = []
    if len(source_gaps) != EXPECTED_SOURCE_HOME_GAPS:
        errors.append(f"source HOME gap count drift: {len(source_gaps)} != {EXPECTED_SOURCE_HOME_GAPS}")
    if len(canonical_gaps) != EXPECTED_CANONICAL_HOME_GAPS:
        errors.append(f"canonical HOME gap count drift: {len(canonical_gaps)} != {EXPECTED_CANONICAL_HOME_GAPS}")

    for key, spec in FACILITIES.items():
        row = school_venues.get(key)
        if row is None:
            errors.append(f"missing school venue identity: {key}")
            continue
        for field in ("venue_id", "city", "state"):
            if row.get(field, "").strip() != spec[field]:
                errors.append(
                    f"school venue identity drift for {key} {field}: {row.get(field, '').strip()!r} != {spec[field]!r}"
                )

    assignments: list[dict[str, Any]] = []
    holds: list[dict[str, str]] = []
    seen_canonical: set[str] = set()

    for source in sorted(source_gaps, key=lambda r: (r.get("season_label", ""), r.get("game_date", ""), r.get("source_game_id", ""))):
        source_id = source.get("source_game_id", "").strip()
        facility_key, reason = facility_for_season(source.get("season_label", "").strip())
        if reason:
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "reason": reason})
            continue

        assertions = assertion_by_source.get(source_id, [])
        canonical_ids = sorted({r.get("canonical_game_id", "").strip() for r in assertions if r.get("canonical_game_id", "").strip()})
        if len(canonical_ids) != 1:
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "reason": f"canonical_mapping_count:{len(canonical_ids)}"})
            continue
        canonical_id = canonical_ids[0]
        canonical = canonical_by_id.get(canonical_id)
        if canonical is None:
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "reason": "canonical_missing"})
            continue
        if not michigan_state_home(canonical):
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "reason": f"canonical_not_michigan_state_home:{canonical.get('site_type', '')}"})
            continue
        if canonical_id in seen_canonical:
            holds.append({"source_game_id": source_id, "season_label": source.get("season_label", ""), "reason": f"duplicate_canonical_mapping:{canonical_id}"})
            continue
        seen_canonical.add(canonical_id)
        facility = FACILITIES[facility_key]
        assignments.append({
            "source_game_id": source_id,
            "canonical_game_id": canonical_id,
            "season_label": source.get("season_label", ""),
            "game_date": source.get("game_date", ""),
            "opponent_key": source.get("normalized_opponent_key", ""),
            "facility_key": facility_key,
            "venue_id": facility["venue_id"],
            "venue_name": facility["display_name"],
            "city": facility["city"],
            "state": facility["state"],
        })

    canonical_gap_ids = {row.get("canonical_game_id", "").strip() for row in canonical_gaps}
    assigned_ids = {row["canonical_game_id"] for row in assignments}
    unassigned_canonical = sorted(canonical_gap_ids - assigned_ids)
    unexpected_assigned = sorted(assigned_ids - canonical_gap_ids)
    if unassigned_canonical:
        errors.append(f"canonical HOME gaps not covered by source assignments: {len(unassigned_canonical)}")
    if unexpected_assigned:
        errors.append(f"assignments outside canonical HOME gap universe: {len(unexpected_assigned)}")

    facility_counts = dict(sorted(Counter(row["facility_key"] for row in assignments).items()))
    payload = {
        "plan_version": PLAN_VERSION,
        "program": PROGRAM,
        "git_head": git_head(repo),
        "source_basis": SOURCE_BASIS,
        "source_home_gap_count": len(source_gaps),
        "canonical_home_gap_count": len(canonical_gaps),
        "assignment_count": len(assignments),
        "hold_count": len(holds),
        "facility_counts": facility_counts,
        "assignments": assignments,
        "holds": holds,
        "unassigned_canonical_game_ids": unassigned_canonical,
        "unexpected_assigned_game_ids": unexpected_assigned,
        "errors": errors,
    }
    return payload


def write_plan(repo: Path, payload: dict[str, Any]) -> tuple[Path, str]:
    out = repo / ".onboarding/michigan-state-home-remediation"
    out.mkdir(parents=True, exist_ok=True)
    digest = plan_hash(payload)
    wrapped = {"sha256": digest, "payload": payload}
    path = out / "plan.json"
    path.write_text(json.dumps(wrapped, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path, digest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    payload = build_plan(repo)
    path, digest = write_plan(repo, payload)

    print("College Basketball History — Michigan State early HOME chronology plan")
    print(f"Git HEAD:             {payload['git_head']}")
    print(f"Source HOME gaps:     {payload['source_home_gap_count']}")
    print(f"Canonical HOME gaps:  {payload['canonical_home_gap_count']}")
    print(f"Assignments:          {payload['assignment_count']}")
    print(f"Holds:                {payload['hold_count']}")
    print(f"Facility counts:      {json.dumps(payload['facility_counts'], sort_keys=True)}")
    print(f"Plan SHA-256:         {digest}")
    if payload["holds"]:
        print("HELD ROWS:")
        for row in payload["holds"]:
            print("  " + json.dumps(row, sort_keys=True))
    if payload["errors"]:
        print("ERRORS:")
        for error in payload["errors"]:
            print("  - " + error)
    print(f"Plan artifact:        {path}")
    if payload["errors"] or payload["holds"]:
        print("STOP: resolve every hold/error before adding apply support.")
        return 1
    print("PASS: exact zero-hold read-only chronology plan; no tracked basketball data changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
