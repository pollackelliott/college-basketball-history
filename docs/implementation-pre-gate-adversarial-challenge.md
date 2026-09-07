# Implementation Pre-Gate Adversarial Challenge

- **Status:** Required Implementation Stage 2 challenge before Owner Gate 1
- **Purpose:** Move deterministic reconciliation/publication failures earlier so the owner receives one mature historical decision packet instead of a serial repair loop.

## Principle

Stage 2 is not complete merely because preflight produced a decision list. Before `OWNER GATE 1 READY`, the Implementation lane must challenge the *predicted post-reconciliation result* as if the proposed recommendations had already been applied.

This is a pre-Gate challenge, not a new owner gate. It must not invent historical facts or replace the disposable Stage 3 rehearsal.

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

### 6. Gate-1 packet maturity

Do not declare `OWNER GATE 1 READY` until:

- the actual applicable conditional universe is known;
- deterministic display/normalization defects are repaired;
- proposed site/H-A-N recommendations have survived the publication-shape challenge;
- the predicted post-reconciliation site-completeness result has no unexplained blocker;
- all remaining items truly require historical owner judgment.

The intended normal path is:

`Stage 2 comprehensive challenge -> one Owner Gate 1 -> Stage 3 rehearsal/seal/apply -> Preview`

A supplemental owner gate remains correct when genuinely new historical evidence or a changed substantive decision universe appears later. The goal is to eliminate avoidable supplemental gates caused by defects Stage 2 could have found deterministically.

## Relationship to Stage 3

This challenge does **not** weaken or replace `rehearse-review`. Stage 3 remains the independent disposable proof that the exact owner-approved review can ingest, reconcile, publish, validate, build, and test cleanly before sealing.

If Stage 3 still finds a technical defect, repair it generically and use carry-forward when the substantive owner decision universe is unchanged. Return to the owner only for genuinely new or changed historical judgment.
