# vcu onboarding review

Generated: 2026-11-09T04:49:49.407063+00:00
Input fingerprint: `432db69d6d865bd52f85604e9b3182afacde0cce14fa12f32c075fb24171dcbc`

## Preflight summary

- Source rows: 1,650
- In-scope rows: 1,650
- Pre-cutoff researched rows: 0
- Existing matches: 489
- New canonical games: 1,152
- Identity reviews: 9
- Safe enrichment fields: 892
- Discrepancies: 28
- Conditional discrepancies: 37
- Canonical-only site reviews: 1
- Affected existing public programs: alabama, arizona-state, arkansas, auburn, baylor, boise-state, boston-college, butler, byu, california, cincinnati, colorado, colorado-state, davidson, dayton, duke, duquesne, fairleigh-dickinson, florida-state, fordham, george-mason, georgetown, georgia, georgia-tech, houston, illinois, indiana, iowa, iowa-state, kansas, kansas-state, la-salle, long-island-university, louisville, loyola-chicago, lsu, marquette, maryland, miami, michigan, michigan-state, mississippi-state, missouri, nc-state, north-carolina, northwestern, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, penn-state, pittsburgh, purdue, rhode-island, rutgers, saint-joseph-s, saint-louis, seton-hall, smu, st-bonaventure, st-john-s, syracuse, tcu, tennessee, texas, texas-a-m, ucf, ucla, uconn, usc, utah, utah-state, vanderbilt, villanova, virginia, virginia-tech, wagner, wake-forest, west-virginia, wisconsin, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. IDENTITY-VCU-1974-75-011

- Category: identity
- Matchup: vcu vs texas-a-m
- Dates: source 1974-12-29; canonical 1974-12-10;1974-12-30
- Field: game_identity
- Source value: `date=1974-12-29; score=80-84`
- Canonical value: `CBBG-0066492;CBBG-0066496`
- Evidence: CBBG-0066492 1974-1975 1974-12-10 98-84 sources=texas-a-m; CBBG-0066496 1974-1975 1974-12-30 84-70 sources=texas-a-m
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 2. CONDITIONAL-DISCREPANCY-VCU-1974-75-011-CBBG-0066492-GAME_DATE

- Category: conditional_discrepancy
- Matchup: texas-a-m vs vcu
- Dates: source 1974-12-29; canonical 1974-12-10
- Field: game_date
- Source value: `1974-12-29`
- Canonical value: `1974-12-10`
- Evidence: texas-a-m 1974-12-10: 1974-12-10
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0066492`

### 3. CONDITIONAL-DISCREPANCY-VCU-1974-75-011-CBBG-0066492-SCORE

- Category: conditional_discrepancy
- Matchup: texas-a-m vs vcu
- Dates: source 1974-12-29; canonical 1974-12-10
- Field: score
- Source value: `84-80`
- Canonical value: `98-84`
- Evidence: texas-a-m 1974-12-10: 98-84
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0066492`

### 4. CONDITIONAL-DISCREPANCY-VCU-1974-75-011-CBBG-0066492-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: texas-a-m vs vcu
- Dates: source 1974-12-29; canonical 1974-12-10
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: texas-a-m 1974-12-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0066492`

### 5. CONDITIONAL-DISCREPANCY-VCU-1974-75-011-CBBG-0066496-GAME_DATE

- Category: conditional_discrepancy
- Matchup: texas-a-m vs vcu
- Dates: source 1974-12-29; canonical 1974-12-30
- Field: game_date
- Source value: `1974-12-29`
- Canonical value: `1974-12-30`
- Evidence: texas-a-m 1974-12-30: 1974-12-30
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0066496`

### 6. CONDITIONAL-DISCREPANCY-VCU-1974-75-011-CBBG-0066496-SCORE

