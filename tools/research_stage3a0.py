#!/usr/bin/env python3
"""Deterministic Stage 3A-0 census/partition and target-only canonical join.

Usage:
    python tools/research_stage3a0.py <school_key> [repository_root]

The input is the target school's current working source-games.csv. The command performs
no external research, reads no opponent packages, and does not adjudicate historical
contradictions. It writes a durable JSON ledger under .research/<school>/ and stops.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REGULAR = "REGULAR_SEASON"
POSTSEASON = {"NCAA_TOURNAMENT", "NIT", "CONFERENCE_TOURNAMENT", "OTHER_POSTSEASON"}
HOME = "HOME"
OPPONENT_HOME = "OPPONENT_HOME"
NEUTRAL = "NEUTRAL"
UNKNOWN = "UNKNOWN"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def clean(value: str | None) -> str:
    return (value or "").strip()


def ordered_pair(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def source_site(row: dict[str, str]) -> str:
    value = clean(row.get("curated_site_type")).upper()
    if value in {"SOURCE_PROGRAM_HOME", "HOME", "TEAM_HOME"}:
        return HOME
    if value in {"OPPONENT_HOME", "AWAY"}:
        return OPPONENT_HOME
    if value == NEUTRAL:
        return NEUTRAL
    return UNKNOWN


def canonical_site(row: dict[str, str], school: str) -> str:
    value = clean(row.get("site_type")).upper()
    designated = clean(row.get("designated_home_team_key"))
    if value == "NEUTRAL":
        return NEUTRAL
    if value in {"TEAM_A_HOME", "TEAM_B_HOME"}:
        return HOME if designated == school else OPPONENT_HOME
    return UNKNOWN


def same_game_candidates(
    source: dict[str, str],
    index: dict[tuple[str, str, str], list[dict[str, str]]],
) -> list[dict[str, str]]:
    school = clean(source.get("source_program_key"))
    opp = clean(source.get("normalized_opponent_key"))
    season = clean(source.get("season_label"))
    if not school or not opp or not season:
        return []
    a, b = ordered_pair(school, opp)
    candidates = index.get((a, b, season), [])
    date = clean(source.get("game_date"))
    if date:
        dated = [r for r in candidates if clean(r.get("game_date")) == date]
        if dated:
            return dated
    team_score = clean(source.get("team_score"))
    opp_score = clean(source.get("opponent_score"))
    if team_score and opp_score:
        scored = []
        for row in candidates:
            if clean(row.get("team_a_key")) == school:
                pair = (clean(row.get("team_a_score")), clean(row.get("team_b_score")))
            else:
                pair = (clean(row.get("team_b_score")), clean(row.get("team_a_score")))
            if pair == (team_score, opp_score):
                scored.append(row)
        if scored:
            return scored
    return candidates if len(candidates) == 1 else []


def row_summary(row: dict[str, str]) -> dict[str, str]:
    keys = (
        "source_game_id", "season_label", "game_date", "normalized_opponent_key",
        "normalized_opponent_name", "curated_game_type", "curated_site_type",
        "curated_venue_name", "city", "state",
    )
    return {key: clean(row.get(key)) for key in keys}


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: python tools/research_stage3a0.py <school_key> [repository_root]")
        return 2

    school = sys.argv[1].strip()
    root = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else Path(__file__).resolve().parents[1]
    source_path = root / "schools" / school / "source-games.csv"
    canonical_path = root / "data" / "canonical" / "games.csv"

    try:
        source_rows = read_csv(source_path)
        canonical_rows = read_csv(canonical_path)
    except FileNotFoundError as exc:
        print(f"FAIL: required structured input not found: {exc}")
        return 1

    if not source_rows:
        print("FAIL: target source-games.csv is empty")
        return 1
    wrong_school = sorted({clean(r.get("source_program_key")) for r in source_rows if clean(r.get("source_program_key")) != school})
    if wrong_school:
        print(f"FAIL: source-games contains rows outside target school: {wrong_school}")
        return 1

    canonical_index: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in canonical_rows:
        a = clean(row.get("team_a_key"))
        b = clean(row.get("team_b_key"))
        season = clean(row.get("season_label"))
        if school not in {a, b}:
            continue
        x, y = ordered_pair(a, b)
        canonical_index[(x, y, season)].append(row)

    regular = []
    postseason = []
    invalid_types = []
    for row in source_rows:
        game_type = clean(row.get("curated_game_type")).upper()
        if game_type == REGULAR:
            regular.append(row)
        elif game_type in POSTSEASON:
            postseason.append(row)
        else:
            invalid_types.append(row)

    site_counts = Counter(source_site(r) for r in regular)
    queues = {HOME: [], OPPONENT_HOME: [], NEUTRAL: [], UNKNOWN: []}
    modern_neutral = []
    historical_neutral = []
    accepted = []
    unmatched = []
    contradictions = []

    for row in regular:
        site = source_site(row)
        queues[site].append(row_summary(row))
        if site == NEUTRAL:
            season = clean(row.get("season_label"))
            start_year = int(season[:4]) if len(season) >= 4 and season[:4].isdigit() else None
            (modern_neutral if start_year is not None and start_year >= 1996 else historical_neutral).append(row_summary(row))

        candidates = same_game_candidates(row, canonical_index)
        if len(candidates) != 1:
            unmatched.append({**row_summary(row), "candidate_count": len(candidates)})
            continue
        candidate = candidates[0]
        csite = canonical_site(candidate, school)
        source_class = source_site(row)
        if source_class != UNKNOWN and csite != UNKNOWN and source_class != csite:
            contradictions.append({
                **row_summary(row),
                "canonical_game_id": clean(candidate.get("canonical_game_id")),
                "source_site_class": source_class,
                "canonical_site_class": csite,
            })
        else:
            accepted.append({
                **row_summary(row),
                "canonical_game_id": clean(candidate.get("canonical_game_id")),
                "canonical_site_class": csite,
                "canonical_venue_key": clean(candidate.get("venue_key")),
                "canonical_venue_id": clean(candidate.get("venue_id")),
                "canonical_city": clean(candidate.get("site_city")),
                "canonical_state": clean(candidate.get("site_state")),
            })

    payload = {
        "schema_version": 1,
        "stage": "3A-0",
        "school_key": school,
        "contract": "deterministic target-only structured-data join",
        "inputs": {
            "source_games": str(source_path.relative_to(root)),
            "canonical_games": str(canonical_path.relative_to(root)),
        },
        "external_historical_research_used": False,
        "counts": {
            "stage1_total": len(source_rows),
            "regular_season": len(regular),
            "postseason_handoff": len(postseason),
            "invalid_or_unclassified_game_type": len(invalid_types),
            "home": site_counts[HOME],
            "opponent_home": site_counts[OPPONENT_HOME],
            "neutral": site_counts[NEUTRAL],
            "unknown": site_counts[UNKNOWN],
            "modern_neutral_1996_97_plus": len(modern_neutral),
            "historical_neutral_1995_96_and_earlier": len(historical_neutral),
            "canonical_join_accepted": len(accepted),
            "canonical_join_unmatched": len(unmatched),
            "canonical_join_contradictions": len(contradictions),
        },
        "queues": {
            "stage3a1_han": queues[UNKNOWN],
            "stage3a2_home": queues[HOME],
            "stage3a3_neutral_modern": modern_neutral,
            "stage3a3_neutral_historical": historical_neutral,
            "opponent_home": queues[OPPONENT_HOME],
            "postseason_stage3b": [row_summary(r) for r in postseason],
            "canonical_join_unmatched": unmatched,
            "canonical_join_contradictions": contradictions,
        },
        "accepted_target_canonical_join": accepted,
        "invalid_or_unclassified_rows": [row_summary(r) for r in invalid_types],
    }

    out_dir = root / ".research" / school
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "stage3a0-ledger.json"
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    out_path.write_text(serialized, encoding="utf-8")
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    print("College Basketball History — deterministic Research Stage 3A-0")
    print(f"School: {school}")
    print(f"Stage 1 total: {len(source_rows):,}")
    print(f"Regular season: {len(regular):,}")
    print(f"Postseason handoff: {len(postseason):,}")
    print(f"H/A/N: {site_counts[HOME]:,} HOME / {site_counts[OPPONENT_HOME]:,} OPPONENT_HOME / {site_counts[NEUTRAL]:,} NEUTRAL / {site_counts[UNKNOWN]:,} UNKNOWN")
    print(f"Canonical join: {len(accepted):,} accepted / {len(unmatched):,} unmatched / {len(contradictions):,} contradictions")
    print(f"Ledger: {out_path}")
    print(f"Ledger SHA-256: {digest}")
    if invalid_types:
        print(f"INCOMPLETE: {len(invalid_types):,} rows have invalid/unclassified game_type; exact queue serialized.")
        return 1
    print("External historical research used: NO")
    print("STAGE 3A-0: COMPLETE")
    print("Next bounded assignment: Stage 3A-1 — H/A/N completion")
    print("STOPPING AT THE REQUIRED STAGE 3A SUBSTAGE BOUNDARY.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
