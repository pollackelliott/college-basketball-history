# Research Lane Bounded Execution Protocol

- **Status:** Controlling Research-lane turn-execution protocol
- **Applies to:** new school Research lanes and recovery of unfinished Research lanes
- **Does not replace:** historical/data-quality policy, six-file schema, site-completeness policy, opponent-identity policy, NON_D1 owner sanity scan, or research-freeze self-challenge
- **Pilot basis:** empirically validated during Kansas State research, September 2026; durability/stopping rules hardened after the DePaul postmortem; execution/convergence revised after the Oregon State retrospective

## 1. Purpose

Research quality standards are unchanged. This protocol changes **how autonomous research is divided into chat turns** so substantial work ends at deliberate, recoverable boundaries rather than attempting an entire school in one unbounded turn.

The governing rule is:

> **Use the largest safely completable bounded execution unit: high historical standards, systematic evidence reuse, aggressive proportional convergence, and durable write-through before execution risk becomes material.**

A completed major stage or required Stage 3A substage boundary is an intentional owner-facing handoff. Evidence classes are research units, not automatically owner-facing stop boundaries. Several small families or classes that use the same research mode should normally be bundled into one meaningful tranche when they can be completed safely.

The owner should not need to manage the research itself. Most major stage/substage transitions require only a short `Proceed` response. Within an authorized stage/substage, routine evidence-class transitions should be handled autonomously unless a genuine owner judgment, a durability boundary, or a materially different research mode requires a stop.

## 2. Authority and startup

At Research-lane startup:

1. inspect current protected `main` and record `research_base_sha`;
2. read current `AGENTS.md` and the controlling research documents it references;
3. read `data/reference/program-top-level-scope.csv` and apply the target school's uncontradicted scope row;
4. identify the owner-supplied school sources and any source-specific authorization limits;
5. begin Stage 1 only.

Repository policy controls over copied handoff wording when they conflict.

A Research lane does not write canonical/global repository state. Research-time global numeric IDs remain provisional. Serialized Implementation performs the authoritative current-main rebase later.

## 3. Common stage rules

### 3.1 Preserve accepted prior stages

Once a stage is complete, its conclusions and durable artifacts are controlling working state. A later stage must not broadly reopen it merely because new work has begun.

Reopen an accepted prior conclusion only when later evidence exposes a **genuine contradiction**. Prefer a narrow correction overlay when game identity/universe remains valid and only a field-level correction is required. Preserve literal source evidence and provenance.

### 3.2 Durable work outranks chat memory

Preserve substantial intermediate ledgers, mappings, censuses, evidence registers, QA results, correction overlays, and hashes whenever the execution environment permits. A replacement chat should be able to recover from durable artifacts without repeating completed research.

A checkpoint is not portable merely because it reports counts. If a stage is incomplete, the durable state must identify the **actual residual rows/labels/items**, not only a statement such as `5 labels remain` or `187 dates remain`.

When practical, emit one owner-facing checkpoint ZIP containing the cumulative accepted continuation state, exact residual queue(s), owner dispositions, completed repairs, QA/status, and manifest/hashes. Supporting constituent files may also be emitted, but the ZIP is the preferred recovery unit.

The checkpoint test is:

> **If this chat disappeared permanently now, could a fresh Research chat attach this checkpoint, verify it, and continue without rediscovering completed work?**

If the answer is no, the checkpoint is not sufficient.

### 3.3 Serialize before extending a substantial research batch

A stage should complete research + mechanical application + artifact emission in one turn when this is safely achievable.

Do not defer all durable serialization until after several expensive research populations have been investigated. Once a substantial coherent population has been resolved, promote that accepted work into the stage's durable working state **before** embarking on another substantial population when the execution environment permits.

This is not a requirement to create tiny owner-facing checkpoints after every few rows. The purpose is to avoid the failure pattern `long research -> more long research -> artifact emission last -> execution boundary -> lost work`.

If substantive research is complete but the full-population mechanical application, census, QA, artifact write, or hashing cannot safely finish in the same turn, **stop cleanly**. The next bounded turn becomes a closeout-only continuation of the same stage. Mechanical closeout comes before new research.

Do not manufacture final counts or hashes that were not actually generated and checked.

### 3.4 Honest incomplete checkpoint is valid

A stage that unexpectedly becomes large may stop before completion. Preserve the exact completed work and the exact residual population, including a row-/label-level remaining queue sufficient for continuation, and do not begin another domain.

