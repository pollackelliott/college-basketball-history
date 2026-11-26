"""Fail-closed keyed-venue registration for proven distinct historic buildings.

This module never assigns global VEN IDs, changes source rows, or guesses an
identity from the shared name. Stage 1 and Phase 0 must separately replay the
original Research ZIP, candidate source/venue hashes, current-main registry and
the same exact reconciliation sidecar before guarded publication.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
import datetime as dt
from typing import Any

from onboarding_plan import WorkflowError


ACTION = "REGISTER_DISTINCT_KEYED_IDENTITY"
_FIELDS = frozenset({
    "action", "local_venue_key", "expected_local_name",
    "expected_local_city", "expected_local_state", "resolution_basis",
    "new_global_venue_key", "source_support_id",
    "source_support_row", "source_support_row_sha256",
    "expected_local_row_sha256", "expected_source_games_sha256",
    "conflicting_global_venue_id", "conflicting_global_venue_key",
    "expected_conflicting_global_row_sha256",
    "expected_conflicting_global_name_rows_sha256",
    "expected_conflicting_global_opened",
    "expected_conflicting_global_closed",
    "physical_separation_basis", "excluded_global_alias_names",
})
_SHA = re.compile(r"^[0-9a-f]{64}$")
_KEY = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _fail(reason: str) -> None:
    raise WorkflowError("DISTINCT_KEYED_VENUE_" + reason)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def year(value: str) -> int | None:
    """Validate a year or an actual calendar date before comparing chronology."""
    if not value:
        return None
    if re.fullmatch(r"\d{4}", value.strip()):
        return int(value.strip())
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value.strip()):
        try:
            return dt.date.fromisoformat(value.strip()).year
        except ValueError:
            return None
    return None


def validate_distinct_keyed_registration(
    raw: dict[str, Any],
    local: dict[str, str],
    all_local_rows: list[dict[str, str]],
    global_rows: list[dict[str, str]],
    global_name_rows: list[dict[str, str]] | None,
    *,
    frozen_support_rows: list[dict[str, str]] | None,
    source_games_sha256: str,
    school_key: str,
) -> dict[str, Any]:
    """Validate one exact separation; return only canonical replay-safe fields."""
    if set(raw) != _FIELDS:
        _fail("FIELD_SET_INVALID")
    for field in _FIELDS - {"source_support_row", "excluded_global_alias_names"}:
        if not isinstance(raw[field], str) or not raw[field].strip():
            # An absent global closing date is a supported explicit empty value.
            if field != "expected_conflicting_global_closed":
                _fail("REQUIRED_FIELD:" + field)
    if raw["action"] != ACTION:
        _fail("ACTION_UNSUPPORTED")
    key = local.get("venue_key", "").strip()
    if (not _KEY.fullmatch(key) or key != raw["local_venue_key"]
            or key != raw["new_global_venue_key"]):
        _fail("FROZEN_KEY_REASSIGNMENT")
    if any(
        local.get(field, "").strip() != raw[expect]
        for field, expect in (
            ("canonical_name", "expected_local_name"),
            ("city", "expected_local_city"),
            ("state", "expected_local_state"),
        )
    ):
        _fail("FROZEN_LOCAL_IDENTITY_CHANGED")
    if (
        local.get("source_program_key", "").strip() != school_key
        or local.get("venue_id", "").strip()
    ):
        _fail("FROZEN_LOCAL_PROVENANCE_INVALID")
    if sum(row.get("venue_key", "").strip() == key for row in all_local_rows) != 1:
        _fail("LOCAL_KEY_NOT_UNIQUE")
    if any(
        other is not local
        and norm(other.get("canonical_name", "")) == norm(local["canonical_name"])
        and other.get("city", "").strip().casefold()
        == local.get("city", "").strip().casefold()
        and other.get("state", "").strip().upper()
        == local.get("state", "").strip().upper()
        for other in all_local_rows
    ):
        _fail("DUPLICATE_LOCAL_PHYSICAL_IDENTITY")
    if sha(local) != raw["expected_local_row_sha256"]:
        _fail("FROZEN_LOCAL_ROW_HASH_MISMATCH")
    support = raw["source_support_row"]
    if not isinstance(support, dict) or sha(support) != raw["source_support_row_sha256"]:
        _fail("FROZEN_SUPPORT_ROW_HASH_MISMATCH")
    if (
        support.get("support_id") != raw["source_support_id"]
        or support.get("support_action") != "NEW_SUPPLEMENTAL"
        or support.get("venue_key") != key
    ):
        _fail("FROZEN_SUPPORT_IDENTITY_MISMATCH")
    try:
        described = json.loads(support["candidate_row_json"])
    except (KeyError, TypeError, ValueError) as exc:
        raise WorkflowError("DISTINCT_KEYED_VENUE_SUPPORT_JSON_INVALID") from exc
    if described != local:
        _fail("FROZEN_SUPPORT_CANDIDATE_MISMATCH")
    if frozen_support_rows is not None:
        matches = [
            row for row in frozen_support_rows
            if row.get("support_id") == raw["source_support_id"]
        ]
        if len(matches) != 1 or matches[0] != support:
            _fail("ORIGINAL_FREEZE_SUPPORT_CHANGED")
    if not _SHA.fullmatch(raw["expected_source_games_sha256"]):
        _fail("SOURCE_GAMES_SHA_INVALID")
    if raw["expected_source_games_sha256"] != source_games_sha256:
        _fail("SOURCE_GAMES_ASSIGNMENTS_CHANGED")
    if not local.get("source_basis", "").strip() or not local.get("site_rule", "").strip():
        _fail("PHYSICAL_EVIDENCE_MISSING")
    if not local.get("relationship_type", "").strip():
        _fail("RELATIONSHIP_MISSING")
    if not raw["physical_separation_basis"].strip():
        _fail("SEPARATION_BASIS_MISSING")
    if not raw["resolution_basis"].strip():
        _fail("OWNER_AUTHORITY_MISSING")

    candidates = [
        row for row in global_rows
        if row.get("venue_id") == raw["conflicting_global_venue_id"]
    ]
    if len(candidates) != 1:
        _fail("GLOBAL_ID_STALE")
    incumbent = candidates[0]
    if (
        incumbent.get("venue_key") != raw["conflicting_global_venue_key"]
        or incumbent.get("opened", "") != raw["expected_conflicting_global_opened"]
        or incumbent.get("closed", "") != raw["expected_conflicting_global_closed"]
        or sha(incumbent) != raw["expected_conflicting_global_row_sha256"]
    ):
        _fail("GLOBAL_PHYSICAL_CHRONOLOGY_OR_IDENTITY_STALE")
    if any(row.get("venue_key") == key for row in global_rows):
        _fail("KEY_ALREADY_REGISTERED")
    if (
        incumbent.get("city", "").strip().casefold()
        != local.get("city", "").strip().casefold()
        or incumbent.get("state", "").strip().upper()
        != local.get("state", "").strip().upper()
    ):
        _fail("CONFLICTING_ID_NOT_SAME_LOCALITY")
    if global_name_rows is None:
        _fail("GLOBAL_ALIASES_UNAUTHENTICATED")
    incumbent_alias_rows = [
        row for row in global_name_rows
        if row.get("venue_id") == incumbent["venue_id"]
    ]
    incumbent_alias_rows.sort(key=lambda row: canonical(row))
    if sha(incumbent_alias_rows) != raw["expected_conflicting_global_name_rows_sha256"]:
        _fail("GLOBAL_ALIAS_HASH_STALE")
    closed_year = year(local.get("known_closed", ""))
    incumbent_opened_year = year(incumbent.get("opened", ""))
    if (
        closed_year is None or incumbent_opened_year is None
        or closed_year >= incumbent_opened_year
    ):
        _fail("DISTINCT_PHYSICAL_CHRONOLOGY_NOT_PROVEN")
    relationship_start = local.get("relationship_start", "").strip()
    relationship_end = local.get("relationship_end", "").strip()
    match_start = re.fullmatch(r"(\d{4})-(\d{4})", relationship_start)
    match_end = re.fullmatch(r"(\d{4})-(\d{4})", relationship_end)
    if (
        match_start is None or match_end is None
        or int(match_start.group(2)) != int(match_start.group(1)) + 1
        or int(match_end.group(2)) != int(match_end.group(1)) + 1
        or int(match_start.group(1)) > int(match_end.group(1))
        or int(match_end.group(2)) > closed_year
    ):
        _fail("FROZEN_RELATIONSHIP_CHRONOLOGY_UNPROVEN")
    local_opened = local.get("known_opened", "").strip()
    if local_opened and (
        year(local_opened) is None
        or year(local_opened) > int(match_start.group(1))
        or year(local_opened) > closed_year
    ):
        _fail("FROZEN_OPENING_CHRONOLOGY_INVALID")
    incumbent_closed = incumbent.get("closed", "").strip()
    if incumbent_closed and (
        year(incumbent_closed) is None
        or year(incumbent_closed) < incumbent_opened_year
    ):
        _fail("INCUMBENT_PHYSICAL_CHRONOLOGY_INVALID")

    # Shared name-only matching could silently choose the wrong building.
    # The local alias is preserved, but collided labels are NOT globally
    # registered for the new identity. No change is made to the incumbent.
    local_aliases = [
        x.strip() for x in local.get("aliases", "").split(";") if x.strip()
    ]
    labels = [local["canonical_name"], *local_aliases]
    excluded = raw["excluded_global_alias_names"]
    if not isinstance(excluded, list) or not excluded or any(
        not isinstance(x, str) or not x.strip() for x in excluded
    ):
        _fail("ALIAS_SUPPRESSION_SET_INVALID")
    if len({norm(x) for x in excluded}) != len(excluded):
        _fail("ALIAS_SUPPRESSION_DUPLICATE")
    if not set(norm(x) for x in excluded) <= set(norm(x) for x in local_aliases):
        _fail("ALIAS_SUPPRESSION_NOT_FROZEN")
    norm_by_id: dict[str, set[str]] = {}
    global_by_id = {row["venue_id"]: row for row in global_rows}
    for row in global_rows:
        norm_by_id.setdefault(row["venue_id"], set()).add(norm(row.get("display_name", "")))
    for row in global_name_rows:
        norm_by_id.setdefault(row["venue_id"], set()).add(
            norm(row.get("normalized_name") or row.get("venue_name", ""))
        )
    collision_names: set[str] = set()
    conflicting_ids: set[str] = set()
    for vid, names in norm_by_id.items():
        record = global_by_id.get(vid)
        if record is None:
            continue
        if (
            record.get("city", "").strip().casefold()
            != local.get("city", "").strip().casefold()
            or record.get("state", "").strip().upper()
            != local.get("state", "").strip().upper()
        ):
            continue
        overlap = {norm(x) for x in labels} & names
        if overlap:
            conflicting_ids.add(vid)
            collision_names.update(overlap)
    if conflicting_ids != {incumbent["venue_id"]}:
        _fail("UNRESOLVED_ADDITIONAL_PHYSICAL_MATCHES")
    if norm(local["canonical_name"]) in collision_names:
        _fail("AMBIGUOUS_CANONICAL_NAME")
    if collision_names != {norm(x) for x in excluded}:
        _fail("UNSAFE_OR_UNUSED_GLOBAL_ALIAS_SUPPRESSION")
    return {
        "action": ACTION,
        "local_venue_key": key,
        "new_global_venue_key": key,
        "excluded_global_alias_names": sorted(set(norm(x) for x in excluded)),
        "source_support_id": raw["source_support_id"],
        "source_support_row_sha256": raw["source_support_row_sha256"],
        "expected_local_row_sha256": raw["expected_local_row_sha256"],
        "expected_source_games_sha256": raw["expected_source_games_sha256"],
        "conflicting_global_venue_id": incumbent["venue_id"],
        "conflicting_global_venue_key": incumbent["venue_key"],
        "expected_conflicting_global_row_sha256": raw["expected_conflicting_global_row_sha256"],
        "expected_conflicting_global_name_rows_sha256": raw["expected_conflicting_global_name_rows_sha256"],
        "distinct_chronology": {
            "earlier_known_closed": local["known_closed"],
            "later_opened": incumbent["opened"],
            "relationship_end": relationship_end,
        },
        "physical_separation_basis": raw["physical_separation_basis"],
        "resolution_basis": raw["resolution_basis"],
    }
