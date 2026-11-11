# uc-davis onboarding review

Generated: 2026-11-11T15:36:00.623680+00:00
Input fingerprint: `814979811ca9812eb5ea736f8834ecd9e9110efb009e069e3e68b784a5dce070`
Approved plan: `8c032a33b6cb071b3d57eb3595afa1f8c0f656d9280684c5069e4bae29882cd0`

## Preflight summary

- Source rows: 668
- In-scope rows: 668
- Pre-cutoff researched rows: 0
- Existing matches: 86
- New canonical games: 582
- Identity reviews: 0
- Safe enrichment fields: 110
- Discrepancies: 2
- Conditional discrepancies: 0
- Canonical-only site reviews: 0
- Affected existing public programs: arizona, arkansas, boise-state, california, colorado, colorado-state, fresno-state, hawai-i, indiana, iowa-state, kansas, louisville, loyola-chicago, oklahoma-state, oregon, oregon-state, saint-joseph-s, san-diego-state, stanford, texas, ucla, usc, utah, utah-state, washington, washington-state

## Blockers

- None.

## Warnings

- None.

## Non-substantive site-gap provenance

- None.

## Owner decisions

### 1. DISCREPANCY-UC-DAVIS-2013-14-005-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs uc-davis
- Date: 2013-11-23
- Field: overtime_periods
- Source value: `1`
- Canonical value: `0`
- Evidence: loyola-chicago 2013-11-23: 0
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use UC Davis's accepted source value of 1 overtime. UC Davis's official box score shows an OT period (12-9) and its official recap calls the 64-61 result an overtime win over Loyola Chicago on Nov. 23, 2013. This is affirmative institutional evidence that the canonical 0 is stale. https://ucdavisaggies.com/sports/mens-basketball/stats/2013-14/loyola/boxscore/2393 https://ucdavisaggies.com/news/2013/11/23/UC_Davis_Wins_Overtime_Thriller_64_61.aspx

### 2. DISCREPANCY-UC-DAVIS-2018-19-013-GAME_DATE

- Category: discrepancy
- Matchup: uc-davis vs usc
- Dates: source 2018-12-30; canonical 2018-12-29
- Field: game_date
- Source value: `2018-12-30`
- Canonical value: `2018-12-29`
- Evidence: usc 2018-12-29: 2018-12-29
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use UC Davis's accepted 2018-12-30 date. UC Davis's official box score dates the 73-55 game at USC Dec. 30, 2018, and USC's official recap and postgame notes independently date the same score/game Sunday, Dec. 30. The canonical 2018-12-29 date is stale. https://ucdavisaggies.com/sports/mens-basketball/stats/2018-19/usc/boxscore/9736 https://usctrojans.com/news/2018/12/30/usc-trojans-m-basketball-recap-uc-davis-aggies-elijah-weaver https://usctrojans.com/documents/download/2018/12/30/December_30_vs_UC_Davis.pdf

### 3. ACCOMPLISHMENTS-UC-DAVIS

- Category: accomplishments
- Matchup: uc-davis
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"ROUND_OF_64","best_finish_year":"2017","conference_regular_season_championships":"2","conference_tournament_championships":"1","final_four_appearances":"0","national_championships":"0","ncaa_tournament_appearances":"1"}`
- Canonical value: `{"best_finish_key":"ROUND_OF_64","best_finish_year":2017,"final_four_appearances":0,"national_championships":0,"ncaa_tournament_appearances":1}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `VERIFY_REFERENCE_VALUES`
- Basis: Verify the existing reference values without applying a redundant patch. Big West official records list UC Davis as men's basketball regular-season champion in 2014-15 and 2017-18 (2 total) and conference tournament champion in 2017 (1 total). UC Davis's official record book and Big West NCAA history support the existing NCAA appearance/best-finish values. https://bigwest.org/sports/2022/6/9/all-time-big-west-regular-season-champions.aspx https://bigwest.org/sports/2022/9/23/mbb-big-west-championship-history.aspx https://ucdavisaggies.com/sports/2026/5/19/mens-basketball-record-book.aspx https://bigwest.org/sports/2022/9/24/mbb-big-west-ncaa-tournament-history.aspx

### 4. PUBLICATION-UC-DAVIS

- Category: publication
- Matchup: uc-davis
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 668 in-scope source rows; 0 identity reviews; 2 definite and 0 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `ENABLE_PUBLIC_PAGE`
- Basis: Recommend enabling UC Davis only through the normal explicit Owner Gate 1, sealed apply, exact Preview, explicit Owner Gate 2, merge, and Production-proof sequence after this exact recommendation map is approved.
