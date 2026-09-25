#!/usr/bin/env python3
"""Normalize retired source administrative-status representations safely."""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path

from administrative_status import (
    administrative_status_errors,
    normalize_legacy_vacated_season_context_row,
)


def read_csv_preserving(path: Path):
    raw = path.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    line_ending = "\r\n" if b"\r\n" in raw else "\n"
    encoding = "utf-8-sig" if has_bom else "utf-8"
    with path.open(encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader), encoding, line_ending


def write_csv_preserving(path, fields, rows, encoding, line_ending):
    with path.open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            lineterminator=line_ending,
        )
        writer.writeheader()
        writer.writerows(
            {field: row.get(field, "") for field in fields}
            for row in rows
        )


def normalize_rows(rows):
    output = []
    legacy_rows = 0
    vacated_wins = 0
    context_only_nonwins = 0

    for row in rows:
        normalized, changed = normalize_legacy_vacated_season_context_row(row)
        if changed:
            legacy_rows += 1
            if normalized.get("administrative_status") == "VACATED_WIN":
                vacated_wins += 1
            else:
                context_only_nonwins += 1
        output.append(normalized)

    errors = []
    for index, row in enumerate(output, start=2):
        label = row.get("source_game_id", "").strip() or f"line {index}"
        errors.extend(administrative_status_errors(row, label))
    if errors:
        raise ValueError("; ".join(errors[:20]))

    return output, {
        "legacy_rows": legacy_rows,
        "vacated_wins": vacated_wins,
        "context_only_nonwins": context_only_nonwins,
    }


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=repo,
        text=True,
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("school_key")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    repo = (
        args.repo.resolve()
        if args.repo
        else Path(__file__).resolve().parents[1]
    )

    branch = git(repo, "branch", "--show-current")
    if branch in {"", "main", "master"}:
        print("FAIL: legacy administrative normalization must run on an onboarding branch.")
        return 1

    status = git(repo, "status", "--porcelain", "--untracked-files=all")
    if status:
        print("FAIL: worktree must be clean before administrative normalization.")
        print(status)
        return 1

    path = repo / "schools" / args.school_key / "source-games.csv"
    if not path.is_file():
        print(f"FAIL: source-games.csv not found: {path}")
        return 1

    fields, rows, encoding, line_ending = read_csv_preserving(path)
    try:
        normalized, counts = normalize_rows(rows)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1

    print("College Basketball History — legacy administrative-status normalization")
    print(f"School:                 {args.school_key}")
    print(f"Legacy context rows:    {counts['legacy_rows']}")
    print(f"VACATED_WIN rows:       {counts['vacated_wins']}")
    print(f"Context-only non-wins:  {counts['context_only_nonwins']}")

    if not counts["legacy_rows"]:
        print("NO-OP: no legacy VACATED_SEASON_CONTEXT rows remain.")
        return 0

    if not args.apply:
        print("DRY RUN COMPLETE: no files changed.")
        print("Next: rerun with --apply.")
        return 0

    write_csv_preserving(
        path,
        fields,
        normalized,
        encoding,
        line_ending,
    )
    print("PASS: source administrative statuses normalized; on-court results unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
