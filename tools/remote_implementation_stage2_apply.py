#!/usr/bin/env python3
"""Remote sealed apply for one fresh-verified Gate 1 seal.

This module authenticates one exact cryptographic Gate 1 seal, replays the
pre-seal technical suite against current protected-main runtime, invokes the
permanent transactional --apply path against the exact sealed hash, prepares
one tracked successor commit, and supplies deterministic proof for write-ahead,
CAS publication, recovery, and fresh verification.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from remote_implementation_control import sha256_bytes, sha256_file
from remote_implementation_io import (
    ROOT,
    Stop,
    commit_file_hashes,
    configure_git,
    git,
    git_show_bytes,
    run,
)
from remote_implementation_stage2_census import (
    RUNTIME_ROOT,
    restore_integration_freeze,
    tracked_worktree_state,
)
from remote_implementation_stage2_preseal import (
    run_stage2_preseal_rehearsal_tool,
)
from remote_implementation_stage2_seal import (
    verify_sealed_plan_bytes,
    verify_stage2_gate1_seal_authority,
)

APPLY_DIR_NAME = "remote-sealed-apply"
APPROVED_PLAN_NAME = "approved-plan.json"
RELEASE_MANIFEST_NAME = "release-manifest.json"
PR_BODY_NAME = "pr-body.md"
VISUAL_QA_NAME = "visual-qa.md"


def _bound_bytes(
    control_commit: str,
    path: str,
    expected_sha256: str,
    *,
    source_repo: Path = ROOT,
    mismatch_code: str,
) -> bytes:
    data = git_show_bytes(control_commit, path, cwd=source_repo)
    if sha256_bytes(data) != expected_sha256:
        raise Stop(mismatch_code)
    return data


def verify_stage2_sealed_apply_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path = ROOT,
) -> dict[str, Any]:
    """Authenticate one exact fresh-verified seal and its complete approval chain."""

    checkpoint_ref = request["stage2_gate1_seal_checkpoint"]
    checkpoint_bytes = _bound_bytes(
        control_commit,
        checkpoint_ref["path"],
        checkpoint_ref["sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_SEALED_APPLY_SEAL_CHECKPOINT_HASH_MISMATCH",
    )
    try:
        manifest = json.loads(checkpoint_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_SEALED_APPLY_SEAL_CHECKPOINT_JSON_INVALID") from exc

    if manifest.get("kind") != "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_CHECKPOINT":
        raise Stop("STAGE2_SEALED_APPLY_SEAL_CHECKPOINT_KIND_MISMATCH")
    if manifest.get("seal_status") != "SEALED":
        raise Stop("STAGE2_SEALED_APPLY_SEAL_NOT_SEALED")
    if manifest.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_SEALED_APPLY_SEAL_SCHOOL_MISMATCH")
    if manifest.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_SEALED_APPLY_SEAL_BRANCH_MISMATCH")
    if manifest.get("target_sha") != request["target_sha"]:
        raise Stop("STAGE2_SEALED_APPLY_SEAL_TARGET_MISMATCH")

    for field, code in (
        ("approved_plan_hash", "APPROVED_PLAN"),
        ("approved_plan_sha256", "APPROVED_PLAN_FILE"),
        ("owner_gate_1_approval_sha256", "OWNER_APPROVAL"),
        ("integration_freeze_sha256", "FREEZE"),
        ("semantic_snapshot_sha256", "SEMANTIC"),
        ("decision_universe_sha256", "DECISION_UNIVERSE"),
        ("recommendation_map_sha256", "MAP"),
        ("filled_review_sha256", "FILLED_REVIEW"),
        ("decision_id_set_sha256", "DECISION_ID_SET"),
    ):
        if manifest.get(field) != request[field]:
            raise Stop("STAGE2_SEALED_APPLY_SEAL_%s_MISMATCH" % code)

    verification_ref = request["stage2_gate1_seal_verification"]
    verification_bytes = _bound_bytes(
        control_commit,
        verification_ref["path"],
        verification_ref["sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_SEALED_APPLY_SEAL_VERIFICATION_HASH_MISMATCH",
    )
    try:
        verification = json.loads(verification_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_SEALED_APPLY_SEAL_VERIFICATION_JSON_INVALID") from exc
    if verification.get("kind") != "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_VERIFICATION":
        raise Stop("STAGE2_SEALED_APPLY_SEAL_VERIFICATION_KIND_MISMATCH")
    if verification.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_SEALED_APPLY_SEAL_VERIFICATION_REQUEST_MISMATCH")
    if verification.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_SEALED_APPLY_SEAL_VERIFICATION_SCHOOL_MISMATCH")
    if verification.get("target_sha") != request["target_sha"]:
        raise Stop("STAGE2_SEALED_APPLY_SEAL_VERIFICATION_TARGET_MISMATCH")
    if verification.get("seal_status") != "SEALED":
        raise Stop("STAGE2_SEALED_APPLY_SEAL_VERIFICATION_NOT_SEALED")
    if verification.get("remote_stage2_gate1_seal_equivalence") != "PASS":
        raise Stop("STAGE2_SEALED_APPLY_SEAL_EQUIVALENCE_NOT_PASS")
    if verification.get("tracked_stage2_mutation") != "NONE":
        raise Stop("STAGE2_SEALED_APPLY_SEAL_TRACKED_MUTATION")
    for field, code in (
        ("approved_plan_hash", "APPROVED_PLAN"),
        ("approved_plan_sha256", "APPROVED_PLAN_FILE"),
        ("owner_gate_1_approval_sha256", "OWNER_APPROVAL"),
        ("integration_freeze_sha256", "FREEZE"),
        ("semantic_snapshot_sha256", "SEMANTIC"),
        ("decision_universe_sha256", "DECISION_UNIVERSE"),
        ("recommendation_map_sha256", "MAP"),
        ("filled_review_sha256", "FILLED_REVIEW"),
        ("decision_id_set_sha256", "DECISION_ID_SET"),
    ):
        if verification.get(field) != request[field]:
            raise Stop("STAGE2_SEALED_APPLY_VERIFICATION_%s_MISMATCH" % code)

    directory = Path(checkpoint_ref["path"]).parent
    seal_request_path = (directory / "request.json").as_posix()
    seal_request_bytes = git_show_bytes(
        control_commit,
        seal_request_path,
        cwd=source_repo,
    )
    if sha256_bytes(seal_request_bytes) != manifest.get("request_sha256"):
        raise Stop("STAGE2_SEALED_APPLY_SOURCE_SEAL_REQUEST_HASH_MISMATCH")
    try:
        seal_request = json.loads(seal_request_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_SEALED_APPLY_SOURCE_SEAL_REQUEST_JSON_INVALID") from exc
    if seal_request.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_SEALED_APPLY_SOURCE_SEAL_REQUEST_ID_MISMATCH")

    seal_authority = verify_stage2_gate1_seal_authority(
        seal_request,
        control_commit,
        source_repo=source_repo,
    )

    approved_plan_path = str(manifest.get("approved_plan_checkpoint_path") or "")
    if not approved_plan_path:
        raise Stop("STAGE2_SEALED_APPLY_APPROVED_PLAN_PATH_MISSING")
    approved_plan_bytes = _bound_bytes(
        control_commit,
        approved_plan_path,
        request["approved_plan_sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_SEALED_APPLY_APPROVED_PLAN_FILE_MISMATCH",
    )

    return {
        "seal_manifest": manifest,
        "seal_checkpoint_bytes": checkpoint_bytes,
        "seal_verification": verification,
        "seal_verification_bytes": verification_bytes,
        "seal_request": seal_request,
        "seal_authority": seal_authority,
        "freeze_bytes": seal_authority["freeze_bytes"],
        "plan_bytes": seal_authority["plan_bytes"],
        "filled_review_bytes": seal_authority["filled_review_bytes"],
        "approved_plan_bytes": approved_plan_bytes,
        "target_tree_sha": manifest.get("target_tree_sha"),
        "expected_changed_path_count": manifest.get(
            "current_main_preseal_changed_path_count"
        ),
        "expected_site_gate_normalized_sha256": manifest.get(
            "current_main_preseal_site_gate_normalized_sha256"
        ),
        "expected_approved_plan_hash_preview": manifest.get(
            "approved_plan_hash_preview"
        ),
        "decision_count": manifest.get("decision_count"),
    }


def add_detached_worktree(
    commit_sha: str,
    school_key: str,
    *,
    source_repo: Path = ROOT,
    prefix: str = "remote-sealed-apply-verify",
) -> Path:
    """Create a clean local worktree at an already authenticated commit."""

    path = Path(tempfile.mkdtemp(prefix="%s-%s-" % (prefix, school_key)))
    shutil.rmtree(path)
    local_branch = "%s/%s-%s" % (prefix, school_key, commit_sha[:12])
    git(
        "worktree",
        "add",
        "-b",
        local_branch,
        str(path),
        commit_sha,
        cwd=source_repo,
    )
    configure_git(path)
    state = tracked_worktree_state(path)
    if state["head_sha"] != commit_sha or state["status"]:
        raise Stop("STAGE2_SEALED_APPLY_WORKTREE_PRECONDITION_FAILED")
    return path


def replay_current_main_preseal(
    repo: Path,
    school_key: str,
    *,
    authority: dict[str, Any],
    diag: Path,
    tool_repo: Path | None = None,
) -> dict[str, Any]:
    """Reconfirm technical readiness on current runtime before tracked mutation."""

    result = run_stage2_preseal_rehearsal_tool(
        repo,
        school_key,
        freeze_bytes=authority["freeze_bytes"],
        plan_bytes=authority["plan_bytes"],
        filled_review_bytes=authority["filled_review_bytes"],
        expected_approved_plan_hash_preview=authority[
            "expected_approved_plan_hash_preview"
        ],
        diag=diag,
        tool_repo=(tool_repo or RUNTIME_ROOT),
    )
    if result["preseal_status"] != "READY_TO_SEAL":
        raise Stop("STAGE2_SEALED_APPLY_CURRENT_MAIN_PRESEAL_NOT_READY")
    if (
        result["approved_plan_hash_preview"]
        != authority["expected_approved_plan_hash_preview"]
    ):
        raise Stop("STAGE2_SEALED_APPLY_CURRENT_MAIN_PREVIEW_MISMATCH")
    if result["changed_path_count"] != authority["expected_changed_path_count"]:
        raise Stop("STAGE2_SEALED_APPLY_CURRENT_MAIN_CHANGED_PATH_COUNT_MISMATCH")
    if (
        result["site_gate_normalized_sha256"]
        != authority["expected_site_gate_normalized_sha256"]
    ):
        raise Stop("STAGE2_SEALED_APPLY_CURRENT_MAIN_SITE_GATE_MISMATCH")
    if result["tracked_mutation_proof"].get("tracked_stage2_mutation") != "NONE":
        raise Stop("STAGE2_SEALED_APPLY_CURRENT_MAIN_PRESEAL_MUTATION")
    return result


def run_sealed_apply_tool(
    repo: Path,
    school_key: str,
    predecessor_sha: str,
    *,
    authority: dict[str, Any],
    diag: Path,
    tool_repo: Path | None = None,
    prepare_commit: bool = True,
) -> dict[str, Any]:
    """Run permanent transactional --apply and optionally prepare one successor commit."""

    before = tracked_worktree_state(repo)
    if before["head_sha"] != predecessor_sha or before["status"]:
        raise Stop("STAGE2_SEALED_APPLY_PRECONDITION_MISMATCH")

    restore_integration_freeze(repo, school_key, authority["freeze_bytes"])
    apply_output = repo / ".onboarding" / school_key / APPLY_DIR_NAME
    apply_output.mkdir(parents=True, exist_ok=True)
    approved_path = apply_output / APPROVED_PLAN_NAME
    approved_path.write_bytes(authority["approved_plan_bytes"])

    seal_summary = verify_sealed_plan_bytes(
        repo,
        plan_bytes=authority["plan_bytes"],
        filled_review_bytes=authority["filled_review_bytes"],
        approved_plan_bytes=authority["approved_plan_bytes"],
    )
    if seal_summary["approved_plan_hash"] != authority["seal_manifest"]["approved_plan_hash"]:
        raise Stop("STAGE2_SEALED_APPLY_APPROVED_PLAN_RECONSTRUCTION_MISMATCH")

    runtime_repo = (tool_repo or RUNTIME_ROOT).resolve()
    onboard_tool = runtime_repo / "tools/onboard_school.py"
    onboarding_plan_tool = runtime_repo / "tools/onboarding_plan.py"
    if not onboard_tool.is_file() or not onboarding_plan_tool.is_file():
        raise Stop("STAGE2_SEALED_APPLY_RUNTIME_TOOL_MISSING")
    runtime_tool_sha256 = {
        "tools/onboard_school.py": sha256_file(onboard_tool),
        "tools/onboarding_plan.py": sha256_file(onboarding_plan_tool),
    }

    cmd = [
        sys.executable,
        str(onboard_tool),
        school_key,
        "--apply",
        "--repo",
        str(repo),
        "--output-dir",
        str(apply_output),
        "--approved-plan",
        authority["seal_manifest"]["approved_plan_hash"],
        "--approved-plan-file",
        str(approved_path),
    ]
    cp = run(cmd, cwd=runtime_repo, check=False)
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "stage2-sealed-apply.log").write_text(
        cp.stdout or "",
        encoding="utf-8",
    )
    if cp.returncode != 0:
        raise Stop("STAGE2_SEALED_APPLY_PERMANENT_COMMAND_FAILED\n" + (cp.stdout or "")[-12000:])
    if "PASS: sealed plan applied transactionally" not in (cp.stdout or ""):
        raise Stop("STAGE2_SEALED_APPLY_SUCCESS_MARKER_MISSING")

    manifest_path = apply_output / RELEASE_MANIFEST_NAME
    if not manifest_path.is_file():
        raise Stop("STAGE2_SEALED_APPLY_RELEASE_MANIFEST_MISSING")
    manifest_bytes = manifest_path.read_bytes()
    try:
        release = json.loads(manifest_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_SEALED_APPLY_RELEASE_MANIFEST_JSON_INVALID") from exc
    if release.get("school_key") != school_key:
        raise Stop("STAGE2_SEALED_APPLY_RELEASE_SCHOOL_MISMATCH")
    if release.get("approved_plan_hash") != authority["seal_manifest"]["approved_plan_hash"]:
        raise Stop("STAGE2_SEALED_APPLY_RELEASE_HASH_MISMATCH")
    if release.get("base_commit") != predecessor_sha:
        raise Stop("STAGE2_SEALED_APPLY_RELEASE_BASE_MISMATCH")

    changed = sorted(str(path) for path in (release.get("changed_paths") or []))
    if not changed:
        raise Stop("STAGE2_SEALED_APPLY_NO_TRACKED_CHANGE")
    if len(changed) != authority["expected_changed_path_count"]:
        raise Stop("STAGE2_SEALED_APPLY_CHANGED_PATH_COUNT_MISMATCH")

    status_paths = sorted(
        line[3:].strip()
        for line in git(
            "status",
            "--porcelain",
            "--untracked-files=all",
            cwd=repo,
        ).stdout.splitlines()
        if line.strip()
    )
    if status_paths != changed:
        raise Stop(
            "STAGE2_SEALED_APPLY_WORKTREE_PATH_MISMATCH expected=%s actual=%s"
            % (changed, status_paths)
        )

    for path in changed:
        git("add", "--", path, cwd=repo)
    staged = sorted(
        line.strip()
        for line in git(
            "diff",
            "--cached",
            "--name-only",
            cwd=repo,
        ).stdout.splitlines()
        if line.strip()
    )
    if staged != changed:
        raise Stop("STAGE2_SEALED_APPLY_STAGED_PATH_MISMATCH")

    if not prepare_commit:
        tree = git("write-tree", cwd=repo).stdout.strip()
        file_hashes = {}
        for path in changed:
            absolute = repo / path
            if absolute.is_file():
                file_hashes[path] = sha256_file(absolute)
            else:
                file_hashes[path] = None
        return {
            "apply_command": [
                "python",
                "tools/onboard_school.py",
                school_key,
                "--apply",
                "--approved-plan",
                authority["seal_manifest"]["approved_plan_hash"],
            ],
            "prepared_tree_sha": tree,
            "prepared_parent_sha": predecessor_sha,
            "changed_paths": changed,
            "changed_file_sha256": file_hashes,
            "release_manifest": release,
            "release_manifest_bytes": manifest_bytes,
            "release_manifest_sha256": sha256_bytes(manifest_bytes),
            "pr_body_bytes": (
                (apply_output / PR_BODY_NAME).read_bytes()
                if (apply_output / PR_BODY_NAME).is_file()
                else b""
            ),
            "visual_qa_bytes": (
                (apply_output / VISUAL_QA_NAME).read_bytes()
                if (apply_output / VISUAL_QA_NAME).is_file()
                else b""
            ),
            "runtime_tool_sha256": runtime_tool_sha256,
        }

    message = "Apply sealed %s onboarding plan" % school_key
    git("commit", "-m", message, cwd=repo)
    prepared = git("rev-parse", "HEAD", cwd=repo).stdout.strip()
    parent = git("rev-parse", "%s^" % prepared, cwd=repo).stdout.strip()
    tree = git("rev-parse", "%s^{tree}" % prepared, cwd=repo).stdout.strip()
    if parent != predecessor_sha:
        raise Stop("STAGE2_SEALED_APPLY_PREPARED_PARENT_MISMATCH")
    commit_changed = sorted(
        line.strip()
        for line in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            prepared,
            cwd=repo,
        ).stdout.splitlines()
        if line.strip()
    )
    if commit_changed != changed:
        raise Stop("STAGE2_SEALED_APPLY_PREPARED_PATH_MISMATCH")

    changed_hashes: dict[str, str | None] = {}
    for path in changed:
        try:
            changed_hashes[path] = sha256_bytes(
                git_show_bytes(prepared, path, cwd=repo)
            )
        except Exception:
            changed_hashes[path] = None

    return {
        "apply_command": [
            "python",
            "tools/onboard_school.py",
            school_key,
            "--apply",
            "--approved-plan",
            authority["seal_manifest"]["approved_plan_hash"],
        ],
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": tree,
        "prepared_parent_sha": parent,
        "commit_message": message,
        "changed_paths": changed,
        "changed_file_sha256": changed_hashes,
        "release_manifest": release,
        "release_manifest_bytes": manifest_bytes,
        "release_manifest_sha256": sha256_bytes(manifest_bytes),
        "pr_body_bytes": (
            (apply_output / PR_BODY_NAME).read_bytes()
            if (apply_output / PR_BODY_NAME).is_file()
            else b""
        ),
        "visual_qa_bytes": (
            (apply_output / VISUAL_QA_NAME).read_bytes()
            if (apply_output / VISUAL_QA_NAME).is_file()
            else b""
        ),
        "runtime_tool_sha256": runtime_tool_sha256,
    }


def verify_prepared_sealed_apply(
    repo: Path,
    *,
    predecessor_sha: str,
    prepared_sha: str,
    changed_paths: list[str],
    changed_file_sha256: dict[str, str | None],
) -> dict[str, Any]:
    parent = git("rev-parse", "%s^" % prepared_sha, cwd=repo).stdout.strip()
    tree = git("rev-parse", "%s^{tree}" % prepared_sha, cwd=repo).stdout.strip()
    if parent != predecessor_sha:
        raise Stop("STAGE2_SEALED_APPLY_VERIFY_PARENT_MISMATCH")
    actual_paths = sorted(
        line.strip()
        for line in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            prepared_sha,
            cwd=repo,
        ).stdout.splitlines()
        if line.strip()
    )
    if actual_paths != sorted(changed_paths):
        raise Stop("STAGE2_SEALED_APPLY_VERIFY_PATH_MISMATCH")
    actual_hashes: dict[str, str | None] = {}
    for path in actual_paths:
        try:
            actual_hashes[path] = sha256_bytes(
                git_show_bytes(prepared_sha, path, cwd=repo)
            )
        except Exception:
            actual_hashes[path] = None
    if actual_hashes != changed_file_sha256:
        raise Stop("STAGE2_SEALED_APPLY_VERIFY_FILE_HASH_MISMATCH")
    return {
        "prepared_parent_sha": parent,
        "prepared_tree_sha": tree,
        "changed_paths": actual_paths,
        "changed_file_sha256": actual_hashes,
    }
