# gonzaga onboarding review

Generated: 2026-10-27T02:19:45.117597+00:00
Input fingerprint: `d353d010351ae09ddc4b5ce87d8bb83595a0851091bdb062d2534a0d82ddd4c5`

## Preflight summary

- Source rows: 2,053
- In-scope rows: 2,053
- Pre-cutoff researched rows: 0
- Existing matches: 421
- New canonical games: 1,623
- Identity reviews: 9
- Safe enrichment fields: 654
- Discrepancies: 34
- Conditional discrepancies: 17
- Canonical-only site reviews: 0
- Affected existing public programs: alabama, arizona, arizona-state, arkansas, auburn, baylor, boise-state, butler, byu, california, chicago-state, cincinnati, clemson, colorado, creighton, depaul, duke, fairleigh-dickinson, florida, florida-state, georgia, georgia-tech, houston, illinois, indiana, iowa, iowa-state, kansas, kansas-state, kentucky, louisville, marquette, maryland, michigan, michigan-state, minnesota, mississippi-state, missouri, nc-state, north-carolina, northwestern, notre-dame, ohio-state, oklahoma, oklahoma-state, oregon, oregon-state, penn-state, providence, purdue, seton-hall, smu, south-carolina, st-john-s, stanford, syracuse, tcu, tennessee, texas, texas-a-m, texas-tech, ucla, uconn, usc, utah, villanova, virginia, virginia-tech, wake-forest, washington, washington-state, west-virginia, wisconsin, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. DISCREPANCY-GONZAGA-1959-60-014-SITE_TYPE

- Category: discrepancy
- Matchup: creighton vs gonzaga
- Date: 1960-01-30
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: creighton 1960-01-30: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 2. DISCREPANCY-GONZAGA-1960-61-009-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs st-john-s
- Date: 1960-12-22
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: st-john-s 1960-12-22: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 3. IDENTITY-GONZAGA-1961-62-019

- Category: identity
- Matchup: gonzaga vs washington-state
- Dates: source 1962-02-05; canonical 1961-12-11;1962-02-08
- Field: game_identity
- Source value: `date=1962-02-05; score=-`
- Canonical value: `CBBG-0116649;CBBG-0116660`
- Evidence: CBBG-0116649 1961-1962 1961-12-11 73-74 sources=washington-state; CBBG-0116660 1961-1962 1962-02-08 74-61 sources=washington-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 4. CONDITIONAL-DISCREPANCY-GONZAGA-1961-62-019-CBBG-0116649-GAME_DATE

- Category: conditional_discrepancy
- Matchup: gonzaga vs washington-state
- Dates: source 1962-02-05; canonical 1961-12-11
- Field: game_date
- Source value: `1962-02-05`
- Canonical value: `1961-12-11`
- Evidence: washington-state 1961-12-11: 1961-12-11
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0116649`

### 5. CONDITIONAL-DISCREPANCY-GONZAGA-1961-62-019-CBBG-0116649-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: gonzaga vs washington-state
- Dates: source 1962-02-05; canonical 1961-12-11
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1961-12-11: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0116649`

### 6. CONDITIONAL-DISCREPANCY-GONZAGA-1961-62-019-CBBG-0116649-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: gonzaga vs washington-state
- Dates: source 1962-02-05; canonical 1961-12-11
- Field: result_winner_team_key
- Source value: `gonzaga`
- Canonical value: `washington-state`
- Evidence: washington-state 1961-12-11: washington-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0116649`

### 7. CONDITIONAL-DISCREPANCY-GONZAGA-1961-62-019-CBBG-0116660-GAME_DATE

- Category: conditional_discrepancy
- Matchup: gonzaga vs washington-state
- Dates: source 1962-02-05; canonical 1962-02-08
- Field: game_date
- Source value: `1962-02-05`
- Canonical value: `1962-02-08`
- Evidence: washington-state 1962-02-08: 1962-02-08
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0116660`

### 8. DISCREPANCY-GONZAGA-1969-70-009-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1970-01-03
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1970-01-03: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 9. IDENTITY-GONZAGA-1970-71-011

