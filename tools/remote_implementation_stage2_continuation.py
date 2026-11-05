#!/usr/bin/env python3
"""Queue deterministic Stage 2 continuation requests after fresh verification.

This helper runs only after a fresh-verified STAGE2_CURRENT_MAIN_REFRESH or
STAGE2_CENSUS operation. It converts one already-authorized phase continuation
spec into the next ordinary guarded request, preserving every existing request,
checkpoint, fresh-verification, CAS, and owner-gate boundary.

It does not execute Stage 2 itself and does not create new owner authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from remote_implementation_control import (
    LIFECYCLE_IDLE,
    OP_STAGE2_CENSUS,
    OP_STAGE2_CURRENT_MAIN_REFRESH,
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
    REQUEST_PATH,
    STATE_PATH,
    Stop,
    configure_git,
    fetch_operational_refs,
    git,
    git_show_bytes,
    git_show_json,
    push_control,
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


def _base_authority(*, census: bool = False, proposal: bool = False) -> dict[str, Any]:
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
        "stage2_preseal_rehearsal": False,
        "stage2_gate1_seal": False,
        "stage2_sealed_apply": False,
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
    if last.get("protected_main_sha") != live_main:
        raise Stop("STAGE2_CONTINUATION_PROTECTED_MAIN_CHANGED")

    operation = last.get("operation")
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
