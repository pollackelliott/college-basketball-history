#!/usr/bin/env python3
"""Generic, fail-closed Owner Gate 2 and exact Production-proof authority.

No PR merge is performed by the control runner. The school Implementation chat
uses its owner-authorized GitHub connector to merge the exact approved PR HEAD,
then invokes the read-only Production proof operation. The durable approval
must be verified independently before connector merge.
"""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import release_school
from remote_implementation_control import sha256_bytes
from remote_implementation_io import Stop, git, git_show_bytes, remote_head
from remote_implementation_release_preview import (
    verify_release_preview_authority,
    verify_pr_checks_and_preview,
)


def require(condition: bool, code: str) -> None:
    if not condition:
        raise Stop(code)


def bound_document(control_head: str, ref: dict[str, str], *, repo: Path, label: str) -> dict:
    path, digest = ref.get("path", ""), ref.get("sha256", "")
    require(
        path.startswith(".remote-implementation/")
        and ".." not in Path(path).parts
        and len(digest) == 64,
        "GATE2_%s_REFERENCE_INVALID" % label,
    )
    payload = git_show_bytes(control_head, path, cwd=repo)
    require(sha256_bytes(payload) == digest, "GATE2_%s_HASH_MISMATCH" % label)
    result = json.loads(payload)
    require(isinstance(result, dict), "GATE2_%s_INVALID_JSON" % label)
    return result


def matched(document: dict, expected: dict, label: str) -> None:
    for name, value in expected.items():
        require(
            document.get(name) == value,
            "GATE2_%s_%s_MISMATCH" % (label, name.upper()),
        )


def verify_gate2_ready_chain(
    request: dict[str, Any],
    control_head: str,
    *,
    repo: Path,
    check_live_preview: bool,
) -> dict[str, Any]:
    school = request["school_key"]
    prefix = f".remote-implementation/checkpoints/{school}/"
    checkpoint_ref = request["release_preview_checkpoint"]
    checkpoint_path = checkpoint_ref["path"]
    require(
        checkpoint_path.startswith(prefix)
        and checkpoint_path.endswith("/checkpoint-manifest.json"),
        "GATE2_PREVIEW_CHECKPOINT_PATH_INVALID",
    )
    manifest = bound_document(
        control_head, checkpoint_ref, repo=repo, label="PREVIEW_CHECKPOINT"
    )
    previous_id = manifest["request_id"]
    verification_path = (
        f".remote-implementation/verifications/{school}/{previous_id}/"
        "release-preview-verification.json"
    )
    verify_ref = request["release_preview_verification"]
    require(
        verify_ref["path"] == verification_path,
        "GATE2_PREVIEW_VERIFICATION_PATH_INVALID",
    )
    verified = bound_document(
        control_head, verify_ref, repo=repo, label="PREVIEW_VERIFICATION"
    )
    expected = {
        "school_key": school,
        "pr_number": request["pr_number"],
        "pr_head_sha": request["target_sha"],
        "preview_deployment_id": request["preview_deployment_id"],
        "preview_url": request["preview_url"],
    }
    matched(manifest, {
        **expected,
        "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_READY_CHECKPOINT",
        "gate2_status": "OWNER_GATE_2_READY",
        "owner_gate_2_approved": False,
        "merged": False,
        "production_proof": False,
        "approved_plan_hash": request["approved_plan_hash"],
        "release_manifest_sha256": request["release_manifest_sha256"],
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
    }, "PREVIEW_CHECKPOINT")
    matched(verified, {
        "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_READY_VERIFICATION",
        "request_id": previous_id,
        "school_key": school,
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "checkpoint_manifest_sha256": checkpoint_ref["sha256"],
        "pr_number": request["pr_number"],
        "pr_head_sha": request["target_sha"],
        "preview_deployment_id": request["preview_deployment_id"],
        "preview_url": request["preview_url"],
        "remote_release_preview_equivalence": "PASS",
        "owner_gate_2_approved": False,
        "merged": False,
    }, "PREVIEW_VERIFICATION")
    prev_path = (Path(checkpoint_path).parent / "request.json").as_posix()
    prev_bytes = git_show_bytes(control_head, prev_path, cwd=repo)
    require(
        sha256_bytes(prev_bytes) == manifest["request_sha256"],
        "GATE2_PREVIEW_SOURCE_REQUEST_HASH_MISMATCH",
    )
    prev_request = json.loads(prev_bytes)
    matched(prev_request, {
        "operation": "RELEASE_PREVIEW_VERIFY",
        "school_key": school,
        "pr_number": request["pr_number"],
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "approved_plan_hash": request["approved_plan_hash"],
        "release_manifest_sha256": request["release_manifest_sha256"],
    }, "SOURCE_REQUEST")
    authority = verify_release_preview_authority(
        prev_request, control_head, source_repo=repo
    )
    require(
        authority["pr_body_sha256"] == manifest["pr_body_sha256"],
        "GATE2_APPROVED_PR_BODY_MISMATCH",
    )
    prev_main = manifest["protected_main_sha"]
    current_main = request["expected_protected_main_sha"]
    require(
        git("merge-base", "--is-ancestor", prev_main, current_main,
            cwd=repo, check=False).returncode == 0,
        "GATE2_CURRENT_MAIN_NOT_DESCENDANT",
    )
    if check_live_preview:
        # Reuse the same permanent exact-PR/CI/Preview verification path.
        checked = verify_pr_checks_and_preview(
            repo,
            pr_number=request["pr_number"],
            target_branch=request["target_branch"],
            target_sha=request["target_sha"],
            exact_pr_body_sha256=authority["pr_body_sha256"],
        )
        require(
            checked["preview_deployment_id"] == request["preview_deployment_id"]
            and checked["preview_url"] == request["preview_url"],
            "GATE2_APPROVED_PREVIEW_DEPLOYMENT_DRIFT",
        )
    return {
        "school_key": school,
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "pr_number": request["pr_number"],
        "preview_deployment_id": request["preview_deployment_id"],
        "preview_url": request["preview_url"],
        "pr_body_sha256": authority["pr_body_sha256"],
        "approved_plan_hash": request["approved_plan_hash"],
        "release_manifest_sha256": request["release_manifest_sha256"],
        "preview_checkpoint_sha256": checkpoint_ref["sha256"],
        "preview_verification_sha256": verify_ref["sha256"],
        "preview_request_id": previous_id,
        "preview_main_sha": prev_main,
    }


