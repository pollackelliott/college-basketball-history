# Mississippi State source notes

## Primary historical source

**2025-26 Mississippi State Men's Basketball Record Book / Media Guide**, Mississippi State Athletics.

Official archive page: https://hailstate.com/sports/2007/6/21/926767

Official full record-book PDF: https://static.hailstate.com/custompages/pdf/mbk/202526/MBKMediaGuide2025-26FullPage.pdf

Primary historical sections used:

- year-by-year results: record-book pp. 312-347 / physical PDF pp. 313-348
- tournament-history sections: record-book pp. 152-241
- opponent-series sections: record-book pp. 242-293
- Humphrey Coliseum history: record-book pp. 294-303

The year-by-year ledger is the primary chronological game source through 2024-25. `raw_text` preserves the printed game line for every historical row.

## Extraction reproducibility

The historical extraction yields **117 calendar-season entries from 1908-09 through 2024-25**, including four explicit no-team seasons. It produces **2,824 dated competitive game rows**, and each played season's extracted game count equals its printed season record total. Aggregate parity is **1,544-1,280** through 2024-25.

No OCR is used. Text is extracted directly from the PDF text layer.

## Completed 2025-26 season

The project owner supplied the completed 2025-26 schedule/results table. It contributes **32 competitive games and a 13-19 record**. The Houston preseason exhibition is excluded.

Mississippi State's official completed-season schedule is used as corroboration and controls two owner-resolved score discrepancies: Memphis (71-66) and Missouri (84-79). The owner-supplied raw values remain preserved in `raw_text`.

## Conference membership

Owner-approved chronology, corroborated by the record book:

1. SIAA — 1908-09 through 1920-21
2. Southern Conference — 1921-22 through 1931-32
3. SEC — 1932-33 onward

SIAA Tournament participation in 1921-22 and 1922-23 is postseason-event evidence and does not override the Southern Conference primary-membership interval.

## Conference-tournament site source

The uploaded `Conference_Tournament_Site_Reference(1).xlsm` is used **only as ephemeral Mississippi State onboarding evidence**. Per owner instruction, it is not asserted to be universally complete and must not be committed wholesale as a future/global reference. Relevant SIAA, Southern, and SEC tournament venue/city/state fields are transcribed into Mississippi State game rows only.

The workbook is complete for Mississippi State's relevant tournament-site needs according to the owner. Where the record-book heading conflicts with it (1945 SEC Tournament), the workbook controls curated venue/location and the conflicting record-book wording is retained for provenance.

## NCAA Tournament site evidence

NCAA games use exact city/state from the Mississippi State record book and established physical-venue identities consistent with NCAA/host records and the project's global venue registry. Historical venue names are retained as `source_venue_name` when the building has since been renamed; `curated_venue_name` uses the project's global display identity.

Examples include Jenison Fieldhouse (1963 East Lansing), Carrier Dome -> JMA Wireless Dome (1991 Syracuse), BSU Pavilion -> ExtraMile Arena (1995 Boise), RCA Dome -> Hoosier Dome physical identity (1996 Indianapolis), Charlotte Coliseum (2005), Alltel Arena -> Simmons Bank Arena (2008 North Little Rock), Rose Garden -> Moda Center (2009 Portland), and SAP Center (2019 San Jose).

## Venue hierarchy

1. explicit game/postseason source venue
2. owner-supplied conference-tournament site reference for relevant SIAA/Southern/SEC tournament games
3. established NCAA physical-site evidence for NCAA games
4. independently established primary-home chronology, but only for games already classified `SOURCE_PROGRAM_HOME`
5. source location tags for city/state only

Venue chronology never establishes or modifies H/A/N.

### Owner-approved Jackson site convention

For Mississippi State games played in **Jackson, MS**, the owner applies the same alternate-site convention used for Ole Miss in Jackson: games against Mississippi-based opponents remain **neutral**; games against out-of-state opponents are curated as **Mississippi State home games**. In this package that affects 33 Jackson games: **25 home and 8 neutral**. Raw source site markers remain preserved separately from the curated classification.

## Opponent normalization

The package contains **301 source opponent labels** and resolves each to a stable canonical key/name. Historical and non-current identities are retained rather than forced into current-D1 identities.

