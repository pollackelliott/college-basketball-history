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
    fields: list[str], rows: list[dict[str, str]], *, bom: bool = False,
) -> bytes:
    value = io.StringIO(newline="")
    writer = csv.DictWriter(value, fieldnames=fields, lineterminator="\n")
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
    legacy_no_sidecar = (
        census is None
        and integration_freeze.get("venue_reconciliation") is None
        and integration_freeze.get("venue_reconciliation_sha256") == ""
        and not (root / ".onboarding" / school / "venue-reconciliation.json").exists()
    )
    if not legacy_no_sidecar and (
        not isinstance(census, dict)
        or census.get("schema_version") != 1
        or census.get("blocker_count") != 0
        or not isinstance(census.get("rows"), list)
    ):
        return reject("phase0_venue_census_invalid")

    fields, rows = _rows(phase0_venues)
    if not {"venue_key", "venue_id", "notes"}.issubset(fields):
        return reject("phase0_venue_schema_invalid")
    parent_venues = _blob(root, integration_base, school, "venues.csv")
    if parent_venues is None:
        return reject("phase0_parent_venues_unavailable")
    parent_fields, parent_rows = _rows(parent_venues)
    if parent_fields != fields:
        return reject("phase0_parent_venue_schema_mismatch")
    # Expansion Freeze may legitimately revise published inherited venue
    # chronology or assignment summaries before Phase 0. Those revisions are
    # historical source-package authority, not a post-Freeze mutation. Require
    # stable inherited venue identity/order here; the reconstructed entire-file
    # SHA-256 check below independently authenticates *every* inherited field
    # against the immutable Freeze, and still rejects any unsealed change.
    if [row.get("venue_key") for row in rows[:len(parent_rows)]] != [
        row.get("venue_key") for row in parent_rows
    ]:
        return reject("phase0_inherited_venue_identity_changed")
    registry = _registry_ids_by_key(root, phase0_commit)
    if registry is None:
        return reject("phase0_global_venue_registry_unavailable")

    if legacy_no_sidecar:
        support = integration_freeze.get("venue_support_actions") or {}
        global_counts = integration_freeze.get("global_venue_reconciliation") or {}
        supplemental_count = len(rows) - len(parent_rows)
        # Legacy pre-fix authority: exact automatic registered reuse with no
        # sidecar.  The cap bounds a search over blank/already-assigned IDs.
        if (
            not 1 <= supplemental_count <= 8
            or type(support.get("NEW_SUPPLEMENTAL")) is not int
            or support["NEW_SUPPLEMENTAL"] != supplemental_count
            or type(global_counts.get("REUSE_REGISTERED_GLOBAL_VENUE")) is not int
            or global_counts["REUSE_REGISTERED_GLOBAL_VENUE"] < supplemental_count
            or global_counts.get("NEW_GLOBAL_VENUE_REGISTRATION_REQUIRED") != 0
            or global_counts.get("GLOBAL_VENUE_IDENTITY_REVIEW_BLOCKER") != 0
        ):
            return reject("phase0_legacy_venue_population_invalid")
        census_rows = [
            {
                "venue_key": row.get("venue_key", "").strip(),
                "classification": "SAFE_REPRESENTATION_REUSE",
                "target_venue_key": row.get("venue_key", "").strip(),
                "target_venue_id": registry.get(
                    row.get("venue_key", "").strip(), ""
                ),
            }
            for row in rows[len(parent_rows):]
        ]
    else:
        census_rows = census["rows"]
        if (
            not census_rows
            or census.get("venue_count") != len(census_rows)
            or len(census_rows) != len({
                str(row.get("venue_key") or "").strip() for row in census_rows
            })
        ):
            return reject("phase0_venue_census_population_invalid")

    if len(rows) != len(parent_rows) + len(census_rows):
        return reject("phase0_supplemental_venue_population_mismatch")

    positions: dict[str, list[int]] = {}
    for index in range(len(parent_rows), len(rows)):
        row = rows[index]
        positions.setdefault(row.get("venue_key", "").strip(), []).append(index)

    transformed: set[int] = set()
    legacy_id_options: list[tuple[int, str]] = []
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
            or (legacy_no_sidecar and current_key != frozen_key)
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
        research_id = str(item.get("research_venue_id") or "").strip()
        if not legacy_no_sidecar and research_id not in {"", expected_id}:
            return reject("phase0_frozen_venue_id_invalid")
        row["venue_key"] = frozen_key
        row["venue_id"] = research_id if not legacy_no_sidecar else ""
        row["notes"] = notes[:-len(suffix)]
        if legacy_no_sidecar:
            legacy_id_options.append((index, expected_id))

    if len(transformed) != len(census_rows):
        return reject("phase0_venue_transform_population_mismatch")
    bom = phase0_venues.startswith(b"\xef\xbb\xbf")
    if not legacy_no_sidecar:
        if _sha(_csv_bytes(fields, rows, bom=bom)) != freeze_venue_sha256:
            return reject("phase0_frozen_venue_bytes_mismatch")
        return True

    # The frozen six-file hash certifies all key/name/locality/chronology
    # fields byte-for-byte.  A frozen VEN ID may be blank or already equal
    # to the authoritative registry ID; no other candidate value is legal.
    from itertools import product

    for assignments in product((False, True), repeat=len(legacy_id_options)):
        recovered = [dict(row) for row in rows]
        for (index, venue_id), keep in zip(legacy_id_options, assignments):
            if keep:
                recovered[index]["venue_id"] = venue_id
        if _sha(_csv_bytes(fields, recovered, bom=bom)) == freeze_venue_sha256:
            return True
    return reject("phase0_frozen_venue_bytes_mismatch")


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

    nonvenue = [name for name in PACKAGE_NAMES if name != "venues.csv"]
    if any(_sha(original[name]) != freeze_hashes[name] for name in nonvenue):
        return reject("phase0_nonvenue_package_mismatch")
    if _sha(original["venues.csv"]) != freeze_hashes["venues.csv"]:
        if integration_freeze is None:
            return reject("phase0_venue_authority_missing")
        if not _reconstruct_frozen_venues(
            root,
            school,
            base_cursor,
            original["venues.csv"],
            freeze_hashes["venues.csv"],
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
