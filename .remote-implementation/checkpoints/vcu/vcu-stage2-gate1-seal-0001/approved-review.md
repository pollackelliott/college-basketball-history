# vcu onboarding review

Generated: 2026-11-09T12:20:01.314965+00:00
Input fingerprint: `5e3f1204afc623bf83bab9755563385751d04771c2b1017c0342ae429fc99d06`
Approved plan: `008612bb8da432a15b60b60c6caa4cf63760d0614a69fff19a51e72f428fbf10`

## Preflight summary

- Source rows: 1,650
- In-scope rows: 1,650
- Pre-cutoff researched rows: 0
- Existing matches: 489
- New canonical games: 1,152
- Identity reviews: 9
- Safe enrichment fields: 892
- Discrepancies: 37
- Conditional discrepancies: 37
- Canonical-only site reviews: 1
- Affected existing public programs: alabama, arizona-state, arkansas, auburn, baylor, boise-state, boston-college, butler, byu, california, cincinnati, colorado, colorado-state, davidson, dayton, duke, duquesne, fairleigh-dickinson, florida-state, fordham, george-mason, georgetown, georgia, georgia-tech, houston, illinois, indiana, iowa, iowa-state, kansas, kansas-state, la-salle, long-island-university, louisville, loyola-chicago, lsu, marquette, maryland, miami, michigan, michigan-state, mississippi-state, missouri, nc-state, north-carolina, northwestern, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, penn-state, pittsburgh, purdue, rhode-island, rutgers, saint-joseph-s, saint-louis, seton-hall, smu, st-bonaventure, st-john-s, syracuse, tcu, tennessee, texas, texas-a-m, ucf, ucla, uconn, usc, utah, utah-state, vanderbilt, villanova, virginia, virginia-tech, wagner, wake-forest, west-virginia, wisconsin, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. IDENTITY-VCU-1974-75-011

- Category: identity
- Matchup: vcu vs texas-a-m
- Dates: source 1974-12-29; canonical 1974-12-10;1974-12-30
- Field: game_identity
- Source value: `date=1974-12-29; score=80-84`
- Canonical value: `CBBG-0066492;CBBG-0066496`
- Evidence: CBBG-0066492 1974-1975 1974-12-10 98-84 sources=texas-a-m; CBBG-0066496 1974-1975 1974-12-30 84-70 sources=texas-a-m
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0066496`
- Basis: Match CBBG-0066496. Texas A&M's institutional sequence has Fairfield on Dec. 29 and at VCU on Dec. 30, 1974, W 84-70; VCU already carries the separate Dec. 10 Texas A&M game. The Dec. 29/80-84 frozen VCU row is therefore the Dec. 30 game with source date/score drift, not a third contest.

### 2. CONDITIONAL-DISCREPANCY-VCU-1974-75-011-CBBG-0066492-GAME_DATE

- Category: conditional_discrepancy
- Matchup: texas-a-m vs vcu
- Dates: source 1974-12-29; canonical 1974-12-10
- Field: game_date
- Source value: `1974-12-29`
- Canonical value: `1974-12-10`
- Evidence: texas-a-m 1974-12-10: 1974-12-10
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0066496
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0066492`

### 3. CONDITIONAL-DISCREPANCY-VCU-1974-75-011-CBBG-0066492-SCORE

- Category: conditional_discrepancy
- Matchup: texas-a-m vs vcu
- Dates: source 1974-12-29; canonical 1974-12-10
- Field: score
- Source value: `84-80`
- Canonical value: `98-84`
- Evidence: texas-a-m 1974-12-10: 98-84
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0066496
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0066492`

### 4. CONDITIONAL-DISCREPANCY-VCU-1974-75-011-CBBG-0066492-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: texas-a-m vs vcu
- Dates: source 1974-12-29; canonical 1974-12-10
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: texas-a-m 1974-12-10: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0066496
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0066492`

### 5. CONDITIONAL-DISCREPANCY-VCU-1974-75-011-CBBG-0066496-GAME_DATE

- Category: discrepancy
- Matchup: texas-a-m vs vcu
- Dates: source 1974-12-29; canonical 1974-12-30
- Field: game_date
- Source value: `1974-12-29`
- Canonical value: `1974-12-30`
- Evidence: texas-a-m 1974-12-30: 1974-12-30
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the target source date to Dec. 30, 1974 because Texas A&M's institutional sequence identifies the Dec. 30 at-VCU game and separately accounts for Dec. 29.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0066496`

### 6. CONDITIONAL-DISCREPANCY-VCU-1974-75-011-CBBG-0066496-SCORE

