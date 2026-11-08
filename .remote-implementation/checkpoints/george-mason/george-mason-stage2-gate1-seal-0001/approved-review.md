# george-mason onboarding review

Generated: 2026-11-08T18:31:29.691834+00:00
Input fingerprint: `88ae854665f3c13da7f633478dcb86434dacf13974e045165b3f6e1d97de9699`
Approved plan: `0c9b26c88fc8de57642af7f5bf9f805bd2162d2b6c3a6bc26c4ebc0f00f15952`

## Preflight summary

- Source rows: 1,455
- In-scope rows: 1,455
- Pre-cutoff researched rows: 0
- Existing matches: 293
- New canonical games: 1,156
- Identity reviews: 6
- Safe enrichment fields: 543
- Discrepancies: 13
- Conditional discrepancies: 14
- Canonical-only site reviews: 0
- Affected existing public programs: auburn, baylor, boise-state, boston-college, butler, central-connecticut, cincinnati, colorado, creighton, davidson, dayton, duke, duquesne, fairleigh-dickinson, florida, fordham, fresno-state, georgetown, georgia, georgia-tech, houston, indiana, iowa, iowa-state, kansas, kansas-state, la-salle, long-island-university, louisville, loyola-chicago, lsu, marquette, maryland, miami, michigan-state, mississippi-state, nc-state, nebraska, north-carolina, northwestern, notre-dame, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, penn-state, pittsburgh, providence, rhode-island, saint-joseph-s, saint-louis, seton-hall, south-carolina, st-bonaventure, st-john-s, tcu, tennessee, ucf, ucla, uconn, usc, villanova, virginia, virginia-tech, wagner, wake-forest, washington, west-virginia

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. DISCREPANCY-GMU-1985-86-001-SCORE

- Category: discrepancy
- Matchup: george-mason vs ucf
- Date: 1985-11-23
- Field: score
- Source value: `72-58`
- Canonical value: `74-58`
- Evidence: ucf 1985-11-23: 74-58
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical 74-58. UCF's official series record lists Nov. 23, 1985 vs George Mason as a 74-58 UCF loss, corroborating the reciprocal UCF media-guide ledger and outweighing the frozen George Mason 72-58 literal. Authority: https://static.ucfknights.com/custompages/attachments1/files/34100/637856.pdf

### 2. DISCREPANCY-GMU-1986-87-010-SITE_TYPE

- Category: discrepancy
- Matchup: butler vs george-mason
- Date: 1986-12-30
- Field: site_type
- Source value: `NEUTRAL`
- Canonical value: `UNKNOWN`
- Evidence: butler 1986-12-30: UNKNOWN
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use the accepted frozen George Mason NEUTRAL classification. The immutable Research Freeze completed H/A/N research and places the Dec. 30, 1986 Butler game in Rochester, NY as neutral; the reciprocal canonical value is only UNKNOWN, so this does not contradict affirmative reciprocal site authority.

### 3. IDENTITY-GMU-1989-90-013

- Category: identity
- Matchup: george-mason vs miami
- Dates: source 1990-01-03; canonical 1990-01-01
- Field: game_identity
- Source value: `date=1990-01-03; score=91-101`
- Canonical value: `CBBG-0132290`
- Evidence: CBBG-0132290 1989-1990 1990-01-01 91-101 sources=miami
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0132290`
- Basis: One real game equals one canonical game. Match the same-season canonical candidate whose opponent and score/result orientation identify the same contest; separately adjudicate selected date/site conflicts using current institutional evidence rather than letting date parsing decide identity.

### 4. CONDITIONAL-DISCREPANCY-GMU-1989-90-013-CBBG-0132290-GAME_DATE

- Category: discrepancy
- Matchup: george-mason vs miami
- Dates: source 1990-01-03; canonical 1990-01-01
- Field: game_date
- Source value: `1990-01-03`
- Canonical value: `1990-01-01`
- Evidence: miami 1990-01-01: 1990-01-01
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical Jan. 1, 1990. Miami's official media guides/game notes identify its 101-91 overtime win at George Mason as Jan. 1, 1990, while the George Mason frozen ledger says Jan. 3. Authority: https://storage.googleapis.com/hurricanesports-com/2023/11/3b450bbd-2023-24-mbb-media-guide.pdf
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0132290`

