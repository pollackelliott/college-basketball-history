#!/usr/bin/env python3
"""Seal and apply the lowest-risk Wave A1 site-completeness repairs.

A1 is intentionally narrow: canonical H/A/N is already established and the
current tier report proposes only blank venue/location enrichment.  This tool
never changes site_type.  Default mode is dry-run; ``--apply`` requires the
exact SHA-256 printed by a prior dry-run against the same repository state.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from location_safety import append_note, registry_fallback_marker
from site_remediation_audit import read_csv
from site_remediation_tier_report import build_tier_report


TIER = "A1_EXISTING_SITE_PROPAGATION"
ALLOWED_CHANGE_FIELDS = {"venue", "site_city", "site_state"}
PLAN_VERSION = 1


class A1ApplyError(RuntimeError):
    """A safe stop for a stale, ambiguous, or out-of-scope A1 plan."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_head(repo: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "[not-a-git-worktree]"


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _plan_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _split_pipe(value: str) -> list[str]:
    return [item for item in (value or "").split("|") if item]


def _source_pair(row: dict[str, str]) -> tuple[str, str]:
    programs = _split_pipe(row.get("supporting_programs", ""))
    source_ids = _split_pipe(row.get("supporting_source_game_ids", ""))
    if len(programs) != 1 or len(source_ids) != 1:
        raise A1ApplyError(
            f"{row.get('canonical_game_id','')}: A1 apply requires exactly one "
            "supporting program/source row for deterministic provenance"
        )
    return programs[0], source_ids[0]


def _patch_for_candidate(row: dict[str, str]) -> dict[str, str]:
    game_id = row.get("canonical_game_id", "").strip()
    change_fields = set(_split_pipe(row.get("change_fields", "")))
    if not change_fields:
        raise A1ApplyError(f"{game_id}: A1 candidate has no change fields")
    if not change_fields <= ALLOWED_CHANGE_FIELDS:
        raise A1ApplyError(
            f"{game_id}: A1 candidate attempts out-of-scope fields "
            + ", ".join(sorted(change_fields - ALLOWED_CHANGE_FIELDS))
        )
    if row.get("proposed_site_type", "").strip():
        raise A1ApplyError(f"{game_id}: A1 must never propose site_type")

    patch: dict[str, str] = {}
    provenance_fields: list[str] = []

    if "venue" in change_fields:
        venue_id = row.get("proposed_venue_id", "").strip()
        venue_key = row.get("proposed_venue_key", "").strip()
        if not venue_id or not venue_key:
            raise A1ApplyError(f"{game_id}: venue proposal is incomplete")
        patch["venue_id"] = venue_id
        patch["venue_key"] = venue_key
        provenance_fields.extend(("venue_id", "venue_key"))

    if "site_city" in change_fields:
        city = row.get("proposed_city", "").strip()
        if not city:
            raise A1ApplyError(f"{game_id}: city proposal is blank")
        patch["site_city"] = city
        provenance_fields.append("site_city")

    if "site_state" in change_fields:
        state = row.get("proposed_state", "").strip()
        if not state:
            raise A1ApplyError(f"{game_id}: state proposal is blank")
        patch["site_state"] = state
        provenance_fields.append("site_state")

    program, source_id = _source_pair(row)
    venue_key = patch.get("venue_key", row.get("current_venue_key", "").strip())
    if not venue_key:
        raise A1ApplyError(f"{game_id}: provenance marker requires a venue_key")
    marker = registry_fallback_marker(
        program,
        source_id,
        venue_key,
        row.get("current_site_type", "").strip(),
        provenance_fields,
    )
    patch["_provenance_marker"] = marker
    return patch


def build_a1_plan(repo: Path) -> dict[str, Any]:
    tier_report = build_tier_report(repo)
    selected = [
        row for row in tier_report["rows"] if row.get("tier", "") == TIER
    ]

    plan_rows: list[dict[str, Any]] = []
    for row in selected:
        patch = _patch_for_candidate(row)
        plan_rows.append(
            {
                "canonical_game_id": row["canonical_game_id"],
                "season_label": row["season_label"],
                "team_a_key": row["team_a_key"],
                "team_b_key": row["team_b_key"],
                "current_site_type": row["current_site_type"],
                "supporting_programs": row["supporting_programs"],
                "supporting_source_game_ids": row["supporting_source_game_ids"],
                "patch": patch,
            }
        )

    plan_rows.sort(key=lambda item: item["canonical_game_id"])
    guarded_files = [
        "data/canonical/games.csv",
        "data/evidence/game-assertions.csv",
        "data/reconciliation/discrepancies.csv",
        "data/reference/venues.csv",
        "data/reference/venue-names.csv",
        "tools/site_remediation_audit.py",
        "tools/site_remediation_tier_report.py",
        "tools/apply_site_remediation_a1.py",
    ]
    inputs = {
        relative: _sha256_file(repo / relative)
        for relative in guarded_files
        if (repo / relative).is_file()
    }
    payload = {
        "plan_version": PLAN_VERSION,
        "tier": TIER,
        "git_head": _git_head(repo),
        "inputs": inputs,
        "candidate_count": len(plan_rows),
        "candidates": plan_rows,
    }
    return {"sha256": _plan_hash(payload), "payload": payload}


