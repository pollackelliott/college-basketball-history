"""Explicit, immutable-input-bounded venue reuse for Implementation Stage 1.

A spec only authorizes current-main representation reconciliation; it never
changes global registries or the frozen six-file research portfolio.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

from onboarding_plan import WorkflowError


_ROW_SELECTOR_PREFIX = "__row_index__:"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _row_selector(index: int) -> str:
    return f"{_ROW_SELECTOR_PREFIX}{index}"


def venue_reconciliation_for_row(
    mappings: dict[str, dict[str, str]],
    local: dict[str, str],
    row_index: int,
) -> dict[str, str] | None:
    """Return explicit reconciliation for one frozen venues.csv row.

    Legacy schema-v1 mappings remain keyed by nonblank local venue_key.
    Schema-v2 may instead bind one exact immutable venues.csv data-row index.
    """
    key = local.get("venue_key", "").strip()
    if key and key in mappings:
        return mappings[key]
    return mappings.get(_row_selector(row_index))


def load_venue_reconciliation(
    path: Path | None,
    *,
    school_key: str,
    package_path: Path,
    local_venues: list[dict[str, str]],
    global_venues: list[dict[str, str]],
) -> tuple[dict[str, dict[str, str]], dict[str, Any] | None]:
    """Validate an explicit identity map and return mappings + durable provenance.

    Both the entire transport ZIP and its exact frozen venues.csv member are
    hash-bound, so no operator instruction can apply to a changed Research
    package. Geography and exact ID/key must agree with current main.

    Schema v2 adds row-index selectors for frozen rows whose venue_key is blank
    and a narrowly guarded DROP_REDUNDANT_LOCAL_ROW representation action.
    """
    if path is None:
        return {}, None
    path = path.resolve()
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise WorkflowError(f"cannot read venue reconciliation {path}: {exc}") from exc
    schema_version = doc.get("schema_version")
    if not isinstance(doc, dict) or schema_version not in {1, 2}:
        raise WorkflowError("venue reconciliation schema_version must be 1 or 2")
    if doc.get("school_key") != school_key:
        raise WorkflowError("venue reconciliation school_key mismatch")
    approval = str(doc.get("owner_approval_basis") or "").strip()
    if not approval:
        raise WorkflowError("venue reconciliation requires owner_approval_basis")
    expected_package = str(doc.get("expected_research_zip_sha256") or "").lower().strip()
    actual_package = _sha256_file(package_path)
    if expected_package != actual_package:
        raise WorkflowError("venue reconciliation frozen package SHA-256 mismatch")
    try:
        with zipfile.ZipFile(package_path) as archive:
            member = archive.read("venues.csv")
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        raise WorkflowError(f"venue reconciliation cannot read frozen venues.csv: {exc}") from exc
    expected_venues = str(doc.get("expected_venues_sha256") or "").lower().strip()
    actual_venues = _sha256_bytes(member)
    if expected_venues != actual_venues:
        raise WorkflowError("venue reconciliation frozen venues.csv SHA-256 mismatch")

    raw_mappings = doc.get("mappings")
    if not isinstance(raw_mappings, list) or not raw_mappings:
        raise WorkflowError("venue reconciliation requires nonempty mappings")

    local_by_key: dict[str, list[dict[str, str]]] = {}
    for row in local_venues:
        key = row.get("venue_key", "").strip()
        local_by_key.setdefault(key, []).append(row)
    global_by_id = {
        row.get("venue_id", "").strip(): row for row in global_venues
    }
    global_by_key = {
        row.get("venue_key", "").strip(): row for row in global_venues
    }

    mappings: dict[str, dict[str, str]] = {}
    for number, raw in enumerate(raw_mappings, 1):
        if not isinstance(raw, dict):
            raise WorkflowError(f"venue reconciliation mapping {number} not an object")

        action = str(raw.get("action") or "REUSE_CURRENT_IDENTITY").strip().upper()
        local_key = str(raw.get("local_venue_key") or "").strip()
        raw_row_index = raw.get("local_venue_row_index")
        has_row_index = raw_row_index not in {None, ""}
        if schema_version == 1 and has_row_index:
            raise WorkflowError(
                "venue reconciliation schema_version 1 does not support local_venue_row_index"
            )
        if bool(local_key) == bool(has_row_index):
            raise WorkflowError(
                f"venue reconciliation mapping {number} requires exactly one "
                "local_venue_key or local_venue_row_index"
            )

        row_index: int | None = None
        if has_row_index:
            try:
                row_index = int(str(raw_row_index))
            except (TypeError, ValueError) as exc:
                raise WorkflowError(
                    f"venue reconciliation mapping {number} local_venue_row_index invalid"
                ) from exc
            if row_index < 1 or row_index > len(local_venues):
                raise WorkflowError(
                    f"venue reconciliation mapping {number} local_venue_row_index out of range"
                )
            selector = _row_selector(row_index)
            local_rows = [local_venues[row_index - 1]]
        else:
            selector = local_key
            local_rows = local_by_key.get(local_key) or []
            if not local_rows:
                raise WorkflowError(
                    f"venue reconciliation unknown local key {local_key!r}"
                )

        if selector in mappings:
            raise WorkflowError(
                f"venue reconciliation repeats local selector {selector!r}"
            )

        common_required = (
            "expected_local_name",
            "expected_local_city",
            "expected_local_state",
            "resolution_basis",
        )
        item = {
            "action": action,
            "local_venue_key": local_key,
            "local_venue_row_index": str(row_index or ""),
            **{
                key: str(raw.get(key) or "").strip()
                for key in common_required
            },
        }
        if not all(item[key] for key in common_required):
            raise WorkflowError(
                f"venue reconciliation mapping {number} missing required field"
            )

        if any(
            local.get("source_program_key", "").strip() != school_key
            for local in local_rows
        ):
            raise WorkflowError(
                f"venue reconciliation school mismatch for {selector!r}"
            )
        local_names = {
            local.get("canonical_name", "").strip() for local in local_rows
        }
        if (
            item["expected_local_name"] not in local_names
            or any(
                local.get("city", "").strip() != item["expected_local_city"]
                or local.get("state", "").strip() != item["expected_local_state"]
                for local in local_rows
            )
        ):
            raise WorkflowError(
                f"venue reconciliation frozen local identity drift for {selector!r}"
            )

        if action == "DROP_REDUNDANT_LOCAL_ROW":
            if row_index is None:
                raise WorkflowError(
                    "DROP_REDUNDANT_LOCAL_ROW requires local_venue_row_index"
                )
            local = local_rows[0]
            if local.get("venue_key", "").strip():
                raise WorkflowError(
                    "DROP_REDUNDANT_LOCAL_ROW is limited to blank-key frozen rows"
                )
            retained = [
                other
                for index, other in enumerate(local_venues, 1)
                if index != row_index
                and other.get("venue_key", "").strip()
                and other.get("canonical_name", "").strip()
                == item["expected_local_name"]
                and other.get("city", "").strip()
                == item["expected_local_city"]
                and other.get("state", "").strip()
                == item["expected_local_state"]
            ]
            if not retained:
                raise WorkflowError(
                    "DROP_REDUNDANT_LOCAL_ROW requires a retained keyed row "
                    "with the same frozen name/geography"
                )
            item["retained_local_keys"] = ";".join(
                sorted({row.get("venue_key", "").strip() for row in retained})
            )
            mappings[selector] = item
            continue

        if action != "REUSE_CURRENT_IDENTITY":
            raise WorkflowError(
                f"venue reconciliation mapping {number} unsupported action {action!r}"
            )

        target_required = (
            "global_venue_id",
            "global_venue_key",
            "expected_global_city",
            "expected_global_state",
        )
        item.update({
            key: str(raw.get(key) or "").strip()
            for key in target_required
        })
        if not all(item[key] for key in target_required):
            raise WorkflowError(
                f"venue reconciliation mapping {number} missing required field"
            )

        target_id = item["global_venue_id"]
        target = global_by_id.get(target_id)
        if (
            target is None
            or target.get("venue_key", "").strip() != item["global_venue_key"]
            or global_by_key.get(item["global_venue_key"]) is not target
        ):
            raise WorkflowError(
                f"venue reconciliation stale global venue ID/key for {selector!r}"
            )
        if (
            target.get("city", "").strip() != item["expected_global_city"]
            or target.get("state", "").strip() != item["expected_global_state"]
            or item["expected_local_city"].casefold()
            != item["expected_global_city"].casefold()
            or item["expected_local_state"].upper()
            != item["expected_global_state"].upper()
        ):
            raise WorkflowError(
                f"venue reconciliation global geography mismatch for {selector!r}"
            )
        mappings[selector] = item

    metadata = {
        "schema_version": schema_version,
        "spec_path": str(path),
        "spec_sha256": _sha256_file(path),
        "owner_approval_basis": approval,
        "research_zip_sha256": actual_package,
        "frozen_venues_sha256": actual_venues,
        "mappings": list(mappings.values()),
    }
    return mappings, metadata
