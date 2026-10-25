# Guarded Remote Implementation Runner

- **Status:** Controlling execution-environment policy for serialized remote Implementation, including the authenticated release and Production-proof lifecycle
- **Applies to:** RESEARCH_FROZEN intake, Implementation Stage 1 inventory, current-main reconciliation, Integration Freeze, stable Phase 0, the read-only Stage 2 capability census through `CAPABILITY_CENSUS_READY` or an honest permanent-tool `BLOCKED` checkpoint, the single census-bound representation-only `STAGE2_OPPONENT_DISPLAY_NORMALIZE` repair, exact-map read-only `STAGE2_PROPOSAL_REHEARSAL` through permanent-tool `OWNER_GATE_1_READY` or an honest durable `BLOCKED` checkpoint, the read-only exact-owner-approval `STAGE2_GATE1_FILL` boundary, the read-only filled-review `STAGE2_PRESEAL_REHEARSAL` boundary, the read-only cryptographic `STAGE2_GATE1_SEAL` boundary, the transactional `STAGE2_SEALED_APPLY` boundary, and the read-only reconciliation diagnostic
- **Does not apply to:** arbitrary unapproved Stage 2 tracked repairs or uncontrolled release/merge bypasses; the remote runner does not itself create or merge PRs or push protected main

## 1. Execution environments

Serialized Implementation may execute either:

1. in the project Codespace under the existing onboarding workflow; or
2. through the repository-owned guarded remote Implementation runner defined here.

Both environments use the same permanent basketball/reconciliation commands and the same historical authority. Remote execution is an orchestration and durability layer only. It does not weaken current-main requirements, owner gates, shared-reference policy, repository validation, release rules, or the one-active-Implementation invariant.

For the currently productionized remote lifecycle, the permanent commands remain:

```bash
python tools/implementation_stage1_inventory.py ...
python tools/stage_research_portfolio.py ... --apply --commit
python tools/implementation_stage2.py <school>
python tools/implementation_stage2.py <school> --map <recommendation-map.json>
python tools/onboarding_hardening.py fill-review <school> --map <recommendation-map.json>
python tools/onboarding_hardening.py rehearse-review <school>
python tools/onboard_school.py <school> --approve --approved-by project-owner
python tools/onboard_school.py <school> --apply --approved-plan <exact-sealed-hash>
python tools/normalize_historical_opponent_displays.py <school> --sync-source-games [--apply]
```

The remote runner must not reimplement their basketball, venue, opponent, conference, scope, reconciliation, or validation logic.

## 2. Permanent entrypoints

Tracked repository capability:

- `tools/remote_implementation_control.py` — request/state validation, replay refusal, mutation classification, sidecar hashing, and Git-ref CAS primitives.
- `tools/remote_implementation_io.py` — hash-bound checkpoint transport, isolated worktrees, permanent-command invocation, and control-branch CAS helpers.
- `tools/remote_implementation_runner.py` — bounded request processor for Stage 1, Phase 0, read-only Stage 2 census, exact-map proposal rehearsal, exact-owner-approval Gate 1 fill, read-only pre-seal rehearsal, read-only cryptographic Gate 1 sealing, transactional sealed apply, the opponent-display normalization mutation, reconciliation diagnostics, and explicit recovery.
- `tools/remote_implementation_stage2_census.py` — exact Phase 0 authority restoration, read-only Stage 2 coordinator invocation, artifact hashing, and tracked-mutation proof shared by the runner and verifier.
- `tools/remote_implementation_stage2_opponent_display.py` — exact census/Freeze authentication, permanent normalizer dry-run/apply orchestration, representation-only field proof, and post-repair Stage 2 regeneration.
- `tools/remote_implementation_stage2_proposal.py` — exact blocker-free Stage 2 authority authentication, immutable recommendation-map transport binding, runtime/target-worktree separation, permanent `--map` invocation, proposal artifact hashing, and tracked-mutation proof.
- `tools/remote_implementation_stage2_gate1_fill.py` — exact `OWNER_GATE_1_READY` proposal plus fresh-verification authentication, exact owner-approval binding, permanent `fill-review` invocation, filled-review hashing, and tracked-mutation proof.
- `tools/remote_implementation_stage2_preseal.py` — exact fresh-verified Gate 1 fill authentication, permanent `rehearse-review` invocation, normalized technical-readiness proof, site-gate capture, and tracked-mutation proof.
- `tools/remote_implementation_stage2_seal.py` — exact fresh-verified `READY_TO_SEAL` authentication, permanent `onboard_school.py --approve` invocation, exact approved-plan/review checkpointing, and independent seal reconstruction without apply.
- `tools/remote_implementation_stage2_apply.py` — exact fresh-verified seal authentication, current-main technical-readiness replay, permanent transactional `onboard_school.py --apply` invocation, exact successor preparation, release-manifest proof, and deterministic prepared-tree verification.
- `tools/remote_implementation_stage2_diagnostic.py` — exact blocked-proposal checkpoint authentication, one-canonical-game diagnostic input restoration, permanent reconciliation-trace invocation, trace hashing, and tracked-mutation proof.
- `tools/remote_implementation_release_readiness.py` — hash-bound sealed-apply release-gate proof.
- `tools/remote_implementation_release_preview.py` — exact existing school PR, successful CI/mergeability and PR-head Preview verification.
- `tools/remote_implementation_production.py` — exact independently verified Owner Gate 2 approval and read-only Production proof.
- `tools/remote_implementation_verify.py` — independent fresh-runner reconstruction of all guarded stages, exact Gate 2 approval, and post-merge Production equality.
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
- `STAGE2_CENSUS`
- `STAGE2_OPPONENT_DISPLAY_NORMALIZE`
- `STAGE2_PROPOSAL_REHEARSAL`
- `STAGE2_GATE1_FILL`
- `STAGE2_PRESEAL_REHEARSAL`
- `STAGE2_GATE1_SEAL`
- `STAGE2_SEALED_APPLY`
- `STAGE2_RECONCILIATION_DIAGNOSTIC`
- `RELEASE_READINESS`
- `RELEASE_PREVIEW_VERIFY`
- `RELEASE_GATE2_APPROVAL`
- `RELEASE_PRODUCTION_PROOF`
- `RECOVER`

