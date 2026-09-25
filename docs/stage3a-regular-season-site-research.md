# Stage 3A Regular-Season Site Research Standard

- **Status:** Controlling Stage 3A research-responsibility, completeness, and durable-state policy
- **Applies to:** every new-school Research lane
- **Owner-approved:** 2026-09-20
- **Execution refactor approved:** 2026-09-21
- **Post-Oregon-State execution amendment approved:** 2026-09-23
- **Neutral publication-priority amendment approved:** 2026-09-23
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

#### Modern neutral games: 1996-97 through present

For regular-season neutral venue research, **modern** means the **1996-97 season through the present**. An exact physical venue is strongly expected.

Modern neutral games ordinarily have sufficient tournament, institutional, host, arena, schedule, box-score, newspaper, or web-era documentation that a shallow first-pass failure is not an acceptable stopping point.

For unresolved modern neutral rows, Stage 3A should systematically use, as applicable:

1. exact-game evidence already present in the project's canonical/evidence layers;
2. recurring tournament/event/site-family structure;
3. official event or tournament records;
4. host-institution records;
5. opponent institutional schedules, record books, or reciprocal package evidence;
6. targeted contemporary reporting or archival material.

A modern neutral row may remain unresolved only after a deliberate, documented pass through the reasonable evidence paths for that row or evidence class. Do not create an unresolved status merely because the source school's primary ledger omits the building.

#### Historical neutral games: 1995-96 and earlier

Regular-season neutral games from **1995-96 and earlier** use a **location-first historical standard**.

The research objective is to establish the best defensible event/locality record, not to exhaustively reconstruct every physical building. Use accepted project evidence plus the obvious systematic event/host/participant institutional opportunity for the row or class. Preserve:

- event/tournament identity when supported;
- city/state when supported;
- exact physical venue when the same obvious evidence directly supplies it;
- explicit `RESEARCHED_PARTIAL` / `RESEARCHED_UNRESOLVED` accounting when stronger detail is unsupported.

**Once supported city/state is established, do not open additional source paths solely to recover the exact physical building.** Do not launch building-only newspaper, yearbook, arena-history, or row-level archive searches merely because the building remains blank.

If the obvious systematic evidence supplies an exact building, accept it. If it supplies only locality/event context, preserve that locality and terminalize the building blank as historical enrichment debt. If even locality remains unsupported after the obvious systematic opportunity, preserve the researched unknown rather than escalating into bespoke archaeology.

Exact-building recovery for this historical regular-season neutral population is desirable enrichment, not a publication blocker. Existing accepted exact venues remain accepted and must not be removed, reopened, or downgraded merely because they fall on the historical side of the cutoff.

### 2.4 Neutral games outside the United States — locality is sufficient

For any neutral-site game whose supported location is **outside the United States**, exact-building research is opportunistic only.

Once the row has a defensible city plus country and, where applicable, state/province/territory/first-level administrative area:

- accept an exact venue if it is already present in accepted project evidence or is immediately supplied by the same obvious authoritative source;
- otherwise stop exact-building research for that row;
- do not open an additional source path solely to recover the building;
- preserve the supported locality/country and mark the exact-building blank as explicitly researched/accounted rather than unresolved active debt.

This owner directive applies regardless of era and overrides the otherwise stronger modern-neutral exact-venue expectation for the exact-building field.

This historical shortcut applies **only to regular-season neutral rows**. It does not apply to NCAA, NIT, conference-tournament, or any other postseason game. Postseason exact-venue research remains a separate Stage 3B obligation, subject to the same outside-the-United-States locality-sufficient exception defined above.

## 3. Canonical/shared-project first pass for neutral games

**Stage 3A-0 note:** when this lookup occurs during Stage 3A-0, the stricter
`docs/stage3a0-local-only-contract.md` applies. The lookup is limited to evidence
already present in the verified checkpoint or checked-out/current protected-main project.
Do not use the web or discover new reciprocal sources during 3A-0.

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

Each substage is a required owner-facing stop boundary. **Evidence classes inside 3A-1 through 3A-3 are research units, not mandatory owner-facing stop boundaries.** Use the largest safely completable bundle of related classes that share a research mode. Avoid both tiny family-by-family relays and open-ended sweeps across a heterogeneous residual.

A plain owner `Proceed` authorizes the identified next substage or serialized unfinished tranche. Routine evidence-class transitions inside an authorized substage should normally be handled autonomously.

### 4.1 Stage 3A-0 — census, partition, and exact-game project evidence

Stage 3A-0 is **strictly local-only and mechanical**. It performs zero external
historical research.

Allowed inputs are limited to the verified durable checkpoint/working state plus
already-present project evidence in the checked-out/current protected-main repository.
Direct reads of known repository files are allowed. Open-ended discovery is not.

Before broad historical research:

1. mechanically identify the exact Stage 1 game universe;
2. partition it into the regular-season Stage 3A population and postseason Stage 3B
   handoff population;