- Category: discrepancy
- Matchup: texas-a-m vs vcu
- Dates: source 1974-12-29; canonical 1974-12-30
- Field: score
- Source value: `84-80`
- Canonical value: `84-70`
- Evidence: texas-a-m 1974-12-30: 84-70
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the target source score to Texas A&M 84, VCU 70. The institutional Texas A&M game sequence and exact matched identity support 84-70; 80-84 is frozen source transcription drift.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0066496`

### 7. DISCREPANCY-VCU-1976-77-009-SITE_TYPE

- Category: discrepancy
- Matchup: vcu vs virginia
- Date: 1976-12-29
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia 1976-12-29: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the accepted frozen VCU HOME designation. The target row is affirmatively home under VCU's accepted marker-era evidence and Richmond Coliseum assignment; reciprocal Virginia classifies the tournament-context game neutral, so preserve that conflict for Owner Gate 1 rather than silently overriding the target.

### 8. DISCREPANCY-VCU-1977-78-021-SITE_TYPE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Date: 1978-02-10
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1978-02-10: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend the accepted frozen VCU HOME designation. VCU's target evidence and marker-era rules classify the Richmond Coliseum game home; Virginia Tech's tournament-context record classifies it neutral. This is a genuine historical designation conflict, not a geography inference.

### 9. DISCREPANCY-VCU-1977-78-027-GAME_TYPE

- Category: discrepancy
- Matchup: georgetown vs vcu
- Date: 1978-03-01
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: georgetown 1978-03-01: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use the frozen generic POSTSEASON type. Research deliberately retained the 1978 ECAC South game outside the repository's controlled NCAA/NIT/conference-tournament classes; do not silently recast the ECAC regional event as a conference tournament.

### 10. DISCREPANCY-VCU-1979-80-008-SITE_TYPE

- Category: discrepancy
- Matchup: vcu vs virginia
- Date: 1979-12-28
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia 1979-12-28: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the VCU source to NEUTRAL. Virginia's reciprocal institutional classification is neutral, and independent schedule evidence places the Dec. 28, 1979 VCU-Virginia game outside the frozen HOME interpretation. Remove the unsupported Richmond Coliseum building assignment but retain Richmond locality.

### 11. IDENTITY-VCU-1984-85-032

- Category: identity
- Matchup: vcu vs alabama
- Dates: source 1985-03-17; canonical 1985-03-22
- Field: game_identity
- Source value: `date=1985-03-17; score=59-63`
- Canonical value: `CBBG-0028889`
- Evidence: CBBG-0028889 1984-1985 1985-03-22 63-59 sources=alabama
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0028889`
- Basis: Match CBBG-0028889 by exact Alabama/VCU NCAA game identity and 63-59 Alabama win. Current institutional/NCAA history places the game on Mar. 17, 1985, so the selected date discrepancy should use the frozen VCU date.

### 12. CONDITIONAL-DISCREPANCY-VCU-1984-85-032-CBBG-0028889-GAME_DATE

- Category: discrepancy
- Matchup: alabama vs vcu
- Dates: source 1985-03-17; canonical 1985-03-22
- Field: game_date
- Source value: `1985-03-17`
- Canonical value: `1985-03-22`
- Evidence: alabama 1985-03-22: 1985-03-22
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Mar. 17, 1985; this is the actual Alabama/VCU NCAA Tournament date.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0028889`

### 13. DISCREPANCY-VCU-1985-86-005-SCORE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Date: 1985-12-14
- Field: score
- Source value: `65-67`
- Canonical value: `57-59`
- Evidence: virginia-tech 1985-12-14: 57-59
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source VCU 65-67. Current VCU institutional series history supports 65-67; Virginia Tech's current history supports 59-57. With a live one-score reciprocal conflict and no decisive third institutional authority, recommend the immutable target source rather than overwriting it.

### 14. DISCREPANCY-VCU-1987-88-008-SITE_TYPE

- Category: discrepancy
- Matchup: vcu vs virginia
- Date: 1987-12-19
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia 1987-12-19: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend frozen VCU HOME. The target's accepted H/A/N evidence classifies the Dec. 19, 1987 Times-Dispatch Invitational game home at Richmond Coliseum; reciprocal Virginia treats the tournament game neutral. Preserve the target recommendation and surface residual uncertainty.

### 15. DISCREPANCY-VCU-1988-89-008-GAME_DATE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1988-12-30; canonical 1988-12-29
- Field: game_date
- Source value: `1988-12-30`
- Canonical value: `1988-12-29`
- Evidence: virginia-tech 1988-12-29: 1988-12-29
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Dec. 30, 1988. Virginia Tech's current official historical schedule lists its 97-91 win at VCU on Dec. 30. Authority: https://stats.hokiesports.com/mbasketball/records/schedule.html

### 16. DISCREPANCY-VCU-1989-90-008-SITE_TYPE

- Category: discrepancy
- Matchup: vcu vs virginia
- Date: 1989-12-20
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia 1989-12-20: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Recommend frozen VCU HOME. Target and historical series evidence support VCU home at Richmond Coliseum; reciprocal Virginia labels the Times-Dispatch Invitational game neutral. Preserve the explicit target classification for owner disposition.

### 17. IDENTITY-VCU-1989-90-011

- Category: identity
- Matchup: vcu vs virginia-tech
- Dates: source 1990-01-08; canonical 1990-01-06
- Field: game_identity
- Source value: `date=1990-01-08; score=68-71`
- Canonical value: `CBBG-0136691`
- Evidence: CBBG-0136691 1989-1990 1990-01-06 68-71 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136691`
- Basis: Match CBBG-0136691 by exact opponent and 71-68 Virginia Tech win. Virginia Tech's current official historical schedule lists VCU on Jan. 8, 1990, so use the VCU source date rather than the stale Jan. 6 canonical date. Authority: https://stats.hokiesports.com/mbasketball/records/schedule.html

