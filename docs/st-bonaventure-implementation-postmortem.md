# St. Bonaventure Implementation postmortem

- **Status:** Control Center maintenance record
- **Completed school:** `st-bonaventure`
- **Final protected-main merge:** `53c0778f5c1f3f6b01dae144a4c6f805ab8d9146`
- **Release PR:** #465
- **Production-proof checkpoint SHA-256:** `6c3ede558cbdba01b34f5724c48e7d738eb8e698cc7fb6fc5b67b6d3e6410c72`
- **Production proof:** PASS
- **Global Implementation control after completion:** IDLE / COMPLETE / `recovery_required=false`

## Executive summary

St. Bonaventure completed correctly, but the path was operationally unacceptable.

The school exposed a legitimate combination of difficult historical and representation
topologies. The repository handled those topologies fail-closed, which protected data
quality. The failure was that adjacent generic defects were repeatedly discovered only
_after_ the preceding repair had merged and the school had been refreshed, re-censused,
and replayed.

Between PR #441 and PR #464, St. Bonaventure exposed **20 merged generic
tooling/capability repairs** before the final onboarding PR #465. Many of those repairs
were individually correct. The process defect was serial discovery.

A second failure amplified the cost: the guarded remote runner represented deterministic
phase continuations as multiple independent GitHub Actions requests. The owner therefore
became the scheduler for refresh -> census -> proposal and similar chains, repeatedly
sending `Continue` while waiting for Actions even though no new owner authority was
required.

This postmortem does not recommend weakening Integration Freeze, owner gates, fresh
verification, expected-predecessor CAS, or fail-closed historical safeguards.

## What happened

The repair train clustered into a small number of families.

### 1. Stage 1 / Phase 0 venue representation

PRs #441-#445 added or repaired:

- reused physical venue identities;
- explicit locality variants;
- preserved relationship-bearing local rows;
- frozen-locality summary matching; and
- post-rebase summary authentication.

These were related representation states and should have been exercised as one
end-to-end Stage 1 -> Phase 0 topology before the family was considered closed.

### 2. Stage 2 frozen-authority propagation

PRs #446, #449, #451 and #454 successively exposed:

- Stage 2 ignoring frozen per-game split authority;
- disposable runtime losing the Integration Freeze;
- sealed pre-ingest mutations being rejected against pre-mutation semantics; and
- reconciliation rebuilding venue maps without the same frozen authority.

The common defect was lifecycle propagation of one authenticated authority through
multiple runtime boundaries.

### 3. Stage 2 patch transport and final semantic verification

PRs #447-#448 and #456-#458 exposed:

- an already-settled new-game date correction missing from the decision universe;
- compact-map transport not sharing one patch-capability registry;
- final target no-op verification using only pre-ingest semantics;
- incomplete final source-semantic projection; and
- final fields being rejected by a pre-ingest-only matcher.

Again, the individual regressions proved local fixes while the complete sealed
transaction still had unexercised downstream boundaries.

### 4. Decision-bound GAME_SITE relationships

PRs #459-#462 exposed, in sequence:

- no sealed target-school GAME_SITE relationship capability;
- frozen venue-byte authentication rejecting the exact sealed suffix;
- reconciliation selecting final venue semantics at the wrong call site; and
- one boolean incorrectly coupling venue-file phase and source-semantic phase.

PR #462 finally modeled the mixed reconciliation state explicitly. The preceding three
repairs were evidence that the complete lifecycle state space had not been exercised
before merge.

### 5. Genuine historical contradiction

PR #464 was different. Once generic reconciliation, post-apply no-op verification and
site completeness passed, the accomplishment cross-check exposed the frozen
March 12, 1978 Penn game as REGULAR_SEASON even though authoritative evidence and the
program accomplishment baseline required an NCAA Tournament appearance.

That was a real post-freeze historical contradiction. The repository correctly routed
it into an explicit pending Gate 1 challenge instead of silently rewriting the Research
Freeze or reducing the accomplishment count.

## Root causes

### RC1 — repair acceptance was boundary-local, not transaction-global

A repair generally added a regression for the line or function that had just failed.
That is necessary but insufficient for a sealed transaction with multiple authority
phases.

The missing acceptance question was:

> With this candidate runtime, what is the terminal result of the exact blocked school
> proposal if we replay the entire disposable Stage 2 transaction now?

Because that question was usually asked only after merge, adjacent defects became
separate protected-main repair cycles.

### RC2 — authentication state was implicit and duplicated

Frozen venue bytes, frozen source semantics, sealed pre-ingest deltas, reconciliation
mutations and final verification were authenticated at several call sites with partially
overlapping flags and helpers.

The #459-#462 sequence showed the cost of implicit phase state directly. A valid
mid-reconciliation state required post-GAME_SITE venue authority while source semantics
were still pre-ingest; the old interface could not express that state.

### RC3 — capability census described decision topology better than execution topology

The Stage 2 census successfully reported the 232-decision universe and decision
categories, but it did not prove that every represented patch class could survive:

map transport -> approval -> pre-ingest -> ingestion -> reconciliation -> final no-op ->
site/accomplishment gates.

