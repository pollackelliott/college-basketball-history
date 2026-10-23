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


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(state_path, request_path, live_main_sha, state_commit):
    state = load_json(state_path)
    request = load_json(request_path)

    if state.get("schema_version") != 1:
        raise Reject("CONTROL_SCHEMA_MISMATCH", "unsupported control-state schema")
    if state.get("experiment_kind") != "REMOTE_IMPLEMENTATION_PROOF3_CONTROL":
        raise Reject("CONTROL_KIND_MISMATCH", "unexpected experiment kind")
    if state.get("school_key") != "long-island-university":
        raise Reject("SCHOOL_MISMATCH", "unexpected control-state school")
    if state.get("integration_frozen") is not False or state.get("phase0_authorized") is not False:
        raise Reject("AUTHORITY_BOUNDARY_VIOLATION", "control state carries forbidden mutation authority")

    request_id = request.get("request_id")
    if not request_id:
        raise Reject("REQUEST_ID_MISSING", "request has no request_id")

    if state.get("active_request_id") is not None or state.get("active_lock_owner") is not None or state.get("lifecycle_state") != "IDLE":
        raise Reject("IMPLEMENTATION_LOCK_OCCUPIED", "experimental implementation control lock is not idle")

    if request_id in state.get("consumed_request_ids", []):
        raise Reject("REQUEST_REPLAY", f"request {request_id} is already consumed")

    if request.get("school_key") != state.get("school_key"):
        raise Reject("SCHOOL_MISMATCH", "request school does not match control state")

    if request.get("operation") != "VERIFY_AND_REPLAY_STAGE1_CHECKPOINT":
        raise Reject("OPERATION_NOT_ALLOWED", "requested operation is not the bounded Proof 3 operation")

    authority = request.get("authority") or {}
    if authority.get("read_only") is not True or authority.get("phase0_authorized") is not False:
        raise Reject("AUTHORITY_BOUNDARY_VIOLATION", "request is not explicitly read-only/non-Phase-0")

    if request.get("predecessor_checkpoint_commit") != state.get("last_accepted_checkpoint_commit"):
        raise Reject("STALE_PREDECESSOR", "request predecessor is not the latest accepted checkpoint")

    if request.get("predecessor_manifest_sha256") != state.get("last_accepted_checkpoint_manifest_sha256"):
        raise Reject("STALE_PREDECESSOR", "request predecessor manifest hash is not current")

    expected_main = request.get("expected_protected_main_sha")
    if expected_main != state.get("expected_protected_main_sha"):
        raise Reject("MAIN_SHA_MISMATCH", "request expected-main does not match durable control state")
    if live_main_sha != expected_main:
        raise Reject("MAIN_SHA_MISMATCH", "live protected main differs from request expectation")

    if request.get("previous_control_state_commit") != state_commit:
        raise Reject("STALE_CONTROL_STATE", "request does not bind the actual predecessor control commit")

    actual_state_sha = sha256_file(state_path)
    if request.get("previous_control_state_sha256") != actual_state_sha:
        raise Reject("STALE_CONTROL_STATE", "request does not bind the exact predecessor control-state bytes")

    if request.get("schema_version") != 1 or request.get("experiment_kind") != "REMOTE_IMPLEMENTATION_PROOF3_REQUEST":
        raise Reject("REQUEST_SCHEMA_MISMATCH", "unexpected request schema/kind")

    print(f"REQUEST_ACCEPTED: {request_id}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("state")
    parser.add_argument("request")
    parser.add_argument("--live-main", required=True)
    parser.add_argument("--state-commit", required=True)
    args = parser.parse_args()
    try:
        verify(args.state, args.request, args.live_main, args.state_commit)
    except Reject as exc:
        print(f"{exc.code}: REJECTED — {exc.detail}")
        raise SystemExit(23)


if __name__ == "__main__":
    main()
