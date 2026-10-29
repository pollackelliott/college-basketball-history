#!/usr/bin/env python3
"""Guarded remote transaction for pre-publication Phase 0 scope supersession."""
from __future__ import annotations

import copy
import csv
import io
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from remote_implementation_control import (
    OP_PHASE0_SCOPE_SUPERSESSION,
    begin_request,
    bind_lock_commit,
    finalize_success,
    publish_ref_cas,
    sha256_bytes,
    sha256_file,
    validate_control_state,
    verify_sidecar_hashes,
)
from remote_implementation_io import (
    REQUIRED_PACKAGE_FILES,
    ROOT,
    STATE_PATH,
    Stop,
    add_isolated_worktree,
    assert_protected_main_unchanged,
    commit_control,
    commit_file_hashes,
    git,
    git_show_bytes,
    materialize_payload,
    materialize_research_checkpoint,
    phase0_allowed_paths,
    phase0_command,
    remote_head,
    run,
    run_stage1_tool,
    validate_stage1_pass,
    write_json,
)
from remote_implementation_scope_supersession import (
    augment_integration_freeze,
    build_scope_superseded_package,
    deterministic_package_zip_bytes,
    proof_sha256,
    validate_scope_supersession_spec,
)


def _read_json_ref(
    control_commit: str,
    ref: dict[str, Any],
    *,
    code: str,
) -> tuple[dict[str, Any], bytes]:
    data = git_show_bytes(control_commit, ref["path"])
    if sha256_bytes(data) != ref["sha256"]:
        raise Stop(code + "_HASH_MISMATCH")
    try:
        value = json.loads(data)
    except (TypeError, ValueError) as exc:
        raise Stop(code + "_JSON_INVALID") from exc
    if not isinstance(value, dict):
        raise Stop(code + "_NOT_OBJECT")
    return value, data


