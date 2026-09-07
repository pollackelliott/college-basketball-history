# Butler source notes and provenance

## Primary institutional source

- **Butler 2026 Men's Basketball Record Book** (`Butler_MBB_Record_Book_2026_July.pdf`), owner supplied. All-Time Results pages 44-60 are the controlling Butler game ledger through completed 2025-26. The year-by-year record headings, Series History, postseason sections, venue history, and facility-history material are used as corroborating Butler-published evidence, but source-internal contradictions are not silently overwritten.
- Butler's record book contains a first-game footnote typo rendering the Jan. 29, 1896 first game as `1986`; season context and the explicit first-game statement control the normalized 1896 date while the raw text is preserved.

## Owner-authorized conference tournament reference

- **`Conference_Tournament_Site_Reference(20260903-090918).xlsm`**, owner supplied. This workbook is not a globally complete source and must not be generalized outside the Butler lane. By owner ruling it is sufficiently complete for Butler's historical conference memberships. It is used only for Butler-relevant physical conference-tournament sites and never to establish H/A/N. Non-centralized Horizon tournaments are cross-checked at the individual Butler game level.

## Historical reciprocal / targeted research

- Wabash College Athletics official Butler opponent history: used to recover exact dates and H/A/N for uniquely matched historical games and to expose, but not forcibly reconcile, the 1899-00/1902-03 source conflicts.
- Ball State Athletics official Butler opponent history: used for exact-date/H/A/N recovery including historical Muncie Normal lineage and the 1944-45 Butler series.
- Indiana and Purdue institutional histories: used for early game-specific H/A/N/date validation, including the 1900-01 Butler/Indiana notation reversal.
- Valparaiso, Saint Louis, Dayton, and Oral Roberts reciprocal histories/schedules: used only for documented modern score/result corrections where game identity is unambiguous.
- Boston University institutional history confirms Butler's 1937-38 `BOSTON` opponent as Boston University.

## Final H/A/N self-challenge sources

The final adversarial pass specifically challenged modern UNKNOWN rows and large/suspicious institutional series. Butler and reciprocal official histories/schedules supplied game-level recoveries without using geography or venue as an H/A/N shortcut. Representative sources include:

- Milwaukee 2002-03 official schedule: https://mkepanthers.com/sports/mens-basketball/schedule/2002-03?grid=true
- Green Bay official Butler opponent history: https://greenbayphoenix.com/sports/mens-basketball/opponent-history/butler-university/34
- DePaul official Butler opponent history: https://depaulbluedemons.com/sports/mbball/opponent-history/butler/44
- Butler official DePaul opponent history: https://butlersports.com/sports/mens-basketball/opponent-history/depaul/28
- Butler official Seton Hall opponent history: https://butlersports.com/sports/mens-basketball/opponent-history/seton-hall-university/103
- Butler official St. John's opponent history: https://butlersports.com/sports/mens-basketball/opponent-history/st-johns-university/89
- Villanova 2025-26 official schedule: https://villanova.com/sports/mens-basketball/schedule/2025-26?grid=true
- Butler 2022-23 official schedule: https://butlersports.com/sports/mens-basketball/schedule/2022-23?grid=true
- Butler 2015-16 official schedule: https://butlersports.com/sports/mens-basketball/schedule/2015-16?grid=true

## Facility and HOME-site research

Butler institutional Hinkle/Butler Fieldhouse history establishes March 7, 1928 as the first Butler Fieldhouse game and the later Hinkle name. The record book explicitly states 1942-43 home games were at Tech H.S.; the Fieldhouse's wartime interruption is independently documented. Pre-Fieldhouse and 1944-45 exact HOME-building gaps are therefore represented as researched uncertainty with complete Indianapolis geography, not filled from a blanket arena chronology.

## NCAA / postseason physical-site research