An incomplete checkpoint is preferable to unsupported certainty, lost work, or a silent/overlong execution failure.

### 3.5 Workload-bounded execution and anti-microbatching

Evidence classes remain the intellectual unit of research, but an evidence class is **not automatically a turn boundary**. The execution unit should be the largest safely completable tranche that uses a coherent research mode and can be durably written through before context/execution risk becomes material.

Use the workload shape—not elapsed wall-clock time—to size the turn:

- **Systematic/mechanical work:** when one authoritative source structure, event history, facility chronology, reciprocal package family, or deterministic rule can resolve many rows, process the supported population in bulk. Multiple small families that use the same research method should normally be bundled rather than checkpointed one family at a time.
- **Independent row-by-row work:** when resolution requires separate external searching, source comparison, or historical adjudication for individual games, a single turn may adjudicate **no more than 25 rows**.
- **Batching floor in practice:** when a homogeneous independent-row residual contains 25 or fewer rows and no special blocker is present, normally process the whole residual in one turn. Do not manufacture 3–8 row owner handoffs merely because each tiny subset could be described as its own evidence class.
- **Heterogeneous large residuals:** do not interpret "systematic" so broadly that one turn becomes an open-ended campaign across dozens of unrelated families or research modes. Bundle related families; do not attempt the entire heterogeneous residual merely because all rows belong to the same Stage 3A bucket.

The 25-row limit is an **execution cap for independent adjudications, not a research stopping rule**. It does not cap mechanical/systematic application and does not waive unresolved rows.

After a meaningful tranche, write accepted findings through into the cumulative row-level state. Checkpoint when the tranche completes, a genuine contradiction/blocker requires isolation, or execution risk becomes material. A checkpoint exists for durability; it is not a requirement to return to the owner after every small family.

Do not rely on the model to notice elapsed wall-clock time and self-interrupt. Avoid both failure patterns: `large heterogeneous residual -> unbounded discovery -> serialization last -> lost response` and `tiny family -> checkpoint -> owner Proceed -> repeat`.

For Stage 3A specifically, substantial historical research and Stage 3A-4 final mechanical closeout remain separate bounded assignments.

### 3.6 Owner questions remain exceptional

A stage boundary is not an owner historical gate. Contact the owner for substantive judgment only when existing repository policy requires it or a genuine historical ambiguity/contradiction requires owner disposition.

The formal NON_D1 sanity scan remains a required owner checkpoint. Other ordinary major stage/substage transitions are execution authorization only. Do not turn ordinary evidence-class completion into repeated owner interaction.

### 3.7 One-chat baseline; rollover is recovery, not an expected lifecycle step

A Research lane should normally complete in **one chat**. Durable checkpoints exist so the lane can recover cleanly if context, rendering, or execution genuinely degrades; they are not an expectation that the owner routinely open a replacement chat at stage boundaries.

Stay in the same healthy chat across ordinary `Proceed` transitions. Use a replacement chat only when there is concrete operational evidence that continuity is becoming unreliable or the current conversation can no longer safely carry the next bounded assignment.

When rollover is actually necessary, recover from the latest verified portable checkpoint rather than conversational reconstruction. The controlling continuity model remains durable state, and the replacement chat must not reopen completed work.

## 4. Required turn-ending contract

Every bounded Research turn must end in one of the following forms.

### Completed stage

```text
STAGE X: COMPLETE

<concise substantive results, residual counts, artifact/hash status, and any corrections>

Genuine owner questions: NONE
Next bounded stage: Stage X+1 — <name>
STOPPING AT THE REQUIRED STAGE BOUNDARY.
```

If an owner question is genuinely required, replace `NONE` with the concise question and do not imply the next stage is ready.

### Incomplete but healthy stage

```text
STAGE X: INCOMPLETE — DURABLE CHECKPOINT PRESERVED

Completed: <exact completed work>
Remaining: <exact residual work and durable queue artifact(s)>
Checkpoint: <portable ZIP/artifact + verified hash when feasible>
Owner decision required: NO
Next bounded assignment: resume Stage X from this exact checkpoint
STOPPING AT THE REQUIRED STAGE BOUNDARY.
```

An incomplete-stage report without a recoverable residual queue is not a sufficient durable checkpoint merely because aggregate counts are known.

If an owner decision is genuinely required, say so explicitly.

