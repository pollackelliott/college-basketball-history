#!/usr/bin/env python3
"""Pure authority primitives for supplemental All-History expansion Research.

This module classifies an already-published LEGACY_TOP_LEVEL_ONLY baseline and
projects the only metadata transition that a future successful serialized
ALL_HISTORY_EXPANSION Implementation may make. It does not read or write
repository state and does not create Research Freeze artifacts.
"""
from __future__ import annotations

from typing import Mapping

from program_history import (
    history_coverage_errors,
    history_scope_errors,
    season_is_published_history,
    valid_season_label,
)


PRE_INCEPTION = "PRE_INCEPTION"
BASELINE_PUBLISHED = "BASELINE_PUBLISHED"
EXPANSION_REQUIRED = "EXPANSION_REQUIRED"
EXPANSION_SEASON_DISPOSITIONS = frozenset(
    {PRE_INCEPTION, BASELINE_PUBLISHED, EXPANSION_REQUIRED}
)


class ExpansionResearchAuthorityError(ValueError):
    """Fail-closed expansion Research authority error."""


def _text_field(program: Mapping[str, str], field: str) -> str:
    value = program.get(field, "")
    if not isinstance(value, str):
        raise ExpansionResearchAuthorityError(
            f"{field} must be a string for expansion Research authority"
        )
    return value.strip()


def _valid_season(value: str, label: str) -> str:
    if not isinstance(value, str) or not valid_season_label(value):
        raise ExpansionResearchAuthorityError(
            f"{label} must be a valid canonical season label"
        )
    return value.strip()


def validate_expansion_baseline_program(
    program: Mapping[str, str],
) -> None:
    """Validate one immutable published LEGACY baseline for expansion Research."""

    public = _text_field(program, "public_page_enabled")
    status = _text_field(program, "history_coverage_status")

    problems: list[str] = []
    if public != "Yes":
        problems.append("public_page_enabled must be Yes")
    if status != "LEGACY_TOP_LEVEL_ONLY":
        problems.append(
            "history_coverage_status must be LEGACY_TOP_LEVEL_ONLY"
        )

    try:
        coverage = history_coverage_errors(
            dict(program),
            public=(public == "Yes"),
        )
        scope = history_scope_errors(dict(program), required=True)
    except (AttributeError, TypeError, ValueError) as exc:
        raise ExpansionResearchAuthorityError(
            f"malformed expansion baseline metadata: {exc}"
        ) from exc

    problems.extend(coverage)
    problems.extend(scope)
    if problems:
        raise ExpansionResearchAuthorityError(
            "invalid ALL_HISTORY_EXPANSION baseline: " + "; ".join(problems)
        )


def _validate_researched_inception(
    baseline_program: Mapping[str, str],
    researched_inception_season: str,
) -> str:
    inception = _valid_season(
        researched_inception_season,
        "researched_inception_season",
    )
    baseline_inception = _text_field(
        baseline_program,
        "program_inception_season",
    )
    if baseline_inception:
        _valid_season(baseline_inception, "program_inception_season")
        if baseline_inception != inception:
            raise ExpansionResearchAuthorityError(
                "researched inception conflicts with the authenticated baseline "
                "program_inception_season"
            )

    history_start = _valid_season(
        _text_field(baseline_program, "history_start_season"),
        "history_start_season",
    )
    if inception > history_start:
        raise ExpansionResearchAuthorityError(
            "researched inception cannot be later than already-published "
            "top-level history_start_season"
        )
    return inception


def expansion_season_disposition(
    season_label: str,
    baseline_program: Mapping[str, str],
    researched_inception_season: str,
) -> str:
    """Classify publication authority for one season without inferring team activity."""

    validate_expansion_baseline_program(baseline_program)
    season = _valid_season(season_label, "season_label")
    inception = _validate_researched_inception(
        baseline_program,
        researched_inception_season,
    )

    if season < inception:
        return PRE_INCEPTION

    if season_is_published_history(season, dict(baseline_program)):
        return BASELINE_PUBLISHED
    return EXPANSION_REQUIRED


def project_complete_institutional_program_row(
    baseline_program: Mapping[str, str],
    researched_inception_season: str,
) -> dict[str, str]:
    """Return the exact future COMPLETE_INSTITUTIONAL metadata projection."""

    validate_expansion_baseline_program(baseline_program)
    inception = _validate_researched_inception(
        baseline_program,
        researched_inception_season,
    )
    projected = dict(baseline_program)
    projected["program_inception_season"] = inception
    projected["history_coverage_status"] = "COMPLETE_INSTITUTIONAL"
    return projected
