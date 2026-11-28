#!/usr/bin/env python3
"""Fail-closed, single-case registered-key representation patch for GCU Stage 2.

This module is deliberately pure and has no publication, branch, lock, or Gate
authority. Only the repository-owned remote control transaction may call it.
Control Center case: https://github.com/pollackelliott/college-basketball-history/issues/736#issuecomment-7243473979
"""
from __future__ import annotations

import csv
import hashlib
import io
from typing import Any

SCHOOL = 'grand-canyon'
OLD_KEY = 'usc-upstate'
NEW_KEY = 'south-carolina-upstate'
GAME_ID = 'grand-canyon-1989-90-035'
RULING_URL = 'https://github.com/pollackelliott/college-basketball-history/issues/736#issuecomment-7243473979'
CENSUS_SHA256 = '30a16fae7319d0c4015dc4e7b2f791313627517e6d54d64dc07a7429efa2d037'
SOURCE_HASHES = {
    'opponents.csv': 'fbcf851f2f2c0b6a288a07078014192ddb20e4c975d088646f7c72e5605a7f88',
    'source-games.csv': '3faa51895daa96370b06f6ed87cfd46918847b920a16ff5863f8aa9b9281c7cd',
}
TARGET_HASHES = {
    'opponents.csv': 'cf2ecc2310ecea7b576ac3ececf519ecf43675f68dc2f6314b8e1725d48ff747',
    'source-games.csv': 'bee104c8c95482a4a69dc5d4889c554fab501625102d504e07d44d57bb8e7e5e',
}
BLOCKER = "opponents.csv line 439: current-D1 opponent key 'usc-upstate' is absent from programs.csv"
ALLOWED_PATHS = ('schools/grand-canyon/opponents.csv', 'schools/grand-canyon/source-games.csv')

