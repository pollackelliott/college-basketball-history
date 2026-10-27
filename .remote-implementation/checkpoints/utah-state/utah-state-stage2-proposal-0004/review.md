# utah-state onboarding review

Generated: 2026-10-27T20:01:34.892983+00:00
Input fingerprint: `adaafb9470aab7013b8ec0b2dc9dd24bfd9e6f4609d5e49948b35f1c309b8401`

## Preflight summary

- Source rows: 2,964
- In-scope rows: 2,964
- Pre-cutoff researched rows: 0
- Existing matches: 749
- New canonical games: 2,205
- Identity reviews: 10
- Safe enrichment fields: 1,513
- Discrepancies: 109
- Conditional discrepancies: 44
- Canonical-only site reviews: 1
- Affected existing public programs: arizona, arizona-state, arkansas, baylor, boise-state, boston-college, butler, byu, california, clemson, colorado, creighton, depaul, duke, fairleigh-dickinson, florida, florida-state, georgetown, georgia, georgia-tech, gonzaga, houston, illinois, indiana, iowa, iowa-state, kansas, kansas-state, kentucky, long-island-university, lsu, marquette, maryland, michigan, michigan-state, minnesota, mississippi-state, missouri, nc-state, nebraska, northwestern, notre-dame, ohio-state, oklahoma, oregon, oregon-state, pittsburgh, providence, purdue, rutgers, seton-hall, smu, stanford, tcu, tennessee, texas, texas-a-m, texas-tech, ucf, ucla, uconn, usc, utah, vanderbilt, villanova, washington, washington-state, wisconsin, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. DISCREPANCY-UST-S1-00026-GAME_DATE

- Category: discrepancy
- Matchup: byu vs utah-state
- Dates: source 1908-02-02; canonical 1908-02-01
- Field: game_date
- Source value: `1908-02-02`
- Canonical value: `1908-02-01`
- Evidence: byu 1908-02-01: 1908-02-01
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 2. DISCREPANCY-UST-S1-00033-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1909-02-04
- Field: score
- Source value: `32-13`
- Canonical value: `33-13`
- Evidence: utah 1909-02-04: 33-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 3. DISCREPANCY-UST-S1-00033-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1909-02-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1909-02-04: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 4. DISCREPANCY-UST-S1-00037-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1909-02-19
- Field: score
- Source value: `37-18`
- Canonical value: `37-19`
- Evidence: utah 1909-02-19: 37-19
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 5. DISCREPANCY-UST-S1-00037-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1909-02-19
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: utah 1909-02-19: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 6. DISCREPANCY-UST-S1-00040-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1910-01-15
- Field: score
- Source value: `46-20`
- Canonical value: `40-20`
- Evidence: byu 1910-01-15: 40-20
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 7. DISCREPANCY-UST-S1-00040-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1910-01-15
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu 1910-01-15: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 8. DISCREPANCY-UST-S1-00045-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1910-02-17
- Field: score
- Source value: `69-15`
- Canonical value: `63-20`
- Evidence: utah 1910-02-17: 63-20
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 9. DISCREPANCY-UST-S1-00045-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1910-02-17
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1910-02-17: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 10. IDENTITY-UST-S1-02962

- Category: identity
- Matchup: utah-state vs utah
- Dates: source [unknown]; canonical 1910-02-17;1910-02-26
- Field: game_identity
- Source value: `date=[unknown]; score=21-38`
- Canonical value: `CBBG-0104045;CBBG-0104048`
- Evidence: CBBG-0104045 1909-1910 1910-02-17 63-20 sources=utah; CBBG-0104048 1909-1910 1910-02-26 38-18 sources=utah
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 11. CONDITIONAL-DISCREPANCY-UST-S1-02962-CBBG-0104045-SCORE

- Category: conditional_discrepancy
- Matchup: utah vs utah-state
- Dates: source [unknown]; canonical 1910-02-17
- Field: score
- Source value: `38-21`
- Canonical value: `63-20`
- Evidence: utah 1910-02-17: 63-20
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0104045`

### 12. CONDITIONAL-DISCREPANCY-UST-S1-02962-CBBG-0104045-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: utah vs utah-state
- Dates: source [unknown]; canonical 1910-02-17
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1910-02-17: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0104045`

### 13. CONDITIONAL-DISCREPANCY-UST-S1-02962-CBBG-0104048-SCORE

- Category: conditional_discrepancy
- Matchup: utah vs utah-state
- Dates: source [unknown]; canonical 1910-02-26
- Field: score
- Source value: `38-21`
- Canonical value: `38-18`
- Evidence: utah 1910-02-26: 38-18
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0104048`

### 14. CONDITIONAL-DISCREPANCY-UST-S1-02962-CBBG-0104048-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: utah vs utah-state
- Dates: source [unknown]; canonical 1910-02-26
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: utah 1910-02-26: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0104048`

