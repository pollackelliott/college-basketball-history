# Penn State research portfolio notes

## Scope and research baseline

- School: Penn State
- School key: `penn-state`
- `research_base_sha=ced6a1e64d46c3be040b680b308bc070d22cff08`
- Owner history-scope ruling: **ALWAYS_TOP_LEVEL_FROM_INCEPTION**.
- Project history start: **1896-1897**, corresponding to Penn State's first varsity basketball season, listed by the record book as 1897.
- This is a research-only six-file portfolio. Shared/global IDs remain provisional until the serialized Implementation lane rebases against then-current `main`.

## Competitive universe

The package contains **2,884 competitive games** and an on-court record of **1,589-1,294-1** through completed 2025-26.

- `REGULAR_SEASON`: **2,758**
- `CONFERENCE_TOURNAMENT`: **66**
- `NCAA_TOURNAMENT`: **22**
- `NIT`: **36**
- `POSTSEASON`: **2**
- H/A/N: **1,402 / 1,210 / 272**
- Unknown exact dates: **6**
- Unknown played scores: **0**

Penn State's All-Time Results ledger contains 2,852 game-like rows through 2024-25, matching the record-book aggregate 1,577-1,274-1. The 2024-10-25 Lafayette row is explicitly a charity exhibition and is excluded. The All-Time Results ledger omits the real 2009 NIT championship win over Baylor; Penn State's dedicated NIT history supplies that game. Those two changes offset, leaving 2,852 competitive games through 2024-25. Penn State's official completed 2025-26 schedule adds 32 competitive games (12-20), excluding the Dayton and Shippensburg exhibitions.

## Conference chronology

1. Independent — 1896-97 through 1934-35
2. Eastern Intercollegiate Conference — 1935-36 through 1938-39
3. Independent — 1939-40 through 1974-75
4. Eastern Collegiate Basketball League — 1975-76
5. Eastern Eight — 1976-77 through 1978-79
6. Independent — 1979-80 through 1981-82
7. Atlantic 10 — 1982-83 through 1990-91
8. Independent — 1991-92
9. Big Ten — 1992-93 onward

The Eastern Intercollegiate Conference, Eastern Collegiate Basketball League, and Eastern Eight are provisional historical conference identities not present in the research-baseline global conference registry. Implementation must rebase/add them safely rather than treating their provisional keys as permanent global IDs.

## Conference-tournament workbook limitation

The owner supplied `Conference_Tournament_Site_Reference(10).xlsm` and authorized Penn State-relevant use. Its Big Ten rows are populated through 2026 and are used for Big Ten Tournament venue/city/state. The Penn State-relevant Atlantic 10/Eastern-era rows in the supplied workbook are not populated with venue/city/state despite the owner's expectation that they were complete. Per the owner's explicit instruction, that omission is treated only as a workbook gap, not evidence that a tournament/site did not exist. Those tournament sites were researched independently from Penn State and Atlantic 10 historical evidence and are preserved in the package.

## NCAA Tournament research

All **22 NCAA Tournament games** have curated physical venue, city, and state. Historical consolation/third-place games remain `NCAA_TOURNAMENT` with blank public round where the project vocabulary has no honest modern equivalent.

Material correction: Penn State's 1955 NCAA box-score section places the Iowa and Kentucky regional games in **Evansville, Ind.**; established NCAA/site evidence places that regional at **McGaw Memorial Hall in Evanston, Illinois**. The curated rows therefore use the current physical identity `Welsh-Ryan Arena` with source-era alias `McGaw Memorial Hall`, while the conflicting Penn State wording remains in `raw_text`/notes.

The 1955 Memphis State opener remains **March 8, 1955**, matching Penn State's dedicated NCAA box score and Memphis archival program evidence; no unsupported date rewrite is made.

## Source-internal corrections and defects

