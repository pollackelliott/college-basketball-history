# loyola-chicago onboarding review

Generated: 2026-11-01T03:40:09.655490+00:00
Input fingerprint: `ec15d0a1742e60094dded7dba72864a617466329ce33d95c526433b29c74782f`

## Preflight summary

- Source rows: 2,727
- In-scope rows: 2,727
- Pre-cutoff researched rows: 0
- Existing matches: 706
- New canonical games: 1,995
- Identity reviews: 26
- Safe enrichment fields: 1,070
- Discrepancies: 186
- Conditional discrepancies: 86
- Canonical-only site reviews: 15
- Affected existing public programs: arizona, arizona-state, arkansas, auburn, boise-state, boston-college, butler, byu, california, chicago-state, cincinnati, clemson, colorado, colorado-state, creighton, depaul, duke, fairleigh-dickinson, florida, georgetown, georgia, georgia-tech, houston, illinois, indiana, iowa, iowa-state, kansas, kansas-state, kentucky, le-moyne, long-island-university, louisville, lsu, marquette, maryland, mercyhurst, miami, michigan, michigan-state, minnesota, mississippi-state, missouri, nc-state, nebraska, north-carolina, northwestern, notre-dame, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, providence, purdue, rutgers, saint-louis, san-diego-state, seton-hall, smu, south-carolina, st-john-s, stanford, syracuse, tcu, tennessee, texas-a-m, texas-tech, ucla, usc, utah, vanderbilt, villanova, virginia, washington-state, wisconsin, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. DISCREPANCY-LOY-STG1-00045-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1922-01-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1922-01-06: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 2. DISCREPANCY-LOY-STG1-00065-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs notre-dame
- Date: 1924-01-16
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: notre-dame 1924-01-16: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 3. DISCREPANCY-LOY-STG1-00083-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1925-01-17
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1925-01-17: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 4. DISCREPANCY-LOY-STG1-00086-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1925-02-07
- Field: score
- Source value: `17-19`
- Canonical value: `17-18`
- Evidence: marquette 1925-02-07: 17-18
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 5. DISCREPANCY-LOY-STG1-00086-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1925-02-07
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1925-02-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 6. IDENTITY-LOY-STG1-00092

- Category: identity
- Matchup: loyola-chicago vs marquette
- Dates: source 1925-02-15; canonical 1925-02-07;1925-02-28
- Field: game_identity
- Source value: `date=1925-02-15; score=6-26`
- Canonical value: `CBBG-0150721;CBBG-0150726`
- Evidence: CBBG-0150721 1924-1925 1925-02-07 17-18 sources=marquette; CBBG-0150726 1924-1925 1925-02-28 20-31 sources=marquette
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 7. CONDITIONAL-DISCREPANCY-LOY-STG1-00092-CBBG-0150721-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1925-02-15; canonical 1925-02-07
- Field: game_date
- Source value: `1925-02-15`
- Canonical value: `1925-02-07`
- Evidence: marquette 1925-02-07: 1925-02-07
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150721`

### 8. CONDITIONAL-DISCREPANCY-LOY-STG1-00092-CBBG-0150721-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1925-02-15; canonical 1925-02-07
- Field: score
- Source value: `6-26`
- Canonical value: `17-18`
- Evidence: marquette 1925-02-07: 17-18
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150721`

### 9. CONDITIONAL-DISCREPANCY-LOY-STG1-00092-CBBG-0150721-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1925-02-15; canonical 1925-02-07
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1925-02-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150721`

### 10. CONDITIONAL-DISCREPANCY-LOY-STG1-00092-CBBG-0150726-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1925-02-15; canonical 1925-02-28
- Field: game_date
- Source value: `1925-02-15`
- Canonical value: `1925-02-28`
- Evidence: marquette 1925-02-28: 1925-02-28
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150726`

### 11. CONDITIONAL-DISCREPANCY-LOY-STG1-00092-CBBG-0150726-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1925-02-15; canonical 1925-02-28
- Field: score
- Source value: `6-26`
- Canonical value: `20-31`
- Evidence: marquette 1925-02-28: 20-31
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150726`

### 12. CONDITIONAL-DISCREPANCY-LOY-STG1-00092-CBBG-0150726-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1925-02-15; canonical 1925-02-28
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: marquette 1925-02-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150726`

### 13. IDENTITY-LOY-STG1-00100

- Category: identity
- Matchup: loyola-chicago vs marquette
- Dates: source 1926-01-13; canonical 1926-02-13;1926-02-18
- Field: game_identity
- Source value: `date=1926-01-13; score=26-16`
- Canonical value: `CBBG-0150735;CBBG-0150736`
- Evidence: CBBG-0150735 1925-1926 1926-02-13 26-16 sources=marquette; CBBG-0150736 1925-1926 1926-02-18 18-19 sources=marquette
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 14. CONDITIONAL-DISCREPANCY-LOY-STG1-00100-CBBG-0150735-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1926-01-13; canonical 1926-02-13
- Field: game_date
- Source value: `1926-01-13`
- Canonical value: `1926-02-13`
- Evidence: marquette 1926-02-13: 1926-02-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150735`

### 15. CONDITIONAL-DISCREPANCY-LOY-STG1-00100-CBBG-0150735-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1926-01-13; canonical 1926-02-13
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1926-02-13: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150735`

### 16. CONDITIONAL-DISCREPANCY-LOY-STG1-00100-CBBG-0150736-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1926-01-13; canonical 1926-02-18
- Field: game_date
- Source value: `1926-01-13`
- Canonical value: `1926-02-18`
- Evidence: marquette 1926-02-18: 1926-02-18
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150736`

### 17. CONDITIONAL-DISCREPANCY-LOY-STG1-00100-CBBG-0150736-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1926-01-13; canonical 1926-02-18
- Field: score
- Source value: `26-16`
- Canonical value: `18-19`
- Evidence: marquette 1926-02-18: 18-19
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150736`

### 18. CONDITIONAL-DISCREPANCY-LOY-STG1-00100-CBBG-0150736-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1926-01-13; canonical 1926-02-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: marquette 1926-02-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150736`

### 19. CONDITIONAL-DISCREPANCY-LOY-STG1-00100-CBBG-0150736-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1926-01-13; canonical 1926-02-18
- Field: result_winner_team_key
- Source value: `loyola-chicago`
- Canonical value: `marquette`
- Evidence: marquette 1926-02-18: marquette
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150736`

### 20. IDENTITY-LOY-STG1-00103

- Category: identity
- Matchup: loyola-chicago vs creighton
- Dates: source 1926-01-22; canonical 1926-01-21
- Field: game_identity
- Source value: `date=1926-01-22; score=22-21`
- Canonical value: `CBBG-0148467`
- Evidence: CBBG-0148467 1925-1926 1926-01-21 20-21 sources=creighton
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 21. CONDITIONAL-DISCREPANCY-LOY-STG1-00103-CBBG-0148467-GAME_DATE

- Category: conditional_discrepancy
- Matchup: creighton vs loyola-chicago
- Dates: source 1926-01-22; canonical 1926-01-21
- Field: game_date
- Source value: `1926-01-22`
- Canonical value: `1926-01-21`
- Evidence: creighton 1926-01-21: 1926-01-21
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0148467`

### 22. CONDITIONAL-DISCREPANCY-LOY-STG1-00103-CBBG-0148467-SCORE

- Category: conditional_discrepancy
- Matchup: creighton vs loyola-chicago
- Dates: source 1926-01-22; canonical 1926-01-21
- Field: score
- Source value: `21-22`
- Canonical value: `20-21`
- Evidence: creighton 1926-01-21: 20-21
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0148467`

### 23. CONDITIONAL-DISCREPANCY-LOY-STG1-00103-CBBG-0148467-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: creighton vs loyola-chicago
- Dates: source 1926-01-22; canonical 1926-01-21
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: creighton 1926-01-21: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0148467`

### 24. DISCREPANCY-LOY-STG1-00106-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1926-02-04
- Field: score
- Source value: `17-30`
- Canonical value: `16-30`
- Evidence: saint-louis 1926-02-04: 16-30
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 25. DISCREPANCY-LOY-STG1-00106-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1926-02-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1926-02-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 26. DISCREPANCY-LOY-STG1-00110-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1926-02-20
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1926-02-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 27. DISCREPANCY-LOY-STG1-00126-GAME_DATE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source 1927-02-10; canonical 1927-02-11
- Field: game_date
- Source value: `1927-02-10`
- Canonical value: `1927-02-11`
- Evidence: saint-louis 1927-02-11: 1927-02-11
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 28. DISCREPANCY-LOY-STG1-00126-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source 1927-02-10; canonical 1927-02-11
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1927-02-11: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 29. DISCREPANCY-LOY-STG1-00128-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs xavier
- Date: 1927-02-15
- Field: score
- Source value: `24-17`
- Canonical value: `17-13`
- Evidence: xavier 1927-02-15: 17-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 30. DISCREPANCY-LOY-STG1-00128-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs xavier
- Date: 1927-02-15
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1927-02-15: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 31. DISCREPANCY-LOY-STG1-00132-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1927-03-05
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1927-03-05: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 32. IDENTITY-LOY-STG1-00135

