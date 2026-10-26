#!/usr/bin/env python3
"""Vercel Ignored Build Step policy for the checked-in static site.

Exit 0 means Vercel should skip the deployment.
Exit 1 means Vercel should continue the deployment.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess


CONTROL_BRANCH = "control/remote-implementation"


def should_skip(*, ref: str, parent_available: bool, site_diff_returncode: int) -> bool:
    """Return whether Vercel should skip this Git-triggered deployment."""
    if ref == "main":
        return False
    if ref == CONTROL_BRANCH:
        return True
    if not parent_available:
        return False
    # git diff --quiet: 0 = no deployable change, 1 = change, >1 = error.
    # Errors fail open so an uncertain gate cannot suppress a required Preview.
    return site_diff_returncode == 0


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    ref = os.environ.get("VERCEL_GIT_COMMIT_REF", "")

    parent = subprocess.run(
        ["git", "rev-parse", "HEAD^"],
        cwd=repo,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    parent_available = parent.returncode == 0

    diff_returncode = 2
    if parent_available:
        diff_returncode = subprocess.run(
            ["git", "diff", "--quiet", "HEAD^", "HEAD", "--", "site", "vercel.json"],
            cwd=repo,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode

    return 0 if should_skip(
        ref=ref,
        parent_available=parent_available,
        site_diff_returncode=diff_returncode,
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
