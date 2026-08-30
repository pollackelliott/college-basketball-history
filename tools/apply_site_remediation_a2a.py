#!/usr/bin/env python3
"""Seal and apply the owner-approved Wave A2a H/A/N propagation batch.

Owner ruling for A2a:
- canonical site_type is currently UNKNOWN;
- exactly one participant source assertion supplies the uncontested site type;
- the reciprocal participant assertion is UNKNOWN, not contradictory;
- the raw site candidate is an explicit H/A/N token/text form OR the literal
  schedule locator ``at``;
- opaque raw codes ``3``, ``4``, and ``vs.`` remain held for research.

This pass changes only semantic H/A/N state (site_type plus the corresponding
``designated_home_team_key``) and appends deterministic provenance.  It does NOT
fill venue or geography.  Those lower-risk enrichments can be reconsidered only
after H/A/N is established.

Default mode is dry-run. ``--apply`` requires the exact SHA-256 printed by a
prior dry-run against the same repository state.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from location_safety import append_note
from site_remediation_a2_census import _raw_indicator_state
from site_remediation_a2_review import build_a2_review
from site_remediation_audit import read_csv


PLAN_VERSION = 1
BATCH = "A2A_DIRECT_SITE_ASSERTION_PROPAGATION"
EXPECTED_APPROVED_COUNT = 201
EXPECTED_HELD_COUNT = 5
EXPECTED_HELD_RAW_COUNTS = {"3": 2, "4": 2, "vs.": 1}
EXPLICIT_RAW_STATES = {"EXPLICIT_RAW_HAN_TOKEN", "EXPLICIT_RAW_HAN_TEXT"}
PROVENANCE_PREFIX = "[SITE_ASSERTION_PROPAGATION "


class A2AApplyError(RuntimeError):
    """A safe stop for a stale, ambiguous, or out-of-scope A2a plan."""


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


def _parts(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split("|") if item.strip()]


def _single(value: str, *, label: str, game_id: str) -> str:
    parts = _parts(value)
    if len(parts) != 1:
        raise A2AApplyError(
            f"{game_id}: A2a requires exactly one {label}; found {parts!r}"
        )
    return parts[0]


def _approved_direct_evidence(row: dict[str, str]) -> bool:
    raw_state = _raw_indicator_state(row)
    if raw_state in EXPLICIT_RAW_STATES:
        return True
    raw_candidate = _single(
        row.get("source_site_candidates", ""),
        label="raw source-site candidate",
        game_id=row.get("canonical_game_id", ""),
    )
    return raw_candidate.casefold() == "at"


def _provenance_marker(
    source_program: str,
    source_game_id: str,
    raw_candidate: str,
    proposed_site_type: str,
) -> str:
    safe_raw = " ".join(raw_candidate.split()).replace(";", ",")
    return (
        f"{PROVENANCE_PREFIX}"
        f"source={source_program}/{source_game_id};"
        f"raw_site_candidate={safe_raw};"
        f"site_type={proposed_site_type}]"
    )


def _plan_item(row: dict[str, str]) -> dict[str, Any]:
    game_id = row.get("canonical_game_id", "").strip()
    if row.get("current_site_type", "").strip() != "UNKNOWN":
        raise A2AApplyError(f"{game_id}: A2a current site_type must be UNKNOWN")
    proposed = row.get("proposed_site_type", "").strip()
    if proposed not in {"TEAM_A_HOME", "TEAM_B_HOME", "NEUTRAL"}:
        raise A2AApplyError(f"{game_id}: invalid proposed site_type {proposed!r}")
    if row.get("supporting_assertion_count", "").strip() != "1":
        raise A2AApplyError(f"{game_id}: A2a requires exactly one supporting assertion")
    if row.get("other_participant_evidence_state", "").strip() != "OTHER_PARTICIPANT_UNKNOWN_ASSERTION":
        raise A2AApplyError(
            f"{game_id}: reciprocal participant is not an UNKNOWN assertion"
        )
    if row.get("site_discrepancy_statuses", "").strip():
        raise A2AApplyError(f"{game_id}: site_type reconciliation unexpectedly exists")

    source_program = _single(
        row.get("supporting_programs", ""), label="supporting program", game_id=game_id
    )
    source_game_id = _single(
        row.get("supporting_source_game_ids", ""),
        label="supporting source_game_id",
        game_id=game_id,
    )
    raw_candidate = _single(
        row.get("source_site_candidates", ""),
        label="raw source-site candidate",
        game_id=game_id,
    )
    source_form = _single(
        row.get("source_site_forms", ""), label="curated source-site form", game_id=game_id
    )
    if source_form not in {"SOURCE_PROGRAM_HOME", "OPPONENT_HOME", "NEUTRAL"}:
        raise A2AApplyError(f"{game_id}: invalid curated source-site form {source_form!r}")

    proposed_home = row.get("proposed_home_team_key", "").strip()
    if proposed in {"TEAM_A_HOME", "TEAM_B_HOME"} and not proposed_home:
        raise A2AApplyError(f"{game_id}: home site lacks proposed_home_team_key")
    if proposed == "NEUTRAL" and proposed_home:
        raise A2AApplyError(f"{game_id}: neutral site unexpectedly proposes a home team")

    return {
        "canonical_game_id": game_id,
        "season_label": row.get("season_label", "").strip(),
        "team_a_key": row.get("team_a_key", "").strip(),
        "team_b_key": row.get("team_b_key", "").strip(),
        "current_site_type": "UNKNOWN",
        "proposed_site_type": proposed,
        "proposed_home_team_key": proposed_home,
        "supporting_program": source_program,
        "supporting_source_game_id": source_game_id,
        "source_site_form": source_form,
        "raw_site_candidate": raw_candidate,
        "raw_indicator_state": _raw_indicator_state(row),
        "evidence_profile": row.get("evidence_profile", "").strip(),
        "provenance_marker": _provenance_marker(
            source_program, source_game_id, raw_candidate, proposed
        ),
    }


def build_a2a_plan(repo: Path) -> dict[str, Any]:
    review = build_a2_review(repo)
    if review["summary"].get("status") != "PASS":
        raise A2AApplyError("A2 owner-review dossier must PASS before A2a planning")

    approved: list[dict[str, Any]] = []
    held: list[dict[str, str]] = []
    for row in review["rows"]:
        item = _plan_item(row)
        if _approved_direct_evidence(row):
            approved.append(item)
        else:
            held.append(
                {
                    "canonical_game_id": item["canonical_game_id"],
                    "season_label": item["season_label"],
                    "team_a_key": item["team_a_key"],
                    "team_b_key": item["team_b_key"],
                    "proposed_site_type": item["proposed_site_type"],
                    "supporting_program": item["supporting_program"],
                    "supporting_source_game_id": item["supporting_source_game_id"],
                    "source_site_form": item["source_site_form"],
                    "raw_site_candidate": item["raw_site_candidate"],
                    "evidence_profile": item["evidence_profile"],
                }
            )

    approved.sort(key=lambda item: item["canonical_game_id"])
    held.sort(key=lambda item: item["canonical_game_id"])
    held_raw_counts = Counter(item["raw_site_candidate"] for item in held)

    if len(approved) != EXPECTED_APPROVED_COUNT:
        raise A2AApplyError(
            f"owner-approved A2a universe changed: expected {EXPECTED_APPROVED_COUNT} "
            f"approved games, found {len(approved)}"
        )
    if len(held) != EXPECTED_HELD_COUNT:
        raise A2AApplyError(
            f"owner-held A2b universe changed: expected {EXPECTED_HELD_COUNT} held games, "
            f"found {len(held)}"
        )
    if dict(sorted(held_raw_counts.items())) != EXPECTED_HELD_RAW_COUNTS:
        raise A2AApplyError(
            "owner-held raw-code signature changed: expected "
            f"{EXPECTED_HELD_RAW_COUNTS}, found {dict(sorted(held_raw_counts.items()))}"
        )

    guarded_files = [
        "data/canonical/games.csv",
        "data/evidence/game-assertions.csv",
        "data/reconciliation/discrepancies.csv",
        "tools/site_remediation_audit.py",
        "tools/site_remediation_tier_report.py",
        "tools/site_remediation_a2_review.py",
        "tools/site_remediation_a2_census.py",
        "tools/apply_site_remediation_a2a.py",
    ]
    inputs = {
        relative: _sha256_file(repo / relative)
        for relative in guarded_files
        if (repo / relative).is_file()
    }
    proposed_counts = Counter(item["proposed_site_type"] for item in approved)
    raw_state_counts = Counter(item["raw_indicator_state"] for item in approved)

    payload = {
        "plan_version": PLAN_VERSION,
        "batch": BATCH,
        "owner_rule": (
            "Propagate UNKNOWN canonical H/A/N only from one uncontested participant "
            "assertion whose raw site evidence is explicit H/A/N text/token or literal 'at'; "
            "hold opaque 3/4/vs. codes; do not propagate venue/geography in A2a."
        ),
        "git_head": _git_head(repo),
        "inputs": inputs,
        "approved_count": len(approved),
        "held_count": len(held),
        "approved_site_counts": dict(sorted(proposed_counts.items())),
        "approved_raw_indicator_counts": dict(sorted(raw_state_counts.items())),
        "held_raw_counts": dict(sorted(held_raw_counts.items())),
        "approved": approved,
        "held": held,
    }
    return {"sha256": _plan_hash(payload), "payload": payload}


def write_plan(plan: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _write_csv_preserving_format(
    path: Path, fieldnames: list[str], rows: list[dict[str, str]]
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


def apply_a2a_plan(
    repo: Path,
    expected_sha256: str,
    *,
    run_validation: bool = True,
) -> dict[str, Any]:
    plan = build_a2a_plan(repo)
    actual_hash = plan["sha256"]
    if not expected_sha256:
        raise A2AApplyError("--apply requires --expected-plan-sha256")
    if expected_sha256 != actual_hash:
        raise A2AApplyError(
            "sealed A2a plan hash mismatch; rerun dry-run before applying "
            f"(expected {expected_sha256}, actual {actual_hash})"
        )

    approved = plan["payload"]["approved"]
    held = plan["payload"]["held"]
    if len(approved) != EXPECTED_APPROVED_COUNT or len(held) != EXPECTED_HELD_COUNT:
        raise A2AApplyError("A2a owner boundary changed after sealing")

    canonical_path = repo / "data/canonical/games.csv"
    original_bytes = canonical_path.read_bytes()
    fields, rows = read_csv(canonical_path)
    by_id = {
        row.get("canonical_game_id", "").strip(): row
        for row in rows
        if row.get("canonical_game_id", "").strip()
    }

    try:
        for item in approved:
            game_id = item["canonical_game_id"]
            row = by_id.get(game_id)
            if row is None:
                raise A2AApplyError(f"{game_id}: canonical row disappeared")
            if row.get("site_type", "").strip() != "UNKNOWN":
                raise A2AApplyError(
                    f"{game_id}: refusing to overwrite known site_type "
                    f"{row.get('site_type','')!r}"
                )
            if row.get("designated_home_team_key", "").strip():
                raise A2AApplyError(
                    f"{game_id}: UNKNOWN canonical site unexpectedly has designated home team"
                )

            row["site_type"] = item["proposed_site_type"]
            if item["proposed_site_type"] in {"TEAM_A_HOME", "TEAM_B_HOME"}:
                row["designated_home_team_key"] = item["proposed_home_team_key"]
            row["notes"] = append_note(row.get("notes", ""), item["provenance_marker"])

        _write_csv_preserving_format(canonical_path, fields, rows)

        post = build_a2_review(repo)
        if post["summary"].get("status") != "PASS":
            raise A2AApplyError("A2 post-apply review dossier failed")
        remaining_ids = {row["canonical_game_id"] for row in post["rows"]}
        selected_ids = {item["canonical_game_id"] for item in approved}
        held_ids = {item["canonical_game_id"] for item in held}
        unexpected_selected = sorted(selected_ids & remaining_ids)
        if unexpected_selected:
            raise A2AApplyError(
                "A2a postcondition failed; applied IDs remain UNKNOWN candidates: "
                + ", ".join(unexpected_selected[:10])
            )
        if remaining_ids != held_ids:
            raise A2AApplyError(
                "A2a postcondition failed; remaining UNKNOWN universe is not exactly "
                f"the five owner-held rows (remaining={len(remaining_ids)}, held={len(held_ids)})"
            )

        if run_validation:
            completed = subprocess.run(
                [sys.executable, "tools/validate_data.py"], cwd=repo, text=True
            )
            if completed.returncode != 0:
                raise A2AApplyError("repository validation failed after A2a apply")
    except Exception:
        canonical_path.write_bytes(original_bytes)
        raise

    return {
        "applied_games": len(approved),
        "held_games": len(held),
        "plan_sha256": actual_hash,
    }


def print_plan(plan: dict[str, Any]) -> None:
    payload = plan["payload"]
    print("College Basketball History — Wave A2a sealed H/A/N plan")
    print(f"Batch:                     {payload['batch']}")
    print(f"Git HEAD:                  {payload['git_head']}")
    print(f"Approved games:            {payload['approved_count']}")
    print(f"Held games:                {payload['held_count']}")
    print(f"Approved site counts:      {json.dumps(payload['approved_site_counts'], sort_keys=True)}")
    print(f"Approved raw-state counts: {json.dumps(payload['approved_raw_indicator_counts'], sort_keys=True)}")
    print(f"Held raw-code counts:      {json.dumps(payload['held_raw_counts'], sort_keys=True)}")
    print(f"Plan SHA-256:              {plan['sha256']}")
    print("Held rows:")
    for item in payload["held"]:
        print(
            f"  {item['canonical_game_id']} {item['season_label']} "
            f"{item['team_a_key']} vs {item['team_b_key']} "
            f"raw={item['raw_site_candidate']!r} -> {item['proposed_site_type']}"
        )
    print("DRY RUN: no tracked basketball data changed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seal/apply owner-approved Wave A2a H/A/N repairs.")
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
        else repo / ".onboarding" / "site-remediation-wave-a2" / "a2a-plan.json"
    )
    try:
        if args.apply:
            result = apply_a2a_plan(repo, args.expected_plan_sha256)
            print(
                f"PASS: applied A2a H/A/N to {result['applied_games']} canonical game(s); "
                f"held {result['held_games']}; sealed plan {result['plan_sha256']}"
            )
            return 0
        plan = build_a2a_plan(repo)
        write_plan(plan, output)
        print_plan(plan)
        print(f"Plan artifact:             {output}")
        return 0
    except (A2AApplyError, FileNotFoundError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
