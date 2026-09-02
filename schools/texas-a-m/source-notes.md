# Texas A&M research sources and provenance

## Primary source

Texas A&M Athletics, *History & Records* / 2024-25 men's basketball media-guide records section, supplied by the owner. This is the primary annual-results ledger through 2023-24 and the authority for source raw text, scores, result notation, overtime markers, conference-game markers, dedicated conference-tournament history, NCAA history, and historical summaries.

## 2024-25 and 2025-26 supplements

Texas A&M Athletics official season schedule pages were used to extend the ledger through the two completed seasons. The 2024-25 official page identifies Oct. 27 Houston as a Charity Exhibition Game; the 2025-26 page identifies Oct. 26 Arizona State as an Exhibition Game. Both are excluded. Official schedules supply exact date, H/A/N, venue, city/state, and event labels for these seasons.

## Conference tournament physical sites

The owner supplied `Conference_Tournament_Site_Reference(20260901-114127).xlsm`. Its Texas A&M-relevant Southwest Conference, Big 12, and SEC sections were independently checked for chronology coverage and are accepted per owner instruction as canonical physical-site evidence for this school. The workbook is globally incomplete. Absence is never negative evidence, and the workbook does not determine H/A/N. Its explicit early-SWC campus-preliminary notes are honored game by game.

## NCAA physical sites

Texas A&M official NCAA Tournament history/current 2025-26 game notes provide the venue and location for all NCAA appearances. These include Municipal Auditorium (1951 Kansas City), Moody Coliseum (1964 Dallas), Daniel-Meyer/Schollmaier physical site (1969 Fort Worth), Ahearn Fieldhouse (1969 Manhattan), Lubbock Municipal Coliseum (1975), The Super Pit and The Summit (1980), Hoosier Dome (1987), Jacksonville Veterans Memorial Arena (2006), Rupp Arena and Alamodome (2007), Honda Center (2008), Philadelphia's Wachovia/Wells Fargo physical arena (2009), Spokane Arena (2010), United Center (2011), Oklahoma City's Chesapeake/Paycom physical arena and Honda Center (2016), Spectrum Center and Staples/Crypto.com physical arena (2018), Wells Fargo Arena Des Moines (2023), FedExForum (2024), Ball Arena (2025), and Paycom Center (2026).

## 1951 District 6 / date enrichment

Texas A&M's official 1950-51 schedule and Texas's official fact book were used to distinguish the three-game SWC/NCAA District 6 playoff from the NCAA Tournament proper and to supply March 9, 12, and 13 dates. Texas A&M's official opponent history/current archive supports March 22, 1951 for Washington. This reduces intentional unknown exact dates without guessing.

## Home chronology

Texas A&M official game-note material titled "The Homes of Aggie Hoops" is the principal home-building source: DeWare Field House 1924-1954, G. Rollie White Coliseum 1954-1998, Reed Arena 1998-. Texas A&M's Nov. 13, 1998 North Texas postgame notes explicitly call that the first basketball game in Reed Arena. Texas A&M campus historical material confirms Memorial Gymnasium/DeWare was built in 1924.

## Reciprocal forfeit evidence

The supplied/archived Texas 2025-26 fact book is used only as reciprocal evidence for the 1918 Texas-A&M Dwyer forfeit. It explicitly says the game was forfeited to Texas because Texas A&M's player was ruled ineligible. The competing A&M source string is preserved.

## Research uncertainty policy

Historical neutral regular-season rows lacking a retained authoritative building/location source are deliberately marked `RESEARCHED_UNRESOLVED` rather than filled from geography. Pre-1924 A&M-home rows use the stricter dedicated home-venue exception with complete College Station, Texas location. Away regular-season opponent buildings are not required by the permanent research-freeze gate and are not guessed.

## Bounded exact-date recovery audit

A post-freeze exact-date QA pass was limited to rows whose `game_date` was blank. The starting count was **759**. Dates were accepted only when authoritative reciprocal/institutional evidence provided an exact date and the candidate identity was sufficiently supported by season, opponent, reciprocal score/result, and H/A/N or other site context. **217 dates were recovered; 542 remain unresolved.**

Principal evidence:
- University of Texas Athletics, official 2025-26 men's basketball Fact Book/year-by-year results, as preserved in current main.
- University of Arkansas Athletics, official historical men's basketball media-guide/year-by-year results, as preserved in current main.
- LSU Athletics, official 2025-26 men's basketball Record Book/year-by-year results, as preserved in current main.
- Kentucky, Purdue, and Ohio State official historical ledgers, as preserved in current main, for isolated reciprocal matches.
- TCU Athletics, official men's basketball opponent history vs. Texas A&M.
- Rice Athletics, official men's basketball opponent history vs. Texas A&M.
- Baylor Athletics, official men's basketball media-almanac all-time results.

The audit deliberately rejected reciprocal candidates when score or site context conflicted materially, when two local rows could plausibly map to one reciprocal game, or when the reciprocal institutional ledger itself omitted a date. No exact date was inferred from sequence, geography, typical series cadence, or calendar plausibility.

Remaining blank-date concentration by starting decade: 1910s 92; 1920s 129; 1930s 156; 1940s 149; 1950-51 16. The surviving gaps are therefore wholly concentrated in the historical ledger through February 1951, especially series for which currently accessible institutional histories omit dates or do not expose a sufficiently matchable reciprocal ledger.

## Research-base venue identity audit

The completed local venue list was compared against the project global venue registry and venue-name alias registry at `research_base_sha=fb886afc1f940ddc9e5904908cc2f2c5cf7077cb`. The comparison used physical building identity plus city/state, known historical/current aliases, and date-aware identity where a name can refer to multiple buildings (notably Madison Square Garden).

The audit exposed one real local physical-identity duplication: historical **Ford Center** and current **Paycom Center** are the same Oklahoma City arena (`VEN-000162` on the research base). The two research-provisional rows were consolidated into one physical row, retaining Ford Center as an alias. Revised results: **64 local physical venue rows; 57 existing-current-main physical reuses; 7 genuinely new physical candidates; 0 ambiguous physical-identity matches.**

New candidates: Arena-Auditorium (Laramie, WY); College Park Center (Arlington, TX); DeWare Field House (College Station, TX); Lakefront Arena (New Orleans, LA); Old Gymnasium (Nevada) (Reno, NV); Redbird Arena (Normal, IL); Schollmaier Arena (Fort Worth, TX).

No local venue IDs were renumbered by this research QA. Final VEN-ID reuse/allocation remains an Implementation responsibility after current-main rebase.
