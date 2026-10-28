# colorado-state onboarding review

Generated: 2026-10-28T21:23:53.271082+00:00
Input fingerprint: `1122ca53b97129f7adf6703de1437be03f669196473157d4912dfce72fed8fed`
Approved plan: `a54db55d5c07b49cb3c38c17e1f6fcd9afcb25452ab3462ffb5f4986bdb30244`

## Preflight summary

- Source rows: 2,765
- In-scope rows: 2,765
- Pre-cutoff researched rows: 0
- Existing matches: 828
- New canonical games: 1,929
- Identity reviews: 8
- Safe enrichment fields: 1,783
- Discrepancies: 66
- Conditional discrepancies: 29
- Canonical-only site reviews: 0
- Affected existing public programs: alabama, arizona, arizona-state, arkansas, auburn, baylor, boise-state, boston-college, byu, california, central-connecticut, chicago-state, colorado, creighton, duke, florida, florida-state, georgia-tech, gonzaga, houston, indiana, iowa, iowa-state, kansas, kansas-state, louisville, maryland, michigan, michigan-state, minnesota, mississippi-state, missouri, nc-state, nebraska, north-carolina, northwestern, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, penn-state, purdue, rutgers, smu, south-carolina, stanford, syracuse, tcu, texas, texas-a-m, texas-tech, ucla, usc, utah, utah-state, villanova, virginia, virginia-tech, washington, washington-state, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. DISCREPANCY-CSU-S1-00012-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1906-03-02
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: colorado 1906-03-02: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: CSU unmarked HOME/Old Main conflicts with Colorado Boulder HOME/University Gymnasium.

### 2. DISCREPANCY-CSU-S1-00014-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1907-01-11
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: colorado 1907-01-11: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: CSU explicitly at Colorado conflicts with Colorado explicitly at Colorado State.

### 3. IDENTITY-CSU-S1-00022

- Category: identity
- Matchup: colorado-state vs colorado
- Dates: source 1908-01-10; canonical 1907-12-31;1908-02-07
- Field: game_identity
- Source value: `date=1908-01-10; score=29-21`
- Canonical value: `CBBG-0086799;CBBG-0086806`
- Evidence: CBBG-0086799 1907-1908 1907-12-31 21-29 sources=colorado; CBBG-0086806 1907-1908 1908-02-07 43-27 sources=colorado
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0086799`
- Basis: Identical score from opposite perspectives, compatible home/away, and first of exactly two meetings in both institutional seasonal records; second meeting is distinct.

### 4. CONDITIONAL-DISCREPANCY-CSU-S1-00022-CBBG-0086799-GAME_DATE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1908-01-10; canonical 1907-12-31
- Field: game_date
- Source value: `1908-01-10`
- Canonical value: `1907-12-31`
- Evidence: colorado 1907-12-31: 1907-12-31
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Score, game order, and site strongly support the proposed first-game identity, but CSU Jan 10 and Colorado Dec 31 cannot be resolved from these institutional records alone. CSU official season schedule reiterates Jan 10.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086799`

### 5. CONDITIONAL-DISCREPANCY-CSU-S1-00022-CBBG-0086806-GAME_DATE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1908-01-10; canonical 1908-02-07
- Field: game_date
- Source value: `1908-01-10`
- Canonical value: `1908-02-07`
- Evidence: colorado 1908-02-07: 1908-02-07
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086799
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086806`

### 6. CONDITIONAL-DISCREPANCY-CSU-S1-00022-CBBG-0086806-SCORE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1908-01-10; canonical 1908-02-07
- Field: score
- Source value: `21-29`
- Canonical value: `43-27`
- Evidence: colorado 1908-02-07: 43-27
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086799
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086806`