Only `STAGE2_GATE1_FILL` may carry Owner Gate 1 authority, bound to its exact fresh-verified proposal checkpoint, decision universe, recommendation map and approved-plan preview. Only `RELEASE_GATE2_APPROVAL` may carry Owner Gate 2 authority, bound to an explicit affirmative owner decision on one exact fresh-verified PR-head Preview. No other operation may carry either owner gate or GitHub merge authority; all guarded Production requests remain read-only.

A generic owner `Proceed` may be converted into a request only when the next bounded operation is already unambiguous under repository policy. It is never an owner-gate approval or recovery authorization. `STAGE2_GATE1_FILL` therefore requires a separately explicit Owner Gate 1 approval before the request may be authored.

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

## 8. Stage 2 capability census request

`STAGE2_CENSUS` is read-only with respect to tracked basketball state and stops at the permanent coordinator's first discovery boundary.

The request binds the exact current protected-main SHA, exact existing onboarding branch and SHA, exact Phase 0 successor manifest path/hash, exact Integration Freeze SHA-256, and exact source-game semantic snapshot SHA-256. A changed or missing onboarding head is a STOP.

The runner authenticates the Phase 0 successor and write-ahead authority already preserved on the control branch, restores only the exact ignored `.onboarding/<school>/integration-freeze.json` required by the permanent Stage 2 coordinator, and verifies the frozen six-file package hashes against the request-bound onboarding commit. It does not regenerate Integration Freeze and does not copy arbitrary historical `.onboarding` state.

It then invokes unchanged:

```bash
python tools/implementation_stage2.py <school>
```

inside an isolated worktree at the exact onboarding SHA. Before and after execution it records HEAD/tree and a complete non-ignored worktree status. Success requires:

```text
TRACKED_STAGE2_MUTATION = NONE
```

The runner persists only the defined discovery artifacts emitted by that invocation when present: `implementation-stage2-status.json`, `implementation-stage2-capability-census.json`, `plan.json`, `review.csv`, and `review.md`. The checkpoint records exact and runner-path-normalized SHA-256 values, permanent-command exit code, Stage 2 status, preflight counts, decision-universe SHA, capability-census status/topology, exact onboarding tree, Phase 0 authority hashes, and the tracked-mutation proof.

A normal result is either:

- `CAPABILITY_CENSUS_READY`; or
- an honest permanent-tool `BLOCKED` checkpoint.

A permanent Stage 2 blocker is durable discovery evidence, not a remote-execution failure. An accepted request that fails before a durable checkpoint remains non-replayable and requires explicit `RECOVER`, using the same read-only recovery boundary as Stage 1.

Fresh verification reconstructs the same onboarding SHA and exact Integration Freeze, reruns unchanged `implementation_stage2.py <school>`, requires the same decision-universe SHA and capability-census semantics, and again proves no tracked mutation. Exact artifact bytes must match when deterministic; the only permitted normalized equivalence is replacement of the fresh runner's absolute repository path with the explicit `<REPO>` token.

`STAGE2_CENSUS` itself does **not** authorize tracked Stage 2 repairs, recommendation-map submission, `--map`, proposal rehearsal, `OWNER_GATE_1_READY`, owner approval, sealing/apply, Preview, or release. A separate exact-map `STAGE2_PROPOSAL_REHEARSAL` request is required after blocker-free Stage 2 authority and a mature recommendation map exist.

### Stage 2 opponent-display normalization mutation

`STAGE2_OPPONENT_DISPLAY_NORMALIZE` is the sole productionized remote tracked Stage 2 repair. It is not a generic repair executor. It may run only when an exact prior `STAGE2_CENSUS` checkpoint is `BLOCKED` solely by deterministic historical opponent-display conflicts, with zero warnings and zero owner decisions.

The request binds the exact current protected-main SHA, existing onboarding branch and predecessor SHA, authoritative Stage 2 census checkpoint path/hash, Integration Freeze SHA-256, semantic snapshot SHA-256, and an authority boundary that excludes Phase 0, recovery, owner gates, release, and unrelated Stage 2 work. A changed onboarding head is a STOP.

The runner uses the real global mutation lock and executes this sequence:

```text
IDLE
→ exact request/census/Freeze authenticated
→ global Implementation lock durable
→ isolated exact predecessor worktree
→ permanent normalizer dry-run with --sync-source-games
→ exact census blocker-key equality + ambiguous-key count zero
→ permanent normalizer --sync-source-games --apply
→ representation-only field proof + semantic-drift PASS
→ repository validation
→ exact prepared commit/tree/diff
→ write-ahead authority durable
→ existing onboarding ref predecessor→prepared CAS
→ unchanged implementation_stage2.py <school> regeneration without --map
→ durable successor + lock release → IDLE
→ fresh-runner equivalence verification
```

The permanent helper, not the remote runner, chooses the authoritative display. The mutation boundary is exact:

