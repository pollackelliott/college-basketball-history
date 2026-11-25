# Boise State ALL_HISTORY_EXPANSION — Stage 1 College of Idaho first-party result checkpoint 0012

**Status: STAGE_1_IN_PROGRESS.** Same existing Boise State independent Research lane, not Control Center or Implementation. No Stage 2, owner gate, Research freeze, protected-main mutation, canonical basketball mutation or shared/global reference mutation.

## Durable lineage and parent authentication

- Immutable `research_base_sha`: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`. **Do not reset** when main advances.
- Protected `main` at start of unit: `4d91da1800d9d7b535ae2e191f309bfc391ea2ee`, protected=true; current `AGENTS.md` and controlling Stage 1 / expansion lifecycle / convergence / portable execution policy blobs unchanged from checkpoint 0011.
- Parent Research branch head: `e7ed9f35ac22aa13a1a6a74dc6f6d8a2c6234dde`.
- Parent 0011 portable ZIP SHA-256: `763d0344c77df04caf9623ea8b9a3b136ae6a27e76a9b7dfc08edac3b72af901`.
- Current 0012 portable ZIP: `boise-state-expansion-stage1-college-idaho-reciprocals-0012.zip`, SHA-256 **`8865c88035872531be90f104d5d142a7ef3051d3e02794d9eb29e8b57e439604`**.
- Portable ZIP complete 16-column `structured-stage1-ledger.csv` SHA-256 `42e5c114b988d95242842838803429c3c417a59f0517f65d1b317cfc747fcc92`.
- ZIP `manifest.json` verifies all contents by exact SHA-256. Includes 154 full source-backed game rows, source inventory, 38-season accounting/census, residuals, eight-game evidence delta, full 12-row opponent-source census, one approved existing-game date repair, seven unresolved inherited/new candidates, and status.
- Github durable mirrors: `stage1-college-idaho-0012-ledger.csv` (154 concise identities, one prior game date repaired), `...-accounting.csv` (38), `...-season-census.csv` (38), `...-opponent-census.csv` (12 official source rows with reconciliation dispositions), `...-field-repairs.csv` (1), `...-candidates.csv` (7), and this status note. Portable ZIP retains **all** prior raw source testimony and richer 16-field detail.

## Systematic source-family inventory

College of Idaho Athletics first-party **men's basketball season-results archive**:
- https://yoteathletics.com/sports/2012/8/31/MBB_0831125836.aspx
- year URL pattern https://static.yoteathletics.com/custompages/stats/mbasketball/1949.htm through https://static.yoteathletics.com/custompages/stats/mbasketball/1967.htm

All **19** original season pages for 1949-50 through 1967-68 were checked for literal Boise / Boise State references. Boise appears as the modernized `Boise State` name with notes clarifying historical `Boise Junior College`. Only six of the 19 year pages returned Boise-result entries: 1949-50, 1950-51, 1951-52, 1952-53, 1956-57 and 1957-58. The archive itself says complete per-game coverage starts 1958, with *varied* earlier coverage, so lack of a Boise entry is **not no-game or no-team authority**. Do not extrapolate.

The six pages contain **12 source-identified Boise encounters**: eight definitely distinct from the 146 parent ledger entries and added below; one exact same-game date match improving a prior row; three other source matches/possible collisions preserved as uncertain and **not** used to create extra games.

### Eight accepted new distinct competitive game identities (Boise 6-2)

| Season | Date | Boise outcome | first-party College of Idaho reciprocal result |
|---|---|---|---|
| 1949-50 | 1949-12-20 | W 54-51 | at Boise State, CoI L 51-54; https://static.yoteathletics.com/custompages/stats/mbasketball/1949.htm |
| 1950-51 | 1951-01-28 | L 50-69 | at Boise State, CoI W 69-50; https://static.yoteathletics.com/custompages/stats/mbasketball/1950.htm |
| 1951-52 | 1951-12-07 | W 48-45 | BOISE STATE, CoI L 45-48; https://static.yoteathletics.com/custompages/stats/mbasketball/1951.htm |
| 1952-53 | 1952-12-19 | W 77-61 | at Boise State, CoI L 61-77; https://static.yoteathletics.com/custompages/stats/mbasketball/1952.htm |
| 1952-53 | 1952-12-20 | L 62-64 | BOISE STATE, CoI W 64-62; same CoI 1952 page |
| 1956-57 | 1956-12-22 | W 81-54 | at Boise State, CoI L 54-81; https://static.yoteathletics.com/custompages/stats/mbasketball/1956.htm |
| 1957-58 | 1957-12-11 | W 64-48 | BOISE STATE, CoI L 48-64; https://static.yoteathletics.com/custompages/stats/mbasketball/1957.htm |
| 1957-58 | 1957-12-19 | W 63-51 | at Boise State, CoI L 51-63; same CoI 1957 page |

All eight recorded with stable new research IDs and exact source dates. **H/A/N remains UNKNOWN**: CoI archive sometimes prints `at Boise State` while placing the game in `Caldwell, ID`, so locality and literal site tokens are **not** proof of Boise HOME/AWAY/NEUTRAL or an exact venue.

### One accepted source-supported same-game field repair

Pre-existing parent ID `BOISE-EXP-S1-WEST-0007-001`: Boise 1949-50 L 44-56 College of Idaho from a newspaper issued Dec 31 1949 had undetermined date. CoI's first-party dated game list gives exact same opponent/score as 1949-12-22. Preserve game ID, W/L, points and original newspaper testimony; fill only `game_date=1949-12-22`, append stronger source citation, and retain provenance. **Do not add a second identity for that match**.

### Three source rows held for duplicate-risk / score conflict

1. CoI 1951-02-13 W 67-59 (Boise L59-67) versus existing `BOISE-EXP-S1-WEST-0007-003` (newspaper Jan 17 1951 has College Idaho unreadable `C7` Boise 59). Same Boise total, dates/chronology conflict. Cannot establish separate game identity confidently; leave source row as candidate, keep prior game untouched.
2. CoI 1951-12-06 L 50-60 (Boise W60-50) versus existing `BOISE-EXP-S1-WEST-0007-004` (Dec 13 1951 Oregon newspaper Boise W69-50). Same CoI total 50, Boise 60-vs-69 and source dates differ. Possible same-game discrepancy; **do not** inflate ledger. Both raw source attestations preserved.
3. CoI 1956-12-21 L 42-51 (Boise W51-42) versus existing `BOISE-EXP-S1-WEST-0007-008` (Dec 23 contemporary scoreboard Boise W51-43 vs CoI). Same Boise 51 and opponent in same week; likely identical game, **one-point score conflict**. Keep earlier score, original ID and both sources until independently adjudicated.

These three are fully explicit in `...-opponent-census.csv`, `...-candidates.csv`, and ZIP residuals. No owner gate is manufactured; historical identity adjudication remains in Stage 1.

## Mechanical accounting and stop

- Parent 0011: **146** source-backed supplemental game IDs. New 0012: **154 distinct game identities** = 146 previous identities, one with new date, plus eight new ones. Original 145 other rows are unchanged in the portable full ledger.
- Junior-college identities: **99** including **one** documented 1937-38 Boise loss outside MW-listed annual season totals.
- Source-complete 1968-69 and 1969-70 supplemental population: **55**, unchanged.
- Mountain West's **33** recognized junior-college annual seasons still sum **441-346 = 787 games**. Precisely **98** game identities are identified within those seasons; **787 - 98 = 689** aggregate-unmatched. This is **numerical historical coverage debt**, **not** 689 invented game IDs nor proof of identical competition inclusion across all source aggregates.
- Other unresolved: December 1948 University of Idaho varsity played/result unknown, Jan 1957 NNC played/result unknown, 1932-33 inception vs 1933-34 institutional first record, 1937-38 and 1938-39 season accounting, 1950s annual W/L discrepancies, Denver 1940 35-vs-38 same-game score, AAU classifications, and site-field debt. Do not silently settle any of them.
- No protected main, global or shared registries, accepted Boise State 1970-71+ package (1,670 rows), canonical data, or Implementation lock touched.

**Next bounded Stage 1 unit:** seek another systematic first-party opponent result family or address a genuine played/result unknown; do not re-open accepted rows without an exact contradiction, and do not advance to Stage 2 merely on `Proceed`. Research Stage 1 remains OPEN.
