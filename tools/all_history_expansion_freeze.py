#!/usr/bin/env python3
"""Deterministic EXPANSION_RESEARCH_FROZEN writer and fresh validator.

The artifact contains only supplemental All-History expansion Research.
Inherited published authority is authenticated from the exact research_base_sha
Git object and is never copied into the freeze ZIP.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from all_history_expansion_research import (
    BASELINE_PUBLISHED,
    EXPANSION_REQUIRED,
    PRE_INCEPTION,
    ExpansionResearchAuthorityError,
    expansion_season_disposition,
    validate_expansion_baseline_program,
)
from program_history import publication_history_games, valid_season_label


SCHEMA_VERSION = 1
WORKFLOW_KIND = "ALL_HISTORY_EXPANSION"
FROZEN_STATE = "EXPANSION_RESEARCH_FROZEN"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

INHERITED_PACKAGE_MEMBERS = (
    "source-games.csv",
    "opponents.csv",
    "venues.csv",
    "conferences.csv",
    "notes.md",
    "source-notes.md",
)

PAYLOAD_MEMBERS = (
    "expansion-source-games.csv",
    "expansion-opponents.csv",
    "expansion-venues.csv",
    "expansion-season-accounting.csv",
    "expansion-exclusions.csv",
    "expansion-residuals.csv",
    "expansion-non-d1-scan.csv",
    "expansion-baseline-correction-questions.csv",
    "expansion-notes.md",
    "expansion-source-notes.md",
)
MANIFEST_MEMBER = "expansion-freeze.json"
ZIP_MEMBERS = tuple(sorted((*PAYLOAD_MEMBERS, MANIFEST_MEMBER)))

SEASON_ACCOUNTING_FIELDS = (
    "season_label",
    "activity_disposition",
    "identified_competitive_game_count",
    "accounting_basis",
)
EXCLUSION_FIELDS = (
    "exclusion_id",
    "season_label",
    "literal_or_source_locator",
    "exclusion_reason",
    "evidence_basis",
)
RESIDUAL_FIELDS = (
    "residual_id",
    "season_label",
    "source_game_id",
    "residual_category",
    "status",
    "research_basis",
)
NON_D1_SCAN_FIELDS = (
    "opponent_key",
    "supplemental_game_count",
    "representative_raw_labels",
    "support_scope",
    "scan_disposition",
    "scan_basis",
)
CORRECTION_QUESTION_FIELDS = (
    "question_id",
    "inherited_source_game_id",
    "canonical_game_id",
    "issue",
    "evidence_basis",
    "expansion_impact",
    "disposition",
)
OPPONENT_SUPPORT_FIELDS = (
    "support_id",
    "support_action",
    "source_opponent_label",
    "canonical_opponent_key",
    "baseline_row_sha256",
    "changed_fields",
    "candidate_row_json",
    "evidence_basis",
)
VENUE_SUPPORT_FIELDS = (
    "support_id",
    "support_action",
    "venue_key",
    "baseline_row_sha256",
    "changed_fields",
    "candidate_row_json",
    "evidence_basis",
)

SUPPORT_ACTIONS = {
    "NEW_SUPPLEMENTAL",
    "REUSE_INHERITED",
    "EXTEND_INHERITED",
}
ACTIVITY_DISPOSITIONS = {"ACTIVE", "DORMANT_OR_NO_TEAM"}
RESIDUAL_STATUSES = {"BLOCKING", "NONBLOCKING_RESEARCHED"}
SCAN_DISPOSITIONS = {"CLEARED", "FLAGGED_RESOLVED", "UNRESOLVED"}
CORRECTION_IMPACTS = {"NO_EXPANSION_IMPACT", "BLOCKS_EXPANSION"}
ALLOWED_GAME_TYPES = {
    "REGULAR_SEASON",
    "CONFERENCE_TOURNAMENT",
    "NCAA_TOURNAMENT",
    "NIT",
    "POSTSEASON",
}
TRUE_D1_VALUES = {"yes", "true", "1", "y", "d1", "current_d1", "current-d1"}
FALSE_D1_VALUES = {"no", "false", "0", "n", "non_d1", "non-d1", "non d1"}
OPPONENT_EXTENSION_FIELDS = {
    "games_with_source_label",
    "first_season",
    "last_season",
    "audit_note",
}
VENUE_EXTENSION_FIELDS = {
    "aliases",
    "games_currently_assigned",
    "first_assigned_game",
    "last_assigned_game",
    "relationship_start",
    "relationship_end",
    "relationship_date_precision",
    "source_basis",
    "notes",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SCHOOL_KEY = re.compile(r"^[a-z0-9][a-z0-9-]{1,127}$")


class ExpansionFreezeError(ValueError):
    """Fail-closed expansion freeze/verification error."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def canonical_row_sha256(row: Mapping[str, str]) -> str:
    return sha256_bytes(canonical_json_bytes(dict(row)))


def population_sha256(values: Iterable[str]) -> str:
    return sha256_bytes(canonical_json_bytes(sorted(str(value) for value in values)))


def normalized_rows_sha256(rows: Iterable[Mapping[str, str]]) -> str:
    normalized = [dict(row) for row in rows]
    normalized.sort(key=lambda row: canonical_json_bytes(row))
    return sha256_bytes(canonical_json_bytes(normalized))


def _git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        message = result.stderr.decode("utf-8", "replace").strip()
        raise ExpansionFreezeError(
            "Git baseline authentication failed: "
            + (message or " ".join(args))
        )
    if binary:
        return result.stdout
    return result.stdout.decode("utf-8", "strict").strip()


def _exact_commit(repo: Path, research_base_sha: str) -> str:
    value = str(research_base_sha or "").strip().lower()
    if not SHA40.fullmatch(value):
        raise ExpansionFreezeError("research_base_sha must be an exact 40-character SHA")
    actual = str(_git(repo, "rev-parse", f"{value}^{{commit}}")).strip().lower()
    if actual != value:
        raise ExpansionFreezeError(
            f"research_base_sha resolved to a different commit: {actual}"
        )
    return value


def _git_show(repo: Path, commit: str, path: str) -> bytes:
    return bytes(_git(repo, "show", f"{commit}:{path}", binary=True))


def _csv_bytes(data: bytes, label: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        text = data.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text, newline=""))
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    except (UnicodeError, csv.Error) as exc:
        raise ExpansionFreezeError(f"{label} is not valid UTF-8 CSV: {exc}") from exc
    if not fields or any(not field for field in fields):
        raise ExpansionFreezeError(f"{label} has an invalid CSV header")
    return fields, rows


