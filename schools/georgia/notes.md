# Georgia onboarding package notes

## Scope

- Program key: `georgia`
- Owner-confirmed public history start: **1905-1906**
- `history_scope_status`: `OWNER_CONFIRMED`
- `history_scope_basis`: `ALWAYS_TOP_LEVEL_FROM_INCEPTION`
- Competitive coverage: 1905-06 through completed 2025-26
- Exhibitions are excluded.

## Package QA snapshot

- Competitive source games: **2,958**
- On-court record: **1,536-1,422**
- Historical media-guide backbone through 2024-25: **2,925 games, 1,514-1,411**
- Completed 2025-26 supplement: **33 games, 22-11**
- Distinct source opponent labels: **333**, all resolved
- Canonical opponent identities represented: **295**
- H/A/N/Unknown source distribution: **1,446 / 1,124 / 340 / 48**
- Game types:
  - `REGULAR_SEASON`: **2,760**
  - `CONFERENCE_TOURNAMENT`: **145**
  - `NIT`: **31**
  - `NCAA_TOURNAMENT`: **21**
  - `POSTSEASON`: **1**
- Unknown exact dates: **2**
- Unknown played scores: **7**
- Venue rows: **48**
- Conference-tournament venue geography complete: **145 / 145**
- NCAA Tournament physical venue + city/state complete: **21 / 21**

## Owner ruling — 1987-88 Japan trip

The owner explicitly ruled the **Japan All-Stars** game on 1987-12-20 an **EXHIBITION** for project purposes. It is excluded from `source-games.csv`, public records, opponent series, venue statistics, and all competitive aggregates.

The preceding Japan-trip games against **New Orleans** and **UAB** remain competitive and are retained. This is a game-specific ruling, not a blanket exclusion of the trip.

This owner ruling also resolves the apparent 1987-88 ledger-count tension: after removal of the Japan All-Stars exhibition, the project season is 20-16.

## History scope

Georgia is treated as always top-level for site purposes beginning with the program's inaugural 1905-06 varsity season. This scope ruling is final for onboarding and should not be reopened during preflight.

## Conference chronology

- SIAA: 1905-06 through 1920-21
- Southern Conference: 1921-22 through 1931-32
- SEC: 1932-33 onward

The 1920-21 tournament is classified under Georgia's SIAA membership even though the media-guide footnote uses `SC Tournament-Atlanta`. The owner-authorized conference-tournament workbook identifies the 1920-21 SIAA tournament in Atlanta. Early joint SIAA/Southern tournament context is retained as provenance but does not create dual primary conference membership.

Conference-tournament package count through 2025-26 is **145**:
- SIAA: 4
- Southern Conference: 29
- SEC: 112

## Conference tournament sites

The owner-supplied universal Conference Tournament Site Reference is still under construction. Only its completed **SIAA, Southern Conference, and SEC** sections were authorized for Georgia and used here. No unfinished conference section was promoted to canon or applied to Georgia.

All 145 Georgia conference-tournament rows have a complete physical venue and city/state. The 2008 SEC Tournament is handled game-specifically: the opening Georgia Dome game remains at the Georgia Dome, while games after the tornado relocation use the Georgia Tech arena physical identity now represented by `McCamish Pavilion` (`VEN-000249`).

## Postseason

Georgia's package contains:
- **21 NCAA Tournament games** through 2026
- **31 NIT games**
- **1 generic POSTSEASON game**: the 1920 National Championship Tournament loss to Rutgers in Atlanta

Regular-season invitationals and tip-off events remain `REGULAR_SEASON`.

Working accomplishment values for Owner Gate 1 verification:
- Conference regular-season championships: **1** (1990)
- Conference tournament championships: **3** (1932 Southern; 1983 SEC; 2008 SEC)
- NCAA Tournament appearances: **14** through 2026, counting on-court appearances later vacated per project policy
- Final Fours: **1** (1983)
- NCAA national championships: **0**
- Best NCAA finish: **Final Four**
- Best-finish year: **1983**

## Administrative actions

Played results and scores remain on-court truth. Administrative action is stored separately.

The package preserves:
- 1985 NCAA Tournament: one later-vacated win and one later-vacated game/loss
- 2001-02 sanctions: affected wins beginning in January 2002 plus the NCAA Tournament loss, as indicated by Georgia's source notation
- 2002-03: all 19 on-court wins marked `VACATED_WIN`