### Required interpretation of owner continuation

After a stage-boundary report, owner responses such as `Proceed`, `Continue`, `Approved, continue`, or substantially equivalent wording authorize **only**:

- the identified next bounded stage, when the prior stage is complete; or
- the identified unfinished remainder of the current stage, when the prior stage is incomplete.

They do **not** authorize running all remaining stages through `RESEARCH_FROZEN` in one turn.

## 5. Stage 1 — Game universe and source ledger

### Objective

Establish the complete competitive game universe and a defensible row-level working ledger.

### Work

- ingest the primary institutional game-history source(s);
- determine played seasons and expected season game counts;
- extract all competitive games through the primary historical endpoint;
- supplement the current/completed season from authoritative institutional sources when required;
- exclude exhibitions/noncompetitive events under repository policy;
- preserve literal source labels/raw evidence;
- resolve duplicate/omitted/bleed rows and game-identity defects;
- apply on-court result policy and document administrative-result differences;
- reconcile every season to authoritative game counts where possible;
- identify genuine exact-date/score/result unknowns without inference;
- establish stable research-local game IDs;
- produce a durable controlling ledger and season reconciliation.

### Internal execution boundary

After primary-source extraction and the first mechanical season census, **serialize the
baseline row ledger before an extended historical discrepancy campaign**.

That baseline should already preserve:

- the complete candidate competitive universe;
- season counts derived from rows;
- explicit exclusions/non-games;
- duplicate/omitted/bleed candidates;
- exact date/score/result discrepancy queues;
- stable research-local game IDs where mechanically possible.

This is an internal durability boundary, not a new owner-facing stop. Continue Stage 1 in
the same authorized turn/chat when healthy, but research subsequent discrepancy families
from this durable baseline rather than keeping the only authoritative state in scratch
reasoning.

Repair discrepancies in coherent evidence families. After substantial work in one
materially different family, write accepted corrections through before opening another.
Do not treat `Stage 1` itself as one giant heterogeneous discrepancy family.

### Completion standard

Stage 1 is complete when:

- the competitive universe is mechanically reconciled;
- season counts are reconciled or source-internal differences are explicitly explained;
- material game-identity/inclusion/duplicate questions are resolved or genuinely owner-blocked;
- accepted corrections are written through with literal evidence preserved;
- surviving exact-date/score/result uncertainties are explicit row-level residuals and do
  not threaten game identity, inclusion, season accounting, or on-court result;
- the controlling ledger and residual queues are durably preserved.

A field may remain unknown without keeping Stage 1 open. In particular, an exact date or
score discrepancy is nonblocking when the game itself, season allocation, inclusion, and
on-court result are independently stable.

Once these completion conditions are met, the required next action is Stage 1
checkpoint/closeout. Do not open another historical source family merely because a missing
field might theoretically be recoverable.

Read `docs/stage1-game-universe-contract.md` for the controlling blocking/nonblocking
criteria and durability requirements.

Do not begin opponent normalization or broad site/venue research in this stage except where necessary to distinguish game identity.

## 6. Stage 2 — Opponent identity

### Objective

Resolve every game to the correct historical/canonical opponent identity without hiding current programs under stale/local/non-D1 identities.

### Work

- normalize literal opponent labels while preserving raw labels;
- research aliases, institutional renames, predecessor/successor questions, branches/campuses, military/club/prep teams, and ambiguous historical names;
- compare suspicious identities against current global program keys and useful published reciprocal alias evidence;
- prevent current-program key splits;
- distinguish true historical non-D1 opponents from current-D1 aliases;
- produce the working distinct `NON_D1` census;
- produce the informational self-corrected-opponent list;
- preserve a game-level opponent mapping and identity provenance.

For obscure historical/NON_D1 opponents, research must remain proportionate to the purpose: establish a defensible canonical identity, avoid false merges/splits, and preserve literal evidence. Do not pursue exhaustive institutional genealogy after available evidence is exhausted when it would not materially affect canonical identity, duplicate handling, or the game universe. Genuine unresolved historical identity remains preferable to unsupported certainty when repository policy permits it.

### Completion standard

- every Stage 1 game has a resolved opponent identity or a genuine owner-level ambiguity;
- unresolved opponent identities = 0 for normal completion;
- known current-program key splits = 0;
- ambiguous current-program matches = 0;
- Stage 1 universe remains accounted exactly;
- opponent artifacts are durable.