### 7. CONDITIONAL-DISCREPANCY-CSU-S1-00022-CBBG-0086806-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1908-01-10; canonical 1908-02-07
- Field: result_winner_team_key
- Source value: `colorado-state`
- Canonical value: `colorado`
- Evidence: colorado 1908-02-07: colorado
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086799
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086806`

### 8. DISCREPANCY-CSU-S1-00025-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1908-02-07
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: colorado 1908-02-07: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: CSU at Colorado conflicts with Colorado at CSU, despite the same reciprocal 43-27 result.

### 9. DISCREPANCY-CSU-S1-00032-GAME_DATE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1911-02-04; canonical 1911-02-03
- Field: game_date
- Source value: `1911-02-04`
- Canonical value: `1911-02-03`
- Evidence: colorado 1911-02-03: 1911-02-03
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Two institutional historical ledgers disagree on the date; CSU record-book/season-schedule account and published reciprocal both have a distinct exact date. Preserve both, and do not select the already-published canonical date by default.

### 10. DISCREPANCY-CSU-S1-00033-SCORE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1911-02-10
- Field: score
- Source value: `37-21`
- Canonical value: `33-17`
- Evidence: colorado 1911-02-10: 33-17
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Both accepted ledgers concern the same Feb 10 game but disagree on both scores (CSU L 21-37; Colorado W 33-17). No independent tiebreaker in accepted materials.

### 11. DISCREPANCY-CSU-S1-00041-GAME_DATE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1912-02-12; canonical 1912-02-13
- Field: game_date
- Source value: `1912-02-12`
- Canonical value: `1912-02-13`
- Evidence: colorado 1912-02-13: 1912-02-13
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Two institutional historical ledgers disagree on the date; CSU record-book/season-schedule account and published reciprocal both have a distinct exact date. Preserve both, and do not select the already-published canonical date by default.

### 12. DISCREPANCY-CSU-S1-00048-GAME_DATE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1913-02-08; canonical 1913-02-07
- Field: game_date
- Source value: `1913-02-08`
- Canonical value: `1913-02-07`
- Evidence: colorado 1913-02-07: 1913-02-07
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Two institutional historical ledgers disagree on the date; CSU record-book/season-schedule account and published reciprocal both have a distinct exact date. Preserve both, and do not select the already-published canonical date by default.

### 13. DISCREPANCY-CSU-S1-00060-SCORE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1914-02-28
- Field: score
- Source value: `26-23`
- Canonical value: `23-26`
- Evidence: colorado 1914-02-28: 23-26
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Critical paired result/winner contradiction: both CSU (23-26) and Colorado (23-26) claim a loss on the same date. Site conflict also persists. Resolve neither score nor winner by silently reversing a result; the winner discrepancy is a separate Stage 2 decision.

### 14. DISCREPANCY-CSU-S1-00060-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1914-02-28
- Field: result_winner_team_key
- Source value: `colorado`
- Canonical value: `colorado-state`
- Evidence: colorado 1914-02-28: colorado-state
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: The institutional records agree on date and opponent, and their at/vs designations are reciprocal. But both explicitly record a 23-26 loss. If both program-perspective scores were correct, each school would have lost the same match, which is impossible. Canonical winner follows Colorado reciprocal; Colorado State source winner follows CSU. Neither is independently established as historically correct. No inference that one school is more authoritative.

### 15. DISCREPANCY-CSU-S1-00066-SCORE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1915-02-10
- Field: score
- Source value: `12-39`
- Canonical value: `21-39`
- Evidence: colorado 1915-02-10: 21-39
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Both ledgers agree CSU scored 39 and won; Colorado losing score is 12 (CSU) vs 21 (Colorado). Colorado online opponent history also reports 21-39 but is institutionally overlapping corroboration, not independent decisive proof.

### 16. DISCREPANCY-CSU-S1-00076-SCORE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1916-02-08
- Field: score
- Source value: `27-23`
- Canonical value: `37-23`
- Evidence: colorado 1916-02-08: 37-23
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Site dispute separately preserved; CSU L 23-27, Colorado W 37-23, so winner and CSU 23 agree; Colorado score differs by 10.

### 17. DISCREPANCY-CSU-S1-00076-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1916-02-08
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: colorado 1916-02-08: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Both teams claim HOME, and CSU/Colorado scores also conflict (27-23 versus 37-23).

### 18. DISCREPANCY-CSU-S1-00083-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1916-03-11
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: colorado 1916-03-11: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Each school claims AWAY, despite identical result.

### 19. IDENTITY-CSU-S1-00089

- Category: identity
- Matchup: colorado-state vs colorado
- Dates: source 1917-02-02; canonical 1917-02-06;1917-02-13
- Field: game_identity
- Source value: `date=1917-02-02; score=24-33`
- Canonical value: `CBBG-0086881;CBBG-0086883`
- Evidence: CBBG-0086881 1916-1917 1917-02-06 33-24 sources=colorado; CBBG-0086883 1916-1917 1917-02-13 35-21 sources=colorado
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0086881`
- Basis: Exact reciprocal score and compatible site. The other season meeting is separately present on February 13 with reciprocal score 21-35.

### 20. CONDITIONAL-DISCREPANCY-CSU-S1-00089-CBBG-0086881-GAME_DATE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1917-02-02; canonical 1917-02-06
- Field: game_date
- Source value: `1917-02-02`
- Canonical value: `1917-02-06`
- Evidence: colorado 1917-02-06: 1917-02-06
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Two institutional historical ledgers disagree on the date; CSU record-book/season-schedule account and published reciprocal both have a distinct exact date. Preserve both, and do not select the already-published canonical date by default.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086881`

### 21. CONDITIONAL-DISCREPANCY-CSU-S1-00089-CBBG-0086883-GAME_DATE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1917-02-02; canonical 1917-02-13
- Field: game_date
- Source value: `1917-02-02`
- Canonical value: `1917-02-13`
- Evidence: colorado 1917-02-13: 1917-02-13
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086881
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086883`

### 22. CONDITIONAL-DISCREPANCY-CSU-S1-00089-CBBG-0086883-SCORE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1917-02-02; canonical 1917-02-13
- Field: score
- Source value: `33-24`
- Canonical value: `35-21`
- Evidence: colorado 1917-02-13: 35-21
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086881
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086883`

### 23. CONDITIONAL-DISCREPANCY-CSU-S1-00089-CBBG-0086883-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1917-02-02; canonical 1917-02-13
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: colorado 1917-02-13: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086881
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086883`

### 24. IDENTITY-CSU-S1-00100