### 5. CONDITIONAL-DISCREPANCY-GMU-1989-90-013-CBBG-0132290-SITE_TYPE

- Category: discrepancy
- Matchup: george-mason vs miami
- Dates: source 1990-01-03; canonical 1990-01-01
- Field: site_type
- Source value: `UNKNOWN`
- Canonical value: `TEAM_A_HOME`
- Evidence: miami 1990-01-01: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical George Mason home designation. Miami's official media guide describes the Jan. 1, 1990 game as 'at George Mason,' affirmatively establishing the Patriots as home; the frozen George Mason row is UNKNOWN rather than contradictory. Authority: https://storage.googleapis.com/hurricanesports-com/2023/11/3b450bbd-2023-24-mbb-media-guide.pdf
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0132290`

### 6. IDENTITY-GMU-1991-92-003

- Category: identity
- Matchup: george-mason vs virginia-tech
- Dates: source 1991-12-04; canonical 1991-11-27;1992-02-05
- Field: game_identity
- Source value: `date=1991-12-04; score=64-76`
- Canonical value: `CBBG-0136722;CBBG-0136734`
- Evidence: CBBG-0136722 1991-1992 1991-11-27 64-76 sources=virginia-tech; CBBG-0136734 1991-1992 1992-02-05 54-53 sources=virginia-tech
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0136722`
- Basis: One real game equals one canonical game. Match the same-season canonical candidate whose opponent and score/result orientation identify the same contest; separately adjudicate selected date/site conflicts using current institutional evidence rather than letting date parsing decide identity.

### 7. CONDITIONAL-DISCREPANCY-GMU-1991-92-003-CBBG-0136722-GAME_DATE

- Category: discrepancy
- Matchup: george-mason vs virginia-tech
- Dates: source 1991-12-04; canonical 1991-11-27
- Field: game_date
- Source value: `1991-12-04`
- Canonical value: `1991-11-27`
- Evidence: virginia-tech 1991-11-27: 1991-11-27
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Dec. 4, 1991. George Mason's frozen institutional ledger says Dec. 4, and Virginia Tech's current official historical schedule independently lists George Mason at Cassell Coliseum on Dec. 4, 1991, W 76-64. The older imported Virginia Tech row carrying Nov. 27 is stale. Authority: https://stats.hokiesports.com/mbasketball/records/schedule.html
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136722`

### 8. CONDITIONAL-DISCREPANCY-GMU-1991-92-003-CBBG-0136734-GAME_DATE

- Category: conditional_discrepancy
- Matchup: george-mason vs virginia-tech
- Dates: source 1991-12-04; canonical 1992-02-05
- Field: game_date
- Source value: `1991-12-04`
- Canonical value: `1992-02-05`
- Evidence: virginia-tech 1992-02-05: 1992-02-05
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136722
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136734`

### 9. CONDITIONAL-DISCREPANCY-GMU-1991-92-003-CBBG-0136734-SCORE

- Category: conditional_discrepancy
- Matchup: george-mason vs virginia-tech
- Dates: source 1991-12-04; canonical 1992-02-05
- Field: score
- Source value: `64-76`
- Canonical value: `54-53`
- Evidence: virginia-tech 1992-02-05: 54-53
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136722
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136734`

### 10. CONDITIONAL-DISCREPANCY-GMU-1991-92-003-CBBG-0136734-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: george-mason vs virginia-tech
- Dates: source 1991-12-04; canonical 1992-02-05
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: virginia-tech 1992-02-05: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136722
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136734`

### 11. CONDITIONAL-DISCREPANCY-GMU-1991-92-003-CBBG-0136734-RESULT_WINNER_TEAM_KEY

- Category: conditional_discrepancy
- Matchup: george-mason vs virginia-tech
- Dates: source 1991-12-04; canonical 1992-02-05
- Field: result_winner_team_key
- Source value: `virginia-tech`
- Canonical value: `george-mason`
- Evidence: virginia-tech 1992-02-05: george-mason
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0136722
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0136734`

### 12. IDENTITY-GMU-2004-05-006

- Category: identity
- Matchup: george-mason vs michigan-state
- Dates: source 2004-12-08; canonical 2004-12-05
- Field: game_identity
- Source value: `date=2004-12-08; score=60-66`
- Canonical value: `CBBG-0048514`
- Evidence: CBBG-0048514 2004-2005 2004-12-05 60-66 sources=michigan-state
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0048514`
- Basis: One real game equals one canonical game. Match the same-season canonical candidate whose opponent and score/result orientation identify the same contest; separately adjudicate selected date/site conflicts using current institutional evidence rather than letting date parsing decide identity.

