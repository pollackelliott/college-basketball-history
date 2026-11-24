#!/usr/bin/env python3
"""Pure fail-closed contract model for the proposed Two-Lane Implementation V1.

This module is deliberately *not* wired into the production remote runner.  It models
lane assignment, operation classes, the single shared-mutation lease, the single
publication lease, main-advance barriers, and migration from the legacy singleton
controller.  It performs no Git I/O and grants no basketball, owner-gate, merge, or
release authority.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from typing import Any

LANE_SCHEMA_VERSION = 2
ARBITER_SCHEMA_VERSION = 2
MIGRATION_SCHEMA_VERSION = 1
LANE_KIND = "REMOTE_IMPLEMENTATION_LANE_CONTROL"
ARBITER_KIND = "REMOTE_IMPLEMENTATION_GLOBAL_ARBITER"
MIGRATION_KIND = "REMOTE_IMPLEMENTATION_TWO_LANE_V1_MIGRATION"

LANE_A = "lane-a"
LANE_B = "lane-b"
LANE_IDS = (LANE_A, LANE_B)
LANE_REFS = {
    LANE_A: "control/remote-implementation-lane-a",
    LANE_B: "control/remote-implementation-lane-b",
}

IMPLEMENTATION_KINDS = {"ORDINARY", "ALL_HISTORY_EXPANSION"}
ASSIGNMENT_AVAILABLE = "AVAILABLE"
ASSIGNMENT_ASSIGNED = "ASSIGNED"
ASSIGNMENT_COMPLETE = "COMPLETE"
ASSIGNMENT_DISABLED = "DISABLED"
ASSIGNMENT_STATES = {
    ASSIGNMENT_AVAILABLE,
    ASSIGNMENT_ASSIGNED,
    ASSIGNMENT_COMPLETE,
    ASSIGNMENT_DISABLED,
}

OP_STAGE1 = "STAGE1_INVENTORY"
OP_PHASE0 = "PHASE0"
OP_EXPANSION_PHASE0 = "EXPANSION_PHASE0"
OP_PHASE0_SCOPE_SUPERSESSION = "PHASE0_SCOPE_SUPERSESSION"
OP_STAGE2_CENSUS = "STAGE2_CENSUS"
OP_STAGE2_CURRENT_MAIN_REFRESH = "STAGE2_CURRENT_MAIN_REFRESH"
OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE = "STAGE2_OPPONENT_DISPLAY_NORMALIZE"
OP_STAGE2_PROPOSAL_REHEARSAL = "STAGE2_PROPOSAL_REHEARSAL"
OP_STAGE2_GATE1_FILL = "STAGE2_GATE1_FILL"
OP_STAGE2_PRESEAL_REHEARSAL = "STAGE2_PRESEAL_REHEARSAL"
OP_STAGE2_GATE1_SEAL = "STAGE2_GATE1_SEAL"
OP_STAGE2_SEALED_APPLY = "STAGE2_SEALED_APPLY"
OP_STAGE2_RECONCILIATION_DIAGNOSTIC = "STAGE2_RECONCILIATION_DIAGNOSTIC"
OP_RELEASE_READINESS = "RELEASE_READINESS"
OP_RELEASE_PRESENTATION_REFRESH = "RELEASE_PRESENTATION_REFRESH"
OP_RELEASE_PREVIEW_VERIFY = "RELEASE_PREVIEW_VERIFY"
OP_RELEASE_GATE2_APPROVAL = "RELEASE_GATE2_APPROVAL"
OP_RELEASE_PRODUCTION_PROOF = "RELEASE_PRODUCTION_PROOF"
OP_VENUE_IDENTITY_MAINTENANCE = "VENUE_IDENTITY_MAINTENANCE"
OP_RECOVER = "RECOVER"

CLASS_LANE_READ_ONLY = "LANE_LOCAL_READ_ONLY"
CLASS_LANE_MUTATION = "LANE_LOCAL_MUTATION"
CLASS_SHARED_MUTATION = "SHARED_MUTATION_SLOT_REQUIRED"
CLASS_PUBLICATION = "PUBLICATION_SLOT_REQUIRED"

LANE_READ_ONLY_OPERATIONS = frozenset({
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
})
LANE_MUTATION_OPERATIONS = frozenset({
    OP_STAGE2_CURRENT_MAIN_REFRESH,
    OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
    OP_RELEASE_PRESENTATION_REFRESH,
})
SHARED_MUTATION_OPERATIONS = frozenset({
    OP_PHASE0,
    OP_EXPANSION_PHASE0,
    OP_PHASE0_SCOPE_SUPERSESSION,
    OP_STAGE2_SEALED_APPLY,
    OP_VENUE_IDENTITY_MAINTENANCE,
})
PUBLICATION_OPERATIONS = frozenset({OP_RELEASE_PRODUCTION_PROOF})
KNOWN_OPERATIONS = (
    LANE_READ_ONLY_OPERATIONS
    | LANE_MUTATION_OPERATIONS
    | SHARED_MUTATION_OPERATIONS
    | PUBLICATION_OPERATIONS
    | {OP_RECOVER}
)

SLOT_FREE = "FREE"
SLOT_HELD = "HELD"
PUBLICATION_PRE_MERGE = "HELD_PRE_MERGE"
PUBLICATION_MERGED = "MERGED_AWAITING_PRODUCTION_PROOF"
BARRIER_OPEN = "OPEN"
BARRIER_BLOCK_NEW_WORK = "BLOCK_NEW_WORK"
BARRIER_MAIN_ADVANCED = "MAIN_ADVANCED_UNVERIFIED"

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SCHOOL_KEY_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,127}$")
REQUEST_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")


class TwoLaneContractError(RuntimeError):
    """Fail-closed Two-Lane V1 contract violation."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise TwoLaneContractError(code)


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha(value: Any, length: int, code: str) -> str:
    text = str(value or "").strip().lower()
    pattern = HEX40 if length == 40 else HEX64
    _require(bool(pattern.fullmatch(text)), code)
    return text