3. derive the whole-population H/A/N work census;
4. separate venue responsibility into `HOME`, `OPPONENT_HOME`, and `NEUTRAL`;
5. separate NEUTRAL rows into 1996-97+ and 1995-96-and-earlier populations;
6. use the permanent repository Stage 3A-0 entrypoint for one structured exact-game join
   against already-present canonical and assertion evidence for the target school;
7. write through only unambiguous accepted same-game evidence;
8. preserve unmatched/contradictory candidates without forcing or researching them;
9. serialize the exact H/A/N, HOME, and NEUTRAL residual queues.

During Stage 3A-0, do **not**:

- search the public web;
- browse institutional archives, schedules, media guides, newspapers, or external PDFs;
- search GitHub/code hosting to discover new source files;
- find new opponent source families;
- research venue candidates externally;
- adjudicate contradictions that require new evidence;
- inspect opponent packages one by one when the same population can be joined
  mechanically from local files.

Stage 3A-0 does **not** enumerate, fetch, or inspect published opponent school packages,
even though those packages are local project evidence. Targeted reciprocal/published-package
use belongs to Stage 3A-1/2/3, where source-family scope is explicit and bounded.

If the canonical/assertion bulk join does not resolve a candidate, leave that candidate for
the appropriate later Stage 3A research substage. Stage 3A-0 succeeds by producing exact
mechanical populations and queues, not by minimizing the residual counts.

Do not begin broad HOME chronology research, broad NEUTRAL venue research, or row-by-row
H/A/N adjudication before Stage 3A-0 is durably closed.

### 4.2 Stage 3A-1 — H/A/N completion

Resolve the H/A/N residual before broad venue research.

`docs/stage3a1-source-fanout-contract.md` is controlling for source hierarchy,
source-fanout limits, and proportional convergence in this substage.

Partition unresolved H/A/N rows into real evidence classes, then bundle multiple small
classes that can be handled through the same source/research mode.

A systematic source family may resolve a large population in one turn. When a class
requires separate external searching, source comparison, or historical adjudication for
individual games, one turn may adjudicate **no more than 25 rows**. When a homogeneous
independent-row residual is already 25 or fewer rows, normally process the whole residual
rather than creating several smaller owner handoffs **only when the same small set of
coherent source families can support that tranche**.

Before opening external sources, define the evidence-class plan and use the required
hierarchy:

1. already-accepted project evidence;
2. target-school institutional source family;
3. obvious opponent institutional source family;
4. at most one specific high-yield authoritative fallback family when justified.

For an individual row, do not turn that hierarchy into unlimited searching. Normally
inspect no more than one target-school institutional path and one opponent institutional
path after project evidence. A third external path is allowed only when a specific named
authoritative source is already identified as plausibly decisive.

Generic web search may locate an authoritative source, but it is not an evidence class.
Do not fan out through Reddit, fan forums, mirrors, scraped schedule sites, aggregators,
random wikis, or unrelated search results merely because the obvious institutional paths
did not resolve the row.

Write accepted H/A/N findings through into the cumulative authoritative working ledger
before the durability boundary. Do not begin HOME or NEUTRAL venue research merely because
the current H/A/N tranche finishes early.

After the whole-population/project-evidence pass and the obvious systematic
institutional/reciprocal/source-family opportunities have been exhausted, a homogeneous
ancient historical/non-D1 residual may be closed **at the population level** as terminal
`RESEARCHED_UNRESOLVED` H/A/N debt. Do not require every surviving opponent family or
every ancient row to prove independently that no deeper archive exists. Once the bounded
authoritative source hierarchy is exhausted for a row/class, another theoretical source
is not sufficient reason to keep searching.

### 4.3 Stage 3A-2 — HOME venue research

Only after Stage 3A-1 completes, use a **facility chronology + default/exception model**:

- establish the program's authoritative home-facility chronology and season-level home
  evidence;
- when a normal home venue is systematically established for a season/era and no accepted
  evidence indicates an alternate site, apply that supported venue across the exact
  covered HOME population rather than re-proving the building through individual box
  scores;
- identify exceptions through count mismatches, explicit source text, alternate-site
  markers, temporary/off-campus evidence, or contradictions;
- explicit game-level evidence overrides the systematic default;
- bundle related facility eras/classes that use the same research mode;
- apply the 25-row cap only when separate row-level adjudications are required.

For ancient HOME residuals, once the reasonable institutional/facility/reciprocal and
other obvious systematic paths are exhausted, close the homogeneous residual under
`RESEARCHED_UNRESOLVED_HOME_VENUE` rather than creating one archaeology project per
game.

**HOME geography must be closed in Stage 3A-2, not deferred to 3A-4.** Every HOME row
using the unresolved-building exception must have supported city/state written through.
When the source program's home geography is systematically established for an era and no
accepted evidence indicates an alternate/off-campus location, that geography may be
propagated across already-established HOME rows as a default-with-exceptions operation.
This is not inference of H/A/N from geography.

### 4.4 Stage 3A-3 — NEUTRAL venue research

