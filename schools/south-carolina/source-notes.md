# South Carolina source notes

## Source hierarchy

1. **South Carolina 2025-26 Records & History / men's basketball media guide** — owner upload `S Carolina .pdf`. This is the primary authority for the historical game universe, year-by-year rows, source H/A/N notation, played results, scores, overtime, NCAA/NIT history, conference context, and homecourt chronology.
2. **Conference Tournament Site Reference** — owner upload `Conference_Tournament_Site_Reference (2).xlsm`. The workbook was audited against South Carolina's actual conference/tournament path. Only South Carolina-relevant rows are relied upon; unfinished unrelated workbook sections are not promoted into project-wide canon.
3. **Official South Carolina Athletics pages and reciprocal institutional sources** are used to supplement completed 2025-26, resolve physical venues, recover source defects where defensible, and cross-check source-internal inconsistencies.
4. **NCAA archival site records** control NCAA Tournament physical-site completion where required.

Raw South Carolina source wording remains in `raw_text`. Structured corrections or enrichments are documented rather than silently replacing the source record.

## Coverage and extraction reproducibility

The final package contains **2,895 competitive games** from 1908-09 through completed 2025-26 and represents an on-court record of **1,530-1,364-1**. The guide supplies 2,863 competitive games through 2024-25; the official 2025-26 South Carolina schedule adds 32 competitive games. The Oct. 26, 2025 NC State exhibition is excluded.

Year-by-year extraction was performed from the guide's Results section with page/row source locators retained in `source_page` and `raw_text`. Season-level W/L/T totals were checked against the guide's printed season aggregates. Tournament/postseason tables and the all-time ledger were used as cross-checks, not as license to overwrite conflicting chronological evidence without documentation.

Current supplement:
https://gamecocksonline.com/sports/mbball/schedule/

## Conference history and tournament-site research

Primary membership used by `conferences.csv`:

- Independent, 1908-09 through 1921-22
- Southern Conference, 1922-23 through 1952-53
- ACC, 1953-54 through 1970-71
- Independent, 1971-72 through 1982-83
- Metro Conference, 1983-84 through 1990-91
- SEC, 1991-92 onward

The 1921-22 and 1922-23 SIAA Tournament appearances remain event-level provenance rather than primary SIAA membership. The owner-supplied tournament workbook contains the two South Carolina-relevant SIAA rows and complete South Carolina-relevant Southern, ACC, Metro, and SEC tournament-site coverage. Shared tournament-site data supplies physical site only and never establishes H/A/N.

## Homecourt evidence

South Carolina's own homecourt history says the first five collegiate games were played outside and does not identify a physical court/building. Those five HOME rows retain Columbia, SC with `RESEARCHED_UNRESOLVED_HOME_VENUE` rather than receiving a guessed facility.

The same institutional history establishes:

- Carolina Gymnasium: first documented varsity game Jan. 7, 1912
- Carolina Fieldhouse: first documented game Feb. 17, 1927; last game Mar. 2, 1968
- Carolina Coliseum: first game Nov. 30, 1968; primary home through 2001-02
- Colonial Life Arena / Carolina Center: first men's game Nov. 24, 2002

The dedicated homecourt page's `Jan. 7, 1911` wording conflicts with its December 1911 renovation completion statement and the 1911-12 season ledger. The program-history chronology supports **1912-01-07**, which is used structurally while the conflict is documented.

## 1918-19 source defects

The guide's official 1918-19 aggregate is **4-7**, but the detailed surviving list exposes ten identifiable games totaling **4-6**. One placeholder loss is retained solely to preserve the source's official season accounting; opponent/date/score/site are left unknown.

A March 12, 1918 *Gamecock* recap naming a loss to the Camp Jackson Quartermasters Corps was investigated and rejected as evidence for the missing 1918-19 game because the article summarizes 1917-18:
https://historicnewspapers.sc.edu/lccn/2012218660/1918-03-12/ed-1/seq-5/ocr/

