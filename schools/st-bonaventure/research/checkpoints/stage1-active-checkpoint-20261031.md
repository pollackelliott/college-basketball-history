# St. Bonaventure Research — Stage 1 active checkpoint

checkpoint_status: ACTIVE_STAGE1
target_team: St. Bonaventure
program_key: st-bonaventure
research_base_sha: bed68f763a7ea8920c6ba830b004334b16c9e303
protected_main_sha_at_checkpoint: bed68f763a7ea8920c6ba830b004334b16c9e303
stage: 1
scope: INCEPTION+
scope_start_season: 1919-20
primary_source_historical_cutoff: 2025-26
required_completed_season_cutoff: 2025-26

## Controlling checkpoint artifact

Artifact: `st-bonaventure-stage1-active-checkpoint-20261031.zip`
SHA-256: `b52b90f65fbcfcf52ea4733dea1e620f06a361c5d0d099bc526f05a41f369ad1`
Archive size: 72,009 bytes
Archive root: `st-bonaventure-stage1-active-checkpoint/`

Members:
- `structured-stage1-ledger.csv`
- `season-census.csv`
- `excluded-rows.csv`
- `accepted-corrections.csv`
- `blocking-residuals.json`
- `source-inventory.json`
- `stage1-status.json`
- `research-log.md`
- `stage1-manifest.json`

## Durable state

- 2,609 identified candidate game rows are serialized.
- Six 1919-20 founding-season games are individually identified.
- The institution records 1919-20 as 6-10 / 16 games, leaving exactly 10 founding-season game identities unresolved at this checkpoint.
- Every played season from 1920-21 through 2025-26 is mechanically row-count reconciled after accepted exclusions/supplements/corrections.
- 1943-44 is preserved as No Team Fielded.
- Non-counting exhibitions are excluded rather than used to force season totals.
- The 1976-77 South Carolina 2-0 administrative forfeit is preserved outside the played-game census because the primary source says the NCAA does not recognize it.
- 2002-03 on-court results remain separate from the later administrative forfeiture note.
- Literal source evidence is retained for every corrected/excluded source row.
- No anonymous or placeholder games have been created.
- Stage 2 has not started.
- No protected-main or shared/global registry state has been mutated.

## Current sole blocker

`STB-STAGE1-BLOCK-001 — FOUNDING_SEASON_PARTIAL_ROW_IDENTIFICATION`

The target institution establishes the 1919-20 varsity season and a 6-10 record, but the supplied record book does not contain its detailed schedule. Bounded institutional/obvious reciprocal research has identified six individual games. The remaining ten may not be allocated from the aggregate record or created as anonymous rows.

Next bounded evidence family:
1. official Westminster historical schedule/opponent history;
2. official Saint Francis (Pa.) historical series/schedule;
3. target institutional opponent-series arithmetic only as reconciliation evidence, never as row creation;
4. stop rather than fan out indefinitely if those obvious authoritative paths fail.

## Recovery rule

Recover from the exact ZIP SHA above plus this branch and current protected-main policy. Do not reconstruct the accepted post-1919 game universe from conversational recollection. Do not reopen already reconciled post-founding seasons absent concrete contradictory evidence.
