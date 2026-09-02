#!/usr/bin/env python3
"""Read-only audit of canonical collisions exposed by opponent-key remediation.

The first remediation planner deliberately blocks exact canonical duplicates after a
program-key replacement. This companion audit widens that review boundary: games with
the same mapped program pair and exact date are grouped even when score, overtime,
site, or other canonical fields disagree. That prevents a real duplicate from escaping
review merely because two sources disagree about one historical detail.

Nothing in this tool mutates repository data or chooses a canonical survivor.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import opponent_identity_remediation as remediation


COMPARE_FIELDS = [
    "team_a_score",
    "team_b_score",
    "result_winner_team_key",
    "overtime_periods",
    "site_type",
    "designated_home_team_key",
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
    "game_type",
    "postseason_round",
    "administrative_status",
    "administrative_note",
]

CORE_FIELDS = ["team_a_score", "team_b_score", "overtime_periods"]


def canonical_id_sort_key(value: str) -> tuple[int, str]:
    match = re.fullmatch(r"CBBG-(\d+)", (value or "").strip())
    if match:
        return int(match.group(1)), value
    return 10**18, value


def _mapped_key(value: str, key_map: dict[str, str]) -> str:
    key = (value or "").strip()
    return key_map.get(key, key)


def mapped_view(row: dict[str, str], key_map: dict[str, str]) -> dict[str, str]:
    """Return a canonical row normalized after the proposed program-key map."""

    mapped_a = _mapped_key(row.get("team_a_key", ""), key_map)
    mapped_b = _mapped_key(row.get("team_b_key", ""), key_map)
    score_a = row.get("team_a_score", "").strip()
    score_b = row.get("team_b_score", "").strip()
    site_type = row.get("site_type", "").strip()

    if mapped_a <= mapped_b:
        team_a, team_b = mapped_a, mapped_b
    else:
        team_a, team_b = mapped_b, mapped_a
        score_a, score_b = score_b, score_a
        if site_type == "TEAM_A_HOME":
            site_type = "TEAM_B_HOME"
        elif site_type == "TEAM_B_HOME":
            site_type = "TEAM_A_HOME"

    return {
        "canonical_game_id": row.get("canonical_game_id", "").strip(),
        "season_label": row.get("season_label", "").strip(),
        "game_date": row.get("game_date", "").strip(),
        "team_a_key": team_a,
        "team_b_key": team_b,
        "team_a_score": score_a,
        "team_b_score": score_b,
        "result_winner_team_key": _mapped_key(
            row.get("result_winner_team_key", ""), key_map
        ),
        "overtime_periods": row.get("overtime_periods", "").strip(),
        "site_type": site_type,
        "designated_home_team_key": _mapped_key(
            row.get("designated_home_team_key", ""), key_map
        ),
        "venue_key": row.get("venue_key", "").strip(),
        "venue_id": row.get("venue_id", "").strip(),
        "site_city": row.get("site_city", "").strip(),
        "site_state": row.get("site_state", "").strip(),
        "game_type": row.get("game_type", "").strip(),
        "postseason_round": row.get("postseason_round", "").strip(),
        "administrative_status": row.get("administrative_status", "").strip(),
        "administrative_note": row.get("administrative_note", "").strip(),
    }


def _field_differences(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    differences: dict[str, dict[str, str]] = {}
    for field in COMPARE_FIELDS:
        values = {row.get(field, "") for row in rows}
        if len(values) <= 1:
            continue
        differences[field] = {
            row["canonical_game_id"]: row.get(field, "") for row in rows
        }
    return differences


def audit_rows(plan: dict[str, Any], games: list[dict[str, str]]) -> dict[str, Any]:
    key_map = dict(plan.get("global_key_map", {}))
    affected = {
        game_id
        for ids in plan.get("affected_canonical_game_ids", {}).values()
        for game_id in ids
    }

    mapped_rows = [mapped_view(row, key_map) for row in games]
    by_date_pair: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in mapped_rows:
        if not row["game_date"]:
            continue
        signature = (
            row["season_label"],
            row["game_date"],
            row["team_a_key"],
            row["team_b_key"],
        )
        by_date_pair[signature].append(row)

    groups: list[dict[str, Any]] = []
    covered_affected: set[str] = set()

    for signature, rows in by_date_pair.items():
        group_affected = sorted(
            {row["canonical_game_id"] for row in rows} & affected,
            key=canonical_id_sort_key,
        )
        if not group_affected or len(rows) < 2:
            continue

        ordered = sorted(rows, key=lambda row: canonical_id_sort_key(row["canonical_game_id"]))
        ids = [row["canonical_game_id"] for row in ordered]
        core_variants = {
            tuple(row.get(field, "") for field in CORE_FIELDS) for row in ordered
        }
        kind = "EXACT_CORE_MATCH" if len(core_variants) == 1 else "SAME_DATE_IDENTITY_CONFLICT"
        candidate = min(ids, key=canonical_id_sort_key)

        groups.append(
            {
                "kind": kind,
                "signature": list(signature),
                "canonical_game_ids": ids,
                "affected_canonical_game_ids": group_affected,
                "oldest_id_candidate": candidate,
                "survivor_status": "REVIEW_CANDIDATE_ONLY",
                "core_variants": [list(item) for item in sorted(core_variants)],
                "field_differences": _field_differences(ordered),
            }
        )
        covered_affected.update(group_affected)

    groups.sort(
        key=lambda item: (
            item["signature"],
            [canonical_id_sort_key(value) for value in item["canonical_game_ids"]],
        )
    )

    exact_groups = [item for item in groups if item["kind"] == "EXACT_CORE_MATCH"]
    conflict_groups = [
        item for item in groups if item["kind"] == "SAME_DATE_IDENTITY_CONFLICT"
    ]
    unpaired = sorted(affected - covered_affected, key=canonical_id_sort_key)

    core = {
        "schema_version": 1,
        "source_plan_sha256": plan.get("plan_sha256", ""),
        "global_key_map": key_map,
        "affected_canonical_game_count": len(affected),
        "same_date_collision_group_count": len(groups),
        "exact_core_match_group_count": len(exact_groups),
        "same_date_identity_conflict_group_count": len(conflict_groups),
        "covered_affected_game_count": len(covered_affected),
        "unpaired_affected_game_count": len(unpaired),
        "collision_groups": groups,
        "unpaired_affected_game_ids": unpaired,
    }
    core["audit_sha256"] = remediation.sha256_text(remediation.stable_json(core))
    return core


def build_audit(repo: Path, decisions_path: Path) -> dict[str, Any]:
    plan = remediation.build_plan(repo, decisions_path)
    games = remediation.read_csv(repo / "data/canonical/games.csv")
    return audit_rows(plan, games)


def print_text(report: dict[str, Any]) -> None:
    print("Opponent identity collision audit")
    print(f"Affected canonical games: {report['affected_canonical_game_count']}")
    print(f"Same-date collision groups: {report['same_date_collision_group_count']}")
    print(f"Exact core matches: {report['exact_core_match_group_count']}")
    print(
        "Same-date identity conflicts: "
        f"{report['same_date_identity_conflict_group_count']}"
    )
    print(f"Unpaired affected games: {report['unpaired_affected_game_count']}")
    print(f"Audit SHA-256: {report['audit_sha256']}")
    for item in report["collision_groups"]:
        fields = ",".join(sorted(item["field_differences"])) or "none"
        print(
            f"{item['kind']} | {','.join(item['canonical_game_ids'])} | "
            f"{' | '.join(item['signature'])} | differences={fields}"
        )
    if report["unpaired_affected_game_ids"]:
        print("UNPAIRED | " + ",".join(report["unpaired_affected_game_ids"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("decisions", type=Path)
    parser.add_argument("--repo", type=Path, default=remediation.repo_root_from_script())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_audit(args.repo.resolve(), args.decisions.resolve())
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    if args.json:
        print(payload, end="")
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
