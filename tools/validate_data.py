#!/usr/bin/env python3
"""
Validate the college-basketball-history repository's core data layers.

Usage:
    python tools/validate_data.py

Optional:
    python tools/validate_data.py /path/to/college-basketball-history
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from conference_reference import (
    REQUIRED_HISTORY_COLUMNS,
    REQUIRED_REGISTRY_COLUMNS,
    history_errors,
    registry_by_key,
)
from location_safety import (
    REGISTRY_FALLBACK_PREFIX,
    assertion_drift,
    location_pair_status,
    parse_registry_fallback_markers,
    source_site_agrees_with_canonical,
    venue_location_conflicts,
)


ALLOWED_SITE_TYPES = {
    "TEAM_A_HOME",
    "TEAM_B_HOME",
    "NEUTRAL",
    "UNKNOWN",
}

ALLOWED_GAME_TYPES = {
    "REGULAR_SEASON",
    "CONFERENCE_TOURNAMENT",
    "NCAA_TOURNAMENT",
    "NIT",
}

ALLOWED_POSTSEASON_ROUNDS = {
    "",
    "Play-in",
    "R64",
    "R32",
    "Sweet Sixteen",
    "Elite Eight",
    "Final Four",
    "Championship",
}

ALLOWED_CANONICAL_STATUSES = {
    "PROVISIONAL",
    "VERIFIED",
    "UNDER_REVIEW",
}

ALLOWED_ADMINISTRATIVE_STATUSES = {
    "",
    "FORFEIT",
    "VACATED_GAME",
    "VACATED_WIN",
}

REQUIRED_CANONICAL_COLUMNS = {
    "canonical_game_id",
    "season_label",
    "game_date",
    "date_precision",
    "team_a_key",
    "team_b_key",
    "team_a_score",
    "team_b_score",
    "result_winner_team_key",
    "overtime_periods",
    "site_type",
    "designated_home_team_key",
    "venue_key",
    "site_city",
    "site_state",
    "game_type",
    "postseason_round",
    "administrative_status",
    "administrative_note",
    "canonical_status",
    "notes",
}

REQUIRED_ASSERTION_COLUMNS = {
    "assertion_id",
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
    "source_era",
    "season_label",
    "game_date",
    "source_opponent_label",
    "normalized_opponent_key",
    "normalized_opponent_name",
    "team_score",
    "opponent_score",
    "played_result",
    "overtime_periods",
    "source_site_candidate",
    "curated_site_type",
    "source_venue_name",
    "curated_venue_name",
    "city",
    "state",
    "event_or_tournament",
    "source_round",
    "curated_game_type",
    "curated_postseason_round",
    "source_page",
    "raw_text",
    "normalization_status",
    "notes",
    "match_status",
    "match_method",
}

REQUIRED_DISCREPANCY_COLUMNS = {
    "discrepancy_id",
    "canonical_game_id",
    "field_name",
    "source_a_program_key",
    "source_a_value",
    "source_b_program_key",
    "source_b_value",
    "canonical_value",
    "status",
    "resolution_basis",
    "notes",
}


ALLOWED_YES_NO = {"Yes", "No"}

PROGRAM_ACHIEVEMENT_FIELDS = (
    "conference_regular_season_championships",
    "conference_tournament_championships",
    "final_four_appearances",
    "national_championships",
)

REQUIRED_PROGRAM_COLUMNS = {
    "program_key",
    "program_name",
    "display_name",
    "nickname",
    "current_d1",
    "public_page_enabled",
    "conference_regular_season_championships",
    "conference_tournament_championships",
    "final_four_appearances",
    "national_championships",
}

REQUIRED_CONFERENCE_MEMBERSHIP_COLUMNS = {
    "program_key",
    "season_label",
    "conference_key",
    "conference_name",
}

SEASON_LABEL_RE = re.compile(r"^(\d{4})-(\d{4})$")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return (reader.fieldnames or []), list(reader)


def require_columns(path: Path, actual: list[str], required: set[str], errors: list[str]) -> None:
    missing = sorted(required - set(actual))
    if missing:
        errors.append(f"{path}: missing required columns: {', '.join(missing)}")


def duplicates(values: list[str]) -> set[str]:
    seen = set()
    dupes = set()
    for value in values:
        if value in seen:
            dupes.add(value)
        seen.add(value)
    return dupes


def valid_season_label(value: str) -> bool:
    match = SEASON_LABEL_RE.fullmatch(value)
    if not match:
        return False
    start_year = int(match.group(1))
    end_year = int(match.group(2))
    return end_year == start_year + 1


def main() -> int:
    if len(sys.argv) > 2:
        print("Usage: python tools/validate_data.py [repository_root]")
        return 2

    repo_root = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) == 2
        else Path(__file__).resolve().parents[1]
    )

    canonical_path = repo_root / "data" / "canonical" / "games.csv"
    assertions_path = repo_root / "data" / "evidence" / "game-assertions.csv"
    discrepancies_path = repo_root / "data" / "reconciliation" / "discrepancies.csv"
    programs_path = repo_root / "data" / "reference" / "programs.csv"
    conference_membership_path = (
        repo_root / "data" / "reference" / "conference-membership.csv"
    )
    conferences_path = repo_root / "data" / "reference" / "conferences.csv"

    errors: list[str] = []
    warnings: list[str] = []

    try:
        canonical_columns, canonical_rows = read_csv(canonical_path)
        assertion_columns, assertion_rows = read_csv(assertions_path)
        discrepancy_columns, discrepancy_rows = read_csv(discrepancies_path)
        program_columns, program_rows = read_csv(programs_path)
        membership_columns, membership_rows = read_csv(conference_membership_path)
        conference_columns, conference_rows = read_csv(conferences_path)
    except FileNotFoundError as exc:
        print(f"FAIL: required file not found: {exc}")
        return 1

    require_columns(canonical_path, canonical_columns, REQUIRED_CANONICAL_COLUMNS, errors)
    require_columns(assertions_path, assertion_columns, REQUIRED_ASSERTION_COLUMNS, errors)
    require_columns(discrepancies_path, discrepancy_columns, REQUIRED_DISCREPANCY_COLUMNS, errors)
    require_columns(programs_path, program_columns, REQUIRED_PROGRAM_COLUMNS, errors)
    require_columns(
        conference_membership_path,
        membership_columns,
        REQUIRED_CONFERENCE_MEMBERSHIP_COLUMNS,
        errors,
    )
    require_columns(
        conferences_path,
        conference_columns,
        REQUIRED_REGISTRY_COLUMNS,
        errors,
    )

    conference_keys = [row.get("conference_key", "").strip() for row in conference_rows]
    if "" in conference_keys:
        errors.append("conferences.csv contains a blank conference_key.")
    duplicate_conference_keys = duplicates(conference_keys)
    if duplicate_conference_keys:
        errors.append(
            "conferences.csv contains duplicate conference_key values: "
            + ", ".join(sorted(duplicate_conference_keys))
        )
    conference_registry = registry_by_key(conference_rows)
    for line_number, row in enumerate(conference_rows, start=2):
        key = row.get("conference_key", "").strip()
        if not row.get("conference_name", "").strip():
            errors.append(f"conferences.csv line {line_number}: conference_name is required.")
        if key != "independent" and not row.get("tournament_label", "").strip():
            errors.append(
                f"conferences.csv line {line_number}: owner-approved "
                "tournament_label is required."
            )

    for line_number, row in enumerate(membership_rows, start=2):
        key = row.get("conference_key", "").strip()
        if key not in conference_registry:
            errors.append(
                f"conference-membership.csv line {line_number}: conference_key "
                f"{key!r} is absent from conferences.csv."
            )

    for history_path in sorted((repo_root / "schools").glob("*/conferences.csv")):
        history_columns, history_rows = read_csv(history_path)
        require_columns(history_path, history_columns, REQUIRED_HISTORY_COLUMNS, errors)
        expected_program_key = history_path.parent.name
        for problem in history_errors(
            history_rows,
            set(conference_registry),
            expected_program_key=expected_program_key,
        ):
            errors.append(f"{history_path}: {problem}")

    canonical_ids = [r.get("canonical_game_id", "") for r in canonical_rows]
    canonical_id_set = set(canonical_ids)

    if "" in canonical_id_set:
        errors.append("Canonical games contain blank canonical_game_id values.")

    dupes = duplicates(canonical_ids)
    if dupes:
        errors.append(f"Duplicate canonical_game_id values: {', '.join(sorted(dupes)[:10])}")

    for line_num, row in enumerate(canonical_rows, start=2):
        game_id = row.get("canonical_game_id", f"row {line_num}")
        team_a = row.get("team_a_key", "")
        team_b = row.get("team_b_key", "")

        if not team_a or not team_b:
            errors.append(f"{game_id}: team_a_key and team_b_key are required.")
        elif team_a >= team_b:
            errors.append(
                f"{game_id}: team keys must be alphabetically ordered and distinct "
                f"(got {team_a!r}, {team_b!r})."
            )

        site_type = row.get("site_type", "")
        if site_type not in ALLOWED_SITE_TYPES:
            errors.append(f"{game_id}: invalid site_type {site_type!r}.")

        game_type = row.get("game_type", "")
        if game_type not in ALLOWED_GAME_TYPES:
            errors.append(f"{game_id}: invalid game_type {game_type!r}.")

        postseason_round = row.get("postseason_round", "")
        if postseason_round not in ALLOWED_POSTSEASON_ROUNDS:
            errors.append(f"{game_id}: invalid postseason_round {postseason_round!r}.")

        status = row.get("canonical_status", "")
        if status not in ALLOWED_CANONICAL_STATUSES:
            errors.append(f"{game_id}: invalid canonical_status {status!r}.")

        administrative_status = row.get("administrative_status", "")
        if administrative_status not in ALLOWED_ADMINISTRATIVE_STATUSES:
            errors.append(
                f"{game_id}: invalid administrative_status {administrative_status!r}."
            )

        score_a = row.get("team_a_score", "").strip()
        score_b = row.get("team_b_score", "").strip()
        result_winner = row.get("result_winner_team_key", "").strip()

        if bool(score_a) != bool(score_b):
            errors.append(
                f"{game_id}: team_a_score and team_b_score must either both be known "
                "or both be blank."
            )

        if result_winner and result_winner not in {team_a, team_b}:
            errors.append(
                f"{game_id}: result_winner_team_key must be blank or one of the two "
                f"participants (got {result_winner!r})."
            )

        if score_a and score_b:
            try:
                score_a_int = int(score_a)
                score_b_int = int(score_b)
            except ValueError:
                errors.append(
                    f"{game_id}: scores must be integer values or blank "
                    f"(got {score_a!r}-{score_b!r})."
                )
            else:
                expected_winner = (
                    team_a
                    if score_a_int > score_b_int
                    else team_b
                    if score_b_int > score_a_int
                    else ""
                )
                if result_winner != expected_winner:
                    errors.append(
                        f"{game_id}: result_winner_team_key={result_winner!r} does not "
                        f"match the scored result {score_a}-{score_b}; expected "
                        f"{expected_winner!r}."
                    )
        elif administrative_status == "FORFEIT" and not result_winner:
            errors.append(
                f"{game_id}: a scoreless FORFEIT requires result_winner_team_key."
            )

        designated_home = row.get("designated_home_team_key", "")
        if site_type == "TEAM_A_HOME" and designated_home != team_a:
            errors.append(
                f"{game_id}: TEAM_A_HOME requires designated_home_team_key={team_a!r}."
            )
        elif site_type == "TEAM_B_HOME" and designated_home != team_b:
            errors.append(
                f"{game_id}: TEAM_B_HOME requires designated_home_team_key={team_b!r}."
            )
        elif site_type in {"NEUTRAL", "UNKNOWN"} and designated_home:
            warnings.append(
                f"{game_id}: {site_type} has designated_home_team_key={designated_home!r}."
            )

        if game_type == "REGULAR_SEASON" and postseason_round:
            errors.append(
                f"{game_id}: REGULAR_SEASON must not have postseason_round={postseason_round!r}."
            )

        if game_type in {"CONFERENCE_TOURNAMENT", "NIT"} and postseason_round not in {"", "Championship"}:
            errors.append(
                f"{game_id}: {game_type} round must be blank or Championship."
            )

    assertion_ids = [r.get("assertion_id", "") for r in assertion_rows]
    if "" in set(assertion_ids):
        errors.append("Evidence contains blank assertion_id values.")
    dupes = duplicates(assertion_ids)
    if dupes:
        errors.append(f"Duplicate assertion_id values: {', '.join(sorted(dupes)[:10])}")

    source_identity_pairs = [
        (r.get("source_program_key", ""), r.get("source_game_id", ""))
        for r in assertion_rows
    ]
    dupes_source = duplicates([f"{a}::{b}" for a, b in source_identity_pairs])
    if dupes_source:
        errors.append(
            "Duplicate source_program_key/source_game_id evidence pairs: "
            + ", ".join(sorted(dupes_source)[:10])
        )

    missing_assertion_refs = sorted({
        r.get("canonical_game_id", "")
        for r in assertion_rows
        if r.get("canonical_game_id", "") not in canonical_id_set
    })
    if missing_assertion_refs:
        errors.append(
            "Evidence references missing canonical games: "
            + ", ".join(missing_assertion_refs[:10])
        )

    assertions_by_source = defaultdict(list)
    assertions_by_game = defaultdict(list)
    for row in assertion_rows:
        assertions_by_source[
            (
                row.get("source_program_key", "").strip(),
                row.get("source_game_id", "").strip(),
            )
        ].append(row)
        assertions_by_game[row.get("canonical_game_id", "").strip()].append(row)

    # Source packages are curated inputs; global assertions are deterministic
    # evidence copies. Legacy drift is summarized rather than made fatal.
    schools_root = repo_root / "schools"
    if schools_root.exists():
        for source_path in sorted(schools_root.glob("*/source-games.csv")):
            program = source_path.parent.name
            _, source_rows = read_csv(source_path)
            drift_rows = 0
            drift_fields = Counter()
            for source in source_rows:
                pair = (
                    source.get("source_program_key", "").strip(),
                    source.get("source_game_id", "").strip(),
                )
                linked = assertions_by_source.get(pair, [])
                if len(linked) != 1:
                    continue
                drift = assertion_drift(source, linked[0])
                if drift:
                    drift_rows += 1
                    drift_fields.update(drift.keys())
            if drift_rows:
                warnings.append(
                    f"{program}: {drift_rows:,} legacy source/assertion rows drift "
                    f"({', '.join(f'{field}={count:,}' for field, count in sorted(drift_fields.items()))}); "
                    "run ingest_school.py --check-package for target-team enforcement."
                )

            local_assertions_path = source_path.parent / "game-assertions.csv"
            if local_assertions_path.exists():
                _, local_rows = read_csv(local_assertions_path)
                local_by_source = defaultdict(list)
                for assertion in local_rows:
                    local_by_source[
                        (
                            assertion.get("source_program_key", "").strip(),
                            assertion.get("source_game_id", "").strip(),
                        )
                    ].append(assertion)
                local_drift_rows = 0
                local_drift_fields = Counter()
                for source in source_rows:
                    pair = (
                        source.get("source_program_key", "").strip(),
                        source.get("source_game_id", "").strip(),
                    )
                    linked = local_by_source.get(pair, [])
                    if len(linked) != 1:
                        continue
                    drift = assertion_drift(source, linked[0])
                    if drift:
                        local_drift_rows += 1
                        local_drift_fields.update(drift.keys())
                if local_drift_rows:
                    warnings.append(
                        f"{program}: {local_drift_rows:,} legacy source/local-assertion "
                        f"rows drift ({', '.join(f'{field}={count:,}' for field, count in sorted(local_drift_fields.items()))}); "
                        "run ingest_school.py --check-package for target-team enforcement."
                    )

    discrepancy_ids = [r.get("discrepancy_id", "") for r in discrepancy_rows]
    if "" in set(discrepancy_ids):
        errors.append("Reconciliation data contains blank discrepancy_id values.")
    dupes = duplicates(discrepancy_ids)
    if dupes:
        errors.append(f"Duplicate discrepancy_id values: {', '.join(sorted(dupes)[:10])}")

    missing_discrepancy_refs = sorted({
        r.get("canonical_game_id", "")
        for r in discrepancy_rows
        if r.get("canonical_game_id", "") not in canonical_id_set
    })
    if missing_discrepancy_refs:
        errors.append(
            "Discrepancies reference missing canonical games: "
            + ", ".join(missing_discrepancy_refs[:10])
        )

    # Reference-layer validation
    program_keys = [r.get("program_key", "") for r in program_rows]
    program_key_set = set(program_keys)

    if "" in program_key_set:
        errors.append("Reference programs contain blank program_key values.")

    dupes = duplicates(program_keys)
    if dupes:
        errors.append(
            f"Duplicate program_key values: {', '.join(sorted(dupes)[:10])}"
        )

    canonical_team_keys = {
        key
        for row in canonical_rows
        for key in (row.get("team_a_key", ""), row.get("team_b_key", ""))
        if key
    }

    for line_num, row in enumerate(program_rows, start=2):
        program_key = row.get("program_key", "")
        label = program_key or f"programs.csv row {line_num}"

        for field in ("program_name", "display_name", "nickname"):
            if not row.get(field, "").strip():
                errors.append(f"{label}: {field} is required.")

        current_d1 = row.get("current_d1", "")
        public_page_enabled = row.get("public_page_enabled", "")

        if current_d1 not in ALLOWED_YES_NO:
            errors.append(
                f"{label}: current_d1 must be Yes or No "
                f"(got {current_d1!r})."
            )

        if public_page_enabled not in ALLOWED_YES_NO:
            errors.append(
                f"{label}: public_page_enabled must be Yes or No "
                f"(got {public_page_enabled!r})."
            )

        if public_page_enabled == "Yes" and current_d1 != "Yes":
            errors.append(
                f"{label}: public_page_enabled=Yes requires current_d1=Yes."
            )

        for field in PROGRAM_ACHIEVEMENT_FIELDS:
            value = row.get(field, "").strip()

            if not value:
                if public_page_enabled == "Yes":
                    errors.append(
                        f"{label}: {field} is required when "
                        "public_page_enabled=Yes."
                    )
                continue

            if not re.fullmatch(r"\d+", value):
                errors.append(
                    f"{label}: {field} must be a nonnegative integer "
                    f"(got {value!r})."
                )

        if public_page_enabled == "Yes" and program_key not in canonical_team_keys:
            errors.append(
                f"{label}: public page is enabled but program does not appear "
                "in canonical games."
            )

    membership_keys = [
        f"{r.get('program_key', '')}::{r.get('season_label', '')}"
        for r in membership_rows
    ]
    dupes = duplicates(membership_keys)
    if dupes:
        errors.append(
            "Duplicate program/season conference memberships: "
            + ", ".join(sorted(dupes)[:10])
        )

    memberships_by_season_program: dict[tuple[str, str], dict[str, str]] = {}

    for line_num, row in enumerate(membership_rows, start=2):
        program_key = row.get("program_key", "")
        season_label = row.get("season_label", "")
        conference_key = row.get("conference_key", "")
        conference_name = row.get("conference_name", "")
        label = (
            f"{program_key}/{season_label}"
            if program_key or season_label
            else f"conference-membership.csv row {line_num}"
        )

        if not program_key:
            errors.append(f"{label}: program_key is required.")
        elif program_key not in program_key_set:
            errors.append(
                f"{label}: program_key {program_key!r} does not exist "
                "in programs.csv."
            )

        if not valid_season_label(season_label):
            errors.append(
                f"{label}: invalid season_label {season_label!r}; "
                "expected consecutive YYYY-YYYY."
            )

        if not conference_key:
            errors.append(f"{label}: conference_key is required.")
        if not conference_name:
            errors.append(f"{label}: conference_name is required.")

        if program_key and season_label:
            memberships_by_season_program[(program_key, season_label)] = row

    # The reference registry is presently a 2026-2027 current-D1 snapshot.
    # Every current D1 program must have exactly one conference row for that season.
    CURRENT_REFERENCE_SEASON = "2026-2027"
    for row in program_rows:
        program_key = row.get("program_key", "")
        if row.get("current_d1", "") == "Yes":
            if (program_key, CURRENT_REFERENCE_SEASON) not in memberships_by_season_program:
                errors.append(
                    f"{program_key}: current_d1=Yes requires a "
                    f"{CURRENT_REFERENCE_SEASON} conference membership."
                )

    # Venue registries must use atomic locations, and a stable venue identity
    # must not silently acquire incompatible public geography across packages.
    registry_rows: list[tuple[str, dict[str, str]]] = []
    registry_keys_by_program: dict[str, set[str]] = defaultdict(set)
    registry_rows_by_program_key: dict[
        tuple[str, str], list[dict[str, str]]
    ] = defaultdict(list)
    registry_name_keys_by_program: dict[
        str, dict[str, str]
    ] = defaultdict(dict)
    if schools_root.exists():
        for venue_path in sorted(schools_root.glob("*/venues.csv")):
            _, venue_rows = read_csv(venue_path)
            program = venue_path.parent.name
            for line_number, row in enumerate(venue_rows, start=2):
                registry_rows.append((str(venue_path.relative_to(repo_root)), row))
                key = row.get("venue_key", "").strip()
                if key:
                    registry_keys_by_program[program].add(key)
                    registry_rows_by_program_key[(program, key)].append(row)
                    names = [row.get("canonical_name", "")]
                    names.extend(row.get("aliases", "").split(";"))
                    for name in names:
                        if name.strip():
                            registry_name_keys_by_program[program][
                                name.strip().casefold()
                            ] = key
                if location_pair_status(
                    row.get("city", ""), row.get("state", "")
                ) == "partial":
                    errors.append(
                        f"{venue_path.relative_to(repo_root)}:{line_number}: "
                        "venue city/state must be both populated or both blank."
                    )
    errors.extend(venue_location_conflicts(registry_rows))

    # Future registry-derived enrichment records an auditable marker in the
    # existing canonical notes field. Validate all such markers end to end.
    for row in canonical_rows:
        game_id = row.get("canonical_game_id", "")
        notes = row.get("notes", "")
        markers = parse_registry_fallback_markers(notes)
        if notes.count(REGISTRY_FALLBACK_PREFIX) != len(markers):
            errors.append(
                f"{game_id}: malformed VENUE_REGISTRY_FALLBACK marker in notes."
            )
        for marker in markers:
            source_pair = (
                marker["source_program_key"], marker["source_game_id"]
            )
            linked = [
                assertion
                for assertion in assertions_by_source.get(source_pair, [])
                if assertion.get("canonical_game_id", "") == game_id
            ]
            if len(linked) != 1:
                errors.append(
                    f"{game_id}: registry fallback marker does not resolve to "
                    f"one linked assertion for {source_pair[0]}/{source_pair[1]}."
                )
            else:
                curated_venue = linked[0].get("curated_venue_name", "").strip()
                resolved_key = registry_name_keys_by_program.get(
                    marker["source_program_key"], {}
                ).get(curated_venue.casefold(), "")
                if not curated_venue or resolved_key != marker["venue_key"]:
                    errors.append(
                        f"{game_id}: registry fallback marker is not backed by "
                        "the linked assertion's curated venue identity."
                    )
                if not source_site_agrees_with_canonical(linked[0], row):
                    errors.append(
                        f"{game_id}: registry fallback marker lacks independent "
                        "source/canonical site-type agreement."
                    )
            if marker["venue_key"] not in registry_keys_by_program.get(
                marker["source_program_key"], set()
            ):
                errors.append(
                    f"{game_id}: registry fallback marker venue_key "
                    f"{marker['venue_key']!r} is absent from "
                    f"schools/{marker['source_program_key']}/venues.csv."
                )
            if marker["site_type"] == "UNKNOWN":
                errors.append(
                    f"{game_id}: registry fallback marker cannot use UNKNOWN site_type."
                )
            elif marker["site_type"] != row.get("site_type", "").strip():
                errors.append(
                    f"{game_id}: registry fallback marker site_type "
                    f"{marker['site_type']!r} does not match canonical site_type."
                )
            allowed_fields = {"venue_key", "site_city", "site_state"}
            fields = set(marker["fields"].split(","))
            if not fields or not fields <= allowed_fields:
                errors.append(
                    f"{game_id}: registry fallback marker has invalid fields "
                    f"{marker['fields']!r}."
                )
                continue
            if (
                "venue_key" in fields
                and row.get("venue_key", "").strip() != marker["venue_key"]
            ):
                errors.append(
                    f"{game_id}: registry-derived canonical venue_key no longer "
                    "matches its provenance marker."
                )
            if fields & {"site_city", "site_state"}:
                registry_entries = registry_rows_by_program_key.get(
                    (marker["source_program_key"], marker["venue_key"]), []
                )
                registry_locations = {
                    (
                        entry.get("city", "").strip(),
                        entry.get("state", "").strip(),
                    )
                    for entry in registry_entries
                    if location_pair_status(
                        entry.get("city", ""), entry.get("state", "")
                    ) == "complete"
                }
                canonical_location = (
                    row.get("site_city", "").strip(),
                    row.get("site_state", "").strip(),
                )
                if len(registry_locations) != 1 or canonical_location not in registry_locations:
                    errors.append(
                        f"{game_id}: registry-derived canonical location is not "
                        "traceable to one complete matching registry row."
                    )

    # Report
    print("College Basketball History — data validation")
    print(f"Repository: {repo_root}")
    print()
    print(f"Canonical games:      {len(canonical_rows):,}")
    print(f"Source assertions:    {len(assertion_rows):,}")
    print(f"Discrepancies:        {len(discrepancy_rows):,}")
    print(f"Reference programs:   {len(program_rows):,}")
    print(f"Conference rows:      {len(membership_rows):,}")
    print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for warning in warnings[:20]:
            print(f"  - {warning}")
        if len(warnings) > 20:
            print(f"  ... {len(warnings) - 20} more")
        print()

    if errors:
        print(f"FAIL ({len(errors)} errors):")
        for error in errors[:50]:
            print(f"  - {error}")
        if len(errors) > 50:
            print(f"  ... {len(errors) - 50} more")
        return 1

    print("PASS: core canonical, evidence, reconciliation, and reference layers are structurally valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
