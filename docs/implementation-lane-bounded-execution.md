# Implementation Lane Bounded Execution Protocol

- **Status:** Controlling Implementation-lane turn-execution protocol
- **Applies to:** serialized school Implementation lanes and their recovery
- **Does not replace:** sealed-plan onboarding policy, Gate 1 historical review, Codespace terminal safety, release tooling, current-main rebase rules, exact Preview approval, or Production proof

## 1. Purpose

This protocol changes **how Implementation work is divided into chat turns**, not the historical or release standards themselves.

The governing rule is:

> **One bounded implementation phase per turn. A completed phase boundary is an intentional execution handoff. Do not automatically begin the next phase.**

The owner should not be used as a command-by-command transport layer. Deterministic work should be batched into phase-sized operations with compact output and durable checkpoints.

## 2. Authority and startup

At Implementation-lane startup:

1. inspect actual protected `main` and record the current SHA;
2. read current `AGENTS.md` plus the implementation documents it references, especially:
   - `docs/school-onboarding-fast-path.md`
   - `docs/onboarding-process-hardening.md`
   - `docs/implementation-efficiency-recovery.md`
   - `docs/codespace-terminal-safety.md`
   - `docs/parallel-portfolio-pipeline.md`
3. authenticate the incoming immutable `RESEARCH_FROZEN` artifact. A precomputed ZIP SHA-256 and final status card are preferred, but if the owner explicitly designates exactly one attached ZIP as the final accepted Research Freeze and omits those copied fields, use the owner-designated-artifact fallback below rather than stopping solely for missing transport metadata;
4. reconstruct actual repository/onboarding state before acting if this is a recovery;
5. begin Implementation Stage 1 only.

Repository policy controls over copied handoff wording.

### 2.1 Owner-designated Research Freeze attachment fallback

The expected normal handoff remains: exact final ZIP, precomputed SHA-256, and compact
Research Freeze status card. That is the easiest way to detect an accidental stale or
superseded upload.

However, the checksum is an integrity identity, not a substitute for the owner's selection
of which artifact is authoritative. When the owner explicitly identifies **exactly one**
attached ZIP as the final accepted `RESEARCH_FROZEN` artifact but does not separately copy
the prior checksum/status card, the Implementation lane must not classify that omission
alone as `STOP — RECOVERY REQUIRED`.

Instead, in the same bounded Stage 1 intake unit:

1. compute the exact SHA-256 and file size of the owner-designated attachment;
2. require the exact flat six-file package contract;
3. recover/verify the package's `research_base_sha` and school identity;
4. run the permanent Research acceptance gate against those exact bytes;
5. inspect the package/durable Research evidence for the required final acceptance facts,
   including the owner NON_D1 scan and pre-freeze self-challenge when applicable;
6. check available durable authority for evidence that another package superseded or
   conflicts with the selected artifact; and
7. if all checks are clean and exactly one candidate exists, record the computed digest as
   the immutable Research Freeze transport identity used by the Stage 1 request and every
   downstream checkpoint.

This is **owner-designated byte authentication**, not self-authentication by an arbitrary
new ZIP. A competing/superseding candidate, mismatched school/research base, failed Research
acceptance, materially missing final-freeze evidence, or ambiguity about which attachment the
owner intended remains a STOP.

A history-scope contradiction discovered at intake is separate. Because guarded
`STAGE1_INVENTORY` is read-only and its request schema does not require Phase 0 history-scope
metadata, a scope discrepancy should be recorded and included in the complete Stage 1
reconciliation inventory. It must be resolved under current scope/shared-reference policy
**before Integration Freeze or Phase 0 mutation**, but it does not by itself justify skipping
or blocking the read-only inventory.

## 3. Common execution rules

### 3.1 Durable repository state outranks chat memory

After interruption, reconstruct from Git/GitHub, tracked files, ignored `.onboarding/<school>/` state, sealed hashes, PR state, and release state. Do not replay successful phases merely because a prior turn ended unexpectedly.

