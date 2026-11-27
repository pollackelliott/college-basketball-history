# San Diego State — Stage 1 checkpoint 0019: founding coverage-gap audit contract diagnosis

Authenticated protected main: 3f5a15458aa468347e56e669327d6fe4c9c6ee69. Existing Research parent: 659edca0d2bb582f97ca43d700bbb5f582f801d4. Immutable research base: 5b840a354fb5cd792239ff8b93cba223a18dd87a. No original accepted or excluded game record changed.

Verified full source ledger: 1,126 named results, 1,086 accepted competitive (1,043 regular season, 43 postseason), 40 excluded, zero held inclusion and game type.

Repaired display-only 49-season source W/L/T census in appended overlay from exact checkpoint 0009. All 49 official fields in checkpoint 0018 presentation file were blank despite its correct counts; checkpoint 0018 remains immutable and the original 0009 census was manifest authenticated. The overlay carries the actual source heading and accepted/excluded/administrative partition for each season.

The original 1921–22 source printed exactly: 1 win, 2 losses vs. unknown teams. Forfeit wins vs. Riverside & Fullerton JC. Source heading 14–8; 17 named results; two forfeit awards; 1W/2L against unknown teams. Named rows partition 14 accepted + two owner-excluded Alumni at Stanford + own JV one. The official record cannot be presented as the recognized competitive game-derived W/L. No names or game IDs invented.

Current protected-main permanent tool is tools/research_stage1_coverage_gap.py, git blob 48d2a085a32873ebf4d22c565fc138e72e03cdf8, SHA-256 7be2816d3884e0b41ec3b222d37d08c22764355ec653d68227487b2b43653175. Its strict _count_missing note parser does not match the literal phrase 'vs. unknown teams'; diagnostic equivalent count pattern yields zero matches and predicts NO_EXPLICIT_INSTITUTIONAL_MISSING_COUNT:1921-22. The tool's source_listed_rows + recovered_count == accepted-ledger row invariant also cannot represent 17 printed = 14 accepted + 3 known excluded without generic representation capability; predicts SOURCE_LISTED_ROWS_MISMATCH after safe parser handling.

The historical facts are not unsolved by these defects. Two source/semantic incompatibilities block the permanent audit even before research-exhaustion certification. They are generic tooling/schema matters, not a school-specific game classification or another owner permission to overwrite history.

Separate research-exhaustion requirement remains unverified. Prior evidence locates SDSU's period newspapers and Fontius historical study, but no record of two fully inspected, independent, 1921–22 source paths establishing that the three unnamed opponents remain unrecoverable. This is not an assertion of archive exhaustion. Record honest access limitations and work that remains.

This checkpoint is an independently hashable STATIC CONTRACT DIAGNOSTIC, NOT the permanent audit, not audit eligibility and not Stage 1 COMPLETE. The permanent audit script was not executed and no compatible SHA256-pinned full Stage 1 ZIP was constructed. Tool repair, if authorized, must be generic fail-closed, cover original wording and excluded-row arithmetic, and add negative and positive regression tests; followed by actual bounded source exhaustion and exact-SHA read-only audit.

No protected-main/tool mutation, no Stage 2, no Research Freeze, no new Implementation, no automatic closeout. Next: Control Center assesses generic correction authority and Research gathers bounded original 1921–22 recovery paths, preserving stable game IDs.
