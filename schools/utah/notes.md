# Utah men's basketball — research portfolio notes

## Status

This is the **Stage 6 post-owner-scan research package** assembled from the accepted Utah Stage 1–4 state, the approved Stage 5 NON_D1 sanity scan, and the bounded final adversarial self-challenge.

- `research_base_sha`: `e5078cd6b57d68f59048f32b7dace422544eff9f`
- Program-perspective scope: `INCEPTION+`
- Competitive games: **3,047**
- Official-result aggregate: **1,924-1,123**
- Played seasons: **118**
- Exhibitions are excluded.
- Stage 4 six-file package QA: **PASS**
- Stage 5 owner `NON_D1` sanity scan: **APPROVED — 123 identities / 238 games / 0 flags**
- `PRE-FREEZE SELF-CHALLENGE: PASS`
- `RESEARCH_FROZEN: YES`
- `CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`
- Current-main/global reference rebase is required during serialized Implementation.

## Accepted game-universe corrections

Literal source evidence remains in `raw_text`; curated fields apply the accepted narrow corrections:

1. 1932-33 Stanford score order: source-impossible loss 41-37 -> **L 37-41**.
2. 2006-07 at BYU: source score order -> **L 62-85**.
3. 2019-20 Stanford: source result marker corrected -> **W 64-56 (OT)**.
4. 2021-22 UCLA: score order -> **L 58-63**.
5. 2024-25 Kansas: **W 74-67**, matching Utah's detailed season results.
6. 2024-25 College Basketball Crown duplicate-UCF publication defect: actual game is
   **2025-03-31 vs Butler, L 84-86**, MGM Grand Garden Arena.
7. 1909-10 at Butte 5W: administrative **2-0 forfeit win** retained as an administrative result;
   no separately evidenced played score is invented.
8. Stage 4 package QA exposed an impossible Provo/Einar-Nielsen physical-venue merge:
   - Utah-USC NCAA first round is normalized to **1960-03-07, Smith Fieldhouse, Provo, UT**;
     Utah's literal `03/08` / `Nielsen Field House` source evidence remains preserved.
   - Utah-Colorado State Skyline championship playoff on **1961-03-11** is normalized to
     **Smith Fieldhouse, Provo, UT**; literal Utah `Nielsen Field House` wording remains preserved.

## H/A/N and site completeness

All-game H/A/N:

- Utah home: **1,552**
- Opponent home: **1,162**
- Neutral: **333**
- Unknown: **0**

Home missing city/state: **0**.
Home rows missing exact venue: **40**, all explicitly
`RESEARCHED_UNRESOLVED_HOME_VENUE`; home publication blockers: **0**.

Neutral rows missing physical venue: **146**.
Neutral rows missing city/state: **58**.
Every residual neutral gap is explicitly researched/accounted; unaccounted neutral site gaps: **0**.

NCAA venue/city/state gaps: **0**.
Conference-tournament venue/location gaps: **0**.
NIT venue/location gaps: **0**.

Ten early other-postseason rows retain an explicit researched exact-building unknown:
seven National AAU games (1916/1919/1920) and three Western Division playoff games
(1932/1933/1937). Event and city/state remain established.

## Home facility chronology

- Pre-Deseret 1908-09/1909-10: HOME/Salt Lake City established; exact building unresolved.
- **Deseret Gymnasium**: primary home beginning 1910-11, including the documented WWII return.
- **Einar Nielsen Fieldhouse**: first Utah game 1940-01-09; later restored after the wartime interruption;
  final Utah game there 1969-02-22.
- 1946-47/1947-48 postwar transition: HOME/Salt Lake City established; exact building unresolved.
- **Jon M. Huntsman Center / Special Events Center physical building**: Utah's home beginning 1969-70.

## Postseason and conference-tournament history

Public competitive partition:

- Regular season: **2,842**
- Conference tournament: **79**
- NCAA Tournament: **70**
- NIT: **32**
- Other postseason: **24**

Utah's WAC tournament titles are preserved in 1995, 1997, and 1999; Mountain West titles in
2004 and 2009. The owner-authorized Utah tournament-site evidence corrects the 2013-16 Pac-12
Tournament physical site to **MGM Grand Garden Arena**, followed by T-Mobile Arena from 2017-24.

The expanded WAC workbook supplied on 2026-09-14 corroborates the Utah WAC site chronology from
1985-86 through 1998-99. Its 1983-84 and 1984-85 `entire tournament at shared venue` flags are
not applied to Utah because stronger Utah row-level evidence establishes campus-round structures:
1984 includes Salt Lake City then Albuquerque; 1985 includes two Salt Lake City games then El Paso.

