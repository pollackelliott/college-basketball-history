# Texas A&M men's basketball source-package curation notes

## Research status

This six-file portfolio was independently rebuilt in the research lane and is **RESEARCH_FROZEN** against `research_base_sha=fb886afc1f940ddc9e5904908cc2f2c5cf7077cb`.

Owner history-scope ruling: **Texas A&M has always been D1/top-level for site purposes.** Independent source review establishes program inception in **1912-13**, which is therefore the site history start season.

## Coverage

- Competitive games: **2,926** (1912-13 through completed 2025-26).
- On-court record with known played result: **1,569-1,356**, plus **1** played-result-unknown administrative-forfeit row.
- Unknown exact dates after bounded reciprocal-source recovery audit: **542** (down from 759; 217 exact dates recovered).
- Unknown played scores: **9**.
- Site perspective: **1,522 home / 1,019 opponent-home / 385 neutral / 0 unknown**.
- Game types: **2,786 regular season / 81 conference tournament / 35 NCAA Tournament / 19 NIT / 5 other postseason**.

The explicit 2024 Houston charity exhibition and 2025 Arizona State exhibition are excluded.

## Administrative results

Exactly two 1917-18 rows carry `FORFEIT` metadata. The Simmons College row is printed as `0-2^` with a generic forfeit footnote; because no independently supported played score/result was found, its structured played score/result is left unknown. The Texas row is source-conflicted: Texas A&M prints `L 7-8†`, while Texas's official fact book explicitly says the contest was forfeited to Texas because A&M's Pay Dwyer was ineligible and preserves the anomalous `W 7-8` notation. The reciprocal evidence establishes the on-court orientation used here: A&M 8, Texas 7, A&M on-court win, followed by an administrative forfeit to Texas. Raw A&M text is preserved verbatim.

## Conference chronology

Independent 1912-13 through 1913-14; Southwest Conference 1914-15 through 1995-96; Big 12 1996-97 through 2011-12; SEC 2012-13 onward.

## Home facilities

Texas A&M's own "Homes of Aggie Hoops" material establishes DeWare Field House (originally Memorial Gymnasium) for 1924-1954, G. Rollie White Coliseum for 1954-1998, and Reed Arena beginning in fall 1998. Reed's first competitive basketball game was the Nov. 13, 1998 North Texas game. Pre-1924 home rows retain College Station, Texas but use the dedicated `RESEARCHED_UNRESOLVED_HOME_VENUE` exception rather than inventing a stable physical building identity; contemporary 1924 reporting confirms a prior gym structure existed at the site of the new Memorial Gymnasium but does not support a sufficiently stable row-level venue identity.

## Postseason taxonomy

Conference tournament classification begins with the 1976 Southwest Conference postseason event and includes the campus-preliminary format through 1984. The owner-supplied workbook controls physical site evidence for Texas A&M-relevant SWC/Big 12/SEC tournament rounds; it never creates H/A/N. Three 1951 Texas games are the NCAA District 6 playoff and are classified generic `POSTSEASON`; the subsequent Washington game is NCAA Tournament. The 2014 Wyoming and Illinois State games are CBI and are generic `POSTSEASON`.

All 35 NCAA Tournament rows have venue/city/state from Texas A&M's official NCAA history/current official game notes. Historical consolation (1969 Colorado) remains `NCAA_TOURNAMENT` with blank controlled round.

## H/A/N discipline

`at` is opponent-home and explicit `vs` is neutral. Unprefixed year-by-year rows are source-program home unless a stronger game-level postseason/site source establishes otherwise. Event markers are stripped before H/A/N parsing. This independently corrects the 1969 NCAA consolation row (`! vs Colorado`) to neutral; the prior interrupted package's aggregate H/A/N checkpoint appears to have counted that one row as home. Physical venue geography never creates or changes H/A/N.

## Bounded exact-date recovery QA

After the initial portfolio freeze, a targeted audit was run only against the 759 blank `game_date` rows, with emphasis on the pre-March-1951 ledger. Exact dates were added only when an authoritative institutional or reciprocal source matched the Texas A&M row strongly enough on season, opponent, reciprocal score/result, and site context. The audit recovered **217** exact dates and leaves **542** blank. No date was filled from schedule order, geography, typical series timing, or season chronology alone.

