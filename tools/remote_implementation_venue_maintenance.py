#!/usr/bin/env python3
"""Permanent-tool wrapper for guarded remote venue-identity maintenance."""
from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from remote_implementation_control import sha256_bytes
from remote_implementation_io import (
    Stop,
    configure_git,
    git,
    git_show_bytes,
    run,
)

SPEC_PATH_RE = re.compile(
    r"^data/reconciliation/venue-identity-maintenance/"
    r"([a-z0-9][a-z0-9._-]{1,127})\.json$"
)

FIXED_MUTATION_PATHS = {
    "data/reference/venues.csv",
    "data/reference/venue-names.csv",
    "data/canonical/games.csv",
    "data/evidence/game-assertions.csv",
    "data/evidence/ncaa-tournament-sites.csv",
}


def validate_repository_spec_path(school_key: str, path: str) -> str:
    value = str(path or "").strip()
    match = SPEC_PATH_RE.fullmatch(value)
    stem = match.group(1) if match else ""
    if not match or not (
        stem == school_key
        or stem.startswith(school_key + "-")
        or stem.startswith(school_key + ".")
        or stem.startswith(school_key + "_")
    ):
        raise Stop("VENUE_MAINTENANCE_REPOSITORY_SPEC_PATH_INVALID")
    return value


def add_maintenance_worktree(
    repo: Path,
    base_sha: str,
    request_id: str,
    *,
    label: str,
) -> Path:
    worktree = Path(
        tempfile.mkdtemp(prefix="remote-venue-maintenance-%s-" % label)
    )
    shutil.rmtree(worktree)
    branch = "remote-venue-maintenance/%s-%s" % (
        re.sub(r"[^a-zA-Z0-9._-]+", "-", request_id)[:80],
        label,
    )
    git("worktree", "add", "-b", branch, str(worktree), base_sha, cwd=repo)
    configure_git(worktree)
    if git("rev-parse", "HEAD", cwd=worktree).stdout.strip() != base_sha:
        raise Stop("VENUE_MAINTENANCE_WORKTREE_BASE_MISMATCH")
    return worktree


