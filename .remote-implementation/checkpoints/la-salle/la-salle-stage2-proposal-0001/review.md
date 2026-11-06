# la-salle onboarding review

Generated: 2026-11-06T19:41:17.221866+00:00
Input fingerprint: `aad15b9c8b5e1bd58c6d7786b3e89ec1a503ac1fe5d7e56b0b0b82f828c98845`

## Preflight summary

- Source rows: 2,587
- In-scope rows: 2,587
- Pre-cutoff researched rows: 0
- Existing matches: 791
- New canonical games: 1,781
- Identity reviews: 15
- Safe enrichment fields: 1,523
- Discrepancies: 115
- Conditional discrepancies: 43
- Canonical-only site reviews: 0
- Affected existing public programs: alabama, arizona, arizona-state, arkansas, auburn, baylor, boise-state, boston-college, butler, byu, california, central-connecticut, cincinnati, clemson, colorado, creighton, davidson, dayton, depaul, duke, duquesne, fairleigh-dickinson, florida, florida-state, fresno-state, georgetown, georgia, georgia-tech, houston, illinois, indiana, iowa, kansas, kansas-state, kentucky, long-island-university, louisville, loyola-chicago, marquette, maryland, miami, michigan, minnesota, missouri, nc-state, nebraska, north-carolina, northwestern, notre-dame, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, penn-state, pittsburgh, providence, purdue, rhode-island, rutgers, saint-louis, san-diego-state, seton-hall, smu, south-carolina, st-bonaventure, st-john-s, stanford, syracuse, tennessee, texas-a-m, texas-tech, ucf, ucla, uconn, usc, utah, utah-state, vanderbilt, villanova, virginia, virginia-tech, wagner, wake-forest, washington, west-virginia, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. IDENTITY-LAS-1931-32-015

- Category: identity
- Matchup: la-salle vs seton-hall
- Dates: source 1932-02-09; canonical 1931-12-19
- Field: game_identity
- Source value: `date=1932-02-09; score=34-24`
- Canonical value: `CBBG-0162407`
- Evidence: CBBG-0162407 1931-1932 1931-12-19 28-34 sources=seton-hall
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 2. CONDITIONAL-DISCREPANCY-LAS-1931-32-015-CBBG-0162407-GAME_DATE

- Category: conditional_discrepancy
- Matchup: la-salle vs seton-hall
- Dates: source 1932-02-09; canonical 1931-12-19
- Field: game_date
- Source value: `1932-02-09`
- Canonical value: `1931-12-19`
- Evidence: seton-hall 1931-12-19: 1931-12-19
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162407`

### 3. CONDITIONAL-DISCREPANCY-LAS-1931-32-015-CBBG-0162407-SCORE

- Category: conditional_discrepancy
- Matchup: la-salle vs seton-hall
- Dates: source 1932-02-09; canonical 1931-12-19
- Field: score
- Source value: `34-24`
- Canonical value: `28-34`
- Evidence: seton-hall 1931-12-19: 28-34
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162407`

### 4. CONDITIONAL-DISCREPANCY-LAS-1931-32-015-CBBG-0162407-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: la-salle vs seton-hall
- Dates: source 1932-02-09; canonical 1931-12-19
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: seton-hall 1931-12-19: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162407`

### 5. CONDITIONAL-DISCREPANCY-LAS-1931-32-015-CBBG-0162407-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: la-salle vs seton-hall
- Dates: source 1932-02-09; canonical 1931-12-19
- Field: result_winner_team_key
- Source value: `la-salle`
- Canonical value: `seton-hall`
- Evidence: seton-hall 1931-12-19: seton-hall
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162407`