def approve_exact_gate2(
    request: dict[str, Any], control_head: str, *, repo: Path,
) -> dict[str, Any]:
    authority = verify_gate2_ready_chain(
        request, control_head, repo=repo, check_live_preview=True
    )
    approval = request["owner_gate_2_approval"]
    require(approval.get("approved") is True, "GATE2_EXPLICIT_APPROVAL_REQUIRED")
    matched(approval, {
        "preview_checkpoint_sha256": authority["preview_checkpoint_sha256"],
        "preview_verification_sha256": authority["preview_verification_sha256"],
        "pr_number": authority["pr_number"],
        "pr_head_sha": authority["target_sha"],
        "preview_deployment_id": authority["preview_deployment_id"],
        "preview_url": authority["preview_url"],
    }, "OWNER_APPROVAL")
    return {
        "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_APPROVAL",
        "status": "OWNER_GATE_2_APPROVED",
        **authority,
        "owner_gate_2_approved": True,
        "merge_authorized_pr_number": authority["pr_number"],
        "merge_authorized_exact_head_sha": authority["target_sha"],
        "merged": False,
        "production_proof": False,
    }


def verify_gate2_approved_chain(
    request: dict[str, Any], control_head: str, *, repo: Path,
) -> dict[str, Any]:
    school = request["school_key"]
    approval_ref = request["owner_gate_2_checkpoint"]
    approval_path = approval_ref["path"]
    require(
        approval_path.startswith(f".remote-implementation/checkpoints/{school}/")
        and approval_path.endswith("/checkpoint-manifest.json"),
        "PRODUCTION_GATE2_APPROVAL_PATH_INVALID",
    )
    manifest = bound_document(
        control_head, approval_ref, repo=repo, label="APPROVAL_CHECKPOINT"
    )
    original_id = manifest["request_id"]
    ver_ref = request["owner_gate_2_verification"]
    vpath = (
        f".remote-implementation/verifications/{school}/{original_id}/"
        "gate2-approval-verification.json"
    )
    require(ver_ref["path"] == vpath, "PRODUCTION_APPROVAL_VERIFICATION_PATH_INVALID")
    verified = bound_document(
        control_head, ver_ref, repo=repo, label="APPROVAL_VERIFICATION"
    )
    matched(manifest, {
        "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_APPROVED_CHECKPOINT",
        "status": "OWNER_GATE_2_APPROVED",
        "school_key": school,
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "pr_number": request["pr_number"],
        "owner_gate_2_approved": True,
        "merged": False,
        "production_proof": False,
    }, "APPROVAL_CHECKPOINT")
    matched(verified, {
        "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_APPROVAL_VERIFICATION",
        "status": "PASS",
        "request_id": original_id,
        "school_key": school,
        "checkpoint_sha256": approval_ref["sha256"],
        "pr_number": request["pr_number"],
        "pr_head_sha": request["target_sha"],
        "owner_gate_2_approved": True,
    }, "APPROVAL_VERIFICATION")
    original_bytes = git_show_bytes(
        control_head, (Path(approval_path).parent / "request.json").as_posix(),
        cwd=repo,
    )
    require(
        sha256_bytes(original_bytes) == manifest["request_sha256"],
        "PRODUCTION_ORIGINAL_GATE2_REQUEST_HASH_MISMATCH",
    )
    original = json.loads(original_bytes)
    matched(original, {
        "operation": "RELEASE_GATE2_APPROVAL",
        "school_key": school,
        "target_sha": request["target_sha"],
        "pr_number": request["pr_number"],
    }, "ORIGINAL_APPROVAL")
    require(
        original["owner_gate_2_approval"]["approved"] is True,
        "PRODUCTION_OWNER_GATE2_NOT_APPROVED",
    )
    # Earlier authority chain is immutable. A merged PR no longer passes the
    # original live-open PR test, so do not use live check here.
    chain = verify_gate2_ready_chain(
        original, control_head, repo=repo, check_live_preview=False
    )
    for name, expected in (
        ("preview_checkpoint_sha256", chain["preview_checkpoint_sha256"]),
        ("preview_verification_sha256", chain["preview_verification_sha256"]),
        ("preview_deployment_id", chain["preview_deployment_id"]),
        ("preview_url", chain["preview_url"]),
        ("approved_plan_hash", chain["approved_plan_hash"]),
        ("release_manifest_sha256", chain["release_manifest_sha256"]),
    ):
        require(manifest.get(name) == expected, "PRODUCTION_GATE2_%s_MISMATCH" % name.upper())
    return {
        **chain,
        "owner_gate_2_approval_checkpoint_sha256": approval_ref["sha256"],
        "owner_gate_2_verification_sha256": ver_ref["sha256"],
        "gate2_request_id": original_id,
        "original_main_sha": original["expected_protected_main_sha"],
    }