def _require_exact_fields(
    fields: list[str],
    expected: Iterable[str],
    label: str,
) -> None:
    wanted = list(expected)
    if fields != wanted:
        raise ExpansionFreezeError(
            f"{label} fields must equal {wanted!r}; found {fields!r}"
        )


def _one_row_by_key(
    rows: list[dict[str, str]],
    field: str,
    value: str,
    label: str,
) -> dict[str, str]:
    matches = [row for row in rows if row.get(field, "").strip() == value]
    if len(matches) != 1:
        raise ExpansionFreezeError(
            f"{label} must contain exactly one {field}={value!r}; found {len(matches)}"
        )
    return matches[0]


def _scope_row(
    rows: list[dict[str, str]],
    program: Mapping[str, str],
) -> dict[str, str]:
    names = {
        str(program.get("program_name", "") or "").strip(),
        str(program.get("display_name", "") or "").strip(),
    }
    names.discard("")
    if str(program.get("program_key", "") or "").strip() == "miami":
        names.add("Miami")
    matches = [row for row in rows if row.get("school", "").strip() in names]
    if len(matches) != 1:
        raise ExpansionFreezeError(
            "program-top-level-scope.csv must have exactly one target row for "
            + "/".join(sorted(names))
            + f"; found {len(matches)}"
        )
    return matches[0]


def _optional_accomplishment_row(
    rows: list[dict[str, str]],
    school_key: str,
) -> tuple[str, dict[str, str] | None]:
    matches = [
        row for row in rows if row.get("program_key", "").strip() == school_key
    ]
    if len(matches) > 1:
        raise ExpansionFreezeError(
            f"program-accomplishments.csv has duplicate rows for {school_key}"
        )
    return ("PRESENT", matches[0]) if matches else ("ABSENT", None)


def _baseline_terminal_season(source_rows: list[dict[str, str]]) -> str:
    seasons = sorted(
        {
            row.get("season_label", "").strip()
            for row in source_rows
            if valid_season_label(row.get("season_label", "").strip())
        }
    )
    if not seasons:
        raise ExpansionFreezeError(
            "inherited source-games.csv has no valid season for baseline terminal horizon"
        )
    return seasons[-1]


def authenticate_baseline(
    repo: Path,
    school_key: str,
    research_base_sha: str,
) -> dict[str, Any]:
    """Freshly authenticate the inherited baseline from one exact Git commit."""

    if not SCHOOL_KEY.fullmatch(school_key):
        raise ExpansionFreezeError(f"invalid school_key {school_key!r}")
    commit = _exact_commit(repo, research_base_sha)

    programs_fields, programs = _csv_bytes(
        _git_show(repo, commit, "data/reference/programs.csv"),
        "baseline programs.csv",
    )
    del programs_fields
    program = _one_row_by_key(
        programs, "program_key", school_key, "baseline programs.csv"
    )
    try:
        validate_expansion_baseline_program(program)
    except ExpansionResearchAuthorityError as exc:
        raise ExpansionFreezeError(str(exc)) from exc

    _, scope_rows = _csv_bytes(
        _git_show(repo, commit, "data/reference/program-top-level-scope.csv"),
        "baseline program-top-level-scope.csv",
    )
    scope_row = _scope_row(scope_rows, program)

    _, accomplishment_rows = _csv_bytes(
        _git_show(repo, commit, "data/reference/program-accomplishments.csv"),
        "baseline program-accomplishments.csv",
    )
    accomplishment_status, accomplishment_row = _optional_accomplishment_row(
        accomplishment_rows, school_key
    )

    package_bytes: dict[str, bytes] = {}
    package_member_sha256: dict[str, str] = {}
    for name in INHERITED_PACKAGE_MEMBERS:
        raw = _git_show(repo, commit, f"schools/{school_key}/{name}")
        package_bytes[name] = raw
        package_member_sha256[name] = sha256_bytes(raw)

    source_fields, source_rows = _csv_bytes(
        package_bytes["source-games.csv"],
        "inherited source-games.csv",
    )
    opponent_fields, opponent_rows = _csv_bytes(
        package_bytes["opponents.csv"],
        "inherited opponents.csv",
    )
    venue_fields, venue_rows = _csv_bytes(
        package_bytes["venues.csv"],
        "inherited venues.csv",
    )
    terminal = _baseline_terminal_season(source_rows)

    canonical_fields, canonical_rows = _csv_bytes(
        _git_show(repo, commit, "data/canonical/games.csv"),
        "baseline canonical games.csv",
    )
    required_canonical = {
        "canonical_game_id",
        "season_label",
        "team_a_key",
        "team_b_key",
    }
    if not required_canonical.issubset(set(canonical_fields)):
        raise ExpansionFreezeError(
            "baseline canonical games.csv lacks required identity fields"
        )
    published_games = publication_history_games(
        canonical_rows,
        school_key,
        program,
    )
    published_ids = [
        game.get("canonical_game_id", "").strip() for game in published_games
    ]
    if any(not value for value in published_ids) or len(published_ids) != len(
        set(published_ids)
    ):
        raise ExpansionFreezeError(
            "baseline publication-authorized canonical population has blank/duplicate IDs"
        )

    source_ids = [row.get("source_game_id", "").strip() for row in source_rows]

    return {
        "research_base_sha": commit,
        "program": program,
        "program_row_sha256": canonical_row_sha256(program),
        "scope_row": scope_row,
        "scope_row_sha256": canonical_row_sha256(scope_row),
        "accomplishment_status": accomplishment_status,
        "accomplishment_row": accomplishment_row,
        "accomplishment_row_sha256": (
            canonical_row_sha256(accomplishment_row)
            if accomplishment_row is not None
            else ""
        ),
        "package_bytes": package_bytes,
        "package_member_sha256": dict(sorted(package_member_sha256.items())),
        "source_fields": source_fields,
        "source_rows": source_rows,
        "source_ids": source_ids,
        "source_game_count": len(source_rows),
        "source_id_population_sha256": population_sha256(source_ids),
        "opponent_fields": opponent_fields,
        "opponent_rows": opponent_rows,
        "venue_fields": venue_fields,
        "venue_rows": venue_rows,
        "baseline_terminal_season": terminal,
        "published_canonical_ids": sorted(published_ids),
        "published_canonical_game_count": len(published_ids),
        "published_canonical_id_population_sha256": population_sha256(
            published_ids
        ),
    }


