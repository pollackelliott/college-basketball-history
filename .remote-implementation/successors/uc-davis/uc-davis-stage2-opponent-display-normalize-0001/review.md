# uc-davis onboarding review

Generated: 2026-11-11T15:20:57.885662+00:00
Input fingerprint: `814979811ca9812eb5ea736f8834ecd9e9110efb009e069e3e68b784a5dce070`

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
- Decision: `PENDING`
- Basis: [required before approval]

### 2. DISCREPANCY-UC-DAVIS-2018-19-013-GAME_DATE

- Category: discrepancy
- Matchup: uc-davis vs usc
- Dates: source 2018-12-30; canonical 2018-12-29
- Field: game_date
- Source value: `2018-12-30`
- Canonical value: `2018-12-29`
- Evidence: usc 2018-12-29: 2018-12-29
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 3. ACCOMPLISHMENTS-UC-DAVIS

- Category: accomplishments
- Matchup: uc-davis
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"ROUND_OF_64","best_finish_year":"2017","conference_regular_season_championships":"2","conference_tournament_championships":"1","final_four_appearances":"0","national_championships":"0","ncaa_tournament_appearances":"1"}`
- Canonical value: `{"best_finish_key":"ROUND_OF_64","best_finish_year":2017,"final_four_appearances":0,"national_championships":0,"ncaa_tournament_appearances":1}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `PENDING`
- Basis: [required before approval]

### 4. PUBLICATION-UC-DAVIS

- Category: publication
- Matchup: uc-davis
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 668 in-scope source rows; 0 identity reviews; 2 definite and 0 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `PENDING`
- Basis: [required before approval]
