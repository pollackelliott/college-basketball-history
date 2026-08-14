#!/usr/bin/env python3
"""Release one transactionally applied school with one visual approval gate.

Prepare (commit, push, PR, CI, preview URL):
    python tools/release_school.py <school> --prepare

After the owner visually approves that exact preview:
    python tools/release_school.py <school> --merge --preview-approved

The command intentionally delegates hosting to the repository's GitHub/Vercel
integration.  It never runs a manual Vercel deployment.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

from onboard_school import run_gates, whitespace_errors
from onboarding_plan import WorkflowError, read_csv


PRODUCTION_BASE = "https://college-basketball-history.vercel.app"


def run(
    command: list[str],
    *,
    cwd: Path,
    label: str,
    echo: bool = True,
) -> str:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=environment,
    )
    output = result.stdout.rstrip()
    if echo and output:
        print(output)
    if result.returncode:
        raise WorkflowError(
            f"{label} failed with exit code {result.returncode}"
            + (f"\n{output}" if not echo and output else "")
        )
    return output


def git(repo: Path, *args: str, echo: bool = False) -> str:
    return run(["git", *args], cwd=repo, label="git " + " ".join(args), echo=echo)


def gh(repo: Path, *args: str, echo: bool = False) -> str:
    if not shutil.which("gh"):
        raise WorkflowError(
            "GitHub CLI (gh) is required. Run this release command in the project Codespace, "
            "where repository authentication is already configured."
        )
    return run(["gh", *args], cwd=repo, label="gh " + " ".join(args), echo=echo)


def gh_json(repo: Path, *args: str) -> Any:
    output = gh(repo, *args, echo=False)
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"GitHub returned non-JSON output for {' '.join(args)}") from exc


def repository_slug(repo: Path) -> str:
    remote = git(repo, "remote", "get-url", "origin").strip()
    match = re.search(r"(?:github\.com[:/])([^/]+/[^/]+?)(?:\.git)?$", remote)
    if not match:
        raise WorkflowError(f"cannot derive GitHub repository from origin URL {remote!r}")
    return match.group(1)


def program_display_name(repo: Path, school_key: str) -> str:
    rows = read_csv(repo / "data/reference/programs.csv")
    row = next((value for value in rows if value.get("program_key") == school_key), None)
    if row is None:
        raise WorkflowError(f"program registry has no row for {school_key}")
    return row.get("display_name") or row.get("program_name") or school_key


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"cannot read {path}: {exc}") from exc


def output_dir(repo: Path, school_key: str, supplied: Path | None) -> Path:
    return supplied.resolve() if supplied else repo / ".onboarding" / school_key


def verify_change_boundary(repo: Path, manifest: dict[str, Any]) -> list[str]:
    if git(repo, "rev-parse", "HEAD").strip() != manifest.get("base_commit"):
        raise WorkflowError(
            "HEAD changed after transactional apply; rerun preflight/approval/apply on the new base"
        )
    expected = set(manifest.get("changed_paths", []))
    tracked = {
        line.strip()
        for line in git(repo, "diff", "--name-only", "HEAD").splitlines()
        if line.strip()
    }
    untracked = {
        line.strip()
        for line in git(
            repo,
            "ls-files",
            "--others",
            "--exclude-standard",
        ).splitlines()
        if line.strip()
    }
    actual = tracked | untracked
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        details = []
        if missing:
            details.append("missing expected changes: " + ", ".join(missing))
        if extra:
            details.append("unapproved changes: " + ", ".join(extra))
        raise WorkflowError("release boundary mismatch; " + "; ".join(details))
    bad = whitespace_errors(repo, sorted(actual))
    if bad:
        raise WorkflowError("trailing whitespace before release: " + ", ".join(bad[:20]))
    return sorted(actual)


def stage_exact_paths(repo: Path, paths: list[str]) -> None:
    for path in paths:
        run(["git", "add", "--", path], cwd=repo, label=f"stage {path}", echo=False)
    staged = {
        line.strip()
        for line in git(repo, "diff", "--cached", "--name-only").splitlines()
        if line.strip()
    }
    if staged != set(paths):
        raise WorkflowError("staged file set does not exactly match the sealed release manifest")
    unstaged = git(repo, "diff", "--name-only").strip()
    untracked = git(repo, "ls-files", "--others", "--exclude-standard").strip()
    if unstaged or untracked:
        raise WorkflowError("unstaged or untracked files remain after exact staging")


def pr_for_branch(repo: Path, branch: str) -> dict[str, Any] | None:
    result = subprocess.run(
        [
            "gh",
            "pr",
            "view",
            branch,
            "--json",
            "number,url,state,headRefOid,headRefName,baseRefName",
        ],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode:
        return None
    return json.loads(result.stdout)


def create_or_reuse_pr(
    repo: Path,
    branch: str,
    school_key: str,
    body_path: Path,
) -> dict[str, Any]:
    existing = pr_for_branch(repo, branch)
    if existing and existing.get("state") == "OPEN":
        return existing
    display = program_display_name(repo, school_key)
    url = gh(
        repo,
        "pr",
        "create",
        "--base",
        "main",
        "--head",
        branch,
        "--title",
        f"Ingest and publish {display} history",
        "--body-file",
        str(body_path),
        echo=True,
    ).splitlines()[-1]
    created = pr_for_branch(repo, branch)
    if not created:
        raise WorkflowError(f"PR creation returned {url!r}, but the PR could not be read back")
    return created


def wait_for_deployment(
    repo: Path,
    repo_slug: str,
    sha: str,
    environment: str,
    timeout_seconds: int,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last_state = "not found"
    while time.monotonic() < deadline:
        deployments = gh_json(
            repo,
            "api",
            "--method",
            "GET",
            f"repos/{repo_slug}/deployments?sha={sha}&per_page=50",
        )
        matching = [
            row
            for row in deployments
            if environment.casefold()
            in str(row.get("environment", "")).casefold()
        ]
        for deployment in matching:
            statuses = gh_json(
                repo,
                "api",
                "--method",
                "GET",
                f"repos/{repo_slug}/deployments/{deployment['id']}/statuses?per_page=10",
            )
            if not statuses:
                continue
            latest = statuses[0]
            last_state = latest.get("state", "unknown")
            if last_state == "success":
                return {
                    "deployment_id": deployment["id"],
                    "environment": deployment.get("environment"),
                    "sha": deployment.get("sha"),
                    "state": last_state,
                    "environment_url": latest.get("environment_url"),
                    "log_url": latest.get("log_url"),
                }
            if last_state in {"error", "failure", "inactive"}:
                raise WorkflowError(
                    f"{environment} deployment {deployment['id']} ended in {last_state}"
                )
        print(f"Waiting for {environment} deployment of {sha[:12]} ({last_state})...")
        time.sleep(10)
    raise WorkflowError(
        f"timed out waiting for {environment} deployment of {sha}; last state {last_state}"
    )


def prepare(repo: Path, school_key: str, artifacts: Path, timeout: int) -> int:
    manifest_path = artifacts / "release-manifest.json"
    approved_path = artifacts / "approved-plan.json"
    body_path = artifacts / "pr-body.md"
    for path in (manifest_path, approved_path, body_path):
        if not path.is_file():
            raise WorkflowError(f"required apply artifact is missing: {path}")
    manifest = load_json(manifest_path)
    approved = load_json(approved_path)
    if manifest.get("school_key") != school_key or approved.get("school_key") != school_key:
        raise WorkflowError("release artifacts do not match the requested school")
    if manifest.get("approved_plan_hash") != approved.get("approved_plan_hash"):
        raise WorkflowError("release manifest and approved plan hashes differ")
    if not (repo / f"site/data/teams/{school_key}.json").is_file():
        raise WorkflowError(
            "the approved plan did not publish a team JSON file; use a data-only PR procedure instead"
        )

    paths = verify_change_boundary(repo, manifest)
    print("=== final local release gate ===")
    run_gates(repo, school_key, paths, include_tests=True)
    stage_exact_paths(repo, paths)
    display = program_display_name(repo, school_key)
    run(
        ["git", "commit", "-m", f"Ingest and publish {display}"],
        cwd=repo,
        label="publication commit",
    )
    branch = git(repo, "branch", "--show-current").strip()
    if branch in {"", "main", "master"}:
        raise WorkflowError("release branch must not be main")
    run(
        ["git", "push", "-u", "origin", branch],
        cwd=repo,
        label="push onboarding branch",
    )
    pr = create_or_reuse_pr(repo, branch, school_key, body_path)
    pr_number = str(pr["number"])
    print("\n=== pull-request checks ===")
    gh(repo, "pr", "checks", pr_number, "--watch", "--interval", "10", echo=True)
    state = gh_json(
        repo,
        "pr",
        "view",
        pr_number,
        "--json",
        "number,url,state,mergeable,mergeStateStatus,headRefOid,headRefName,baseRefName",
    )
    if state.get("state") != "OPEN" or state.get("mergeable") != "MERGEABLE":
        raise WorkflowError(f"PR #{pr_number} is not cleanly mergeable: {state}")
    head_sha = state["headRefOid"]
    deployment = wait_for_deployment(
        repo,
        repository_slug(repo),
        head_sha,
        "Preview",
        timeout,
    )
    release_state = {
        "schema_version": 1,
        "school_key": school_key,
        "approved_plan_hash": approved["approved_plan_hash"],
        "branch": branch,
        "head_sha": head_sha,
        "pr_number": int(pr_number),
        "pr_url": state["url"],
        "preview_deployment": deployment,
        "changed_paths": paths,
    }
    (artifacts / "release-state.json").write_text(
        json.dumps(release_state, indent=2) + "\n",
        encoding="utf-8",
    )
    print("\nOWNER GATE 2 — PREVIEW VISUAL QA")
    print(f"PR:      {state['url']}")
    print(f"Preview: {deployment.get('environment_url') or '[open Vercel from the PR check]'}")
    print(f"Checklist:{artifacts / 'visual-qa.md'}")
    print("\nAfter the preview passes, run:")
    print(
        f"python tools/release_school.py {school_key} --merge --preview-approved"
    )
    return 0


def remote_json(url: str) -> Any:
    request = Request(
        url,
        headers={
            "Cache-Control": "no-cache",
            "User-Agent": "college-basketball-history-release-check",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def production_data_check(
    repo: Path,
    school_key: str,
    sha: str,
    changed_paths: list[str],
) -> list[str]:
    json_paths = sorted(
        path
        for path in changed_paths
        if path.startswith("site/data/") and path.endswith(".json")
    )
    required = {
        "site/data/manifest.json",
        "site/data/programs.json",
        f"site/data/teams/{school_key}.json",
    }
    json_paths = sorted(set(json_paths) | required)
    checked: list[str] = []
    for relative in json_paths:
        local_path = repo / relative
        if not local_path.is_file():
            raise WorkflowError(f"production check has no local expected file: {relative}")
        public_path = "/" + relative.removeprefix("site/")
        separator = "&" if "?" in public_path else "?"
        remote = remote_json(
            PRODUCTION_BASE + public_path + separator + "release=" + quote(sha)
        )
        local = json.loads(local_path.read_text(encoding="utf-8"))
        if remote != local:
            raise WorkflowError(f"production JSON differs from merged main: {public_path}")
        checked.append(public_path)
    return checked


def merge(repo: Path, school_key: str, artifacts: Path, timeout: int, approved: bool) -> int:
    if not approved:
        raise WorkflowError(
            "--merge requires --preview-approved after the owner visually checks the exact PR preview"
        )
    state_path = artifacts / "release-state.json"
    if not state_path.is_file():
        raise WorkflowError("release-state.json is missing; run --prepare first")
    state = load_json(state_path)
    if state.get("school_key") != school_key:
        raise WorkflowError("release state belongs to another school")
    branch = git(repo, "branch", "--show-current").strip()
    if branch != state.get("branch"):
        raise WorkflowError(
            f"expected release branch {state.get('branch')!r}; current branch is {branch!r}"
        )
    if git(repo, "status", "--porcelain", "--untracked-files=all").strip():
        raise WorkflowError("release branch is not clean")
    head_sha = git(repo, "rev-parse", "HEAD").strip()
    if head_sha != state.get("head_sha"):
        raise WorkflowError("release branch HEAD changed after preview approval")
    pr_number = str(state["pr_number"])
    gh(repo, "pr", "checks", pr_number, "--watch", "--interval", "10", echo=True)
    pr = gh_json(
        repo,
        "pr",
        "view",
        pr_number,
        "--json",
        "state,mergeable,mergeStateStatus,headRefOid,url",
    )
    if (
        pr.get("state") != "OPEN"
        or pr.get("mergeable") != "MERGEABLE"
        or pr.get("headRefOid") != head_sha
    ):
        raise WorkflowError(f"PR changed or is no longer mergeable: {pr}")

    display = program_display_name(repo, school_key)
    gh(
        repo,
        "pr",
        "merge",
        pr_number,
        "--merge",
        "--subject",
        f"Merge pull request #{pr_number} from {repository_slug(repo).split('/')[0]}/{branch}",
        "--body",
        f"Ingest and publish {display} history",
        echo=True,
    )
    merged_pr = gh_json(
        repo,
        "pr",
        "view",
        pr_number,
        "--json",
        "state,mergedAt,mergeCommit,url",
    )
    if merged_pr.get("state") != "MERGED" or not merged_pr.get("mergeCommit"):
        raise WorkflowError(f"GitHub did not confirm PR #{pr_number} as merged")
    expected_merge_sha = merged_pr["mergeCommit"]["oid"]
    git(repo, "fetch", "origin", echo=True)
    git(repo, "switch", "main", echo=True)
    git(repo, "pull", "--ff-only", "origin", "main", echo=True)
    merge_sha = git(repo, "rev-parse", "HEAD").strip()
    if merge_sha != expected_merge_sha:
        raise WorkflowError(
            "origin/main advanced beyond the visually approved merge before production "
            f"verification ({merge_sha} != {expected_merge_sha})"
        )
    print("\n=== merged-main reproducibility ===")
    run_gates(repo, school_key, [], include_tests=True)
    deployment = wait_for_deployment(
        repo,
        repository_slug(repo),
        merge_sha,
        "Production",
        timeout,
    )
    checked = production_data_check(
        repo,
        school_key,
        merge_sha,
        state.get("changed_paths", []),
    )
    status = git(repo, "status", "-sb").strip()
    if status != "## main...origin/main":
        raise WorkflowError(f"main is not clean and synchronized after merge: {status}")
    final = {
        **state,
        "merge_sha": merge_sha,
        "production_deployment": deployment,
        "production_json_checked": checked,
        "status": "COMPLETE",
    }
    (artifacts / "release-state.json").write_text(
        json.dumps(final, indent=2) + "\n",
        encoding="utf-8",
    )
    print("\nPRODUCTION QA PASSED")
    print(f"Merged SHA: {merge_sha}")
    print(f"Production: {deployment.get('environment_url') or PRODUCTION_BASE}")
    print(f"Exact JSON documents verified: {len(checked):,}")
    print("main is clean and synchronized with origin/main.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare or merge the sealed release for one onboarded school."
    )
    parser.add_argument("school_key")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare", action="store_true")
    mode.add_argument("--merge", action="store_true")
    parser.add_argument("--preview-approved", action="store_true")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--deployment-timeout", type=int, default=900)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    artifacts = output_dir(repo, args.school_key, args.output_dir)
    try:
        if args.prepare:
            if args.preview_approved:
                raise WorkflowError("--preview-approved is valid only with --merge")
            return prepare(repo, args.school_key, artifacts, args.deployment_timeout)
        return merge(
            repo,
            args.school_key,
            artifacts,
            args.deployment_timeout,
            args.preview_approved,
        )
    except (WorkflowError, KeyError, ValueError, OSError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