def verify_scope_supersession_authority(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> dict[str, Any]:
    target_branch = request["target_branch"]
    target_sha = request["target_sha"]
    if remote_head(ROOT, target_branch) != target_sha:
        raise Stop("SCOPE_SUPERSESSION_TARGET_HEAD_MISMATCH")

    last = state.get("last_operation") or {}
    if (
        last.get("school_key") != request["school_key"]
        or last.get("target_branch") != target_branch
        or last.get("target_sha") != target_sha
        or last.get("fresh_runner_verification") != "PASS"
    ):
        raise Stop("SCOPE_SUPERSESSION_TARGET_NOT_FRESH_VERIFIED")

    phase0, phase0_bytes = _read_json_ref(
        predecessor_commit,
        request["superseded_phase0_successor"],
        code="SCOPE_SUPERSESSION_PHASE0_SUCCESSOR",
    )
    if (
        phase0.get("kind") != "REMOTE_IMPLEMENTATION_SUCCESSOR"
        or phase0.get("school_key") != request["school_key"]
        or phase0.get("target_branch") != target_branch
        or phase0.get("integration_freeze_sha256")
        != request["superseded_integration_freeze_sha256"]
        or phase0.get("semantic_snapshot_sha256")
        != request["superseded_semantic_snapshot_sha256"]
        or phase0.get("repository_validation") != "PASS"
        or phase0.get("final_transaction_state") != "COMPLETE"
    ):
        raise Stop("SCOPE_SUPERSESSION_PHASE0_SUCCESSOR_BINDING_MISMATCH")

    current, current_bytes = _read_json_ref(
        predecessor_commit,
        request["superseded_successor"],
        code="SCOPE_SUPERSESSION_CURRENT_SUCCESSOR",
    )
    if (
        current.get("school_key") != request["school_key"]
        or current.get("target_branch") != target_branch
        or current.get("actual_published_target_sha") != target_sha
        or current.get("prepared_commit_sha") != target_sha
        or current.get("integration_freeze_sha256")
        != request["superseded_integration_freeze_sha256"]
        or current.get("semantic_snapshot_sha256")
        != request["superseded_semantic_snapshot_sha256"]
        or current.get("repository_validation") != "PASS"
        or current.get("final_transaction_state") != "COMPLETE"
    ):
        raise Stop("SCOPE_SUPERSESSION_CURRENT_SUCCESSOR_BINDING_MISMATCH")
    if current.get("kind") not in {
        "REMOTE_IMPLEMENTATION_SUCCESSOR",
        "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR",
    }:
        raise Stop("SCOPE_SUPERSESSION_CURRENT_SUCCESSOR_KIND_UNSUPPORTED")

    spec_path = materialize_payload(
        request_commit,
        request["scope_supersession_spec"],
        Path(tempfile.mkdtemp(prefix="scope-supersession-spec-"))
        / "scope-supersession.json",
    )
    if spec_path is None:
        raise Stop("SCOPE_SUPERSESSION_SPEC_MISSING")
    spec_bytes = spec_path.read_bytes()
    spec = validate_scope_supersession_spec(
        json.loads(spec_bytes),
        school_key=request["school_key"],
    )
    if (
        spec["new_scope"] != request["history_scope"].get("intervals")
        or spec["history_start_season"]
        != request["history_scope"].get("start_season")
    ):
        raise Stop("SCOPE_SUPERSESSION_SPEC_HISTORY_SCOPE_MISMATCH")
    if (
        request["scope_supersession_authorization"].get("spec_sha256")
        != sha256_bytes(spec_bytes)
    ):
        raise Stop("SCOPE_SUPERSESSION_AUTHORIZATION_SPEC_BYTES_MISMATCH")

    return {
        "phase0_successor": phase0,
        "phase0_successor_bytes": phase0_bytes,
        "current_successor": current,
        "current_successor_bytes": current_bytes,
        "spec": spec,
        "spec_bytes": spec_bytes,
    }


def _predecessor_members(
    target_sha: str,
    school_key: str,
) -> dict[str, bytes]:
    return {
        name: git_show_bytes(
            target_sha,
            f"schools/{school_key}/{name}",
            cwd=ROOT,
        )
        for name in REQUIRED_PACKAGE_FILES
    }


def _original_research_source_ids(path: Path) -> set[str]:
    with zipfile.ZipFile(path) as archive:
        data = archive.read("source-games.csv").decode("utf-8-sig")
    return {
        row["source_game_id"].strip()
        for row in csv.DictReader(io.StringIO(data, newline=""))
        if row.get("source_game_id", "").strip()
    }


def _package_source_ids(data: bytes) -> set[str]:
    return {
        row["source_game_id"].strip()
        for row in csv.DictReader(
            io.StringIO(data.decode("utf-8-sig"), newline="")
        )
        if row.get("source_game_id", "").strip()
    }


def _candidate_request(
    request: dict[str, Any],
    *,
    candidate_sha256: str,
) -> dict[str, Any]:
    candidate = copy.deepcopy(request)
    candidate["research_checkpoint"]["sha256"] = candidate_sha256
    candidate["venue_reconciliation"] = None
    candidate["conference_reconciliation"] = None
    return candidate


def prepare_scope_supersession(
    *,
    request: dict[str, Any],
    authority: dict[str, Any],
    live_main: str,
    diag: Path,
) -> dict[str, Any]:
    school = request["school_key"]
    target_sha = request["target_sha"]
    predecessor_members = _predecessor_members(target_sha, school)

    scratch = Path(tempfile.mkdtemp(prefix="scope-supersession-inputs-"))
    original_zip = scratch / "original-research-frozen.zip"
    original_info = materialize_research_checkpoint(request, original_zip)
    expected_before = int(authority["spec"]["expected_source_game_count_before"])
    if original_info["source_game_count"] != expected_before:
        raise Stop("SCOPE_SUPERSESSION_ORIGINAL_RESEARCH_COUNT_MISMATCH")
    if _original_research_source_ids(original_zip) != _package_source_ids(
        predecessor_members["source-games.csv"]
    ):
        raise Stop("SCOPE_SUPERSESSION_PREDECESSOR_SOURCE_ID_DRIFT")

    current_main_venues = git_show_bytes(
        live_main,
        "data/reference/venues.csv",
        cwd=ROOT,
    )
    candidate_members, proof = build_scope_superseded_package(
        predecessor_members,
        current_main_venues,
        authority["spec"],
        school_key=school,
    )
    if proof["source_game_count_before"] != expected_before:
        raise Stop("SCOPE_SUPERSESSION_PROOF_BEFORE_COUNT_MISMATCH")

    candidate_zip_bytes = deterministic_package_zip_bytes(candidate_members)
    candidate_zip = scratch / "scope-superseded.zip"
    candidate_zip.write_bytes(candidate_zip_bytes)
    candidate_sha = sha256_bytes(candidate_zip_bytes)
    candidate_request = _candidate_request(
        request,
        candidate_sha256=candidate_sha,
    )

    worktree = add_isolated_worktree(live_main, school)
    report, report_path = run_stage1_tool(
        worktree,
        candidate_request,
        candidate_zip,
        None,
        None,
        diag / "stage1",
    )
    validate_stage1_pass(report)

    phase0_cp = run(
        phase0_command(
            worktree,
            candidate_request,
            candidate_zip,
            None,
            None,
        ),
        cwd=worktree,
        check=False,
    )
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "phase0.log").write_text(phase0_cp.stdout, encoding="utf-8")
    if phase0_cp.returncode != 0:
        raise Stop(
            "SCOPE_SUPERSESSION_PERMANENT_PHASE0_FAILED\n"
            + phase0_cp.stdout[-10000:]
        )

    phase0_commit = git("rev-parse", "HEAD", cwd=worktree).stdout.strip()
    phase0_parent = git(
        "rev-parse",
        f"{phase0_commit}^",
        cwd=worktree,
    ).stdout.strip()
    if phase0_parent != live_main:
        raise Stop("SCOPE_SUPERSESSION_PHASE0_PARENT_MISMATCH")
    tree = git(
        "rev-parse",
        f"{phase0_commit}^{{tree}}",
        cwd=worktree,
    ).stdout.strip()

    phase0_changed = sorted(
        line.strip()
        for line in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            phase0_commit,
            cwd=worktree,
        ).stdout.splitlines()
        if line.strip()
    )
    allowed = phase0_allowed_paths(school)
    unexpected = sorted(set(phase0_changed) - allowed)
    if unexpected:
        raise Stop(
            "SCOPE_SUPERSESSION_PHASE0_DIFF_OUTSIDE_CONTRACT:"
            + ",".join(unexpected)
        )
    required_school = {
        f"schools/{school}/{name}" for name in REQUIRED_PACKAGE_FILES
    }
    if not required_school.issubset(set(phase0_changed)):
        raise Stop("SCOPE_SUPERSESSION_PHASE0_SIX_FILE_INCOMPLETE")

    freeze_path = worktree / ".onboarding" / school / "integration-freeze.json"
    if not freeze_path.is_file():
        raise Stop("SCOPE_SUPERSESSION_INTEGRATION_FREEZE_MISSING")
    freeze_bytes = augment_integration_freeze(
        freeze_path.read_bytes(),
        request=request,
        spec=authority["spec"],
        proof=proof,
        candidate_zip_sha256=candidate_sha,
    )
    freeze_path.write_bytes(freeze_bytes)
    integration = json.loads(freeze_bytes)

    ancestry = run(
        ["git", "merge-base", "--is-ancestor", live_main, target_sha],
        cwd=worktree,
        check=False,
    )
    commit_tree_args = ["commit-tree", tree, "-p", target_sha]
    prepared_main_parent = None
    if ancestry.returncode != 0:
        commit_tree_args.extend(["-p", live_main])
        prepared_main_parent = live_main
    commit_tree_args.extend(
        [
            "-m",
            f"Supersede {school.replace('-', ' ').title()} public history scope",
        ]
    )
    prepared = git(*commit_tree_args, cwd=worktree).stdout.strip()
    parent_line = git(
        "rev-list",
        "--parents",
        "-n",
        "1",
        prepared,
        cwd=worktree,
    ).stdout.strip().split()
    expected_parents = [target_sha]
    if prepared_main_parent:
        expected_parents.append(prepared_main_parent)
    if parent_line[1:] != expected_parents:
        raise Stop("SCOPE_SUPERSESSION_PREPARED_PARENT_SET_MISMATCH")
    prepared_parent = target_sha
    prepared_tree = git(
        "rev-parse",
        f"{prepared}^{{tree}}",
        cwd=worktree,
    ).stdout.strip()
    if prepared_tree != tree:
        raise Stop("SCOPE_SUPERSESSION_REPARENT_FAILED")

    changed = sorted(
        line.strip()
        for line in git(
            "diff",
            "--name-only",
            target_sha,
            prepared,
            cwd=worktree,
        ).stdout.splitlines()
        if line.strip()
    )
    unexpected = sorted(set(changed) - allowed)
    if unexpected:
        raise Stop(
            "SCOPE_SUPERSESSION_PREPARED_DIFF_OUTSIDE_CONTRACT:"
            + ",".join(unexpected)
        )

    package_hashes = integration.get("package_member_sha256") or {}
    for name in REQUIRED_PACKAGE_FILES:
        actual = sha256_bytes(
            git_show_bytes(
                prepared,
                f"schools/{school}/{name}",
                cwd=worktree,
            )
        )
        if actual != package_hashes.get(name):
            raise Stop("SCOPE_SUPERSESSION_PACKAGE_HASH_MISMATCH:" + name)

    return {
        "worktree": worktree,
        "prepared_commit_sha": prepared,
        "prepared_parent_sha": prepared_parent,
        "prepared_main_parent_sha": prepared_main_parent,
        "prepared_tree_sha": prepared_tree,
        "changed_paths": changed,
        "changed_file_sha256": commit_file_hashes(worktree, prepared, changed),
        "allowed_paths": sorted(allowed),
        "candidate_zip_sha256": candidate_sha,
        "candidate_package_member_sha256": {
            name: sha256_bytes(candidate_members[name])
            for name in REQUIRED_PACKAGE_FILES
        },
        "original_research_member_sha256": original_info["member_sha256"],
        "stage1_report_path": report_path,
        "stage1_report_sha256": sha256_file(report_path),
        "proof": proof,
        "proof_sha256": proof_sha256(proof),
        "freeze_bytes": freeze_bytes,
        "integration_freeze_sha256": sha256_bytes(freeze_bytes),
        "semantic_snapshot_sha256": (
            integration.get("source_game_semantic_guard") or {}
        ).get("snapshot_sha256"),
        "history_scope": integration.get("history_scope"),
        "venue_mapping": integration.get("venue_mapping"),
        "conference_mapping": integration.get("conference_mapping"),
        "program_alias_mapping": integration.get("program_alias_mapping"),
        "repository_validation": "PASS",
    }