- Category: identity
- Matchup: colorado-state vs colorado
- Dates: source 1918-02-02; canonical 1918-02-05;1918-02-16
- Field: game_identity
- Source value: `date=1918-02-02; score=21-34`
- Canonical value: `CBBG-0086890;CBBG-0086893`
- Evidence: CBBG-0086890 1917-1918 1918-02-05 33-24 sources=colorado; CBBG-0086893 1917-1918 1918-02-16 35-21 sources=colorado
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0086890`
- Basis: Each institutional season ledger contains exactly two CSU-Colorado contests. This is the first meeting in each list, with matching away/home direction and closely spaced dates; the second dated February 16 is a separate paired meeting.

### 25. CONDITIONAL-DISCREPANCY-CSU-S1-00100-CBBG-0086890-GAME_DATE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1918-02-02; canonical 1918-02-05
- Field: game_date
- Source value: `1918-02-02`
- Canonical value: `1918-02-05`
- Evidence: colorado 1918-02-05: 1918-02-05
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Identity is only MODERATE confidence; first-game CSU Feb 2 and Colorado Feb 5 differ in date AND score. Second February 16 meeting also conflicts in site/score. No confident historical date authority.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086890`

### 26. CONDITIONAL-DISCREPANCY-CSU-S1-00100-CBBG-0086890-SCORE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1918-02-02; canonical 1918-02-05
- Field: score
- Source value: `34-21`
- Canonical value: `33-24`
- Evidence: colorado 1918-02-05: 33-24
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Selected first 1917-18 meeting has MODERATE identity confidence; scores disagree on both sides, 34-21 CSU claim vs 33-24 Colorado claim. Companion Feb 16 meeting also has score/site conflict. Do not force either outcome.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086890`

### 27. CONDITIONAL-DISCREPANCY-CSU-S1-00100-CBBG-0086893-GAME_DATE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1918-02-02; canonical 1918-02-16
- Field: game_date
- Source value: `1918-02-02`
- Canonical value: `1918-02-16`
- Evidence: colorado 1918-02-16: 1918-02-16
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086890
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086893`

### 28. CONDITIONAL-DISCREPANCY-CSU-S1-00100-CBBG-0086893-SCORE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1918-02-02; canonical 1918-02-16
- Field: score
- Source value: `34-21`
- Canonical value: `35-21`
- Evidence: colorado 1918-02-16: 35-21
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086890
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086893`

### 29. DISCREPANCY-CSU-S1-00103-SCORE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1918-02-16
- Field: score
- Source value: `27-21`
- Canonical value: `35-21`
- Evidence: colorado 1918-02-16: 35-21
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Feb 16 1918 second meeting: CSU L 21-27 at CSU home, Colorado W 35-21 at Colorado home, so both score and H/A/N conflict; preserve as independent competing institutional assertions.

### 30. DISCREPANCY-CSU-S1-00103-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1918-02-16
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: colorado 1918-02-16: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Both claim HOME; second-game scores also differ (27-21 versus 35-21). Retain link to contested 1917-18 two-game identity pair.

### 31. DISCREPANCY-CSU-S1-00115-SCORE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1919-02-21
- Field: score
- Source value: `41-21`
- Canonical value: `37-20`
- Evidence: colorado 1919-02-21: 37-20
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: CSU L 21-41 vs Colorado W 37-20, different both sides. No definitive independent adjudication.

### 32. DISCREPANCY-CSU-S1-00120-SCORE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1919-03-21
- Field: score
- Source value: `48-32`
- Canonical value: `48-31`
- Evidence: colorado 1919-03-21: 48-31
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 33. DISCREPANCY-CSU-S1-00122-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1920-01-24
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: colorado 1920-01-24: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Both institutions claim HOME despite exact reciprocal score.

### 34. DISCREPANCY-CSU-S1-00131-GAME_DATE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1921-01-28; canonical 1921-01-27
- Field: game_date
- Source value: `1921-01-28`
- Canonical value: `1921-01-27`
- Evidence: colorado 1921-01-27: 1921-01-27
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Two institutional historical ledgers disagree on the date; CSU record-book/season-schedule account and published reciprocal both have a distinct exact date. Preserve both, and do not select the already-published canonical date by default.

### 35. IDENTITY-CSU-S1-00143

- Category: identity
- Matchup: colorado-state vs colorado
- Dates: source 1922-01-27; canonical 1922-01-10;1922-02-03
- Field: game_identity
- Source value: `date=1922-01-27; score=20-24`
- Canonical value: `CBBG-0086924;CBBG-0086930`
- Evidence: CBBG-0086924 1921-1922 1922-01-10 24-20 sources=colorado; CBBG-0086930 1921-1922 1922-02-03 22-8 sources=colorado
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0086924`
- Basis: Exact score and complementary home/away. The other meeting matches the 22-8 score in both school ledgers, ruling out swapping the identities.

### 36. CONDITIONAL-DISCREPANCY-CSU-S1-00143-CBBG-0086924-GAME_DATE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1922-01-27; canonical 1922-01-10
- Field: game_date
- Source value: `1922-01-27`
- Canonical value: `1922-01-10`
- Evidence: colorado 1922-01-10: 1922-01-10
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado exact score and complementary site match the first 1921-22 game but gives Jan 10, while CSU official guide and season schedule give Jan 27; preserve 17-day disagreement.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086924`

### 37. CONDITIONAL-DISCREPANCY-CSU-S1-00143-CBBG-0086930-GAME_DATE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1922-01-27; canonical 1922-02-03
- Field: game_date
- Source value: `1922-01-27`
- Canonical value: `1922-02-03`
- Evidence: colorado 1922-02-03: 1922-02-03
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086924
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086930`