### 13. CONDITIONAL-DISCREPANCY-GMU-2004-05-006-CBBG-0048514-GAME_DATE

- Category: discrepancy
- Matchup: george-mason vs michigan-state
- Dates: source 2004-12-08; canonical 2004-12-05
- Field: game_date
- Source value: `2004-12-08`
- Canonical value: `2004-12-05`
- Evidence: michigan-state 2004-12-05: 2004-12-05
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical Dec. 5, 2004. Michigan State's current official recap identifies the 66-60 BB&T Classic consolation victory over George Mason as Dec. 5, 2004; the frozen George Mason 12/8 date is erroneous. Authority: https://msuspartans.com/news/2004/12/5/No_11_Michigan_St_Defeats_George_Mason_66_60
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0048514`

### 14. IDENTITY-GMU-2004-05-008

- Category: identity
- Matchup: george-mason vs st-bonaventure
- Dates: source 2004-12-28; canonical 2004-12-22
- Field: game_identity
- Source value: `date=2004-12-28; score=95-58`
- Canonical value: `CBBG-0194097`
- Evidence: CBBG-0194097 2004-2005 2004-12-22 95-58 sources=st-bonaventure
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0194097`
- Basis: One real game equals one canonical game. Match the same-season canonical candidate whose opponent and score/result orientation identify the same contest; separately adjudicate selected date/site conflicts using current institutional evidence rather than letting date parsing decide identity.

### 15. CONDITIONAL-DISCREPANCY-GMU-2004-05-008-CBBG-0194097-GAME_DATE

- Category: discrepancy
- Matchup: george-mason vs st-bonaventure
- Dates: source 2004-12-28; canonical 2004-12-22
- Field: game_date
- Source value: `2004-12-28`
- Canonical value: `2004-12-22`
- Evidence: st-bonaventure 2004-12-22: 2004-12-22
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical Dec. 22, 2004. St. Bonaventure's official series preview explicitly identifies the prior meeting as Dec. 22, 2004 at the Reilly Center, George Mason 95-58; the frozen George Mason 12/28 date is erroneous. Authority: https://gobonnies.com/news/2014/2/14/2_14_2014_2060
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0194097`

### 16. IDENTITY-GMU-2005-06-002

- Category: identity
- Matchup: george-mason vs wake-forest
- Dates: source 2005-11-25; canonical 2005-11-11
- Field: game_identity
- Source value: `date=2005-11-25; score=78-83`
- Canonical value: `CBBG-0128384`
- Evidence: CBBG-0128384 2005-2006 2005-11-11 78-83 sources=wake-forest
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0128384`
- Basis: One real game equals one canonical game. Match the same-season canonical candidate whose opponent and score/result orientation identify the same contest; separately adjudicate selected date/site conflicts using current institutional evidence rather than letting date parsing decide identity.

### 17. CONDITIONAL-DISCREPANCY-GMU-2005-06-002-CBBG-0128384-GAME_DATE

