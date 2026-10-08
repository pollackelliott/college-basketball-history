"""Conference registry and historical-membership safety helpers."""

from __future__ import annotations

import re
from collections.abc import Iterable


REQUIRED_REGISTRY_COLUMNS = {
    "conference_key",
    "conference_name",
    "tournament_label",
    "status",
    "notes",
}

REQUIRED_HISTORY_COLUMNS = {
    "source_program_key",
    "start_season",
    "end_season",
    "conference_key",
    "conference_name",
    "membership_type",
    "ongoing",
    "basis",
    "notes",
}

SEASON_RE = re.compile(r"^(\d{4})-(\d{4})$")


def season_start(value: str) -> int | None:
    match = SEASON_RE.fullmatch((value or "").strip())
    if not match or int(match.group(2)) != int(match.group(1)) + 1:
        return None
    return int(match.group(1))


def registry_by_key(rows: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        row.get("conference_key", "").strip(): row
        for row in rows
        if row.get("conference_key", "").strip()
    }


def matching_history_rows(
    history: Iterable[dict[str, str]], season_label: str
) -> list[dict[str, str]]:
    season = season_start(season_label)
    if season is None:
        return []
    matches = []
    for row in history:
        start = season_start(row.get("start_season", ""))
        end_text = row.get("end_season", "").strip()
        end = season_start(end_text) if end_text else None
        if start is not None and start <= season and (end is None or season <= end):
            matches.append(row)
    return matches


def resolved_history_key(
    history: Iterable[dict[str, str]], season_label: str
) -> str | None:
    matches = matching_history_rows(history, season_label)
    if len(matches) != 1:
        return None
    key = matches[0].get("conference_key", "").strip()
    return key if key and key != "independent" else None


def history_errors(
    rows: list[dict[str, str]],
    registry_keys: set[str],
    expected_program_key: str | None = None,
) -> list[str]:
    errors: list[str] = []
    # Preserve the complete row so documented, simultaneous dual conference
    # affiliations can be distinguished from accidental interval collisions.
    intervals: list[tuple[int, int | None, int, str, dict[str, str]]] = []

    for line_number, row in enumerate(rows, start=2):
        program_key = row.get("source_program_key", "").strip()
        conference_key = row.get("conference_key", "").strip()
        start = season_start(row.get("start_season", ""))
        end_text = row.get("end_season", "").strip()
        end = season_start(end_text) if end_text else None

        if expected_program_key and program_key != expected_program_key:
            errors.append(
                f"line {line_number}: source_program_key must be "
                f"{expected_program_key!r}, got {program_key!r}"
            )
        if conference_key not in registry_keys:
            errors.append(
                f"line {line_number}: conference_key {conference_key!r} is absent "
                "from data/reference/conferences.csv; stop for owner review"
            )
        if start is None:
            errors.append(f"line {line_number}: invalid start_season")
        if end_text and end is None:
            errors.append(f"line {line_number}: invalid end_season")
        if start is not None and end is not None and end < start:
            errors.append(f"line {line_number}: end_season precedes start_season")
        if start is not None and (not end_text or end is not None):
            intervals.append((start, end, line_number, conference_key, row))

    intervals.sort(key=lambda interval: (interval[0], interval[1] or 9999))
    for index, left in enumerate(intervals):
        for right in intervals[index + 1 :]:
            left_end = left[1]
            if left_end is not None and right[0] > left_end:
                break

            # An accepted Research record may explicitly document concurrent
            # affiliation with TWO distinct conferences in one season. Require
            # the same one-season interval, matching program, non-independent
            # identities, per-row source authority, and explicit dual-membership
            # documentation on BOTH rows. Never infer dual membership from the
            # overlap itself or allow open-ended / multi-season overlaps.
            same_single_season = (
                left[0] == right[0] == left[1] == right[1]
            )
            same_season_memberships = (
                sum(
                    1
                    for candidate in intervals
                    if candidate[0] <= left[0]
                    and (candidate[1] is None or left[0] <= candidate[1])
                )
                if same_single_season
                else 0
            )
            documented_dual = (
                same_single_season
                and same_season_memberships == 2
                and left[3] != right[3]
                and all(key and key != "independent" for key in (left[3], right[3]))
                and bool(left[4].get("source_program_key", "").strip())
                and left[4].get("source_program_key", "").strip()
                == right[4].get("source_program_key", "").strip()
                and all(
                    row.get("basis", "").strip()
                    and "concurrent dual conference membership"
                    in row.get("notes", "").casefold()
                    for row in (left[4], right[4])
                )
            )
            if not documented_dual:
                errors.append(
                    f"lines {left[2]} and {right[2]}: conference-history intervals overlap"
                )

    return errors


def explicit_tournament_conference_keys(
    event_texts: Iterable[str], registry: dict[str, dict[str, str]]
) -> set[str]:
    """Conservatively identify explicit '<conference> Tournament' evidence."""
    found: set[str] = set()
    for event_text in event_texts:
        event = " ".join((event_text or "").replace("\u2008", " ").split())
        if not event:
            continue
        for key, row in registry.items():
            candidates = {
                row.get("conference_name", "").strip(),
                row.get("tournament_label", "").strip(),
            }
            for candidate in candidates - {""}:
                pattern = (
                    rf"(?:^|[-/]\s*){re.escape(candidate)}(?:\s+Basketball)?"
                    rf"(?:\s+Post-Season)?\s+Tournament\b"
                )
                if re.search(pattern, event, flags=re.IGNORECASE):
                    found.add(key)
    return found
