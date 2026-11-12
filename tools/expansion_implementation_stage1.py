#!/usr/bin/env python3
"""Read-only Stage 1 foundation for frozen All-History expansions.

This is NOT an Integration Freeze, onboarding, Phase 0, or mutation entrypoint.
It reconstructs the candidate only in a separately supplied *external* directory,
after exact Research-freeze verification against the original Git baseline.
Canonical reconciliation is an inventory, never a canonical write decision.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping

from all_history_expansion_freeze import (
    OPPONENT_EXTENSION_FIELDS, VENUE_EXTENSION_FIELDS,
    authenticate_baseline, canonical_row_sha256, validate_delta_payload,
    verify_expansion,
)
from match_games import CONFIDENT, NEW_GAME, REVIEW, identify_game, ordered_pair, compare_fields

PACKAGE_FILES = (
    "source-games.csv", "opponents.csv", "venues.csv",
    "conferences.csv", "notes.md", "source-notes.md",
)
SUPPORT_ACTIONS = ("NEW_SUPPLEMENTAL", "REUSE_INHERITED", "EXTEND_INHERITED")


class Stage1Stop(ValueError):
    """An unsafe or unauthorized expansion candidate has been rejected."""


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def git_bytes(repo: Path, commit: str, path: str) -> bytes:
    if not commit or len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise Stage1Stop("Exact 40-character Git commit SHA required")
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode:
        raise Stage1Stop(f"Missing authenticated Git path {commit}:{path}")
    return result.stdout


def git_revision(repo: Path, name: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", name],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise Stage1Stop(f"Git reference unavailable: {name}")
    return result.stdout.strip()


def csv_rows(raw: bytes, label: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""))
        fields = list(reader.fieldnames or ())
        if not fields or len(fields) != len(set(fields)) or any(not f for f in fields):
            raise Stage1Stop(f"Invalid CSV header: {label}")
        rows = list(reader)
        if any(None in row or any(not isinstance(v, str) for v in row.values()) for row in rows):
            raise Stage1Stop(f"Invalid CSV record: {label}")
        return fields, rows
    except (UnicodeError, csv.Error) as exc:
        raise Stage1Stop(f"Unreadable CSV: {label}") from exc


def render_csv(fields: list[str], rows: list[dict[str, str]]) -> bytes:
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n", extrasaction="raise")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def materialize_support(
    inherited_rows: list[dict[str, str]], fields: list[str], support: list[dict[str, str]],
    identity_fields: tuple[str, ...], allowed_extensions: set[str] | frozenset[str],
    label: str,
) -> tuple[list[dict[str, str]], dict[str, int], list[dict[str, str]]]:
    """Exact action semantics; frozen baseline rows are never changed in place."""
    result = [dict(r) for r in inherited_rows]
    indexes: dict[tuple[str, ...], list[int]] = defaultdict(list)
    for i, item in enumerate(result):
        indexes[tuple(item.get(f, "").strip() for f in identity_fields)].append(i)
    counts: Counter[str] = Counter()
    provenance: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    for item in support:
        action = item["support_action"].strip()
        if action not in SUPPORT_ACTIONS:
            raise Stage1Stop(f"{label}: unsupported support action {action}")
        try:
            candidate = json.loads(item["candidate_row_json"])
        except (ValueError, TypeError) as exc:
            raise Stage1Stop(f"{label}: invalid candidate JSON") from exc
        if not isinstance(candidate, dict) or set(candidate) != set(fields) or any(
            not isinstance(v, str) for v in candidate.values()
        ):
            raise Stage1Stop(f"{label}: candidate row schema mismatch")
        identity = tuple(candidate[f].strip() for f in identity_fields)
        if identity in seen:
            raise Stage1Stop(f"{label}: duplicate supplemental identity {identity}")
        seen.add(identity)
        matches = indexes.get(identity, [])
        changes = [v.strip() for v in item["changed_fields"].split(";") if v.strip()]
        if len(changes) != len(set(changes)):
            raise Stage1Stop(f"{label}: repeated changed field")
        if action == "NEW_SUPPLEMENTAL":
            if matches or item["baseline_row_sha256"].strip() or changes:
                raise Stage1Stop(f"{label}: new support collides with inherited authority")
            indexes[identity] = [len(result)]
            result.append(candidate)
        else:
            if len(matches) != 1:
                raise Stage1Stop(f"{label}: inherited support identity not unique")
            idx = matches[0]
            original = inherited_rows[idx]
            if item["baseline_row_sha256"].strip() != canonical_row_sha256(original):
                raise Stage1Stop(f"{label}: inherited support row hash changed")
            diff = {f for f in fields if original[f] != candidate[f]}
            if action == "REUSE_INHERITED":
                if changes or diff:
                    raise Stage1Stop(f"{label}: REUSE_INHERITED would modify inherited row")
            else:
                if set(changes) != diff or not diff or diff - set(allowed_extensions):
                    raise Stage1Stop(f"{label}: contradictory or forbidden inherited extension")
                result[idx] = candidate
        counts[action] += 1
        provenance.append({"support_id": item["support_id"], "action": action,
                           "identity": "|".join(identity),
                           "candidate_sha256": canonical_row_sha256(candidate)})
    return result, {act: counts[act] for act in SUPPORT_ACTIONS}, provenance


def build_candidate(baseline: Mapping[str, Any], payload: Mapping[str, bytes],
                    validated: Mapping[str, Any]) -> tuple[dict[str, bytes], dict[str, Any]]:
    """Pure candidate projection; does not assign canonical IDs or write data."""
    fields = baseline["source_fields"]
    supplemental = validated["source_rows"]
    source_ids = [row["source_game_id"].strip() for row in baseline["source_rows"] + supplemental]
    if any(not sid for sid in source_ids) or len(set(source_ids)) != len(source_ids):
        raise Stage1Stop("Duplicate/blank inherited or supplemental source-game ID")
    if any(set(row) != set(fields) for row in supplemental):
        raise Stage1Stop("Supplemental source-game schema differs from inherited package")
    combined_sources = [dict(r) for r in baseline["source_rows"] + supplemental]
    opp, opp_counts, opp_provenance = materialize_support(
        baseline["opponent_rows"], baseline["opponent_fields"],
        validated["opponent_support_rows"],
        ("source_opponent_label", "canonical_opponent_key"),
        OPPONENT_EXTENSION_FIELDS, "opponent support",
    )
    ven, ven_counts, ven_provenance = materialize_support(
        baseline["venue_rows"], baseline["venue_fields"],
        validated["venue_support_rows"], ("venue_key",),
        VENUE_EXTENSION_FIELDS, "venue support",
    )
    original = baseline["package_bytes"]
    def append_notes(name: str, supplement: str) -> bytes:
        inherited = original[name]
        if not inherited.endswith(b"\n"):
            inherited += b"\n"
        return (inherited + b"\n---\n\n## Accepted supplemental All-History expansion\n\n"
                + payload[supplement])
    candidate = {
        "source-games.csv": render_csv(fields, combined_sources),
        "opponents.csv": render_csv(baseline["opponent_fields"], opp),
        "venues.csv": render_csv(baseline["venue_fields"], ven),
        "conferences.csv": original["conferences.csv"],
        "notes.md": append_notes("notes.md", "expansion-notes.md"),
        "source-notes.md": append_notes("source-notes.md", "expansion-source-notes.md"),
    }
    # Reparse the projected source ledger to prove byte roundtrip and exact inheritance.
    _, check = csv_rows(candidate["source-games.csv"], "projected source-games.csv")
    if check != combined_sources or check[:len(baseline["source_rows"])] != baseline["source_rows"]:
        raise Stage1Stop("Projection altered inherited source-game evidence")
    return candidate, {
        "inherited_source_game_count": len(baseline["source_rows"]),
        "supplemental_new_source_game_count": len(supplemental),
        "combined_source_game_count": len(combined_sources),
        "inherited_source_id_population_sha256": sha256(canonical_bytes(sorted(
            row["source_game_id"].strip() for row in baseline["source_rows"]))),
        "opponent_support_actions": opp_counts,
        "venue_support_actions": ven_counts,
        "opponent_support_provenance": opp_provenance,
        "venue_support_provenance": ven_provenance,
    }


def reconcile_canonical(school: str, supplemental: list[dict[str, str]],
                        canonical: list[dict[str, str]]) -> dict[str, Any]:
    """Reuse the permanent matcher; ambiguous identities are hard blockers."""
    index: dict[tuple[str, tuple[str, str]], list[dict[str, str]]] = defaultdict(list)
    for row in canonical:
        if school not in (row.get("team_a_key"), row.get("team_b_key")):
            continue
        key = (row["season_label"], ordered_pair(row["team_a_key"], row["team_b_key"]))
        index[key].append(row)
    rows: list[dict[str, Any]] = []
    reuse_by_id: dict[str, list[str]] = defaultdict(list)
    seen_strong: dict[tuple[str, str, str, str, str], list[str]] = defaultdict(list)
    counts = Counter()
    for src in supplemental:
        sid = src["source_game_id"].strip()
        pair = ordered_pair(school, src["normalized_opponent_key"])
        candidates = index.get((src["season_label"], pair), [])
        status, match, method = identify_game(src, candidates)
        if status == CONFIDENT:
            reuse_by_id[match].append(sid)
            can = next(c for c in candidates if c["canonical_game_id"] == match)
            differences = compare_fields(src, can)
        else:
            differences = []
        label = "REUSE_CANONICAL" if status == CONFIDENT else (
            "PROVISIONAL_NEW_CANONICAL" if status == NEW_GAME else "IDENTITY_REVIEW_BLOCKER")
        counts[label] += 1
        rows.append({"source_game_id": sid, "classification": label,
                     "canonical_game_id": match if status == CONFIDENT else "",
                     "candidate_canonical_game_id": match if status == REVIEW else "",
                     "match_method": method, "field_disagreements": differences,
                     "same_pair_season_candidate_count": len(candidates)})
        if src.get("game_date") and src.get("team_score") and src.get("opponent_score"):
            key = (src["season_label"], src["game_date"], src["normalized_opponent_key"],
                   src["team_score"], src["opponent_score"])
            seen_strong[key].append(sid)
    return {
        "counts": {label: counts[label] for label in (
            "REUSE_CANONICAL", "PROVISIONAL_NEW_CANONICAL", "IDENTITY_REVIEW_BLOCKER")},
        "game_rows": rows,
        "duplicate_canonical_reuse": {k: v for k, v in sorted(reuse_by_id.items()) if len(v) > 1},
        "possible_duplicate_supplemental_rows": [v for v in seen_strong.values() if len(v) > 1],
    }


def read_csv_at_git(repo: Path, commit: str, path: str) -> list[dict[str, str]]:
    return csv_rows(git_bytes(repo, commit, path), path)[1]


def stage1(repo: Path, school: str, artifact: Path, expected_sha: str,
           research_base: str, main_sha: str, output: Path) -> dict[str, Any]:
    repo, artifact, output = repo.resolve(), artifact.resolve(), output.resolve()
    if output == repo or repo in output.parents:
        raise Stage1Stop("Stage 1 rehearsal output must be outside tracked repository")
    if output.exists():
        raise Stage1Stop("Stage 1 output already exists; refuse silent overwrite")
    if git_revision(repo, "refs/remotes/origin/main") != main_sha:
        raise Stage1Stop("Current origin/main differs from exact authenticated protected main")
    git_revision(repo, main_sha + "^{commit}")
    if sha256(artifact.read_bytes()) != expected_sha:
        raise Stage1Stop("Exact expansion freeze ZIP SHA-256 mismatch")
    verified = verify_expansion(repo, artifact)
    if verified.get("status") != "VERIFIED_EXPANSION_RESEARCH_FROZEN":
        raise Stage1Stop("Permanent expansion freeze fresh verification did not pass")
    if (verified["school_key"], verified["research_base_sha"]) != (school, research_base):
        raise Stage1Stop("Research Freeze school or immutable research_base_sha mismatch")
    baseline = authenticate_baseline(repo, school, research_base)
    with zipfile.ZipFile(artifact) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
        manifest = json.loads(members["expansion-freeze.json"])
        payload = {name: raw for name, raw in members.items() if name != "expansion-freeze.json"}
    validated = validate_delta_payload(payload, baseline, school,
                                      manifest["researched_inception_season"])
    candidate, census = build_candidate(baseline, payload, validated)
    blockers: list[dict[str, Any]] = []
    for name in PACKAGE_FILES:
        current = git_bytes(repo, main_sha, f"schools/{school}/{name}")
        if current != baseline["package_bytes"][name]:
            blockers.append({"class": "CURRENT_MAIN_INHERITED_PACKAGE_DRIFT", "path": f"schools/{school}/{name}"})
    for label, path, key, expected in (
        ("PROGRAM", "data/reference/programs.csv", "program_key", baseline["program"]),
        ("SCOPE", "data/reference/program-top-level-scope.csv", "school", baseline["scope_row"]),
        ("ACCOMPLISHMENT", "data/reference/program-accomplishments.csv", "program_key", baseline["accomplishment_row"]),
    ):
        if expected is None:
            continue
        current = [r for r in read_csv_at_git(repo, main_sha, path) if r.get(key) == expected[key]]
        if len(current) != 1 or canonical_row_sha256(current[0]) != canonical_row_sha256(expected):
            blockers.append({"class": "CURRENT_MAIN_INHERITED_METADATA_DRIFT", "surface": label})
    # Explicitly refuse inherited canonical history drift even when source package is unchanged.
    base_canonical = read_csv_at_git(repo, research_base, "data/canonical/games.csv")
    main_canonical = read_csv_at_git(repo, main_sha, "data/canonical/games.csv")
    baseline_ids = set(baseline["published_canonical_ids"])
    base_by_id = {r["canonical_game_id"]: r for r in base_canonical if r["canonical_game_id"] in baseline_ids}
    main_by_id = {r["canonical_game_id"]: r for r in main_canonical if r["canonical_game_id"] in baseline_ids}
    canonical_drift = sorted(k for k in baseline_ids if base_by_id.get(k) != main_by_id.get(k))
    if canonical_drift:
        blockers.append({"class": "CURRENT_MAIN_INHERITED_CANONICAL_DRIFT", "canonical_game_ids": canonical_drift})
    # A registered venue key is a physical identity, not permission to overwrite a different building.
    global_venues = read_csv_at_git(repo, main_sha, "data/reference/venues.csv")
    venues_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for venue in global_venues:
        venues_by_key[venue.get("venue_key", "").strip()].append(venue)
    registered_programs = {r["program_key"] for r in read_csv_at_git(
        repo, main_sha, "data/reference/programs.csv")}
    for item in validated["venue_support_rows"]:
        proposed = json.loads(item["candidate_row_json"])
        matches = venues_by_key.get(item["venue_key"].strip(), [])
        if len(matches) > 1:
            blockers.append({"class": "DUPLICATE_GLOBAL_VENUE_KEY", "support_id": item["support_id"]})
        elif matches:
            current = matches[0]
            if (proposed.get("city", "").casefold(), proposed.get("state", "").upper()) != (
                current.get("city", "").casefold(), current.get("state", "").upper()
            ) and proposed.get("city") and proposed.get("state"):
                blockers.append({"class": "CONFLICTING_GLOBAL_VENUE_GEOGRAPHY",
                                 "support_id": item["support_id"],
                                 "existing_venue_id": current.get("venue_id", "")})
    for item in validated["opponent_support_rows"]:
        proposed = json.loads(item["candidate_row_json"])
        if (item["canonical_opponent_key"] in registered_programs and
                proposed.get("current_d1", "").strip().casefold() not in {"yes", "true", "1"}):
            blockers.append({"class": "REGISTERED_PROGRAM_OPPONENT_CLASSIFICATION_CONFLICT",
                             "support_id": item["support_id"],
                             "opponent_key": item["canonical_opponent_key"]})
    identity = reconcile_canonical(school, validated["source_rows"], main_canonical)
    if identity["counts"]["IDENTITY_REVIEW_BLOCKER"]:
        blockers.append({"class": "AMBIGUOUS_SUPPLEMENTAL_CANONICAL_IDENTITIES", "source_game_ids": [
            r["source_game_id"] for r in identity["game_rows"] if r["classification"] == "IDENTITY_REVIEW_BLOCKER"]})
    if identity["duplicate_canonical_reuse"]:
        blockers.append({"class": "MULTIPLE_SUPPLEMENTAL_SOURCES_REUSE_ONE_CANONICAL", "population": identity["duplicate_canonical_reuse"]})
    if identity["possible_duplicate_supplemental_rows"]:
        blockers.append({"class": "POSSIBLE_DUPLICATE_SUPPLEMENTAL_GAMES", "population": identity["possible_duplicate_supplemental_rows"]})
    if manifest["schema_version"] != 1:
        blockers.append({"class": "V2_SCOPE_AND_INHERITED_UNPUBLISHED_REUSE_NOT_YET_MATERIALIZED"})
    # This adapter deliberately cannot authorize release or write a school Integration Freeze.
    blockers.append({"class": "DOWNSTREAM_EXPANSION_INTEGRATION_FREEZE_AND_GUARDED_PHASE0_MISSING"})
    report = {
        "kind": "ALL_HISTORY_EXPANSION_STAGE1_REHEARSAL", "status": "BLOCKED",
        "school_key": school, "protected_main_sha": main_sha,
        "research_base_sha": research_base, "expansion_freeze_sha256": expected_sha,
        "freeze_manifest_sha256": sha256(members["expansion-freeze.json"]),
        "researched_inception_season": manifest["researched_inception_season"],
        "baseline_package_member_sha256": baseline["package_member_sha256"],
        "candidate_member_sha256": {k: sha256(v) for k,v in sorted(candidate.items())},
        "season_accounting_count": len(validated["season_accounting_rows"]),
        "non_d1_owner_scan_count": len(validated["non_d1_scan_rows"]),
        "accepted_residual_count": len(validated["residual_rows"]),
        "census": census, "canonical_identity_census": identity, "blockers": blockers,
        "write_authority": "NONE_REHEARSAL_ONLY",
    }
    output.mkdir(parents=True)
    for name, raw in candidate.items():
        (output / name).write_bytes(raw)
    (output / "expansion-stage1-reconciliation.json").write_bytes(canonical_bytes(report))
    return report


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("school_key")
    p.add_argument("freeze_zip", type=Path)
    p.add_argument("--expected-sha256", required=True)
    p.add_argument("--research-base", required=True)
    p.add_argument("--main-sha", required=True)
    p.add_argument("--repo", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args(argv)
    try:
        report = stage1(args.repo,args.school_key,args.freeze_zip,args.expected_sha256,
                        args.research_base,args.main_sha,args.output)
        print(json.dumps({"status": report["status"], "school": args.school_key,
             "candidate": str(args.output), "identity": report["canonical_identity_census"]["counts"],
             "blocker_classes": [x["class"] for x in report["blockers"]]}, indent=2))
        return 0  # A checkpointed BLOCKED inventory is an expected, inspectable result.
    except (Stage1Stop, OSError, ValueError) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