The Jan. 29, 1919 official row remains corrupted as `Cam3-45`. South Carolina's own current archive labels the opponent `NEEDS ADDED - Cam3-45`; no defensible opponent or score was recovered:
https://gamecocksonline.com/boxscore/needs-added-cam3-45/

Both unresolved historical opponent identities are represented explicitly in `opponents.csv` with `RESEARCHED_UNRESOLVED` status.

## NCAA physical-site research

All **19 NCAA Tournament rows** have a physical venue, city, and state. NCAA attendance/site records and official event material were checked against the South Carolina NCAA history and project physical-venue identities.

Representative NCAA identities include Reynolds Coliseum (1971 Raleigh), William and Mary Hall (1972 Williamsburg), WVU Coliseum (1972 Morgantown), Levitt Arena/current Charles Koch Arena (1973 Wichita), Hofheinz Pavilion (1973 Houston), The Palestra (1974 Philadelphia), Providence Civic Center/current Amica Mutual Pavilion (1989 Providence), Civic Arena (1997 Pittsburgh), MCI Center/current Capital One Arena (1998 Washington), Kemper Arena (2004 Kansas City), Bon Secours Wellness Arena (2017 Greenville), Madison Square Garden (2017 New York), University of Phoenix Stadium/current State Farm Stadium (2017 Final Four), and PPG Paints Arena (2024 Pittsburgh).

General NCAA site source:
https://fs.ncaa.org/Docs/stats/m_final4/2023/AttendSites.pdf

2024 Pittsburgh event evidence:
https://www.ncaa.com/_flysystem/public-s3/images/2024/03/18/2024%20MBB%20Satellite%20Coordinates_FirstFour_FirstSecondRound.pdf

## NIT research

All **32 NIT games** are physical-site complete. Dedicated NIT history establishes postseason identity; reciprocal/host sources were used where the guide supplied city or event context without a building.

Representative official evidence:
- UConn 2001 NIT / Gampel Pavilion: https://uconnhuskies.com/news/2001/3/12/tickets_for_uconn_south_carolina_nit_game_on_sale_tuesday
- Florida State 2006 NIT: https://gamecocksonline.com/news/2006/03/20/south-carolina-travels-to-florida-state-march-21-for-espn-televised-nit-second-round/
- Cincinnati 2006 NIT / Fifth Third Arena: https://gobearcats.com/news/2006/3/22/UC_Battles_USC_For_Berth_In_NIT_Final_Four.aspx

NIT championship games are marked `Championship`; other NIT rounds retain blank public postseason round under the project taxonomy.

## Neutral / special-event physical-site enrichment

H/A/N is never inferred from venue, city, opponent geography, or facility chronology. Once the guide establishes a neutral/special-site context, reciprocal official/event evidence may enrich the physical building.

The final research pass recovered all neutral physical-venue gaps from **1990-91 forward** and several additional 1980s sites. Representative resolutions include:

- 1980 Iona in Bowling Green — E.A. Diddle Arena. Iona official schedule: https://ionagaels.com/sports/mens-basketball/schedule/1980-81
- 1982, 1984, 1986, 1988 Davidson games in Charlotte — original 1955 Charlotte Coliseum, using reciprocal Davidson historical schedules.
- 1986 Sugar Bowl Tournament vs Vanderbilt/Villanova — Louisiana Superdome. Contemporary tournament reporting confirms the event; institutional Sugar Bowl tournament histories establish the Superdome physical site. Representative history: https://stats.hokiesports.com/mbasketball/records/schedule.html
- 1987 Iona — Brendan Byrne Arena. Iona official schedule: https://ionagaels.com/sports/mens-basketball/schedule/1986-87
- 1989 Central Fidelity Classic vs Maryland — Robins Center. Maryland official schedule: https://umterps.com/sports/mens-basketball/schedule/1989-90
- 1989 Sun Carnival Classic vs Kansas State — Special Events Center/current Don Haskins Center. Kansas State schedule: https://www.kstatesports.com/sports/mens-basketball/schedule/1989-90 ; UTEP/Sun Carnival venue history is consistent with the Special Events Center.
- 1990 ECAC Holiday Festival vs BYU/Maryland — Madison Square Garden. BYU: https://byucougars.com/sports/mens-basketball/schedule/season/1990-1991/ ; Maryland: https://umterps.com/sports/mens-basketball/schedule/1990-91
- 1996 and 2001 Maui Invitational — Lahaina Civic Center.
- 1998 Food Lion MVP Classic — 1988 Charlotte Coliseum.
- 1999 Puerto Rico Shootout — Coliseo Rubén Rodríguez, Bayamón.
- 2003 Guardians Classic — Municipal Auditorium, Kansas City.
- 2007 Old Spice Classic — Disney's Milk House/current HP Field House. South Carolina: https://gamecocksonline.com/news/2007/11/22/gamecocks-open-play-at-old-spice-classic-vs-penn-state/
- 2011 Las Vegas Invitational — Orleans Arena. South Carolina event material identifies the final rounds at Orleans Arena.
- 2013 Diamond Head Classic — Stan Sheriff Center.
- 2014 and 2022 Charleston Classic — TD Arena.
- 2016 and 2017 New York events — Madison Square Garden.
- 2017 Puerto Rico Tip-Off relocated to Myrtle Beach area — HTC Center, Conway, SC. South Carolina event material identifies HTC Center.
- 2019 Cancun Challenge — Hard Rock Hotel Riviera Maya Convention Center, Puerto Aventuras, Mexico; the event branding remains Cancun Challenge.
- 2020 Hall of Fame Classic — T-Mobile Center, Kansas City.
- 2021 Asheville Championship — Harrah's Cherokee Center.
- 2023 Virginia Tech game — Spectrum Center, Charlotte.
- 2023 Arizona Tip-Off — Desert Diamond Arena.
- 2024 Fort Myers Tip-Off — Suncoast Credit Union Arena.
- 2025 Greenbrier Tip-Off — Colonial Hall at The Greenbrier, from official Butler/Northwestern box-score evidence.

After this pass, **118** neutral historical rows remain without a defensible physical venue: 4 in the 1940s, 27 in the 1950s, 36 in the 1960s, 43 in the 1970s, and 8 in the 1980s. Each has paired `RESEARCHED_PARTIAL` status/basis; no unaccounted material site gap remains.

## Source-internal corrections and conflicts

Structured values were corrected only when official/reciprocal evidence made the source defect clear; `raw_text` remains untouched. Notable cases include:

- 2019-20 Mississippi State 83-71 is present in the guide; an early extraction pass missed its unusually formatted date token, so no supplemental duplicate is added.
- 2024-02-14 Auburn: the guide's result letter conflicts with its own 61-101 score; structured played result is a loss.
- 2006 Princeton: a guide score typo was corrected from reciprocal/official evidence while preserving the printed source text.
- Several 2009-10 losses use winner-first score presentation in the guide; structured South Carolina/opponent score orientation was normalized only after season/reciprocal cross-checks.

## Opponent normalization

`opponents.csv` contains **360 source-label rows** resolving to **307 canonical opponent identities**. Current Division I aliases are aligned to the project program registry where defensible; historical clubs, military units, YMCAs, high schools, reserve teams, and non-current colleges remain distinct historical identities rather than being forced into modern programs.

The two 1918-19 source defects remain explicit historical unresolved identities. Every `normalized_opponent_key` used by `source-games.csv` has a corresponding `opponents.csv` row, so the permanent research acceptance gate reports zero unresolved opponent references.

## Venue identity discipline

`venues.csv` contains **84** physical venue relationship/provenance rows. Numeric `venue_id` is intentionally blank throughout this research artifact. Existing physical identities and aliases are reused conceptually where known, but authoritative numeric IDs and any key/name reconciliation must occur after the mandatory current-main rebase in the serialized Implementation lane.

Different buildings with the same textual name remain separate physical identities, including the 1955 and 1988 Charlotte Coliseums and the historical/current Madison Square Garden distinction where relevant.
