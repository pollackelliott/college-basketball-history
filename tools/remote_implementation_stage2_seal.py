#!/usr/bin/env python3
"""Remote cryptographic Owner Gate 1 sealing without sealed apply.

The operation authenticates one fresh-verified READY_TO_SEAL checkpoint, replays
the permanent pre-seal rehearsal against current protected-main runtime, invokes
the permanent onboard_school.py --approve seal path, and proves tracked
basketball state remains unchanged. It never applies the sealed plan.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

from onboarding_plan import approve_plan, verify_approved_plan
from remote_implementation_control import sha256_bytes, sha256_file
from remote_implementation_io import ROOT, Stop, git_show_bytes, run
from remote_implementation_stage2_census import (
    RUNTIME_ROOT,
    restore_integration_freeze,
    tracked_worktree_state,
)
from remote_implementation_stage2_preseal import verify_stage2_preseal_authority

APPROVED_BY = "project-owner"
SEALED_DIR_NAME = "remote-gate1-seal"
APPROVED_PLAN_NAME = "approved-plan.json"
APPROVED_REVIEW_NAME = "approved-review.md"
_APPROVED_HASH_RE = re.compile(r"Approved plan:\s*([0-9a-f]{64})")


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


def verify_stage2_gate1_seal_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path = ROOT,
) -> dict[str, Any]:
    """Authenticate exact fresh-verified pre-seal authority and its approval chain."""

    checkpoint_ref = request["stage2_preseal_checkpoint"]
    checkpoint_bytes = _bound_bytes(
        control_commit,
        checkpoint_ref["path"],
        checkpoint_ref["sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_GATE1_SEAL_PRESEAL_CHECKPOINT_HASH_MISMATCH",
    )
    try:
        manifest = json.loads(checkpoint_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_CHECKPOINT_JSON_INVALID") from exc

    if (
        manifest.get("kind")
        != "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT"
    ):
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_CHECKPOINT_KIND_MISMATCH")
    if manifest.get("preseal_status") != "READY_TO_SEAL":
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_NOT_READY")
    if manifest.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_SCHOOL_MISMATCH")
    if manifest.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_BRANCH_MISMATCH")
    if manifest.get("target_sha") != request["target_sha"]:
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_TARGET_MISMATCH")

    for field, code in (
        ("integration_freeze_sha256", "FREEZE"),
        ("semantic_snapshot_sha256", "SEMANTIC"),
        ("decision_universe_sha256", "DECISION_UNIVERSE"),
        ("recommendation_map_sha256", "MAP"),
        ("approved_plan_hash_preview", "APPROVED_PLAN_PREVIEW"),
        ("filled_review_sha256", "FILLED_REVIEW"),
        ("decision_id_set_sha256", "DECISION_ID_SET"),
        ("owner_gate_1_approval_sha256", "OWNER_APPROVAL"),
        ("equivalence_sha256", "PRESEAL_EQUIVALENCE"),
    ):
        if manifest.get(field) != request[field]:
            raise Stop("STAGE2_GATE1_SEAL_PRESEAL_%s_MISMATCH" % code)

    verification_ref = request["stage2_preseal_verification"]
    verification_bytes = _bound_bytes(
        control_commit,
        verification_ref["path"],
        verification_ref["sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_GATE1_SEAL_PRESEAL_VERIFICATION_HASH_MISMATCH",
    )
    try:
        verification = json.loads(verification_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_VERIFICATION_JSON_INVALID") from exc
    if (
        verification.get("kind")
        != "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_VERIFICATION"
    ):
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_VERIFICATION_KIND_MISMATCH")
    if verification.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_VERIFICATION_REQUEST_MISMATCH")
    if verification.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_VERIFICATION_SCHOOL_MISMATCH")
    if verification.get("target_sha") != request["target_sha"]:
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_VERIFICATION_TARGET_MISMATCH")
    if verification.get("preseal_status") != "READY_TO_SEAL":
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_VERIFICATION_NOT_READY")
    if verification.get("remote_stage2_preseal_equivalence") != "PASS":
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_EQUIVALENCE_NOT_PASS")
    if verification.get("tracked_stage2_mutation") != "NONE":
        raise Stop("STAGE2_GATE1_SEAL_PRESEAL_TRACKED_MUTATION")
    for field, code in (
        ("integration_freeze_sha256", "FREEZE"),
        ("semantic_snapshot_sha256", "SEMANTIC"),
        ("decision_universe_sha256", "DECISION_UNIVERSE"),
        ("recommendation_map_sha256", "MAP"),
        ("approved_plan_hash_preview", "APPROVED_PLAN_PREVIEW"),
        ("filled_review_sha256", "FILLED_REVIEW"),
        ("decision_id_set_sha256", "DECISION_ID_SET"),
        ("owner_gate_1_approval_sha256", "OWNER_APPROVAL"),
        ("equivalence_sha256", "PRESEAL_EQUIVALENCE"),
    ):
        if verification.get(field) != request[field]:
            raise Stop("STAGE2_GATE1_SEAL_VERIFICATION_%s_MISMATCH" % code)

    directory = Path(checkpoint_ref["path"]).parent
    preseal_request_path = (directory / "request.json").as_posix()
    preseal_request_bytes = git_show_bytes(
        control_commit,
        preseal_request_path,
        cwd=source_repo,
    )
    if sha256_bytes(preseal_request_bytes) != manifest.get("request_sha256"):
        raise Stop("STAGE2_GATE1_SEAL_SOURCE_PRESEAL_REQUEST_HASH_MISMATCH")
    try:
        preseal_request = json.loads(preseal_request_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_GATE1_SEAL_SOURCE_PRESEAL_REQUEST_JSON_INVALID") from exc
    if preseal_request.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_GATE1_SEAL_SOURCE_PRESEAL_REQUEST_ID_MISMATCH")

    preseal_authority = verify_stage2_preseal_authority(
        preseal_request,
        control_commit,
        source_repo=source_repo,
    )
    if (
        preseal_authority.get("owner_gate_1_approval_sha256")
        != request["owner_gate_1_approval_sha256"]
    ):
        raise Stop("STAGE2_GATE1_SEAL_OWNER_APPROVAL_CHAIN_MISMATCH")

    return {
        "preseal_manifest": manifest,
        "preseal_checkpoint_bytes": checkpoint_bytes,
        "preseal_verification": verification,
        "preseal_verification_bytes": verification_bytes,
        "preseal_request": preseal_request,
        "preseal_authority": preseal_authority,
        "freeze_bytes": preseal_authority["freeze_bytes"],
        "plan_bytes": preseal_authority["plan_bytes"],
        "filled_review_bytes": preseal_authority["filled_review_bytes"],
        "target_tree_sha": manifest.get("target_tree_sha"),
        "expected_changed_path_count": manifest.get("changed_path_count"),
        "expected_site_gate_normalized_sha256": manifest.get(
            "site_gate_normalized_sha256"
        ),
    }


def verify_sealed_plan_bytes(
    repo: Path,
    *,
    plan_bytes: bytes,
    filled_review_bytes: bytes,
    approved_plan_bytes: bytes,
) -> dict[str, Any]:
    """Independently reconstruct and verify one exact sealed approved plan."""

    try:
        approved = json.loads(approved_plan_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_GATE1_SEAL_APPROVED_PLAN_JSON_INVALID") from exc
    if not isinstance(approved, dict):
        raise Stop("STAGE2_GATE1_SEAL_APPROVED_PLAN_NOT_OBJECT")

    approval = approved.get("approval")
    if not isinstance(approval, dict):
        raise Stop("STAGE2_GATE1_SEAL_APPROVAL_METADATA_MISSING")
    if approval.get("approved_by") != APPROVED_BY:
        raise Stop("STAGE2_GATE1_SEAL_APPROVED_BY_MISMATCH")
    approved_at = str(approval.get("approved_at") or "").strip()
    if not approved_at:
        raise Stop("STAGE2_GATE1_SEAL_APPROVED_AT_MISSING")
    try:
        parsed = dt.datetime.fromisoformat(approved_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise Stop("STAGE2_GATE1_SEAL_APPROVED_AT_INVALID") from exc
    if parsed.tzinfo is None:
        raise Stop("STAGE2_GATE1_SEAL_APPROVED_AT_NOT_OFFSET_AWARE")

    approved_hash = str(approved.get("approved_plan_hash") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", approved_hash):
        raise Stop("STAGE2_GATE1_SEAL_APPROVED_PLAN_HASH_INVALID")
    try:
        verify_approved_plan(repo, approved, approved_hash)
    except Exception as exc:
        raise Stop("STAGE2_GATE1_SEAL_APPROVED_PLAN_VERIFY_FAILED") from exc

    with tempfile.TemporaryDirectory(prefix="gate1-seal-verify-") as temporary:
        temp = Path(temporary)
        plan_path = temp / "plan.json"
        review_path = temp / "filled-review.csv"
        plan_path.write_bytes(plan_bytes)
        review_path.write_bytes(filled_review_bytes)
        try:
            expected, expected_hash = approve_plan(
                repo,
                plan_path,
                review_path,
                APPROVED_BY,
                approved_at=approved_at,
            )
        except Exception as exc:
            raise Stop("STAGE2_GATE1_SEAL_RECONSTRUCTION_FAILED") from exc

    if expected_hash != approved_hash or expected != approved:
        raise Stop("STAGE2_GATE1_SEAL_RECONSTRUCTION_MISMATCH")

    expected_bytes = (
        json.dumps(expected, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    if expected_bytes != approved_plan_bytes:
        raise Stop("STAGE2_GATE1_SEAL_APPROVED_PLAN_BYTES_MISMATCH")

    return {
        "approved_plan_hash": approved_hash,
        "approved_plan_sha256": sha256_bytes(approved_plan_bytes),
        "approved_by": APPROVED_BY,
        "approved_at": approved_at,
        "decision_count": len(approved.get("decisions") or []),
    }


def run_stage2_gate1_seal_tool(
    repo: Path,
    school_key: str,
    *,
    freeze_bytes: bytes,
    plan_bytes: bytes,
    filled_review_bytes: bytes,
    diag: Path,
    tool_repo: Path | None = None,
) -> dict[str, Any]:
    """Invoke permanent --approve, checkpoint exact seal bytes, and prove no mutation."""

    restore_integration_freeze(repo, school_key, freeze_bytes)
    base_output = repo / ".onboarding" / school_key
    seal_output = base_output / SEALED_DIR_NAME
    seal_output.mkdir(parents=True, exist_ok=True)
    plan_path = seal_output / "plan.json"
    review_path = seal_output / "filled-review.csv"
    plan_path.write_bytes(plan_bytes)
    review_path.write_bytes(filled_review_bytes)

    before = tracked_worktree_state(repo)
    if before["status"]:
        raise Stop("STAGE2_GATE1_SEAL_TRACKED_STATE_DIRTY_BEFORE_RUN")

    runtime_repo = (tool_repo or RUNTIME_ROOT).resolve()
    onboard_tool = runtime_repo / "tools/onboard_school.py"
    onboarding_plan_tool = runtime_repo / "tools/onboarding_plan.py"
    if not onboard_tool.is_file():
        raise Stop("STAGE2_GATE1_SEAL_RUNTIME_ONBOARD_TOOL_MISSING")
    if not onboarding_plan_tool.is_file():
        raise Stop("STAGE2_GATE1_SEAL_RUNTIME_PLAN_TOOL_MISSING")
    runtime_tool_sha256 = {
        "tools/onboard_school.py": sha256_file(onboard_tool),
        "tools/onboarding_plan.py": sha256_file(onboarding_plan_tool),
    }

    cmd = [
        sys.executable,
        str(onboard_tool),
        school_key,
        "--approve",
        "--repo",
        str(repo),
        "--output-dir",
        str(seal_output),
        "--plan-file",
        str(plan_path),
        "--review-file",
        str(review_path),
        "--approved-by",
        APPROVED_BY,
    ]
    cp = run(cmd, cwd=runtime_repo, check=False)
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "stage2-gate1-seal.log").write_text(
        cp.stdout or "",
        encoding="utf-8",
    )

    after = tracked_worktree_state(repo)
    if (
        before["head_sha"] != after["head_sha"]
        or before["tree_sha"] != after["tree_sha"]
        or after["status"]
    ):
        raise Stop(
            "STAGE2_GATE1_SEAL_TRACKED_MUTATION_DETECTED "
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
        raise Stop("STAGE2_GATE1_SEAL_PERMANENT_COMMAND_FAILED")
    if "OWNER GATE 1 SEALED" not in (cp.stdout or ""):
        raise Stop("STAGE2_GATE1_SEAL_SUCCESS_MARKER_MISSING")

    approved_path = seal_output / APPROVED_PLAN_NAME
    approved_review_path = seal_output / APPROVED_REVIEW_NAME
    if not approved_path.is_file() or not approved_review_path.is_file():
        raise Stop("STAGE2_GATE1_SEAL_OUTPUT_MISSING")
    approved_plan_bytes = approved_path.read_bytes()
    approved_review_bytes = approved_review_path.read_bytes()
    summary = verify_sealed_plan_bytes(
        repo,
        plan_bytes=plan_bytes,
        filled_review_bytes=filled_review_bytes,
        approved_plan_bytes=approved_plan_bytes,
    )

    output_match = _APPROVED_HASH_RE.search(cp.stdout or "")
    if not output_match or output_match.group(1) != summary["approved_plan_hash"]:
        raise Stop("STAGE2_GATE1_SEAL_COMMAND_HASH_MISMATCH")

    return {
        "command": [
            "python",
            "tools/onboard_school.py",
            school_key,
            "--approve",
            "--approved-by",
            APPROVED_BY,
        ],
        "exit_code": cp.returncode,
        "approved_plan_bytes": approved_plan_bytes,
        "approved_review_bytes": approved_review_bytes,
        "approved_plan_hash": summary["approved_plan_hash"],
        "approved_plan_sha256": summary["approved_plan_sha256"],
        "approved_review_sha256": sha256_bytes(approved_review_bytes),
        "approved_by": summary["approved_by"],
        "approved_at": summary["approved_at"],
        "decision_count": summary["decision_count"],
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
