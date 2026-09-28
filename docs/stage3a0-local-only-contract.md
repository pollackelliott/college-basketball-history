# Stage 3A-0 Checkpoint-Only Census Contract

- **Status:** Controlling Research-lane execution policy
- **Applies to:** every Stage 3A-0 census / partition pass
- **Simplified:** 2026-09-28 after live Research execution failures
- **Purpose:** keep Stage 3A-0 an introductory mechanical census rather than a repository-transport or historical-research problem

## 1. Governing rule

> **Stage 3A-0 is checkpoint-only, mechanical, deterministic, and bounded.**

Its historical job is intentionally small: validate the structured Stage 2 Research state, partition the accepted game universe, derive the H/A/N census, and emit the exact downstream queues.

Stage 3A-0 performs:

- zero public-web research;
- zero external source discovery;
- zero opponent-package research;
- zero venue archaeology;
- zero historical adjudication;
- zero required canonical/project-evidence lookup.

Project-evidence reuse belongs to the later substage that actually needs it:

- Stage 3A-1 for H/A/N reconciliation;
- Stage 3A-2 for HOME chronology/exceptions;
- Stage 3A-3 Tier 1 for neutral accepted-project-evidence reuse.

## 2. Required input

The authoritative input is either:

- the durable Stage 2 checkpoint ZIP; or
- the structured Stage 2 game ledger directly.

For checkpoints created under current policy, Stage 2 completion must include a full
game-level `structured-stage2-ledger.csv`. That ledger is the accepted Stage 1 game
universe with Stage 2 opponent identity written through to every row. It must preserve
stable row IDs, season, game type, literal/raw source fields, and any already-established
H/A/N value.

If Stage 2 has not established standardized H/A/N for a row, write
`site_type=UNKNOWN`. Stage 2 and Stage 3A-0 must **never infer H/A/N from
source_site_token** merely to populate the structured ledger.

### Legacy Stage 2 compatibility

Some accepted pre-hardening Stage 2 checkpoints completed opponent identity at the
label/family level but did not serialize those conclusions back into a full per-game
Stage 2 ledger.

Stage 3A-0 may mechanically materialize a legacy checkpoint only when the ZIP itself
contains both:

1. one full game-level accepted ledger with stable row IDs, season, game type, and source
   opponent label; and
2. one complete label-level opponent mapping that deterministically supplies one opponent
   key for every source opponent label used by that game ledger.

The permanent command owns that mechanical join. It must require complete label coverage,
reject conflicting complete mappings, preserve the accepted game rows and raw site tokens,
write the resolved opponent key onto each row, and use `site_type=UNKNOWN` whenever the
legacy ledger lacks an already-standardized H/A/N value.

This compatibility path is not Stage 2 research, is not permission to reconstruct missing
state from prose, and must not parse raw source-site notation into H/A/N.

If the checkpoint lacks either a full game-level ledger or complete deterministic opponent
mapping, Stage 3A-0 remains entry-not-ready and stops.

Required structured fields after direct entry or mechanical legacy materialization are:

- stable research/source row ID;
- season;
- resolved opponent key;
- H/A/N/site classification, including explicit `UNKNOWN`;
- game type.

Explicit `UNKNOWN` H/A/N is a valid Stage 3A-0 value and belongs in the UNKNOWN queue.
A present but unrecognized standardized site value is an input defect.

A pre-hardening checkpoint that lacks required `game_type` may use only the documented
narrow compatibility migration plus declared-intent validator. Do not broaden that repair
into historical research.

## 3. Permanent execution

After the owner authorizes Stage 3A-0 and current protected `main` is confirmed, run:

```bash
python tools/research_stage3a0.py <school_key> <stage2-checkpoint.zip> --main-sha <protected-main-sha>
```

A structured Stage 2 ledger may be supplied instead of the ZIP.

The permanent tool owns:

1. checkpoint/ledger entry;
2. structured readiness;
3. exact row count;
4. regular-season/postseason partition;
5. HOME / OPPONENT_HOME / NEUTRAL / UNKNOWN census;
6. modern versus historical regular-season NEUTRAL split;
7. exact downstream queue emission;
8. durable status/manifest generation.

The protected-main SHA is recorded for policy/version traceability. Stage 3A-0 does **not** require repository basketball data to compute its census.

The deprecated `--canonical` argument may remain accepted for backward-compatible old commands, but Stage 3A-0 ignores it.

## 4. No-checkout execution

A persistent checkout is not required.

When an exact-state checkout is already available, the command may run there.

Otherwise use the authenticated GitHub connector to fetch the exact `tools/research_stage3a0.py` file at the confirmed full protected-main SHA, write those exact bytes to temporary storage, and execute that file against the attached checkpoint/ledger with explicit `--main-sha`.

This is executable transport of the repository-owned permanent tool, not source discovery and not permission to reinterpret or rewrite the algorithm conversationally.

**Do not use codeload, clone the repository, download a full repository archive, or ask the owner to open Codespaces merely to run Stage 3A-0.**

Report `STAGE_3A0_EXECUTION_ENVIRONMENT_UNAVAILABLE` only when the lane cannot access one of:

- the authoritative checkpoint/ledger;
- the exact permanent tool bytes at the confirmed protected-main SHA;
- temporary Python/filesystem execution sufficient to run the tool.

That sentinel should be exceptional, not a normal Research boundary.

## 5. Required durable outputs

A successful Stage 3A-0 must durably preserve:

- exact input artifact/member and hashes;
- exact ledger row count;
- exact regular-season count;
- exact postseason Stage 3B handoff count and queue;
- HOME queue;
- OPPONENT_HOME queue;
- UNKNOWN H/A/N queue;
- full NEUTRAL queue;
- modern NEUTRAL queue;
- historical NEUTRAL queue;
- H/A/N census derived from rows;
- `stage3a0-summary.json`;
- `stage3a0-status.json`;
- manifest/hashes;
- explicit `external_historical_research_used: false`.

No target-canonical match, unmatched-candidate, or contradiction artifact is required for Stage 3A-0.

## 6. Stop behavior

If entry/readiness fails, read `stage3a0-status.json`, perform only the bounded prior-stage/input remediation it names, and stop. Do not research around the gate.

If execution succeeds, stop at:

```text
STAGE 3A-0: COMPLETE
Next bounded assignment: Stage 3A-1 — H/A/N completion
STOPPING AT THE REQUIRED STAGE 3A SUBSTAGE BOUNDARY.
```

A large UNKNOWN, HOME, or NEUTRAL queue is a valid Stage 3A-0 result. Stage 3A-0 succeeds by producing correct populations, not by minimizing residual counts.

## 7. Recovery rule

When recovering Stage 3A-0:

- verify the controlling Stage 2 checkpoint;
- preserve its immutable Research baseline;
- rerun the permanent checkpoint-only operation if no valid Stage 3A-0 completion artifact exists;
- never reconstruct prior scratch work from prose;
- never open historical sources merely because the mechanical queue is large.

The intended owner experience is:

> **Stage 2 checkpoint -> Proceed -> Stage 3A-0 completes mechanically -> concise census -> Proceed to Stage 3A-1**

