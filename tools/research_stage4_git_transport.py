#!/usr/bin/env python3
"""Read-only, hash-bound Git-object transport for expansion Stage 4 authoring.

The GitHub Actions producer ships a real Git bundle containing the exact
protected-main ancestry. The local consumer clones the bundle, validates real
Git objects and unmodified permanent runtime bytes, then invokes the existing
Stage 4 author command against the unchanged Stage 3B ZIP.

This module provides transport, not historical authority or an alternative
Stage 4 acceptance algorithm.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BUNDLE_FILE = "research-stage4-history.bundle"
MANIFEST_FILE = "research-stage4-history-manifest.json"
SOURCE_PATHS = (
    "tools/research_stage4.py",
    "tools/research_stage4_closeout.py",
    "tools/expansion_stage4_coverage.py",
)
_SHA40 = re.compile(r"[0-9a-f]{40}\Z")
_SHA64 = re.compile(r"[0-9a-f]{64}\Z")
_SCHOOL = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


class GitTransportError(ValueError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _hash_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _require(value: str, expression: re.Pattern[str], label: str) -> str:
    if not expression.fullmatch(value):
        raise GitTransportError(f"invalid {label}")
    return value


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, check=False
    )
    if check and result.returncode:
        raise GitTransportError(
            f"git {args[0]} failed: {result.stderr.decode(errors='replace').strip()}"
        )
    return result


def _commit(repo: Path, sha: str, label: str) -> None:
    _require(sha, _SHA40, label)
    result = _git(repo, "rev-parse", "--verify", f"{sha}^{{commit}}", check=False)
    if result.returncode or result.stdout.decode().strip() != sha:
        raise GitTransportError(f"{label} is missing or not the exact Git commit")


def _auth_checkout(repo: Path, main_sha: str, base_sha: str) -> None:
    git_dir = _git(repo, "rev-parse", "--is-inside-work-tree").stdout.decode().strip()
    if git_dir != "true":
        raise GitTransportError("genuine Git worktree required")
    _commit(repo, main_sha, "protected-main SHA")
    _commit(repo, base_sha, "research-base SHA")
    head = _git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    if head != main_sha:
        raise GitTransportError("runtime checkout is not exact protected main")
    if _git(repo, "merge-base", "--is-ancestor", base_sha, main_sha, check=False).returncode:
        raise GitTransportError("research-base Git commit is not in protected-main ancestry")
    if _git(repo, "status", "--porcelain", "--untracked-files=no").stdout.strip():
        raise GitTransportError("permanent-tool runtime contains tracked edits")
    for path in SOURCE_PATHS:
        source = repo / path
        if not source.is_file():
            raise GitTransportError(f"permanent-tool runtime missing {path}")
        from_git = _git(repo, "show", f"{main_sha}:{path}").stdout
        if source.read_bytes() != from_git:
            raise GitTransportError(f"stale/mismatched permanent-tool runtime: {path}")


def build(*, repo: Path, output: Path, main_sha: str, base_sha: str,
          school: str, checkpoint_sha: str) -> dict:
    """Run in an Actions Git checkout with complete fetched history."""
    _require(school, _SCHOOL, "school key")
    _require(checkpoint_sha, _SHA64, "Stage 3B checkpoint SHA-256")
    _commit(repo, main_sha, "protected-main SHA")
    _commit(repo, base_sha, "research-base SHA")
    remote = _git(repo, "ls-remote", "origin", "refs/heads/main").stdout.decode().strip()
    if not remote or remote.split()[0] != main_sha:
        raise GitTransportError("protected main moved or requested main SHA is wrong")
    if _git(repo, "merge-base", "--is-ancestor", base_sha, main_sha, check=False).returncode:
        raise GitTransportError("research-base Git commit is not in protected-main ancestry")
    output.mkdir(parents=True, exist_ok=True)
    bundle = output / BUNDLE_FILE
    # Temporary local ref is scheduling/transport only: no remote ref is changed.
    ref = "refs/heads/stage4-transport-immutable-main"
    _git(repo, "update-ref", ref, main_sha)
    try:
        _git(repo, "bundle", "create", str(bundle), ref)
    finally:
        _git(repo, "update-ref", "-d", ref)
    _git(repo, "bundle", "verify", str(bundle))
    manifest = {
        "schema_version": 1,
        "transport": "AUTHENTICATED_GIT_OBJECT_BUNDLE",
        "protected_main_sha": main_sha,
        "research_base_sha": base_sha,
        "school_key": school,
        "stage3b_checkpoint_sha256": checkpoint_sha,
        "bundle_name": BUNDLE_FILE,
        "bundle_sha256": _sha256(bundle),
        "bundle_bytes": bundle.stat().st_size,
    }
    (output / MANIFEST_FILE).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def run(*, artifact: Path, checkpoint: Path, output: Path, school: str,
        main_sha: str, base_sha: str, checkpoint_sha: str) -> dict:
    """Authenticate, clone genuine Git history, invoke permanent Stage 4 author."""
    _require(main_sha, _SHA40, "protected-main SHA")
    _require(base_sha, _SHA40, "research-base SHA")
    _require(checkpoint_sha, _SHA64, "Stage 3B checkpoint SHA-256")
    _require(school, _SCHOOL, "school key")
    manifest = json.loads((artifact / MANIFEST_FILE).read_text())
    expected = {
        "schema_version": 1,
        "transport": "AUTHENTICATED_GIT_OBJECT_BUNDLE",
        "protected_main_sha": main_sha,
        "research_base_sha": base_sha,
        "school_key": school,
        "stage3b_checkpoint_sha256": checkpoint_sha,
        "bundle_name": BUNDLE_FILE,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise GitTransportError(f"Git-transport manifest mismatch: {key}")
    bundle = artifact / BUNDLE_FILE
    if bundle.stat().st_size != manifest.get("bundle_bytes") or _sha256(bundle) != manifest.get("bundle_sha256"):
        raise GitTransportError("changed or corrupt genuine Git bundle")
    if not checkpoint.is_file() or _sha256(checkpoint) != checkpoint_sha:
        raise GitTransportError("changed Stage 3B checkpoint bytes/hash")

    output.mkdir(parents=True, exist_ok=True)
    # Never 'git init' or write synthetic Git objects. A real clone of the
    # authenticated Actions Git bundle is mandatory.
    with tempfile.TemporaryDirectory(prefix="stage4-auth-git-") as tmp:
        root = Path(tmp) / "runtime"
        cloned = subprocess.run(
            ["git", "clone", "--quiet", "--no-checkout", str(bundle), str(root)],
            capture_output=True, check=False,
        )
        if cloned.returncode:
            raise GitTransportError("authenticated Git bundle cannot be cloned: " + cloned.stderr.decode(errors="replace").strip())
        _git(root, "checkout", "--quiet", "--detach", main_sha)
        _auth_checkout(root, main_sha, base_sha)
        if _sha256(checkpoint) != checkpoint_sha:
            raise GitTransportError("Stage 3B checkpoint changed before permanent author")
        cmd = [sys.executable, "tools/research_stage4.py", "author", school,
               str(checkpoint.resolve()), "--main-sha", main_sha,
               "--output-dir", str((output / "stage4").resolve())]
        process = subprocess.run(cmd, cwd=root, capture_output=True)
        (output / "permanent-stage4-stdout.txt").write_bytes(process.stdout)
        (output / "permanent-stage4-stderr.txt").write_bytes(process.stderr)
        result = {
            "status": "PERMANENT_STAGE4_ACCEPTANCE_FAILED" if process.returncode else "PERMANENT_STAGE4_COMMAND_SUCCEEDED",
            "exit_code": process.returncode,
            "protected_main_sha": main_sha,
            "research_base_sha": base_sha,
            "stage3b_checkpoint_sha256": checkpoint_sha,
            "authenticated_git_worktree": True,
            "permanent_tool": "tools/research_stage4.py author",
            "tool_sha256": _sha256(root / "tools/research_stage4.py"),
        }
        (output / "stage4-git-transport-execution.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
        if process.returncode:
            raise GitTransportError(f"permanent Stage 4 author failed with exit {process.returncode}; diagnostics preserved")
        return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    for mode in ("build", "run"):
        p = sub.add_parser(mode)
        p.add_argument("--main-sha", required=True)
        p.add_argument("--research-base-sha", required=True)
        p.add_argument("--school-key", required=True)
        p.add_argument("--checkpoint-sha256", required=True)
        p.add_argument("--output-dir", type=Path, required=True)
        if mode == "build":
            p.add_argument("--repo-root", type=Path, required=True)
        else:
            p.add_argument("--artifact-dir", type=Path, required=True)
            p.add_argument("--stage3b-checkpoint", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.mode == "build":
            value = build(repo=args.repo_root.resolve(), output=args.output_dir.resolve(), main_sha=args.main_sha,
                          base_sha=args.research_base_sha, school=args.school_key, checkpoint_sha=args.checkpoint_sha256)
        else:
            value = run(artifact=args.artifact_dir.resolve(), checkpoint=args.stage3b_checkpoint.resolve(),
                        output=args.output_dir.resolve(), school=args.school_key, main_sha=args.main_sha,
                        base_sha=args.research_base_sha, checkpoint_sha=args.checkpoint_sha256)
        print(json.dumps(value, indent=2, sort_keys=True))
        return 0
    except (GitTransportError, OSError, ValueError) as exc:
        print(f"STAGE4_AUTHENTICATED_GIT_TRANSPORT_BLOCKED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