- Category: identity
- Matchup: gonzaga vs boise-state
- Dates: source 1971-01-11; canonical 1971-01-12;1971-02-27
- Field: game_identity
- Source value: `date=1971-01-11; score=-`
- Canonical value: `CBBG-0171862;CBBG-0171877`
- Evidence: CBBG-0171862 1970-1971 1971-01-12 90-74 sources=boise-state; CBBG-0171877 1970-1971 1971-02-27 87-92 sources=boise-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 10. CONDITIONAL-DISCREPANCY-GONZAGA-1970-71-011-CBBG-0171862-GAME_DATE

- Category: conditional_discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1971-01-11; canonical 1971-01-12
- Field: game_date
- Source value: `1971-01-11`
- Canonical value: `1971-01-12`
- Evidence: boise-state 1971-01-12: 1971-01-12
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0171862`

### 11. CONDITIONAL-DISCREPANCY-GONZAGA-1970-71-011-CBBG-0171877-GAME_DATE

- Category: conditional_discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1971-01-11; canonical 1971-02-27
- Field: game_date
- Source value: `1971-01-11`
- Canonical value: `1971-02-27`
- Evidence: boise-state 1971-02-27: 1971-02-27
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0171877`

### 12. CONDITIONAL-DISCREPANCY-GONZAGA-1970-71-011-CBBG-0171877-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1971-01-11; canonical 1971-02-27
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: boise-state 1971-02-27: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0171877`

### 13. CONDITIONAL-DISCREPANCY-GONZAGA-1970-71-011-CBBG-0171877-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1971-01-11; canonical 1971-02-27
- Field: result_winner_team_key
- Source value: `boise-state`
- Canonical value: `gonzaga`
- Evidence: boise-state 1971-02-27: gonzaga
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0171877`

### 14. DISCREPANCY-GONZAGA-1971-72-021-SITE_TYPE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Date: 1972-02-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: boise-state 1972-02-18: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 15. DISCREPANCY-GONZAGA-1973-74-004-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1973-12-10
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1973-12-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 16. DISCREPANCY-GONZAGA-1974-75-010-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1975-01-02
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1975-01-02: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 17. IDENTITY-GONZAGA-1975-76-004

- Category: identity
- Matchup: gonzaga vs creighton
- Dates: source 1975-12-11; canonical 1975-12-09
- Field: game_identity
- Source value: `date=1975-12-11; score=-`
- Canonical value: `CBBG-0149289`
- Evidence: CBBG-0149289 1975-1976 1975-12-09 70-62 sources=creighton
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 18. CONDITIONAL-DISCREPANCY-GONZAGA-1975-76-004-CBBG-0149289-GAME_DATE

- Category: conditional_discrepancy
- Matchup: creighton vs gonzaga
- Dates: source 1975-12-11; canonical 1975-12-09
- Field: game_date
- Source value: `1975-12-11`
- Canonical value: `1975-12-09`
- Evidence: creighton 1975-12-09: 1975-12-09
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0149289`

### 19. DISCREPANCY-GONZAGA-1975-76-016-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1976-01-25
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1976-01-25: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 20. DISCREPANCY-GONZAGA-1976-77-003-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1976-12-03
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1976-12-03: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 21. DISCREPANCY-GONZAGA-1976-77-014-SITE_TYPE

- Category: discrepancy
- Matchup: creighton vs gonzaga
- Date: 1977-01-15
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: creighton 1977-01-15: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 22. DISCREPANCY-GONZAGA-1978-79-008-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1978-12-13
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1978-12-13: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 23. DISCREPANCY-GONZAGA-1980-81-005-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1980-12-13
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1980-12-13: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 24. DISCREPANCY-GONZAGA-1981-82-002-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1981-12-02
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1981-12-02: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 25. DISCREPANCY-GONZAGA-1982-83-003-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1982-12-01
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1982-12-01: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 26. DISCREPANCY-GONZAGA-1983-84-007-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1983-12-12
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1983-12-12: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 27. DISCREPANCY-GONZAGA-1985-86-004-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1985-12-02
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1985-12-02: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 28. DISCREPANCY-GONZAGA-1985-86-009-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs iowa
- Date: 1985-12-23
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: iowa 1985-12-23: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 29. IDENTITY-GONZAGA-1989-90-006

- Category: identity
- Matchup: gonzaga vs boise-state
- Dates: source 1989-12-09; canonical 1989-12-10
- Field: game_identity
- Source value: `date=1989-12-09; score=-`
- Canonical value: `CBBG-0172348`
- Evidence: CBBG-0172348 1989-1990 1989-12-10 54-52 sources=boise-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 30. CONDITIONAL-DISCREPANCY-GONZAGA-1989-90-006-CBBG-0172348-GAME_DATE

- Category: conditional_discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1989-12-09; canonical 1989-12-10
- Field: game_date
- Source value: `1989-12-09`
- Canonical value: `1989-12-10`
- Evidence: boise-state 1989-12-10: 1989-12-10
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0172348`

