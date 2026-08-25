# Nebraska source notes and provenance

## Primary sources

1. **Nebraska 2025-26 men's basketball media guide** (owner supplied). The year-by-year historical ledger is the primary game source through 2024-25; conference/postseason/home-court sections provide supporting context.
2. **Nebraska Athletics official 2025-26 schedule**: https://huskers.com/sports/mens-basketball/schedule/season/2025-26
   - Supplies 35 competitive games and a 28-7 record: 18 home, 10 away, 7 neutral.
   - BYU and Midland are noncompetitive preseason games and are excluded.
   - Supplies the 2026 Big Ten Tournament and three NCAA Tournament games.
3. **Owner-supplied `Conference_Tournament_Site_Reference(9).xlsm`**. It is incomplete as universal canon, but the owner explicitly authorized its completed Nebraska-relevant Big Eight, Big 12, and Big Ten sections for this portfolio only.

The conference workbook supplies physical shared venue/city/state and historical site boundaries; it does not independently infer H/A/N. Campus preliminary rounds are not replaced by later centralized shared sites.

## H/A/N evidence and cross-checks

The media-guide ledger is the primary H/A/N source. `H` is Nebraska home; `N`, `KC`, `NY`, `N*`, and `N^` are neutral evidence; `A` is opponent home unless explicit game-level evidence establishes otherwise.

Recent cross-checks:
- 2017 Big Ten Tournament vs. Penn State: https://huskers.com/news/2017/03/7/huskers-face-penn-state-in-big-ten-tourney
- 2023-24 official schedule / 2024 Big Ten Tournament: https://huskers.com/sports/mens-basketball/schedule/season/2023-24
- 2024 Illinois Big Ten semifinal box score: https://huskers.com/boxscore/22250
- 2024 Indiana Big Ten quarterfinal box score: https://huskers.com/boxscore/22210
- 2024 NCAA first round vs. Texas A&M: https://huskers.com/news/2024/03/22/huskers-season-comes-to-an-end-in-ncaa-first-round

### 1978 Oklahoma State correction

Nebraska's ledger marks the game neutral. Oklahoma State's official box-score archive identifies it at the NU Sports Complex in Lincoln:
https://okstate.com/documents/download/2023/1/5/Boxscores_1977-78_Part26.pdf

That reciprocal official evidence controls curated H/A/N while Nebraska's raw marker remains preserved.

## NCAA physical-site research

Representative supporting sources:
- 1986 Nebraska-Western Kentucky, Charlotte: https://huskers.com/boxscore/6093
- 1986 Charlotte Coliseum contemporary cross-check: https://www.sports-reference.com/cbb/schools/western-kentucky/men/1986-schedule.html
- 1991 Xavier-Nebraska at Hubert H. Humphrey Metrodome: https://goxavier.com/documents/download/2016/11/3/117_172_records.pdf
- 1992 Nebraska-Connecticut: https://huskers.com/boxscore/6281
- 2014 Nebraska-Baylor at AT&T Center: https://baylorbears.com/documents/download/2014/3/25/_bay_m_baskbl_2013_14_misc_non_event__MBB-Postseason-Guide-14.pdf
- 2024 Nebraska-Texas A&M at FedExForum: https://huskers.com/news/2024/03/22/huskers-season-comes-to-an-end-in-ncaa-first-round

Physical-building names are normalized rather than split solely because of naming-rights changes. Historical source names remain aliases/provenance.

## 1994 Big Eight championship score

Nebraska's year-by-year ledger says Nebraska 77, Oklahoma State 68. Nebraska's official historical schedule independently confirms 77-68:
https://huskers.com/sports/mens-basketball/schedule/season/1993-94

The dedicated media-guide conference-tournament table's 77-66 line is documented as a source-internal discrepancy.

## Opponent normalization

Every exact source opponent label resolves through `opponents.csv`; unresolved opponents are zero. Important lineage normalizations include Alabama-Birmingham -> UAB, Arkansas-Little Rock -> Little Rock, Detroit -> Detroit Mercy, IPFW -> Purdue Fort Wayne, Loyola (Ill.) -> Loyola Chicago, Memphis State -> Memphis, Nebraska-Omaha -> Omaha, Nevada-Reno -> Nevada, Northeast Louisiana -> UL Monroe, SW Missouri State -> Missouri State, SW Texas State -> Texas State, Texas-Pan American -> UT Rio Grande Valley, UMKC -> Kansas City, and Southern California -> USC.

`Southeastern` (2018-11-11) is normalized to Southeastern Louisiana, cross-checked against Nebraska's official 2018-19 schedule:
https://huskers.com/sports/mens-basketball/schedule/season/2018-19

Historical clubs, military teams, high schools, reserve teams, and non-current college programs remain separate non-D1 identities rather than being forced into modern Division I programs.

## Result and taxonomy policy

Scores and W/L values represent on-court truth. No game is removed or rewritten for later administrative treatment without explicit game-level evidence. Regular-season invitationals remain `REGULAR_SEASON`. The 1909 Missouri Valley championship playoff, 1949 title/qualifying playoffs, and 2025 College Basketball Crown use generic `POSTSEASON` because they are real postseason games not properly classified as the annual conference tournament, NCAA Tournament, or NIT.