The formal owner NON_D1 sanity scan does **not** occur yet; it occurs after package assembly/QA in Stage 5.

## 7. Stage 3A — Regular-season H/A/N and physical venues

### Controlling standard

Read and follow `docs/stage3a-regular-season-site-research.md`. That document is
controlling for Stage 3A research responsibility, venue-completeness expectations,
canonical/shared reuse, stopping, the substage architecture below, and the mandatory
final row-level Stage 3A state.

Stage 3A is **not one monolithic execution unit**. It is divided into five required
substage boundaries. Each substage is a real owner-facing stop boundary.

Within Stages 3A-1 through 3A-3, evidence classes guide research but are **not** mandatory
owner-facing stop boundaries. Bundle multiple small classes that use the same research
mode into a meaningful tranche when safe. A plain owner `Proceed` after a required
Stage 3A substage boundary authorizes the exact next substage; after a durability
checkpoint it authorizes the serialized unfinished tranche.

### Stage 3A-0 — Mechanical census, partition, and project-evidence harvest

This substage is **strictly local-only and mechanical**. It is read-only except for
writing unambiguous accepted same-game project evidence through into the working ledger.
The detailed controlling scope is `docs/stage3a0-local-only-contract.md`.

Allowed evidence is limited to the verified durable checkpoint/working state and
already-present structured project evidence in the checked-out/current protected-main repository.
"Project-evidence harvest" does not authorize reading documents or source files for interpretation.

Before broad historical searching:

1. mechanically partition the exact Stage 1 universe into regular-season Stage 3A rows
   and postseason Stage 3B handoff rows;
2. derive the whole-population H/A/N work census;
3. identify HOME, OPPONENT_HOME, NEUTRAL, and unresolved H/A/N responsibilities;
4. separate NEUTRAL rows into 1996-97+ and 1995-96-and-earlier populations;
5. run the repository-owned deterministic Stage 3A-0 structured-data operation (normally
   `python tools/research_stage3a0.py <school_key> <structured-stage2-ledger.csv>`) and
   perform its one target-school canonical exact-game join;
6. preserve unmatched or contradictory candidates without forcing or researching them;
7. write unambiguous accepted same-game evidence through into the cumulative row-level
   working state;
8. serialize the exact residual queues required by Stage 3A-1 through 3A-3.

**Zero external research is authorized in Stage 3A-0.** Do not search the public web,
institutional athletics sites, media guides, newspapers, external PDFs, or GitHub/code
hosting for new sources. Do not discover opponent source families or investigate venue
candidates externally. Do not inspect opponent packages one-by-one when a structured
local join can produce the same population.

If local project evidence cannot resolve a candidate, preserve it for Stage 3A-1, 3A-2,
or 3A-3. Lack of a local answer is not permission to broaden the search.

Do **not** begin broad HOME chronology research, broad NEUTRAL historical research, or
row-by-row H/A/N adjudication in Stage 3A-0.

Completion response:

```text
STAGE 3A-0: COMPLETE
Next bounded assignment: Stage 3A-1 — H/A/N completion
STOPPING AT THE REQUIRED STAGE 3A SUBSTAGE BOUNDARY.
```

### Stage 3A-1 — H/A/N completion

Resolve the regular-season H/A/N residual before broad venue research.

`docs/stage3a1-source-fanout-contract.md` is controlling for source hierarchy and
fanout. **A bounded row queue does not authorize unbounded source discovery.**

First partition the unresolved H/A/N population into coherent evidence classes. Then work
the **largest safely completable bundle of related classes** that use the same research
mode.

- A systematic source family may resolve a large population in one turn.
- Multiple small opponent/source families should normally be bundled rather than returned
  to the owner one by one.
- If work requires independent row-by-row external research/adjudication, apply the §3.5
  maximum of 25 independent adjudications; when a homogeneous residual is already 25 or
  fewer rows, normally process it as one tranche only when the same small set of source
  families can support that tranche.
- Before external research, define the evidence-class source plan: accepted project
  evidence -> target-school institutional family -> obvious opponent institutional family
  -> at most one specific high-yield authoritative fallback family when justified.
- For one row, normally do not exceed one target-school institutional path plus one
  opponent institutional path after project evidence. A third external path requires a
  specific named authoritative source already identified as plausibly decisive.
