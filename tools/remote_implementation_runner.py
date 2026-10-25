#!/usr/bin/env python3
"""Request processor for the guarded remote Implementation control plane."""
from __future__ import annotations

import json
import os
import shutil
import sys
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
    OP_STAGE2_CENSUS,
    OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
    OP_STAGE2_PROPOSAL_REHEARSAL,
    OP_STAGE2_GATE1_FILL,
    OP_STAGE2_PRESEAL_REHEARSAL,
    OP_STAGE2_GATE1_SEAL,
    OP_STAGE2_SEALED_APPLY,
    OP_RELEASE_READINESS,
    OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
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
    assert_protected_main_unchanged,
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
from remote_implementation_stage2_census import (
    STAGE2_ARTIFACT_NAMES,
    add_existing_onboarding_worktree,
    run_stage2_census_tool,
    verify_phase0_authority,
)
from remote_implementation_stage2_proposal import (
    PROPOSAL_ARTIFACT_NAMES,
    run_stage2_proposal_tool,
    verify_stage2_proposal_authority,
)
from remote_implementation_stage2_gate1_fill import (
    run_stage2_gate1_fill_tool,
    verify_stage2_gate1_fill_authority,
)
from remote_implementation_stage2_preseal import (
    run_stage2_preseal_rehearsal_tool,
    verify_stage2_preseal_authority,
)
from remote_implementation_stage2_seal import (
    run_stage2_gate1_seal_tool,
    verify_stage2_gate1_seal_authority,
)
from remote_implementation_stage2_apply import (
    replay_current_main_preseal,
    run_sealed_apply_tool,
    verify_prepared_sealed_apply,
    verify_stage2_sealed_apply_authority,
)
from remote_implementation_release_readiness import (
    verify_release_readiness_authority,
    run_permanent_release_readiness,
)
from remote_implementation_stage2_diagnostic import (
    run_stage2_reconciliation_diagnostic_tool,
    verify_stage2_diagnostic_authority,
)
from remote_implementation_stage2_opponent_display import (
    apply_and_prepare_repair,
    post_repair_stage2_result,
    run_normalizer_dry_run,
    stage2_result_summary,
    verify_census_and_freeze_authority,
    verify_prepared_commit_field_boundary,
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
    assert_protected_main_unchanged(live_main)
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


def persist_stage2_census_checkpoint(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    live_main: str,
    worktree: Path,
    result: dict[str, Any],
    phase0_authority: dict[str, Any],
    expected_remote: str,
) -> str:
    rid = request["request_id"]
    school = request["school_key"]
    directory = Path(
        ".remote-implementation/checkpoints/%s/%s" % (school, rid)
    )
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "request.json").write_bytes(request_bytes)

    artifact_hashes: dict[str, str] = {}
    normalized_hashes: dict[str, str] = {}
    source_dir = worktree / ".onboarding" / school
    for name in STAGE2_ARTIFACT_NAMES:
        source = source_dir / name
        if not source.is_file():
            continue
        target = directory / name
        shutil.copyfile(source, target)
        artifact_hashes[name] = sha256_file(target)
        normalized_hashes[name] = result["artifact_normalized_sha256"][name]
        if artifact_hashes[name] != result["artifact_sha256"][name]:
            raise Stop("STAGE2_CHECKPOINT_ARTIFACT_COPY_HASH_MISMATCH:%s" % name)

    status = result["status"]
    census = result.get("capability_census") or {}
    preflight = dict(status.get("preflight") or {})
    capability_status = str(census.get("status") or "")
    capability_hash = artifact_hashes.get(
        "implementation-stage2-capability-census.json"
    )
    manifest = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_CENSUS_CHECKPOINT",
        "request_id": rid,
        "school_key": school,
        "protected_main_sha": live_main,
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "target_tree_sha": result["tracked_mutation_proof"]["after_tree_sha"],
        "phase0_successor_path": request["phase0_successor"]["path"],
        "phase0_successor_sha256": request["phase0_successor"]["sha256"],
        "phase0_protected_main_sha": phase0_authority[
            "phase0_protected_main_sha"
        ],
        "integration_freeze_sha256": request[
            "integration_freeze_sha256"
        ],
        "semantic_snapshot_sha256": request[
            "semantic_snapshot_sha256"
        ],
        "permanent_command": result["command"],
        "command_exit_code": result["exit_code"],
        "stage2_status": result["stage2_status"],
        "preflight": preflight,
        "decision_universe_sha256": preflight.get(
            "decision_universe_sha256"
        ),
        "capability_census_status": capability_status,
        "capability_census_sha256": capability_hash,
        "capability_preflight": census.get("preflight", {}),
        "capability_topology_groups": census.get(
            "topology_groups", []
        ),
        "artifact_sha256": artifact_hashes,
        "artifact_normalized_sha256": normalized_hashes,
        "tracked_mutation_proof": result[
            "tracked_mutation_proof"
        ],
        "authority_statement": (
            "Read-only remote Implementation Stage 2 discovery checkpoint. "
            "No tracked repair, recommendation map, Gate 1 rehearsal, owner "
            "approval, sealed apply, Preview, or release authority is included."
        ),
    }
    manifest_path = directory / "checkpoint-manifest.json"
    write_json(manifest_path, manifest)
    manifest_sha = sha256_file(manifest_path)

    final_state = finalize_success(
        state,
        request_id=rid,
        last_operation={
            "operation": OP_STAGE2_CENSUS,
            "request_id": rid,
            "school_key": school,
            "protected_main_sha": live_main,
            "target_branch": request["target_branch"],
            "target_sha": request["target_sha"],
            "checkpoint_manifest_path": manifest_path.as_posix(),
            "checkpoint_manifest_sha256": manifest_sha,
            "stage2_status": result["stage2_status"],
            "decision_universe_sha256": preflight.get(
                "decision_universe_sha256"
            ),
            "capability_census_sha256": capability_hash,
            "fresh_runner_verification": "PENDING",
            "remote_stage2_census_equivalence": "PENDING",
        },
    )
    write_json(STATE_PATH, final_state)
    return commit_control(
        expected_remote,
        "finalize Stage 2 census checkpoint %s" % rid,
        [STATE_PATH, directory],
    )


def run_read_only_stage2_census(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    phase0_authority = verify_phase0_authority(
        request,
        predecessor_commit,
    )
    actual_target = remote_head(ROOT, request["target_branch"])
    if actual_target != request["target_sha"]:
        raise Stop(
            "STAGE2_ONBOARDING_HEAD_MISMATCH expected=%s actual=%s"
            % (request["target_sha"], actual_target or "[missing]")
        )

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
        "accept read-only Stage 2 census request %s"
        % request["request_id"],
        [STATE_PATH, archive],
    )

    worktree = add_existing_onboarding_worktree(
        request["target_branch"],
        request["target_sha"],
        request["school_key"],
    )
    result = run_stage2_census_tool(
        worktree,
        request["school_key"],
        phase0_authority["freeze_bytes"],
        DIAG,
    )
    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, request["target_branch"]) != request["target_sha"]:
        raise Stop("STAGE2_ONBOARDING_HEAD_CHANGED_DURING_RUN")

    checkpoint_commit = persist_stage2_census_checkpoint(
        state=active,
        request=request,
        request_bytes=request_bytes,
        live_main=live_main,
        worktree=worktree,
        result=result,
        phase0_authority=phase0_authority,
        expected_remote=accepted_commit,
    )
    print(
        "REMOTE STAGE 2 CENSUS: %s checkpoint_commit=%s"
        % (result["stage2_status"], checkpoint_commit)
    )




def _copy_stage2_proposal_artifacts(
    *,
    worktree: Path,
    school: str,
    result: dict[str, Any],
    directory: Path,
) -> tuple[dict[str, str], dict[str, str]]:
    artifact_hashes: dict[str, str] = {}
    normalized_hashes: dict[str, str] = {}
    source_dir = worktree / ".onboarding" / school
    for name in PROPOSAL_ARTIFACT_NAMES:
        source = source_dir / name
        if not source.is_file():
            continue
        target = directory / name
        shutil.copyfile(source, target)
        artifact_hashes[name] = sha256_file(target)
        normalized_hashes[name] = result["artifact_normalized_sha256"][name]
        if artifact_hashes[name] != result["artifact_sha256"][name]:
            raise Stop(
                "STAGE2_PROPOSAL_ARTIFACT_COPY_HASH_MISMATCH:%s" % name
            )
    return artifact_hashes, normalized_hashes


