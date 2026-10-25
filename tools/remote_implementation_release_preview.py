#!/usr/bin/env python3
"""Read-only, exact-PR/Preview verification after a school chat creates its PR.

No mutation to GitHub refs, PRs, deployment resources, or Owner Gate 2 state.
The school Implementation chat creates/reuses a PR using its own authorized
GitHub connector, then supplies the exact PR number through a bounded request.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import release_school
from remote_implementation_io import Stop, remote_head


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
        "number,url,state,isDraft,headRefOid,headRefName,baseRefName,body",
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