### 18. CONDITIONAL-DISCREPANCY-VCU-1989-90-011-CBBG-0136691-GAME_DATE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1990-01-08; canonical 1990-01-06
- Field: game_date
- Source value: `1990-01-08`
- Canonical value: `1990-01-06`
- Evidence: virginia-tech 1990-01-06: 1990-01-06
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Jan. 8, 1990; Virginia Tech's current official historical schedule independently confirms it.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136691`

### 19. IDENTITY-VCU-1990-91-006

- Category: identity
- Matchup: vcu vs virginia-tech
- Dates: source 1990-12-11; canonical 1990-12-08
- Field: game_identity
- Source value: `date=1990-12-11; score=75-77`
- Canonical value: `CBBG-0136707`
- Evidence: CBBG-0136707 1990-1991 1990-12-08 75-77 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136707`
- Basis: Match CBBG-0136707 by exact opponent and 77-75 Virginia Tech overtime win. Virginia Tech's current official history lists the game on Dec. 11, 1990, so use the VCU source date rather than Dec. 8. Authority: https://stats.hokiesports.com/mbasketball/records/schedule.html

### 20. CONDITIONAL-DISCREPANCY-VCU-1990-91-006-CBBG-0136707-GAME_DATE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1990-12-11; canonical 1990-12-08
- Field: game_date
- Source value: `1990-12-11`
- Canonical value: `1990-12-08`
- Evidence: virginia-tech 1990-12-08: 1990-12-08
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Dec. 11, 1990; Virginia Tech's current official historical schedule independently confirms it.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136707`

### 21. DISCREPANCY-VCU-1991-92-006-GAME_DATE

- Category: discrepancy
- Matchup: george-mason vs vcu
- Dates: source 1991-12-11; canonical 1991-12-12
- Field: game_date
- Source value: `1991-12-11`
- Canonical value: `1991-12-12`
- Evidence: george-mason 1991-12-12: 1991-12-12
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical Dec. 12, 1991. The only current reciprocal project authority gives Dec. 12, while the frozen VCU row gives Dec. 11 and VCU's current online opponent-history series does not cover this pre-1993 game. Recommend canonical but retain the one-day source conflict.

### 22. IDENTITY-VCU-1991-92-022

- Category: identity
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-01-11;1992-02-15
- Field: game_identity
- Source value: `date=1992-02-20; score=63-60`
- Canonical value: `CBBG-0136728;CBBG-0136737`
- Evidence: CBBG-0136728 1991-1992 1992-01-11 72-73 sources=virginia-tech; CBBG-0136737 1991-1992 1992-02-15 63-60 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136737`
- Basis: Match CBBG-0136737: its 63-60 score uniquely identifies the Feb. 20, 1992 VCU win among the two same-season Virginia Tech games. Virginia Tech's current official schedule confirms Feb. 20 at Richmond Coliseum. Authority: https://stats.hokiesports.com/mbasketball/records/schedule.html

### 23. CONDITIONAL-DISCREPANCY-VCU-1991-92-022-CBBG-0136728-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-01-11
- Field: game_date
- Source value: `1992-02-20`
- Canonical value: `1992-01-11`
- Evidence: virginia-tech 1992-01-11: 1992-01-11
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136737
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136728`

### 24. CONDITIONAL-DISCREPANCY-VCU-1991-92-022-CBBG-0136728-SCORE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-01-11
- Field: score
- Source value: `63-60`
- Canonical value: `72-73`
- Evidence: virginia-tech 1992-01-11: 72-73
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136737
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136728`

### 25. CONDITIONAL-DISCREPANCY-VCU-1991-92-022-CBBG-0136728-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-01-11
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: virginia-tech 1992-01-11: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136737
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136728`

