# san-diego-state onboarding review

Generated: 2026-10-30T02:28:36.775047+00:00
Input fingerprint: `36b1eb82a636637323883847cdd06f89fb78b64e43abcd3ffcb08fb7fcb36095`
Approved plan: `bc5d82586fe8cd5e0f097d66bd90beca15d21a446d518dad5da2167f2f06de38`

## Preflight summary

- Source rows: 1,709
- In-scope rows: 1,709
- Pre-cutoff researched rows: 0
- Existing matches: 630
- New canonical games: 1,077
- Identity reviews: 2
- Safe enrichment fields: 1,320
- Discrepancies: 24
- Conditional discrepancies: 6
- Canonical-only site reviews: 0
- Affected existing public programs: alabama, arizona, arizona-state, arkansas, baylor, boise-state, byu, california, central-connecticut, chicago-state, cincinnati, colorado, colorado-state, creighton, depaul, duke, florida, florida-state, fresno-state, georgetown, georgia, georgia-tech, gonzaga, houston, illinois, indiana, iowa, iowa-state, kansas, kansas-state, long-island-university, marquette, miami, michigan, michigan-state, missouri, nc-state, nebraska, north-carolina, northwestern, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, pittsburgh, providence, purdue, smu, south-carolina, st-john-s, stanford, syracuse, tcu, tennessee, texas, texas-tech, ucla, uconn, usc, utah, utah-state, villanova, virginia, washington, washington-state, west-virginia, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. IDENTITY-SDSU-S1-000017

- Category: identity
- Matchup: san-diego-state vs fresno-state
- Dates: source 1971-01-30; canonical 1971-02-06;1971-02-13
- Field: game_identity
- Source value: `date=1971-01-30; score=96-97`
- Canonical value: `CBBG-0179159;CBBG-0179163`
- Evidence: CBBG-0179159 1970-1971 1971-02-06 97-96 sources=fresno-state; CBBG-0179163 1970-1971 1971-02-13 95-106 sources=fresno-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0179159`
- Basis: Fresno State's current official record book lists a 1971-01-30 Fresno State 97-96 home win over San Diego State and a separate 1971-02-13 San Diego State 106-95 win. The target row is the reciprocal 96-97 road loss, so it is the same one real game as CBBG-0179159; CBBG-0179163 is the separate Feb. 13 game.

### 2. CONDITIONAL-DISCREPANCY-SDSU-S1-000017-CBBG-0179159-GAME_DATE

- Category: discrepancy
- Matchup: fresno-state vs san-diego-state
- Dates: source 1971-01-30; canonical 1971-02-06
- Field: game_date
- Source value: `1971-01-30`
- Canonical value: `1971-02-06`
- Evidence: fresno-state 1971-02-06: 1971-02-06
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fresno State institutional history dates the matched 97-96 Fresno home win to 1971-01-30, matching the accepted SDSU source and disproving canonical 1971-02-06. Use the accepted target-source date after matching CBBG-0179159.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0179159`

### 3. CONDITIONAL-DISCREPANCY-SDSU-S1-000017-CBBG-0179163-GAME_DATE

- Category: conditional_discrepancy
- Matchup: fresno-state vs san-diego-state
- Dates: source 1971-01-30; canonical 1971-02-13
- Field: game_date
- Source value: `1971-01-30`
- Canonical value: `1971-02-13`
- Evidence: fresno-state 1971-02-13: 1971-02-13
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0179159
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0179163`

### 4. CONDITIONAL-DISCREPANCY-SDSU-S1-000017-CBBG-0179163-SCORE

- Category: conditional_discrepancy
- Matchup: fresno-state vs san-diego-state
- Dates: source 1971-01-30; canonical 1971-02-13
- Field: score
- Source value: `97-96`
- Canonical value: `95-106`
- Evidence: fresno-state 1971-02-13: 95-106
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0179159
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0179163`

### 5. CONDITIONAL-DISCREPANCY-SDSU-S1-000017-CBBG-0179163-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: fresno-state vs san-diego-state
- Dates: source 1971-01-30; canonical 1971-02-13
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: fresno-state 1971-02-13: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0179159
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0179163`

### 6. CONDITIONAL-DISCREPANCY-SDSU-S1-000017-CBBG-0179163-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: fresno-state vs san-diego-state
- Dates: source 1971-01-30; canonical 1971-02-13
- Field: result_winner_team_key
- Source value: `fresno-state`
- Canonical value: `san-diego-state`
- Evidence: fresno-state 1971-02-13: san-diego-state
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0179159
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0179163`

### 7. DISCREPANCY-SDSU-S1-000060-GAME_DATE

