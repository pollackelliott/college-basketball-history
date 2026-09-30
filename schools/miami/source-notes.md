# Miami (FL) source notes

## Source hierarchy

This Stage 6 audited package preserves the accepted durable Stage 1 through Stage 3B chain and the completed Stage 4/Stage 5 state. Stage 6 used only bounded self-challenge and targeted accepted-project checks. The controlling evidence order carried forward from those stages is:

1. Miami institutional media guide / official schedule and exact-game Miami pages;
2. accepted project/current-main reciprocal and physical-identity evidence;
3. owner-authorized conference-tournament site reference after independent postseason classification;
4. official event, conference, host, opponent, NCAA/NIT/NAIA, and participant institutional evidence used in the bounded Stage 3 research units;
5. targeted authoritative archival fallback only where the completed research stages required it.

Literal source evidence is preserved in `raw_text`. Accepted corrections or stronger site/classification evidence are recorded in curated fields and `notes` rather than rewriting the literal row.

## Primary historical source

**Miami 2025-26 Men's Basketball Media Guide**  
User-supplied filename: `Miami (fl).pdf`  
SHA-256: `08c28f9a983ee15c58ffdabe27b0e4b9d6f6122d79e94372b9cc3dcf05093c70`

The media guide's All-Time Results section supplies the row-level historical spine through 2024-25, including literal opponent/result strings, date tokens, H/A/N/source markers, postseason markers, and page-level locators. Its program-history, season-summary, NCAA, NIT, ACC Tournament, BIG EAST Tournament, home-record/facility, and accomplishments sections provide systematic cross-check and contextual evidence used by the accepted research stages.

The package preserves 1,807 rows with source era `miami_2025_26_media_guide_all_time_results`.

## Modern-season supplementation

**Miami Hurricanes Official Athletics — 2025-26 Men's Basketball Schedule**  
`https://miamihurricanes.com/sports/mbball/schedule/season/2025-26`

The official completed schedule supplies 35 accepted 2025-26 source rows through Miami's NCAA Tournament second-round game on 2026-03-22. Exact-game Miami recaps/announcements and official event/participant pages were used during the already-completed Stage 3A/3B site work where the schedule or guide did not itself provide all required venue/postseason detail.

## Row-count audit

- media-guide rows: 1,807
- 2025-26 official-schedule rows: 35
- total competitive rows: 1,842
- unique `source_game_id` values: 1,842
- exhibitions/noncompetitive events included: 0
- rows with blank exact date: 3
- rows with blank played score: 0

The Stage 4 source-game ID population exactly matches the authoritative Stage 3B working ledger.

## Accepted top-level scope

The repository's owner-supplied Program Top-Level Scope Reference controls Miami as:

`1948-49..1952-53 | 1954-55..1970-71 | 1985-86+`

Stage 1/Stage 4 therefore do not reconstruct or publish source rows outside those accepted intervals merely because the institutional media guide contains broader program history. There are no accepted source-game rows for 1953-54 or the 1971-72 through 1984-85 hiatus.

## Opponent identity sources

Stage 2 is authoritative for package opponent identity. Current Division I identities are rechecked against protected-main `data/reference/programs.csv`; source labels are preserved independently in `source_opponent_label` and `raw_text`. Historical/non-D1 identities remain distinct where the evidence supports distinct entities.

Two particularly non-obvious current-D1 lineage normalizations are preserved as informational self-corrections:

- `Baptist` -> Charleston Southern, based on institutional name history for Baptist College at Charleston / Charleston Southern;
- `Teachers College of CT` -> Central Connecticut, based on Central Connecticut institutional history for the Teachers College of Connecticut naming era.

Non-D1 lineage/name examples include `Biscayne` -> St. Thomas (FL) and `Loyola (N.O.)` -> Loyola New Orleans. The complete NON_D1 population is serialized for owner review rather than silently treated as final merely because Stage 2 resolved it.

## Conference source

Miami institutional year-by-year/coaching records and historical narrative establish the package chronology:

- Independent through the pre-hiatus accepted era;
- Independent after the 1985-86 rebirth through 1990-91;
- BIG EAST beginning 1991-92;
- ACC beginning 2004-05, following official ACC membership on July 1, 2004.

Protected-main `data/reference/conferences.csv` already contains `independent`, `big-east`, and `acc`; Stage 4 creates no new shared conference identity.

## HOME venue sources

Accepted Stage 3A facility chronology is carried into the package, including:

- Miami institutional history/home-record tables for James L. Knight Center, Miami Arena, and the Convocation Center / BankUnited Center / Watsco Center physical building;
- University of Miami historical institutional material establishing the accepted Dinner Key Auditorium rows;
- contemporaneous Miami institutional/local archival evidence supporting the accepted Miami Beach Auditorium default classes;
- the deliberately unresolved 1957-58 split between Miami Beach Auditorium and Coral Gables High gym when exact row allocation could not be established.

The accepted Stage 3A row-level basis remains controlling. Venue chronology was applied only after HOME classification had been independently established.

## Regular-season neutral sources

