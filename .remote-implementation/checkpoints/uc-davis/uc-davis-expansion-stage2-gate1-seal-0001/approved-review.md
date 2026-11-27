# uc-davis onboarding review

Generated: 2026-11-26T23:52:39.547522+00:00
Input fingerprint: `92ca42dff1d9f73f15bbb872549856f974e910468a185c19e91573c4b11b8841`
Approved plan: `498257f67cc96306ffcda3f25ff872bc6569ccd83df8abe6a9f1ee3a250f326d`

## Preflight summary

- Source rows: 2,632
- Publication-eligible rows: 2,632
- Top-level rows: 668
- Publication-excluded researched rows: 0
- Existing matches: 737
- New canonical games: 1,891
- Identity reviews: 4
- Safe enrichment fields: 20
- Discrepancies: 4
- Conditional discrepancies: 7
- Canonical-only site reviews: 0
- Affected existing public programs: arizona, arkansas, boise-state, byu, california, colorado, colorado-state, dayton, depaul, fresno-state, gonzaga, hawai-i, houston, indiana, iowa-state, kansas, kansas-state, louisville, loyola-chicago, minnesota, missouri, nebraska, ohio-state, oklahoma-state, oregon, oregon-state, saint-joseph-s, saint-louis, san-diego-state, stanford, texas, ucla, unlv, usc, utah, utah-state, washington, washington-state, wisconsin

## Blockers

- None.

## Warnings

- None.

## Non-substantive site-gap provenance

- None.

## Owner decisions

### 1. IDENTITY-UC-DAVIS-EXP-1914-15-004

