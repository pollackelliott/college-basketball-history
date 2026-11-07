# fordham onboarding review

Generated: 2026-11-07T20:01:17.369427+00:00
Input fingerprint: `6fc6dfb0163e353022644fedaf5d613e357ca549fae34f48a0bbc33fe317cc77`
Approved plan: `a81ffb4936f4b1a1a398abf8a0c852aa85188700b410e2cbbe939c9e1fd4c90a`

## Preflight summary

- Source rows: 2,917
- In-scope rows: 2,917
- Pre-cutoff researched rows: 0
- Existing matches: 954
- New canonical games: 1,941
- Identity reviews: 22
- Safe enrichment fields: 1,846
- Discrepancies: 104
- Conditional discrepancies: 52
- Canonical-only site reviews: 2
- Affected existing public programs: arizona, arizona-state, arkansas, auburn, boston-college, butler, byu, california, central-connecticut, cincinnati, clemson, colorado-state, davidson, dayton, depaul, duquesne, fairleigh-dickinson, florida, florida-state, georgetown, georgia, georgia-tech, houston, kansas, la-salle, long-island-university, louisville, loyola-chicago, lsu, marquette, maryland, miami, michigan, missouri, nc-state, nebraska, new-haven, north-carolina, northwestern, notre-dame, oklahoma, ole-miss, penn-state, pittsburgh, providence, purdue, rhode-island, rutgers, saint-louis, san-diego-state, seton-hall, south-carolina, st-bonaventure, st-john-s, stanford, stonehill, syracuse, tcu, tennessee, texas, texas-a-m, texas-state, ucf, ucla, uconn, usc, utah, utah-state, vanderbilt, villanova, virginia, virginia-tech, wagner, west-virginia, wisconsin, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. IDENTITY-FORDHAM-1907-08-011

- Category: identity
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1908-01-18
- Field: game_identity
- Source value: `date=[unknown]; score=31-29`
- Canonical value: `CBBG-0163754`
- Evidence: CBBG-0163754 1907-1908 1908-01-18 14-25 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `FORCE_NEW`
- Basis: Fordham has two 1907-08 Georgetown rows: the 14-25 loss already corresponds to CBBG-0163754, while this row is a distinct 31-29 win. One real game equals one canonical game, so this row must remain a new game rather than duplicate the other source row onto the reciprocal canonical game.

### 2. CONDITIONAL-DISCREPANCY-FORDHAM-1907-08-011-CBBG-0163754-SCORE

- Category: conditional_discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1908-01-18
- Field: score
- Source value: `31-29`
- Canonical value: `14-25`
- Evidence: georgetown 1908-01-18: 14-25
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163754`

### 3. CONDITIONAL-DISCREPANCY-FORDHAM-1907-08-011-CBBG-0163754-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1908-01-18
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgetown 1908-01-18: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163754`

### 4. CONDITIONAL-DISCREPANCY-FORDHAM-1907-08-011-CBBG-0163754-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1908-01-18
- Field: result_winner_team_key
- Source value: `fordham`
- Canonical value: `georgetown`
- Evidence: georgetown 1908-01-18: georgetown
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163754`

### 5. IDENTITY-FORDHAM-1908-09-006

- Category: identity
- Matchup: fordham vs st-john-s
- Dates: source [unknown]; canonical 1909-01-30
- Field: game_identity
- Source value: `date=[unknown]; score=22-13`
- Canonical value: `CBBG-0158347`
- Evidence: CBBG-0158347 1908-1909 1909-01-30 21-13 sources=st-john-s
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0158347`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 6. CONDITIONAL-DISCREPANCY-FORDHAM-1908-09-006-CBBG-0158347-SCORE

- Category: discrepancy
- Matchup: fordham vs st-john-s
- Dates: source [unknown]; canonical 1909-01-30
- Field: score
- Source value: `22-13`
- Canonical value: `21-13`
- Evidence: st-john-s 1909-01-30: 21-13
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0158347`

### 7. IDENTITY-FORDHAM-1908-09-014

- Category: identity
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1909-02-22
- Field: game_identity
- Source value: `date=[unknown]; score=35-19`
- Canonical value: `CBBG-0163765`
- Evidence: CBBG-0163765 1908-1909 1909-02-22 19-27 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `FORCE_NEW`
- Basis: Fordham has a separate 19-27 Georgetown loss that corresponds to CBBG-0163765; this 35-19 win is a distinct game and must remain FORCE_NEW.

### 8. CONDITIONAL-DISCREPANCY-FORDHAM-1908-09-014-CBBG-0163765-SCORE

- Category: conditional_discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1909-02-22
- Field: score
- Source value: `35-19`
- Canonical value: `19-27`
- Evidence: georgetown 1909-02-22: 19-27
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163765`

### 9. CONDITIONAL-DISCREPANCY-FORDHAM-1908-09-014-CBBG-0163765-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1909-02-22
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgetown 1909-02-22: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163765`

### 10. CONDITIONAL-DISCREPANCY-FORDHAM-1908-09-014-CBBG-0163765-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1909-02-22
- Field: result_winner_team_key
- Source value: `fordham`
- Canonical value: `georgetown`
- Evidence: georgetown 1909-02-22: georgetown
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163765`

### 11. IDENTITY-FORDHAM-1911-12-008

- Category: identity
- Matchup: fordham vs st-john-s
- Dates: source [unknown]; canonical 1912-01-11
- Field: game_identity
- Source value: `date=[unknown]; score=19-42`
- Canonical value: `CBBG-0158391`
- Evidence: CBBG-0158391 1911-1912 1912-01-11 19-48 sources=st-john-s
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0158391`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 12. CONDITIONAL-DISCREPANCY-FORDHAM-1911-12-008-CBBG-0158391-SCORE

- Category: discrepancy
- Matchup: fordham vs st-john-s
- Dates: source [unknown]; canonical 1912-01-11
- Field: score
- Source value: `19-42`
- Canonical value: `19-48`
- Evidence: st-john-s 1912-01-11: 19-48
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0158391`

### 13. IDENTITY-FORDHAM-1912-13-006

- Category: identity
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1914-02-06
- Field: game_identity
- Source value: `date=[unknown]; score=15-25`
- Canonical value: `CBBG-0163822`
- Evidence: CBBG-0163822 1913-1914 1914-02-06 15-25 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0163822`
- Basis: The permanent preflight proved a unique adjacent-season exact-score Georgetown candidate, CBBG-0163822, and the exact source correction season_label=1913-1914 / game_date=1914-02-06. Match that one real game and apply only the preflight-proven source date/season patch.

### 14. CONDITIONAL-DISCREPANCY-FORDHAM-1912-13-006-CBBG-0163822-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1914-02-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: georgetown 1914-02-06: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Fordham's frozen target row intentionally remains UNKNOWN after completed H/A/N research. Preserve the existing concrete reciprocal/canonical site classification without manufacturing target-school certainty.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163822`

