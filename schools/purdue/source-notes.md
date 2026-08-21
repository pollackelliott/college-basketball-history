# Purdue source notes

## Principal source

**2025-26 Purdue Men's Basketball Media Guide / Record Book**, Purdue University Athletics.

High-value sections used directly:

- Team history / quick facts — opening pages
- Annual team results — season record cross-check
- Year-by-Year Scores — printed pp. 114-132
- Overtime Games — printed pp. 133-134
- Neutral-Site Games — printed pp. 139-141
- NCAA Tournament History / game-by-game results — printed pp. 160-162
- Big Ten Tournament History / game-by-game results — printed pp. 171-172

The year-by-year section is the row-level chronological source. Extraction produced **3,047 competitive games through 2024-25** and exactly reproduces Purdue's printed **1,971-1,076** on-court record. Every season's extracted W-L total reconciles to the annual record table.

Dedicated postseason and facility sections are cross-check/evidence layers, not blanket replacements for the chronological ledger.

## Completed 2025-26 source

The project owner supplied a completed 2025-26 schedule/results table through the NCAA Tournament.

The package includes **39 competitive games (30-9)** and excludes both exhibitions:

- 2025-10-24 at Kentucky — exhibition
- 2025-10-29 Indianapolis — exhibition

The completed table supplies explicit H/A/N syntax and venue/city/state for 2025-26.

## Conference-tournament source

The project owner supplied **Conference Tournament Site Reference** workbook.

Only its **Big Ten section** is authorized as complete/reliable for Purdue assembly. It is used as an ephemeral lookup source for Big Ten Tournament shared physical venue/city/state from 1998 through 2026. Non-Big-Ten portions are not treated as universal canon and are not ingested from this package.

Shared tournament-site data never establishes H/A/N. Purdue Big Ten Tournament games are independently neutral from the tournament/game context and year-by-year `vs.` notation.

## Purdue home-court evidence

Primary Purdue institutional historical source:

https://purduesports.com/purdue-university-mens-basketball-official-athletic-site-25

Additional Purdue-hosted historical record-book material:

https://storage.googleapis.com/purduesports-com-prod/2025/05/16/RufRiHTk3zth5WBEGuqXS4jbQPH9VuwvmhXng2xT.pdf

Institutional material supports:

- original basketball home in **Military Hall and Gymnasium / Old Gym**
- move to the downtown **Lafayette Coliseum** for home games in 1907
- first **Memorial Gymnasium** basketball game on **1910-01-08**, a 55-14 Purdue win
- four temporary home games at **Lafayette Jefferson High School** in calendar 1929
- renewed Lafayette Jefferson use from 1934 until Purdue Fieldhouse opened
- first **Purdue Fieldhouse / Lambert Fieldhouse** game on **1937-12-11**, a 61-18 win over Indiana State
- first **Purdue Arena / Mackey Arena** game on **1967-12-02**, a 73-71 loss to UCLA

The exact four 1929 Lafayette Jefferson games are not identified by the institutional narrative. All ten calendar-1929 Purdue home rows therefore keep venue blank rather than assigning six of them to Memorial Gymnasium by guess.

The continuous 1934-37 Lafayette Jefferson package boundary is established from the institutional chronology plus the year-by-year schedule: first 1934-35 home game **1934-12-10 vs. Western State**, last 1936-37 home game **1937-02-27 vs. Indiana**.

## NCAA Tournament normalization

The dedicated Purdue NCAA Tournament table contains 87 games through 2025 and reconciles to its printed 51-36 tournament record. Four completed 2026 NCAA games extend the portfolio to **91 games, 54-37**.

NCAA physical sites are normalized against established project venue identities. NCAA rows require complete venue/city/state under the current repository safety gate.

Three dedicated NCAA-table score transcriptions conflict with the year-by-year ledger:

- **1980-03-08 vs. St. John's:** dedicated NCAA table prints 87-73; year-by-year prints **87-72**
- **1988-03-19 vs. Memphis:** dedicated NCAA table prints 100-79; year-by-year prints **100-73**
- **2015-03-19 vs. Cincinnati:** dedicated NCAA table prints 66-67; year-by-year prints **65-66 OT**

Independent archival checks support the year-by-year values in all three cases, so the package retains 87-72, 100-73, and 65-66 OT respectively. The raw year-by-year line remains preserved on each source row.

Historical NCAA opening-round normalization follows the current project vocabulary: a 1977 first-round game in the 32-team field maps to `R32`; opening first-round games in the expanded 1979-84 fields map to `Play-in`; 1985-and-later first rounds map to `R64`. Historical third-place/consolation games retain `NCAA_TOURNAMENT` with blank public round.

## Big Ten Tournament normalization

Purdue's dedicated Big Ten Tournament table contains **46 games through 2025 (21-25)**. The owner-supplied 2026 results add four wins, producing **50 games, 25-25**.

One internal 2016 score conflict was resolved:

- **2016-03-12 vs. Michigan:** dedicated Big Ten Tournament table prints 75-69, while the year-by-year ledger prints **76-59**.

Purdue's official game recap and official 2015-16 schedule both confirm **Purdue 76, Michigan 59**:

https://purduesports.com/news/2016/03/12/no-13-purdue-advances-to-big-ten-final

Public Big Ten Tournament rounds remain blank except championship games.

## NIT and other postseason

Purdue annual records identify NIT participation in 1971, 1974, 1979, 1981, 1982, 1992, 2001, and 2004. The package classifies **27 NIT games, 20-7**.

Year-by-year footnotes establish West Lafayette, New York, Indianapolis, or South Bend tournament-site context where available. Physical venue is left blank when the source establishes only city/state and a specific building cannot be proved safely.

Purdue's 2012-13 annual results identify a **CBI (1-1)** appearance. The current repository `data-schema.md` exposes only `REGULAR_SEASON`, `CONFERENCE_TOURNAMENT`, `NCAA_TOURNAMENT`, and `NIT`. Accordingly the two CBI rows preserve `CBI` in `event_or_tournament` while remaining `REGULAR_SEASON` for current-schema compatibility.

## 1995-96 forfeiture / vacation evidence

Purdue official reporting states that NCAA sanctions later affected the 1995-96 season. Purdue's official response says the university was asked to forfeit 24 games because of an ineligible player's participation, while a later Purdue article notes that the NCAA did not recognize 19 victories.

Purdue official response:

https://purduesports.com/purdue-responds-to-ncaa-announcement

The package's principal row-level sources do not identify the exact affected-game set with sufficient authority. Because the project preserves on-court results and stores administrative treatment separately, all 1995-96 played scores/results remain intact and row-level `administrative_status` is left blank pending a reliable affected-game list.

## Opponent normalization

Current Division-I identities use the repository's established program keys. Historical/non-current opponents are preserved with stable descriptive keys rather than speculatively merged.

Examples:

- `Connecticut` -> `uconn`
- `Miami, Fla.` / `Miami (FL)` -> `miami`
- `Western State` -> `western-michigan` (historical institutional lineage)
- `Rose Poly` -> `rose-hulman`
- `LIU Brooklyn` -> `long-island-university`
- `St. Joseph, Ind.` / `St. Joseph’s, Ind.` -> `saint-josephs-indiana`
- `Washington, Mo.` -> `washington-mo`

The package contains **324 distinct source labels mapped to 312 canonical opponent identities**, with no unresolved opponent labels.

## Venue hierarchy

1. explicit game-level venue/location evidence
2. dedicated Purdue NCAA site evidence plus established physical identity
3. owner-supplied Big Ten-complete tournament-site reference
4. Purdue institutional primary-home chronology, only after independent home classification

Venue chronology and geography never infer H/A/N.
