#!/usr/bin/env python3
"""Fresh-runner verification for a completed remote Phase 0 successor."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

from remote_implementation_control import (
    LIFECYCLE_IDLE,
    OP_PHASE0,
    OP_RECOVER,
    OP_STAGE2_CENSUS,
    OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
    OP_STAGE2_PROPOSAL_REHEARSAL,
    RemoteImplementationError,
    sha256_bytes,
    validate_control_state,
)
from remote_implementation_io import (
    REQUIRED_PACKAGE_FILES,
    ROOT,
    STATE_PATH,
    Stop,
    commit_control,
    configure_git,
    fetch_operational_refs,
    git,
    git_show_bytes,
    git_show_json,
    read_json,
    remote_head,
    run,
    write_json,
)
from remote_implementation_stage2_census import (
    STAGE2_ARTIFACT_NAMES,
    add_existing_onboarding_worktree,
    run_stage2_census_tool,
    verify_phase0_authority,
)
from remote_implementation_stage2_proposal import (
    run_stage2_proposal_tool,
    verify_stage2_proposal_authority,
)
from remote_implementation_stage2_opponent_display import (
    run_normalizer_dry_run,
    verify_census_and_freeze_authority,
    verify_prepared_commit_field_boundary,
)
from integration_freeze_guard import semantic_drift_report

DIAG = Path(
    os.environ.get(
        "REMOTE_IMPLEMENTATION_DIAG",
        "/tmp/remote-implementation-verification",
    )
)



def verify_stage2_proposal_rehearsal(
    live_main: str,
    control_head: str,
    state: dict,
) -> int:
    last = state.get("last_operation") or {}
    if last.get("fresh_runner_verification") == "PASS":
        print("REMOTE STAGE 2 PROPOSAL EQUIVALENCE: PASS (already verified)")
        return 0

    checkpoint_path = last["checkpoint_manifest_path"]
    checkpoint_bytes = git_show_bytes(control_head, checkpoint_path)
    if sha256_bytes(checkpoint_bytes) != last["checkpoint_manifest_sha256"]:
        raise Stop("STAGE2_PROPOSAL_FRESH_CHECKPOINT_HASH_MISMATCH")
    manifest = json.loads(checkpoint_bytes)
    if (
        manifest.get("kind")
        != "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_CHECKPOINT"
    ):
        raise Stop("STAGE2_PROPOSAL_FRESH_CHECKPOINT_KIND_MISMATCH")
    if manifest.get("protected_main_sha") != live_main:
        raise Stop("STAGE2_PROPOSAL_FRESH_MAIN_CHANGED")
    if manifest.get("target_sha") != last.get("target_sha"):
        raise Stop("STAGE2_PROPOSAL_FRESH_TARGET_BINDING_MISMATCH")
    if (
        manifest.get("decision_universe_sha256")
        != last.get("decision_universe_sha256")
    ):
        raise Stop("STAGE2_PROPOSAL_FRESH_DECISION_BINDING_MISMATCH")
    if (
        manifest.get("recommendation_map_sha256")
        != last.get("recommendation_map_sha256")
    ):
        raise Stop("STAGE2_PROPOSAL_FRESH_MAP_BINDING_MISMATCH")

    directory = Path(checkpoint_path).parent
    request_bytes = git_show_bytes(
        control_head,
        (directory / "request.json").as_posix(),
    )
    if sha256_bytes(request_bytes) != manifest.get("request_sha256"):
        raise Stop("STAGE2_PROPOSAL_FRESH_REQUEST_HASH_MISMATCH")
    request = json.loads(request_bytes)
    if request.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_PROPOSAL_FRESH_REQUEST_ID_MISMATCH")
    authority = verify_stage2_proposal_authority(request, control_head)

    map_bytes = git_show_bytes(
        control_head,
        manifest["recommendation_map_checkpoint_path"],
    )
    if sha256_bytes(map_bytes) != manifest["recommendation_map_sha256"]:
        raise Stop("STAGE2_PROPOSAL_FRESH_MAP_HASH_MISMATCH")
    map_dir = Path(tempfile.mkdtemp(prefix="remote-stage2-proposal-fresh-map-"))
    map_path = map_dir / "recommendation-map.json"
    map_path.write_bytes(map_bytes)

    target_branch = manifest["target_branch"]
    target_sha = remote_head(ROOT, target_branch)
    if target_sha != manifest["target_sha"]:
        raise Stop("STAGE2_PROPOSAL_FRESH_TARGET_REF_MISMATCH")
    worktree = add_existing_onboarding_worktree(
        target_branch,
        target_sha,
        manifest["school_key"],
    )
    tree = git("rev-parse", "HEAD^{tree}", cwd=worktree).stdout.strip()
    if tree != manifest["target_tree_sha"]:
        raise Stop("STAGE2_PROPOSAL_FRESH_TARGET_TREE_MISMATCH")
    if authority.get("target_tree_sha") and tree != authority["target_tree_sha"]:
        raise Stop("STAGE2_PROPOSAL_FRESH_AUTHORITY_TREE_MISMATCH")

    result = run_stage2_proposal_tool(
        worktree,
        manifest["school_key"],
        authority["freeze_bytes"],
        map_path,
        manifest["decision_universe_sha256"],
        DIAG / "stage2-proposal",
    )
    if result["runtime_tool_sha256"] != manifest["runtime_tool_sha256"]:
        raise Stop("STAGE2_PROPOSAL_FRESH_RUNTIME_TOOL_MISMATCH")
    if result["stage2_status"] != manifest["stage2_status"]:
        raise Stop("STAGE2_PROPOSAL_FRESH_STATUS_MISMATCH")
    runtime_decision_sha = result["status"].get("preflight", {}).get(
        "decision_universe_sha256"
    )
    if runtime_decision_sha != manifest.get("runtime_decision_universe_sha256"):
        raise Stop("STAGE2_PROPOSAL_FRESH_DECISION_UNIVERSE_MISMATCH")
    if (
        result.get("decision_universe_compatibility") or {}
    ) != (manifest.get("decision_universe_compatibility") or {}):
        raise Stop("STAGE2_PROPOSAL_FRESH_DECISION_COMPATIBILITY_MISMATCH")
    if (
        result["tracked_mutation_proof"].get("tracked_stage2_mutation")
        != "NONE"
    ):
        raise Stop("STAGE2_PROPOSAL_FRESH_TRACKED_MUTATION")

    status = result["status"]
    recommendation = status.get("recommendation_map") or {}
    rehearsal = status.get("proposal_rehearsal") or {}
    if manifest["stage2_status"] == "OWNER_GATE_1_READY":
        if recommendation.get("sha256") != manifest["recommendation_map_sha256"]:
            raise Stop("STAGE2_PROPOSAL_FRESH_PERMANENT_MAP_HASH_MISMATCH")
        if rehearsal != manifest.get("proposal_rehearsal", {}):
            raise Stop("STAGE2_PROPOSAL_FRESH_REHEARSAL_SUMMARY_MISMATCH")
        if (
            rehearsal.get("approved_plan_hash_preview")
            != manifest.get("approved_plan_hash_preview")
        ):
            raise Stop("STAGE2_PROPOSAL_FRESH_PLAN_HASH_MISMATCH")
    if (result.get("site_diagnostic") or {}) != (
        manifest.get("site_diagnostic") or {}
    ):
        raise Stop("STAGE2_PROPOSAL_FRESH_SITE_DIAGNOSTIC_MISMATCH")
    actual_census = result.get("capability_census") or {}
    if actual_census.get("status") != manifest.get("capability_census_status"):
        raise Stop("STAGE2_PROPOSAL_FRESH_CAPABILITY_STATUS_MISMATCH")
    if actual_census.get("topology_groups", []) != manifest.get(
        "capability_topology_groups", []
    ):
        raise Stop("STAGE2_PROPOSAL_FRESH_CAPABILITY_TOPOLOGY_MISMATCH")

    expected_raw = manifest.get("artifact_sha256") or {}
    expected_normalized = manifest.get("artifact_normalized_sha256") or {}
    actual_raw = result["artifact_sha256"]
    actual_normalized = result["artifact_normalized_sha256"]
    if set(expected_raw) != set(actual_raw):
        raise Stop("STAGE2_PROPOSAL_FRESH_ARTIFACT_SET_MISMATCH")
    normalized_equivalence: list[str] = []
    for name in sorted(expected_raw):
        if expected_raw[name] == actual_raw.get(name):
            continue
        if expected_normalized.get(name) != actual_normalized.get(name):
            raise Stop(
                "STAGE2_PROPOSAL_FRESH_ARTIFACT_HASH_MISMATCH:%s" % name
            )
        normalized_equivalence.append(name)

    verification = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_VERIFICATION",
        "request_id": manifest["request_id"],
        "school_key": manifest["school_key"],
        "protected_main_sha": live_main,
        "target_branch": target_branch,
        "target_sha": target_sha,
        "target_tree_sha": tree,
        "integration_freeze_sha256": manifest["integration_freeze_sha256"],
        "semantic_snapshot_sha256": manifest["semantic_snapshot_sha256"],
        "decision_universe_sha256": manifest["decision_universe_sha256"],
        "runtime_decision_universe_sha256": manifest.get(
            "runtime_decision_universe_sha256"
        ),
        "decision_universe_compatibility": manifest.get(
            "decision_universe_compatibility"
        ) or {},
        "recommendation_map_sha256": manifest["recommendation_map_sha256"],
        "stage2_status": result["stage2_status"],
        "approved_plan_hash_preview": manifest.get("approved_plan_hash_preview"),
        "capability_census_status": actual_census.get("status"),
        "artifact_sha256": actual_raw,
        "artifact_normalized_sha256": actual_normalized,
        "normalized_equivalence_artifacts": normalized_equivalence,
        "tracked_stage2_mutation": "NONE",
        "remote_stage2_proposal_equivalence": "PASS",
    }
    verify_dir = Path(
        ".remote-implementation/verifications/%s/%s"
        % (manifest["school_key"], manifest["request_id"])
    )
    write_json(
        verify_dir / "stage2-proposal-rehearsal-verification.json",
        verification,
    )

    local_state = read_json(STATE_PATH)
    validate_control_state(local_state)
    local_last = local_state.get("last_operation") or {}
    if (
        local_last.get("operation") != OP_STAGE2_PROPOSAL_REHEARSAL
        or local_last.get("request_id") != manifest["request_id"]
    ):
        raise Stop("STAGE2_PROPOSAL_FRESH_CONTROL_MOVED")
    local_last["fresh_runner_verification"] = "PASS"
    local_last["remote_stage2_proposal_equivalence"] = "PASS"
    local_state["last_operation"] = local_last
    write_json(STATE_PATH, local_state)
    commit = commit_control(
        control_head,
        "persist fresh Stage 2 proposal rehearsal verification %s"
        % manifest["request_id"],
        [STATE_PATH, verify_dir],
    )
    print(
        "REMOTE STAGE 2 PROPOSAL EQUIVALENCE: PASS verification_commit=%s"
        % commit
    )
    return 0


def verify_stage2_census(
    live_main: str,
    control_head: str,
    state: dict,
) -> int:
    last = state.get("last_operation") or {}
    if last.get("fresh_runner_verification") == "PASS":
        print("REMOTE STAGE 2 CENSUS EQUIVALENCE: PASS (already verified)")
        return 0

    checkpoint_path = last["checkpoint_manifest_path"]
    checkpoint_bytes = git_show_bytes(control_head, checkpoint_path)
    if sha256_bytes(checkpoint_bytes) != last["checkpoint_manifest_sha256"]:
        raise Stop("STAGE2_FRESH_CHECKPOINT_HASH_MISMATCH")
    manifest = json.loads(checkpoint_bytes)
    if manifest.get("kind") != "REMOTE_IMPLEMENTATION_STAGE2_CENSUS_CHECKPOINT":
        raise Stop("STAGE2_FRESH_CHECKPOINT_KIND_MISMATCH")
    if manifest.get("protected_main_sha") != live_main:
        raise Stop("STAGE2_FRESH_MAIN_CHANGED")
    if manifest.get("target_sha") != last.get("target_sha"):
        raise Stop("STAGE2_FRESH_TARGET_BINDING_MISMATCH")

    directory = Path(checkpoint_path).parent
    request_bytes = git_show_bytes(
        control_head,
        (directory / "request.json").as_posix(),
    )
    request = json.loads(request_bytes)
    if request.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_FRESH_REQUEST_ID_MISMATCH")
    if request.get("target_sha") != manifest.get("target_sha"):
        raise Stop("STAGE2_FRESH_REQUEST_TARGET_MISMATCH")

    phase0 = verify_phase0_authority(request, control_head)
    target_branch = manifest["target_branch"]
    target_sha = remote_head(ROOT, target_branch)
    if target_sha != manifest["target_sha"]:
        raise Stop("STAGE2_FRESH_TARGET_REF_MISMATCH")

    worktree = add_existing_onboarding_worktree(
        target_branch,
        target_sha,
        manifest["school_key"],
    )
    result = run_stage2_census_tool(
        worktree,
        manifest["school_key"],
        phase0["freeze_bytes"],
        DIAG,
    )
    if result["stage2_status"] != manifest["stage2_status"]:
        raise Stop("STAGE2_FRESH_STATUS_MISMATCH")
    if (
        result["status"].get("preflight", {}).get("decision_universe_sha256")
        != manifest.get("decision_universe_sha256")
    ):
        raise Stop("STAGE2_FRESH_DECISION_UNIVERSE_MISMATCH")

    expected_raw = manifest.get("artifact_sha256") or {}
    expected_normalized = manifest.get("artifact_normalized_sha256") or {}
    actual_raw = result["artifact_sha256"]
    actual_normalized = result["artifact_normalized_sha256"]
    if set(actual_raw) != set(expected_raw):
        raise Stop("STAGE2_FRESH_ARTIFACT_SET_MISMATCH")
    normalized_equivalence: list[str] = []
    for name in sorted(expected_raw):
        if actual_raw.get(name) == expected_raw[name]:
            continue
        if actual_normalized.get(name) != expected_normalized.get(name):
            raise Stop("STAGE2_FRESH_ARTIFACT_HASH_MISMATCH:%s" % name)
        normalized_equivalence.append(name)

    census = result.get("capability_census") or {}
    if str(census.get("status") or "") != str(
        manifest.get("capability_census_status") or ""
    ):
        raise Stop("STAGE2_FRESH_CAPABILITY_STATUS_MISMATCH")
    if result["tracked_mutation_proof"].get("tracked_stage2_mutation") != "NONE":
        raise Stop("STAGE2_FRESH_TRACKED_MUTATION")

    verification = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_CENSUS_VERIFICATION",
        "request_id": manifest["request_id"],
        "school_key": manifest["school_key"],
        "protected_main_sha": live_main,
        "target_branch": target_branch,
        "target_sha": target_sha,
        "target_tree_sha": result["tracked_mutation_proof"]["after_tree_sha"],
        "integration_freeze_sha256": manifest[
            "integration_freeze_sha256"
        ],
        "semantic_snapshot_sha256": manifest[
            "semantic_snapshot_sha256"
        ],
        "stage2_status": result["stage2_status"],
        "decision_universe_sha256": manifest.get(
            "decision_universe_sha256"
        ),
        "capability_census_status": manifest.get(
            "capability_census_status"
        ),
        "artifact_sha256": actual_raw,
        "artifact_normalized_sha256": actual_normalized,
        "normalized_path_equivalence_artifacts": normalized_equivalence,
        "tracked_stage2_mutation": "NONE",
        "remote_stage2_census_equivalence": "PASS",
    }
    verify_dir = Path(
        ".remote-implementation/verifications/%s/%s"
        % (manifest["school_key"], manifest["request_id"])
    )
    write_json(
        verify_dir / "stage2-census-verification.json",
        verification,
    )

    local_state = read_json(STATE_PATH)
    validate_control_state(local_state)
    local_last = local_state.get("last_operation") or {}
    if (
        local_last.get("operation") != OP_STAGE2_CENSUS
        or local_last.get("request_id") != manifest["request_id"]
    ):
        raise Stop("STAGE2_FRESH_CONTROL_MOVED")
    local_last["fresh_runner_verification"] = "PASS"
    local_last["remote_stage2_census_equivalence"] = "PASS"
    local_state["last_operation"] = local_last
    write_json(STATE_PATH, local_state)
    commit = commit_control(
        control_head,
        "persist fresh Stage 2 census verification %s"
        % manifest["request_id"],
        [STATE_PATH, verify_dir],
    )
    print(
        "REMOTE STAGE 2 CENSUS EQUIVALENCE: PASS verification_commit=%s"
        % commit
    )
    return 0



def verify_stage2_opponent_display_normalization(
    live_main: str,
    control_head: str,
    state: dict,
) -> int:
    last = state.get("last_operation") or {}
    if last.get("fresh_runner_verification") == "PASS":
        print(
            "REMOTE STAGE 2 OPPONENT DISPLAY EQUIVALENCE: PASS "
            "(already verified)"
        )
        return 0

    successor_path = last["successor_manifest_path"]
    successor_bytes = git_show_bytes(control_head, successor_path)
    if sha256_bytes(successor_bytes) != last["successor_manifest_sha256"]:
        raise Stop("OPPONENT_DISPLAY_FRESH_SUCCESSOR_HASH_MISMATCH")
    successor = json.loads(successor_bytes)
    if (
        successor.get("kind")
        != "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR"
    ):
        raise Stop("OPPONENT_DISPLAY_FRESH_SUCCESSOR_KIND_MISMATCH")
    if successor.get("protected_main_sha") != live_main:
        raise Stop("OPPONENT_DISPLAY_FRESH_MAIN_CHANGED")
    if successor.get("operation") != OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE:
        raise Stop("OPPONENT_DISPLAY_FRESH_OPERATION_MISMATCH")

    target_branch = successor["target_branch"]
    prepared = successor["prepared_commit_sha"]
    predecessor = successor["expected_target_predecessor_sha"]

    request_path = (
        ".remote-implementation/requests/%s/request.json"
        % successor["request_id"]
    )
    request_bytes = git_show_bytes(control_head, request_path)
    if sha256_bytes(request_bytes) != successor["request_sha256"]:
        raise Stop("OPPONENT_DISPLAY_FRESH_REQUEST_HASH_MISMATCH")
    request = json.loads(request_bytes)
    authority = verify_census_and_freeze_authority(
        request,
        control_head,
    )
    if authority["blocker_keys"] != successor["expected_blocker_keys"]:
        raise Stop("OPPONENT_DISPLAY_FRESH_CENSUS_KEY_MISMATCH")
    if (
        request["stage2_census_checkpoint"]["path"]
        != successor["stage2_census_checkpoint_path"]
        or request["stage2_census_checkpoint"]["sha256"]
        != successor["stage2_census_checkpoint_sha256"]
    ):
        raise Stop("OPPONENT_DISPLAY_FRESH_CENSUS_BINDING_MISMATCH")

    if remote_head(ROOT, target_branch) != prepared:
        raise Stop("OPPONENT_DISPLAY_FRESH_TARGET_REF_MISMATCH")
    git(
        "fetch",
        "--no-tags",
        "origin",
        "+refs/heads/%s:refs/remotes/origin/remote-opponent-display-target"
        % target_branch,
    )

    writeahead_path = successor["writeahead_manifest_path"]
    writeahead_bytes = git_show_bytes(control_head, writeahead_path)
    if (
        sha256_bytes(writeahead_bytes)
        != successor["writeahead_manifest_sha256"]
    ):
        raise Stop("OPPONENT_DISPLAY_FRESH_WRITEAHEAD_HASH_MISMATCH")
    manifest = json.loads(writeahead_bytes)
    if manifest.get("operation") != OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE:
        raise Stop("OPPONENT_DISPLAY_FRESH_WRITEAHEAD_OPERATION_MISMATCH")
    if manifest.get("expected_target_predecessor_sha") != predecessor:
        raise Stop("OPPONENT_DISPLAY_FRESH_PREDECESSOR_MISMATCH")
    if manifest.get("prepared_commit_sha") != prepared:
        raise Stop("OPPONENT_DISPLAY_FRESH_PREPARED_MISMATCH")

    prefix = Path(writeahead_path).parent
    bundle = Path(tempfile.mkdtemp(prefix="remote-opponent-display-fresh-"))
    for relative, expected in (manifest.get("sidecars") or {}).items():
        data = git_show_bytes(
            control_head,
            (prefix / relative).as_posix(),
        )
        target = bundle / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        if sha256_bytes(data) != expected:
            raise Stop(
                "OPPONENT_DISPLAY_FRESH_SIDECAR_HASH_MISMATCH:%s"
                % relative
            )

    parent = git("rev-parse", "%s^" % prepared).stdout.strip()
    tree = git("rev-parse", "%s^{tree}" % prepared).stdout.strip()
    if parent != manifest["prepared_parent_sha"] or parent != predecessor:
        raise Stop("OPPONENT_DISPLAY_FRESH_PARENT_MISMATCH")
    if tree != manifest["prepared_tree_sha"]:
        raise Stop("OPPONENT_DISPLAY_FRESH_TREE_MISMATCH")
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
        raise Stop("OPPONENT_DISPLAY_FRESH_CHANGED_PATH_MISMATCH")
    for path, expected in manifest["changed_file_sha256"].items():
        if sha256_bytes(git_show_bytes(prepared, path)) != expected:
            raise Stop(
                "OPPONENT_DISPLAY_FRESH_CHANGED_FILE_HASH_MISMATCH:%s"
                % path
            )

    field_proof = verify_prepared_commit_field_boundary(
        ROOT,
        school_key=successor["school_key"],
        predecessor_sha=predecessor,
        prepared_sha=prepared,
        expected_blocker_keys=manifest["expected_blocker_keys"],
    )
    stored_field_proof = json.loads(
        (bundle / "field-level-proof.json").read_bytes()
    )
    if field_proof != stored_field_proof:
        raise Stop("OPPONENT_DISPLAY_FRESH_FIELD_PROOF_MISMATCH")

    predecessor_tree = Path(
        tempfile.mkdtemp(prefix="remote-opponent-display-predecessor-")
    )
    shutil.rmtree(predecessor_tree)
    git(
        "worktree",
        "add",
        "-b",
        "remote-opponent-display-verify/%s"
        % predecessor[:12],
        str(predecessor_tree),
        predecessor,
    )
    configure_git(predecessor_tree)
    freeze_bytes = (bundle / "integration-freeze.json").read_bytes()
    if sha256_bytes(freeze_bytes) != manifest["integration_freeze_sha256"]:
        raise Stop("OPPONENT_DISPLAY_FRESH_FREEZE_HASH_MISMATCH")
    if freeze_bytes != authority["freeze_bytes"]:
        raise Stop("OPPONENT_DISPLAY_FRESH_FREEZE_AUTHORITY_MISMATCH")
    dry = run_normalizer_dry_run(
        predecessor_tree,
        successor["school_key"],
        freeze_bytes,
        manifest["expected_blocker_keys"],
        DIAG / "opponent-display-dry-run",
    )
    if dry["report_sha256"] != manifest["normalization_report_sha256"]:
        raise Stop("OPPONENT_DISPLAY_FRESH_NORMALIZATION_REPORT_MISMATCH")

    prepared_tree = add_existing_onboarding_worktree(
        target_branch,
        prepared,
        successor["school_key"],
    )
    freeze_path = (
        prepared_tree
        / ".onboarding"
        / successor["school_key"]
        / "integration-freeze.json"
    )
    freeze_path.parent.mkdir(parents=True, exist_ok=True)
    freeze_path.write_bytes(freeze_bytes)
    drift = semantic_drift_report(
        prepared_tree,
        successor["school_key"],
    )
    if drift.get("status") != "PASS" or drift.get("changes"):
        raise Stop("OPPONENT_DISPLAY_FRESH_SEMANTIC_DRIFT")

    result = run_stage2_census_tool(
        prepared_tree,
        successor["school_key"],
        freeze_bytes,
        DIAG / "opponent-display-stage2",
    )
    expected_stage2 = successor.get("post_repair_stage2") or {}
    actual_preflight = result.get("status", {}).get("preflight", {})
    actual_census = result.get("capability_census") or {}
    comparisons = {
        "stage2_status": result.get("stage2_status"),
        "blocker_count": int(actual_preflight.get("blocker_count", 0) or 0),
        "warning_count": int(actual_preflight.get("warning_count", 0) or 0),
        "decision_count": int(actual_preflight.get("decision_count", 0) or 0),
        "decision_universe_sha256": actual_preflight.get(
            "decision_universe_sha256"
        ),
        "capability_census_status": actual_census.get("status"),
    }
    for key, actual in comparisons.items():
        if actual != expected_stage2.get(key):
            raise Stop(
                "OPPONENT_DISPLAY_FRESH_STAGE2_MISMATCH:%s" % key
            )
    if (
        result["tracked_mutation_proof"].get("tracked_stage2_mutation")
        != "NONE"
    ):
        raise Stop("OPPONENT_DISPLAY_FRESH_STAGE2_TRACKED_MUTATION")

    expected_raw = expected_stage2.get("artifact_sha256") or {}
    expected_normalized = (
        expected_stage2.get("artifact_normalized_sha256") or {}
    )
    actual_raw = result["artifact_sha256"]
    actual_normalized = result["artifact_normalized_sha256"]
    if set(expected_raw) != set(actual_raw):
        raise Stop("OPPONENT_DISPLAY_FRESH_ARTIFACT_SET_MISMATCH")
    normalized_equivalence: list[str] = []
    for name in sorted(expected_raw):
        if expected_raw[name] == actual_raw.get(name):
            continue
        if expected_normalized.get(name) != actual_normalized.get(name):
            raise Stop(
                "OPPONENT_DISPLAY_FRESH_ARTIFACT_HASH_MISMATCH:%s"
                % name
            )
        normalized_equivalence.append(name)

    verification = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_VERIFICATION",
        "request_id": successor["request_id"],
        "school_key": successor["school_key"],
        "protected_main_sha": live_main,
        "target_branch": target_branch,
        "target_predecessor_sha": predecessor,
        "target_sha": prepared,
        "target_tree_sha": tree,
        "changed_paths": changed,
        "expected_blocker_keys": manifest["expected_blocker_keys"],
        "normalization_report_sha256": manifest[
            "normalization_report_sha256"
        ],
        "field_level_proof_sha256": manifest["field_level_proof_sha256"],
        "integration_freeze_sha256": manifest[
            "integration_freeze_sha256"
        ],
        "semantic_snapshot_sha256": manifest[
            "semantic_snapshot_sha256"
        ],
        "semantic_drift": "PASS",
        "stage2_status": result["stage2_status"],
        "decision_universe_sha256": comparisons[
            "decision_universe_sha256"
        ],
        "capability_census_status": comparisons[
            "capability_census_status"
        ],
        "artifact_sha256": actual_raw,
        "artifact_normalized_sha256": actual_normalized,
        "normalized_equivalence_artifacts": normalized_equivalence,
        "tracked_stage2_mutation": "NONE",
        "remote_stage2_opponent_display_equivalence": "PASS",
    }
    verify_dir = Path(
        ".remote-implementation/verifications/%s/%s"
        % (successor["school_key"], successor["request_id"])
    )
    write_json(
        verify_dir / "stage2-opponent-display-verification.json",
        verification,
    )

    local_state = read_json(STATE_PATH)
    validate_control_state(local_state)
    local_last = local_state.get("last_operation") or {}
    if (
        local_last.get("operation")
        != OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE
        or local_last.get("request_id") != successor["request_id"]
    ):
        raise Stop("OPPONENT_DISPLAY_FRESH_CONTROL_MOVED")
    local_last["fresh_runner_verification"] = "PASS"
    local_last[
        "remote_stage2_opponent_display_equivalence"
    ] = "PASS"
    local_state["last_operation"] = local_last
    write_json(STATE_PATH, local_state)
    commit = commit_control(
        control_head,
        "persist fresh Stage 2 opponent-display verification %s"
        % successor["request_id"],
        [STATE_PATH, verify_dir],
    )
    print(
        "REMOTE STAGE 2 OPPONENT DISPLAY EQUIVALENCE: PASS "
        "verification_commit=%s" % commit
    )
    return 0


def main() -> int:
    DIAG.mkdir(parents=True, exist_ok=True)
    try:
        configure_git()
        live_main, control_head = fetch_operational_refs()
        state = git_show_json(control_head, STATE_PATH.as_posix())
        validate_control_state(state)
        if state.get("lifecycle_state") != LIFECYCLE_IDLE:
            raise Stop("FRESH_VERIFY_CONTROL_NOT_IDLE")
        last = state.get("last_operation") or {}
        if last.get("operation") == OP_STAGE2_CENSUS:
            return verify_stage2_census(
                live_main,
                control_head,
                state,
            )
        if last.get("operation") == OP_STAGE2_PROPOSAL_REHEARSAL:
            return verify_stage2_proposal_rehearsal(
                live_main,
                control_head,
                state,
            )
        if last.get("operation") == OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE:
            return verify_stage2_opponent_display_normalization(
                live_main,
                control_head,
                state,
            )
        if last.get("operation") != OP_PHASE0:
            if last.get("operation") == OP_RECOVER:
                print("REMOTE PHASE 0 VERIFICATION: NOT APPLICABLE AFTER ABANDONED RECOVERY")
                return 0
            raise Stop("FRESH_VERIFY_NO_PHASE0_SUCCESSOR")
        if last.get("fresh_runner_verification") == "PASS":
            print("REMOTE PHASE 0 EQUIVALENCE: PASS (already verified)")
            return 0

        successor_path = last["successor_manifest_path"]
        successor_bytes = git_show_bytes(control_head, successor_path)
        if sha256_bytes(successor_bytes) != last["successor_manifest_sha256"]:
            raise Stop("FRESH_VERIFY_SUCCESSOR_HASH_MISMATCH")
        successor = json.loads(successor_bytes)
        if successor.get("protected_main_sha") != live_main:
            raise Stop("FRESH_VERIFY_MAIN_CHANGED")
        target_branch = successor["target_branch"]
        target_sha = remote_head(ROOT, target_branch)
        if target_sha != successor["prepared_commit_sha"]:
            raise Stop("FRESH_VERIFY_TARGET_REF_MISMATCH")
        git(
            "fetch",
            "--no-tags",
            "origin",
            "+refs/heads/%s:refs/remotes/origin/remote-target" % target_branch,
        )
        fetched_target = git(
            "rev-parse",
            "refs/remotes/origin/remote-target",
        ).stdout.strip()
        if fetched_target != target_sha:
            raise Stop("FRESH_VERIFY_TARGET_FETCH_MISMATCH")

        writeahead_path = successor["writeahead_manifest_path"]
        writeahead_bytes = git_show_bytes(control_head, writeahead_path)
        if (
            sha256_bytes(writeahead_bytes)
            != successor["writeahead_manifest_sha256"]
        ):
            raise Stop("FRESH_VERIFY_WRITEAHEAD_HASH_MISMATCH")
        manifest = json.loads(writeahead_bytes)
        prefix = Path(writeahead_path).parent
        bundle = Path(tempfile.mkdtemp(prefix="remote-fresh-writeahead-"))
        for relative, expected in manifest["sidecars"].items():
            data = git_show_bytes(
                control_head,
                (prefix / relative).as_posix(),
            )
            target = bundle / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            if sha256_bytes(data) != expected:
                raise Stop(
                    "FRESH_VERIFY_SIDECAR_HASH_MISMATCH:%s" % relative
                )

        prepared = manifest["prepared_commit_sha"]
        parent = git("rev-parse", "%s^" % prepared).stdout.strip()
        tree = git("rev-parse", "%s^{tree}" % prepared).stdout.strip()
        if parent != manifest["prepared_parent_sha"]:
            raise Stop("FRESH_VERIFY_PARENT_MISMATCH")
        if tree != manifest["prepared_tree_sha"]:
            raise Stop("FRESH_VERIFY_TREE_MISMATCH")
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
            raise Stop("FRESH_VERIFY_CHANGED_PATH_MISMATCH")
        for path, expected in manifest["changed_file_sha256"].items():
            if sha256_bytes(git_show_bytes(prepared, path)) != expected:
                raise Stop(
                    "FRESH_VERIFY_CHANGED_FILE_HASH_MISMATCH:%s" % path
                )

        freeze_bytes = (bundle / "integration-freeze.json").read_bytes()
        if (
            sha256_bytes(freeze_bytes)
            != manifest["integration_freeze_sha256"]
        ):
            raise Stop("FRESH_VERIFY_INTEGRATION_FREEZE_HASH_MISMATCH")
        integration = json.loads(freeze_bytes)
        if (
            integration.get("integration_base_sha") != live_main
            or integration.get("origin_main_sha") != live_main
        ):
            raise Stop("FRESH_VERIFY_INTEGRATION_BASE_MISMATCH")

        verify_tree = Path(
            tempfile.mkdtemp(prefix="remote-phase0-verify-")
        )
        shutil.rmtree(verify_tree)
        git("worktree", "add", "--detach", str(verify_tree), prepared)
        validation = run(
            [sys.executable, "tools/validate_data.py"],
            cwd=verify_tree,
            check=False,
        )
        (DIAG / "validate-data.log").write_text(
            validation.stdout,
            encoding="utf-8",
        )
        if validation.returncode != 0:
            raise Stop("FRESH_VERIFY_REPOSITORY_VALIDATION_FAILED")

        for name in REQUIRED_PACKAGE_FILES:
            data = (
                verify_tree
                / "schools"
                / successor["school_key"]
                / name
            ).read_bytes()
            if (
                sha256_bytes(data)
                != manifest["package_member_sha256"].get(name)
            ):
                raise Stop(
                    "FRESH_VERIFY_PACKAGE_MEMBER_HASH_MISMATCH:%s" % name
                )

        sem_script = (
            "import json,sys\n"
            "from pathlib import Path\n"
            "root=Path(sys.argv[1]); school=sys.argv[2]\n"
            "sys.path.insert(0,str(root/'tools'))\n"
            "from integration_freeze_guard import build_source_game_semantic_snapshot, semantic_snapshot_sha256\n"
            "snap=build_source_game_semantic_snapshot(root/'schools'/school/'source-games.csv')\n"
            "print(json.dumps({'hash':semantic_snapshot_sha256(snap)},sort_keys=True))\n"
        )
        sem = run(
            [
                sys.executable,
                "-c",
                sem_script,
                str(verify_tree),
                successor["school_key"],
            ],
            check=True,
        )
        semantic_hash = json.loads(sem.stdout)["hash"]
        if semantic_hash != manifest["semantic_snapshot_sha256"]:
            raise Stop("FRESH_VERIFY_SEMANTIC_SNAPSHOT_MISMATCH")

        verification = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_FRESH_VERIFICATION",
            "request_id": successor["request_id"],
            "school_key": successor["school_key"],
            "protected_main_sha": live_main,
            "target_branch": target_branch,
            "target_sha": target_sha,
            "prepared_commit_sha": prepared,
            "prepared_tree_sha": tree,
            "prepared_parent_sha": parent,
            "integration_freeze_sha256": manifest[
                "integration_freeze_sha256"
            ],
            "semantic_snapshot_sha256": semantic_hash,
            "repository_validation": "PASS",
            "exact_sidecars_verified": True,
            "package_member_hashes_verified": True,
            "remote_phase0_equivalence": "PASS",
        }
        directory = Path(
            ".remote-implementation/verifications/%s/%s"
            % (successor["school_key"], successor["request_id"])
        )
        write_json(directory / "fresh-verification.json", verification)

        local_state = read_json(STATE_PATH)
        validate_control_state(local_state)
        local_last = local_state.get("last_operation") or {}
        if local_last.get("request_id") != successor["request_id"]:
            raise Stop("FRESH_VERIFY_CONTROL_MOVED")
        local_last["fresh_runner_verification"] = "PASS"
        local_last["remote_phase0_equivalence"] = "PASS"
        local_state["last_operation"] = local_last
        write_json(STATE_PATH, local_state)
        commit = commit_control(
            control_head,
            "persist fresh Phase 0 verification %s"
            % successor["request_id"],
            [STATE_PATH, directory],
        )
        print(
            "REMOTE PHASE 0 EQUIVALENCE: PASS verification_commit=%s"
            % commit
        )
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
