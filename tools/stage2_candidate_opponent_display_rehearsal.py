#!/usr/bin/env python3
"""Exact blocked-census candidate-runtime replay for a recovered display repair.

This is a disposable, pre-merge proof. It never publishes UCF/school state,
reuses the unchanged permanent census/normalization helpers, and refuses stale
or ambiguous control, candidate, target and protected-main identities.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from remote_implementation_stage2_census import add_existing_onboarding_worktree  # noqa: E402
from remote_implementation_stage2_opponent_display import (  # noqa: E402
    apply_and_prepare_repair,
    post_repair_stage2_result,
    run_normalizer_dry_run,
    stage2_result_summary,
    verify_census_and_freeze_authority,
)


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True
    ).strip()


def json_file(path: Path) -> dict:
    return json.loads(path.read_bytes())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--control-checkout", type=Path, required=True)
    parser.add_argument("--candidate-checkout", type=Path, required=True)
    parser.add_argument("--candidate-sha", required=True)
    parser.add_argument("--control-commit", required=True)
    parser.add_argument("--pr-head-ref", required=True)
    parser.add_argument("--diag", type=Path, required=True)
    args = parser.parse_args()

    control = args.control_checkout.resolve()
    candidate = args.candidate_checkout.resolve()
    diag = args.diag.resolve()
    diag.mkdir(parents=True, exist_ok=True)
    for value in (args.candidate_sha, args.control_commit):
        require(bool(re.fullmatch(r"[0-9a-f]{40}", value)), "INVALID_SHA")
    require(git(control, "rev-parse", "HEAD") == args.control_commit,
            "CONTROL_CHECKOUT_CHANGED")
    require(git(candidate, "rev-parse", "HEAD") == args.candidate_sha,
            "CANDIDATE_CHECKOUT_CHANGED")
    require(args.pr_head_ref.startswith("tooling/stage2-display-"),
            "UNSUPPORTED_CANDIDATE_REHEARSAL_ROUTE")
    require(git(candidate, "ls-remote", "origin",
                "refs/heads/" + args.pr_head_ref).split()[0] == args.candidate_sha,
            "LIVE_PR_HEAD_CHANGED")

    state = json_file(control / ".remote-implementation/control-state.json")
    last = state.get("last_operation") or {}
    require(
        state.get("kind") == "REMOTE_IMPLEMENTATION_GLOBAL_CONTROL"
        and state.get("lifecycle_state") == "IDLE"
        and state.get("transaction_state") == "ABANDONED_NOT_ATTEMPTED"
        and state.get("recovery_required") is False
        and state.get("active_request_id") is None
        and last.get("operation") == "RECOVER"
        and last.get("disposition") == "ABANDONED_NOT_ATTEMPTED",
        "NOT_EXACT_SAFE_RECOVERY_BOUNDARY",
    )
    recovery = last.get("recovery_manifest") or {}
    failed_id = str(last.get("recovered_request_id") or "")
    require(bool(re.fullmatch(r"[a-z0-9][a-z0-9._-]+", failed_id)),
            "RECOVERED_REQUEST_ID_INVALID")
    require(recovery.get("recovered_request_id") == failed_id
            and recovery.get("mutation_classification") == "NOT_ATTEMPTED"
            and recovery.get("request_id") in state.get("consumed_request_ids", []),
            "RECOVERY_CLASSIFICATION_NOT_VERIFIED")
    school = failed_id.split("-expansion-stage2-opponent-display-normalize-")[0]
    require(bool(re.fullmatch(r"[a-z0-9][a-z0-9-]+", school)),
            "RECOVERED_SCHOOL_ID_INVALID")
    original_path = (control / ".remote-implementation/requests" /
                     failed_id / "request.json")
    original = json_file(original_path)
    require(original.get("operation") == "STAGE2_OPPONENT_DISPLAY_NORMALIZE"
            and original.get("request_id") == failed_id
            and original.get("school_key") == school
            and original.get("authority", {}).get("stage2_opponent_display_normalize") is True
            and original.get("target_branch") == "data/" + school + "-onboarding"
            and recovery.get("target_branch") == original["target_branch"]
            and recovery.get("actual_target_sha") == original.get("target_sha")
            and original["request_id"] in state.get("accepted_request_ids", []),
            "ORIGINAL_NORMALIZATION_AUTHORITY_MISMATCH")

    ref = original["stage2_census_checkpoint"]
    census_path = control / ref["path"]
    require(census_path.is_file()
            and census_path.resolve().is_relative_to(
                (control / ".remote-implementation/checkpoints" / school).resolve())
            and sha256(census_path) == ref["sha256"],
            "EXACT_CENSUS_HASH_MISMATCH")
    census = json_file(census_path)
    verification_path = (control / ".remote-implementation/verifications" / school /
                         census["request_id"] / "stage2-census-verification.json")
    verified = json_file(verification_path)
    require(
        verified.get("kind") == "REMOTE_IMPLEMENTATION_STAGE2_CENSUS_VERIFICATION"
        and verified.get("request_id") == census["request_id"]
        and verified.get("remote_stage2_census_equivalence") == "PASS"
        and verified.get("tracked_stage2_mutation") == "NONE"
        and verified.get("stage2_status") == "BLOCKED"
        and verified.get("target_sha") == original["target_sha"],
        "CENSUS_FRESH_EQUIVALENCE_MISSING",
    )
    require(
        original.get("expected_protected_main_sha")
            == git(candidate, "ls-remote", "origin", "refs/heads/main").split()[0]
        and recovery.get("protected_main_sha")
            == original["expected_protected_main_sha"],
        "CHANGED_PROTECTED_MAIN",
    )
    authority = verify_census_and_freeze_authority(
        original, args.control_commit, source_repo=control
    )
    blockers = authority["blocker_keys"]
    require(len(blockers) == int(census["preflight"]["blocker_count"])
            and int(census["preflight"]["warning_count"]) == 0
            and int(census["preflight"]["decision_count"]) == 0,
            "CENSUS_BLOCKER_POPULATION_INVALID")

    worktree = add_existing_onboarding_worktree(
        original["target_branch"], original["target_sha"], school,
        source_repo=candidate,
    )
    try:
        dry = run_normalizer_dry_run(
            worktree, school, authority["freeze_bytes"], blockers,
            diag, tool_repo=candidate,
        )
        require(
            sorted(item["canonical_opponent_key"]
                   for item in dry["report"]["changes"]) == blockers,
            "CANDIDATE_DRY_RUN_OPPONENT_KEYS_DIFFER",
        )
        off_census = sorted({
            item["normalized_opponent_key"]
            for item in dry["report"].get("source_game_display_changes", [])
        } - set(blockers))
        require(not off_census, "CANDIDATE_SOURCE_SYNC_OUTSIDE_CENSUS:" +
                ",".join(off_census))
        result = apply_and_prepare_repair(
            worktree, school, original["target_sha"], authority["freeze_bytes"],
            dry, blockers, diag, tool_repo=candidate,
        )
        proof = result["field_level_proof"]
        require(proof["source_game_non_name_field_changes"] == 0
                and proof["literal_evidence_changes"] == 0
                and proof["opponent_changed_keys"] == blockers
                and not set(proof["source_game_changed_keys"]) - set(blockers),
                "CANDIDATE_FIELD_PROOF_FAILED")
        regenerated = post_repair_stage2_result(
            worktree, school, authority["freeze_bytes"], diag,
            tool_repo=candidate,
        )
        stage2 = stage2_result_summary(regenerated)
        summary = {
            "kind": "CENSUS_BOUND_OPPONENT_DISPLAY_CANDIDATE_RUNTIME_REHEARSAL",
            "candidate_sha": args.candidate_sha,
            "control_commit": args.control_commit,
            "school_key": school,
            "target_predecessor": original["target_sha"],
            "protected_main_sha": original["expected_protected_main_sha"],
            "census_manifest_sha256": ref["sha256"],
            "census_blocker_keys": blockers,
            "dry_run_source_changed_keys": sorted({
                x["normalized_opponent_key"]
                for x in dry["report"].get("source_game_display_changes", [])
            }),
            "field_level_proof": proof,
            "post_repair_stage2": stage2,
            "tracked_publication": "NONE",
        }
        (diag / "candidate-opponent-display-summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        require(stage2["stage2_status"] == "CAPABILITY_CENSUS_READY"
                and stage2["blocker_count"] == 0,
                "CANDIDATE_POST_REPAIR_STAGE2_NOT_READY:" +
                str(stage2["stage2_status"]))
    finally:
        subprocess.run(["git", "-C", str(candidate), "worktree", "remove",
                        "--force", str(worktree)], check=True)

    require(git(candidate, "ls-remote", "origin",
                "refs/heads/" + args.pr_head_ref).split()[0] == args.candidate_sha
            and git(control, "ls-remote", "origin",
                    "refs/heads/control/remote-implementation").split()[0]
                == args.control_commit
            and git(candidate, "ls-remote", "origin",
                    "refs/heads/main").split()[0]
                == original["expected_protected_main_sha"],
            "POST_REHEARSAL_AUTHORITY_MOVED")
    print("EXACT_CENSUS_BOUND_CANDIDATE_REPLAY=PASS")
    print("OUTSIDE_CENSUS_SOURCE_ROW_CHANGES=ZERO")
    print("POST_REPAIR_STAGE2_CAPABILITY_CENSUS=READY")
    print("TRACKED_BASKETBALL_PUBLICATION=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