- Category: conditional_discrepancy
- Matchup: texas-a-m vs vcu
- Dates: source 1974-12-29; canonical 1974-12-30
- Field: score
- Source value: `84-80`
- Canonical value: `84-70`
- Evidence: texas-a-m 1974-12-30: 84-70
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0066496`

### 7. DISCREPANCY-VCU-1976-77-009-SITE_TYPE

- Category: discrepancy
- Matchup: vcu vs virginia
- Date: 1976-12-29
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia 1976-12-29: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 8. DISCREPANCY-VCU-1977-78-021-SITE_TYPE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Date: 1978-02-10
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1978-02-10: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 9. DISCREPANCY-VCU-1977-78-027-GAME_TYPE

- Category: discrepancy
- Matchup: georgetown vs vcu
- Date: 1978-03-01
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: georgetown 1978-03-01: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 10. DISCREPANCY-VCU-1979-80-008-SITE_TYPE

- Category: discrepancy
- Matchup: vcu vs virginia
- Date: 1979-12-28
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia 1979-12-28: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 11. IDENTITY-VCU-1984-85-032

- Category: identity
- Matchup: vcu vs alabama
- Dates: source 1985-03-17; canonical 1985-03-22
- Field: game_identity
- Source value: `date=1985-03-17; score=59-63`
- Canonical value: `CBBG-0028889`
- Evidence: CBBG-0028889 1984-1985 1985-03-22 63-59 sources=alabama
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 12. CONDITIONAL-DISCREPANCY-VCU-1984-85-032-CBBG-0028889-GAME_DATE

- Category: conditional_discrepancy
- Matchup: alabama vs vcu
- Dates: source 1985-03-17; canonical 1985-03-22
- Field: game_date
- Source value: `1985-03-17`
- Canonical value: `1985-03-22`
- Evidence: alabama 1985-03-22: 1985-03-22
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0028889`

### 13. DISCREPANCY-VCU-1985-86-005-SCORE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Date: 1985-12-14
- Field: score
- Source value: `65-67`
- Canonical value: `57-59`
- Evidence: virginia-tech 1985-12-14: 57-59
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 14. DISCREPANCY-VCU-1987-88-008-SITE_TYPE

- Category: discrepancy
- Matchup: vcu vs virginia
- Date: 1987-12-19
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia 1987-12-19: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 15. DISCREPANCY-VCU-1988-89-008-GAME_DATE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1988-12-30; canonical 1988-12-29
- Field: game_date
- Source value: `1988-12-30`
- Canonical value: `1988-12-29`
- Evidence: virginia-tech 1988-12-29: 1988-12-29
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 16. DISCREPANCY-VCU-1989-90-008-SITE_TYPE

- Category: discrepancy
- Matchup: vcu vs virginia
- Date: 1989-12-20
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia 1989-12-20: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 17. IDENTITY-VCU-1989-90-011

- Category: identity
- Matchup: vcu vs virginia-tech
- Dates: source 1990-01-08; canonical 1990-01-06
- Field: game_identity
- Source value: `date=1990-01-08; score=68-71`
- Canonical value: `CBBG-0136691`
- Evidence: CBBG-0136691 1989-1990 1990-01-06 68-71 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 18. CONDITIONAL-DISCREPANCY-VCU-1989-90-011-CBBG-0136691-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1990-01-08; canonical 1990-01-06
- Field: game_date
- Source value: `1990-01-08`
- Canonical value: `1990-01-06`
- Evidence: virginia-tech 1990-01-06: 1990-01-06
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136691`

### 19. IDENTITY-VCU-1990-91-006

- Category: identity
- Matchup: vcu vs virginia-tech
- Dates: source 1990-12-11; canonical 1990-12-08
- Field: game_identity
- Source value: `date=1990-12-11; score=75-77`
- Canonical value: `CBBG-0136707`
- Evidence: CBBG-0136707 1990-1991 1990-12-08 75-77 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 20. CONDITIONAL-DISCREPANCY-VCU-1990-91-006-CBBG-0136707-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1990-12-11; canonical 1990-12-08
- Field: game_date
- Source value: `1990-12-11`
- Canonical value: `1990-12-08`
- Evidence: virginia-tech 1990-12-08: 1990-12-08
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136707`

### 21. DISCREPANCY-VCU-1991-92-006-GAME_DATE

