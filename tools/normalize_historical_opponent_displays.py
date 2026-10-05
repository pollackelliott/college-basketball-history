#!/usr/bin/env python3
"""Normalize one staged school's historical opponent display names to project authority.

This is a representation-only Stage-2 helper. It never changes opponent keys or
source-game evidence. Existing integrated school packages provide the display-name
authority for historical/non-registry opponent keys.

Dry run:
    python tools/normalize_historical_opponent_displays.py <school_key>

Apply:
    python tools/normalize_historical_opponent_displays.py <school_key> --apply
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

import build_site_data


def read_csv_preserving(path: Path):
    raw = path.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    line_ending = "\r\n" if b"\r\n" in raw else "\n"
    encoding = "utf-8-sig" if has_bom else "utf-8"
    with path.open(encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader), encoding, line_ending


def write_csv_preserving(path: Path, fields, rows, encoding: str, line_ending: str):
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


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=repo,
        text=True,
    ).strip()


def project_program_keys(repo: Path) -> set[str]:
    return {
        row.get("program_key", "").strip()
        for row in build_site_data.read_csv(repo / "data/reference/programs.csv")
        if row.get("program_key", "").strip()
    }


def authority_names_by_key(
    repo: Path,
    target_school: str,
    *,
    program_keys: set[str] | None = None,
) -> dict[str, set[str]]:
    program_keys = program_keys if program_keys is not None else project_program_keys(repo)
    names: dict[str, set[str]] = defaultdict(set)
    for path in sorted((repo / "schools").glob("*/opponents.csv")):
        if path.parent.name == target_school:
            continue
        for row in build_site_data.read_csv(path):
            key = row.get("canonical_opponent_key", "").strip()
            name = row.get("canonical_opponent_name", "").strip()
            if key and name and key not in program_keys:
                names[key].add(name)
    return dict(names)


def build_normalization_plan(repo: Path, school_key: str) -> dict[str, Any]:
    path = repo / "schools" / school_key / "opponents.csv"
    if not path.is_file():
        raise FileNotFoundError(path)

    fields, rows, encoding, line_ending = read_csv_preserving(path)
    required = {"canonical_opponent_key", "canonical_opponent_name"}
    missing = sorted(required - set(fields))
    if missing:
        raise ValueError(
            "opponents.csv missing required column(s): " + ", ".join(missing)
        )

    program_keys = project_program_keys(repo)
    authority = authority_names_by_key(
        repo,
        school_key,
        program_keys=program_keys,
    )

    changes_by_key: dict[str, dict[str, Any]] = {}
    ambiguous: list[dict[str, Any]] = []

    target_names: dict[str, set[str]] = defaultdict(set)
    target_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        key = row.get("canonical_opponent_key", "").strip()
        name = row.get("canonical_opponent_name", "").strip()
        if key and name:
            target_names[key].add(name)
            target_counts[key] += 1

    for key in sorted(target_names):
        if key in program_keys:
            continue
        authority_names = set(authority.get(key, set()))
        if not authority_names:
            continue

        signatures = {
            build_site_data.normalized_name_signature(name)
            for name in authority_names
            if build_site_data.normalized_name_signature(name)
        }
        if len(signatures) != 1:
            ambiguous.append(
                {
                    "canonical_opponent_key": key,
                    "target_names": sorted(target_names[key]),
                    "authority_names": sorted(authority_names),
                    "authority_signatures": sorted(signatures),
                }
            )
            continue

        authority_signature = next(iter(signatures))
        preferred = build_site_data.preferred_display_name(authority_names)
        mismatched = sorted(
            name
            for name in target_names[key]
            if build_site_data.normalized_name_signature(name)
            != authority_signature
        )
        if mismatched:
            changes_by_key[key] = {
                "canonical_opponent_key": key,
                "from_names": mismatched,
                "to_name": preferred,
                "authority_names": sorted(authority_names),
                "authority_signature": authority_signature,
                "target_row_count": target_counts[key],
            }

    changed_rows = 0
    output_rows = []
    for row in rows:
        updated = dict(row)
        key = row.get("canonical_opponent_key", "").strip()
        item = changes_by_key.get(key)
        if item:
            current = row.get("canonical_opponent_name", "").strip()
            if build_site_data.normalized_name_signature(current) != item["authority_signature"]:
                updated["canonical_opponent_name"] = item["to_name"]
                changed_rows += 1
        output_rows.append(updated)

    return {
        "schema_version": 1,
        "school_key": school_key,
        "path": path,
        "fields": fields,
        "rows": output_rows,
        "encoding": encoding,
        "line_ending": line_ending,
        "status": "BLOCKED" if ambiguous else "PASS",
        "change_key_count": len(changes_by_key),
        "change_row_count": changed_rows,
        "changes": [changes_by_key[key] for key in sorted(changes_by_key)],
        "ambiguous_key_count": len(ambiguous),
        "ambiguous": ambiguous,
    }


def public_report(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": plan["schema_version"],
        "school_key": plan["school_key"],
        "status": plan["status"],
        "change_key_count": plan["change_key_count"],
        "change_row_count": plan["change_row_count"],
        "changes": plan["changes"],
        "ambiguous_key_count": plan["ambiguous_key_count"],
        "ambiguous": plan["ambiguous"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("school_key")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json-output", type=Path, default=None)
    args = parser.parse_args()

    repo = (
        args.repo.resolve()
        if args.repo
        else Path(__file__).resolve().parents[1]
    )

    branch = git(repo, "branch", "--show-current")
    if branch in {"", "main", "master"}:
        print("FAIL: historical opponent display normalization must run on an onboarding branch.")
        return 1

    status = git(repo, "status", "--porcelain", "--untracked-files=all")
    if status:
        print("FAIL: worktree must be clean before historical opponent display normalization.")
        print(status)
        return 1

    try:
        plan = build_normalization_plan(repo, args.school_key)
    except (FileNotFoundError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1

    report = public_report(plan)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print("College Basketball History — historical opponent display normalization")
    print(f"School:             {args.school_key}")
    print(f"Status:             {plan['status']}")
    print(f"Keys to normalize:  {plan['change_key_count']}")
    print(f"Rows to normalize:  {plan['change_row_count']}")
    print(f"Ambiguous keys:     {plan['ambiguous_key_count']}")

    if plan["ambiguous"]:
        for item in plan["ambiguous"]:
            print(
                "AMBIGUOUS: "
                f"{item['canonical_opponent_key']} | "
                f"target={item['target_names']} | authority={item['authority_names']}"
            )
        print("STOP: existing project authority is not mechanically unique; no files changed.")
        return 1

    if not plan["change_row_count"]:
        print("NO-OP: target package already matches historical display authority.")
        return 0

    if not args.apply:
        print("DRY RUN COMPLETE: no files changed.")
        print("Next: rerun with --apply.")
        return 0

    write_csv_preserving(
        plan["path"],
        plan["fields"],
        plan["rows"],
        plan["encoding"],
        plan["line_ending"],
    )
    print("PASS: opponents.csv display representation normalized; keys and source-games.csv unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