### 15. IDENTITY-FORDHAM-1912-13-008

- Category: identity
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-01-08
- Field: game_identity
- Source value: `date=[unknown]; score=18-23`
- Canonical value: `CBBG-0162161`
- Evidence: CBBG-0162161 1912-1913 1913-01-08 18-24 sources=seton-hall
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0162161`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 16. CONDITIONAL-DISCREPANCY-FORDHAM-1912-13-008-CBBG-0162161-SCORE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-01-08
- Field: score
- Source value: `18-23`
- Canonical value: `18-24`
- Evidence: seton-hall 1913-01-08: 18-24
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162161`

### 17. CONDITIONAL-DISCREPANCY-FORDHAM-1912-13-008-CBBG-0162161-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-01-08
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: seton-hall 1913-01-08: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Fordham's frozen target row intentionally remains UNKNOWN after completed H/A/N research. Preserve the existing concrete reciprocal/canonical site classification without manufacturing target-school certainty.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162161`

### 18. DISCREPANCY-FORDHAM-1913-14-001-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Dates: source 1913-12-20; canonical 1913-12-19
- Field: game_date
- Source value: `1913-12-20`
- Canonical value: `1913-12-19`
- Evidence: georgetown 1913-12-19: 1913-12-19
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 19. IDENTITY-FORDHAM-1913-14-012

- Category: identity
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-12-10;1914-01-07
- Field: game_identity
- Source value: `date=[unknown]; score=37-17`
- Canonical value: `CBBG-0162170;CBBG-0162174`
- Evidence: CBBG-0162170 1913-1914 1913-12-10 14-23 sources=seton-hall; CBBG-0162174 1913-1914 1914-01-07 35-17 sources=seton-hall
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0162174`
- Basis: The same-season Fordham source has a separate 14-23 Seton Hall loss corresponding to CBBG-0162170; this 37-17 win aligns with CBBG-0162174 (35-17 reciprocal score) and is the remaining reciprocal game.

### 20. CONDITIONAL-DISCREPANCY-FORDHAM-1913-14-012-CBBG-0162170-SCORE

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-12-10
- Field: score
- Source value: `37-17`
- Canonical value: `14-23`
- Evidence: seton-hall 1913-12-10: 14-23
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0162174
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162170`

### 21. CONDITIONAL-DISCREPANCY-FORDHAM-1913-14-012-CBBG-0162170-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-12-10
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: seton-hall 1913-12-10: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0162174
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162170`

### 22. CONDITIONAL-DISCREPANCY-FORDHAM-1913-14-012-CBBG-0162170-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-12-10
- Field: result_winner_team_key
- Source value: `fordham`
- Canonical value: `seton-hall`
- Evidence: seton-hall 1913-12-10: seton-hall
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0162174
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162170`

### 23. CONDITIONAL-DISCREPANCY-FORDHAM-1913-14-012-CBBG-0162174-SCORE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1914-01-07
- Field: score
- Source value: `37-17`
- Canonical value: `35-17`
- Evidence: seton-hall 1914-01-07: 35-17
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162174`

### 24. CONDITIONAL-DISCREPANCY-FORDHAM-1913-14-012-CBBG-0162174-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1914-01-07
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: seton-hall 1914-01-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Fordham's frozen target row intentionally remains UNKNOWN after completed H/A/N research. Preserve the existing concrete reciprocal/canonical site classification without manufacturing target-school certainty.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162174`

### 25. IDENTITY-FORDHAM-1913-14-018

- Category: identity
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-12-10;1914-01-07
- Field: game_identity
- Source value: `date=[unknown]; score=-`
- Canonical value: `CBBG-0162170;CBBG-0162174`
- Evidence: CBBG-0162170 1913-1914 1913-12-10 14-23 sources=seton-hall; CBBG-0162174 1913-1914 1914-01-07 35-17 sources=seton-hall
- Recommended: `REVIEW_REQUIRED`
- Decision: `FORCE_NEW`
- Basis: The two existing Seton Hall canonical candidates correspond to Fordham's other two same-season source rows; this third Fordham win has no unused reciprocal canonical identity and remains FORCE_NEW.

### 26. CONDITIONAL-DISCREPANCY-FORDHAM-1913-14-018-CBBG-0162170-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-12-10
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: seton-hall 1913-12-10: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162170`

### 27. CONDITIONAL-DISCREPANCY-FORDHAM-1913-14-018-CBBG-0162170-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-12-10
- Field: result_winner_team_key
- Source value: `fordham`
- Canonical value: `seton-hall`
- Evidence: seton-hall 1913-12-10: seton-hall
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162170`

### 28. CONDITIONAL-DISCREPANCY-FORDHAM-1913-14-018-CBBG-0162174-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1914-01-07
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: seton-hall 1914-01-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162174`

### 29. IDENTITY-FORDHAM-1914-15-016

- Category: identity
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1914-12-18;1915-02-05
- Field: game_identity
- Source value: `date=[unknown]; score=16-21`
- Canonical value: `CBBG-0163828;CBBG-0163835`
- Evidence: CBBG-0163828 1914-1915 1914-12-18 31-28 sources=georgetown; CBBG-0163835 1914-1915 1915-02-05 16-31 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0163835`
- Basis: Fordham's separate 31-28 Georgetown win corresponds to CBBG-0163828; this 16-21 loss is therefore the remaining game represented by CBBG-0163835 despite the reciprocal score disagreement.

### 30. CONDITIONAL-DISCREPANCY-FORDHAM-1914-15-016-CBBG-0163828-SCORE

- Category: conditional_discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1914-12-18
- Field: score
- Source value: `16-21`
- Canonical value: `31-28`
- Evidence: georgetown 1914-12-18: 31-28
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0163835
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163828`

### 31. CONDITIONAL-DISCREPANCY-FORDHAM-1914-15-016-CBBG-0163828-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1914-12-18
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: georgetown 1914-12-18: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0163835
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163828`

### 32. CONDITIONAL-DISCREPANCY-FORDHAM-1914-15-016-CBBG-0163828-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1914-12-18
- Field: result_winner_team_key
- Source value: `georgetown`
- Canonical value: `fordham`
- Evidence: georgetown 1914-12-18: fordham
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0163835
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163828`

### 33. CONDITIONAL-DISCREPANCY-FORDHAM-1914-15-016-CBBG-0163835-SCORE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Dates: source [unknown]; canonical 1915-02-05
- Field: score
- Source value: `16-21`
- Canonical value: `16-31`
- Evidence: georgetown 1915-02-05: 16-31
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163835`

