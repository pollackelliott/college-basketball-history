# Colorado men's basketball — research portfolio notes

## Status

This is the Stage 6 post-owner-scan research package assembled from the accepted Colorado Stage 1–3B working state and the bounded final adversarial self-challenge.

- `research_base_sha`: `724c45e8d2d92a2a8cfc1e6174eeeb90de8bebda`
- Program-perspective scope: `INCEPTION+`
- Competitive games: **2,768**
- On-court record: **1,456-1,312**
- Played seasons: **123**
- No team: **1942-43, 1943-44**
- Exhibitions are excluded.
- The required owner `NON_D1` sanity scan is **APPROVED** (71 identities / 237 games; no flags).
- `PRE-FREEZE SELF-CHALLENGE: PASS`.
- This package is **not RESEARCH_FROZEN yet**; immutable packaging/hash is reserved for Stage 7.
- Current-main/global identity rebase is required during serialized Implementation. Research-time numeric IDs for new physical venues are provisional transport provenance only.

## Accepted game-universe corrections

Literal source evidence remains in `raw_text`; the curated fields apply these narrow corrections:

1. **1919-02-28 at Colorado College** — the record book prints impossible `F 29`; Colorado's opponent-history evidence gives February 28.
2. **1920-21 vs Colorado College** — the record book prints `W 32-36`; Colorado's official schedule gives `W 36-32`, consistent with the 8-0 season.
3. **1933-12-22 and 1933-12-23 at Kansas Teachers** — Pittsburg State reciprocal records establish December 22-23, 1933 rather than the March dates printed by Colorado.
4. NCAA date repairs supported by official NCAA bracket history:
   - Stanford: **1942-03-21**
   - Bradley: **1954-03-12**
   - Rice: **1954-03-13**
5. **1985-03-06 at Iowa State** — Big Eight quarterfinal was an Iowa State home game at Hilton Coliseum, not a Kansas City neutral game.
6. **2025-26 overtime metadata** — Colorado's completed schedule explicitly identifies Eastern Washington (2025-11-08), BYU (2026-02-14), and Oklahoma in the College Basketball Crown (2026-04-01) as overtime games.
7. **1931-01-02 and 1931-01-03 vs Kansas** — Kansas official schedule/opponent history establishes both as Kansas away games at Colorado in **Denver**, not neutral Kansas City. Colorado's literal source wording remains preserved. The Jan. 3 score is corrected from Colorado's printed 29-36 to **28-36**, matching Kansas's official history.
8. **1998-11-28 vs American (P.R.)** — Colorado's current official 1998-99 schedule and the Puerto Rico Shootout event chronology establish November 28 rather than the November 29 date printed in the record-book row.


## Administrative-result note

Colorado's guide reports 1960-61 as **15-10 on court**, then separately records a later Big Eight administrative ruling that converted seven wins to forfeits and revised the official standing to 8-17. Project game results preserve the on-court outcomes. Because the source does not support a safe row-level identification of the seven forfeited wins in this research state, no individual game is rewritten merely to reproduce the administrative season record.

## Postseason classification

Final competitive partition:

- Regular season: **2,621**
- Conference tournament: **83**
- NCAA Tournament: **31**
- NIT: **26**
- Other postseason: **7**

The seven generic `POSTSEASON` games are the three-game 1930 Rocky Mountain Conference championship playoff series, two CBI games, and two College Basketball Crown games.

### 1930 Rocky Mountain Conference playoff series

Colorado played Montana State on March 10-12, 1930 after winning the Rocky Mountain Conference Eastern Division. Montana State historical evidence describes the series as the league playoffs. Contemporary season summaries state there was **no conventional conference tournament**. Accordingly:

- event: `Rocky Mountain Conference Championship Playoff Series`
- public game type: `POSTSEASON`
- **not** `CONFERENCE_TOURNAMENT`
- site: Romney Gym, Bozeman, Montana
- H/A/N: opponent home

No other pre-1950 conventional Colorado conference tournament was found.

## H/A/N and site completeness

Final all-game H/A/N after the Stage 6 reciprocal challenge:

- Colorado home: **1,325**
- Opponent home: **1,141**
- Neutral: **302**
- Unknown: **0**

The H/A/N change is limited to the two January 1931 Kansas games, which Kansas's official history identifies as away games at Colorado in Denver.

Regular-season home publication blockers: **0**. Two off-campus Colorado HOME games (Kansas, Jan. 2-3, 1931) retain an exact-building unknown under the dedicated `RESEARCHED_UNRESOLVED_HOME_VENUE` exception; Denver and true Colorado HOME status are established independently, but no reviewed game-specific source safely identifies the physical building.

All 31 NCAA Tournament games have complete physical venue, city, and state.

Only **four neutral games** retain a researched physical-building unknown: Missouri/Utah in Denver (1936), Missouri in Kansas City (1944), and Oklahoma State in Tulsa (1952). All have complete city/state plus paired `RESEARCHED_PARTIAL` provenance. Together with the two 1931 HOME venue-only unknowns, final material site-gap rows are **6**, all researched/accounted; unaccounted material site gaps: **0**.

## Colorado home facility chronology