### 3.2 Owner relay should be phase-sized and thin

When the owner's Codespace is the only execution surface, invoke the supported permanent repository command directly by default. Assistant-authored multi-line shell/Python orchestration is not a normal Implementation interface. Use a narrow temporary helper only for genuinely bespoke work that current tooling does not own; if the same operation can recur, treat that as a permanent-tooling gap and repair the repository instead of normalizing the helper.

"Phase-sized" does not mean monolithic. The normal relay should contain one principal repository operation plus its immediate validation. Do not wrap a permanent command in a large bespoke program merely to restate its branch, lifecycle, validation, or release invariants, and do not combine mutation, regenerated preflight, rehearsal, release preparation, and unrelated confidence checks into one giant wrapper merely to reduce the number of pastes.

Browser Codespaces transport convention: the owner may drag the immutable `RESEARCH_FROZEN` ZIP into the repository root in the Explorer. Do **not** ask the owner to manually copy or move that ZIP to `/tmp`. The permanent `python tools/implementation_stage1_inventory.py ...` command accepts that repository-root path, verifies the expected SHA-256 first, and then relocates an untracked root ZIP to `/tmp/cbh-implementation-inputs/` before any branch/cleanliness-sensitive Stage 1 guard runs. A tracked ZIP is never relocated. Inputs already outside the repository root are left unchanged.

Follow `docs/codespace-terminal-safety.md` exactly. In particular:

- never use `set -u`, `set -euo pipefail`, or `set -eo pipefail` directly in the owner's interactive shell;
- never use `exit` from pasted interactive-shell instructions;
- put fail-fast guarded logic in a child script under `/tmp`;
- never use `git add -A`;
- let permanent repository tooling own invariants it already validates instead of reimplementing them in shell;
- changed-path inventories must include untracked files when they claim to represent the complete worktree;
- derive numerical postconditions from durable state when practical rather than manually remembering totals;
- keep verbose logs local and return compact PASS/STOP output;
- inspect and classify state before rerunning a failed phase.

For recurring Implementation operations already owned by permanent repository tooling, invoke that tooling directly by default. Do not replace an existing supported operation with bespoke shell or `/tmp` Python merely because the same result can be scripted. In particular, Stage 2 uses `python tools/implementation_stage2.py <school>` for authoritative preflight/recovery state and reruns that command with `--map <recommendation-map.json>` for permanent map validation plus proposal rehearsal. Use supported review-fill, onboarding, site-gate, package-check, and release commands for the later responsibilities they own. Temporary helpers are appropriate for genuinely school-specific diagnostics or operations not represented by current tooling, and should remain narrow rather than reimplementing permanent invariants.

Before sending an owner-executed bespoke wrapper, establish from current repository state the exact precondition, intended mutation or read-only effect, allowed changed paths/derived changes, and success condition. If the relay wraps a permanent repository command, inspect and trust that command's actual contract rather than adding an undocumented invariant that the owner must disprove by execution.

The preferred execution order is:

`permanent repository command -> pasted standard command/guard -> pasted temporary helper -> manual helper-file transport`

Manual helper-file transport remains exceptional under `docs/codespace-terminal-safety.md`.

If an owner-run relay fails, first classify the stop as `REPOSITORY/DATA FAILURE`, `HISTORICAL REVIEW`, or `ASSISTANT WRAPPER DEFECT`. A wrapper defect should be repaired without making the owner re-investigate healthy basketball data.

### 3.3 Preserve settled owner decisions

A purely technical failure, rerun, or fingerprint regeneration does not reopen historical decisions when the substantive decision universe is unchanged. Use supported carry-forward behavior where permitted.

### 3.4 Honest incomplete checkpoint is valid

If a phase cannot safely finish in one turn, preserve the exact durable state and stop. Do not begin the next phase merely to maintain momentum.

### 3.5 `Proceed` is execution authorization, not a historical/release gate

After an ordinary completed implementation stage, owner responses such as `Proceed`, `Continue`, or equivalent authorize only the identified next bounded stage.

