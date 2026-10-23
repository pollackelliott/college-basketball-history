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

DIAG = Path(
    os.environ.get(
        "REMOTE_IMPLEMENTATION_DIAG",
        "/tmp/remote-implementation-verification",
    )
)


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