- Category: identity
- Matchup: loyola-chicago vs oregon-state
- Dates: source 1927-12-31; canonical [unknown]
- Field: game_identity
- Source value: `date=1927-12-31; score=31-19`
- Canonical value: `CBBG-0117714`
- Evidence: CBBG-0117714 1927-1928 [unknown] 29-19 sources=oregon-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 33. CONDITIONAL-DISCREPANCY-LOY-STG1-00135-CBBG-0117714-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs oregon-state
- Dates: source 1927-12-31; canonical [unknown]
- Field: score
- Source value: `31-19`
- Canonical value: `29-19`
- Evidence: oregon-state [unknown]: 29-19
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0117714`

### 34. CONDITIONAL-DISCREPANCY-LOY-STG1-00135-CBBG-0117714-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs oregon-state
- Dates: source 1927-12-31; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: oregon-state [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0117714`

### 35. IDENTITY-LOY-STG1-00137

- Category: identity
- Matchup: loyola-chicago vs marquette
- Dates: source 1928-01-09; canonical 1927-12-21;1928-01-13
- Field: game_identity
- Source value: `date=1928-01-09; score=27-12`
- Canonical value: `CBBG-0150744;CBBG-0150746`
- Evidence: CBBG-0150744 1927-1928 1927-12-21 20-9 sources=marquette; CBBG-0150746 1927-1928 1928-01-13 27-12 sources=marquette
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 36. CONDITIONAL-DISCREPANCY-LOY-STG1-00137-CBBG-0150744-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1928-01-09; canonical 1927-12-21
- Field: game_date
- Source value: `1928-01-09`
- Canonical value: `1927-12-21`
- Evidence: marquette 1927-12-21: 1927-12-21
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150744`

### 37. CONDITIONAL-DISCREPANCY-LOY-STG1-00137-CBBG-0150744-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1928-01-09; canonical 1927-12-21
- Field: score
- Source value: `27-12`
- Canonical value: `20-9`
- Evidence: marquette 1927-12-21: 20-9
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150744`

### 38. CONDITIONAL-DISCREPANCY-LOY-STG1-00137-CBBG-0150744-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1928-01-09; canonical 1927-12-21
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: marquette 1927-12-21: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150744`

### 39. CONDITIONAL-DISCREPANCY-LOY-STG1-00137-CBBG-0150746-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1928-01-09; canonical 1928-01-13
- Field: game_date
- Source value: `1928-01-09`
- Canonical value: `1928-01-13`
- Evidence: marquette 1928-01-13: 1928-01-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150746`

### 40. CONDITIONAL-DISCREPANCY-LOY-STG1-00137-CBBG-0150746-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source 1928-01-09; canonical 1928-01-13
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1928-01-13: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0150746`

### 41. DISCREPANCY-LOY-STG1-00138-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1928-01-14
- Field: score
- Source value: `26-21`
- Canonical value: `27-21`
- Evidence: saint-louis 1928-01-14: 27-21
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 42. DISCREPANCY-LOY-STG1-00138-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1928-01-14
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1928-01-14: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 43. DISCREPANCY-LOY-STG1-00144-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1928-02-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1928-02-04: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 44. IDENTITY-LOY-STG1-00151

- Category: identity
- Matchup: loyola-chicago vs xavier
- Dates: source 1928-02-29; canonical 1928-02-15;1928-02-25
- Field: game_identity
- Source value: `date=1928-02-29; score=40-19`
- Canonical value: `CBBG-0152416;CBBG-0152420`
- Evidence: CBBG-0152416 1927-1928 1928-02-15 11-14 sources=xavier; CBBG-0152420 1927-1928 1928-02-25 40-19 sources=xavier
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 45. CONDITIONAL-DISCREPANCY-LOY-STG1-00151-CBBG-0152416-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source 1928-02-29; canonical 1928-02-15
- Field: game_date
- Source value: `1928-02-29`
- Canonical value: `1928-02-15`
- Evidence: xavier 1928-02-15: 1928-02-15
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0152416`

### 46. CONDITIONAL-DISCREPANCY-LOY-STG1-00151-CBBG-0152416-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source 1928-02-29; canonical 1928-02-15
- Field: score
- Source value: `40-19`
- Canonical value: `11-14`
- Evidence: xavier 1928-02-15: 11-14
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0152416`

### 47. CONDITIONAL-DISCREPANCY-LOY-STG1-00151-CBBG-0152416-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source 1928-02-29; canonical 1928-02-15
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: xavier 1928-02-15: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0152416`

### 48. CONDITIONAL-DISCREPANCY-LOY-STG1-00151-CBBG-0152416-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source 1928-02-29; canonical 1928-02-15
- Field: result_winner_team_key
- Source value: `loyola-chicago`
- Canonical value: `xavier`
- Evidence: xavier 1928-02-15: xavier
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0152416`

### 49. CONDITIONAL-DISCREPANCY-LOY-STG1-00151-CBBG-0152420-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source 1928-02-29; canonical 1928-02-25
- Field: game_date
- Source value: `1928-02-29`
- Canonical value: `1928-02-25`
- Evidence: xavier 1928-02-25: 1928-02-25
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0152420`

### 50. CONDITIONAL-DISCREPANCY-LOY-STG1-00151-CBBG-0152420-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source 1928-02-29; canonical 1928-02-25
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1928-02-25: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0152420`

### 51. DISCREPANCY-LOY-STG1-00154-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1928-12-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1928-12-30: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 52. IDENTITY-LOY-STG1-00160

- Category: identity
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1928-12-30;1929-01-30
- Field: game_identity
- Source value: `date=[unknown]; score=21-20`
- Canonical value: `CBBG-0182888;CBBG-0182891`
- Evidence: CBBG-0182888 1928-1929 1928-12-30 28-26 sources=saint-louis; CBBG-0182891 1928-1929 1929-01-30 21-19 sources=saint-louis
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 53. CONDITIONAL-DISCREPANCY-LOY-STG1-00160-CBBG-0182888-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1928-12-30
- Field: score
- Source value: `21-20`
- Canonical value: `28-26`
- Evidence: saint-louis 1928-12-30: 28-26
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0182888`

### 54. CONDITIONAL-DISCREPANCY-LOY-STG1-00160-CBBG-0182888-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1928-12-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1928-12-30: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0182888`

### 55. CONDITIONAL-DISCREPANCY-LOY-STG1-00160-CBBG-0182891-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1929-01-30
- Field: score
- Source value: `21-20`
- Canonical value: `21-19`
- Evidence: saint-louis 1929-01-30: 21-19
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0182891`

### 56. CONDITIONAL-DISCREPANCY-LOY-STG1-00160-CBBG-0182891-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1929-01-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1929-01-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0182891`

### 57. IDENTITY-LOY-STG1-00176

- Category: identity
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1930-01-14;1930-01-23
- Field: game_identity
- Source value: `date=[unknown]; score=18-13`
- Canonical value: `CBBG-0152440;CBBG-0152443`
- Evidence: CBBG-0152440 1929-1930 1930-01-14 18-13 sources=xavier; CBBG-0152443 1929-1930 1930-01-23 18-13 sources=xavier
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 58. CONDITIONAL-DISCREPANCY-LOY-STG1-00176-CBBG-0152440-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1930-01-14
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1930-01-14: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0152440`

### 59. CONDITIONAL-DISCREPANCY-LOY-STG1-00176-CBBG-0152443-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1930-01-23
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: xavier 1930-01-23: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0152443`

### 60. DISCREPANCY-LOY-STG1-00178-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs purdue
- Dates: source [unknown]; canonical 1930-01-30
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: purdue 1930-01-30: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 61. IDENTITY-LOY-STG1-00180

- Category: identity
- Matchup: loyola-chicago vs georgetown
- Dates: source [unknown]; canonical 1930-02-11
- Field: game_identity
- Source value: `date=[unknown]; score=25-34`
- Canonical value: `CBBG-0163996`
- Evidence: CBBG-0163996 1929-1930 1930-02-11 34-23 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 62. CONDITIONAL-DISCREPANCY-LOY-STG1-00180-CBBG-0163996-SCORE

