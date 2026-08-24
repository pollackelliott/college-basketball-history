# Ohio State curation notes

## Program scope and coverage
Ohio State men's basketball is curated from program inception in **1898-99** through completed **2025-26**.

Owner ruling: **Ohio State has always been D1/top-level for site purposes.**  
Research baseline: `4c8d75592f98b42a8534182a5af9bf240b1fd16c`.

This is a parallel research-lane package. It is **RESEARCH_FROZEN**, not integration-frozen.

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

NCAA Tournament games are classified/site-normalized from the dedicated Ohio State NCAA table. Every NCAA row has venue/city/state populated. Historical NCAA rounds are left blank where a modern-equivalent stage is not sufficiently explicit; third-place/consolation games retain blank round.

The package contains **30 NIT games**, matching Ohio State's 10 appearances and 21-9 on-court NIT record. Preseason NIT games remain regular season; only title games use `Championship`.

## Accomplishment evidence collected
- Big Ten regular-season championships: **20**
- Big Ten Tournament championships: **4**
- NCAA appearances through 2025-26: **32**
- Final Fours: **10**
- National championships: **1**
- Best Finish: **National Champion**
- Best Finish Year: **1960**

The guide has an internal NCAA-appearance-count inconsistency; the listed historical appearance seasons support 31 through 2022, and 2025-26 adds the 32nd.

## Provisional global venue IDs
All new research-time numeric venue allocations are provisional:
- Armory (Columbus, OH) -> `VEN-000281` **PROVISIONAL**
- Coliseum (Columbus, OH) -> `VEN-000282` **PROVISIONAL**
- Cow Palace (Daly City, CA) -> `VEN-000283` **PROVISIONAL**
- Cincinnati Gardens (Cincinnati, OH) -> `VEN-000284` **PROVISIONAL**
- Convocation Center (Athens, OH) -> `VEN-000285` **PROVISIONAL**
- Covelli Center (Columbus, OH) -> `VEN-000286` **PROVISIONAL**

A current-main shared-reference rebase is mandatory before tracked Phase 0.

## Owner questions remaining
None.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=b8b543544cc97d993056537e3b7fc8d09258fa8c` from `research_base_sha=4c8d75592f98b42a8534182a5af9bf240b1fd16c`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
