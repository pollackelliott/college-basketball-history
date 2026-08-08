#!/usr/bin/env python3
"""
Read-only matcher for curated school source games against the global canonical game table.

Usage:
    python tools/match_games.py missouri

Optional repository root:
    python tools/match_games.py missouri /path/to/college-basketball-history

This tool DOES NOT modify repository files.

Important distinction:
- Matching decides whether two source rows describe the SAME GAME.
- Field comparison decides whether the sources AGREE about that game.

A unique same-team-pair + same-season + same-date match is therefore a confident
game-identity match even when score/site/etc. differs. Those differences belong in
the reconciliation layer; they should not cause duplicate canonical games.
"""

from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path


CONFIDENT = "CONFIDENT_MATCH"
REVIEW = "REVIEW"
NEW_GAME = "NEW_GAME"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def ordered_pair(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a.strip(), b.strip())))


def source_scores_in_canonical_orientation(row: dict[str, str]) -> tuple[str, str]:
    school = row.get("source_program_key", "").strip()
    opp = row.get("normalized_opponent_key", "").strip()
    team_a, _ = ordered_pair(school, opp)

    school_score = row.get("team_score", "").strip()
    opp_score = row.get("opponent_score", "").strip()

    if team_a == school:
        return school_score, opp_score
    return opp_score, school_score


def scores_match(source: dict[str, str], canonical: dict[str, str]) -> bool:
    src_a, src_b = source_scores_in_canonical_orientation(source)
    can_a = canonical.get("team_a_score", "").strip()
    can_b = canonical.get("team_b_score", "").strip()
    return (
        src_a != ""
        and src_b != ""
        and can_a != ""
        and can_b != ""
        and src_a == can_a
        and src_b == can_b
    )


def compare_fields(source: dict[str, str], canonical: dict[str, str]) -> list[str]:
    """
    Compare fields that exist meaningfully in both layers.
    These are evidence differences, not game-identity failures.
    """
    differences: list[str] = []

    src_date = source.get("game_date", "").strip()
    can_date = canonical.get("game_date", "").strip()
    if src_date and can_date and src_date != can_date:
        differences.append("date")

    src_a, src_b = source_scores_in_canonical_orientation(source)
    can_a = canonical.get("team_a_score", "").strip()
    can_b = canonical.get("team_b_score", "").strip()
    if src_a and src_b and can_a and can_b and (src_a != can_a or src_b != can_b):
        differences.append("score")

    src_ot = source.get("overtime_periods", "").strip()
    can_ot = canonical.get("overtime_periods", "").strip()
    if src_ot and can_ot and src_ot != can_ot:
        differences.append("overtime_periods")

    return differences


