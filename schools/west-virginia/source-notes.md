# West Virginia source notes

## Primary institutional source
**WVU 2023-24 Record Book / Media Guide** — owner-supplied institutional source (`WVU(3).pdf` in the recovery environment).
- Primary authority for the accepted historical all-time-score ledger through 2022-23, literal opponent labels, season totals, and postseason appearance evidence.
- The Stage 1 source register preserved the originally ingested owner-file SHA-256 `742476b2403dc6be725d23ad7940dcb3d1fddcffb757f964b7c03de40e120d7d`.

## Official WVU supplements
- WVU official athletics 2023-24 men's basketball schedule: https://wvusports.com/sports/mens-basketball/schedule/text/2023-24
- WVU official athletics 2024-25 men's basketball schedule: https://wvusports.com/sports/mens-basketball/schedule/text/2024-25
- WVU official athletics 2025-26 men's basketball schedule: https://wvusports.com/sports/mens-basketball/schedule/text/2025-26

## Research provenance
- Research base: `58a86ee6af72ea9c3b2bd388db772de5a9ff6fb3`.
- Stage 3B completion checkpoint SHA-256: `6b5287b09034c6098546dd5ab00d41d93658297d77b04583b3835573b9f4f48b`.
- Stage 4 checkpoint SHA-256: `a3d160d67b3caa018ad1f2b064bafc3b7e4fbcc4a8f9607c13d87092ea92a77f`.
- Stage 5 checkpoint SHA-256: `621d1ecc8405fa9e3fd4b38fe5f9147f8058857be070a2698532126b65494780`.
- Literal `raw_text`, source locator/page, raw opponent label, and raw location remain preserved per game in `source-games.csv`.
- Stage 6 did not alter accepted source-game IDs, H/A/N classifications, opponent normalization, game taxonomy, raw text, or source-page provenance.

## Stage 5 owner NON_D1 disposition
The owner reviewed the complete 90-identity / 536-game working NON_D1/historical population on 2026-09-19 and approved the list as presented with **0 owner flags**. During the scan the owner asked about the 1915-16 literal opponent label `West Lafayette`; bounded follow-up did not establish a Purdue identity, so the accepted NON_D1 normalization was retained unchanged.

## Stage 6 exact-site recoveries
Stage 6 used a bounded institutional/event/reciprocal challenge rather than reopening Stage 3A broadly.

### Far West Classic — Veterans Memorial Coliseum, Portland
Six accepted neutral rows were repaired to the exact physical building:
- 1966-12-28 Washington State
- 1966-12-29 Minnesota
- 1966-12-30 Saint Louis
- 1973-12-27 Washington
- 1973-12-28 Texas
- 1973-12-29 BYU

Principal evidence:
- WVU 2022 Portland State notes state that WVU's first seven games in Oregon were at Veterans Memorial Coliseum and that WVU participated in the Far West Classic in 1966 and 1973: https://wvusports.com/documents/download/2022/11/25/WVU-Portland_State_Notes_11-25-22.pdf
- West Virginia 1966-67 schedule evidence identifies Memorial Coliseum for all three 1966 Far West Classic games: https://www.sports-reference.com/cbb/schools/west-virginia/men/1967-schedule.html
- BYU's official 1973-74 schedule identifies Memorial Coliseum for the 1973-12-29 West Virginia game: https://byucougars.com/sports/mens-basketball/schedule/season/1973-1974

The research-base registry already contains the physical identity `veterans-memorial-coliseum-portland` / `VEN-000297`; numeric global IDs remain Implementation-authoritative.

### 1977 Big Sun Tournament — Bayfront Center
`WVU-STG1-01543`, 1977-12-09 vs Seton Hall, was repaired to Bayfront Center, St. Petersburg, FL.
- WVU official 1977-78 schedule preserves Big Sun Tournament / St. Petersburg context: https://wvusports.com/sports/mens-basketball/schedule/text/1977-78
- WVU schedule evidence identifies Bayfront Center: https://www.sports-reference.com/cbb/schools/west-virginia/men/1978-schedule.html
- Seton Hall reciprocal schedule evidence independently identifies Bayfront Center: https://www.sports-reference.com/cbb/schools/seton-hall/men/1978-schedule.html

Bayfront Center is preserved as a historically resolved local physical identity pending authoritative current-main registration/reuse determination.

