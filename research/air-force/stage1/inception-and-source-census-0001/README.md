# Air Force — Stage 1 inception, inaugural census and source inventory 0001

STATUS: STAGE1_IN_PROGRESS — DURABLE INITIAL SOURCE/CENSUS CHECKPOINT (not Stage 1 COMPLETE, not RESEARCH_FROZEN)

- School: Air Force; key: `air-force`; identity: United States Air Force Academy (Falcons)
- research_base_sha (immutable): `3f5a15458aa468347e56e669327d6fe4c9c6ee69`
- branch: `research/air-force`
- institutional inception: **1956-57**. The institutional 2026-27 history PDF includes Bob Spear's 1956-57 squad, dated individual results and roster/player records. The official historical 1956-57 schedule/roster and an Air Force 2006 article describing the inaugural season independently corroborate the year.
- accepted owner top-level classification: **`Air Force,1957-58+`**, baseline CONFIRMED and FINAL, not inferred from inception. 1956-57 is **NON_D1** and its 21 legitimate varsity competitive games remain in the complete-institutional publication research population.
- primary_source_historical_cutoff: **2025-26**, established from actual season results on the source's year-by-year pages, not inferred from its title.
- required_completed_season_cutoff: **2025-26**.
- Primary institutional guide: https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/goairforcefalcons.com/documents/2026/5/27/History.2026-27.pdf?timestamp=20260527033629
- Guide PDF uploaded copy SHA-256: `5fdf61cc80c698bae8ce61cc0ae1009d01139682c8148014934e304b407b73fd`
- Guide year-by-year won/loss records: PDF p. 42. Guide detailed year-by-year results: PDF pp. 58–72. 1956-57 detailed results: PDF p. 58.
- Official schedule: https://goairforcefalcons.com/sports/mens-basketball/schedule/1956-57

## Completed bounded work

* 70 consecutive institution-documented seasons, 1956-57..2025-26, with season-level W/L and games recorded in `season-census.csv` (21 plus 69 top-level seasons). All 70 remain active seasons per source W/L, no proven DORMANT_OR_NO_TEAM.
* Inaugural 1956-57 identified competitive games: **21 / expected 21**, **11 W / 10 L**. All rows have unique stable local IDs, dates, scored results, original opponent labels, literal media-guide row text, and REGULAR_SEASON game type. No extra synthetic games.
* The institutional official schedule supports **9 HOME (6-3), 8 AWAY (3-5), 4 NEUTRAL (2-2)**. These are game-level source classifications, not deductions from geography.
* Six media-guide rows bearing `*` have the explicit guide note **Denver Auditorium Arena**. The official schedule places all six in Denver and lists 4 of them NEUTRAL, 2 AWAY. Retain the original H/A/N evidence separately from venue evidence.
* 1956-57 schedule and media-guide results agree game-for-game in dates, literal opponent identity as named (apart from display variation), scores and W/L; zero identified game-identity/season-accounting blockers for this season. Both overtime rows preserved.
* The guide's 2025-26 results establish the primary-source historical cutoff. 2026-27 is a prospective season and is **not** in the completed-season Research universe.
* No exhibitions are present in either counted 1956-57 result list. This is not a blanket claim that no other unlisted exhibition occurred.

## Deliberately incomplete — exact outstanding populations

1. **69 top-level seasons (1957-58 through 2025-26)** have institutional W/L aggregates but their full game-row populations have **not yet been extracted** into a working ledger. They total **1,907 aggregate-expected games** based on the per-season records; this number is NOT accepted row-level games or a source-acknowledged missing-game gap. Next step is high-yield systematic extraction in bounded season blocks.
2. The PDF's printed **TOTAL 816-1114** (p. 42) conflicts with summing its 70 listed season records: **814-1114**. Exactly **+2 printed total wins** are unaccounted for. Preserve this as a source-internal aggregate discrepancy; do not silently modify any season or invent games.
3. Opponent identity crosswalk, full later-season inclusion/exclusion accounting, and all later-year game-level H/A/N/site evidence remain Stage 1/Stage 2/Stage 3 work, not yet accepted. H/A/N classifications on the inaugural schedule are source-supported, but do not promote any external-link domain in the schedule to historical opponent-identity authority.
4. Game-level source text for 1957-58 onward, and potential detail-heading vs season-aggregate discrepancies, are an unfinished systematic extraction family. No bespoke opponent-by-opponent research is justified yet.
5. No Stage 5 NON_D1-opponent owner sanity scan has been performed; this belongs to the required later gate, not to scope adjudication.

## Exact next bounded Research unit

Extract and reconcile the guide's **1957-58 through 1960-61** detailed game results (PDF p. 58) against the institutional season aggregates and official season schedules. Add all identified game rows with stable IDs and literal/provenance preservation; separately classify duplicate/excluded/heading mismatch residuals. Stop at the resulting durable checkpoint; do not advance to Stage 2.

## Safety

Research-only branch. Protected main, canonical games, global shared registries, other school checkpoints, published history and Implementation lane untouched. 1957-58 D1 boundary final. Research package terminal label will be ordinary RESEARCH_FROZEN, not expansion.
