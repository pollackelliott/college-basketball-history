#!/usr/bin/env python3
"""Read-only contract adapter for a future serialized expansion Phase 0.

NOT a runner, publisher, recovery handler or independent verifier. Reuse the
existing remote Implementation controller's primitive lock/CAS/recovery
functions; refuse operation authoring or tracked mutation before those paths
are integrated with exact runtime and fresh-verifier code.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from all_history_expansion_integration import (
    MANIFEST_NAME, PACKAGE_FILES, STAGE1_REPORT, IntegrationAuthorityError,
    canonical_bytes, sha256, verify_manifest_bytes,
)
from all_history_expansion_venue_guard import require_clean
from remote_implementation_control import (
    MUTATION_COMPLETE, MUTATION_DIVERGED, MUTATION_NOT_ATTEMPTED,
    MUTATION_PREPARED, MUTATION_PUBLISHED, begin_request, bind_lock_commit,
    classify_mutation, classify_publication_precondition, initial_control_state,
    validate_control_state,
)

OP_EXPANSION_PHASE0 = "EXPANSION_PHASE0"
MUTABLE_GLOBALS = frozenset({
    "data/reference/programs.csv",
    "data/reference/venues.csv",
    "data/reference/venue-names.csv",
})


def require(ok: Any, code: str) -> None:
    if not ok:
        raise IntegrationAuthorityError(code)


def exact_paths(school: str) -> frozenset[str]:
    return MUTABLE_GLOBALS | frozenset(
        f"schools/{school}/{name}" for name in PACKAGE_FILES
    )


def authenticate_intent(
    *,
    request: dict[str, Any],
    current_main: str,
    current_target: str,
    target_is_ancestor_of_main: bool,
    freeze: Path,
    phase0_preview: Path,
    original_research_sha256: str,
    accepted_stage1_proof_sha256: str,
    exact_freeze_manifest_sha256: str,
) -> dict[str, Any]:
    """Inspect a future proposal without starting a remote transaction."""
    authority=request.get("authority")
    require(request.get("operation")==OP_EXPANSION_PHASE0,
            "EXPANSION_OPERATION_WRONG")
    require(isinstance(authority,dict) and
            authority.get("expansion_phase0") is True,
            "EXPANSION_PHASE0_EXPLICIT_AUTHORITY_REQUIRED")
    require(all(authority.get(flag) is False for flag in
                ("owner_gate_1","owner_gate_2","release","stage2_census",
                 "phase0","recovery","stage2_sealed_apply")),
            "EXPANSION_FORBIDS_UNRELATED_OPERATION_AUTHORITY")
    school=request.get("school_key")
    require(isinstance(school,str) and school and
            all(c.islower() or c.isdigit() or c=="-" for c in school),
            "EXPANSION_SCHOOL_KEY_INVALID")
    require(request.get("target_branch")==f"data/{school}-onboarding",
            "EXPANSION_TARGET_MUST_REUSE_SERIALIZED_SCHOOL_BRANCH")
    require(request.get("expected_protected_main_sha")==current_main,
            "EXPANSION_CURRENT_MAIN_MOVED")
    require(request.get("target_sha")==current_target,
            "EXPANSION_EXPECTED_TARGET_PREDECESSOR_CHANGED")
    require(bool(target_is_ancestor_of_main),
            "EXPANSION_TARGET_PREDECESSOR_NOT_ACCEPTED_IN_MAIN")
    # Explicitly bind the active published baseline to the new worktree
    # without creating a second parallel target branch.
    manifest=verify_manifest_bytes((freeze/MANIFEST_NAME).read_bytes(),freeze)
    raw=(freeze/MANIFEST_NAME).read_bytes()
    require(sha256(raw)==exact_freeze_manifest_sha256==
            request.get("integration_freeze_sha256"),
            "EXPANSION_INTEGRATION_FREEZE_SHA_MISMATCH")
    require(manifest["protected_main_sha"]==current_main,
            "EXPANSION_FREEZE_MAIN_CHANGED")
    require(manifest["school_key"]==school,
            "EXPANSION_FREEZE_SCHOOL_MISMATCH")
    require(manifest["research_freeze_zip_sha256"]==original_research_sha256==
            request.get("research_freeze_sha256"),
            "EXPANSION_ORIGINAL_RESEARCH_FREEZE_MISMATCH")
    require(manifest["independent_stage1_proof_sha256"]==
            accepted_stage1_proof_sha256==
            request.get("stage1_independent_proof_sha256"),
            "EXPANSION_INDEPENDENT_STAGE1_PROOF_CHANGED")
    require(manifest["canonical_identity_counts"].get("IDENTITY_REVIEW_BLOCKER")==0,
            "EXPANSION_CANONICAL_AMBIGUITY")
    require(manifest["global_venue_reconciliation"].get(
            "GLOBAL_VENUE_IDENTITY_REVIEW_BLOCKER")==0,
            "EXPANSION_STAGE1_VENUE_IDENTITY_BLOCKED")
    raw_preview=(phase0_preview/"phase0-preview.json").read_bytes()
    preview=json.loads(raw_preview)
    require(preview.get("status")=="DISPOSABLE_ONLY_NOT_PUBLISHED",
            "EXPANSION_PHASE0_PREVIEW_STATUS_INVALID")
    require(preview.get("integration_freeze_sha256")==sha256(raw),
            "EXPANSION_PHASE0_PREVIEW_FREEZE_HASH_MISMATCH")
    require(preview.get("protected_main_sha")==current_main,
            "EXPANSION_PHASE0_PREVIEW_MAIN_CHANGED")
    require(preview.get("school_key")==school,
            "EXPANSION_PHASE0_PREVIEW_SCHOOL_CHANGED")
    require(preview.get("source_game_count")==
            manifest["source_preservation"]["combined_count"],
            "EXPANSION_PHASE0_SOURCE_COUNT_CHANGED")
    require(preview.get("inherited_source_game_count")==
            manifest["source_preservation"]["inherited_count"],
            "EXPANSION_PHASE0_INHERITED_COUNT_CHANGED")
    require(preview.get("supplemental_source_game_count")==
            manifest["source_preservation"]["supplemental_count"],
            "EXPANSION_PHASE0_SUPPLEMENTAL_COUNT_CHANGED")
    require(preview.get("global_venue_registration_count")==
            manifest["global_venue_reconciliation"]["NEW_GLOBAL_VENUE_REGISTRATION_REQUIRED"],
            "EXPANSION_GLOBAL_VENUE_REGISTRATION_DRIFT")
    require(preview.get("authorized_live_mutation") is False and
            preview.get("branch_published") is False and
            preview.get("lock_acquired") is False,
            "EXPANSION_PREVIEW_UNEXPECTED_MUTATION_CLAIM")
    # The pre-registration guard must be rerun before any live transaction.
    # Preview created before the guard existed has no such authority.
    require_clean(preview.get("venue_identity_census",{}))
    require(preview["venue_identity_census"]["new_support_count"]==
            manifest["venue_support_actions"]["NEW_SUPPLEMENTAL"],
            "EXPANSION_NEW_VENUE_POPULATION_CHANGED")
    require(preview["permitted_new_coverage_status"]=="COMPLETE_INSTITUTIONAL",
            "EXPANSION_METADATA_TARGET_INVALID")
    require(preview["protected_top_level_and_accomplishments"]=="UNCHANGED",
            "EXPANSION_TOP_LEVEL_OR_ACCOMPLISHMENTS_CHANGED")
    expected=exact_paths(school)
    require(set(preview["six_file_preview_sha256"])==set(PACKAGE_FILES),
            "EXPANSION_SIX_FILE_PREVIEW_INCOMPLETE")
    require(set(preview["global_reference_preview_sha256"])==MUTABLE_GLOBALS,
            "EXPANSION_GLOBAL_PREVIEW_PATHS_FORBIDDEN")
    for name,digest in preview["six_file_preview_sha256"].items():
        require(sha256((phase0_preview/name).read_bytes())==digest,
                "EXPANSION_PHASE0_CANDIDATE_TAMPERED:"+name)
    for name,digest in preview["global_reference_preview_sha256"].items():
        require(sha256((phase0_preview/"references"/Path(name).name).read_bytes())==digest,
                "EXPANSION_PHASE0_GLOBAL_CANDIDATE_TAMPERED:"+name)
    return {
        "schema_version":1,"kind":"EXPANSION_GUARDED_PHASE0_TRANSACTION_INTENT",
        "status":"RECONCILED_PREPARATION_ONLY",
        "school_key":school,"protected_main_sha":current_main,
        "expected_target_predecessor_sha":current_target,
        "integration_freeze_sha256":sha256(raw),
        "research_freeze_sha256":original_research_sha256,
        "stage1_proof_sha256":accepted_stage1_proof_sha256,
        "source_game_count":preview["source_game_count"],
        "canonical_identity_counts":manifest["canonical_identity_counts"],
        "allowed_changed_paths":sorted(expected),
        "projected_package_sha256":preview["six_file_preview_sha256"],
        "projected_global_sha256":preview["global_reference_preview_sha256"],
        "stage2_authority":False,"owner_gate_authority":False,
        "live_mutation_authority":False,
    }


def prove_lock_contract(state:dict[str,Any],request:dict[str,Any],
                        request_bytes:bytes,
                        request_commit:str,lock_commit:str) -> dict[str,Any]:
    """Use existing serialized lock semantics without writing control state."""
    validate_control_state(state)
    require(state["lifecycle_state"]=="IDLE", "EXPANSION_GLOBAL_LOCK_OCCUPIED")
    current=begin_request(state,request,sha256(request_bytes),
                          run_id="disposable-test",
                          run_attempt="1",request_commit=request_commit)
    require(current["active_lock_owner"] is not None and
            current["lifecycle_state"]=="ACTIVE",
            "EXPANSION_LOCK_NOT_ACTIVE")
    current=bind_lock_commit(current,lock_commit)
    require(current["active_lock_commit"]==lock_commit,
            "EXPANSION_LOCK_COMMIT_NOT_BOUND")
    return current


def inspect_recovery(*, expected_target_predecessor: str,
                     actual_target: str,
                     writeahead: dict[str,Any]|None,
                     successor:dict[str,Any]|None=None) -> dict[str,str]:
    """Reuse exact controller classification, never republish a completed op."""
    result=classify_mutation(expected_target_predecessor,actual_target,
                             manifest=writeahead,successor=successor)
    if result==MUTATION_DIVERGED:
        raise IntegrationAuthorityError("EXPANSION_RECOVERY_DIVERGED_STOP")
    action={
        MUTATION_NOT_ATTEMPTED:"ABANDON_WITHOUT_PUBLICATION",
        MUTATION_PREPARED:"ABANDON_PREPARED_UNPUBLISHED",
        MUTATION_PUBLISHED:"ADOPT_ONLY_AFTER_EXACT_PREPARED_TREE_REPLAY",
        MUTATION_COMPLETE:"NO_REAPPLICATION_PERMITTED",
    }[result]
    return {"mutation_classification":result,"safe_next_action":action}


def check_cas(*, predecessor: str, observed: str, prepared: str) -> None:
    status=classify_publication_precondition(
        expected_predecessor=predecessor,actual_target=observed,
        prepared_commit=prepared)
    require(status=="PUBLICATION_ALLOWED", "EXPANSION_TARGET_CAS_REFUSED")


def verify_exact_prepared(
    *,
    intent:dict[str,Any],
    prepared_parent_sha:str,
    prepared_tree_sha:str,
    replay_tree_sha:str,
    changed_paths:list[str],
    committed_files_sha256:dict[str,str],
    inherited_rows_preserved:bool,
    semantic_guard_hash:str,
) -> dict[str,Any]:
    """Compare independently read Git tree evidence, no publication action."""
    require(prepared_parent_sha==intent["protected_main_sha"],
            "EXPANSION_PREPARED_MAIN_PARENT_CHANGED")
    require(prepared_tree_sha==replay_tree_sha,
            "EXPANSION_INDEPENDENT_TREE_MISMATCH")
    require(bool(inherited_rows_preserved),
            "EXPANSION_INHERITED_ROWS_CHANGED")
    require(bool(semantic_guard_hash) and len(semantic_guard_hash)==64,
            "EXPANSION_SEMANTIC_HASH_MISSING")
    require(sorted(changed_paths)==sorted(set(changed_paths)),
            "EXPANSION_CHANGED_PATHS_DUPLICATE")
    # A complete six-file candidate need not change every inherited member.
    # The six expected file hashes below must all be present on the prepared
    # commit; require only the expanded source game ledger to actually change.
    require(f"schools/{intent['school_key']}/source-games.csv" in changed_paths,
            "EXPANSION_SOURCE_GAME_PACKAGE_NOT_UPDATED")
    require(set(changed_paths)<=set(intent["allowed_changed_paths"]),
            "EXPANSION_CHANGED_PATH_OUTSIDE_ALLOWLIST")
    expected={f"schools/{intent['school_key']}/{name}":digest
              for name,digest in intent["projected_package_sha256"].items()}
    expected.update(intent["projected_global_sha256"])
    require(all(committed_files_sha256.get(k)==v for k,v in expected.items()),
            "EXPANSION_PREPARED_BLOB_HASH_MISMATCH")
    return {"status":"INDEPENDENT_DISPOSABLE_PREPARED_TREE_EQUIVALENCE",
            "protected_main_sha":prepared_parent_sha,
            "prepared_tree_sha":prepared_tree_sha,
            "changed_paths":sorted(changed_paths),
            "school_key":intent["school_key"],
            "semantic_snapshot_sha256":semantic_guard_hash,
            "publish_authority":False}