## Opponent identity

Every game resolves to a canonical opponent identity.

- canonical opponent identities: **354**
- current-D1 identities: **231**
- historical/current-NON_D1 identities: **123**
- unresolved opponent identities: **0**
- known current-program key splits: **0**
- ambiguous current-program matches: **0**

The formal 123-identity `NON_D1` owner sanity scan is deliberately deferred to Stage 5.

## Conference chronology

- `State` — 1908-09 through 1923-24 (literal Utah source label; proposed `state-utah` global identity)
- Rocky Mountain Conference — 1924-25 through 1936-37
- Mountain States Conference / Utah source terminology `Skyline` — 1937-38 through 1961-62
- WAC — 1962-63 through 1998-99
- Mountain West — 1999-00 through 2010-11
- Pac-12 — 2011-12 through 2023-24
- Big 12 — 2024-25 onward

The proposed historical `state-utah` identity is **RESOLVED in the Utah source sense** but
**global registration is PENDING_CURRENT_MAIN_REBASE**. No unsupported expanded conference name
has been invented.

## Physical venue identity

This Stage 4 package contains **64** local physical venue relationships:
**59 research-base reuses** and
**5 genuinely new Utah-package candidates**.

New candidates carried with provisional transport IDs are:

- Deseret Gymnasium — Salt Lake City, UT
- Einar Nielsen Fieldhouse — Salt Lake City, UT
- Robertson Memorial Fieldhouse — Peoria, IL
- Donald W. Reynolds Center — Tulsa, OK
- Landers Center — Southaven, MS

Research-base same-building aliases are normalized rather than multiplied, including
American Airlines Arena -> Kaseya Center, San Jose Arena -> SAP Center,
NRG Stadium -> Reliant Stadium, Roberts Stadium -> Roberts Municipal Stadium,
and source-era names for Ball Arena/Crypto.com Arena/Honda Center.

Madison Square Garden is correctly split into the 1925-1968 and 1968-present physical buildings.
Kansas City Municipal Auditorium uses the established `VEN-000143` identity rather than creating
another copy of the known research-base duplicate representation.

All numeric/global venue IDs remain subject to authoritative current-main Implementation rebase.


## Stage 6 adversarial self-challenge

`PRE-FREEZE SELF-CHALLENGE: PASS`

The final bounded challenge targeted the largest residual classes rather than restarting Utah research.

### H/A/N repairs

Two literal `vs.` rows were exposed as true opponent-home games:

- **2005-12-22 Washington State** — Utah was the visitor in Washington State's contracted Seattle home game at KeyArena.
- **2014-12-13 Kansas** — Kansas Athletics explicitly states Kansas played host to Utah at Sprint Center; the physical building is the current T-Mobile Center identity.

Final all-game H/A/N is therefore:

- Utah HOME: **1,552**
- OPPONENT_HOME: **1,164**
- NEUTRAL: **331**
- UNKNOWN: **0**

### Neutral-site systematic recovery

The self-challenge attacked the modern neutral-site debt as one high-yield population.
It recovered **41 previously blank neutral physical venues** across recurring/event evidence,
plus the Washington State/Kansas H/A/N corrections above. Recovered events include the
1994/1998/2002 Maui Invitational, 1996/2000 Wooden Classic, 1997/1998 Great Eight,
2000 Puerto Rico Shootout, 2001 Southwest Showdown, 2003 Preseason NIT,
2004 Great Alaska Shootout, 2006 San Juan Shootout, 2007 NIT Season Tip-Off,
2008 Glenn Wilkes Classic, 2009 Las Vegas Invitational, 2010 Diamond Head Classic,
2011 Battle 4 Atlantis, the 2015 Duke game at Madison Square Garden, and the 2017
MGM Resorts Main Event/Beehive Classic.

Surviving neutral exact-building debt:

- physical venue blanks: **105**
- location blanks: **44**
- modern (1990+) venue blanks: **0**
- modern (1990+) location blanks: **0**
- unaccounted neutral material gaps: **0**

The surviving building debt is now entirely pre-1990 and explicitly researched/accounted.
No comparable systematic modern event-source class remains. It is classified as terminal
researched historical debt rather than being filled by arena-era inference.

### HOME venue exception challenge

`RESEARCHED_UNRESOLVED_HOME_VENUE` final count: **40**.