def persist_stage2_proposal_checkpoint(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    live_main: str,
    worktree: Path,
    map_path: Path,
    result: dict[str, Any],
    authority: dict[str, Any],
    expected_remote: str,
) -> str:
    rid = request["request_id"]
    school = request["school_key"]
    directory = Path(
        ".remote-implementation/checkpoints/%s/%s" % (school, rid)
    )
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "request.json").write_bytes(request_bytes)
    map_target = directory / "recommendation-map.json"
    shutil.copyfile(map_path, map_target)
    if sha256_file(map_target) != request["recommendation_map"]["sha256"]:
        raise Stop("STAGE2_PROPOSAL_CHECKPOINT_MAP_HASH_MISMATCH")

    artifact_hashes, normalized_hashes = _copy_stage2_proposal_artifacts(
        worktree=worktree,
        school=school,
        result=result,
        directory=directory,
    )
    status = result["status"]
    census = result.get("capability_census") or {}
    preflight = dict(status.get("preflight") or {})
    recommendation = dict(status.get("recommendation_map") or {})
    rehearsal = dict(status.get("proposal_rehearsal") or {})
    site = result.get("site_diagnostic") or {}
    approved_plan_hash = (
        rehearsal.get("approved_plan_hash_preview")
        or recommendation.get("approved_plan_hash_preview")
    )
    manifest = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_CHECKPOINT",
        "request_id": rid,
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": school,
        "protected_main_sha": live_main,
        "runtime_commit_sha": live_main,
        "runtime_tool_sha256": result["runtime_tool_sha256"],
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "target_tree_sha": result["tracked_mutation_proof"]["after_tree_sha"],
        "stage2_authority_path": request["stage2_authority"]["path"],
        "stage2_authority_sha256": request["stage2_authority"]["sha256"],
        "stage2_authority_kind": authority["authority_kind"],
        "integration_freeze_sha256": request["integration_freeze_sha256"],
        "semantic_snapshot_sha256": request["semantic_snapshot_sha256"],
        "decision_universe_sha256": request["decision_universe_sha256"],
        "runtime_decision_universe_sha256": (
            result.get("decision_universe_compatibility") or {}
        ).get("runtime_decision_universe_sha256"),
        "decision_universe_compatibility": result.get(
            "decision_universe_compatibility"
        ) or {},
        "recommendation_map_request_path": request["recommendation_map"]["path"],
        "recommendation_map_checkpoint_path": map_target.as_posix(),
        "recommendation_map_sha256": request["recommendation_map"]["sha256"],
        "permanent_command": result["command"],
        "command_exit_code": result["exit_code"],
        "stage2_status": result["stage2_status"],
        "preflight": preflight,
        "recommendation_map": recommendation,
        "proposal_rehearsal": rehearsal,
        "approved_plan_hash_preview": approved_plan_hash,
        "action_counts": rehearsal.get("action_counts", {}),
        "changed_path_count": rehearsal.get("changed_path_count"),
        "site_diagnostic": site,
        "capability_census_status": census.get("status"),
        "capability_topology_groups": census.get("topology_groups", []),
        "artifact_sha256": artifact_hashes,
        "artifact_normalized_sha256": normalized_hashes,
        "tracked_mutation_proof": result["tracked_mutation_proof"],
        "authority_statement": (
            "Read-only remote Stage 2 proposal rehearsal checkpoint. "
            "OWNER_GATE_1_READY means only that this exact recommendation map "
            "survived the permanent disposable rehearsal. No Owner Gate 1 "
            "approval, fill/seal/apply, Preview, merge, or release authority "
            "is included."
        ),
    }
    manifest_path = directory / "checkpoint-manifest.json"
    write_json(manifest_path, manifest)
    manifest_sha = sha256_file(manifest_path)

    final_state = finalize_success(
        state,
        request_id=rid,
        last_operation={
            "operation": OP_STAGE2_PROPOSAL_REHEARSAL,
            "request_id": rid,
            "school_key": school,
            "protected_main_sha": live_main,
            "target_branch": request["target_branch"],
            "target_sha": request["target_sha"],
            "checkpoint_manifest_path": manifest_path.as_posix(),
            "checkpoint_manifest_sha256": manifest_sha,
            "stage2_status": result["stage2_status"],
            "decision_universe_sha256": request["decision_universe_sha256"],
            "runtime_decision_universe_sha256": (
                result.get("decision_universe_compatibility") or {}
            ).get("runtime_decision_universe_sha256"),
            "decision_universe_compatibility": result.get(
                "decision_universe_compatibility"
            ) or {},
            "recommendation_map_sha256": request["recommendation_map"]["sha256"],
            "approved_plan_hash_preview": approved_plan_hash,
            "capability_census_status": census.get("status"),
            "fresh_runner_verification": "PENDING",
            "remote_stage2_proposal_equivalence": "PENDING",
        },
    )
    write_json(STATE_PATH, final_state)
    return commit_control(
        expected_remote,
        "finalize Stage 2 proposal rehearsal %s" % rid,
        [STATE_PATH, directory],
    )


def run_read_only_stage2_proposal(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    authority = verify_stage2_proposal_authority(
        request,
        predecessor_commit,
    )
    actual_target = remote_head(ROOT, request["target_branch"])
    if actual_target != request["target_sha"]:
        raise Stop(
            "STAGE2_PROPOSAL_TARGET_HEAD_MISMATCH expected=%s actual=%s"
            % (request["target_sha"], actual_target or "[missing]")
        )

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
        "accept read-only Stage 2 proposal rehearsal request %s"
        % request["request_id"],
        [STATE_PATH, archive],
    )

    scratch = Path(tempfile.mkdtemp(prefix="remote-stage2-proposal-map-"))
    map_path = materialize_payload(
        request_commit,
        request["recommendation_map"],
        scratch / "recommendation-map.json",
    )
    if map_path is None:
        raise Stop("STAGE2_PROPOSAL_MAP_MISSING")

    worktree = add_existing_onboarding_worktree(
        request["target_branch"],
        request["target_sha"],
        request["school_key"],
    )
    target_tree = git("rev-parse", "HEAD^{tree}", cwd=worktree).stdout.strip()
    if authority.get("target_tree_sha") and target_tree != authority["target_tree_sha"]:
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_TREE_MISMATCH")

    result = run_stage2_proposal_tool(
        worktree,
        request["school_key"],
        authority["freeze_bytes"],
        map_path,
        request["decision_universe_sha256"],
        DIAG / "stage2-proposal",
    )
    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, request["target_branch"]) != request["target_sha"]:
        raise Stop("STAGE2_PROPOSAL_TARGET_CHANGED_DURING_RUN")

    checkpoint_commit = persist_stage2_proposal_checkpoint(
        state=active,
        request=request,
        request_bytes=request_bytes,
        live_main=live_main,
        worktree=worktree,
        map_path=map_path,
        result=result,
        authority=authority,
        expected_remote=accepted_commit,
    )
    print(
        "REMOTE STAGE 2 PROPOSAL REHEARSAL: %s checkpoint_commit=%s"
        % (result["stage2_status"], checkpoint_commit)
    )



def persist_stage2_gate1_fill_checkpoint(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    live_main: str,
    result: dict[str, Any],
    authority: dict[str, Any],
    expected_remote: str,
) -> str:
    rid = request["request_id"]
    school = request["school_key"]
    directory = Path(
        ".remote-implementation/checkpoints/%s/%s" % (school, rid)
    )
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "request.json").write_bytes(request_bytes)

    source_review = directory / "source-review.csv"
    source_review.write_bytes(authority["review_bytes"])
    filled_review = directory / "filled-review.csv"
    filled_review.write_bytes(result["filled_review_bytes"])
    plan_target = directory / "plan.json"
    plan_target.write_bytes(authority["plan_bytes"])
    map_target = directory / "recommendation-map.json"
    map_target.write_bytes(authority["map_bytes"])

    if sha256_file(filled_review) != result["filled_review_sha256"]:
        raise Stop("STAGE2_GATE1_FILL_CHECKPOINT_REVIEW_HASH_MISMATCH")
    if sha256_file(map_target) != request["recommendation_map_sha256"]:
        raise Stop("STAGE2_GATE1_FILL_CHECKPOINT_MAP_HASH_MISMATCH")
    if sha256_file(plan_target) != result["plan_sha256"]:
        raise Stop("STAGE2_GATE1_FILL_CHECKPOINT_PLAN_HASH_MISMATCH")

    proposal = authority["proposal_manifest"]
    manifest = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_CHECKPOINT",
        "request_id": rid,
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": school,
        "protected_main_sha": live_main,
        "runtime_commit_sha": live_main,
        "runtime_tool_sha256": result["runtime_tool_sha256"],
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "target_tree_sha": result["tracked_mutation_proof"]["after_tree_sha"],
        "stage2_proposal_checkpoint_path": request["stage2_proposal_checkpoint"]["path"],
        "stage2_proposal_checkpoint_sha256": request["stage2_proposal_checkpoint"]["sha256"],
        "stage2_proposal_verification_path": request["stage2_proposal_verification"]["path"],
        "stage2_proposal_verification_sha256": request["stage2_proposal_verification"]["sha256"],
        "source_proposal_request_id": proposal.get("request_id"),
        "integration_freeze_sha256": request["integration_freeze_sha256"],
        "semantic_snapshot_sha256": request["semantic_snapshot_sha256"],
        "decision_universe_sha256": request["decision_universe_sha256"],
        "recommendation_map_sha256": request["recommendation_map_sha256"],
        "approved_plan_hash_preview": request["approved_plan_hash_preview"],
        "owner_gate_1_approval_sha256": authority["owner_gate_1_approval_sha256"],
        "owner_gate_1_approval": request["owner_gate_1_approval"],
        "permanent_command": result["command"],
        "command_exit_code": result["exit_code"],
        "gate1_fill_status": "FILLED",
        "source_review_sha256": result["source_review_sha256"],
        "filled_review_checkpoint_path": filled_review.as_posix(),
        "filled_review_sha256": result["filled_review_sha256"],
        "plan_checkpoint_path": plan_target.as_posix(),
        "plan_sha256": result["plan_sha256"],
        "recommendation_map_checkpoint_path": map_target.as_posix(),
        "decision_count": result["decision_count"],
        "action_counts": result["action_counts"],
        "decision_id_set_sha256": result["decision_id_set_sha256"],
        "tracked_mutation_proof": result["tracked_mutation_proof"],
        "authority_statement": (
            "Owner Gate 1 fill checkpoint only. The exact explicit owner approval "
            "is hash-bound to the exact OWNER_GATE_1_READY proposal, decision "
            "universe, recommendation map, and approved-plan preview. The permanent "
            "fill-review command populated only ignored review state; no tracked "
            "basketball mutation, pre-seal rehearsal, cryptographic seal, apply, "
            "Preview, merge, or release authority is included."
        ),
    }
    manifest_path = directory / "checkpoint-manifest.json"
    write_json(manifest_path, manifest)
    manifest_sha = sha256_file(manifest_path)

    final_state = finalize_success(
        state,
        request_id=rid,
        last_operation={
            "operation": OP_STAGE2_GATE1_FILL,
            "request_id": rid,
            "school_key": school,
            "protected_main_sha": live_main,
            "target_branch": request["target_branch"],
            "target_sha": request["target_sha"],
            "checkpoint_manifest_path": manifest_path.as_posix(),
            "checkpoint_manifest_sha256": manifest_sha,
            "source_proposal_request_id": proposal.get("request_id"),
            "decision_universe_sha256": request["decision_universe_sha256"],
            "recommendation_map_sha256": request["recommendation_map_sha256"],
            "approved_plan_hash_preview": request["approved_plan_hash_preview"],
            "owner_gate_1_approval_sha256": authority["owner_gate_1_approval_sha256"],
            "filled_review_sha256": result["filled_review_sha256"],
            "decision_id_set_sha256": result["decision_id_set_sha256"],
            "gate1_fill_status": "FILLED",
            "fresh_runner_verification": "PENDING",
            "remote_stage2_gate1_fill_equivalence": "PENDING",
        },
    )
    write_json(STATE_PATH, final_state)
    return commit_control(
        expected_remote,
        "finalize Stage 2 Gate 1 fill %s" % rid,
        [STATE_PATH, directory],
    )


