# Boise State ALL_HISTORY_EXPANSION — Stage 1 founding-era reciprocal checkpoint 0002

**Status: STAGE_1_IN_PROGRESS; no Stage 2; no Implementation or shared-reference mutation.**

## Exact immutable authority
- Research base: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`; baseline on that commit is 1,670 published Boise State rows, 1970-71+.
- Parent initial checkpoint ZIP SHA-256: `888533cc13e3d9a9aa4bb277225ce332d1f7cbfeaa2d445011efd641d92ed259`.
- Updated portable ZIP: `boise-state-expansion-stage1-founding-0002.zip`; SHA-256 `1c84e15edd26889713c8a9b43ebad2dd03b2974556861fd6f4d5edf85a3176a6`.
- Portable ZIP ledger member SHA-256: `de1c3f721ecdcceb513402c0349eaa96c541bdd9ec49e18a71141ebf58f0412d`; census member SHA-256 `7dcc74401a029a29b6b949ded71ac3e9fab2f911d556a8ffe764ef76b133c206`. Full digest manifest is in ZIP.
- GitHub text authority: `research/boise-state/stage1-founding-0002-ledger.csv` (62 games), `...-source-delta.csv` (seven new reciprocal games with exact source excerpts), `...-season-census.csv` (38 candidate seasons). The ZIP carries richer 16-column rows and source inventory; branch CSV provides independently accessible recovery.

## Source-backed increment
Original 55 competitive games from institution's 2024 record book are preserved without reinterpretation: 1968-69 27 games (19-8) and 1969-70 28 games (20-8).

Seven additional distinct school-specific competitive results:
- 1934-35 versus Boise JC in Idaho State University Athletics' retrospective Year-by-Year Results: Idaho State wins 63-19, 53-36, 57-30, 45-36, hence Boise JC losses 19-63, 36-53, 30-57, 36-45. Four distinct rows, no dates. Source: https://isubengals.com/sports/2014/6/18/MBB_0618144002.aspx?id=214
- 1939-40 same institutional reciprocal: Idaho State wins 56-26 and 44-28; hence Boise losses 26-56 and 28-44; dates not supplied.
- March 18, 1940 versus University of Denver at the **Regional AAU Tournament**, in Denver, Colorado: Denver's official retrospective gives Denver W 77-35 / Boise JC L 35-77. Treat as lower-level `POSTSEASON` pending later site research. Source: https://denverpioneers.com/news/2010/5/13/All_Time_Results_1930_39_

This tranche closes with **62 identified supplemental games**, including **five original 1968-70 postseason plus one added 1940 postseason**. Game-type classification is provisional where further evidence may affect junior-college postseason authority. All seven new H/A/N remain `UNKNOWN` (preserve literal reciprocal site tokens; no geography inference). Exact dates remain blank for six Idaho State matches. Neither date nor venue was manufactured.

## Inception / early-year source inventory
- University Archives Athletics Timeline dates Basketball to Dec. 1, 1932, explicitly stating basketball is longest-running athletic program and survived WWII: https://www.boisestate.edu/archives/university-archives/the-boise-state-story/timelines/
- Boise State Athletics Men's Basketball Tradition dates first **Junior College** year to 1933 and junior-college aggregate to 441-346, 1933-1968: https://broncosports.com/sports/2018/5/18/sports-m-baskbl-spec-rel-bosu-m-baskbl-tradition-html
- A third-party site reports Jan. 29, 1933 as a first game W 33-22 versus St. Joseph Academy in Talbot Gym: https://insidersbettingdigest.com/ncaab/teams/boise-state-broncos/ . This has **NOT** been accepted as a game-level identity: original/contemporary proof and eligibility against a high-school opponent are still needed. It supports investigating 1932-33 but is not authoritative acceptance.
- The Boise State `Les Bois` yearbooks 1935-38 are cataloged with athletics subsections at https://scholarworks.boisestate.edu/student_yearbooks/ ; athletics PDF downloads returned HTTP 403 on the initial bounded attempt. No repeated access loops. Catalog existence is not content proof.
- Institutional **1932-33 remains provisional**; 1933-34 alternative not yet closed. The 441-346 junior-college aggregate is **not** a 787-row ledger; 34 candidate 1932-33..1967-68 seasons still have no individual game rows, and two have partial reciprocal coverage.

## Next bounded Stage 1 unit
Search **one coherent systematic junior-college source family** with high yield (alternative accessible school yearbooks, first-party conference/reciprocal histories, or date-indexed contemporary newspaper corpus), harvest season-first in multi-season blocks, preserve full source/raw result and exclusions. Do not prolong archival 403 retries. No owner ruling requested at this step.

**Recovery: continue the same independent Boise State research branch, immutable research_base_sha unchanged, and use this 0002 ZIP / committed 62-game ledger as parent.**