Biscayne College is normalized to the historical Florida St. Thomas University lineage (`st-thomas-university`, `current_d1=No`) and must not be merged with the modern D1 University of St. Thomas in Minnesota.

## Administrative results

Exactly 17 record-book rows in 2018-19 carry `[V]`. Those rows preserve their on-court result/score and receive `VACATED_WIN` administrative metadata.

## Exhibition treatment

No exhibition is included in the 2,856-game package. The explicit Oct. 26, 2025 Houston exhibition is excluded.

## Dedicated tournament-result cross-check

Mississippi State's dedicated **SEC Tournament Results** table (record-book p. 220) is treated as stronger game-specific evidence when it conflicts with the year-by-year ledger. That cross-check produces exactly three normalized corrections: 1936 Kentucky date to Feb. 28; 1943 Georgia Tech date to Feb. 26; and 1945 Georgia Tech to March 2 with a 60-43 score. The conflicting year-by-year strings remain preserved verbatim in `raw_text`.

For the 1926 Southern Conference Tournament, Mississippi State's official 1925-26 schedule establishes the North Carolina game as the tournament-ending loss, and Southern Conference historical tournament evidence identifies it as the championship game. Mississippi State's official source gives the score as 38-23; the conference historical record gives 37-23. The package preserves the Mississippi State score and documents the disagreement rather than silently reconciling it.

Mississippi State 1925-26 schedule: https://hailstate.com/sports/mens-basketball/schedule/1925-26

## Accomplishment verification

The owner approved cross-conference accomplishment totals of **10 regular-season conference championships** and **4 conference-tournament championships**.

Mississippi State's current record book identifies four early championship seasons (1911-12, 1912-13, 1913-14, 1915-16), six SEC regular-season championships (1959, 1961, 1962, 1963, 1991, 2004), the 1923 SIAA Tournament championship, and three SEC Tournament championships (1996, 2002, 2009). The record book's historical label "Southern Conference Champions" for the four early seasons is preserved as source wording; the project's independently approved conference chronology still places those seasons in the SIAA era.

The NCAA accomplishment fields remain: 14 NCAA Tournament appearances, 1 Final Four, 0 national championships, best finish Final Four, best-finish year 1996.

## Retroactive HOME-site remediation (2026-08-30)

The published-site hardening audit identified 168 Mississippi State canonical HOME games with missing venue and/or location. This remediation applies the owner-approved historical-unrecoverable HOME venue policy rather than inventing unsupported physical venue names.

- 139 Mississippi State source HOME rows are exhaustively researched but retain a blank physical venue under `RESEARCHED_UNRESOLVED_HOME_VENUE`; city/state remain complete. This comprises pre-Tin Starkville HOME games plus pre-1962 Jackson alternate-site HOME games, including the reconciled 1929 Kentucky game.
- 20 Jackson HOME rows beginning 1962-12-15 are assigned **Mississippi Coliseum**, supported by Mississippi State Athletics' official Jackson-game history and Mississippi Fairgrounds' 1962 facility history.
- 10 canonical-only HOME gaps are assigned from the already-established Tin Gym / McCarthy Gymnasium / Humphrey Coliseum chronology.
- `CBBG-0014851` is corrected from Kentucky HOME at Alumni Gym to Mississippi State alternate-site HOME in Jackson. UK Athletics' official all-time results marks both 1928-29 Mississippi A&M games as Kentucky away games, while Mississippi State places the 32-14 game in Jackson. The 1929-02-02 vs. 1929-02-03 source-date disagreement is preserved and not altered by this site-only correction.

Primary supporting sources:

- Mississippi State official historical record book / media guide and facility history.
- Mississippi State Athletics, official Jackson basketball breakdown identifying Mississippi Coliseum games beginning 1962-12-15.
- Mississippi Fairgrounds / Mississippi Department of Agriculture and Commerce history identifying Mississippi Coliseum as a 1962 facility.
- UK Athletics official men's basketball all-time results for 1928-29.

The unresolved HOME venue status is a permanent statement of historical uncertainty, not a placeholder for unfinished research. If stronger game-specific physical-venue evidence is later discovered, it should replace the exception.
