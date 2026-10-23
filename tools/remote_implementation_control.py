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
OP_RECOVER_PHASE0 = "RECOVER_PHASE0"
SUPPORTED_OPERATIONS = {OP_STAGE1, OP_PHASE0, OP_RECOVER_PHASE0}

LIFECYCLE_IDLE = "IDLE"
LIFECYCLE_READ_ONLY = "READ_ONLY_ACTIVE"
LIFECYCLE_ACTIVE = "ACTIVE"

TX_IDLE = "IDLE"
TX_STAGE1_RUNNING = "STAGE1_RUNNING"
TX_LOCKED = "LOCKED"
TX_INPUTS_VERIFIED = "INPUTS_VERIFIED"
TX_PREPARED = "PREPARED_NOT_PUBLISHED"
TX_PUBLISHED = "PUBLISHED_NOT_FINALIZED"
TX_COMPLETE = "COMPLETE"
TX_DIVERGED = "DIVERGED_STOP"

MUTATION_NOT_ATTEMPTED = "NOT_ATTEMPTED"
MUTATION_PREPARED = "PREPARED_NOT_PUBLISHED"
MUTATION_PUBLISHED = "PUBLISHED_NOT_FINALIZED"
MUTATION_COMPLETE = "COMPLETE"
MUTATION_DIVERGED = "DIVERGED_STOP"

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REQUEST_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
SCHOOL_KEY_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,127}$")


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
            TX_LOCKED,
            TX_INPUTS_VERIFIED,
            TX_PREPARED,
            TX_PUBLISHED,
            TX_COMPLETE,
            TX_DIVERGED,
        },
        "CONTROL_TRANSACTION_STATE_INVALID",
    )
    for key in ("accepted_request_ids", "consumed_request_ids", "abandoned_request_ids"):
        values = state.get(key)
        _require(isinstance(values, list), f"CONTROL_{key.upper()}_INVALID")
        _require(len(values) == len(set(values)), f"CONTROL_{key.upper()}_DUPLICATE")
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
    _require(authority.get("owner_gate_1") is False, "REQUEST_GATE1_AUTHORITY_FORBIDDEN")
    _require(authority.get("owner_gate_2") is False, "REQUEST_GATE2_AUTHORITY_FORBIDDEN")
    _require(authority.get("release") is False, "REQUEST_RELEASE_AUTHORITY_FORBIDDEN")

    if operation in {OP_STAGE1, OP_PHASE0}:
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

    if operation == OP_PHASE0:
        _require(authority.get("phase0") is True, "PHASE0_REQUEST_AUTHORITY_REQUIRED")
        expected_target = f"data/{school_key}-onboarding"
        _require(request.get("target_branch") == expected_target, "PHASE0_TARGET_BRANCH_INVALID")
        _validate_payload_ref(request.get("stage1_checkpoint"), "stage1_checkpoint", required=True)
        scope = request.get("history_scope")
        _require(isinstance(scope, dict), "REQUEST_HISTORY_SCOPE_MISSING")
        for key in ("start_season", "basis", "intervals", "notes"):
            _require(bool(str(scope.get(key) or "").strip()), f"REQUEST_HISTORY_SCOPE_{key.upper()}_MISSING")

    if operation == OP_RECOVER_PHASE0:
        _require(authority.get("recovery") is True, "RECOVERY_REQUEST_AUTHORITY_REQUIRED")
        recovery = request.get("recovery")
        _require(isinstance(recovery, dict), "RECOVERY_REQUEST_DETAILS_MISSING")
        _require(
            bool(REQUEST_ID_RE.fullmatch(str(recovery.get("abandoned_request_id") or ""))),
            "RECOVERY_REQUEST_ABANDONED_ID_INVALID",
        )
        _require_sha(recovery.get("lock_commit"), 40, "RECOVERY_REQUEST_LOCK_COMMIT_INVALID")
        target = str(recovery.get("target_branch") or "")
        _require(target == f"data/{school_key}-onboarding", "RECOVERY_TARGET_BRANCH_INVALID")


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
    if request["operation"] == OP_RECOVER_PHASE0 and allow_active_recovery:
        _require(state.get("lifecycle_state") == LIFECYCLE_ACTIVE, "STALE_RECOVERY_NO_ACTIVE_LOCK")
        recovery = request["recovery"]
        _require(
            state.get("active_request_id") == recovery["abandoned_request_id"],
            "STALE_RECOVERY_REQUEST_MISMATCH",
        )
        _require(
            state.get("active_lock_commit") == recovery["lock_commit"],
            "STALE_RECOVERY_LOCK_MISMATCH",
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
    if request["operation"] == OP_STAGE1:
        result["lifecycle_state"] = LIFECYCLE_READ_ONLY
        result["transaction_state"] = TX_STAGE1_RUNNING
        result["active_lock_owner"] = None
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
        "operation": OP_RECOVER_PHASE0,
        "recovered_request_id": active,
        "disposition": disposition,
        "recovery_manifest": recovery_manifest,
    }
    result = clear_active(result)
    result["transaction_state"] = disposition
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
    _require(cp.returncode == 0, "TARGET_PUBLICATION_CAS_FAILED")
    _require(
        remote_head(repo, branch, remote=remote) == prepared_commit,
        "TARGET_PUBLICATION_VERIFY_FAILED",
    )
