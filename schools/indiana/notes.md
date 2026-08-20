# Indiana onboarding notes

## 1. Coverage and owner scope

This package covers Indiana men's basketball from **1900-01 through 2025-26** and contains **3,112 competitive non-exhibition games**. The project owner confirmed that Indiana has always been D1/top-level for site purposes, so `history_start_season` is **1900-1901** and the required scope basis is `ALWAYS_TOP_LEVEL_FROM_INCEPTION`.

The package on-court record is **1,965-1,147**. Administrative forfeits are stored separately and do not rewrite the played result.

## 2. Conference chronology

- **1900-01 through 1903-04:** Independent
- **1904-05 to present:** Big Ten

The project registry's stable `big-ten` identity covers the league's historical Western Conference / Big Nine naming. Indiana has remained in that lineage continuously since 1904-05.

## 3. Home-court chronology

H/A/N is established from game-level source notation or postseason context before any venue chronology is applied. Venue history never creates a home designation by itself.

For games already established as Indiana home games, the owner-approved chronology is:

- **Old Assembly Hall:** 1901-02-28 through 1917-01-05
- **Men's Gymnasium:** 1917-01-19 through 1928-12-08
- **IU Fieldhouse:** 1928-12-13 through the end of 1959-60
- **New IU Fieldhouse:** 1960-61 through 1970-71
- **Assembly Hall:** beginning 1971-12-01 and ongoing

The current arena is displayed in this project **exclusively as `Assembly Hall`**. `Simon Skjodt Assembly Hall` is retained as source/alias wording only. This Bloomington venue remains physically distinct from the Champaign venue `VEN-000196`, whose project display is also Assembly Hall.

The record book's home-courts narrative contains an internal wording conflict around the first facility: the chronological ledger explicitly lists **1901-02-08 at Butler** and **1901-02-28 Butler at home**. Game-level chronology controls the H/A classification, and the first assigned Old Assembly Hall game is therefore 1901-02-28.

## 4. Postseason taxonomy

Package game types:

- `REGULAR_SEASON`: **2,950**
- `CONFERENCE_TOURNAMENT`: **44**
- `NCAA_TOURNAMENT`: **104**
- `NIT`: **14**
- `POSTSEASON`: **0**

Named regular-season events remain `REGULAR_SEASON`.

Indiana's Big Ten Tournament history begins with the 1998 tournament. The owner-supplied conference-tournament workbook is used only for shared venue/city/state enrichment; it does not infer H/A/N. Big Ten Tournament games are independently established as neutral by the tournament/game context. Public conference-tournament rounds remain blank except Indiana's 2001 championship-game loss to Iowa.

NCAA Tournament classification is cross-checked against Indiana's dedicated **NCAA Tournament Results** section. Historical consolation/third-place games keep `NCAA_TOURNAMENT` with blank public round. NCAA Tournament status does **not** determine H/A/N. Tournament games remain `NCAA_TOURNAMENT`, but a game played as a true participant-home game is classified H/A when explicit historical/game-level evidence establishes that status; venue geography alone never creates it. The 1981 Bloomington regional wins over UAB (March 20) and St. Joseph's (March 22) are therefore Indiana home games at Assembly Hall, not neutral-site games.

Postseason NIT appearances in the chronological ledger occur in **1972, 1979, 1985, 2005, 2017, and 2019**. The 1979 and 1985 title games use public round `Championship`; other NIT rounds remain blank.

## 5. Administrative results

Two 1976-77 losses to Minnesota are explicitly marked by the record book as games later forfeited to Indiana:

- 1977-01-27 — Minnesota 79, Indiana 60
- 1977-02-15 — Minnesota 65, Indiana 61

Both remain on-court Indiana losses and carry `administrative_status=FORFEIT` with a source note. The administrative action is not allowed to rewrite the played score/result.

## 6. Internal source corrections

The year-by-year ledger is the primary chronological game source. Its original text remains in `raw_text`. Exactly nine normalized game facts require corrections because of an internally impossible line or stronger dedicated/archival evidence:

- 1967-03-17 vs Virginia Tech — year-by-year prints March 16; NCAA/reciprocal evidence establishes March 17.
- 1975-03-15 vs UTEP — year-by-year prints 78-52; NCAA bracket/tournament evidence establishes **78-53**.
- 1986-03-14 vs Cleveland State — year-by-year prints March 13; NCAA/reciprocal evidence establishes March 14.
- 1997-03-13 vs Colorado — year-by-year prints March 11; NCAA/reciprocal evidence establishes March 13.
- 1999-03-05 vs Illinois — normalized to **Illinois 82, Indiana 66**.
- 2005-03-11 vs Minnesota — normalized to **Minnesota 71, Indiana 55**.
- 2007-01-13 at Penn State — printed `W 74-84`; normalized to **Indiana 84, Penn State 74**.
- 2020-02-01 at Ohio State — printed `L 68-59`; normalized to **Ohio State 68, Indiana 59**.
- 2022-03-12 vs Iowa — normalized to **Iowa 80, Indiana 77**.

The dedicated NCAA section itself contains several transcription errors; those are documented in `source-notes.md` and are not silently allowed to overwrite better-supported chronological facts.

A separate modern site correction is applied to **2005-03-16 Vanderbilt (NIT)**: the year-by-year ledger says `vs. Vanderbilt`, while Vanderbilt's official recap states the game was played at Indiana. It is therefore normalized to an Indiana home game at Assembly Hall.

## 7. 2025-26 completed season

The owner-supplied completed 2025-26 schedule contributes **32 competitive games** and an **18-14** on-court record. The Puerto Rico foreign-tour exhibitions plus the Marian and Baylor exhibitions are excluded. The March 11, 2026 loss to Northwestern is `CONFERENCE_TOURNAMENT` at the United Center; regular-season showcases remain `REGULAR_SEASON`.

## 8. Package QA

- competitive games: **3,112**
- on-court record: **1,965-1,147**
- unique source opponent labels: **341**
- H/A/N: **1,538 / 1,220 / 354**
- exact-date unknowns: **0**
- package venue rows: **67**
- administrative actions: **{'FORFEIT': 2}**
- exhibitions included: **0**

## 9. Accomplishment verification

Indiana official historical material supports the existing project reference values:

- conference regular-season championships: **22**
- conference tournament championships: **0**
- NCAA Tournament appearances: **41**
- Final Four appearances: **8**
- national championships: **5**
- best NCAA finish: **National Champion**
- most recent best-finish year: **1987**

No pre-Big-Ten conference title is added; Indiana was independent through 1903-04.

## 10. Aggregate source caveat

The year-by-year game ledger produces **1,947-1,133 on court through 2024-25**. The record book Quick Facts summary states **1,950-1,131**. Converting the two 1976-77 Minnesota played losses to administrative-forfeit wins explains two wins and two losses of that difference but still leaves one summary win unexplained. The project does **not** manufacture or delete a game to force an aggregate match; the row-level competitive ledger controls the package, and the source summary discrepancy is preserved for audit.
