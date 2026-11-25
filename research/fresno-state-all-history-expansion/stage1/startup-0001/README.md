# Fresno State ALL_HISTORY_EXPANSION — Stage 1 startup checkpoint 0001

**Status:** INITIAL_SOURCE_RECOVERY; Stage 1 OPEN. This is not a Stage 1 COMPLETE checkpoint or a Research Freeze.

- School: Fresno State (fresno-state)
- Research lane: research/fresno-state-all-history-expansion
- Immutable expansion research_base_sha: `087ac5dedc65780b65b7ae8d61e239d2033e2eea`
- Accepted published baseline: 1,708 source-game rows; 1970–71+ publication, LEGACY_TOP_LEVEL_ONLY.
- Accepted top-level authority: 1970–71+, NOT superseded.
- Original preserved 1,786-game research representation: `7925342ad192f86ac7f943ce4b439e31dc402b80`; source-games.csv Git blob `8005f9e96841acd65dc1fa5e50676a022ec9d785`.
- Recovered prior unpublished evidence: exactly 78 original rows in 1955–56, 1956–57, 1957–58 (25, 26, 27). **Not publication authority.** Original final Research Freeze ZIP has not been independently recovered and is not being impersonated.
- Newly supplied source: Fresno State 2025–26 Men's Basketball Media Guide, original uploaded filename `NEW_25-26_MBB_Media_Guide_V2.pdf`, SHA-256 `b960369400bb42be27caa0331a1be2c9defd1e9163e4ea14f567c38e262693ba`.
- Primary cited results coverage of uploaded guide: PDF pp. 41–47 (printed pp. 39–45) contains season-by-season results 1921–22 through 1969–70, with subsequent 1970+ pages also present; guide Quick Facts, PDF p. 4 (printed p. 2) states first season 1921–22.
- Censused pre-baseline seasons: 49 (1921–22 through 1969–70); 48 explicit W–L aggregates, totaling 554 wins / 480 losses / 1,034 aggregate games. These are **season aggregates**, not 1,034 adjudicated individual competitive rows and NOT the number of missing games.
- 1943–44: university guide specifically reports withdrawal from *intercollegiate* competition, participation in local San Joaquin Valley League against service/civilian teams, and no available records; varsity game-universe treatment remains a distinct open historical assessment. Do not label every game dormant without adjudication.
- Official 1955–58 aggregates exactly equal 78 previously accepted original rows: 8–17 (25), 16–10 (26), 19–8 (27); 1957–58 prior rows include two NCAA College Division postseason games.
- Prior owner 2026-10-29 scope exclusion is separately binding; recovering this research evidence does not reverse owner publication scope or alter top-level classification.
- The publication baseline is **not** reproduced in this branch or supplemental ledger, and inherited source games must be deduplicated against existing canonical/reciprocal evidence later.
- No tracked published data, canonical games, global registries, or Implementation lock modified.

## Durable members

1. `season-census.csv`: source-aggregate season accounting and activity/research classifications for all 49 years; identified *new* supplemental rows currently zero, pending source-first reconstruction.
2. `historical-1955-58-original-source-games.csv`: exact CSV text of the 78 original excluded rows read from authenticated historical commit above.
3. `media-guide-early-results-raw.txt`: raw parsed text of all seven source pages, preserving source text even if this chat or uploaded attachment becomes unavailable.
4. This `README.md`: base, provenance, source limitations, initial result, recovery instructions.

## Next bounded Stage 1 unit

Perform season-first extraction/reconciliation of the preserved media-guide source pages across the pre-1970 interval; preserve stable row identities and literal score/result/opponent. Separate legitimate competitive games from documented exhibitions, alumni/scrimmage ambiguity, and 1943–44 activity uncertainty. Reuse the recovered 78 original IDs and existing evidence without copying them as newly invented or publication-authorized rows. Compare every season's identified ledger to the official 49-season census and preserve discrepancy/exclusion queues. Read original Research Freeze if a separately hash-authenticated artifact becomes available. Do not equate media-guide aggregate game counts with extractable games until reconciliation.
