# USC men's basketball source-package curation notes

## Research status

This six-file portfolio is **RESEARCH_FROZEN** against `research_base_sha=fb886afc1f940ddc9e5904908cc2f2c5cf7077cb`. Owner scope: **ALWAYS_TOP_LEVEL_FROM_INCEPTION**. USC's official year-by-year ledger begins in **1906-07** (calendar-year 1907 inception).

## Coverage

- Competitive games: **3,063**
- On-court record: **1763-1300**
- Coverage: **1906-07 through completed 2025-26**
- Exhibitions: **excluded** (the 2025-26 LMU and Grand Canyon exhibitions are not portfolio rows)
- Site classifications: **1435 USC-home / 1062 opponent-home / 257 neutral / 309 unknown**
- Game types: **2961 regular season / 48 conference tournament / 40 NCAA Tournament / 8 NIT / 6 other postseason**

## H/A/N discipline

The USC year-by-year ledger's `*` marker explicitly denotes home games. `vs.` syntax and dedicated postseason/event evidence establish neutral games. USC all-time opponent-series H/A/N is used as reciprocal source evidence only when it can be matched safely by season/opponent/score; it does not override the year-by-year HOME marker. Geography and venue identity never create H/A/N. Remaining unknown H/A/N rows are machine-visible researched unknowns rather than inferred.

## HOME facility research

USC Athletics' 2006-07 facility material states that the Los Angeles Memorial Sports Arena was USC's main home from the 1959 season through 2005-06 and lists documented alternate home sites; Galen Center became the home beginning in 2006-07. It also lists the 13 pre-Galen home locations known from records dating to 1927-28. Independent historical evidence supports Pan-Pacific Auditorium as USC's home from 1949 through 1959 and Shrine Auditorium as a major 1940s home site. Because USC used multiple buildings before 1949 and surviving game-level material does not safely distinguish them for every HOME row, those exact building identities remain blank under `RESEARCHED_UNRESOLVED_HOME_VENUE`; complete Los Angeles, CA geography is retained. This is a researched uncertainty, not an unexamined chronology hole.

## Postseason taxonomy

Regular-season invitationals remain `REGULAR_SEASON`. The portfolio contains the USC official postseason universe: 40 played NCAA Tournament games, 8 NIT games, 48 modern conference-tournament games through the 2026 Big Ten Tournament, and 6 other postseason games (four National Commissioner's Invitational/Commissioner's Classic games in 1974-75 and two 2025 College Basketball Crown games). All NCAA rows have physical venue, city, and state.

## Conference tournament site workbook

Owner-supplied `Conference_Tournament_Site_Reference(20260901-204513).xlsm` is globally incomplete. By owner ruling, its USC-relevant conference sections are complete and may be used only for USC research. This package uses those rows only for physical conference-tournament venue/city/state evidence. It never uses the workbook to establish H/A/N, and independently controls the Pac-10/Pac-12 chronology.

## Exact-date uncertainty

The working year-by-year extraction began with **302** blank exact dates. Targeted all-time-series reciprocal recovery supplies **11** exact dates on rows whose season/opponent/score identity is unique and supported. **291** exact dates remain blank, concentrated almost entirely before 1930; these are retained as genuine historical-source limitations rather than guessed from schedule order or usual series timing.

## Source-unknown opponents / scores

USC's 1920-21 ledger literally contains two `Unknown (no score)` winning rows while its 10-4 season aggregate requires those wins. They remain source-truth placeholders with blank scores. The opponent normalization table resolves the source label to a stable placeholder key; it does not invent institutional identity. Total rows with unknown played scores are **14**.

## Administrative history

USC's official guide states that 21 wins and one loss from 2007-08 were vacated by NCAA penalty. The package preserves on-court scores/results; wins carry `VACATED_WIN`, and the NCAA Tournament loss carries `VACATED_GAME`, without converting played truth into the administrative record.

## Current-main venue rebase

Numeric global venue IDs are intentionally not authoritative in this research package. `venues.csv` records physical identity, name/aliases, city/state, and usage. Implementation must compare these identities against then-current main and allocate/reuse numeric IDs only after the required current-main rebase.

## Bounded site-debt validation repair

A post-freeze bounded audit was performed only on the two large site-debt populations. It did not reopen the game universe, dates, scores, opponent identities, taxonomy, postseason, conference history, or accomplishments. The audit exposed a real H/A/N recovery hole concentrated in the Stanford series and two incorrectly unresolved 1985 CSUDH home-venue rows. Stanford Athletics' official Year-By-Year Results was used reciprocally to resolve the 134 previously UNKNOWN Stanford rows (128 USC away, five USC home, one neutral in Seattle). Six additional UNKNOWN rows were resolved from USC series/raw evidence or a Nebraska institutional reciprocal. The two January 1985 CSUDH temporary-home games were physically resolved to the CSUDH Gymnasium/Torodome in Carson from contemporary reporting plus CSUDH facility evidence. Remaining exceptions retain researched status/basis; no blanket geography or primary-arena chronology was used.

## Current-main opponent identity rebase and owner sanity scan — 2026-09-02

Before `INTEGRATION_FROZEN`, USC received the required complete owner sanity scan of the distinct opponent population remaining outside the current Division I program registry. Mechanical current-main key/alias drift was repaired while preserving source labels and `raw_text`.

Owner lineage rulings:
- `St. Vincent's` is treated as the Loyola Marymount program lineage and normalized to `loyola-marymount`.
- `Los Angeles Normal` remains a distinct historical non-D1 identity and is **not** normalized to UCLA; UCLA's accepted basketball history begins with 1919-20.
- generic `Normal School` remains unresolved/distinct and maps to no current program.

The owner approved the remainder of the presented NON_D1 sanity-scan inventory. No game-universe, score/result, site, venue, taxonomy, conference, postseason, or accomplishment research was reopened by this identity-only rebase.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=3ce72167df31c2a7d7b1a38de48a270e6ac09c6e` from `research_base_sha=fb886afc1f940ddc9e5904908cc2f2c5cf7077cb`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
