# Arizona men's basketball research notes

## Status
- School: Arizona
- Source program key: `arizona`
- Research base SHA: `3989158d6e461a3dfb7be919586c5b388f8ef83d`
- Owner-confirmed history scope: `INCEPTION+`
- Superseded protected-main scope at research start: `1947-48..1947-48|1950-51+`
- First covered season: 1904-05
- Final covered season: 2025-26
- Competitive games: 3,019
- On-court record: 2,013-1,005-1
- Stages 1-3B: COMPLETE
- Stage 4 six-file package QA: PASS
- Stage 5 owner NON_D1 sanity scan: APPROVED — 0 flags
- RESEARCH_FROZEN: NO
- CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES

## Scope and universe
- Owner overruled the old Arizona top-level scope and set Arizona to `INCEPTION+` on 2026-09-14.
- Research therefore preserves the competitive varsity universe from 1904-05 through completed 2025-26.
- The 1905-06 record is explicitly intrasquad-only and contributes zero competitive games.
- 122 season intervals reconcile mechanically; 3,019 competitive games produce the on-court record 2,013-1,005-1.
- Exact-date debt after Stage 6 reciprocal challenge: 142 rows (7 exact dates recovered). Exact-score debt: 21 rows. Unknown played result: 0.
- Four source score errors were repaired with stronger Arizona official evidence and one omitted 2022-23 competitive game was restored.
- Administrative history remains separate from played results: 2 `FORFEIT`, 69 `VACATED_WIN`, and 4 `VACATED_GAME` rows.

## Opponent identity
- 3,019 game rows map to 379 canonical opponent identities.
- Current-D1 identities: 243 / 2,638 games.
- Working `NON_D1`/historical identities: 122 / 367 games.
- Fourteen very early games have game-specific `RESEARCHED_UNKNOWN_IDENTITY` placeholders because the institutional source proves the games but not the opponents. These are not falsely classified as NON_D1.
- Unresolved normalization rows: 0.
- Known current-program key splits: 0.
- Ambiguous current-program matches: 0.
- Formal owner NON_D1 sanity scan: APPROVED on 2026-09-14; 0 owner flags.

## Site research
- Final all-game H/A/N: 1,477 SOURCE_PROGRAM_HOME / 1,153 OPPONENT_HOME / 377 NEUTRAL / 12 UNKNOWN.
- All 1,477 Arizona HOME rows have physical venue + Tucson, AZ geography; HOME publication blockers = 0.
- The 12 UNKNOWN H/A/N rows are aggregate-only early games from 1908-09 through 1911-12 whose game-level site evidence does not survive.
- 94 regular-season neutral rows retain complete geography but no safely established physical building; every row is explicitly `RESEARCHED_PARTIAL`. Stage 6 resolved all 14 previously blank neutral venues from 2000-01 onward.
- Postseason site debt: 0. NCAA, conference-tournament, NIT, and other postseason rows all have complete venue/city/state.
- NCAA physical venue + city/state gaps: 0.
- Ambiguous physical venue identities: 0.
- Unaccounted material site gaps: 0.

## Arizona home venue chronology
Herring Hall (1904-05 through 1920-21) -> Tucson National Guard Armory (1921-22 through 1924-25) -> Tucson High School (1925-26) -> Bear Down Gym (1926-27 through 1941-42) -> Tucson High School wartime displacement (1942-43 through 1943-44) -> Bear Down Gym (1944-45 through the pre-McKale era), with seven specifically footnoted 1971-72 home games at Tucson Community Center/Tucson Arena -> McKale Center beginning with Wyoming on 1973-02-01.

McKale is a definite research-base reuse (`VEN-000127`). Herring Hall, Tucson National Guard Armory, Tucson High School, Bear Down Gym, and Tucson Arena are historically resolved research identities whose global registration/reuse remains pending the authoritative current-main Implementation rebase.

## Postseason
- NCAA Tournament: 105 games, on-court 66-39, 40 appearance seasons through 2026.
- Conference tournament: 73 games.
- NIT: 4 games.
- Other controlled `POSTSEASON`: 7 games.
- Postseason H/A/N: 5 source-program home / 3 opponent home / 181 neutral / 0 unknown.
- 1943 and 1946 Border Conference tournament games are preserved as real postseason events in Albuquerque; Border tournament existence is not generalized beyond documented seasons.
- The 1953 Hardin-Simmons row is a Border/NCAA-representation playoff at Rose Field House and is physically `OPPONENT_HOME`.
- 1948 and 1949 NCAA District 6 playoffs remain project `POSTSEASON`, not `NCAA_TOURNAMENT`, consistent with Arizona's recognized NCAA appearance history.

## Conference history
Independent (1904-05–1930-31) -> Border Conference (1931-32–1960-61) -> Independent transition (1961-62) -> WAC (1962-63–1977-78) -> Pacific-10 Conference (1978-79–2010-11) -> Pac-12 (2011-12–2023-24) -> Big 12 (2024-25–present).

The Border Conference note in Arizona's record book is historically useful: travel restrictions prevented an official Border championship in 1943-44 and 1944-45. The project does not manufacture tournament rows from conference membership alone.

