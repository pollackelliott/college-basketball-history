#!/usr/bin/env python3
"""Read-only Stage A shadow observer for exact release connector handoffs.

Nothing in this module creates PRs, merges, pushes refs, dispatches Actions,
creates authority, or writes to the repository. A "WOULD_*" result identifies
a cryptographically authenticated packet, NOT a license to execute the action:
live PR/CI/Preview checks and an independently authorized external executor
remain future, separately governed work.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from remote_implementation_control import (
    LIFECYCLE_IDLE,
    TX_COMPLETE,
    sha256_bytes,
    validate_control_state,
)

STATE_PATH = ".remote-implementation/control-state.json"
CONTROL_BRANCH = "control/remote-implementation"
REA = "RELEASE_READINESS"
GATE = "RELEASE_GATE2_APPROVAL"
VALID_SHA = re.compile(r"^[0-9a-f]{40}$")
SAFE_BRANCH = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._/-]*$")
Blob = Callable[[str], bytes]


class ShadowStop(ValueError):
    """A read-only authority or identity check refused the proposed action."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ShadowStop(code)


def read_json(raw: bytes, code: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw)
    except (TypeError, ValueError) as exc:
        raise ShadowStop(code) from exc
    require(isinstance(parsed, dict), code)
    return parsed


def webhook_wakeup(payload: bytes, signature: str, secret: bytes) -> dict[str, str]:
    """Authenticate a completed workflow webhook; it is scheduling only."""
    require(bool(secret), "SHADOW_WEBHOOK_SECRET_REQUIRED")
    require(signature.startswith("sha256="), "SHADOW_WEBHOOK_SIGNATURE_MISSING")
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    require(
        hmac.compare_digest(signature[len("sha256="):], expected),
        "SHADOW_WEBHOOK_SIGNATURE_INVALID",
    )
    event = read_json(payload, "SHADOW_WEBHOOK_JSON_INVALID")
    workflow = event.get("workflow_run")
    require(isinstance(workflow, dict), "SHADOW_WEBHOOK_NOT_WORKFLOW_RUN")
    require(
        event.get("action") == "completed"
        and workflow.get("status") == "completed",
        "SHADOW_WEBHOOK_NOT_COMPLETED",
    )
    run_id = workflow.get("id")
    require(isinstance(run_id, int) and run_id > 0, "SHADOW_RUN_ID_INVALID")
    return {"wakeup_kind": "WORKFLOW_RUN_COMPLETED", "run_id": str(run_id)}


def _blob(blobs: Blob, path: str, label: str) -> bytes:
    require(
        path.startswith(".remote-implementation/")
        and ".." not in Path(path).parts,
        "SHADOW_UNSAFE_" + label + "_PATH",
    )
    try:
        raw = blobs(path)
    except (OSError, KeyError, ValueError) as exc:
        raise ShadowStop("SHADOW_" + label + "_NOT_FOUND") from exc
    require(isinstance(raw, bytes), "SHADOW_" + label + "_NOT_BYTES")
    return raw


def _bound_doc(blobs: Blob, path: str, expected_sha: str, label: str) -> dict[str, Any]:
    require(
        isinstance(expected_sha, str) and bool(re.fullmatch(r"[0-9a-f]{64}", expected_sha)),
        "SHADOW_" + label + "_HASH_REQUIRED",
    )
    raw = _blob(blobs, path, label)
    require(sha256_bytes(raw) == expected_sha, "SHADOW_" + label + "_HASH_MISMATCH")
    return read_json(raw, "SHADOW_" + label + "_JSON_INVALID")


def _same(d: dict[str, Any], expected: dict[str, Any], label: str) -> None:
    for field, value in expected.items():
        require(d.get(field) == value, f"SHADOW_{label}_{field.upper()}_MISMATCH")


def _load_source(
    control_head: str,
    state: dict[str, Any],
    blobs: Blob,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], str]:
    last = state.get("last_operation")
    require(isinstance(last, dict), "SHADOW_LAST_OPERATION_MISSING")
    req_id = last.get("request_id")
    school = last.get("school_key")
    require(isinstance(req_id, str) and bool(req_id), "SHADOW_REQUEST_ID_INVALID")
    require(isinstance(school, str) and re.fullmatch(r"[a-z0-9-]+", school) is not None,
            "SHADOW_SCHOOL_INVALID")
    base = f".remote-implementation/checkpoints/{school}/{req_id}"
    manifest_path = base + "/checkpoint-manifest.json"
    require(last.get("checkpoint_manifest_path") == manifest_path,
            "SHADOW_LAST_CHECKPOINT_PATH_MISMATCH")
    checkpoint = _bound_doc(
        blobs, manifest_path, last.get("checkpoint_manifest_sha256"),
        "CHECKPOINT",
    )
    request = _bound_doc(
        blobs, base + "/request.json", checkpoint.get("request_sha256"),
        "ORIGINAL_REQUEST",
    )
    _same(checkpoint, {"request_id": req_id, "school_key": school}, "CHECKPOINT")
    _same(request, {
        "request_id": req_id,
        "school_key": school,
        "operation": last.get("operation"),
    }, "SOURCE_REQUEST")
    # The action is a pure observation at one immutable Git control commit.
    require(bool(VALID_SHA.fullmatch(control_head)), "SHADOW_CONTROL_HEAD_INVALID")
    return last, checkpoint, request, base