### 38. CONDITIONAL-DISCREPANCY-CSU-S1-00143-CBBG-0086930-SCORE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1922-01-27; canonical 1922-02-03
- Field: score
- Source value: `24-20`
- Canonical value: `22-8`
- Evidence: colorado 1922-02-03: 22-8
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086924
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086930`

### 39. CONDITIONAL-DISCREPANCY-CSU-S1-00143-CBBG-0086930-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1922-01-27; canonical 1922-02-03
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: colorado 1922-02-03: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086924
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086930`

### 40. IDENTITY-CSU-S1-00151

- Category: identity
- Matchup: colorado-state vs colorado
- Dates: source 1922-02-24; canonical 1922-01-10;1922-02-03
- Field: game_identity
- Source value: `date=1922-02-24; score=8-22`
- Canonical value: `CBBG-0086924;CBBG-0086930`
- Evidence: CBBG-0086924 1921-1922 1922-01-10 24-20 sources=colorado; CBBG-0086930 1921-1922 1922-02-03 22-8 sources=colorado
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0086930`
- Basis: Exact reciprocal score and home/away. The other 1921-22 meeting is separately paired by score 20-24.

### 41. CONDITIONAL-DISCREPANCY-CSU-S1-00151-CBBG-0086924-GAME_DATE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1922-02-24; canonical 1922-01-10
- Field: game_date
- Source value: `1922-02-24`
- Canonical value: `1922-01-10`
- Evidence: colorado 1922-01-10: 1922-01-10
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086930
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086924`

### 42. CONDITIONAL-DISCREPANCY-CSU-S1-00151-CBBG-0086924-SCORE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1922-02-24; canonical 1922-01-10
- Field: score
- Source value: `22-8`
- Canonical value: `24-20`
- Evidence: colorado 1922-01-10: 24-20
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086930
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086924`

### 43. CONDITIONAL-DISCREPANCY-CSU-S1-00151-CBBG-0086924-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1922-02-24; canonical 1922-01-10
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: colorado 1922-01-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0086930
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086924`

### 44. CONDITIONAL-DISCREPANCY-CSU-S1-00151-CBBG-0086930-GAME_DATE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Dates: source 1922-02-24; canonical 1922-02-03
- Field: game_date
- Source value: `1922-02-24`
- Canonical value: `1922-02-03`
- Evidence: colorado 1922-02-03: 1922-02-03
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado exact score/site match the other 1921-22 game but gives Feb 3, whereas CSU official guide and season schedule say Feb 24; preserve 21-day disagreement.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0086930`

### 45. DISCREPANCY-CSU-S1-00156-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1924-01-25
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: colorado 1924-01-25: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Both institutions claim AWAY despite exact reciprocal score.

### 46. DISCREPANCY-CSU-S1-00175-SITE_TYPE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1925-03-03
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: colorado 1925-03-03: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Both institutions claim AWAY despite exact reciprocal score.

### 47. DISCREPANCY-CSU-S1-00312-SCORE

- Category: discrepancy
- Matchup: colorado-state vs utah
- Date: 1937-01-02
- Field: score
- Source value: `25-42`
- Canonical value: `25-41`
- Evidence: utah 1937-01-02: 25-41
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 48. DISCREPANCY-CSU-S1-00346-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1939-01-13
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: utah-state 1939-01-13: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU supplies explicit at Utah State; Utah State accepted reciprocal retains UNKNOWN, not an opposing affirmative classification.

### 49. DISCREPANCY-CSU-S1-00348-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1939-01-21
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: utah-state 1939-01-21: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU supplies explicit unmarked Colorado State HOME plus venue and geography; Utah State accepted reciprocal retains UNKNOWN, not an opposing affirmative classification.

### 50. DISCREPANCY-CSU-S1-00374-SCORE

- Category: discrepancy
- Matchup: colorado-state vs utah
- Date: 1940-03-02
- Field: score
- Source value: `54-83`
- Canonical value: `52-83`
- Evidence: utah 1940-03-02: 52-83
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 51. DISCREPANCY-CSU-S1-00388-GAME_DATE

- Category: discrepancy
- Matchup: byu vs colorado-state
- Dates: source 1941-02-14; canonical 1941-02-15
- Field: game_date
- Source value: `1941-02-14`
- Canonical value: `1941-02-15`
- Evidence: byu 1941-02-15: 1941-02-15
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU media-guide ledger, official 1940-41 game schedule and its BYU opponent-history page consistently identify Friday Feb 14 for the 36-40 home loss; BYU preserved record book says Feb 15. Recommend CSU date, but do not mutate BYU source.

### 52. DISCREPANCY-CSU-S1-00394-SCORE

- Category: discrepancy
- Matchup: colorado-state vs kansas-state
- Date: 1941-12-10
- Field: score
- Source value: `27-30`
- Canonical value: `25-30`
- Evidence: kansas-state 1941-12-10: 25-30
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 53. DISCREPANCY-CSU-S1-00475-SCORE

- Category: discrepancy
- Matchup: colorado-state vs washington-state
- Date: 1946-12-16
- Field: score
- Source value: `31-57`
- Canonical value: `30-57`
- Evidence: washington-state 1946-12-16: 30-57
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 54. DISCREPANCY-CSU-S1-00501-SCORE

- Category: discrepancy
- Matchup: colorado-state vs nebraska
- Date: 1947-12-23
- Field: score
- Source value: `46-67`
- Canonical value: `47-67`
- Evidence: nebraska 1947-12-23: 47-67
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 55. DISCREPANCY-CSU-S1-00508-SCORE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1948-02-14
- Field: score
- Source value: `33-64`
- Canonical value: `45-64`
- Evidence: utah-state 1948-02-14: 45-64
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: CSU L 33-64 vs Utah State W 64-45: target losing-score conflict of 12 points, paired exact date. Accepted Utah State source does not establish H/A/N (its own site is UNKNOWN).

### 56. DISCREPANCY-CSU-S1-00508-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1948-02-14
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: utah-state 1948-02-14: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU supplies explicit at Utah State; Utah State accepted reciprocal retains UNKNOWN, not an opposing affirmative classification.

### 57. IDENTITY-CSU-S1-00509

- Category: identity
- Matchup: colorado-state vs byu
- Dates: source 1948-02-18; canonical 1948-01-24;1948-02-16
- Field: game_identity
- Source value: `date=1948-02-18; score=48-79`
- Canonical value: `CBBG-0107289;CBBG-0107293`
- Evidence: CBBG-0107289 1947-1948 1948-01-24 64-51 sources=byu; CBBG-0107293 1947-1948 1948-02-16 79-48 sources=byu
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0107293`
- Basis: Exact reciprocal score and home/away, while both schools separately list January 24 as the other game (BYU 64-51).

