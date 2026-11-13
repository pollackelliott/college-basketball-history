#!/usr/bin/env python3
"""Independent fresh verification of a completed guarded presentation refresh.

Does NOT approve a Preview or merge. Requires the immutable original Stage 2
apply proof and the newly published exact one-file presentation successor.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from remote_implementation_control import (
    OP_RELEASE_PRESENTATION_REFRESH, sha256_bytes,
    sha256_file, validate_control_state, verify_sidecar_hashes,
)
from remote_implementation_io import (
    ROOT, STATE_PATH, Stop, commit_control,
    git, git_show_bytes, read_json, remote_head, write_json,
)
from remote_implementation_presentation_refresh import (
    ASSET_PATH, verify_presentation_successor,
)
from remote_implementation_presentation_publish import (
    SUCCESSOR_KIND, validate_presentation_intent,
)
from remote_implementation_stage2_apply import verify_prepared_sealed_apply


def require(ok: bool, code: str) -> None:
    if not ok:
        raise Stop(code)


def bound_doc(control_head: str, reference: dict[str, Any], *, repo: Path) -> dict:
    content = git_show_bytes(control_head, reference["path"], cwd=repo)
    require(
        sha256_bytes(content) == reference["sha256"],
        "PRESENTATION_FRESH_BOUND_DOC_HASH_MISMATCH",
    )
    return json.loads(content)


def inspect_presentation_checkpoint(
    live_main: str, control_head: str, state: dict,
    *, repo: Path = ROOT,
) -> dict[str, Any]:
    """No writes: reconstruct original sealed and new presentation tree proofs."""
    last = state.get("last_operation") or {}
    require(
        last.get("operation") == OP_RELEASE_PRESENTATION_REFRESH
        and last.get("fresh_runner_verification") in {"PENDING", "PASS"},
        "PRESENTATION_FRESH_OPERATION_NOT_READY",
    )
    successor = bound_doc(
        control_head, {
            "path": last["successor_manifest_path"],
            "sha256": last["successor_manifest_sha256"],
        }, repo=repo,
    )
    require(
        successor.get("kind") == SUCCESSOR_KIND
        and successor.get("operation") == OP_RELEASE_PRESENTATION_REFRESH
        and successor.get("request_id") == last.get("request_id")
        and successor.get("target_branch") == last.get("target_branch")
        and successor.get("prepared_commit_sha") == last.get("target_sha")
        and successor.get("prepared_tree_sha") == last.get("prepared_tree_sha")
        and successor.get("actual_published_target_sha") == last.get("target_sha")
        and successor.get("expected_target_predecessor_sha")
            == last.get("original_sealed_sha")
        and successor.get("owner_gate_2_approved") is False
        and successor.get("tracked_basketball_mutation") == "NONE"
        and successor.get("final_transaction_state") == "COMPLETE"
        and successor.get("repository_validation") == "PASS"
        and successor.get("protected_main_sha") == live_main,
        "PRESENTATION_FRESH_SUCCESSOR_AUTHORITY_MISMATCH",
    )
    require(
        remote_head(repo, successor["target_branch"]) == successor["prepared_commit_sha"],
        "PRESENTATION_FRESH_REMOTE_TARGET_MISMATCH",
    )
    # A fresh checkout may not have fetched the unpublished-to-main C object.
    # Fetch the exact remote target before inspecting any candidate Git tree.
    git(
        "fetch", "--no-tags", "origin",
        "+refs/heads/%s:refs/remotes/origin/presentation-refresh-target"
        % successor["target_branch"], cwd=repo,
    )
    require(
        git(
            "rev-parse", "refs/remotes/origin/presentation-refresh-target",
            cwd=repo,
        ).stdout.strip() == successor["prepared_commit_sha"],
        "PRESENTATION_FRESH_FETCHED_TARGET_CHANGED",
    )
    request_bytes = git_show_bytes(
        control_head,
        ".remote-implementation/requests/%s/request.json" % successor["request_id"],
        cwd=repo,
    )
    require(
        sha256_bytes(request_bytes) == successor["request_sha256"],
        "PRESENTATION_FRESH_REQUEST_HASH_MISMATCH",
    )
    request = json.loads(request_bytes)
    require(
        request["operation"] == OP_RELEASE_PRESENTATION_REFRESH
        and request["target_branch"] == successor["target_branch"]
        and request["target_sha"] == successor["expected_target_predecessor_sha"]
        and request["repair_main_sha"] == live_main
        and request["expected_protected_main_sha"] == live_main
        and request["sealed_tree_sha"] == successor["sealed_tree_sha"]
        and request["accepted_asset_blob_sha"] == successor["accepted_asset_blob_sha"]
        and request["approved_plan_hash"] == successor["approved_plan_hash"]
        and request["release_manifest_sha256"] == successor["release_manifest_sha256"]
        and request["stage2_apply_successor"] == successor["stage2_apply_successor"]
        and request["stage2_apply_verification"] == successor["stage2_apply_verification"],
        "PRESENTATION_FRESH_REQUEST_SUCCESSOR_SCOPE_MISMATCH",
    )
    manifest = bound_doc(
        control_head, {
            "path": successor["writeahead_manifest_path"],
            "sha256": successor["writeahead_manifest_sha256"],
        }, repo=repo,
    )
    require(
        manifest.get("request_sha256") == successor["request_sha256"]
        and manifest.get("global_lock_commit") == successor["global_lock_commit"]
        and manifest.get("protected_main_sha") == live_main
        and manifest.get("prepared_commit_sha") == successor["prepared_commit_sha"]
        and manifest.get("prepared_tree_sha") == successor["prepared_tree_sha"]
        and manifest.get("changed_file_sha256") == successor["changed_file_sha256"]
        and manifest.get("approved_plan_hash") == request["approved_plan_hash"],
        "PRESENTATION_FRESH_WRITEAHEAD_SUCCESSOR_MISMATCH",
    )
    sidecars = manifest.get("sidecars")
    require(
        isinstance(sidecars, dict) and set(sidecars) == {"prepared-proof.json"},
        "PRESENTATION_FRESH_WRONG_SIDECARS",
    )
    proof_path = str(Path(successor["writeahead_manifest_path"]).parent / "prepared-proof.json")
    proof_bytes = git_show_bytes(control_head, proof_path, cwd=repo)
    require(
        sha256_bytes(proof_bytes) == sidecars["prepared-proof.json"],
        "PRESENTATION_FRESH_PREPARED_PROOF_HASH_MISMATCH",
    )
    saved_proof = json.loads(proof_bytes)
    require(
        saved_proof.get("prepared_commit_sha") == successor["prepared_commit_sha"]
        and saved_proof.get("prepared_tree_sha") == successor["prepared_tree_sha"]
        and saved_proof.get("branch_published") is False
        and saved_proof.get("owner_gate_2_approved") is False
        and saved_proof.get("tracked_basketball_mutation") == "NONE",
        "PRESENTATION_FRESH_PREPARED_PROOF_SCOPE_MISMATCH",
    )
    # Independently regenerate complete exact child tree/blob from Git objects.
    checked = validate_presentation_intent(request, manifest, repo=repo)
    require(
        checked["successor_sha"] == successor["prepared_commit_sha"]
        and checked["successor_tree_sha"] == successor["prepared_tree_sha"]
        and checked["sealed_parent"] == request["target_sha"],
        "PRESENTATION_FRESH_TREE_NOT_EQUIVALENT",
    )
    original = bound_doc(
        control_head, request["stage2_apply_successor"], repo=repo,
    )
    original_v = bound_doc(
        control_head, request["stage2_apply_verification"], repo=repo,
    )
    require(
        original.get("kind") == "REMOTE_IMPLEMENTATION_STAGE2_SEALED_APPLY_SUCCESSOR"
        and original.get("actual_published_target_sha") == request["target_sha"]
        and original.get("prepared_tree_sha") == request["sealed_tree_sha"]
        and original.get("approved_plan_hash") == request["approved_plan_hash"]
        and original.get("release_manifest_sha256") == request["release_manifest_sha256"]
        and original.get("final_transaction_state") == "COMPLETE"
        and original_v.get("remote_stage2_sealed_apply_equivalence") == "PASS"
        and original_v.get("target_sha") == request["target_sha"]
        and original_v.get("target_tree_sha") == request["sealed_tree_sha"],
        "PRESENTATION_FRESH_ORIGINAL_SEALED_AUTHORITY_MISMATCH",
    )
    # Recheck original sealed apply's exact original parent, path manifest and
    # per-file content SHA against real Git objects. The historical seal is
    # reauthenticated pre-publication; it is never rewritten here.
    original_proof = verify_prepared_sealed_apply(
        repo,
        predecessor_sha=original["expected_target_predecessor_sha"],
        prepared_sha=request["target_sha"],
        changed_paths=original["changed_paths"],
        changed_file_sha256=original["changed_file_sha256"],
        deleted_paths=original["deleted_paths"],
    )
    require(
        original_proof["prepared_tree_sha"] == request["sealed_tree_sha"],
        "PRESENTATION_FRESH_ORIGINAL_APPLY_TREE_MISMATCH",
    )
    return {
        "kind": "REMOTE_IMPLEMENTATION_PRESENTATION_REFRESH_FRESH_PROOF",
        "request_id": request["request_id"],
        "school_key": request["school_key"],
        "original_sealed_sha": request["target_sha"],
        "successor_sha": successor["prepared_commit_sha"],
        "successor_tree_sha": successor["prepared_tree_sha"],
        "protected_main_sha": live_main,
        "accepted_asset_blob_sha": request["accepted_asset_blob_sha"],
        "changed_paths": [ASSET_PATH],
        "original_sealed_apply_equivalence": "PASS",
        "fresh_presentation_tree_equivalence": "PASS",
        "branch_published_exact": True,
        "owner_gate_2_approved": False,
    }


def verify_presentation_refresh_equivalence(
    live_main: str, control_head: str, state: dict,
    *, repo: Path = ROOT,
) -> int:
    last = state.get("last_operation") or {}
    if last.get("fresh_runner_verification") == "PASS":
        # As with the other remote fresh verifiers, a previous verified state
        # remains durable and may be reused only with identical control head.
        print("REMOTE PRESENTATION REFRESH EQUIVALENCE: PASS (already verified)")
        return 0
    fresh = inspect_presentation_checkpoint(
        live_main, control_head, state, repo=repo,
    )
    directory = Path(
        ".remote-implementation/verifications/%s/%s" % (
            fresh["school_key"], fresh["request_id"]
        )
    )
    write_json(directory / "presentation-refresh-verification.json", fresh)
    local = read_json(STATE_PATH)
    validate_control_state(local)
    previous = local.get("last_operation") or {}
    require(
        previous.get("operation") == OP_RELEASE_PRESENTATION_REFRESH
        and previous.get("request_id") == fresh["request_id"]
        and previous.get("target_sha") == fresh["successor_sha"]
        and previous.get("fresh_runner_verification") == "PENDING",
        "PRESENTATION_FRESH_CONTROL_MOVED",
    )
    previous["fresh_runner_verification"] = "PASS"
    previous["remote_presentation_refresh_equivalence"] = "PASS"
    previous["fresh_verification_path"] = (
        directory / "presentation-refresh-verification.json"
    ).as_posix()
    previous["fresh_verification_sha256"] = sha256_file(
        directory / "presentation-refresh-verification.json"
    )
    local["last_operation"] = previous
    write_json(STATE_PATH, local)
    result = commit_control(
        control_head,
        "persist fresh post-seal presentation refresh verification %s"
        % fresh["request_id"],
        [STATE_PATH, directory],
    )
    print("REMOTE PRESENTATION REFRESH EQUIVALENCE: PASS commit=%s" % result)
    return 0
