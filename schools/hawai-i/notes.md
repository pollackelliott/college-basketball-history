# hawai-i research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: 2181adac6bc5ba87ca93d1efd4ca0986f16e910fe32f50feace092c964bc7fd0
- Research base SHA: 6a192223de544cd942100cce9c0a7565985c9784
- Stage 3B status: COMPLETE
- Competitive games: 1,649
- Primary-source historical results cutoff: 2022-2023
- Required completed-season cutoff: 2025-2026
- Coverage cutoffs are explicit Research declarations; media-guide titles and filenames are not coverage inference rules.
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Accepted top-level history scope

- Accepted target top-level scope: 1970-71+
- Current protected-main reusable scope authority at Stage 7: 1970-71+
- Reusable baseline disposition: CONFIRMED (not superseded)
- Owner-confirmed Research scope and current reusable scope authority agree exactly.

## Final game census

- CONFERENCE_TOURNAMENT: 65
- NCAA_TOURNAMENT: 7
- NIT: 18
- POSTSEASON: 3
- REGULAR_SEASON: 1,556

## Final H/A/N census

- NEUTRAL: 118
- OPPONENT_HOME: 512
- SOURCE_PROGRAM_HOME: 1,019

## Stage 6 bounded adversarial repairs

- Corrected one structured score pair (1975-02-22 Centenary, 95-89) from institutional game-history evidence while preserving the conflicting record-book literal in raw_text.
- Corrected two exact dates from authoritative reciprocal institutional evidence while preserving conflicting Hawai'i source literals in raw_text.
- Reviewed all 7 NCAA Tournament round assignments: 6 supported controlled round mappings added; the 1972 25-team First Round remains curated-round blank because no historically honest controlled-vocabulary mapping exists.
- No H/A/N, opponent identity, physical venue identity, score, result, or postseason membership changed.

## Post-freeze owner H/A/N correction — 2026-11-10

Explicit owner historical ruling supersedes the prior NEUTRAL classification for exactly three regular-season games:

- 1983-12-07 vs UNLV -> SOURCE_PROGRAM_HOME (Lahaina, HI; exact building remains unresolved and is not inferred).
- 2010-12-17 vs Chicago State -> SOURCE_PROGRAM_HOME at Lahaina Civic Center, Lahaina, HI.
- 2011-12-18 vs North Carolina A&T -> SOURCE_PROGRAM_HOME at War Memorial Gymnasium, Wailuku, HI.

All other previously accepted H/A/N classifications remain unchanged. Raw/source literals remain preserved. The prior immutable RESEARCH_FROZEN ZIP is retained as historical predecessor authority but is superseded by this owner ruling for these three H/A/N fields.

## Post-freeze owner venue ruling — 2026-11-10

- `hawai-i-1983-84-005` (1983-12-07 vs UNLV) remains `SOURCE_PROGRAM_HOME`.
- Owner explicitly assigns exact venue `Lahaina Civic Center`, Lahaina, HI.
- This supersedes the predecessor package's researched-unresolved HOME-building status for this one game.
- No other H/A/N, venue, opponent, score, date, game-type, or game-universe meaning is changed by this ruling.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=36b8e829e7e5ffde7390ec7ef00816cda3d7f663` from `research_base_sha=6a192223de544cd942100cce9c0a7565985c9784`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
