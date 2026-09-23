# Implementation Gate 1 Authority Boundary

- **Status:** Controlling serialized-Implementation policy
- **Applies to:** every school after `RESEARCH_FROZEN` / `INTEGRATION_FROZEN` and before Owner Gate 1
- **Approved:** 2026-09-23 after the Stanford / Washington State Implementation retrospective
- **Purpose:** keep pre-Gate cleanup deterministic without allowing Implementation to become a second Research/adjudication pass

## 1. Governing principle

> **Pre-Gate Implementation may correct representation. It may investigate history and recommend corrections, but it may not adjudicate newly disputed historical meaning merely because the agent believes it has found the better answer.**

The objective of pre-Gate work is a **mature decision packet**, not the smallest possible decision packet.

A large Gate 1 universe is not a process failure. The collaborator should research and compress it into supported recommendations rather than rewrite frozen history until decisions disappear.

## 2. Historical meaning versus integration representation

After Research freezes, distinguish two different kinds of change.

### Integration representation — normally valid before Gate 1

These changes preserve an already-settled historical conclusion while reconciling it against current protected main or current project representation. Examples include:

- rebasing provisional Research-time venue IDs to existing/current global venue identities;
- allocating a new global numeric venue ID for a physical identity already settled by Research;
- applying an already-settled shared-reference proposal during current-main rebase;
- correcting stale current-program stable keys when the institutional identity itself is unchanged and current registry authority is unambiguous;
- current project display-name normalization;
- attaching an exact reciprocal/canonical assertion to the correct game when game identity is deterministic **without changing which disputed historical field should control**;
- technical/tooling repairs that do not choose between competing historical assertions.

### Historical meaning — Owner Gate 1 authority

These fields describe what happened in the historical game and may not be silently rewritten after `INTEGRATION_FROZEN` merely because Implementation finds new evidence:

- exact date / season placement;
- team or opponent score;
- winner / played result;
- overtime count;
- H/A/N / canonical site classification;
- physical venue or game geography when the correction changes the accepted historical conclusion rather than only a current-main identity/display mapping;
- game type;
- postseason round;
- game inclusion/identity when competing plausible historical interpretations remain;
- preserved literal source evidence.

When new evidence supports a correction to historical meaning, the normal path is:

```text
challenge -> understand -> recommend -> encode proposed patch -> rehearse -> Owner Gate 1
```

not:

```text
challenge -> understand -> mutate frozen source -> rerun preflight until discrepancy disappears
```

## 3. Integration Freeze semantic guard

`tools/stage_research_portfolio.py` records an ignored semantic snapshot of the staged `source-games.csv` inside:

```text
.onboarding/<school>/integration-freeze.json
```

The snapshot is taken **after** the authorized current-main representation rebase. That makes `INTEGRATION_FROZEN` the comparison baseline.

The guard covers substantive/evidentiary source-game fields, including date, scores, result, overtime, site type, venue/location, event/game type, postseason round, source opponent label, and raw source evidence.

Representation-only opponent key/display normalization is intentionally outside this semantic snapshot.

Authoritative preflight, pre-seal rehearsal, sealing, and sealed apply must fail if protected historical meaning has drifted from the Integration Freeze baseline before Gate 1 authorization.

For explicit inspection:

```bash
python tools/onboarding_hardening.py freeze-drift <school_key>
```

A semantic-drift failure is not permission to update the baseline. Restore the frozen fields and represent the proposed historical correction through Gate 1.

If a future deterministic historical normalization can truly be proven from already-frozen information alone, it must be implemented as a **specific permanent machine rule with tests**. Ad hoc editing plus an assertion that the change is "deterministic" does not bypass the guard.

## 4. Pre-Gate execution model

The normal path after Phase 0 is:

1. run authoritative preflight;
2. clear true blockers caused by current-main representation/reference incompatibility;
3. once a blocker-free preflight exists, perform one comprehensive deterministic representation/identity sweep;
4. make at most one coherent deterministic repair batch;
5. rerun authoritative preflight;
6. investigate every material remaining discrepancy enough to provide a recommendation;
7. encode any recommended historical corrections as Gate 1 review patches;
8. rehearse the complete proposed recommendation map;
9. present one consolidated Owner Gate 1 packet.

The first blocker-free preflight is a meaningful milestone. From that point forward, **decision-count reduction is not an optimization target**.

A second fingerprint-changing repair cycle is justified only by a newly discovered technical/current-main representation defect that could not reasonably have been included in the first deterministic sweep. Historical disagreement is not such a reason.

## 5. Gate 1 patch path

The review machinery already supports owner-authorized source and canonical patches.

The compact decision map may now include:

```json
{
  "source_patch_by_decision": {
    "DISCREPANCY-...": {
      "overtime_periods": "1"
    }
  },
  "canonical_patch_by_decision": {
    "DISCREPANCY-...": {
      "overtime_periods": "1"
    }
  },
  "notes_by_decision": {
    "DISCREPANCY-...": "Evidence basis / explanatory note."
  }
}
```

Use these fields when Implementation discovers a supported historical correction after freeze. Rehearsal proves the exact proposed outcome before owner approval without mutating the tracked frozen package.

The sealed transactional apply remains the authority that performs an approved source/canonical historical patch.

## 6. Owner interaction

Do not interrupt the owner merely because one difficult historical row appears before Gate 1.

Research the row, form a recommendation, and include it in the consolidated packet unless:

- repository policy explicitly requires an earlier owner decision;
- no safe technical continuation is possible without that decision; or
- the question changes the authorized history scope/fundamental implementation premise rather than an ordinary reconciliation item.

The Stanford reciprocal-only TCU case is evidence that an early owner question can be handled safely, but it is not the preferred default.

## 7. Generic tooling changes during a school lane

A school may expose a genuine generic modeling or validator gap.

A pre-Gate tooling repair is acceptable only when:

- the represented state is generally valid, not school-specific;
- the historical premise is already settled or is represented in Gate 1 rather than silently assumed;
- the implementation is narrow;
- regression tests cover both acceptance and rejection cases; and
- the repair does not create a bypass around the sealed-plan decision authority.

"Make this school pass" is not sufficient justification for a generic gate exception.

## 8. What this does not change

This policy does not weaken adversarial Implementation review.

The collaborator should still inspect current-main reciprocal/canonical evidence, identify source drift, research discrepancies, challenge identity matches, and discover likely historical corrections before Gate 1.

The change is **where authority lives**:

- discovery and recommendation belong to the collaborator;
- current-main representation reconciliation belongs to pre-Gate Implementation;
- disputed/new historical meaning belongs to Owner Gate 1;
- approved mutation belongs to sealed transactional apply.

The intended result is Stanford-like decision discipline without reproducing Stanford's avoidable terminal-wrapper friction, and without repeating Washington State's pre-Gate second-research-cycle behavior.