- Category: conditional_discrepancy
- Matchup: georgetown vs loyola-chicago
- Dates: source [unknown]; canonical 1930-02-11
- Field: score
- Source value: `34-25`
- Canonical value: `34-23`
- Evidence: georgetown 1930-02-11: 34-23
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163996`

### 63. CONDITIONAL-DISCREPANCY-LOY-STG1-00180-CBBG-0163996-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: georgetown vs loyola-chicago
- Dates: source [unknown]; canonical 1930-02-11
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: georgetown 1930-02-11: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163996`

### 64. IDENTITY-LOY-STG1-00182

- Category: identity
- Matchup: loyola-chicago vs north-carolina
- Dates: source [unknown]; canonical 1930-02-12
- Field: game_identity
- Source value: `date=[unknown]; score=26-25`
- Canonical value: `CBBG-0094957`
- Evidence: CBBG-0094957 1929-1930 1930-02-12 25-24 sources=north-carolina
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 65. CONDITIONAL-DISCREPANCY-LOY-STG1-00182-CBBG-0094957-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs north-carolina
- Dates: source [unknown]; canonical 1930-02-12
- Field: score
- Source value: `26-25`
- Canonical value: `25-24`
- Evidence: north-carolina 1930-02-12: 25-24
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0094957`

### 66. CONDITIONAL-DISCREPANCY-LOY-STG1-00182-CBBG-0094957-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs north-carolina
- Dates: source [unknown]; canonical 1930-02-12
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: north-carolina 1930-02-12: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0094957`

### 67. IDENTITY-LOY-STG1-00186

- Category: identity
- Matchup: loyola-chicago vs michigan-state
- Dates: source [unknown]; canonical 1931-02-14
- Field: game_identity
- Source value: `date=[unknown]; score=21-26`
- Canonical value: `CBBG-0047466`
- Evidence: CBBG-0047466 1930-1931 1931-02-14 16-24 sources=michigan-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 68. CONDITIONAL-DISCREPANCY-LOY-STG1-00186-CBBG-0047466-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs michigan-state
- Dates: source [unknown]; canonical 1931-02-14
- Field: score
- Source value: `21-26`
- Canonical value: `16-24`
- Evidence: michigan-state 1931-02-14: 16-24
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0047466`

### 69. CONDITIONAL-DISCREPANCY-LOY-STG1-00186-CBBG-0047466-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs michigan-state
- Dates: source [unknown]; canonical 1931-02-14
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: michigan-state 1931-02-14: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0047466`

### 70. IDENTITY-LOY-STG1-00187

