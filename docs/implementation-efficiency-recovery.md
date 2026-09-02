# Implementation Efficiency and Recovery Standard

- **Status:** Required operating standard after Texas A&M
- **Applies to:** every serialized school Implementation lane
- **Goal:** reduce owner relay work, terminal fragility, repeated phase work, and chat-context growth without weakening historical or release safeguards

Texas A&M proved that the sealed-plan architecture can still be operationally inefficient even when the final result is correct. The remaining friction was not caused by parallel-school chat reuse: the project already uses a fresh Research chat and a fresh Implementation chat per school. The main costs were repeated owner copy/paste, verbose diagnostics, Codespace/runtime failures, and large transcripts created by restating durable repository state.

This standard treats those as process defects to minimize rather than an unavoidable reason to relax quality.

## 1. Fresh chat is necessary but not sufficient

Continue using one fresh Implementation chat per school.

Do not expect that alone to prevent lag. A single school can still accumulate a large transcript if the lane repeatedly pastes raw CSVs, long logs, full test output, or state that already exists durably in the repository.

The implementation lane should keep the conversation focused on:

- phase boundaries;
- genuine historical decisions;
- compact failure summaries;
- exact owner approvals;
- final release proof.

Verbose evidence should live in files or ignored `.onboarding/` / `/tmp` artifacts whenever possible.

## 2. One owner relay per phase, not per command

The default interaction unit is a complete reversible phase.

A phase handoff should normally contain one runnable command block or one guarded operation, not a sequence of messages where the owner must execute and paste one command at a time.

When several deterministic commands are required, prefer a guarded child script or repository tool that:

1. performs the complete phase;
2. stops safely on the first real blocker;
3. writes verbose diagnostics to an artifact;
4. prints a compact terminal summary;
5. preserves enough state to resume without reconstructing the phase from chat history.

Owner attention is not a transport mechanism for routine technical state.

## 3. Compact-output contract

Implementation tools and agent-authored shell work should default to compact output.

The live terminal should normally show:

- phase name;
- branch / HEAD / expected base SHA;
- important input fingerprint or plan hash;
- pass/fail counts;
- exact failing decision IDs or paths;
- path to verbose diagnostics when applicable;
- the next safe phase boundary.

Do not print thousands of successful rows merely to prove that they were inspected.

When a command is inherently verbose, redirect full output to `/tmp/<school>-<phase>.log` or an ignored `.onboarding/<school>/` artifact and print only the concise tail/summary needed for diagnosis.

## 4. Durable state outranks chat state

After every successful major phase, the implementation lane should identify the durable checkpoint that proves completion.

Examples include:

- immutable Research ZIP SHA-256;
- `.onboarding/<school>/integration-freeze.json`;
- Phase 0 commit SHA;
- authoritative preflight review files;
- filled review plus exact decision-ID set;
- approved-plan hash;
- sealed apply commit;
- release PR number and exact PR-head SHA;
- merged-main SHA;
- exact Production deployment proof.

Do not restate or reconstruct a completed phase from memory if its durable artifact still exists.

## 5. Failure recovery rule

A Codespace, shell, browser, or chat failure does not automatically restart Implementation.

On recovery, inspect in this order:

1. current protected `origin/main`;
2. current branch and HEAD;
3. tracked worktree status;
4. current onboarding branch ancestry;
5. ignored `.onboarding/<school>/` state;
6. latest stable Phase 0 / apply / release commit;
7. existing PR and its exact head SHA;
8. previously sealed hashes/fingerprints.

Then resume from the earliest incomplete phase.

Do not rerun a successful phase merely because the prior chat turn ended unexpectedly, unless its fingerprint or repository prerequisites have changed.

Unexpected tracked state remains a STOP; recovery must not use blind reset, stash, force-push, or branch deletion.

## 6. Chat interruption recovery capsule

If the chat becomes laggy or unusable before the school is complete, the lane should be able to emit a compact recovery capsule rather than a giant narrative handoff.

Recommended fields:

```text
TEAM: <school>
IMPLEMENTATION STATE: <REBASE_REQUIRED|INTEGRATION_FROZEN|PHASE_0|GATE_1|SEALED|RELEASE_PREP|PREVIEW_APPROVED|MERGED>
origin/main: <sha>
branch: <branch>
HEAD: <sha>
research ZIP SHA-256: <sha>
integration freeze: <path/hash or none>
preflight/review state: <path/hash or none>
Gate 1 owner approval: <pending|approved; decision count>
approved plan SHA-256: <sha or none>
PR: <number or none>
PR head: <sha or none>
Preview approval: <pending|approved for exact sha>
Production proof: <pending|complete>
tracked worktree: <clean or exact unexpected paths>
NEXT SAFE ACTION: <one phase-sized action>
```

A replacement chat should verify this capsule against actual repository state before acting.

The capsule is an accelerator, not an authority that overrides Git/GitHub state.

## 7. Avoid copy/paste loops

Do not ask the owner to paste back data that the agent can reasonably inspect from:

- repository files;
- ignored onboarding artifacts already described by the current output;
- GitHub PR state;
- committed QA manifests;
- generated review files.

If the owner's Codespace is the only available execution environment, request the smallest output needed to diagnose the next action.

Prefer commands that print machine-readable or deliberately compact summaries.

## 8. Gate 1 remains one human decision packet

Operational efficiency must not fragment historical judgment.

Authoritative preflight still becomes one consolidated owner packet. The owner should not receive separate messages for deterministic identity consequences, routine normalization, and each individual discrepancy when they can be researched and presented together.

If technical repair after approval leaves the substantive decision universe unchanged, use supported carry-forward rather than asking for another full Gate 1 review.

## 9. Do not make chat lag a data-quality tradeoff

When transcript size becomes a problem, reduce transcript size rather than reduce validation.

Preferred response order:

1. write verbose evidence to durable artifacts;
2. print smaller summaries;
3. batch commands by phase;
4. resume from checkpoints rather than replaying phases;
5. if necessary, move to a fresh Implementation chat using the recovery capsule.

Never skip research acceptance, current-main rebase, owner decisions, pre-seal rehearsal, transactional apply, exact Preview approval, or Production proof merely to make a chat shorter.

## 10. Tooling direction

Generic tooling should continue moving toward:

- resumable phase-sized commands;
- an implementation status command/capsule generated from repository state;
- concise diagnostics with verbose log artifacts;
- idempotent no-op behavior after successful phases;
- automatic detection of the earliest incomplete safe phase;
- fewer owner-mediated command/result round trips.

Until those capabilities are fully automated, agents should follow the same operating model manually using existing durable state.

## 11. Success criterion

A normal school should require owner interaction only for:

- startup inputs when not already supplied;
- one consolidated Gate 1 historical decision packet;
- exact Preview visual approval;
- genuinely unexpected owner-level historical questions.

Technical failures may require an owner relay when the Codespace is the only execution surface, but each failure should produce a compact diagnosis and resume point rather than a new command-by-command conversation.

The objective remains:

> **MORE THROUGHPUT, LESS RELAY WORK, SAME HISTORICAL AND RELEASE QUALITY.**