### 34. IDENTITY-FORDHAM-1914-15-019

- Category: identity
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1914-12-02
- Field: game_identity
- Source value: `date=[unknown]; score=27-21`
- Canonical value: `CBBG-0162185`
- Evidence: CBBG-0162185 1914-1915 1914-12-02 14-39 sources=seton-hall
- Recommended: `REVIEW_REQUIRED`
- Decision: `FORCE_NEW`
- Basis: Fordham's separate 14-39 Seton Hall loss corresponds to CBBG-0162185; this 27-21 win is a distinct game and remains FORCE_NEW.

### 35. CONDITIONAL-DISCREPANCY-FORDHAM-1914-15-019-CBBG-0162185-SCORE

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1914-12-02
- Field: score
- Source value: `27-21`
- Canonical value: `14-39`
- Evidence: seton-hall 1914-12-02: 14-39
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162185`

### 36. CONDITIONAL-DISCREPANCY-FORDHAM-1914-15-019-CBBG-0162185-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1914-12-02
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: seton-hall 1914-12-02: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162185`

### 37. CONDITIONAL-DISCREPANCY-FORDHAM-1914-15-019-CBBG-0162185-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1914-12-02
- Field: result_winner_team_key
- Source value: `fordham`
- Canonical value: `seton-hall`
- Evidence: seton-hall 1914-12-02: seton-hall
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was FORCE_NEW
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162185`

### 38. DISCREPANCY-FORDHAM-1919-20-007-SCORE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Date: 1920-01-14
- Field: score
- Source value: `27-39`
- Canonical value: `27-37`
- Evidence: seton-hall 1920-01-14: 27-37
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 39. IDENTITY-FORDHAM-1919-20-014

- Category: identity
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1920-01-14;1920-03-06;1921-02-10
- Field: game_identity
- Source value: `date=[unknown]; score=25-36`
- Canonical value: `CBBG-0162247;CBBG-0162252;CBBG-0162266`
- Evidence: CBBG-0162247 1919-1920 1920-01-14 27-37 sources=seton-hall; CBBG-0162252 1919-1920 1920-03-06 51-27 sources=seton-hall; CBBG-0162266 1920-1921 1921-02-10 25-36 sources=seton-hall
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0162266`
- Basis: The permanent preflight proved CBBG-0162266 as the unique adjacent-season exact-score 25-36 Seton Hall candidate; Fordham's dated Jan. 14 and Mar. 6 rows correspond to the other two canonical meetings. Apply only the exact preflight-proven season/date patch to 1920-1921 / 1921-02-10.

### 40. CONDITIONAL-DISCREPANCY-FORDHAM-1919-20-014-CBBG-0162247-SCORE

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1920-01-14
- Field: score
- Source value: `25-36`
- Canonical value: `27-37`
- Evidence: seton-hall 1920-01-14: 27-37
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0162266
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162247`

### 41. CONDITIONAL-DISCREPANCY-FORDHAM-1919-20-014-CBBG-0162247-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1920-01-14
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: seton-hall 1920-01-14: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0162266
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162247`

### 42. CONDITIONAL-DISCREPANCY-FORDHAM-1919-20-014-CBBG-0162252-SCORE

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1920-03-06
- Field: score
- Source value: `25-36`
- Canonical value: `51-27`
- Evidence: seton-hall 1920-03-06: 51-27
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0162266
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162252`

### 43. CONDITIONAL-DISCREPANCY-FORDHAM-1919-20-014-CBBG-0162252-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1920-03-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: seton-hall 1920-03-06: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0162266
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162252`

### 44. CONDITIONAL-DISCREPANCY-FORDHAM-1919-20-014-CBBG-0162252-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1920-03-06
- Field: result_winner_team_key
- Source value: `seton-hall`
- Canonical value: `fordham`
- Evidence: seton-hall 1920-03-06: fordham
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0162266
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162252`

### 45. CONDITIONAL-DISCREPANCY-FORDHAM-1919-20-014-CBBG-0162266-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1921-02-10
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `NEUTRAL`
- Evidence: seton-hall 1921-02-10: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Fordham's frozen target row intentionally remains UNKNOWN after completed H/A/N research. Preserve the existing concrete reciprocal/canonical site classification without manufacturing target-school certainty.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0162266`

### 46. DISCREPANCY-FORDHAM-1919-20-016-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Dates: source 1920-02-27; canonical 1920-02-26
- Field: game_date
- Source value: `1920-02-27`
- Canonical value: `1920-02-26`
- Evidence: georgetown 1920-02-26: 1920-02-26
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 47. DISCREPANCY-FORDHAM-1919-20-018-SCORE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Date: 1920-03-06
- Field: score
- Source value: `55-27`
- Canonical value: `51-27`
- Evidence: seton-hall 1920-03-06: 51-27
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 48. DISCREPANCY-FORDHAM-1919-20-018-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Date: 1920-03-06
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: seton-hall 1920-03-06: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Fordham's frozen target row intentionally remains UNKNOWN after completed H/A/N research. Preserve the existing concrete reciprocal/canonical site classification without manufacturing target-school certainty.

### 49. DISCREPANCY-FORDHAM-1920-21-016-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs villanova
- Date: 1921-02-05
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: villanova 1921-02-05: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 50. DISCREPANCY-FORDHAM-1921-22-014-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Date: 1922-02-08
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: seton-hall 1922-02-08: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 51. IDENTITY-FORDHAM-1925-26-018

- Category: identity
- Matchup: fordham vs georgetown
- Dates: source 1926-02-23; canonical 1926-02-25
- Field: game_identity
- Source value: `date=1926-02-23; score=35-18`
- Canonical value: `CBBG-0163948`
- Evidence: CBBG-0163948 1925-1926 1926-02-25 35-18 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0163948`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 52. CONDITIONAL-DISCREPANCY-FORDHAM-1925-26-018-CBBG-0163948-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Dates: source 1926-02-23; canonical 1926-02-25
- Field: game_date
- Source value: `1926-02-23`
- Canonical value: `1926-02-25`
- Evidence: georgetown 1926-02-25: 1926-02-25
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0163948`

### 53. DISCREPANCY-FORDHAM-1928-29-008-SCORE

