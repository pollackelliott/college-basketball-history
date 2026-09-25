# Virginia source notes

## Source hierarchy

1. Owner-supplied **2025-26 Virginia Men's Basketball record book / media guide**.
2. Virginia Athletics official schedules, recaps, game notes, all-time series, venue history, and postseason history.
3. Accepted protected-main reciprocal/project evidence from already-published school packages and global venue references.
4. Owner-maintained conference-tournament site reference, consumed only after postseason classification was independently established and only within its documented authority.
5. NCAA, conference, host, participant, and event institutional sources for bounded site/identity gaps.
6. Targeted archival/secondary evidence only where current Research policy explicitly permitted it.

## Primary institutional source

**2025-26 Virginia Men's Basketball Record Book**, Virginia Athletics, owner supplied.

Durable Stage 3A source register SHA-256 for the supplied record-book artifact:
`16be58797aef8dbb8eaf2087c56e86c2b10384180c1ebc5c0b63b768858f3a32`

The year-by-year results on pp. 84-94 form the row-level historical spine through 2024-25. Coaching records, all-time series, postseason tables, facility material, and source footnotes are cross-check/enrichment layers rather than silent replacements.

## Completed 2025-26 supplement

Virginia's official completed 2025-26 schedule/results page supplies the project endpoint omitted from the record book's historical year-by-year section:

`https://virginiasports.com/sports/mbball/schedule/season/2025-26`

The supplement contributes **36 competitive games** and excludes two preseason exhibitions. A Stage 3A partition defect caused by the literal schedule marker `ACC` was mechanically repaired: 18 ordinary ACC regular-season games were restored to Stage 3A while five genuine 2025-26 postseason games remained in Stage 3B.

## Stage 1 universe

The accepted competitive universe contains **3,026** source assertions. Literal row evidence is preserved in `raw_text`.

Accepted Stage 1 correction overlays are documented in the durable research artifacts and summarized in `notes.md`; no correction erases the source wording that made the defect auditable.

## Opponent sources and identity work

Stage 2 used the Virginia institutional all-time opponent/series evidence, current project program registry, published reciprocal packages where useful, and bounded historical identity research.

The package preserves **93** working distinct `NON_D1` identities for the required owner sanity scan. The separate informational self-corrected list contains **84** source-label families normalized without owner intervention.

## Regular-season H/A/N and venue sources

H/A/N is based on explicit/game-level evidence and accepted reciprocal evidence, never inferred from venue geography.

Key Virginia facility sources include:

- Virginia Athletics, **Virginia Men's Basketball: University Hall / Earlier Basketball Venues**:
  `https://virginiasports.com/news/2010/08/03/virginia-men-s-basketball-university-hall`
- Virginia Athletics, **Men's Hoops Battles Delaware Dec. 27**:
  `https://virginiasports.com/news/1999/06/21/men-s-hoops-battles-deleware-dec-27`
- Virginia Athletics, **John Paul Jones Arena** and official 2025-26 game notes:
  `https://virginiasports.com/john-paul-jones-arena`

Those sources establish the accepted Fayerweather -> Memorial Gymnasium -> University Hall -> John Paul Jones Arena chronology. Chronology is applied only after HOME classification is independently settled.

Modern neutral-site research used target/event/host/participant institutional sources and current project venue identities. Historical 1995-96-and-earlier neutral rows received the repository-authorized location-first enrichment pass; once supported city/state was established, research did not open a second source path solely to recover a building.

## Conference-tournament source

Protected main at the research base contains the owner-maintained conference-tournament site snapshot:

- `docs/conference-tournament-site-reference.md`
- `data/reference/conference-tournament-sites.csv.gz.b64`
- `tools/conference_tournament_reference.py`

The reference was used as site evidence only after Virginia's own source evidence established a confirmed conference-tournament game. It never established H/A/N or postseason classification.

For the Feb. 24, 1933 Virginia-Duke Southern Conference Tournament game, the shared reference conflicted with Duke's accepted reciprocal and institutional evidence. The owner explicitly selected **Raleigh Memorial Auditorium**. The shared reference itself remains unchanged and the conflict is preserved as maintenance debt.

## NCAA / NIT / other postseason sources

