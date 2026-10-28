#!/usr/bin/env python3
"""I/O and permanent-tool invocation helpers for remote Implementation."""
from __future__ import annotations

import base64
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from remote_implementation_control import (
    RemoteImplementationError,
    canonical_json_bytes,
    remote_head,
    sha256_bytes,
    sha256_file,
)

CONTROL_BRANCH = os.environ.get(
    "REMOTE_IMPLEMENTATION_CONTROL_BRANCH",
    "control/remote-implementation",
)
STATE_PATH = Path(".remote-implementation/control-state.json")
REQUEST_PATH = Path(".remote-implementation/request.json")
ROOT = Path(__file__).resolve().parents[1]
INTERNAL_PREFIX = "[remote-implementation-internal]"
REQUIRED_PACKAGE_FILES = [
    "conferences.csv",
    "notes.md",
    "opponents.csv",
    "source-games.csv",
    "source-notes.md",
    "venues.csv",
]
STAGE2_TRANSITIVE_RUNTIME_TOOL_PATHS = (
    "tools/onboarding_hardening.py",
    "tools/reconciliation_trace.py",
    "tools/onboard_school.py",
    "tools/onboarding_plan.py",
)
PHASE0_GLOBAL_PATHS = {
    "data/reference/programs.csv",
    "data/reference/program-top-level-scope.csv",
    "data/reference/venues.csv",
    "data/reference/venue-names.csv",
    "data/reference/conferences.csv",
}


class Stop(RemoteImplementationError):
    pass


def run(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    text: bool = True,
) -> subprocess.CompletedProcess:
    cp = subprocess.run(
        cmd,
        cwd=cwd,
        text=text,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if check and cp.returncode != 0:
        output = cp.stdout if text else cp.stdout.decode("utf-8", errors="replace")
        raise Stop("command failed (%s): %s\n%s" % (cp.returncode, " ".join(cmd), output))
    return cp


def git(*args: str, cwd: Path | None = None, check: bool = True, text: bool = True):
    return run(["git", *args], cwd=cwd, check=check, text=text)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(value))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def configure_git(cwd: Path | None = None) -> None:
    git("config", "user.name", "github-actions[bot]", cwd=cwd)
    git(
        "config",
        "user.email",
        "41898282+github-actions[bot]@users.noreply.github.com",
        cwd=cwd,
    )


def git_show_bytes(commit: str, path: str, *, cwd: Path | None = None) -> bytes:
    return git("show", "%s:%s" % (commit, path), cwd=cwd, text=False).stdout


def git_show_json(commit: str, path: str, *, cwd: Path | None = None) -> dict[str, Any]:
    return json.loads(git_show_bytes(commit, path, cwd=cwd))


def push_control(expected_remote: str) -> str:
    new_head = git("rev-parse", "HEAD").stdout.strip()
    cp = git(
        "push",
        "--force-with-lease=refs/heads/%s:%s" % (CONTROL_BRANCH, expected_remote),
        "origin",
        "%s:refs/heads/%s" % (new_head, CONTROL_BRANCH),
        check=False,
    )
    if cp.returncode != 0:
        raise Stop("CONTROL_REF_CAS_FAILED\n" + cp.stdout)
    return new_head


def commit_control(expected_remote: str, message: str, paths: list[Path | str]) -> str:
    for path in paths:
        git("add", "--", str(path))
    git("commit", "-m", INTERNAL_PREFIX + " " + message)
    return push_control(expected_remote)


def fetch_operational_refs(target_branch: str | None = None) -> tuple[str, str]:
    args = [
        "fetch",
        "--no-tags",
        "origin",
        "+refs/heads/main:refs/remotes/origin/main",
        "+refs/heads/%s:refs/remotes/origin/remote-control" % CONTROL_BRANCH,
    ]
    if target_branch and remote_head(ROOT, target_branch):
        args.append(
            "+refs/heads/%s:refs/remotes/origin/remote-target" % target_branch
        )
    git(*args)
    return (
        git("rev-parse", "refs/remotes/origin/main").stdout.strip(),
        git("rev-parse", "refs/remotes/origin/remote-control").stdout.strip(),
    )


def assert_protected_main_unchanged(expected_sha: str) -> None:
    git(
        "fetch",
        "--no-tags",
        "origin",
        "+refs/heads/main:refs/remotes/origin/main",
    )
    actual = git(
        "rev-parse",
        "refs/remotes/origin/main",
    ).stdout.strip()
    if actual != expected_sha:
        raise Stop(
            "PROTECTED_MAIN_CHANGED_DURING_REMOTE_OPERATION expected=%s actual=%s"
            % (expected_sha, actual)
        )


