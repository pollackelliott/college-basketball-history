#!/usr/bin/env python3
"""Shared location/provenance safeguards for onboarding and publication."""

from __future__ import annotations

import re
from collections import defaultdict


SOURCE_ASSERTION_SYNC_FIELDS = (
    "game_date",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
    "event_or_tournament",
    "raw_text",
)

REGISTRY_FALLBACK_PREFIX = "[VENUE_REGISTRY_FALLBACK "
VENUE_LOCATION_VARIANT_MARKER = "VENUE_LOCATION_VARIANT:"

_REGISTRY_FALLBACK_RE = re.compile(
    r"\[VENUE_REGISTRY_FALLBACK "
    r"source=([^/;\]]+)/([^;\]]+);"
    r"venue_key=([^;\]]+);site_type=([^;\]]+);fields=([^\]]+)\]"
)

_NARRATIVE_CITY_PATTERNS = (
    re.compile(r"\byearly\s+resul", re.IGNORECASE),
    re.compile(r"\bfirst\s+ap\s+ranking\b", re.IGNORECASE),
    re.compile(r"\bplayed\s+in\b", re.IGNORECASE),
    re.compile(r"\bneutral[- ]site\b", re.IGNORECASE),
)


def location_pair_status(city: str, state: str) -> str:
    """Return ``complete``, ``blank``, or ``partial`` for a location pair."""
    has_city = bool((city or "").strip())
    has_state = bool((state or "").strip())
    if has_city and has_state:
        return "complete"
    if not has_city and not has_state:
        return "blank"
    return "partial"


def public_location_pair(city: str, state: str) -> tuple[str | None, str | None]:
    """Suppress legacy partial geography rather than publishing half a pair."""
    if location_pair_status(city, state) != "complete":
        return None, None
    return city.strip(), state.strip()


def obvious_city_contamination(
    city: str,
    source_venue_name: str = "",
    curated_venue_name: str = "",
    registry_venue_names: set[str] | None = None,
) -> str | None:
    """Identify a small, deterministic set of invalid normalized-city forms."""
    value = (city or "").strip()
    if not value:
        return None

    folded = value.casefold()
    venue_names = {
        name.strip().casefold()
        for name in (
            source_venue_name,
            curated_venue_name,
            *(registry_venue_names or set()),
        )
        if name and name.strip()
    }
    if folded in venue_names:
        return "city equals a source/curated venue name"
    if " and " in folded:
        return "city contains a combined multi-city value"
    if any(pattern.search(value) for pattern in _NARRATIVE_CITY_PATTERNS):
        return "city contains narrative or footnote text"
    if any(character in value for character in ("%", "\n", "\r", "\t")):
        return "city contains extraction-control or footnote characters"
    return None


def source_location_preflight(
    rows: list[dict[str, str]],
    existing_source_pairs: set[tuple[str, str]],
    registry_venue_names: set[str],
) -> tuple[list[str], list[str]]:
    """Validate new source rows while grandfathering identical legacy defects."""
    errors: list[str] = []
    warnings: list[str] = []
    for line_number, row in enumerate(rows, start=2):
        program = row.get("source_program_key", "").strip()
        source_id = row.get("source_game_id", "").strip()
        label = source_id or f"line {line_number}"
        existing = (program, source_id) in existing_source_pairs
        city = row.get("city", "")
        state = row.get("state", "")

        problem = None
        if location_pair_status(city, state) == "partial":
            problem = "partial normalized location; city and state must be both populated or both blank"
        else:
            problem = obvious_city_contamination(
                city,
                row.get("source_venue_name", ""),
                row.get("curated_venue_name", ""),
                registry_venue_names,
            )

        if problem:
            message = f"{label}: {problem}"
            (warnings if existing else errors).append(message)
    return errors, warnings


def assertion_drift(
    source: dict[str, str], assertion: dict[str, str]
) -> dict[str, tuple[str, str]]:
    """Compare only fields copied from one source row into its own assertion."""
    return {
        field: (source.get(field, ""), assertion.get(field, ""))
        for field in SOURCE_ASSERTION_SYNC_FIELDS
        if source.get(field, "") != assertion.get(field, "")
    }