def run_read_only_stage2_gate1_fill(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    authority = verify_stage2_gate1_fill_authority(
        request,
        predecessor_commit,
    )
    actual_target = remote_head(ROOT, request["target_branch"])
    if actual_target != request["target_sha"]:
        raise Stop(
            "STAGE2_GATE1_FILL_TARGET_HEAD_MISMATCH expected=%s actual=%s"
            % (request["target_sha"], actual_target or "[missing]")
        )

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
        "accept read-only Stage 2 Gate 1 fill request %s" % request["request_id"],
        [STATE_PATH, archive],
    )

    worktree = add_existing_onboarding_worktree(
        request["target_branch"],
        request["target_sha"],
        request["school_key"],
    )
    target_tree = git("rev-parse", "HEAD^{tree}", cwd=worktree).stdout.strip()
    if authority.get("target_tree_sha") and target_tree != authority["target_tree_sha"]:
        raise Stop("STAGE2_GATE1_FILL_AUTHORITY_TREE_MISMATCH")

    result = run_stage2_gate1_fill_tool(
        worktree,
        request["school_key"],
        freeze_bytes=authority["freeze_bytes"],
        map_bytes=authority["map_bytes"],
        plan_bytes=authority["plan_bytes"],
        review_bytes=authority["review_bytes"],
        expected_action_counts=authority["expected_action_counts"],
        expected_decision_count=authority["expected_decision_count"],
        diag=DIAG / "stage2-gate1-fill",
    )
    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, request["target_branch"]) != request["target_sha"]:
        raise Stop("STAGE2_GATE1_FILL_TARGET_CHANGED_DURING_RUN")

    checkpoint_commit = persist_stage2_gate1_fill_checkpoint(
        state=active,
        request=request,
        request_bytes=request_bytes,
        live_main=live_main,
        result=result,
        authority=authority,
        expected_remote=accepted_commit,
    )
    print(
        "REMOTE STAGE 2 GATE 1 FILL: PASS checkpoint_commit=%s"
        % checkpoint_commit
    )


def persist_stage2_preseal_checkpoint(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    live_main: str,
    result: dict[str, Any],
    authority: dict[str, Any],
    expected_remote: str,
) -> str:
    rid = request["request_id"]
    school = request["school_key"]
    directory = Path(
        ".remote-implementation/checkpoints/%s/%s" % (school, rid)
    )
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "request.json").write_bytes(request_bytes)

    log_source = DIAG / "stage2-preseal" / "stage2-preseal-rehearsal.log"
    log_target = directory / "rehearsal.log"
    if log_source.is_file():
        shutil.copyfile(log_source, log_target)

    site_target = None
    site_gate = result.get("site_gate")
    if site_gate is not None:
        site_target = directory / "site-gate.json"
        write_json(site_target, site_gate)

    manifest = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
        "request_id": rid,
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": school,
        "protected_main_sha": live_main,
        "runtime_commit_sha": live_main,
        "runtime_tool_sha256": result["runtime_tool_sha256"],
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "target_tree_sha": result["tracked_mutation_proof"]["after_tree_sha"],
        "stage2_gate1_fill_checkpoint_path": request[
            "stage2_gate1_fill_checkpoint"
        ]["path"],
        "stage2_gate1_fill_checkpoint_sha256": request[
            "stage2_gate1_fill_checkpoint"
        ]["sha256"],
        "stage2_gate1_fill_verification_path": request[
            "stage2_gate1_fill_verification"
        ]["path"],
        "stage2_gate1_fill_verification_sha256": request[
            "stage2_gate1_fill_verification"
        ]["sha256"],
        "source_gate1_fill_request_id": authority["gate1_fill_manifest"].get(
            "request_id"
        ),
        "owner_gate_1_approval_sha256": authority[
            "owner_gate_1_approval_sha256"
        ],
        "integration_freeze_sha256": request["integration_freeze_sha256"],
        "semantic_snapshot_sha256": request["semantic_snapshot_sha256"],
        "decision_universe_sha256": request["decision_universe_sha256"],
        "recommendation_map_sha256": request["recommendation_map_sha256"],
        "approved_plan_hash_preview": request["approved_plan_hash_preview"],
        "filled_review_sha256": request["filled_review_sha256"],
        "decision_id_set_sha256": request["decision_id_set_sha256"],
        "permanent_command": result["command"],
        "command_exit_code": result["exit_code"],
        "preseal_status": result["preseal_status"],
        "rehearsal_approved_plan_hash_preview": result[
            "approved_plan_hash_preview"
        ],
        "changed_path_count": result["changed_path_count"],
        "raw_log_sha256": result["raw_log_sha256"],
        "normalized_log_sha256": result["normalized_log_sha256"],
        "equivalence_sha256": result["equivalence_sha256"],
        "rehearsal_log_checkpoint_path": (
            log_target.as_posix() if log_target.is_file() else None
        ),
        "site_gate_checkpoint_path": (
            site_target.as_posix() if site_target is not None else None
        ),
        "site_gate_normalized_sha256": result[
            "site_gate_normalized_sha256"
        ],
        "tracked_mutation_proof": result["tracked_mutation_proof"],
        "authority_statement": (
            "Read-only pre-seal technical rehearsal checkpoint. It authenticates "
            "the exact fresh-verified Owner Gate 1 filled review and invokes the "
            "permanent disposable rehearse-review gate suite. READY_TO_SEAL means "
            "technical rehearsal passed only. Raw/normalized rehearsal-log hashes "
            "are diagnostic evidence; fresh equivalence is bound to the stable "
            "structured equivalence hash. No cryptographic seal, sealed apply, "
            "tracked onboarding mutation, Preview, Owner Gate 2, merge, or release "
            "authority is included."
        ),
    }
    manifest_path = directory / "checkpoint-manifest.json"
    write_json(manifest_path, manifest)
    manifest_sha = sha256_file(manifest_path)

    final_state = finalize_success(
        state,
        request_id=rid,
        last_operation={
            "operation": OP_STAGE2_PRESEAL_REHEARSAL,
            "request_id": rid,
            "school_key": school,
            "protected_main_sha": live_main,
            "target_branch": request["target_branch"],
            "target_sha": request["target_sha"],
            "checkpoint_manifest_path": manifest_path.as_posix(),
            "checkpoint_manifest_sha256": manifest_sha,
            "source_gate1_fill_request_id": authority[
                "gate1_fill_manifest"
            ].get("request_id"),
            "owner_gate_1_approval_sha256": authority[
                "owner_gate_1_approval_sha256"
            ],
            "decision_universe_sha256": request[
                "decision_universe_sha256"
            ],
            "recommendation_map_sha256": request[
                "recommendation_map_sha256"
            ],
            "approved_plan_hash_preview": request[
                "approved_plan_hash_preview"
            ],
            "filled_review_sha256": request["filled_review_sha256"],
            "decision_id_set_sha256": request[
                "decision_id_set_sha256"
            ],
            "preseal_status": result["preseal_status"],
            "changed_path_count": result["changed_path_count"],
            "raw_log_sha256": result["raw_log_sha256"],
            "normalized_log_sha256": result["normalized_log_sha256"],
            "equivalence_sha256": result["equivalence_sha256"],
            "site_gate_normalized_sha256": result[
                "site_gate_normalized_sha256"
            ],
            "fresh_runner_verification": "PENDING",
            "remote_stage2_preseal_equivalence": "PENDING",
        },
    )
    write_json(STATE_PATH, final_state)
    return commit_control(
        expected_remote,
        "finalize Stage 2 pre-seal rehearsal %s" % rid,
        [STATE_PATH, directory],
    )


def run_read_only_stage2_preseal_rehearsal(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    authority = verify_stage2_preseal_authority(
        request,
        predecessor_commit,
    )
    actual_target = remote_head(ROOT, request["target_branch"])
    if actual_target != request["target_sha"]:
        raise Stop(
            "STAGE2_PRESEAL_TARGET_HEAD_MISMATCH expected=%s actual=%s"
            % (request["target_sha"], actual_target or "[missing]")
        )

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
        "accept read-only Stage 2 pre-seal rehearsal request %s"
        % request["request_id"],
        [STATE_PATH, archive],
    )

    worktree = add_existing_onboarding_worktree(
        request["target_branch"],
        request["target_sha"],
        request["school_key"],
    )
    target_tree = git("rev-parse", "HEAD^{tree}", cwd=worktree).stdout.strip()
    if authority.get("target_tree_sha") and target_tree != authority[
        "target_tree_sha"
    ]:
        raise Stop("STAGE2_PRESEAL_AUTHORITY_TREE_MISMATCH")

    result = run_stage2_preseal_rehearsal_tool(
        worktree,
        request["school_key"],
        freeze_bytes=authority["freeze_bytes"],
        plan_bytes=authority["plan_bytes"],
        filled_review_bytes=authority["filled_review_bytes"],
        expected_approved_plan_hash_preview=request[
            "approved_plan_hash_preview"
        ],
        diag=DIAG / "stage2-preseal",
    )
    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, request["target_branch"]) != request["target_sha"]:
        raise Stop("STAGE2_PRESEAL_TARGET_CHANGED_DURING_RUN")

    checkpoint_commit = persist_stage2_preseal_checkpoint(
        state=active,
        request=request,
        request_bytes=request_bytes,
        live_main=live_main,
        result=result,
        authority=authority,
        expected_remote=accepted_commit,
    )
    print(
        "REMOTE STAGE 2 PRE-SEAL REHEARSAL: %s checkpoint_commit=%s"
        % (result["preseal_status"], checkpoint_commit)
    )


