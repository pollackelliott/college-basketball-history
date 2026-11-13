# Control Center Succession and Recovery

- **Status:** Permanent governance/recovery protocol
- **Applies to:** any fresh or replacement College Basketball History Control Center conversation
- **Repository:** `pollackelliott/college-basketball-history`
- **Purpose:** recover authoritative project governance after a chat/context limit without replaying accepted work or creating a competing status system

## 1. Trigger and role

When the owner says **"New Control Center needed"**, **"successor Control Center"**, or otherwise identifies the conversation as the College Basketball History Control Center, assume the repository-wide governance/orchestration role.

The Control Center is not an ordinary school Research lane and is not an ordinary school Implementation lane.

A succession event does **not** authorize:

- reopening Research;
- starting another Implementation school;
- replaying a completed remote request;
- creating a maintenance campaign;
- bypassing Owner Gate 1 or Owner Gate 2;
- mutating protected `main`;
- treating a conversational handoff as repository authority.

The first action is a bounded, read-only recovery.

## 2. Authority order

Use this authority order:

1. current protected `main`;
2. current `AGENTS.md` and the controlling documents it requires;
3. the global remote Implementation control branch and its hash-bound checkpoints;
4. exact school branches, commits, PRs, immutable Research Freeze artifacts, Production proofs, and other durable repository evidence;
5. owner-supplied current lane/status hints;
6. pasted predecessor messages and conversational summaries.

Owner-supplied school lists and pasted messages are **recovery locators**, not a substitute source of truth.

Never manufacture a conflict merely because a conversational status is older than durable state. Report only material discrepancies.

## 3. Required initial recovery

Perform the following once, read-only, before repository-specific governance work.

### A. Authenticate protected main

Record the exact current SHA of protected `main`.

Read `AGENTS.md` from that exact protected-main authority. Read this document and every additional current policy/workflow document needed for the issue in front of the Control Center.

Do not rely on a SHA copied from the succession message when current Git/GitHub state is available.

### B. Authenticate global Implementation control

Authenticate the exact current head of:

`control/remote-implementation`

Read:

`.remote-implementation/control-state.json`

At minimum recover:

- `current_sequence`;
- `lifecycle_state`;
- `transaction_state`;
- `active_request_id`;
- `active_school_key`;
- `active_lock_owner`;
- `recovery_required`;
- `last_operation`.

If `last_operation` references a checkpoint/manifest needed to determine the current Implementation boundary, read that exact referenced artifact rather than copying values from a prior chat.

A physically IDLE mutation lock does not by itself authorize a second Implementation school. Preserve the currently serialized school/lifecycle ownership until the existing Implementation is COMPLETE or the owner and durable state establish a safe handoff.

### C. Recover the portfolio inventory

Reconcile the owner's bootstrap hints against durable evidence.

For the current serialized Implementation school, preserve:

- school key;
- current phase/boundary;
- exact branch and commit;
- latest authoritative checkpoint and fresh-verification state;
- current blocker, if any;
- whether Owner Gate 1 or Owner Gate 2 is pending;
- next permitted lifecycle boundary.

For Research lanes, preserve only status that can be supported by their authoritative durable checkpoints/artifacts. Do not infer `RESEARCH_FROZEN` from a branch name alone.

For already completed/live schools, do not re-verify every historical checkpoint merely because the Control Center chat changed. Inspect them only when a current governance question requires it.

### D. Reconcile recent owner context

The owner may provide:

- Implementation lane in progress;
- Research-frozen schools;
- Research-in-progress schools;
- the last predecessor Control Center message;
- an active lane escalation;
- a recent owner decision.

Use those items to locate relevant durable state quickly.

If the supplied context conflicts materially with current durable state, state the discrepancy and use durable authority.

If the supplied context is merely older than current durable state, report the advancement without treating it as an error.

### E. Report the baseline

The initial response should be concise and should state:

- exact protected-main SHA;
- exact global-control status;
- whether a mutation lock or recovery condition exists;
- which school currently owns serialized Implementation authority;
- current Research / Research Freeze inventory supported by available durable evidence;
- any actual Control Center governance problem;
- next meaningful boundary;
- exact owner action, if any.

