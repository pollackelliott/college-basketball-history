# Oklahoma research portfolio notes

## Research status and scope

This six-file portfolio is **RESEARCH_FROZEN** as a parallel research-lane artifact. No repository integration, canonical ingestion, Owner Gate, release, publication, or shared/global repository mutation has been performed.

- `research_base_sha`: `2899c45e7b8dc2b8553c8b9e2342715a9a091484`
- Owner history-scope ruling: **ALWAYS_TOP_LEVEL_FROM_INCEPTION**
- `history_start_season`: **1907-1908**
- Coverage: **1907-08 through completed 2025-26**
- Competitive games: **2,996**
- On-court record: **1,815-1,181**
- Exhibitions/scrimmages: **excluded**
- Unknown exact dates: **762**
- Unknown played scores: **0**
- Source opponent labels: **394**, all resolved
- H/A/N/Unknown: **1,411 / 1,100 / 485 / 0**
- Venue rows: **65**

Game-type counts:

- `REGULAR_SEASON`: **2,801**
- `CONFERENCE_TOURNAMENT`: **92**
- `NCAA_TOURNAMENT`: **76**
- `NIT`: **19**
- `POSTSEASON`: **8**

The 2,925-game ledger through 2023-24 is **1,774-1,151 on court**, exactly matching the media guide's separately stated on-court aggregate. The completed 2024-25 season adds **20-14** and 2025-26 adds **21-16**, producing the final **1,815-1,181** total.

## On-court / administrative result policy

Oklahoma's media guide publishes an NCAA-adjusted all-time record that removes 13 wins from 2009-10. The guide separately states the actual on-court record. This package preserves those 13 played wins and records `VACATED_WIN` administrative metadata, consistent with project policy.

## Source-internal corrections and caveats

The chronological ledger remains the row-level evidence layer and its literal wording is preserved in `raw_text`. Structured values differ only where stronger official/dedicated evidence supports normalization.

- **2021-22 Baylor:** the year-by-year ledger prints the Jan. 4 game as an Oklahoma 84-74 win, but the season record and official completed-season evidence support a **74-84 loss**. Structured score/result are normalized while the printed line remains in `raw_text`.
- **2015-16 season header:** the year-by-year results header prints **29-7**, while the 37-game ledger and dedicated year-by-year record table support **29-8**. The package follows the actual game ledger.
- **1971 NIT at Hawai'i:** the chronological ledger prints **Hawai'i 88, Oklahoma 87 (2OT)**. Oklahoma's dedicated NIT results table instead prints **Hawai'i 87, Oklahoma 86**. Oklahoma's later official retrospective and independent schedule evidence support the chronological 88-87 result. The package therefore retains Oklahoma 87-88, classifies the game as `NIT`, and documents the dedicated-table conflict rather than silently harmonizing it.

## Conference history

- Independent: **1907-08 through 1918-19**
- Missouri Valley: **1919-20 through 1927-28**
- Big Six: **1928-29 through 1946-47**
- Big Seven: **1947-48 through 1956-57**
- Big Eight: **1957-58 through 1995-96**
- Big 12: **1996-97 through 2023-24**
- SEC: **2024-25 onward**

## Conference tournaments

The owner-supplied `Conference_Tournament_Site_Reference(20260825-203529).xlsm` is incomplete globally. The owner explicitly authorized the portions pertinent to Oklahoma's membership history as complete for Oklahoma, and only those Big Eight, Big 12, and SEC rows are used here. The workbook is not promoted to universal project canon.

Final conference-tournament ledger:

- Big Eight: **39 games, 23-16**
- Big 12: **48 games, 24-24**
- SEC through 2025-26: **5 games, 3-2**
- Total: **92 games, 50-42**

Final QA caught and corrected five conference-tournament rows that the initial year-by-year extraction had treated as regular season: **1977 Missouri, 1989 Iowa State, 2013 Iowa State, 2017 TCU, and 2024 TCU**. Oklahoma's dedicated conference-championship section confirms those tournament identities.

The media guide's conference-tournament headline is internally inconsistent: it prints **“46-39 RECORD; 23-16 BIG EIGHT; 24-24 BIG 12.”** The two component records sum to **47-40**, not 46-39. The package follows the game-by-game/component histories and preserves the headline defect as source provenance rather than forcing the ledger to match it.

For 1977 through 1985 Big Eight tournaments, the authorized workbook distinguishes campus-site quarterfinals from the shared Kemper Arena semifinals/final. Campus preliminary games are not automatically assigned to Kemper Arena. Beginning with the later centralized format, shared-site chronology is applied season-specifically.

## Postseason taxonomy

The package contains **76 NCAA Tournament games (42-34)**, **19 NIT games (11-8)**, and **8 generic POSTSEASON games (5-3)** in addition to conference-tournament games. Regular-season invitationals remain `REGULAR_SEASON`.

Historical NCAA third-place/consolation games remain `NCAA_TOURNAMENT` with a blank controlled round when no supported modern round label exists. All **76 NCAA Tournament rows have curated physical venue, city, and state**, and all populated NCAA rounds use the project-controlled vocabulary.

The 2025-26 College Basketball Crown games are genuine non-NCAA/non-NIT postseason and use `POSTSEASON`; the West Virginia finale is marked `Championship`.

## Venue and H/A/N discipline

H/A/N is established from explicit game-level source notation or official schedule/tournament context. Venue or geography never establishes H/A/N.

All 65 research-time `VEN-99xxxx` values are intentionally **provisional transport identifiers**, not claims that 65 new global venues must be created. The durable facts are physical venue identity, normalized name/aliases, geography, and game assignments. The serialized Implementation lane must rebase every venue against then-current `data/reference/venues.csv`, reuse existing physical identities where present, and allocate new global IDs only for genuinely new buildings.

