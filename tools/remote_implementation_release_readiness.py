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
from remote_implementation_control import sha256_bytes
from remote_implementation_io import Stop, git, git_show_bytes, remote_head
from remote_implementation_stage2_apply import verify_prepared_sealed_apply

SUCCESSOR_KIND = "REMOTE_IMPLEMENTATION_STAGE2_SEALED_APPLY_SUCCESSOR"
VERIFICATION_KIND = "REMOTE_IMPLEMENTATION_STAGE2_SEALED_APPLY_VERIFICATION"
WRITEAHEAD_KIND = "REMOTE_IMPLEMENTATION_WRITEAHEAD"
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


def verify_release_readiness_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path,
) -> dict[str, Any]:
    """Bind request, prior write-ahead, successor, verification and sealed bytes."""
    school = request["school_key"]
    branch = "data/%s-onboarding" % school
    target = request["target_sha"]
    _require(request.get("target_branch") == branch, "RELEASE_TARGET_BRANCH_INVALID")
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
        remote_head(source_repo, branch) == target,
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
        "sidecars": sidecars,
        "manifest": manifest,
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
    for name in ("release-manifest.json", "approved-plan.json", "pr-body.md", "visual-qa.md"):
        (artifact_dir / name).write_bytes(authority["sidecars"][name])
    paths = release_school.verify_committed_change_boundary(
        worktree, manifest, target
    )
    release_school.run_gates(
        worktree,
        school,
        paths,
        include_tests=True,
        **release_school.correction_gate_kwargs_from_manifest(manifest, school),
    )
    release_school.verify_committed_change_boundary(worktree, manifest, target)
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
        "permanent_release_gates": "PASS",
        "tracked_mutation": "NONE",
        "pr_created": False,
        "preview_verified": False,
        "owner_gate_2": False,
    }