class KeyRebaseStop(ValueError):
    """The exact authorized representation exception does not apply."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise KeyRebaseStop(code)


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def rows(blob: bytes) -> tuple[list[str], list[dict[str, str]]]:
    try:
        content = blob.decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(content, newline=''))
        fields = list(reader.fieldnames or [])
        require(bool(fields), 'REBASE_NO_HEADER')
        data = list(reader)
        require(all(None not in row for row in data), 'REBASE_MALFORMED_CSV')
        return fields, data
    except (UnicodeError, csv.Error) as exc:
        raise KeyRebaseStop('REBASE_UNREADABLE_CSV') from exc


def require_registry(registry: bytes) -> dict[str, str]:
    fields, data = rows(registry)
    require({'program_key', 'current_d1', 'display_name', 'city'} <= set(fields),
            'REBASE_REGISTRY_SCHEMA')
    chosen = [row for row in data if row['program_key'] == NEW_KEY]
    require(len(chosen) == 1, 'REBASE_TARGET_PROGRAM_MISSING_OR_DUPLICATE')
    require(not any(row['program_key'] == OLD_KEY for row in data),
            'REBASE_OLD_KEY_STILL_REGISTERED')
    row = chosen[0]
    require(row['current_d1'] == 'Yes' and row['display_name'] == 'USC Upstate'
            and row['city'] == 'Spartanburg', 'REBASE_PROGRAM_IDENTITY_CONFLICT')
    return row


def require_census(status: dict[str, Any], census: dict[str, Any]) -> list[str]:
    blockers = list(status.get('blockers') or [])
    preflight = status.get('preflight') or {}
    require(status.get('status') == 'BLOCKED', 'REBASE_CENSUS_NOT_BLOCKED')
    require(status.get('semantic_drift', {}).get('status') == 'PASS',
            'REBASE_SEMANTIC_DRIFT')
    require(preflight.get('blocker_count') == 40 and len(blockers) == 40,
            'REBASE_BLOCKER_COUNT')
    require(preflight.get('warning_count') == 0 and preflight.get('decision_count') == 0,
            'REBASE_OWNER_OR_WARNING_BLOCKERS')
    require(blockers.count(BLOCKER) == 1, 'REBASE_MISSING_KEY_BLOCKER')
    display = [v.split(':', 2)[1].strip() for v in blockers
               if v.startswith('historical opponent display conflict: ')]
    require(len(display) == 39 and len(set(display)) == 39,
            'REBASE_DISPLAY_POPULATION_UNEXPECTED')
    require(len(display) + 1 == len(blockers), 'REBASE_OTHER_BLOCKER')
    require(census.get('status') == 'PREFLIGHT_BLOCKED'
            and (census.get('preflight') or {}).get('blocker_count') == 40,
            'REBASE_CAPABILITY_CENSUS_MISMATCH')
    return sorted(display)


def verify_diff(before: dict[str, bytes], after: dict[str, bytes]) -> dict[str, Any]:
    require(set(before) == set(SOURCE_HASHES) == set(after), 'REBASE_PATH_SET_INVALID')
    report: dict[str, Any] = {'school_key': SCHOOL, 'case': GAME_ID,
                              'allowed_paths': list(ALLOWED_PATHS), 'field_changes': []}
    for filename, expected_field, expected_id_field, expected_id, expected_count, expected_row in (
        ('opponents.csv', 'canonical_opponent_key', 'source_opponent_label', 'USC-Spartanburg', 491, 439),
        ('source-games.csv', 'normalized_opponent_key', 'source_game_id', GAME_ID, 2147, 1499),
    ):
        initial = before[filename]
        final = after[filename]
        require(digest(initial) == SOURCE_HASHES[filename],
                'REBASE_ORIGINAL_HASH_MISMATCH:' + filename)
        require(digest(final) == TARGET_HASHES[filename],
                'REBASE_CANDIDATE_HASH_MISMATCH:' + filename)
        h0, d0 = rows(initial)
        h1, d1 = rows(final)
        require(h0 == h1 and len(d0) == len(d1) == expected_count,
                'REBASE_TABLE_POPULATION_MISMATCH:' + filename)
        changes = []
        for n, (old, new) in enumerate(zip(d0, d1), start=2):
            for field in h0:
                if old[field] != new[field]:
                    changes.append((n, field, old[field], new[field], old[expected_id_field]))
        require(changes == [(expected_row, expected_field, OLD_KEY, NEW_KEY, expected_id)],
                'REBASE_EXTRA_FIELD_OR_ROW_CHANGE:' + filename)
        report['field_changes'].append({'path': 'schools/' + SCHOOL + '/' + filename,
                                        'row': expected_row, 'field': expected_field,
                                        'before': OLD_KEY, 'after': NEW_KEY})
    return report


def make_candidate(
    old_opponents: bytes, old_games: bytes, main_program_registry: bytes,
) -> tuple[dict[str, bytes], dict[str, Any]]:
    require_registry(main_program_registry)
    before = {'opponents.csv': old_opponents, 'source-games.csv': old_games}
    for name, data in before.items():
        require(digest(data) == SOURCE_HASHES[name], 'REBASE_ORIGINAL_HASH_MISMATCH:' + name)
    _, opp_rows = rows(old_opponents)
    matches = [(i, row) for i, row in enumerate(opp_rows, start=2)
               if row.get('canonical_opponent_key') == OLD_KEY]
    require(len(matches) == 1 and matches[0][0] == 439,
            'REBASE_OPPONENT_KEY_COUNT_OR_POSITION')
    opponent = matches[0][1]
    require(opponent['source_opponent_label'] == 'USC-Spartanburg'
            and opponent['canonical_opponent_name'] == 'USC Upstate'
            and opponent['current_d1'] == 'Yes', 'REBASE_OPPONENT_IDENTITY_MISMATCH')
    require(not any(row.get('canonical_opponent_key') == NEW_KEY for row in opp_rows),
            'REBASE_TARGET_OPPONENT_KEY_COLLISION')
    _, game_rows = rows(old_games)
    games = [(i, row) for i, row in enumerate(game_rows, start=2)
             if row.get('normalized_opponent_key') == OLD_KEY]
    require(len(games) == 1 and games[0][0] == 1499,
            'REBASE_SOURCE_GAME_COUNT_OR_POSITION')
    game = games[0][1]
    require(game['source_game_id'] == GAME_ID and game['game_date'] == '1990-03-15'
            and game['source_opponent_label'] == 'USC-Spartanburg'
            and game['normalized_opponent_name'] == 'USC Upstate'
            and game['team_score'] == '69' and game['opponent_score'] == '75'
            and game['played_result'] == 'L' and game['curated_site_type'] == 'NEUTRAL'
            and game['curated_game_type'] == 'POSTSEASON' and game['city'] == 'Kansas City',
            'REBASE_SOURCE_GAME_IDENTITY_MISMATCH')
    needle = b',' + OLD_KEY.encode('ascii') + b','
    substitute = b',' + NEW_KEY.encode('ascii') + b','
    after = {}
    for name, data in before.items():
        require(data.count(needle) == 1, 'REBASE_BYTE_OCCURRENCE_MISMATCH:' + name)
        after[name] = data.replace(needle, substitute, 1)
    proof = verify_diff(before, after)
    return after, proof


def require_exact_target_files(
    predecessor: dict[str, bytes], prepared: dict[str, bytes], registry: bytes,
) -> dict[str, Any]:
    expected, proof = make_candidate(predecessor['opponents.csv'],
                                     predecessor['source-games.csv'], registry)
    require(expected == prepared, 'REBASE_TARGET_BYTES_MISMATCH')
    require(verify_diff(predecessor, prepared) == proof, 'REBASE_FIELD_PROOF_MISMATCH')
    return proof
