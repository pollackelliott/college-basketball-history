# Ohio State curation notes

## Program scope and coverage
Ohio State men's basketball is curated from program inception in **1898-99** through completed **2025-26**.

Owner ruling: **Ohio State has always been D1/top-level for site purposes.**  
Research baseline: `4c8d75592f98b42a8534182a5af9bf240b1fd16c`.

The immutable transport ZIP remains the **RESEARCH_FROZEN** research provenance. This tracked copy was rebased onto current main during Phase 0; the subsequent executable-preflight repair is documented below.

## Competitive history
- Competitive games: **3,125**
- On-court record: **1,908-1,217**
- 2025-26: **34 competitive games, 21-13**
- Exhibitions excluded: **Yes**
- Nine games have genuinely unknown exact dates; they remain blank rather than guessed.

The row-level record is on-court history and therefore differs from Ohio State's NCAA-adjusted administrative quick-facts record.

## 1992-93 omitted ledger game
The record-book 1992-93 page declares 15-13 but lists only 27 games. Ohio State's official historical schedule supplies the omitted **1992-12-01 home win over Ohio, 77-61**. It is carried as `official_historical_schedule_supplement`, preserving the fact that the current guide omitted the row.

## Source/OCR score normalizations
`raw_text` preserves the source wording. Supported normalized scores correct seven demonstrable orientation/OCR defects: Radford (1989), Detroit NCAA (1999), Louisville (2001), Pittsburgh (2001), Wisconsin (2005), Memphis (2015 OT), and Wisconsin (2020).

## NCAA vacaturs
The guide states that the NCAA vacated **113 games (82-31)** between 1998-99 and 2001-02 and marks affected individual games in italics. PDF font-level inspection confirms exactly 113 italicized game rows.

The package preserves on-court results and stores administrative status separately:
- `VACATED_WIN`: **82**
- `VACATED_GAME`: **31**

## H/A/N
H/A/N comes from explicit game-level source notation: unmarked home, `@`/`at` away, `vs.` neutral; 2025-26 uses the official schedule's Home/Away/Neutral field. Venue chronology never establishes H/A/N.

## Home facilities
Once HOME is independently established, facility chronology may fill venue/location:
- Armory: 1898 through 1919
- Coliseum: 1919 through 1956
- St. John Arena: first game 1956-12-01; primary home through 1997-98
- Value City Arena: first game 1998-11-13; primary home thereafter

Explicit later St. John return games and the 2020-21 Covelli Center footnote override the ordinary Value City fallback.

## Conference history
- 1898-99 through 1911-12: Independent
- 1912-13 onward: Big Ten

## Postseason
Big Ten Tournament games are classified from Ohio State's dedicated tournament table. The owner-supplied conference-tournament workbook is used **only** for its authorized complete Big Ten section and only for venue/city/state.

NCAA Tournament games are classified/site-normalized from the dedicated Ohio State NCAA table. Every NCAA row has venue/city/state populated. Historical NCAA stages are mapped to the project's controlled vocabulary only when the source and tournament structure support the equivalent. The 1944, 1945 and 1946 year-by-year ledgers explicitly mark the second tournament games as **Final Four**; their opening games in the eight-team field therefore map to **Elite Eight**. The 1950 C.C.N.Y. opening game likewise maps to **Elite Eight**, while the subsequent Holy Cross consolation game remains blank. The 1962 and 1971 regional progression and later bracket rounds are normalized consistently; opening first-round games in the 1979-84 expanded fields use `Play-in`, and 1985-and-later first rounds use `R64`. Historical third-place/consolation games remain `NCAA_TOURNAMENT` with blank public round.

The dedicated NCAA table also resolves one opponent contradiction: the 1950-03-23 tournament game was against **C.C.N.Y. (CCNY)**, not NYU. The chronological ledger's `New York Univ.` wording remains preserved verbatim in `raw_text`.

The package contains **30 NIT games**, matching Ohio State's 10 appearances and 21-9 on-court NIT record. Preseason NIT games remain regular season; only title games use `Championship`.

## Accomplishment evidence collected
Project accomplishment totals use **on-court history**, with later NCAA vacations stored administratively rather than erasing what was achieved on the court:
- Conference regular-season championships: **22**
- Big Ten Tournament championships: **5**
- NCAA appearances through 2025-26: **36**
- Final Fours: **11**
- National championships: **1**
- Best Finish: **National Champion**
- Best Finish Year: **1960**

Ohio State's current administrative quick facts show 20 conference titles, 4 Big Ten Tournament titles, 32 NCAA appearances and 10 Final Fours because the 1998-99 through 2001-02 NCAA action removes those achievements from current official totals. Contemporary Ohio State material documents the underlying on-court achievements: Big Ten regular-season titles in **2000 and 2002**, the **2002 Big Ten Tournament championship**, **four consecutive NCAA appearances from 1999 through 2002**, and the **1999 Final Four**. Those achievements are retained in the project's on-court accomplishment reference while the vacation remains separately preserved as administrative history.

## Provisional global venue IDs
All new research-time numeric venue allocations are provisional:
- Armory (Columbus, OH) -> `VEN-000281` **PROVISIONAL**
- Coliseum (Columbus, OH) -> `VEN-000282` **PROVISIONAL**
- Cow Palace (Daly City, CA) -> `VEN-000283` **PROVISIONAL**
- Cincinnati Gardens (Cincinnati, OH) -> `VEN-000284` **PROVISIONAL**
- Convocation Center (Athens, OH) -> `VEN-000285` **PROVISIONAL**
- Covelli Center (Columbus, OH) -> `VEN-000286` **PROVISIONAL**

These numeric values describe the frozen research-time proposals only. Phase 0 has completed the current-main rebase; tracked `venues.csv` and the integration-freeze manifest contain the integration assignments.

## Owner questions remaining
None.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=b8b543544cc97d993056537e3b7fc8d09258fa8c` from `research_base_sha=4c8d75592f98b42a8534182a5af9bf240b1fd16c`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
