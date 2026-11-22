#!/usr/bin/env python3
"""Fail-closed nested-rehearsal proof for post-Freeze representation successors.

The immutable All-History Integration Freeze remains historical authority.
Expansion Phase 0 may make one exact census-bound venue representation rebase,
and a later committed Stage-2 normalization may change only opponent display
columns.  This checker proves that composition from Git ancestry, the frozen
package hashes, the frozen Phase-0 venue census, and existing project display
authority.  It never grants arbitrary school-package drift.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import normalize_historical_opponent_displays as normalization


PACKAGE_NAMES = (
    "conferences.csv", "notes.md", "opponents.csv",
    "source-games.csv", "source-notes.md", "venues.csv",
)
DISPLAY_COLUMNS = {
    "opponents.csv": "canonical_opponent_name",
    "source-games.csv": "normalized_opponent_name",
}
OPPONENT_REPRESENTATION_COLUMNS = {
    "canonical_opponent_name",
    "current_d1",
}
PHASE0_VENUE_SUFFIX = " Integration rebase resolved final global venue ID {venue_id}."


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


def _csv_bytes(
    fields: list[str],
    rows: list[dict[str, str]],
    *,
    bom: bool = False,
    line_ending: str = "\n",
) -> bytes:
    value = io.StringIO(newline="")
    writer = csv.DictWriter(value, fieldnames=fields, lineterminator=line_ending)
    writer.writeheader()
    writer.writerows(rows)
    data = value.getvalue().encode("utf-8")
    return (b"\xef\xbb\xbf" + data) if bom else data


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _blob(root: Path, commit: str, school: str, name: str) -> bytes | None:
    return _git(root, "show", f"{commit}:schools/{school}/{name}")


def _package(root: Path, commit: str, school: str) -> dict[str, bytes] | None:
    result: dict[str, bytes] = {}
    for name in PACKAGE_NAMES:
        data = _blob(root, commit, school, name)
        if data is None:
            return None
        result[name] = data
    return result


def _columns_only_changes(
    before: bytes,
    after: bytes,
    allowed_columns: set[str],
) -> list[tuple[dict[str, str], dict[str, str]]] | None:
    old_fields, old_rows = _rows(before)
    new_fields, new_rows = _rows(after)
    if (
        old_fields != new_fields
        or not allowed_columns.intersection(old_fields)
        or len(old_rows) != len(new_rows)
    ):
        return None
    result = []
    for old, new in zip(old_rows, new_rows):
        if {k: v for k, v in old.items() if k not in allowed_columns} != {
            k: v for k, v in new.items() if k not in allowed_columns
        }:
            return None
        if any(old.get(column, "") != new.get(column, "") for column in allowed_columns):
            result.append((old, new))
    return result


def _column_only_changes(
    before: bytes, after: bytes, column: str,
) -> list[tuple[dict[str, str], dict[str, str]]] | None:
    return _columns_only_changes(before, after, {column})


def _opponent_representation_changes(
    before: bytes,
    after: bytes,
) -> list[tuple[dict[str, str], dict[str, str]]] | None:
    changes = _columns_only_changes(
        before,
        after,
        OPPONENT_REPRESENTATION_COLUMNS,
    )
    if changes is None:
        return None
    for old, new in changes:
        if old.get("current_d1", "") != new.get("current_d1", "") and (
            new.get("current_d1", "") not in {"Yes", "No"}
        ):
            return None
    return changes


def _package_preserving_first_parent(
    root: Path, commit: str, school: str,
) -> str | None:
    lineage = _git(root, "rev-list", "--parents", "-n", "1", commit)
    if lineage is None:
        return None
    parts = lineage.decode().split()
    if len(parts) != 3 or parts[0] != commit:
        return None
    first_parent = parts[1]
    if any(
        _blob(root, commit, school, name)
        != _blob(root, first_parent, school, name)
        for name in PACKAGE_NAMES
    ):
        return None
    return first_parent


def _registry_ids_by_key(root: Path, commit: str) -> dict[str, str] | None:
    data = _git(root, "show", f"{commit}:data/reference/venues.csv")
    if data is None:
        return None
    fields, rows = _rows(data)
    if "venue_key" not in fields or "venue_id" not in fields:
        return None
    result: dict[str, str] = {}
    for row in rows:
        key = row.get("venue_key", "").strip()
        venue_id = row.get("venue_id", "").strip()
        if not key or not venue_id:
            continue
        if key in result and result[key] != venue_id:
            return None
        result[key] = venue_id
    return result


def _reconstruct_frozen_venues(
    root: Path,
    school: str,
    phase0_commit: str,
    phase0_venues: bytes,
    freeze_venue_sha256: str,
    integration_freeze: dict[str, Any],
    *,
    diagnostics: list[str] | None = None,
) -> bool:
    def reject(reason: str) -> bool:
        if diagnostics is not None:
            diagnostics.append(reason)
        return False

    if (
        integration_freeze.get("kind") != "ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE"
        or integration_freeze.get("status") != "INTEGRATION_FROZEN"
        or integration_freeze.get("school_key") != school
        or (integration_freeze.get("candidate_member_sha256") or {}).get("venues.csv")
        != freeze_venue_sha256
    ):
        return reject("phase0_freeze_identity_invalid")
    integration_base = str(integration_freeze.get("integration_base_sha") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", integration_base):
        return reject("phase0_integration_base_invalid")
    lineage = _git(root, "rev-list", "--parents", "-n", "1", phase0_commit)
    if lineage is None:
        return reject("phase0_lineage_unavailable")
    parts = lineage.decode().split()
    if len(parts) != 2 or parts[0] != phase0_commit or parts[1] != integration_base:
        return reject("phase0_integration_base_mismatch")
    message = _git(root, "show", "-s", "--format=%s", phase0_commit)
    if message is None or message.decode().strip() != (
        f"Stage {school} all-history expansion Phase 0"
    ):
        return reject("phase0_commit_message_invalid")

    census = integration_freeze.get("venue_reconciliation_census")
    if (
        not isinstance(census, dict)
        or census.get("schema_version") != 1
        or census.get("blocker_count") != 0
        or not isinstance(census.get("rows"), list)
    ):
        return reject("phase0_venue_census_invalid")
    census_rows = census["rows"]
    if (
        not census_rows
        or census.get("venue_count") != len(census_rows)
        or len(census_rows) != len({
            str(row.get("venue_key") or "").strip() for row in census_rows
        })
    ):
        return reject("phase0_venue_census_population_invalid")

    fields, rows = _rows(phase0_venues)
    if not {"venue_key", "venue_id", "notes"}.issubset(fields):
        return reject("phase0_venue_schema_invalid")
    parent_venues = _blob(root, integration_base, school, "venues.csv")
    if parent_venues is None:
        return reject("phase0_parent_venues_unavailable")
    parent_fields, parent_rows = _rows(parent_venues)
    if parent_fields != fields:
        return reject("phase0_parent_venue_schema_mismatch")
    if len(rows) != len(parent_rows) + len(census_rows):
        return reject("phase0_supplemental_venue_population_mismatch")
    if rows[:len(parent_rows)] != parent_rows:
        return reject("phase0_inherited_venue_rows_changed")

    registry = _registry_ids_by_key(root, phase0_commit)
    if registry is None:
        return reject("phase0_global_venue_registry_unavailable")

    positions: dict[str, list[int]] = {}
    for index in range(len(parent_rows), len(rows)):
        row = rows[index]
        positions.setdefault(row.get("venue_key", "").strip(), []).append(index)

    transformed: set[int] = set()
    for item in census_rows:
        if not isinstance(item, dict):
            return reject("phase0_venue_census_row_invalid")
        frozen_key = str(item.get("venue_key") or "").strip()
        classification = str(item.get("classification") or "").strip()
        current_key = str(item.get("target_venue_key") or frozen_key).strip()
        if (
            not frozen_key
            or not current_key
            or classification not in {
                "SAFE_REPRESENTATION_REUSE", "NEW_GLOBAL_IDENTITY",
            }
        ):
            return reject("phase0_venue_census_row_unsupported")
        matches = positions.get(current_key, [])
        if len(matches) != 1 or matches[0] in transformed:
            return reject("phase0_venue_row_not_unique")
        index = matches[0]
        transformed.add(index)

        expected_id = registry.get(current_key, "")
        census_target_id = str(item.get("target_venue_id") or "").strip()
        if (
            not re.fullmatch(r"VEN-[0-9]{6}", expected_id)
            or (census_target_id and census_target_id != expected_id)
            or (
                classification == "SAFE_REPRESENTATION_REUSE"
                and census_target_id != expected_id
            )
        ):
            return reject("phase0_venue_id_authority_mismatch")
        row = rows[index]
        if row.get("venue_id", "").strip() != expected_id:
            return reject("phase0_venue_id_mutation_invalid")
        suffix = PHASE0_VENUE_SUFFIX.format(venue_id=expected_id)
        notes = row.get("notes", "")
        if not notes.endswith(suffix):
            return reject("phase0_venue_note_suffix_invalid")
        row["venue_key"] = frozen_key
        row["venue_id"] = ""
        row["notes"] = notes[:-len(suffix)]

    if len(transformed) != len(census_rows):
        return reject("phase0_venue_transform_population_mismatch")
    reconstructed = _csv_bytes(
        fields, rows, bom=phase0_venues.startswith(b"\xef\xbb\xbf")
    )
    if _sha(reconstructed) != freeze_venue_sha256:
        return reject("phase0_frozen_venue_bytes_mismatch")
    return True


def _phase0_commit_identity(
    root: Path,
    school: str,
    phase0_commit: str,
    integration_freeze: dict[str, Any],
    *,
    diagnostics: list[str] | None = None,
) -> bool:
    def reject(reason: str) -> bool:
        if diagnostics is not None:
            diagnostics.append(reason)
        return False

    integration_base = str(integration_freeze.get("integration_base_sha") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", integration_base):
        return reject("phase0_integration_base_invalid")
    lineage = _git(root, "rev-list", "--parents", "-n", "1", phase0_commit)
    if lineage is None:
        return reject("phase0_lineage_unavailable")
    parts = lineage.decode().split()
    if len(parts) != 2 or parts[0] != phase0_commit or parts[1] != integration_base:
        return reject("phase0_integration_base_mismatch")
    message = _git(root, "show", "-s", "--format=%s", phase0_commit)
    if message is None or message.decode().strip() != (
        f"Stage {school} all-history expansion Phase 0"
    ):
        return reject("phase0_commit_message_invalid")
    return True


def _reconstruct_frozen_opponent_display(
    root: Path,
    school: str,
    projected_package: dict[str, bytes],
    freeze_hashes: dict[str, str],
    integration_freeze: dict[str, Any],
    *,
    diagnostics: list[str] | None = None,
) -> bool:
    def reject(reason: str) -> bool:
        if diagnostics is not None:
            diagnostics.append(reason)
        return False

    meta = integration_freeze.get("opponent_display_reconciliation")
    meta_sha = str(
        integration_freeze.get("opponent_display_reconciliation_sha256") or ""
    )
    if not isinstance(meta, dict) or not re.fullmatch(r"[0-9a-f]{64}", meta_sha):
        return reject("phase0_display_authority_missing")
    if meta.get("spec_sha256") != meta_sha:
        return reject("phase0_display_authority_hash_mismatch")

    projected_hashes = meta.get("projected_candidate_sha256")
    pre_hashes = meta.get("pre_candidate_sha256")
    if (
        not isinstance(projected_hashes, dict)
        or not isinstance(pre_hashes, dict)
        or set(projected_hashes) != set(DISPLAY_COLUMNS)
        or set(pre_hashes) != set(DISPLAY_COLUMNS)
    ):
        return reject("phase0_display_hash_population_invalid")

    proof = meta.get("field_level_proof")
    if not isinstance(proof, dict):
        return reject("phase0_display_field_proof_missing")
    for field in (
        "literal_evidence_changes",
        "opponent_key_changes",
        "source_game_key_changes",
        "source_game_non_name_field_changes",
        "current_d1_changes",
    ):
        if int(proof.get(field, -1)) != 0:
            return reject("phase0_display_nonrepresentation_delta")

    working: dict[str, tuple[list[str], list[dict[str, str]], bool, str]] = {}
    for name in DISPLAY_COLUMNS:
        data = projected_package[name]
        if _sha(data) != projected_hashes.get(name):
            return reject("phase0_display_projected_hash_mismatch:" + name)
        fields, rows = _rows(data)
        working[name] = (
            fields,
            rows,
            data.startswith(b"\xef\xbb\xbf"),
            "\r\n" if b"\r\n" in data else "\n",
        )

    opponent_changes = meta.get("opponent_changes")
    source_changes = meta.get("source_game_changes")
    if not isinstance(opponent_changes, list) or not isinstance(source_changes, list):
        return reject("phase0_display_change_population_invalid")

    opp_fields, opp_rows, opp_bom, opp_eol = working["opponents.csv"]
    if "canonical_opponent_name" not in opp_fields:
        return reject("phase0_display_opponent_column_missing")
    changed_keys: set[str] = set()
    for change in opponent_changes:
        if not isinstance(change, dict):
            return reject("phase0_display_opponent_change_invalid")
        line = change.get("line")
        if not isinstance(line, int) or line < 2 or line - 2 >= len(opp_rows):
            return reject("phase0_display_opponent_line_invalid")
        row = opp_rows[line - 2]
        key = str(change.get("canonical_opponent_key") or "").strip()
        if (
            row.get("canonical_opponent_key", "").strip() != key
            or row.get("source_opponent_label", "")
            != str(change.get("source_opponent_label") or "")
            or row.get("canonical_opponent_name", "")
            != str(change.get("to_name") or "")
        ):
            return reject("phase0_display_opponent_change_mismatch")
        row["canonical_opponent_name"] = str(change.get("from_name") or "")
        changed_keys.add(key)

    src_fields, src_rows, src_bom, src_eol = working["source-games.csv"]
    if "normalized_opponent_name" not in src_fields:
        return reject("phase0_display_source_column_missing")
    for change in source_changes:
        if not isinstance(change, dict):
            return reject("phase0_display_source_change_invalid")
        line = change.get("line")
        if not isinstance(line, int) or line < 2 or line - 2 >= len(src_rows):
            return reject("phase0_display_source_line_invalid")
        row = src_rows[line - 2]
        if (
            row.get("source_game_id", "")
            != str(change.get("source_game_id") or "")
            or row.get("normalized_opponent_key", "").strip()
            != str(change.get("normalized_opponent_key") or "").strip()
            or row.get("normalized_opponent_name", "")
            != str(change.get("to_name") or "")
        ):
            return reject("phase0_display_source_change_mismatch")
        row["normalized_opponent_name"] = str(change.get("from_name") or "")

    reconstructed_opponents = _csv_bytes(
        opp_fields, opp_rows, bom=opp_bom, line_ending=opp_eol
    )
    reconstructed_sources = _csv_bytes(
        src_fields, src_rows, bom=src_bom, line_ending=src_eol
    )
    for name, data in (
        ("opponents.csv", reconstructed_opponents),
        ("source-games.csv", reconstructed_sources),
    ):
        if _sha(data) != freeze_hashes[name] or _sha(data) != pre_hashes.get(name):
            return reject("phase0_display_frozen_bytes_mismatch:" + name)

    declared_keys = sorted(str(x) for x in meta.get("changed_keys") or [])
    if sorted(changed_keys) != declared_keys or proof.get("changed_keys") != declared_keys:
        return reject("phase0_display_changed_key_population_mismatch")

    try:
        registered = normalization.project_program_keys(root)
        established = normalization.authority_names_by_key(
            root, school, program_keys=registered,
        )
    except (OSError, ValueError, KeyError):
        return reject("phase0_display_identity_authority_unavailable")

    final_names: dict[str, str] = {}
    _, final_opp_rows = _rows(projected_package["opponents.csv"])
    for row in final_opp_rows:
        key = row.get("canonical_opponent_key", "").strip()
        if key not in changed_keys:
            continue
        name = row.get("canonical_opponent_name", "").strip()
        if not name or key in registered:
            return reject("phase0_display_final_key_invalid")
        if key in final_names and final_names[key] != name:
            return reject("phase0_display_final_name_not_unique")
        final_names[key] = name

    for key, name in final_names.items():
        signatures = {
            normalization.build_site_data.normalized_name_signature(value)
            for value in established.get(key, ())
            if normalization.build_site_data.normalized_name_signature(value)
        }
        if (
            len(signatures) != 1
            or normalization.build_site_data.normalized_name_signature(name)
            not in signatures
        ):
            return reject("phase0_display_established_identity_mismatch")

    _, final_source_rows = _rows(projected_package["source-games.csv"])
    for row in final_source_rows:
        key = row.get("normalized_opponent_key", "").strip()
        if key in changed_keys and row.get("normalized_opponent_name", "") != final_names.get(
            key, ""
        ):
            return reject("phase0_display_source_not_aligned")
    return True


def _phase0_package_matches_frozen_authority(
    root: Path,
    school: str,
    phase0_commit: str,
    package: dict[str, bytes],
    freeze_hashes: dict[str, str],
    integration_freeze: dict[str, Any],
    *,
    diagnostics: list[str] | None = None,
) -> bool:
    def reject(reason: str) -> bool:
        if diagnostics is not None:
            diagnostics.append(reason)
        return False

    if not _phase0_commit_identity(
        root,
        school,
        phase0_commit,
        integration_freeze,
        diagnostics=diagnostics,
    ):
        return False

    display_meta = integration_freeze.get("opponent_display_reconciliation")
    for name in PACKAGE_NAMES:
        if name in DISPLAY_COLUMNS or name == "venues.csv":
            continue
        if _sha(package[name]) != freeze_hashes[name]:
            return reject("phase0_nonrepresentation_package_mismatch:" + name)

    if display_meta is None:
        if any(
            _sha(package[name]) != freeze_hashes[name]
            for name in DISPLAY_COLUMNS
        ):
            return reject("phase0_unbound_display_package_mismatch")
    else:
        if not _reconstruct_frozen_opponent_display(
            root,
            school,
            package,
            freeze_hashes,
            integration_freeze,
            diagnostics=diagnostics,
        ):
            return False

    if _sha(package["venues.csv"]) != freeze_hashes["venues.csv"]:
        if not _reconstruct_frozen_venues(
            root,
            school,
            phase0_commit,
            package["venues.csv"],
            freeze_hashes["venues.csv"],
            integration_freeze,
            diagnostics=diagnostics,
        ):
            return False
    return True


def permits_authenticated_display_successor(
    root: Path,
    school: str,
    freeze_hashes: dict[str, str],
    *,
    integration_freeze: dict[str, Any] | None = None,
    diagnostics: list[str] | None = None,
) -> bool:
    """Prove the exact Phase0-venue + display-successor composition.

    Package-preserving current-main merges may occur before or after the one
    display normalization commit.  The normalization predecessor may either be
    the exact original six-file Freeze, or an exact expansion Phase-0 successor
    whose only package difference is a venue representation transition that can
    be mechanically reversed from the frozen venue census to byte-identical
    frozen venues.csv.  No historical/source meaning may change.
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
    try:
        current = {name: (school_dir / name).read_bytes() for name in PACKAGE_NAMES}
    except OSError:
        return reject("school_package_unavailable")
    changed = {name for name in PACKAGE_NAMES if _sha(current[name]) != freeze_hashes[name]}
    permitted_changed = set(DISPLAY_COLUMNS) | {"venues.csv"}
    if not changed or not changed.issubset(permitted_changed):
        return reject("changed_file_scope_invalid")
    if "opponents.csv" not in changed:
        return reject("opponents_unchanged")

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

    # A pre-Phase0 display reconciliation is already representation authority.
    # If no later package-changing normalization exists, accept the exact
    # authenticated Phase-0 composition directly after stripping only
    # package-preserving first-parent commits.
    if integration_freeze is not None and integration_freeze.get(
        "opponent_display_reconciliation"
    ) is not None:
        phase0_cursor = cursor
        for _ in range(12):
            preserving_parent = _package_preserving_first_parent(
                root, phase0_cursor, school
            )
            if preserving_parent is None:
                break
            phase0_cursor = preserving_parent
        else:
            return reject("phase0_lineage_depth_limit")
        phase0_package = _package(root, phase0_cursor, school)
        if phase0_package is not None and _phase0_package_matches_frozen_authority(
            root,
            school,
            phase0_cursor,
            phase0_package,
            freeze_hashes,
            integration_freeze,
            diagnostics=diagnostics,
        ):
            return True

    normalization_commit = ""
    normalization_parent = ""
    for _ in range(12):
        preserving_parent = _package_preserving_first_parent(root, cursor, school)
        if preserving_parent is not None:
            cursor = preserving_parent
            continue
        lineage = _git(root, "rev-list", "--parents", "-n", "1", cursor)
        if lineage is None:
            return reject("lineage_unavailable")
        parts = lineage.decode().split()
        if len(parts) != 2 or parts[0] != cursor:
            return reject("nonlinear_or_missing_normalization_parent")
        message = _git(root, "show", "-s", "--format=%s", cursor)
        if message is None or message.decode().strip() != (
            f"Normalize {school} historical opponent display representation"
        ):
            return reject("unexpected_normalization_commit_message")
        normalization_commit = cursor
        normalization_parent = parts[1]
        break
    if not normalization_commit:
        return reject("lineage_depth_limit")

    paths = _git(root, "diff", "--name-only", normalization_parent, normalization_commit)
    if paths is None:
        return reject("git_diff_unavailable")
    permitted_paths = {f"schools/{school}/{name}" for name in DISPLAY_COLUMNS}
    actual_paths = set(paths.decode().splitlines())
    if not actual_paths or not actual_paths.issubset(permitted_paths):
        return reject("normalization_changed_extra_path")

    base_cursor = normalization_parent
    for _ in range(12):
        preserving_parent = _package_preserving_first_parent(root, base_cursor, school)
        if preserving_parent is None:
            break
        base_cursor = preserving_parent
    else:
        return reject("pre_normalization_lineage_depth_limit")
    original = _package(root, base_cursor, school)
    if original is None:
        return reject("normalization_predecessor_package_unavailable")

    if integration_freeze is None:
        return reject("phase0_authority_missing")
    if not _phase0_package_matches_frozen_authority(
        root,
        school,
        base_cursor,
        original,
        freeze_hashes,
        integration_freeze,
        diagnostics=diagnostics,
    ):
        return False

    opponent_changes = _opponent_representation_changes(
        original["opponents.csv"], current["opponents.csv"],
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
        if not key:
            return reject("opponent_representation_key_missing")

        if old.get("canonical_opponent_name", "") == new.get(
            "canonical_opponent_name", ""
        ):
            continue

        new_name = new.get("canonical_opponent_name", "").strip()
        if not new_name or key in registered:
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

    for old, new in source_changes:
        key = new.get("normalized_opponent_key", "").strip()
        if key not in final_name_by_key or (
            new.get("normalized_opponent_name") != final_name_by_key[key]
        ):
            return reject("source_name_outside_changed_keys")
    _, source_after = _rows(current["source-games.csv"])
    for new in source_after:
        key = new.get("normalized_opponent_key", "").strip()
        if key in final_name_by_key and (
            new.get("normalized_opponent_name") != final_name_by_key[key]
        ):
            return reject("changed_key_source_not_aligned")
    return True
