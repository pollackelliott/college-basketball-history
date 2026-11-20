#!/usr/bin/env python3
"""Fail-closed Stage 2 compatibility for true zero-game-delta expansions.

This module carries no school-specific authority. It recognizes zero delta only
from an authenticated ALL_HISTORY_EXPANSION Integration Freeze and projects the
ordinary Stage 2 plan by excluding review debt that belongs solely to the
unchanged inherited published baseline.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ZERO_DELTA_EXPANSION_KIND = "ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE"
ZERO_DELTA_STALE_ACCOMPLISHMENT_BLOCKER = (
    "Accomplishment reference has stale EXPLAINED_ADMIN_DIFFERENCE "
    "but the current canonical cross-check no longer differs"
)


class ZeroDeltaExpansionError(RuntimeError):
    """Fail-closed zero-delta compatibility error."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_row_sha256(row: dict[str, str]) -> str:
    payload = (
        json.dumps(
            dict(row),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))




ZERO_DELTA_DISCREPANCY_AUDIT_MARKER = "ZERO_DELTA_DISCREPANCY_AUDIT_JSON="


def normalized_inherited_discrepancies(
    rows: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """Exact historical discrepancy identities, not merely an aggregate count."""

    keys = (
        "source_game_id", "canonical_game_id", "field_name",
        "source_value", "canonical_value",
    )
    normalized: list[dict[str, str]] = []
    identities: set[tuple[str, str, str]] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ZeroDeltaExpansionError("inherited discrepancy audit row is invalid")
        if any(key not in row or not isinstance(row[key], str) for key in keys):
            raise ZeroDeltaExpansionError("inherited discrepancy audit has missing fields")
        item = {key: row[key] for key in keys}
        identity = (
            item["source_game_id"], item["canonical_game_id"], item["field_name"]
        )
        if not all(identity) or identity in identities:
            raise ZeroDeltaExpansionError(
                "inherited discrepancy audit has a blank/duplicate identity"
            )
        identities.add(identity)
        normalized.append(item)
    return sorted(
        normalized,
        key=lambda item: tuple(item[key] for key in keys),
    )

def authenticate_zero_delta_expansion(
    repo: Path,
    school_key: str,
) -> dict[str, Any] | None:
    """Return exact zero-delta authority or None for non-zero/non-expansion lanes."""

    manifest_path = repo / ".onboarding" / school_key / "integration-freeze.json"
    if not manifest_path.is_file():
        return None
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ZeroDeltaExpansionError(
            "cannot read zero-delta expansion Integration Freeze"
        ) from exc
    if manifest.get("kind") != ZERO_DELTA_EXPANSION_KIND:
        return None
    if (
        manifest.get("status") != "INTEGRATION_FROZEN"
        or manifest.get("school_key") != school_key
    ):
        raise ZeroDeltaExpansionError(
            "zero-delta expansion Integration Freeze identity mismatch"
        )

    preservation = manifest.get("source_preservation")
    if not isinstance(preservation, dict):
        raise ZeroDeltaExpansionError(
            "zero-delta expansion Integration Freeze lacks source preservation"
        )
    try:
        inherited_count = int(preservation.get("inherited_count"))
        supplemental_count = int(preservation.get("supplemental_count"))
        combined_count = int(preservation.get("combined_count"))
    except (TypeError, ValueError) as exc:
        raise ZeroDeltaExpansionError(
            "zero-delta expansion source preservation counts are invalid"
        ) from exc
    if supplemental_count != 0:
        return None
    if inherited_count <= 0 or combined_count != inherited_count:
        raise ZeroDeltaExpansionError(
            "zero-delta expansion source preservation population is inconsistent"
        )

    package_hashes = manifest.get("package_member_sha256")
    baseline_hashes = manifest.get("baseline_package_member_sha256")
    if not isinstance(package_hashes, dict) or not isinstance(baseline_hashes, dict):
        raise ZeroDeltaExpansionError(
            "zero-delta expansion package hash authority is missing"
        )
    frozen_source_hash = str(package_hashes.get("source-games.csv", "")).strip()
    baseline_source_hash = str(baseline_hashes.get("source-games.csv", "")).strip()
    source_path = repo / "schools" / school_key / "source-games.csv"
    if (
        not re.fullmatch(r"[0-9a-f]{64}", frozen_source_hash)
        or not re.fullmatch(r"[0-9a-f]{64}", baseline_source_hash)
        or frozen_source_hash != baseline_source_hash
        or not source_path.is_file()
        or _sha256_file(source_path) != frozen_source_hash
    ):
        raise ZeroDeltaExpansionError(
            "zero-delta expansion source-game bytes differ from inherited baseline"
        )

    for label in ("opponent_support_actions", "venue_support_actions"):
        actions = manifest.get(label)
        if not isinstance(actions, dict):
            raise ZeroDeltaExpansionError(
                f"zero-delta expansion {label} authority is missing"
            )
        try:
            nonzero = {
                key: int(value)
                for key, value in actions.items()
                if int(value) != 0
            }
        except (TypeError, ValueError) as exc:
            raise ZeroDeltaExpansionError(
                f"zero-delta expansion {label} counts are invalid"
            ) from exc
        if nonzero:
            raise ZeroDeltaExpansionError(
                f"zero-delta expansion unexpectedly has {label}: {sorted(nonzero)}"
            )

    identity_counts = manifest.get("canonical_identity_counts")
    if not isinstance(identity_counts, dict):
        raise ZeroDeltaExpansionError(
            "zero-delta expansion canonical identity authority is missing"
        )
    try:
        nonzero_identity = {
            key: int(value)
            for key, value in identity_counts.items()
            if int(value) != 0
        }
    except (TypeError, ValueError) as exc:
        raise ZeroDeltaExpansionError(
            "zero-delta expansion canonical identity counts are invalid"
        ) from exc
    if nonzero_identity or list(manifest.get("canonical_reuses") or []):
        raise ZeroDeltaExpansionError(
            "zero-delta expansion unexpectedly carries canonical identity work"
        )
    if int(manifest.get("unresolved_history_decisions", 0) or 0) != 0:
        raise ZeroDeltaExpansionError(
            "zero-delta expansion unexpectedly carries unresolved historical decisions"
        )

    reconciliation = manifest.get("current_main_reconciliation") or {}
    if not isinstance(reconciliation, dict):
        raise ZeroDeltaExpansionError(
            "zero-delta expansion current-main reconciliation is invalid"
        )
    if list(reconciliation.get("changed_source_game_ids") or []):
        raise ZeroDeltaExpansionError(
            "zero-delta expansion current-main reconciliation changed source games"
        )

    accomplishment_status = str(manifest.get("accomplishment_status", "")).strip()
    accomplishment_hash = str(manifest.get("accomplishment_row_sha256", "")).strip()
    accomplishments = _read_csv(repo / "data/reference/program-accomplishments.csv")
    accomplishment = next(
        (row for row in accomplishments if row.get("program_key") == school_key),
        None,
    )
    if accomplishment_status == "PRESENT":
        if (
            accomplishment is None
            or not re.fullmatch(r"[0-9a-f]{64}", accomplishment_hash)
            or _canonical_row_sha256(accomplishment) != accomplishment_hash
        ):
            raise ZeroDeltaExpansionError(
                "zero-delta expansion accomplishment authority drifted from "
                "the accepted inherited baseline"
            )
    elif accomplishment_status in {"ABSENT", "MISSING"}:
        if accomplishment is not None:
            raise ZeroDeltaExpansionError(
                "zero-delta expansion gained an accomplishment row outside "
                "its frozen authority"
            )
    else:
        raise ZeroDeltaExpansionError(
            "zero-delta expansion accomplishment status is invalid"
        )

    return {
        "kind": "ZERO_DELTA_METADATA_ONLY",
        "inherited_source_game_count": inherited_count,
        "source_games_sha256": frozen_source_hash,
        "accomplishment_status": accomplishment_status,
        "accomplishment_row_sha256": accomplishment_hash,
    }


def apply_zero_delta_projection(
    plan: dict[str, Any],
    context: dict[str, Any],
) -> None:
    """Remove only inherited-baseline review debt from a proven zero-delta plan."""

    summary = plan.get("summary")
    decisions = plan.get("decisions")
    blockers = plan.get("blockers")
    if (
        not isinstance(summary, dict)
        or not isinstance(decisions, list)
        or not isinstance(blockers, list)
    ):
        raise ZeroDeltaExpansionError("zero-delta expansion plan shape is invalid")

    required_zero_summary = (
        "new_canonical_games",
        "identity_review_required",
        "assertions_to_add",
        "canonical_enrichment_games",
        "canonical_enrichment_fields",
        "conditional_discrepancies",
        "canonical_site_patch_reviews",
    )
    unexpected_counts = {
        key: int(summary.get(key, 0) or 0)
        for key in required_zero_summary
        if int(summary.get(key, 0) or 0) != 0
    }
    if unexpected_counts:
        raise ZeroDeltaExpansionError(
            "zero-delta expansion surfaced non-baseline Stage 2 work: "
            + json.dumps(unexpected_counts, sort_keys=True)
        )

    if plan.get("identity_collision_groups") or plan.get("identity_cardinality_constraints"):
        raise ZeroDeltaExpansionError(
            "zero-delta expansion surfaced canonical identity review topology"
        )

    allowed_categories = {"discrepancy", "accomplishments"}
    unexpected_categories = sorted(
        {
            str(item.get("category", ""))
            for item in decisions
            if str(item.get("category", "")) not in allowed_categories
        }
    )
    if unexpected_categories:
        raise ZeroDeltaExpansionError(
            "zero-delta expansion surfaced unsupported Stage 2 decision categories: "
            + ", ".join(unexpected_categories)
        )

    inherited_discrepancies = [
        item for item in decisions if item.get("category") == "discrepancy"
    ]
    for item in inherited_discrepancies:
        if not str(item.get("source_game_id", "")).strip():
            raise ZeroDeltaExpansionError(
                "zero-delta expansion discrepancy lacks inherited source-game identity"
            )
    accomplishment_decisions = [
        item for item in decisions if item.get("category") == "accomplishments"
    ]
    retained_blockers = [
        blocker
        for blocker in blockers
        if blocker != ZERO_DELTA_STALE_ACCOMPLISHMENT_BLOCKER
    ]

    plan["blockers"] = retained_blockers
    plan["decisions"] = []
    summary["expansion_transaction_kind"] = context["kind"]
    summary["zero_delta_inherited_source_game_count"] = context[
        "inherited_source_game_count"
    ]
    summary["inherited_unrelated_reviews_excluded"] = len(inherited_discrepancies)
    summary["zero_delta_excluded_discrepancy_population"] = (
        normalized_inherited_discrepancies(inherited_discrepancies)
    )
    summary["inherited_accomplishment_decisions_excluded"] = len(
        accomplishment_decisions
    )
    summary["inherited_stale_accomplishment_blockers_excluded"] = (
        len(blockers) - len(retained_blockers)
    )
    summary["discrepancies_to_add"] = 0
    summary["conditional_discrepancies"] = 0
    summary["canonical_site_patch_reviews"] = 0
    summary["affected_public_programs"] = []
