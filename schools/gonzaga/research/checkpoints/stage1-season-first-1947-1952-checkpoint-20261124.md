# Gonzaga ALL_HISTORY_EXPANSION Research — Stage 1 season-first 1947-48 through 1951-52 bulk checkpoint

checkpoint_status: ACTIVE_STAGE1_SEASON_FIRST_BULK_TRANCHE_ACCEPTED
target_team: Gonzaga
program_key: gonzaga
research_base_sha: f64ce23988faa04a304eb15d9ad96c2144ed5777
protected_main_sha_at_checkpoint: 1a1d1758b40f2fedaec56f3c3d6528647a6c909d
accepted_program_inception_season: 1907-08
stage: 1
stage1_complete: false
stage2_authorized: false

## Method change

This checkpoint deliberately changes the primary Stage 1 execution shape from **opponent-family-first** harvesting to **season-first bulk reconstruction**.

The accepted 422-game ledger remains the immutable deduplication seed for this successor.

The new process is:
1. select high-gap seasons;
2. harvest played-game identities across all opponents from systematic contemporary/official corpora;
3. deduplicate mechanically against the accepted ledger;
4. reconcile the entire season block against Gonzaga's official season records;
5. use opponent-family work later as bounded repair rather than the main discovery engine.

This is the Stage 1 execution shape contemplated by the repository contract: establish the candidate universe first, then repair residual discrepancies.

## Bulk tranche

Seasons:
- 1947-48
- 1948-49
- 1949-50
- 1950-51
- 1951-52

Previous controlling ledger: **422**
Accepted additions: **37**
New controlling ledger: **459**

All 37 additions have stable played-game identity and on-court result.

No exact-date collision was found.
No same-opponent/same-score duplicate against the accepted ledger was found.
No new season-accounting contradiction was created.

## Season accounting after this tranche

| Season | Official Gonzaga record | Identified after tranche | Newly added | Arithmetic difference |
| --- | --- | --- | ---: | ---: |
| 1947-48 | 24-11 / 35 | 15-7 / 22 | 10 | 13 |
| 1948-49 | 17-12 / 29 | 7-7 / 14 | 2 | 15 |
| 1949-50 | 18-11 / 29 | 14-11 / 25 | 11 | 4 |
| 1950-51 | 8-22 / 30 | 5-9 / 14 | 3 | 16 |
| 1951-52 | 19-16 / 35 | 13-13 / 26 | 11 | 9 |

The arithmetic difference is diagnostic only. It is not a missing-game row count and never authorizes an anonymous game.

The most striking convergence is **1949-50**, which moves from 14 identified games to **25 of the official 29** in one season-first pass.

## Source mode

This tranche uses:
- official opponent schedule/history pages where available;
- contemporary college-score/game reporting preserved by Oregon Historic Newspapers;
- NAIA historical championship records for lower-level national postseason.

Schedule-only mentions were not admitted as games.

The West Coast Conference historical record-book PDF was tested as a possible bulk extractor and **rejected** for this unit because its multi-column text extraction was interleaved in the current interface and could not be safely visually verified. No row relies on that corrupted extraction.

## Conservative field policy

Unknown remains preferable to unsupported certainty.

Dates are written only when:
- directly printed by an official schedule/history;
- or mechanically fixed by an explicit contemporary phrase such as `last night`, a weekday-result label, or a Friday/Saturday series recap.

H/A/N is written only from source-explicit relationship evidence.

Two score conflicts remain nonblocking:
- 1949-50 Whitman: Gonzaga win and 65 Gonzaga points are stable; Whitman score conflicts between 20 and 29, so opponent score is blank.
- 1952-01-14 Eastern Oregon: Gonzaga win, 90 Gonzaga points, date and neutral Baker site are stable; contemporary opponent scores conflict among 63, 62 and 41, so opponent score is blank.

Neither uncertainty can change game identity, inclusion, season allocation, or result.

## Postseason

Lower-level postseason is structured generically as `POSTSEASON`, including:
- 1948 Pacific Lutheran NAIB qualification;
- 1948 NAIA national-tournament games vs Texas Wesleyan and Hamline;
- 1952 Whitworth NAIB qualification.

No top-level conference-tournament meaning is implied.

## Existing accounting debt

The four parked research-exhausted accounting contradictions remain unchanged:
- 1915-16;
- 1930-31;
- 1936-37;
- 1937-38.

Active discrepancy-research blockers remain **0**.

## Current Stage 1 posture

Official expansion aggregate: **477-500 / 977**

Identified game identities: **459**
Known results: **459**
Aggregate-minus-identified diagnostic: **518**

Stage 1 remains active.
Stage 2 remains unauthorized.

## Next bounded unit

Continue the **season-first bulk method**.

Prioritize another high-yield chronological block rather than returning to opponent-by-opponent harvesting. The next logical target is the large 1941-47 residual block (especially 1941-42, 1944-45 and 1946-47), or a comparably dense systematic season corpus if it yields more rows cleanly.

Opponent-family work should now be reserved primarily for bounded discrepancy repair and clearly high-yield complete series.