### 26. CONDITIONAL-DISCREPANCY-VCU-1991-92-022-CBBG-0136728-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-01-11
- Field: result_winner_team_key
- Source value: `vcu`
- Canonical value: `virginia-tech`
- Evidence: virginia-tech 1992-01-11: virginia-tech
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136737
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136728`

### 27. CONDITIONAL-DISCREPANCY-VCU-1991-92-022-CBBG-0136737-GAME_DATE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1992-02-20; canonical 1992-02-15
- Field: game_date
- Source value: `1992-02-20`
- Canonical value: `1992-02-15`
- Evidence: virginia-tech 1992-02-15: 1992-02-15
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Feb. 20, 1992; Virginia Tech's current official historical schedule lists the 60-63 loss at VCU on that date.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136737`

### 28. IDENTITY-VCU-1992-93-018

- Category: identity
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-02-03;1993-02-20;1993-03-13
- Field: game_identity
- Source value: `date=1993-02-06; score=73-54`
- Canonical value: `CBBG-0136758;CBBG-0136763;CBBG-0136768`
- Evidence: CBBG-0136758 1992-1993 1993-02-03 73-54 sources=virginia-tech; CBBG-0136763 1992-1993 1993-02-20 86-69 sources=virginia-tech; CBBG-0136768 1992-1993 1993-03-13 85-71 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136758`
- Basis: Match CBBG-0136758: the 73-54 score uniquely identifies Virginia Tech's Feb. 6, 1993 home loss to VCU. Virginia Tech's current official schedule confirms the date. Authority: https://stats.hokiesports.com/mbasketball/records/schedule.html

### 29. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136758-GAME_DATE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-02-03
- Field: game_date
- Source value: `1993-02-06`
- Canonical value: `1993-02-03`
- Evidence: virginia-tech 1993-02-03: 1993-02-03
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Feb. 6, 1993; Virginia Tech's current official historical schedule lists the 54-73 home loss on that date.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136758`

### 30. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136763-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-02-20
- Field: game_date
- Source value: `1993-02-06`
- Canonical value: `1993-02-20`
- Evidence: virginia-tech 1993-02-20: 1993-02-20
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136758
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136763`

### 31. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136763-SCORE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-02-20
- Field: score
- Source value: `73-54`
- Canonical value: `86-69`
- Evidence: virginia-tech 1993-02-20: 86-69
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136758
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136763`

### 32. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136763-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-02-20
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: virginia-tech 1993-02-20: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136758
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136763`

### 33. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136768-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-03-13
- Field: game_date
- Source value: `1993-02-06`
- Canonical value: `1993-03-13`
- Evidence: virginia-tech 1993-03-13: 1993-03-13
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136758
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 34. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136768-SCORE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-03-13
- Field: score
- Source value: `73-54`
- Canonical value: `85-71`
- Evidence: virginia-tech 1993-03-13: 85-71
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136758
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 35. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136768-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-03-13
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1993-03-13: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136758
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 36. CONDITIONAL-DISCREPANCY-VCU-1992-93-018-CBBG-0136768-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-06; canonical 1993-03-13
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: virginia-tech 1993-03-13: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136758
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 37. IDENTITY-VCU-1992-93-023

- Category: identity
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-02-03;1993-02-20;1993-03-13
- Field: game_identity
- Source value: `date=1993-02-22; score=86-69`
- Canonical value: `CBBG-0136758;CBBG-0136763;CBBG-0136768`
- Evidence: CBBG-0136758 1992-1993 1993-02-03 73-54 sources=virginia-tech; CBBG-0136763 1992-1993 1993-02-20 86-69 sources=virginia-tech; CBBG-0136768 1992-1993 1993-03-13 85-71 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136763`
- Basis: Match CBBG-0136763: the 86-69 score uniquely identifies Virginia Tech's Feb. 22, 1993 road loss at VCU. Virginia Tech's current official schedule confirms the date. Authority: https://stats.hokiesports.com/mbasketball/records/schedule.html

### 38. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136758-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-02-03
- Field: game_date
- Source value: `1993-02-22`
- Canonical value: `1993-02-03`
- Evidence: virginia-tech 1993-02-03: 1993-02-03
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136763
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136758`

### 39. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136758-SCORE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-02-03
- Field: score
- Source value: `86-69`
- Canonical value: `73-54`
- Evidence: virginia-tech 1993-02-03: 73-54
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136763
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136758`

### 40. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136758-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-02-03
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: virginia-tech 1993-02-03: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136763
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136758`

### 41. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136763-GAME_DATE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-02-20
- Field: game_date
- Source value: `1993-02-22`
- Canonical value: `1993-02-20`
- Evidence: virginia-tech 1993-02-20: 1993-02-20
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Feb. 22, 1993; Virginia Tech's current official historical schedule lists the 69-86 road loss on that date.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136763`