def finalize_scope_supersession_successor(
    *,
    active: dict[str, Any],
    original_request: dict[str, Any],
    request_sha256: str,
    live_main: str,
    writeahead: dict[str, Any],
    writeahead_path: str,
    writeahead_sha256: str,
    writeahead_commit: str | None,
    expected_remote: str,
    publication_cas: str,
    extra_commit_paths: list[Path | str] | None = None,
    recovery_request_id: str | None = None,
    recovery_classification: str | None = None,
) -> str:
    school = original_request["school_key"]
    rid = original_request["request_id"]
    prepared = writeahead["prepared_commit_sha"]
    target_branch = original_request["target_branch"]
    if remote_head(ROOT, target_branch) != prepared:
        raise Stop("SCOPE_SUPERSESSION_TARGET_NOT_PREPARED_COMMIT")

    successor_dir = Path(
        f".remote-implementation/successors/{school}/{rid}"
    )
    successor_dir.mkdir(parents=True, exist_ok=True)
    successor = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_SUCCESSOR",
        "operation": OP_PHASE0_SCOPE_SUPERSESSION,
        "request_id": rid,
        "request_sha256": request_sha256,
        "school_key": school,
        "global_lock_commit": active["active_lock_commit"],
        "writeahead_commit": writeahead_commit,
        "writeahead_manifest_path": writeahead_path,
        "writeahead_manifest_sha256": writeahead_sha256,
        "protected_main_sha": live_main,
        "target_branch": target_branch,
        "expected_target_predecessor_sha": writeahead[
            "expected_target_predecessor_sha"
        ],
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": writeahead["prepared_tree_sha"],
        "prepared_parent_sha": writeahead["prepared_parent_sha"],
        "prepared_main_parent_sha": writeahead.get("prepared_main_parent_sha"),
        "actual_published_target_sha": prepared,
        "changed_paths": writeahead["changed_paths"],
        "changed_file_sha256": writeahead["changed_file_sha256"],
        "integration_freeze_sha256": writeahead[
            "integration_freeze_sha256"
        ],
        "semantic_snapshot_sha256": writeahead[
            "semantic_snapshot_sha256"
        ],
        "candidate_zip_sha256": writeahead["candidate_zip_sha256"],
        "scope_supersession_spec_sha256": writeahead[
            "scope_supersession_spec_sha256"
        ],
        "scope_supersession_proof_sha256": writeahead[
            "scope_supersession_proof_sha256"
        ],
        "repository_validation": "PASS",
        "publication_cas": publication_cas,
        "recovery_request_id": recovery_request_id,
        "recovery_classification": recovery_classification,
        "final_transaction_state": "COMPLETE",
    }
    successor_path = successor_dir / "successor-manifest.json"
    write_json(successor_path, successor)
    successor_sha = sha256_file(successor_path)

    final_state = finalize_success(
        active,
        request_id=rid,
        last_operation={
            "operation": OP_PHASE0_SCOPE_SUPERSESSION,
            "request_id": rid,
            "school_key": school,
            "protected_main_sha": live_main,
            "target_branch": target_branch,
            "target_predecessor_sha": writeahead[
                "expected_target_predecessor_sha"
            ],
            "target_sha": prepared,
            "writeahead_manifest_path": writeahead_path,
            "writeahead_manifest_sha256": writeahead_sha256,
            "successor_manifest_path": successor_path.as_posix(),
            "successor_manifest_sha256": successor_sha,
            "integration_freeze_sha256": writeahead[
                "integration_freeze_sha256"
            ],
            "semantic_snapshot_sha256": writeahead[
                "semantic_snapshot_sha256"
            ],
            "candidate_zip_sha256": writeahead["candidate_zip_sha256"],
            "scope_supersession_spec_sha256": writeahead[
                "scope_supersession_spec_sha256"
            ],
            "scope_supersession_proof_sha256": writeahead[
                "scope_supersession_proof_sha256"
            ],
            "fresh_runner_verification": "PENDING",
            "remote_phase0_scope_supersession_equivalence": "PENDING",
            "recovery_request_id": recovery_request_id,
            "recovery_classification": recovery_classification,
        },
    )
    if recovery_request_id and recovery_request_id not in final_state[
        "consumed_request_ids"
    ]:
        final_state["consumed_request_ids"].append(recovery_request_id)
    write_json(STATE_PATH, final_state)
    paths: list[Path | str] = [STATE_PATH, successor_dir]
    if extra_commit_paths:
        paths.extend(extra_commit_paths)
    return commit_control(
        expected_remote,
        f"finalize Phase 0 scope supersession {rid}",
        paths,
    )