NCAA physical venues were checked against Butler/institutional tournament material and established tournament histories. Legacy naming is represented as physical identities/aliases in `venues.csv` where appropriate (for example Verizon Center/Capital One Arena, EnergySolutions Arena/Delta Center, HSBC Arena/KeyBank Center, BMO Harris Bradley Center/Bradley Center, and separate Madison Square Garden III/IV physical buildings). NIT, CBI, College Basketball Crown, conference-tournament, and material neutral sites were likewise checked against institutional schedules/releases and event histories.

The 1924 AAU National Tournament is retained as generic postseason and all four Butler games are assigned to **Convention Hall, Kansas City, MO**. Contemporary championship reporting reprinted by the Marion County Historical Society describes the Butler-Hillyards championship before approximately 12,000 at Convention Hall, and historical AAU venue chronology supports Convention Hall for the 1924 national tournament: https://www.mchsindy.org/single-post/butler-captures-national-court-tourney-30-to-26

The 1980-81 MCC tournament game against Oklahoma City is deliberately more conservative. Butler's game is independently established as an Oklahoma City-hosted contest, so H/A/N is not inferred from venue. Surviving tournament/building evidence does not safely distinguish the exact building; city/state are retained as Oklahoma City, OK and the venue remains blank under `RESEARCHED_PARTIAL` rather than forcing a building.

## Neutral-event physical-site research

Targeted event/institutional evidence was used to fill modern neutral sites where support was game- or event-specific. Examples include Met Center (Pillsbury Classic), Hearnes Center (Show Me Classic), McKale Center (Fiesta Bowl Classic), Carlson Center (Top of the World Classic), Stan Sheriff Center (Rainbow/Diamond Head), Arena-Auditorium (BCA Classic), Madison Square Garden, Sullivan Arena (Great Alaska Shootout), Anaheim Convention Center (76 Classic), Imperial Arena (Battle 4 Atlantis), Coliseo Roberto Clemente (Puerto Rico Tip-Off), Orleans Arena (Las Vegas Invitational), Moda Center/Veterans Memorial Coliseum (PK80), Michelob ULTRA Arena (2021 Maui Invitational in Las Vegas), and Colonial Hall at The Greenbrier.

Remaining neutral building/location blanks are explicitly research-accounted rather than inherited silently. The three remaining neutral location blanks are early Wabash games for which Butler/Wabash evidence establishes neutral classification but not a safe city/state. The 1986 Rochester Classic, 1987 Blade Classic, and 1996 Puerto Rico Shootout retain known event geography while exact building identity remains unsupported.

## Opponent identity audit

The local opponent inventory was compared against the protected-main current-D1 program registry and published reciprocal aliases. Three mechanical current-program key splits were repaired during the final self-challenge: Detroit→`detroit-mercy`, Penn→`pennsylvania`, and Hawaii→`hawai-i`. Historical institutional names were merged only where continuity was independently supported; string similarity alone was not used.

The owner approved the complete Butler NON_D1 sanity scan and then separately approved the self-challenge amendment adding Saint Francis (Pa.). Final approved population: **77 distinct canonical NON_D1 identities / 645 identifiable games**. Ambiguous current-program identity matches: **0**.

## Research-base physical-venue audit

Research was conducted against `research_base_sha=e982a0ae746879d3a4c41a4dc128dc0107229f6d`. The final `venues.csv` has **72** local physical identities: **62** definite reuses of physical venues present at the research base and **10** genuinely new research-time candidates. The new candidates are Arsenal Technical High School, Athletics-Recreation Center, Brown County Arena, Carver Arena, Nutter Center, Afook-Chinen Civic Auditorium, Anaheim Convention Center, Carlson Center, Coliseo Roberto Clemente, and Klotsche Center. Ambiguous physical-identity matches: **0**.

Numeric venue IDs are deliberately deferred. Current main may move while this frozen package waits, so the serialized Implementation lane must perform the authoritative current-main shared-reference rebase before tracked Phase 0.