### 15. DISCREPANCY-UST-S1-00052-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1911-02-17
- Field: score
- Source value: `46-33`
- Canonical value: `45-32`
- Evidence: utah 1911-02-17: 45-32
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 16. DISCREPANCY-UST-S1-00052-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1911-02-17
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1911-02-17: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 17. DISCREPANCY-UST-S1-00068-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1913-02-28
- Field: score
- Source value: `20-31`
- Canonical value: `42-31`
- Evidence: utah 1913-02-28: 42-31
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 18. DISCREPANCY-UST-S1-00068-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1913-02-28
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1913-02-28: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 19. DISCREPANCY-UST-S1-00068-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1913-02-28
- Field: result_winner_team_key
- Source value: `utah-state`
- Canonical value: `utah`
- Evidence: utah 1913-02-28: utah
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 20. DISCREPANCY-UST-S1-00075-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1914-02-06
- Field: score
- Source value: `23-41`
- Canonical value: `33-41`
- Evidence: utah 1914-02-06: 33-41
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 21. DISCREPANCY-UST-S1-00075-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1914-02-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: utah 1914-02-06: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 22. DISCREPANCY-UST-S1-00080-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1914-02-20
- Field: score
- Source value: `37-27`
- Canonical value: `34-27`
- Evidence: utah 1914-02-20: 34-27
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 23. DISCREPANCY-UST-S1-00080-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1914-02-20
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1914-02-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 24. DISCREPANCY-UST-S1-00083-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1914-03-06
- Field: score
- Source value: `38-19`
- Canonical value: `28-19`
- Evidence: byu 1914-03-06: 28-19
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 25. DISCREPANCY-UST-S1-00083-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1914-03-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu 1914-03-06: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 26. DISCREPANCY-UST-S1-00097-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1916-02-19
- Field: score
- Source value: `31-17`
- Canonical value: `33-17`
- Evidence: utah 1916-02-19: 33-17
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 27. DISCREPANCY-UST-S1-00097-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1916-02-19
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: utah 1916-02-19: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 28. DISCREPANCY-UST-S1-00128-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1919-03-01
- Field: score
- Source value: `36-26`
- Canonical value: `23-26`
- Evidence: byu 1919-03-01: 23-26
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 29. DISCREPANCY-UST-S1-00128-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1919-03-01
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: byu 1919-03-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 30. DISCREPANCY-UST-S1-00128-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1919-03-01
- Field: result_winner_team_key
- Source value: `byu`
- Canonical value: `utah-state`
- Evidence: byu 1919-03-01: utah-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 31. DISCREPANCY-UST-S1-00177-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1924-02-29
- Field: score
- Source value: `44-22`
- Canonical value: `44-24`
- Evidence: utah 1924-02-29: 44-24
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 32. DISCREPANCY-UST-S1-00177-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1924-02-29
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1924-02-29: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 33. DISCREPANCY-UST-S1-00181-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1925-01-30
- Field: score
- Source value: `33-30`
- Canonical value: `33-29`
- Evidence: utah 1925-01-30: 33-29
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 34. DISCREPANCY-UST-S1-00181-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1925-01-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1925-01-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 35. IDENTITY-UST-S1-00188

- Category: identity
- Matchup: utah-state vs usc
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=21-34`
- Canonical value: `CBBG-0067844;CBBG-0067845`
- Evidence: CBBG-0067844 1924-1925 [unknown] 23-31 sources=usc; CBBG-0067845 1924-1925 [unknown] 34-20 sources=usc
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 36. CONDITIONAL-DISCREPANCY-UST-S1-00188-CBBG-0067844-SCORE

- Category: conditional_discrepancy
- Matchup: usc vs utah-state
- Date: [unknown]
- Field: score
- Source value: `34-21`
- Canonical value: `23-31`
- Evidence: usc [unknown]: 23-31
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0067844`

### 37. CONDITIONAL-DISCREPANCY-UST-S1-00188-CBBG-0067844-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: usc vs utah-state
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `usc`
- Canonical value: `utah-state`
- Evidence: usc [unknown]: utah-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0067844`

### 38. CONDITIONAL-DISCREPANCY-UST-S1-00188-CBBG-0067845-SCORE

- Category: conditional_discrepancy
- Matchup: usc vs utah-state
- Date: [unknown]
- Field: score
- Source value: `34-21`
- Canonical value: `34-20`
- Evidence: usc [unknown]: 34-20
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0067845`

### 39. IDENTITY-UST-S1-00198

- Category: identity
- Matchup: utah-state vs usc
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=28-82`
- Canonical value: `CBBG-0067851;CBBG-0067852`
- Evidence: CBBG-0067851 1925-1926 [unknown] 32-38 sources=usc; CBBG-0067852 1925-1926 [unknown] 27-52 sources=usc
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 40. CONDITIONAL-DISCREPANCY-UST-S1-00198-CBBG-0067851-SCORE

- Category: conditional_discrepancy
- Matchup: usc vs utah-state
- Date: [unknown]
- Field: score
- Source value: `82-28`
- Canonical value: `32-38`
- Evidence: usc [unknown]: 32-38
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0067851`

### 41. CONDITIONAL-DISCREPANCY-UST-S1-00198-CBBG-0067851-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: usc vs utah-state
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `usc`
- Canonical value: `utah-state`
- Evidence: usc [unknown]: utah-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0067851`

### 42. CONDITIONAL-DISCREPANCY-UST-S1-00198-CBBG-0067852-SCORE

- Category: conditional_discrepancy
- Matchup: usc vs utah-state
- Date: [unknown]
- Field: score
- Source value: `82-28`
- Canonical value: `27-52`
- Evidence: usc [unknown]: 27-52
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0067852`