They do **not** substitute for:

- Owner Gate 1 historical decisions;
- exact Vercel Preview approval;
- any other explicit owner judgment required by repository policy.

## 4. Required turn-ending contract

**Every bounded Implementation response MUST end with exactly one `NEXT OWNER ACTION` classification**, on its own final line. Give the next bounded operation (or the precise necessary decision) immediately before that line. This requirement applies to both ordinary continuation and checkpoint/recovery turns; a stage status such as `BLOCKED` does not, by itself, identify the next owner action.

- `NEXT OWNER ACTION: PROCEED` — The next single bounded operation is routine, unambiguous, and already authorized under repository policy. Identify that operation and explicitly say **no Control Center consultation is required**. This includes policy-supported deterministic technical repairs after a read-only `BLOCKED` census; it never authorizes a new stage automatically.
- `NEXT OWNER ACTION: EXPLICIT OWNER APPROVAL REQUIRED` — A genuine historical-authority decision, the exact Owner Gate 1 packet, or the exact PR-head Preview at Owner Gate 2 needs affirmative owner approval. State precisely what must be approved; generic `Proceed` is insufficient.
- `NEXT OWNER ACTION: CONTROL CENTER AUTHORIZATION REQUIRED` — An exceptional shared/global mutation, unresolved policy or permission-governance choice, competing Implementation lock, or other explicitly controlled authority boundary requires Control Center disposition. State its exact scope rather than silently broadening a routine `Proceed`.
- `NEXT OWNER ACTION: STOP — RECOVERY REQUIRED` — Durable transaction/control state is unsafe or a genuinely failed/ambiguous operation requires evidence-first recovery. Identify the failing authority and required recovery path. Do **not** use this label merely because a healthy, checkpointed census says `BLOCKED`, because an ordinary bounded stage is incomplete, or because a known next deterministic repair is available.
- `NEXT OWNER ACTION: NONE — IMPLEMENTATION COMPLETE` — The school has passed the exact approved merge, successful same-SHA Vercel Production deployment, all required public Production JSON equivalence checks, and **independent fresh Production-proof verification**, with healthy final control state. The school has no further Implementation stage; do not misleadingly conclude `PROCEED` just because that was the previous standard's last routine option.

Use **exactly these five labels**. Keep the final classification short and unmistakable; do not replace it with an ambiguous `Next action` sentence. When the appropriate label is `PROCEED`, let the owner answer simply `Proceed` at the next turn; do not demand a special handoff, ceremonial Control Center confirmation, or an extra technical owner gate. The classification changes **communication only**; all one-bounded-unit execution limits, repository mutation protections, Owner Gate 1/2 approvals, and Production-proof requirements remain unchanged.


### Completed ordinary stage

```text
IMPLEMENTATION STAGE X: COMPLETE

<concise substantive/technical results and durable checkpoint>

Owner decision required: NO
Next bounded stage: Implementation Stage X+1 — <name>
STOPPING AT THE REQUIRED IMPLEMENTATION STAGE BOUNDARY.
```

### Incomplete but healthy stage

```text
IMPLEMENTATION STAGE X: INCOMPLETE — DURABLE CHECKPOINT PRESERVED

Completed: <exact completed work>
Remaining: <exact residual work>
Owner decision required: NO
Next bounded assignment: resume Implementation Stage X from this exact checkpoint
STOPPING AT THE REQUIRED IMPLEMENTATION STAGE BOUNDARY.
```

### Owner gate boundary

When a genuine owner gate is reached, say so explicitly and do not imply that a generic `Proceed` is sufficient.

## 5. Implementation Stage 1 — Intake, current-main rebase, and Integration Freeze

### Objective

Accept the incoming `RESEARCH_FROZEN` portfolio against **current protected main** and establish an integration-ready package without reopening settled research unnecessarily.

### Work