`docs/stage3a3-neutral-tranche-contract.md` is controlling for execution tiers,
tranche sizing, source fanout, and proportional convergence.

Only after Stage 3A-2 completes, use this default execution order:

1. accepted exact-game venue evidence already present in the durable state;
2. modern (1996-97+) recurring event/site families;
3. modern (1996-97+) one-offs;
4. one historical (1995-96 and earlier) **location-enrichment pass** across the remaining regular-season neutral residual.

After substantial work begins in one tier, **do not cross into the next materially
different tier in the same turn**. Bring the active tier/tranche to disposition, write
accepted findings through, serialize the exact residual, and stop at a durable continuation
point. A tier boundary is an execution boundary, not a new owner historical gate.

For recurring families, establish the event/site pattern once for the exact supported
editions and apply it systematically; research only genuine exceptions, contradictions,
or multi-venue editions individually. Multiple small related families using the same
research mode should normally be bundled into one meaningful tranche.

Use a bounded source hierarchy for recurring families:

1. accepted project/canonical/reciprocal evidence;
2. official event/tournament/host institutional source family;
3. target-school or obvious participant institutional source family;
4. at most one specific high-yield authoritative fallback family when justified.

For the historical location-enrichment pass, group rows by the largest sensible systematic
event/opponent/locality structures already visible in the authoritative residual, but do not
turn those groups into separate building-research campaigns. Use accepted project evidence
plus the obvious event/host/participant institutional opportunity. The goal is event/locality
completion and opportunistic exact-venue recovery when that same evidence supplies it.

Once city/state is established for a historical regular-season neutral row, do not open
another source path solely to recover the building. Surviving exact-building blanks become
terminal historical enrichment debt with explicit research accounting. Historical one-offs
must not become row-by-row archive searches.

Do not continue a "locate exact sources for missing patches" tail chase after the obvious
systematic location evidence is exhausted.

The 1996-97+ population retains the strong exact-venue expectation. The 1995-96-and-earlier
regular-season neutral population uses the location-first standard above. This does not
weaken the anti-inference rule and does not apply to postseason. NCAA, NIT, conference-
tournament, and other postseason exact venues remain Stage 3B research obligations.

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
5. verify HOME city/state is complete, including every unresolved-building exception;
6. preserve OPPONENT_HOME rows intentionally outside source-school building responsibility;
7. run Stage 3A QA;
8. serialize/hash the Stage 3A completion checkpoint.

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

### NEUTRAL, 1996-97 through present

Apply a strong completeness expectation. Canonical/shared reuse and the obvious modern event/host/opponent evidence classes must be challenged before accepting unresolved debt.

### NEUTRAL, 1995-96 and earlier

Apply the location-first historical standard. Use accepted project evidence and the obvious systematic event/host/participant opportunity to establish event and city/state where possible. Accept an exact building when that same evidence directly supplies it. Once supported city/state is established, do not continue searching solely for the building. A surviving building blank is nonblocking historical enrichment debt.

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
- NEUTRAL unresolved venue debt, including modern (1996-97+) vs historical (1995-96 and earlier) concentration;
- OPPONENT_HOME rows whose venue remains intentionally outside source-school responsibility.

If an accepted Stage 3A correction changes any row after an earlier checkpoint, the authoritative row-level ledger must be regenerated or explicitly superseded. Additive overlays alone are not an acceptable final Stage 3A product.

### Write-through durability during Stage 3A

Do not wait until Stage 3A closeout to consolidate accepted findings. After each **meaningful execution tranche**—which may contain several small evidence classes using the same research mode—write accepted row-level findings through into the cumulative authoritative working ledger before execution risk becomes material.

Evidence-class overlays, research notes, and source registers remain useful audit artifacts, but they are supplemental. They must not become the only durable location of accepted H/A/N or venue truth.

A durability checkpoint does not require an owner handoff after every tiny family. Preserve the exact residual queue when a meaningful tranche completes, the independent-row cap is reached, a genuine contradiction/blocker requires isolation, or context/execution risk becomes material.

Substantial historical research and Stage 3A-4 mechanical closeout are separate bounded assignments. Do not combine them merely because research happened to converge late in a turn.

Aggregate counts are QA checks; they may never be used to choose row classifications merely to make arithmetic fit.

## 7. Stage 3A completion standard

Stage 3A may complete only after Stage 3A-0 through Stage 3A-4 have each closed under the required execution boundaries and:

- the exact regular-season/postseason-deferred partition reconciles mechanically to Stage 1;
- regular-season H/A/N is fully researched/accounted under repository policy;
- HOME venue work satisfies the strong source-school standard, with only valid researched-unresolved home exceptions remaining;
- no ordinary `OPPONENT_HOME` building blank remains in an active source-school research queue;
- modern neutral games (1996-97 through present) have received the strong completeness pass;
- historical regular-season neutral games (1995-96 and earlier) have received the location-first systematic pass, with supported event/city/state preserved and surviving exact-building gaps explicitly accounted as nonblocking terminal enrichment debt;
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
