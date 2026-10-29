#!/usr/bin/env python3
"""Generic durable control-plane primitives for serialized remote Implementation.

This module owns only control state, request validation, mutation classification,
hash binding, Git-ref CAS publication, and explicit recovery semantics. Basketball
history, reconciliation, Phase 0 staging, and validation remain owned by the
existing permanent repository tools.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

CONTROL_KIND = "REMOTE_IMPLEMENTATION_GLOBAL_CONTROL"
REQUEST_KIND = "REMOTE_IMPLEMENTATION_REQUEST"
CONTROL_SCHEMA_VERSION = 1
REQUEST_SCHEMA_VERSION = 1

OP_STAGE1 = "STAGE1_INVENTORY"
OP_PHASE0 = "PHASE0"
OP_PHASE0_SCOPE_SUPERSESSION = "PHASE0_SCOPE_SUPERSESSION"
OP_STAGE2_CENSUS = "STAGE2_CENSUS"
OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE = "STAGE2_OPPONENT_DISPLAY_NORMALIZE"
OP_STAGE2_PROPOSAL_REHEARSAL = "STAGE2_PROPOSAL_REHEARSAL"
OP_STAGE2_GATE1_FILL = "STAGE2_GATE1_FILL"
OP_STAGE2_PRESEAL_REHEARSAL = "STAGE2_PRESEAL_REHEARSAL"
OP_STAGE2_GATE1_SEAL = "STAGE2_GATE1_SEAL"
OP_STAGE2_SEALED_APPLY = "STAGE2_SEALED_APPLY"
OP_RELEASE_READINESS = "RELEASE_READINESS"
OP_RELEASE_PREVIEW_VERIFY = "RELEASE_PREVIEW_VERIFY"
OP_RELEASE_GATE2_APPROVAL = "RELEASE_GATE2_APPROVAL"
OP_RELEASE_PRODUCTION_PROOF = "RELEASE_PRODUCTION_PROOF"
OP_STAGE2_RECONCILIATION_DIAGNOSTIC = "STAGE2_RECONCILIATION_DIAGNOSTIC"
OP_VENUE_IDENTITY_MAINTENANCE = "VENUE_IDENTITY_MAINTENANCE"
OP_RECOVER = "RECOVER"
SUPPORTED_OPERATIONS = {
    OP_STAGE1,
    OP_PHASE0,
    OP_PHASE0_SCOPE_SUPERSESSION,
    OP_STAGE2_CENSUS,
    OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
    OP_STAGE2_PROPOSAL_REHEARSAL,
    OP_STAGE2_GATE1_FILL,
    OP_STAGE2_PRESEAL_REHEARSAL,
    OP_STAGE2_GATE1_SEAL,
    OP_STAGE2_SEALED_APPLY,
    OP_RELEASE_READINESS,
    OP_RELEASE_PREVIEW_VERIFY,
    OP_RELEASE_GATE2_APPROVAL,
    OP_RELEASE_PRODUCTION_PROOF,
    OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
    OP_VENUE_IDENTITY_MAINTENANCE,
    OP_RECOVER,
}

LIFECYCLE_IDLE = "IDLE"
LIFECYCLE_READ_ONLY = "READ_ONLY_ACTIVE"
LIFECYCLE_ACTIVE = "ACTIVE"

TX_IDLE = "IDLE"
TX_STAGE1_RUNNING = "STAGE1_RUNNING"
TX_STAGE2_CENSUS_RUNNING = "STAGE2_CENSUS_RUNNING"
TX_STAGE2_PROPOSAL_RUNNING = "STAGE2_PROPOSAL_REHEARSAL_RUNNING"
TX_STAGE2_GATE1_FILL_RUNNING = "STAGE2_GATE1_FILL_RUNNING"
TX_STAGE2_PRESEAL_RUNNING = "STAGE2_PRESEAL_REHEARSAL_RUNNING"
TX_STAGE2_GATE1_SEAL_RUNNING = "STAGE2_GATE1_SEAL_RUNNING"
TX_STAGE2_DIAGNOSTIC_RUNNING = "STAGE2_RECONCILIATION_DIAGNOSTIC_RUNNING"
TX_RELEASE_READINESS_RUNNING = "RELEASE_READINESS_RUNNING"
TX_RELEASE_PREVIEW_RUNNING = "RELEASE_PREVIEW_RUNNING"
TX_RELEASE_GATE2_RUNNING = "RELEASE_GATE2_RUNNING"
TX_RELEASE_PRODUCTION_RUNNING = "RELEASE_PRODUCTION_RUNNING"
TX_LOCKED = "LOCKED"
TX_INPUTS_VERIFIED = "INPUTS_VERIFIED"
TX_PREPARED = "PREPARED_NOT_PUBLISHED"
TX_PUBLISHED = "PUBLISHED_NOT_FINALIZED"
TX_COMPLETE = "COMPLETE"
TX_DIVERGED = "DIVERGED_STOP"
TX_ABANDONED_NOT_ATTEMPTED = "ABANDONED_NOT_ATTEMPTED"
TX_ABANDONED_PREPARED = "ABANDONED_PREPARED_NOT_PUBLISHED"

MUTATION_NOT_ATTEMPTED = "NOT_ATTEMPTED"
MUTATION_PREPARED = "PREPARED_NOT_PUBLISHED"
MUTATION_PUBLISHED = "PUBLISHED_NOT_FINALIZED"
MUTATION_COMPLETE = "COMPLETE"
MUTATION_DIVERGED = "DIVERGED_STOP"

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REQUEST_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
SCHOOL_KEY_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,127}$")
CANONICAL_GAME_ID_RE = re.compile(r"^CBBG-[0-9]{1,12}$")


class RemoteImplementationError(RuntimeError):
    """Fail-closed control-plane error."""


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json_bytes(value: bytes) -> dict[str, Any]:
    try:
        doc = json.loads(value)
    except (TypeError, ValueError) as exc:
        raise RemoteImplementationError(f"invalid JSON: {exc}") from exc
    if not isinstance(doc, dict):
        raise RemoteImplementationError("JSON document must be an object")
    return doc


def initial_control_state() -> dict[str, Any]:
    return {
        "schema_version": CONTROL_SCHEMA_VERSION,
        "kind": CONTROL_KIND,
        "lifecycle_state": LIFECYCLE_IDLE,
        "transaction_state": TX_IDLE,
        "current_sequence": 0,
        "accepted_request_ids": [],
        "consumed_request_ids": [],
        "abandoned_request_ids": [],
        "active_request_id": None,
        "active_request_sha256": None,
        "active_school_key": None,
        "active_operation": None,
        "active_expected_main_sha": None,
        "active_lock_owner": None,
        "active_lock_commit": None,
        "active_writeahead_path": None,
        "active_writeahead_sha256": None,
        "active_writeahead_commit": None,
        "active_prepared_commit_sha": None,
        "active_prepared_tree_sha": None,
        "active_target_branch": None,
        "recovery_required": False,
        "last_operation": None,
        "authority_statement": (
            "Global serialized remote Implementation control authority. "
            "This state never supplies Owner Gate 1 or Owner Gate 2 approval."
        ),
    }


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise RemoteImplementationError(code)


def _require_sha(value: Any, length: int, code: str) -> str:
    text = str(value or "").strip().lower()
    pattern = HEX40 if length == 40 else HEX64
    _require(bool(pattern.fullmatch(text)), code)
    return text


def validate_control_state(state: dict[str, Any]) -> None:
    _require(state.get("schema_version") == CONTROL_SCHEMA_VERSION, "CONTROL_SCHEMA_MISMATCH")
    _require(state.get("kind") == CONTROL_KIND, "CONTROL_KIND_MISMATCH")
    _require(
        state.get("lifecycle_state")
        in {LIFECYCLE_IDLE, LIFECYCLE_READ_ONLY, LIFECYCLE_ACTIVE},
        "CONTROL_LIFECYCLE_INVALID",
    )
    _require(
        state.get("transaction_state")
        in {
            TX_IDLE,
            TX_STAGE1_RUNNING,
            TX_STAGE2_CENSUS_RUNNING,
            TX_STAGE2_PROPOSAL_RUNNING,
            TX_STAGE2_GATE1_FILL_RUNNING,
            TX_STAGE2_PRESEAL_RUNNING,
            TX_STAGE2_GATE1_SEAL_RUNNING,
            TX_STAGE2_DIAGNOSTIC_RUNNING,
            TX_RELEASE_READINESS_RUNNING,
            TX_RELEASE_PREVIEW_RUNNING,
            TX_RELEASE_GATE2_RUNNING,
            TX_RELEASE_PRODUCTION_RUNNING,
            TX_LOCKED,
            TX_INPUTS_VERIFIED,
            TX_PREPARED,
            TX_PUBLISHED,
            TX_COMPLETE,
            TX_DIVERGED,
            TX_ABANDONED_NOT_ATTEMPTED,
            TX_ABANDONED_PREPARED,
        },
        "CONTROL_TRANSACTION_STATE_INVALID",
    )
    for key in ("accepted_request_ids", "consumed_request_ids", "abandoned_request_ids"):
        values = state.get(key)
        _require(isinstance(values, list), f"CONTROL_{key.upper()}_INVALID")
        _require(len(values) == len(set(values)), f"CONTROL_{key.upper()}_DUPLICATE")
    # Abandonment is a valid terminal transaction, but only with matching durable
    # RECOVER provenance. It is not an escape hatch for an active control lock.
    abandoned_classifications = {
        TX_ABANDONED_NOT_ATTEMPTED: MUTATION_NOT_ATTEMPTED,
        TX_ABANDONED_PREPARED: MUTATION_PREPARED,
    }
    classification = abandoned_classifications.get(state["transaction_state"])
    if classification is not None:
        _require(
            state["lifecycle_state"] == LIFECYCLE_IDLE,
            "ABANDONED_TRANSACTION_NOT_IDLE",
        )
        last = state.get("last_operation")
        _require(
            isinstance(last, dict)
            and last.get("operation") == OP_RECOVER
            and last.get("disposition") == state["transaction_state"],
            "ABANDONED_TRANSACTION_RECOVERY_DISPOSITION_INVALID",
        )
        recovered_id = last.get("recovered_request_id")
        _require(
            recovered_id in state["abandoned_request_ids"],
            "ABANDONED_TRANSACTION_REQUEST_NOT_RECORDED",
        )
        recovery_manifest = last.get("recovery_manifest")
        _require(
            isinstance(recovery_manifest, dict)
            and recovery_manifest.get("mutation_classification") == classification
            and recovery_manifest.get("recovered_request_id") == recovered_id
            and recovery_manifest.get("request_id") in state["consumed_request_ids"],
            "ABANDONED_TRANSACTION_MANIFEST_INVALID",
        )
    active = state.get("active_request_id")
    if state.get("lifecycle_state") == LIFECYCLE_IDLE:
        _require(active is None, "IDLE_CONTROL_HAS_ACTIVE_REQUEST")
        _require(state.get("active_lock_commit") is None, "IDLE_CONTROL_HAS_ACTIVE_LOCK")
        _require(state.get("recovery_required") is False, "IDLE_CONTROL_REQUIRES_RECOVERY")
    else:
        _require(isinstance(active, str) and bool(active), "ACTIVE_CONTROL_MISSING_REQUEST")


def request_used(state: dict[str, Any], request_id: str) -> bool:
    return (
        request_id == state.get("active_request_id")
        or request_id in set(state.get("accepted_request_ids") or [])
        or request_id in set(state.get("consumed_request_ids") or [])
        or request_id in set(state.get("abandoned_request_ids") or [])
    )


def _validate_transport(transport: Any) -> None:
    _require(isinstance(transport, dict), "REQUEST_TRANSPORT_MISSING")
    _require(transport.get("kind") == "git_base64_parts", "REQUEST_TRANSPORT_KIND_UNSUPPORTED")
    _require_sha(transport.get("commit_sha"), 40, "REQUEST_TRANSPORT_COMMIT_INVALID")
    prefix = str(transport.get("path_prefix") or "").strip()
    _require(bool(prefix) and not prefix.startswith("/"), "REQUEST_TRANSPORT_PREFIX_INVALID")
    part_count = transport.get("part_count")
    _require(isinstance(part_count, int) and part_count >= 1, "REQUEST_TRANSPORT_PART_COUNT_INVALID")


def _validate_payload_ref(value: Any, name: str, *, required: bool = False) -> None:
    if value is None:
        _require(not required, f"REQUEST_{name.upper()}_REQUIRED")
        return
    _require(isinstance(value, dict), f"REQUEST_{name.upper()}_INVALID")
    path = str(value.get("path") or "").strip()
    _require(bool(path) and not path.startswith("/"), f"REQUEST_{name.upper()}_PATH_INVALID")
    _require_sha(value.get("sha256"), 64, f"REQUEST_{name.upper()}_SHA_INVALID")


def validate_request(request: dict[str, Any]) -> None:
    _require(request.get("schema_version") == REQUEST_SCHEMA_VERSION, "REQUEST_SCHEMA_MISMATCH")
    _require(request.get("kind") == REQUEST_KIND, "REQUEST_KIND_MISMATCH")
    request_id = str(request.get("request_id") or "")
    school_key = str(request.get("school_key") or "")
    operation = request.get("operation")
    _require(bool(REQUEST_ID_RE.fullmatch(request_id)), "REQUEST_ID_INVALID")
    _require(bool(SCHOOL_KEY_RE.fullmatch(school_key)), "REQUEST_SCHOOL_KEY_INVALID")
    _require(operation in SUPPORTED_OPERATIONS, "REQUEST_OPERATION_UNSUPPORTED")
    _require_sha(
        request.get("previous_control_state_commit"),
        40,
        "REQUEST_PREDECESSOR_COMMIT_INVALID",
    )
    _require_sha(
        request.get("previous_control_state_sha256"),
        64,
        "REQUEST_PREDECESSOR_STATE_HASH_INVALID",
    )
    _require_sha(
        request.get("expected_protected_main_sha"),
        40,
        "REQUEST_EXPECTED_MAIN_INVALID",
    )

    provenance = request.get("creation_provenance")
    _require(isinstance(provenance, dict), "REQUEST_PROVENANCE_MISSING")
    _require(bool(str(provenance.get("origin") or "").strip()), "REQUEST_PROVENANCE_ORIGIN_MISSING")
    _require(
        bool(str(provenance.get("authorization") or "").strip()),
        "REQUEST_PROVENANCE_AUTHORIZATION_MISSING",
    )

    authority = request.get("authority")
    _require(isinstance(authority, dict), "REQUEST_AUTHORITY_MISSING")
    if operation == OP_STAGE2_GATE1_FILL:
        _require(
            authority.get("owner_gate_1") is True,
            "STAGE2_GATE1_FILL_OWNER_GATE1_AUTHORITY_REQUIRED",
        )
        _require(
            authority.get("stage2_gate1_fill") is True,
            "STAGE2_GATE1_FILL_REQUEST_AUTHORITY_REQUIRED",
        )
    else:
        _require(
            authority.get("owner_gate_1") is False,
            "REQUEST_GATE1_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_gate1_fill") is not True,
            "REQUEST_GATE1_FILL_AUTHORITY_FORBIDDEN",
        )
    if operation == OP_STAGE2_PRESEAL_REHEARSAL:
        _require(
            authority.get("stage2_preseal_rehearsal") is True,
            "STAGE2_PRESEAL_REQUEST_AUTHORITY_REQUIRED",
        )
    else:
        _require(
            authority.get("stage2_preseal_rehearsal") is not True,
            "REQUEST_PRESEAL_AUTHORITY_FORBIDDEN",
        )
    if operation == OP_STAGE2_GATE1_SEAL:
        _require(
            authority.get("stage2_gate1_seal") is True,
            "STAGE2_GATE1_SEAL_REQUEST_AUTHORITY_REQUIRED",
        )
    else:
        _require(
            authority.get("stage2_gate1_seal") is not True,
            "REQUEST_GATE1_SEAL_AUTHORITY_FORBIDDEN",
        )
    if operation == OP_STAGE2_SEALED_APPLY:
        _require(
            authority.get("stage2_sealed_apply") is True,
            "STAGE2_SEALED_APPLY_REQUEST_AUTHORITY_REQUIRED",
        )
    else:
        _require(
            authority.get("stage2_sealed_apply") is not True,
            "REQUEST_SEALED_APPLY_AUTHORITY_FORBIDDEN",
        )
    if operation == OP_RELEASE_GATE2_APPROVAL:
        _require(
            authority.get("owner_gate_2") is True,
            "REQUEST_GATE2_APPROVAL_AUTHORITY_REQUIRED",
        )
    else:
        _require(authority.get("owner_gate_2") is False, "REQUEST_GATE2_AUTHORITY_FORBIDDEN")
    if operation == OP_PHASE0_SCOPE_SUPERSESSION:
        _require(
            authority.get("phase0_scope_supersession") is True,
            "SCOPE_SUPERSESSION_REQUEST_AUTHORITY_REQUIRED",
        )
    else:
        _require(
            authority.get("phase0_scope_supersession") is not True,
            "REQUEST_SCOPE_SUPERSESSION_AUTHORITY_FORBIDDEN",
        )

    if operation == OP_VENUE_IDENTITY_MAINTENANCE:
        _require(
            authority.get("venue_identity_maintenance") is True,
            "VENUE_MAINTENANCE_REQUEST_AUTHORITY_REQUIRED",
        )
    else:
        _require(
            authority.get("venue_identity_maintenance") is not True,
            "REQUEST_VENUE_MAINTENANCE_AUTHORITY_FORBIDDEN",
        )

    # RELEASE_READINESS is inspection and final-gate rehearsal only. No PR,
    # Preview, Owner Gate 2, or merge authority can be supplied by a request.
    _require(authority.get("release") is False, "REQUEST_RELEASE_AUTHORITY_FORBIDDEN")
    if operation == OP_RELEASE_READINESS:
        _require(
            authority.get("release_readiness") is True,
            "RELEASE_READINESS_AUTHORITY_REQUIRED",
        )
    else:
        _require(
            authority.get("release_readiness") is not True,
            "REQUEST_RELEASE_READINESS_AUTHORITY_FORBIDDEN",
        )
    if operation == OP_RELEASE_PREVIEW_VERIFY:
        _require(
            authority.get("release_preview_verify") is True,
            "RELEASE_PREVIEW_VERIFY_AUTHORITY_REQUIRED",
        )
    else:
        _require(
            authority.get("release_preview_verify") is not True,
            "REQUEST_RELEASE_PREVIEW_AUTHORITY_FORBIDDEN",
        )

    if operation in {OP_RELEASE_GATE2_APPROVAL, OP_RELEASE_PRODUCTION_PROOF}:
        flag = (
            "release_gate2_approval"
            if operation == OP_RELEASE_GATE2_APPROVAL
            else "release_production_proof"
        )
        for key in (
            "phase0", "recovery", "stage2_census", "stage2_opponent_display_normalize",
            "stage2_proposal_rehearsal", "stage2_gate1_fill",
            "stage2_preseal_rehearsal", "stage2_gate1_seal", "stage2_sealed_apply",
            "stage2_reconciliation_diagnostic", "release_readiness",
            "release_preview_verify", "release",
        ):
            _require(
                authority.get(key) is False,
                "RELEASE_GATE2_OTHER_AUTHORITY_FORBIDDEN:" + key,
            )
        _require(
            authority.get(flag) is True,
            "RELEASE_GATE2_OPERATION_AUTHORITY_REQUIRED:" + flag,
        )
        other = (
            "release_production_proof"
            if operation == OP_RELEASE_GATE2_APPROVAL
            else "release_gate2_approval"
        )
        _require(
            authority.get(other) is not True,
            "RELEASE_GATE2_CROSS_OPERATION_AUTHORITY_FORBIDDEN",
        )
        _require(
            request.get("target_branch") == f"data/{school_key}-onboarding",
            "RELEASE_GATE2_TARGET_BRANCH_INVALID",
        )
        _require_sha(request.get("target_sha"), 40, "RELEASE_GATE2_TARGET_SHA_INVALID")
        pr_number = request.get("pr_number")
        _require(
            type(pr_number) is int and 0 < pr_number <= 2147483647,
            "RELEASE_GATE2_PR_NUMBER_INVALID",
        )
        if operation == OP_RELEASE_GATE2_APPROVAL:
            for field in ("approved_plan_hash", "release_manifest_sha256"):
                _require_sha(
                    request.get(field), 64,
                    "RELEASE_GATE2_%s_INVALID" % field.upper(),
                )
            for field in ("release_preview_checkpoint", "release_preview_verification"):
                _validate_payload_ref(request.get(field), field, required=True)
            approval = request.get("owner_gate_2_approval")
            _require(
                isinstance(approval, dict) and approval.get("approved") is True,
                "RELEASE_GATE2_EXPLICIT_OWNER_APPROVAL_REQUIRED",
            )
            _require(
                bool(str(approval.get("approval_basis") or "").strip()),
                "RELEASE_GATE2_OWNER_APPROVAL_BASIS_REQUIRED",
            )
            _require(
                type(request.get("preview_deployment_id")) is int
                and request["preview_deployment_id"] > 0,
                "RELEASE_GATE2_PREVIEW_DEPLOYMENT_INVALID",
            )
            _require(
                str(request.get("preview_url") or "").startswith("https://"),
                "RELEASE_GATE2_PREVIEW_URL_INVALID",
            )
            for key in (
                "preview_checkpoint_sha256", "preview_verification_sha256",
            ):
                _require_sha(approval.get(key), 64, "RELEASE_GATE2_APPROVAL_SHA_INVALID")
            for key in (
                "pr_number", "pr_head_sha", "preview_deployment_id", "preview_url",
            ):
                _require(
                    approval.get(key) == request.get(
                        "target_sha" if key == "pr_head_sha" else key
                    ),
                    "RELEASE_GATE2_APPROVAL_SCOPE_MISMATCH:" + key,
                )
            _require(
                approval.get("preview_checkpoint_sha256")
                == request["release_preview_checkpoint"]["sha256"]
                and approval.get("preview_verification_sha256")
                == request["release_preview_verification"]["sha256"],
                "RELEASE_GATE2_APPROVAL_CHECKPOINT_SCOPE_MISMATCH",
            )
        else:
            _require_sha(
                request.get("merge_sha"), 40,
                "RELEASE_PRODUCTION_EXACT_MERGE_SHA_INVALID",
            )
            for field in ("owner_gate_2_checkpoint", "owner_gate_2_verification"):
                _validate_payload_ref(request.get(field), field, required=True)

    if operation == OP_VENUE_IDENTITY_MAINTENANCE:
        for key in (
            "phase0", "recovery", "stage2_census",
            "stage2_opponent_display_normalize", "stage2_proposal_rehearsal",
            "stage2_gate1_fill", "stage2_preseal_rehearsal",
            "stage2_gate1_seal", "stage2_sealed_apply",
            "stage2_reconciliation_diagnostic", "release_readiness",
            "release_preview_verify", "release_gate2_approval",
            "release_production_proof", "release",
        ):
            _require(
                authority.get(key) is not True,
                "VENUE_MAINTENANCE_OTHER_AUTHORITY_FORBIDDEN:" + key,
            )
        target_branch = str(request.get("target_branch") or "").strip()
        _require(
            target_branch.startswith(
                "maintenance/%s-" % school_key
            )
            and ".." not in target_branch
            and not target_branch.endswith("/"),
            "VENUE_MAINTENANCE_TARGET_BRANCH_INVALID",
        )
        _validate_payload_ref(
            request.get("venue_maintenance_spec"),
            "venue_maintenance_spec",
            required=True,
        )
        repository_spec_path = str(
            request.get("repository_spec_path") or ""
        ).strip()
        _require(
            repository_spec_path.startswith(
                "data/reconciliation/venue-identity-maintenance/%s"
                % school_key
            )
            and repository_spec_path.endswith(".json")
            and ".." not in repository_spec_path,
            "VENUE_MAINTENANCE_REPOSITORY_SPEC_PATH_INVALID",
        )
        _require_sha(
            request.get("expected_plan_sha256"),
            64,
            "VENUE_MAINTENANCE_PLAN_SHA_INVALID",
        )
        authorization = request.get("maintenance_authorization")
        _require(
            isinstance(authorization, dict)
            and authorization.get("approved") is True,
            "VENUE_MAINTENANCE_CONTROL_CENTER_APPROVAL_REQUIRED",
        )
        _require(
            authorization.get("authority_kind")
            == "CONTROL_CENTER_EXPLICIT",
            "VENUE_MAINTENANCE_AUTHORITY_KIND_INVALID",
        )
        _require(
            bool(str(
                authorization.get("authorization_basis") or ""
            ).strip()),
            "VENUE_MAINTENANCE_AUTHORIZATION_BASIS_REQUIRED",
        )
        _require(
            authorization.get("spec_sha256")
            == request["venue_maintenance_spec"]["sha256"],
            "VENUE_MAINTENANCE_AUTHORIZATION_SPEC_MISMATCH",
        )

    if operation in {OP_STAGE1, OP_PHASE0, OP_PHASE0_SCOPE_SUPERSESSION}:
        checkpoint = request.get("research_checkpoint")
        _require(isinstance(checkpoint, dict), "REQUEST_RESEARCH_CHECKPOINT_MISSING")
        _require_sha(
            checkpoint.get("sha256"),
            64,
            "REQUEST_RESEARCH_CHECKPOINT_SHA_INVALID",
        )
        _require_sha(
            checkpoint.get("research_base_sha"),
            40,
            "REQUEST_RESEARCH_BASE_INVALID",
        )
        _validate_transport(checkpoint.get("transport"))
        _validate_payload_ref(request.get("venue_reconciliation"), "venue_reconciliation")
        _validate_payload_ref(
            request.get("conference_reconciliation"),
            "conference_reconciliation",
        )

    if operation == OP_STAGE1:
        _require(authority.get("phase0") is False, "STAGE1_REQUEST_PHASE0_AUTHORITY_FORBIDDEN")
        _require(
            authority.get("stage2_census") is not True,
            "STAGE1_REQUEST_STAGE2_CENSUS_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_opponent_display_normalize") is not True,
            "STAGE1_REQUEST_STAGE2_OPPONENT_DISPLAY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_proposal_rehearsal") is not True,
            "STAGE1_REQUEST_STAGE2_PROPOSAL_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_reconciliation_diagnostic") is not True,
            "STAGE1_REQUEST_STAGE2_DIAGNOSTIC_AUTHORITY_FORBIDDEN",
        )

    if operation == OP_PHASE0:
        _require(authority.get("phase0") is True, "PHASE0_REQUEST_AUTHORITY_REQUIRED")
        expected_target = f"data/{school_key}-onboarding"
        _require(request.get("target_branch") == expected_target, "PHASE0_TARGET_BRANCH_INVALID")
        _validate_payload_ref(request.get("stage1_checkpoint"), "stage1_checkpoint", required=True)
        scope = request.get("history_scope")
        _require(isinstance(scope, dict), "REQUEST_HISTORY_SCOPE_MISSING")
        for key in ("start_season", "basis", "notes"):
            _require(
                bool(str(scope.get(key) or "").strip()),
                f"REQUEST_HISTORY_SCOPE_{key.upper()}_MISSING",
            )
        if str(scope.get("basis") or "").strip() == "TOP_LEVEL_INTERVALS":
            _require(
                bool(str(scope.get("intervals") or "").strip()),
                "REQUEST_HISTORY_SCOPE_INTERVALS_MISSING",
            )
        _require(
            authority.get("stage2_census") is not True,
            "PHASE0_REQUEST_STAGE2_CENSUS_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_opponent_display_normalize") is not True,
            "PHASE0_REQUEST_STAGE2_OPPONENT_DISPLAY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_proposal_rehearsal") is not True,
            "PHASE0_REQUEST_STAGE2_PROPOSAL_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_reconciliation_diagnostic") is not True,
            "PHASE0_REQUEST_STAGE2_DIAGNOSTIC_AUTHORITY_FORBIDDEN",
        )

    if operation == OP_PHASE0_SCOPE_SUPERSESSION:
        for key in (
            "phase0", "recovery", "stage2_census",
            "stage2_opponent_display_normalize", "stage2_proposal_rehearsal",
            "stage2_gate1_fill", "stage2_preseal_rehearsal",
            "stage2_gate1_seal", "stage2_sealed_apply",
            "stage2_reconciliation_diagnostic", "release_readiness",
            "release_preview_verify", "release_gate2_approval",
            "release_production_proof", "venue_identity_maintenance", "release",
        ):
            _require(
                authority.get(key) is not True,
                "SCOPE_SUPERSESSION_OTHER_AUTHORITY_FORBIDDEN:" + key,
            )
        expected_target = f"data/{school_key}-onboarding"
        _require(
            request.get("target_branch") == expected_target,
            "SCOPE_SUPERSESSION_TARGET_BRANCH_INVALID",
        )
        _require_sha(
            request.get("target_sha"),
            40,
            "SCOPE_SUPERSESSION_TARGET_SHA_INVALID",
        )
        _validate_payload_ref(
            request.get("scope_supersession_spec"),
            "scope_supersession_spec",
            required=True,
        )
        _validate_payload_ref(
            request.get("superseded_phase0_successor"),
            "superseded_phase0_successor",
            required=True,
        )
        _validate_payload_ref(
            request.get("superseded_successor"),
            "superseded_successor",
            required=True,
        )
        _validate_payload_ref(
            request.get("superseded_successor_verification"),
            "superseded_successor_verification",
            required=True,
        )
        _require_sha(
            request.get("superseded_integration_freeze_sha256"),
            64,
            "SCOPE_SUPERSESSION_OLD_FREEZE_SHA_INVALID",
        )
        _require_sha(
            request.get("superseded_semantic_snapshot_sha256"),
            64,
            "SCOPE_SUPERSESSION_OLD_SEMANTIC_SHA_INVALID",
        )
        scope = request.get("history_scope")
        _require(isinstance(scope, dict), "REQUEST_HISTORY_SCOPE_MISSING")
        for key in ("start_season", "basis", "notes"):
            _require(
                bool(str(scope.get(key) or "").strip()),
                f"REQUEST_HISTORY_SCOPE_{key.upper()}_MISSING",
            )
        if str(scope.get("basis") or "").strip() == "TOP_LEVEL_INTERVALS":
            _require(
                bool(str(scope.get("intervals") or "").strip()),
                "REQUEST_HISTORY_SCOPE_INTERVALS_MISSING",
            )
        authorization = request.get("scope_supersession_authorization")
        _require(
            isinstance(authorization, dict)
            and authorization.get("approved") is True,
            "SCOPE_SUPERSESSION_CONTROL_CENTER_APPROVAL_REQUIRED",
        )
        _require(
            authorization.get("authority_kind") == "CONTROL_CENTER_EXPLICIT",
            "SCOPE_SUPERSESSION_AUTHORITY_KIND_INVALID",
        )
        _require(
            bool(str(authorization.get("authorization_basis") or "").strip()),
            "SCOPE_SUPERSESSION_AUTHORIZATION_BASIS_REQUIRED",
        )
        _require(
            authorization.get("spec_sha256")
            == request["scope_supersession_spec"]["sha256"],
            "SCOPE_SUPERSESSION_AUTHORIZATION_SPEC_MISMATCH",
        )
        _require(
            request.get("venue_reconciliation") is None
            and request.get("conference_reconciliation") is None,
            "SCOPE_SUPERSESSION_RECONCILIATION_PAYLOAD_FORBIDDEN",
        )

    if operation == OP_STAGE2_CENSUS:
        _require(
            authority.get("stage2_census") is True,
            "STAGE2_CENSUS_REQUEST_AUTHORITY_REQUIRED",
        )
        _require(
            authority.get("phase0") is False,
            "STAGE2_CENSUS_PHASE0_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("recovery") is False,
            "STAGE2_CENSUS_RECOVERY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_opponent_display_normalize") is not True,
            "STAGE2_CENSUS_OPPONENT_DISPLAY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_proposal_rehearsal") is not True,
            "STAGE2_CENSUS_PROPOSAL_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_reconciliation_diagnostic") is not True,
            "STAGE2_CENSUS_DIAGNOSTIC_AUTHORITY_FORBIDDEN",
        )
        expected_target = f"data/{school_key}-onboarding"
        _require(
            request.get("target_branch") == expected_target,
            "STAGE2_CENSUS_TARGET_BRANCH_INVALID",
        )
        _require_sha(
            request.get("target_sha"),
            40,
            "STAGE2_CENSUS_TARGET_SHA_INVALID",
        )
        _validate_payload_ref(
            request.get("phase0_successor"),
            "phase0_successor",
            required=True,
        )
        _require_sha(
            request.get("integration_freeze_sha256"),
            64,
            "STAGE2_CENSUS_INTEGRATION_FREEZE_SHA_INVALID",
        )
        _require_sha(
            request.get("semantic_snapshot_sha256"),
            64,
            "STAGE2_CENSUS_SEMANTIC_SNAPSHOT_SHA_INVALID",
        )

    if operation == OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE:
        _require(
            authority.get("stage2_opponent_display_normalize") is True,
            "STAGE2_OPPONENT_DISPLAY_REQUEST_AUTHORITY_REQUIRED",
        )
        _require(
            authority.get("phase0") is False,
            "STAGE2_OPPONENT_DISPLAY_PHASE0_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("recovery") is False,
            "STAGE2_OPPONENT_DISPLAY_RECOVERY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_census") is False,
            "STAGE2_OPPONENT_DISPLAY_CENSUS_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_proposal_rehearsal") is not True,
            "STAGE2_OPPONENT_DISPLAY_PROPOSAL_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_reconciliation_diagnostic") is not True,
            "STAGE2_OPPONENT_DISPLAY_DIAGNOSTIC_AUTHORITY_FORBIDDEN",
        )
        expected_target = f"data/{school_key}-onboarding"
        _require(
            request.get("target_branch") == expected_target,
            "STAGE2_OPPONENT_DISPLAY_TARGET_BRANCH_INVALID",
        )
        _require_sha(
            request.get("target_sha"),
            40,
            "STAGE2_OPPONENT_DISPLAY_TARGET_SHA_INVALID",
        )
        _validate_payload_ref(
            request.get("stage2_census_checkpoint"),
            "stage2_census_checkpoint",
            required=True,
        )
        _require_sha(
            request.get("integration_freeze_sha256"),
            64,
            "STAGE2_OPPONENT_DISPLAY_INTEGRATION_FREEZE_SHA_INVALID",
        )
        _require_sha(
            request.get("semantic_snapshot_sha256"),
            64,
            "STAGE2_OPPONENT_DISPLAY_SEMANTIC_SNAPSHOT_SHA_INVALID",
        )

    if operation == OP_STAGE2_PROPOSAL_REHEARSAL:
        _require(
            authority.get("stage2_proposal_rehearsal") is True,
            "STAGE2_PROPOSAL_REQUEST_AUTHORITY_REQUIRED",
        )
        _require(
            authority.get("phase0") is False,
            "STAGE2_PROPOSAL_PHASE0_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("recovery") is False,
            "STAGE2_PROPOSAL_RECOVERY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_census") is False,
            "STAGE2_PROPOSAL_CENSUS_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_opponent_display_normalize") is False,
            "STAGE2_PROPOSAL_OPPONENT_DISPLAY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_reconciliation_diagnostic") is not True,
            "STAGE2_PROPOSAL_DIAGNOSTIC_AUTHORITY_FORBIDDEN",
        )
        expected_target = f"data/{school_key}-onboarding"
        _require(
            request.get("target_branch") == expected_target,
            "STAGE2_PROPOSAL_TARGET_BRANCH_INVALID",
        )
        _require_sha(
            request.get("target_sha"),
            40,
            "STAGE2_PROPOSAL_TARGET_SHA_INVALID",
        )
        _validate_payload_ref(
            request.get("stage2_authority"),
            "stage2_authority",
            required=True,
        )
        _validate_payload_ref(
            request.get("recommendation_map"),
            "recommendation_map",
            required=True,
        )
        _require_sha(
            request.get("integration_freeze_sha256"),
            64,
            "STAGE2_PROPOSAL_INTEGRATION_FREEZE_SHA_INVALID",
        )
        _require_sha(
            request.get("semantic_snapshot_sha256"),
            64,
            "STAGE2_PROPOSAL_SEMANTIC_SNAPSHOT_SHA_INVALID",
        )
        _require_sha(
            request.get("decision_universe_sha256"),
            64,
            "STAGE2_PROPOSAL_DECISION_UNIVERSE_SHA_INVALID",
        )


    if operation == OP_STAGE2_GATE1_FILL:
        _require(
            authority.get("phase0") is False,
            "STAGE2_GATE1_FILL_PHASE0_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("recovery") is False,
            "STAGE2_GATE1_FILL_RECOVERY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_census") is False,
            "STAGE2_GATE1_FILL_CENSUS_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_opponent_display_normalize") is False,
            "STAGE2_GATE1_FILL_OPPONENT_DISPLAY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_proposal_rehearsal") is False,
            "STAGE2_GATE1_FILL_PROPOSAL_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_reconciliation_diagnostic") is False,
            "STAGE2_GATE1_FILL_DIAGNOSTIC_AUTHORITY_FORBIDDEN",
        )
        expected_target = f"data/{school_key}-onboarding"
        _require(
            request.get("target_branch") == expected_target,
            "STAGE2_GATE1_FILL_TARGET_BRANCH_INVALID",
        )
        _require_sha(
            request.get("target_sha"),
            40,
            "STAGE2_GATE1_FILL_TARGET_SHA_INVALID",
        )
        _validate_payload_ref(
            request.get("stage2_proposal_checkpoint"),
            "stage2_proposal_checkpoint",
            required=True,
        )
        _validate_payload_ref(
            request.get("stage2_proposal_verification"),
            "stage2_proposal_verification",
            required=True,
        )
        for field, code in (
            ("integration_freeze_sha256", "INTEGRATION_FREEZE"),
            ("semantic_snapshot_sha256", "SEMANTIC_SNAPSHOT"),
            ("decision_universe_sha256", "DECISION_UNIVERSE"),
            ("recommendation_map_sha256", "RECOMMENDATION_MAP"),
            ("approved_plan_hash_preview", "APPROVED_PLAN_PREVIEW"),
        ):
            _require_sha(
                request.get(field),
                64,
                f"STAGE2_GATE1_FILL_{code}_SHA_INVALID",
            )
        approval = request.get("owner_gate_1_approval")
        _require(
            isinstance(approval, dict),
            "STAGE2_GATE1_FILL_OWNER_APPROVAL_MISSING",
        )
        _require(
            approval.get("approved") is True,
            "STAGE2_GATE1_FILL_OWNER_APPROVAL_REQUIRED",
        )
        _require(
            bool(str(approval.get("approval_basis") or "").strip()),
            "STAGE2_GATE1_FILL_OWNER_APPROVAL_BASIS_MISSING",
        )
        expected_approval_bindings = {
            "proposal_checkpoint_sha256": request["stage2_proposal_checkpoint"]["sha256"],
            "decision_universe_sha256": request["decision_universe_sha256"],
            "recommendation_map_sha256": request["recommendation_map_sha256"],
            "approved_plan_hash_preview": request["approved_plan_hash_preview"],
        }
        for field, expected in expected_approval_bindings.items():
            _require(
                approval.get(field) == expected,
                f"STAGE2_GATE1_FILL_OWNER_APPROVAL_BINDING_MISMATCH:{field}",
            )


    if operation == OP_STAGE2_PRESEAL_REHEARSAL:
        _require(
            authority.get("phase0") is False,
            "STAGE2_PRESEAL_PHASE0_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("recovery") is False,
            "STAGE2_PRESEAL_RECOVERY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_census") is False,
            "STAGE2_PRESEAL_CENSUS_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_opponent_display_normalize") is False,
            "STAGE2_PRESEAL_OPPONENT_DISPLAY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_proposal_rehearsal") is False,
            "STAGE2_PRESEAL_PROPOSAL_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_gate1_fill") is False,
            "STAGE2_PRESEAL_GATE1_FILL_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_reconciliation_diagnostic") is False,
            "STAGE2_PRESEAL_DIAGNOSTIC_AUTHORITY_FORBIDDEN",
        )
        expected_target = f"data/{school_key}-onboarding"
        _require(
            request.get("target_branch") == expected_target,
            "STAGE2_PRESEAL_TARGET_BRANCH_INVALID",
        )
        _require_sha(
            request.get("target_sha"),
            40,
            "STAGE2_PRESEAL_TARGET_SHA_INVALID",
        )
        _validate_payload_ref(
            request.get("stage2_gate1_fill_checkpoint"),
            "stage2_gate1_fill_checkpoint",
            required=True,
        )
        _validate_payload_ref(
            request.get("stage2_gate1_fill_verification"),
            "stage2_gate1_fill_verification",
            required=True,
        )
        for field, code in (
            ("integration_freeze_sha256", "INTEGRATION_FREEZE"),
            ("semantic_snapshot_sha256", "SEMANTIC_SNAPSHOT"),
            ("decision_universe_sha256", "DECISION_UNIVERSE"),
            ("recommendation_map_sha256", "RECOMMENDATION_MAP"),
            ("approved_plan_hash_preview", "APPROVED_PLAN_PREVIEW"),
            ("filled_review_sha256", "FILLED_REVIEW"),
            ("decision_id_set_sha256", "DECISION_ID_SET"),
        ):
            _require_sha(
                request.get(field),
                64,
                f"STAGE2_PRESEAL_{code}_SHA_INVALID",
            )


    if operation == OP_STAGE2_GATE1_SEAL:
        for key, code in (
            ("phase0", "PHASE0"),
            ("recovery", "RECOVERY"),
            ("stage2_census", "CENSUS"),
            ("stage2_opponent_display_normalize", "OPPONENT_DISPLAY"),
            ("stage2_proposal_rehearsal", "PROPOSAL"),
            ("stage2_gate1_fill", "GATE1_FILL"),
            ("stage2_preseal_rehearsal", "PRESEAL"),
            ("stage2_reconciliation_diagnostic", "DIAGNOSTIC"),
        ):
            _require(
                authority.get(key) is False,
                f"STAGE2_GATE1_SEAL_{code}_AUTHORITY_FORBIDDEN",
            )
        expected_target = f"data/{school_key}-onboarding"
        _require(
            request.get("target_branch") == expected_target,
            "STAGE2_GATE1_SEAL_TARGET_BRANCH_INVALID",
        )
        _require_sha(
            request.get("target_sha"),
            40,
            "STAGE2_GATE1_SEAL_TARGET_SHA_INVALID",
        )
        _validate_payload_ref(
            request.get("stage2_preseal_checkpoint"),
            "stage2_preseal_checkpoint",
            required=True,
        )
        _validate_payload_ref(
            request.get("stage2_preseal_verification"),
            "stage2_preseal_verification",
            required=True,
        )
        for field, code in (
            ("integration_freeze_sha256", "INTEGRATION_FREEZE"),
            ("semantic_snapshot_sha256", "SEMANTIC_SNAPSHOT"),
            ("decision_universe_sha256", "DECISION_UNIVERSE"),
            ("recommendation_map_sha256", "RECOMMENDATION_MAP"),
            ("approved_plan_hash_preview", "APPROVED_PLAN_PREVIEW"),
            ("filled_review_sha256", "FILLED_REVIEW"),
            ("decision_id_set_sha256", "DECISION_ID_SET"),
            ("owner_gate_1_approval_sha256", "OWNER_APPROVAL"),
            ("equivalence_sha256", "PRESEAL_EQUIVALENCE"),
        ):
            _require_sha(
                request.get(field),
                64,
                f"STAGE2_GATE1_SEAL_{code}_SHA_INVALID",
            )


    if operation == OP_STAGE2_SEALED_APPLY:
        for key, code in (
            ("phase0", "PHASE0"),
            ("recovery", "RECOVERY"),
            ("stage2_census", "CENSUS"),
            ("stage2_opponent_display_normalize", "OPPONENT_DISPLAY"),
            ("stage2_proposal_rehearsal", "PROPOSAL"),
            ("stage2_gate1_fill", "GATE1_FILL"),
            ("stage2_preseal_rehearsal", "PRESEAL"),
            ("stage2_gate1_seal", "GATE1_SEAL"),
            ("stage2_reconciliation_diagnostic", "DIAGNOSTIC"),
        ):
            _require(
                authority.get(key) is False,
                f"STAGE2_SEALED_APPLY_{code}_AUTHORITY_FORBIDDEN",
            )
        expected_target = f"data/{school_key}-onboarding"
        _require(
            request.get("target_branch") == expected_target,
            "STAGE2_SEALED_APPLY_TARGET_BRANCH_INVALID",
        )
        _require_sha(
            request.get("target_sha"),
            40,
            "STAGE2_SEALED_APPLY_TARGET_SHA_INVALID",
        )
        _validate_payload_ref(
            request.get("stage2_gate1_seal_checkpoint"),
            "stage2_gate1_seal_checkpoint",
            required=True,
        )
        _validate_payload_ref(
            request.get("stage2_gate1_seal_verification"),
            "stage2_gate1_seal_verification",
            required=True,
        )
        for field, code in (
            ("approved_plan_hash", "APPROVED_PLAN"),
            ("approved_plan_sha256", "APPROVED_PLAN_FILE"),
            ("owner_gate_1_approval_sha256", "OWNER_APPROVAL"),
            ("integration_freeze_sha256", "INTEGRATION_FREEZE"),
            ("semantic_snapshot_sha256", "SEMANTIC_SNAPSHOT"),
            ("decision_universe_sha256", "DECISION_UNIVERSE"),
            ("recommendation_map_sha256", "RECOMMENDATION_MAP"),
            ("filled_review_sha256", "FILLED_REVIEW"),
            ("decision_id_set_sha256", "DECISION_ID_SET"),
        ):
            _require_sha(
                request.get(field),
                64,
                f"STAGE2_SEALED_APPLY_{code}_SHA_INVALID",
            )


    if operation == OP_RELEASE_READINESS:
        for key in (
            "phase0", "recovery", "stage2_census",
            "stage2_opponent_display_normalize", "stage2_proposal_rehearsal",
            "stage2_gate1_fill", "stage2_preseal_rehearsal",
            "stage2_gate1_seal", "stage2_sealed_apply",
            "stage2_reconciliation_diagnostic",
        ):
            _require(
                authority.get(key) is False,
                "RELEASE_READINESS_OTHER_AUTHORITY_FORBIDDEN:" + key,
            )
        _require(
            request.get("target_branch") == f"data/{school_key}-onboarding",
            "RELEASE_READINESS_TARGET_BRANCH_INVALID",
        )
        _require_sha(
            request.get("target_sha"), 40, "RELEASE_READINESS_TARGET_SHA_INVALID"
        )
        _validate_payload_ref(
            request.get("stage2_apply_successor"),
            "stage2_apply_successor",
            required=True,
        )
        _validate_payload_ref(
            request.get("stage2_apply_verification"),
            "stage2_apply_verification",
            required=True,
        )
        for key in ("approved_plan_hash", "release_manifest_sha256"):
            _require_sha(
                request.get(key), 64,
                "RELEASE_READINESS_%s_INVALID" % key.upper(),
            )

    if operation == OP_RELEASE_PREVIEW_VERIFY:
        for key in (
            "phase0", "recovery", "stage2_census",
            "stage2_opponent_display_normalize", "stage2_proposal_rehearsal",
            "stage2_gate1_fill", "stage2_preseal_rehearsal",
            "stage2_gate1_seal", "stage2_sealed_apply",
            "stage2_reconciliation_diagnostic", "release_readiness",
        ):
            _require(
                authority.get(key) is False,
                "RELEASE_PREVIEW_OTHER_AUTHORITY_FORBIDDEN:" + key,
            )
        _require(
            request.get("target_branch") == f"data/{school_key}-onboarding",
            "RELEASE_PREVIEW_TARGET_BRANCH_INVALID",
        )
        _require_sha(request.get("target_sha"), 40, "RELEASE_PREVIEW_TARGET_SHA_INVALID")
        _validate_payload_ref(
            request.get("release_readiness_checkpoint"),
            "release_readiness_checkpoint", required=True,
        )
        _validate_payload_ref(
            request.get("release_readiness_verification"),
            "release_readiness_verification", required=True,
        )
        for key in ("approved_plan_hash", "release_manifest_sha256"):
            _require_sha(
                request.get(key), 64,
                "RELEASE_PREVIEW_%s_INVALID" % key.upper(),
            )
        pr_number = request.get("pr_number")
        _require(
            isinstance(pr_number, int) and 1 <= pr_number <= 2147483647,
            "RELEASE_PREVIEW_PR_NUMBER_INVALID",
        )

    if operation == OP_STAGE2_RECONCILIATION_DIAGNOSTIC:
        _require(
            authority.get("stage2_reconciliation_diagnostic") is True,
            "STAGE2_DIAGNOSTIC_REQUEST_AUTHORITY_REQUIRED",
        )
        _require(
            authority.get("phase0") is False,
            "STAGE2_DIAGNOSTIC_PHASE0_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("recovery") is False,
            "STAGE2_DIAGNOSTIC_RECOVERY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_census") is False,
            "STAGE2_DIAGNOSTIC_CENSUS_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_opponent_display_normalize") is False,
            "STAGE2_DIAGNOSTIC_OPPONENT_DISPLAY_AUTHORITY_FORBIDDEN",
        )
        _require(
            authority.get("stage2_proposal_rehearsal") is False,
            "STAGE2_DIAGNOSTIC_PROPOSAL_AUTHORITY_FORBIDDEN",
        )
        expected_target = f"data/{school_key}-onboarding"
        _require(
            request.get("target_branch") == expected_target,
            "STAGE2_DIAGNOSTIC_TARGET_BRANCH_INVALID",
        )
        _require_sha(
            request.get("target_sha"),
            40,
            "STAGE2_DIAGNOSTIC_TARGET_SHA_INVALID",
        )
        _validate_payload_ref(
            request.get("stage2_proposal_checkpoint"),
            "stage2_proposal_checkpoint",
            required=True,
        )
        _require_sha(
            request.get("integration_freeze_sha256"),
            64,
            "STAGE2_DIAGNOSTIC_INTEGRATION_FREEZE_SHA_INVALID",
        )
        _require_sha(
            request.get("semantic_snapshot_sha256"),
            64,
            "STAGE2_DIAGNOSTIC_SEMANTIC_SNAPSHOT_SHA_INVALID",
        )
        _require_sha(
            request.get("decision_universe_sha256"),
            64,
            "STAGE2_DIAGNOSTIC_DECISION_UNIVERSE_SHA_INVALID",
        )
        _require_sha(
            request.get("recommendation_map_sha256"),
            64,
            "STAGE2_DIAGNOSTIC_RECOMMENDATION_MAP_SHA_INVALID",
        )
        _require(
            bool(
                CANONICAL_GAME_ID_RE.fullmatch(
                    str(request.get("canonical_game_id") or "")
                )
            ),
            "STAGE2_DIAGNOSTIC_CANONICAL_GAME_ID_INVALID",
        )

    if operation == OP_RECOVER:
        _require(authority.get("recovery") is True, "RECOVERY_REQUEST_AUTHORITY_REQUIRED")
        recovery = request.get("recovery")
        _require(isinstance(recovery, dict), "RECOVERY_REQUEST_DETAILS_MISSING")
        _require(
            bool(REQUEST_ID_RE.fullmatch(str(recovery.get("abandoned_request_id") or ""))),
            "RECOVERY_REQUEST_ABANDONED_ID_INVALID",
        )
        lock_commit = recovery.get("lock_commit")
        if lock_commit is not None:
            _require_sha(lock_commit, 40, "RECOVERY_REQUEST_LOCK_COMMIT_INVALID")
        target = recovery.get("target_branch")
        if target is not None:
            target_text = str(target)
            _require(
                target_text == f"data/{school_key}-onboarding"
                or (
                    target_text.startswith(f"maintenance/{school_key}-")
                    and ".." not in target_text
                    and not target_text.endswith("/")
                ),
                "RECOVERY_TARGET_BRANCH_INVALID",
            )


def verify_request_predecessor(
    state: dict[str, Any],
    state_bytes: bytes,
    state_commit: str,
    request: dict[str, Any],
    live_main_sha: str,
    *,
    allow_active_recovery: bool = False,
) -> None:
    validate_control_state(state)
    validate_request(request)
    _require(
        request["previous_control_state_commit"] == state_commit,
        "STALE_CONTROL_PREDECESSOR",
    )
    _require(
        request["previous_control_state_sha256"] == sha256_bytes(state_bytes),
        "STALE_CONTROL_STATE_HASH",
    )
    _require(
        request["expected_protected_main_sha"] == live_main_sha,
        "CHANGED_PROTECTED_MAIN",
    )
    request_id = request["request_id"]
    _require(not request_used(state, request_id), "REQUEST_REPLAY_REFUSED")
    if request["operation"] == OP_RECOVER and allow_active_recovery:
        _require(
            state.get("lifecycle_state") in {LIFECYCLE_ACTIVE, LIFECYCLE_READ_ONLY},
            "STALE_RECOVERY_NO_ACTIVE_REQUEST",
        )
        recovery = request["recovery"]
        _require(
            state.get("active_request_id") == recovery["abandoned_request_id"],
            "STALE_RECOVERY_REQUEST_MISMATCH",
        )
        _require(
            state.get("active_lock_commit") == recovery.get("lock_commit"),
            "STALE_RECOVERY_LOCK_MISMATCH",
        )
        if state.get("active_operation") == OP_VENUE_IDENTITY_MAINTENANCE:
            _require(
                recovery.get("target_branch")
                == state.get("active_target_branch"),
                "STALE_RECOVERY_TARGET_MISMATCH",
            )
        elif state.get("active_operation") in {
            OP_PHASE0,
            OP_PHASE0_SCOPE_SUPERSESSION,
            OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
            OP_STAGE2_SEALED_APPLY,
        }:
            _require(
                recovery.get("target_branch")
                == f"data/{state.get('active_school_key')}-onboarding",
                "STALE_RECOVERY_TARGET_MISMATCH",
            )
        elif state.get("active_operation") in {
            OP_STAGE1,
            OP_STAGE2_CENSUS,
            OP_STAGE2_PROPOSAL_REHEARSAL,
            OP_STAGE2_GATE1_FILL,
            OP_STAGE2_PRESEAL_REHEARSAL,
            OP_STAGE2_GATE1_SEAL,
            OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
            OP_RELEASE_READINESS,
            OP_RELEASE_PREVIEW_VERIFY,
            OP_RELEASE_GATE2_APPROVAL,
            OP_RELEASE_PRODUCTION_PROOF,
        }:
            _require(
                recovery.get("target_branch") is None
                and recovery.get("lock_commit") is None,
                "STALE_READ_ONLY_RECOVERY_BOUNDARY_MISMATCH",
            )
        _require(state.get("recovery_required") is True, "STALE_RECOVERY_NOT_REQUIRED")
    else:
        _require(state.get("lifecycle_state") == LIFECYCLE_IDLE, "GLOBAL_IMPLEMENTATION_LOCK_OCCUPIED")


def begin_request(
    state: dict[str, Any],
    request: dict[str, Any],
    request_sha256: str,
    *,
    run_id: str,
    run_attempt: str,
    request_commit: str,
) -> dict[str, Any]:
    validate_control_state(state)
    _require(state["lifecycle_state"] == LIFECYCLE_IDLE, "GLOBAL_IMPLEMENTATION_LOCK_OCCUPIED")
    _require(not request_used(state, request["request_id"]), "REQUEST_REPLAY_REFUSED")
    result = copy.deepcopy(state)
    result["accepted_request_ids"].append(request["request_id"])
    result["active_request_id"] = request["request_id"]
    result["active_request_sha256"] = request_sha256
    result["active_school_key"] = request["school_key"]
    result["active_operation"] = request["operation"]
    result["active_expected_main_sha"] = request["expected_protected_main_sha"]
    result["lock_acquired_run_id"] = str(run_id)
    result["lock_acquired_run_attempt"] = str(run_attempt)
    result["lock_acquisition_request_commit"] = request_commit
    if request["operation"] in {
        OP_STAGE1,
        OP_STAGE2_CENSUS,
        OP_STAGE2_PROPOSAL_REHEARSAL,
        OP_STAGE2_GATE1_FILL,
        OP_STAGE2_PRESEAL_REHEARSAL,
        OP_STAGE2_GATE1_SEAL,
        OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
        OP_RELEASE_READINESS,
        OP_RELEASE_PREVIEW_VERIFY,
        OP_RELEASE_GATE2_APPROVAL,
        OP_RELEASE_PRODUCTION_PROOF,
    }:
        result["lifecycle_state"] = LIFECYCLE_READ_ONLY
        if request["operation"] == OP_STAGE1:
            result["transaction_state"] = TX_STAGE1_RUNNING
        elif request["operation"] == OP_STAGE2_CENSUS:
            result["transaction_state"] = TX_STAGE2_CENSUS_RUNNING
        elif request["operation"] == OP_STAGE2_PROPOSAL_REHEARSAL:
            result["transaction_state"] = TX_STAGE2_PROPOSAL_RUNNING
        elif request["operation"] == OP_STAGE2_GATE1_FILL:
            result["transaction_state"] = TX_STAGE2_GATE1_FILL_RUNNING
        elif request["operation"] == OP_STAGE2_PRESEAL_REHEARSAL:
            result["transaction_state"] = TX_STAGE2_PRESEAL_RUNNING
        elif request["operation"] == OP_STAGE2_GATE1_SEAL:
            result["transaction_state"] = TX_STAGE2_GATE1_SEAL_RUNNING
        elif request["operation"] == OP_RELEASE_READINESS:
            result["transaction_state"] = TX_RELEASE_READINESS_RUNNING
        elif request["operation"] == OP_RELEASE_PREVIEW_VERIFY:
            result["transaction_state"] = TX_RELEASE_PREVIEW_RUNNING
        elif request["operation"] == OP_RELEASE_GATE2_APPROVAL:
            result["transaction_state"] = TX_RELEASE_GATE2_RUNNING
        elif request["operation"] == OP_RELEASE_PRODUCTION_PROOF:
            result["transaction_state"] = TX_RELEASE_PRODUCTION_RUNNING
        else:
            result["transaction_state"] = TX_STAGE2_DIAGNOSTIC_RUNNING
        result["active_lock_owner"] = None
        result["active_target_branch"] = request.get("target_branch")
        result["recovery_required"] = True
    else:
        result["lifecycle_state"] = LIFECYCLE_ACTIVE
        result["transaction_state"] = TX_LOCKED
        result["active_lock_owner"] = f"github-actions:{run_id}:{run_attempt}"
        result["active_target_branch"] = request.get("target_branch")
        result["recovery_required"] = True
    return result


def bind_lock_commit(state: dict[str, Any], lock_commit: str) -> dict[str, Any]:
    result = copy.deepcopy(state)
    _require(result.get("lifecycle_state") == LIFECYCLE_ACTIVE, "LOCK_BIND_WITHOUT_ACTIVE_MUTATION")
    result["active_lock_commit"] = _require_sha(lock_commit, 40, "LOCK_COMMIT_INVALID")
    return result


def clear_active(state: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(state)
    for key in (
        "active_request_id",
        "active_request_sha256",
        "active_school_key",
        "active_operation",
        "active_expected_main_sha",
        "active_lock_owner",
        "active_lock_commit",
        "active_writeahead_path",
        "active_writeahead_sha256",
        "active_writeahead_commit",
        "active_prepared_commit_sha",
        "active_prepared_tree_sha",
        "active_target_branch",
    ):
        result[key] = None
    for key in (
        "lock_acquired_run_id",
        "lock_acquired_run_attempt",
        "lock_acquisition_request_commit",
    ):
        result.pop(key, None)
    result["lifecycle_state"] = LIFECYCLE_IDLE
    result["recovery_required"] = False
    return result


def finalize_success(
    state: dict[str, Any],
    *,
    request_id: str,
    last_operation: dict[str, Any],
    transaction_state: str = TX_COMPLETE,
) -> dict[str, Any]:
    result = copy.deepcopy(state)
    _require(result.get("active_request_id") == request_id, "FINALIZE_REQUEST_MISMATCH")
    if request_id not in result["consumed_request_ids"]:
        result["consumed_request_ids"].append(request_id)
    result["current_sequence"] = int(result.get("current_sequence", 0)) + 1
    result["last_operation"] = copy.deepcopy(last_operation)
    result = clear_active(result)
    result["transaction_state"] = transaction_state
    return result


def abandon_active(
    state: dict[str, Any],
    *,
    recovery_request_id: str,
    disposition: str,
    recovery_manifest: dict[str, Any],
) -> dict[str, Any]:
    result = copy.deepcopy(state)
    active = result.get("active_request_id")
    _require(bool(active), "RECOVERY_NO_ACTIVE_REQUEST")
    if active not in result["abandoned_request_ids"]:
        result["abandoned_request_ids"].append(active)
    if recovery_request_id not in result["consumed_request_ids"]:
        result["consumed_request_ids"].append(recovery_request_id)
    result["current_sequence"] = int(result.get("current_sequence", 0)) + 1
    result["last_operation"] = {
        "operation": OP_RECOVER,
        "recovered_request_id": active,
        "disposition": disposition,
        "recovery_manifest": recovery_manifest,
    }
    result = clear_active(result)
    result["transaction_state"] = disposition
    validate_control_state(result)
    return result


def verify_sidecar_hashes(manifest: dict[str, Any], bundle_dir: Path) -> None:
    sidecars = manifest.get("sidecars")
    _require(isinstance(sidecars, dict) and bool(sidecars), "WRITEAHEAD_SIDECARS_MISSING")
    for relative, expected in sidecars.items():
        _require_sha(expected, 64, "WRITEAHEAD_SIDECAR_SHA_INVALID")
        path = bundle_dir / relative
        _require(path.is_file(), f"WRITEAHEAD_SIDECAR_MISSING:{relative}")
        _require(sha256_file(path) == expected, f"WRITEAHEAD_SIDECAR_HASH_MISMATCH:{relative}")


def classify_mutation(
    expected_predecessor: str | None,
    actual_target: str | None,
    *,
    manifest: dict[str, Any] | None = None,
    successor: dict[str, Any] | None = None,
) -> str:
    if manifest is None:
        if actual_target == expected_predecessor:
            return MUTATION_NOT_ATTEMPTED
        return MUTATION_DIVERGED

    _require(
        manifest.get("expected_target_predecessor_sha") == expected_predecessor,
        "WRITEAHEAD_PREDECESSOR_MISMATCH",
    )
    prepared = _require_sha(
        manifest.get("prepared_commit_sha"),
        40,
        "WRITEAHEAD_PREPARED_COMMIT_INVALID",
    )
    if actual_target == expected_predecessor:
        return MUTATION_PREPARED
    if actual_target == prepared:
        if successor is not None:
            if (
                successor.get("prepared_commit_sha") == prepared
                and successor.get("actual_published_target_sha") == actual_target
                and successor.get("final_transaction_state") == TX_COMPLETE
            ):
                return MUTATION_COMPLETE
        return MUTATION_PUBLISHED
    return MUTATION_DIVERGED


def classify_publication_precondition(
    *,
    expected_predecessor: str | None,
    actual_target: str | None,
    prepared_commit: str,
) -> str:
    _require_sha(prepared_commit, 40, "PREPARED_COMMIT_INVALID")
    if actual_target == expected_predecessor:
        return "PUBLICATION_ALLOWED"
    if actual_target == prepared_commit:
        return "ALREADY_PUBLISHED_EXACT"
    return MUTATION_DIVERGED


def _run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if check and cp.returncode != 0:
        raise RemoteImplementationError(
            "GIT_COMMAND_FAILED: " + " ".join(args) + "\n" + cp.stdout
        )
    return cp


def remote_head(repo: Path, branch: str, *, remote: str = "origin") -> str | None:
    cp = _run_git(
        repo,
        "ls-remote",
        "--heads",
        remote,
        f"refs/heads/{branch}",
        check=True,
    )
    line = cp.stdout.strip()
    return line.split()[0] if line else None


def _safe_publication_push_output(output: str, *, max_chars: int = 2048) -> str:
    """Retain bounded Git failure detail without echoing remote auth material."""
    detail = str(output or "")
    detail = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", detail)
    detail = re.sub(
        r"(?i)(?:\b(?:https?|ssh|git)://[^\s<>\"']+|\bgit@[^\s:]+:[^\s<>\"']+)",
        "[REDACTED_URL]",
        detail,
    )
    detail = re.sub(
        r"(?i)\b[\w.-]+:[^\s@]+@[\w.-]+(?:/[^\s]*)?",
        "[REDACTED_AUTHORITY]",
        detail,
    )
    detail = re.sub(
        r"(?i)\b(?:github_pat_|gh[pousr]_|glpat-|xox[baprs]-|sk-)[a-z0-9_-]+",
        "[REDACTED_TOKEN]",
        detail,
    )
    detail = re.sub(
        r"(?i)\b(?:authorization\s*:\s*)?(?:basic|bearer)\s+[^\s]+",
        "[REDACTED_AUTH]",
        detail,
    )
    detail = re.sub(
        r"(?i)(\b(?:gh_token|github_token|access_token|token|secret|password|passwd|api[_-]?key|credential|client_secret|authorization)\s*[:=]\s*)(?:\"[^\"]*\"|'[^']*'|[^\s]+)",
        r"\1[REDACTED]",
        detail,
    )
    detail = re.sub(r"\b[A-Za-z0-9_+/=-]{32,}\b", "[REDACTED_LONG_VALUE]", detail)
    detail = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", detail)
    detail = detail.strip()
    return detail[-max_chars:] if detail else "[no Git output]"


def publish_ref_cas(
    repo: Path,
    *,
    branch: str,
    prepared_commit: str,
    expected_predecessor: str | None,
    remote: str = "origin",
) -> None:
    prepared_commit = _require_sha(prepared_commit, 40, "PREPARED_COMMIT_INVALID")
    if expected_predecessor is not None:
        expected_predecessor = _require_sha(
            expected_predecessor,
            40,
            "TARGET_PREDECESSOR_INVALID",
        )
    actual = remote_head(repo, branch, remote=remote)
    status = classify_publication_precondition(
        expected_predecessor=expected_predecessor,
        actual_target=actual,
        prepared_commit=prepared_commit,
    )
    _require(status == "PUBLICATION_ALLOWED", "TARGET_PUBLICATION_CAS_PRECONDITION_FAILED")
    expected = expected_predecessor or ""
    cp = _run_git(
        repo,
        "push",
        f"--force-with-lease=refs/heads/{branch}:{expected}",
        remote,
        f"{prepared_commit}:refs/heads/{branch}",
        check=False,
    )
    if cp.returncode != 0:
        raise RemoteImplementationError(
            "TARGET_PUBLICATION_CAS_FAILED returncode=%s\n%s"
            % (cp.returncode, _safe_publication_push_output(cp.stdout))
        )
    _require(
        remote_head(repo, branch, remote=remote) == prepared_commit,
        "TARGET_PUBLICATION_VERIFY_FAILED",
    )
