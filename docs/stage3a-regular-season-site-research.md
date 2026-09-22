# Stage 3A Regular-Season Site Research Standard

- **Status:** Controlling Stage 3A research-responsibility, completeness, and durable-state policy
- **Applies to:** every new-school Research lane
- **Owner-approved:** 2026-09-20
- **Execution refactor approved:** 2026-09-21
- **Purpose:** make Stage 3A rigorous, finite, reusable, operationally bounded, and directly consumable by later stages

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

Before external historical searching for an unresolved neutral game, perform a **bounded, read-only exact-game lookup** to determine whether the exact same game already exists in the current project with usable accepted venue evidence. Treat this as a mechanical first-pass reuse check, not as a mandate to reconcile every historical disagreement with canonical data.

Useful read-only sources can include:

- `data/canonical/games.csv`;
- `data/evidence/game-assertions.csv`;
- accepted published school packages or reciprocal research artifacts;
- other approved shared-reference evidence.

Reuse is valid only when the same-game match is unambiguous and the venue evidence has traceable provenance. If the lookup exposes a genuine H/A/N or historical-site contradiction, isolate that row for narrow adjudication under normal Research rules; do not automatically overwrite the source-school conclusion and do not reopen unrelated accepted populations.

Do not infer a neutral venue from:

- the opponent's ordinary home arena;
- a nearby game;
- a tournament's usual venue in another edition;
- city alone;
- arena chronology alone.

Research lanes may read and cite protected-main canonical/shared evidence. They still may not mutate protected-main shared registries outside the shared-reference authority policy.

## 4. Required Stage 3A execution architecture

Stage 3A research standards are unchanged, but Stage 3A is **not** a single chat-execution unit.

It must run through five ordered substages:

1. **Stage 3A-0 — mechanical census, partition, and project-evidence harvest**
2. **Stage 3A-1 — H/A/N completion**
3. **Stage 3A-2 — HOME venue research**
4. **Stage 3A-3 — NEUTRAL venue research**
5. **Stage 3A-4 — mechanical closeout and QA**

Each substage is a required execution stop boundary. Do not automatically roll from one
substage into the next in the same turn. A plain owner `Proceed` authorizes only the
identified next substage or the identified unfinished evidence-class continuation.

### 4.1 Stage 3A-0 — census, partition, and exact-game project evidence

Before broad historical research:

1. mechanically identify the exact Stage 1 game universe;
2. partition it into the regular-season Stage 3A population and postseason Stage 3B
   handoff population;
3. derive the whole-population H/A/N work census;
4. separate venue responsibility into `HOME`, `OPPONENT_HOME`, and `NEUTRAL`;
5. separate NEUTRAL rows into 1984-85+ and pre-1984-85 populations;
6. perform the bounded read-only exact-game canonical/accepted reciprocal lookup;
7. write through only unambiguous accepted same-game evidence;
8. preserve unmatched/contradictory candidates without forcing them;
9. serialize the exact H/A/N, HOME, and NEUTRAL residual queues.

Do not begin broad HOME chronology research, broad NEUTRAL venue research, or large
row-by-row H/A/N adjudication before Stage 3A-0 is durably closed.

### 4.2 Stage 3A-1 — H/A/N completion

Resolve the H/A/N residual before broad venue research.

Partition unresolved H/A/N rows into real evidence classes and work **one evidence class
per turn**. Examples may include one reciprocal institutional series, one schedule/source
family, one event/site family where H/A/N is explicit, or a finite one-off residual after
higher-yield classes are exhausted.

A systematic source structure may resolve a large class in one turn. However, when a
class requires separate external searching, source comparison, or historical adjudication
for individual games, one turn may adjudicate **no more than 25 rows**. This is an
execution cap, not a research stopping rule; preserve the same evidence-class identity
and resume its exact residual queue on the next `Proceed`.

Write accepted H/A/N findings through into the cumulative authoritative working ledger
before stopping. Do not begin HOME or NEUTRAL venue research merely because the current
H/A/N class finishes early.

### 4.3 Stage 3A-2 — HOME venue research

Only after Stage 3A-1 completes:

- establish the program's home-facility chronology from authoritative evidence;
- work one coherent HOME evidence class per turn;
- allow one systematic source/chronology to resolve a large class mechanically when
  evidence supports it;
- apply the 25-row execution cap when separate row-level external adjudications are
  required;
- write accepted venue/location/provenance findings through before stopping;
- preserve the dedicated researched-unresolved HOME exception where justified.

