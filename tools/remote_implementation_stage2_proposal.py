#!/usr/bin/env python3
"""Read-only remote orchestration for exact Stage 2 proposal rehearsal.

This module authenticates durable Stage-2 authority and an exact recommendation-map
payload, invokes the unchanged permanent implementation_stage2.py coordinator with
--map against an exact onboarding worktree, and proves that the rehearsal leaves
tracked basketball state untouched. It never parses or interprets recommendation
actions itself.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from remote_implementation_control import sha256_bytes, sha256_file
from remote_implementation_io import ROOT, Stop, git_show_bytes, run
from remote_implementation_stage2_census import (
    STAGE2_ARTIFACT_NAMES,
    STAGE2_CENSUS,
    STAGE2_STATUS,
    RUNTIME_ROOT,
    normalize_artifact_bytes,
    restore_integration_freeze,
    tracked_worktree_state,
)

SITE_DIAGNOSTIC = "last-rehearsal-site-gate.json"
PROPOSAL_ARTIFACT_NAMES = (*STAGE2_ARTIFACT_NAMES, SITE_DIAGNOSTIC)
PROPOSAL_ALLOWED_STATUSES = {"OWNER_GATE_1_READY", "BLOCKED"}


def _bound_json(
    control_commit: str,
    ref: dict[str, Any],
    *,
    source_repo: Path = ROOT,
    mismatch_code: str,
) -> tuple[dict[str, Any], bytes]:
    data = git_show_bytes(control_commit, ref["path"], cwd=source_repo)
    if sha256_bytes(data) != ref["sha256"]:
        raise Stop(mismatch_code)
    try:
        return json.loads(data), data
    except (TypeError, ValueError) as exc:
        raise Stop(mismatch_code + "_JSON_INVALID") from exc


def _freeze_from_writeahead(
    *,
    control_commit: str,
    writeahead_path: str,
    writeahead_sha256: str,
    request: dict[str, Any],
    source_repo: Path,
) -> tuple[bytes, dict[str, Any]]:
    data = git_show_bytes(control_commit, writeahead_path, cwd=source_repo)
    if sha256_bytes(data) != writeahead_sha256:
        raise Stop("STAGE2_PROPOSAL_WRITEAHEAD_HASH_MISMATCH")
    writeahead = json.loads(data)
    if writeahead.get("kind") != "REMOTE_IMPLEMENTATION_WRITEAHEAD":
        raise Stop("STAGE2_PROPOSAL_WRITEAHEAD_KIND_MISMATCH")
    if writeahead.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_PROPOSAL_WRITEAHEAD_SCHOOL_MISMATCH")
    if writeahead.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_PROPOSAL_WRITEAHEAD_BRANCH_MISMATCH")
    if writeahead.get("integration_freeze_sha256") != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_PROPOSAL_WRITEAHEAD_FREEZE_MISMATCH")
    if writeahead.get("semantic_snapshot_sha256") != request["semantic_snapshot_sha256"]:
        raise Stop("STAGE2_PROPOSAL_WRITEAHEAD_SEMANTIC_MISMATCH")

    freeze_path = (Path(writeahead_path).parent / "integration-freeze.json").as_posix()
    freeze_bytes = git_show_bytes(control_commit, freeze_path, cwd=source_repo)
    sidecar_sha = (writeahead.get("sidecars") or {}).get("integration-freeze.json")
    if sidecar_sha != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_PROPOSAL_FREEZE_SIDECAR_MISMATCH")
    if sha256_bytes(freeze_bytes) != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_PROPOSAL_FREEZE_BYTES_MISMATCH")
    freeze = json.loads(freeze_bytes)
    if freeze.get("status") != "INTEGRATION_FROZEN":
        raise Stop("STAGE2_PROPOSAL_FREEZE_STATUS_MISMATCH")
    if freeze.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_PROPOSAL_FREEZE_SCHOOL_MISMATCH")
    semantic = (freeze.get("source_game_semantic_guard") or {}).get("snapshot_sha256")
    if semantic != request["semantic_snapshot_sha256"]:
        raise Stop("STAGE2_PROPOSAL_FREEZE_SEMANTIC_MISMATCH")
    return freeze_bytes, writeahead


def verify_stage2_proposal_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path = ROOT,
) -> dict[str, Any]:
    """Authenticate the exact blocker-free Stage-2 authority bound by the request."""

    authority, authority_bytes = _bound_json(
        control_commit,
        request["stage2_authority"],
        source_repo=source_repo,
        mismatch_code="STAGE2_PROPOSAL_AUTHORITY_HASH_MISMATCH",
    )
    kind = authority.get("kind")
    if kind == "REMOTE_IMPLEMENTATION_STAGE2_CENSUS_CHECKPOINT":
        stage2_status = authority.get("stage2_status")
        blocker_count = int((authority.get("preflight") or {}).get("blocker_count", -1))
        warning_count = int((authority.get("preflight") or {}).get("warning_count", -1))
        decision_sha = authority.get("decision_universe_sha256")
        target_sha = authority.get("target_sha")
        target_tree_sha = authority.get("target_tree_sha")
        integration_freeze_sha = authority.get("integration_freeze_sha256")
        semantic_sha = authority.get("semantic_snapshot_sha256")
        writeahead_path = ""
        writeahead_sha = ""
        phase0_path = str(authority.get("phase0_successor_path") or "")
        phase0_sha = str(authority.get("phase0_successor_sha256") or "")
        if not phase0_path or not phase0_sha:
            raise Stop("STAGE2_PROPOSAL_PHASE0_REFERENCE_MISSING")
        phase0_bytes = git_show_bytes(control_commit, phase0_path, cwd=source_repo)
        if sha256_bytes(phase0_bytes) != phase0_sha:
            raise Stop("STAGE2_PROPOSAL_PHASE0_HASH_MISMATCH")
        phase0 = json.loads(phase0_bytes)
        writeahead_path = str(phase0.get("writeahead_manifest_path") or "")
        writeahead_sha = str(phase0.get("writeahead_manifest_sha256") or "")
    elif kind == "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR":
        stage2 = authority.get("post_repair_stage2") or {}
        stage2_status = stage2.get("stage2_status")
        blocker_count = int(stage2.get("blocker_count", -1))
        warning_count = int(stage2.get("warning_count", -1))
        decision_sha = stage2.get("decision_universe_sha256")
        target_sha = authority.get("actual_published_target_sha")
        target_tree_sha = authority.get("prepared_tree_sha")
        integration_freeze_sha = authority.get("integration_freeze_sha256")
        semantic_sha = authority.get("semantic_snapshot_sha256")
        writeahead_path = str(authority.get("writeahead_manifest_path") or "")
        writeahead_sha = str(authority.get("writeahead_manifest_sha256") or "")
    else:
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_KIND_UNSUPPORTED")

    if authority.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_SCHOOL_MISMATCH")
    if authority.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_BRANCH_MISMATCH")
    if target_sha != request["target_sha"]:
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_TARGET_MISMATCH")
    if stage2_status != "CAPABILITY_CENSUS_READY":
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_NOT_READY")
    if blocker_count != 0:
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_BLOCKERS_PRESENT")
    if warning_count != 0:
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_WARNINGS_PRESENT")
    if decision_sha != request["decision_universe_sha256"]:
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_DECISION_UNIVERSE_MISMATCH")
    if integration_freeze_sha != request["integration_freeze_sha256"]:
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_FREEZE_MISMATCH")
    if semantic_sha != request["semantic_snapshot_sha256"]:
        raise Stop("STAGE2_PROPOSAL_AUTHORITY_SEMANTIC_MISMATCH")
    if not writeahead_path or not writeahead_sha:
        raise Stop("STAGE2_PROPOSAL_WRITEAHEAD_REFERENCE_MISSING")

    freeze_bytes, writeahead = _freeze_from_writeahead(
        control_commit=control_commit,
        writeahead_path=writeahead_path,
        writeahead_sha256=writeahead_sha,
        request=request,
        source_repo=source_repo,
    )
    return {
        "authority": authority,
        "authority_bytes": authority_bytes,
        "authority_kind": kind,
        "target_tree_sha": target_tree_sha,
        "freeze_bytes": freeze_bytes,
        "writeahead": writeahead,
    }


def normalize_proposal_artifact_bytes(
    name: str,
    data: bytes,
    repo: Path,
    map_path: Path,
) -> bytes:
    result = normalize_artifact_bytes(name, data, repo)
    for value in {str(map_path), str(map_path.resolve())}:
        if value:
            result = result.replace(value.encode("utf-8"), b"<MAP>")
    if name == STAGE2_STATUS:
        doc = json.loads(result)
        recommendation = doc.get("recommendation_map")
        if isinstance(recommendation, dict) and recommendation.get("path"):
            recommendation["path"] = "<MAP>"
        result = (
            json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
    return result


def proposal_artifact_hashes(
    repo: Path,
    school_key: str,
    map_path: Path,
) -> tuple[dict[str, str], dict[str, str]]:
    directory = repo / ".onboarding" / school_key
    raw: dict[str, str] = {}
    normalized: dict[str, str] = {}
    for name in PROPOSAL_ARTIFACT_NAMES:
        path = directory / name
        if not path.is_file():
            continue
        data = path.read_bytes()
        raw[name] = sha256_bytes(data)
        normalized[name] = sha256_bytes(
            normalize_proposal_artifact_bytes(name, data, repo, map_path)
        )
    return raw, normalized


def run_stage2_proposal_tool(
    repo: Path,
    school_key: str,
    freeze_bytes: bytes,
    map_path: Path,
    expected_decision_universe_sha256: str,
    diag: Path,
    *,
    tool_repo: Path | None = None,
) -> dict[str, Any]:
    """Run the unchanged permanent Stage-2 coordinator with one exact map payload."""

    restore_integration_freeze(repo, school_key, freeze_bytes)
    before = tracked_worktree_state(repo)
    if before["status"]:
        raise Stop("STAGE2_PROPOSAL_TRACKED_STATE_DIRTY_BEFORE_RUN")

    runtime_repo = (tool_repo or RUNTIME_ROOT).resolve()
    tool_path = runtime_repo / "tools/implementation_stage2.py"
    if not tool_path.is_file():
        raise Stop("STAGE2_PROPOSAL_RUNTIME_TOOL_MISSING:%s" % tool_path)
    runtime_tool_sha256 = sha256_file(tool_path)
    cmd = [
        sys.executable,
        str(tool_path),
        school_key,
        "--repo",
        str(repo),
        "--map",
        str(map_path),
    ]
    cp = run(cmd, cwd=runtime_repo, check=False)
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "stage2-proposal-rehearsal.log").write_text(cp.stdout, encoding="utf-8")

    after = tracked_worktree_state(repo)
    if (
        before["head_sha"] != after["head_sha"]
        or before["tree_sha"] != after["tree_sha"]
        or after["status"]
    ):
        raise Stop(
            "TRACKED_STAGE2_MUTATION_DETECTED before_head=%s after_head=%s "
            "before_tree=%s after_tree=%s status=%r"
            % (
                before["head_sha"],
                after["head_sha"],
                before["tree_sha"],
                after["tree_sha"],
                after["status"],
            )
        )

    status_path = repo / ".onboarding" / school_key / STAGE2_STATUS
    if not status_path.is_file():
        raise Stop("PERMANENT_STAGE2_PROPOSAL_STATUS_ARTIFACT_MISSING")
    status = json.loads(status_path.read_text(encoding="utf-8"))
    stage2_status = str(status.get("status") or "")
    if stage2_status not in PROPOSAL_ALLOWED_STATUSES:
        raise Stop("PERMANENT_STAGE2_PROPOSAL_STATUS_UNSUPPORTED:%s" % stage2_status)
    if stage2_status == "OWNER_GATE_1_READY" and cp.returncode != 0:
        raise Stop("PERMANENT_STAGE2_PROPOSAL_READY_EXIT_CODE_MISMATCH")
    if stage2_status == "BLOCKED" and cp.returncode == 0:
        raise Stop("PERMANENT_STAGE2_PROPOSAL_BLOCKED_EXIT_CODE_MISMATCH")

    preflight = status.get("preflight") or {}
    if preflight.get("decision_universe_sha256") != expected_decision_universe_sha256:
        raise Stop("STAGE2_PROPOSAL_DECISION_UNIVERSE_MISMATCH")

    raw_hashes, normalized_hashes = proposal_artifact_hashes(
        repo, school_key, map_path
    )
    for name in (STAGE2_STATUS, "plan.json", "review.csv", "review.md"):
        if name not in raw_hashes:
            raise Stop("PERMANENT_STAGE2_PROPOSAL_ARTIFACT_MISSING:%s" % name)
    capability = status.get("capability_census") or {}
    if capability.get("path") and STAGE2_CENSUS not in raw_hashes:
        raise Stop("PERMANENT_STAGE2_PROPOSAL_CAPABILITY_CENSUS_MISSING")
    if stage2_status == "OWNER_GATE_1_READY":
        recommendation = status.get("recommendation_map") or {}
        if recommendation.get("sha256") != sha256_file(map_path):
            raise Stop("PERMANENT_STAGE2_PROPOSAL_MAP_HASH_MISMATCH")
        if not status.get("proposal_rehearsal"):
            raise Stop("PERMANENT_STAGE2_PROPOSAL_SUMMARY_MISSING")

    census_doc = None
    census_path = repo / ".onboarding" / school_key / STAGE2_CENSUS
    if census_path.is_file():
        census_doc = json.loads(census_path.read_text(encoding="utf-8"))
    site_doc = None
    site_path = repo / ".onboarding" / school_key / SITE_DIAGNOSTIC
    if site_path.is_file():
        site_doc = json.loads(site_path.read_text(encoding="utf-8"))

    return {
        "command": [
            "python",
            "tools/implementation_stage2.py",
            school_key,
            "--map",
            "<MAP>",
        ],
        "exit_code": cp.returncode,
        "stage2_status": stage2_status,
        "status": status,
        "capability_census": census_doc,
        "site_diagnostic": site_doc,
        "artifact_sha256": raw_hashes,
        "artifact_normalized_sha256": normalized_hashes,
        "runtime_tool_sha256": runtime_tool_sha256,
        "tracked_mutation_proof": {
            "before_head_sha": before["head_sha"],
            "after_head_sha": after["head_sha"],
            "before_tree_sha": before["tree_sha"],
            "after_tree_sha": after["tree_sha"],
            "before_status": before["status"],
            "after_status": after["status"],
            "tracked_stage2_mutation": "NONE",
        },
    }