def _season_start(value: str) -> int:
    if not valid_season_label(value):
        raise ExpansionFreezeError(f"invalid canonical season {value!r}")
    return int(value[:4])


def _season_from_start(start: int) -> str:
    return f"{start:04d}-{start + 1:04d}"


def expected_expansion_seasons(
    baseline_program: Mapping[str, str],
    researched_inception_season: str,
    baseline_terminal_season: str,
) -> list[str]:
    """Enumerate the exact finite EXPANSION_REQUIRED season authority."""

    start = _season_start(researched_inception_season)
    end = _season_start(baseline_terminal_season)
    if end < start:
        raise ExpansionFreezeError(
            "baseline terminal season predates researched institutional inception"
        )

    expected: list[str] = []
    for year in range(start, end + 1):
        season = _season_from_start(year)
        try:
            disposition = expansion_season_disposition(
                season,
                baseline_program,
                researched_inception_season,
            )
        except ExpansionResearchAuthorityError as exc:
            raise ExpansionFreezeError(str(exc)) from exc
        if disposition == EXPANSION_REQUIRED:
            expected.append(season)
        elif disposition not in {BASELINE_PUBLISHED, PRE_INCEPTION}:
            raise ExpansionFreezeError(
                f"unknown expansion season disposition {disposition!r}"
            )
    return expected


def _read_delta_dir(delta_dir: Path) -> dict[str, bytes]:
    if not delta_dir.is_dir():
        raise ExpansionFreezeError(f"delta directory does not exist: {delta_dir}")
    entries = sorted(delta_dir.iterdir(), key=lambda path: path.name)
    names = [path.name for path in entries]
    if any(not path.is_file() for path in entries):
        raise ExpansionFreezeError("delta directory must contain flat files only")
    if names != sorted(PAYLOAD_MEMBERS):
        raise ExpansionFreezeError(
            f"delta directory must contain exactly {sorted(PAYLOAD_MEMBERS)!r}; "
            f"found {names!r}"
        )
    return {path.name: path.read_bytes() for path in entries}


def _candidate_row_json(
    raw: str,
    expected_fields: list[str],
    label: str,
) -> dict[str, str]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ExpansionFreezeError(f"{label} candidate_row_json is invalid") from exc
    if not isinstance(value, dict) or set(value) != set(expected_fields):
        raise ExpansionFreezeError(
            f"{label} candidate_row_json must contain the exact inherited row schema"
        )
    if any(not isinstance(item, str) for item in value.values()):
        raise ExpansionFreezeError(
            f"{label} candidate_row_json values must all be strings"
        )
    return {field: value[field] for field in expected_fields}


def _split_changed_fields(value: str, label: str) -> set[str]:
    items = [item.strip() for item in value.split(";") if item.strip()]
    if len(items) != len(set(items)):
        raise ExpansionFreezeError(f"{label} changed_fields contains duplicates")
    return set(items)


def _current_d1_class(value: str, label: str) -> bool:
    normalized = value.strip().casefold()
    if normalized in TRUE_D1_VALUES:
        return True
    if normalized in FALSE_D1_VALUES:
        return False
    raise ExpansionFreezeError(f"{label} current_d1 is not explicit: {value!r}")


def _baseline_opponent_matches(
    baseline: dict[str, Any],
    source_label: str,
    canonical_key: str,
) -> list[dict[str, str]]:
    return [
        row
        for row in baseline["opponent_rows"]
        if row.get("source_opponent_label", "").strip() == source_label
        and row.get("canonical_opponent_key", "").strip() == canonical_key
    ]


def _validate_opponent_support(
    rows: list[dict[str, str]],
    baseline: dict[str, Any],
    school_key: str,
    supplemental_sources: list[dict[str, str]],
) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[str, str]]:
    support_ids: set[str] = set()
    by_identity: dict[tuple[str, str], dict[str, Any]] = {}
    required_scan_scope: dict[str, set[str]] = defaultdict(set)

    for index, row in enumerate(rows, start=2):
        label = f"expansion-opponents.csv line {index}"
        support_id = row["support_id"].strip()
        action = row["support_action"].strip()
        source_label = row["source_opponent_label"].strip()
        canonical_key = row["canonical_opponent_key"].strip()
        basis = row["evidence_basis"].strip()
        if not support_id or support_id in support_ids:
            raise ExpansionFreezeError(f"{label} has blank/duplicate support_id")
        support_ids.add(support_id)
        if action not in SUPPORT_ACTIONS:
            raise ExpansionFreezeError(f"{label} has invalid support_action {action!r}")
        if not source_label or not canonical_key or not basis:
            raise ExpansionFreezeError(
                f"{label} requires source label, canonical key, and evidence basis"
            )
        identity = (source_label, canonical_key)
        if identity in by_identity:
            raise ExpansionFreezeError(f"{label} repeats support identity {identity!r}")

        candidate = _candidate_row_json(
            row["candidate_row_json"],
            baseline["opponent_fields"],
            label,
        )
        if candidate.get("source_program_key", "").strip() != school_key:
            raise ExpansionFreezeError(f"{label} candidate belongs to another school")
        if candidate.get("source_opponent_label", "").strip() != source_label:
            raise ExpansionFreezeError(f"{label} source label/candidate mismatch")
        if candidate.get("canonical_opponent_key", "").strip() != canonical_key:
            raise ExpansionFreezeError(f"{label} canonical key/candidate mismatch")

        matches = _baseline_opponent_matches(
            baseline, source_label, canonical_key
        )
        changed = _split_changed_fields(row["changed_fields"], label)
        baseline_hash = row["baseline_row_sha256"].strip()

        if action == "NEW_SUPPLEMENTAL":
            if matches:
                raise ExpansionFreezeError(
                    f"{label} NEW_SUPPLEMENTAL already exists in inherited opponents"
                )
            if baseline_hash or changed:
                raise ExpansionFreezeError(
                    f"{label} NEW_SUPPLEMENTAL cannot claim inherited hash/changed fields"
                )
        else:
            if len(matches) != 1:
                raise ExpansionFreezeError(
                    f"{label} requires exactly one inherited opponent row"
                )
            inherited = matches[0]
            expected_hash = canonical_row_sha256(inherited)
            if baseline_hash != expected_hash:
                raise ExpansionFreezeError(
                    f"{label} inherited opponent hash mismatch"
                )
            differences = {
                field
                for field in baseline["opponent_fields"]
                if inherited.get(field, "") != candidate.get(field, "")
            }
            if action == "REUSE_INHERITED":
                if changed or differences:
                    raise ExpansionFreezeError(
                        f"{label} REUSE_INHERITED must preserve inherited row exactly"
                    )
            else:
                if not changed or changed != differences:
                    raise ExpansionFreezeError(
                        f"{label} EXTEND_INHERITED changed_fields must equal exact row diff"
                    )
                forbidden = changed - OPPONENT_EXTENSION_FIELDS
                if forbidden:
                    raise ExpansionFreezeError(
                        f"{label} cannot extend opponent fields {sorted(forbidden)!r}"
                    )

        current_d1 = _current_d1_class(
            candidate.get("current_d1", ""),
            label,
        )
        if not current_d1 and action == "NEW_SUPPLEMENTAL":
            required_scan_scope[canonical_key].add("SUPPLEMENTAL_NEW")
        if not current_d1 and action == "EXTEND_INHERITED":
            required_scan_scope[canonical_key].add("INHERITED_EXTENSION")

        by_identity[identity] = {
            "row": row,
            "candidate": candidate,
            "action": action,
        }

    source_identities = {
        (
            source.get("source_opponent_label", "").strip(),
            source.get("normalized_opponent_key", "").strip(),
        )
        for source in supplemental_sources
    }
    if set(by_identity) != source_identities:
        missing = sorted(source_identities - set(by_identity))
        extra = sorted(set(by_identity) - source_identities)
        raise ExpansionFreezeError(
            "expansion-opponents.csv must exactly cover supplemental source "
            f"label/key identities; missing={missing!r}, extra={extra!r}"
        )

    scan_scope: dict[str, str] = {}
    for key, scopes in required_scan_scope.items():
        if scopes == {"SUPPLEMENTAL_NEW"}:
            scan_scope[key] = "SUPPLEMENTAL_NEW"
        elif scopes == {"INHERITED_EXTENSION"}:
            scan_scope[key] = "INHERITED_EXTENSION"
        else:
            scan_scope[key] = "SUPPLEMENTAL_NEW_AND_INHERITED_EXTENSION"
    return by_identity, scan_scope


