# Butler men's basketball source-package curation notes

## Research status

This six-file portfolio is **RESEARCH_FROZEN** against `research_base_sha=e982a0ae746879d3a4c41a4dc128dc0107229f6d`. Owner scope: **ALWAYS_TOP_LEVEL_FROM_INCEPTION / INCEPTION+**. Butler's accepted competitive history begins in **1895-96** and runs through completed **2025-26**. Butler did not field a competitive varsity season in 1896-97 (intrasquad only), 1913-14, or 1943-44.

## Coverage and source-internal aggregate conflict

- Individually identifiable competitive game rows curated: **2,966**
- Curated on-court record from those identifiable rows after game-specific source corrections: **1706-1260**
- Site classifications: **1294 Butler-home / 1131 opponent-home / 184 neutral / 357 unknown**
- Game types: **2825 regular season / 77 conference tournament / 40 NCAA Tournament / 15 NIT / 9 other postseason**
- Exhibitions/intrasquad contests: **excluded**

Butler's 2026 record book contains a genuine internal aggregate contradiction and the package does not manufacture anonymous games to force one total. Its printed all-time total is **1,710-1,259 (2,969 decisions)**. The season record headings sum instead to **1,709-1,261 (2,970 decisions)**. The all-time game ledger yields **2,966 individually identifiable rows**. The 1899-00 and 1902-03 sections explicitly say **Other Results Not Available** and their season headings imply aggregate-only games, while the 1944-45 heading says 14-6 even though its 20 named result lines total 13-7. These incompatible official representations are preserved as provenance debt rather than reconciled by invented rows or arbitrary result flips.

## Game-specific source corrections

Four modern Butler ledger lines are normalized using stronger reciprocal/game-specific evidence while their original strings remain unchanged in `raw_text`: 1981-82 Dayton (Butler W 70-58), 1981-82 at Saint Louis (Butler W 70-61), 1982-83 Valparaiso (Butler W 69-60), and 1984-85 at Oral Roberts (Butler W 62-60). Two impossible February 29 date renderings were likewise corrected field-specifically after schedule/reciprocal review: 2004-05 UIC to 2005-02-26 and 2005-06 at Detroit to 2006-02-25. Butler's first-game footnote typo rendering Jan. 29, 1896 as 1986 is preserved in raw provenance while normalized to 1896.

## H/A/N discipline

Butler's printed all-time ledger uses explicit `at`, `vs.`, and opponent typography as site evidence, but early notation is not treated as mechanically infallible. Butler-published series history and authoritative reciprocal opponent histories override the ledger only when a season/opponent/score match is unique. The clearest early example is 1900-01 Indiana, where reciprocal Indiana evidence reverses the apparent direction of Butler's Feb. 8 and Feb. 28 typography. Geography and venue identity never establish H/A/N.

The adversarial self-challenge began from **435** working UNKNOWN H/A/N rows and recovered **78**, leaving **357** researched UNKNOWN rows. All surviving UNKNOWN H/A/N rows are pre-2000 and carry substantive research accounting. The final decade concentration is: 1890s 6; 1900s 34; 1910s 69; 1920s 109; 1930s 40; 1940s 25; 1950s 11; 1960s 10; 1970s 14; 1980s 22; 1990s 17. The final pass specifically removed the remaining suspicious modern debt using Butler and reciprocal institutional histories, including DePaul, Seton Hall, St. John's, Villanova, Milwaukee, Green Bay, and the 2001 conference-tournament Loyola game.

## HOME venue research

Butler institutional history establishes the first game in Butler Fieldhouse on **March 7, 1928**, and the building's later Hinkle Fieldhouse identity. Hinkle is assigned only after Butler HOME classification is independently established; the facility chronology never creates H/A/N. The 1942-43 record book explicitly says home games were played at **Tech H.S.**, normalized to Arsenal Technical High School. Butler's Fieldhouse history documents the wartime interruption.

Final `RESEARCHED_UNRESOLVED_HOME_VENUE` population: **47 rows** — **40** pre-Fieldhouse HOME games from 1895-96 through February 1928 and **7** 1944-45 HOME games during the wartime Fieldhouse interruption. Every row has Indianapolis, IN geography and a substantive research basis. Institutional facility history, Butler schedules/record book, archival facility material, and available reciprocal histories were reviewed; no authoritative evidence safely assigns one physical predecessor/replacement building to these individual games. This is therefore a bounded historical exception, not a primary-ledger venue blank carried forward without research. HOME publication blockers: **0**.

## Postseason and neutral-site completeness

Regular-season invitationals remain `REGULAR_SEASON`. Butler's official competitive ledger contributes **40 NCAA Tournament games**, **15 NIT games**, **77 conference-tournament games**, the four-game 1924 AAU National Tournament, the 2012 CBI, and the 2025 College Basketball Crown. Every NCAA Tournament row has a physical venue plus city/state.

