# Opponent Identity Remediation

Opponent identity is a separate integrity dimension from site/location completeness.
The remediation goal is not to make every historical opponent look like a modern D1
program. It is to ensure that one institutional basketball program has one canonical
program identity while genuinely distinct institutions, clubs, military teams, high
schools, and other historical opponents remain distinct.

## Safety principles

1. String similarity is never sufficient institutional-identity evidence.
2. Preserve literal source opponent labels and raw source text.
3. Historical official names become aliases of one program only when authoritative
   institutional lineage supports continuity.
4. A current-D1 flag correction is not automatically a program-key merge.
5. One real game remains one canonical game. A key merge that exposes duplicate
   canonical rows must stop for explicit game reconciliation before apply.
6. Opponent remediation is serialized repository mutation and shares the integration
   lock with school Implementation and site/location remediation.
7. Build and review a deterministic plan before any basketball-data write.

## Global program-name registry

`data/reference/program-names.csv` stores verified alternate names for identities in
`data/reference/programs.csv`.

Columns:

- `program_key`: authoritative program identity.
- `alias_name`: historical/alternate spelling or name.
- `alias_type`: one of `OFFICIAL_HISTORICAL_NAME`, `ATHLETIC_BRAND`,
  `SOURCE_ABBREVIATION`, or `PROJECT_DISPLAY_ALIAS`.
- `effective_start_season` / `effective_end_season`: optional era bounds when needed.
- `verification_status`: currently must be `VERIFIED` for a row to be registry
  authority.
- `evidence_basis`: concise explanation of the institutional-lineage evidence.
- `evidence_url`: supporting source URL where available.
- `notes`: optional nuance.

The same normalized alias may point to different programs only when complete,
non-overlapping effective-era ranges make the identities unambiguous. Otherwise the
registry validator blocks it.

## Gate 1 owner sanity scan

For each new school, Implementation should run:

```bash
python tools/opponent_identity_remediation.py sanity <school_key>
```

The output is a compact list of opponent rows not already represented as a clean
current-D1 identity, enriched with published-opponent census flags.

This is an owner expertise backstop, not another approval gate. Add it to the normal
Owner Gate 1 packet. The owner only flags suspicious names; genuine historical non-D1
opponents do not require row-by-row approval.

Research remains responsible for opponent normalization before `RESEARCH_FROZEN`.

## Evidence-backed decision file

The planner consumes a CSV with these fields:

```text
source_program_key
source_opponent_label
from_program_key
to_program_key
decision
evidence_basis
evidence_url
```

Supported `decision` values:

- `MERGE_TO_PROGRAM`: the stored key is a stale/alternate identity for the target
  registry program.
- `MARK_CURRENT_D1`: the key is already correct; only current-D1 treatment is stale.
- `KEEP_DISTINCT`: evidence establishes that the proposed merge is wrong.
- `HOLD`: uncertainty remains; preserve the separate identity pending stronger
  evidence.

The planner assigns a stable `OID-...` decision ID from the substantive identity
inputs. Evidence wording may improve without changing that ID.

## Read-only remediation plan

Run:

```bash
python tools/opponent_identity_remediation.py plan /path/to/decisions.csv \
  --output /tmp/opponent-plan.json
```

The planner validates:

- target program registry identity;
- exact school `opponents.csv` row;
- exact school `source-games.csv` row count;
- global consistency of every stale-key -> target-key mapping;
- alias-registry validity;
- canonical games touched by each key merge;
- source assertions touched by each key merge;
- self-game impossibilities after replacement;
- exact-date canonical collision candidates;
- unknown-date collision review candidates;
- fingerprints of controlling repository files and the decision file.

The JSON plan is deterministic and ends with `plan_sha256`.

An exact-date canonical collision is a blocker, not an instruction to delete a row.
It means the identity repair has exposed two canonical rows that may represent the
same real game and must be reconciled under the project's one-real-game rule.

## Apply boundary

The current tool is intentionally read-only. Do not manually edit canonical or
evidence CSVs from a plan.

A transactional apply implementation must be added and tested before the first
published-opponent remediation batch. It must consume a reviewed/sealed plan,
revalidate fingerprints, update every affected source/reference/generated layer
consistently, reconcile duplicate canonical games without changing permanent surviving
IDs casually, run repository validation/site build/tests, and produce exact Preview
and Production proof.

## Legacy cleanup exit criteria

Before resuming the normal school Implementation queue after the initial opponent
cleanup window:

- published opponent census `P0 = 0`;
- published opponent census `P1 = 0`, except explicitly researched/reclassified holds;
- no evidence-confirmed current program remains displayed as a separate false non-D1
  identity;
- protected false-friend identities remain distinct;
- no published-vs-published series remains split solely by a stale opponent key;
- literal source labels remain preserved;
- full repository tests and deterministic site generation pass;
- exact Preview and Production verification pass for the remediation PR.