If no genuine Control Center issue exists, explicitly say the Control Center is recovered, ready, and requires no owner action.

### F. Routine school-lane tooling PRs are not Control Center work

The Control Center is an exception/governance lane, not a mandatory merge desk for every permanent-tool repair.

Once the owner has authorized a school Research stage or Implementation phase, a generic tooling-only repair required to complete that same stage/phase may be developed, validated, and merged from the school lane under the delegation rule in `AGENTS.md`. A ready exact-head tooling PR is **not** by itself a Control Center escalation.

That delegation is **phase/family-persistent, not one-PR-only**. If a second manifestation in the same generic defect family could not be mechanically observed until the first repair or a required deterministic state transition completed, the school lane may perform the dependent follow-on repair and exact-head merge under the same stage/phase authority. The lane must document the dependency, add regression coverage for the newly reachable topology, and rerun the full permanent coordinator. A repeated unchanged failure or an expanding/unclear defect family should stop at a durable same-phase checkpoint, but does not require Control Center review unless authority, shared/global basketball state, mutation scope, serialized ownership, or recovery safety actually changes.

Likewise, `recovery_required=true` is not automatically Control Center work. When an accepted request is read-only or permanent recovery proves no tracked target publication (`NOT_ATTEMPTED` / `PREPARED_NOT_PUBLISHED`), the school lane should execute exact evidence-first recovery/abandonment, return control to `IDLE`, correct the mechanical request defect, and resume the same authorized phase with a new request ID. Escalate recovery only for ambiguous/diverged mutation state, materially changed authority, or a recovery action that itself needs new historical/shared mutation permission.

The school lane may carry that repair through merge when all of the following remain true:

- the diff is confined to generic tooling, tests, workflows, and documentation;
- no school package, canonical-game data, generated public data, shared/global basketball registry, owner-gate record, or publication state is changed;
- the exact failure topology has regression coverage;
- required exact-head CI and any applicable target-school candidate/runtime rehearsal pass;
- protected `main` and the exact PR head are reauthenticated immediately before merge;
- any intervening main advance is either incorporated and fully revalidated or classified as a material authority conflict and stopped;
- post-merge protected main and merge parents are authenticated, followed by a rerun of the permanent school-stage entrypoint.

Return to the Control Center only when the proposed repair changes historical/shared authority, mutates shared/global or already-published basketball state, changes repository policy/governance or mutation scope, creates a competing serialized Implementation claim, or enters an unsafe/ambiguous recovery state.

For Research in particular, the intended owner interaction is **stage result -> owner `Proceed` -> next stage**. Control Center round trips between deterministic technical steps inside that stage are a process defect.

The same principle applies when a school Implementation phase was temporarily interrupted by a generic tooling repair. A repair authorization may forbid executing the later live school mutation *inside the repair unit* without turning that later mutation into permanent Control Center work. After the repair merges and the school revalidates against refreshed protected main, return to the ordinary lifecycle boundary. If current policy says the next mutation is normal target-school Phase 0 authority, the owner authorizes it with ordinary `Proceed` in that school lane.

Likewise, a school-specific owner-authority registry entry that merely serializes an **already explicit owner decision** for that target school's Research closeout is not, by itself, Control Center work. Under the `AGENTS.md` school-scoped authority delegation, the Research lane may add the exact hash-bound target-school case, merge it after exact-head validation, refresh protected main, and run the permanent closeout. Escalate only if the registry change affects another school, changes registry schema/policy, alters shared/global basketball truth, or requires a new owner judgment.

## 4. Repository-owned recovery command

When a runnable repository checkout is available, use:

`python tools/control_center_status.py`

or:

`python tools/control_center_status.py --json`

This command is deliberately read-only. It may inspect Git refs and cached control state, but it does not mutate tracked files, branches, control state, basketball data, or protected main.

Its branch listings are **locators only**. In particular:

- a `research/*` branch does not prove a Research stage or Research Freeze;
- a `data/*-onboarding` branch does not by itself prove which lifecycle phase is authoritative;
- an IDLE global control state does not grant a new school the serialized lane.