### 1989 Palm Beach Classic — West Palm Beach Auditorium
`WVU-STG1-01913` (Boston College) and `WVU-STG1-01914` (Lehigh), 1989-12-27/28, were repaired to West Palm Beach Auditorium, West Palm Beach, FL.
- WVU official 1989-90 schedule confirms the Palm Beach Classic but reports the source location as Miami, Fla.; that literal source geography remains preserved in `source_site_candidate`/`raw_text`: https://wvusports.com/sports/mens-basketball/schedule/text/1989-90
- West Virginia schedule evidence identifies West Palm Beach Auditorium for both games: https://www.sports-reference.com/cbb/schools/west-virginia/men/1990-schedule.html
- Boston College reciprocal schedule evidence identifies West Palm Beach Auditorium on 1989-12-27: https://www.sports-reference.com/cbb/schools/boston-college/men/1990-schedule.html
- Lehigh reciprocal schedule evidence identifies West Palm Beach Auditorium on 1989-12-28: https://www.sports-reference.com/cbb/schools/lehigh/men/1990-schedule.html

The curated physical site uses West Palm Beach, FL while preserving the WVU source's Miami wording as a documented source-location discrepancy. West Palm Beach Auditorium remains a historically resolved local physical identity pending current-main registration/reuse determination.

## Stage 6 packaging repairs to accepted Stage 3A debt
Stage 4 accidentally converted accepted **exact-building** uncertainty into broader geography blanks on the terminal Stage 3A population. Stage 6 repaired the package mechanically without changing accepted H/A/N:
- the 52 neutral rows regained the accepted/source-supported city/state geography before exact-site recoveries were applied;
- `WVU-STG1-00314` retained HOME, regained Morgantown, WV geography, and now uses `RESEARCHED_UNRESOLVED_HOME_VENUE` with a substantive basis.

After nine exact-site recoveries, terminal research debt is 43 neutral exact-building blanks plus the one HOME exact-building blank. All 44 retain complete geography and explicit research accounting.

## Stage 6 reciprocal challenge
Three accepted WVU neutral games against Maryland in Cumberland, MD were compared with Maryland's current published package, which labels them as at West Virginia. WVU's current official historical schedule/opponent-history evidence places those games in Cumberland. Stage 6 therefore retained the accepted WVU neutral classification and records the reciprocal-package disagreement rather than silently adopting the conflicting Maryland assertion.

## Stage 6 physical-venue identity challenge
Local venue identities were reconciled against the research-base `data/reference/venues.csv` and `venue-names.csv`. Naming-era labels and aliases were collapsed only when they represented the same physical building; raw/source venue evidence remains preserved in `source-games.csv`.

Examples of physical-identity evidence used in the bounded challenge include:
- The Pit / Bob King Court: University of New Mexico facility history identifies Bob King Court as the court inside The Pit: https://golobos.com/the-pit
- Harold J. Toso Pavilion / Leavey Center: Santa Clara facility history identifies Leavey as the reconstructed/former Toso Pavilion physical facility.
- U. of U. Special Events Center / Jon M. Huntsman Center: Utah facility history identifies the Special Events Center as the same building later renamed for Jon M. Huntsman.
- Birmingham-Jefferson Civic Center/Coliseum / Legacy Arena: BJCC facility history supports the naming-era continuity.
- Cleveland arena naming eras: official arena history supports Gund Arena -> Quicken Loans Arena -> Rocket Mortgage FieldHouse -> Rocket Arena as one physical building.
- Blue Cross/Blue Shield Arena / Rochester War Memorial: Rochester facility history ties the arena to the War Memorial physical building.

Final local physical venue state: **124** rows = **93** definite research-base reuses, **27** historically resolved pending current-main registration/reuse decisions, and **4** historically resolved cases where the research-base shared registry itself contains duplicate/competing IDs. Those four shared-registry cases are deferred to serialized Implementation; Research does not mutate shared registries or choose an authoritative global numeric ID.

## Postseason
All 248 postseason rows remain closed: conference tournament 143/143; NCAA 63/63; NIT 37/37; other postseason 5/5. NCAA exact physical venue + city + state gaps are zero. Stage 6 introduced no postseason taxonomy changes.

## Preserved Old Dominion contradiction
`WVU-STG1-01812` (1986-03-13 vs Old Dominion) remains a narrow internal WVU source conflict: accepted Stage 1 score 64-72 versus 62-74 in the WVU Postseason Appearances table. The accepted disposition remains `OPEN_NARROW_SCORE_CONFLICT_STAGE1_REMAINS_CONTROLLING`; Stage 6 did not reopen it.

## Shared-reference boundary
Research preserves historically resolved opponent and venue identities. Numeric/global shared IDs remain provisional where current-main reconciliation is required. This Research lane does not mutate protected shared registries; serialized Implementation performs the authoritative current-main identity rebase later.

## Stage 6 disposition
**PRE-FREEZE SELF-CHALLENGE: PASS.** Final Stage 6 QA has 0 research/package acceptance errors and 0 warnings; HOME publication blockers 0; NCAA site gaps 0; unaccounted material site gaps 0; known current-program key splits 0; ambiguous current-program matches 0; ambiguous historical physical venue identities 0.

`RESEARCH_FROZEN` remains **NO**. Stage 7 immutable final packaging is separately owner-authorized work and has not been performed.
