#!/usr/bin/env python3
"""Guarded pre-Gate-1 reset of a stale All-History expansion onboarding ref.

This operation carries no basketball-history authority. It exists only to preserve
an exact, freshly verified pre-Gate-1 expansion lineage and move the one serialized
data/<school>-onboarding ref back to the request-bound protected-main commit so the
ordinary expansion startup can begin again from its normal ancestor topology.

The superseded target lineage is preserved as a Git bundle on the durable control
branch before the ref mutation is attempted.
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from remote_implementation_control import (
    OP_EXPANSION_PHASE0,
    OP_EXPANSION_REBOOTSTRAP_FROM_FREEZE,
    OP_STAGE2_CENSUS,
    OP_STAGE2_CURRENT_MAIN_REFRESH,
    OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
    OP_STAGE2_PROPOSAL_REHEARSAL,
    OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
    begin_request,
    bind_lock_commit,
    finalize_success,
    publish_ref_cas,
    sha256_bytes,
    sha256_file,
    validate_control_state,
)
from remote_implementation_expansion_phase0 import (
    materialize_expansion_research_checkpoint,
)
from remote_implementation_io import (
    ROOT,
    STATE_PATH,
    Stop,
    assert_protected_main_unchanged,
    commit_control,
    git,
    git_show_bytes,
    remote_head,
    write_json,
)

SUCCESSOR_KIND_PHASE0 = "REMOTE_IMPLEMENTATION_SUCCESSOR"
SUCCESSOR_KIND_DISPLAY = "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR"
SUCCESSOR_KIND_REFRESH = "REMOTE_IMPLEMENTATION_STAGE2_CURRENT_MAIN_REFRESH_SUCCESSOR"

PRE_GATE1_OPERATIONS = frozenset({
    OP_EXPANSION_PHASE0,
    OP_STAGE2_CENSUS,
    OP_STAGE2_CURRENT_MAIN_REFRESH,
    OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
    OP_STAGE2_PROPOSAL_REHEARSAL,
    OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
})

_SUCCESSOR_VERIFICATION_CONTRACTS = {
    SUCCESSOR_KIND_PHASE0: (
        OP_EXPANSION_PHASE0,
        "REMOTE_IMPLEMENTATION_FRESH_VERIFICATION",
        "remote_phase0_equivalence",
    ),
    SUCCESSOR_KIND_DISPLAY: (
        OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
        "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_VERIFICATION",
        "remote_stage2_opponent_display_equivalence",
    ),
    SUCCESSOR_KIND_REFRESH: (
        OP_STAGE2_CURRENT_MAIN_REFRESH,
        "REMOTE_IMPLEMENTATION_STAGE2_CURRENT_MAIN_REFRESH_VERIFICATION",
        "remote_stage2_current_main_refresh_equivalence",
    ),
}


def _read_json_ref(
    control_commit: str,
    ref: dict[str, Any],
    *,
    code: str,
) -> tuple[dict[str, Any], bytes]:
    data = git_show_bytes(control_commit, str(ref.get("path") or ""))
    if sha256_bytes(data) != ref.get("sha256"):
        raise Stop(code + "_HASH_MISMATCH")
    try:
        value = json.loads(data)
    except (TypeError, ValueError) as exc:
        raise Stop(code + "_JSON_INVALID") from exc
    if not isinstance(value, dict):
        raise Stop(code + "_NOT_OBJECT")
    return value, data


def successor_verification_contract(
    successor_kind: str,
) -> tuple[str, str, str]:
    try:
        return _SUCCESSOR_VERIFICATION_CONTRACTS[successor_kind]
    except KeyError as exc:
        raise Stop(
            "EXPANSION_REBOOTSTRAP_SUCCESSOR_KIND_UNSUPPORTED:" + successor_kind
        ) from exc


def _require_linear_main_advance(
    earlier: str,
    current: str,
    *,
    repo: Path = ROOT,
    code: str,
) -> None:
    if earlier == current:
        return
    cp = git(
        "merge-base",
        "--is-ancestor",
        earlier,
        current,
        cwd=repo,
        check=False,
    )
    if cp.returncode != 0:
        raise Stop(code)


def require_pre_gate_control_boundary(
    state: dict[str, Any],
    request: dict[str, Any],
    live_main: str,
    *,
    repo: Path = ROOT,
) -> dict[str, Any]:
    """Require one exact freshly verified pre-Gate-1 stopping point."""
    validate_control_state(state)
    if state.get("lifecycle_state") != "IDLE" or state.get("recovery_required"):
        raise Stop("EXPANSION_REBOOTSTRAP_CONTROL_NOT_IDLE")
    last = state.get("last_operation") or {}
    if last.get("operation") not in PRE_GATE1_OPERATIONS:
        raise Stop("EXPANSION_REBOOTSTRAP_NOT_PRE_GATE1")
    if last.get("fresh_runner_verification") != "PASS":
        raise Stop("EXPANSION_REBOOTSTRAP_PREDECESSOR_NOT_FRESH_VERIFIED")
    for field in ("school_key", "target_branch", "target_sha"):
        if last.get(field) != request.get(field):
            raise Stop(
                "EXPANSION_REBOOTSTRAP_PREDECESSOR_SCOPE_MISMATCH:" + field
            )
    prior_main = str(last.get("protected_main_sha") or "")
    if len(prior_main) != 40:
        raise Stop("EXPANSION_REBOOTSTRAP_PREDECESSOR_MAIN_INVALID")
    _require_linear_main_advance(
        prior_main,
        live_main,
        repo=repo,
        code="EXPANSION_REBOOTSTRAP_PREDECESSOR_MAIN_NOT_ANCESTOR",
    )
    return last


def _verify_phase0_lineage(
    request: dict[str, Any],
    control_commit: str,
) -> dict[str, Any]:
    phase0, phase0_bytes = _read_json_ref(
        control_commit,
        request["superseded_phase0_successor"],
        code="EXPANSION_REBOOTSTRAP_PHASE0_SUCCESSOR",
    )
    if (
        phase0.get("kind") != SUCCESSOR_KIND_PHASE0
        or phase0.get("operation") != OP_EXPANSION_PHASE0
        or phase0.get("school_key") != request["school_key"]
        or phase0.get("target_branch") != request["target_branch"]
        or phase0.get("integration_freeze_sha256")
        != request["superseded_integration_freeze_sha256"]
        or phase0.get("semantic_snapshot_sha256")
        != request["superseded_semantic_snapshot_sha256"]
        or phase0.get("repository_validation") != "PASS"
        or phase0.get("final_transaction_state") != "COMPLETE"
    ):
        raise Stop("EXPANSION_REBOOTSTRAP_PHASE0_SUCCESSOR_BINDING_MISMATCH")

    writeahead_path = str(phase0.get("writeahead_manifest_path") or "")
    writeahead_sha = str(phase0.get("writeahead_manifest_sha256") or "")
    if not writeahead_path or not writeahead_sha:
        raise Stop("EXPANSION_REBOOTSTRAP_PHASE0_WRITEAHEAD_REFERENCE_MISSING")
    writeahead_bytes = git_show_bytes(control_commit, writeahead_path)
    if sha256_bytes(writeahead_bytes) != writeahead_sha:
        raise Stop("EXPANSION_REBOOTSTRAP_PHASE0_WRITEAHEAD_HASH_MISMATCH")
    try:
        writeahead = json.loads(writeahead_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("EXPANSION_REBOOTSTRAP_PHASE0_WRITEAHEAD_JSON_INVALID") from exc
    checkpoint = request["expansion_research_checkpoint"]
    if (
        writeahead.get("operation") != OP_EXPANSION_PHASE0
        or writeahead.get("school_key") != request["school_key"]
        or writeahead.get("target_branch") != request["target_branch"]
        or writeahead.get("research_checkpoint_sha256")
        != request["research_freeze_sha256"]
        or writeahead.get("research_base_sha") != checkpoint["research_base_sha"]
        or writeahead.get("integration_freeze_sha256")
        != request["superseded_integration_freeze_sha256"]
        or writeahead.get("semantic_snapshot_sha256")
        != request["superseded_semantic_snapshot_sha256"]
    ):
        raise Stop("EXPANSION_REBOOTSTRAP_PHASE0_WRITEAHEAD_BINDING_MISMATCH")
    return {
        "successor": phase0,
        "successor_bytes": phase0_bytes,
        "writeahead": writeahead,
        "writeahead_bytes": writeahead_bytes,
    }


def authenticate_superseded_lineage(
    request: dict[str, Any],
    control_commit: str,
    live_main: str,
    *,
    state: dict[str, Any] | None = None,
    require_live_target: bool = True,
    repo: Path = ROOT,
) -> dict[str, Any]:
    """Authenticate the exact old expansion lineage without interpreting history."""
    if state is not None:
        require_pre_gate_control_boundary(
            state,
            request,
            live_main,
            repo=repo,
        )

    target = str(request["target_sha"])
    if require_live_target and remote_head(repo, request["target_branch"]) != target:
        raise Stop("EXPANSION_REBOOTSTRAP_TARGET_HEAD_MISMATCH")

    already_accepted = git(
        "merge-base",
        "--is-ancestor",
        target,
        live_main,
        cwd=repo,
        check=False,
    )
    if already_accepted.returncode == 0:
        raise Stop("EXPANSION_REBOOTSTRAP_NOT_REQUIRED_TARGET_ALREADY_IN_MAIN")

    phase0 = _verify_phase0_lineage(request, control_commit)

    current, current_bytes = _read_json_ref(
        control_commit,
        request["superseded_successor"],
        code="EXPANSION_REBOOTSTRAP_CURRENT_SUCCESSOR",
    )
    operation, verification_kind, equivalence_field = (
        successor_verification_contract(str(current.get("kind") or ""))
    )
    if (
        current.get("operation") != operation
        or current.get("school_key") != request["school_key"]
        or current.get("target_branch") != request["target_branch"]
        or current.get("actual_published_target_sha") != target
        or current.get("prepared_commit_sha") != target
        or current.get("integration_freeze_sha256")
        != request["superseded_integration_freeze_sha256"]
        or current.get("semantic_snapshot_sha256")
        != request["superseded_semantic_snapshot_sha256"]
        or current.get("repository_validation") != "PASS"
        or current.get("final_transaction_state") != "COMPLETE"
    ):
        raise Stop("EXPANSION_REBOOTSTRAP_CURRENT_SUCCESSOR_BINDING_MISMATCH")

    verification, verification_bytes = _read_json_ref(
        control_commit,
        request["superseded_successor_verification"],
        code="EXPANSION_REBOOTSTRAP_CURRENT_VERIFICATION",
    )
    if (
        verification.get("kind") != verification_kind
        or verification.get("request_id") != current.get("request_id")
        or verification.get("school_key") != request["school_key"]
        or verification.get("target_branch") != request["target_branch"]
        or verification.get("target_sha") != target
        or verification.get(equivalence_field) != "PASS"
    ):
        raise Stop("EXPANSION_REBOOTSTRAP_CURRENT_VERIFICATION_BINDING_MISMATCH")

    scratch = Path(tempfile.mkdtemp(prefix="expansion-rebootstrap-freeze-"))
    try:
        checkpoint = materialize_expansion_research_checkpoint(
            request,
            scratch / "expansion-research-frozen.zip",
        )
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    if (
        checkpoint["sha256"] != request["research_freeze_sha256"]
        or checkpoint["research_base_sha"]
        != request["expansion_research_checkpoint"]["research_base_sha"]
    ):
        raise Stop("EXPANSION_REBOOTSTRAP_RESEARCH_FREEZE_BINDING_MISMATCH")

    return {
        "phase0_successor": phase0["successor"],
        "current_successor": current,
        "current_successor_bytes": current_bytes,
        "current_verification": verification,
        "current_verification_bytes": verification_bytes,
        "current_successor_operation": operation,
        "research_checkpoint": checkpoint,
    }


def _bundle_ref_name(school_key: str, target_sha: str) -> str:
    return "refs/rebootstrap/%s/%s" % (school_key, target_sha[:16])


def verify_superseded_bundle(
    bundle_path: Path,
    *,
    expected_sha256: str,
    expected_target_sha: str,
    expected_ref: str,
    expected_merge_base_sha: str,
    repo: Path = ROOT,
) -> dict[str, Any]:
    if not bundle_path.is_file():
        raise Stop("EXPANSION_REBOOTSTRAP_BUNDLE_MISSING")
    if sha256_file(bundle_path) != expected_sha256:
        raise Stop("EXPANSION_REBOOTSTRAP_BUNDLE_HASH_MISMATCH")
    verification = git(
        "bundle",
        "verify",
        str(bundle_path.resolve()),
        cwd=repo,
        check=False,
    )
    if verification.returncode != 0:
        raise Stop("EXPANSION_REBOOTSTRAP_BUNDLE_VERIFY_FAILED")
    heads = git(
        "bundle",
        "list-heads",
        str(bundle_path.resolve()),
        cwd=repo,
    ).stdout.splitlines()
    exact = [line.split() for line in heads if line.strip()]
    if [expected_target_sha, expected_ref] not in exact:
        raise Stop("EXPANSION_REBOOTSTRAP_BUNDLE_HEAD_MISMATCH")
    if not expected_merge_base_sha or len(expected_merge_base_sha) != 40:
        raise Stop("EXPANSION_REBOOTSTRAP_BUNDLE_MERGE_BASE_INVALID")
    return {
        "bundle_sha256": expected_sha256,
        "target_sha": expected_target_sha,
        "bundle_ref": expected_ref,
        "merge_base_sha": expected_merge_base_sha,
    }


def create_superseded_bundle(
    *,
    repo: Path,
    school_key: str,
    target_sha: str,
    protected_main_sha: str,
    bundle_path: Path,
) -> dict[str, Any]:
    """Create an exact Git-object archive for the target-only lineage."""
    merge_base = git(
        "merge-base",
        target_sha,
        protected_main_sha,
        cwd=repo,
    ).stdout.strip()
    if not merge_base:
        raise Stop("EXPANSION_REBOOTSTRAP_MERGE_BASE_MISSING")
    ref_name = _bundle_ref_name(school_key, target_sha)
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    git("update-ref", ref_name, target_sha, cwd=repo)
    try:
        cp = git(
            "bundle",
            "create",
            str(bundle_path.resolve()),
            ref_name,
            "^" + merge_base,
            cwd=repo,
            check=False,
        )
        if cp.returncode != 0:
            raise Stop("EXPANSION_REBOOTSTRAP_BUNDLE_CREATE_FAILED")
    finally:
        git("update-ref", "-d", ref_name, cwd=repo, check=False)

    bundle_sha = sha256_file(bundle_path)
    return verify_superseded_bundle(
        bundle_path,
        expected_sha256=bundle_sha,
        expected_target_sha=target_sha,
        expected_ref=ref_name,
        expected_merge_base_sha=merge_base,
        repo=repo,
    )


def finalize_expansion_rebootstrap_successor(
    *,
    active: dict[str, Any],
    original_request: dict[str, Any],
    request_sha256: str,
    live_main: str,
    writeahead: dict[str, Any],
    writeahead_path: str,
    writeahead_sha256: str,
    writeahead_commit: str | None,
    expected_remote: str,
    publication_cas: str,
    extra_commit_paths: list[Path | str] | None = None,
    recovery_request_id: str | None = None,
    recovery_classification: str | None = None,
) -> str:
    rid = original_request["request_id"]
    school = original_request["school_key"]
    branch = original_request["target_branch"]
    prepared = writeahead["prepared_commit_sha"]
    if prepared != live_main:
        raise Stop("EXPANSION_REBOOTSTRAP_PREPARED_NOT_BOUND_MAIN")
    if remote_head(ROOT, branch) != prepared:
        raise Stop("EXPANSION_REBOOTSTRAP_TARGET_NOT_RESET_MAIN")

    successor_dir = Path(
        ".remote-implementation/successors/%s/%s" % (school, rid)
    )
    successor_dir.mkdir(parents=True, exist_ok=True)
    successor = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_EXPANSION_REBOOTSTRAP_SUCCESSOR",
        "operation": OP_EXPANSION_REBOOTSTRAP_FROM_FREEZE,
        "request_id": rid,
        "request_sha256": request_sha256,
        "school_key": school,
        "global_lock_commit": active.get("active_lock_commit"),
        "writeahead_commit": writeahead_commit,
        "writeahead_manifest_path": writeahead_path,
        "writeahead_manifest_sha256": writeahead_sha256,
        "protected_main_sha": live_main,
        "target_branch": branch,
        "expected_target_predecessor_sha": writeahead[
            "expected_target_predecessor_sha"
        ],
        "prepared_commit_sha": prepared,
        "prepared_tree_sha": writeahead["prepared_tree_sha"],
        "actual_published_target_sha": prepared,
        "superseded_bundle_path": writeahead["superseded_bundle_path"],
        "superseded_bundle_sha256": writeahead["superseded_bundle_sha256"],
        "superseded_bundle_ref": writeahead["superseded_bundle_ref"],
        "superseded_merge_base_sha": writeahead["superseded_merge_base_sha"],
        "research_freeze_sha256": writeahead["research_freeze_sha256"],
        "research_base_sha": writeahead["research_base_sha"],
        "superseded_integration_freeze_sha256": writeahead[
            "superseded_integration_freeze_sha256"
        ],
        "superseded_semantic_snapshot_sha256": writeahead[
            "superseded_semantic_snapshot_sha256"
        ],
        "publication_cas": publication_cas,
        "recovery_request_id": recovery_request_id,
        "recovery_classification": recovery_classification,
        "final_transaction_state": "COMPLETE",
    }
    successor_path = successor_dir / "successor-manifest.json"
    write_json(successor_path, successor)
    successor_sha = sha256_file(successor_path)

    final_state = finalize_success(
        active,
        request_id=rid,
        last_operation={
            "operation": OP_EXPANSION_REBOOTSTRAP_FROM_FREEZE,
            "request_id": rid,
            "school_key": school,
            "protected_main_sha": live_main,
            "target_branch": branch,
            "target_predecessor_sha": writeahead[
                "expected_target_predecessor_sha"
            ],
            "target_sha": prepared,
            "successor_manifest_path": successor_path.as_posix(),
            "successor_manifest_sha256": successor_sha,
            "writeahead_manifest_path": writeahead_path,
            "writeahead_manifest_sha256": writeahead_sha256,
            "superseded_bundle_sha256": writeahead[
                "superseded_bundle_sha256"
            ],
            "research_freeze_sha256": writeahead["research_freeze_sha256"],
            "fresh_runner_verification": "PENDING",
            "remote_expansion_rebootstrap_equivalence": "PENDING",
            "recovery_request_id": recovery_request_id,
            "recovery_classification": recovery_classification,
        },
    )
    if (
        recovery_request_id
        and recovery_request_id not in final_state["consumed_request_ids"]
    ):
        final_state["consumed_request_ids"].append(recovery_request_id)
    write_json(STATE_PATH, final_state)
    paths: list[Path | str] = [STATE_PATH, successor_dir]
    if extra_commit_paths:
        paths.extend(extra_commit_paths)
    return commit_control(
        expected_remote,
        "finalize expansion re-bootstrap %s" % rid,
        paths,
    )


def run_expansion_rebootstrap(
    *,
    state: dict[str, Any],
    request: dict[str, Any],
    request_bytes: bytes,
    request_commit: str,
    predecessor_commit: str,
    live_main: str,
) -> None:
    """Preserve the stale lineage, then CAS-reset only the onboarding ref."""
    authority = authenticate_superseded_lineage(
        request,
        predecessor_commit,
        live_main,
        state=state,
        require_live_target=True,
        repo=ROOT,
    )
    target_branch = request["target_branch"]
    target_before = request["target_sha"]

    git("fetch", "--no-tags", "origin", target_before, cwd=ROOT)
    git("fetch", "--no-tags", "origin", live_main, cwd=ROOT)

    run_id = os.environ.get("GITHUB_RUN_ID", "local")
    attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")
    active = begin_request(
        state,
        request,
        sha256_bytes(request_bytes),
        run_id=run_id,
        run_attempt=attempt,
        request_commit=request_commit,
    )
    write_json(STATE_PATH, active)
    request_archive = Path(
        ".remote-implementation/requests/%s/request.json"
        % request["request_id"]
    )
    request_archive.parent.mkdir(parents=True, exist_ok=True)
    request_archive.write_bytes(request_bytes)
    lock_commit = commit_control(
        request_commit,
        "acquire expansion re-bootstrap lock %s" % request["request_id"],
        [STATE_PATH, request_archive],
    )
    active = bind_lock_commit(active, lock_commit)
    write_json(STATE_PATH, active)
    lock_bound_commit = commit_control(
        lock_commit,
        "bind expansion re-bootstrap lock %s" % request["request_id"],
        [STATE_PATH],
    )

    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, target_branch) != target_before:
        raise Stop("EXPANSION_REBOOTSTRAP_TARGET_CHANGED_BEFORE_WRITEAHEAD")

    writeahead_dir = Path(
        ".remote-implementation/writeahead/%s/%s"
        % (request["school_key"], request["request_id"])
    )
    writeahead_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = writeahead_dir / "superseded-target.bundle"
    bundle = create_superseded_bundle(
        repo=ROOT,
        school_key=request["school_key"],
        target_sha=target_before,
        protected_main_sha=live_main,
        bundle_path=bundle_path,
    )
    lineage_proof = {
        "schema_version": 1,
        "kind": "EXPANSION_REBOOTSTRAP_SUPERSEDED_LINEAGE_PROOF",
        "school_key": request["school_key"],
        "target_branch": target_branch,
        "superseded_target_sha": target_before,
        "protected_main_sha": live_main,
        "current_successor_kind": authority["current_successor"].get("kind"),
        "current_successor_operation": authority[
            "current_successor_operation"
        ],
        "current_successor_request_id": authority[
            "current_successor"
        ].get("request_id"),
        "research_freeze_sha256": request["research_freeze_sha256"],
        "research_base_sha": request["expansion_research_checkpoint"][
            "research_base_sha"
        ],
        **bundle,
    }
    lineage_path = writeahead_dir / "superseded-lineage-proof.json"
    write_json(lineage_path, lineage_proof)

    tree = git(
        "rev-parse",
        live_main + "^{tree}",
        cwd=ROOT,
    ).stdout.strip()
    sidecars = {
        "superseded-target.bundle": sha256_file(bundle_path),
        "superseded-lineage-proof.json": sha256_file(lineage_path),
    }
    writeahead = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
        "operation": OP_EXPANSION_REBOOTSTRAP_FROM_FREEZE,
        "request_id": request["request_id"],
        "request_sha256": sha256_bytes(request_bytes),
        "school_key": request["school_key"],
        "global_lock_commit": lock_commit,
        "protected_main_sha": live_main,
        "target_branch": target_branch,
        "expected_target_predecessor_sha": target_before,
        "prepared_commit_sha": live_main,
        "prepared_tree_sha": tree,
        "changed_paths": [],
        "changed_file_sha256": {},
        "allowed_paths": [],
        "sidecars": sidecars,
        "superseded_bundle_path": (
            writeahead_dir / "superseded-target.bundle"
        ).as_posix(),
        "superseded_bundle_sha256": bundle["bundle_sha256"],
        "superseded_bundle_ref": bundle["bundle_ref"],
        "superseded_merge_base_sha": bundle["merge_base_sha"],
        "research_freeze_sha256": request["research_freeze_sha256"],
        "research_base_sha": request["expansion_research_checkpoint"][
            "research_base_sha"
        ],
        "superseded_integration_freeze_sha256": request[
            "superseded_integration_freeze_sha256"
        ],
        "superseded_semantic_snapshot_sha256": request[
            "superseded_semantic_snapshot_sha256"
        ],
        "mutation_state": "PREPARED_NOT_PUBLISHED",
    }
    writeahead_path = writeahead_dir / "writeahead-manifest.json"
    write_json(writeahead_path, writeahead)
    writeahead_sha = sha256_file(writeahead_path)

    active["transaction_state"] = "PREPARED_NOT_PUBLISHED"
    active["active_writeahead_path"] = writeahead_path.as_posix()
    active["active_writeahead_sha256"] = writeahead_sha
    active["active_prepared_commit_sha"] = live_main
    active["active_prepared_tree_sha"] = tree
    write_json(STATE_PATH, active)
    writeahead_commit = commit_control(
        lock_bound_commit,
        "publish expansion re-bootstrap write-ahead %s"
        % request["request_id"],
        [STATE_PATH, writeahead_dir],
    )
    active["active_writeahead_commit"] = writeahead_commit
    write_json(STATE_PATH, active)
    writeahead_bound_commit = commit_control(
        writeahead_commit,
        "bind expansion re-bootstrap write-ahead %s"
        % request["request_id"],
        [STATE_PATH],
    )

    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, target_branch) != target_before:
        raise Stop("EXPANSION_REBOOTSTRAP_TARGET_CHANGED_BEFORE_PUBLICATION")
    publish_ref_cas(
        ROOT,
        branch=target_branch,
        prepared_commit=live_main,
        expected_predecessor=target_before,
    )
    if remote_head(ROOT, target_branch) != live_main:
        raise Stop("EXPANSION_REBOOTSTRAP_TARGET_RESET_VERIFY_FAILED")

    commit = finalize_expansion_rebootstrap_successor(
        active=active,
        original_request=request,
        request_sha256=sha256_bytes(request_bytes),
        live_main=live_main,
        writeahead=writeahead,
        writeahead_path=writeahead_path.as_posix(),
        writeahead_sha256=writeahead_sha,
        writeahead_commit=writeahead_commit,
        expected_remote=writeahead_bound_commit,
        publication_cas="EXISTING_REF_CAS_PASS",
    )
    print(
        "REMOTE EXPANSION RE-BOOTSTRAP: COMPLETE "
        "superseded=%s reset_target=%s successor_commit=%s"
        % (target_before, live_main, commit)
    )


def verify_expansion_rebootstrap_equivalence(
    *,
    live_main: str,
    control_head: str,
    state: dict[str, Any],
    diag: Path,
) -> int:
    """Freshly prove the old lineage archive and exact ref reset."""
    last = state.get("last_operation") or {}
    if last.get("fresh_runner_verification") == "PASS":
        print("REMOTE EXPANSION RE-BOOTSTRAP EQUIVALENCE: PASS (already verified)")
        return 0

    successor_path = last["successor_manifest_path"]
    successor_bytes = git_show_bytes(control_head, successor_path)
    if sha256_bytes(successor_bytes) != last["successor_manifest_sha256"]:
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_SUCCESSOR_HASH_MISMATCH")
    successor = json.loads(successor_bytes)
    if (
        successor.get("kind")
        != "REMOTE_IMPLEMENTATION_EXPANSION_REBOOTSTRAP_SUCCESSOR"
        or successor.get("operation") != OP_EXPANSION_REBOOTSTRAP_FROM_FREEZE
    ):
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_SUCCESSOR_KIND_MISMATCH")

    bound_main = str(successor.get("protected_main_sha") or "")
    _require_linear_main_advance(
        bound_main,
        live_main,
        repo=ROOT,
        code="EXPANSION_REBOOTSTRAP_FRESH_MAIN_NOT_ANCESTOR",
    )
    branch = successor["target_branch"]
    if remote_head(ROOT, branch) != bound_main:
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_TARGET_REF_MISMATCH")

    request_path = (
        ".remote-implementation/requests/%s/request.json"
        % successor["request_id"]
    )
    request_bytes = git_show_bytes(control_head, request_path)
    if sha256_bytes(request_bytes) != successor["request_sha256"]:
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_REQUEST_HASH_MISMATCH")
    request = json.loads(request_bytes)

    authority = authenticate_superseded_lineage(
        request,
        control_head,
        live_main,
        state=None,
        require_live_target=False,
        repo=ROOT,
    )
    if (
        authority["current_successor"].get("prepared_commit_sha")
        != successor["expected_target_predecessor_sha"]
    ):
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_LINEAGE_TARGET_MISMATCH")

    writeahead_path = successor["writeahead_manifest_path"]
    writeahead_bytes = git_show_bytes(control_head, writeahead_path)
    if sha256_bytes(writeahead_bytes) != successor["writeahead_manifest_sha256"]:
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_WRITEAHEAD_HASH_MISMATCH")
    writeahead = json.loads(writeahead_bytes)
    if (
        writeahead.get("operation") != OP_EXPANSION_REBOOTSTRAP_FROM_FREEZE
        or writeahead.get("prepared_commit_sha") != bound_main
        or writeahead.get("expected_target_predecessor_sha")
        != request["target_sha"]
        or writeahead.get("changed_paths") != []
        or writeahead.get("changed_file_sha256") != {}
    ):
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_WRITEAHEAD_BINDING_MISMATCH")

    tree = git("rev-parse", bound_main + "^{tree}", cwd=ROOT).stdout.strip()
    if tree != writeahead.get("prepared_tree_sha"):
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_MAIN_TREE_MISMATCH")

    prefix = Path(writeahead_path).parent
    bundle_bytes = git_show_bytes(
        control_head,
        (prefix / "superseded-target.bundle").as_posix(),
    )
    expected_bundle_sha = (writeahead.get("sidecars") or {}).get(
        "superseded-target.bundle"
    )
    if sha256_bytes(bundle_bytes) != expected_bundle_sha:
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_BUNDLE_SIDECAR_MISMATCH")
    bundle_dir = Path(tempfile.mkdtemp(prefix="expansion-rebootstrap-fresh-"))
    try:
        bundle_path = bundle_dir / "superseded-target.bundle"
        bundle_path.write_bytes(bundle_bytes)
        bundle = verify_superseded_bundle(
            bundle_path,
            expected_sha256=successor["superseded_bundle_sha256"],
            expected_target_sha=successor["expected_target_predecessor_sha"],
            expected_ref=successor["superseded_bundle_ref"],
            expected_merge_base_sha=successor["superseded_merge_base_sha"],
            repo=ROOT,
        )
    finally:
        shutil.rmtree(bundle_dir, ignore_errors=True)

    assert_protected_main_unchanged(live_main)
    if remote_head(ROOT, branch) != bound_main:
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_TARGET_MOVED")

    verification = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_EXPANSION_REBOOTSTRAP_VERIFICATION",
        "request_id": successor["request_id"],
        "school_key": successor["school_key"],
        "protected_main_sha": bound_main,
        "observed_live_main_sha": live_main,
        "target_branch": branch,
        "superseded_target_sha": successor[
            "expected_target_predecessor_sha"
        ],
        "reset_target_sha": bound_main,
        "reset_target_tree_sha": tree,
        "superseded_bundle_sha256": bundle["bundle_sha256"],
        "superseded_bundle_ref": bundle["bundle_ref"],
        "superseded_merge_base_sha": bundle["merge_base_sha"],
        "research_freeze_sha256": successor["research_freeze_sha256"],
        "research_base_sha": successor["research_base_sha"],
        "tracked_basketball_mutation": "NONE",
        "remote_expansion_rebootstrap_equivalence": "PASS",
    }
    verify_dir = Path(
        ".remote-implementation/verifications/%s/%s"
        % (successor["school_key"], successor["request_id"])
    )
    write_json(
        verify_dir / "expansion-rebootstrap-verification.json",
        verification,
    )

    local = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    validate_control_state(local)
    current = local.get("last_operation") or {}
    if (
        current.get("operation") != OP_EXPANSION_REBOOTSTRAP_FROM_FREEZE
        or current.get("request_id") != successor["request_id"]
    ):
        raise Stop("EXPANSION_REBOOTSTRAP_FRESH_CONTROL_MOVED")
    current["fresh_runner_verification"] = "PASS"
    current["remote_expansion_rebootstrap_equivalence"] = "PASS"
    local["last_operation"] = current
    write_json(STATE_PATH, local)
    commit = commit_control(
        control_head,
        "persist fresh expansion re-bootstrap verification %s"
        % successor["request_id"],
        [STATE_PATH, verify_dir],
    )
    print(
        "REMOTE EXPANSION RE-BOOTSTRAP EQUIVALENCE: PASS "
        "verification_commit=%s" % commit
    )
    return 0