- Generic web search is discovery-only. Do not fan out through Reddit, forums, mirrors,
  scraped schedule sites, aggregators, random wikis, or unrelated search results merely
  because institutional evidence did not resolve the row.
- Write accepted H/A/N findings through before the durability boundary.
- Preserve contradictions or genuine researched unknowns explicitly; never infer H/A/N
  from geography.
- Do not start HOME or NEUTRAL venue research merely because H/A/N finishes early in the
  same turn.

**Ancient/historical convergence:** after the whole-population/project-evidence pass and
the obvious systematic institutional/reciprocal/source-family opportunities have been
exhausted, a homogeneous old historical/non-D1 residual may be closed at the population
level as terminal `RESEARCHED_UNRESOLVED` H/A/N debt. Once the bounded authoritative
source hierarchy has been exhausted for a row/class, the mere possibility of another
archive is not a reason to continue searching.

Return an incomplete checkpoint only after a meaningful tranche or when execution risk,
a genuine contradiction, or a materially different research mode requires a stop. When
H/A/N is fully researched/accounted, stop with `STAGE 3A-1: COMPLETE`.

### Stage 3A-2 — HOME venue research

Only after Stage 3A-1 completes, research source-program HOME physical venues.

Use a **facility chronology + default/exception model**:

- establish the program's authoritative home-facility chronology and season-level home
  evidence;
- when a normal home venue is systematically established for a season/era and there is
  no evidence of an alternate site, apply that supported venue across the exact covered
  HOME population rather than re-proving the building through individual box scores;
- use count mismatches, explicit source text, alternate-site markers, temporary/off-campus
  evidence, or contradictions to isolate exception rows for exact-game research;
- explicit game-level evidence always overrides the systematic default;
- bundle related facility eras/classes that use the same research mode when safe;
- if separate row-level adjudications are required, apply the §3.5 maximum of 25;
- write accepted venue/location/provenance findings through before the durability boundary.

For ancient HOME residuals, after the reasonable institutional/facility/reciprocal and
other obvious systematic paths are exhausted, close the homogeneous residual under
`RESEARCHED_UNRESOLVED_HOME_VENUE` rather than creating one archaeology project per
game. **Before Stage 3A-2 may complete, every such row must also have supported city/state
geography written through.** Systematically established source-program home geography may
be propagated across already-established HOME rows when no accepted evidence indicates an
alternate/off-campus location; this is geography propagation, not H/A/N inference.
Isolate exceptions rather than forcing the default.

Ordinary OPPONENT_HOME building blanks are not an active HOME research queue.

When all HOME obligations and HOME geography are researched/accounted, stop with
`STAGE 3A-2: COMPLETE`.

### Stage 3A-3 — NEUTRAL venue research

Only after Stage 3A-2 completes, research remaining regular-season NEUTRAL physical
venues.

`docs/stage3a3-neutral-tranche-contract.md` is controlling for Stage 3A-3 tier
boundaries, tranche sizing, source fanout, and recovery.

The Stage 3A-0 exact-game harvest remains controlling project evidence and must not be
repeated wholesale unless a specific contradiction or changed project state makes a
narrow recheck necessary.

Use this default execution order:

1. **mechanical accepted-evidence application** already present in the durable state;
2. **1996-97+ recurring event/site families**, using event/host/tournament history and
   default-plus-exceptions family evidence;
3. **1996-97+ one-offs**, under the strong exact-venue standard;
4. one **1995-96-and-earlier historical location-enrichment pass** across the remaining
   regular-season neutral residual.

After substantial research begins in one tier, **do not cross into the next materially
different tier in the same turn**. Finish the active tier/tranche, write accepted findings
through, serialize the exact residual by tier, and stop at a durable continuation point.
The owner should normally need only `Proceed` to continue.

For recurring families, prove the event/site pattern once for the exact covered editions
and apply it systematically; research only genuine exceptions or multi-venue editions
individually. Do not re-prove the same venue game by game.

Use this source hierarchy for recurring families:

1. accepted project/canonical/reciprocal evidence;
2. official event/tournament/host institutional source family;
3. target-school or obvious participant institutional source family;
4. at most one specific high-yield authoritative fallback family when justified.

For the historical location-enrichment pass, mechanically regroup the remaining residual
by obvious event/opponent/locality structures when useful, but do not turn those groups
into separate exact-building research obligations. Use accepted project evidence plus the
obvious systematic event/host/participant institutional opportunity. Preserve supported
event identity and city/state; accept an exact building when that same evidence directly
supplies it.

