#!/usr/bin/env python3
"""
Add result_winner_team_key to canonical games and backfill every existing row.

Default mode is DRY RUN. Nothing is written unless --apply is supplied.

Usage:
    python tools/migrate_result_winner.py
    python tools/migrate_result_winner.py --apply
    python tools/migrate_result_winner.py /path/to/repository
    python tools/migrate_result_winner.py /path/to/repository --apply
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


RESULT_FIELD = "result_winner_team_key"

# Exactly two existing canonical games have both scores unknown.
# Their outcomes are nevertheless known from official source evidence.
SCORELESS_KNOWN_RESULTS = {
    "CBBG-0010307": {
        "participants": {"minnesota", "northwestern"},
        "winner": "northwestern",
        "administrative_status": "FORFEIT",
        "administrative_note": (
            "Minnesota forfeited; game was not played and no score exists."
        ),
    },
    "CBBG-0014540": {
        "participants": {"kentucky", "transylvania"},
        "winner": "kentucky",
        "administrative_status": None,
        "administrative_note": None,
    },
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return (reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    tmp.replace(path)


def derive_scored_winner(row: dict[str, str]) -> str:
    score_a = int(row["team_a_score"].strip())
    score_b = int(row["team_b_score"].strip())
    if score_a > score_b:
        return row["team_a_key"].strip()
    if score_b > score_a:
        return row["team_b_key"].strip()
    return ""


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
        help="Write the migration to data/canonical/games.csv.",
    )
    args = parser.parse_args()

    repo_root = (
        Path(args.repository_root).resolve()
        if args.repository_root
        else Path(__file__).resolve().parents[1]
    )
    canonical_path = repo_root / "data" / "canonical" / "games.csv"

    try:
        fieldnames, rows = read_csv(canonical_path)
    except FileNotFoundError as exc:
        print(f"FAIL: required file not found: {exc}")
        return 1

    if not rows:
        print("FAIL: canonical games file is empty.")
        return 1

    already_has_field = RESULT_FIELD in fieldnames
    if not already_has_field:
        try:
            insert_at = fieldnames.index("team_b_score") + 1
        except ValueError:
            print("FAIL: team_b_score column not found; refusing migration.")
            return 1
        fieldnames = fieldnames[:insert_at] + [RESULT_FIELD] + fieldnames[insert_at:]

    counts = Counter()
    errors: list[str] = []
    seen_scoreless: set[str] = set()
    changed_rows = 0

    for row in rows:
        game_id = row.get("canonical_game_id", "")
        team_a = row.get("team_a_key", "").strip()
        team_b = row.get("team_b_key", "").strip()
        score_a = row.get("team_a_score", "").strip()
        score_b = row.get("team_b_score", "").strip()

        before = (
            row.get(RESULT_FIELD, ""),
            row.get("administrative_status", ""),
            row.get("administrative_note", ""),
        )

        if bool(score_a) != bool(score_b):
            errors.append(
                f"{game_id}: one score is blank and the other is populated."
            )
            continue

        if score_a and score_b:
            try:
                winner = derive_scored_winner(row)
            except ValueError:
                errors.append(
                    f"{game_id}: non-integer score {score_a!r}-{score_b!r}."
                )
                continue

            row[RESULT_FIELD] = winner
            if winner:
                counts["scored_decisions"] += 1
            else:
                counts["ties"] += 1
        else:
            special = SCORELESS_KNOWN_RESULTS.get(game_id)
            if special is None:
                errors.append(
                    f"{game_id}: scoreless canonical game has no explicit migration rule."
                )
                continue

            participants = {team_a, team_b}
            if participants != special["participants"]:
                errors.append(
                    f"{game_id}: expected participants "
                    f"{sorted(special['participants'])}, got {sorted(participants)}."
                )
                continue

            row[RESULT_FIELD] = special["winner"]
            seen_scoreless.add(game_id)
            counts["scoreless_known_results"] += 1

            if special["administrative_status"] is not None:
                existing_status = row.get("administrative_status", "").strip()
                if existing_status not in {"", special["administrative_status"]}:
                    errors.append(
                        f"{game_id}: refusing to replace administrative_status "
                        f"{existing_status!r}."
                    )
                    continue
                row["administrative_status"] = special["administrative_status"]

            if special["administrative_note"] is not None:
                existing_note = row.get("administrative_note", "").strip()
                if existing_note not in {"", special["administrative_note"]}:
                    errors.append(
                        f"{game_id}: refusing to replace administrative_note "
                        f"{existing_note!r}."
                    )
                    continue
                row["administrative_note"] = special["administrative_note"]

        after = (
            row.get(RESULT_FIELD, ""),
            row.get("administrative_status", ""),
            row.get("administrative_note", ""),
        )
        if before != after:
            changed_rows += 1

    missing_specials = sorted(set(SCORELESS_KNOWN_RESULTS) - seen_scoreless)
    if missing_specials:
        errors.append(
            "Expected scoreless canonical games were not found: "
            + ", ".join(missing_specials)
        )

    print("College Basketball History — canonical result-winner migration")
    print(f"Repository:               {repo_root}")
    print(f"Mode:                     {'APPLY' if args.apply else 'DRY RUN'}")
    print()
    print(f"Canonical games:          {len(rows):,}")
    print(f"Scored decisions:         {counts['scored_decisions']:,}")
    print(f"Ties:                     {counts['ties']:,}")
    print(f"Scoreless known results:  {counts['scoreless_known_results']:,}")
    print(f"Rows that would change:   {changed_rows:,}")
    print(f"Column already present:   {'Yes' if already_has_field else 'No'}")
    print()

    for game_id in sorted(SCORELESS_KNOWN_RESULTS):
        row = next((r for r in rows if r.get("canonical_game_id") == game_id), None)
        if row:
            print(
                f"- {game_id}: "
                f"{row.get('team_a_key')} {row.get('team_a_score') or '[blank]'} - "
                f"{row.get('team_b_score') or '[blank]'} {row.get('team_b_key')} | "
                f"winner={row.get(RESULT_FIELD) or '[blank]'} | "
                f"admin={row.get('administrative_status') or '[blank]'}"
            )

    if errors:
        print()
        print(f"FAIL ({len(errors)} errors):")
        for error in errors[:50]:
            print(f"  - {error}")
        return 1

    if not args.apply:
        print()
        print("DRY RUN COMPLETE: no files changed.")
        return 0

    write_csv(canonical_path, fieldnames, rows)
    print()
    print(
        f"PASS: migrated {len(rows):,} canonical games and wrote "
        f"{RESULT_FIELD}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