def verify_exact_merge(
    request: dict[str, Any], authority: dict[str, Any], *,
    repo: Path,
) -> dict[str, Any]:
    merge_sha = request["merge_sha"]
    pr_number = request["pr_number"]
    _target = request["target_sha"]
    live_main = release_school.git(repo, "ls-remote", "--heads", "origin", "main").split()
    require(bool(live_main) and live_main[0] == merge_sha, "PRODUCTION_MAIN_NOT_EXACT_MERGE")
    merged = release_school.gh_json(
        repo, "pr", "view", str(pr_number), "--json",
        "number,state,mergedAt,mergeCommit,headRefOid,headRefName,baseRefName",
    )
    matched(merged, {
        "number": pr_number,
        "state": "MERGED",
        "headRefOid": _target,
        "headRefName": request["target_branch"],
        "baseRefName": "main",
    }, "MERGED_PR")
    require(bool(merged.get("mergedAt")), "PRODUCTION_PR_NO_MERGED_AT")
    require(
        isinstance(merged.get("mergeCommit"), dict)
        and merged["mergeCommit"].get("oid") == merge_sha,
        "PRODUCTION_PR_MERGE_SHA_MISMATCH",
    )
    parents = release_school.git(repo, "rev-list", "--parents", "-n", "1", merge_sha).split()
    require(len(parents) == 3, "PRODUCTION_NOT_EXACT_TWO_PARENT_MERGE")
    require(parents[0] == merge_sha and parents[2] == _target, "PRODUCTION_MERGE_SECOND_PARENT_INVALID")
    require(
        parents[1] == authority["original_main_sha"],
        "PRODUCTION_MERGE_FIRST_PARENT_NOT_APPROVED_MAIN",
    )
    return {
        "pr_number": pr_number,
        "pr_head_sha": _target,
        "merge_sha": merge_sha,
        "merge_parent_main": parents[1],
        "merge_parent_onboarding": parents[2],
    }