- Category: discrepancy
- Matchup: george-mason vs vcu
- Dates: source 1991-12-11; canonical 1991-12-12
- Field: game_date
- Source value: `1991-12-11`
- Canonical value: `1991-12-12`
- Evidence: george-mason 1991-12-12: 1991-12-12
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 22. IDENTITY-VCU-1991-92-022

- Category: identity
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-01-11;1992-02-15
- Field: game_identity
- Source value: `date=1992-02-20; score=63-60`
- Canonical value: `CBBG-0136728;CBBG-0136737`
- Evidence: CBBG-0136728 1991-1992 1992-01-11 72-73 sources=virginia-tech; CBBG-0136737 1991-1992 1992-02-15 63-60 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 23. CONDITIONAL-DISCREPANCY-VCU-1991-92-022-CBBG-0136728-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-01-11
- Field: game_date
- Source value: `1992-02-20`
- Canonical value: `1992-01-11`
- Evidence: virginia-tech 1992-01-11: 1992-01-11
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136728`

### 24. CONDITIONAL-DISCREPANCY-VCU-1991-92-022-CBBG-0136728-SCORE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-01-11
- Field: score
- Source value: `63-60`
- Canonical value: `72-73`
- Evidence: virginia-tech 1992-01-11: 72-73
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136728`

### 25. CONDITIONAL-DISCREPANCY-VCU-1991-92-022-CBBG-0136728-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-01-11
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: virginia-tech 1992-01-11: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136728`

### 26. CONDITIONAL-DISCREPANCY-VCU-1991-92-022-CBBG-0136728-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-01-11
- Field: result_winner_team_key
- Source value: `vcu`
- Canonical value: `virginia-tech`
- Evidence: virginia-tech 1992-01-11: virginia-tech
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136728`

### 27. CONDITIONAL-DISCREPANCY-VCU-1991-92-022-CBBG-0136737-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-02-15
- Field: game_date
- Source value: `1992-02-20`
- Canonical value: `1992-02-15`
- Evidence: virginia-tech 1992-02-15: 1992-02-15
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136737`

### 28. IDENTITY-VCU-1992-93-018

- Category: identity
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-02-03;1993-02-20;1993-03-13
- Field: game_identity
- Source value: `date=1993-02-06; score=73-54`
- Canonical value: `CBBG-0136758;CBBG-0136763;CBBG-0136768`
- Evidence: CBBG-0136758 1992-1993 1993-02-03 73-54 sources=virginia-tech; CBBG-0136763 1992-1993 1993-02-20 86-69 sources=virginia-tech; CBBG-0136768 1992-1993 1993-03-13 85-71 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 29. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136758-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-02-03
- Field: game_date
- Source value: `1993-02-06`
- Canonical value: `1993-02-03`
- Evidence: virginia-tech 1993-02-03: 1993-02-03
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136758`

### 30. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136763-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-02-20
- Field: game_date
- Source value: `1993-02-06`
- Canonical value: `1993-02-20`
- Evidence: virginia-tech 1993-02-20: 1993-02-20
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136763`

### 31. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136763-SCORE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-02-20
- Field: score
- Source value: `73-54`
- Canonical value: `86-69`
- Evidence: virginia-tech 1993-02-20: 86-69
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136763`

### 32. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136763-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-02-20
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: virginia-tech 1993-02-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136763`

### 33. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136768-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-03-13
- Field: game_date
- Source value: `1993-02-06`
- Canonical value: `1993-03-13`
- Evidence: virginia-tech 1993-03-13: 1993-03-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 34. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136768-SCORE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-03-13
- Field: score
- Source value: `73-54`
- Canonical value: `85-71`
- Evidence: virginia-tech 1993-03-13: 85-71
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 35. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136768-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-03-13
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1993-03-13: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 36. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136768-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-03-13
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: virginia-tech 1993-03-13: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 37. IDENTITY-VCU-1992-93-023

- Category: identity
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-02-03;1993-02-20;1993-03-13
- Field: game_identity
- Source value: `date=1993-02-22; score=86-69`
- Canonical value: `CBBG-0136758;CBBG-0136763;CBBG-0136768`
- Evidence: CBBG-0136758 1992-1993 1993-02-03 73-54 sources=virginia-tech; CBBG-0136763 1992-1993 1993-02-20 86-69 sources=virginia-tech; CBBG-0136768 1992-1993 1993-03-13 85-71 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 38. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136758-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-02-03
- Field: game_date
- Source value: `1993-02-22`
- Canonical value: `1993-02-03`
- Evidence: virginia-tech 1993-02-03: 1993-02-03
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136758`

