"""Program-perspective history scope and accomplishment helpers."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Iterable


SEASON_LABEL_RE = re.compile(r"^(\d{4})-(\d{4})$")

HISTORY_SCOPE_STATUSES = {"", "OWNER_CONFIRMED", "UNDER_REVIEW"}
HISTORY_SCOPE_BASES = {
    "",
    "ALWAYS_TOP_LEVEL_FROM_INCEPTION",
    "FIRST_TOP_LEVEL_SEASON",
}

BEST_FINISH_LABELS = {
    "NATIONAL_CHAMPION": "National Champion",
    "NATIONAL_RUNNER_UP": "National Runner Up",
    "FINAL_FOUR": "Final Four",
    "ELITE_EIGHT": "Elite Eight",
    "SWEET_SIXTEEN": "Sweet Sixteen",
    "ROUND_OF_32": "Round of 32",
    "ROUND_OF_64": "Round of 64",
    "PLAY_IN_ROUND": "Play-in Round",
}

BEST_FINISH_RANK = {
    "PLAY_IN_ROUND": 1,
    "ROUND_OF_64": 2,
    "ROUND_OF_32": 3,
    "SWEET_SIXTEEN": 4,
    "ELITE_EIGHT": 5,
    "FINAL_FOUR": 6,
    "NATIONAL_RUNNER_UP": 7,
    "NATIONAL_CHAMPION": 8,
}

ROUND_TO_FINISH = {
    "Play-in": "PLAY_IN_ROUND",
    "R64": "ROUND_OF_64",
    "R32": "ROUND_OF_32",
    "Sweet Sixteen": "SWEET_SIXTEEN",
    "Elite Eight": "ELITE_EIGHT",
    "Final Four": "FINAL_FOUR",
}

VERIFICATION_STATUSES = {
    "OWNER_BASELINE_UNVERIFIED",
    "VERIFIED",
    "UNDER_REVIEW",
}

CANONICAL_CROSSCHECK_STATUSES = {
    "MATCH",
    "EXPLAINED_ADMIN_DIFFERENCE",
    "CONFLICT",
    "NOT_CHECKED",
    "CANONICAL_INCOMPLETE",
}

ACCOMPLISHMENT_COUNT_FIELDS = (
    "conference_regular_season_championships",
    "conference_tournament_championships",
    "ncaa_tournament_appearances",
    "final_four_appearances",
    "national_championships",
)


def valid_season_label(value: str) -> bool:
    match = SEASON_LABEL_RE.fullmatch(value.strip())
    if not match:
        return False
    return int(match.group(2)) == int(match.group(1)) + 1


def season_is_in_scope(season_label: str, history_start_season: str) -> bool:
    """Return whether a valid game season belongs to one program's perspective."""
    return (
        valid_season_label(season_label)
        and valid_season_label(history_start_season)
        and season_label >= history_start_season
    )


def scope_canonical_games(
    games: Iterable[dict[str, Any]],
    program_key: str,
    history_start_season: str,
) -> list[dict[str, Any]]:
    """Select canonical games that count for one program's approved perspective."""
    return [
        game
        for game in games
        if program_key in {game.get("team_a_key"), game.get("team_b_key")}
        and season_is_in_scope(
            str(game.get("season_label", "")), history_start_season
        )
    ]


