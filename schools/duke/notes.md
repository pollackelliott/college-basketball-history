# Duke men's basketball — Stage 6 complete research working portfolio notes

## Status

This is the repaired six-file research working package after completion of Duke Research Stage 6.

- `research_base_sha`: `bb2fcf16dd8800e3d9b823c0b4999b2d1b516d6b`
- Current protected-main SHA at Stage 4 assembly: `541c188c7e57035b2edb20b66323c1912ccabac6`
- Program-perspective scope: `INCEPTION+`
- Competitive games: **3,306**
- On-court record: **2,370-936**
- Varsity history begins: **1905-06**
- Exhibitions are excluded.
- Stage 6 pre-freeze research acceptance: **PASS**
- Owner-approved `NON_D1` scan population after the Stage 6 Charlotte correction: **73 identities / 261 games**
- The original 72 identities / 257 games remain covered by the preserved Stage 5 approval; the one new `Charlotte (historical team)` identity (4 games, 1909-10 through 1910-11) was explicitly owner-approved on 2026-09-11.
- Stage 6 is **COMPLETE**, but this working package is **not yet RESEARCH_FROZEN**; immutable packaging is the separately bounded Stage 7.
- Current-main/global venue identity rebase remains required during serialized Implementation. Research-time `VEN-990xxx` IDs are provisional transport provenance only.

## Final game partition

After the accepted 1947 partition correction:

- Regular season: **2,898**
- Conference tournament: **225**
- NCAA Tournament: **172**
- NIT: **11**

The one Stage 3A mechanical defer error is `DUKE-PRINT-00781` (1947-02-28 vs North Carolina), which is curated as a regular-season Duke HOME game. Literal prior-stage/source evidence remains preserved in `raw_text` and supporting correction provenance.

## H/A/N and site completeness

Final all-game H/A/N:

- Duke home: **1,324**
- Opponent home: **1,131**
- Neutral: **706**
- Unknown: **145**

Research/package site census:

- source-program HOME missing venue: **0**
- source-program HOME missing city/state: **0**
- UNKNOWN H/A/N rows: **145**, all with explicit `RESEARCHED_UNRESOLVED` accounting
- neutral rows missing exact venue: **67**
- neutral rows missing city/state: **59**
- material researched site-gap rows: **212**
- unaccounted material site-gap rows: **0**
- conference-tournament/NIT site gaps: **0**
- NCAA Tournament physical venue + city + state gaps: **0 / 172**

Historical uncertainty is preserved rather than inferred. Away regular-season building/location blanks are not publication blockers under project policy.

## Duke home-facility chronology

- **Angier B. Duke Gymnasium**, Durham — 1905-06 through 1922-23
- **Alumni Memorial Gymnasium**, Durham — 1923-24 through 1929-30
- **Card Gym**, Durham — 1930-31 through 1938-39
- **Cameron Indoor Stadium** (historical Duke Indoor Stadium), Durham — 1939-40 onward

Venue chronology is enrichment only after independent H/A/N classification.

## Physical venue identity

The Stage 6 repaired package contains **95** distinct local physical venue relationships:

- **80** research-base/current-main registry reuses
- **15** genuinely new/provisional research identities (`VEN-990001` through `VEN-990015`)
- ambiguous physical venue identities: **0**

Stage 4 performed only mechanical research-base identity reconciliation. In particular:

- historical **Duke Indoor Stadium** reuses the Cameron Indoor Stadium physical identity `VEN-000035`;
- Maryland's **The Gymnasium** reuses `VEN-000327`;
- Georgia's **Woodruff Hall** reuses `VEN-000279`;
- **Raleigh Memorial Auditorium** remains a distinct new researched physical identity and is not merged with `VEN-000328` Thompson Gym;
- the earlier **Raleigh Auditorium** row remains a separate research identity rather than being collapsed into the later Memorial Auditorium without evidence.

All provisional global numeric IDs must be rebased against then-current protected `main` during serialized Implementation.

## Accepted Stage 3B correction overlays

Literal source evidence remains in `raw_text`; curated fields apply the accepted narrow corrections:

1. **1967-03-11 vs North Carolina** — official ACC history establishes North Carolina 82, Duke 73 in the ACC championship at Greensboro Coliseum; the inherited literal `73-83` row is preserved in `raw_text`.
2. **1947-02-28 vs North Carolina** — regular-season Duke HOME game, not postseason; the mechanically inherited Stage 3A defer is preserved only in provenance.
3. **2007-03-08 vs NC State** — curated Neutral at St. Pete Times Forum / Benchmark International Arena; Duke's current schedule rendering as Away is preserved as conflicting source evidence.
4. **1993 NCAA games vs Southern Illinois and California** — curated Rosemont Horizon/Allstate Arena, Rosemont, Illinois; Duke's Chicago shorthand is preserved.
5. **1978 NCAA games vs Pennsylvania and Notre Dame** — physical sites corrected to Providence Civic Center and The Checkerdome/St. Louis Arena respectively; Duke archived schedule geography remains preserved.

