#!/usr/bin/env python3
"""Read-only remote execution for one filled-review pre-seal rehearsal.

This module authenticates an exact fresh-verified STAGE2_GATE1_FILL checkpoint,
restores only the ignored inputs required by the permanent rehearse-review command,
and proves tracked basketball state remains unchanged. It never seals or applies.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from remote_implementation_control import sha256_bytes, sha256_file
from remote_implementation_io import ROOT, Stop, git_show_bytes, run
from remote_implementation_stage2_census import (
    RUNTIME_ROOT,
    restore_integration_freeze,
    tracked_worktree_state,
)
from remote_implementation_stage2_gate1_fill import verify_stage2_gate1_fill_authority

SOURCE_PLAN = "plan.json"
FILLED_REVIEW = "filled-review.csv"
SITE_GATE_NAME = "last-rehearsal-site-gate.json"

_PREVIEW_RE = re.compile(r"Preview approved-plan hash:\s*([0-9a-f]{64})")
_CHANGED_RE = re.compile(r"Changed paths:\s*([0-9,]+)")


def _bound_bytes(
    control_commit: str,
    path: str,
    expected_sha256: str,
    *,
    source_repo: Path = ROOT,
    mismatch_code: str,
) -> bytes:
    data = git_show_bytes(control_commit, path, cwd=source_repo)
    if sha256_bytes(data) != expected_sha256:
        raise Stop(mismatch_code)
    return data


def _normalize_text(text: str, *, repo: Path) -> str:
    normalized = text.replace(str(repo.resolve()), "<TARGET_REPO>")
    normalized = re.sub(
        r"/tmp/preseal-[^/\s]+(?:/repository)?",
        "<PRESEAL_REPO>",
        normalized,
    )
    return normalized


def _normalize_json(value: Any, *, repo: Path) -> Any:
    if isinstance(value, dict):
        return {
            key: _normalize_json(item, repo=repo)
            for key, item in sorted(value.items())
        }
    if isinstance(value, list):
        return [_normalize_json(item, repo=repo) for item in value]
    if isinstance(value, str):
        return _normalize_text(value, repo=repo)
    return value


def verify_stage2_preseal_authority(
    request: dict[str, Any],
    control_commit: str,
    *,
    source_repo: Path = ROOT,
) -> dict[str, Any]:
    """Authenticate exact Gate 1 fill + its fresh equivalence + approval chain."""

    checkpoint_ref = request["stage2_gate1_fill_checkpoint"]
    checkpoint_bytes = _bound_bytes(
        control_commit,
        checkpoint_ref["path"],
        checkpoint_ref["sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_PRESEAL_GATE1_FILL_CHECKPOINT_HASH_MISMATCH",
    )
    try:
        manifest = json.loads(checkpoint_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_CHECKPOINT_JSON_INVALID") from exc

    if manifest.get("kind") != "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_CHECKPOINT":
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_CHECKPOINT_KIND_MISMATCH")
    if manifest.get("gate1_fill_status") != "FILLED":
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_NOT_FILLED")
    if manifest.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_SCHOOL_MISMATCH")
    if manifest.get("target_branch") != request["target_branch"]:
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_BRANCH_MISMATCH")
    if manifest.get("target_sha") != request["target_sha"]:
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_TARGET_MISMATCH")

    for field, code in (
        ("integration_freeze_sha256", "FREEZE"),
        ("semantic_snapshot_sha256", "SEMANTIC"),
        ("decision_universe_sha256", "DECISION_UNIVERSE"),
        ("recommendation_map_sha256", "MAP"),
        ("approved_plan_hash_preview", "APPROVED_PLAN_PREVIEW"),
        ("filled_review_sha256", "FILLED_REVIEW"),
        ("decision_id_set_sha256", "DECISION_ID_SET"),
    ):
        if manifest.get(field) != request[field]:
            raise Stop("STAGE2_PRESEAL_GATE1_FILL_%s_MISMATCH" % code)

    verification_ref = request["stage2_gate1_fill_verification"]
    verification_bytes = _bound_bytes(
        control_commit,
        verification_ref["path"],
        verification_ref["sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_PRESEAL_GATE1_FILL_VERIFICATION_HASH_MISMATCH",
    )
    try:
        verification = json.loads(verification_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_VERIFICATION_JSON_INVALID") from exc
    if (
        verification.get("kind")
        != "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_VERIFICATION"
    ):
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_VERIFICATION_KIND_MISMATCH")
    if verification.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_VERIFICATION_REQUEST_MISMATCH")
    if verification.get("school_key") != request["school_key"]:
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_VERIFICATION_SCHOOL_MISMATCH")
    if verification.get("target_sha") != request["target_sha"]:
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_VERIFICATION_TARGET_MISMATCH")
    if verification.get("remote_stage2_gate1_fill_equivalence") != "PASS":
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_EQUIVALENCE_NOT_PASS")
    if verification.get("tracked_stage2_mutation") != "NONE":
        raise Stop("STAGE2_PRESEAL_GATE1_FILL_TRACKED_MUTATION")
    for field, code in (
        ("integration_freeze_sha256", "FREEZE"),
        ("semantic_snapshot_sha256", "SEMANTIC"),
        ("decision_universe_sha256", "DECISION_UNIVERSE"),
        ("recommendation_map_sha256", "MAP"),
        ("approved_plan_hash_preview", "APPROVED_PLAN_PREVIEW"),
        ("filled_review_sha256", "FILLED_REVIEW"),
        ("decision_id_set_sha256", "DECISION_ID_SET"),
    ):
        if verification.get(field) != request[field]:
            raise Stop("STAGE2_PRESEAL_VERIFICATION_%s_MISMATCH" % code)

    directory = Path(checkpoint_ref["path"]).parent
    fill_request_path = (directory / "request.json").as_posix()
    fill_request_bytes = git_show_bytes(
        control_commit,
        fill_request_path,
        cwd=source_repo,
    )
    if sha256_bytes(fill_request_bytes) != manifest.get("request_sha256"):
        raise Stop("STAGE2_PRESEAL_SOURCE_FILL_REQUEST_HASH_MISMATCH")
    try:
        fill_request = json.loads(fill_request_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("STAGE2_PRESEAL_SOURCE_FILL_REQUEST_JSON_INVALID") from exc
    if fill_request.get("request_id") != manifest.get("request_id"):
        raise Stop("STAGE2_PRESEAL_SOURCE_FILL_REQUEST_ID_MISMATCH")

    fill_authority = verify_stage2_gate1_fill_authority(
        fill_request,
        control_commit,
        source_repo=source_repo,
    )

    plan_path = str(manifest.get("plan_checkpoint_path") or "")
    review_path = str(manifest.get("filled_review_checkpoint_path") or "")
    if not plan_path or not review_path:
        raise Stop("STAGE2_PRESEAL_INPUT_PATH_MISSING")

    plan_bytes = _bound_bytes(
        control_commit,
        plan_path,
        str(manifest.get("plan_sha256") or ""),
        source_repo=source_repo,
        mismatch_code="STAGE2_PRESEAL_PLAN_HASH_MISMATCH",
    )
    filled_review_bytes = _bound_bytes(
        control_commit,
        review_path,
        request["filled_review_sha256"],
        source_repo=source_repo,
        mismatch_code="STAGE2_PRESEAL_FILLED_REVIEW_HASH_MISMATCH",
    )

    return {
        "gate1_fill_manifest": manifest,
        "gate1_fill_checkpoint_bytes": checkpoint_bytes,
        "gate1_fill_verification": verification,
        "gate1_fill_verification_bytes": verification_bytes,
        "gate1_fill_request": fill_request,
        "gate1_fill_authority": fill_authority,
        "freeze_bytes": fill_authority["freeze_bytes"],
        "plan_bytes": plan_bytes,
        "filled_review_bytes": filled_review_bytes,
        "target_tree_sha": manifest.get("target_tree_sha"),
        "owner_gate_1_approval_sha256": manifest.get(
            "owner_gate_1_approval_sha256"
        ),
    }


def run_stage2_preseal_rehearsal_tool(
    repo: Path,
    school_key: str,
    *,
    freeze_bytes: bytes,
    plan_bytes: bytes,
    filled_review_bytes: bytes,
    expected_approved_plan_hash_preview: str,
    diag: Path,
    tool_repo: Path | None = None,
) -> dict[str, Any]:
    """Run the permanent filled-review rehearsal without tracked mutation."""

    restore_integration_freeze(repo, school_key, freeze_bytes)
    output = repo / ".onboarding" / school_key
    output.mkdir(parents=True, exist_ok=True)
    plan_path = output / SOURCE_PLAN
    review_path = output / FILLED_REVIEW
    plan_path.write_bytes(plan_bytes)
    review_path.write_bytes(filled_review_bytes)

    before = tracked_worktree_state(repo)
    if before["status"]:
        raise Stop("STAGE2_PRESEAL_TRACKED_STATE_DIRTY_BEFORE_RUN")

    runtime_repo = (tool_repo or RUNTIME_ROOT).resolve()
    hardening_tool = runtime_repo / "tools/onboarding_hardening.py"
    onboard_tool = runtime_repo / "tools/onboard_school.py"
    if not hardening_tool.is_file():
        raise Stop("STAGE2_PRESEAL_RUNTIME_HARDENING_TOOL_MISSING")
    if not onboard_tool.is_file():
        raise Stop("STAGE2_PRESEAL_RUNTIME_ONBOARD_TOOL_MISSING")
    runtime_tool_sha256 = {
        "tools/onboarding_hardening.py": sha256_file(hardening_tool),
        "tools/onboard_school.py": sha256_file(onboard_tool),
    }

    cmd = [
        sys.executable,
        str(hardening_tool),
        "rehearse-review",
        school_key,
        "--repo",
        str(repo),
        "--plan-file",
        str(plan_path),
        "--review-file",
        str(review_path),
    ]
    cp = run(cmd, cwd=runtime_repo, check=False)
    diag.mkdir(parents=True, exist_ok=True)
    log_text = cp.stdout or ""
    (diag / "stage2-preseal-rehearsal.log").write_text(
        log_text,
        encoding="utf-8",
    )

    after = tracked_worktree_state(repo)
    if (
        before["head_sha"] != after["head_sha"]
        or before["tree_sha"] != after["tree_sha"]
        or after["status"]
    ):
        raise Stop(
            "STAGE2_PRESEAL_TRACKED_MUTATION_DETECTED "
            "before_head=%s after_head=%s before_tree=%s after_tree=%s status=%r"
            % (
                before["head_sha"],
                after["head_sha"],
                before["tree_sha"],
                after["tree_sha"],
                after["status"],
            )
        )

    normalized_log = _normalize_text(log_text, repo=repo)
    normalized_log_sha256 = sha256_bytes(normalized_log.encode("utf-8"))

    preview_match = _PREVIEW_RE.search(log_text)
    changed_match = _CHANGED_RE.search(log_text)
    preview_hash = preview_match.group(1) if preview_match else None
    changed_path_count = (
        int(changed_match.group(1).replace(",", ""))
        if changed_match
        else None
    )

    site_path = output / SITE_GATE_NAME
    site_json = None
    site_normalized_sha256 = None
    if site_path.is_file():
        try:
            site_json = json.loads(site_path.read_text(encoding="utf-8"))
        except (TypeError, ValueError) as exc:
            raise Stop("STAGE2_PRESEAL_SITE_GATE_JSON_INVALID") from exc
        normalized_site = _normalize_json(site_json, repo=repo)
        site_normalized_sha256 = sha256_bytes(
            (
                json.dumps(
                    normalized_site,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                + "\n"
            ).encode("utf-8")
        )

    status = "READY_TO_SEAL" if cp.returncode == 0 else "BLOCKED"
    if status == "READY_TO_SEAL":
        if preview_hash != expected_approved_plan_hash_preview:
            raise Stop(
                "STAGE2_PRESEAL_APPROVED_PLAN_HASH_MISMATCH expected=%s actual=%s"
                % (expected_approved_plan_hash_preview, preview_hash)
            )
        if changed_path_count is None:
            raise Stop("STAGE2_PRESEAL_CHANGED_PATH_COUNT_MISSING")
        if "TECHNICAL READINESS PASSED" not in log_text:
            raise Stop("STAGE2_PRESEAL_SUCCESS_MARKER_MISSING")

    return {
        "command": [
            "python",
            "tools/onboarding_hardening.py",
            "rehearse-review",
            school_key,
        ],
        "exit_code": cp.returncode,
        "preseal_status": status,
        "approved_plan_hash_preview": preview_hash,
        "changed_path_count": changed_path_count,
        "normalized_log_sha256": normalized_log_sha256,
        "site_gate": site_json,
        "site_gate_normalized_sha256": site_normalized_sha256,
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
