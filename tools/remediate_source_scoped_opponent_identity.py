#!/usr/bin/env python3
"""Sealed source-scoped opponent-identity reconciliation.

This transaction is intentionally narrower than the global opponent-identity tools.
It corrects one literal source-label population whose normalized opponent key is
wrong, then absorbs the resulting duplicate canonical row into an explicitly named
counterpart. It never creates a global old-key -> new-key mapping.

Default mode is dry-run. ``--apply`` requires the exact SHA-256 printed by the
same plan against the same repository state.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class ScopedIdentityError(RuntimeError):
    pass


MERGE_FIELDS = [
    "season_label",
    "game_date",
    "date_precision",
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
    "canonical_status",
]


def clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


def stable(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    encoding = "utf-8-sig" if bom else "utf-8"
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator=newline)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
    temp.replace(path)


def git_head(repo: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True, capture_output=True
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def truthy(value: str) -> bool:
    return clean(value).lower() in {"yes", "true", "1", "y"}


def append_note(existing: str, marker: str) -> str:
    current = clean(existing)
    if marker in current:
        return current
    return f"{current} | {marker}" if current else marker


def canonical_view(row: dict[str, str], old_key: str, new_key: str) -> dict[str, str]:
    mapped = dict(row)
    a = new_key if clean(row.get("team_a_key")) == old_key else clean(row.get("team_a_key"))
    b = new_key if clean(row.get("team_b_key")) == old_key else clean(row.get("team_b_key"))
    score_a = clean(row.get("team_a_score"))
    score_b = clean(row.get("team_b_score"))
    site = clean(row.get("site_type"))
    winner = new_key if clean(row.get("result_winner_team_key")) == old_key else clean(row.get("result_winner_team_key"))
    designated = new_key if clean(row.get("designated_home_team_key")) == old_key else clean(row.get("designated_home_team_key"))
    if a <= b:
        mapped["team_a_key"] = a
        mapped["team_b_key"] = b
        mapped["team_a_score"] = score_a
        mapped["team_b_score"] = score_b
    else:
        mapped["team_a_key"] = b
        mapped["team_b_key"] = a
        mapped["team_a_score"] = score_b
        mapped["team_b_score"] = score_a
        if site == "TEAM_A_HOME":
            site = "TEAM_B_HOME"
        elif site == "TEAM_B_HOME":
            site = "TEAM_A_HOME"
    mapped["site_type"] = site
    mapped["result_winner_team_key"] = winner
    mapped["designated_home_team_key"] = designated
    return mapped


def merge_value(field: str, survivor: str, absorbed: str) -> str:
    left = clean(survivor)
    right = clean(absorbed)
    if left == right:
        return left
    if not right:
        return left
    if not left:
        return right
    if field == "site_type" and {left, right} <= {"", "UNKNOWN"}:
        return "UNKNOWN"
    raise ScopedIdentityError(
        f"canonical counterpart conflict in {field}: survivor={left!r}, absorbed={right!r}"
    )


def build_plan(
    repo: Path,
    *,
    source_program: str,
    source_label: str,
    source_game_id: str,
    old_key: str,
    new_key: str,
    new_name: str,
    stale_canonical_id: str,
    survivor_canonical_id: str,
    basis: str,
) -> dict[str, Any]:
    repo = repo.resolve()
    if not all(
        clean(value)
        for value in (
            source_program,
            source_label,
            source_game_id,
            old_key,
            new_key,
            new_name,
            stale_canonical_id,
            survivor_canonical_id,
            basis,
        )
    ):
        raise ScopedIdentityError("all source-scoped reconciliation arguments are required")
    if old_key == new_key:
        raise ScopedIdentityError("old and new opponent keys must differ")
    if stale_canonical_id == survivor_canonical_id:
        raise ScopedIdentityError("stale and survivor canonical IDs must differ")

    paths = {
        "opponents": repo / "schools" / source_program / "opponents.csv",
        "source_games": repo / "schools" / source_program / "source-games.csv",
        "canonical": repo / "data/canonical/games.csv",
        "assertions": repo / "data/evidence/game-assertions.csv",
        "discrepancies": repo / "data/reconciliation/discrepancies.csv",
        "programs": repo / "data/reference/programs.csv",
    }
    for label, path in paths.items():
        if not path.is_file():
            raise ScopedIdentityError(f"required {label} file is missing: {path}")

    _, programs = read_csv(paths["programs"])
    target_program = next(
        (row for row in programs if clean(row.get("program_key")) == new_key), None
    )
    if target_program is None:
        raise ScopedIdentityError(f"target program {new_key!r} is absent from registry")
    if not truthy(target_program.get("current_d1", "")):
        raise ScopedIdentityError(f"target program {new_key!r} is not current D1")

    _, opponents = read_csv(paths["opponents"])
    opponent_matches = [
        row
        for row in opponents
        if clean(row.get("source_opponent_label")) == source_label
        and clean(row.get("canonical_opponent_key")) == old_key
    ]
    if len(opponent_matches) != 1:
        raise ScopedIdentityError(
            f"expected exactly one opponents.csv row for {source_label!r}/{old_key!r}; "
            f"found {len(opponent_matches)}"
        )
    try:
        expected_games = int(clean(opponent_matches[0].get("games_with_source_label")))
    except ValueError as exc:
        raise ScopedIdentityError("opponents.csv games_with_source_label is invalid") from exc
    if expected_games != 1:
        raise ScopedIdentityError(
            "source-scoped transaction currently requires a one-game literal label population"
        )

    _, source_games = read_csv(paths["source_games"])
    game_matches = [
        row
        for row in source_games
        if clean(row.get("source_game_id")) == source_game_id
        and clean(row.get("source_opponent_label")) == source_label
        and clean(row.get("normalized_opponent_key")) == old_key
    ]
    if len(game_matches) != 1:
        raise ScopedIdentityError(
            f"expected exactly one source game {source_game_id!r} with old identity; found {len(game_matches)}"
        )

    _, assertions = read_csv(paths["assertions"])
    assertion_matches = [
        row
        for row in assertions
        if clean(row.get("source_program_key")) == source_program
        and clean(row.get("source_game_id")) == source_game_id
        and clean(row.get("canonical_game_id")) == stale_canonical_id
        and clean(row.get("normalized_opponent_key")) == old_key
    ]
    if len(assertion_matches) != 1:
        raise ScopedIdentityError(
            "expected exactly one stale assertion for the named source game/canonical row"
        )

    _, discrepancies = read_csv(paths["discrepancies"])
    stale_discrepancies = [
        row
        for row in discrepancies
        if clean(row.get("canonical_game_id")) == stale_canonical_id
    ]
    if stale_discrepancies:
        raise ScopedIdentityError(
            f"stale canonical row has {len(stale_discrepancies)} discrepancy row(s); explicit review required"
        )

    canonical_fields, canonical = read_csv(paths["canonical"])
    by_id = {
        clean(row.get("canonical_game_id")): row
        for row in canonical
        if clean(row.get("canonical_game_id"))
    }
    stale = by_id.get(stale_canonical_id)
    survivor = by_id.get(survivor_canonical_id)
    if stale is None or survivor is None:
        raise ScopedIdentityError("stale or survivor canonical row is missing")
    stale_mapped = canonical_view(stale, old_key, new_key)

    for field in (
        "season_label",
        "game_date",
        "date_precision",
        "team_a_key",
        "team_b_key",
        "team_a_score",
        "team_b_score",
        "result_winner_team_key",
        "overtime_periods",
        "game_type",
    ):
        if clean(stale_mapped.get(field)) != clean(survivor.get(field)):
            raise ScopedIdentityError(
                f"named rows are not the same real game after scoped remap: {field} "
                f"{clean(stale_mapped.get(field))!r} != {clean(survivor.get(field))!r}"
            )

    final_values: dict[str, str] = {}
    for field in MERGE_FIELDS:
        if field not in canonical_fields:
            continue
        final_values[field] = merge_value(
            field,
            survivor.get(field, ""),
            stale_mapped.get(field, ""),
        )

    marker = (
        "[SOURCE_SCOPED_OPPONENT_IDENTITY_RECONCILIATION "
        f"source={source_program}/{source_game_id};label={source_label};"
        f"from={old_key};to={new_key};absorbed={stale_canonical_id}]"
    )
    final_values["notes"] = append_note(survivor.get("notes", ""), marker)

    payload = {
        "schema_version": 1,
        "git_head": git_head(repo),
        "source_program": source_program,
        "source_opponent_label": source_label,
        "source_game_id": source_game_id,
        "old_key": old_key,
        "new_key": new_key,
        "new_name": new_name,
        "stale_canonical_id": stale_canonical_id,
        "survivor_canonical_id": survivor_canonical_id,
        "basis": basis,
        "final_canonical_values": final_values,
        "fingerprints": {
            str(path.relative_to(repo)): sha_file(path)
            for path in paths.values()
        },
    }
    return {"sha256": sha_text(stable(payload)), "payload": payload}


def apply_plan(repo: Path, plan: dict[str, Any], expected_sha256: str) -> dict[str, Any]:
    if clean(expected_sha256) != plan["sha256"]:
        raise ScopedIdentityError(
            f"sealed plan hash mismatch: expected {expected_sha256}, actual {plan['sha256']}"
        )
    payload = plan["payload"]
    source_program = payload["source_program"]
    source_label = payload["source_opponent_label"]
    source_game_id = payload["source_game_id"]
    old_key = payload["old_key"]
    new_key = payload["new_key"]
    new_name = payload["new_name"]
    stale_id = payload["stale_canonical_id"]
    survivor_id = payload["survivor_canonical_id"]

    paths = [
        repo / "schools" / source_program / "opponents.csv",
        repo / "schools" / source_program / "source-games.csv",
        repo / "data/canonical/games.csv",
        repo / "data/evidence/game-assertions.csv",
    ]
    originals = {path: path.read_bytes() for path in paths}
    try:
        opp_fields, opponents = read_csv(paths[0])
        opp_matches = [
            row
            for row in opponents
            if clean(row.get("source_opponent_label")) == source_label
            and clean(row.get("canonical_opponent_key")) == old_key
        ]
        if len(opp_matches) != 1:
            raise ScopedIdentityError("opponents.csv changed after sealing")
        opp_matches[0]["canonical_opponent_key"] = new_key
        opp_matches[0]["canonical_opponent_name"] = new_name
        if "current_d1" in opp_fields:
            opp_matches[0]["current_d1"] = "Yes"

        source_fields, source_games = read_csv(paths[1])
        source_matches = [
            row
            for row in source_games
            if clean(row.get("source_game_id")) == source_game_id
            and clean(row.get("source_opponent_label")) == source_label
            and clean(row.get("normalized_opponent_key")) == old_key
        ]
        if len(source_matches) != 1:
            raise ScopedIdentityError("source-games.csv changed after sealing")
        source_matches[0]["normalized_opponent_key"] = new_key
        source_matches[0]["normalized_opponent_name"] = new_name
        if "opponent_current_d1" in source_fields:
            source_matches[0]["opponent_current_d1"] = "Yes"
        source_matches[0]["notes"] = append_note(
            source_matches[0].get("notes", ""),
            f"Identity correction during Implementation: literal source label {source_label!r} resolves to {new_name} ({new_key}), not {old_key}.",
        )

        canonical_fields, canonical = read_csv(paths[2])
        by_id = {
            clean(row.get("canonical_game_id")): row
            for row in canonical
            if clean(row.get("canonical_game_id"))
        }
        if stale_id not in by_id or survivor_id not in by_id:
            raise ScopedIdentityError("canonical rows changed after sealing")
        survivor = by_id[survivor_id]
        for field, value in payload["final_canonical_values"].items():
            if field in canonical_fields:
                survivor[field] = value
        canonical = [
            row for row in canonical if clean(row.get("canonical_game_id")) != stale_id
        ]

        assertion_fields, assertions = read_csv(paths[3])
        assertion_matches = [
            row
            for row in assertions
            if clean(row.get("source_program_key")) == source_program
            and clean(row.get("source_game_id")) == source_game_id
            and clean(row.get("canonical_game_id")) == stale_id
            and clean(row.get("normalized_opponent_key")) == old_key
        ]
        if len(assertion_matches) != 1:
            raise ScopedIdentityError("assertion row changed after sealing")
        assertion_matches[0]["canonical_game_id"] = survivor_id
        assertion_matches[0]["normalized_opponent_key"] = new_key
        assertion_matches[0]["normalized_opponent_name"] = new_name
        if "match_status" in assertion_fields:
            assertion_matches[0]["match_status"] = "MATCHED"
        if "match_method" in assertion_fields:
            assertion_matches[0]["match_method"] = "SOURCE_SCOPED_IDENTITY_RECONCILIATION"

        write_csv(paths[0], opp_fields, opponents)
        write_csv(paths[1], source_fields, source_games)
        write_csv(paths[2], canonical_fields, canonical)
        write_csv(paths[3], assertion_fields, assertions)

        validation = subprocess.run(
            [sys.executable, "tools/validate_data.py"], cwd=repo, text=True
        )
        if validation.returncode != 0:
            raise ScopedIdentityError("repository validation failed after scoped identity apply")
    except Exception:
        for path, raw in originals.items():
            path.write_bytes(raw)
        raise

    return {
        "plan_sha256": plan["sha256"],
        "source_rows_changed": 1,
        "assertions_repointed": 1,
        "canonical_rows_absorbed": 1,
        "survivor_canonical_id": survivor_id,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--source-program", required=True)
    parser.add_argument("--source-opponent-label", required=True)
    parser.add_argument("--source-game-id", required=True)
    parser.add_argument("--from-key", required=True)
    parser.add_argument("--to-key", required=True)
    parser.add_argument("--to-name", required=True)
    parser.add_argument("--stale-canonical-id", required=True)
    parser.add_argument("--survivor-canonical-id", required=True)
    parser.add_argument("--basis", required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-plan-sha256", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    try:
        plan = build_plan(
            repo,
            source_program=args.source_program,
            source_label=args.source_opponent_label,
            source_game_id=args.source_game_id,
            old_key=args.from_key,
            new_key=args.to_key,
            new_name=args.to_name,
            stale_canonical_id=args.stale_canonical_id,
            survivor_canonical_id=args.survivor_canonical_id,
            basis=args.basis,
        )
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if not args.apply:
            print("College Basketball History — source-scoped opponent identity plan")
            print(f"Git HEAD:             {plan['payload']['git_head']}")
            print(f"Source:               {plan['payload']['source_program']}/{plan['payload']['source_game_id']}")
            print(f"Literal label:        {plan['payload']['source_opponent_label']}")
            print(f"Identity correction: {plan['payload']['old_key']} -> {plan['payload']['new_key']}")
            print(
                "Canonical absorb:     "
                f"{plan['payload']['stale_canonical_id']} -> {plan['payload']['survivor_canonical_id']}"
            )
            print(f"Plan SHA-256:         {plan['sha256']}")
            print("DRY RUN: no tracked basketball data changed.")
            return 0
        result = apply_plan(repo, plan, args.expected_plan_sha256)
        print("PASS: SOURCE-SCOPED OPPONENT IDENTITY RECONCILIATION")
        for key, value in result.items():
            print(f"{key}={value}")
        return 0
    except (ScopedIdentityError, FileNotFoundError, KeyError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
