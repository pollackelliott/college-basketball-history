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
3. when those authenticated bytes can be written to temporary storage, run that exact file against the authoritative Stage 2 checkpoint/ledger with explicit `--main-sha`;
4. if the connector can read the file but cannot materialize/write those bytes into the execution filesystem, use the authenticated exact-SHA Stage 3A-0 artifact fallback described below;
5. preserve the emitted Stage 3A-0 artifacts.

A repository archive is not required for Stage 3A-0.

The connector fetch and the exact-SHA artifact are executable transport. Do not inspect the tool source to derive basketball conclusions, edit the fetched algorithm conversationally, or substitute a hand-reimplemented census.

### Stage 3A-0 authenticated exact-SHA artifact fallback

Protected `main` publishes a short-retention GitHub Actions artifact named
`research-stage3a0-tool-<exact-protected-main-sha>`. It is built from the exact pushed
commit by `.github/workflows/research-stage3a0-portable.yml`.

The artifact contains exactly:

- `tools/research_stage3a0.py`;
- `tools/research_stage3a0_portable.py`;
- `research-stage3a0-tool-manifest.json` with the exact protected-main SHA, file sizes,
  and SHA-256 hashes.

It deliberately contains no canonical games, registries, school packages, or other
basketball/project state because Stage 3A-0 does not read them.

When direct exact-file transport cannot be materialized into the execution filesystem:

1. query GitHub Actions through the authenticated GitHub connector for the successful
   `Research Stage 3A-0 portable tool` push run whose `head_sha` is the exact
   protected-main SHA;
2. require the artifact name to contain that exact SHA;
3. download/materialize that artifact into temporary storage;
4. verify the extracted bundle with
   `python tools/research_stage3a0_portable.py verify <bundle-dir> --main-sha <exact-sha>`;
5. only after verification succeeds, run the unchanged
   `tools/research_stage3a0.py` against the authoritative Stage 2 checkpoint/ledger with
   the same exact `--main-sha`.

Do not use an artifact from another commit, an expired artifact without re-establishing
exact state, a hand-reconstructed tool file, codeload, a clone, a full repository archive,
or owner-operated Codespaces merely to run Stage 3A-0.

The Stage 3A-0 invariant is:

`same checkpoint + same permanent-tool bytes = same census/partition/queues`

The protected-main SHA remains recorded so the exact tool/policy version is auditable.

## Deterministic stages that genuinely require project state

Some later mechanical operations may legitimately require protected-main basketball/project files. Stage 3A-3 Tier 1 currently does.

For such an operation:

1. confirm the exact protected-main SHA;
2. use an already-runnable checkout at that exact state when available;
3. otherwise, if direct HTTPS download/extraction works, fetch one disposable repository archive pinned to that exact SHA;
4. if the archive transport is unavailable, use the authenticated GitHub exact-SHA artifact fallback described below;
5. run the permanent repository command from the verified snapshot, passing the exact protected-main SHA explicitly;
6. preserve the command outputs/checkpoint;
7. discard the temporary snapshot.

The authorized full-repository portable archive for a stateful operation remains:

`https://codeload.github.com/pollackelliott/college-basketball-history/zip/<exact-protected-main-sha>`

Use the full 40-character commit SHA. Never use `main`, `HEAD`, a tag, or another moving reference.

This archive path is **not** the Stage 3A-0 execution path.

### Authenticated exact-SHA artifact fallback

Protected `main` publishes a short-retention GitHub Actions artifact named
`research-stage3a3-tier1-state-<exact-protected-main-sha>`. It is built from the
exact pushed commit by `.github/workflows/research-stage3a3-tier1-portable.yml`.

The artifact contains exactly the permanent Tier-1 executable surface and its complete
repository evidence surface:

- `tools/research_stage3a3_tier1.py`;
- `tools/research_stage3a3_tier1_portable.py`;
- `data/canonical/games.csv`;
- every `schools/*/source-games.csv`;
- `research-stage3a3-tier1-state-manifest.json` with the exact protected-main SHA,
  file sizes, and SHA-256 hashes.

This is not a row-filtered or conversationally selected evidence subset. It is the
complete set of repository files the permanent Tier-1 algorithm reads.

When codeload/archive transport is unavailable:

1. query GitHub Actions through the authenticated GitHub connector for the successful
   `Research Stage 3A-3 Tier 1 portable state` push run whose `head_sha` is the
   exact protected-main SHA;
2. require the artifact name to contain that exact SHA;
3. download/materialize that artifact into temporary storage;
4. verify the extracted snapshot with
   `python tools/research_stage3a3_tier1_portable.py verify <snapshot-dir> --main-sha <exact-sha>`;
5. only after verification succeeds, run the unchanged permanent Tier-1 command using
   that snapshot as `--repo-root` and the same exact `--main-sha`.

Do not use an artifact from another commit, an expired artifact without re-establishing
exact state, a hand-selected file subset, or reconstructed project evidence.

## Stage 3A-3 Tier 1

Stage 3A-3 Tier 1 continues to use the unchanged permanent
`tools/research_stage3a3_tier1.py` accepted-evidence pass and therefore requires exact
protected-main project state.

When no exact-state checkout exists, use the exact-SHA codeload snapshot when available.
If that transport fails, use the authenticated exact-SHA Actions artifact above. Both
transports expose the same complete Tier-1 evidence surface.

The snapshot does not broaden evidence authority. The permanent Tier-1 tool still owns
the canonical/published-reciprocal evidence scan and exact-game reuse logic.

Do not substitute a different evidence surface merely because portable transport is inconvenient.

## Execution-unavailable sentinels

For Stage 3A-0, `STAGE_3A0_EXECUTION_ENVIRONMENT_UNAVAILABLE` is appropriate only when the lane cannot access the authoritative checkpoint/ledger, cannot obtain and execute the exact permanent Stage 3A-0 tool through either the direct authenticated-file path or the authenticated exact-SHA artifact fallback, or lacks temporary Python/filesystem execution after those transports are exhausted.

For a stateful deterministic pass, the relevant execution-unavailable state applies only when no exact-state checkout is available and both authorized exact-SHA transports fail: the pinned codeload/archive path and the authenticated GitHub Actions artifact path.

Execution difficulty is never permission to begin historical research, clone moving state, use an unpinned snapshot, or transfer routine command execution to the owner.

## Scope discipline

Portable execution changes transport only. It does not change:

- historical evidence standards;
- Research stage boundaries;
- protected-main mutation authority;
- shared-reference authority;
- checkpoint hashes or immutable Research baselines;
- the rule that the permanent repository tool, not conversational reconstruction, owns deterministic output.

