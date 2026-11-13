#!/usr/bin/env python3
"""Guarded post-seal website-asset refresh for an existing Implementation lane.

The only permitted tracked delta is the exact accepted protected-main blob for
site/index.html, placed as a direct child of the original sealed-apply commit.
This transaction does not approve Owner Gate 2, produce Preview or merge a PR.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from remote_implementation_control import (
    OP_RELEASE_PRESENTATION_REFRESH,
    begin_request, bind_lock_commit, finalize_success,
    publish_ref_cas, sha256_bytes, sha256_file,
)
from remote_implementation_io import (
    ROOT, STATE_PATH, Stop, assert_protected_main_unchanged,
    commit_control, git_show_bytes, remote_head, write_json,
)
from remote_implementation_presentation_refresh import (
    ASSET_PATH, PresentationRefreshStop, verify_presentation_successor,
)
from remote_implementation_presentation_transaction import (
    PREPARED_KIND, prepare_presentation_successor,
)

SUCCESSOR_KIND = "REMOTE_IMPLEMENTATION_PRESENTATION_REFRESH_SUCCESSOR"
WRITEAHEAD_KIND = "REMOTE_IMPLEMENTATION_WRITEAHEAD"


def require(ok: bool, code: str) -> None:
    if not ok:
        raise Stop(code)


def verify_committed_presentation(
    request: dict[str, Any], candidate_sha: str, *, repo: Path,
) -> dict[str, object]:
    try:
        return verify_presentation_successor(
            repo,
            sealed_commit_sha=request["target_sha"],
            successor_sha=candidate_sha,
            repair_main_sha=request["repair_main_sha"],
            expected_sealed_tree_sha=request["sealed_tree_sha"],
            expected_asset_blob_sha=request["accepted_asset_blob_sha"],
        )
    except PresentationRefreshStop as exc:
        # The remote runner's STOP boundary uses the permanent Stop class.
        # A tampered published commit must fail closed instead of escaping
        # that boundary as a raw tree-helper exception.
        raise Stop(str(exc)) from exc


def writeahead_contents(
    *, request: dict[str, Any], request_bytes: bytes, prepared: dict[str, Any],
    global_lock_commit: str, protected_main_sha: str,
    proof_sha256: str,
) -> dict[str, Any]:
    """Deterministic immutable intent before target-branch CAS publication."""
    require(
        prepared["kind"] == PREPARED_KIND
        and prepared["expected_target_predecessor_sha"] == request["target_sha"]
        and prepared["prepared_parent_sha"] == request["target_sha"]
        and prepared["changed_paths"] == [ASSET_PATH]
        and prepared["deleted_paths"] == []
        and prepared["repair_main_sha"] == protected_main_sha
        and prepared["accepted_asset_blob_sha"] == request["accepted_asset_blob_sha"]
        and prepared["tracked_basketball_mutation"] == "NONE"
        and prepared["branch_published"] is False,
        "PRESENTATION_WRITEAHEAD_PREPARED_AUTHORITY_INVALID",
    )
    return {
        "schema_version": 1,
        "kind": WRITEAHEAD_KIND,
        "operation": OP_RELEASE_PRESENTATION_REFRESH,
        "request_id": request["request_id"],
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": request["school_key"],
        "target_branch": request["target_branch"],
        "global_lock_commit": global_lock_commit,
        "protected_main_sha": protected_main_sha,
        "repair_main_sha": request["repair_main_sha"],
        "accepted_asset_blob_sha": request["accepted_asset_blob_sha"],
        "sealed_tree_sha": request["sealed_tree_sha"],
        "stage2_apply_successor": request["stage2_apply_successor"],
        "stage2_apply_verification": request["stage2_apply_verification"],
        "approved_plan_hash": request["approved_plan_hash"],
        "release_manifest_sha256": request["release_manifest_sha256"],
        "expected_target_predecessor_sha": request["target_sha"],
        "prepared_parent_sha": request["target_sha"],
        "prepared_commit_sha": prepared["prepared_commit_sha"],
        "prepared_tree_sha": prepared["prepared_tree_sha"],
        "changed_paths": [ASSET_PATH],
        "changed_file_sha256": prepared["changed_file_sha256"],
        "deleted_paths": [],
        "sidecars": {"prepared-proof.json": proof_sha256},
        "repository_validation": "PASS",
        "mutation_state": "PREPARED_NOT_PUBLISHED",
        "owner_gate_2_approved": False,
    }


def validate_presentation_intent(
    request: dict[str, Any], writeahead: dict[str, Any],
    *, repo: Path,
) -> dict[str, object]:
    """Post-write-ahead recheck, also used by recovery and fresh verification."""
    require(
        writeahead.get("kind") == WRITEAHEAD_KIND
        and writeahead.get("operation") == OP_RELEASE_PRESENTATION_REFRESH
        and writeahead.get("request_id") == request["request_id"]
        and writeahead.get("school_key") == request["school_key"]
        and writeahead.get("target_branch") == request["target_branch"]
        and writeahead.get("expected_target_predecessor_sha") == request["target_sha"]
        and writeahead.get("prepared_parent_sha") == request["target_sha"]
        and writeahead.get("repair_main_sha") == request["repair_main_sha"]
        and writeahead.get("accepted_asset_blob_sha") == request["accepted_asset_blob_sha"]
        and writeahead.get("sealed_tree_sha") == request["sealed_tree_sha"]
        and writeahead.get("stage2_apply_successor") == request["stage2_apply_successor"]
        and writeahead.get("stage2_apply_verification") == request["stage2_apply_verification"]
        and writeahead.get("approved_plan_hash") == request["approved_plan_hash"]
        and writeahead.get("release_manifest_sha256") == request["release_manifest_sha256"]
        and writeahead.get("changed_paths") == [ASSET_PATH]
        and writeahead.get("deleted_paths") == []
        and writeahead.get("repository_validation") == "PASS"
        and writeahead.get("owner_gate_2_approved") is False,
        "PRESENTATION_WRITEAHEAD_AUTHORITY_MISMATCH",
    )
    proof = verify_committed_presentation(
        request, writeahead["prepared_commit_sha"], repo=repo,
    )
    require(
        proof["successor_tree_sha"] == writeahead["prepared_tree_sha"],
        "PRESENTATION_WRITEAHEAD_TREE_MISMATCH",
    )
    require(
        list(writeahead["changed_file_sha256"]) == [ASSET_PATH],
        "PRESENTATION_WRITEAHEAD_FILE_HASH_KEYS_INVALID",
    )
    expected = sha256_bytes(
        git_show_bytes(writeahead["prepared_commit_sha"], ASSET_PATH, cwd=repo)
    )
    require(
        writeahead["changed_file_sha256"][ASSET_PATH] == expected,
        "PRESENTATION_WRITEAHEAD_ASSET_HASH_MISMATCH",
    )
    return proof


def finalize_presentation_refresh_successor(
    *, active: dict[str, Any], request: dict[str, Any],
    request_sha256: str, live_main: str,
    writeahead: dict[str, Any], writeahead_path: str,
    writeahead_sha256: str, writeahead_commit: str | None,
    expected_remote: str, publication_cas: str,
    extra_commit_paths: list[Path | str] | None = None,
    recovery_request_id: str | None = None,
    recovery_classification: str | None = None,
    repo: Path = ROOT,
) -> str:
    prepared = writeahead["prepared_commit_sha"]
    require(
        remote_head(repo, request["target_branch"]) == prepared,
        "PRESENTATION_TARGET_NOT_EXACT_PREPARED",
    )
    require(
        live_main == writeahead["protected_main_sha"],
        "PRESENTATION_FINAL_MAIN_MISMATCH",
    )
    validate_presentation_intent(request, writeahead, repo=repo)
    directory = Path(
        ".remote-implementation/successors/%s/%s" % (
            request["school_key"], request["request_id"]
        )
    )
    directory.mkdir(parents=True, exist_ok=True)
    successor = {
        "schema_version": 1,
        "kind": SUCCESSOR_KIND,
        "operation": OP_RELEASE_PRESENTATION_REFRESH,
        "request_id": request["request_id"],
        "request_sha256": request_sha256,
        "school_key": request["school_key"],
        "target_branch": request["target_branch"],
        "protected_main_sha": live_main,
        "global_lock_commit": active["active_lock_commit"],
        "writeahead_manifest_path": writeahead_path,
        "writeahead_manifest_sha256": writeahead_sha256,
        "writeahead_commit": writeahead_commit,
        "expected_target_predecessor_sha": request["target_sha"],
        "prepared_parent_sha": request["target_sha"],
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": writeahead["prepared_tree_sha"],
        "actual_published_target_sha": prepared,
        "changed_paths": [ASSET_PATH],
        "changed_file_sha256": writeahead["changed_file_sha256"],
        "deleted_paths": [],
        "sealed_tree_sha": request["sealed_tree_sha"],
        "repair_main_sha": request["repair_main_sha"],
        "accepted_asset_blob_sha": request["accepted_asset_blob_sha"],
        "stage2_apply_successor": request["stage2_apply_successor"],
        "stage2_apply_verification": request["stage2_apply_verification"],
        "approved_plan_hash": request["approved_plan_hash"],
        "release_manifest_sha256": request["release_manifest_sha256"],
        "publication_cas": publication_cas,
        "recovery_request_id": recovery_request_id,
        "recovery_classification": recovery_classification,
        "owner_gate_2_approved": False,
        "tracked_basketball_mutation": "NONE",
        "repository_validation": "PASS",
        "final_transaction_state": "COMPLETE",
    }
    successor_path = directory / "successor-manifest.json"
    write_json(successor_path, successor)
    successor_sha256 = sha256_file(successor_path)
    finished = finalize_success(
        active,
        request_id=request["request_id"],
        last_operation={
            "operation": OP_RELEASE_PRESENTATION_REFRESH,
            "request_id": request["request_id"],
            "school_key": request["school_key"],
            "protected_main_sha": live_main,
            "target_branch": request["target_branch"],
            "original_sealed_sha": request["target_sha"],
            "target_sha": prepared,
            "prepared_tree_sha": writeahead["prepared_tree_sha"],
            "approved_plan_hash": request["approved_plan_hash"],
            "release_manifest_sha256": request["release_manifest_sha256"],
            "writeahead_manifest_path": writeahead_path,
            "writeahead_manifest_sha256": writeahead_sha256,
            "successor_manifest_path": successor_path.as_posix(),
            "successor_manifest_sha256": successor_sha256,
            "fresh_runner_verification": "PENDING",
            "remote_presentation_refresh_equivalence": "PENDING",
            "owner_gate_2_approved": False,
            "recovery_request_id": recovery_request_id,
            "recovery_classification": recovery_classification,
        },
    )
    if recovery_request_id and recovery_request_id not in finished["consumed_request_ids"]:
        finished["consumed_request_ids"].append(recovery_request_id)
    write_json(STATE_PATH, finished)
    paths: list[Path | str] = [STATE_PATH, directory]
    if extra_commit_paths:
        paths.extend(extra_commit_paths)
    return commit_control(
        expected_remote,
        "finalize post-seal presentation refresh %s" % request["request_id"],
        paths,
    )


def run_presentation_refresh(
    state: dict[str, Any], request: dict[str, Any], request_bytes: bytes,
    request_commit: str, predecessor_commit: str, live_main: str,
    *, repo: Path = ROOT,
) -> None:
    """The sole guarded mutation entrypoint, using existing control primitives."""
    require(
        request["operation"] == OP_RELEASE_PRESENTATION_REFRESH,
        "PRESENTATION_OPERATION_MISMATCH",
    )
    require(
        request["repair_main_sha"] == live_main,
        "PRESENTATION_MAIN_NOT_ACCEPTED_REPAIR_SOURCE",
    )
    require(
        remote_head(repo, request["target_branch"]) == request["target_sha"],
        "PRESENTATION_TARGET_NOT_ORIGINAL_SEALED",
    )
    # Authenticate complete original sealed-apply/readiness chain BEFORE lock.
    prepared = prepare_presentation_successor(
        request, predecessor_commit, repo=repo,
    )
    assert_protected_main_unchanged(live_main)
    require(
        remote_head(repo, request["target_branch"]) == request["target_sha"],
        "PRESENTATION_TARGET_MOVED_BEFORE_LOCK",
    )

    active = begin_request(
        state, request, sha256_bytes(request_bytes),
        run_id=os.environ.get("GITHUB_RUN_ID", "local"),
        run_attempt=os.environ.get("GITHUB_RUN_ATTEMPT", "1"),
        request_commit=request_commit,
    )
    write_json(STATE_PATH, active)
    request_path = Path(
        ".remote-implementation/requests/%s/request.json" % request["request_id"]
    )
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_bytes(request_bytes)
    lock_commit = commit_control(
        request_commit,
        "acquire global presentation refresh lock %s" % request["request_id"],
        [STATE_PATH, request_path],
    )
    active = bind_lock_commit(active, lock_commit)
    write_json(STATE_PATH, active)
    bound_lock = commit_control(
        lock_commit,
        "bind global presentation refresh lock %s" % request["request_id"],
        [STATE_PATH],
    )

    assert_protected_main_unchanged(live_main)
    require(
        remote_head(repo, request["target_branch"]) == request["target_sha"],
        "PRESENTATION_TARGET_MOVED_BEFORE_WRITEAHEAD",
    )
    writeahead_dir = Path(
        ".remote-implementation/writeahead/%s/%s" % (
            request["school_key"], request["request_id"]
        )
    )
    writeahead_dir.mkdir(parents=True, exist_ok=True)
    proof_file = writeahead_dir / "prepared-proof.json"
    write_json(proof_file, prepared)
    manifest = writeahead_contents(
        request=request, request_bytes=request_bytes, prepared=prepared,
        global_lock_commit=lock_commit, protected_main_sha=live_main,
        proof_sha256=sha256_file(proof_file),
    )
    validate_presentation_intent(request, manifest, repo=repo)
    writeahead_path = writeahead_dir / "writeahead-manifest.json"
    write_json(writeahead_path, manifest)
    writeahead_sha256 = sha256_file(writeahead_path)
    active["transaction_state"] = "PREPARED_NOT_PUBLISHED"
    active["active_writeahead_path"] = writeahead_path.as_posix()
    active["active_writeahead_sha256"] = writeahead_sha256
    active["active_prepared_commit_sha"] = prepared["prepared_commit_sha"]
    active["active_prepared_tree_sha"] = prepared["prepared_tree_sha"]
    write_json(STATE_PATH, active)
    writeahead_commit = commit_control(
        bound_lock,
        "persist presentation refresh write-ahead %s" % request["request_id"],
        [STATE_PATH, writeahead_dir],
    )
    active["active_writeahead_commit"] = writeahead_commit
    write_json(STATE_PATH, active)
    bound_writeahead = commit_control(
        writeahead_commit,
        "bind presentation refresh write-ahead %s" % request["request_id"],
        [STATE_PATH],
    )

    assert_protected_main_unchanged(live_main)
    require(
        remote_head(repo, request["target_branch"]) == request["target_sha"],
        "PRESENTATION_TARGET_MOVED_BEFORE_CAS",
    )
    validate_presentation_intent(request, manifest, repo=repo)
    publish_ref_cas(
        repo, branch=request["target_branch"],
        prepared_commit=prepared["prepared_commit_sha"],
        expected_predecessor=request["target_sha"],
    )
    require(
        remote_head(repo, request["target_branch"]) == prepared["prepared_commit_sha"],
        "PRESENTATION_CAS_PUBLICATION_NOT_EXACT",
    )
    assert_protected_main_unchanged(live_main)
    checkpoint = finalize_presentation_refresh_successor(
        active=active, request=request,
        request_sha256=sha256_bytes(request_bytes), live_main=live_main,
        writeahead=manifest, writeahead_path=writeahead_path.as_posix(),
        writeahead_sha256=writeahead_sha256,
        writeahead_commit=writeahead_commit,
        expected_remote=bound_writeahead,
        publication_cas="EXISTING_REF_CAS_PASS",
        repo=repo,
    )
    print(
        "PRESENTATION REFRESH: COMPLETE candidate=%s checkpoint=%s"
        % (prepared["prepared_commit_sha"], checkpoint)
    )