- authenticate the immutable research artifact under the preferred precomputed-hash path or the owner-designated attachment fallback above, then verify the exact-six-file contract;
- inspect current protected `main`, branch/worktree state, and research baseline;
- rerun the research acceptance check under current tooling;
- **before any Stage 1 mutation**, run `python tools/implementation_stage1_inventory.py <school> <research.zip> ...` and preserve `.onboarding/<school>/stage1-reconciliation.json`;
- require the read-only inventory to scan the complete frozen venue/program reconciliation population rather than stopping discovery at the first mutation blocker;
- classify the population into mechanically safe reuse/new identity, shared/global maintenance, and genuine ambiguous STOP cases before deciding how to mutate;
- if existing published/global state must be changed through a dedicated maintenance PR, present one consolidated declared maintenance scope and obtain explicit Control Center authorization before that protected-main maintenance batch; ordinary `Proceed` for Stage 1 does not by itself authorize a hidden sequence of dedicated maintenance PRs;
- batch same-family generic Stage 1 tooling defects into one coherent repair wherever the complete inventory shows they are members of the same representation problem; do not use rerun/regeneration as the discovery mechanism;
- after any authorized maintenance/tooling batch lands, refresh protected main once and rerun the complete read-only inventory; establish Integration Freeze only after the inventory is clean;
- recheck every provisional/shared physical venue identity against current main;
- recheck opponent/program aliases and shared reference identities that may have changed since `research_base_sha`;
- reuse identities added by intervening schools when they represent the same real entity;
- allocate current numeric venue IDs only after physical-identity reconciliation;
- resolve stale key/name/reference collisions mechanically where unambiguous;
- preserve completed NON_D1 owner approval unless current-main rebase materially changes an affected identity;
- if the portfolio predates the NON_D1 owner-scan policy, perform that required checkpoint before Integration Freeze;
- rerun package QA/hashes after rebase;
- if configured history scope excludes researched rows, state the publication consequence in plain English: the public start season, how many researched rows/seasons remain outside the page, and the preserved season range; do not treat a prior scope reference as proof that the owner understood this product consequence;
- create the durable integration-freeze checkpoint required by current tooling.

### Completion standard

- latest read-only Stage 1 reconciliation inventory status = `PASS`;
- current-main rebase complete;
- ambiguous shared/global identities = 0;
- current package QA clean;
- `INTEGRATION_FROZEN` established;
- no tracked Phase 0 work begun unless the current generic staging tool makes stable Phase 0 inseparable from the integration-freeze operation.

If current tooling creates the stable Phase 0 checkpoint as part of the same guarded operation, report that explicitly; do not redo it in Stage 2.

## 6. Implementation Stage 2 — Stable Phase 0, preflight, and Gate 1 readiness

### Objective

Install the integration-frozen portfolio on the serialized onboarding branch, run canonical preflight, investigate all genuine owner-relevant decisions, and stop with one consolidated Gate 1 packet.

### Work

The repository-owned guarded remote runner may execute only the initial read-only Stage 2 census through `CAPABILITY_CENSUS_READY` or an honest permanent-tool `BLOCKED` checkpoint. Any tracked deterministic repair, recommendation-map work, proposal rehearsal, or Gate 1 readiness remains outside the remote capability and requires the separately authorized Stage 2 execution path.

