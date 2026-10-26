# gonzaga research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: eeccc55f30a659c3610791639f33dc0568a7ccd3fd62c7565bc36b7faf9b9f84
- Research base SHA: fa692b90a72bf32f56bba63c1e10c958513a42f7
- Stage 3B status: COMPLETE
- Competitive games: 2,053
- Primary-source historical results cutoff: 2025-2026
- Required completed-season cutoff: 2025-2026
- Coverage cutoffs are explicit Research declarations; media-guide titles and filenames are not coverage inference rules.
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 87
- NCAA_TOURNAMENT: 76
- NIT: 5
- REGULAR_SEASON: 1,885

## Final H/A/N census

- NEUTRAL: 388
- OPPONENT_HOME: 726
- SOURCE_PROGRAM_HOME: 814
- UNKNOWN: 125

## Stage 5 / Stage 6 closeout

The owner approved the complete Stage 5 NON_D1 sanity scan (39 distinct identities / 160 games) on 2026-10-25 with no flagged identities. Stage 6 then performed the required adversarial pre-freeze self-challenge. The only package defect found was the school-wide blank NCAA standardized-round field; all 76 NCAA rows were repaired from accepted institutional tournament-phase evidence plus NCAA bracket verification as documented in `source-notes.md`. No game identity, result, score, H/A/N, venue, opponent identity, conference classification, or postseason-site conclusion was otherwise changed.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=7226bad1cd2cff8cefcc0f7d44cb5b13179fd9b0` from `research_base_sha=fa692b90a72bf32f56bba63c1e10c958513a42f7`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
