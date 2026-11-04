#!/usr/bin/env python3
"""Authenticate frozen per-source-game venue split authority for runtime use.

This module is dependency-neutral so both Stage 2 planning and ingestion/apply can
consume the exact same Integration-Freeze authority without creating import cycles.
It never infers venue identity. It only authenticates already-frozen per-game split
assignments against the current source semantic snapshot and frozen venues.csv bytes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


class FrozenVenueSplitAuthorityError(ValueError):
    """The Integration Freeze venue-split authority is missing trust invariants."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _snapshot_sha256(snapshot: dict[str, Any]) -> str:
    payload = json.dumps(
        snapshot,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _current_snapshot_from_template(
    source_games_path: Path,
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    fields = snapshot.get("fields")
    rows = snapshot.get("rows")
    if (
        snapshot.get("schema_version") != 1
        or not isinstance(fields, list)
        or any(not isinstance(field, str) or not field for field in fields)
        or not isinstance(rows, dict)
    ):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority lacks semantic guard"
        )
    if not source_games_path.is_file():
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority does not match current source semantics"
        )

    with source_games_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if "source_game_id" not in set(reader.fieldnames or []):
            raise FrozenVenueSplitAuthorityError(
                "Integration Freeze venue split authority does not match current source semantics"
            )
        current_rows: dict[str, dict[str, str]] = {}
        for row in reader:
            source_id = row.get("source_game_id", "").strip()
            if not source_id or source_id in current_rows:
                raise FrozenVenueSplitAuthorityError(
                    "Integration Freeze venue split authority does not match current source semantics"
                )
            current_rows[source_id] = {
                field: row.get(field, "")
                for field in fields
            }

    return {
        "schema_version": 1,
        "fields": list(fields),
        "rows": current_rows,
    }