- Category: discrepancy
- Matchup: depaul vs san-diego-state
- Dates: source 1972-12-19; canonical 1972-12-20
- Field: game_date
- Source value: `1972-12-19`
- Canonical value: `1972-12-20`
- Evidence: depaul 1972-12-20: 1972-12-20
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: DePaul's current official year-by-year results date the 89-75 home win over San Diego State to 1972-12-20. Retain the canonical date; the SDSU 12/19 source notation remains preserved as source evidence.

### 8. DISCREPANCY-SDSU-S1-000068-SCORE

- Category: discrepancy
- Matchup: creighton vs san-diego-state
- Date: 1973-01-18
- Field: score
- Source value: `68-73`
- Canonical value: `61-73`
- Evidence: creighton 1973-01-18: 61-73
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Creighton's accepted institutional reciprocal row records a 73-61 San Diego State win on 1973-01-18, supporting canonical 61-73 in Creighton-oriented ordering rather than the SDSU source's 73-68.

### 9. DISCREPANCY-SDSU-S1-000083-SCORE

- Category: discrepancy
- Matchup: arizona vs san-diego-state
- Date: 1973-12-11
- Field: score
- Source value: `109-79`
- Canonical value: `101-79`
- Evidence: arizona 1973-12-11: 101-79
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Arizona's accepted institutional reciprocal row records a 101-79 Arizona home win on 1973-12-11, supporting canonical 101-79 rather than the SDSU source's 109-79.

### 10. DISCREPANCY-SDSU-S1-000132-GAME_DATE

- Category: discrepancy
- Matchup: fresno-state vs san-diego-state
- Dates: source 1975-03-02; canonical 1975-03-01
- Field: game_date
- Source value: `1975-03-02`
- Canonical value: `1975-03-01`
- Evidence: fresno-state 1975-03-01: 1975-03-01
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Fresno State's current official record book dates its 68-64 home win over San Diego State to 1975-03-02, matching the accepted SDSU source and disproving canonical 1975-03-01.

### 11. DISCREPANCY-SDSU-S1-000146-SCORE

- Category: discrepancy
- Matchup: iowa-state vs san-diego-state
- Date: 1976-01-08
- Field: score
- Source value: `78-92`
- Canonical value: `75-92`
- Evidence: iowa-state 1976-01-08: 75-92
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Iowa State's accepted institutional reciprocal row records a 92-75 San Diego State home win on 1976-01-08, supporting canonical 75-92 in Iowa State-oriented ordering rather than the SDSU source's 92-78.

### 12. DISCREPANCY-SDSU-S1-000169-SCORE

- Category: discrepancy
- Matchup: boise-state vs san-diego-state
- Date: 1976-12-16
- Field: score
- Source value: `68-78`
- Canonical value: `68-79`
- Evidence: boise-state 1976-12-16: 68-79
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: The accepted SDSU source records 78-68, and Boise State's own institutional series notes also identify the 1976-12-16 game as San Diego State 78-68. This independent reciprocal authority outweighs the current Boise package's 79-68 transcription; use the SDSU source score.

### 13. DISCREPANCY-SDSU-S1-000227-SITE_TYPE

- Category: discrepancy
- Matchup: san-diego-state vs stanford
- Dates: source 1978-12-29; canonical [unknown]
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: stanford [unknown]: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Stanford's accepted reciprocal Research row classifies the 1978-12-29 Cabrillo Classic game in San Diego as NEUTRAL after reconciling the event footnote and Stanford season H/A/N totals. A separate Stanford series table labels the game away, but the accepted event/season accounting is the stronger already-adjudicated project authority; retain canonical NEUTRAL.

### 14. DISCREPANCY-SDSU-S1-000239-GAME_DATE

- Category: discrepancy
- Matchup: colorado-state vs san-diego-state
- Dates: source 1979-02-09; canonical 1979-02-08
- Field: game_date
- Source value: `1979-02-09`
- Canonical value: `1979-02-08`
- Evidence: colorado-state 1979-02-08: 1979-02-08
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Colorado State's institutional series notes date the 83-90 road loss at San Diego State to 1979-02-08. Retain canonical 1979-02-08 rather than the SDSU source's 02/09 notation.

### 15. DISCREPANCY-SDSU-S1-000453-SITE_TYPE

- Category: discrepancy
- Matchup: ole-miss vs san-diego-state
- Date: 1986-12-28
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: ole-miss 1986-12-28: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Ole Miss institutional opponent history classifies the 1986-12-28 88-77 win over San Diego State in San Diego as a neutral-site game. Retain canonical NEUTRAL rather than treating the San Diego venue as SDSU home solely from geography.

### 16. DISCREPANCY-SDSU-S1-000532-GAME_DATE

