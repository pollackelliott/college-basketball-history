#!/usr/bin/env python3
"""Backfill blank canonical venue identity from curated source assertions."""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from location_safety import (
    append_note,
    registry_fallback_marker,
    source_site_agrees_with_canonical,
)
from venue_reference import load_global_venue_reference

CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "date_precision",
    "team_a_key",
    "team_b_key",
    "team_a_score",
    "team_b_score",
    "result_winner_team_key",
    "overtime_periods",
    "site_type",
    "designated_home_team_key",
    "venue_key",
    "venue_id",
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
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=CANONICAL_FIELDS,
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in CANONICAL_FIELDS})
    temp.replace(path)


def resolve_candidate_identity(
    pairs: set[tuple[str, str]],
    venues_by_id: dict[str, dict[str, str]],
) -> tuple[str, str] | None:
    """Resolve claims by permanent physical venue_id."""
    venue_ids = {venue_id for _, venue_id in pairs if venue_id}
    if len(venue_ids) != 1:
        return None

    venue_id = next(iter(venue_ids))
    global_row = venues_by_id.get(venue_id)
    if global_row is None:
        raise ValueError(f"unknown global venue_id {venue_id!r}")

    venue_key = global_row.get("venue_key", "").strip()
    if not venue_key:
        raise ValueError(f"{venue_id}: global venue_key is required")

    return venue_key, venue_id


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--repo", type=Path, default=None)
    args = parser.parse_args()

    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    canonical_path = repo / "data/canonical/games.csv"
    assertions_path = repo / "data/evidence/game-assertions.csv"
    schools_root = repo / "schools"

    try:
        canonical = read_csv(canonical_path)
        assertions = read_csv(assertions_path)
        global_venues_by_id, _, _ = load_global_venue_reference(repo)
    except (FileNotFoundError, ValueError) as exc:
        print(f"FAIL: required venue input is invalid: {exc}")
        return 1

    canonical_by_id = {
        row.get("canonical_game_id", ""): row
        for row in canonical
    }

    venue_maps: dict[str, dict[str, tuple[str, str]]] = {}
    if schools_root.exists():
        for school_dir in schools_root.iterdir():
            if not school_dir.is_dir():
                continue
            venue_path = school_dir / "venues.csv"
            if not venue_path.exists():
                continue

            mapping: dict[str, tuple[str, str]] = {}
            for row in read_csv(venue_path):
                name = row.get("canonical_name", "").strip()
                key = row.get("venue_key", "").strip()
                venue_id = row.get("venue_id", "").strip()
                if not key or not venue_id:
                    continue
                pair = (key, venue_id)
                if name:
                    mapping[name.casefold()] = pair
                for alias in row.get("aliases", "").split(";"):
                    alias = alias.strip()
                    if alias:
                        mapping[alias.casefold()] = pair

            venue_maps[school_dir.name] = mapping

    candidates: dict[str, set[tuple[str, str]]] = defaultdict(set)
    details: dict[
        str,
        list[tuple[str, str, str, str, str]],
    ] = defaultdict(list)
    unresolved: list[tuple[str, str, str, str]] = []

    for assertion in assertions:
        game_id = assertion.get("canonical_game_id", "").strip()
        program = assertion.get("source_program_key", "").strip()
        venue_name = assertion.get("curated_venue_name", "").strip()

        if not game_id or not program or not venue_name:
            continue

        canonical_row = canonical_by_id.get(game_id)
        if not canonical_row or not source_site_agrees_with_canonical(
            assertion, canonical_row
        ):
            continue

        pair = venue_maps.get(program, {}).get(venue_name.casefold())
        if pair:
            candidates[game_id].add(pair)
            details[game_id].append(
                (
                    program,
                    assertion.get("source_game_id", ""),
                    venue_name,
                    pair[0],
                    pair[1],
                )
            )
        else:
            unresolved.append(
                (
                    game_id,
                    program,
                    venue_name,
                    assertion.get("source_game_id", ""),
                )
            )

    filled = 0
    conflicts = []
    existing_conflicts = []
    samples = []

    for row in canonical:
        game_id = row.get("canonical_game_id", "")
        pairs = candidates.get(game_id, set())
        existing_key = row.get("venue_key", "").strip()
        existing_id = row.get("venue_id", "").strip()

        physical_ids = {venue_id for _, venue_id in pairs if venue_id}
        if len(physical_ids) > 1:
            conflicts.append((game_id, sorted(pairs)))
            continue

        resolved = resolve_candidate_identity(pairs, global_venues_by_id)
        if resolved is not None:
            candidate_key, candidate_id = resolved

            if existing_key or existing_id:
                # venue_id is authoritative physical identity. Different legacy
                # venue_key values may legitimately refer to the same building.
                conflict = (
                    existing_id != candidate_id
                    if existing_id
                    else existing_key != candidate_key
                )
                if conflict:
                    existing_conflicts.append(
                        (
                            game_id,
                            existing_key,
                            existing_id,
                            candidate_key,
                            candidate_id,
                        )
                    )
                continue

            row["venue_key"] = candidate_key
            row["venue_id"] = candidate_id

            program, source_game_id, _, _, _ = sorted(details[game_id])[0]
            marker = registry_fallback_marker(
                program,
                source_game_id,
                candidate_key,
                row.get("site_type", ""),
                ["venue_key", "venue_id"],
            )
            row["notes"] = append_note(row.get("notes", ""), marker)
            filled += 1

            if len(samples) < 12:
                samples.append(
                    (
                        game_id,
                        row.get("season_label", ""),
                        row.get("team_a_key", ""),
                        row.get("team_b_key", ""),
                        candidate_key,
                        candidate_id,
                    )
                )

    print("College Basketball History — canonical venue identity backfill")
    print(f"Repository: {repo}")
    print(f"Mode:       {'APPLY' if args.apply else 'DRY RUN'}")
    print()
    print(f"Canonical games:                      {len(canonical):,}")
    print(f"Blank venue identities safely fillable:{filled:>8,}")
    print(f"Games with conflicting physical venues:{len(conflicts):>8,}")
    print(f"Existing canonical/venue conflicts:   {len(existing_conflicts):,}")
    print(f"Assertion venue names not in registry:{len(unresolved):>8,}")
    print()

    if samples:
        print("SAMPLE FILLS:")
        for game_id, season, a, b, key, venue_id in samples:
            print(
                f"  - {game_id} | {season} | {a} vs {b} | "
                f"{key} | {venue_id}"
            )
        print()

    if existing_conflicts:
        print("EXISTING CANONICAL VENUE CONFLICTS:")
        for game_id, old_key, old_id, new_key, new_id in existing_conflicts:
            print(
                f"  - {game_id} | canonical={old_key}/{old_id} | "
                f"assertion-derived={new_key}/{new_id}"
            )
        print()

    if not args.apply:
        print("DRY RUN COMPLETE: no files changed.")
        return 0

    if existing_conflicts:
        print("FAIL SAFE: refusing --apply while existing conflicts remain.")
        return 2

    write_csv(canonical_path, canonical)
    print(f"Applied {filled:,} canonical venue identity fills.")

    validator = repo / "tools/validate_data.py"
    if validator.exists():
        result = subprocess.run([sys.executable, str(validator), str(repo)])
        if result.returncode != 0:
            print("FAIL: backfill applied, but validator failed.")
            return result.returncode
        print()
        print("PASS: venue identity backfill applied and validated.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
