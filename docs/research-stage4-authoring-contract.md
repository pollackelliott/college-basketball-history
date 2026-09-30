# Research Stage 4 Authoring Durability Contract

- **Status:** Controlling for new/current-policy Research lanes
- **Goal:** make Stage 3B COMPLETE -> Stage 4 package -> owner NON_D1 scan a deterministic continuation rather than a reconstruction exercise
- **Historical authority:** unchanged; this contract governs durable representation and mechanical authoring only

## 1. Core invariant

A Research checkpoint must not discard accepted information that a later stage needs.

For a current-policy lane, a Stage 3B checkpoint may be reported COMPLETE only when a fresh successor chat can author the complete six-file Research portfolio without:

- conversational memory;
- current-registry reconstruction of prior Research decisions;
- web research;
- reopening accepted Stage 1-3B conclusions;
- hand-renaming or hand-repackaging legacy schemas.

The owner experience should normally remain:

media guide / sources -> Proceed -> bounded Research stages -> Proceed -> Stage 4 -> owner NON_D1 sanity scan -> Proceed -> Research Frozen

Mechanical compatibility is not an owner decision.

## 2. Durable Stage 4 authoring capsule

Current-policy checkpoints carry package-authoring state under stage4-authoring/.

The package-ready members are:

1. stage4-authoring/opponents.csv
2. stage4-authoring/venues.csv
3. stage4-authoring/conferences.csv

These files are not a second historical truth layer. They are durable serialization of accepted Research conclusions needed by Stage 4.

Every checkpoint manifest that contains one of these members must hash/size-account for it.

### Opponents

Stage 2 owns stage4-authoring/opponents.csv.

It must preserve, for every accepted source-label mapping:

- source program;
- literal source opponent label;
- canonical opponent key;
- canonical opponent display name;
- current-D1 classification as established at the immutable Research base;
- game count / first season / last season;
- resolution status and method;
- owner choice when applicable;
- audit/provenance note.

Later stages carry this table forward byte-for-byte unless a specifically authorized opponent-identity correction changes it. A game-level opponent key alone is not sufficient durable Stage 2 output.

### Venues

Stage 3A/3B own stage4-authoring/venues.csv.

The table must be package-ready and must preserve the accepted physical venue identity, aliases, locality, research-base reuse/provisional identity provenance, and any accepted relationship chronology. Stage 3A-2/3A-4 should write regular-season venue state through; Stage 3B should add/update postseason venue state.

Do not infer missing facility chronology in Stage 4 from first/last game dates merely to fill this table.

### Conferences

Conference chronology used by the Research package must be durable no later than Stage 3B closeout as stage4-authoring/conferences.csv.

If ordinary source work established the chronology earlier, serialize it then and carry it forward. Do not wait until Stage 4 and reconstruct it from chat memory.

## 3. Carry-forward rule

Every successor Research checkpoint carries all existing stage4-authoring/ members forward.

A later stage may add or legitimately update the file it owns, but it must not silently drop an earlier package-authoring member.

tools/research_stage3a0.py mechanically carries any Stage 2 authoring capsule through its output and records those files in its manifest. Later Research substages must preserve the same invariant when serializing their checkpoints.

## 4. Stage 3B completion preflight

Before reporting a current-policy Stage 3B checkpoint COMPLETE, run:

    python tools/research_stage4.py preflight <school_key> <stage3b-checkpoint.zip>

PASS is required.

The preflight verifies:

- Stage 3B is complete;
- all three authoring tables are present and manifested;
- package-required columns are present;
- source-program ownership is coherent;
- every game has durable opponent presentation authority;
- literal source-label -> opponent-key mappings are represented;
- every curated venue name is represented by the durable venue table;
- the final game ledger can be projected mechanically into the current source-games.csv vocabulary.

If preflight returns STAGE4_AUTHORING_INPUT_INCOMPLETE or STAGE4_AUTHORING_INPUT_INVALID, remain in Stage 3B mechanical closeout. Repair only the durable representation/capsule defect. Do not reopen historical research unless the defect exposes an actual unresolved historical question.

## 5. Stage 4 command-first authoring

After owner continuation from Stage 3B, Stage 4 begins with:

    python tools/research_stage4.py author <school_key> <stage3b-checkpoint.zip> --main-sha <protected-main-sha>

The coordinator:

1. reruns Stage 4 authoring preflight;
2. projects the accepted final Stage 3B ledger to current source-games.csv;
3. copies the three durable authoring tables unchanged;
4. generates notes.md and source-notes.md mechanically from durable checkpoint state;
5. invokes the permanent Stage 4 closeout gate;
6. emits the package, QA, NON_D1 scan, and durable Stage 4 checkpoint.

Stage 4 must not independently rediscover opponent identity, physical venue meaning, conference chronology, or source provenance.

## 6. Legacy checkpoint compatibility

Accepted legacy checkpoints remain authoritative and immutable.

The permanent Stage 4 tools may normalize known legacy field vocabulary and checkpoint topology in memory. They must not rewrite the source checkpoint merely to satisfy the current representation.

A legacy Stage 3B checkpoint that predates this authoring-capsule contract may legitimately lack package-authoring state. That is a bounded compatibility-recovery problem, not permission to reconstruct prior opponent/conference decisions from present-day registry state or conversational memory.

When predecessor durable artifacts contain the missing accepted state, recover from those artifacts. If they do not, stop with the exact missing authority population.

## 7. Notes and source notes

notes.md and source-notes.md are Stage 4 presentation artifacts.

The permanent Stage 4 coordinator generates their mechanical baseline from:

- Stage 3B status/checkpoint hashes;
- final game/site/type censuses;
- row-level source metadata;
- durable source registers present in the checkpoint.

They are not a reason to keep essential Research conclusions only in prose/chat.

## 8. Owner boundary

This contract creates no new owner gate.

The Stage 4 terminal state remains:

STAGE 4: COMPLETE — OWNER NON_D1 SANITY SCAN READY

Stage 5 remains the required owner NON_D1 sanity scan. Stage 4 must not approve it on the owner's behalf or automatically begin Stage 5.