## Conference chronology

- Independent — 1905-06 through 1927-28
- Southern Conference — 1928-29 through 1952-53
- ACC — 1953-54 onward

The `southern` and `acc` identities already exist in the research-base conference registry.

## Accomplishment cross-check

Research-base Duke accomplishment baseline:

- Conference regular-season championships: **25**
- Conference tournament championships: **29**
- NCAA Tournament appearances: **48**
- Final Four appearances: **18**
- National championships: **5**
- Best NCAA finish: **National Champion (2015)**

The assembled game ledger independently reproduces:

- **48** distinct NCAA appearance seasons
- **18** Final Four seasons
- **5** NCAA championship wins
- **29** conference-tournament championship wins

The accepted Duke conference/history evidence does not contradict the owner baseline of 25 regular-season conference championships. Formal accomplishment verification/decision remains part of the later onboarding workflow.

## Opponent identity

All bona fide opponents are resolved.

- Current-D1 opponent games: **3,047**
- Current-D1 canonical opponent identities: **246**
- `NON_D1` opponent games: **257**
- Distinct `NON_D1` identities: **72**
- Aggregate-source placeholder games with no bona fide opponent identity: **2**
- Unresolved normal opponent identities: **0**
- Known current-program key splits: **0**
- Ambiguous current-program matches: **0**

The complete Stage 4 owner-scan presentation is preserved separately in the Stage 4 checkpoint. Its 72 identities and game counts match the previously approved Duke owner scan exactly.

## Stage 4 boundary

`STAGE 4: COMPLETE — OWNER NON_D1 SANITY SCAN READY`

No Stage 5 action or final adversarial self-challenge has been performed in this Stage 4 turn.

## Stage 6 adversarial self-challenge — repaired working state

Stage 6 was run as a finish-line pass under the terminal-debt policy, not as a broad restart.

### Bounded repairs applied

- **25 NC State reciprocal H/A/N corrections**, including 19 `UNKNOWN` recoveries and six corrections to
  earlier H/A/N assignments. Literal Duke site markers remain preserved.
- **46 neutral physical-site recoveries** from already-identified Duke official event/schedule/game-note evidence.
  Major systematic recoveries include Lahaina Civic Center, Sullivan Arena, Madison Square Garden IV,
  Sprint Center/T-Mobile Center, Rose Garden/Moda Center, United Center, Bankers Life/Gainbridge Fieldhouse,
  and IZOD/Brendan Byrne Arena.
- **4 early `Charlotte` games (1909-10/1910-11)** split from the modern Charlotte program. The project scope
  for modern Charlotte begins in 1972-73; the early games are now the distinct historical identity
  `charlotte-historical-team`. Exact institutional lineage is deliberately not forced.
- **2 aggregate-source unknown-opponent placeholders** now use the schema sentinel `opponent-unknown`;
  this does not assert a bona fide opponent identity and is excluded from the NON_D1 owner scan.

### Terminal researched historical debt after repair

- `UNKNOWN` H/A/N: **145**
  - 1900s: 31
  - 1910s: 45
  - 1920s: 62
  - 1930s: 7
- Neutral rows missing exact physical venue: **67**
  - 1910s: 2
  - 1930s: 2
  - 1940s: 6
  - 1960s: 15
  - 1970s: 1
  - 1980s: 14
  - 1990s: 9
  - 2000s: 18
  - 2010s/2020s: 0
- Neutral rows missing complete location: **59**
- Unknown exact dates: **259**
  - 1900s: 31
  - 1910s: 100
  - 1920s: 109
  - 1930s: 18
  - 1940s: 1

Every surviving material site-gap row remains explicitly research-accounted. No surviving HOME venue/location
gap exists. No NCAA physical-site gap exists. No postseason site gap exists.

Under the terminal-debt rule, these residuals are release-safe historical debt: the largest systematic
reciprocal and modern neutral-event opportunities were challenged, supported repairs were applied, and no
comparable unresolved high-yield evidence class remains. They are not to be reopened merely to drive counts
toward zero.

### Stage 6 owner-scan delta

The historical Charlotte split creates exactly **one new NON_D1 identity** relative to the previously
owner-approved Stage 5 population:

- `charlotte-historical-team` — Charlotte (historical team) — **4 games**, 1909-10 through 1910-11,
  raw label `Charlotte`.

The owner explicitly approved this one-item delta on 2026-09-11, confirming that the four games are not
modern D1 Charlotte and may remain `Charlotte (historical team)` verbatim. No Stage 6 blocker remains.

**PRE-FREEZE SELF-CHALLENGE: PASS.**

Stage 6 is complete. Stage 7 is the next bounded stage and has not begun.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=9747fe7abca8be44f25c728c8aec9099caa3529e` from `research_base_sha=bb2fcf16dd8800e3d9b823c0b4999b2d1b516d6b`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
