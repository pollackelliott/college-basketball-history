#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


class Reject(Exception):
    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code
        self.detail = detail


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def common(state, request, state_path, state_commit, live_main):
    if state.get("schema_version") != 1:
        raise Reject("CONTROL_SCHEMA_MISMATCH", "unsupported control schema")
    if state.get("experiment_kind") != "REMOTE_IMPLEMENTATION_PROOF4_GLOBAL_CONTROL":
        raise Reject("CONTROL_KIND_MISMATCH", "unexpected control kind")
    if state.get("global_lock_scope") != "ONE_ACTIVE_IMPLEMENTATION_PROJECT_WIDE":
        raise Reject("CONTROL_SCOPE_MISMATCH", "control is not project-wide")
    if state.get("integration_frozen") is not False or state.get("phase0_authorized") is not False:
        raise Reject("AUTHORITY_BOUNDARY_VIOLATION", "durable state carries forbidden mutation authority")

    if request.get("schema_version") != 1:
        raise Reject("REQUEST_SCHEMA_MISMATCH", "unsupported request schema")
    if request.get("experiment_kind") != "REMOTE_IMPLEMENTATION_PROOF4_REQUEST":
        raise Reject("REQUEST_SCHEMA_MISMATCH", "unexpected request kind")
    authority = request.get("authority") or {}
    if authority.get("experimental_control_only") is not True:
        raise Reject("AUTHORITY_BOUNDARY_VIOLATION", "request is not experiment-only")
    if authority.get("basketball_mutation_authorized") is not False:
        raise Reject("AUTHORITY_BOUNDARY_VIOLATION", "request authorizes basketball mutation")
    if authority.get("integration_freeze_authorized") is not False:
        raise Reject("AUTHORITY_BOUNDARY_VIOLATION", "request authorizes Integration Freeze")
    if authority.get("phase0_authorized") is not False:
        raise Reject("AUTHORITY_BOUNDARY_VIOLATION", "request authorizes Phase 0")

    if request.get("previous_control_state_commit") != state_commit:
        raise Reject("STALE_CONTROL_STATE", "request does not bind exact predecessor control commit")
    if request.get("previous_control_state_sha256") != file_sha(state_path):
        raise Reject("STALE_CONTROL_STATE", "request does not bind exact predecessor control bytes")

    expected_main = request.get("expected_protected_main_sha")
    if expected_main != state.get("expected_protected_main_sha"):
        raise Reject("MAIN_SHA_MISMATCH", "request expected-main differs from durable control basis")
    if live_main != expected_main:
        raise Reject("MAIN_SHA_MISMATCH", "live protected main differs from request expectation")

    request_id = request.get("request_id")
    if not request_id:
        raise Reject("REQUEST_ID_MISSING", "missing request ID")
    return request_id


def evaluate(state_path, request_path, live_main, state_commit):
    state = load(state_path)
    request = load(request_path)
    request_id = common(state, request, state_path, state_commit, live_main)

    operation = request.get("operation")
    lifecycle = state.get("lifecycle_state")
    accepted = set(state.get("accepted_request_ids") or [])
    consumed = set(state.get("consumed_request_ids") or [])
    abandoned = set(state.get("abandoned_request_ids") or [])

    if operation == "TEST_DURABLE_LOCK_FAILURE":
        if request_id == state.get("active_request_id") or request_id in accepted or request_id in abandoned:
            raise Reject("REQUEST_ALREADY_ACCEPTED_OR_ACTIVE", f"{request_id} is not reusable")
        if request_id in consumed:
            raise Reject("REQUEST_REPLAY", f"{request_id} was already consumed")
        if lifecycle != "IDLE" or state.get("active_request_id") is not None or state.get("active_lock_owner") is not None:
            raise Reject(
                "IMPLEMENTATION_LOCK_OCCUPIED",
                f"global lock held by {state.get('active_request_id')} / {state.get('active_fixture_id')}",
            )
        print("FAILURE_REQUEST_ADMISSIBLE")
        return

    if operation == "TEST_GLOBAL_LOCK_ADMISSION":
        if request_id in accepted or request_id in consumed or request_id in abandoned:
            raise Reject("REQUEST_REPLAY", f"{request_id} is not reusable")
        if lifecycle != "IDLE" or state.get("active_request_id") is not None or state.get("active_lock_owner") is not None:
            raise Reject(
                "IMPLEMENTATION_LOCK_OCCUPIED",
                f"global lock held by {state.get('active_request_id')} / {state.get('active_fixture_id')}",
            )
        print("GLOBAL_LOCK_ADMISSION_AVAILABLE")
        return

    if operation == "RECOVER_ABANDONED_EXPERIMENT_LOCK":
        if lifecycle != "ACTIVE" or state.get("active_request_id") is None:
            raise Reject("RECOVERY_PREDECESSOR_STALE", "there is no exact active lock to recover")
        if request.get("abandoned_request_id") != state.get("active_request_id"):
            raise Reject("RECOVERY_AUTHORITY_MISMATCH", "recovery names a different active request")
        if request.get("active_lock_commit") != state.get("active_lock_commit"):
            raise Reject("RECOVERY_AUTHORITY_MISMATCH", "recovery names a different lock-acquisition commit")
        if int(request.get("failed_action_run_id", -1)) != int(state.get("lock_acquired_run_id", -2)):
            raise Reject("RECOVERY_AUTHORITY_MISMATCH", "recovery names a different failed Action run")
        if int(request.get("failed_action_run_attempt", -1)) != int(state.get("lock_acquired_run_attempt", -2)):
            raise Reject("RECOVERY_AUTHORITY_MISMATCH", "recovery names a different failed Action attempt")
        if request.get("durable_active_state_commit") != state.get("durable_active_state_commit"):
            raise Reject("RECOVERY_AUTHORITY_MISMATCH", "recovery names a different stranded ACTIVE state")
        print("RECOVERY_REQUEST_ADMISSIBLE")
        return

    raise Reject("OPERATION_NOT_ALLOWED", f"unsupported Proof 4 operation {operation!r}")


def rerun_guard(durable_state_path, request_path):
    state = load(durable_state_path)
    request = load(request_path)
    request_id = request.get("request_id")
    accepted = set(state.get("accepted_request_ids") or [])
    abandoned = set(state.get("abandoned_request_ids") or [])
    consumed = set(state.get("consumed_request_ids") or [])
    if state.get("active_request_id") == request_id or request_id in accepted or request_id in abandoned:
        raise Reject("DURABLE_ACTIVE_REQUEST_EXISTS", f"{request_id} has durable prior acceptance")
    if request_id in consumed:
        raise Reject("REQUEST_REPLAY", f"{request_id} was already consumed")
    print("RERUN_GUARD_CLEAR")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("evaluate")
    e.add_argument("state")
    e.add_argument("request")
    e.add_argument("--live-main", required=True)
    e.add_argument("--state-commit", required=True)

    r = sub.add_parser("rerun-guard")
    r.add_argument("durable_state")
    r.add_argument("request")

    args = p.parse_args()
    try:
        if args.cmd == "evaluate":
            evaluate(args.state, args.request, args.live_main, args.state_commit)
        else:
            rerun_guard(args.durable_state, args.request)
    except Reject as exc:
        print(f"{exc.code}: REJECTED — {exc.detail}")
        raise SystemExit(23)


if __name__ == "__main__":
    main()
