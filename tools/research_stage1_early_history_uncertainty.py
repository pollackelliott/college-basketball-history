#!/usr/bin/env python3
"""Read-only audit and closeout verification for terminal early-history uncertainty.

This tool never invents games or results and never mutates a Research checkpoint.
audit-candidate proves that an exact no-ledger-change Stage 1 candidate is eligible
for the narrow early-history uncertainty path. verify-closeout independently proves
that a separately hashed Stage 1 COMPLETE successor preserved the historical ledger
and reclassified only the accepted terminal uncertainty.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

CLASS_A = "UNQUANTIFIED_FOUNDING_ERA_SEASON_COVERAGE"
CLASS_B = "IDENTIFIED_COMPETITIVE_GAMES_UNKNOWN_RESULTS"
TERMINAL_A = "EARLY_HISTORY_UNQUANTIFIED_SEASON_COVERAGE"
TERMINAL_B = "EARLY_HISTORY_IDENTIFIED_GAME_RESULT_UNKNOWN"
ELIGIBLE = "ELIGIBLE_FOR_EARLY_HISTORY_UNCERTAINTY_CLOSEOUT"
VERIFIED = "VERIFIED_EARLY_HISTORY_UNCERTAINTY_CLOSEOUT"
METADATA = "early-history-uncertainty.json"
AUTHORING_METADATA = "stage4-authoring/early-history-uncertainty.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_sha(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(data)


def _json(data: bytes) -> Any:
    return json.loads(data.decode("utf-8-sig"))


def _csv(data: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline="")))


def _first(row: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = str(row.get(key, "") or "").strip()
        if value:
            return value
    return ""


def _season_start(value: str) -> int | None:
    match = re.match(r"^\s*(\d{4})", value or "")
    return int(match.group(1)) if match else None


def _explicit_missing_count(text: str) -> int | None:
    words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    }
    token = r"(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)"
    pattern = re.compile(
        rf"\b(?P<count>{token})\s+(?:games?|wins?|loss(?:es)?|ties?)\b"
        rf"[^.;\n]{{0,40}}\bmissing\b",
        re.IGNORECASE,
    )
    total = 0
    for match in pattern.finditer(text or ""):
        raw = match.group("count").lower()
        value = int(raw) if raw.isdecimal() else words[raw]
        if not 0 < value <= 10:
            return None
        total += value
    return total or None


def _is_complete(status: dict[str, Any]) -> bool:
    if status.get("stage1_complete") is True:
        return True
    values = {
        str(status.get("status", "")).upper(),
        str(status.get("stage1_status", "")).upper(),
        str(status.get("stage_status", "")).upper(),
    }
    return "COMPLETE" in values or "STAGE_1_COMPLETE" in values


def _archive(checkpoint: Path, expected_sha256: str) -> tuple[dict[str, bytes], str]:
    actual = sha256_path(checkpoint)
    if not expected_sha256 or actual != expected_sha256:
        raise ValueError("CHECKPOINT_HASH_MISMATCH_OR_UNPINNED")
    with zipfile.ZipFile(checkpoint) as z:
        bad = z.testzip()
        if bad:
            raise ValueError("INVALID_ARCHIVE_CRC:" + bad)
        files = [name for name in z.namelist() if not name.endswith("/")]
        root_files = [name for name in files if "/" not in name]
        if root_files:
            prefix = ""
        else:
            roots = {name.split("/", 1)[0] for name in files}
            if len(roots) != 1:
                raise ValueError("UNEXPECTED_ARCHIVE_LAYOUT")
            prefix = next(iter(roots)) + "/"
        members = {
            name[len(prefix):]: z.read(name)
            for name in files
            if name.startswith(prefix)
        }
    return members, actual


def _verify_manifest(members: dict[str, bytes]) -> list[str]:
    defects: list[str] = []
    if "stage1-manifest.json" not in members:
        return ["MISSING_STAGE1_MANIFEST"]
    try:
        manifest = _json(members["stage1-manifest.json"])
    except (json.JSONDecodeError, UnicodeDecodeError, TypeError):
        return ["INVALID_STAGE1_MANIFEST"]
    tracked = manifest.get("members")
    if not isinstance(tracked, dict):
        return ["INVALID_MANIFEST_MEMBERS"]
    actual_names = set(members) - {"stage1-manifest.json"}
    if set(tracked) != actual_names:
        defects.append("MANIFEST_MEMBER_SET_MISMATCH")
    for name, meta in tracked.items():
        data = members.get(name)
        if data is None or not isinstance(meta, dict):
            defects.append("MANIFEST_MISSING_MEMBER:" + name)
            continue
        if (
            meta.get("size") != len(data)
            or meta.get("sha256") != sha256_bytes(data)
        ):
            defects.append("MANIFEST_MISMATCH:" + name)
    return defects


def _required(
    members: dict[str, bytes], name: str, defects: list[str]
) -> bytes:
    data = members.get(name)
    if data is None:
        defects.append(
            "MISSING_" + name.upper().replace("/", "_").replace("-", "_")
        )
        return b""
    return data


def _row_result(
    row: dict[str, str], school_key: str
) -> tuple[str, str, str, bool]:
    school_score_key = school_key.replace("-", "_") + "_score"
    team = _first(
        row, "team_score", school_score_key, "source_program_score"
    )
    opponent = _first(row, "opponent_score", "opponent_points")
    played = _first(
        row, "played_result", "on_court_result", "source_result", "result"
    ).upper()
    if played in {"W", "L", "T"}:
        return team, opponent, played, True
    if bool(team) != bool(opponent):
        return team, opponent, "", False
    if team and opponent:
        try:
            a, b = int(team), int(opponent)
        except ValueError:
            return team, opponent, "", False
        return (
            team,
            opponent,
            "W" if a > b else "L" if a < b else "T",
            True,
        )
    return team, opponent, "", False


def _evidence_ok(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= 2
        and all(
            isinstance(item, dict)
            and str(item.get("source", "")).strip()
            and str(item.get("authority", "")).strip()
            and str(item.get("finding", "")).strip()
            for item in value
        )
    )


def _blocker_refs(blocker: Any) -> tuple[str, str]:
    if not isinstance(blocker, dict):
        return "", ""
    season = str(
        blocker.get("season", "")
        or blocker.get("season_label", "")
        or ""
    ).strip()
    game_id = str(
        blocker.get("research_game_id", "")
        or blocker.get("game_id", "")
        or ""
    ).strip()
    detail = blocker.get("detail")
    if isinstance(detail, dict):
        season = season or str(
            detail.get("season", "")
            or detail.get("season_label", "")
            or ""
        ).strip()
        game_id = game_id or str(
            detail.get("research_game_id", "")
            or detail.get("game_id", "")
            or ""
        ).strip()
    return season, game_id


def _policy_payload(metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": metadata.get("schema_version"),
        "school_key": metadata.get("school_key"),
        "research_base_sha": metadata.get("research_base_sha"),
        "parent_checkpoint_sha256": metadata.get(
            "parent_checkpoint_sha256"
        ),
        "identified_game_count": metadata.get("identified_game_count"),
        "known_result_game_count": metadata.get(
            "known_result_game_count"
        ),
        "known_result_wins": metadata.get("known_result_wins"),
        "known_result_losses": metadata.get("known_result_losses"),
        "known_result_ties": metadata.get("known_result_ties"),
        "class_a": metadata.get("class_a", []),
        "class_b": metadata.get("class_b", []),
    }


def audit_candidate(
    parent: Path,
    candidate: Path,
    *,
    expected_parent_sha256: str,
    expected_candidate_sha256: str,
) -> dict[str, Any]:
    defects: list[str] = []
    try:
        parent_members, parent_sha = _archive(
            parent, expected_parent_sha256
        )
        candidate_members, candidate_sha = _archive(
            candidate, expected_candidate_sha256
        )
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        return {"status": "FAIL", "defects": [str(exc)]}
    defects.extend(
        "PARENT_" + item for item in _verify_manifest(parent_members)
    )
    defects.extend(
        "CANDIDATE_" + item
        for item in _verify_manifest(candidate_members)
    )

    for name in (
        "structured-stage1-ledger.csv",
        "season-census.csv",
    ):
        if parent_members.get(name) != candidate_members.get(name):
            defects.append("CANDIDATE_HISTORICAL_CORE_DRIFT:" + name)

    try:
        ledger = _csv(
            _required(
                candidate_members,
                "structured-stage1-ledger.csv",
                defects,
            )
        )
        census = _csv(
            _required(candidate_members, "season-census.csv", defects)
        )
        status = _json(
            _required(candidate_members, "stage1-status.json", defects)
        )
        blockers = _json(
            _required(
                candidate_members, "blocking-residuals.json", defects
            )
        )
        metadata = _json(
            _required(candidate_members, METADATA, defects)
        )
        manifest = _json(
            _required(
                candidate_members, "stage1-manifest.json", defects
            )
        )
    except (
        json.JSONDecodeError,
        csv.Error,
        UnicodeDecodeError,
        TypeError,
    ):
        return {
            "status": "FAIL",
            "checkpoint_sha256": candidate_sha,
            "defects": sorted(
                set(defects + ["INVALID_CANDIDATE_CONTENT"])
            ),
        }

    if (
        not isinstance(status, dict)
        or not isinstance(blockers, list)
        or not isinstance(metadata, dict)
    ):
        defects.append("INVALID_STATUS_BLOCKERS_OR_METADATA")
        return {
            "status": "FAIL",
            "checkpoint_sha256": candidate_sha,
            "defects": sorted(set(defects)),
        }
    if _is_complete(status):
        defects.append("PREMATURE_STAGE1_COMPLETE")

    school = str(
        metadata.get("school_key", "") or status.get("school", "")
    ).strip()
    research_base = str(
        metadata.get("research_base_sha", "")
    ).strip()
    if not school:
        defects.append("MISSING_SCHOOL_KEY")
    if (
        not research_base
        or research_base
        != str(status.get("research_base_sha", "")).strip()
    ):
        defects.append("RESEARCH_BASE_MISMATCH")
    if manifest.get("research_base_sha") not in (
        None,
        research_base,
    ):
        defects.append("MANIFEST_RESEARCH_BASE_MISMATCH")
    if metadata.get("parent_checkpoint_sha256") != parent_sha:
        defects.append("PARENT_SHA_BINDING_MISMATCH")

    ids = [
        str(row.get("research_game_id", "") or "").strip()
        for row in ledger
    ]
    if not ledger or not all(ids) or len(ids) != len(set(ids)):
        defects.append("BLANK_OR_DUPLICATE_GAME_IDS")
    if any(
        not _first(
            row,
            "opponent_literal",
            "source_opponent_label",
            "source_opponent_text",
        )
        or not _first(row, "game_type")
        for row in ledger
    ):
        defects.append("UNIDENTIFIED_OR_UNTYPED_LEDGER_GAME")
    if any(
        "PLACEHOLDER" in str(
            row.get("game_universe_state", "")
        ).upper()
        or "UNIDENTIFIED"
        in str(row.get("game_universe_state", "")).upper()
        for row in ledger
    ):
        defects.append("FABRICATED_PLACEHOLDER_GAME_ROW")

    by_id = {
        row.get("research_game_id", "").strip(): row
        for row in ledger
    }
    by_season: dict[str, list[str]] = {}
    known_w = known_l = known_t = known_count = 0
    unknown_ids: set[str] = set()
    malformed_score_ids: set[str] = set()
    for row in ledger:
        gid = row.get("research_game_id", "").strip()
        season = _first(row, "season_label", "season")
        by_season.setdefault(season, []).append(gid)
        team, opp, result, known = _row_result(row, school)
        if bool(team) != bool(opp):
            malformed_score_ids.add(gid)
        if known:
            known_count += 1
            if result == "W":
                known_w += 1
            elif result == "L":
                known_l += 1
            elif result == "T":
                known_t += 1
        elif not team and not opp:
            unknown_ids.add(gid)
    if malformed_score_ids:
        defects.append(
            "ONE_SIDED_SCORE_POPULATION:"
            + ",".join(sorted(malformed_score_ids))
        )

    summary_expected = {
        "identified_game_count": len(ledger),
        "known_result_game_count": known_count,
        "known_result_wins": known_w,
        "known_result_losses": known_l,
        "known_result_ties": known_t,
    }
    for key, expected in summary_expected.items():
        if metadata.get(key) != expected:
            defects.append("SUMMARY_COUNT_MISMATCH:" + key)

    class_a = metadata.get("class_a", [])
    class_b = metadata.get("class_b", [])
    if not isinstance(class_a, list) or not isinstance(class_b, list):
        defects.append("INVALID_CLASS_COLLECTION")
        class_a, class_b = [], []
    if not class_a and not class_b:
        defects.append("NO_EARLY_HISTORY_UNCERTAINTY_DECLARED")

    census_by_season = {
        str(
            row.get("season", "")
            or row.get("season_label", "")
        ).strip(): row
        for row in census
    }
    class_a_seasons: set[str] = set()
    for item in class_a:
        if not isinstance(item, dict):
            defects.append("INVALID_CLASS_A_RECORD")
            continue
        season = str(item.get("season", "")).strip()
        if not season or season in class_a_seasons:
            defects.append("BLANK_OR_DUPLICATE_CLASS_A_SEASON")
            continue
        class_a_seasons.add(season)
        inception = _season_start(
            str(item.get("program_inception_season", ""))
        )
        end = _season_start(
            str(item.get("founding_era_end_season", ""))
        )
        current = _season_start(season)
        if (
            inception is None
            or end is None
            or current is None
            or not inception <= current <= end
        ):
            defects.append("CLASS_A_NOT_FOUNDING_ERA:" + season)
        state = str(item.get("source_state", "")).upper()
        if state not in {
            "NO_RECORD",
            "RECORD_UNAVAILABLE",
            "EQUIVALENT_UNQUANTIFIED",
        }:
            defects.append(
                "CLASS_A_SOURCE_STATE_NOT_UNQUANTIFIED:" + season
            )
        note = str(item.get("source_note", ""))
        if (
            _explicit_missing_count(note) is not None
            or item.get("explicit_missing_game_count")
            not in (None, "")
        ):
            defects.append(
                "CLASS_A_EXPLICIT_COUNT_BELONGS_TO_COUNTED_GAP_PATH:"
                + season
            )
        if item.get("zero_competitive_games_established") is not False:
            defects.append(
                "CLASS_A_ZERO_GAMES_NOT_EXCLUDED:" + season
            )
        if item.get("competitive_game_count_established") is not False:
            defects.append(
                "CLASS_A_GAME_COUNT_NOT_UNQUANTIFIED:" + season
            )
        if (
            item.get("research_exhausted") is not True
            or not _evidence_ok(
                item.get("systematic_evidence_checked")
            )
        ):
            defects.append(
                "CLASS_A_RESEARCH_NOT_EXHAUSTED:" + season
            )
        observed = item.get("observed_identified_game_ids")
        if (
            not isinstance(observed, list)
            or sorted(observed)
            != sorted(by_season.get(season, []))
        ):
            defects.append(
                "CLASS_A_OBSERVED_IDS_MISMATCH:" + season
            )
        c = census_by_season.get(season)
        if c is None:
            defects.append(
                "CLASS_A_MISSING_SEASON_CENSUS:" + season
            )
        else:
            try:
                observed_count = int(
                    str(c.get("observed_games", "")).strip()
                )
            except ValueError:
                observed_count = -1
            if observed_count != len(
                by_season.get(season, [])
            ):
                defects.append(
                    "CLASS_A_CENSUS_OBSERVED_MISMATCH:" + season
                )

    class_b_ids: set[str] = set()
    for item in class_b:
        if not isinstance(item, dict):
            defects.append("INVALID_CLASS_B_RECORD")
            continue
        gid = str(item.get("research_game_id", "")).strip()
        if not gid or gid in class_b_ids:
            defects.append(
                "BLANK_OR_DUPLICATE_CLASS_B_GAME_ID"
            )
            continue
        class_b_ids.add(gid)
        row = by_id.get(gid)
        if row is None:
            defects.append(
                "CLASS_B_GAME_ID_NOT_IN_LEDGER:" + gid
            )
            continue
        team, opp, result, known = _row_result(row, school)
        if team or opp or result or known:
            defects.append(
                "CLASS_B_RESULT_NOT_GENUINELY_UNKNOWN:" + gid
            )
        if item.get("competitive_inclusion") is not True:
            defects.append(
                "CLASS_B_COMPETITIVE_INCLUSION_NOT_ESTABLISHED:"
                + gid
            )
        if (
            str(item.get("game_type", "")).strip()
            != _first(row, "game_type")
        ):
            defects.append("CLASS_B_GAME_TYPE_MISMATCH:" + gid)
        literal = _first(
            row,
            "opponent_literal",
            "source_opponent_label",
            "source_opponent_text",
        )
        if (
            str(item.get("opponent_literal", "")).strip()
            != literal
        ):
            defects.append(
                "CLASS_B_LITERAL_OPPONENT_MISMATCH:" + gid
            )
        if (
            item.get("direct_score_or_result_evidence_present")
            is not False
        ):
            defects.append(
                "CLASS_B_DIRECT_RESULT_EVIDENCE_NOT_EXCLUDED:"
                + gid
            )
        if item.get("aggregate_result_allocation_used") is not False:
            defects.append(
                "CLASS_B_AGGREGATE_ALLOCATION_NOT_EXCLUDED:"
                + gid
            )
        if (
            item.get("research_exhausted") is not True
            or not _evidence_ok(
                item.get("systematic_evidence_checked")
            )
        ):
            defects.append(
                "CLASS_B_RESEARCH_NOT_EXHAUSTED:" + gid
            )

    if class_b_ids != unknown_ids:
        defects.append(
            "CLASS_B_UNKNOWN_RESULT_POPULATION_MISMATCH"
        )

    for index, blocker in enumerate(blockers):
        season, gid = _blocker_refs(blocker)
        if (
            season not in class_a_seasons
            and gid not in class_b_ids
        ):
            defects.append(
                f"UNRELATED_STAGE1_BLOCKER:{index}"
            )
    if len(blockers) != int(
        status.get("blocking_residual_count", len(blockers))
    ):
        defects.append("BLOCKER_COUNT_CONFLICT")

    payload = _policy_payload(metadata)
    report = {
        "schema_version": 1,
        "status": ELIGIBLE if not defects else "FAIL",
        "parent_checkpoint_sha256": parent_sha,
        "candidate_checkpoint_sha256": candidate_sha,
        "research_base_sha": research_base,
        "school_key": school,
        **summary_expected,
        "unknown_result_game_ids": sorted(unknown_ids),
        "unquantified_coverage_seasons": sorted(
            class_a_seasons
        ),
        "policy_payload_sha256": canonical_json_sha(payload),
        "defects": sorted(set(defects)),
        "stage1_complete": False,
    }
    return report


def verify_closeout(
    candidate: Path,
    closeout: Path,
    audit: Path,
    *,
    expected_candidate_sha256: str,
    expected_closeout_sha256: str,
    expected_audit_sha256: str,
) -> dict[str, Any]:
    defects: list[str] = []
    try:
        candidate_members, candidate_sha = _archive(
            candidate, expected_candidate_sha256
        )
        closeout_members, closeout_sha = _archive(
            closeout, expected_closeout_sha256
        )
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        return {"status": "FAIL", "defects": [str(exc)]}

    audit_bytes = audit.read_bytes()
    audit_sha = sha256_bytes(audit_bytes)
    if (
        not expected_audit_sha256
        or audit_sha != expected_audit_sha256
    ):
        defects.append("AUDIT_HASH_MISMATCH_OR_UNPINNED")
    try:
        audit_report = _json(audit_bytes)
    except (json.JSONDecodeError, UnicodeDecodeError):
        audit_report = {}
        defects.append("INVALID_AUDIT_REPORT")

    defects.extend(
        "CANDIDATE_" + item
        for item in _verify_manifest(candidate_members)
    )
    defects.extend(
        "CLOSEOUT_" + item
        for item in _verify_manifest(closeout_members)
    )
    for name in (
        "structured-stage1-ledger.csv",
        "season-census.csv",
    ):
        if candidate_members.get(name) != closeout_members.get(name):
            defects.append(
                "CLOSEOUT_HISTORICAL_CORE_DRIFT:" + name
            )

    try:
        candidate_metadata = _json(
            _required(candidate_members, METADATA, defects)
        )
        closeout_metadata = _json(
            _required(closeout_members, METADATA, defects)
        )
        authoring_metadata = _json(
            _required(closeout_members, AUTHORING_METADATA, defects)
        )
        closeout_status = _json(
            _required(
                closeout_members, "stage1-status.json", defects
            )
        )
        closeout_blockers = _json(
            _required(
                closeout_members,
                "blocking-residuals.json",
                defects,
            )
        )
        closeout_ledger = _csv(
            _required(
                closeout_members,
                "structured-stage1-ledger.csv",
                defects,
            )
        )
    except (
        json.JSONDecodeError,
        csv.Error,
        UnicodeDecodeError,
        TypeError,
    ):
        return {
            "status": "FAIL",
            "checkpoint_sha256": closeout_sha,
            "defects": sorted(
                set(defects + ["INVALID_CLOSEOUT_CONTENT"])
            ),
        }

    if (
        not isinstance(candidate_metadata, dict)
        or not isinstance(closeout_metadata, dict)
        or not isinstance(authoring_metadata, dict)
    ):
        defects.append("INVALID_EARLY_HISTORY_METADATA")
        return {
            "status": "FAIL",
            "checkpoint_sha256": closeout_sha,
            "defects": sorted(set(defects)),
        }

    if _policy_payload(candidate_metadata) != _policy_payload(
        closeout_metadata
    ):
        defects.append("EARLY_HISTORY_POLICY_PAYLOAD_DRIFT")
    if _policy_payload(closeout_metadata) != _policy_payload(
        authoring_metadata
    ):
        defects.append(
            "STAGE4_AUTHORING_UNCERTAINTY_PAYLOAD_DRIFT"
        )
    payload_sha = canonical_json_sha(
        _policy_payload(candidate_metadata)
    )
    if audit_report.get("status") != ELIGIBLE:
        defects.append("AUDIT_NOT_ELIGIBLE")
    if (
        audit_report.get("candidate_checkpoint_sha256")
        != candidate_sha
    ):
        defects.append("AUDIT_CANDIDATE_BINDING_MISMATCH")
    if audit_report.get("policy_payload_sha256") != payload_sha:
        defects.append("AUDIT_POLICY_PAYLOAD_MISMATCH")
    if closeout_metadata.get("audit_sha256") != audit_sha:
        defects.append("CLOSEOUT_AUDIT_BINDING_MISMATCH")
    terminals = closeout_metadata.get(
        "terminal_classifications"
    )
    if terminals != {
        "class_a": TERMINAL_A,
        "class_b": TERMINAL_B,
    }:
        defects.append("TERMINAL_CLASSIFICATIONS_MISMATCH")
    if not _is_complete(closeout_status):
        defects.append("CLOSEOUT_NOT_STAGE1_COMPLETE")
    if (
        not isinstance(closeout_blockers, list)
        or closeout_blockers
    ):
        defects.append("CLOSEOUT_BLOCKERS_NOT_ZERO")
    if int(
        closeout_status.get("blocking_residual_count", 0)
    ) != 0:
        defects.append(
            "CLOSEOUT_STATUS_BLOCKER_COUNT_NOT_ZERO"
        )

    ids = [
        row.get("research_game_id", "").strip()
        for row in closeout_ledger
    ]
    if len(ids) != len(set(ids)) or not all(ids):
        defects.append("CLOSEOUT_GAME_ID_DRIFT")
    if len(closeout_ledger) != audit_report.get(
        "identified_game_count"
    ):
        defects.append("CLOSEOUT_IDENTIFIED_COUNT_DRIFT")
    if sorted(
        audit_report.get("unknown_result_game_ids", [])
    ) != sorted(
        str(item.get("research_game_id", "")).strip()
        for item in closeout_metadata.get("class_b", [])
        if isinstance(item, dict)
    ):
        defects.append("CLOSEOUT_UNKNOWN_RESULT_ID_DRIFT")
    if sorted(
        audit_report.get("unquantified_coverage_seasons", [])
    ) != sorted(
        str(item.get("season", "")).strip()
        for item in closeout_metadata.get("class_a", [])
        if isinstance(item, dict)
    ):
        defects.append("CLOSEOUT_CLASS_A_SEASON_DRIFT")

    return {
        "schema_version": 1,
        "status": VERIFIED if not defects else "FAIL",
        "candidate_checkpoint_sha256": candidate_sha,
        "closeout_checkpoint_sha256": closeout_sha,
        "audit_sha256": audit_sha,
        "policy_payload_sha256": payload_sha,
        "research_base_sha": closeout_metadata.get(
            "research_base_sha"
        ),
        "school_key": closeout_metadata.get("school_key"),
        "identified_game_count": len(closeout_ledger),
        "unknown_result_game_ids": audit_report.get(
            "unknown_result_game_ids", []
        ),
        "unquantified_coverage_seasons": audit_report.get(
            "unquantified_coverage_seasons", []
        ),
        "defects": sorted(set(defects)),
        "stage1_complete": not defects,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(
        dest="command", required=True
    )
    audit = sub.add_parser("audit-candidate")
    audit.add_argument("parent", type=Path)
    audit.add_argument("candidate", type=Path)
    audit.add_argument(
        "--expected-parent-sha256", required=True
    )
    audit.add_argument(
        "--expected-candidate-sha256", required=True
    )
    audit.add_argument("--output", type=Path)

    verify = sub.add_parser("verify-closeout")
    verify.add_argument("candidate", type=Path)
    verify.add_argument("closeout", type=Path)
    verify.add_argument("audit", type=Path)
    verify.add_argument(
        "--expected-candidate-sha256", required=True
    )
    verify.add_argument(
        "--expected-closeout-sha256", required=True
    )
    verify.add_argument(
        "--expected-audit-sha256", required=True
    )
    verify.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    try:
        if args.command == "audit-candidate":
            report = audit_candidate(
                args.parent,
                args.candidate,
                expected_parent_sha256=(
                    args.expected_parent_sha256
                ),
                expected_candidate_sha256=(
                    args.expected_candidate_sha256
                ),
            )
            success = report.get("status") == ELIGIBLE
        else:
            report = verify_closeout(
                args.candidate,
                args.closeout,
                args.audit,
                expected_candidate_sha256=(
                    args.expected_candidate_sha256
                ),
                expected_closeout_sha256=(
                    args.expected_closeout_sha256
                ),
                expected_audit_sha256=(
                    args.expected_audit_sha256
                ),
            )
            success = report.get("status") == VERIFIED
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        zipfile.BadZipFile,
        json.JSONDecodeError,
        csv.Error,
    ) as exc:
        report = {
            "status": "FAIL",
            "defects": [
                "INVALID_INPUT:" + type(exc).__name__
            ],
        }
        success = False

    rendered = (
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    if args.output:
        args.output.parent.mkdir(
            parents=True, exist_ok=True
        )
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if success else 2


if __name__ == "__main__":
    sys.exit(main())
