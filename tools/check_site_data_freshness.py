#!/usr/bin/env python3
"""Fail when committed public site JSON is stale relative to curated repository data.

This is a release/verification gate. It builds the deterministic public JSON in a
throwaway copy, then compares the generated ``site/data`` tree with the repository's
committed ``site/data`` tree. No tracked file in the real repository is modified.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


class FreshnessError(RuntimeError):
    pass


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_hashes(repo: Path) -> dict[str, str]:
    root = repo / "site" / "data"
    if not root.is_dir():
        raise FreshnessError(f"missing generated site-data directory: {root}")
    return {
        path.relative_to(repo).as_posix(): file_sha(path)
        for path in sorted(root.rglob("*.json"))
        if path.is_file()
    }


def copy_repository(source: Path, destination: Path) -> None:
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if name in {".git", ".onboarding", "__pycache__"} or name.endswith(".pyc")
        }

    shutil.copytree(source, destination, ignore=ignore)


def freshness_report(repo: Path) -> dict[str, object]:
    committed = json_hashes(repo)
    with tempfile.TemporaryDirectory(prefix="site-freshness-") as temporary:
        rehearsal = Path(temporary) / "repository"
        copy_repository(repo, rehearsal)
        completed = subprocess.run(
            [
                sys.executable,
                str(rehearsal / "tools" / "build_site_data.py"),
                str(rehearsal),
                "--apply",
            ],
            cwd=rehearsal,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if completed.returncode:
            raise FreshnessError(
                "deterministic site rebuild failed:\n" + completed.stdout.rstrip()
            )
        rebuilt = json_hashes(rehearsal)

    stale = sorted(
        path
        for path in set(committed) | set(rebuilt)
        if committed.get(path) != rebuilt.get(path)
    )
    return {
        "status": "PASS" if not stale else "FAIL",
        "committed_json_files": len(committed),
        "rebuilt_json_files": len(rebuilt),
        "stale_paths": stale,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repository_root",
        nargs="?",
        default=None,
        help="Repository root; defaults to the parent of tools/.",
    )
    args = parser.parse_args()
    repo = (
        Path(args.repository_root).resolve()
        if args.repository_root
        else Path(__file__).resolve().parents[1]
    )
    try:
        report = freshness_report(repo)
    except (FreshnessError, FileNotFoundError, OSError) as exc:
        print(f"FAIL: {exc}")
        return 1

    print("College Basketball History — committed site-data freshness")
    print(f"Repository:           {repo}")
    print(f"Committed JSON files: {report['committed_json_files']}")
    print(f"Rebuilt JSON files:   {report['rebuilt_json_files']}")
    print(f"Stale paths:          {len(report['stale_paths'])}")
    for path in report["stale_paths"][:50]:
        print(f"  - {path}")
    if report["stale_paths"]:
        print(
            "FAIL: committed site/data does not match deterministic public output. "
            "Run tools/build_site_data.py --apply and commit the generated JSON before Preview/release."
        )
        return 1
    print("PASS: committed site/data exactly matches a deterministic rebuild.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
