#!/usr/bin/env python3
"""Pure field-level proof for opponent display representation changes.

Only canonical_opponent_name in opponents.csv and normalized_opponent_name in
source-games.csv are permitted unless an existing caller explicitly opts into
current_d1. Opponent keys, literal source labels, raw evidence, and all other
historical fields remain immutable.
"""
from __future__ import annotations

import csv
import io
from typing import Any

from remote_implementation_io import Stop


def _csv_from_bytes(data: bytes) -> tuple[list[str], list[dict[str, str]]]:
    text = data.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    return list(reader.fieldnames or []), list(reader)


def field_level_mutation_proof(
    *,
    school_key: str,
    before_opponents: bytes,
    after_opponents: bytes,
    before_source_games: bytes,
    after_source_games: bytes,
    expected_blocker_keys: list[str],
    allow_current_d1: bool = False,
) -> dict[str, Any]:
    opp_fields_before, opp_before = _csv_from_bytes(before_opponents)
    opp_fields_after, opp_after = _csv_from_bytes(after_opponents)
    if opp_fields_before != opp_fields_after or len(opp_before) != len(opp_after):
        raise Stop("OPPONENT_DISPLAY_OPPONENT_TABLE_SHAPE_CHANGED")
    if "canonical_opponent_key" not in opp_fields_before:
        raise Stop("OPPONENT_DISPLAY_OPPONENT_KEY_COLUMN_MISSING")
    opponent_changed_rows = 0
    opponent_changed_keys: set[str] = set()
    current_d1_changed_keys: set[str] = set()
    for index, (before, after) in enumerate(zip(opp_before, opp_after), start=2):
        for field in opp_fields_before:
            if before.get(field, "") == after.get(field, ""):
                continue
            allowed_fields = {"canonical_opponent_name"}
            if allow_current_d1:
                allowed_fields.add("current_d1")
            if field not in allowed_fields:
                raise Stop(
                    "OPPONENT_DISPLAY_OPPONENT_FIELD_CHANGED line=%s field=%s"
                    % (index, field)
                )
            if field == "current_d1" and after.get(field, "") not in {"Yes", "No"}:
                raise Stop(
                    "OPPONENT_DISPLAY_CURRENT_D1_VALUE_INVALID line=%s value=%r"
                    % (index, after.get(field, ""))
                )
        if before != after:
            if (
                before.get("canonical_opponent_key", "")
                != after.get("canonical_opponent_key", "")
            ):
                raise Stop("OPPONENT_DISPLAY_OPPONENT_KEY_CHANGED")
            opponent_changed_rows += 1
            changed_key = before.get("canonical_opponent_key", "").strip()
            opponent_changed_keys.add(changed_key)
            if before.get("current_d1", "") != after.get("current_d1", ""):
                current_d1_changed_keys.add(changed_key)

    src_fields_before, src_before = _csv_from_bytes(before_source_games)
    src_fields_after, src_after = _csv_from_bytes(after_source_games)
    if src_fields_before != src_fields_after or len(src_before) != len(src_after):
        raise Stop("OPPONENT_DISPLAY_SOURCE_GAME_TABLE_SHAPE_CHANGED")
    for required in ("source_game_id", "normalized_opponent_key", "normalized_opponent_name"):
        if required not in src_fields_before:
            raise Stop("OPPONENT_DISPLAY_SOURCE_GAME_COLUMN_MISSING:%s" % required)
    source_changed_rows = 0
    source_changed_keys: set[str] = set()
    source_changed_ids: list[str] = []
    for index, (before, after) in enumerate(zip(src_before, src_after), start=2):
        for field in src_fields_before:
            if before.get(field, "") == after.get(field, ""):
                continue
            if field != "normalized_opponent_name":
                raise Stop(
                    "OPPONENT_DISPLAY_SOURCE_FIELD_CHANGED line=%s field=%s"
                    % (index, field)
                )
        if before != after:
            if (
                before.get("normalized_opponent_key", "")
                != after.get("normalized_opponent_key", "")
            ):
                raise Stop("OPPONENT_DISPLAY_SOURCE_OPPONENT_KEY_CHANGED")
            source_changed_rows += 1
            source_changed_keys.add(
                before.get("normalized_opponent_key", "").strip()
            )
            source_changed_ids.append(before.get("source_game_id", ""))

    expected = sorted(expected_blocker_keys)
    if sorted(opponent_changed_keys) != expected:
        raise Stop(
            "OPPONENT_DISPLAY_APPLY_KEY_POPULATION_MISMATCH "
            "expected=%s actual=%s"
            % (expected, sorted(opponent_changed_keys))
        )
    unexpected_current_d1_keys = sorted(current_d1_changed_keys - set(expected))
    if unexpected_current_d1_keys:
        raise Stop(
            "OPPONENT_DISPLAY_CURRENT_D1_KEY_OUTSIDE_CENSUS:"
            + ",".join(unexpected_current_d1_keys)
        )
    unexpected_source_keys = sorted(source_changed_keys - set(expected))
    if unexpected_source_keys:
        raise Stop(
            "OPPONENT_DISPLAY_SOURCE_GAME_KEY_OUTSIDE_CENSUS:"
            + ",".join(unexpected_source_keys)
        )
    return {
        "schema_version": 1,
        "school_key": school_key,
        "allowed_paths": [
            "schools/%s/opponents.csv" % school_key,
            "schools/%s/source-games.csv" % school_key,
        ],
        "opponent_changed_row_count": opponent_changed_rows,
        "opponent_changed_keys": sorted(opponent_changed_keys),
        "opponent_current_d1_changed_keys": sorted(current_d1_changed_keys),
        "opponent_current_d1_changed_key_count": len(current_d1_changed_keys),
        "source_game_normalized_name_row_count": source_changed_rows,
        "source_game_changed_keys": sorted(source_changed_keys),
        "source_game_changed_ids": source_changed_ids,
        "opponent_key_changes": 0,
        "source_game_non_name_field_changes": 0,
        "literal_evidence_changes": 0,
    }
