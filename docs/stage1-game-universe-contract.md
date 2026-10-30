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
   - record the **primary-source historical results cutoff** from the actual completed
     results contained by the source, never from a media-guide title or filename;
   - separately record the **required completed-season cutoff** for the target Research
     package. If that cutoff is later than the primary-source cutoff, supplement the
     missing completed season(s) from the current official institutional schedule/results
     source rather than treating the primary source's normal preseason cutoff as the end
     of the game universe;
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

Nonblocking does not mean “ignore.” Every surviving identifiable-game residual must be explicit, row-level, and provenance-preserving.

### Narrow exception: source-acknowledged unidentified historical games

An institution may explicitly acknowledge that one or more historical games are absent from its detailed game list while the identity of those games is not recoverable. Those *unidentified games* have no defensible row-level identity. Their source-acknowledged omission is a **season-level coverage gap**, not permission to create an anonymous game row or to silently declare the published game universe exhaustive.

A bounded Stage 1 closeout may carry such gaps **without holding every otherwise identified game hostage**, but only when **all** the following apply:

1. The primary institutional source itself explicitly identifies the affected season and the **number of missing games** (an inferred gap from a secondary record total alone does not qualify). Preserve its exact note, source page/context, detailed-game tally, and any conflicting season heading/aggregate separately.
2. The accepted competitive-game ledger has stable unique IDs, source-backed opponent labels, structured game types, reconciled inclusions/exclusions, and all other Stage 1 universe defects resolved. No unidentified game is added to the ledger, game counts, or canonical game identities.
3. Bounded institutional/obvious reciprocal/source-family research has genuinely failed to identify each absent game's opponent or other sufficient same-game identity. The investigated authoritative paths and exact evidentiary limits are serialized. Do not continue an unbounded source campaign solely to clear an acknowledged source omission.
4. The number of unidentified games, source count note, ledger/census difference, and remaining discrepancy records reconcile. A season whose detailed row tally already matches its heading **must still retain** a conflicting explicit missing-game note and must not invent an additional win or loss from a secondary aggregate.
5. **Every other Stage 1 blocker is absent.** This is never a waiver for uncertain inclusion of *identified* rows, suspected duplicates, game-type/season allocation, omitted extractable games, or unresolved on-court results on identified games.
6. The repository-owned read-only check `tools/research_stage1_coverage_gap.py` reports `ELIGIBLE_FOR_SOURCE_ACKNOWLEDGED_COVERAGE_GAP` against an exact SHA-pinned, manifest-verified checkpoint and its manifested bounded-research evidence. Eligibility is not itself a Stage 1 COMPLETE checkpoint or an authorization to enter Stage 2.

The Research lane then makes **one explicit, separately hashed Stage 1 closeout successor** preserving the original checkpoint byte-for-byte as parent and carrying the unchanged identified-game ledger, source/literal evidence, season-census contradiction, the exact season-level missing-game counts and research exhaustion, and the audit report. It reclassifies *only* those qualifying blocker records as terminal `SOURCE_ACKNOWLEDGED_UNIDENTIFIED_GAME_GAP` coverage records. Keep identified-game count and unidentified-game count separate in downstream Stage 2 / Research Freeze / Implementation handoffs and any public coverage statement. Never represent the missing games as canonical games or silently adopt an aggregate record as the verified per-game W/L sum. Reopen only when new concrete evidence establishes a real game identity.

This exception creates no automatic school-specific exemption or new owner gate. A genuine contrary historical judgment still belongs to the owner. All other Stage 1 completion, documentation, and acceptance rules remain unchanged.

### Separate narrow exception: terminal early-history uncertainty

Some inception/founding-era evidence can be honest, authoritative, and permanently incomplete without fitting the counted-gap exception above. Stage 1 may close through the separate `EARLY_HISTORY_UNCERTAINTY` path only after the repository-owned read-only `tools/research_stage1_early_history_uncertainty.py` independently verifies the exact checkpoint chain.

Two classes are eligible:

1. **Unquantified founding-era season coverage** — authoritative institutional/comparable evidence establishes that the program/team existed in the inception/founding era, but neither an exact competitive-game count nor zero competitive games is established after bounded manifested research. Identified games remain ordinary rows; no anonymous/placeholder game or expected count may be invented. An explicit source missing-game count is **not** eligible here and remains governed exclusively by the existing counted-gap path above.
2. **Identified competitive games with genuinely unknown results** — each affected game has a stable research ID, season, literal opponent evidence, competitive inclusion, and structured game type, while both scores and the on-court W/L/T remain unknown after bounded manifested research. Do not allocate outcomes from aggregate records or discard direct literal score/result evidence.

Common safeguards:

- exact parent/candidate SHA pins, manifest verification, immutable `research_base_sha`, unique stable IDs, and zero unrelated Stage 1 blockers are mandatory;
- known-result W/L/T totals are computed only from rows whose outcome is actually known;
- `audit-candidate` authenticates the unchanged historical ledger/census plus manifested `early-history-uncertainty.json` and may emit only `ELIGIBLE_FOR_EARLY_HISTORY_UNCERTAINTY_CLOSEOUT`; it always leaves `stage1_complete: false`;
- the Research lane then creates one separately hashed closeout successor, preserving the audited ledger/census unchanged, binding the audit hash, reclassifying only the accepted terminal debt, and seeding an identical `stage4-authoring/early-history-uncertainty.json` payload for later Research carry-through;
- `verify-closeout` independently verifies that successor and is the only path that permits `STAGE_1 / COMPLETE` with terminal codes `EARLY_HISTORY_UNQUANTIFIED_SEASON_COVERAGE` and/or `EARLY_HISTORY_IDENTIFIED_GAME_RESULT_UNKNOWN`;
- the metadata is durable historical uncertainty authority, not permission for later stages to fill a score/result, manufacture a game, or infer a season total.

This path is generic and evidence-preserving. It creates no school-specific waiver and no additional owner gate.

## 4. Stage 1 convergence rule

Once all of the following are true:

- the **identified** competitive-game universe is mechanically reconciled, with any source-acknowledged unidentified-game coverage gap separately audited under §3 and any terminal early-history uncertainty separately audited/verified under the narrow exception above;
- every season census is reconciled or its source-internal discrepancy is explicitly explained, including the approved §3 counted-gap representation or an independently verified unquantified founding-era coverage record;
- the target game universe reaches its explicitly declared required completed-season
  cutoff, even when the primary media guide/record book naturally stops one completed
  season earlier;
- duplicate/omitted/bleed/inclusion questions are resolved or genuinely owner-blocked;
- stable research-local game IDs exist;
- every game has a structured `game_type` sufficient to distinguish `REGULAR_SEASON` from postseason; this is a Stage 1 invariant for new Research lanes and Stage 2 must preserve it unchanged;
- accepted corrections are written through with literal evidence preserved;
- remaining field-level unknowns are explicitly queued and do not threaten game identity, inclusion, season accounting, or on-court result, except for exact terminal Class B result-unknown rows independently verified under the early-history uncertainty path;

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
- exact residual queue grouped by defect class, plus any separately audited source-acknowledged unidentified-game coverage record with institution's literal count note, season/source, evidence exhaustion, the preserved aggregate/ledger contradiction, and original parent checkpoint SHA;
- stable research-local IDs;
- structured `game_type` on every game, with postseason identity sufficient for the later mechanical Stage 3A/3B partition;
- provenance/literal-source preservation;
- explicit `primary_source_historical_cutoff` and
  `required_completed_season_cutoff` declarations, or an equivalent manifested
  durable representation carried forward for Stage 4;
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
- deriving a source-results cutoff from a media-guide title/filename, or treating a
  normal preseason guide cutoff as permission to omit a later already-completed target season;
- reopening already reconciled seasons merely because another source family exists;
- moving from one unrelated discrepancy family to another without writing accepted repairs through;
- continuing research after the completion conditions in §4 are already satisfied;
- allowing a long Stage 1 turn to consume the chat while the authoritative ledger exists only in scratch reasoning.

The intended experience is:

> **extract/census -> durable baseline -> bounded discrepancy repair -> mechanical closeout -> Stage 1 checkpoint -> stop**
