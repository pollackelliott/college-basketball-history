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

---

## Accepted supplemental All-History expansion

# Hawai'i All-History expansion Research freeze notes

workflow_kind=ALL_HISTORY_EXPANSION
research_base_sha=2f6a0d7525cff222cfec0f286ed8e1c456707a54
researched institutional inception=1920-1921

The accepted published baseline is inherited authority and was not reopened. This artifact freezes only the supplemental EXPANSION_REQUIRED Research population from 1920-1921 through 1969-1970.

Accepted top-level classification remains the inherited `1970-71+` authority; this expansion changes publication coverage only and does not supersede top-level/D-I-equivalent scope.

Supplemental competitive-game universe: 812 identified varsity games across 45 active seasons; five expansion-required seasons are DORMANT_OR_NO_TEAM. The 34 identified pre-1920 rows are PRE_INCEPTION institutional basketball and therefore are not supplemental freeze exclusions.

Terminal early-history authority:
- 1922-23 National Guard is one identified competitive game with genuinely unknown result/score; no season aggregate allocation is used.
- 1924-25 institutional aggregate remains 7-3, while nine identified game rows total 7-2; the one-game/one-loss gap remains season-level debt and no anonymous game is invented.

Owner NON_D1 sanity scan: APPROVED on 2026-11-24; 194 distinct supplemental/touched NON_D1 identities, 540 games, zero flags, zero unresolved owner dispositions.

PRE-FREEZE SELF-CHALLENGE: PASS.
- UNKNOWN H/A/N: 472 terminal researched historical rows.
- RESEARCHED_UNRESOLVED_HOME_VENUE: 47 rows, all Honolulu, HI; zero HOME publication blockers.
- Historical regular-season neutral exact-building debt: 6 rows; locality complete.
- Postseason exact-site gaps: 0.
- Exact-date blanks after Stage 6 repair: 424.
- Unresolved opponent identities: 0.
- Known current-program key splits: 0.
- Ambiguous physical venue identities: 0.
- Genuine owner-level conflicts: NONE.

Stage 6 exact-date repair: hawai-i-exp-1964-65-005 vs San Francisco is dated 1964-12-14 from official San Francisco institutional year-by-year results; only the exact date changed.

Stage 6 package SHA-256: c741227c183c3410d43bf8dc458913b64315fb194e25dcc88985555d8c47bea5
Stage 6 checkpoint SHA-256: 69e7fdb4d64bba12bd61aa2b46233ef598623d2b0c1099b63f3fac13b83ecbf8
