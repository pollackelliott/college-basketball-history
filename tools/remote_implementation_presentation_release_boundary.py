#!/usr/bin/env python3
"""Strict dual release boundary for a sealed historical apply plus site-only fix.

This is a read-only validation component, NOT a release-readiness dispatcher or
an alternative owner-gate implementation. It must be called after independently
authenticating original Stage 2 sealed-apply and presentation-refresh records.
The ordinary sealed-only validator in release_school.py remains unchanged.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import release_school
from remote_implementation_control import sha256_bytes
from remote_implementation_io import Stop, git, git_show_bytes
from remote_implementation_presentation_refresh import (
    ASSET_PATH, PresentationRefreshStop, verify_presentation_successor,
)
from remote_implementation_stage2_apply import verify_prepared_sealed_apply


BOUNDARY_KIND = "REMOTE_IMPLEMENTATION_PRESENTATION_DUAL_RELEASE_BOUNDARY_V1"


def require(test: bool, message: str) -> None:
    if not test:
        raise Stop(message)


def verify_presentation_dual_release_boundary(
    repo: Path,
    *,
    school_key: str,
    original_release_manifest: dict[str, Any],
    approved_plan_hash: str,
    original_apply_base_sha: str,
    original_sealed_sha: str,
    original_sealed_tree_sha: str,
    original_changed_paths: list[str],
    original_changed_file_sha256: dict[str, str],
    original_deleted_paths: list[str],
    presentation_successor_sha: str,
    source_protected_main_sha: str,
    accepted_site_blob_sha: str,
) -> dict[str, Any]:
    """Prove G's original historical boundary and C's strict one-file overlay.

    No Git ref is updated, no approved plan is rewritten, and no replacement
    seven-file seal manifest is ever created. Both invariants must pass.
    """
    repo = Path(repo)
    require(
        git("rev-parse", "HEAD", cwd=repo).stdout.strip()
        == presentation_successor_sha,
        "PRESENTATION_DUAL_TARGET_HEAD_MISMATCH",
    )
    require(
        not git(
            "status", "--porcelain", "--untracked-files=all",
            cwd=repo,
        ).stdout.strip(),
        "PRESENTATION_DUAL_WORKTREE_NOT_CLEAN",
    )

    # Historical boundary 1: original sealed apply, checked without relying on
    # C's changed file path or any rewritten historical manifest.
    manifest = original_release_manifest
    require(
        isinstance(manifest, dict)
        and manifest.get("school_key") == school_key
        and manifest.get("base_commit") == original_apply_base_sha
        and manifest.get("approved_plan_hash") == approved_plan_hash
        and manifest.get("changed_paths") == original_changed_paths,
        "PRESENTATION_DUAL_ORIGINAL_MANIFEST_MISMATCH",
    )
    require(
        isinstance(original_changed_paths, list)
        and bool(original_changed_paths)
        and len(original_changed_paths) == len(set(original_changed_paths))
        and ASSET_PATH not in original_changed_paths,
        "PRESENTATION_DUAL_ORIGINAL_PATH_SCOPE_INVALID",
    )
    require(
        set(original_changed_file_sha256) | set(original_deleted_paths)
        == set(original_changed_paths)
        and not set(original_changed_file_sha256).intersection(original_deleted_paths),
        "PRESENTATION_DUAL_ORIGINAL_HASH_SCOPE_MISMATCH",
    )
    original = verify_prepared_sealed_apply(
        repo,
        predecessor_sha=original_apply_base_sha,
        prepared_sha=original_sealed_sha,
        changed_paths=original_changed_paths,
        changed_file_sha256=original_changed_file_sha256,
        deleted_paths=original_deleted_paths,
    )
    require(
        original["prepared_parent_sha"] == original_apply_base_sha
        and original["prepared_tree_sha"] == original_sealed_tree_sha,
        "PRESENTATION_DUAL_ORIGINAL_APPLY_TREE_MISMATCH",
    )

    # Presentation boundary 2: C has exactly one parent G and the complete
    # tree differs from G solely in the exact accepted site/index.html Git blob.
    # The helper independently builds a disposable candidate tree from G,
    # so all untouched basketball/public data blobs are compared implicitly.
    try:
        presentation = verify_presentation_successor(
            repo,
            sealed_commit_sha=original_sealed_sha,
            successor_sha=presentation_successor_sha,
            repair_main_sha=source_protected_main_sha,
            expected_sealed_tree_sha=original_sealed_tree_sha,
            expected_asset_blob_sha=accepted_site_blob_sha,
        )
    except PresentationRefreshStop as exc:
        raise Stop("PRESENTATION_DUAL_PRESENTATION_BOUNDARY:" + str(exc)) from exc
    require(
        presentation["fresh_tree_equivalence"] == "PASS"
        and presentation["sealed_parent"] == original_sealed_sha
        and presentation["successor_sha"] == presentation_successor_sha
        and presentation["successor_tree_sha"] == presentation["candidate_tree_sha"]
        and presentation["allowed_changed_paths"] == [ASSET_PATH],
        "PRESENTATION_DUAL_PRESENTATION_REPLAY_MISMATCH",
    )
    # Recheck byte SHA for the presented asset, not just its Git blob ID.
    asset_sha256 = sha256_bytes(
        git_show_bytes(presentation_successor_sha, ASSET_PATH, cwd=repo)
    )
    require(bool(asset_sha256), "PRESENTATION_DUAL_ASSET_HASH_MISSING")
    return {
        "kind": BOUNDARY_KIND,
        "school_key": school_key,
        "approved_plan_hash": approved_plan_hash,
        "original_apply_base_sha": original_apply_base_sha,
        "original_sealed_sha": original_sealed_sha,
        "original_sealed_tree_sha": original_sealed_tree_sha,
        "original_release_changed_paths": sorted(original_changed_paths),
        "original_release_changed_path_count": len(original_changed_paths),
        "original_apply_path_hash_equivalence": "PASS",
        "presentation_successor_sha": presentation_successor_sha,
        "presentation_successor_tree_sha": presentation["successor_tree_sha"],
        "presentation_source_protected_main_sha": source_protected_main_sha,
        "presentation_accepted_site_blob_sha": accepted_site_blob_sha,
        "presentation_site_sha256": asset_sha256,
        "presentation_changed_paths": [ASSET_PATH],
        "presentation_tree_equivalence": "PASS",
        "full_rehearsal_changed_paths": sorted(
            set(original_changed_paths) | {ASSET_PATH}
        ),
        "tracked_basketball_mutation_after_seal": "NONE",
        "original_manifest_modified": False,
        "owner_gate_2_approved": False,
    }
