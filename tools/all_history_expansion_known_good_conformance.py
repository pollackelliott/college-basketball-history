#!/usr/bin/env python3
"""Replay durable successful All-History expansions with current generic tooling."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from remote_implementation_control import sha256_bytes
from remote_implementation_io import Stop, git_show_bytes
from remote_implementation_stage2_census import run_stage2_census_tool
from remote_implementation_stage2_proposal import (
    run_stage2_proposal_tool,
    verify_stage2_proposal_authority,
)

WITNESSES = (
    (
        "vcu",
        ".remote-implementation/checkpoints/vcu/vcu-expansion-stage2-proposal-0001/checkpoint-manifest.json",
        ".remote-implementation/checkpoints/vcu/vcu-expansion-release-production-proof-0001/checkpoint-manifest.json",
    ),
    (
        "arizona-state",
        ".remote-implementation/checkpoints/arizona-state/arizona-state-expansion-stage2-proposal-0002/checkpoint-manifest.json",
        ".remote-implementation/checkpoints/arizona-state/arizona-state-expansion-release-production-proof-0001/checkpoint-manifest.json",
    ),
    (
        "houston",
        ".remote-implementation/checkpoints/houston/houston-expansion-stage2-proposal-0003/checkpoint-manifest.json",
        ".remote-implementation/checkpoints/houston/houston-expansion-release-production-proof-0001/checkpoint-manifest.json",
    ),
    (
        "ucf",
        ".remote-implementation/checkpoints/ucf/ucf-expansion-stage2-proposal-0004/checkpoint-manifest.json",
        ".remote-implementation/checkpoints/ucf/ucf-expansion-release-production-proof-0001/checkpoint-manifest.json",
    ),
)

PREFLIGHT_KEYS = (
    "blocker_count",
    "warning_count",
    "decision_count",
    "decision_categories",
    "decision_universe_sha256",
    "existing_game_matches",
    "new_canonical_games",
    "discrepancies_to_add",
    "conditional_discrepancies",
    "confident_collision_groups",
    "confident_collision_source_rows",
    "identity_cardinality_constraints",
)

SITE_COUNT_KEYS = (
    "strict_home_gap_rows",
    "strict_ncaa_gap_rows",
    "unaccounted_public_gap_rows",
    "target_source_information_loss",
    "invalid_home_venue_exception_marker_rows",
    "target_canonical_games",
)


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if check and cp.returncode:
        raise Stop("KNOWN_GOOD_GIT_FAILED:" + " ".join(args) + "\n" + cp.stdout[-4000:])
    return cp


def json_at(repo: Path, commit: str, path: str) -> tuple[dict[str, Any], bytes]:
    raw = git_show_bytes(commit, path, cwd=repo)
    try:
        doc = json.loads(raw)
    except (TypeError, ValueError) as exc:
        raise Stop("KNOWN_GOOD_JSON_INVALID:" + path) from exc
    if not isinstance(doc, dict):
        raise Stop("KNOWN_GOOD_JSON_OBJECT_REQUIRED:" + path)
    return doc, raw


def subset(doc: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    return {key: doc.get(key) for key in keys}


def require_equal(label: str, expected: Any, actual: Any) -> None:
    if expected != actual:
        raise Stop(
            "KNOWN_GOOD_MISMATCH:"
            + label
            + ":expected="
            + json.dumps(expected, sort_keys=True)
            + ":actual="
            + json.dumps(actual, sort_keys=True)
        )


def materialize(
    repo: Path,
    commit: str,
    path: str,
    expected_sha: str,
    destination: Path,
) -> Path:
    raw = git_show_bytes(commit, path, cwd=repo)
    if sha256_bytes(raw) != expected_sha:
        raise Stop("KNOWN_GOOD_HASH_MISMATCH:" + path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(raw)
    return destination


def historical_worktree(runtime_repo: Path, target_sha: str, school: str) -> Path:
    present = git(
        runtime_repo,
        "rev-parse",
        "--verify",
        target_sha + "^{commit}",
        check=False,
    )
    if present.returncode:
        git(runtime_repo, "fetch", "--no-tags", "origin", target_sha)
    observed = git(
        runtime_repo, "rev-parse", "--verify", target_sha + "^{commit}"
    ).stdout.strip()
    require_equal(school + ":target-sha", target_sha, observed)
    worktree = Path(tempfile.mkdtemp(prefix="known-good-" + school + "-"))
    shutil.rmtree(worktree)
    local_branch = "data/" + school + "-onboarding"
    existing_branch = git(
        runtime_repo,
        "show-ref",
        "--verify",
        "--quiet",
        "refs/heads/" + local_branch,
        check=False,
    )
    if existing_branch.returncode == 0:
        git(runtime_repo, "branch", "-D", local_branch)
    git(runtime_repo, "worktree", "add", "-b", local_branch, str(worktree), target_sha)
    require_equal(school + ":worktree-head", target_sha, git(worktree, "rev-parse", "HEAD").stdout.strip())
    require_equal(school + ":worktree-branch", local_branch, git(worktree, "branch", "--show-current").stdout.strip())
    if git(worktree, "status", "--porcelain").stdout.strip():
        raise Stop("KNOWN_GOOD_WORKTREE_DIRTY:" + school)
    return worktree


def cleanup_worktree(runtime_repo: Path, worktree: Path | None) -> None:
    if worktree is None:
        return
    branch = git(worktree, "branch", "--show-current", check=False).stdout.strip()
    git(runtime_repo, "worktree", "remove", "--force", str(worktree), check=False)
    if branch:
        git(runtime_repo, "branch", "-D", branch, check=False)
    shutil.rmtree(worktree, ignore_errors=True)


def replay(
    control_repo: Path,
    runtime_repo: Path,
    control_commit: str,
    witness: tuple[str, str, str],
    diag: Path,
) -> dict[str, Any]:
    school, proposal_path, production_path = witness
    manifest, _ = json_at(control_repo, control_commit, proposal_path)
    require_equal(school + ":proposal-kind", "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_CHECKPOINT", manifest.get("kind"))
    require_equal(school + ":proposal-status", "OWNER_GATE_1_READY", manifest.get("stage2_status"))

    production, _ = json_at(control_repo, control_commit, production_path)
    require_equal(school + ":production-kind", "REMOTE_IMPLEMENTATION_EXACT_PRODUCTION_CHECKPOINT", production.get("kind"))
    require_equal(school + ":production-status", "PRODUCTION_PROOF_PASS", production.get("status"))
    require_equal(school + ":production-proof", True, production.get("production_proof"))

    checkpoint_dir = Path(proposal_path).parent
    request_path = (checkpoint_dir / "request.json").as_posix()
    request, request_raw = json_at(control_repo, control_commit, request_path)
    require_equal(school + ":request-id", manifest.get("request_id"), request.get("request_id"))
    request_sha = str(manifest.get("request_sha256") or "")
    if request_sha:
        require_equal(school + ":request-sha", request_sha, sha256_bytes(request_raw))
    require_equal(school + ":request-operation", "STAGE2_PROPOSAL_REHEARSAL", request.get("operation"))

    authority = verify_stage2_proposal_authority(
        request, control_commit, source_repo=control_repo
    )
    scratch = Path(tempfile.mkdtemp(prefix="known-good-map-" + school + "-"))
    worktree = None
    try:
        map_ref = str(manifest.get("recommendation_map_checkpoint_path") or "")
        map_sha = str(manifest.get("recommendation_map_sha256") or "")
        if not map_ref or len(map_sha) != 64:
            raise Stop("KNOWN_GOOD_MAP_REFERENCE_MISSING:" + school)
        map_path = materialize(
            control_repo,
            control_commit,
            map_ref,
            map_sha,
            scratch / "recommendation-map.json",
        )

        challenge_path = None
        challenge_ref = authority.get("historical_game_type_challenge")
        if challenge_ref:
            challenge_path = materialize(
                control_repo,
                control_commit,
                str(challenge_ref["path"]),
                str(challenge_ref["sha256"]),
                scratch / "historical-game-type-challenge.json",
            )

        target_sha = str(request.get("target_sha") or "")
        if len(target_sha) != 40:
            raise Stop("KNOWN_GOOD_TARGET_SHA_INVALID:" + school)
        worktree = historical_worktree(runtime_repo, target_sha, school)

        census = run_stage2_census_tool(
            worktree,
            school,
            authority["freeze_bytes"],
            diag / school / "census",
            tool_repo=runtime_repo,
            historical_game_type_challenge_path=challenge_path,
        )
        expected_universe = str(manifest.get("decision_universe_sha256") or "")
        require_equal(
            school + ":census-status",
            "CAPABILITY_CENSUS_READY",
            census.get("stage2_status"),
        )
        require_equal(
            school + ":census-universe",
            expected_universe,
            ((census.get("status") or {}).get("preflight") or {}).get("decision_universe_sha256"),
        )
        require_equal(
            school + ":census-mutation",
            "NONE",
            (census.get("tracked_mutation_proof") or {}).get("tracked_stage2_mutation"),
        )

        proposal = run_stage2_proposal_tool(
            worktree,
            school,
            authority["freeze_bytes"],
            map_path,
            expected_universe,
            diag / school / "proposal",
            tool_repo=runtime_repo,
            historical_game_type_challenge_path=challenge_path,
            venue_reconciliation_bytes=authority.get("venue_reconciliation_bytes"),
        )
        require_equal(school + ":gate1-status", "OWNER_GATE_1_READY", proposal.get("stage2_status"))
        require_equal(
            school + ":proposal-mutation",
            "NONE",
            (proposal.get("tracked_mutation_proof") or {}).get("tracked_stage2_mutation"),
        )
        require_equal(
            school + ":universe-compatibility",
            "EXACT",
            (proposal.get("decision_universe_compatibility") or {}).get("status"),
        )

        status = proposal.get("status") or {}
        require_equal(
            school + ":preflight",
            subset(manifest.get("preflight") or {}, PREFLIGHT_KEYS),
            subset(status.get("preflight") or {}, PREFLIGHT_KEYS),
        )
        require_equal(
            school + ":action-counts",
            manifest.get("action_counts") or {},
            (status.get("proposal_rehearsal") or {}).get("action_counts") or {},
        )
        require_equal(
            school + ":approved-plan-hash",
            manifest.get("approved_plan_hash_preview"),
            (status.get("proposal_rehearsal") or {}).get("approved_plan_hash_preview"),
        )

        expected_site = manifest.get("site_diagnostic") or {}
        actual_site = proposal.get("site_diagnostic") or {}
        require_equal(school + ":site-status", expected_site.get("status"), actual_site.get("status"))
        require_equal(
            school + ":site-counts",
            subset(expected_site.get("counts") or {}, SITE_COUNT_KEYS),
            subset(actual_site.get("counts") or {}, SITE_COUNT_KEYS),
        )

        return {
            "school_key": school,
            "status": "PASS",
            "historical_target_sha": target_sha,
            "production_merge_sha": production.get("merge_sha"),
            "decision_universe_sha256": expected_universe,
            "recommendation_map_sha256": map_sha,
            "action_counts": manifest.get("action_counts") or {},
            "approved_plan_hash_preview": manifest.get("approved_plan_hash_preview"),
            "site_status": actual_site.get("status"),
            "site_counts": subset(actual_site.get("counts") or {}, SITE_COUNT_KEYS),
            "tracked_stage2_mutation": "NONE",
        }
    finally:
        cleanup_worktree(runtime_repo, worktree)
        shutil.rmtree(scratch, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--control-repo", type=Path, required=True)
    parser.add_argument("--runtime-repo", type=Path, default=ROOT)
    parser.add_argument("--control-commit", default="HEAD")
    parser.add_argument("--diag", type=Path, default=Path("/tmp/all-history-expansion-known-good"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    control_repo = args.control_repo.resolve()
    runtime_repo = args.runtime_repo.resolve()
    control_commit = args.control_commit
    try:
        if control_commit == "HEAD":
            control_commit = git(control_repo, "rev-parse", "HEAD").stdout.strip()
        else:
            require_equal(
                "control-commit",
                control_commit,
                git(control_repo, "rev-parse", "--verify", control_commit + "^{commit}").stdout.strip(),
            )
        runtime_commit = git(runtime_repo, "rev-parse", "HEAD").stdout.strip()
    except Stop as exc:
        print("FAIL: " + str(exc))
        return 1

    results: list[dict[str, Any]] = []
    failures = 0
    for witness in WITNESSES:
        school = witness[0]
        try:
            results.append(
                replay(
                    control_repo,
                    runtime_repo,
                    control_commit,
                    witness,
                    args.diag.resolve(),
                )
            )
        except Stop as exc:
            failures += 1
            results.append(
                {
                    "school_key": school,
                    "status": "FAIL",
                    "error": str(exc),
                }
            )

    summary = {
        "schema_version": 1,
        "kind": "ALL_HISTORY_EXPANSION_KNOWN_GOOD_CONFORMANCE",
        "status": "PASS" if failures == 0 else "FAIL",
        "control_commit": control_commit,
        "runtime_commit": runtime_commit,
        "witness_count": len(results),
        "failure_count": failures,
        "witnesses": results,
    }

    payload = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
