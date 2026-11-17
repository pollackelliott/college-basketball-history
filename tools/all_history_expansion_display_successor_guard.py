#!/usr/bin/env python3
"""Fail-closed nested-rehearsal proof for a post-Freeze display-only successor.

The immutable All-History Integration Freeze always remains the historical
authority. A later committed opponent-display normalization may change only two
representation columns, not the underlying games or any source evidence.
This checker independently proves that exact topology using local Git history,
the frozen package hashes and existing project display authority. It never
trusts an ignored sidecar to authorize a mutation.
"""
from __future__ import annotations

import csv
import hashlib
import io
import re
import subprocess
from pathlib import Path

import normalize_historical_opponent_displays as normalization


PACKAGE_NAMES = (
    "conferences.csv", "notes.md", "opponents.csv",
    "source-games.csv", "source-notes.md", "venues.csv",
)
DISPLAY_COLUMNS = {
    "opponents.csv": "canonical_opponent_name",
    "source-games.csv": "normalized_opponent_name",
}


def _git(root: Path, *args: str) -> bytes | None:
    try:
        done = subprocess.run(
            ["git", "-C", str(root), *args],
            check=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None
    return done.stdout if done.returncode == 0 else None


def _rows(data: bytes) -> tuple[list[str], list[dict[str, str]]]:
    value = io.StringIO(data.decode("utf-8-sig"), newline="")
    reader = csv.DictReader(value)
    return list(reader.fieldnames or []), list(reader)


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _blob(root: Path, commit: str, school: str, name: str) -> bytes | None:
    return _git(root, "show", f"{commit}:schools/{school}/{name}")


def _column_only_changes(
    before: bytes, after: bytes, column: str,
) -> list[tuple[dict[str, str], dict[str, str]]] | None:
    old_fields, old_rows = _rows(before)
    new_fields, new_rows = _rows(after)
    if old_fields != new_fields or column not in old_fields or len(old_rows) != len(new_rows):
        return None
    result = []
    for old, new in zip(old_rows, new_rows):
        if {k: v for k, v in old.items() if k != column} != {
            k: v for k, v in new.items() if k != column
        }:
            return None
        if old[column] != new[column]:
            result.append((old, new))
    return result


def permits_authenticated_display_successor(
    root: Path,
    school: str,
    freeze_hashes: dict[str, str],
    *,
    diagnostics: list[str] | None = None,
) -> bool:
    """Prove an exact Git successor, never grant arbitrary package drift.

    Allow a bounded sequence of intervening disjoint current-main merges that
    preserve *all* six package files, followed by exactly one first-parent
    normalization commit whose predecessor has the original frozen six files.
    Require the already-committed display changes to be the same scoped,
    established-project-identity representation chosen by the permanent
    normalizer. No other historical or source column may change.
    """
    def reject(reason: str) -> bool:
        if diagnostics is not None:
            diagnostics.append(reason)
        return False

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", school):
        return reject("school_key_invalid")
    if set(freeze_hashes) != set(PACKAGE_NAMES):
        return reject("freeze_member_set_invalid")
    school_dir = root / "schools" / school
    current = {name: (school_dir / name).read_bytes() for name in PACKAGE_NAMES}
    changed = {name for name in PACKAGE_NAMES if _sha(current[name]) != freeze_hashes[name]}
    if not changed or not changed.issubset(DISPLAY_COLUMNS):
        return reject("changed_file_scope_invalid")
    if "opponents.csv" not in changed:
        return reject("opponents_unchanged")
    # No uncommitted/staged bypass; the source must equal its Git HEAD.
    dirty = _git(root, "status", "--porcelain", "--untracked-files=no", "--",
                 f"schools/{school}")
    head = _git(root, "rev-parse", "HEAD")
    if dirty is None or dirty or head is None:
        return reject("tracked_package_dirty")
    cursor = head.decode().strip()
    for name in PACKAGE_NAMES:
        current_git = _blob(root, cursor, school, name)
        if current_git is None or current_git != current[name]:
            return reject("working_tree_not_equal_head")

    # A later current-main refresh is a two-parent merge whose target package
    # is byte-identical to its first parent, even though tooling may advance.
    for _ in range(12):
        lineage = _git(root, "rev-list", "--parents", "-n", "1", cursor)
        if lineage is None:
            return reject("lineage_unavailable")
        parts = lineage.decode().split()
        if not parts or parts[0] != cursor:
            return reject("lineage_invalid")
        if len(parts) == 3:
            parent = parts[1]
            if any(
                _blob(root, cursor, school, name)
                != _blob(root, parent, school, name)
                for name in PACKAGE_NAMES
            ):
                return reject("merge_changes_school_package")
            cursor = parent
            continue
        if len(parts) != 2:
            return reject("nonlinear_or_missing_parent")
        parent = parts[1]
        message = _git(root, "show", "-s", "--format=%s", cursor)
        if message is None or message.decode().strip() != (
            f"Normalize {school} historical opponent display representation"
        ):
            return reject("unexpected_normalization_commit_message")

        original = {name: _blob(root, parent, school, name) for name in PACKAGE_NAMES}
        if any(original[name] is None or _sha(original[name]) != freeze_hashes[name]
               for name in PACKAGE_NAMES):
            return reject("normalization_predecessor_not_frozen")
        paths = _git(root, "diff", "--name-only", parent, cursor)
        if paths is None:
            return reject("git_diff_unavailable")
        permitted = {f"schools/{school}/{name}" for name in DISPLAY_COLUMNS}
        actual_paths = set(paths.decode().splitlines())
        if not actual_paths or not actual_paths.issubset(permitted):
            return reject("normalization_changed_extra_path")

        opponent_changes = _column_only_changes(
            original["opponents.csv"], current["opponents.csv"],
            DISPLAY_COLUMNS["opponents.csv"],
        )
        source_changes = _column_only_changes(
            original["source-games.csv"], current["source-games.csv"],
            DISPLAY_COLUMNS["source-games.csv"],
        )
        if opponent_changes is None or source_changes is None or not opponent_changes:
            return reject("non_display_field_delta")
        try:
            registered = normalization.project_program_keys(root)
            established = normalization.authority_names_by_key(
                root, school, program_keys=registered,
            )
        except (OSError, ValueError, KeyError):
            return reject("identity_authority_unavailable")

        final_name_by_key: dict[str, str] = {}
        for old, new in opponent_changes:
            key = new.get("canonical_opponent_key", "").strip()
            new_name = new.get("canonical_opponent_name", "").strip()
            if not key or not new_name or key in registered:
                return reject("invalid_nonregistered_display_key")
            signatures = {
                normalization.build_site_data.normalized_name_signature(x)
                for x in established.get(key, ())
                if normalization.build_site_data.normalized_name_signature(x)
            }
            if len(signatures) != 1 or (
                normalization.build_site_data.normalized_name_signature(new_name)
                not in signatures
            ):
                return reject("established_identity_signature_mismatch")
            if key in final_name_by_key and final_name_by_key[key] != new_name:
                return reject("duplicate_key_display_mismatch")
            final_name_by_key[key] = new_name

        # Every changed source display must correspond to a changed opponent
        # identity display, and the permanent scoped sync edits every source
        # row for that key that previously disagreed with the final name.
        for old, new in source_changes:
            key = new.get("normalized_opponent_key", "").strip()
            if key not in final_name_by_key or (
                new.get("normalized_opponent_name") != final_name_by_key[key]
            ):
                return reject("source_name_outside_changed_keys")
        _, source_before = _rows(original["source-games.csv"])
        _, source_after = _rows(current["source-games.csv"])
        for old, new in zip(source_before, source_after):
            key = new.get("normalized_opponent_key", "").strip()
            if key in final_name_by_key and (
                new.get("normalized_opponent_name") != final_name_by_key[key]
            ):
                return reject("changed_key_source_not_aligned")
        return True
    return reject("lineage_depth_limit")
