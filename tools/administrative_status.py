"""Controlled administrative-result vocabulary for game-source integration."""

from __future__ import annotations

from typing import Any


ALLOWED_ADMINISTRATIVE_STATUSES = {
    "",
    "FORFEIT",
    "VACATED_GAME",
    "VACATED_WIN",
}

LEGACY_VACATED_SEASON_CONTEXT = "VACATED_SEASON_CONTEXT"


def administrative_status_errors(
    row: dict[str, Any],
    label: str,
) -> list[str]:
    """Validate one source/canonical administrative-result representation."""

    status = str(row.get("administrative_status", "") or "").strip()
    note = str(row.get("administrative_note", "") or "").strip()

    errors: list[str] = []
    if status not in ALLOWED_ADMINISTRATIVE_STATUSES:
        errors.append(
            f"{label}: invalid administrative_status {status!r}; "
            "allowed values are blank, FORFEIT, VACATED_GAME, or VACATED_WIN"
        )
    if status and not note:
        errors.append(
            f"{label}: administrative_note is required when "
            "administrative_status is populated"
        )
    return errors


def normalize_legacy_vacated_season_context_row(
    row: dict[str, str],
) -> tuple[dict[str, str], bool]:
    """Normalize the retired season-context sentinel to game-level status.

    The legacy sentinel represented a season-level statement that victories were
    later vacated. The already-settled on-court W/L remains unchanged:
    wins become VACATED_WIN; non-wins receive no game-level administrative status.
    The original administrative note is preserved verbatim.
    """

    status = row.get("administrative_status", "").strip()
    if status != LEGACY_VACATED_SEASON_CONTEXT:
        return dict(row), False

    note = row.get("administrative_note", "").strip()
    folded_note = note.casefold()
    if not note or "vacat" not in folded_note or "victor" not in folded_note:
        raise ValueError(
            "VACATED_SEASON_CONTEXT may be normalized only when the preserved "
            "administrative note explicitly states that victories were vacated"
        )

    played = row.get("played_result", "").strip().upper()
    if played not in {"W", "L", "T"}:
        raise ValueError(
            "VACATED_SEASON_CONTEXT normalization requires a settled W/L/T "
            "played_result"
        )

    normalized = dict(row)
    normalized["administrative_status"] = (
        "VACATED_WIN" if played == "W" else ""
    )
    return normalized, True
