#!/usr/bin/env python3
"""Audit and close a Stage 1 candidate with two legitimate early-history terminal families.

This coordinator is deliberately narrow. It composes only:

* owner-authorized ``EARLY_HISTORY_AGGREGATE_RECONCILED_GAP`` seasons; and
* identified competitive games whose on-court result remains genuinely unknown,
  terminalized as ``EARLY_HISTORY_IDENTIFIED_GAME_RESULT_UNKNOWN``.

It does not weaken or replace the existing single-family closeout tools. A mixed
candidate must already contain durable aggregate-evidence and uncertainty payloads,
zero unrelated blockers, and an unchanged identified-game ledger / season census.
No anonymous game or aggregate-derived row-level result is ever created.

Commands:
  audit CANDIDATE --expected-candidate-sha256 SHA [--registry PATH] [--output REPORT.json]
  closeout CANDIDATE AUDIT.json --expected-candidate-sha256 SHA --expected-audit-sha256 SHA --output SUCCESSOR.zip [--registry PATH]
  verify-closeout CANDIDATE SUCCESSOR.zip AUDIT.json --expected-candidate-sha256 SHA --expected-closeout-sha256 SHA --expected-audit-sha256 SHA [--registry PATH] [--output REPORT.json]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

REGISTRY = Path(__file__).resolve().parents[1] / "data/reference/early-aggregate-coverage-authorities.json"
ELIGIBLE = "ELIGIBLE_FOR_MIXED_EARLY_HISTORY_TERMINAL_CLOSEOUT"
VERIFIED = "VERIFIED_MIXED_EARLY_HISTORY_TERMINAL_CLOSEOUT"
AGG_BLOCKER = "FOUNDING_SEASON_PARTIAL_ROW_IDENTIFICATION"
UNKNOWN_RESULT_BLOCKER = "IDENTIFIED_COMPETITIVE_GAME_RESULT_UNKNOWN"
AGG_TERMINAL = "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP"
UNKNOWN_RESULT_TERMINAL = "EARLY_HISTORY_IDENTIFIED_GAME_RESULT_UNKNOWN"
AGG_EVIDENCE = "founding-season-evidence-exhaustion.json"
AGG_PROPOSAL = "proposed-early-aggregate-authority.json"
UNCERTAINTY_PROPOSAL = "proposed-early-history-uncertainty.json"
MIXED_CLOSEOUT = "mixed-terminal-closeout.json"
AGG_CLOSEOUT = "aggregate-coverage-closeout.json"
UNCERTAINTY_CLOSEOUT = "early-history-uncertainty.json"
STAGE4_AGG = "stage4-authoring/season-coverage.json"
STAGE4_UNCERTAINTY = "stage4-authoring/early-history-uncertainty.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def csv_rows(data: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline="")))


def first(row: dict[str, Any], *names: str) -> str:
    for name in names:
        value = str(row.get(name, "") or "").strip()
        if value:
            return value
    return ""


def read_zip(path: Path, expected_sha256: str) -> tuple[dict[str, bytes], str]:
    raw = path.read_bytes()
    actual = digest(raw)
    if not expected_sha256 or actual != expected_sha256:
        raise ValueError("CHECKPOINT_HASH_MISMATCH_OR_UNPINNED")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError("INVALID_ARCHIVE_CRC:" + bad)
        names = [name for name in archive.namelist() if not name.endswith("/")]
        if not names or len(names) != len(set(names)):
            raise ValueError("INVALID_ARCHIVE_NAMES")
        if "stage1-manifest.json" in names:
            prefix = ""
        else:
            roots = {name.split("/", 1)[0] for name in names if "/" in name}
            if len(roots) != 1 or any("/" not in name for name in names):
                raise ValueError("UNEXPECTED_ARCHIVE_LAYOUT")
            prefix = next(iter(roots)) + "/"
        members: dict[str, bytes] = {}
        for name in names:
            if not name.startswith(prefix):
                raise ValueError("UNEXPECTED_ARCHIVE_LAYOUT")
            inner = name[len(prefix):]
            if not inner or inner.startswith("/") or ".." in Path(inner).parts:
                raise ValueError("UNSAFE_ARCHIVE_PATH")
            members[inner] = archive.read(name)
    return members, actual


def manifest_defects(members: dict[str, bytes]) -> list[str]:
    raw = members.get("stage1-manifest.json")
    if raw is None:
        return ["MISSING_STAGE1_MANIFEST"]
    try:
        manifest = json.loads(raw)
    except (json.JSONDecodeError, UnicodeError):
        return ["INVALID_STAGE1_MANIFEST"]
    tracked = manifest.get("members")
    if not isinstance(tracked, dict):
        return ["INVALID_MANIFEST_MEMBERS"]
    defects: list[str] = []
    actual_names = set(members) - {"stage1-manifest.json"}
    if set(tracked) != actual_names:
        defects.append("MANIFEST_MEMBER_SET_MISMATCH")
    for name, meta in tracked.items():
        data = members.get(name)
        if data is None or not isinstance(meta, dict):
            defects.append("MANIFEST_MISSING_MEMBER:" + name)
            continue
        size = meta.get("size", meta.get("bytes"))
        if size != len(data) or meta.get("sha256") != digest(data):
            defects.append("MANIFEST_MISMATCH:" + name)
    return defects


def load_json(members: dict[str, bytes], name: str, defects: list[str]) -> Any:
    raw = members.get(name)
    if raw is None:
        defects.append("MISSING_" + name.upper().replace("/", "_").replace("-", "_"))
        return None
    try:
        return json.loads(raw.decode("utf-8-sig"))
    except (json.JSONDecodeError, UnicodeError):
        defects.append("INVALID_" + name.upper().replace("/", "_").replace("-", "_"))
        return None


def read_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("authority_type") != "OWNER_APPROVED_EARLY_AGGREGATE_COVERAGE":
        raise ValueError("INVALID_OWNER_AUTHORITY_REGISTRY")
    if not isinstance(data.get("cases"), list):
        raise ValueError("INVALID_OWNER_AUTHORITY_REGISTRY")
    return data


def authority_case(registry: dict[str, Any], school: str, season: str) -> dict[str, Any] | None:
    matches = [case for case in registry["cases"] if case.get("school_key") == school and case.get("season") == season]
    if len(matches) > 1:
        raise ValueError("DUPLICATE_OWNER_AUTHORITY:" + season)
    return matches[0] if matches else None


def normalize_proposals(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict) and isinstance(value.get("cases"), list):
        value = value["cases"]
    elif isinstance(value, dict):
        value = [value]
    if not isinstance(value, list) or not value or any(not isinstance(item, dict) for item in value):
        raise ValueError("INVALID_AGGREGATE_PROPOSAL")
    return value


def row_result(row: dict[str, str]) -> tuple[str, str, str, bool]:
    team = first(row, "accepted_team_score", "team_score", "source_program_score")
    opponent = first(row, "accepted_opponent_score", "opponent_score", "opponent_points")
    played = first(row, "accepted_result", "played_result", "on_court_result", "source_result", "result").upper()
    if played in {"W", "L", "T"}:
        return team, opponent, played, True
    if bool(team) != bool(opponent):
        return team, opponent, "", False
    if team and opponent:
        try:
            a, b = int(team), int(opponent)
        except ValueError:
            return team, opponent, "", False
        return team, opponent, "W" if a > b else "L" if a < b else "T", True
    return team, opponent, "", False


def census_int(row: dict[str, str], *names: str) -> int | None:
    value = first(row, *names)
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def evidence_sources_ok(value: Any, minimum: int) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= minimum
        and all(
            isinstance(item, dict)
            and str(item.get("source", "")).strip()
            and str(item.get("authority", "")).strip()
            and str(item.get("finding", "")).strip()
            for item in value
        )
    )


def audit_candidate(candidate: Path, *, expected_candidate_sha256: str, registry_path: Path = REGISTRY) -> dict[str, Any]:
    try:
        members, candidate_sha = read_zip(candidate, expected_candidate_sha256)
        registry = read_registry(registry_path)
    except (OSError, ValueError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        return {"status": "FAIL", "defects": [str(exc)], "stage1_complete": False}

    defects = manifest_defects(members)
    status = load_json(members, "stage1-status.json", defects)
    manifest = load_json(members, "stage1-manifest.json", defects)
    blockers = load_json(members, "blocking-residuals.json", defects)
    agg_proposal_raw = load_json(members, AGG_PROPOSAL, defects)
    uncertainty = load_json(members, UNCERTAINTY_PROPOSAL, defects)
    agg_evidence_raw = load_json(members, AGG_EVIDENCE, defects)
    try:
        ledger = csv_rows(members["structured-stage1-ledger.csv"])
        census = csv_rows(members["season-census.csv"])
    except (KeyError, csv.Error, UnicodeError):
        defects.append("MISSING_OR_INVALID_HISTORICAL_CORE")
        ledger, census = [], []

    if not isinstance(status, dict) or not isinstance(manifest, dict) or not isinstance(blockers, list):
        defects.append("INVALID_STATUS_MANIFEST_OR_BLOCKERS")
        return {"status": "FAIL", "checkpoint_sha256": candidate_sha, "defects": sorted(set(defects)), "stage1_complete": False}

    school = str(status.get("school_key") or status.get("school") or manifest.get("school_key") or "").strip()
    research_base = str(status.get("research_base_sha") or manifest.get("research_base_sha") or "").strip()
    authority_parent = str(status.get("parent_checkpoint_sha256") or manifest.get("parent_checkpoint_sha256") or "").strip()
    if not school:
        defects.append("MISSING_SCHOOL_KEY")
    if not research_base or manifest.get("research_base_sha") != research_base:
        defects.append("RESEARCH_BASE_MISMATCH")
    if not authority_parent:
        defects.append("MISSING_AUTHORITY_PARENT_CHECKPOINT")
    if status.get("stage1_complete") is True or str(status.get("stage", "")) != "STAGE_1":
        defects.append("CANDIDATE_NOT_INCOMPLETE_STAGE1")
    if status.get("blocking_residual_count") != len(blockers) or manifest.get("blocking_residuals") != len(blockers):
        defects.append("BLOCKER_COUNT_CONFLICT")
    if status.get("total_candidate_game_rows", status.get("identified_competitive_games")) != len(ledger) or manifest.get("game_rows") != len(ledger):
        defects.append("LEDGER_COUNT_CONFLICT")

    ids = [first(row, "research_game_id") for row in ledger]
    if not ledger or not all(ids) or len(ids) != len(set(ids)):
        defects.append("BLANK_OR_DUPLICATE_GAME_IDS")
    for row in ledger:
        if not first(row, "opponent_literal", "source_opponent_label", "source_opponent_text") or not first(row, "game_type"):
            defects.append("UNIDENTIFIED_OR_UNTYPED_LEDGER_GAME")
            break
        state = first(row, "game_universe_state").upper()
        if "PLACEHOLDER" in state or "UNIDENTIFIED" in state:
            defects.append("FABRICATED_PLACEHOLDER_GAME_ROW")
            break

    by_id = {first(row, "research_game_id"): row for row in ledger if first(row, "research_game_id")}
    by_season: dict[str, list[dict[str, str]]] = {}
    known = Counter()
    unknown_ids: set[str] = set()
    for row in ledger:
        season = first(row, "season_label", "season")
        by_season.setdefault(season, []).append(row)
        team, opp, result, is_known = row_result(row)
        gid = first(row, "research_game_id")
        if bool(team) != bool(opp):
            defects.append("ONE_SIDED_SCORE:" + gid)
        if is_known:
            known[result] += 1
        elif not team and not opp:
            unknown_ids.add(gid)

    aggregate_blockers = [item for item in blockers if isinstance(item, dict) and item.get("class") == AGG_BLOCKER]
    unknown_blockers = [item for item in blockers if isinstance(item, dict) and item.get("class") == UNKNOWN_RESULT_BLOCKER]
    unrelated = [item for item in blockers if not isinstance(item, dict) or item.get("class") not in {AGG_BLOCKER, UNKNOWN_RESULT_BLOCKER}]
    if unrelated:
        defects.append("UNRELATED_STAGE1_BLOCKERS")
    if not aggregate_blockers or not unknown_blockers:
        defects.append("MIXED_TERMINAL_POPULATION_REQUIRED")

    try:
        proposals = normalize_proposals(agg_proposal_raw)
    except ValueError as exc:
        defects.append(str(exc))
        proposals = []
    proposal_by_season = {str(item.get("season", "")): item for item in proposals if str(item.get("season", ""))}
    if len(proposal_by_season) != len(proposals):
        defects.append("DUPLICATE_OR_BLANK_AGGREGATE_PROPOSAL_SEASON")

    if isinstance(agg_evidence_raw, dict) and isinstance(agg_evidence_raw.get("seasons"), list):
        evidence_items = agg_evidence_raw["seasons"]
    elif isinstance(agg_evidence_raw, dict):
        evidence_items = [agg_evidence_raw]
    else:
        evidence_items = []
    evidence_by_season = {str(item.get("season", "")): item for item in evidence_items if isinstance(item, dict) and str(item.get("season", ""))}

    aggregate_coverage: list[dict[str, Any]] = []
    agg_seasons: set[str] = set()
    for blocker in aggregate_blockers:
        season = str(blocker.get("season", "")).strip()
        if not season or season in agg_seasons:
            defects.append("DUPLICATE_OR_BLANK_AGGREGATE_BLOCKER")
            continue
        agg_seasons.add(season)
        if blocker.get("research_state") != "RESEARCH_EXHAUSTED_SOURCE_COVERAGE":
            defects.append("AGGREGATE_RESEARCH_NOT_EXHAUSTED:" + season)
        if blocker.get("terminal_classification") not in (None, "", AGG_TERMINAL):
            defects.append("AGGREGATE_TERMINAL_CLASS_MISMATCH:" + season)
        if not str(blocker.get("research_evidence_summary", "")).strip():
            defects.append("MISSING_AGGREGATE_RESEARCH_PROVENANCE:" + season)

        proposal = proposal_by_season.get(season)
        authority = authority_case(registry, school, season) if school else None
        if proposal is None:
            defects.append("MISSING_AGGREGATE_PROPOSAL:" + season)
            proposal = {}
        if authority is None:
            defects.append("NO_EXACT_OWNER_AUTHORITY:" + season)
            authority = {}
        if proposal != authority:
            defects.append("PROPOSED_AUTHORITY_REGISTRY_MISMATCH:" + season)
        if authority.get("parent_checkpoint_sha256") != authority_parent or authority.get("research_base_sha") != research_base:
            defects.append("OWNER_AUTHORITY_BINDING_MISMATCH:" + season)
        if not str(authority.get("owner_disposition", "")).startswith("https://github.com/"):
            defects.append("OWNER_DISPOSITION_PROVENANCE_MISSING:" + season)
        if authority.get("identified_rows") != len(ledger) or authority.get("identified_ledger_sha256") != digest(members.get("structured-stage1-ledger.csv", b"")):
            defects.append("IDENTIFIED_LEDGER_AUTHORITY_MISMATCH:" + season)
        year = int(season[:4]) if season[:4].isdigit() else 9999
        if year > int(authority.get("maximum_eligible_season_start_year", 0) or 0):
            defects.append("OUTSIDE_FOUNDING_ERA:" + season)

        rows = by_season.get(season, [])
        tally = Counter()
        for row in rows:
            _, _, result, is_known = row_result(row)
            if not is_known or result not in {"W", "L"}:
                defects.append("UNRESOLVED_AGGREGATE_SEASON_GAME_OUTCOME:" + season)
            else:
                tally[result] += 1
        identified = {"wins": tally["W"], "losses": tally["L"], "games": len(rows)}
        institutional = authority.get("institutional_record", {})
        expected_identified = authority.get("identified_record", {})
        if identified != expected_identified:
            defects.append("IDENTIFIED_RECORD_AUTHORITY_MISMATCH:" + season)
        if institutional.get("wins", -1) + institutional.get("losses", -1) != institutional.get("games", -2):
            defects.append("INSTITUTIONAL_RECORD_ARITHMETIC:" + season)
        difference = {
            "wins": institutional.get("wins", 0) - identified.get("wins", 0),
            "losses": institutional.get("losses", 0) - identified.get("losses", 0),
            "games": institutional.get("games", 0) - identified.get("games", 0),
        }
        if difference != authority.get("unidentified_record") or difference.get("games", 0) <= 0 or difference["wins"] + difference["losses"] != difference["games"]:
            defects.append("AGGREGATE_RESIDUAL_ARITHMETIC_MISMATCH:" + season)

        crows = [row for row in census if first(row, "season", "season_label") == season]
        if len(crows) != 1:
            defects.append("MISSING_OR_DUPLICATE_SEASON_CENSUS:" + season)
        else:
            c = crows[0]
            checks = {
                "institutional_wins": census_int(c, "source_aggregate_wins", "source_all_time_record_wins", "institutional_wins", "source_year_by_year_wins"),
                "institutional_losses": census_int(c, "source_aggregate_losses", "source_all_time_record_losses", "institutional_losses", "source_year_by_year_losses"),
                "institutional_games": census_int(c, "source_aggregate_games", "source_all_time_record_games", "institutional_games"),
                "identified_games": census_int(c, "accepted_or_identified_rows", "identified_competitive_games", "observed_games"),
                "identified_wins": census_int(c, "known_played_wins", "identified_wins"),
                "identified_losses": census_int(c, "known_played_losses", "identified_losses"),
            }
            expected = {
                "institutional_wins": institutional.get("wins"),
                "institutional_losses": institutional.get("losses"),
                "institutional_games": institutional.get("games"),
                "identified_games": identified.get("games"),
                "identified_wins": identified.get("wins"),
                "identified_losses": identified.get("losses"),
            }
            if checks != expected:
                defects.append("SEASON_CENSUS_AGGREGATE_MISMATCH:" + season)

        detail = blocker.get("detail", {}) if isinstance(blocker.get("detail"), dict) else {}
        if int(detail.get("identified_game_rows", detail.get("observed_games", -1))) != len(rows) or int(detail.get("unidentified_game_rows", detail.get("unidentified_games", -1))) != difference.get("games"):
            defects.append("AGGREGATE_BLOCKER_COUNT_MISMATCH:" + season)

        evidence = evidence_by_season.get(season)
        if not isinstance(evidence, dict):
            defects.append("MISSING_AGGREGATE_EVIDENCE:" + season)
        else:
            if evidence.get("policy_result") != "RESEARCH_EXHAUSTED_IDENTITIES_UNRESOLVED" or evidence.get("identified_game_rows") != len(rows) or evidence.get("unidentified_game_rows") != difference.get("games") or evidence.get("rows_added") != 0 or evidence.get("accepted_game_rows_before") != len(ledger) or evidence.get("accepted_game_rows_after") != len(ledger) or evidence.get("anonymous_placeholder_rows") != 0 or evidence.get("rows_added_from_aggregate_inference") != 0:
                defects.append("AGGREGATE_EVIDENCE_EXHAUSTION_INCONSISTENT:" + season)
            sources = evidence.get("systematic_evidence_checked")
            if not evidence_sources_ok(sources, 3) or not any("target institutional" in str(item.get("authority", "")) for item in sources or []):
                defects.append("INADEQUATE_AGGREGATE_INSTITUTIONAL_EVIDENCE:" + season)
            if evidence.get("school_key") != school or evidence.get("season") != season or evidence.get("institutional_record") != institutional:
                defects.append("AGGREGATE_EVIDENCE_AUTHORITY_MISMATCH:" + season)

        aggregate_coverage.append({
            "school_key": school,
            "season": season,
            "institutional_record": institutional,
            "identified_record": identified,
            "unidentified_record": difference,
            "owner_disposition": authority.get("owner_disposition"),
            "authority_parent_checkpoint_sha256": authority_parent,
            "candidate_checkpoint_sha256": candidate_sha,
            "research_base_sha": research_base,
            "terminal_classification": AGG_TERMINAL,
            "warning": "Season-level institutional aggregate only. No unidentified game row, opponent, date, site, score, or row-level result allocation is represented.",
        })

    if set(proposal_by_season) != agg_seasons:
        defects.append("AGGREGATE_PROPOSAL_POPULATION_MISMATCH")
    if set(evidence_by_season) != agg_seasons:
        defects.append("AGGREGATE_EVIDENCE_POPULATION_MISMATCH")
    authority_seasons = {
        str(case.get("season", ""))
        for case in registry.get("cases", [])
        if case.get("school_key") == school
        and case.get("parent_checkpoint_sha256") == authority_parent
        and case.get("research_base_sha") == research_base
    }
    if authority_seasons != agg_seasons:
        defects.append("OWNER_AUTHORITY_POPULATION_MISMATCH")

    if not isinstance(uncertainty, dict):
        defects.append("INVALID_EARLY_HISTORY_UNCERTAINTY_PROPOSAL")
        uncertainty = {}
    class_a = uncertainty.get("class_a", [])
    class_b = uncertainty.get("class_b", [])
    if class_a not in ([], None):
        defects.append("MIXED_COORDINATOR_CLASS_A_NOT_SUPPORTED")
    if not isinstance(class_b, list) or not class_b:
        defects.append("MISSING_CLASS_B_UNKNOWN_RESULT_POPULATION")
        class_b = []

    summary_expected = {
        "identified_game_count": len(ledger),
        "known_result_game_count": sum(known.values()),
        "known_result_wins": known["W"],
        "known_result_losses": known["L"],
        "known_result_ties": known["T"],
    }
    for key, expected in summary_expected.items():
        if uncertainty.get(key) != expected:
            defects.append("UNCERTAINTY_SUMMARY_COUNT_MISMATCH:" + key)
    if uncertainty.get("school_key") != school or uncertainty.get("research_base_sha") != research_base or uncertainty.get("parent_checkpoint_sha256") != authority_parent:
        defects.append("UNCERTAINTY_AUTHORITY_BINDING_MISMATCH")

    class_b_ids: set[str] = set()
    uncertainty_records: list[dict[str, Any]] = []
    blocker_by_id = {str(item.get("research_game_id", "")): item for item in unknown_blockers if isinstance(item, dict)}
    if len(blocker_by_id) != len(unknown_blockers):
        defects.append("BLANK_OR_DUPLICATE_UNKNOWN_RESULT_BLOCKER_ID")
    for item in class_b:
        if not isinstance(item, dict):
            defects.append("INVALID_CLASS_B_RECORD")
            continue
        gid = str(item.get("research_game_id", "")).strip()
        if not gid or gid in class_b_ids:
            defects.append("BLANK_OR_DUPLICATE_CLASS_B_GAME_ID")
            continue
        class_b_ids.add(gid)
        row = by_id.get(gid)
        if row is None:
            defects.append("CLASS_B_GAME_ID_NOT_IN_LEDGER:" + gid)
            continue
        team, opp, result, is_known = row_result(row)
        if team or opp or result or is_known:
            defects.append("CLASS_B_RESULT_NOT_GENUINELY_UNKNOWN:" + gid)
        if item.get("competitive_inclusion") is not True or "IDENTIFIED_COMPETITIVE" not in first(row, "game_universe_state").upper():
            defects.append("CLASS_B_COMPETITIVE_INCLUSION_NOT_ESTABLISHED:" + gid)
        if str(item.get("game_type", "")).strip() != first(row, "game_type"):
            defects.append("CLASS_B_GAME_TYPE_MISMATCH:" + gid)
        opponent_literal = first(row, "opponent_literal", "source_opponent_label", "source_opponent_text")
        if str(item.get("opponent_literal", "")).strip() != opponent_literal:
            defects.append("CLASS_B_LITERAL_OPPONENT_MISMATCH:" + gid)
        if item.get("direct_score_or_result_evidence_present") is not False:
            defects.append("CLASS_B_DIRECT_RESULT_EVIDENCE_NOT_EXCLUDED:" + gid)
        if item.get("aggregate_result_allocation_used") is not False:
            defects.append("CLASS_B_AGGREGATE_ALLOCATION_NOT_EXCLUDED:" + gid)
        if item.get("research_exhausted") is not True or not evidence_sources_ok(item.get("systematic_evidence_checked"), 2):
            defects.append("CLASS_B_RESEARCH_NOT_EXHAUSTED:" + gid)
        blocker = blocker_by_id.get(gid)
        if blocker is None:
            defects.append("CLASS_B_BLOCKER_MISSING:" + gid)
        else:
            if blocker.get("research_state") != "RESEARCHED_UNRESOLVED":
                defects.append("CLASS_B_BLOCKER_STATE_MISMATCH:" + gid)
            if blocker.get("terminal_classification") not in (None, "", UNKNOWN_RESULT_TERMINAL):
                defects.append("CLASS_B_TERMINAL_CLASS_MISMATCH:" + gid)
            if str(blocker.get("season", "")) != first(row, "season_label", "season"):
                defects.append("CLASS_B_BLOCKER_SEASON_MISMATCH:" + gid)
            if not str(blocker.get("research_evidence_summary", "")).strip():
                defects.append("CLASS_B_RESEARCH_PROVENANCE_MISSING:" + gid)
        uncertainty_records.append({
            "school_key": school,
            "research_game_id": gid,
            "season": first(row, "season_label", "season"),
            "opponent_literal": opponent_literal,
            "game_type": first(row, "game_type"),
            "terminal_classification": UNKNOWN_RESULT_TERMINAL,
            "warning": "Identified competitive game with genuinely unknown result. No season aggregate is allocated to this row.",
            "systematic_evidence_checked": item.get("systematic_evidence_checked", []),
        })

    if class_b_ids != unknown_ids:
        defects.append("CLASS_B_UNKNOWN_RESULT_POPULATION_MISMATCH")
    if class_b_ids != set(blocker_by_id):
        defects.append("CLASS_B_BLOCKER_POPULATION_MISMATCH")

    aggregate_coverage.sort(key=lambda item: item["season"])
    uncertainty_records.sort(key=lambda item: item["research_game_id"])
    payload = {
        "schema_version": 1,
        "school_key": school,
        "research_base_sha": research_base,
        "candidate_checkpoint_sha256": candidate_sha,
        "authority_parent_checkpoint_sha256": authority_parent,
        "identified_game_count": len(ledger),
        "identified_ledger_sha256": digest(members.get("structured-stage1-ledger.csv", b"")),
        "season_census_sha256": digest(members.get("season-census.csv", b"")),
        "aggregate_coverage": aggregate_coverage,
        "unknown_result_games": uncertainty_records,
        "terminal_classifications": [AGG_TERMINAL, UNKNOWN_RESULT_TERMINAL],
        "historical_ledger_mutation": "NONE",
        "season_census_mutation": "NONE",
    }
    return {
        **payload,
        "status": ELIGIBLE if not defects else "FAIL",
        "defects": sorted(set(defects)),
        "stage1_complete": False,
    }


def verified_audit(candidate: Path, audit_path: Path, *, candidate_sha: str, audit_sha: str, registry_path: Path) -> tuple[dict[str, Any], dict[str, bytes]]:
    raw = audit_path.read_bytes()
    if not audit_sha or digest(raw) != audit_sha:
        raise ValueError("AUDIT_HASH_MISMATCH_OR_UNPINNED")
    provided = json.loads(raw.decode("utf-8"))
    computed = audit_candidate(candidate, expected_candidate_sha256=candidate_sha, registry_path=registry_path)
    if computed.get("status") != ELIGIBLE or provided != computed:
        raise ValueError("AUDIT_NOT_ELIGIBLE_OR_CONTENT_MISMATCH")
    members, _ = read_zip(candidate, candidate_sha)
    return computed, members


def successor_members(candidate_members: dict[str, bytes], audit: dict[str, Any], audit_sha: str) -> dict[str, bytes]:
    result = dict(candidate_members)
    status = json.loads(result["stage1-status.json"])
    status.update({
        "status": "COMPLETE",
        "stage1_complete": True,
        "blocking_residual_count": 0,
        "next_action": "STAGE_2_AFTER_OWNER_AUTHORIZATION",
        "next_bounded_stage": "STAGE_2_AFTER_OWNER_AUTHORIZATION",
        "mixed_terminal_audit_sha256": audit_sha,
        "mixed_terminal_candidate_sha256": audit["candidate_checkpoint_sha256"],
        "terminal_historical_debt": audit["terminal_classifications"],
    })
    result["stage1-status.json"] = json_bytes(status)
    result["blocking-residuals.json"] = b"[]\n"

    aggregate_payload = {
        "schema_version": 1,
        "school_key": audit["school_key"],
        "research_base_sha": audit["research_base_sha"],
        "candidate_checkpoint_sha256": audit["candidate_checkpoint_sha256"],
        "authority_parent_checkpoint_sha256": audit["authority_parent_checkpoint_sha256"],
        "audit_sha256": audit_sha,
        "coverage": audit["aggregate_coverage"],
    }
    uncertainty_payload = json.loads(result[UNCERTAINTY_PROPOSAL])
    uncertainty_payload.update({
        "candidate_checkpoint_sha256": audit["candidate_checkpoint_sha256"],
        "audit_sha256": audit_sha,
        "terminal_classifications": {"class_b": UNKNOWN_RESULT_TERMINAL},
    })
    mixed_payload = {
        "schema_version": 1,
        "status": "STAGE_1_COMPLETE_MIXED_EARLY_HISTORY_TERMINALS",
        "school_key": audit["school_key"],
        "research_base_sha": audit["research_base_sha"],
        "candidate_checkpoint_sha256": audit["candidate_checkpoint_sha256"],
        "authority_parent_checkpoint_sha256": audit["authority_parent_checkpoint_sha256"],
        "audit_sha256": audit_sha,
        "identified_game_count": audit["identified_game_count"],
        "identified_ledger_sha256": audit["identified_ledger_sha256"],
        "season_census_sha256": audit["season_census_sha256"],
        "aggregate_coverage": audit["aggregate_coverage"],
        "unknown_result_games": audit["unknown_result_games"],
        "terminal_classifications": audit["terminal_classifications"],
        "historical_ledger_mutation": "NONE",
        "season_census_mutation": "NONE",
    }
    result[MIXED_CLOSEOUT] = json_bytes(mixed_payload)
    result[AGG_CLOSEOUT] = json_bytes(aggregate_payload)
    result[UNCERTAINTY_CLOSEOUT] = json_bytes(uncertainty_payload)
    result[STAGE4_AGG] = json_bytes({"schema_version": 1, "coverage": audit["aggregate_coverage"]})
    result[STAGE4_UNCERTAINTY] = json_bytes(uncertainty_payload)

    manifest = json.loads(result["stage1-manifest.json"])
    manifest.update({
        "status": "COMPLETE",
        "blocking_residuals": 0,
        "mixed_terminal_audit_sha256": audit_sha,
        "mixed_terminal_candidate_sha256": audit["candidate_checkpoint_sha256"],
        "terminal_historical_debt": audit["terminal_classifications"],
    })
    manifest["members"] = {
        name: {"size": len(data), "sha256": digest(data)}
        for name, data in sorted(result.items())
        if name != "stage1-manifest.json"
    }
    result["stage1-manifest.json"] = json_bytes(manifest)
    return result


def serialize_zip(members: dict[str, bytes], output: Path) -> str:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, members[name])
    data = buffer.getvalue()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return digest(data)


def closeout(candidate: Path, audit_path: Path, output: Path, *, candidate_sha: str, audit_sha: str, registry_path: Path = REGISTRY) -> dict[str, Any]:
    audit, members = verified_audit(candidate, audit_path, candidate_sha=candidate_sha, audit_sha=audit_sha, registry_path=registry_path)
    successor = successor_members(members, audit, audit_sha)
    sha = serialize_zip(successor, output)
    return {
        "status": "STAGE1_MIXED_TERMINAL_CLOSEOUT_CANDIDATE_CREATED",
        "candidate_checkpoint_sha256": candidate_sha,
        "closeout_checkpoint_sha256": sha,
        "audit_sha256": audit_sha,
        "stage1_complete": False,
        "next_action": "Independently verify-closeout before declaring Stage 1 COMPLETE.",
    }


def verify_closeout(candidate: Path, successor: Path, audit_path: Path, *, candidate_sha: str, successor_sha: str, audit_sha: str, registry_path: Path = REGISTRY) -> dict[str, Any]:
    defects: list[str] = []
    try:
        audit, original = verified_audit(candidate, audit_path, candidate_sha=candidate_sha, audit_sha=audit_sha, registry_path=registry_path)
        actual, _ = read_zip(successor, successor_sha)
        expected = successor_members(original, audit, audit_sha)
        defects.extend(manifest_defects(actual))
        if actual != expected:
            defects.append("CLOSEOUT_CONTENT_DRIFT")
        for name in ("structured-stage1-ledger.csv", "season-census.csv"):
            if actual.get(name) != original.get(name):
                defects.append("HISTORICAL_CORE_DRIFT:" + name)
        mutable = {
            "stage1-manifest.json",
            "stage1-status.json",
            "blocking-residuals.json",
            MIXED_CLOSEOUT,
            AGG_CLOSEOUT,
            UNCERTAINTY_CLOSEOUT,
            STAGE4_AGG,
            STAGE4_UNCERTAINTY,
        }
        for name, data in original.items():
            if name not in mutable and actual.get(name) != data:
                defects.append("IMMUTABLE_CANDIDATE_MEMBER_DRIFT:" + name)
    except (OSError, ValueError, KeyError, TypeError, csv.Error, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        return {"status": "FAIL", "defects": [str(exc)], "stage1_complete": False}
    return {
        "schema_version": 1,
        "status": VERIFIED if not defects else "FAIL",
        "defects": sorted(set(defects)),
        "stage1_complete": not defects,
        "school_key": audit["school_key"],
        "research_base_sha": audit["research_base_sha"],
        "candidate_checkpoint_sha256": candidate_sha,
        "closeout_checkpoint_sha256": successor_sha,
        "audit_sha256": audit_sha,
        "identified_game_count": audit["identified_game_count"],
        "identified_ledger_sha256": audit["identified_ledger_sha256"],
        "season_census_sha256": audit["season_census_sha256"],
        "terminal_classifications": audit["terminal_classifications"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    audit_p = sub.add_parser("audit")
    audit_p.add_argument("candidate", type=Path)
    audit_p.add_argument("--expected-candidate-sha256", required=True)
    audit_p.add_argument("--registry", type=Path, default=REGISTRY)
    audit_p.add_argument("--output", type=Path)

    close_p = sub.add_parser("closeout")
    close_p.add_argument("candidate", type=Path)
    close_p.add_argument("audit", type=Path)
    close_p.add_argument("--expected-candidate-sha256", required=True)
    close_p.add_argument("--expected-audit-sha256", required=True)
    close_p.add_argument("--registry", type=Path, default=REGISTRY)
    close_p.add_argument("--output", type=Path, required=True)

    verify_p = sub.add_parser("verify-closeout")
    verify_p.add_argument("candidate", type=Path)
    verify_p.add_argument("closeout", type=Path)
    verify_p.add_argument("audit", type=Path)
    verify_p.add_argument("--expected-candidate-sha256", required=True)
    verify_p.add_argument("--expected-closeout-sha256", required=True)
    verify_p.add_argument("--expected-audit-sha256", required=True)
    verify_p.add_argument("--registry", type=Path, default=REGISTRY)
    verify_p.add_argument("--output", type=Path)

    args = parser.parse_args(argv)
    try:
        if args.command == "audit":
            report = audit_candidate(args.candidate, expected_candidate_sha256=args.expected_candidate_sha256, registry_path=args.registry)
            ok = report.get("status") == ELIGIBLE
        elif args.command == "closeout":
            report = closeout(args.candidate, args.audit, args.output, candidate_sha=args.expected_candidate_sha256, audit_sha=args.expected_audit_sha256, registry_path=args.registry)
            ok = True
        else:
            report = verify_closeout(args.candidate, args.closeout, args.audit, candidate_sha=args.expected_candidate_sha256, successor_sha=args.expected_closeout_sha256, audit_sha=args.expected_audit_sha256, registry_path=args.registry)
            ok = report.get("status") == VERIFIED
    except (OSError, ValueError, KeyError, TypeError, csv.Error, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        report = {"status": "FAIL", "defects": [str(exc)], "stage1_complete": False}
        ok = False

    rendered = json_bytes(report)
    if getattr(args, "output", None) and args.command != "closeout":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(rendered)
    print(rendered.decode("utf-8"), end="")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