def _baseline_venue_matches(
    baseline: dict[str, Any],
    venue_key: str,
) -> list[dict[str, str]]:
    return [
        row
        for row in baseline["venue_rows"]
        if row.get("venue_key", "").strip() == venue_key
    ]


def _venue_names(row: Mapping[str, str]) -> set[str]:
    names = {str(row.get("canonical_name", "") or "").strip().casefold()}
    names.update(
        item.strip().casefold()
        for item in str(row.get("aliases", "") or "").split(";")
        if item.strip()
    )
    names.discard("")
    return names


def _validate_venue_support(
    rows: list[dict[str, str]],
    baseline: dict[str, Any],
    school_key: str,
    supplemental_sources: list[dict[str, str]],
) -> dict[str, dict[str, Any]]:
    support_ids: set[str] = set()
    by_key: dict[str, dict[str, Any]] = {}

    for index, row in enumerate(rows, start=2):
        label = f"expansion-venues.csv line {index}"
        support_id = row["support_id"].strip()
        action = row["support_action"].strip()
        venue_key = row["venue_key"].strip()
        basis = row["evidence_basis"].strip()
        if not support_id or support_id in support_ids:
            raise ExpansionFreezeError(f"{label} has blank/duplicate support_id")
        support_ids.add(support_id)
        if action not in SUPPORT_ACTIONS:
            raise ExpansionFreezeError(f"{label} has invalid support_action {action!r}")
        if not venue_key or not basis or venue_key in by_key:
            raise ExpansionFreezeError(
                f"{label} requires unique venue_key and nonblank evidence basis"
            )

        candidate = _candidate_row_json(
            row["candidate_row_json"],
            baseline["venue_fields"],
            label,
        )
        if candidate.get("source_program_key", "").strip() != school_key:
            raise ExpansionFreezeError(f"{label} candidate belongs to another school")
        if candidate.get("venue_key", "").strip() != venue_key:
            raise ExpansionFreezeError(f"{label} venue_key/candidate mismatch")

        matches = _baseline_venue_matches(baseline, venue_key)
        changed = _split_changed_fields(row["changed_fields"], label)
        baseline_hash = row["baseline_row_sha256"].strip()

        if action == "NEW_SUPPLEMENTAL":
            if matches:
                raise ExpansionFreezeError(
                    f"{label} NEW_SUPPLEMENTAL venue already exists in inherited package"
                )
            if baseline_hash or changed:
                raise ExpansionFreezeError(
                    f"{label} NEW_SUPPLEMENTAL cannot claim inherited hash/changed fields"
                )
        else:
            if len(matches) != 1:
                raise ExpansionFreezeError(
                    f"{label} requires exactly one inherited venue row"
                )
            inherited = matches[0]
            if baseline_hash != canonical_row_sha256(inherited):
                raise ExpansionFreezeError(f"{label} inherited venue hash mismatch")
            differences = {
                field
                for field in baseline["venue_fields"]
                if inherited.get(field, "") != candidate.get(field, "")
            }
            if action == "REUSE_INHERITED":
                if changed or differences:
                    raise ExpansionFreezeError(
                        f"{label} REUSE_INHERITED must preserve inherited venue exactly"
                    )
            else:
                if not changed or changed != differences:
                    raise ExpansionFreezeError(
                        f"{label} EXTEND_INHERITED changed_fields must equal exact row diff"
                    )
                forbidden = changed - VENUE_EXTENSION_FIELDS
                if forbidden:
                    raise ExpansionFreezeError(
                        f"{label} cannot extend venue fields {sorted(forbidden)!r}"
                    )
        by_key[venue_key] = {
            "row": row,
            "candidate": candidate,
            "action": action,
        }

    name_hits: dict[str, int] = Counter()
    for item in by_key.values():
        for name in _venue_names(item["candidate"]):
            name_hits[name] += 1
    for index, source in enumerate(supplemental_sources, start=2):
        venue_name = source.get("curated_venue_name", "").strip().casefold()
        if not venue_name:
            continue
        if name_hits.get(venue_name, 0) != 1:
            raise ExpansionFreezeError(
                "supplemental source row "
                f"{index} venue {source.get('curated_venue_name', '')!r} "
                "must map to exactly one expansion venue support row"
            )
    return by_key


