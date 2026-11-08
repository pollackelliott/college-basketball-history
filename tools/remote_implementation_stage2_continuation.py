#!/usr/bin/env python3
"""Queue deterministic Stage 2 continuation requests after fresh verification.

This helper runs only after a fresh-verified operation carrying a supported
phase-continuation spec. It converts one already-authorized continuation into
the next ordinary guarded request, preserving every existing request,
checkpoint, fresh-verification, CAS, and owner-gate boundary.

It does not execute Stage 2 itself and does not create new owner authority.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from remote_implementation_control import (
    LIFECYCLE_IDLE,
    OP_STAGE2_CENSUS,
    OP_STAGE2_CURRENT_MAIN_REFRESH,
    OP_STAGE2_GATE1_FILL,
    OP_STAGE2_PRESEAL_REHEARSAL,
    OP_STAGE2_GATE1_SEAL,
    OP_STAGE2_SEALED_APPLY,
    OP_STAGE2_PROPOSAL_REHEARSAL,
    REQUEST_KIND,
    REQUEST_SCHEMA_VERSION,
    request_used,
    sha256_bytes,
    validate_control_state,
    validate_request,
    validate_stage2_phase_continuation,
)
from remote_implementation_io import (
    CONTROL_BRANCH,
    REQUEST_PATH,
    STATE_PATH,
    Stop,
    configure_git,
    fetch_operational_refs,
    git,
    git_show_bytes,
    git_show_json,
    push_control,
    run,
    write_json,
)


def _archived_request_path(request_id: str) -> str:
    return f".remote-implementation/requests/{request_id}/request.json"


def _load_archived_request(control_head: str, request_id: str) -> tuple[dict[str, Any], bytes]:
    path = _archived_request_path(request_id)
    data = git_show_bytes(control_head, path)
    try:
        request = json.loads(data)
    except json.JSONDecodeError as exc:
        raise Stop("STAGE2_CONTINUATION_ARCHIVED_REQUEST_INVALID") from exc
    if request.get("request_id") != request_id:
        raise Stop("STAGE2_CONTINUATION_ARCHIVED_REQUEST_ID_MISMATCH")
    return request, data


def _verify_payload_ref(control_head: str, ref: dict[str, str], label: str) -> bytes:
    path = str(ref.get("path") or "")
    expected = str(ref.get("sha256") or "")
    data = git_show_bytes(control_head, path)
    if sha256_bytes(data) != expected:
        raise Stop(f"STAGE2_CONTINUATION_{label}_HASH_MISMATCH")
    return data


def _base_authority(
    *,
    census: bool = False,
    proposal: bool = False,
    preseal: bool = False,
    seal: bool = False,
    apply: bool = False,
) -> dict[str, Any]:
    return {
        "owner_gate_1": False,
        "owner_gate_2": False,
        "release": False,
        "phase0": False,
        "recovery": False,
        "stage2_census": census,
        "stage2_opponent_display_normalize": False,
        "stage2_proposal_rehearsal": proposal,
        "stage2_reconciliation_diagnostic": False,
        "stage2_gate1_fill": False,
        "stage2_preseal_rehearsal": preseal,
        "stage2_gate1_seal": seal,
        "stage2_sealed_apply": apply,
        "stage2_current_main_refresh": False,
        "venue_identity_maintenance": False,
        "release_readiness": False,
        "release_preview_verify": False,
        "release_gate2_approval": False,
        "release_production_proof": False,
        "phase0_scope_supersession": False,
    }


def _request_base(
    *,
    parent: dict[str, Any],
    operation: str,
    request_id: str,
    control_head: str,
    state_bytes: bytes,
    live_main: str,
    authority: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": REQUEST_SCHEMA_VERSION,
        "kind": REQUEST_KIND,
        "request_id": request_id,
        "school_key": parent["school_key"],
        "operation": operation,
        "previous_control_state_commit": control_head,
        "previous_control_state_sha256": sha256_bytes(state_bytes),
        "expected_protected_main_sha": live_main,
        "creation_provenance": {
            "origin": "repository-owned Stage 2 phase continuation",
            "authorization": (
                "phase-persistent owner/Control Center authority inherited from "
                + str(parent["request_id"])
            ),
        },
        "authority": authority,
    }


def _already_queued(control_head: str, state: dict[str, Any], request_id: str) -> bool:
    if request_used(state, request_id):
        return True
    try:
        current = git_show_json(control_head, REQUEST_PATH.as_posix())
    except Exception:
        return False
    return current.get("request_id") == request_id


def _dispatch_child_workflow_if_actions(new_head: str) -> None:
    """Launch the child control-plane run when this queue push came from Actions.

    Ordinary pushes made by a user/connector already trigger the control workflow.
    GitHub suppresses push-triggered workflow recursion for pushes authenticated by
    the workflow's own GITHUB_TOKEN, so Actions-authored continuation requests must
    explicitly use workflow_dispatch after their exact control-ref CAS succeeds.
    """

    if os.environ.get("GITHUB_ACTIONS", "").strip().lower() != "true":
        return

    repository = os.environ.get("GITHUB_REPOSITORY", "").strip()
    token = os.environ.get("GH_TOKEN", "").strip()
    if not repository:
        raise Stop("STAGE2_CONTINUATION_DISPATCH_REPOSITORY_MISSING")
    if not token:
        raise Stop("STAGE2_CONTINUATION_DISPATCH_TOKEN_MISSING")

    cp = run(
        [
            "gh",
            "api",
            "--method",
            "POST",
            f"repos/{repository}/actions/workflows/remote-implementation.yml/dispatches",
            "-f",
            f"ref={CONTROL_BRANCH}",
        ],
        check=False,
    )
    if cp.returncode != 0:
        raise Stop(
            "STAGE2_CONTINUATION_WORKFLOW_DISPATCH_FAILED\n"
            + str(cp.stdout or "")
        )
    print(
        "STAGE2 CONTINUATION DISPATCHED: "
        f"workflow=remote-implementation.yml ref={CONTROL_BRANCH} queued_commit={new_head}"
    )


def _queue_request(
    request: dict[str, Any],
    *,
    expected_control_head: str,
    state: dict[str, Any],
) -> str:
    request_id = request["request_id"]
    if _already_queued(expected_control_head, state, request_id):
        print(f"STAGE2 CONTINUATION: already queued/used request={request_id}")
        return expected_control_head

    validate_request(request)
    local_head = git("rev-parse", "HEAD").stdout.strip()
    if local_head != expected_control_head:
        raise Stop(
            "STAGE2_CONTINUATION_LOCAL_CONTROL_HEAD_MISMATCH "
            f"expected={expected_control_head} actual={local_head}"
        )

    write_json(REQUEST_PATH, request)
    git("add", "--", REQUEST_PATH.as_posix())
    git("commit", "-m", f"queue Stage 2 continuation {request_id}")
    new_head = push_control(expected_control_head)
    _dispatch_child_workflow_if_actions(new_head)
    print(
        "STAGE2 CONTINUATION QUEUED: "
        f"operation={request['operation']} request={request_id} commit={new_head}"
    )
    return new_head


def _continuation_from_parent(parent: dict[str, Any]) -> dict[str, Any] | None:
    continuation = parent.get("phase_continuation")
    if continuation is None:
        return None
    validate_stage2_phase_continuation(parent["operation"], parent["request_id"], continuation)
    return continuation


def verify_phase_continuation_payloads(
    request: dict[str, Any],
    control_commit: str,
) -> None:
    """Bind continuation payload bytes before any refresh mutation occurs."""

    spec = request.get("phase_continuation")
    if spec is None:
        return
    validate_stage2_phase_continuation(
        request["operation"],
        request["request_id"],
        spec,
    )
    _verify_payload_ref(
        control_commit,
        spec["recommendation_map"],
        "RECOMMENDATION_MAP",
    )
    challenge = spec.get("historical_game_type_challenge")
    if challenge is not None:
        _verify_payload_ref(
            control_commit,
            challenge,
            "HISTORICAL_CHALLENGE",
        )


def queue_after_refresh(
    *,
    live_main: str,
    control_head: str,
    state: dict[str, Any],
    state_bytes: bytes,
    last: dict[str, Any],
) -> int:
    parent, _ = _load_archived_request(control_head, last["request_id"])
    continuation = _continuation_from_parent(parent)
    if continuation is None:
        print("STAGE2 CONTINUATION: refresh has no phase continuation")
        return 0

    successor_ref = {
        "path": last["successor_manifest_path"],
        "sha256": last["successor_manifest_sha256"],
    }
    successor_bytes = _verify_payload_ref(
        control_head, successor_ref, "REFRESH_SUCCESSOR"
    )
    successor = json.loads(successor_bytes)
    if successor.get("actual_published_target_sha") != last.get("target_sha"):
        raise Stop("STAGE2_CONTINUATION_REFRESH_TARGET_MISMATCH")

    _verify_payload_ref(
        control_head,
        continuation["recommendation_map"],
        "RECOMMENDATION_MAP",
    )
    challenge = continuation.get("historical_game_type_challenge")
    if challenge is not None:
        _verify_payload_ref(control_head, challenge, "HISTORICAL_CHALLENGE")

    request = _request_base(
        parent=parent,
        operation=OP_STAGE2_CENSUS,
        request_id=continuation["census_request_id"],
        control_head=control_head,
        state_bytes=state_bytes,
        live_main=live_main,
        authority=_base_authority(census=True),
    )
    request.update(
        {
            "target_branch": parent["target_branch"],
            "target_sha": successor["actual_published_target_sha"],
            "phase0_successor": parent["phase0_successor"],
            "integration_freeze_sha256": parent["integration_freeze_sha256"],
            "semantic_snapshot_sha256": parent["semantic_snapshot_sha256"],
            "stage2_current_main_refresh_successor": successor_ref,
            "phase_continuation": continuation,
        }
    )
    if parent.get("stage2_opponent_display_successor") is not None:
        request["stage2_opponent_display_successor"] = parent[
            "stage2_opponent_display_successor"
        ]
    if challenge is not None:
        request["historical_game_type_challenge"] = challenge

    _queue_request(
        request,
        expected_control_head=control_head,
        state=state,
    )
    return 0


def queue_after_census(
    *,
    live_main: str,
    control_head: str,
    state: dict[str, Any],
    state_bytes: bytes,
    last: dict[str, Any],
) -> int:
    parent, _ = _load_archived_request(control_head, last["request_id"])
    continuation = _continuation_from_parent(parent)
    if continuation is None:
        print("STAGE2 CONTINUATION: census has no phase continuation")
        return 0

    if last.get("stage2_status") != "CAPABILITY_CENSUS_READY":
        raise Stop(
            "STAGE2_CONTINUATION_CENSUS_NOT_READY:"
            + str(last.get("stage2_status") or "")
        )
    expected_universe = continuation["expected_decision_universe_sha256"]
    actual_universe = str(last.get("decision_universe_sha256") or "")
    if actual_universe != expected_universe:
        raise Stop(
            "STAGE2_CONTINUATION_DECISION_UNIVERSE_CHANGED "
            f"expected={expected_universe} actual={actual_universe}"
        )

    map_ref = continuation["recommendation_map"]
    _verify_payload_ref(control_head, map_ref, "RECOMMENDATION_MAP")
    challenge = continuation.get("historical_game_type_challenge")
    if challenge is not None:
        _verify_payload_ref(control_head, challenge, "HISTORICAL_CHALLENGE")

    stage2_authority = {
        "path": last["checkpoint_manifest_path"],
        "sha256": last["checkpoint_manifest_sha256"],
    }
    _verify_payload_ref(control_head, stage2_authority, "CENSUS_CHECKPOINT")

    request = _request_base(
        parent=parent,
        operation=OP_STAGE2_PROPOSAL_REHEARSAL,
        request_id=continuation["proposal_request_id"],
        control_head=control_head,
        state_bytes=state_bytes,
        live_main=live_main,
        authority=_base_authority(proposal=True),
    )
    request.update(
        {
            "target_branch": parent["target_branch"],
            "target_sha": parent["target_sha"],
            "stage2_authority": stage2_authority,
            "recommendation_map": map_ref,
            "integration_freeze_sha256": parent["integration_freeze_sha256"],
            "semantic_snapshot_sha256": parent["semantic_snapshot_sha256"],
            "decision_universe_sha256": actual_universe,
        }
    )
    if challenge is not None:
        request["historical_game_type_challenge"] = challenge

    _queue_request(
        request,
        expected_control_head=control_head,
        state=state,
    )
    return 0


def _verification_ref(
    control_head: str,
    *,
    school_key: str,
    request_id: str,
    filename: str,
    label: str,
) -> dict[str, str]:
    path = (
        f".remote-implementation/verifications/{school_key}/"
        f"{request_id}/{filename}"
    )
    data = git_show_bytes(control_head, path)
    return {"path": path, "sha256": sha256_bytes(data)}


def _checkpoint_manifest(
    control_head: str,
    last: dict[str, Any],
    *,
    expected_kind: str,
    label: str,
) -> tuple[dict[str, Any], dict[str, str]]:
    ref = {
        "path": last["checkpoint_manifest_path"],
        "sha256": last["checkpoint_manifest_sha256"],
    }
    data = _verify_payload_ref(control_head, ref, label)
    manifest = json.loads(data)
    if manifest.get("kind") != expected_kind:
        raise Stop(f"STAGE2_CONTINUATION_{label}_KIND_MISMATCH")
    return manifest, ref


def queue_after_gate1_fill(
    *,
    live_main: str,
    control_head: str,
    state: dict[str, Any],
    state_bytes: bytes,
    last: dict[str, Any],
) -> int:
    parent, _ = _load_archived_request(control_head, last["request_id"])
    continuation = _continuation_from_parent(parent)
    if continuation is None:
        print("STAGE2 CONTINUATION: Gate 1 fill has no phase continuation")
        return 0

    manifest, checkpoint_ref = _checkpoint_manifest(
        control_head,
        last,
        expected_kind="REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_CHECKPOINT",
        label="GATE1_FILL_CHECKPOINT",
    )
    if manifest.get("gate1_fill_status") != "FILLED":
        raise Stop("STAGE2_CONTINUATION_GATE1_FILL_NOT_FILLED")
    verification_ref = _verification_ref(
        control_head,
        school_key=manifest["school_key"],
        request_id=manifest["request_id"],
        filename="stage2-gate1-fill-verification.json",
        label="GATE1_FILL_VERIFICATION",
    )

    request = _request_base(
        parent=parent,
        operation=OP_STAGE2_PRESEAL_REHEARSAL,
        request_id=continuation["preseal_request_id"],
        control_head=control_head,
        state_bytes=state_bytes,
        live_main=live_main,
        authority=_base_authority(preseal=True),
    )
    request.update(
        {
            "target_branch": manifest["target_branch"],
            "target_sha": manifest["target_sha"],
            "stage2_gate1_fill_checkpoint": checkpoint_ref,
            "stage2_gate1_fill_verification": verification_ref,
            "integration_freeze_sha256": manifest["integration_freeze_sha256"],
            "semantic_snapshot_sha256": manifest["semantic_snapshot_sha256"],
            "decision_universe_sha256": manifest["decision_universe_sha256"],
            "recommendation_map_sha256": manifest["recommendation_map_sha256"],
            "approved_plan_hash_preview": manifest["approved_plan_hash_preview"],
            "filled_review_sha256": manifest["filled_review_sha256"],
            "decision_id_set_sha256": manifest["decision_id_set_sha256"],
            "phase_continuation": continuation,
        }
    )
    _queue_request(
        request,
        expected_control_head=control_head,
        state=state,
    )
    return 0


def queue_after_preseal(
    *,
    live_main: str,
    control_head: str,
    state: dict[str, Any],
    state_bytes: bytes,
    last: dict[str, Any],
) -> int:
    parent, _ = _load_archived_request(control_head, last["request_id"])
    continuation = _continuation_from_parent(parent)
    if continuation is None:
        print("STAGE2 CONTINUATION: pre-seal has no phase continuation")
        return 0

    manifest, checkpoint_ref = _checkpoint_manifest(
        control_head,
        last,
        expected_kind="REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
        label="PRESEAL_CHECKPOINT",
    )
    if manifest.get("preseal_status") != "READY_TO_SEAL":
        raise Stop(
            "STAGE2_CONTINUATION_PRESEAL_NOT_READY:"
            + str(manifest.get("preseal_status") or "")
        )
    verification_ref = _verification_ref(
        control_head,
        school_key=manifest["school_key"],
        request_id=manifest["request_id"],
        filename="stage2-preseal-rehearsal-verification.json",
        label="PRESEAL_VERIFICATION",
    )

    request = _request_base(
        parent=parent,
        operation=OP_STAGE2_GATE1_SEAL,
        request_id=continuation["seal_request_id"],
        control_head=control_head,
        state_bytes=state_bytes,
        live_main=live_main,
        authority=_base_authority(seal=True),
    )
    request.update(
        {
            "target_branch": manifest["target_branch"],
            "target_sha": manifest["target_sha"],
            "stage2_preseal_checkpoint": checkpoint_ref,
            "stage2_preseal_verification": verification_ref,
            "integration_freeze_sha256": manifest["integration_freeze_sha256"],
            "semantic_snapshot_sha256": manifest["semantic_snapshot_sha256"],
            "decision_universe_sha256": manifest["decision_universe_sha256"],
            "recommendation_map_sha256": manifest["recommendation_map_sha256"],
            "approved_plan_hash_preview": manifest["approved_plan_hash_preview"],
            "filled_review_sha256": manifest["filled_review_sha256"],
            "decision_id_set_sha256": manifest["decision_id_set_sha256"],
            "owner_gate_1_approval_sha256": manifest[
                "owner_gate_1_approval_sha256"
            ],
            "equivalence_sha256": manifest["equivalence_sha256"],
            "phase_continuation": continuation,
        }
    )
    _queue_request(
        request,
        expected_control_head=control_head,
        state=state,
    )
    return 0


def queue_after_gate1_seal(
    *,
    live_main: str,
    control_head: str,
    state: dict[str, Any],
    state_bytes: bytes,
    last: dict[str, Any],
) -> int:
    parent, _ = _load_archived_request(control_head, last["request_id"])
    continuation = _continuation_from_parent(parent)
    if continuation is None:
        print("STAGE2 CONTINUATION: Gate 1 seal has no phase continuation")
        return 0

    manifest, checkpoint_ref = _checkpoint_manifest(
        control_head,
        last,
        expected_kind="REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_CHECKPOINT",
        label="GATE1_SEAL_CHECKPOINT",
    )
    if manifest.get("seal_status") != "SEALED":
        raise Stop("STAGE2_CONTINUATION_GATE1_NOT_SEALED")
    verification_ref = _verification_ref(
        control_head,
        school_key=manifest["school_key"],
        request_id=manifest["request_id"],
        filename="stage2-gate1-seal-verification.json",
        label="GATE1_SEAL_VERIFICATION",
    )

    request = _request_base(
        parent=parent,
        operation=OP_STAGE2_SEALED_APPLY,
        request_id=continuation["apply_request_id"],
        control_head=control_head,
        state_bytes=state_bytes,
        live_main=live_main,
        authority=_base_authority(apply=True),
    )
    request.update(
        {
            "target_branch": manifest["target_branch"],
            "target_sha": manifest["target_sha"],
            "stage2_gate1_seal_checkpoint": checkpoint_ref,
            "stage2_gate1_seal_verification": verification_ref,
            "approved_plan_hash": manifest["approved_plan_hash"],
            "approved_plan_sha256": manifest["approved_plan_sha256"],
            "owner_gate_1_approval_sha256": manifest[
                "owner_gate_1_approval_sha256"
            ],
            "integration_freeze_sha256": manifest["integration_freeze_sha256"],
            "semantic_snapshot_sha256": manifest["semantic_snapshot_sha256"],
            "decision_universe_sha256": manifest["decision_universe_sha256"],
            "recommendation_map_sha256": manifest["recommendation_map_sha256"],
            "filled_review_sha256": manifest["filled_review_sha256"],
            "decision_id_set_sha256": manifest["decision_id_set_sha256"],
        }
    )
    _queue_request(
        request,
        expected_control_head=control_head,
        state=state,
    )
    return 0


def main() -> int:
    configure_git()
    live_main, control_head = fetch_operational_refs()
    state_bytes = git_show_bytes(control_head, STATE_PATH.as_posix())
    state = json.loads(state_bytes)
    validate_control_state(state)
    if state.get("lifecycle_state") != LIFECYCLE_IDLE:
        raise Stop("STAGE2_CONTINUATION_CONTROL_NOT_IDLE")

    last = state.get("last_operation") or {}
    if last.get("fresh_runner_verification") != "PASS":
        print("STAGE2 CONTINUATION: last operation is not fresh-verified PASS")
        return 0

    operation = last.get("operation")
    if last.get("protected_main_sha") != live_main:
        if operation == OP_STAGE2_CURRENT_MAIN_REFRESH:
            print(
                "STAGE2 CONTINUATION: protected main advanced after the verified "
                "refresh; do not queue a stale census. A new ordinary current-main "
                "refresh is required."
            )
            return 0
        raise Stop("STAGE2_CONTINUATION_PROTECTED_MAIN_CHANGED")
    if operation == OP_STAGE2_CURRENT_MAIN_REFRESH:
        return queue_after_refresh(
            live_main=live_main,
            control_head=control_head,
            state=state,
            state_bytes=state_bytes,
            last=last,
        )
    if operation == OP_STAGE2_CENSUS:
        return queue_after_census(
            live_main=live_main,
            control_head=control_head,
            state=state,
            state_bytes=state_bytes,
            last=last,
        )
    if operation == OP_STAGE2_GATE1_FILL:
        return queue_after_gate1_fill(
            live_main=live_main,
            control_head=control_head,
            state=state,
            state_bytes=state_bytes,
            last=last,
        )
    if operation == OP_STAGE2_PRESEAL_REHEARSAL:
        return queue_after_preseal(
            live_main=live_main,
            control_head=control_head,
            state=state,
            state_bytes=state_bytes,
            last=last,
        )
    if operation == OP_STAGE2_GATE1_SEAL:
        return queue_after_gate1_seal(
            live_main=live_main,
            control_head=control_head,
            state=state,
            state_bytes=state_bytes,
            last=last,
        )

    print(
        "STAGE2 CONTINUATION: no continuation action for operation="
        + str(operation or "")
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Stop as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