### 58. CONDITIONAL-DISCREPANCY-CSU-S1-00509-CBBG-0107289-GAME_DATE

- Category: conditional_discrepancy
- Matchup: byu vs colorado-state
- Dates: source 1948-02-18; canonical 1948-01-24
- Field: game_date
- Source value: `1948-02-18`
- Canonical value: `1948-01-24`
- Evidence: byu 1948-01-24: 1948-01-24
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0107293
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107289`

### 59. CONDITIONAL-DISCREPANCY-CSU-S1-00509-CBBG-0107289-SCORE

- Category: conditional_discrepancy
- Matchup: byu vs colorado-state
- Dates: source 1948-02-18; canonical 1948-01-24
- Field: score
- Source value: `79-48`
- Canonical value: `64-51`
- Evidence: byu 1948-01-24: 64-51
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0107293
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107289`

### 60. CONDITIONAL-DISCREPANCY-CSU-S1-00509-CBBG-0107289-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: byu vs colorado-state
- Dates: source 1948-02-18; canonical 1948-01-24
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: byu 1948-01-24: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0107293
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107289`

### 61. CONDITIONAL-DISCREPANCY-CSU-S1-00509-CBBG-0107293-GAME_DATE

- Category: discrepancy
- Matchup: byu vs colorado-state
- Dates: source 1948-02-18; canonical 1948-02-16
- Field: game_date
- Source value: `1948-02-18`
- Canonical value: `1948-02-16`
- Evidence: byu 1948-02-16: 1948-02-16
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: The single 79-48 February 1948 BYU meeting is securely identified against BYU Feb 16 and CSU Feb 18. No independent contemporary date evidence resolves two-day disagreement.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0107293`

### 62. DISCREPANCY-CSU-S1-00510-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1948-02-21
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: utah-state 1948-02-21: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU supplies explicit unmarked Colorado State HOME plus venue and geography; Utah State accepted reciprocal retains UNKNOWN, not an opposing affirmative classification.

### 63. IDENTITY-CSU-S1-00520

- Category: identity
- Matchup: colorado-state vs michigan
- Dates: source 1948-12-23; canonical 1948-12-18
- Field: game_identity
- Source value: `date=1948-12-23; score=37-56`
- Canonical value: `CBBG-0049238`
- Evidence: CBBG-0049238 1948-1949 1948-12-18 37-56 sources=michigan
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0049238`
- Basis: Exact reciprocal 56-37 score, opponent aliases refer to the same institution, compatible home/away and sole listed matchup this season.

### 64. CONDITIONAL-DISCREPANCY-CSU-S1-00520-CBBG-0049238-GAME_DATE

- Category: discrepancy
- Matchup: colorado-state vs michigan
- Dates: source 1948-12-23; canonical 1948-12-18
- Field: game_date
- Source value: `1948-12-23`
- Canonical value: `1948-12-18`
- Evidence: michigan 1948-12-18: 1948-12-18
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Exact 56-37 score and sole meeting support identity, but CSU official guide and season schedule date Dec 23 (schedule itself reports 37-57); Michigan preserved source says Dec 18 W 56-37. Preserve date and score tensions.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0049238`

### 65. DISCREPANCY-CSU-S1-00522-SCORE

- Category: discrepancy
- Matchup: auburn vs colorado-state
- Date: 1948-12-28
- Field: score
- Source value: `51-54`
- Canonical value: `41-46`
- Evidence: auburn 1948-12-28: 41-46
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Same Dec 28 1948 Oklahoma City neutral contest; CSU says W 54-51, Auburn frozen source and official schedule say L 41-46. A third-party score compilation lists Auburn 51-CSU 54, but may depend on CSU material, so no independent tiebreaker. Keep contested rather than use numerical plausibility.

### 66. DISCREPANCY-CSU-S1-00530-SCORE

