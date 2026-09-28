# Portable Research Execution Contract

- **Status:** Controlling Research-lane execution policy
- **Applies to:** deterministic Research substages requiring pinned protected-main project state
- **Purpose:** preserve mobile-first Research while keeping mechanical passes deterministic and SHA-pinned

## Governing rule

A Research lane must not require an owner-managed Codespace merely because a deterministic project-evidence pass needs protected-main repository files.

The normal owner experience remains:

`attach checkpoint -> Proceed -> bounded Research work -> durable checkpoint`

A persistent repository checkout is one valid execution surface. It is not the only valid execution surface.

## Execution order

For a deterministic Research command requiring protected-main project state:

1. confirm the exact protected-main SHA;
2. use an already-runnable checkout at that exact state when available;
3. otherwise, if temporary filesystem, Python, and direct HTTPS download/extraction are available, fetch one disposable repository archive pinned to that exact SHA;
4. run the same permanent repository command from the extracted snapshot, passing the exact protected-main SHA explicitly;
5. preserve the command outputs/checkpoint;
6. discard the temporary snapshot.

Portable execution is transport of already-authorized project state. It is not external historical research and does not broaden the evidence universe of the active Research stage.

## Exact-SHA archive

The only authorized portable archive is:

`https://codeload.github.com/pollackelliott/college-basketball-history/zip/<exact-protected-main-sha>`

Use the full 40-character commit SHA.

Do not:

- use `main`, `HEAD`, a tag, or another moving reference;
- clone the repository;
- create or push a branch;
- mutate protected main;
- search for alternate mirrors, snapshots, or tools;
- inspect remote tool source to derive historical conclusions;
- use repository search as historical source discovery;
- ask the owner to open Codespaces merely to provide this mechanical execution surface.

## Stage 3A-0

When no checkout exists, run `tools/research_stage3a0.py` from the disposable exact-SHA snapshot with the authoritative Stage 2 checkpoint/ledger and explicit `--main-sha`.

All Stage 3A-0 local-only evidence restrictions remain unchanged.

## Stage 3A-3 Tier 1

When no checkout exists, run `tools/research_stage3a3_tier1.py` from the disposable exact-SHA snapshot with explicit `--repo-root` and `--main-sha`.

The permanent tool retains authority for canonical and published-reciprocal evidence reuse.

Do not substitute `data/evidence/game-assertions.csv` for published reciprocal source packages; parity testing found missing published rows and material site-field differences.

## Execution-unavailable sentinel

`STAGE_3A0_EXECUTION_ENVIRONMENT_UNAVAILABLE` applies only when neither is available:

- an exact-state runnable checkout; nor
- temporary execution capable of downloading, extracting, and running one exact-SHA disposable repository snapshot.

The sentinel is not triggered merely because the owner is using the mobile app or because no persistent checkout is mounted.

If neither execution route exists, stop. Do not simulate the permanent command conversationally or transfer routine execution work to the owner.

## Invariant

The intended result is execution-surface equivalence:

`same checkpoint + same protected-main SHA + same permanent tool = same mechanical Research result`
