#!/usr/bin/env python3
"""
Build deterministic public website JSON from the repository's curated data.

Default mode is DRY RUN. Use --apply to write site/data/.

Usage:
    python tools/build_site_data.py
    python tools/build_site_data.py --apply
    python tools/build_site_data.py /path/to/repository
    python tools/build_site_data.py /path/to/repository --apply
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

from location_safety import public_location_pair


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def yes(value: str) -> bool:
    return value.strip().lower() == "yes"


def record_from_games(games: list[dict[str, Any]]) -> dict[str, int]:
    wins = sum(1 for game in games if game["result"] == "W")
    losses = sum(1 for game in games if game["result"] == "L")
    ties = sum(1 for game in games if game["result"] == "T")
    return {
        "games": len(games),
        "wins": wins,
        "losses": losses,
        "ties": ties,
    }


def json_text(payload: Any) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=False,
    ) + "\n"


def perspective_game(
    row: dict[str, str],
    program_key: str,
    opponent_names: dict[str, str],
    venue_names: dict[str, str],
    programs: dict[str, dict[str, str]],
) -> dict[str, Any]:
    team_a = row["team_a_key"]
    team_b = row["team_b_key"]

    score_a = row["team_a_score"].strip()
    score_b = row["team_b_score"].strip()

    if program_key == team_a:
        opponent_key = team_b
        team_score = int(score_a) if score_a else None
        opponent_score = int(score_b) if score_b else None
    elif program_key == team_b:
        opponent_key = team_a
        team_score = int(score_b) if score_b else None
        opponent_score = int(score_a) if score_a else None
    else:
        raise ValueError(
            f'{row["canonical_game_id"]}: {program_key!r} is not a participant.'
        )

    result_winner = row["result_winner_team_key"].strip()
    if result_winner == program_key:
        result = "W"
    elif result_winner == opponent_key:
        result = "L"
    elif team_score is not None and opponent_score is not None and team_score == opponent_score:
        result = "T"
    else:
        result = None

    site_type = row["site_type"]
    designated_home = row["designated_home_team_key"]

    if site_type == "NEUTRAL":
        site = "NEUTRAL"
    elif site_type == "UNKNOWN":
        site = "UNKNOWN"
    elif designated_home == program_key:
        site = "HOME"
    else:
        site = "AWAY"

    opponent_program = programs.get(opponent_key)

    public_city, public_state = public_location_pair(
        row.get("site_city", ""), row.get("site_state", "")
    )

    return {
        "canonical_game_id": row["canonical_game_id"],
        "season_label": row["season_label"],
        "game_date": row["game_date"] or None,
        "date_precision": row["date_precision"],
        "opponent_key": opponent_key,
        "opponent_name": opponent_names[opponent_key],
        "opponent_current_d1": (
            yes(opponent_program["current_d1"]) if opponent_program else False
        ),
        "opponent_public_page_enabled": (
            yes(opponent_program["public_page_enabled"]) if opponent_program else False
        ),
        "team_score": team_score,
        "opponent_score": opponent_score,
        "score_known": team_score is not None and opponent_score is not None,
        "result": result,
        "overtime_periods": int(row["overtime_periods"] or 0),
        "site": site,
        "venue_key": row["venue_key"] or None,
        "venue_name": (
            venue_names.get(row["venue_key"].strip())
            if row["venue_key"].strip()
            else None
        ),
        "site_city": public_city,
        "site_state": public_state,
        "game_type": row["game_type"],
        "postseason_round": row["postseason_round"] or None,
        "administrative_status": row["administrative_status"] or None,
        "administrative_note": row["administrative_note"] or None,
    }


def game_sort_key(game: dict[str, Any]) -> tuple[str, str, str]:
    return (
        game["season_label"],
        game["game_date"] or "9999-99-99",
        game["canonical_game_id"],
    )


def normalized_name_signature(value: str) -> str:
    """
    Compare display-name variants while ignoring harmless punctuation/footnote residue.

    This is intentionally conservative: it only treats names as equivalent when their
    letters and numbers reduce to the same sequence. Truly different names still fail
    the build and require explicit reconciliation.
    """
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def preferred_display_name(names: set[str]) -> str:
    """
    Pick a deterministic clean display form among equivalent variants.

    Preference:
    1. no leading footnote/symbol residue;
    2. shorter cleaned label;
    3. ordinary lexical order for stable ties.
    """
    cleaned = []
    for name in names:
        candidate = re.sub(r"^[^A-Za-z0-9]+\s*", "", name).strip()
        cleaned.append(candidate)

    return sorted(
        set(cleaned),
        key=lambda value: (
            len(value),
            value.casefold(),
            value,
        ),
    )[0]


def load_opponent_names(
    repo_root: Path,
    programs: dict[str, dict[str, str]],
) -> dict[str, str]:
    names_by_key: dict[str, set[str]] = defaultdict(set)

    for key, program in programs.items():
        names_by_key[key].add(program["program_name"].strip())

    schools_dir = repo_root / "schools"
    if schools_dir.exists():
        for path in sorted(schools_dir.glob("*/opponents.csv")):
            for row in read_csv(path):
                key = row.get("canonical_opponent_key", "").strip()
                name = row.get("canonical_opponent_name", "").strip()
                if key and name:
                    names_by_key[key].add(name)

    resolved_names: dict[str, str] = {}
    true_conflicts: dict[str, list[str]] = {}

    for key, names in names_by_key.items():
        if key in programs:
            resolved_names[key] = programs[key]["program_name"].strip()
            continue

        signatures = {normalized_name_signature(name) for name in names}

        if len(signatures) == 1:
            resolved_names[key] = preferred_display_name(names)
        else:
            true_conflicts[key] = sorted(names)

    if true_conflicts:
        sample = "; ".join(
            f"{key}: {names}"
            for key, names in list(sorted(true_conflicts.items()))[:10]
        )
        raise ValueError(
            "Conflicting historical opponent display names found after "
            "punctuation/footnote normalization. Resolve before publishing. "
            + sample
        )

    return resolved_names



def load_venue_names(repo_root: Path) -> dict[str, str]:
    names_by_key: dict[str, set[str]] = defaultdict(set)

    schools_dir = repo_root / "schools"
    if schools_dir.exists():
        for path in sorted(schools_dir.glob("*/venues.csv")):
            for row in read_csv(path):
                key = row.get("venue_key", "").strip()
                name = row.get("canonical_name", "").strip()
                if key and name:
                    names_by_key[key].add(name)

    resolved_names: dict[str, str] = {}
    true_conflicts: dict[str, list[str]] = {}

    for key, names in names_by_key.items():
        signatures = {normalized_name_signature(name) for name in names}

        if len(signatures) == 1:
            resolved_names[key] = preferred_display_name(names)
        else:
            true_conflicts[key] = sorted(names)

    if true_conflicts:
        sample = "; ".join(
            f"{key}: {names}"
            for key, names in list(sorted(true_conflicts.items()))[:10]
        )
        raise ValueError(
            "Conflicting canonical venue display names found after "
            "punctuation normalization. Resolve before publishing. "
            + sample
        )

    return resolved_names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repository_root",
        nargs="?",
        default=None,
        help="Repository root; defaults to the parent of tools/.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write generated JSON to site/data/.",
    )
    args = parser.parse_args()

    repo_root = (
        Path(args.repository_root).resolve()
        if args.repository_root
        else Path(__file__).resolve().parents[1]
    )

    programs_path = repo_root / "data" / "reference" / "programs.csv"
    memberships_path = (
        repo_root / "data" / "reference" / "conference-membership.csv"
    )
    games_path = repo_root / "data" / "canonical" / "games.csv"

    program_rows = read_csv(programs_path)
    membership_rows = read_csv(memberships_path)
    canonical_rows = read_csv(games_path)

    programs = {row["program_key"]: row for row in program_rows}
    if len(programs) != len(program_rows):
        raise ValueError("Duplicate program_key values in programs.csv.")

    if not membership_rows:
        raise ValueError("conference-membership.csv is empty.")

    reference_season = max(row["season_label"] for row in membership_rows)

    current_memberships = {
        row["program_key"]: row
        for row in membership_rows
        if row["season_label"] == reference_season
    }

    opponent_names = load_opponent_names(repo_root, programs)
    venue_names = load_venue_names(repo_root)

    enabled_keys = sorted(
        row["program_key"]
        for row in program_rows
        if yes(row["public_page_enabled"])
    )

    canonical_keys_for_enabled: set[str] = set()
    for row in canonical_rows:
        if row["team_a_key"] in enabled_keys or row["team_b_key"] in enabled_keys:
            canonical_keys_for_enabled.add(row["team_a_key"])
            canonical_keys_for_enabled.add(row["team_b_key"])

    missing_names = sorted(canonical_keys_for_enabled - set(opponent_names))
    if missing_names:
        raise ValueError(
            "Public-team games contain opponent keys with no known display name: "
            + ", ".join(missing_names[:20])
        )

    public_programs = []
    for row in sorted(
        program_rows,
        key=lambda r: (r["display_name"].casefold(), r["program_key"]),
    ):
        membership = current_memberships.get(row["program_key"])
        public_programs.append(
            {
                "program_key": row["program_key"],
                "program_name": row["program_name"],
                "display_name": row["display_name"],
                "nickname": row["nickname"],
                "city": row.get("city", ""),
                "state": row.get("state", ""),
                "primary_hex": row.get("primary_hex", ""),
                "secondary_hex": row.get("secondary_hex", ""),
                "conference_regular_season_championships": (
                    int(row["conference_regular_season_championships"])
                    if row.get("conference_regular_season_championships", "").strip()
                    else None
                ),
                "conference_tournament_championships": (
                    int(row["conference_tournament_championships"])
                    if row.get("conference_tournament_championships", "").strip()
                    else None
                ),
                "final_four_appearances": (
                    int(row["final_four_appearances"])
                    if row.get("final_four_appearances", "").strip()
                    else None
                ),
                "national_championships": (
                    int(row["national_championships"])
                    if row.get("national_championships", "").strip()
                    else None
                ),
                "current_d1": yes(row["current_d1"]),
                "public_page_enabled": yes(row["public_page_enabled"]),
                "current_conference": (
                    {
                        "conference_key": membership["conference_key"],
                        "conference_name": membership["conference_name"],
                    }
                    if membership
                    else None
                ),
            }
        )

    team_payloads: dict[str, dict[str, Any]] = {}

    for program_key in enabled_keys:
        program = programs[program_key]
        membership = current_memberships.get(program_key)

        perspective_games = [
            perspective_game(
                row,
                program_key,
                opponent_names,
                venue_names,
                programs,
            )
            for row in canonical_rows
            if program_key in {row["team_a_key"], row["team_b_key"]}
        ]
        partial_public_locations = [
            game["canonical_game_id"]
            for game in perspective_games
            if bool(game["site_city"]) != bool(game["site_state"])
        ]
        if partial_public_locations:
            raise ValueError(
                "Public game data contains partial city/state geography: "
                + ", ".join(partial_public_locations[:20])
            )
        perspective_games.sort(key=game_sort_key)

        seasons: dict[str, list[dict[str, Any]]] = defaultdict(list)
        opponents: dict[str, list[dict[str, Any]]] = defaultdict(list)

        for game in perspective_games:
            seasons[game["season_label"]].append(game)
            opponents[game["opponent_key"]].append(game)

        season_summaries = []
        for season_label in sorted(seasons, reverse=True):
            season_games = seasons[season_label]
            season_summaries.append(
                {
                    "season_label": season_label,
                    **record_from_games(season_games),
                }
            )

        opponent_summaries = []
        for opponent_key, opponent_games in opponents.items():
            opponent_program = programs.get(opponent_key)
            opponent_membership = current_memberships.get(opponent_key)
            opponent_summaries.append(
                {
                    "opponent_key": opponent_key,
                    "opponent_name": opponent_names[opponent_key],
                    "current_d1": (
                        yes(opponent_program["current_d1"])
                        if opponent_program
                        else False
                    ),
                    "public_page_enabled": (
                        yes(opponent_program["public_page_enabled"])
                        if opponent_program
                        else False
                    ),
                    "current_conference": (
                        {
                            "conference_key": opponent_membership["conference_key"],
                            "conference_name": opponent_membership["conference_name"],
                        }
                        if opponent_membership
                        else None
                    ),
                    "first_season": min(
                        game["season_label"] for game in opponent_games
                    ),
                    "last_season": max(
                        game["season_label"] for game in opponent_games
                    ),
                    **record_from_games(opponent_games),
                }
            )

        opponent_summaries.sort(
            key=lambda row: (row["opponent_name"].casefold(), row["opponent_key"])
        )

        overall = record_from_games(perspective_games)

        team_payloads[program_key] = {
            "schema_version": 1,
            "reference_season": reference_season,
            "program": {
                "program_key": program_key,
                "program_name": program["program_name"],
                "display_name": program["display_name"],
                "nickname": program["nickname"],
                "city": program.get("city", ""),
                "state": program.get("state", ""),
                "primary_hex": program.get("primary_hex", ""),
                "secondary_hex": program.get("secondary_hex", ""),
                "conference_regular_season_championships": (
                    int(program["conference_regular_season_championships"])
                    if program.get("conference_regular_season_championships", "").strip()
                    else None
                ),
                "conference_tournament_championships": (
                    int(program["conference_tournament_championships"])
                    if program.get("conference_tournament_championships", "").strip()
                    else None
                ),
                "final_four_appearances": (
                    int(program["final_four_appearances"])
                    if program.get("final_four_appearances", "").strip()
                    else None
                ),
                "national_championships": (
                    int(program["national_championships"])
                    if program.get("national_championships", "").strip()
                    else None
                ),
                "current_conference": (
                    {
                        "conference_key": membership["conference_key"],
                        "conference_name": membership["conference_name"],
                    }
                    if membership
                    else None
                ),
            },
            "summary": {
                **overall,
                "first_season": min(seasons) if seasons else None,
                "last_season": max(seasons) if seasons else None,
                "opponents": len(opponents),
            },
            "seasons": season_summaries,
            "opponents": opponent_summaries,
            "games": perspective_games,
        }

    manifest = {
        "schema_version": 1,
        "reference_season": reference_season,
        "program_count": len(program_rows),
        "public_page_count": len(enabled_keys),
        "canonical_game_count": len(canonical_rows),
        "files": {
            "programs": "programs.json",
            "teams_root": "teams/",
        },
    }

    programs_payload = {
        "schema_version": 1,
        "reference_season": reference_season,
        "programs": public_programs,
    }

    planned = {
        repo_root / "site" / "data" / "manifest.json": json_text(manifest),
        repo_root / "site" / "data" / "programs.json": json_text(programs_payload),
    }
    for program_key, payload in team_payloads.items():
        planned[
            repo_root / "site" / "data" / "teams" / f"{program_key}.json"
        ] = json_text(payload)

    teams_dir = repo_root / "site" / "data" / "teams"
    expected_team_files = {
        path.resolve()
        for path in planned
        if path.parent.resolve() == teams_dir.resolve()
    }
    stale_team_files = (
        sorted(
            path
            for path in teams_dir.glob("*.json")
            if path.resolve() not in expected_team_files
        )
        if teams_dir.exists()
        else []
    )

    print("College Basketball History — public site-data build")
    print(f"Repository:          {repo_root}")
    print(f"Mode:                {'APPLY' if args.apply else 'DRY RUN'}")
    print()
    print(f"Reference season:    {reference_season}")
    print(f"Programs:            {len(program_rows):,}")
    print(f"Public pages:        {len(enabled_keys):,}")
    print(f"Canonical games:     {len(canonical_rows):,}")
    print(f"Team JSON files:     {len(team_payloads):,}")
    print(f"Stale team files:    {len(stale_team_files):,}")
    print()

    for program_key in enabled_keys:
        payload = team_payloads[program_key]
        summary = payload["summary"]
        print(
            f"- {program_key}: "
            f'{summary["games"]:,} games, '
            f'{summary["wins"]:,}-{summary["losses"]:,}'
            + (f'-{summary["ties"]:,}' if summary["ties"] else "")
            + f', {summary["opponents"]:,} opponents'
        )

    if not args.apply:
        print()
        print("DRY RUN COMPLETE: no files changed.")
        return 0

    for path, contents in planned.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")

    for path in stale_team_files:
        path.unlink()

    print()
    print(f"PASS: wrote {len(planned):,} deterministic JSON files under site/data/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