### 39. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136758-SCORE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-02-03
- Field: score
- Source value: `86-69`
- Canonical value: `73-54`
- Evidence: virginia-tech 1993-02-03: 73-54
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136758`

### 40. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136758-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-02-03
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: virginia-tech 1993-02-03: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136758`

### 41. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136763-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-02-20
- Field: game_date
- Source value: `1993-02-22`
- Canonical value: `1993-02-20`
- Evidence: virginia-tech 1993-02-20: 1993-02-20
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136763`

### 42. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136768-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-03-13
- Field: game_date
- Source value: `1993-02-22`
- Canonical value: `1993-03-13`
- Evidence: virginia-tech 1993-03-13: 1993-03-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 43. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136768-SCORE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-03-13
- Field: score
- Source value: `86-69`
- Canonical value: `85-71`
- Evidence: virginia-tech 1993-03-13: 85-71
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 44. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136768-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-03-13
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1993-03-13: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 45. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136768-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-03-13
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: virginia-tech 1993-03-13: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 46. DISCREPANCY-VCU-1993-94-022-SCORE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Date: 1994-02-17
- Field: score
- Source value: `59-76`
- Canonical value: `59-75`
- Evidence: virginia-tech 1994-02-17: 59-75
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 47. IDENTITY-VCU-1994-95-029

- Category: identity
- Matchup: vcu vs louisville
- Dates: source 1995-03-05; canonical 1995-01-05;1995-03-02;1995-03-10
- Field: game_identity
- Source value: `date=1995-03-05; score=64-80`
- Canonical value: `CBBG-0144854;CBBG-0144868;CBBG-0144869`
- Evidence: CBBG-0144854 1994-1995 1995-01-05 63-67 sources=louisville; CBBG-0144868 1994-1995 1995-03-02 80-64 sources=louisville; CBBG-0144869 1994-1995 1995-03-10 84-61 sources=louisville
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 48. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144854-GAME_DATE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-01-05
- Field: game_date
- Source value: `1995-03-05`
- Canonical value: `1995-01-05`
- Evidence: louisville 1995-01-05: 1995-01-05
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144854`

### 49. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144854-SCORE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-01-05
- Field: score
- Source value: `80-64`
- Canonical value: `63-67`
- Evidence: louisville 1995-01-05: 63-67
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144854`

### 50. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144854-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-01-05
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: louisville 1995-01-05: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144854`

### 51. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144854-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-01-05
- Field: result_winner_team_key
- Source value: `louisville`
- Canonical value: `vcu`
- Evidence: louisville 1995-01-05: vcu
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144854`

### 52. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144868-GAME_DATE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-03-02
- Field: game_date
- Source value: `1995-03-05`
- Canonical value: `1995-03-02`
- Evidence: louisville 1995-03-02: 1995-03-02
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144868`

### 53. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144869-GAME_DATE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-03-10
- Field: game_date
- Source value: `1995-03-05`
- Canonical value: `1995-03-10`
- Evidence: louisville 1995-03-10: 1995-03-10
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144869`

### 54. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144869-SCORE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-03-10
- Field: score
- Source value: `80-64`
- Canonical value: `84-61`
- Evidence: louisville 1995-03-10: 84-61
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144869`

