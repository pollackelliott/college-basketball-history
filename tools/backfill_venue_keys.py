#!/usr/bin/env python3
"""
Backfill blank canonical venue_key values from already-ingested source assertions
and each school's curated venues.csv registry.

Default is DRY RUN:
    python tools/backfill_venue_keys.py

Apply:
    python tools/backfill_venue_keys.py --apply

This only fills BLANK canonical venue_key fields when all usable source assertions
for that canonical game agree on one venue key. It never overwrites an existing
canonical venue key and never guesses across conflicting assertions.

The dry run also prints all conflicts/unmapped venue names so they can be reviewed
before applying.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "date_precision",
    "team_a_key",
    "team_b_key",
    "team_a_score",
    "team_b_score",
    "overtime_periods",
    "site_type",
    "designated_home_team_key",
    "venue_key",
    "site_city",
    "site_state",
    "game_type",
    "postseason_round",
    "administrative_status",
    "administrative_note",
    "canonical_status",
    "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CANONICAL_FIELDS)
        w.writeheader()
        for row in rows:
            w.writerow({field: row.get(field, "") for field in CANONICAL_FIELDS})
    tmp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--repo", type=Path, default=None)
    args = parser.parse_args()

    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    canonical_path = repo / "data" / "canonical" / "games.csv"
    assertions_path = repo / "data" / "evidence" / "game-assertions.csv"
    schools_root = repo / "schools"

    try:
        canonical = read_csv(canonical_path)
        assertions = read_csv(assertions_path)
    except FileNotFoundError as exc:
        print(f"FAIL: required file not found: {exc}")
        return 1

    canonical_by_id = {r.get("canonical_game_id", ""): r for r in canonical}

    venue_maps: dict[str, dict[str, str]] = {}
    if schools_root.exists():
        for school_dir in schools_root.iterdir():
            if not school_dir.is_dir():
                continue
            venue_path = school_dir / "venues.csv"
            if not venue_path.exists():
                continue
            mapping = {}
            for row in read_csv(venue_path):
                name = row.get("canonical_name", "").strip()
                key = row.get("venue_key", "").strip()
                if name and key:
                    mapping[name.casefold()] = key
            venue_maps[school_dir.name] = mapping

    candidates: dict[str, set[str]] = defaultdict(set)
    candidate_details: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    unresolved_details: list[tuple[str, str, str, str]] = []

    for assertion in assertions:
        game_id = assertion.get("canonical_game_id", "").strip()
        program = assertion.get("source_program_key", "").strip()
        venue_name = assertion.get("curated_venue_name", "").strip()
        if not game_id or not program or not venue_name:
            continue

        key = venue_maps.get(program, {}).get(venue_name.casefold(), "")
        if key:
            candidates[game_id].add(key)
            candidate_details[game_id].append((program, venue_name, key))
        else:
            unresolved_details.append(
                (game_id, program, venue_name, assertion.get("source_game_id", ""))
            )

    filled = 0
    conflicting_assertions = []
    existing_conflicts = []
    samples = []

    for row in canonical:
        game_id = row.get("canonical_game_id", "")
        keys = candidates.get(game_id, set())
        existing = row.get("venue_key", "").strip()

        if len(keys) > 1:
            conflicting_assertions.append((game_id, sorted(keys)))
            continue

        if len(keys) == 1:
            candidate = next(iter(keys))
            if existing:
                if existing != candidate:
                    existing_conflicts.append((game_id, existing, candidate))
                continue

            row["venue_key"] = candidate
            filled += 1
            if len(samples) < 12:
                samples.append(
                    (
                        game_id,
                        row.get("season_label", ""),
                        row.get("team_a_key", ""),
                        row.get("team_b_key", ""),
                        candidate,
                    )
                )

    print("College Basketball History — canonical venue-key backfill")
    print(f"Repository: {repo}")
    print(f"Mode:       {'APPLY' if args.apply else 'DRY RUN'}")
    print()
    print(f"Canonical games:                     {len(canonical):,}")
    print(f"Blank venue keys safely fillable:    {filled:,}")
    print(f"Games with conflicting venue claims: {len(conflicting_assertions):,}")
    print(f"Existing canonical/key conflicts:    {len(existing_conflicts):,}")
    print(f"Assertion venue names not in registry:{len(unresolved_details):>8,}")
    print()

    if samples:
        print("SAMPLE FILLS:")
        for game_id, season, a, b, key in samples:
            print(f"  - {game_id} | {season} | {a} vs {b} | {key}")
        print()

    if conflicting_assertions:
        print("CONFLICTING ASSERTION VENUE CLAIMS:")
        for game_id, keys in conflicting_assertions:
            c = canonical_by_id.get(game_id, {})
            print(
                f"  - {game_id} | {c.get('season_label','')} | "
                f"{c.get('team_a_key','')} vs {c.get('team_b_key','')} | "
                f"candidate keys: {', '.join(keys)}"
            )
            for program, venue_name, key in candidate_details.get(game_id, []):
                print(f"      {program}: {venue_name} -> {key}")
        print()

    if existing_conflicts:
        print("EXISTING CANONICAL VENUE-KEY CONFLICTS:")
        for game_id, existing, candidate in existing_conflicts:
            c = canonical_by_id.get(game_id, {})
            print(
                f"  - {game_id} | {c.get('season_label','')} | "
                f"{c.get('team_a_key','')} vs {c.get('team_b_key','')} | "
                f"canonical={existing} | assertion-derived={candidate}"
            )
            for program, venue_name, key in candidate_details.get(game_id, []):
                print(f"      {program}: {venue_name} -> {key}")
        print()

    if unresolved_details:
        print("ASSERTION VENUE NAMES NOT FOUND IN SCHOOL REGISTRY:")
        for game_id, program, venue_name, source_game_id in unresolved_details:
            c = canonical_by_id.get(game_id, {})
            print(
                f"  - {game_id} | {c.get('season_label','')} | "
                f"{program} | {venue_name!r} | source={source_game_id}"
            )
        print()

    if not args.apply:
        print("DRY RUN COMPLETE: no files changed.")
        return 0

    if conflicting_assertions or existing_conflicts:
        print("FAIL SAFE: refusing --apply while venue conflicts remain.")
        print("Resolve or explicitly exempt those cases, then rerun the dry run.")
        return 2

    write_csv(canonical_path, canonical)
    print(f"Applied {filled:,} canonical venue-key fills.")

    validator = repo / "tools" / "validate_data.py"
    if validator.exists():
        result = subprocess.run([sys.executable, str(validator), str(repo)])
        if result.returncode != 0:
            print("FAIL: backfill applied, but validator failed.")
            return result.returncode
        print()
        print("PASS: venue backfill applied and post-write validation succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
