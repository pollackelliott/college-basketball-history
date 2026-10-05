#!/usr/bin/env python3
"""Research Stage 4 deterministic mechanical closeout.

This command does not research or alter historical meaning. It consumes an already
assembled six-file package plus the completed Stage 3B checkpoint and owns the
mechanical closeout work that follows package authoring:

- validate the Stage 3B checkpoint manifest/status;
- reconcile the exact game-ID population and core historical meaning;
- run the permanent research portfolio acceptance gate;
- generate the complete NON_D1 owner-scan presentation;
- write deterministic package/QA/status/checkpoint artifacts.

If any of the six package files are missing, the command stops immediately with an
explicit authoring-incomplete status instead of attempting research or repository
reconstruction.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

from onboarding_hardening import research_portfolio_report

REQUIRED_PACKAGE_FILES = (
    "conferences.csv",
    "notes.md",
    "opponents.csv",
    "source-games.csv",
    "source-notes.md",
    "venues.csv",
)
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
FALSE_VALUES = {"no", "false", "0", "n", "non_d1", "non-d1", "non d1"}
TRUE_VALUES = {"yes", "true", "1", "y", "d1", "current_d1", "current-d1"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv_bytes(data: bytes) -> tuple[list[str], list[dict[str, str]]]:
    text = data.decode("utf-8-sig")
    handle = io.StringIO(text, newline="")
    reader = csv.DictReader(handle)
    return list(reader.fieldnames or []), list(reader)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return read_csv_bytes(path.read_bytes())


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_deterministic_zip(path: Path, members: dict[str, bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, members[name])


CURRENT_STAGE3B_PARENT_MEMBERS = {
    "checkpoint-manifest.json",
    "stage3b-status.json",
    "stage3b-working-ledger.csv",
}
LEGACY_STAGE3B_PARENT_MEMBERS = {
    "manifest.json",
    "stage3b-status.json",
    "stage3b-ledger.csv",
}


def _safe_relative_member(name: str) -> str:
    path = PurePosixPath(name)
    if (
        not name
        or path.is_absolute()
        or ".." in path.parts
        or name.startswith("./")
    ):
        raise ValueError(
            f"unsafe Stage 3B manifest member name: {name!r}"
        )
    return path.as_posix()


def _manifest_records(
    manifest: dict[str, Any],
    *,
    legacy: bool,
) -> list[dict[str, Any]]:
    files = manifest.get("files", {})
    if legacy:
        if not isinstance(files, dict):
            raise ValueError(
                "legacy Stage 3B manifest files must be a "
                "filename-keyed object"
            )
        records: list[dict[str, Any]] = []
        for name, metadata in files.items():
            if not isinstance(metadata, dict):
                raise ValueError(
                    "legacy Stage 3B manifest file metadata "
                    f"must be an object: {name!r}"
                )
            record = dict(metadata)
            record["name"] = str(name)
            records.append(record)
        return records

    if not isinstance(files, list):
        raise ValueError(
            "current Stage 3B manifest files must be a list"
        )
    records = []
    for item in files:
        if not isinstance(item, dict):
            raise ValueError(
                "current Stage 3B manifest file records "
                "must be objects"
            )
        records.append(dict(item))
    return records


def resolve_stage3b_parent_layout(
    archive: zipfile.ZipFile,
) -> dict[str, str]:
    names = {
        name for name in archive.namelist()
        if name and not name.endswith("/")
    }

    current_complete = CURRENT_STAGE3B_PARENT_MEMBERS.issubset(
        names
    )

    legacy_candidates: list[str] = []
    prefixes = {
        name.split("/", 1)[0]
        for name in names
        if "/" in name
    }
    for prefix in sorted(prefixes):
        required = {
            f"{prefix}/{name}"
            for name in LEGACY_STAGE3B_PARENT_MEMBERS
        }
        if required.issubset(names):
            legacy_candidates.append(prefix)

    if current_complete and legacy_candidates:
        raise ValueError(
            "Stage 3B checkpoint has ambiguous mixed current/legacy "
            "parent layouts"
        )
    if len(legacy_candidates) > 1:
        raise ValueError(
            "Stage 3B checkpoint has multiple legacy parent directories: "
            + ", ".join(legacy_candidates)
        )

    if current_complete:
        return {
            "topology": "CURRENT_ROOT",
            "prefix": "",
            "manifest_path": "checkpoint-manifest.json",
            "status_path": "stage3b-status.json",
            "ledger_path": "stage3b-working-ledger.csv",
        }

    if len(legacy_candidates) == 1:
        prefix = legacy_candidates[0]
        outside = sorted(
            name
            for name in names
            if not name.startswith(prefix + "/")
        )
        if outside:
            raise ValueError(
                "legacy Stage 3B checkpoint must contain exactly one "
                "containing directory; outside members: "
                + ", ".join(outside[:10])
            )
        return {
            "topology": "LEGACY_SINGLE_DIRECTORY",
            "prefix": prefix + "/",
            "manifest_path": f"{prefix}/manifest.json",
            "status_path": f"{prefix}/stage3b-status.json",
            "ledger_path": f"{prefix}/stage3b-ledger.csv",
        }

    raise ValueError(
        "Stage 3B checkpoint does not match the current root layout "
        "or the supported single-directory legacy layout"
    )


def validate_checkpoint_manifest(
    archive: zipfile.ZipFile,
    layout: dict[str, str],
) -> dict[str, Any]:
    names = set(archive.namelist())
    manifest_path = layout["manifest_path"]
    if manifest_path not in names:
        raise ValueError(
            "Stage 3B checkpoint is missing "
            + manifest_path
        )

    manifest = json.loads(archive.read(manifest_path))
    legacy = layout["topology"] == "LEGACY_SINGLE_DIRECTORY"
    records = _manifest_records(manifest, legacy=legacy)

    defects: list[dict[str, Any]] = []
    for item in records:
        logical_name = _safe_relative_member(
            str(item.get("name", ""))
        )
        if logical_name in {
            "checkpoint-manifest.json",
            "manifest.json",
        }:
            continue
        member_name = (
            layout["prefix"] + logical_name
            if legacy
            else logical_name
        )
        if member_name not in names:
            defects.append(
                {
                    "reason": "MISSING_MEMBER",
                    "name": logical_name,
                }
            )
            continue
        data = archive.read(member_name)
        expected_sha = item.get("sha256")
        expected_size = item.get(
            "bytes",
            item.get("size_bytes", item.get("size")),
        )
        if expected_sha and sha256_bytes(data) != expected_sha:
            defects.append(
                {
                    "reason": "HASH_MISMATCH",
                    "name": logical_name,
                }
            )
        if (
            expected_size is not None
            and len(data) != int(expected_size)
        ):
            defects.append(
                {
                    "reason": "SIZE_MISMATCH",
                    "name": logical_name,
                }
            )
    if defects:
        raise ValueError(
            "Stage 3B checkpoint manifest validation failed: "
            + json.dumps(defects[:10], sort_keys=True)
        )
    return manifest


def normalize_site(value: str) -> str:
    folded = (value or "").strip().upper()
    return {
        "HOME": "SOURCE_PROGRAM_HOME",
        "SOURCE_PROGRAM_HOME": "SOURCE_PROGRAM_HOME",
        "AWAY": "OPPONENT_HOME",
        "OPPONENT_HOME": "OPPONENT_HOME",
        "NEUTRAL": "NEUTRAL",
        "N": "NEUTRAL",
    }.get(folded, folded)


def season_start(value: str) -> str:
    match = re.match(r"^(\d{4})-", (value or "").strip())
    return match.group(1) if match else (value or "").strip()


def _first_parent_value(row: dict[str, str], *fields: str) -> str:
    for field in fields:
        value = row.get(field, "").strip()
        if value:
            return value
    return ""


def first_literal(row: dict[str, str], *fields: str) -> str:
    """Return the first populated literal field without normalizing its bytes."""

    for field in fields:
        value = row.get(field)
        if value is not None and value != "":
            return value
    return ""


def project_game_id(row: dict[str, str]) -> str:
    """Project one accepted stable game ID across Research/Stage 4 namespaces."""

    for field in ("source_game_id", "research_game_id"):
        value = str(row.get(field, "") or "").strip()
        if value:
            return value
    return ""


def project_season_label(value: str) -> str:
    """Project accepted season labels into the six-file YYYY-YYYY form."""

    label = (value or "").strip()
    if not label:
        return ""

    full = re.fullmatch(r"(\d{4})-(\d{4})", label)
    compact = re.fullmatch(r"(\d{4})-(\d{2})", label)
    if full:
        start = int(full.group(1))
        end = int(full.group(2))
        if end != start + 1:
            raise ValueError(
                f"inconsistent full season_label {label!r}; expected "
                f"{start:04d}-{start + 1:04d}"
            )
        return label
    if compact:
        start = int(compact.group(1))
        suffix = int(compact.group(2))
        expected_suffix = (start + 1) % 100
        if suffix != expected_suffix:
            raise ValueError(
                f"inconsistent compact season_label {label!r}; expected "
                f"{start:04d}-{expected_suffix:02d}"
            )
        return f"{start:04d}-{start + 1:04d}"

    raise ValueError(
        f"unsupported season_label {label!r}; expected YYYY-YY or YYYY-YYYY"
    )


def project_administrative_status(
    row: dict[str, str],
) -> tuple[str, str]:
    """Project accepted legacy administrative vocabulary without changing play."""

    status = row.get("administrative_status", "").strip()
    note = row.get("administrative_note", "").strip()
    if status != "FORFEIT_LOSS":
        return status, note

    played = row.get("played_result", "").strip()
    provenance = (
        "Stage 4 representation normalization: accepted legacy "
        "administrative_status FORFEIT_LOSS projected to FORFEIT; "
        f"on-court played_result={played or '[blank]'} unchanged."
    )
    return "FORFEIT", f"{note} {provenance}".strip()


def normalize_game_type(value: str) -> str:
    folded = (value or "").strip().upper()
    return {
        "NCAA": "NCAA_TOURNAMENT",
        "NCAA_TOURNAMENT": "NCAA_TOURNAMENT",
        "REGULAR": "REGULAR_SEASON",
        "REGULAR_SEASON": "REGULAR_SEASON",
        "CONFERENCE_TOURNAMENT": "CONFERENCE_TOURNAMENT",
        "NIT": "NIT",
        "POSTSEASON": "POSTSEASON",
    }.get(folded, folded)


def expected_parent_values(row: dict[str, str]) -> dict[str, str]:
    stage3b_status = row.get("stage3b_status", "").strip()
    stage3b_payload_present = any(
        row.get(field, "").strip()
        for field in (
            "stage3b_physical_venue_name",
            "stage3b_curated_venue_name",
            "stage3b_venue_city",
            "stage3b_site_city",
            "stage3b_venue_state",
            "stage3b_site_state",
            "stage3b_current_main_venue_key",
            "stage3b_curated_venue_key",
            "stage3a_final_venue_name",
            "stage3a_final_city",
            "stage3a_final_state",
            "accepted_venue_name",
            "accepted_city",
            "accepted_state",
            "accepted_venue_key",
        )
    )
    stage3b_active = (
        stage3b_status != "NOT_APPLICABLE_REGULAR_SEASON"
        and (bool(stage3b_status) or stage3b_payload_present)
    )

    site = _first_parent_value(
        row,
        "stage3b_site_type",
        "stage3a_final_site_type",
        "stage3a_final_han",
        "curated_site_type",
        "site_type",
    )
    if stage3b_active:
        venue = _first_parent_value(
            row,
            "stage3b_physical_venue_name",
            "stage3b_curated_venue_name",
            "stage3a_final_physical_venue_name",
            "stage3a_final_venue_name",
            "accepted_venue_name",
            "stage3a_curated_venue_name",
        )
        city = _first_parent_value(
            row,
            "stage3b_venue_city",
            "stage3b_site_city",
            "stage3a_final_venue_city",
            "stage3a_final_city",
            "accepted_city",
            "stage3a_site_city",
        )
        state = _first_parent_value(
            row,
            "stage3b_venue_state",
            "stage3b_site_state",
            "stage3a_final_venue_state",
            "stage3a_final_state",
            "accepted_state",
            "stage3a_site_state",
        )
        venue_key = _first_parent_value(
            row,
            "stage3b_current_main_venue_key",
            "stage3b_curated_venue_key",
            "stage3a_final_current_main_venue_key",
            "accepted_venue_key",
            "stage3a_curated_venue_key",
        )
    else:
        venue = _first_parent_value(
            row,
            "stage3a_final_physical_venue_name",
            "stage3a_final_venue_name",
            "accepted_venue_name",
            "stage3a_curated_venue_name",
            "stage3a2_physical_venue_name",
            "stage3a3_physical_venue_name",
        )
        city = _first_parent_value(
            row,
            "stage3a_final_venue_city",
            "stage3a_final_city",
            "accepted_city",
            "stage3a_site_city",
            "stage3a2_venue_city",
            "stage3a3_venue_city",
        )
        state = _first_parent_value(
            row,
            "stage3a_final_venue_state",
            "stage3a_final_state",
            "accepted_state",
            "stage3a_site_state",
            "stage3a2_venue_state",
            "stage3a3_venue_state",
        )
        venue_key = _first_parent_value(
            row,
            "stage3a_final_current_main_venue_key",
            "accepted_venue_key",
            "stage3a_curated_venue_key",
            "stage3a2_current_main_venue_key",
            "stage3a3_current_main_venue_key",
        )

    return {
        "source_program_key": row.get("source_program_key", "").strip(),
        "season_start": season_start(row.get("season_label", "")),
        "game_date": row.get("game_date", "").strip(),
        "normalized_opponent_key": _first_parent_value(
            row,
            "opponent_program_key",
            "normalized_opponent_key",
            "opponent_key",
        ),
        "team_score": row.get("team_score", "").strip(),
        "opponent_score": row.get("opponent_score", "").strip(),
        "played_result": row.get("played_result", "").strip(),
        "overtime_periods": row.get("overtime_periods", "").strip(),
        "curated_site_type": normalize_site(site),
        "venue_present": "1" if venue.strip() else "0",
        "venue_key": venue_key,
        "city": city.strip(),
        "state": state.strip(),
        "curated_game_type": normalize_game_type(
            _first_parent_value(
                row,
                "curated_game_type",
                "game_type",
                "structured_game_type",
            )
        ),
        "raw_text": first_literal(row, "raw_text", "source_raw_text"),
    }


def _normalized_venue_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").casefold())


def _package_venue_matches_parent_key(
    package_row: dict[str, str],
    expected_venue_key: str,
    venue_rows_by_key: dict[str, list[dict[str, str]]],
    venue_rows: list[dict[str, str]],
) -> bool:
    candidates = venue_rows_by_key.get(expected_venue_key, [])
    if len(candidates) != 1:
        return False

    venue_row = candidates[0]
    package_name = _normalized_venue_name(
        package_row.get("curated_venue_name", "")
    )
    accepted_names = {
        _normalized_venue_name(name)
        for name in (
            [venue_row.get("canonical_name", "").strip()]
            + [
                alias.strip()
                for alias in venue_row.get("aliases", "").split(";")
            ]
        )
        if name.strip()
    }
    if not package_name or package_name not in accepted_names:
        return False

    locality_conflict = False
    for game_field, venue_field in (("city", "city"), ("state", "state")):
        game_value = package_row.get(game_field, "").strip()
        venue_value = venue_row.get(venue_field, "").strip()
        if (
            game_value
            and venue_value
            and game_value.casefold() != venue_value.casefold()
        ):
            locality_conflict = True
            break

    if not locality_conflict:
        return True

    # A game may preserve an accepted locality label that differs from the
    # canonical locality stored for the same physical venue. Venue-key
    # identity is ambiguous only when another same-name venue row is
    # compatible with the accepted game locality. The game city/state fields
    # are compared separately against the Stage 3B parent and remain strict.
    package_city = package_row.get("city", "").strip()
    package_state = package_row.get("state", "").strip()
    for other in venue_rows:
        other_key = other.get("venue_key", "").strip()
        if not other_key or other_key == expected_venue_key:
            continue
        other_names = {
            _normalized_venue_name(name)
            for name in (
                [other.get("canonical_name", "").strip()]
                + [
                    alias.strip()
                    for alias in other.get("aliases", "").split(";")
                ]
            )
            if name.strip()
        }
        if package_name not in other_names:
            continue

        other_city = other.get("city", "").strip()
        other_state = other.get("state", "").strip()
        city_matches = (
            not package_city
            or not other_city
            or package_city.casefold() == other_city.casefold()
        )
        state_matches = (
            not package_state
            or not other_state
            or package_state.casefold() == other_state.casefold()
        )
        if city_matches and state_matches:
            return False

    return True


def compare_parent_semantics(
    parent_rows: list[dict[str, str]],
    package_rows: list[dict[str, str]],
    venue_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    parent = {
        project_game_id(r): r
        for r in parent_rows
    }
    package = {
        str(r.get("source_game_id") or "").strip(): r
        for r in package_rows
    }
    venue_rows_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for venue_row in venue_rows:
        key = venue_row.get("venue_key", "").strip()
        if key:
            venue_rows_by_key[key].append(venue_row)

    mismatches: list[dict[str, str]] = []
    for game_id in sorted(parent):
        if game_id not in package:
            continue
        expected = expected_parent_values(parent[game_id])
        actual_row = package[game_id]
        actual = {
            "source_program_key": actual_row.get("source_program_key", "").strip(),
            "season_start": season_start(actual_row.get("season_label", "")),
            "game_date": actual_row.get("game_date", "").strip(),
            "normalized_opponent_key": actual_row.get(
                "normalized_opponent_key", ""
            ).strip(),
            "team_score": actual_row.get("team_score", "").strip(),
            "opponent_score": actual_row.get("opponent_score", "").strip(),
            "played_result": actual_row.get("played_result", "").strip(),
            "overtime_periods": actual_row.get("overtime_periods", "").strip(),
            "curated_site_type": normalize_site(
                actual_row.get("curated_site_type", "")
            ),
            "venue_present": (
                "1" if actual_row.get("curated_venue_name", "").strip() else "0"
            ),
            "city": actual_row.get("city", "").strip(),
            "state": actual_row.get("state", "").strip(),
            "curated_game_type": actual_row.get(
                "curated_game_type", ""
            ).strip(),
            "raw_text": actual_row.get("raw_text", ""),
        }
        for field in expected:
            if field == "venue_key":
                if not expected[field]:
                    continue
                package_value = (
                    expected[field]
                    if _package_venue_matches_parent_key(
                        actual_row,
                        expected[field],
                        venue_rows_by_key,
                        venue_rows,
                    )
                    else ""
                )
            else:
                package_value = actual[field]

            if expected[field] != package_value:
                mismatches.append(
                    {
                        "source_game_id": game_id,
                        "field": field,
                        "parent_value": expected[field],
                        "package_value": package_value,
                    }
                )
    return mismatches

def current_d1_flag(value: str) -> bool | None:
    folded = (value or "").strip().casefold()
    if folded in TRUE_VALUES:
        return True
    if folded in FALSE_VALUES:
        return False
    return None


def generate_non_d1_scan(
    package_dir: Path,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    _, opponents = read_csv(package_dir / "opponents.csv")
    _, games = read_csv(package_dir / "source-games.csv")
    by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    invalid_flags: list[dict[str, str]] = []

    for row in opponents:
        key = row.get("canonical_opponent_key", "").strip()
        flag = current_d1_flag(row.get("current_d1", ""))
        if flag is None:
            invalid_flags.append(
                {
                    "source_opponent_label": row.get(
                        "source_opponent_label", ""
                    ),
                    "canonical_opponent_key": key,
                    "current_d1": row.get("current_d1", ""),
                }
            )
        elif flag is False:
            by_key[key].append(row)

    if invalid_flags:
        raise ValueError(
            "opponents.csv has non-boolean current_d1 classifications: "
            + json.dumps(invalid_flags[:10], sort_keys=True)
        )

    games_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in games:
        games_by_key[
            row.get("normalized_opponent_key", "").strip()
        ].append(row)

    rows: list[dict[str, str]] = []
    for key in sorted(by_key):
        mapping_rows = by_key[key]
        names = sorted(
            {
                r.get("canonical_opponent_name", "").strip()
                for r in mapping_rows
                if r.get("canonical_opponent_name", "").strip()
            }
        )
        if len(names) > 1:
            raise ValueError(
                f"NON_D1 key {key!r} has multiple canonical names: {names}"
            )
        game_rows = games_by_key.get(key, [])
        labels = sorted(
            {
                r.get("source_opponent_label", "").strip()
                for r in game_rows
                if r.get("source_opponent_label", "").strip()
            }
        )
        seasons = sorted(
            {
                r.get("season_label", "").strip()
                for r in game_rows
                if r.get("season_label", "").strip()
            }
        )
        display = names[0] if names else key
        folded_display = re.sub(
            r"[^a-z0-9]+", "", display.casefold()
        )
        differing = [
            label
            for label in labels
            if re.sub(r"[^a-z0-9]+", "", label.casefold())
            != folded_display
        ]
        note = (
            "Representative source label differs from canonical display."
            if differing
            else ""
        )
        rows.append(
            {
                "canonical_opponent_key": key,
                "canonical_opponent_name": display,
                "game_count": str(len(game_rows)),
                "first_season": seasons[0] if seasons else "",
                "last_season": seasons[-1] if seasons else "",
                "representative_source_labels": "; ".join(labels[:5]),
                "additional_source_label_count": str(
                    max(0, len(labels) - 5)
                ),
                "note": note,
            }
        )

    return rows, {
        "distinct_identities": len(rows),
        "games": sum(int(r["game_count"]) for r in rows),
    }


def render_non_d1_markdown(
    school_key: str,
    rows: list[dict[str, str]],
    summary: dict[str, Any],
) -> str:
    lines = [
        f"# {school_key} NON_D1 owner sanity scan",
        "",
        f"Distinct NON_D1 identities: {summary['distinct_identities']}",
        f"Games represented: {summary['games']}",
        "",
        "| Opponent | Key | Games | Seasons | Representative source labels | Note |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for row in rows:
        seasons = (
            row["first_season"]
            if row["first_season"] == row["last_season"]
            else f"{row['first_season']}–{row['last_season']}"
        )
        labels = row["representative_source_labels"]
        if row["additional_source_label_count"] != "0":
            labels += (
                f" (+{row['additional_source_label_count']} more)"
            )
        cells = [
            row["canonical_opponent_name"],
            row["canonical_opponent_key"],
            row["game_count"],
            seasons,
            labels,
            row["note"],
        ]
        cells = [
            cell.replace("|", "\\|").replace("\n", " ")
            for cell in cells
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines.extend(
        [
            "",
            (
                "Owner action: rapid sanity scan only. Flag only entries "
                "that appear misclassified or otherwise suspicious."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def manifest_for_members(
    members: dict[str, bytes],
) -> dict[str, Any]:
    return {
        "files": [
            {
                "name": name,
                "bytes": len(data),
                "sha256": sha256_bytes(data),
            }
            for name, data in sorted(members.items())
        ]
    }


def closeout(
    school_key: str,
    package_dir: Path,
    stage3b_checkpoint: Path,
    main_sha: str,
    output_dir: Path,
) -> dict[str, Any]:
    package_dir = package_dir.resolve()
    stage3b_checkpoint = stage3b_checkpoint.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    missing = [
        name
        for name in REQUIRED_PACKAGE_FILES
        if not (package_dir / name).is_file()
    ]
    empty_markdown = [
        name
        for name in ("notes.md", "source-notes.md")
        if (package_dir / name).is_file()
        and not (package_dir / name).read_text(
            encoding="utf-8"
        ).strip()
    ]
    if missing or empty_markdown:
        status = {
            "schema_version": 1,
            "school_key": school_key,
            "stage": "STAGE_4",
            "status": "PACKAGE_AUTHORING_INCOMPLETE",
            "protected_main_sha": main_sha,
            "missing_required_files": missing,
            "empty_markdown_files": empty_markdown,
            "repository_mutations": 0,
            "next_bounded_assignment": (
                "Finish only the listed Stage 4 package-authoring files, "
                "then rerun this permanent closeout command. Do not open "
                "new historical research merely because closeout is incomplete."
            ),
        }
        write_json(output_dir / "stage4-status.json", status)
        return status

    parent_bytes = stage3b_checkpoint.read_bytes()
    parent_sha = sha256_bytes(parent_bytes)
    with zipfile.ZipFile(io.BytesIO(parent_bytes)) as parent_zip:
        parent_layout = resolve_stage3b_parent_layout(
            parent_zip
        )
        parent_manifest = validate_checkpoint_manifest(
            parent_zip,
            parent_layout,
        )
        parent_status = json.loads(
            parent_zip.read(parent_layout["status_path"])
        )
        if str(parent_status.get("status", "")).upper() != "COMPLETE":
            raise ValueError(
                "Stage 3B checkpoint is not COMPLETE: "
                f"{parent_status.get('status')!r}"
            )
        if (
            parent_status.get("school_key")
            and parent_status.get("school_key") != school_key
        ):
            raise ValueError(
                "Stage 3B checkpoint school_key mismatch: "
                f"expected {school_key!r}, "
                f"found {parent_status.get('school_key')!r}"
            )
        _, parent_rows = read_csv_bytes(
            parent_zip.read(parent_layout["ledger_path"])
        )

    package_members = {
        name: (package_dir / name).read_bytes()
        for name in REQUIRED_PACKAGE_FILES
    }
    package_zip = output_dir / "stage4-research-package.zip"
    write_deterministic_zip(package_zip, package_members)
    package_sha = sha256_file(package_zip)

    _, package_rows = read_csv(
        package_dir / "source-games.csv"
    )
    _, venue_rows = read_csv(package_dir / "venues.csv")
    package_ids = [
        r.get("source_game_id", "").strip()
        for r in package_rows
    ]
    parent_ids = [project_game_id(r) for r in parent_rows]
    parent_sanity = {
        "status": "PASS",
        "stage3b_checkpoint_sha256": parent_sha,
        "stage3b_manifest_validation": "PASS",
        "stage3b_parent_topology": parent_layout["topology"],
        "stage3b_manifest_member": parent_layout["manifest_path"],
        "stage3b_status_member": parent_layout["status_path"],
        "stage3b_ledger_member": parent_layout["ledger_path"],
        "stage3b_parent_rows": len(parent_rows),
        "package_source_game_rows": len(package_rows),
        "stage3b_parent_game_ids_unique": (
            len(parent_ids) == len(set(parent_ids))
            and all(parent_ids)
        ),
        "package_game_ids_unique": (
            len(package_ids) == len(set(package_ids))
            and all(package_ids)
        ),
        "source_game_id_population_exact_match": (
            set(parent_ids) == set(package_ids)
            and len(parent_ids) == len(package_ids)
        ),
        "protected_main_sha": main_sha,
        "research_base_sha": parent_status.get(
            "research_base_sha",
            parent_manifest.get("research_base_sha", ""),
        ),
    }
    if (
        not parent_sanity["stage3b_parent_game_ids_unique"]
        or not parent_sanity["package_game_ids_unique"]
        or not parent_sanity[
            "source_game_id_population_exact_match"
        ]
    ):
        parent_sanity["status"] = "FAIL"
        write_json(
            output_dir / "stage4-parent-sanity-check.json",
            parent_sanity,
        )
        raise ValueError(
            "Stage 4 package game-ID population does not exactly "
            "match the Stage 3B parent"
        )

    mismatches = compare_parent_semantics(
        parent_rows,
        package_rows,
        venue_rows,
    )
    parent_sanity[
        "semantic_comparison_unexpected_mismatches"
    ] = len(mismatches)
    parent_sanity["semantic_comparison_examples"] = mismatches[:25]
    if mismatches:
        parent_sanity["status"] = "FAIL"
        write_json(
            output_dir / "stage4-parent-sanity-check.json",
            parent_sanity,
        )
        raise ValueError(
            "Stage 4 package changed "
            f"{len(mismatches)} accepted Stage 3B semantic "
            "field value(s)"
        )
    write_json(
        output_dir / "stage4-parent-sanity-check.json",
        parent_sanity,
    )

    research_check = research_portfolio_report(
        package_zip,
        school_key=school_key,
        expected_sha256=package_sha,
    )
    write_json(
        output_dir / "stage4-research-check.json",
        research_check,
    )
    if research_check["status"] != "PASS":
        raise ValueError(
            "Stage 4 research acceptance failed with "
            f"{len(research_check['errors'])} error(s)"
        )

    scan_rows, scan_summary = generate_non_d1_scan(package_dir)
    scan_fields = [
        "canonical_opponent_key",
        "canonical_opponent_name",
        "game_count",
        "first_season",
        "last_season",
        "representative_source_labels",
        "additional_source_label_count",
        "note",
    ]
    write_csv(
        output_dir / "non-d1-owner-scan.csv",
        scan_fields,
        scan_rows,
    )
    (output_dir / "non-d1-owner-scan.md").write_text(
        render_non_d1_markdown(
            school_key,
            scan_rows,
            scan_summary,
        ),
        encoding="utf-8",
    )

    package_qa = {
        "status": "PASS",
        "protected_main_sha": main_sha,
        "research_base_sha": parent_sanity["research_base_sha"],
        "stage3b_parent_sha256": parent_sha,
        "six_file_package_sha256": package_sha,
        "six_file_package_exact_flat_members": list(
            REQUIRED_PACKAGE_FILES
        ),
        "stage3b_game_id_population_exact_match": True,
        "stage3b_semantic_comparison_unexpected_mismatches": 0,
        "research_acceptance_contract_check": "PASS",
        "research_acceptance_contract_errors": 0,
        "research_acceptance_contract_warnings": len(
            research_check.get("warnings", [])
        ),
        "owner_scan": scan_summary,
        "mechanical_stage4_csv_repairs_required": 0,
        "mechanical_stage4_csv_repairs_applied": 0,
    }
    write_json(
        output_dir / "stage4-package-qa.json",
        package_qa,
    )

    counts = research_check["counts"]
    status = {
        "schema_version": 1,
        "school_key": school_key,
        "stage": "STAGE_4",
        "status": "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY",
        "terminal_label": (
            "STAGE 4: COMPLETE — OWNER NON_D1 SANITY SCAN READY"
        ),
        "protected_main_sha": main_sha,
        "research_base_sha": parent_sanity["research_base_sha"],
        "source_stage3b_complete_checkpoint_sha256": parent_sha,
        "six_file_package_sha256": package_sha,
        "source_games_rows": counts["competitive_games"],
        "opponent_rows": counts["opponent_rows"],
        "venue_rows": counts["venue_rows"],
        "conference_rows": counts["conference_rows"],
        "package_qa": "PASS",
        "research_acceptance_contract_qa": "PASS",
        "unresolved_opponent_identities": counts[
            "unresolved_opponents"
        ],
        "unknown_han_rows": counts["site_types"].get(
            "UNKNOWN", 0
        ),
        "home_publication_blocker_rows": counts[
            "site_completeness"
        ].get("home_publication_blocker_rows", 0),
        "material_site_gap_rows": counts["site_completeness"].get(
            "material_gap_rows", 0
        ),
        "researched_site_gap_rows": counts[
            "site_completeness"
        ].get("researched_gap_rows", 0),
        "unaccounted_site_gap_rows": counts[
            "site_completeness"
        ].get("unaccounted_gap_rows", 0),
        "ncaa_rows": counts["ncaa_rows"],
        "non_d1_owner_scan_distinct_identities": scan_summary[
            "distinct_identities"
        ],
        "non_d1_owner_scan_games": scan_summary["games"],
        "owner_non_d1_scan_ready": True,
        "owner_non_d1_scan_approved": False,
        "stage5_started": False,
        "repository_mutations": 0,
        "mechanical_stage4_csv_repairs_applied": 0,
        "next_bounded_assignment": (
            "Stage 5 only after a new owner continuation: present "
            "the complete NON_D1 owner-scan population and stop for "
            "actual owner disposition. Do not begin Stage 6 automatically."
        ),
    }
    write_json(output_dir / "stage4-status.json", status)

    checkpoint_members: dict[str, bytes] = {
        "README.txt": (
            "Research Stage 4 deterministic closeout checkpoint.\n"
            "Historical meaning is inherited from the completed "
            "Stage 3B parent; this checkpoint records only mechanical "
            "Stage 4 assembly/QA and owner-scan readiness.\n"
        ).encode(),
        "stage3b-complete-checkpoint.zip": parent_bytes,
        "stage4-research-package.zip": package_zip.read_bytes(),
    }
    for name in REQUIRED_PACKAGE_FILES:
        checkpoint_members[name] = package_members[name]
    for name in (
        "stage4-parent-sanity-check.json",
        "stage4-research-check.json",
        "stage4-package-qa.json",
        "stage4-status.json",
        "non-d1-owner-scan.csv",
        "non-d1-owner-scan.md",
    ):
        checkpoint_members[name] = (
            output_dir / name
        ).read_bytes()

    checkpoint_manifest = manifest_for_members(
        checkpoint_members
    )
    checkpoint_manifest.update(
        {
            "protected_main_sha": main_sha,
            "research_base_sha": parent_sanity[
                "research_base_sha"
            ],
            "school_key": school_key,
            "stage": "STAGE_4",
            "status": (
                "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY"
            ),
            "stage3b_parent_sha256": parent_sha,
            "six_file_package_sha256": package_sha,
        }
    )
    checkpoint_members["checkpoint-manifest.json"] = (
        json.dumps(
            checkpoint_manifest,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode()

    checkpoint_path = (
        output_dir
        / f"{school_key}-stage4-complete-checkpoint.zip"
    )
    write_deterministic_zip(
        checkpoint_path,
        checkpoint_members,
    )
    status["checkpoint_path"] = str(checkpoint_path)
    status["checkpoint_sha256"] = sha256_file(
        checkpoint_path
    )
    write_json(output_dir / "stage4-status.json", status)
    return status


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Deterministic Research Stage 4 mechanical closeout "
            "and owner-scan preparation."
        )
    )
    parser.add_argument("school_key")
    parser.add_argument("package_dir", type=Path)
    parser.add_argument("stage3b_checkpoint", type=Path)
    parser.add_argument("--main-sha", required=True)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output = (
        args.output_dir
        or Path(".research")
        / args.school_key
        / "stage4-closeout"
    )
    try:
        status = closeout(
            args.school_key,
            args.package_dir,
            args.stage3b_checkpoint,
            args.main_sha,
            output,
        )
        print(
            "College Basketball History — Research Stage 4 closeout"
        )
        print(f"School:               {args.school_key}")
        print(f"Status:               {status['status']}")
        if status["status"] == "PACKAGE_AUTHORING_INCOMPLETE":
            print(
                "Missing files:        "
                + ", ".join(status["missing_required_files"])
            )
            print(
                "Empty markdown files: "
                + ", ".join(status["empty_markdown_files"])
            )
            print(
                "STAGE 4: INCOMPLETE — PACKAGE AUTHORING REQUIRED"
            )
            return 2
        print(
            f"Games:                {status['source_games_rows']:,}"
        )
        print(
            "NON_D1 identities:    "
            f"{status['non_d1_owner_scan_distinct_identities']:,}"
        )
        print(
            "NON_D1 games:         "
            f"{status['non_d1_owner_scan_games']:,}"
        )
        print(
            "Package SHA-256:      "
            f"{status['six_file_package_sha256']}"
        )
        print(
            "Checkpoint SHA-256:   "
            f"{status['checkpoint_sha256']}"
        )
        print(
            "STAGE 4: COMPLETE — OWNER NON_D1 SANITY SCAN READY"
        )
        return 0
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
    ) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
