#!/usr/bin/env python3
"""Apply a sealed, zero-review legacy HOME chronology remediation plan.

This tool is intentionally conservative.  It delegates all semantic selection to
``plan_home_chronology_remediation.py`` and will apply a plan only when:

* the caller supplies the exact current plan SHA-256;
* every selected program has zero review rows;
* every candidate still maps to exactly one source row, one assertion row, and one
  canonical row; and
* every patched field is blank or already equal to the sealed proposed value.

The tool never changes H/A/N.  It fills only venue/location fields selected by the
planner, adds transparent canonical provenance, validates the repository, and rolls
all touched files back byte-for-byte if any postcondition fails.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path
from typing import Any

from location_safety import append_note
from plan_home_chronology_remediation import build_plan, clean


class HomeChronologyApplyError(RuntimeError):
    """A safe stop for a stale, review-bearing, or conflicting apply attempt."""


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _write_csv_preserving_format(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> None:
    original = path.read_bytes()
    has_bom = original.startswith(b"\xef\xbb\xbf")
    line_ending = "\r\n" if b"\r\n" in original else "\n"
    encoding = "utf-8-sig" if has_bom else "utf-8"
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator=line_ending)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    temporary.replace(path)


def _unique_by(rows: list[dict[str, str]], key_fn, *, label: str) -> dict[Any, dict[str, str]]:
    result: dict[Any, dict[str, str]] = {}
    duplicates: list[str] = []
    for row in rows:
        key = key_fn(row)
        if not key or (isinstance(key, tuple) and not all(key)):
            continue
        if key in result:
            duplicates.append(str(key))
        else:
            result[key] = row
    if duplicates:
        raise HomeChronologyApplyError(
            f"duplicate {label} key(s): " + ", ".join(duplicates[:12])
        )
    return result


def _patch_blanks(
    row: dict[str, str],
    patch: dict[str, str],
    *,
    label: str,
) -> int:
    changed = 0
    for field, value in patch.items():
        proposed = clean(value)
        if not proposed:
            raise HomeChronologyApplyError(f"{label}: proposed {field} is blank")
        if field not in row:
            raise HomeChronologyApplyError(f"{label}: missing field {field}")
        current = clean(row.get(field))
        if current and current != proposed:
            raise HomeChronologyApplyError(
                f"{label}: refusing to overwrite {field}={current!r} with {proposed!r}"
            )
        if not current:
            row[field] = proposed
            changed += 1
    return changed


def _marker(candidate: dict[str, Any]) -> str:
    venue = candidate.get("venue") or {}
    venue_key = clean(venue.get("venue_key"))
    return (
        "[HOME_CHRONOLOGY_BACKFILL "
        f"program={candidate['program']} "
        f"source_game_id={candidate['source_game_id']} "
        f"venue_key={venue_key}; canonical HOME independently established; "
        "venue/location supplied by documented school HOME chronology]"
    )


def apply_plan(
    repo: Path,
    programs: list[str],
    expected_plan_sha256: str,
    *,
    run_validation: bool = True,
) -> dict[str, Any]:
    repo = repo.resolve()
    selected = sorted(set(programs))
    if not selected:
        raise HomeChronologyApplyError("at least one --program is required")

    plan = build_plan(repo, selected)
    actual_hash = plan["sha256"]
    payload = plan["payload"]

    if not expected_plan_sha256:
        raise HomeChronologyApplyError("--apply requires --expected-plan-sha256")
    if actual_hash != expected_plan_sha256:
        raise HomeChronologyApplyError(
            "sealed HOME chronology plan hash mismatch; rerun the planner and review "
            f"the new plan (expected {expected_plan_sha256}, actual {actual_hash})"
        )
    if payload.get("review_count", 0):
        raise HomeChronologyApplyError(
            "selected programs still contain review rows; resolve them before applying "
            f"({payload['review_count']} review row(s))"
        )
    candidates = list(payload.get("candidates", []))
    if not candidates:
        return {
            "applied_games": 0,
            "plan_sha256": actual_hash,
            "source_fields_changed": 0,
            "assertion_fields_changed": 0,
            "canonical_fields_changed": 0,
        }

    canonical_path = repo / "data/canonical/games.csv"
    assertions_path = repo / "data/evidence/game-assertions.csv"
    source_paths = {
        program: repo / "schools" / program / "source-games.csv"
        for program in selected
    }

    touched_paths = [canonical_path, assertions_path, *source_paths.values()]
    originals = {path: path.read_bytes() for path in touched_paths}

    canonical_fields, canonical_rows = _read_csv(canonical_path)
    assertion_fields, assertion_rows = _read_csv(assertions_path)
    source_loaded = {
        program: _read_csv(path)
        for program, path in source_paths.items()
    }

    canonical_by_id = _unique_by(
        canonical_rows,
        lambda row: clean(row.get("canonical_game_id")),
        label="canonical_game_id",
    )
    assertion_by_key = _unique_by(
        assertion_rows,
        lambda row: (
            clean(row.get("canonical_game_id")),
            clean(row.get("source_program_key")),
            clean(row.get("source_game_id")),
        ),
        label="assertion mapping",
    )
    source_by_program = {
        program: _unique_by(
            rows,
            lambda row: clean(row.get("source_game_id")),
            label=f"{program} source_game_id",
        )
        for program, (_, rows) in source_loaded.items()
    }

    source_changed = 0
    assertion_changed = 0
    canonical_changed = 0

    try:
        seen_games: set[str] = set()
        for candidate in candidates:
            program = clean(candidate.get("program"))
            game_id = clean(candidate.get("canonical_game_id"))
            source_game_id = clean(candidate.get("source_game_id"))
            if program not in selected:
                raise HomeChronologyApplyError(
                    f"{game_id}: candidate program {program!r} escaped selection"
                )
            if game_id in seen_games:
                raise HomeChronologyApplyError(f"duplicate candidate game {game_id}")
            seen_games.add(game_id)

            canonical = canonical_by_id.get(game_id)
            source = source_by_program.get(program, {}).get(source_game_id)
            assertion = assertion_by_key.get((game_id, program, source_game_id))
            if canonical is None:
                raise HomeChronologyApplyError(f"{game_id}: canonical row disappeared")
            if source is None:
                raise HomeChronologyApplyError(
                    f"{game_id}: source row {program}/{source_game_id} disappeared"
                )
            if assertion is None:
                raise HomeChronologyApplyError(
                    f"{game_id}: assertion {program}/{source_game_id} disappeared"
                )

            site = clean(canonical.get("site_type"))
            team_a = clean(canonical.get("team_a_key"))
            team_b = clean(canonical.get("team_b_key"))
            home = team_a if site == "TEAM_A_HOME" else team_b if site == "TEAM_B_HOME" else ""
            if home != program:
                raise HomeChronologyApplyError(
                    f"{game_id}: canonical HOME classification changed after sealing"
                )
            if clean(source.get("curated_site_type")) != "SOURCE_PROGRAM_HOME":
                raise HomeChronologyApplyError(
                    f"{game_id}: source HOME classification changed after sealing"
                )

            patches = candidate.get("patches") or {}
            source_changed += _patch_blanks(
                source,
                dict(patches.get("source") or {}),
                label=f"{game_id} source",
            )
            assertion_changed += _patch_blanks(
                assertion,
                dict(patches.get("assertion") or {}),
                label=f"{game_id} assertion",
            )
            canonical_changed += _patch_blanks(
                canonical,
                dict(patches.get("canonical") or {}),
                label=f"{game_id} canonical",
            )

            if "notes" not in canonical:
                raise HomeChronologyApplyError(f"{game_id}: canonical notes field missing")
            before = canonical.get("notes", "")
            canonical["notes"] = append_note(before, _marker(candidate))
            if canonical["notes"] != before:
                canonical_changed += 1

        _write_csv_preserving_format(canonical_path, canonical_fields, canonical_rows)
        _write_csv_preserving_format(assertions_path, assertion_fields, assertion_rows)
        for program, path in source_paths.items():
            fields, rows = source_loaded[program]
            _write_csv_preserving_format(path, fields, rows)

        post = build_plan(repo, selected)["payload"]
        if post.get("candidate_count", 0) or post.get("review_count", 0):
            raise HomeChronologyApplyError(
                "postcondition failed: selected programs still contain planner debt "
                f"(candidates={post.get('candidate_count', 0)}, reviews={post.get('review_count', 0)})"
            )
        for program in selected:
            summary = post.get("summary_by_program", {}).get(program, {})
            if int(summary.get("hard_blocker", 0)) != 0:
                raise HomeChronologyApplyError(
                    f"postcondition failed: {program} still has "
                    f"{summary.get('hard_blocker', 0)} hard HOME blocker(s)"
                )

        if run_validation:
            completed = subprocess.run(
                [sys.executable, "tools/validate_data.py"],
                cwd=repo,
                text=True,
            )
            if completed.returncode != 0:
                raise HomeChronologyApplyError("repository validation failed after apply")

    except Exception:
        for path, content in originals.items():
            path.write_bytes(content)
        raise

    return {
        "applied_games": len(candidates),
        "plan_sha256": actual_hash,
        "source_fields_changed": source_changed,
        "assertion_fields_changed": assertion_changed,
        "canonical_fields_changed": canonical_changed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply a sealed zero-review HOME chronology remediation plan."
    )
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--program", action="append", default=[])
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-plan-sha256", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    try:
        plan = build_plan(repo, args.program)
        if not args.apply:
            payload = plan["payload"]
            print("College Basketball History — sealed HOME chronology apply preview")
            print(f"Git HEAD:       {payload.get('git_head', '')}")
            print(f"Programs:       {len(payload.get('programs', []))}")
            print(f"Candidates:     {payload.get('candidate_count', 0)}")
            print(f"Reviews:        {payload.get('review_count', 0)}")
            print(f"Plan SHA-256:   {plan['sha256']}")
            print("DRY RUN: no tracked basketball data changed.")
            return 0

        result = apply_plan(
            repo,
            args.program,
            args.expected_plan_sha256,
        )
        print(
            "PASS: HOME chronology remediation applied; "
            f"games={result['applied_games']} "
            f"source_fields={result['source_fields_changed']} "
            f"assertion_fields={result['assertion_fields_changed']} "
            f"canonical_fields={result['canonical_fields_changed']} "
            f"plan={result['plan_sha256']}"
        )
        return 0
    except (HomeChronologyApplyError, FileNotFoundError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
