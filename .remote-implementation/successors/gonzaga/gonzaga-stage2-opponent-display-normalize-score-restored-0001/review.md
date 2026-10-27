# gonzaga onboarding review

Generated: 2026-10-27T12:36:33.668545+00:00
Input fingerprint: `342773aa9ed265b88c7b6e7bb69ad32a5043eff0dbd85f6ff3e826bdf4ef00db`

## Preflight summary

- Source rows: 2,053
- In-scope rows: 2,053
- Pre-cutoff researched rows: 0
- Existing matches: 426
- New canonical games: 1,623
- Identity reviews: 4
- Safe enrichment fields: 659
- Discrepancies: 52
- Conditional discrepancies: 9
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
- Source value: `date=1962-02-05; score=74-61`
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

### 5. CONDITIONAL-DISCREPANCY-GONZAGA-1961-62-019-CBBG-0116649-SCORE

- Category: conditional_discrepancy
- Matchup: gonzaga vs washington-state
- Dates: source 1962-02-05; canonical 1961-12-11
- Field: score
- Source value: `74-61`
- Canonical value: `73-74`
- Evidence: washington-state 1961-12-11: 73-74
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0116649`

### 6. CONDITIONAL-DISCREPANCY-GONZAGA-1961-62-019-CBBG-0116649-SITE_TYPE

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

### 7. CONDITIONAL-DISCREPANCY-GONZAGA-1961-62-019-CBBG-0116649-RESULT_WINNER_TEAM_KEY

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

### 8. CONDITIONAL-DISCREPANCY-GONZAGA-1961-62-019-CBBG-0116660-GAME_DATE

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

### 9. DISCREPANCY-GONZAGA-1969-70-009-SITE_TYPE

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

### 10. DISCREPANCY-GONZAGA-1970-71-011-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1971-01-11; canonical 1971-01-12
- Field: game_date
- Source value: `1971-01-11`
- Canonical value: `1971-01-12`
- Evidence: boise-state 1971-01-12: 1971-01-12
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 11. DISCREPANCY-GONZAGA-1971-72-005-SCORE

- Category: discrepancy
- Matchup: gonzaga vs oregon
- Date: 1971-12-11
- Field: score
- Source value: `69-87`
- Canonical value: `60-87`
- Evidence: oregon 1971-12-11: 60-87
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 12. DISCREPANCY-GONZAGA-1971-72-021-SITE_TYPE

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

### 13. DISCREPANCY-GONZAGA-1972-73-009-SCORE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Date: 1973-01-05
- Field: score
- Source value: `58-73`
- Canonical value: `56-73`
- Evidence: boise-state 1973-01-05: 56-73
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 14. DISCREPANCY-GONZAGA-1973-74-004-SITE_TYPE

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

### 15. DISCREPANCY-GONZAGA-1973-74-023-SCORE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Date: 1974-02-16
- Field: score
- Source value: `63-77`
- Canonical value: `63-75`
- Evidence: boise-state 1974-02-16: 63-75
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
- Source value: `date=1975-12-11; score=62-70`
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

### 23. DISCREPANCY-GONZAGA-1979-80-004-SCORE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1979-12-05
- Field: score
- Source value: `58-75`
- Canonical value: `48-75`
- Evidence: washington-state 1979-12-05: 48-75
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 24. DISCREPANCY-GONZAGA-1980-81-005-SITE_TYPE

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

### 25. DISCREPANCY-GONZAGA-1981-82-002-SITE_TYPE

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

### 26. DISCREPANCY-GONZAGA-1982-83-003-SCORE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1982-12-01
- Field: score
- Source value: `53-73`
- Canonical value: `53-75`
- Evidence: washington-state 1982-12-01: 53-75
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 27. DISCREPANCY-GONZAGA-1982-83-003-SITE_TYPE

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

### 28. DISCREPANCY-GONZAGA-1983-84-007-SITE_TYPE

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

### 29. DISCREPANCY-GONZAGA-1983-84-010-SCORE

- Category: discrepancy
- Matchup: gonzaga vs oregon
- Date: 1983-12-29
- Field: score
- Source value: `52-72`
- Canonical value: `53-72`
- Evidence: oregon 1983-12-29: 53-72
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 30. DISCREPANCY-GONZAGA-1985-86-004-SITE_TYPE

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

### 31. DISCREPANCY-GONZAGA-1985-86-009-SITE_TYPE

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

### 32. DISCREPANCY-GONZAGA-1989-90-006-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1989-12-09; canonical 1989-12-10
- Field: game_date
- Source value: `1989-12-09`
- Canonical value: `1989-12-10`
- Evidence: boise-state 1989-12-10: 1989-12-10
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 33. DISCREPANCY-GONZAGA-1991-92-003-SCORE

- Category: discrepancy
- Matchup: baylor vs gonzaga
- Date: 1991-11-29
- Field: score
- Source value: `75-77`
- Canonical value: `57-87`
- Evidence: baylor 1991-11-29: 57-87
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 34. DISCREPANCY-GONZAGA-1991-92-005-SITE_TYPE

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

### 35. IDENTITY-GONZAGA-1992-93-003

- Category: identity
- Matchup: gonzaga vs usc
- Dates: source 1992-12-07; canonical 1992-12-05
- Field: game_identity
- Source value: `date=1992-12-07; score=59-77`
- Canonical value: `CBBG-0069448`
- Evidence: CBBG-0069448 1992-1993 1992-12-05 59-77 sources=usc
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 36. CONDITIONAL-DISCREPANCY-GONZAGA-1992-93-003-CBBG-0069448-GAME_DATE

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

### 37. DISCREPANCY-GONZAGA-1998-99-001-GAME_DATE

- Category: discrepancy
- Matchup: gonzaga vs kansas
- Dates: source 1998-11-14; canonical 1998-11-13
- Field: game_date
- Source value: `1998-11-14`
- Canonical value: `1998-11-13`
- Evidence: kansas 1998-11-13: 1998-11-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 38. DISCREPANCY-GONZAGA-1998-99-005-SITE_TYPE

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

### 39. DISCREPANCY-GONZAGA-1998-99-009-SITE_TYPE

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

### 40. DISCREPANCY-GONZAGA-1998-99-014-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1999-01-02; canonical 1999-01-03
- Field: game_date
- Source value: `1999-01-02`
- Canonical value: `1999-01-03`
- Evidence: boise-state 1999-01-03: 1999-01-03
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 41. DISCREPANCY-GONZAGA-1998-99-014-SITE_TYPE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1999-01-02; canonical 1999-01-03
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: boise-state 1999-01-03: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 42. DISCREPANCY-GONZAGA-1999-00-003-SITE_TYPE

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

### 43. DISCREPANCY-GONZAGA-1999-00-008-SITE_TYPE

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

### 44. IDENTITY-GONZAGA-2003-04-004

- Category: identity
- Matchup: gonzaga vs georgia
- Dates: source 2003-11-24; canonical 2003-11-29
- Field: game_identity
- Source value: `date=2003-11-24; score=82-76`
- Canonical value: `CBBG-0042638`
- Evidence: CBBG-0042638 2003-2004 2003-11-29 76-82 sources=georgia
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 45. CONDITIONAL-DISCREPANCY-GONZAGA-2003-04-004-CBBG-0042638-GAME_DATE

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

### 46. CONDITIONAL-DISCREPANCY-GONZAGA-2003-04-004-CBBG-0042638-SITE_TYPE

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

### 47. DISCREPANCY-GONZAGA-2003-04-008-SITE_TYPE

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

### 48. DISCREPANCY-GONZAGA-2003-04-010-SCORE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 2003-12-28
- Field: score
- Source value: `95-58`
- Canonical value: `96-58`
- Evidence: washington-state 2003-12-28: 96-58
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 49. DISCREPANCY-GONZAGA-2005-06-008-SITE_TYPE

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

### 50. DISCREPANCY-GONZAGA-2006-07-003-SITE_TYPE

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

### 51. DISCREPANCY-GONZAGA-2006-07-009-SCORE

- Category: discrepancy
- Matchup: gonzaga vs texas
- Date: 2006-12-02
- Field: score
- Source value: `88-77`
- Canonical value: `87-77`
- Evidence: texas 2006-12-02: 87-77
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 52. DISCREPANCY-GONZAGA-2007-08-008-SITE_TYPE

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

### 53. DISCREPANCY-GONZAGA-2007-08-012-SITE_TYPE

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

### 54. DISCREPANCY-GONZAGA-2007-08-015-SITE_TYPE

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

### 55. DISCREPANCY-GONZAGA-2014-15-006-SITE_TYPE

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

### 56. DISCREPANCY-GONZAGA-2014-15-009-SCORE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 2014-12-10
- Field: score
- Source value: `81-66`
- Canonical value: `81-68`
- Evidence: washington-state 2014-12-10: 81-68
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 57. DISCREPANCY-GONZAGA-2014-15-009-SITE_TYPE

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

### 58. DISCREPANCY-GONZAGA-2016-17-009-SCORE

- Category: discrepancy
- Matchup: gonzaga vs washington
- Date: 2016-12-07
- Field: score
- Source value: `98-71`
- Canonical value: `86-71`
- Evidence: washington 2016-12-07: 86-71
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 59. DISCREPANCY-GONZAGA-2017-18-006-GAME_DATE

- Category: discrepancy
- Matchup: gonzaga vs texas
- Dates: source 2017-11-26; canonical 2017-11-25
- Field: game_date
- Source value: `2017-11-26`
- Canonical value: `2017-11-25`
- Evidence: texas 2017-11-25: 2017-11-25
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 60. DISCREPANCY-GONZAGA-2020-21-004-SITE_TYPE

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

### 61. DISCREPANCY-GONZAGA-2021-22-009-SITE_TYPE

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

### 62. DISCREPANCY-GONZAGA-2022-23-004-SITE_TYPE

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

### 63. DISCREPANCY-GONZAGA-2024-25-001-SITE_TYPE

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

### 64. DISCREPANCY-GONZAGA-2024-25-013-SCORE

- Category: discrepancy
- Matchup: gonzaga vs ucla
- Date: 2024-12-28
- Field: score
- Source value: `62-65`
- Canonical value: `71-73`
- Evidence: ucla 2024-12-28: 71-73
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 65. DISCREPANCY-GONZAGA-2025-26-002-SITE_TYPE

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

### 66. ACCOMPLISHMENTS-GONZAGA

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

### 67. PUBLICATION-GONZAGA

- Category: publication
- Matchup: gonzaga
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 2,053 in-scope source rows; 4 identity reviews; 52 definite and 9 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `PENDING`
- Basis: [required before approval]
