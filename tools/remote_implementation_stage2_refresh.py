#!/usr/bin/env python3
"""Guarded current-main refresh for an in-flight Stage 2 onboarding branch.

The operation is intentionally narrow. It may merge a newer protected-main commit
into an already-authorized onboarding target only when the target-only and
main-only changed-path populations are disjoint. Any overlapping path requires
ordinary Control Center reconciliation rather than an automatic merge.
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from integration_freeze_guard import semantic_drift_report
from remote_implementation_control import sha256_bytes
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
from remote_implementation_stage2_census import (
    add_existing_onboarding_worktree,
    restore_integration_freeze,
    verify_phase0_authority,
)

SUCCESSOR_KIND = "REMOTE_IMPLEMENTATION_STAGE2_CURRENT_MAIN_REFRESH_SUCCESSOR"
VERIFICATION_KIND = "REMOTE_IMPLEMENTATION_STAGE2_CURRENT_MAIN_REFRESH_VERIFICATION"


def _paths_between(repo: Path, base: str, head: str) -> list[str]:
    return sorted(
        line.strip()
        for line in git(
            "diff", "--name-only", base, head, cwd=repo
        ).stdout.splitlines()
        if line.strip()
    )


def _path_hash(commit: str, path: str, *, repo: Path) -> str:
    return sha256_bytes(git_show_bytes(commit, path, cwd=repo))


def verify_current_main_refresh_authority(
    request: dict[str, Any],
    control_commit: str,
    live_main: str,
    *,
    source_repo: Path = ROOT,
) -> dict[str, Any]:
    school = request["school_key"]
    branch = request["target_branch"]
    target = request["target_sha"]
    if branch != f"data/{school}-onboarding":
        raise Stop("STAGE2_REFRESH_TARGET_BRANCH_INVALID")
    if remote_head(source_repo, branch) != target:
        raise Stop("STAGE2_REFRESH_TARGET_HEAD_MISMATCH")

    prior = verify_phase0_authority(
        request,
        control_commit,
        source_repo=source_repo,
    )
    if prior["target_authority_kind"] not in {
        "PHASE0_SUCCESSOR",
        "STAGE2_OPPONENT_DISPLAY_SUCCESSOR",
        "STAGE2_CURRENT_MAIN_REFRESH_SUCCESSOR",
    }:
        raise Stop("STAGE2_REFRESH_PRIOR_AUTHORITY_KIND_UNSUPPORTED")

    git(
        "fetch",
        "--no-tags",
        "origin",
        f"+refs/heads/{branch}:refs/remotes/origin/remote-stage2-refresh-target",
        cwd=source_repo,
    )
    fetched = git(
        "rev-parse",
        "refs/remotes/origin/remote-stage2-refresh-target",
        cwd=source_repo,
    ).stdout.strip()
    if fetched != target:
        raise Stop("STAGE2_REFRESH_TARGET_FETCH_MISMATCH")

    merge_base = git(
        "merge-base", target, live_main, cwd=source_repo
    ).stdout.strip()
    if not merge_base:
        raise Stop("STAGE2_REFRESH_MERGE_BASE_MISSING")

    target_paths = _paths_between(source_repo, merge_base, target)
    main_paths = _paths_between(source_repo, merge_base, live_main)
    overlap = sorted(set(target_paths) & set(main_paths))
    if overlap:
        raise Stop(
            "STAGE2_REFRESH_PATH_OVERLAP_REQUIRES_RECONCILIATION:"
            + ",".join(overlap)
        )
    if not main_paths:
        raise Stop("STAGE2_REFRESH_MAIN_HAS_NO_NEW_PATHS")

    school_prefix = f"schools/{school}/"
    main_school_paths = [p for p in main_paths if p.startswith(school_prefix)]
    if main_school_paths:
        raise Stop(
            "STAGE2_REFRESH_CURRENT_MAIN_TOUCHED_TARGET_SCHOOL:"
            + ",".join(main_school_paths)
        )

    origin_main = prior.get("phase0_protected_main_sha")
    if not origin_main:
        raise Stop("STAGE2_REFRESH_PRIOR_MAIN_MISSING")
    if git(
        "merge-base", "--is-ancestor", origin_main, live_main,
        cwd=source_repo, check=False,
    ).returncode != 0:
        raise Stop("STAGE2_REFRESH_PRIOR_MAIN_NOT_ANCESTOR")

    package_hashes = {
        name: _path_hash(
            target,
            f"schools/{school}/{name}",
            repo=source_repo,
        )
        for name in REQUIRED_PACKAGE_FILES
    }
    return {
        "prior_authority": prior,
        "merge_base_sha": merge_base,
        "target_changed_paths": target_paths,
        "main_changed_paths": main_paths,
        "overlap_paths": overlap,
        "package_member_sha256": package_hashes,
    }


def prepare_current_main_refresh(
    request: dict[str, Any],
    authority: dict[str, Any],
    live_main: str,
    *,
    source_repo: Path = ROOT,
    diag: Path,
) -> dict[str, Any]:
    school = request["school_key"]
    branch = request["target_branch"]
    target = request["target_sha"]

    worktree = add_existing_onboarding_worktree(
        branch,
        target,
        school,
        source_repo=source_repo,
    )
    before_package = dict(authority["package_member_sha256"])
    restore_integration_freeze(
        worktree,
        school,
        authority["prior_authority"]["freeze_bytes"],
    )

    cp = git(
        "merge",
        "--no-ff",
        "--no-edit",
        live_main,
        cwd=worktree,
        check=False,
    )
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "stage2-current-main-refresh-merge.log").write_text(
        cp.stdout or "",
        encoding="utf-8",
    )
    if cp.returncode != 0:
        raise Stop(
            "STAGE2_REFRESH_MERGE_FAILED\n" + (cp.stdout or "")[-12000:]
        )

    prepared = git("rev-parse", "HEAD", cwd=worktree).stdout.strip()
    parents = git(
        "rev-list", "--parents", "-n", "1", prepared, cwd=worktree
    ).stdout.strip().split()
    if len(parents) != 3 or parents[1:] != [target, live_main]:
        raise Stop("STAGE2_REFRESH_PREPARED_PARENTS_MISMATCH")
    tree = git(
        "rev-parse", f"{prepared}^{{tree}}", cwd=worktree
    ).stdout.strip()

    changed = _paths_between(worktree, target, prepared)
    if changed != authority["main_changed_paths"]:
        raise Stop("STAGE2_REFRESH_CHANGED_PATH_SET_MISMATCH")

    changed_hashes = {
        path: _path_hash(prepared, path, repo=worktree)
        for path in changed
        if git(
            "cat-file", "-e", f"{prepared}:{path}",
            cwd=worktree, check=False,
        ).returncode == 0
    }
    deleted = [
        path for path in changed
        if path not in changed_hashes
    ]

    preserved_target_hashes: dict[str, str] = {}
    for path in authority["target_changed_paths"]:
        old_exists = git(
            "cat-file", "-e", f"{target}:{path}",
            cwd=worktree, check=False,
        ).returncode == 0
        new_exists = git(
            "cat-file", "-e", f"{prepared}:{path}",
            cwd=worktree, check=False,
        ).returncode == 0
        if old_exists != new_exists:
            raise Stop("STAGE2_REFRESH_TARGET_PATH_PRESERVATION_MISMATCH:" + path)
        if old_exists:
            old_hash = _path_hash(target, path, repo=worktree)
            new_hash = _path_hash(prepared, path, repo=worktree)
            if old_hash != new_hash:
                raise Stop("STAGE2_REFRESH_TARGET_PATH_CHANGED:" + path)
            preserved_target_hashes[path] = old_hash

    after_package = {
        name: _path_hash(
            prepared,
            f"schools/{school}/{name}",
            repo=worktree,
        )
        for name in REQUIRED_PACKAGE_FILES
    }
    if after_package != before_package:
        raise Stop("STAGE2_REFRESH_SCHOOL_PACKAGE_CHANGED")

    drift = semantic_drift_report(worktree, school)
    if drift.get("status") != "PASS" or drift.get("changes"):
        raise Stop("STAGE2_REFRESH_SEMANTIC_DRIFT")

    validation = run(
        [sys.executable, "tools/validate_data.py"],
        cwd=worktree,
        check=False,
    )
    (diag / "stage2-current-main-refresh-validate-data.log").write_text(
        validation.stdout or "",
        encoding="utf-8",
    )
    if validation.returncode != 0:
        raise Stop("STAGE2_REFRESH_REPOSITORY_VALIDATION_FAILED")

    proof = {
        "schema_version": 1,
        "school_key": school,
        "target_branch": branch,
        "expected_target_predecessor_sha": target,
        "protected_main_sha": live_main,
        "merge_base_sha": authority["merge_base_sha"],
        "target_changed_paths": authority["target_changed_paths"],
        "main_changed_paths": authority["main_changed_paths"],
        "overlap_paths": [],
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": tree,
        "prepared_parents": [target, live_main],
        "changed_paths": changed,
        "changed_file_sha256": changed_hashes,
        "deleted_paths": deleted,
        "preserved_target_file_sha256": preserved_target_hashes,
        "package_member_sha256": after_package,
        "semantic_snapshot_sha256": request["semantic_snapshot_sha256"],
        "semantic_drift": "PASS",
        "repository_validation": "PASS",
    }
    return {
        "worktree": worktree,
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": tree,
        "prepared_parents": [target, live_main],
        "changed_paths": changed,
        "changed_file_sha256": changed_hashes,
        "deleted_paths": deleted,
        "proof": proof,
    }


def reconstruct_refresh_tree(
    *,
    predecessor_sha: str,
    protected_main_sha: str,
    school_key: str,
    source_repo: Path = ROOT,
) -> str:
    path = Path(tempfile.mkdtemp(prefix="remote-stage2-refresh-fresh-"))
    shutil.rmtree(path)
    git(
        "worktree", "add", "-b",
        f"remote-stage2-refresh-verify/{school_key}-{predecessor_sha[:12]}",
        str(path), predecessor_sha,
        cwd=source_repo,
    )
    configure_git(path)
    cp = git(
        "merge", "--no-ff", "--no-commit", protected_main_sha,
        cwd=path, check=False,
    )
    if cp.returncode != 0:
        raise Stop("STAGE2_REFRESH_FRESH_MERGE_FAILED")
    return git("write-tree", cwd=path).stdout.strip()