## Program-accomplishment verification
Current authoritative Arizona evidence through completed 2025-26 supports:
- 32 conference regular-season championships;
- 10 conference-tournament championships;
- 40 NCAA Tournament appearances;
- 5 Final Four appearances;
- 1 national championship;
- best finish `NATIONAL_CHAMPION`, 1997.

The 2026 Arizona Athletics regular-season-title release explicitly calls the title the program's 32nd regular-season conference championship; the 2026 Big 12 Tournament title is Arizona's first Big 12 Tournament championship, and the 2026 NCAA run is the program's fifth Final Four. The research-base `program-accomplishments.csv` row has 30 regular-season titles, so serialized Implementation should update that value to 32 after current-main rebase/validation. The other baseline fields match the completed 2025-26 evidence.

## Research-lane venue identity
- Local physical venue rows: 77.
- Definite research-base physical reuses: 68.
- Historically resolved identities pending current-main registration/reuse decision: 9.
- `venue_id` is intentionally blank throughout this Research package. Serialized Implementation performs the authoritative current-main physical-ID rebase.

## Required Implementation reference mutation
During serialized Implementation current-main rebase, update Arizona in `data/reference/program-top-level-scope.csv` to `INCEPTION+` through the controlled shared-reference mutation path. Research does not mutate protected main.

## Stage 5 owner checkpoint
The owner reviewed the complete 122-identity / 367-game NON_D1-historical population on 2026-09-14 and responded `Approved`. Owner flags: 0. Stage 5 did not change the six-file package.

## Stage 6 pre-freeze adversarial self-challenge
**PRE-FREEZE SELF-CHALLENGE: PASS**

Control Center challenge question: **If the Control Center challenged the largest unresolved/debt populations in this portfolio, what would it challenge?**

It would challenge the 142-row early exact-date debt, the 94-row researched-partial neutral exact-building debt, the 12 aggregate-only UNKNOWN H/A/N rows, the game-specific early unknown-opponent source facts, and the venue identities that appeared to require new global registration.

Bounded challenge results:
- **Exact dates:** published reciprocal packages and institutional schedules were checked for systematic recoveries. Seven dates were recovered (Texas Tech 5, USC 1, Purdue 1). The surviving 142 blanks are confined to 1904-05 through 1941-42 and remain source-limited historical debt; additional reciprocal candidates checked were also undated or contradictory.
- **Neutral exact buildings:** all 14 previously blank neutral venues from 2000-01 onward were resolved. The remaining 94 are entirely pre-2000, have complete city/state, and retain explicit `RESEARCHED_PARTIAL` basis. The modern systematic opportunity is exhausted; no comparable remaining authoritative batch source was identified.
- **UNKNOWN H/A/N:** all 12 are the accepted aggregate-only 1908-09 through 1911-12 placeholders. The Arizona institutional source does not preserve game-level opponent/site facts for those rows; they remain explicit `RESEARCHED_UNRESOLVED` rather than inferred.
- **Physical venue identity:** six Stage 4 pending-registration candidates were found already present in the research-base registry and reclassified as definite reuses: Anaheim Convention Center, Intuit Dome, Kaseya Center, Sullivan Arena, The Forum, and Fair Park Recreation Building. Five newly resolved modern neutral buildings are also definite research-base reuses. Madison Square Garden was repaired from one ambiguous textual label into the 1925-1968 and 1968-present physical buildings by game date. Final local venue state: 77 rows, 68 definite research-base reuses, 9 genuine pending current-main registration/reuse candidates, 0 ambiguous physical identities.
- **Opponent identity:** Stage 5 owner approval remains controlling (122 NON_D1/historical identities / 367 games; 0 flags). The two modern NON_D1 identities previously challenged remain Adams State and Chaminade; no current-program split or ambiguous current-program match is exposed. The 14 early actual-opponent-unknown games retain game-specific researched-unknown keys, so unresolved **normalization** mappings remain 0.
- **Universe/series:** all 122 season intervals still reconcile to the accepted 3,019-game universe and 2,013-1,005-1 on-court record. Stage 6 reciprocal/site checks exposed no additional omitted competitive game or modern series defect.

Terminal researched historical debt after bounded challenge:
- exact-date blanks: **142**
- UNKNOWN H/A/N: **12**
- regular neutral rows missing exact building but with complete geography and explicit research accounting: **94**
- HOME publication blockers: **0**
- NCAA site gaps: **0**
- postseason material site gaps: **0**
- unaccounted material site-gap rows: **0**
- unresolved opponent normalization mappings: **0**
- known current-program key splits: **0**
- ambiguous current-program matches: **0**
- ambiguous physical venue identities: **0**

Research acceptance errors: **0**. Research acceptance warnings: **0**.

`RESEARCH_FROZEN` remains **NO** until separately authorized Stage 7 immutable packaging.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=7c41810be02d4b21cebb2d747a0d079f2a0922f7` from `research_base_sha=3989158d6e461a3dfb7be919586c5b388f8ef83d`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
