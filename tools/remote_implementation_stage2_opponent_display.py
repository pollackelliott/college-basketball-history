#!/usr/bin/env python3
"""Narrow remote Stage 2 historical opponent-display normalization orchestration.

This module never chooses opponent identities or display authority. It invokes the
existing permanent normalize_historical_opponent_displays.py helper, proves the
result is representation-only, and authenticates the exact Stage 2 census and
Integration Freeze authority that bounded the repair.
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

from integration_freeze_guard import semantic_drift_report
from remote_implementation_control import sha256_bytes
from remote_implementation_io import (
    ROOT,
    Stop,
    commit_file_hashes,
    git,
    git_show_bytes,
    run,
)
from remote_implementation_stage2_census import (
    STAGE2_ARTIFACT_NAMES,
    add_existing_onboarding_worktree,
    restore_integration_freeze,
    run_stage2_census_tool,
    tracked_worktree_state,
)

DISPLAY_BLOCKER_RE = re.compile(
    r"^historical opponent display conflict: ([a-z0-9][a-z0-9-]*):"
)
ALLOWED_REPAIR_PATH_NAMES = ("opponents.csv", "source-games.csv")


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _csv_from_bytes(data: bytes) -> tuple[list[str], list[dict[str, str]]]:
    text = data.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    return list(reader.fieldnames or []), list(reader)


def _display_blocker_keys(blockers: list[Any]) -> list[str]:
    keys: list[str] = []
    for blocker in blockers:
        match = DISPLAY_BLOCKER_RE.match(str(blocker))
        if not match:
            raise Stop(
                "STAGE2_OPPONENT_DISPLAY_CENSUS_HAS_OTHER_BLOCKER:"
                + str(blocker)
            )
        keys.append(match.group(1))
    if len(keys) != len(set(keys)):
        raise Stop("STAGE2_OPPONENT_DISPLAY_DUPLICATE_BLOCKER_KEY")
    return sorted(keys)


def verify_census_and_freeze_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path = ROOT,
) -> dict[str, Any]:
    """Authenticate the exact Stage 2 census and its Phase 0 freeze provenance."""

    ref = request["stage2_census_checkpoint"]
    manifest_bytes = git_show_bytes(
        control_commit,
        ref["path"],
        cwd=source_repo,
    )
    if sha256_bytes(manifest_bytes) != ref["sha256"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_HASH_MISMATCH")
    manifest = json.loads(manifest_bytes)
    if manifest.get("kind") != "REMOTE_IMPLEMENTATION_STAGE2_CENSUS_CHECKPOINT":
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_KIND_MISMATCH")
    if manifest.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_SCHOOL_MISMATCH")
    if manifest.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_BRANCH_MISMATCH")
    if manifest.get("target_sha") != request["target_sha"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_TARGET_MISMATCH")
    if (
        manifest.get("integration_freeze_sha256")
        != request["integration_freeze_sha256"]
    ):
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_FREEZE_MISMATCH")
    if (
        manifest.get("semantic_snapshot_sha256")
        != request["semantic_snapshot_sha256"]
    ):
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_SEMANTIC_MISMATCH")
    if manifest.get("stage2_status") != "BLOCKED":
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_NOT_BLOCKED")
    if manifest.get("capability_census_status") != "PREFLIGHT_BLOCKED":
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_NOT_PREFLIGHT_BLOCKED")

    preflight = manifest.get("preflight") or {}
    if int(preflight.get("warning_count", -1)) != 0:
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_WARNINGS_PRESENT")
    if int(preflight.get("decision_count", -1)) != 0:
        raise Stop("STAGE2_OPPONENT_DISPLAY_CENSUS_DECISIONS_PRESENT")

    checkpoint_dir = Path(ref["path"]).parent
    status_path = (checkpoint_dir / "implementation-stage2-status.json").as_posix()
    status_bytes = git_show_bytes(control_commit, status_path, cwd=source_repo)
    expected_status_sha = (manifest.get("artifact_sha256") or {}).get(
        "implementation-stage2-status.json"
    )
    if not expected_status_sha or sha256_bytes(status_bytes) != expected_status_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_STATUS_HASH_MISMATCH")
    status = json.loads(status_bytes)
    blockers = list(status.get("blockers") or [])
    blocker_keys = _display_blocker_keys(blockers)
    if len(blocker_keys) != int(preflight.get("blocker_count", -1)):
        raise Stop("STAGE2_OPPONENT_DISPLAY_BLOCKER_COUNT_MISMATCH")
    if not blocker_keys:
        raise Stop("STAGE2_OPPONENT_DISPLAY_EMPTY_BLOCKER_POPULATION")

    phase0_path = str(manifest.get("phase0_successor_path") or "")
    phase0_sha = str(manifest.get("phase0_successor_sha256") or "")
    if not phase0_path or not phase0_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_REFERENCE_MISSING")
    phase0_bytes = git_show_bytes(control_commit, phase0_path, cwd=source_repo)
    if sha256_bytes(phase0_bytes) != phase0_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_SUCCESSOR_HASH_MISMATCH")
    phase0 = json.loads(phase0_bytes)
    if phase0.get("kind") != "REMOTE_IMPLEMENTATION_SUCCESSOR":
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_SUCCESSOR_KIND_MISMATCH")
    if phase0.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_SUCCESSOR_SCHOOL_MISMATCH")
    if phase0.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_SUCCESSOR_BRANCH_MISMATCH")
    if phase0.get("final_transaction_state") != "COMPLETE":
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_NOT_COMPLETE")
    if phase0.get("repository_validation") != "PASS":
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_NOT_VALIDATED")
    if (
        phase0.get("integration_freeze_sha256")
        != request["integration_freeze_sha256"]
    ):
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_FREEZE_MISMATCH")
    if (
        phase0.get("semantic_snapshot_sha256")
        != request["semantic_snapshot_sha256"]
    ):
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_SEMANTIC_MISMATCH")

    writeahead_path = str(phase0.get("writeahead_manifest_path") or "")
    writeahead_sha = str(phase0.get("writeahead_manifest_sha256") or "")
    if not writeahead_path or not writeahead_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_WRITEAHEAD_MISSING")
    writeahead_bytes = git_show_bytes(
        control_commit,
        writeahead_path,
        cwd=source_repo,
    )
    if sha256_bytes(writeahead_bytes) != writeahead_sha:
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_WRITEAHEAD_HASH_MISMATCH")
    writeahead = json.loads(writeahead_bytes)
    if writeahead.get("kind") != "REMOTE_IMPLEMENTATION_WRITEAHEAD":
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_WRITEAHEAD_KIND_MISMATCH")
    if (
        writeahead.get("integration_freeze_sha256")
        != request["integration_freeze_sha256"]
    ):
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_WRITEAHEAD_FREEZE_MISMATCH")
    if (
        writeahead.get("semantic_snapshot_sha256")
        != request["semantic_snapshot_sha256"]
    ):
        raise Stop("STAGE2_OPPONENT_DISPLAY_PHASE0_WRITEAHEAD_SEMANTIC_MISMATCH")

    freeze_path = (
        Path(writeahead_path).parent / "integration-freeze.json"
    ).as_posix()
    freeze_bytes = git_show_bytes(control_commit, freeze_path, cwd=source_repo)
    sidecar_sha = (writeahead.get("sidecars") or {}).get(
        "integration-freeze.json"
    )
    if sidecar_sha != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FREEZE_SIDECAR_MISMATCH")
    if sha256_bytes(freeze_bytes) != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FREEZE_BYTES_MISMATCH")
    freeze = json.loads(freeze_bytes)
    if freeze.get("status") != "INTEGRATION_FROZEN":
        raise Stop("STAGE2_OPPONENT_DISPLAY_FREEZE_STATUS_MISMATCH")
    if freeze.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FREEZE_SCHOOL_MISMATCH")
    snapshot = (freeze.get("source_game_semantic_guard") or {}).get(
        "snapshot_sha256"
    )
    if snapshot != request["semantic_snapshot_sha256"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_FREEZE_SEMANTIC_MISMATCH")

    return {
        "census_manifest": manifest,
        "census_manifest_bytes": manifest_bytes,
        "status": status,
        "status_bytes": status_bytes,
        "blocker_keys": blocker_keys,
        "phase0_successor": phase0,
        "phase0_successor_bytes": phase0_bytes,
        "phase0_writeahead": writeahead,
        "freeze_bytes": freeze_bytes,
        "freeze_path": freeze_path,
    }


def _require_semantic_pass(repo: Path, school_key: str, label: str) -> dict[str, Any]:
    report = semantic_drift_report(repo, school_key)
    if report.get("status") != "PASS" or report.get("changes"):
        raise Stop(
            "STAGE2_OPPONENT_DISPLAY_SEMANTIC_DRIFT_%s" % label.upper()
        )
    return report


def run_normalizer_dry_run(
    repo: Path,
    school_key: str,
    freeze_bytes: bytes,
    expected_blocker_keys: list[str],
    diag: Path,
) -> dict[str, Any]:
    restore_integration_freeze(repo, school_key, freeze_bytes)
    drift = _require_semantic_pass(repo, school_key, "before")
    before = tracked_worktree_state(repo)
    if before["status"]:
        raise Stop("STAGE2_OPPONENT_DISPLAY_DIRTY_BEFORE_DRY_RUN")

    diag.mkdir(parents=True, exist_ok=True)
    report_path = diag / "opponent-display-normalization-dry-run.json"
    if report_path.exists():
        report_path.unlink()
    cmd = [
        sys.executable,
        str(repo / "tools/normalize_historical_opponent_displays.py"),
        school_key,
        "--repo",
        str(repo),
        "--sync-source-games",
        "--json-output",
        str(report_path),
    ]
    cp = run(cmd, cwd=repo, check=False)
    (diag / "opponent-display-normalization-dry-run.log").write_text(
        cp.stdout,
        encoding="utf-8",
    )
    if cp.returncode != 0:
        raise Stop(
            "PERMANENT_OPPONENT_DISPLAY_DRY_RUN_FAILED\n" + cp.stdout[-10000:]
        )
    if not report_path.is_file():
        raise Stop("OPPONENT_DISPLAY_DRY_RUN_REPORT_MISSING")
    report_bytes = report_path.read_bytes()
    report = json.loads(report_bytes)
    if report.get("status") != "PASS":
        raise Stop("OPPONENT_DISPLAY_DRY_RUN_NOT_PASS")
    if int(report.get("ambiguous_key_count", -1)) != 0:
        raise Stop("OPPONENT_DISPLAY_DRY_RUN_AMBIGUOUS")
    proposed = sorted(
        str(item.get("canonical_opponent_key") or "")
        for item in report.get("changes") or []
    )
    expected = sorted(expected_blocker_keys)
    if proposed != expected:
        raise Stop(
            "OPPONENT_DISPLAY_DRY_RUN_KEY_POPULATION_MISMATCH "
            "expected=%s proposed=%s" % (expected, proposed)
        )
    if int(report.get("change_key_count", -1)) != len(expected):
        raise Stop("OPPONENT_DISPLAY_DRY_RUN_KEY_COUNT_MISMATCH")

    after = tracked_worktree_state(repo)
    if after != before:
        raise Stop("OPPONENT_DISPLAY_DRY_RUN_TRACKED_MUTATION")
    return {
        "command": [
            "python",
            "tools/normalize_historical_opponent_displays.py",
            school_key,
            "--sync-source-games",
            "--json-output",
            "<DIAG>/opponent-display-normalization-dry-run.json",
        ],
        "report": report,
        "report_bytes": report_bytes,
        "report_sha256": sha256_bytes(report_bytes),
        "semantic_drift_before": drift,
        "tracked_state_before": before,
        "tracked_state_after": after,
    }


def field_level_mutation_proof(
    *,
    school_key: str,
    before_opponents: bytes,
    after_opponents: bytes,
    before_source_games: bytes,
    after_source_games: bytes,
    expected_blocker_keys: list[str],
) -> dict[str, Any]:
    opp_fields_before, opp_before = _csv_from_bytes(before_opponents)
    opp_fields_after, opp_after = _csv_from_bytes(after_opponents)
    if opp_fields_before != opp_fields_after or len(opp_before) != len(opp_after):
        raise Stop("OPPONENT_DISPLAY_OPPONENT_TABLE_SHAPE_CHANGED")
    if "canonical_opponent_key" not in opp_fields_before:
        raise Stop("OPPONENT_DISPLAY_OPPONENT_KEY_COLUMN_MISSING")
    opponent_changed_rows = 0
    opponent_changed_keys: set[str] = set()
    for index, (before, after) in enumerate(zip(opp_before, opp_after), start=2):
        for field in opp_fields_before:
            if before.get(field, "") == after.get(field, ""):
                continue
            if field != "canonical_opponent_name":
                raise Stop(
                    "OPPONENT_DISPLAY_OPPONENT_FIELD_CHANGED line=%s field=%s"
                    % (index, field)
                )
        if before != after:
            if (
                before.get("canonical_opponent_key", "")
                != after.get("canonical_opponent_key", "")
            ):
                raise Stop("OPPONENT_DISPLAY_OPPONENT_KEY_CHANGED")
            opponent_changed_rows += 1
            opponent_changed_keys.add(
                before.get("canonical_opponent_key", "").strip()
            )

    src_fields_before, src_before = _csv_from_bytes(before_source_games)
    src_fields_after, src_after = _csv_from_bytes(after_source_games)
    if src_fields_before != src_fields_after or len(src_before) != len(src_after):
        raise Stop("OPPONENT_DISPLAY_SOURCE_GAME_TABLE_SHAPE_CHANGED")
    for required in ("source_game_id", "normalized_opponent_key", "normalized_opponent_name"):
        if required not in src_fields_before:
            raise Stop("OPPONENT_DISPLAY_SOURCE_GAME_COLUMN_MISSING:%s" % required)
    source_changed_rows = 0
    source_changed_keys: set[str] = set()
    source_changed_ids: list[str] = []
    for index, (before, after) in enumerate(zip(src_before, src_after), start=2):
        for field in src_fields_before:
            if before.get(field, "") == after.get(field, ""):
                continue
            if field != "normalized_opponent_name":
                raise Stop(
                    "OPPONENT_DISPLAY_SOURCE_FIELD_CHANGED line=%s field=%s"
                    % (index, field)
                )
        if before != after:
            if (
                before.get("normalized_opponent_key", "")
                != after.get("normalized_opponent_key", "")
            ):
                raise Stop("OPPONENT_DISPLAY_SOURCE_OPPONENT_KEY_CHANGED")
            source_changed_rows += 1
            source_changed_keys.add(
                before.get("normalized_opponent_key", "").strip()
            )
            source_changed_ids.append(before.get("source_game_id", ""))

    expected = sorted(expected_blocker_keys)
    if sorted(opponent_changed_keys) != expected:
        raise Stop(
            "OPPONENT_DISPLAY_APPLY_KEY_POPULATION_MISMATCH "
            "expected=%s actual=%s"
            % (expected, sorted(opponent_changed_keys))
        )
    unexpected_source_keys = sorted(source_changed_keys - set(expected))
    if unexpected_source_keys:
        raise Stop(
            "OPPONENT_DISPLAY_SOURCE_GAME_KEY_OUTSIDE_CENSUS:"
            + ",".join(unexpected_source_keys)
        )
    return {
        "schema_version": 1,
        "school_key": school_key,
        "allowed_paths": [
            "schools/%s/opponents.csv" % school_key,
            "schools/%s/source-games.csv" % school_key,
        ],
        "opponent_changed_row_count": opponent_changed_rows,
        "opponent_changed_keys": sorted(opponent_changed_keys),
        "source_game_normalized_name_row_count": source_changed_rows,
        "source_game_changed_keys": sorted(source_changed_keys),
        "source_game_changed_ids": source_changed_ids,
        "opponent_key_changes": 0,
        "source_game_non_name_field_changes": 0,
        "literal_evidence_changes": 0,
    }


def apply_and_prepare_repair(
    repo: Path,
    school_key: str,
    predecessor_sha: str,
    freeze_bytes: bytes,
    dry_run: dict[str, Any],
    expected_blocker_keys: list[str],
    diag: Path,
) -> dict[str, Any]:
    before_state = tracked_worktree_state(repo)
    if before_state["head_sha"] != predecessor_sha or before_state["status"]:
        raise Stop("OPPONENT_DISPLAY_APPLY_PRECONDITION_MISMATCH")
    before_opponents = git_show_bytes(
        predecessor_sha,
        "schools/%s/opponents.csv" % school_key,
        cwd=repo,
    )
    before_source_games = git_show_bytes(
        predecessor_sha,
        "schools/%s/source-games.csv" % school_key,
        cwd=repo,
    )

    cmd = [
        sys.executable,
        str(repo / "tools/normalize_historical_opponent_displays.py"),
        school_key,
        "--repo",
        str(repo),
        "--sync-source-games",
        "--apply",
    ]
    cp = run(cmd, cwd=repo, check=False)
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "opponent-display-normalization-apply.log").write_text(
        cp.stdout,
        encoding="utf-8",
    )
    if cp.returncode != 0:
        raise Stop(
            "PERMANENT_OPPONENT_DISPLAY_APPLY_FAILED\n" + cp.stdout[-10000:]
        )

    allowed_paths = {
        "schools/%s/opponents.csv" % school_key,
        "schools/%s/source-games.csv" % school_key,
    }
    changed_worktree = sorted(
        line[3:].strip()
        for line in git(
            "status",
            "--porcelain",
            "--untracked-files=all",
            cwd=repo,
        ).stdout.splitlines()
        if line.strip()
    )
    if not changed_worktree:
        raise Stop("OPPONENT_DISPLAY_APPLY_NO_TRACKED_CHANGE")
    if set(changed_worktree) - allowed_paths:
        raise Stop(
            "OPPONENT_DISPLAY_APPLY_PATH_OUTSIDE_CONTRACT:"
            + ",".join(sorted(set(changed_worktree) - allowed_paths))
        )

    after_opponents = (repo / "schools" / school_key / "opponents.csv").read_bytes()
    after_source_games = (
        repo / "schools" / school_key / "source-games.csv"
    ).read_bytes()
    proof = field_level_mutation_proof(
        school_key=school_key,
        before_opponents=before_opponents,
        after_opponents=after_opponents,
        before_source_games=before_source_games,
        after_source_games=after_source_games,
        expected_blocker_keys=expected_blocker_keys,
    )
    report = dry_run["report"]
    if proof["opponent_changed_row_count"] != int(report.get("change_row_count", -1)):
        raise Stop("OPPONENT_DISPLAY_APPLY_OPPONENT_ROW_COUNT_MISMATCH")
    if proof["source_game_normalized_name_row_count"] != int(
        report.get("source_game_display_change_rows", -1)
    ):
        raise Stop("OPPONENT_DISPLAY_APPLY_SOURCE_ROW_COUNT_MISMATCH")

    restore_integration_freeze(repo, school_key, freeze_bytes)
    drift_after = _require_semantic_pass(repo, school_key, "after")

    for path in sorted(changed_worktree):
        git("add", path, cwd=repo)
    message = "Normalize %s historical opponent display representation" % school_key
    git("commit", "-m", message, cwd=repo)
    prepared = git("rev-parse", "HEAD", cwd=repo).stdout.strip()
    parent = git("rev-parse", "%s^" % prepared, cwd=repo).stdout.strip()
    tree = git("rev-parse", "%s^{tree}" % prepared, cwd=repo).stdout.strip()
    if parent != predecessor_sha:
        raise Stop("OPPONENT_DISPLAY_PREPARED_PARENT_MISMATCH")
    changed = sorted(
        line.strip()
        for line in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            prepared,
            cwd=repo,
        ).stdout.splitlines()
        if line.strip()
    )
    if set(changed) - allowed_paths or not changed:
        raise Stop("OPPONENT_DISPLAY_PREPARED_PATH_CONTRACT_FAILED")
    changed_hashes = commit_file_hashes(repo, prepared, changed)
    return {
        "apply_command": [
            "python",
            "tools/normalize_historical_opponent_displays.py",
            school_key,
            "--sync-source-games",
            "--apply",
        ],
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": tree,
        "prepared_parent_sha": parent,
        "commit_message": message,
        "changed_paths": changed,
        "changed_file_sha256": changed_hashes,
        "field_level_proof": proof,
        "semantic_drift_after": drift_after,
    }


def verify_prepared_commit_field_boundary(
    repo: Path,
    *,
    school_key: str,
    predecessor_sha: str,
    prepared_sha: str,
    expected_blocker_keys: list[str],
) -> dict[str, Any]:
    return field_level_mutation_proof(
        school_key=school_key,
        before_opponents=git_show_bytes(
            predecessor_sha,
            "schools/%s/opponents.csv" % school_key,
            cwd=repo,
        ),
        after_opponents=git_show_bytes(
            prepared_sha,
            "schools/%s/opponents.csv" % school_key,
            cwd=repo,
        ),
        before_source_games=git_show_bytes(
            predecessor_sha,
            "schools/%s/source-games.csv" % school_key,
            cwd=repo,
        ),
        after_source_games=git_show_bytes(
            prepared_sha,
            "schools/%s/source-games.csv" % school_key,
            cwd=repo,
        ),
        expected_blocker_keys=expected_blocker_keys,
    )


def post_repair_stage2_result(
    repo: Path,
    school_key: str,
    freeze_bytes: bytes,
    diag: Path,
) -> dict[str, Any]:
    return run_stage2_census_tool(
        repo,
        school_key,
        freeze_bytes,
        diag,
    )


def stage2_result_summary(result: dict[str, Any]) -> dict[str, Any]:
    status = result.get("status") or {}
    preflight = status.get("preflight") or {}
    census = result.get("capability_census") or {}
    return {
        "stage2_status": result.get("stage2_status"),
        "command_exit_code": result.get("exit_code"),
        "blocker_count": int(preflight.get("blocker_count", 0) or 0),
        "warning_count": int(preflight.get("warning_count", 0) or 0),
        "decision_count": int(preflight.get("decision_count", 0) or 0),
        "decision_universe_sha256": preflight.get("decision_universe_sha256"),
        "capability_census_status": census.get("status"),
        "capability_topology_groups": census.get("topology_groups", []),
        "artifact_sha256": result.get("artifact_sha256", {}),
        "artifact_normalized_sha256": result.get(
            "artifact_normalized_sha256", {}
        ),
        "tracked_mutation_proof": result.get("tracked_mutation_proof", {}),
    }
