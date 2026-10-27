# gonzaga onboarding review

Generated: 2026-10-27T13:21:14.091468+00:00
Input fingerprint: `342773aa9ed265b88c7b6e7bb69ad32a5043eff0dbd85f6ff3e826bdf4ef00db`
Approved plan: `93fef75167acf9c861bc87a4e6279909d60ed51429190245cc02bca565b1a542`

## Preflight summary

- Source rows: 2,053
- In-scope rows: 2,053
- Pre-cutoff researched rows: 0
- Existing matches: 426
- New canonical games: 1,623
- Identity reviews: 4
- Safe enrichment fields: 659
- Discrepancies: 57
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
- Decision: `USE_SOURCE`
- Basis: Recommend NEUTRAL from the frozen Gonzaga source. Gonzaga's accepted Stage 3A row is explicitly curated NEUTRAL and the year-by-year '+' marker is documented as Coeur d'Alene, Idaho. Gonzaga's later official series history separately says the 71-70 Jan. 30, 1960 meeting occurred in Coeur d'Alene and that the 2017 meeting was the first Gonzaga-Creighton game in Spokane. Creighton's reciprocal row says 'at Gonzaga'; preserve that disagreement for Gate 1 rather than replacing the accepted target-school Research conclusion.

### 2. DISCREPANCY-GONZAGA-1960-61-009-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs st-john-s
- Date: 1960-12-22
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: st-john-s 1960-12-22: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Recommend NORMALIZE_SOURCE_TO_CANONICAL. The frozen Gonzaga row has OPPONENT_HOME but no source marker or site-research basis supporting that H/A/N choice. St. John's accepted institutional media-guide row explicitly marks the exact Dec. 22, 1960 game 'Gonzaga (N)' and its season note places the game at Fordham University in the Bronx. Canonical NEUTRAL is therefore supported, and the target curated site classification should be normalized only after Owner Gate 1 approval while raw_text remains preserved.

### 3. IDENTITY-GONZAGA-1961-62-019

- Category: identity
- Matchup: gonzaga vs washington-state
- Dates: source 1962-02-05; canonical 1961-12-11;1962-02-08
- Field: game_identity
- Source value: `date=1962-02-05; score=74-61`
- Canonical value: `CBBG-0116649;CBBG-0116660`
- Evidence: CBBG-0116649 1961-1962 1961-12-11 73-74 sources=washington-state; CBBG-0116660 1961-1962 1962-02-08 74-61 sources=washington-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0116660`
- Basis: Match CBBG-0116660. The frozen Gonzaga row is W 74-61 over Washington State and SOURCE_PROGRAM_HOME at Spokane Coliseum; Washington State's reciprocal 1962-02-08 game is a 61-74 loss at Gonzaga. The other candidate, CBBG-0116649, is Washington State's 74-73 overtime win on 1961-12-11 and corresponds to Gonzaga's separate accepted 1961-12-11 row, not this source row.

### 4. CONDITIONAL-DISCREPANCY-GONZAGA-1961-62-019-CBBG-0116649-GAME_DATE

- Category: conditional_discrepancy
- Matchup: gonzaga vs washington-state
- Dates: source 1962-02-05; canonical 1961-12-11
- Field: game_date
- Source value: `1962-02-05`
- Canonical value: `1961-12-11`
- Evidence: washington-state 1961-12-11: 1961-12-11
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0116660
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
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0116660
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
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0116660
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
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0116660
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0116649`

### 8. CONDITIONAL-DISCREPANCY-GONZAGA-1961-62-019-CBBG-0116660-GAME_DATE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Dates: source 1962-02-05; canonical 1962-02-08
- Field: game_date
- Source value: `1962-02-05`
- Canonical value: `1962-02-08`
- Evidence: washington-state 1962-02-08: 1962-02-08
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the curated Gonzaga date from 1962-02-05 to canonical 1962-02-08. Opponent, mirrored 74-61 score/result, and home relationship identify one game; preserve Gonzaga raw_text showing '2/5' as literal source evidence.
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
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_A_HOME assertion for the 1970-01-03 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 10. DISCREPANCY-GONZAGA-1970-71-011-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1971-01-11; canonical 1971-01-12
- Field: game_date
- Source value: `1971-01-11`
- Canonical value: `1971-01-12`
- Evidence: boise-state 1971-01-12: 1971-01-12
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the curated Gonzaga date from 1971-01-11 to 1971-01-12; exact reciprocal score/result/site establish the identity while Gonzaga raw_text retains the printed 1/11 date.

