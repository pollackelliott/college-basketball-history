# Stage A: Unattended Connector Handoff — Shadow Proof of Concept

**Authority:** Control Center owner authorized **Stage A only** on 2026-11-17.
**Scope:** inert, read-only observation and synthetic tests. No worker deployment,
GitHub App registration/installation, permission change, endpoint subscription,
school Implementation, PR creation/merging by an executor, control request, or
GitHub workflow dispatch. The tooling development PR is not a school release PR.

## Exact-current-main baseline

This prototype was authored against protected main
`653f65d89f68ed273a8db5a8717bacecc89a4a99`
and the unchanged global control sequence 625. The controlling process is
`AGENTS.md`, `docs/remote-implementation-runner.md`, and
`docs/implementation-efficiency-recovery.md`.

## Behavior

`tools/remote_implementation_connector_shadow.py` is a **pure decision core**
plus an optional **read-only Git CLI**:

```bash
python tools/remote_implementation_connector_shadow.py --repo .
```

The CLI performs **only** remote `git ls-remote` and local `git show` reads.
For exact checkpoint inspection, the local checkout must already contain the
fetched control commit. If the Git object is absent, the observer fails closed;
the observer itself does not fetch, check out, commit, push, merge, dispatch
workflows, or make HTTP calls. An operator may refresh a disposable read-only
checkout independently for observation, but this is not part of Stage A.

The observer authenticates the exact live main/control refs; the raw control
state from that immutable control commit; the `IDLE / COMPLETE`, no-lock,
no-recovery state; one exact source request and checkpoint; the unchanged
source-request hash; the stage-specific independently fresh `PASS`
verification; and the exact packet hash and cross-bound fields.

Eligible last operation:

1. `RELEASE_READINESS` with `RELEASE_READINESS_TO_PREVIEW_V1`:
   authenticate archived PR packet, exact preserved PR body, immutable target,
   explicit future Preview request identity. Return
   `WOULD_CREATE_OR_REUSE_EXACT_PR_AFTER_LIVE_CHECKS`.
2. `RELEASE_GATE2_APPROVAL` with `RELEASE_GATE2_TO_PRODUCTION_V1`:
   authenticate archived owner-approved Gate 2 packet and its fresh verifier,
   exact approved main, PR/head/Preview identities, mandatory merge method
   `merge`, and exact future Production-proof ID. Return
   `WOULD_MERGE_EXACT_APPROVED_PR_AFTER_LIVE_CHECKS`.

For any other completed operation, including **UCF's final
`RELEASE_PRODUCTION_PROOF`**, return `NO_ELIGIBLE_HANDOFF` and **perform no
packet reads or actions**. A source whose fresh verification is not PASS returns
`NOT_READY`. Missing/mismatched authority, moved refs, occupied control,
wrong hash, changed body/approval, and unsafe state produce a fail-closed
`STOP`. Every return has `actions_executed=0` or the equivalent zero-action
contract.

Every candidate record expressly says
`external_pr_ci_preview_preconditions=NOT_CHECKED_BY_SHADOW` and
`execution_authorized_by_this_tool=false`. It is **not** a declaration that
the live PR, required checks, Preview, mergeability or GitHub App capability
are valid. Those would require fresh read-only GitHub checks and a separately
approved, real executor before any write-capable stage.

`webhook_wakeup()` is a **pure signed-event parser**, not an installed
webhook receiver. It authenticates an HMAC-SHA256 payload and only recognizes
completed workflow-run events. The result is scheduling data, not owner
approval or authority to act. Duplicate events deterministically yield the
same wakeup; authority always comes from Git, never from the event.

The receipt's `work_item_sha256` is a deterministic identity derived from
repository, school, source operation/request ID and packet hash. It is **not**
an exactly-once ledger or durable event log. Stage B must design durable
deduplication and crash recovery before enabling PR mutations.

## Tests and explicit non-goals

The synthetic tests cover both authenticated packet types; missing fresh PASS;
body/request/packet tampering; mismatched main or target; changed Gate 2
approval; non-`merge` method; changed child IDs; occupied lock; repeated and
tampered webhook delivery; and a completed-UCF-shaped `NO_ELIGIBLE_HANDOFF`
that does not read old packets. They require no credentials or network.

**Stage A is not approved as an unattended production service.** It does not
create PRs, trigger PR/Preview checks, merge, queue child requests, run
Production proof, install a GitHub App, grant Actions permissions, change
protected-main policy, or supersede Gate 1/Gate 2. It does not supply
`RELEASE_PREVIEW_VERIFY` or `RELEASE_PRODUCTION_PROOF` automation.

## Stage A exit criteria

- Pure read-only observer and auth checks reviewed and tested on exact PR head.
- UCF-complete shaped fixture reports no action; no live UCF replay.
- Both hypothetical connector packets yield shadow-only candidate reports with
  zero writes and explicit unverified live external preconditions.
- Negative/duplicate-event cases fail closed.
- No new permissions, workflow deployment, changes to basketball data, control
  state, or protected main during the shadow evaluation.
- Separate owner review of app identity, credential custody, hosting, live PR
  checks, durable dedup, trusted child request dispatch, and branch protection
  **before** Stage B. Stage C (merge capability) requires an additional owner
  decision after Stage B validation.

**Current status:** Stage A source/test proof only, no activation. Opening or
merging this inert tooling code is not permission to deploy a listener or enable
mutating connector actions.
