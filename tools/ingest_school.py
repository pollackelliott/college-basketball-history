#!/usr/bin/env python3
"""
Safely ingest one curated school's source-games.csv into the global data layers.

Default mode is DRY RUN. Nothing is written unless --apply is supplied.

Usage:
    python tools/ingest_school.py missouri
    python tools/ingest_school.py missouri --apply

Optional repository root:
    python tools/ingest_school.py missouri --repo /path/to/college-basketball-history

Current responsibilities:
- Match source rows to existing canonical games conservatively.
- Create new canonical games only when no same-season team-pair candidate exists.
- Add missing source assertions.
- Detect field disagreements on confidently matched games.
- Refuse to apply if any identity matches require review.
- Preserve permanent canonical_game_id values.
- Run tools/validate_data.py after an applied write.

Important:
- A score/site/etc. disagreement does NOT create a second canonical game.
- This script does not silently overwrite canonical facts from a new source.
- Conflicting evidence is appended to discrepancies.csv for later review.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


CONFIDENT = "CONFIDENT_MATCH"
REVIEW = "REVIEW"
NEW_GAME = "NEW_GAME"

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

ASSERTION_FIELDS = [
    "assertion_id",
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
    "source_era",
    "season_label",
    "game_date",
    "source_opponent_label",
    "normalized_opponent_key",
    "normalized_opponent_name",
    "team_score",
    "opponent_score",
    "played_result",
    "overtime_periods",
    "source_site_candidate",
    "curated_site_type",
    "source_venue_name",
    "curated_venue_name",
    "city",
    "state",
    "event_or_tournament",
    "source_round",
    "curated_game_type",
    "curated_postseason_round",
    "source_page",
    "raw_text",
    "normalization_status",
    "notes",
    "match_status",
    "match_method",
]

DISCREPANCY_FIELDS = [
    "discrepancy_id",
    "canonical_game_id",
    "field_name",
    "source_a_program_key",
    "source_a_value",
    "source_b_program_key",
    "source_b_value",
    "canonical_value",
    "status",
    "resolution_basis",
    "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    tmp.replace(path)


def ordered_pair(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a.strip(), b.strip())))


def source_scores_in_canonical_orientation(row: dict[str, str]) -> tuple[str, str]:
    school = row.get("source_program_key", "").strip()
    opp = row.get("normalized_opponent_key", "").strip()
    team_a, _ = ordered_pair(school, opp)
    school_score = row.get("team_score", "").strip()
    opp_score = row.get("opponent_score", "").strip()
    return (school_score, opp_score) if team_a == school else (opp_score, school_score)


def source_site_to_canonical(row: dict[str, str]) -> tuple[str, str]:
    school = row.get("source_program_key", "").strip()
    opp = row.get("normalized_opponent_key", "").strip()
    team_a, team_b = ordered_pair(school, opp)
    site = row.get("curated_site_type", "").strip()

    if site == "SOURCE_PROGRAM_HOME":
        return ("TEAM_A_HOME" if team_a == school else "TEAM_B_HOME", school)
    if site == "OPPONENT_HOME":
        return ("TEAM_A_HOME" if team_a == opp else "TEAM_B_HOME", opp)
    if site == "NEUTRAL":
        return ("NEUTRAL", "")
    return ("UNKNOWN", "")


def scores_match(source: dict[str, str], canonical: dict[str, str]) -> bool:
    src_a, src_b = source_scores_in_canonical_orientation(source)
    return (
        src_a != ""
        and src_b != ""
        and src_a == canonical.get("team_a_score", "").strip()
        and src_b == canonical.get("team_b_score", "").strip()
    )


def identify_game(
    source: dict[str, str],
    candidates: list[dict[str, str]],
) -> tuple[str, str, str]:
    if not candidates:
        return NEW_GAME, "", "NO_SAME_SEASON_TEAM_PAIR"

    src_date = source.get("game_date", "").strip()

    if src_date:
        same_date = [c for c in candidates if c.get("game_date", "").strip() == src_date]

        if len(same_date) == 1:
            return CONFIDENT, same_date[0]["canonical_game_id"], "UNIQUE_PAIR_SEASON_DATE"

        if len(same_date) > 1:
            same_date_score = [c for c in same_date if scores_match(source, c)]
            if len(same_date_score) == 1:
                return (
                    CONFIDENT,
                    same_date_score[0]["canonical_game_id"],
                    "PAIR_SEASON_DATE_PLUS_SCORE_DISAMBIGUATION",
                )
            return REVIEW, "", "MULTIPLE_PAIR_SEASON_DATE_CANDIDATES"

    same_score = [c for c in candidates if scores_match(source, c)]

    if len(same_score) == 1:
        candidate = same_score[0]
        can_date = candidate.get("game_date", "").strip()

        if not src_date or not can_date:
            return (
                CONFIDENT,
                candidate["canonical_game_id"],
                "UNIQUE_PAIR_SEASON_SCORE_DATE_INCOMPLETE",
            )

        # A unique same-season score match is strong enough to establish game
        # identity even when two official sources disagree on the exact date.
        # The date disagreement is preserved separately in reconciliation;
        # it must not create a duplicate canonical game.
        if src_date != can_date:
            return (
                CONFIDENT,
                candidate["canonical_game_id"],
                "UNIQUE_PAIR_SEASON_SCORE_DATE_CONFLICT",
            )

    if len(same_score) > 1:
        return REVIEW, "", "MULTIPLE_PAIR_SEASON_SCORE_CANDIDATES"

    if len(candidates) == 1:
        return REVIEW, candidates[0]["canonical_game_id"], "UNIQUE_PAIR_SEASON_ONLY"

    return REVIEW, "", "MULTIPLE_SAME_SEASON_CANDIDATES"


def discrepancy_candidates(
    source: dict[str, str],
    canonical: dict[str, str],
) -> list[tuple[str, str, str]]:
    """
    Return (field_name, source_value, canonical_value) for material disagreements.
    Blank source values do not overwrite or conflict with known canonical values.
    """
    result = []

    src_date = source.get("game_date", "").strip()
    can_date = canonical.get("game_date", "").strip()
    if src_date and can_date and src_date != can_date:
        result.append(("game_date", src_date, can_date))

    src_a, src_b = source_scores_in_canonical_orientation(source)
    can_a = canonical.get("team_a_score", "").strip()
    can_b = canonical.get("team_b_score", "").strip()
    if src_a and src_b and can_a and can_b and (src_a != can_a or src_b != can_b):
        result.append(("score", f"{src_a}-{src_b}", f"{can_a}-{can_b}"))

    src_ot = source.get("overtime_periods", "").strip()
    can_ot = canonical.get("overtime_periods", "").strip()
    if src_ot and can_ot and src_ot != can_ot:
        result.append(("overtime_periods", src_ot, can_ot))

    src_site, _ = source_site_to_canonical(source)
    can_site = canonical.get("site_type", "").strip()
    if src_site != "UNKNOWN" and can_site and can_site != "UNKNOWN" and src_site != can_site:
        result.append(("site_type", src_site, can_site))

    src_game_type = source.get("curated_game_type", "").strip()
    can_game_type = canonical.get("game_type", "").strip()
    if src_game_type and can_game_type and src_game_type != can_game_type:
        result.append(("game_type", src_game_type, can_game_type))

    src_round = source.get("curated_postseason_round", "").strip()
    can_round = canonical.get("postseason_round", "").strip()
    if src_round and can_round and src_round != can_round:
        result.append(("postseason_round", src_round, can_round))

    return result


def numeric_suffix(value: str, prefix: str) -> int:
    match = re.fullmatch(re.escape(prefix) + r"(\d+)", value or "")
    return int(match.group(1)) if match else 0


def next_canonical_number(rows: list[dict[str, str]]) -> int:
    return max((numeric_suffix(r.get("canonical_game_id", ""), "CBBG-") for r in rows), default=0) + 1


def next_discrepancy_number(rows: list[dict[str, str]]) -> int:
    return max((numeric_suffix(r.get("discrepancy_id", ""), "DISC-") for r in rows), default=0) + 1


def assertion_id_for(source: dict[str, str]) -> str:
    school = re.sub(r"[^A-Za-z0-9]+", "-", source.get("source_program_key", "").strip()).strip("-").upper()
    source_game = re.sub(r"[^A-Za-z0-9._-]+", "-", source.get("source_game_id", "").strip()).strip("-")
    return f"ASRT-{school}-{source_game}"


def build_assertion(
    source: dict[str, str],
    canonical_game_id: str,
    match_method: str,
) -> dict[str, str]:
    row = {field: source.get(field, "") for field in ASSERTION_FIELDS}
    row["assertion_id"] = assertion_id_for(source)
    row["canonical_game_id"] = canonical_game_id
    row["match_status"] = "MATCHED"
    row["match_method"] = match_method
    return row


def build_new_canonical(source: dict[str, str], game_id: str) -> dict[str, str]:
    school = source["source_program_key"].strip()
    opp = source["normalized_opponent_key"].strip()
    team_a, team_b = ordered_pair(school, opp)
    score_a, score_b = source_scores_in_canonical_orientation(source)
    site_type, home_key = source_site_to_canonical(source)

    return {
        "canonical_game_id": game_id,
        "season_label": source.get("season_label", ""),
        "game_date": source.get("game_date", ""),
        "date_precision": "EXACT" if source.get("game_date", "").strip() else "SEASON",
        "team_a_key": team_a,
        "team_b_key": team_b,
        "team_a_score": score_a,
        "team_b_score": score_b,
        "overtime_periods": source.get("overtime_periods", ""),
        "site_type": site_type,
        "designated_home_team_key": home_key,
        "venue_key": "",
        "site_city": source.get("city", ""),
        "site_state": source.get("state", ""),
        "game_type": source.get("curated_game_type", "") or "REGULAR_SEASON",
        "postseason_round": source.get("curated_postseason_round", ""),
        "administrative_status": "",
        "administrative_note": "",
        "canonical_status": "PROVISIONAL",
        "notes": "",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("school_key")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--repo", type=Path, default=None)
    args = parser.parse_args()

    repo_root = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    source_path = repo_root / "schools" / args.school_key / "source-games.csv"
    canonical_path = repo_root / "data" / "canonical" / "games.csv"
    assertions_path = repo_root / "data" / "evidence" / "game-assertions.csv"
    discrepancies_path = repo_root / "data" / "reconciliation" / "discrepancies.csv"

    try:
        sources = read_csv(source_path)
        canonical = read_csv(canonical_path)
        assertions = read_csv(assertions_path)
        discrepancies = read_csv(discrepancies_path)
    except FileNotFoundError as exc:
        print(f"FAIL: required file not found: {exc}")
        return 1

    index: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    canonical_by_id = {}
    for row in canonical:
        index[(row["team_a_key"], row["team_b_key"], row["season_label"])].append(row)
        canonical_by_id[row["canonical_game_id"]] = row

    existing_source_pairs = {
        (r.get("source_program_key", ""), r.get("source_game_id", ""))
        for r in assertions
    }

    # Deduplicate discrepancy records by game + field + source program.
    # The same underlying disagreement may be written in different human-readable
    # formats, so value formatting must not create a duplicate record.
    existing_discrepancy_keys = {
        (
            r.get("canonical_game_id", ""),
            r.get("field_name", ""),
            r.get("source_a_program_key", ""),
        )
        for r in discrepancies
    }

    planned = []
    identity_counts = Counter()
    next_game_num = next_canonical_number(canonical)

    for source in sources:
        school = source.get("source_program_key", "").strip()
        opp = source.get("normalized_opponent_key", "").strip()
        season = source.get("season_label", "").strip()

        if not school or not opp or not season or not source.get("source_game_id", "").strip():
            planned.append((source, REVIEW, "", "MISSING_REQUIRED_SOURCE_IDENTITY"))
            identity_counts[REVIEW] += 1
            continue

        team_a, team_b = ordered_pair(school, opp)
        candidates = index.get((team_a, team_b, season), [])
        status, game_id, method = identify_game(source, candidates)

        if status == NEW_GAME:
            game_id = f"CBBG-{next_game_num:07d}"
            next_game_num += 1

        planned.append((source, status, game_id, method))
        identity_counts[status] += 1

    print("College Basketball History — school ingestion")
    print(f"Repository: {repo_root}")
    print(f"School:     {args.school_key}")
    print(f"Mode:       {'APPLY' if args.apply else 'DRY RUN'}")
    print()
    print(f"Source rows:                {len(sources):,}")
    print(f"Existing-game matches:      {identity_counts[CONFIDENT]:,}")
    print(f"New canonical games:        {identity_counts[NEW_GAME]:,}")
    print(f"Identity review required:   {identity_counts[REVIEW]:,}")

    if identity_counts[REVIEW]:
        print()
        print("STOP: review-required identities exist. No files will be changed.")
        for source, status, game_id, method in [x for x in planned if x[1] == REVIEW][:20]:
            print(
                f"  - {source.get('source_game_id','')} | "
                f"{source.get('season_label','')} | "
                f"{source.get('game_date','') or '[no exact date]'} | "
                f"{source.get('normalized_opponent_name','')} | {method}"
            )
        return 0

    new_assertions = []
    new_canonical = []
    new_discrepancies = []
    next_disc_num = next_discrepancy_number(discrepancies)

    # Temporary lookup includes newly planned canonical games so assertions can link immediately.
    temp_canonical_by_id = dict(canonical_by_id)

    for source, status, game_id, method in planned:
        if status == NEW_GAME:
            row = build_new_canonical(source, game_id)
            new_canonical.append(row)
            temp_canonical_by_id[game_id] = row

        source_pair = (source.get("source_program_key", ""), source.get("source_game_id", ""))
        if source_pair not in existing_source_pairs:
            new_assertions.append(build_assertion(source, game_id, method))
            existing_source_pairs.add(source_pair)

        if status == CONFIDENT:
            can = temp_canonical_by_id[game_id]
            for field_name, source_value, canonical_value in discrepancy_candidates(source, can):
                discrepancy_key = (
                    game_id,
                    field_name,
                    source.get("source_program_key", ""),
                )
                if discrepancy_key in existing_discrepancy_keys:
                    continue

                new_discrepancies.append({
                    "discrepancy_id": f"DISC-{next_disc_num:06d}",
                    "canonical_game_id": game_id,
                    "field_name": field_name,
                    "source_a_program_key": source.get("source_program_key", ""),
                    "source_a_value": source_value,
                    "source_b_program_key": "",
                    "source_b_value": "",
                    "canonical_value": canonical_value,
                    "status": "UNDER_REVIEW",
                    "resolution_basis": "",
                    "notes": "Automatically detected during school ingestion; canonical value was not overwritten.",
                })
                next_disc_num += 1
                existing_discrepancy_keys.add(discrepancy_key)

    print(f"Assertions to add:           {len(new_assertions):,}")
    print(f"Discrepancies to add:        {len(new_discrepancies):,}")
    print()

    if not args.apply:
        print("DRY RUN COMPLETE: no files changed.")
        if not new_canonical and not new_assertions and not new_discrepancies:
            print("NO-OP: this school is already fully represented in the current global layers.")
        else:
            print("Re-run with --apply only after reviewing these counts.")
        return 0

    if not new_canonical and not new_assertions and not new_discrepancies:
        print("NO-OP: nothing to apply.")
        return 0

    write_csv(canonical_path, CANONICAL_FIELDS, canonical + new_canonical)
    write_csv(assertions_path, ASSERTION_FIELDS, assertions + new_assertions)
    write_csv(discrepancies_path, DISCREPANCY_FIELDS, discrepancies + new_discrepancies)

    print("Applied updates:")
    print(f"  canonical games:   +{len(new_canonical):,}")
    print(f"  source assertions: +{len(new_assertions):,}")
    print(f"  discrepancies:     +{len(new_discrepancies):,}")
    print()

    validator = repo_root / "tools" / "validate_data.py"
    if validator.exists():
        result = subprocess.run([sys.executable, str(validator), str(repo_root)])
        if result.returncode != 0:
            print()
            print("FAIL: files were written, but post-write validation failed.")
            return result.returncode
        print()
        print("PASS: ingestion applied and post-write validation succeeded.")
    else:
        print("WARNING: validate_data.py not found; post-write validation was skipped.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