### 31. DISCREPANCY-GONZAGA-1991-92-005-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs usc
- Date: 1991-12-04
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: usc 1991-12-04: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 32. IDENTITY-GONZAGA-1992-93-003

- Category: identity
- Matchup: gonzaga vs usc
- Dates: source 1992-12-07; canonical 1992-12-05
- Field: game_identity
- Source value: `date=1992-12-07; score=-`
- Canonical value: `CBBG-0069448`
- Evidence: CBBG-0069448 1992-1993 1992-12-05 59-77 sources=usc
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 33. CONDITIONAL-DISCREPANCY-GONZAGA-1992-93-003-CBBG-0069448-GAME_DATE

- Category: conditional_discrepancy
- Matchup: gonzaga vs usc
- Dates: source 1992-12-07; canonical 1992-12-05
- Field: game_date
- Source value: `1992-12-07`
- Canonical value: `1992-12-05`
- Evidence: usc 1992-12-05: 1992-12-05
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0069448`

### 34. IDENTITY-GONZAGA-1998-99-001

- Category: identity
- Matchup: gonzaga vs kansas
- Dates: source 1998-11-14; canonical 1998-11-13
- Field: game_identity
- Source value: `date=1998-11-14; score=-`
- Canonical value: `CBBG-0013575`
- Evidence: CBBG-0013575 1998-1999 1998-11-13 66-80 sources=kansas
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 35. CONDITIONAL-DISCREPANCY-GONZAGA-1998-99-001-CBBG-0013575-GAME_DATE

- Category: conditional_discrepancy
- Matchup: gonzaga vs kansas
- Dates: source 1998-11-14; canonical 1998-11-13
- Field: game_date
- Source value: `1998-11-14`
- Canonical value: `1998-11-13`
- Evidence: kansas 1998-11-13: 1998-11-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0013575`

### 36. DISCREPANCY-GONZAGA-1998-99-005-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1998-11-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1998-11-28: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 37. DISCREPANCY-GONZAGA-1998-99-009-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington
- Date: 1998-12-08
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington 1998-12-08: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 38. IDENTITY-GONZAGA-1998-99-014

- Category: identity
- Matchup: gonzaga vs boise-state
- Dates: source 1999-01-02; canonical 1999-01-03
- Field: game_identity
- Source value: `date=1999-01-02; score=-`
- Canonical value: `CBBG-0172590`
- Evidence: CBBG-0172590 1998-1999 1999-01-03 58-68 sources=boise-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 39. CONDITIONAL-DISCREPANCY-GONZAGA-1998-99-014-CBBG-0172590-GAME_DATE

- Category: conditional_discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1999-01-02; canonical 1999-01-03
- Field: game_date
- Source value: `1999-01-02`
- Canonical value: `1999-01-03`
- Evidence: boise-state 1999-01-03: 1999-01-03
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0172590`

### 40. CONDITIONAL-DISCREPANCY-GONZAGA-1998-99-014-CBBG-0172590-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1999-01-02; canonical 1999-01-03
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: boise-state 1999-01-03: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0172590`

### 41. DISCREPANCY-GONZAGA-1999-00-003-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1999-11-29
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1999-11-29: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 42. DISCREPANCY-GONZAGA-1999-00-008-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington
- Date: 1999-12-13
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington 1999-12-13: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 43. IDENTITY-GONZAGA-2003-04-004

- Category: identity
- Matchup: gonzaga vs georgia
- Dates: source 2003-11-24; canonical 2003-11-29
- Field: game_identity
- Source value: `date=2003-11-24; score=-`
- Canonical value: `CBBG-0042638`
- Evidence: CBBG-0042638 2003-2004 2003-11-29 76-82 sources=georgia
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 44. CONDITIONAL-DISCREPANCY-GONZAGA-2003-04-004-CBBG-0042638-GAME_DATE

