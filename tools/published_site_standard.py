#!/usr/bin/env python3
"""Audit canonical games against the owner published-site completeness standard.

This is a read-only global scorecard. It distinguishes:

- hard debt: a published program is the home team but venue/location is blank;
- expected reciprocal debt: a published program is away at an unpublished home team;
- neutral-site research debt, with heightened published-vs-published visibility;
- UNKNOWN H/A/N involving published programs, again highlighting cases where both
  participant source packages should already be available.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _complete_location(row: dict[str, str]) -> bool:
    return bool(row.get("site_city", "").strip() and row.get("site_state", "").strip())


def _venue_known(row: dict[str, str]) -> bool:
    return bool(row.get("venue_key", "").strip() or row.get("venue_id", "").strip())


def _home_team(row: dict[str, str]) -> str:
    site = row.get("site_type", "").strip()
    if site == "TEAM_A_HOME":
        return row.get("team_a_key", "").strip()
    if site == "TEAM_B_HOME":
        return row.get("team_b_key", "").strip()
    return ""


def published_site_standard_report(
    repo: Path,
    *,
    example_limit: int = 12,
) -> dict[str, Any]:
    _, programs = read_csv(repo / "data/reference/programs.csv")
    _, games = read_csv(repo / "data/canonical/games.csv")

    published = {
        row.get("program_key", "").strip()
        for row in programs
        if row.get("public_page_enabled", "").strip().lower() == "yes"
        and row.get("program_key", "").strip()
    }

    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    hard_home_ids: set[str] = set()
    expected_away_ids: set[str] = set()
    heightened_neutral_ids: set[str] = set()
    heightened_unknown_ids: set[str] = set()

    def record(category: str, game_id: str) -> None:
        counts[category] += 1
        if len(examples[category]) < example_limit:
            examples[category].append(game_id)

    for row in games:
        game_id = row.get("canonical_game_id", "").strip()
        team_a = row.get("team_a_key", "").strip()
        team_b = row.get("team_b_key", "").strip()
        participants = {team_a, team_b} - {""}
        published_participants = participants & published
        if not published_participants:
            continue

        both_published = len(participants) == 2 and participants <= published
        site = row.get("site_type", "").strip()
        home_team = _home_team(row)
        venue_missing = not _venue_known(row)
        location_missing = not _complete_location(row)

        if home_team in published:
            if venue_missing:
                record("published_home_missing_venue", game_id)
                hard_home_ids.add(game_id)
            if location_missing:
                record("published_home_missing_location", game_id)
                hard_home_ids.add(game_id)
            if venue_missing and location_missing:
                record("published_home_missing_both", game_id)
        elif home_team and home_team not in published:
            # One or more published participants are away at an unpublished home team.
            # Missing building/geography is expected reciprocal debt until that home
            # program is researched and published.
            if venue_missing:
                record("published_away_at_unpublished_missing_venue", game_id)
                expected_away_ids.add(game_id)
            if location_missing:
                record("published_away_at_unpublished_missing_location", game_id)
                expected_away_ids.add(game_id)

        if site in {"", "UNKNOWN"}:
            record("published_unknown_site_type", game_id)
            if both_published:
                record("published_vs_published_unknown_site_type", game_id)
                heightened_unknown_ids.add(game_id)

        if site == "NEUTRAL":
            if venue_missing:
                record("published_neutral_missing_venue", game_id)
                if both_published:
                    record("published_vs_published_neutral_missing_venue", game_id)
            if location_missing:
                record("published_neutral_missing_location", game_id)
                if both_published:
                    record("published_vs_published_neutral_missing_location", game_id)
                    heightened_neutral_ids.add(game_id)

    return {
        "status": "PASS" if not hard_home_ids else "FAIL",
        "published_programs": len(published),
        "counts": {
            **dict(sorted(counts.items())),
            "hard_published_home_blocker_games": len(hard_home_ids),
            "expected_away_at_unpublished_debt_games": len(expected_away_ids),
            "heightened_published_vs_published_neutral_games": len(heightened_neutral_ids),
            "heightened_published_vs_published_unknown_site_games": len(heightened_unknown_ids),
        },
        "examples": {key: value for key, value in sorted(examples.items())},
    }


def print_report(report: dict[str, Any]) -> None:
    print("College Basketball History — published site standard")
    print(f"Status:             {report['status']}")
    print(f"Published programs: {report['published_programs']:,}")
    print("Counts:             " + json.dumps(report["counts"], sort_keys=True))
    if report["examples"]:
        print("Examples:           " + json.dumps(report["examples"], sort_keys=True))
    if report["status"] == "PASS":
        print("PASS: no published-program home game is missing venue or location.")
    else:
        print(
            "FAIL: published-program home venue/location debt remains. "
            "Away-at-unpublished debt is reported separately and is not a hard blocker."
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit the owner published-site standard.")
    parser.add_argument("--repo", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    try:
        report = published_site_standard_report(repo)
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print_report(report)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
