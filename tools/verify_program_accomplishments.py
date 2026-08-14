#!/usr/bin/env python3
"""Read-only canonical cross-check for one program's accomplishment reference."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from program_history import (
    BEST_FINISH_LABELS,
    derive_ncaa_accomplishments,
    history_scope_errors,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def compare_program(
    program: dict[str, str],
    reference: dict[str, str],
    canonical_games: list[dict[str, str]],
) -> bool:
    program_key = program["program_key"]
    cutoff = program.get("history_start_season", "").strip()
    scope_problems = history_scope_errors(program, required=True)
    if scope_problems:
        print(f"{program_key}: INCOMPLETE — {'; '.join(scope_problems)}")
        return False

    derived = derive_ncaa_accomplishments(canonical_games, program_key, cutoff)
    comparisons = {
        "ncaa_tournament_appearances": derived["ncaa_tournament_appearances"],
        "final_four_appearances": derived["final_four_appearances"],
        "national_championships": derived["national_championships"],
        "best_finish_key": derived["best_finish_key"] or "",
        "best_finish_year": (
            str(derived["best_finish_year"])
            if derived["best_finish_year"] is not None
            else ""
        ),
    }
    conflicts = [
        f"{field}: reference={reference.get(field, '')!r}, canonical={value!r}"
        for field, value in comparisons.items()
        if str(reference.get(field, "")).strip() != str(value)
    ]
    if derived["incomplete_reasons"]:
        result = "INCOMPLETE"
    elif conflicts:
        result = "CONFLICT"
    else:
        result = "MATCH"

    finish_label = BEST_FINISH_LABELS.get(
        derived["best_finish_key"], "—"
    )
    print(
        f"{program_key}: {result} | since {cutoff} | "
        f"NCAA {derived['ncaa_tournament_appearances']} | "
        f"Final Fours {derived['final_four_appearances']} | "
        f"titles {derived['national_championships']} | "
        f"best {finish_label} "
        f"{derived['best_finish_year'] if derived['best_finish_year'] is not None else '—'}"
    )
    print(
        "  Conference regular-season championships: NOT_DERIVABLE; "
        "authoritative source verification required."
    )
    print(
        "  Conference tournament titles from tagged on-court finals: "
        f"{derived['conference_tournament_championships_supporting']} "
        "(supporting cross-check only)."
    )
    print(
        "  Reference status: "
        f"{reference.get('verification_status', '')}; stored canonical cross-check: "
        f"{reference.get('canonical_crosscheck_status', '')}."
    )
    for conflict in conflicts:
        print(f"  - {conflict}")
    for reason in derived["incomplete_reasons"]:
        print(f"  - {reason}")
    return result == "MATCH"


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("program_key", nargs="?")
    group.add_argument("--all-public", action="store_true")
    parser.add_argument("--repo", type=Path, default=None)
    args = parser.parse_args()

    repo_root = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    programs = read_csv(repo_root / "data/reference/programs.csv")
    accomplishments = read_csv(
        repo_root / "data/reference/program-accomplishments.csv"
    )
    canonical_games = read_csv(repo_root / "data/canonical/games.csv")
    programs_by_key = {row["program_key"]: row for row in programs}
    accomplishments_by_key = {
        row["program_key"]: row for row in accomplishments
    }

    if args.all_public:
        keys = sorted(
            row["program_key"]
            for row in programs
            if row.get("public_page_enabled") == "Yes"
        )
    else:
        keys = [args.program_key]

    failures = 0
    for key in keys:
        if key not in programs_by_key or key not in accomplishments_by_key:
            print(f"{key}: INCOMPLETE — missing reference row")
            failures += 1
            continue
        if not compare_program(
            programs_by_key[key], accomplishments_by_key[key], canonical_games
        ):
            failures += 1

    print()
    if failures:
        print(f"FAIL: {failures} program cross-check(s) need review.")
        return 1
    print(f"PASS: {len(keys)} program accomplishment cross-check(s) match.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
