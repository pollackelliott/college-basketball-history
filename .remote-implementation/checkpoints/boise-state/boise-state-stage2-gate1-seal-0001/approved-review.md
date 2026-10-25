# boise-state onboarding review

Generated: 2026-10-25T20:42:55.016189+00:00
Input fingerprint: `115d32f6226ed367be0ea192c1cffdb175983958f1c0a376b5fd5c770811af77`
Approved plan: `b76b1e2c5e5e1969fb59890ad68805f93a015a822d01ae7eee6d388d6b483db3`

## Preflight summary

- Source rows: 1,670
- In-scope rows: 1,670
- Pre-cutoff researched rows: 0
- Existing matches: 136
- New canonical games: 1,534
- Identity reviews: 0
- Safe enrichment fields: 182
- Discrepancies: 5
- Conditional discrepancies: 0
- Canonical-only site reviews: 0
- Affected existing public programs: arizona, arizona-state, arkansas, boston-college, butler, byu, chicago-state, cincinnati, clemson, colorado, creighton, georgia-tech, houston, illinois, indiana, iowa, iowa-state, kansas, kentucky, louisville, lsu, marquette, michigan, michigan-state, mississippi-state, nc-state, nebraska, northwestern, oklahoma-state, ole-miss, oregon, oregon-state, rutgers, smu, south-carolina, stanford, tcu, texas-a-m, ucla, usc, utah, vanderbilt, virginia-tech, washington, washington-state, wisconsin

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. DISCREPANCY-BOI-S1-198485-004-SCORE

- Category: discrepancy
- Matchup: boise-state vs chicago-state
- Date: 1984-12-08
- Field: score
- Source value: `59-74`
- Canonical value: `81-61`
- Evidence: chicago-state 1984-12-08: 81-61
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Chicago State's accepted institutional media-guide reciprocal record identifies the 1984-12-08 game at Boise State as a 61-81 Chicago State loss, matching canonical Boise State 81-61. Independent season records also align with 81-61. Boise State's conflicting 59-74 record-book line remains preserved as source evidence.

### 2. DISCREPANCY-BOI-S1-198485-004-RESULT_WINNER_TEAM_KEY

- Category: discrepancy
- Matchup: boise-state vs chicago-state
- Date: 1984-12-08
- Field: result_winner_team_key
- Source value: `chicago-state`
- Canonical value: `boise-state`
- Evidence: chicago-state 1984-12-08: boise-state
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Chicago State's accepted institutional media-guide reciprocal record identifies Boise State as the 1984-12-08 winner, 81-61; independent season records agree. Retain canonical Boise State as winner while preserving Boise State's contrary frozen source assertion.

### 3. DISCREPANCY-BOI-S1-199697-007-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs oregon
- Dates: source 1996-12-19; canonical 1996-12-20
- Field: game_date
- Source value: `1996-12-19`
- Canonical value: `1996-12-20`
- Evidence: oregon 1996-12-20: 1996-12-20
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Oregon's official 1996-97 schedule and opponent history both date the 61-58 road win at Boise State to Friday, 1996-12-20; Oregon's later institutional recap repeats Dec. 20 and contemporary Associated Press reporting describes the game as Friday night. Retain canonical 1996-12-20 and preserve Boise State's 1996-12-19 source date.

### 4. DISCREPANCY-BOI-S1-199899-006-GAME_DATE

- Category: discrepancy
- Matchup: boise-state vs washington
- Dates: source 1998-12-04; canonical 1998-12-05
- Field: game_date
- Source value: `1998-12-04`
- Canonical value: `1998-12-05`
- Evidence: washington 1998-12-05: 1998-12-05
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Washington's contemporary institutional preview published 1998-12-04 explicitly schedules the Boise State game for Saturday, 1998-12-05, and subsequent Washington institutional recaps identify the 69-61 loss at Boise State as Dec. 5. Retain canonical 1998-12-05 and preserve Boise State's conflicting 1998-12-04 source date.

### 5. DISCREPANCY-BOI-S1-201920-002-SCORE

- Category: discrepancy
- Matchup: boise-state vs oregon
- Date: 2019-11-09
- Field: score
- Source value: `75-106`
- Canonical value: `65-106`
- Evidence: oregon 2019-11-09: 65-106
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Oregon's official 2019-20 opponent history, game recap, schedule, and cumulative statistics all identify Oregon's 2019-11-09 home win over Boise State as 106-75. Boise State's frozen source value 75-106 is therefore supported; replace the stale canonical 65-106 score while preserving all literal source evidence.

### 6. ACCOMPLISHMENTS-BOISE-STATE

- Category: accomplishments
- Matchup: boise-state
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"ROUND_OF_32","best_finish_year":"1976","conference_regular_season_championships":"7","conference_tournament_championships":"6","final_four_appearances":"0","national_championships":"0","ncaa_tournament_appearances":"10"}`
- Canonical value: `{"best_finish_key":"ROUND_OF_32","best_finish_year":1976,"final_four_appearances":0,"national_championships":0,"ncaa_tournament_appearances":10}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `VERIFY_REFERENCE_VALUES`
- Basis: Boise State's official 2025-26 game notes list 7 regular-season conference championships, 6 conference-tournament championships, and 10 NCAA Tournament appearances; the official 2022 NCAA-selection release confirms the 2022 Mountain West tournament title as the program's sixth conference-tournament automatic-bid championship. The existing reference values (7, 6, 10, 0 Final Fours, 0 national titles, ROUND_OF_32 best finish in 1976) require no patch. Sources: https://broncosports.com/documents/download/2026/1/6/20260107_GrandCanyon.pdf ; https://broncosports.com/news/2022/3/13/mbb-earns-highest-ncaa-tournament-seed-in-program-history

### 7. PUBLICATION-BOISE-STATE

- Category: publication
- Matchup: boise-state
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 1,670 in-scope source rows; 0 identity reviews; 5 definite and 0 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `ENABLE_PUBLIC_PAGE`
- Basis: Enable Boise State's public page only after the exact approved seven-decision Gate 1 packet, including the supported 2019 Oregon score correction, survives permanent pre-seal rehearsal, cryptographic sealing, transactional apply, and all publication/release gates.
