# Virginia curation notes

## Program status and coverage

Virginia men's basketball is curated from varsity inception in **1905-06** through completed **2025-26**.

Project top-level scope reference: **INCEPTION+**. Research base: `5c91e35485060a0be27f9612d0b140883a555dbf` (protected `main`, PR #144).

This is the Stage 4 research package. It is not authoritative global repository state, and it has **not** yet passed the required owner NON_D1 sanity scan, final adversarial self-challenge, or `RESEARCH_FROZEN` sealing.

## Competitive history

- Competitive games: **3,026**
- On-court record: **1,787-1,238-1**
- Covered seasons: **121**
- Exact-date unknowns preserved: **86**
- Unknown played scores/results: **0**
- Exhibitions: excluded from the competitive package.

Literal `raw_text` from the accepted Stage 1 source universe is preserved on every source row.

## Material Stage 1 repairs

Accepted Stage 1 repairs were applied mechanically without erasing literal source evidence:

- 1950-51: excluded one source-bleed duplicate of the 1905-06 Charlottesville YMCA opener.
- 1951-52: restored the omitted Feb. 11, 1952 road win at Catholic, 82-65, from older Virginia institutional evidence and the official series record.
- 1949-50: corrected the Dec. 19 Gettysburg result marker from loss to win, consistent with the printed 59-57 score and Gettysburg's official schedule.
- 1964-65: corrected the Feb. 23 North Carolina score to Virginia 101, North Carolina 105, in two overtimes.
- 2023-24: corrected the March 15 NC State ACC semifinal score orientation to Virginia 65, NC State 73, overtime.
- 2025-26: added the completed **36-game** competitive season from Virginia's official schedule/results supplement; two preseason exhibitions remain excluded.

## Opponent identity

All **3,026** games have resolved opponent identities.

- Distinct source-label mapping rows: **1,066**
- Working distinct `NON_D1` identities: **93**
- Unresolved opponent identities: **0**
- Known current-program key splits: **0**
- Ambiguous current-program matches: **0**
- Informational self-corrected source-label families: **84**

The complete Stage 5 owner scan has been generated separately but is **not yet approved**.

## H/A/N and site completeness

Across the complete package:

- SOURCE_PROGRAM_HOME: **1,472**
- OPPONENT_HOME: **1,096**
- NEUTRAL: **458**
- UNKNOWN: **0**

Regular-season Stage 3A contains **2,800** games. All source-program HOME rows have complete physical venue and normalized city/state. Ordinary regular-season OPPONENT_HOME building reconstruction remains outside source-school responsibility unless accepted evidence already supplied it.

The regular-season neutral population contains **121** deliberately researched material site-gap rows:

- **119** historical (1995-96 and earlier) location-enrichment debt rows under the project's location-first stopping rule.
- **2** modern 2009 Cancun Challenge `RESEARCHED_PARTIAL` rows: Moon Palace Resort / Cancun, Mexico is supported, but the exact ballroom is not; Galactic Ballroom was not inferred.

Those rows carry explicit `site_research_status` / `site_research_basis`; silent material site gaps are not used.

## Home venue chronology

After HOME is independently established:

- 1905-06 through 1922-23 — **Fayerweather Gymnasium**, Charlottesville, VA
- 1923-24 through 1964-65 — **Memorial Gymnasium (Virginia)**, Charlottesville, VA
- 1965-66 through 2005-06 — **University Hall**, Charlottesville, VA
- 2006-07 onward — **John Paul Jones Arena**, Charlottesville, VA

Two accepted off-campus Virginia HOME games (Auburn 2004 and UMBC 2005) are assigned to **Siegel Center**, Richmond, VA. Venue chronology never establishes H/A/N.

## Postseason

Final Stage 3B population: **226 games**

- Conference tournament: **130**
- NCAA Tournament: **62**
- NIT: **31**
- Other postseason / CBI: **3**

All 226 postseason rows have exact physical venue plus city/state. NCAA site gaps: **0**. NIT/conference-tournament/other postseason exact-site gaps: **0**.

Owner disposition for `UVA-R-1932-018` (Virginia-Duke, Feb. 24, 1933 Southern Conference Tournament): **Raleigh Memorial Auditorium**, Raleigh, NC (`VEN-000522`). The conflicting owner-maintained shared conference-tournament reference row naming Thompson Gym is preserved as shared-reference maintenance debt and was not mutated from this school Research lane.

## Physical venue identity

The Stage 4 package contains **120** physical venue relationship rows:

- Protected-main physical identity reuses: **110**
- Historically resolved new physical venue candidates pending current-main Integration reconciliation: **10**

Pending candidates:

- `american-bank-center` — American Bank Center, Corpus Christi, TX
- `arena-at-northwest-florida-state-college` — The Arena at Northwest Florida State College, Niceville, FL
- `benedictine-high-school-gym` — Benedictine High School Gym, Richmond, VA
- `fayerweather-gymnasium` — Fayerweather Gymnasium, Charlottesville, VA
- `finneran-pavilion` — Finneran Pavilion, Villanova, PA
- `hampton-coliseum` — Hampton Coliseum, Hampton, VA
- `konawaena-high-school` — Konawaena High School, Kealakekua, HI
- `salem-civic-center` — Salem Civic Center, Salem, VA
- `siegel-center` — Siegel Center, Richmond, VA
- `war-memorial-gymnasium-blacksburg` — War Memorial Gymnasium, Blacksburg, VA

Research does not assign authoritative new global numeric venue IDs. Those identities remain `PENDING_CURRENT_MAIN_REBASE` for serialized Implementation.

Physical reused-name distinctions are preserved, including Madison Square Garden III vs. IV and Charlotte Coliseum I vs. II.

## Conference history

Accepted package chronology:

- 1905-06 through 1920-21 — Independent
- 1921-22 through 1952-53 — Southern Conference
- 1953-54 onward — ACC

Conference membership does not itself establish whether a game is a conference-tournament game; postseason classification is row-level evidence.

## Accomplishment context

Protected main currently carries Virginia's owner baseline as:

- Conference regular-season championships: **12**
- Conference tournament championships: **3**
- NCAA Tournament appearances: **27**
- Final Fours: **3**
- National championships: **1**
- Best finish: **National Champion (2019)**

That row remains `OWNER_BASELINE_UNVERIFIED`; authoritative accomplishment verification belongs to the later serialized workflow and is not silently promoted by this Research package.

## Known non-site discrepancy debt

The following field-specific date/source discrepancies remain preserved rather than silently overwritten during site research:

- `UVA-R-1916-011`
- `UVA-R-1921-007`
- `UVA-R-1977-012`
- `UVA-R-1923-008`
- reciprocal examples `UVA-R-1921-016` and `UVA-R-1993-025`

They are not permission to reopen Stage 1 during package assembly.

## Stage status

Stage 4 package assembly and mechanical package QA are complete.

Stage 5 owner NON_D1 sanity scan: **APPROVED** on **2026-09-24**. The owner approved the complete 93-identity working NON_D1 population after the pre-review mechanical correction `Fort Belvior` → `Fort Belvoir`; no identities were flagged for follow-up.

Stage 6 adversarial self-challenge, Stage 7 immutable package sealing, Implementation, canonical reconciliation, and publication remain later boundaries.

## Stage 6 adversarial self-challenge — COMPLETE

Stage 6 was recovered from the owner-approved Stage 5 checkpoint and executed under protected-main policy at
`b3f58a8e72fa2e8bbbfd75c088d2cf0f56a3bc04`. The Stage 5 checkpoint and its 128 manifest-tracked members
were verified byte-for-byte before any Stage 6 work; the embedded approved six-file portfolio matched
`01bc001c14b9e87cf4875a3907a35b3a759e134a1348731845f6a9f0f694e940`.

Stage 6 was an adversarial audit, not a second Research cycle. It challenged the largest/suspicious residual
classes systematically and made only bounded repairs supported by materially stronger evidence.

### Exact-date challenge and repairs

Working exact-date blanks entering Stage 6: **86**.

A systematic official-reciprocal pass was performed against the largest concentrated institutional series:
Washington & Lee, Virginia Tech, VMI, and George Washington. Washington & Lee and Virginia Tech recovered
**13** exact dates. A separate source-token/parser challenge recovered **1** additional date for
`UVA-R-1974-007` from the literal `J 4 Clemson` row, corroborated by Clemson's reciprocal schedule.

Total exact dates recovered in Stage 6: **14**.
Final exact-date blanks: **72**.

The 72 survivors are concentrated entirely in 1908-09 through 1947-48: 1 in the 1900s, 3 in the 1920s,
12 in the 1930s, and 56 in the 1940s. VMI's official history uses obvious `11/1` / `12/1` placeholder-like
dates across this early population and was not used to create false exact dates. George Washington's obvious
official historical path did not supply comparable early exact-date detail. After those class-level challenges,
the remaining fragmented early/service/non-D1 population is terminal researched exact-date debt.

### H/A/N contradictions repaired

The same official reciprocal date challenge exposed four concrete site contradictions; those rows were
repaired rather than preserving known error:

- `UVA-R-1921-017` — Washington & Lee: `SOURCE_PROGRAM_HOME` -> `NEUTRAL`, Lynchburg, VA.
- `UVA-R-1943-010` — Virginia Tech: `OPPONENT_HOME` -> `NEUTRAL`, Lynchburg, VA.
- `UVA-R-1945-005` — Washington & Lee: `SOURCE_PROGRAM_HOME` -> `OPPONENT_HOME`, Lexington, VA.
- `UVA-R-1945-010` — Washington & Lee: `OPPONENT_HOME` -> `SOURCE_PROGRAM_HOME`; Memorial Gymnasium
  (Virginia), Charlottesville, VA, follows the already accepted Virginia home-facility chronology.

The 1945-46 W&L pair is a site correction only. W&L's reciprocal history reports the December game as
63-25 while Virginia's source reports 63-24; the score conflict is preserved rather than silently resolved.

Final regular-season H/A/N census: **1,452 SOURCE_PROGRAM_HOME / 1,088 OPPONENT_HOME / 260 NEUTRAL /
0 UNKNOWN**. Final all-game census: **1,471 SOURCE_PROGRAM_HOME / 1,095 OPPONENT_HOME / 460 NEUTRAL /
0 UNKNOWN**.

### Direct reciprocal site write-through

During the same bounded reciprocal pass, directly supplied opponent-home location/site evidence was retained
rather than discarded:

- W&L opponent-home rows `UVA-R-1908-002`, `UVA-R-1942-021`, and `UVA-R-1946-009` now preserve
  Lexington, VA.
- Virginia Tech opponent-home row `UVA-R-1946-013` now preserves War Memorial Gymnasium, Blacksburg, VA.

No separate opponent-home building-research campaign was opened.

### Neutral debt challenge

The historical regular-season neutral population was **not** reopened for building archaeology. The two
newly corrected historical neutral rows above have supported Lynchburg locality but no supported exact
building, so they correctly become location-first `RESEARCHED_PARTIAL` debt.

Final regular-season neutral debt:
- historical 1995-96-and-earlier exact-building blanks: **121**; **56** also lack supported locality after the
  completed historical location-enrichment pass;
- modern 1996-97+ exact-building blanks: **2** (`UVA-R-2009-005`, `UVA-R-2009-006`), both 2009 Cancun
  Challenge rows. Moon Palace Resort / Cancun, Mexico is supported, but the exact contest room remains
  unsupported; no ballroom name was inferred.

Protected main advanced after the Research base only through later integrations/hardening. The newly published
Oregon State package contains no Virginia source-game row, so it creates no new reciprocal same-game neutral
recovery opportunity.

### Current-main venue and opponent-identity challenge

The Stage 4 physical-identity census was challenged against protected main
`b3f58a8e72fa2e8bbbfd75c088d2cf0f56a3bc04`. Main added six Oregon State onboarding venues after the
Virginia Research base; none collide with Virginia's ten pending physical candidates. Final venue identity
status remains **120 local physical rows / 110 current-main reuses / 10 genuinely new candidates /
0 ambiguous identities**.

The protected-main program-registry delta since Virginia's Research base changes Oregon State metadata only
and creates no Virginia opponent-key split. The newly published Oregon State opponent map was also checked
against Virginia's NON_D1 population; no contradictory current-program alias mapping was exposed. The six
Virginia NON_D1 identities represented in 2000-01-or-later games were specifically retained under the
already owner-approved Stage 5 identity state. Final known current-program key splits: **0**; ambiguous
current-program matches: **0**.

### Final Stage 6 acceptance state

- competitive games: **3,026**
- unresolved opponent identities: **0**
- unknown exact dates: **72**
- unknown played scores/results: **0**
- UNKNOWN H/A/N: **0**
- HOME venue/location blockers: **0**
- researched-unresolved HOME venue exceptions: **0**
- regular-season neutral material site-gap rows: **123**, all research-accounted
- unaccounted material site gaps: **0**
- postseason exact-site gaps: **0**
- NCAA site gaps: **0**
- ambiguous physical venue identities: **0**
- opponent mapping count mismatches: **0**
- current-program opponent key splits: **0**
- ambiguous current-program identity matches: **0**

`PRE-FREEZE SELF-CHALLENGE: PASS`

Stage 6 is complete. **Stage 7 / RESEARCH_FROZEN has not begun and must not begin without the owner's next
`Proceed`.**

## Stage 7 immutable Research Freeze

Stage 7 performed final immutable packaging only. No game identity, opponent identity, score, result,
exact date, H/A/N classification, venue/site conclusion, conference membership, postseason
classification, accomplishment conclusion, or unresolved-debt disposition changed from the accepted
Stage 6 portfolio.

- Stage 5 owner NON_D1 disposition: **APPROVED — 93 identities reviewed, zero flagged**
- Stage 6 pre-freeze adversarial self-challenge: **PASS**
- Research acceptance errors: **0**
- Research acceptance warnings: **0**
- Protected `main` observed at freeze: `b3f58a8e72fa2e8bbbfd75c088d2cf0f56a3bc04`
- Recorded research base remains: `5c91e35485060a0be27f9612d0b140883a555dbf`

`RESEARCH_FROZEN: YES`  
`CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`

Stage 7 does not begin serialized Implementation and does not mutate protected-main shared references.


## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=7f0ecd727dd0c8a7fbc80d0723bb912e3ceccc35` from `research_base_sha=5c91e35485060a0be27f9612d0b140883a555dbf`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
