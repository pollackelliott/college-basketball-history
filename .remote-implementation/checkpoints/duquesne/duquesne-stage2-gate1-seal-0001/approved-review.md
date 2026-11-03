# duquesne onboarding review

Generated: 2026-11-02T23:05:20.789550+00:00
Input fingerprint: `e476ef0e0bdfa3babffc01c688ddd74d6259db2551046f2ee0d42ddd9254a4d8`
Approved plan: `c72c988cf11c1a8443363335f880f00b2103479ad895ae6d5eb0e937632bf171`

## Preflight summary

- Source rows: 2,741
- In-scope rows: 2,741
- Pre-cutoff researched rows: 0
- Existing matches: 809
- New canonical games: 1,920
- Identity reviews: 12
- Safe enrichment fields: 1,584
- Discrepancies: 98
- Conditional discrepancies: 48
- Canonical-only site reviews: 0
- Affected existing public programs: alabama, arizona, arizona-state, auburn, baylor, boise-state, boston-college, butler, byu, central-connecticut, chicago-state, cincinnati, clemson, colorado, colorado-state, creighton, davidson, dayton, depaul, duke, florida, florida-state, georgetown, georgia, georgia-tech, gonzaga, illinois, indiana, iowa, kansas, kentucky, long-island-university, louisville, loyola-chicago, lsu, marquette, maryland, miami, michigan, minnesota, missouri, nc-state, nebraska, north-carolina, northwestern, notre-dame, ohio-state, oklahoma-state, oregon, penn-state, pittsburgh, providence, purdue, rutgers, saint-louis, seton-hall, south-carolina, st-john-s, stanford, syracuse, tennessee, texas, texas-a-m, texas-state, texas-tech, ucf, ucla, usc, utah, utah-state, villanova, virginia-tech, wake-forest, west-virginia, wisconsin, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. DISCREPANCY-DUQ-S1-1929-30-002-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Dates: source 1929-12-11; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 2. DISCREPANCY-DUQ-S1-1929-30-016-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Dates: source 1930-02-08; canonical [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 3. DISCREPANCY-DUQ-S1-1931-32-005-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs georgetown
- Dates: source 1932-01-19; canonical 1932-01-20
- Field: game_date
- Source value: `1932-01-19`
- Canonical value: `1932-01-20`
- Evidence: georgetown 1932-01-20: 1932-01-20
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 4. DISCREPANCY-DUQ-S1-1931-32-005-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs georgetown
- Dates: source 1932-01-19; canonical 1932-01-20
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: georgetown 1932-01-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 5. DISCREPANCY-DUQ-S1-1931-32-017-SCORE

- Category: discrepancy
- Matchup: duquesne vs georgetown
- Date: 1932-02-20
- Field: score
- Source value: `37-25`
- Canonical value: `37-24`
- Evidence: georgetown 1932-02-20: 37-24
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 6. DISCREPANCY-DUQ-S1-1933-34-011-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1934-02-06
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: pittsburgh 1934-02-06: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 7. IDENTITY-DUQ-S1-1934-35-003

- Category: identity
- Matchup: duquesne vs loyola-chicago
- Dates: source 1934-12-20; canonical [unknown];[unknown]
- Field: game_identity
- Source value: `date=1934-12-20; score=39-23`
- Canonical value: `CBBG-0184852;CBBG-0184858`
- Evidence: CBBG-0184852 1934-1935 [unknown] 38-23 sources=loyola-chicago; CBBG-0184858 1934-1935 [unknown] 51-22 sources=loyola-chicago
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0184852`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 8. CONDITIONAL-DISCREPANCY-DUQ-S1-1934-35-003-CBBG-0184852-SCORE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Dates: source 1934-12-20; canonical [unknown]
- Field: score
- Source value: `39-23`
- Canonical value: `38-23`
- Evidence: loyola-chicago [unknown]: 38-23
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0184852`

### 9. CONDITIONAL-DISCREPANCY-DUQ-S1-1934-35-003-CBBG-0184852-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Dates: source 1934-12-20; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0184852`

### 10. CONDITIONAL-DISCREPANCY-DUQ-S1-1934-35-003-CBBG-0184858-SCORE

- Category: conditional_discrepancy
- Matchup: duquesne vs loyola-chicago
- Dates: source 1934-12-20; canonical [unknown]
- Field: score
- Source value: `39-23`
- Canonical value: `51-22`
- Evidence: loyola-chicago [unknown]: 51-22
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0184852
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0184858`

### 11. CONDITIONAL-DISCREPANCY-DUQ-S1-1934-35-003-CBBG-0184858-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: duquesne vs loyola-chicago
- Dates: source 1934-12-20; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0184852
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0184858`

### 12. DISCREPANCY-DUQ-S1-1934-35-009-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Dates: source 1935-01-15; canonical [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 13. DISCREPANCY-DUQ-S1-1934-35-012-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs st-john-s
- Dates: source 1935-01-31; canonical 1935-02-01
- Field: game_date
- Source value: `1935-01-31`
- Canonical value: `1935-02-01`
- Evidence: st-john-s 1935-02-01: 1935-02-01
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 14. DISCREPANCY-DUQ-S1-1935-36-005-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1936-01-08; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 15. IDENTITY-DUQ-S1-1935-36-017

- Category: identity
- Matchup: duquesne vs west-virginia
- Dates: source 1936-03-02; canonical 1936-02-01;1936-02-29
- Field: game_identity
- Source value: `date=1936-03-02; score=33-35`
- Canonical value: `CBBG-0119189;CBBG-0119195`
- Evidence: CBBG-0119189 1935-1936 1936-02-01 55-41 sources=west-virginia; CBBG-0119195 1935-1936 1936-02-29 33-35 sources=west-virginia
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0119195`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 16. CONDITIONAL-DISCREPANCY-DUQ-S1-1935-36-017-CBBG-0119189-GAME_DATE

- Category: conditional_discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1936-03-02; canonical 1936-02-01
- Field: game_date
- Source value: `1936-03-02`
- Canonical value: `1936-02-01`
- Evidence: west-virginia 1936-02-01: 1936-02-01
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0119195
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0119189`

### 17. CONDITIONAL-DISCREPANCY-DUQ-S1-1935-36-017-CBBG-0119189-SCORE

- Category: conditional_discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1936-03-02; canonical 1936-02-01
- Field: score
- Source value: `33-35`
- Canonical value: `55-41`
- Evidence: west-virginia 1936-02-01: 55-41
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0119195
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0119189`

### 18. CONDITIONAL-DISCREPANCY-DUQ-S1-1935-36-017-CBBG-0119189-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1936-03-02; canonical 1936-02-01
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: west-virginia 1936-02-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0119195
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0119189`

### 19. CONDITIONAL-DISCREPANCY-DUQ-S1-1935-36-017-CBBG-0119189-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1936-03-02; canonical 1936-02-01
- Field: result_winner_team_key
- Source value: `west-virginia`
- Canonical value: `duquesne`
- Evidence: west-virginia 1936-02-01: duquesne
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0119195
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0119189`

### 20. CONDITIONAL-DISCREPANCY-DUQ-S1-1935-36-017-CBBG-0119195-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1936-03-02; canonical 1936-02-29
- Field: game_date
- Source value: `1936-03-02`
- Canonical value: `1936-02-29`
- Evidence: west-virginia 1936-02-29: 1936-02-29
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0119195`

### 21. DISCREPANCY-DUQ-S1-1936-37-006-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1937-01-09; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 22. DISCREPANCY-DUQ-S1-1937-38-011-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1938-01-22; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 23. DISCREPANCY-DUQ-S1-1938-39-013-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1939-02-08; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 24. DISCREPANCY-DUQ-S1-1939-40-003-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs marquette
- Date: 1939-12-21
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1939-12-21: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 25. DISCREPANCY-DUQ-S1-1939-40-004-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs indiana
- Date: 1939-12-27
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: indiana 1939-12-27: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 26. DISCREPANCY-DUQ-S1-1939-40-005-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs duquesne
- Date: 1940-01-02
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: colorado 1940-01-02: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 27. DISCREPANCY-DUQ-S1-1939-40-008-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Dates: source 1940-01-15; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 28. DISCREPANCY-DUQ-S1-1939-40-013-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1940-02-07; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 29. DISCREPANCY-DUQ-S1-1939-40-019-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs st-john-s
- Date: 1940-03-11
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-john-s 1940-03-11: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 30. DISCREPANCY-DUQ-S1-1940-41-007-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Dates: source 1941-01-11; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 31. IDENTITY-DUQ-S1-1940-41-012

- Category: identity
- Matchup: duquesne vs long-island-university
- Dates: source 1941-02-08; canonical [unknown]
- Field: game_identity
- Source value: `date=1941-02-08; score=35-34`
- Canonical value: `CBBG-0170451`
- Evidence: CBBG-0170451 1940-1941 [unknown] 36-34 sources=long-island-university
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0170451`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 32. CONDITIONAL-DISCREPANCY-DUQ-S1-1940-41-012-CBBG-0170451-SCORE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1941-02-08; canonical [unknown]
- Field: score
- Source value: `35-34`
- Canonical value: `36-34`
- Evidence: long-island-university [unknown]: 36-34
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0170451`

### 33. CONDITIONAL-DISCREPANCY-DUQ-S1-1940-41-012-CBBG-0170451-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1941-02-08; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0170451`

### 34. DISCREPANCY-DUQ-S1-1940-41-015-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Dates: source 1941-02-17; canonical [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago [unknown]: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 35. DISCREPANCY-DUQ-S1-1940-41-019-SCORE

- Category: discrepancy
- Matchup: duquesne vs west-virginia
- Date: 1941-03-08
- Field: score
- Source value: `51-35`
- Canonical value: `51-37`
- Evidence: west-virginia 1941-03-08: 51-37
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 36. DISCREPANCY-DUQ-S1-1941-42-014-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1942-02-09; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 37. DISCREPANCY-DUQ-S1-1941-42-018-SCORE

- Category: discrepancy
- Matchup: depaul vs duquesne
- Date: 1942-02-23
- Field: score
- Source value: `35-36`
- Canonical value: `34-35`
- Evidence: depaul 1942-02-23: 34-35
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 38. IDENTITY-DUQ-S1-1942-43-009

- Category: identity
- Matchup: duquesne vs west-virginia
- Dates: source 1943-01-20; canonical 1943-01-23;1943-03-06
- Field: game_identity
- Source value: `date=1943-01-20; score=52-36`
- Canonical value: `CBBG-0119314;CBBG-0119324`
- Evidence: CBBG-0119314 1942-1943 1943-01-23 52-36 sources=west-virginia; CBBG-0119324 1942-1943 1943-03-06 37-56 sources=west-virginia
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0119314`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 39. CONDITIONAL-DISCREPANCY-DUQ-S1-1942-43-009-CBBG-0119314-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1943-01-20; canonical 1943-01-23
- Field: game_date
- Source value: `1943-01-20`
- Canonical value: `1943-01-23`
- Evidence: west-virginia 1943-01-23: 1943-01-23
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0119314`

### 40. CONDITIONAL-DISCREPANCY-DUQ-S1-1942-43-009-CBBG-0119324-GAME_DATE

- Category: conditional_discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1943-01-20; canonical 1943-03-06
- Field: game_date
- Source value: `1943-01-20`
- Canonical value: `1943-03-06`
- Evidence: west-virginia 1943-03-06: 1943-03-06
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0119314
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0119324`

### 41. CONDITIONAL-DISCREPANCY-DUQ-S1-1942-43-009-CBBG-0119324-SCORE

- Category: conditional_discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1943-01-20; canonical 1943-03-06
- Field: score
- Source value: `52-36`
- Canonical value: `37-56`
- Evidence: west-virginia 1943-03-06: 37-56
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0119314
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0119324`

### 42. CONDITIONAL-DISCREPANCY-DUQ-S1-1942-43-009-CBBG-0119324-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1943-01-20; canonical 1943-03-06
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: west-virginia 1943-03-06: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0119314
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0119324`

### 43. CONDITIONAL-DISCREPANCY-DUQ-S1-1942-43-009-CBBG-0119324-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1943-01-20; canonical 1943-03-06
- Field: result_winner_team_key
- Source value: `duquesne`
- Canonical value: `west-virginia`
- Evidence: west-virginia 1943-03-06: west-virginia
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0119314
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0119324`

### 44. DISCREPANCY-DUQ-S1-1942-43-011-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1943-02-08; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 45. DISCREPANCY-DUQ-S1-1946-47-009-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs utah
- Date: 1947-01-03
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: utah 1947-01-03: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 46. DISCREPANCY-DUQ-S1-1947-48-003-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs utah-state
- Date: 1947-12-23
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: utah-state 1947-12-23: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 47. IDENTITY-DUQ-S1-1948-49-006

- Category: identity
- Matchup: duquesne vs long-island-university
- Dates: source 1949-01-01; canonical [unknown]
- Field: game_identity
- Source value: `date=1949-01-01; score=54-45`
- Canonical value: `CBBG-0170575`
- Evidence: CBBG-0170575 1948-1949 [unknown] 64-55 sources=long-island-university
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0170575`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 48. CONDITIONAL-DISCREPANCY-DUQ-S1-1948-49-006-CBBG-0170575-SCORE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1949-01-01; canonical [unknown]
- Field: score
- Source value: `54-45`
- Canonical value: `64-55`
- Evidence: long-island-university [unknown]: 64-55
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0170575`

### 49. CONDITIONAL-DISCREPANCY-DUQ-S1-1948-49-006-CBBG-0170575-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1949-01-01; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0170575`

### 50. DISCREPANCY-DUQ-S1-1949-50-002-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs kansas
- Date: 1949-12-17
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: kansas 1949-12-17: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 51. DISCREPANCY-DUQ-S1-1949-50-012-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Date: 1950-01-14
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago 1950-01-14: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 52. DISCREPANCY-DUQ-S1-1949-50-021-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1950-02-16; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 53. DISCREPANCY-DUQ-S1-1949-50-026-SCORE

- Category: discrepancy
- Matchup: duquesne vs villanova
- Date: 1950-03-08
- Field: score
- Source value: `52-68`
- Canonical value: `51-68`
- Evidence: villanova 1950-03-08: 51-68
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 54. DISCREPANCY-DUQ-S1-1949-50-029-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs st-john-s
- Date: 1950-03-18
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-john-s 1950-03-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 55. DISCREPANCY-DUQ-S1-1950-51-014-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1951-01-16; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 56. DISCREPANCY-DUQ-S1-1950-51-025-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Date: 1951-02-28
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago 1951-02-28: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 57. DISCREPANCY-DUQ-S1-1952-53-028-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs st-john-s
- Date: 1953-03-12
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-john-s 1953-03-12: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 58. DISCREPANCY-DUQ-S1-1953-54-004-SCORE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1953-12-12
- Field: score
- Source value: `79-43`
- Canonical value: `79-46`
- Evidence: pittsburgh 1953-12-12: 79-46
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 59. IDENTITY-DUQ-S1-1954-55-011

- Category: identity
- Matchup: duquesne vs dayton
- Dates: source 1955-01-19; canonical 1954-12-29;1955-01-10;1955-02-26;1955-03-18
- Field: game_identity
- Source value: `date=1955-01-19; score=67-68`
- Canonical value: `CBBG-0187352;CBBG-0187354;CBBG-0187361;CBBG-0187363`
- Evidence: CBBG-0187352 1954-1955 1954-12-29 75-90 sources=dayton; CBBG-0187354 1954-1955 1955-01-10 68-67 sources=dayton; CBBG-0187361 1954-1955 1955-02-26 67-58 sources=dayton; CBBG-0187363 1954-1955 1955-03-18 58-70 sources=dayton
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0187354`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 60. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187352-GAME_DATE

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1954-12-29
- Field: game_date
- Source value: `1955-01-19`
- Canonical value: `1954-12-29`
- Evidence: dayton 1954-12-29: 1954-12-29
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187352`

### 61. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187352-SCORE

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1954-12-29
- Field: score
- Source value: `68-67`
- Canonical value: `75-90`
- Evidence: dayton 1954-12-29: 75-90
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187352`

### 62. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187352-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1954-12-29
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: dayton 1954-12-29: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187352`

### 63. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187352-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1954-12-29
- Field: result_winner_team_key
- Source value: `dayton`
- Canonical value: `duquesne`
- Evidence: dayton 1954-12-29: duquesne
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187352`

### 64. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187354-GAME_DATE

- Category: discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1955-01-10
- Field: game_date
- Source value: `1955-01-19`
- Canonical value: `1955-01-10`
- Evidence: dayton 1955-01-10: 1955-01-10
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187354`

### 65. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187361-GAME_DATE

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1955-02-26
- Field: game_date
- Source value: `1955-01-19`
- Canonical value: `1955-02-26`
- Evidence: dayton 1955-02-26: 1955-02-26
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187361`

### 66. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187361-SCORE

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1955-02-26
- Field: score
- Source value: `68-67`
- Canonical value: `67-58`
- Evidence: dayton 1955-02-26: 67-58
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187361`

### 67. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187361-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1955-02-26
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: dayton 1955-02-26: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187361`

### 68. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187363-GAME_DATE

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1955-03-18
- Field: game_date
- Source value: `1955-01-19`
- Canonical value: `1955-03-18`
- Evidence: dayton 1955-03-18: 1955-03-18
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187363`

### 69. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187363-SCORE

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1955-03-18
- Field: score
- Source value: `68-67`
- Canonical value: `58-70`
- Evidence: dayton 1955-03-18: 58-70
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187363`

### 70. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187363-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1955-03-18
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: dayton 1955-03-18: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187363`

### 71. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187363-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1955-03-18
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `NIT`
- Evidence: dayton 1955-03-18: NIT
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187363`

### 72. CONDITIONAL-DISCREPANCY-DUQ-S1-1954-55-011-CBBG-0187363-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-01-19; canonical 1955-03-18
- Field: result_winner_team_key
- Source value: `dayton`
- Canonical value: `duquesne`
- Evidence: dayton 1955-03-18: duquesne
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0187354
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187363`

### 73. DISCREPANCY-DUQ-S1-1954-55-026-GAME_DATE

- Category: discrepancy
- Matchup: dayton vs duquesne
- Dates: source 1955-03-19; canonical 1955-03-18
- Field: game_date
- Source value: `1955-03-19`
- Canonical value: `1955-03-18`
- Evidence: dayton 1955-03-18: 1955-03-18
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 74. IDENTITY-DUQ-S1-1955-56-026

- Category: identity
- Matchup: duquesne vs oklahoma-state
- Dates: source 1956-03-10; canonical 1956-03-17
- Field: game_identity
- Source value: `date=1956-03-10; score=69-61`
- Canonical value: `CBBG-0081216`
- Evidence: CBBG-0081216 1955-1956 1956-03-17 69-61 sources=oklahoma-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0081216`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 75. CONDITIONAL-DISCREPANCY-DUQ-S1-1955-56-026-CBBG-0081216-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs oklahoma-state
- Dates: source 1956-03-10; canonical 1956-03-17
- Field: game_date
- Source value: `1956-03-10`
- Canonical value: `1956-03-17`
- Evidence: oklahoma-state 1956-03-17: 1956-03-17
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0081216`

### 76. IDENTITY-DUQ-S1-1955-56-027

- Category: identity
- Matchup: duquesne vs louisville
- Dates: source 1956-03-11; canonical 1956-03-19
- Field: game_identity
- Source value: `date=1956-03-11; score=72-84`
- Canonical value: `CBBG-0144125`
- Evidence: CBBG-0144125 1955-1956 1956-03-19 72-84 sources=louisville
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0144125`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 77. CONDITIONAL-DISCREPANCY-DUQ-S1-1955-56-027-CBBG-0144125-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs louisville
- Dates: source 1956-03-11; canonical 1956-03-19
- Field: game_date
- Source value: `1956-03-11`
- Canonical value: `1956-03-19`
- Evidence: louisville 1956-03-19: 1956-03-19
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144125`

### 78. DISCREPANCY-DUQ-S1-1957-58-017-SCORE

- Category: discrepancy
- Matchup: dayton vs duquesne
- Date: 1958-02-08
- Field: score
- Source value: `68-66`
- Canonical value: `68-65`
- Evidence: dayton 1958-02-08: 68-65
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 79. DISCREPANCY-DUQ-S1-1958-59-004-SITE_TYPE

- Category: discrepancy
- Matchup: clemson vs duquesne
- Date: 1958-12-12
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: clemson 1958-12-12: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 80. DISCREPANCY-DUQ-S1-1959-60-019-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs loyola-chicago
- Date: 1960-02-20
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: loyola-chicago 1960-02-20: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 81. DISCREPANCY-DUQ-S1-1961-62-008-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs villanova
- Date: 1961-12-28
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: villanova 1961-12-28: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 82. DISCREPANCY-DUQ-S1-1961-62-028-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs st-john-s
- Date: 1962-03-22
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-john-s 1962-03-22: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 83. DISCREPANCY-DUQ-S1-1962-63-005-SITE_TYPE

- Category: discrepancy
- Matchup: boston-college vs duquesne
- Date: 1962-12-14
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: boston-college 1962-12-14: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 84. DISCREPANCY-DUQ-S1-1962-63-013-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs villanova
- Dates: source 1963-01-29; canonical 1963-01-30
- Field: game_date
- Source value: `1963-01-29`
- Canonical value: `1963-01-30`
- Evidence: villanova 1963-01-30: 1963-01-30
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 85. DISCREPANCY-DUQ-S1-1964-65-003-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs virginia-tech
- Date: 1964-12-05
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1964-12-05: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 86. DISCREPANCY-DUQ-S1-1966-67-004-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1966-12-10
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1966-12-10: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 87. DISCREPANCY-DUQ-S1-1966-67-010-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs st-john-s
- Dates: source 1966-12-27; canonical 1966-12-28
- Field: game_date
- Source value: `1966-12-27`
- Canonical value: `1966-12-28`
- Evidence: st-john-s 1966-12-28: 1966-12-28
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 88. DISCREPANCY-DUQ-S1-1967-68-004-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1967-12-09
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1967-12-09: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 89. DISCREPANCY-DUQ-S1-1967-68-008-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs villanova
- Date: 1967-12-27
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: villanova 1967-12-27: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 90. DISCREPANCY-DUQ-S1-1967-68-010-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs wisconsin
- Dates: source 1967-12-30; canonical 1967-12-29
- Field: game_date
- Source value: `1967-12-30`
- Canonical value: `1967-12-29`
- Evidence: wisconsin 1967-12-29: 1967-12-29
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 91. DISCREPANCY-DUQ-S1-1968-69-003-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1968-12-07
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1968-12-07: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 92. IDENTITY-DUQ-S1-1968-69-010

- Category: identity
- Matchup: duquesne vs lsu
- Dates: source 1968-12-30; canonical 1969-01-20
- Field: game_identity
- Source value: `date=1968-12-30; score=91-94`
- Canonical value: `CBBG-0040724`
- Evidence: CBBG-0040724 1968-1969 1969-01-20 91-94 sources=lsu
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0040724`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 93. CONDITIONAL-DISCREPANCY-DUQ-S1-1968-69-010-CBBG-0040724-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs lsu
- Dates: source 1968-12-30; canonical 1969-01-20
- Field: game_date
- Source value: `1968-12-30`
- Canonical value: `1969-01-20`
- Evidence: lsu 1969-01-20: 1969-01-20
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0040724`

### 94. DISCREPANCY-DUQ-S1-1968-69-023-GAME_DATE

- Category: discrepancy
- Matchup: boston-college vs duquesne
- Dates: source 1969-03-06; canonical 1969-03-05
- Field: game_date
- Source value: `1969-03-06`
- Canonical value: `1969-03-05`
- Evidence: boston-college 1969-03-05: 1969-03-05
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 95. DISCREPANCY-DUQ-S1-1968-69-026-SCORE

- Category: discrepancy
- Matchup: duquesne vs st-john-s
- Date: 1969-03-15
- Field: score
- Source value: `75-72`
- Canonical value: `74-72`
- Evidence: st-john-s 1969-03-15: 74-72
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 96. DISCREPANCY-DUQ-S1-1969-70-014-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs long-island-university
- Dates: source 1970-01-31; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 97. DISCREPANCY-DUQ-S1-1970-71-006-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1970-12-29
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1970-12-29: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 98. DISCREPANCY-DUQ-S1-1971-72-007-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs wake-forest
- Date: 1971-12-29
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: wake-forest 1971-12-29: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 99. DISCREPANCY-DUQ-S1-1971-72-008-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1971-12-30
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1971-12-30: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 100. DISCREPANCY-DUQ-S1-1972-73-002-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1972-12-08
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1972-12-08: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 101. DISCREPANCY-DUQ-S1-1973-74-003-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1973-12-07
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1973-12-07: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 102. DISCREPANCY-DUQ-S1-1973-74-004-SITE_TYPE

- Category: discrepancy
- Matchup: clemson vs duquesne
- Date: 1973-12-08
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: clemson 1973-12-08: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 103. DISCREPANCY-DUQ-S1-1973-74-006-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs illinois
- Dates: source 1973-12-28; canonical 1973-12-29
- Field: game_date
- Source value: `1973-12-28`
- Canonical value: `1973-12-29`
- Evidence: illinois 1973-12-29: 1973-12-29
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 104. DISCREPANCY-DUQ-S1-1974-75-002-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1974-12-06
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1974-12-06: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 105. DISCREPANCY-DUQ-S1-1974-75-003-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs oregon
- Date: 1974-12-07
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: oregon 1974-12-07: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 106. DISCREPANCY-DUQ-S1-1975-76-002-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1975-12-05
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1975-12-05: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 107. DISCREPANCY-DUQ-S1-1975-76-006-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs oregon
- Dates: source 1975-12-26; canonical 1975-12-27
- Field: game_date
- Source value: `1975-12-26`
- Canonical value: `1975-12-27`
- Evidence: oregon 1975-12-27: 1975-12-27
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 108. DISCREPANCY-DUQ-S1-1975-76-006-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs oregon
- Dates: source 1975-12-26; canonical 1975-12-27
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: oregon 1975-12-27: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 109. DISCREPANCY-DUQ-S1-1975-76-007-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs texas-tech
- Dates: source 1975-12-27; canonical 1975-12-28
- Field: game_date
- Source value: `1975-12-27`
- Canonical value: `1975-12-28`
- Evidence: texas-tech 1975-12-28: 1975-12-28
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 110. DISCREPANCY-DUQ-S1-1975-76-008-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs northwestern
- Dates: source 1975-12-29; canonical 1975-12-30
- Field: game_date
- Source value: `1975-12-29`
- Canonical value: `1975-12-30`
- Evidence: northwestern 1975-12-30: 1975-12-30
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 111. DISCREPANCY-DUQ-S1-1976-77-005-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1976-12-11
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1976-12-11: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 112. DISCREPANCY-DUQ-S1-1977-78-005-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs penn-state
- Date: 1977-12-20
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: penn-state 1977-12-20: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 113. DISCREPANCY-DUQ-S1-1977-78-013-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1978-01-19; canonical 1978-01-18
- Field: game_date
- Source value: `1978-01-19`
- Canonical value: `1978-01-18`
- Evidence: west-virginia 1978-01-18: 1978-01-18
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 114. DISCREPANCY-DUQ-S1-1977-78-016-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs south-carolina
- Date: 1978-01-30
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: south-carolina 1978-01-30: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 115. DISCREPANCY-DUQ-S1-1979-80-027-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1980-03-06
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1980-03-06: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 116. DISCREPANCY-DUQ-S1-1980-81-029-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1981-03-07
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 1981-03-07: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 117. DISCREPANCY-DUQ-S1-1983-84-002-SCORE

- Category: discrepancy
- Matchup: duquesne vs syracuse
- Date: 1983-12-03
- Field: score
- Source value: `69-78`
- Canonical value: `69-87`
- Evidence: syracuse 1983-12-03: 69-87
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 118. DISCREPANCY-DUQ-S1-1983-84-008-SITE_TYPE

- Category: discrepancy
- Matchup: baylor vs duquesne
- Date: 1983-12-28
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: baylor 1983-12-28: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 119. DISCREPANCY-DUQ-S1-1984-85-029-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs west-virginia
- Dates: source 1985-03-07; canonical 1985-03-06
- Field: game_date
- Source value: `1985-03-07`
- Canonical value: `1985-03-06`
- Evidence: west-virginia 1985-03-06: 1985-03-06
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 120. DISCREPANCY-DUQ-S1-1984-85-030-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs rutgers
- Dates: source 1985-03-08; canonical 1985-03-07
- Field: game_date
- Source value: `1985-03-08`
- Canonical value: `1985-03-07`
- Evidence: rutgers 1985-03-07: 1985-03-07
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 121. DISCREPANCY-DUQ-S1-1984-85-030-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs rutgers
- Dates: source 1985-03-08; canonical 1985-03-07
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: rutgers 1985-03-07: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 122. DISCREPANCY-DUQ-S1-1989-90-004-SITE_TYPE

- Category: discrepancy
- Matchup: auburn vs duquesne
- Date: 1989-12-09
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: auburn 1989-12-09: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 123. DISCREPANCY-DUQ-S1-1995-96-001-SCORE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 1995-11-29
- Field: score
- Source value: `74-84`
- Canonical value: `73-84`
- Evidence: pittsburgh 1995-11-29: 73-84
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 124. IDENTITY-DUQ-S1-1995-96-011

- Category: identity
- Matchup: duquesne vs virginia-tech
- Dates: source 1996-01-10; canonical 1996-01-02;1996-02-07
- Field: game_identity
- Source value: `date=1996-01-10; score=69-88`
- Canonical value: `CBBG-0136825;CBBG-0136835`
- Evidence: CBBG-0136825 1995-1996 1996-01-02 69-88 sources=virginia-tech; CBBG-0136835 1995-1996 1996-02-07 63-69 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136825`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 125. CONDITIONAL-DISCREPANCY-DUQ-S1-1995-96-011-CBBG-0136825-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1996-01-10; canonical 1996-01-02
- Field: game_date
- Source value: `1996-01-10`
- Canonical value: `1996-01-02`
- Evidence: virginia-tech 1996-01-02: 1996-01-02
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136825`

### 126. CONDITIONAL-DISCREPANCY-DUQ-S1-1995-96-011-CBBG-0136835-GAME_DATE

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1996-01-10; canonical 1996-02-07
- Field: game_date
- Source value: `1996-01-10`
- Canonical value: `1996-02-07`
- Evidence: virginia-tech 1996-02-07: 1996-02-07
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136825
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136835`

### 127. CONDITIONAL-DISCREPANCY-DUQ-S1-1995-96-011-CBBG-0136835-SCORE

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1996-01-10; canonical 1996-02-07
- Field: score
- Source value: `69-88`
- Canonical value: `63-69`
- Evidence: virginia-tech 1996-02-07: 63-69
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136825
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136835`

### 128. CONDITIONAL-DISCREPANCY-DUQ-S1-1995-96-011-CBBG-0136835-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1996-01-10; canonical 1996-02-07
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: virginia-tech 1996-02-07: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136825
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136835`

### 129. DISCREPANCY-DUQ-S1-1995-96-019-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1996-02-06; canonical 1996-02-07
- Field: game_date
- Source value: `1996-02-06`
- Canonical value: `1996-02-07`
- Evidence: virginia-tech 1996-02-07: 1996-02-07
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.

### 130. IDENTITY-DUQ-S1-1996-97-011

- Category: identity
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-01-06; canonical 1997-01-04;1997-03-01
- Field: game_identity
- Source value: `date=1997-01-06; score=76-63`
- Canonical value: `CBBG-0136851;CBBG-0136866`
- Evidence: CBBG-0136851 1996-1997 1997-01-04 76-63 sources=virginia-tech; CBBG-0136866 1996-1997 1997-03-01 62-76 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136851`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 131. CONDITIONAL-DISCREPANCY-DUQ-S1-1996-97-011-CBBG-0136851-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-01-06; canonical 1997-01-04
- Field: game_date
- Source value: `1997-01-06`
- Canonical value: `1997-01-04`
- Evidence: virginia-tech 1997-01-04: 1997-01-04
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136851`

### 132. CONDITIONAL-DISCREPANCY-DUQ-S1-1996-97-011-CBBG-0136866-GAME_DATE

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-01-06; canonical 1997-03-01
- Field: game_date
- Source value: `1997-01-06`
- Canonical value: `1997-03-01`
- Evidence: virginia-tech 1997-03-01: 1997-03-01
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136851
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136866`

### 133. CONDITIONAL-DISCREPANCY-DUQ-S1-1996-97-011-CBBG-0136866-SCORE

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-01-06; canonical 1997-03-01
- Field: score
- Source value: `76-63`
- Canonical value: `62-76`
- Evidence: virginia-tech 1997-03-01: 62-76
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136851
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136866`

### 134. CONDITIONAL-DISCREPANCY-DUQ-S1-1996-97-011-CBBG-0136866-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-01-06; canonical 1997-03-01
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: virginia-tech 1997-03-01: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136851
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136866`

### 135. CONDITIONAL-DISCREPANCY-DUQ-S1-1996-97-011-CBBG-0136866-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-01-06; canonical 1997-03-01
- Field: result_winner_team_key
- Source value: `duquesne`
- Canonical value: `virginia-tech`
- Evidence: virginia-tech 1997-03-01: virginia-tech
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136851
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136866`

### 136. IDENTITY-DUQ-S1-1996-97-024

- Category: identity
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-02-23; canonical 1997-01-04;1997-03-01
- Field: game_identity
- Source value: `date=1997-02-23; score=62-76`
- Canonical value: `CBBG-0136851;CBBG-0136866`
- Evidence: CBBG-0136851 1996-1997 1997-01-04 76-63 sources=virginia-tech; CBBG-0136866 1996-1997 1997-03-01 62-76 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136866`
- Basis: One real game equals one canonical game. Select the same-season candidate uniquely supported by exact or near-exact score/result and companion-game context; use a unique pair-season candidate when no competing real game is represented. Do not create a duplicate canonical game where the reciprocal record already represents the same contest.

### 137. CONDITIONAL-DISCREPANCY-DUQ-S1-1996-97-024-CBBG-0136851-GAME_DATE

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-02-23; canonical 1997-01-04
- Field: game_date
- Source value: `1997-02-23`
- Canonical value: `1997-01-04`
- Evidence: virginia-tech 1997-01-04: 1997-01-04
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136866
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136851`

### 138. CONDITIONAL-DISCREPANCY-DUQ-S1-1996-97-024-CBBG-0136851-SCORE

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-02-23; canonical 1997-01-04
- Field: score
- Source value: `62-76`
- Canonical value: `76-63`
- Evidence: virginia-tech 1997-01-04: 76-63
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136866
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136851`

### 139. CONDITIONAL-DISCREPANCY-DUQ-S1-1996-97-024-CBBG-0136851-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-02-23; canonical 1997-01-04
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: virginia-tech 1997-01-04: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136866
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136851`

### 140. CONDITIONAL-DISCREPANCY-DUQ-S1-1996-97-024-CBBG-0136851-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-02-23; canonical 1997-01-04
- Field: result_winner_team_key
- Source value: `virginia-tech`
- Canonical value: `duquesne`
- Evidence: virginia-tech 1997-01-04: duquesne
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136866
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136851`

### 141. CONDITIONAL-DISCREPANCY-DUQ-S1-1996-97-024-CBBG-0136866-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs virginia-tech
- Dates: source 1997-02-23; canonical 1997-03-01
- Field: game_date
- Source value: `1997-02-23`
- Canonical value: `1997-03-01`
- Evidence: virginia-tech 1997-03-01: 1997-03-01
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Preserve existing canonical authority for date, score, winner, game-type and other non-site historical conflicts when the newly staged Duquesne assertion conflicts with an already-published reciprocal institutional assertion and no independent corroboration in this bounded review requires a correction. Preserve the Duquesne raw/source evidence and carry the conflict transparently.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136866`

### 142. DISCREPANCY-DUQ-S1-2009-10-007-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs pittsburgh
- Date: 2009-12-02
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: pittsburgh 2009-12-02: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 143. DISCREPANCY-DUQ-S1-2010-11-008-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs west-virginia
- Date: 2010-12-12
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: west-virginia 2010-12-12: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Duquesne's accepted frozen Research H/A/N is the target-school historical authority after the completed Stage 3A/3B research and Stage 6 self-challenge. Use the frozen Duquesne site_type for this conflict while preserving reciprocal/canonical assertions as evidence rather than silently overriding accepted target research.

### 144. ACCOMPLISHMENTS-DUQUESNE

- Category: accomplishments
- Matchup: duquesne
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"FINAL_FOUR","best_finish_year":"1940","conference_regular_season_championships":"2","conference_tournament_championships":"2","final_four_appearances":"1","national_championships":"0","ncaa_tournament_appearances":"6"}`
- Canonical value: `{"best_finish_key":"FINAL_FOUR","best_finish_year":1940,"final_four_appearances":1,"national_championships":0,"ncaa_tournament_appearances":6}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `VERIFY_REFERENCE_VALUES`
- Basis: Duquesne Athletics' official historical material supports two Atlantic 10/Eastern 8 regular-season shares (1980 and 1981) and two conference tournament championships (1977 and 2024); the existing NCAA appearance/Final Four fields already match the accepted baseline, so verify the existing 2/2/6/1/0/FINAL_FOUR/1940 values without rewriting identical reference values.

### 145. PUBLICATION-DUQUESNE

- Category: publication
- Matchup: duquesne
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 2,741 in-scope source rows; 12 identity reviews; 83 definite and 48 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `ENABLE_PUBLIC_PAGE`
- Basis: Enable Duquesne publication only through the normal Gate 1, sealed-apply, Preview, Gate 2, merge, and Production-proof workflow after every approved decision and automated gate passes.
