#!/usr/bin/env python3
"""Protect RESEARCH_FROZEN historical meaning during serialized Implementation.

Phase 0 may rebase integration representation against current main. Once
INTEGRATION_FROZEN is written, substantive historical source-game fields must not
drift silently before Owner Gate 1.

The guard deliberately excludes representation-only fields such as current
opponent display names and normalized opponent keys. Those can require current-main
registry reconciliation. It snapshots the historical/evidentiary fields whose
meaning should reach Gate 1 unchanged unless permanent tooling explicitly authorizes
a deterministic repair.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from onboarding_plan import WorkflowError


SEMANTIC_SOURCE_GAME_FIELDS = (
    "season_label",
    "game_date",
    "team_score",
    "opponent_score",
    "played_result",
    "overtime_periods",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
    "event_or_tournament",
    "curated_game_type",
    "curated_postseason_round",
    "source_opponent_label",
    "raw_text",
)

FIELD_CATEGORIES = {
    "season_label": "SEASON",
    "game_date": "DATE",
    "team_score": "SCORE",
    "opponent_score": "SCORE",
    "played_result": "RESULT",
    "overtime_periods": "OVERTIME",
    "curated_site_type": "SITE_TYPE",
    "curated_venue_name": "VENUE",
    "city": "LOCATION",
    "state": "LOCATION",
    "event_or_tournament": "EVENT",
    "curated_game_type": "GAME_TYPE",
    "curated_postseason_round": "POSTSEASON_ROUND",
    "source_opponent_label": "FROZEN_SOURCE_EVIDENCE",
    "raw_text": "FROZEN_SOURCE_EVIDENCE",
}


def _read_source_games(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise WorkflowError(f"source-games.csv not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        if "source_game_id" not in fieldnames:
            raise WorkflowError(f"{path}: missing source_game_id")
        return list(reader)


def build_source_game_semantic_snapshot(path: Path) -> dict[str, Any]:
    """Return the Integration-Freeze semantic baseline for one source ledger."""

    rows = _read_source_games(path)
    snapshot_rows: dict[str, dict[str, str]] = {}
    for row in rows:
        source_game_id = row.get("source_game_id", "").strip()
        if not source_game_id:
            raise WorkflowError(f"{path}: blank source_game_id in semantic snapshot")
        if source_game_id in snapshot_rows:
            raise WorkflowError(
                f"{path}: duplicate source_game_id in semantic snapshot: {source_game_id}"
            )
        snapshot_rows[source_game_id] = {
            field: row.get(field, "")
            for field in SEMANTIC_SOURCE_GAME_FIELDS
        }

    return {
        "schema_version": 1,
        "fields": list(SEMANTIC_SOURCE_GAME_FIELDS),
        "rows": snapshot_rows,
    }


def semantic_snapshot_sha256(snapshot: dict[str, Any]) -> str:
    payload = json.dumps(
        snapshot,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _manifest_path(repo: Path, school_key: str) -> Path:
    return repo / ".onboarding" / school_key / "integration-freeze.json"


def semantic_drift_report(repo: Path, school_key: str) -> dict[str, Any]:
    """Compare tracked source-game historical meaning with INTEGRATION_FROZEN."""

    manifest_path = _manifest_path(repo, school_key)
    if not manifest_path.is_file():
        raise WorkflowError(
            "INTEGRATION_FROZEN manifest is missing; cannot prove the pre-Gate "
            f"historical boundary: {manifest_path}"
        )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    guard = manifest.get("source_game_semantic_guard")
    if not isinstance(guard, dict) or not isinstance(guard.get("snapshot"), dict):
        raise WorkflowError(
            "INTEGRATION_FROZEN manifest predates the semantic-drift guard or is "
            "incomplete. Re-establish the Phase 0 integration freeze from the immutable "
            "Research package before authoritative preflight."
        )

    baseline = guard["snapshot"]
    expected_hash = str(guard.get("snapshot_sha256", "")).strip()
    actual_baseline_hash = semantic_snapshot_sha256(baseline)
    if expected_hash and expected_hash != actual_baseline_hash:
        raise WorkflowError(
            "INTEGRATION_FROZEN semantic snapshot hash mismatch; the ignored manifest "
            "is not trustworthy."
        )

    current_path = repo / "schools" / school_key / "source-games.csv"
    current = build_source_game_semantic_snapshot(current_path)

    baseline_rows = baseline.get("rows", {})
    current_rows = current.get("rows", {})
    if not isinstance(baseline_rows, dict) or not isinstance(current_rows, dict):
        raise WorkflowError("invalid semantic snapshot row structure")

    changes: list[dict[str, str]] = []
    before_ids = set(baseline_rows)
    after_ids = set(current_rows)

    for source_game_id in sorted(before_ids - after_ids):
        changes.append(
            {
                "source_game_id": source_game_id,
                "field": "[row]",
                "category": "ROW_REMOVED",
                "before": "present",
                "after": "missing",
            }
        )
    for source_game_id in sorted(after_ids - before_ids):
        changes.append(
            {
                "source_game_id": source_game_id,
                "field": "[row]",
                "category": "ROW_ADDED",
                "before": "missing",
                "after": "present",
            }
        )

    fields = tuple(baseline.get("fields", SEMANTIC_SOURCE_GAME_FIELDS))
    for source_game_id in sorted(before_ids & after_ids):
        before = baseline_rows[source_game_id]
        after = current_rows[source_game_id]
        for field in fields:
            before_value = str(before.get(field, ""))
            after_value = str(after.get(field, ""))
            if before_value == after_value:
                continue
            changes.append(
                {
                    "source_game_id": source_game_id,
                    "field": field,
                    "category": FIELD_CATEGORIES.get(field, "HISTORICAL_FIELD"),
                    "before": before_value,
                    "after": after_value,
                }
            )

    categories = Counter(change["category"] for change in changes)
    return {
        "status": "PASS" if not changes else "FAIL",
        "school_key": school_key,
        "integration_base_sha": manifest.get("integration_base_sha", ""),
        "baseline_sha256": actual_baseline_hash,
        "current_sha256": semantic_snapshot_sha256(current),
        "changes": changes,
        "category_counts": dict(sorted(categories.items())),
    }


def print_semantic_drift_report(report: dict[str, Any], *, limit: int = 20) -> None:
    print("College Basketball History — Integration Freeze semantic drift")
    print(f"School:            {report['school_key']}")
    print(f"Status:            {report['status']}")
    print(f"Integration base:  {report.get('integration_base_sha') or '[unknown]'}")
    print(f"Baseline SHA-256:  {report['baseline_sha256']}")
    print(f"Current SHA-256:   {report['current_sha256']}")
    print(f"Substantive drift: {len(report['changes']):,}")
    if report["category_counts"]:
        print(
            "Categories:         "
            + json.dumps(report["category_counts"], sort_keys=True)
        )

    for change in report["changes"][:limit]:
        before = change["before"] or "[blank]"
        after = change["after"] or "[blank]"
        print(
            "  - "
            f"{change['source_game_id']} {change['field']} "
            f"({change['category']}): {before!r} -> {after!r}"
        )
    if len(report["changes"]) > limit:
        print(f"  ... {len(report['changes']) - limit:,} more change(s)")

    if report["status"] == "PASS":
        print(
            "PASS: historical meaning remains identical to INTEGRATION_FROZEN. "
            "Representation-only current-main normalization is outside this guard."
        )


def assert_no_unapproved_semantic_drift(repo: Path, school_key: str) -> dict[str, Any]:
    """STOP preflight/rehearsal/seal if historical meaning drifted pre-Gate."""

    report = semantic_drift_report(repo, school_key)
    if report["status"] == "PASS":
        return report

    summary = ", ".join(
        f"{category}={count}"
        for category, count in report["category_counts"].items()
    )
    examples = []
    for change in report["changes"][:8]:
        examples.append(
            f"{change['source_game_id']}:{change['field']} "
            f"{change['before']!r}->{change['after']!r}"
        )
    detail = "; ".join(examples)
    raise WorkflowError(
        "RESEARCH_FROZEN semantic drift detected after INTEGRATION_FROZEN: "
        f"{len(report['changes'])} change(s)"
        + (f" ({summary})" if summary else "")
        + (f". Examples: {detail}" if detail else "")
        + ". Restore the frozen historical fields and carry the proposed correction "
        "to Owner Gate 1 via the review decision/source_patch_json/canonical_patch_json "
        "machinery. Decision-count reduction is not authority to rewrite history."
    )