def persist_stage2_gate1_seal_checkpoint(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    live_main: str,
    current_preseal: dict[str, Any],
    seal_result: dict[str, Any],
    authority: dict[str, Any],
    expected_remote: str,
) -> str:
    rid = request["request_id"]
    school = request["school_key"]
    directory = Path(
        ".remote-implementation/checkpoints/%s/%s" % (school, rid)
    )
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "request.json").write_bytes(request_bytes)

    approved_plan_target = directory / "approved-plan.json"
    approved_plan_target.write_bytes(seal_result["approved_plan_bytes"])
    approved_review_target = directory / "approved-review.md"
    approved_review_target.write_bytes(seal_result["approved_review_bytes"])

    if sha256_file(approved_plan_target) != seal_result["approved_plan_sha256"]:
        raise Stop("STAGE2_GATE1_SEAL_CHECKPOINT_PLAN_HASH_MISMATCH")
    if sha256_file(approved_review_target) != seal_result["approved_review_sha256"]:
        raise Stop("STAGE2_GATE1_SEAL_CHECKPOINT_REVIEW_HASH_MISMATCH")

    source = authority["preseal_manifest"]
    manifest = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_CHECKPOINT",
        "request_id": rid,
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": school,
        "protected_main_sha": live_main,
        "runtime_commit_sha": live_main,
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "target_tree_sha": seal_result["tracked_mutation_proof"]["after_tree_sha"],
        "source_preseal_request_id": source.get("request_id"),
        "stage2_preseal_checkpoint_path": request[
            "stage2_preseal_checkpoint"
        ]["path"],
        "stage2_preseal_checkpoint_sha256": request[
            "stage2_preseal_checkpoint"
        ]["sha256"],
        "stage2_preseal_verification_path": request[
            "stage2_preseal_verification"
        ]["path"],
        "stage2_preseal_verification_sha256": request[
            "stage2_preseal_verification"
        ]["sha256"],
        "owner_gate_1_approval_sha256": request[
            "owner_gate_1_approval_sha256"
        ],
        "integration_freeze_sha256": request["integration_freeze_sha256"],
        "semantic_snapshot_sha256": request["semantic_snapshot_sha256"],
        "decision_universe_sha256": request["decision_universe_sha256"],
        "recommendation_map_sha256": request["recommendation_map_sha256"],
        "approved_plan_hash_preview": request["approved_plan_hash_preview"],
        "filled_review_sha256": request["filled_review_sha256"],
        "decision_id_set_sha256": request["decision_id_set_sha256"],
        "source_preseal_equivalence_sha256": request["equivalence_sha256"],
        "current_main_preseal_status": current_preseal["preseal_status"],
        "current_main_preseal_approved_plan_hash_preview": current_preseal[
            "approved_plan_hash_preview"
        ],
        "current_main_preseal_changed_path_count": current_preseal[
            "changed_path_count"
        ],
        "current_main_preseal_site_gate_normalized_sha256": current_preseal[
            "site_gate_normalized_sha256"
        ],
        "current_main_preseal_equivalence_sha256": current_preseal[
            "equivalence_sha256"
        ],
        "current_main_preseal_runtime_tool_sha256": current_preseal[
            "runtime_tool_sha256"
        ],
        "seal_runtime_tool_sha256": seal_result["runtime_tool_sha256"],
        "seal_command": seal_result["command"],
        "seal_command_exit_code": seal_result["exit_code"],
        "seal_status": "SEALED",
        "approved_plan_hash": seal_result["approved_plan_hash"],
        "approved_plan_checkpoint_path": approved_plan_target.as_posix(),
        "approved_plan_sha256": seal_result["approved_plan_sha256"],
        "approved_review_checkpoint_path": approved_review_target.as_posix(),
        "approved_review_sha256": seal_result["approved_review_sha256"],
        "approved_by": seal_result["approved_by"],
        "approved_at": seal_result["approved_at"],
        "decision_count": seal_result["decision_count"],
        "tracked_mutation_proof": seal_result["tracked_mutation_proof"],
        "authority_statement": (
            "Cryptographic Owner Gate 1 seal checkpoint only. The exact prior "
            "fresh-verified READY_TO_SEAL authority was replayed against current "
            "protected-main runtime before the permanent --approve path emitted "
            "the exact approved-plan hash. No sealed apply, tracked basketball "
            "mutation, Preview, Owner Gate 2, merge, or release authority is included."
        ),
    }
    manifest_path = directory / "checkpoint-manifest.json"
    write_json(manifest_path, manifest)
    manifest_sha = sha256_file(manifest_path)

    final_state = finalize_success(
        state,
        request_id=rid,
        last_operation={
            "operation": OP_STAGE2_GATE1_SEAL,
            "request_id": rid,
            "school_key": school,
            "protected_main_sha": live_main,
            "target_branch": request["target_branch"],
            "target_sha": request["target_sha"],
            "checkpoint_manifest_path": manifest_path.as_posix(),
            "checkpoint_manifest_sha256": manifest_sha,
            "source_preseal_request_id": source.get("request_id"),
            "owner_gate_1_approval_sha256": request[
                "owner_gate_1_approval_sha256"
            ],
            "decision_universe_sha256": request[
                "decision_universe_sha256"
            ],
            "recommendation_map_sha256": request[
                "recommendation_map_sha256"
            ],
            "approved_plan_hash_preview": request[
                "approved_plan_hash_preview"
            ],
            "filled_review_sha256": request["filled_review_sha256"],
            "decision_id_set_sha256": request["decision_id_set_sha256"],
            "source_preseal_equivalence_sha256": request[
                "equivalence_sha256"
            ],
            "current_main_preseal_equivalence_sha256": current_preseal[
                "equivalence_sha256"
            ],
            "approved_plan_hash": seal_result["approved_plan_hash"],
            "approved_plan_sha256": seal_result["approved_plan_sha256"],
            "approved_by": seal_result["approved_by"],
            "approved_at": seal_result["approved_at"],
            "seal_status": "SEALED",
            "fresh_runner_verification": "PENDING",
            "remote_stage2_gate1_seal_equivalence": "PENDING",
        },
    )
    write_json(STATE_PATH, final_state)
    return commit_control(
        expected_remote,
        "finalize Stage 2 Gate 1 seal %s" % rid,
        [STATE_PATH, directory],
    )


def run_read_only_stage2_gate1_seal(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    authority = verify_stage2_gate1_seal_authority(
        request,
        predecessor_commit,
    )
    actual_target = remote_head(ROOT, request["target_branch"])
    if actual_target != request["target_sha"]:
        raise Stop(
            "STAGE2_GATE1_SEAL_TARGET_HEAD_MISMATCH expected=%s actual=%s"
            % (request["target_sha"], actual_target or "[missing]")
        )

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
        "accept read-only Stage 2 Gate 1 seal request %s"
        % request["request_id"],
        [STATE_PATH, archive],
    )

    worktree = add_existing_onboarding_worktree(
        request["target_branch"],
        request["target_sha"],
        request["school_key"],
    )
    target_tree = git("rev-parse", "HEAD^{tree}", cwd=worktree).stdout.strip()
    if authority.get("target_tree_sha") and target_tree != authority[
        "target_tree_sha"
    ]:
        raise Stop("STAGE2_GATE1_SEAL_AUTHORITY_TREE_MISMATCH")

    # Re-run the full permanent pre-seal gate suite on current protected-main
    # runtime so a tooling-only main advance never requires a separate owner
    # relay merely to refresh technical readiness.
    current_preseal = run_stage2_preseal_rehearsal_tool(
        worktree,
        request["school_key"],
        freeze_bytes=authority["freeze_bytes"],
        plan_bytes=authority["plan_bytes"],
        filled_review_bytes=authority["filled_review_bytes"],
        expected_approved_plan_hash_preview=request[
            "approved_plan_hash_preview"
        ],
        diag=DIAG / "stage2-gate1-seal-preseal",
    )
    if current_preseal["preseal_status"] != "READY_TO_SEAL":
        raise Stop("STAGE2_GATE1_SEAL_CURRENT_MAIN_PRESEAL_NOT_READY")
    if (
        current_preseal["approved_plan_hash_preview"]
        != request["approved_plan_hash_preview"]
    ):
        raise Stop("STAGE2_GATE1_SEAL_CURRENT_MAIN_PREVIEW_MISMATCH")
    if (
        current_preseal["changed_path_count"]
        != authority["expected_changed_path_count"]
    ):
        raise Stop("STAGE2_GATE1_SEAL_CURRENT_MAIN_CHANGED_PATH_COUNT_MISMATCH")
    if (
        current_preseal["site_gate_normalized_sha256"]
        != authority["expected_site_gate_normalized_sha256"]
    ):
        raise Stop("STAGE2_GATE1_SEAL_CURRENT_MAIN_SITE_GATE_MISMATCH")
    if (
        current_preseal["tracked_mutation_proof"].get(
            "tracked_stage2_mutation"
        )
        != "NONE"
    ):
        raise Stop("STAGE2_GATE1_SEAL_CURRENT_MAIN_PRESEAL_MUTATION")

    seal_result = run_stage2_gate1_seal_tool(
        worktree,
        request["school_key"],
        freeze_bytes=authority["freeze_bytes"],
        plan_bytes=authority["plan_bytes"],
        filled_review_bytes=authority["filled_review_bytes"],
        diag=DIAG / "stage2-gate1-seal",
    )
    expected_decisions = authority.get("expected_decision_count")
    if (
        expected_decisions is not None
        and seal_result["decision_count"] != expected_decisions
    ):
        raise Stop("STAGE2_GATE1_SEAL_DECISION_COUNT_MISMATCH")

    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, request["target_branch"]) != request["target_sha"]:
        raise Stop("STAGE2_GATE1_SEAL_TARGET_CHANGED_DURING_RUN")

    checkpoint_commit = persist_stage2_gate1_seal_checkpoint(
        state=active,
        request=request,
        request_bytes=request_bytes,
        live_main=live_main,
        current_preseal=current_preseal,
        seal_result=seal_result,
        authority=authority,
        expected_remote=accepted_commit,
    )
    print(
        "REMOTE STAGE 2 GATE 1 SEAL: SEALED approved_plan=%s checkpoint_commit=%s"
        % (seal_result["approved_plan_hash"], checkpoint_commit)
    )


