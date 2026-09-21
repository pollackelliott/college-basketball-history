# Stage 3A Regular-Season Site Research Standard

- **Status:** Controlling Stage 3A research-responsibility, completeness, and durable-state policy
- **Applies to:** every new-school Research lane
- **Owner-approved:** 2026-09-20
- **Purpose:** make Stage 3A rigorous, finite, reusable, and directly consumable by later stages

This document controls when older Stage 3A wording is more general or would produce a different research obligation.

## 1. Stage 3A objective

Stage 3A must establish the regular-season site's historical truth while keeping two questions separate:

1. **What is the game-site classification?** — `HOME`, `OPPONENT_HOME`, `NEUTRAL`, or a genuinely researched unresolved classification under existing policy.
2. **Given that classification, what venue research does the source school actually own?**

Venue responsibility is intentionally asymmetric. A source school owns its own home history, does not own another school's home-building chronology, and should make a serious but proportionate effort to recover neutral-site venues.

Unsupported certainty is always worse than a researched unknown.

## 2. Responsibility by site type

### 2.1 HOME — source-school responsibility

An exact physical venue is the expected outcome for a regular-season `HOME` game.

Research must systematically establish the program's home-facility chronology and use it to resolve:

- primary home arenas/buildings by era;
- predecessor facilities and transition dates;
- temporary or replacement home sites;
- off-campus home sites;
- known one-off or special home venues.

Do not bulk-assign a building merely because it was the program's usual arena in that era. Explicit game-level evidence overrides chronology.

#### Ancient-home safety valve

The project does **not** require false certainty for genuinely difficult ancient home games.

When deliberate research establishes `HOME` and complete city/state geography but the surviving historical record does not support a specific physical building, the row may use the existing `RESEARCHED_UNRESOLVED_HOME_VENUE` exception.

This safety valve is especially relevant to games from the **1930s or earlier**, where surviving facility documentation may be thin. That era emphasis is not an automatic waiver: obvious institutional, archival, facility, reciprocal, and game-level evidence must still be exhausted first.

A broad unexplored historical era does not qualify.

### 2.2 OPPONENT_HOME — no dedicated building research

A regular-season `OPPONENT_HOME` game is not an active source-school venue-research obligation.

Stage 3A must:

- establish the supported H/A/N classification;
- preserve an exact opponent-home venue when it is already supplied by the source;
- preserve/reuse an exact venue when an authoritative accepted reciprocal, canonical, or shared project record already supplies it;
- otherwise leave the opponent's exact home-building reconstruction to that opponent's own Research lane.

Do **not** browse historical sources solely because an `OPPONENT_HOME` building field is blank.

Do not pretend known evidence is absent: if the venue is literally already present in accepted project/source evidence, carry it forward with provenance.

### 2.3 NEUTRAL — serious, proportionate venue research

Neutral-site games should receive active physical-venue research.

The research standard differs by era.

#### Modern neutral games: 1984-85 through present

For the **1984-85 season through the present**, an exact physical venue is strongly expected.

Modern neutral games ordinarily have sufficient tournament, institutional, host, arena, schedule, box-score, newspaper, or web-era documentation that a shallow first-pass failure is not an acceptable stopping point.

For unresolved modern neutral rows, Stage 3A should systematically use, as applicable:

1. exact-game evidence already present in the project's canonical/evidence layers;
2. recurring tournament/event/site-family structure;
3. official event or tournament records;
4. host-institution records;
5. opponent institutional schedules, record books, or reciprocal package evidence;
6. targeted contemporary reporting or archival material.

A modern neutral row may remain unresolved only after a deliberate, documented pass through the reasonable evidence paths for that row or evidence class. Do not create an unresolved status merely because the source school's primary ledger omits the building.

#### Historical neutral games: before 1984-85

Pre-1984-85 neutral games still deserve real research, especially when they belong to a recurring event, tournament, city/site family, or useful reciprocal institutional series.

Research should remain proportionate. After the canonical/shared first pass and the obvious systematic event/reciprocal evidence classes have been exhausted, a genuinely unsupported exact building may remain `RESEARCHED_PARTIAL` or `RESEARCHED_UNRESOLVED` under existing site-accounting policy.