- only `schools/<school>/opponents.csv` and `schools/<school>/source-games.csv` may change;
- `opponents.csv` may change only `canonical_opponent_name`;
- `source-games.csv` may change only `normalized_opponent_name`;
- opponent keys, literal source opponent labels, raw text, game identity, dates, scores/results, H/A/N, venues/locations, game type/postseason fields, and every other column must remain unchanged;
- the Integration Freeze semantic guard must be `PASS` before and after;
- the dry-run key population must equal the complete bound census blocker population exactly. A broader proposal is a STOP, not opportunistic cleanup.

Before publication, write-ahead state preserves the exact request, lock, census binding, target predecessor, prepared commit/tree, changed paths/file hashes, normalization report, field-level proof, Integration Freeze/semantic hashes, and semantic-drift proof. Publication is an expected-head CAS on the already-existing onboarding ref; unrestricted force updates are forbidden.

Recovery reuses the ordinary mutation classifier. `PREPARED_NOT_PUBLISHED` may be abandoned by explicit recovery; `PUBLISHED_NOT_FINALIZED` may be adopted only when the target is the exact prepared commit and all write-ahead/field proofs match, after which Stage 2 is regenerated before completion. Any other target is `DIVERGED_STOP`.

Fresh verification independently reauthenticates the original census request, reproduces the permanent normalizer dry run from the predecessor, recomputes the predecessor→prepared field proof, authenticates/restores the exact Integration Freeze, confirms semantic drift remains `PASS`, reruns unchanged Stage 2 without `--map`, compares exact/normalized discovery artifacts, and verifies no further tracked mutation.

This operation authorizes no recommendation map, proposal rehearsal, `OWNER_GATE_1_READY`, Gate 1, sealed apply, Preview, release, or arbitrary Stage 2 repair.

### Stage 2 proposal rehearsal request

`STAGE2_PROPOSAL_REHEARSAL` is read-only with respect to tracked basketball state. It exists only to authenticate one exact blocker-free Stage 2 authority record and one exact recommendation-map payload, then invoke the unchanged permanent coordinator through its existing `--map` path.

The request binds:

- exact current protected-main SHA;
- exact existing onboarding branch and SHA;
- exact blocker-free Stage 2 census checkpoint or post-repair successor path/hash;
- exact Integration Freeze SHA-256 and semantic snapshot SHA-256;
- exact decision-universe SHA-256;
- exact recommendation-map path in the request commit and exact map SHA-256;
- explicit proposal-rehearsal authority with Owner Gate 1, Owner Gate 2, fill/seal/apply, release, and unrelated tracked-repair authority absent.

The recommendation map is immutable request transport. The runner verifies its bytes/hash and never derives, rewrites, completes, or interprets recommendation actions. The permanent `validate_decision_map` path inside `implementation_stage2.py` remains the only map schema/completeness/action authority.

The runner authenticates the request-bound Stage 2 authority, restores only the exact ignored `.onboarding/<school>/integration-freeze.json`, creates an exact worktree at the request-bound onboarding SHA, and invokes current production runtime tooling conceptually as:

```bash
python <runtime>/tools/implementation_stage2.py <school> --repo <exact-target-worktree> --map <exact-map>
```

Basketball/package bytes come from the exact target worktree. Permanent tooling comes from the current production runtime checkout. Stale tool copies embedded in an older onboarding commit are not executed.

Before and after the permanent invocation, the runner proves exact HEAD/tree stability and a clean non-ignored worktree. The required result is:

```text
TRACKED_STAGE2_MUTATION = NONE
```

No target-branch push or tracked-mutation CAS exists for this operation.

A normal permanent result is either:

- `OWNER_GATE_1_READY`, meaning only that the exact recommendation map survived the permanent disposable proposal rehearsal; or
- `BLOCKED`, preserving the permanent failure evidence without synthesizing a replacement outcome.

The durable checkpoint preserves, where generated: the exact recommendation map, Stage 2 status/capability census, plan, review CSV/Markdown, site-gate diagnostic, permanent proposal-rehearsal summary, approved-plan-hash preview, action/changed-path counts, exact and normalized artifact hashes, runtime tool hash/current-main commit, Stage 2 authority binding, Integration Freeze/semantic bindings, decision-universe hash, and tracked-mutation proof.

A malformed/incomplete/stale recommendation map, invalid action, proposal-apply failure, site/releaseability gate failure, or other permanent coordinator stop is a **PERMANENT PROPOSAL REHEARSAL BLOCKED** result when the permanent status artifact is successfully produced. Failure before a durable permanent result—such as payload hash mismatch, changed target ref, authority tampering, or runner/tool execution failure—is a **REMOTE EXECUTION FAILURE** and uses the existing non-replayable accepted-request recovery model.

Fresh verification independently reauthenticates the same target SHA, Stage 2 authority, Integration Freeze, semantic snapshot, decision universe, and map bytes; reruns unchanged `implementation_stage2.py --map`; reproduces the same permanent status, approved-plan-hash preview when present, site/capability semantics, and exact/normalized artifact set; and again proves no tracked mutation.

`OWNER_GATE_1_READY` is not owner approval. This operation does not authorize filling, sealing, or applying the real review; Owner Gate 1 approval; Preview; Owner Gate 2; merge; Production proof; or arbitrary Stage 2 tracked repair.


### Stage 2 Owner Gate 1 fill request

`STAGE2_GATE1_FILL` is read-only with respect to tracked basketball state. It exists only after the owner has explicitly approved one exact proposal that already has a durable `OWNER_GATE_1_READY` checkpoint and independent fresh-runner proposal equivalence `PASS`.

The request binds:

- exact current protected-main SHA;
- exact existing onboarding branch, SHA, and proposal-bound tree;
- exact `OWNER_GATE_1_READY` proposal checkpoint path/hash;
- exact independent proposal-verification artifact path/hash;
- exact Integration Freeze and semantic snapshot SHA-256 values;
- exact decision-universe SHA-256;
- exact recommendation-map SHA-256;
- exact approved-plan preview hash;
- an explicit `owner_gate_1_approval` object whose proposal-checkpoint, decision-universe, recommendation-map, and approved-plan-preview bindings exactly equal the request;
- explicit `stage2_gate1_fill=true` and `owner_gate_1=true`, with Phase 0, census, opponent-display repair, proposal rehearsal, reconciliation diagnostic, recovery, Owner Gate 2, and release authority absent.

The runner independently authenticates both the proposal checkpoint and its fresh verification, reauthenticates the proposal's original Stage 2/Integration Freeze authority, recovers the exact checkpointed `plan.json`, unfilled `review.csv`, and recommendation map, and restores them only as ignored onboarding state inside an exact target worktree.

It then invokes current production runtime tooling conceptually as:

```bash
python <runtime>/tools/onboarding_hardening.py fill-review <school> \
  --repo <exact-target-worktree> \
  --review-file <checkpointed-review> \
  --map <checkpointed-map>
```

Success requires the permanent command to reproduce the exact proposal action counts and decision count, populate every review decision and resolution basis, preserve the exact decision-ID set, and leave target HEAD/tree and non-ignored worktree state unchanged. The durable checkpoint stores the exact filled review bytes/hash, source review hash, exact plan/map bytes and hashes, owner-approval hash, proposal/verification bindings, action counts, decision-ID-set hash, runtime tool hash, and tracked-mutation proof.

Fresh verification repeats the same authority checks and permanent fill on an independent runner and requires exact filled-review SHA-256, action counts, decision count, decision-ID-set SHA-256, runtime tool hash, and tracked-mutation proof.

This is a **fill-only** boundary. It does not run pre-seal rehearsal, cryptographically seal Gate 1, apply the sealed plan, mutate the onboarding branch, create Preview, approve Gate 2, merge, or release.



### Stage 2 pre-seal rehearsal request

`STAGE2_PRESEAL_REHEARSAL` is read-only with respect to tracked basketball state. It exists only after an exact `STAGE2_GATE1_FILL` checkpoint has completed as `FILLED` and its independent fresh-runner fill equivalence is `PASS`.

The request binds:

- exact current protected-main SHA;
- exact existing onboarding branch, SHA, and fill-bound tree;
- exact Gate 1 fill checkpoint path/hash;
- exact Gate 1 fill verification artifact path/hash;
- exact Integration Freeze and semantic snapshot SHA-256 values;
- exact decision-universe and recommendation-map SHA-256 values;
- exact approved-plan preview hash;
- exact filled-review SHA-256;
- exact decision-ID-set SHA-256;
- explicit `stage2_preseal_rehearsal=true`, with mutation, proposal, fill, diagnostic, recovery, Owner Gate 1, Owner Gate 2, and release authority absent.

The runner reauthenticates the entire Gate 1 fill authority chain, including the original explicit Owner Gate 1 approval. It restores the exact checkpointed Integration Freeze, plan, and filled review only as ignored onboarding state in an exact target worktree, then invokes current production runtime tooling conceptually as:

```bash
python <runtime>/tools/onboarding_hardening.py rehearse-review <school> \
  --repo <exact-target-worktree> \
  --plan-file <checkpointed-plan> \
  --review-file <checkpointed-filled-review>
```

The permanent command owns the disposable transaction and gate suite. The remote layer does not reproduce reconciliation or validation logic. It captures the permanent result as either:

- `READY_TO_SEAL` when the technical-readiness marker, approved-plan preview hash, changed-path count, and full gate suite pass; or
- `BLOCKED` when the permanent rehearsal itself exits nonzero.

A permanent `BLOCKED` rehearsal is durable technical evidence, not a remote-execution failure. Authority/hash drift, changed target refs, runtime failures, or tracked mutation remain remote-execution failures.

Before and after execution, target HEAD/tree and non-ignored status must remain unchanged. The durable checkpoint records the filled-review and approval bindings, runtime tool hashes, pre-seal status, changed-path count when available, normalized site-gate hash when emitted, tracked-mutation proof, and both raw/normalized rehearsal-log hashes as diagnostic evidence.

Fresh verification independently reauthenticates the same fill checkpoint and target SHA and reruns the same permanent rehearsal. Equivalence is determined only from stable structured technical-readiness facts: the `READY_TO_SEAL`/`BLOCKED` result, permanent-command exit code, approved-plan preview hash, changed-path count, normalized site-gate proof, runtime tool hashes, exact target tree, and tracked-mutation result. Those facts are hashed into a deterministic `equivalence_sha256`. Rehearsal-log hashes are not equivalence authority because disposable temp paths, warning paths, runner timing, and similar diagnostics may differ across otherwise equivalent runs. Raw and normalized log hashes remain preserved for audit and diagnosis, and normalization removes ephemeral `/tmp/<root>` basenames and unittest elapsed time where possible.

This operation supplies **technical readiness only**. It does not cryptographically seal Gate 1, run sealed apply, mutate the onboarding branch, create Preview, approve Owner Gate 2, merge, or release.



### Stage 2 Gate 1 seal request

`STAGE2_GATE1_SEAL` creates cryptographic Owner Gate 1 authority while remaining read-only with respect to tracked basketball state. It exists only after an exact pre-seal checkpoint is `READY_TO_SEAL` and its independent fresh-runner pre-seal equivalence is `PASS`.

