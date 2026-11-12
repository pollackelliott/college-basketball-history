#!/usr/bin/env python3
"""Hash-bound inherited publication proof for supplemental Stage 4 acceptance.

The ordinary whole-school research validator is intentionally unchanged.
This module authenticates the *one* missing-final-season exception using the
exact inherited Git baseline and the existing publication-history authority.
It neither edits school files nor certifies an expansion Research Freeze.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from all_history_expansion_freeze import (
    ExpansionFreezeError,
    _csv_bytes,
    _git_show,
    authenticate_baseline,
    canonical_row_sha256,
    population_sha256,
)
from program_history import (
    normalize_scope_season,
    parse_history_scope_intervals,
    publication_history_games,
    season_is_published_history,
    valid_season_label,
)

WORKFLOW = "ALL_HISTORY_EXPANSION"


class ExpansionStage4CoverageError(ValueError):
    """Fail-closed, immutable-baseline expansion Stage 4 acceptance defect."""


def _scope_reference_includes(
    season: str,
    scope_expression: str,
    history_start: str,
) -> bool:
    if scope_expression == "INCEPTION+":
        return valid_season_label(history_start) and season >= history_start
    intervals = parse_history_scope_intervals(scope_expression)
    return bool(intervals) and any(
        season >= start and (end is None or season <= end)
        for start, end in intervals
    )


def prove_expansion_stage4_coverage(
    *,
    repo: Path,
    school_key: str,
    research_base_sha: str,
    required_completed_season_cutoff: str,
    supplemental_rows: list[dict[str, str]],
) -> dict[str, Any]:
    """Prove that the omitted completed season is already published, not missing.

    A successful proof NEVER excuses other Research validation errors. The exact
    inherited Git commit must exist in the supplied checkout.
    """
    required = str(required_completed_season_cutoff or "").strip()
    if not valid_season_label(required):
        raise ExpansionStage4CoverageError(
            "expansion Stage 4 requires valid completed-season cutoff"
        )
    try:
        baseline = authenticate_baseline(
            Path(repo).resolve(), school_key, research_base_sha
        )
        program = baseline["program"]
        scope_expression = baseline["scope_row"].get("top_level_scope", "").strip()
        if not scope_expression:
            raise ExpansionStage4CoverageError("missing baseline scope expression")
        if not supplemental_rows:
            raise ExpansionStage4CoverageError(
                "expansion Stage 4 must not claim an empty supplemental game universe"
            )
        if not season_is_published_history(required, program):
            raise ExpansionStage4CoverageError(
                "required completed season is not published under inherited program scope"
            )
        if not _scope_reference_includes(
            required, scope_expression, program.get("history_start_season", "").strip()
        ):
            raise ExpansionStage4CoverageError(
                "required completed season is not in inherited scope reference"
            )

        inherited = {}
        for row in baseline["source_rows"]:
            sid = row.get("source_game_id", "").strip()
            if not sid or sid in inherited:
                raise ExpansionStage4CoverageError(
                    "inherited source-game IDs are blank or duplicated"
                )
            inherited[sid] = row

        inherited_cutoff_rows = [
            row for row in baseline["source_rows"]
            if row.get("season_label", "").strip() == required
            and row.get("source_program_key", "").strip() == school_key
        ]
        if not inherited_cutoff_rows:
            raise ExpansionStage4CoverageError(
                "inherited source package has no required completed-season games"
            )

        fields, canonical_rows = _csv_bytes(
            _git_show(
                Path(repo).resolve(), baseline["research_base_sha"],
                "data/canonical/games.csv",
            ),
            "authenticated baseline canonical games.csv",
        )
        for column in ("canonical_game_id", "season_label", "team_a_key", "team_b_key"):
            if column not in fields:
                raise ExpansionStage4CoverageError(
                    f"baseline canonical games missing {column}"
                )
        published = publication_history_games(canonical_rows, school_key, program)
        published_cutoff = [
            row for row in published if row.get("season_label", "").strip() == required
        ]
        if not published_cutoff:
            raise ExpansionStage4CoverageError(
                "baseline publication-authorized canonical population has no "
                "required completed-season games"
            )

        seen = set()
        all_seasons = set()
        ids = []
        for row in supplemental_rows:
            sid = row.get("source_game_id", "").strip()
            season = row.get("season_label", "").strip()
            if not sid or sid in seen:
                raise ExpansionStage4CoverageError(
                    "supplemental source IDs are blank or duplicated"
                )
            seen.add(sid)
            ids.append(sid)
            if row.get("source_program_key", "").strip() != school_key:
                raise ExpansionStage4CoverageError(
                    f"supplemental row {sid} belongs to another school"
                )
            if not valid_season_label(season):
                raise ExpansionStage4CoverageError(
                    f"supplemental row {sid} has invalid season"
                )
            if season > required:
                raise ExpansionStage4CoverageError(
                    f"supplemental row {sid} lies after completed-season cutoff"
                )
            if season_is_published_history(season, program) or _scope_reference_includes(
                season, scope_expression, program.get("history_start_season", "").strip()
            ):
                raise ExpansionStage4CoverageError(
                    f"supplemental row {sid} belongs to inherited published history"
                )
            inherited_row = inherited.get(sid)
            if inherited_row is not None and (
                canonical_row_sha256(inherited_row) != canonical_row_sha256(row)
            ):
                raise ExpansionStage4CoverageError(
                    f"supplemental row {sid} collides with a non-identical inherited source"
                )
            all_seasons.add(season)

        # Verify baseline program metadata and the owner scope reference classify
        # every season across the supplemental -> completed-season span identically.
        earliest = min(all_seasons)
        for year in range(int(earliest[:4]), int(required[:4]) + 1):
            season = f"{year:04d}-{year+1:04d}"
            if season_is_published_history(season, program) != _scope_reference_includes(
                season, scope_expression, program.get("history_start_season", "").strip()
            ):
                raise ExpansionStage4CoverageError(
                    f"inherited scope row and program metadata disagree for {season}"
                )

        return {
            "status": "PASS",
            "workflow_kind": WORKFLOW,
            "school_key": school_key,
            "research_base_sha": baseline["research_base_sha"],
            "baseline_program_row_sha256": baseline["program_row_sha256"],
            "baseline_scope_row_sha256": baseline["scope_row_sha256"],
            "baseline_source_game_id_population_sha256": baseline[
                "source_id_population_sha256"
            ],
            "baseline_published_canonical_id_population_sha256": baseline[
                "published_canonical_id_population_sha256"
            ],
            "baseline_scope_expression": scope_expression,
            "required_completed_season_cutoff": required,
            "inherited_required_season_source_rows": len(inherited_cutoff_rows),
            "inherited_required_season_published_canonical_rows": len(published_cutoff),
            "supplemental_game_count": len(ids),
            "supplemental_source_id_population_sha256": population_sha256(ids),
            "supplemental_first_season": min(all_seasons),
            "supplemental_last_season": max(all_seasons),
            "exception_scope": "INHERITED_PUBLISHED_COMPLETED_SEASON_ONLY",
            "research_accepted_inherited_rows_reproven": False,
            "publication_mutation": False,
        }
    except (ExpansionFreezeError, ValueError) as exc:
        if isinstance(exc, ExpansionStage4CoverageError):
            raise
        raise ExpansionStage4CoverageError(str(exc)) from exc


def reconcile_stage4_research_report(
    report: dict[str, Any],
    proof: Mapping[str, Any],
) -> dict[str, Any]:
    """Drop *only* the proved missing-target-completed-season complaint."""
    if proof.get("status") != "PASS" or proof.get("workflow_kind") != WORKFLOW:
        raise ExpansionStage4CoverageError("invalid expansion coverage proof")
    required = proof["required_completed_season_cutoff"]
    expected_error = (
        f"research package declares required completed-season cutoff {required} "
        "but contains zero competitive target-school rows for that season"
    )
    coverage = report.get("counts", {}).get("coverage", {})
    if coverage.get("required_completed_season_cutoff") != required:
        raise ExpansionStage4CoverageError(
            "Research report completed-season cutoff disagrees with baseline proof"
        )
    if coverage.get("required_season_rows") != 0:
        raise ExpansionStage4CoverageError(
            "supplemental package must not contain inherited completed-season games"
        )
    errors = list(report.get("errors", []))
    if errors.count(expected_error) != 1:
        raise ExpansionStage4CoverageError(
            "ordinary Research report must contain the one proved "
            "completed-season error exactly once"
        )
    remaining = [error for error in errors if error != expected_error]
    adjusted = dict(report)
    adjusted["errors"] = remaining
    adjusted["status"] = "PASS" if not remaining else "FAIL"
    adjusted["warnings"] = list(report.get("warnings", [])) + [
        "All-History expansion: required completed season was authenticated "
        "in inherited published history at the immutable research_base_sha; "
        "it is intentionally absent from this supplemental-only package."
    ]
    adjusted["counts"] = dict(report["counts"])
    adjusted["counts"]["coverage"] = {
        **coverage,
        "acceptance_scope": "ALL_HISTORY_EXPANSION_SUPPLEMENTAL",
        "inherited_published_required_season_source_rows": proof[
            "inherited_required_season_source_rows"
        ],
        "inherited_published_required_season_canonical_rows": proof[
            "inherited_required_season_published_canonical_rows"
        ],
        "authenticated_research_base_sha": proof["research_base_sha"],
    }
    adjusted["expansion_coverage_proof"] = dict(proof)
    return adjusted