### 43. CONDITIONAL-DISCREPANCY-UST-S1-00198-CBBG-0067852-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: usc vs utah-state
- Date: [unknown]
- Field: result_winner_team_key
- Source value: `usc`
- Canonical value: `utah-state`
- Evidence: usc [unknown]: utah-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0067852`

### 44. IDENTITY-UST-S1-00199

- Category: identity
- Matchup: utah-state vs usc
- Dates: source [unknown]; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=[unknown]; score=52-17`
- Canonical value: `CBBG-0067851;CBBG-0067852`
- Evidence: CBBG-0067851 1925-1926 [unknown] 32-38 sources=usc; CBBG-0067852 1925-1926 [unknown] 27-52 sources=usc
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 45. CONDITIONAL-DISCREPANCY-UST-S1-00199-CBBG-0067851-SCORE

- Category: conditional_discrepancy
- Matchup: usc vs utah-state
- Date: [unknown]
- Field: score
- Source value: `17-52`
- Canonical value: `32-38`
- Evidence: usc [unknown]: 32-38
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0067851`

### 46. CONDITIONAL-DISCREPANCY-UST-S1-00199-CBBG-0067852-SCORE

- Category: conditional_discrepancy
- Matchup: usc vs utah-state
- Date: [unknown]
- Field: score
- Source value: `17-52`
- Canonical value: `27-52`
- Evidence: usc [unknown]: 27-52
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0067852`

### 47. DISCREPANCY-UST-S1-00204-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1926-01-30
- Field: score
- Source value: `35-32`
- Canonical value: `36-32`
- Evidence: byu 1926-01-30: 36-32
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 48. DISCREPANCY-UST-S1-00204-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1926-01-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: byu 1926-01-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 49. DISCREPANCY-UST-S1-00208-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1926-02-20
- Field: score
- Source value: `49-36`
- Canonical value: `51-36`
- Evidence: utah 1926-02-20: 51-36
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 50. DISCREPANCY-UST-S1-00208-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1926-02-20
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1926-02-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 51. DISCREPANCY-UST-S1-00217-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1927-01-21
- Field: score
- Source value: `48-50`
- Canonical value: `47-50`
- Evidence: byu 1927-01-21: 47-50
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 52. DISCREPANCY-UST-S1-00217-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1927-01-21
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu 1927-01-21: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 53. DISCREPANCY-UST-S1-00224-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1927-02-18
- Field: score
- Source value: `33-41`
- Canonical value: `31-41`
- Evidence: utah 1927-02-18: 31-41
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 54. DISCREPANCY-UST-S1-00224-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1927-02-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: utah 1927-02-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 55. DISCREPANCY-UST-S1-00229-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1927-03-05
- Field: score
- Source value: `25-42`
- Canonical value: `35-42`
- Evidence: byu 1927-03-05: 35-42
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 56. DISCREPANCY-UST-S1-00229-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1927-03-05
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: byu 1927-03-05: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 57. IDENTITY-UST-S1-00236

- Category: identity
- Matchup: utah-state vs byu
- Dates: source 1928-02-01; canonical 1928-02-10;1928-02-11;[unknown];[unknown]
- Field: game_identity
- Source value: `date=1928-02-01; score=34-49`
- Canonical value: `CBBG-0106878;CBBG-0106879;CBBG-0106880;CBBG-0106881`
- Evidence: CBBG-0106878 1927-1928 1928-02-10 49-34 sources=byu; CBBG-0106879 1927-1928 1928-02-11 31-39 sources=byu; CBBG-0106880 1927-1928 [unknown] 41-52 sources=byu; CBBG-0106881 1927-1928 [unknown] 42-48 sources=byu
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 58. CONDITIONAL-DISCREPANCY-UST-S1-00236-CBBG-0106878-GAME_DATE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical 1928-02-10
- Field: game_date
- Source value: `1928-02-01`
- Canonical value: `1928-02-10`
- Evidence: byu 1928-02-10: 1928-02-10
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106878`

### 59. CONDITIONAL-DISCREPANCY-UST-S1-00236-CBBG-0106879-GAME_DATE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical 1928-02-11
- Field: game_date
- Source value: `1928-02-01`
- Canonical value: `1928-02-11`
- Evidence: byu 1928-02-11: 1928-02-11
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106879`

### 60. CONDITIONAL-DISCREPANCY-UST-S1-00236-CBBG-0106879-SCORE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical 1928-02-11
- Field: score
- Source value: `49-34`
- Canonical value: `31-39`
- Evidence: byu 1928-02-11: 31-39
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106879`

### 61. CONDITIONAL-DISCREPANCY-UST-S1-00236-CBBG-0106879-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical 1928-02-11
- Field: result_winner_team_key
- Source value: `byu`
- Canonical value: `utah-state`
- Evidence: byu 1928-02-11: utah-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106879`

### 62. CONDITIONAL-DISCREPANCY-UST-S1-00236-CBBG-0106880-SCORE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical [unknown]
- Field: score
- Source value: `49-34`
- Canonical value: `41-52`
- Evidence: byu [unknown]: 41-52
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106880`

### 63. CONDITIONAL-DISCREPANCY-UST-S1-00236-CBBG-0106880-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106880`

