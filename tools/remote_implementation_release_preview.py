#!/usr/bin/env python3
"""Read-only, exact-PR/Preview verification after a school chat creates its PR.

No mutation to GitHub refs, PRs, deployment resources, or Owner Gate 2 state.
The school Implementation chat creates/reuses a PR using its own authorized
GitHub connector, then supplies the exact PR number through a bounded request.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import release_school
from remote_implementation_io import Stop, remote_head, git, git_show_bytes
from remote_implementation_control import sha256_bytes
from remote_implementation_release_readiness import (
    verify_release_readiness_authority,
)


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise Stop(code)


def check_pr_identity(
    repo: Path,
    *,
    pr_number: int,
    target_branch: str,
    target_sha: str,
    exact_pr_body_sha256: str,
) -> dict[str, Any]:
    """Refuse altered head, wrong target/base, draft/closed PR, or body drift."""
    _require(
        isinstance(pr_number, int) and 1 <= pr_number <= 2147483647,
        "PREVIEW_PR_NUMBER_INVALID",
    )
    _require(
        remote_head(repo, target_branch) == target_sha,
        "PREVIEW_TARGET_REF_MOVED",
    )
    pr = release_school.gh_json(
        repo, "pr", "view", str(pr_number),
        "--json",
        "number,url,state,isDraft,headRefOid,headRefName,baseRefName,body,headRepositoryOwner,headRepository",
    )
    for key, expected in (
        ("number", pr_number),
        ("state", "OPEN"),
        ("isDraft", False),
        ("headRefOid", target_sha),
        ("headRefName", target_branch),
        ("baseRefName", "main"),
    ):
        _require(pr.get(key) == expected, "PREVIEW_PR_%s_MISMATCH" % key.upper())
    # A matching branch name and commit SHA are insufficient if the PR's
    # head is from an unrelated fork. Bind the repository, not just its ref.
    repo_slug = release_school.repository_slug(repo)
    expected_owner, expected_repo = repo_slug.split("/", 1)
    actual_owner = pr.get("headRepositoryOwner") or {}
    actual_repo = pr.get("headRepository") or {}
    _require(
        isinstance(actual_owner, dict)
        and str(actual_owner.get("login", "")).casefold()
        == expected_owner.casefold()
        and isinstance(actual_repo, dict)
        and str(actual_repo.get("name", "")).casefold()
        == expected_repo.casefold(),
        "PREVIEW_PR_FOREIGN_HEAD_REPOSITORY",
    )
    body = pr.get("body")
    _require(isinstance(body, str), "PREVIEW_PR_BODY_MISSING")
    _require(
        hashlib.sha256(body.encode("utf-8")).hexdigest() == exact_pr_body_sha256,
        "PREVIEW_PR_BODY_SHA_MISMATCH",
    )
    url = pr.get("url")
    _require(
        isinstance(url, str) and url.startswith("https://github.com/"),
        "PREVIEW_PR_URL_INVALID",
    )
    return {
        "pr_number": pr_number,
        "pr_url": url,
        "target_branch": target_branch,
        "target_sha": target_sha,
        "pr_body_sha256": exact_pr_body_sha256,
    }


def verify_pr_checks_and_preview(
    repo: Path,
    *,
    pr_number: int,
    target_branch: str,
    target_sha: str,
    exact_pr_body_sha256: str,
    timeout_seconds: int = 900,
) -> dict[str, Any]:
    """Reuse permanent release checks/mergeability/Preview, then re-pin PR.

    This helper must be invoked only after authentication of fresh-verified
    RELEASE_READINESS. In particular this does not itself create the PR.
    """
    identity = check_pr_identity(
        repo, pr_number=pr_number, target_branch=target_branch,
        target_sha=target_sha, exact_pr_body_sha256=exact_pr_body_sha256,
    )
    _require(0 < timeout_seconds <= 1800, "PREVIEW_TIMEOUT_INVALID")
    # Same permanent --prepare check machinery as the Codespaces route.
    release_school.gh(
        repo, "pr", "checks", str(pr_number),
        "--watch", "--interval", "10", echo=False,
    )
    mergeability = release_school.wait_for_pr_mergeable(
        repo, str(pr_number),
        expected_head_sha=target_sha,
    )
    _require(
        mergeability.get("headRefOid") == target_sha,
        "PREVIEW_MERGEABILITY_HEAD_MISMATCH",
    )
    deployment = release_school.wait_for_deployment(
        repo, release_school.repository_slug(repo),
        target_sha, "Preview", timeout_seconds,
    )
    _require(
        deployment.get("sha") == target_sha
        and deployment.get("state") == "success"
        and "preview" in str(deployment.get("environment") or "").casefold(),
        "PREVIEW_DEPLOYMENT_IDENTITY_MISMATCH",
    )
    url = deployment.get("environment_url")
    _require(
        isinstance(url, str) and url.startswith("https://"),
        "PREVIEW_DEPLOYMENT_URL_MISSING",
    )
    # Refuse any exact PR-head or body change during CI/Preview monitoring.
    _require(
        check_pr_identity(
            repo, pr_number=pr_number,
            target_branch=target_branch,
            target_sha=target_sha,
            exact_pr_body_sha256=exact_pr_body_sha256,
        ) == identity,
        "PREVIEW_PR_CHANGED_DURING_VERIFICATION",
    )
    return {
        "kind": "REMOTE_IMPLEMENTATION_PR_PREVIEW_VERIFICATION",
        "status": "OWNER_GATE_2_READY",
        **identity,
        "mergeability": "MERGEABLE",
        "checks": "PASS",
        "preview_deployment_id": deployment["deployment_id"],
        "preview_deployment_sha": target_sha,
        "preview_url": url,
        "preview_status": "success",
        "pr_created_by_runner": False,
        "owner_gate_2_approved": False,
        "merged": False,
        "production_proof": False,
    }


def verify_release_preview_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path,
) -> dict[str, Any]:
    """Authenticate exact fresh-verified readiness and sealed-apply chain."""
    school = request["school_key"]
    branch = f"data/{school}-onboarding"
    checkpoint_ref = request["release_readiness_checkpoint"]
    verification_ref = request["release_readiness_verification"]
    prefix = (
        f".remote-implementation/checkpoints/{school}/"
    )
    checkpoint_path = checkpoint_ref["path"]
    _require(
        checkpoint_path.startswith(prefix)
        and checkpoint_path.endswith("/checkpoint-manifest.json"),
        "PREVIEW_READINESS_CHECKPOINT_PATH_INVALID",
    )
    checkpoint_bytes = git_show_bytes(
        control_commit, checkpoint_path, cwd=source_repo,
    )
    _require(
        sha256_bytes(checkpoint_bytes) == checkpoint_ref["sha256"],
        "PREVIEW_READINESS_CHECKPOINT_HASH_MISMATCH",
    )
    checkpoint = json.loads(checkpoint_bytes)
    source_request_id = checkpoint["request_id"]
    verification_path = (
        f".remote-implementation/verifications/{school}/"
        f"{source_request_id}/release-readiness-verification.json"
    )
    _require(
        verification_ref["path"] == verification_path,
        "PREVIEW_READINESS_VERIFICATION_PATH_INVALID",
    )
    verified_bytes = git_show_bytes(
        control_commit, verification_path, cwd=source_repo,
    )
    _require(
        sha256_bytes(verified_bytes) == verification_ref["sha256"],
        "PREVIEW_READINESS_VERIFICATION_HASH_MISMATCH",
    )
    verified = __import__("json").loads(verified_bytes)
    for doc, expected, label in (
        (
            checkpoint,
            {
                "kind": "REMOTE_IMPLEMENTATION_RELEASE_READINESS_CHECKPOINT",
                "readiness_status": "RELEASE_READINESS_PASS",
                "school_key": school,
                "target_branch": branch,
                "target_sha": request["target_sha"],
                "approved_plan_hash": request["approved_plan_hash"],
                "release_manifest_sha256": request["release_manifest_sha256"],
                "tracked_mutation": "NONE",
                "pr_created": False,
                "owner_gate_2": False,
            },
            "CHECKPOINT",
        ),
        (
            verified,
            {
                "kind": "REMOTE_IMPLEMENTATION_RELEASE_READINESS_VERIFICATION",
                "remote_release_readiness_equivalence": "PASS",
                "request_id": source_request_id,
                "school_key": school,
                "target_branch": branch,
                "target_sha": request["target_sha"],
                "checkpoint_manifest_sha256": checkpoint_ref["sha256"],
                "tracked_mutation": "NONE",
                "pr_created": False,
                "owner_gate_2": False,
            },
            "VERIFICATION",
        ),
    ):
        for field, value in expected.items():
            _require(doc.get(field) == value, f"PREVIEW_READINESS_{label}_{field.upper()}_MISMATCH")
    request_path = (
        Path(checkpoint_path).parent / "request.json"
    ).as_posix()
    prior_bytes = git_show_bytes(
        control_commit, request_path, cwd=source_repo,
    )
    _require(
        sha256_bytes(prior_bytes) == checkpoint["request_sha256"],
        "PREVIEW_READINESS_REQUEST_HASH_MISMATCH",
    )
    prior_request = __import__("json").loads(prior_bytes)
    _require(
        prior_request.get("request_id") == source_request_id
        and prior_request.get("operation") == "RELEASE_READINESS",
        "PREVIEW_READINESS_SOURCE_OPERATION_MISMATCH",
    )
    prior_authority = verify_release_readiness_authority(
        prior_request, control_commit, source_repo=source_repo,
    )
    _require(
        prior_authority["target_sha"] == request["target_sha"]
        and prior_authority["approved_plan_hash"] == request["approved_plan_hash"]
        and prior_authority["release_manifest_sha256"] == request["release_manifest_sha256"],
        "PREVIEW_READINESS_APPLY_CHAIN_MISMATCH",
    )
    source_main = checkpoint["protected_main_sha"]
    current_main = request["expected_protected_main_sha"]
    _require(
        git(
            "merge-base", "--is-ancestor", source_main, current_main,
            cwd=source_repo, check=False,
        ).returncode == 0,
        "PREVIEW_CURRENT_MAIN_NOT_DESCENDANT_OF_READINESS_MAIN",
    )
    _require(
        remote_head(source_repo, branch) == request["target_sha"],
        "PREVIEW_TARGET_MOVED_BEFORE_CHECKS",
    )
    pr_body = prior_authority["sidecars"]["pr-body.md"]
    return {
        "school_key": school,
        "target_branch": branch,
        "target_sha": request["target_sha"],
        "approved_plan_hash": request["approved_plan_hash"],
        "release_manifest_sha256": request["release_manifest_sha256"],
        "readiness_checkpoint_sha256": checkpoint_ref["sha256"],
        "readiness_verification_sha256": verification_ref["sha256"],
        "readiness_request_id": source_request_id,
        "pr_body_sha256": sha256_bytes(pr_body),
    }