- Category: discrepancy
- Matchup: san-diego-state vs utah
- Dates: source 1989-03-09; canonical 1989-03-08
- Field: game_date
- Source value: `1989-03-09`
- Canonical value: `1989-03-08`
- Evidence: utah 1989-03-08: 1989-03-08
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Utah's accepted institutional reciprocal row dates the conference-tournament 70-57 win over San Diego State to 1989-03-08. Retain canonical 1989-03-08 rather than the SDSU source's 03/09 notation.

### 17. DISCREPANCY-SDSU-S1-000544-SITE_TYPE

- Category: discrepancy
- Matchup: san-diego-state vs villanova
- Date: 1989-12-28
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `UNKNOWN`
- Evidence: villanova 1989-12-28: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: SDSU institutional history describes Villanova's 57-52 win as the final of the Texaco Star Classic at the San Diego Sports Arena, and the accepted SDSU source places it at SDSU's home arena. The reciprocal Villanova package is UNKNOWN rather than contradictory authority. Use SDSU SOURCE_PROGRAM_HOME.

### 18. DISCREPANCY-SDSU-S1-000776-SITE_TYPE

- Category: discrepancy
- Matchup: san-diego-state vs tcu
- Date: 1998-01-17
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `TEAM_B_HOME`
- Evidence: tcu 1998-01-17: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: TCU institutional series history places its 105-61 win on 1998-01-17 in Fort Worth. For the canonical san-diego-state vs tcu ordering this is TEAM_B_HOME, so retain canonical.

### 19. DISCREPANCY-SDSU-S1-000783-SITE_TYPE

- Category: discrepancy
- Matchup: san-diego-state vs tcu
- Date: 1998-02-14
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: tcu 1998-02-14: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: TCU institutional series history places its 91-69 win on 1998-02-14 in San Diego. For the canonical san-diego-state vs tcu ordering this is TEAM_A_HOME, so retain canonical.

### 20. DISCREPANCY-SDSU-S1-000819-SITE_TYPE

- Category: discrepancy
- Matchup: oklahoma-state vs san-diego-state
- Date: 1999-12-12
- Field: site_type
- Source value: `TEAM_A_HOME`
- Canonical value: `NEUTRAL`
- Evidence: oklahoma-state 1999-12-12: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Oklahoma State institutional contemporaneous coverage identifies the 1999-12-12 97-63 win over San Diego State as an Oklahoma State home game played at the Myriad Center in Oklahoma City. Use the SDSU opponent-home classification; preserve Oklahoma City, OK as the supported historical locality without requiring bespoke building archaeology.

### 21. DISCREPANCY-SDSU-S1-000991-SCORE

- Category: discrepancy
- Matchup: san-diego-state vs utah
- Date: 2005-03-05
- Field: score
- Source value: `67-77`
- Canonical value: `60-72`
- Evidence: utah 2005-03-05: 60-72
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Utah's official recap and institutional game record show a 72-60 Utah win over San Diego State on 2005-03-05. Retain canonical 60-72 in San Diego State-oriented ordering rather than the SDSU source's 67-77.

### 22. DISCREPANCY-SDSU-S1-001036-SCORE

- Category: discrepancy
- Matchup: arizona vs san-diego-state
- Date: 2006-12-09
- Field: score
- Source value: `69-48`
- Canonical value: `68-49`
- Evidence: arizona 2006-12-09: 68-49
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: The accepted SDSU source records Arizona 69-48, and current Arizona institutional opponent/schedule evidence supports that final. Use the SDSU source score rather than the stale reciprocal/canonical 68-49 value.

### 23. DISCREPANCY-SDSU-S1-001039-SITE_TYPE

- Category: discrepancy
- Matchup: san-diego-state vs washington-state
- Date: 2006-12-21
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `NEUTRAL`
- Evidence: washington-state 2006-12-21: NEUTRAL
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Washington State institutional history labels the 2006-12-21 64-54 Seattle win as a WSU home game and later explicitly states that the 2017 meeting was the first official neutral-site game despite prior WSU home games at Spokane and Seattle. Use WSU home and preserve the already-registered KeyArena/Seattle site metadata.

### 24. DISCREPANCY-SDSU-S1-001234-SITE_TYPE