Stage 3A neutral research used the serialized accepted evidence for recurring and one-off event families. High-yield official event/participant examples preserved in row evidence include Charleston Classic, Paradise Jam, Puerto Rico Tip-Off, Diamond Head Classic, Wooden Legacy, ESPN Events Invitational, Baha Mar Hoops Bahamas Championship, Basketball Hall of Fame events, and exact Miami game pages.

Historical regular-season neutral 1995-96-and-earlier rows use the current location-first standard. Modern U.S. neutral rows use the strong exact-venue expectation. Outside-U.S. locality-sufficient terminalization is preserved where applicable. Stage 6 did not reopen historical neutral building archaeology. A targeted check of the eight blank neutral rows that already carried published-reciprocal provenance recovered one exact venue: Michigan reciprocal row MICHRAW-01588 names Sullivan Arena for Miami on 1987-11-27; the other seven reciprocal rows remain locality-only.

## Postseason sources and aggregate QA

The accepted Stage 3B ledger contains 112 postseason rows:

- 58 conference-tournament rows;
- 29 NCAA Tournament rows;
- 23 NIT rows;
- 2 other postseason rows.

Conference-tournament sites use the owner-authorized shared site reference only after independent classification and within its allowed scope. Miami institutional ACC/BIG EAST Tournament history remains the target-program classification/round backbone.

NCAA/NIT/other-postseason site work uses Miami institutional postseason history plus exact-game Miami, host, opponent, NCAA/NIT/NAIA, and other authoritative evidence serialized in the Stage 3B basis fields. Exact-site examples include Miami institutional NCAA/NIT retrospective pages, official Miami NCAA recaps, and protected-main physical venue reconciliation.

Postseason QA carried forward into Stage 4:

- H/A/N gaps: 0
- locality gaps: 0
- NCAA exact-site gaps: 0
- exact postseason venue resolved: 111/112
- researched-unresolved exact postseason venue: 1 (1952 NAIB District 25, DeLand, FL)

The historical regular-season neutral shortcut is not used to waive postseason research obligations.

## Accomplishment evidence

The Miami media guide program-history/season sections identify:

- 1999-2000 BIG EAST regular-season co-championship;
- 2012-13 ACC regular-season and ACC Tournament championships;
- 2022-23 ACC regular-season co-championship and first Final Four.

The accepted NCAA ledger spans 13 distinct appearance seasons after inclusion of the completed 2025-26 NCAA appearance. Stage 4 therefore supports the current project accomplishment baseline without mutating the shared accomplishment registry.

## Cross-source evidence and known inconsistencies

Accepted row-level notes preserve stronger-evidence reconciliation rather than hiding source disagreement. Important examples include:

- 2024 Tennessee event label: media-guide family label conflicts with exact-game Miami Jimmy V Men's Classic evidence; exact-game evidence controls the curated event/site.
- 2008 NCAA locality: guide wording says Little Rock; exact Alltel Arena evidence establishes North Little Rock.
- 1952 Florida State NAIB District 25: the accepted Stage 1 date is retained despite a one-day retrospective discrepancy; exact building remains researched unresolved.
- Historical arena naming: source-era names are preserved even when a current/main physical venue identity carries a different canonical display name.

The package preserves the explicit Miami-only owner locality disposition affecting 285 exhausted pre-1971 HOME rows. Stage 6 challenged the entire 286-row HOME-venue residual as a population and found no safe row-level building propagation. The Miami Beach Auditorium venue relationship is now explicitly marked row-specific so its first/last accepted assignments cannot be misread as a continuous chronology.

## Shared-reference authority and provenance limits

Research does not mutate protected-main global registries. Four venue identities remain historically resolved but globally pending: Dinner Key Auditorium, Miami Beach Auditorium, Santander Arena, and South Point Arena. Their numeric `venue_id` fields stay blank until serialized current-main rebase.

The required Stage 5 owner NON_D1 sanity scan was approved with no flags. Stage 6 adversarial self-challenge is complete and passed. Stage 7 immutable packaging has not begun and `RESEARCH_FROZEN` is not implied by this Stage 6 package.

## Exhibition treatment

Only recognized competitive varsity games in the accepted top-level scope are represented. Exhibition/scrimmage/noncompetitive rows are excluded rather than encoded as competitive games.


## Stage 6 targeted accepted-project challenge

Protected-main compare from immutable `research_base_sha` `5fa4d84e6b646a7c5e29f426905435c130caeee1` to Stage 6 protected main `953837e1da328fe4c8c99529b04ef91535194e4d` contains only Stage 3A-0 portable-tooling/policy files and no basketball data/reference or school source-game changes. Broad refetch of canonical/evidence datasets was therefore unnecessary for the defined challenge.

For the surviving neutral exact-building debt that already preserved published-reciprocal provenance, Stage 6 checked the exact protected-main reciprocal rows only. Clemson (`CLEM-R-1955-011`, `CLEM-R-1958-006`, `CLEM-R-1966-003`), TCU (`TCU-R-00850`), Stanford (`STAN-R-1716`), and Tennessee (`TENRAW-00812`, `TENRAW-01817`) remain locality-only. Michigan `MICHRAW-01588` explicitly supplies Sullivan Arena, Anchorage, AK, so Miami `MIA-S1-1987-001` is repaired to that venue and linked to protected-main `VEN-000361`.
