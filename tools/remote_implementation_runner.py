#!/usr/bin/env python3
"""Request processor for the guarded remote Implementation control plane."""
from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from remote_implementation_control import (
    MUTATION_COMPLETE,
    MUTATION_DIVERGED,
    MUTATION_NOT_ATTEMPTED,
    MUTATION_PREPARED,
    MUTATION_PUBLISHED,
    OP_PHASE0,
    OP_RECOVER,
    OP_STAGE1,
    RemoteImplementationError,
    abandon_active,
    begin_request,
    bind_lock_commit,
    classify_mutation,
    finalize_success,
    publish_ref_cas,
    request_used,
    sha256_bytes,
    sha256_file,
    validate_request,
    verify_request_predecessor,
    verify_sidecar_hashes,
)
from remote_implementation_io import (
    CONTROL_BRANCH,
    INTERNAL_PREFIX,
    REQUEST_PATH,
    REQUIRED_PACKAGE_FILES,
    ROOT,
    STATE_PATH,
    Stop,
    add_isolated_worktree,
    commit_control,
    commit_file_hashes,
    configure_git,
    fetch_operational_refs,
    git,
    git_show_bytes,
    git_show_json,
    materialize_payload,
    materialize_research_checkpoint,
    phase0_allowed_paths,
    phase0_command,
    read_json,
    remote_head,
    run,
    run_stage1_tool,
    validate_stage1_pass,
    write_json,
)

DIAG = Path(
    os.environ.get(
        "REMOTE_IMPLEMENTATION_DIAG",
        "/tmp/remote-implementation-diagnostics",
    )
)


def archive_request(request: dict[str, Any], request_bytes: bytes) -> Path:
    path = Path(
        ".remote-implementation/requests/%s/request.json" % request["request_id"]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(request_bytes)
    return path


def persist_stage1_checkpoint(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    live_main: str,
    report: dict[str, Any],
    report_path: Path,
    package_info: dict[str, Any],
    venue_spec: Path | None,
    conference_spec: Path | None,
    expected_remote: str,
) -> str:
    rid = request["request_id"]
    school = request["school_key"]
    directory = Path(
        ".remote-implementation/checkpoints/%s/%s" % (school, rid)
    )
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "request.json").write_bytes(request_bytes)
    shutil.copyfile(report_path, directory / "stage1-reconciliation.json")
    sidecars = {
        "request.json": sha256_file(directory / "request.json"),
        "stage1-reconciliation.json": sha256_file(
            directory / "stage1-reconciliation.json"
        ),
    }
    if venue_spec:
        shutil.copyfile(venue_spec, directory / "venue-reconciliation.json")
        sidecars["venue-reconciliation.json"] = sha256_file(
            directory / "venue-reconciliation.json"
        )
    if conference_spec:
        shutil.copyfile(
            conference_spec,
            directory / "conference-reconciliation.json",
        )
        sidecars["conference-reconciliation.json"] = sha256_file(
            directory / "conference-reconciliation.json"
        )
    manifest = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE1_CHECKPOINT",
        "request_id": rid,
        "school_key": school,
        "protected_main_sha": live_main,
        "research_checkpoint_sha256": request["research_checkpoint"]["sha256"],
        "research_base_sha": request["research_checkpoint"]["research_base_sha"],
        "research_member_sha256": package_info["member_sha256"],
        "stage1_status": report.get("status"),
        "stage1_blocker_count": report.get("blocker_count"),
        "sidecars": sidecars,
        "authority_statement": (
            "Durable remote Stage 1 checkpoint only. A new bounded PHASE0 request "
            "is required before tracked mutation."
        ),
    }
    manifest_path = directory / "checkpoint-manifest.json"
    write_json(manifest_path, manifest)
    manifest_sha = sha256_file(manifest_path)
    final_state = finalize_success(
        state,
        request_id=rid,
        last_operation={
            "operation": OP_STAGE1,
            "request_id": rid,
            "school_key": school,
            "protected_main_sha": live_main,
            "checkpoint_manifest_path": manifest_path.as_posix(),
            "checkpoint_manifest_sha256": manifest_sha,
            "stage1_status": report.get("status"),
            "stage1_reconciliation_sha256": sidecars[
                "stage1-reconciliation.json"
            ],
        },
        transaction_state="IDLE",
    )
    write_json(STATE_PATH, final_state)
    return commit_control(
        expected_remote,
        "finalize Stage 1 checkpoint %s" % rid,
        [STATE_PATH, directory],
    )


