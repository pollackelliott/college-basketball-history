# pittsburgh research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: 9e9bc83de5af747f28d9d6bc5f381e6e7c7905b2f0f363df062645f6c794f763
- Research base SHA: 9666455b6fa34cfc69b16086433a3e53ff6008c6
- Stage 3B status: COMPLETE
- Competitive games: 2,979
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 92
- NCAA_TOURNAMENT: 54
- NIT: 15
- POSTSEASON: 8
- REGULAR_SEASON: 2,810

## Final H/A/N census

- NEUTRAL: 297
- OPPONENT_HOME: 1,165
- SOURCE_PROGRAM_HOME: 1,512
- UNKNOWN: 5

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=eaf9227ad16b5169e36fb5d460868b896fb0df8c` from `research_base_sha=9666455b6fa34cfc69b16086433a3e53ff6008c6`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.


## 2025-26 bounded post-publication correction

- Correction Research checkpoint SHA-256: 96c28c57d125a4f252216809ea26c8148e1fe11632a0cb568fc3a4187a7d8497
- Accepted competitive 2025-26 rows added to the source package: 33 (2 exhibitions excluded).
- Current package competitive games after correction: 3,012.
- Current game-type census after correction: 95 CONFERENCE_TOURNAMENT; 54 NCAA_TOURNAMENT; 15 NIT; 8 POSTSEASON; 2,840 REGULAR_SEASON.
- Current H/A/N census after correction: 301 NEUTRAL; 1,176 OPPONENT_HOME; 1,530 SOURCE_PROGRAM_HOME; 5 UNKNOWN.
- Canonical reconciliation topology remains 22 existing games / 11 genuinely new games; the 2026-01-27 Wake Forest overtime conflict is preserved for downstream Owner Gate 1.

