# creighton research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: b81f97b866ff5bced7eb5e80d1b606ad2093e93b6e91d10fba507f9d81e125d8
- Research base SHA: 05dcc0ca58ed668f9a1cd2cf5a19648b1a14f13c
- Stage 3B status: COMPLETE
- Competitive games: 2,862
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 87
- NCAA_TOURNAMENT: 48
- NIT: 21
- POSTSEASON: 15
- REGULAR_SEASON: 2,691

## Final H/A/N census

- NEUTRAL: 239
- OPPONENT_HOME: 1,205
- SOURCE_PROGRAM_HOME: 1,414
- UNKNOWN: 4

## Stage 6 pre-freeze self-challenge repair

The adversarial self-challenge recovered H/A/N and locality for the four 1916-17 rows
previously carried as source-explicit UNKNOWN site:

- York — OPPONENT_HOME, York, NE
- Bellevue — OPPONENT_HOME, Bellevue, NE
- Doane — OPPONENT_HOME, Crete, NE
- Peru State — OPPONENT_HOME, Peru, NE

Creighton's current official 1916-17 schedule explicitly marks each as an away game and
supplies the opponent locality. The same page also explicitly states that the exact dates
for the four matches are unknown. Its displayed March 14 value is therefore preserved as
a presentation/CMS placeholder only and is not written into `game_date`.

The four exact-date blanks remain terminal researched historical debt.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=20518c9e999ac96ac27108e5841f86017bbd5274` from `research_base_sha=05dcc0ca58ed668f9a1cd2cf5a19648b1a14f13c`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

Owner-authorized Stage 1 conference-history reconciliation was applied during current-main integration; the exact correction specification and hash are recorded in the Integration Freeze manifest.
