# Research Lane Bounded Execution Protocol

- **Status:** Controlling Research-lane turn-execution protocol
- **Applies to:** new school Research lanes and recovery of unfinished Research lanes
- **Does not replace:** historical/data-quality policy, six-file schema, site-completeness policy, opponent-identity policy, NON_D1 owner sanity scan, or research-freeze self-challenge
- **Pilot basis:** empirically validated during Kansas State research, September 2026

## 1. Purpose

Research quality standards are unchanged. This protocol changes **how autonomous research is divided into chat turns** so substantial work ends at deliberate, recoverable boundaries rather than attempting an entire school in one unbounded turn.

The governing rule is:

> **One bounded research objective per turn. A completed stage boundary is an intentional execution handoff. Do not automatically begin the next stage.**

The owner should not need to manage the research itself. Most stage transitions require only a short `Proceed` response. That response authorizes the next bounded unit of execution; it is not an owner adjudication of historical facts.

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

### 3.3 Mechanical closeout may split from research

A stage should complete research + mechanical application + artifact emission in one turn when this is safely achievable.

If substantive research is complete but the full-population mechanical application, census, QA, artifact write, or hashing cannot safely finish in the same turn, **stop cleanly**. The next bounded turn becomes a closeout-only continuation of the same stage.

Do not manufacture final counts or hashes that were not actually generated and checked.

### 3.4 Honest incomplete checkpoint is valid

A stage that unexpectedly becomes large may stop before completion. Preserve the exact completed work, identify the exact residual population, and do not begin another domain.

An incomplete checkpoint is preferable to unsupported certainty, lost work, or a silent/overlong execution failure.

### 3.5 Owner questions remain exceptional

A stage boundary is not an owner historical gate. Contact the owner for substantive judgment only when existing repository policy requires it or a genuine historical ambiguity/contradiction requires owner disposition.

The formal NON_D1 sanity scan remains a required owner checkpoint. Other ordinary stage transitions are execution authorization only.

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
Remaining: <exact residual work>
Owner decision required: NO
Next bounded assignment: resume Stage X from this exact checkpoint
STOPPING AT THE REQUIRED STAGE BOUNDARY.
```

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

### Completion standard

Stage 1 is complete when the competitive universe is mechanically reconciled, material game-identity questions are resolved or explicitly owner-blocked, and the controlling ledger is durably preserved.

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

### Completion standard

- every Stage 1 game has a resolved opponent identity or a genuine owner-level ambiguity;
- unresolved opponent identities = 0 for normal completion;
- known current-program key splits = 0;
- ambiguous current-program matches = 0;
- Stage 1 universe remains accounted exactly;
- opponent artifacts are durable.

The formal owner NON_D1 sanity scan does **not** occur yet; it occurs after package assembly/QA in Stage 5.

## 7. Stage 3A — Regular-season H/A/N and physical venues

### Objective

Research H/A/N classification and physical venue/site identity for the non-postseason population while keeping those two concepts independent.

### Work

- establish home-facility chronology from authoritative evidence;
- research alternate/temporary/off-campus home games rather than bulk-assigning solely from era;
- resolve H/A/N from explicit/game-level evidence, never geography inference;
- research recurring neutral events and one-off neutral sites;
- distinguish venue naming eras/aliases from physical buildings;
- identify research-base registry reuses versus genuinely new physical venue candidates;
- preserve researched unresolved building identity where evidence is insufficient;
- quantify UNKNOWN H/A/N and material site debt by era;
- maintain explicit site-research accounting required by `docs/site-completeness-protocol.md`.

### Completion standard

Produce a mechanically closed regular-season population with:

- final H/A/N census;
- UNKNOWN H/A/N count and era concentration;
- HOME physical-venue unresolved count and era concentration;
- regular-season neutral physical-venue unresolved count;
- ambiguous physical venue identities = 0;
- game-level/site working state preserved durably;
- exact partition/accounting against the Stage 1 universe.

If research converges but full mechanical closeout/artifact emission does not fit safely in the same turn, use the closeout rule in §3.3 and resume Stage 3A only.

## 8. Stage 3B — Postseason classification and sites

### Objective

Close conference-tournament, NCAA, NIT, and other postseason classification/site research.

### Work

- identify the exact postseason population and taxonomy;
- normalize controlled rounds under repository policy;
- research H/A/N independently from physical venue identity;
- research conference-tournament sites, including split-site/campus-round structures;
- use owner-supplied tournament-site references only within their explicitly authorized school/conference scope and cross-verify prudently;
- research NCAA Tournament physical venue + city + state completely;
- research NIT/other postseason sites and explicitly account for any genuine residual unknowns;
- reconcile physical venue aliases/naming eras;
- preserve correction overlays when stronger postseason evidence corrects a Stage 1 field without changing game identity.

### Completion standard

- complete postseason partition and H/A/N census;
- NCAA physical venue + city + state gaps = 0;
- conference/NIT/other material site gaps explicitly researched/accounted;
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

Record the owner disposition. No owner-flagged identity may remain unexplained at the freeze point.

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

If a stage is unusually large, split **within that same stage** at a natural residual boundary and use the incomplete checkpoint contract. The next turn resumes the same stage.

If a stage is small enough to research, mechanically close, QA, write artifacts, and hash safely in one turn, do so; do not create artificial extra turns merely to follow an A/B naming scheme.

Do not use clock-based heartbeat rules as a substitute for bounded objectives. The execution unit is defined by work scope, not a promised number of minutes.

After interruption or chat replacement:

1. inspect durable artifacts and the last valid stage report;
2. verify accepted prior-stage fingerprints/hashes where available;
3. resume from the earliest incomplete bounded stage;
4. do not restart completed research absent a genuine contradiction.

## 14. Relationship to existing policy

This document controls **Research-lane turn boundaries and continuation semantics**.

Existing documents remain controlling for their substantive domains, including:

- `docs/site-completeness-protocol.md` — site research/accounting and NCAA completeness;
- `docs/non-d1-owner-sanity-scan.md` — required owner NON_D1 checkpoint;
- `docs/research-freeze-self-challenge.md` — final adversarial acceptance review;
- `docs/program-top-level-scope-reference.md` and `data/reference/program-top-level-scope.csv` — accepted top-level history scope;
- `docs/parallel-portfolio-pipeline.md` — research freeze vs integration freeze and current-main rebase;
- current schema/onboarding documents referenced by `AGENTS.md`.

Where an older document says a Research lane should automatically continue through multiple research phases without an owner continuation message, this bounded-execution protocol is controlling **only as to the stage-boundary stop/continue behavior**.

Historical standards, owner decision authority, and freeze requirements are not relaxed.