def operation_class(operation: str, *, recovered_operation: str | None = None) -> str:
    if operation == OP_RECOVER:
        _require(recovered_operation is not None, "RECOVERY_OPERATION_REQUIRED")
        _require(recovered_operation != OP_RECOVER, "RECOVERY_NESTING_FORBIDDEN")
        return operation_class(recovered_operation)
    _require(operation in KNOWN_OPERATIONS, "TWO_LANE_OPERATION_UNKNOWN")
    if operation in LANE_READ_ONLY_OPERATIONS:
        return CLASS_LANE_READ_ONLY
    if operation in LANE_MUTATION_OPERATIONS:
        return CLASS_LANE_MUTATION
    if operation in SHARED_MUTATION_OPERATIONS:
        return CLASS_SHARED_MUTATION
    return CLASS_PUBLICATION


def build_migration_manifest(
    *,
    legacy_control_commit: str,
    legacy_control_state_sha256: str,
    protected_main_sha: str,
) -> dict[str, Any]:
    return {
        "schema_version": MIGRATION_SCHEMA_VERSION,
        "kind": MIGRATION_KIND,
        "status": "SHADOW_ONLY_NOT_ACTIVATED",
        "legacy_control_commit": _sha(
            legacy_control_commit, 40, "MIGRATION_LEGACY_CONTROL_COMMIT_INVALID"
        ),
        "legacy_control_state_sha256": _sha(
            legacy_control_state_sha256,
            64,
            "MIGRATION_LEGACY_CONTROL_STATE_HASH_INVALID",
        ),
        "protected_main_sha": _sha(
            protected_main_sha, 40, "MIGRATION_PROTECTED_MAIN_INVALID"
        ),
        "lane_refs": copy.deepcopy(LANE_REFS),
        "initial_max_active_lanes": 1,
        "lane_b_activation_authority": False,
        "live_runner_integration": False,
    }


