"""Explicit, immutable-input-bounded venue reuse for Implementation Stage 1.

A spec only authorizes current-main representation reconciliation; it never
changes global registries or the frozen six-file research portfolio.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from typing import Any

from onboarding_plan import WorkflowError
from venue_geography import normalize_jurisdiction


_ROW_SELECTOR_PREFIX = "__row_index__:"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _row_selector(index: int) -> str:
    return f"{_ROW_SELECTOR_PREFIX}{index}"


def _normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").casefold())


def _csv_rows(data: bytes) -> list[dict[str, str]]:
    return list(
        csv.DictReader(
            io.StringIO(data.decode("utf-8-sig"), newline="")
        )
    )


def _season_window(value: str) -> tuple[dt.date, dt.date] | None:
    match = re.fullmatch(r"(\d{4})-(\d{4})", (value or "").strip())
    if not match or int(match.group(2)) != int(match.group(1)) + 1:
        return None
    return (
        dt.date(int(match.group(1)), 7, 1),
        dt.date(int(match.group(2)), 6, 30),
    )


def _game_summary(rows: list[dict[str, str]]) -> dict[str, str]:
    dates = [row.get("game_date", "").strip() for row in rows]
    exact = [value for value in dates if value]
    return {
        "games_currently_assigned": str(len(rows)),
        "first_assigned_game": (
            min(exact) if rows and len(exact) == len(rows) else ""
        ),
        "last_assigned_game": (
            max(exact) if rows and len(exact) == len(rows) else ""
        ),
    }


def _matching_source_games(
    source_games: list[dict[str, str]],
    local: dict[str, str],
) -> list[dict[str, str]]:
    labels = {_normalize_name(local.get("canonical_name", ""))}
    labels.update(
        _normalize_name(alias)
        for alias in local.get("aliases", "").split(";")
        if alias.strip()
    )
    labels.discard("")
    city = local.get("city", "").strip().casefold()
    state = normalize_jurisdiction(local.get("state", ""))
    return [
        row
        for row in source_games
        if _normalize_name(row.get("curated_venue_name", "")) in labels
        and row.get("city", "").strip().casefold() == city
        and normalize_jurisdiction(row.get("state", "")) == state
    ]


def explicit_reuse_locality_compatible(
    local: dict[str, str],
    global_row: dict[str, str],
    mapping: dict[str, Any],
) -> bool:
    """Return whether an explicit reuse may canonicalize a locality variant.

    Exact geography remains the default. Schema-v2 explicit reconciliation may
    opt into a documented representation-only locality variant only when the
    exact current-main venue ID/key has already been authenticated and at least
    one populated locality axis independently agrees. Frozen source-game
    geography is never changed by this predicate.
    """
    local_city = local.get("city", "").strip()
    local_state = local.get("state", "").strip()
    global_city = global_row.get("city", "").strip()
    global_state = global_row.get("state", "").strip()

    if (
        local_city.casefold() == global_city.casefold()
        and normalize_jurisdiction(local_state) == normalize_jurisdiction(global_state)
    ):
        return True

    if not mapping.get("allow_locality_variant"):
        return False
    if not mapping.get("locality_variant_basis", "").strip():
        return False
    if not all((local_city, local_state, global_city, global_state)):
        return False

    return (
        local_city.casefold() == global_city.casefold()
        or normalize_jurisdiction(local_state) == normalize_jurisdiction(global_state)
    )


def representation_consolidation_conflicts(
    local: dict[str, str],
    retained_rows: list[dict[str, str]],
) -> list[str]:
    """Return semantic reasons a blank representation row may not consolidate."""
    conflicts: list[str] = []
    if any(
        local.get(field, "").strip()
        for field in (
            "relationship_type",
            "relationship_start",
            "relationship_end",
            "relationship_date_precision",
        )
    ):
        conflicts.append("RELATIONSHIP_AUTHORITY_PRESENT")

    for field in (
        "site_rule",
        "source_basis",
        "notes",
        "venue_type",
        "known_opened",
        "known_closed",
        "venue_date_precision",
    ):
        value = local.get(field, "").strip()
        if value and any(
            retained.get(field, "").strip() != value
            for retained in retained_rows
        ):
            conflicts.append(f"UNIQUE_{field.upper()}_AUTHORITY")

    aliases = {
        value.strip().casefold()
        for value in local.get("aliases", "").split(";")
        if value.strip()
    }
    retained_labels = set()
    for retained in retained_rows:
        canonical = retained.get("canonical_name", "").strip()
        if canonical:
            retained_labels.add(canonical.casefold())
        retained_labels.update(
            value.strip().casefold()
            for value in retained.get("aliases", "").split(";")
            if value.strip()
        )
    if not aliases.issubset(retained_labels):
        conflicts.append("UNIQUE_ALIASES")
    return conflicts


def venue_reconciliation_for_row(
    mappings: dict[str, dict[str, Any]],
    local: dict[str, str],
    row_index: int,
) -> dict[str, Any] | None:
    """Return explicit reconciliation for one frozen venues.csv row.

    Legacy schema-v1 mappings remain keyed by nonblank local venue_key.
    Schema-v2 may instead bind one exact immutable venues.csv data-row index.
    """
    key = local.get("venue_key", "").strip()
    if key and key in mappings:
        return mappings[key]
    return mappings.get(_row_selector(row_index))


def load_venue_reconciliation(
    path: Path | None,
    *,
    school_key: str,
    package_path: Path | None,
    local_venues: list[dict[str, str]],
    global_venues: list[dict[str, str]],
    expected_package_sha256: str | None = None,
    frozen_venues_bytes: bytes | None = None,
    source_games_bytes: bytes | None = None,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any] | None]:
    """Validate an explicit identity map and return mappings + durable provenance.

    Both the entire transport ZIP identity and its exact frozen venues.csv
    representation are hash-bound, so no operator instruction can apply to
    changed Research authority. Ordinary onboarding reads both directly from
    the package ZIP; callers with a different immutable package shape may pass
    the already-authenticated package SHA plus deterministic frozen venues bytes.
    Geography and exact ID/key must agree with current main.

    Schema v2 adds row-index selectors for blank-key representation rows, a
    narrowly guarded DROP_REDUNDANT_LOCAL_ROW action, and documented
    locality-variant reuse for either key-bound or row-index-bound identities.
    """
    if path is None:
        return {}, None
    path = path.resolve()
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise WorkflowError(f"cannot read venue reconciliation {path}: {exc}") from exc
    if not isinstance(doc, dict):
        raise WorkflowError("venue reconciliation document must be an object")
    schema_version = doc.get("schema_version")
    if schema_version not in {1, 2}:
        raise WorkflowError("venue reconciliation schema_version must be 1 or 2")
    if doc.get("school_key") != school_key:
        raise WorkflowError("venue reconciliation school_key mismatch")
    approval = str(doc.get("owner_approval_basis") or "").strip()
    if not approval:
        raise WorkflowError("venue reconciliation requires owner_approval_basis")
    expected_package = str(doc.get("expected_research_zip_sha256") or "").lower().strip()
    if package_path is not None:
        actual_package = _sha256_file(package_path)
    else:
        actual_package = str(expected_package_sha256 or "").lower().strip()
        if not re.fullmatch(r"[0-9a-f]{64}", actual_package):
            raise WorkflowError(
                "venue reconciliation requires authenticated package SHA-256"
            )
    if expected_package != actual_package:
        raise WorkflowError("venue reconciliation frozen package SHA-256 mismatch")
    if frozen_venues_bytes is None:
        if package_path is None:
            raise WorkflowError(
                "venue reconciliation requires frozen venues.csv bytes"
            )
        try:
            with zipfile.ZipFile(package_path) as archive:
                member = archive.read("venues.csv")
                source_games_member = (
                    archive.read("source-games.csv")
                    if "source-games.csv" in archive.namelist()
                    else b""
                )
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
            raise WorkflowError(
                f"venue reconciliation cannot read frozen package members: {exc}"
            ) from exc
    else:
        member = frozen_venues_bytes
        source_games_member = source_games_bytes or b""
    source_games = (
        _csv_rows(source_games_member)
        if source_games_member
        else []
    )
    expected_venues = str(doc.get("expected_venues_sha256") or "").lower().strip()
    actual_venues = _sha256_bytes(member)
    if expected_venues != actual_venues:
        raise WorkflowError("venue reconciliation frozen venues.csv SHA-256 mismatch")

    raw_mappings = doc.get("mappings")
    if not isinstance(raw_mappings, list) or not raw_mappings:
        raise WorkflowError("venue reconciliation requires nonempty mappings")

    local_by_key: dict[str, list[dict[str, str]]] = {}
    for row in local_venues:
        key = row.get("venue_key", "").strip()
        local_by_key.setdefault(key, []).append(row)
    global_by_id = {
        row.get("venue_id", "").strip(): row for row in global_venues
    }
    global_by_key = {
        row.get("venue_key", "").strip(): row for row in global_venues
    }

    mappings: dict[str, dict[str, Any]] = {}
    new_identity_specs: dict[str, tuple[str, str, str]] = {}
    for number, raw in enumerate(raw_mappings, 1):
        if not isinstance(raw, dict):
            raise WorkflowError(f"venue reconciliation mapping {number} not an object")

        action = str(raw.get("action") or "REUSE_CURRENT_IDENTITY").strip().upper()
        local_key = str(raw.get("local_venue_key") or "").strip()
        raw_row_index = raw.get("local_venue_row_index")
        has_row_index = (
            raw_row_index is not None and str(raw_row_index).strip() != ""
        )
        if schema_version == 1 and has_row_index:
            raise WorkflowError(
                "venue reconciliation schema_version 1 does not support local_venue_row_index"
            )
        if bool(local_key) == bool(has_row_index):
            raise WorkflowError(
                f"venue reconciliation mapping {number} requires exactly one "
                "local_venue_key or local_venue_row_index"
            )

        row_index: int | None = None
        if has_row_index:
            try:
                row_index = int(str(raw_row_index))
            except (TypeError, ValueError) as exc:
                raise WorkflowError(
                    f"venue reconciliation mapping {number} local_venue_row_index invalid"
                ) from exc
            if row_index < 1 or row_index > len(local_venues):
                raise WorkflowError(
                    f"venue reconciliation mapping {number} local_venue_row_index out of range"
                )
            selector = _row_selector(row_index)
            local_rows = [local_venues[row_index - 1]]
            if local_rows[0].get("venue_key", "").strip():
                raise WorkflowError(
                    "local_venue_row_index is limited to blank-key frozen rows"
                )
        else:
            selector = local_key
            local_rows = local_by_key.get(local_key) or []
            if not local_rows:
                raise WorkflowError(
                    f"venue reconciliation unknown local key {local_key!r}"
                )

        if selector in mappings:
            if local_key:
                raise WorkflowError(
                    f"venue reconciliation repeats local key {local_key!r}"
                )
            raise WorkflowError(
                f"venue reconciliation repeats local selector {selector!r}"
            )

        common_required = (
            "expected_local_name",
            "expected_local_city",
            "expected_local_state",
            "resolution_basis",
        )
        item = {
            "action": action,
            "local_venue_key": local_key,
            "local_venue_row_index": str(row_index or ""),
            **{
                key: str(raw.get(key) or "").strip()
                for key in common_required
            },
        }
        if not all(item[key] for key in common_required):
            raise WorkflowError(
                f"venue reconciliation mapping {number} missing required field"
            )

        if any(
            local.get("source_program_key", "").strip() != school_key
            for local in local_rows
        ):
            raise WorkflowError(
                f"venue reconciliation school mismatch for {selector!r}"
            )
        local_names = {
            local.get("canonical_name", "").strip() for local in local_rows
        }
        if (
            item["expected_local_name"] not in local_names
            or any(
                local.get("city", "").strip() != item["expected_local_city"]
                or local.get("state", "").strip() != item["expected_local_state"]
                for local in local_rows
            )
        ):
            raise WorkflowError(
                f"venue reconciliation frozen local identity drift for {selector!r}"
            )

        if action == "REGISTER_NEW_IDENTITY":
            if row_index is None:
                raise WorkflowError(
                    "REGISTER_NEW_IDENTITY requires local_venue_row_index"
                )
            local = local_rows[0]
            if local.get("venue_key", "").strip():
                raise WorkflowError(
                    "REGISTER_NEW_IDENTITY is limited to blank-key frozen rows"
                )
            new_key = str(raw.get("new_global_venue_key") or "").strip()
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", new_key):
                raise WorkflowError(
                    "REGISTER_NEW_IDENTITY requires a normalized new_global_venue_key"
                )
            if new_key in global_by_key:
                raise WorkflowError(
                    f"REGISTER_NEW_IDENTITY key already exists on current main: {new_key}"
                )
            identity = (
                item["expected_local_name"],
                item["expected_local_city"],
                item["expected_local_state"],
            )
            prior = new_identity_specs.get(new_key)
            if prior is not None and prior != identity:
                raise WorkflowError(
                    "REGISTER_NEW_IDENTITY repeats a proposed key for a "
                    "different frozen physical identity"
                )
            new_identity_specs[new_key] = identity
            item["new_global_venue_key"] = new_key
            mappings[selector] = item
            continue

        if action == "SPLIT_LOCAL_ROW_BY_CUTOVER":
            if row_index is None:
                raise WorkflowError(
                    "SPLIT_LOCAL_ROW_BY_CUTOVER requires local_venue_row_index"
                )
            local = local_rows[0]
            if local.get("venue_key", "").strip():
                raise WorkflowError(
                    "SPLIT_LOCAL_ROW_BY_CUTOVER is limited to blank-key frozen rows"
                )
            if any(
                local.get(field, "").strip()
                for field in (
                    "relationship_type",
                    "relationship_start",
                    "relationship_end",
                    "relationship_date_precision",
                )
            ):
                raise WorkflowError(
                    "SPLIT_LOCAL_ROW_BY_CUTOVER cannot discard venue relationship authority"
                )

            cutover_text = str(raw.get("cutover_date") or "").strip()
            try:
                cutover = dt.date.fromisoformat(cutover_text)
            except ValueError as exc:
                raise WorkflowError(
                    "SPLIT_LOCAL_ROW_BY_CUTOVER requires exact ISO cutover_date"
                ) from exc
            cutover_basis = str(raw.get("cutover_basis") or "").strip()
            if not cutover_basis:
                raise WorkflowError(
                    "SPLIT_LOCAL_ROW_BY_CUTOVER requires cutover_basis"
                )

            target_specs = []
            for side in ("before", "after"):
                target_id = str(
                    raw.get(f"{side}_global_venue_id") or ""
                ).strip()
                target_key = str(
                    raw.get(f"{side}_global_venue_key") or ""
                ).strip()
                if not target_id or not target_key:
                    raise WorkflowError(
                        "SPLIT_LOCAL_ROW_BY_CUTOVER requires before/after "
                        "global venue ID and key"
                    )
                target = global_by_id.get(target_id)
                if (
                    target is None
                    or target.get("venue_key", "").strip() != target_key
                    or global_by_key.get(target_key) is not target
                ):
                    raise WorkflowError(
                        "SPLIT_LOCAL_ROW_BY_CUTOVER target no longer matches current main"
                    )
                if (
                    target.get("city", "").strip().casefold()
                    != item["expected_local_city"].casefold()
                    or normalize_jurisdiction(target.get("state", ""))
                    != normalize_jurisdiction(item["expected_local_state"])
                ):
                    raise WorkflowError(
                        "SPLIT_LOCAL_ROW_BY_CUTOVER target geography mismatch"
                    )
                retained = [
                    other
                    for index, other in enumerate(local_venues, 1)
                    if index != row_index
                    and other.get("venue_key", "").strip() == target_key
                    and other.get("canonical_name", "").strip()
                    == item["expected_local_name"]
                    and other.get("city", "").strip()
                    == item["expected_local_city"]
                    and other.get("state", "").strip()
                    == item["expected_local_state"]
                ]
                if len(retained) != 1:
                    raise WorkflowError(
                        "SPLIT_LOCAL_ROW_BY_CUTOVER requires exactly one retained "
                        f"frozen row for target key {target_key!r}"
                    )
                target_specs.append((side, target_id, target_key, retained[0]))

            if target_specs[0][1] == target_specs[1][1]:
                raise WorkflowError(
                    "SPLIT_LOCAL_ROW_BY_CUTOVER requires two distinct physical targets"
                )

            exact_preservation_fields = (
                "site_rule",
                "source_basis",
                "notes",
                "venue_type",
                "known_opened",
                "known_closed",
                "venue_date_precision",
            )
            for field in exact_preservation_fields:
                value = local.get(field, "").strip()
                if value and any(
                    retained.get(field, "").strip() != value
                    for _, _, _, retained in target_specs
                ):
                    raise WorkflowError(
                        "SPLIT_LOCAL_ROW_BY_CUTOVER cannot discard unique frozen "
                        f"{field} authority"
                    )

            local_aliases = {
                value.strip().casefold()
                for value in local.get("aliases", "").split(";")
                if value.strip()
            }
            retained_labels = set()
            for _, _, _, retained in target_specs:
                canonical = retained.get("canonical_name", "").strip()
                if canonical:
                    retained_labels.add(canonical.casefold())
                retained_labels.update(
                    value.strip().casefold()
                    for value in retained.get("aliases", "").split(";")
                    if value.strip()
                )
            if not local_aliases.issubset(retained_labels):
                raise WorkflowError(
                    "SPLIT_LOCAL_ROW_BY_CUTOVER cannot discard unique frozen aliases"
                )

            matching_games = _matching_source_games(source_games, local)
            if not matching_games:
                raise WorkflowError(
                    "SPLIT_LOCAL_ROW_BY_CUTOVER found no matching frozen source games"
                )
            before_games: list[dict[str, str]] = []
            after_games: list[dict[str, str]] = []
            for game in matching_games:
                game_id = game.get("source_game_id", "").strip() or "[unknown]"
                game_date_text = game.get("game_date", "").strip()
                if game_date_text:
                    try:
                        game_date = dt.date.fromisoformat(game_date_text)
                    except ValueError as exc:
                        raise WorkflowError(
                            "SPLIT_LOCAL_ROW_BY_CUTOVER encountered invalid exact "
                            f"date for {game_id}: {game_date_text!r}"
                        ) from exc
                    (before_games if game_date < cutover else after_games).append(game)
                    continue

                season = _season_window(game.get("season_label", ""))
                if season is None:
                    raise WorkflowError(
                        "SPLIT_LOCAL_ROW_BY_CUTOVER cannot classify undated game "
                        f"{game_id} with invalid season"
                    )
                if season[1] < cutover:
                    before_games.append(game)
                elif season[0] >= cutover:
                    after_games.append(game)
                else:
                    raise WorkflowError(
                        "SPLIT_LOCAL_ROW_BY_CUTOVER transition-season game lacks "
                        f"an exact date: {game_id}"
                    )

            if not before_games or not after_games:
                raise WorkflowError(
                    "SPLIT_LOCAL_ROW_BY_CUTOVER requires populated assignments "
                    "on both sides of the cutover"
                )

            split_targets = []
            for (side, target_id, target_key, _), rows in zip(
                target_specs, (before_games, after_games)
            ):
                source_game_ids = sorted(
                    row.get("source_game_id", "").strip()
                    for row in rows
                )
                split_targets.append(
                    {
                        "side": side.upper(),
                        "global_venue_id": target_id,
                        "global_venue_key": target_key,
                        **_game_summary(rows),
                        "source_game_ids": source_game_ids,
                        "source_game_ids_sha256": _sha256_bytes(
                            ("\n".join(source_game_ids) + "\n").encode("utf-8")
                        ),
                    }
                )

            item.update(
                {
                    "cutover_date": cutover_text,
                    "cutover_basis": cutover_basis,
                    "split_source_game_count": str(len(matching_games)),
                    "split_targets": split_targets,
                }
            )
            mappings[selector] = item
            continue

        if action == "DROP_REDUNDANT_LOCAL_ROW":
            if row_index is None:
                raise WorkflowError(
                    "DROP_REDUNDANT_LOCAL_ROW requires local_venue_row_index"
                )
            local = local_rows[0]
            if local.get("venue_key", "").strip():
                raise WorkflowError(
                    "DROP_REDUNDANT_LOCAL_ROW is limited to blank-key frozen rows"
                )
            protected_relationship_fields = (
                "relationship_type",
                "relationship_start",
                "relationship_end",
                "relationship_date_precision",
            )
            if any(
                local.get(field, "").strip()
                for field in protected_relationship_fields
            ):
                raise WorkflowError(
                    "DROP_REDUNDANT_LOCAL_ROW cannot discard venue relationship authority"
                )
            retained = [
                other
                for index, other in enumerate(local_venues, 1)
                if index != row_index
                and other.get("venue_key", "").strip()
                and other.get("canonical_name", "").strip()
                == item["expected_local_name"]
                and other.get("city", "").strip()
                == item["expected_local_city"]
                and other.get("state", "").strip()
                == item["expected_local_state"]
            ]
            if not retained:
                raise WorkflowError(
                    "DROP_REDUNDANT_LOCAL_ROW requires a retained keyed row "
                    "with the same frozen name/geography"
                )

            # A blank-key aggregate representation may be dropped only when all
            # non-relationship authority it carries is provably preserved by the
            # retained keyed rows. This is deliberately stricter than ordinary
            # same-name/geography matching.
            exact_redundancy_fields = (
                "site_rule",
                "source_basis",
                "notes",
                "venue_type",
                "known_opened",
                "known_closed",
                "venue_date_precision",
            )
            for field in exact_redundancy_fields:
                local_value = local.get(field, "").strip()
                if local_value and any(
                    other.get(field, "").strip() != local_value
                    for other in retained
                ):
                    raise WorkflowError(
                        "DROP_REDUNDANT_LOCAL_ROW cannot discard unique frozen "
                        f"{field} authority"
                    )

            local_aliases = {
                value.strip().casefold()
                for value in local.get("aliases", "").split(";")
                if value.strip()
            }
            retained_names = {
                row.get("canonical_name", "").strip().casefold()
                for row in retained
                if row.get("canonical_name", "").strip()
            }
            for row in retained:
                retained_names.update(
                    value.strip().casefold()
                    for value in row.get("aliases", "").split(";")
                    if value.strip()
                )
            if not local_aliases.issubset(retained_names):
                raise WorkflowError(
                    "DROP_REDUNDANT_LOCAL_ROW cannot discard unique frozen aliases"
                )

            local_count = local.get("games_currently_assigned", "").strip()
            if local_count:
                try:
                    local_count_int = int(local_count)
                    retained_counts = [
                        int(other.get("games_currently_assigned", "").strip())
                        for other in retained
                    ]
                except ValueError as exc:
                    raise WorkflowError(
                        "DROP_REDUNDANT_LOCAL_ROW requires numeric assignment counts"
                    ) from exc
                if sum(retained_counts) != local_count_int:
                    raise WorkflowError(
                        "DROP_REDUNDANT_LOCAL_ROW retained assignment counts "
                        "do not exactly partition the dropped row"
                    )
                item["dropped_games_currently_assigned"] = str(local_count_int)
                item["retained_games_currently_assigned"] = str(
                    sum(retained_counts)
                )

            local_first = local.get("first_assigned_game", "").strip()
            if local_first:
                retained_first = [
                    other.get("first_assigned_game", "").strip()
                    for other in retained
                ]
                if any(not value for value in retained_first) or min(retained_first) > local_first:
                    raise WorkflowError(
                        "DROP_REDUNDANT_LOCAL_ROW retained rows do not cover "
                        "the dropped row first assignment"
                    )

            local_last = local.get("last_assigned_game", "").strip()
            if local_last:
                retained_last = [
                    other.get("last_assigned_game", "").strip()
                    for other in retained
                ]
                if any(not value for value in retained_last) or max(retained_last) < local_last:
                    raise WorkflowError(
                        "DROP_REDUNDANT_LOCAL_ROW retained rows do not cover "
                        "the dropped row last assignment"
                    )

            item["retained_local_keys"] = ";".join(
                sorted({row.get("venue_key", "").strip() for row in retained})
            )
            mappings[selector] = item
            continue

        if action != "REUSE_CURRENT_IDENTITY":
            raise WorkflowError(
                f"venue reconciliation mapping {number} unsupported action {action!r}"
            )

        target_required = (
            "global_venue_id",
            "global_venue_key",
            "expected_global_city",
            "expected_global_state",
        )
        item.update({
            key: str(raw.get(key) or "").strip()
            for key in target_required
        })
        if not all(item[key] for key in target_required):
            raise WorkflowError(
                f"venue reconciliation mapping {number} missing required field"
            )

        target_id = item["global_venue_id"]
        target = global_by_id.get(target_id)
        if (
            target is None
            or target.get("venue_key", "").strip() != item["global_venue_key"]
            or global_by_key.get(item["global_venue_key"]) is not target
        ):
            raise WorkflowError(
                f"venue reconciliation stale global venue ID/key for {selector!r}"
            )

        raw_allow_variant = raw.get("allow_locality_variant", False)
        if not isinstance(raw_allow_variant, bool):
            raise WorkflowError(
                "venue reconciliation allow_locality_variant must be boolean"
            )
        locality_variant_basis = str(
            raw.get("locality_variant_basis") or ""
        ).strip()
        if raw_allow_variant:
            if schema_version != 2:
                raise WorkflowError(
                    "allow_locality_variant requires schema-v2 reconciliation"
                )
            if not locality_variant_basis:
                raise WorkflowError(
                    "allow_locality_variant requires locality_variant_basis"
                )
        elif locality_variant_basis:
            raise WorkflowError(
                "locality_variant_basis requires allow_locality_variant=true"
            )
        item["allow_locality_variant"] = raw_allow_variant
        item["locality_variant_basis"] = locality_variant_basis

        if (
            target.get("city", "").strip() != item["expected_global_city"]
            or target.get("state", "").strip() != item["expected_global_state"]
        ):
            raise WorkflowError(
                f"venue reconciliation global geography mismatch for {selector!r}"
            )
        if not explicit_reuse_locality_compatible(local_rows[0], target, item):
            raise WorkflowError(
                f"venue reconciliation global geography mismatch for {selector!r}"
            )

        raw_preserve_local = raw.get("preserve_local_representation", False)
        if not isinstance(raw_preserve_local, bool):
            raise WorkflowError(
                "venue reconciliation preserve_local_representation must be boolean"
            )
        if raw_preserve_local:
            if schema_version != 2 or row_index is None:
                raise WorkflowError(
                    "preserve_local_representation requires schema-v2 "
                    "local_venue_row_index"
                )
            retained = [
                other
                for index, other in enumerate(local_venues, 1)
                if index != row_index
                and other.get("venue_key", "").strip()
                == item["global_venue_key"]
                and other.get("canonical_name", "").strip()
                == item["expected_local_name"]
                and explicit_reuse_locality_compatible(
                    local_rows[0], other, item
                )
            ]
            if not retained:
                raise WorkflowError(
                    "preserve_local_representation requires a retained keyed "
                    "row for the same authenticated physical venue"
                )
            conflicts = representation_consolidation_conflicts(
                local_rows[0], retained
            )
            if "RELATIONSHIP_AUTHORITY_PRESENT" not in conflicts:
                raise WorkflowError(
                    "preserve_local_representation is limited to frozen rows "
                    "carrying venue relationship authority"
                )
            item["preservation_conflicts"] = conflicts
        item["preserve_local_representation"] = raw_preserve_local

        mappings[selector] = item

    metadata = {
        "schema_version": schema_version,
        "spec_path": str(path),
        "spec_sha256": _sha256_file(path),
        "owner_approval_basis": approval,
        "research_zip_sha256": actual_package,
        "frozen_venues_sha256": actual_venues,
        "mappings": list(mappings.values()),
    }
    return mappings, metadata