def run_phase0_scope_supersession(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
    diag: Path,
) -> None:
    authority = verify_scope_supersession_authority(
        state=state,
        request=request,
        request_commit=request_commit,
        predecessor_commit=predecessor_commit,
        live_main=live_main,
    )
    target_branch = request["target_branch"]
    target_before = request["target_sha"]

    run_id = __import__("os").environ.get("GITHUB_RUN_ID", "local")
    attempt = __import__("os").environ.get("GITHUB_RUN_ATTEMPT", "1")
    active = begin_request(
        state,
        request,
        sha256_bytes(request_bytes),
        run_id=run_id,
        run_attempt=attempt,
        request_commit=request_commit,
    )
    write_json(STATE_PATH, active)

    archive = Path(
        f".remote-implementation/requests/{request['request_id']}/request.json"
    )
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(request_bytes)
    lock_commit = commit_control(
        request_commit,
        f"acquire global Implementation lock {request['request_id']}",
        [STATE_PATH, archive],
    )
    active = bind_lock_commit(active, lock_commit)
    write_json(STATE_PATH, active)
    lock_bound_commit = commit_control(
        lock_commit,
        f"bind global Implementation lock {request['request_id']}",
        [STATE_PATH],
    )

    prepared = prepare_scope_supersession(
        request=request,
        authority=authority,
        live_main=live_main,
        diag=diag / "scope-supersession",
    )
    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, target_branch) != target_before:
        raise Stop("SCOPE_SUPERSESSION_TARGET_CHANGED_BEFORE_WRITEAHEAD")

    input_dir = Path(
        f".remote-implementation/phase0-inputs/{request['school_key']}/"
        f"{request['request_id']}"
    )
    input_dir.mkdir(parents=True, exist_ok=True)
    (input_dir / "scope-supersession.json").write_bytes(
        authority["spec_bytes"]
    )
    shutil.copyfile(
        prepared["stage1_report_path"],
        input_dir / "stage1-reconciliation.json",
    )
    write_json(input_dir / "scope-supersession-proof.json", prepared["proof"])
    input_sidecars = {
        name: sha256_file(input_dir / name)
        for name in (
            "scope-supersession.json",
            "stage1-reconciliation.json",
            "scope-supersession-proof.json",
        )
    }
    write_json(
        input_dir / "input-manifest.json",
        {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_SCOPE_SUPERSESSION_INPUTS",
            "request_id": request["request_id"],
            "school_key": request["school_key"],
            "protected_main_sha": live_main,
            "target_predecessor_sha": target_before,
            "original_research_checkpoint_sha256": request[
                "research_checkpoint"
            ]["sha256"],
            "candidate_zip_sha256": prepared["candidate_zip_sha256"],
            "sidecars": input_sidecars,
            "stage1_status": "PASS",
        },
    )
    active["transaction_state"] = "INPUTS_VERIFIED"
    write_json(STATE_PATH, active)
    inputs_commit = commit_control(
        lock_bound_commit,
        f"persist authenticated scope supersession inputs {request['request_id']}",
        [STATE_PATH, input_dir],
    )

    writeahead_dir = Path(
        f".remote-implementation/writeahead/{request['school_key']}/"
        f"{request['request_id']}"
    )
    writeahead_dir.mkdir(parents=True, exist_ok=True)
    (writeahead_dir / "integration-freeze.json").write_bytes(
        prepared["freeze_bytes"]
    )
    (writeahead_dir / "scope-supersession.json").write_bytes(
        authority["spec_bytes"]
    )
    write_json(
        writeahead_dir / "scope-supersession-proof.json",
        prepared["proof"],
    )
    shutil.copyfile(
        prepared["stage1_report_path"],
        writeahead_dir / "stage1-reconciliation.json",
    )
    sidecars = {
        name: sha256_file(writeahead_dir / name)
        for name in (
            "integration-freeze.json",
            "scope-supersession.json",
            "scope-supersession-proof.json",
            "stage1-reconciliation.json",
        )
    }
    writeahead = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
        "operation": OP_PHASE0_SCOPE_SUPERSESSION,
        "request_id": request["request_id"],
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": request["school_key"],
        "global_lock_commit": lock_commit,
        "protected_main_sha": live_main,
        "original_research_checkpoint_sha256": request[
            "research_checkpoint"
        ]["sha256"],
        "research_base_sha": request["research_checkpoint"][
            "research_base_sha"
        ],
        "target_branch": target_branch,
        "expected_target_predecessor_sha": target_before,
        "prepared_commit_sha": prepared["prepared_commit_sha"],
        "prepared_tree_sha": prepared["prepared_tree_sha"],
        "prepared_parent_sha": prepared["prepared_parent_sha"],
        "prepared_main_parent_sha": prepared["prepared_main_parent_sha"],
        "commit_message": (
            f"Supersede {request['school_key'].replace('-', ' ').title()} "
            "public history scope"
        ),
        "changed_paths": prepared["changed_paths"],
        "changed_file_sha256": prepared["changed_file_sha256"],
        "allowed_paths": prepared["allowed_paths"],
        "sidecars": sidecars,
        "candidate_zip_sha256": prepared["candidate_zip_sha256"],
        "candidate_package_member_sha256": prepared[
            "candidate_package_member_sha256"
        ],
        "original_research_member_sha256": prepared[
            "original_research_member_sha256"
        ],
        "scope_supersession_spec_sha256": sha256_bytes(
            authority["spec_bytes"]
        ),
        "scope_supersession_proof_sha256": prepared["proof_sha256"],
        "superseded_phase0_successor_sha256": request[
            "superseded_phase0_successor"
        ]["sha256"],
        "superseded_successor_sha256": request["superseded_successor"][
            "sha256"
        ],
        "superseded_integration_freeze_sha256": request[
            "superseded_integration_freeze_sha256"
        ],
        "superseded_semantic_snapshot_sha256": request[
            "superseded_semantic_snapshot_sha256"
        ],
        "integration_freeze_sha256": prepared[
            "integration_freeze_sha256"
        ],
        "package_member_sha256": json.loads(
            prepared["freeze_bytes"]
        ).get("package_member_sha256", {}),
        "semantic_snapshot_sha256": prepared[
            "semantic_snapshot_sha256"
        ],
        "history_scope": prepared["history_scope"],
        "venue_mapping": prepared["venue_mapping"],
        "conference_mapping": prepared["conference_mapping"],
        "program_alias_mapping": prepared["program_alias_mapping"],
        "repository_validation": "PASS",
        "mutation_state": "PREPARED_NOT_PUBLISHED",
    }
    writeahead_path = writeahead_dir / "writeahead-manifest.json"
    write_json(writeahead_path, writeahead)
    writeahead_sha = sha256_file(writeahead_path)

    active["transaction_state"] = "PREPARED_NOT_PUBLISHED"
    active["active_writeahead_path"] = writeahead_path.as_posix()
    active["active_writeahead_sha256"] = writeahead_sha
    active["active_prepared_commit_sha"] = prepared["prepared_commit_sha"]
    active["active_prepared_tree_sha"] = prepared["prepared_tree_sha"]
    write_json(STATE_PATH, active)
    writeahead_commit = commit_control(
        inputs_commit,
        f"publish scope supersession write-ahead {request['request_id']}",
        [STATE_PATH, writeahead_dir],
    )
    active["active_writeahead_commit"] = writeahead_commit
    write_json(STATE_PATH, active)
    writeahead_bound_commit = commit_control(
        writeahead_commit,
        f"bind scope supersession write-ahead {request['request_id']}",
        [STATE_PATH],
    )

    assert_protected_main_unchanged(live_main)
    publish_ref_cas(
        ROOT,
        branch=target_branch,
        prepared_commit=prepared["prepared_commit_sha"],
        expected_predecessor=target_before,
    )
    if remote_head(ROOT, target_branch) != prepared["prepared_commit_sha"]:
        raise Stop("SCOPE_SUPERSESSION_TARGET_PUBLICATION_VERIFY_FAILED")

    successor_commit = finalize_scope_supersession_successor(
        active=active,
        original_request=request,
        request_sha256=sha256_bytes(request_bytes),
        live_main=live_main,
        writeahead=writeahead,
        writeahead_path=writeahead_path.as_posix(),
        writeahead_sha256=writeahead_sha,
        writeahead_commit=writeahead_commit,
        expected_remote=writeahead_bound_commit,
        publication_cas="EXISTING_REF_CAS_PASS",
    )
    print(
        "REMOTE PHASE 0 SCOPE SUPERSESSION: COMPLETE "
        f"target={prepared['prepared_commit_sha']} "
        f"successor_commit={successor_commit}"
    )