- **1903 Indiana State label:** Penn State's All-Time Results prints `Indiana State`, but Penn State's own series table files the 1903 game under Indiana (Pa.). That one row is normalized to `indiana-pa`; later genuine Indiana State games remain `indiana-state`. The literal source wording is preserved.
- **1918 Carnegie Tech impossible date:** the All-Time Results ledger prints `F 29` for the 54-30 road win, and later Penn State material repeats it as a Feb. 29, 1918 game. Because 1918 was not a leap year and no authoritative corrected exact date was located, the portfolio preserves the game but leaves `game_date` blank.
- **2009 Davidson date:** All-Time Results prints Nov. 21; Penn State's archived official box score and Davidson's official schedule establish **Nov. 22, 2009**. The normalized date is corrected to Nov. 22 and the printed line remains in `raw_text`.
- **1991 Atlantic 10 championship date:** the chronological ledger and Atlantic 10 tournament history support **March 7, 1991**; Penn State's Notable Victories section prints March 9. March 7 controls.
- **2020 Seton Hall series entry:** the series table contains a malformed 2021 date; the chronological ledger and official game evidence support Dec. 6, 2020.
- **2024 Saint Francis (Pa.) series filing:** Penn State's series table places the 2024-11-12 game under St. John's; the chronological ledger and actual opponent identify Saint Francis (Pa.). The game is normalized to Saint Francis (Pa.).
- **Bryce Jordan Center opener:** the BJC fast-facts box prints Minnesota 76-51, while Penn State's chronological ledger and Notable Victories section establish **76-61** on Jan. 11, 1996. The game row uses 76-61.
- Several older series-table date typos exist. The chronological All-Time Results ledger remains the primary date/score/result source unless stronger game-specific evidence establishes a correction.

## H/A/N policy

Penn State's Series Game-by-Game tables are the primary H/A/N cross-check. Physical venue chronology never creates H/A/N by geography. Postseason/tournament venue research enriches physical site after site classification. The 1995 NIT third-place game against Canisius is one explicit site correction: Penn State's dedicated NIT history puts it at Madison Square Garden, so it is neutral despite an inconsistent series-table H marker.

## Home facilities

Penn State's record book supplies the primary-home sequence:

- The Armory — 1897-1928
- Rec Hall — 1929 through Jan. 10, 1996 for the project chronology
- Bryce Jordan Center — opened Jan. 11, 1996 and remains the primary home

Chronology is used only after an independently supported home classification and is not blanket-applied over rows carrying event/site markers.

## Venue rebase warning

At `research_base_sha`, the global venue reference contains `VEN-000229` as Welsh-Ryan Arena with **McGaw Memorial Hall** as a historical alias, while later baseline data also contains a duplicate `VEN-000258` McGaw Memorial Hall identity. Penn State's 1955 NCAA rows intentionally use the existing `VEN-000229` physical identity. Implementation must resolve/rebase that duplicate and must not create a third McGaw/Welsh-Ryan venue.

## Remaining historical uncertainty

Exactly **six competitive games lack an authoritative exact date**: four Bucknell games and one Cornell game in the 1897/1898 opening-era material, plus the 1917-18 Carnegie Tech road win that Penn State prints as **F 29** even though 1918 was not a leap year. Penn State later repeated that impossible date in official material; no authoritative exact-date correction was found, so the date is intentionally blank rather than fabricated. Their scores, opponents, seasons, and H/A classifications are preserved. No played score is unknown.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=ca9da72a525234e3b08fabe13359f182c71445f7` from `research_base_sha=ced6a1e64d46c3be040b680b308bc070d22cff08`. Research-time numeric venue IDs remain immutable transport provenance; final authoritative venue IDs were assigned or reused against current main. Historical conference identities `eastern-intercollegiate-conference` (EIC), `eastern-collegiate-basketball-league` (ECBL), and `eastern-eight` (E8) were registered centrally following owner approval on 2026-08-25. The known pre-existing McGaw Memorial Hall / Welsh-Ryan duplicate global identity was not broadened into this school onboarding; Penn State reuses authoritative `welsh-ryan-arena` / `VEN-000229`. Status: **INTEGRATION_FROZEN**.

## Owner display-geography ruling

Owner display-geography ruling (2026-08-25): Penn State's three program home venues — Penn State Armory, Rec Hall, and Bryce Jordan Center — normalize to State College, PA for project presentation. Historical/source wording such as University Park, PA remains preserved in raw source text and reciprocal evidence.

## Owner Palestra home-game ruling

On 2026-08-25, Elliott confirmed that the recent Penn State-hosted
annual games at the Palestra are Penn State home games and opponent
road games. The affected portfolio sequence is Purdue (2023-01-08),
Michigan (2024-01-07), Indiana (2025-01-05), and Illinois
(2026-01-03). The venue is Palestra, Philadelphia, PA.

The Palestra is an alternate-site home venue for these games and is
not one of Penn State's three regular program-home venue
relationships. Raw source text remains preserved.
