# vcu onboarding review

Generated: 2026-11-14T20:23:45.602515+00:00
Input fingerprint: `9ce84d95fcf2bb77ac9c44cee8689ba610c44f432edacb324f2bcb497da0bb8a`
Approved plan: `b647eb83bfc2a3a3d71e9568471f3dc4c09a0c291034d82b8822473f5788079d`

## Preflight summary

- Source rows: 1,759
- Publication-eligible rows: 1,759
- Top-level rows: 1,650
- Publication-excluded researched rows: 0
- Existing matches: 1,658
- New canonical games: 101
- Identity reviews: 0
- Safe enrichment fields: 7
- Discrepancies: 2
- Conditional discrepancies: 0
- Canonical-only site reviews: 0
- Affected existing public programs: alabama, arizona-state, arkansas, auburn, baylor, boise-state, boston-college, butler, byu, california, cincinnati, colorado, colorado-state, davidson, dayton, depaul, duke, duquesne, fairleigh-dickinson, florida-state, fordham, george-mason, george-washington, georgetown, georgia, georgia-tech, houston, illinois, indiana, iowa, iowa-state, kansas, kansas-state, la-salle, long-island-university, louisville, loyola-chicago, lsu, marquette, maryland, miami, michigan, michigan-state, minnesota, mississippi-state, missouri, nc-state, north-carolina, northwestern, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, penn-state, pittsburgh, providence, purdue, rhode-island, richmond, rutgers, saint-joseph-s, saint-louis, seton-hall, smu, st-bonaventure, st-john-s, syracuse, tcu, tennessee, texas, texas-a-m, ucf, ucla, uconn, usc, utah, utah-state, vanderbilt, villanova, virginia, virginia-tech, wagner, wake-forest, west-virginia, wisconsin, xavier

## Blockers

- None.

## Warnings

- None.

## Non-substantive site-gap provenance

- None.

## Owner decisions

### 1. DISCREPANCY-VCU-EXP-1969-70-002-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: long-island-university vs vcu
- Dates: source 1969-12-02; canonical [unknown]
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: long-island-university [unknown]: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical 1OT. Long Island University's preserved reciprocal institutional source row is the exact 72-67 Virginia Commonwealth game and explicitly records 'ot'; VCU's frozen supplemental source row records overtime_periods=0. Preserve the conflicting VCU source assertion rather than normalizing it silently, while retaining the reciprocally supported canonical value.

### 2. DISCREPANCY-VCU-EXP-1970-71-009-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: minnesota vs vcu
- Date: 1970-12-28
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: minnesota 1970-12-28: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical 1OT. Minnesota's preserved institutional media-guide row for Dec. 28, 1970 at Virginia Commonwealth explicitly records 'L 56-63 (OT)', matching the exact VCU game; VCU's frozen supplemental source row records overtime_periods=0. Preserve the VCU source assertion as conflicting evidence while retaining the reciprocally supported canonical value.

### 3. POSTSEASON-CLASSIFICATION-VCU-1977-78-027

- Category: postseason_classification
- Matchup: vcu vs georgetown
- Date: 1978-03-01
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 1 ^at Georgetown W 88-75
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. Prior accepted VCU Stage 2 authority already adjudicated this exact decision: the row is ECAC regional/other-postseason or CBI, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 4. POSTSEASON-CLASSIFICATION-VCU-1977-78-028

- Category: postseason_classification
- Matchup: vcu vs st-bonaventure
- Date: 1978-03-04
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 4 &vs. St. Bonaventure (:03) L 61-63
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. Prior accepted VCU Stage 2 authority already adjudicated this exact decision: the row is ECAC regional/other-postseason or CBI, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 5. POSTSEASON-CLASSIFICATION-VCU-2009-10-032

- Category: postseason_classification
- Matchup: vcu vs george-washington
- Date: 2010-03-16
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 16 %at George Washington W 79-73
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. Prior accepted VCU Stage 2 authority already adjudicated this exact decision: the row is ECAC regional/other-postseason or CBI, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 6. POSTSEASON-CLASSIFICATION-VCU-2009-10-033

- Category: postseason_classification
- Matchup: vcu vs charleston
- Date: 2010-03-22
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 22 %CHARLESTON W 93-86
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. Prior accepted VCU Stage 2 authority already adjudicated this exact decision: the row is ECAC regional/other-postseason or CBI, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 7. POSTSEASON-CLASSIFICATION-VCU-2009-10-034

- Category: postseason_classification
- Matchup: vcu vs boston-university
- Date: 2010-03-24
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 24 %BOSTON UNIVERSITY W 88-75
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. Prior accepted VCU Stage 2 authority already adjudicated this exact decision: the row is ECAC regional/other-postseason or CBI, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 8. POSTSEASON-CLASSIFICATION-VCU-2009-10-035

- Category: postseason_classification
- Matchup: vcu vs saint-louis
- Date: 2010-03-29
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 29 %SAINT LOUIS W 68-56
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. Prior accepted VCU Stage 2 authority already adjudicated this exact decision: the row is ECAC regional/other-postseason or CBI, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 9. POSTSEASON-CLASSIFICATION-VCU-2009-10-036

- Category: postseason_classification
- Matchup: vcu vs saint-louis
- Date: 2010-03-31
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 31 %at Saint Louis W 71-65
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. Prior accepted VCU Stage 2 authority already adjudicated this exact decision: the row is ECAC regional/other-postseason or CBI, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.
