#!/usr/bin/env python3
"""Authenticate one fresh-verified remote sealed-apply successor for release.

This module is intentionally read-only with respect to tracked basketball and
GitHub refs. It does NOT open a PR, poll Preview, approve Gate 2, or merge.
The guarded remote runner will later checkpoint this proof before PR creation.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import release_school
from remote_implementation_control import sha256_bytes, school_data_target_kind
from remote_implementation_io import Stop, git, git_show_bytes, remote_head
from remote_implementation_stage2_apply import verify_prepared_sealed_apply
from remote_implementation_presentation_release_boundary import (
    verify_presentation_dual_release_boundary,
)

SUCCESSOR_KIND = "REMOTE_IMPLEMENTATION_STAGE2_SEALED_APPLY_SUCCESSOR"
VERIFICATION_KIND = "REMOTE_IMPLEMENTATION_STAGE2_SEALED_APPLY_VERIFICATION"
WRITEAHEAD_KIND = "REMOTE_IMPLEMENTATION_WRITEAHEAD"
PR_PACKET_KIND = "REMOTE_IMPLEMENTATION_RELEASE_PR_PACKET"
REQUIRED_SIDECARS = {
    "approved-plan.json",
    "release-manifest.json",
    "pr-body.md",
    "visual-qa.md",
    "integration-freeze.json",
    "seal-checkpoint-manifest.json",
    "seal-verification.json",
    "current-main-preseal.json",
}


def _require(value: bool, code: str) -> None:
    if not value:
        raise Stop(code)


def _bound_json(
    control_commit: str,
    ref: dict[str, str],
    *,
    source_repo: Path,
    label: str,
) -> tuple[dict[str, Any], bytes]:
    path = str(ref.get("path", ""))
    expected = ref.get("sha256")
    _require(
        path.startswith(".remote-implementation/")
        and not any(part in {".", ".."} for part in Path(path).parts)
        and len(str(expected or "")) == 64,
        "RELEASE_%s_REFERENCE_INVALID" % label,
    )
    data = git_show_bytes(control_commit, path, cwd=source_repo)
    _require(sha256_bytes(data) == expected, "RELEASE_%s_HASH_MISMATCH" % label)
    try:
        document = json.loads(data)
    except (ValueError, UnicodeDecodeError) as exc:
        raise Stop("RELEASE_%s_JSON_INVALID" % label) from exc
    _require(isinstance(document, dict), "RELEASE_%s_OBJECT_REQUIRED" % label)
    return document, data


def _matching(document: dict[str, Any], fields: dict[str, Any], label: str) -> None:
    for key, expected in fields.items():
        _require(document.get(key) == expected, "RELEASE_%s_%s_MISMATCH" % (label, key.upper()))


def _verify_sealed_release_readiness_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path,
    published_head_sha: str | None = None,
) -> dict[str, Any]:
    """Bind request, prior write-ahead, successor, verification and sealed bytes."""
    school = request["school_key"]
    branch = str(request.get("target_branch") or "")
    target = request["target_sha"]
    _require(
        school_data_target_kind(school, branch) is not None,
        "RELEASE_TARGET_BRANCH_INVALID",
    )
    successor_ref = request["stage2_apply_successor"]
    verify_ref = request["stage2_apply_verification"]
    successor, successor_bytes = _bound_json(
        control_commit, successor_ref, source_repo=source_repo, label="SUCCESSOR"
    )
    verification, verification_bytes = _bound_json(
        control_commit, verify_ref, source_repo=source_repo, label="VERIFICATION"
    )
    _matching(
        successor,
        {
            "kind": SUCCESSOR_KIND,
            "operation": "STAGE2_SEALED_APPLY",
            "school_key": school,
            "target_branch": branch,
            "actual_published_target_sha": target,
            "prepared_commit_sha": target,
            "protected_main_sha": successor.get("protected_main_sha"),
            "approved_plan_hash": request["approved_plan_hash"],
            "release_manifest_sha256": request["release_manifest_sha256"],
            "repository_validation": "PASS",
            "final_transaction_state": "COMPLETE",
        },
        "SUCCESSOR",
    )
    # Historical/apply authority stays anchored to its original protected main.
    # Tooling productionization advances current main without invalidating it.
    # Require genuine ancestry rather than pretending the two SHAs are equal.
    original_main = successor["protected_main_sha"]
    current_main = request["expected_protected_main_sha"]
    _require(
        git(
            "merge-base", "--is-ancestor", original_main, current_main,
            cwd=source_repo, check=False,
        ).returncode == 0,
        "RELEASE_CURRENT_MAIN_NOT_DESCENDANT_OF_APPLY_MAIN",
    )
    apply_id = successor["request_id"]
    prefix = ".remote-implementation/successors/%s/%s" % (school, apply_id)
    _require(
        successor_ref["path"] == prefix + "/successor-manifest.json",
        "RELEASE_SUCCESSOR_PATH_INVALID",
    )
    expected_vpath = (
        ".remote-implementation/verifications/%s/%s/"
        "stage2-sealed-apply-verification.json" % (school, apply_id)
    )
    _require(verify_ref["path"] == expected_vpath, "RELEASE_VERIFICATION_PATH_INVALID")
    _matching(
        verification,
        {
            "kind": VERIFICATION_KIND,
            "school_key": school,
            "request_id": apply_id,
            "target_branch": branch,
            "target_sha": target,
            "protected_main_sha": successor["protected_main_sha"],
            "approved_plan_hash": request["approved_plan_hash"],
            "release_manifest_sha256": request["release_manifest_sha256"],
            "remote_stage2_sealed_apply_equivalence": "PASS",
            "tracked_stage2_mutation": "EXACT_SEALED_APPLY_SUCCESSOR",
            "target_predecessor_sha": successor["expected_target_predecessor_sha"],
            "target_tree_sha": successor["prepared_tree_sha"],
            "fresh_replayed_tree_sha": successor["prepared_tree_sha"],
            "changed_paths": successor["changed_paths"],
            "changed_file_sha256": successor["changed_file_sha256"],
            "deleted_paths": successor["deleted_paths"],
        },
        "VERIFICATION",
    )
    writeahead_ref = {
        "path": successor["writeahead_manifest_path"],
        "sha256": successor["writeahead_manifest_sha256"],
    }
    expected_wpath = ".remote-implementation/writeahead/%s/%s/writeahead-manifest.json" % (
        school, apply_id
    )
    _require(writeahead_ref["path"] == expected_wpath, "RELEASE_WRITEAHEAD_PATH_INVALID")
    writeahead, writeahead_bytes = _bound_json(
        control_commit, writeahead_ref, source_repo=source_repo, label="WRITEAHEAD"
    )
    _matching(
        writeahead,
        {
            "kind": WRITEAHEAD_KIND,
            "operation": "STAGE2_SEALED_APPLY",
            "school_key": school,
            "request_id": apply_id,
            "target_branch": branch,
            "protected_main_sha": successor["protected_main_sha"],
            "prepared_commit_sha": target,
            "prepared_tree_sha": successor["prepared_tree_sha"],
            "expected_target_predecessor_sha": successor["expected_target_predecessor_sha"],
            "changed_paths": successor["changed_paths"],
            "changed_file_sha256": successor["changed_file_sha256"],
            "deleted_paths": successor["deleted_paths"],
            "approved_plan_hash": request["approved_plan_hash"],
            "release_manifest_sha256": request["release_manifest_sha256"],
        },
        "WRITEAHEAD",
    )
    _require(
        writeahead.get("prepared_parent_sha") == successor["prepared_parent_sha"]
        == successor["expected_target_predecessor_sha"],
        "RELEASE_PREPARED_PARENT_MISMATCH",
    )
    sidecar_hashes = writeahead.get("sidecars", {})
    _require(
        isinstance(sidecar_hashes, dict)
        and REQUIRED_SIDECARS.issubset(set(sidecar_hashes)),
        "RELEASE_REQUIRED_SIDECARS_MISSING",
    )
    sidecars: dict[str, bytes] = {}
    source_prefix = Path(writeahead_ref["path"]).parent
    for name, expected in sidecar_hashes.items():
        _require(
            name in REQUIRED_SIDECARS and len(str(expected)) == 64,
            "RELEASE_UNEXPECTED_SIDECAR",
        )
        data = git_show_bytes(
            control_commit, (source_prefix / name).as_posix(), cwd=source_repo
        )
        _require(sha256_bytes(data) == expected, "RELEASE_SIDECAR_HASH_MISMATCH:" + name)
        sidecars[name] = data
    _require(
        sha256_bytes(sidecars["release-manifest.json"])
        == request["release_manifest_sha256"],
        "RELEASE_MANIFEST_SHA_MISMATCH",
    )
    _require(
        sha256_bytes(sidecars["approved-plan.json"])
        == successor["approved_plan_sha256"],
        "RELEASE_APPROVED_PLAN_FILE_MISMATCH",
    )
    manifest = json.loads(sidecars["release-manifest.json"])
    approved = json.loads(sidecars["approved-plan.json"])
    _matching(
        manifest,
        {
            "school_key": school,
            # The sealed apply manifest was produced in a disposable runner
            # worktree. Its 'branch' is not the published target Git ref.
            "base_commit": successor["expected_target_predecessor_sha"],
            "approved_plan_hash": request["approved_plan_hash"],
            "changed_paths": successor["changed_paths"],
        },
        "MANIFEST",
    )
    _matching(
        approved,
        {"school_key": school, "approved_plan_hash": request["approved_plan_hash"]},
        "APPROVED",
    )
    _require(
        remote_head(source_repo, branch) == (
            published_head_sha if published_head_sha is not None else target
        ),
        "RELEASE_TARGET_MOVED",
    )
    # The existing sealed-apply verifier is the canonical prepared-parent/tree,
    # exact changed-path, hash, and deletion proof.
    prepared = verify_prepared_sealed_apply(
        source_repo,
        predecessor_sha=successor["expected_target_predecessor_sha"],
        prepared_sha=target,
        changed_paths=successor["changed_paths"],
        changed_file_sha256=successor["changed_file_sha256"],
        deleted_paths=successor["deleted_paths"],
    )
    _require(
        prepared["prepared_tree_sha"] == successor["prepared_tree_sha"],
        "RELEASE_PREPARED_TREE_MISMATCH",
    )
    return {
        "school_key": school,
        "target_branch": branch,
        "target_sha": target,
        "apply_request_id": apply_id,
        "successor_sha256": sha256_bytes(successor_bytes),
        "verification_sha256": sha256_bytes(verification_bytes),
        "writeahead_sha256": sha256_bytes(writeahead_bytes),
        "protected_main_sha": request["expected_protected_main_sha"],
        "apply_protected_main_sha": original_main,
        "approved_plan_hash": request["approved_plan_hash"],
        "release_manifest_sha256": request["release_manifest_sha256"],
        "changed_path_count": len(successor["changed_paths"]),
        "changed_paths": successor["changed_paths"],
        "original_apply_file_hashes": successor["changed_file_sha256"],
        "original_apply_deleted_paths": successor["deleted_paths"],
        "sidecars": sidecars,
        "manifest": manifest,
        "approved": approved,
    }


def verify_release_readiness_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path,
) -> dict[str, Any]:
    """Keep ordinary G unchanged; demand an authenticated G+C proof for C."""
    succ_ref = request.get("presentation_refresh_successor")
    fresh_ref = request.get("presentation_refresh_verification")
    _require(
        (succ_ref is None) == (fresh_ref is None),
        "RELEASE_PRESENTATION_REFERENCES_MUST_BE_PAIRED",
    )
    if succ_ref is None:
        return _verify_sealed_release_readiness_authority(
            request, control_commit, source_repo=source_repo,
        )

    school = request["school_key"]
    branch = request["target_branch"]
    target = request["target_sha"]
    successor, _ = _bound_json(
        control_commit, succ_ref, source_repo=source_repo,
        label="PRESENTATION_SUCCESSOR",
    )
    fresh, _ = _bound_json(
        control_commit, fresh_ref, source_repo=source_repo,
        label="PRESENTATION_VERIFICATION",
    )
    rid = successor.get("request_id")
    _require(
        isinstance(rid, str) and rid
        and succ_ref["path"] ==
          ".remote-implementation/successors/%s/%s/successor-manifest.json" %
          (school, rid)
        and fresh_ref["path"] ==
          ".remote-implementation/verifications/%s/%s/"
          "presentation-refresh-verification.json" % (school, rid),
        "RELEASE_PRESENTATION_REFERENCE_PATH_MISMATCH",
    )
    sealed_sha = successor.get("expected_target_predecessor_sha")
    _require(
        isinstance(sealed_sha, str) and len(sealed_sha) == 40
        and sealed_sha != target,
        "RELEASE_PRESENTATION_ORIGINAL_SEAL_MISSING",
    )
    _matching(successor, {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_PRESENTATION_REFRESH_SUCCESSOR",
        "operation": "RELEASE_PRESENTATION_REFRESH",
        "school_key": school,
        "target_branch": branch,
        "prepared_parent_sha": sealed_sha,
        "prepared_commit_sha": target,
        "actual_published_target_sha": target,
        "changed_paths": ["site/index.html"],
        "deleted_paths": [],
        "approved_plan_hash": request["approved_plan_hash"],
        "release_manifest_sha256": request["release_manifest_sha256"],
        "stage2_apply_successor": request["stage2_apply_successor"],
        "stage2_apply_verification": request["stage2_apply_verification"],
        "repository_validation": "PASS",
        "tracked_basketball_mutation": "NONE",
        "owner_gate_2_approved": False,
        "final_transaction_state": "COMPLETE",
    }, "PRESENTATION_SUCCESSOR")
    _matching(fresh, {
        "kind": "REMOTE_IMPLEMENTATION_PRESENTATION_REFRESH_FRESH_PROOF",
        "request_id": rid,
        "school_key": school,
        "original_sealed_sha": sealed_sha,
        "successor_sha": target,
        "successor_tree_sha": successor.get("prepared_tree_sha"),
        "protected_main_sha": successor.get("protected_main_sha"),
        "accepted_asset_blob_sha": successor.get("accepted_asset_blob_sha"),
        "changed_paths": ["site/index.html"],
        "original_sealed_apply_equivalence": "PASS",
        "fresh_presentation_tree_equivalence": "PASS",
        "branch_published_exact": True,
        "owner_gate_2_approved": False,
    }, "PRESENTATION_VERIFICATION")
    _require(
        remote_head(source_repo, branch) == target,
        "RELEASE_PRESENTATION_TARGET_MOVED",
    )
    original_main = successor.get("repair_main_sha")
    current_main = request["expected_protected_main_sha"]
    _require(
        git(
            "merge-base", "--is-ancestor", original_main, current_main,
            cwd=source_repo, check=False,
        ).returncode == 0,
        "RELEASE_PRESENTATION_SOURCE_NOT_CURRENT_MAIN_ANCESTOR",
    )
    _require(
        git(
            "rev-parse", current_main + ":site/index.html",
            cwd=source_repo,
        ).stdout.strip() == successor.get("accepted_asset_blob_sha"),
        "RELEASE_PRESENTATION_ACCEPTED_BLOB_DRIFT",
    )
    # Reconstruct the full original Stage 2 sealed-release sidecars and hash
    # evidence with G as target; the real branch MUST remain at C throughout.
    sealed_request = dict(request)
    sealed_request["target_sha"] = sealed_sha
    original = _verify_sealed_release_readiness_authority(
        sealed_request, control_commit, source_repo=source_repo,
        published_head_sha=target,
    )
    _require(
        original["target_sha"] == sealed_sha
        and original["approved_plan_hash"] == request["approved_plan_hash"]
        and original["release_manifest_sha256"] == request["release_manifest_sha256"],
        "RELEASE_PRESENTATION_ORIGINAL_AUTHORITY_MISMATCH",
    )
    # Exact parent and complete-tree replay, independent of the original
    # manifest's seven-file historical apply and its sealed-only validator.
    # This check can run without a school worktree; full clean-HEAD verification
    # follows inside run_permanent_release_readiness.
    from remote_implementation_presentation_refresh import (
        PresentationRefreshStop, verify_presentation_successor,
    )
    try:
        tree_proof = verify_presentation_successor(
            source_repo,
            sealed_commit_sha=sealed_sha,
            successor_sha=target,
            repair_main_sha=original_main,
            expected_sealed_tree_sha=successor["sealed_tree_sha"],
            expected_asset_blob_sha=successor["accepted_asset_blob_sha"],
        )
    except PresentationRefreshStop as exc:
        raise Stop("RELEASE_PRESENTATION_TREE_REPLAY:" + str(exc)) from exc
    _require(
        tree_proof["successor_tree_sha"] == successor["prepared_tree_sha"],
        "RELEASE_PRESENTATION_SUCCESSOR_TREE_MISMATCH",
    )
    original["target_sha"] = target
    original["changed_paths"] = sorted(
        set(original["changed_paths"]) | {"site/index.html"}
    )
    original["changed_path_count"] = len(original["changed_paths"])
    original["presentation_refresh"] = {
        "successor_ref": succ_ref,
        "fresh_verification_ref": fresh_ref,
        "original_sealed_sha": sealed_sha,
        "original_sealed_tree_sha": successor["sealed_tree_sha"],
        "source_protected_main_sha": original_main,
        "accepted_site_blob_sha": successor["accepted_asset_blob_sha"],
        "presentation_successor_sha": target,
        "presentation_successor_tree_sha": successor["prepared_tree_sha"],
        "historical_apply_paths": original["manifest"]["changed_paths"],
        "fresh_presentation_tree_equivalence": "PASS",
        "owner_gate_2_approved": False,
    }
    return original


def build_release_pr_packet(
    authority: dict[str, Any],
    worktree: Path,
    *,
    readiness_request_id: str,
    preview_request_id: str,
    body_checkpoint_path: str,
) -> dict[str, Any]:
    """Build the exact connector-owned PR handoff after readiness."""

    body = authority["sidecars"]["pr-body.md"]
    display = release_school.program_display_name(
        worktree,
        authority["school_key"],
    )
    return {
        "schema_version": 1,
        "kind": PR_PACKET_KIND,
        "readiness_request_id": readiness_request_id,
        "preview_request_id": preview_request_id,
        "school_key": authority["school_key"],
        "base_branch": "main",
        "head_branch": authority["target_branch"],
        "head_sha": authority["target_sha"],
        "new_pr_title": f"Ingest and publish {display} history",
        "body_checkpoint_path": body_checkpoint_path,
        "body_sha256": sha256_bytes(body),
        "approved_plan_hash": authority["approved_plan_hash"],
        "release_manifest_sha256": authority["release_manifest_sha256"],
        "pr_created_by_runner": False,
        "owner_gate_2": False,
        "authority_statement": (
            "Exact connector-owned PR creation packet after fresh release "
            "readiness. The school Implementation lane may create or reuse only "
            "this exact head/base/body PR (using new_pr_title when creating a "
            "new PR), then queue the bound Preview "
            "verification request. This packet grants no Owner Gate 2, merge, "
            "Production, or tracked mutation authority."
        ),
    }


def run_permanent_release_readiness(
    authority: dict[str, Any],
    *,
    worktree: Path,
    artifact_dir: Path,
) -> dict[str, Any]:
    """Run unchanged permanent final gates with no GitHub or tracked write."""
    school = authority["school_key"]
    target = authority["target_sha"]
    manifest = authority["manifest"]
    _require(
        git("rev-parse", "HEAD", cwd=worktree).stdout.strip() == target,
        "RELEASE_READINESS_WORKTREE_HEAD_MISMATCH",
    )
    # Only ignored artifacts supplied by exact authenticated write-ahead are restored.
    artifact_dir.mkdir(parents=True, exist_ok=True)
    for name in (
        "release-manifest.json", "approved-plan.json", "pr-body.md",
        "visual-qa.md", "integration-freeze.json",
    ):
        (artifact_dir / name).write_bytes(authority["sidecars"][name])
    presentation = authority.get("presentation_refresh")
    if presentation is None:
        paths = release_school.verify_committed_change_boundary(
            worktree, manifest, target
        )
        dual_boundary = None
    else:
        # Never reinterpret the G manifest as a manifest for C. Independently
        # prove original G and the one-asset C overlay as separate boundaries.
        dual_boundary = verify_presentation_dual_release_boundary(
            worktree,
            school_key=school,
            original_release_manifest=manifest,
            approved_plan_hash=authority["approved_plan_hash"],
            original_apply_base_sha=manifest["base_commit"],
            original_sealed_sha=presentation["original_sealed_sha"],
            original_sealed_tree_sha=presentation["original_sealed_tree_sha"],
            original_changed_paths=manifest["changed_paths"],
            original_changed_file_sha256=authority["original_apply_file_hashes"],
            original_deleted_paths=authority["original_apply_deleted_paths"],
            presentation_successor_sha=target,
            source_protected_main_sha=presentation["source_protected_main_sha"],
            accepted_site_blob_sha=presentation["accepted_site_blob_sha"],
        )
        paths = dual_boundary["full_rehearsal_changed_paths"]
    release_school.run_gates(
        worktree,
        school,
        paths,
        include_tests=True,
        approved_plan=authority["approved"],
        **release_school.correction_gate_kwargs_from_manifest(manifest, school),
    )
    if presentation is None:
        release_school.verify_committed_change_boundary(worktree, manifest, target)
    else:
        second_proof = verify_presentation_dual_release_boundary(
            worktree,
            school_key=school,
            original_release_manifest=manifest,
            approved_plan_hash=authority["approved_plan_hash"],
            original_apply_base_sha=manifest["base_commit"],
            original_sealed_sha=presentation["original_sealed_sha"],
            original_sealed_tree_sha=presentation["original_sealed_tree_sha"],
            original_changed_paths=manifest["changed_paths"],
            original_changed_file_sha256=authority["original_apply_file_hashes"],
            original_deleted_paths=authority["original_apply_deleted_paths"],
            presentation_successor_sha=target,
            source_protected_main_sha=presentation["source_protected_main_sha"],
            accepted_site_blob_sha=presentation["accepted_site_blob_sha"],
        )
        _require(
            second_proof == dual_boundary,
            "RELEASE_PRESENTATION_GATE_REPLAY_DRIFT",
        )
    return {
        "kind": "REMOTE_IMPLEMENTATION_RELEASE_READINESS",
        "status": "RELEASE_READINESS_PASS",
        "school_key": school,
        "target_branch": authority["target_branch"],
        "target_sha": target,
        "protected_main_sha": authority["protected_main_sha"],
        "apply_protected_main_sha": authority["apply_protected_main_sha"],
        "apply_request_id": authority["apply_request_id"],
        "successor_sha256": authority["successor_sha256"],
        "verification_sha256": authority["verification_sha256"],
        "writeahead_sha256": authority["writeahead_sha256"],
        "approved_plan_hash": authority["approved_plan_hash"],
        "release_manifest_sha256": authority["release_manifest_sha256"],
        "changed_path_count": authority["changed_path_count"],
        "presentation_dual_boundary": (
            dual_boundary if presentation is not None else None
        ),
        "permanent_release_gates": "PASS",
        "tracked_mutation": "NONE",
        "pr_created": False,
        "preview_verified": False,
        "owner_gate_2": False,
    }
