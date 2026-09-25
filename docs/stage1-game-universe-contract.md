# Stage 1 Game-Universe Durability Contract

- **Status:** Controlling Research Stage 1 execution/stopping contract
- **Applies to:** new-school Stage 1 game-universe construction and Stage 1 recovery
- **Does not replace:** historical inclusion policy, on-court result policy, program-scope policy, literal-source preservation, or later-stage opponent/site research
- **Purpose:** preserve rigorous game-universe reconciliation without turning Stage 1 into one unbounded historical discrepancy campaign before durable state exists

## 1. Governing principle

> **Establish and serialize the mechanical game universe first; then repair discrepancies in bounded evidence families; close Stage 1 once game identity and season accounting are stable even if explicitly nonblocking field unknowns remain.**

Stage 1 owns game-universe truth. It does **not** require every historical date or score field to become known before a durable ledger may exist or before Stage 1 may close.

Unknown is preferable to unsupported certainty.

## 2. Required internal execution shape

Stage 1 has one owner-facing stage boundary, but internally it should proceed in this order:

1. **Primary-source inventory and extraction**
   - understand the source structure before row extraction;
   - establish played seasons and source season headings/counts;
   - extract the complete candidate competitive-game ledger;
   - preserve literal source text/labels;
   - separate obvious non-games such as cancellations, postponements, exhibitions, and duplicate representations.

2. **Mechanical baseline reconciliation**
   - assign stable research-local game IDs;
   - calculate season game counts from rows;
   - identify season-count mismatches;
   - identify duplicate/bleed/omitted-row candidates;
   - identify exact-date/score/result blanks or contradictions;
   - preserve administrative/vacated-result annotations separately from on-court participation.

3. **Durable baseline serialization**
   - once the candidate universe, season census, exclusions, and discrepancy classes are mechanically known, write the row-level ledger and exact residual queues durably **before** opening an extended historical discrepancy campaign;
   - this is an internal durability boundary, not a new owner gate;
   - if the chat vanished at this point, another chat must be able to continue Stage 1 without re-extracting the institutional source.

4. **Bounded discrepancy repair**
   - research coherent discrepancy families rather than “all remaining Stage 1 uncertainty” as one task;
   - examples include season-count mismatches, duplicate/bleed candidates, score/result contradictions, exact-date contradictions, and administrative-result anomalies;
   - after substantial work in one materially different evidence family, write accepted corrections through before opening another family;
   - do not recursively broaden source discovery merely because a field remains unknown.

5. **Mechanical closeout**
   - rederive the authoritative universe and season census from rows;
   - verify inclusions/exclusions and duplicate accounting;
   - serialize accepted corrections and exact surviving residuals;
   - checkpoint/hash the controlling Stage 1 state;
   - stop before Stage 2.

## 3. Blocking versus nonblocking residuals

A Stage 1 residual is **blocking** when unresolved uncertainty could materially change:

- whether a row represents a played competitive game;
- whether two rows are the same real game;
- season allocation or season game count;
- inclusion/exclusion of a game;
- on-court win/loss/tie result;
- another fact required to keep the Stage 1 universe internally consistent.

A Stage 1 residual may be **nonblocking** when game identity/inclusion and season accounting are stable, including examples such as:

- exact date unknown within an established season when the game itself is unambiguous;
- exact score unknown or contradictory when the on-court result and game identity are independently established;
- source-internal season-heading/summary discrepancies whose detailed game list and independent institutional season record establish the game universe;
- administrative/vacated-result differences when on-court participation and result policy are explicitly preserved;
- literal-source defects where a stronger same-source or authoritative source supports the curated field and the literal defect remains preserved.

Nonblocking does not mean “ignore.” Every surviving residual must be explicit, row-level, and provenance-preserving.

## 4. Stage 1 convergence rule

Once all of the following are true:

- the competitive game universe is mechanically reconciled;
- every season census is reconciled or its source-internal discrepancy is explicitly explained;
- duplicate/omitted/bleed/inclusion questions are resolved or genuinely owner-blocked;
- stable research-local game IDs exist;
- accepted corrections are written through with literal evidence preserved;
- remaining field-level unknowns are explicitly queued and do not threaten game identity, inclusion, season accounting, or on-court result;

the next required action is **Stage 1 closeout/checkpoint**, not another historical source family.

Do not continue researching merely because another newspaper, yearbook, opponent schedule, archive, or repository may theoretically contain a missing exact date or score.

## 5. Source-fanout discipline

Stage 1 may use external authoritative evidence when needed to reconcile the game universe. This contract does not impose a local-only rule.

However:

- define the discrepancy class before opening a new source path;
- prefer institutional/systematic sources that can resolve a coherent population;
- a row-level discrepancy does not authorize an open-ended audit of adjacent seasons/opponents;
- once a discrepancy is proven nonblocking under §3, continued searching requires a concrete reason it could still change the Stage 1 universe or on-court result;
- do not mix several unrelated historical source families into one long pre-checkpoint pass.

## 6. Durable checkpoint requirements

A complete Stage 1 checkpoint should contain, directly or through its manifest:

- authoritative row-level working ledger;
- exact game-universe count;
- season census/reconciliation;
- excluded non-game rows;
- accepted corrections ledger;
- exact residual queue grouped by defect class;
- stable research-local IDs;
- provenance/literal-source preservation;
- completion status and next bounded stage;
- manifest/hash verification when the environment supports it.

An incomplete Stage 1 checkpoint must additionally identify the exact unfinished discrepancy population and the next bounded repair family.

Aggregate counts alone are not sufficient recovery state.

## 7. Owner interaction

This contract creates **no new owner-facing substage**.

The normal owner experience remains:

`initial Stage 1 assignment -> STAGE 1 COMPLETE -> Proceed to Stage 2`

Return early only for:

- genuine owner-level inclusion/scope/game-identity judgment;
- corrupted/unrecoverable source state;
- a necessary durability stop because execution/context is degrading.

Routine internal transitions from extraction to baseline serialization to discrepancy repair do not require owner approval.

## 8. Anti-patterns

Flag and stop these Stage 1 behaviors:

- extracting the full universe but postponing all serialization until every historical discrepancy is researched;
- treating every exact-date or score blank as a Stage 1 blocker;
- reopening already reconciled seasons merely because another source family exists;
- moving from one unrelated discrepancy family to another without writing accepted repairs through;
- continuing research after the completion conditions in §4 are already satisfied;
- allowing a long Stage 1 turn to consume the chat while the authoritative ledger exists only in scratch reasoning.

The intended experience is:

> **extract/census -> durable baseline -> bounded discrepancy repair -> mechanical closeout -> Stage 1 checkpoint -> stop**
