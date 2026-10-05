# louisville research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: 6825b230a27c69f321c6a65217d91fe1985f8d5560fb4ef85ab4fbaf270aaa10
- Research base SHA: 4bc113322e91c716299aa5c85f497c549e970b0e
- Stage 3B status: COMPLETE
- Competitive games: 2,991
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 147
- NCAA_TOURNAMENT: 123
- NIT: 31
- POSTSEASON: 6
- REGULAR_SEASON: 2,684

## Final H/A/N census

- NEUTRAL: 393
- OPPONENT_HOME: 1,091
- SOURCE_PROGRAM_HOME: 1,507

## Stage 5 NON_D1 owner sanity scan

- Complete population presented: 83 distinct NON_D1 identities / 459 games.
- Owner disposition: APPROVED with no flagged identities.
- Stage 5 approval changes no opponent mapping or historical game field.

## Stage 6 pre-freeze self-challenge

- Bounded adversarial audit performed under current protected main `fc22e5cd351d83bc1fa534ac74fed003ad41d9ac`.
- One concrete repair: `LOU-STG1-001987` (1996-11-29 vs Montana State, Big Island Invitational) exact venue recovered as Afook-Chinen Civic Auditorium, Hilo, HI.
- RESEARCHED_UNRESOLVED_HOME_VENUE: 169 rows remain; concentrated entirely in early overlapping Louisville home-facility eras through 1947-48, including four 1946-47 KIAC HOME tournament rows already researched to exhaustion. No new systematic allocation authority was found; survivors remain terminal researched debt.
- UNKNOWN H/A/N: 0.
- UNKNOWN exact dates: 0.
- Historical regular-season neutral building debt: 69 rows remain under the 1995-96-and-earlier location-first rule.
- Modern regular-season neutral exact-building debt: 0 after the one Big Island Invitational recovery.
- Non-NCAA postseason exact-building debt: 33 conference-tournament rows remain explicitly researched to exhaustion; no new concrete systematic source class was identified.
- Venue physical identities: 100 local venue rows; 91 current-main reuses, 9 settled new/pending-current-main-rebase candidates, 0 ambiguous matches.
- Opponent identities: Stage 5 owner scan approved; current-main program-registry exact-key and normalized-name collisions across the 83 NON_D1 identities: 0; known current-program key splits: 0; ambiguous current-program matches: 0.
- PRE-FREEZE SELF-CHALLENGE: PASS.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=d045a08b9b4c643f467b6ffbe621a411812c52c1` from `research_base_sha=4bc113322e91c716299aa5c85f497c549e970b0e`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
