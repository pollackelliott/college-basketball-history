#!/usr/bin/env python3
"""Read-only remote execution for one Stage 2 reconciliation diagnostic.

This module authenticates an exact prior Stage 2 proposal-rehearsal checkpoint,
restores only the ignored proposal inputs required by the permanent diagnostic,
invokes current-main onboarding_hardening.py against an exact onboarding worktree,
and proves that tracked basketball state remains unchanged.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from remote_implementation_control import sha256_bytes, sha256_file
from remote_implementation_io import ROOT, Stop, git_show_bytes, run
from remote_implementation_stage2_census import (
    RUNTIME_ROOT,
    restore_integration_freeze,
    tracked_worktree_state,
)
from remote_implementation_stage2_proposal import verify_stage2_proposal_authority

TRACE_NAME = "last-rehearsal-reconciliation-trace.json"
SOURCE_PLAN = "plan.json"
SOURCE_REVIEW = "review.csv"


def _bound_bytes(
    control_commit: str,
    path: str,
    expected_sha256: str,
    *,
    source_repo: Path = ROOT,
    mismatch_code: str,
) -> bytes:
    data = git_show_bytes(control_commit, path, cwd=source_repo)
    if sha256_bytes(data) != expected_sha256:
        raise Stop(mismatch_code)
    return data


def verify_stage2_diagnostic_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path = ROOT,
) -> dict[str, Any]:
    """Authenticate one exact prior blocked proposal checkpoint."""

    ref = request["stage2_proposal_checkpoint"]
    checkpoint_bytes = _bound_bytes(
        control_commit,
        ref["path"],
        ref["sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_DIAGNOSTIC_PROPOSAL_CHECKPOINT_HASH_MISMATCH",
    )
    try:
        manifest = json.loads(checkpoint_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_DIAGNOSTIC_PROPOSAL_CHECKPOINT_JSON_INVALID") from exc

    if (
        manifest.get("kind")
        != "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_CHECKPOINT"
    ):
        raise Stop("STAGE2_DIAGNOSTIC_PROPOSAL_CHECKPOINT_KIND_MISMATCH")
    if manifest.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_DIAGNOSTIC_PROPOSAL_CHECKPOINT_SCHOOL_MISMATCH")
    if manifest.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_DIAGNOSTIC_PROPOSAL_CHECKPOINT_BRANCH_MISMATCH")
    if manifest.get("target_sha") != request["target_sha"]:
        raise Stop("STAGE2_DIAGNOSTIC_PROPOSAL_CHECKPOINT_TARGET_MISMATCH")
    if manifest.get("stage2_status") != "BLOCKED":
        raise Stop("STAGE2_DIAGNOSTIC_PROPOSAL_CHECKPOINT_NOT_BLOCKED")
    for field, code in (
        ("integration_freeze_sha256", "FREEZE"),
        ("semantic_snapshot_sha256", "SEMANTIC"),
        ("decision_universe_sha256", "DECISION_UNIVERSE"),
        ("recommendation_map_sha256", "MAP"),
    ):
        if manifest.get(field) != request[field]:
            raise Stop(f"STAGE2_DIAGNOSTIC_PROPOSAL_{code}_MISMATCH")

    directory = Path(ref["path"]).parent
    proposal_request_path = (directory / "request.json").as_posix()
    proposal_request_bytes = git_show_bytes(
        control_commit, proposal_request_path, cwd=source_repo
    )
    if sha256_bytes(proposal_request_bytes) != manifest.get("request_sha256"):
        raise Stop("STAGE2_DIAGNOSTIC_SOURCE_REQUEST_HASH_MISMATCH")
    try:
        proposal_request = json.loads(proposal_request_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_DIAGNOSTIC_SOURCE_REQUEST_JSON_INVALID") from exc
    if proposal_request.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_DIAGNOSTIC_SOURCE_REQUEST_ID_MISMATCH")

    proposal_authority = verify_stage2_proposal_authority(
        proposal_request,
        control_commit,
        source_repo=source_repo,
    )

    map_path = str(manifest.get("recommendation_map_checkpoint_path") or "")
    if not map_path:
        raise Stop("STAGE2_DIAGNOSTIC_MAP_PATH_MISSING")
    map_bytes = _bound_bytes(
        control_commit,
        map_path,
        request["recommendation_map_sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_DIAGNOSTIC_MAP_HASH_MISMATCH",
    )

    artifacts = manifest.get("artifact_sha256") or {}
    plan_sha = str(artifacts.get(SOURCE_PLAN) or "")
    review_sha = str(artifacts.get(SOURCE_REVIEW) or "")
    if not plan_sha or not review_sha:
        raise Stop("STAGE2_DIAGNOSTIC_SOURCE_ARTIFACT_HASH_MISSING")
    plan_bytes = _bound_bytes(
        control_commit,
        (directory / SOURCE_PLAN).as_posix(),
        plan_sha,
        source_repo=source_repo,
        mismatch_code="STAGE2_DIAGNOSTIC_PLAN_HASH_MISMATCH",
    )
    review_bytes = _bound_bytes(
        control_commit,
        (directory / SOURCE_REVIEW).as_posix(),
        review_sha,
        source_repo=source_repo,
        mismatch_code="STAGE2_DIAGNOSTIC_REVIEW_HASH_MISMATCH",
    )

    return {
        "proposal_manifest": manifest,
        "proposal_checkpoint_bytes": checkpoint_bytes,
        "proposal_request": proposal_request,
        "proposal_authority": proposal_authority,
        "freeze_bytes": proposal_authority["freeze_bytes"],
        "map_bytes": map_bytes,
        "plan_bytes": plan_bytes,
        "review_bytes": review_bytes,
        "target_tree_sha": manifest.get("target_tree_sha"),
    }


def run_stage2_reconciliation_diagnostic_tool(
    repo: Path,
    school_key: str,
    *,
    freeze_bytes: bytes,
    map_bytes: bytes,
    plan_bytes: bytes,
    review_bytes: bytes,
    canonical_game_id: str,
    diag: Path,
    tool_repo: Path | None = None,
) -> dict[str, Any]:
    """Run the permanent diagnostic against one exact disposable target worktree."""

    restore_integration_freeze(repo, school_key, freeze_bytes)
    output = repo / ".onboarding" / school_key
    output.mkdir(parents=True, exist_ok=True)
    plan_path = output / SOURCE_PLAN
    review_path = output / SOURCE_REVIEW
    plan_path.write_bytes(plan_bytes)
    review_path.write_bytes(review_bytes)
    map_path = output / "remote-diagnostic-recommendation-map.json"
    map_path.write_bytes(map_bytes)

    before = tracked_worktree_state(repo)
    if before["status"]:
        raise Stop("STAGE2_DIAGNOSTIC_TRACKED_STATE_DIRTY_BEFORE_RUN")

    runtime_repo = (tool_repo or RUNTIME_ROOT).resolve()
    hardening_tool = runtime_repo / "tools/onboarding_hardening.py"
    trace_tool = runtime_repo / "tools/reconciliation_trace.py"
    if not hardening_tool.is_file():
        raise Stop("STAGE2_DIAGNOSTIC_RUNTIME_HARDENING_TOOL_MISSING")
    if not trace_tool.is_file():
        raise Stop("STAGE2_DIAGNOSTIC_RUNTIME_TRACE_TOOL_MISSING")
    runtime_tool_sha256 = {
        "tools/onboarding_hardening.py": sha256_file(hardening_tool),
        "tools/reconciliation_trace.py": sha256_file(trace_tool),
    }

    cmd = [
        sys.executable,
        str(hardening_tool),
        "diagnose-reconciliation",
        school_key,
        "--repo",
        str(repo),
        "--plan-file",
        str(plan_path),
        "--review-file",
        str(review_path),
        "--map",
        str(map_path),
        "--canonical-game-id",
        canonical_game_id,
    ]
    cp = run(cmd, cwd=runtime_repo, check=False)
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "stage2-reconciliation-diagnostic.log").write_text(
        cp.stdout, encoding="utf-8"
    )

    after = tracked_worktree_state(repo)
    if (
        before["head_sha"] != after["head_sha"]
        or before["tree_sha"] != after["tree_sha"]
        or after["status"]
    ):
        raise Stop(
            "STAGE2_DIAGNOSTIC_TRACKED_MUTATION_DETECTED "
            "before_head=%s after_head=%s before_tree=%s after_tree=%s status=%r"
            % (
                before["head_sha"],
                after["head_sha"],
                before["tree_sha"],
                after["tree_sha"],
                after["status"],
            )
        )
    if cp.returncode != 0:
        raise Stop("STAGE2_DIAGNOSTIC_PERMANENT_COMMAND_FAILED")

    trace_path = output / TRACE_NAME
    if not trace_path.is_file():
        raise Stop("STAGE2_DIAGNOSTIC_TRACE_MISSING")
    trace_bytes = trace_path.read_bytes()
    try:
        trace = json.loads(trace_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_DIAGNOSTIC_TRACE_JSON_INVALID") from exc
    if trace.get("kind") != "IMPLEMENTATION_RECONCILIATION_TRACE":
        raise Stop("STAGE2_DIAGNOSTIC_TRACE_KIND_MISMATCH")
    if trace.get("school_key") != school_key:
        raise Stop("STAGE2_DIAGNOSTIC_TRACE_SCHOOL_MISMATCH")
    if trace.get("canonical_game_id") != canonical_game_id:
        raise Stop("STAGE2_DIAGNOSTIC_TRACE_GAME_MISMATCH")
    if trace.get("diagnostic_status") != "PASS":
        raise Stop("STAGE2_DIAGNOSTIC_TRACE_STATUS_NOT_PASS")
    if trace.get("real_tracked_repository_unchanged") is not True:
        raise Stop("STAGE2_DIAGNOSTIC_TRACE_MUTATION_PROOF_FAILED")

    return {
        "command": [
            "python",
            "tools/onboarding_hardening.py",
            "diagnose-reconciliation",
            school_key,
            "--map",
            "<MAP>",
            "--canonical-game-id",
            canonical_game_id,
        ],
        "exit_code": cp.returncode,
        "canonical_game_id": canonical_game_id,
        "trace": trace,
        "trace_bytes": trace_bytes,
        "trace_sha256": sha256_bytes(trace_bytes),
        "runtime_tool_sha256": runtime_tool_sha256,
        "tracked_mutation_proof": {
            "before_head_sha": before["head_sha"],
            "after_head_sha": after["head_sha"],
            "before_tree_sha": before["tree_sha"],
            "after_tree_sha": after["tree_sha"],
            "before_status": before["status"],
            "after_status": after["status"],
            "tracked_stage2_mutation": "NONE",
        },
    }
