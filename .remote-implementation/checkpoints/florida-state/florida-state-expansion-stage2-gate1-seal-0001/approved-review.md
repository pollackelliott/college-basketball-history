# florida-state onboarding review

Generated: 2026-11-24T22:56:53.525634+00:00
Input fingerprint: `0d94db355a7815adfbb6baf50605c34f47ea787b3314c9c4d75d63054d1751de`
Approved plan: `f7b69d314b01fa533968bc3b4d670a71c3c0a3dae0005635733153427ea1220f`

## Preflight summary

- Source rows: 2,291
- Publication-eligible rows: 2,291
- Top-level rows: 2,053
- Publication-excluded researched rows: 0
- Existing matches: 2,111
- New canonical games: 179
- Identity reviews: 1
- Safe enrichment fields: 50
- Discrepancies: 7
- Conditional discrepancies: 5
- Canonical-only site reviews: 0
- Affected existing public programs: alabama, arizona, arkansas, auburn, baylor, boston-college, butler, byu, california, central-connecticut, chicago-state, cincinnati, clemson, colorado, colorado-state, creighton, davidson, dayton, depaul, duke, duquesne, fairleigh-dickinson, florida, fordham, george-washington, georgetown, georgia, georgia-tech, gonzaga, hawai-i, houston, illinois, indiana, iowa, iowa-state, kansas, kansas-state, kentucky, la-salle, louisville, lsu, marquette, maryland, miami, michigan, michigan-state, minnesota, mississippi-state, missouri, nc-state, nebraska, north-carolina, northwestern, notre-dame, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, penn-state, pittsburgh, providence, purdue, rhode-island, richmond, rutgers, saint-joseph-s, saint-louis, san-diego-state, seton-hall, smu, south-carolina, st-bonaventure, st-john-s, stanford, syracuse, tcu, tennessee, texas, texas-a-m, ucf, ucla, uconn, unlv, usc, utah-state, vanderbilt, vcu, villanova, virginia, virginia-tech, wagner, wake-forest, washington, washington-state, west-virginia, wisconsin, xavier

## Blockers

- None.

## Warnings

- FSU-STG1-00253: curated venue 'Allen Fieldhouse' absent from venues.csv (unchanged published legacy debt outside this expansion)

## Non-substantive site-gap provenance

- None.

## Owner decisions

### 1. IDENTITY-FSU-EXP-S1-00075

- Category: identity
- Matchup: florida-state vs ole-miss
- Dates: source 1951-01-09; canonical 1951-01-11;1951-02-14
- Field: game_identity
- Source value: `date=1951-01-09; score=63-58`
- Canonical value: `CBBG-0032433;CBBG-0032437`
- Evidence: CBBG-0032433 1950-1951 1951-01-11 63-58 sources=ole-miss; CBBG-0032437 1950-1951 1951-02-14 75-79 sources=ole-miss
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0032433`
- Basis: The frozen Florida State row is a 63-58 win over Ole Miss. CBBG-0032433 is the same 63-58 matchup, while CBBG-0032437 is the distinct 75-79 Ole Miss game already confidently matched to FSU-EXP-S1-00084. Select CBBG-0032433; this also satisfies the permanent one-target-match cardinality constraint for CBBG-0032437.

### 2. CONDITIONAL-DISCREPANCY-FSU-EXP-S1-00075-CBBG-0032433-GAME_DATE

- Category: discrepancy
- Matchup: florida-state vs ole-miss
- Dates: source 1951-01-09; canonical 1951-01-11
- Field: game_date
- Source value: `1951-01-09`
- Canonical value: `1951-01-11`
- Evidence: ole-miss 1951-01-11: 1951-01-11
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Florida State's frozen institutional row explicitly dates the 63-58 Ole Miss win to 1951-01-09. The reciprocal canonical representation dates the same score to 1951-01-11. Preserve the accepted Florida State research date in the proposed canonical reconciliation while retaining the reciprocal assertion as evidence.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0032433`

### 3. CONDITIONAL-DISCREPANCY-FSU-EXP-S1-00075-CBBG-0032437-GAME_DATE

- Category: conditional_discrepancy
- Matchup: florida-state vs ole-miss
- Dates: source 1951-01-09; canonical 1951-02-14
- Field: game_date
- Source value: `1951-01-09`
- Canonical value: `1951-02-14`
- Evidence: ole-miss 1951-02-14: 1951-02-14
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0032433
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0032437`

### 4. CONDITIONAL-DISCREPANCY-FSU-EXP-S1-00075-CBBG-0032437-SCORE

- Category: conditional_discrepancy
- Matchup: florida-state vs ole-miss
- Dates: source 1951-01-09; canonical 1951-02-14
- Field: score
- Source value: `63-58`
- Canonical value: `75-79`
- Evidence: ole-miss 1951-02-14: 75-79
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0032433
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0032437`