- **University Gymnasium**, Boulder — 1901-02 through 1923-24
- **Carlson Gymnasium** (1924 Men's Gymnasium physical building), Boulder — 1924-25 through 1935-36
- **Balch Fieldhouse** (earlier CU Fieldhouse), Boulder — 1936-37 through 1978-79
- **CU Events Center**, Boulder — 1979-80 onward

Venue chronology is enrichment only after independent H/A/N classification.

## Physical venue identity

The package uses research-base physical venue identities when exact identity is already established and assigns provisional `VEN-990xxx` IDs only to genuinely new research candidates. After Stage 6, there are **69 local physical venue relationships: 56 research-base reuses and 13 genuinely new candidates**. The new candidates are:

- Balch Fieldhouse
- Carlson Gymnasium
- Coliseo de Puerto Rico
- Connolly Center
- Denver Auditorium
- Denver Coliseum
- Halton Arena
- Moby Arena
- Ocean Center
- Romney Gym
- Sun Devil Gymnasium
- University Gymnasium
- Vines Center

Stage 6 specifically avoided two duplicate-physical-identity mistakes: the 1998 Boston University game at source-era **Worthington Arena** reuses research-base **Brick Breeden Fieldhouse** because Montana State identifies Worthington as the basketball arena inside that physical building; and the 1969 Lobo Classic reuses the established Albuquerque **The Pit** physical identity rather than creating a new `University Arena` venue.

Two research-base duplicate-representation issues are explicitly carried for serialized current-main rebase rather than multiplied:

- Kansas City Municipal Auditorium: Colorado uses `VEN-000143` / `municipal-auditorium-kc`; research base also contains `VEN-000410`.
- The Pit in Albuquerque: Colorado uses `VEN-000208` / `the-pit`; research base also contains `VEN-000427`.

These are Integration rebase items, not unresolved historical physical identities.

## Conference chronology

- Independent — 1901-02 through 1908-09
- Rocky Mountain Conference — 1909-10 through 1936-37
- Mountain States Conference — 1937-38 through 1946-47
- Big Seven — 1947-48 through 1957-58
- Big Eight — 1958-59 through 1995-96
- Big 12 — 1996-97 through 2010-11
- Pac-12 — 2011-12 through 2023-24
- Big 12 — 2024-25 onward

The Rocky Mountain and Mountain States historical identities are not present in the research-base global conference registry and therefore remain explicit current-main registration/rebase work for serialized Implementation. They are not silently collapsed into another conference.

## Accomplishment cross-check

The research-base owner baseline for Colorado is:

- Conference regular-season championships: **19**
- Conference tournament championships: **1**
- NCAA Tournament appearances: **16**
- Final Four appearances: **2**
- National championships: **0**
- Best NCAA finish: **Final Four (1955)**

The assembled game ledger independently reproduces **16 distinct NCAA appearance seasons**, two Final Four seasons under the project's controlled historical round semantics, and exactly one conference-tournament championship win (2012 Pac-12 Tournament). The institutional season history contains the underlying conference-title seasons and does not contradict the owner baseline of 19 regular-season league championships.

## Opponent identity

All 2,768 games have resolved opponent identities.

- Current-D1 opponent games: **2,531**
- Current-D1 canonical opponents: **226**
- `NON_D1` opponent games: **237**
- Distinct `NON_D1` identities: **71**
- Unresolved opponent identities: **0**
- Known current-program key splits: **0**
- Ambiguous current-program matches: **0**

The complete owner `NON_D1` sanity scan was approved in Stage 5 with no flagged rows. Stage 6 additionally challenged all 11 `NON_D1` identities with games in 2000-01 or later against the research-base current-D1 registry; none is an exact current-D1 key, and no current-program split or ambiguous current-program match was exposed.


## Stage 6 adversarial self-challenge

`PRE-FREEZE SELF-CHALLENGE: PASS`

The challenge targeted the portfolio's actual largest/suspicious residuals instead of restarting settled research.

- `RESEARCHED_UNRESOLVED_HOME_VENUE`: **2** final rows, both Jan. 1931 Kansas games in Denver. Reciprocal Kansas evidence recovered true Colorado HOME status and corrected the Jan. 3 score, but exact Denver building remains unsupported.
- `UNKNOWN` H/A/N: **0**.
- Unknown exact dates: **0** after correcting the 1998 American (P.R.) Puerto Rico Shootout game to Nov. 28.
- Neutral-site debt: reduced from **18** researched-partial building blanks to **4**.
- Physical venue relationships: **69** = **56** research-base reuses + **13** new candidates; ambiguous physical identities: **0**.
- Opponent identities: owner-approved `NON_D1` population **71 / 237 games**; 11 modern `NON_D1` identities separately challenged; known current-program key splits **0**; ambiguous current-program matches **0**.
- NCAA physical venue + city + state gaps: **0 / 31**.
- Unaccounted material site gaps: **0**.
- HOME publication blockers: **0**.

Stage 6 exact-building recoveries:
- 1965 Sun Devil Classic: Sun Devil Gymnasium (2 games)
- 1969 Lobo Classic: The Pit (2)
- 1981 Las Vegas event: Las Vegas Convention Center (1)
- 1987 Mile High Classic: Denver Coliseum (1)
- 1989 Early Season Tournament: Lahaina Civic Center (2)
- 1998 Puerto Rico Shootout: Eugenio Guerra Sports Complex (3)
- 1998 Montana State Invitational: Worthington Arena naming evidence reconciled to the Brick Breeden Fieldhouse physical identity (1)

No Stage 6 repair changes the accepted 2,768-game universe or the 1,456-1,312 on-court record.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=bb2fcf16dd8800e3d9b823c0b4999b2d1b516d6b` from `research_base_sha=724c45e8d2d92a2a8cfc1e6174eeeb90de8bebda`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
