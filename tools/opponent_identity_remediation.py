#!/usr/bin/env python3
"""Guarded, read-only opponent-identity review and remediation planning.

This tool deliberately does not mutate basketball data. It provides the durable
review layer that must precede any opponent-identity remediation:

* ``sanity`` emits the compact non-D1/non-current opponent scan used as an
  Implementation Gate 1 owner backstop.
* ``validate-aliases`` validates ``data/reference/program-names.csv``.
* ``plan`` converts evidence-backed identity decisions into a deterministic,
  fingerprinted plan and reports canonical collision candidates before any write.

A later transactional apply step may consume a sealed plan, but string similarity
alone is never authority to merge institutional identities.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import published_opponent_identity_census as census


ALIAS_TYPES = {
    "OFFICIAL_HISTORICAL_NAME",
    "ATHLETIC_BRAND",
    "SOURCE_ABBREVIATION",
    "PROJECT_DISPLAY_ALIAS",
}

DECISIONS = {
    "MERGE_TO_PROGRAM",
    "MARK_CURRENT_D1",
    "KEEP_DISTINCT",
    "HOLD",
}

REQUIRED_ALIAS_FIELDS = [
    "program_key",
    "alias_name",
    "alias_type",
    "effective_start_season",
    "effective_end_season",
    "verification_status",
    "evidence_basis",
    "evidence_url",
    "notes",
]

REQUIRED_DECISION_FIELDS = [
    "source_program_key",
    "source_opponent_label",
    "from_program_key",
    "to_program_key",
    "decision",
    "evidence_basis",
    "evidence_url",
]


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def headers(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            return next(reader)
        except StopIteration:
            return []


def yes(value: str) -> bool:
    return (value or "").strip().lower() == "yes"


def season_start(value: str) -> int | None:
    text = (value or "").strip()
    if len(text) >= 4 and text[:4].isdigit():
        return int(text[:4])
    return None


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def decision_id(row: dict[str, str]) -> str:
    payload = "|".join(
        [
            row.get("source_program_key", "").strip(),
            row.get("source_opponent_label", "").strip(),
            row.get("from_program_key", "").strip(),
            row.get("to_program_key", "").strip(),
            row.get("decision", "").strip().upper(),
        ]
    )
    return "OID-" + sha256_text(payload)[:16].upper()


def load_programs(repo: Path) -> tuple[dict[str, dict[str, str]], set[str], set[str]]:
    rows = read_csv(repo / "data/reference/programs.csv")
    programs: dict[str, dict[str, str]] = {}
    current_d1: set[str] = set()
    published: set[str] = set()
    for row in rows:
        key = row.get("program_key", "").strip()
        if not key:
            continue
        programs[key] = row
        if yes(row.get("current_d1", "")):
            current_d1.add(key)
        if yes(row.get("public_page_enabled", "")):
            published.add(key)
    return programs, current_d1, published


def validate_alias_registry(repo: Path) -> dict[str, Any]:
    path = repo / "data/reference/program-names.csv"
    actual_headers = headers(path)
    errors: list[str] = []
    warnings: list[str] = []

    if actual_headers != REQUIRED_ALIAS_FIELDS:
        errors.append(
            "program-names.csv header mismatch: expected "
            + ",".join(REQUIRED_ALIAS_FIELDS)
        )
        return {"errors": errors, "warnings": warnings, "row_count": 0}

    programs, _, _ = load_programs(repo)
    rows = read_csv(path)
    normalized_groups: dict[str, list[dict[str, str]]] = defaultdict(list)

    for number, row in enumerate(rows, start=2):
        key = row.get("program_key", "").strip()
        alias_name = row.get("alias_name", "").strip()
        alias_type = row.get("alias_type", "").strip()
        status = row.get("verification_status", "").strip()
        basis = row.get("evidence_basis", "").strip()
        start = season_start(row.get("effective_start_season", ""))
        end = season_start(row.get("effective_end_season", ""))

        if key not in programs:
            errors.append(f"row {number}: unknown program_key {key!r}")
        if not alias_name:
            errors.append(f"row {number}: alias_name is required")
        if alias_type not in ALIAS_TYPES:
            errors.append(f"row {number}: unsupported alias_type {alias_type!r}")
        if status != "VERIFIED":
            errors.append(f"row {number}: verification_status must be VERIFIED")
        if not basis:
            errors.append(f"row {number}: evidence_basis is required")
        if start is not None and end is not None and start > end:
            errors.append(f"row {number}: effective season range is reversed")

        normalized = census.normalize_name(alias_name)
        if normalized:
            enriched = dict(row)
            enriched["_line"] = str(number)
            enriched["_start"] = str(start or "")
            enriched["_end"] = str(end or "")
            normalized_groups[normalized].append(enriched)

    # The same spelling may legitimately identify different institutions in disjoint
    # eras, but overlapping or undated verified aliases for different program keys are
    # too ambiguous to become registry authority.
    for normalized, group in normalized_groups.items():
        keys = {row.get("program_key", "").strip() for row in group}
        if len(keys) <= 1:
            continue
        for i, left in enumerate(group):
            for right in group[i + 1 :]:
                if left.get("program_key") == right.get("program_key"):
                    continue
                l_start = season_start(left.get("effective_start_season", ""))
                l_end = season_start(left.get("effective_end_season", ""))
                r_start = season_start(right.get("effective_start_season", ""))
                r_end = season_start(right.get("effective_end_season", ""))
                if None in (l_start, l_end, r_start, r_end):
                    errors.append(
                        "ambiguous alias without disjoint complete era bounds: "
                        f"{normalized!r} -> {left.get('program_key')} / "
                        f"{right.get('program_key')}"
                    )
                    continue
                if max(l_start, r_start) <= min(l_end, r_end):
                    errors.append(
                        "overlapping ambiguous alias eras: "
                        f"{normalized!r} -> {left.get('program_key')} / "
                        f"{right.get('program_key')}"
                    )

    return {
        "schema_version": 1,
        "row_count": len(rows),
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }


def _census_findings_by_row(repo: Path) -> dict[tuple[str, str, str], list[dict[str, Any]]]:
    report = census.build_census(repo)
    by_row: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for finding in report["findings"]:
        signature = (
            finding["source_program_key"],
            finding["source_opponent_label"],
            finding["canonical_opponent_key"],
        )
        by_row[signature].append(finding)
    return by_row


def sanity_report(repo: Path, school_key: str) -> dict[str, Any]:
    programs, current_d1, _ = load_programs(repo)
    package = repo / "schools" / school_key / "opponents.csv"
    if not package.exists():
        raise FileNotFoundError(package)

    findings_by_row = _census_findings_by_row(repo)
    output: list[dict[str, Any]] = []
    for row in read_csv(package):
        canonical_key = row.get("canonical_opponent_key", "").strip()
        stored_current = yes(row.get("current_d1", ""))
        if canonical_key in current_d1 and stored_current:
            continue
        signature = (
            school_key,
            row.get("source_opponent_label", "").strip(),
            canonical_key,
        )
        flags = findings_by_row.get(signature, [])
        output.append(
            {
                "source_opponent_label": row.get("source_opponent_label", "").strip(),
                "canonical_opponent_key": canonical_key,
                "canonical_opponent_name": row.get("canonical_opponent_name", "").strip(),
                "stored_current_d1": row.get("current_d1", "").strip(),
                "registry_program_exists": canonical_key in programs,
                "registry_current_d1": canonical_key in current_d1,
                "games": census.parse_int(row.get("games_with_source_label", "")),
                "first_season": row.get("first_season", "").strip(),
                "last_season": row.get("last_season", "").strip(),
                "tool_flags": [
                    {
                        "priority": item["priority"],
                        "finding_type": item["finding_type"],
                        "suggested_program_key": item["suggested_program_key"],
                    }
                    for item in flags
                ],
            }
        )

    output.sort(
        key=lambda row: (
            min(
                [census.PRIORITY_ORDER[x["priority"]] for x in row["tool_flags"]]
                or [9]
            ),
            -row["games"],
            row["source_opponent_label"].lower(),
        )
    )
    flagged = sum(1 for row in output if row["tool_flags"])
    return {
        "schema_version": 1,
        "school_key": school_key,
        "non_current_or_non_d1_rows": len(output),
        "tool_flagged_rows": flagged,
        "rows": output,
    }


def load_decisions(path: Path) -> list[dict[str, str]]:
    actual = headers(path)
    missing = [field for field in REQUIRED_DECISION_FIELDS if field not in actual]
    if missing:
        raise ValueError("decision file missing fields: " + ", ".join(missing))
    rows = read_csv(path)
    for row in rows:
        row["decision"] = row.get("decision", "").strip().upper()
    return rows


def _canonical_score_orientation(row: dict[str, str], mapped_a: str, mapped_b: str) -> tuple[str, str, str, str]:
    original_a = row.get("team_a_key", "").strip()
    original_b = row.get("team_b_key", "").strip()
    score_a = row.get("team_a_score", "").strip()
    score_b = row.get("team_b_score", "").strip()
    if mapped_a <= mapped_b:
        return mapped_a, mapped_b, score_a, score_b
    return mapped_b, mapped_a, score_b, score_a


def _collision_signature(row: dict[str, str], key_map: dict[str, str]) -> tuple[str, ...]:
    mapped_a = key_map.get(row.get("team_a_key", "").strip(), row.get("team_a_key", "").strip())
    mapped_b = key_map.get(row.get("team_b_key", "").strip(), row.get("team_b_key", "").strip())
    team_a, team_b, score_a, score_b = _canonical_score_orientation(row, mapped_a, mapped_b)
    return (
        row.get("season_label", "").strip(),
        row.get("game_date", "").strip(),
        team_a,
        team_b,
        score_a,
        score_b,
        row.get("overtime_periods", "").strip(),
    )


def build_plan(repo: Path, decisions_path: Path) -> dict[str, Any]:
    programs, current_d1, _ = load_programs(repo)
    alias_validation = validate_alias_registry(repo)
    decisions = load_decisions(decisions_path)
    blockers: list[str] = list(alias_validation["errors"])
    warnings: list[str] = []
    decision_items: list[dict[str, Any]] = []
    key_map: dict[str, str] = {}

    for row in decisions:
        source_program_key = row.get("source_program_key", "").strip()
        source_label = row.get("source_opponent_label", "").strip()
        from_key = row.get("from_program_key", "").strip()
        to_key = row.get("to_program_key", "").strip()
        action = row.get("decision", "").strip().upper()
        basis = row.get("evidence_basis", "").strip()
        evidence_url = row.get("evidence_url", "").strip()
        did = decision_id(row)

        if action not in DECISIONS:
            blockers.append(f"{did}: unsupported decision {action!r}")
        if source_program_key not in programs:
            blockers.append(f"{did}: unknown source program {source_program_key!r}")
        if not source_label:
            blockers.append(f"{did}: source_opponent_label is required")
        if not from_key:
            blockers.append(f"{did}: from_program_key is required")
        if not basis:
            blockers.append(f"{did}: evidence_basis is required")

        if action in {"MERGE_TO_PROGRAM", "MARK_CURRENT_D1"}:
            if to_key not in programs:
                blockers.append(f"{did}: target program {to_key!r} is absent from registry")
            if to_key not in current_d1:
                blockers.append(f"{did}: target program {to_key!r} is not current D1")

        if action == "MERGE_TO_PROGRAM":
            if not to_key or to_key == from_key:
                blockers.append(f"{did}: MERGE_TO_PROGRAM requires a different target key")
            previous = key_map.get(from_key)
            if previous and previous != to_key:
                blockers.append(
                    f"{did}: global key {from_key!r} maps inconsistently to "
                    f"{previous!r} and {to_key!r}"
                )
            elif to_key:
                key_map[from_key] = to_key
        elif action == "MARK_CURRENT_D1":
            if to_key != from_key:
                blockers.append(f"{did}: MARK_CURRENT_D1 requires to_program_key == from_program_key")

        opponents_path = repo / "schools" / source_program_key / "opponents.csv"
        source_games_path = repo / "schools" / source_program_key / "source-games.csv"
        matching_opponents: list[dict[str, str]] = []
        matching_source_games: list[dict[str, str]] = []
        if opponents_path.exists():
            matching_opponents = [
                item
                for item in read_csv(opponents_path)
                if item.get("source_opponent_label", "").strip() == source_label
                and item.get("canonical_opponent_key", "").strip() == from_key
            ]
        else:
            blockers.append(f"{did}: missing {opponents_path}")
        if source_games_path.exists():
            matching_source_games = [
                item
                for item in read_csv(source_games_path)
                if item.get("source_opponent_label", "").strip() == source_label
                and item.get("normalized_opponent_key", "").strip() == from_key
            ]
        else:
            blockers.append(f"{did}: missing {source_games_path}")

        if not matching_opponents:
            blockers.append(
                f"{did}: no exact opponents.csv row for {source_program_key} / "
                f"{source_label!r} / {from_key!r}"
            )
        expected_games = sum(
            census.parse_int(item.get("games_with_source_label", ""))
            for item in matching_opponents
        )
        if expected_games != len(matching_source_games):
            blockers.append(
                f"{did}: opponents.csv reports {expected_games} game(s), but exact "
                f"source-games match count is {len(matching_source_games)}"
            )

        decision_items.append(
            {
                "decision_id": did,
                "source_program_key": source_program_key,
                "source_opponent_label": source_label,
                "from_program_key": from_key,
                "to_program_key": to_key,
                "decision": action,
                "evidence_basis": basis,
                "evidence_url": evidence_url,
                "package_opponent_rows": len(matching_opponents),
                "package_source_game_count": len(matching_source_games),
                "source_game_ids": sorted(
                    item.get("source_game_id", "").strip()
                    for item in matching_source_games
                    if item.get("source_game_id", "").strip()
                ),
            }
        )

    canonical_path = repo / "data/canonical/games.csv"
    assertions_path = repo / "data/evidence/game-assertions.csv"
    canonical_rows = read_csv(canonical_path)
    assertion_rows = read_csv(assertions_path)

    affected_canonical: dict[str, list[str]] = {}
    affected_assertions: dict[str, int] = {}
    for from_key, to_key in sorted(key_map.items()):
        cids = sorted(
            row.get("canonical_game_id", "").strip()
            for row in canonical_rows
            if from_key
            in {
                row.get("team_a_key", "").strip(),
                row.get("team_b_key", "").strip(),
            }
        )
        affected_canonical[f"{from_key}->{to_key}"] = cids
        affected_assertions[f"{from_key}->{to_key}"] = sum(
            1
            for row in assertion_rows
            if row.get("normalized_opponent_key", "").strip() == from_key
        )

    self_game_ids: list[str] = []
    signatures: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in canonical_rows:
        mapped_a = key_map.get(row.get("team_a_key", "").strip(), row.get("team_a_key", "").strip())
        mapped_b = key_map.get(row.get("team_b_key", "").strip(), row.get("team_b_key", "").strip())
        if mapped_a == mapped_b:
            self_game_ids.append(row.get("canonical_game_id", "").strip())
        signatures[_collision_signature(row, key_map)].append(row)

    exact_collisions: list[dict[str, Any]] = []
    imprecise_collisions: list[dict[str, Any]] = []
    for signature, group in signatures.items():
        if len(group) <= 1:
            continue
        # Only report collisions touched by the proposed key map.
        touched = any(
            row.get("team_a_key", "").strip() in key_map
            or row.get("team_b_key", "").strip() in key_map
            for row in group
        )
        if not touched:
            continue
        item = {
            "signature": list(signature),
            "canonical_game_ids": sorted(
                row.get("canonical_game_id", "").strip() for row in group
            ),
        }
        if signature[1]:
            exact_collisions.append(item)
        else:
            imprecise_collisions.append(item)

    if self_game_ids:
        blockers.append(
            "program-key replacement would create self-games: "
            + ", ".join(sorted(self_game_ids)[:25])
        )
    if exact_collisions:
        blockers.append(
            f"program-key replacement exposes {len(exact_collisions)} exact-date "
            "canonical collision candidate(s); these require one-real-game reconciliation"
        )
    if imprecise_collisions:
        warnings.append(
            f"program-key replacement exposes {len(imprecise_collisions)} unknown-date "
            "collision candidate(s) requiring review"
        )

    fingerprints = {
        "programs.csv": sha256_file(repo / "data/reference/programs.csv"),
        "program-names.csv": sha256_file(repo / "data/reference/program-names.csv"),
        "canonical-games.csv": sha256_file(canonical_path),
        "game-assertions.csv": sha256_file(assertions_path),
        "decisions.csv": sha256_file(decisions_path),
    }

    decision_items.sort(key=lambda item: item["decision_id"])
    core = {
        "schema_version": 1,
        "decision_count": len(decision_items),
        "decisions": decision_items,
        "global_key_map": key_map,
        "affected_canonical_game_ids": affected_canonical,
        "affected_assertion_counts": affected_assertions,
        "exact_collision_candidates": exact_collisions,
        "imprecise_collision_candidates": imprecise_collisions,
        "blockers": sorted(set(blockers)),
        "warnings": sorted(set(warnings)),
        "fingerprints": fingerprints,
    }
    core["plan_sha256"] = sha256_text(stable_json(core))
    return core


def print_sanity_text(report: dict[str, Any]) -> None:
    print(f"OPPONENT SANITY SCAN: {report['school_key']}")
    print(f"non-D1/non-current rows: {report['non_current_or_non_d1_rows']}")
    print(f"tool-flagged rows: {report['tool_flagged_rows']}")
    print()
    for row in report["rows"]:
        flags = ";".join(
            f"{flag['priority']}:{flag['finding_type']}"
            + (f"->{flag['suggested_program_key']}" if flag['suggested_program_key'] else "")
            for flag in row["tool_flags"]
        ) or "-"
        print(
            f"{row['source_opponent_label']} | {row['canonical_opponent_key']} | "
            f"games={row['games']} | {row['first_season']}..{row['last_season']} | {flags}"
        )


def print_plan_text(plan: dict[str, Any]) -> None:
    print("OPPONENT IDENTITY REMEDIATION PLAN")
    print(f"decisions: {plan['decision_count']}")
    print(f"global key merges: {len(plan['global_key_map'])}")
    print(f"exact collision candidates: {len(plan['exact_collision_candidates'])}")
    print(f"unknown-date collision candidates: {len(plan['imprecise_collision_candidates'])}")
    print(f"blockers: {len(plan['blockers'])}")
    print(f"warnings: {len(plan['warnings'])}")
    print(f"plan sha256: {plan['plan_sha256']}")
    if plan["blockers"]:
        print("\nBLOCKERS")
        for item in plan["blockers"]:
            print(f"- {item}")
    if plan["warnings"]:
        print("\nWARNINGS")
        for item in plan["warnings"]:
            print(f"- {item}")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=repo_root_from_script())
    sub = parser.add_subparsers(dest="command", required=True)

    alias_parser = sub.add_parser("validate-aliases")
    alias_parser.add_argument("--json", action="store_true")

    sanity_parser = sub.add_parser("sanity")
    sanity_parser.add_argument("school_key")
    sanity_parser.add_argument("--json", action="store_true")

    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("decisions_csv", type=Path)
    plan_parser.add_argument("--output", type=Path)
    plan_parser.add_argument("--json", action="store_true")

    args = parser.parse_args(list(argv) if argv is not None else None)
    repo = args.repo.resolve()

    if args.command == "validate-aliases":
        report = validate_alias_registry(repo)
        if args.json:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print(f"program-name aliases: {report['row_count']}")
            print(f"errors: {len(report['errors'])}")
            print(f"warnings: {len(report['warnings'])}")
            for item in report["errors"]:
                print(f"ERROR: {item}")
        return 1 if report["errors"] else 0

    if args.command == "sanity":
        report = sanity_report(repo, args.school_key)
        if args.json:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print_sanity_text(report)
        return 0

    if args.command == "plan":
        plan = build_plan(repo, args.decisions_csv.resolve())
        if args.output:
            args.output.write_text(
                json.dumps(plan, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        if args.json:
            print(json.dumps(plan, indent=2, sort_keys=True))
        else:
            print_plan_text(plan)
        return 2 if plan["blockers"] else 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