### 64. CONDITIONAL-DISCREPANCY-UST-S1-00236-CBBG-0106880-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical [unknown]
- Field: result_winner_team_key
- Source value: `byu`
- Canonical value: `utah-state`
- Evidence: byu [unknown]: utah-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106880`

### 65. CONDITIONAL-DISCREPANCY-UST-S1-00236-CBBG-0106881-SCORE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical [unknown]
- Field: score
- Source value: `49-34`
- Canonical value: `42-48`
- Evidence: byu [unknown]: 42-48
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106881`

### 66. CONDITIONAL-DISCREPANCY-UST-S1-00236-CBBG-0106881-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106881`

### 67. CONDITIONAL-DISCREPANCY-UST-S1-00236-CBBG-0106881-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical [unknown]
- Field: result_winner_team_key
- Source value: `byu`
- Canonical value: `utah-state`
- Evidence: byu [unknown]: utah-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106881`

### 68. IDENTITY-UST-S1-00237

- Category: identity
- Matchup: utah-state vs byu
- Dates: source 1928-02-01; canonical 1928-02-10;1928-02-11;[unknown];[unknown]
- Field: game_identity
- Source value: `date=1928-02-01; score=39-31`
- Canonical value: `CBBG-0106878;CBBG-0106879;CBBG-0106880;CBBG-0106881`
- Evidence: CBBG-0106878 1927-1928 1928-02-10 49-34 sources=byu; CBBG-0106879 1927-1928 1928-02-11 31-39 sources=byu; CBBG-0106880 1927-1928 [unknown] 41-52 sources=byu; CBBG-0106881 1927-1928 [unknown] 42-48 sources=byu
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 69. CONDITIONAL-DISCREPANCY-UST-S1-00237-CBBG-0106878-GAME_DATE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical 1928-02-10
- Field: game_date
- Source value: `1928-02-01`
- Canonical value: `1928-02-10`
- Evidence: byu 1928-02-10: 1928-02-10
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106878`

### 70. CONDITIONAL-DISCREPANCY-UST-S1-00237-CBBG-0106878-SCORE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical 1928-02-10
- Field: score
- Source value: `31-39`
- Canonical value: `49-34`
- Evidence: byu 1928-02-10: 49-34
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106878`

### 71. CONDITIONAL-DISCREPANCY-UST-S1-00237-CBBG-0106878-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical 1928-02-10
- Field: result_winner_team_key
- Source value: `utah-state`
- Canonical value: `byu`
- Evidence: byu 1928-02-10: byu
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106878`

### 72. CONDITIONAL-DISCREPANCY-UST-S1-00237-CBBG-0106879-GAME_DATE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical 1928-02-11
- Field: game_date
- Source value: `1928-02-01`
- Canonical value: `1928-02-11`
- Evidence: byu 1928-02-11: 1928-02-11
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106879`

### 73. CONDITIONAL-DISCREPANCY-UST-S1-00237-CBBG-0106880-SCORE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical [unknown]
- Field: score
- Source value: `31-39`
- Canonical value: `41-52`
- Evidence: byu [unknown]: 41-52
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106880`

### 74. CONDITIONAL-DISCREPANCY-UST-S1-00237-CBBG-0106880-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106880`

### 75. CONDITIONAL-DISCREPANCY-UST-S1-00237-CBBG-0106881-SCORE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical [unknown]
- Field: score
- Source value: `31-39`
- Canonical value: `42-48`
- Evidence: byu [unknown]: 42-48
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106881`

### 76. CONDITIONAL-DISCREPANCY-UST-S1-00237-CBBG-0106881-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1928-02-01; canonical [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu [unknown]: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106881`

### 77. DISCREPANCY-UST-S1-00240-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1928-02-10
- Field: score
- Source value: `41-52`
- Canonical value: `49-34`
- Evidence: byu 1928-02-10: 49-34
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 78. DISCREPANCY-UST-S1-00240-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1928-02-10
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: byu 1928-02-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 79. DISCREPANCY-UST-S1-00240-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1928-02-10
- Field: result_winner_team_key
- Source value: `utah-state`
- Canonical value: `byu`
- Evidence: byu 1928-02-10: byu
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 80. DISCREPANCY-UST-S1-00241-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1928-02-11
- Field: score
- Source value: `42-48`
- Canonical value: `31-39`
- Evidence: byu 1928-02-11: 31-39
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 81. DISCREPANCY-UST-S1-00241-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1928-02-11
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: byu 1928-02-11: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 82. DISCREPANCY-UST-S1-00315-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1932-01-22
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: byu 1932-01-22: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 83. DISCREPANCY-UST-S1-00338-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1933-01-21
- Field: score
- Source value: `38-33`
- Canonical value: `39-31`
- Evidence: utah 1933-01-21: 39-31
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 84. DISCREPANCY-UST-S1-00338-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1933-01-21
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1933-01-21: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 85. DISCREPANCY-UST-S1-00380-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1935-02-08
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: byu 1935-02-08: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 86. DISCREPANCY-UST-S1-00414-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: kansas vs utah-state
- Date: 1936-03-25
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: kansas 1936-03-25: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 87. DISCREPANCY-UST-S1-00414-SITE_TYPE