def _validate_source_games(
    fields: list[str],
    rows: list[dict[str, str]],
    baseline: dict[str, Any],
    school_key: str,
    researched_inception_season: str,
) -> tuple[list[str], Counter[str], Counter[str]]:
    if fields != baseline["source_fields"]:
        raise ExpansionFreezeError(
            "expansion-source-games.csv must use the exact ordinary source-game "
            "schema inherited by the target package"
        )

    baseline_ids = {
        value for value in baseline["source_ids"] if value
    }
    seen: set[str] = set()
    source_ids: list[str] = []
    per_season: Counter[str] = Counter()
    per_opponent: Counter[str] = Counter()

    for index, row in enumerate(rows, start=2):
        label = f"expansion-source-games.csv line {index}"
        source_id = row.get("source_game_id", "").strip()
        season = row.get("season_label", "").strip()
        if not source_id or source_id in seen:
            raise ExpansionFreezeError(f"{label} has blank/duplicate source_game_id")
        if source_id in baseline_ids:
            raise ExpansionFreezeError(
                f"{label} source_game_id collides with inherited baseline: {source_id}"
            )
        seen.add(source_id)
        source_ids.append(source_id)

        if row.get("source_program_key", "").strip() != school_key:
            raise ExpansionFreezeError(f"{label} belongs to another source program")
        try:
            disposition = expansion_season_disposition(
                season,
                baseline["program"],
                researched_inception_season,
            )
        except ExpansionResearchAuthorityError as exc:
            raise ExpansionFreezeError(f"{label}: {exc}") from exc
        if disposition != EXPANSION_REQUIRED:
            raise ExpansionFreezeError(
                f"{label} season {season!r} is {disposition}, not EXPANSION_REQUIRED"
            )

        source_label = row.get("source_opponent_label", "").strip()
        opponent_key = row.get("normalized_opponent_key", "").strip()
        if not source_label or not opponent_key:
            raise ExpansionFreezeError(
                f"{label} requires resolved source opponent label and opponent key"
            )
        game_type = row.get("curated_game_type", "").strip()
        if game_type not in ALLOWED_GAME_TYPES:
            raise ExpansionFreezeError(
                f"{label} is not a recognized competitive varsity game type: "
                f"{game_type!r}"
            )
        if "EXHIBITION" in row.get("administrative_status", "").upper():
            raise ExpansionFreezeError(f"{label} is marked as an exhibition")
        if not row.get("raw_text", "").strip():
            raise ExpansionFreezeError(f"{label} must preserve literal raw_text")
        if not row.get("source_page", "").strip():
            raise ExpansionFreezeError(f"{label} must preserve a source locator")

        per_season[season] += 1
        per_opponent[opponent_key] += 1

    return source_ids, per_season, per_opponent


def _validate_season_accounting(
    rows: list[dict[str, str]],
    expected_seasons: list[str],
    per_season_games: Counter[str],
) -> None:
    by_season: dict[str, dict[str, str]] = {}
    for index, row in enumerate(rows, start=2):
        label = f"expansion-season-accounting.csv line {index}"
        season = row["season_label"].strip()
        activity = row["activity_disposition"].strip()
        basis = row["accounting_basis"].strip()
        if season in by_season or not valid_season_label(season):
            raise ExpansionFreezeError(f"{label} has invalid/duplicate season")
        if activity not in ACTIVITY_DISPOSITIONS:
            raise ExpansionFreezeError(f"{label} has invalid activity disposition")
        if not basis:
            raise ExpansionFreezeError(f"{label} requires nonblank accounting basis")
        try:
            declared = int(row["identified_competitive_game_count"].strip())
        except ValueError as exc:
            raise ExpansionFreezeError(f"{label} has invalid game count") from exc
        if declared < 0:
            raise ExpansionFreezeError(f"{label} game count cannot be negative")
        actual = per_season_games.get(season, 0)
        if activity == "ACTIVE" and declared != actual:
            raise ExpansionFreezeError(
                f"{label} ACTIVE count {declared} does not equal supplemental "
                f"source-game count {actual}"
            )
        if activity == "DORMANT_OR_NO_TEAM" and (declared != 0 or actual != 0):
            raise ExpansionFreezeError(
                f"{label} dormant/no-team season cannot contain supplemental games"
            )
        by_season[season] = row

    if set(by_season) != set(expected_seasons):
        missing = sorted(set(expected_seasons) - set(by_season))
        extra = sorted(set(by_season) - set(expected_seasons))
        raise ExpansionFreezeError(
            "season accounting must equal the exact EXPANSION_REQUIRED population; "
            f"missing={missing!r}, extra={extra!r}"
        )


def _validate_exclusions(
    rows: list[dict[str, str]],
    baseline: dict[str, Any],
    inception: str,
) -> None:
    ids: set[str] = set()
    for index, row in enumerate(rows, start=2):
        label = f"expansion-exclusions.csv line {index}"
        rid = row["exclusion_id"].strip()
        season = row["season_label"].strip()
        if not rid or rid in ids:
            raise ExpansionFreezeError(f"{label} has blank/duplicate exclusion_id")
        ids.add(rid)
        try:
            disposition = expansion_season_disposition(
                season, baseline["program"], inception
            )
        except ExpansionResearchAuthorityError as exc:
            raise ExpansionFreezeError(f"{label}: {exc}") from exc
        if disposition != EXPANSION_REQUIRED:
            raise ExpansionFreezeError(
                f"{label} belongs to {disposition}, not supplemental Research"
            )
        if not row["literal_or_source_locator"].strip():
            raise ExpansionFreezeError(f"{label} requires literal/source locator")
        if not row["exclusion_reason"].strip() or not row["evidence_basis"].strip():
            raise ExpansionFreezeError(f"{label} requires exclusion reason and basis")


