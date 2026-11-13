#!/usr/bin/env python3
"""Replay one durable blocked Stage-2 proposal against candidate tooling.

This is a read-only pre-merge repair gate. It authenticates the exact blocked
proposal/checkpoint on the remote control branch, recreates the exact onboarding
worktree and Integration Freeze, then runs the candidate runtime's permanent
implementation_stage2.py against the preserved recommendation map.

The tool never updates protected main, the onboarding branch, or remote control.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from remote_implementation_io import Stop, git_show_bytes, sha256_bytes
from remote_implementation_stage2_census import (
    add_existing_onboarding_worktree,
    run_stage2_census_tool,
)
from remote_implementation_stage2_proposal import (
    run_stage2_proposal_tool,
    verify_stage2_proposal_authority,
)


ALLOWED_CANDIDATE_PATHS = (
    "tools/",
    "tests/",
    "docs/",
    ".github/workflows/",
)
ALLOWED_CANDIDATE_FILES = {"AGENTS.md"}
STAGE2_STATUS = "implementation-stage2-status.json"


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
        raise Stop("CANDIDATE_REHEARSAL_GIT_FAILED:" + " ".join(args) + "\n" + cp.stdout)
    return cp


def candidate_changed_paths(
    candidate_repo: Path,
    base_sha: str,
    candidate_sha: str,
) -> list[str]:
    ancestry = _run_git(
        candidate_repo,
        "merge-base",
        "--is-ancestor",
        base_sha,
        candidate_sha,
        check=False,
    )
    if ancestry.returncode != 0:
        raise Stop("CANDIDATE_REHEARSAL_BASE_NOT_ANCESTOR")
    cp = _run_git(
        candidate_repo,
        "diff",
        "--name-only",
        f"{base_sha}..{candidate_sha}",
    )
    return [line.strip() for line in cp.stdout.splitlines() if line.strip()]


def validate_candidate_scope(paths: list[str]) -> None:
    disallowed = [
        path
        for path in paths
        if path not in ALLOWED_CANDIDATE_FILES
        and not any(path.startswith(prefix) for prefix in ALLOWED_CANDIDATE_PATHS)
    ]
    if disallowed:
        raise Stop(
            "CANDIDATE_REHEARSAL_NON_TOOLING_PATHS:"
            + ",".join(sorted(disallowed))
        )


SITE_BLOCKER_KEYS = (
    "strict_home_gap_rows",
    "strict_ncaa_gap_rows",
    "target_source_information_loss",
    "reciprocal_unpropagated",
    "unaccounted_public_gap_rows",
    "invalid_home_venue_exception_marker_rows",
)


def _site_blocker_signature(site_diagnostic: Any) -> dict[str, Any] | None:
    """Return the structured publication-blocker population for one site diagnostic."""

    if not isinstance(site_diagnostic, dict):
        return None
    counts = site_diagnostic.get("counts")
    examples = site_diagnostic.get("examples")
    if not isinstance(counts, dict) or not isinstance(examples, dict):
        return None

    signature: dict[str, Any] = {}
    for key in SITE_BLOCKER_KEYS:
        raw_count = counts.get(key, 0)
        try:
            count = int(raw_count or 0)
        except (TypeError, ValueError):
            return None
        raw_examples = examples.get(key, [])
        if raw_examples is None:
            raw_examples = []
        if not isinstance(raw_examples, list):
            return None
        normalized_examples = sorted(
            str(value).strip()
            for value in raw_examples
            if str(value).strip()
        )
        if count or normalized_examples:
            signature[key] = {
                "count": count,
                "examples": normalized_examples,
            }
    return signature


def classify_candidate_result(
    baseline_status: dict[str, Any],
    candidate_result: dict[str, Any],
) -> str:
    candidate_status = str(candidate_result.get("stage2_status") or "")
    if candidate_status == "OWNER_GATE_1_READY":
        return "RESOLVED_TO_GATE1"
    if candidate_status != "BLOCKED":
        raise Stop("CANDIDATE_REHEARSAL_UNSUPPORTED_STAGE2_STATUS:" + candidate_status)

    baseline_error = str(baseline_status.get("last_error") or "").strip()
    candidate_error = str((candidate_result.get("status") or {}).get("last_error") or "").strip()
    if baseline_error and candidate_error == baseline_error:
        baseline_site = _site_blocker_signature(
            baseline_status.get("site_diagnostic")
        )
        candidate_site = _site_blocker_signature(
            candidate_result.get("site_diagnostic")
        )
        if (
            baseline_site is not None
            and candidate_site is not None
            and baseline_site != candidate_site
        ):
            return "ADVANCED_TO_DIFFERENT_BLOCKER"
        return "NO_PROGRESS_SAME_BLOCKER"
    return "ADVANCED_TO_DIFFERENT_BLOCKER"


def candidate_census_decision_universe(
    candidate_result: dict[str, Any],
) -> str:
    """Return the candidate census decision-universe fingerprint or fail closed."""
    status = candidate_result.get("status") or {}
    preflight = status.get("preflight") or {}
    value = str(preflight.get("decision_universe_sha256") or "").strip()
    if len(value) != 64:
        raise Stop("CANDIDATE_REHEARSAL_DECISION_UNIVERSE_MISSING")
    return value


def _load_json_at(
    source_repo: Path,
    commit: str,
    path: str,
) -> tuple[dict[str, Any], bytes]:
    data = git_show_bytes(commit, path, cwd=source_repo)
    try:
        obj = json.loads(data)
    except json.JSONDecodeError as exc:
        raise Stop("CANDIDATE_REHEARSAL_JSON_INVALID:" + path) from exc
    if not isinstance(obj, dict):
        raise Stop("CANDIDATE_REHEARSAL_JSON_OBJECT_REQUIRED:" + path)
    return obj, data


def _materialize(
    source_repo: Path,
    commit: str,
    path: str,
    expected_sha256: str,
    destination: Path,
) -> Path:
    data = git_show_bytes(commit, path, cwd=source_repo)
    if sha256_bytes(data) != expected_sha256:
        raise Stop("CANDIDATE_REHEARSAL_PAYLOAD_HASH_MISMATCH:" + path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return destination


def run_candidate_rehearsal(
    *,
    source_repo: Path,
    candidate_runtime: Path,
    candidate_sha: str,
    control_commit: str,
    proposal_checkpoint_path: str,
    diag: Path,
) -> dict[str, Any]:
    actual_candidate = _run_git(candidate_runtime, "rev-parse", "HEAD").stdout.strip()
    if actual_candidate != candidate_sha:
        raise Stop(
            "CANDIDATE_REHEARSAL_HEAD_MISMATCH:"
            f"expected={candidate_sha}:actual={actual_candidate}"
        )

    manifest, _ = _load_json_at(source_repo, control_commit, proposal_checkpoint_path)
    if manifest.get("kind") != "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_CHECKPOINT":
        raise Stop("CANDIDATE_REHEARSAL_CHECKPOINT_KIND_MISMATCH")
    if manifest.get("stage2_status") != "BLOCKED":
        raise Stop("CANDIDATE_REHEARSAL_SOURCE_CHECKPOINT_NOT_BLOCKED")

    directory = Path(proposal_checkpoint_path).parent
    request_path = (directory / "request.json").as_posix()
    request, request_bytes = _load_json_at(source_repo, control_commit, request_path)
    if request.get("request_id") != manifest.get("request_id"):
        raise Stop("CANDIDATE_REHEARSAL_REQUEST_ID_MISMATCH")
    expected_request_sha = str(manifest.get("request_sha256") or "")
    if expected_request_sha and sha256_bytes(request_bytes) != expected_request_sha:
        raise Stop("CANDIDATE_REHEARSAL_REQUEST_HASH_MISMATCH")

    base_sha = str(request.get("expected_protected_main_sha") or "")
    if len(base_sha) != 40:
        raise Stop("CANDIDATE_REHEARSAL_BASE_SHA_INVALID")
    changed_paths = candidate_changed_paths(candidate_runtime, base_sha, candidate_sha)
    validate_candidate_scope(changed_paths)

    authority = verify_stage2_proposal_authority(
        request,
        control_commit,
        source_repo=source_repo,
    )

    baseline_status_path = (directory / STAGE2_STATUS).as_posix()
    baseline_status, _ = _load_json_at(
        source_repo,
        control_commit,
        baseline_status_path,
    )

    scratch = Path(tempfile.mkdtemp(prefix="stage2-candidate-rehearsal-"))
    map_ref = str(manifest.get("recommendation_map_checkpoint_path") or "")
    map_sha = str(manifest.get("recommendation_map_sha256") or "")
    if not map_ref or len(map_sha) != 64:
        raise Stop("CANDIDATE_REHEARSAL_MAP_REFERENCE_MISSING")
    map_path = _materialize(
        source_repo,
        control_commit,
        map_ref,
        map_sha,
        scratch / "recommendation-map.json",
    )

    challenge_path = None
    challenge_ref = authority.get("historical_game_type_challenge")
    if challenge_ref:
        challenge_path = _materialize(
            source_repo,
            control_commit,
            str(challenge_ref["path"]),
            str(challenge_ref["sha256"]),
            scratch / "historical-game-type-challenge.json",
        )

    target = add_existing_onboarding_worktree(
        str(request["target_branch"]),
        str(request["target_sha"]),
        str(request["school_key"]),
        source_repo=source_repo,
    )

    candidate_census = run_stage2_census_tool(
        target,
        str(request["school_key"]),
        authority["freeze_bytes"],
        diag / "candidate-census",
        tool_repo=candidate_runtime,
        historical_game_type_challenge_path=challenge_path,
    )
    expected_universe = str(request["decision_universe_sha256"])
    candidate_universe = candidate_census_decision_universe(candidate_census)

    if candidate_universe != expected_universe:
        result = candidate_census
        classification = "ADVANCED_TO_CHANGED_DECISION_UNIVERSE"
        decision_universe_compatibility = {
            "status": "CHANGED",
            "kind": "MECHANICAL_PLANNER_ELIGIBILITY_RECOMPUTE",
            "authority_decision_universe_sha256": expected_universe,
            "runtime_decision_universe_sha256": candidate_universe,
        }
    else:
        result = run_stage2_proposal_tool(
            target,
            str(request["school_key"]),
            authority["freeze_bytes"],
            map_path,
            expected_universe,
            diag,
            tool_repo=candidate_runtime,
            historical_game_type_challenge_path=challenge_path,
        )
        classification = classify_candidate_result(baseline_status, result)
        decision_universe_compatibility = result.get(
            "decision_universe_compatibility"
        )

    summary = {
        "schema_version": 1,
        "kind": "STAGE2_CANDIDATE_RUNTIME_REHEARSAL",
        "school_key": request["school_key"],
        "candidate_sha": candidate_sha,
        "base_protected_main_sha": base_sha,
        "control_commit": control_commit,
        "proposal_checkpoint_path": proposal_checkpoint_path,
        "proposal_checkpoint_sha256": manifest.get("checkpoint_manifest_sha256"),
        "request_id": request.get("request_id"),
        "target_branch": request.get("target_branch"),
        "target_sha": request.get("target_sha"),
        "recommendation_map_sha256": map_sha,
        "decision_universe_sha256": request.get("decision_universe_sha256"),
        "candidate_decision_universe_sha256": candidate_universe,
        "changed_paths": changed_paths,
        "baseline_error": baseline_status.get("last_error"),
        "candidate_stage2_status": result.get("stage2_status"),
        "candidate_error": (result.get("status") or {}).get("last_error"),
        "decision_universe_compatibility": decision_universe_compatibility,
        "tracked_mutation_proof": result.get("tracked_mutation_proof"),
        "classification": classification,
    }
    diag.mkdir(parents=True, exist_ok=True)
    (diag / "candidate-rehearsal-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if classification == "NO_PROGRESS_SAME_BLOCKER":
        raise Stop("CANDIDATE_REHEARSAL_NO_PROGRESS_SAME_BLOCKER")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replay a blocked Stage-2 proposal against candidate tooling."
    )
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--candidate-runtime", type=Path, required=True)
    parser.add_argument("--candidate-sha", required=True)
    parser.add_argument("--control-commit", required=True)
    parser.add_argument("--proposal-checkpoint-path", required=True)
    parser.add_argument(
        "--diag",
        type=Path,
        default=Path("/tmp/stage2-candidate-runtime-rehearsal"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        summary = run_candidate_rehearsal(
            source_repo=args.source_repo.resolve(),
            candidate_runtime=args.candidate_runtime.resolve(),
            candidate_sha=args.candidate_sha,
            control_commit=args.control_commit,
            proposal_checkpoint_path=args.proposal_checkpoint_path,
            diag=args.diag.resolve(),
        )
    except Stop as exc:
        print(f"FAIL: {exc}")
        return 1

    print(
        "STAGE2 CANDIDATE RUNTIME REHEARSAL: "
        f"{summary['classification']} "
        f"candidate_status={summary['candidate_stage2_status']}"
    )
    if summary.get("candidate_error"):
        print("candidate_error=" + str(summary["candidate_error"]))
    print("summary=" + str((args.diag / "candidate-rehearsal-summary.json").resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