def _verified_readiness(
    blobs: Blob,
    last: dict[str, Any],
    checkpoint: dict[str, Any],
    request: dict[str, Any],
    base: str,
    main_sha: str,
    target_sha: str,
) -> tuple[dict[str, Any], str]:
    rid = checkpoint["request_id"]
    school = checkpoint["school_key"]
    _same(checkpoint, {
        "kind": "REMOTE_IMPLEMENTATION_RELEASE_READINESS_CHECKPOINT",
        "readiness_status": "RELEASE_READINESS_PASS",
        "owner_gate_2": False,
        "pr_created": False,
        "preview_verified": False,
        "tracked_mutation": "NONE",
    }, "READINESS")
    require(
        request.get("release_phase_continuation", {}).get("kind")
        == "RELEASE_READINESS_TO_PREVIEW_V1",
        "SHADOW_READINESS_NOT_PREAUTHORIZED_FOR_CONTINUATION",
    )
    verification_path = (
        f".remote-implementation/verifications/{school}/{rid}/"
        "release-readiness-verification.json"
    )
    verification = read_json(
        _blob(blobs, verification_path, "READINESS_VERIFICATION"),
        "SHADOW_READINESS_VERIFICATION_JSON_INVALID",
    )
    _same(verification, {
        "kind": "REMOTE_IMPLEMENTATION_RELEASE_READINESS_VERIFICATION",
        "request_id": rid,
        "school_key": school,
        "remote_release_readiness_equivalence": "PASS",
        "checkpoint_manifest_sha256": last["checkpoint_manifest_sha256"],
        "preview_request_id": checkpoint.get("preview_request_id"),
        "release_pr_packet_sha256": checkpoint.get("release_pr_packet_sha256"),
        "pr_body_sha256": checkpoint.get("pr_body_sha256"),
        "target_sha": checkpoint.get("target_sha"),
        "tracked_mutation": "NONE",
        "owner_gate_2": False,
        "pr_created": False,
    }, "READINESS_VERIFICATION")
    packet_path = base + "/release-pr-packet.json"
    require(checkpoint.get("release_pr_packet_path") == packet_path,
            "SHADOW_PR_PACKET_PATH_MISMATCH")
    packet = _bound_doc(
        blobs, packet_path, checkpoint.get("release_pr_packet_sha256"), "PR_PACKET"
    )
    body_path = base + "/pr-body.md"
    require(checkpoint.get("pr_body_checkpoint_path") == body_path,
            "SHADOW_PR_BODY_PATH_MISMATCH")
    body = _blob(blobs, body_path, "PR_BODY")
    require(
        sha256_bytes(body) == checkpoint.get("pr_body_sha256"),
        "SHADOW_PR_BODY_HASH_MISMATCH",
    )
    _same(packet, {
        "kind": "REMOTE_IMPLEMENTATION_RELEASE_PR_PACKET",
        "school_key": school,
        "readiness_request_id": rid,
        "preview_request_id": checkpoint.get("preview_request_id"),
        "base_branch": "main",
        "head_branch": checkpoint.get("target_branch"),
        "head_sha": checkpoint.get("target_sha"),
        "body_checkpoint_path": body_path,
        "body_sha256": checkpoint.get("pr_body_sha256"),
        "approved_plan_hash": checkpoint.get("approved_plan_hash"),
        "release_manifest_sha256": checkpoint.get("release_manifest_sha256"),
        "owner_gate_2": False,
        "pr_created_by_runner": False,
    }, "PR_PACKET")
    require(
        request.get("release_phase_continuation", {}).get("preview_request_id")
        == packet["preview_request_id"],
        "SHADOW_PREVIEW_CHILD_ID_AUTHORITY_MISMATCH",
    )
    require(
        packet["head_sha"] == target_sha
        and checkpoint.get("protected_main_sha") == main_sha,
        "SHADOW_READINESS_CURRENT_REFS_CHANGED",
    )
    return packet, "WOULD_CREATE_OR_REUSE_EXACT_PR_AFTER_LIVE_CHECKS"


