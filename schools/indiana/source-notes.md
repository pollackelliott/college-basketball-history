# Indiana source notes

## Principal source

**2025-26 Indiana Basketball Record Book**, Indiana University Athletics Strategic Communication Department.

High-value sections used directly:

- Year-By-Year Results — printed pp. 105-123
- NCAA Tournament Results — printed pp. 138-139
- Big Ten Tournament Results — printed pp. 140-144
- Hoosiers in Indianapolis — printed p. 145
- Hoosier Home Courts — printed pp. 244-246
- Assembly Hall historical material — printed pp. 247-248

The year-by-year section is the row-level chronological source. Dedicated postseason and facility sections are cross-check/evidence layers, not blanket replacements for the chronological ledger.

## Completed 2025-26 source

The project owner supplied a completed 2025-26 results table through the Big Ten Tournament. The package includes 32 competitive games (18-14) and excludes all foreign-tour/exhibition contests.

## Conference-tournament source

The owner supplied **Conference Tournament Site Reference** workbook. Its Big Ten section is complete for Indiana's tournament era (1998-2026). It is used as an ephemeral lookup source for shared physical venue/city/state only and is **not** ingested into the repository. Its own instructions explicitly prohibit using shared-site data to infer H/A/N.

## Venue hierarchy

1. explicit game/postseason source venue
2. established NCAA physical-site evidence for NCAA games
3. owner-supplied Big Ten shared-site reference for Big Ten Tournament venue/city/state
4. owner-confirmed Indiana primary-home chronology, but only after a row is independently classified `SOURCE_PROGRAM_HOME`
5. dedicated Indianapolis index for city/state enrichment where applicable

Venue chronology never establishes H/A/N.

NCAA Tournament status likewise never establishes neutral-site status by itself. Historical tournament games played as a true participant-home game remain H/A when explicit game-level evidence supports that classification. For Indiana, the 1981-03-20 UAB and 1981-03-22 St. Joseph's regional games at Assembly Hall are owner-confirmed Indiana home games; the ledger's original `vs.` wording remains preserved in `source_site_candidate`/`raw_text` as provenance.

## Home facility evidence

Indiana institutional/history material supports the physical succession from the original Assembly Hall to Men's Gymnasium, the 1928 Fieldhouse, the 1960 New Fieldhouse, and the 1971 Assembly Hall. For project display, the owner directs that the current Bloomington building be called **Assembly Hall** only.

## NCAA result-section conflicts

Indiana's dedicated NCAA Tournament Results section is useful for tournament participation, stage, and site city/state, but contains multiple transcription errors when compared with the chronological ledger and external archival evidence. Notable examples include:

- 1940 Springfield/Duquesne dates printed as March 20/21 in the NCAA section; NCAA archival history and the year-by-year ledger support March 22/23.
- 1953 DePaul score printed 92-80 in the NCAA section; the year-by-year ledger has 82-80.
- 1958 Notre Dame score orientation is reversed in the NCAA section; year-by-year correctly records Indiana's 87-94 loss.
- 1967 Virginia Tech date: year-by-year March 16, NCAA section March 17; archival evidence supports March 17.
- 1973 Providence third-place date: NCAA section March 25, year-by-year March 26; reciprocal archival schedule supports March 26.
- 1975 UTEP: year-by-year 78-52, NCAA section 78-53; NCAA bracket evidence supports 78-53.
- 1980 Virginia Tech: NCAA section prints 63-62; NCAA bracket/reciprocal evidence supports year-by-year 68-59.
- 1986 Cleveland State date: year-by-year March 13, NCAA section March 14; reciprocal evidence supports March 14.
- 1997 Colorado date: year-by-year March 11, NCAA section March 13; reciprocal evidence supports March 13.
- 1998 Connecticut: NCAA section prints Indiana 61, Connecticut 78; Connecticut archival material supports year-by-year Indiana 68, Connecticut 78.
- 2016 Chattanooga date is printed March 15 in the NCAA section; the chronological ledger's March 17 is retained.
- 2022 First Four / Saint Mary's dates are shifted two days later in the NCAA section; the chronological ledger's March 15 and March 17 dates are retained.
- 2023 NCAA section says `New Albany, N.Y.`; the tournament site is normalized to Albany, NY / MVP Arena.

These conflicts remain visible in documentation rather than being silently harmonized.

## Big Ten Tournament cross-check

The dedicated Big Ten section is used to verify tournament identity and venue history. It resolves the year-by-year score orientation for 1999 Illinois, 2005 Minnesota, and 2022 Iowa. The dedicated summary itself has at least two score typos (2006 Ohio State and 2022 Illinois), so the source is assessed game-by-game rather than treated as infallible.

## NIT treatment

The year-by-year footnotes explicitly identify postseason NIT games in 1971-72, 1978-79, 1984-85, 2004-05, 2016-17, and 2018-19. Preseason NIT appearances remain `REGULAR_SEASON`. The 1979 and 1985 NIT finals are marked `Championship`.

## Opponent identity research

Current D1 aliases are normalized to the repository program registry. Historical/non-current opponents are preserved as distinct identities rather than forced into modern programs. Specific lineage checks include:

- **Buchtel** -> Akron institutional lineage. University of Akron history states the institution now known as Akron was founded as Buchtel College and became the Municipal University of Akron in 1913.
- **Indiana Normal** -> Indiana State institutional lineage. Indiana State history traces the university to Indiana State Normal School.
- **NE Louisiana** -> UL Monroe lineage.
- historical names such as Memphis State, Colorado A&M, Southwest Missouri State, Houston Baptist, and Pan American are normalized to their established program lineages while source wording remains in `source_opponent_label` and `raw_text`.

Unclear athletic clubs, YMCAs, military teams, high schools, and other historical one-off identities are retained as historical/non-current stable source identities rather than speculatively merged.

## Supplemental research references

- NCAA historical championship/bracket material for old tournament dates, scores, rounds, and sites.
- Reciprocal school schedule/history material for selected pre-2000 NCAA conflicts.
- Vanderbilt Athletics official 2005 NIT recap for the Vanderbilt-at-Indiana site correction.
- Indiana University institutional facility-history material for the home-court chronology.

## Known aggregate mismatch

The official Quick Facts aggregate (1,950-1,131 through 2024-25) does not exactly reconcile to the year-by-year on-court ledger. The package intentionally preserves the row-level ledger instead of creating an unsupported synthetic result. See `notes.md` for the administrative-forfeit explanation and remaining one-win gap.