The four 1924 AAU games are now physically resolved to **Convention Hall, Kansas City, MO** from contemporary tournament reporting and historical AAU venue chronology. Conference-tournament, NIT, CBI, Crown, and modern neutral-event sites received targeted game/event review. Residual researched site debt is deliberately narrow: **6** non-NCAA neutral rows lack an exact venue, **3** of those also lack city/state (1898-99 and 1918-19 Wabash neutral games), and **1** postseason row — Butler's 1981 MCC game against Oklahoma City — has Oklahoma City, OK but no exact building because surviving sources conflict/are insufficient at building level. Postseason rows missing location: **0**. NCAA site gaps: **0**.

## Conference tournament site workbook

Owner-supplied **`Conference_Tournament_Site_Reference(20260903-090918).xlsm`** is globally incomplete and is authorized **only for Butler research in this lane**. Butler-relevant Midwestern City/Midwestern Collegiate/Horizon/A10/BIG EAST rows are used for physical venue/city/state evidence and cross-checked at game level when the event was not entirely centralized. The workbook never establishes H/A/N. Its 1993-94 `Hinke Fieldhouse` spelling is normalized to Hinkle Fieldhouse while the source-version note preserves the workbook provenance.

## Exact-date uncertainty

The working ledger extraction began with **473** rows lacking an exact date. Official Wabash and Ball State reciprocal histories plus targeted institutional evidence recovered **68** exact dates on uniquely matched games; **405** remain blank. Final blank-date concentration: 1890s 9; 1900s 34; 1910s 69; 1920s 140; 1930s 103; 1940s 49; 1950s 1. No date was inferred from schedule order, geography, usual series timing, or season chronology.

## Opponent identity and owner sanity scan

All source opponent labels resolve to stable canonical identities. The adversarial current-registry audit found and mechanically repaired **3** current-D1 key splits: Detroit→`detroit-mercy`, Penn→`pennsylvania`, and Hawaii→`hawai-i`. Ambiguous current-program identity matches at freeze: **0**.

The owner approved the complete NON_D1 population, including the self-challenge amendment for Saint Francis (Pa.): **77 distinct canonical identities / 645 identifiable games**. The Saint Francis amendment covers Butler's two games against the institution now transitioning from Division I to Division III. No opponent identity remains unresolved.

## Venue physical-identity census

`venues.csv` contains **72 local physical venue rows**. Against the recorded research base, **62** are definite physical reuses and **10** are genuinely new research-time candidates: Arsenal Technical High School; Athletics-Recreation Center; Brown County Arena; Carver Arena; Nutter Center; Afook-Chinen Civic Auditorium; Anaheim Convention Center; Carlson Center; Coliseo Roberto Clemente; and Klotsche Center. Ambiguous physical-identity matches: **0**.

The self-challenge also explicitly split Madison Square Garden III (1925 building) from Madison Square Garden IV/current Garden rather than treating the shared name as one physical venue. Numeric global venue IDs remain intentionally blank/provisional. The serialized Implementation lane must perform the authoritative current-main physical-identity rebase before tracked Phase 0.

## PRE-FREEZE SELF-CHALLENGE: PASS

- `RESEARCHED_UNRESOLVED_HOME_VENUE`: **47 final**; pre-March-1928 and 1944-45 only; 1942-43 Tech H.S. recovered as a specific physical home site.
- UNKNOWN H/A/N: **435 working / 78 recovered / 357 final**; all final rows pre-2000 and research-accounted.
- UNKNOWN exact dates: **473 original / 68 recovered / 405 final**, overwhelmingly pre-1950.
- VENUES: **72 local physical rows / 62 research-base reuses / 10 genuinely new candidates / 0 ambiguous identities**.
- OPPONENT IDENTITIES: **3 current-program key splits found/repaired / 0 ambiguous current-program matches / owner-approved NON_D1 population 77 identities and 645 games**.
- HOME publication blockers: **0**.
- NCAA physical-site gaps: **0**.
- Material site-gap rows: **411**; researched/accounted: **411**; unaccounted: **0**.
- Research acceptance errors: **0**.
- Research acceptance warnings: **0**.

## Freeze boundary

The package is research-complete under the project's current evidence and uncertainty rules. It is not integration-ready without the required serialized current-main rebase of shared opponent/conference/venue references.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=286548b2041ee854e85c84c9b42a977b7efbc3ff` from `research_base_sha=e982a0ae746879d3a4c41a4dc128dc0107229f6d`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.


### Stage 2 NCAA accomplishment normalization

Current Implementation preflight exposed a deterministic accomplishment cross-check gap because the four 2010/2011 Final Four games were correctly present in the frozen game ledger but carried blank normalized NCAA rounds. The following round labels were added without changing game identity, date, score, opponent, site, venue, or raw source evidence:

- 2010-04-03 vs Michigan State — Final Four
- 2010-04-05 vs Duke — Championship
- 2011-04-02 vs VCU — Final Four
- 2011-04-04 vs Connecticut — Championship

Authoritative corroboration: Butler Athletics identifies Michigan State and VCU as national semifinals and Duke/Connecticut as national title games; NCAA championship history records Butler as national runner-up in both 2010 and 2011.