def partition_source_rows(
    rows: Iterable[dict[str, str]], history_start_season: str
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Partition target source evidence without altering either set of rows."""
    in_scope: list[dict[str, str]] = []
    pre_cutoff: list[dict[str, str]] = []
    for row in rows:
        season = row.get("season_label", "").strip()
        if valid_season_label(season) and season < history_start_season:
            pre_cutoff.append(row)
        else:
            in_scope.append(row)
    return in_scope, pre_cutoff


def trim_conference_history(
    history_rows: Iterable[dict[str, str]], history_start_season: str
) -> list[dict[str, str]]:
    """Return public interval copies clipped to the program history boundary."""
    trimmed: list[dict[str, str]] = []
    for source in history_rows:
        start = source.get("start_season", "").strip()
        end = source.get("end_season", "").strip()
        if end and end < history_start_season:
            continue
        row = dict(source)
        if start < history_start_season:
            row["start_season"] = history_start_season
        trimmed.append(row)
    return trimmed


def history_scope_errors(program: dict[str, str], required: bool) -> list[str]:
    """Validate one program's explicit owner-approved perspective boundary."""
    errors: list[str] = []
    start = program.get("history_start_season", "").strip()
    status = program.get("history_scope_status", "").strip()
    basis = program.get("history_scope_basis", "").strip()

    if status not in HISTORY_SCOPE_STATUSES:
        errors.append(f"unknown history_scope_status {status!r}")
    if basis not in HISTORY_SCOPE_BASES:
        errors.append(f"unknown history_scope_basis {basis!r}")

    if required:
        if not valid_season_label(start):
            errors.append("valid history_start_season is required")
        if status != "OWNER_CONFIRMED":
            errors.append("history_scope_status must be OWNER_CONFIRMED")
        if basis not in HISTORY_SCOPE_BASES - {""}:
            errors.append("history_scope_basis is required")
    elif any((start, status, basis)):
        if not valid_season_label(start):
            errors.append("partially populated history scope needs a valid season")
        if not status or not basis:
            errors.append("history scope fields must be populated together")

    return errors


def _calendar_year(game: dict[str, Any]) -> int | None:
    game_date = str(game.get("game_date", "") or "")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", game_date):
        return int(game_date[:4])
    season = str(game.get("season_label", ""))
    if valid_season_label(season):
        return int(season.split("-")[1])
    return None


def _game_finish(game: dict[str, Any], program_key: str) -> str | None:
    round_name = str(game.get("postseason_round", "") or "")
    if round_name == "Championship":
        winner = str(game.get("result_winner_team_key", "") or "")
        if winner == program_key:
            return "NATIONAL_CHAMPION"
        if winner:
            return "NATIONAL_RUNNER_UP"
        return None
    return ROUND_TO_FINISH.get(round_name)


def derive_ncaa_accomplishments(
    canonical_games: Iterable[dict[str, Any]],
    program_key: str,
    history_start_season: str,
) -> dict[str, Any]:
    """Derive on-court NCAA accomplishments within one program's scope."""
    scoped = scope_canonical_games(
        canonical_games, program_key, history_start_season
    )
    ncaa_games = [g for g in scoped if g.get("game_type") == "NCAA_TOURNAMENT"]
    by_season: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for game in ncaa_games:
        by_season[str(game.get("season_label", ""))].append(game)

    incomplete: list[str] = []
    season_finishes: dict[str, tuple[str, int | None]] = {}
    for season, games in sorted(by_season.items()):
        candidates: list[tuple[int, str, int | None]] = []
        for game in games:
            finish = _game_finish(game, program_key)
            if finish:
                candidates.append(
                    (BEST_FINISH_RANK[finish], finish, _calendar_year(game))
                )
            elif game.get("postseason_round") == "Championship":
                incomplete.append(
                    f"{game.get('canonical_game_id', season)} championship winner is unresolved"
                )
        if not candidates:
            incomplete.append(f"{season} has no resolved NCAA round")
            continue
        best_rank = max(item[0] for item in candidates)
        best_candidates = [item for item in candidates if item[0] == best_rank]
        years = [item[2] for item in best_candidates if item[2] is not None]
        season_finishes[season] = (
            best_candidates[0][1], max(years) if years else None
        )

    final_fours = sum(
        BEST_FINISH_RANK[finish] >= BEST_FINISH_RANK["FINAL_FOUR"]
        for finish, _ in season_finishes.values()
    )
    championships = sum(
        finish == "NATIONAL_CHAMPION"
        for finish, _ in season_finishes.values()
    )

    if season_finishes:
        best_rank = max(
            BEST_FINISH_RANK[finish] for finish, _ in season_finishes.values()
        )
        best_finish = next(
            finish
            for finish, rank in BEST_FINISH_RANK.items()
            if rank == best_rank
        )
        best_years = [
            year
            for finish, year in season_finishes.values()
            if finish == best_finish and year is not None
        ]
        best_year = max(best_years) if best_years else None
        if not best_years:
            incomplete.append("best finish calendar year is unresolved")
    else:
        best_finish = None
        best_year = None

    conference_titles = 0
    for game in scoped:
        if (
            game.get("game_type") == "CONFERENCE_TOURNAMENT"
            and game.get("postseason_round") == "Championship"
            and game.get("result_winner_team_key") == program_key
        ):
            conference_titles += 1

    return {
        "ncaa_tournament_appearances": len(by_season),
        "final_four_appearances": final_fours,
        "national_championships": championships,
        "best_finish_key": best_finish,
        "best_finish_year": best_year,
        "conference_tournament_championships_supporting": conference_titles,
        "ncaa_game_count": len(ncaa_games),
        "incomplete_reasons": incomplete,
    }


def accomplishment_row_issues(
    row: dict[str, str],
    program: dict[str, str],
    public: bool,
) -> tuple[list[str], list[str]]:
    """Validate one normalized accomplishment row."""
    errors: list[str] = []
    warnings: list[str] = []
    values: dict[str, int] = {}

    for field in ACCOMPLISHMENT_COUNT_FIELDS:
        value = row.get(field, "").strip()
        if not re.fullmatch(r"\d+", value):
            errors.append(f"{field} must be a nonnegative integer")
        else:
            values[field] = int(value)

    status = row.get("verification_status", "").strip()
    crosscheck = row.get("canonical_crosscheck_status", "").strip()
    if status not in VERIFICATION_STATUSES:
        errors.append(f"unknown verification_status {status!r}")
    if crosscheck not in CANONICAL_CROSSCHECK_STATUSES:
        errors.append(f"unknown canonical_crosscheck_status {crosscheck!r}")

    if all(field in values for field in ACCOMPLISHMENT_COUNT_FIELDS):
        appearances = values["ncaa_tournament_appearances"]
        final_fours = values["final_four_appearances"]
        championships = values["national_championships"]
        if championships > final_fours:
            errors.append("national_championships exceeds final_four_appearances")
        if final_fours > appearances:
            errors.append("final_four_appearances exceeds ncaa_tournament_appearances")

        finish = row.get("best_finish_key", "").strip()
        year = row.get("best_finish_year", "").strip()
        if finish and finish not in BEST_FINISH_LABELS:
            errors.append(f"unknown best_finish_key {finish!r}")
        if appearances == 0:
            if finish:
                errors.append("zero NCAA appearances requires blank best_finish_key")
            if year:
                errors.append("zero NCAA appearances requires blank best_finish_year")
        else:
            if not finish:
                errors.append("positive NCAA appearances requires best_finish_key")
            if not year:
                message = "positive NCAA appearances requires best_finish_year"
                if not public and status == "UNDER_REVIEW":
                    warnings.append(message)
                else:
                    errors.append(message)

        if year:
            if not re.fullmatch(r"\d{4}", year):
                errors.append("best_finish_year must be a four-digit calendar year")
            else:
                history_start = program.get("history_start_season", "").strip()
                if valid_season_label(history_start):
                    first_calendar_year = int(history_start.split("-")[1])
                    if int(year) < first_calendar_year:
                        errors.append("best_finish_year predates history_start_season")

        if championships and finish and finish != "NATIONAL_CHAMPION":
            errors.append("a national champion must have NATIONAL_CHAMPION best finish")
        if finish == "NATIONAL_CHAMPION" and championships == 0:
            errors.append("NATIONAL_CHAMPION best finish requires a championship")
        if finish and BEST_FINISH_RANK.get(finish, 0) >= BEST_FINISH_RANK["FINAL_FOUR"] and final_fours == 0:
            errors.append("Final Four-or-better finish requires a Final Four appearance")

    if public:
        if status == "UNDER_REVIEW":
            errors.append("public accomplishment row cannot be UNDER_REVIEW")
        elif status == "OWNER_BASELINE_UNVERIFIED":
            warnings.append("public accomplishment row awaits source verification")
    if status == "VERIFIED" and crosscheck in {"CONFLICT", "CANONICAL_INCOMPLETE"}:
        errors.append("VERIFIED row cannot retain unresolved canonical conflict")
    if crosscheck == "CONFLICT" and status != "UNDER_REVIEW":
        errors.append("canonical CONFLICT requires UNDER_REVIEW verification status")

    return errors, warnings
