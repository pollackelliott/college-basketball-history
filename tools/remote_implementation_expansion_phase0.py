#!/usr/bin/env python3
"""Expansion-aware Phase 0 transaction helpers for guarded remote Implementation.

This module does not create a second control plane. It binds the generic
ALL_HISTORY_EXPANSION Integration Freeze and Phase 0 preview to the existing
serialized remote Implementation lock, write-ahead, expected-predecessor CAS,
recovery, and independent fresh-verifier contracts.
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from all_history_expansion_freeze import ZIP_MEMBERS, ZIP_MEMBERS_V2
from all_history_expansion_integration import (
    MANIFEST_NAME,
    PACKAGE_FILES,
    STAGE1_REPORT,
    freeze_authority,
    sha256,
)
from all_history_expansion_phase0_preview import preview_phase0
from all_history_expansion_remote_contract import (
    authenticate_intent,
    exact_paths,
    verify_exact_prepared,
)
from remote_implementation_control import (
    OP_EXPANSION_PHASE0,
    begin_request,
    bind_lock_commit,
    canonical_json_bytes,
    finalize_success,
    publish_ref_cas,
    sha256_bytes,
    sha256_file,
)
from remote_implementation_io import (
    ROOT,
    STATE_PATH,
    Stop,
    add_isolated_worktree,
    assert_protected_main_unchanged,
    commit_control,
    commit_file_hashes,
    configure_git,
    git,
    git_show_bytes,
    materialize_payload,
    remote_head,
    run,
    write_json,
)


def materialize_expansion_research_checkpoint(
    request: dict[str, Any],
    out_path: Path,
) -> dict[str, Any]:
    """Materialize and authenticate an immutable expansion Research Freeze."""
    checkpoint = request["expansion_research_checkpoint"]
    transport = checkpoint["transport"]
    commit_sha = transport["commit_sha"]
    git("fetch", "--no-tags", "origin", commit_sha)
    git("fetch", "--no-tags", "origin", checkpoint["research_base_sha"])
    prefix = transport["path_prefix"]
    parts = sorted(
        path
        for path in git("ls-tree", "-r", "--name-only", commit_sha).stdout.splitlines()
        if path.startswith(prefix)
    )
    if len(parts) != int(transport["part_count"]):
        raise Stop(
            "EXPANSION_RESEARCH_CHECKPOINT_PART_COUNT_MISMATCH expected=%s actual=%s"
            % (transport["part_count"], len(parts))
        )
    encoded = b"".join(git_show_bytes(commit_sha, path) for path in parts)
    try:
        data = base64.b64decode(encoded, validate=True)
    except ValueError as exc:
        raise Stop("EXPANSION_RESEARCH_CHECKPOINT_BASE64_INVALID: %s" % exc) from exc
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    actual = sha256_file(out_path)
    if actual != checkpoint["sha256"]:
        raise Stop(
            "EXPANSION_RESEARCH_CHECKPOINT_SHA_MISMATCH expected=%s actual=%s"
            % (checkpoint["sha256"], actual)
        )
    try:
        with zipfile.ZipFile(out_path) as archive:
            names = tuple(sorted(archive.namelist()))
    except zipfile.BadZipFile as exc:
        raise Stop("EXPANSION_RESEARCH_CHECKPOINT_ZIP_INVALID") from exc
    if names not in {ZIP_MEMBERS, ZIP_MEMBERS_V2}:
        raise Stop("EXPANSION_RESEARCH_CHECKPOINT_MEMBER_SET_MISMATCH:%s" % (names,))
    return {
        "sha256": actual,
        "research_base_sha": checkpoint["research_base_sha"],
        "member_names": list(names),
    }


def _target_predecessor_authority(
    request: dict[str, Any],
    live_main: str,
) -> tuple[str, bool]:
    target_branch = request["target_branch"]
    target = remote_head(ROOT, target_branch)
    if target != request["target_sha"]:
        raise Stop(
            "EXPANSION_PHASE0_TARGET_PREDECESSOR_CHANGED expected=%s actual=%s"
            % (request["target_sha"], target or "[missing]")
        )
    cp = git(
        "merge-base",
        "--is-ancestor",
        target,
        live_main,
        cwd=ROOT,
        check=False,
    )
    return target, cp.returncode == 0


def _external_authority(
    *,
    request: dict[str, Any],
    control_commit: str,
    live_main: str,
    worktree: Path,
    scratch: Path,
) -> dict[str, Any]:
    research_zip = scratch / "expansion-research-frozen.zip"
    checkpoint_info = materialize_expansion_research_checkpoint(request, research_zip)
    proof = materialize_payload(
        control_commit,
        request["stage1_independent_proof"],
        scratch / "stage1-independent-proof.json",
    )
    if proof is None:
        raise Stop("EXPANSION_PHASE0_STAGE1_PROOF_MISSING")
    if sha256_file(proof) != request["stage1_independent_proof_sha256"]:
        raise Stop("EXPANSION_PHASE0_STAGE1_PROOF_HASH_MISMATCH")

    frozen = scratch / "integration-freeze"
    manifest = freeze_authority(
        worktree,
        request["school_key"],
        research_zip,
        request["research_freeze_sha256"],
        request["expansion_research_checkpoint"]["research_base_sha"],
        live_main,
        proof,
        request["stage1_independent_proof_sha256"],
        frozen,
    )
    manifest_bytes = (frozen / MANIFEST_NAME).read_bytes()
    manifest_sha = sha256_bytes(manifest_bytes)
    if manifest_sha != request["integration_freeze_sha256"]:
        raise Stop(
            "EXPANSION_PHASE0_INTEGRATION_FREEZE_HASH_MISMATCH expected=%s actual=%s"
            % (request["integration_freeze_sha256"], manifest_sha)
        )

    preview_dir = scratch / "phase0-preview"
    try:
        preview = preview_phase0(worktree, frozen, preview_dir)
    except Exception:
        blocker = preview_dir / "phase0-venue-identity-blockers.json"
        diag = Path(
            os.environ.get(
                "REMOTE_IMPLEMENTATION_DIAG",
                "/tmp/remote-implementation-diagnostics",
            )
        )
        if blocker.is_file():
            diag.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(blocker, diag / blocker.name)
        raise

    target, ancestor = _target_predecessor_authority(request, live_main)
    intent = authenticate_intent(
        request=request,
        current_main=live_main,
        current_target=target,
        target_is_ancestor_of_main=ancestor,
        freeze=frozen,
        phase0_preview=preview_dir,
        original_research_sha256=request["research_freeze_sha256"],
        accepted_stage1_proof_sha256=request["stage1_independent_proof_sha256"],
        exact_freeze_manifest_sha256=request["integration_freeze_sha256"],
    )
    semantic = manifest.get("source_game_semantic_guard") or {}
    semantic_sha = str(semantic.get("snapshot_sha256") or "")
    if len(semantic_sha) != 64:
        raise Stop("EXPANSION_PHASE0_SEMANTIC_SNAPSHOT_MISSING")

    return {
        "checkpoint_info": checkpoint_info,
        "proof_path": proof,
        "frozen": frozen,
        "manifest": manifest,
        "manifest_bytes": manifest_bytes,
        "preview_dir": preview_dir,
        "preview": preview,
        "intent": intent,
        "semantic_snapshot_sha256": semantic_sha,
    }


def _install_preview_candidate(
    worktree: Path,
    request: dict[str, Any],
    authority: dict[str, Any],
) -> list[str]:
    preview_dir = authority["preview_dir"]
    school = request["school_key"]
    for name in PACKAGE_FILES:
        destination = worktree / "schools" / school / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((preview_dir / name).read_bytes())
    for path in sorted(authority["intent"]["projected_global_sha256"]):
        source = preview_dir / "references" / Path(path).name
        destination = worktree / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())

    allowed = sorted(exact_paths(school))
    git("add", "--", *allowed, cwd=worktree)
    return allowed


def _repository_validation(worktree: Path, diag: Path) -> None:
    cp = run(
        [sys.executable, str(worktree / "tools" / "validate_data.py")],
        cwd=worktree,
        check=False,
    )
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "expansion-phase0-validate-data.log").write_text(
        cp.stdout,
        encoding="utf-8",
    )
    if cp.returncode != 0:
        raise Stop(
            "EXPANSION_PHASE0_REPOSITORY_VALIDATION_FAILED\n" + cp.stdout[-10000:]
        )


def _all_expected_hashes(
    commit_or_treeish: str,
    request: dict[str, Any],
    intent: dict[str, Any],
    *,
    repo: Path,
) -> dict[str, str]:
    result: dict[str, str] = {}
    for name in PACKAGE_FILES:
        path = "schools/%s/%s" % (request["school_key"], name)
        result[path] = sha256_bytes(git_show_bytes(commit_or_treeish, path, cwd=repo))
    for path in sorted(intent["projected_global_sha256"]):
        result[path] = sha256_bytes(git_show_bytes(commit_or_treeish, path, cwd=repo))
    return result


def _verify_projected_hashes(
    request: dict[str, Any],
    intent: dict[str, Any],
    hashes: dict[str, str],
) -> None:
    expected = {
        "schools/%s/%s" % (request["school_key"], name): digest
        for name, digest in intent["projected_package_sha256"].items()
    }
    expected.update(intent["projected_global_sha256"])
    if hashes != expected:
        missing = sorted(set(expected) ^ set(hashes))
        bad = sorted(
            path
            for path in set(expected) & set(hashes)
            if expected[path] != hashes[path]
        )
        raise Stop(
            "EXPANSION_PHASE0_PROJECTED_HASH_MISMATCH missing=%s bad=%s"
            % (missing, bad)
        )


def prepare_expansion_candidate(
    *,
    request: dict[str, Any],
    control_commit: str,
    live_main: str,
    diag: Path,
    commit: bool,
) -> dict[str, Any]:
    """Reconstruct exact expansion Phase 0 candidate from protected main."""
    worktree = add_isolated_worktree(live_main, request["school_key"])
    scratch = Path(tempfile.mkdtemp(prefix="remote-expansion-phase0-authority-"))
    authority = _external_authority(
        request=request,
        control_commit=control_commit,
        live_main=live_main,
        worktree=worktree,
        scratch=scratch,
    )
    allowed = _install_preview_candidate(worktree, request, authority)
    _repository_validation(worktree, diag)

    changed = sorted(
        line.strip()
        for line in git(
            "diff",
            "--cached",
            "--name-only",
            cwd=worktree,
        ).stdout.splitlines()
        if line.strip()
    )
    if "schools/%s/source-games.csv" % request["school_key"] not in changed:
        raise Stop("EXPANSION_PHASE0_SOURCE_GAME_PACKAGE_NOT_UPDATED")
    if not set(changed).issubset(set(allowed)):
        raise Stop(
            "EXPANSION_PHASE0_DIFF_OUTSIDE_CONTRACT:"
            + ",".join(sorted(set(changed) - set(allowed)))
        )

    replay_tree = git("write-tree", cwd=worktree).stdout.strip()
    if commit:
        message = "Stage %s all-history expansion Phase 0" % request["school_key"]
        git("commit", "-m", message, cwd=worktree)
        prepared = git("rev-parse", "HEAD", cwd=worktree).stdout.strip()
        parent = git("rev-parse", prepared + "^", cwd=worktree).stdout.strip()
        tree = git("rev-parse", prepared + "^{tree}", cwd=worktree).stdout.strip()
        if parent != live_main:
            raise Stop("EXPANSION_PHASE0_PREPARED_PARENT_MISMATCH")
        if tree != replay_tree:
            raise Stop("EXPANSION_PHASE0_PREPARED_TREE_CHANGED_AFTER_COMMIT")
    else:
        prepared = ""
        parent = live_main
        tree = replay_tree
        message = ""

    hashes = _all_expected_hashes(
        prepared if commit else tree,
        request,
        authority["intent"],
        repo=worktree,
    )
    _verify_projected_hashes(request, authority["intent"], hashes)

    proof = verify_exact_prepared(
        intent=authority["intent"],
        prepared_parent_sha=parent,
        prepared_tree_sha=tree,
        replay_tree_sha=replay_tree,
        changed_paths=changed,
        committed_files_sha256=hashes,
        inherited_rows_preserved=True,
        semantic_guard_hash=authority["semantic_snapshot_sha256"],
    )
    return {
        "worktree": worktree,
        "scratch": scratch,
        "authority": authority,
        "allowed_paths": allowed,
        "changed_paths": changed,
        "all_expected_hashes": hashes,
        "prepared_commit_sha": prepared,
        "prepared_parent_sha": parent,
        "prepared_tree_sha": tree,
        "commit_message": message,
        "exact_tree_proof": proof,
    }


def _archive_request(request: dict[str, Any], request_bytes: bytes) -> Path:
    path = Path(
        ".remote-implementation/requests/%s/request.json" % request["request_id"]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(request_bytes)
    return path


def run_expansion_phase0(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    live_main: str,
    diag: Path,
) -> None:
    """Execute one expansion Phase 0 through the existing mutation primitives."""
    target_branch = request["target_branch"]
    target, ancestor = _target_predecessor_authority(request, live_main)
    if not ancestor:
        raise Stop("EXPANSION_PHASE0_TARGET_PREDECESSOR_NOT_ACCEPTED_IN_MAIN")

    run_id = os.environ.get("GITHUB_RUN_ID", "local")
    attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")
    active = begin_request(
        state,
        request,
        sha256_bytes(request_bytes),
        run_id=run_id,
        run_attempt=attempt,
        request_commit=request_commit,
    )
    write_json(STATE_PATH, active)
    archive = _archive_request(request, request_bytes)
    lock_commit = commit_control(
        request_commit,
        "acquire global expansion Phase 0 lock %s" % request["request_id"],
        [STATE_PATH, archive],
    )
    active = bind_lock_commit(active, lock_commit)
    write_json(STATE_PATH, active)
    lock_bound_commit = commit_control(
        lock_commit,
        "bind global expansion Phase 0 lock %s" % request["request_id"],
        [STATE_PATH],
    )

    candidate = prepare_expansion_candidate(
        request=request,
        control_commit=lock_bound_commit,
        live_main=live_main,
        diag=diag,
        commit=True,
    )
    authority = candidate["authority"]

    input_dir = Path(
        ".remote-implementation/phase0-inputs/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    input_dir.mkdir(parents=True, exist_ok=True)
    (input_dir / "integration-freeze.json").write_bytes(
        authority["manifest_bytes"]
    )
    (input_dir / STAGE1_REPORT).write_bytes(
        (authority["frozen"] / STAGE1_REPORT).read_bytes()
    )
    (input_dir / "phase0-preview.json").write_bytes(
        (authority["preview_dir"] / "phase0-preview.json").read_bytes()
    )
    (input_dir / "stage1-independent-proof.json").write_bytes(
        authority["proof_path"].read_bytes()
    )
    sidecars = {
        name: sha256_file(input_dir / name)
        for name in (
            "integration-freeze.json",
            STAGE1_REPORT,
            "phase0-preview.json",
            "stage1-independent-proof.json",
        )
    }
    write_json(
        input_dir / "input-manifest.json",
        {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_EXPANSION_PHASE0_INPUTS",
            "request_id": request["request_id"],
            "school_key": request["school_key"],
            "protected_main_sha": live_main,
            "expected_target_predecessor_sha": target,
            "research_freeze_sha256": request["research_freeze_sha256"],
            "research_base_sha": request["expansion_research_checkpoint"][
                "research_base_sha"
            ],
            "stage1_independent_proof_sha256": request[
                "stage1_independent_proof_sha256"
            ],
            "integration_freeze_sha256": request["integration_freeze_sha256"],
            "semantic_snapshot_sha256": authority[
                "semantic_snapshot_sha256"
            ],
            "sidecars": sidecars,
        },
    )
    active["transaction_state"] = "INPUTS_VERIFIED"
    write_json(STATE_PATH, active)
    inputs_commit = commit_control(
        lock_bound_commit,
        "persist authenticated expansion Phase 0 inputs %s" % request["request_id"],
        [STATE_PATH, input_dir],
    )

    prepared = candidate["prepared_commit_sha"]
    tree = candidate["prepared_tree_sha"]
    parent = candidate["prepared_parent_sha"]
    changed = candidate["changed_paths"]
    changed_hashes = commit_file_hashes(
        candidate["worktree"],
        prepared,
        changed,
    )

    writeahead_dir = Path(
        ".remote-implementation/writeahead/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    writeahead_dir.mkdir(parents=True, exist_ok=True)
    for name in sidecars:
        shutil.copyfile(input_dir / name, writeahead_dir / name)
    writeahead = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
        "operation": OP_EXPANSION_PHASE0,
        "request_id": request["request_id"],
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": request["school_key"],
        "global_lock_commit": lock_commit,
        "protected_main_sha": live_main,
        "research_checkpoint_sha256": request["research_freeze_sha256"],
        "research_base_sha": request["expansion_research_checkpoint"][
            "research_base_sha"
        ],
        "stage1_independent_proof_sha256": request[
            "stage1_independent_proof_sha256"
        ],
        "target_branch": target_branch,
        "expected_target_predecessor_sha": target,
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": tree,
        "prepared_parent_sha": parent,
        "commit_message": candidate["commit_message"],
        "changed_paths": changed,
        "changed_file_sha256": changed_hashes,
        "allowed_paths": candidate["allowed_paths"],
        "sidecars": sidecars,
        "integration_freeze_sha256": request["integration_freeze_sha256"],
        "package_member_sha256": authority["manifest"][
            "package_member_sha256"
        ],
        "semantic_snapshot_sha256": authority[
            "semantic_snapshot_sha256"
        ],
        "repository_validation": "PASS",
        "mutation_state": "PREPARED_NOT_PUBLISHED",
    }
    writeahead_path = writeahead_dir / "writeahead-manifest.json"
    write_json(writeahead_path, writeahead)
    writeahead_sha = sha256_file(writeahead_path)

    active["transaction_state"] = "PREPARED_NOT_PUBLISHED"
    active["active_writeahead_path"] = writeahead_path.as_posix()
    active["active_writeahead_sha256"] = writeahead_sha
    active["active_prepared_commit_sha"] = prepared
    active["active_prepared_tree_sha"] = tree
    write_json(STATE_PATH, active)
    writeahead_commit = commit_control(
        inputs_commit,
        "publish expansion Phase 0 write-ahead %s" % request["request_id"],
        [STATE_PATH, writeahead_dir],
    )
    active["active_writeahead_commit"] = writeahead_commit
    write_json(STATE_PATH, active)
    writeahead_bound_commit = commit_control(
        writeahead_commit,
        "bind expansion Phase 0 write-ahead %s" % request["request_id"],
        [STATE_PATH],
    )

    assert_protected_main_unchanged(live_main)
    publish_ref_cas(
        ROOT,
        branch=target_branch,
        prepared_commit=prepared,
        expected_predecessor=target,
    )
    actual_target = remote_head(ROOT, target_branch)
    if actual_target != prepared:
        raise Stop("EXPANSION_PHASE0_TARGET_PUBLICATION_VERIFY_FAILED")

    successor_dir = Path(
        ".remote-implementation/successors/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    successor_dir.mkdir(parents=True, exist_ok=True)
    successor = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_SUCCESSOR",
        "operation": OP_EXPANSION_PHASE0,
        "request_id": request["request_id"],
        "school_key": request["school_key"],
        "request_sha256": sha256_bytes(request_bytes),
        "global_lock_commit": lock_commit,
        "writeahead_commit": writeahead_commit,
        "writeahead_manifest_path": writeahead_path.as_posix(),
        "writeahead_manifest_sha256": writeahead_sha,
        "protected_main_sha": live_main,
        "expected_target_predecessor_sha": target,
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": tree,
        "prepared_parent_sha": parent,
        "actual_published_target_sha": actual_target,
        "target_branch": target_branch,
        "changed_paths": changed,
        "changed_file_sha256": changed_hashes,
        "integration_freeze_sha256": request["integration_freeze_sha256"],
        "semantic_snapshot_sha256": authority[
            "semantic_snapshot_sha256"
        ],
        "repository_validation": "PASS",
        "publication_cas": "EXISTING_REF_CAS_PASS",
        "final_transaction_state": "COMPLETE",
    }
    successor_path = successor_dir / "successor-manifest.json"
    write_json(successor_path, successor)
    successor_sha = sha256_file(successor_path)
    final_state = finalize_success(
        active,
        request_id=request["request_id"],
        last_operation={
            "operation": OP_EXPANSION_PHASE0,
            "request_id": request["request_id"],
            "school_key": request["school_key"],
            "protected_main_sha": live_main,
            "target_branch": target_branch,
            "target_sha": actual_target,
            "writeahead_manifest_path": writeahead_path.as_posix(),
            "writeahead_manifest_sha256": writeahead_sha,
            "successor_manifest_path": successor_path.as_posix(),
            "successor_manifest_sha256": successor_sha,
            "integration_freeze_sha256": request["integration_freeze_sha256"],
            "semantic_snapshot_sha256": authority[
                "semantic_snapshot_sha256"
            ],
            "fresh_runner_verification": "PENDING",
            "remote_phase0_equivalence": "PENDING",
        },
    )
    write_json(STATE_PATH, final_state)
    successor_commit = commit_control(
        writeahead_bound_commit,
        "finalize expansion Phase 0 %s" % request["request_id"],
        [STATE_PATH, successor_dir],
    )
    print(
        "REMOTE EXPANSION PHASE 0: COMPLETE target=%s successor_commit=%s"
        % (actual_target, successor_commit)
    )


def verify_expansion_phase0_equivalence(
    *,
    live_main: str,
    control_head: str,
    state: dict[str, Any],
    diag: Path,
) -> int:
    """Freshly reconstruct and prove the exact published expansion successor tree."""
    last = state.get("last_operation") or {}
    if last.get("operation") != OP_EXPANSION_PHASE0:
        raise Stop("EXPANSION_PHASE0_FRESH_OPERATION_MISMATCH")
    if last.get("fresh_runner_verification") == "PASS":
        print("REMOTE EXPANSION PHASE 0 EQUIVALENCE: ALREADY PASS")
        return 0

    successor_bytes = git_show_bytes(
        control_head,
        last["successor_manifest_path"],
    )
    if sha256_bytes(successor_bytes) != last["successor_manifest_sha256"]:
        raise Stop("EXPANSION_PHASE0_FRESH_SUCCESSOR_HASH_MISMATCH")
    successor = json.loads(successor_bytes)
    if (
        successor.get("kind") != "REMOTE_IMPLEMENTATION_SUCCESSOR"
        or successor.get("operation") != OP_EXPANSION_PHASE0
        or successor.get("final_transaction_state") != "COMPLETE"
    ):
        raise Stop("EXPANSION_PHASE0_FRESH_SUCCESSOR_INVALID")

    writeahead_bytes = git_show_bytes(
        control_head,
        successor["writeahead_manifest_path"],
    )
    if sha256_bytes(writeahead_bytes) != successor["writeahead_manifest_sha256"]:
        raise Stop("EXPANSION_PHASE0_FRESH_WRITEAHEAD_HASH_MISMATCH")
    writeahead = json.loads(writeahead_bytes)
    if writeahead.get("operation") != OP_EXPANSION_PHASE0:
        raise Stop("EXPANSION_PHASE0_FRESH_WRITEAHEAD_OPERATION_MISMATCH")

    request_path = (
        ".remote-implementation/requests/%s/request.json"
        % successor["request_id"]
    )
    request_bytes = git_show_bytes(control_head, request_path)
    if sha256_bytes(request_bytes) != successor["request_sha256"]:
        raise Stop("EXPANSION_PHASE0_FRESH_REQUEST_HASH_MISMATCH")
    request = json.loads(request_bytes)

    target_branch = successor["target_branch"]
    git(
        "fetch",
        "--no-tags",
        "origin",
        "+refs/heads/%s:refs/remotes/origin/remote-expansion-verify-target"
        % target_branch,
        cwd=ROOT,
    )
    actual_target = remote_head(ROOT, target_branch)
    if actual_target != successor["prepared_commit_sha"]:
        raise Stop("EXPANSION_PHASE0_FRESH_TARGET_MOVED")
    parent = git(
        "rev-parse",
        successor["prepared_commit_sha"] + "^",
        cwd=ROOT,
    ).stdout.strip()
    tree = git(
        "rev-parse",
        successor["prepared_commit_sha"] + "^{tree}",
        cwd=ROOT,
    ).stdout.strip()
    if parent != live_main or parent != successor["prepared_parent_sha"]:
        raise Stop("EXPANSION_PHASE0_FRESH_PARENT_MISMATCH")
    if tree != successor["prepared_tree_sha"]:
        raise Stop("EXPANSION_PHASE0_FRESH_TREE_MISMATCH")

    reconstructed = prepare_expansion_candidate(
        request=request,
        control_commit=control_head,
        live_main=live_main,
        diag=diag,
        commit=False,
    )
    if reconstructed["prepared_tree_sha"] != tree:
        raise Stop("EXPANSION_PHASE0_FRESH_REPLAY_TREE_MISMATCH")
    if (
        reconstructed["authority"]["semantic_snapshot_sha256"]
        != successor["semantic_snapshot_sha256"]
    ):
        raise Stop("EXPANSION_PHASE0_FRESH_SEMANTIC_MISMATCH")
    if reconstructed["changed_paths"] != successor["changed_paths"]:
        raise Stop("EXPANSION_PHASE0_FRESH_CHANGED_PATH_MISMATCH")

    for path, expected in successor["changed_file_sha256"].items():
        if sha256_bytes(
            git_show_bytes(successor["prepared_commit_sha"], path, cwd=ROOT)
        ) != expected:
            raise Stop("EXPANSION_PHASE0_FRESH_CHANGED_FILE_MISMATCH:" + path)

    verification = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_EXPANSION_PHASE0_VERIFICATION",
        "status": "PASS",
        "request_id": request["request_id"],
        "school_key": request["school_key"],
        "protected_main_sha": live_main,
        "target_branch": target_branch,
        "expected_target_predecessor_sha": successor[
            "expected_target_predecessor_sha"
        ],
        "target_sha": successor["prepared_commit_sha"],
        "prepared_tree_sha": tree,
        "integration_freeze_sha256": successor[
            "integration_freeze_sha256"
        ],
        "semantic_snapshot_sha256": successor[
            "semantic_snapshot_sha256"
        ],
        "changed_paths": successor["changed_paths"],
        "repository_validation": "PASS",
        "independent_exact_tree_equivalence": "PASS",
        "publication_cas": successor["publication_cas"],
    }
    folder = Path(
        ".remote-implementation/verifications/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    write_json(folder / "expansion-phase0-verification.json", verification)

    current = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    current_last = current.get("last_operation") or {}
    if (
        current_last.get("operation") != OP_EXPANSION_PHASE0
        or current_last.get("request_id") != request["request_id"]
    ):
        raise Stop("EXPANSION_PHASE0_FRESH_CONTROL_MOVED")
    current_last["fresh_runner_verification"] = "PASS"
    current_last["remote_phase0_equivalence"] = "PASS"
    current["last_operation"] = current_last
    write_json(STATE_PATH, current)
    commit = commit_control(
        control_head,
        "persist independent expansion Phase 0 proof %s" % request["request_id"],
        [STATE_PATH, folder],
    )
    print("REMOTE EXPANSION PHASE 0 EQUIVALENCE PASS commit=%s" % commit)
    return 0