def _validate_residuals(
    rows: list[dict[str, str]],
    baseline: dict[str, Any],
    inception: str,
    source_by_id: dict[str, dict[str, str]],
) -> dict[str, int]:
    ids: set[str] = set()
    summary: Counter[str] = Counter()
    for index, row in enumerate(rows, start=2):
        label = f"expansion-residuals.csv line {index}"
        rid = row["residual_id"].strip()
        season = row["season_label"].strip()
        source_id = row["source_game_id"].strip()
        status = row["status"].strip()
        if not rid or rid in ids:
            raise ExpansionFreezeError(f"{label} has blank/duplicate residual_id")
        ids.add(rid)
        if status not in RESIDUAL_STATUSES:
            raise ExpansionFreezeError(f"{label} has invalid residual status")
        if not row["residual_category"].strip() or not row["research_basis"].strip():
            raise ExpansionFreezeError(f"{label} requires category and research basis")
        if not season and not source_id:
            raise ExpansionFreezeError(f"{label} must identify a season or source game")
        if source_id:
            source = source_by_id.get(source_id)
            if source is None:
                raise ExpansionFreezeError(
                    f"{label} references unknown supplemental source_game_id"
                )
            source_season = source.get("season_label", "").strip()
            if season and season != source_season:
                raise ExpansionFreezeError(
                    f"{label} season conflicts with referenced supplemental source"
                )
            season = source_season
        if season:
            try:
                disposition = expansion_season_disposition(
                    season, baseline["program"], inception
                )
            except ExpansionResearchAuthorityError as exc:
                raise ExpansionFreezeError(f"{label}: {exc}") from exc
            if disposition != EXPANSION_REQUIRED:
                raise ExpansionFreezeError(
                    f"{label} residual belongs to {disposition}, not expansion"
                )
        summary[status] += 1

    if summary["BLOCKING"]:
        raise ExpansionFreezeError(
            f"EXPANSION_RESEARCH_FROZEN cannot contain "
            f"{summary['BLOCKING']} BLOCKING residuals"
        )
    return dict(sorted(summary.items()))


def _validate_non_d1_scan(
    rows: list[dict[str, str]],
    required_scope: dict[str, str],
    per_opponent_games: Counter[str],
) -> dict[str, int]:
    by_key: dict[str, dict[str, str]] = {}
    summary: Counter[str] = Counter()
    for index, row in enumerate(rows, start=2):
        label = f"expansion-non-d1-scan.csv line {index}"
        key = row["opponent_key"].strip()
        disposition = row["scan_disposition"].strip()
        if not key or key in by_key:
            raise ExpansionFreezeError(f"{label} has blank/duplicate opponent_key")
        if disposition not in SCAN_DISPOSITIONS:
            raise ExpansionFreezeError(f"{label} has invalid scan disposition")
        try:
            declared_count = int(row["supplemental_game_count"].strip())
        except ValueError as exc:
            raise ExpansionFreezeError(f"{label} has invalid game count") from exc
        if declared_count != per_opponent_games.get(key, 0):
            raise ExpansionFreezeError(
                f"{label} supplemental game count does not match accepted source rows"
            )
        if not row["representative_raw_labels"].strip():
            raise ExpansionFreezeError(f"{label} requires representative raw labels")
        if disposition == "FLAGGED_RESOLVED" and not row["scan_basis"].strip():
            raise ExpansionFreezeError(f"{label} flagged resolution requires basis")
        if disposition == "UNRESOLVED":
            raise ExpansionFreezeError(
                f"{label} owner-flagged NON_D1 identity remains unresolved"
            )
        by_key[key] = row
        summary[disposition] += 1

    if set(by_key) != set(required_scope):
        missing = sorted(set(required_scope) - set(by_key))
        extra = sorted(set(by_key) - set(required_scope))
        raise ExpansionFreezeError(
            "expansion NON_D1 scan must equal exact supplemental/touched population; "
            f"missing={missing!r}, extra={extra!r}"
        )
    for key, expected_scope in required_scope.items():
        if by_key[key]["support_scope"].strip() != expected_scope:
            raise ExpansionFreezeError(
                f"NON_D1 scan {key} has wrong support_scope; "
                f"expected {expected_scope}"
            )
    return dict(sorted(summary.items()))


def _validate_correction_questions(
    rows: list[dict[str, str]],
) -> dict[str, int]:
    ids: set[str] = set()
    summary: Counter[str] = Counter()
    for index, row in enumerate(rows, start=2):
        label = f"expansion-baseline-correction-questions.csv line {index}"
        qid = row["question_id"].strip()
        impact = row["expansion_impact"].strip()
        if not qid or qid in ids:
            raise ExpansionFreezeError(f"{label} has blank/duplicate question_id")
        ids.add(qid)
        if impact not in CORRECTION_IMPACTS:
            raise ExpansionFreezeError(f"{label} has invalid expansion_impact")
        if not row["issue"].strip() or not row["evidence_basis"].strip():
            raise ExpansionFreezeError(f"{label} requires issue and evidence basis")
        if not row["disposition"].strip():
            raise ExpansionFreezeError(f"{label} requires explicit disposition")
        summary[impact] += 1

    if summary["BLOCKS_EXPANSION"]:
        raise ExpansionFreezeError(
            "baseline correction questions include BLOCKS_EXPANSION; "
            "resolve separately before freeze"
        )
    return dict(sorted(summary.items()))


def _validate_notes(
    payload: dict[str, bytes],
    research_base_sha: str,
    inception: str,
) -> None:
    try:
        notes = payload["expansion-notes.md"].decode("utf-8")
        source_notes = payload["expansion-source-notes.md"].decode("utf-8")
    except UnicodeError as exc:
        raise ExpansionFreezeError("expansion notes must be UTF-8") from exc
    if not notes.strip() or not source_notes.strip():
        raise ExpansionFreezeError("expansion notes/source-notes must be nonblank")
    folded = notes.casefold()
    if research_base_sha not in notes or inception not in notes:
        raise ExpansionFreezeError(
            "expansion-notes.md must state research_base_sha and researched inception"
        )
    if "baseline" not in folded or "inherited" not in folded:
        raise ExpansionFreezeError(
            "expansion-notes.md must state that the baseline is inherited"
        )