Principal reciprocal/institutional evidence was Texas's official 2025-26 Fact Book year-by-year ledger, Arkansas's official historical media-guide ledger, LSU's 2025-26 Record Book, Kentucky/Purdue/Ohio State official historical ledgers already preserved on current main, TCU Athletics' official Texas A&M opponent-history page, Rice Athletics' official Texas A&M opponent-history page, and Baylor's official men's basketball media-almanac all-time results. Conflicting or incomplete reciprocal rows were deliberately left blank.

The remaining unknown dates are entirely historical, from 1912-13 through 1950-51. By starting-decade they are: 1910s **92**, 1920s **129**, 1930s **156**, 1940s **149**, and 1950-51 **16**.

## Research-base venue identity comparison

The original 65 local `venues.csv` rows were compared against `data/reference/venues.csv` and `data/reference/venue-names.csv` at `fb886afc1f940ddc9e5904908cc2f2c5cf7077cb`, using physical identity, city/state, known aliases, and date-aware split identities where required. The audit exposed one real local physical-identity duplication: historical **Ford Center** and current **Paycom Center** are the same Oklahoma City arena (current-main `VEN-000162`). They were consolidated into one local physical row, with Ford Center retained as an alias. The revised `venues.csv` therefore has **64** physical rows: **57** match existing current-main physical venues and **7** are genuine research-time new physical candidates: Arena-Auditorium (Laramie), College Park Center (Arlington), DeWare Field House (College Station), Lakefront Arena (New Orleans), Old Gymnasium (Nevada) (Reno), Redbird Arena (Normal), and Schollmaier Arena (Fort Worth). **Ambiguous physical-identity matches: 0.** Numeric IDs remain provisional; authoritative reuse/allocation belongs to Implementation after current-main rebase.

## Implementation current-main rebase provenance

- Original RESEARCH_FROZEN ZIP SHA-256: `1369f835acbe14e98fa7eee2f5d09b5f290e403ee37b36adfe73a597861942d5`
- Original Research Freeze transport artifact remains unmodified.
- Implementation created a derivative package solely for current-main shared-reference reconciliation.
- Physical venue identity outcome: 57 current-main reuses; 7 genuinely new physical venues; 0 ambiguous identities.
- Shared venue-key/current-main reconciliations:
  - `addition-financial-arena` -> `cfe-arena` (Addition Financial Arena)
  - `ahearn-fieldhouse` -> `ahearn-field-house` (Ahearn Fieldhouse)
  - `benchmark-international-arena` -> `amalie-arena` (Benchmark International Arena)
  - `exactech-arena` -> `oconnell-center` (Exactech Arena)
  - `gregory-gymnasium` -> `gregory-gym` (Gregory Gymnasium)
  - `jacksonville-veterans-memorial-arena` -> `vystar-veterans-memorial-arena` (Jacksonville Veterans Memorial Arena)
  - `mgm-grand-garden-arena` (MGM Grand Garden Arena): GLOBAL_GEOGRAPHY_REBASE:Las Vegas,NV->Paradise,NV
  - `madison-square-garden` -> `madison-square-garden-1968` (Madison Square Garden)
  - `maravich-assembly-center` -> `pete-maravich-assembly-center` (Maravich Assembly Center)
  - `municipal-auditorium` -> `municipal-auditorium-kc` (Municipal Auditorium)
  - `spokane-arena` -> `numerica-veterans-arena` (Spokane Arena)
  - `the-super-pit` -> `unt-coliseum` (The Super Pit)
  - `thompson-boling-arena-at-food-city-center` -> `thompson-boling-arena` (Thompson-Boling Arena at Food City Center)
  - `wells-fargo-center` -> `xfinity-mobile-arena` (Wells Fargo Center)
- Madison Square Garden is explicitly rebased to the 1968/current physical building; all Texas A&M MSG games in the package are dated 1979 or later.
- MGM Grand Garden Arena reuses the existing physical identity; `Paradise, NV` is the global venue-registry geography while game-level source locality may remain `Las Vegas, NV`.