def source_site_agrees_with_canonical(
    source: dict[str, str], canonical: dict[str, str]
) -> bool:
    """Return whether independently curated source H/A/N matches canonical H/A/N."""
    program = source.get("source_program_key", "").strip()
    opponent = source.get("normalized_opponent_key", "").strip()
    site = source.get("curated_site_type", "").strip()
    if not program or not opponent or site == "UNKNOWN" or not site:
        return False
    team_a, _ = sorted((program, opponent))
    if site == "SOURCE_PROGRAM_HOME":
        candidate = "TEAM_A_HOME" if program == team_a else "TEAM_B_HOME"
    elif site == "OPPONENT_HOME":
        candidate = "TEAM_A_HOME" if opponent == team_a else "TEAM_B_HOME"
    elif site == "NEUTRAL":
        candidate = "NEUTRAL"
    else:
        return False
    return candidate == canonical.get("site_type", "").strip()


def atomic_location_enrichments(
    canonical_city: str,
    canonical_state: str,
    candidate_city: str,
    candidate_state: str,
) -> list[tuple[str, str]]:
    """Return fills only when the resulting canonical pair will be complete."""
    if location_pair_status(candidate_city, candidate_state) != "complete":
        return []

    can_city = (canonical_city or "").strip()
    can_state = (canonical_state or "").strip()
    new_city = candidate_city.strip()
    new_state = candidate_state.strip()
    status = location_pair_status(can_city, can_state)

    if status == "blank":
        return [("site_city", new_city), ("site_state", new_state)]
    if status == "complete":
        return []
    if can_city and can_city == new_city:
        return [("site_state", new_state)]
    if can_state and can_state == new_state:
        return [("site_city", new_city)]
    return []


def registry_fallback_marker(
    source_program_key: str,
    source_game_id: str,
    venue_key: str,
    site_type: str,
    fields: list[str] | tuple[str, ...],
) -> str:
    """Create a deterministic, machine-readable audit marker in canonical notes."""
    field_text = ",".join(sorted(set(fields)))
    return (
        f"{REGISTRY_FALLBACK_PREFIX}"
        f"source={source_program_key}/{source_game_id};"
        f"venue_key={venue_key};site_type={site_type};fields={field_text}]"
    )


def append_note(existing: str, marker: str) -> str:
    existing = (existing or "").strip()
    if marker in existing:
        return existing
    return f"{existing} {marker}".strip()


def parse_registry_fallback_markers(notes: str) -> list[dict[str, str]]:
    """Parse deterministic registry-fallback audit markers from canonical notes."""
    return [
        {
            "source_program_key": match.group(1),
            "source_game_id": match.group(2),
            "venue_key": match.group(3),
            "site_type": match.group(4),
            "fields": match.group(5),
        }
        for match in _REGISTRY_FALLBACK_RE.finditer(notes or "")
    ]


def venue_location_conflicts(
    registry_rows: list[tuple[str, dict[str, str]]],
) -> list[str]:
    """Find incompatible complete locations for a stable venue key."""
    by_key: dict[str, list[tuple[str, dict[str, str]]]] = defaultdict(list)
    for path, row in registry_rows:
        key = row.get("venue_key", "").strip()
        if key:
            by_key[key].append((path, row))

    conflicts: list[str] = []
    for key, entries in sorted(by_key.items()):
        locations = {
            (row.get("city", "").strip(), row.get("state", "").strip())
            for _, row in entries
            if location_pair_status(row.get("city", ""), row.get("state", "")) == "complete"
        }
        if len(locations) <= 1:
            continue
        if all(
            VENUE_LOCATION_VARIANT_MARKER in row.get("notes", "")
            for _, row in entries
        ):
            continue
        rendered = "; ".join(
            f"{path}={city}, {state}" for path, row in entries
            for city, state in [(row.get("city", "").strip(), row.get("state", "").strip())]
        )
        conflicts.append(f"venue_key {key!r} has incompatible registry locations: {rendered}")
    return conflicts