The request binds:

- exact current protected-main SHA;
- exact onboarding branch, SHA, and pre-seal-bound tree;
- exact pre-seal checkpoint path/hash and independent verification path/hash;
- exact Integration Freeze and semantic snapshot SHA-256 values;
- exact decision-universe and recommendation-map SHA-256 values;
- exact technical approved-plan preview hash;
- exact filled-review SHA-256 and decision-ID-set SHA-256;
- exact prior Owner Gate 1 approval SHA-256;
- exact source pre-seal structured-equivalence SHA-256;
- explicit `stage2_gate1_seal=true`, with new Owner Gate 1 authority, Stage 2 fill/pre-seal mutation authority, recovery, Owner Gate 2, release, and sealed-apply authority absent.

The source pre-seal checkpoint may have been created before a later tooling-only protected-main advance. The seal operation therefore does not merely trust the old runtime result. After authenticating the complete prior Owner Gate 1/pre-seal chain, it re-runs the permanent `rehearse-review` suite on the request-bound current protected-main runtime against the same exact target SHA, plan, filled review, and Integration Freeze. Current-main sealing may continue only when that replay remains `READY_TO_SEAL` and reproduces the same approved-plan preview hash, changed-path count, normalized site-gate proof, and no tracked mutation.

Only then does the runner invoke the unchanged permanent seal path conceptually as:

```bash
python <runtime>/tools/onboard_school.py <school> --approve \
  --repo <exact-target-worktree> \
  --output-dir <ignored-seal-output> \
  --plan-file <checkpointed-plan> \
  --review-file <checkpointed-filled-review> \
  --approved-by project-owner
```

The final sealed `approved_plan_hash` is the real mutation authority for the later apply step. It is distinct from the deterministic technical preview hash because the real seal contains approval metadata, including its actual approval timestamp. The checkpoint preserves the exact `approved-plan.json` and `approved-review.md` bytes/hashes, approved-plan hash, approval metadata, source pre-seal authority, current-main pre-seal replay proof, permanent-tool hashes, exact target tree, and tracked-mutation proof.

Fresh verification must not mint a second seal with a new timestamp. Instead it independently:

1. reauthenticates the same pre-seal authority and exact target;
2. reruns the permanent pre-seal suite on current protected-main runtime;
3. verifies the current permanent `onboard_school.py` / `onboarding_plan.py` tool hashes;
4. verifies the checkpointed approved-plan cryptographic hash and input fingerprint;
5. reconstructs the exact approved plan from the checkpointed plan/review using the seal's own `approved_by` and `approved_at` metadata through permanent `approve_plan`;
6. reproduces the exact approved-plan bytes and approved-review rendering; and
7. again proves tracked basketball mutation remains `NONE`.

Only then may the verification record say `remote_stage2_gate1_seal_equivalence = PASS`.

This is a **seal-only** boundary. It creates the exact approved-plan authority but does not run `--apply`, archive sealed decisions into tracked basketball state, mutate the onboarding branch, create Preview, approve Owner Gate 2, merge, or release.



### Stage 2 sealed apply request

`STAGE2_SEALED_APPLY` is the tracked-mutation boundary that consumes one exact fresh-verified cryptographic Owner Gate 1 seal. Unlike fill, pre-seal, and seal, it is a serialized mutation operation: it acquires the one-active-Implementation global lock and must remain recoverable from durable write-ahead state.

The request binds:

- exact current protected-main SHA;
- exact existing onboarding branch, predecessor SHA, and seal-bound tree;
- exact Gate 1 seal checkpoint path/hash and independent seal-verification path/hash;
- exact final sealed `approved_plan_hash` and approved-plan file SHA-256;
- exact prior Owner Gate 1 approval SHA-256;
- exact Integration Freeze and semantic snapshot SHA-256 values;
- exact decision-universe and recommendation-map SHA-256 values;
- exact filled-review and decision-ID-set SHA-256 values;
- explicit `stage2_sealed_apply=true`, with new Owner Gate 1 authority, Gate 2 authority, release authority, unrelated Stage 2 mutation authority, and recovery authority absent.

The runner authenticates the complete seal chain and exact approved-plan bytes before acquiring the mutation lock. After the lock is durably bound, it creates an exact worktree at the request-bound onboarding predecessor and replays the permanent pre-seal technical suite on current protected-main runtime. Mutation may continue only when that replay remains `READY_TO_SEAL` and reproduces the seal-bound technical preview, changed-path count, site-gate proof, and no tracked mutation.

The runner then invokes current production runtime tooling conceptually as:

```bash
python <runtime>/tools/onboard_school.py <school> --apply \
  --repo <exact-target-worktree> \
  --output-dir <ignored-apply-output> \
  --approved-plan <exact-final-sealed-hash> \
  --approved-plan-file <checkpointed-approved-plan.json>
```

The permanent `--apply` path owns basketball mutation and validation. It first rehearses the complete sealed transaction in a disposable repository, runs the full automated gate suite, and only then copies the allow-listed validated changes into the real target worktree. The remote layer does not duplicate reconciliation or gate logic.

After permanent apply succeeds, the remote layer requires the target worktree's tracked path set to equal the permanent `release-manifest.json` changed-path set exactly. It stages only those exact paths, never `git add -A`, and creates one successor commit whose parent is the request-bound predecessor. The prepared commit records the exact tree, changed paths, post-commit file hashes, explicit deletion set, runtime tool hashes, and permanent release-manifest proof.

Before any target-branch publication, control must durably commit a write-ahead bundle containing at minimum:

- exact request/seal authority;
- global lock commit;
- current protected-main SHA;
- exact predecessor/prepared commit/tree/parent;
- changed-path list, changed-file hashes, and explicit deletion list;
- exact approved-plan bytes/hash;
- Integration Freeze;
- seal checkpoint and seal verification;
- current-main pre-seal replay proof;
- permanent release manifest plus its SHA-256;
- review/visual-QA sidecars emitted by permanent apply when present.

Only after write-ahead is committed and bound may the runner publish the prepared successor to the existing onboarding branch, using expected-predecessor CAS. A changed target is a STOP; no force push or blind overwrite is permitted.

Recovery follows objective mutation state:

- `NOT_ATTEMPTED` or `PREPARED_NOT_PUBLISHED`: explicit recovery may abandon the active request without mutating the target ref.
- `PUBLISHED_NOT_FINALIZED`: recovery may adopt only when the target ref is the exact write-ahead prepared commit and its parent, tree, path set, file hashes, and deletion set all match.
- any other target state: `DIVERGED_STOP`.

After publication, the durable successor records the exact predecessor and prepared successor, seal authority, write-ahead identity, changed paths/hashes/deletions, release-manifest hash, current-main pre-seal proof, runtime hashes, publication CAS result, and recovery status when applicable. Control then returns to `IDLE / COMPLETE`, but fresh verification remains pending.

Fresh verification independently starts again from the exact predecessor commit. It:

1. authenticates the successor, write-ahead bundle/sidecars, original request, and fresh-verified seal;
2. verifies the published successor commit's exact parent/tree/path/file/deletion proof;
3. replays current-main pre-seal;
4. reruns the full permanent sealed apply against the same predecessor without creating a second published commit;
5. requires the fresh staged Git tree to equal the published successor tree exactly;
6. requires exact changed paths, post-mutation file hashes, and deletions;
7. compares stable release-manifest authority fields and deterministic PR-body / visual-QA sidecars when present.

Only then may the verification artifact say `remote_stage2_sealed_apply_equivalence = PASS`.

This operation ends at a fresh-verified tracked apply successor. It does **not** prepare the release PR or Preview, approve Owner Gate 2, merge, or perform Production proof.



### Read-only remote release readiness (not PR preparation)

`RELEASE_READINESS` is a bounded **read-only** technical boundary available only after an exact independently fresh-verified `STAGE2_SEALED_APPLY` successor. It does not create a pull request, start or approve Preview, request Owner Gate 2, merge, or change tracked basketball state.

Its request is bound to exact current protected-main SHA, existing onboarding branch and successor SHA, the exact earlier Stage 2 sealed-apply successor manifest path/hash, the independent sealed-apply verification path/hash, final `approved_plan_hash`, release-manifest SHA-256, and an exclusive `release_readiness=true` authority field. All other operation/owner/PR/release authority flags must be false. A generic owner `Proceed` can authorize this reversible technical boundary only after the predecessor is unambiguous and the control state is IDLE.

The runner authenticates the original applied predecessor/successor tree, exact write-ahead sidecars, per-file hashes and deletions, sealed approved-plan bytes, changed-path set, and independent fresh-runner equivalent apply tree. It requires unchanged protected main and exact target ref before and after execution. The global read-only operation state is durably checkpointed; a failed accepted request requires explicit recovery and is not replayable.

The permanent release validation gates are invoked against an isolated clean checkout of the committed successor, using the current runtime's unchanged `release_school.run_gates`. The exact committed path boundary is checked before and afterward through `release_school.verify_committed_change_boundary`. Only exact authenticated ignored release artifacts may be restored from the durable write-ahead. The runner never calls `release_school.py --prepare`, GitHub `gh pr create`, or any deployment mutation.

A successful request checkpoints `RELEASE_READINESS_PASS` with exact proof SHA, source successor and verification hashes, release-manifest hash, a tracked-mutation `NONE` declaration, and explicit `pr_created=false`, `preview_verified=false`, `owner_gate_2=false`. A fresh independent runner authenticates the same authority, reruns the permanent final gates, compares the stable structured proof exactly, confirms the target ref is unchanged, and durably records `remote_release_readiness_equivalence = PASS`.

This is **not** `OWNER_GATE_2_READY`. A subsequent separately productionized authenticated PR/CI/Preview unit is required to reach that boundary. The operational GitHub Action still has no `pull-requests:write` scope and must not create PRs using its ordinary `GITHUB_TOKEN` as a shortcut that would produce CI approval friction.

### Exact remote PR/CI/Preview verification

`RELEASE_PREVIEW_VERIFY` is a separate bounded, read-only control operation after a completed and independently fresh-verified `RELEASE_READINESS` checkpoint **and** creation of the onboarding release PR by the school Implementation chat through its authorized GitHub connector. The ordinary GitHub Actions `GITHUB_TOKEN` is never used to create the PR: PR creation must trigger the repository's ordinary required CI and Vercel Preview workflows without a routine owner-side `Approve workflows to run` step.

A school Implementation lane may advance both internal boundaries within **one** owner-authorized release `Proceed`: authenticate the sealed apply, submit/monitor release readiness through independent PASS, then use its GitHub connector to create or reuse the exact school-specific PR with the preserved approved `pr-body.md`, submit/monitor `RELEASE_PREVIEW_VERIFY`, and present the resulting Preview. These are bounded, serialized operations; do not submit a second remote request while an earlier request is active or unverified. If any intermediate phase blocks, stop at its durable checkpoint and do not keep advancing.