Once city/state is supported, do not open another source path solely to recover the exact
building. Terminalize the blank building as historical enrichment debt. If locality itself
remains unsupported after the obvious systematic opportunity, preserve the researched
unknown rather than escalating into row-level archive research.

The independent-adjudication ceiling still applies when the historical pass unexpectedly
breaks into genuinely separate row-level adjudications, but the normal goal is one
population-level location pass rather than repeated small owner-facing packages.

Do not infer a venue from city, event custom, nearby editions, opponent home arena, or
chronology alone. Write accepted venue/location/provenance findings through before the
durability boundary. When all NEUTRAL obligations are researched/accounted, stop with
`STAGE 3A-3: COMPLETE`.

### Stage 3A-4 — Mechanical closeout and QA

This is a **mechanical closeout substage**, not another historical research pass.

Do not launch broad new historical searching here. If closeout exposes a genuine
historical contradiction or a missing required research population, stop and return that
specific population to the appropriate earlier Stage 3A substage.

Otherwise:

1. regenerate or supersede the single authoritative row-level Stage 3A ledger;
2. reconcile the exact regular-season/postseason handoff partition to Stage 1;
3. derive the final regular-season H/A/N census from rows;
4. identify valid HOME researched-unresolved exceptions;
5. identify NEUTRAL researched debt by modern (1996-97+) vs historical (1995-96 and earlier) era;
6. identify OPPONENT_HOME rows intentionally outside source-school building responsibility;
7. run Stage 3A QA;
8. serialize/hash the final Stage 3A completion checkpoint.

Stage 3A may declare complete only after Stage 3A-4 passes. The completion state must
include:

- exact Stage 1 partition accounting;
- final regular-season H/A/N census derived from row-level state;
- HOME venue gaps limited to valid researched-unresolved HOME exceptions;
- ordinary OPPONENT_HOME venue blanks excluded from active source-school research;
- modern neutral rows (1996-97+) subjected to the strong exact-venue pass;
- historical regular-season neutral rows (1995-96 and earlier) subjected to the location-first systematic pass, with supported event/city/state preserved and surviving exact-building gaps allowed as explicitly accounted nonblocking terminal enrichment debt;
- every material unresolved site fact explicitly researched/accounted;
- ambiguous physical venue identities = 0;
- one authoritative row-level Stage 3A ledger sufficient for a successor chat and Stage 4.

Completion response:

```text
STAGE 3A: COMPLETE
Next bounded stage: Stage 3B — Postseason classification and sites
STOPPING AT THE REQUIRED STAGE BOUNDARY.
```

## 8. Stage 3B — Postseason classification and sites

### Objective

Close conference-tournament, NCAA, NIT, and other postseason classification/site research.

### Work

- identify the exact postseason population and taxonomy;
- normalize controlled rounds under repository policy;
- research H/A/N independently from physical venue identity;
- research **every postseason game's exact physical venue + city/state to exhaustion** across NCAA, NIT, conference tournaments, and other postseason events;
- research conference-tournament sites, including split-site/campus-round structures and host-site exceptions;
- for confirmed conference-tournament rows, consult `data/reference/conference-tournament-sites.csv.gz.b64` through `tools/conference_tournament_reference.py` before external site research;
- treat a season/conference/date-or-round-scope-matching `COMPLETE` row under `docs/conference-tournament-site-reference.md` as accepted shared project evidence for physical venue/city/state unless material contradictory authoritative evidence is present;
- do not use the shared reference to establish postseason classification or H/A/N, and continue normal Stage 3B research to exhaustion for absent, `PARTIAL`, `UNCERTAIN`, `UNRESOLVED`, campus-round, boundary-mismatched, or contradicted cases;
- use official tournament/conference/host/participant sources and targeted archival evidence as needed until the reasonable authoritative paths are exhausted;
- reconcile physical venue aliases/naming eras;
- preserve correction overlays when stronger postseason evidence corrects a Stage 1 field without changing game identity.

The historical regular-season neutral shortcut does **not** apply to Stage 3B. Do not stop
postseason exact-venue research merely because city/state is known. Exact building identity
remains an active research obligation for NCAA, NIT, conference-tournament, and every other
postseason row.

### Completion standard