- Category: discrepancy
- Matchup: colorado-state vs utah
- Date: 1949-01-17
- Field: score
- Source value: `37-69`
- Canonical value: `35-69`
- Evidence: utah 1949-01-17: 35-69
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 67. DISCREPANCY-CSU-S1-00576-SCORE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1950-02-27
- Field: score
- Source value: `48-53`
- Canonical value: `48-54`
- Evidence: utah-state 1950-02-27: 48-54
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 68. DISCREPANCY-CSU-S1-00576-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1950-02-27
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: utah-state 1950-02-27: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU supplies explicit at Utah State; Utah State accepted reciprocal retains UNKNOWN, not an opposing affirmative classification.

### 69. DISCREPANCY-CSU-S1-00593-SCORE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1951-01-08
- Field: score
- Source value: `14-23`
- Canonical value: `62-63`
- Evidence: utah-state 1951-01-08: 62-63
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Large 1951-01-08 contradiction: CSU L 14-23 vs Utah State W 63-62, same opponent/date but incompatible scoring. Do not repair by plausibility or assume quarter/half score transcription without evidence.

### 70. DISCREPANCY-CSU-S1-00593-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1951-01-08
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: utah-state 1951-01-08: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU supplies explicit at Utah State; Utah State accepted reciprocal retains UNKNOWN, not an opposing affirmative classification.

### 71. DISCREPANCY-CSU-S1-00615-GAME_DATE

- Category: discrepancy
- Matchup: colorado-state vs indiana
- Dates: source 1951-12-14; canonical 1951-12-15
- Field: game_date
- Source value: `1951-12-14`
- Canonical value: `1951-12-15`
- Evidence: indiana 1951-12-15: 1951-12-15
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Same 80-48 game but CSU claims Friday Dec 14 at Wyoming Tournament in Laramie while Indiana claims Saturday Dec 15 at Colorado A&M in Fort Collins. Date and H/A/N/location contested in linked site review; do not fix one in isolation.

### 72. DISCREPANCY-CSU-S1-00615-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs indiana
- Dates: source 1951-12-14; canonical 1951-12-15
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: indiana 1951-12-15: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State institutional guide/schedule claim neutral Wyoming Tournament at Laramie Dec 14, whereas Indiana official ledger claims AWAY at Colorado A&M in Fort Collins Dec 15.

### 73. DISCREPANCY-CSU-S1-00633-SCORE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1952-02-14
- Field: score
- Source value: `62-85`
- Canonical value: `69-85`
- Evidence: utah-state 1952-02-14: 69-85
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 74. DISCREPANCY-CSU-S1-00633-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1952-02-14
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: utah-state 1952-02-14: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU supplies explicit at Utah State; Utah State accepted reciprocal retains UNKNOWN, not an opposing affirmative classification.

### 75. DISCREPANCY-CSU-S1-00667-SCORE

- Category: discrepancy
- Matchup: colorado vs colorado-state
- Date: 1953-12-07
- Field: score
- Source value: `42-54`
- Canonical value: `44-54`
- Evidence: colorado 1953-12-07: 44-54
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado reciprocal W/L is consistent with CSU win, but the losing Colorado total is 42 in CSU and 44 in Colorado; unresolved.

### 76. DISCREPANCY-CSU-S1-00670-SCORE

- Category: discrepancy
- Matchup: colorado-state vs iowa
- Date: 1953-12-15
- Field: score
- Source value: `55-70`
- Canonical value: `55-72`
- Evidence: iowa 1953-12-15: 55-72
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 77. DISCREPANCY-CSU-S1-00702-SCORE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1955-01-06
- Field: score
- Source value: `65-85`
- Canonical value: `65-75`
- Evidence: utah-state 1955-01-06: 65-75
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 78. DISCREPANCY-CSU-S1-00702-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1955-01-06
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: utah-state 1955-01-06: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU supplies explicit at Utah State; Utah State accepted reciprocal retains UNKNOWN, not an opposing affirmative classification.

### 79. DISCREPANCY-CSU-S1-00883-GAME_DATE

- Category: discrepancy
- Matchup: byu vs colorado-state
- Dates: source 1962-02-16; canonical 1962-02-15
- Field: game_date
- Source value: `1962-02-16`
- Canonical value: `1962-02-15`
- Evidence: byu 1962-02-15: 1962-02-15
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU media guide, 1961-62 official season schedule and CSU BYU opponent-history page identify Friday Feb 16 (then CSU hosts Utah State Feb 17). BYU record-book source says Feb 15. Prefer CSU date provisionally without touching BYU source.

### 80. DISCREPANCY-CSU-S1-00899-GAME_DATE

- Category: discrepancy
- Matchup: colorado-state vs ucla
- Dates: source 1962-12-28; canonical 1962-12-29
- Field: game_date
- Source value: `1962-12-28`
- Canonical value: `1962-12-29`
- Evidence: ucla 1962-12-29: 1962-12-29
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU official 1962-63 schedule and opponent-history page identify Dec 28, also supported by Sports-Reference UCLA game ledger. The canonical UCLA-source Dec 29 is contradicted; an additional secondary UCLA listing also reports Dec 29. Prefer Dec 28 with residual reciprocal challenge visible.

### 81. DISCREPANCY-CSU-S1-01048-SCORE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 1969-02-17
- Field: score
- Source value: `70-60`
- Canonical value: `90-60`
- Evidence: utah-state 1969-02-17: 90-60
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Same Feb 17 1969 fixture: CSU W 70-60 vs Utah State L 60-90. Winning score differs by 20; do not normalize as a presumed typo.