Virginia's institutional postseason history establishes game identity, round, and site city. NCAA/host/participant institutional site evidence was then used at edition/site-block level to establish exact physical buildings. Exact physical identities were reconciled against protected-main venue references.

Final Stage 3B site coverage:

- Conference tournament: 130 / 130 exact sites
- NCAA Tournament: 62 / 62 exact sites
- NIT: 31 / 31 exact sites
- CBI / other postseason: 3 / 3 exact sites

NCAA controlled round labels follow repository policy. NIT, conference-tournament, and generic POSTSEASON rounds are blank except verified championship games; literal source-round wording is retained separately.

## Venue identity and shared-reference boundary

Stage 4 rechecked all exact physical venue identities against protected `main` at:
`5c91e35485060a0be27f9612d0b140883a555dbf`.

The six-file package reuses exact current-main `venue_key` / `venue_id` values where a physical identity is already registered. Ten historically resolved physical sites remain new candidates with blank research-time numeric `venue_id`; serialized Implementation must assign authoritative IDs after a fresh current-main rebase.

Research does not mutate `data/reference/venues.csv`, `venue-names.csv`, or the conference-tournament shared reference.

## Source inconsistencies and preserved debt

Research preserves supported conflicts rather than flattening them. Examples include:

- the 1933 Raleigh Memorial Auditorium vs. Thompson Gym shared-reference conflict, resolved for Virginia by owner disposition while preserving global maintenance debt;
- known non-site date discrepancies listed in `notes.md`;
- historical regular-season neutral rows where a locality but not exact building is supportable;
- two 2009 Cancun Challenge rows where Moon Palace Resort / Cancun is supported but the exact ballroom is not.

Unsupported certainty is not introduced to make package QA pass.

## Stage 4 status

The six-file portfolio is a Research artifact. The required Stage 5 owner `NON_D1` sanity scan was **APPROVED on 2026-09-24** with no flagged identities. Final freeze still requires the Stage 6 adversarial self-challenge to pass.

## Stage 6 evidence additions

The pre-freeze self-challenge used only bounded, high-yield evidence classes and did not restart completed
Stage 3A/3B research.

Official reciprocal sources used for the Stage 6 date/site challenge:

- Washington & Lee men's basketball opponent history vs. Virginia:
  `https://generalssports.com/sports/mens-basketball/opponent-history/university-of-virginia/52`
- Virginia Tech men's basketball Virginia series history:
  `https://stats.hokiesports.com/mbasketball/opponents/Virginia`
- Virginia Tech historical schedule:
  `https://stats.hokiesports.com/mbasketball/records/schedule.html`
- VMI men's basketball opponent history vs. Virginia:
  `https://vmikeydets.com/sports/mens-basketball/opponent-history/university-of-virginia/7`

The VMI source's early `11/1` and `12/1` entries were treated as non-unique placeholder-like dates rather
than authoritative month/day evidence. The George Washington institutional source family was also challenged;
its obvious historical material did not support a comparable systematic exact-date recovery for Virginia's
remaining early blanks.

`UVA-R-1974-007` was repaired to 1975-01-04 because the preserved Virginia literal row itself contains the
`J 4` date token and Clemson's reciprocal schedule independently matches Virginia's 68-86 loss on that date.
The Clemson opponent identity was retained.

The two surviving 2009 Cancun neutral rows were challenged again. Target/participant evidence supports
Moon Palace Resort and Cancun, Mexico, but does not safely establish an exact physical contest room. They
remain `RESEARCHED_PARTIAL`; no current ballroom name is back-projected.

Current-main drift was challenged only where the post-research-base delta could matter to Virginia:
new Oregon State shared venue registrations, the Oregon State published source/opponent package, and the
program-registry delta. No Virginia shared-identity collision or opponent-key split was exposed.

Stage 6 package QA passed with zero errors and zero warnings. Stage 7 / final `RESEARCH_FROZEN` sealing is
still pending owner `Proceed`.

## Stage 7 immutable Research Freeze

Stage 7 sealed the Stage 6-accepted six-file portfolio after final verification. The only six-file
portfolio edits made during Stage 7 are these Research Freeze status annotations in `notes.md` and
`source-notes.md`; all row-level basketball facts, identities, research-accounting fields, and residual
debt conclusions are byte-identical to the Stage 6 accepted data files.

`RESEARCH_FROZEN: YES`  
`CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`