## Implementation conference-key rebase

- Current-main shared-reference normalization: `southwest` -> `southwest-conference`.
- This reuses the established Southwest Conference identity already used by published Arkansas and Texas; it does not create a new conference identity.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=fb886afc1f940ddc9e5904908cc2f2c5cf7077cb` from `research_base_sha=fb886afc1f940ddc9e5904908cc2f2c5cf7077cb`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

## Authoritative preflight blocker repairs

Three bounded normalization defects discovered by authoritative onboarding
preflight were corrected without reopening the research game universe,
opponent identities, results, or history scope:

- **1979-03-15 vs. Alabama (NIT):** official Texas A&M NIT history places the
  72-68 Alabama win in Houston. The source row is normalized from the
  incorrectly assigned Madison Square Garden / New York location to **The
  Summit, Houston, TX**, reusing current-main `VEN-000210`.
  Official evidence:
  https://12thman.com/news/2005/03/15/aggies-face-clemson-in-first-round-nit-battle
- **1964-03-09 vs. Texas Western (NCAA):** official Texas A&M history identifies
  the game as an NCAA first-round loss. The 25-team field used preliminary
  games before the 16-team regional stage, so current project bracket-stage
  taxonomy normalizes the row to **Play-in**.
  Official evidence:
  https://12thman.com/news/2011/03/15/texas-am-heads-to-chicago-for-ncaa-secondthird-rounds
- **1975-03-15 vs. Cincinnati (NCAA):** Texas A&M explicitly describes the
  tournament as a 32-team field and the Cincinnati game as its first round.
  Current project bracket-stage taxonomy therefore normalizes it to **R32**.
  Official evidence:
  https://12thman.com/news/2001/01/04/am-to-honor-four-championship-teams-on-saturday

Raw source text is unchanged. These are implementation-stage factual
normalizations required to clear machine blockers, not owner reconciliation
decisions.

## Pre-Owner-Gate structured-source normalization

Authoritative preflight exposed a bounded set of modern structured-source
transcription errors whose answers are independently established by Texas A&M's
own dedicated schedules, recaps, and box scores. They were corrected before
Owner Gate 1 so the owner is not asked to arbitrate demonstrably false machine
conflicts.

Corrected structured facts:

- TAMRAW-02387: Missouri date `2010-02-06` -> `2010-02-03`
- TAMRAW-02390: Kansas date `2010-02-20` -> `2010-02-15`
- TAMRAW-02393: Texas date `2010-03-01` -> `2010-02-27`
- TAMRAW-02396: Big 12 Tournament Nebraska date `2010-03-10` -> `2010-03-11`
- TAMRAW-02397: Big 12 Tournament Kansas date `2010-03-11` -> `2010-03-12`
- TAMRAW-02419: Nebraska date `2011-01-26` -> `2011-01-29`
- TAMRAW-02485: Kentucky overtime periods `0` -> `1`
- TAMRAW-02667: NCAA Michigan date `2018-03-24` -> `2018-03-22`
- TAMRAW-02720: Missouri score `66-64` -> Texas A&M `68-51`
- TAMRAW-02762: Arkansas score `86-61` -> Texas A&M `86-81`
- TAMRAW-02877: Ole Miss date `2025-01-21` -> `2025-01-22`

Principal authoritative Texas A&M evidence:

- https://12thman.com/sports/mens-basketball/schedule/season/2009-10
- https://12thman.com/news/2011/1/29/205233267
- https://12thman.com/news/2013/02/02/aggies-fall-to-kentucky-in-ot-72-68
- https://12thman.com/sports/mens-basketball/stats/2017-18/michigan/boxscore/7276
- https://12thman.com/news/2020/02/4/four-aggies-score-in-double-figures-as-am-defeats-missouri-68-51
- https://12thman.com/sports/mens-basketball/stats/2021/arkansas/boxscore/18394
- https://12thman.com/sports/mens-basketball/stats/2024-25/ole-miss/boxscore/22167

No game was added or removed. Opponent identity, history scope, and raw source
text were not changed.