- Category: discrepancy
- Matchup: fordham vs syracuse
- Date: 1929-01-11
- Field: score
- Source value: `37-15`
- Canonical value: `35-14`
- Evidence: syracuse 1929-01-11: 35-14
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 54. DISCREPANCY-FORDHAM-1929-30-011-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Dates: source 1930-02-03; canonical 1930-02-02
- Field: game_date
- Source value: `1930-02-03`
- Canonical value: `1930-02-02`
- Evidence: pittsburgh 1930-02-02: 1930-02-02
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 55. DISCREPANCY-FORDHAM-1930-31-008-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Dates: source 1931-01-15; canonical 1931-01-16
- Field: game_date
- Source value: `1931-01-15`
- Canonical value: `1931-01-16`
- Evidence: pittsburgh 1931-01-16: 1931-01-16
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 56. DISCREPANCY-FORDHAM-1930-31-008-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Dates: source 1931-01-15; canonical 1931-01-16
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: pittsburgh 1931-01-16: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 57. DISCREPANCY-FORDHAM-1931-32-010-SCORE

- Category: discrepancy
- Matchup: fordham vs rutgers
- Date: 1932-02-03
- Field: score
- Source value: `23-26`
- Canonical value: `36-45`
- Evidence: rutgers 1932-02-03: 36-45
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 58. DISCREPANCY-FORDHAM-1934-35-007-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Dates: source 1935-01-16; canonical 1935-01-17
- Field: game_date
- Source value: `1935-01-16`
- Canonical value: `1935-01-17`
- Evidence: pittsburgh 1935-01-17: 1935-01-17
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 59. DISCREPANCY-FORDHAM-1934-35-007-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Dates: source 1935-01-16; canonical 1935-01-17
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: pittsburgh 1935-01-17: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 60. DISCREPANCY-FORDHAM-1934-35-008-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Date: 1935-01-19
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: seton-hall 1935-01-19: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 61. IDENTITY-FORDHAM-1937-38-005

- Category: identity
- Matchup: fordham vs pittsburgh
- Dates: source 1937-12-17; canonical 1937-12-20
- Field: game_identity
- Source value: `date=1937-12-17; score=23-35`
- Canonical value: `CBBG-0137765`
- Evidence: CBBG-0137765 1937-1938 1937-12-20 23-35 sources=pittsburgh
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0137765`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 62. CONDITIONAL-DISCREPANCY-FORDHAM-1937-38-005-CBBG-0137765-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Dates: source 1937-12-17; canonical 1937-12-20
- Field: game_date
- Source value: `1937-12-17`
- Canonical value: `1937-12-20`
- Evidence: pittsburgh 1937-12-20: 1937-12-20
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0137765`

