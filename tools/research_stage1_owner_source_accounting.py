#!/usr/bin/env python3
"""Fail-closed, owner-scoped Fresno 1965-66 Stage 1 source-accounting closeout.

Issue #732. Distinguishes the 29-game institutional 21-8 aggregate from the
28 identified 21-7 games without manufacturing an unidentified game.

Commands:
  audit CHECKPOINT_DIR --expected-parent-sha SHA --output REPORT.json
  closeout CHECKPOINT_DIR AUDIT.json --expected-parent-sha SHA
      --expected-audit-sha256 SHA --output SUCCESSOR.zip
  verify-closeout CHECKPOINT_DIR SUCCESSOR.zip AUDIT.json
      --expected-parent-sha SHA --expected-audit-sha256 SHA
      --expected-closeout-sha256 SHA --output REPORT.json

The separate closeout stays INCOMPLETE until independent verification passes.
No command writes to the parent checkpoint, research branch or protected main.
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
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_PATH = ROOT / "data/governance/research-stage1-owner-source-accounting-authorities.json"
MANIFEST = "manifest-0035.json"
SOURCE = "stage1-source-dispositions.csv"
LEDGER = "stage1-accepted-game-ledger.csv"
CENSUS = "49-season-stage1-census.csv"
CANDIDATE = "49-season-stage1-census-owner-ruling-CANDIDATE.csv"
PENDING = "stage1-pending-source-groups.csv"
RULING = "owner-1965-66-ruling.json"
TERMINAL = "OWNER_ACCEPTED_SOURCE_ACCOUNTING_UNCERTAINTY"
CANDIDATE_STATUS = (
    "OWNER_ACCEPTED_NONBLOCKING_SOURCE_AGGREGATE_TYPO__"
    "POSSIBLE_UNIDENTIFIED_LOSS_RETAINED"
)
SOURCE_CLASSES = {
    "ACCEPTED_NEW_COMPETITIVE_SOURCE_GAME": 933,
    "INHERITED_PRIOR_ACCEPTED_RESEARCH_ID": 78,
    "EXCLUDED_NONCOMPETITIVE_EVENT": 17,
    "DUPLICATE_SOURCE_REPRESENTATION_NO_EXTRA_GAME": 2,
    "OWNER_APPROVED_UNATTRIBUTED_CONFLICTING_FRESNO_SCORE_CLAIM": 4,
    "EXCLUDED_OWNER_DIRECTED_EXHIBITION": 2,
}
GAME_ACCEPTED_CLASSES = {
    "ACCEPTED_NEW_COMPETITIVE_SOURCE_GAME",
    "INHERITED_PRIOR_ACCEPTED_RESEARCH_ID",
}
EXHIBITION_IDS = {
    "FRESNO-EXP-CAND-1935-36-019": ("Broadway Clowns", "L", "37-34"),
    "FRESNO-EXP-CAND-1953-54-018": ("Harlem Clowns", "W", "82-61"),
}
UCD_UNASSIGNED_IDS = {
    "FRESNO-EXP-CAND-1926-27-006", "FRESNO-EXP-CAND-1926-27-007",
    "FRESNO-EXP-CAND-1926-27-012", "FRESNO-EXP-CAND-1926-27-013",
}
UCD_GAME_IDS = {
    "FRESNO-EXP-RECIP-UCD-1926-27-04",
    "FRESNO-EXP-RECIP-UCD-1926-27-05",
}


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def table(raw: bytes) -> list[dict[str, str]]:
    text = raw.decode("utf-8-sig")
    if not text.endswith("\n"):
        raise ValueError("CSV_TRAILING_NEWLINE_REQUIRED")
    data = list(csv.DictReader(io.StringIO(text, newline="")))
    if not data or any(None in row or None in row.values() for row in data):
        raise ValueError("CSV_INVALID_OR_EMPTY")
    return data


def one(rows: list[dict], field: str, value: str) -> dict:
    matches = [row for row in rows if row.get(field) == value]
    if len(matches) != 1:
        raise ValueError("EXPECTED_EXACTLY_ONE:" + field + ":" + value)
    return matches[0]


def require(ok: object, message: str) -> None:
    if not ok:
        raise ValueError(message)


def load_authority() -> dict:
    data = json.loads(AUTHORITY_PATH.read_bytes())
    require(data.get("schema_version") == 1
            and data.get("authority_type") == "EXACT_OWNER_STAGE1_SOURCE_ACCOUNTING_UNCERTAINTY",
            "INVALID_GOVERNANCE_REGISTRY")
    cases = data.get("cases", [])
    require(isinstance(cases, list) and len(cases) == 1, "REGISTRY_MUST_CONTAIN_ONE_CASE")
    case = cases[0]
    require(case.get("owner_disposition_issue")
            == "https://github.com/pollackelliott/college-basketball-history/issues/732",
            "UNAPPROVED_OWNER_AUTHORITY")
    return case


def authenticated_parent(checkpoint: Path, case: dict) -> dict[str, bytes]:
    require(checkpoint.is_dir(), "PARENT_CHECKPOINT_DIRECTORY_REQUIRED")
    require(set(p.name for p in checkpoint.iterdir()) == {MANIFEST, *case["member_git_blobs"]},
            "PARENT_MEMBER_SET_MISMATCH")
    manifest_raw = (checkpoint / MANIFEST).read_bytes()
    require(git_blob(manifest_raw) == case["checkpoint_manifest_blob_sha"],
            "PARENT_MANIFEST_GIT_BLOB_SHA_MISMATCH")
    manifest = json.loads(manifest_raw)
    require(manifest.get("research_parent_sha") == case["checkpoint_previous_research_sha"]
            and manifest.get("parent_tree_sha") == case["checkpoint_previous_tree_sha"]
            and manifest.get("immutable_research_base_sha") == case["research_base_sha"]
            and manifest.get("checkpoint_path") == case["checkpoint_path"]
            and manifest.get("school_key") == "fresno-state"
            and manifest.get("stage1_complete") is False,
            "PARENT_MANIFEST_CONTEXT_MISMATCH")
    require(manifest.get("members") == case["member_git_blobs"],
            "PARENT_MANIFEST_CONTENTS_DIFFER_FROM_AUTHORITY")
    raw = {MANIFEST: manifest_raw}
    for name, digest in case["member_git_blobs"].items():
        require("/" not in name and name not in {".", ".."},
                "UNSAFE_PARENT_MEMBER_NAME")
        item = checkpoint / name
        require(item.is_file() and not item.is_symlink(), "PARENT_MEMBER_NOT_REGULAR:" + name)
        raw[name] = item.read_bytes()
        require(git_blob(raw[name]) == digest, "PARENT_MEMBER_GIT_HASH_MISMATCH:" + name)
    return raw


def verify_semantics(raw: dict[str, bytes], case: dict) -> dict:
    games = table(raw[LEDGER])
    sources = table(raw[SOURCE])
    seasons = table(raw[CENSUS])
    proposed = table(raw[CANDIDATE])
    require(len(games) == 1011 and len(sources) == 1036
            and len(seasons) == 49 and len(proposed) == 49,
            "EXACT_POPULATION_CHANGED")
    require(raw[PENDING].decode("utf-8").count("\n") == 1
            and raw[PENDING].decode("utf-8").strip() == "\"source_entry_id\",\"season\",\"guide_source\",\"blocker\",\"needed_evidence\"",
            "OTHER_PENDING_SOURCE_GROUPS")
    require(len({g["research_game_id"] for g in games}) == len(games)
            and len({g["source_entry_id"] for g in games}) == len(games),
            "DUPLICATE_OR_BLANK_GAME_ID")
    require(all(g["research_game_id"] and g["source_entry_id"]
                and g["inclusion"] in GAME_ACCEPTED_CLASSES
                and g["game_type"] in {"REGULAR_SEASON", "POSTSEASON", "NCAA_TOURNAMENT"}
                and g["played_result"] in {"W", "L"}
                and g["opponent_literal"].strip()
                and not re.search(r"\b(anonymous|unidentified|placeholder|tbd)\b",
                                  g["opponent_literal"], re.IGNORECASE)
                for g in games), "ANONYMOUS_OR_UNSUPPORTED_GAME")
    require(Counter(g["played_result"] for g in games) == Counter({"W": 532, "L": 479}),
            "GLOBAL_WL_CHANGED")
    require(len({s["source_entry_id"] for s in sources}) == len(sources)
            and Counter(s["stage1_bulk_disposition"] for s in sources) == SOURCE_CLASSES,
            "SOURCE_ID_OR_DISPOSITION_CHANGED")
    src = {s["source_entry_id"]: s for s in sources}
    ledger_ids = {g["research_game_id"] for g in games}
    require({s["stage1_curated_game_id"] for s in sources
             if s["stage1_bulk_disposition"] in GAME_ACCEPTED_CLASSES} == ledger_ids,
            "SOURCE_TO_GAME_SET_MISMATCH")
    for game in games:
        item = src.get(game["source_entry_id"])
        require(item is not None and item["stage1_bulk_disposition"] == game["inclusion"]
                and item["stage1_curated_game_id"] == game["research_game_id"]
                and item["season_label"] == game["season"]
                and item["source_raw_text"] == game["source_literal"],
                "GAME_SOURCE_JOIN_OR_LITERAL_MISMATCH")
    for identity, (opponent, result, score) in EXHIBITION_IDS.items():
        item = src[identity]
        require(item["stage1_bulk_disposition"] == "EXCLUDED_OWNER_DIRECTED_EXHIBITION"
                and item["literal_opponent"] == opponent
                and item["literal_result"] == result
                and item["literal_score"] == score
                and not item["stage1_curated_game_id"]
                and identity not in {g["source_entry_id"] for g in games},
                "CLOWNS_EXHIBITION_OWNER_DISPOSITION_CHANGED")
    require({s["source_entry_id"] for s in sources
             if s["stage1_bulk_disposition"]
             == "OWNER_APPROVED_UNATTRIBUTED_CONFLICTING_FRESNO_SCORE_CLAIM"}
            == UCD_UNASSIGNED_IDS, "UNASSIGNED_UCD_FRESNO_CLAIMS_CHANGED")
    for identity in UCD_UNASSIGNED_IDS:
        item = src[identity]
        require(item["literal_opponent"] == "UC Davis"
                and item["literal_result"] == "W"
                and not item["stage1_curated_game_id"]
                and item["stage1_identity_status"]
                == "OWNER_APPROVED_COUNT_TWO__FRESNO_SCORE_CLAIM_UNASSIGNED",
                "UCD_CONFLICTING_SOURCE_CLAIM_MISASSIGNED")
    require({g["research_game_id"] for g in games
             if g["research_game_id"].startswith("FRESNO-EXP-RECIP-UCD")}
            == UCD_GAME_IDS, "UCD_TWO_GAME_UNIVERSE_CHANGED")
    for identity in UCD_GAME_IDS:
        g = one(games, "research_game_id", identity)
        item = src[identity]
        require(g["season"] == "1926-27" and g["opponent_literal"] == "UC Davis"
                and g["played_result"] == "W" and g["source_literal_result"] == "L"
                and not g["team_points"] and not g["opponent_points"]
                and g["source_literal"] == "Fresno State | L"
                and item["stage1_identity_status"] == "OWNER_APPROVED_RECIPROCAL_DISTINCT_SOURCE_GAME",
                "UCD_RECIPROCAL_COUNT_RESULT_OR_SCORE_FABRICATED")
    census_map = {row["season"]: row for row in seasons}
    require(len(census_map) == 49, "DUPLICATE_CENSUS_SEASON")
    require([row["season"] for row in seasons] == [row["season"] for row in proposed],
            "CENSUS_SEASON_ORDER_CHANGED")
    groups = defaultdict(list)
    for g in games:
        require(g["season"] in census_map, "GAME_OUTSIDE_DECLARED_SEASON_CENSUS")
        groups[g["season"]].append(g)
    diffs = []
    for original, proposal in zip(seasons, proposed):
        season = original["season"]
        gr = groups[season]
        require(int(original["working_accepted_games"]) == len(gr)
                and int(original["working_W"]) == sum(g["played_result"] == "W" for g in gr)
                and int(original["working_L"]) == sum(g["played_result"] == "L" for g in gr)
                and original["blocked_groups"] == "0" and not original["blocked_ids"],
                "ORDINARY_SEASON_CENSUS_OR_PENDING_DEFECT:" + season)
        if original != proposal:
            require(season == "1965-66"
                    and {k for k in original if original[k] != proposal[k]} == {"final_status"}
                    and proposal["final_status"] == CANDIDATE_STATUS,
                    "UNAPPROVED_CENSUS_CANDIDATE_CHANGE")
            diffs.append(season)
        if season not in {"1965-66", "1926-27", "1935-36", "1953-54"}:
            require(original["final_status"] == "BULK_WORKING_GAMES_ACCEPTED_NOT_STAGE1_COMPLETE",
                    "EXTRA_UNRESOLVED_STAGE1_SEASON:" + season)
    require(diffs == ["1965-66"], "EXACT_ONE_TERMINAL_CANDIDATE_REQUIRED")
    require(census_map["1965-66"]["final_status"] == "ONE_AGGREGATE_LOSS_UNMAPPED"
            and census_map["1965-66"]["source_result_rows"] == "29"
            and census_map["1965-66"]["duplicate_representations"] == "1"
            and len(groups["1965-66"]) == 28,
            "NONMATCHING_1965_66_DISCREPANCY")
    require(census_map["1926-27"]["final_status"].startswith("OWNER_APPROVED_TWO_DAVIS_GAMES")
            and census_map["1926-27"]["working_accepted_games"] == "18"
            and census_map["1926-27"]["working_W"] == "10"
            and census_map["1926-27"]["working_L"] == "8",
            "UCD_ORDINARY_SEASON_COUNT_NOT_VALIDATED")
    for season in ("1935-36", "1953-54"):
        require(census_map[season]["final_status"]
                == "OWNER_EXHIBITION_EXCLUSION__LITERAL_PRINTED_AGGREGATE_CONTRADICTION",
                "CLOWNS_RELATED_SEASON_STATUS_CHANGED")
    require(Counter(g["played_result"] for g in groups["1965-66"])
            == Counter({"W": 21, "L": 7}), "1965_66_IDENTIFIED_WL_CHANGED")
    require(len([s for s in sources if s["season_label"] == "1965-66"]) == 29,
            "1965_66_SOURCE_LINES_CHANGED")
    a = src["FRESNO-EXP-CAND-1965-66-007"]
    b = src["FRESNO-EXP-CAND-1965-66-022"]
    require(a["literal_result"] == "W" and a["stage1_bulk_disposition"]
            == "ACCEPTED_NEW_COMPETITIVE_SOURCE_GAME"
            and b["stage1_bulk_disposition"] == "DUPLICATE_SOURCE_REPRESENTATION_NO_EXTRA_GAME",
            "UTEP_CORRECTION_OR_SDSU_DUPLICATE_REMOVED")
    owner = json.loads(raw[RULING])
    require(owner.get("owner_statement_verbatim") == case["owner_statement_verbatim"]
            and owner.get("research_parent_sha") == case["ruling_research_parent_sha"]
            and owner.get("immutable_research_base_sha") == case["research_base_sha"]
            and owner.get("owner_authority_scope") == "THIS_FRESNO_1965_66_SUMMARY_DISCREPANCY_ONLY"
            and owner.get("assume_no_missing_game_proven") is False
            and owner.get("game_creation_authorized") is False
            and owner.get("nonblocking_treatment_owner_requested") is True
            and owner.get("stage1_terminal_complete_authorized_automatically") is False
            and owner.get("preserve_official_printed_summary")
            == {"games": 29, "wins": 21, "losses": 8}
            and owner.get("accepted_identified_record") == {"wins": 21, "losses": 7}
            and owner.get("accepted_identified_game_total") == 28,
            "OWNER_AUTHORITY_PROVENANCE_OR_UNCERTAINTY_CHANGED")
    return {"school_key": "fresno-state", "season": "1965-66",
            "source_entries": len(sources), "accepted_games": len(games),
            "accepted_wins": 532, "accepted_losses": 479,
            "season_rows": len(seasons), "ucd_representation_checked": True}


def audit_checkpoint(checkpoint: Path, case: dict | None = None) -> dict:
    try:
        case = case if case is not None else load_authority()
        require(case["school_key"] == "fresno-state"
                and case["season"] == "1965-66"
                and case["research_base_sha"] == "087ac5dedc65780b65b7ae8d61e239d2033e2eea",
                "WRONG_SCHOOL_SEASON_BASE_AUTHORITY")
        raw = authenticated_parent(checkpoint, case)
        findings = verify_semantics(raw, case)
        return {"status": "ELIGIBLE_OWNER_SOURCE_ACCOUNTING_UNCERTAINTY",
                "stage1_complete": False,
                "checkpoint_commit_sha": case["checkpoint_commit_sha"],
                "checkpoint_manifest_blob_sha": case["checkpoint_manifest_blob_sha"],
                "source_member_git_blobs": case["member_git_blobs"],
                "findings": findings,
                "terminal_class": TERMINAL,
                "ordinary_other_seasons_checked": True,
                "ucd_representation_checked": True}
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return {"status": "BLOCKED", "stage1_complete": False,
                "defects": [str(exc)]}


def terminal_record() -> dict:
    return {
        "schema_version": 1, "school_key": "fresno-state", "season": "1965-66",
        "terminal_class": TERMINAL,
        "owner_disposition": "https://github.com/pollackelliott/college-basketball-history/issues/732",
        "reported_institutional": {"games": 29, "wins": 21, "losses": 8},
        "identified_competitive": {"games": 28, "wins": 21, "losses": 7},
        "working_interpretation": "RESEARCH_EXHAUSTED_POSSIBLE_SOURCE_ACCOUNTING_TYPO",
        "independent_additional_loss_possible": True,
        "unidentified_game_count_asserted": False,
        "reported_games_are_game_derived": False,
        "original_editorial_cause_proven": False,
        "anonymous_games_created": 0,
        "reopen_for_new_concrete_game_evidence": True,
        "source_literal_preservation_required": True,
        "publication_caveat": (
            "Fresno's printed 1965-66 record is 21-8 (29 games); "
            "28 individually documented games total 21-7. "
            "The difference may be a source-accounting error, but a separate "
            "unidentified loss remains possible. No unknown game is inferred."
        ),
    }


def successor_members(checkpoint: Path, case: dict, audit: dict) -> dict[str, bytes]:
    raw = authenticated_parent(checkpoint, case)
    require(audit.get("status") == "ELIGIBLE_OWNER_SOURCE_ACCOUNTING_UNCERTAINTY"
            and audit == audit_checkpoint(checkpoint, case), "STALE_OR_INVALID_AUDIT")
    record = terminal_record()
    members = {
        LEDGER: raw[LEDGER], SOURCE: raw[SOURCE], CENSUS: raw[CENSUS],
        PENDING: raw[PENDING], RULING: raw[RULING],
        "49-season-stage1-terminal-census.csv": raw[CANDIDATE],
        "stage1-predecessor-manifest-0035.json": raw[MANIFEST],
        "stage1-terminal-source-accounting.json": canonical(record),
        "stage4-authoring/season-coverage.json": canonical({
            "schema_version": 1, "school_key": "fresno-state",
            "terminal_source_accounting_uncertainties": [record],
            "identified_games_only": True,
            "carry_through_research_freeze_implementation_and_publication": True,
        }),
        "stage1-closeout-status.json": canonical({
            "schema_version": 1, "school_key": "fresno-state",
            "stage": "STAGE_1", "status": "AWAITING_INDEPENDENT_VERIFICATION",
            "stage1_complete": False, "stage2_authorized": False,
            "source_checkpoint_commit_sha": case["checkpoint_commit_sha"],
            "terminal_class": TERMINAL,
        }),
    }
    manifest = {
        "schema_version": 1, "kind": "OWNER_SOURCE_ACCOUNTING_CLOSEOUT_SUCCESSOR_V1",
        "school_key": "fresno-state", "stage": "STAGE_1",
        "parent_checkpoint_commit_sha": case["checkpoint_commit_sha"],
        "parent_manifest_git_blob_sha": case["checkpoint_manifest_blob_sha"],
        "member_sha256": {name: sha256(raw) for name, raw in sorted(members.items())},
        "member_bytes": {name: len(raw) for name, raw in sorted(members.items())},
    }
    members["manifest.json"] = canonical(manifest)
    return members


def zip_bytes(members: dict[str, bytes]) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_STORED) as z:
        for name, raw in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o600 << 16
            z.writestr(info, raw)
    return out.getvalue()


def validate_pinned_audit(checkpoint: Path, case: dict, path: Path, pin: str) -> dict:
    data = path.read_bytes()
    require(sha256(data) == pin, "AUDIT_SHA256_MISMATCH")
    report = json.loads(data)
    require(report == audit_checkpoint(checkpoint, case)
            and report.get("status") == "ELIGIBLE_OWNER_SOURCE_ACCOUNTING_UNCERTAINTY",
            "AUDIT_NOT_FRESH_ELIGIBLE")
    return report


def closeout(checkpoint: Path, audit_path: Path, output: Path,
             *, audit_sha: str, case: dict | None = None) -> dict:
    case = case if case is not None else load_authority()
    audit = validate_pinned_audit(checkpoint, case, audit_path, audit_sha)
    raw = zip_bytes(successor_members(checkpoint, case, audit))
    output.write_bytes(raw)
    return {"status": "AWAITING_INDEPENDENT_VERIFICATION", "stage1_complete": False,
            "successor_sha256": sha256(raw), "source_checkpoint_commit_sha":
            case["checkpoint_commit_sha"]}


def verify_closeout(checkpoint: Path, closeout_path: Path, audit_path: Path,
                    *, closeout_sha: str, audit_sha: str,
                    case: dict | None = None) -> dict:
    try:
        case = case if case is not None else load_authority()
        audit = validate_pinned_audit(checkpoint, case, audit_path, audit_sha)
        actual = closeout_path.read_bytes()
        require(sha256(actual) == closeout_sha, "SUCCESSOR_SHA256_MISMATCH")
        expected = zip_bytes(successor_members(checkpoint, case, audit))
        require(actual == expected, "INDEPENDENT_SUCCESSOR_REPLAY_MISMATCH")
        with zipfile.ZipFile(io.BytesIO(actual)) as z:
            require(z.testzip() is None and len(z.namelist()) == len(set(z.namelist())),
                    "SUCCESSOR_CRC_OR_DUPLICATE_MEMBER")
            members = {name: z.read(name) for name in z.namelist()}
        manifest = json.loads(members.pop("manifest.json"))
        require(set(members) == set(manifest["member_sha256"])
                and all(sha256(raw) == manifest["member_sha256"][name]
                        and len(raw) == manifest["member_bytes"][name]
                        for name, raw in members.items()), "SUCCESSOR_MANIFEST_INVALID")
        coverage = json.loads(members["stage4-authoring/season-coverage.json"])
        terminal = json.loads(members["stage1-terminal-source-accounting.json"])
        require(coverage["terminal_source_accounting_uncertainties"] == [terminal]
                and terminal["independent_additional_loss_possible"] is True
                and terminal["unidentified_game_count_asserted"] is False
                and terminal["anonymous_games_created"] == 0,
                "DOWNSTREAM_COVERAGE_OR_POSSIBLE_LOSS_MISSING")
        require(json.loads(members["stage1-closeout-status.json"])["stage1_complete"]
                is False, "PRE_VERIFICATION_COMPLETION_FABRICATED")
        return {"status": "VERIFIED_STAGE1_OWNER_SOURCE_ACCOUNTING_CLOSEOUT",
                "stage1_complete": True,
                "verified_successor_sha256": closeout_sha,
                "checkpoint_commit_sha": case["checkpoint_commit_sha"],
                "stage2_authorized": False,
                "historical_uncertainty_retained": True}
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile,
            json.JSONDecodeError) as exc:
        return {"status": "FAIL", "stage1_complete": False, "defects": [str(exc)]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    a = commands.add_parser("audit")
    a.add_argument("checkpoint", type=Path)
    a.add_argument("--expected-parent-sha", required=True)
    a.add_argument("--output", type=Path, required=True)
    c = commands.add_parser("closeout")
    c.add_argument("checkpoint", type=Path)
    c.add_argument("audit", type=Path)
    c.add_argument("--expected-parent-sha", required=True)
    c.add_argument("--expected-audit-sha256", required=True)
    c.add_argument("--output", type=Path, required=True)
    v = commands.add_parser("verify-closeout")
    v.add_argument("checkpoint", type=Path)
    v.add_argument("closeout", type=Path)
    v.add_argument("audit", type=Path)
    v.add_argument("--expected-parent-sha", required=True)
    v.add_argument("--expected-audit-sha256", required=True)
    v.add_argument("--expected-closeout-sha256", required=True)
    v.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    case = load_authority()
    if args.expected_parent_sha != case["checkpoint_commit_sha"]:
        report = {"status": "BLOCKED", "stage1_complete": False,
                  "defects": ["OWNER_CHECKPOINT_COMMIT_MISMATCH"]}
    elif args.command == "audit":
        report = audit_checkpoint(args.checkpoint, case)
    elif args.command == "closeout":
        try:
            report = closeout(args.checkpoint, args.audit, args.output,
                              audit_sha=args.expected_audit_sha256, case=case)
        except (ValueError, OSError, KeyError, TypeError) as exc:
            report = {"status": "BLOCKED", "stage1_complete": False,
                      "defects": [str(exc)]}
    else:
        report = verify_closeout(args.checkpoint, args.closeout, args.audit,
                                 closeout_sha=args.expected_closeout_sha256,
                                 audit_sha=args.expected_audit_sha256, case=case)
    args.output.write_bytes(canonical(report))
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] in {
        "ELIGIBLE_OWNER_SOURCE_ACCOUNTING_UNCERTAINTY",
        "AWAITING_INDEPENDENT_VERIFICATION",
        "VERIFIED_STAGE1_OWNER_SOURCE_ACCOUNTING_CLOSEOUT",
    } else 1


if __name__ == "__main__":
    sys.exit(main())
