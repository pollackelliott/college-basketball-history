# Oklahoma State source notes

## Primary institutional source

**Oklahoma State University, 2025-26 Men's Basketball Media Guide** (`2025-26_OSU_MBB_Guide_web-.pdf`).

SHA-256: `7b48ff4ee671136e38380cd2b289012805dc7f7fd4fef470c4e32210359b486e`

High-value sections used include:
- program quick facts / all-time record
- year-by-year records
- game-by-game history
- conference affiliation and championship history
- Gallagher-Iba / home-facility history
- NCAA Tournament history
- NIT/postseason history

The source's literal opponent/date/result wording is preserved in `source-games.csv.raw_text`. Structured normalization does not erase source defects or historical labels.

## Completed 2025-26 supplementation

**Oklahoma State Athletics official 2025-26 schedule/results**
https://okstate.com/sports/mens-basketball/schedule/2025-26

The completed season contributes **35 competitive games, 20-15**. Two explicitly designated exhibitions are excluded:
- 2025-10-15 Auburn — exhibition
- 2025-10-25 at SMU — exhibition

The competitive season ends with the Big 12 Tournament and NIT through 2026-03-22.

## Owner-authorized conference-tournament site reference

**`Conference_Tournament_Site_Reference(20260907-005551).xlsm`**

SHA-256: `5fe2fb5659b6f4e0f37471b5893b860d07bc9113c9c16b1692aa78c9f434e79e`

Owner authorization is deliberately narrow: the workbook is incomplete globally and must not be promoted to universal project canon. It is authorized only for Oklahoma State's conference-membership/tournament history.

It is used for Oklahoma State-relevant tournament-site evidence and split-site/campus-round chronology. It never establishes H/A/N from geography.

## Source-internal defects and corrections

The primary guide contains several documented defects:
- two duplicated Saint Louis bleed rows inside the 1972-73 block;
- 1912-13 section header prints 3-6 while listed games reconcile 4-5;
- 2000-01 section header prints 23-9 while listed games reconcile 20-10;
- conference regular-season championship headline prints 18 even though the listed component totals sum to 19.

The competitive ledger preserves the actual listed games and source provenance rather than forcing row-level history to match defective headers/headlines.

## Opponent identity research

Every distinct Oklahoma State source label is resolved in `opponents.csv`; unresolved opponent identities = 0.

Particularly important structured corrections, with literal source label preserved:
- `McMurry` -> MacMurray College (Illinois), two games
- `Trinity (TX)` / `Trinity` -> Trinity College (Conn.), three games
- `Santa Fe College` -> College of Santa Fe, one game

Historical clubs, service teams, small colleges, and other genuinely distinct non-current opponents remain distinct identities. Current-D1 lineages are not hidden under stale historical aliases.

## H/A/N and venue hierarchy

Research hierarchy:
1. explicit Oklahoma State game-level `at` / `vs` / home context;
2. explicit official schedule/postseason context;
3. owner-authorized Oklahoma State conference-tournament site evidence;
4. established NCAA/postseason physical-site evidence;
5. Oklahoma State home-facility chronology only after HOME is independently established.

Venue and geography never create H/A/N.

## Home-facility history

Institutional/athletics history supports three physical home eras:
- Oklahoma A&M Original Armory, program inception through the 1918-19 season;
- Oklahoma A&M New Armory, replacement facility beginning in 1919 through the final documented home game on 1938-03-04;
- Gallagher-Iba Arena, current physical building beginning with the 1938-12-09 basketball opener.

The two Armories are separate physical venue candidates. Gallagher-Iba reuses the research-base global physical venue identity.

## Big Eight Holiday Tournament taxonomy correction

Stage 3B identified 54 December `c` rows from 1958-59 through 1975-76 as **Big Eight Holiday Tournament** games. The media-guide season legends identify these games as the holiday event in Kansas City; they are `REGULAR_SEASON`, not conference postseason.

