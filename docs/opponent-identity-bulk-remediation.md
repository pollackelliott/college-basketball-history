# Bulk Opponent Identity Remediation

The first sealed opponent-identity transaction was intentionally optimized for a
reciprocal-duplicate batch: every affected stale canonical row represented the same
real game as a later canonical counterpart. A broader owner-reviewed cleanup has a
larger state space and must not force valid games into that assumption.

`tools/opponent_identity_bulk_transaction.py` is the guarded transaction boundary for
that broader case.

## Supported canonical outcomes

Every canonical row touched by the global key map must end in exactly one reviewed
state:

1. **In-place remap** — the game is already unique; only the stale participant key is
   normalized. The permanent canonical game ID survives.
2. **Duplicate absorption** — the key correction exposes two canonical rows for one
   real game. The affected stale-key row survives by default when there is one stale
   row plus one authoritative counterpart; assertions and discrepancy references from
   the absorbed row are redirected.
3. **Explicit reconciliation** — a same-date score/overtime/other populated-field
   conflict, or a non-standard counterpart pairing, requires a reviewed resolution.
4. **Retain distinct** — two genuinely separate games may be indistinguishable at the
   available historical precision. Unknown-date collision candidates therefore block
   by default and survive only through an explicit `retain_distinct` ruling.

The 1913-14 Texas A&M / Sam Houston case is the motivating example for state 4: the
source ledger contains separate home and away games, but exact dates and scores are
unavailable. A key correction must preserve both games.

## Manifest

The bulk manifest is CSV with these fields:

```text
source_program_key
source_opponent_label
from_program_key
to_program_key
to_program_name
target_current_d1
decision
evidence_basis
evidence_url
```

Supported decisions:

- `MERGE_TO_PROGRAM` — target must exist in the global program registry and be current
  D1; `target_current_d1` must be `Yes`.
- `REKEY_DISTINCT_NON_D1` — owner/evidence-backed normalization of one non-current-D1
  institutional identity; `target_current_d1` must be `No`. This exists so historical
  cleanup never fabricates current-D1 status merely to reuse the D1 alias machinery.

For ordinary rows, each manifest entry is verified against one exact `opponents.csv`
source label and its matching `source-games.csv` population. For historical packages
whose opponent index aggregates multiple literal spellings, set `source_opponent_label`
to `__ALL_KEY_USAGES__`; that explicitly scopes the row to every package row and every
source-game row for the old key within that source program. The planned opponent-label
set and source-game IDs are sealed before apply. Literal source opponent labels and raw
source text are never rewritten.

## Resolution document

The JSON document uses `schema_version: 2` and contains:

- `resolutions`: the same explicit survivor/absorbed reconciliation records accepted by
  `opponent_identity_transaction.py`;
- `retain_distinct`: explicit groups of canonical IDs that must remain separate despite
  an unknown-date mapped-signature collision, with substantive resolution basis.

Exact-date core matches with exactly one stale row and one authoritative counterpart
may be absorbed automatically only when all populated canonical fields merge without
conflict. Any material conflict blocks unless explicitly resolved.

Unknown-date collisions never auto-dedupe.

## Seal and apply

Generate the plan twice from the exact protected-main base and require byte-identical
`plan_sha256` values before any apply:

```bash
python tools/opponent_identity_bulk_transaction.py plan decisions.csv resolutions.json \
  --output /tmp/bulk-opponent-plan.json
```

Apply requires the exact seal and explicit `--apply`:

```bash
python tools/opponent_identity_bulk_transaction.py apply decisions.csv resolutions.json \
  --expected-plan-sha256 <sha256> --apply
```

The transaction rolls back every touched file if validation fails. After apply, no old
mapped key may remain in canonical participants or assertion normalization; absorbed
canonical IDs must be gone; explicitly retained-distinct IDs must all survive.

## Release boundary

Bulk opponent remediation remains serialized global mutation. The production branch
must start from then-current protected `main`, regenerate the sealed plan, rebuild
site data deterministically, pass repository validation and the full test suite, and
stop at the exact-head Preview for owner Gate 2 approval before merge.
