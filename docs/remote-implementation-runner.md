# Guarded Remote Implementation Runner

- **Status:** Controlling execution-environment policy for serialized Implementation through stable Phase 0
- **Applies to:** RESEARCH_FROZEN intake, Implementation Stage 1 inventory, current-main reconciliation, Integration Freeze, and stable Phase 0
- **Does not apply to:** Stage 2, Owner Gate 1, sealed apply, Preview, Owner Gate 2, merge, or Production proof

## 1. Execution environments

Serialized Implementation may execute either:

1. in the project Codespace under the existing onboarding workflow; or
2. through the repository-owned guarded remote Implementation runner defined here.

Both environments use the same permanent basketball/reconciliation commands and the same historical authority. Remote execution is an orchestration and durability layer only. It does not weaken current-main requirements, owner gates, shared-reference policy, repository validation, release rules, or the one-active-Implementation invariant.

For the currently productionized remote lifecycle, the permanent commands remain:

```bash
python tools/implementation_stage1_inventory.py ...
python tools/stage_research_portfolio.py ... --apply --commit
```

The remote runner must not reimplement their basketball, venue, opponent, conference, scope, reconciliation, or validation logic.

## 2. Permanent entrypoints

Tracked repository capability:

- `tools/remote_implementation_control.py` — request/state validation, replay refusal, mutation classification, sidecar hashing, and Git-ref CAS primitives.
- `tools/remote_implementation_io.py` — hash-bound checkpoint transport, isolated worktrees, permanent-command invocation, and control-branch CAS helpers.
- `tools/remote_implementation_runner.py` — bounded request processor for Stage 1, Phase 0, and explicit recovery.
- `tools/remote_implementation_verify.py` — fresh-runner reconstruction of a completed Phase 0.
- `.github/workflows/remote-implementation.yml` — push-driven repository Action for the permanent control branch.
- `config/remote-implementation-control-state.initial.json` — canonical initial IDLE state for creating the operational control branch.

The operational machine authority lives on the dedicated branch:

```text
control/remote-implementation
```

Protected `main` remains the source of permanent code and basketball state. The control branch is durable orchestration/checkpoint state and must never become a substitute source of basketball truth.

## 3. Global control authority

The control branch contains:

```text
.remote-implementation/control-state.json
.remote-implementation/request.json
.remote-implementation/requests/<request_id>/...
.remote-implementation/checkpoints/<school>/<request_id>/...
.remote-implementation/phase0-inputs/<school>/<request_id>/...
.remote-implementation/writeahead/<school>/<request_id>/...
.remote-implementation/successors/<school>/<request_id>/...
.remote-implementation/recoveries/<school>/<request_id>/...
.remote-implementation/verifications/<school>/<request_id>/...
```

There is one global control state, not one lock per school.

The state records accepted, consumed, and abandoned request IDs; lifecycle and transaction state; the active school/request/operation; exact expected protected-main SHA; lock owner/run/attempt identity; exact lock commit; write-ahead identity; prepared commit/tree; target branch; and whether explicit recovery is required.

An IDLE state has no active request or lock. An ACTIVE mutation lock remains durable after runner failure until an explicit recovery request resolves it.

## 4. Bounded request contract

Every push-driven transition is an explicit JSON request bound to:

- schema version;
- unique request ID;
- school key;
- exact operation;
- exact predecessor control commit;
- SHA-256 of the exact predecessor control-state bytes;
- exact expected protected-main SHA;
- immutable Research Freeze SHA-256 and research-base SHA when applicable;
- immutable Git checkpoint transport identity;
- exact reconciliation payload paths/hashes when applicable;
- creation provenance and authorization boundary.

Supported operations are:

- `STAGE1_INVENTORY`
- `PHASE0`
- `RECOVER`

No request in this lifecycle may carry Owner Gate 1, Owner Gate 2, or release authority.

A generic owner `Proceed` may be converted into a request only when the next bounded operation is already unambiguous under repository policy. It is never an owner-gate approval or recovery authorization.

## 5. Research/checkpoint transport

The initial permanent transport is the proven immutable Git-part transport:

```text
kind = git_base64_parts
commit_sha = exact immutable commit
path_prefix = exact part prefix
part_count = exact expected count
sha256 = exact reconstructed Research Freeze SHA-256
```

The runner reconstructs the ZIP outside the tracked worktree, verifies the exact hash, requires exactly the six package members, and then passes that file to the existing permanent commands.

Reconciliation JSON payloads are exact request-commit files with SHA-256 bindings.

Large Research artifacts are not copied blindly into control state. The control branch preserves identities, hashes, exact small sidecars, and durable output checkpoints.

## 6. Stage 1 request

`STAGE1_INVENTORY` is read-only with respect to basketball repository branches.

The runner:

1. authenticates current protected `main`, predecessor control state, request identity, and replay status;
2. durably accepts the request;
3. reconstructs the exact Research Freeze and optional reconciliation specs;
4. creates an isolated runner-local `data/<school>-onboarding` worktree at exact current main;
5. invokes unchanged `tools/implementation_stage1_inventory.py`;
6. persists exact `.onboarding/<school>/stage1-reconciliation.json` plus request/reconciliation sidecars under a hash-bound Stage 1 checkpoint;
7. returns global control to IDLE.

A blocked Stage 1 inventory may be checkpointed honestly; it does not authorize Phase 0.

A failed accepted request is not replayable. Explicit recovery is required before normal progression resumes.

## 7. Phase 0 request and global lock

`PHASE0` requires a hash-bound PASS Stage 1 checkpoint from the same current protected main and Research Freeze.

The mutation sequence is:

```text
IDLE
→ request authenticated
→ global lock durable
→ fresh current-main Stage 1 PASS
→ isolated permanent Phase 0 preparation
→ exact Integration Freeze captured
→ write-ahead authority durable
→ create-once target ref CAS
→ durable successor checkpoint
→ lock release
→ IDLE
→ fresh-runner verification
```

The target is exactly:

```text
data/<school_key>-onboarding
```

Normal Phase 0 refuses a pre-existing target branch. It never silently overwrites or force-adopts an existing onboarding branch.

The permanent Phase 0 command owns the commit/tree. Remote orchestration does not incrementally edit the target branch through GitHub file APIs.

## 8. Write-ahead and objective mutation state

Before target publication, the control branch must durably preserve a write-ahead manifest containing at minimum:

- request identity/hash;
- global lock commit;
- exact protected-main SHA;
- Research Freeze/research-base identity;
- exact prepared commit/tree/parent;
- exact changed paths and changed-file hashes;
- exact allowed-path contract;
- exact `integration-freeze.json` bytes/hash;
- exact Stage 1 reconciliation bytes/hash;
- exact reconciliation sidecars/hashes when used;
- package-member hashes;
- semantic snapshot hash;
- venue/conference/program-alias mappings and scope metadata exposed by the Integration Freeze.

Recovery classifies durable state objectively as:

- `NOT_ATTEMPTED`
- `PREPARED_NOT_PUBLISHED`
- `PUBLISHED_NOT_FINALIZED`
- `COMPLETE`
- `DIVERGED_STOP`

An Action conclusion alone is never mutation authority.

## 9. Publication and fresh verification

Tracked mutation publication is one exact Git ref update using expected-head/create-once CAS.

A fresh runner then independently reconstructs from GitHub-visible durable state and verifies:

- protected-main binding;
- target branch exact SHA;
- prepared parent/tree;
- changed-path census and file hashes;
- exact write-ahead sidecars;
- exact Integration Freeze bindings;
- package-member hashes;
- source-game semantic snapshot;
- repository validation.

Only then may the durable verification record say:

```text
REMOTE PHASE 0 EQUIVALENCE: PASS
```

## 10. Recovery

There is no automatic retry of an accepted request.

A recovery request must bind the exact active request and exact lock commit. It inspects durable write-ahead authority and the actual target ref.

- `NOT_ATTEMPTED` or `PREPARED_NOT_PUBLISHED`: the failed request may be explicitly abandoned and the lock released.
- `PUBLISHED_NOT_FINALIZED`: the already-published commit may be adopted only when the exact commit/tree/ref/write-ahead authority matches.
- `DIVERGED_STOP`: fail closed. Do not reset, overwrite, or guess.
- stale recovery authority is refused.

Another school may not enter while the global control is not IDLE.

## 11. Permissions and protected main

The permanent workflow receives only repository `contents: write` permission because it must:

- commit durable control/checkpoint state to the control branch; and
- create the authorized onboarding branch ref.

It does not receive pull-request, deployment, environment, administration, or protected-main bypass authority.

Protected `main` is read as the exact integration base. The runner never pushes to `main`.

Stage 2, owner gates, sealed apply, Preview, merge, and Production proof remain outside the remote capability until separately productionized and tested.

## 12. Mobile / ChatGPT operation

The normal remote interaction is:

```text
owner in ChatGPT
→ bounded Proceed / explicit authorization
→ ChatGPT authenticates current durable state
→ ChatGPT writes one exact control request
→ push starts repository Action
→ permanent tool runs
→ durable checkpoint/successor appears
→ ChatGPT authenticates and reports it
```

Routine owner desktop, Codespaces, or GitHub UI interaction is not required for the supported lifecycle.

## 13. Experimental provenance

The accepted architecture experiments remain historical audit evidence on the existing `experiment/remote-implementation-proof*` branches.

Production code was extracted from the proven invariants; experimental `.remote-implementation-poc/` state is not merged into protected main.

The accepted Proof 6 end-to-end evidence includes the LIU disposable Phase 0 result and fresh-runner equivalence proof on the Proof 6 control branch. Those branches should be retained unless a separately authorized cleanup policy preserves equivalent audit provenance elsewhere.