def validate_migration_manifest(value: dict[str, Any]) -> None:
    _require(isinstance(value, dict), "MIGRATION_MANIFEST_NOT_OBJECT")
    _require(
        value.get("schema_version") == MIGRATION_SCHEMA_VERSION,
        "MIGRATION_SCHEMA_INVALID",
    )
    _require(value.get("kind") == MIGRATION_KIND, "MIGRATION_KIND_INVALID")
    _require(
        value.get("status") == "SHADOW_ONLY_NOT_ACTIVATED",
        "MIGRATION_STATUS_INVALID",
    )
    _sha(
        value.get("legacy_control_commit"),
        40,
        "MIGRATION_LEGACY_CONTROL_COMMIT_INVALID",
    )
    _sha(
        value.get("legacy_control_state_sha256"),
        64,
        "MIGRATION_LEGACY_CONTROL_STATE_HASH_INVALID",
    )
    _sha(value.get("protected_main_sha"), 40, "MIGRATION_PROTECTED_MAIN_INVALID")
    _require(value.get("lane_refs") == LANE_REFS, "MIGRATION_LANE_REFS_INVALID")
    _require(
        value.get("initial_max_active_lanes") == 1,
        "MIGRATION_INITIAL_CAPACITY_INVALID",
    )
    _require(
        value.get("lane_b_activation_authority") is False,
        "MIGRATION_PREMATURE_LANE_B_AUTHORITY",
    )
    _require(
        value.get("live_runner_integration") is False,
        "MIGRATION_PREMATURE_LIVE_INTEGRATION",
    )


def initial_lane_state(
    lane_id: str, *, protected_main_sha: str, enabled: bool
) -> dict[str, Any]:
    _require(lane_id in LANE_IDS, "LANE_ID_INVALID")
    main = _sha(protected_main_sha, 40, "LANE_MAIN_SHA_INVALID")
    return {
        "schema_version": LANE_SCHEMA_VERSION,
        "kind": LANE_KIND,
        "lane_id": lane_id,
        "lane_ref": LANE_REFS[lane_id],
        "assignment_status": (
            ASSIGNMENT_AVAILABLE if enabled else ASSIGNMENT_DISABLED
        ),
        "assigned_school_key": None,
        "implementation_kind": None,
        "bound_main_sha": main,
        "lane_sequence": 0,
        "active_request_id": None,
        "active_operation": None,
        "recovery_required": False,
        "last_operation": None,
        "authority_statement": (
            "Lane-scoped orchestration authority only. This state grants no owner gate, "
            "shared mutation lease, merge authority, or Production authority."
        ),
    }


def validate_lane_state(state: dict[str, Any]) -> None:
    _require(isinstance(state, dict), "LANE_STATE_NOT_OBJECT")
    _require(
        state.get("schema_version") == LANE_SCHEMA_VERSION,
        "LANE_SCHEMA_INVALID",
    )
    _require(state.get("kind") == LANE_KIND, "LANE_KIND_INVALID")
    lane_id = state.get("lane_id")
    _require(lane_id in LANE_IDS, "LANE_ID_INVALID")
    _require(state.get("lane_ref") == LANE_REFS[lane_id], "LANE_REF_INVALID")
    status = state.get("assignment_status")
    _require(status in ASSIGNMENT_STATES, "LANE_ASSIGNMENT_STATUS_INVALID")
    _sha(state.get("bound_main_sha"), 40, "LANE_MAIN_SHA_INVALID")
    _require(
        type(state.get("lane_sequence")) is int and state["lane_sequence"] >= 0,
        "LANE_SEQUENCE_INVALID",
    )
    school = state.get("assigned_school_key")
    kind = state.get("implementation_kind")
    if status == ASSIGNMENT_ASSIGNED:
        _require(
            isinstance(school, str) and SCHOOL_KEY_RE.fullmatch(school),
            "LANE_ASSIGNED_SCHOOL_INVALID",
        )
        _require(
            kind in IMPLEMENTATION_KINDS,
            "LANE_IMPLEMENTATION_KIND_INVALID",
        )
    else:
        _require(school is None, "LANE_UNASSIGNED_HAS_SCHOOL")
        _require(
            kind is None,
            "LANE_UNASSIGNED_HAS_IMPLEMENTATION_KIND",
        )
    active_request = state.get("active_request_id")
    active_operation = state.get("active_operation")
    if active_request is None:
        _require(active_operation is None, "LANE_IDLE_HAS_OPERATION")
        _require(
            state.get("recovery_required") is False,
            "LANE_IDLE_RECOVERY_REQUIRED",
        )
    else:
        _require(
            status == ASSIGNMENT_ASSIGNED,
            "LANE_ACTIVE_WITHOUT_ASSIGNMENT",
        )
        _require(
            bool(REQUEST_ID_RE.fullmatch(str(active_request))),
            "LANE_REQUEST_ID_INVALID",
        )
        _require(
            active_operation in KNOWN_OPERATIONS,
            "LANE_ACTIVE_OPERATION_INVALID",
        )


