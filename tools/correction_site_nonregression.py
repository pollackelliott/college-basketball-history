"""Fail-closed one-game published-correction site nonregression proof.

The ordinary site gate still emits its independent full FAIL for inherited
debt. Only an exact frozen single-game correction can instead prove that
no site-category/game pair regressed.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any

from implementation_site_gate import implementation_site_report

FULL_POPULATION_LIMIT = 100000


def stable(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(report: dict[str, Any]) -> str:
    return hashlib.sha256(stable(report).encode("utf-8")).hexdigest()


def capture(repo, school_key: str) -> dict[str, Any]:
    return implementation_site_report(repo, school_key, example_limit=FULL_POPULATION_LIMIT)


def prove(before: dict[str, Any], after: dict[str, Any], target_game: str) -> dict[str, Any]:
    from onboarding_plan import WorkflowError

    if (
        not target_game
        or before.get("school_key") != after.get("school_key")
        or before.get("history_start_season") != after.get("history_start_season")
        or before.get("source_validation_scope") != after.get("source_validation_scope")
        or before.get("source_validation_scope", {}).get("mode") != "CORRECTION_DELTA"
        or before.get("source_validation_scope", {}).get("scoped_source_games") != 1
    ):
        raise WorkflowError("correction site proof requires identical trusted one-game scope")
    bcounts, acounts = before.get("counts", {}), after.get("counts", {})
    if bcounts.get("target_canonical_games") != acounts.get("target_canonical_games"):
        raise WorkflowError("correction site proof changed target canonical universe")
    if before.get("source_site_counts") != after.get("source_site_counts"):
        raise WorkflowError("correction site proof changed source-side Research debt")
    bex, aex = before.get("examples", {}), after.get("examples", {})
    inherited, eliminated = 0, 0
    for category in sorted(set(bex) | set(aex)):
        b, a = bex.get(category, []), aex.get(category, [])
        if (
            not isinstance(b, list) or not isinstance(a, list)
            or len(set(b)) != len(b) or len(set(a)) != len(a)
            or len(b) != bcounts.get(category, 0)
            or len(a) != acounts.get(category, 0)
        ):
            raise WorkflowError(
                "correction site proof lacks complete failure population: " + category
            )
        new = sorted(set(a) - set(b))
        if new:
            raise WorkflowError(
                "correction introduced site failure " + category + ": "
                + ", ".join(new[:5])
            )
        inherited += len(a)
        eliminated += len(set(b) - set(a))
    return {
        "mode": "SINGLE_GAME_CORRECTION_NONREGRESSION",
        "school_key": before["school_key"],
        "target_game_id": target_game,
        "baseline_report_sha256": digest(before),
        "corrected_report_sha256": digest(after),
        "baseline_site_status": before["status"],
        "corrected_site_status": after["status"],
        "inherited_site_findings": inherited,
        "removed_site_findings": eliminated,
        "before_counts": bcounts,
        "after_counts": acounts,
        "site_debt_remains": after["status"] != "PASS",
    }


def verify_current(report: dict[str, Any], proof: dict[str, Any], school: str) -> None:
    from onboarding_plan import WorkflowError

    if (
        proof.get("mode") != "SINGLE_GAME_CORRECTION_NONREGRESSION"
        or proof.get("school_key") != school
        or report.get("school_key") != school
        or not proof.get("target_game_id")
        or digest(report) != proof.get("corrected_report_sha256")
        or report.get("status") != proof.get("corrected_site_status")
    ):
        raise WorkflowError("correction site proof does not match independent site gate")
