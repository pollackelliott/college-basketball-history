# Purdue onboarding notes

## 1. Coverage and owner scope

This package covers Purdue men's basketball from **1896-97 through 2025-26** and contains **3,086 competitive non-exhibition games**.

The project owner confirmed that Purdue has always been D1/top-level for site purposes, so the required `history_start_season` is **1896-1897** and the scope basis is `ALWAYS_TOP_LEVEL_FROM_INCEPTION`.

The package on-court record is **2,001-1,085**. The 2025-26 package contribution is **39 competitive games (30-9)**; the October 24 Kentucky and October 29 Indianapolis exhibitions are excluded.

Administrative forfeits/vacated results do not rewrite the played result.

## 2. Conference chronology

- **1896-97 through 1904-05:** Independent
- **1905-06 to present:** Big Ten

The project registry's stable `big-ten` identity covers the league's historical Western Conference / Big Nine naming lineage.

## 3. Home-court chronology

H/A/N is established from game-level source syntax or explicit tournament/game context before any venue chronology is applied. Venue history never creates a home designation by itself.

For games already established as Purdue home games, the package uses this conservative chronology:

- **Military Hall and Gymnasium:** through 1906-12-21; first established Purdue basketball game 1897-01-23 vs. Lafayette YMCA
- **Lafayette Coliseum:** 1907-01-10 through 1909-03-13
- **Memorial Gymnasium:** 1910-01-08 through 1934-03-03, subject to the unresolved 1929 exception below
- **Old Lafayette Jefferson High School Gymnasium:** continuous 1934-12-10 through 1937-02-27
- **Lambert Fieldhouse:** 1937-12-11 through 1967-03-06
- **Mackey Arena:** beginning 1967-12-02 and ongoing

Purdue institutional history states that **four home games in calendar 1929** were moved from Memorial Gymnasium to Lafayette Jefferson High School's larger gym. The institutional source does not identify the four game rows. Rather than guess, this package intentionally leaves the venue blank for all ten Purdue home games played during calendar 1929. H/A classification for those games remains intact.

The rough owner-supplied venue chronology has therefore been refined: Lafayette Coliseum is not treated as Purdue's original home. Purdue institutional history places the original program in Military Hall and Gymnasium / Old Gym and specifically states that home games moved to the downtown Lafayette Coliseum in 1907.

## 4. Postseason taxonomy

Package game types:

- `REGULAR_SEASON`: **2,918**
- `CONFERENCE_TOURNAMENT`: **50**
- `NCAA_TOURNAMENT`: **91**
- `NIT`: **27**

Purdue's Big Ten Tournament record through 2026 is **25-25**. The owner-supplied Big Ten-complete tournament-site workbook is used only for shared venue/city/state enrichment and never to infer H/A/N. Public conference-tournament rounds are blank except championship games.

Purdue's NCAA Tournament record through 2026 is **54-37** in **37 appearances**. NCAA rounds use the project's controlled vocabulary. Purdue's 1980 NCAA games vs. La Salle and St. John's in West Lafayette remain Purdue home-site games because the year-by-year source independently presents them as home games and the dedicated NCAA history places them at Purdue's home venue. Other NCAA games in the package are neutral.

Purdue's NIT record in the package is **20-7**. Public NIT round is `Championship` only for the 1974 Utah, 1979 Indiana, and 1982 Bradley title games; consolation/third-place and earlier rounds remain blank.

The current repository schema does not yet expose a generic `POSTSEASON` game type. Purdue's two 2013 CBI games are therefore retained as `REGULAR_SEASON` with `CBI` preserved in event metadata, matching the current `data-schema.md` contract.

## 5. Venue and location principles

Venue/location enrichment follows the project hierarchy:

1. explicit game-level venue/location evidence
2. Purdue dedicated NCAA Tournament history plus established physical NCAA venue identity
3. owner-supplied Big Ten-complete conference-tournament site reference for Big Ten Tournament venue/city/state
4. Purdue primary-home chronology, but only after a row is independently classified `SOURCE_PROGRAM_HOME`

Venue geography never establishes H/A/N.

The portfolio references six planned new global physical venue identities that are not present on the current `main` registry and must be added in guarded Codespace Phase 0 before ingestion:

- `VEN-000262` — Military Hall and Gymnasium
- `VEN-000263` — Lafayette Coliseum
- `VEN-000264` — Memorial Gymnasium (Purdue physical building)
- `VEN-000265` — Old Lafayette Jefferson High School Gymnasium
- `VEN-000266` — Lambert Fieldhouse
- `VEN-000267` — Baha Mar Convention Center

All other portfolio venue identities reuse the current global registry.

## 6. 1995-96 administrative history

Purdue's played 1995-96 record is preserved as **26-6** in the game ledger. Purdue official material states that NCAA sanctions later required forfeiture/vacation associated with Luther Clay's participation; a later Purdue article notes that the NCAA did not recognize 19 Purdue victories from the season.

The source set used for this package does not identify the affected games row-by-row with enough authority to allocate `FORFEIT` / `VACATED_*` status safely. Therefore no row-level administrative status is manufactured. The aggregate sanction is preserved here and in `source-notes.md` for later owner-reviewed administrative enrichment if a reliable affected-game list is obtained.

## 7. Package QA and intentional unknowns

- Competitive games: **3,086**
- On-court record: **2,001-1,085**
- H/A/N: **1,554 / 1,196 / 336**
- Opponent source labels: **324**, all resolved
- Canonical opponent identities represented: **312**
- Unknown exact dates: **28**
- Package venue rows: **64**
- 2025-26 competitive record: **30-9**
- 2025-26 H/A/N: **17 / 11 / 11**
- 2025-26 Big Ten Tournament: **4-0, champion**
- 2025-26 NCAA Tournament: **3-1, Elite Eight**

The 28 blank exact dates are retained because the Purdue year-by-year source does not provide a date precise enough to justify invention. The 1929 venue ambiguity and the 1995-96 row-level administrative allocation are the two principal intentional unresolved enrichment items; neither prevents game identity, score, result, or H/A/N curation.

## 8. Expected accomplishment reference values after 2025-26

For the later guarded Codespace reference-layer update, Purdue's authoritative/source-supported values are:

- Conference regular-season championships: **26**
- Conference tournament championships: **3**
- NCAA Tournament appearances: **37**
- Final Four appearances: **3**
- National championships: **0**
- `best_finish_key`: **NATIONAL_RUNNER_UP**
- `best_finish_year`: **2024**

The 2026 Elite Eight does not change Purdue's best NCAA finish.
