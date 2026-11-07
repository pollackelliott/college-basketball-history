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

HISTORICAL_CHALLENGE_KIND = "STAGE2_HISTORICAL_GAME_TYPE_CHALLENGES"
HISTORICAL_CHALLENGE_LEGACY_TYPE = "REGULAR_TO_NCAA_TOURNAMENT"
HISTORICAL_CHALLENGE_NONAPPEARANCE_TYPE = "NCAA_NON_APPEARANCE_QUALIFIER"
HISTORICAL_CHALLENGE_SOURCE_TYPE = "REGULAR_SEASON"
HISTORICAL_CHALLENGE_TARGET_TYPE = "NCAA_TOURNAMENT"
HISTORICAL_CHALLENGE_ACTION = "APPLY_POSTSEASON_CLASSIFICATION_PATCH"
HISTORICAL_CHALLENGE_CANONICAL_IDENTITY_FIELDS = (
    "season_label",
    "game_date",
    "team_a_key",
    "team_b_key",
    "team_a_score",
    "team_b_score",
    "result_winner_team_key",
    "overtime_periods",
    "site_type",
    "designated_home_team_key",
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
)


def row_fingerprint(source: dict[str, str]) -> str:
    """Bind one review to the complete, unchanged staged source row."""
    payload = json.dumps(
        source, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_historical_game_type_challenges(
    document: dict[str, Any] | None,
    school_key: str,
) -> dict[str, dict[str, str]]:
    """Validate an external, hash-bound challenge document without approving it."""

    if document is None:
        return {}
    if not isinstance(document, dict):
        raise ValueError("historical game-type challenge must be a JSON object")
    if document.get("schema_version") != 1:
        raise ValueError("historical game-type challenge schema_version must be 1")
    if document.get("kind") != HISTORICAL_CHALLENGE_KIND:
        raise ValueError("historical game-type challenge kind is unsupported")
    if str(document.get("school_key", "")).strip() != school_key:
        raise ValueError("historical game-type challenge school_key mismatch")
    allowed_top = {"schema_version", "kind", "school_key", "challenges", "authority_basis"}
    unknown_top = sorted(set(document) - allowed_top)
    if unknown_top:
        raise ValueError(
            "historical game-type challenge has unknown top-level fields: "
            + ", ".join(unknown_top)
        )
    if not str(document.get("authority_basis", "")).strip():
        raise ValueError("historical game-type challenge authority_basis is required")
    rows = document.get("challenges")
    if not isinstance(rows, list) or not rows:
        raise ValueError("historical game-type challenge requires a nonempty challenges list")

    legacy_required = {
        "source_game_id",
        "source_row_sha256",
        "expected_source_game_type",
        "proposed_source_game_type",
        "evidence_basis",
    }
    qualifier_required = legacy_required | {
        "challenge_type",
        "expected_source_postseason_round",
        "proposed_source_postseason_round",
    }
    result: dict[str, dict[str, str]] = {}
    for raw in rows:
        if not isinstance(raw, dict):
            raise ValueError("historical game-type challenge rows must be objects")
        raw_fields = set(raw)
        if raw_fields == legacy_required:
            challenge_type = HISTORICAL_CHALLENGE_LEGACY_TYPE
        elif raw_fields == qualifier_required:
            challenge_type = str(raw.get("challenge_type", "")).strip()
            if challenge_type != HISTORICAL_CHALLENGE_NONAPPEARANCE_TYPE:
                raise ValueError(
                    "historical qualifier challenge_type is unsupported"
                )
        else:
            raise ValueError(
                "historical game-type challenge rows require exactly either legacy fields "
                "or the qualifier extension fields"
            )
        source_id = str(raw.get("source_game_id", "")).strip()
        if not source_id or source_id in result:
            raise ValueError(
                "historical game-type challenge requires unique nonblank source_game_id"
            )
        fingerprint = str(raw.get("source_row_sha256", "")).strip().lower()
        if len(fingerprint) != 64 or any(ch not in "0123456789abcdef" for ch in fingerprint):
            raise ValueError(
                f"{source_id}: historical game-type challenge source_row_sha256 is invalid"
            )
        expected = str(raw.get("expected_source_game_type", "")).strip()
        proposed = str(raw.get("proposed_source_game_type", "")).strip()
        if challenge_type == HISTORICAL_CHALLENGE_LEGACY_TYPE:
            if expected != HISTORICAL_CHALLENGE_SOURCE_TYPE:
                raise ValueError(
                    f"{source_id}: challenge may only begin from "
                    f"{HISTORICAL_CHALLENGE_SOURCE_TYPE}"
                )
            if proposed != HISTORICAL_CHALLENGE_TARGET_TYPE:
                raise ValueError(
                    f"{source_id}: challenge may only propose "
                    f"{HISTORICAL_CHALLENGE_TARGET_TYPE}"
                )
        else:
            if (
                expected != "NCAA_TOURNAMENT"
                or proposed != "NCAA_TOURNAMENT"
            ):
                raise ValueError(
                    f"{source_id}: non-appearance qualifier challenge must remain "
                    "broad NCAA_TOURNAMENT"
                )
            expected_round = str(
                raw.get("expected_source_postseason_round", "")
            ).strip()
            proposed_round = str(
                raw.get("proposed_source_postseason_round", "")
            ).strip()
            if not expected_round or expected_round not in NCAA_ROUNDS:
                raise ValueError(
                    f"{source_id}: non-appearance qualifier challenge requires "
                    "one exact nonblank controlled NCAA round"
                )
            if proposed_round:
                raise ValueError(
                    f"{source_id}: non-appearance qualifier challenge must clear "
                    "the controlled NCAA round"
                )
        basis = str(raw.get("evidence_basis", "")).strip()
        if not basis:
            raise ValueError(f"{source_id}: challenge evidence_basis is required")
        parsed = {
            "source_game_id": source_id,
            "source_row_sha256": fingerprint,
            "expected_source_game_type": expected,
            "proposed_source_game_type": proposed,
            "challenge_type": challenge_type,
            "evidence_basis": basis,
        }
        if challenge_type == HISTORICAL_CHALLENGE_NONAPPEARANCE_TYPE:
            parsed["expected_source_postseason_round"] = str(
                raw["expected_source_postseason_round"]
            ).strip()
            parsed["proposed_source_postseason_round"] = ""
        result[source_id] = parsed
    return result


def build_historical_game_type_challenge_review(
    school_key: str,
    candidate: dict[str, Any],
    challenge: dict[str, str],
    expected_canonical_identity: dict[str, str],
) -> dict[str, Any]:
    """Expose one exact post-freeze contradiction as pending Gate 1 material."""

    source = candidate["source"]
    source_id = str(source.get("source_game_id", "")).strip()
    if source_id != challenge["source_game_id"]:
        raise ValueError("historical challenge source identity mismatch")
    if row_fingerprint(source) != challenge["source_row_sha256"]:
        raise ValueError(
            f"{source_id}: historical challenge frozen source-row fingerprint mismatch"
        )
    if source.get("curated_game_type", "").strip() != challenge[
        "expected_source_game_type"
    ]:
        raise ValueError(
            f"{source_id}: historical challenge source game type changed"
        )
    challenge_type = challenge.get(
        "challenge_type", HISTORICAL_CHALLENGE_LEGACY_TYPE
    )
    if challenge_type == HISTORICAL_CHALLENGE_NONAPPEARANCE_TYPE:
        expected_round = challenge["expected_source_postseason_round"]
        if source.get("curated_postseason_round", "").strip() != expected_round:
            raise ValueError(
                f"{source_id}: historical qualifier challenge source round changed"
            )
    if candidate.get("planned_identity_status") != "NEW_GAME":
        raise ValueError(
            f"{source_id}: historical game-type challenge currently requires NEW_GAME identity"
        )
    if not expected_canonical_identity or set(expected_canonical_identity) != set(
        HISTORICAL_CHALLENGE_CANONICAL_IDENTITY_FIELDS
    ):
        raise ValueError(
            f"{source_id}: historical challenge canonical identity is incomplete"
        )

    if challenge_type == HISTORICAL_CHALLENGE_NONAPPEARANCE_TYPE:
        return {
            "decision_id": "HISTORICAL-NCAA-QUALIFIER-" + source_id,
            "category": "postseason_classification",
            "source_game_id": source_id,
            "canonical_game_id": "",
            "season_label": source.get("season_label", "").strip(),
            "source_game_date": source.get("game_date", "").strip(),
            "canonical_game_date": source.get("game_date", "").strip(),
            "matchup": (
                f"{school_key} vs "
                + source.get("normalized_opponent_key", "").strip()
            ),
            "field_name": "postseason_round",
            "source_value": challenge["expected_source_postseason_round"],
            "canonical_value": "",
            "source_row_sha256": challenge["source_row_sha256"],
            "frozen_source_row": dict(source),
            "expected_canonical_identity": dict(expected_canonical_identity),
            "planned_identity_status": "NEW_GAME",
            "historical_ncaa_nonappearance_qualifier_challenge": True,
            "source_game_type": "NCAA_TOURNAMENT",
            "expected_source_postseason_round": challenge[
                "expected_source_postseason_round"
            ],
            "proposed_game_type": "NCAA_TOURNAMENT",
            "proposed_postseason_round": "",
            "original_site_type": source.get("curated_site_type", "").strip(),
            "relevant_evidence": (
                challenge["evidence_basis"]
                + " This is a post-freeze NCAA non-appearance qualifier challenge only; "
                "Owner Gate 1 must explicitly approve clearing the controlled round "
                "and applying the durable qualifier marker."
            ),
            "recommended_action": HISTORICAL_CHALLENGE_ACTION,
            "allowed_actions": [HISTORICAL_CHALLENGE_ACTION],
            "decision": "PENDING",
            "resolution_basis": "",
            "canonical_patch_json": "{}",
            "source_patch_json": "{}",
            "notes": (
                "Exact frozen row and post-ingest canonical identity are bound. "
                "curated_game_type must remain NCAA_TOURNAMENT; only the controlled "
                "postseason round may be cleared and the durable non-appearance "
                "qualifier marker appended. H/A/N, venue/location, score/result, "
                "overtime, raw evidence, and unrelated source fields are unchanged."
            ),
        }

    return {
        "decision_id": "HISTORICAL-GAME-TYPE-" + source_id,
        "category": "postseason_classification",
        "source_game_id": source_id,
        "canonical_game_id": "",
        "season_label": source.get("season_label", "").strip(),
        "source_game_date": source.get("game_date", "").strip(),
        "canonical_game_date": source.get("game_date", "").strip(),
        "matchup": (
            f"{school_key} vs "
            + source.get("normalized_opponent_key", "").strip()
        ),
        "field_name": "game_type",
        "source_value": challenge["expected_source_game_type"],
        "canonical_value": "",
        "source_row_sha256": challenge["source_row_sha256"],
        "frozen_source_row": dict(source),
        "expected_canonical_identity": dict(expected_canonical_identity),
        "planned_identity_status": "NEW_GAME",
        "historical_game_type_challenge": True,
        "proposed_game_type": challenge["proposed_source_game_type"],
        "original_site_type": source.get("curated_site_type", "").strip(),
        "relevant_evidence": (
            challenge["evidence_basis"]
            + " This is a post-freeze contradiction challenge only; "
            "Owner Gate 1 must explicitly approve the game-type correction."
        ),
        "recommended_action": HISTORICAL_CHALLENGE_ACTION,
        "allowed_actions": [HISTORICAL_CHALLENGE_ACTION],
        "decision": "PENDING",
        "resolution_basis": "",
        "canonical_patch_json": "{}",
        "source_patch_json": "{}",
        "notes": (
            "Exact frozen row and post-ingest canonical identity are bound. "
            "Only curated_game_type may change; no postseason round, H/A/N, "
            "venue/location, score/result, overtime, raw evidence, or unrelated "
            "source field is authorized."
        ),
    }


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


def nonappearance_qualifier_mismatch_is_reviewable(
    reference: dict[str, str],
    derived: dict[str, Any],
    candidate_rows: list[dict[str, Any]],
    appearance_game_counts_by_season: dict[str, int],
) -> bool:
    """Return whether exact qualifier challenges can explain an appearance surplus.

    Only seasons represented by one and only one currently appearance-counting
    NCAA game are removable at this boundary. Final Four and championship totals
    must already agree because a qualifier challenge may not erase earned bracket
    accomplishments.
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
    if (
        expected_appearances >= actual_appearances
        or expected_final_fours != actual_final_fours
        or expected_championships != actual_championships
    ):
        return False
    eligible_seasons = {
        str(item["source"].get("season_label", "")).strip()
        for item in candidate_rows
        if item.get("historical_challenge_type")
        == HISTORICAL_CHALLENGE_NONAPPEARANCE_TYPE
        and str(item["source"].get("season_label", "")).strip()
        and appearance_game_counts_by_season.get(
            str(item["source"].get("season_label", "")).strip(), 0
        )
        == 1
    }
    return actual_appearances - expected_appearances <= len(eligible_seasons)


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
