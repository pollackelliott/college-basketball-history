#!/usr/bin/env python3
"""Audit and close out an owner-authorized, research-exhausted early season aggregate gap.

No unidentified game is ever inserted into the ledger or canonical game universe.
The registry is a protected-main, exact-parent owner authority; a raw aggregate
record alone cannot make an arbitrary school or season eligible.

Commands:
  audit PARENT --expected-parent-sha256 SHA [--output REPORT.json]
  closeout PARENT AUDIT.json --expected-parent-sha256 SHA --expected-audit-sha256 SHA --output SUCCESSOR.zip
  verify-closeout PARENT SUCCESSOR.zip AUDIT.json --expected-parent-sha256 SHA --expected-closeout-sha256 SHA --expected-audit-sha256 SHA
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
ELIGIBLE = "ELIGIBLE_FOR_EARLY_AGGREGATE_COVERAGE_CLOSEOUT"
VERIFIED = "VERIFIED_EARLY_AGGREGATE_COVERAGE_CLOSEOUT"
TERMINAL = "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP"
CLOSEOUT_MEMBER = "aggregate-coverage-closeout.json"
AUTHORING_MEMBER = "stage4-authoring/season-coverage.json"
SOURCE_MEMBER = "founding-season-evidence-exhaustion.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def read_zip(path: Path, expected: str) -> tuple[dict[str, bytes], str]:
    raw = path.read_bytes()
    actual = digest(raw)
    if not expected or actual != expected:
        raise ValueError("CHECKPOINT_HASH_MISMATCH_OR_UNPINNED")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if z.testzip():
            raise ValueError("INVALID_ARCHIVE_CRC")
        names = z.namelist()
        if not names or len(names) != len(set(names)):
            raise ValueError("INVALID_ARCHIVE_NAMES")
        prefixes = {name.split("/", 1)[0] for name in names if "/" in name}
        if all("/" not in name for name in names):
            prefix = ""
        elif len(prefixes) == 1 and all(name.startswith(next(iter(prefixes)) + "/") for name in names):
            prefix = next(iter(prefixes)) + "/"
        else:
            raise ValueError("INVALID_ARCHIVE_LAYOUT")
        members = {}
        for name in names:
            inner = name[len(prefix):]
            if not inner or inner.startswith("/") or ".." in Path(inner).parts:
                raise ValueError("UNSAFE_ARCHIVE_PATH")
            members[inner] = z.read(name)
    return members, actual


def manifest_defects(members: dict[str, bytes]) -> list[str]:
    try:
        manifest = json.loads(members["stage1-manifest.json"])
        expected = manifest["members"]
    except (KeyError, ValueError, TypeError):
        return ["INVALID_MANIFEST"]
    defects = []
    if set(expected) != set(members) - {"stage1-manifest.json"}:
        defects.append("MANIFEST_MEMBER_SET_MISMATCH")
    for name, meta in expected.items():
        raw = members.get(name)
        if raw is None or len(raw) != meta.get("size") or digest(raw) != meta.get("sha256"):
            defects.append("MANIFEST_MISMATCH:" + name)
    return defects


def as_csv(raw: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))


def lookup_authority(school: str, season: str, registry: Path) -> dict[str, Any] | None:
    data = json.loads(registry.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("authority_type") != "OWNER_APPROVED_EARLY_AGGREGATE_COVERAGE":
        raise ValueError("INVALID_OWNER_AUTHORITY_REGISTRY")
    cases = [case for case in data["cases"] if case.get("school_key") == school and case.get("season") == season]
    if len(cases) > 1:
        raise ValueError("DUPLICATE_OWNER_AUTHORITY")
    return cases[0] if cases else None


def audit_checkpoint(parent: Path, *, expected_parent_sha256: str,
                     registry: Path = REGISTRY) -> dict[str, Any]:
    members, parent_sha = read_zip(parent, expected_parent_sha256)
    defects = manifest_defects(members)
    try:
        status = json.loads(members["stage1-status.json"])
        manifest = json.loads(members["stage1-manifest.json"])
        residuals = json.loads(members["blocking-residuals.json"])
        ledger = as_csv(members["structured-stage1-ledger.csv"])
        census = as_csv(members["season-census.csv"])
        evidence = json.loads(members[SOURCE_MEMBER])
    except (KeyError, TypeError, ValueError, UnicodeError, csv.Error):
        return {"status": "FAIL", "defects": ["INVALID_SOURCE_CHECKPOINT"]}
    school = status.get("school_key") or status.get("school")
    if status.get("stage1_complete") or status.get("status") != "RESEARCH_BLOCKED_SOURCE_COVERAGE":
        defects.append("PARENT_NOT_RESEARCH_BLOCKED")
    if manifest.get("research_base_sha") != status.get("research_base_sha"):
        defects.append("RESEARCH_BASE_MISMATCH")
    if manifest.get("game_rows") != len(ledger) or status.get("total_candidate_game_rows") != len(ledger):
        defects.append("LEDGER_COUNT_MISMATCH")
    if not isinstance(residuals, list) or len(residuals) != 1:
        defects.append("OTHER_STAGE1_BLOCKERS")
        residual = {}
    else:
        residual = residuals[0]
        if residual.get("class") != "FOUNDING_SEASON_PARTIAL_ROW_IDENTIFICATION":
            defects.append("UNRELATED_STAGE1_BLOCKER")
        if residual.get("research_state") != "RESEARCH_EXHAUSTED_SOURCE_COVERAGE":
            defects.append("RESEARCH_NOT_EXHAUSTED")
        if not residual.get("research_evidence_summary"):
            defects.append("MISSING_RESEARCH_PROVENANCE")
    season = residual.get("season", "")
    authority = lookup_authority(school, season, registry)
    if authority is None:
        defects.append("NO_EXACT_OWNER_AUTHORITY")
        authority = {}
    elif (authority.get("parent_checkpoint_sha256") != parent_sha
          or authority.get("research_base_sha") != status.get("research_base_sha")
          or not str(authority.get("owner_disposition", "")).startswith("https://github.com/")):
        defects.append("OWNER_AUTHORITY_BINDING_MISMATCH")
    year = int(season[:4]) if len(season) >= 4 and season[:4].isdigit() else 9999
    if year > int(authority.get("maximum_eligible_season_start_year", 0)):
        defects.append("OUTSIDE_FOUNDING_ERA")
    ids = [row.get("research_game_id", "").strip() for row in ledger]
    if len(set(ids)) != len(ids) or not all(ids):
        defects.append("MISSING_OR_DUPLICATE_GAME_IDS")
    if any(not row.get("opponent_literal", "").strip() or not row.get("game_type", "").strip()
           or "PLACEHOLDER" in row.get("game_universe_state", "").upper()
           or "UNIDENTIFIED" in row.get("game_universe_state", "").upper()
           for row in ledger):
        defects.append("FABRICATED_OR_UNTYPED_GAME_ROW")
    rows = [row for row in ledger if row.get("season_label") == season]
    if any(row.get("game_inclusion") != "INCLUDED" for row in rows):
        defects.append("SEASON_INCLUDED_GAME_MISMATCH")
    tally = Counter(row.get("played_result", "") for row in rows)
    if tally.get("", 0) or any(result not in ("W", "L") for result in tally):
        defects.append("UNRESOLVED_KNOWN_GAME_OUTCOMES")
    identified = {"wins": tally["W"], "losses": tally["L"], "games": len(rows)}
    record = evidence.get("institutional_record", {})
    if record != authority.get("institutional_record"):
        defects.append("INSTITUTIONAL_RECORD_AUTHORITY_MISMATCH")
    if identified != authority.get("identified_record"):
        defects.append("IDENTIFIED_RECORD_AUTHORITY_MISMATCH")
    if record.get("wins", -1) + record.get("losses", -1) != record.get("games", -2):
        defects.append("INSTITUTIONAL_RECORD_ARITHMETIC")
    difference = {field: record.get(field, 0) - identified.get(field, 0)
                  for field in ("wins", "losses", "games")}
    if (difference != authority.get("unidentified_record") or
            difference.get("games", 0) <= 0 or
            difference["wins"] + difference["losses"] != difference["games"]):
        defects.append("AGGREGATE_RESIDUAL_ARITHMETIC_MISMATCH")
    season_census = [row for row in census if row.get("season_label", row.get("season")) == season]
    if len(season_census) != 1:
        defects.append("MISSING_OR_DUPLICATE_SEASON_CENSUS")
    else:
        c = season_census[0]
        for field, value in (("source_aggregate_wins", record.get("wins")),
                             ("source_aggregate_losses", record.get("losses")),
                             ("source_aggregate_games", record.get("games")),
                             ("accepted_or_identified_rows", len(rows)),
                             ("known_played_wins", tally["W"]),
                             ("known_played_losses", tally["L"])):
            if c.get(field) != str(value):
                defects.append("SEASON_CENSUS_CONFLICT:" + field)
    detail = residual.get("detail", {})
    if (detail.get("identified_game_rows") != len(rows)
        or detail.get("unidentified_game_rows") != difference.get("games")):
        defects.append("RESIDUAL_COUNT_MISMATCH")
    if (evidence.get("policy_result") != "RESEARCH_EXHAUSTED_IDENTITIES_UNRESOLVED"
        or evidence.get("identified_game_rows") != len(rows)
        or evidence.get("unidentified_game_rows") != difference.get("games")
        or evidence.get("rows_added") != 0
        or evidence.get("accepted_game_rows_before") != len(ledger)
        or evidence.get("accepted_game_rows_after") != len(ledger)
        or evidence.get("anonymous_placeholder_rows") != 0
        or evidence.get("rows_added_from_aggregate_inference") != 0):
        defects.append("EVIDENCE_EXHAUSTION_INCONSISTENT")
    sources = evidence.get("systematic_evidence_checked", [])
    if (len(sources) < 3
        or not any("target institutional" in s.get("authority", "") for s in sources)
        or not all(s.get("source") and s.get("finding") and s.get("authority") for s in sources)):
        defects.append("INADEQUATE_INSTITUTIONAL_EVIDENCE")
    if (not residual.get("blocker_id") or
            not authority.get("owner_disposition") or
            evidence.get("school_key") != school or evidence.get("season") != season):
        defects.append("SOURCE_PROVENANCE_OR_OWNER_AUTHORITY_MISSING")
    gap = {"school_key": school, "season": season,
           "institutional_record": record, "identified_record": identified,
           "unidentified_record": difference,
           "source_description": "Institutional year-by-year season aggregate; individual game details incomplete",
           "evidence_member": SOURCE_MEMBER,
           "owner_disposition": authority.get("owner_disposition"),
           "parent_checkpoint_sha256": parent_sha,
           "research_base_sha": status.get("research_base_sha"),
           "terminal_classification": TERMINAL,
           "warning": "Missing-game count is derived from a primary institutional aggregate, not directly stated by the institution. No unidentified game rows are represented."}
    return {"schema_version": 1, "status": ELIGIBLE if not defects else "FAIL",
            "school_key": school, "parent_checkpoint_sha256": parent_sha,
            "research_base_sha": status.get("research_base_sha"),
            "identified_game_rows": len(ledger), "season_coverage": gap,
            "season_coverage_sha256": digest(json_bytes(gap)),
            "defects": sorted(set(defects)), "stage1_complete": False}


def expected_successor(parent_members: dict[str, bytes],
                       report: dict[str, Any], audit_sha: str) -> dict[str, bytes]:
    result = dict(parent_members)
    status = json.loads(result["stage1-status.json"])
    manifest = json.loads(result["stage1-manifest.json"])
    coverage = dict(report["season_coverage"])
    coverage["audit_sha256"] = audit_sha
    status.update({"status": "COMPLETE", "stage1_complete": True,
                   "blocking_residual_count": 0, "next_bounded_unit": "STAGE_2_AFTER_OWNER_AUTHORIZATION",
                   "next_owner_boundary": "Stage 1 terminal aggregate coverage accepted; stop for ordinary Stage 2 owner authorization.",
                   "aggregate_coverage_terminal": TERMINAL,
                   "aggregate_coverage_audit_sha256": audit_sha,
                   "aggregate_coverage_parent_sha256": report["parent_checkpoint_sha256"]})
    result["stage1-status.json"] = json_bytes(status)
    result["blocking-residuals.json"] = json_bytes([])
    result[CLOSEOUT_MEMBER] = json_bytes(coverage)
    result[AUTHORING_MEMBER] = json_bytes({"schema_version": 1, "coverage": [coverage]})
    manifest.update({"status": "COMPLETE", "blocking_residuals": 0,
                     "parent_checkpoint_sha256": report["parent_checkpoint_sha256"],
                     "aggregate_coverage_audit_sha256": audit_sha,
                     "aggregate_coverage_terminal": TERMINAL})
    manifest["members"] = {name: {"size": len(data), "sha256": digest(data)}
                           for name, data in result.items() if name != "stage1-manifest.json"}
    result["stage1-manifest.json"] = json_bytes(manifest)
    return result


def serialize_zip(members: dict[str, bytes], path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(members):
            z.writestr(name, members[name])
    return digest(path.read_bytes())


def verified_audit(parent: Path, audit_path: Path, parent_sha: str, audit_sha: str,
                   registry: Path) -> tuple[dict[str, Any], dict[str, bytes]]:
    raw = audit_path.read_bytes()
    if not audit_sha or digest(raw) != audit_sha:
        raise ValueError("AUDIT_HASH_MISMATCH_OR_UNPINNED")
    provided = json.loads(raw)
    computed = audit_checkpoint(parent, expected_parent_sha256=parent_sha, registry=registry)
    if computed["status"] != ELIGIBLE or provided != computed:
        raise ValueError("AUDIT_NOT_ELIGIBLE_OR_CONTENT_MISMATCH")
    members, _ = read_zip(parent, parent_sha)
    return computed, members


def closeout(parent: Path, audit_path: Path, output: Path, *,
             parent_sha: str, audit_sha: str, registry: Path = REGISTRY) -> dict[str, Any]:
    report, members = verified_audit(parent, audit_path, parent_sha, audit_sha, registry)
    successor = expected_successor(members, report, audit_sha)
    sha = serialize_zip(successor, output)
    return {"status": "STAGE1_CLOSEOUT_CANDIDATE_CREATED",
            "closeout_sha256": sha, "parent_checkpoint_sha256": parent_sha,
            "stage1_complete": False, "next_action": "Independently verify-closeout before declaring Stage 1 COMPLETE."}


def verify_closeout(parent: Path, successor: Path, audit_path: Path, *,
                    parent_sha: str, successor_sha: str, audit_sha: str,
                    registry: Path = REGISTRY) -> dict[str, Any]:
    try:
        report, original = verified_audit(parent, audit_path, parent_sha, audit_sha, registry)
        actual, _ = read_zip(successor, successor_sha)
        expected = expected_successor(original, report, audit_sha)
        defects = manifest_defects(actual)
        if actual != expected:
            defects.append("CLOSEOUT_CONTENT_OR_HISTORICAL_LEDGER_DRIFT")
    except (OSError, ValueError, TypeError, KeyError, csv.Error, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        return {"status": "FAIL", "defects": [str(exc)], "stage1_complete": False}
    return {"schema_version": 1, "status": VERIFIED if not defects else "FAIL",
            "defects": defects, "stage1_complete": not defects,
            "parent_checkpoint_sha256": parent_sha,
            "closeout_checkpoint_sha256": successor_sha,
            "audit_sha256": audit_sha,
            "school_key": report["school_key"],
            "season_coverage": report["season_coverage"]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    p = parser.add_subparsers(dest="command", required=True)
    a = p.add_parser("audit")
    a.add_argument("parent", type=Path)
    a.add_argument("--expected-parent-sha256", required=True)
    a.add_argument("--output", type=Path)
    c = p.add_parser("closeout")
    c.add_argument("parent", type=Path)
    c.add_argument("audit", type=Path)
    c.add_argument("--expected-parent-sha256", required=True)
    c.add_argument("--expected-audit-sha256", required=True)
    c.add_argument("--output", type=Path, required=True)
    v = p.add_parser("verify-closeout")
    v.add_argument("parent", type=Path)
    v.add_argument("closeout", type=Path)
    v.add_argument("audit", type=Path)
    v.add_argument("--expected-parent-sha256", required=True)
    v.add_argument("--expected-closeout-sha256", required=True)
    v.add_argument("--expected-audit-sha256", required=True)
    v.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "audit":
            report = audit_checkpoint(args.parent, expected_parent_sha256=args.expected_parent_sha256)
            ok = report["status"] == ELIGIBLE
        elif args.command == "closeout":
            report = closeout(args.parent, args.audit, args.output,
                              parent_sha=args.expected_parent_sha256,
                              audit_sha=args.expected_audit_sha256)
            ok = True
        else:
            report = verify_closeout(args.parent, args.closeout, args.audit,
                                     parent_sha=args.expected_parent_sha256,
                                     successor_sha=args.expected_closeout_sha256,
                                     audit_sha=args.expected_audit_sha256)
            ok = report["status"] == VERIFIED
    except (OSError, ValueError, TypeError, KeyError, csv.Error, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        report = {"status": "FAIL", "defects": [str(exc)]}
        ok = False
    rendered = json_bytes(report)
    if getattr(args, "output", None) and args.command != "closeout":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(rendered)
    print(rendered.decode("utf-8"), end="")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
