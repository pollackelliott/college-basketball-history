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
from datetime import date
from pathlib import Path
from game_assertion_store import read_game_assertions_at_git
from typing import Any, Mapping

from all_history_expansion_freeze import (
    OPPONENT_EXTENSION_FIELDS, VENUE_EXTENSION_FIELDS,
    authenticate_baseline, canonical_row_sha256, validate_delta_payload,
    verify_expansion,
)
from match_games import (
    CONFIDENT, NEW_GAME, REVIEW, identify_game, ordered_pair, compare_fields,
    scores_match, source_scores_in_canonical_orientation,
)

PACKAGE_FILES = (
    "source-games.csv", "opponents.csv", "venues.csv",
    "conferences.csv", "notes.md", "source-notes.md",
)
SUPPORT_ACTIONS = ("NEW_SUPPLEMENTAL", "REUSE_INHERITED", "EXTEND_INHERITED")

# Protected current main may legitimately enrich a shared inherited canonical game
# after the immutable Research base was frozen (for example, another school's
# completed Implementation can add exact venue/locality support).  Expansion Stage 1
# may inherit only this narrow non-historical representation delta automatically.
# Everything that can change game identity, result, H/A/N, game type, postseason
# semantics, or administrative outcome remains fail-closed.
CANONICAL_CURRENT_MAIN_ENRICHMENT_FIELDS = frozenset({
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
    "notes",
})


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