The preview-verification request binds current main, exact school target ref/SHA, approved-plan hash, sealed release-manifest hash, the exact release-readiness checkpoint path/SHA-256, its independently fresh PASS verification path/SHA-256, and the **existing** PR number. It carries only `release_preview_verify=true`, with all mutation, `release`, Owner Gate 1, and Owner Gate 2 authority false. It authenticates the complete earlier sealed apply and readiness chain, the prior exact approved PR-body bytes, the ancestry of any later tooling main, and the unchanged target SHA.

The permanent `release_school` helpers, not new replica release logic, check the PR's exact open/non-draft state, base `main`, correct head branch and **exact sealed-apply successor SHA**, exact PR body SHA-256, successful GitHub PR checks, clean mergeability, and the successful Vercel `Preview` deployment associated with **that exact PR head SHA**. The PR state, target Git ref, and body are rechecked after Preview. A Preview deployment is never accepted as Production proof.

On success, the runner durably checkpoints `OWNER_GATE_2_READY` with PR number/URL, exact head, Preview URL/deployment ID/SHA, earlier readiness authority, and explicit `owner_gate_2_approved=false`, `merged=false`, `production_proof=false`. An independent fresh runner repeats exact PR/CI/Preview verification, compares the stable structured result, and checkpoints `remote_release_preview_equivalence=PASS`. The school chat then presents the exact PR-head Preview and `visual-qa.md` to the owner and **stops**. Ordinary `Proceed` never constitutes Owner Gate 2 approval. No merge or Production proof is available through this new operation.

A failed accepted request remains durable and non-replayable; explicit authorized recovery is required. A missing PR or mismatched head, unauthorized changed body, failed/absent checks, missing/mismatched Preview, moved target branch or main, or lack of fresh prior readiness must fail closed, not be bypassed.

### Explicit Owner Gate 2 approval (read-only) and exact post-merge Production proof

`RELEASE_GATE2_APPROVAL` is an **explicit owner-authority** boundary, never inferred from generic `Proceed`. It accepts the exact previously fresh-verified `OWNER_GATE_2_READY` checkpoint and its independent verification, PR number and head SHA, successful Preview deployment ID/URL, approved-plan/release-manifest hashes, current protected-main SHA, and a scoped `owner_gate_2_approval` object with `approved=true` and the same exact preview/checkpoint/PR bindings. The request must state the owner's affirmative approval basis; any missing or conflicting authority fails closed. It carries `owner_gate_2=true` and `release_gate2_approval=true`; no merge/release or other operation authority is granted.

The runner authenticates the complete previous sealed-apply/readiness/Preview chain, rechecks the currently open non-draft same-repository PR, exact approved head and body, passing PR checks and clean mergeability, and the precise successful Preview deployment. It then persists `OWNER_GATE_2_APPROVED` with `merged=false`, `production_proof=false` and the exact approved scope. A separate fresh runner repeats the PR/Preview proof and independently records `remote_gate2_approval_equivalence=PASS`. No PR merge occurs inside the runner.

**Only after the fresh Gate 2 approval PASS**, the school Implementation chat may use its authorized GitHub connector to perform exactly one merge of the approved PR, supplying `expected_head_sha` equal to the approved head. Before merging it must recheck that protected main and the PR head remain at the exact approved identities, required checks and mergeability are passing, and no other Implementation lane is active. The standard repository merge method is a two-parent merge; squash/rebase or unapproved main changes are not acceptable. If connector permissions cannot perform the protected merge, STOP and escalate the permission boundary: do not bypass through an uncontrolled tool or broaden Actions credentials. A successful GitHub merge response is not Implementation COMPLETE.

`RELEASE_PRODUCTION_PROOF` is a separately bounded **read-only** remote request after that merge. It authenticates the exact independently fresh-verified Gate 2 approval checkpoint/verification, prior approved Preview head, PR identity/mergedAt/mergeCommit, and new exact protected-main SHA. The permanent release checker requires `main` to equal that exact merge commit with first parent equal to the Gate-2-approved main and second parent the exact approved PR head. The standard permanent `release_school` merged-main reproducibility checks run on an isolated detached merge checkout; exact SHA successful Vercel `Production` deployment is required, followed by public Production JSON equality for the target and **all** changed generated JSON from the complete merge diff (including earlier Phase 0 paths). The remote action is not allowed to change the merge, PR, or main.

The runner preserves a durable `PRODUCTION_PROOF_PASS` checkpoint with the precise merge SHA, both parents, Production deployment ID/SHA, counts and hashes of the checked generated files, and the original owner approval scope. Its independent fresh-runner verification reconstructs the exact merge, reruns the permanent gates and Production JSON comparisons, requires stable structured equivalence, and persists `remote_production_proof_equivalence=PASS`. Only then is Implementation `COMPLETE`; merge alone, successful Preview, or GitHub deployment metadata alone never suffice.

Failures after explicit Gate 2 approval or after the external GitHub merge require evidence-first recovery. Never blindly retry a merge. Inspect the exact PR merge SHA, current main SHA, global control state, pending request and durable checkpoints; distinguish missing Production deployment from mismatched JSON or wrong commit. Any accepted failed remote request remains non-replayable until authorized recovery. Never infer new owner approval from earlier gate evidence if PR HEAD, approved Preview, or merge identity changes.

These are generic capabilities and **the school Implementation chat**, not the Control Center, executes them for every authorized school. The Owner Gate 2 approval is a real, necessary owner decision; technical request submission and post-merge checks are not additional owner gates.

### Stage 2 reconciliation diagnostic request

`STAGE2_RECONCILIATION_DIAGNOSTIC` is read-only with respect to tracked basketball state. It exists only after an exact `STAGE2_PROPOSAL_REHEARSAL` has durably completed as `BLOCKED`, when one canonical game requires compact transaction-path diagnosis rather than conversational repository archaeology.