### 42. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136768-GAME_DATE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-03-13
- Field: game_date
- Source value: `1993-02-22`
- Canonical value: `1993-03-13`
- Evidence: virginia-tech 1993-03-13: 1993-03-13
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136763
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 43. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136768-SCORE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-03-13
- Field: score
- Source value: `86-69`
- Canonical value: `85-71`
- Evidence: virginia-tech 1993-03-13: 85-71
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136763
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 44. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136768-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-03-13
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: virginia-tech 1993-03-13: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136763
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 45. CONDITIONAL-DISCREPANCY-VCU-1992-93-023-CBBG-0136768-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: vcu vs virginia-tech
- Dates: source 1993-02-22; canonical 1993-03-13
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: virginia-tech 1993-03-13: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136763
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136768`

### 46. DISCREPANCY-VCU-1993-94-022-SCORE

- Category: discrepancy
- Matchup: vcu vs virginia-tech
- Date: 1994-02-17
- Field: score
- Source value: `59-76`
- Canonical value: `59-75`
- Evidence: virginia-tech 1994-02-17: 59-75
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source VCU 59-76. VCU's current institutional schedule/series record gives a 59-76 loss at Virginia Tech; Virginia Tech currently gives 75-59. Recommend direct target authority while preserving the one-point reciprocal conflict.

### 47. IDENTITY-VCU-1994-95-029

- Category: identity
- Matchup: vcu vs louisville
- Dates: source 1995-03-05; canonical 1995-01-05;1995-03-02;1995-03-10
- Field: game_identity
- Source value: `date=1995-03-05; score=64-80`
- Canonical value: `CBBG-0144854;CBBG-0144868;CBBG-0144869`
- Evidence: CBBG-0144854 1994-1995 1995-01-05 63-67 sources=louisville; CBBG-0144868 1994-1995 1995-03-02 80-64 sources=louisville; CBBG-0144869 1994-1995 1995-03-10 84-61 sources=louisville
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0144868`
- Basis: Match CBBG-0144868. Louisville's Mar. 2, 1995 80-64 win is the exact score/orientation match; the other same-season Louisville candidates have different scores. Normalize the frozen Mar. 5 date to Mar. 2.

### 48. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144854-GAME_DATE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-01-05
- Field: game_date
- Source value: `1995-03-05`
- Canonical value: `1995-01-05`
- Evidence: louisville 1995-01-05: 1995-01-05
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0144868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144854`

### 49. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144854-SCORE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-01-05
- Field: score
- Source value: `80-64`
- Canonical value: `63-67`
- Evidence: louisville 1995-01-05: 63-67
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0144868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144854`

### 50. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144854-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-01-05
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: louisville 1995-01-05: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0144868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144854`

### 51. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144854-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-01-05
- Field: result_winner_team_key
- Source value: `louisville`
- Canonical value: `vcu`
- Evidence: louisville 1995-01-05: vcu
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0144868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144854`

### 52. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144868-GAME_DATE

- Category: discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-03-02
- Field: game_date
- Source value: `1995-03-05`
- Canonical value: `1995-03-02`
- Evidence: louisville 1995-03-02: 1995-03-02
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the target source date to Mar. 2, 1995; Louisville's current official history identifies the exact 80-64 contest on Mar. 2.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144868`

### 53. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144869-GAME_DATE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-03-10
- Field: game_date
- Source value: `1995-03-05`
- Canonical value: `1995-03-10`
- Evidence: louisville 1995-03-10: 1995-03-10
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0144868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144869`

### 54. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144869-SCORE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-03-10
- Field: score
- Source value: `80-64`
- Canonical value: `84-61`
- Evidence: louisville 1995-03-10: 84-61
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0144868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144869`

### 55. CONDITIONAL-DISCREPANCY-VCU-1994-95-029-CBBG-0144869-GAME_TYPE

- Category: conditional_discrepancy
- Matchup: louisville vs vcu
- Dates: source 1995-03-05; canonical 1995-03-10
- Field: game_type
- Source value: `REGULAR_SEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: louisville 1995-03-10: CONFERENCE_TOURNAMENT
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0144868
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0144869`

### 56. DISCREPANCY-VCU-1996-97-008-SITE_TYPE

- Category: discrepancy
- Matchup: tcu vs vcu
- Date: 1996-12-27
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: tcu 1996-12-27: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the source to NEUTRAL and correct the physical site to historical Levitt Arena in Wichita, Kansas. TCU's institutional row classifies the Cessna Classic game neutral, and Wichita State event/facility evidence places the event at Levitt Arena. The registered physical identity is Charles Koch Arena, VEN-000039.

### 57. DISCREPANCY-VCU-2000-01-006-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: texas-a-m vs vcu
- Date: 2000-12-02
- Field: overtime_periods
- Source value: `2`
- Canonical value: `1`
- Evidence: texas-a-m 2000-12-02: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source 2OT. VCU's current history and Texas A&M's contemporary institutional recap both identify the Dec. 2, 2000 game as double overtime.