### 11. DISCREPANCY-GONZAGA-1971-72-005-SCORE

- Category: discrepancy
- Matchup: gonzaga vs oregon
- Date: 1971-12-11
- Field: score
- Source value: `69-87`
- Canonical value: `60-87`
- Evidence: oregon 1971-12-11: 60-87
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-1971-72-005, the frozen target-school value 69-87 conflicts with reciprocal canonical 60-87; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 12. DISCREPANCY-GONZAGA-1971-72-021-SITE_TYPE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Date: 1972-02-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: boise-state 1972-02-18: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend UNKNOWN from the frozen Gonzaga Research conclusion. Stage 3A-1 explicitly recorded an authoritative unresolved site conflict after bounded convergence: Gonzaga's series material treated the 1972 game as Gonzaga home, while Boise State's official record book treats the Feb. 18 game as Boise State home. Research therefore deliberately preserved UNKNOWN. Current canonical TEAM_A_HOME selects only one side of that unresolved conflict, so the recommendation is to restore UNKNOWN rather than manufacture certainty.

### 13. DISCREPANCY-GONZAGA-1972-73-009-SCORE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Date: 1973-01-05
- Field: score
- Source value: `58-73`
- Canonical value: `56-73`
- Evidence: boise-state 1973-01-05: 56-73
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-1972-73-009, the frozen target-school value 58-73 conflicts with reciprocal canonical 56-73; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 14. DISCREPANCY-GONZAGA-1973-74-004-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1973-12-10
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1973-12-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_A_HOME assertion for the 1973-12-10 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 15. DISCREPANCY-GONZAGA-1973-74-023-SCORE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Date: 1974-02-16
- Field: score
- Source value: `63-77`
- Canonical value: `63-75`
- Evidence: boise-state 1974-02-16: 63-75
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-1973-74-023, the frozen target-school value 63-77 conflicts with reciprocal canonical 63-75; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 16. DISCREPANCY-GONZAGA-1974-75-010-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1975-01-02
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1975-01-02: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_A_HOME assertion for the 1975-01-02 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 17. IDENTITY-GONZAGA-1975-76-004