If the exact remote control-state object is not present in the local Git object database, the command will report that limitation rather than fetching or inventing state. A connector-enabled Control Center should then read the exact control branch directly through GitHub.

## 5. Connector-first recovery when no checkout exists

A fresh ChatGPT Control Center does not require the owner's Codespace merely to recover governance state.

Using the authenticated GitHub connection, it should:

1. read current protected `main` and record its exact SHA;
2. read `AGENTS.md` at that authority;
3. read this succession protocol and applicable controlling documents;
4. authenticate `control/remote-implementation`;
5. read its exact `.remote-implementation/control-state.json`;
6. inspect the exact last-operation checkpoint when needed;
7. inspect relevant school branch/PR/checkpoint state only as required to reconcile the owner bootstrap;
8. stop after one bounded recovery pass unless a genuine governance problem is found.

Do not use ordinary public web search to replace private/durable repository state when the GitHub connection can read it directly.

## 6. Minimal owner bootstrap

The owner should be able to start a replacement Control Center with only:

```text
NEW CONTROL CENTER NEEDED

Implementation lane in progress:
<school or NONE>

Research frozen:
<schools or NONE>

Research in progress:
<schools or NONE>

Urgent/recent context:
<paste the last important Control Center/lane message, an owner decision, or leave blank>

Recover authoritative state from the repository, assume the permanent Control Center role, and perform the repository-defined bounded read-only succession recovery.
```

The lists above are intentionally short. They are not expected to encode exact SHAs, checkpoint hashes, or every completed school.

## 7. Recommended ChatGPT Project bootstrap

The ChatGPT Project should contain only stable routing information, not changing school status.

Recommended Project instruction:

```text
CONTROL CENTER SUCCESSION ROUTING

When the owner says "New Control Center needed", "successor Control Center", or otherwise identifies the conversation as the College Basketball History Control Center, this refers to:

https://github.com/pollackelliott/college-basketball-history

Assume the repository-wide Control Center governance role.

Before relying on conversational state, inspect current protected main, read current AGENTS.md, and follow the repository-defined Control Center succession procedure.

Owner-supplied school statuses and pasted predecessor messages are recovery locators, not durable authority. Repository/Git/GitHub state and authoritative checkpoint artifacts control.

Do not initiate Research, Implementation, maintenance, owner gates, or repository mutation merely because succession occurred. Begin with one bounded read-only governance recovery.
```

Do **not** place current school names, current SHAs, current request IDs, or current stage status in Project instructions. Those facts change and must be recovered from durable state.

## 8. Outgoing Control Center discipline

An outgoing Control Center should not attempt to serialize its entire conversation.

Before context exhaustion, it should ensure that:

- completed repository operations are durable in Git/GitHub;
- active Implementation work has an exact durable checkpoint;
- owner approvals are preserved in their normal repository-defined authority chain;
- genuinely exceptional unresolved governance information is summarized compactly;
- the owner can provide that compact summary in the `Urgent/recent context` field.

Routine status should be recoverable. The handoff should contain only facts that cannot yet be derived cleanly from durable state.

## 9. No competing PROJECT STATUS database

This protocol does not create a second manually maintained project-status ledger.

The Control Center maintains an operational inventory by reconciling existing durable authorities:

- protected `main`;
- the global remote Implementation control;
- school Research checkpoints and immutable Freeze artifacts;
- Implementation branches/checkpoints;
- PRs, merge evidence, and Production proof;
- explicit owner decisions.

If future repository tooling can derive more of that inventory mechanically, extend the read-only recovery command rather than introducing a manually synchronized status file.

## 10. Safe stopping rule

Succession itself is complete when the new Control Center can answer:

- What is current protected main?
- Is global control healthy, active, blocked, or in recovery?
- Which school, if any, owns serialized Implementation authority?
- Which supplied Research statuses can be confirmed from durable evidence?
- Is any real Control Center decision pending?
- What is the next meaningful owner boundary?

If those questions are answered and no governance issue is pending, stop recovery work and remain on standby.