def initial_arbiter_state(
    *,
    protected_main_sha: str,
    migration_manifest: dict[str, Any],
) -> dict[str, Any]:
    validate_migration_manifest(migration_manifest)
    main = _sha(protected_main_sha, 40, "ARBITER_MAIN_SHA_INVALID")
    _require(
        main == migration_manifest["protected_main_sha"],
        "ARBITER_MIGRATION_MAIN_MISMATCH",
    )
    migration_sha = sha256_bytes(canonical_json_bytes(migration_manifest))
    return {
        "schema_version": ARBITER_SCHEMA_VERSION,
        "kind": ARBITER_KIND,
        "protected_main_sha": main,
        "max_active_lanes": 1,
        "lane_refs": copy.deepcopy(LANE_REFS),
        "lane_assignments": {LANE_A: None, LANE_B: None},
        "shared_mutation_slot": {
            "state": SLOT_FREE,
            "lane_id": None,
            "school_key": None,
            "request_id": None,
            "operation": None,
        },
        "publication_slot": {
            "state": SLOT_FREE,
            "lane_id": None,
            "school_key": None,
            "pr_number": None,
            "pr_head_sha": None,
            "merge_sha": None,
        },
        "main_advance_barrier": {
            "state": BARRIER_OPEN,
            "holder_lane_id": None,
        },
        "migration_manifest_sha256": migration_sha,
        "live_runner_integration": False,
        "lane_b_activation": {
            "compatibility_pilot_passed": False,
            "adversarial_suite_passed": False,
            "owner_authorized": False,
        },
    }