- Category: identity
- Matchup: gonzaga vs creighton
- Dates: source 1975-12-11; canonical 1975-12-09
- Field: game_identity
- Source value: `date=1975-12-11; score=62-70`
- Canonical value: `CBBG-0149289`
- Evidence: CBBG-0149289 1975-1976 1975-12-09 70-62 sources=creighton
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0149289`
- Basis: Match CBBG-0149289. Gonzaga records a 62-70 loss at Creighton; Creighton records a 70-62 home win on 1975-12-09. Exact mirrored score/result/site establish one game.

### 18. CONDITIONAL-DISCREPANCY-GONZAGA-1975-76-004-CBBG-0149289-GAME_DATE

- Category: discrepancy
- Matchup: creighton vs gonzaga
- Dates: source 1975-12-11; canonical 1975-12-09
- Field: game_date
- Source value: `1975-12-11`
- Canonical value: `1975-12-09`
- Evidence: creighton 1975-12-09: 1975-12-09
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the curated Gonzaga date from 1975-12-11 to 1975-12-09 while preserving the raw 12/11 source text.
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
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_A_HOME assertion for the 1976-01-25 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 20. DISCREPANCY-GONZAGA-1976-77-003-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1976-12-03
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1976-12-03: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_B_HOME assertion for the 1976-12-03 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 21. DISCREPANCY-GONZAGA-1976-77-014-SITE_TYPE

- Category: discrepancy
- Matchup: creighton vs gonzaga
- Date: 1977-01-15
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: creighton 1977-01-15: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga OPPONENT_HOME classification, which in canonical orientation means Creighton home. Gonzaga's own later official series history says Creighton's 100-83 win on Jan. 15, 1977 was in Omaha, Nebraska. That exact-game statement supports Creighton home and directly conflicts with the current Creighton reciprocal row's 'at Gonzaga' label. Use the target-school conclusion and preserve the reciprocal disagreement for Gate 1.

### 22. DISCREPANCY-GONZAGA-1978-79-008-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1978-12-13
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1978-12-13: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_B_HOME assertion for the 1978-12-13 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 23. DISCREPANCY-GONZAGA-1979-80-004-SCORE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1979-12-05
- Field: score
- Source value: `58-75`
- Canonical value: `48-75`
- Evidence: washington-state 1979-12-05: 48-75
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-1979-80-004, the frozen target-school value 58-75 conflicts with reciprocal canonical 48-75; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 24. DISCREPANCY-GONZAGA-1980-81-005-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1980-12-13
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1980-12-13: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_B_HOME assertion for the 1980-12-13 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 25. DISCREPANCY-GONZAGA-1981-82-002-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1981-12-02
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1981-12-02: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_A_HOME assertion for the 1981-12-02 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 26. DISCREPANCY-GONZAGA-1982-83-003-SCORE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1982-12-01
- Field: score
- Source value: `53-73`
- Canonical value: `53-75`
- Evidence: washington-state 1982-12-01: 53-75
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-1982-83-003, the frozen target-school value 53-73 conflicts with reciprocal canonical 53-75; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 27. DISCREPANCY-GONZAGA-1982-83-003-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1982-12-01
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1982-12-01: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_B_HOME assertion for the 1982-12-01 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 28. DISCREPANCY-GONZAGA-1983-84-007-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1983-12-12
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1983-12-12: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_A_HOME assertion for the 1983-12-12 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 29. DISCREPANCY-GONZAGA-1983-84-010-SCORE

- Category: discrepancy
- Matchup: gonzaga vs oregon
- Date: 1983-12-29
- Field: score
- Source value: `52-72`
- Canonical value: `53-72`
- Evidence: oregon 1983-12-29: 53-72
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-1983-84-010, the frozen target-school value 52-72 conflicts with reciprocal canonical 53-72; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 30. DISCREPANCY-GONZAGA-1985-86-004-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1985-12-02
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1985-12-02: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_A_HOME assertion for the 1985-12-02 Washington State game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1.

### 31. DISCREPANCY-GONZAGA-1985-86-009-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs iowa
- Date: 1985-12-23
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: iowa 1985-12-23: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_A_HOME assertion for the 1985-12-23 Iowa game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1. Iowa's accepted source row independently prints 'at Gonzaga' for the same 84-64 result, so the reciprocal conflict is explicit rather than inferred.

### 32. DISCREPANCY-GONZAGA-1989-90-006-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1989-12-09; canonical 1989-12-10
- Field: game_date
- Source value: `1989-12-09`
- Canonical value: `1989-12-10`
- Evidence: boise-state 1989-12-10: 1989-12-10
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the curated Gonzaga date from 1989-12-09 to 1989-12-10 while preserving the raw 12/9 source text.

### 33. DISCREPANCY-GONZAGA-1991-92-003-SCORE

- Category: discrepancy
- Matchup: baylor vs gonzaga
- Date: 1991-11-29
- Field: score
- Source value: `75-77`
- Canonical value: `57-87`
- Evidence: baylor 1991-11-29: 57-87
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-1991-92-003, the frozen target-school value 75-77 conflicts with reciprocal canonical 57-87; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 34. DISCREPANCY-GONZAGA-1991-92-005-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs usc
- Date: 1991-12-04
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: usc 1991-12-04: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL classification. The accepted Gonzaga Research row explicitly curates this exact game as NEUTRAL and identifies Spokane Coliseum in Spokane, Washington as the venue. The Stage 2 census carries a conflicting reciprocal/canonical TEAM_A_HOME assertion for the 1991-12-04 USC game. Implementation must not replace the accepted target-school historical conclusion merely because reciprocal evidence chose a home designation; preserve that disagreement for Owner Gate 1. USC's accepted reciprocal row classifies the same 77-60 result as OPPONENT_HOME, so the reciprocal conflict is explicit rather than inferred.

### 35. IDENTITY-GONZAGA-1992-93-003

- Category: identity
- Matchup: gonzaga vs usc
- Dates: source 1992-12-07; canonical 1992-12-05
- Field: game_identity
- Source value: `date=1992-12-07; score=59-77`
- Canonical value: `CBBG-0069448`
- Evidence: CBBG-0069448 1992-1993 1992-12-05 59-77 sources=usc
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0069448`
- Basis: Match CBBG-0069448. Gonzaga records a 59-77 loss at Southern California; USC records a 77-59 home win on 1992-12-05. Exact mirrored score/result/site establish one game.

