#!/usr/bin/env python3
"""Authoritative read-only census of published game-site completeness debt.

The census measures the exact public-game universe implied by programs.csv and each
published program's approved history_start_season. It never mutates basketball data.

HOME exception accounting is deliberately delegated to implementation_site_gate so
this scoreboard cannot drift from the hardened per-school release semantics.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from implementation_site_gate import implementation_site_report
from program_history import season_is_in_scope


POSTSEASON_TYPES = {
    "NCAA_TOURNAMENT",
    "CONFERENCE_TOURNAMENT",
    "NIT",
    "POSTSEASON",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def yes(value: str) -> bool:
    return (value or "").strip().lower() == "yes"


def venue_known(row: dict[str, str]) -> bool:
    return bool(row.get("venue_key", "").strip() or row.get("venue_id", "").strip())


def location_complete(row: dict[str, str]) -> bool:
    return bool(row.get("site_city", "").strip() and row.get("site_state", "").strip())


def site_completely_blank(row: dict[str, str]) -> bool:
    return (
        not venue_known(row)
        and not row.get("site_city", "").strip()
        and not row.get("site_state", "").strip()
    )


def season_decade(season_label: str) -> str:
    value = (season_label or "").strip()
    if len(value) < 4 or not value[:4].isdigit():
        return "UNKNOWN"
    start_year = int(value[:4])
    return f"{start_year // 10 * 10}s"


def postseason_bucket(game_type: str) -> str | None:
    value = (game_type or "").strip().upper()
    if value == "NCAA_TOURNAMENT":
        return "ncaa"
    if value == "CONFERENCE_TOURNAMENT":
        return "conference_tournament"
    if value == "NIT":
        return "nit"
    if value == "POSTSEASON":
        return "other_postseason"
    return None


def empty_gap_counts() -> dict[str, int]:
    return {
        "total": 0,
        "missing_venue": 0,
        "missing_location": 0,
        "missing_any": 0,
        "completely_blank": 0,
    }


def add_gap_counts(counts: dict[str, int], row: dict[str, str]) -> None:
    missing_venue = not venue_known(row)
    missing_location = not location_complete(row)
    counts["total"] += 1
    counts["missing_venue"] += int(missing_venue)
    counts["missing_location"] += int(missing_location)
    counts["missing_any"] += int(missing_venue or missing_location)
    counts["completely_blank"] += int(site_completely_blank(row))


def _published_perspectives(
    row: dict[str, str],
    published: dict[str, dict[str, str]],
) -> list[str]:
    season = row.get("season_label", "").strip()
    perspectives: list[str] = []
    for key in {row.get("team_a_key", "").strip(), row.get("team_b_key", "").strip()}:
        if not key or key not in published:
            continue
        if season_is_in_scope(season, published[key]["history_start_season"]):
            perspectives.append(key)
    return sorted(perspectives)


def _is_home_for(row: dict[str, str], program_key: str) -> bool:
    site = row.get("site_type", "").strip().upper()
    return (
        site == "TEAM_A_HOME" and row.get("team_a_key", "").strip() == program_key
    ) or (
        site == "TEAM_B_HOME" and row.get("team_b_key", "").strip() == program_key
    )


def _event_labels_by_game(assertions: Iterable[dict[str, str]]) -> dict[str, tuple[str, ...]]:
    labels: dict[str, set[str]] = defaultdict(set)
    for row in assertions:
        canonical_id = row.get("canonical_game_id", "").strip()
        event = row.get("event_or_tournament", "").strip()
        if canonical_id and event:
            labels[canonical_id].add(event)
    return {key: tuple(sorted(values)) for key, values in labels.items()}


def build_census(repo: Path, *, example_limit: int = 10) -> dict[str, Any]:
    programs = read_csv(repo / "data/reference/programs.csv")
    canonical = read_csv(repo / "data/canonical/games.csv")
    assertions = read_csv(repo / "data/evidence/game-assertions.csv")

    published: dict[str, dict[str, str]] = {}
    for row in programs:
        if not yes(row.get("public_page_enabled", "")):
            continue
        key = row.get("program_key", "").strip()
        history_start = row.get("history_start_season", "").strip()
        if not key or not history_start:
            raise ValueError(
                "every public_page_enabled program must have program_key and history_start_season"
            )
        published[key] = {
            "program_key": key,
            "display_name": row.get("display_name", "").strip() or key,
            "history_start_season": history_start,
        }

    if not published:
        raise ValueError("no public_page_enabled programs found")

    event_labels = _event_labels_by_game(assertions)

    public_rows: list[tuple[dict[str, str], list[str]]] = []
    for row in canonical:
        perspectives = _published_perspectives(row, published)
        if perspectives:
            public_rows.append((row, perspectives))

    home = {
        "total_home_games": 0,
        "missing_venue": 0,
        "missing_location": 0,
        "missing_any": 0,
        "completely_blank": 0,
        "hard_blockers": 0,
        "researched_unresolved_venue_exceptions": 0,
        "invalid_exception_markers": 0,
    }
    postseason = {
        "all": empty_gap_counts(),
        "ncaa": empty_gap_counts(),
        "conference_tournament": empty_gap_counts(),
        "nit": empty_gap_counts(),
        "other_postseason": empty_gap_counts(),
    }
    neutral = {
        "all": empty_gap_counts(),
        "regular_season": empty_gap_counts(),
        "postseason": empty_gap_counts(),
        "published_vs_published": empty_gap_counts(),
    }

    by_game_type: dict[str, dict[str, int]] = defaultdict(empty_gap_counts)
    by_team: dict[str, dict[str, Any]] = {}
    for key, meta in sorted(published.items()):
        gate = implementation_site_report(repo, key, example_limit=example_limit)
        counts = gate["counts"]
        home["hard_blockers"] += counts.get("strict_home_gap_rows", 0)
        home["researched_unresolved_venue_exceptions"] += counts.get(
            "researched_unresolved_home_venue_rows", 0
        )
        home["invalid_exception_markers"] += counts.get(
            "invalid_home_venue_exception_marker_rows", 0
        )
        by_team[key] = {
            "display_name": meta["display_name"],
            "history_start_season": meta["history_start_season"],
            "total_games": 0,
            "home": {
                "total_home_games": 0,
                "missing_venue": 0,
                "missing_location": 0,
                "missing_any": 0,
                "completely_blank": 0,
                "hard_blockers": counts.get("strict_home_gap_rows", 0),
                "researched_unresolved_venue_exceptions": counts.get(
                    "researched_unresolved_home_venue_rows", 0
                ),
                "invalid_exception_markers": counts.get(
                    "invalid_home_venue_exception_marker_rows", 0
                ),
            },
            "postseason": empty_gap_counts(),
            "neutral": empty_gap_counts(),
        }

    by_decade = {
        "home_hard_blocker_candidates": Counter(),
        "postseason_missing_any": Counter(),
        "neutral_missing_any": Counter(),
    }
    unknown_site_type = 0
    partial_location_rows = 0

    event_counters: dict[tuple[str, tuple[str, ...]], dict[str, Any]] = {}

    for row, perspectives in public_rows:
        game_type = row.get("game_type", "").strip().upper() or "UNKNOWN"
        site_type = row.get("site_type", "").strip().upper()
        missing_venue = not venue_known(row)
        missing_location = not location_complete(row)
        missing_any = missing_venue or missing_location
        decade = season_decade(row.get("season_label", ""))

        if site_type in {"", "UNKNOWN"}:
            unknown_site_type += 1
        if bool(row.get("site_city", "").strip()) != bool(row.get("site_state", "").strip()):
            partial_location_rows += 1

        add_gap_counts(by_game_type[game_type], row)

        home_programs = [key for key in perspectives if _is_home_for(row, key)]
        if home_programs:
            # Canonical site_type can identify at most one home program. Counting the
            # row once keeps the global HOME denominator canonical-game based.
            home["total_home_games"] += 1
            home["missing_venue"] += int(missing_venue)
            home["missing_location"] += int(missing_location)
            home["missing_any"] += int(missing_any)
            home["completely_blank"] += int(site_completely_blank(row))
            if missing_any:
                by_decade["home_hard_blocker_candidates"][decade] += 1

        bucket = postseason_bucket(game_type)
        if bucket is not None:
            add_gap_counts(postseason["all"], row)
            add_gap_counts(postseason[bucket], row)
            if missing_any:
                by_decade["postseason_missing_any"][decade] += 1

        if site_type == "NEUTRAL":
            add_gap_counts(neutral["all"], row)
            if game_type == "REGULAR_SEASON":
                add_gap_counts(neutral["regular_season"], row)
            if bucket is not None:
                add_gap_counts(neutral["postseason"], row)
            if len(perspectives) == 2:
                add_gap_counts(neutral["published_vs_published"], row)
            if missing_any:
                by_decade["neutral_missing_any"][decade] += 1

        for key in perspectives:
            team = by_team[key]
            team["total_games"] += 1
            if _is_home_for(row, key):
                team_home = team["home"]
                team_home["total_home_games"] += 1
                team_home["missing_venue"] += int(missing_venue)
                team_home["missing_location"] += int(missing_location)
                team_home["missing_any"] += int(missing_any)
                team_home["completely_blank"] += int(site_completely_blank(row))
            if bucket is not None:
                add_gap_counts(team["postseason"], row)
            if site_type == "NEUTRAL":
                add_gap_counts(team["neutral"], row)

        if game_type == "CONFERENCE_TOURNAMENT" and missing_any:
            canonical_id = row.get("canonical_game_id", "").strip()
            labels = event_labels.get(canonical_id, ())
            event_key = (row.get("season_label", "").strip() or "UNKNOWN", labels)
            event = event_counters.setdefault(
                event_key,
                {
                    "season_label": event_key[0],
                    "event_labels": list(labels),
                    "games": 0,
                    "missing_venue": 0,
                    "missing_location": 0,
                    "completely_blank": 0,
                    "published_program_keys": set(),
                    "example_game_ids": [],
                },
            )
            event["games"] += 1
            event["missing_venue"] += int(missing_venue)
            event["missing_location"] += int(missing_location)
            event["completely_blank"] += int(site_completely_blank(row))
            event["published_program_keys"].update(perspectives)
            if canonical_id and len(event["example_game_ids"]) < example_limit:
                event["example_game_ids"].append(canonical_id)

    # The raw HOME missing-any denominator should partition cleanly into either a
    # validated historical exception or a hard blocker. If it does not, the census
    # itself is not authoritative and must fail rather than publish contradictory debt.
    partitioned_home_gaps = (
        home["hard_blockers"] + home["researched_unresolved_venue_exceptions"]
    )
    if partitioned_home_gaps != home["missing_any"]:
        raise ValueError(
            "HOME gap accounting mismatch: canonical missing_any="
            f"{home['missing_any']} but strict blockers + valid exceptions="
            f"{partitioned_home_gaps}. Run the per-school implementation gate to locate "
            "the accounting mismatch before trusting this census."
        )

    conference_gap_events = []
    for _, event in sorted(
        event_counters.items(),
        key=lambda item: (item[0][0], item[0][1]),
    ):
        event["published_program_keys"] = sorted(event["published_program_keys"])
        conference_gap_events.append(event)

    return {
        "schema_version": 1,
        "published_program_count": len(published),
        "published_program_keys": sorted(published),
        "published_unique_canonical_games": len(public_rows),
        "unknown_site_type_games": unknown_site_type,
        "partial_city_state_games": partial_location_rows,
        "home": home,
        "postseason": postseason,
        "neutral": neutral,
        "by_team": by_team,
        "by_decade": {
            key: dict(sorted(counter.items()))
            for key, counter in by_decade.items()
        },
        "by_game_type": {
            key: value for key, value in sorted(by_game_type.items())
        },
        "conference_tournament_gap_events": conference_gap_events,
    }


def print_text(report: dict[str, Any]) -> None:
    print("College Basketball History — published site completeness census")
    print(f"Published programs:      {report['published_program_count']}")
    print(f"Unique public games:     {report['published_unique_canonical_games']:,}")
    print(f"Unknown site type:       {report['unknown_site_type_games']:,}")
    print(f"Partial city/state:      {report['partial_city_state_games']:,}")

    home = report["home"]
    print("\nHOME")
    print(f"  total:                 {home['total_home_games']:,}")
    print(f"  missing venue:         {home['missing_venue']:,}")
    print(f"  missing location:      {home['missing_location']:,}")
    print(f"  hard blockers:         {home['hard_blockers']:,}")
    print(
        "  researched exception: "
        f"{home['researched_unresolved_venue_exceptions']:,}"
    )
    print(f"  invalid markers:       {home['invalid_exception_markers']:,}")

    print("\nPOSTSEASON")
    for key in ("all", "ncaa", "conference_tournament", "nit", "other_postseason"):
        counts = report["postseason"][key]
        print(
            f"  {key:22} total={counts['total']:,} "
            f"missing_venue={counts['missing_venue']:,} "
            f"missing_location={counts['missing_location']:,} "
            f"completely_blank={counts['completely_blank']:,}"
        )

    print("\nNEUTRAL")
    for key in ("all", "regular_season", "postseason", "published_vs_published"):
        counts = report["neutral"][key]
        print(
            f"  {key:22} total={counts['total']:,} "
            f"missing_venue={counts['missing_venue']:,} "
            f"missing_location={counts['missing_location']:,} "
            f"completely_blank={counts['completely_blank']:,}"
        )

    print("\nBY TEAM — HOME hard blockers / postseason gaps / neutral gaps")
    for key, team in sorted(report["by_team"].items()):
        print(
            f"  {key:24} home={team['home']['hard_blockers']:,} "
            f"postseason={team['postseason']['missing_any']:,} "
            f"neutral={team['neutral']['missing_any']:,}"
        )

    events = report["conference_tournament_gap_events"]
    print(f"\nConference-tournament gap event groups: {len(events):,}")
    for event in events[:20]:
        labels = " | ".join(event["event_labels"]) or "event unlabeled"
        print(
            f"  {event['season_label']} — {labels}: games={event['games']:,}, "
            f"missing_venue={event['missing_venue']:,}, "
            f"missing_location={event['missing_location']:,}"
        )
    if len(events) > 20:
        print(f"  ... {len(events) - 20:,} more event groups; use --json for the full ledger")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repository_root",
        nargs="?",
        default=None,
        help="Repository root; defaults to the parent of tools/.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the complete machine-readable census instead of the text summary.",
    )
    parser.add_argument(
        "--example-limit",
        type=int,
        default=10,
        help="Maximum example canonical IDs retained per conference-tournament event group.",
    )
    args = parser.parse_args()

    repo = (
        Path(args.repository_root).resolve()
        if args.repository_root
        else Path(__file__).resolve().parents[1]
    )
    report = build_census(repo, example_limit=max(0, args.example_limit))
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
