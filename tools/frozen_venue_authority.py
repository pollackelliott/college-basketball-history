#!/usr/bin/env python3
"""Authenticate frozen per-source-game venue split authority for runtime use.

This module is dependency-neutral so both Stage 2 planning and ingestion/apply can
consume the exact same Integration-Freeze authority without creating import cycles.
It never infers venue identity. It only authenticates already-frozen per-game split
assignments against the current source semantic snapshot and frozen venues.csv bytes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


class FrozenVenueSplitAuthorityError(ValueError):
    """The Integration Freeze venue-split authority is missing trust invariants."""


PRE_INGEST_SEMANTIC_FIELDS = frozenset({
    "season_label",
    "game_date",
    "curated_site_type",
    "curated_game_type",
    "curated_postseason_round",
})


def sealed_pre_ingest_semantic_delta(
    approved: dict[str, Any] | None,
) -> dict[str, dict[str, str]]:
    """Derive the exact Freeze-covered delta authorized by one sealed plan.

    This deliberately mirrors only source mutations that occur before ingestion.
    Other source patches either happen later or affect representation-only fields
    outside the Integration-Freeze semantic snapshot.
    """

    if not approved:
        return {}
    approved_hash = str(approved.get("approved_plan_hash", "")).strip()
    if not re.fullmatch(r"[0-9a-f]{64}", approved_hash):
        raise FrozenVenueSplitAuthorityError(
            "sealed pre-ingest semantic delta requires an approved plan hash"
        )
    decisions = approved.get("decisions")
    if not isinstance(decisions, list):
        raise FrozenVenueSplitAuthorityError(
            "sealed pre-ingest semantic delta requires a decision list"
        )

    result: dict[str, dict[str, str]] = {}

    def add_fields(item: dict[str, Any], fields: dict[str, Any]) -> None:
        if not fields:
            return
        source_id = str(item.get("source_game_id", "")).strip()
        if not source_id:
            raise FrozenVenueSplitAuthorityError(
                "sealed pre-ingest semantic delta has a blank source_game_id"
            )
        target = result.setdefault(source_id, {})
        for field, value in fields.items():
            if field not in PRE_INGEST_SEMANTIC_FIELDS:
                raise FrozenVenueSplitAuthorityError(
                    f"sealed pre-ingest semantic delta contains unsupported field {field!r}"
                )
            normalized = str(value)
            prior = target.get(field)
            if prior is not None and prior != normalized:
                raise FrozenVenueSplitAuthorityError(
                    f"sealed pre-ingest semantic delta conflicts for {source_id} {field}"
                )
            target[field] = normalized

    for item in decisions:
        if not isinstance(item, dict):
            raise FrozenVenueSplitAuthorityError(
                "sealed pre-ingest semantic delta contains an invalid decision"
            )
        category = str(item.get("category", "")).strip()
        action = str(item.get("decision", "")).strip()
        patch = item.get("source_patch", {})
        if patch is None:
            patch = {}
        if not isinstance(patch, dict):
            raise FrozenVenueSplitAuthorityError(
                f"{item.get('decision_id', '')}: source_patch is not an object"
            )

        if category == "postseason_classification":
            if action == "APPLY_POSTSEASON_CLASSIFICATION_PATCH":
                allowed = {
                    field: patch[field]
                    for field in (
                        "curated_game_type",
                        "curated_postseason_round",
                        "curated_site_type",
                    )
                    if field in patch
                }
                if set(patch) != set(allowed):
                    raise FrozenVenueSplitAuthorityError(
                        f"{item.get('decision_id', '')}: postseason pre-ingest delta "
                        "contains unsupported fields"
                    )
                add_fields(item, allowed)
            elif action == "KEEP_POSTSEASON_UNRESOLVED":
                if patch:
                    raise FrozenVenueSplitAuthorityError(
                        f"{item.get('decision_id', '')}: unresolved postseason row "
                        "cannot carry a pre-ingest semantic delta"
                    )

        elif category == "new_game_site_patch":
            if action == "APPLY_SOURCE_SITE_PATCH":
                if set(patch) != {"curated_site_type"}:
                    raise FrozenVenueSplitAuthorityError(
                        f"{item.get('decision_id', '')}: new-game site delta must "
                        "contain exactly curated_site_type"
                    )
                add_fields(item, {"curated_site_type": patch["curated_site_type"]})

        elif category == "new_game_date_patch":
            if action == "APPLY_SOURCE_DATE_PATCH":
                if set(patch) != {"game_date"}:
                    raise FrozenVenueSplitAuthorityError(
                        f"{item.get('decision_id', '')}: new-game date delta must "
                        "contain exactly game_date"
                    )
                add_fields(item, {"game_date": patch["game_date"]})

        elif category == "ncaa_round_patch" and "game_date" in patch:
            add_fields(item, {"game_date": patch["game_date"]})

        elif category == "identity":
            expected = item.get("cross_season_source_patch_by_action", {})
            selected = expected.get(action) if isinstance(expected, dict) else None
            if selected is not None:
                if (
                    not isinstance(selected, dict)
                    or patch != selected
                    or set(selected) != {"season_label", "game_date"}
                ):
                    raise FrozenVenueSplitAuthorityError(
                        f"{item.get('decision_id', '')}: adjacent-season semantic "
                        "delta does not match the sealed preflight patch"
                    )
                add_fields(
                    item,
                    {
                        "season_label": selected["season_label"],
                        "game_date": selected["game_date"],
                    },
                )

    return result


FINAL_SOURCE_SEMANTIC_FIELDS = frozenset({
    "season_label",
    "game_date",
    "team_score",
    "opponent_score",
    "played_result",
    "overtime_periods",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
    "event_or_tournament",
    "curated_game_type",
    "curated_postseason_round",
    "source_opponent_label",
    "raw_text",
})

POST_RECONCILIATION_NORMALIZATION_FIELDS = frozenset({
    "game_date",
    "score",
    "overtime_periods",
    "site_type",
    "game_type",
    "postseason_round",
    "result_winner_team_key",
})

DIRECT_POST_RECONCILIATION_PATCH_CATEGORIES = frozenset({
    "discrepancy",
    "conditional_discrepancy",
})


def _canonical_review_value(row: dict[str, str], field_name: str) -> str:
    if field_name == "score":
        return f"{row.get('team_a_score', '')}-{row.get('team_b_score', '')}"
    return row.get(field_name, "")


def _venue_names_by_key(repo_root: Path) -> dict[str, str]:
    """Mirror onboarding_plan._venue_maps canonical-name selection."""

    names_by_key: dict[str, str] = {}
    for path in sorted((repo_root / "schools").glob("*/venues.csv")):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                key = row.get("venue_key", "").strip()
                name = row.get("canonical_name", "").strip()
                if key and name:
                    names_by_key.setdefault(key, name)
    return names_by_key


def _normalized_source_projection(
    canonical: dict[str, str],
    school_key: str,
    field_name: str,
    expected: str,
    venue_names: dict[str, str],
) -> dict[str, str]:
    """Project exactly what onboarding_plan.set_source_field writes.

    Site normalization also mirrors the immediately-following
    _sync_site_metadata_to_source call. This function is deliberately pure and
    dependency-neutral so final no-op authentication cannot import onboarding_plan.
    """

    if field_name not in POST_RECONCILIATION_NORMALIZATION_FIELDS:
        raise FrozenVenueSplitAuthorityError(
            f"sealed post-reconciliation normalization has unsupported field {field_name!r}"
        )

    current = _canonical_review_value(canonical, field_name)
    if current != expected:
        raise FrozenVenueSplitAuthorityError(
            f"sealed canonical {field_name} no longer matches"
        )

    team_a = canonical.get("team_a_key", "").strip()
    team_b = canonical.get("team_b_key", "").strip()
    if field_name in {"score", "site_type", "result_winner_team_key"}:
        if school_key not in {team_a, team_b}:
            raise FrozenVenueSplitAuthorityError(
                "target school is absent from the sealed canonical game"
            )

    if field_name == "score":
        try:
            score_a, score_b = expected.split("-", 1)
            number_a = int(score_a)
            number_b = int(score_b)
        except (ValueError, TypeError) as exc:
            raise FrozenVenueSplitAuthorityError(
                "sealed canonical score is not an exact integer score pair"
            ) from exc
        if school_key == team_a:
            team_score, opponent_score = score_a, score_b
            team_number, opponent_number = number_a, number_b
        else:
            team_score, opponent_score = score_b, score_a
            team_number, opponent_number = number_b, number_a
        played_result = (
            "W"
            if team_number > opponent_number
            else "L"
            if opponent_number > team_number
            else "T"
        )
        return {
            "team_score": team_score,
            "opponent_score": opponent_score,
            "played_result": played_result,
        }

    if field_name == "site_type":
        if expected in {"NEUTRAL", "UNKNOWN", ""}:
            normalized = expected or "UNKNOWN"
        elif expected == "TEAM_A_HOME":
            normalized = (
                "SOURCE_PROGRAM_HOME" if team_a == school_key else "OPPONENT_HOME"
            )
        elif expected == "TEAM_B_HOME":
            normalized = (
                "SOURCE_PROGRAM_HOME" if team_b == school_key else "OPPONENT_HOME"
            )
        else:
            raise FrozenVenueSplitAuthorityError(
                f"unsupported canonical site_type {expected!r}"
            )
        venue_key = canonical.get("venue_key", "").strip()
        return {
            "curated_site_type": normalized,
            "curated_venue_name": venue_names.get(venue_key, "") if venue_key else "",
            "city": canonical.get("site_city", ""),
            "state": canonical.get("site_state", ""),
        }

    if field_name == "game_type":
        return {"curated_game_type": expected}
    if field_name == "postseason_round":
        return {"curated_postseason_round": expected}
    if field_name == "result_winner_team_key":
        if expected in {"[TIE]", ""}:
            played_result = "T"
        elif expected == school_key:
            played_result = "W"
        elif expected in {team_a, team_b}:
            played_result = "L"
        else:
            raise FrozenVenueSplitAuthorityError(
                f"unsupported canonical result_winner_team_key {expected!r}"
            )
        return {"played_result": played_result}

    return {field_name: expected}


def sealed_post_reconciliation_semantic_delta(
    repo_root: Path,
    school_key: str,
    approved: dict[str, Any] | None,
) -> dict[str, dict[str, str]]:
    """Derive exact frozen-source semantics after sealed reconciliation finishes.

    Pre-ingest authority stays deliberately narrow. Final no-op verification may
    additionally authenticate only source mutations deterministically produced by
    the sealed permanent reconciliation transaction: the complete supported
    NORMALIZE_SOURCE_TO_CANONICAL field universe, exact direct source patches, and
    source-consistency patches in their real execution order.
    """

    result = {
        source_id: dict(fields)
        for source_id, fields in sealed_pre_ingest_semantic_delta(approved).items()
    }
    if not approved:
        return result
    if str(approved.get("school_key", "")).strip() != school_key:
        raise FrozenVenueSplitAuthorityError(
            "sealed post-reconciliation semantic delta school_key mismatch"
        )

    canonical_path = repo_root / "data" / "canonical" / "games.csv"
    if not canonical_path.is_file():
        raise FrozenVenueSplitAuthorityError(
            "sealed post-reconciliation semantic delta requires canonical games"
        )
    canonical_by_id: dict[str, dict[str, str]] = {}
    with canonical_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            game_id = row.get("canonical_game_id", "").strip()
            if not game_id or game_id in canonical_by_id:
                raise FrozenVenueSplitAuthorityError(
                    "sealed post-reconciliation semantic delta has invalid canonical identity"
                )
            canonical_by_id[game_id] = row

    decisions = approved.get("decisions")
    if not isinstance(decisions, list):
        raise FrozenVenueSplitAuthorityError(
            "sealed post-reconciliation semantic delta requires a decision list"
        )

    venue_names = _venue_names_by_key(repo_root)
    source_consistency_items: list[dict[str, Any]] = []

    def apply_exact_patch(
        item: dict[str, Any],
        patch: dict[str, Any],
        *,
        allow_raw_text: bool = False,
    ) -> None:
        source_id = str(item.get("source_game_id", "")).strip()
        guarded = {
            field: str(value)
            for field, value in patch.items()
            if field in FINAL_SOURCE_SEMANTIC_FIELDS
        }
        if "raw_text" in guarded and not allow_raw_text:
            raise FrozenVenueSplitAuthorityError(
                f"{item.get('decision_id', '')}: sealed source patch may not mutate raw_text"
            )
        if guarded and not source_id:
            raise FrozenVenueSplitAuthorityError(
                "sealed post-reconciliation source patch has a blank source_game_id"
            )
        if guarded:
            result.setdefault(source_id, {}).update(guarded)

    for item in decisions:
        if not isinstance(item, dict):
            raise FrozenVenueSplitAuthorityError(
                "sealed post-reconciliation semantic delta contains an invalid decision"
            )
        category = str(item.get("category", "")).strip()
        action = str(item.get("decision", "")).strip()
        source_id = str(item.get("source_game_id", "")).strip()
        field_name = str(item.get("field_name", "")).strip()
        patch = item.get("source_patch", {})
        if patch is None:
            patch = {}
        if not isinstance(patch, dict):
            raise FrozenVenueSplitAuthorityError(
                f"{item.get('decision_id', '')}: source_patch is not an object"
            )

        if category == "source_consistency":
            source_consistency_items.append(item)
            continue

        if action == "NORMALIZE_SOURCE_TO_CANONICAL":
            if category not in DIRECT_POST_RECONCILIATION_PATCH_CATEGORIES:
                raise FrozenVenueSplitAuthorityError(
                    f"{item.get('decision_id', '')}: normalization is not a discrepancy decision"
                )
            if not source_id:
                raise FrozenVenueSplitAuthorityError(
                    "sealed post-reconciliation normalization has a blank source_game_id"
                )
            game_id = str(item.get("canonical_game_id", "")).strip()
            canonical = canonical_by_id.get(game_id)
            if canonical is None:
                raise FrozenVenueSplitAuthorityError(
                    f"sealed post-reconciliation normalization references unknown canonical game {game_id}"
                )

            canonical_patch = item.get("canonical_patch", {})
            if canonical_patch is None:
                canonical_patch = {}
            if not isinstance(canonical_patch, dict):
                raise FrozenVenueSplitAuthorityError(
                    f"{item.get('decision_id', '')}: canonical_patch is not an object"
                )
            if (
                field_name == "site_type"
                and set(canonical_patch)
                & {"venue_key", "venue_id", "site_city", "site_state"}
                and not {"curated_venue_name", "city", "state"} <= set(patch)
            ):
                raise FrozenVenueSplitAuthorityError(
                    f"{item.get('decision_id', '')}: cannot reconstruct pre-patch site metadata"
                )

            expected = str(item.get("canonical_value", ""))
            projection = _normalized_source_projection(
                canonical,
                school_key,
                field_name,
                expected,
                venue_names,
            )
            result.setdefault(source_id, {}).update(projection)

        if category in DIRECT_POST_RECONCILIATION_PATCH_CATEGORIES:
            # Generic reconciliation writes source_patch after normalization.
            apply_exact_patch(item, patch)
        elif category == "ncaa_round_patch":
            if action == "APPLY_NCAA_ROUND_PATCH" and "curated_postseason_round" in patch:
                game_id = str(item.get("canonical_game_id", "")).strip()
                canonical = canonical_by_id.get(game_id)
                desired = str(patch["curated_postseason_round"])
                if canonical is None or canonical.get("postseason_round", "") != desired:
                    raise FrozenVenueSplitAuthorityError(
                        f"{item.get('decision_id', '')}: sealed canonical postseason_round no longer matches"
                    )
                apply_exact_patch(
                    item,
                    {"curated_postseason_round": desired},
                )

        # Every other guarded source patch must already have been authenticated
        # by the narrower pre-ingest path. Anything else is a new/unsupported
        # post-freeze mutation and therefore fails closed.
        for field, value in patch.items():
            if field not in FINAL_SOURCE_SEMANTIC_FIELDS:
                continue
            if (
                category in DIRECT_POST_RECONCILIATION_PATCH_CATEGORIES
                or category == "source_consistency"
                or (
                    category == "ncaa_round_patch"
                    and field == "curated_postseason_round"
                    and action == "APPLY_NCAA_ROUND_PATCH"
                )
            ):
                continue
            if result.get(source_id, {}).get(field) != str(value):
                raise FrozenVenueSplitAuthorityError(
                    f"{item.get('decision_id', '')}: unsupported sealed final source mutation {field!r}"
                )

    # Permanent reconciliation processes source-consistency decisions only after
    # all discrepancy normalization/source-patch work, regardless of plan order.
    for item in source_consistency_items:
        decision_id = str(item.get("decision_id", ""))
        if str(item.get("decision", "")).strip() != "APPLY_SOURCE_CONSISTENCY_PATCH":
            raise FrozenVenueSplitAuthorityError(
                f"{decision_id}: unsupported source-consistency decision"
            )
        patch = item.get("source_patch", {})
        if not isinstance(patch, dict) or not patch or set(patch) - {
            "team_score",
            "opponent_score",
            "played_result",
        }:
            raise FrozenVenueSplitAuthorityError(
                f"{decision_id}: invalid sealed source-consistency patch"
            )
        expected_state = item.get("source_consistency_expected", {})
        if not isinstance(expected_state, dict):
            raise FrozenVenueSplitAuthorityError(
                f"{decision_id}: invalid source-consistency expected state"
            )
        projected = {
            "team_score": str(expected_state.get("team_score", "")),
            "opponent_score": str(expected_state.get("opponent_score", "")),
            "played_result": str(expected_state.get("played_result", "")),
        }
        projected.update({field: str(value) for field, value in patch.items()})
        try:
            team_number = int(projected["team_score"])
            opponent_number = int(projected["opponent_score"])
        except ValueError as exc:
            raise FrozenVenueSplitAuthorityError(
                f"{decision_id}: source-consistency score is not integer"
            ) from exc
        implied = (
            "W"
            if team_number > opponent_number
            else "L"
            if opponent_number > team_number
            else "T"
        )
        if projected["played_result"].strip().upper() != implied:
            raise FrozenVenueSplitAuthorityError(
                f"{decision_id}: source-consistency patch remains contradictory"
            )
        apply_exact_patch(item, patch)

    return result


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _snapshot_sha256(snapshot: dict[str, Any]) -> str:
    payload = json.dumps(
        snapshot,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _current_snapshot_from_template(
    source_games_path: Path,
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    fields = snapshot.get("fields")
    rows = snapshot.get("rows")
    if (
        snapshot.get("schema_version") != 1
        or not isinstance(fields, list)
        or any(not isinstance(field, str) or not field for field in fields)
        or not isinstance(rows, dict)
    ):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority lacks semantic guard"
        )
    if not source_games_path.is_file():
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority does not match current source semantics"
        )

    with source_games_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if "source_game_id" not in set(reader.fieldnames or []):
            raise FrozenVenueSplitAuthorityError(
                "Integration Freeze venue split authority does not match current source semantics"
            )
        current_rows: dict[str, dict[str, str]] = {}
        for row in reader:
            source_id = row.get("source_game_id", "").strip()
            if not source_id or source_id in current_rows:
                raise FrozenVenueSplitAuthorityError(
                    "Integration Freeze venue split authority does not match current source semantics"
                )
            current_rows[source_id] = {
                field: row.get(field, "")
                for field in fields
            }

    return {
        "schema_version": 1,
        "fields": list(fields),
        "rows": current_rows,
    }


def _semantic_snapshot_matches_allowed_delta(
    baseline: dict[str, Any],
    current: dict[str, Any],
    allowed_delta: dict[str, dict[str, str]] | None,
) -> bool:
    """Require current semantics to equal baseline plus exactly the sealed delta."""

    if (
        baseline.get("schema_version") != current.get("schema_version")
        or baseline.get("fields") != current.get("fields")
    ):
        return False
    fields = baseline.get("fields")
    baseline_rows = baseline.get("rows")
    current_rows = current.get("rows")
    if (
        not isinstance(fields, list)
        or not isinstance(baseline_rows, dict)
        or not isinstance(current_rows, dict)
        or set(baseline_rows) != set(current_rows)
    ):
        return False

    delta = allowed_delta or {}
    for source_id, patch in delta.items():
        if source_id not in baseline_rows or not isinstance(patch, dict):
            return False
        if any(
            field not in fields or field not in PRE_INGEST_SEMANTIC_FIELDS
            for field in patch
        ):
            return False

    for source_id, baseline_row in baseline_rows.items():
        current_row = current_rows.get(source_id)
        if not isinstance(baseline_row, dict) or not isinstance(current_row, dict):
            return False
        patch = delta.get(source_id, {})
        for field in fields:
            expected = patch.get(field, baseline_row.get(field, ""))
            if current_row.get(field, "") != expected:
                return False
    return True


def authenticated_frozen_venue_split_authority(
    repo: Path,
    school_key: str,
    *,
    allowed_semantic_delta: dict[str, dict[str, str]] | None = None,
) -> tuple[dict[str, dict[str, str]], bytes | None]:
    """Return exact frozen split assignments and their authenticated manifest bytes.

    A missing Integration Freeze is equivalent to no split authority. If a manifest
    exists, all trust invariants used by Stage 2 planning must pass before any
    authority is returned or transported into a disposable runtime copy.
    """

    manifest_path = repo / ".onboarding" / school_key / "integration-freeze.json"
    if not manifest_path.is_file():
        return {}, None

    try:
        payload = manifest_path.read_bytes()
        manifest = json.loads(payload)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FrozenVenueSplitAuthorityError(
            "cannot read Integration Freeze venue split authority"
        ) from exc

    if not isinstance(manifest, dict):
        raise FrozenVenueSplitAuthorityError(
            "cannot read Integration Freeze venue split authority"
        )

    reconciliation = manifest.get("venue_reconciliation")
    mappings = (
        reconciliation.get("mappings")
        if isinstance(reconciliation, dict)
        else None
    )
    split_mappings = (
        [
            mapping
            for mapping in mappings
            if isinstance(mapping, dict)
            and mapping.get("action") == "SPLIT_LOCAL_ROW_BY_CUTOVER"
        ]
        if isinstance(mappings, list)
        else []
    )
    if not split_mappings:
        return {}, payload

    if (
        manifest.get("status") != "INTEGRATION_FROZEN"
        or manifest.get("school_key") != school_key
    ):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority identity mismatch"
        )

    guard = manifest.get("source_game_semantic_guard")
    if not isinstance(guard, dict) or not isinstance(guard.get("snapshot"), dict):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority lacks semantic guard"
        )
    snapshot = guard["snapshot"]
    expected_semantic_hash = str(guard.get("snapshot_sha256", "")).strip()
    current_snapshot = _current_snapshot_from_template(
        repo / "schools" / school_key / "source-games.csv",
        snapshot,
    )
    if (
        not expected_semantic_hash
        or _snapshot_sha256(snapshot) != expected_semantic_hash
        or not _semantic_snapshot_matches_allowed_delta(
            snapshot,
            current_snapshot,
            allowed_semantic_delta,
        )
    ):
        suffix = (
            " outside the exact sealed pre-ingest semantic delta"
            if allowed_semantic_delta
            else ""
        )
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority does not match current "
            f"source semantics{suffix}"
        )

    package_hashes = manifest.get("package_member_sha256")
    expected_venues_hash = (
        str(package_hashes.get("venues.csv", "")).strip()
        if isinstance(package_hashes, dict)
        else ""
    )
    venues_path = repo / "schools" / school_key / "venues.csv"
    if (
        not re.fullmatch(r"[0-9a-f]{64}", expected_venues_hash)
        or not venues_path.is_file()
        or _sha256_file(venues_path) != expected_venues_hash
    ):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze venue split authority does not match current venues.csv"
        )

    snapshot_rows = snapshot.get("rows")
    if not isinstance(snapshot_rows, dict):
        raise FrozenVenueSplitAuthorityError(
            "Integration Freeze semantic snapshot rows are invalid"
        )

    authority: dict[str, dict[str, str]] = {}
    for mapping in mappings:
        if not isinstance(mapping, dict):
            raise FrozenVenueSplitAuthorityError(
                "Integration Freeze venue reconciliation row is invalid"
            )
        if mapping.get("action") != "SPLIT_LOCAL_ROW_BY_CUTOVER":
            continue

        venue_name = str(mapping.get("expected_local_name", "")).strip()
        targets = mapping.get("split_targets")
        if not venue_name or not isinstance(targets, list) or not targets:
            raise FrozenVenueSplitAuthorityError(
                "frozen venue cutover split is incomplete"
            )

        assigned_count = 0
        for target in targets:
            if not isinstance(target, dict):
                raise FrozenVenueSplitAuthorityError(
                    "frozen venue cutover target is invalid"
                )
            venue_id = str(target.get("global_venue_id", "")).strip()
            venue_key = str(target.get("global_venue_key", "")).strip()
            source_ids = target.get("source_game_ids")
            if not venue_id or not venue_key or not isinstance(source_ids, list):
                raise FrozenVenueSplitAuthorityError(
                    "frozen venue cutover target is incomplete"
                )

            clean_ids = [str(value).strip() for value in source_ids]
            if (
                any(not value for value in clean_ids)
                or len(set(clean_ids)) != len(clean_ids)
            ):
                raise FrozenVenueSplitAuthorityError(
                    "frozen venue cutover source-game population is invalid"
                )
            declared = str(target.get("games_currently_assigned", "")).strip()
            if not declared.isdigit() or int(declared) != len(clean_ids):
                raise FrozenVenueSplitAuthorityError(
                    "frozen venue cutover target count mismatch"
                )

            for source_id in clean_ids:
                semantic_row = snapshot_rows.get(source_id)
                if not isinstance(semantic_row, dict):
                    raise FrozenVenueSplitAuthorityError(
                        f"frozen venue cutover references unknown source game {source_id}"
                    )
                if (
                    str(semantic_row.get("curated_venue_name", "")).strip().casefold()
                    != venue_name.casefold()
                ):
                    raise FrozenVenueSplitAuthorityError(
                        f"frozen venue cutover source game {source_id} has a different venue"
                    )
                entry = {
                    "venue_id": venue_id,
                    "venue_key": venue_key,
                    "curated_venue_name": venue_name,
                }
                prior = authority.get(source_id)
                if prior is not None and prior != entry:
                    raise FrozenVenueSplitAuthorityError(
                        f"frozen venue cutover assigns source game {source_id} more than once"
                    )
                authority[source_id] = entry
            assigned_count += len(clean_ids)

        declared_total = str(mapping.get("split_source_game_count", "")).strip()
        if not declared_total.isdigit() or int(declared_total) != assigned_count:
            raise FrozenVenueSplitAuthorityError(
                "frozen venue cutover total count mismatch"
            )

    return authority, payload


def load_frozen_venue_split_authority(
    repo: Path,
    school_key: str,
    *,
    allowed_semantic_delta: dict[str, dict[str, str]] | None = None,
) -> dict[str, dict[str, str]]:
    """Return only authenticated per-game split assignments."""

    authority, _ = authenticated_frozen_venue_split_authority(
        repo,
        school_key,
        allowed_semantic_delta=allowed_semantic_delta,
    )
    return authority


def frozen_venue_split_freeze_bytes(
    repo: Path,
    school_key: str,
    *,
    allowed_semantic_delta: dict[str, dict[str, str]] | None = None,
) -> bytes | None:
    """Return manifest bytes only when their split authority remains authenticated."""

    authority, payload = authenticated_frozen_venue_split_authority(
        repo,
        school_key,
        allowed_semantic_delta=allowed_semantic_delta,
    )
    return payload if authority else None
