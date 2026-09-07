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
3. verify the incoming immutable `RESEARCH_FROZEN` ZIP/hash and status card;
4. reconstruct actual repository/onboarding state before acting if this is a recovery;
5. begin Implementation Stage 1 only.

Repository policy controls over copied handoff wording.

## 3. Common execution rules

### 3.1 Durable repository state outranks chat memory

After interruption, reconstruct from Git/GitHub, tracked files, ignored `.onboarding/<school>/` state, sealed hashes, PR state, and release state. Do not replay successful phases merely because a prior turn ended unexpectedly.

### 3.2 Owner relay should be phase-sized

When the owner's Codespace is the only execution surface, prefer one guarded phase-sized child script or compact command block per bounded phase rather than repeated one-command-at-a-time handoffs.

Follow `docs/codespace-terminal-safety.md` exactly:

- never use `set -u`, `set -euo pipefail`, or `set -eo pipefail` directly in the owner's interactive shell;
- never use `exit` from pasted interactive-shell instructions;
- put fail-fast guarded logic in a child script under `/tmp`;
- never use `git add -A`;
- inspect state before rerunning a failed phase.

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

- verify the immutable research ZIP/hash and exactly-six-file contract;
- inspect current protected `main`, branch/worktree state, and research baseline;
- rerun the research acceptance check under current tooling;
- recheck every provisional/shared physical venue identity against current main;
- recheck opponent/program aliases and shared reference identities that may have changed since `research_base_sha`;
- reuse identities added by intervening schools when they represent the same real entity;
- allocate current numeric venue IDs only after physical-identity reconciliation;
- resolve stale key/name/reference collisions mechanically where unambiguous;
- preserve completed NON_D1 owner approval unless current-main rebase materially changes an affected identity;
- if the portfolio predates the NON_D1 owner-scan policy, perform that required checkpoint before Integration Freeze;
- rerun package QA/hashes after rebase;
- create the durable integration-freeze checkpoint required by current tooling.

### Completion standard

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

- establish/verify `data/<school_key>-onboarding` from the correct base;
- install the six-file package and required current-main reference additions;
- create/verify the stable Phase 0 checkpoint;
- run generic onboarding preflight;
- correct demonstrable mechanical/package-normalization defects before owner review;
- regenerate preflight after such narrow fixes;
- research every genuine owner-relevant decision row;
- consolidate recommendations, evidence bases, accomplishments, and publication decisions into one readable Gate 1 packet;
- run the pre-Gate releaseability challenge required by current policy, including implementation site completeness, stale venue fallback checks, physical venue propagation, target no-op prediction, accomplishment/publication readiness, and deterministic fingerprint-changing corrections that can be made before owner review.

### Completion standard

Stop at:

```text
OWNER GATE 1 READY
```

The owner receives one consolidated historical decision packet. Do not encode, seal, or apply owner decisions before the owner actually supplies them.

## 7. Owner Gate 1 — historical decision packet

This is a **real owner gate**, not an ordinary stage transition.

The owner reviews the consolidated batch and supplies the required dispositions/evidence approval under current repository policy.

A generic `Proceed` is not enough unless the owner has already clearly approved the exact recommendations/decisions being referenced.

If the owner changes or flags any recommendation, research only the affected issue unless the new evidence exposes a broader contradiction.

## 8. Implementation Stage 3 — Encode, rehearse, seal, apply, and post-apply validation

### Objective

Turn the owner-approved Gate 1 batch into a technically validated applied release candidate while preserving unchanged owner judgments through purely technical reruns.

### Work

- encode the approved review using current generic tooling;
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

> **Few phase-sized owner relays, not many command-sized relays.**

A normal school should ideally require owner attention only for:

- one or a small number of phase-sized Codespace executions when necessary;
- Owner Gate 1;
- exact Preview approval;
- genuinely unexpected historical/repository blockers.

## 14. Relationship to existing policy

This document is controlling for **Implementation chat turn boundaries and continuation semantics**.

Existing repository documents remain controlling for the substantive mechanics and quality rules within each stage. If an older document says to continue autonomously through several implementation phases, this protocol requires a stop at the bounded stage boundary without weakening the underlying work.