def authenticated_frozen_venue_split_authority(
    repo: Path,
    school_key: str,
) -> tuple[dict[str, dict[str, str]], bytes | None]:
    """Return exact frozen split assignments and their authenticated manifest bytes.

    A missing Integration Freeze is equivalent to no split authority. If a manifest
    exists, all trust invariants used by Stage 2 planning must pass before any
    authority is returned or transported into a disposable runtime copy.
    """

    manifest_path = repo / ".onboarding" / school_key / "integration-freeze.json"
    if not manifest_path.is_file():
        return {}, None

    try:
        payload = manifest_path.read_bytes()
        manifest = json.loads(payload)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FrozenVenueSplitAuthorityError(
            "cannot read Integration Freeze venue split authority"
        ) from exc

    if not isinstance(manifest, dict):
        raise FrozenVenueSplitAuthorityError(
            "cannot read Integration Freeze venue split authority"
        )
    if (
        manifest.get("status") != "INTEGRATION_FROZEN"
        or manifest.get("school_key") != school_key
    ):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority identity mismatch"
        )

    guard = manifest.get("source_game_semantic_guard")
    if not isinstance(guard, dict) or not isinstance(guard.get("snapshot"), dict):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority lacks semantic guard"
        )
    snapshot = guard["snapshot"]
    expected_semantic_hash = str(guard.get("snapshot_sha256", "")).strip()
    current_snapshot = _current_snapshot_from_template(
        repo / "schools" / school_key / "source-games.csv",
        snapshot,
    )
    if (
        not expected_semantic_hash
        or _snapshot_sha256(snapshot) != expected_semantic_hash
        or current_snapshot != snapshot
    ):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority does not match current source semantics"
        )

    package_hashes = manifest.get("package_member_sha256")
    expected_venues_hash = (
        str(package_hashes.get("venues.csv", "")).strip()
        if isinstance(package_hashes, dict)
        else ""
    )
    venues_path = repo / "schools" / school_key / "venues.csv"
    if (
        not re.fullmatch(r"[0-9a-f]{64}", expected_venues_hash)
        or not venues_path.is_file()
        or _sha256_file(venues_path) != expected_venues_hash
    ):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority does not match current venues.csv"
        )

    reconciliation = manifest.get("venue_reconciliation")
    if not isinstance(reconciliation, dict):
        return {}, payload
    mappings = reconciliation.get("mappings")
    if not isinstance(mappings, list):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue reconciliation mappings are invalid"
        )

    snapshot_rows = snapshot.get("rows")
    if not isinstance(snapshot_rows, dict):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze semantic snapshot rows are invalid"
        )

    authority: dict[str, dict[str, str]] = {}
    for mapping in mappings:
        if not isinstance(mapping, dict):
            raise FrozenVenueSplitAuthorityError(
                "Integration Freeze venue reconciliation row is invalid"
            )
        if mapping.get("action") != "SPLIT_LOCAL_ROW_BY_CUTOVER":
            continue

        venue_name = str(mapping.get("expected_local_name", "")).strip()
        targets = mapping.get("split_targets")
        if not venue_name or not isinstance(targets, list) or not targets:
            raise FrozenVenueSplitAuthorityError(
                "frozen venue cutover split is incomplete"
            )

        assigned_count = 0
        for target in targets:
            if not isinstance(target, dict):
                raise FrozenVenueSplitAuthorityError(
                    "frozen venue cutover target is invalid"
                )
            venue_id = str(target.get("global_venue_id", "")).strip()
            venue_key = str(target.get("global_venue_key", "")).strip()
            source_ids = target.get("source_game_ids")
            if not venue_id or not venue_key or not isinstance(source_ids, list):
                raise FrozenVenueSplitAuthorityError(
                    "frozen venue cutover target is incomplete"
                )

            clean_ids = [str(value).strip() for value in source_ids]
            if (
                any(not value for value in clean_ids)
                or len(set(clean_ids)) != len(clean_ids)
            ):
                raise FrozenVenueSplitAuthorityError(
                    "frozen venue cutover source-game population is invalid"
                )
            declared = str(target.get("games_currently_assigned", "")).strip()
            if not declared.isdigit() or int(declared) != len(clean_ids):
                raise FrozenVenueSplitAuthorityError(
                    "frozen venue cutover target count mismatch"
                )

            for source_id in clean_ids:
                semantic_row = snapshot_rows.get(source_id)
                if not isinstance(semantic_row, dict):
                    raise FrozenVenueSplitAuthorityError(
                        f"frozen venue cutover references unknown source game {source_id}"
                    )
                if (
                    str(semantic_row.get("curated_venue_name", "")).strip().casefold()
                    != venue_name.casefold()
                ):
                    raise FrozenVenueSplitAuthorityError(
                        f"frozen venue cutover source game {source_id} has a different venue"
                    )
                entry = {
                    "venue_id": venue_id,
                    "venue_key": venue_key,
                    "curated_venue_name": venue_name,
                }
                prior = authority.get(source_id)
                if prior is not None and prior != entry:
                    raise FrozenVenueSplitAuthorityError(
                        f"frozen venue cutover assigns source game {source_id} more than once"
                    )
                authority[source_id] = entry
            assigned_count += len(clean_ids)

        declared_total = str(mapping.get("split_source_game_count", "")).strip()
        if not declared_total.isdigit() or int(declared_total) != assigned_count:
            raise FrozenVenueSplitAuthorityError(
                "frozen venue cutover total count mismatch"
            )

    return authority, payload


def load_frozen_venue_split_authority(
    repo: Path,
    school_key: str,
) -> dict[str, dict[str, str]]:
    """Return only authenticated per-game split assignments."""

    authority, _ = authenticated_frozen_venue_split_authority(repo, school_key)
    return authority


def frozen_venue_split_freeze_bytes(
    repo: Path,
    school_key: str,
) -> bytes | None:
    """Return exact manifest bytes only when they carry authenticated split authority."""

    authority, payload = authenticated_frozen_venue_split_authority(repo, school_key)
    return payload if authority else None