def _plan_school_paths(plan: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    for merge in plan.get("merges") or []:
        for item in merge.get("school_files") or []:
            path = str(item.get("path") or "").strip()
            if path:
                paths.add(path)
    return paths


def _validate_changed_paths(
    changed: list[str],
    plan: dict[str, Any],
    repository_spec_path: str,
) -> list[str]:
    allowed = FIXED_MUTATION_PATHS | _plan_school_paths(plan) | {
        repository_spec_path
    }
    unexpected = [
        path
        for path in changed
        if path not in allowed
        and not (
            path.startswith("site/data/")
            and path.endswith(".json")
        )
    ]
    if unexpected:
        raise Stop(
            "VENUE_MAINTENANCE_DIFF_OUTSIDE_CONTRACT:"
            + ",".join(sorted(unexpected))
        )
    if repository_spec_path not in changed:
        raise Stop("VENUE_MAINTENANCE_SPEC_NOT_COMMITTED")
    if "data/reference/venues.csv" not in changed:
        raise Stop("VENUE_MAINTENANCE_VENUE_REGISTRY_UNCHANGED")
    if "data/reference/venue-names.csv" not in changed:
        raise Stop("VENUE_MAINTENANCE_NAME_REGISTRY_UNCHANGED")
    return sorted(allowed)


def _parse_apply_result(output: str) -> dict[str, Any]:
    for line in reversed(output.splitlines()):
        if line.startswith("PASS: "):
            try:
                value = json.loads(line[len("PASS: "):])
            except json.JSONDecodeError as exc:
                raise Stop(
                    "VENUE_MAINTENANCE_APPLY_RESULT_INVALID"
                ) from exc
            if not isinstance(value, dict):
                raise Stop("VENUE_MAINTENANCE_APPLY_RESULT_INVALID")
            return value
    raise Stop("VENUE_MAINTENANCE_APPLY_RESULT_MISSING")


def prepare_venue_maintenance(
    *,
    repo: Path,
    base_sha: str,
    request_id: str,
    school_key: str,
    spec_bytes: bytes,
    repository_spec_path: str,
    expected_plan_sha256: str,
    diag: Path,
    label: str,
) -> dict[str, Any]:
    repository_spec_path = validate_repository_spec_path(
        school_key,
        repository_spec_path,
    )
    worktree = add_maintenance_worktree(
        repo,
        base_sha,
        request_id,
        label=label,
    )
    spec_path = worktree / repository_spec_path
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_bytes(spec_bytes)

    diag.mkdir(parents=True, exist_ok=True)
    plan_path = Path(
        tempfile.mkstemp(
            prefix="venue-maintenance-plan-",
            suffix=".json",
        )[1]
    )
    plan_cp = run(
        [
            sys.executable,
            "tools/venue_identity_transaction.py",
            "plan",
            repository_spec_path,
            "--output",
            str(plan_path),
        ],
        cwd=worktree,
        check=False,
    )
    (diag / ("venue-maintenance-plan-%s.log" % label)).write_text(
        plan_cp.stdout,
        encoding="utf-8",
    )
    if plan_cp.returncode != 0 or not plan_path.is_file():
        raise Stop(
            "VENUE_MAINTENANCE_PLAN_FAILED\n"
            + plan_cp.stdout[-10000:]
        )
    plan_bytes = plan_path.read_bytes()
    plan = json.loads(plan_bytes)
    if plan.get("git_head") != base_sha:
        raise Stop("VENUE_MAINTENANCE_PLAN_BASE_MISMATCH")
    if plan.get("blockers"):
        raise Stop(
            "VENUE_MAINTENANCE_PLAN_BLOCKED:"
            + "|".join(str(item) for item in plan["blockers"][:8])
        )
    if plan.get("plan_sha256") != expected_plan_sha256:
        raise Stop(
            "VENUE_MAINTENANCE_PLAN_HASH_MISMATCH expected=%s actual=%s"
            % (expected_plan_sha256, plan.get("plan_sha256"))
        )

    apply_cp = run(
        [
            sys.executable,
            "tools/venue_identity_transaction.py",
            "apply",
            repository_spec_path,
            "--expected-plan-sha256",
            expected_plan_sha256,
            "--apply",
        ],
        cwd=worktree,
        check=False,
    )
    (diag / ("venue-maintenance-apply-%s.log" % label)).write_text(
        apply_cp.stdout,
        encoding="utf-8",
    )
    if apply_cp.returncode != 0:
        raise Stop(
            "VENUE_MAINTENANCE_APPLY_FAILED\n"
            + apply_cp.stdout[-12000:]
        )
    apply_result = _parse_apply_result(apply_cp.stdout)

    freshness_cp = run(
        [sys.executable, "tools/check_site_data_freshness.py"],
        cwd=worktree,
        check=False,
    )
    (diag / ("venue-maintenance-freshness-%s.log" % label)).write_text(
        freshness_cp.stdout,
        encoding="utf-8",
    )
    if freshness_cp.returncode != 0:
        raise Stop("VENUE_MAINTENANCE_SITE_DATA_NOT_FRESH")

    git("add", "-A", cwd=worktree)
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
    allowed = _validate_changed_paths(
        changed,
        plan,
        repository_spec_path,
    )
    if not changed:
        raise Stop("VENUE_MAINTENANCE_EMPTY_DIFF")

    name_status = git(
        "diff",
        "--cached",
        "--name-status",
        cwd=worktree,
    ).stdout.splitlines()
    deleted_paths = sorted(
        line.split("\t", 1)[1]
        for line in name_status
        if line.startswith("D\t")
    )

    commit_message = "Reconcile shared venue identities for %s" % school_key
    git("commit", "-m", commit_message, cwd=worktree)
    prepared = git("rev-parse", "HEAD", cwd=worktree).stdout.strip()
    parent = git("rev-parse", "%s^" % prepared, cwd=worktree).stdout.strip()
    tree = git("rev-parse", "%s^{tree}" % prepared, cwd=worktree).stdout.strip()
    if parent != base_sha:
        raise Stop("VENUE_MAINTENANCE_PREPARED_PARENT_MISMATCH")

    changed_file_sha256 = {
        path: sha256_bytes(git_show_bytes(prepared, path, cwd=worktree))
        for path in changed
        if path not in deleted_paths
    }

    return {
        "worktree": worktree,
        "plan": plan,
        "plan_bytes": plan_bytes,
        "plan_sha256": plan["plan_sha256"],
        "apply_result": apply_result,
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": tree,
        "prepared_parent_sha": parent,
        "changed_paths": changed,
        "deleted_paths": deleted_paths,
        "changed_file_sha256": changed_file_sha256,
        "allowed_paths": allowed,
        "repository_spec_path": repository_spec_path,
        "repository_spec_sha256": sha256_bytes(spec_bytes),
        "repository_validation": "PASS",
        "site_data_freshness": "PASS",
        "commit_message": commit_message,
    }
