#!/usr/bin/env python3
"""Authenticated post-seal presentation preflight; no tracked ref publication.

The full guarded operation must later acquire the existing Implementation
lock, persist a write-ahead, publish by CAS, support explicit recovery, and
independently fresh-verify before release readiness is allowed.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from remote_implementation_control import canonical_json_bytes, sha256_bytes
from remote_implementation_io import Stop, git_show_bytes
from remote_implementation_release_readiness import verify_release_readiness_authority
from remote_implementation_presentation_refresh import (
    ASSET_PATH, git, presentation_refresh_tree_plan,
    verify_presentation_successor,
)

PREPARED_KIND = "REMOTE_IMPLEMENTATION_PRESENTATION_REFRESH_PREPARED_V1"


def require(ok: bool, code: str) -> None:
    if not ok:
        raise Stop(code)


def authenticate_presentation_preflight(
    request: dict[str, Any], control_head: str, *, repo: Path,
) -> dict[str, Any]:
    """Prove existing sealed apply and approved site blob before any commit."""
    repo = Path(repo)
    require(
        request.get("operation") == "RELEASE_PRESENTATION_REFRESH",
        "PRESENTATION_PREFLIGHT_OPERATION_INVALID",
    )
    require(
        request.get("repair_main_sha") == request.get("expected_protected_main_sha"),
        "PRESENTATION_PREFLIGHT_SOURCE_MAIN_MISMATCH",
    )
    # This permanent authenticator re-proves original Gate 1, seal, apply,
    # the approved release manifest, and the currently untouched sealed ref.
    original = verify_release_readiness_authority(
        request, control_head, source_repo=repo,
    )
    require(
        original["target_sha"] == request["target_sha"],
        "PRESENTATION_PREFLIGHT_TARGET_MISMATCH",
    )
    ref = request["stage2_apply_successor"]
    payload = git_show_bytes(control_head, ref["path"], cwd=repo)
    require(
        sha256_bytes(payload) == ref["sha256"],
        "PRESENTATION_PREFLIGHT_SUCCESSOR_HASH_MISMATCH",
    )
    successor = json.loads(payload)
    require(
        successor.get("kind") == "REMOTE_IMPLEMENTATION_STAGE2_SEALED_APPLY_SUCCESSOR"
        and successor.get("actual_published_target_sha") == request["target_sha"]
        and successor.get("prepared_tree_sha") == request["sealed_tree_sha"]
        and successor.get("approved_plan_hash") == request["approved_plan_hash"]
        and successor.get("release_manifest_sha256") == request["release_manifest_sha256"],
        "PRESENTATION_PREFLIGHT_ORIGINAL_SEAL_MISMATCH",
    )
    plan = presentation_refresh_tree_plan(
        repo,
        sealed_commit_sha=request["target_sha"],
        repair_main_sha=request["repair_main_sha"],
        expected_sealed_tree_sha=request["sealed_tree_sha"],
        expected_asset_blob_sha=request["accepted_asset_blob_sha"],
    )
    require(
        plan["allowed_changed_paths"] == [ASSET_PATH],
        "PRESENTATION_PREFLIGHT_SCOPE_MISMATCH",
    )
    return {"plan": plan, "original_apply": original}


def prepare_presentation_successor(
    request: dict[str, Any], control_head: str, *, repo: Path,
) -> dict[str, Any]:
    """Create one unreferenced Git commit and verify its entire tree."""
    repo = Path(repo)
    proof = authenticate_presentation_preflight(request, control_head, repo=repo)
    plan = proof["plan"]
    prepared_sha = git(
        repo, "commit-tree", str(plan["candidate_tree_sha"]),
        "-p", request["target_sha"],
        "-m", "Guarded post-seal presentation-only refresh",
    )
    checked = verify_presentation_successor(
        repo,
        sealed_commit_sha=request["target_sha"],
        successor_sha=prepared_sha,
        repair_main_sha=request["repair_main_sha"],
        expected_sealed_tree_sha=request["sealed_tree_sha"],
        expected_asset_blob_sha=request["accepted_asset_blob_sha"],
    )
    require(
        checked["fresh_tree_equivalence"] == "PASS"
        and checked["successor_tree_sha"] == plan["candidate_tree_sha"],
        "PRESENTATION_PREFLIGHT_PREPARED_TREE_MISMATCH",
    )
    asset = git_show_bytes(prepared_sha, ASSET_PATH, cwd=repo)
    return {
        "kind": PREPARED_KIND,
        "school_key": request["school_key"],
        "target_branch": request["target_branch"],
        "expected_target_predecessor_sha": request["target_sha"],
        "prepared_parent_sha": request["target_sha"],
        "prepared_commit_sha": prepared_sha,
        "prepared_tree_sha": plan["candidate_tree_sha"],
        "changed_paths": [ASSET_PATH],
        "changed_file_sha256": {ASSET_PATH: sha256_bytes(asset)},
        "deleted_paths": [],
        "repair_main_sha": request["repair_main_sha"],
        "accepted_asset_blob_sha": request["accepted_asset_blob_sha"],
        "original_apply_successor_sha256": request["stage2_apply_successor"]["sha256"],
        "original_apply_verification_sha256": request["stage2_apply_verification"]["sha256"],
        "approved_plan_hash": request["approved_plan_hash"],
        "release_manifest_sha256": request["release_manifest_sha256"],
        "plan_sha256": sha256_bytes(canonical_json_bytes(plan)),
        "tracked_basketball_mutation": "NONE",
        "branch_published": False,
        "owner_gate_2_approved": False,
    }