def validate_delta_payload(
    payload: dict[str, bytes],
    baseline: dict[str, Any],
    school_key: str,
    researched_inception_season: str,
) -> dict[str, Any]:
    """Validate the complete supplemental artifact payload against baseline authority."""

    if set(payload) != set(PAYLOAD_MEMBERS):
        raise ExpansionFreezeError("supplemental payload member population mismatch")

    expected_seasons = expected_expansion_seasons(
        baseline["program"],
        researched_inception_season,
        baseline["baseline_terminal_season"],
    )

    source_fields, source_rows = _csv_bytes(
        payload["expansion-source-games.csv"],
        "expansion-source-games.csv",
    )
    source_ids, per_season, per_opponent = _validate_source_games(
        source_fields,
        source_rows,
        baseline,
        school_key,
        researched_inception_season,
    )
    source_by_id = {
        row["source_game_id"].strip(): row for row in source_rows
    }

    opponent_fields, opponent_rows = _csv_bytes(
        payload["expansion-opponents.csv"],
        "expansion-opponents.csv",
    )
    _require_exact_fields(
        opponent_fields, OPPONENT_SUPPORT_FIELDS, "expansion-opponents.csv"
    )
    _, required_scan_scope = _validate_opponent_support(
        opponent_rows,
        baseline,
        school_key,
        source_rows,
    )

    venue_fields, venue_rows = _csv_bytes(
        payload["expansion-venues.csv"],
        "expansion-venues.csv",
    )
    _require_exact_fields(
        venue_fields, VENUE_SUPPORT_FIELDS, "expansion-venues.csv"
    )
    _validate_venue_support(
        venue_rows,
        baseline,
        school_key,
        source_rows,
    )

    accounting_fields, accounting_rows = _csv_bytes(
        payload["expansion-season-accounting.csv"],
        "expansion-season-accounting.csv",
    )
    _require_exact_fields(
        accounting_fields,
        SEASON_ACCOUNTING_FIELDS,
        "expansion-season-accounting.csv",
    )
    _validate_season_accounting(
        accounting_rows,
        expected_seasons,
        per_season,
    )

    exclusion_fields, exclusion_rows = _csv_bytes(
        payload["expansion-exclusions.csv"],
        "expansion-exclusions.csv",
    )
    _require_exact_fields(
        exclusion_fields, EXCLUSION_FIELDS, "expansion-exclusions.csv"
    )
    _validate_exclusions(
        exclusion_rows,
        baseline,
        researched_inception_season,
    )

    residual_fields, residual_rows = _csv_bytes(
        payload["expansion-residuals.csv"],
        "expansion-residuals.csv",
    )
    _require_exact_fields(
        residual_fields, RESIDUAL_FIELDS, "expansion-residuals.csv"
    )
    residual_summary = _validate_residuals(
        residual_rows,
        baseline,
        researched_inception_season,
        source_by_id,
    )

    scan_fields, scan_rows = _csv_bytes(
        payload["expansion-non-d1-scan.csv"],
        "expansion-non-d1-scan.csv",
    )
    _require_exact_fields(
        scan_fields, NON_D1_SCAN_FIELDS, "expansion-non-d1-scan.csv"
    )
    scan_summary = _validate_non_d1_scan(
        scan_rows,
        required_scan_scope,
        per_opponent,
    )

    correction_fields, correction_rows = _csv_bytes(
        payload["expansion-baseline-correction-questions.csv"],
        "expansion-baseline-correction-questions.csv",
    )
    _require_exact_fields(
        correction_fields,
        CORRECTION_QUESTION_FIELDS,
        "expansion-baseline-correction-questions.csv",
    )
    correction_summary = _validate_correction_questions(correction_rows)

    _validate_notes(
        payload,
        baseline["research_base_sha"],
        researched_inception_season,
    )

    return {
        "expected_expansion_seasons": expected_seasons,
        "source_rows": source_rows,
        "source_ids": source_ids,
        "season_accounting_rows": accounting_rows,
        "exclusion_rows": exclusion_rows,
        "residual_rows": residual_rows,
        "residual_summary": residual_summary,
        "non_d1_scan_rows": scan_rows,
        "non_d1_scan_summary": scan_summary,
        "correction_question_rows": correction_rows,
        "correction_question_summary": correction_summary,
        "opponent_support_rows": opponent_rows,
        "venue_support_rows": venue_rows,
    }


def manifest_self_fingerprint(manifest: Mapping[str, Any]) -> str:
    projected = copy.deepcopy(dict(manifest))
    projected["manifest_self_fingerprint_sha256"] = ""
    return sha256_bytes(canonical_json_bytes(projected))


def build_manifest(
    baseline: dict[str, Any],
    payload: dict[str, bytes],
    validated: dict[str, Any],
    school_key: str,
    researched_inception_season: str,
) -> dict[str, Any]:
    member_hashes = {
        name: sha256_bytes(payload[name]) for name in sorted(PAYLOAD_MEMBERS)
    }
    expected_seasons = validated["expected_expansion_seasons"]
    source_ids = validated["source_ids"]
    accounting_rows = validated["season_accounting_rows"]
    exclusion_rows = validated["exclusion_rows"]
    residual_rows = validated["residual_rows"]
    scan_rows = validated["non_d1_scan_rows"]
    correction_rows = validated["correction_question_rows"]

    manifest: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "workflow_kind": WORKFLOW_KIND,
        "state": FROZEN_STATE,
        "school_key": school_key,
        "research_base_sha": baseline["research_base_sha"],
        "researched_inception_season": researched_inception_season,
        "baseline_terminal_season": baseline["baseline_terminal_season"],
        "baseline": {
            "program_row_sha256": baseline["program_row_sha256"],
            "top_level_scope_row_sha256": baseline["scope_row_sha256"],
            "accomplishment_row_status": baseline["accomplishment_status"],
            "accomplishment_row_sha256": baseline["accomplishment_row_sha256"],
            "package_member_sha256": baseline["package_member_sha256"],
            "source_game_count": baseline["source_game_count"],
            "source_game_id_population_sha256": (
                baseline["source_id_population_sha256"]
            ),
            "publication_authorized_canonical_game_count": (
                baseline["published_canonical_game_count"]
            ),
            "publication_authorized_canonical_id_population_sha256": (
                baseline["published_canonical_id_population_sha256"]
            ),
        },
        "expansion": {
            "required_season_count": len(expected_seasons),
            "required_season_population_sha256": population_sha256(
                expected_seasons
            ),
            "supplemental_source_game_count": len(source_ids),
            "supplemental_source_id_population_sha256": population_sha256(
                source_ids
            ),
            "season_accounting_count": len(accounting_rows),
            "season_accounting_sha256": normalized_rows_sha256(
                accounting_rows
            ),
            "exclusion_count": len(exclusion_rows),
            "exclusion_sha256": normalized_rows_sha256(exclusion_rows),
            "residual_count": len(residual_rows),
            "residual_status_summary": validated["residual_summary"],
            "residual_sha256": normalized_rows_sha256(residual_rows),
            "non_d1_scan_count": len(scan_rows),
            "non_d1_scan_status_summary": validated["non_d1_scan_summary"],
            "non_d1_scan_sha256": normalized_rows_sha256(scan_rows),
            "baseline_correction_question_count": len(correction_rows),
            "baseline_correction_question_status_summary": (
                validated["correction_question_summary"]
            ),
            "baseline_correction_question_sha256": normalized_rows_sha256(
                correction_rows
            ),
            "opponent_support_count": len(validated["opponent_support_rows"]),
            "venue_support_count": len(validated["venue_support_rows"]),
        },
        "frozen_payload_member_sha256": member_hashes,
        "authority_statement": (
            "Supplemental expansion Research authority only. Inherited published "
            "baseline rows remain accepted authority and are not reproduced or "
            "freshly researched by this artifact. Full baseline+delta materialization "
            "requires later serialized Implementation."
        ),
        "manifest_self_fingerprint_sha256": "",
    }
    manifest["manifest_self_fingerprint_sha256"] = manifest_self_fingerprint(
        manifest
    )
    return manifest