- complete postseason partition and H/A/N census;
- NCAA physical venue + city + state gaps = 0;
- NIT, conference-tournament, and other postseason exact-venue gaps have been researched to exhaustion and any genuinely unrecoverable survivor is explicitly documented with the exact authoritative paths exhausted;
- no postseason row is terminalized under the historical regular-season neutral enrichment shortcut;
- ambiguous physical venue identities = 0;
- postseason + regular-season partitions account exactly for Stage 1;
- durable mapping/audit artifacts emitted when feasible.

Do not begin six-file finalization during this stage unless the stage itself is already fully closed and the owner has separately authorized the next bounded stage; normally stop here.

## 9. Stage 4 — Six-file package assembly and package QA

### Objective

Mechanically assemble the researched school portfolio and reach readiness for the required owner NON_D1 sanity scan.

### Work

Construct exactly the current-schema six flat files:

1. `source-games.csv`
2. `opponents.csv`
3. `venues.csv`
4. `conferences.csv`
5. `notes.md`
6. `source-notes.md`

Then:

- apply accepted Stage 1–3B research mechanically;
- apply documented correction overlays without erasing literal raw evidence;
- establish conference chronology/accomplishment/source notes required by current schema/policy;
- run applicable research/package QA and repair mechanical defects;
- reconcile venue identities against `research_base_sha` while keeping new numeric global IDs provisional;
- confirm site-completeness accounting and NCAA completeness;
- generate the complete distinct working `NON_D1` owner-scan presentation;
- include the informational self-corrected-opponent section.

### Completion standard

Stage 4 ends at:

```text
STAGE 4: COMPLETE — OWNER NON_D1 SANITY SCAN READY
```

Package QA should be clean under current research tooling/policy, the six-file portfolio should be complete, and the complete owner-scan population should be ready.

Do **not** approve the NON_D1 population on the owner's behalf. Do not begin final self-challenge or freeze.

## 10. Stage 5 — Owner NON_D1 sanity scan

### Objective

Execute the required lightweight owner checkpoint in `docs/non-d1-owner-sanity-scan.md`.

### Agent action

Present the owner with the complete distinct `NON_D1` list, including required counts/raw labels/disambiguation notes, plus the informational self-corrected identities.

Then stop for actual owner review.

### Owner response

The owner may approve with simple language (`looks good`, `approved`, etc.) or flag entries for bounded follow-up.

### If entries are flagged

Research only the flagged identity population and mechanically dependent package fields. Explain or correct each flag, rerun affected QA, and return to the owner if a genuine disposition remains necessary.

Do not reopen unrelated research.

### Completion standard

Record the owner disposition durably. No owner-flagged identity may remain unexplained at the freeze point. A later recovery must not require the owner to repeat a completed Stage 5 approval when the preserved disposition verifies cleanly.

After clean approval, the next bounded stage is Stage 6.

## 11. Stage 6 — Final adversarial self-challenge and bounded repair

### Objective

Perform the required final Research-lane adversarial review under `docs/research-freeze-self-challenge.md` after the owner NON_D1 checkpoint.

### Work

Challenge the largest/suspicious residual populations, especially:

- researched-unresolved HOME venues;
- UNKNOWN H/A/N;
- exact-date debt;
- neutral/postseason site debt;
- physical venue identity candidates;
- suspicious opponent/current-program identities;
- surprising modern/institutional series gaps.

Use the controlling self-challenge document for the evidence/accounting standard.

If a real defect is exposed, repair only the affected research fields, rerun affected package QA, and refresh dependent artifacts/hashes. Do not restart the school.

### Terminal-debt stopping rule

Stage 6 is an adversarial audit, not a command to eliminate every permitted historical unknown. **Residual populations enter Stage 6 as accepted researched debt from completed earlier stages, not as freshly reopened research queues.**

For each meaningful residual class:

1. challenge the population as a class;
2. identify a concrete contradiction, material deficiency, or specific systematic/high-yield opportunity that could materially change the class;
3. repair supported defects in batch and isolate genuine contradictions narrowly;
4. once that systematic opportunity is exhausted, return the surviving rows immediately to **terminal researched historical debt** unless another comparably concrete opportunity is already identified.

The burden is on the self-challenge to justify reopening a portion of the accepted debt. The mere existence of unresolved rows does not do so.

Do not recursively treat every smaller remainder as a new mandate for exhaustive row-by-row research. Do not stop for owner interaction after one or two ordinary repairs if the same systematic challenge can safely continue across the class. Large residual counts are review triggers, not zero-unknown requirements.

