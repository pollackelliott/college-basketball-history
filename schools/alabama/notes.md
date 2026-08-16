# Alabama curation notes

## 1. Program status and coverage

Alabama is curated from its first varsity season, **1912-13**, through the completed **2025-26** season. The owner confirmed that Alabama has always been D1/top-level for project purposes, so `history_start_season = 1912-1913` and public history begins at program inception. The 1943-44 no-team season creates no synthetic rows.

## 2. Competitive game count and on-court record

The package contains **2,968 recognized non-exhibition competitive games: 1,847-1,120-1 on court**. The Alabama all-time-results ledger contributes **2,933** competitive games through 2024-25 at **1,822-1,110-1**. The owner-supplied completed 2025-26 season contributes **35 games, 25-10**.

## 3. Exclusions and source-layout duplication

The historical guide contains **34 explicit exhibitions**, all excluded. The owner-supplied 2025-26 table contains **2 preseason exhibitions** (Florida State and Furman), also excluded. The canceled 2020 SEC Tournament entry is not a played game and is excluded. The 1948-49 source layout duplicates six consecutive played rows (Jan. 5 Auburn; Jan. 7 Georgia; Jan. 14 Georgia Tech; Jan. 18 Georgia; Jan. 20 LSU; Jan. 22 Tulane); each real game appears once in the package.

## 4. Date and source corrections

Exactly **180 competitive games remain without an exact date** because the supplied chronological ledger does not print one; no date is inferred from row order. The 2021-22 South Dakota State line loses its date in the media-guide text extraction, so the package uses **2021-11-12** from Alabama's official archived schedule. The 2024-11-11 McNeese row prints `W 64 72`; Alabama's official recap/schedule establish **Alabama W 72-64**, which is curated while the printed line remains in `raw_text`.

## 5. Site classification policy

Alabama's media-guide row prefixes are useful but not perfectly self-consistent with every published season Home/Road/Neutral heading. Explicit `at` and `vs.` markers are retained as source candidates. When an entire `at` or `vs.` prefix category would exceed that season's published road or neutral count, those conflicting rows remain `UNKNOWN` pending reciprocal/research reconciliation rather than forcing a contradictory site. An unprefixed row is assigned `SOURCE_PROGRAM_HOME` only when the complete original season prefix distribution reconciles exactly to the published H/A/N totals. This yields **954 home / 926 away / 487 neutral / 601 unknown** package site classifications. Venue chronology never establishes H/A/N. As an aggregate QA bound, the historical season headings, after restoring the three vacated 1987 NCAA games to the on-court neutral count, imply **1,352 home / 1,037 road / 544 neutral** competitive games through 2024-25; the owner-supplied 2025-26 season brings that to **1,367 / 1,047 / 554**. These aggregate totals are used as a consistency check only and never to manufacture game-level site assignments.

## 6. Owner-approved home-venue chronology

The owner-approved chronology is: no blanket primary venue for 1912-13 through 1913-14; Clark Hall for 1914-15 at season-level precision; Little Hall from 1915-16 through 1938-39; Foster Auditorium from 1939-40 through the January 1968 home schedule; Coleman Coliseum relationship beginning 1968-01-30, with Alabama's first game there on 1968-02-01 vs Samford, and Coleman thereafter. Primary-home venues are assigned only after a game is independently established as Alabama home.

## 7. Conference chronology

Owner-authoritative membership: Independent through 1920-21; Southern Conference 1921-22 through 1931-32; SEC from 1932-33 onward.

## 8. Postseason taxonomy

SIAA/Southern/SEC tournament contests are `CONFERENCE_TOURNAMENT`; NCAA games are `NCAA_TOURNAMENT`; true postseason NIT games are `NIT`. Named regular-season events, Preseason NIT, and NIT Season Tipoff remain `REGULAR_SEASON`. Public conference-tournament rounds remain blank except source-established championship games; NCAA rounds use the controlled project taxonomy.

## 9. Administrative actions

The three played 1987 NCAA Tournament games are retained with `administrative_status = VACATED_GAME`. Alabama's source says the NCAA Tournament appearance was later vacated; project policy retains the on-court scores/results and accomplishment history.

## 10. Opponent identity policy

Current Division-I programs reuse project identities and historical aliases where established. Historical clubs, YMCAs, military teams, and non-current colleges remain conservative distinct identities. `Howard` is normalized to Samford/Howard College; Samford's 1963-64 yearbook independently corroborates both Alabama games under the Howard College name. Pre-1918 `Southern` and `Birmingham College` remain separate predecessor institutions because Birmingham-Southern states its own official athletic history begins with the 1918 merger. Modern `Southern` resolves to Southern University. Historical Trinity College (N.C.) resolves to Duke, while the 1970s Trinity opponent remains Trinity (Texas). Miami uses project convention Miami (FL) = `miami`, Miami (OH) = `miami-oh`.

## 11. Accomplishment metadata

Owner-approved project totals are **11 conference regular-season championships, 9 conference tournament championships, 27 NCAA Tournament appearances, 1 Final Four, 0 national championships, Best Finish = Final Four, Best Finish Year = 2024**. The conference totals reconcile to Alabama's 9 SEC regular-season / 8 SEC Tournament titles plus the approved Southern Conference-era championships in the package's history scope. NCAA appearance totals follow the project on-court convention, retaining the vacated 1987 appearance and adding 2026.

## Package QA snapshot

- Games: 2,968
- On-court record: 1,847-1,120-1
- Historical through 2024-25: 2,933 games, 1,822-1,110-1
- 2025-26: 35 games, 25-10
- Excluded exhibitions: 36 total (34 guide + 2 owner-supplied)
- Canceled entries excluded: 1
- Duplicate source-layout copies excluded: 6
- Blank exact dates: 180
- Distinct canonical opponent keys: 314
- Site types: {'OPPONENT_HOME': 926, 'SOURCE_PROGRAM_HOME': 954, 'UNKNOWN': 601, 'NEUTRAL': 487}
- Game types: {'REGULAR_SEASON': 2713, 'CONFERENCE_TOURNAMENT': 151, 'NIT': 43, 'NCAA_TOURNAMENT': 61}
- Public postseason rounds: {'Championship': 15, 'R32': 20, 'Sweet Sixteen': 13, 'R64': 24, 'Elite Eight': 3, 'Final Four': 1}
- Established-home rows lacking curated primary venue: 8
- Rows without complete city/state: 1698

## Venue/location normalization
- MGM Grand Garden Arena uses the existing project canonical location `Paradise, NV`. Alabama's supplied 2025-26 source text says `Las Vegas, NV`; that wording remains preserved in source provenance/raw text. Site type was independently established as neutral and was not inferred from geography.