def validate_arbiter_state(state: dict[str, Any]) -> None:
    _require(isinstance(state, dict), "ARBITER_STATE_NOT_OBJECT")
    _require(
        state.get("schema_version") == ARBITER_SCHEMA_VERSION,
        "ARBITER_SCHEMA_INVALID",
    )
    _require(state.get("kind") == ARBITER_KIND, "ARBITER_KIND_INVALID")
    _sha(state.get("protected_main_sha"), 40, "ARBITER_MAIN_SHA_INVALID")
    _require(
        state.get("max_active_lanes") in {1, 2},
        "ARBITER_CAPACITY_INVALID",
    )
    _require(state.get("lane_refs") == LANE_REFS, "ARBITER_LANE_REFS_INVALID")
    assignments = state.get("lane_assignments")
    _require(
        isinstance(assignments, dict) and set(assignments) == set(LANE_IDS),
        "ARBITER_ASSIGNMENTS_INVALID",
    )
    schools = [x for x in assignments.values() if x is not None]
    for school in schools:
        _require(
            isinstance(school, str) and SCHOOL_KEY_RE.fullmatch(school),
            "ARBITER_ASSIGNED_SCHOOL_INVALID",
        )
    _require(
        len(schools) == len(set(schools)),
        "ARBITER_DUPLICATE_SCHOOL_ASSIGNMENT",
    )
    if state["max_active_lanes"] == 1:
        _require(
            assignments[LANE_B] is None,
            "ARBITER_LANE_B_ASSIGNED_WHILE_DISABLED",
        )

    slot = state.get("shared_mutation_slot")
    _require(isinstance(slot, dict), "ARBITER_SHARED_SLOT_INVALID")
    _require(
        slot.get("state") in {SLOT_FREE, SLOT_HELD},
        "ARBITER_SHARED_SLOT_STATE_INVALID",
    )
    if slot["state"] == SLOT_FREE:
        _require(
            all(
                slot.get(k) is None
                for k in ("lane_id", "school_key", "request_id", "operation")
            ),
            "ARBITER_FREE_SHARED_SLOT_HAS_OWNER",
        )
    else:
        _require(
            slot.get("lane_id") in LANE_IDS,
            "ARBITER_SHARED_SLOT_LANE_INVALID",
        )
        _require(
            assignments.get(slot["lane_id"]) == slot.get("school_key"),
            "ARBITER_SHARED_SLOT_SCHOOL_MISMATCH",
        )
        _require(
            bool(
                REQUEST_ID_RE.fullmatch(
                    str(slot.get("request_id") or "")
                )
            ),
            "ARBITER_SHARED_SLOT_REQUEST_INVALID",
        )
        _require(
            operation_class(str(slot.get("operation") or ""))
            == CLASS_SHARED_MUTATION,
            "ARBITER_SHARED_SLOT_OPERATION_INVALID",
        )

    pub = state.get("publication_slot")
    _require(isinstance(pub, dict), "ARBITER_PUBLICATION_SLOT_INVALID")
    _require(
        pub.get("state")
        in {SLOT_FREE, PUBLICATION_PRE_MERGE, PUBLICATION_MERGED},
        "ARBITER_PUBLICATION_SLOT_STATE_INVALID",
    )
    if pub["state"] == SLOT_FREE:
        _require(
            all(
                pub.get(k) is None
                for k in (
                    "lane_id",
                    "school_key",
                    "pr_number",
                    "pr_head_sha",
                    "merge_sha",
                )
            ),
            "ARBITER_FREE_PUBLICATION_SLOT_HAS_OWNER",
        )
    else:
        _require(
            pub.get("lane_id") in LANE_IDS,
            "ARBITER_PUBLICATION_LANE_INVALID",
        )
        _require(
            assignments.get(pub["lane_id"]) == pub.get("school_key"),
            "ARBITER_PUBLICATION_SCHOOL_MISMATCH",
        )
        _require(
            type(pub.get("pr_number")) is int and pub["pr_number"] > 0,
            "ARBITER_PUBLICATION_PR_INVALID",
        )
        _sha(
            pub.get("pr_head_sha"),
            40,
            "ARBITER_PUBLICATION_HEAD_INVALID",
        )
        if pub["state"] == PUBLICATION_PRE_MERGE:
            _require(
                pub.get("merge_sha") is None,
                "ARBITER_PREMERGE_HAS_MERGE_SHA",
            )
        else:
            _sha(pub.get("merge_sha"), 40, "ARBITER_MERGE_SHA_INVALID")
            _require(
                state["protected_main_sha"] == pub["merge_sha"],
                "ARBITER_MERGED_MAIN_MISMATCH",
            )

    barrier = state.get("main_advance_barrier")
    _require(isinstance(barrier, dict), "ARBITER_BARRIER_INVALID")
    _require(
        barrier.get("state")
        in {
            BARRIER_OPEN,
            BARRIER_BLOCK_NEW_WORK,
            BARRIER_MAIN_ADVANCED,
        },
        "ARBITER_BARRIER_STATE_INVALID",
    )
    if pub["state"] == SLOT_FREE:
        _require(
            barrier
            == {
                "state": BARRIER_OPEN,
                "holder_lane_id": None,
            },
            "ARBITER_FREE_PUBLICATION_BARRIER_NOT_OPEN",
        )
    else:
        _require(
            barrier.get("holder_lane_id") == pub.get("lane_id"),
            "ARBITER_BARRIER_HOLDER_MISMATCH",
        )
        expected = (
            BARRIER_BLOCK_NEW_WORK
            if pub["state"] == PUBLICATION_PRE_MERGE
            else BARRIER_MAIN_ADVANCED
        )
        _require(
            barrier.get("state") == expected,
            "ARBITER_BARRIER_PUBLICATION_STATE_MISMATCH",
        )

    activation = state.get("lane_b_activation")
    _require(
        isinstance(activation, dict),
        "ARBITER_LANE_B_ACTIVATION_INVALID",
    )
    for key in (
        "compatibility_pilot_passed",
        "adversarial_suite_passed",
        "owner_authorized",
    ):
        _require(
            type(activation.get(key)) is bool,
            "ARBITER_LANE_B_ACTIVATION_FLAG_INVALID",
        )
    if state["max_active_lanes"] == 2:
        _require(
            all(activation.values()),
            "ARBITER_LANE_B_ACTIVATED_WITHOUT_PROOFS",
        )


