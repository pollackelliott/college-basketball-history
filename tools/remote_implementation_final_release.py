#!/usr/bin/env python3
"""Bind post-Gate-2 connector merge to one exact Production-proof request."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from remote_implementation_control import sha256_bytes
from remote_implementation_io import Stop, git_show_bytes

FINAL_RELEASE_CONTINUATION_KIND = "RELEASE_GATE2_TO_PRODUCTION_V1"
MERGE_PACKET_KIND = "REMOTE_IMPLEMENTATION_GATE2_MERGE_PACKET"


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise Stop(code)


def verify_final_release_packet_binding(
    request: dict[str, Any],
    control_head: str,
    *,
    repo: Path,
) -> dict[str, Any] | None:
    """Authenticate the optional fresh-verified Gate-2 merge handoff."""

    checkpoint_ref = request["owner_gate_2_checkpoint"]
    checkpoint_path = checkpoint_ref["path"]
    checkpoint_bytes = git_show_bytes(control_head, checkpoint_path, cwd=repo)
    _require(
        sha256_bytes(checkpoint_bytes) == checkpoint_ref["sha256"],
        "FINAL_RELEASE_GATE2_CHECKPOINT_HASH_MISMATCH",
    )
    checkpoint = json.loads(checkpoint_bytes)
    production_id = checkpoint.get("production_request_id")
    if production_id is None:
        return None

    _require(
        request.get("request_id") == production_id,
        "FINAL_RELEASE_PRODUCTION_REQUEST_ID_MISMATCH",
    )

    gate2_id = checkpoint["request_id"]
    verification_ref = request["owner_gate_2_verification"]
    expected_verification_path = (
        f".remote-implementation/verifications/{request['school_key']}/"
        f"{gate2_id}/gate2-approval-verification.json"
    )
    _require(
        verification_ref["path"] == expected_verification_path,
        "FINAL_RELEASE_GATE2_VERIFICATION_PATH_MISMATCH",
    )
    verification_bytes = git_show_bytes(
        control_head,
        verification_ref["path"],
        cwd=repo,
    )
    _require(
        sha256_bytes(verification_bytes) == verification_ref["sha256"],
        "FINAL_RELEASE_GATE2_VERIFICATION_HASH_MISMATCH",
    )
    verification = json.loads(verification_bytes)
    _require(
        verification.get("production_request_id") == production_id,
        "FINAL_RELEASE_VERIFICATION_PRODUCTION_ID_MISMATCH",
    )
    _require(
        verification.get("gate2_merge_packet_sha256")
        == checkpoint.get("gate2_merge_packet_sha256")
        and bool(checkpoint.get("gate2_merge_packet_sha256")),
        "FINAL_RELEASE_MERGE_PACKET_VERIFICATION_HASH_MISMATCH",
    )

    gate2_request_path = (
        Path(checkpoint_path).parent / "request.json"
    ).as_posix()
    gate2_request_bytes = git_show_bytes(
        control_head,
        gate2_request_path,
        cwd=repo,
    )
    _require(
        sha256_bytes(gate2_request_bytes) == checkpoint["request_sha256"],
        "FINAL_RELEASE_GATE2_REQUEST_HASH_MISMATCH",
    )
    gate2_request = json.loads(gate2_request_bytes)
    continuation = gate2_request.get("final_release_continuation")
    _require(
        isinstance(continuation, dict)
        and continuation.get("kind") == FINAL_RELEASE_CONTINUATION_KIND
        and continuation.get("production_request_id") == production_id,
        "FINAL_RELEASE_CONTINUATION_MISMATCH",
    )

    packet_path = (
        Path(checkpoint_path).parent / "gate2-merge-packet.json"
    ).as_posix()
    _require(
        checkpoint.get("gate2_merge_packet_path") == packet_path,
        "FINAL_RELEASE_MERGE_PACKET_PATH_MISMATCH",
    )
    packet_bytes = git_show_bytes(control_head, packet_path, cwd=repo)
    _require(
        sha256_bytes(packet_bytes) == checkpoint["gate2_merge_packet_sha256"],
        "FINAL_RELEASE_MERGE_PACKET_HASH_MISMATCH",
    )
    packet = json.loads(packet_bytes)

    expected = {
        "kind": MERGE_PACKET_KIND,
        "gate2_request_id": gate2_id,
        "production_request_id": production_id,
        "school_key": request["school_key"],
        "pr_number": request["pr_number"],
        "pr_head_sha": request["target_sha"],
        "target_branch": request["target_branch"],
        "base_branch": "main",
        "approved_main_sha": gate2_request["expected_protected_main_sha"],
        "merge_method": "merge",
        "owner_gate_2_approved": True,
        "merged": False,
        "production_proof": False,
    }
    for field, value in expected.items():
        _require(
            packet.get(field) == value,
            "FINAL_RELEASE_MERGE_PACKET_FIELD_MISMATCH:" + field,
        )

    return packet
