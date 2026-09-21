#!/usr/bin/env python3
"""Durable Stage 3A research-state validation and exact-game reuse helpers.

This tool exists for the independent Research lane. It does not mutate canonical data.

Commands:
- validate: prove that the Stage 3A row ledger is structurally complete and reconciles
  exactly to Stage 1 / the accepted postseason handoff.
- canonical-neutral-lookup: perform the required read-only exact-game lookup for
  neutral-site work before external historical research.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]

FIELD_ALIASES = {
    "id": ("research_game_id", "source_game_id"),
    "season": ("season_label", "season"),
    "date": ("game_date", "date"),
    "opponent": (
        "normalized_opponent_key",
        "opponent_key",
        "canonical_opponent_key",
    ),
    "disposition": (
        "stage3a_disposition",
        "stage3a_population_disposition",
        "stage3a_restart_scope",
    ),
    "han": (
        "stage3a_han",
        "han",
        "site_classification",
        "curated_site_type",
    ),
    "han_basis": ("stage3a_han_basis",),
    "venue": ("stage3a_venue", "curated_venue_name", "venue_name"),
    "city": ("stage3a_city", "city", "site_city"),
    "state": ("stage3a_state", "state", "site_state"),
    "status": (
        "site_research_status",
        "stage3a_venue_status",
        "resolution_status",
    ),
    "basis": (
        "site_research_basis",
        "stage3a_research_note",
        "evidence_basis",
    ),
    "next_action": ("stage3a_next_action", "next_action"),
}

REGULAR_DISPOSITIONS = {
    "REGULAR",
    "REGULAR_SEASON",
    "REGULAR_SEASON_STAGE3A",
    "REGULAR_SEASON_STAGE3A_RESTART",
}
POSTSEASON_DISPOSITIONS = {
    "POSTSEASON",
    "POSTSEASON_DEFERRED",
    "POSTSEASON_HANDOFF",
    "POSTSEASON_HANDOFF_ACCEPTED",
}
HAN_VALUES = {"HOME", "OPPONENT_HOME", "NEUTRAL"}
TERMINAL_ACTIONS = {
    "COMPLETE",
    "SUPPORTED",
    "POSTSEASON_HANDOFF",
    "NO_SOURCE_SCHOOL_VENUE_RESEARCH",
    "TERMINAL_RESEARCHED_DEBT",
}
NEUTRAL_DEBT_STATUSES = {"RESEARCHED_PARTIAL", "RESEARCHED_UNRESOLVED"}
HOME_DEBT_STATUS = "RESEARCHED_UNRESOLVED_HOME_VENUE"


class Stage3AError(RuntimeError):
    pass


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise Stage3AError(f"CSV not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _resolve_field(
    fields: Iterable[str],
    semantic: str,
    *,
    required: bool = False,
) -> str | None:
    available = set(fields)
    for candidate in FIELD_ALIASES[semantic]:
        if candidate in available:
            return candidate
    if required:
        raise Stage3AError(
            f"missing required Stage 3A column for {semantic}; "
            f"accepted names={FIELD_ALIASES[semantic]}"
        )
    return None


def _value(row: dict[str, str], field: str | None) -> str:
    if not field:
        return ""
    return (row.get(field) or "").strip()


def _normalize_disposition(value: str) -> str:
    raw = (value or "").strip().upper()
    if raw in REGULAR_DISPOSITIONS or raw.startswith("REGULAR_SEASON"):
        return "REGULAR_SEASON"
    if raw in POSTSEASON_DISPOSITIONS or raw.startswith("POSTSEASON"):
        return "POSTSEASON_HANDOFF"
    return raw


def _normalize_han(value: str) -> str:
    raw = (value or "").strip().upper()
    if raw in {"HOME", "SOURCE_PROGRAM_HOME"}:
        return "HOME"
    if raw in {"AWAY", "OPPONENT_HOME"}:
        return "OPPONENT_HOME"
    if raw == "NEUTRAL":
        return "NEUTRAL"
    if not raw:
        return ""
    return raw


def _season_start(value: str) -> int | None:
    match = re.match(r"^(\d{4})[-–](\d{2}|\d{4})$", (value or "").strip())
    if not match:
        return None
    return int(match.group(1))


def _exact_date(value: str) -> bool:
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", (value or "").strip()))


def _id_set(
    path: Path,
    *,
    label: str,
) -> tuple[set[str], list[str]]:
    fields, rows = _read_csv(path)
    id_field = _resolve_field(fields, "id", required=True)
    values = [_value(row, id_field) for row in rows]
    errors: list[str] = []
    if any(not value for value in values):
        errors.append(f"{label} contains blank stable IDs")
    counts = Counter(values)
    duplicates = sorted(value for value, count in counts.items() if value and count > 1)
    if duplicates:
        errors.append(
            f"{label} contains duplicate stable IDs; examples: "
            + ", ".join(duplicates[:12])
        )
    return {value for value in values if value}, errors


def validate_stage3a_state(
    ledger_path: Path,
    *,
    stage1_path: Path,
    postseason_path: Path | None = None,
    phase: str = "complete",
    example_limit: int = 12,
) -> dict[str, Any]:
    """Validate one durable Stage 3A row-level ledger.

    The validator accepts a small alias set for recovery artifacts, but new Research
    lanes should use the canonical field names documented in
    docs/stage3a-regular-season-site-research.md.
    """

    fields, rows = _read_csv(ledger_path)
    errors: list[str] = []
    warnings: list[str] = []

    id_field = _resolve_field(fields, "id", required=True)
    disposition_field = _resolve_field(fields, "disposition", required=True)
    season_field = _resolve_field(fields, "season", required=phase == "complete")
    han_field = _resolve_field(fields, "han", required=phase == "complete")
    han_basis_field = _resolve_field(fields, "han_basis", required=phase == "complete")
    venue_field = _resolve_field(fields, "venue", required=phase == "complete")
    city_field = _resolve_field(fields, "city", required=phase == "complete")
    state_field = _resolve_field(fields, "state", required=phase == "complete")
    status_field = _resolve_field(fields, "status", required=phase == "complete")
    basis_field = _resolve_field(fields, "basis", required=phase == "complete")
    next_action_field = _resolve_field(
        fields,
        "next_action",
        required=phase == "complete",
    )
    opponent_field = _resolve_field(fields, "opponent", required=False)
    date_field = _resolve_field(fields, "date", required=False)

    ledger_ids = [_value(row, id_field) for row in rows]
    if any(not value for value in ledger_ids):
        errors.append("Stage 3A ledger contains blank stable IDs")
    ledger_counts = Counter(ledger_ids)
    duplicates = sorted(
        value for value, count in ledger_counts.items() if value and count > 1
    )
    if duplicates:
        errors.append(
            "Stage 3A ledger contains duplicate stable IDs; examples: "
            + ", ".join(duplicates[:example_limit])
        )

    stage1_ids, stage1_errors = _id_set(stage1_path, label="Stage 1 ledger")
    errors.extend(stage1_errors)
    ledger_id_set = {value for value in ledger_ids if value}
    missing = sorted(stage1_ids - ledger_id_set)
    extra = sorted(ledger_id_set - stage1_ids)
    if missing or extra:
        errors.append(
            "Stage 3A ledger does not exactly equal the Stage 1 universe; "
            f"missing={missing[:example_limit]} extra={extra[:example_limit]}"
        )

    dispositions: Counter[str] = Counter()
    han_counts: Counter[str] = Counter()
    action_counts: Counter[str] = Counter()
    regular_ids: set[str] = set()
    postseason_ids: set[str] = set()
    home_debt: list[str] = []
    modern_neutral_debt: list[str] = []
    historical_neutral_debt: list[str] = []
    opponent_home_no_research: list[str] = []
    active_action_rows: list[str] = []

    for line_number, row in enumerate(rows, start=2):
        rid = _value(row, id_field) or f"line {line_number}"
        disposition = _normalize_disposition(_value(row, disposition_field))
        dispositions[disposition or "BLANK"] += 1

        if disposition == "REGULAR_SEASON":
            regular_ids.add(rid)
        elif disposition == "POSTSEASON_HANDOFF":
            postseason_ids.add(rid)
        else:
            errors.append(
                f"{rid}: invalid stage3a disposition {_value(row, disposition_field)!r}"
            )
            continue

        if phase != "complete":
            continue

        action = _value(row, next_action_field).upper()
        action_counts[action or "BLANK"] += 1

        if disposition == "POSTSEASON_HANDOFF":
            if action != "POSTSEASON_HANDOFF":
                errors.append(
                    f"{rid}: postseason handoff row must have "
                    "stage3a_next_action=POSTSEASON_HANDOFF"
                )
            continue

        han = _normalize_han(_value(row, han_field))
        han_counts[han or "BLANK"] += 1
        if han not in HAN_VALUES:
            errors.append(f"{rid}: regular-season H/A/N is not fully resolved: {han!r}")
            continue

        han_basis = _value(row, han_basis_field)
        if not han_basis:
            errors.append(f"{rid}: regular-season H/A/N basis is blank")

        venue = _value(row, venue_field)
        city = _value(row, city_field)
        state = _value(row, state_field)
        status = _value(row, status_field).upper()
        basis = _value(row, basis_field)

        if bool(city) != bool(state):
            errors.append(f"{rid}: Stage 3A city/state must be both populated or both blank")

        if status and not basis:
            errors.append(f"{rid}: site research status is populated without a basis")
        if basis and not status and not venue and han in {"HOME", "NEUTRAL"}:
            warnings.append(
                f"{rid}: site research basis is populated without a status on an "
                "unresolved source-school site responsibility"
            )

        if han == "HOME":
            if venue:
                if not city or not state:
                    errors.append(f"{rid}: HOME venue requires complete city/state")
                if not basis:
                    errors.append(f"{rid}: HOME venue requires site research provenance")
                if action not in {"COMPLETE", "SUPPORTED"}:
                    errors.append(
                        f"{rid}: completed HOME row has nonterminal next action {action!r}"
                    )
            else:
                if status != HOME_DEBT_STATUS or not basis or not city or not state:
                    errors.append(
                        f"{rid}: blank HOME venue requires {HOME_DEBT_STATUS}, "
                        "complete city/state, and a research basis"
                    )
                else:
                    home_debt.append(rid)
                if action != "TERMINAL_RESEARCHED_DEBT":
                    errors.append(
                        f"{rid}: researched-unresolved HOME row must be terminal debt"
                    )

        elif han == "OPPONENT_HOME":
            if venue and bool(city) != bool(state):
                errors.append(
                    f"{rid}: populated OPPONENT_HOME venue has incomplete city/state"
                )
            if action not in {
                "COMPLETE",
                "SUPPORTED",
                "NO_SOURCE_SCHOOL_VENUE_RESEARCH",
            }:
                active_action_rows.append(rid)
            if not venue and action == "NO_SOURCE_SCHOOL_VENUE_RESEARCH":
                opponent_home_no_research.append(rid)

        elif han == "NEUTRAL":
            start_year = _season_start(_value(row, season_field))
            if start_year is None:
                errors.append(
                    f"{rid}: cannot determine neutral era from season "
                    f"{_value(row, season_field)!r}"
                )
            if venue:
                if not city or not state:
                    errors.append(f"{rid}: NEUTRAL venue requires complete city/state")
                if not basis:
                    errors.append(
                        f"{rid}: NEUTRAL venue requires site research provenance"
                    )
                if action not in {"COMPLETE", "SUPPORTED"}:
                    errors.append(
                        f"{rid}: completed NEUTRAL row has nonterminal next action {action!r}"
                    )
            else:
                if status not in NEUTRAL_DEBT_STATUSES or not basis:
                    errors.append(
                        f"{rid}: blank NEUTRAL venue requires researched partial/unresolved "
                        "status plus a research basis"
                    )
                elif start_year is not None and start_year >= 1984:
                    modern_neutral_debt.append(rid)
                else:
                    historical_neutral_debt.append(rid)
                if action != "TERMINAL_RESEARCHED_DEBT":
                    errors.append(
                        f"{rid}: researched-unresolved NEUTRAL row must be terminal debt"
                    )

        if action not in TERMINAL_ACTIONS:
            active_action_rows.append(rid)

    if phase == "complete" and active_action_rows:
        unique_active = sorted(set(active_action_rows))
        errors.append(
            "Stage 3A completion ledger still contains active/nonterminal next actions "
            f"on {len(unique_active):,} row(s); examples: "
            + ", ".join(unique_active[:example_limit])
        )

    if regular_ids & postseason_ids:
        errors.append("regular-season and postseason-handoff stable-ID sets overlap")
    if regular_ids | postseason_ids != ledger_id_set:
        errors.append(
            "regular-season + postseason-handoff stable-ID sets do not equal the "
            "Stage 3A ledger universe"
        )

    if postseason_path is not None:
        expected_postseason_ids, postseason_errors = _id_set(
            postseason_path,
            label="accepted postseason handoff",
        )
        errors.extend(postseason_errors)
        missing_post = sorted(expected_postseason_ids - postseason_ids)
        extra_post = sorted(postseason_ids - expected_postseason_ids)
        if missing_post or extra_post:
            errors.append(
                "Stage 3A postseason handoff does not exactly equal the accepted "
                "postseason ledger; "
                f"missing={missing_post[:example_limit]} "
                f"extra={extra_post[:example_limit]}"
            )

    counts: dict[str, Any] = {
        "stage1_rows": len(stage1_ids),
        "stage3a_rows": len(rows),
        "regular_season_rows": len(regular_ids),
        "postseason_handoff_rows": len(postseason_ids),
        "dispositions": dict(sorted(dispositions.items())),
    }
    if phase == "complete":
        counts.update(
            {
                "han": dict(sorted(han_counts.items())),
                "next_actions": dict(sorted(action_counts.items())),
                "home_terminal_debt_rows": len(home_debt),
                "modern_neutral_terminal_debt_rows": len(modern_neutral_debt),
                "historical_neutral_terminal_debt_rows": len(
                    historical_neutral_debt
                ),
                "opponent_home_no_source_school_venue_research_rows": len(
                    opponent_home_no_research
                ),
            }
        )
        if modern_neutral_debt:
            warnings.append(
                "modern (1984-85+) neutral venue debt remains on "
                f"{len(modern_neutral_debt):,} row(s); Stage 6 must challenge this "
                "population explicitly"
            )

    return {
        "status": "PASS" if not errors else "FAIL",
        "phase": phase,
        "ledger": str(ledger_path),
        "stage1_ledger": str(stage1_path),
        "postseason_ledger": str(postseason_path) if postseason_path else "",
        "columns": {
            "research_game_id": id_field,
            "season": season_field or "",
            "game_date": date_field or "",
            "normalized_opponent_key": opponent_field or "",
            "stage3a_disposition": disposition_field,
            "stage3a_han": han_field or "",
            "stage3a_han_basis": han_basis_field or "",
            "stage3a_venue": venue_field or "",
            "stage3a_city": city_field or "",
            "stage3a_state": state_field or "",
            "site_research_status": status_field or "",
            "site_research_basis": basis_field or "",
            "stage3a_next_action": next_action_field or "",
        },
        "counts": counts,
        "debt": {
            "home": home_debt,
            "modern_neutral": modern_neutral_debt,
            "historical_neutral": historical_neutral_debt,
        },
        "errors": errors,
        "warnings": warnings,
    }


def _canonical_target_han(row: dict[str, str], source_program_key: str) -> str:
    site_type = (row.get("site_type") or "").strip().upper()
    team_a = (row.get("team_a_key") or "").strip()
    team_b = (row.get("team_b_key") or "").strip()
    if site_type == "NEUTRAL":
        return "NEUTRAL"
    if site_type == "TEAM_A_HOME":
        return "HOME" if team_a == source_program_key else "OPPONENT_HOME"
    if site_type == "TEAM_B_HOME":
        return "HOME" if team_b == source_program_key else "OPPONENT_HOME"
    designated = (row.get("designated_home_team_key") or "").strip()
    if designated:
        return "HOME" if designated == source_program_key else "OPPONENT_HOME"
    return ""


def canonical_neutral_lookup(
    ledger_path: Path,
    *,
    source_program_key: str,
    output_path: Path,
    canonical_games_path: Path,
    assertions_path: Path,
    venues_path: Path,
) -> dict[str, Any]:
    """Write read-only exact-game canonical/reciprocal candidates for neutral rows."""

    fields, rows = _read_csv(ledger_path)
    id_field = _resolve_field(fields, "id", required=True)
    date_field = _resolve_field(fields, "date", required=True)
    opponent_field = _resolve_field(fields, "opponent", required=True)
    han_field = _resolve_field(fields, "han", required=False)
    disposition_field = _resolve_field(fields, "disposition", required=False)
    season_field = _resolve_field(fields, "season", required=False)

    input_rows: list[dict[str, str]] = []
    needed_keys: set[tuple[str, str]] = set()
    for row in rows:
        if disposition_field and _normalize_disposition(
            _value(row, disposition_field)
        ) == "POSTSEASON_HANDOFF":
            continue
        if han_field and _normalize_han(_value(row, han_field)) != "NEUTRAL":
            continue
        input_rows.append(row)
        game_date = _value(row, date_field)
        opponent = _value(row, opponent_field)
        if _exact_date(game_date) and opponent:
            needed_keys.add((game_date, opponent))

    canonical_matches: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    canonical_ids: set[str] = set()

    with canonical_games_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            team_a = (row.get("team_a_key") or "").strip()
            team_b = (row.get("team_b_key") or "").strip()
            if source_program_key not in {team_a, team_b}:
                continue
            opponent = team_b if team_a == source_program_key else team_a
            key = ((row.get("game_date") or "").strip(), opponent)
            if key not in needed_keys:
                continue
            canonical_matches[key].append(row)
            canonical_game_id = (row.get("canonical_game_id") or "").strip()
            if canonical_game_id:
                canonical_ids.add(canonical_game_id)

    venue_by_id: dict[str, dict[str, str]] = {}
    if venues_path.is_file():
        with venues_path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                venue_id = (row.get("venue_id") or "").strip()
                if venue_id:
                    venue_by_id[venue_id] = row

    assertions_by_game: dict[str, list[dict[str, str]]] = defaultdict(list)
    with assertions_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            canonical_game_id = (row.get("canonical_game_id") or "").strip()
            if canonical_game_id not in canonical_ids:
                continue
            if (row.get("source_program_key") or "").strip() == source_program_key:
                continue
            has_site_evidence = any(
                (row.get(field) or "").strip()
                for field in (
                    "curated_venue_name",
                    "source_venue_name",
                    "city",
                    "state",
                    "curated_site_type",
                    "source_site_candidate",
                )
            )
            if has_site_evidence:
                assertions_by_game[canonical_game_id].append(row)

    output_fields = [
        "research_game_id",
        "season_label",
        "game_date",
        "normalized_opponent_key",
        "research_han",
        "lookup_status",
        "canonical_match_count",
        "canonical_game_ids",
        "canonical_target_han",
        "canonical_venue_ids",
        "canonical_venue_keys",
        "canonical_venue_names",
        "canonical_city_states",
        "reciprocal_assertion_count",
        "reciprocal_assertion_sources",
        "reciprocal_venue_candidates",
        "lookup_note",
    ]

    output_rows: list[dict[str, str]] = []
    status_counts: Counter[str] = Counter()

    for row in input_rows:
        rid = _value(row, id_field)
        game_date = _value(row, date_field)
        opponent = _value(row, opponent_field)
        research_han = _normalize_han(_value(row, han_field))
        season = _value(row, season_field)

        out = {field: "" for field in output_fields}
        out.update(
            {
                "research_game_id": rid,
                "season_label": season,
                "game_date": game_date,
                "normalized_opponent_key": opponent,
                "research_han": research_han,
            }
        )

        if not _exact_date(game_date) or not opponent:
            status = "INSUFFICIENT_EXACT_MATCH_KEYS"
            out["lookup_status"] = status
            out["lookup_note"] = (
                "Exact-game reuse requires an ISO game_date and normalized opponent key."
            )
            status_counts[status] += 1
            output_rows.append(out)
            continue

        matches = canonical_matches.get((game_date, opponent), [])
        out["canonical_match_count"] = str(len(matches))
        if not matches:
            status = "NO_EXACT_CANONICAL_MATCH"
            out["lookup_status"] = status
            status_counts[status] += 1
            output_rows.append(out)
            continue

        if len(matches) > 1:
            status = "AMBIGUOUS_EXACT_CANONICAL_MATCH"
            out["lookup_status"] = status
            out["canonical_game_ids"] = "|".join(
                sorted(
                    {
                        (match.get("canonical_game_id") or "").strip()
                        for match in matches
                        if (match.get("canonical_game_id") or "").strip()
                    }
                )
            )
            out["lookup_note"] = (
                "Multiple canonical rows match the same exact date/opponent; "
                "do not auto-reuse."
            )
            status_counts[status] += 1
            output_rows.append(out)
            continue

        match = matches[0]
        canonical_game_id = (match.get("canonical_game_id") or "").strip()
        canonical_han = _canonical_target_han(match, source_program_key)
        venue_id = (match.get("venue_id") or "").strip()
        venue_key = (match.get("venue_key") or "").strip()
        city = (match.get("site_city") or "").strip()
        state = (match.get("site_state") or "").strip()
        venue_ref = venue_by_id.get(venue_id, {})
        venue_name = (venue_ref.get("display_name") or "").strip()

        out["canonical_game_ids"] = canonical_game_id
        out["canonical_target_han"] = canonical_han
        out["canonical_venue_ids"] = venue_id
        out["canonical_venue_keys"] = venue_key
        out["canonical_venue_names"] = venue_name
        out["canonical_city_states"] = (
            f"{city}, {state}" if city and state else city or state
        )

        reciprocal = assertions_by_game.get(canonical_game_id, [])
        reciprocal_sources = sorted(
            {
                (item.get("source_program_key") or "").strip()
                + "/"
                + (item.get("source_game_id") or "").strip()
                for item in reciprocal
                if (item.get("source_program_key") or "").strip()
            }
        )
        reciprocal_candidates: list[dict[str, str]] = []
        for item in reciprocal:
            candidate = {
                "source_program_key": (item.get("source_program_key") or "").strip(),
                "source_game_id": (item.get("source_game_id") or "").strip(),
                "curated_site_type": (item.get("curated_site_type") or "").strip(),
                "curated_venue_name": (
                    item.get("curated_venue_name") or ""
                ).strip(),
                "source_venue_name": (item.get("source_venue_name") or "").strip(),
                "city": (item.get("city") or "").strip(),
                "state": (item.get("state") or "").strip(),
            }
            reciprocal_candidates.append(candidate)

        out["reciprocal_assertion_count"] = str(len(reciprocal))
        out["reciprocal_assertion_sources"] = "|".join(reciprocal_sources)
        out["reciprocal_venue_candidates"] = json.dumps(
            reciprocal_candidates,
            sort_keys=True,
            separators=(",", ":"),
        )

        if research_han == "NEUTRAL" and canonical_han and canonical_han != "NEUTRAL":
            status = "EXACT_GAME_HAN_CONTRADICTION"
            out["lookup_note"] = (
                "Canonical/reciprocal evidence is a review trigger, not an automatic "
                "override of Research H/A/N."
            )
        elif venue_id or venue_key:
            status = "CANONICAL_EXACT_GAME_VENUE"
        elif any(
            candidate["curated_venue_name"] or candidate["source_venue_name"]
            for candidate in reciprocal_candidates
        ):
            status = "RECIPROCAL_EXACT_GAME_VENUE_CANDIDATE"
        else:
            status = "EXACT_GAME_MATCH_NO_VENUE"

        out["lookup_status"] = status
        status_counts[status] += 1
        output_rows.append(out)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    return {
        "status": "PASS",
        "source_program_key": source_program_key,
        "input_neutral_rows": len(input_rows),
        "output": str(output_path),
        "lookup_status_counts": dict(sorted(status_counts.items())),
        "note": (
            "This is read-only exact-game evidence discovery. Matches and contradictions "
            "must be adjudicated under Stage 3A policy; nothing is auto-applied."
        ),
    }


def _write_report(path: Path | None, report: dict[str, Any]) -> None:
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage 3A durable-state and canonical exact-game helpers."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser(
        "validate",
        help="Validate one full Stage 3A row-level ledger against Stage 1.",
    )
    validate.add_argument("--ledger", type=Path, required=True)
    validate.add_argument("--stage1-ledger", type=Path, required=True)
    validate.add_argument("--postseason-ledger", type=Path)
    validate.add_argument(
        "--phase",
        choices=("bootstrap", "complete"),
        default="complete",
    )
    validate.add_argument("--report", type=Path)

    lookup = sub.add_parser(
        "canonical-neutral-lookup",
        help="Write read-only exact-game canonical/reciprocal venue candidates.",
    )
    lookup.add_argument("--ledger", type=Path, required=True)
    lookup.add_argument("--source-program-key", required=True)
    lookup.add_argument("--output", type=Path, required=True)
    lookup.add_argument(
        "--canonical-games",
        type=Path,
        default=ROOT / "data" / "canonical" / "games.csv",
    )
    lookup.add_argument(
        "--assertions",
        type=Path,
        default=ROOT / "data" / "evidence" / "game-assertions.csv",
    )
    lookup.add_argument(
        "--venues",
        type=Path,
        default=ROOT / "data" / "reference" / "venues.csv",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "validate":
            report = validate_stage3a_state(
                args.ledger,
                stage1_path=args.stage1_ledger,
                postseason_path=args.postseason_ledger,
                phase=args.phase,
            )
            _write_report(args.report, report)
            return 0 if report["status"] == "PASS" else 1

        report = canonical_neutral_lookup(
            args.ledger,
            source_program_key=args.source_program_key,
            output_path=args.output,
            canonical_games_path=args.canonical_games,
            assertions_path=args.assertions,
            venues_path=args.venues,
        )
        _write_report(None, report)
        return 0
    except Stage3AError as exc:
        print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