The population remains narrowly concentrated in the already-identified transition classes:
1908-09/1909-10 before the Deseret Gym chronology is safely established, and 1946-47/1947-48
during the postwar return transition. University institutional history confirms Nielsen opened
in 1939/dedicated in 1940, served as Utah basketball's historic home, and was converted to Army
housing during WWII; Utah Athletics gives the first Nielsen game as 1940-01-09 and the final
one as 1969-02-22. Those broad histories do not safely establish each individual transition-era
home game's building, and known wartime exceptions demonstrate why blanket back-projection is
unsafe.

Home city/state blanks: **0**.
Home publication blockers: **0**.
No Stage 6 home row was converted from an explicit researched unknown to unsupported certainty.

### Exact dates

Unknown exact dates: **0**. No residual date debt remains.

### Venue physical identities

Local physical venue relationships after the Stage 6 recoveries: **74**.
The five Stage 4 new candidates remain the only genuinely new physical venue candidates:
Deseret Gymnasium, Einar Nielsen Fieldhouse, Robertson Memorial Fieldhouse,
Donald W. Reynolds Center, and Landers Center. Research-base search found no existing
same-physical entries for those names. Ambiguous physical identities: **0**.

Stage 6 introduced no additional new global physical identities; all recovered modern sites
reuse established research-base venue identities.

### Opponent identities

The owner approved the complete **123-identity / 238-game NON_D1 scan with no flags**.
The accepted Stage 2 identity work remains intact:

- unresolved opponent identities: **0**
- known current-program key splits: **0**
- ambiguous current-program matches: **0**
- modern NON_D1 identities specifically reviewed in Stage 2: **15**

No Stage 6 evidence exposed a reason to reopen an accepted opponent identity.

### Final Stage 6 acceptance state

- research package structural QA: PASS
- UNKNOWN H/A/N: 0
- HOME publication blockers: 0
- NCAA site gaps: 0
- conference-tournament site gaps: 0
- NIT site gaps: 0
- unaccounted neutral material site gaps: 0
- ambiguous physical venue identities: 0
- owner NON_D1 scan: APPROVED
- PRE-FREEZE SELF-CHALLENGE: PASS


## Research freeze

This six-file portfolio completed the bounded Research protocol through Stage 7.

- `RESEARCH_FROZEN: YES`
- `CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`
- Research freeze does not authorize repository integration.
- Provisional/global shared identities must be reconciled against then-current protected `main`
  before tracked Phase 0.

## Current-main Integration reconciliation

The immutable RESEARCH_FROZEN artifact remains the accepted historical evidence.
This Integration copy was reconciled mechanically against protected main before
INTEGRATION_FROZEN:

- `utah-einar-nielsen-fieldhouse` was remapped to current-main shared identity
  `nielsen-fieldhouse` (Nielsen Fieldhouse / Einar Nielsen Fieldhouse).
- `donald-w-reynolds-center` was remapped to current-main shared identity
  `reynolds-center` (Reynolds Center / Donald W. Reynolds Center).
- Paradise, Nevada arena geography was normalized to the project's current
  shared-reference convention `Las Vegas, NV` for MGM Grand Garden Arena,
  Orleans Arena, and T-Mobile Arena; 26 Utah source-game rows received the same
  normalized-location treatment.
- The frozen MGM Grand Garden Arena alias field incorrectly cross-linked
  T-Mobile Arena and T-Mobile Center, which are separate physical venues on
  current main; those invalid aliases were removed from the Integration copy.
- Pipe-delimited same-physical aliases for Hec Edmundson Pavilion and Honda
  Center were normalized to the current semicolon-delimited package contract.

- Legacy `YYYY-YY` source-game and opponent season labels were expanded
  mechanically to the current `YYYY-YYYY` package contract.
- Legacy unpaired `site_research_basis` provenance on 2,902 otherwise
  non-gap rows was preserved in each row's general `notes` field and removed
  from the gap-specific paired research-status fields.