- Category: identity
- Matchup: uc-davis vs stanford
- Date: [unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=16-23`
- Canonical value: `CBBG-0114369`
- Evidence: CBBG-0114369 1914-1915 [unknown] 36-31 sources=stanford
- Recommended: `REVIEW_REQUIRED`
- Decision: `FORCE_NEW`
- Basis: UC Davis's year-by-year source independently lists two 1914-15 losses to Stanford: 23-16 (this row) and 36-31 (UC-DAVIS-EXP-1914-15-005). Stanford's established STAN-R-0083 and CBBG-0114369 are explicitly the 36-31 game already matched to row 005. The 23-16 meeting is separate; force a new identity, never reuse one canonical game for both.

### 2. CONDITIONAL-DISCREPANCY-UC-DAVIS-EXP-1914-15-004-CBBG-0114369-SCORE

- Category: conditional_discrepancy
- Matchup: stanford vs uc-davis
- Date: [unknown]
- Field: score
- Source value: `23-16`
- Canonical value: `36-31`
- Evidence: stanford [unknown]: 36-31
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0114369`

### 3. CONDITIONAL-DISCREPANCY-UC-DAVIS-EXP-1914-15-004-CBBG-0114369-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: stanford vs uc-davis
- Date: [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: stanford [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0114369`

### 4. IDENTITY-UC-DAVIS-EXP-1936-37-001

- Category: identity
- Matchup: uc-davis vs stanford
- Date: [unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=16-42`
- Canonical value: `CBBG-0114571`
- Evidence: CBBG-0114571 1936-1937 [unknown] 41-16 sources=stanford
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0114571`
- Basis: UC Davis independently records a 1936-37 42-16 loss at Stanford; Stanford's institutional STAN-R-0469 reports one California Aggies home win 41-16 in the same season at Stanford Pavilion. Same program pairing, season, winner, losing team's 16 points, and a one-point winning-score variance favor one contested-score game over manufacturing an uncorroborated second 41/42-16 meeting. Match the established CBBG-0114571 while retaining both literal source scores.

### 5. CONDITIONAL-DISCREPANCY-UC-DAVIS-EXP-1936-37-001-CBBG-0114571-SCORE

- Category: discrepancy
- Matchup: stanford vs uc-davis
- Date: [unknown]
- Field: score
- Source value: `42-16`
- Canonical value: `41-16`
- Evidence: stanford [unknown]: 41-16
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Stanford's reciprocal STAN-R-0469 and published canonical CBBG-0114571 record 41-16; UC Davis's independent year-by-year list records 42-16. Neither source conclusively adjudicates the single-point difference. Conservatively retain the published canonical 41-16, preserve UC Davis's 42-16 raw/source assertion as the documented discrepancy, and present the conflict to Owner Gate 1.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0114571`

### 6. IDENTITY-UC-DAVIS-EXP-1942-43-005

- Category: identity
- Matchup: uc-davis vs california
- Date: [unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=32-43`
- Canonical value: `CBBG-0113018`
- Evidence: CBBG-0113018 1942-1943 [unknown] 50-20 sources=california
- Recommended: `REVIEW_REQUIRED`
- Decision: `FORCE_NEW`
- Basis: UC Davis explicitly lists two distinct 1942-43 California losses, 50-20 (UC-DAVIS-EXP-1942-43-001) and 43-32 (this row). California's CAL-R1-00588 reports the 50-20 Berkeley/Harmon Gym win and is already the confident match to CBBG-0113018. The 43-32 game cannot also match that canonical identity under the one-game/one-canonical rule. Force new; preserve unknown H/A/N.

### 7. CONDITIONAL-DISCREPANCY-UC-DAVIS-EXP-1942-43-005-CBBG-0113018-SCORE

- Category: conditional_discrepancy
- Matchup: california vs uc-davis
- Date: [unknown]
- Field: score
- Source value: `43-32`
- Canonical value: `50-20`
- Evidence: california [unknown]: 50-20
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0113018`

### 8. CONDITIONAL-DISCREPANCY-UC-DAVIS-EXP-1942-43-005-CBBG-0113018-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: california vs uc-davis
- Date: [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: california [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0113018`

### 9. IDENTITY-UC-DAVIS-EXP-1947-48-006

- Category: identity
- Matchup: uc-davis vs california
- Dates: source [unknown]; canonical 1947-12-13
- Field: game_identity
- Source value: `date=[unknown]; score=39-54`
- Canonical value: `CBBG-0113104`
- Evidence: CBBG-0113104 1947-1948 1947-12-13 58-42 sources=california
- Recommended: `REVIEW_REQUIRED`
- Decision: `FORCE_NEW`
- Basis: UC Davis lists two 1947-48 California losses: dated 1947-12-13 58-42 (UC-DAVIS-EXP-1947-48-003), and undated 54-39 (this row). California's CAL-R1-00710 explicitly reports Dec 13 58-42 at Harmon Gym, already confidently matched to CBBG-0113104. The 54-39 game is a separate meeting and cannot be assigned to that same canonical identity. Force new, preserving date/site uncertainty.

### 10. CONDITIONAL-DISCREPANCY-UC-DAVIS-EXP-1947-48-006-CBBG-0113104-SCORE

- Category: conditional_discrepancy
- Matchup: california vs uc-davis
- Dates: source [unknown]; canonical 1947-12-13
- Field: score
- Source value: `54-39`
- Canonical value: `58-42`
- Evidence: california 1947-12-13: 58-42
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0113104`

### 11. CONDITIONAL-DISCREPANCY-UC-DAVIS-EXP-1947-48-006-CBBG-0113104-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: california vs uc-davis
- Dates: source [unknown]; canonical 1947-12-13
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: california 1947-12-13: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0113104`

### 12. DISCREPANCY-UC-DAVIS-EXP-1973-74-001-SITE_TYPE

- Category: discrepancy
- Matchup: minnesota vs uc-davis
- Date: 1973-12-01
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: minnesota 1973-12-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: UC Davis's 1973-12-01 Minnesota loss 45-55 carries a generic 'vs.' cue and Hickey Gymnasium inference, but Minnesota's dated institutional MINRAW-01436 records the exact 55-45 win as HOME at Williams Arena, Minneapolis. The reciprocal exact-score/date and explicit venue favor the established Minnesota-home canonical site. Recommend KEEP_CANONICAL, retain UC Davis's original source and record the opposing presentation for owner review.

### 13. DISCREPANCY-UC-DAVIS-EXP-1973-74-002-SITE_TYPE

- Category: discrepancy
- Matchup: uc-davis vs wisconsin
- Date: 1973-12-03
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: wisconsin 1973-12-03: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: UC Davis's 1973-12-03 53-97 Wisconsin loss is coded from 'vs.' and Hickey Gymnasium, but Wisconsin's WISCRAW-01405 explicitly records the 97-53 win on the same date HOME at Wisconsin Field House, Madison. Strong date/score/facility reciprocal evidence favors the existing Wisconsin-home canonical classification. Recommend KEEP_CANONICAL and preserve source evidence for owner review.

### 14. DISCREPANCY-UC-DAVIS-EXP-1973-74-004-SITE_TYPE

- Category: discrepancy
- Matchup: oregon vs uc-davis
- Date: 1973-12-19
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: oregon 1973-12-19: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: UC Davis's 1973-12-19 59-82 Oregon loss carries a generic 'vs.' and Hickey Gymnasium inference; Oregon's ORERAW-01617 explicitly documents the 82-59 win at home (McArthur Court, Eugene) on that date. Retain the independently corroborated Oregon-home canonical site with KEEP_CANONICAL and preserve UC Davis's alternate curated representation for the owner.
