#!/usr/bin/env python3
"""Audit and close out owner-authorized multi-season early-history accounting debt.

This path is for an exact owner-authorized checkpoint containing both:
- source-explicit aggregate-only seasons whose individual games remain unidentified; and
- detailed seasons whose source-internal season/cumulative accounting cannot be safely
  reconciled to the preserved row-level ledger.

The tool never invents games, removes identified games, or allocates aggregate results.

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
from pathlib import Path
from typing import Any

REGISTRY = Path(__file__).resolve().parents[1] / "data/reference/early-history-accounting-authorities.json"
ELIGIBLE = "ELIGIBLE_FOR_EARLY_HISTORY_ACCOUNTING_CLOSEOUT"
VERIFIED = "VERIFIED_EARLY_HISTORY_ACCOUNTING_CLOSEOUT"
AGGREGATE_TERMINAL = "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP"
ACCOUNTING_TERMINAL = "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION"
CLOSEOUT_MEMBER = "early-history-accounting-closeout.json"
AUTHORING_MEMBER = "stage4-authoring/season-coverage.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def csv_rows(data: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline="")))


def read_zip(path: Path, expected: str) -> tuple[dict[str, bytes], str]:
    raw = path.read_bytes()
    actual = digest(raw)
    if not expected or actual != expected:
        raise ValueError("CHECKPOINT_HASH_MISMATCH_OR_UNPINNED")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if archive.testzip():
            raise ValueError("INVALID_ARCHIVE_CRC")
        names = archive.namelist()
        if not names or len(names) != len(set(names)):
            raise ValueError("INVALID_ARCHIVE_NAMES")
        files = [name for name in names if not name.endswith("/")]
        if "manifest.json" in files:
            prefix = ""
        else:
            prefixes = {name.split("/", 1)[0] for name in files if "/" in name}
            if len(prefixes) != 1:
                raise ValueError("INVALID_ARCHIVE_LAYOUT")
            candidate = next(iter(prefixes)) + "/"
            if candidate + "manifest.json" not in files or not all(name.startswith(candidate) for name in files):
                raise ValueError("INVALID_ARCHIVE_LAYOUT")
            prefix = candidate
        members: dict[str, bytes] = {}
        for name in files:
            inner = name[len(prefix):]
            if not inner or inner.startswith("/") or ".." in Path(inner).parts:
                raise ValueError("UNSAFE_ARCHIVE_PATH")
            members[inner] = archive.read(name)
    return members, actual


def manifest_defects(members: dict[str, bytes]) -> list[str]:
    try:
        manifest = json.loads(members["manifest.json"])
        listed = manifest["files"]
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return ["INVALID_MANIFEST"]
    if not isinstance(listed, list):
        return ["INVALID_MANIFEST_FILES"]
    expected: dict[str, dict[str, Any]] = {}
    defects: list[str] = []
    for item in listed:
        if not isinstance(item, dict) or not item.get("path") or item["path"] in expected:
            defects.append("INVALID_OR_DUPLICATE_MANIFEST_ENTRY")
            continue
        expected[item["path"]] = item
    if set(expected) != set(members) - {"manifest.json"}:
        defects.append("MANIFEST_MEMBER_SET_MISMATCH")
    for name, meta in expected.items():
        data = members.get(name)
        if data is None:
            continue
        if meta.get("sha256") != digest(data) or meta.get("size") != len(data):
            defects.append("MANIFEST_HASH_OR_SIZE_MISMATCH:" + name)
    return defects


def lookup_authority(school: str, registry: Path) -> dict[str, Any] | None:
    data = json.loads(registry.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("authority_type") != "OWNER_APPROVED_EARLY_HISTORY_ACCOUNTING_CLOSEOUT":
        raise ValueError("INVALID_OWNER_AUTHORITY_REGISTRY")
    cases = [case for case in data.get("cases", []) if case.get("school_key") == school]
    if len(cases) > 1:
        raise ValueError("DUPLICATE_OWNER_AUTHORITY")
    return cases[0] if cases else None


def record(row: dict[str, str], *, official: bool) -> dict[str, int]:
    prefix = "official_" if official else "identified_"
    return {
        "wins": int(row[prefix + "w"]),
        "losses": int(row[prefix + "l"]),
        "games": int(row["official_games"] if official else row["identified_rows"]),
    }


def authority_records(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for item in items:
        season = str(item.get("season", ""))
        if not season or season in out:
            raise ValueError("DUPLICATE_OR_BLANK_AUTHORITY_SEASON")
        out[season] = item
    return out


def audit_checkpoint(parent: Path, *, expected_parent_sha256: str,
                     registry: Path = REGISTRY) -> dict[str, Any]:
    members, parent_sha = read_zip(parent, expected_parent_sha256)
    defects = manifest_defects(members)
    required = [
        "stage1-status.json", "stage1-residuals.csv", "stage1-identified-game-ledger.csv",
        "stage1-season-census.csv", "source-explicit-aggregate-only-seasons.csv",
        "early-period-season-accounting.csv", "early-reconciliation-summary.json",
        "manifest.json",
    ]
    missing = [name for name in required if name not in members]
    if missing:
        return {"status": "FAIL", "defects": ["MISSING_REQUIRED_MEMBER:" + x for x in missing], "stage1_complete": False}
    try:
        status = json.loads(members["stage1-status.json"])
        manifest = json.loads(members["manifest.json"])
        residuals = csv_rows(members["stage1-residuals.csv"])
        ledger = csv_rows(members["stage1-identified-game-ledger.csv"])
        census = csv_rows(members["stage1-season-census.csv"])
        aggregate_rows = csv_rows(members["source-explicit-aggregate-only-seasons.csv"])
        accounting_rows = csv_rows(members["early-period-season-accounting.csv"])
        summary = json.loads(members["early-reconciliation-summary.json"])
    except (KeyError, TypeError, ValueError, UnicodeError, csv.Error, json.JSONDecodeError):
        return {"status": "FAIL", "defects": ["INVALID_SOURCE_CHECKPOINT"], "stage1_complete": False}

    school = str(status.get("school_key") or status.get("school") or "").strip()
    research_base = str(status.get("research_base_sha") or "").strip()
    authority = lookup_authority(school, registry)
    if authority is None:
        defects.append("NO_EXACT_OWNER_AUTHORITY")
        authority = {}
    elif (
        authority.get("parent_checkpoint_sha256") != parent_sha
        or authority.get("research_base_sha") != research_base
        or not str(authority.get("owner_disposition", "")).startswith("https://github.com/")
    ):
        defects.append("OWNER_AUTHORITY_BINDING_MISMATCH")

    if status.get("stage1_complete") is True or status.get("stage") != "STAGE_1":
        defects.append("PARENT_NOT_BLOCKED_STAGE1")
    if manifest.get("research_base_sha") != research_base or manifest.get("school_key") != school:
        defects.append("MANIFEST_AUTHORITY_MISMATCH")
    if authority.get("identified_ledger_sha256") != digest(members["stage1-identified-game-ledger.csv"]):
        defects.append("IDENTIFIED_LEDGER_AUTHORITY_MISMATCH")
    if authority.get("identified_rows") != len(ledger):
        defects.append("IDENTIFIED_LEDGER_COUNT_MISMATCH")

    ids = [str(row.get("research_game_id", "")).strip() for row in ledger]
    if any(not gid for gid in ids) or len(ids) != len(set(ids)):
        defects.append("MISSING_OR_DUPLICATE_GAME_IDS")
    for row in ledger:
        text = " ".join(str(row.get(key, "")) for key in ("research_game_id", "source_opponent_label", "source_opponent_raw", "notes")).upper()
        if "PLACEHOLDER" in text or "ANONYMOUS GAME" in text:
            defects.append("FABRICATED_GAME_ROW")
            break

    blocking = [row for row in residuals if str(row.get("blocking", "")).strip().upper() in {"YES", "Y", "TRUE", "1"}]
    blocking_classes = {row.get("residual_class", "") for row in blocking}
    expected_classes = {
        "EARLY_SOURCE_EXPLICIT_AGGREGATE_ONLY_GAME_IDENTITIES_UNKNOWN",
        "EARLY_DETAILED_VS_OVERALL_CLUB_ACCOUNTING_CONTRADICTION",
    }
    if len(blocking) != 2 or blocking_classes != expected_classes:
        defects.append("UNRELATED_OR_MISSING_STAGE1_BLOCKER")

    aggregate_authority = authority_records(authority.get("aggregate_only_seasons", [])) if authority else {}
    aggregate_by_season = {row.get("season", ""): row for row in aggregate_rows}
    if set(aggregate_by_season) != set(aggregate_authority):
        defects.append("AGGREGATE_SEASON_POPULATION_MISMATCH")
    coverage: list[dict[str, Any]] = []
    for season in sorted(aggregate_authority):
        row = aggregate_by_season.get(season, {})
        auth = aggregate_authority[season]
        try:
            official = {"wins": int(row.get("official_w", "")), "losses": int(row.get("official_l", "")), "games": int(row.get("official_games", ""))}
            identified = {"wins": 0, "losses": 0, "games": int(row.get("individual_game_rows_in_guide", ""))}
        except ValueError:
            defects.append("AGGREGATE_RECORD_INVALID:" + season)
            continue
        if official != auth.get("institutional_record") or identified != auth.get("identified_record"):
            defects.append("AGGREGATE_RECORD_AUTHORITY_MISMATCH:" + season)
        if official["wins"] + official["losses"] != official["games"] or identified != {"wins": 0, "losses": 0, "games": 0}:
            defects.append("AGGREGATE_ARITHMETIC_OR_ROW_IDENTITY_INVALID:" + season)
        source_note = str(row.get("source_note", "")).strip()
        if source_note != auth.get("source_note"):
            defects.append("AGGREGATE_SOURCE_NOTE_MISMATCH:" + season)
        coverage.append({
            "school_key": school,
            "season": season,
            "institutional_record": official,
            "identified_record": identified,
            "unidentified_record": official,
            "source_description": source_note,
            "owner_disposition": authority.get("owner_disposition"),
            "parent_checkpoint_sha256": parent_sha,
            "research_base_sha": research_base,
            "terminal_classification": AGGREGATE_TERMINAL,
            "warning": "Season-level institutional record only. No unidentified game rows, opponents, dates, sites, scores, or result allocations are represented.",
        })

    accounting_authority = authority_records(authority.get("accounting_contradiction_seasons", [])) if authority else {}
    accounting_by_season = {
        row.get("season", ""): row for row in accounting_rows
        if row.get("source_status") == "DETAILED"
    }
    if set(accounting_by_season) != set(accounting_authority):
        defects.append("ACCOUNTING_SEASON_POPULATION_MISMATCH")
    contradictions: list[dict[str, Any]] = []
    for season in sorted(accounting_authority):
        row = accounting_by_season.get(season, {})
        auth = accounting_authority[season]
        try:
            official = record(row, official=True)
            identified = record(row, official=False)
        except (KeyError, ValueError):
            defects.append("ACCOUNTING_RECORD_INVALID:" + season)
            continue
        if official != auth.get("institutional_record") or identified != auth.get("identified_record"):
            defects.append("ACCOUNTING_RECORD_AUTHORITY_MISMATCH:" + season)
        delta = {key: official[key] - identified[key] for key in ("wins", "losses", "games")}
        if delta != auth.get("mechanical_delta"):
            defects.append("ACCOUNTING_DELTA_AUTHORITY_MISMATCH:" + season)
        contradictions.append({
            "school_key": school,
            "season": season,
            "institutional_record": official,
            "identified_record": identified,
            "mechanical_delta": delta,
            "source_description": "Institutional detailed rows and season/cumulative accounting conflict; arithmetic fitting is prohibited.",
            "owner_disposition": authority.get("owner_disposition"),
            "parent_checkpoint_sha256": parent_sha,
            "research_base_sha": research_base,
            "terminal_classification": ACCOUNTING_TERMINAL,
            "warning": "Preserve identified game rows unchanged. This delta is diagnostic only and is never an unidentified-game count or result allocation.",
        })

    expected_summary = authority.get("accounting_summary", {}) if authority else {}
    actual_summary = {
        "official_season_aggregate": summary.get("official_season_aggregate"),
        "chronological_detail": summary.get("chronological_detail"),
        "club_high_school_aggregate": summary.get("club_high_school_aggregate"),
        "simple_union_implied_overlap_games": summary.get("simple_union_implied_overlap_games"),
    }
    if actual_summary != expected_summary:
        defects.append("ACCOUNTING_SUMMARY_AUTHORITY_MISMATCH")
    if summary.get("conclusion") != "SIMPLE_UNION_RECONCILIATION_REJECTED. Aggregate structures cannot be converted into anonymous or inferred game rows. String-similar opponent labels are review triggers only, not same-game authority.":
        defects.append("ACCOUNTING_RECONCILIATION_GUARD_MISSING")
    conflicts = summary.get("direct_candidate_result_conflicts")
    if not isinstance(conflicts, list) or len(conflicts) < int(authority.get("minimum_direct_result_conflicts", 1) or 1):
        defects.append("ACCOUNTING_CONFLICT_EVIDENCE_INSUFFICIENT")

    census_seasons = [row.get("season", row.get("season_label", "")) for row in census]
    for season in set(aggregate_authority) | set(accounting_authority):
        if census_seasons.count(season) != 1:
            defects.append("MISSING_OR_DUPLICATE_SEASON_CENSUS:" + season)

    if status.get("anonymous_games_manufactured", status.get("early_period", {}).get("anonymous_games_manufactured", 0)) not in (0, None):
        defects.append("ANONYMOUS_GAMES_PRESENT")
    early = status.get("early_archive_pass", {})
    spalding = status.get("early_spalding_pass", {})
    if early.get("new_game_identities_recovered") != 0 or spalding.get("new_game_identities_recovered") != 0:
        defects.append("RESEARCH_EXHAUSTION_STATUS_CONFLICT")
    if early.get("source_explicit_aggregate_only_games") != sum(x["unidentified_record"]["games"] for x in coverage):
        defects.append("AGGREGATE_TOTAL_CONFLICT")

    payload = {
        "schema_version": 1,
        "school_key": school,
        "parent_checkpoint_sha256": parent_sha,
        "research_base_sha": research_base,
        "owner_disposition": authority.get("owner_disposition"),
        "identified_game_rows": len(ledger),
        "aggregate_coverage": coverage,
        "accounting_contradictions": contradictions,
        "aggregate_unidentified_games": sum(x["unidentified_record"]["games"] for x in coverage),
        "accounting_contradiction_seasons": len(contradictions),
        "historical_ledger_mutation": "NONE",
    }
    return {
        **payload,
        "status": ELIGIBLE if not defects else "FAIL",
        "payload_sha256": digest(json_bytes(payload)),
        "defects": sorted(set(defects)),
        "stage1_complete": False,
    }


def render_residuals(data: bytes) -> bytes:
    text = data.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    rows = list(reader)
    fields = list(reader.fieldnames or [])
    mapping = {
        "EARLY_SOURCE_EXPLICIT_AGGREGATE_ONLY_GAME_IDENTITIES_UNKNOWN": AGGREGATE_TERMINAL,
        "EARLY_DETAILED_VS_OVERALL_CLUB_ACCOUNTING_CONTRADICTION": ACCOUNTING_TERMINAL,
    }
    seen: set[str] = set()
    for row in rows:
        cls = row.get("residual_class", "")
        if cls not in mapping:
            continue
        seen.add(cls)
        row["detail"] = f"Terminalized from {cls} under exact owner-authorized early-history accounting closeout. " + row.get("detail", "")
        row["residual_class"] = mapping[cls]
        row["blocking"] = "NO"
        row["next_evidence_family"] = "TERMINAL_RESEARCHED_HISTORICAL_DEBT; reopen only on concrete new game-level evidence"
    if seen != set(mapping):
        raise ValueError("CLOSEOUT_BLOCKER_POPULATION_MISMATCH")
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def expected_successor(parent_members: dict[str, bytes], report: dict[str, Any], audit_sha: str) -> dict[str, bytes]:
    result = dict(parent_members)
    status = json.loads(result["stage1-status.json"])
    manifest = json.loads(result["manifest.json"])
    aggregate = []
    for item in report["aggregate_coverage"]:
        value = dict(item)
        value["audit_sha256"] = audit_sha
        aggregate.append(value)
    contradictions = []
    for item in report["accounting_contradictions"]:
        value = dict(item)
        value["audit_sha256"] = audit_sha
        contradictions.append(value)
    capsule = {
        "schema_version": 1,
        "school_key": report["school_key"],
        "research_base_sha": report["research_base_sha"],
        "parent_checkpoint_sha256": report["parent_checkpoint_sha256"],
        "owner_disposition": report["owner_disposition"],
        "audit_sha256": audit_sha,
        "aggregate_coverage": aggregate,
        "accounting_contradictions": contradictions,
    }
    status.update({
        "state": "COMPLETE",
        "status": "COMPLETE",
        "stage1_complete": True,
        "blocking_residual_count": 0,
        "next_bounded_family": "STAGE_2_AFTER_OWNER_AUTHORIZATION",
        "next_bounded_unit": "STAGE_2_AFTER_OWNER_AUTHORIZATION",
        "next_owner_boundary": "Stage 1 early-history accounting closeout independently verified; stop for ordinary Stage 2 owner authorization.",
        "early_history_accounting_terminal": [AGGREGATE_TERMINAL, ACCOUNTING_TERMINAL],
        "early_history_accounting_audit_sha256": audit_sha,
        "early_history_accounting_parent_sha256": report["parent_checkpoint_sha256"],
    })
    result["stage1-status.json"] = json_bytes(status)
    result["stage1-residuals.csv"] = render_residuals(result["stage1-residuals.csv"])
    result[CLOSEOUT_MEMBER] = json_bytes(capsule)
    result[AUTHORING_MEMBER] = json_bytes({
        "schema_version": 1,
        "coverage": aggregate,
        "accounting_contradictions": contradictions,
    })
    manifest.update({
        "state": "COMPLETE",
        "status": "COMPLETE",
        "parent_checkpoint_sha256": report["parent_checkpoint_sha256"],
        "early_history_accounting_audit_sha256": audit_sha,
        "early_history_accounting_terminal": [AGGREGATE_TERMINAL, ACCOUNTING_TERMINAL],
    })
    manifest["files"] = [
        {"path": name, "size": len(data), "sha256": digest(data)}
        for name, data in sorted(result.items()) if name != "manifest.json"
    ]
    result["manifest.json"] = json_bytes(manifest)
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


def closeout(parent: Path, audit_path: Path, output: Path, *, parent_sha: str,
             audit_sha: str, registry: Path = REGISTRY) -> dict[str, Any]:
    report, members = verified_audit(parent, audit_path, parent_sha, audit_sha, registry)
    successor = expected_successor(members, report, audit_sha)
    sha = serialize_zip(successor, output)
    return {
        "status": "STAGE1_CLOSEOUT_CANDIDATE_CREATED",
        "closeout_sha256": sha,
        "parent_checkpoint_sha256": parent_sha,
        "stage1_complete": False,
        "next_action": "Independently verify-closeout before declaring Stage 1 COMPLETE.",
    }


def verify_closeout(parent: Path, successor: Path, audit_path: Path, *, parent_sha: str,
                    successor_sha: str, audit_sha: str, registry: Path = REGISTRY) -> dict[str, Any]:
    try:
        report, original = verified_audit(parent, audit_path, parent_sha, audit_sha, registry)
        actual, _ = read_zip(successor, successor_sha)
        expected = expected_successor(original, report, audit_sha)
        defects = manifest_defects(actual)
        if actual != expected:
            defects.append("CLOSEOUT_CONTENT_OR_HISTORICAL_LEDGER_DRIFT")
        if actual.get("stage1-identified-game-ledger.csv") != original.get("stage1-identified-game-ledger.csv"):
            defects.append("IDENTIFIED_GAME_LEDGER_DRIFT")
        if actual.get("stage1-season-census.csv") != original.get("stage1-season-census.csv"):
            defects.append("SEASON_CENSUS_DRIFT")
    except (OSError, ValueError, TypeError, KeyError, csv.Error, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        return {"status": "FAIL", "defects": [str(exc)], "stage1_complete": False}
    return {
        "schema_version": 1,
        "status": VERIFIED if not defects else "FAIL",
        "defects": defects,
        "stage1_complete": not defects,
        "parent_checkpoint_sha256": parent_sha,
        "closeout_checkpoint_sha256": successor_sha,
        "audit_sha256": audit_sha,
        "school_key": report["school_key"],
        "aggregate_coverage": report["aggregate_coverage"],
        "accounting_contradictions": report["accounting_contradictions"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    audit_p = sub.add_parser("audit")
    audit_p.add_argument("parent", type=Path)
    audit_p.add_argument("--expected-parent-sha256", required=True)
    audit_p.add_argument("--output", type=Path)
    close_p = sub.add_parser("closeout")
    close_p.add_argument("parent", type=Path)
    close_p.add_argument("audit", type=Path)
    close_p.add_argument("--expected-parent-sha256", required=True)
    close_p.add_argument("--expected-audit-sha256", required=True)
    close_p.add_argument("--output", type=Path, required=True)
    verify_p = sub.add_parser("verify-closeout")
    verify_p.add_argument("parent", type=Path)
    verify_p.add_argument("closeout", type=Path)
    verify_p.add_argument("audit", type=Path)
    verify_p.add_argument("--expected-parent-sha256", required=True)
    verify_p.add_argument("--expected-closeout-sha256", required=True)
    verify_p.add_argument("--expected-audit-sha256", required=True)
    verify_p.add_argument("--output", type=Path)
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
