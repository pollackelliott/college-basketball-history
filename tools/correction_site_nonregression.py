"""Fail-closed published-site nonregression proofs.

The ordinary site gate still emits its independent full PASS/FAIL result for
inherited debt. Exact bounded corrections and authenticated All-History
expansions may additionally prove that they introduced no new site-category/game
failure while leaving pre-existing published debt visible.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any, Iterable
from implementation_site_gate import implementation_site_report
FULL_POPULATION_LIMIT = 100000
SINGLE_MODE = "SINGLE_GAME_CORRECTION_NONREGRESSION"
MULTI_MODE = "MULTI_GAME_CORRECTION_NONREGRESSION"
EXPANSION_MODE = "ALL_HISTORY_EXPANSION_NONREGRESSION"
PACKAGE_ONLY_MODE = "PACKAGE_ONLY_CORRECTION_NONREGRESSION"

# These are the canonical populations that the permanent implementation site
# report turns into actual publication errors. Raw gap categories such as
# home_missing_venue, neutral_missing_venue, or unknown_site_type may grow in an
# All-History expansion when the same report independently proves those exact
# rows are research-accounted or owner-authorized exceptions.
EXPANSION_BLOCKING_CATEGORIES = frozenset({
    "strict_home_gap",
    "invalid_home_venue_exception_marker",
    "strict_ncaa_gap",
    "target_source_site_type_lost",
    "target_source_venue_lost",
    "target_source_location_lost",
    "reciprocal_site_type_unpropagated",
    "reciprocal_venue_unpropagated",
    "reciprocal_location_unpropagated",
    "unaccounted_public_gap",
})

def stable(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(report: dict[str, Any]) -> str:
    return hashlib.sha256(stable(report).encode("utf-8")).hexdigest()

def capture(repo, school_key: str) -> dict[str, Any]:
    return implementation_site_report(repo, school_key, example_limit=FULL_POPULATION_LIMIT)

def _target_games(value: str | Iterable[str]) -> list[str]:
    if isinstance(value, str): raw = [value]
    else: raw = list(value)
    games = [str(item).strip() for item in raw]
    if not games or not all(games) or len(set(games)) != len(games):
        from onboarding_plan import WorkflowError
        raise WorkflowError("correction site proof requires unique target canonical games")
    return sorted(games)

def prove(before: dict[str, Any], after: dict[str, Any], target_games: str | Iterable[str]) -> dict[str, Any]:
    from onboarding_plan import WorkflowError
    games = _target_games(target_games)
    if (before.get('school_key') != after.get('school_key')
        or before.get('history_start_season') != after.get('history_start_season')
        or before.get('source_validation_scope') != after.get('source_validation_scope')
        or before.get('source_validation_scope', {}).get('mode') != 'CORRECTION_DELTA'
        or before.get('source_validation_scope', {}).get('scoped_source_games') != len(games)):
        raise WorkflowError("correction site proof requires identical trusted one-game scope" if len(games)==1 else "correction site proof requires identical trusted bounded correction scope")
    bcounts, acounts = before.get('counts', {}), after.get('counts', {})
    if bcounts.get('target_canonical_games') != acounts.get('target_canonical_games'):
        raise WorkflowError("correction site proof changed target canonical universe")
    if before.get('source_site_counts') != after.get('source_site_counts'):
        raise WorkflowError("correction site proof changed source-side Research debt")
    bex, aex = before.get('examples', {}), after.get('examples', {})
    inherited, eliminated = 0, 0
    for category in sorted(set(bex) | set(aex)):
        b, a = bex.get(category, []), aex.get(category, [])
        if (not isinstance(b,list) or not isinstance(a,list) or len(set(b))!=len(b) or len(set(a))!=len(a) or len(b)!=bcounts.get(category,0) or len(a)!=acounts.get(category,0)):
            raise WorkflowError("correction site proof lacks complete failure population: " + category)
        new = sorted(set(a)-set(b))
        if new:
            raise WorkflowError("correction introduced site failure " + category + ": " + ", ".join(new[:5]))
        inherited += len(a)
        eliminated += len(set(b)-set(a))
    proof = {
        'mode': SINGLE_MODE if len(games)==1 else MULTI_MODE,
        'school_key': before['school_key'],
        'baseline_report_sha256': digest(before),
        'corrected_report_sha256': digest(after),
        'baseline_site_status': before['status'],
        'corrected_site_status': after['status'],
        'inherited_site_findings': inherited,
        'removed_site_findings': eliminated,
        'before_counts': bcounts, 'after_counts': acounts,
        'site_debt_remains': after['status'] != 'PASS',
    }
    if len(games)==1: proof['target_game_id']=games[0]
    else: proof['target_game_ids']=games
    return proof

def verify_current(report: dict[str, Any], proof: dict[str, Any], school: str) -> None:
    from onboarding_plan import WorkflowError
    mode=proof.get('mode')
    target_ok = (bool(proof.get('target_game_id')) if mode==SINGLE_MODE else (isinstance(proof.get('target_game_ids'),list) and len(proof['target_game_ids'])>=2 and proof['target_game_ids']==sorted(set(proof['target_game_ids'])) and all(proof['target_game_ids'])) if mode==MULTI_MODE else False)
    if (not target_ok or proof.get('school_key') != school or report.get('school_key') != school or digest(report) != proof.get('corrected_report_sha256') or report.get('status') != proof.get('corrected_site_status')):
        raise WorkflowError("correction site proof does not match independent site gate")



def prove_package_only(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """Prove a package-only correction changed no game/site-bearing state."""

    from onboarding_plan import WorkflowError
    before_scope = before.get("source_validation_scope", {})
    after_scope = after.get("source_validation_scope", {})
    if (
        before.get("school_key") != after.get("school_key")
        or before.get("history_start_season") != after.get("history_start_season")
        or before_scope != after_scope
        or before_scope.get("mode") != "PACKAGE_ONLY_CORRECTION"
        or int(before_scope.get("scoped_source_games", -1)) != 0
    ):
        raise WorkflowError(
            "package-only site proof requires identical zero-source correction scope"
        )
    if before != after:
        raise WorkflowError(
            "package-only correction changed the independent site-completeness report"
        )
    report_hash = digest(after)
    return {
        "mode": PACKAGE_ONLY_MODE,
        "school_key": before["school_key"],
        "baseline_report_sha256": report_hash,
        "corrected_report_sha256": report_hash,
        "baseline_site_status": before["status"],
        "corrected_site_status": after["status"],
        "site_debt_remains": after["status"] != "PASS",
    }


def verify_package_only_current(
    report: dict[str, Any], proof: dict[str, Any], school: str
) -> None:
    """Require the independent site gate to equal the package-only proved state."""

    from onboarding_plan import WorkflowError
    if (
        proof.get("mode") != PACKAGE_ONLY_MODE
        or proof.get("school_key") != school
        or report.get("school_key") != school
        or report.get("source_validation_scope", {}).get("mode")
        != "PACKAGE_ONLY_CORRECTION"
        or digest(report) != proof.get("corrected_report_sha256")
        or report.get("status") != proof.get("corrected_site_status")
    ):
        raise WorkflowError(
            "package-only correction site proof does not match independent site gate"
        )


def prove_expansion(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """Prove an All-History expansion introduced no new canonical site debt."""
    from onboarding_plan import WorkflowError
    if (
        before.get("school_key") != after.get("school_key")
        or before.get("history_start_season") != after.get("history_start_season")
        or before.get("source_validation_scope") != after.get("source_validation_scope")
        or before.get("source_validation_scope", {}).get("mode") != "FULL_SOURCE_PACKAGE"
    ):
        raise WorkflowError(
            "expansion site proof requires identical trusted full-source scope"
        )
    if before.get("source_site_counts") != after.get("source_site_counts"):
        raise WorkflowError("expansion site proof changed source-side Research debt")

    bcounts, acounts = before.get("counts", {}), after.get("counts", {})
    before_games = int(bcounts.get("target_canonical_games", 0) or 0)
    after_games = int(acounts.get("target_canonical_games", 0) or 0)
    if after_games < before_games:
        raise WorkflowError("expansion site proof shrank target canonical universe")

    bex, aex = before.get("examples", {}), after.get("examples", {})
    inherited, eliminated = 0, 0
    for category in sorted(EXPANSION_BLOCKING_CATEGORIES):
        b, a = bex.get(category, []), aex.get(category, [])
        if (
            not isinstance(b, list)
            or not isinstance(a, list)
            or len(set(b)) != len(b)
            or len(set(a)) != len(a)
            or len(b) != int(bcounts.get(category, 0) or 0)
            or len(a) != int(acounts.get(category, 0) or 0)
        ):
            raise WorkflowError(
                "expansion site proof lacks complete failure population: " + category
            )
        new = sorted(set(a) - set(b))
        if new:
            raise WorkflowError(
                "expansion introduced site failure "
                + category
                + ": "
                + ", ".join(new[:5])
            )
        inherited += len(a)
        eliminated += len(set(b) - set(a))

    before_errors = before.get("errors", [])
    after_errors = after.get("errors", [])
    if not isinstance(before_errors, list) or not isinstance(after_errors, list):
        raise WorkflowError("expansion site proof requires structured site errors")
    new_errors = [error for error in after_errors if error not in before_errors]
    if new_errors:
        raise WorkflowError(
            "expansion introduced site failure report-error: "
            + str(new_errors[0])
        )

    return {
        "mode": EXPANSION_MODE,
        "school_key": before["school_key"],
        "baseline_report_sha256": digest(before),
        "expanded_report_sha256": digest(after),
        "baseline_site_status": before["status"],
        "expanded_site_status": after["status"],
        "baseline_target_canonical_games": before_games,
        "expanded_target_canonical_games": after_games,
        "added_target_canonical_games": after_games - before_games,
        "inherited_site_findings": inherited,
        "removed_site_findings": eliminated,
        "before_counts": bcounts,
        "after_counts": acounts,
        "site_debt_remains": after["status"] != "PASS",
    }


def verify_expansion_current(
    report: dict[str, Any], proof: dict[str, Any], school: str
) -> None:
    """Require the independent full site gate to equal the proved expansion state."""
    from onboarding_plan import WorkflowError
    if (
        proof.get("mode") != EXPANSION_MODE
        or proof.get("school_key") != school
        or report.get("school_key") != school
        or digest(report) != proof.get("expanded_report_sha256")
        or report.get("status") != proof.get("expanded_site_status")
    ):
        raise WorkflowError(
            "expansion site proof does not match independent site gate"
        )