### 55. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144869-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-03-10
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: louisville 1995-03-10: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144869`

### 56. DISCREPANCY-VCU-1996-97-008-SITE_TYPE

- Category: discrepancy
- Matchup: tcu vs vcu
- Date: 1996-12-27
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: tcu 1996-12-27: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 57. DISCREPANCY-VCU-2000-01-006-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: texas-a-m vs vcu
- Date: 2000-12-02
- Field: overtime_periods
- Source value: `2`
- Canonical value: `1`
- Evidence: texas-a-m 2000-12-02: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 58. DISCREPANCY-VCU-2004-05-002-GAME_DATE

- Category: discrepancy
- Matchup: vcu vs wake-forest
- Dates: source 2004-11-18; canonical 2004-11-19
- Field: game_date
- Source value: `2004-11-18`
- Canonical value: `2004-11-19`
- Evidence: wake-forest 2004-11-19: 2004-11-19
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 59. DISCREPANCY-VCU-2009-10-023-SITE_TYPE

- Category: discrepancy
- Matchup: george-mason vs vcu
- Date: 2010-02-09
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: george-mason 2010-02-09: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 60. DISCREPANCY-VCU-2010-11-003-SCORE

- Category: discrepancy
- Matchup: vcu vs wake-forest
- Date: 2010-11-16
- Field: score
- Source value: `90-69`
- Canonical value: `80-69`
- Evidence: wake-forest 2010-11-16: 80-69
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 61. DISCREPANCY-VCU-2011-12-006-SITE_TYPE

- Category: discrepancy
- Matchup: alabama vs vcu
- Date: 2011-11-27
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: alabama 2011-11-27: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 62. DISCREPANCY-VCU-2012-13-006-SCORE

- Category: discrepancy
- Matchup: missouri vs vcu
- Date: 2012-11-24
- Field: score
- Source value: `65-58`
- Canonical value: `68-65`
- Evidence: missouri 2012-11-24: 68-65
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 63. DISCREPANCY-VCU-2012-13-006-SITE_TYPE

- Category: discrepancy
- Matchup: missouri vs vcu
- Date: 2012-11-24
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: missouri 2012-11-24: UNKNOWN
- Recommended: `LEAVE_UNRESOLVED`
- Decision: `PENDING`
- Basis: [required before approval]

### 64. DISCREPANCY-VCU-2013-14-034-SCORE

- Category: discrepancy
- Matchup: saint-joseph-s vs vcu
- Date: 2014-03-16
- Field: score
- Source value: `65-61`
- Canonical value: `64-61`
- Evidence: saint-joseph-s 2014-03-16: 64-61
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 65. DISCREPANCY-VCU-2014-15-031-SCORE

- Category: discrepancy
- Matchup: george-mason vs vcu
- Date: 2015-03-07
- Field: score
- Source value: `60-71`
- Canonical value: `51-67`
- Evidence: george-mason 2015-03-07: 51-67
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 66. DISCREPANCY-VCU-2016-17-023-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: st-bonaventure vs vcu
- Date: 2017-02-04
- Field: overtime_periods
- Source value: `1`
- Canonical value: `0`
- Evidence: st-bonaventure 2017-02-04: 0
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 67. DISCREPANCY-VCU-2019-20-014-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs vcu
- Date: 2020-01-02
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: fordham 2020-01-02: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 68. DISCREPANCY-VCU-2019-20-022-SCORE

- Category: discrepancy
- Matchup: rhode-island vs vcu
- Date: 2020-01-31
- Field: score
- Source value: `87-75`
- Canonical value: `81-75`
- Evidence: rhode-island 2020-01-31: 81-75
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 69. IDENTITY-VCU-2020-21-011

- Category: identity
- Matchup: vcu vs george-washington
- Date: 2021-01-06
- Field: game_identity
- Source value: `date=2021-01-06; score=66-61`
- Canonical value: `CBBG-0203017`
- Evidence: CBBG-0203017 2020-2021 2021-01-06 61-66 sources=george-mason
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 70. DISCREPANCY-VCU-2020-21-025-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs vcu
- Date: 2021-03-06
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: davidson 2021-03-06: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 71. DISCREPANCY-VCU-2022-23-033-GAME_DATE

- Category: discrepancy
- Matchup: saint-louis vs vcu
- Dates: source 2023-03-10; canonical 2023-03-11
- Field: game_date
- Source value: `2023-03-10`
- Canonical value: `2023-03-11`
- Evidence: saint-louis 2023-03-11: 2023-03-11
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 72. DISCREPANCY-VCU-2022-23-034-GAME_DATE

- Category: discrepancy
- Matchup: dayton vs vcu
- Dates: source 2023-03-11; canonical 2023-03-12
- Field: game_date
- Source value: `2023-03-11`
- Canonical value: `2023-03-12`
- Evidence: dayton 2023-03-12: 2023-03-12
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 73. DISCREPANCY-VCU-2023-24-005-GAME_DATE

- Category: discrepancy
- Matchup: iowa-state vs vcu
- Dates: source 2023-11-24; canonical 2023-11-23
- Field: game_date
- Source value: `2023-11-24`
- Canonical value: `2023-11-23`
- Evidence: iowa-state 2023-11-23: 2023-11-23
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 74. DISCREPANCY-VCU-2023-24-006-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs vcu
- Dates: source 2023-11-25; canonical 2023-11-24
- Field: game_date
- Source value: `2023-11-25`
- Canonical value: `2023-11-24`
- Evidence: boise-state 2023-11-24: 2023-11-24
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 75. CANONICAL-SITE-PATCH-CBBG-0066496

- Category: canonical_site_patch
- Matchup: texas-a-m vs vcu
- Dates: source [unknown]; canonical 1974-12-30
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_B_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from texas-a-m; documented target HOME chronology yields 2 candidate physical venue(s): Franklin Street Gym, Richmond Coliseum. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 76. POSTSEASON-CLASSIFICATION-VCU-1977-78-027

- Category: postseason_classification
- Matchup: vcu vs georgetown
- Date: 1978-03-01
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 1 ^at Georgetown W 88-75
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 77. POSTSEASON-CLASSIFICATION-VCU-1977-78-028

- Category: postseason_classification
- Matchup: vcu vs st-bonaventure
- Date: 1978-03-04
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 4 &vs. St. Bonaventure (:03) L 61-63
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 78. POSTSEASON-CLASSIFICATION-VCU-2009-10-032

- Category: postseason_classification
- Matchup: vcu vs george-washington
- Dates: source 2010-03-16; canonical [unknown]
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: ``
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 16 %at George Washington W 79-73
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 79. POSTSEASON-CLASSIFICATION-VCU-2009-10-033

- Category: postseason_classification
- Matchup: vcu vs charleston
- Dates: source 2010-03-22; canonical [unknown]
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: ``
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 22 %CHARLESTON W 93-86
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 80. POSTSEASON-CLASSIFICATION-VCU-2009-10-034

- Category: postseason_classification
- Matchup: vcu vs boston-university
- Dates: source 2010-03-24; canonical [unknown]
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: ``
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 24 %BOSTON UNIVERSITY W 88-75
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 81. POSTSEASON-CLASSIFICATION-VCU-2009-10-035

- Category: postseason_classification
- Matchup: vcu vs saint-louis
- Date: 2010-03-29
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 29 %SAINT LOUIS W 68-56
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 82. POSTSEASON-CLASSIFICATION-VCU-2009-10-036

- Category: postseason_classification
- Matchup: vcu vs saint-louis
- Date: 2010-03-31
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 31 %at Saint Louis W 71-65
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 83. ACCOMPLISHMENTS-VCU

- Category: accomplishments
- Matchup: vcu
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"FINAL_FOUR","best_finish_year":"2011","conference_regular_season_championships":"14","conference_tournament_championships":"12","final_four_appearances":"1","national_championships":"0","ncaa_tournament_appearances":"21"}`
- Canonical value: `{"best_finish_key":"FINAL_FOUR","best_finish_year":2011,"final_four_appearances":1,"national_championships":0,"ncaa_tournament_appearances":20}`
- Evidence: Projected NCAA totals depend on explicit owner-reviewed classification and round decisions for generic postseason source games; the normal sealed disposable rehearsal must establish exact canonical accomplishment equality before publication or VERIFIED status.
- Recommended: `KEEP_UNDER_REVIEW`
- Decision: `PENDING`
- Basis: [required before approval]

### 84. PUBLICATION-VCU

- Category: publication
- Matchup: vcu
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 1,650 in-scope source rows; 9 identity reviews; 28 definite and 37 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `PENDING`
- Basis: [required before approval]