- Category: discrepancy
- Matchup: george-mason vs wake-forest
- Dates: source 2005-11-25; canonical 2005-11-11
- Field: game_date
- Source value: `2005-11-25`
- Canonical value: `2005-11-11`
- Evidence: wake-forest 2005-11-11: 2005-11-11
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical Nov. 11, 2005. Wake Forest's current official game center and opponent history identify the 83-78 overtime win over George Mason as Nov. 11, 2005 in Winston-Salem; the frozen George Mason 11/25 date is erroneous. Authority: https://godeacs.com/game-center/1536
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0128384`

### 18. IDENTITY-GMU-2014-15-018

- Category: identity
- Matchup: george-mason vs davidson
- Dates: source 2015-01-24; canonical 2014-10-24;2015-02-11
- Field: game_identity
- Source value: `date=2015-01-24; score=73-80`
- Canonical value: `CBBG-0190492;CBBG-0190496`
- Evidence: CBBG-0190492 2014-2015 2014-10-24 80-73 sources=davidson; CBBG-0190496 2014-2015 2015-02-11 92-71 sources=davidson
- Recommended: `REVIEW_REQUIRED`
- Decision: `MATCH_CANONICAL:CBBG-0190492`
- Basis: One real game equals one canonical game. Match the same-season canonical candidate whose opponent and score/result orientation identify the same contest; separately adjudicate selected date/site conflicts using current institutional evidence rather than letting date parsing decide identity.

### 19. CONDITIONAL-DISCREPANCY-GMU-2014-15-018-CBBG-0190492-GAME_DATE

- Category: discrepancy
- Matchup: davidson vs george-mason
- Dates: source 2015-01-24; canonical 2014-10-24
- Field: game_date
- Source value: `2015-01-24`
- Canonical value: `2014-10-24`
- Evidence: davidson 2014-10-24: 2014-10-24
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Jan. 24, 2015. Both George Mason and Davidson current official records identify Davidson's 80-73 overtime win at George Mason as Jan. 24, 2015. The reciprocal imported Davidson row's 2014-10-24 value is a month-parsing defect in a day-only ledger line. Authorities: https://gomason.com/news/2015/1/24/209863512.aspx ; https://davidsonwildcats.com/news/2015/1/24/MBB_0124151019
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0190492`

### 20. CONDITIONAL-DISCREPANCY-GMU-2014-15-018-CBBG-0190496-GAME_DATE

- Category: conditional_discrepancy
- Matchup: davidson vs george-mason
- Dates: source 2015-01-24; canonical 2015-02-11
- Field: game_date
- Source value: `2015-01-24`
- Canonical value: `2015-02-11`
- Evidence: davidson 2015-02-11: 2015-02-11
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0190492
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0190496`

### 21. CONDITIONAL-DISCREPANCY-GMU-2014-15-018-CBBG-0190496-SCORE

- Category: conditional_discrepancy
- Matchup: davidson vs george-mason
- Dates: source 2015-01-24; canonical 2015-02-11
- Field: score
- Source value: `80-73`
- Canonical value: `92-71`
- Evidence: davidson 2015-02-11: 92-71
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0190492
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0190496`

### 22. CONDITIONAL-DISCREPANCY-GMU-2014-15-018-CBBG-0190496-SITE_TYPE

- Category: conditional_discrepancy
- Matchup: davidson vs george-mason
- Dates: source 2015-01-24; canonical 2015-02-11
- Field: site_type
- Source value: `TEAM_B_HOME`
- Canonical value: `TEAM_A_HOME`
- Evidence: davidson 2015-02-11: TEAM_A_HOME
- Recommended: `KEEP_CANONICAL`
- Decision: `NOT_APPLICABLE`
- Basis: Not applicable because the sealed identity decision was MATCH_CANONICAL:CBBG-0190492
- Applies if identity decision: `MATCH_CANONICAL:CBBG-0190496`

### 23. DISCREPANCY-GMU-2016-17-024-SCORE

- Category: discrepancy
- Matchup: davidson vs george-mason
- Date: 2017-02-08
- Field: score
- Source value: `67-76`
- Canonical value: `69-76`
- Evidence: davidson 2017-02-08: 69-76
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical 76-69. Both current George Mason and Davidson official recaps/box scores give the Feb. 8, 2017 final as George Mason 76, Davidson 69; the frozen George Mason 76-67 literal is erroneous. Authority: https://gomason.com/news/2017/2/8/mens-basketball-mason-closes-out-76-69-win-at-davidson.aspx

### 24. DISCREPANCY-GMU-2016-17-032-SCORE

- Category: discrepancy
- Matchup: fordham vs george-mason
- Date: 2017-03-09
- Field: score
- Source value: `71-82`
- Canonical value: `71-81`
- Evidence: fordham 2017-03-09: 71-81
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source 82-71. Current George Mason and Fordham official box scores both show George Mason's Mar. 9, 2017 overtime win as 82-71; the canonical 81-71 value omits Mason's final made free throw. Authorities: https://gomason.com/sports/mens-basketball/stats/2016-17/fordham/boxscore/8104 ; https://fordhamsports.com/sports/mens-basketball/stats/2016-17/george-mason-university/boxscore/6155