### 63. CONDITIONAL-DISCREPANCY-FORDHAM-1937-38-005-CBBG-0137765-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Dates: source 1937-12-17; canonical 1937-12-20
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: pittsburgh 1937-12-20: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0137765`

### 64. DISCREPANCY-FORDHAM-1937-38-012-SCORE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Date: 1938-02-01
- Field: score
- Source value: `38-36`
- Canonical value: `38-26`
- Evidence: georgetown 1938-02-01: 38-26
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 65. DISCREPANCY-FORDHAM-1938-39-011-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Dates: source 1939-01-30; canonical 1939-01-31
- Field: game_date
- Source value: `1939-01-30`
- Canonical value: `1939-01-31`
- Evidence: georgetown 1939-01-31: 1939-01-31
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 66. DISCREPANCY-FORDHAM-1939-40-009-SCORE

- Category: discrepancy
- Matchup: fordham vs syracuse
- Date: 1940-01-12
- Field: score
- Source value: `43-34`
- Canonical value: `42-34`
- Evidence: syracuse 1940-01-12: 42-34
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 67. DISCREPANCY-FORDHAM-1940-41-019-SCORE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Date: 1941-02-28
- Field: score
- Source value: `53-42`
- Canonical value: `52-42`
- Evidence: georgetown 1941-02-28: 52-42
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 68. DISCREPANCY-FORDHAM-1941-42-009-SCORE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Date: 1942-01-08
- Field: score
- Source value: `53-31`
- Canonical value: `33-31`
- Evidence: georgetown 1942-01-08: 33-31
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 69. DISCREPANCY-FORDHAM-1941-42-009-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Date: 1942-01-08
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `UNKNOWN`
- Evidence: georgetown 1942-01-08: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 70. DISCREPANCY-FORDHAM-1942-43-015-SCORE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Date: 1943-02-11
- Field: score
- Source value: `49-52`
- Canonical value: `39-52`
- Evidence: georgetown 1943-02-11: 39-52
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 71. DISCREPANCY-FORDHAM-1942-43-021-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs st-john-s
- Date: 1943-03-27
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-john-s 1943-03-27: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: The frozen Fordham row is RESEARCHED_UNRESOLVED and explicitly records the conflict: Fordham evidence treats the MSG NIT game as neutral while the accepted St. John's reciprocal source treats it as source-program home. Preserve that documented disagreement rather than manufacture H/A/N authority.

### 72. DISCREPANCY-FORDHAM-1947-48-009-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs villanova
- Date: 1948-01-16
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: villanova 1948-01-16: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 73. IDENTITY-FORDHAM-1949-50-024

- Category: identity
- Matchup: fordham vs georgetown
- Dates: source 1950-02-23; canonical 1950-02-09
- Field: game_identity
- Source value: `date=1950-02-23; score=64-63`
- Canonical value: `CBBG-0164265`
- Evidence: CBBG-0164265 1949-1950 1950-02-09 64-63 sources=georgetown
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0164265`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 74. CONDITIONAL-DISCREPANCY-FORDHAM-1949-50-024-CBBG-0164265-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Dates: source 1950-02-23; canonical 1950-02-09
- Field: game_date
- Source value: `1950-02-23`
- Canonical value: `1950-02-09`
- Evidence: georgetown 1950-02-09: 1950-02-09
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0164265`

### 75. DISCREPANCY-FORDHAM-1951-52-017-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Dates: source 1952-02-02; canonical 1952-02-03
- Field: game_date
- Source value: `1952-02-02`
- Canonical value: `1952-02-03`
- Evidence: georgetown 1952-02-03: 1952-02-03
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 76. DISCREPANCY-FORDHAM-1951-52-018-SCORE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Date: 1952-02-06
- Field: score
- Source value: `40-61`
- Canonical value: `41-60`
- Evidence: seton-hall 1952-02-06: 41-60
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 77. IDENTITY-FORDHAM-1951-52-024

- Category: identity
- Matchup: fordham vs rutgers
- Dates: source 1952-02-27; canonical 1952-03-01
- Field: game_identity
- Source value: `date=1952-02-27; score=70-59`
- Canonical value: `CBBG-0076317`
- Evidence: CBBG-0076317 1951-1952 1952-03-01 70-59 sources=rutgers
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0076317`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 78. CONDITIONAL-DISCREPANCY-FORDHAM-1951-52-024-CBBG-0076317-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs rutgers
- Dates: source 1952-02-27; canonical 1952-03-01
- Field: game_date
- Source value: `1952-02-27`
- Canonical value: `1952-03-01`
- Evidence: rutgers 1952-03-01: 1952-03-01
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0076317`

### 79. DISCREPANCY-FORDHAM-1952-53-009-SCORE

- Category: discrepancy
- Matchup: dayton vs fordham
- Date: 1953-01-03
- Field: score
- Source value: `57-64`
- Canonical value: `59-64`
- Evidence: dayton 1953-01-03: 59-64
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 80. DISCREPANCY-FORDHAM-1952-53-018-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs villanova
- Date: 1953-02-07
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: villanova 1953-02-07: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 81. IDENTITY-FORDHAM-1952-53-023

- Category: identity
- Matchup: fordham vs nc-state
- Dates: source 1953-02-24; canonical 1953-02-28
- Field: game_identity
- Source value: `date=1953-02-24; score=70-73`
- Canonical value: `CBBG-0134677`
- Evidence: CBBG-0134677 1952-1953 1953-02-28 70-73 sources=nc-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0134677`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 82. CONDITIONAL-DISCREPANCY-FORDHAM-1952-53-023-CBBG-0134677-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs nc-state
- Dates: source 1953-02-24; canonical 1953-02-28
- Field: game_date
- Source value: `1953-02-24`
- Canonical value: `1953-02-28`
- Evidence: nc-state 1953-02-28: 1953-02-28
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0134677`

### 83. DISCREPANCY-FORDHAM-1953-54-014-SCORE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Date: 1954-01-30
- Field: score
- Source value: `70-53`
- Canonical value: `67-53`
- Evidence: seton-hall 1954-01-30: 67-53
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 84. DISCREPANCY-FORDHAM-1954-55-003-SCORE

- Category: discrepancy
- Matchup: duquesne vs fordham
- Date: 1954-12-10
- Field: score
- Source value: `67-46`
- Canonical value: `67-45`
- Evidence: duquesne 1954-12-10: 67-45
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 85. DISCREPANCY-FORDHAM-1954-55-003-SITE_TYPE

- Category: discrepancy
- Matchup: duquesne vs fordham
- Date: 1954-12-10
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: duquesne 1954-12-10: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 86. DISCREPANCY-FORDHAM-1955-56-017-SCORE

- Category: discrepancy
- Matchup: fordham vs la-salle
- Date: 1956-02-07
- Field: score
- Source value: `84-69`
- Canonical value: `84-68`
- Evidence: la-salle 1956-02-07: 84-68
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 87. DISCREPANCY-FORDHAM-1955-56-024-SCORE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Date: 1956-03-03
- Field: score
- Source value: `78-76`
- Canonical value: `78-75`
- Evidence: seton-hall 1956-03-03: 78-75
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 88. DISCREPANCY-FORDHAM-1956-57-005-SCORE

- Category: discrepancy
- Matchup: fordham vs rhode-island
- Date: 1956-12-13
- Field: score
- Source value: `86-71`
- Canonical value: `85-71`
- Evidence: rhode-island 1956-12-13: 85-71
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 89. DISCREPANCY-FORDHAM-1956-57-022-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs st-john-s
- Date: 1957-02-23
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: st-john-s 1957-02-23: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 90. DISCREPANCY-FORDHAM-1956-57-023-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs la-salle
- Date: 1957-02-27
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: la-salle 1957-02-27: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 91. DISCREPANCY-FORDHAM-1958-59-007-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Dates: source 1958-12-29; canonical 1958-12-28
- Field: game_date
- Source value: `1958-12-29`
- Canonical value: `1958-12-28`
- Evidence: pittsburgh 1958-12-28: 1958-12-28
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 92. IDENTITY-FORDHAM-1959-60-008

- Category: identity
- Matchup: fordham vs pittsburgh
- Dates: source 1959-12-22; canonical 1959-12-26
- Field: game_identity
- Source value: `date=1959-12-22; score=80-68`
- Canonical value: `CBBG-0138038`
- Evidence: CBBG-0138038 1959-1960 1959-12-26 80-68 sources=pittsburgh
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0138038`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 93. CONDITIONAL-DISCREPANCY-FORDHAM-1959-60-008-CBBG-0138038-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Dates: source 1959-12-22; canonical 1959-12-26
- Field: game_date
- Source value: `1959-12-22`
- Canonical value: `1959-12-26`
- Evidence: pittsburgh 1959-12-26: 1959-12-26
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0138038`

### 94. DISCREPANCY-FORDHAM-1959-60-018-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Dates: source 1960-02-06; canonical 1960-02-05
- Field: game_date
- Source value: `1960-02-06`
- Canonical value: `1960-02-05`
- Evidence: georgetown 1960-02-05: 1960-02-05
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 95. DISCREPANCY-FORDHAM-1962-63-003-SCORE

- Category: discrepancy
- Matchup: fordham vs rhode-island
- Date: 1962-12-08
- Field: score
- Source value: `73-74`
- Canonical value: `71-74`
- Evidence: rhode-island 1962-12-08: 71-74
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 96. DISCREPANCY-FORDHAM-1962-63-003-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs rhode-island
- Date: 1962-12-08
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: rhode-island 1962-12-08: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 97. DISCREPANCY-FORDHAM-1962-63-017-SCORE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Date: 1963-02-06
- Field: score
- Source value: `61-89`
- Canonical value: `61-87`
- Evidence: pittsburgh 1963-02-06: 61-87
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 98. DISCREPANCY-FORDHAM-1963-64-013-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs pittsburgh
- Dates: source 1964-02-08; canonical 1964-02-09
- Field: game_date
- Source value: `1964-02-08`
- Canonical value: `1964-02-09`
- Evidence: pittsburgh 1964-02-09: 1964-02-09
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 99. DISCREPANCY-FORDHAM-1966-67-003-SCORE

- Category: discrepancy
- Matchup: fordham vs seton-hall
- Date: 1966-12-10
- Field: score
- Source value: `79-77`
- Canonical value: `81-77`
- Evidence: seton-hall 1966-12-10: 81-77
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 100. DISCREPANCY-FORDHAM-1966-67-010-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs nc-state
- Date: 1967-01-04
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: nc-state 1967-01-04: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 101. DISCREPANCY-FORDHAM-1969-70-007-SCORE

- Category: discrepancy
- Matchup: fordham vs maryland
- Date: 1969-12-20
- Field: score
- Source value: `71-93`
- Canonical value: `71-94`
- Evidence: maryland 1969-12-20: 71-94
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 102. DISCREPANCY-FORDHAM-1970-71-018-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs rhode-island
- Date: 1971-02-11
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: rhode-island 1971-02-11: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 103. DISCREPANCY-FORDHAM-1970-71-022-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs marquette
- Date: 1971-02-25
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1971-02-25: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 104. DISCREPANCY-FORDHAM-1971-72-023-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs saint-louis
- Date: 1972-02-24
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: saint-louis 1972-02-24: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 105. DISCREPANCY-FORDHAM-1972-73-002-SITE_TYPE

- Category: discrepancy
- Matchup: florida vs fordham
- Date: 1972-12-09
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: florida 1972-12-09: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 106. DISCREPANCY-FORDHAM-1972-73-008-GAME_DATE

- Category: discrepancy
- Matchup: california vs fordham
- Dates: source 1972-12-24; canonical 1972-12-23
- Field: game_date
- Source value: `1972-12-24`
- Canonical value: `1972-12-23`
- Evidence: california 1972-12-23: 1972-12-23
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 107. DISCREPANCY-FORDHAM-1972-73-017-SCORE

- Category: discrepancy
- Matchup: fordham vs rhode-island
- Date: 1973-01-27
- Field: score
- Source value: `72-92`
- Canonical value: `79-92`
- Evidence: rhode-island 1973-01-27: 79-92
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 108. DISCREPANCY-FORDHAM-1972-73-021-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs maryland
- Date: 1973-02-08
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: maryland 1973-02-08: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 109. DISCREPANCY-FORDHAM-1972-73-022-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs st-john-s
- Dates: source 1973-02-11; canonical 1973-02-10
- Field: game_date
- Source value: `1973-02-11`
- Canonical value: `1973-02-10`
- Evidence: st-john-s 1973-02-10: 1973-02-10
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 110. DISCREPANCY-FORDHAM-1972-73-022-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs st-john-s
- Dates: source 1973-02-11; canonical 1973-02-10
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: st-john-s 1973-02-10: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 111. DISCREPANCY-FORDHAM-1972-73-026-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs marquette
- Date: 1973-02-24
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1973-02-24: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 112. DISCREPANCY-FORDHAM-1973-74-015-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs usc
- Date: 1974-01-26
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: usc 1974-01-26: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 113. DISCREPANCY-FORDHAM-1974-75-009-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs usc
- Date: 1974-12-30
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: usc 1974-12-30: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 114. DISCREPANCY-FORDHAM-1974-75-021-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs marquette
- Date: 1975-02-20
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1975-02-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 115. DISCREPANCY-FORDHAM-1976-77-021-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs georgetown
- Dates: source 1977-02-09; canonical 1977-02-10
- Field: game_date
- Source value: `1977-02-09`
- Canonical value: `1977-02-10`
- Evidence: georgetown 1977-02-10: 1977-02-10
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 116. DISCREPANCY-FORDHAM-1978-79-023-SCORE

- Category: discrepancy
- Matchup: fordham vs st-john-s
- Date: 1979-02-10
- Field: score
- Source value: `43-66`
- Canonical value: `48-66`
- Evidence: st-john-s 1979-02-10: 48-66
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 117. DISCREPANCY-FORDHAM-1979-80-001-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs wagner
- Date: 1979-12-01
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: wagner 1979-12-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 118. DISCREPANCY-FORDHAM-1979-80-027-GAME_TYPE

- Category: discrepancy
- Matchup: fordham vs wagner
- Date: 1980-02-26
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: wagner 1980-02-26: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's frozen institutional conference chronology records the program as Independent through 1980-81 and its first MAAC season as 1981-82. A Fordham game in 1979-80 or 1980-81 therefore cannot be a Fordham conference-tournament game; preserve the accepted REGULAR_SEASON target classification.

### 119. DISCREPANCY-FORDHAM-1980-81-027-GAME_TYPE

- Category: discrepancy
- Matchup: fordham vs long-island-university
- Dates: source 1981-02-27; canonical [unknown]
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: long-island-university [unknown]: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's frozen institutional conference chronology records the program as Independent through 1980-81 and its first MAAC season as 1981-82. A Fordham game in 1979-80 or 1980-81 therefore cannot be a Fordham conference-tournament game; preserve the accepted REGULAR_SEASON target classification.

### 120. DISCREPANCY-FORDHAM-1981-82-006-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs syracuse
- Date: 1981-12-12
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: syracuse 1981-12-12: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 121. DISCREPANCY-FORDHAM-1982-83-005-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs ole-miss
- Dates: source 1982-12-09; canonical 1982-12-10
- Field: game_date
- Source value: `1982-12-09`
- Canonical value: `1982-12-10`
- Evidence: ole-miss 1982-12-10: 1982-12-10
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 122. DISCREPANCY-FORDHAM-1982-83-006-GAME_DATE

- Category: discrepancy
- Matchup: byu vs fordham
- Dates: source 1982-12-10; canonical 1982-12-11
- Field: game_date
- Source value: `1982-12-10`
- Canonical value: `1982-12-11`
- Evidence: byu 1982-12-11: 1982-12-11
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 123. DISCREPANCY-FORDHAM-1983-84-032-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs la-salle
- Date: 1984-03-01
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: la-salle 1984-03-01: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 124. DISCREPANCY-FORDHAM-1984-85-001-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs north-carolina
- Date: 1984-11-25
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: north-carolina 1984-11-25: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 125. DISCREPANCY-FORDHAM-1986-87-028-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs texas
- Date: 1987-02-21
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: texas 1987-02-21: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 126. DISCREPANCY-FORDHAM-1987-88-011-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs north-carolina
- Date: 1988-01-06
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: north-carolina 1988-01-06: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 127. DISCREPANCY-FORDHAM-1987-88-020-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs marquette
- Date: 1988-02-01
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: marquette 1988-02-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 128. DISCREPANCY-FORDHAM-1987-88-022-SCORE

- Category: discrepancy
- Matchup: fordham vs la-salle
- Date: 1988-02-06
- Field: score
- Source value: `51-76`
- Canonical value: `61-76`
- Evidence: la-salle 1988-02-06: 61-76
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 129. DISCREPANCY-FORDHAM-1987-88-032-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs la-salle
- Date: 1988-03-07
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: la-salle 1988-03-07: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 130. DISCREPANCY-FORDHAM-1988-89-029-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs la-salle
- Date: 1989-03-04
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: la-salle 1989-03-04: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 131. DISCREPANCY-FORDHAM-1989-90-031-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs la-salle
- Date: 1990-03-05
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: la-salle 1990-03-05: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 132. IDENTITY-FORDHAM-1995-96-006

- Category: identity
- Matchup: fordham vs st-john-s
- Dates: source 1995-12-23; canonical 1995-12-20
- Field: game_identity
- Source value: `date=1995-12-23; score=47-66`
- Canonical value: `CBBG-0159949`
- Evidence: CBBG-0159949 1995-1996 1995-12-20 47-66 sources=st-john-s
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0159949`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 133. CONDITIONAL-DISCREPANCY-FORDHAM-1995-96-006-CBBG-0159949-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs st-john-s
- Dates: source 1995-12-23; canonical 1995-12-20
- Field: game_date
- Source value: `1995-12-23`
- Canonical value: `1995-12-20`
- Evidence: st-john-s 1995-12-20: 1995-12-20
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0159949`

### 134. IDENTITY-FORDHAM-1995-96-016

- Category: identity
- Matchup: fordham vs virginia-tech
- Dates: source 1996-01-27; canonical 1996-01-24
- Field: game_identity
- Source value: `date=1996-01-27; score=57-81`
- Canonical value: `CBBG-0136831`
- Evidence: CBBG-0136831 1995-1996 1996-01-24 57-81 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136831`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 135. CONDITIONAL-DISCREPANCY-FORDHAM-1995-96-016-CBBG-0136831-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1996-01-27; canonical 1996-01-24
- Field: game_date
- Source value: `1996-01-27`
- Canonical value: `1996-01-24`
- Evidence: virginia-tech 1996-01-24: 1996-01-24
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136831`

### 136. IDENTITY-FORDHAM-1996-97-020

- Category: identity
- Matchup: fordham vs virginia-tech
- Dates: source 1997-02-08; canonical 1997-02-12;1997-03-12
- Field: game_identity
- Source value: `date=1997-02-08; score=32-50`
- Canonical value: `CBBG-0136861;CBBG-0136868`
- Evidence: CBBG-0136861 1996-1997 1997-02-12 32-50 sources=virginia-tech; CBBG-0136868 1996-1997 1997-03-12 53-56 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136861`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 137. CONDITIONAL-DISCREPANCY-FORDHAM-1996-97-020-CBBG-0136861-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1997-02-08; canonical 1997-02-12
- Field: game_date
- Source value: `1997-02-08`
- Canonical value: `1997-02-12`
- Evidence: virginia-tech 1997-02-12: 1997-02-12
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136861`

### 138. CONDITIONAL-DISCREPANCY-FORDHAM-1996-97-020-CBBG-0136868-GAME_DATE

- Category: conditional_discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1997-02-08; canonical 1997-03-12
- Field: game_date
- Source value: `1997-02-08`
- Canonical value: `1997-03-12`
- Evidence: virginia-tech 1997-03-12: 1997-03-12
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136861
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136868`