- Category: discrepancy
- Matchup: kansas vs utah-state
- Date: 1936-03-25
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: kansas 1936-03-25: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 88. DISCREPANCY-UST-S1-00414-GAME_TYPE

- Category: discrepancy
- Matchup: kansas vs utah-state
- Date: 1936-03-25
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `REGULAR_SEASON`
- Evidence: kansas 1936-03-25: REGULAR_SEASON
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 89. DISCREPANCY-UST-S1-00415-SITE_TYPE

- Category: discrepancy
- Matchup: kansas vs utah-state
- Date: 1936-03-26
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: kansas 1936-03-26: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 90. DISCREPANCY-UST-S1-00415-GAME_TYPE

- Category: discrepancy
- Matchup: kansas vs utah-state
- Date: 1936-03-26
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `REGULAR_SEASON`
- Evidence: kansas 1936-03-26: REGULAR_SEASON
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 91. DISCREPANCY-UST-S1-00416-SCORE

- Category: discrepancy
- Matchup: kansas vs utah-state
- Date: 1936-03-28
- Field: score
- Source value: `33-50`
- Canonical value: `31-50`
- Evidence: kansas 1936-03-28: 31-50
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 92. DISCREPANCY-UST-S1-00416-SITE_TYPE

- Category: discrepancy
- Matchup: kansas vs utah-state
- Date: 1936-03-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: kansas 1936-03-28: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 93. DISCREPANCY-UST-S1-00416-GAME_TYPE

- Category: discrepancy
- Matchup: kansas vs utah-state
- Date: 1936-03-28
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `REGULAR_SEASON`
- Evidence: kansas 1936-03-28: REGULAR_SEASON
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 94. DISCREPANCY-UST-S1-00420-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1937-01-16
- Field: score
- Source value: `49-46`
- Canonical value: `49-35`
- Evidence: byu 1937-01-16: 49-35
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 95. DISCREPANCY-UST-S1-00420-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1937-01-16
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: byu 1937-01-16: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 96. DISCREPANCY-UST-S1-00483-SCORE

- Category: discrepancy
- Matchup: colorado vs utah-state
- Date: 1940-01-12
- Field: score
- Source value: `28-31`
- Canonical value: `29-31`
- Evidence: colorado 1940-01-12: 29-31
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 97. DISCREPANCY-UST-S1-00483-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs utah-state
- Date: 1940-01-12
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: colorado 1940-01-12: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 98. DISCREPANCY-UST-S1-00515-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1941-03-14
- Field: score
- Source value: `49-27`
- Canonical value: `49-24`
- Evidence: utah 1941-03-14: 49-24
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 99. DISCREPANCY-UST-S1-00515-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1941-03-14
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1941-03-14: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 100. DISCREPANCY-UST-S1-00518-SCORE

- Category: discrepancy
- Matchup: oregon-state vs utah-state
- Date: 1941-12-22
- Field: score
- Source value: `45-30`
- Canonical value: `46-30`
- Evidence: oregon-state 1941-12-22: 46-30
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 101. DISCREPANCY-UST-S1-00518-SITE_TYPE

- Category: discrepancy
- Matchup: oregon-state vs utah-state
- Date: 1941-12-22
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `NEUTRAL`
- Evidence: oregon-state 1941-12-22: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 102. DISCREPANCY-UST-S1-00579-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1946-01-12
- Field: score
- Source value: `47-41`
- Canonical value: `47-29`
- Evidence: byu 1946-01-12: 47-29
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 103. DISCREPANCY-UST-S1-00583-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1946-02-01
- Field: score
- Source value: `69-44`
- Canonical value: `34-31`
- Evidence: utah 1946-02-01: 34-31
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 104. DISCREPANCY-UST-S1-00583-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1946-02-01
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: utah 1946-02-01: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 105. DISCREPANCY-UST-S1-00589-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1946-03-04
- Field: score
- Source value: `34-31`
- Canonical value: `69-44`
- Evidence: utah 1946-03-04: 69-44
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 106. DISCREPANCY-UST-S1-00589-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1946-03-04
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1946-03-04: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 107. DISCREPANCY-UST-S1-00601-SITE_TYPE