### 36. CONDITIONAL-DISCREPANCY-GONZAGA-1992-93-003-CBBG-0069448-GAME_DATE

- Category: discrepancy
- Matchup: gonzaga vs usc
- Dates: source 1992-12-07; canonical 1992-12-05
- Field: game_date
- Source value: `1992-12-07`
- Canonical value: `1992-12-05`
- Evidence: usc 1992-12-05: 1992-12-05
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the curated Gonzaga date from 1992-12-07 to 1992-12-05 while preserving the raw 12/7 source text.
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
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the curated Gonzaga date from 1998-11-14 to 1998-11-13 while preserving the raw 11/14 source text.

### 38. DISCREPANCY-GONZAGA-1998-99-005-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1998-11-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 1998-11-28: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Accepted Gonzaga row is NEUTRAL at Numerica Veterans Arena; Gonzaga venue authority separately records exact 1998 Washington State Spokane Arena evidence and warns venue identity does not itself establish H/A/N. Preserve frozen target classification over reciprocal TEAM_A_HOME.

### 39. DISCREPANCY-GONZAGA-1998-99-009-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington
- Date: 1998-12-08
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington 1998-12-08: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Accepted Gonzaga row is NEUTRAL at Numerica Veterans Arena. Washington reciprocal says at Gonzaga/OPPONENT_HOME. Preserve the already-frozen target-school modern exact-venue conclusion and carry the reciprocal conflict to Gate 1.

### 40. DISCREPANCY-GONZAGA-1998-99-014-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1999-01-02; canonical 1999-01-03
- Field: game_date
- Source value: `1999-01-02`
- Canonical value: `1999-01-03`
- Evidence: boise-state 1999-01-03: 1999-01-03
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the curated Gonzaga date from 1999-01-02 to 1999-01-03. Preserve raw_text showing 1/2.

### 41. DISCREPANCY-GONZAGA-1998-99-014-SITE_TYPE

- Category: discrepancy
- Matchup: boise-state vs gonzaga
- Dates: source 1999-01-02; canonical 1999-01-03
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: boise-state 1999-01-03: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga OPPONENT_HOME assertion (canonical TEAM_A_HOME in the Boise State vs Gonzaga orientation). Gonzaga's raw row explicitly says 'at Boise State'; Boise State's reciprocal row marks Boise as away. Preserve the reciprocal disagreement for Owner Gate 1 rather than replacing the accepted target-school conclusion.

### 42. DISCREPANCY-GONZAGA-1999-00-003-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 1999-11-29
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington-state 1999-11-29: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Accepted Gonzaga row is NEUTRAL at Beasley Coliseum. Gonzaga venue authority independently records Beasley Coliseum as neutral_event_site for this exact accepted Stage 3A-3 game/site evidence. Preserve NEUTRAL over reciprocal TEAM_B_HOME.

### 43. DISCREPANCY-GONZAGA-1999-00-008-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington
- Date: 1999-12-13
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington 1999-12-13: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Accepted Gonzaga row is NEUTRAL at KeyArena. Gonzaga venue authority classifies KeyArena as neutral_event_site under accepted Battle in Seattle institutional history. Washington reciprocal calls the game home; preserve that disagreement for Gate 1.

### 44. IDENTITY-GONZAGA-2003-04-004

- Category: identity
- Matchup: gonzaga vs georgia
- Dates: source 2003-11-24; canonical 2003-11-29
- Field: game_identity
- Source value: `date=2003-11-24; score=82-76`
- Canonical value: `CBBG-0042638`
- Evidence: CBBG-0042638 2003-2004 2003-11-29 76-82 sources=georgia
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0042638`
- Basis: Match CBBG-0042638. Both institutional rows describe Gonzaga's 82-76 overtime win over Georgia in the same season; the exact mirrored score/result make FORCE_NEW unsupported despite the printed-date and site-classification conflicts.

### 45. CONDITIONAL-DISCREPANCY-GONZAGA-2003-04-004-CBBG-0042638-GAME_DATE

- Category: discrepancy
- Matchup: georgia vs gonzaga
- Dates: source 2003-11-24; canonical 2003-11-29
- Field: game_date
- Source value: `2003-11-24`
- Canonical value: `2003-11-29`
- Evidence: georgia 2003-11-29: 2003-11-29
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the curated Gonzaga date from 2003-11-24 to 2003-11-29 while preserving Gonzaga raw_text showing 11/24.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0042638`