def write_plan(plan: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(plan, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def apply_a1_plan(
    repo: Path,
    expected_sha256: str,
    *,
    run_validation: bool = True,
) -> dict[str, Any]:
    plan = build_a1_plan(repo)
    actual_hash = plan["sha256"]
    if not expected_sha256:
        raise A1ApplyError("--apply requires --expected-plan-sha256")
    if expected_sha256 != actual_hash:
        raise A1ApplyError(
            "sealed A1 plan hash mismatch; rerun dry-run and review the new plan "
            f"(expected {expected_sha256}, actual {actual_hash})"
        )

    candidates = plan["payload"]["candidates"]
    if not candidates:
        return {"applied_games": 0, "plan_sha256": actual_hash}

    canonical_path = repo / "data/canonical/games.csv"
    original_bytes = canonical_path.read_bytes()
    fields, rows = read_csv(canonical_path)
    by_id = {
        row.get("canonical_game_id", "").strip(): row
        for row in rows
        if row.get("canonical_game_id", "").strip()
    }

    try:
        for item in candidates:
            game_id = item["canonical_game_id"]
            row = by_id.get(game_id)
            if row is None:
                raise A1ApplyError(f"{game_id}: canonical row disappeared")
            if row.get("site_type", "").strip() != item["current_site_type"]:
                raise A1ApplyError(f"{game_id}: canonical site_type changed after sealing")

            patch = dict(item["patch"])
            marker = patch.pop("_provenance_marker")
            for field, value in patch.items():
                current = row.get(field, "").strip()
                if current and current != value:
                    raise A1ApplyError(
                        f"{game_id}: refusing to overwrite nonblank {field}={current!r}"
                    )
                row[field] = value
            row["notes"] = append_note(row.get("notes", ""), marker)

        _write_csv_preserving_format(canonical_path, fields, rows)

        # The exact A1 game IDs must disappear from the candidate universe after
        # application.  A2 is intentionally untouched and may remain.
        post = build_tier_report(repo)
        remaining_a1 = {
            row["canonical_game_id"]
            for row in post["rows"]
            if row.get("tier", "") == TIER
        }
        selected_ids = {item["canonical_game_id"] for item in candidates}
        still_present = sorted(selected_ids & remaining_a1)
        if still_present:
            raise A1ApplyError(
                "A1 postcondition failed; candidates remain after apply: "
                + ", ".join(still_present)
            )

        if run_validation:
            completed = subprocess.run(
                [sys.executable, "tools/validate_data.py"],
                cwd=repo,
                text=True,
            )
            if completed.returncode != 0:
                raise A1ApplyError("repository validation failed after A1 apply")
    except Exception:
        canonical_path.write_bytes(original_bytes)
        raise

    return {"applied_games": len(candidates), "plan_sha256": actual_hash}


def print_plan(plan: dict[str, Any]) -> None:
    payload = plan["payload"]
    print("College Basketball History — Wave A1 sealed propagation plan")
    print(f"Tier:                 {payload['tier']}")
    print(f"Git HEAD:             {payload['git_head']}")
    print(f"Candidate games:      {payload['candidate_count']}")
    print(f"Plan SHA-256:         {plan['sha256']}")
    for item in payload["candidates"]:
        patch = dict(item["patch"])
        patch.pop("_provenance_marker", None)
        print(
            f"  {item['canonical_game_id']} {item['season_label']} "
            f"{item['team_a_key']} vs {item['team_b_key']} -> "
            + json.dumps(patch, sort_keys=True)
        )
    print("DRY RUN: no tracked basketball data changed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seal/apply lowest-risk A1 site repairs.")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-plan-sha256", default="")
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    output = (
        args.output.resolve()
        if args.output
        else repo / ".onboarding" / "site-remediation-wave-a" / "a1-plan.json"
    )
    try:
        if args.apply:
            result = apply_a1_plan(repo, args.expected_plan_sha256)
            print(
                f"PASS: applied A1 repairs to {result['applied_games']} canonical game(s); "
                f"sealed plan {result['plan_sha256']}"
            )
            return 0
        plan = build_a1_plan(repo)
        write_plan(plan, output)
        print_plan(plan)
        print(f"Plan artifact:        {output}")
        return 0
    except (A1ApplyError, FileNotFoundError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
