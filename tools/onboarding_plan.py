#!/usr/bin/env python3
"""Plan, seal, and apply owner-reviewed school-onboarding decisions.

This module is intentionally repository-specific.  It turns the existing safe
ingestion primitives into a human-reviewable plan without weakening any of the
project's historical stop rules.

The public CLI is ``tools/onboard_school.py``.  Keeping the plan mechanics here
makes the date-reporting and approval contract directly unit-testable.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import ingest_school
from conference_reference import history_errors, registry_by_key
from location_safety import (
    append_note,
    assertion_drift,
    location_pair_status,
    registry_fallback_marker,
    retire_site_mismatched_registry_fallbacks,
    source_location_preflight,
)
from program_history import (
    derive_ncaa_accomplishments,
    history_scope_errors,
    partition_source_rows,
)


WORKFLOW_VERSION = 1
PLAN_SCHEMA_VERSION = 1
REQUIRED_PACKAGE_FILES = (
    "source-games.csv",
    "opponents.csv",
    "venues.csv",
    "conferences.csv",
    "notes.md",
    "source-notes.md",
)

REVIEW_COLUMNS = (
    "decision_id",
    "category",
    "source_game_id",
    "season_label",
    "source_game_date",
    "canonical_game_date",
    "matchup",
    "field_name",
    "source_value",
    "canonical_value",
    "relevant_evidence",
    "recommended_action",
    "allowed_actions",
    "decision",
    "resolution_basis",
    "canonical_patch_json",
    "source_patch_json",
    "notes",
)

DISCREPANCY_ACTIONS = {
    "KEEP_CANONICAL",
    "USE_SOURCE",
    "NORMALIZE_SOURCE_TO_CANONICAL",
    "LEAVE_UNRESOLVED",
}
ACCOMPLISHMENT_ACTIONS = {
    "VERIFY_REFERENCE_VALUES",
    "KEEP_UNDER_REVIEW",
}
PUBLICATION_ACTIONS = {"ENABLE_PUBLIC_PAGE", "KEEP_DISABLED"}

SOURCE_ASSERTION_COPY_FIELDS = tuple(
    field
    for field in ingest_school.ASSERTION_FIELDS
    if field not in {"assertion_id", "canonical_game_id", "match_status", "match_method"}
)

CANONICAL_PATCH_FIELDS = {
    "game_date",
    "date_precision",
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
SOURCE_PATCH_FIELDS = set(SOURCE_ASSERTION_COPY_FIELDS) - {
    "source_program_key",
    "source_game_id",
    "raw_text",
}


class WorkflowError(RuntimeError):
    """A safe, user-correctable onboarding stop."""


def read_csv_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def read_csv(path: Path) -> list[dict[str, str]]:
    return read_csv_table(path)[1]


def write_csv_preserving_format(
    path: Path,
    fieldnames: list[str] | tuple[str, ...],
    rows: Iterable[dict[str, str]],
) -> None:
    original = path.read_bytes() if path.exists() else b""
    has_bom = original.startswith(b"\xef\xbb\xbf")
    line_ending = "\r\n" if b"\r\n" in original else "\n"
    encoding = "utf-8-sig" if has_bom else "utf-8"
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding=encoding) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(fieldnames),
            lineterminator=line_ending,
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    temporary.replace(path)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def plan_input_paths(repo: Path, school_key: str) -> list[Path]:
    school = repo / "schools" / school_key
    paths = [school / name for name in REQUIRED_PACKAGE_FILES]
    paths.extend(
        [
            repo / "data/canonical/games.csv",
            repo / "data/evidence/game-assertions.csv",
            repo / "data/reconciliation/discrepancies.csv",
            repo / "data/reference/programs.csv",
            repo / "data/reference/program-accomplishments.csv",
            repo / "data/reference/conference-membership.csv",
            repo / "data/reference/conferences.csv",
            repo / "tools/build_site_data.py",
            repo / "tools/conference_reference.py",
            repo / "tools/ingest_school.py",
            repo / "tools/location_safety.py",
            repo / "tools/onboard_school.py",
            repo / "tools/onboarding_plan.py",
            repo / "tools/program_history.py",
            repo / "tools/validate_data.py",
            repo / "tools/verify_program_accomplishments.py",
        ]
    )
    return paths


def input_fingerprint(repo: Path, school_key: str) -> dict[str, Any]:
    entries: dict[str, str] = {}
    for path in plan_input_paths(repo, school_key):
        relative = path.relative_to(repo).as_posix()
        entries[relative] = sha256_file(path) if path.is_file() else "MISSING"
    try:
        git_head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        git_head = "[not-a-git-worktree]"
    digest = sha256_text(
        canonical_json(
            {
                "workflow_version": WORKFLOW_VERSION,
                "school_key": school_key,
                "git_head": git_head,
                "files": entries,
            }
        )
    )
    return {"sha256": digest, "git_head": git_head, "files": entries}


def _season_is_valid(value: str) -> bool:
    match = re.fullmatch(r"(\d{4})-(\d{4})", value)
    return bool(match and int(match.group(2)) == int(match.group(1)) + 1)


def validate_package(repo: Path, school_key: str) -> dict[str, Any]:
    """Run the permanent equivalent of the former pasted package-QA snippet."""

    school = repo / "schools" / school_key
    errors: list[str] = []
    warnings: list[str] = []
    missing = [name for name in REQUIRED_PACKAGE_FILES if not (school / name).is_file()]
    if missing:
        return {
            "errors": ["Missing package files: " + ", ".join(missing)],
            "warnings": [],
            "counts": {},
        }

    game_fields, games = read_csv_table(school / "source-games.csv")
    _, opponents = read_csv_table(school / "opponents.csv")
    _, venues = read_csv_table(school / "venues.csv")
    _, conferences = read_csv_table(school / "conferences.csv")

    required_game_fields = {
        "source_game_id",
        "source_program_key",
        "season_label",
        "game_date",
        "normalized_opponent_key",
        "normalized_opponent_name",
        "team_score",
        "opponent_score",
        "played_result",
        "overtime_periods",
        "curated_site_type",
        "curated_game_type",
        "curated_postseason_round",
        "raw_text",
    }
    for field in sorted(required_game_fields - set(game_fields)):
        errors.append(f"source-games.csv missing column: {field}")

    source_ids = [row.get("source_game_id", "").strip() for row in games]
    if any(not value for value in source_ids):
        errors.append("source-games.csv contains a blank source_game_id")
    duplicates = sorted(
        value for value, count in Counter(source_ids).items() if value and count > 1
    )
    if duplicates:
        errors.append("Duplicate source_game_id values: " + ", ".join(duplicates[:10]))

    opponent_keys = {
        row.get("canonical_opponent_key", "").strip()
        for row in opponents
        if row.get("canonical_opponent_key", "").strip()
    }
    venue_names: set[str] = set()
    for row in venues:
        canonical_name = row.get("canonical_name", "").strip().casefold()
        if canonical_name:
            venue_names.add(canonical_name)
        for alias in row.get("aliases", "").split(";"):
            alias = alias.strip().casefold()
            if alias:
                venue_names.add(alias)
        if row.get("source_program_key", "").strip() not in {"", school_key}:
            errors.append(
                "venues.csv contains a row for another source program: "
                + row.get("source_program_key", "")
            )
        if location_pair_status(row.get("city", ""), row.get("state", "")) == "partial":
            errors.append(
                f"venue {row.get('venue_key', '[blank]')}: city/state must be both populated or both blank"
            )

    allowed_sites = {"SOURCE_PROGRAM_HOME", "OPPONENT_HOME", "NEUTRAL", "UNKNOWN"}
    allowed_types = {"REGULAR_SEASON", "CONFERENCE_TOURNAMENT", "NCAA_TOURNAMENT", "NIT", "POSTSEASON"}
    allowed_rounds = {
        "",
        "Play-in",
        "R64",
        "R32",
        "Sweet Sixteen",
        "Elite Eight",
        "Final Four",
        "Championship",
    }

    for line_number, row in enumerate(games, start=2):
        label = row.get("source_game_id", "").strip() or f"line {line_number}"
        if row.get("source_program_key", "").strip() != school_key:
            errors.append(f"{label}: wrong source_program_key")
        season = row.get("season_label", "").strip()
        if not _season_is_valid(season):
            errors.append(f"{label}: invalid season_label {season!r}")
        game_date = row.get("game_date", "").strip()
        if game_date:
            try:
                dt.date.fromisoformat(game_date)
            except ValueError:
                errors.append(f"{label}: invalid ISO game_date {game_date!r}")

        opponent = row.get("normalized_opponent_key", "").strip()
        if not opponent:
            errors.append(f"{label}: blank normalized_opponent_key")
        elif opponent not in opponent_keys:
            errors.append(f"{label}: opponent key {opponent!r} absent from opponents.csv")

        team_score = row.get("team_score", "").strip()
        opponent_score = row.get("opponent_score", "").strip()
        if bool(team_score) != bool(opponent_score):
            errors.append(f"{label}: only one score is populated")
        if team_score and opponent_score:
            try:
                team_number = int(team_score)
                opponent_number = int(opponent_score)
            except ValueError:
                errors.append(f"{label}: score is not an integer")
            else:
                expected = (
                    "W" if team_number > opponent_number else "L" if opponent_number > team_number else "T"
                )
                played = row.get("played_result", "").strip().upper()
                if played and played != expected:
                    warnings.append(
                        f"{label}: score implies {expected}, curated result says {played}"
                    )

        overtime = row.get("overtime_periods", "").strip()
        if overtime and (not overtime.isdigit() or int(overtime) < 0):
            errors.append(f"{label}: invalid overtime_periods {overtime!r}")
        site = row.get("curated_site_type", "").strip().upper()
        if site not in allowed_sites:
            errors.append(f"{label}: invalid curated_site_type {site!r}")
        if location_pair_status(row.get("city", ""), row.get("state", "")) == "partial":
            errors.append(f"{label}: normalized city/state must be both populated or both blank")
        city = row.get("city", "").strip()
        if city.casefold() in venue_names:
            errors.append(f"{label}: normalized city contains a venue name")
        if " and " in city.casefold():
            errors.append(f"{label}: normalized city contains a combined multi-city value")

        game_type = row.get("curated_game_type", "").strip()
        round_name = row.get("curated_postseason_round", "").strip()
        if game_type not in allowed_types:
            errors.append(f"{label}: invalid curated_game_type {game_type!r}")
        if round_name not in allowed_rounds:
            errors.append(f"{label}: invalid curated_postseason_round {round_name!r}")
        if game_type == "REGULAR_SEASON" and round_name:
            errors.append(f"{label}: regular-season game has a postseason round")
        if game_type in {"CONFERENCE_TOURNAMENT", "NIT", "POSTSEASON"} and round_name not in {"", "Championship"}:
            errors.append(f"{label}: {game_type} round must be blank or Championship")

        venue = row.get("curated_venue_name", "").strip()
        if venue and venue.casefold() not in venue_names:
            errors.append(f"{label}: curated venue {venue!r} absent from venues.csv")
        audit_text = " ".join(
            [row.get("raw_text", ""), row.get("event_or_tournament", ""), row.get("notes", "")]
        ).casefold()
        if "exhib" in audit_text:
            warnings.append(f"{label}: exhibition-like wording requires manual confirmation")

    for filename, rows in (("opponents.csv", opponents), ("conferences.csv", conferences)):
        for line_number, row in enumerate(rows, start=2):
            value = row.get("source_program_key", "").strip()
            if value and value != school_key:
                errors.append(f"{filename} line {line_number}: wrong source_program_key {value!r}")

    programs = read_csv(repo / "data/reference/programs.csv")
    target_programs = [row for row in programs if row.get("program_key") == school_key]
    if len(target_programs) != 1:
        errors.append("Target must have exactly one programs.csv row")
    else:
        errors.extend(
            f"history scope: {problem}"
            for problem in history_scope_errors(target_programs[0], required=True)
        )

    conference_registry = registry_by_key(read_csv(repo / "data/reference/conferences.csv"))
    errors.extend(
        f"conferences.csv {problem}"
        for problem in history_errors(
            conferences,
            set(conference_registry),
            expected_program_key=school_key,
        )
    )

    return {
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "source_games": len(games),
            "opponents": len(opponents),
            "venues": len(venues),
            "conference_intervals": len(conferences),
        },
    }


def _decision_id(category: str, *parts: str) -> str:
    raw = "-".join((category, *parts)).upper()
    return re.sub(r"[^A-Z0-9._-]+", "-", raw).strip("-")


def _canonical_value(row: dict[str, str], field_name: str) -> str:
    if field_name == "score":
        return f"{row.get('team_a_score', '')}-{row.get('team_b_score', '')}"
    return row.get(field_name, "")


def _assertion_value(
    assertion: dict[str, str],
    canonical: dict[str, str],
    field_name: str,
) -> str:
    if field_name == "score":
        score_a, score_b = ingest_school.source_scores_in_canonical_orientation(assertion)
        return f"{score_a}-{score_b}"
    if field_name == "site_type":
        return ingest_school.source_site_to_canonical(assertion)[0]
    if field_name == "game_type":
        return assertion.get("curated_game_type", "")
    if field_name == "result_winner_team_key":
        known, winner = ingest_school.source_result_winner(assertion)
        return (winner or "[TIE]") if known else "[UNKNOWN]"
    return assertion.get(field_name, "")


def _date_fields(source_date: str, canonical_date: str) -> dict[str, str]:
    """Dates are always separate; a date conflict can never hide behind one label."""

    return {
        "source_game_date": source_date or "[unknown]",
        "canonical_game_date": canonical_date or "[unknown]",
    }


def date_label(item: dict[str, Any]) -> str:
    source_date = str(item.get("source_game_date", "") or "[unknown]")
    canonical_date = str(item.get("canonical_game_date", "") or "[unknown]")
    if source_date == canonical_date:
        return f"Date: {source_date}"
    return f"Dates: source {source_date}; canonical {canonical_date}"


def _identity_candidates(
    candidates: list[dict[str, str]],
    assertions_by_game: dict[str, list[dict[str, str]]],
) -> tuple[str, str, str]:
    ids = ";".join(row["canonical_game_id"] for row in candidates) or "[none]"
    dates = ";".join(row.get("game_date", "") or "[unknown]" for row in candidates) or "[none]"
    evidence: list[str] = []
    for candidate in candidates:
        programs = sorted(
            {
                row.get("source_program_key", "")
                for row in assertions_by_game.get(candidate["canonical_game_id"], [])
                if row.get("source_program_key", "")
            }
        )
        evidence.append(
            f"{candidate['canonical_game_id']} {candidate.get('game_date') or '[unknown]'} "
            f"{candidate.get('team_a_score','')}-{candidate.get('team_b_score','')} "
            f"sources={','.join(programs) or '[none]'}"
        )
    return ids, dates, "; ".join(evidence)


def _accomplishment_conflicts(
    program: dict[str, str],
    reference: dict[str, str],
    canonical_games: list[dict[str, str]],
) -> tuple[dict[str, Any], list[str]]:
    derived = derive_ncaa_accomplishments(
        canonical_games,
        program["program_key"],
        program.get("history_start_season", "").strip(),
    )
    comparisons = {
        "ncaa_tournament_appearances": str(derived["ncaa_tournament_appearances"]),
        "final_four_appearances": str(derived["final_four_appearances"]),
        "national_championships": str(derived["national_championships"]),
        "best_finish_key": derived["best_finish_key"] or "",
        "best_finish_year": (
            str(derived["best_finish_year"])
            if derived["best_finish_year"] is not None
            else ""
        ),
    }
    conflicts = [
        f"{field}: reference={reference.get(field, '')!r}, canonical={value!r}"
        for field, value in comparisons.items()
        if reference.get(field, "").strip() != value
    ]
    conflicts.extend(derived["incomplete_reasons"])
    return derived, conflicts


def build_plan(repo: Path, school_key: str) -> dict[str, Any]:
    repo = repo.resolve()
    package = validate_package(repo, school_key)
    blockers = list(package["errors"])
    warnings = list(package["warnings"])
    if blockers:
        return {
            "schema_version": PLAN_SCHEMA_VERSION,
            "workflow_version": WORKFLOW_VERSION,
            "school_key": school_key,
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "input_fingerprint": input_fingerprint(repo, school_key),
            "package": package,
            "blockers": blockers,
            "warnings": warnings,
            "summary": {},
            "decisions": [],
        }

    source_path = repo / "schools" / school_key / "source-games.csv"
    all_sources = read_csv(source_path)
    programs = read_csv(repo / "data/reference/programs.csv")
    program = next(row for row in programs if row["program_key"] == school_key)
    sources, pre_cutoff = partition_source_rows(
        all_sources,
        program["history_start_season"].strip(),
    )
    canonical = read_csv(repo / "data/canonical/games.csv")
    assertions = read_csv(repo / "data/evidence/game-assertions.csv")
    discrepancies = read_csv(repo / "data/reconciliation/discrepancies.csv")
    accomplishments = read_csv(repo / "data/reference/program-accomplishments.csv")
    accomplishment = next(
        (row for row in accomplishments if row.get("program_key") == school_key),
        None,
    )
    if accomplishment is None:
        blockers.append("Target has no program-accomplishments.csv row")

    canonical_by_id = {row["canonical_game_id"]: row for row in canonical}
    canonical_index: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in canonical:
        canonical_index[(row["team_a_key"], row["team_b_key"], row["season_label"])].append(row)

    assertions_by_source: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    assertions_by_game: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertions:
        assertions_by_source[(row.get("source_program_key", ""), row.get("source_game_id", ""))].append(row)
        assertions_by_game[row.get("canonical_game_id", "")].append(row)

    existing_pairs = set(assertions_by_source)
    venue_name_map = ingest_school.load_venue_name_map(
        repo / "schools" / school_key / "venues.csv"
    )
    venue_names = set(venue_name_map)
    location_errors, location_warnings = source_location_preflight(
        sources,
        existing_pairs,
        venue_names,
    )
    blockers.extend(location_errors)
    warnings.extend(location_warnings)

    sync_errors: list[str] = []
    for source in sources:
        pair = (school_key, source.get("source_game_id", ""))
        linked = assertions_by_source.get(pair, [])
        if len(linked) == 1:
            drift = assertion_drift(source, linked[0])
            if drift:
                sync_errors.append(
                    f"{pair[1]}: global assertion differs in {', '.join(sorted(drift))}"
                )
        elif len(linked) > 1:
            sync_errors.append(f"{pair[1]}: multiple global assertions exist")
    if sync_errors:
        blockers.extend(sync_errors)

    existing_discrepancy_keys = {
        (
            row.get("canonical_game_id", ""),
            row.get("field_name", ""),
            row.get("source_a_program_key", ""),
        )
        for row in discrepancies
    }

    decisions: list[dict[str, Any]] = []
    identity_counts = Counter()
    predicted_conflicts = 0
    conditional_conflicts = 0
    predicted_enrichment_fields = 0
    predicted_enrichment_games: set[str] = set()
    affected_public_programs: set[str] = set()
    public_keys = {
        row["program_key"]
        for row in programs
        if row.get("public_page_enabled") == "Yes"
    }
    venue_metadata = ingest_school.load_venue_metadata_map(
        repo / "schools" / school_key / "venues.csv"
    )

    for source in sources:
        opponent = source.get("normalized_opponent_key", "").strip()
        if opponent in public_keys:
            affected_public_programs.add(opponent)
        season = source.get("season_label", "").strip()
        team_a, team_b = ingest_school.ordered_pair(school_key, opponent)
        candidates = canonical_index.get((team_a, team_b, season), [])
        pair = (school_key, source.get("source_game_id", ""))
        prior_ids = sorted(
            {
                row.get("canonical_game_id", "").strip()
                for row in assertions_by_source.get(pair, [])
                if row.get("canonical_game_id", "").strip()
            }
        )
        if len(prior_ids) == 1:
            status, game_id, method = ingest_school.CONFIDENT, prior_ids[0], "EXISTING_SOURCE_ASSERTION"
        elif len(prior_ids) > 1:
            status, game_id, method = ingest_school.REVIEW, "", "SOURCE_ASSERTION_LINKS_MULTIPLE_CANONICAL_GAMES"
        else:
            override = ingest_school.resolve_identity_override(
                source,
                candidates,
                assertions_by_source,
                canonical_by_id,
            )
            status, game_id, method = override or ingest_school.identify_game(source, candidates)
        identity_counts[status] += 1

        if status == ingest_school.REVIEW:
            if method == "SOURCE_ASSERTION_LINKS_MULTIPLE_CANONICAL_GAMES":
                blockers.append(
                    f"{source.get('source_game_id','')}: one source row is already linked "
                    "to multiple canonical games; repair evidence identity before approval"
                )
                continue
            candidate_ids, candidate_dates, evidence = _identity_candidates(
                candidates,
                assertions_by_game,
            )
            allowed = [f"MATCH_CANONICAL:{row['canonical_game_id']}" for row in candidates]
            allowed.append("FORCE_NEW")
            decisions.append(
                {
                    "decision_id": _decision_id("IDENTITY", source.get("source_game_id", "")),
                    "category": "identity",
                    "source_game_id": source.get("source_game_id", ""),
                    "season_label": season,
                    **_date_fields(source.get("game_date", ""), candidate_dates),
                    "matchup": f"{school_key} vs {opponent}",
                    "field_name": "game_identity",
                    "source_value": (
                        f"date={source.get('game_date') or '[unknown]'}; "
                        f"score={source.get('team_score','')}-{source.get('opponent_score','')}"
                    ),
                    "canonical_value": candidate_ids,
                    "relevant_evidence": evidence or method,
                    "recommended_action": "REVIEW_REQUIRED",
                    "allowed_actions": allowed,
                    "decision": "PENDING",
                    "resolution_basis": "",
                    "canonical_patch_json": "{}",
                    "source_patch_json": "{}",
                    "notes": method,
                }
            )
            for candidate in candidates:
                candidate_id = candidate["canonical_game_id"]
                for participant in (candidate["team_a_key"], candidate["team_b_key"]):
                    if participant != school_key and participant in public_keys:
                        affected_public_programs.add(participant)
                for (
                    field_name,
                    source_value,
                    canonical_value,
                ) in ingest_school.discrepancy_candidates(source, candidate):
                    key = (candidate_id, field_name, school_key)
                    if key in existing_discrepancy_keys:
                        continue
                    conditional_conflicts += 1
                    competing = []
                    agreement_count = 0
                    for assertion in assertions_by_game.get(candidate_id, []):
                        if assertion.get("source_program_key") == school_key:
                            continue
                        value = _assertion_value(assertion, candidate, field_name)
                        assertion_date = assertion.get("game_date", "") or "[unknown]"
                        competing.append(
                            f"{assertion.get('source_program_key','?')} "
                            f"{assertion_date}: {value or '[blank]'}"
                        )
                        if value == canonical_value:
                            agreement_count += 1
                    recommended = (
                        "KEEP_CANONICAL" if agreement_count else "LEAVE_UNRESOLVED"
                    )
                    decisions.append(
                        {
                            "decision_id": _decision_id(
                                "CONDITIONAL-DISCREPANCY",
                                source.get("source_game_id", ""),
                                candidate_id,
                                field_name,
                            ),
                            "category": "conditional_discrepancy",
                            "applies_if_identity_decision": (
                                f"MATCH_CANONICAL:{candidate_id}"
                            ),
                            "source_game_id": source.get("source_game_id", ""),
                            "canonical_game_id": candidate_id,
                            "season_label": season,
                            **_date_fields(
                                source.get("game_date", ""),
                                candidate.get("game_date", ""),
                            ),
                            "matchup": (
                                f"{candidate['team_a_key']} vs {candidate['team_b_key']}"
                            ),
                            "field_name": field_name,
                            "source_value": source_value,
                            "canonical_value": canonical_value,
                            "relevant_evidence": (
                                "; ".join(competing)
                                or "No reciprocal assertion is yet available."
                            ),
                            "recommended_action": recommended,
                            "allowed_actions": sorted(
                                DISCREPANCY_ACTIONS | {"NOT_APPLICABLE"}
                            ),
                            "decision": "PENDING",
                            "resolution_basis": "",
                            "canonical_patch_json": "{}",
                            "source_patch_json": "{}",
                            "notes": (
                                "Applies only if the owner selects this canonical "
                                "identity; otherwise approval seals it NOT_APPLICABLE."
                            ),
                        }
                    )
            continue

        if status == ingest_school.NEW_GAME:
            continue

        canonical_row = canonical_by_id[game_id]
        for participant in (canonical_row["team_a_key"], canonical_row["team_b_key"]):
            if participant != school_key and participant in public_keys:
                affected_public_programs.add(participant)

        enrichments = ingest_school.canonical_enrichment_candidates(
            source,
            canonical_row,
            venue_metadata,
        )
        if enrichments:
            predicted_enrichment_games.add(game_id)
            predicted_enrichment_fields += len(enrichments)

        for field_name, source_value, canonical_value in ingest_school.discrepancy_candidates(
            source,
            canonical_row,
        ):
            key = (game_id, field_name, school_key)
            if key in existing_discrepancy_keys:
                continue
            predicted_conflicts += 1
            competing = []
            agreement_count = 0
            for assertion in assertions_by_game.get(game_id, []):
                if assertion.get("source_program_key") == school_key:
                    continue
                value = _assertion_value(assertion, canonical_row, field_name)
                assertion_date = assertion.get("game_date", "") or "[unknown]"
                competing.append(
                    f"{assertion.get('source_program_key','?')} "
                    f"{assertion_date}: {value or '[blank]'}"
                )
                if value == canonical_value:
                    agreement_count += 1
            recommended = "KEEP_CANONICAL" if agreement_count else "LEAVE_UNRESOLVED"
            decisions.append(
                {
                    "decision_id": _decision_id(
                        "DISCREPANCY",
                        source.get("source_game_id", ""),
                        field_name,
                    ),
                    "category": "discrepancy",
                    "source_game_id": source.get("source_game_id", ""),
                    "canonical_game_id": game_id,
                    "season_label": season,
                    **_date_fields(
                        source.get("game_date", ""),
                        canonical_row.get("game_date", ""),
                    ),
                    "matchup": f"{canonical_row['team_a_key']} vs {canonical_row['team_b_key']}",
                    "field_name": field_name,
                    "source_value": source_value,
                    "canonical_value": canonical_value,
                    "relevant_evidence": "; ".join(competing) or "No reciprocal assertion is yet available.",
                    "recommended_action": recommended,
                    "allowed_actions": sorted(DISCREPANCY_ACTIONS),
                    "decision": "PENDING",
                    "resolution_basis": "",
                    "canonical_patch_json": "{}",
                    "source_patch_json": "{}",
                    "notes": "Material source/canonical conflict; raw source evidence will remain preserved.",
                }
            )

    if accomplishment is not None:
        # Cross-check the target package itself, not only the current global
        # canonical layer.  A first-time school is not present globally yet,
        # so using current canonical games would incorrectly report zero NCAA
        # history and block every legitimate onboarding.
        synthetic_target_games = [
            ingest_school.build_new_canonical(
                source,
                f"PREFLIGHT-{number:07d}",
                venue_name_map,
                venue_metadata,
            )
            for number, source in enumerate(sources, start=1)
        ]
        derived, accomplishment_conflicts = _accomplishment_conflicts(
            program,
            accomplishment,
            synthetic_target_games,
        )
        if accomplishment_conflicts:
            blockers.append(
                "Accomplishment reference conflicts with canonical cross-check: "
                + "; ".join(accomplishment_conflicts)
            )
        elif (
            accomplishment.get("verification_status") != "VERIFIED"
            or accomplishment.get("canonical_crosscheck_status") != "MATCH"
        ):
            decisions.append(
                {
                    "decision_id": _decision_id("ACCOMPLISHMENTS", school_key),
                    "category": "accomplishments",
                    "source_game_id": "",
                    "season_label": "",
                    **_date_fields("", ""),
                    "matchup": school_key,
                    "field_name": "program_accomplishments",
                    "source_value": canonical_json(
                        {
                            key: accomplishment.get(key, "")
                            for key in (
                                "conference_regular_season_championships",
                                "conference_tournament_championships",
                                "ncaa_tournament_appearances",
                                "final_four_appearances",
                                "national_championships",
                                "best_finish_key",
                                "best_finish_year",
                            )
                        }
                    ),
                    "canonical_value": canonical_json(
                        {
                            "ncaa_tournament_appearances": derived["ncaa_tournament_appearances"],
                            "final_four_appearances": derived["final_four_appearances"],
                            "national_championships": derived["national_championships"],
                            "best_finish_key": derived["best_finish_key"],
                            "best_finish_year": derived["best_finish_year"],
                        }
                    ),
                    "relevant_evidence": "Canonical NCAA fields match; conference titles still require authoritative source verification.",
                    "recommended_action": "VERIFY_REFERENCE_VALUES",
                    "allowed_actions": sorted(ACCOMPLISHMENT_ACTIONS),
                    "decision": "PENDING",
                    "resolution_basis": "",
                    "canonical_patch_json": "{}",
                    "source_patch_json": "{}",
                    "notes": "Approval basis must cite the authoritative accomplishment source.",
                }
            )

    if program.get("public_page_enabled") != "Yes":
        decisions.append(
            {
                "decision_id": _decision_id("PUBLICATION", school_key),
                "category": "publication",
                "source_game_id": "",
                "season_label": "",
                **_date_fields("", ""),
                "matchup": school_key,
                "field_name": "public_page_enabled",
                "source_value": program.get("public_page_enabled", ""),
                "canonical_value": "Yes",
                "relevant_evidence": (
                    f"{len(sources):,} in-scope source rows; "
                    f"{identity_counts[ingest_school.REVIEW]:,} identity reviews; "
                    f"{predicted_conflicts:,} definite and "
                    f"{conditional_conflicts:,} conditional discrepancies."
                ),
                "recommended_action": "ENABLE_PUBLIC_PAGE",
                "allowed_actions": sorted(PUBLICATION_ACTIONS),
                "decision": "PENDING",
                "resolution_basis": "",
                "canonical_patch_json": "{}",
                "source_patch_json": "{}",
                "notes": "Publication occurs only after every approved decision and automated gate passes.",
            }
        )

    summary = {
        "source_rows": len(all_sources),
        "in_scope_source_rows": len(sources),
        "pre_cutoff_rows": len(pre_cutoff),
        "existing_game_matches": identity_counts[ingest_school.CONFIDENT],
        "new_canonical_games": identity_counts[ingest_school.NEW_GAME],
        "identity_review_required": identity_counts[ingest_school.REVIEW],
        "assertions_to_add": sum(
            (school_key, row.get("source_game_id", "")) not in existing_pairs
            for row in sources
        ),
        "canonical_enrichment_games": len(predicted_enrichment_games),
        "canonical_enrichment_fields": predicted_enrichment_fields,
        "discrepancies_to_add": predicted_conflicts,
        "conditional_discrepancies": conditional_conflicts,
        "affected_public_programs": sorted(affected_public_programs),
        "already_public": program.get("public_page_enabled") == "Yes",
    }

    return {
        "schema_version": PLAN_SCHEMA_VERSION,
        "workflow_version": WORKFLOW_VERSION,
        "school_key": school_key,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "input_fingerprint": input_fingerprint(repo, school_key),
        "package": package,
        "blockers": blockers,
        "warnings": warnings,
        "summary": summary,
        "decisions": decisions,
    }


def render_report(plan: dict[str, Any], approved_hash: str = "") -> str:
    summary = plan.get("summary", {})
    lines = [
        f"# {plan['school_key']} onboarding review",
        "",
        f"Generated: {plan.get('created_at', '')}",
        f"Input fingerprint: `{plan.get('input_fingerprint', {}).get('sha256', '')}`",
    ]
    if approved_hash:
        lines.append(f"Approved plan: `{approved_hash}`")
    lines.extend(["", "## Preflight summary", ""])
    if summary:
        labels = (
            ("Source rows", "source_rows"),
            ("In-scope rows", "in_scope_source_rows"),
            ("Existing matches", "existing_game_matches"),
            ("New canonical games", "new_canonical_games"),
            ("Identity reviews", "identity_review_required"),
            ("Safe enrichment fields", "canonical_enrichment_fields"),
            ("Discrepancies", "discrepancies_to_add"),
            ("Conditional discrepancies", "conditional_discrepancies"),
        )
        for label, key in labels:
            lines.append(f"- {label}: {summary.get(key, 0):,}")
        affected = summary.get("affected_public_programs", [])
        lines.append(
            "- Affected existing public programs: "
            + (", ".join(affected) if affected else "none")
        )
    else:
        lines.append("- Counts unavailable because package blockers stopped planning.")

    blockers = plan.get("blockers", [])
    warnings = plan.get("warnings", [])
    lines.extend(["", "## Blockers", ""])
    lines.extend(f"- {value}" for value in blockers)
    if not blockers:
        lines.append("- None.")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {value}" for value in warnings)
    if not warnings:
        lines.append("- None.")

    lines.extend(["", "## Owner decisions", ""])
    decisions = plan.get("decisions", [])
    if not decisions:
        lines.append("No owner decisions are pending.")
    for number, item in enumerate(decisions, start=1):
        lines.extend(
            [
                f"### {number}. {item['decision_id']}",
                "",
                f"- Category: {item['category']}",
                f"- Matchup: {item.get('matchup') or '[not game-specific]'}",
                f"- {date_label(item)}",
                f"- Field: {item.get('field_name', '')}",
                f"- Source value: `{item.get('source_value', '')}`",
                f"- Canonical value: `{item.get('canonical_value', '')}`",
                f"- Evidence: {item.get('relevant_evidence', '')}",
                f"- Recommended: `{item.get('recommended_action', '')}`",
                f"- Decision: `{item.get('decision', 'PENDING')}`",
                f"- Basis: {item.get('resolution_basis') or '[required before approval]'}",
            ]
        )
        if item.get("applies_if_identity_decision"):
            lines.append(
                "- Applies if identity decision: `"
                + item["applies_if_identity_decision"]
                + "`"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_preflight_artifacts(plan: dict[str, Any], output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    plan_path = output_dir / "plan.json"
    review_path = output_dir / "review.csv"
    report_path = output_dir / "review.md"
    plan_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with review_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(REVIEW_COLUMNS))
        writer.writeheader()
        for item in plan.get("decisions", []):
            row = dict(item)
            row["allowed_actions"] = " | ".join(item.get("allowed_actions", []))
            writer.writerow({field: row.get(field, "") for field in REVIEW_COLUMNS})
    report_path.write_text(render_report(plan), encoding="utf-8")
    return {"plan": plan_path, "review": review_path, "report": report_path}


def _parse_patch(value: str, label: str) -> dict[str, str]:
    value = (value or "{}").strip() or "{}"
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise WorkflowError(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(parsed, dict) or any(not isinstance(key, str) for key in parsed):
        raise WorkflowError(f"{label} must be a JSON object")
    return {str(key): "" if val is None else str(val) for key, val in parsed.items()}


def _allowed_decision(item: dict[str, Any], decision: str) -> bool:
    category = item["category"]
    if category == "identity":
        if decision == "FORCE_NEW":
            return True
        if decision.startswith("MATCH_CANONICAL:"):
            candidate = decision.split(":", 1)[1]
            return candidate in str(item.get("canonical_value", "")).split(";")
        return False
    if category == "conditional_discrepancy":
        return decision == "NOT_APPLICABLE" or decision in DISCREPANCY_ACTIONS
    allowed = set(item.get("allowed_actions", []))
    return decision in allowed


def approve_plan(
    repo: Path,
    plan_path: Path,
    review_path: Path,
    approved_by: str,
) -> tuple[dict[str, Any], str]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("blockers"):
        raise WorkflowError("Preflight blockers must be cleared before approval")
    current = input_fingerprint(repo, plan["school_key"])
    expected = plan.get("input_fingerprint", {})
    if current.get("sha256") != expected.get("sha256"):
        raise WorkflowError(
            "Plan inputs changed after preflight; run --preflight again before approving"
        )

    with review_path.open(newline="", encoding="utf-8-sig") as handle:
        review_rows = list(csv.DictReader(handle))
    by_id = {row.get("decision_id", ""): row for row in review_rows}
    if len(by_id) != len(review_rows):
        raise WorkflowError("review.csv contains blank or duplicate decision_id values")
    expected_ids = {item["decision_id"] for item in plan.get("decisions", [])}
    if set(by_id) != expected_ids:
        extra = sorted(set(by_id) - expected_ids)
        missing = sorted(expected_ids - set(by_id))
        detail = []
        if missing:
            detail.append("missing: " + ", ".join(missing))
        if extra:
            detail.append("unexpected: " + ", ".join(extra))
        raise WorkflowError("review.csv decision set changed; " + "; ".join(detail))

    identity_choices: dict[str, str] = {}
    for item in plan.get("decisions", []):
        if item.get("category") != "identity":
            continue
        review = by_id[item["decision_id"]]
        decision = review.get("decision", "").strip()
        if not decision or decision == "PENDING":
            raise WorkflowError(f"{item['decision_id']}: decision is still PENDING")
        if not _allowed_decision(item, decision):
            raise WorkflowError(
                f"{item['decision_id']}: unsupported decision {decision!r}"
            )
        identity_choices[item["source_game_id"]] = decision

    sealed_items: list[dict[str, Any]] = []
    for item in plan.get("decisions", []):
        decision_id = item["decision_id"]
        review = by_id.get(decision_id)
        if review is None:
            raise WorkflowError(f"review.csv is missing {decision_id}")
        decision = review.get("decision", "").strip()
        basis = review.get("resolution_basis", "").strip()
        if item.get("category") == "conditional_discrepancy":
            selected_identity = identity_choices.get(item.get("source_game_id", ""))
            applies = selected_identity == item.get("applies_if_identity_decision")
            if not applies:
                sealed = dict(item)
                sealed.update(
                    {
                        "decision": "NOT_APPLICABLE",
                        "resolution_basis": (
                            "Not applicable because the sealed identity decision was "
                            f"{selected_identity or '[missing]'}"
                        ),
                        "canonical_patch": {},
                        "source_patch": {},
                    }
                )
                sealed_items.append(sealed)
                continue
            if decision == "NOT_APPLICABLE":
                raise WorkflowError(
                    f"{decision_id}: selected identity makes this discrepancy applicable"
                )
        if not decision or decision == "PENDING":
            raise WorkflowError(f"{decision_id}: decision is still PENDING")
        if not _allowed_decision(item, decision):
            raise WorkflowError(f"{decision_id}: unsupported decision {decision!r}")
        if not basis:
            raise WorkflowError(f"{decision_id}: resolution_basis is required")
        canonical_patch = _parse_patch(
            review.get("canonical_patch_json", "{}"),
            f"{decision_id} canonical_patch_json",
        )
        source_patch = _parse_patch(
            review.get("source_patch_json", "{}"),
            f"{decision_id} source_patch_json",
        )
        unknown_canonical = sorted(set(canonical_patch) - CANONICAL_PATCH_FIELDS)
        unknown_source = sorted(set(source_patch) - SOURCE_PATCH_FIELDS)
        if unknown_canonical:
            raise WorkflowError(
                f"{decision_id}: forbidden canonical patch fields: {', '.join(unknown_canonical)}"
            )
        if unknown_source:
            raise WorkflowError(
                f"{decision_id}: forbidden source patch fields: {', '.join(unknown_source)}"
            )
        sealed = dict(item)
        sealed.update(
            {
                "decision": decision,
                "resolution_basis": basis,
                "canonical_patch": canonical_patch,
                "source_patch": source_patch,
                "notes": review.get("notes", item.get("notes", "")).strip(),
            }
        )
        if sealed.get("category") == "conditional_discrepancy":
            sealed["category"] = "discrepancy"
            sealed["conditional_identity_satisfied"] = True
        sealed_items.append(sealed)

    publication = next(
        (item for item in sealed_items if item["category"] == "publication"),
        None,
    )
    accomplishment = next(
        (item for item in sealed_items if item["category"] == "accomplishments"),
        None,
    )
    if publication and publication["decision"] == "ENABLE_PUBLIC_PAGE":
        if accomplishment and accomplishment["decision"] != "VERIFY_REFERENCE_VALUES":
            raise WorkflowError(
                "Publication cannot be enabled while accomplishments remain under review"
            )

    approved = dict(plan)
    approved["decisions"] = sealed_items
    approved["summary"] = dict(plan.get("summary", {}))
    approved["summary"]["discrepancies_to_add"] = sum(
        item.get("category") == "discrepancy" for item in sealed_items
    )
    approved["approval"] = {
        "approved_by": approved_by,
        "approved_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    approved_hash = sha256_text(canonical_json(approved))
    approved["approved_plan_hash"] = approved_hash
    return approved, approved_hash


def write_approved_plan(
    approved: dict[str, Any],
    output_dir: Path,
) -> Path:
    path = output_dir / "approved-plan.json"
    path.write_text(json.dumps(approved, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output_dir / "approved-review.md").write_text(
        render_report(approved, approved["approved_plan_hash"]),
        encoding="utf-8",
    )
    return path


def verify_approved_plan(
    repo: Path,
    approved: dict[str, Any],
    supplied_hash: str,
) -> None:
    stored = approved.get("approved_plan_hash", "")
    if not supplied_hash or supplied_hash != stored:
        raise WorkflowError("--approved-plan must exactly match approved-plan.json")
    unhashed = dict(approved)
    unhashed.pop("approved_plan_hash", None)
    actual_hash = sha256_text(canonical_json(unhashed))
    if actual_hash != stored:
        raise WorkflowError("approved-plan.json content does not match its sealed hash")
    current = input_fingerprint(repo, approved["school_key"])
    if current.get("sha256") != approved.get("input_fingerprint", {}).get("sha256"):
        raise WorkflowError(
            "Repository inputs changed after owner approval; preflight and approval must be repeated"
        )


def canonical_field_value(row: dict[str, str], field_name: str) -> str:
    return _canonical_value(row, field_name)


def set_canonical_field(row: dict[str, str], field_name: str, value: str) -> None:
    if field_name == "score":
        score_a, score_b = value.split("-", 1)
        row["team_a_score"] = score_a
        row["team_b_score"] = score_b
        a, b = int(score_a), int(score_b)
        row["result_winner_team_key"] = (
            row["team_a_key"] if a > b else row["team_b_key"] if b > a else ""
        )
        return
    row[field_name] = value
    if field_name == "game_date" and value:
        row["date_precision"] = "EXACT"
    if field_name == "site_type":
        if value == "TEAM_A_HOME":
            row["designated_home_team_key"] = row["team_a_key"]
        elif value == "TEAM_B_HOME":
            row["designated_home_team_key"] = row["team_b_key"]
        else:
            row["designated_home_team_key"] = ""


def relative_source_site(
    source_program_key: str,
    canonical: dict[str, str],
    canonical_site: str,
) -> str:
    if canonical_site in {"NEUTRAL", "UNKNOWN", ""}:
        return canonical_site or "UNKNOWN"
    home_key = (
        canonical["team_a_key"]
        if canonical_site == "TEAM_A_HOME"
        else canonical["team_b_key"]
    )
    return "SOURCE_PROGRAM_HOME" if home_key == source_program_key else "OPPONENT_HOME"


def set_source_field(
    source: dict[str, str],
    canonical: dict[str, str],
    field_name: str,
    value: str,
) -> None:
    if field_name == "score":
        score_a, score_b = value.split("-", 1)
        if source["source_program_key"] == canonical["team_a_key"]:
            team_score, opponent_score = score_a, score_b
        else:
            team_score, opponent_score = score_b, score_a
        source["team_score"] = team_score
        source["opponent_score"] = opponent_score
        team_number, opponent_number = int(team_score), int(opponent_score)
        source["played_result"] = (
            "W" if team_number > opponent_number else "L" if opponent_number > team_number else "T"
        )
        return
    if field_name == "site_type":
        source["curated_site_type"] = relative_source_site(
            source["source_program_key"], canonical, value
        )
        return
    if field_name == "game_type":
        source["curated_game_type"] = value
        return
    if field_name == "result_winner_team_key":
        if value in {"[TIE]", ""}:
            source["played_result"] = "T"
        elif value == source["source_program_key"]:
            source["played_result"] = "W"
        else:
            source["played_result"] = "L"
        return
    source[field_name] = value


def _append_note(existing: str, addition: str) -> str:
    existing = (existing or "").strip()
    if addition in existing:
        return existing
    return f"{existing}; {addition}" if existing else addition


def _sync_site_metadata_from_source(
    source: dict[str, str],
    canonical: dict[str, str],
    venue_map: dict[str, dict[str, str]],
) -> None:
    site = canonical.get("site_type", "")
    if site == "UNKNOWN":
        canonical["venue_key"] = ""
        canonical["site_city"] = ""
        canonical["site_state"] = ""
        return
    venue_name = source.get("curated_venue_name", "").strip().casefold()
    venue = venue_map.get(venue_name, {}) if venue_name else {}
    canonical["venue_key"] = venue.get("venue_key", "")
    registry_fields: list[str] = []
    if canonical["venue_key"]:
        registry_fields.append("venue_key")
    if location_pair_status(source.get("city", ""), source.get("state", "")) == "complete":
        canonical["site_city"] = source["city"].strip()
        canonical["site_state"] = source["state"].strip()
    elif location_pair_status(venue.get("city", ""), venue.get("state", "")) == "complete":
        canonical["site_city"] = venue["city"].strip()
        canonical["site_state"] = venue["state"].strip()
        registry_fields.extend(("site_city", "site_state"))
    else:
        canonical["site_city"] = ""
        canonical["site_state"] = ""
    if registry_fields:
        canonical["notes"] = append_note(
            canonical.get("notes", ""),
            registry_fallback_marker(
                source.get("source_program_key", ""),
                source.get("source_game_id", ""),
                canonical["venue_key"],
                canonical.get("site_type", ""),
                registry_fields,
            ),
        )


def _sync_site_metadata_to_source(
    source: dict[str, str],
    canonical: dict[str, str],
    venue_names: dict[str, str],
) -> None:
    source["curated_venue_name"] = venue_names.get(canonical.get("venue_key", ""), "")
    source["city"] = canonical.get("site_city", "")
    source["state"] = canonical.get("site_state", "")


def _venue_maps(repo: Path, school_key: str) -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    target_metadata = ingest_school.load_venue_metadata_map(
        repo / "schools" / school_key / "venues.csv"
    )
    names_by_key: dict[str, str] = {}
    for path in sorted((repo / "schools").glob("*/venues.csv")):
        for row in read_csv(path):
            key = row.get("venue_key", "").strip()
            name = row.get("canonical_name", "").strip()
            if key and name:
                names_by_key.setdefault(key, name)
    return target_metadata, names_by_key


def apply_reconciliation_decisions(
    repo: Path,
    approved: dict[str, Any],
) -> dict[str, int]:
    school_key = approved["school_key"]
    reconciliation_items = [
        item
        for item in approved.get("decisions", [])
        if item.get("category") == "discrepancy"
    ]
    if not reconciliation_items:
        return {}
    canonical_path = repo / "data/canonical/games.csv"
    assertions_path = repo / "data/evidence/game-assertions.csv"
    discrepancies_path = repo / "data/reconciliation/discrepancies.csv"
    source_path = repo / "schools" / school_key / "source-games.csv"

    canonical_fields, canonical_rows = read_csv_table(canonical_path)
    assertion_fields, assertion_rows = read_csv_table(assertions_path)
    discrepancy_fields, discrepancy_rows = read_csv_table(discrepancies_path)
    source_fields, source_rows = read_csv_table(source_path)
    canonical_by_id = {row["canonical_game_id"]: row for row in canonical_rows}
    source_by_id = {row["source_game_id"]: row for row in source_rows}
    assertion_by_source: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in assertion_rows:
        assertion_by_source[(row.get("source_program_key", ""), row.get("source_game_id", ""))].append(row)

    discrepancy_index: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in discrepancy_rows:
        discrepancy_index[
            (
                row.get("canonical_game_id", ""),
                row.get("field_name", ""),
                row.get("source_a_program_key", ""),
            )
        ].append(row)

    target_venue_metadata, venue_names = _venue_maps(repo, school_key)
    counts = Counter()
    for item in reconciliation_items:
        game_id = item["canonical_game_id"]
        field_name = item["field_name"]
        source_game_id = item["source_game_id"]
        canonical = canonical_by_id.get(game_id)
        source = source_by_id.get(source_game_id)
        assertions = assertion_by_source.get((school_key, source_game_id), [])
        discrepancy_matches = discrepancy_index.get((game_id, field_name, school_key), [])
        if canonical is None or source is None:
            raise WorkflowError(f"{item['decision_id']}: canonical or source row is missing after ingestion")
        if len(assertions) != 1:
            raise WorkflowError(f"{item['decision_id']}: expected one target assertion; found {len(assertions)}")
        if len(discrepancy_matches) != 1:
            raise WorkflowError(f"{item['decision_id']}: expected one discrepancy; found {len(discrepancy_matches)}")
        assertion = assertions[0]
        discrepancy = discrepancy_matches[0]
        if discrepancy.get("source_a_value", "") != item.get("source_value", ""):
            raise WorkflowError(f"{item['decision_id']}: ingested source discrepancy value changed")

        current = canonical_field_value(canonical, field_name)
        expected = item.get("canonical_value", "")
        decision = item["decision"]
        if current != expected and not (
            decision == "USE_SOURCE" and current == item.get("source_value", "")
        ):
            raise WorkflowError(
                f"{item['decision_id']}: canonical {field_name} is {current!r}, expected {expected!r}"
            )

        final_value = current
        if decision == "USE_SOURCE":
            final_value = item["source_value"]
            set_canonical_field(canonical, field_name, final_value)
            if field_name == "site_type":
                _sync_site_metadata_from_source(source, canonical, target_venue_metadata)
                canonical["notes"], retired = retire_site_mismatched_registry_fallbacks(
                    canonical.get("notes", ""),
                    canonical.get("site_type", ""),
                )
                counts["registry_fallbacks_retired"] += retired
            counts["canonical_changes"] += 1
        elif decision == "NORMALIZE_SOURCE_TO_CANONICAL":
            final_value = current
            set_source_field(source, canonical, field_name, final_value)
            if field_name == "site_type":
                _sync_site_metadata_to_source(source, canonical, venue_names)
            counts["source_normalizations"] += 1
        elif decision == "KEEP_CANONICAL":
            final_value = current
            counts["canonical_retentions"] += 1
        elif decision == "LEAVE_UNRESOLVED":
            final_value = current
            counts["left_under_review"] += 1
        else:
            raise WorkflowError(f"{item['decision_id']}: unsupported discrepancy action {decision}")

        for field, value in item.get("canonical_patch", {}).items():
            canonical[field] = value
        for field, value in item.get("source_patch", {}).items():
            source[field] = value
        if location_pair_status(canonical.get("site_city", ""), canonical.get("site_state", "")) == "partial":
            raise WorkflowError(f"{item['decision_id']}: canonical patch creates partial city/state")
        if location_pair_status(source.get("city", ""), source.get("state", "")) == "partial":
            raise WorkflowError(f"{item['decision_id']}: source patch creates partial city/state")

        if decision == "NORMALIZE_SOURCE_TO_CANONICAL" or item.get("source_patch"):
            note = (
                f"Owner-approved onboarding reconciliation {approved['approved_plan_hash'][:12]}: "
                f"{field_name} normalized; raw_text preserved."
            )
            source["notes"] = _append_note(source.get("notes", ""), note)
        for field in SOURCE_ASSERTION_COPY_FIELDS:
            assertion[field] = source.get(field, "")

        discrepancy["canonical_value"] = canonical_field_value(canonical, field_name)
        discrepancy["resolution_basis"] = item["resolution_basis"]
        if decision == "LEAVE_UNRESOLVED":
            discrepancy["status"] = "UNDER_REVIEW"
            discrepancy["notes"] = (
                "Owner explicitly approved publication with this dated conflict unresolved; "
                "canonical and source evidence remain preserved."
            )
        else:
            discrepancy["status"] = "RESOLVED"
            discrepancy["notes"] = (
                "Resolved through the sealed generic onboarding plan; source raw_text and "
                "the original discrepancy value remain preserved."
            )
        counts["processed"] += 1

    write_csv_preserving_format(canonical_path, canonical_fields, canonical_rows)
    write_csv_preserving_format(assertions_path, assertion_fields, assertion_rows)
    write_csv_preserving_format(discrepancies_path, discrepancy_fields, discrepancy_rows)
    write_csv_preserving_format(source_path, source_fields, source_rows)
    return dict(counts)


def apply_publication_decisions(
    repo: Path,
    approved: dict[str, Any],
) -> dict[str, int]:
    school_key = approved["school_key"]
    programs_path = repo / "data/reference/programs.csv"
    accomplishments_path = repo / "data/reference/program-accomplishments.csv"
    program_fields, program_rows = read_csv_table(programs_path)
    accomplishment_fields, accomplishment_rows = read_csv_table(accomplishments_path)
    program = next(row for row in program_rows if row["program_key"] == school_key)
    accomplishment = next(row for row in accomplishment_rows if row["program_key"] == school_key)
    counts = Counter()
    program_changed = False
    accomplishment_changed = False

    for item in approved.get("decisions", []):
        if item["category"] == "accomplishments":
            if item["decision"] == "VERIFY_REFERENCE_VALUES":
                accomplishment["verification_status"] = "VERIFIED"
                accomplishment["verification_basis"] = item["resolution_basis"]
                accomplishment["canonical_crosscheck_status"] = "MATCH"
                accomplishment["notes"] = _append_note(
                    accomplishment.get("notes", ""),
                    f"Verified through onboarding plan {approved['approved_plan_hash'][:12]}.",
                )
                counts["accomplishments_verified"] += 1
                accomplishment_changed = True
            elif item["decision"] != "KEEP_UNDER_REVIEW":
                raise WorkflowError(f"Unsupported accomplishment decision {item['decision']}")
        elif item["category"] == "publication":
            if item["decision"] == "ENABLE_PUBLIC_PAGE":
                program["public_page_enabled"] = "Yes"
                counts["pages_enabled"] += 1
                program_changed = True
            elif item["decision"] != "KEEP_DISABLED":
                raise WorkflowError(f"Unsupported publication decision {item['decision']}")

    if program_changed:
        write_csv_preserving_format(programs_path, program_fields, program_rows)
    if accomplishment_changed:
        write_csv_preserving_format(
            accomplishments_path,
            accomplishment_fields,
            accomplishment_rows,
        )
    return dict(counts)


def archive_approved_plan(repo: Path, approved: dict[str, Any]) -> Path:
    directory = repo / "data/reconciliation/onboarding-decisions"
    directory.mkdir(parents=True, exist_ok=True)
    name = f"{approved['school_key']}-{approved['approved_plan_hash'][:12]}.json"
    path = directory / name
    payload = dict(approved)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path