def verify_scope_supersession_equivalence(
    *,
    live_main: str,
    control_head: str,
    state: dict[str, Any],
    diag: Path,
) -> int:
    """Independently reconstruct one completed scope-supersession successor."""

    last = state.get("last_operation") or {}
    if last.get("fresh_runner_verification") == "PASS":
        print("REMOTE PHASE 0 SCOPE SUPERSESSION EQUIVALENCE: PASS (already verified)")
        return 0

    successor_path = last["successor_manifest_path"]
    successor_bytes = git_show_bytes(control_head, successor_path)
    if sha256_bytes(successor_bytes) != last["successor_manifest_sha256"]:
        raise Stop("SCOPE_SUPERSESSION_FRESH_SUCCESSOR_HASH_MISMATCH")
    successor = json.loads(successor_bytes)
    if (
        successor.get("kind") != "REMOTE_IMPLEMENTATION_SUCCESSOR"
        or successor.get("operation") != OP_PHASE0_SCOPE_SUPERSESSION
        or successor.get("protected_main_sha") != live_main
        or successor.get("final_transaction_state") != "COMPLETE"
    ):
        raise Stop("SCOPE_SUPERSESSION_FRESH_SUCCESSOR_BINDING_MISMATCH")

    target_branch = successor["target_branch"]
    target_sha = remote_head(ROOT, target_branch)
    if target_sha != successor["prepared_commit_sha"]:
        raise Stop("SCOPE_SUPERSESSION_FRESH_TARGET_REF_MISMATCH")
    git(
        "fetch",
        "--no-tags",
        "origin",
        f"+refs/heads/{target_branch}:refs/remotes/origin/remote-target",
    )
    fetched_target = git(
        "rev-parse",
        "refs/remotes/origin/remote-target",
    ).stdout.strip()
    if fetched_target != target_sha:
        raise Stop("SCOPE_SUPERSESSION_FRESH_TARGET_FETCH_MISMATCH")
    parent_line = git(
        "rev-list", "--parents", "-n", "1", target_sha
    ).stdout.strip().split()
    target_parent = parent_line[1] if len(parent_line) > 1 else ""
    target_main_parent = parent_line[2] if len(parent_line) > 2 else None
    if len(parent_line) > 3:
        raise Stop("SCOPE_SUPERSESSION_FRESH_TOO_MANY_PARENTS")
    target_tree = git("rev-parse", f"{target_sha}^{{tree}}").stdout.strip()
    if (
        target_parent != successor["prepared_parent_sha"]
        or target_main_parent != successor.get("prepared_main_parent_sha")
        or target_tree != successor["prepared_tree_sha"]
    ):
        raise Stop("SCOPE_SUPERSESSION_FRESH_TARGET_COMMIT_MISMATCH")

    writeahead_path = successor["writeahead_manifest_path"]
    writeahead_bytes = git_show_bytes(control_head, writeahead_path)
    if sha256_bytes(writeahead_bytes) != successor["writeahead_manifest_sha256"]:
        raise Stop("SCOPE_SUPERSESSION_FRESH_WRITEAHEAD_HASH_MISMATCH")
    writeahead = json.loads(writeahead_bytes)
    if (
        writeahead.get("operation") != OP_PHASE0_SCOPE_SUPERSESSION
        or writeahead.get("protected_main_sha") != live_main
        or writeahead.get("prepared_commit_sha") != target_sha
        or writeahead.get("prepared_tree_sha") != target_tree
        or writeahead.get("prepared_parent_sha") != target_parent
        or writeahead.get("prepared_main_parent_sha") != target_main_parent
    ):
        raise Stop("SCOPE_SUPERSESSION_FRESH_WRITEAHEAD_BINDING_MISMATCH")

    prefix = Path(writeahead_path).parent
    bundle = Path(tempfile.mkdtemp(prefix="scope-supersession-fresh-sidecars-"))
    for relative in writeahead.get("sidecars") or {}:
        path = bundle / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(
            git_show_bytes(
                control_head,
                (prefix / relative).as_posix(),
            )
        )
    verify_sidecar_hashes(writeahead, bundle)

    request_path = (
        f".remote-implementation/requests/{successor['request_id']}/request.json"
    )
    request_bytes = git_show_bytes(control_head, request_path)
    if sha256_bytes(request_bytes) != successor["request_sha256"]:
        raise Stop("SCOPE_SUPERSESSION_FRESH_REQUEST_HASH_MISMATCH")
    request = json.loads(request_bytes)
    if (
        request.get("operation") != OP_PHASE0_SCOPE_SUPERSESSION
        or request.get("expected_protected_main_sha") != live_main
        or request.get("target_branch") != target_branch
        or request.get("target_sha") != target_parent
    ):
        raise Stop("SCOPE_SUPERSESSION_FRESH_REQUEST_BINDING_MISMATCH")

    spec_bytes = (bundle / "scope-supersession.json").read_bytes()
    if sha256_bytes(spec_bytes) != request["scope_supersession_spec"]["sha256"]:
        raise Stop("SCOPE_SUPERSESSION_FRESH_SPEC_HASH_MISMATCH")
    spec = validate_scope_supersession_spec(
        json.loads(spec_bytes),
        school_key=request["school_key"],
    )

    # Re-authenticate the superseded durable authority chain independently.
    phase0, _ = _read_json_ref(
        control_head,
        request["superseded_phase0_successor"],
        code="SCOPE_SUPERSESSION_FRESH_PHASE0_SUCCESSOR",
    )
    current, _ = _read_json_ref(
        control_head,
        request["superseded_successor"],
        code="SCOPE_SUPERSESSION_FRESH_CURRENT_SUCCESSOR",
    )
    if (
        phase0.get("integration_freeze_sha256")
        != request["superseded_integration_freeze_sha256"]
        or phase0.get("semantic_snapshot_sha256")
        != request["superseded_semantic_snapshot_sha256"]
        or current.get("actual_published_target_sha") != target_parent
        or current.get("integration_freeze_sha256")
        != request["superseded_integration_freeze_sha256"]
        or current.get("semantic_snapshot_sha256")
        != request["superseded_semantic_snapshot_sha256"]
    ):
        raise Stop("SCOPE_SUPERSESSION_FRESH_SUPERSEDED_AUTHORITY_MISMATCH")

    rebuilt = prepare_scope_supersession(
        request=request,
        authority={"spec": spec, "spec_bytes": spec_bytes},
        live_main=live_main,
        diag=diag / "scope-supersession",
    )
    stored_proof = json.loads(
        (bundle / "scope-supersession-proof.json").read_text(encoding="utf-8")
    )
    if rebuilt["proof"] != stored_proof:
        raise Stop("SCOPE_SUPERSESSION_FRESH_PROOF_MISMATCH")
    comparisons = {
        "prepared_tree_sha": target_tree,
        "candidate_zip_sha256": writeahead["candidate_zip_sha256"],
        "integration_freeze_sha256": writeahead["integration_freeze_sha256"],
        "semantic_snapshot_sha256": writeahead["semantic_snapshot_sha256"],
        "proof_sha256": writeahead["scope_supersession_proof_sha256"],
    }
    for field, expected in comparisons.items():
        if rebuilt.get(field) != expected:
            raise Stop("SCOPE_SUPERSESSION_FRESH_REBUILD_MISMATCH:" + field)
    if rebuilt["changed_paths"] != writeahead["changed_paths"]:
        raise Stop("SCOPE_SUPERSESSION_FRESH_CHANGED_PATH_MISMATCH")
    if rebuilt["changed_file_sha256"] != writeahead["changed_file_sha256"]:
        raise Stop("SCOPE_SUPERSESSION_FRESH_CHANGED_FILE_HASH_MISMATCH")
    if rebuilt["candidate_package_member_sha256"] != writeahead[
        "candidate_package_member_sha256"
    ]:
        raise Stop("SCOPE_SUPERSESSION_FRESH_CANDIDATE_MEMBER_MISMATCH")

    verification = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_PHASE0_SCOPE_SUPERSESSION_VERIFICATION",
        "request_id": successor["request_id"],
        "school_key": successor["school_key"],
        "protected_main_sha": live_main,
        "target_branch": target_branch,
        "target_predecessor_sha": target_parent,
        "target_sha": target_sha,
        "target_tree_sha": target_tree,
        "original_research_checkpoint_sha256": request[
            "research_checkpoint"
        ]["sha256"],
        "candidate_zip_sha256": rebuilt["candidate_zip_sha256"],
        "scope_supersession_spec_sha256": sha256_bytes(spec_bytes),
        "scope_supersession_proof_sha256": rebuilt["proof_sha256"],
        "excluded_source_game_count": rebuilt["proof"][
            "excluded_source_game_count"
        ],
        "retained_source_game_count": rebuilt["proof"][
            "source_game_count_after"
        ],
        "retained_semantic_equivalence": rebuilt["proof"][
            "retained_semantic_equivalence"
        ],
        "integration_freeze_sha256": rebuilt[
            "integration_freeze_sha256"
        ],
        "semantic_snapshot_sha256": rebuilt["semantic_snapshot_sha256"],
        "repository_validation": "PASS",
        "remote_phase0_scope_supersession_equivalence": "PASS",
    }
    verify_dir = Path(
        f".remote-implementation/verifications/{successor['school_key']}/"
        f"{successor['request_id']}"
    )
    write_json(
        verify_dir / "phase0-scope-supersession-verification.json",
        verification,
    )

    local_state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    validate_control_state(local_state)
    local_last = local_state.get("last_operation") or {}
    if (
        local_last.get("operation") != OP_PHASE0_SCOPE_SUPERSESSION
        or local_last.get("request_id") != successor["request_id"]
        or local_last.get("target_sha") != target_sha
    ):
        raise Stop("SCOPE_SUPERSESSION_FRESH_CONTROL_MOVED")
    local_last["fresh_runner_verification"] = "PASS"
    local_last["remote_phase0_scope_supersession_equivalence"] = "PASS"
    local_state["last_operation"] = local_last
    write_json(STATE_PATH, local_state)
    commit = commit_control(
        control_head,
        f"persist fresh Phase 0 scope supersession verification "
        f"{successor['request_id']}",
        [STATE_PATH, verify_dir],
    )
    print(
        "REMOTE PHASE 0 SCOPE SUPERSESSION EQUIVALENCE: PASS "
        f"verification_commit={commit}"
    )
    return 0