As a result, "232 decisions / 0 blockers / 0 warnings" was historically meaningful but
not a full executable-capability proof.

### RC4 — repository orchestration did not match phase-persistent authority

Policy correctly says owner authorization persists through deterministic substeps.
The remote architecture nevertheless exposed refresh, census, proposal, fill, pre-seal,
seal, apply, readiness and verification as separate requests.

That is safe at the control-plane level, but it pushed scheduling back into conversation.
The owner repeatedly had to send `Continue` merely to advance already-authorized work.

### RC5 — waiting policy encouraged chat-side polling

The efficiency standard attempted to avoid premature owner handoffs by telling the lane
to keep monitoring healthy workflows in the same turn, including a multi-minute
no-progress budget.

For a conversational execution surface without asynchronous continuation, that created
long turns full of status reads and still often ended in a transport yield. It optimized
for fewer messages at the cost of latency, context growth and owner frustration.

## What worked and must remain

The following safeguards materially protected the repository and should not be weakened:

- immutable Research Freeze evidence;
- Integration Freeze semantic guards;
- exact recommendation-map and decision-universe binding;
- read-only proposal rehearsal;
- explicit Owner Gate 1 / Gate 2;
- sealed transactional apply;
- expected-predecessor CAS;
- independent fresh verification;
- site completeness and accomplishment cross-checks;
- exact Production proof.

The 1978 Penn contradiction is evidence that these gates found a real historical defect
after the generic execution path was repaired.

## Corrective actions

### P0 — pre-merge candidate-runtime replay

Before merging a generic Stage 2 tooling repair that was exposed by a durable blocked
proposal, replay that exact blocked proposal against the candidate PR runtime.

The replay must:

- authenticate the exact blocked checkpoint and recommendation map;
- reconstruct the exact onboarding target and Integration Freeze;
- execute the candidate runtime's permanent `implementation_stage2.py --map`;
- prove tracked basketball mutation remains NONE;
- fail when the same blocker remains;
- report a different downstream blocker before merge; and
- reject candidate branches that contain basketball/reference data changes.

A different blocker is not automatically permission to merge. It must be classified
before merge as either the same repair family, a materially different generic family, or
a historical/owner boundary.

### P0 — phase-sized Actions orchestration

Add repository-owned continuation operations for deterministic phase chains, beginning
with the repeated post-tooling Stage 2 path:

`current-main refresh if required -> fresh census -> exact-map proposal -> fresh verification`.

The owner should not schedule each sub-operation.

The first implementation is `STAGE2_REFRESH_CENSUS_PROPOSAL_V1`: an optional
hash-bound continuation on the ordinary guarded refresh request. It does not collapse
the operations. Fresh refresh verification automatically queues the ordinary census;
fresh census verification queues the ordinary exact-map proposal only when the expected
decision-universe SHA is reproduced exactly. Each child retains its ordinary checkpoint
and independent verifier.

The same design should then be evaluated for:

- Gate 1 approval -> fill -> pre-seal -> seal -> sealed apply -> verification; and
- release readiness -> Preview readiness, where PR creation permissions permit.

Internal checkpoints remain durable. Bundling scheduling must not collapse authority
boundaries.

### P0 — bounded waiting, no chat-side idle loops

A chat may make a bounded status observation after dispatch, but it must not spend minutes
performing repeated no-progress polling merely to avoid returning control.

When a repository operation is still genuinely in flight and no useful independent work
remains, yield once with the exact workflow link and persistent phase authority.

Repeated transport yields inside one deterministic phase are themselves evidence that
repository orchestration is incomplete and should be fixed rather than normalized.

### P1 — full sealed-transaction regression topology

Maintain at least one generic high-complexity fixture that exercises, in one transaction:

- frozen reused-venue split authority;
- sealed pre-ingest semantic mutation;
- ingestion;
- reconciliation-time venue resolution;
- source normalization including date/overtime/game-type/site fields;
- sealed GAME_SITE append;
- mixed reconciliation authority;
- final source/venue authentication;
- target no-op;
- site gate; and
- accomplishment cross-check.

Local unit tests remain necessary, but a family repair is not complete when only its local
boundary is covered.

### P1 — execution-topology census

Extend Stage 2 capability reporting so it distinguishes:

- decision topology;
- patch-transport topology;
- authority-phase topology; and
- terminal gate topology.

This should identify unsupported execution combinations before the first repair merge
where they can be derived statically or by disposable rehearsal.

## Acceptance criteria

The maintenance is successful when:

1. a generic Stage 2 repair can replay the exact blocked school proposal against its
   candidate runtime before merge;
2. the same blocker cannot survive that gate unnoticed;
3. deterministic Stage 2 continuation after a tooling-only main advance requires one
   repository-owned Actions phase rather than owner-scheduled refresh/census/proposal;
4. ordinary chat execution performs no multi-minute idle polling loop;
5. owner interactions return to meaningful boundaries: genuine blocker, Gate 1, Gate 2,
   changed authority, or completion; and
6. no safeguard listed above is weakened.
