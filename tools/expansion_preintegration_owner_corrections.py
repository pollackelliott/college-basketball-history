#!/usr/bin/env python3
"""Authenticate a narrowly owner-approved pre-Integration source correction.

Historical authority originates outside this read-only module. The immutable
Research Freeze and literal source evidence are never mutated. A caller must
separately authenticate the exact approval transport and scope envelope; this
module binds those bytes to every original frozen source row and returns an
effective candidate-only projection with a deterministic audit receipt.

This is NOT general permission to edit frozen Research or bypass Gate 1.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import date
from typing import Any

ALLOWED = frozenset({
    "game_date", "team_score", "opponent_score", "curated_site_type",
    "curated_venue_name", "city", "state",
})
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
ISSUE = re.compile(r"^https://github[.]com/[^/]+/[^/]+/issues/[0-9]+$")
AUTHORITY_KIND = "CONTROL_CENTER_OWNER_APPROVED_PREINTEGRATION_V1"


class OwnerCorrectionStop(ValueError):
    """Invalid or unapproved effective-source correction."""


def require(condition: Any, reason: str) -> None:
    if not condition:
        raise OwnerCorrectionStop("OWNER_PREINTEGRATION_" + reason)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":")) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_reference(reference: dict[str, Any], *, school: str, freeze_sha: str) -> None:
    """Validate the control-branch hash/scope envelope independently of Git transport."""
    require(isinstance(reference, dict), "REFERENCE_INVALID")
    require(reference.get("authority_kind") == AUTHORITY_KIND,
            "AUTHORITY_KIND_INVALID")
    require(bool(ISSUE.fullmatch(str(reference.get("approval_issue_url") or ""))),
            "APPROVAL_ISSUE_INVALID")
    for key in ("sha256", "owner_checkpoint_sha256"):
        require(bool(SHA64.fullmatch(str(reference.get(key) or ""))),
                "REFERENCE_SHA_INVALID:" + key)
    require(reference["sha256"] == reference["owner_checkpoint_sha256"],
            "CHECKPOINT_SHA_BINDING_MISMATCH")
    require(reference.get("freeze_sha256") == freeze_sha,
            "REFERENCE_FREEZE_BINDING_MISMATCH")
    require(reference.get("school_key") == school, "REFERENCE_SCHOOL_MISMATCH")
    path = str(reference.get("path") or "")
    require(path and not path.startswith("/") and ".." not in path,
            "REFERENCE_PATH_INVALID")
    ids = reference.get("approved_source_game_ids")
    require(isinstance(ids, list) and bool(ids)
            and all(isinstance(x, str) and x.strip() for x in ids)
            and ids == sorted(set(ids)), "SOURCE_ID_SET_INVALID")


def project_effective_source_rows(
    artifact_bytes: bytes,
    reference: dict[str, Any],
    source_rows: list[dict[str, str]],
    *,
    school: str,
    freeze_sha: str,
    research_base: str,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    """Validate exact original->approved deltas, then project only candidate rows."""
    validate_reference(reference, school=school, freeze_sha=freeze_sha)
    require(digest(artifact_bytes) == reference["sha256"],
            "ARTIFACT_SHA_MISMATCH")
    require(bool(SHA40.fullmatch(research_base)), "RESEARCH_BASE_INVALID")
    try:
        approved = json.loads(artifact_bytes)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise OwnerCorrectionStop("OWNER_PREINTEGRATION_ARTIFACT_JSON_INVALID") from exc
    require(isinstance(approved, dict), "ARTIFACT_OBJECT_REQUIRED")
    meta = approved.get("authority")
    approval = approved.get("approval")
    require(isinstance(meta, dict) and isinstance(approval, dict),
            "APPROVAL_PROVENANCE_MISSING")
    require(meta.get("school") == school and
            meta.get("research_base_sha") == research_base and
            meta.get("frozen_original_zip_sha256") == freeze_sha,
            "APPROVAL_AUTHORITY_BINDING_MISMATCH")
    require(bool(SHA40.fullmatch(str(meta.get("protected_main_sha") or ""))),
            "APPROVED_MAIN_SHA_INVALID")
    require(str(approval.get("owner_response") or "").strip() == "APPROVED. Proceed",
            "EXPLICIT_OWNER_APPROVAL_MISSING")
    require(bool(str(approval.get("exact_scope") or "").strip()),
            "OWNER_SCOPE_MISSING")
    require(approval.get("owner_gate_1_approval") == "NOT_IMPLIED"
            and approval.get("owner_gate_2_approval") == "NOT_IMPLIED",
            "OWNER_GATE_SCOPE_INVALID")
    declarations = approved.get("approved_source_rows")
    require(isinstance(declarations, list), "APPROVED_ROWS_MISSING")
    ids = [x.get("source_game_id") if isinstance(x, dict) else None
           for x in declarations]
    require(sorted(ids) == reference["approved_source_game_ids"]
            and len(ids) == len(set(ids)), "APPROVED_SOURCE_SET_MISMATCH")
    original = {r.get("source_game_id"): r for r in source_rows}
    require(len(original) == len(source_rows), "ORIGINAL_SOURCE_IDS_NOT_UNIQUE")
    result = [dict(r) for r in source_rows]
    projected = {r["source_game_id"]: r for r in result}
    receipts: list[dict[str, Any]] = []
    for item in declarations:
        sid = item["source_game_id"]
        require(sid in original, "UNAUTHENTICATED_SOURCE_GAME:" + sid)
        before = original[sid]
        require(before.get("source_program_key") == school,
                "SOURCE_PROGRAM_CHANGED:" + sid)
        original_hash = digest(canonical(before))
        require(item.get("immutable_original_row_sha256") == original_hash,
                "ORIGINAL_SOURCE_HASH_STALE:" + sid)
        delta = item.get("exact_owner_approved_field_changes")
        require(isinstance(delta, dict) and bool(delta)
                and set(delta) <= ALLOWED, "UNAUTHORIZED_FIELD:" + sid)
        after = projected[sid]
        for field, pair in sorted(delta.items()):
            require(field in before and isinstance(pair, dict)
                    and set(pair) == {"before", "approved_after"}
                    and pair["before"] == before[field]
                    and isinstance(pair["approved_after"], str)
                    and pair["approved_after"] != before[field],
                    "DELTA_MISMATCH:" + sid + ":" + field)
            after[field] = pair["approved_after"]
        if "game_date" in delta:
            try:
                date.fromisoformat(after["game_date"])
            except ValueError as exc:
                raise OwnerCorrectionStop(
                    "OWNER_PREINTEGRATION_DATE_INVALID:" + sid
                ) from exc
        if any(field in delta for field in ("team_score", "opponent_score")):
            require(after["team_score"].isdigit() and
                    after["opponent_score"].isdigit(), "SCORE_INVALID:" + sid)
        if "curated_site_type" in delta:
            require(after["curated_site_type"] in
                    {"SOURCE_PROGRAM_HOME", "OPPONENT_HOME", "NEUTRAL", "UNKNOWN"},
                    "SITE_INVALID:" + sid)
        require(digest(canonical(after)) ==
                item.get("hypothetical_approved_overlay_row_sha256"),
                "EFFECTIVE_SOURCE_HASH_MISMATCH:" + sid)
        # The allowlist is intentionally smaller than the literal/raw evidence
        # set. All nonapproved fields, including opponent and game type, are
        # guaranteed identical because 'after' began as a copy of 'before'.
        receipts.append({
            "source_game_id": sid,
            "immutable_original_row_sha256": original_hash,
            "effective_row_sha256": digest(canonical(after)),
            "field_names": sorted(delta),
        })
    require(len(result) == len(source_rows), "SOURCE_COUNT_CHANGED")
    receipt = {
        "schema_version": 1,
        "kind": "PREINTEGRATION_OWNER_CORRECTION_RECEIPT",
        "owner_approved": True,
        "artifact_sha256": reference["sha256"],
        "owner_checkpoint_sha256": reference["owner_checkpoint_sha256"],
        "approval_issue_url": reference["approval_issue_url"],
        "authority_kind": reference["authority_kind"],
        "school_key": school,
        "research_base_sha": research_base,
        "freeze_sha256": freeze_sha,
        "approved_source_game_ids": reference["approved_source_game_ids"],
        "source_row_receipts": sorted(receipts, key=lambda r:r["source_game_id"]),
        "effective_source_rows_sha256": digest(canonical(result)),
        "tracked_mutation": "NONE",
        "owner_gate_1_approval": False,
    }
    return result, receipt