### 139. CONDITIONAL-DISCREPANCY-FORDHAM-1996-97-020-CBBG-0136868-SCORE

- Category: conditional_discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1997-02-08; canonical 1997-03-12
- Field: score
- Source value: `32-50`
- Canonical value: `53-56`
- Evidence: virginia-tech 1997-03-12: 53-56
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136861
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136868`

### 140. CONDITIONAL-DISCREPANCY-FORDHAM-1996-97-020-CBBG-0136868-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1997-02-08; canonical 1997-03-12
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1997-03-12: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136861
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136868`

### 141. CONDITIONAL-DISCREPANCY-FORDHAM-1996-97-020-CBBG-0136868-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1997-02-08; canonical 1997-03-12
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: virginia-tech 1997-03-12: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136861
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136868`

### 142. IDENTITY-FORDHAM-1996-97-027

- Category: identity
- Matchup: fordham vs virginia-tech
- Dates: source 1997-03-05; canonical 1997-02-12;1997-03-12
- Field: game_identity
- Source value: `date=1997-03-05; score=53-56`
- Canonical value: `CBBG-0136861;CBBG-0136868`
- Evidence: CBBG-0136861 1996-1997 1997-02-12 32-50 sources=virginia-tech; CBBG-0136868 1996-1997 1997-03-12 53-56 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136868`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 143. CONDITIONAL-DISCREPANCY-FORDHAM-1996-97-027-CBBG-0136861-GAME_DATE