No foreign location was forced into a domestic state taxonomy. Source wording for the Bahamas is preserved, while normalized city/state are left blank where the current project representation does not safely support a domestic-style pair.

## Intentional unknowns

Exactly **762** historical rows retain blank exact dates after two previously blank dates were resolved by stronger reciprocal official records. All played scores are known. Remaining dates are left blank unless authoritative evidence establishes calendar precision; no date is invented from sequence, opponent chronology, or aggregate season totals.

## Implementation current-main preparation

The immutable `RESEARCH_FROZEN` transport artifact remains preserved separately
with SHA-256 `d0a0203f35cbbfee550ebdb1372c84b31468df9c8f2c2d1a0496976214fdc0aa`.

A derived integration input was created solely to resolve current-main shared
physical-venue identities before Phase 0. Deterministic corrections were:

- existing historical/current venue names were mapped to their established
  current-main physical venue keys;
- the research-time Madison Square Garden row was split between the existing
  1925 and 1968 physical buildings, with the 1947 NCAA Championship assigned
  to the 1925 building and the 1971 NIT game assigned to the 1968 building;
- the school-level venue relationship geography for Imperial Arena,
  MGM Grand Garden Arena, and T-Mobile Arena was aligned to the existing
  current-main global venue registry;
- game-level source geography and raw source wording were not changed by those
  registry-geography normalizations.

No competitive game was added, removed, or reidentified.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=b8c84717fa6434610c43c8e1a49bc6d634870e0a` from `research_base_sha=2899c45e7b8dc2b8553c8b9e2342715a9a091484`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

## Implementation H/A/N normalization repair

A pre-Owner-Gate audit found a systematic parser omission in the 2024-25
media-guide year-by-year ledger: 205 rows whose preserved `raw_text`
explicitly says `at` and 25 rows whose preserved `raw_text` explicitly says
`vs.` had blank `source_site_candidate` values and had therefore fallen
through to `SOURCE_PROGRAM_HOME`.

The correction follows the portfolio's existing source hierarchy: explicit
game-level `at` / `vs.` notation controls H/A/N before venue chronology.
The 205 `at` rows are now `OPPONENT_HOME`; the 25 `vs.` rows are now
`NEUTRAL`. The documented 1907-08 Epworth source-internal home exception is
unchanged.

Exactly 136 Lloyd Noble Center / Norman fallbacks that existed only because
of those erroneous home classifications were removed rather than replaced
with unsupported venue guesses. Raw source wording, game identities, dates,
scores, opponents, game types, and administrative statuses were not changed.

The two research-local `Ford Center` and `Paycom Center` relationship rows
were also consolidated after current-main rebase proved that both refer to
the same physical `Paycom Center` identity. `Ford Center` remains an alias.

After this bulk marker repair, interim H/A/N totals were **1,413 home / 1,097 away / 486 neutral / 0 unknown**. A subsequent reciprocal-source audit made the smaller final structured corrections documented below. The integration package contains **65 physical venue rows**.

## Implementation final structured normalization repair

A final pre-Owner-Gate reciprocal-source audit resolved 17 structured rows
without changing literal Oklahoma `raw_text`, scores, results, opponent
identities, game types, or administrative statuses.

The repair set consists of:

- two previously blank exact dates resolved from reciprocal official records:
  1916-02-17 at Missouri and 1948-12-18 at Ohio State;
- eight additional printed-date corrections established by official
  Kansas, Texas, Nebraska, and Michigan historical records;
- five single-overtime flags supplied by explicit Oklahoma wording or
  stronger official game evidence;
- 1916 Missouri and 1948 Ohio State corrected from Oklahoma home to
  opponent home;
- the 1983 Big Eight campus quarterfinal against Kansas corrected from
  neutral to Oklahoma home at Lloyd Noble Center;
- the 2016 Texas game corrected from Oklahoma home to Texas home at
  Frank Erwin Center in Austin.

The 1948 Ohio State game is also normalized to one overtime. No historical
physical arena is asserted for that game because the reciprocal source
establishes Columbus/home status but does not safely establish a building.

Final package accounting is **1,411 home / 1,100 away / 485 neutral / 0
unknown**, with **762 unknown exact dates**, **0 unknown played scores**, and
**65 physical venue rows**.

## Implementation opponent-registry normalization repair

Pre-seal deterministic site generation exposed two opponent relationship
normalization defects without changing Oklahoma's literal source evidence.

- `centenary` retains its established historical opponent key, with canonical
  display normalized from `Centenary (La.)` to the project-stable `Centenary`.
- Two Oklahoma games previously assigned to non-registry key `miami-ohio`
  were corrected to current Division I registry key `miami-oh`, with canonical
  display `Miami (OH)`.

The affected Oklahoma `source_opponent_label` and `raw_text` values remain
unchanged. This is relationship/identity normalization, not a rewrite of the
school's historical source wording.

## 2003-12-06 Michigan State identity/site integration repair

Pre-seal canonical accounting found that `OKLRAW-02250` was already present
in the Oklahoma ledger but had been normalized to orphan opponent key
`mich-state`, causing the game to be treated as new even though Michigan
State onboarding had already created canonical game `CBBG-0048496`.

Integration QA corrected the normalized identity to current Division I
registry key `michigan-state` / `Michigan State`. Oklahoma's literal source
label `Mich. State` and raw text remain unchanged.

Oklahoma's official game box score identifies the game site as Auburn Hills,
Michigan (`The Palace`). The Oklahoma school venue relationship therefore
reuses global physical venue `VEN-000206` (`the-palace-of-auburn-hills`).
Michigan State's official historical evidence independently corroborates the
game date, 80-77 overtime result, and Auburn Hills neutral setting.