def _verified_gate2(
    blobs: Blob,
    last: dict[str, Any],
    checkpoint: dict[str, Any],
    request: dict[str, Any],
    base: str,
    main_sha: str,
    target_sha: str,
) -> tuple[dict[str, Any], str]:
    rid = checkpoint["request_id"]
    school = checkpoint["school_key"]
    _same(checkpoint, {
        "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_APPROVED_CHECKPOINT",
        "status": "OWNER_GATE_2_APPROVED",
        "owner_gate_2_approved": True,
        "merged": False,
        "production_proof": False,
    }, "GATE2")
    require(
        request.get("final_release_continuation", {}).get("kind")
        == "RELEASE_GATE2_TO_PRODUCTION_V1"
        and request.get("owner_gate_2_approval", {}).get("approved") is True,
        "SHADOW_EXPLICIT_GATE2_APPROVAL_MISSING",
    )
    verification_path = (
        f".remote-implementation/verifications/{school}/{rid}/"
        "gate2-approval-verification.json"
    )
    verified = read_json(
        _blob(blobs, verification_path, "GATE2_VERIFICATION"),
        "SHADOW_GATE2_VERIFICATION_JSON_INVALID",
    )
    _same(verified, {
        "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_APPROVAL_VERIFICATION",
        "request_id": rid,
        "school_key": school,
        "checkpoint_sha256": last.get("checkpoint_manifest_sha256"),
        "remote_gate2_approval_equivalence": "PASS",
        "owner_gate_2_approved": True,
        "pr_head_sha": checkpoint.get("pr_head_sha"),
        "pr_number": checkpoint.get("pr_number"),
        "preview_deployment_id": checkpoint.get("preview_deployment_id"),
        "preview_url": checkpoint.get("preview_url"),
        "production_request_id": checkpoint.get("production_request_id"),
        "gate2_merge_packet_sha256": checkpoint.get("gate2_merge_packet_sha256"),
        "merged": False,
    }, "GATE2_VERIFICATION")
    packet_path = base + "/gate2-merge-packet.json"
    require(checkpoint.get("gate2_merge_packet_path") == packet_path,
            "SHADOW_MERGE_PACKET_PATH_MISMATCH")
    packet = _bound_doc(
        blobs, packet_path, checkpoint.get("gate2_merge_packet_sha256"),
        "MERGE_PACKET",
    )
    _same(packet, {
        "kind": "REMOTE_IMPLEMENTATION_GATE2_MERGE_PACKET",
        "school_key": school,
        "gate2_request_id": rid,
        "production_request_id": checkpoint.get("production_request_id"),
        "pr_number": checkpoint.get("pr_number"),
        "pr_head_sha": checkpoint.get("pr_head_sha"),
        "base_branch": "main",
        "target_branch": checkpoint.get("target_branch"),
        "merge_method": "merge",
        "approved_main_sha": checkpoint.get("protected_main_sha"),
        "preview_deployment_id": checkpoint.get("preview_deployment_id"),
        "preview_url": checkpoint.get("preview_url"),
        "owner_gate_2_approved": True,
        "merged": False,
        "production_proof": False,
    }, "MERGE_PACKET")
    require(
        request.get("final_release_continuation", {}).get("production_request_id")
        == packet["production_request_id"],
        "SHADOW_PRODUCTION_CHILD_ID_AUTHORITY_MISMATCH",
    )
    require(
        packet["approved_main_sha"] == main_sha
        and packet["pr_head_sha"] == target_sha,
        "SHADOW_GATE2_CURRENT_REFS_CHANGED",
    )
    return packet, "WOULD_MERGE_EXACT_APPROVED_PR_AFTER_LIVE_CHECKS"


