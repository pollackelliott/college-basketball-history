# New Mexico ordinary Research — Stage 1 checkpoint 0001

**State:** STAGE_1_IN_PROGRESS — source inventory / automated candidate extraction only. **NOT STAGE_1_COMPLETE.**
**Research branch:** `research/new-mexico`
**Immutable `research_base_sha`:** `242370fc551fd749c157c74d92917ddfafbe40e0` (authenticated protected `main` on 2026-11-28)
**Research type:** NEW ORIGINAL-SCHOOL; ordinary complete-institutional Research. Not All-History Expansion or Implementation.
**Target:** New Mexico (`new-mexico`); men's varsity.
**Accepted top-level scope:** `INCEPTION+` — **FINAL OWNER RULING**, superseding the `1950-51+` New Mexico row in `data/reference/program-top-level-scope.csv`. Scope provenance and researched inception are preserved in `research/new-mexico/stage4-authoring/institutional-scope.json`. Research does not modify the protected-main reference; serialized target Implementation later reconciles only its target row during guarded Phase 0.
**Researched varsity inception:** `1899-00`, as the University of New Mexico itself states on physical page 3 and begins its historical results on physical page 121.
**Required completed-season cutoff:** `2025-26` (2026-27 is in progress on 2026-11-28).
**Primary results cutoff verified:** `2025-26` (last year-by-year-results heading on physical page 132); source covers the required period.

## Primary attachment/provenance

- One source PDF received: `New Mexico.pdf`, University of New Mexico, *2026-27 New Mexico Basketball* record book / media guide, 132 PDF pages.
- Exact uploaded PDF SHA-256: `94a121232efa82a71ebb448139d4e72c799ac032128cb625ce2a5178b6bbdcc7`; original PDF not committed (33 MB).
- Page 3: PROGRAM HISTORY states **First Season 1899-1900**, overall record **1,667-1,223**, "in 126 seasons".
- Pages 121–132: year-by-year results from **1899-00 through 2025-26**, with season headings and month/day date tokens, opponent labels, on-court W/L and scores. Repeated opponents/dates are separate source appearances until canonical verification.
- Page 1: 2026-27 schedule marks preseason exhibitions explicitly **(Ex.)**, demonstrating that scheduled exhibition games are a separate noncompetitive population; these 2026-27 future rows are not in Stage 1 completed-season scope.

## What is serialized (mechanical first pass, not accepted games)

- `provisional-result-rows.csv`: **2,756 preliminary parsed result lines**, all extracted from the 12 official year-by-year-results pages, carrying literal date token, opponent text, result, score, PDF page/column, source order and text. **Not** a final unique competitive-game count.
- `season-census.csv`: **127 printed season headings** across 1899-00..2025-26, with official heading W/L where present, candidate row W/L, no-team states and explicit mismatch status. Four source headings read "No Team": 1900-01, 1903-04, source literal 1907-18 (likely typo for 1917-18), and 1920-21. Do not silently turn a no-team season into one with games.
- `mechanical-review-queue.csv`: **375 review records**: 308 unmatched/other score-like extracted lines, 64 candidate-versus-season-heading record mismatches, 1 date heading typo review, 1 overall aggregate contradiction, and 1 additional 1918-19 source contradiction marker (also counted within the 64 season mismatches). Some records are mere coach statistics/footnotes; review them mechanically before treating them as historical missing games. A single true issue may appear in more than one queue row.

### Source discrepancies already witnessed

1. Page 121 labels a no-team season "**1907-18 (No Team)**" between 1916-17 and 1918-19, an evident chronology typo; likely normalized to 1917-18 after explicit verification, preserve source wording.
2. Page 121 heading "**1918-19 (4-1)**" conflicts with the six detailed results, which list **2 W and 4 L**; adjacent John F. McGough coaching box reads **2-4**. This is a **primary-source internal contradiction**, not permission to remove games or overwrite results.
3. Page 3 aggregate **1,667-1,223** differs from naive sum of the 123 numeric source-season headings (**1,668-1,221**). Must research/account for record corrections and missing source rows before accepting aggregate arithmetic.
4. Most later season mismatch records are attributable at least partly to table extraction layout/split tournament labels; **do not infer 64 actual missing seasons or games** from the first-pass machine output.

## Provisional-file SHA-256 (LF normalized as committed)

- `provisional-result-rows.csv`: `082787ea088702d4e51926b81b6078c714ef2c534d73e52573454468eb8b7b51`
- `season-census.csv`: `ba684ac00b0630a0341fc339321967c1b9f8ced329e79530e325e8245bb7e3aa`
- `mechanical-review-queue.csv`: `698ebaa7fcd96fe6db555fc6b97b358abe3f7799ea8474dc46cba64ba3cbfe01`

Every GitHub file was read back from the Research branch and text-compared exactly after creation. This provisional mechanical snapshot is self-contained with its raw rows, season headings, source PDF hash, discrepancy queue, and scope authority; do not treat a displayed source aggregate as a verified game-ledger total.

## Required next bounded Stage 1 unit

Perform **one systematic table-layout repair and reconciliation pass** across PDF pages 121–132, specifically the 308 unmatched lines (multi-line tournament scores, table breaks, date/score typography) and linked 64 season-heading differences. Separate layout artifacts and coach statistics from real games, recognize explicit postseason/tournament labels, serialize game_type for every accepted game, flag any actual exhibitions and duplicates, and establish stable research-local game IDs. Prioritize 1918-19, 1933-34, 1940-41 and late-season postseason omitted/split rows as representative defect families; preserve literal evidence and any genuine unresolved historical inconsistencies. Produce a successor SHA/size-manifested Stage 1 checkpoint with **accepted competitive-game ledger, exclusion ledger, reconciled season census, and exact surviving blocker/nonblocker queues** before external historical discrepancy research. Do not enter Stage 2 without owner-stage authorization.

No repository shared basketball data, current main, existing school packages or Implementation mutation lock was modified. No workflow is presently running or awaited.