### 46. CONDITIONAL-DISCREPANCY-GONZAGA-2003-04-004-CBBG-0042638-SITE_TYPE

- Category: discrepancy
- Matchup: georgia vs gonzaga
- Dates: source 2003-11-24; canonical 2003-11-29
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgia 2003-11-29: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the frozen Gonzaga NEUTRAL assertion. The accepted target row places the game at Numerica Veterans Arena in Spokane and is curated NEUTRAL; Georgia's reciprocal row labels the game 'at Gonzaga'. Preserve that institutional disagreement for Owner Gate 1; do not infer H/A/N from Spokane geography.
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
- Decision: `USE_SOURCE`
- Basis: Accepted Gonzaga row is NEUTRAL at Hearnes Center. Gonzaga venue authority independently records this exact Hearnes Center assignment as neutral_event_site from accepted Stage 3A-3 exact-game/site evidence. Missouri reciprocal says SOURCE_PROGRAM_HOME; do not silently reopen the frozen target conclusion.

### 48. DISCREPANCY-GONZAGA-2003-04-010-SCORE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 2003-12-28
- Field: score
- Source value: `95-58`
- Canonical value: `96-58`
- Evidence: washington-state 2003-12-28: 96-58
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-2003-04-010, the frozen target-school value 95-58 conflicts with reciprocal canonical 96-58; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 49. DISCREPANCY-GONZAGA-2005-06-008-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs oklahoma-state
- Date: 2005-12-10
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: oklahoma-state 2005-12-10: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Oklahoma State reciprocal explicitly records vs Gonzaga as NEUTRAL at KeyArena for the same 62-64 result. Gonzaga venue authority identifies KeyArena as Battle in Seattle neutral_event_site. This direct reciprocal exact-venue evidence supports canonical NEUTRAL over the conflicting Gonzaga SOURCE_PROGRAM_HOME row.

### 50. DISCREPANCY-GONZAGA-2006-07-003-SITE_TYPE

- Category: discrepancy
- Matchup: baylor vs gonzaga
- Date: 2006-11-15
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: baylor 2006-11-15: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Accepted Gonzaga row is NEUTRAL at Numerica Veterans Arena. Gonzaga venue authority records 2006 NIT Season Tip-Off institutional evidence and explicitly allows mixed HOME-exception/NEUTRAL use without geography inference. Baylor reciprocal says at Gonzaga; retain frozen target NEUTRAL and preserve conflict.

### 51. DISCREPANCY-GONZAGA-2006-07-009-SCORE

- Category: discrepancy
- Matchup: gonzaga vs texas
- Date: 2006-12-02
- Field: score
- Source value: `88-77`
- Canonical value: `87-77`
- Evidence: texas 2006-12-02: 87-77
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-2006-07-009, the frozen target-school value 88-77 conflicts with reciprocal canonical 87-77; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 52. DISCREPANCY-GONZAGA-2007-08-008-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs uconn
- Date: 2007-12-01
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: uconn 2007-12-01: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: UConn reciprocal explicitly classifies the same 82-85 game as NEUTRAL at TD Garden in Boston. Direct reciprocal H/A/N plus exact modern venue supports canonical NEUTRAL over Gonzaga OPPONENT_HOME.

### 53. DISCREPANCY-GONZAGA-2007-08-012-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs oklahoma
- Date: 2007-12-20
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: oklahoma 2007-12-20: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Oklahoma reciprocal explicitly prints vs. Gonzaga and is curated NEUTRAL for the same 72-68 result. Direct institutional H/A/N supports canonical NEUTRAL; no geography inference is required.

### 54. DISCREPANCY-GONZAGA-2007-08-015-SITE_TYPE

- Category: discrepancy
- Matchup: georgia vs gonzaga
- Date: 2008-01-05
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgia 2008-01-05: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Accepted Gonzaga row is NEUTRAL at Numerica Veterans Arena. Gonzaga venue authority separately records exact 2008 Georgia Spokane Arena evidence and notes mixed HOME-exception/NEUTRAL assignments. Georgia reciprocal says at Gonzaga; preserve conflict and retain frozen target NEUTRAL.