def evaluate_shadow(
    *,
    repo_slug: str,
    control_head: str,
    state_bytes: bytes,
    blobs: Blob,
    main_sha: str,
    target_sha: str | None,
) -> dict[str, Any]:
    """Pure, deterministic, fail-closed evaluation; emits no mutations."""
    state = read_json(state_bytes, "SHADOW_CONTROL_STATE_JSON_INVALID")
    validate_control_state(state)
    require(bool(VALID_SHA.fullmatch(control_head)), "SHADOW_CONTROL_HEAD_INVALID")
    require(bool(VALID_SHA.fullmatch(main_sha)), "SHADOW_MAIN_SHA_INVALID")
    require(state.get("lifecycle_state") == LIFECYCLE_IDLE
            and state.get("transaction_state") == TX_COMPLETE
            and state.get("recovery_required") is False
            and state.get("active_request_id") is None
            and state.get("active_lock_commit") is None,
            "SHADOW_CONTROL_NOT_SAFELY_IDLE")
    last = state.get("last_operation") or {}
    op = last.get("operation")
    if op not in {REA, GATE}:
        return {
            "status": "NO_ELIGIBLE_HANDOFF",
            "reason": "LAST_OPERATION_NOT_CONNECTOR_HANDOFF",
            "last_operation": op,
            "control_head": control_head,
            "actions_executed": 0,
        }
    if last.get("fresh_runner_verification") != "PASS":
        return {
            "status": "NOT_READY",
            "reason": "FRESH_VERIFICATION_NOT_PASS",
            "last_operation": op,
            "control_head": control_head,
            "actions_executed": 0,
        }
    require(isinstance(target_sha, str) and bool(VALID_SHA.fullmatch(target_sha)),
            "SHADOW_TARGET_HEAD_REQUIRED")
    last, checkpoint, request, base = _load_source(control_head, state, blobs)
    if op == REA:
        packet, action = _verified_readiness(
            blobs, last, checkpoint, request, base, main_sha, target_sha
        )
        packet_hash = checkpoint["release_pr_packet_sha256"]
    else:
        packet, action = _verified_gate2(
            blobs, last, checkpoint, request, base, main_sha, target_sha
        )
        packet_hash = checkpoint["gate2_merge_packet_sha256"]
    identity = "\n".join((
        repo_slug, checkpoint["school_key"], op,
        checkpoint["request_id"], packet_hash,
    ))
    return {
        "status": "AUTHENTICATED_PACKET_SHADOW_ONLY",
        "candidate_action": action,
        "external_pr_ci_preview_preconditions": "NOT_CHECKED_BY_SHADOW",
        "control_head": control_head,
        "source_request_id": checkpoint["request_id"],
        "school_key": checkpoint["school_key"],
        "packet_sha256": packet_hash,
        "work_item_sha256": hashlib.sha256(identity.encode("utf-8")).hexdigest(),
        "child_request_id": (
            packet["preview_request_id"] if op == REA
            else packet["production_request_id"]
        ),
        "actions_executed": 0,
        "execution_authorized_by_this_tool": False,
    }


def _git(repo: Path, *args: str) -> bytes:
    run = subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if run.returncode:
        raise ShadowStop("SHADOW_GIT_READ_FAILED:" + " ".join(args[:2]))
    return run.stdout


def _remote_head(repo: Path, branch: str) -> str:
    require(bool(SAFE_BRANCH.fullmatch(branch))
            and ".." not in branch and "//" not in branch,
            "SHADOW_UNSAFE_BRANCH")
    result = _git(repo, "ls-remote", "--heads", "origin", branch).decode().strip()
    require(bool(result), "SHADOW_REMOTE_HEAD_MISSING")
    sha = result.split("\t", 1)[0]
    require(bool(VALID_SHA.fullmatch(sha)), "SHADOW_REMOTE_HEAD_INVALID")
    return sha


def inspect_live_read_only(repo: Path) -> dict[str, Any]:
    """Git remote reads only. No fetch, checkout, commit, dispatch, or push."""
    control_head = _remote_head(repo, CONTROL_BRANCH)
    main_sha = _remote_head(repo, "main")
    state_raw = _git(repo, "show", f"{control_head}:{STATE_PATH}")
    state = read_json(state_raw, "SHADOW_CONTROL_STATE_JSON_INVALID")
    last = state.get("last_operation") or {}
    # A completed/non-handoff school needs no remote target query at all.
    target_sha = None
    if last.get("operation") in {REA, GATE}:
        checkpoint_path = last.get("checkpoint_manifest_path")
        require(isinstance(checkpoint_path, str), "SHADOW_CHECKPOINT_PATH_MISSING")
        manifest = read_json(
            _git(repo, "show", f"{control_head}:{checkpoint_path}"),
            "SHADOW_CHECKPOINT_JSON_INVALID",
        )
        branch = manifest.get("target_branch")
        require(isinstance(branch, str), "SHADOW_TARGET_BRANCH_MISSING")
        target_sha = _remote_head(repo, branch)
    return evaluate_shadow(
        repo_slug="pollackelliott/college-basketball-history",
        control_head=control_head,
        state_bytes=state_raw,
        blobs=lambda p: _git(repo, "show", f"{control_head}:{p}"),
        main_sha=main_sha,
        target_sha=target_sha,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = inspect_live_read_only(args.repo)
    except (ShadowStop, ValueError) as exc:
        result = {
            "status": "STOP",
            "reason": str(exc),
            "actions_executed": 0,
        }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["status"] != "STOP" else 1


if __name__ == "__main__":
    sys.exit(main())
