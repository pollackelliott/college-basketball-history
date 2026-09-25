"""Stage 1 target-school reference reconciliation helpers.

This module handles owner-authorized conference-history corrections and safe
current-main conference registrations without mutating the frozen transport
artifact.  The correction specification is external input to Stage 1; the
corrected school package and Integration Freeze manifest become the durable
representation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from onboarding_plan import WorkflowError


CONFERENCE_HISTORY_FIELDS = [
    "source_program_key",
    "start_season",
    "end_season",
    "conference_key",
    "conference_name",
    "membership_type",
    "ongoing",
    "basis",
    "notes",
]

CONFERENCE_REGISTRY_FIELDS = [
    "conference_key",
    "conference_name",
    "tournament_label",
    "status",
    "notes",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_conference_reconciliation(
    path: Path | None,
    *,
    school_key: str,
    conferences_path: Path,
    local_fields: list[str],
) -> tuple[list[dict[str, str]] | None, list[dict[str, str]], dict[str, Any] | None]:
    """Load and validate an optional owner-authorized Stage 1 conference correction."""

    if path is None:
        return None, [], None

    path = path.resolve()
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"cannot read conference reconciliation {path}: {exc}") from exc

    if document.get("schema_version") != 1:
        raise WorkflowError("conference reconciliation schema_version must be 1")
    if document.get("school_key") != school_key:
        raise WorkflowError(
            "conference reconciliation school_key mismatch: "
            f"expected {school_key!r}, found {document.get('school_key')!r}"
        )
    if not str(document.get("owner_approval_basis", "")).strip():
        raise WorkflowError("conference reconciliation requires owner_approval_basis")

    expected_hash = str(document.get("expected_conferences_sha256", "")).strip().lower()
    actual_hash = sha256_file(conferences_path).lower()
    if not expected_hash or actual_hash != expected_hash:
        raise WorkflowError(
            "conference reconciliation frozen conferences.csv hash mismatch: "
            f"expected {expected_hash or '[missing]'}, found {actual_hash}"
        )

    replacement = document.get("replacement_history")
    if not isinstance(replacement, list) or not replacement:
        raise WorkflowError("conference reconciliation requires replacement_history")

    if set(local_fields) != set(CONFERENCE_HISTORY_FIELDS):
        raise WorkflowError(
            "conference reconciliation requires the standard conferences.csv schema; "
            f"found {local_fields}"
        )

    replacement_rows: list[dict[str, str]] = []
    for index, raw in enumerate(replacement, start=1):
        if not isinstance(raw, dict):
            raise WorkflowError(
                f"conference reconciliation replacement_history row {index} is not an object"
            )
        row = {field: str(raw.get(field, "")) for field in local_fields}
        if row["source_program_key"].strip() != school_key:
            raise WorkflowError(
                f"conference reconciliation replacement row {index} source_program_key "
                f"must be {school_key!r}"
            )
        if not row["conference_key"].strip() or not row["conference_name"].strip():
            raise WorkflowError(
                f"conference reconciliation replacement row {index} requires "
                "conference_key and conference_name"
            )
        replacement_rows.append(row)

    registrations_raw = document.get("registrations", [])
    if not isinstance(registrations_raw, list):
        raise WorkflowError("conference reconciliation registrations must be a list")

    registrations: list[dict[str, str]] = []
    registration_keys: set[str] = set()
    for index, raw in enumerate(registrations_raw, start=1):
        if not isinstance(raw, dict):
            raise WorkflowError(
                f"conference reconciliation registration {index} is not an object"
            )
        row = {field: str(raw.get(field, "")).strip() for field in CONFERENCE_REGISTRY_FIELDS}
        key = row["conference_key"]
        if not key or not row["conference_name"] or not row["status"]:
            raise WorkflowError(
                f"conference reconciliation registration {index} requires "
                "conference_key, conference_name, and status"
            )
        if key != "independent" and not row["tournament_label"]:
            raise WorkflowError(
                f"conference reconciliation registration {key!r} requires "
                "an owner-approved tournament_label"
            )
        if key in registration_keys:
            raise WorkflowError(
                f"conference reconciliation repeats registration key {key!r}"
            )
        registration_keys.add(key)
        registrations.append(row)

    replacement_keys = {
        row["conference_key"].strip()
        for row in replacement_rows
        if row["conference_key"].strip()
    }
    unused = sorted(registration_keys - replacement_keys)
    if unused:
        raise WorkflowError(
            "conference reconciliation contains registrations not used by replacement "
            "history: " + ", ".join(unused)
        )

    metadata = {
        "spec_path": str(path),
        "spec_sha256": sha256_file(path),
        "frozen_conferences_sha256": actual_hash,
        "owner_approval_basis": str(document["owner_approval_basis"]).strip(),
        "replacement_row_count": len(replacement_rows),
        "registration_count": len(registrations),
    }
    return replacement_rows, registrations, metadata


def conference_reconciliation_inventory(
    local_rows: list[dict[str, str]],
    global_rows: list[dict[str, str]],
    registrations: list[dict[str, str]],
) -> dict[str, Any]:
    """Inventory target conference-key reuse/new registrations before mutation."""

    global_by_key = {
        row.get("conference_key", "").strip(): row
        for row in global_rows
        if row.get("conference_key", "").strip()
    }
    registration_by_key = {
        row.get("conference_key", "").strip(): row
        for row in registrations
        if row.get("conference_key", "").strip()
    }

    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for local in local_rows:
        key = local.get("conference_key", "").strip()
        if not key or key in seen:
            continue
        seen.add(key)

        item: dict[str, Any] = {
            "conference_key": key,
            "conference_name": local.get("conference_name", "").strip(),
            "classification": "",
            "issues": [],
        }
        if key in global_by_key:
            item["classification"] = "REUSE_CURRENT_IDENTITY"
        elif key in registration_by_key:
            item["classification"] = "NEW_GLOBAL_IDENTITY"
            registered_name = registration_by_key[key].get("conference_name", "").strip()
            local_name = item["conference_name"]
            if (
                registered_name
                and local_name
                and registered_name.casefold() != local_name.casefold()
            ):
                item["classification"] = "STOP_AMBIGUOUS"
                item["issues"].append("REGISTRATION_NAME_CONFLICT")
        else:
            item["classification"] = "STOP_AMBIGUOUS"
            item["issues"].append("MISSING_GLOBAL_CONFERENCE_REGISTRATION")
        results.append(item)

    counts: dict[str, int] = {}
    for row in results:
        classification = row["classification"]
        counts[classification] = counts.get(classification, 0) + 1
    blockers = [row for row in results if row["classification"] == "STOP_AMBIGUOUS"]
    return {
        "schema_version": 1,
        "row_count": len(results),
        "classification_counts": dict(sorted(counts.items())),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "rows": results,
    }


def register_conferences(
    global_rows: list[dict[str, str]],
    registrations: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Apply only missing, exact conference registrations to current-main rows."""

    by_key = {
        row.get("conference_key", "").strip(): row
        for row in global_rows
        if row.get("conference_key", "").strip()
    }
    mappings: list[dict[str, str]] = []

    for registration in registrations:
        key = registration["conference_key"]
        existing = by_key.get(key)
        if existing is not None:
            mismatches = [
                field
                for field in ("conference_name", "tournament_label", "status")
                if existing.get(field, "").strip()
                != registration.get(field, "").strip()
            ]
            if mismatches:
                raise WorkflowError(
                    f"conference registration {key!r} conflicts with current main "
                    f"on {', '.join(mismatches)}"
                )
            mappings.append(
                {
                    "conference_key": key,
                    "resolution": "REUSE_CURRENT_IDENTITY",
                }
            )
            continue

        row = {field: registration.get(field, "") for field in CONFERENCE_REGISTRY_FIELDS}
        global_rows.append(row)
        by_key[key] = row
        mappings.append(
            {
                "conference_key": key,
                "resolution": "NEW_GLOBAL_IDENTITY",
            }
        )

    return global_rows, mappings