def add_exact_protected_main_runtime_worktree(
    live_main: str,
    *,
    source_repo: Path = ROOT,
) -> Path:
    """Create a clean detached executable runtime at one authenticated main SHA."""

    fetched_main = git(
        "rev-parse",
        "refs/remotes/origin/main",
        cwd=source_repo,
    ).stdout.strip()
    if fetched_main != live_main:
        raise Stop(
            "RUNTIME_PROTECTED_MAIN_REF_MISMATCH expected=%s actual=%s"
            % (live_main, fetched_main)
        )

    path = Path(tempfile.mkdtemp(prefix="remote-main-runtime-"))
    shutil.rmtree(path)
    git("worktree", "add", "--detach", str(path), live_main, cwd=source_repo)
    configure_git(path)

    head = git("rev-parse", "HEAD", cwd=path).stdout.strip()
    if head != live_main:
        raise Stop(
            "RUNTIME_WORKTREE_HEAD_MISMATCH expected=%s actual=%s"
            % (live_main, head)
        )
    status = git(
        "status",
        "--porcelain",
        "--untracked-files=all",
        cwd=path,
    ).stdout
    if status:
        raise Stop("RUNTIME_WORKTREE_NOT_CLEAN")
    return path


def runtime_tool_sha256_manifest(
    runtime_repo: Path,
    *,
    extra_paths: tuple[str, ...] = (),
) -> dict[str, str]:
    """Hash the materially transitive Stage 2 runtime used for reconciliation."""

    paths = sorted(set(STAGE2_TRANSITIVE_RUNTIME_TOOL_PATHS + extra_paths))
    result: dict[str, str] = {}
    for relative in paths:
        tool = runtime_repo / relative
        if not tool.is_file():
            raise Stop("RUNTIME_TRANSITIVE_TOOL_MISSING:%s" % relative)
        result[relative] = sha256_file(tool)
    return result


def materialize_research_checkpoint(request: dict[str, Any], out_path: Path) -> dict[str, Any]:
    checkpoint = request["research_checkpoint"]
    transport = checkpoint["transport"]
    commit_sha = transport["commit_sha"]
    git("fetch", "--no-tags", "origin", commit_sha)
    prefix = transport["path_prefix"]
    parts = sorted(
        path
        for path in git("ls-tree", "-r", "--name-only", commit_sha).stdout.splitlines()
        if path.startswith(prefix)
    )
    if len(parts) != int(transport["part_count"]):
        raise Stop(
            "RESEARCH_CHECKPOINT_PART_COUNT_MISMATCH expected=%s actual=%s"
            % (transport["part_count"], len(parts))
        )
    encoded = b"".join(git_show_bytes(commit_sha, path) for path in parts)
    try:
        data = base64.b64decode(encoded, validate=True)
    except ValueError as exc:
        raise Stop("RESEARCH_CHECKPOINT_BASE64_INVALID: %s" % exc) from exc
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    actual = sha256_file(out_path)
    if actual != checkpoint["sha256"]:
        raise Stop(
            "RESEARCH_CHECKPOINT_SHA_MISMATCH expected=%s actual=%s"
            % (checkpoint["sha256"], actual)
        )
    with zipfile.ZipFile(out_path) as archive:
        names = sorted(archive.namelist())
        if names != sorted(REQUIRED_PACKAGE_FILES):
            raise Stop("RESEARCH_CHECKPOINT_MEMBER_SET_MISMATCH: %s" % names)
        member_hashes = {
            name: sha256_bytes(archive.read(name))
            for name in REQUIRED_PACKAGE_FILES
        }
        rows = list(
            csv.DictReader(
                io.StringIO(archive.read("source-games.csv").decode("utf-8-sig"))
            )
        )
    return {
        "zip_sha256": actual,
        "member_sha256": member_hashes,
        "source_game_count": len(rows),
    }