def classify_current_main_canonical_drift(
    base_by_id: Mapping[str, dict[str, str]],
    main_by_id: Mapping[str, dict[str, str]],
    canonical_ids: list[str],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Partition accepted representation enrichment from historical-semantic drift.

    The immutable Research-base row remains provenance.  Protected current main may
    be inherited automatically only when the same canonical ID still exists with the
    exact same schema and every changed field is confined to venue/locality/provenance
    enrichment.  Any identity, result, H/A/N, game-type, postseason, administrative,
    or status change remains unresolved for an explicit authority path.
    """
    accepted: list[dict[str, Any]] = []
    unresolved: list[str] = []
    for game_id in canonical_ids:
        before = base_by_id.get(game_id)
        after = main_by_id.get(game_id)
        if before is None or after is None or set(before) != set(after):
            unresolved.append(game_id)
            continue
        changed = sorted(
            field for field in before if before.get(field, "") != after.get(field, "")
        )
        if changed and set(changed) <= CANONICAL_CURRENT_MAIN_ENRICHMENT_FIELDS:
            accepted.append({
                "canonical_game_id": game_id,
                "changed_fields": changed,
            })
            continue
        unresolved.append(game_id)
    return accepted, unresolved


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



IDENTITY_REBASE_SOURCE_FIELDS = frozenset({
    "normalized_opponent_key",
    "normalized_opponent_name",
})
OPPONENT_REBASE_CORE_FIELDS = (
    "source_program_key",
    "source_opponent_label",
    "canonical_opponent_key",
    "canonical_opponent_name",
    "current_d1",
    "resolution_status",
    "user_choice",
)


def _resolved_external_correction_source_ids(
    validated: Mapping[str, Any],
) -> set[str]:
    """Return inherited source IDs explicitly routed to completed correction authority."""
    result: set[str] = set()
    for row in validated.get("correction_question_rows", []):
        if row.get("expansion_impact", "").strip() != "NO_EXPANSION_IMPACT":
            continue
        disposition = row.get("disposition", "").strip()
        if not disposition.startswith("RESOLVED_EXTERNALLY"):
            continue
        for value in row.get("inherited_source_game_id", "").split("|"):
            value = value.strip()
            if value:
                result.add(value)
    return result


def _git_lines(repo: Path, *args: str) -> list[str]:
    cp = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if cp.returncode:
        return []
    return [line.strip() for line in cp.stdout.splitlines() if line.strip()]


def _completed_post_freeze_package_correction_authorities(
    repo: Path,
    school: str,
    research_base_sha: str,
    main_sha: str,
    member: str,
    current_raw: bytes,
) -> list[dict[str, Any]]:
    """Authenticate exact completed correction authority for one inherited package member.

    Expansion Research remains immutable.  A later package member may be inherited only
    when control preserves a completed correction Production proof, its independent
    verification passes, the exact two-parent correction merge is after the Research
    base and an ancestor of current main, the correction merge changed this exact school
    package path, and current main still contains byte-identical correction output.
    """
    if not research_base_sha:
        return []
    try:
        control_sha = git_revision(repo, "refs/remotes/origin/remote-control")
    except Stage1Stop:
        return []
    prefix = f".remote-implementation/checkpoints/{school}"
    paths = _git_lines(
        repo, "ls-tree", "-r", "--name-only", control_sha, "--", prefix
    )
    request_paths = sorted(
        path for path in paths
        if path.endswith("/request.json") and "release-production-proof" in path
    )
    member_path = f"schools/{school}/{member}"
    matches: list[dict[str, Any]] = []
    for request_path in request_paths:
        try:
            request_raw = git_bytes(repo, control_sha, request_path)
            request = json.loads(request_raw)
        except (Stage1Stop, json.JSONDecodeError, TypeError):
            continue
        request_id = str(request.get("request_id") or "")
        merge_sha = str(request.get("merge_sha") or "")
        target_sha = str(request.get("target_sha") or "")
        if (
            request.get("kind") != "REMOTE_IMPLEMENTATION_REQUEST"
            or request.get("operation") != "RELEASE_PRODUCTION_PROOF"
            or request.get("school_key") != school
            or request.get("target_branch") != f"data/{school}-correction"
            or len(merge_sha) != 40
            or len(target_sha) != 40
        ):
            continue
        checkpoint_path = (
            request_path.rsplit("/", 1)[0] + "/checkpoint-manifest.json"
        )
        verification_path = (
            f".remote-implementation/verifications/{school}/{request_id}/"
            "production-verification.json"
        )
        try:
            checkpoint_raw = git_bytes(repo, control_sha, checkpoint_path)
            verification_raw = git_bytes(repo, control_sha, verification_path)
            checkpoint = json.loads(checkpoint_raw)
            verification = json.loads(verification_raw)
        except (Stage1Stop, json.JSONDecodeError, TypeError):
            continue
        if (
            checkpoint.get("kind") != "REMOTE_IMPLEMENTATION_EXACT_PRODUCTION_CHECKPOINT"
            or checkpoint.get("status") != "PRODUCTION_PROOF_PASS"
            or checkpoint.get("request_id") != request_id
            or checkpoint.get("school_key") != school
            or checkpoint.get("merge_sha") != merge_sha
            or checkpoint.get("merged") is not True
            or checkpoint.get("production_proof") is not True
            or checkpoint.get("request_sha256") != sha256(request_raw)
        ):
            continue
        if (
            verification.get("kind") != "REMOTE_IMPLEMENTATION_EXACT_PRODUCTION_VERIFICATION"
            or verification.get("status") != "COMPLETE"
            or verification.get("exact_production_equivalence") != "PASS"
            or verification.get("request_id") != request_id
            or verification.get("school_key") != school
            or verification.get("merge_sha") != merge_sha
            or verification.get("merged") is not True
            or verification.get("production_proof") is not True
            or verification.get("checkpoint_sha256") != sha256(checkpoint_raw)
            or verification.get("pr_number") != checkpoint.get("pr_number")
            or verification.get("pr_head_sha") != checkpoint.get("pr_head_sha")
            or verification.get("production_deployment_id")
            != checkpoint.get("production_deployment_id")
        ):
            continue
        ancestry_after_base = subprocess.run(
            ["git", "-C", str(repo), "merge-base", "--is-ancestor",
             research_base_sha, merge_sha],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        ).returncode == 0
        ancestry_to_main = subprocess.run(
            ["git", "-C", str(repo), "merge-base", "--is-ancestor",
             merge_sha, main_sha],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        ).returncode == 0
        if not ancestry_after_base or not ancestry_to_main:
            continue
        parent_line = _git_lines(repo, "rev-list", "--parents", "-n", "1", merge_sha)
        if len(parent_line) != 1:
            continue
        parents = parent_line[0].split()
        if len(parents) != 3:
            continue
        parent_main, parent_target = parents[1], parents[2]
        if (
            checkpoint.get("merge_parent_main") != parent_main
            or checkpoint.get("merge_parent_onboarding") != parent_target
            or target_sha != parent_target
            or checkpoint.get("pr_head_sha") != parent_target
        ):
            continue
        changed_paths = set(
            _git_lines(
                repo, "diff", "--name-only", parent_main, merge_sha,
                "--", f"schools/{school}",
            )
        )
        if member_path not in changed_paths:
            continue
        try:
            corrected_raw = git_bytes(repo, merge_sha, member_path)
        except Stage1Stop:
            continue
        if corrected_raw != current_raw:
            continue
        matches.append({
            "member": member,
            "path": member_path,
            "control_authority_sha": control_sha,
            "request_id": request_id,
            "merge_sha": merge_sha,
            "merge_parent_main": parent_main,
            "merge_parent_correction": parent_target,
            "target_branch": request["target_branch"],
            "pr_number": checkpoint.get("pr_number"),
            "production_deployment_id": checkpoint.get("production_deployment_id"),
            "checkpoint_sha256": sha256(checkpoint_raw),
            "verification_sha256": sha256(verification_raw),
            "member_sha256": sha256(corrected_raw),
        })
    return matches


def _season_sort_key(value: str) -> tuple[int, str]:
    text = str(value or "").strip()
    try:
        return int(text[:4]), text
    except (TypeError, ValueError):
        return (999999, text)


def _rebase_new_opponent_support(
    support_rows: list[dict[str, str]],
    current_rows: list[dict[str, str]],
    fields: list[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Convert a frozen NEW support row to a narrow extension when current main already
    contains the same accepted opponent identity because a resolved external correction
    landed after the immutable Research base.
    """
    by_identity: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in current_rows:
        by_identity[(
            row.get("source_opponent_label", "").strip(),
            row.get("canonical_opponent_key", "").strip(),
        )].append(row)

    transformed: list[dict[str, str]] = []
    provenance: list[dict[str, str]] = []
    for item in support_rows:
        identity = (
            item.get("source_opponent_label", "").strip(),
            item.get("canonical_opponent_key", "").strip(),
        )
        matches = by_identity.get(identity, [])
        if item.get("support_action", "").strip() != "NEW_SUPPLEMENTAL" or not matches:
            transformed.append(dict(item))
            continue
        if len(matches) != 1:
            raise Stage1Stop(
                "current-main correction rebase opponent identity is not unique: "
                + "|".join(identity)
            )
        current = matches[0]
        candidate = json.loads(item["candidate_row_json"])
        if not isinstance(candidate, dict) or set(candidate) != set(fields):
            raise Stage1Stop(
                "current-main correction rebase candidate opponent schema mismatch"
            )
        for field in OPPONENT_REBASE_CORE_FIELDS:
            if candidate.get(field, "") != current.get(field, ""):
                raise Stage1Stop(
                    "current-main correction rebase opponent core conflict: "
                    f"{identity!r}:{field}"
                )

        merged = dict(current)
        for field in ("games_with_source_label",):
            try:
                merged[field] = str(
                    int(current.get(field, "").strip())
                    + int(candidate.get(field, "").strip())
                )
            except ValueError as exc:
                raise Stage1Stop(
                    "current-main correction rebase opponent game count is not numeric"
                ) from exc
        for field, fn in (("first_season", min), ("last_season", max)):
            values = [
                value
                for value in (
                    current.get(field, "").strip(),
                    candidate.get(field, "").strip(),
                )
                if value
            ]
            if values:
                merged[field] = fn(values, key=_season_sort_key)
        candidate_note = candidate.get("audit_note", "").strip()
        current_note = current.get("audit_note", "").strip()
        if candidate_note and candidate_note not in current_note:
            merged["audit_note"] = (
                current_note + (" | " if current_note else "")
                + "Expansion supplement: " + candidate_note
            )

        changed = [field for field in fields if current.get(field, "") != merged.get(field, "")]
        if not changed or set(changed) - set(OPPONENT_EXTENSION_FIELDS):
            raise Stage1Stop(
                "current-main correction rebase produced unsupported opponent extension"
            )
        rewritten = dict(item)
        rewritten["support_action"] = "EXTEND_INHERITED"
        rewritten["baseline_row_sha256"] = canonical_row_sha256(current)
        rewritten["changed_fields"] = ";".join(changed)
        rewritten["candidate_row_json"] = json.dumps(
            merged, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        transformed.append(rewritten)
        provenance.append({
            "support_id": item.get("support_id", "").strip(),
            "original_action": "NEW_SUPPLEMENTAL",
            "operational_action": "EXTEND_INHERITED",
            "identity": "|".join(identity),
        })
    return transformed, provenance


def prepare_current_main_identity_rebase(
    repo: Path,
    school: str,
    main_sha: str,
    baseline: dict[str, Any],
    validated: dict[str, Any],
    *,
    research_base_sha: str = "",
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    """Preserve one narrowly authenticated class of accepted post-freeze correction.

    Expansion Research stays immutable. When current protected main differs from the
    Research-base package only by an identity-only correction explicitly preserved in
    the frozen NO_EXPANSION_IMPACT / RESOLVED_EXTERNALLY provenance, materialization
    may inherit that already-live representation instead of replaying the stale baseline.
    """
    current_bytes = {
        name: git_bytes(repo, main_sha, f"schools/{school}/{name}")
        for name in PACKAGE_FILES
    }
    changed_members = [
        name for name in PACKAGE_FILES
        if current_bytes[name] != baseline["package_bytes"][name]
    ]
    metadata: dict[str, Any] = {
        "status": "NOT_REQUIRED",
        "changed_members": changed_members,
        "changed_source_game_ids": [],
        "accepted_canonical_game_ids": [],
        "support_action_rebases": [],
        "resolved_external_source_game_ids": sorted(
            _resolved_external_correction_source_ids(validated)
        ),
        "current_package_member_sha256": {
            name: sha256(current_bytes[name]) for name in PACKAGE_FILES
        },
    }
    if not changed_members:
        return baseline, validated, metadata, []

    blockers: list[dict[str, Any]] = []
    allowed_members = {"source-games.csv", "opponents.csv"}
    unsupported_members = sorted(set(changed_members) - allowed_members)
    package_authorities: list[dict[str, Any]] = []
    for name in unsupported_members:
        matches = _completed_post_freeze_package_correction_authorities(
            repo,
            school,
            research_base_sha,
            main_sha,
            name,
            current_bytes[name],
        )
        if len(matches) != 1:
            blockers.append({
                "class": "CURRENT_MAIN_INHERITED_PACKAGE_DRIFT",
                "path": f"schools/{school}/{name}",
                "reason": (
                    "NO_COMPLETED_POST_FREEZE_PACKAGE_CORRECTION_AUTHORITY"
                    if not matches
                    else "AMBIGUOUS_POST_FREEZE_PACKAGE_CORRECTION_AUTHORITY"
                ),
                "matching_authority_count": len(matches),
            })
            continue
        package_authorities.append(matches[0])
    if blockers:
        return baseline, validated, metadata, blockers

    package_rebased_baseline = dict(baseline)
    package_rebased_bytes = dict(baseline["package_bytes"])
    for authority in package_authorities:
        package_rebased_bytes[authority["member"]] = current_bytes[authority["member"]]
    package_rebased_baseline["package_bytes"] = package_rebased_bytes
    metadata["completed_package_corrections"] = package_authorities
    metadata["accepted_package_members"] = sorted(
        authority["member"] for authority in package_authorities
    )
    control_authorities = sorted({
        authority["control_authority_sha"] for authority in package_authorities
    })
    metadata["control_authority_sha"] = (
        control_authorities[0] if len(control_authorities) == 1 else ""
    )

    identity_members_changed = bool(set(changed_members) & allowed_members)
    if not identity_members_changed:
        if package_authorities:
            metadata["status"] = "APPLIED_RESOLVED_EXTERNAL_PACKAGE_CORRECTION"
        return package_rebased_baseline, validated, metadata, []

    allowed_source_ids = set(metadata["resolved_external_source_game_ids"])
    if not allowed_source_ids:
        blockers.append({
            "class": "CURRENT_MAIN_INHERITED_PACKAGE_DRIFT",
            "path": f"schools/{school}/source-games.csv",
            "reason": "NO_RESOLVED_EXTERNAL_CORRECTION_AUTHORITY",
        })
        return baseline, validated, metadata, blockers

    current_source_fields, current_sources = csv_rows(
        current_bytes["source-games.csv"], "current-main inherited source-games.csv"
    )
    current_opponent_fields, current_opponents = csv_rows(
        current_bytes["opponents.csv"], "current-main inherited opponents.csv"
    )
    if current_source_fields != baseline["source_fields"]:
        blockers.append({
            "class": "CURRENT_MAIN_INHERITED_PACKAGE_DRIFT",
            "path": f"schools/{school}/source-games.csv",
            "reason": "SOURCE_SCHEMA_DRIFT",
        })
        return baseline, validated, metadata, blockers
    if current_opponent_fields != baseline["opponent_fields"]:
        blockers.append({
            "class": "CURRENT_MAIN_INHERITED_PACKAGE_DRIFT",
            "path": f"schools/{school}/opponents.csv",
            "reason": "OPPONENT_SCHEMA_DRIFT",
        })
        return baseline, validated, metadata, blockers

    base_ids = [row.get("source_game_id", "").strip() for row in baseline["source_rows"]]
    current_ids = [row.get("source_game_id", "").strip() for row in current_sources]
    if current_ids != base_ids:
        blockers.append({
            "class": "CURRENT_MAIN_INHERITED_PACKAGE_DRIFT",
            "path": f"schools/{school}/source-games.csv",
            "reason": "SOURCE_ID_POPULATION_OR_ORDER_DRIFT",
        })
        return baseline, validated, metadata, blockers

    changed_source_ids: list[str] = []
    allowed_old_opponents: set[tuple[str, str]] = set()
    allowed_new_opponents: set[tuple[str, str]] = set()
    for original, current in zip(baseline["source_rows"], current_sources):
        if original == current:
            continue
        source_id = original.get("source_game_id", "").strip()
        changed_source_ids.append(source_id)
        changed_fields = {
            field for field in current_source_fields
            if original.get(field, "") != current.get(field, "")
        }
        if source_id not in allowed_source_ids or (
            changed_fields - IDENTITY_REBASE_SOURCE_FIELDS
        ):
            blockers.append({
                "class": "CURRENT_MAIN_INHERITED_PACKAGE_DRIFT",
                "path": f"schools/{school}/source-games.csv",
                "source_game_id": source_id,
                "reason": "UNAUTHORIZED_OR_NON_IDENTITY_SOURCE_DRIFT",
                "changed_fields": sorted(changed_fields),
            })
            continue
        label = original.get("source_opponent_label", "").strip()
        allowed_old_opponents.add(
            (label, original.get("normalized_opponent_key", "").strip())
        )
        allowed_new_opponents.add(
            (label, current.get("normalized_opponent_key", "").strip())
        )

    if blockers:
        return baseline, validated, metadata, blockers
    if not changed_source_ids:
        blockers.append({
            "class": "CURRENT_MAIN_INHERITED_PACKAGE_DRIFT",
            "path": f"schools/{school}/opponents.csv",
            "reason": "OPPONENT_DRIFT_WITHOUT_SOURCE_IDENTITY_DRIFT",
        })
        return baseline, validated, metadata, blockers

    def by_identity(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
        result: dict[tuple[str, str], dict[str, str]] = {}
        for row in rows:
            identity = (
                row.get("source_opponent_label", "").strip(),
                row.get("canonical_opponent_key", "").strip(),
            )
            if identity in result:
                raise Stage1Stop(
                    "current-main correction rebase opponent identity is duplicated"
                )
            result[identity] = row
        return result

    base_opponents = by_identity(baseline["opponent_rows"])
    current_opponents_by_identity = by_identity(current_opponents)
    changed_opponent_identities = sorted(
        identity
        for identity in set(base_opponents) | set(current_opponents_by_identity)
        if base_opponents.get(identity) != current_opponents_by_identity.get(identity)
    )
    allowed_opponent_identities = allowed_old_opponents | allowed_new_opponents
    unexpected_opponent_identities = [
        identity for identity in changed_opponent_identities
        if identity not in allowed_opponent_identities
    ]
    if unexpected_opponent_identities:
        blockers.append({
            "class": "CURRENT_MAIN_INHERITED_PACKAGE_DRIFT",
            "path": f"schools/{school}/opponents.csv",
            "reason": "UNRELATED_OPPONENT_DRIFT",
            "identities": ["|".join(value) for value in unexpected_opponent_identities],
        })
        return baseline, validated, metadata, blockers

    try:
        opponent_support, support_rebases = _rebase_new_opponent_support(
            validated["opponent_support_rows"],
            current_opponents,
            current_opponent_fields,
        )
    except (Stage1Stop, ValueError, TypeError, KeyError) as exc:
        blockers.append({
            "class": "CURRENT_MAIN_INHERITED_PACKAGE_DRIFT",
            "path": f"schools/{school}/opponents.csv",
            "reason": "SUPPLEMENTAL_SUPPORT_REBASE_CONFLICT",
            "detail": str(exc),
        })
        return baseline, validated, metadata, blockers

    rebased_baseline = dict(package_rebased_baseline)
    rebased_baseline.update({
        "package_bytes": current_bytes,
        "source_fields": current_source_fields,
        "source_rows": current_sources,
        "source_ids": current_ids,
        "source_game_count": len(current_sources),
        "opponent_fields": current_opponent_fields,
        "opponent_rows": current_opponents,
    })
    rebased_validated = dict(validated)
    rebased_validated["opponent_support_rows"] = opponent_support
    metadata.update({
        "status": (
            "APPLIED_RESOLVED_EXTERNAL_PACKAGE_AND_IDENTITY_CORRECTIONS"
            if package_authorities
            else "APPLIED_RESOLVED_EXTERNAL_IDENTITY_CORRECTION"
        ),
        "changed_source_game_ids": sorted(changed_source_ids),
        "changed_opponent_identities": [
            "|".join(value) for value in changed_opponent_identities
        ],
        "support_action_rebases": support_rebases,
    })
    return rebased_baseline, rebased_validated, metadata, []



def _frozen_reciprocal_source_assertion_match(
    repo: Path,
    research_base: str,
    school: str,
    source: dict[str, str],
    candidates: list[dict[str, str]],
    reciprocal_cache: dict[str, list[dict[str, str]]],
) -> tuple[str, str]:
    """Resolve one frozen reciprocal source assertion without trusting free text."""
    program = source.get("identity_match_program_key", "").strip()
    source_id = source.get("identity_match_source_game_id", "").strip()
    basis = source.get("identity_override_basis", "").strip()
    opponent = source.get("normalized_opponent_key", "").strip()
    if not program or not source_id or not basis:
        return "", "SOURCE_ASSERTION_BINDING_INCOMPLETE"
    if program != opponent:
        return "", "SOURCE_ASSERTION_PROGRAM_MISMATCH"

    if program not in reciprocal_cache:
        try:
            _, rows = csv_rows(
                git_bytes(repo, research_base, f"schools/{program}/source-games.csv"),
                f"research-base reciprocal source-games.csv for {program}",
            )
        except Stage1Stop:
            return "", "SOURCE_ASSERTION_RECIPROCAL_SOURCE_UNAVAILABLE"
        reciprocal_cache[program] = rows

    matches = [
        row for row in reciprocal_cache[program]
        if row.get("source_game_id", "").strip() == source_id
    ]
    if len(matches) != 1:
        return "", "SOURCE_ASSERTION_RECIPROCAL_SOURCE_NOT_UNIQUE"
    reciprocal = matches[0]
    if (
        reciprocal.get("source_program_key", "").strip() != program
        or reciprocal.get("normalized_opponent_key", "").strip() != school
    ):
        return "", "SOURCE_ASSERTION_RECIPROCAL_PAIR_MISMATCH"
    if reciprocal.get("season_label", "").strip() != source.get("season_label", "").strip():
        return "", "SOURCE_ASSERTION_RECIPROCAL_SEASON_MISMATCH"

    source_result = source.get("played_result", "").strip().upper()
    reciprocal_result = reciprocal.get("played_result", "").strip().upper()
    opposite = {"W": "L", "L": "W", "T": "T"}
    if source_result in opposite and reciprocal_result in opposite:
        if opposite[source_result] != reciprocal_result:
            return "", "SOURCE_ASSERTION_RECIPROCAL_RESULT_MISMATCH"

    source_type = source.get("curated_game_type", "").strip()
    reciprocal_type = reciprocal.get("curated_game_type", "").strip()
    if source_type and reciprocal_type and source_type != reciprocal_type:
        return "", "SOURCE_ASSERTION_RECIPROCAL_GAME_TYPE_MISMATCH"

    status, match, method = identify_game(reciprocal, candidates)
    if status != CONFIDENT or not match:
        return "", "SOURCE_ASSERTION_RECIPROCAL_NOT_CONFIDENT"
    return match, "FROZEN_RECIPROCAL_SOURCE_ASSERTION_" + method



def _expansion_known_source_home(source: dict[str, str]) -> str:
    """Use only explicitly researched H/A; neither city nor venue name implies home."""
    site = source.get("curated_site_type", "").strip()
    if site == "SOURCE_PROGRAM_HOME":
        return source.get("source_program_key", "").strip()
    if site == "OPPONENT_HOME":
        return source.get("normalized_opponent_key", "").strip()
    return ""


def _expansion_known_canonical_home(candidate: dict[str, str]) -> str:
    """Require a consistent, explicitly designated canonical home team."""
    site = candidate.get("site_type", "").strip()
    team_field = {
        "TEAM_A_HOME": "team_a_key",
        "TEAM_B_HOME": "team_b_key",
    }.get(site)
    if not team_field:
        return ""
    derived = candidate.get(team_field, "").strip()
    designated = candidate.get("designated_home_team_key", "").strip()
    if designated and designated != derived:
        return ""
    return derived


def _expansion_exact_day_gap(left: str, right: str) -> int | None:
    if not left or not right:
        return None
    try:
        return abs((date.fromisoformat(left) - date.fromisoformat(right)).days)
    except ValueError:
        return None


def _expansion_numeric_scores(
    source: dict[str, str], candidate: dict[str, str]
) -> tuple[int, int, int, int] | None:
    sa, sb = source_scores_in_canonical_orientation(source)
    ca = candidate.get("team_a_score", "").strip()
    cb = candidate.get("team_b_score", "").strip()
    if not all(x.isdigit() for x in (sa, sb, ca, cb)):
        return None
    return int(sa), int(sb), int(ca), int(cb)


def _expansion_safe_identity_tiebreak(
    source: dict[str, str],
    candidates: list[dict[str, str]],
    status: str, match: str, method: str,
) -> tuple[str, str, str]:
    """Resolve only documented, independently distinguishable Stage 1 topologies.

    Identity is distinct from score/date authority. Any conflicting evidence stays
    unchanged and visible to later Gate 1 reconciliation. No guessed venue,
    score, date, canonical ID or unbound identity assertion is authored here.
    """
    src_date = source.get("game_date", "").strip()
    src_home = _expansion_known_source_home(source)

    # When a conflicting exact-date row matches a DIFFERENT candidate's full
    # score on an adjacent day, prefer the full-score identity. The generic
    # ingestion matcher already accepts this narrowly bounded topology.
    if status == CONFIDENT and match and src_date:
        current = next((c for c in candidates
                        if c["canonical_game_id"] == match), None)
        if current is not None and not scores_match(source, current):
            score_matches = [c for c in candidates if scores_match(source, c)]
            if (len(score_matches) == 1
                    and score_matches[0]["canonical_game_id"] != match
                    and (_expansion_exact_day_gap(
                        src_date, score_matches[0].get("game_date", "").strip()
                    ) is not None)
                    and _expansion_exact_day_gap(
                        src_date, score_matches[0].get("game_date", "").strip()
                    ) <= 1):
                return (CONFIDENT, score_matches[0]["canonical_game_id"],
                        "UNIQUE_PAIR_SEASON_SCORE_OVERRIDES_CONFLICTING_EXACT_DATE")

    if status != REVIEW or not src_home or not candidates:
        return status, match, method

    # A single reciprocal game can be identified by an independently agreed
    # home side, result direction, and one exact team score, while the other
    # published score disagrees. Do not silently resolve that score conflict.
    partial: list[dict[str, str]] = []
    for candidate in candidates:
        if _expansion_known_canonical_home(candidate) != src_home:
            continue
        can_date = candidate.get("game_date", "").strip()
        if src_date and can_date and src_date != can_date:
            continue
        scores = _expansion_numeric_scores(source, candidate)
        if scores is None:
            continue
        sa, sb, ca, cb = scores
        if ((sa == ca) != (sb == cb)
                and (sa > sb) - (sa < sb) == (ca > cb) - (ca < cb)):
            partial.append(candidate)
    if len(partial) == 1:
        return (CONFIDENT, partial[0]["canonical_game_id"],
                "UNIQUE_PAIR_SEASON_PARTIAL_SCORE_AND_HOME")

    # Clearly separate trips can be provisionally NEW despite earlier same-
    # season meetings. Require every published candidate to have a known exact
    # date at least seven days away, a different explicit home side and no
    # shared team score. Any missing/ambiguous evidence remains REVIEW.
    if src_date and all(
        _expansion_known_canonical_home(c)
        and _expansion_known_canonical_home(c) != src_home
        and (gap := _expansion_exact_day_gap(
            src_date, c.get("game_date", "").strip()
        )) is not None and gap >= 7
        and (sc := _expansion_numeric_scores(source, c)) is not None
        and sc[0] != sc[2] and sc[1] != sc[3]
        for c in candidates
    ):
        return NEW_GAME, "", "DISTINCT_EXACT_DATES_HOME_SIDES_AND_SCORES"
    return status, match, method


def reconcile_canonical(
    school: str,
    supplemental: list[dict[str, str]],
    canonical: list[dict[str, str]],
    *,
    repo: Path | None = None,
    research_base: str = "",
) -> dict[str, Any]:
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
    reciprocal_cache: dict[str, list[dict[str, str]]] = {}
    counts = Counter()
    for src in supplemental:
        sid = src["source_game_id"].strip()
        pair = ordered_pair(school, src["normalized_opponent_key"])
        candidates = index.get((src["season_label"], pair), [])
        status, match, method = identify_game(src, candidates)
        if src.get("identity_override", "").strip() != "MATCH_SOURCE_ASSERTION":
            status, match, method = _expansion_safe_identity_tiebreak(
                src, candidates, status, match, method,
            )
        if src.get("identity_override", "").strip() == "MATCH_SOURCE_ASSERTION":
            if repo is None or not research_base:
                status, method = REVIEW, "SOURCE_ASSERTION_AUTHORITY_UNAVAILABLE"
            else:
                asserted_match, asserted_method = _frozen_reciprocal_source_assertion_match(
                    repo, research_base, school, src, candidates, reciprocal_cache,
                )
                if not asserted_match:
                    status, match, method = REVIEW, "", asserted_method
                elif status == CONFIDENT and match != asserted_match:
                    status, match, method = (
                        REVIEW, "", "SOURCE_ASSERTION_GENERIC_MATCH_CONFLICT"
                    )
                else:
                    status, match, method = CONFIDENT, asserted_match, asserted_method
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

    # Two distinct games in one verified frozen season ledger may face only one
    # previously published canonical game.  If one frozen row has independently
    # claimed that canonical game by its FULL exact score, the other frozen row
    # cannot be forced onto the already-claimed game merely because the pair and
    # season match.  This is an identity-only proof: it never alters or chooses
    # between dates, sites, scores, or the source's opponent assertion.
    #
    # Require exactly two rows for the pair/season, one uniquely confident
    # canonical claim, and disjoint complete score pairs.  Any competing
    # candidate, unbound identity override, repeated exact date, missing score,
    # partial-score overlap, or conflicting canonical claim remains a REVIEW.
    grouped_frozen: dict[
        tuple[str, tuple[str, str]], list[tuple[dict[str, str], dict[str, Any]]]
    ] = defaultdict(list)
    for src, item in zip(supplemental, rows):
        grouped_frozen[
            (src["season_label"], ordered_pair(school, src["normalized_opponent_key"]))
        ].append((src, item))
    canonical_by_id = {c["canonical_game_id"]: c for c in canonical}
    for pair_rows in grouped_frozen.values():
        if len(pair_rows) != 2:
            continue
        reused = [(s, r) for s, r in pair_rows if r["classification"] == "REUSE_CANONICAL"]
        reviewing = [(s, r) for s, r in pair_rows if r["classification"] == "IDENTITY_REVIEW_BLOCKER"]
        if len(reused) != 1 or len(reviewing) != 1:
            continue
        matched_src, matched = reused[0]
        other_src, other = reviewing[0]
        cid = matched["canonical_game_id"]
        candidate = canonical_by_id.get(cid)
        if (
            candidate is None
            or other["candidate_canonical_game_id"] != cid
            or other["match_method"] != "UNIQUE_PAIR_SEASON_ONLY"
            or other["same_pair_season_candidate_count"] != 1
            or len(reuse_by_id[cid]) != 1
            or matched_src.get("identity_override", "").strip()
            or other_src.get("identity_override", "").strip()
        ):
            continue
        matched_scores = (
            matched_src.get("team_score", "").strip(),
            matched_src.get("opponent_score", "").strip(),
        )
        other_scores = (
            other_src.get("team_score", "").strip(),
            other_src.get("opponent_score", "").strip(),
        )
        if not all(value.isdigit() for value in (*matched_scores, *other_scores)):
            continue
        if (
            int(matched_scores[0]) == int(other_scores[0])
            or int(matched_scores[1]) == int(other_scores[1])
        ):
            continue
        matched_date = matched_src.get("game_date", "").strip()
        other_date = other_src.get("game_date", "").strip()
        if matched_date and matched_date == other_date:
            continue
        if not scores_match(matched_src, candidate) or scores_match(other_src, candidate):
            continue

        other["classification"] = "PROVISIONAL_NEW_CANONICAL"
        other["candidate_canonical_game_id"] = ""
        other["match_method"] = "DISTINCT_FROZEN_PEER_FULL_SCORE_CANONICAL_CLAIM"
        counts["IDENTITY_REVIEW_BLOCKER"] -= 1
        counts["PROVISIONAL_NEW_CANONICAL"] += 1

    return {
        "counts": {label: counts[label] for label in (
            "REUSE_CANONICAL", "PROVISIONAL_NEW_CANONICAL", "IDENTITY_REVIEW_BLOCKER")},
        "game_rows": rows,
        "duplicate_canonical_reuse": {k: v for k, v in sorted(reuse_by_id.items()) if len(v) > 1},
        "possible_duplicate_supplemental_rows": [v for v in seen_strong.values() if len(v) > 1],
    }



def reconcile_global_venues(
    support_rows: list[dict[str, str]],
    registered_venues: list[dict[str, str]],
) -> dict[str, Any]:
    """Classify global venue reuse without inventing IDs or changing candidates.

    NEW_SUPPLEMENTAL denotes new *school* support, not a new physical building.
    An already-registered venue_key is reused only when its physical identity
    and any explicitly carried global ID agree. Ambiguity is a blocker.
    """
    by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in registered_venues:
        by_key[row.get("venue_key", "").strip()].append(row)
        if row.get("venue_id", "").strip():
            by_id[row["venue_id"].strip()].append(row)
    rows: list[dict[str, str]] = []
    blockers: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for item in support_rows:
        key = item["venue_key"].strip()
        support_id = item["support_id"].strip()
        candidate = json.loads(item["candidate_row_json"])
        matches = by_key.get(key, [])
        reasons: list[str] = []
        existing_id = ""
        if len(matches) > 1:
            reasons.append("DUPLICATE_GLOBAL_VENUE_KEY")
        elif len(matches) == 1:
            registered = matches[0]
            existing_id = registered.get("venue_id", "").strip()
            candidate_id = candidate.get("venue_id", "").strip()
            if not existing_id:
                reasons.append("REGISTERED_VENUE_ID_MISSING")
            elif candidate_id and candidate_id != existing_id:
                reasons.append("REGISTERED_VENUE_ID_CONFLICT")
            if (candidate.get("canonical_name", "").strip().casefold()
                    != registered.get("display_name", "").strip().casefold()):
                reasons.append("REGISTERED_VENUE_NAME_REVIEW")
            for field in ("city", "state"):
                declared = candidate.get(field, "").strip()
                official = registered.get(field, "").strip()
                if not declared or not official or declared.casefold() != official.casefold():
                    reasons.append("REGISTERED_VENUE_GEOGRAPHY_REVIEW")
                    break
        else:
            candidate_id = candidate.get("venue_id", "").strip()
            if candidate_id:
                reasons.append("UNREGISTERED_VENUE_ID_REFERENCE")
                if by_id.get(candidate_id):
                    reasons.append("GLOBAL_VENUE_ID_USED_BY_DIFFERENT_KEY")
        status = (
            "GLOBAL_VENUE_IDENTITY_REVIEW_BLOCKER" if reasons else
            "REUSE_REGISTERED_GLOBAL_VENUE" if matches else
            "NEW_GLOBAL_VENUE_REGISTRATION_REQUIRED"
        )
        counts[status] += 1
        rows.append({
            "support_id": support_id, "venue_key": key,
            "support_action": item["support_action"],
            "global_reconciliation_class": status,
            "existing_global_venue_id": existing_id,
        })
        for reason in reasons:
            blockers.append({
                "class": reason, "support_id": support_id, "venue_key": key,
                "registered_venue_id": existing_id,
            })
    return {
        "counts": {k: counts[k] for k in (
            "REUSE_REGISTERED_GLOBAL_VENUE",
            "NEW_GLOBAL_VENUE_REGISTRATION_REQUIRED",
            "GLOBAL_VENUE_IDENTITY_REVIEW_BLOCKER",
        )},
        "rows": rows,
        "blockers": blockers,
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
    materialization_baseline, materialized_validated, current_main_reconciliation, rebase_blockers = (
        prepare_current_main_identity_rebase(
            repo,
            school,
            main_sha,
            baseline,
            validated,
            research_base_sha=research_base,
        )
    )
    candidate, census = build_candidate(
        materialization_baseline, payload, materialized_validated
    )
    blockers: list[dict[str, Any]] = list(rebase_blockers)
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
    accepted_enrichment, unresolved_canonical_drift = (
        classify_current_main_canonical_drift(
            base_by_id,
            main_by_id,
            canonical_drift,
        )
    )
    current_main_reconciliation["accepted_canonical_enrichment"] = accepted_enrichment
    if unresolved_canonical_drift:
        if current_main_reconciliation.get("status") == (
            "APPLIED_RESOLVED_EXTERNAL_IDENTITY_CORRECTION"
        ):
            changed_sources = set(
                current_main_reconciliation.get("changed_source_game_ids") or []
            )
            assertions = read_game_assertions_at_git(
                repo, main_sha, read_csv_at_git
            )
            assertion_ids: dict[str, set[str]] = defaultdict(set)
            for row in assertions:
                source_id = row.get("source_game_id", "").strip()
                if (
                    row.get("source_program_key", "").strip() == school
                    and source_id in changed_sources
                    and row.get("canonical_game_id", "").strip()
                ):
                    assertion_ids[source_id].add(
                        row.get("canonical_game_id", "").strip()
                    )
            invalid_bindings = sorted(
                source_id
                for source_id in changed_sources
                if len(assertion_ids.get(source_id, set())) != 1
            )
            allowed_canonical = sorted({
                next(iter(assertion_ids[source_id]))
                for source_id in changed_sources
                if len(assertion_ids.get(source_id, set())) == 1
            })
            unexpected = sorted(
                set(unresolved_canonical_drift) - set(allowed_canonical)
            )
            if invalid_bindings or unexpected:
                blockers.append({
                    "class": "CURRENT_MAIN_INHERITED_CANONICAL_DRIFT",
                    "canonical_game_ids": unresolved_canonical_drift,
                    "reason": "CORRECTION_ASSERTION_BINDING_MISMATCH",
                    "invalid_source_game_ids": invalid_bindings,
                    "unexpected_canonical_game_ids": unexpected,
                    "accepted_nonhistorical_enrichment": accepted_enrichment,
                })
            else:
                current_main_reconciliation["accepted_canonical_game_ids"] = (
                    unresolved_canonical_drift
                )
        else:
            blockers.append({
                "class": "CURRENT_MAIN_INHERITED_CANONICAL_DRIFT",
                "canonical_game_ids": unresolved_canonical_drift,
                "accepted_nonhistorical_enrichment": accepted_enrichment,
            })
    global_venues = read_csv_at_git(repo, main_sha, "data/reference/venues.csv")
    global_venue_reconciliation = reconcile_global_venues(
        validated["venue_support_rows"], global_venues,
    )
    blockers.extend(global_venue_reconciliation["blockers"])
    registered_programs = {r["program_key"] for r in read_csv_at_git(
        repo, main_sha, "data/reference/programs.csv")}
    for item in validated["opponent_support_rows"]:
        proposed = json.loads(item["candidate_row_json"])
        if (item["canonical_opponent_key"] in registered_programs and
                proposed.get("current_d1", "").strip().casefold() not in {"yes", "true", "1"}):
            blockers.append({"class": "REGISTERED_PROGRAM_OPPONENT_CLASSIFICATION_CONFLICT",
                             "support_id": item["support_id"],
                             "opponent_key": item["canonical_opponent_key"]})
    identity = reconcile_canonical(
        school,
        validated["source_rows"],
        main_canonical,
        repo=repo,
        research_base=research_base,
    )
    if identity["counts"]["IDENTITY_REVIEW_BLOCKER"]:
        blockers.append({"class": "AMBIGUOUS_SUPPLEMENTAL_CANONICAL_IDENTITIES", "source_game_ids": [
            r["source_game_id"] for r in identity["game_rows"] if r["classification"] == "IDENTITY_REVIEW_BLOCKER"]})
    if identity["duplicate_canonical_reuse"]:
        blockers.append({"class": "MULTIPLE_SUPPLEMENTAL_SOURCES_REUSE_ONE_CANONICAL", "population": identity["duplicate_canonical_reuse"]})
    if identity["possible_duplicate_supplemental_rows"]:
        blockers.append({"class": "POSSIBLE_DUPLICATE_SUPPLEMENTAL_GAMES", "population": identity["possible_duplicate_supplemental_rows"]})
    # Schema-v2 inherited-unpublished references and accepted scope authority
    # are already fail-closed authenticated by validate_delta_payload(). Stage 1
    # materializes the unchanged inherited package plus genuinely new rows; the
    # later Integration Freeze owns the frozen metadata/scope projection.
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
        "research_freeze_schema_version": manifest["schema_version"],
        "inherited_reused_source_reference_count": len(
            validated.get("inherited_source_references") or []
        ),
        "scope_authority": validated.get("scope_authority"),
        "census": census, "global_venue_reconciliation": global_venue_reconciliation,
        "canonical_identity_census": identity, "blockers": blockers,
        "current_main_reconciliation": current_main_reconciliation,
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
