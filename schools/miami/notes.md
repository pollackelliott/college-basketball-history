# Miami (FL) research package notes

## Stage 6 audited package status and coverage

- School: Miami (FL)
- Program key: `miami`
- Research stage: `STAGE_6`
- Stage 5 owner NON_D1 sanity scan: `APPROVED` on 2026-09-29 with no flagged identities
- Stage 6 disposition: final adversarial pre-freeze self-challenge passed after two bounded repairs; Stage 7 has not begun
- Immutable `research_base_sha`: `5fa4d84e6b646a7c5e29f426905435c130caeee1`
- Protected-main SHA used for Stage 4 reconciliation: `953837e1da328fe4c8c99529b04ef91535194e4d`
- Authoritative Stage 3B COMPLETE parent SHA-256: `8d58df23776a733b4ebd0fa0e3bc1c0379c5451c61804e262885d23396cc98f4`
- Accepted top-level scope: `1948-49..1952-53 | 1954-55..1970-71 | 1985-86+`
- Package seasons represented: 63
- Competitive source rows: 1,842
- On-court record represented by the accepted package: 1,052-790
- Coverage cutoff: completed 2025-26 season, through 2026-03-22
- Exhibitions/noncompetitive events: excluded from the accepted competitive universe

This Stage 6 audited package preserves the accepted Stage 1 through Stage 3B durable state and the completed Stage 4/Stage 5 artifacts. Stage 6 did not restart historical research and did not alter protected-main shared state. The accepted project scope is narrower than Miami's full institutional basketball history; the package therefore does not attempt to reproduce the media guide's full all-time program record outside the owner-supplied top-level intervals.

## Game universe and source preservation

`source-games.csv` contains exactly the 1,842 stable game IDs from the Stage 3B working ledger. Literal game-row evidence is preserved in `raw_text`; accepted normalization is written to curated fields rather than replacing the source row. Three accepted historical rows retain blank exact dates rather than receiving inferred dates:

- `MIA-S1-1948-001` — Checker Cab
- `MIA-S1-1951-001` — Boca Chica
- `MIA-S1-1951-002` — Key West Navy

All accepted rows have complete played scores/results. No administrative-action status is currently required by the accepted Miami ledger.

## Opponent identity

- Opponent mapping rows: 295
- Distinct current-D1 program keys represented by current-D1 source labels: 244
- Distinct package identities currently classified NON_D1: 36
- Games against those NON_D1 identities: 193
- Unresolved opponent identities: 0

Current-D1 classification was rechecked read-only against protected main during Stage 4. The complete 36-entry NON_D1 population is serialized separately for the required Stage 5 owner sanity scan. Two accepted Stage 2 lineage/name corrections are also carried as informational self-corrections for owner visibility: `Baptist` -> Charleston Southern and `Teachers College of CT` -> Central Connecticut.

## Conference chronology

- 1948-49 through 1970-71: Independent
- 1985-86 through 1990-91: Independent
- 1991-92 through 2003-04: Big East
- 2004-05 through present: ACC

The accepted top-level scope contains no game rows for 1953-54 and no varsity rows from 1971-72 through 1984-85. Miami institutional history identifies BIG EAST competition beginning in 1991-92 and official ACC membership beginning July 1, 2004. Conference-tournament classification remains a game-level Stage 3B conclusion and is not inferred merely from membership.

## H/A/N and site completeness

Across all 1,842 accepted games:

- `SOURCE_PROGRAM_HOME`: 962
- `OPPONENT_HOME`: 663
- `NEUTRAL`: 217
- `UNKNOWN`: 0

The regular-season Stage 3A census remains 955 HOME / 650 OPPONENT_HOME / 125 NEUTRAL. The postseason Stage 3B census adds 7 HOME / 13 OPPONENT_HOME / 92 NEUTRAL.

Current package material-site accounting:

- source-program HOME rows with blank exact venue: 286
- source-program HOME rows missing normalized city/state: 0
- regular-season neutral exact-venue blanks: 39
- postseason exact-venue blanks: 1
- material site-gap rows: 326
- research-accounted material site-gap rows: 326
- unaccounted material site-gap rows: 0
- NCAA Tournament exact-site gaps: 0

The 286 HOME exact-venue exceptions are carried unchanged from accepted Stage 3A. Of those, 285 use the explicit one-time Miami-only owner locality disposition recorded on 2026-09-29: the exhausted historical HOME rows are normalized to Miami, FL even though that locality is not supported row-by-row, and their exact physical venue remains unresolved. One additional HOME row has independently supported Coral Gables, FL locality but no supported exact building. This one-time Miami disposition is not a repository-wide policy precedent.