### 58. DISCREPANCY-VCU-2004-05-002-GAME_DATE

- Category: discrepancy
- Matchup: vcu vs wake-forest
- Dates: source 2004-11-18; canonical 2004-11-19
- Field: game_date
- Source value: `2004-11-18`
- Canonical value: `2004-11-19`
- Evidence: wake-forest 2004-11-19: 2004-11-19
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Nov. 18, 2004. Wake Forest's contemporary institutional archive identifies the VCU game on Nov. 18; the Nov. 19 canonical date is stale.

### 59. DISCREPANCY-VCU-2009-10-023-SITE_TYPE

- Category: discrepancy
- Matchup: george-mason vs vcu
- Date: 2010-02-09
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: george-mason 2010-02-09: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source OPPONENT_HOME. VCU's current institutional George Mason history explicitly lists Feb. 9, 2010 as an away game in Fairfax, so the reciprocal canonical VCU-home designation is erroneous.

### 60. DISCREPANCY-VCU-2010-11-003-SCORE

- Category: discrepancy
- Matchup: vcu vs wake-forest
- Date: 2010-11-16
- Field: score
- Source value: `90-69`
- Canonical value: `80-69`
- Evidence: wake-forest 2010-11-16: 80-69
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source VCU 90-69. VCU's current schedule, cumulative statistics, and contemporary recap all give the Nov. 16, 2010 Wake Forest final as 90-69.

### 61. DISCREPANCY-VCU-2011-12-006-SITE_TYPE

- Category: discrepancy
- Matchup: alabama vs vcu
- Date: 2011-11-27
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: alabama 2011-11-27: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source OPPONENT_HOME. The VCU frozen row explicitly says at Alabama; canonical UNKNOWN is weaker than affirmative target site authority.

### 62. DISCREPANCY-VCU-2012-13-006-SCORE

- Category: discrepancy
- Matchup: missouri vs vcu
- Date: 2012-11-24
- Field: score
- Source value: `65-58`
- Canonical value: `68-65`
- Evidence: missouri 2012-11-24: 68-65
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the frozen structured score to VCU 65, Missouri 68. VCU's own exact 2012 box score gives 65-68; the frozen 58-65 orientation arose from a literal-source transcription error. Preserve raw_text unchanged. Authority: https://vcuathletics.com/sports/mens-basketball/stats/2012-13/-13-missouri/boxscore/1271

### 63. DISCREPANCY-VCU-2012-13-006-SITE_TYPE

- Category: discrepancy
- Matchup: missouri vs vcu
- Date: 2012-11-24
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: missouri 2012-11-24: UNKNOWN
- Recommended: `LEAVE_UNRESOLVED`
- Decision: `USE_SOURCE`
- Basis: Use the target NEUTRAL designation and correct the curated physical site to Imperial Arena, Nassau, BS. VCU's exact box score says Battle 4 Atlantis at Imperial Arena, Paradise Island, Bahamas; the frozen Mizzou Arena/Columbia assignment is wrong. Authority: https://vcuathletics.com/sports/mens-basketball/stats/2012-13/-13-missouri/boxscore/1271

### 64. DISCREPANCY-VCU-2013-14-034-SCORE

- Category: discrepancy
- Matchup: saint-joseph-s vs vcu
- Date: 2014-03-16
- Field: score
- Source value: `65-61`
- Canonical value: `64-61`
- Evidence: saint-joseph-s 2014-03-16: 64-61
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source VCU 61-65. VCU's current institutional Saint Joseph's series history gives the Mar. 16, 2014 loss as 61-65; reciprocal 64-61 conflicts by one point.

### 65. DISCREPANCY-VCU-2014-15-031-SCORE

- Category: discrepancy
- Matchup: george-mason vs vcu
- Date: 2015-03-07
- Field: score
- Source value: `60-71`
- Canonical value: `51-67`
- Evidence: george-mason 2015-03-07: 51-67
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source VCU 71-60. VCU's current George Mason history and contemporary recap both give the Mar. 7, 2015 final as 71-60.

### 66. DISCREPANCY-VCU-2016-17-023-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: st-bonaventure vs vcu
- Date: 2017-02-04
- Field: overtime_periods
- Source value: `1`
- Canonical value: `0`
- Evidence: st-bonaventure 2017-02-04: 0
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source 1OT. The reciprocal St. Bonaventure structured value is 0 but its preserved raw source explicitly says OT; the frozen VCU overtime token is therefore the coherent value.

### 67. DISCREPANCY-VCU-2019-20-014-SITE_TYPE

