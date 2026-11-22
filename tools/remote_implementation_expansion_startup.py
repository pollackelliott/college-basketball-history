#!/usr/bin/env python3
"""Prepare and queue one guarded All-History expansion Phase 0 request.

This is repository-owned orchestration for the initial serialized
ALL_HISTORY_EXPANSION Implementation phase. It performs only read-only
preparation against exact protected main, then writes durable control-plane
payloads and the ordinary EXPANSION_PHASE0 request. Basketball mutation remains
owned exclusively by the existing guarded EXPANSION_PHASE0 transaction.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from all_history_expansion_integration import (
    MANIFEST_NAME,
    PACKAGE_FILES,
    STAGE1_REPORT,
)
from remote_implementation_control import (
    canonical_json_bytes,
    sha256_bytes,
    sha256_file,
    validate_control_state,
    validate_request,
)
from remote_implementation_expansion_phase0 import (
    materialize_expansion_research_checkpoint,
)
from remote_implementation_io import (
    CONTROL_BRANCH,
    ROOT,
    STATE_PATH,
    Stop,
    assert_protected_main_unchanged,
    configure_git,
    fetch_operational_refs,
    git,
    push_control,
    remote_head,
    run,
)

STARTUP_PATH = Path(".remote-implementation/expansion-startup.json")
STARTUP_KIND = "REMOTE_IMPLEMENTATION_EXPANSION_STARTUP"
STARTUP_SCHEMA_VERSION = 1
DIAG = Path(
    os.environ.get(
        "REMOTE_IMPLEMENTATION_EXPANSION_STARTUP_DIAG",
        "/tmp/remote-expansion-startup",
    )
)
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
SCHOOL_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,127}$")


def require(condition: bool, code: str) -> None:
    if not condition:
        raise Stop(code)


def _sha(value: Any, length: int, code: str) -> str:
    text = str(value or "").strip().lower()
    pattern = HEX40 if length == 40 else HEX64
    require(bool(pattern.fullmatch(text)), code)
    return text


def validate_startup_intent(intent: dict[str, Any]) -> dict[str, Any]:
    """Validate one school-agnostic startup intent without granting mutation."""
    require(
        intent.get("schema_version") == STARTUP_SCHEMA_VERSION,
        "EXPANSION_STARTUP_SCHEMA_MISMATCH",
    )
    require(
        intent.get("kind") == STARTUP_KIND,
        "EXPANSION_STARTUP_KIND_MISMATCH",
    )
    startup_id = str(intent.get("startup_id") or "").strip()
    request_id = str(intent.get("phase0_request_id") or "").strip()
    school = str(intent.get("school_key") or "").strip()
    require(bool(ID_RE.fullmatch(startup_id)), "EXPANSION_STARTUP_ID_INVALID")
    require(
        bool(ID_RE.fullmatch(request_id)),
        "EXPANSION_STARTUP_PHASE0_REQUEST_ID_INVALID",
    )
    require(startup_id != request_id, "EXPANSION_STARTUP_ID_COLLISION")
    require(bool(SCHOOL_RE.fullmatch(school)), "EXPANSION_STARTUP_SCHOOL_INVALID")

    main_sha = _sha(
        intent.get("expected_protected_main_sha"),
        40,
        "EXPANSION_STARTUP_MAIN_INVALID",
    )
    target_sha = _sha(
        intent.get("target_sha"),
        40,
        "EXPANSION_STARTUP_TARGET_SHA_INVALID",
    )
    freeze_sha = _sha(
        intent.get("research_freeze_sha256"),
        64,
        "EXPANSION_STARTUP_FREEZE_SHA_INVALID",
    )
    target_branch = str(intent.get("target_branch") or "").strip()
    require(
        target_branch == f"data/{school}-onboarding",
        "EXPANSION_STARTUP_TARGET_BRANCH_INVALID",
    )

    checkpoint = intent.get("expansion_research_checkpoint")
    require(
        isinstance(checkpoint, dict),
        "EXPANSION_STARTUP_RESEARCH_CHECKPOINT_MISSING",
    )
    require(
        _sha(
            checkpoint.get("sha256"),
            64,
            "EXPANSION_STARTUP_CHECKPOINT_SHA_INVALID",
        )
        == freeze_sha,
        "EXPANSION_STARTUP_FREEZE_BINDING_MISMATCH",
    )
    research_base = _sha(
        checkpoint.get("research_base_sha"),
        40,
        "EXPANSION_STARTUP_RESEARCH_BASE_INVALID",
    )
    transport = checkpoint.get("transport")
    require(
        isinstance(transport, dict),
        "EXPANSION_STARTUP_TRANSPORT_MISSING",
    )
    require(
        transport.get("kind") == "git_base64_parts",
        "EXPANSION_STARTUP_TRANSPORT_KIND_INVALID",
    )
    transport_commit = _sha(
        transport.get("commit_sha"),
        40,
        "EXPANSION_STARTUP_TRANSPORT_COMMIT_INVALID",
    )
    prefix = str(transport.get("path_prefix") or "")
    require(
        prefix and ".." not in prefix and not prefix.startswith("/"),
        "EXPANSION_STARTUP_TRANSPORT_PREFIX_INVALID",
    )
    count = transport.get("part_count")
    require(
        type(count) is int and count > 0,
        "EXPANSION_STARTUP_TRANSPORT_PART_COUNT_INVALID",
    )

    provenance = intent.get("creation_provenance")
    require(
        isinstance(provenance, dict),
        "EXPANSION_STARTUP_PROVENANCE_MISSING",
    )
    require(
        bool(str(provenance.get("origin") or "").strip()),
        "EXPANSION_STARTUP_PROVENANCE_ORIGIN_MISSING",
    )
    require(
        bool(str(provenance.get("authorization") or "").strip()),
        "EXPANSION_STARTUP_PROVENANCE_AUTHORIZATION_MISSING",
    )

    venue = intent.get("venue_reconciliation")
    if venue is not None:
        require(
            isinstance(venue, dict),
            "EXPANSION_STARTUP_VENUE_RECONCILIATION_INVALID",
        )
        path = str(venue.get("path") or "")
        require(
            path and ".." not in path and not path.startswith("/"),
            "EXPANSION_STARTUP_VENUE_RECONCILIATION_PATH_INVALID",
        )
        _sha(
            venue.get("sha256"),
            64,
            "EXPANSION_STARTUP_VENUE_RECONCILIATION_SHA_INVALID",
        )

    return {
        "startup_id": startup_id,
        "phase0_request_id": request_id,
        "school_key": school,
        "expected_protected_main_sha": main_sha,
        "target_branch": target_branch,
        "target_sha": target_sha,
        "research_freeze_sha256": freeze_sha,
        "research_base_sha": research_base,
        "transport_commit": transport_commit,
    }


def require_startup_idle_control(state: dict[str, Any]) -> None:
    """Require a healthy idle global controller, including recovered terminal states."""
    validate_control_state(state)
    require(
        state.get("lifecycle_state") == "IDLE",
        "EXPANSION_STARTUP_CONTROL_NOT_IDLE",
    )
    require(
        state.get("recovery_required") is False,
        "EXPANSION_STARTUP_RECOVERY_REQUIRED",
    )
    for key in (
        "active_request_id",
        "active_school_key",
        "active_lock_owner",
        "active_lock_commit",
    ):
        require(
            state.get(key) is None,
            "EXPANSION_STARTUP_ACTIVE_CONTROL_FIELD:" + key,
        )


def _authority() -> dict[str, bool]:
    keys = (
        "owner_gate_1",
        "owner_gate_2",
        "phase0",
        "phase0_scope_supersession",
        "recovery",
        "release",
        "release_gate2_approval",
        "release_presentation_refresh",
        "release_preview_verify",
        "release_production_proof",
        "release_readiness",
        "stage2_census",
        "stage2_current_main_refresh",
        "stage2_gate1_fill",
        "stage2_gate1_seal",
        "stage2_opponent_display_normalize",
        "stage2_preseal_rehearsal",
        "stage2_proposal_rehearsal",
        "stage2_reconciliation_diagnostic",
        "stage2_sealed_apply",
        "venue_identity_maintenance",
        "expansion_phase0",
    )
    result = {key: False for key in keys}
    result["expansion_phase0"] = True
    return result


def candidate_hashes(root: Path) -> dict[str, str]:
    return {
        name: sha256_file(root / name)
        for name in (*PACKAGE_FILES, STAGE1_REPORT)
    }


def build_stage1_proof(
    report: dict[str, Any],
    candidate_root: Path,
    *,
    protected_main_sha: str,
    research_base_sha: str,
    freeze_zip_sha256: str,
) -> dict[str, Any]:
    """Build the exact generic proof consumed by Integration Freeze."""
    return {
        "status": "INDEPENDENTLY_REPRODUCED_READ_ONLY_STAGE1",
        "protected_main_sha": protected_main_sha,
        "research_base_sha": research_base_sha,
        "freeze_zip_sha256": freeze_zip_sha256,
        "candidate_sha256": candidate_hashes(candidate_root),
        "identity_counts": report["canonical_identity_census"]["counts"],
        "global_venue_counts": report["global_venue_reconciliation"]["counts"],
        "support_opponents": report["census"]["opponent_support_actions"],
        "support_venues": report["census"]["venue_support_actions"],
        "blockers": report["blockers"],
        "control_authority_sha": (
            (report.get("current_main_reconciliation") or {}).get(
                "control_authority_sha", ""
            )
        ),
        "integration_freeze_authorized": False,
    }


def require_stage1_control_authority(
    report: dict[str, Any],
    expected_control_sha: str,
) -> None:
    """Bind any inherited post-Freeze package correction to exact startup control."""
    reconciliation = report.get("current_main_reconciliation") or {}
    corrections = reconciliation.get("completed_package_corrections") or []
    if not corrections:
        return
    consumed = str(reconciliation.get("control_authority_sha") or "")
    require(
        consumed == expected_control_sha,
        "EXPANSION_STARTUP_STAGE1_CONTROL_AUTHORITY_MISMATCH",
    )
    require(
        all(
            str(item.get("control_authority_sha") or "") == expected_control_sha
            for item in corrections
        ),
        "EXPANSION_STARTUP_STAGE1_CORRECTION_CONTROL_AUTHORITY_MISMATCH",
    )


def build_phase0_request(
    intent: dict[str, Any],
    *,
    predecessor_commit: str,
    predecessor_state_sha256: str,
    proof_path: str,
    proof_sha256: str,
    integration_freeze_sha256: str,
    stage1_control_authority_sha: str,
    venue_reconciliation_ref: dict[str, str] | None,
) -> dict[str, Any]:
    meta = validate_startup_intent(intent)
    provenance = intent["creation_provenance"]
    request: dict[str, Any] = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_REQUEST",
        "request_id": meta["phase0_request_id"],
        "school_key": meta["school_key"],
        "operation": "EXPANSION_PHASE0",
        "previous_control_state_commit": predecessor_commit,
        "previous_control_state_sha256": predecessor_state_sha256,
        "expected_protected_main_sha": meta["expected_protected_main_sha"],
        "target_branch": meta["target_branch"],
        "target_sha": meta["target_sha"],
        "research_freeze_sha256": meta["research_freeze_sha256"],
        "stage1_independent_proof_sha256": proof_sha256,
        "stage1_control_authority_sha": stage1_control_authority_sha,
        "integration_freeze_sha256": integration_freeze_sha256,
        "expansion_research_checkpoint": intent[
            "expansion_research_checkpoint"
        ],
        "stage1_independent_proof": {
            "path": proof_path,
            "sha256": proof_sha256,
        },
        "creation_provenance": {
            "origin": str(provenance["origin"]).strip(),
            "authorization": (
                str(provenance["authorization"]).strip()
                + " Generic repository-owned expansion startup coordinator "
                "completed deterministic Stage 1 / Integration Freeze "
                "preparation; the child request authorizes only guarded "
                "EXPANSION_PHASE0."
            ),
        },
        "authority": _authority(),
    }
    if venue_reconciliation_ref is not None:
        request["venue_reconciliation"] = venue_reconciliation_ref
    validate_request(request)
    return request


def _run_acceptance() -> dict[str, Any]:
    cp = run(
        [
            sys.executable,
            str(
                ROOT
                / "tools"
                / "all_history_expansion_implementation_acceptance.py"
            ),
            "--json",
        ],
        cwd=ROOT,
        check=False,
    )
    try:
        payload = json.loads(cp.stdout)
    except json.JSONDecodeError as exc:
        raise Stop("EXPANSION_STARTUP_ACCEPTANCE_OUTPUT_INVALID") from exc
    summary = payload.get("summary") or {}
    if (
        cp.returncode != 0
        or summary.get("status") != "PASS"
        or summary.get("curated_lifecycle_suite") != "PASS"
    ):
        raise Stop(
            "EXPANSION_STARTUP_ACCEPTANCE_FAILED errors=%s"
            % (payload.get("errors") or [])
        )
    return payload


def _run_stage1(
    *,
    school: str,
    freeze: Path,
    freeze_sha: str,
    research_base: str,
    main_sha: str,
    output: Path,
) -> dict[str, Any]:
    cp = run(
        [
            sys.executable,
            str(ROOT / "tools" / "expansion_implementation_stage1.py"),
            school,
            str(freeze),
            "--expected-sha256",
            freeze_sha,
            "--research-base",
            research_base,
            "--main-sha",
            main_sha,
            "--repo",
            str(ROOT),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=False,
    )
    if cp.returncode != 0:
        raise Stop(
            "EXPANSION_STARTUP_STAGE1_FAILED\n" + cp.stdout[-10000:]
        )
    report_path = output / STAGE1_REPORT
    require(
        report_path.is_file(),
        "EXPANSION_STARTUP_STAGE1_REPORT_MISSING",
    )
    return json.loads(report_path.read_text(encoding="utf-8"))


def _require_deterministic_stage1(first: Path, second: Path) -> None:
    first_files = sorted(
        path.relative_to(first).as_posix()
        for path in first.rglob("*")
        if path.is_file()
    )
    second_files = sorted(
        path.relative_to(second).as_posix()
        for path in second.rglob("*")
        if path.is_file()
    )
    require(
        first_files == second_files,
        "EXPANSION_STARTUP_STAGE1_FILESET_NONDETERMINISTIC",
    )
    for relative in first_files:
        require(
            (first / relative).read_bytes()
            == (second / relative).read_bytes(),
            "EXPANSION_STARTUP_STAGE1_BYTES_NONDETERMINISTIC:"
            + relative,
        )


def _copy_payload(
    source: Path,
    directory: Path,
    name: str,
) -> tuple[Path, str]:
    destination = directory / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    return destination, sha256_file(destination)


def preserve_preintegration_diagnostics(
    stage1_dir: Path,
    proof_path: Path,
) -> None:
    """Preserve Stage 1 evidence before Integration Freeze can fail."""
    DIAG.mkdir(parents=True, exist_ok=True)
    _copy_payload(
        stage1_dir / STAGE1_REPORT,
        DIAG,
        "stage1-reconciliation.json",
    )
    _copy_payload(
        proof_path,
        DIAG,
        "stage1-independent-proof.json",
    )


def _dispatch_control_workflow() -> None:
    repository = str(os.environ.get("GITHUB_REPOSITORY") or "").strip()
    require(
        repository.count("/") == 1,
        "EXPANSION_STARTUP_GITHUB_REPOSITORY_MISSING",
    )
    cp = run(
        [
            "gh",
            "api",
            "--method",
            "POST",
            (
                f"repos/{repository}/actions/workflows/"
                "remote-implementation.yml/dispatches"
            ),
            "-f",
            f"ref={CONTROL_BRANCH}",
        ],
        check=False,
    )
    if cp.returncode != 0:
        raise Stop(
            "EXPANSION_STARTUP_CHILD_DISPATCH_FAILED\n"
            + cp.stdout[-5000:]
        )


def _persist_startup_payload(
    expected_remote: str,
    directory: Path,
    startup_id: str,
) -> str:
    git("add", "--", directory.as_posix())
    git(
        "commit",
        "-m",
        (
            "[remote-implementation-internal] persist expansion startup "
            f"preparation {startup_id}"
        ),
    )
    return push_control(expected_remote)


def run_startup() -> dict[str, Any]:
    configure_git()
    require(
        STARTUP_PATH.is_file(),
        "EXPANSION_STARTUP_INTENT_MISSING",
    )
    intent_bytes = STARTUP_PATH.read_bytes()
    intent = json.loads(intent_bytes)
    require(
        isinstance(intent, dict),
        "EXPANSION_STARTUP_INTENT_NOT_OBJECT",
    )
    meta = validate_startup_intent(intent)

    startup_commit = os.environ.get(
        "GITHUB_SHA",
        git("rev-parse", "HEAD").stdout.strip(),
    )
    require(
        bool(HEX40.fullmatch(startup_commit)),
        "EXPANSION_STARTUP_COMMIT_INVALID",
    )
    startup_parent = git(
        "rev-parse",
        f"{startup_commit}^",
    ).stdout.strip()
    require(
        meta["transport_commit"] == startup_parent,
        "EXPANSION_STARTUP_TRANSPORT_MUST_BE_IMMEDIATE_PREDECESSOR",
    )

    live_main, durable_head = fetch_operational_refs(
        meta["target_branch"],
        cwd=ROOT,
    )
    runtime_control_head = git(
        "rev-parse",
        "refs/remotes/origin/remote-control",
        cwd=ROOT,
    ).stdout.strip()
    require(
        runtime_control_head == durable_head,
        "EXPANSION_STARTUP_RUNTIME_CONTROL_REF_MISMATCH",
    )
    require(
        durable_head == startup_commit,
        "EXPANSION_STARTUP_CONTROL_MOVED_AFTER_EVENT",
    )
    require(
        live_main == meta["expected_protected_main_sha"],
        "EXPANSION_STARTUP_PROTECTED_MAIN_CHANGED",
    )

    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    require_startup_idle_control(state)
    used = set(state.get("accepted_request_ids") or [])
    used.update(state.get("consumed_request_ids") or [])
    used.update(state.get("abandoned_request_ids") or [])
    require(
        meta["phase0_request_id"] not in used,
        "EXPANSION_STARTUP_PHASE0_REQUEST_ID_ALREADY_USED",
    )

    actual_target = remote_head(ROOT, meta["target_branch"])
    require(
        actual_target == meta["target_sha"],
        "EXPANSION_STARTUP_TARGET_MOVED",
    )
    git(
        "fetch",
        "--no-tags",
        "origin",
        meta["target_sha"],
        cwd=ROOT,
    )
    ancestor = git(
        "merge-base",
        "--is-ancestor",
        meta["target_sha"],
        live_main,
        cwd=ROOT,
        check=False,
    )
    require(
        ancestor.returncode == 0,
        "EXPANSION_STARTUP_TARGET_NOT_ANCESTOR_OF_MAIN",
    )

    git(
        "fetch",
        "--no-tags",
        "origin",
        "+refs/heads/main:refs/remotes/origin/main",
        cwd=ROOT,
    )
    git(
        "fetch",
        "--no-tags",
        "origin",
        meta["research_base_sha"],
        cwd=ROOT,
    )
    require(
        git(
            "rev-parse",
            "refs/remotes/origin/main",
            cwd=ROOT,
        ).stdout.strip()
        == live_main,
        "EXPANSION_STARTUP_RUNTIME_MAIN_REF_MISMATCH",
    )

    DIAG.mkdir(parents=True, exist_ok=True)
    acceptance = _run_acceptance()
    acceptance_diag = DIAG / "implementation-acceptance.json"
    acceptance_diag.write_bytes(canonical_json_bytes(acceptance))

    scratch = Path(
        tempfile.mkdtemp(prefix="remote-expansion-startup-")
    )
    freeze = scratch / "expansion-research-frozen.zip"
    checkpoint_info = materialize_expansion_research_checkpoint(
        {
            "expansion_research_checkpoint":
            intent["expansion_research_checkpoint"]
        },
        freeze,
    )
    require(
        checkpoint_info["sha256"]
        == meta["research_freeze_sha256"],
        "EXPANSION_STARTUP_MATERIALIZED_FREEZE_MISMATCH",
    )

    venue_path: Path | None = None
    venue_ref: dict[str, str] | None = None
    if intent.get("venue_reconciliation") is not None:
        ref = intent["venue_reconciliation"]
        raw = git(
            "show",
            f"{meta['transport_commit']}:{ref['path']}",
            text=False,
        ).stdout
        require(
            sha256_bytes(raw) == ref["sha256"],
            (
                "EXPANSION_STARTUP_VENUE_RECONCILIATION_"
                "HASH_MISMATCH"
            ),
        )
        venue_path = scratch / "venue-reconciliation.json"
        venue_path.write_bytes(raw)

    stage1_a = scratch / "stage1-a"
    stage1_b = scratch / "stage1-b"
    _run_stage1(
        school=meta["school_key"],
        freeze=freeze,
        freeze_sha=meta["research_freeze_sha256"],
        research_base=meta["research_base_sha"],
        main_sha=live_main,
        output=stage1_a,
    )
    report = _run_stage1(
        school=meta["school_key"],
        freeze=freeze,
        freeze_sha=meta["research_freeze_sha256"],
        research_base=meta["research_base_sha"],
        main_sha=live_main,
        output=stage1_b,
    )
    _require_deterministic_stage1(stage1_a, stage1_b)
    require_stage1_control_authority(report, durable_head)

    proof = build_stage1_proof(
        report,
        stage1_b,
        protected_main_sha=live_main,
        research_base_sha=meta["research_base_sha"],
        freeze_zip_sha256=meta["research_freeze_sha256"],
    )
    proof_path = scratch / "stage1-independent-proof.json"
    proof_path.write_bytes(canonical_json_bytes(proof))
    proof_sha = sha256_file(proof_path)
    preserve_preintegration_diagnostics(stage1_b, proof_path)

    integration = scratch / "integration-freeze"
    cmd = [
        sys.executable,
        str(
            ROOT
            / "tools"
            / "all_history_expansion_integration.py"
        ),
        "freeze",
        meta["school_key"],
        str(freeze),
        "--expected-sha256",
        meta["research_freeze_sha256"],
        "--research-base",
        meta["research_base_sha"],
        "--main-sha",
        live_main,
        "--independent-proof",
        str(proof_path),
        "--independent-proof-sha256",
        proof_sha,
        "--repo",
        str(ROOT),
        "--output",
        str(integration),
    ]
    if venue_path is not None:
        cmd.extend(
            ["--venue-reconciliation", str(venue_path)]
        )
    cp = run(cmd, cwd=ROOT, check=False)
    if cp.returncode != 0:
        raise Stop(
            "EXPANSION_STARTUP_INTEGRATION_FREEZE_FAILED\n"
            + cp.stdout[-10000:]
        )
    integration_manifest = integration / MANIFEST_NAME
    require(
        integration_manifest.is_file(),
        "EXPANSION_STARTUP_INTEGRATION_FREEZE_MISSING",
    )
    integration_sha = sha256_file(integration_manifest)

    preview = scratch / "phase0-preview"
    cp = run(
        [
            sys.executable,
            str(
                ROOT
                / "tools"
                / "all_history_expansion_phase0_preview.py"
            ),
            "--repo",
            str(ROOT),
            "--integration-freeze",
            str(integration),
            "--output",
            str(preview),
        ],
        cwd=ROOT,
        check=False,
    )
    if cp.returncode != 0:
        raise Stop(
            "EXPANSION_STARTUP_PHASE0_PREVIEW_FAILED\n"
            + cp.stdout[-10000:]
        )
    preview_json = preview / "phase0-preview.json"
    require(
        preview_json.is_file(),
        "EXPANSION_STARTUP_PHASE0_PREVIEW_MISSING",
    )

    assert_protected_main_unchanged(live_main)
    require(
        remote_head(ROOT, meta["target_branch"])
        == meta["target_sha"],
        "EXPANSION_STARTUP_TARGET_MOVED_DURING_PREPARATION",
    )

    directory = Path(
        ".remote-implementation/startups/%s/%s"
        % (meta["school_key"], meta["startup_id"])
    )
    directory.mkdir(parents=True, exist_ok=False)
    (directory / "startup-intent.json").write_bytes(
        intent_bytes
    )
    _, acceptance_sha = _copy_payload(
        acceptance_diag,
        directory,
        "implementation-acceptance.json",
    )
    _, stage1_sha = _copy_payload(
        stage1_b / STAGE1_REPORT,
        directory,
        STAGE1_REPORT,
    )
    durable_proof, durable_proof_sha = _copy_payload(
        proof_path,
        directory,
        "stage1-independent-proof.json",
    )
    _, durable_integration_sha = _copy_payload(
        integration_manifest,
        directory,
        MANIFEST_NAME,
    )
    _, preview_sha = _copy_payload(
        preview_json,
        directory,
        "phase0-preview.json",
    )
    require(
        durable_proof_sha == proof_sha,
        "EXPANSION_STARTUP_PROOF_COPY_MISMATCH",
    )
    require(
        durable_integration_sha == integration_sha,
        "EXPANSION_STARTUP_FREEZE_COPY_MISMATCH",
    )

    if venue_path is not None:
        durable_venue, durable_venue_sha = _copy_payload(
            venue_path,
            directory,
            "venue-reconciliation.json",
        )
        venue_ref = {
            "path": durable_venue.as_posix(),
            "sha256": durable_venue_sha,
        }

    manifest = {
        "schema_version": 1,
        "kind": (
            "REMOTE_IMPLEMENTATION_EXPANSION_STARTUP_CHECKPOINT"
        ),
        "status": (
            "READY_TO_SUBMIT_GUARDED_EXPANSION_PHASE0"
        ),
        "startup_id": meta["startup_id"],
        "phase0_request_id": meta["phase0_request_id"],
        "school_key": meta["school_key"],
        "protected_main_sha": live_main,
        "research_base_sha": meta["research_base_sha"],
        "research_freeze_sha256": (
            meta["research_freeze_sha256"]
        ),
        "target_branch": meta["target_branch"],
        "target_sha": meta["target_sha"],
        "startup_intent_sha256": sha256_bytes(intent_bytes),
        "implementation_acceptance_sha256": acceptance_sha,
        "stage1_reconciliation_sha256": stage1_sha,
        "stage1_independent_proof_sha256": proof_sha,
        "stage1_control_authority_sha": durable_head,
        "integration_freeze_sha256": integration_sha,
        "phase0_preview_sha256": preview_sha,
        "tracked_basketball_mutation": (
            "NONE_PREPARATION_ONLY"
        ),
        "next_operation": "EXPANSION_PHASE0",
    }
    (directory / "checkpoint-manifest.json").write_bytes(
        canonical_json_bytes(manifest)
    )

    preparation_commit = _persist_startup_payload(
        startup_commit,
        directory,
        meta["startup_id"],
    )
    state_sha = sha256_bytes(STATE_PATH.read_bytes())

    request = build_phase0_request(
        intent,
        predecessor_commit=preparation_commit,
        predecessor_state_sha256=state_sha,
        proof_path=durable_proof.as_posix(),
        proof_sha256=proof_sha,
        integration_freeze_sha256=integration_sha,
        stage1_control_authority_sha=durable_head,
        venue_reconciliation_ref=venue_ref,
    )
    request_path = Path(
        ".remote-implementation/request.json"
    )
    request_path.write_bytes(canonical_json_bytes(request))
    git("add", "--", request_path.as_posix())
    git(
        "commit",
        "-m",
        (
            "Queue guarded expansion Phase 0 request "
            + meta["phase0_request_id"]
        ),
    )
    request_commit = push_control(preparation_commit)
    _dispatch_control_workflow()

    return {
        "status": "EXPANSION_STARTUP_PHASE0_QUEUED",
        "school_key": meta["school_key"],
        "startup_id": meta["startup_id"],
        "phase0_request_id": meta["phase0_request_id"],
        "protected_main_sha": live_main,
        "target_sha": meta["target_sha"],
        "stage1_independent_proof_sha256": proof_sha,
        "integration_freeze_sha256": integration_sha,
        "preparation_commit": preparation_commit,
        "request_commit": request_commit,
    }


def main() -> int:
    DIAG.mkdir(parents=True, exist_ok=True)
    try:
        result = run_startup()
        print(json.dumps(result, sort_keys=True))
        return 0
    except (
        Stop,
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        (DIAG / "stop.txt").write_text(
            str(exc) + "\n",
            encoding="utf-8",
        )
        print("STOP: %s" % exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