def verify_stage1_checkpoint_reference(
    request: dict[str, Any],
    predecessor_commit: str,
    live_main: str,
) -> dict[str, Any]:
    ref = request["stage1_checkpoint"]
    data = git_show_bytes(predecessor_commit, ref["path"])
    if sha256_bytes(data) != ref["sha256"]:
        raise Stop("STAGE1_CHECKPOINT_MANIFEST_HASH_MISMATCH")
    manifest = json.loads(data)
    if manifest.get("kind") != "REMOTE_IMPLEMENTATION_STAGE1_CHECKPOINT":
        raise Stop("STAGE1_CHECKPOINT_KIND_MISMATCH")
    if manifest.get("school_key") != request["school_key"]:
        raise Stop("STAGE1_CHECKPOINT_SCHOOL_MISMATCH")
    if manifest.get("protected_main_sha") != live_main:
        raise Stop("STAGE1_CHECKPOINT_STALE_MAIN")
    if (
        manifest.get("research_checkpoint_sha256")
        != request["research_checkpoint"]["sha256"]
    ):
        raise Stop("STAGE1_CHECKPOINT_RESEARCH_MISMATCH")
    if manifest.get("stage1_status") != "PASS":
        raise Stop("STAGE1_CHECKPOINT_NOT_PASS")
    report_hash = (manifest.get("sidecars") or {}).get(
        "stage1-reconciliation.json"
    )
    if not report_hash:
        raise Stop("STAGE1_CHECKPOINT_REPORT_HASH_MISSING")
    report_path = (
        Path(ref["path"]).parent / "stage1-reconciliation.json"
    ).as_posix()
    if sha256_bytes(git_show_bytes(predecessor_commit, report_path)) != report_hash:
        raise Stop("STAGE1_CHECKPOINT_REPORT_HASH_MISMATCH")
    return manifest


def run_read_only_stage1(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    live_main: str,
) -> None:
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
    archive = archive_request(request, request_bytes)
    accepted_commit = commit_control(
        request_commit,
        "accept read-only request %s" % request["request_id"],
        [STATE_PATH, archive],
    )

    scratch = Path(tempfile.mkdtemp(prefix="remote-stage1-inputs-"))
    package = scratch / "research-frozen.zip"
    package_info = materialize_research_checkpoint(request, package)
    venue_spec = materialize_payload(
        request_commit,
        request.get("venue_reconciliation"),
        scratch / "venue-reconciliation.json",
    )
    conference_spec = materialize_payload(
        request_commit,
        request.get("conference_reconciliation"),
        scratch / "conference-reconciliation.json",
    )
    worktree = add_isolated_worktree(live_main, request["school_key"])
    report, report_path = run_stage1_tool(
        worktree,
        request,
        package,
        venue_spec,
        conference_spec,
        DIAG,
    )
    checkpoint_commit = persist_stage1_checkpoint(
        state=active,
        request=request,
        request_bytes=request_bytes,
        live_main=live_main,
        report=report,
        report_path=report_path,
        package_info=package_info,
        venue_spec=venue_spec,
        conference_spec=conference_spec,
        expected_remote=accepted_commit,
    )
    print(
        "REMOTE STAGE 1 CHECKPOINT: %s commit=%s"
        % (report.get("status"), checkpoint_commit)
    )