def claim_lane(
    arbiter: dict[str, Any],
    lane: dict[str, Any],
    *,
    school_key: str,
    implementation_kind: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_arbiter_state(arbiter)
    validate_lane_state(lane)
    lane_id = lane["lane_id"]
    _require(
        lane["assignment_status"] == ASSIGNMENT_AVAILABLE,
        "LANE_NOT_AVAILABLE",
    )
    _require(
        arbiter["lane_assignments"][lane_id] is None,
        "ARBITER_LANE_ALREADY_ASSIGNED",
    )
    if lane_id == LANE_B:
        _require(
            arbiter["max_active_lanes"] == 2,
            "ARBITER_LANE_B_DISABLED",
        )
    _require(
        bool(SCHOOL_KEY_RE.fullmatch(school_key)),
        "LANE_CLAIM_SCHOOL_INVALID",
    )
    _require(
        implementation_kind in IMPLEMENTATION_KINDS,
        "LANE_CLAIM_IMPLEMENTATION_KIND_INVALID",
    )
    _require(
        school_key
        not in set(
            x for x in arbiter["lane_assignments"].values() if x
        ),
        "ARBITER_DUPLICATE_SCHOOL_ASSIGNMENT",
    )
    result_arbiter = copy.deepcopy(arbiter)
    result_lane = copy.deepcopy(lane)
    result_arbiter["lane_assignments"][lane_id] = school_key
    result_lane["assignment_status"] = ASSIGNMENT_ASSIGNED
    result_lane["assigned_school_key"] = school_key
    result_lane["implementation_kind"] = implementation_kind
    result_lane["lane_sequence"] += 1
    validate_arbiter_state(result_arbiter)
    validate_lane_state(result_lane)
    return result_arbiter, result_lane


def activate_lane_b(
    arbiter: dict[str, Any],
    *,
    compatibility_pilot_passed: bool,
    adversarial_suite_passed: bool,
    owner_authorized: bool,
) -> dict[str, Any]:
    validate_arbiter_state(arbiter)
    _require(
        arbiter["max_active_lanes"] == 1,
        "ARBITER_LANE_B_ALREADY_ENABLED",
    )
    _require(
        arbiter["shared_mutation_slot"]["state"] == SLOT_FREE,
        "ARBITER_ACTIVATION_SHARED_SLOT_BUSY",
    )
    _require(
        arbiter["publication_slot"]["state"] == SLOT_FREE,
        "ARBITER_ACTIVATION_PUBLICATION_BUSY",
    )
    _require(
        compatibility_pilot_passed,
        "ARBITER_COMPATIBILITY_PILOT_REQUIRED",
    )
    _require(
        adversarial_suite_passed,
        "ARBITER_ADVERSARIAL_SUITE_REQUIRED",
    )
    _require(
        owner_authorized,
        "ARBITER_OWNER_AUTHORIZATION_REQUIRED",
    )
    result = copy.deepcopy(arbiter)
    result["lane_b_activation"] = {
        "compatibility_pilot_passed": True,
        "adversarial_suite_passed": True,
        "owner_authorized": True,
    }
    result["max_active_lanes"] = 2
    validate_arbiter_state(result)
    return result


def may_begin_operation(
    arbiter: dict[str, Any],
    lane: dict[str, Any],
    operation: str,
    *,
    recovered_operation: str | None = None,
) -> bool:
    validate_arbiter_state(arbiter)
    validate_lane_state(lane)
    lane_id = lane["lane_id"]
    _require(
        lane["assignment_status"] == ASSIGNMENT_ASSIGNED,
        "LANE_OPERATION_WITHOUT_ASSIGNMENT",
    )
    _require(
        arbiter["lane_assignments"][lane_id]
        == lane["assigned_school_key"],
        "LANE_ARBITER_ASSIGNMENT_MISMATCH",
    )
    op_class = operation_class(
        operation,
        recovered_operation=recovered_operation,
    )
    pub = arbiter["publication_slot"]
    if pub["state"] != SLOT_FREE and pub["lane_id"] != lane_id:
        return False
    if pub["state"] == PUBLICATION_MERGED:
        return (
            operation == OP_RELEASE_PRODUCTION_PROOF
            and pub["lane_id"] == lane_id
        )
    if lane["bound_main_sha"] != arbiter["protected_main_sha"]:
        return False
    if op_class == CLASS_SHARED_MUTATION:
        slot = arbiter["shared_mutation_slot"]
        return slot["state"] in {SLOT_FREE, SLOT_HELD} and (
            slot["state"] == SLOT_FREE
            or slot["lane_id"] == lane_id
        )
    if op_class == CLASS_PUBLICATION:
        return (
            pub["state"] == PUBLICATION_MERGED
            and pub["lane_id"] == lane_id
        )
    return True


def acquire_shared_mutation_slot(
    arbiter: dict[str, Any],
    lane: dict[str, Any],
    *,
    request_id: str,
    operation: str,
) -> dict[str, Any]:
    validate_arbiter_state(arbiter)
    validate_lane_state(lane)
    _require(
        operation_class(operation) == CLASS_SHARED_MUTATION,
        "ARBITER_SHARED_SLOT_OPERATION_CLASS_INVALID",
    )
    _require(
        may_begin_operation(arbiter, lane, operation),
        "ARBITER_SHARED_SLOT_BEGIN_FORBIDDEN",
    )
    _require(
        arbiter["shared_mutation_slot"]["state"] == SLOT_FREE,
        "ARBITER_SHARED_MUTATION_BUSY",
    )
    _require(
        arbiter["publication_slot"]["state"] == SLOT_FREE,
        "ARBITER_SHARED_MUTATION_PUBLICATION_BUSY",
    )
    _require(
        bool(REQUEST_ID_RE.fullmatch(request_id)),
        "ARBITER_SHARED_SLOT_REQUEST_INVALID",
    )
    result = copy.deepcopy(arbiter)
    result["shared_mutation_slot"] = {
        "state": SLOT_HELD,
        "lane_id": lane["lane_id"],
        "school_key": lane["assigned_school_key"],
        "request_id": request_id,
        "operation": operation,
    }
    validate_arbiter_state(result)
    return result


def release_shared_mutation_slot(
    arbiter: dict[str, Any],
    *,
    lane_id: str,
    request_id: str,
    disposition: str,
) -> dict[str, Any]:
    validate_arbiter_state(arbiter)
    slot = arbiter["shared_mutation_slot"]
    _require(
        slot["state"] == SLOT_HELD,
        "ARBITER_SHARED_SLOT_NOT_HELD",
    )
    _require(
        slot["lane_id"] == lane_id
        and slot["request_id"] == request_id,
        "ARBITER_SHARED_SLOT_RELEASE_OWNER_MISMATCH",
    )
    _require(
        disposition
        in {
            "COMPLETE",
            "RECOVERED_NOT_ATTEMPTED",
            "RECOVERED_PREPARED_NOT_PUBLISHED",
        },
        "ARBITER_SHARED_SLOT_RELEASE_DISPOSITION_INVALID",
    )
    result = copy.deepcopy(arbiter)
    result["shared_mutation_slot"] = {
        "state": SLOT_FREE,
        "lane_id": None,
        "school_key": None,
        "request_id": None,
        "operation": None,
    }
    validate_arbiter_state(result)
    return result


def acquire_publication_slot(
    arbiter: dict[str, Any],
    lane: dict[str, Any],
    *,
    pr_number: int,
    pr_head_sha: str,
) -> dict[str, Any]:
    validate_arbiter_state(arbiter)
    validate_lane_state(lane)
    _require(
        lane["assignment_status"] == ASSIGNMENT_ASSIGNED,
        "ARBITER_PUBLICATION_WITHOUT_ASSIGNMENT",
    )
    _require(
        lane["bound_main_sha"] == arbiter["protected_main_sha"],
        "ARBITER_PUBLICATION_LANE_MAIN_STALE",
    )
    _require(
        arbiter["shared_mutation_slot"]["state"] == SLOT_FREE,
        "ARBITER_PUBLICATION_SHARED_MUTATION_BUSY",
    )
    _require(
        arbiter["publication_slot"]["state"] == SLOT_FREE,
        "ARBITER_PUBLICATION_BUSY",
    )
    _require(
        type(pr_number) is int and pr_number > 0,
        "ARBITER_PUBLICATION_PR_INVALID",
    )
    head = _sha(
        pr_head_sha,
        40,
        "ARBITER_PUBLICATION_HEAD_INVALID",
    )
    result = copy.deepcopy(arbiter)
    result["publication_slot"] = {
        "state": PUBLICATION_PRE_MERGE,
        "lane_id": lane["lane_id"],
        "school_key": lane["assigned_school_key"],
        "pr_number": pr_number,
        "pr_head_sha": head,
        "merge_sha": None,
    }
    result["main_advance_barrier"] = {
        "state": BARRIER_BLOCK_NEW_WORK,
        "holder_lane_id": lane["lane_id"],
    }
    validate_arbiter_state(result)
    return result


def mark_publication_merged(
    arbiter: dict[str, Any],
    *,
    lane_id: str,
    merge_sha: str,
) -> dict[str, Any]:
    validate_arbiter_state(arbiter)
    pub = arbiter["publication_slot"]
    _require(
        pub["state"] == PUBLICATION_PRE_MERGE,
        "ARBITER_PUBLICATION_NOT_PREMERGE",
    )
    _require(
        pub["lane_id"] == lane_id,
        "ARBITER_PUBLICATION_MERGE_OWNER_MISMATCH",
    )
    merged = _sha(merge_sha, 40, "ARBITER_MERGE_SHA_INVALID")
    result = copy.deepcopy(arbiter)
    result["publication_slot"]["state"] = PUBLICATION_MERGED
    result["publication_slot"]["merge_sha"] = merged
    result["protected_main_sha"] = merged
    result["main_advance_barrier"] = {
        "state": BARRIER_MAIN_ADVANCED,
        "holder_lane_id": lane_id,
    }
    validate_arbiter_state(result)
    return result


def release_publication_slot_after_production(
    arbiter: dict[str, Any],
    *,
    lane_id: str,
    production_proof_passed: bool,
    proved_main_sha: str,
) -> dict[str, Any]:
    validate_arbiter_state(arbiter)
    pub = arbiter["publication_slot"]
    _require(
        pub["state"] == PUBLICATION_MERGED,
        "ARBITER_PUBLICATION_NOT_AWAITING_PRODUCTION",
    )
    _require(
        pub["lane_id"] == lane_id,
        "ARBITER_PUBLICATION_RELEASE_OWNER_MISMATCH",
    )
    _require(
        production_proof_passed,
        "ARBITER_PRODUCTION_PROOF_REQUIRED",
    )
    proved = _sha(
        proved_main_sha,
        40,
        "ARBITER_PRODUCTION_MAIN_INVALID",
    )
    _require(
        proved == pub["merge_sha"] == arbiter["protected_main_sha"],
        "ARBITER_PRODUCTION_MAIN_MISMATCH",
    )
    result = copy.deepcopy(arbiter)
    result["publication_slot"] = {
        "state": SLOT_FREE,
        "lane_id": None,
        "school_key": None,
        "pr_number": None,
        "pr_head_sha": None,
        "merge_sha": None,
    }
    result["main_advance_barrier"] = {
        "state": BARRIER_OPEN,
        "holder_lane_id": None,
    }
    validate_arbiter_state(result)
    return result


def rebind_lane_main(
    lane: dict[str, Any],
    *,
    new_main_sha: str,
    proof_kind: str,
    proof_passed: bool,
) -> dict[str, Any]:
    validate_lane_state(lane)
    _require(
        lane["active_request_id"] is None,
        "LANE_MAIN_REBIND_ACTIVE_REQUEST",
    )
    _require(
        proof_kind
        in {
            "FRESH_STARTUP_REAUTH",
            "STAGE2_CURRENT_MAIN_REFRESH",
            "POST_PUBLICATION_REAUTH",
        },
        "LANE_MAIN_REBIND_PROOF_KIND_INVALID",
    )
    _require(
        proof_passed,
        "LANE_MAIN_REBIND_PROOF_REQUIRED",
    )
    result = copy.deepcopy(lane)
    result["bound_main_sha"] = _sha(
        new_main_sha,
        40,
        "LANE_MAIN_SHA_INVALID",
    )
    result["lane_sequence"] += 1
    validate_lane_state(result)
    return result
