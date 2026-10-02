# nc-state research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: f486c8ca745a7a7c712813f86751c7c760c77240220935e254993553e8b875d8
- Research base SHA: 375f6b7e3f9cdb50833c245eab7e070b6d37c668
- Stage 3B status: COMPLETE
- Competitive games: 3,049
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 194
- NCAA_TOURNAMENT: 70
- NIT: 34
- REGULAR_SEASON: 2,751

## Final H/A/N census

- NEUTRAL: 446
- OPPONENT_HOME: 896
- SOURCE_PROGRAM_HOME: 1,704
- UNKNOWN: 3

## Stage 6 exact-date audit repairs

- Stage 6 recovered 176 exact dates from authoritative evidence without changing score, result, opponent, H/A/N, venue/location, game type, or raw source text.
- 170 recoveries use exact current-main published reciprocal package rows at protected main `f28f2b7aa078b9645e7000de5ea91508e65eaa27`, requiring a unique season + reciprocal-score match.
- 6 later malformed/omitted dates use the authoritative institutional sources listed in source-notes.md.
- Two 1927-28 North Carolina blank-date rows remained unresolved because reciprocal score matching produced two equally plausible games; no date was inferred.

## Stage 6 score-debt audit

- The Stage 6 adversarial pass found 11 rows with blank structured scores.
- Ten of those rows already preserved an unambiguous target-source score in `raw_text`; Stage 6 populated only `team_score` / `opponent_score` from that literal evidence and left every other accepted game fact unchanged.
- One 1912-13 Davidson reciprocal row genuinely lacks a recorded score and remains blank rather than inferred.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=a3be243463955837b1bda2b732481ebb59d07910` from `research_base_sha=375f6b7e3f9cdb50833c245eab7e070b6d37c668`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
