#!/usr/bin/env python3
"""Fail-closed, ref-preserving core for a post-seal presentation-only successor.

This module deliberately does NOT publish a branch, acquire an Implementation
lock, create a Preview, or approve Gate 2. A future guarded runner must first
fresh-authenticate the ORIGINAL sealed-apply successor and approved-plan authority,
then use this module inside its write-ahead/CAS/fresh-verifier transaction.
"""
from __future__ import annotations

import os
import re
import subprocess
import tempfile
from pathlib import Path

ASSET_PATH = "site/index.html"
PLAN_KIND = "REMOTE_IMPLEMENTATION_PRESENTATION_REFRESH_TREE_PLAN_V1"
OID = re.compile(r"^[0-9a-f]{40}$")


class PresentationRefreshStop(ValueError):
    """The proposed presentation-only successor is not authorized."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise PresentationRefreshStop(code)


def git(
    repo: Path,
    *args: str,
    index_file: str | None = None,
    env_overrides: dict[str, str] | None = None,
) -> str:
    env = os.environ.copy()
    if index_file is not None:
        env["GIT_INDEX_FILE"] = index_file
    if env_overrides:
        env.update(env_overrides)
    result = subprocess.run(
        ["git", *args], cwd=repo, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        check=False,
    )
    if result.returncode:
        raise PresentationRefreshStop(
            f"PRESENTATION_GIT_FAILURE:{' '.join(args)}:{result.stdout.strip()}"
        )
    return result.stdout.strip()


def commit_tree(repo: Path, commit: str) -> str:
    require(bool(OID.fullmatch(commit)), "PRESENTATION_COMMIT_ID_INVALID")
    require(git(repo, "cat-file", "-t", commit) == "commit", "PRESENTATION_NOT_COMMIT")
    return git(repo, "rev-parse", f"{commit}^{{tree}}")


def asset_entry(repo: Path, revision: str) -> tuple[str, str]:
    lines = git(repo, "ls-tree", revision, "--", ASSET_PATH).splitlines()
    require(len(lines) == 1, "PRESENTATION_ASSET_MISSING")
    meta, sep, path = lines[0].partition("\t")
    require(sep == "\t" and path == ASSET_PATH, "PRESENTATION_ASSET_PATH_INVALID")
    fields = meta.split()
    require(
        len(fields) == 3 and fields[1] == "blob" and bool(OID.fullmatch(fields[2])),
        "PRESENTATION_ASSET_NOT_BLOB",
    )
    require(fields[0] == "100644", "PRESENTATION_ASSET_MODE_INVALID")
    return fields[0], fields[2]


def require_one_asset_diff(repo: Path, old: str, new: str) -> None:
    # Git compares COMPLETE trees. A single M path guarantees every other
    # tracked data/reference/generated-public-JSON blob is byte-identical.
    changed = git(
        repo, "diff", "--no-ext-diff", "--name-status", old, new,
    ).splitlines()
    require(
        changed == [f"M\t{ASSET_PATH}"],
        "PRESENTATION_CHANGED_PATHS_NOT_EXACT_ASSET",
    )


def presentation_refresh_tree_plan(
    repo: Path,
    *,
    sealed_commit_sha: str,
    repair_main_sha: str,
    expected_sealed_tree_sha: str,
    expected_asset_blob_sha: str,
) -> dict[str, object]:
    """Prepare an unreferenced candidate tree, never changing a Git ref.

    Authenticated authority must supply the pinned ORIGINAL sealed commit/tree,
    accepted protected-main code commit, and reviewed code blob. A random branch
    name or a human assertion is not a substitute for those proof inputs.
    """
    repo = Path(repo)
    sealed_tree = commit_tree(repo, sealed_commit_sha)
    commit_tree(repo, repair_main_sha)
    require(
        sealed_tree == expected_sealed_tree_sha,
        "PRESENTATION_SEALED_TREE_MISMATCH",
    )
    require(
        bool(OID.fullmatch(expected_asset_blob_sha)),
        "PRESENTATION_EXPECTED_ASSET_SHA_INVALID",
    )
    _, source_blob = asset_entry(repo, repair_main_sha)
    _, existing_blob = asset_entry(repo, sealed_commit_sha)
    require(
        source_blob == expected_asset_blob_sha,
        "PRESENTATION_REPAIR_SOURCE_BLOB_MISMATCH",
    )
    require(
        existing_blob != source_blob,
        "PRESENTATION_NO_EFFECTIVE_CHANGE",
    )

    # Build the exact tree in a disposable index. No working-tree edit,
    # branch move, or commit is performed; only an immutable Git tree object
    # may be created for deterministic proof and later guarded publication.
    with tempfile.TemporaryDirectory(prefix="presentation-index-") as tmp:
        temporary_index = str(Path(tmp) / "candidate.index")
        git(repo, "read-tree", sealed_commit_sha, index_file=temporary_index)
        git(
            repo, "update-index", "--cacheinfo",
            f"100644,{source_blob},{ASSET_PATH}", index_file=temporary_index,
        )
        candidate_tree = git(repo, "write-tree", index_file=temporary_index)

    require_one_asset_diff(repo, sealed_commit_sha, candidate_tree)
    _, candidate_blob = asset_entry(repo, candidate_tree)
    require(
        candidate_blob == source_blob,
        "PRESENTATION_CANDIDATE_BLOB_MISMATCH",
    )
    return {
        "kind": PLAN_KIND,
        "sealed_commit_sha": sealed_commit_sha,
        "sealed_tree_sha": sealed_tree,
        "repair_main_sha": repair_main_sha,
        "accepted_asset_blob_sha": source_blob,
        "allowed_changed_paths": [ASSET_PATH],
        "candidate_tree_sha": candidate_tree,
        "tracked_basketball_mutation": "NONE",
        "branch_published": False,
        "owner_gate_2_approved": False,
    }


def verify_presentation_successor(
    repo: Path,
    *,
    sealed_commit_sha: str,
    successor_sha: str,
    repair_main_sha: str,
    expected_sealed_tree_sha: str,
    expected_asset_blob_sha: str,
) -> dict[str, object]:
    """Independent exact-parent and exact-tree proof of a proposed commit.

    A committed successor MUST be one direct child of the original sealed
    commit, with the exact prepared tree. This does not assert that its Git ref
    was published through CAS; the guarded control layer must prove that.
    """
    plan = presentation_refresh_tree_plan(
        repo,
        sealed_commit_sha=sealed_commit_sha,
        repair_main_sha=repair_main_sha,
        expected_sealed_tree_sha=expected_sealed_tree_sha,
        expected_asset_blob_sha=expected_asset_blob_sha,
    )
    successor_tree = commit_tree(Path(repo), successor_sha)
    parents = git(Path(repo), "rev-list", "--parents", "-n", "1", successor_sha).split()
    require(
        parents == [successor_sha, sealed_commit_sha],
        "PRESENTATION_SUCCESSOR_PARENT_MISMATCH",
    )
    require(
        successor_tree == plan["candidate_tree_sha"],
        "PRESENTATION_SUCCESSOR_TREE_MISMATCH",
    )
    require_one_asset_diff(Path(repo), sealed_commit_sha, successor_sha)
    _, actual_blob = asset_entry(Path(repo), successor_sha)
    require(
        actual_blob == plan["accepted_asset_blob_sha"],
        "PRESENTATION_SUCCESSOR_ASSET_MISMATCH",
    )
    return {
        **plan,
        "successor_sha": successor_sha,
        "successor_tree_sha": successor_tree,
        "fresh_tree_equivalence": "PASS",
        "sealed_parent": sealed_commit_sha,
    }