For exact-date debt, pursue concentrated institutional/reciprocal opportunities (for example, a large opponent series) as class-level challenges; if the concentrated source does not materially resolve the population, terminalize the survivors rather than switching to newspaper archaeology.

### Completion standard

Stage 6 ends only when the required self-challenge passes and package-level research acceptance is clean, including:

- research acceptance errors = 0;
- research acceptance warnings = 0;
- unresolved opponent identities = 0;
- known current-program key splits = 0;
- ambiguous current-program matches = 0;
- HOME publication blockers = 0;
- NCAA site gaps = 0;
- unaccounted material site gaps = 0;
- ambiguous physical venue identities = 0;
- `PRE-FREEZE SELF-CHALLENGE: PASS`.

Stop at the stage boundary. Do not silently proceed into immutable packaging unless the owner authorizes Stage 7.

## 12. Stage 7 — Immutable package and RESEARCH_FROZEN

### Objective

Create and verify the final immutable research package from the accepted six-file portfolio.

### Work

- confirm exactly six flat package files;
- generate final manifest/file hashes;
- create immutable ZIP;
- calculate and verify ZIP SHA-256;
- create the final Research Freeze status card;
- preserve owner NON_D1 disposition and self-challenge result in supporting durable artifacts;
- confirm the package still matches the final accepted QA state.

### Completion standard

Return the final package/hash and status card, ending with:

```text
RESEARCH_FROZEN: YES
CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES
```

This is the terminal Research-lane state. Do not begin serialized Implementation in the Research lane.

## 13. Stage sizing and recovery

The numbered stages are the normal domain boundaries, not a command to force every school into identically sized turns.

If a stage is unusually large, split **within that same stage** at a natural residual boundary and use the incomplete checkpoint contract. The next turn resumes the same stage. Do not return merely because a few rows were resolved; a bounded unit should normally make a meaningful reduction in a coherent population unless a genuine blocker or execution boundary intervenes.

If a stage is small enough to research, mechanically close, QA, write artifacts, and hash safely in one turn, do so; do not create artificial extra turns merely to follow an A/B naming scheme.

Do not use clock-based heartbeat rules as a substitute for bounded objectives. The execution unit is defined by work scope, not a promised number of minutes.

### Recovery after interruption or chat replacement

Recovery should be mechanical and artifact-first:

1. locate the latest portable checkpoint ZIP/artifact, including File Library when the visible prior response is unavailable;
2. verify its hash/manifest and accepted owner dispositions;
3. load the exact serialized residual queue(s);
4. resume only the earliest incomplete bounded stage from those queues;
5. do not perform open-ended conversational archaeology, hidden-workspace searching, or broad reconstruction of completed work merely because a prior chat mentioned it;
6. if the required residual queue is genuinely missing, stop and identify the exact missing artifact/state before authorizing reconstruction;
7. do not restart completed research absent a genuine contradiction.

The desired recovery experience is: **attach checkpoint -> verify -> continue**.

## 14. Relationship to existing policy

This document controls **Research-lane turn boundaries and continuation semantics**.

Existing documents remain controlling for their substantive domains, including:

- `docs/stage3a0-local-only-contract.md` — strict local-only Stage 3A-0 execution scope;
- `docs/stage3a1-source-fanout-contract.md` — bounded Stage 3A-1 source hierarchy and convergence;
- `docs/stage3a3-neutral-tranche-contract.md` — bounded Stage 3A-3 neutral tiers, source fanout, and convergence;
- `docs/site-completeness-protocol.md` — site research/accounting and NCAA completeness;
- `docs/non-d1-owner-sanity-scan.md` — required owner NON_D1 checkpoint;
- `docs/research-freeze-self-challenge.md` — final adversarial acceptance review;
- `docs/program-top-level-scope-reference.md` and `data/reference/program-top-level-scope.csv` — accepted top-level history scope;
- `docs/parallel-portfolio-pipeline.md` — research freeze vs integration freeze and current-main rebase;
- current schema/onboarding documents referenced by `AGENTS.md`.

Where an older document says a Research lane should automatically continue through multiple research phases without an owner continuation message, this bounded-execution protocol is controlling **only as to the stage-boundary stop/continue behavior**.

Historical standards, owner decision authority, and freeze requirements are not relaxed.