- Category: discrepancy
- Matchup: fordham vs vcu
- Date: 2020-01-02
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: fordham 2020-01-02: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize the VCU source to SOURCE_PROGRAM_HOME at Siegel Center. VCU's current Fordham opponent history explicitly lists Jan. 2, 2020 as a home 64-46 win; the frozen OPPONENT_HOME classification is wrong.

### 68. DISCREPANCY-VCU-2019-20-022-SCORE

- Category: discrepancy
- Matchup: rhode-island vs vcu
- Date: 2020-01-31
- Field: score
- Source value: `87-75`
- Canonical value: `81-75`
- Evidence: rhode-island 2020-01-31: 81-75
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source VCU 75-87. VCU's current Rhode Island series history lists the Jan. 31, 2020 road loss as 75-87; reciprocal canonical 81-75 is erroneous.

### 69. IDENTITY-VCU-2020-21-011

- Category: identity
- Matchup: vcu vs george-washington
- Date: 2021-01-06
- Field: game_identity
- Source value: `date=2021-01-06; score=66-61`
- Canonical value: `CBBG-0203017`
- Evidence: CBBG-0203017 2020-2021 2021-01-06 61-66 sources=george-mason
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0203017`
- Basis: Match CBBG-0203017 and use the plan's built-in cross-opponent source patch to George Mason. VCU's current official statistics list Jan. 6, 2021 at George Mason, W 66-61, while the actual George Washington game was Jan. 13, W 84-77. Authority: https://vcuathletics.com/sports/mens-basketball/stats/2020-21

### 70. DISCREPANCY-VCU-2020-21-025-SITE_TYPE

- Category: discrepancy
- Matchup: davidson vs vcu
- Date: 2021-03-06
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: davidson 2021-03-06: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source SOURCE_PROGRAM_HOME. VCU's current official 2020-21 schedule explicitly labels the Mar. 6, 2021 A-10 semifinal against Davidson as Home at Siegel Center. The conference/event convention creates a real designation conflict, but the target institution's explicit designation is affirmative authority. Authority: https://vcuathletics.com/sports/mens-basketball/schedule/2020-21?grid=true

### 71. DISCREPANCY-VCU-2022-23-033-GAME_DATE

- Category: discrepancy
- Matchup: saint-louis vs vcu
- Dates: source 2023-03-10; canonical 2023-03-11
- Field: game_date
- Source value: `2023-03-10`
- Canonical value: `2023-03-11`
- Evidence: saint-louis 2023-03-11: 2023-03-11
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize source to canonical Mar. 11, 2023. VCU's current official schedule places the A-10 semifinal against Saint Louis on Mar. 11.

### 72. DISCREPANCY-VCU-2022-23-034-GAME_DATE

- Category: discrepancy
- Matchup: dayton vs vcu
- Dates: source 2023-03-11; canonical 2023-03-12
- Field: game_date
- Source value: `2023-03-11`
- Canonical value: `2023-03-12`
- Evidence: dayton 2023-03-12: 2023-03-12
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize source to canonical Mar. 12, 2023. VCU's current official schedule places the A-10 championship against Dayton on Mar. 12.

### 73. DISCREPANCY-VCU-2023-24-005-GAME_DATE

- Category: discrepancy
- Matchup: iowa-state vs vcu
- Dates: source 2023-11-24; canonical 2023-11-23
- Field: game_date
- Source value: `2023-11-24`
- Canonical value: `2023-11-23`
- Evidence: iowa-state 2023-11-23: 2023-11-23
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize source to canonical Nov. 23, 2023. VCU's current official schedule places the Iowa State game on Nov. 23.

### 74. DISCREPANCY-VCU-2023-24-006-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs vcu
- Dates: source 2023-11-25; canonical 2023-11-24
- Field: game_date
- Source value: `2023-11-25`
- Canonical value: `2023-11-24`
- Evidence: boise-state 2023-11-24: 2023-11-24
- Recommended: `KEEP_CANONICAL`
- Decision: `NORMALIZE_SOURCE_TO_CANONICAL`
- Basis: Normalize source to canonical Nov. 24, 2023. VCU's current official schedule places the Boise State game on Nov. 24.

### 75. CANONICAL-SITE-PATCH-CBBG-0066496

- Category: canonical_site_patch
- Matchup: texas-a-m vs vcu
- Dates: source [unknown]; canonical 1974-12-30
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_B_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from texas-a-m; documented target HOME chronology yields 2 candidate physical venue(s): Franklin Street Gym, Richmond Coliseum. An explicit owner-reviewed site patch is required rather than a chronology guess. This review applies only if no pending target identity is approved as a match to this canonical game.
- Recommended: `REVIEW_REQUIRED`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because target identity was matched to this canonical game: VCU-1974-75-011

### 76. POSTSEASON-CLASSIFICATION-VCU-1977-78-027

- Category: postseason_classification
- Matchup: vcu vs georgetown
- Date: 1978-03-01
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `CONFERENCE_TOURNAMENT`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 1 ^at Georgetown W 88-75
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. The row is an ECAC regional/other-postseason or CBI game, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 77. POSTSEASON-CLASSIFICATION-VCU-1977-78-028

- Category: postseason_classification
- Matchup: vcu vs st-bonaventure
- Date: 1978-03-04
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 4 &vs. St. Bonaventure (:03) L 61-63
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. The row is an ECAC regional/other-postseason or CBI game, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 78. POSTSEASON-CLASSIFICATION-VCU-2009-10-032

- Category: postseason_classification
- Matchup: vcu vs george-washington
- Dates: source 2010-03-16; canonical [unknown]
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: ``
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 16 %at George Washington W 79-73
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. The row is an ECAC regional/other-postseason or CBI game, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 79. POSTSEASON-CLASSIFICATION-VCU-2009-10-033

- Category: postseason_classification
- Matchup: vcu vs charleston
- Dates: source 2010-03-22; canonical [unknown]
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: ``
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 22 %CHARLESTON W 93-86
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. The row is an ECAC regional/other-postseason or CBI game, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 80. POSTSEASON-CLASSIFICATION-VCU-2009-10-034

- Category: postseason_classification
- Matchup: vcu vs boston-university
- Dates: source 2010-03-24; canonical [unknown]
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: ``
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 24 %BOSTON UNIVERSITY W 88-75
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. The row is an ECAC regional/other-postseason or CBI game, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 81. POSTSEASON-CLASSIFICATION-VCU-2009-10-035

- Category: postseason_classification
- Matchup: vcu vs saint-louis
- Date: 2010-03-29
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 29 %SAINT LOUIS W 68-56
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. The row is an ECAC regional/other-postseason or CBI game, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 82. POSTSEASON-CLASSIFICATION-VCU-2009-10-036

- Category: postseason_classification
- Matchup: vcu vs saint-louis
- Date: 2010-03-31
- Field: game_type
- Source value: `POSTSEASON`
- Canonical value: `POSTSEASON`
- Evidence: Source type is generic POSTSEASON; institutional tournament classification and controlled NCAA round (when applicable) must be supported in this exact row's owner approval. Original source: Mar. 31 %at Saint Louis W 71-65
- Recommended: `REVIEW_REQUIRED`
- Decision: `KEEP_POSTSEASON_UNRESOLVED`
- Basis: Keep the accepted generic POSTSEASON classification unresolved in the controlled taxonomy. The row is an ECAC regional/other-postseason or CBI game, while the permanent classifier only offers NCAA_TOURNAMENT, NIT, or CONFERENCE_TOURNAMENT. Do not manufacture a false controlled class.

### 83. ACCOMPLISHMENTS-VCU

- Category: accomplishments
- Matchup: vcu
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"FINAL_FOUR","best_finish_year":"2011","conference_regular_season_championships":"14","conference_tournament_championships":"12","final_four_appearances":"1","national_championships":"0","ncaa_tournament_appearances":"21"}`
- Canonical value: `{"best_finish_key":"FINAL_FOUR","best_finish_year":2011,"final_four_appearances":1,"national_championships":0,"ncaa_tournament_appearances":20}`
- Evidence: Projected NCAA totals depend on explicit owner-reviewed classification and round decisions for generic postseason source games; the normal sealed disposable rehearsal must establish exact canonical accomplishment equality before publication or VERIFIED status.
- Recommended: `KEEP_UNDER_REVIEW`
- Decision: `VERIFY_EXPLAINED_ADMIN_DIFFERENCE`
- Basis: Verify the current VCU reference values with an explained administrative difference: 14 regular-season conference titles, 12 conference tournament titles, 21 NCAA appearances, 1 Final Four, 0 national titles, best finish Final Four in 2011. VCU calls the 2026 berth its 21st NCAA appearance; the canonical on-court total is one lower because the 2021 NCAA selection ended in an NCAA-declared no contest before a game was played. Authorities: https://vcuathletics.com/news/2026/3/15/mens-basketball-vcu-to-face-off-with-north-carolina-in-ncaa-tournament-first-round.aspx ; https://vcuathletics.com/news/2021/3/20/mens-basketball-vcu-removed-from-ncaa-tournament-as-committee-declares-game-no-contest.aspx

### 84. PUBLICATION-VCU

- Category: publication
- Matchup: vcu
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 1,650 in-scope source rows; 9 identity reviews; 28 definite and 37 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `ENABLE_PUBLIC_PAGE`
- Basis: Recommend enabling VCU publication only through the normal sealed apply, Preview, Owner Gate 2, merge, and Production-proof path after all Gate 1 decisions are approved and rehearsed.
