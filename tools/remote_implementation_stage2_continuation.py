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
    STAGE2_POST_GATE1_CONTINUATION_KIND,
    TX_COMPLETE,
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



def _resume_post_gate1_from_verified_replacement(
    parent: dict[str, Any],
    manifest: dict[str, Any],
    *,
    control_head: str,
    state: dict[str, Any],
    last: dict[str, Any],
) -> dict[str, str] | None:
    """Resume only a verified replacement for an originally BLOCKED pre-seal.

    No original owner approval is restated and no failed request ID is replayed.
    Exact fresh-verified replacement authority must match the original approved
    fill and first blocked pre-seal; otherwise refuse continuation. The resulting
    seal/apply IDs are deterministic and single-use, not retry counters.
    """

    if (
        state.get("lifecycle_state") != LIFECYCLE_IDLE
        or state.get("transaction_state") != TX_COMPLETE
        or state.get("recovery_required") is not False
        or state.get("active_request_id") is not None
        or state.get("active_lock_commit") is not None
        or last.get("fresh_runner_verification") != "PASS"
        or last.get("request_id") != parent.get("request_id")
        or manifest.get("request_id") != parent.get("request_id")
        or manifest.get("school_key") != parent.get("school_key")
    ):
        raise Stop("STAGE2_RESUME_CONTROL_OR_PRESEAL_AUTHORITY_UNSAFE")

    fill_ref = parent.get("stage2_gate1_fill_checkpoint")
    fill_verification_ref = parent.get("stage2_gate1_fill_verification")
    if not isinstance(fill_ref, dict) or not isinstance(fill_verification_ref, dict):
        return None

    try:
        fill = json.loads(_verify_payload_ref(control_head, fill_ref, "RESUME_FILL"))
        fill_verification = json.loads(
            _verify_payload_ref(
                control_head, fill_verification_ref, "RESUME_FILL_VERIFICATION"
            )
        )
    except (ValueError, TypeError) as exc:
        raise Stop("STAGE2_RESUME_FILL_AUTHORITY_INVALID") from exc

    fill_id = fill.get("request_id")
    if (
        fill.get("kind") != "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_CHECKPOINT"
        or fill.get("gate1_fill_status") != "FILLED"
        or fill.get("owner_gate_1_approval", {}).get("approved") is not True
        or fill_verification.get("kind")
        != "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_VERIFICATION"
        or fill_verification.get("request_id") != fill_id
        or fill_verification.get("remote_stage2_gate1_fill_equivalence") != "PASS"
        or fill_verification.get("tracked_stage2_mutation") != "NONE"
        or fill_ref.get("path")
        != (
            f".remote-implementation/checkpoints/{parent['school_key']}/"
            f"{fill_id}/checkpoint-manifest.json"
        )
        or fill_verification_ref.get("path")
        != (
            f".remote-implementation/verifications/{parent['school_key']}/"
            f"{fill_id}/stage2-gate1-fill-verification.json"
        )
    ):
        raise Stop("STAGE2_RESUME_FILL_AUTHORITY_NOT_VERIFIED")

    fill_request, fill_request_bytes = _load_archived_request(control_head, fill_id)
    if (
        fill_request.get("operation") != OP_STAGE2_GATE1_FILL
        or fill_request.get("school_key") != parent["school_key"]
        or fill_request.get("authority", {}).get("owner_gate_1") is not True
        or fill.get("request_sha256") != sha256_bytes(fill_request_bytes)
    ):
        raise Stop("STAGE2_RESUME_ORIGINAL_OWNER_APPROVAL_MISMATCH")

    authorized = _continuation_from_parent(fill_request)
    if authorized is None:
        return None  # An approved fill without continuation cannot create one.

    first_id = authorized["preseal_request_id"]
    if first_id == parent["request_id"]:
        return None  # No distinct blocked predecessor; no replacement to resume.

    first_request, first_request_bytes = _load_archived_request(control_head, first_id)
    if (
        first_request.get("operation") != OP_STAGE2_PRESEAL_REHEARSAL
        or first_request.get("school_key") != parent["school_key"]
        or first_request.get("phase_continuation") != authorized
        or first_request.get("stage2_gate1_fill_checkpoint") != fill_ref
        or first_request.get("stage2_gate1_fill_verification")
        != fill_verification_ref
        or not request_used(state, first_id)
    ):
        raise Stop("STAGE2_RESUME_ORIGINAL_PRESEAL_LINEAGE_INVALID")

    first_checkpoint_path = (
        f".remote-implementation/checkpoints/{parent['school_key']}/"
        f"{first_id}/checkpoint-manifest.json"
    )
    first_verification_path = (
        f".remote-implementation/verifications/{parent['school_key']}/"
        f"{first_id}/stage2-preseal-rehearsal-verification.json"
    )
    try:
        first = json.loads(git_show_bytes(control_head, first_checkpoint_path))
        first_verification = json.loads(
            git_show_bytes(control_head, first_verification_path)
        )
    except (ValueError, TypeError) as exc:
        raise Stop("STAGE2_RESUME_ORIGINAL_PRESEAL_EVIDENCE_INVALID") from exc

    if (
        first.get("kind") != "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT"
        or first.get("request_id") != first_id
        or first.get("request_sha256") != sha256_bytes(first_request_bytes)
        or first_verification.get("kind")
        != "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_VERIFICATION"
        or first_verification.get("request_id") != first_id
    ):
        raise Stop("STAGE2_RESUME_ORIGINAL_PRESEAL_EVIDENCE_INVALID")

    preseal_evidence = [(first, first_verification)]
    seal_evidence: tuple[dict[str, Any], dict[str, Any]] | None = None
    apply_writeahead: dict[str, Any] | None = None

    first_status = first.get("preseal_status")
    if first_status == "BLOCKED":
        if (
            first_verification.get("preseal_status") != "BLOCKED"
            or first_verification.get("remote_stage2_preseal_equivalence") != "PASS"
            or first_verification.get("tracked_stage2_mutation") != "NONE"
        ):
            raise Stop("STAGE2_RESUME_ORIGINAL_PRESEAL_NOT_VERIFIED_BLOCKED")
        if any(
            request_used(state, authorized[key])
            for key in ("seal_request_id", "apply_request_id")
        ):
            raise Stop("STAGE2_RESUME_ORIGINAL_CHILD_ALREADY_CONSUMED")
    elif first_status == "READY_TO_SEAL":
        if (
            first_verification.get("preseal_status") != "READY_TO_SEAL"
            or first_verification.get("remote_stage2_preseal_equivalence") != "PASS"
            or first_verification.get("tracked_stage2_mutation") != "NONE"
        ):
            raise Stop("STAGE2_RESUME_ORIGINAL_PRESEAL_EVIDENCE_INVALID")
        seal_id = authorized["seal_request_id"]
        apply_id = authorized["apply_request_id"]
        accepted = set(state.get("accepted_request_ids") or [])
        consumed = set(state.get("consumed_request_ids") or [])
        abandoned = set(state.get("abandoned_request_ids") or [])
        if (
            seal_id not in accepted
            or seal_id not in consumed
            or apply_id not in accepted
            or apply_id not in abandoned
            or apply_id in consumed
        ):
            raise Stop("STAGE2_RESUME_ORIGINAL_CHILD_RECOVERY_INVALID")

        first_ref = {
            "path": first_checkpoint_path,
            "sha256": sha256_bytes(git_show_bytes(control_head, first_checkpoint_path)),
        }
        first_verification_ref = {
            "path": first_verification_path,
            "sha256": sha256_bytes(
                git_show_bytes(control_head, first_verification_path)
            ),
        }

        seal_request, seal_request_bytes = _load_archived_request(control_head, seal_id)
        seal_checkpoint_path = (
            f".remote-implementation/checkpoints/{parent['school_key']}/"
            f"{seal_id}/checkpoint-manifest.json"
        )
        seal_verification_path = (
            f".remote-implementation/verifications/{parent['school_key']}/"
            f"{seal_id}/stage2-gate1-seal-verification.json"
        )
        try:
            seal = json.loads(git_show_bytes(control_head, seal_checkpoint_path))
            seal_verification = json.loads(
                git_show_bytes(control_head, seal_verification_path)
            )
        except (ValueError, TypeError) as exc:
            raise Stop("STAGE2_RESUME_ORIGINAL_SEAL_EVIDENCE_INVALID") from exc

        seal_ref = {
            "path": seal_checkpoint_path,
            "sha256": sha256_bytes(git_show_bytes(control_head, seal_checkpoint_path)),
        }
        seal_verification_ref = {
            "path": seal_verification_path,
            "sha256": sha256_bytes(
                git_show_bytes(control_head, seal_verification_path)
            ),
        }
        if (
            seal_request.get("operation") != OP_STAGE2_GATE1_SEAL
            or seal_request.get("school_key") != parent["school_key"]
            or seal_request.get("phase_continuation") != authorized
            or seal_request.get("stage2_preseal_checkpoint") != first_ref
            or seal_request.get("stage2_preseal_verification") != first_verification_ref
            or seal.get("kind")
            != "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_CHECKPOINT"
            or seal.get("request_id") != seal_id
            or seal.get("request_sha256") != sha256_bytes(seal_request_bytes)
            or seal.get("seal_status") != "SEALED"
            or seal.get("source_preseal_request_id") != first_id
            or seal_verification.get("kind")
            != "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_VERIFICATION"
            or seal_verification.get("request_id") != seal_id
            or seal_verification.get("seal_status") != "SEALED"
            or seal_verification.get("remote_stage2_gate1_seal_equivalence") != "PASS"
            or seal_verification.get("tracked_stage2_mutation") != "NONE"
        ):
            raise Stop("STAGE2_RESUME_ORIGINAL_SEAL_EVIDENCE_INVALID")
        seal_evidence = (seal, seal_verification)

        apply_request, apply_request_bytes = _load_archived_request(control_head, apply_id)
        writeahead_path = (
            f".remote-implementation/writeahead/{parent['school_key']}/"
            f"{apply_id}/writeahead-manifest.json"
        )
        try:
            apply_writeahead = json.loads(git_show_bytes(control_head, writeahead_path))
        except (ValueError, TypeError) as exc:
            raise Stop("STAGE2_RESUME_ORIGINAL_APPLY_RECOVERY_INVALID") from exc
        if (
            apply_request.get("operation") != OP_STAGE2_SEALED_APPLY
            or apply_request.get("school_key") != parent["school_key"]
            or apply_request.get("stage2_gate1_seal_checkpoint") != seal_ref
            or apply_request.get("stage2_gate1_seal_verification")
            != seal_verification_ref
            or apply_writeahead.get("kind") != "REMOTE_IMPLEMENTATION_WRITEAHEAD"
            or apply_writeahead.get("operation") != OP_STAGE2_SEALED_APPLY
            or apply_writeahead.get("request_id") != apply_id
            or apply_writeahead.get("request_sha256")
            != sha256_bytes(apply_request_bytes)
            or apply_writeahead.get("mutation_state") != "PREPARED_NOT_PUBLISHED"
            or apply_writeahead.get("target_branch") != parent["target_branch"]
            or apply_writeahead.get("expected_target_predecessor_sha")
            != parent["target_sha"]
            or apply_writeahead.get("prepared_parent_sha") != parent["target_sha"]
        ):
            raise Stop("STAGE2_RESUME_ORIGINAL_APPLY_RECOVERY_INVALID")

        # A tooling repair or protected-main advance may require one or more
        # fresh READY replacement pre-seals before the live replacement can
        # continue. Authenticate that exact control-state ancestry backward,
        # through independently verified read-only READY replacements, until the
        # first independently verified BLOCKED pre-seal in the same fill lineage.
        # Bound the walk so malformed/cyclic history fails closed.
        ancestry_commit = str(parent.get("previous_control_state_commit") or "")
        visited_commits: set[str] = set()
        visited_ids: set[str] = set()
        blocked_found = False
        for _ in range(8):
            if not ancestry_commit or ancestry_commit in visited_commits:
                raise Stop("STAGE2_RESUME_PRESEAL_ANCESTRY_STATE_INVALID")
            visited_commits.add(ancestry_commit)
            try:
                ancestor_state = git_show_json(
                    ancestry_commit, STATE_PATH.as_posix()
                )
                validate_control_state(ancestor_state)
            except Exception as exc:
                raise Stop("STAGE2_RESUME_PRESEAL_ANCESTRY_STATE_INVALID") from exc

            ancestor_last = ancestor_state.get("last_operation") or {}
            ancestor_id = str(ancestor_last.get("request_id") or "")
            if (
                ancestor_state.get("lifecycle_state") != LIFECYCLE_IDLE
                or ancestor_state.get("transaction_state") != TX_COMPLETE
                or ancestor_state.get("recovery_required") is not False
                or ancestor_last.get("operation") != OP_STAGE2_PRESEAL_REHEARSAL
                or ancestor_last.get("fresh_runner_verification") != "PASS"
                or ancestor_last.get("school_key") != parent["school_key"]
                or ancestor_last.get("target_branch") != parent["target_branch"]
                or ancestor_last.get("target_sha") != parent["target_sha"]
                or ancestor_id in {"", first_id, parent["request_id"]}
                or ancestor_id in visited_ids
                or ancestor_id
                not in set(ancestor_state.get("consumed_request_ids") or [])
                or not request_used(state, ancestor_id)
            ):
                raise Stop("STAGE2_RESUME_PRESEAL_ANCESTRY_STATE_INVALID")
            visited_ids.add(ancestor_id)

            ancestor_request, ancestor_request_bytes = _load_archived_request(
                control_head, ancestor_id
            )
            if (
                ancestor_request.get("operation") != OP_STAGE2_PRESEAL_REHEARSAL
                or ancestor_request.get("school_key") != parent["school_key"]
                or ancestor_request.get("target_branch") != parent["target_branch"]
                or ancestor_request.get("target_sha") != parent["target_sha"]
                or ancestor_request.get("phase_continuation") is not None
                or ancestor_request.get("stage2_gate1_fill_checkpoint") != fill_ref
                or ancestor_request.get("stage2_gate1_fill_verification")
                != fill_verification_ref
            ):
                raise Stop("STAGE2_RESUME_PRESEAL_ANCESTRY_LINEAGE_INVALID")

            ancestor_checkpoint_path = (
                f".remote-implementation/checkpoints/{parent['school_key']}/"
                f"{ancestor_id}/checkpoint-manifest.json"
            )
            ancestor_verification_path = (
                f".remote-implementation/verifications/{parent['school_key']}/"
                f"{ancestor_id}/stage2-preseal-rehearsal-verification.json"
            )
            try:
                ancestor_bytes = git_show_bytes(
                    control_head, ancestor_checkpoint_path
                )
                ancestor = json.loads(ancestor_bytes)
                ancestor_verification = json.loads(
                    git_show_bytes(control_head, ancestor_verification_path)
                )
            except (ValueError, TypeError) as exc:
                raise Stop(
                    "STAGE2_RESUME_PRESEAL_ANCESTRY_EVIDENCE_INVALID"
                ) from exc

            ancestor_status = ancestor.get("preseal_status")
            if (
                ancestor_last.get("checkpoint_manifest_path")
                != ancestor_checkpoint_path
                or ancestor_last.get("checkpoint_manifest_sha256")
                != sha256_bytes(ancestor_bytes)
                or ancestor.get("kind")
                != "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT"
                or ancestor.get("request_id") != ancestor_id
                or ancestor.get("request_sha256")
                != sha256_bytes(ancestor_request_bytes)
                or ancestor_status not in {"BLOCKED", "READY_TO_SEAL"}
                or ancestor_last.get("preseal_status") != ancestor_status
                or ancestor_verification.get("kind")
                != "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_VERIFICATION"
                or ancestor_verification.get("request_id") != ancestor_id
                or ancestor_verification.get("preseal_status") != ancestor_status
                or ancestor_verification.get("remote_stage2_preseal_equivalence")
                != "PASS"
                or ancestor_verification.get("tracked_stage2_mutation") != "NONE"
            ):
                raise Stop("STAGE2_RESUME_PRESEAL_ANCESTRY_EVIDENCE_INVALID")

            preseal_evidence.append((ancestor, ancestor_verification))
            if ancestor_status == "BLOCKED":
                blocked_found = True
                break

            # A READY bridge is evidence only. If any child was ever used or is
            # currently queued, it is not a harmless read-only bridge.
            for child_id in (ancestor_id + "-seal", ancestor_id + "-apply"):
                if (
                    request_used(state, child_id)
                    or _already_queued(control_head, state, child_id)
                ):
                    raise Stop("STAGE2_RESUME_READY_BRIDGE_CHILD_ALREADY_USED")

            ancestry_commit = str(
                ancestor_request.get("previous_control_state_commit") or ""
            )

        if not blocked_found:
            raise Stop("STAGE2_RESUME_PRESEAL_ANCESTRY_BLOCKED_NOT_FOUND")
    else:
        raise Stop("STAGE2_RESUME_ORIGINAL_PRESEAL_NOT_RECOVERABLE")

    identity_fields = (
        "school_key",
        "target_branch",
        "target_sha",
        "target_tree_sha",
        "integration_freeze_sha256",
        "semantic_snapshot_sha256",
        "decision_universe_sha256",
        "recommendation_map_sha256",
        "approved_plan_hash_preview",
        "filled_review_sha256",
        "decision_id_set_sha256",
        "owner_gate_1_approval_sha256",
    )
    for field in identity_fields:
        if (
            fill.get(field) is None
            or fill.get(field) != manifest.get(field)
            or fill_verification.get(field) != fill.get(field)
        ):
            raise Stop("STAGE2_RESUME_HISTORICAL_AUTHORITY_CHANGED:" + field)
        for checkpoint, verification in preseal_evidence:
            if (
                checkpoint.get(field) != fill.get(field)
                or verification.get(field) != checkpoint.get(field)
            ):
                raise Stop("STAGE2_RESUME_HISTORICAL_AUTHORITY_CHANGED:" + field)
        if seal_evidence is not None:
            seal, seal_verification = seal_evidence
            if (
                seal.get(field) != fill.get(field)
                or seal_verification.get(field) != seal.get(field)
            ):
                raise Stop("STAGE2_RESUME_HISTORICAL_AUTHORITY_CHANGED:" + field)

    if apply_writeahead is not None:
        for field in (
            "integration_freeze_sha256",
            "semantic_snapshot_sha256",
            "decision_universe_sha256",
            "recommendation_map_sha256",
            "filled_review_sha256",
            "decision_id_set_sha256",
            "owner_gate_1_approval_sha256",
        ):
            if apply_writeahead.get(field) != fill.get(field):
                raise Stop("STAGE2_RESUME_HISTORICAL_AUTHORITY_CHANGED:" + field)

    if (
        manifest.get("source_gate1_fill_request_id") != fill_id
        or manifest.get("stage2_gate1_fill_checkpoint_path") != fill_ref["path"]
        or manifest.get("stage2_gate1_fill_checkpoint_sha256")
        != fill_ref["sha256"]
        or manifest.get("stage2_gate1_fill_verification_path")
        != fill_verification_ref["path"]
        or manifest.get("stage2_gate1_fill_verification_sha256")
        != fill_verification_ref["sha256"]
        or parent.get("target_branch") != manifest["target_branch"]
        or parent.get("target_sha") != manifest["target_sha"]
        or manifest.get("preseal_status") != "READY_TO_SEAL"
    ):
        raise Stop("STAGE2_RESUME_REPLACEMENT_PRESEAL_BINDING_INVALID")

    # These IDs can never represent a replay of the abandoned original chain.
    preseal_id = parent["request_id"]
    resume = {
        "kind": STAGE2_POST_GATE1_CONTINUATION_KIND,
        "preseal_request_id": preseal_id,
        "seal_request_id": preseal_id + "-seal",
        "apply_request_id": preseal_id + "-apply",
    }
    validate_stage2_phase_continuation(
        OP_STAGE2_PRESEAL_REHEARSAL, preseal_id, resume
    )
    for key in ("seal_request_id", "apply_request_id"):
        if (
            request_used(state, resume[key])
            or _already_queued(control_head, state, resume[key])
        ):
            raise Stop("STAGE2_RESUME_REPLACEMENT_CHILD_ALREADY_USED")
    return resume


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
    parent, parent_bytes = _load_archived_request(control_head, last["request_id"])
    continuation = _continuation_from_parent(parent)
    manifest, checkpoint_ref = _checkpoint_manifest(
        control_head,
        last,
        expected_kind="REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
        label="PRESEAL_CHECKPOINT",
    )
    if continuation is None:
        if manifest.get("request_sha256") != sha256_bytes(parent_bytes):
            raise Stop("STAGE2_RESUME_REPLACEMENT_REQUEST_HASH_MISMATCH")
        if manifest.get("preseal_status") != "READY_TO_SEAL":
            print("STAGE2 CONTINUATION: pre-seal has no phase continuation")
            return 0
        continuation = _resume_post_gate1_from_verified_replacement(
            parent, manifest, control_head=control_head, state=state, last=last
        )
        if continuation is None:
            print("STAGE2 CONTINUATION: no authenticated continuation to resume")
            return 0
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
