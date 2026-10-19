# georgetown research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: 2c4d1da77f036f2e33602c219595c350ae5d3de21bd118f677dd385c3d815daf
- Research base SHA: a23b9aceb3b6aaa51e3cc012f4616c5cfc43b943
- Stage 3B status: COMPLETE
- Competitive games: 2,943
- Primary-source historical results cutoff: 2018-2019
- Required completed-season cutoff: 2025-2026
- Coverage cutoffs are explicit Research declarations; media-guide titles and filenames are not coverage inference rules.
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 106
- NCAA_TOURNAMENT: 77
- NIT: 29
- POSTSEASON: 3
- REGULAR_SEASON: 2,728

## Final H/A/N census

- NEUTRAL: 344
- OPPONENT_HOME: 1,178
- SOURCE_PROGRAM_HOME: 1,414
- UNKNOWN: 7

## Stage 6 bounded self-challenge repairs

- Owner NON_D1 sanity scan completed with no remaining flags; Florida Southern separately verified from South Florida.
- Exact-date systematic challenge recovered 29 dates: 25 from Georgetown official opponent-history tables, 3 from accepted protected-main reciprocal packages at `ddf1bb9e1fc0cbd90147f9f7aa13c6086faec7af`, and the 1942 Fordham date from agreeing Fordham institutional + Georgetown specialist evidence.
- No scores, H/A/N, venues, opponent identities, game types, or postseason classifications were changed.
- `GTG-S1-00180` North Carolina remains date-unresolved because Georgetown gives 1920-02-10 while accepted North Carolina reciprocal evidence gives 1920-02-09.
- `GTG-S1-00541` Marquette remains date-unresolved because the Georgetown specialist schedule gives 1942-02-06 while the accepted Marquette reciprocal gives 1942-02-07.
- Surviving blank dates are retained only after the bounded systematic exact-date opportunity was exhausted; Georgetown official opponent tables remain season-only for the remaining 1941-42 class.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=9b6d1ae3b03df3abcd201239cb27cc127f039833` from `research_base_sha=a23b9aceb3b6aaa51e3cc012f4616c5cfc43b943`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
