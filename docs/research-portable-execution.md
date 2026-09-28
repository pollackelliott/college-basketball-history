# Portable Research Execution Contract

- **Status:** Controlling Research-lane execution policy
- **Applies to:** deterministic Research operations that need repository-owned executable/state
- **Purpose:** preserve mobile-first Research without forcing the owner to operate Codespaces

## Governing rule

A Research lane must not require an owner-managed Codespace merely because a deterministic repository-owned operation needs to run.

The normal owner experience remains:

`attach checkpoint -> Proceed -> bounded Research work -> durable checkpoint`

Use the smallest exact-state transport that the operation actually needs. Do not transport an entire repository when one exact permanent tool file is sufficient.

## Stage 3A-0: tool-only portable execution

Stage 3A-0 is checkpoint-only. It does not require canonical games, assertions, published opponent packages, registries, or another repository data surface.

After confirming the exact protected-main SHA:

1. if an exact-state runnable checkout already exists, run the permanent command there;
2. otherwise use the authenticated GitHub connector to fetch the exact `tools/research_stage3a0.py` file at that full SHA;
3. write those exact bytes to temporary storage;
4. run that file against the authoritative Stage 2 checkpoint/ledger with explicit `--main-sha`;
5. preserve the emitted Stage 3A-0 artifacts.

A repository archive is not required for Stage 3A-0.

The connector fetch is executable transport. Do not inspect the tool source to derive basketball conclusions, edit the fetched algorithm conversationally, or substitute a hand-reimplemented census.

Do not use codeload, clone the repository, search for alternate snapshots, or ask the owner to open Codespaces merely to run Stage 3A-0.

The Stage 3A-0 invariant is:

`same checkpoint + same permanent-tool bytes = same census/partition/queues`

The protected-main SHA remains recorded so the exact tool/policy version is auditable.

## Deterministic stages that genuinely require project state

Some later mechanical operations may legitimately require protected-main basketball/project files. Stage 3A-3 Tier 1 currently does.

For such an operation:

1. confirm the exact protected-main SHA;
2. use an already-runnable checkout at that exact state when available;
3. otherwise, if temporary filesystem, Python, and direct HTTPS download/extraction are available, fetch one disposable repository archive pinned to that exact SHA;
4. run the permanent repository command from the extracted snapshot, passing the exact protected-main SHA explicitly;
5. preserve the command outputs/checkpoint;
6. discard the temporary snapshot.

The authorized full-repository portable archive for a stateful operation remains:

`https://codeload.github.com/pollackelliott/college-basketball-history/zip/<exact-protected-main-sha>`

Use the full 40-character commit SHA. Never use `main`, `HEAD`, a tag, or another moving reference.

This archive path is **not** the Stage 3A-0 execution path.

## Stage 3A-3 Tier 1

Until its own architecture is separately reviewed, Stage 3A-3 Tier 1 continues to use the current permanent `tools/research_stage3a3_tier1.py` accepted-evidence pass and therefore requires protected-main project state.

When no exact-state checkout exists, the exact-SHA disposable snapshot remains the current authorized fallback.

The snapshot does not broaden evidence authority. The permanent Tier-1 tool still owns the canonical/published-reciprocal evidence scan and exact-game reuse logic.

Do not substitute a different evidence surface merely because portable transport is inconvenient.

## Execution-unavailable sentinels

For Stage 3A-0, `STAGE_3A0_EXECUTION_ENVIRONMENT_UNAVAILABLE` is appropriate only when the lane cannot access:

- the authoritative checkpoint/ledger;
- the exact permanent Stage 3A-0 tool file at the confirmed SHA; or
- temporary Python/filesystem execution.

For a stateful deterministic pass, the relevant execution-unavailable state applies only when neither an exact-state checkout nor the currently authorized exact-SHA project-state transport works.

Execution difficulty is never permission to begin historical research, clone moving state, use an unpinned snapshot, or transfer routine command execution to the owner.

## Scope discipline

Portable execution changes transport only. It does not change:

- historical evidence standards;
- Research stage boundaries;
- protected-main mutation authority;
- shared-reference authority;
- checkpoint hashes or immutable Research baselines;
- the rule that the permanent repository tool, not conversational reconstruction, owns deterministic output.

