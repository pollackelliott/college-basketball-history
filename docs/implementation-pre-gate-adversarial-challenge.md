# Implementation Pre-Gate Adversarial Challenge

- **Status:** Required Implementation Stage 2 challenge before Owner Gate 1
- **Purpose:** Move deterministic reconciliation/publication failures earlier so the owner receives one mature historical decision packet instead of a serial repair loop.

## Principle

Stage 2 is not complete merely because preflight produced a decision list. Before `OWNER GATE 1 READY`, the Implementation lane must challenge the *predicted post-reconciliation result* as if the proposed recommendations had already been applied.

This is a pre-Gate challenge, not a new owner gate. It must not invent historical facts or replace the independent disposable Stage 3 rehearsal of the **owner-approved** review.

The Stage 2 standard is **research to recommendation, not necessarily to resolution**. Once a genuine historical conflict has been investigated enough to eliminate mechanical explanations, characterize the material competing evidence, and support a responsible recommendation, residual uncertainty belongs in the Owner Reconciliation Packet. Do not prolong Stage 2 merely to make the owner unnecessary.

Before researching or escalating a recurring venue-identity/locality question, apply `docs/recurring-venue-identity-conventions.md`. Stable project conventions such as Madison Square Garden physical-building splits and Paradise-vs-Las-Vegas venue geography should be reused mechanically rather than re-litigated for each school unless game-specific evidence creates a genuine contradiction.

### Comprehensive deterministic sweep before serial repair

Before beginning a serial repair loop, perform one comprehensive deterministic candidate sweep across the staged package and predicted integrated state using the current repository tooling and evidence already available to Implementation. Inventory together, where presently detectable:

- package/reference normalization drift;
- current-D1 key or display-identity drift;
- stale source-normalized values against the current authorized source set;
- site-research metadata that is inconsistent with already-resolved site/venue state;
- reciprocal/canonical count mismatches or assertion-closure anomalies;
- predicted opponent-display collisions;
- the deterministic publication/site-completeness defects covered below.

Exercise the permanent repository detection surfaces that already own these checks before adding bespoke diagnostics; do not treat a category as challenged merely because the lane reasoned about it without running the available non-destructive builder/gate/check that can expose it.

Repair that bounded inventory as a coherent population where safe, then regenerate authoritative preflight/challenge state. Do not intentionally rely on successive full simulations to discover deterministic defects one at a time.

This is an execution-order rule, not a new gate and not authority for speculative research. Integrated-state issues that cannot safely be known until a simulation or reciprocal reconciliation may still emerge iteratively; diagnose those normally rather than forcing unsupported early conclusions.

## Required challenge

### 1. Conditional discrepancy applicability

Use the repository's actual onboarding/reconciliation logic to determine which conditional discrepancies would be selected by the proposed canonical identities. Do not infer applicability from an ad-hoc field or from the raw count of conditional rows.

Before Gate 1, report the selected/applicable conditional count and include every owner-relevant selected conditional in the consolidated packet.

### 2. Site/H-A-N `KEEP_CANONICAL` challenge

Treat reciprocal existence as evidence of game identity, not automatically as proof that canonical site truth is correct.

For every proposed `KEEP_CANONICAL` disposition involving `site_type`, venue, or location, compare the target source, agreeing/conflicting reciprocal assertions, and the predicted canonical publication result. A recommendation that would discard stronger supported H/A/N, venue, or locality evidence must be corrected before Gate 1 or presented as an explicit owner decision.

### 3. Predicted post-reconciliation site completeness

Before Gate 1, simulate or otherwise deterministically inspect the site shape that would result from the proposed recommendations. Run the same substantive invariants enforced by `tools/implementation_site_gate.py` wherever the current tooling permits without mutating tracked canonical state.

At minimum challenge:

- target HOME venue/location completeness and approved researched-unresolved exceptions;
- UNKNOWN H/A/N;
- NCAA site completeness;
- neutral/postseason research accounting;
- target-source site/venue/location information loss;
- safe reciprocal site/venue/location evidence left unpropagated;
- stale venue-registry fallback or canonical locality that would overwrite stronger supported source evidence.

Any deterministic fingerprint-changing correction discovered here belongs before Gate 1.

### 4. Project-stable opponent display identity

Before Gate 1, compare every staged normalized opponent identity/display against current global program/reference identities and already-published reciprocal usage. Historical display variants must not survive merely because the opponent key is correct when current project state already establishes the stable display identity.

Resolve deterministic display normalization before Gate 1. Stop only for a genuine identity ambiguity.

### 5. Implausible normalized-value challenge

Scan staged game-level normalized values for technically valid but historically implausible outliers that ordinary schema validation may accept. This is a challenge, not authority to guess a replacement.

At minimum, overtime counts must be challenged when they exceed a conservative plausibility threshold. A value such as `69` must never reach Owner Gate 1 as an accepted ordinary integer merely because the schema permits nonnegative integers. Recover the supported value from source evidence or present the affected row as unresolved/owner-relevant if history is genuinely ambiguous.

### 6. Exact-recommendation disposable rehearsal

Before `OWNER GATE 1 READY`, construct the exact recommendation map the lane proposes to present to the owner and run it through the permanent full disposable rehearsal surface. The rehearsal must exercise the proposed identities and dispositions through actual conditional applicability, reconciliation, deterministic publication/site generation, implementation site completeness, target no-op behavior, and the current automated gate/test suite.

This is a **proposal rehearsal**, not owner approval and not cryptographic sealing. It must not write owner-approval semantics into tracked state.

Classify rehearsal findings as follows:

- **mechanical/deterministic failure:** repair it before Gate 1 and rerun the proposal rehearsal;
- **genuine historical conflict:** perform bounded investigation sufficient for a supported recommendation, then include the conflict in Gate 1 with the competing evidence and residual uncertainty;
- **tool/lifecycle misuse or wrapper defect:** correct the execution path rather than treating the false failure as basketball evidence.

When conflicting institutional records share a strong fingerprint—such as identical date and score but different opponent identity—present that fingerprint as competing evidence. Do not assume either the incoming school or existing canonical source is authoritative merely because one is newer, already published, or locally convenient.

### 7. Gate-1 packet maturity

Do not declare `OWNER GATE 1 READY` until:

- the actual applicable conditional universe is known;
- deterministic display/normalization defects are repaired;
- proposed site/H-A-N recommendations have survived the publication-shape challenge;
- the predicted post-reconciliation site-completeness result has no unexplained blocker;
- every material historical conflict has been investigated to a responsible recommendation or explicitly identified as requiring a narrow owner-directed research return;
- the exact proposed recommendation map has passed the full disposable proposal rehearsal, except that genuine historical choices surfaced by that rehearsal are represented explicitly in the packet rather than silently resolved;
- all remaining items truly require historical owner judgment.

The intended normal path is:

`Stage 2 comprehensive challenge -> exact recommendation-map proposal rehearsal -> one Owner Reconciliation Packet / Gate 1 -> Stage 3 owner-approved rehearsal/seal/apply -> Preview`

A supplemental owner gate remains correct when genuinely new historical evidence or a changed substantive decision universe appears later. The goal is to eliminate avoidable supplemental gates caused by defects Stage 2 could have found deterministically.

## Relationship to Stage 3

This challenge does **not** weaken or replace `rehearse-review`. Stage 3 remains the independent disposable proof that the exact owner-approved review can ingest, reconcile, publish, validate, build, and test cleanly before sealing.

If Stage 3 still finds a technical defect, repair it generically and use carry-forward when the substantive owner decision universe is unchanged. Return to the owner only for genuinely new or changed historical judgment.
