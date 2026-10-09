"""Conservative owner-review eligibility for generic postseason source history.

This module DOES NOT classify games.  It only supplies stable, source-bound
Gate 1 review rows where the NCAA accomplishment mismatch could plausibly be
caused by an explicitly generic POSTSEASON source population.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

REVIEW_TYPES = frozenset({
    "NCAA_TOURNAMENT", "NIT", "CONFERENCE_TOURNAMENT",
})
REVIEW_ACTIONS = frozenset({
    "APPLY_POSTSEASON_CLASSIFICATION_PATCH", "KEEP_POSTSEASON_UNRESOLVED",
})
NCAA_ROUNDS = frozenset({
    "Play-in", "R64", "R32", "Sweet Sixteen", "Elite Eight",
    "Final Four", "Championship",
})
REVIEW_SITES = frozenset({
    "SOURCE_PROGRAM_HOME", "OPPONENT_HOME", "NEUTRAL",
})


def row_fingerprint(source: dict[str, str]) -> str:
    """Bind one review to the complete, unchanged staged source row."""
    payload = json.dumps(
        source, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def mismatch_is_reviewable(
    reference: dict[str, str],
    derived: dict[str, Any],
    candidate_rows: list[dict[str, Any]],
) -> bool:
    """Gate eligibility only; NEVER treat a proposed aggregate as verified.

    Existing NCAA appearance seasons already counted by canonical projections
    cannot be counted again.  Missing appearance seasons must be explainable by
    distinct still-generic source seasons.  Existing earned NCAA totals cannot
    be reduced by hypothetical postseason classification.
    """
    try:
        expected_appearances = int(reference["ncaa_tournament_appearances"])
        expected_final_fours = int(reference["final_four_appearances"])
        expected_championships = int(reference["national_championships"])
        actual_appearances = int(derived["ncaa_tournament_appearances"])
        actual_final_fours = int(derived["final_four_appearances"])
        actual_championships = int(derived["national_championships"])
    except (KeyError, TypeError, ValueError):
        return False
    if not candidate_rows or expected_appearances <= actual_appearances:
        return False
    if (expected_final_fours < actual_final_fours or
            expected_championships < actual_championships or
            expected_final_fours > expected_appearances or
            expected_championships > expected_final_fours):
        return False
    eligible_seasons = {
        str(item["source"].get("season_label", "")).strip()
        for item in candidate_rows
        if str(item["source"].get("season_label", "")).strip()
    }
    return (
        expected_appearances - actual_appearances <= len(eligible_seasons)
        and expected_appearances >= expected_final_fours
    )


def build_review_rows(
    school_key: str,
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Produce one unapproved Gate 1 decision per generic source game."""
    decisions: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in candidates:
        source = item["source"]
        source_id = str(source.get("source_game_id", "")).strip()
        if not source_id or source_id in seen:
            raise ValueError("postseason review requires unique nonblank source IDs")
        if source.get("curated_game_type", "").strip() != "POSTSEASON":
            raise ValueError("postseason review may only target generic POSTSEASON")
        seen.add(source_id)
        date = source.get("game_date", "").strip()
        opponent = source.get("normalized_opponent_key", "").strip()
        decisions.append({
            "decision_id": "POSTSEASON-CLASSIFICATION-" + source_id,
            "category": "postseason_classification",
            "source_game_id": source_id,
            "canonical_game_id": str(item.get("canonical_game_id", "") or ""),
            "season_label": source.get("season_label", "").strip(),
            "source_game_date": date,
            "canonical_game_date": str(item.get("canonical_game_date", "") or ""),
            "matchup": f"{school_key} vs {opponent}",
            "field_name": "game_type",
            "source_value": "POSTSEASON",
            "canonical_value": str(item.get("canonical_game_type", "") or ""),
            "source_row_sha256": row_fingerprint(source),
            "original_site_type": source.get("curated_site_type", "").strip(),
            "relevant_evidence": (
                "Source type is generic POSTSEASON; institutional tournament "
                "classification and controlled NCAA round (when applicable) "
                "must be supported in this exact row's owner approval. "
                "Original source: " + source.get("raw_text", "").strip()[:240]
            ),
            "recommended_action": "REVIEW_REQUIRED",
            "allowed_actions": sorted(REVIEW_ACTIONS),
            "decision": "PENDING",
            "resolution_basis": "",
            "canonical_patch_json": "{}",
            "source_patch_json": "{}",
            "notes": (
                "No automatic NCAA/NIT/conference assignment, round inference, "
                "or H/A/N change. Raw source text and Research Freeze remain preserved."
            ),
        })
    return decisions