- Category: identity
- Matchup: loyola-chicago vs butler
- Date: [unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=22-26`
- Canonical value: `CBBG-0082871`
- Evidence: CBBG-0082871 1930-1931 [unknown] 27-22 sources=butler
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 71. CONDITIONAL-DISCREPANCY-LOY-STG1-00187-CBBG-0082871-SCORE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Date: [unknown]
- Field: score
- Source value: `26-22`
- Canonical value: `27-22`
- Evidence: butler [unknown]: 27-22
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0082871`

### 72. CONDITIONAL-DISCREPANCY-LOY-STG1-00187-CBBG-0082871-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Date: [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: butler [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0082871`

### 73. IDENTITY-LOY-STG1-00195

- Category: identity
- Matchup: loyola-chicago vs michigan-state
- Dates: source [unknown]; canonical 1931-02-14
- Field: game_identity
- Source value: `date=[unknown]; score=18-22`
- Canonical value: `CBBG-0047466`
- Evidence: CBBG-0047466 1930-1931 1931-02-14 16-24 sources=michigan-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 74. CONDITIONAL-DISCREPANCY-LOY-STG1-00195-CBBG-0047466-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs michigan-state
- Dates: source [unknown]; canonical 1931-02-14
- Field: score
- Source value: `18-22`
- Canonical value: `16-24`
- Evidence: michigan-state 1931-02-14: 16-24
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0047466`

### 75. CONDITIONAL-DISCREPANCY-LOY-STG1-00195-CBBG-0047466-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs michigan-state
- Dates: source [unknown]; canonical 1931-02-14
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: michigan-state 1931-02-14: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0047466`

### 76. IDENTITY-LOY-STG1-00198

- Category: identity
- Matchup: loyola-chicago vs depaul
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=15-23`
- Canonical value: `CBBG-0089684;CBBG-0089686`
- Evidence: CBBG-0089684 1930-1931 [unknown] 22-15 sources=depaul; CBBG-0089686 1930-1931 [unknown] 20-24 sources=depaul
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 77. CONDITIONAL-DISCREPANCY-LOY-STG1-00198-CBBG-0089684-SCORE

- Category: conditional_discrepancy
- Matchup: depaul vs loyola-chicago
- Date: [unknown]
- Field: score
- Source value: `23-15`
- Canonical value: `22-15`
- Evidence: depaul [unknown]: 22-15
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0089684`

### 78. CONDITIONAL-DISCREPANCY-LOY-STG1-00198-CBBG-0089684-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: depaul vs loyola-chicago
- Date: [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: depaul [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0089684`

### 79. CONDITIONAL-DISCREPANCY-LOY-STG1-00198-CBBG-0089686-SCORE

- Category: conditional_discrepancy
- Matchup: depaul vs loyola-chicago
- Date: [unknown]
- Field: score
- Source value: `23-15`
- Canonical value: `20-24`
- Evidence: depaul [unknown]: 20-24
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0089686`

### 80. CONDITIONAL-DISCREPANCY-LOY-STG1-00198-CBBG-0089686-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: depaul vs loyola-chicago
- Date: [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: depaul [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0089686`

### 81. CONDITIONAL-DISCREPANCY-LOY-STG1-00198-CBBG-0089686-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: depaul vs loyola-chicago
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `depaul`
- Canonical value: `loyola-chicago`
- Evidence: depaul [unknown]: loyola-chicago
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0089686`

### 82. IDENTITY-LOY-STG1-00206

- Category: identity
- Matchup: loyola-chicago vs butler
- Date: [unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=21-19`
- Canonical value: `CBBG-0082886`
- Evidence: CBBG-0082886 1931-1932 [unknown] 21-22 sources=butler
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 83. CONDITIONAL-DISCREPANCY-LOY-STG1-00206-CBBG-0082886-SCORE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Date: [unknown]
- Field: score
- Source value: `19-21`
- Canonical value: `21-22`
- Evidence: butler [unknown]: 21-22
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0082886`

### 84. DISCREPANCY-LOY-STG1-00242-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1934-02-10
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1934-02-10: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 85. DISCREPANCY-LOY-STG1-00247-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1934-03-05
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1934-03-05: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 86. DISCREPANCY-LOY-STG1-00265-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1935-02-16
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1935-02-16: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 87. DISCREPANCY-LOY-STG1-00267-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1935-03-01
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1935-03-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 88. DISCREPANCY-LOY-STG1-00280-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1936-01-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1936-01-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 89. DISCREPANCY-LOY-STG1-00281-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1936-02-07
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1936-02-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 90. IDENTITY-LOY-STG1-00292

- Category: identity
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1937-01-12
- Field: game_identity
- Source value: `date=[unknown]; score=45-21`
- Canonical value: `CBBG-0182981`
- Evidence: CBBG-0182981 1936-1937 1937-01-12 47-21 sources=saint-louis
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 91. CONDITIONAL-DISCREPANCY-LOY-STG1-00292-CBBG-0182981-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1937-01-12
- Field: score
- Source value: `45-21`
- Canonical value: `47-21`
- Evidence: saint-louis 1937-01-12: 47-21
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0182981`

### 92. CONDITIONAL-DISCREPANCY-LOY-STG1-00292-CBBG-0182981-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1937-01-12
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1937-01-12: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0182981`

### 93. DISCREPANCY-LOY-STG1-00308-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs utah
- Dates: source [unknown]; canonical 1938-01-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1938-01-06: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 94. DISCREPANCY-LOY-STG1-00343-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs st-john-s
- Dates: source [unknown]; canonical 1939-03-20
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: st-john-s 1939-03-20: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 95. DISCREPANCY-LOY-STG1-00343-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs st-john-s
- Dates: source [unknown]; canonical 1939-03-20
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-john-s 1939-03-20: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 96. IDENTITY-LOY-STG1-00376

- Category: identity
- Matchup: loyola-chicago vs depaul
- Date: [unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=34-37`
- Canonical value: `CBBG-0089843`
- Evidence: CBBG-0089843 1940-1941 [unknown] 37-33 sources=depaul
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 97. CONDITIONAL-DISCREPANCY-LOY-STG1-00376-CBBG-0089843-SCORE

- Category: conditional_discrepancy
- Matchup: depaul vs loyola-chicago
- Date: [unknown]
- Field: score
- Source value: `37-34`
- Canonical value: `37-33`
- Evidence: depaul [unknown]: 37-33
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0089843`

### 98. CONDITIONAL-DISCREPANCY-LOY-STG1-00376-CBBG-0089843-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: depaul vs loyola-chicago
- Date: [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0089843`

### 99. IDENTITY-LOY-STG1-00409

- Category: identity
- Matchup: loyola-chicago vs byu
- Dates: source [unknown]; canonical 1942-12-18
- Field: game_identity
- Source value: `date=[unknown]; score=50-42`
- Canonical value: `CBBG-0107195`
- Evidence: CBBG-0107195 1942-1943 1942-12-18 44-50 sources=byu
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 100. CONDITIONAL-DISCREPANCY-LOY-STG1-00409-CBBG-0107195-SCORE

- Category: conditional_discrepancy
- Matchup: byu vs loyola-chicago
- Dates: source [unknown]; canonical 1942-12-18
- Field: score
- Source value: `42-50`
- Canonical value: `44-50`
- Evidence: byu 1942-12-18: 44-50
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107195`

### 101. CONDITIONAL-DISCREPANCY-LOY-STG1-00409-CBBG-0107195-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: byu vs loyola-chicago
- Dates: source [unknown]; canonical 1942-12-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu 1942-12-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107195`

### 102. DISCREPANCY-LOY-STG1-00418-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1943-01-26
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1943-01-26: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 103. DISCREPANCY-LOY-STG1-00423-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1943-02-16
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1943-02-16: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 104. DISCREPANCY-LOY-STG1-00464-SITE_TYPE

- Category: discrepancy
- Matchup: indiana vs loyola-chicago
- Dates: source [unknown]; canonical 1946-12-21
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: indiana 1946-12-21: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 105. DISCREPANCY-LOY-STG1-00466-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs smu
- Date: [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: smu [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 106. DISCREPANCY-LOY-STG1-00467-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs tcu
- Dates: source [unknown]; canonical 1946-12-28
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: tcu 1946-12-28: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 107. DISCREPANCY-LOY-STG1-00474-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs oklahoma-state
- Dates: source [unknown]; canonical 1947-02-01
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: oklahoma-state 1947-02-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 108. DISCREPANCY-LOY-STG1-00481-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Dates: source [unknown]; canonical 1947-02-26
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1947-02-26: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 109. DISCREPANCY-LOY-STG1-00482-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Dates: source [unknown]; canonical 1947-03-01
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul 1947-03-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 110. DISCREPANCY-LOY-STG1-00494-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1947-12-20
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul 1947-12-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 111. DISCREPANCY-LOY-STG1-00495-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs tcu
- Date: 1947-12-23
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: tcu 1947-12-23: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 112. DISCREPANCY-LOY-STG1-00497-SITE_TYPE

- Category: discrepancy
- Matchup: georgetown vs loyola-chicago
- Date: 1948-01-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgetown 1948-01-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 113. DISCREPANCY-LOY-STG1-00508-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs oklahoma-state
- Date: 1948-01-31
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: oklahoma-state 1948-01-31: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 114. DISCREPANCY-LOY-STG1-00512-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1948-02-17
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1948-02-17: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 115. DISCREPANCY-LOY-STG1-00517-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1948-03-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul 1948-03-06: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 116. DISCREPANCY-LOY-STG1-00525-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1948-12-22
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul 1948-12-22: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 117. DISCREPANCY-LOY-STG1-00537-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1949-02-12
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul 1949-02-12: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 118. DISCREPANCY-LOY-STG1-00553-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs wisconsin
- Date: 1949-12-10
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: wisconsin 1949-12-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 119. DISCREPANCY-LOY-STG1-00554-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1949-12-12
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1949-12-12: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 120. DISCREPANCY-LOY-STG1-00555-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1949-12-17
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul 1949-12-17: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 121. DISCREPANCY-LOY-STG1-00557-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs oregon
- Date: 1949-12-27
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: oregon 1949-12-27: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 122. DISCREPANCY-LOY-STG1-00559-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs utah
- Date: 1950-01-02
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1950-01-02: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 123. DISCREPANCY-LOY-STG1-00560-SCORE

- Category: discrepancy
- Matchup: byu vs loyola-chicago
- Date: 1950-01-04
- Field: score
- Source value: `51-45`
- Canonical value: `54-45`
- Evidence: byu 1950-01-04: 54-45
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 124. DISCREPANCY-LOY-STG1-00560-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs loyola-chicago
- Date: 1950-01-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu 1950-01-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 125. DISCREPANCY-LOY-STG1-00566-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs oklahoma-state
- Date: 1950-01-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: oklahoma-state 1950-01-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 126. DISCREPANCY-LOY-STG1-00569-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs notre-dame
- Date: 1950-02-07
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: notre-dame 1950-02-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 127. DISCREPANCY-LOY-STG1-00575-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1950-02-25
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul 1950-02-25: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 128. DISCREPANCY-LOY-STG1-00586-SITE_TYPE

- Category: discrepancy
- Matchup: iowa vs loyola-chicago
- Date: 1950-12-28
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: iowa 1950-12-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 129. DISCREPANCY-LOY-STG1-00593-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1951-01-20
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul 1951-01-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 130. DISCREPANCY-LOY-STG1-00601-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1951-02-17
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1951-02-17: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 131. DISCREPANCY-LOY-STG1-00606-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1951-03-08
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: depaul 1951-03-08: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 132. DISCREPANCY-LOY-STG1-00607-SITE_TYPE

- Category: discrepancy
- Matchup: kentucky vs loyola-chicago
- Dates: source [unknown]; canonical 1951-03-13
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: kentucky 1951-03-13: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 133. DISCREPANCY-LOY-STG1-00620-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs xavier
- Date: 1952-01-23
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1952-01-23: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 134. DISCREPANCY-LOY-STG1-00621-SITE_TYPE

- Category: discrepancy
- Matchup: louisville vs loyola-chicago
- Date: 1952-01-26
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: louisville 1952-01-26: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 135. DISCREPANCY-LOY-STG1-00626-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1952-02-16
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul 1952-02-16: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 136. DISCREPANCY-LOY-STG1-00628-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1952-02-21
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1952-02-21: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 137. DISCREPANCY-LOY-STG1-00629-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs seton-hall
- Date: 1952-02-23
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: seton-hall 1952-02-23: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 138. DISCREPANCY-LOY-STG1-00634-SITE_TYPE

- Category: discrepancy
- Matchup: creighton vs loyola-chicago
- Date: 1952-12-01
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: creighton 1952-12-01: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 139. DISCREPANCY-LOY-STG1-00648-SITE_TYPE

- Category: discrepancy
- Matchup: louisville vs loyola-chicago
- Date: 1953-01-31
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: louisville 1953-01-31: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 140. DISCREPANCY-LOY-STG1-00650-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1953-02-07
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: depaul 1953-02-07: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 141. DISCREPANCY-LOY-STG1-00653-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs seton-hall
- Date: 1953-02-21
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: seton-hall 1953-02-21: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 142. DISCREPANCY-LOY-STG1-00654-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1953-02-23
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: marquette 1953-02-23: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 143. DISCREPANCY-LOY-STG1-00654-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1953-02-23
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1953-02-23: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 144. DISCREPANCY-LOY-STG1-00659-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs wisconsin
- Date: 1953-12-07
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: wisconsin 1953-12-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 145. DISCREPANCY-LOY-STG1-00667-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1954-01-11
- Field: score
- Source value: `63-69`
- Canonical value: `63-68`
- Evidence: marquette 1954-01-11: 63-68
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 146. DISCREPANCY-LOY-STG1-00667-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1954-01-11
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1954-01-11: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 147. DISCREPANCY-LOY-STG1-00674-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs seton-hall
- Date: 1954-02-15
- Field: score
- Source value: `60-72`
- Canonical value: `63-72`
- Evidence: seton-hall 1954-02-15: 63-72
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 148. DISCREPANCY-LOY-STG1-00678-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs notre-dame
- Date: 1954-02-27
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: notre-dame 1954-02-27: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 149. DISCREPANCY-LOY-STG1-00680-SITE_TYPE

- Category: discrepancy
- Matchup: iowa vs loyola-chicago
- Date: 1954-12-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: iowa 1954-12-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 150. DISCREPANCY-LOY-STG1-00690-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1955-01-10
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1955-01-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 151. DISCREPANCY-LOY-STG1-00693-SITE_TYPE

- Category: discrepancy
- Matchup: illinois vs loyola-chicago
- Date: 1955-01-29
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: illinois 1955-01-29: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 152. DISCREPANCY-LOY-STG1-00695-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs notre-dame
- Date: 1955-02-05
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: notre-dame 1955-02-05: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 153. DISCREPANCY-LOY-STG1-00702-SITE_TYPE

- Category: discrepancy
- Matchup: louisville vs loyola-chicago
- Date: 1955-02-26
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: louisville 1955-02-26: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 154. DISCREPANCY-LOY-STG1-00705-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs notre-dame
- Date: 1955-12-07
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: notre-dame 1955-12-07: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 155. DISCREPANCY-LOY-STG1-00706-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs ohio-state
- Date: 1955-12-10
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: ohio-state 1955-12-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 156. DISCREPANCY-LOY-STG1-00707-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs purdue
- Date: 1955-12-14
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: purdue 1955-12-14: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 157. DISCREPANCY-LOY-STG1-00718-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs notre-dame
- Date: 1956-02-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: notre-dame 1956-02-04: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 158. DISCREPANCY-LOY-STG1-00719-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs seton-hall
- Date: 1956-02-11
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: seton-hall 1956-02-11: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 159. DISCREPANCY-LOY-STG1-00723-SITE_TYPE

- Category: discrepancy
- Matchup: creighton vs loyola-chicago
- Date: 1956-02-22
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: creighton 1956-02-22: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 160. DISCREPANCY-LOY-STG1-00724-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1956-02-25
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1956-02-25: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 161. DISCREPANCY-LOY-STG1-00742-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs oklahoma-state
- Date: 1957-01-26
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: oklahoma-state 1957-01-26: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 162. DISCREPANCY-LOY-STG1-00745-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs notre-dame
- Date: 1957-02-09
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: notre-dame 1957-02-09: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 163. DISCREPANCY-LOY-STG1-00746-SITE_TYPE

- Category: discrepancy
- Matchup: kentucky vs loyola-chicago
- Date: 1957-02-15
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: kentucky 1957-02-15: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 164. DISCREPANCY-LOY-STG1-00748-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1957-02-23
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: marquette 1957-02-23: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 165. DISCREPANCY-LOY-STG1-00748-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1957-02-23
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1957-02-23: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 166. DISCREPANCY-LOY-STG1-00763-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1958-01-25
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1958-01-25: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 167. DISCREPANCY-LOY-STG1-00764-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs xavier
- Date: 1958-02-01
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1958-02-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 168. DISCREPANCY-LOY-STG1-00770-SITE_TYPE

- Category: discrepancy
- Matchup: kentucky vs loyola-chicago
- Date: 1958-02-15
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: kentucky 1958-02-15: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 169. DISCREPANCY-LOY-STG1-00778-SITE_TYPE

- Category: discrepancy
- Matchup: creighton vs loyola-chicago
- Date: 1958-12-11
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: creighton 1958-12-11: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 170. DISCREPANCY-LOY-STG1-00788-SITE_TYPE

- Category: discrepancy
- Matchup: georgetown vs loyola-chicago
- Date: 1959-01-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgetown 1959-01-30: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 171. DISCREPANCY-LOY-STG1-00789-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs st-john-s
- Date: 1959-01-31
- Field: overtime_periods
- Source value: `0`
- Canonical value: `2`
- Evidence: st-john-s 1959-01-31: 2
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 172. DISCREPANCY-LOY-STG1-00789-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs st-john-s
- Date: 1959-01-31
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `NEUTRAL`
- Evidence: st-john-s 1959-01-31: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 173. DISCREPANCY-LOY-STG1-00791-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1959-02-07
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1959-02-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 174. DISCREPANCY-LOY-STG1-00793-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs north-carolina
- Date: 1959-02-14
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: north-carolina 1959-02-14: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 175. DISCREPANCY-LOY-STG1-00801-SITE_TYPE

- Category: discrepancy
- Matchup: creighton vs loyola-chicago
- Date: 1959-12-07
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: creighton 1959-12-07: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 176. DISCREPANCY-LOY-STG1-00805-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs missouri
- Date: 1959-12-21
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: missouri 1959-12-21: UNKNOWN
- Recommended: `LEAVE_UNRESOLVED`
- Decision: `PENDING`
- Basis: [required before approval]

### 177. DISCREPANCY-LOY-STG1-00810-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs xavier
- Date: 1960-01-22
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1960-01-22: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 178. DISCREPANCY-LOY-STG1-00812-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs st-john-s
- Date: 1960-01-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: st-john-s 1960-01-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 179. DISCREPANCY-LOY-STG1-00815-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1960-02-13
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1960-02-13: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 180. DISCREPANCY-LOY-STG1-00826-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs ohio-state
- Date: 1960-12-19
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: ohio-state 1960-12-19: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 181. DISCREPANCY-LOY-STG1-00832-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs wisconsin
- Date: 1961-01-28
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: wisconsin 1961-01-28: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 182. DISCREPANCY-LOY-STG1-00836-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs st-john-s
- Date: 1961-02-07
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: st-john-s 1961-02-07: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 183. DISCREPANCY-LOY-STG1-00837-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1961-02-14
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1961-02-14: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 184. DISCREPANCY-LOY-STG1-00838-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs ucla
- Date: 1961-02-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: ucla 1961-02-18: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 185. DISCREPANCY-LOY-STG1-00843-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs xavier
- Date: 1961-03-11
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1961-03-11: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 186. DISCREPANCY-LOY-STG1-00857-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs st-john-s
- Date: 1962-01-27
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: st-john-s 1962-01-27: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 187. DISCREPANCY-LOY-STG1-00891-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1963-02-12
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: marquette 1963-02-12: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 188. DISCREPANCY-LOY-STG1-00901-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: cincinnati vs loyola-chicago
- Dates: source [unknown]; canonical 1963-03-23
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: cincinnati 1963-03-23: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 189. DISCREPANCY-LOY-STG1-00937-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs minnesota
- Date: 1964-12-22
- Field: score
- Source value: `73-89`
- Canonical value: `75-89`
- Evidence: minnesota 1964-12-22: 75-89
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 190. DISCREPANCY-LOY-STG1-00938-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1964-12-26
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1964-12-26: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 191. DISCREPANCY-LOY-STG1-00940-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1964-12-31
- Field: score
- Source value: `58-90`
- Canonical value: `57-90`
- Evidence: saint-louis 1964-12-31: 57-90
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 192. DISCREPANCY-LOY-STG1-00940-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1964-12-31
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `NEUTRAL`
- Evidence: saint-louis 1964-12-31: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 193. DISCREPANCY-LOY-STG1-00941-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1965-01-06
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: marquette 1965-01-06: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 194. DISCREPANCY-LOY-STG1-00945-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs ucla
- Date: 1965-01-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: ucla 1965-01-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 195. DISCREPANCY-LOY-STG1-00946-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs st-john-s
- Date: 1965-02-01
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: st-john-s 1965-02-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 196. IDENTITY-LOY-STG1-00947

- Category: identity
- Matchup: loyola-chicago vs indiana
- Dates: source 1965-02-04; canonical 1965-02-08
- Field: game_identity
- Source value: `date=1965-02-04; score=82-109`
- Canonical value: `CBBG-0036310`
- Evidence: CBBG-0036310 1964-1965 1965-02-08 109-82 sources=indiana
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 197. CONDITIONAL-DISCREPANCY-LOY-STG1-00947-CBBG-0036310-GAME_DATE

- Category: conditional_discrepancy
- Matchup: indiana vs loyola-chicago
- Dates: source 1965-02-04; canonical 1965-02-08
- Field: game_date
- Source value: `1965-02-04`
- Canonical value: `1965-02-08`
- Evidence: indiana 1965-02-08: 1965-02-08
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0036310`

### 198. DISCREPANCY-LOY-STG1-00985-SITE_TYPE

- Category: discrepancy
- Matchup: indiana vs loyola-chicago
- Date: 1966-12-17
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: indiana 1966-12-17: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 199. DISCREPANCY-LOY-STG1-00989-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1966-12-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1966-12-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 200. IDENTITY-LOY-STG1-00990

- Category: identity
- Matchup: loyola-chicago vs minnesota
- Dates: source 1967-01-03; canonical 1967-01-05
- Field: game_identity
- Source value: `date=1967-01-03; score=87-63`
- Canonical value: `CBBG-0026093`
- Evidence: CBBG-0026093 1966-1967 1967-01-05 87-63 sources=minnesota
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 201. CONDITIONAL-DISCREPANCY-LOY-STG1-00990-CBBG-0026093-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs minnesota
- Dates: source 1967-01-03; canonical 1967-01-05
- Field: game_date
- Source value: `1967-01-03`
- Canonical value: `1967-01-05`
- Evidence: minnesota 1967-01-05: 1967-01-05
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0026093`

### 202. DISCREPANCY-LOY-STG1-00994-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs ucla
- Date: 1967-01-28
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: ucla 1967-01-28: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 203. DISCREPANCY-LOY-STG1-00996-SITE_TYPE

- Category: discrepancy
- Matchup: iowa vs loyola-chicago
- Date: 1967-02-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: iowa 1967-02-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 204. DISCREPANCY-LOY-STG1-00998-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1967-02-13
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1967-02-13: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 205. DISCREPANCY-LOY-STG1-01010-SITE_TYPE

- Category: discrepancy
- Matchup: georgia-tech vs loyola-chicago
- Date: 1967-12-30
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: georgia-tech 1967-12-30: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 206. DISCREPANCY-LOY-STG1-01013-SCORE

- Category: discrepancy
- Matchup: iowa vs loyola-chicago
- Date: 1968-01-08
- Field: score
- Source value: `71-63`
- Canonical value: `71-65`
- Evidence: iowa 1968-01-08: 71-65
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 207. DISCREPANCY-LOY-STG1-01039-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1969-01-07
- Field: score
- Source value: `64-65`
- Canonical value: `56-61`
- Evidence: marquette 1969-01-07: 56-61
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 208. DISCREPANCY-LOY-STG1-01042-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1969-01-24
- Field: score
- Source value: `56-61`
- Canonical value: `64-65`
- Evidence: marquette 1969-01-24: 64-65
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 209. DISCREPANCY-LOY-STG1-01044-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs michigan
- Date: 1969-02-01
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: michigan 1969-02-01: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 210. DISCREPANCY-LOY-STG1-01044-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs michigan
- Date: 1969-02-01
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: michigan 1969-02-01: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 211. DISCREPANCY-LOY-STG1-01107-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1971-12-29
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1971-12-29: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 212. DISCREPANCY-LOY-STG1-01124-SITE_TYPE

- Category: discrepancy
- Matchup: arizona-state vs loyola-chicago
- Date: 1972-12-09
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: arizona-state 1972-12-09: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 213. DISCREPANCY-LOY-STG1-01126-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs minnesota
- Date: 1972-12-16
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: minnesota 1972-12-16: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 214. DISCREPANCY-LOY-STG1-01134-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs ucla
- Date: 1973-01-25
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: ucla 1973-01-25: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 215. DISCREPANCY-LOY-STG1-01135-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1973-01-27
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1973-01-27: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 216. DISCREPANCY-LOY-STG1-01138-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs northwestern
- Date: 1973-02-10
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: northwestern 1973-02-10: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 217. DISCREPANCY-LOY-STG1-01148-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs minnesota
- Date: 1973-12-13
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: minnesota 1973-12-13: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 218. DISCREPANCY-LOY-STG1-01175-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs minnesota
- Date: 1974-12-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: minnesota 1974-12-18: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 219. DISCREPANCY-LOY-STG1-01180-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs xavier
- Date: 1975-01-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1975-01-04: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 220. DISCREPANCY-LOY-STG1-01235-SCORE

- Category: discrepancy
- Matchup: creighton vs loyola-chicago
- Date: 1977-01-29
- Field: score
- Source value: `85-81`
- Canonical value: `86-81`
- Evidence: creighton 1977-01-29: 86-81
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 221. DISCREPANCY-LOY-STG1-01248-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs minnesota
- Date: 1977-11-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: minnesota 1977-11-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 222. DISCREPANCY-LOY-STG1-01250-SITE_TYPE

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1977-12-05
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: butler 1977-12-05: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 223. DISCREPANCY-LOY-STG1-01262-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1978-01-28
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1978-01-28: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 224. DISCREPANCY-LOY-STG1-01265-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: georgetown vs loyola-chicago
- Date: 1978-02-04
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: georgetown 1978-02-04: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 225. DISCREPANCY-LOY-STG1-01265-SITE_TYPE

- Category: discrepancy
- Matchup: georgetown vs loyola-chicago
- Date: 1978-02-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgetown 1978-02-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 226. DISCREPANCY-LOY-STG1-01269-SCORE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1978-02-18
- Field: score
- Source value: `73-63`
- Canonical value: `83-73`
- Evidence: depaul 1978-02-18: 83-73
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 227. DISCREPANCY-LOY-STG1-01269-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1978-02-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: depaul 1978-02-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 228. DISCREPANCY-LOY-STG1-01275-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs minnesota
- Date: 1978-12-02
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: minnesota 1978-12-02: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 229. DISCREPANCY-LOY-STG1-01307-SCORE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1979-12-22
- Field: score
- Source value: `92-83`
- Canonical value: `92-85`
- Evidence: depaul 1979-12-22: 92-85
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 230. DISCREPANCY-LOY-STG1-01315-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1980-01-19
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 1980-01-19: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 231. DISCREPANCY-LOY-STG1-01335-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs loyola-chicago
- Date: 1980-12-19
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: depaul 1980-12-19: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 232. DISCREPANCY-LOY-STG1-01359-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: illinois vs loyola-chicago
- Date: 1981-11-28
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: illinois 1981-11-28: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 233. DISCREPANCY-LOY-STG1-01384-SITE_TYPE

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1982-03-02
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: butler 1982-03-02: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 234. DISCREPANCY-LOY-STG1-01400-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1983-01-22
- Field: score
- Source value: `73-62`
- Canonical value: `65-62`
- Evidence: saint-louis 1983-01-22: 65-62
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 235. DISCREPANCY-LOY-STG1-01400-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs saint-louis
- Date: 1983-01-22
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1983-01-22: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 236. DISCREPANCY-LOY-STG1-01412-SCORE

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1983-02-28
- Field: score
- Source value: `72-82`
- Canonical value: `72-83`
- Evidence: butler 1983-02-28: 72-83
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 237. DISCREPANCY-LOY-STG1-01415-GAME_DATE

- Category: discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source 1983-03-10; canonical 1983-03-11
- Field: game_date
- Source value: `1983-03-10`
- Canonical value: `1983-03-11`
- Evidence: xavier 1983-03-11: 1983-03-11
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 238. DISCREPANCY-LOY-STG1-01417-SITE_TYPE

- Category: discrepancy
- Matchup: illinois vs loyola-chicago
- Dates: source [unknown]; canonical 1983-11-26
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: illinois 1983-11-26: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 239. IDENTITY-LOY-STG1-01439

- Category: identity
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1984-01-23;1984-02-20
- Field: game_identity
- Source value: `date=[unknown]; score=75-63`
- Canonical value: `CBBG-0183663;CBBG-0183669`
- Evidence: CBBG-0183663 1983-1984 1984-01-23 79-76 sources=saint-louis; CBBG-0183669 1983-1984 1984-02-20 75-64 sources=saint-louis
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 240. CONDITIONAL-DISCREPANCY-LOY-STG1-01439-CBBG-0183663-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1984-01-23
- Field: score
- Source value: `75-63`
- Canonical value: `79-76`
- Evidence: saint-louis 1984-01-23: 79-76
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0183663`

### 241. CONDITIONAL-DISCREPANCY-LOY-STG1-01439-CBBG-0183663-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1984-01-23
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1984-01-23: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0183663`

### 242. CONDITIONAL-DISCREPANCY-LOY-STG1-01439-CBBG-0183669-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1984-02-20
- Field: score
- Source value: `75-63`
- Canonical value: `75-64`
- Evidence: saint-louis 1984-02-20: 75-64
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0183669`

### 243. IDENTITY-LOY-STG1-01444

- Category: identity
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1984-01-09;1984-02-06;1984-03-09
- Field: game_identity
- Source value: `date=[unknown]; score=69-90`
- Canonical value: `CBBG-0153383;CBBG-0153390;CBBG-0153397`
- Evidence: CBBG-0153383 1983-1984 1984-01-09 94-83 sources=xavier; CBBG-0153390 1983-1984 1984-02-06 61-64 sources=xavier; CBBG-0153397 1983-1984 1984-03-09 69-80 sources=xavier
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 244. CONDITIONAL-DISCREPANCY-LOY-STG1-01444-CBBG-0153383-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1984-01-09
- Field: score
- Source value: `69-90`
- Canonical value: `94-83`
- Evidence: xavier 1984-01-09: 94-83
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0153383`

### 245. CONDITIONAL-DISCREPANCY-LOY-STG1-01444-CBBG-0153383-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1984-01-09
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1984-01-09: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0153383`

### 246. CONDITIONAL-DISCREPANCY-LOY-STG1-01444-CBBG-0153383-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1984-01-09
- Field: game_type
- Source value: `CONFERENCE_TOURNAMENT`
- Canonical value: `REGULAR_SEASON`
- Evidence: xavier 1984-01-09: REGULAR_SEASON
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0153383`

### 247. CONDITIONAL-DISCREPANCY-LOY-STG1-01444-CBBG-0153383-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1984-01-09
- Field: result_winner_team_key
- Source value: `xavier`
- Canonical value: `loyola-chicago`
- Evidence: xavier 1984-01-09: loyola-chicago
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0153383`

### 248. CONDITIONAL-DISCREPANCY-LOY-STG1-01444-CBBG-0153390-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1984-02-06
- Field: score
- Source value: `69-90`
- Canonical value: `61-64`
- Evidence: xavier 1984-02-06: 61-64
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0153390`

### 249. CONDITIONAL-DISCREPANCY-LOY-STG1-01444-CBBG-0153390-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1984-02-06
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: xavier 1984-02-06: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0153390`

### 250. CONDITIONAL-DISCREPANCY-LOY-STG1-01444-CBBG-0153390-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1984-02-06
- Field: game_type
- Source value: `CONFERENCE_TOURNAMENT`
- Canonical value: `REGULAR_SEASON`
- Evidence: xavier 1984-02-06: REGULAR_SEASON
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0153390`

### 251. CONDITIONAL-DISCREPANCY-LOY-STG1-01444-CBBG-0153397-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1984-03-09
- Field: score
- Source value: `69-90`
- Canonical value: `69-80`
- Evidence: xavier 1984-03-09: 69-80
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0153397`

### 252. DISCREPANCY-LOY-STG1-01453-SITE_TYPE

- Category: discrepancy
- Matchup: illinois vs loyola-chicago
- Date: 1984-12-22
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: illinois 1984-12-22: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 253. DISCREPANCY-LOY-STG1-01456-SCORE

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1985-01-05
- Field: score
- Source value: `76-86`
- Canonical value: `74-86`
- Evidence: butler 1985-01-05: 74-86
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 254. DISCREPANCY-LOY-STG1-01499-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs xavier
- Date: 1986-02-10
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: xavier 1986-02-10: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 255. DISCREPANCY-LOY-STG1-01502-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: cincinnati vs loyola-chicago
- Date: 1986-02-20
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: cincinnati 1986-02-20: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 256. DISCREPANCY-LOY-STG1-01517-SCORE

- Category: discrepancy
- Matchup: colorado vs loyola-chicago
- Date: 1987-01-07
- Field: score
- Source value: `66-65`
- Canonical value: `65-64`
- Evidence: colorado 1987-01-07: 65-64
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 257. DISCREPANCY-LOY-STG1-01518-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1987-01-10
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 1987-01-10: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 258. IDENTITY-LOY-STG1-01533

- Category: identity
- Matchup: loyola-chicago vs saint-louis
- Dates: source 1987-02-23; canonical 1987-01-26;1987-02-12
- Field: game_identity
- Source value: `date=1987-02-23; score=68-70`
- Canonical value: `CBBG-0183730;CBBG-0183737`
- Evidence: CBBG-0183730 1986-1987 1987-01-26 76-67 sources=saint-louis; CBBG-0183737 1986-1987 1987-02-12 68-70 sources=saint-louis
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 259. CONDITIONAL-DISCREPANCY-LOY-STG1-01533-CBBG-0183730-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source 1987-02-23; canonical 1987-01-26
- Field: game_date
- Source value: `1987-02-23`
- Canonical value: `1987-01-26`
- Evidence: saint-louis 1987-01-26: 1987-01-26
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0183730`

### 260. CONDITIONAL-DISCREPANCY-LOY-STG1-01533-CBBG-0183730-SCORE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source 1987-02-23; canonical 1987-01-26
- Field: score
- Source value: `68-70`
- Canonical value: `76-67`
- Evidence: saint-louis 1987-01-26: 76-67
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0183730`

### 261. CONDITIONAL-DISCREPANCY-LOY-STG1-01533-CBBG-0183730-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source 1987-02-23; canonical 1987-01-26
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: saint-louis 1987-01-26: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0183730`

### 262. CONDITIONAL-DISCREPANCY-LOY-STG1-01533-CBBG-0183730-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source 1987-02-23; canonical 1987-01-26
- Field: result_winner_team_key
- Source value: `saint-louis`
- Canonical value: `loyola-chicago`
- Evidence: saint-louis 1987-01-26: loyola-chicago
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0183730`

### 263. CONDITIONAL-DISCREPANCY-LOY-STG1-01533-CBBG-0183737-GAME_DATE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs saint-louis
- Dates: source 1987-02-23; canonical 1987-02-12
- Field: game_date
- Source value: `1987-02-23`
- Canonical value: `1987-02-12`
- Evidence: saint-louis 1987-02-12: 1987-02-12
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0183737`

### 264. DISCREPANCY-LOY-STG1-01535-GAME_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs xavier
- Date: 1987-02-27
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: xavier 1987-02-27: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 265. DISCREPANCY-LOY-STG1-01540-SCORE

- Category: discrepancy
- Matchup: loyola-chicago vs northwestern
- Date: 1987-12-17
- Field: score
- Source value: `47-54`
- Canonical value: `47-57`
- Evidence: northwestern 1987-12-17: 47-57
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 266. DISCREPANCY-LOY-STG1-01563-SITE_TYPE

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1988-03-10
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: butler 1988-03-10: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 267. DISCREPANCY-LOY-STG1-01594-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1989-12-05
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: marquette 1989-12-05: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 268. DISCREPANCY-LOY-STG1-01644-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs marquette
- Date: 1991-02-17
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: marquette 1991-02-17: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 269. DISCREPANCY-LOY-STG1-01704-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1993-03-04
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 1993-03-04: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 270. DISCREPANCY-LOY-STG1-01744-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1995-01-12
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 1995-01-12: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 271. DISCREPANCY-LOY-STG1-01753-SCORE

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1995-02-09
- Field: score
- Source value: `67-60`
- Canonical value: `67-50`
- Evidence: butler 1995-02-09: 67-50
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 272. DISCREPANCY-LOY-STG1-01769-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs northwestern
- Date: 1995-12-30
- Field: overtime_periods
- Source value: `0`
- Canonical value: `2`
- Evidence: northwestern 1995-12-30: 2
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 273. DISCREPANCY-LOY-STG1-01830-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1998-01-07
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 1998-01-07: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 274. DISCREPANCY-LOY-STG1-01837-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1998-01-31
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 1998-01-31: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 275. DISCREPANCY-LOY-STG1-01844-SITE_TYPE

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 1998-02-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: butler 1998-02-28: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 276. IDENTITY-LOY-STG1-01857

- Category: identity
- Matchup: loyola-chicago vs butler
- Dates: source 1999-01-02; canonical 1999-01-04;1999-01-30
- Field: game_identity
- Source value: `date=1999-01-02; score=53-51`
- Canonical value: `CBBG-0084292;CBBG-0084301`
- Evidence: CBBG-0084292 1998-1999 1999-01-04 51-53 sources=butler; CBBG-0084301 1998-1999 1999-01-30 57-52 sources=butler
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 277. CONDITIONAL-DISCREPANCY-LOY-STG1-01857-CBBG-0084292-GAME_DATE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Dates: source 1999-01-02; canonical 1999-01-04
- Field: game_date
- Source value: `1999-01-02`
- Canonical value: `1999-01-04`
- Evidence: butler 1999-01-04: 1999-01-04
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0084292`

### 278. CONDITIONAL-DISCREPANCY-LOY-STG1-01857-CBBG-0084301-GAME_DATE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Dates: source 1999-01-02; canonical 1999-01-30
- Field: game_date
- Source value: `1999-01-02`
- Canonical value: `1999-01-30`
- Evidence: butler 1999-01-30: 1999-01-30
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0084301`

### 279. CONDITIONAL-DISCREPANCY-LOY-STG1-01857-CBBG-0084301-SCORE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Dates: source 1999-01-02; canonical 1999-01-30
- Field: score
- Source value: `51-53`
- Canonical value: `57-52`
- Evidence: butler 1999-01-30: 57-52
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0084301`

### 280. CONDITIONAL-DISCREPANCY-LOY-STG1-01857-CBBG-0084301-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Dates: source 1999-01-02; canonical 1999-01-30
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: butler 1999-01-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0084301`

### 281. CONDITIONAL-DISCREPANCY-LOY-STG1-01857-CBBG-0084301-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Dates: source 1999-01-02; canonical 1999-01-30
- Field: result_winner_team_key
- Source value: `loyola-chicago`
- Canonical value: `butler`
- Evidence: butler 1999-01-30: butler
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0084301`

### 282. IDENTITY-LOY-STG1-01952

- Category: identity
- Matchup: loyola-chicago vs butler
- Dates: source 2002-02-16; canonical 2002-01-23;2002-02-20
- Field: game_identity
- Source value: `date=2002-02-16; score=60-56`
- Canonical value: `CBBG-0084391;CBBG-0084399`
- Evidence: CBBG-0084391 2001-2002 2002-01-23 78-48 sources=butler; CBBG-0084399 2001-2002 2002-02-20 56-60 sources=butler
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 283. CONDITIONAL-DISCREPANCY-LOY-STG1-01952-CBBG-0084391-GAME_DATE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Dates: source 2002-02-16; canonical 2002-01-23
- Field: game_date
- Source value: `2002-02-16`
- Canonical value: `2002-01-23`
- Evidence: butler 2002-01-23: 2002-01-23
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0084391`

### 284. CONDITIONAL-DISCREPANCY-LOY-STG1-01952-CBBG-0084391-SCORE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Dates: source 2002-02-16; canonical 2002-01-23
- Field: score
- Source value: `56-60`
- Canonical value: `78-48`
- Evidence: butler 2002-01-23: 78-48
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0084391`

### 285. CONDITIONAL-DISCREPANCY-LOY-STG1-01952-CBBG-0084391-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Dates: source 2002-02-16; canonical 2002-01-23
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: butler 2002-01-23: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0084391`

### 286. CONDITIONAL-DISCREPANCY-LOY-STG1-01952-CBBG-0084391-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Dates: source 2002-02-16; canonical 2002-01-23
- Field: result_winner_team_key
- Source value: `loyola-chicago`
- Canonical value: `butler`
- Evidence: butler 2002-01-23: butler
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0084391`

### 287. CONDITIONAL-DISCREPANCY-LOY-STG1-01952-CBBG-0084399-GAME_DATE

- Category: conditional_discrepancy
- Matchup: butler vs loyola-chicago
- Dates: source 2002-02-16; canonical 2002-02-20
- Field: game_date
- Source value: `2002-02-16`
- Canonical value: `2002-02-20`
- Evidence: butler 2002-02-20: 2002-02-20
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0084399`

### 288. DISCREPANCY-LOY-STG1-01972-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 2003-01-09
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 2003-01-09: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 289. DISCREPANCY-LOY-STG1-02009-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 2004-02-07
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 2004-02-07: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 290. DISCREPANCY-LOY-STG1-02031-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 2005-01-13
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 2005-01-13: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 291. DISCREPANCY-LOY-STG1-02097-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 2007-01-25
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 2007-01-25: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 292. DISCREPANCY-LOY-STG1-02108-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: butler vs loyola-chicago
- Date: 2007-03-03
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: butler 2007-03-03: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 293. DISCREPANCY-LOY-STG1-02280-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: chicago-state vs loyola-chicago
- Date: 2013-01-20
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: chicago-state 2013-01-20: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 294. DISCREPANCY-LOY-STG1-02301-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: loyola-chicago vs mississippi-state
- Date: 2013-12-01
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: mississippi-state 2013-12-01: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 295. DISCREPANCY-LOY-STG1-02566-SITE_TYPE

- Category: discrepancy
- Matchup: loyola-chicago vs michigan-state
- Date: 2021-11-24
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: michigan-state 2021-11-24: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 296. IDENTITY-LOY-STG1-02730

- Category: identity
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1930-01-14;1930-01-23
- Field: game_identity
- Source value: `date=[unknown]; score=18-13`
- Canonical value: `CBBG-0152440;CBBG-0152443`
- Evidence: CBBG-0152440 1929-1930 1930-01-14 18-13 sources=xavier; CBBG-0152443 1929-1930 1930-01-23 18-13 sources=xavier
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 297. CONDITIONAL-DISCREPANCY-LOY-STG1-02730-CBBG-0152440-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1930-01-14
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1930-01-14: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0152440`

### 298. CONDITIONAL-DISCREPANCY-LOY-STG1-02730-CBBG-0152443-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1930-01-23
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: xavier 1930-01-23: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0152443`

### 299. CANONICAL-SITE-PATCH-CBBG-0084292

- Category: canonical_site_patch
- Matchup: butler vs loyola-chicago
- Dates: source [unknown]; canonical 1999-01-04
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_B_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from butler; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 300. CANONICAL-SITE-PATCH-CBBG-0084399

- Category: canonical_site_patch
- Matchup: butler vs loyola-chicago
- Dates: source [unknown]; canonical 2002-02-20
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_B_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from butler; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 301. CANONICAL-SITE-PATCH-CBBG-0089684

- Category: canonical_site_patch
- Matchup: depaul vs loyola-chicago
- Date: [unknown]
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_B_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from depaul; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 302. CANONICAL-SITE-PATCH-CBBG-0107195

- Category: canonical_site_patch
- Matchup: byu vs loyola-chicago
- Dates: source [unknown]; canonical 1942-12-18
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_B_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from byu; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 303. CANONICAL-SITE-PATCH-CBBG-0117714

- Category: canonical_site_patch
- Matchup: loyola-chicago vs oregon-state
- Date: [unknown]
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from oregon-state; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 304. CANONICAL-SITE-PATCH-CBBG-0148467

- Category: canonical_site_patch
- Matchup: creighton vs loyola-chicago
- Dates: source [unknown]; canonical 1926-01-21
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_B_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from creighton; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 305. CANONICAL-SITE-PATCH-CBBG-0150735

- Category: canonical_site_patch
- Matchup: loyola-chicago vs marquette
- Dates: source [unknown]; canonical 1926-02-13
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from marquette; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 306. CANONICAL-SITE-PATCH-CBBG-0150746

- Category: canonical_site_patch
- Matchup: loyola-chicago vs marquette
- Dates: source [unknown]; canonical 1928-01-13
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from marquette; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 307. CANONICAL-SITE-PATCH-CBBG-0152420

- Category: canonical_site_patch
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1928-02-25
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from xavier; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 308. CANONICAL-SITE-PATCH-CBBG-0152440

- Category: canonical_site_patch
- Matchup: loyola-chicago vs xavier
- Dates: source [unknown]; canonical 1930-01-14
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from xavier; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 309. CANONICAL-SITE-PATCH-CBBG-0182742

- Category: canonical_site_patch
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1917-01-17
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from saint-louis; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 310. CANONICAL-SITE-PATCH-CBBG-0182891

- Category: canonical_site_patch
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1929-01-30
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from saint-louis; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 311. CANONICAL-SITE-PATCH-CBBG-0182981

- Category: canonical_site_patch
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1937-01-12
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from saint-louis; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 312. CANONICAL-SITE-PATCH-CBBG-0183669

- Category: canonical_site_patch
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1984-02-20
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from saint-louis; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 313. CANONICAL-SITE-PATCH-CBBG-0183737

- Category: canonical_site_patch
- Matchup: loyola-chicago vs saint-louis
- Dates: source [unknown]; canonical 1987-02-12
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from saint-louis; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 314. ACCOMPLISHMENTS-LOYOLA-CHICAGO

- Category: accomplishments
- Matchup: loyola-chicago
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"NATIONAL_CHAMPION","best_finish_year":"1963","conference_regular_season_championships":"8","conference_tournament_championships":"4","final_four_appearances":"2","national_championships":"1","ncaa_tournament_appearances":"8"}`
- Canonical value: `{"best_finish_key":"NATIONAL_CHAMPION","best_finish_year":1963,"final_four_appearances":2,"national_championships":1,"ncaa_tournament_appearances":8}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `PENDING`
- Basis: [required before approval]

### 315. PUBLICATION-LOYOLA-CHICAGO

- Category: publication
- Matchup: loyola-chicago
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 2,727 in-scope source rows; 26 identity reviews; 186 definite and 86 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `PENDING`
- Basis: [required before approval]