These are current-main identity/schema reconciliations only. No accepted Utah
game universe, H/A/N adjudication, score, opponent identity, postseason
classification, or Research conclusion was reopened.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=9738fe4f54b813aad4d2a12344a2c8279c3590ee` from `research_base_sha=e5078cd6b57d68f59048f32b7dace422544eff9f`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

## Stage 2 deterministic current-main normalization

Before Owner Gate 1, the comprehensive current-main sweep identified and
mechanically corrected deterministic package drift:

- research-base keys `florida-a-and-m`, `prairie-view-a-and-m`, and
  `texas-a-and-m` were rebased to current project keys `florida-a-m`,
  `prairie-view-a-m`, and `texas-a-m`;
- stable current project opponent displays were normalized to `CSUN`,
  `Mizzou`, `UNC Asheville`, and `Penn`, while literal Utah source labels
  remain preserved;
- the 32 competitive 2025-26 supplement rows were reworded from the
  game-level phrase `exhibitions excluded` to `non-countable contests
  excluded` solely to avoid a generic substring false positive.
  `source-notes.md` continues to preserve the explicit Research conclusion
  that Nevada (2025-10-17) and Oregon (2025-10-24) were exhibitions and were
  excluded.

No game identity, score, date, H/A/N, physical venue, postseason
classification, or accepted Research adjudication was changed.

## Stage 2 current-source normalization challenge

The required Implementation pre-Gate adversarial sweep compared presently
detectable modern normalized values against Utah Athletics' current official
schedule/result surfaces. Eight source rows contained deterministic
record-book/extraction drift and were corrected in curated fields while their
frozen `raw_text` remains unchanged:

- 2007-12-08 Oregon: normalized from OPPONENT_HOME with blank site metadata
  to NEUTRAL at the Rose Garden / current project physical identity Moda
  Center, Portland, Oregon. Utah's current schedule and opponent history
  explicitly classify the Pape Jam game as neutral.
- 2009-03-08 TCU date -> 2009-03-07.
- 2016-03-05 Colorado score 77-75 -> 57-55.
- 2022-02-12 Colorado score 77-81 -> 76-81.
- 2022-11-07 LIU score 93-58 -> 89-48. Utah's current schedule shows
  93-58 as the excluded Nov. 2 Westminster exhibition, not the LIU result.
- 2022-11-15 Sam Houston date -> 2022-11-17.
- 2022-11-20 Georgia Tech date -> 2022-11-21.
- 2022-11-21 Mississippi State date -> 2022-11-23.

Authoritative Utah Athletics current-source surfaces used:
- https://utahutes.com/sports/mens-basketball/schedule/2007-08
- https://utahutes.com/sports/mens-basketball/schedule/2008-09
- https://utahutes.com/sports/mens-basketball/schedule/2015-16
- https://utahutes.com/sports/mens-basketball/schedule/2021-22
- https://utahutes.com/sports/mens-basketball/schedule/2022-23

These corrections do not alter the accepted competitive-game universe.
They repair demonstrable normalized date/score/site defects before Owner
Gate 1 and preserve the literal frozen Research evidence.

## Stage 2 historical opponent display normalization

The disposable pre-Gate publication challenge exposed four historical
non-current opponent keys whose Utah normalized display differed from an
already-published project display. Identity keys and literal Utah source
labels were unchanged.

- `pacific-oregon`: `Pacific (OR)` -> `Pacific (Oregon)`
- `st-francis-illinois`: `St. Francis (IL)` -> `St. Francis (Ill.)`
- `st-thomas-florida`: `St. Thomas (FL)` -> `St. Thomas University (FL)`
- `westminster-utah`: `Westminster (UT)` -> `Westminster`

Each replacement was mechanically verified against an existing published
school package before mutation. No basketball fact or opponent identity
changed.

## Stage 2 predicted-publication site blocker repair

The disposable predicted-state site gate exposed two inherited HOME
canonical gaps.

`CBBG-0068010` / `UTA-S1-00361`:
Utah Athletics' current USC series history explicitly places the first
meeting on 1934-01-05 in San Francisco, with Utah losing 32-43. USC's
institutional year-by-year history instead records its 1934 Utah meeting
as a 40-35 USC win on Dec. 21. Both institutional histories treat this
as the first meeting, so the records are retained as conflicting evidence
for one game rather than manufactured into two games. The explicit San
Francisco location establishes NEUTRAL H/A/N; exact physical venue remains
unsupported after the completed site research. The earlier Stage 2
HOME/Deseret interpretation was incorrect and is superseded by this
current-source correction. Date and score remain for Owner Gate 1.

`CBBG-0079219`:
Washington's published reciprocal source establishes the 1970-12-19
89-78 game as at Utah. Washington Athletics later explicitly identifies
that meeting as having been played in the Huntsman Center in Salt Lake
City. The existing canonical game was enriched to global physical venue
`VEN-000097` / `jon-m-huntsman-center`, Salt Lake City, Utah.

No new competitive game was created by either correction.