### 82. DISCREPANCY-CSU-S1-01274-SCORE

- Category: discrepancy
- Matchup: arizona-state vs colorado-state
- Date: 1978-01-28
- Field: score
- Source value: `89-67`
- Canonical value: `87-67`
- Evidence: arizona-state 1978-01-28: 87-67
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Colorado State frozen results row and the accepted reciprocal institutional game row preserve incompatible exact same-game scores; both claims remain distinguishable. No independently decisive same-game box score/tiebreaker established in the bounded evidence pass.

### 83. DISCREPANCY-CSU-S1-01567-GAME_DATE

- Category: discrepancy
- Matchup: colorado-state vs utah
- Dates: source 1988-03-10; canonical 1988-03-09
- Field: game_date
- Source value: `1988-03-10`
- Canonical value: `1988-03-09`
- Evidence: utah 1988-03-09: 1988-03-09
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: CSU official 1987-88 schedule lists quarterfinal Utah W 78-68 on Thu Mar 10, semifinal Wyoming on Fri Mar 11, and CSU opponent-history page also records Mar 10. Strong tournament-sequence corroboration favors CSU over Utah canonical March 9.

### 84. DISCREPANCY-CSU-S1-01615-SCORE

- Category: discrepancy
- Matchup: baylor vs colorado-state
- Date: 1989-12-20
- Field: score
- Source value: `55-74`
- Canonical value: `55-64`
- Evidence: baylor 1989-12-20: 55-64
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: CSU W 74-55 vs Baylor L 55-64; same date, same winner, Baylor opponent score conflict 74 vs 64.

### 85. DISCREPANCY-CSU-S1-01937-SITE_TYPE

- Category: discrepancy
- Matchup: central-connecticut vs colorado-state
- Date: 2000-12-01
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: central-connecticut 2000-12-01: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: CSU raw at Central Connecticut and current official opponent-history list AWAY Hartford; CCSU accepted raw vs Colorado State and Hartford Civic Center explicitly NEUTRAL. Phoenix Classic event and Hartford venue do not themselves determine H/A/N.

### 86. IDENTITY-CSU-S1-02199

- Category: identity
- Matchup: colorado-state vs utah
- Dates: source 2009-01-18; canonical 2009-01-17;2009-02-18
- Field: game_identity
- Source value: `date=2009-01-18; score=79-89`
- Canonical value: `CBBG-0106266;CBBG-0106273`
- Evidence: CBBG-0106266 2008-2009 2009-01-17 66-82 sources=utah; CBBG-0106273 2008-2009 2009-02-18 79-89 sources=utah
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0106273`
- Basis: Exact reciprocal score and home/away. Distinct January 17 road game is present in BOTH sources at CSU 66-82 / Utah 82-66. CSU Jan-18 row appears between its Feb-14 and Feb-21 entries, independently indicating a likely January/February typo.

### 87. CONDITIONAL-DISCREPANCY-CSU-S1-02199-CBBG-0106266-GAME_DATE

- Category: conditional_discrepancy
- Matchup: colorado-state vs utah
- Dates: source 2009-01-18; canonical 2009-01-17
- Field: game_date
- Source value: `2009-01-18`
- Canonical value: `2009-01-17`
- Evidence: utah 2009-01-17: 2009-01-17
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0106273
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106266`

### 88. CONDITIONAL-DISCREPANCY-CSU-S1-02199-CBBG-0106266-SCORE

- Category: conditional_discrepancy
- Matchup: colorado-state vs utah
- Dates: source 2009-01-18; canonical 2009-01-17
- Field: score
- Source value: `79-89`
- Canonical value: `66-82`
- Evidence: utah 2009-01-17: 66-82
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0106273
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106266`

### 89. CONDITIONAL-DISCREPANCY-CSU-S1-02199-CBBG-0106266-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: colorado-state vs utah
- Dates: source 2009-01-18; canonical 2009-01-17
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: utah 2009-01-17: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0106273
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106266`

### 90. CONDITIONAL-DISCREPANCY-CSU-S1-02199-CBBG-0106273-GAME_DATE

