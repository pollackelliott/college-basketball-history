#!/usr/bin/env python3
"""Authenticate and apply pre-Phase0 historical opponent display reconciliation.

This is an authority adapter around the existing historical display normalizer,
not a second normalization system. It projects only current-project display
representation while preserving the immutable Research/Integration candidate.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import normalize_historical_opponent_displays as normalization
from expansion_implementation_stage1 import render_csv
from opponent_display_representation import field_level_mutation_proof
from remote_implementation_io import Stop

SCHEMA_VERSION = 1
KIND = "ALL_HISTORY_EXPANSION_OPPONENT_DISPLAY_RECONCILIATION"
TOP_LEVEL_KEYS = {
    "schema_version", "kind", "school_key", "protected_main_sha",
    "research_freeze_sha256", "opponent_changes", "source_game_changes",
}
OPPONENT_CHANGE_KEYS = {
    "source_opponent_label", "canonical_opponent_key", "from_name", "to_name",
}
SOURCE_CHANGE_KEYS = {
    "source_game_id", "normalized_opponent_key", "from_name", "to_name",
}


class OpponentDisplayReconciliationError(ValueError):
    """Fail-closed sidecar or current-project representation mismatch."""


def require(condition: Any, code: str) -> None:
    if not condition:
        raise OpponentDisplayReconciliationError(code)


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _rows(data: bytes, label: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise OpponentDisplayReconciliationError(label + "_UTF8_INVALID") from exc
    reader = csv.DictReader(io.StringIO(text, newline=""))
    fields = list(reader.fieldnames or [])
    require(bool(fields), label + "_HEADER_MISSING")
    return fields, list(reader)


def _load_spec(spec_bytes: bytes) -> dict[str, Any]:
    try:
        spec = json.loads(spec_bytes)
    except (TypeError, ValueError) as exc:
        raise OpponentDisplayReconciliationError(
            "EXPANSION_OPPONENT_DISPLAY_SPEC_JSON_INVALID"
        ) from exc
    require(isinstance(spec, dict), "EXPANSION_OPPONENT_DISPLAY_SPEC_NOT_OBJECT")
    require(set(spec) == TOP_LEVEL_KEYS, "EXPANSION_OPPONENT_DISPLAY_SPEC_FIELDS_INVALID")
    require(spec.get("schema_version") == SCHEMA_VERSION,
            "EXPANSION_OPPONENT_DISPLAY_SPEC_SCHEMA_MISMATCH")
    require(spec.get("kind") == KIND,
            "EXPANSION_OPPONENT_DISPLAY_SPEC_KIND_MISMATCH")
    return spec


def _validated_changes(value: Any, *, keys: set[str], label: str) -> list[dict[str, str]]:
    require(isinstance(value, list), label + "_NOT_LIST")
    result: list[dict[str, str]] = []
    for item in value:
        require(isinstance(item, dict) and set(item) == keys, label + "_FIELDS_INVALID")
        row: dict[str, str] = {}
        for key in keys:
            raw = item.get(key)
            require(isinstance(raw, str), label + "_VALUE_NOT_STRING:" + key)
            row[key] = raw
        result.append(row)
    return result


def _opponent_sort(item: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        item["canonical_opponent_key"], item["source_opponent_label"],
        item["from_name"], item["to_name"],
    )


def _source_sort(item: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        item["source_game_id"], item["normalized_opponent_key"],
        item["from_name"], item["to_name"],
    )


def _require_unique(items: list[dict[str, str]], label: str) -> None:
    fingerprints = {
        json.dumps(item, sort_keys=True, separators=(",", ":"))
        for item in items
    }
    require(len(fingerprints) == len(items), label + "_DUPLICATE")


def reconcile_opponent_display(
    *,
    repo: Path,
    school_key: str,
    protected_main_sha: str,
    research_freeze_sha256: str,
    opponents_bytes: bytes,
    source_games_bytes: bytes,
    spec_bytes: bytes,
) -> dict[str, Any]:
    spec = _load_spec(spec_bytes)
    require(spec.get("school_key") == school_key,
            "EXPANSION_OPPONENT_DISPLAY_SCHOOL_MISMATCH")
    require(spec.get("protected_main_sha") == protected_main_sha,
            "EXPANSION_OPPONENT_DISPLAY_MAIN_MISMATCH")
    require(spec.get("research_freeze_sha256") == research_freeze_sha256,
            "EXPANSION_OPPONENT_DISPLAY_RESEARCH_FREEZE_MISMATCH")
    requested_opponents = _validated_changes(
        spec.get("opponent_changes"),
        keys=OPPONENT_CHANGE_KEYS,
        label="EXPANSION_OPPONENT_DISPLAY_OPPONENT_CHANGES",
    )
    requested_sources = _validated_changes(
        spec.get("source_game_changes"),
        keys=SOURCE_CHANGE_KEYS,
        label="EXPANSION_OPPONENT_DISPLAY_SOURCE_CHANGES",
    )
    require(requested_opponents,
            "EXPANSION_OPPONENT_DISPLAY_EMPTY_CHANGE_POPULATION")
    _require_unique(requested_opponents,
                    "EXPANSION_OPPONENT_DISPLAY_OPPONENT_CHANGE")
    _require_unique(requested_sources,
                    "EXPANSION_OPPONENT_DISPLAY_SOURCE_CHANGE")

    opponent_fields, opponent_rows = _rows(
        opponents_bytes, "EXPANSION_OPPONENT_DISPLAY_OPPONENTS"
    )
    source_fields, source_rows = _rows(
        source_games_bytes, "EXPANSION_OPPONENT_DISPLAY_SOURCE_GAMES"
    )
    require(
        {"source_opponent_label", "canonical_opponent_key", "canonical_opponent_name"}
        <= set(opponent_fields),
        "EXPANSION_OPPONENT_DISPLAY_OPPONENT_COLUMNS_MISSING",
    )
    require(
        {"source_game_id", "normalized_opponent_key", "normalized_opponent_name"}
        <= set(source_fields),
        "EXPANSION_OPPONENT_DISPLAY_SOURCE_COLUMNS_MISSING",
    )
    require(render_csv(opponent_fields, opponent_rows) == opponents_bytes,
            "EXPANSION_OPPONENT_DISPLAY_OPPONENT_SERIALIZATION_NOT_CANONICAL")
    require(render_csv(source_fields, source_rows) == source_games_bytes,
            "EXPANSION_OPPONENT_DISPLAY_SOURCE_SERIALIZATION_NOT_CANONICAL")

    program_keys = normalization.project_program_keys(repo)
    authority = normalization.authority_names_by_key(
        repo, school_key, program_keys=program_keys,
    )
    expected_opponents: list[dict[str, str]] = []
    changed_keys: set[str] = set()
    projected_opponents: list[dict[str, str]] = []
    for row in opponent_rows:
        updated = dict(row)
        key = row.get("canonical_opponent_key", "").strip()
        current_raw = row.get("canonical_opponent_name", "")
        authority_names = set(authority.get(key, set()))
        if key and key not in program_keys and authority_names:
            signatures = {
                normalization.build_site_data.normalized_name_signature(name)
                for name in authority_names
                if normalization.build_site_data.normalized_name_signature(name)
            }
            require(len(signatures) == 1,
                    "EXPANSION_OPPONENT_DISPLAY_AUTHORITY_AMBIGUOUS:" + key)
            current_signature = normalization.build_site_data.normalized_name_signature(
                current_raw.strip()
            )
            authority_signature = next(iter(signatures))
            if current_signature != authority_signature:
                preferred = normalization.build_site_data.preferred_display_name(
                    authority_names
                )
                expected_opponents.append({
                    "source_opponent_label": row.get("source_opponent_label", ""),
                    "canonical_opponent_key": key,
                    "from_name": current_raw,
                    "to_name": preferred,
                })
                changed_keys.add(key)
                updated["canonical_opponent_name"] = preferred
        projected_opponents.append(updated)

    _require_unique(expected_opponents,
                    "EXPANSION_OPPONENT_DISPLAY_DERIVED_OPPONENT_CHANGE")
    require(
        sorted(requested_opponents, key=_opponent_sort)
        == sorted(expected_opponents, key=_opponent_sort),
        "EXPANSION_OPPONENT_DISPLAY_OPPONENT_POPULATION_MISMATCH",
    )

    names_by_key: dict[str, set[str]] = defaultdict(set)
    for row in projected_opponents:
        key = row.get("canonical_opponent_key", "").strip()
        name = row.get("canonical_opponent_name", "").strip()
        if key and name:
            names_by_key[key].add(name)
    final_name_by_key: dict[str, str] = {}
    for key in sorted(changed_keys):
        require(len(names_by_key.get(key, set())) == 1,
                "EXPANSION_OPPONENT_DISPLAY_TARGET_NAME_NOT_UNIQUE:" + key)
        final_name_by_key[key] = next(iter(names_by_key[key]))

    expected_sources: list[dict[str, str]] = []
    projected_sources: list[dict[str, str]] = []
    source_ids: set[str] = set()
    for row in source_rows:
        source_id = row.get("source_game_id", "")
        require(bool(source_id) and source_id not in source_ids,
                "EXPANSION_OPPONENT_DISPLAY_SOURCE_ID_NOT_UNIQUE")
        source_ids.add(source_id)
        updated = dict(row)
        key = row.get("normalized_opponent_key", "").strip()
        target = final_name_by_key.get(key)
        current = row.get("normalized_opponent_name", "")
        if target is not None and current != target:
            expected_sources.append({
                "source_game_id": source_id,
                "normalized_opponent_key": key,
                "from_name": current,
                "to_name": target,
            })
            updated["normalized_opponent_name"] = target
        projected_sources.append(updated)

    _require_unique(expected_sources,
                    "EXPANSION_OPPONENT_DISPLAY_DERIVED_SOURCE_CHANGE")
    require(
        sorted(requested_sources, key=_source_sort)
        == sorted(expected_sources, key=_source_sort),
        "EXPANSION_OPPONENT_DISPLAY_SOURCE_POPULATION_MISMATCH",
    )

    projected_opponent_bytes = render_csv(opponent_fields, projected_opponents)
    projected_source_bytes = render_csv(source_fields, projected_sources)
    try:
        field_proof = field_level_mutation_proof(
            school_key=school_key,
            before_opponents=opponents_bytes,
            after_opponents=projected_opponent_bytes,
            before_source_games=source_games_bytes,
            after_source_games=projected_source_bytes,
            expected_blocker_keys=sorted(changed_keys),
            allow_current_d1=False,
        )
    except Stop as exc:
        raise OpponentDisplayReconciliationError(str(exc)) from exc
    require(
        sorted(field_proof.get("source_game_changed_ids") or [])
        == sorted(item["source_game_id"] for item in expected_sources),
        "EXPANSION_OPPONENT_DISPLAY_SOURCE_ID_PROOF_MISMATCH",
    )
    metadata = {
        "schema_version": 1,
        "kind": KIND,
        "spec_sha256": sha256(spec_bytes),
        "school_key": school_key,
        "protected_main_sha": protected_main_sha,
        "research_freeze_sha256": research_freeze_sha256,
        "before_sha256": {
            "opponents.csv": sha256(opponents_bytes),
            "source-games.csv": sha256(source_games_bytes),
        },
        "after_sha256": {
            "opponents.csv": sha256(projected_opponent_bytes),
            "source-games.csv": sha256(projected_source_bytes),
        },
        "changed_opponent_keys": sorted(changed_keys),
        "changed_source_game_ids": sorted(
            item["source_game_id"] for item in expected_sources
        ),
        "field_level_proof": field_proof,
    }
    return {
        "metadata": metadata,
        "opponents_bytes": projected_opponent_bytes,
        "source_games_bytes": projected_source_bytes,
    }
