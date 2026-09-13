# Duke men's basketball — source notes

## Research provenance

- Research base: `bb2fcf16dd8800e3d9b823c0b4999b2d1b516d6b`
- Target scope: `INCEPTION+`
- Stage 4 assembly date: 2026-09-11

### Primary historical source

**2025-26 Duke Men's Basketball Media Guide — All-Time Results**

- Historical ledger recovered from printed pp. **164-181**
- Printed rows mechanically recovered: **3,265**
- Seasons represented in printed ledger: **120**
- Literal printed game rows are retained in `source-games.csv::raw_text`.
- Source anomalies, typos, score conflicts, and later corrections are not silently erased.

The accepted recovery package also preserves the mechanical recovery QA and durable correction evidence used to reconstruct the ledger after the original Duke research chat failed.

### Completed 2025-26 supplement

**Duke Athletics official 2025-26 schedule/results and media hub**

- Schedule: `https://goduke.com/sports/mens-basketball/schedule/2025-26`
- Media hub: `https://goduke.com/sports/2025/9/24/2025-26-duke-mens-basketball-media-hub`
- Competitive supplement: **38 games, 35-3**
- UCF and Tennessee exhibitions are excluded.
- The official schedule/media hub supplies current-season result, H/A/N, listed location/venue, and event evidence.

### Duke-specific conference-tournament site source

**Conference_Tournament_Site_Reference(20260904-035740).xlsm**

- Authorization is **Duke-specific only**.
- The surviving recovery checkpoint states it is complete for Duke's conference-tournament history.
- It is not promoted as universal/global tournament-site truth.

## Research hierarchy used

1. Duke official media guide / all-time results / archived season schedules / opponent histories.
2. NCAA official bracket, site, and Final Four history for NCAA Tournament requirements.
3. Owner-authorized Duke-scope conference-tournament site reference.
4. Opponent institutional schedules, record books, arena histories, and reciprocal game evidence.
5. Archival/contemporary evidence when institutional sources were insufficient.

Unsupported inference was not used merely to make package fields complete.

## Stage 1 recovery controls

Final competitive universe: **3,306 games, 2,370-936**.

Accepted structural corrections include:

- excluded duplicated 1907-08 Trinity Park 24-1 carryover;
- added omitted 1915-16 60-28 road win at Guilford;
- added omitted 1917-18 20-26 loss to Durham YMCA on 1918-01-15;
- preserved one unidentified official-season victory in 1917-18 as a clearly marked aggregate-source placeholder;
- preserved one unidentified official-season victory in 1919-20 as a clearly marked aggregate-source placeholder;
- retained literal source score conflicts rather than silently normalizing them when stronger evidence did not control the Duke source assertion.

## Opponent identity research

The completed Stage 6 package resolves **319** bona fide canonical opponent identities from the Duke source-label universe.

- Current-D1 identities: **246**
- `NON_D1` identities: **73**
- Normal opponent identities unresolved: **0**
- Aggregate-source placeholders: **2 games**, represented by the schema sentinel `opponent-unknown` rather than a bona fide identity

The informational self-corrected current-program alias list contains **33** source labels whose naive/local wording was normalized to the current project program identity.

The preserved Stage 5 approval covers the reconstructed **72 identities / 257 games**. Stage 6 added one
historical identity—`Charlotte (historical team)`, 4 games in 1909-10/1910-11—which the owner explicitly
approved on 2026-09-11. Final owner-approved `NON_D1` census: **73 identities / 261 games**.

## Site research

### Regular season

Stage 3A closed **2,897** rows before the later one-row partition correction was discovered.

Accepted Stage 3A census:

- 1,316 HOME
- 1,108 AWAY
- 309 NEUTRAL
- 164 UNKNOWN
- HOME missing venue/location: 0 / 0
- 113 regular neutral rows missing exact venue
- 75 regular neutral rows missing location
- every material regular-site gap explicitly researched/accounted
- ambiguous physical venue identities: 0

### Postseason

Stage 3B dispositioned all **409** mechanically deferred rows.

- 408 genuine postseason rows
- 1 regular-season partition correction
- NCAA physical-site completeness: **172/172**
- conference-tournament/NIT material site gaps: **0**
- ambiguous physical venue identities: 0

Raleigh Memorial Auditorium is retained as a distinct researched physical-identity candidate pending serialized Implementation rebase. It is not forced into Thompson Gym.

## Research-base identity handling

Existing research-base venue identities are reused only when physical identity is supported.
Genuinely new candidates receive provisional `VEN-990xxx` transport IDs in `venues.csv`.
Those IDs are not authoritative global IDs and must be rebased against current protected `main` before tracked Phase 0.

Stage 4 also mechanically recognizes two accepted overlay venues that already exist in the research-base registry:

- `VEN-000327` — The Gymnasium, College Park, MD
- `VEN-000279` — Woodruff Hall, Athens, GA

This is shared-reference reconciliation, not a reopening of accepted H/A/N or game-universe research.

## Known researched historical debt

The package intentionally preserves:

- **259** games without exact dates;
- **164** `UNKNOWN` H/A/N rows;
- **113** neutral rows without exact physical venue;
- **75** neutral rows without city/state.

All material site gaps have explicit research accounting. After the Stage 6 adversarial challenge, the surviving permitted populations are certified as terminal researched historical debt under current policy.

## Stage 4 QA result

The six-file package is mechanically closed under the current schema:

- source-game rows: 3,306
- source-game IDs unique: yes
- opponent mappings complete for all bona fide identities: yes
- current-program key splits: 0
- ambiguous current-program matches: 0
- HOME publication blockers: 0
- NCAA site gaps: 0
- unaccounted material site gaps: 0
- conference intervals non-overlapping: yes
- physical venue identities ambiguous: 0

Final Stage 6 research acceptance is **PASS**. `RESEARCH_FROZEN` is not yet claimed because immutable packaging is the separately bounded Stage 7.

## Stage 6 finish-line self-challenge

The self-challenge applied only finite, supported repairs and then invoked the terminal-debt stopping rule.

Final repaired working package controls:

- competitive games: **3,306**
- record: **2,370-936**
- site types: **1,324 SOURCE_PROGRAM_HOME / 1,131 OPPONENT_HOME / 706 NEUTRAL / 145 UNKNOWN**
- exact-date blanks: **259**
- HOME publication blockers: **0**
- NCAA physical-site gaps: **0/172**
- conference/NIT/other postseason site gaps: **0**
- material site-gap rows: **212**
- explicitly research-accounted material gaps: **212**
- unaccounted material site gaps: **0**
- local physical venue relationships: **95**
- current/research-base physical reuses: **80**
- provisional research candidates: **15**
- ambiguous physical venue identities: **0**
- known current-program key splits after the Charlotte repair: **0**
- ambiguous current-program matches: **0**

The 145 surviving UNKNOWN H/A/N rows, 67 neutral venue gaps, and 259 exact-date blanks are terminal researched
historical debt under current policy. They are concentrated in early historical eras except for 18 regular-season
neutral venue gaps in the 2000s. Modern 2010s/2020s neutral venue debt was eliminated by the Stage 6 bounded pass.

The one Stage 6 owner-scan delta, `charlotte-historical-team` (4 games, 1909-10 through 1910-11),
was explicitly owner-approved on 2026-09-11. The four games remain `Charlotte (historical team)` and are
not attributed to the current D1 Charlotte program.

**PRE-FREEZE SELF-CHALLENGE: PASS.**

Stage 6 is complete; Stage 7 has not begun.