Do not turn a difficult one-off neutral game from an early era into unlimited newspaper/yearbook archaeology merely to drive the unknown count to zero.

## 3. Canonical/shared-project first pass for neutral games

Before external historical searching for an unresolved neutral game, check whether the **exact same game** already exists in the current project with usable accepted venue evidence.

Useful read-only sources can include:

- `data/canonical/games.csv`;
- `data/evidence/game-assertions.csv`;
- accepted published school packages or reciprocal research artifacts;
- other approved shared-reference evidence.

Reuse is valid only when the same-game match is unambiguous and the venue evidence has traceable provenance.

Do not infer a neutral venue from:

- the opponent's ordinary home arena;
- a nearby game;
- a tournament's usual venue in another edition;
- city alone;
- arena chronology alone.

Research lanes may read and cite protected-main canonical/shared evidence. They still may not mutate protected-main shared registries outside the shared-reference authority policy.

Use the permanent read-only helper as the default exact-game canonical first pass:

```bash
python tools/stage3a_research.py neutral-lookup \
  --ledger <stage3a-ledger.csv> \
  --output <neutral-canonical-candidates.csv>
```

The helper matches by exact date plus the source/opponent program pair, resolves the
protected-main venue display identity when available, and returns provenance. It does
**not** mutate the research ledger. A canonical H/A/N disagreement is emitted as
`H_A_N_CONTRADICTION`, which requires narrow adjudication rather than automatic
override.

## 4. Whole-population execution model

Before substantial Stage 3A searching:

1. mechanically identify the current regular-season working population;
2. establish the H/A/N work census;
3. separate venue responsibility into `HOME`, `OPPONENT_HOME`, and `NEUTRAL`;
4. perform the neutral canonical/shared-project lookup;
5. group active HOME and NEUTRAL work into real evidence classes.

Examples of useful evidence classes include:

- one documented home-facility era;
- a facility transition/temporary-home class;
- one recurring tournament or event family;
- one NCAA-like site block or other single-event site structure where applicable;
- a reciprocal institutional series;
- a modern neutral-source family;
- a finite set of one-off neutral games after higher-yield classes are exhausted.

An arbitrary chronological slice is not an evidence class by itself.

Do not impose a universal row-count cap. A complete systematic class may be researched in one audit when the evidence structure is coherent. If execution/context risk becomes material, serialize at a coherent class boundary rather than fragmenting the class arbitrarily.

## 5. Stopping rules

### HOME

Continue until each HOME row has either:

- an exact physical venue with complete location/provenance; or
- a valid `RESEARCHED_UNRESOLVED_HOME_VENUE` disposition under the dedicated policy.

The 1930s-or-earlier safety valve prevents false certainty; it does not excuse shallow research.

### OPPONENT_HOME

A blank physical building is not a Stage 3A research blocker by itself.

Do not create or extend a research queue solely to fill opponent-home buildings.

### NEUTRAL, 1984-85 through present

Apply a strong completeness expectation. Canonical/shared reuse and the obvious modern event/host/opponent evidence classes must be challenged before accepting unresolved debt.

### NEUTRAL, before 1984-85

Apply serious but proportionate research. Once the obvious systematic/high-yield evidence classes have been exhausted and the remaining uncertainty is historically plausible, preserve the researched unknown and stop.

## 6. Mandatory durable Stage 3A row state

Stage 3A is not complete merely because aggregate counts and a sequence of overlays reconcile conversationally.

Before Stage 3A may declare complete, it must serialize **one authoritative row-level Stage 3A state** sufficient for a fresh chat and for Stage 4 to consume without reconstructing prior work.

The durable Stage 3A ledger must cover the full Stage 1 universe or otherwise provide an exact mechanically provable partition.

For new lanes, use this machine-readable row contract so the permanent validator and
canonical lookup can operate without school-specific adapters:

- `research_game_id`
- `source_program_key`
- `season_label`
- `game_date` (blank is allowed only when historically unresolved)
- `normalized_opponent_key`
- `stage3a_disposition` — `REGULAR_SEASON` or `POSTSEASON_HANDOFF`
- `stage3a_han` — `HOME`, `OPPONENT_HOME`, `NEUTRAL`, or active `UNKNOWN`
- `stage3a_venue_name`
- `stage3a_city`
- `stage3a_state`
- `stage3a_site_research_status`
- `stage3a_site_research_basis`
- `stage3a_boundary_correction`
- `stage3a_next_action`

`stage3a_next_action` is the durable queue field. Terminal values are `NONE`,
`NO_SOURCE_SCHOOL_VENUE_RESEARCH`, and `POSTSEASON_HANDOFF`; any other nonblank
value denotes active work and therefore keeps Stage 3A incomplete.

The ledger must preserve final regular-season H/A/N, exact physical venue when known,
city/state when known and required, explicit site-research status/basis for accepted
historical debt, and every accepted boundary correction affecting a row.

The final Stage 3A artifact must mechanically identify:

- the exact regular-season stable-ID population;
- the exact postseason-deferred/handoff stable-ID population;
- the final H/A/N census derived from those rows;
- HOME unresolved venue exceptions;
- NEUTRAL unresolved venue debt, including modern vs pre-1984-85 concentration;
- OPPONENT_HOME rows whose venue remains intentionally outside source-school responsibility.

If an accepted Stage 3A correction changes any row after an earlier checkpoint, the authoritative row-level ledger must be regenerated or explicitly superseded. Additive overlays alone are not an acceptable final Stage 3A product.

Accepted research must be written through to the full ledger before another substantial
evidence class begins. Class-specific overlay files are useful audit trails, but they may
not become the only durable location of accepted truth. The helper

```bash
python tools/stage3a_research.py apply-updates \
  --ledger <current-full-ledger.csv> \
  --updates <accepted-row-updates.csv> \
  --output <next-full-ledger.csv>
```

provides a generic sparse write-through path. Blank update cells mean leave unchanged;
`__CLEAR__` explicitly clears a field.

Aggregate counts are QA checks; they may never be used to choose row classifications merely to make arithmetic fit.

## 7. Stage 3A completion standard

Stage 3A may complete only when:

- the exact regular-season/postseason-deferred partition reconciles mechanically to Stage 1;
- regular-season H/A/N is fully researched/accounted under repository policy;
- HOME venue work satisfies the strong source-school standard, with only valid researched-unresolved home exceptions remaining;
- no ordinary `OPPONENT_HOME` building blank remains in an active source-school research queue;
- modern neutral games (1984-85 through present) have received the strong completeness pass;
- historical neutral games have received the proportionate systematic pass;
- every material unresolved site fact has explicit research accounting;
- ambiguous physical venue identities = 0;
- the single authoritative row-level Stage 3A ledger is written, hashed/verified when checkpoint packaging is used, and sufficient for downstream assembly without historical reconstruction.

Immediately before Stage 3A completion, validate the authoritative state mechanically:

```bash
python tools/stage3a_research.py check \
  --universe <stage1-ledger.csv> \
  --ledger <stage3a-ledger.csv> \
  --handoff <postseason-handoff.csv> \
  --require-complete
```

During bootstrap or an incomplete stage, run the same command without
`--require-complete`; active `stage3a_next_action` rows are then reported as a healthy
incomplete queue rather than being hidden in prose.

The pre-freeze self-challenge remains required and should specifically challenge surprising modern neutral debt and any claimed HOME exception.

## 8. Relationship to other policies

This document does not weaken:

- the rule that H/A/N may not be inferred from geography;
- NCAA Stage 3B strict physical-site completeness;
- the shared-reference mutation boundary;
- site-research provenance requirements;
- the owner NON_D1 sanity scan;
- the pre-freeze adversarial self-challenge;
- the rule that literal source evidence and conflicts remain preserved.

When older Stage 3A wording differs on responsibility, modern-neutral expectations, ancient-home stopping, canonical-first reuse, or final row-level serialization, **this document controls**.