- Category: conditional_discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1997-03-05; canonical 1997-02-12
- Field: game_date
- Source value: `1997-03-05`
- Canonical value: `1997-02-12`
- Evidence: virginia-tech 1997-02-12: 1997-02-12
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136861`

### 144. CONDITIONAL-DISCREPANCY-FORDHAM-1996-97-027-CBBG-0136861-SCORE

- Category: conditional_discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1997-03-05; canonical 1997-02-12
- Field: score
- Source value: `53-56`
- Canonical value: `32-50`
- Evidence: virginia-tech 1997-02-12: 32-50
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136861`

### 145. CONDITIONAL-DISCREPANCY-FORDHAM-1996-97-027-CBBG-0136861-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1997-03-05; canonical 1997-02-12
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: virginia-tech 1997-02-12: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136861`

### 146. CONDITIONAL-DISCREPANCY-FORDHAM-1996-97-027-CBBG-0136861-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1997-03-05; canonical 1997-02-12
- Field: game_type
- Source value: `CONFERENCE_TOURNAMENT`
- Canonical value: `REGULAR_SEASON`
- Evidence: virginia-tech 1997-02-12: REGULAR_SEASON
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136861`

### 147. CONDITIONAL-DISCREPANCY-FORDHAM-1996-97-027-CBBG-0136868-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1997-03-05; canonical 1997-03-12
- Field: game_date
- Source value: `1997-03-05`
- Canonical value: `1997-03-12`
- Evidence: virginia-tech 1997-03-12: 1997-03-12
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136868`

### 148. DISCREPANCY-FORDHAM-1998-99-027-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs virginia-tech
- Dates: source 1999-03-04; canonical 1999-03-03
- Field: game_date
- Source value: `1999-03-04`
- Canonical value: `1999-03-03`
- Evidence: virginia-tech 1999-03-03: 1999-03-03
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 149. DISCREPANCY-FORDHAM-2001-02-001-SITE_TYPE

- Category: discrepancy
- Matchup: depaul vs fordham
- Date: 2001-11-12
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: depaul 2001-11-12: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 150. DISCREPANCY-FORDHAM-2012-13-031-SCORE

- Category: discrepancy
- Matchup: fordham vs st-bonaventure
- Date: 2013-03-09
- Field: score
- Source value: `76-72`
- Canonical value: `76-7`
- Evidence: st-bonaventure 2013-03-09: 76-7
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 151. DISCREPANCY-FORDHAM-2016-17-018-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs st-bonaventure
- Date: 2017-01-14
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: st-bonaventure 2017-01-14: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 152. DISCREPANCY-FORDHAM-2017-18-017-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs fordham
- Date: 2018-01-14
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: davidson 2018-01-14: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 153. DISCREPANCY-FORDHAM-2018-19-016-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs st-bonaventure
- Date: 2019-01-12
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: st-bonaventure 2019-01-12: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fordham's accepted frozen target package carries an affirmative H/A/N conclusion for this game (including explicit 'at', HOME chronology, or accepted neutral venue/locality evidence). Preserve the settled target-school historical assertion and retain the reciprocal disagreement as provenance rather than silently replacing the frozen conclusion.

### 154. DISCREPANCY-FORDHAM-2018-19-024-SCORE

- Category: discrepancy
- Matchup: davidson vs fordham
- Date: 2019-02-12
- Field: score
- Source value: `79-68`
- Canonical value: `79-69`
- Evidence: davidson 2019-02-12: 79-69
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 155. IDENTITY-FORDHAM-2019-20-027

- Category: identity
- Matchup: fordham vs rhode-island
- Dates: source 2020-02-26; canonical 2020-02-24
- Field: game_identity
- Source value: `date=2020-02-26; score=75-76`
- Canonical value: `CBBG-0196390`
- Evidence: CBBG-0196390 2019-2020 2020-02-24 75-76 sources=rhode-island
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0196390`
- Basis: One real game equals one canonical game. Match the unique reciprocal candidate supported by same-season matchup context and score/result where it represents the same historical game; do not create a duplicate canonical game merely because a source date or score conflicts.