### 55. DISCREPANCY-GONZAGA-2014-15-006-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs st-john-s
- Date: 2014-11-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-john-s 2014-11-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted Gonzaga row classifies the 2014-11-28 St. John's game as NEUTRAL at Madison Square Garden. Gonzaga venue authority independently identifies exact 2014 NIT Season Tip-Off evidence at Madison Square Garden and classifies the building as a neutral_event_site for this recurring/event context. St. John's reciprocal row calls the game SOURCE_PROGRAM_HOME at MSG, but also identifies the NIT Season Tip-Off regular-season tournament. Preserve the frozen Gonzaga tournament-neutral conclusion and carry the reciprocal home designation to Gate 1.

### 56. DISCREPANCY-GONZAGA-2014-15-009-SCORE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 2014-12-10
- Field: score
- Source value: `81-66`
- Canonical value: `81-68`
- Evidence: washington-state 2014-12-10: 81-68
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-2014-15-009, the frozen target-school value 81-66 conflicts with reciprocal canonical 81-68; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 57. DISCREPANCY-GONZAGA-2014-15-009-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs washington-state
- Date: 2014-12-10
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: washington-state 2014-12-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted Gonzaga row classifies the 2014-12-10 Washington State game as NEUTRAL at Numerica Veterans Arena / Spokane Arena. Gonzaga venue authority explicitly treats Spokane Arena as a mixed-use physical venue with independently established per-game HOME exceptions and NEUTRAL assignments; venue identity or Spokane geography never establishes H/A/N. This date is not one of the registry's explicit HOME exceptions. Preserve the accepted target-school NEUTRAL classification over the reciprocal TEAM_A_HOME assertion.

### 58. DISCREPANCY-GONZAGA-2016-17-009-SCORE

- Category: discrepancy
- Matchup: gonzaga vs washington
- Date: 2016-12-07
- Field: score
- Source value: `98-71`
- Canonical value: `86-71`
- Evidence: washington 2016-12-07: 86-71
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-2016-17-009, the frozen target-school value 98-71 conflicts with reciprocal canonical 86-71; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 59. DISCREPANCY-GONZAGA-2017-18-006-GAME_DATE

- Category: discrepancy
- Matchup: gonzaga vs texas
- Dates: source 2017-11-26; canonical 2017-11-25
- Field: game_date
- Source value: `2017-11-26`
- Canonical value: `2017-11-25`
- Evidence: texas 2017-11-25: 2017-11-25
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the curated Gonzaga date from 2017-11-26 to 2017-11-25 while preserving the raw 11/26 source text.

### 60. DISCREPANCY-GONZAGA-2020-21-004-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs iowa
- Date: 2020-12-19
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: iowa 2020-12-19: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted Gonzaga row classifies the 2020-12-19 Iowa game as NEUTRAL. Iowa's own accepted reciprocal raw_text says 'Gonzaga (n)' for the same 88-99 result even though Iowa's curated_site_type is SOURCE_PROGRAM_HOME. The raw institutional neutral marker directly contradicts the curated reciprocal home assertion, so the Gonzaga NEUTRAL conclusion is the stronger preserved historical reading.

### 61. DISCREPANCY-GONZAGA-2021-22-009-SITE_TYPE

- Category: discrepancy
- Matchup: alabama vs gonzaga
- Date: 2021-12-04
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: alabama 2021-12-04: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted Gonzaga row classifies the 2021-12-04 Alabama game as NEUTRAL at Climate Pledge Arena in Seattle. Alabama's accepted reciprocal row uses source_site_candidate 'Neutral', raw_text 'vs. Gonzaga', and event 'Battle in Seattle (Seattle, Wash.)' while its curated_site_type remains UNKNOWN. Gonzaga venue authority treats KeyArena/Climate Pledge Arena as the Battle in Seattle neutral_event_site. Direct reciprocal source wording therefore supports, rather than contradicts, Gonzaga NEUTRAL.

### 62. DISCREPANCY-GONZAGA-2022-23-004-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs kentucky
- Date: 2022-11-20
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: kentucky 2022-11-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted Gonzaga row classifies the 2022-11-20 Kentucky game as NEUTRAL at Numerica Veterans Arena / Spokane Arena. Kentucky's reciprocal record says 'at Gonzaga', creating a genuine institutional conflict. Gonzaga venue authority explicitly distinguishes Spokane Arena's independently established per-game HOME exceptions from NEUTRAL assignments and warns against geography-only inference. This game is not one of the registry's explicit HOME-exception dates; retain the frozen Gonzaga NEUTRAL conclusion for Gate 1.

