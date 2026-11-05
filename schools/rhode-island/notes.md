# rhode-island research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: 719e35c4c7410318e0325b5a1a1226a6fd814574dceb9560e390caa7a6956031
- Research base SHA: 80b00278ac9add94702ac76c5fa310b95d2b1929
- Stage 3B status: COMPLETE
- Competitive games: 2,866
- Primary-source historical results cutoff: 2025-2026
- Required completed-season cutoff: 2025-2026
- Coverage cutoffs are explicit Research declarations; media-guide titles and filenames are not coverage inference rules.
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 76
- NCAA_TOURNAMENT: 18
- NIT: 30
- POSTSEASON: 4
- REGULAR_SEASON: 2,738

## Final H/A/N census

- NEUTRAL: 230
- OPPONENT_HOME: 1,217
- SOURCE_PROGRAM_HOME: 1,411
- UNKNOWN: 8

## Stage 6 NCAA round self-challenge

- All 18 NCAA Tournament games reviewed against the actual historical bracket era and preserved institutional source-round evidence.
- Controlled-round corrections applied only where historically one-to-one: 1978 first round -> R32; 1985+ first round -> R64; 1985+ second round -> R32.
- 1961 and 1966 historical First Round labels remain in source_round with curated_postseason_round blank because non-power-of-two fields/byes prevent an honest controlled-vocabulary equivalence.
- Existing Sweet Sixteen / Elite Eight assignments were retained where already supported.

## Stage 6 final pre-freeze synthesis

- PRE-FREEZE SELF-CHALLENGE: PASS.
- Owner NON_D1 sanity scan: APPROVED.
- UNKNOWN H/A/N: 9 starting; 1 recovered (1906-03-02 New Hampshire HOME at Lippitt Hall); 8 terminal early-history rows remain.
- Unknown exact dates: 1 starting; 1 recovered (1961-11-30 vs Pratt); 0 remain.
- HOME venue chronology: 1,411/1,411 rows challenged against 6 accepted relationships/exceptions; 0 conflicts; 0 unresolved HOME venues.
- Neutral/postseason site debt: 72 pre-1996 regular-season neutral rows remain location-complete exact-building enrichment debt; 2 modern regular-season neutral exact venues remain researched-unresolved; 2 1951 NEIT postseason exact sites/localities remain researched-unresolved after exhaustive authoritative paths.
- NCAA rounds: 18/18 reviewed; 13 controlled-round corrections; 3 already correct; 2 historically justified controlled-round blanks (1961 and 1966 historical First Round labels preserved in source_round).
- Physical venue identities: 69 local rows; 66 definite reuses (65 immutable-base + 1 additional current-main); 3 genuinely new candidates; 0 ambiguous identities.
- Opponent identities: 207 current-D1 keys checked; 105 NON_D1 identities challenged; 10 modern NON_D1 identities specifically reviewed; 0 known current-program key splits; 0 ambiguous current-program matches.
- Research acceptance: PASS with 0 errors, 0 warnings, 0 unresolved opponents, 0 HOME publication blockers, 0 NCAA site gaps, and 0 unaccounted material site gaps.
- Accepted target top-level scope: INCEPTION+ (1903-04+), owner-approved 2026-11-03; history_start_season=1903-1904, history_scope_status=OWNER_CONFIRMED, history_scope_basis=ALWAYS_TOP_LEVEL_FROM_INCEPTION.
- Current protected main lacked a reusable Rhode Island scope-reference row at freeze; serialized Implementation must reconcile this frozen scope into current-main reference state without reopening Research.
- RESEARCH_FROZEN: YES after exact current-main permanent acceptance passes on these six files.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=5492240bd889b0f2b946034529ef6562fdc9fbca` from `research_base_sha=80b00278ac9add94702ac76c5fa310b95d2b1929`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