### 156. CONDITIONAL-DISCREPANCY-FORDHAM-2019-20-027-CBBG-0196390-GAME_DATE

- Category: discrepancy
- Matchup: fordham vs rhode-island
- Dates: source 2020-02-26; canonical 2020-02-24
- Field: game_date
- Source value: `2020-02-26`
- Canonical value: `2020-02-24`
- Evidence: rhode-island 2020-02-24: 2020-02-24
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0196390`

### 157. DISCREPANCY-FORDHAM-2023-24-015-SCORE

- Category: discrepancy
- Matchup: fordham vs la-salle
- Date: 2024-01-06
- Field: score
- Source value: `75-81`
- Canonical value: `76-81`
- Evidence: la-salle 2024-01-06: 76-81
- Recommended: `KEEP_CANONICAL`
- Decision: `LEAVE_UNRESOLVED`
- Basis: Fordham's accepted frozen target evidence and an accepted reciprocal/canonical assertion disagree on this date/score/result field, and this Gate 1 packet contains no stronger independent authority that justifies overwriting either side. Preserve both assertions and leave the conflict explicitly unresolved.

### 158. CANONICAL-SITE-PATCH-CBBG-0162161

- Category: canonical_site_patch
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1913-01-08
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from seton-hall; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because target identity was matched to this canonical game: FORDHAM-1912-13-008

### 159. CANONICAL-SITE-PATCH-CBBG-0162174

- Category: canonical_site_patch
- Matchup: fordham vs seton-hall
- Dates: source [unknown]; canonical 1914-01-07
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from seton-hall; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because target identity was matched to this canonical game: FORDHAM-1913-14-012

### 160. HISTORICAL-NCAA-QUALIFIER-FORDHAM-1990-91-031

- Category: postseason_classification
- Matchup: fordham vs saint-francis-pa
- Date: 1991-03-06
- Field: postseason_round
- Source value: `Play-in`
- Canonical value: ``
- Evidence: Fordham institutional history establishes that the Patriot League lacked an automatic bid; Fordham lost the NCAA-administered Saint Francis play-in, then still awaited an NCAA at-large bid, did not receive one, and entered the NIT. The game is therefore a qualifier outside the national bracket rather than an NCAA Tournament appearance. This is a post-freeze NCAA non-appearance qualifier challenge only; Owner Gate 1 must explicitly approve clearing the controlled round and applying the durable qualifier marker.
- Recommended: `APPLY_POSTSEASON_CLASSIFICATION_PATCH`
- Decision: `APPLY_POSTSEASON_CLASSIFICATION_PATCH`
- Basis: Control Center Issue #502 / merged PR #503 preserve the settled Fordham institutional interpretation: the March 6, 1991 Saint Francis game was an NCAA-administered qualifier outside the national bracket. Keep broad NCAA_TOURNAMENT provenance, clear the controlled Play-in round, append the durable NCAA non-appearance qualifier marker, and preserve every unrelated frozen field. This remains pending Owner Gate 1 approval.

### 161. ACCOMPLISHMENTS-FORDHAM

- Category: accomplishments
- Matchup: fordham
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"SWEET_SIXTEEN","best_finish_year":"1971","conference_regular_season_championships":"4","conference_tournament_championships":"3","final_four_appearances":"0","national_championships":"0","ncaa_tournament_appearances":"4"}`
- Canonical value: `{"best_finish_key":"SWEET_SIXTEEN","best_finish_year":1971,"final_four_appearances":0,"national_championships":0,"ncaa_tournament_appearances":5}`
- Evidence: Projected NCAA totals depend on explicit owner-reviewed classification and round decisions for generic postseason source games; the normal sealed disposable rehearsal must establish exact canonical accomplishment equality before publication or VERIFIED status.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `APPLY_ACCOMPLISHMENT_PATCH`
- Basis: Authoritative records correct the owner baseline regular-season title count from 4 to 3: the Patriot League official men's basketball record book credits Fordham with regular-season titles in 1991, 1992 (co-champion), and 1994 (co-champion), and two Patriot tournament championships (1991, 1992); MAAC/Fordham records establish the 1983 MAAC tournament title. Fordham institutional records support the NCAA appearance/best-finish fields after the separately owner-reviewed 1991 non-appearance qualifier correction. Sources: https://s3.amazonaws.com/sidearm.sites/patriotleague.org/documents/2022/8/23/PatriotMBB_2022_23_Record_Book.pdf ; https://themetro.org/sports/2007/6/30/1060599.aspx ; https://fordhamsports.com/honors/hall-of-fame/edward-conlin/59 ; https://fordhamsports.com/news/2020/3/20/on-this-day-mens-basketball-defeats-6-south-carolina-in-1971-ncaas ; https://fordhamsports.com/honors/hall-of-fame/jean-eduard-prioleau/290/kiosk

### 162. PUBLICATION-FORDHAM

- Category: publication
- Matchup: fordham
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 2,917 in-scope source rows; 22 identity reviews; 83 definite and 52 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `ENABLE_PUBLIC_PAGE`
- Basis: Enable Fordham's public page only as part of the sealed onboarding transaction after explicit Owner Gate 1 approval of this exact 162-decision packet and successful permanent apply/publication gates. The accepted scope is 1902-03+ / INCEPTION+ and all 2,917 frozen competitive rows are in scope.
