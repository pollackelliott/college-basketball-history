#!/usr/bin/env python3
"""Deterministic pre-publication history-scope supersession helpers.

This module does not publish refs. It derives one six-file candidate package from an
existing onboarding predecessor after an explicit owner/Control Center scope ruling.
The remote runner owns locking, current-main Phase 0 replay, write-ahead, CAS
publication, recovery, and fresh verification.
"""
from __future__ import annotations

import csv
import io
import json
import re
import tempfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from integration_freeze_guard import (
    build_source_game_semantic_snapshot,
    semantic_snapshot_sha256,
)
from remote_implementation_control import sha256_bytes
from remote_implementation_io import REQUIRED_PACKAGE_FILES, Stop

WORKFLOW_KIND = "PRE_PUBLICATION_SCOPE_SUPERSESSION"
SPEC_KIND = "REMOTE_IMPLEMENTATION_SCOPE_SUPERSESSION"
_SEASON = re.compile(r"^(\d{4})-(\d{2}|\d{4})$")
_SCOPE_SINGLE = re.compile(r"^(\d{4})-(\d{2})\+$")
_SCOPE_RANGE = re.compile(r"^(\d{4})-(\d{2})\.\.(\d{4})-(\d{2})$")


def _csv_rows(data: bytes) -> tuple[list[str], list[dict[str, str]]]:
    text = data.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    return list(reader.fieldnames or []), list(reader)