### 63. DISCREPANCY-GONZAGA-2024-25-001-SITE_TYPE

- Category: discrepancy
- Matchup: baylor vs gonzaga
- Date: 2024-11-04
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: baylor 2024-11-04: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted Gonzaga row classifies the 2024-11-04 Baylor game as NEUTRAL at Numerica Veterans Arena / Spokane Arena. Baylor's accepted reciprocal row says 'at Gonzaga', but Gonzaga's venue authority permits both exact HOME exceptions and NEUTRAL games at Spokane Arena and identifies only different dates as HOME exceptions. Preserve the accepted target-school per-game NEUTRAL classification; do not convert same-city location into HOME.

### 64. DISCREPANCY-GONZAGA-2024-25-013-SCORE

- Category: discrepancy
- Matchup: gonzaga vs ucla
- Date: 2024-12-28
- Field: score
- Source value: `62-65`
- Canonical value: `71-73`
- Evidence: ucla 2024-12-28: 71-73
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted superseding score-only Gonzaga Research Freeze restored this structured score from the 2026-27 Gonzaga Men's Basketball Record Book and passed the bounded score-specific Stage 6 self-challenge with zero remaining blank scores, zero score/result mismatches, and no non-score field changes. For GONZAGA-2024-25-013, the frozen target-school value 62-65 conflicts with reciprocal canonical 71-73; recommend the accepted frozen Gonzaga score and preserve the reciprocal disagreement for Owner Gate 1 rather than reverting the repaired Research authority.

### 65. DISCREPANCY-GONZAGA-2025-26-002-SITE_TYPE

- Category: discrepancy
- Matchup: gonzaga vs oklahoma
- Date: 2025-11-08
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: oklahoma 2025-11-08: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: USE_SOURCE. The accepted Gonzaga row classifies the 2025-11-08 Oklahoma game as NEUTRAL at Spokane Arena. Oklahoma's official completed schedule labels the game Away at Gonzaga, creating a direct institutional conflict. Gonzaga venue authority again treats Spokane Arena as mixed-use and lists explicit HOME exceptions on other dates, while the frozen Gonzaga row for this exact date is NEUTRAL. Preserve that target-school conclusion for Gate 1 rather than inferring HOME from Spokane or Oklahoma's away label.

### 66. ACCOMPLISHMENTS-GONZAGA

- Category: accomplishments
- Matchup: gonzaga
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"NATIONAL_RUNNER_UP","best_finish_year":"2021","conference_regular_season_championships":"29","conference_tournament_championships":"23","final_four_appearances":"2","national_championships":"0","ncaa_tournament_appearances":"28"}`
- Canonical value: `{"best_finish_key":"NATIONAL_RUNNER_UP","best_finish_year":2021,"final_four_appearances":2,"national_championships":0,"ncaa_tournament_appearances":28}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `APPLY_ACCOMPLISHMENT_PATCH`
- Basis: Authoritative Gonzaga Athletics verification supports 27 WCC regular-season championships through 2025-26, 23 WCC Tournament championships, 28 NCAA Tournament appearances, two Final Four/national-championship-game appearances, zero national championships, and NATIONAL_RUNNER_UP with latest such finish in 2021. The repository owner baseline is therefore correct in every accomplishment field except conference_regular_season_championships, which is stale at 29 and should be corrected to 27. Current official Gonzaga sources explicitly call the 2025-26 title the program's 27th WCC regular-season championship and 23rd WCC Tournament title; current NCAA notes call 2026 the 28th overall NCAA Tournament appearance; Gonzaga's current coaching/history materials identify national title-game appearances in 2017 and 2021.

### 67. PUBLICATION-GONZAGA

- Category: publication
- Matchup: gonzaga
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 2,053 in-scope source rows; 4 identity reviews; 52 definite and 9 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `ENABLE_PUBLIC_PAGE`
- Basis: ENABLE_PUBLIC_PAGE is the mature recommendation because the score-restored Stage 2 census covers 2,053 in-scope source rows and all 67 current Stage 2 decisions now have explicit recommendations, including the accepted score-restoration consequences and authoritative accomplishment correction. This recommendation does not itself publish anything: publication remains conditional on exact-map proposal rehearsal, explicit Owner Gate 1 approval, sealed apply, validation, Preview, explicit Owner Gate 2 approval, merge, and Production proof.