### 6. DISCREPANCY-LAS-1933-34-017-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1934-03-06
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1934-03-06: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 7. DISCREPANCY-LAS-1936-37-007-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs long-island-university
- Dates: source 1937-01-11; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: long-island-university [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 8. DISCREPANCY-LAS-1937-38-015-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs seton-hall
- Dates: source 1938-02-22; canonical 1938-02-23
- Field: game_date
- Source value: `1938-02-22`
- Canonical value: `1938-02-23`
- Evidence: seton-hall 1938-02-23: 1938-02-23
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 9. IDENTITY-LAS-1945-46-017

- Category: identity
- Matchup: la-salle vs georgetown
- Dates: source 1946-02-12; canonical 1946-02-16;1946-03-09
- Field: game_identity
- Source value: `date=1946-02-12; score=55-53`
- Canonical value: `CBBG-0164197;CBBG-0164202`
- Evidence: CBBG-0164197 1945-1946 1946-02-16 53-55 sources=georgetown; CBBG-0164202 1945-1946 1946-03-09 54-37 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 10. CONDITIONAL-DISCREPANCY-LAS-1945-46-017-CBBG-0164197-GAME_DATE

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1946-02-12; canonical 1946-02-16
- Field: game_date
- Source value: `1946-02-12`
- Canonical value: `1946-02-16`
- Evidence: georgetown 1946-02-16: 1946-02-16
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164197`

### 11. CONDITIONAL-DISCREPANCY-LAS-1945-46-017-CBBG-0164202-GAME_DATE

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1946-02-12; canonical 1946-03-09
- Field: game_date
- Source value: `1946-02-12`
- Canonical value: `1946-03-09`
- Evidence: georgetown 1946-03-09: 1946-03-09
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164202`

### 12. CONDITIONAL-DISCREPANCY-LAS-1945-46-017-CBBG-0164202-SCORE

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1946-02-12; canonical 1946-03-09
- Field: score
- Source value: `53-55`
- Canonical value: `54-37`
- Evidence: georgetown 1946-03-09: 54-37
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164202`

### 13. CONDITIONAL-DISCREPANCY-LAS-1945-46-017-CBBG-0164202-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1946-02-12; canonical 1946-03-09
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgetown 1946-03-09: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164202`

### 14. CONDITIONAL-DISCREPANCY-LAS-1945-46-017-CBBG-0164202-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1946-02-12; canonical 1946-03-09
- Field: result_winner_team_key
- Source value: `la-salle`
- Canonical value: `georgetown`
- Evidence: georgetown 1946-03-09: georgetown
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164202`

### 15. IDENTITY-LAS-1945-46-023

- Category: identity
- Matchup: la-salle vs georgetown
- Dates: source 1946-03-04; canonical 1946-02-16;1946-03-09
- Field: game_identity
- Source value: `date=1946-03-04; score=37-54`
- Canonical value: `CBBG-0164197;CBBG-0164202`
- Evidence: CBBG-0164197 1945-1946 1946-02-16 53-55 sources=georgetown; CBBG-0164202 1945-1946 1946-03-09 54-37 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 16. CONDITIONAL-DISCREPANCY-LAS-1945-46-023-CBBG-0164197-GAME_DATE

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1946-03-04; canonical 1946-02-16
- Field: game_date
- Source value: `1946-03-04`
- Canonical value: `1946-02-16`
- Evidence: georgetown 1946-02-16: 1946-02-16
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164197`

### 17. CONDITIONAL-DISCREPANCY-LAS-1945-46-023-CBBG-0164197-SCORE

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1946-03-04; canonical 1946-02-16
- Field: score
- Source value: `54-37`
- Canonical value: `53-55`
- Evidence: georgetown 1946-02-16: 53-55
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164197`

### 18. CONDITIONAL-DISCREPANCY-LAS-1945-46-023-CBBG-0164197-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1946-03-04; canonical 1946-02-16
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: georgetown 1946-02-16: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164197`

### 19. CONDITIONAL-DISCREPANCY-LAS-1945-46-023-CBBG-0164197-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1946-03-04; canonical 1946-02-16
- Field: result_winner_team_key
- Source value: `georgetown`
- Canonical value: `la-salle`
- Evidence: georgetown 1946-02-16: la-salle
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164197`

### 20. CONDITIONAL-DISCREPANCY-LAS-1945-46-023-CBBG-0164202-GAME_DATE

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1946-03-04; canonical 1946-03-09
- Field: game_date
- Source value: `1946-03-04`
- Canonical value: `1946-03-09`
- Evidence: georgetown 1946-03-09: 1946-03-09
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164202`

### 21. DISCREPANCY-LAS-1946-47-001-SCORE

- Category: discrepancy
- Matchup: boston-college vs la-salle
- Date: 1946-11-30
- Field: score
- Source value: `41-76`
- Canonical value: `76-41`
- Evidence: boston-college 1946-11-30: 76-41
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 22. DISCREPANCY-LAS-1946-47-001-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: boston-college vs la-salle
- Date: 1946-11-30
- Field: result_winner_team_key
- Source value: `la-salle`
- Canonical value: `boston-college`
- Evidence: boston-college 1946-11-30: boston-college
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 23. IDENTITY-LAS-1946-47-019

- Category: identity
- Matchup: la-salle vs georgetown
- Dates: source 1947-02-12; canonical 1947-02-14
- Field: game_identity
- Source value: `date=1947-02-12; score=59-65`
- Canonical value: `CBBG-0164215`
- Evidence: CBBG-0164215 1946-1947 1947-02-14 65-59 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 24. CONDITIONAL-DISCREPANCY-LAS-1946-47-019-CBBG-0164215-GAME_DATE

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1947-02-12; canonical 1947-02-14
- Field: game_date
- Source value: `1947-02-12`
- Canonical value: `1947-02-14`
- Evidence: georgetown 1947-02-14: 1947-02-14
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164215`

### 25. IDENTITY-LAS-1947-48-012

- Category: identity
- Matchup: la-salle vs georgetown
- Dates: source 1948-01-15; canonical 1948-01-17
- Field: game_identity
- Source value: `date=1948-01-15; score=48-35`
- Canonical value: `CBBG-0164232`
- Evidence: CBBG-0164232 1947-1948 1948-01-17 35-48 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 26. CONDITIONAL-DISCREPANCY-LAS-1947-48-012-CBBG-0164232-GAME_DATE

- Category: conditional_discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1948-01-15; canonical 1948-01-17
- Field: game_date
- Source value: `1948-01-15`
- Canonical value: `1948-01-17`
- Evidence: georgetown 1948-01-17: 1948-01-17
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164232`

### 27. DISCREPANCY-LAS-1947-48-022-SITE_TYPE

- Category: discrepancy
- Matchup: cincinnati vs la-salle
- Date: 1948-02-27
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: cincinnati 1948-02-27: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 28. IDENTITY-LAS-1948-49-003

- Category: identity
- Matchup: la-salle vs byu
- Dates: source 1948-12-08; canonical 1948-12-10
- Field: game_identity
- Source value: `date=1948-12-08; score=76-54`
- Canonical value: `CBBG-0107303`
- Evidence: CBBG-0107303 1948-1949 1948-12-10 54-76 sources=byu
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 29. CONDITIONAL-DISCREPANCY-LAS-1948-49-003-CBBG-0107303-GAME_DATE

- Category: conditional_discrepancy
- Matchup: byu vs la-salle
- Dates: source 1948-12-08; canonical 1948-12-10
- Field: game_date
- Source value: `1948-12-08`
- Canonical value: `1948-12-10`
- Evidence: byu 1948-12-10: 1948-12-10
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107303`

### 30. DISCREPANCY-LAS-1948-49-027-SITE_TYPE

- Category: discrepancy
- Matchup: cincinnati vs la-salle
- Date: 1949-03-07
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: cincinnati 1949-03-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 31. DISCREPANCY-LAS-1950-51-016-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs nc-state
- Date: 1951-01-20
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: nc-state 1951-01-20: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 32. DISCREPANCY-LAS-1951-52-023-GAME_DATE

- Category: discrepancy
- Matchup: georgetown vs la-salle
- Dates: source 1952-02-23; canonical 1952-02-22
- Field: game_date
- Source value: `1952-02-23`
- Canonical value: `1952-02-22`
- Evidence: georgetown 1952-02-22: 1952-02-22
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 33. IDENTITY-LAS-1951-52-028

- Category: identity
- Matchup: la-salle vs duquesne
- Dates: source 1952-03-13; canonical 1952-02-04;1952-03-11
- Field: game_identity
- Source value: `date=1952-03-13; score=59-46`
- Canonical value: `CBBG-0191291;CBBG-0191298`
- Evidence: CBBG-0191291 1951-1952 1952-02-04 71-60 sources=duquesne; CBBG-0191298 1951-1952 1952-03-11 46-59 sources=duquesne
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 34. CONDITIONAL-DISCREPANCY-LAS-1951-52-028-CBBG-0191291-GAME_DATE

- Category: conditional_discrepancy
- Matchup: duquesne vs la-salle
- Dates: source 1952-03-13; canonical 1952-02-04
- Field: game_date
- Source value: `1952-03-13`
- Canonical value: `1952-02-04`
- Evidence: duquesne 1952-02-04: 1952-02-04
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0191291`

### 35. CONDITIONAL-DISCREPANCY-LAS-1951-52-028-CBBG-0191291-SCORE

- Category: conditional_discrepancy
- Matchup: duquesne vs la-salle
- Dates: source 1952-03-13; canonical 1952-02-04
- Field: score
- Source value: `46-59`
- Canonical value: `71-60`
- Evidence: duquesne 1952-02-04: 71-60
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0191291`

### 36. CONDITIONAL-DISCREPANCY-LAS-1951-52-028-CBBG-0191291-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: duquesne vs la-salle
- Dates: source 1952-03-13; canonical 1952-02-04
- Field: game_type
- Source value: `NIT`
- Canonical value: `REGULAR_SEASON`
- Evidence: duquesne 1952-02-04: REGULAR_SEASON
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0191291`

### 37. CONDITIONAL-DISCREPANCY-LAS-1951-52-028-CBBG-0191291-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: duquesne vs la-salle
- Dates: source 1952-03-13; canonical 1952-02-04
- Field: result_winner_team_key
- Source value: `la-salle`
- Canonical value: `duquesne`
- Evidence: duquesne 1952-02-04: duquesne
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0191291`

### 38. CONDITIONAL-DISCREPANCY-LAS-1951-52-028-CBBG-0191298-GAME_DATE

- Category: conditional_discrepancy
- Matchup: duquesne vs la-salle
- Dates: source 1952-03-13; canonical 1952-03-11
- Field: game_date
- Source value: `1952-03-13`
- Canonical value: `1952-03-11`
- Evidence: duquesne 1952-03-11: 1952-03-11
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0191298`

### 39. DISCREPANCY-LAS-1951-52-OTR-002-GAME_TYPE

- Category: discrepancy
- Matchup: kansas vs la-salle
- Date: 1952-03-31
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `REGULAR_SEASON`
- Evidence: kansas 1952-03-31: REGULAR_SEASON
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 40. DISCREPANCY-LAS-1952-53-010-SCORE

- Category: discrepancy
- Matchup: cincinnati vs la-salle
- Date: 1952-12-29
- Field: score
- Source value: `81-86`
- Canonical value: `66-81`
- Evidence: cincinnati 1952-12-29: 66-81
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 41. DISCREPANCY-LAS-1953-54-008-SITE_TYPE

- Category: discrepancy
- Matchup: kentucky vs la-salle
- Date: 1953-12-22
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: kentucky 1953-12-22: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 42. DISCREPANCY-LAS-1953-54-017-SCORE

- Category: discrepancy
- Matchup: la-salle vs nc-state
- Date: 1954-01-23
- Field: score
- Source value: `83-78`
- Canonical value: `88-78`
- Evidence: nc-state 1954-01-23: 88-78
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 43. NEW-GAME-SITE-PATCH-LAS-1953-54-026

- Category: new_game_site_patch
- Matchup: la-salle vs fordham
- Dates: source 1954-03-08; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue Buffalo Memorial Auditorium (buffalo-memorial-auditorium/VEN-000512) with registry geography Buffalo, NY, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 44. NEW-GAME-SITE-PATCH-LAS-1953-54-028

- Category: new_game_site_patch
- Matchup: la-salle vs navy
- Dates: source 1954-03-13; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue Palestra (palestra/VEN-000159) with registry geography Philadelphia, PA, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 45. NEW-GAME-SITE-PATCH-LAS-1953-54-030

- Category: new_game_site_patch
- Matchup: la-salle vs bradley
- Dates: source 1954-03-20; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue Municipal Auditorium (municipal-auditorium-kc/VEN-000143) with registry geography Kansas City, MO, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 46. DISCREPANCY-LAS-1954-55-006-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs utah
- Date: 1954-12-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: utah 1954-12-18: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 47. DISCREPANCY-LAS-1954-55-008-SITE_TYPE

- Category: discrepancy
- Matchup: kentucky vs la-salle
- Date: 1954-12-22
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: kentucky 1954-12-22: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 48. DISCREPANCY-LAS-1954-55-009-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs syracuse
- Dates: source 1954-12-27; canonical 1954-12-28
- Field: game_date
- Source value: `1954-12-27`
- Canonical value: `1954-12-28`
- Evidence: syracuse 1954-12-28: 1954-12-28
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 49. DISCREPANCY-LAS-1954-55-012-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs saint-louis
- Dates: source 1955-01-02; canonical 1955-01-01
- Field: game_date
- Source value: `1955-01-02`
- Canonical value: `1955-01-01`
- Evidence: saint-louis 1955-01-01: 1955-01-01
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 50. NEW-GAME-SITE-PATCH-LAS-1954-55-028

- Category: new_game_site_patch
- Matchup: la-salle vs princeton
- Dates: source 1955-03-11; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue Palestra (palestra/VEN-000159) with registry geography Philadelphia, PA, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 51. NEW-GAME-SITE-PATCH-LAS-1954-55-029

- Category: new_game_site_patch
- Matchup: la-salle vs canisius
- Dates: source 1955-03-12; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue Palestra (palestra/VEN-000159) with registry geography Philadelphia, PA, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 52. NEW-GAME-SITE-PATCH-LAS-1954-55-031

- Category: new_game_site_patch
- Matchup: la-salle vs san-francisco
- Dates: source 1955-03-19; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue Municipal Auditorium (municipal-auditorium-kc/VEN-000143) with registry geography Kansas City, MO, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 53. DISCREPANCY-LAS-1955-56-023-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1956-02-29
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1956-02-29: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 54. DISCREPANCY-LAS-1955-56-025-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1956-03-10
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1956-03-10: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 55. IDENTITY-LAS-1956-57-013

- Category: identity
- Matchup: la-salle vs cincinnati
- Dates: source 1957-01-12; canonical 1957-01-16
- Field: game_identity
- Source value: `date=1957-01-12; score=58-74`
- Canonical value: `CBBG-0121959`
- Evidence: CBBG-0121959 1956-1957 1957-01-16 74-58 sources=cincinnati
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 56. CONDITIONAL-DISCREPANCY-LAS-1956-57-013-CBBG-0121959-GAME_DATE

- Category: conditional_discrepancy
- Matchup: cincinnati vs la-salle
- Dates: source 1957-01-12; canonical 1957-01-16
- Field: game_date
- Source value: `1957-01-12`
- Canonical value: `1957-01-16`
- Evidence: cincinnati 1957-01-16: 1957-01-16
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0121959`

### 57. DISCREPANCY-LAS-1956-57-018-SCORE

- Category: discrepancy
- Matchup: georgetown vs la-salle
- Date: 1957-02-05
- Field: score
- Source value: `75-62`
- Canonical value: `75-65`
- Evidence: georgetown 1957-02-05: 75-65
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 58. DISCREPANCY-LAS-1956-57-025-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1957-03-06
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1957-03-06: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 59. DISCREPANCY-LAS-1957-58-011-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1958-01-11
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1958-01-11: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 60. IDENTITY-LAS-1957-58-017

- Category: identity
- Matchup: la-salle vs st-bonaventure
- Dates: source 1958-02-08; canonical [unknown]
- Field: game_identity
- Source value: `date=1958-02-08; score=71-90`
- Canonical value: `CBBG-0193280`
- Evidence: CBBG-0193280 1957-1958 [unknown] 71-85 sources=st-bonaventure
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 61. CONDITIONAL-DISCREPANCY-LAS-1957-58-017-CBBG-0193280-SCORE

- Category: conditional_discrepancy
- Matchup: la-salle vs st-bonaventure
- Dates: source 1958-02-08; canonical [unknown]
- Field: score
- Source value: `71-90`
- Canonical value: `71-85`
- Evidence: st-bonaventure [unknown]: 71-85
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0193280`

### 62. CONDITIONAL-DISCREPANCY-LAS-1957-58-017-CBBG-0193280-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: la-salle vs st-bonaventure
- Dates: source 1958-02-08; canonical [unknown]
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: st-bonaventure [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0193280`

### 63. DISCREPANCY-LAS-1957-58-025-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1958-03-08
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1958-03-08: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 64. DISCREPANCY-LAS-1958-59-016-SCORE

- Category: discrepancy
- Matchup: la-salle vs seton-hall
- Date: 1959-02-07
- Field: score
- Source value: `83-69`
- Canonical value: `83-60`
- Evidence: seton-hall 1959-02-07: 83-60
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 65. DISCREPANCY-LAS-1958-59-023-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1959-03-07
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1959-03-07: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 66. DISCREPANCY-LAS-1959-60-022-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1960-03-05
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1960-03-05: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 67. DISCREPANCY-LAS-1960-61-021-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1961-03-04
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1961-03-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 68. DISCREPANCY-LAS-1961-62-022-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1962-02-24
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1962-02-24: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 69. DISCREPANCY-LAS-1961-62-025-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1962-03-09
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1962-03-09: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 70. DISCREPANCY-LAS-1962-63-023-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1963-03-02
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1963-03-02: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 71. DISCREPANCY-LAS-1963-64-007-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs northwestern
- Date: 1963-12-27
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: northwestern 1963-12-27: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 72. DISCREPANCY-LAS-1963-64-019-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1964-02-08
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1964-02-08: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 73. DISCREPANCY-LAS-1964-65-007-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs st-john-s
- Date: 1964-12-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-john-s 1964-12-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 74. DISCREPANCY-LAS-1964-65-011-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1965-01-08
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1965-01-08: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 75. DISCREPANCY-LAS-1965-66-004-SITE_TYPE

- Category: discrepancy
- Matchup: georgetown vs la-salle
- Date: 1965-12-11
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgetown 1965-12-11: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 76. DISCREPANCY-LAS-1965-66-009-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs minnesota
- Date: 1965-12-30
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: minnesota 1965-12-30: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 77. DISCREPANCY-LAS-1965-66-019-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1966-02-12
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1966-02-12: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 78. DISCREPANCY-LAS-1966-67-009-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs syracuse
- Date: 1966-12-27
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `NEUTRAL`
- Evidence: syracuse 1966-12-27: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 79. DISCREPANCY-LAS-1966-67-021-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1967-02-18
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1967-02-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 80. DISCREPANCY-LAS-1967-68-010-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs syracuse
- Dates: source 1967-12-29; canonical 1967-12-30
- Field: game_date
- Source value: `1967-12-29`
- Canonical value: `1967-12-30`
- Evidence: syracuse 1967-12-30: 1967-12-30
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 81. DISCREPANCY-LAS-1967-68-024-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1968-02-24
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1968-02-24: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 82. NEW-GAME-SITE-PATCH-LAS-1967-68-028

- Category: new_game_site_patch
- Matchup: la-salle vs columbia
- Dates: source 1968-03-09; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue Cole Field House (cole-field-house/VEN-000047) with registry geography College Park, MD, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 83. DISCREPANCY-LAS-1968-69-019-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1969-02-08
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1969-02-08: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 84. DISCREPANCY-LAS-1969-70-007-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs tennessee
- Date: 1969-12-20
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: tennessee 1969-12-20: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 85. DISCREPANCY-LAS-1969-70-025-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1970-02-21
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1970-02-21: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 86. DISCREPANCY-LAS-1970-71-019-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1971-02-13
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1971-02-13: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 87. DISCREPANCY-LAS-1971-72-007-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs nebraska
- Date: 1971-12-18
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: nebraska 1971-12-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 88. DISCREPANCY-LAS-1971-72-008-SITE_TYPE

- Category: discrepancy
- Matchup: boston-college vs la-salle
- Date: 1971-12-27
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `NEUTRAL`
- Evidence: boston-college 1971-12-27: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 89. DISCREPANCY-LAS-1971-72-025-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1972-02-26
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1972-02-26: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 90. DISCREPANCY-LAS-1972-73-025-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1973-02-28
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1973-02-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 91. DISCREPANCY-LAS-1973-74-024-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1974-02-20
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1974-02-20: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 92. DISCREPANCY-LAS-1973-74-025-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs rutgers
- Date: 1974-02-23
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: rutgers 1974-02-23: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 93. DISCREPANCY-LAS-1974-75-010-SITE_TYPE

- Category: discrepancy
- Matchup: alabama vs la-salle
- Date: 1974-12-30
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: alabama 1974-12-30: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 94. DISCREPANCY-LAS-1974-75-022-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1975-02-12
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1975-02-12: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 95. DISCREPANCY-LAS-1974-75-025-SCORE

- Category: discrepancy
- Matchup: la-salle vs rutgers
- Date: 1975-02-22
- Field: score
- Source value: `82-96`
- Canonical value: `84-96`
- Evidence: rutgers 1975-02-22: 84-96
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 96. DISCREPANCY-LAS-1974-75-025-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs rutgers
- Date: 1975-02-22
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: rutgers 1975-02-22: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 97. DISCREPANCY-LAS-1975-76-008-SITE_TYPE

- Category: discrepancy
- Matchup: kansas vs la-salle
- Date: 1975-12-20
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: kansas 1975-12-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 98. DISCREPANCY-LAS-1975-76-022-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1976-02-14
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1976-02-14: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 99. DISCREPANCY-LAS-1976-77-007-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs tennessee
- Date: 1976-12-17
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: tennessee 1976-12-17: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 100. DISCREPANCY-LAS-1976-77-009-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs san-diego-state
- Date: 1976-12-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: san-diego-state 1976-12-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 101. DISCREPANCY-LAS-1976-77-019-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1977-02-02
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1977-02-02: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 102. DISCREPANCY-LAS-1976-77-026-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs notre-dame
- Date: 1977-02-26
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: notre-dame 1977-02-26: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 103. DISCREPANCY-LAS-1977-78-007-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs louisville
- Date: 1977-12-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: louisville 1977-12-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 104. DISCREPANCY-LAS-1977-78-024-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1978-02-18
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1978-02-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 105. DISCREPANCY-LAS-1978-79-020-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1979-01-31
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1979-01-31: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 106. IDENTITY-LAS-1978-79-026

- Category: identity
- Matchup: la-salle vs notre-dame
- Dates: source 1979-02-24; canonical 1979-02-26
- Field: game_identity
- Source value: `date=1979-02-24; score=70-93`
- Canonical value: `CBBG-0147612`
- Evidence: CBBG-0147612 1978-1979 1979-02-26 70-93 sources=notre-dame
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 107. CONDITIONAL-DISCREPANCY-LAS-1978-79-026-CBBG-0147612-GAME_DATE

- Category: conditional_discrepancy
- Matchup: la-salle vs notre-dame
- Dates: source 1979-02-24; canonical 1979-02-26
- Field: game_date
- Source value: `1979-02-24`
- Canonical value: `1979-02-26`
- Evidence: notre-dame 1979-02-26: 1979-02-26
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0147612`

### 108. DISCREPANCY-LAS-1979-80-004-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1979-12-08
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1979-12-08: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 109. DISCREPANCY-LAS-1979-80-006-SCORE

- Category: discrepancy
- Matchup: la-salle vs texas-a-m
- Date: 1979-12-14
- Field: score
- Source value: `72-67`
- Canonical value: `73-67`
- Evidence: texas-a-m 1979-12-14: 73-67
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 110. DISCREPANCY-LAS-1980-81-004-SCORE

- Category: discrepancy
- Matchup: la-salle vs xavier
- Date: 1980-12-10
- Field: score
- Source value: `70-65`
- Canonical value: `65-60`
- Evidence: xavier 1980-12-10: 65-60
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 111. DISCREPANCY-LAS-1980-81-006-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1980-12-20
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1980-12-20: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 112. DISCREPANCY-LAS-1980-81-007-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs san-diego-state
- Date: 1980-12-29
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: san-diego-state 1980-12-29: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 113. DISCREPANCY-LAS-1980-81-010-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs missouri
- Date: 1981-01-07
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: missouri 1981-01-07: UNKNOWN
- Recommended: `LEAVE_UNRESOLVED`
- Decision: `PENDING`
- Basis: [required before approval]

### 114. DISCREPANCY-LAS-1980-81-026-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs rhode-island
- Date: 1981-02-28
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: rhode-island 1981-02-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 115. DISCREPANCY-LAS-1981-82-017-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1982-01-27
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1982-01-27: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 116. DISCREPANCY-LAS-1982-83-014-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1983-01-22
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1983-01-22: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 117. IDENTITY-LAS-1982-83-021

- Category: identity
- Matchup: la-salle vs dayton
- Dates: source 1983-02-14; canonical 1983-02-12
- Field: game_identity
- Source value: `date=1983-02-14; score=73-79`
- Canonical value: `CBBG-0187797`
- Evidence: CBBG-0187797 1982-1983 1983-02-12 79-73 sources=dayton
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 118. CONDITIONAL-DISCREPANCY-LAS-1982-83-021-CBBG-0187797-GAME_DATE

- Category: conditional_discrepancy
- Matchup: dayton vs la-salle
- Dates: source 1983-02-14; canonical 1983-02-12
- Field: game_date
- Source value: `1983-02-14`
- Canonical value: `1983-02-12`
- Evidence: dayton 1983-02-12: 1983-02-12
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0187797`

### 119. NEW-GAME-SITE-PATCH-LAS-1982-83-031

- Category: new_game_site_patch
- Matchup: la-salle vs boston-university
- Dates: source 1983-03-15; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue Palestra (palestra/VEN-000159) with registry geography Philadelphia, PA, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 120. NEW-GAME-SITE-PATCH-LAS-1982-83-032

- Category: new_game_site_patch
- Matchup: la-salle vs vcu
- Dates: source 1983-03-17; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue Greensboro Coliseum (greensboro-coliseum/VEN-000076) with registry geography Greensboro, NC, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 121. DISCREPANCY-LAS-1983-84-006-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1983-12-17
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1983-12-17: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 122. DISCREPANCY-LAS-1983-84-008-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs maryland
- Date: 1983-12-30
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: maryland 1983-12-30: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 123. DISCREPANCY-LAS-1983-84-009-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs notre-dame
- Date: 1984-01-04
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `NEUTRAL`
- Evidence: notre-dame 1984-01-04: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 124. DISCREPANCY-LAS-1984-85-004-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs stanford
- Date: 1984-12-01
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: stanford 1984-12-01: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 125. DISCREPANCY-LAS-1985-86-004-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1985-12-04
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1985-12-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 126. DISCREPANCY-LAS-1986-87-001-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs penn-state
- Dates: source 1986-11-28; canonical 1986-11-27
- Field: game_date
- Source value: `1986-11-28`
- Canonical value: `1986-11-27`
- Evidence: penn-state 1986-11-27: 1986-11-27
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 127. DISCREPANCY-LAS-1987-88-011-SITE_TYPE

- Category: discrepancy
- Matchup: dayton vs la-salle
- Date: 1987-12-25
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: dayton 1987-12-25: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 128. DISCREPANCY-LAS-1988-89-008-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1988-12-22
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1988-12-22: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 129. NEW-GAME-SITE-PATCH-LAS-1988-89-032

- Category: new_game_site_patch
- Matchup: la-salle vs louisiana-tech
- Dates: source 1989-03-16; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue Memorial Gymnasium (memorial-gymnasium/VEN-000130) with registry geography Nashville, TN, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 130. DISCREPANCY-LAS-1989-90-002-SITE_TYPE

- Category: discrepancy
- Matchup: fresno-state vs la-salle
- Date: 1989-11-25
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: fresno-state 1989-11-25: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 131. NEW-GAME-SITE-PATCH-LAS-1989-90-031

- Category: new_game_site_patch
- Matchup: la-salle vs southern-miss
- Dates: source 1990-03-15; canonical [unknown]
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `[new canonical game]`
- Evidence: New NCAA Tournament game has an exact accepted physical venue XL Center (xl-center/VEN-000257) with registry geography Hartford, CT, but frozen H/A/N remains UNKNOWN. NCAA publication requires the exact venue/location and an explicit owner historical ruling is required before the source H/A/N may change.
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 132. IDENTITY-LAS-1990-91-007

- Category: identity
- Matchup: la-salle vs villanova
- Dates: source 1990-12-22; canonical 1990-12-12
- Field: game_identity
- Source value: `date=1990-12-22; score=102-94`
- Canonical value: `CBBG-0161644`
- Evidence: CBBG-0161644 1990-1991 1990-12-12 102-94 sources=villanova
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 133. CONDITIONAL-DISCREPANCY-LAS-1990-91-007-CBBG-0161644-GAME_DATE

- Category: conditional_discrepancy
- Matchup: la-salle vs villanova
- Dates: source 1990-12-22; canonical 1990-12-12
- Field: game_date
- Source value: `1990-12-22`
- Canonical value: `1990-12-12`
- Evidence: villanova 1990-12-12: 1990-12-12
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0161644`

### 134. DISCREPANCY-LAS-1991-92-004-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1991-12-09
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1991-12-09: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 135. DISCREPANCY-LAS-1993-94-004-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs la-salle
- Date: 1993-12-04
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: colorado 1993-12-04: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 136. DISCREPANCY-LAS-1993-94-025-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 1994-02-28
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: villanova 1994-02-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 137. DISCREPANCY-LAS-1994-95-005-SITE_TYPE

- Category: discrepancy
- Matchup: baylor vs la-salle
- Date: 1994-12-10
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: baylor 1994-12-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 138. IDENTITY-LAS-1995-96-013

- Category: identity
- Matchup: la-salle vs virginia-tech
- Dates: source 1996-01-13; canonical 1996-01-06;1996-02-21
- Field: game_identity
- Source value: `date=1996-01-13; score=55-71`
- Canonical value: `CBBG-0136826;CBBG-0136839`
- Evidence: CBBG-0136826 1995-1996 1996-01-06 55-71 sources=virginia-tech; CBBG-0136839 1995-1996 1996-02-21 56-61 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 139. CONDITIONAL-DISCREPANCY-LAS-1995-96-013-CBBG-0136826-GAME_DATE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1996-01-13; canonical 1996-01-06
- Field: game_date
- Source value: `1996-01-13`
- Canonical value: `1996-01-06`
- Evidence: virginia-tech 1996-01-06: 1996-01-06
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136826`

### 140. CONDITIONAL-DISCREPANCY-LAS-1995-96-013-CBBG-0136826-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1996-01-13; canonical 1996-01-06
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1996-01-06: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136826`

### 141. CONDITIONAL-DISCREPANCY-LAS-1995-96-013-CBBG-0136839-GAME_DATE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1996-01-13; canonical 1996-02-21
- Field: game_date
- Source value: `1996-01-13`
- Canonical value: `1996-02-21`
- Evidence: virginia-tech 1996-02-21: 1996-02-21
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136839`

### 142. CONDITIONAL-DISCREPANCY-LAS-1995-96-013-CBBG-0136839-SCORE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1996-01-13; canonical 1996-02-21
- Field: score
- Source value: `55-71`
- Canonical value: `56-61`
- Evidence: virginia-tech 1996-02-21: 56-61
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136839`

### 143. CONDITIONAL-DISCREPANCY-LAS-1995-96-013-CBBG-0136839-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1996-01-13; canonical 1996-02-21
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: virginia-tech 1996-02-21: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136839`

### 144. DISCREPANCY-LAS-1995-96-014-GAME_DATE

- Category: discrepancy
- Matchup: duquesne vs la-salle
- Dates: source 1996-01-15; canonical 1996-01-16
- Field: game_date
- Source value: `1996-01-15`
- Canonical value: `1996-01-16`
- Evidence: duquesne 1996-01-16: 1996-01-16
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 145. DISCREPANCY-LAS-1995-96-026-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1996-02-22; canonical 1996-02-21
- Field: game_date
- Source value: `1996-02-22`
- Canonical value: `1996-02-21`
- Evidence: virginia-tech 1996-02-21: 1996-02-21
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 146. DISCREPANCY-LAS-1996-97-003-SCORE

- Category: discrepancy
- Matchup: iowa vs la-salle
- Date: 1996-12-07
- Field: score
- Source value: `65-62`
- Canonical value: `65-60`
- Evidence: iowa 1996-12-07: 65-60
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 147. IDENTITY-LAS-1996-97-013

- Category: identity
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-01-20; canonical 1997-01-22;1997-02-15
- Field: game_identity
- Source value: `date=1997-01-20; score=46-57`
- Canonical value: `CBBG-0136856;CBBG-0136862`
- Evidence: CBBG-0136856 1996-1997 1997-01-22 46-57 sources=virginia-tech; CBBG-0136862 1996-1997 1997-02-15 59-56 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 148. CONDITIONAL-DISCREPANCY-LAS-1996-97-013-CBBG-0136856-GAME_DATE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-01-20; canonical 1997-01-22
- Field: game_date
- Source value: `1997-01-20`
- Canonical value: `1997-01-22`
- Evidence: virginia-tech 1997-01-22: 1997-01-22
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136856`

### 149. CONDITIONAL-DISCREPANCY-LAS-1996-97-013-CBBG-0136862-GAME_DATE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-01-20; canonical 1997-02-15
- Field: game_date
- Source value: `1997-01-20`
- Canonical value: `1997-02-15`
- Evidence: virginia-tech 1997-02-15: 1997-02-15
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136862`

### 150. CONDITIONAL-DISCREPANCY-LAS-1996-97-013-CBBG-0136862-SCORE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-01-20; canonical 1997-02-15
- Field: score
- Source value: `46-57`
- Canonical value: `59-56`
- Evidence: virginia-tech 1997-02-15: 59-56
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136862`

### 151. CONDITIONAL-DISCREPANCY-LAS-1996-97-013-CBBG-0136862-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-01-20; canonical 1997-02-15
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: virginia-tech 1997-02-15: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136862`

### 152. CONDITIONAL-DISCREPANCY-LAS-1996-97-013-CBBG-0136862-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-01-20; canonical 1997-02-15
- Field: result_winner_team_key
- Source value: `virginia-tech`
- Canonical value: `la-salle`
- Evidence: virginia-tech 1997-02-15: la-salle
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136862`

### 153. IDENTITY-LAS-1996-97-020

- Category: identity
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-02-10; canonical 1997-01-22;1997-02-15
- Field: game_identity
- Source value: `date=1997-02-10; score=59-56`
- Canonical value: `CBBG-0136856;CBBG-0136862`
- Evidence: CBBG-0136856 1996-1997 1997-01-22 46-57 sources=virginia-tech; CBBG-0136862 1996-1997 1997-02-15 59-56 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `PENDING`
- Basis: [required before approval]

### 154. CONDITIONAL-DISCREPANCY-LAS-1996-97-020-CBBG-0136856-GAME_DATE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-02-10; canonical 1997-01-22
- Field: game_date
- Source value: `1997-02-10`
- Canonical value: `1997-01-22`
- Evidence: virginia-tech 1997-01-22: 1997-01-22
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136856`

### 155. CONDITIONAL-DISCREPANCY-LAS-1996-97-020-CBBG-0136856-SCORE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-02-10; canonical 1997-01-22
- Field: score
- Source value: `59-56`
- Canonical value: `46-57`
- Evidence: virginia-tech 1997-01-22: 46-57
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136856`

### 156. CONDITIONAL-DISCREPANCY-LAS-1996-97-020-CBBG-0136856-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-02-10; canonical 1997-01-22
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: virginia-tech 1997-01-22: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136856`

### 157. CONDITIONAL-DISCREPANCY-LAS-1996-97-020-CBBG-0136856-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-02-10; canonical 1997-01-22
- Field: result_winner_team_key
- Source value: `la-salle`
- Canonical value: `virginia-tech`
- Evidence: virginia-tech 1997-01-22: virginia-tech
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136856`

### 158. CONDITIONAL-DISCREPANCY-LAS-1996-97-020-CBBG-0136862-GAME_DATE

- Category: conditional_discrepancy
- Matchup: la-salle vs virginia-tech
- Dates: source 1997-02-10; canonical 1997-02-15
- Field: game_date
- Source value: `1997-02-10`
- Canonical value: `1997-02-15`
- Evidence: virginia-tech 1997-02-15: 1997-02-15
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136862`

### 159. DISCREPANCY-LAS-1996-97-021-SCORE

- Category: discrepancy
- Matchup: duquesne vs la-salle
- Date: 1997-02-13
- Field: score
- Source value: `86-77`
- Canonical value: `88-77`
- Evidence: duquesne 1997-02-13: 88-77
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 160. DISCREPANCY-LAS-1996-97-022-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs st-bonaventure
- Date: 1997-02-15
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-bonaventure 1997-02-15: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 161. DISCREPANCY-LAS-1996-97-023-SCORE

- Category: discrepancy
- Matchup: dayton vs la-salle
- Date: 1997-02-20
- Field: score
- Source value: `82-72`
- Canonical value: `72-62`
- Evidence: dayton 1997-02-20: 72-62
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 162. DISCREPANCY-LAS-1997-98-007-SITE_TYPE

- Category: discrepancy
- Matchup: arizona-state vs la-salle
- Date: 1997-12-27
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: arizona-state 1997-12-27: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 163. DISCREPANCY-LAS-1998-99-007-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs purdue
- Date: 1998-12-12
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: purdue 1998-12-12: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 164. DISCREPANCY-LAS-1998-99-028-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs rhode-island
- Dates: source 1999-03-04; canonical 1999-03-03
- Field: game_date
- Source value: `1999-03-04`
- Canonical value: `1999-03-03`
- Evidence: rhode-island 1999-03-03: 1999-03-03
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 165. DISCREPANCY-LAS-1999-00-009-SITE_TYPE

- Category: discrepancy
- Matchup: butler vs la-salle
- Date: 1999-12-29
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: butler 1999-12-29: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 166. DISCREPANCY-LAS-2000-01-005-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs seton-hall
- Date: 2000-12-02
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: seton-hall 2000-12-02: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 167. DISCREPANCY-LAS-2000-01-008-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 2000-12-14
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: villanova 2000-12-14: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 168. DISCREPANCY-LAS-2000-01-011-GAME_DATE

- Category: discrepancy
- Matchup: california vs la-salle
- Dates: source 2000-12-29; canonical 2000-12-30
- Field: game_date
- Source value: `2000-12-29`
- Canonical value: `2000-12-30`
- Evidence: california 2000-12-30: 2000-12-30
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 169. DISCREPANCY-LAS-2001-02-017-SCORE

- Category: discrepancy
- Matchup: la-salle vs xavier
- Date: 2002-01-19
- Field: score
- Source value: `64-71`
- Canonical value: `67-71`
- Evidence: xavier 2002-01-19: 67-71
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 170. DISCREPANCY-LAS-2001-02-018-SCORE

- Category: discrepancy
- Matchup: dayton vs la-salle
- Date: 2002-01-23
- Field: score
- Source value: `71-67`
- Canonical value: `71-69`
- Evidence: dayton 2002-01-23: 71-69
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 171. DISCREPANCY-LAS-2002-03-006-SCORE

- Category: discrepancy
- Matchup: cincinnati vs la-salle
- Date: 2002-12-14
- Field: score
- Source value: `64-61`
- Canonical value: `65-62`
- Evidence: cincinnati 2002-12-14: 65-62
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 172. DISCREPANCY-LAS-2002-03-014-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs st-bonaventure
- Date: 2003-01-18
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-bonaventure 2003-01-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 173. DISCREPANCY-LAS-2003-04-006-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 2003-12-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `NEUTRAL`
- Evidence: villanova 2003-12-06: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 174. DISCREPANCY-LAS-2003-04-030-SCORE

- Category: discrepancy
- Matchup: la-salle vs rhode-island
- Date: 2004-03-10
- Field: score
- Source value: `42-55`
- Canonical value: `69-81`
- Evidence: rhode-island 2004-03-10: 69-81
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 175. DISCREPANCY-LAS-2007-08-025-SCORE

- Category: discrepancy
- Matchup: dayton vs la-salle
- Date: 2008-02-21
- Field: score
- Source value: `78-81`
- Canonical value: `67-75`
- Evidence: dayton 2008-02-21: 67-75
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 176. DISCREPANCY-LAS-2009-10-005-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Dates: source 2009-11-28; canonical 2009-11-27
- Field: game_date
- Source value: `2009-11-28`
- Canonical value: `2009-11-27`
- Evidence: villanova 2009-11-27: 2009-11-27
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 177. DISCREPANCY-LAS-2009-10-011-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs oklahoma-state
- Date: 2009-12-21
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: oklahoma-state 2009-12-21: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 178. DISCREPANCY-LAS-2011-12-031-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs st-bonaventure
- Dates: source 2012-03-02; canonical 2012-03-03
- Field: game_date
- Source value: `2012-03-02`
- Canonical value: `2012-03-03`
- Evidence: st-bonaventure 2012-03-03: 2012-03-03
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 179. DISCREPANCY-LAS-2011-12-034-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs minnesota
- Dates: source 2012-03-14; canonical 2012-03-13
- Field: game_date
- Source value: `2012-03-14`
- Canonical value: `2012-03-13`
- Evidence: minnesota 2012-03-13: 2012-03-13
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 180. DISCREPANCY-LAS-2014-15-006-SCORE

- Category: discrepancy
- Matchup: la-salle vs vanderbilt
- Date: 2014-11-29
- Field: score
- Source value: `70-84`
- Canonical value: `55-68`
- Evidence: vanderbilt 2014-11-29: 55-68
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 181. DISCREPANCY-LAS-2015-16-028-GAME_DATE

- Category: discrepancy
- Matchup: la-salle vs saint-louis
- Dates: source 2016-03-02; canonical 2016-03-03
- Field: game_date
- Source value: `2016-03-02`
- Canonical value: `2016-03-03`
- Evidence: saint-louis 2016-03-03: 2016-03-03
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 182. DISCREPANCY-LAS-2016-17-007-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 2016-12-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: villanova 2016-12-06: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 183. DISCREPANCY-LAS-2021-22-005-SITE_TYPE

- Category: discrepancy
- Matchup: la-salle vs villanova
- Date: 2021-11-28
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: villanova 2021-11-28: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 184. DISCREPANCY-LAS-2024-25-014-SCORE

- Category: discrepancy
- Matchup: dayton vs la-salle
- Date: 2024-12-31
- Field: score
- Source value: `84-70`
- Canonical value: `74-70`
- Evidence: dayton 2024-12-31: 74-70
- Recommended: `KEEP_CANONICAL`
- Decision: `PENDING`
- Basis: [required before approval]

### 185. ACCOMPLISHMENTS-LA-SALLE

- Category: accomplishments
- Matchup: la-salle
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"NATIONAL_CHAMPION","best_finish_year":"1954","conference_regular_season_championships":"8","conference_tournament_championships":"8","final_four_appearances":"2","national_championships":"1","ncaa_tournament_appearances":"12"}`
- Canonical value: `{"best_finish_key":"NATIONAL_CHAMPION","best_finish_year":1954,"final_four_appearances":2,"national_championships":1,"ncaa_tournament_appearances":12}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `PENDING`
- Basis: [required before approval]

### 186. PUBLICATION-LA-SALLE

- Category: publication
- Matchup: la-salle
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 2,587 in-scope source rows; 15 identity reviews; 115 definite and 43 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `PENDING`
- Basis: [required before approval]
