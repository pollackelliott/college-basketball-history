"""Explicit, immutable-input-bounded venue reuse for Implementation Stage 1.

A spec only authorizes reuse of an existing global physical-venue identity; it
never changes global registries or the frozen six-file research portfolio.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

from onboarding_plan import WorkflowError


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


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
    """
    if path is None:
        return {}, None
    path = path.resolve()
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise WorkflowError(f"cannot read venue reconciliation {path}: {exc}") from exc
    if not isinstance(doc, dict) or doc.get("schema_version") != 1:
        raise WorkflowError("venue reconciliation schema_version must be 1")
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

    local_by_key = {}
    for row in local_venues:
        key = row.get("venue_key", "").strip()
        if key in local_by_key:
            raise WorkflowError(f"venue reconciliation duplicate frozen local key {key!r}")
        local_by_key[key] = row
    global_by_id = {
        row.get("venue_id", "").strip(): row for row in global_venues
    }
    global_by_key = {
        row.get("venue_key", "").strip(): row for row in global_venues
    }
    mappings: dict[str, dict[str, str]] = {}
    used_target_ids: set[str] = set()
    for number, raw in enumerate(raw_mappings, 1):
        if not isinstance(raw, dict):
            raise WorkflowError(f"venue reconciliation mapping {number} not an object")
        required = (
            "local_venue_key", "expected_local_name", "expected_local_city",
            "expected_local_state", "global_venue_id", "global_venue_key",
            "expected_global_city", "expected_global_state", "resolution_basis",
        )
        item = {key: str(raw.get(key) or "").strip() for key in required}
        if not all(item.values()):
            raise WorkflowError(f"venue reconciliation mapping {number} missing required field")
        key = item["local_venue_key"]
        if key in mappings:
            raise WorkflowError(f"venue reconciliation repeats local key {key!r}")
        local = local_by_key.get(key)
        if local is None:
            raise WorkflowError(f"venue reconciliation unknown local key {key!r}")
        if local.get("source_program_key", "").strip() != school_key:
            raise WorkflowError(f"venue reconciliation school mismatch for {key!r}")
        if (local.get("canonical_name", "").strip() != item["expected_local_name"]
            or local.get("city", "").strip() != item["expected_local_city"]
            or local.get("state", "").strip() != item["expected_local_state"]):
            raise WorkflowError(f"venue reconciliation frozen local identity drift for {key!r}")
        target_id = item["global_venue_id"]
        target = global_by_id.get(target_id)
        if (target is None
            or target.get("venue_key", "").strip() != item["global_venue_key"]
            or global_by_key.get(item["global_venue_key"]) is not target):
            raise WorkflowError(f"venue reconciliation stale global venue ID/key for {key!r}")
        if (target.get("city", "").strip() != item["expected_global_city"]
            or target.get("state", "").strip() != item["expected_global_state"]
            or item["expected_local_city"].casefold() != item["expected_global_city"].casefold()
            or item["expected_local_state"].upper() != item["expected_global_state"].upper()):
            raise WorkflowError(f"venue reconciliation global geography mismatch for {key!r}")
        if target_id in used_target_ids:
            raise WorkflowError(f"venue reconciliation target ID repeated: {target_id}")
        used_target_ids.add(target_id)
        mappings[key] = item

    metadata = {
        "schema_version": 1,
        "spec_path": str(path),
        "spec_sha256": _sha256_file(path),
        "owner_approval_basis": approval,
        "research_zip_sha256": actual_package,
        "frozen_venues_sha256": actual_venues,
        "mappings": list(mappings.values()),
    }
    return mappings, metadata