def run_phase0(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    verify_stage1_checkpoint_reference(
        request,
        predecessor_commit,
        live_main,
    )
    target_branch = request["target_branch"]
    if remote_head(ROOT, target_branch) is not None:
        raise Stop("ONBOARDING_TARGET_ALREADY_EXISTS")

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
    archive = archive_request(request, request_bytes)
    lock_commit = commit_control(
        request_commit,
        "acquire global Implementation lock %s" % request["request_id"],
        [STATE_PATH, archive],
    )
    active = bind_lock_commit(active, lock_commit)
    write_json(STATE_PATH, active)
    lock_bound_commit = commit_control(
        lock_commit,
        "bind global Implementation lock %s" % request["request_id"],
        [STATE_PATH],
    )
    print("GLOBAL IMPLEMENTATION LOCK: ACQUIRED %s" % lock_commit)

    scratch = Path(tempfile.mkdtemp(prefix="remote-phase0-inputs-"))
    package = scratch / "research-frozen.zip"
    package_info = materialize_research_checkpoint(request, package)
    venue_spec = materialize_payload(
        request_commit,
        request.get("venue_reconciliation"),
        scratch / "venue-reconciliation.json",
    )
    conference_spec = materialize_payload(
        request_commit,
        request.get("conference_reconciliation"),
        scratch / "conference-reconciliation.json",
    )
    worktree = add_isolated_worktree(live_main, request["school_key"])
    report, report_path = run_stage1_tool(
        worktree,
        request,
        package,
        venue_spec,
        conference_spec,
        DIAG,
    )
    validate_stage1_pass(report)

    input_dir = Path(
        ".remote-implementation/phase0-inputs/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    input_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(report_path, input_dir / "stage1-reconciliation.json")
    input_sidecars = {
        "stage1-reconciliation.json": sha256_file(
            input_dir / "stage1-reconciliation.json"
        )
    }
    if venue_spec:
        shutil.copyfile(venue_spec, input_dir / "venue-reconciliation.json")
        input_sidecars["venue-reconciliation.json"] = sha256_file(
            input_dir / "venue-reconciliation.json"
        )
    if conference_spec:
        shutil.copyfile(
            conference_spec,
            input_dir / "conference-reconciliation.json",
        )
        input_sidecars["conference-reconciliation.json"] = sha256_file(
            input_dir / "conference-reconciliation.json"
        )
    write_json(
        input_dir / "input-manifest.json",
        {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_PHASE0_INPUTS",
            "request_id": request["request_id"],
            "school_key": request["school_key"],
            "protected_main_sha": live_main,
            "research_checkpoint_sha256": request["research_checkpoint"][
                "sha256"
            ],
            "research_member_sha256": package_info["member_sha256"],
            "sidecars": input_sidecars,
            "stage1_status": "PASS",
        },
    )
    active["transaction_state"] = "INPUTS_VERIFIED"
    write_json(STATE_PATH, active)
    inputs_commit = commit_control(
        lock_bound_commit,
        "persist authenticated Phase 0 inputs %s" % request["request_id"],
        [STATE_PATH, input_dir],
    )

    phase0_cp = run(
        phase0_command(
            worktree,
            request,
            package,
            venue_spec,
            conference_spec,
        ),
        cwd=worktree,
        check=False,
    )
    DIAG.mkdir(parents=True, exist_ok=True)
    (DIAG / "phase0.log").write_text(phase0_cp.stdout, encoding="utf-8")
    if phase0_cp.returncode != 0:
        raise Stop(
            "PERMANENT_PHASE0_COMMAND_FAILED\n" + phase0_cp.stdout[-10000:]
        )

    prepared = git("rev-parse", "HEAD", cwd=worktree).stdout.strip()
    parent = git(
        "rev-parse",
        "%s^" % prepared,
        cwd=worktree,
    ).stdout.strip()
    tree = git(
        "rev-parse",
        "%s^{tree}" % prepared,
        cwd=worktree,
    ).stdout.strip()
    message = git(
        "log",
        "-1",
        "--format=%B",
        prepared,
        cwd=worktree,
    ).stdout.strip()
    if parent != live_main:
        raise Stop("PHASE0_PARENT_MISMATCH")
    changed = sorted(
        line.strip()
        for line in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            prepared,
            cwd=worktree,
        ).stdout.splitlines()
        if line.strip()
    )
    allowed = phase0_allowed_paths(request["school_key"])
    unexpected = sorted(set(changed) - allowed)
    if unexpected:
        raise Stop(
            "PHASE0_DIFF_OUTSIDE_CONTRACT: " + ", ".join(unexpected)
        )
    required_school_paths = {
        "schools/%s/%s" % (request["school_key"], name)
        for name in REQUIRED_PACKAGE_FILES
    }
    if not required_school_paths.issubset(changed):
        raise Stop("PHASE0_SIX_FILE_COMMIT_INCOMPLETE")

    freeze_path = (
        worktree
        / ".onboarding"
        / request["school_key"]
        / "integration-freeze.json"
    )
    if not freeze_path.is_file():
        raise Stop("INTEGRATION_FREEZE_MISSING")
    freeze_bytes = freeze_path.read_bytes()
    freeze_sha = sha256_bytes(freeze_bytes)
    integration = json.loads(freeze_bytes)
    if integration.get("status") != "INTEGRATION_FROZEN":
        raise Stop("INTEGRATION_FREEZE_STATUS_MISMATCH")
    if (
        integration.get("integration_base_sha") != live_main
        or integration.get("origin_main_sha") != live_main
    ):
        raise Stop("INTEGRATION_FREEZE_MAIN_BINDING_MISMATCH")
    if (
        integration.get("research_zip_sha256")
        != request["research_checkpoint"]["sha256"]
        or integration.get("research_base_sha")
        != request["research_checkpoint"]["research_base_sha"]
    ):
        raise Stop("INTEGRATION_FREEZE_RESEARCH_BINDING_MISMATCH")

    package_hashes = integration.get("package_member_sha256") or {}
    for name in REQUIRED_PACKAGE_FILES:
        data = git_show_bytes(
            prepared,
            "schools/%s/%s" % (request["school_key"], name),
            cwd=worktree,
        )
        if sha256_bytes(data) != package_hashes.get(name):
            raise Stop(
                "INTEGRATION_FREEZE_PACKAGE_HASH_MISMATCH:%s" % name
            )

    changed_hashes = commit_file_hashes(worktree, prepared, changed)
    writeahead_dir = Path(
        ".remote-implementation/writeahead/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    writeahead_dir.mkdir(parents=True, exist_ok=True)
    (writeahead_dir / "integration-freeze.json").write_bytes(freeze_bytes)
    shutil.copyfile(
        input_dir / "stage1-reconciliation.json",
        writeahead_dir / "stage1-reconciliation.json",
    )
    sidecars = {
        "integration-freeze.json": sha256_file(
            writeahead_dir / "integration-freeze.json"
        ),
        "stage1-reconciliation.json": sha256_file(
            writeahead_dir / "stage1-reconciliation.json"
        ),
    }
    for name in (
        "venue-reconciliation.json",
        "conference-reconciliation.json",
    ):
        source = input_dir / name
        if source.is_file():
            shutil.copyfile(source, writeahead_dir / name)
            sidecars[name] = sha256_file(writeahead_dir / name)

    writeahead = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
        "request_id": request["request_id"],
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": request["school_key"],
        "global_lock_commit": lock_commit,
        "protected_main_sha": live_main,
        "research_checkpoint_sha256": request["research_checkpoint"]["sha256"],
        "research_base_sha": request["research_checkpoint"][
            "research_base_sha"
        ],
        "target_branch": target_branch,
        "expected_target_predecessor_sha": None,
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": tree,
        "prepared_parent_sha": parent,
        "commit_message": message,
        "changed_paths": changed,
        "changed_file_sha256": changed_hashes,
        "allowed_paths": sorted(allowed),
        "sidecars": sidecars,
        "integration_freeze_sha256": freeze_sha,
        "package_member_sha256": package_hashes,
        "semantic_snapshot_sha256": (
            integration.get("source_game_semantic_guard") or {}
        ).get("snapshot_sha256"),
        "venue_mapping": integration.get("venue_mapping"),
        "conference_mapping": integration.get("conference_mapping"),
        "program_alias_mapping": integration.get("program_alias_mapping"),
        "history_scope": integration.get("history_scope"),
        "venue_reconciliation": integration.get("venue_reconciliation"),
        "conference_reconciliation": integration.get(
            "conference_reconciliation"
        ),
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
        "publish Phase 0 write-ahead %s" % request["request_id"],
        [STATE_PATH, writeahead_dir],
    )
    active["active_writeahead_commit"] = writeahead_commit
    write_json(STATE_PATH, active)
    writeahead_bound_commit = commit_control(
        writeahead_commit,
        "bind Phase 0 write-ahead %s" % request["request_id"],
        [STATE_PATH],
    )

    publish_ref_cas(
        ROOT,
        branch=target_branch,
        prepared_commit=prepared,
        expected_predecessor=None,
    )
    actual_target = remote_head(ROOT, target_branch) if target_branch else None
    if actual_target != prepared:
        raise Stop("PHASE0_TARGET_PUBLICATION_VERIFY_FAILED")

    successor_dir = Path(
        ".remote-implementation/successors/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    successor_dir.mkdir(parents=True, exist_ok=True)
    successor = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_SUCCESSOR",
        "request_id": request["request_id"],
        "school_key": request["school_key"],
        "request_sha256": sha256_bytes(request_bytes),
        "global_lock_commit": lock_commit,
        "writeahead_commit": writeahead_commit,
        "writeahead_manifest_path": writeahead_path.as_posix(),
        "writeahead_manifest_sha256": writeahead_sha,
        "protected_main_sha": live_main,
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": tree,
        "prepared_parent_sha": parent,
        "actual_published_target_sha": actual_target,
        "target_branch": target_branch,
        "changed_paths": changed,
        "changed_file_sha256": changed_hashes,
        "integration_freeze_sha256": freeze_sha,
        "semantic_snapshot_sha256": writeahead[
            "semantic_snapshot_sha256"
        ],
        "repository_validation": "PASS",
        "publication_cas": "CREATE_ONCE_PASS",
        "final_transaction_state": "COMPLETE",
    }
    successor_path = successor_dir / "successor-manifest.json"
    write_json(successor_path, successor)
    successor_sha = sha256_file(successor_path)
    final_state = finalize_success(
        active,
        request_id=request["request_id"],
        last_operation={
            "operation": OP_PHASE0,
            "request_id": request["request_id"],
            "school_key": request["school_key"],
            "protected_main_sha": live_main,
            "target_branch": target_branch,
            "target_sha": actual_target,
            "writeahead_manifest_path": writeahead_path.as_posix(),
            "writeahead_manifest_sha256": writeahead_sha,
            "successor_manifest_path": successor_path.as_posix(),
            "successor_manifest_sha256": successor_sha,
            "integration_freeze_sha256": freeze_sha,
            "fresh_runner_verification": "PENDING",
            "remote_phase0_equivalence": "PENDING",
        },
    )
    write_json(STATE_PATH, final_state)
    successor_commit = commit_control(
        writeahead_bound_commit,
        "finalize stable Phase 0 %s" % request["request_id"],
        [STATE_PATH, successor_dir],
    )
    print(
        "REMOTE PHASE 0: COMPLETE target=%s successor_commit=%s"
        % (actual_target, successor_commit)
    )


def load_writeahead(
    commit: str,
    path: str,
    expected_sha: str,
) -> dict[str, Any]:
    data = git_show_bytes(commit, path)
    if sha256_bytes(data) != expected_sha:
        raise Stop("RECOVERY_WRITEAHEAD_HASH_MISMATCH")
    manifest = json.loads(data)
    temp = Path(tempfile.mkdtemp(prefix="remote-recovery-writeahead-"))
    prefix = Path(path).parent
    for relative in manifest.get("sidecars") or {}:
        target = temp / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(
            git_show_bytes(
                commit,
                (prefix / relative).as_posix(),
            )
        )
    verify_sidecar_hashes(manifest, temp)
    return manifest


def run_recovery(
    state: dict[str, Any],
    request: dict[str, Any],
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    recovery = request["recovery"]
    target_branch = recovery.get("target_branch")
    manifest = None
    if state.get("active_writeahead_path"):
        manifest = load_writeahead(
            predecessor_commit,
            state["active_writeahead_path"],
            state["active_writeahead_sha256"],
        )
    actual_target = (
        remote_head(ROOT, target_branch)
        if target_branch
        else None
    )
    classification = classify_mutation(
        manifest.get("expected_target_predecessor_sha")
        if manifest
        else None,
        actual_target,
        manifest=manifest,
    )
    if classification == MUTATION_DIVERGED:
        raise Stop("RECOVERY_DIVERGED_STOP")

    directory = Path(
        ".remote-implementation/recoveries/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    directory.mkdir(parents=True, exist_ok=True)
    recovery_manifest = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_RECOVERY",
        "request_id": request["request_id"],
        "recovered_request_id": recovery["abandoned_request_id"],
        "lock_commit": recovery.get("lock_commit"),
        "protected_main_sha": live_main,
        "target_branch": target_branch,
        "actual_target_sha": actual_target,
        "mutation_classification": classification,
    }
    write_json(directory / "recovery-manifest.json", recovery_manifest)
    commit_paths: list[Path | str] = [STATE_PATH, directory]

    if classification in {MUTATION_NOT_ATTEMPTED, MUTATION_PREPARED}:
        final_state = abandon_active(
            state,
            recovery_request_id=request["request_id"],
            disposition="ABANDONED_%s" % classification,
            recovery_manifest=recovery_manifest,
        )
    elif classification in {MUTATION_PUBLISHED, MUTATION_COMPLETE}:
        if not manifest:
            raise Stop("RECOVERY_PUBLISHED_WITHOUT_WRITEAHEAD")
        if manifest.get("protected_main_sha") != live_main:
            raise Stop("RECOVERY_PUBLISHED_STALE_PROTECTED_MAIN")
        prepared = manifest["prepared_commit_sha"]
        if not target_branch or actual_target != prepared:
            raise Stop("RECOVERY_TARGET_NOT_EXACT_PREPARED_COMMIT")
        parent = git("rev-parse", "%s^" % prepared).stdout.strip()
        tree = git("rev-parse", "%s^{tree}" % prepared).stdout.strip()
        if parent != manifest["prepared_parent_sha"]:
            raise Stop("RECOVERY_PREPARED_PARENT_MISMATCH")
        if tree != manifest["prepared_tree_sha"]:
            raise Stop("RECOVERY_PREPARED_TREE_MISMATCH")
        changed = sorted(
            line.strip()
            for line in git(
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "-r",
                prepared,
            ).stdout.splitlines()
            if line.strip()
        )
        if changed != sorted(manifest["changed_paths"]):
            raise Stop("RECOVERY_CHANGED_PATH_MISMATCH")
        for path, expected in manifest["changed_file_sha256"].items():
            if sha256_bytes(git_show_bytes(prepared, path)) != expected:
                raise Stop(
                    "RECOVERY_CHANGED_FILE_HASH_MISMATCH:%s" % path
                )

        original_request_id = state["active_request_id"]
        successor_dir = Path(
            ".remote-implementation/successors/%s/%s"
            % (request["school_key"], original_request_id)
        )
        successor_dir.mkdir(parents=True, exist_ok=True)
        successor = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_SUCCESSOR",
            "request_id": original_request_id,
            "school_key": request["school_key"],
            "request_sha256": state["active_request_sha256"],
            "global_lock_commit": state["active_lock_commit"],
            "writeahead_commit": state.get(
                "active_writeahead_commit"
            ),
            "writeahead_manifest_path": state[
                "active_writeahead_path"
            ],
            "writeahead_manifest_sha256": state[
                "active_writeahead_sha256"
            ],
            "protected_main_sha": live_main,
            "prepared_commit_sha": prepared,
            "prepared_tree_sha": tree,
            "prepared_parent_sha": parent,
            "actual_published_target_sha": actual_target,
            "target_branch": target_branch,
            "changed_paths": changed,
            "changed_file_sha256": manifest[
                "changed_file_sha256"
            ],
            "integration_freeze_sha256": manifest[
                "integration_freeze_sha256"
            ],
            "semantic_snapshot_sha256": manifest[
                "semantic_snapshot_sha256"
            ],
            "repository_validation": manifest[
                "repository_validation"
            ],
            "publication_cas": "RECOVERY_ADOPTION_EXACT_MATCH",
            "recovery_request_id": request["request_id"],
            "recovery_classification": classification,
            "final_transaction_state": "COMPLETE",
        }
        successor_path = (
            successor_dir / "successor-manifest.json"
        )
        write_json(successor_path, successor)
        successor_sha = sha256_file(successor_path)
        commit_paths.append(successor_dir)

        final_state = finalize_success(
            state,
            request_id=original_request_id,
            last_operation={
                "operation": OP_PHASE0,
                "request_id": original_request_id,
                "school_key": request["school_key"],
                "protected_main_sha": live_main,
                "target_branch": target_branch,
                "target_sha": actual_target,
                "writeahead_manifest_path": state[
                    "active_writeahead_path"
                ],
                "writeahead_manifest_sha256": state[
                    "active_writeahead_sha256"
                ],
                "successor_manifest_path": (
                    successor_path.as_posix()
                ),
                "successor_manifest_sha256": successor_sha,
                "integration_freeze_sha256": manifest[
                    "integration_freeze_sha256"
                ],
                "fresh_runner_verification": "PENDING",
                "remote_phase0_equivalence": "PENDING",
                "recovery_request_id": request["request_id"],
                "recovery_classification": classification,
            },
        )
        if request["request_id"] not in final_state[
            "consumed_request_ids"
        ]:
            final_state["consumed_request_ids"].append(
                request["request_id"]
            )
    else:
        raise Stop("RECOVERY_CLASSIFICATION_UNSUPPORTED")

    write_json(STATE_PATH, final_state)
    commit = commit_control(
        request_commit,
        "recover remote Implementation request %s"
        % request["request_id"],
        commit_paths,
    )
    print(
        "REMOTE IMPLEMENTATION RECOVERY: %s commit=%s"
        % (classification, commit)
    )


def verify_control_code_matches_main(
    request_commit: str,
    live_main: str,
) -> None:
    changed = [
        line.strip()
        for line in git(
            "diff",
            "--name-only",
            live_main,
            request_commit,
        ).stdout.splitlines()
        if line.strip()
    ]
    unexpected = [
        path
        for path in changed
        if not path.startswith(".remote-implementation/")
    ]
    if unexpected:
        raise Stop(
            "CONTROL_BRANCH_CODE_NOT_EXACT_PROTECTED_MAIN: "
            + ", ".join(unexpected)
        )


def main() -> int:
    DIAG.mkdir(parents=True, exist_ok=True)
    try:
        configure_git()
        if not REQUEST_PATH.is_file():
            print("REMOTE IMPLEMENTATION: no request present")
            return 0
        request_bytes = REQUEST_PATH.read_bytes()
        request = json.loads(request_bytes)
        validate_request(request)
        request_commit = os.environ.get(
            "GITHUB_SHA",
            git("rev-parse", "HEAD").stdout.strip(),
        )
        predecessor_commit = git(
            "rev-parse",
            "%s^" % request_commit,
        ).stdout.strip()
        target = request.get("target_branch") or (
            request.get("recovery") or {}
        ).get("target_branch")
        live_main, durable_head = fetch_operational_refs(target)

        if int(os.environ.get("GITHUB_RUN_ATTEMPT", "1")) > 1:
            durable_state = git_show_json(
                durable_head,
                STATE_PATH.as_posix(),
            )
            if request_used(durable_state, request["request_id"]):
                raise Stop("ACCEPTED_REQUEST_REPLAY_REFUSED")
            raise Stop(
                "RERUN_ATTEMPT_WITHOUT_DURABLE_ACCEPTANCE_IS_NOT_AUTHORIZED"
            )

        if durable_head != request_commit:
            raise Stop("CONTROL_BRANCH_MOVED_AFTER_REQUEST_EVENT")
        verify_control_code_matches_main(request_commit, live_main)

        state_bytes = git_show_bytes(
            predecessor_commit,
            STATE_PATH.as_posix(),
        )
        state = json.loads(state_bytes)
        verify_request_predecessor(
            state,
            state_bytes,
            predecessor_commit,
            request,
            live_main,
            allow_active_recovery=request["operation"] == OP_RECOVER,
        )

        if request["operation"] == OP_STAGE1:
            run_read_only_stage1(
                state,
                request,
                request_bytes,
                request_commit,
                live_main,
            )
        elif request["operation"] == OP_PHASE0:
            run_phase0(
                state,
                request,
                request_bytes,
                request_commit,
                predecessor_commit,
                live_main,
            )
        elif request["operation"] == OP_RECOVER:
            run_recovery(
                state,
                request,
                request_commit,
                predecessor_commit,
                live_main,
            )
        else:
            raise Stop("UNSUPPORTED_OPERATION")
        return 0
    except (
        Stop,
        RemoteImplementationError,
        FileNotFoundError,
        ValueError,
    ) as exc:
        DIAG.mkdir(parents=True, exist_ok=True)
        (DIAG / "stop.txt").write_text(
            str(exc) + "\n",
            encoding="utf-8",
        )
        print("STOP: %s" % exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