### 5. CONDITIONAL-DISCREPANCY-FSU-EXP-S1-00075-CBBG-0032437-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: florida-state vs ole-miss
- Dates: source 1951-01-09; canonical 1951-02-14
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: ole-miss 1951-02-14: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0032433
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0032437`

### 6. CONDITIONAL-DISCREPANCY-FSU-EXP-S1-00075-CBBG-0032437-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: florida-state vs ole-miss
- Dates: source 1951-01-09; canonical 1951-02-14
- Field: result_winner_team_key
- Source value: `florida-state`
- Canonical value: `ole-miss`
- Evidence: ole-miss 1951-02-14: ole-miss
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0032433
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0032437`

### 7. DISCREPANCY-FSU-EXP-S1-00102-GAME_DATE

- Category: discrepancy
- Matchup: florida-state vs georgia
- Dates: source 1951-12-27; canonical 1951-12-26
- Field: game_date
- Source value: `1951-12-27`
- Canonical value: `1951-12-26`
- Evidence: georgia 1951-12-26: 1951-12-26
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: The frozen Florida State source explicitly records the Georgia game as D27 in the Gator Bowl Tournament at Jacksonville, Florida, and the accepted research row is dated 1951-12-27. Recommend the accepted source date over the reciprocal canonical 1951-12-26 representation.

### 8. DISCREPANCY-FSU-EXP-S1-00104-SITE_TYPE

- Category: discrepancy
- Matchup: florida vs florida-state
- Date: 1951-12-29
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: florida 1951-12-29: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Florida State's frozen row explicitly says 'vs Florida' and identifies the Gator Bowl Tournament at Jacksonville, Florida. Its accepted research basis specifically preserves NEUTRAL despite the existing canonical Florida State-home conflict. Recommend the frozen neutral classification.

### 9. DISCREPANCY-FSU-EXP-S1-00128-SCORE

- Category: discrepancy
- Matchup: florida-state vs miami
- Date: 1953-01-09
- Field: score
- Source value: `63-93`
- Canonical value: `65-93`
- Evidence: miami 1953-01-09: 65-93
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Florida State's frozen institutional row explicitly records a 63-93 loss at Miami on 1953-01-09. The reciprocal canonical representation has 65-93. The accepted Florida State research package preserves 63-93 without an unresolved-score designation; recommend the frozen source score while retaining reciprocal evidence.

### 10. DISCREPANCY-FSU-EXP-S1-00167-GAME_DATE

- Category: discrepancy
- Matchup: florida vs florida-state
- Dates: source 1954-12-27; canonical 1954-12-28
- Field: game_date
- Source value: `1954-12-27`
- Canonical value: `1954-12-28`
- Evidence: florida 1954-12-28: 1954-12-28
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: The frozen Florida State source explicitly records the Florida game as D27 in the Gator Bowl Tournament at Jacksonville, Florida, and the accepted research row is dated 1954-12-27. Recommend the accepted source date over the reciprocal canonical 1954-12-28 representation.

### 11. DISCREPANCY-FSU-EXP-S1-00183-GAME_TYPE

- Category: discrepancy
- Matchup: florida-state vs miami
- Date: 1955-02-25
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `REGULAR_SEASON`
- Evidence: miami 1955-02-25: REGULAR_SEASON
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Florida State's frozen row identifies the 1955-02-25 game at Miami as the Florida Intercollegiate Conference Championship, source round Championship, with accepted curated game type POSTSEASON. The postseason site research was explicitly exhausted and preserved. Recommend POSTSEASON over the reciprocal canonical regular-season representation.

### 12. DISCREPANCY-FSU-EXP-S1-00210-GAME_TYPE

- Category: discrepancy
- Matchup: florida-state vs miami
- Date: 1956-02-25
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `REGULAR_SEASON`
- Evidence: miami 1956-02-25: REGULAR_SEASON
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Florida State's frozen row identifies the 1956-02-25 game at Miami as the Florida Intercollegiate Conference Championship, source round Championship, with accepted curated game type POSTSEASON. The postseason site research was explicitly exhausted and preserved. Recommend POSTSEASON over the reciprocal canonical regular-season representation.
