# davidson onboarding review

Generated: 2026-11-02T18:31:52.781044+00:00
Input fingerprint: `b374f14356b86e8c9e5b698603f984416ab6393aea5a90941b1c026d440b35aa`

## Preflight summary

- Source rows: 2,899
- In-scope rows: 2,899
- Pre-cutoff researched rows: 0
- Existing matches: 792
- New canonical games: 2,082
- Identity reviews: 25
- Safe enrichment fields: 1,186
- Discrepancies: 138
- Conditional discrepancies: 67
- Canonical-only site reviews: 0
- Affected existing public programs: alabama, arizona, arizona-state, auburn, baylor, boise-state, boston-college, butler, byu, california, central-connecticut, cincinnati, clemson, creighton, dayton, depaul, duke, fairleigh-dickinson, florida, florida-state, georgetown, georgia, georgia-tech, gonzaga, indiana, iowa, iowa-state, kansas, kansas-state, kentucky, louisville, loyola-chicago, marquette, maryland, mercyhurst, miami, michigan, michigan-state, mississippi-state, missouri, nc-state, nebraska, north-carolina, notre-dame, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, penn-state, pittsburgh, providence, purdue, rutgers, saint-louis, seton-hall, smu, south-carolina, st-john-s, stanford, syracuse, tennessee, texas, texas-a-m, texas-state, texas-tech, ucf, ucla, uconn, utah-state, vanderbilt, villanova, virginia, virginia-tech, wake-forest, washington-state, west-virginia, wisconsin

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. DISCREPANCY-DAV-S1-1908-09-002-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: wake-forest [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 2. DISCREPANCY-DAV-S1-1908-09-003-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 3. DISCREPANCY-DAV-S1-1909-10-001-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs virginia-tech
- Date: 1910-01-13
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: virginia-tech 1910-01-13: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 4. DISCREPANCY-DAV-S1-1909-10-003-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1909-11-02
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: south-carolina 1909-11-02: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 5. DISCREPANCY-DAV-S1-1910-11-001-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: wake-forest [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 6. DISCREPANCY-DAV-S1-1910-11-002-GAME_DATE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1911-02-07; canonical 1911-02-08
- Field: game_date
- Source value: `1911-02-07`
- Canonical value: `1911-02-08`
- Evidence: north-carolina 1911-02-08: 1911-02-08
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 7. DISCREPANCY-DAV-S1-1910-11-002-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1911-02-07; canonical 1911-02-08
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: north-carolina 1911-02-08: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 8. IDENTITY-DAV-S1-1911-12-003

- Category: identity
- Matchup: davidson vs south-carolina
- Dates: source 1911-11-19; canonical 1912-01-19
- Field: game_identity
- Source value: `date=1911-11-19; score=35-33`
- Canonical value: `CBBG-0063418`
- Evidence: CBBG-0063418 1911-1912 1912-01-19 35-33 sources=south-carolina
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 9. CONDITIONAL-DISCREPANCY-DAV-S1-1911-12-003-CBBG-0063418-GAME_DATE

- Category: conditional_discrepancy
- Matchup: davidson vs south-carolina
- Dates: source 1911-11-19; canonical 1912-01-19
- Field: game_date
- Source value: `1911-11-19`
- Canonical value: `1912-01-19`
- Evidence: south-carolina 1912-01-19: 1912-01-19
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0063418`

### 10. CONDITIONAL-DISCREPANCY-DAV-S1-1911-12-003-CBBG-0063418-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs south-carolina
- Dates: source 1911-11-19; canonical 1912-01-19
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: south-carolina 1912-01-19: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0063418`

### 11. IDENTITY-DAV-S1-1912-13-005

- Category: identity
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=-`
- Canonical value: `CBBG-0135484`
- Evidence: CBBG-0135484 1912-1913 [unknown] - sources=nc-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 12. CONDITIONAL-DISCREPANCY-DAV-S1-1912-13-005-CBBG-0135484-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: nc-state [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0135484`

### 13. IDENTITY-DAV-S1-1915-16-006

- Category: identity
- Matchup: davidson vs nc-state
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=30-18`
- Canonical value: `CBBG-0134261;CBBG-0134262`
- Evidence: CBBG-0134261 1915-1916 [unknown] 24-23 sources=nc-state; CBBG-0134262 1915-1916 [unknown] 14-37 sources=nc-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 14. CONDITIONAL-DISCREPANCY-DAV-S1-1915-16-006-CBBG-0134261-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `30-18`
- Canonical value: `24-23`
- Evidence: nc-state [unknown]: 24-23
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134261`

### 15. CONDITIONAL-DISCREPANCY-DAV-S1-1915-16-006-CBBG-0134262-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `30-18`
- Canonical value: `14-37`
- Evidence: nc-state [unknown]: 14-37
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134262`

### 16. CONDITIONAL-DISCREPANCY-DAV-S1-1915-16-006-CBBG-0134262-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134262`

### 17. CONDITIONAL-DISCREPANCY-DAV-S1-1915-16-006-CBBG-0134262-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `davidson`
- Canonical value: `nc-state`
- Evidence: nc-state [unknown]: nc-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134262`

### 18. IDENTITY-DAV-S1-1915-16-012

- Category: identity
- Matchup: davidson vs nc-state
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=14-35`
- Canonical value: `CBBG-0134261;CBBG-0134262`
- Evidence: CBBG-0134261 1915-1916 [unknown] 24-23 sources=nc-state; CBBG-0134262 1915-1916 [unknown] 14-37 sources=nc-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 19. CONDITIONAL-DISCREPANCY-DAV-S1-1915-16-012-CBBG-0134261-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `14-35`
- Canonical value: `24-23`
- Evidence: nc-state [unknown]: 24-23
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134261`

### 20. CONDITIONAL-DISCREPANCY-DAV-S1-1915-16-012-CBBG-0134261-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: nc-state [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134261`

### 21. CONDITIONAL-DISCREPANCY-DAV-S1-1915-16-012-CBBG-0134261-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `nc-state`
- Canonical value: `davidson`
- Evidence: nc-state [unknown]: davidson
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134261`

### 22. CONDITIONAL-DISCREPANCY-DAV-S1-1915-16-012-CBBG-0134262-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `14-35`
- Canonical value: `14-37`
- Evidence: nc-state [unknown]: 14-37
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134262`

### 23. DISCREPANCY-DAV-S1-1915-16-014-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1916-02-16
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: north-carolina 1916-02-16: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 24. DISCREPANCY-DAV-S1-1915-16-020-GAME_DATE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1916-02-26; canonical 1916-02-25
- Field: game_date
- Source value: `1916-02-26`
- Canonical value: `1916-02-25`
- Evidence: north-carolina 1916-02-25: 1916-02-25
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 25. DISCREPANCY-DAV-S1-1915-16-020-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1916-02-26; canonical 1916-02-25
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: north-carolina 1916-02-25: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 26. DISCREPANCY-DAV-S1-1917-18-009-GAME_DATE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1918-02-27; canonical 1918-02-28
- Field: game_date
- Source value: `1918-02-27`
- Canonical value: `1918-02-28`
- Evidence: north-carolina 1918-02-28: 1918-02-28
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 27. DISCREPANCY-DAV-S1-1917-18-011-SCORE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1918-03-02
- Field: score
- Source value: `22-37`
- Canonical value: `24-36`
- Evidence: clemson 1918-03-02: 24-36
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 28. DISCREPANCY-DAV-S1-1918-19-009-GAME_DATE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1919-03-02; canonical 1919-03-01
- Field: game_date
- Source value: `1919-03-02`
- Canonical value: `1919-03-01`
- Evidence: north-carolina 1919-03-01: 1919-03-01
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 29. DISCREPANCY-DAV-S1-1918-19-009-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1919-03-02; canonical 1919-03-01
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: north-carolina 1919-03-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 30. IDENTITY-DAV-S1-1919-20-007

- Category: identity
- Matchup: davidson vs clemson
- Dates: source [unknown]; canonical 1920-02-07
- Field: game_identity
- Source value: `date=[unknown]; score=26-28`
- Canonical value: `CBBG-0128925`
- Evidence: CBBG-0128925 1919-1920 1920-02-07 28-25 sources=clemson
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 31. CONDITIONAL-DISCREPANCY-DAV-S1-1919-20-007-CBBG-0128925-SCORE

- Category: conditional_discrepancy
- Matchup: clemson vs davidson
- Dates: source [unknown]; canonical 1920-02-07
- Field: score
- Source value: `28-26`
- Canonical value: `28-25`
- Evidence: clemson 1920-02-07: 28-25
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0128925`

### 32. DISCREPANCY-DAV-S1-1919-20-008-SCORE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1920-02-07
- Field: score
- Source value: `38-27`
- Canonical value: `28-25`
- Evidence: clemson 1920-02-07: 28-25
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 33. DISCREPANCY-DAV-S1-1919-20-008-SITE_TYPE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1920-02-07
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: clemson 1920-02-07: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 34. DISCREPANCY-DAV-S1-1919-20-012-SCORE

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1920-02-26
- Field: score
- Source value: `17-28`
- Canonical value: `28-18`
- Evidence: south-carolina 1920-02-26: 28-18
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 35. DISCREPANCY-DAV-S1-1919-20-012-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1920-02-26
- Field: result_winner_team_key
- Source value: `south-carolina`
- Canonical value: `davidson`
- Evidence: south-carolina 1920-02-26: davidson
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 36. DISCREPANCY-DAV-S1-1920-21-002-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 37. DISCREPANCY-DAV-S1-1921-22-004-SCORE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1922-02-07
- Field: score
- Source value: `18-22`
- Canonical value: `18-24`
- Evidence: duke 1922-02-07: 18-24
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 38. IDENTITY-DAV-S1-1922-23-003

- Category: identity
- Matchup: davidson vs nc-state
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=21-8`
- Canonical value: `CBBG-0134334;CBBG-0134337`
- Evidence: CBBG-0134334 1922-1923 [unknown] 19-8 sources=nc-state; CBBG-0134337 1922-1923 [unknown] 22-26 sources=nc-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 39. CONDITIONAL-DISCREPANCY-DAV-S1-1922-23-003-CBBG-0134334-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `21-8`
- Canonical value: `19-8`
- Evidence: nc-state [unknown]: 19-8
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134334`

### 40. CONDITIONAL-DISCREPANCY-DAV-S1-1922-23-003-CBBG-0134334-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134334`

### 41. CONDITIONAL-DISCREPANCY-DAV-S1-1922-23-003-CBBG-0134337-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `21-8`
- Canonical value: `22-26`
- Evidence: nc-state [unknown]: 22-26
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134337`

### 42. CONDITIONAL-DISCREPANCY-DAV-S1-1922-23-003-CBBG-0134337-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134337`

### 43. CONDITIONAL-DISCREPANCY-DAV-S1-1922-23-003-CBBG-0134337-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `davidson`
- Canonical value: `nc-state`
- Evidence: nc-state [unknown]: nc-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134337`

### 44. DISCREPANCY-DAV-S1-1922-23-005-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 45. DISCREPANCY-DAV-S1-1922-23-009-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: wake-forest [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 46. IDENTITY-DAV-S1-1922-23-012

- Category: identity
- Matchup: davidson vs wake-forest
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=27-17`
- Canonical value: `CBBG-0127108;CBBG-0127110`
- Evidence: CBBG-0127108 1922-1923 [unknown] 24-29 sources=wake-forest; CBBG-0127110 1922-1923 [unknown] 25-17 sources=wake-forest
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 47. CONDITIONAL-DISCREPANCY-DAV-S1-1922-23-012-CBBG-0127108-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: score
- Source value: `27-17`
- Canonical value: `24-29`
- Evidence: wake-forest [unknown]: 24-29
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127108`

### 48. CONDITIONAL-DISCREPANCY-DAV-S1-1922-23-012-CBBG-0127108-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `davidson`
- Canonical value: `wake-forest`
- Evidence: wake-forest [unknown]: wake-forest
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127108`

### 49. CONDITIONAL-DISCREPANCY-DAV-S1-1922-23-012-CBBG-0127110-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: score
- Source value: `27-17`
- Canonical value: `25-17`
- Evidence: wake-forest [unknown]: 25-17
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127110`

### 50. CONDITIONAL-DISCREPANCY-DAV-S1-1922-23-012-CBBG-0127110-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: wake-forest [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127110`

### 51. DISCREPANCY-DAV-S1-1923-24-007-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 52. IDENTITY-DAV-S1-1923-24-008

- Category: identity
- Matchup: davidson vs florida
- Date: [unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=34-22`
- Canonical value: `CBBG-0017673`
- Evidence: CBBG-0017673 1923-1924 [unknown] 24-22 sources=florida
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 53. CONDITIONAL-DISCREPANCY-DAV-S1-1923-24-008-CBBG-0017673-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs florida
- Date: [unknown]
- Field: score
- Source value: `34-22`
- Canonical value: `24-22`
- Evidence: florida [unknown]: 24-22
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0017673`

### 54. IDENTITY-DAV-S1-1923-24-014

- Category: identity
- Matchup: davidson vs wake-forest
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=16-33`
- Canonical value: `CBBG-0127130;CBBG-0127132`
- Evidence: CBBG-0127130 1923-1924 [unknown] 22-32 sources=wake-forest; CBBG-0127132 1923-1924 [unknown] 16-35 sources=wake-forest
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 55. CONDITIONAL-DISCREPANCY-DAV-S1-1923-24-014-CBBG-0127130-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: score
- Source value: `16-33`
- Canonical value: `22-32`
- Evidence: wake-forest [unknown]: 22-32
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127130`

### 56. CONDITIONAL-DISCREPANCY-DAV-S1-1923-24-014-CBBG-0127130-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: wake-forest [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127130`

### 57. CONDITIONAL-DISCREPANCY-DAV-S1-1923-24-014-CBBG-0127132-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: score
- Source value: `16-33`
- Canonical value: `16-35`
- Evidence: wake-forest [unknown]: 16-35
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127132`

### 58. DISCREPANCY-DAV-S1-1924-25-004-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 59. DISCREPANCY-DAV-S1-1924-25-014-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs georgia-tech
- Date: 1925-02-17
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgia-tech 1925-02-17: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 60. DISCREPANCY-DAV-S1-1925-26-003-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1926-01-08
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke 1926-01-08: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 61. DISCREPANCY-DAV-S1-1925-26-004-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 62. DISCREPANCY-DAV-S1-1925-26-011-SITE_TYPE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1926-02-15
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: clemson 1926-02-15: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 63. DISCREPANCY-DAV-S1-1925-26-014-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 64. DISCREPANCY-DAV-S1-1925-26-015-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 65. DISCREPANCY-DAV-S1-1926-27-009-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 66. DISCREPANCY-DAV-S1-1926-27-018-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 67. DISCREPANCY-DAV-S1-1927-28-002-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1928-01-11
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke 1928-01-11: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 68. DISCREPANCY-DAV-S1-1927-28-015-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1928-02-22
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke 1928-02-22: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 69. IDENTITY-DAV-S1-1928-29-007

- Category: identity
- Matchup: davidson vs virginia-tech
- Dates: source [unknown]; canonical 1929-02-02;1929-02-12
- Field: game_identity
- Source value: `date=[unknown]; score=28-12`
- Canonical value: `CBBG-0135739;CBBG-0135741`
- Evidence: CBBG-0135739 1928-1929 1929-02-02 28-13 sources=virginia-tech; CBBG-0135741 1928-1929 1929-02-12 41-19 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 70. CONDITIONAL-DISCREPANCY-DAV-S1-1928-29-007-CBBG-0135739-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs virginia-tech
- Dates: source [unknown]; canonical 1929-02-02
- Field: score
- Source value: `28-12`
- Canonical value: `28-13`
- Evidence: virginia-tech 1929-02-02: 28-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0135739`

### 71. CONDITIONAL-DISCREPANCY-DAV-S1-1928-29-007-CBBG-0135741-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs virginia-tech
- Dates: source [unknown]; canonical 1929-02-12
- Field: score
- Source value: `28-12`
- Canonical value: `41-19`
- Evidence: virginia-tech 1929-02-12: 41-19
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0135741`

### 72. CONDITIONAL-DISCREPANCY-DAV-S1-1928-29-007-CBBG-0135741-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs virginia-tech
- Dates: source [unknown]; canonical 1929-02-12
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: virginia-tech 1929-02-12: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0135741`

### 73. DISCREPANCY-DAV-S1-1928-29-008-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 74. DISCREPANCY-DAV-S1-1928-29-016-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 75. DISCREPANCY-DAV-S1-1929-30-012-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 76. DISCREPANCY-DAV-S1-1929-30-017-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 77. DISCREPANCY-DAV-S1-1930-31-007-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 78. DISCREPANCY-DAV-S1-1930-31-012-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: duke [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 79. IDENTITY-DAV-S1-1930-31-013

- Category: identity
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=20-22`
- Canonical value: `CBBG-0127231`
- Evidence: CBBG-0127231 1930-1931 [unknown] 22-26 sources=wake-forest
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 80. CONDITIONAL-DISCREPANCY-DAV-S1-1930-31-013-CBBG-0127231-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: score
- Source value: `20-22`
- Canonical value: `22-26`
- Evidence: wake-forest [unknown]: 22-26
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127231`

### 81. DISCREPANCY-DAV-S1-1931-32-005-SCORE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1932-02-01
- Field: score
- Source value: `20-38`
- Canonical value: `20-33`
- Evidence: duke 1932-02-01: 20-33
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 82. DISCREPANCY-DAV-S1-1932-33-012-SCORE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1933-02-07
- Field: score
- Source value: `25-44`
- Canonical value: `28-44`
- Evidence: duke 1933-02-07: 28-44
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 83. IDENTITY-DAV-S1-1932-33-014

- Category: identity
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=39-43`
- Canonical value: `CBBG-0127251`
- Evidence: CBBG-0127251 1932-1933 [unknown] 42-45 sources=wake-forest
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 84. CONDITIONAL-DISCREPANCY-DAV-S1-1932-33-014-CBBG-0127251-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: score
- Source value: `39-43`
- Canonical value: `42-45`
- Evidence: wake-forest [unknown]: 42-45
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127251`

### 85. IDENTITY-DAV-S1-1932-33-017

- Category: identity
- Matchup: davidson vs nc-state
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=23-35`
- Canonical value: `CBBG-0134417;CBBG-0134418`
- Evidence: CBBG-0134417 1932-1933 [unknown] 16-39 sources=nc-state; CBBG-0134418 1932-1933 [unknown] 20-35 sources=nc-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 86. CONDITIONAL-DISCREPANCY-DAV-S1-1932-33-017-CBBG-0134417-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `23-35`
- Canonical value: `16-39`
- Evidence: nc-state [unknown]: 16-39
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134417`

### 87. CONDITIONAL-DISCREPANCY-DAV-S1-1932-33-017-CBBG-0134417-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: nc-state [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134417`

### 88. CONDITIONAL-DISCREPANCY-DAV-S1-1932-33-017-CBBG-0134418-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `23-35`
- Canonical value: `20-35`
- Evidence: nc-state [unknown]: 20-35
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134418`

### 89. DISCREPANCY-DAV-S1-1933-34-005-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1934-01-06
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: north-carolina 1934-01-06: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 90. DISCREPANCY-DAV-S1-1933-34-006-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1934-01-08
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 1934-01-08: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 91. DISCREPANCY-DAV-S1-1933-34-013-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 92. IDENTITY-DAV-S1-1933-34-014

- Category: identity
- Matchup: davidson vs nc-state
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=23-36`
- Canonical value: `CBBG-0134420;CBBG-0134423`
- Evidence: CBBG-0134420 1933-1934 [unknown] 29-32 sources=nc-state; CBBG-0134423 1933-1934 [unknown] 26-50 sources=nc-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 93. CONDITIONAL-DISCREPANCY-DAV-S1-1933-34-014-CBBG-0134420-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `23-36`
- Canonical value: `29-32`
- Evidence: nc-state [unknown]: 29-32
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134420`

### 94. CONDITIONAL-DISCREPANCY-DAV-S1-1933-34-014-CBBG-0134423-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `23-36`
- Canonical value: `26-50`
- Evidence: nc-state [unknown]: 26-50
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134423`

### 95. CONDITIONAL-DISCREPANCY-DAV-S1-1933-34-014-CBBG-0134423-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134423`

### 96. DISCREPANCY-DAV-S1-1935-36-005-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1936-01-08
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 1936-01-08: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 97. DISCREPANCY-DAV-S1-1935-36-006-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 98. IDENTITY-DAV-S1-1935-36-012

- Category: identity
- Matchup: davidson vs north-carolina
- Dates: source 1936-02-12; canonical 1936-01-04;1936-02-29
- Field: game_identity
- Source value: `date=1936-02-12; score=16-31`
- Canonical value: `CBBG-0095043;CBBG-0095058`
- Evidence: CBBG-0095043 1935-1936 1936-01-04 27-45 sources=north-carolina; CBBG-0095058 1935-1936 1936-02-29 16-31 sources=north-carolina
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 99. CONDITIONAL-DISCREPANCY-DAV-S1-1935-36-012-CBBG-0095043-GAME_DATE

- Category: conditional_discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1936-02-12; canonical 1936-01-04
- Field: game_date
- Source value: `1936-02-12`
- Canonical value: `1936-01-04`
- Evidence: north-carolina 1936-01-04: 1936-01-04
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0095043`

### 100. CONDITIONAL-DISCREPANCY-DAV-S1-1935-36-012-CBBG-0095043-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1936-02-12; canonical 1936-01-04
- Field: score
- Source value: `16-31`
- Canonical value: `27-45`
- Evidence: north-carolina 1936-01-04: 27-45
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0095043`

### 101. CONDITIONAL-DISCREPANCY-DAV-S1-1935-36-012-CBBG-0095043-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1936-02-12; canonical 1936-01-04
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: north-carolina 1936-01-04: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0095043`

### 102. CONDITIONAL-DISCREPANCY-DAV-S1-1935-36-012-CBBG-0095058-GAME_DATE

- Category: conditional_discrepancy
- Matchup: davidson vs north-carolina
- Dates: source 1936-02-12; canonical 1936-02-29
- Field: game_date
- Source value: `1936-02-12`
- Canonical value: `1936-02-29`
- Evidence: north-carolina 1936-02-29: 1936-02-29
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0095058`

### 103. DISCREPANCY-DAV-S1-1935-36-013-SCORE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1936-02-13
- Field: score
- Source value: `33-37`
- Canonical value: `33-36`
- Evidence: duke 1936-02-13: 33-36
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 104. DISCREPANCY-DAV-S1-1936-37-004-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1937-01-06
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 1937-01-06: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 105. DISCREPANCY-DAV-S1-1936-37-007-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 106. DISCREPANCY-DAV-S1-1936-37-009-GAME_DATE

- Category: discrepancy
- Matchup: davidson vs duke
- Dates: source 1937-02-01; canonical 1937-02-02
- Field: game_date
- Source value: `1937-02-01`
- Canonical value: `1937-02-02`
- Evidence: duke 1937-02-02: 1937-02-02
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 107. IDENTITY-DAV-S1-1936-37-016

- Category: identity
- Matchup: davidson vs wake-forest
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=43-31`
- Canonical value: `CBBG-0127303;CBBG-0127305`
- Evidence: CBBG-0127303 1936-1937 [unknown] 43-32 sources=wake-forest; CBBG-0127305 1936-1937 [unknown] 31-42 sources=wake-forest
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 108. CONDITIONAL-DISCREPANCY-DAV-S1-1936-37-016-CBBG-0127303-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: score
- Source value: `43-31`
- Canonical value: `43-32`
- Evidence: wake-forest [unknown]: 43-32
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127303`

### 109. CONDITIONAL-DISCREPANCY-DAV-S1-1936-37-016-CBBG-0127305-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: score
- Source value: `43-31`
- Canonical value: `31-42`
- Evidence: wake-forest [unknown]: 31-42
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127305`

### 110. CONDITIONAL-DISCREPANCY-DAV-S1-1936-37-016-CBBG-0127305-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: wake-forest [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127305`

### 111. CONDITIONAL-DISCREPANCY-DAV-S1-1936-37-016-CBBG-0127305-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `davidson`
- Canonical value: `wake-forest`
- Evidence: wake-forest [unknown]: wake-forest
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127305`

### 112. IDENTITY-DAV-S1-1936-37-020

- Category: identity
- Matchup: davidson vs wake-forest
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=33-44`
- Canonical value: `CBBG-0127303;CBBG-0127305`
- Evidence: CBBG-0127303 1936-1937 [unknown] 43-32 sources=wake-forest; CBBG-0127305 1936-1937 [unknown] 31-42 sources=wake-forest
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 113. CONDITIONAL-DISCREPANCY-DAV-S1-1936-37-020-CBBG-0127303-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: score
- Source value: `33-44`
- Canonical value: `43-32`
- Evidence: wake-forest [unknown]: 43-32
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127303`

### 114. CONDITIONAL-DISCREPANCY-DAV-S1-1936-37-020-CBBG-0127303-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: wake-forest [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127303`

### 115. CONDITIONAL-DISCREPANCY-DAV-S1-1936-37-020-CBBG-0127303-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `wake-forest`
- Canonical value: `davidson`
- Evidence: wake-forest [unknown]: davidson
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127303`

### 116. CONDITIONAL-DISCREPANCY-DAV-S1-1936-37-020-CBBG-0127305-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: score
- Source value: `33-44`
- Canonical value: `31-42`
- Evidence: wake-forest [unknown]: 31-42
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0127305`

### 117. DISCREPANCY-DAV-S1-1937-38-005-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1938-01-05
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 1938-01-05: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 118. DISCREPANCY-DAV-S1-1937-38-007-SCORE

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1938-01-11
- Field: score
- Source value: `37-26`
- Canonical value: `36-27`
- Evidence: south-carolina 1938-01-11: 36-27
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 119. IDENTITY-DAV-S1-1937-38-009

- Category: identity
- Matchup: davidson vs clemson
- Dates: source [unknown]; canonical 1938-01-08;1938-02-21
- Field: game_identity
- Source value: `date=[unknown]; score=29-39`
- Canonical value: `CBBG-0129133;CBBG-0129141`
- Evidence: CBBG-0129133 1937-1938 1938-01-08 41-26 sources=clemson; CBBG-0129141 1937-1938 1938-02-21 35-34 sources=clemson
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 120. CONDITIONAL-DISCREPANCY-DAV-S1-1937-38-009-CBBG-0129133-SCORE

- Category: conditional_discrepancy
- Matchup: clemson vs davidson
- Dates: source [unknown]; canonical 1938-01-08
- Field: score
- Source value: `39-29`
- Canonical value: `41-26`
- Evidence: clemson 1938-01-08: 41-26
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0129133`

### 121. CONDITIONAL-DISCREPANCY-DAV-S1-1937-38-009-CBBG-0129141-SCORE

- Category: conditional_discrepancy
- Matchup: clemson vs davidson
- Dates: source [unknown]; canonical 1938-02-21
- Field: score
- Source value: `39-29`
- Canonical value: `35-34`
- Evidence: clemson 1938-02-21: 35-34
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0129141`

### 122. DISCREPANCY-DAV-S1-1937-38-010-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 123. DISCREPANCY-DAV-S1-1937-38-015-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: wake-forest [unknown]: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 124. DISCREPANCY-DAV-S1-1937-38-019-SITE_TYPE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1938-02-21
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: clemson 1938-02-21: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 125. DISCREPANCY-DAV-S1-1937-38-022-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs wake-forest
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: wake-forest [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 126. DISCREPANCY-DAV-S1-1938-39-010-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1939-01-05
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 1939-01-05: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 127. DISCREPANCY-DAV-S1-1938-39-015-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 128. DISCREPANCY-DAV-S1-1938-39-018-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1939-02-07
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: north-carolina 1939-02-07: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 129. DISCREPANCY-DAV-S1-1938-39-020-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs virginia-tech
- Date: 1939-02-11
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1939-02-11: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 130. IDENTITY-DAV-S1-1939-40-010

- Category: identity
- Matchup: davidson vs nc-state
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=41-52`
- Canonical value: `CBBG-0134467;CBBG-0134470`
- Evidence: CBBG-0134467 1939-1940 [unknown] 53-41 sources=nc-state; CBBG-0134470 1939-1940 [unknown] 27-40 sources=nc-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 131. CONDITIONAL-DISCREPANCY-DAV-S1-1939-40-010-CBBG-0134467-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `41-52`
- Canonical value: `53-41`
- Evidence: nc-state [unknown]: 53-41
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134467`

### 132. CONDITIONAL-DISCREPANCY-DAV-S1-1939-40-010-CBBG-0134467-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134467`

### 133. CONDITIONAL-DISCREPANCY-DAV-S1-1939-40-010-CBBG-0134467-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `nc-state`
- Canonical value: `davidson`
- Evidence: nc-state [unknown]: davidson
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134467`

### 134. CONDITIONAL-DISCREPANCY-DAV-S1-1939-40-010-CBBG-0134470-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `41-52`
- Canonical value: `27-40`
- Evidence: nc-state [unknown]: 27-40
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134470`

### 135. CONDITIONAL-DISCREPANCY-DAV-S1-1939-40-010-CBBG-0134470-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134470`

### 136. DISCREPANCY-DAV-S1-1939-40-015-SCORE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1940-02-07
- Field: score
- Source value: `31-44`
- Canonical value: `28-41`
- Evidence: north-carolina 1940-02-07: 28-41
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 137. DISCREPANCY-DAV-S1-1940-41-007-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1941-01-06
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 1941-01-06: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 138. DISCREPANCY-DAV-S1-1940-41-012-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs virginia-tech
- Date: 1941-02-01
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1941-02-01: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 139. DISCREPANCY-DAV-S1-1940-41-022-SCORE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1941-02-22
- Field: score
- Source value: `31-39`
- Canonical value: `30-39`
- Evidence: north-carolina 1941-02-22: 30-39
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 140. DISCREPANCY-DAV-S1-1940-41-022-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1941-02-22
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: north-carolina 1941-02-22: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 141. DISCREPANCY-DAV-S1-1941-42-005-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1941-12-13
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: north-carolina 1941-12-13: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 142. DISCREPANCY-DAV-S1-1941-42-009-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1942-01-07
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 1942-01-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 143. IDENTITY-DAV-S1-1941-42-010

- Category: identity
- Matchup: davidson vs nc-state
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=48-71`
- Canonical value: `CBBG-0134483;CBBG-0134486`
- Evidence: CBBG-0134483 1941-1942 [unknown] 36-71 sources=nc-state; CBBG-0134486 1941-1942 [unknown] 43-60 sources=nc-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 144. CONDITIONAL-DISCREPANCY-DAV-S1-1941-42-010-CBBG-0134483-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `48-71`
- Canonical value: `36-71`
- Evidence: nc-state [unknown]: 36-71
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134483`

### 145. CONDITIONAL-DISCREPANCY-DAV-S1-1941-42-010-CBBG-0134483-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134483`

### 146. CONDITIONAL-DISCREPANCY-DAV-S1-1941-42-010-CBBG-0134486-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: score
- Source value: `48-71`
- Canonical value: `43-60`
- Evidence: nc-state [unknown]: 43-60
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134486`

### 147. CONDITIONAL-DISCREPANCY-DAV-S1-1941-42-010-CBBG-0134486-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134486`

### 148. DISCREPANCY-DAV-S1-1942-43-006-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 149. DISCREPANCY-DAV-S1-1942-43-012-SCORE

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1943-02-04
- Field: score
- Source value: `54-64`
- Canonical value: `54-68`
- Evidence: south-carolina 1943-02-04: 54-68
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 150. DISCREPANCY-DAV-S1-1942-43-012-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1943-02-04
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: south-carolina 1943-02-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 151. DISCREPANCY-DAV-S1-1942-43-015-SCORE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1943-02-12
- Field: score
- Source value: `27-53`
- Canonical value: `27-50`
- Evidence: north-carolina 1943-02-12: 27-50
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 152. DISCREPANCY-DAV-S1-1942-43-015-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1943-02-12
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: north-carolina 1943-02-12: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 153. DISCREPANCY-DAV-S1-1942-43-016-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 154. DISCREPANCY-DAV-S1-1942-43-017-SCORE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1943-02-16
- Field: score
- Source value: `41-53`
- Canonical value: `31-53`
- Evidence: clemson 1943-02-16: 31-53
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 155. DISCREPANCY-DAV-S1-1942-43-022-SITE_TYPE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1943-02-27
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: clemson 1943-02-27: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 156. DISCREPANCY-DAV-S1-1943-44-008-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1944-01-08
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: north-carolina 1944-01-08: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 157. DISCREPANCY-DAV-S1-1943-44-019-SCORE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1944-02-16
- Field: score
- Source value: `38-42`
- Canonical value: `40-42`
- Evidence: clemson 1944-02-16: 40-42
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 158. DISCREPANCY-DAV-S1-1943-44-020-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 159. DISCREPANCY-DAV-S1-1943-44-021-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 160. DISCREPANCY-DAV-S1-1944-45-004-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1945-01-10
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: north-carolina 1945-01-10: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 161. DISCREPANCY-DAV-S1-1944-45-006-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 162. DISCREPANCY-DAV-S1-1945-46-006-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1946-01-05
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 1946-01-05: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 163. DISCREPANCY-DAV-S1-1945-46-020-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 164. DISCREPANCY-DAV-S1-1946-47-007-SCORE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1947-01-07
- Field: score
- Source value: `47-55`
- Canonical value: `48-55`
- Evidence: duke 1947-01-07: 48-55
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 165. DISCREPANCY-DAV-S1-1946-47-007-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1947-01-07
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 1947-01-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 166. DISCREPANCY-DAV-S1-1946-47-011-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1947-01-28
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: south-carolina 1947-01-28: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 167. IDENTITY-DAV-S1-1946-47-014

- Category: identity
- Matchup: davidson vs south-carolina
- Dates: source 1947-02-03; canonical 1947-01-28;1947-02-01
- Field: game_identity
- Source value: `date=1947-02-03; score=52-50`
- Canonical value: `CBBG-0063964;CBBG-0063966`
- Evidence: CBBG-0063964 1946-1947 1947-01-28 74-43 sources=south-carolina; CBBG-0063966 1946-1947 1947-02-01 52-50 sources=south-carolina
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 168. CONDITIONAL-DISCREPANCY-DAV-S1-1946-47-014-CBBG-0063964-GAME_DATE

- Category: conditional_discrepancy
- Matchup: davidson vs south-carolina
- Dates: source 1947-02-03; canonical 1947-01-28
- Field: game_date
- Source value: `1947-02-03`
- Canonical value: `1947-01-28`
- Evidence: south-carolina 1947-01-28: 1947-01-28
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0063964`

### 169. CONDITIONAL-DISCREPANCY-DAV-S1-1946-47-014-CBBG-0063964-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs south-carolina
- Dates: source 1947-02-03; canonical 1947-01-28
- Field: score
- Source value: `52-50`
- Canonical value: `74-43`
- Evidence: south-carolina 1947-01-28: 74-43
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0063964`

### 170. CONDITIONAL-DISCREPANCY-DAV-S1-1946-47-014-CBBG-0063964-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs south-carolina
- Dates: source 1947-02-03; canonical 1947-01-28
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: south-carolina 1947-01-28: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0063964`

### 171. CONDITIONAL-DISCREPANCY-DAV-S1-1946-47-014-CBBG-0063966-GAME_DATE

- Category: conditional_discrepancy
- Matchup: davidson vs south-carolina
- Dates: source 1947-02-03; canonical 1947-02-01
- Field: game_date
- Source value: `1947-02-03`
- Canonical value: `1947-02-01`
- Evidence: south-carolina 1947-02-01: 1947-02-01
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0063966`

### 172. DISCREPANCY-DAV-S1-1946-47-018-SITE_TYPE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1947-02-14
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: clemson 1947-02-14: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 173. DISCREPANCY-DAV-S1-1946-47-020-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1947-02-18
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: north-carolina 1947-02-18: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 174. DISCREPANCY-DAV-S1-1947-48-009-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1948-01-06
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 1948-01-06: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 175. DISCREPANCY-DAV-S1-1947-48-010-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: 1948-01-09
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: nc-state 1948-01-09: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 176. DISCREPANCY-DAV-S1-1947-48-023-SCORE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1948-02-24
- Field: score
- Source value: `46-52`
- Canonical value: `45-52`
- Evidence: north-carolina 1948-02-24: 45-52
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 177. DISCREPANCY-DAV-S1-1947-48-023-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 1948-02-24
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: north-carolina 1948-02-24: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 178. DISCREPANCY-DAV-S1-1947-48-028-SCORE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1948-03-05
- Field: score
- Source value: `39-53`
- Canonical value: `37-53`
- Evidence: duke 1948-03-05: 37-53
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 179. DISCREPANCY-DAV-S1-1948-49-008-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1949-01-08
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: south-carolina 1949-01-08: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 180. DISCREPANCY-DAV-S1-1949-50-003-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs virginia-tech
- Date: 1949-12-10
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1949-12-10: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 181. DISCREPANCY-DAV-S1-1949-50-010-SCORE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: 1950-01-10
- Field: score
- Source value: `35-44`
- Canonical value: `38-44`
- Evidence: nc-state 1950-01-10: 38-44
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 182. DISCREPANCY-DAV-S1-1949-50-010-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: 1950-01-10
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: nc-state 1950-01-10: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 183. DISCREPANCY-DAV-S1-1950-51-016-SCORE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1951-01-27
- Field: score
- Source value: `55-56`
- Canonical value: `74-62`
- Evidence: clemson 1951-01-27: 74-62
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 184. DISCREPANCY-DAV-S1-1950-51-016-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1951-01-27
- Field: result_winner_team_key
- Source value: `davidson`
- Canonical value: `clemson`
- Evidence: clemson 1951-01-27: clemson
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 185. DISCREPANCY-DAV-S1-1950-51-022-SCORE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1951-02-09
- Field: score
- Source value: `74-62`
- Canonical value: `55-56`
- Evidence: clemson 1951-02-09: 55-56
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 186. DISCREPANCY-DAV-S1-1950-51-022-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1951-02-09
- Field: result_winner_team_key
- Source value: `clemson`
- Canonical value: `davidson`
- Evidence: clemson 1951-02-09: davidson
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 187. DISCREPANCY-DAV-S1-1951-52-006-GAME_DATE

- Category: discrepancy
- Matchup: auburn vs davidson
- Dates: source 1951-12-27; canonical 1951-12-28
- Field: game_date
- Source value: `1951-12-27`
- Canonical value: `1951-12-28`
- Evidence: auburn 1951-12-28: 1951-12-28
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 188. DISCREPANCY-DAV-S1-1951-52-016-GAME_DATE

- Category: discrepancy
- Matchup: davidson vs wake-forest
- Dates: source 1952-02-05; canonical 1952-02-06
- Field: game_date
- Source value: `1952-02-05`
- Canonical value: `1952-02-06`
- Evidence: wake-forest 1952-02-06: 1952-02-06
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 189. DISCREPANCY-DAV-S1-1952-53-020-GAME_DATE

- Category: discrepancy
- Matchup: davidson vs duke
- Dates: source 1953-02-24; canonical 1953-02-23
- Field: game_date
- Source value: `1953-02-24`
- Canonical value: `1953-02-23`
- Evidence: duke 1953-02-23: 1953-02-23
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 190. DISCREPANCY-DAV-S1-1954-55-013-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs wake-forest
- Date: 1955-01-31
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: wake-forest 1955-01-31: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 191. DISCREPANCY-DAV-S1-1955-56-013-SCORE

- Category: discrepancy
- Matchup: davidson vs virginia-tech
- Date: 1956-01-09
- Field: score
- Source value: `63-89`
- Canonical value: `73-89`
- Evidence: virginia-tech 1956-01-09: 73-89
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 192. DISCREPANCY-DAV-S1-1957-58-001-SCORE

- Category: discrepancy
- Matchup: davidson vs wake-forest
- Date: 1957-12-02
- Field: score
- Source value: `61-68`
- Canonical value: `61-69`
- Evidence: wake-forest 1957-12-02: 61-69
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 193. DISCREPANCY-DAV-S1-1957-58-015-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs virginia-tech
- Date: 1958-02-01
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: virginia-tech 1958-02-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 194. DISCREPANCY-DAV-S1-1958-59-010-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1958-12-29
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: south-carolina 1958-12-29: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 195. DISCREPANCY-DAV-S1-1961-62-002-SCORE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1961-12-05
- Field: score
- Source value: `72-115`
- Canonical value: `72-117`
- Evidence: duke 1961-12-05: 72-117
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 196. DISCREPANCY-DAV-S1-1961-62-008-SITE_TYPE

- Category: discrepancy
- Matchup: alabama vs davidson
- Date: 1961-12-22
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: alabama 1961-12-22: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 197. DISCREPANCY-DAV-S1-1963-64-022-SCORE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1964-02-15
- Field: score
- Source value: `78-85`
- Canonical value: `75-82`
- Evidence: duke 1964-02-15: 75-82
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 198. DISCREPANCY-DAV-S1-1964-65-014-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs west-virginia
- Date: 1965-01-14
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: west-virginia 1965-01-14: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 199. DISCREPANCY-DAV-S1-1965-66-017-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs west-virginia
- Date: 1966-02-02
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: west-virginia 1966-02-02: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 200. DISCREPANCY-DAV-S1-1969-70-005-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs georgia
- Date: 1969-12-22
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: georgia 1969-12-22: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 201. DISCREPANCY-DAV-S1-1971-72-001-SCORE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1971-12-04
- Field: score
- Source value: `65-75`
- Canonical value: `65-76`
- Evidence: clemson 1971-12-04: 65-76
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 202. DISCREPANCY-DAV-S1-1971-72-001-SITE_TYPE

- Category: discrepancy
- Matchup: clemson vs davidson
- Date: 1971-12-04
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: clemson 1971-12-04: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 203. DISCREPANCY-DAV-S1-1973-74-008-SCORE

- Category: discrepancy
- Matchup: davidson vs loyola-chicago
- Date: 1973-12-28
- Field: score
- Source value: `98-83`
- Canonical value: `98-82`
- Evidence: loyola-chicago 1973-12-28: 98-82
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 204. DISCREPANCY-DAV-S1-1973-74-008-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs loyola-chicago
- Date: 1973-12-28
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: loyola-chicago 1973-12-28: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 205. DISCREPANCY-DAV-S1-1975-76-011-SCORE

- Category: discrepancy
- Matchup: davidson vs virginia
- Date: 1976-01-05
- Field: score
- Source value: `51-52`
- Canonical value: `51-72`
- Evidence: virginia 1976-01-05: 51-72
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 206. DISCREPANCY-DAV-S1-1975-76-017-SCORE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 1976-01-27
- Field: score
- Source value: `79-84`
- Canonical value: `79-94`
- Evidence: duke 1976-01-27: 79-94
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 207. DISCREPANCY-DAV-S1-1979-80-023-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1980-02-09
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: south-carolina 1980-02-09: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 208. DISCREPANCY-DAV-S1-1982-83-004-SCORE

- Category: discrepancy
- Matchup: davidson vs wake-forest
- Date: 1982-12-07
- Field: score
- Source value: `61-81`
- Canonical value: `62-81`
- Evidence: wake-forest 1982-12-07: 62-81
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 209. DISCREPANCY-DAV-S1-1988-89-001-SCORE

- Category: discrepancy
- Matchup: davidson vs texas-state
- Date: 1988-11-25
- Field: score
- Source value: `57-53`
- Canonical value: `57-55`
- Evidence: texas-state 1988-11-25: 57-55
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 210. DISCREPANCY-DAV-S1-1994-95-007-SCORE

- Category: discrepancy
- Matchup: davidson vs seton-hall
- Date: 1994-12-22
- Field: score
- Source value: `65-73`
- Canonical value: `66-73`
- Evidence: seton-hall 1994-12-22: 66-73
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 211. DISCREPANCY-DAV-S1-1995-96-005-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: 1995-12-09
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state 1995-12-09: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 212. DISCREPANCY-DAV-S1-1995-96-030-SCORE

- Category: discrepancy
- Matchup: davidson vs south-carolina
- Date: 1996-03-13
- Field: score
- Source value: `79-100`
- Canonical value: `73-100`
- Evidence: south-carolina 1996-03-13: 73-100
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 213. DISCREPANCY-DAV-S1-1996-97-001-SCORE

- Category: discrepancy
- Matchup: davidson vs fairleigh-dickinson
- Date: 1996-11-23
- Field: score
- Source value: `87-75`
- Canonical value: `87-73`
- Evidence: fairleigh-dickinson 1996-11-23: 87-73
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 214. IDENTITY-DAV-S1-2001-02-009

- Category: identity
- Matchup: davidson vs georgia-tech
- Dates: source 2001-12-19; canonical 2001-12-17
- Field: game_identity
- Source value: `date=2001-12-19; score=69-83`
- Canonical value: `CBBG-0133841`
- Evidence: CBBG-0133841 2001-2002 2001-12-17 69-83 sources=georgia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 215. CONDITIONAL-DISCREPANCY-DAV-S1-2001-02-009-CBBG-0133841-GAME_DATE

- Category: conditional_discrepancy
- Matchup: davidson vs georgia-tech
- Dates: source 2001-12-19; canonical 2001-12-17
- Field: game_date
- Source value: `2001-12-19`
- Canonical value: `2001-12-17`
- Evidence: georgia-tech 2001-12-17: 2001-12-17
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0133841`

### 216. DISCREPANCY-DAV-S1-2007-08-010-SCORE

- Category: discrepancy
- Matchup: davidson vs nc-state
- Date: 2007-12-21
- Field: score
- Source value: `65-66`
- Canonical value: `66-67`
- Evidence: nc-state 2007-12-21: 66-67
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 217. DISCREPANCY-DAV-S1-2009-10-009-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs gonzaga
- Date: 2009-12-12
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: gonzaga 2009-12-12: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 218. DISCREPANCY-DAV-S1-2011-12-010-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs kansas
- Date: 2011-12-19
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: kansas 2011-12-19: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 219. IDENTITY-DAV-S1-2012-13-004

- Category: identity
- Matchup: davidson vs vanderbilt
- Dates: source 2012-11-02; canonical 2012-11-22
- Field: game_identity
- Source value: `date=2012-11-02; score=75-62`
- Canonical value: `CBBG-0024666`
- Evidence: CBBG-0024666 2012-2013 2012-11-22 75-62 sources=vanderbilt
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 220. CONDITIONAL-DISCREPANCY-DAV-S1-2012-13-004-CBBG-0024666-GAME_DATE

- Category: conditional_discrepancy
- Matchup: davidson vs vanderbilt
- Dates: source 2012-11-02; canonical 2012-11-22
- Field: game_date
- Source value: `2012-11-02`
- Canonical value: `2012-11-22`
- Evidence: vanderbilt 2012-11-22: 2012-11-22
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0024666`

### 221. DISCREPANCY-DAV-S1-2012-13-013-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs duke
- Date: 2013-01-02
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: duke 2013-01-02: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 222. DISCREPANCY-DAV-S1-2014-15-003-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 2014-11-22
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: north-carolina 2014-11-22: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 223. IDENTITY-DAV-S1-2014-15-014

- Category: identity
- Matchup: davidson vs saint-louis
- Dates: source 2014-10-10; canonical 2015-01-10
- Field: game_identity
- Source value: `date=2014-10-10; score=89-54`
- Canonical value: `CBBG-0184319`
- Evidence: CBBG-0184319 2014-2015 2015-01-10 89-54 sources=saint-louis
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 224. CONDITIONAL-DISCREPANCY-DAV-S1-2014-15-014-CBBG-0184319-GAME_DATE

- Category: conditional_discrepancy
- Matchup: davidson vs saint-louis
- Dates: source 2014-10-10; canonical 2015-01-10
- Field: game_date
- Source value: `2014-10-10`
- Canonical value: `2015-01-10`
- Evidence: saint-louis 2015-01-10: 2015-01-10
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0184319`

### 225. IDENTITY-DAV-S1-2014-15-017

- Category: identity
- Matchup: davidson vs dayton
- Dates: source 2014-10-20; canonical 2015-01-20
- Field: game_identity
- Source value: `date=2014-10-20; score=77-60`
- Canonical value: `CBBG-0188411`
- Evidence: CBBG-0188411 2014-2015 2015-01-20 77-60 sources=dayton
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 226. CONDITIONAL-DISCREPANCY-DAV-S1-2014-15-017-CBBG-0188411-GAME_DATE

- Category: conditional_discrepancy
- Matchup: davidson vs dayton
- Dates: source 2014-10-20; canonical 2015-01-20
- Field: game_date
- Source value: `2014-10-20`
- Canonical value: `2015-01-20`
- Evidence: dayton 2015-01-20: 2015-01-20
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0188411`

### 227. DISCREPANCY-DAV-S1-2016-17-009-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs kansas
- Date: 2016-12-17
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: kansas 2016-12-17: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 228. DISCREPANCY-DAV-S1-2017-18-006-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs north-carolina
- Date: 2017-12-01
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: north-carolina 2017-12-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 229. DISCREPANCY-DAV-S1-2019-20-005-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs wake-forest
- Date: 2019-11-22
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: wake-forest 2019-11-22: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 230. DISCREPANCY-DAV-S1-2021-22-011-SITE_TYPE

- Category: discrepancy
- Matchup: alabama vs davidson
- Date: 2021-12-21
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: alabama 2021-12-21: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 231. ACCOMPLISHMENTS-DAVIDSON

- Category: accomplishments
- Matchup: davidson
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"ELITE_EIGHT","best_finish_year":"2008","conference_regular_season_championships":"25","conference_tournament_championships":"13","final_four_appearances":"0","national_championships":"0","ncaa_tournament_appearances":"15"}`
- Canonical value: `{"best_finish_key":"ELITE_EIGHT","best_finish_year":2008,"final_four_appearances":0,"national_championships":0,"ncaa_tournament_appearances":15}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `PENDING`
- Basis: [required before approval]

### 232. PUBLICATION-DAVIDSON

- Category: publication
- Matchup: davidson
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 2,899 in-scope source rows; 25 identity reviews; 138 definite and 67 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `PENDING`
- Basis: [required before approval]