def run_permanent_production_proof(
    request: dict[str, Any],
    authority: dict[str, Any], *,
    repo: Path,
    timeout: int = 900,
) -> dict[str, Any]:
    merge = verify_exact_merge(request, authority, repo=repo)
    school, merge_sha = request["school_key"], request["merge_sha"]
    require(0 < timeout <= 1800, "PRODUCTION_TIMEOUT_INVALID")
    with tempfile.TemporaryDirectory(prefix=f"remote-prod-proof-{school}-") as temp:
        proof_repo = Path(temp) / "repository"
        release_school.create_production_proof_repository(
            repo, proof_repo, merge_sha, school_key=school,
            correction_freeze=None,
        )
        # The full PR delta includes prior Phase 0 data, not only sealed
        # apply's final changed-path population.
        names = release_school.git(
            proof_repo, "diff", "--name-only", merge["merge_parent_main"], merge_sha
        )
        changed_paths = sorted(set(x.strip() for x in names.splitlines() if x.strip()))
        require(bool(changed_paths), "PRODUCTION_EMPTY_PR_DELTA")
        release_school.run_gates(
            proof_repo, school, [], include_tests=True,
        )
        deployment = release_school.wait_for_deployment(
            proof_repo, release_school.repository_slug(repo),
            merge_sha, "Production", timeout,
        )
        require(
            deployment.get("sha") == merge_sha
            and deployment.get("state") == "success"
            and "production" in str(deployment.get("environment", "")).casefold(),
            "PRODUCTION_EXACT_DEPLOYMENT_MISMATCH",
        )
        checked = release_school.production_data_check(
            proof_repo, school, merge_sha, changed_paths
        )
        required_public_json = {
            "/data/manifest.json",
            "/data/programs.json",
            f"/data/teams/{school}.json",
        }
        require(
            required_public_json.issubset(set(checked)),
            "PRODUCTION_REQUIRED_PUBLIC_JSON_NOT_VERIFIED",
        )
    require(
        release_school.git(repo, "ls-remote", "--heads", "origin", "main").split()[0]
        == merge_sha, "PRODUCTION_MAIN_MOVED_DURING_PROOF"
    )
    return {
        "kind": "REMOTE_IMPLEMENTATION_EXACT_PRODUCTION_PROOF",
        "status": "COMPLETE",
        "school_key": school,
        "pr_number": request["pr_number"],
        "pr_head_sha": request["target_sha"],
        "merge_sha": merge_sha,
        "merge_parent_main": merge["merge_parent_main"],
        "merge_parent_onboarding": merge["merge_parent_onboarding"],
        "production_deployment_id": deployment["deployment_id"],
        "production_deployment_sha": deployment["sha"],
        "production_environment": deployment["environment"],
        "production_json_checked": checked,
        "production_json_checked_count": len(checked),
        "owner_gate_2_approval_checkpoint_sha256": authority["owner_gate_2_approval_checkpoint_sha256"],
        "owner_gate_2_verification_sha256": authority["owner_gate_2_verification_sha256"],
        "permanent_merged_main_gates": "PASS",
        "exact_production_json": "PASS",
    }