The 2003-03-09 South Carolina row is structured as Georgia 60, South Carolina 55 in overtime from Georgia's official all-time South Carolina series; the chronological ledger's conflicting 65-60 text remains in `raw_text`.

## Source-internal and reciprocal discrepancies preserved

- **1962-63 Mississippi State:** the detailed Georgia ledger contains the real 1963-02-18 game, Mississippi State 86-75 Georgia. The game is retained even though Georgia's season summary is internally inconsistent. A reciprocal Mississippi State source also confirms the game.
- **2023-24:** the detailed ledger has 37 games and a 20-17 record; the season summary also supports 20-17 even though one chronological heading extraction is inconsistent.
- **1947-48 SEC Tournament vs Georgia Tech:** chronological ledger date is 1948-03-04 while the dedicated SEC Tournament history lists 1948-03-05. The package preserves the chronological source date for preflight reconciliation rather than silently collapsing the conflict.
- **1954-55 at Georgia Tech:** retained as 2OT from the chronological ledger / official opponent history despite an omission in Georgia's dedicated overtime table.
- **2014-15 LSU:** the chronological result/score is retained where the dedicated overtime table carries a conflicting score.

## Source normalization corrections

The package preserves the original `raw_text` while normalizing structured values where Georgia's own authoritative evidence resolves an internal defect. Notable examples include:
- 1956-12-27 Clemson: ledger prints an impossible `L 84-76`; normalized to a Georgia win.
- 1957-01-28 Alabama: ledger prints an impossible `W 73-89`; normalized to a Georgia loss.
- 1994-02-16 Florida: ledger prints `W 79-91`; normalized to a Georgia loss.
- 2015-03-03 Kentucky and 2021-11-23 Northwestern: reversed score order normalized from official season evidence.
- 2021-11-09 Florida International: malformed media-guide date token normalized from Georgia's official schedule context.
- 1911-12 Augusta YMCA, 1919-20 S.E. Christian College, and the 1925-26 Dahlonega/Westminster A.C. rows receive exact dates from Georgia Athletics' official historical schedule archive.

Two source rows still lack an authoritative exact date and remain blank rather than invented:
- 1908-09 Auburn, Georgia W 48-37
- 1928-29 Florida, Georgia W 48-32

Seven early rows preserve a known W result but genuinely unknown played score.

## Opponent identities

All 333 source labels resolve to 295 identities. Historical clubs, YMCAs, military teams, and defunct/non-Division-I schools remain conservative distinct identities unless a supported institutional lineage is established.

Important final shorthand/lineage resolutions include:
- `Birmingham` -> Birmingham Athletic Club
- `Columbus` -> Columbus YMCA
- `Nashville` -> Nashville Ramblers
- `Trinity` -> Duke
- `LSU-New Orleans` -> New Orleans
- `Baptist College` -> Charleston Southern
- `Pan American` -> UTRGV
- Augusta College/Augusta State -> Augusta University
- Columbus College -> Columbus State
- `Dahlonega` -> North Georgia

## Venue chronology and Phase-0 prerequisites

Venue chronology is never used to infer H/A/N. It only fills a physical venue after a game has independently been classified home.

Established Georgia home-facility evidence:
- Athens YMCA
- Alumni Hall
- The Octagon
- Moss Auditorium
- Woodruff Hall
- Georgia Coliseum / Stegeman Coliseum (same physical building)

The Octagon and Moss Auditorium overlap in the historical narrative. They are retained as physical identities, but the package does not blanket-assign ambiguous 1920-25 home games to either building.

Georgia Coliseum/Stegeman is one physical venue (`VEN-000198`). Georgia Athletics establishes the first varsity game in the building as **1964-02-22 vs Georgia Tech**, and the building was renamed Stegeman Coliseum on 1996-03-02.

The portfolio reserves six new global physical venue IDs after current main's `VEN-000274`; Codespace Phase 0 must add them to the global venue registry (and required name rows) before preflight:
- `VEN-000275` Athens YMCA
- `VEN-000276` Alumni Hall (Georgia)
- `VEN-000277` The Octagon
- `VEN-000278` Moss Auditorium
- `VEN-000279` Woodruff Hall
- `VEN-000280` TD Arena

No other new global venue identity is required by the six-file package.