- Category: discrepancy
- Matchup: colorado-state vs utah
- Dates: source 2009-01-18; canonical 2009-02-18
- Field: game_date
- Source value: `2009-01-18`
- Canonical value: `2009-02-18`
- Evidence: utah 2009-02-18: 2009-02-18
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Correct CSU structured game_date from erroneous January 18 to February 18. Independent Utah official opponent history, CSU official schedule, CSU opponent history, and the contemporary 2009-02-18 CSU recap agree; preserve literal raw_text. The Jan 17 Utah game is already a separate canonical fixture.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0106273`

### 91. DISCREPANCY-CSU-S1-02207-SCORE

- Category: discrepancy
- Matchup: colorado-state vs oregon
- Date: 2009-11-15
- Field: score
- Source value: `55-68`
- Canonical value: `53-68`
- Evidence: oregon 2009-11-15: 53-68
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Correction supported by CSU institutional 2017 series history (Oregon 68-55), Oregon contemporaneous 2009-10 game-by-game statistical report (halves 36+32 vs 27+28), contemporary published game recap, and CSU historical ledger. Oregon currently published source and official digital schedule instead say 68-53, a downstream reciprocal-source inconsistency not within CSU mutation authority.

### 92. DISCREPANCY-CSU-S1-02608-SCORE

- Category: discrepancy
- Matchup: colorado-state vs utah-state
- Date: 2022-01-12
- Field: score
- Source value: `79-49`
- Canonical value: `77-72`
- Evidence: utah-state 2022-01-12: 77-72
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Both institutions contemporary Jan 12 2022 recap and complete box score prove CSU 77-72 Utah State; CSU historical frozen results row W 79-49 is erroneous. The canonical score is already 77-72; propose a CSU team_score/opponent_score source patch only at owner Gate 1.

### 93. DISCREPANCY-CSU-S1-SUP-008-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs washington
- Date: 2023-12-02
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington 2023-12-02: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Colorado State official season schedule explicitly NEUTRAL; contemporary event/box score identifies exact arena and out-of-state city; Washington contemporary material corroborates a neutral-tournament event, whereas its published long-run extracted row incorrectly assigns H/Seattle/Hec Edmundson.

### 94. DISCREPANCY-CSU-S1-SUP-042-SITE_TYPE

- Category: discrepancy
- Matchup: colorado-state vs washington
- Date: 2024-11-28
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington 2024-11-28: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Colorado State official season schedule explicitly NEUTRAL; contemporary event/box score identifies exact arena and out-of-state city; Washington contemporary material corroborates a neutral-tournament event, whereas its published long-run extracted row incorrectly assigns H/Seattle/Hec Edmundson.

### 95. ACCOMPLISHMENTS-COLORADO-STATE

- Category: accomplishments
- Matchup: colorado-state
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"ELITE_EIGHT","best_finish_year":"1969","conference_regular_season_championships":"4","conference_tournament_championships":"2","final_four_appearances":"0","national_championships":"0","ncaa_tournament_appearances":"13"}`
- Canonical value: `{"best_finish_key":"ELITE_EIGHT","best_finish_year":1969,"final_four_appearances":0,"national_championships":0,"ncaa_tournament_appearances":13}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `VERIFY_REFERENCE_VALUES`
- Basis: Accept the seven numeric/category accomplishment values as authoritatively supported, without value edits, with a later verification_basis citation and strict canonical crosscheck before any change of reference metadata. The plan-level canonical values match the five derivable NCAA fields. Do not authorize publication in this unit. Evidence: [{'fields': ['conference_regular_season_championships', 'conference_tournament_championships'], 'evidence': 'Colorado State Athletics conference championship index, updated March 26 2026, lists 1953-54 Skyline, 1960-61 Skyline, 1988-89 WAC regular season, 1989-90 WAC regular season, 2002-03 MW Tournament, 2024-25 MW Tournament. Therefore 4 regular-season + 2 tournament titles.', 'url': 'https://csurams.com/sports/2021/2/25/conference-championships', 'rating': 'official primary source', 'confidence': 'HIGH'}, {'fields': ['ncaa_tournament_appearances', 'best_finish_key', 'best_finish_year', 'final_four_appearances', 'national_championships'], 'evidence': 'Colorado State official 2025-26 game notes, published Mar 3 2026, p.7 / PDF p.6, identify the 2025 NCAA Tournament as the 13th appearance, 1969 as the only historic Sweet 16 and deepest finish in Elite Eight; by definition no Final Four or NCAA national championship.', 'url': 'https://csurams.com/documents/download/2026/3/3/GM30-New_Mexico.pdf', 'rating': 'official primary source', 'confidence': 'HIGH'}, {'fields': ['ncaa_tournament_appearances', 'best_finish_key', 'best_finish_year'], 'evidence': 'Mountain West 2025-26 record book,

### 96. PUBLICATION-COLORADO-STATE

- Category: publication
- Matchup: colorado-state
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 2,765 in-scope source rows; 8 identity reviews; 57 definite and 29 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `ENABLE_PUBLIC_PAGE`
- Basis: ['School is an accepted serialized onboarding/Implementation target with 2,765 in-scope source rows and an immutable Research Freeze and Integration Freeze.', 'All 96 Stage 2 census decisions have working evidence reviews, including 8 identity, 26 site/H-A-N, 24 date, 34 score, 2 winner/result, 1 accomplishment, 1 publication.', 'The Stage 2 census is CAPABILITY_CENSUS_READY with zero census blockers/warnings. This is not a rehearsal, pre-seal, owner Gate 1, page publication, or production verification PASS.', 'The exact census plan recommends ENABLE_PUBLIC_PAGE, but states it occurs only after approved decisions and automated gates pass.', 'Protected-main program reference currently has public_page_enabled=No. The actual reference must remain No throughout this review.', "School's main reference row has blank history scope metadata; separate program-top-level-scope.csv establishes Colorado State INCEPTION+. Reconcile program scope with immutable accepted Research Freeze through authorized Implementation before publication.", 'Program accomplishment reference row remains OWNER_BASELINE_UNVERIFIED and NOT_CHECKED. Prior evidence review supports historical values, but permanent canonical cross-check and verified reference metadata remain unperformed.', 'Historical date, score, site and winner disagreements remain explicitly documented; eligible unresolved conflicts require informed Owner Gate 1 acceptance and defensible canonical publication state rather than forced research closure.']