def materialize_payload(
    request_commit: str,
    payload: dict[str, Any] | None,
    out_path: Path,
) -> Path | None:
    if payload is None:
        return None
    data = git_show_bytes(request_commit, payload["path"])
    actual = sha256_bytes(data)
    if actual != payload["sha256"]:
        raise Stop(
            "REQUEST_PAYLOAD_HASH_MISMATCH path=%s expected=%s actual=%s"
            % (payload["path"], payload["sha256"], actual)
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(data)
    return out_path


def add_isolated_worktree(live_main: str, school_key: str) -> Path:
    path = Path(tempfile.mkdtemp(prefix="remote-implementation-%s-" % school_key))
    shutil.rmtree(path)
    git("worktree", "add", "-b", "data/%s-onboarding" % school_key, str(path), live_main, cwd=ROOT)
    configure_git(path)
    if git("rev-parse", "HEAD", cwd=path).stdout.strip() != live_main:
        raise Stop("WORKTREE_MAIN_MISMATCH")
    if git("rev-parse", "origin/main", cwd=path).stdout.strip() != live_main:
        raise Stop("WORKTREE_ORIGIN_MAIN_MISMATCH")
    return path


def stage1_command(
    worktree: Path,
    request: dict[str, Any],
    package: Path,
    venue_spec: Path | None,
    conference_spec: Path | None,
) -> list[str]:
    cmd = [
        sys.executable,
        str(worktree / "tools/implementation_stage1_inventory.py"),
        request["school_key"],
        str(package),
        "--expected-sha256",
        request["research_checkpoint"]["sha256"],
        "--research-base",
        request["research_checkpoint"]["research_base_sha"],
        "--repo",
        str(worktree),
    ]
    if venue_spec:
        cmd += ["--venue-reconciliation", str(venue_spec)]
    if conference_spec:
        cmd += ["--conference-reconciliation", str(conference_spec)]
    return cmd


def phase0_command(
    worktree: Path,
    request: dict[str, Any],
    package: Path,
    venue_spec: Path | None,
    conference_spec: Path | None,
) -> list[str]:
    scope = request["history_scope"]
    cmd = [
        sys.executable,
        str(worktree / "tools/stage_research_portfolio.py"),
        request["school_key"],
        str(package),
        "--expected-sha256",
        request["research_checkpoint"]["sha256"],
        "--research-base",
        request["research_checkpoint"]["research_base_sha"],
        "--history-start-season",
        scope["start_season"],
        "--history-scope-basis",
        scope["basis"],
        "--history-scope-intervals",
        scope["intervals"],
        "--history-scope-notes",
        scope["notes"],
        "--repo",
        str(worktree),
    ]
    if venue_spec:
        cmd += ["--venue-reconciliation", str(venue_spec)]
    if conference_spec:
        cmd += ["--conference-reconciliation", str(conference_spec)]
    return cmd + ["--apply", "--commit"]


def run_stage1_tool(
    worktree: Path,
    request: dict[str, Any],
    package: Path,
    venue_spec: Path | None,
    conference_spec: Path | None,
    diag: Path,
) -> tuple[dict[str, Any], Path]:
    cp = run(
        stage1_command(worktree, request, package, venue_spec, conference_spec),
        cwd=worktree,
        check=False,
    )
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "stage1.log").write_text(cp.stdout, encoding="utf-8")
    if cp.returncode != 0:
        raise Stop("PERMANENT_STAGE1_COMMAND_FAILED\n" + cp.stdout[-8000:])
    report_path = (
        worktree
        / ".onboarding"
        / request["school_key"]
        / "stage1-reconciliation.json"
    )
    if not report_path.is_file():
        raise Stop("PERMANENT_STAGE1_ARTIFACT_MISSING")
    report = read_json(report_path)
    if report.get("integration_base_sha") != request["expected_protected_main_sha"]:
        raise Stop("STAGE1_INTEGRATION_BASE_MISMATCH")
    if report.get("origin_main_sha") != request["expected_protected_main_sha"]:
        raise Stop("STAGE1_ORIGIN_MAIN_MISMATCH")
    if report.get("research_zip_sha256") != request["research_checkpoint"]["sha256"]:
        raise Stop("STAGE1_RESEARCH_CHECKPOINT_MISMATCH")
    return report, report_path


def validate_stage1_pass(report: dict[str, Any]) -> None:
    if (
        report.get("status") != "PASS"
        or int(report.get("blocker_count", -1)) != 0
        or int(report.get("ambiguous_stop_count", -1)) != 0
        or int(report.get("maintenance_required_count", -1)) != 0
    ):
        raise Stop(
            "FRESH_STAGE1_NOT_PASS\n"
            + json.dumps(
                {
                    "status": report.get("status"),
                    "blockers": report.get("blocker_count"),
                    "ambiguous": report.get("ambiguous_stop_count"),
                    "maintenance": report.get("maintenance_required_count"),
                },
                indent=2,
            )
        )


def phase0_allowed_paths(school_key: str) -> set[str]:
    return PHASE0_GLOBAL_PATHS | {
        "schools/%s/%s" % (school_key, name)
        for name in REQUIRED_PACKAGE_FILES
    }


def commit_file_hashes(worktree: Path, commit: str, paths: list[str]) -> dict[str, str]:
    return {
        path: sha256_bytes(git_show_bytes(commit, path, cwd=worktree))
        for path in paths
    }