- establish/verify `data/<school_key>-onboarding` from the correct base;
- install the six-file package and required current-main reference additions;
- create/verify the stable Phase 0 checkpoint;
- run the repository-owned Stage-2 coordinator (`python tools/implementation_stage2.py <school>`) to verify semantic freeze, regenerate authoritative preflight, and write both the durable `.onboarding/<school>/implementation-stage2-status.json` recovery artifact and `.onboarding/<school>/implementation-stage2-capability-census.json`;
- treat `CAPABILITY_CENSUS_READY`, not a blocker-free raw preflight, as the first healthy Stage-2 discovery boundary; the census must inventory the presently detectable decision/site/H-A-N representation topology before the first fingerprint-changing Stage-2 repair;
- before any fingerprint-changing Stage 2 repair, run the comprehensive deterministic candidate sweep defined by `docs/implementation-pre-gate-adversarial-challenge.md` and classify the presently detectable normalization, current-source, reciprocal, display, site-metadata, predicted-publication, and historical-conflict population together;
- correct the classified deterministic population in one coherent repair batch wherever safe; split it only when a later repair genuinely depends on changed state from an earlier repair, and name that dependency rather than using regeneration itself as a discovery strategy;
- regenerate authoritative preflight after the coherent repair batch, not merely because one individual item became clear;
- research every genuine owner-relevant decision row **to recommendation, not necessarily to resolution**: eliminate mechanical explanations, assemble the material competing evidence, and make a supported recommendation; do not delay Gate 1 merely to eliminate reasonable historical uncertainty;
- treat Gate 1 as the **Owner Reconciliation Packet**: for each material historical conflict, summarize the competing interpretations, recommendation and basis, and meaningful residual uncertainty so the owner can approve, choose another supported disposition, or return that specific item for additional bounded research;
- construct the exact proposed recommendation map that will underlie Gate 1 and rerun the Stage-2 coordinator with `--map <recommendation-map.json>`; the coordinator must validate the map with the authoritative review parser and run the full disposable pre-Gate rehearsal required by `docs/implementation-pre-gate-adversarial-challenge.md`;
- repair deterministic/mechanical failures exposed by the rehearsal before owner review; when the site gate runs, use the preserved `.onboarding/<school>/last-rehearsal-site-gate.json` diagnostic rather than rebuilding a school-specific classifier; when the rehearsal exposes a genuine historical conflict, investigate it only far enough to produce a responsible recommendation and include it in Gate 1 rather than turning Stage 2 into open-ended archaeology;
- consolidate recommendations, evidence bases, accomplishments, and publication decisions into one readable Gate 1 packet;
- run the pre-Gate releaseability challenge required by current policy, including implementation site completeness, stale venue fallback checks, physical venue propagation, target no-op prediction, accomplishment/publication readiness, and deterministic fingerprint-changing corrections that can be made before owner review;
- if Stage 2 exposes a generic permanent-tool defect, checkpoint as a technical tooling repair, classify the **complete currently detected defect population** in the durable capability census, and define one consolidated repair scope before merging the first repair; batch same-family capability defects into one protected-main tooling PR wherever technically coherent, add regression coverage for every exposed topology, then rerun the repository-owned Stage-2 coordinator. Do not use repeated repair/merge/rerun cycles as the discovery mechanism, substitute a bespoke wrapper, or mix the tooling repair into a new unbounded historical-research pass.

### Completion standard

A blocker-free raw preflight is not a completion state. `CAPABILITY_CENSUS_READY` means only that the durable population-level discovery record exists and the lane may mature the recommendation map.

Stop at:

```text
OWNER GATE 1 READY
```

only after the exact recommendation map passes the full disposable proposal rehearsal and the capability census records `PASS`. The owner receives one consolidated **Owner Reconciliation Packet**. Every material historical conflict should normally carry an agent recommendation even when uncertainty remains. A recommendation is not permission to decide silently for the owner. Do not encode, seal, or apply owner decisions before the owner actually supplies them.

## 7. Owner Gate 1 — historical decision packet

This is a **real owner gate**, not an ordinary stage transition.

The owner reviews the consolidated batch and supplies the required dispositions/evidence approval under current repository policy.

A generic `Proceed` is not enough unless the owner has already clearly approved the exact recommendations/decisions being referenced.

The owner may approve a recommendation, choose another supported disposition, or return a specific item for additional bounded research. If the owner changes or flags any recommendation, research only the affected issue unless the new evidence exposes a broader contradiction.

## 8. Implementation Stage 3 — Encode, rehearse, seal, apply, and post-apply validation

### Objective

Turn the owner-approved Gate 1 batch into a technically validated applied release candidate while preserving unchanged owner judgments through purely technical reruns.

### Work