Regular-season OPPONENT_HOME exact-building reconstruction remains outside Miami's source-school responsibility absent accepted exact venue evidence.

## HOME facility chronology and accepted exceptions

The accepted row-level package uses these documented modern/late historical physical-site relationships only after HOME classification was independently established:

- 1985-86 through 1987-88: James L. Knight Center, Miami, FL
- 1988-89 through 2002-12-30: Miami Arena, Miami, FL, including the first five 2002-03 HOME games
- 2003-01-04 through present: physical Watsco Center, Coral Gables, FL, under source-era names Convocation Center / BankUnited Center / Watsco Center
- 1971-02-01 through 1971-03-02 accepted HOME rows: Dinner Key Auditorium, Miami, FL
- selected 1960-61 and 1966-67 HOME rows: Miami Beach Auditorium, Miami Beach, FL, under the accepted Stage 3A default-plus-exceptions findings

The 1957-58 evidence establishes a split between Miami Beach Auditorium and the Coral Gables High gym but does not establish exact row membership; those rows therefore remain among the accepted exact-building exceptions instead of receiving an invented allocation.

## Regular-season neutral policy

Stage 3A is closed. Modern U.S. regular-season neutral games were researched under the strong exact-venue expectation. Two modern Puerto Rico rows remain without exact buildings under the already-accepted Stage 3A-3 locality-sufficient disposition. Historical 1995-96-and-earlier neutral rows use the location-first terminal standard: 37 retain explicit exact-building enrichment debt with supported locality after Stage 6 recovered Sullivan Arena for the 1987-11-27 Michigan game from the already-published exact reciprocal. The surviving residuals remain research-accounted terminal debt.

Four settled physical venue identities are not registered in the Research base/protected-main venue registry and therefore retain blank provisional numeric IDs for later current-main rebase:

- Dinner Key Auditorium — Miami, FL — 7 assigned games
- Miami Beach Auditorium — Miami Beach, FL — 21 assigned games
- Santander Arena — Reading, PA — 1 assigned game
- South Point Arena — Las Vegas, NV — 3 assigned games

For all four: `Historical identity: RESOLVED`; `Global registration: PENDING_CURRENT_MAIN_REBASE`. Research does not mutate the shared registry.

## Postseason closeout

Stage 3B is closed at 112 postseason rows:

- conference tournament: 58
- NCAA Tournament: 29
- NIT: 23
- other postseason: 2

All 112 postseason rows have H/A/N, locality, and a dispositioned source/public round. NCAA site completeness is 29/29. Exact physical venue is resolved for 111/112 postseason rows. The sole exhaustively researched survivor is `MIA-S1-1951-022`, Florida State in the 1952 NAIB District 25 first round: DeLand, FL is established, but the exact building remains `RESEARCHED_UNRESOLVED` after the accepted authoritative paths were exhausted. Potential DeLand buildings were not inferred.

Historical NCAA source-round wording is preserved separately from public canonical-round taxonomy. In particular, the 1960 Western Kentucky game retains source round `First Round` while the public canonical NCAA round remains blank, consistent with the repository treatment of pre-modern-bracket historical rounds.

## Accomplishment verification prepared for Implementation

The accepted Miami institutional evidence plus the completed 2025-26 postseason ledger supports the current project baseline:

- conference regular-season championships: 3 — 1999-2000 BIG EAST co-champion, 2012-13 ACC champion, 2022-23 ACC co-champion
- conference tournament championships: 1 — 2013 ACC Tournament
- NCAA Tournament appearances: 13, including 2025-26
- Final Four appearances: 1 — 2023
- national championships: 0
- best NCAA finish: Final Four
- most recent best-finish year: 2023

Stage 4 records the evidence state only; it does not mutate `data/reference/program-accomplishments.csv`.

## Cross-source reconciliations and preserved inconsistencies

Material accepted reconciliations remain visible in row notes rather than being erased:

- 2024 Tennessee: the media-guide event-family label conflicts with Miami exact-game evidence; the exact-game evidence resolves the contest to the Jimmy V Men's Classic at Madison Square Garden.
- 2008 NCAA Tournament: Miami's guide uses Little Rock, Arkansas wording while exact-game evidence establishes Alltel Arena in North Little Rock; the physical current-main identity is Simmons Bank Arena.
- 1952 Florida State NAIB District 25: accepted Stage 1 date remains 1952-02-29 despite a one-day discrepancy in Florida State retrospective material; Stage 3B did not reopen date authority.
- Historical/current arena naming is represented through one physical venue identity with source-era names preserved as aliases/evidence where the repository has an established physical identity.