def _csv_bytes_like(
    original: bytes,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> bytes:
    has_bom = original.startswith(b"\xef\xbb\xbf")
    ending = "\r\n" if b"\r\n" in original else "\n"
    out = io.StringIO(newline="")
    writer = csv.DictWriter(
        out,
        fieldnames=fieldnames,
        lineterminator=ending,
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(rows)
    data = out.getvalue().encode("utf-8")
    return (b"\xef\xbb\xbf" + data) if has_bom else data


def _season_start(value: str) -> int:
    match = _SEASON.fullmatch(str(value or "").strip())
    if not match:
        raise Stop("SCOPE_SUPERSESSION_SEASON_INVALID:%s" % value)
    return int(match.group(1))


def _full_season(start: int) -> str:
    return f"{start:04d}-{start + 1:04d}"


def _compact_season(value: str) -> str:
    start = _season_start(value)
    return f"{start:04d}-{(start + 1) % 100:02d}"


def parse_scope_intervals(expression: str) -> list[tuple[int, int | None]]:
    text = str(expression or "").strip()
    if text == "INCEPTION+":
        return [(-10**9, None)]
    if not text:
        raise Stop("SCOPE_SUPERSESSION_SCOPE_EMPTY")
    intervals: list[tuple[int, int | None]] = []
    for raw in text.split("|"):
        part = raw.strip()
        match = _SCOPE_SINGLE.fullmatch(part)
        if match:
            intervals.append((int(match.group(1)), None))
            continue
        match = _SCOPE_RANGE.fullmatch(part)
        if match:
            start = int(match.group(1))
            end = int(match.group(3))
            if end < start:
                raise Stop("SCOPE_SUPERSESSION_SCOPE_RANGE_REVERSED")
            intervals.append((start, end))
            continue
        raise Stop("SCOPE_SUPERSESSION_SCOPE_INVALID:%s" % part)
    ordered = sorted(intervals)
    for index, (start, end) in enumerate(ordered[1:], start=1):
        prior_start, prior_end = ordered[index - 1]
        if prior_end is None or start <= prior_end:
            raise Stop("SCOPE_SUPERSESSION_SCOPE_INTERVAL_OVERLAP")
    return ordered


def season_in_scope(season_label: str, expression: str) -> bool:
    season = _season_start(season_label)
    return any(
        season >= start and (end is None or season <= end)
        for start, end in parse_scope_intervals(expression)
    )


def validate_scope_supersession_spec(
    spec: dict[str, Any],
    *,
    school_key: str,
) -> dict[str, Any]:
    if not isinstance(spec, dict):
        raise Stop("SCOPE_SUPERSESSION_SPEC_NOT_OBJECT")
    if spec.get("schema_version") != 1 or spec.get("kind") != SPEC_KIND:
        raise Stop("SCOPE_SUPERSESSION_SPEC_IDENTITY_INVALID")
    if spec.get("school_key") != school_key:
        raise Stop("SCOPE_SUPERSESSION_SPEC_SCHOOL_MISMATCH")
    for key in ("old_scope", "new_scope", "history_start_season", "authority_statement"):
        if not str(spec.get(key) or "").strip():
            raise Stop("SCOPE_SUPERSESSION_SPEC_FIELD_MISSING:%s" % key)
    parse_scope_intervals(str(spec["old_scope"]))
    parse_scope_intervals(str(spec["new_scope"]))
    _season_start(str(spec["history_start_season"]))

    ids = spec.get("excluded_source_game_ids")
    if (
        not isinstance(ids, list)
        or not ids
        or any(not isinstance(value, str) or not value.strip() for value in ids)
        or len(ids) != len(set(ids))
    ):
        raise Stop("SCOPE_SUPERSESSION_EXCLUDED_IDS_INVALID")

    before = spec.get("expected_source_game_count_before")
    after = spec.get("expected_source_game_count_after")
    if type(before) is not int or type(after) is not int or before <= after or after < 1:
        raise Stop("SCOPE_SUPERSESSION_EXPECTED_COUNTS_INVALID")
    if before - after != len(ids):
        raise Stop("SCOPE_SUPERSESSION_EXPECTED_COUNT_DELTA_MISMATCH")

    drops = spec.get("drop_school_venue_keys", [])
    if (
        not isinstance(drops, list)
        or any(not isinstance(value, str) or not value.strip() for value in drops)
        or len(drops) != len(set(drops))
    ):
        raise Stop("SCOPE_SUPERSESSION_DROP_VENUE_KEYS_INVALID")
    return spec


def _semantic_snapshot(data: bytes) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="scope-supersession-semantic-") as tmp:
        path = Path(tmp) / "source-games.csv"
        path.write_bytes(data)
        return build_source_game_semantic_snapshot(path)


def _regenerate_opponents(
    original: bytes,
    retained_games: list[dict[str, str]],
) -> tuple[bytes, dict[str, int]]:
    fields, rows = _csv_rows(original)
    labels: dict[str, list[dict[str, str]]] = defaultdict(list)
    for game in retained_games:
        labels[game.get("source_opponent_label", "")].append(game)

    source_rows: dict[str, dict[str, str]] = {}
    for row in rows:
        label = row.get("source_opponent_label", "")
        if label in source_rows:
            raise Stop("SCOPE_SUPERSESSION_DUPLICATE_OPPONENT_LABEL:%s" % label)
        source_rows[label] = row
    missing = sorted(set(labels) - set(source_rows))
    if missing:
        raise Stop(
            "SCOPE_SUPERSESSION_RETAINED_OPPONENT_LABEL_MISSING:"
            + ",".join(missing[:20])
        )

    output: list[dict[str, str]] = []
    removed = 0
    recounted = 0
    for row in rows:
        label = row.get("source_opponent_label", "")
        games = labels.get(label, [])
        if not games:
            removed += 1
            continue
        copy = dict(row)
        seasons = sorted({game.get("season_label", "") for game in games})
        if "games_with_source_label" in copy:
            copy["games_with_source_label"] = str(len(games))
        if "first_season" in copy:
            copy["first_season"] = _compact_season(seasons[0])
        if "last_season" in copy:
            copy["last_season"] = _compact_season(seasons[-1])
        if copy != row:
            recounted += 1
        output.append(copy)
    return _csv_bytes_like(original, fields, output), {
        "removed_rows": removed,
        "recounted_rows": recounted,
        "retained_rows": len(output),
    }


def _scope_overlap(
    row_start: int,
    row_end: int | None,
    scope: list[tuple[int, int | None]],
) -> list[tuple[int, int | None]]:
    overlaps: list[tuple[int, int | None]] = []
    for scope_start, scope_end in scope:
        start = max(row_start, scope_start)
        if row_end is None and scope_end is None:
            end = None
        elif row_end is None:
            end = scope_end
        elif scope_end is None:
            end = row_end
        else:
            end = min(row_end, scope_end)
        if end is None or start <= end:
            overlaps.append((start, end))
    return overlaps


def _clip_conferences(
    original: bytes,
    scope_expression: str,
) -> tuple[bytes, dict[str, int]]:
    fields, rows = _csv_rows(original)
    scope = parse_scope_intervals(scope_expression)
    output: list[dict[str, str]] = []
    removed = 0
    split_or_clipped = 0
    for row in rows:
        start = _season_start(row.get("start_season", ""))
        end_text = row.get("end_season", "").strip()
        end = _season_start(end_text) if end_text else None
        overlaps = _scope_overlap(start, end, scope)
        if not overlaps:
            removed += 1
            continue
        if len(overlaps) != 1 or overlaps[0] != (start, end):
            split_or_clipped += 1
        for overlap_start, overlap_end in overlaps:
            copy = dict(row)
            copy["start_season"] = _full_season(overlap_start)
            copy["end_season"] = (
                _full_season(overlap_end) if overlap_end is not None else ""
            )
            if "ongoing" in copy:
                copy["ongoing"] = (
                    "True"
                    if overlap_end is None
                    and str(row.get("ongoing", "")).strip().lower()
                    in {"true", "yes", "1"}
                    else "False"
                )
            output.append(copy)
    return _csv_bytes_like(original, fields, output), {
        "removed_rows": removed,
        "split_or_clipped_rows": split_or_clipped,
        "retained_rows": len(output),
    }


def _venue_names(row: dict[str, str]) -> set[str]:
    values = [row.get("canonical_name", "")]
    values.extend((row.get("aliases", "") or "").split(";"))
    return {value.strip().casefold() for value in values if value.strip()}


def _rebase_venues(
    original: bytes,
    current_main_venues: bytes,
    retained_games: list[dict[str, str]],
    *,
    drop_keys: list[str],
) -> tuple[bytes, dict[str, Any]]:
    fields, rows = _csv_rows(original)
    _, globals_ = _csv_rows(current_main_venues)
    main_by_key = {
        row.get("venue_key", "").strip(): row.get("venue_id", "").strip()
        for row in globals_
        if row.get("venue_key", "").strip()
    }
    drop = set(drop_keys)
    by_key = {row.get("venue_key", "").strip(): row for row in rows}
    missing = sorted(drop - set(by_key))
    if missing:
        raise Stop(
            "SCOPE_SUPERSESSION_DROP_VENUE_KEY_MISSING:" + ",".join(missing)
        )

    used_names = {
        value.strip().casefold()
        for game in retained_games
        for value in (
            game.get("source_venue_name", ""),
            game.get("curated_venue_name", ""),
        )
        if value.strip()
    }
    for key in sorted(drop):
        if _venue_names(by_key[key]) & used_names:
            raise Stop("SCOPE_SUPERSESSION_DROP_VENUE_STILL_USED:%s" % key)

    output: list[dict[str, str]] = []
    cleared_ids: list[str] = []
    rebound_ids: list[str] = []
    for row in rows:
        key = row.get("venue_key", "").strip()
        if key in drop:
            continue
        copy = dict(row)
        current = main_by_key.get(key)
        if current:
            if copy.get("venue_id", "").strip() != current:
                rebound_ids.append(key)
            copy["venue_id"] = current
        else:
            if copy.get("venue_id", "").strip():
                cleared_ids.append(key)
            copy["venue_id"] = ""
            if "notes" in copy:
                copy["notes"] = re.sub(
                    r"\s*Integration rebase resolved final global venue ID VEN-\d+\.",
                    "",
                    copy.get("notes", ""),
                ).strip()
        output.append(copy)
    return _csv_bytes_like(original, fields, output), {
        "dropped_keys": sorted(drop),
        "cleared_unregistered_ids": sorted(cleared_ids),
        "rebound_current_main_ids": sorted(rebound_ids),
        "retained_rows": len(output),
    }


def _replace_bullet(text: str, label: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^- {re.escape(label)}:.*$")
    return pattern.sub(f"- {label}: {value}", text)


def _scope_section(
    *,
    old_scope: str,
    new_scope: str,
    before_count: int,
    after_count: int,
    excluded_count: int,
) -> str:
    return (
        "## Publication scope supersession\n\n"
        f"- Original accepted Research scope: {old_scope}\n"
        f"- Owner-authorized public scope: {new_scope}\n"
        f"- Original Research competitive games preserved externally: {before_count:,}\n"
        f"- Excluded from public package by scope supersession: {excluded_count:,}\n"
        f"- Public-package competitive games: {after_count:,}\n"
        "- The immutable original Research Freeze remains preserved as audit evidence; "
        "excluded rows are not publication authority.\n\n"
    )


def _update_notes(
    original: bytes,
    *,
    spec: dict[str, Any],
    retained_games: list[dict[str, str]],
    source_notes: bool,
) -> bytes:
    has_bom = original.startswith(b"\xef\xbb\xbf")
    text = original.decode("utf-8-sig")
    ending = "\r\n" if "\r\n" in text else "\n"
    text = text.replace("\r\n", "\n")
    section = _scope_section(
        old_scope=str(spec["old_scope"]),
        new_scope=str(spec["new_scope"]),
        before_count=int(spec["expected_source_game_count_before"]),
        after_count=int(spec["expected_source_game_count_after"]),
        excluded_count=len(spec["excluded_source_game_ids"]),
    )
    if "## Publication scope supersession" not in text:
        first_break = text.find("\n")
        if first_break >= 0:
            text = text[: first_break + 1] + "\n" + section + text[first_break + 1 :]
        else:
            text = text + "\n\n" + section

    text = _replace_bullet(
        text,
        "Primary-source historical results cutoff",
        str(spec["history_start_season"]),
    )
    if not source_notes:
        text = _replace_bullet(
            text,
            "Competitive games",
            f"{len(retained_games):,}",
        )
        game_counts = Counter(
            game.get("curated_game_type", "") for game in retained_games
        )
        for label in (
            "CONFERENCE_TOURNAMENT",
            "NCAA_TOURNAMENT",
            "NIT",
            "POSTSEASON",
            "REGULAR_SEASON",
        ):
            text = _replace_bullet(text, label, f"{game_counts.get(label, 0):,}")
        site_counts = Counter(
            game.get("curated_site_type", "") for game in retained_games
        )
        for label in ("NEUTRAL", "OPPONENT_HOME", "SOURCE_PROGRAM_HOME"):
            text = _replace_bullet(text, label, f"{site_counts.get(label, 0):,}")

    data = text.replace("\n", ending).encode("utf-8")
    return (b"\xef\xbb\xbf" + data) if has_bom else data


def build_scope_superseded_package(
    predecessor_members: dict[str, bytes],
    current_main_venues: bytes,
    spec: dict[str, Any],
    *,
    school_key: str,
) -> tuple[dict[str, bytes], dict[str, Any]]:
    validate_scope_supersession_spec(spec, school_key=school_key)
    missing = sorted(set(REQUIRED_PACKAGE_FILES) - set(predecessor_members))
    if missing:
        raise Stop(
            "SCOPE_SUPERSESSION_PREDECESSOR_MEMBER_MISSING:" + ",".join(missing)
        )

    source_original = predecessor_members["source-games.csv"]
    source_fields, source_rows = _csv_rows(source_original)
    if len(source_rows) != int(spec["expected_source_game_count_before"]):
        raise Stop("SCOPE_SUPERSESSION_SOURCE_COUNT_BEFORE_MISMATCH")
    ids = [row.get("source_game_id", "").strip() for row in source_rows]
    if not all(ids) or len(ids) != len(set(ids)):
        raise Stop("SCOPE_SUPERSESSION_SOURCE_IDS_INVALID")

    old_scope = str(spec["old_scope"])
    new_scope = str(spec["new_scope"])
    out_of_old = [
        row["source_game_id"]
        for row in source_rows
        if not season_in_scope(row.get("season_label", ""), old_scope)
    ]
    if out_of_old:
        raise Stop("SCOPE_SUPERSESSION_PREDECESSOR_OUTSIDE_OLD_SCOPE")

    retained = [
        row for row in source_rows
        if season_in_scope(row.get("season_label", ""), new_scope)
    ]
    derived_excluded = sorted(
        row["source_game_id"]
        for row in source_rows
        if not season_in_scope(row.get("season_label", ""), new_scope)
    )
    expected_excluded = sorted(spec["excluded_source_game_ids"])
    if derived_excluded != expected_excluded:
        raise Stop("SCOPE_SUPERSESSION_EXCLUDED_ID_SET_MISMATCH")
    if len(retained) != int(spec["expected_source_game_count_after"]):
        raise Stop("SCOPE_SUPERSESSION_SOURCE_COUNT_AFTER_MISMATCH")

    source_candidate = _csv_bytes_like(source_original, source_fields, retained)
    predecessor_retained = _csv_bytes_like(source_original, source_fields, retained)
    before_snapshot = _semantic_snapshot(predecessor_retained)
    after_snapshot = _semantic_snapshot(source_candidate)
    if before_snapshot != after_snapshot:
        raise Stop("SCOPE_SUPERSESSION_RETAINED_SEMANTIC_DRIFT")

    opponents, opponent_proof = _regenerate_opponents(
        predecessor_members["opponents.csv"],
        retained,
    )
    conferences, conference_proof = _clip_conferences(
        predecessor_members["conferences.csv"],
        new_scope,
    )
    venues, venue_proof = _rebase_venues(
        predecessor_members["venues.csv"],
        current_main_venues,
        retained,
        drop_keys=list(spec.get("drop_school_venue_keys") or []),
    )
    notes = _update_notes(
        predecessor_members["notes.md"],
        spec=spec,
        retained_games=retained,
        source_notes=False,
    )
    source_notes = _update_notes(
        predecessor_members["source-notes.md"],
        spec=spec,
        retained_games=retained,
        source_notes=True,
    )

    members = {
        "conferences.csv": conferences,
        "notes.md": notes,
        "opponents.csv": opponents,
        "source-games.csv": source_candidate,
        "source-notes.md": source_notes,
        "venues.csv": venues,
    }
    proof = {
        "schema_version": 1,
        "workflow_kind": WORKFLOW_KIND,
        "school_key": school_key,
        "old_scope": old_scope,
        "new_scope": new_scope,
        "source_game_count_before": len(source_rows),
        "source_game_count_after": len(retained),
        "excluded_source_game_count": len(derived_excluded),
        "excluded_source_game_ids_sha256": sha256_bytes(
            ("\n".join(derived_excluded) + "\n").encode("utf-8")
        ),
        "retained_source_game_ids_sha256": sha256_bytes(
            ("\n".join(row["source_game_id"] for row in retained) + "\n").encode(
                "utf-8"
            )
        ),
        "predecessor_retained_semantic_sha256": semantic_snapshot_sha256(
            before_snapshot
        ),
        "candidate_semantic_sha256": semantic_snapshot_sha256(after_snapshot),
        "retained_semantic_equivalence": "PASS",
        "opponents": opponent_proof,
        "conferences": conference_proof,
        "venues": venue_proof,
        "package_member_sha256": {
            name: sha256_bytes(members[name]) for name in REQUIRED_PACKAGE_FILES
        },
    }
    return members, proof


def deterministic_package_zip_bytes(members: dict[str, bytes]) -> bytes:
    missing = sorted(set(REQUIRED_PACKAGE_FILES) - set(members))
    extra = sorted(set(members) - set(REQUIRED_PACKAGE_FILES))
    if missing or extra:
        raise Stop(
            "SCOPE_SUPERSESSION_PACKAGE_MEMBER_SET_INVALID missing=%s extra=%s"
            % (missing, extra)
        )
    buffer = io.BytesIO()
    with zipfile.ZipFile(
        buffer,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for name in REQUIRED_PACKAGE_FILES:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, members[name])
    return buffer.getvalue()


def proof_sha256(proof: dict[str, Any]) -> str:
    data = json.dumps(
        proof,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(data)


def augment_integration_freeze(
    freeze_bytes: bytes,
    *,
    request: dict[str, Any],
    spec: dict[str, Any],
    proof: dict[str, Any],
    candidate_zip_sha256: str,
) -> bytes:
    """Bind the fresh ordinary Phase 0 freeze to the supersession authority."""

    try:
        manifest = json.loads(freeze_bytes)
    except (TypeError, ValueError) as exc:
        raise Stop("SCOPE_SUPERSESSION_INTEGRATION_FREEZE_INVALID") from exc
    if not isinstance(manifest, dict) or manifest.get("status") != "INTEGRATION_FROZEN":
        raise Stop("SCOPE_SUPERSESSION_INTEGRATION_FREEZE_STATUS_INVALID")
    if manifest.get("school_key") != request["school_key"]:
        raise Stop("SCOPE_SUPERSESSION_INTEGRATION_FREEZE_SCHOOL_MISMATCH")
    if manifest.get("research_zip_sha256") != candidate_zip_sha256:
        raise Stop("SCOPE_SUPERSESSION_INTEGRATION_FREEZE_CANDIDATE_MISMATCH")
    semantic = (manifest.get("source_game_semantic_guard") or {}).get(
        "snapshot_sha256"
    )
    if semantic != proof.get("candidate_semantic_sha256"):
        raise Stop("SCOPE_SUPERSESSION_INTEGRATION_FREEZE_SEMANTIC_MISMATCH")

    manifest["workflow_kind"] = WORKFLOW_KIND
    manifest["scope_supersession"] = {
        "schema_version": 1,
        "authority_kind": "OWNER_AND_CONTROL_CENTER_SUPERSESSION",
        "scope_supersession_spec_sha256": request["scope_supersession_spec"][
            "sha256"
        ],
        "original_research_zip_sha256": request["research_checkpoint"]["sha256"],
        "research_base_sha": request["research_checkpoint"]["research_base_sha"],
        "candidate_zip_sha256": candidate_zip_sha256,
        "target_predecessor_sha": request["target_sha"],
        "superseded_phase0_successor_sha256": request[
            "superseded_phase0_successor"
        ]["sha256"],
        "superseded_successor_sha256": request["superseded_successor"]["sha256"],
        "superseded_integration_freeze_sha256": request[
            "superseded_integration_freeze_sha256"
        ],
        "superseded_semantic_snapshot_sha256": request[
            "superseded_semantic_snapshot_sha256"
        ],
        "old_scope": spec["old_scope"],
        "new_scope": spec["new_scope"],
        "excluded_source_game_count": proof["excluded_source_game_count"],
        "excluded_source_game_ids_sha256": proof[
            "excluded_source_game_ids_sha256"
        ],
        "retained_source_game_count": proof["source_game_count_after"],
        "retained_source_game_ids_sha256": proof[
            "retained_source_game_ids_sha256"
        ],
        "predecessor_retained_semantic_sha256": proof[
            "predecessor_retained_semantic_sha256"
        ],
        "candidate_semantic_sha256": proof["candidate_semantic_sha256"],
        "retained_semantic_equivalence": proof[
            "retained_semantic_equivalence"
        ],
        "proof_sha256": proof_sha256(proof),
        "authority_statement": spec["authority_statement"],
    }
    return (
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