The request binds:

- exact current protected-main SHA, which supplies the diagnostic runtime;
- exact existing onboarding branch and SHA;
- exact prior blocked Stage 2 proposal checkpoint path/hash;
- exact Integration Freeze SHA-256 and semantic snapshot SHA-256 inherited from that checkpoint;
- exact decision-universe and recommendation-map SHA-256 values inherited from that checkpoint;
- one exact canonical game ID;
- explicit diagnostic authority with census, opponent-display mutation, proposal rehearsal, recovery, Owner Gate 1, Owner Gate 2, and release authority absent.

The runner authenticates the prior blocked proposal checkpoint and its original proposal request, recovers the exact checkpointed `plan.json`, `review.csv`, recommendation map, and Integration Freeze, and restores those ignored inputs only inside an exact worktree at the request-bound onboarding SHA. It then invokes current production runtime tooling conceptually as:

```bash
python <runtime>/tools/onboarding_hardening.py diagnose-reconciliation <school> \
  --repo <exact-target-worktree> \
  --plan-file <checkpointed-plan> \
  --review-file <checkpointed-review> \
  --map <checkpointed-map> \
  --canonical-game-id <CBBG-ID>
```

The permanent diagnostic observes the real reconciliation implementation rather than reimplementing basketball logic. Its durable trace records the selected game's canonical/source/assertion path, actual decision order and mutations, site-metadata synchronization branch where applicable, final integrity result, and whether a partial city/state pair was introduced, mutated, or merely persisted.

Before and after execution the runner proves exact target HEAD/tree stability and a clean non-ignored worktree. The checkpoint preserves the exact trace bytes/hash, source proposal authority, runtime tool hashes, target/Freeze/semantic/decision/map bindings, and tracked-mutation proof. No target-branch push exists for this operation.

Fresh verification independently reauthenticates the same prior proposal checkpoint and target SHA, reruns the same permanent diagnostic with the same canonical game ID using current protected-main runtime, requires the exact same trace SHA-256 and summary classification, and again proves no tracked mutation.

This operation supplies no historical decision, repair recommendation, Owner Gate 1 approval, tracked Stage 2 mutation, Preview authority, merge authority, or release authority. Its output is diagnostic evidence for the next bounded Implementation unit.

## 9. Write-ahead and objective mutation state

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

## 10. Publication and fresh verification

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

## 11. Recovery

There is no automatic retry of an accepted request.

A recovery request must bind the exact active request and exact lock commit. It inspects durable write-ahead authority and the actual target ref.

- `NOT_ATTEMPTED` or `PREPARED_NOT_PUBLISHED`: the failed request may be explicitly abandoned and the lock released.
- `PUBLISHED_NOT_FINALIZED`: the already-published commit may be adopted only when the exact commit/tree/ref/write-ahead authority matches.
- `DIVERGED_STOP`: fail closed. Do not reset, overwrite, or guess.
- stale recovery authority is refused.

A successful abandonment leaves the global lifecycle `IDLE` with a durable
`transaction_state` of `ABANDONED_NOT_ATTEMPTED` or
`ABANDONED_PREPARED_NOT_PUBLISHED`, not an invented `COMPLETE` result. Both
are valid only with matching `RECOVER` last-operation evidence, a recorded
abandoned original request, a consumed recovery request, and a matching
mutation classification in the immutable recovery manifest. The fresh verifier
may then report the ordinary Phase 0 check as not applicable. Do not rewrite
historical recovery checkpoints simply to normalize the transaction label.

Another school may not enter while the global control is not IDLE.

## 12. Permissions and protected main

The permanent workflow receives only repository `contents: write` permission because it must:

- commit durable control/checkpoint state to the control branch; and
- create the authorized onboarding branch ref.

It does not receive pull-request, deployment, environment, administration, or protected-main bypass authority.

Protected `main` is read as the exact integration base. The runner never pushes to `main`.

Remote Stage 2 capability is limited to the read-only census, the census-bound `STAGE2_OPPONENT_DISPLAY_NORMALIZE` representation repair, exact-map read-only `STAGE2_PROPOSAL_REHEARSAL` through permanent-tool `OWNER_GATE_1_READY` or durable `BLOCKED`, exact-owner-approval read-only `STAGE2_GATE1_FILL`, read-only filled-review `STAGE2_PRESEAL_REHEARSAL`, read-only cryptographic `STAGE2_GATE1_SEAL`, transactional `STAGE2_SEALED_APPLY`, read-only `RELEASE_READINESS` final-gate verification, read-only `RELEASE_PREVIEW_VERIFY` exact PR-head CI/Preview verification, and the read-only blocked-proposal `STAGE2_RECONCILIATION_DIAGNOSTIC` described above. Other tracked Stage 2 repairs remain unauthorized. The remote runner cannot merge or push protected main; explicit scoped Owner Gate 2 approval and post-merge Production proof are separately guarded, and merge is performed only by the authorized school Implementation connector after approval.

## 13. Mobile / ChatGPT operation

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

## 14. Experimental provenance

The accepted architecture experiments remain historical audit evidence on the existing `experiment/remote-implementation-proof*` branches.

Production code was extracted from the proven invariants; experimental `.remote-implementation-poc/` state is not merged into protected main.

The accepted Proof 6 end-to-end evidence includes the LIU disposable Phase 0 result and fresh-runner equivalence proof on the Proof 6 control branch. Those branches should be retained unless a separately authorized cleanup policy preserves equivalent audit provenance elsewhere.