Resolved Stage 3A/3B research bases that no longer describe a material site gap are preserved in row `notes` under resolved-evidence markers. `site_research_status` / `site_research_basis` are reserved for the 326 rows that still have a material site gap after Stage 6.

## Known unresolved questions

Current accepted research debt is explicit rather than silent:

- 3 historical exact-date blanks;
- 286 source-program HOME exact-building blanks with complete normalized locality and the accepted Stage 3A exception basis;
- 39 regular-season neutral exact-building blanks with explicit researched status;
- 1 exhaustively researched postseason exact-building blank (1952 NAIB District 25, DeLand);
- 4 resolved physical venue identities pending current-main registration/rebase.

None of these residuals is silently converted into certainty during Stage 4.

## Public presentation notes

Public opponent and venue display should use canonical package/current-registry identities, while raw/source names remain evidence. Conference-tournament presentation must resolve against the season-specific conference intervals above. Pending physical venue registrations must be reconciled during the serialized current-main rebase rather than assigned Research-time global numeric IDs.

## Stage 6 adversarial self-challenge

`PRE-FREEZE SELF-CHALLENGE: PASS`

The 286 `RESEARCHED_UNRESOLVED_HOME_VENUE` rows were challenged first as one population, not re-researched row-by-row. All are pre-1971. None carries a target-source venue token or event field that can safely assign a building. The accepted modern/late facility chronologies (James L. Knight Center, Miami Arena, Watsco Center, and the exact Dinner Key row range) have zero unresolved HOME rows inside their supported default intervals. The Miami Beach Auditorium evidence is row-specific rather than a continuous 1960-67 default: 77 unresolved HOME rows fall between its first and last accepted assignments, so the venue table now explicitly prevents chronology propagation from those bracketing dates. The 1957-58 Miami Beach Auditorium/Coral Gables High split still lacks row-level allocation. No HOME row was reopened or reassigned.

Targeted accepted-project checks were preferred over broad canonical/evidence retrieval. Protected main is only one policy/tooling commit ahead of `research_base_sha`, with no basketball data, school source-game, venue-registry, or program-registry changes in that compare. The eight surviving neutral-building rows that already carried published-reciprocal provenance were checked directly against their protected-main reciprocal rows. Seven remain locality-only; one exact defect was recovered: Michigan `MICHRAW-01588` explicitly names Sullivan Arena for `MIA-S1-1987-001` (1987-11-27), and protected main already registers that physical venue as `VEN-000361`. That row is repaired and no longer carries research-gap metadata.

The three blank exact dates remain terminal ancient/non-D1 debt: Checker Cab (1948-49), Boca Chica (1951-52), and Key West Navy (1951-52). The primary Miami ledger supplies no exact date and there is no newly identified concentrated institutional/reciprocal source class that justifies reopening them. The sole postseason building blank (`MIA-S1-1951-022`, 1952 NAIB District 25) remains exhaustively researched and unchanged.

Opponent identity challenge is clean: all 244 package identities marked current D1 still exist in protected-main `programs.csv` with current-D1 status, and none of the 36 owner-approved NON_D1 identities has an exact current-D1 key/name collision. Known current-program key splits: 0. Ambiguous current-program matches: 0.

Physical-venue identity challenge after the Sullivan repair: 63 local physical rows; 59 definite protected-main reuses; 4 genuinely new/pending current-main registrations (Dinner Key Auditorium, Miami Beach Auditorium, Santander Arena, South Point Arena); ambiguous physical identities: 0. Research does not register those four globally.

Final residual site debt after Stage 6: 286 HOME exact-building blanks; 39 regular-season neutral exact-building blanks (37 historical, 2 previously accepted Puerto Rico locality-sufficient rows); 1 exhaustively researched other-postseason building blank; 0 UNKNOWN H/A/N; 0 NCAA site gaps; 0 unaccounted material site gaps.

Stage 6 stops before Stage 7 immutable packaging. `RESEARCH_FROZEN` has not been declared by this Stage 6 artifact.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=34d43832b403db09123bc7c8860b85dfdf8460f3` from `research_base_sha=5fa4d84e6b646a7c5e29f426905435c130caeee1`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