def persist_stage2_reconciliation_diagnostic_checkpoint(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    live_main: str,
    result: dict[str, Any],
    authority: dict[str, Any],
    expected_remote: str,
) -> str:
    rid = request["request_id"]
    school = request["school_key"]
    directory = Path(
        ".remote-implementation/checkpoints/%s/%s" % (school, rid)
    )
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "request.json").write_bytes(request_bytes)
    trace_target = directory / "reconciliation-trace.json"
    trace_target.write_bytes(result["trace_bytes"])
    if sha256_file(trace_target) != result["trace_sha256"]:
        raise Stop("STAGE2_DIAGNOSTIC_CHECKPOINT_TRACE_HASH_MISMATCH")

    trace = result["trace"]
    source_manifest = authority["proposal_manifest"]
    manifest = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_RECONCILIATION_DIAGNOSTIC_CHECKPOINT",
        "request_id": rid,
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": school,
        "protected_main_sha": live_main,
        "runtime_commit_sha": live_main,
        "runtime_tool_sha256": result["runtime_tool_sha256"],
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "target_tree_sha": result["tracked_mutation_proof"]["after_tree_sha"],
        "stage2_proposal_checkpoint_path": request["stage2_proposal_checkpoint"]["path"],
        "stage2_proposal_checkpoint_sha256": request["stage2_proposal_checkpoint"]["sha256"],
        "source_proposal_request_id": source_manifest.get("request_id"),
        "source_proposal_protected_main_sha": source_manifest.get("protected_main_sha"),
        "integration_freeze_sha256": request["integration_freeze_sha256"],
        "semantic_snapshot_sha256": request["semantic_snapshot_sha256"],
        "decision_universe_sha256": request["decision_universe_sha256"],
        "recommendation_map_sha256": request["recommendation_map_sha256"],
        "canonical_game_id": request["canonical_game_id"],
        "permanent_command": result["command"],
        "command_exit_code": result["exit_code"],
        "trace_checkpoint_path": trace_target.as_posix(),
        "trace_sha256": result["trace_sha256"],
        "diagnostic_status": trace.get("diagnostic_status"),
        "execution_status": trace.get("execution_status"),
        "execution_error": trace.get("execution_error"),
        "partial_location_classification": trace.get(
            "partial_location_classification"
        ),
        "integrity": trace.get("integrity") or {},
        "decision_count": len(trace.get("decision_order") or []),
        "mutation_count": len(trace.get("mutations") or []),
        "site_sync_count": len(trace.get("site_sync_events") or []),
        "tracked_mutation_proof": result["tracked_mutation_proof"],
        "authority_statement": (
            "Read-only Stage 2 reconciliation diagnostic. This checkpoint "
            "interprets no historical fact, supplies no Owner Gate approval, "
            "and authorizes no tracked school or protected-main mutation."
        ),
    }
    manifest_path = directory / "checkpoint-manifest.json"
    write_json(manifest_path, manifest)
    manifest_sha = sha256_file(manifest_path)

    final_state = finalize_success(
        state,
        request_id=rid,
        last_operation={
            "operation": OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
            "request_id": rid,
            "school_key": school,
            "protected_main_sha": live_main,
            "target_branch": request["target_branch"],
            "target_sha": request["target_sha"],
            "checkpoint_manifest_path": manifest_path.as_posix(),
            "checkpoint_manifest_sha256": manifest_sha,
            "source_proposal_request_id": source_manifest.get("request_id"),
            "canonical_game_id": request["canonical_game_id"],
            "trace_sha256": result["trace_sha256"],
            "partial_location_classification": trace.get(
                "partial_location_classification"
            ),
            "fresh_runner_verification": "PENDING",
            "remote_stage2_diagnostic_equivalence": "PENDING",
        },
    )
    write_json(STATE_PATH, final_state)
    return commit_control(
        expected_remote,
        "finalize Stage 2 reconciliation diagnostic %s" % rid,
        [STATE_PATH, directory],
    )


def run_read_only_stage2_reconciliation_diagnostic(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    authority = verify_stage2_diagnostic_authority(
        request,
        predecessor_commit,
    )
    actual_target = remote_head(ROOT, request["target_branch"])
    if actual_target != request["target_sha"]:
        raise Stop(
            "STAGE2_DIAGNOSTIC_TARGET_HEAD_MISMATCH expected=%s actual=%s"
            % (request["target_sha"], actual_target or "[missing]")
        )

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
        "accept read-only Stage 2 reconciliation diagnostic request %s"
        % request["request_id"],
        [STATE_PATH, archive],
    )

    worktree = add_existing_onboarding_worktree(
        request["target_branch"],
        request["target_sha"],
        request["school_key"],
    )
    target_tree = git("rev-parse", "HEAD^{tree}", cwd=worktree).stdout.strip()
    if authority.get("target_tree_sha") and target_tree != authority["target_tree_sha"]:
        raise Stop("STAGE2_DIAGNOSTIC_AUTHORITY_TREE_MISMATCH")

    result = run_stage2_reconciliation_diagnostic_tool(
        worktree,
        request["school_key"],
        freeze_bytes=authority["freeze_bytes"],
        map_bytes=authority["map_bytes"],
        plan_bytes=authority["plan_bytes"],
        review_bytes=authority["review_bytes"],
        canonical_game_id=request["canonical_game_id"],
        diag=DIAG / "stage2-reconciliation-diagnostic",
    )
    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, request["target_branch"]) != request["target_sha"]:
        raise Stop("STAGE2_DIAGNOSTIC_TARGET_CHANGED_DURING_RUN")

    checkpoint_commit = persist_stage2_reconciliation_diagnostic_checkpoint(
        state=active,
        request=request,
        request_bytes=request_bytes,
        live_main=live_main,
        result=result,
        authority=authority,
        expected_remote=accepted_commit,
    )
    print(
        "REMOTE STAGE 2 RECONCILIATION DIAGNOSTIC: PASS "
        "classification=%s checkpoint_commit=%s"
        % (
            result["trace"].get("partial_location_classification", ""),
            checkpoint_commit,
        )
    )


def _copy_stage2_result_artifacts(
    *,
    worktree: Path,
    school: str,
    result: dict[str, Any],
    directory: Path,
) -> tuple[dict[str, str], dict[str, str]]:
    artifact_hashes: dict[str, str] = {}
    normalized_hashes: dict[str, str] = {}
    source_dir = worktree / ".onboarding" / school
    for name in STAGE2_ARTIFACT_NAMES:
        source = source_dir / name
        if not source.is_file():
            continue
        target = directory / name
        shutil.copyfile(source, target)
        artifact_hashes[name] = sha256_file(target)
        normalized_hashes[name] = result["artifact_normalized_sha256"][name]
        if artifact_hashes[name] != result["artifact_sha256"][name]:
            raise Stop(
                "STAGE2_OPPONENT_DISPLAY_ARTIFACT_COPY_HASH_MISMATCH:%s"
                % name
            )
    return artifact_hashes, normalized_hashes


def finalize_stage2_opponent_display_successor(
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
    freeze_bytes: bytes,
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
        raise Stop("STAGE2_OPPONENT_DISPLAY_TARGET_NOT_PREPARED_COMMIT")

    stage2_worktree = add_existing_onboarding_worktree(
        target_branch,
        prepared,
        school,
    )
    result = post_repair_stage2_result(
        stage2_worktree,
        school,
        freeze_bytes,
        DIAG / "post-repair-stage2",
    )
    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, target_branch) != prepared:
        raise Stop("STAGE2_OPPONENT_DISPLAY_TARGET_CHANGED_DURING_REGENERATION")

    successor_dir = Path(
        ".remote-implementation/successors/%s/%s" % (school, rid)
    )
    successor_dir.mkdir(parents=True, exist_ok=True)
    artifact_hashes, normalized_hashes = _copy_stage2_result_artifacts(
        worktree=stage2_worktree,
        school=school,
        result=result,
        directory=successor_dir,
    )
    summary = stage2_result_summary(result)
    summary["artifact_sha256"] = artifact_hashes
    summary["artifact_normalized_sha256"] = normalized_hashes

    successor = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR",
        "operation": OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
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
        "actual_published_target_sha": prepared,
        "changed_paths": writeahead["changed_paths"],
        "changed_file_sha256": writeahead["changed_file_sha256"],
        "stage2_census_checkpoint_path": writeahead[
            "stage2_census_checkpoint_path"
        ],
        "stage2_census_checkpoint_sha256": writeahead[
            "stage2_census_checkpoint_sha256"
        ],
        "expected_blocker_keys": writeahead["expected_blocker_keys"],
        "normalization_report_sha256": writeahead[
            "normalization_report_sha256"
        ],
        "field_level_proof_sha256": writeahead[
            "field_level_proof_sha256"
        ],
        "source_game_normalized_name_row_count": writeahead[
            "source_game_normalized_name_row_count"
        ],
        "integration_freeze_sha256": writeahead[
            "integration_freeze_sha256"
        ],
        "semantic_snapshot_sha256": writeahead[
            "semantic_snapshot_sha256"
        ],
        "semantic_drift_before": writeahead["semantic_drift_before"],
        "semantic_drift_after": writeahead["semantic_drift_after"],
        "repository_validation": writeahead["repository_validation"],
        "publication_cas": publication_cas,
        "post_repair_stage2": summary,
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
            "operation": OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
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
            "stage2_status": result["stage2_status"],
            "decision_universe_sha256": (
                result.get("status", {}).get("preflight", {})
            ).get("decision_universe_sha256"),
            "capability_census_status": (
                result.get("capability_census") or {}
            ).get("status"),
            "fresh_runner_verification": "PENDING",
            "remote_stage2_opponent_display_equivalence": "PENDING",
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
        "finalize Stage 2 opponent-display normalization %s" % rid,
        paths,
    )