Chronology may define or organize a real evidence class, but an arbitrary chronological
slice is not an evidence class by itself.

### 4.4 Stage 3A-3 — NEUTRAL venue research

Only after Stage 3A-2 completes:

- carry forward the Stage 3A-0 exact-game project-evidence harvest rather than repeating
  it wholesale;
- work one coherent NEUTRAL evidence class per turn;
- apply the stronger 1984-85+ exact-venue expectation;
- apply serious but proportionate pre-1984-85 research;
- allow a systematic event/source structure to resolve a large class mechanically;
- apply the 25-row execution cap when separate row-level external adjudications are
  required;
- write accepted venue/location/provenance findings through before stopping.

Examples of useful NEUTRAL evidence classes include one recurring tournament/event
family, one reciprocal institutional series, one host/source family, one modern
neutral-source family, or a finite one-off residual after higher-yield classes are
exhausted.

### 4.5 Stage 3A-4 — mechanical closeout and QA

Stage 3A-4 is deliberately separate from substantial historical research.

Do not launch broad new searching in this substage. If closeout exposes a genuine
historical contradiction or a missing required research population, stop and route that
specific population back to the appropriate earlier substage.

Otherwise mechanically:

1. regenerate or explicitly supersede the authoritative full row-level Stage 3A ledger;
2. reconcile the exact regular-season/postseason partition to Stage 1;
3. derive the final H/A/N census from rows;
4. derive HOME exception and NEUTRAL debt populations;
5. preserve OPPONENT_HOME rows intentionally outside source-school building responsibility;
6. run Stage 3A QA;
7. serialize/hash the Stage 3A completion checkpoint.

This separation prevents the failure mode in which a long historical-research turn also
attempts full-population ledger reconstruction, census, QA, packaging, and hashing before
returning a response.

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

The durable Stage 3A ledger must cover the full Stage 1 universe or otherwise provide an exact mechanically provable partition, and must preserve at minimum:

- stable `research_game_id`;
- current Stage 3A population disposition: regular season vs postseason-deferred/handoff;
- final regular-season H/A/N classification;
- exact physical venue when known;
- city/state when known and required;
- site-research status;
- site-research basis/provenance;
- any accepted boundary correction affecting the row.

The final Stage 3A artifact must mechanically identify:

- the exact regular-season stable-ID population;
- the exact postseason-deferred/handoff stable-ID population;
- the final H/A/N census derived from those rows;
- HOME unresolved venue exceptions;
- NEUTRAL unresolved venue debt, including modern vs pre-1984-85 concentration;
- OPPONENT_HOME rows whose venue remains intentionally outside source-school responsibility.

If an accepted Stage 3A correction changes any row after an earlier checkpoint, the authoritative row-level ledger must be regenerated or explicitly superseded. Additive overlays alone are not an acceptable final Stage 3A product.

### Write-through durability during Stage 3A

Do not wait until Stage 3A closeout to consolidate accepted findings. After every completed evidence class or capped row-by-row tranche, write accepted row-level findings through into the cumulative authoritative working ledger before stopping.

Evidence-class overlays, research notes, and source registers remain useful audit artifacts, but they are supplemental. They must not become the only durable location of accepted H/A/N or venue truth.

When a class remains unfinished because the row-by-row execution cap was reached, preserve the current full working ledger plus the exact residual queue for that same class. A later continuation must be able to resume without reconstructing accepted rows from prose or scattered overlays.

Substantial historical research and Stage 3A-4 mechanical closeout are separate bounded assignments. Do not combine them merely because research happened to converge late in a turn.

Aggregate counts are QA checks; they may never be used to choose row classifications merely to make arithmetic fit.

## 7. Stage 3A completion standard

Stage 3A may complete only after Stage 3A-0 through Stage 3A-4 have each closed under the required execution boundaries and:

- the exact regular-season/postseason-deferred partition reconciles mechanically to Stage 1;
- regular-season H/A/N is fully researched/accounted under repository policy;
- HOME venue work satisfies the strong source-school standard, with only valid researched-unresolved home exceptions remaining;
- no ordinary `OPPONENT_HOME` building blank remains in an active source-school research queue;
- modern neutral games (1984-85 through present) have received the strong completeness pass;
- historical neutral games have received the proportionate systematic pass;
- every material unresolved site fact has explicit research accounting;
- ambiguous physical venue identities = 0;
- the single authoritative row-level Stage 3A ledger is written, hashed/verified when checkpoint packaging is used, and sufficient for downstream assembly without historical reconstruction.

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