- encode the approved review using current generic tooling;
- execute the approved-decision mechanical sequence as one guarded Stage 3 operation where current permanent tooling safely permits it: fill/encode -> disposable rehearsal -> seal only on PASS -> transactional apply -> post-apply validation;
- run disposable pre-seal rehearsal;
- diagnose and repair purely technical failures generically where possible;
- if tracked inputs change but substantive owner decisions remain identical, regenerate preflight and use supported carry-forward rather than re-asking the owner;
- return to the owner only for genuinely new/changed historical decisions;
- seal the exact approved plan/hash;
- execute the transactional apply with the exact sealed hash;
- verify target no-op, implementation site completeness, accomplishment cross-check, deterministic site build, tests, whitespace, changed-path allow-list, and target assertion closure;
- preserve the exact durable applied-release state.

### Completion standard

- transactional apply complete;
- post-apply technical validation complete;
- no unresolved new owner decisions;
- exact release candidate/fingerprint established;
- release preparation not yet performed.

## 9. Implementation Stage 4 — Release preparation and exact Preview

### Objective

Create the exact release/PR state and obtain the exact Vercel Preview that the owner must inspect.

### Work

Run the current release-preparation workflow, which owns the release commit, push, PR preparation, checks, mergeability verification, and exact Preview deployment.

Do not manually commit between final apply and release preparation when current tooling binds the release manifest to HEAD.

### Completion standard

Stop at:

```text
OWNER GATE 2 — EXACT PREVIEW APPROVAL REQUIRED
```

Report at minimum:

- PR number/URL;
- exact PR-head SHA;
- exact Preview URL;
- visual-QA artifact/checklist status.

Do not merge. A generic `Proceed` is not Preview approval.

## 10. Owner Gate 2 — exact Preview visual approval

The owner must personally inspect the exact Preview associated with the exact PR-head SHA and explicitly approve it.

Any PR-head change invalidates prior Preview approval.

## 11. Implementation Stage 5 — Merge, Production proof, and completion

### Objective

Merge only the exact owner-approved release state and prove that the exact merged SHA reached Production correctly.

### Work

- verify the approved Preview still matches the current exact PR head;
- run the current merge command with explicit preview-approved semantics;
- verify protected `main` contains the exact merge result;
- wait for the exact merged-main SHA's successful Production deployment;
- compare production JSON/equivalent published artifacts against merged main for the target and every required affected document;
- verify final release lock/status and clean repository state.

### Completion standard

Only after all release proofs pass may the lane declare:

```text
IMPLEMENTATION COMPLETE: YES
LIVE/PRODUCTION VERIFIED: YES
```

## 12. Recovery semantics

If a chat, Codespace, browser, or tool session fails:

1. inspect actual protected main;
2. inspect current branch/HEAD/worktree;
3. inspect `.onboarding/<school>/` durable state;
4. inspect existing PR/release state;
5. compare fingerprints/hashes to the last completed stage;
6. resume from the earliest incomplete bounded stage.

Do not restart the school, blindly reset/stash, force-push, delete branches, or rerun completed phases whose fingerprints remain valid.

## 13. Copy/paste minimization target

The protocol does not create terminal access that the chat does not possess. When the owner's Codespace remains the only execution surface, some owner relay may still be required.

The required operating target is:

> **Few thin phase-sized owner relays, not many command-sized relays and not giant multi-operation scripts.**

A normal school should ideally require owner attention only for:

- one or a small number of thin phase-sized Codespace executions when necessary;
- Owner Gate 1;
- exact Preview approval;
- genuinely unexpected historical/repository blockers.

A false stop caused only by assistant-authored wrapper arithmetic, incomplete changed-path inventory, formatting, or duplicated verification logic does not count as an acceptable normal blocker. Treat repeated wrapper defects as process bugs to eliminate, not as the expected cost of safe onboarding.

## 14. Relationship to existing policy

This document is controlling for **Implementation chat turn boundaries and continuation semantics**.

Existing repository documents remain controlling for the substantive mechanics and quality rules within each stage. If an older document says to continue autonomously through several implementation phases, this protocol requires a stop at the bounded stage boundary without weakening the underlying work.