- Category: discrepancy
- Matchup: long-island-university vs utah-state
- Date: [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 108. DISCREPANCY-UST-S1-00627-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1948-01-31
- Field: score
- Source value: `65-68`
- Canonical value: `66-47`
- Evidence: byu 1948-01-31: 66-47
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 109. DISCREPANCY-UST-S1-00627-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1948-01-31
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: byu 1948-01-31: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 110. DISCREPANCY-UST-S1-00627-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1948-01-31
- Field: result_winner_team_key
- Source value: `utah-state`
- Canonical value: `byu`
- Evidence: byu 1948-01-31: byu
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 111. DISCREPANCY-UST-S1-00637-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1948-02-28
- Field: score
- Source value: `66-47`
- Canonical value: `65-68`
- Evidence: byu 1948-02-28: 65-68
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 112. DISCREPANCY-UST-S1-00637-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1948-02-28
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu 1948-02-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 113. DISCREPANCY-UST-S1-00637-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1948-02-28
- Field: result_winner_team_key
- Source value: `byu`
- Canonical value: `utah-state`
- Evidence: byu 1948-02-28: utah-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 114. DISCREPANCY-UST-S1-00655-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1949-01-22
- Field: score
- Source value: `64-46`
- Canonical value: `64-56`
- Evidence: byu 1949-01-22: 64-56
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 115. DISCREPANCY-UST-S1-00655-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1949-01-22
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: byu 1949-01-22: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 116. DISCREPANCY-UST-S1-00671-SCORE

- Category: discrepancy
- Matchup: oregon vs utah-state
- Date: 1949-12-02
- Field: score
- Source value: `86-72`
- Canonical value: `66-72`
- Evidence: oregon 1949-12-02: 66-72
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 117. DISCREPANCY-UST-S1-00671-SITE_TYPE

- Category: discrepancy
- Matchup: oregon vs utah-state
- Date: 1949-12-02
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `NEUTRAL`
- Evidence: oregon 1949-12-02: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 118. DISCREPANCY-UST-S1-00671-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: oregon vs utah-state
- Date: 1949-12-02
- Field: result_winner_team_key
- Source value: `oregon`
- Canonical value: `utah-state`
- Evidence: oregon 1949-12-02: utah-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 119. DISCREPANCY-UST-S1-00682-SCORE

- Category: discrepancy
- Matchup: iowa vs utah-state
- Date: 1950-01-02
- Field: score
- Source value: `62-60`
- Canonical value: `62-58`
- Evidence: iowa 1950-01-02: 62-58
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 120. DISCREPANCY-UST-S1-00682-SITE_TYPE

- Category: discrepancy
- Matchup: iowa vs utah-state
- Date: 1950-01-02
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: iowa 1950-01-02: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 121. DISCREPANCY-UST-S1-00708-SCORE

- Category: discrepancy
- Matchup: kansas vs utah-state
- Date: 1950-12-06
- Field: score
- Source value: `59-38`
- Canonical value: `56-38`
- Evidence: kansas 1950-12-06: 56-38
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 122. DISCREPANCY-UST-S1-00708-SITE_TYPE

- Category: discrepancy
- Matchup: kansas vs utah-state
- Date: 1950-12-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: kansas 1950-12-06: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 123. DISCREPANCY-UST-S1-00760-SCORE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1952-02-15
- Field: score
- Source value: `63-67`
- Canonical value: `69-67`
- Evidence: byu 1952-02-15: 69-67
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 124. DISCREPANCY-UST-S1-00760-SITE_TYPE

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1952-02-15
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: byu 1952-02-15: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 125. DISCREPANCY-UST-S1-00760-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: byu vs utah-state
- Date: 1952-02-15
- Field: result_winner_team_key
- Source value: `utah-state`
- Canonical value: `byu`
- Evidence: byu 1952-02-15: byu
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 126. DISCREPANCY-UST-S1-00764-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1952-03-01
- Field: score
- Source value: `79-70`
- Canonical value: `60-70`
- Evidence: utah 1952-03-01: 60-70
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 127. DISCREPANCY-UST-S1-00764-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1952-03-01
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: utah 1952-03-01: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 128. DISCREPANCY-UST-S1-00764-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1952-03-01
- Field: result_winner_team_key
- Source value: `utah`
- Canonical value: `utah-state`
- Evidence: utah 1952-03-01: utah-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 129. DISCREPANCY-UST-S1-00839-SCORE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1955-01-28
- Field: score
- Source value: `60-62`
- Canonical value: `60-52`
- Evidence: utah 1955-01-28: 60-52
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 130. DISCREPANCY-UST-S1-00839-SITE_TYPE

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1955-01-28
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: utah 1955-01-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 131. DISCREPANCY-UST-S1-00839-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: utah vs utah-state
- Date: 1955-01-28
- Field: result_winner_team_key
- Source value: `utah-state`
- Canonical value: `utah`
- Evidence: utah 1955-01-28: utah
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 132. IDENTITY-UST-S1-00975

- Category: identity
- Matchup: utah-state vs providence
- Dates: source 1960-03-17; canonical 1960-03-20
- Field: game_identity
- Source value: `date=1960-03-17; score=62-68`
- Canonical value: `CBBG-0157104`
- Evidence: CBBG-0157104 1959-1960 1960-03-20 68-62 sources=providence
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 133. CONDITIONAL-DISCREPANCY-UST-S1-00975-CBBG-0157104-GAME_DATE

- Category: conditional_discrepancy
- Matchup: providence vs utah-state
- Dates: source 1960-03-17; canonical 1960-03-20
- Field: game_date
- Source value: `1960-03-17`
- Canonical value: `1960-03-20`
- Evidence: providence 1960-03-20: 1960-03-20
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0157104`

### 134. IDENTITY-UST-S1-00986

- Category: identity
- Matchup: utah-state vs tcu
- Dates: source 1960-12-28; canonical 1960-12-27
- Field: game_identity
- Source value: `date=1960-12-28; score=87-61`
- Canonical value: `CBBG-0102906`
- Evidence: CBBG-0102906 1960-1961 1960-12-27 71-87 sources=tcu
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 135. CONDITIONAL-DISCREPANCY-UST-S1-00986-CBBG-0102906-GAME_DATE

- Category: conditional_discrepancy
- Matchup: tcu vs utah-state
- Dates: source 1960-12-28; canonical 1960-12-27
- Field: game_date
- Source value: `1960-12-28`
- Canonical value: `1960-12-27`
- Evidence: tcu 1960-12-27: 1960-12-27
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0102906`

### 136. CONDITIONAL-DISCREPANCY-UST-S1-00986-CBBG-0102906-SCORE

- Category: conditional_discrepancy
- Matchup: tcu vs utah-state
- Dates: source 1960-12-28; canonical 1960-12-27
- Field: score
- Source value: `61-87`
- Canonical value: `71-87`
- Evidence: tcu 1960-12-27: 71-87
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0102906`

### 137. IDENTITY-UST-S1-00996

- Category: identity
- Matchup: utah-state vs byu
- Dates: source 1961-02-11; canonical 1961-01-27;1961-02-13
- Field: game_identity
- Source value: `date=1961-02-11; score=94-73`
- Canonical value: `CBBG-0107567;CBBG-0107570`
- Evidence: CBBG-0107567 1960-1961 1961-01-27 75-57 sources=byu; CBBG-0107570 1960-1961 1961-02-13 73-94 sources=byu
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 138. CONDITIONAL-DISCREPANCY-UST-S1-00996-CBBG-0107567-GAME_DATE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1961-02-11; canonical 1961-01-27
- Field: game_date
- Source value: `1961-02-11`
- Canonical value: `1961-01-27`
- Evidence: byu 1961-01-27: 1961-01-27
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107567`

### 139. CONDITIONAL-DISCREPANCY-UST-S1-00996-CBBG-0107567-SCORE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1961-02-11; canonical 1961-01-27
- Field: score
- Source value: `73-94`
- Canonical value: `75-57`
- Evidence: byu 1961-01-27: 75-57
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107567`

### 140. CONDITIONAL-DISCREPANCY-UST-S1-00996-CBBG-0107567-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1961-02-11; canonical 1961-01-27
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: byu 1961-01-27: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107567`

### 141. CONDITIONAL-DISCREPANCY-UST-S1-00996-CBBG-0107567-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1961-02-11; canonical 1961-01-27
- Field: result_winner_team_key
- Source value: `utah-state`
- Canonical value: `byu`
- Evidence: byu 1961-01-27: byu
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107567`

### 142. CONDITIONAL-DISCREPANCY-UST-S1-00996-CBBG-0107570-GAME_DATE

- Category: conditional_discrepancy
- Matchup: byu vs utah-state
- Dates: source 1961-02-11; canonical 1961-02-13
- Field: game_date
- Source value: `1961-02-11`
- Canonical value: `1961-02-13`
- Evidence: byu 1961-02-13: 1961-02-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107570`

### 143. DISCREPANCY-UST-S1-01041-SITE_TYPE

- Category: discrepancy
- Matchup: ucla vs utah-state
- Date: 1962-12-26
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: ucla 1962-12-26: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 144. DISCREPANCY-UST-S1-01043-SITE_TYPE

- Category: discrepancy
- Matchup: usc vs utah-state
- Date: 1962-12-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: usc 1962-12-28: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 145. IDENTITY-UST-S1-01097

- Category: identity
- Matchup: utah-state vs arizona-state
- Dates: source 1964-12-29; canonical 1964-12-27;1965-01-23
- Field: game_identity
- Source value: `date=1964-12-29; score=98-96`
- Canonical value: `CBBG-0111616;CBBG-0111621`
- Evidence: CBBG-0111616 1964-1965 1964-12-27 96-98 sources=arizona-state; CBBG-0111621 1964-1965 1965-01-23 99-93 sources=arizona-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 146. CONDITIONAL-DISCREPANCY-UST-S1-01097-CBBG-0111616-GAME_DATE

- Category: conditional_discrepancy
- Matchup: arizona-state vs utah-state
- Dates: source 1964-12-29; canonical 1964-12-27
- Field: game_date
- Source value: `1964-12-29`
- Canonical value: `1964-12-27`
- Evidence: arizona-state 1964-12-27: 1964-12-27
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0111616`

### 147. CONDITIONAL-DISCREPANCY-UST-S1-01097-CBBG-0111621-GAME_DATE

- Category: conditional_discrepancy
- Matchup: arizona-state vs utah-state
- Dates: source 1964-12-29; canonical 1965-01-23
- Field: game_date
- Source value: `1964-12-29`
- Canonical value: `1965-01-23`
- Evidence: arizona-state 1965-01-23: 1965-01-23
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0111621`

### 148. CONDITIONAL-DISCREPANCY-UST-S1-01097-CBBG-0111621-SCORE

- Category: conditional_discrepancy
- Matchup: arizona-state vs utah-state
- Dates: source 1964-12-29; canonical 1965-01-23
- Field: score
- Source value: `96-98`
- Canonical value: `99-93`
- Evidence: arizona-state 1965-01-23: 99-93
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0111621`

### 149. CONDITIONAL-DISCREPANCY-UST-S1-01097-CBBG-0111621-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: arizona-state vs utah-state
- Dates: source 1964-12-29; canonical 1965-01-23
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: arizona-state 1965-01-23: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0111621`

### 150. CONDITIONAL-DISCREPANCY-UST-S1-01097-CBBG-0111621-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: arizona-state vs utah-state
- Dates: source 1964-12-29; canonical 1965-01-23
- Field: result_winner_team_key
- Source value: `utah-state`
- Canonical value: `arizona-state`
- Evidence: arizona-state 1965-01-23: arizona-state
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0111621`

### 151. DISCREPANCY-UST-S1-01124-GAME_DATE

- Category: discrepancy
- Matchup: stanford vs utah-state
- Dates: source 1965-12-29; canonical 1965-12-30
- Field: game_date
- Source value: `1965-12-29`
- Canonical value: `1965-12-30`
- Evidence: stanford 1965-12-30: 1965-12-30
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 152. DISCREPANCY-UST-S1-01125-GAME_DATE

- Category: discrepancy
- Matchup: arizona-state vs utah-state
- Dates: source 1965-12-30; canonical 1965-12-29
- Field: game_date
- Source value: `1965-12-30`
- Canonical value: `1965-12-29`
- Evidence: arizona-state 1965-12-29: 1965-12-29
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 153. DISCREPANCY-UST-S1-01147-SITE_TYPE

- Category: discrepancy
- Matchup: utah-state vs xavier
- Date: 1966-12-27
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: xavier 1966-12-27: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 154. DISCREPANCY-UST-S1-01176-GAME_DATE

- Category: discrepancy
- Matchup: tennessee vs utah-state
- Dates: source 1967-12-30; canonical 1967-12-29
- Field: game_date
- Source value: `1967-12-30`
- Canonical value: `1967-12-29`
- Evidence: tennessee 1967-12-29: 1967-12-29
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 155. DISCREPANCY-UST-S1-01176-SITE_TYPE

- Category: discrepancy
- Matchup: tennessee vs utah-state
- Dates: source 1967-12-30; canonical 1967-12-29
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: tennessee 1967-12-29: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 156. DISCREPANCY-UST-S1-01205-SCORE

- Category: discrepancy
- Matchup: arizona-state vs utah-state
- Date: 1969-01-18
- Field: score
- Source value: `108-91`
- Canonical value: `103-91`
- Evidence: arizona-state 1969-01-18: 103-91
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 157. DISCREPANCY-UST-S1-01221-SITE_TYPE

- Category: discrepancy
- Matchup: utah-state vs washington
- Date: 1969-12-13
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington 1969-12-13: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 158. DISCREPANCY-UST-S1-01222-SITE_TYPE

- Category: discrepancy
- Matchup: utah-state vs wisconsin
- Date: 1969-12-26
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: wisconsin 1969-12-26: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 159. DISCREPANCY-UST-S1-01684-SITE_TYPE

- Category: discrepancy
- Matchup: nc-state vs utah-state
- Date: 1986-11-30
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: nc-state 1986-11-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 160. DISCREPANCY-UST-S1-01913-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs utah-state
- Dates: source 1994-11-26; canonical 1994-11-25
- Field: game_date
- Source value: `1994-11-26`
- Canonical value: `1994-11-25`
- Evidence: boise-state 1994-11-25: 1994-11-25
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 161. DISCREPANCY-UST-S1-02051-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs utah-state
- Dates: source 1999-01-21; canonical 1999-01-22
- Field: game_date
- Source value: `1999-01-21`
- Canonical value: `1999-01-22`
- Evidence: boise-state 1999-01-22: 1999-01-22
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 162. DISCREPANCY-UST-S1-02628-SCORE

- Category: discrepancy
- Matchup: purdue vs utah-state
- Date: 2016-11-22
- Field: score
- Source value: `85-64`
- Canonical value: `85-61`
- Evidence: purdue 2016-11-22: 85-61
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 163. DISCREPANCY-UST-S1-02792-SITE_TYPE

- Category: discrepancy
- Matchup: oklahoma vs utah-state
- Date: 2021-11-21
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: oklahoma 2021-11-21: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 164. CANONICAL-SITE-PATCH-CBBG-0104048

- Category: canonical_site_patch
- Matchup: utah vs utah-state
- Dates: source [unknown]; canonical 1910-02-26
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_B_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from utah; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 165. ACCOMPLISHMENTS-UTAH-STATE

- Category: accomplishments
- Matchup: utah-state
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"ELITE_EIGHT","best_finish_year":"1970","conference_regular_season_championships":"18","conference_tournament_championships":"11","final_four_appearances":"0","national_championships":"0","ncaa_tournament_appearances":"26"}`
- Canonical value: `{"best_finish_key":"ELITE_EIGHT","best_finish_year":1970,"final_four_appearances":0,"national_championships":0,"ncaa_tournament_appearances":26}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `PENDING`
- Basis: [required before approval]

### 166. PUBLICATION-UTAH-STATE

- Category: publication
- Matchup: utah-state
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 2,964 in-scope source rows; 10 identity reviews; 109 definite and 44 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `PENDING`
- Basis: [required before approval]