def identify_game(
    source: dict[str, str],
    candidates: list[dict[str, str]],
) -> tuple[str, str, str]:
    """
    Return (identity_status, canonical_game_id, match_method).
    """
    if not candidates:
        return NEW_GAME, "", "NO_SAME_SEASON_TEAM_PAIR"

    src_date = source.get("game_date", "").strip()

    # Rule 1: unique same team pair + season + exact date.
    # Score agreement is NOT required to establish identity.
    if src_date:
        same_date = [
            c for c in candidates
            if c.get("game_date", "").strip() == src_date
        ]

        if len(same_date) == 1:
            return CONFIDENT, same_date[0]["canonical_game_id"], "UNIQUE_PAIR_SEASON_DATE"

        if len(same_date) > 1:
            # If multiple games somehow share the same pair/date, score may distinguish them.
            same_date_score = [c for c in same_date if scores_match(source, c)]
            if len(same_date_score) == 1:
                return (
                    CONFIDENT,
                    same_date_score[0]["canonical_game_id"],
                    "PAIR_SEASON_DATE_PLUS_SCORE_DISAMBIGUATION",
                )
            return REVIEW, "", "MULTIPLE_PAIR_SEASON_DATE_CANDIDATES"

    # Rule 2: when exact date is unavailable, unique same-season score match.
    same_score = [c for c in candidates if scores_match(source, c)]
    if len(same_score) == 1:
        candidate = same_score[0]
        can_date = candidate.get("game_date", "").strip()

        # Safe only if at least one side lacks an exact date.
        if not src_date or not can_date:
            return (
                CONFIDENT,
                candidate["canonical_game_id"],
                "UNIQUE_PAIR_SEASON_SCORE_DATE_INCOMPLETE",
            )

    if len(same_score) > 1:
        return REVIEW, "", "MULTIPLE_PAIR_SEASON_SCORE_CANDIDATES"

    # Rule 3: one same-season meeting is a candidate, but not enough by itself
    # when date/score failed to establish identity.
    if len(candidates) == 1:
        return REVIEW, candidates[0]["canonical_game_id"], "UNIQUE_PAIR_SEASON_ONLY"

    return REVIEW, "", "MULTIPLE_SAME_SEASON_CANDIDATES"


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: python tools/match_games.py <school_key> [repository_root]")
        return 2

    school_key = sys.argv[1].strip()
    repo_root = (
        Path(sys.argv[2]).resolve()
        if len(sys.argv) == 3
        else Path(__file__).resolve().parents[1]
    )

    source_path = repo_root / "schools" / school_key / "source-games.csv"
    canonical_path = repo_root / "data" / "canonical" / "games.csv"

    try:
        source_rows = read_csv(source_path)
        canonical_rows = read_csv(canonical_path)
    except FileNotFoundError as exc:
        print(f"FAIL: required file not found: {exc}")
        return 1

    index: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    canonical_by_id: dict[str, dict[str, str]] = {}

    for row in canonical_rows:
        team_a = row.get("team_a_key", "").strip()
        team_b = row.get("team_b_key", "").strip()
        season = row.get("season_label", "").strip()
        index[(team_a, team_b, season)].append(row)
        canonical_by_id[row["canonical_game_id"]] = row

    results = []

    for src in source_rows:
        school = src.get("source_program_key", "").strip()
        opp = src.get("normalized_opponent_key", "").strip()
        season = src.get("season_label", "").strip()

        if not school or not opp or not season:
            results.append({
                "identity_status": REVIEW,
                "canonical_game_id": "",
                "match_method": "MISSING_REQUIRED_SOURCE_IDENTITY",
                "differences": [],
                "source": src,
            })
            continue

        team_a, team_b = ordered_pair(school, opp)
        candidates = index.get((team_a, team_b, season), [])

        status, game_id, method = identify_game(src, candidates)
        differences = []

        if status == CONFIDENT and game_id:
            differences = compare_fields(src, canonical_by_id[game_id])

        results.append({
            "identity_status": status,
            "canonical_game_id": game_id,
            "match_method": method,
            "differences": differences,
            "source": src,
        })

    identity_counts = Counter(r["identity_status"] for r in results)
    difference_counts = Counter(
        field
        for r in results
        for field in r["differences"]
    )
    matched_with_differences = sum(
        r["identity_status"] == CONFIDENT and bool(r["differences"])
        for r in results
    )

    print("College Basketball History — read-only game matcher")
    print(f"Repository: {repo_root}")
    print(f"School:     {school_key}")
    print()
    print(f"Source rows:                 {len(source_rows):,}")
    print(f"Confident identity matches:  {identity_counts[CONFIDENT]:,}")
    print(f"Review required:             {identity_counts[REVIEW]:,}")
    print(f"New games:                   {identity_counts[NEW_GAME]:,}")
    print(f"Matched rows with differences:{matched_with_differences:>8,}")
    print()

    if difference_counts:
        print("FIELD DIFFERENCES ON CONFIDENTLY MATCHED GAMES:")
        for field, count in sorted(difference_counts.items()):
            print(f"  - {field}: {count:,}")
        print()

    review_rows = [r for r in results if r["identity_status"] == REVIEW]
    new_rows = [r for r in results if r["identity_status"] == NEW_GAME]

    if review_rows:
        print("REVIEW SAMPLE:")
        for r in review_rows[:20]:
            s = r["source"]
            print(
                "  - "
                f"{s.get('source_game_id','')} | "
                f"{s.get('season_label','')} | "
                f"{s.get('game_date','') or '[no exact date]'} | "
                f"{s.get('normalized_opponent_name','')} | "
                f"{s.get('team_score','')}-{s.get('opponent_score','')} | "
                f"{r['canonical_game_id'] or '[no unique candidate]'} | "
                f"{r['match_method']}"
            )
        if len(review_rows) > 20:
            print(f"  ... {len(review_rows) - 20} more")
        print()

    if new_rows:
        print("NEW GAME SAMPLE:")
        for r in new_rows[:20]:
            s = r["source"]
            print(
                "  - "
                f"{s.get('source_game_id','')} | "
                f"{s.get('season_label','')} | "
                f"{s.get('game_date','') or '[no exact date]'} | "
                f"{s.get('normalized_opponent_name','')} | "
                f"{s.get('team_score','')}-{s.get('opponent_score','')}"
            )
        if len(new_rows) > 20:
            print(f"  ... {len(new_rows) - 20} more")
        print()

    if (
        identity_counts[CONFIDENT] == len(source_rows)
        and identity_counts[REVIEW] == 0
        and identity_counts[NEW_GAME] == 0
    ):
        print("PASS: every source row matched exactly one existing canonical game with high-confidence identity.")
        if matched_with_differences:
            print(
                "NOTE: field differences are expected evidence/reconciliation items; "
                "they do not create duplicate games."
            )
        return 0

    print("CHECK: matcher completed safely; non-confident identities were not auto-matched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
