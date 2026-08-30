# Researched-Unresolved Home Venue Policy

This document records the owner-approved exception for historically unrecoverable published-program HOME venue identities.

## Governing principle

The project prefers an explicit, researched unknown over an invented physical venue identity.

A published program's HOME venue is ordinarily mandatory. The only permanent exception is a game for which deliberate historical research establishes the home city/state but the surviving record does not support a specific physical venue identity.

This exception exists to prevent false certainty. It is not a convenience mechanism and must never be used to avoid building a known home-venue chronology.

## Machine-visible status

Use `site_research_status=RESEARCHED_UNRESOLVED_HOME_VENUE` only when all of the following are true:

1. `curated_site_type=SOURCE_PROGRAM_HOME` is independently established. Venue/geography may not be used to infer H/A/N.
2. `city` and `state` are both populated.
3. `curated_venue_name` remains blank because the exact physical venue identity is genuinely unrecoverable after deliberate research.
4. `site_research_basis` documents the research performed and the reason stronger venue identification is unsupported.
5. No agreeing target-source or reciprocal assertion supplies a usable curated venue identity. If such evidence exists, it must be propagated or reconciled rather than waived.
6. NCAA Tournament strict site rules do not apply to the row.

The status may waive only `home_missing_venue`. It may never waive `home_missing_location` or `home_missing_both`.

## Canonical/public representation

When a source-side exception survives reconciliation into a canonical HOME game:

- canonical `site_city` and `site_state` remain populated;
- canonical venue fields remain blank rather than receiving a fabricated venue;
- canonical `notes` must contain the marker `[RESEARCHED_UNRESOLVED_HOME_VENUE ...]` tying the public unknown to its researched source provenance.

Implementation must reject the exception if known agreeing venue evidence exists or if the canonical location is incomplete.

## Reporting

Global published-site reporting must distinguish:

- true hard HOME blockers;
- researched-unresolved HOME venue exceptions; and
- fully venue-complete HOME games.

A researched-unresolved exception is therefore not silently treated as complete. It remains visible debt of a different, historically honest kind.

## Research standard

Before assigning this status, the research lane should review, as applicable:

- the program's official media guide / record book;
- institutional facility and archival history;
- contemporary newspapers or archival schedules when available;
- reciprocal published-program evidence;
- known venue chronology and transition dates;
- game-level location or special-site evidence.

A broad unexplored era, an absent first-pass venue table, or a generic claim that a site is "unknown" does not qualify.

## Owner ruling

Approved by the project owner on 2026-08-30. The governing intent is: a truthful researched blank is preferable to inventing a historical venue solely to satisfy a completeness counter.
