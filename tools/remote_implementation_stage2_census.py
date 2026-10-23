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


def normalize_artifact_bytes(
    name: str,
    data: bytes,
    repo: Path,
) -> bytes:
    """Normalize only documented non-semantic replay variance.

    The permanent preflight records a wall-clock ``created_at`` in plan.json and
    renders the same value as ``Generated:`` in review.md. Those fields are
    diagnostic chronology, not decision-universe authority. Absolute runner
    repository paths may also vary. No other content is normalized.
    """
    result = data
    for value in {str(repo), str(repo.resolve())}:
        if value:
            result = result.replace(value.encode("utf-8"), b"<REPO>")
    if name == STAGE2_PLAN:
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
    if successor.get("actual_published_target_sha") != request["target_sha"]:
        raise Stop("STAGE2_PHASE0_SUCCESSOR_TARGET_MISMATCH")
    if successor.get("prepared_commit_sha") != request["target_sha"]:
        raise Stop("STAGE2_PHASE0_PREPARED_COMMIT_MISMATCH")
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
    if writeahead.get("prepared_commit_sha") != request["target_sha"]:
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
        actual = sha256_bytes(
            git_show_bytes(
                request["target_sha"],
                "schools/%s/%s" % (request["school_key"], name),
                cwd=source_repo,
            )
        )
        if not expected or actual != expected:
            raise Stop("STAGE2_PHASE0_PACKAGE_HASH_MISMATCH:%s" % name)

    return {
        "successor": successor,
        "successor_bytes": successor_bytes,
        "writeahead": writeahead,
        "writeahead_bytes": writeahead_bytes,
        "freeze_bytes": freeze_bytes,
        "freeze_path": freeze_path,
        "phase0_protected_main_sha": successor.get("protected_main_sha"),
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
) -> dict[str, Any]:
    restore_integration_freeze(repo, school_key, freeze_bytes)
    before = tracked_worktree_state(repo)
    if before["status"]:
        raise Stop("STAGE2_TRACKED_STATE_DIRTY_BEFORE_RUN")

    cmd = [
        sys.executable,
        str(repo / "tools/implementation_stage2.py"),
        school_key,
        "--repo",
        str(repo),
    ]
    cp = run(cmd, cwd=repo, check=False)
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
