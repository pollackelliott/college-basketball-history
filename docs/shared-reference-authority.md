# Shared Reference Authority Boundary

- **Status:** Controlling policy for shared/global reference mutation discovered during school Research
- **Applies to:** independent Research lanes, serialized Implementation lanes, and dedicated shared-reference maintenance work
- **Purpose:** preserve parallel Research speed while keeping authoritative global repository state serialized, auditable, and protected from unrelated school-lane mutations

## 1. Governing principle

> **Research establishes historical truth; Integration establishes global repository identity.**

Independent Research lanes may discover, define, and fully research shared identities or corrections, including historical conferences, programs, program aliases, venues, venue aliases, and comparable global reference facts.

They must not turn those findings directly into incidental mutations of protected `main` shared-reference registries.

Research owns the historical conclusion. Serialized Implementation, or an explicitly authorized dedicated maintenance workflow, owns the authoritative global repository mutation.

## 2. Research-lane authority

A school Research lane may:

- mutate its own research-local/checkpoint/frozen artifacts as required;
- determine that current protected `main` lacks a shared identity needed by the target school;
- research that identity to the same evidentiary standard as any other historical conclusion;
- preserve the proposed stable key/name/type/status, aliases, dates/eras, geography where applicable, evidence basis, and the target school's usage;
- carry the result into `RESEARCH_FROZEN` as a settled shared-reference proposal.

A school Research lane must not:

- directly commit to protected `main`;
- directly mutate protected-main shared registries as an incidental side effect of school Research;
- treat broad permission to mutate repository or research state as permission to change authoritative shared/global state;
- create competing global identities merely because another concurrent lane has not yet integrated its own proposal.

Research-time numeric/global IDs remain provisional where repository policy already treats them as provisional.

## 3. Resolved history versus pending global registration

A shared identity is not historically unresolved merely because its authoritative global registry row has intentionally been deferred.

Research may freeze a conclusion in the form:

```text
Historical identity: RESOLVED
Global registration: PENDING_CURRENT_MAIN_REBASE
```

The frozen handoff must contain enough evidence and identity detail for Implementation to reconcile the proposal mechanically without redoing settled historical research.

Implementation must not reopen an accepted historical conclusion merely because the global registration is still pending. Reopen only when current-main evidence exposes a genuine contradiction or identity conflict.

## 4. Normal Integration path

Implementation Stage 1 current-main rebase is the normal authority point for pending shared-reference proposals.

For each proposal, Implementation determines whether the identity is:

- already present and reusable;
- still genuinely new;
- superseded by a better current-main identity;
- in conflict with an intervening identity; or
- ambiguous enough to require a STOP and narrow reconciliation.

If the identity is already present, reuse it. If it is still new and mechanically safe, register it through the controlled Implementation path. If current main conflicts materially with the frozen proposal, stop for the minimum necessary reconciliation rather than silently creating another global truth.

This is analogous to provisional Research-time venue identity: Research establishes physical/historical meaning; Integration establishes the final authoritative repository identity against current `main`.

## 5. Early shared-reference registration exception

Occasionally several active lanes may immediately benefit from a newly established shared identity before the discovering school reaches Implementation.

That is an explicit exception, not normal Research behavior.

The Research lane should surface the need to the Control Center. If early registration is genuinely useful, the Control Center may authorize a **dedicated shared-reference maintenance branch/PR**.

That maintenance change must be isolated from the school Research lane and must use a narrow validated diff whose declared purpose is the shared-reference mutation itself.

The school Research lane must not write directly to protected `main` to achieve the same result.

## 6. Intent-constrained diff validation

Repository validation is necessary but not sufficient for any shared-reference mutation.

Every shared-reference operation must also answer:

> **Did only the state we declared we intended to change actually change?**

For example, if the declared operation is:

```text
Register historical Border Conference
```

then unrelated changes to CAA, Indiana Collegiate, another conference, programs, venues, or other shared identities are a STOP even if CSV serialization succeeds.

For narrow additions/corrections, the expected diff should be correspondingly narrow. Prefer exact changed-file/row assertions when practical. Unexpected unrelated modifications require inspection before the change is accepted.

The required safety pair is therefore:

1. repository validation passes; and
2. the actual diff matches the declared mutation scope.

This principle applies to shared program identities, program-name aliases, conference identities, venue identities/aliases, and comparable global registries.

## 7. Concurrency model

The project intentionally permits multiple independent Research lanes while maintaining one serialized Implementation lane.

Therefore:

> **Parallel work owns school-local historical knowledge. Serialized work owns shared global state.**

A parallel Research lane must not unexpectedly change the global foundation beneath an unrelated Implementation lane.

Guarded Implementation startup must still validate current protected `main`; this policy reduces the number of independent actors capable of invalidating that state in the first place.

## 8. Research Freeze representation

No seventh required school-package file is introduced by this policy.

Shared-reference proposals should be preserved in the existing durable Research handoff/status/notes artifacts in a form that is explicit and mechanically actionable. At minimum record, as applicable:

- proposed stable key;
- display/canonical name;
- identity type/status;
- known historical aliases;
- effective dates/eras;
- geography;
- evidence basis/source;
- target-school usage;
- `Historical identity: RESOLVED`;
- `Global registration: PENDING_CURRENT_MAIN_REBASE`.

If repeated live use later proves that a dedicated machine-readable proposal artifact materially improves reliability, that may be considered separately. This policy does not create one now.

### Owner-maintained shared research datasets

A Control-Center-authorized dedicated maintenance PR may also register a reusable owner-maintained
research dataset whose purpose is to prevent repeated school-by-school research. Once merged, school
Research lanes may consume that dataset as read-only shared project evidence under its controlling
dataset-specific policy, but may not edit the shared dataset incidentally from a school lane.

`docs/conference-tournament-site-reference.md` is the first such dataset-specific authority.
Its incomplete or uncertain rows do not become assertions merely because the dataset is shared;
updates to that reference return through a dedicated maintenance/refresh PR with source-version
provenance and intent-constrained diff review.

## 9. What does not change

This boundary does not weaken Research. Research still fully resolves, to current policy standards:

- opponent identity;
- conference history;
- physical venue identity;
- H/A/N and site research;
- postseason classification/sites;
- NON_D1 classification and owner sanity scan;
- final adversarial self-challenge;
- complete historical evidence packaging.

It also does not add a new owner gate, Research stage, or Implementation stage.

The change is only the authority boundary for **authoritative shared/global repository mutation**.

## 10. Code-review and maintenance rule

Flag any workflow that allows an independent school Research lane to mutate protected-main shared registries directly or that treats general Research mutation permission as sufficient authority for such a write.

Flag any shared-reference maintenance/Integration change whose actual diff includes unrelated shared identities outside the declared scope.

Dedicated maintenance PRs remain valid when explicitly authorized and narrowly validated.