def run_stage2_opponent_display_normalize(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    authority = verify_census_and_freeze_authority(
        request,
        predecessor_commit,
    )
    target_branch = request["target_branch"]
    target_sha = request["target_sha"]
    actual_target = remote_head(ROOT, target_branch)
    if actual_target != target_sha:
        raise Stop(
            "STAGE2_OPPONENT_DISPLAY_TARGET_HEAD_MISMATCH expected=%s actual=%s"
            % (target_sha, actual_target or "[missing]")
        )

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

    worktree = add_existing_onboarding_worktree(
        target_branch,
        target_sha,
        request["school_key"],
    )
    dry_run = run_normalizer_dry_run(
        worktree,
        request["school_key"],
        authority["freeze_bytes"],
        authority["blocker_keys"],
        DIAG / "opponent-display",
    )
    prepared = apply_and_prepare_repair(
        worktree,
        request["school_key"],
        target_sha,
        authority["freeze_bytes"],
        dry_run,
        authority["blocker_keys"],
        DIAG / "opponent-display",
    )
    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, target_branch) != target_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_TARGET_CHANGED_BEFORE_WRITEAHEAD")

    validation = run(
        [sys.executable, "tools/validate_data.py"],
        cwd=worktree,
        check=False,
    )
    DIAG.mkdir(parents=True, exist_ok=True)
    (DIAG / "opponent-display-validate-data.log").write_text(
        validation.stdout,
        encoding="utf-8",
    )
    if validation.returncode != 0:
        raise Stop("STAGE2_OPPONENT_DISPLAY_REPOSITORY_VALIDATION_FAILED")

    writeahead_dir = Path(
        ".remote-implementation/writeahead/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    writeahead_dir.mkdir(parents=True, exist_ok=True)
    (writeahead_dir / "integration-freeze.json").write_bytes(
        authority["freeze_bytes"]
    )
    (writeahead_dir / "normalization-report.json").write_bytes(
        dry_run["report_bytes"]
    )
    write_json(
        writeahead_dir / "field-level-proof.json",
        prepared["field_level_proof"],
    )
    write_json(
        writeahead_dir / "semantic-drift-proof.json",
        {
            "before": dry_run["semantic_drift_before"],
            "after": prepared["semantic_drift_after"],
        },
    )
    (writeahead_dir / "census-checkpoint-manifest.json").write_bytes(
        authority["census_manifest_bytes"]
    )
    sidecars = {
        name: sha256_file(writeahead_dir / name)
        for name in (
            "integration-freeze.json",
            "normalization-report.json",
            "field-level-proof.json",
            "semantic-drift-proof.json",
            "census-checkpoint-manifest.json",
        )
    }
    writeahead = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
        "operation": OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
        "request_id": request["request_id"],
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": request["school_key"],
        "global_lock_commit": lock_commit,
        "protected_main_sha": live_main,
        "target_branch": target_branch,
        "expected_target_predecessor_sha": target_sha,
        "prepared_commit_sha": prepared["prepared_commit_sha"],
        "prepared_tree_sha": prepared["prepared_tree_sha"],
        "prepared_parent_sha": prepared["prepared_parent_sha"],
        "commit_message": prepared["commit_message"],
        "changed_paths": prepared["changed_paths"],
        "changed_file_sha256": prepared["changed_file_sha256"],
        "allowed_paths": sorted(
            {
                "schools/%s/opponents.csv" % request["school_key"],
                "schools/%s/source-games.csv" % request["school_key"],
            }
        ),
        "sidecars": sidecars,
        "stage2_census_checkpoint_path": request[
            "stage2_census_checkpoint"
        ]["path"],
        "stage2_census_checkpoint_sha256": request[
            "stage2_census_checkpoint"
        ]["sha256"],
        "expected_blocker_keys": authority["blocker_keys"],
        "normalization_report_sha256": sidecars[
            "normalization-report.json"
        ],
        "field_level_proof_sha256": sidecars["field-level-proof.json"],
        "source_game_normalized_name_row_count": prepared[
            "field_level_proof"
        ]["source_game_normalized_name_row_count"],
        "integration_freeze_sha256": request[
            "integration_freeze_sha256"
        ],
        "semantic_snapshot_sha256": request[
            "semantic_snapshot_sha256"
        ],
        "semantic_drift_before": dry_run["semantic_drift_before"],
        "semantic_drift_after": prepared["semantic_drift_after"],
        "repository_validation": "PASS",
        "mutation_state": "PREPARED_NOT_PUBLISHED",
    }
    writeahead_path = writeahead_dir / "writeahead-manifest.json"
    write_json(writeahead_path, writeahead)
    writeahead_sha = sha256_file(writeahead_path)

    active["transaction_state"] = "PREPARED_NOT_PUBLISHED"
    active["active_writeahead_path"] = writeahead_path.as_posix()
    active["active_writeahead_sha256"] = writeahead_sha
    active["active_prepared_commit_sha"] = prepared[
        "prepared_commit_sha"
    ]
    active["active_prepared_tree_sha"] = prepared["prepared_tree_sha"]
    write_json(STATE_PATH, active)
    writeahead_commit = commit_control(
        lock_bound_commit,
        "publish Stage 2 opponent-display write-ahead %s"
        % request["request_id"],
        [STATE_PATH, writeahead_dir],
    )
    active["active_writeahead_commit"] = writeahead_commit
    write_json(STATE_PATH, active)
    writeahead_bound_commit = commit_control(
        writeahead_commit,
        "bind Stage 2 opponent-display write-ahead %s"
        % request["request_id"],
        [STATE_PATH],
    )

    assert_protected_main_unchanged(live_main)
    publish_ref_cas(
        ROOT,
        branch=target_branch,
        prepared_commit=prepared["prepared_commit_sha"],
        expected_predecessor=target_sha,
    )
    if remote_head(ROOT, target_branch) != prepared["prepared_commit_sha"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_TARGET_PUBLICATION_VERIFY_FAILED")

    successor_commit = finalize_stage2_opponent_display_successor(
        active=active,
        original_request=request,
        request_sha256=sha256_bytes(request_bytes),
        live_main=live_main,
        writeahead=writeahead,
        writeahead_path=writeahead_path.as_posix(),
        writeahead_sha256=writeahead_sha,
        writeahead_commit=writeahead_commit,
        expected_remote=writeahead_bound_commit,
        freeze_bytes=authority["freeze_bytes"],
        publication_cas="EXISTING_REF_CAS_PASS",
    )
    print(
        "REMOTE STAGE 2 OPPONENT DISPLAY NORMALIZATION: COMPLETE "
        "target=%s successor_commit=%s"
        % (prepared["prepared_commit_sha"], successor_commit)
    )


def finalize_stage2_sealed_apply_successor(
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
        raise Stop("STAGE2_SEALED_APPLY_TARGET_NOT_PREPARED_COMMIT")

    proof = verify_prepared_sealed_apply(
        ROOT,
        predecessor_sha=writeahead["expected_target_predecessor_sha"],
        prepared_sha=prepared,
        changed_paths=writeahead["changed_paths"],
        changed_file_sha256=writeahead["changed_file_sha256"],
        deleted_paths=writeahead.get("deleted_paths") or [],
    )
    if proof["prepared_tree_sha"] != writeahead["prepared_tree_sha"]:
        raise Stop("STAGE2_SEALED_APPLY_FINAL_TREE_MISMATCH")

    successor_dir = Path(
        ".remote-implementation/successors/%s/%s" % (school, rid)
    )
    successor_dir.mkdir(parents=True, exist_ok=True)
    prefix = Path(writeahead_path).parent
    for name in (
        "release-manifest.json",
        "pr-body.md",
        "visual-qa.md",
        "approved-plan.json",
        "current-main-preseal.json",
    ):
        source_path = (prefix / name).as_posix()
        try:
            data = git_show_bytes(
                active.get("active_writeahead_commit") or writeahead_commit or expected_remote,
                source_path,
            )
        except Exception:
            data = None
        if data is not None:
            (successor_dir / name).write_bytes(data)

    successor = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_SEALED_APPLY_SUCCESSOR",
        "operation": OP_STAGE2_SEALED_APPLY,
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
        "actual_published_target_sha": prepared,
        "changed_paths": writeahead["changed_paths"],
        "changed_file_sha256": writeahead["changed_file_sha256"],
        "deleted_paths": writeahead.get("deleted_paths") or [],
        "approved_plan_hash": writeahead["approved_plan_hash"],
        "approved_plan_sha256": writeahead["approved_plan_sha256"],
        "stage2_gate1_seal_checkpoint_path": writeahead[
            "stage2_gate1_seal_checkpoint_path"
        ],
        "stage2_gate1_seal_checkpoint_sha256": writeahead[
            "stage2_gate1_seal_checkpoint_sha256"
        ],
        "stage2_gate1_seal_verification_path": writeahead[
            "stage2_gate1_seal_verification_path"
        ],
        "stage2_gate1_seal_verification_sha256": writeahead[
            "stage2_gate1_seal_verification_sha256"
        ],
        "integration_freeze_sha256": writeahead[
            "integration_freeze_sha256"
        ],
        "semantic_snapshot_sha256": writeahead[
            "semantic_snapshot_sha256"
        ],
        "decision_universe_sha256": writeahead[
            "decision_universe_sha256"
        ],
        "recommendation_map_sha256": writeahead[
            "recommendation_map_sha256"
        ],
        "filled_review_sha256": writeahead["filled_review_sha256"],
        "decision_id_set_sha256": writeahead["decision_id_set_sha256"],
        "owner_gate_1_approval_sha256": writeahead[
            "owner_gate_1_approval_sha256"
        ],
        "current_main_preseal": writeahead["current_main_preseal"],
        "apply_runtime_tool_sha256": writeahead[
            "apply_runtime_tool_sha256"
        ],
        "release_manifest_sha256": writeahead[
            "release_manifest_sha256"
        ],
        "release_manifest_changed_path_count": writeahead[
            "release_manifest_changed_path_count"
        ],
        "repository_validation": writeahead["repository_validation"],
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
            "operation": OP_STAGE2_SEALED_APPLY,
            "request_id": rid,
            "school_key": school,
            "protected_main_sha": live_main,
            "target_branch": target_branch,
            "target_predecessor_sha": writeahead[
                "expected_target_predecessor_sha"
            ],
            "target_sha": prepared,
            "approved_plan_hash": writeahead["approved_plan_hash"],
            "approved_plan_sha256": writeahead["approved_plan_sha256"],
            "writeahead_manifest_path": writeahead_path,
            "writeahead_manifest_sha256": writeahead_sha256,
            "successor_manifest_path": successor_path.as_posix(),
            "successor_manifest_sha256": successor_sha,
            "changed_path_count": len(writeahead["changed_paths"]),
            "release_manifest_sha256": writeahead[
                "release_manifest_sha256"
            ],
            "fresh_runner_verification": "PENDING",
            "remote_stage2_sealed_apply_equivalence": "PENDING",
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
        "finalize Stage 2 sealed apply %s" % rid,
        paths,
    )


def run_stage2_sealed_apply(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    authority = verify_stage2_sealed_apply_authority(
        request,
        predecessor_commit,
    )
    target_branch = request["target_branch"]
    target_sha = request["target_sha"]
    if remote_head(ROOT, target_branch) != target_sha:
        raise Stop("STAGE2_SEALED_APPLY_TARGET_HEAD_MISMATCH")

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

    worktree = add_existing_onboarding_worktree(
        target_branch,
        target_sha,
        request["school_key"],
    )
    if authority.get("target_tree_sha"):
        tree = git("rev-parse", "HEAD^{tree}", cwd=worktree).stdout.strip()
        if tree != authority["target_tree_sha"]:
            raise Stop("STAGE2_SEALED_APPLY_AUTHORITY_TREE_MISMATCH")

    current_preseal = replay_current_main_preseal(
        worktree,
        request["school_key"],
        authority=authority,
        diag=DIAG / "sealed-apply-preseal",
    )
    prepared = run_sealed_apply_tool(
        worktree,
        request["school_key"],
        target_sha,
        authority=authority,
        diag=DIAG / "sealed-apply",
        prepare_commit=True,
    )
    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, target_branch) != target_sha:
        raise Stop("STAGE2_SEALED_APPLY_TARGET_CHANGED_BEFORE_WRITEAHEAD")

    writeahead_dir = Path(
        ".remote-implementation/writeahead/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    writeahead_dir.mkdir(parents=True, exist_ok=True)
    (writeahead_dir / "integration-freeze.json").write_bytes(
        authority["freeze_bytes"]
    )
    (writeahead_dir / "approved-plan.json").write_bytes(
        authority["approved_plan_bytes"]
    )
    (writeahead_dir / "seal-checkpoint-manifest.json").write_bytes(
        authority["seal_checkpoint_bytes"]
    )
    (writeahead_dir / "seal-verification.json").write_bytes(
        authority["seal_verification_bytes"]
    )
    (writeahead_dir / "release-manifest.json").write_bytes(
        prepared["release_manifest_bytes"]
    )
    if prepared["pr_body_bytes"]:
        (writeahead_dir / "pr-body.md").write_bytes(
            prepared["pr_body_bytes"]
        )
    if prepared["visual_qa_bytes"]:
        (writeahead_dir / "visual-qa.md").write_bytes(
            prepared["visual_qa_bytes"]
        )
    write_json(
        writeahead_dir / "current-main-preseal.json",
        {
            "preseal_status": current_preseal["preseal_status"],
            "approved_plan_hash_preview": current_preseal[
                "approved_plan_hash_preview"
            ],
            "changed_path_count": current_preseal["changed_path_count"],
            "site_gate_normalized_sha256": current_preseal[
                "site_gate_normalized_sha256"
            ],
            "equivalence_sha256": current_preseal["equivalence_sha256"],
            "runtime_tool_sha256": current_preseal[
                "runtime_tool_sha256"
            ],
            "tracked_stage2_mutation": "NONE",
        },
    )
    sidecars = {
        path.name: sha256_file(path)
        for path in writeahead_dir.iterdir()
        if path.is_file()
    }

    writeahead = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
        "operation": OP_STAGE2_SEALED_APPLY,
        "request_id": request["request_id"],
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": request["school_key"],
        "global_lock_commit": lock_commit,
        "protected_main_sha": live_main,
        "target_branch": target_branch,
        "expected_target_predecessor_sha": target_sha,
        "prepared_commit_sha": prepared["prepared_commit_sha"],
        "prepared_tree_sha": prepared["prepared_tree_sha"],
        "prepared_parent_sha": prepared["prepared_parent_sha"],
        "commit_message": prepared["commit_message"],
        "changed_paths": prepared["changed_paths"],
        "changed_file_sha256": prepared["changed_file_sha256"],
        "deleted_paths": prepared.get("deleted_paths") or [],
        "sidecars": sidecars,
        "stage2_gate1_seal_checkpoint_path": request[
            "stage2_gate1_seal_checkpoint"
        ]["path"],
        "stage2_gate1_seal_checkpoint_sha256": request[
            "stage2_gate1_seal_checkpoint"
        ]["sha256"],
        "stage2_gate1_seal_verification_path": request[
            "stage2_gate1_seal_verification"
        ]["path"],
        "stage2_gate1_seal_verification_sha256": request[
            "stage2_gate1_seal_verification"
        ]["sha256"],
        "approved_plan_hash": request["approved_plan_hash"],
        "approved_plan_sha256": request["approved_plan_sha256"],
        "owner_gate_1_approval_sha256": request[
            "owner_gate_1_approval_sha256"
        ],
        "integration_freeze_sha256": request[
            "integration_freeze_sha256"
        ],
        "semantic_snapshot_sha256": request[
            "semantic_snapshot_sha256"
        ],
        "decision_universe_sha256": request[
            "decision_universe_sha256"
        ],
        "recommendation_map_sha256": request[
            "recommendation_map_sha256"
        ],
        "filled_review_sha256": request["filled_review_sha256"],
        "decision_id_set_sha256": request["decision_id_set_sha256"],
        "current_main_preseal": json.loads(
            (writeahead_dir / "current-main-preseal.json").read_text(
                encoding="utf-8"
            )
        ),
        "apply_runtime_tool_sha256": prepared[
            "runtime_tool_sha256"
        ],
        "release_manifest_sha256": prepared[
            "release_manifest_sha256"
        ],
        "release_manifest_changed_path_count": len(
            prepared["release_manifest"]["changed_paths"]
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
    active["active_prepared_commit_sha"] = prepared[
        "prepared_commit_sha"
    ]
    active["active_prepared_tree_sha"] = prepared["prepared_tree_sha"]
    write_json(STATE_PATH, active)
    writeahead_commit = commit_control(
        lock_bound_commit,
        "publish Stage 2 sealed apply write-ahead %s"
        % request["request_id"],
        [STATE_PATH, writeahead_dir],
    )
    active["active_writeahead_commit"] = writeahead_commit
    write_json(STATE_PATH, active)
    writeahead_bound_commit = commit_control(
        writeahead_commit,
        "bind Stage 2 sealed apply write-ahead %s"
        % request["request_id"],
        [STATE_PATH],
    )

    assert_protected_main_unchanged(live_main)
    publish_ref_cas(
        ROOT,
        branch=target_branch,
        prepared_commit=prepared["prepared_commit_sha"],
        expected_predecessor=target_sha,
    )
    if remote_head(ROOT, target_branch) != prepared["prepared_commit_sha"]:
        raise Stop("STAGE2_SEALED_APPLY_TARGET_PUBLICATION_VERIFY_FAILED")

    successor_commit = finalize_stage2_sealed_apply_successor(
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
        "REMOTE STAGE 2 SEALED APPLY: COMPLETE target=%s successor_commit=%s"
        % (prepared["prepared_commit_sha"], successor_commit)
    )


def run_read_only_release_readiness(
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    """Checkpoint final gates on a fresh-verified committed apply; create no PR."""
    authority = verify_release_readiness_authority(
        request, predecessor_commit, source_repo=ROOT
    )
    if remote_head(ROOT, request["target_branch"]) != request["target_sha"]:
        raise Stop("RELEASE_READINESS_TARGET_CHANGED_BEFORE_REQUEST")

    active = begin_request(
        state,
        request,
        sha256_bytes(request_bytes),
        run_id=os.environ.get("GITHUB_RUN_ID", "local"),
        run_attempt=os.environ.get("GITHUB_RUN_ATTEMPT", "1"),
        request_commit=request_commit,
    )
    write_json(STATE_PATH, active)
    archive = archive_request(request, request_bytes)
    accepted_commit = commit_control(
        request_commit,
        "accept read-only release readiness %s" % request["request_id"],
        [STATE_PATH, archive],
    )
    worktree = add_existing_onboarding_worktree(
        request["target_branch"], request["target_sha"], request["school_key"]
    )
    result = run_permanent_release_readiness(
        authority,
        worktree=worktree,
        artifact_dir=worktree / ".onboarding" / request["school_key"],
    )
    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, request["target_branch"]) != request["target_sha"]:
        raise Stop("RELEASE_READINESS_TARGET_MOVED_AFTER_GATES")
    directory = Path(
        ".remote-implementation/checkpoints/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "request.json").write_bytes(request_bytes)
    write_json(directory / "readiness-proof.json", result)
    manifest = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_RELEASE_READINESS_CHECKPOINT",
        "request_id": request["request_id"],
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": request["school_key"],
        "protected_main_sha": live_main,
        "target_branch": request["target_branch"],
        "target_sha": request["target_sha"],
        "readiness_status": "RELEASE_READINESS_PASS",
        "source_apply_request_id": result["apply_request_id"],
        "stage2_apply_successor_path": request["stage2_apply_successor"]["path"],
        "stage2_apply_successor_sha256": request["stage2_apply_successor"]["sha256"],
        "stage2_apply_verification_path": request["stage2_apply_verification"]["path"],
        "stage2_apply_verification_sha256": request["stage2_apply_verification"]["sha256"],
        "approved_plan_hash": result["approved_plan_hash"],
        "release_manifest_sha256": result["release_manifest_sha256"],
        "changed_path_count": result["changed_path_count"],
        "readiness_proof_sha256": sha256_file(directory / "readiness-proof.json"),
        "tracked_mutation": "NONE",
        "pr_created": False,
        "preview_verified": False,
        "owner_gate_2": False,
        "authority_statement": (
            "Read-only final release gate proof on one exact fresh-verified "
            "sealed-apply successor. This checkpoint supplies no PR creation, "
            "Preview, Owner Gate 2, merge, or Production authority."
        ),
    }
    manifest_path = directory / "checkpoint-manifest.json"
    write_json(manifest_path, manifest)
    final_state = finalize_success(
        active,
        request_id=request["request_id"],
        last_operation={
            "operation": OP_RELEASE_READINESS,
            "request_id": request["request_id"],
            "school_key": request["school_key"],
            "protected_main_sha": live_main,
            "target_branch": request["target_branch"],
            "target_sha": request["target_sha"],
            "checkpoint_manifest_path": manifest_path.as_posix(),
            "checkpoint_manifest_sha256": sha256_file(manifest_path),
            "readiness_status": "RELEASE_READINESS_PASS",
            "fresh_runner_verification": "PENDING",
            "remote_release_readiness_equivalence": "PENDING",
        },
    )
    write_json(STATE_PATH, final_state)
    commit = commit_control(
        accepted_commit,
        "checkpoint read-only release readiness %s" % request["request_id"],
        [STATE_PATH, directory],
    )
    print("REMOTE RELEASE READINESS: PASS checkpoint_commit=%s" % commit)


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

    assert_protected_main_unchanged(live_main)
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

    assert_protected_main_unchanged(live_main)
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

        if state.get("active_operation") == OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE:
            if manifest.get("operation") != OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE:
                raise Stop("RECOVERY_OPPONENT_DISPLAY_WRITEAHEAD_OPERATION_MISMATCH")
            prefix = Path(state["active_writeahead_path"]).parent
            freeze_bytes = git_show_bytes(
                predecessor_commit,
                (prefix / "integration-freeze.json").as_posix(),
            )
            if sha256_bytes(freeze_bytes) != manifest["integration_freeze_sha256"]:
                raise Stop("RECOVERY_OPPONENT_DISPLAY_FREEZE_HASH_MISMATCH")
            original_request_path = (
                ".remote-implementation/requests/%s/request.json"
                % original_request_id
            )
            original_request_bytes = git_show_bytes(
                predecessor_commit,
                original_request_path,
            )
            if sha256_bytes(original_request_bytes) != state["active_request_sha256"]:
                raise Stop("RECOVERY_OPPONENT_DISPLAY_REQUEST_HASH_MISMATCH")
            original_request = json.loads(original_request_bytes)
            proof = verify_prepared_commit_field_boundary(
                ROOT,
                school_key=request["school_key"],
                predecessor_sha=manifest["expected_target_predecessor_sha"],
                prepared_sha=prepared,
                expected_blocker_keys=manifest["expected_blocker_keys"],
            )
            stored_proof = json.loads(
                git_show_bytes(
                    predecessor_commit,
                    (prefix / "field-level-proof.json").as_posix(),
                )
            )
            if proof != stored_proof:
                raise Stop("RECOVERY_OPPONENT_DISPLAY_FIELD_PROOF_MISMATCH")
            commit = finalize_stage2_opponent_display_successor(
                active=state,
                original_request=original_request,
                request_sha256=state["active_request_sha256"],
                live_main=live_main,
                writeahead=manifest,
                writeahead_path=state["active_writeahead_path"],
                writeahead_sha256=state["active_writeahead_sha256"],
                writeahead_commit=state.get("active_writeahead_commit"),
                expected_remote=request_commit,
                freeze_bytes=freeze_bytes,
                publication_cas="RECOVERY_ADOPTION_EXACT_MATCH",
                extra_commit_paths=[directory],
                recovery_request_id=request["request_id"],
                recovery_classification=classification,
            )
            print(
                "REMOTE IMPLEMENTATION RECOVERY: %s commit=%s"
                % (classification, commit)
            )
            return

        if state.get("active_operation") == OP_STAGE2_SEALED_APPLY:
            if manifest.get("operation") != OP_STAGE2_SEALED_APPLY:
                raise Stop("RECOVERY_SEALED_APPLY_WRITEAHEAD_OPERATION_MISMATCH")
            original_request_path = (
                ".remote-implementation/requests/%s/request.json"
                % original_request_id
            )
            original_request_bytes = git_show_bytes(
                predecessor_commit,
                original_request_path,
            )
            if sha256_bytes(original_request_bytes) != state["active_request_sha256"]:
                raise Stop("RECOVERY_SEALED_APPLY_REQUEST_HASH_MISMATCH")
            original_request = json.loads(original_request_bytes)
            proof = verify_prepared_sealed_apply(
                ROOT,
                predecessor_sha=manifest["expected_target_predecessor_sha"],
                prepared_sha=prepared,
                changed_paths=manifest["changed_paths"],
                changed_file_sha256=manifest["changed_file_sha256"],
                deleted_paths=manifest.get("deleted_paths") or [],
            )
            if proof["prepared_tree_sha"] != manifest["prepared_tree_sha"]:
                raise Stop("RECOVERY_SEALED_APPLY_TREE_MISMATCH")
            commit = finalize_stage2_sealed_apply_successor(
                active=state,
                original_request=original_request,
                request_sha256=state["active_request_sha256"],
                live_main=live_main,
                writeahead=manifest,
                writeahead_path=state["active_writeahead_path"],
                writeahead_sha256=state["active_writeahead_sha256"],
                writeahead_commit=state.get("active_writeahead_commit"),
                expected_remote=request_commit,
                publication_cas="RECOVERY_ADOPTION_EXACT_MATCH",
                extra_commit_paths=[directory],
                recovery_request_id=request["request_id"],
                recovery_classification=classification,
            )
            print(
                "REMOTE IMPLEMENTATION RECOVERY: %s commit=%s"
                % (classification, commit)
            )
            return

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
        elif request["operation"] == OP_STAGE2_CENSUS:
            run_read_only_stage2_census(
                state,
                request,
                request_bytes,
                request_commit,
                predecessor_commit,
                live_main,
            )
        elif request["operation"] == OP_STAGE2_PROPOSAL_REHEARSAL:
            run_read_only_stage2_proposal(
                state,
                request,
                request_bytes,
                request_commit,
                predecessor_commit,
                live_main,
            )
        elif request["operation"] == OP_STAGE2_GATE1_FILL:
            run_read_only_stage2_gate1_fill(
                state,
                request,
                request_bytes,
                request_commit,
                predecessor_commit,
                live_main,
            )
        elif request["operation"] == OP_STAGE2_PRESEAL_REHEARSAL:
            run_read_only_stage2_preseal_rehearsal(
                state,
                request,
                request_bytes,
                request_commit,
                predecessor_commit,
                live_main,
            )
        elif request["operation"] == OP_STAGE2_GATE1_SEAL:
            run_read_only_stage2_gate1_seal(
                state,
                request,
                request_bytes,
                request_commit,
                predecessor_commit,
                live_main,
            )
        elif request["operation"] == OP_STAGE2_SEALED_APPLY:
            run_stage2_sealed_apply(
                state,
                request,
                request_bytes,
                request_commit,
                predecessor_commit,
                live_main,
            )
        elif request["operation"] == OP_RELEASE_READINESS:
            run_read_only_release_readiness(
                state, request, request_bytes, request_commit,
                predecessor_commit, live_main,
            )
        elif request["operation"] == OP_STAGE2_RECONCILIATION_DIAGNOSTIC:
            run_read_only_stage2_reconciliation_diagnostic(
                state,
                request,
                request_bytes,
                request_commit,
                predecessor_commit,
                live_main,
            )
        elif request["operation"] == OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE:
            run_stage2_opponent_display_normalize(
                state,
                request,
                request_bytes,
                request_commit,
                predecessor_commit,
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