### 25. DISCREPANCY-GMU-2019-20-006-GAME_DATE

- Category: discrepancy
- Matchup: george-mason vs maryland
- Dates: source 2019-11-22; canonical 2019-11-23
- Field: game_date
- Source value: `2019-11-22`
- Canonical value: `2019-11-23`
- Evidence: maryland 2019-11-23: 2019-11-23
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Nov. 22, 2019. Current Maryland opponent history/game notes and George Mason's official box score all identify Maryland's 86-63 home win over Mason as Friday Nov. 22, 2019; the imported Maryland row's Nov. 23 value is stale. Authorities: https://umterps.com/sports/mens-basketball/opponent-history/george-mason-university/88 ; https://gomason.com/sports/mens-basketball/stats/2019-20/maryland/boxscore/10495

### 26. DISCREPANCY-GMU-2020-21-011-GAME_DATE

- Category: discrepancy
- Matchup: george-mason vs la-salle
- Dates: source 2021-01-13; canonical 2021-01-12
- Field: game_date
- Source value: `2021-01-13`
- Canonical value: `2021-01-12`
- Evidence: la-salle 2021-01-12: 2021-01-12
- Recommended: `KEEP_CANONICAL`
- Decision: `USE_SOURCE`
- Basis: Use source Jan. 13, 2021. Current La Salle schedule/opponent history and George Mason's official recap/box score all identify the 75-42 game in Fairfax as Wednesday Jan. 13, 2021; the imported La Salle row's Jan. 12 value is stale. Authorities: https://goexplorers.com/sports/mens-basketball/schedule/2020-21?grid=true ; https://gomason.com/sports/mens-basketball/stats/2020-21/la-salle/boxscore/10896

### 27. ACCOMPLISHMENTS-GEORGE-MASON

- Category: accomplishments
- Matchup: george-mason
- Date: [unknown]
- Field: program_accomplishments
- Source value: `{"best_finish_key":"FINAL_FOUR","best_finish_year":"2006","conference_regular_season_championships":"5","conference_tournament_championships":"4","final_four_appearances":"1","national_championships":"0","ncaa_tournament_appearances":"6"}`
- Canonical value: `{"best_finish_key":"FINAL_FOUR","best_finish_year":2006,"final_four_appearances":1,"national_championships":0,"ncaa_tournament_appearances":6}`
- Evidence: Canonical NCAA fields match; conference titles still require authoritative source verification.
- Recommended: `VERIFY_REFERENCE_VALUES`
- Decision: `VERIFY_REFERENCE_VALUES`
- Basis: Verify the existing George Mason reference values unchanged: 5 conference regular-season championships (four CAA plus the 2025 A-10 share), 4 conference tournament championships, 6 NCAA appearances, 1 Final Four, 0 national titles, best finish FINAL_FOUR in 2006. George Mason's official materials confirm six NCAA appearances and the 2006 Final Four; the 2011 CAA regular-season title; the 2025 A-10 title as the first regular-season title since 2011; and that entering 2012 Mason was seeking its fifth CAA tournament championship, establishing four prior tournament titles. The existing reference therefore remains historically consistent and Stage 2 reports no canonical NCAA conflict. Authorities include https://gomason.com/news/2011/4/22/205141320.aspx ; https://gomason.com/news/2025/3/8/mens-basketball-champs-patriots-win-first-ever-a-10-regular-season-title-with-win-at-richmond.aspx ; https://static.gomason.com/custompages/pdf/1112-mbb-infoguide.pdf

### 28. PUBLICATION-GEORGE-MASON

- Category: publication
- Matchup: george-mason
- Date: [unknown]
- Field: public_page_enabled
- Source value: `No`
- Canonical value: `Yes`
- Evidence: 1,455 in-scope source rows; 6 identity reviews; 6 definite and 14 conditional discrepancies.
- Recommended: `ENABLE_PUBLIC_PAGE`
- Decision: `ENABLE_PUBLIC_PAGE`
- Basis: Enable George Mason publication only through the normal Owner Gate 1, sealed apply, Preview, explicit Owner Gate 2, merge and Production-proof workflow after every approved decision and automated gate passes.
