#!/usr/bin/env python3
"""Read-only remote execution for Owner Gate 1 review filling.

This module authenticates an exact OWNER_GATE_1_READY proposal checkpoint plus
its independent fresh verification, restores only ignored onboarding inputs in
an exact target worktree, invokes the permanent fill-review command, and proves
that tracked basketball state remains unchanged. It does not seal or apply.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
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


def _decision_id_set_sha256(review_bytes: bytes) -> str:
    text = review_bytes.decode("utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    decision_ids = [str(row.get("decision_id") or "").strip() for row in rows]
    if not decision_ids or any(not value for value in decision_ids):
        raise Stop("STAGE2_GATE1_FILL_DECISION_ID_SET_INVALID")
    if len(decision_ids) != len(set(decision_ids)):
        raise Stop("STAGE2_GATE1_FILL_DECISION_ID_SET_DUPLICATE")
    payload = ("\n".join(sorted(decision_ids)) + "\n").encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _filled_review_summary(review_bytes: bytes) -> dict[str, Any]:
    text = review_bytes.decode("utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    if not rows:
        raise Stop("STAGE2_GATE1_FILL_REVIEW_EMPTY")
    counts: Counter[str] = Counter()
    for row in rows:
        decision_id = str(row.get("decision_id") or "").strip()
        decision = str(row.get("decision") or "").strip()
        basis = str(row.get("resolution_basis") or "").strip()
        if not decision_id:
            raise Stop("STAGE2_GATE1_FILL_REVIEW_DECISION_ID_BLANK")
        if not decision:
            raise Stop("STAGE2_GATE1_FILL_REVIEW_DECISION_BLANK:%s" % decision_id)
        if not basis:
            raise Stop("STAGE2_GATE1_FILL_REVIEW_BASIS_BLANK:%s" % decision_id)
        counts[decision] += 1
    return {
        "decision_count": len(rows),
        "action_counts": dict(sorted(counts.items())),
        "decision_id_set_sha256": _decision_id_set_sha256(review_bytes),
    }


def verify_stage2_gate1_fill_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path = ROOT,
) -> dict[str, Any]:
    """Authenticate exact rehearsed proposal + fresh verification + owner binding."""

    checkpoint_ref = request["stage2_proposal_checkpoint"]
    checkpoint_bytes = _bound_bytes(
        control_commit,
        checkpoint_ref["path"],
        checkpoint_ref["sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_GATE1_FILL_PROPOSAL_CHECKPOINT_HASH_MISMATCH",
    )
    try:
        manifest = json.loads(checkpoint_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_CHECKPOINT_JSON_INVALID") from exc

    if (
        manifest.get("kind")
        != "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_CHECKPOINT"
    ):
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_CHECKPOINT_KIND_MISMATCH")
    if manifest.get("stage2_status") != "OWNER_GATE_1_READY":
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_NOT_READY")
    if manifest.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_SCHOOL_MISMATCH")
    if manifest.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_BRANCH_MISMATCH")
    if manifest.get("target_sha") != request["target_sha"]:
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_TARGET_MISMATCH")

    for field, code in (
        ("integration_freeze_sha256", "FREEZE"),
        ("semantic_snapshot_sha256", "SEMANTIC"),
        ("decision_universe_sha256", "DECISION_UNIVERSE"),
        ("recommendation_map_sha256", "MAP"),
        ("approved_plan_hash_preview", "APPROVED_PLAN_PREVIEW"),
    ):
        if manifest.get(field) != request[field]:
            raise Stop("STAGE2_GATE1_FILL_PROPOSAL_%s_MISMATCH" % code)

    verification_ref = request["stage2_proposal_verification"]
    verification_bytes = _bound_bytes(
        control_commit,
        verification_ref["path"],
        verification_ref["sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_GATE1_FILL_PROPOSAL_VERIFICATION_HASH_MISMATCH",
    )
    try:
        verification = json.loads(verification_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_VERIFICATION_JSON_INVALID") from exc
    if (
        verification.get("kind")
        != "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_VERIFICATION"
    ):
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_VERIFICATION_KIND_MISMATCH")
    if verification.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_VERIFICATION_REQUEST_MISMATCH")
    if verification.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_VERIFICATION_SCHOOL_MISMATCH")
    if verification.get("target_sha") != request["target_sha"]:
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_VERIFICATION_TARGET_MISMATCH")
    if verification.get("stage2_status") != "OWNER_GATE_1_READY":
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_VERIFICATION_NOT_READY")
    if verification.get("remote_stage2_proposal_equivalence") != "PASS":
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_EQUIVALENCE_NOT_PASS")
    if verification.get("tracked_stage2_mutation") != "NONE":
        raise Stop("STAGE2_GATE1_FILL_PROPOSAL_TRACKED_MUTATION")
    for field, code in (
        ("integration_freeze_sha256", "FREEZE"),
        ("semantic_snapshot_sha256", "SEMANTIC"),
        ("decision_universe_sha256", "DECISION_UNIVERSE"),
        ("recommendation_map_sha256", "MAP"),
        ("approved_plan_hash_preview", "APPROVED_PLAN_PREVIEW"),
    ):
        if verification.get(field) != request[field]:
            raise Stop("STAGE2_GATE1_FILL_VERIFICATION_%s_MISMATCH" % code)

    directory = Path(checkpoint_ref["path"]).parent
    proposal_request_path = (directory / "request.json").as_posix()
    proposal_request_bytes = git_show_bytes(
        control_commit,
        proposal_request_path,
        cwd=source_repo,
    )
    if sha256_bytes(proposal_request_bytes) != manifest.get("request_sha256"):
        raise Stop("STAGE2_GATE1_FILL_SOURCE_REQUEST_HASH_MISMATCH")
    try:
        proposal_request = json.loads(proposal_request_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_GATE1_FILL_SOURCE_REQUEST_JSON_INVALID") from exc
    if proposal_request.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_GATE1_FILL_SOURCE_REQUEST_ID_MISMATCH")
    proposal_authority = verify_stage2_proposal_authority(
        proposal_request,
        control_commit,
        source_repo=source_repo,
    )

    map_path = str(manifest.get("recommendation_map_checkpoint_path") or "")
    if not map_path:
        raise Stop("STAGE2_GATE1_FILL_MAP_PATH_MISSING")
    map_bytes = _bound_bytes(
        control_commit,
        map_path,
        request["recommendation_map_sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_GATE1_FILL_MAP_HASH_MISMATCH",
    )

    artifacts = manifest.get("artifact_sha256") or {}
    plan_sha = str(artifacts.get(SOURCE_PLAN) or "")
    review_sha = str(artifacts.get(SOURCE_REVIEW) or "")
    if not plan_sha or not review_sha:
        raise Stop("STAGE2_GATE1_FILL_SOURCE_ARTIFACT_HASH_MISSING")
    plan_bytes = _bound_bytes(
        control_commit,
        (directory / SOURCE_PLAN).as_posix(),
        plan_sha,
        source_repo=source_repo,
        mismatch_code="STAGE2_GATE1_FILL_PLAN_HASH_MISMATCH",
    )
    review_bytes = _bound_bytes(
        control_commit,
        (directory / SOURCE_REVIEW).as_posix(),
        review_sha,
        source_repo=source_repo,
        mismatch_code="STAGE2_GATE1_FILL_REVIEW_HASH_MISMATCH",
    )

    approval = request["owner_gate_1_approval"]
    approval_sha256 = sha256_bytes(
        (json.dumps(approval, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    )

    return {
        "proposal_manifest": manifest,
        "proposal_checkpoint_bytes": checkpoint_bytes,
        "proposal_verification": verification,
        "proposal_verification_bytes": verification_bytes,
        "proposal_request": proposal_request,
        "proposal_authority": proposal_authority,
        "freeze_bytes": proposal_authority["freeze_bytes"],
        "map_bytes": map_bytes,
        "plan_bytes": plan_bytes,
        "review_bytes": review_bytes,
        "target_tree_sha": manifest.get("target_tree_sha"),
        "expected_action_counts": manifest.get("action_counts") or {},
        "expected_decision_count": int(
            (manifest.get("preflight") or {}).get("decision_count", 0)
        ),
        "owner_gate_1_approval_sha256": approval_sha256,
    }


def run_stage2_gate1_fill_tool(
    repo: Path,
    school_key: str,
    *,
    freeze_bytes: bytes,
    map_bytes: bytes,
    plan_bytes: bytes,
    review_bytes: bytes,
    expected_action_counts: dict[str, int],
    expected_decision_count: int,
    diag: Path,
    tool_repo: Path | None = None,
) -> dict[str, Any]:
    """Fill one exact owner-approved review without mutating tracked repository state."""

    restore_integration_freeze(repo, school_key, freeze_bytes)
    output = repo / ".onboarding" / school_key
    output.mkdir(parents=True, exist_ok=True)
    plan_path = output / SOURCE_PLAN
    review_path = output / SOURCE_REVIEW
    map_path = output / "remote-gate1-fill-recommendation-map.json"
    plan_path.write_bytes(plan_bytes)
    review_path.write_bytes(review_bytes)
    map_path.write_bytes(map_bytes)

    before = tracked_worktree_state(repo)
    if before["status"]:
        raise Stop("STAGE2_GATE1_FILL_TRACKED_STATE_DIRTY_BEFORE_RUN")

    runtime_repo = (tool_repo or RUNTIME_ROOT).resolve()
    hardening_tool = runtime_repo / "tools/onboarding_hardening.py"
    if not hardening_tool.is_file():
        raise Stop("STAGE2_GATE1_FILL_RUNTIME_HARDENING_TOOL_MISSING")
    runtime_tool_sha256 = sha256_file(hardening_tool)

    cmd = [
        sys.executable,
        str(hardening_tool),
        "fill-review",
        school_key,
        "--repo",
        str(repo),
        "--review-file",
        str(review_path),
        "--map",
        str(map_path),
    ]
    cp = run(cmd, cwd=runtime_repo, check=False)
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "stage2-gate1-fill.log").write_text(cp.stdout, encoding="utf-8")

    after = tracked_worktree_state(repo)
    if (
        before["head_sha"] != after["head_sha"]
        or before["tree_sha"] != after["tree_sha"]
        or after["status"]
    ):
        raise Stop(
            "STAGE2_GATE1_FILL_TRACKED_MUTATION_DETECTED "
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
        raise Stop("STAGE2_GATE1_FILL_PERMANENT_COMMAND_FAILED")

    filled_review_bytes = review_path.read_bytes()
    summary = _filled_review_summary(filled_review_bytes)
    if summary["decision_count"] != expected_decision_count:
        raise Stop(
            "STAGE2_GATE1_FILL_DECISION_COUNT_MISMATCH expected=%s actual=%s"
            % (expected_decision_count, summary["decision_count"])
        )
    if summary["action_counts"] != expected_action_counts:
        raise Stop(
            "STAGE2_GATE1_FILL_ACTION_COUNTS_MISMATCH expected=%r actual=%r"
            % (expected_action_counts, summary["action_counts"])
        )

    return {
        "command": [
            "python",
            "tools/onboarding_hardening.py",
            "fill-review",
            school_key,
            "--map",
            "<MAP>",
        ],
        "exit_code": cp.returncode,
        "filled_review_bytes": filled_review_bytes,
        "filled_review_sha256": sha256_bytes(filled_review_bytes),
        "source_review_sha256": sha256_bytes(review_bytes),
        "plan_sha256": sha256_bytes(plan_bytes),
        "recommendation_map_sha256": sha256_bytes(map_bytes),
        "decision_count": summary["decision_count"],
        "action_counts": summary["action_counts"],
        "decision_id_set_sha256": summary["decision_id_set_sha256"],
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
