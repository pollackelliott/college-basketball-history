#!/usr/bin/env python3
"""Vercel Ignored Build Step policy for the checked-in static site.

Exit 0 means Vercel should skip the deployment.
Exit 1 means Vercel should continue the deployment.

The static `git.deploymentEnabled` allow-list in `vercel.json` is the primary
quota-control boundary. This helper mirrors that allow-list as defense in depth.
"""
from __future__ import annotations

import os


PUBLICATION_BRANCH_PREFIXES = ("data/", "maintenance/")


def should_skip(*, ref: str, parent_available: bool, site_diff_returncode: int) -> bool:
    """Return whether Vercel should skip this Git-triggered deployment.

    `parent_available` and `site_diff_returncode` remain accepted for compatibility
    with existing callers/tests, but deployment eligibility is intentionally branch-only:
    Production `main` and exact publication Preview branches are deployable; everything
    else is non-deployable.
    """
    del parent_available, site_diff_returncode
    if ref == "main":
        return False
    if ref.startswith(PUBLICATION_BRANCH_PREFIXES):
        return False
    return True


def main() -> int:
    ref = os.environ.get("VERCEL_GIT_COMMIT_REF", "")
    return 0 if should_skip(
        ref=ref,
        parent_available=False,
        site_diff_returncode=2,
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