Stage 6 adversarial review supplied stronger official conference-history evidence for the building chronology. Iowa State Athletics states that Municipal Auditorium hosted the final Big Eight Holiday Tournament game there on 1973-12-29, and Kansas State's official conference-history material states the event was held at Municipal Auditorium from 1946-73 and moved to Kemper Arena beginning with the 1974 tournament. Accordingly all 54 rows now have physical venues: Municipal Auditorium through 1973 and Kemper Arena beginning in 1974.

## NCAA Tournament site research

Acceptance state:
- NCAA Tournament games: **67**
- physical venue complete: **67/67**
- city/state complete: **67/67**
- ambiguous physical venue identities: **0**

Historical source-era arena names are normalized to the correct physical building while source-era labels remain preserved where available.

The 1951 NCAA third-place game remains `NCAA_TOURNAMENT` with blank controlled round under project policy for historical consolation/third-place games.

## Non-NCAA postseason residuals

Stage 6 reciprocal review recovered all four previously unresolved road-NIT buildings:
- 1989 St. John's — Alumni Hall, same physical building later Carnesecca Arena;
- 2006 Miami (FL) — BankUnited Center, same physical building later Watsco Center;
- 2008 Southern Illinois — SIU Arena, same physical building later Banterra Center;
- 2023 Youngstown State — Beeghly Center, current naming Zidian Family Arena at Beeghly Center.

Oklahoma State's official 2025 Oklahoma City history also identifies the 1939 district playoff loss to Oklahoma at the old Municipal Auditorium (now Civic Center Music Hall), resolving that row's building.

Eight historical non-NCAA postseason rows still lack exact buildings: two 1936 District Olympic Trials rows and six NCAA District Playoff rows from 1939-49. Their H/A/N and city/state are established, and each carries explicit research basis. These are researched historical building unknowns, not silent blanks.

## Administrative-result policy

The project uses played on-court result for historical game records. Later forfeits/vacated outcomes are preserved separately in source-level administrative notes. Oklahoma State's seven known administrative-difference rows remain literal on-court W/L rows with explanatory provenance.

## Research baseline

Repository research policies, source schema, global opponent identities, conference registry, and physical venue registry were evaluated against:

`research_base_sha=c6be3bc78b4f777f731735a03cbbd5ad418f04a7`

Research-time numeric IDs for genuinely new venues remain provisional until serialized current-main rebase.

## Stage 6 modern neutral-site recovery

The adversarial self-challenge targeted all 29 regular-season neutral venue blanks from the 2000s. Official Oklahoma State and reciprocal institutional schedules/game notes recovered **27** exact buildings. The recovered physical identities include Mabee Center, Myriad Convention Center, Valley High School, Simmons Bank Arena (source-era ALLTEL Arena), Sullivan Arena, Delta Center, Paycom Center (source-era Ford Center), Viejas Arena (source-era Cox Arena), Bridgestone Arena (source-era Gaylord Entertainment Center), Lahaina Civic Center, HP Field House (source-era The Milk House), Orleans Arena, and Mohegan Sun Arena.

Only two 2000s regular-season neutral building blanks remain: the 2006 South Padre Island Invitational games against Auburn and Missouri State. Official material confirms South Padre Island but did not provide a sufficiently supported exact physical building, so those rows remain explicitly `RESEARCHED_PARTIAL`.

## Stage 6 physical-identity reconciliation

Research-base global venue identity was rechecked before freeze. Current-base reuses were preferred wherever the building already existed. Historical naming-rights labels remain in `source_venue_name` or venue aliases while `curated_venue_name` represents the physical identity.

Two provisional local identities received naming-era clarification without being merged into unsupported global rows:
- Oklahoma City Municipal Auditorium is the same physical building later known as Civic Center Music Hall.
- Tulsa Convention Center is the same physical convention-center facility through Cox Business Center/Cox Business Convention Center and Arvest Convention Center naming eras.

No matching physical rows existed for those buildings in the recorded research-base venue registry. Numeric `VEN-99xxxx` identifiers remain provisional until serialized current-main rebase.
