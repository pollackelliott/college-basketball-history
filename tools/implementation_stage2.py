#!/usr/bin/env python3
"""Repository-owned coordinator for Implementation Stage 2.

This command deliberately composes existing permanent onboarding tools rather than
reimplementing their invariants in shell. Normal use:

    python tools/implementation_stage2.py <school>
    python tools/implementation_stage2.py <school> --map /path/to/recommendations.json
    python tools/implementation_stage2.py <school> --status

The first form verifies INTEGRATION_FROZEN and regenerates authoritative preflight
artifacts. The second additionally validates the compact recommendation map with
the authoritative review parser and runs the full disposable proposal rehearsal.
Every run writes an ignored machine-readable recovery artifact at
.onboarding/<school>/implementation-stage2-status.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import onboard_school
from integration_freeze_guard import semantic_drift_report
from onboarding_hardening import (
    rehearse_decision_map,
    validate_decision_map,
)
from onboarding_plan import (
    WorkflowError,
    build_plan,
    write_preflight_artifacts,
)


STATUS_SCHEMA_VERSION = 1
STATUS_FILENAME = "implementation-stage2-status.json"
CAPABILITY_CENSUS_FILENAME = "implementation-stage2-capability-census.json"
SITE_DIAGNOSTIC_FILENAME = "last-rehearsal-site-gate.json"

SITE_REVIEW_FIELDS = {
    "site_type",
    "venue",
    "venue_key",
    "venue_id",
    "location",
    "site_city",
    "site_state",
    "site_metadata",
}


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _decision_universe_sha256(plan: dict[str, Any]) -> str:
    decisions = sorted(
        plan.get("decisions", []),
        key=lambda row: str(row.get("decision_id", "")),
    )
    payload = json.dumps(
        decisions,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return _sha256_bytes(payload)


def _relative(repo: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _integration_manifest(repo: Path, school_key: str) -> dict[str, Any]:
    path = repo / ".onboarding" / school_key / "integration-freeze.json"
    if not path.is_file():
        raise WorkflowError(
            "INTEGRATION_FROZEN manifest is missing; run the permanent Stage 1 "
            f"staging workflow first: {path}"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _git_state(repo: Path) -> dict[str, str]:
    return {
        "branch": onboard_school.git(repo, "branch", "--show-current").strip(),
        "head_sha": onboard_school.git(repo, "rev-parse", "HEAD").strip(),
    }


def _site_diagnostic(repo: Path, school_key: str) -> dict[str, Any] | None:
    path = repo / ".onboarding" / school_key / SITE_DIAGNOSTIC_FILENAME
    if not path.is_file():
        return None
    report = json.loads(path.read_text(encoding="utf-8"))
    return {
        "path": _relative(repo, path),
        "status": report.get("status"),
        "counts": report.get("counts", {}),
        "examples": report.get("examples", {}),
        "errors": report.get("errors", []),
    }


def _write_status(repo: Path, school_key: str, status: dict[str, Any]) -> Path:
    output = repo / ".onboarding" / school_key / STATUS_FILENAME
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output


def _capability_census(
    plan: dict[str, Any],
    *,
    site_diagnostic: dict[str, Any] | None = None,
    proposal_rehearsal_passed: bool = False,
) -> dict[str, Any]:
    decisions = list(plan.get("decisions", []))
    decision_categories = Counter(
        str(row.get("category", "")) for row in decisions
    )
    decision_fields = Counter(
        str(row.get("field_name", "")) for row in decisions
        if str(row.get("field_name", ""))
    )
    site_review_ids = sorted(
        str(row.get("decision_id", ""))
        for row in decisions
        if row.get("category") == "canonical_site_patch"
        or str(row.get("field_name", "")) in SITE_REVIEW_FIELDS
    )

    topology_groups: list[dict[str, Any]] = []
    blockers = list(plan.get("blockers", []))
    warnings = list(plan.get("warnings", []))
    if blockers:
        topology_groups.append(
            {
                "topology": "preflight_blockers",
                "count": len(blockers),
                "classification": "UNCLASSIFIED",
            }
        )
    if warnings:
        topology_groups.append(
            {
                "topology": "preflight_warnings",
                "count": len(warnings),
                "classification": "UNCLASSIFIED",
            }
        )
    if site_review_ids:
        topology_groups.append(
            {
                "topology": "site_or_han_review_population",
                "count": len(site_review_ids),
                "classification": "HISTORICAL_OR_REPRESENTATION_REVIEW",
            }
        )

    site_counts: dict[str, Any] = {}
    site_examples: dict[str, Any] = {}
    if site_diagnostic:
        site_counts = dict(site_diagnostic.get("counts", {}))
        site_examples = dict(site_diagnostic.get("examples", {}))
        for key in (
            "strict_home_gap_rows",
            "strict_ncaa_gap_rows",
            "target_source_information_loss",
            "reciprocal_unpropagated",
            "unaccounted_public_gap_rows",
            "invalid_home_venue_exception_marker_rows",
        ):
            count = int(site_counts.get(key, 0) or 0)
            if count:
                topology_groups.append(
                    {
                        "topology": key,
                        "count": count,
                        "classification": "UNCLASSIFIED_CAPABILITY_OR_HISTORY",
                        "examples": list(site_examples.get(key, [])),
                    }
                )

    if proposal_rehearsal_passed:
        census_status = "PASS"
    elif site_diagnostic and site_diagnostic.get("status") == "FAIL":
        census_status = "REPAIR_SCOPE_REQUIRED"
    elif blockers:
        census_status = "PREFLIGHT_BLOCKED"
    else:
        census_status = "CENSUS_CAPTURED"

    return {
        "schema_version": 1,
        "status": census_status,
        "preflight": {
            "blocker_count": len(blockers),
            "warning_count": len(warnings),
            "decision_count": len(decisions),
            "decision_categories": dict(sorted(decision_categories.items())),
            "decision_fields": dict(sorted(decision_fields.items())),
            "canonical_site_patch_reviews": int(
                plan.get("summary", {}).get("canonical_site_patch_reviews", 0) or 0
            ),
            "site_or_han_review_decision_ids": site_review_ids,
        },
        "site_diagnostic": {
            "status": site_diagnostic.get("status") if site_diagnostic else "",
            "counts": site_counts,
            "examples": site_examples,
        },
        "topology_groups": topology_groups,
        "repair_rule": (
            "If any topology is a generic permanent-tool defect, classify the complete "
            "currently detected defect population and define one consolidated repair "
            "scope before merging the first tooling repair. Rerun/regeneration is "
            "verification, not the discovery mechanism."
        ),
    }


def _write_capability_census(
    repo: Path,
    school_key: str,
    census: dict[str, Any],
) -> Path:
    output = repo / ".onboarding" / school_key / CAPABILITY_CENSUS_FILENAME
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(census, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output


def _base_status(repo: Path, school_key: str) -> dict[str, Any]:
    git_state = _git_state(repo)
    manifest = _integration_manifest(repo, school_key)
    semantic_guard = manifest.get("source_game_semantic_guard", {})
    return {
        "schema_version": STATUS_SCHEMA_VERSION,
        "school_key": school_key,
        "stage": "IMPLEMENTATION_STAGE_2",
        "status": "RUNNING",
        **git_state,
        "research_base_sha": manifest.get("research_base_sha", ""),
        "integration_base_sha": manifest.get("integration_base_sha", ""),
        "origin_main_sha_at_integration_freeze": manifest.get("origin_main_sha", ""),
        "integration_semantic_sha256": semantic_guard.get("snapshot_sha256", ""),
    }


def _plan_summary(plan: dict[str, Any]) -> dict[str, Any]:
    categories = Counter(
        str(row.get("category", "")) for row in plan.get("decisions", [])
    )
    summary = plan.get("summary", {})
    return {
        "blocker_count": len(plan.get("blockers", [])),
        "warning_count": len(plan.get("warnings", [])),
        "decision_count": len(plan.get("decisions", [])),
        "decision_categories": dict(sorted(categories.items())),
        "decision_universe_sha256": _decision_universe_sha256(plan),
        "existing_game_matches": summary.get("existing_game_matches", 0),
        "new_canonical_games": summary.get("new_canonical_games", 0),
        "discrepancies_to_add": summary.get("discrepancies_to_add", 0),
        "conditional_discrepancies": summary.get("conditional_discrepancies", 0),
    }


def _print_status(status: dict[str, Any], status_path: Path) -> None:
    print("College Basketball History — Implementation Stage 2")
    print(f"School:          {status.get('school_key', '')}")
    print(f"Status:          {status.get('status', '')}")
    print(f"Branch:          {status.get('branch', '')}")
    print(f"HEAD:            {status.get('head_sha', '')}")
    plan = status.get("preflight", {})
    if plan:
        print(
            "Preflight:        "
            f"{plan.get('blocker_count', 0)} blocker(s), "
            f"{plan.get('warning_count', 0)} warning(s), "
            f"{plan.get('decision_count', 0)} decision(s)"
        )
        print(
            "Decision SHA:     "
            + str(plan.get("decision_universe_sha256", ""))
        )
    recommendation = status.get("recommendation_map")
    if recommendation:
        print(
            "Recommendation:   "
            f"{recommendation.get('decision_count', 0)} validated decision(s)"
        )
    rehearsal = status.get("proposal_rehearsal")
    if rehearsal:
        print(
            "Proposal proof:   "
            + str(rehearsal.get("approved_plan_hash_preview", ""))
        )
    census = status.get("capability_census")
    if census:
        print(
            "Capability census:"
            f" {census.get('status', '')} at {census.get('path', '')}"
        )
    site = status.get("site_diagnostic")
    if site:
        print(
            "Site diagnostic:  "
            f"{site.get('status', '')} at {site.get('path', '')}"
        )
    if status.get("last_error"):
        print("Last error:       " + str(status["last_error"]).splitlines()[0])
    print("Status artifact:  " + _relative(Path.cwd(), status_path))
    print("Next:             " + status.get("next_action", ""))


def run_stage2(
    repo: Path,
    school_key: str,
    *,
    map_path: Path | None = None,
) -> tuple[int, dict[str, Any], Path]:
    status: dict[str, Any] = {
        "schema_version": STATUS_SCHEMA_VERSION,
        "school_key": school_key,
        "stage": "IMPLEMENTATION_STAGE_2",
        "status": "RUNNING",
    }
    status_path = repo / ".onboarding" / school_key / STATUS_FILENAME
    plan: dict[str, Any] | None = None

    try:
        status.update(_base_status(repo, school_key))
        onboard_school.ensure_package_checkpoint(repo)
        drift = semantic_drift_report(repo, school_key)
        if drift.get("status") != "PASS":
            raise WorkflowError(
                "INTEGRATION_FROZEN semantic drift detected; restore frozen historical "
                "meaning before Stage 2 continues."
            )
        status["semantic_drift"] = {
            "status": drift.get("status"),
            "change_count": len(drift.get("changes", [])),
        }

        output_dir = repo / ".onboarding" / school_key
        plan = build_plan(repo, school_key)
        paths = write_preflight_artifacts(plan, output_dir)
        status["preflight"] = _plan_summary(plan)
        status["preflight"]["plan_path"] = _relative(repo, paths["plan"])
        status["preflight"]["review_path"] = _relative(repo, paths["review"])

        census = _capability_census(plan)
        census_path = _write_capability_census(repo, school_key, census)
        status["capability_census"] = {
            "path": _relative(repo, census_path),
            "status": census["status"],
            "topology_group_count": len(census["topology_groups"]),
        }

        if plan.get("blockers"):
            status["status"] = "BLOCKED"
            status["blockers"] = plan["blockers"]
            status["next_action"] = (
                "Classify the complete durable capability census before the first "
                "generic tooling repair. Resolve the authoritative preflight blockers "
                "as one coherent repair scope where they share a topology, then rerun "
                "this same Stage-2 command."
            )
            status_path = _write_status(repo, school_key, status)
            return 1, status, status_path

        if map_path is None:
            status["status"] = "CAPABILITY_CENSUS_READY"
            status["next_action"] = (
                "Review the durable capability census, complete the bounded "
                "deterministic/adversarial review and supported historical "
                "recommendations, then write one compact recommendation map and rerun "
                "this command with --map <path>. Do not merge the first generic "
                "tooling repair until the complete currently detected repair scope is "
                "classified."
            )
            status_path = _write_status(repo, school_key, status)
            return 0, status, status_path

        map_path = map_path.resolve()
        validation = validate_decision_map(
            repo,
            school_key,
            plan_path=paths["plan"],
            review_path=paths["review"],
            map_path=map_path,
        )
        status["recommendation_map"] = {
            "path": _relative(repo, map_path),
            "sha256": _sha256_file(map_path),
            **validation,
        }

        rehearsal = rehearse_decision_map(
            repo,
            school_key,
            plan_path=paths["plan"],
            review_path=paths["review"],
            map_path=map_path,
        )
        status["proposal_rehearsal"] = {
            "approved_plan_hash_preview": rehearsal["approved_plan_hash_preview"],
            "changed_path_count": len(rehearsal["changed_paths"]),
            "action_counts": rehearsal.get("action_counts", {}),
        }
        status["site_diagnostic"] = _site_diagnostic(repo, school_key)
        census = _capability_census(
            plan,
            site_diagnostic=status["site_diagnostic"],
            proposal_rehearsal_passed=True,
        )
        census_path = _write_capability_census(repo, school_key, census)
        status["capability_census"] = {
            "path": _relative(repo, census_path),
            "status": census["status"],
            "topology_group_count": len(census["topology_groups"]),
        }
        status["status"] = "OWNER_GATE_1_READY"
        status["next_action"] = (
            "Present the single consolidated Owner Gate 1 reconciliation packet. "
            "Do not fill, seal, or apply the real owner review until explicit approval."
        )
        status_path = _write_status(repo, school_key, status)
        return 0, status, status_path

    except (WorkflowError, FileNotFoundError, KeyError, ValueError, json.JSONDecodeError) as exc:
        status["status"] = "BLOCKED"
        status["last_error"] = str(exc)
        status["site_diagnostic"] = _site_diagnostic(repo, school_key)
        if plan is not None:
            census = _capability_census(
                plan,
                site_diagnostic=status["site_diagnostic"],
                proposal_rehearsal_passed=False,
            )
            census_path = _write_capability_census(repo, school_key, census)
            status["capability_census"] = {
                "path": _relative(repo, census_path),
                "status": census["status"],
                "topology_group_count": len(census["topology_groups"]),
            }
        if status["site_diagnostic"]:
            status["next_action"] = (
                "Inspect the preserved site diagnostic and durable capability census. "
                "Classify the complete detected failure population before changing "
                "history or tooling; if generic permanent tooling is defective, define "
                "one consolidated repair scope before merging the first repair. Do not "
                "invent a replacement rehearsal wrapper."
            )
        else:
            status["next_action"] = (
                "Diagnose this repository/tool failure from durable state and the "
                "authoritative permanent-tool output; do not replace the phase with "
                "assistant-authored orchestration."
            )
        status_path = _write_status(repo, school_key, status)
        return 1, status, status_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the repository-owned Implementation Stage 2 coordinator."
    )
    parser.add_argument("school_key")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument(
        "--map",
        dest="map_path",
        type=Path,
        default=None,
        help="Compact Gate 1 recommendation map to validate and rehearse.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print the most recent durable Stage-2 recovery status without running work.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    status_path = repo / ".onboarding" / args.school_key / STATUS_FILENAME

    if args.status:
        if not status_path.is_file():
            print(f"FAIL: no Stage-2 status artifact exists at {status_path}")
            return 1
        status = json.loads(status_path.read_text(encoding="utf-8"))
        _print_status(status, status_path)
        return 0

    code, status, status_path = run_stage2(
        repo,
        args.school_key,
        map_path=args.map_path,
    )
    _print_status(status, status_path)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
