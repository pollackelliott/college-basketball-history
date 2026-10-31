#!/usr/bin/env python3
"""Read-only orchestration helpers for remote Implementation Stage 2 census."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from remote_implementation_control import sha256_bytes, sha256_file
from remote_implementation_io import (
    REQUIRED_PACKAGE_FILES,
    ROOT,
    Stop,
    configure_git,
    git,
    git_show_bytes,
    remote_head,
    run,
)

STAGE2_STATUS = "implementation-stage2-status.json"
STAGE2_CENSUS = "implementation-stage2-capability-census.json"
STAGE2_PLAN = "plan.json"
STAGE2_REVIEW = "review.csv"
STAGE2_REPORT = "review.md"
STAGE2_ARTIFACT_NAMES = (
    STAGE2_STATUS,
    STAGE2_CENSUS,
    STAGE2_PLAN,
    STAGE2_REVIEW,
    STAGE2_REPORT,
)
STAGE2_ALLOWED_STATUSES = {"CAPABILITY_CENSUS_READY", "BLOCKED"}
RUNTIME_ROOT = Path(__file__).resolve().parents[1]
OPPONENT_DISPLAY_PACKAGE_FILES = ("opponents.csv", "source-games.csv")



def normalize_artifact_bytes(
    name: str,
    data: bytes,
    repo: Path,
) -> bytes:
    """Normalize only documented non-semantic replay variance.

    The permanent preflight records a wall-clock ``created_at`` in plan.json and
    renders the same value as ``Generated:`` in review.md. Stage-2 status also
    records the ephemeral local worktree branch name. Those fields are diagnostic
    runner metadata, not decision-universe authority. Absolute runner repository
    paths may also vary. No other content is normalized.
    """
    result = data
    for value in {str(repo), str(repo.resolve())}:
        if value:
            result = result.replace(value.encode("utf-8"), b"<REPO>")
    if name == STAGE2_STATUS:
        doc = json.loads(result)
        if "branch" in doc:
            doc["branch"] = "<WORKTREE_BRANCH>"
        result = (
            json.dumps(
                doc,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode("utf-8")
    elif name == STAGE2_PLAN:
        doc = json.loads(result)
        if "created_at" in doc:
            doc["created_at"] = "<GENERATED_AT>"
        result = (
            json.dumps(
                doc,
                ensure_ascii=False,
                indent=2,
                sort_keys=False,
            )
            + "\n"
        ).encode("utf-8")
    elif name == STAGE2_REPORT:
        text = result.decode("utf-8")
        lines = [
            "Generated: <GENERATED_AT>"
            if line.startswith("Generated: ")
            else line
            for line in text.splitlines()
        ]
        result = ("\n".join(lines) + ("\n" if text.endswith("\n") else "")).encode(
            "utf-8"
        )
    return result

def tracked_worktree_state(repo: Path) -> dict[str, str]:
    return {
        "head_sha": git("rev-parse", "HEAD", cwd=repo).stdout.strip(),
        "tree_sha": git("rev-parse", "HEAD^{tree}", cwd=repo).stdout.strip(),
        "status": git(
            "status",
            "--porcelain",
            "--untracked-files=all",
            cwd=repo,
        ).stdout,
    }


def add_existing_onboarding_worktree(
    target_branch: str,
    target_sha: str,
    school_key: str,
    *,
    source_repo: Path = ROOT,
) -> Path:
    actual = remote_head(source_repo, target_branch)
    if actual != target_sha:
        raise Stop(
            "STAGE2_ONBOARDING_HEAD_MISMATCH expected=%s actual=%s"
            % (target_sha, actual or "[missing]")
        )
    git(
        "fetch",
        "--no-tags",
        "origin",
        "+refs/heads/%s:refs/remotes/origin/remote-stage2-target"
        % target_branch,
        cwd=source_repo,
    )
    fetched = git(
        "rev-parse",
        "refs/remotes/origin/remote-stage2-target",
        cwd=source_repo,
    ).stdout.strip()
    if fetched != target_sha:
        raise Stop("STAGE2_ONBOARDING_FETCH_MISMATCH")
    path = Path(tempfile.mkdtemp(prefix="remote-stage2-%s-" % school_key))
    shutil.rmtree(path)
    local_branch = "remote-stage2-census/%s-%s" % (school_key, target_sha[:12])
    git(
        "worktree",
        "add",
        "-b",
        local_branch,
        str(path),
        target_sha,
        cwd=source_repo,
    )
    configure_git(path)
    state = tracked_worktree_state(path)
    if state["head_sha"] != target_sha:
        raise Stop("STAGE2_WORKTREE_HEAD_MISMATCH")
    if state["status"]:
        raise Stop("STAGE2_WORKTREE_NOT_CLEAN")
    return path


def _school_package_hash(
    commit_sha: str,
    school_key: str,
    name: str,
    *,
    source_repo: Path,
) -> str:
    return sha256_bytes(
        git_show_bytes(
            commit_sha,
            "schools/%s/%s" % (school_key, name),
            cwd=source_repo,
        )
    )


def _verify_opponent_display_target_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    phase0_target_sha: str,
    package_hashes: dict[str, str],
    source_repo: Path,
) -> dict[str, Any]:
    ref = request.get("stage2_opponent_display_successor")
    if not isinstance(ref, dict):
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_REFERENCE_REQUIRED")

    successor_bytes = git_show_bytes(
        control_commit,
        str(ref.get("path") or ""),
        cwd=source_repo,
    )
    if sha256_bytes(successor_bytes) != ref.get("sha256"):
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_HASH_MISMATCH")
    successor = json.loads(successor_bytes)
    if successor.get("kind") != "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR":
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_KIND_MISMATCH")
    if successor.get("operation") != "STAGE2_OPPONENT_DISPLAY_NORMALIZE":
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_OPERATION_MISMATCH")
    if successor.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_SCHOOL_MISMATCH")
    if successor.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_BRANCH_MISMATCH")
    if successor.get("expected_target_predecessor_sha") != phase0_target_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_PREDECESSOR_MISMATCH")
    if successor.get("prepared_parent_sha") != phase0_target_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_PREPARED_PARENT_MISMATCH")
    if successor.get("actual_published_target_sha") != request["target_sha"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_TARGET_MISMATCH")
    if successor.get("prepared_commit_sha") != request["target_sha"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_PREPARED_COMMIT_MISMATCH")
    if successor.get("publication_cas") != "EXISTING_REF_CAS_PASS":
        raise Stop("STAGE2_OPPONENT_DISPLAY_PUBLICATION_CAS_MISMATCH")
    if successor.get("repository_validation") != "PASS":
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_NOT_VALIDATED")
    if successor.get("final_transaction_state") != "COMPLETE":
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_NOT_COMPLETE")
    if successor.get("integration_freeze_sha256") != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_FREEZE_MISMATCH")
    if successor.get("semantic_snapshot_sha256") != request["semantic_snapshot_sha256"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_SEMANTIC_MISMATCH")

    for label in ("semantic_drift_before", "semantic_drift_after"):
        drift = successor.get(label) or {}
        if (
            drift.get("status") != "PASS"
            or list(drift.get("changes") or [])
            or drift.get("baseline_sha256") != request["semantic_snapshot_sha256"]
            or drift.get("current_sha256") != request["semantic_snapshot_sha256"]
        ):
            raise Stop(
                "STAGE2_OPPONENT_DISPLAY_SUCCESSOR_%s_MISMATCH"
                % label.upper()
            )

    allowed_paths = {
        "schools/%s/%s" % (request["school_key"], name)
        for name in OPPONENT_DISPLAY_PACKAGE_FILES
    }
    changed_paths = list(successor.get("changed_paths") or [])
    if not changed_paths or not set(changed_paths).issubset(allowed_paths):
        raise Stop("STAGE2_OPPONENT_DISPLAY_CHANGED_PATHS_INVALID")
    changed_hashes = successor.get("changed_file_sha256") or {}
    if set(changed_hashes) != set(changed_paths):
        raise Stop("STAGE2_OPPONENT_DISPLAY_CHANGED_HASH_SET_MISMATCH")

    parents = git(
        "show",
        "-s",
        "--format=%P",
        request["target_sha"],
        cwd=source_repo,
    ).stdout.strip().split()
    if parents != [phase0_target_sha]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_GIT_PARENT_MISMATCH")
    actual_diff = sorted(
        line.strip()
        for line in git(
            "diff",
            "--name-only",
            phase0_target_sha,
            request["target_sha"],
            cwd=source_repo,
        ).stdout.splitlines()
        if line.strip()
    )
    if actual_diff != sorted(changed_paths):
        raise Stop("STAGE2_OPPONENT_DISPLAY_GIT_DIFF_MISMATCH")

    actual_tree = git(
        "rev-parse",
        request["target_sha"] + "^{tree}",
        cwd=source_repo,
    ).stdout.strip()
    if successor.get("prepared_tree_sha") != actual_tree:
        raise Stop("STAGE2_OPPONENT_DISPLAY_PREPARED_TREE_MISMATCH")

    writeahead_path = str(successor.get("writeahead_manifest_path") or "")
    writeahead_sha = str(successor.get("writeahead_manifest_sha256") or "")
    if not writeahead_path or not writeahead_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_REFERENCE_MISSING")
    writeahead_bytes = git_show_bytes(
        control_commit,
        writeahead_path,
        cwd=source_repo,
    )
    if sha256_bytes(writeahead_bytes) != writeahead_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_HASH_MISMATCH")
    writeahead = json.loads(writeahead_bytes)
    if writeahead.get("kind") != "REMOTE_IMPLEMENTATION_WRITEAHEAD":
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_KIND_MISMATCH")
    if writeahead.get("operation") != "STAGE2_OPPONENT_DISPLAY_NORMALIZE":
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_OPERATION_MISMATCH")
    if writeahead.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_SCHOOL_MISMATCH")
    if writeahead.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_BRANCH_MISMATCH")
    if writeahead.get("expected_target_predecessor_sha") != phase0_target_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_PREDECESSOR_MISMATCH")
    if writeahead.get("prepared_parent_sha") != phase0_target_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_PARENT_MISMATCH")
    if writeahead.get("prepared_commit_sha") != request["target_sha"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_TARGET_MISMATCH")
    if writeahead.get("prepared_tree_sha") != actual_tree:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_TREE_MISMATCH")
    if list(writeahead.get("changed_paths") or []) != changed_paths:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_PATH_MISMATCH")
    if (writeahead.get("changed_file_sha256") or {}) != changed_hashes:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_FILE_HASH_MISMATCH")
    if set(writeahead.get("allowed_paths") or []) != allowed_paths:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_ALLOWED_PATH_MISMATCH")
    if writeahead.get("integration_freeze_sha256") != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_FREEZE_MISMATCH")
    if writeahead.get("semantic_snapshot_sha256") != request["semantic_snapshot_sha256"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_WRITEAHEAD_SEMANTIC_MISMATCH")

    proof_sha = str(successor.get("field_level_proof_sha256") or "")
    if not proof_sha or writeahead.get("field_level_proof_sha256") != proof_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FIELD_PROOF_BINDING_MISMATCH")
    proof_path = (Path(writeahead_path).parent / "field-level-proof.json").as_posix()
    proof_bytes = git_show_bytes(control_commit, proof_path, cwd=source_repo)
    if sha256_bytes(proof_bytes) != proof_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FIELD_PROOF_HASH_MISMATCH")
    if (writeahead.get("sidecars") or {}).get("field-level-proof.json") != proof_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FIELD_PROOF_SIDECAR_MISMATCH")
    proof = json.loads(proof_bytes)
    if proof.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FIELD_PROOF_SCHOOL_MISMATCH")
    if set(proof.get("allowed_paths") or []) != allowed_paths:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FIELD_PROOF_ALLOWED_PATH_MISMATCH")
    for field in (
        "literal_evidence_changes",
        "opponent_key_changes",
        "source_game_non_name_field_changes",
    ):
        if int(proof.get(field, -1)) != 0:
            raise Stop(
                "STAGE2_OPPONENT_DISPLAY_FIELD_PROOF_NONREPRESENTATIONAL:%s"
                % field
            )
    blocker_keys = sorted(str(x) for x in successor.get("expected_blocker_keys") or [])
    if not blocker_keys:
        raise Stop("STAGE2_OPPONENT_DISPLAY_BLOCKER_KEYS_MISSING")
    if sorted(str(x) for x in proof.get("opponent_changed_keys") or []) != blocker_keys:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FIELD_PROOF_OPPONENT_KEYS_MISMATCH")
    if sorted(str(x) for x in proof.get("source_game_changed_keys") or []) != blocker_keys:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FIELD_PROOF_SOURCE_KEYS_MISMATCH")
    if int(proof.get("source_game_normalized_name_row_count", -1)) != int(
        successor.get("source_game_normalized_name_row_count", -2)
    ):
        raise Stop("STAGE2_OPPONENT_DISPLAY_FIELD_PROOF_ROW_COUNT_MISMATCH")

    verification_path = (
        ".remote-implementation/verifications/%s/%s/"
        "stage2-opponent-display-verification.json"
        % (request["school_key"], successor.get("request_id"))
    )
    verification_bytes = git_show_bytes(
        control_commit,
        verification_path,
        cwd=source_repo,
    )
    verification = json.loads(verification_bytes)
    if verification.get("kind") != "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_VERIFICATION":
        raise Stop("STAGE2_OPPONENT_DISPLAY_VERIFICATION_KIND_MISMATCH")
    bindings = {
        "request_id": successor.get("request_id"),
        "school_key": request["school_key"],
        "target_branch": request["target_branch"],
        "target_predecessor_sha": phase0_target_sha,
        "target_sha": request["target_sha"],
        "target_tree_sha": actual_tree,
        "integration_freeze_sha256": request["integration_freeze_sha256"],
        "semantic_snapshot_sha256": request["semantic_snapshot_sha256"],
        "field_level_proof_sha256": proof_sha,
        "normalization_report_sha256": successor.get("normalization_report_sha256"),
        "protected_main_sha": successor.get("protected_main_sha"),
    }
    for field, expected in bindings.items():
        if verification.get(field) != expected:
            raise Stop(
                "STAGE2_OPPONENT_DISPLAY_VERIFICATION_BINDING_MISMATCH:%s"
                % field
            )
    if sorted(verification.get("changed_paths") or []) != sorted(changed_paths):
        raise Stop("STAGE2_OPPONENT_DISPLAY_VERIFICATION_PATH_MISMATCH")
    if sorted(verification.get("expected_blocker_keys") or []) != blocker_keys:
        raise Stop("STAGE2_OPPONENT_DISPLAY_VERIFICATION_BLOCKER_MISMATCH")
    if verification.get("semantic_drift") != "PASS":
        raise Stop("STAGE2_OPPONENT_DISPLAY_VERIFICATION_SEMANTIC_MISMATCH")
    if verification.get("tracked_stage2_mutation") != "NONE":
        raise Stop("STAGE2_OPPONENT_DISPLAY_VERIFICATION_MUTATION_MISMATCH")
    if verification.get("remote_stage2_opponent_display_equivalence") != "PASS":
        raise Stop("STAGE2_OPPONENT_DISPLAY_VERIFICATION_NOT_PASS")

    for path, expected in changed_hashes.items():
        actual = sha256_bytes(
            git_show_bytes(request["target_sha"], path, cwd=source_repo)
        )
        if actual != expected:
            raise Stop(
                "STAGE2_OPPONENT_DISPLAY_CHANGED_FILE_HASH_MISMATCH:%s"
                % path
            )

    changed_names = {
        Path(path).name
        for path in changed_paths
        if path.startswith("schools/%s/" % request["school_key"])
    }
    for name in REQUIRED_PACKAGE_FILES:
        actual = _school_package_hash(
            request["target_sha"],
            request["school_key"],
            name,
            source_repo=source_repo,
        )
        if name in changed_names:
            expected = changed_hashes.get(
                "schools/%s/%s" % (request["school_key"], name)
            )
        else:
            expected = package_hashes.get(name)
        if not expected or actual != expected:
            raise Stop(
                "STAGE2_OPPONENT_DISPLAY_PACKAGE_HASH_MISMATCH:%s" % name
            )

    return {
        "successor": successor,
        "successor_bytes": successor_bytes,
        "writeahead": writeahead,
        "writeahead_bytes": writeahead_bytes,
        "field_level_proof": proof,
        "field_level_proof_bytes": proof_bytes,
        "verification": verification,
        "verification_bytes": verification_bytes,
        "verification_path": verification_path,
    }


def verify_phase0_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path = ROOT,
) -> dict[str, Any]:
    successor_ref = request["phase0_successor"]
    successor_bytes = git_show_bytes(control_commit, successor_ref["path"], cwd=source_repo)
    if sha256_bytes(successor_bytes) != successor_ref["sha256"]:
        raise Stop("STAGE2_PHASE0_SUCCESSOR_HASH_MISMATCH")
    successor = json.loads(successor_bytes)
    if successor.get("kind") != "REMOTE_IMPLEMENTATION_SUCCESSOR":
        raise Stop("STAGE2_PHASE0_SUCCESSOR_KIND_MISMATCH")
    if successor.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_PHASE0_SUCCESSOR_SCHOOL_MISMATCH")
    if successor.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_PHASE0_SUCCESSOR_BRANCH_MISMATCH")
    phase0_target_sha = str(successor.get("actual_published_target_sha") or "")
    if not phase0_target_sha or successor.get("prepared_commit_sha") != phase0_target_sha:
        raise Stop("STAGE2_PHASE0_SUCCESSOR_TARGET_MISMATCH")
    if successor.get("integration_freeze_sha256") != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_PHASE0_INTEGRATION_FREEZE_MISMATCH")
    if successor.get("semantic_snapshot_sha256") != request["semantic_snapshot_sha256"]:
        raise Stop("STAGE2_PHASE0_SEMANTIC_SNAPSHOT_MISMATCH")
    if successor.get("repository_validation") != "PASS":
        raise Stop("STAGE2_PHASE0_SUCCESSOR_NOT_VALIDATED")
    if successor.get("final_transaction_state") != "COMPLETE":
        raise Stop("STAGE2_PHASE0_SUCCESSOR_NOT_COMPLETE")

    writeahead_path = str(successor.get("writeahead_manifest_path") or "")
    writeahead_sha = str(successor.get("writeahead_manifest_sha256") or "")
    if not writeahead_path or not writeahead_sha:
        raise Stop("STAGE2_PHASE0_WRITEAHEAD_REFERENCE_MISSING")
    writeahead_bytes = git_show_bytes(control_commit, writeahead_path, cwd=source_repo)
    if sha256_bytes(writeahead_bytes) != writeahead_sha:
        raise Stop("STAGE2_PHASE0_WRITEAHEAD_HASH_MISMATCH")
    writeahead = json.loads(writeahead_bytes)
    if writeahead.get("kind") != "REMOTE_IMPLEMENTATION_WRITEAHEAD":
        raise Stop("STAGE2_PHASE0_WRITEAHEAD_KIND_MISMATCH")
    if writeahead.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_PHASE0_WRITEAHEAD_SCHOOL_MISMATCH")
    if writeahead.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_PHASE0_WRITEAHEAD_BRANCH_MISMATCH")
    if writeahead.get("prepared_commit_sha") != phase0_target_sha:
        raise Stop("STAGE2_PHASE0_WRITEAHEAD_TARGET_MISMATCH")
    if writeahead.get("integration_freeze_sha256") != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_PHASE0_WRITEAHEAD_FREEZE_MISMATCH")
    if writeahead.get("semantic_snapshot_sha256") != request["semantic_snapshot_sha256"]:
        raise Stop("STAGE2_PHASE0_WRITEAHEAD_SEMANTIC_MISMATCH")

    freeze_path = (
        Path(writeahead_path).parent / "integration-freeze.json"
    ).as_posix()
    freeze_bytes = git_show_bytes(control_commit, freeze_path, cwd=source_repo)
    sidecar_hash = (writeahead.get("sidecars") or {}).get("integration-freeze.json")
    if sidecar_hash != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_PHASE0_FREEZE_SIDECAR_BINDING_MISMATCH")
    if sha256_bytes(freeze_bytes) != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_PHASE0_FREEZE_BYTES_MISMATCH")
    integration = json.loads(freeze_bytes)
    if integration.get("status") != "INTEGRATION_FROZEN":
        raise Stop("STAGE2_INTEGRATION_FREEZE_STATUS_MISMATCH")
    if integration.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_INTEGRATION_FREEZE_SCHOOL_MISMATCH")
    semantic = (integration.get("source_game_semantic_guard") or {}).get(
        "snapshot_sha256"
    )
    if semantic != request["semantic_snapshot_sha256"]:
        raise Stop("STAGE2_INTEGRATION_FREEZE_SEMANTIC_MISMATCH")

    package_hashes = integration.get("package_member_sha256") or {}
    for name in REQUIRED_PACKAGE_FILES:
        expected = package_hashes.get(name)
        actual = _school_package_hash(
            phase0_target_sha,
            request["school_key"],
            name,
            source_repo=source_repo,
        )
        if not expected or actual != expected:
            raise Stop("STAGE2_PHASE0_PACKAGE_HASH_MISMATCH:%s" % name)

    display_authority: dict[str, Any] | None = None
    if request["target_sha"] == phase0_target_sha:
        if request.get("stage2_opponent_display_successor") is not None:
            raise Stop("STAGE2_OPPONENT_DISPLAY_SUCCESSOR_NOT_APPLICABLE")
        target_authority_kind = "PHASE0_SUCCESSOR"
    else:
        display_authority = _verify_opponent_display_target_authority(
            request,
            control_commit,
            phase0_target_sha=phase0_target_sha,
            package_hashes=package_hashes,
            source_repo=source_repo,
        )
        target_authority_kind = "STAGE2_OPPONENT_DISPLAY_SUCCESSOR"

    return {
        "successor": successor,
        "successor_bytes": successor_bytes,
        "writeahead": writeahead,
        "writeahead_bytes": writeahead_bytes,
        "freeze_bytes": freeze_bytes,
        "freeze_path": freeze_path,
        "phase0_target_sha": phase0_target_sha,
        "phase0_protected_main_sha": successor.get("protected_main_sha"),
        "target_authority_kind": target_authority_kind,
        "opponent_display_authority": display_authority,
    }


def restore_integration_freeze(
    repo: Path,
    school_key: str,
    freeze_bytes: bytes,
) -> Path:
    path = repo / ".onboarding" / school_key / "integration-freeze.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(freeze_bytes)
    return path


def stage2_artifact_hashes(
    repo: Path,
    school_key: str,
) -> tuple[dict[str, str], dict[str, str]]:
    directory = repo / ".onboarding" / school_key
    raw: dict[str, str] = {}
    normalized: dict[str, str] = {}
    for name in STAGE2_ARTIFACT_NAMES:
        path = directory / name
        if not path.is_file():
            continue
        data = path.read_bytes()
        raw[name] = sha256_bytes(data)
        normalized[name] = sha256_bytes(
            normalize_artifact_bytes(name, data, repo)
        )
    return raw, normalized


def run_stage2_census_tool(
    repo: Path,
    school_key: str,
    freeze_bytes: bytes,
    diag: Path,
    *,
    tool_repo: Path | None = None,
) -> dict[str, Any]:
    restore_integration_freeze(repo, school_key, freeze_bytes)
    before = tracked_worktree_state(repo)
    if before["status"]:
        raise Stop("STAGE2_TRACKED_STATE_DIRTY_BEFORE_RUN")

    runtime_repo = (tool_repo or RUNTIME_ROOT).resolve()
    tool_path = runtime_repo / "tools/implementation_stage2.py"
    if not tool_path.is_file():
        raise Stop("STAGE2_RUNTIME_TOOL_MISSING:%s" % tool_path)
    cmd = [
        sys.executable,
        str(tool_path),
        school_key,
        "--repo",
        str(repo),
    ]
    cp = run(cmd, cwd=runtime_repo, check=False)
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "stage2-census.log").write_text(cp.stdout, encoding="utf-8")

    after = tracked_worktree_state(repo)
    if (
        before["head_sha"] != after["head_sha"]
        or before["tree_sha"] != after["tree_sha"]
        or after["status"]
    ):
        raise Stop(
            "TRACKED_STAGE2_MUTATION_DETECTED before_head=%s after_head=%s "
            "before_tree=%s after_tree=%s status=%r"
            % (
                before["head_sha"],
                after["head_sha"],
                before["tree_sha"],
                after["tree_sha"],
                after["status"],
            )
        )

    status_path = (
        repo
        / ".onboarding"
        / school_key
        / STAGE2_STATUS
    )
    if not status_path.is_file():
        raise Stop("PERMANENT_STAGE2_STATUS_ARTIFACT_MISSING")
    status = json.loads(status_path.read_text(encoding="utf-8"))
    stage2_status = str(status.get("status") or "")
    if stage2_status not in STAGE2_ALLOWED_STATUSES:
        raise Stop("PERMANENT_STAGE2_STATUS_UNSUPPORTED:%s" % stage2_status)
    if stage2_status == "CAPABILITY_CENSUS_READY" and cp.returncode != 0:
        raise Stop("PERMANENT_STAGE2_READY_EXIT_CODE_MISMATCH")
    if stage2_status == "BLOCKED" and cp.returncode == 0:
        raise Stop("PERMANENT_STAGE2_BLOCKED_EXIT_CODE_MISMATCH")

    raw_hashes, normalized_hashes = stage2_artifact_hashes(repo, school_key)
    if STAGE2_STATUS not in raw_hashes:
        raise Stop("PERMANENT_STAGE2_STATUS_ARTIFACT_MISSING")
    capability = status.get("capability_census") or {}
    if capability.get("path") and STAGE2_CENSUS not in raw_hashes:
        raise Stop("PERMANENT_STAGE2_CAPABILITY_CENSUS_MISSING")
    if stage2_status == "CAPABILITY_CENSUS_READY":
        for name in STAGE2_ARTIFACT_NAMES:
            if name not in raw_hashes:
                raise Stop("PERMANENT_STAGE2_READY_ARTIFACT_MISSING:%s" % name)

    census_doc: dict[str, Any] | None = None
    census_path = repo / ".onboarding" / school_key / STAGE2_CENSUS
    if census_path.is_file():
        census_doc = json.loads(census_path.read_text(encoding="utf-8"))

    return {
        "command": ["python", "tools/implementation_stage2.py", school_key],
        "exit_code": cp.returncode,
        "stage2_status": stage2_status,
        "status": status,
        "capability_census": census_doc,
        "artifact_sha256": raw_hashes,
        "artifact_normalized_sha256": normalized_hashes,
        "tracked_mutation_proof": {
            "before_head_sha": before["head_sha"],
            "after_head_sha": after["head_sha"],
            "before_tree_sha": before["tree_sha"],
            "after_tree_sha": after["tree_sha"],
            "before_status": before["status"],
            "after_status": after["status"],
            "tracked_stage2_mutation": "NONE",
        },
    }