def write_deterministic_zip(path: Path, members: Mapping[str, bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, members[name])


def freeze_expansion(
    repo: Path,
    school_key: str,
    delta_dir: Path,
    research_base_sha: str,
    researched_inception_season: str,
    output: Path,
) -> dict[str, Any]:
    """Validate and write one deterministic supplemental Research freeze."""

    repo = repo.resolve()
    baseline = authenticate_baseline(repo, school_key, research_base_sha)
    payload = _read_delta_dir(delta_dir.resolve())
    validated = validate_delta_payload(
        payload,
        baseline,
        school_key,
        researched_inception_season,
    )
    manifest = build_manifest(
        baseline,
        payload,
        validated,
        school_key,
        researched_inception_season,
    )
    manifest_bytes = canonical_json_bytes(manifest)
    members = dict(payload)
    members[MANIFEST_MEMBER] = manifest_bytes
    if set(members) != set(ZIP_MEMBERS):
        raise ExpansionFreezeError("internal freeze member population mismatch")
    output = output.resolve()
    write_deterministic_zip(output, members)
    return {
        "status": FROZEN_STATE,
        "school_key": school_key,
        "research_base_sha": baseline["research_base_sha"],
        "artifact": str(output),
        "zip_sha256": sha256_file(output),
        "manifest_sha256": sha256_bytes(manifest_bytes),
        "supplemental_source_game_count": len(validated["source_ids"]),
        "expansion_required_season_count": len(
            validated["expected_expansion_seasons"]
        ),
    }


def _read_frozen_zip(path: Path) -> dict[str, bytes]:
    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        raise ExpansionFreezeError(f"invalid expansion freeze ZIP: {exc}") from exc
    with archive:
        if archive.testzip() is not None:
            raise ExpansionFreezeError("expansion freeze ZIP failed CRC validation")
        names = archive.namelist()
        if names != list(ZIP_MEMBERS):
            raise ExpansionFreezeError(
                f"expansion freeze ZIP members/order must equal {list(ZIP_MEMBERS)!r}"
            )
        for info in archive.infolist():
            if info.date_time != FIXED_ZIP_TIME:
                raise ExpansionFreezeError(
                    f"{info.filename}: nondeterministic ZIP timestamp"
                )
            if info.compress_type != zipfile.ZIP_STORED:
                raise ExpansionFreezeError(
                    f"{info.filename}: deterministic artifact must use ZIP_STORED"
                )
            mode = (info.external_attr >> 16) & 0o177777
            if mode != 0o100644:
                raise ExpansionFreezeError(
                    f"{info.filename}: deterministic file mode mismatch"
                )
        return {name: archive.read(name) for name in names}


def verify_expansion(repo: Path, artifact: Path) -> dict[str, Any]:
    """Freshly verify ZIP bytes and recompute exact baseline/delta authority."""

    artifact = artifact.resolve()
    members = _read_frozen_zip(artifact)
    try:
        manifest = json.loads(members[MANIFEST_MEMBER].decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ExpansionFreezeError("expansion-freeze.json is invalid") from exc
    if not isinstance(manifest, dict):
        raise ExpansionFreezeError("expansion-freeze.json must contain an object")
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise ExpansionFreezeError("unsupported expansion freeze schema_version")
    if manifest.get("workflow_kind") != WORKFLOW_KIND:
        raise ExpansionFreezeError("expansion freeze workflow_kind mismatch")
    if manifest.get("state") != FROZEN_STATE:
        raise ExpansionFreezeError("expansion freeze state mismatch")

    expected_member_hashes = {
        name: sha256_bytes(members[name]) for name in sorted(PAYLOAD_MEMBERS)
    }
    if manifest.get("frozen_payload_member_sha256") != expected_member_hashes:
        raise ExpansionFreezeError("frozen payload member SHA-256 map mismatch")
    if manifest.get("manifest_self_fingerprint_sha256") != (
        manifest_self_fingerprint(manifest)
    ):
        raise ExpansionFreezeError("expansion manifest self-fingerprint mismatch")

    school_key = str(manifest.get("school_key") or "").strip()
    research_base = str(manifest.get("research_base_sha") or "").strip()
    inception = str(manifest.get("researched_inception_season") or "").strip()
    baseline = authenticate_baseline(repo.resolve(), school_key, research_base)
    payload = {name: members[name] for name in PAYLOAD_MEMBERS}
    validated = validate_delta_payload(
        payload,
        baseline,
        school_key,
        inception,
    )
    expected_manifest = build_manifest(
        baseline,
        payload,
        validated,
        school_key,
        inception,
    )
    if manifest != expected_manifest:
        raise ExpansionFreezeError(
            "expansion manifest differs from freshly recomputed baseline/delta authority"
        )

    return {
        "status": "VERIFIED_EXPANSION_RESEARCH_FROZEN",
        "school_key": school_key,
        "research_base_sha": research_base,
        "zip_sha256": sha256_file(artifact),
        "manifest_sha256": sha256_bytes(members[MANIFEST_MEMBER]),
        "baseline_terminal_season": baseline["baseline_terminal_season"],
        "expansion_required_season_count": len(
            validated["expected_expansion_seasons"]
        ),
        "supplemental_source_game_count": len(validated["source_ids"]),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    freeze = sub.add_parser("freeze")
    freeze.add_argument("school_key")
    freeze.add_argument("delta_dir", type=Path)
    freeze.add_argument("--research-base", required=True)
    freeze.add_argument("--researched-inception-season", required=True)
    freeze.add_argument("--output", required=True, type=Path)

    verify = sub.add_parser("verify")
    verify.add_argument("artifact", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "freeze":
            report = freeze_expansion(
                args.repo,
                args.school_key,
                args.delta_dir,
                args.research_base,
                args.researched_inception_season,
                args.output,
            )
        else:
            report = verify_expansion(args.repo, args.artifact)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except (ExpansionFreezeError, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