- Category: discrepancy
- Matchup: san-diego-state vs syracuse
- Date: 2012-11-11
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_A_HOME`
- Evidence: syracuse 2012-11-11: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Syracuse institutional schedule/recap treats the 2012-11-11 Battle on the Midway game as an away game at San Diego State. The USS Midway location does not itself make the game neutral, and SDSU season accounting is consistent with this being its lone home loss. Retain canonical SDSU home.

### 25. DISCREPANCY-SDSU-S1-001385-SCORE

- Category: discrepancy
- Matchup: arizona-state vs san-diego-state
- Date: 2016-12-10
- Field: score
- Source value: `74-63`
- Canonical value: `74-67`
- Evidence: arizona-state 2016-12-10: 74-67
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Arizona State's official recap records a 74-63 road win at San Diego State on 2016-12-10. Use the accepted SDSU source score 63-74 rather than canonical 67-74.

### 26. DISCREPANCY-SDSU-S1-001392-SCORE

- Category: discrepancy
- Matchup: boise-state vs san-diego-state
- Date: 2017-01-07
- Field: score
- Source value: `78-68`
- Canonical value: `78-66`
- Evidence: boise-state 2017-01-07: 78-66
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Boise State's official recap records a 78-66 home win over San Diego State on 2017-01-07. Retain canonical 78-66 rather than the SDSU source's 78-68.

### 27. IDENTITY-SDSU-S1-001423

- Category: identity
- Matchup: san-diego-state vs utah-state
- Dates: source 2017-12-30; canonical 2017-12-20
- Field: game_identity
- Source value: `date=2017-12-30; score=79-59`
- Canonical value: `CBBG-0176965`
- Evidence: CBBG-0176965 2017-2018 2017-12-20 79-59 sources=utah-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0176965`
- Basis: SDSU and Utah State institutional records both identify one 2017-18 game with this 79-59 score at San Diego State; the accepted SDSU date is 2017-12-30. The unique season/opponent/score/site match is CBBG-0176965, whose current 2017-12-20 date is stale.

### 28. CONDITIONAL-DISCREPANCY-SDSU-S1-001423-CBBG-0176965-GAME_DATE

- Category: discrepancy
- Matchup: san-diego-state vs utah-state
- Dates: source 2017-12-30; canonical 2017-12-20
- Field: game_date
- Source value: `2017-12-30`
- Canonical value: `2017-12-20`
- Evidence: utah-state 2017-12-20: 2017-12-20
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: SDSU institutional schedule/recap and Utah State institutional series evidence date the matched 79-59 San Diego State home win to 2017-12-30. Use the accepted target-source date after matching CBBG-0176965.
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0176965`

### 29. DISCREPANCY-SDSU-S1-001536-SCORE

- Category: discrepancy
- Matchup: san-diego-state vs utah-state
- Date: 2021-03-13
- Field: score
- Source value: `77-70`
- Canonical value: `68-57`
- Evidence: utah-state 2021-03-13: 68-57
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: SDSU's official 2021 media central identifies the 2021-03-13 Mountain West Championship as San Diego State 68-57 Utah State; 77-70 was the prior day's semifinal score against Nevada. Retain canonical 68-57.

### 30. DISCREPANCY-SDSU-S1-001613-SITE_TYPE

- Category: discrepancy
- Matchup: san-diego-state vs washington
- Date: 2023-11-19
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `TEAM_B_HOME`
- Evidence: washington 2023-11-19: TEAM_B_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Washington institutional coverage identifies the 2023-11-19 100-97 overtime loss to San Diego State as the Continental Tire Main Event championship in Las Vegas, and SDSU's event announcement places the event at T-Mobile Arena. Use target NEUTRAL, but correct the target source's inherited Hec Edmundson/Seattle venue metadata to T-Mobile Arena, Las Vegas.

### 31. ACCOMPLISHMENTS-SAN-DIEGO-STATE

- Category: accomplishments
- Matchup: san-diego-state
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"NATIONAL_RUNNER_UP","best_finish_year":"2023","conference_regular_season_championships":"11","conference_tournament_championships":"9","final_four_appearances":"1","national_championships":"0","ncaa_tournament_appearances":"17"}`
- Canonical value: `{"best_finish_key":"NATIONAL_RUNNER_UP","best_finish_year":2023,"final_four_appearances":1,"national_championships":0,"ncaa_tournament_appearances":17}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `VERIFY_REFERENCE_VALUES`
- Basis: SDSU institutional history establishes two pre-Mountain-West Division I regular-season conference titles (PCAA shares in 1977 and 1978), two pre-MW conference tournament titles (PCAA 1976 and WAC 1985), and nine Mountain West regular-season plus seven Mountain West tournament titles through the completed 2025-26 season. The in-scope totals are therefore 11 regular-season and 9 tournament championships; the existing NCAA/Final Four/runner-up fields already match.

### 32. PUBLICATION-SAN-DIEGO-STATE

- Category: publication
- Matchup: san-diego-state
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 1,709 in-scope source rows; 2 identity reviews; 22 definite and 6 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `ENABLE_PUBLIC_PAGE`
- Basis: Recommend enabling the page only through the sealed onboarding workflow after the complete 32-decision map passes the exact proposal rehearsal, explicit Owner Gate 1, sealed apply, verification, Preview, explicit Gate 2, merge, and Production proof.