- Category: conditional_discrepancy
- Matchup: georgia vs gonzaga
- Dates: source 2003-11-24; canonical 2003-11-29
- Field: game_date
- Source value: `2003-11-24`
- Canonical value: `2003-11-29`
- Evidence: georgia 2003-11-29: 2003-11-29
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0042638`

### 45. CONDITIONAL-DISCREPANCY-GONZAGA-2003-04-004-CBBG-0042638-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: georgia vs gonzaga
- Dates: source 2003-11-24; canonical 2003-11-29
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgia 2003-11-29: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0042638`

### 46. DISCREPANCY-GONZAGA-2003-04-008-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs missouri
- Date: 2003-12-13
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: missouri 2003-12-13: UNKNOWN
- Recommended: `LEAVE_UNRESOLVED`
- Decision: `PENDING`
- Basis: [required before approval]

### 47. DISCREPANCY-GONZAGA-2005-06-008-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs oklahoma-state
- Date: 2005-12-10
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: oklahoma-state 2005-12-10: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 48. DISCREPANCY-GONZAGA-2006-07-003-SITE_TYPE

- Category: discrepancy
- Matchup: baylor vs gonzaga
- Date: 2006-11-15
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: baylor 2006-11-15: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 49. DISCREPANCY-GONZAGA-2007-08-008-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs uconn
- Date: 2007-12-01
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: uconn 2007-12-01: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 50. DISCREPANCY-GONZAGA-2007-08-012-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs oklahoma
- Date: 2007-12-20
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: oklahoma 2007-12-20: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 51. DISCREPANCY-GONZAGA-2007-08-015-SITE_TYPE

- Category: discrepancy
- Matchup: georgia vs gonzaga
- Date: 2008-01-05
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgia 2008-01-05: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 52. DISCREPANCY-GONZAGA-2014-15-006-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs st-john-s
- Date: 2014-11-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-john-s 2014-11-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 53. DISCREPANCY-GONZAGA-2014-15-009-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 2014-12-10
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 2014-12-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 54. IDENTITY-GONZAGA-2017-18-006

- Category: identity
- Matchup: gonzaga vs texas
- Dates: source 2017-11-26; canonical 2017-11-25
- Field: game_identity
- Source value: `date=2017-11-26; score=-`
- Canonical value: `CBBG-0061100`
- Evidence: CBBG-0061100 2017-2018 2017-11-25 76-71 sources=texas
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 55. CONDITIONAL-DISCREPANCY-GONZAGA-2017-18-006-CBBG-0061100-GAME_DATE

- Category: conditional_discrepancy
- Matchup: gonzaga vs texas
- Dates: source 2017-11-26; canonical 2017-11-25
- Field: game_date
- Source value: `2017-11-26`
- Canonical value: `2017-11-25`
- Evidence: texas 2017-11-25: 2017-11-25
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0061100`

### 56. DISCREPANCY-GONZAGA-2020-21-004-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs iowa
- Date: 2020-12-19
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: iowa 2020-12-19: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 57. DISCREPANCY-GONZAGA-2021-22-009-SITE_TYPE

- Category: discrepancy
- Matchup: alabama vs gonzaga
- Date: 2021-12-04
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: alabama 2021-12-04: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 58. DISCREPANCY-GONZAGA-2022-23-004-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs kentucky
- Date: 2022-11-20
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: kentucky 2022-11-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 59. DISCREPANCY-GONZAGA-2024-25-001-SITE_TYPE

- Category: discrepancy
- Matchup: baylor vs gonzaga
- Date: 2024-11-04
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: baylor 2024-11-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 60. DISCREPANCY-GONZAGA-2025-26-002-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs oklahoma
- Date: 2025-11-08
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: oklahoma 2025-11-08: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 61. ACCOMPLISHMENTS-GONZAGA

- Category: accomplishments
- Matchup: gonzaga
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"NATIONAL_RUNNER_UP","best_finish_year":"2021","conference_regular_season_championships":"29","conference_tournament_championships":"23","final_four_appearances":"2","national_championships":"0","ncaa_tournament_appearances":"28"}`
- Canonical value: `{"best_finish_key":"NATIONAL_RUNNER_UP","best_finish_year":2021,"final_four_appearances":2,"national_championships":0,"ncaa_tournament_appearances":28}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `PENDING`
- Basis: [required before approval]

### 62. PUBLICATION-GONZAGA

- Category: publication
- Matchup: gonzaga
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 2,053 in-scope source rows; 9 identity reviews; 34 definite and 17 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `PENDING`
- Basis: [required before approval]
