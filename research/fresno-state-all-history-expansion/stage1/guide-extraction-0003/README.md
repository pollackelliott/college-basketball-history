# Fresno State — ALL_HISTORY_EXPANSION Stage 1 source reconstruction checkpoint 0003

**Status:** 1943–44 through 1969–70 guide extraction COMPLETE, prior 78 rows crosswalk COMPLETE; **Stage 1 OPEN**. These are source-entry inventories, not accepted unique-game IDs, Stage 1 closeout, Research Freeze, or publication authority.

- Immutable Research base: `087ac5dedc65780b65b7ae8d61e239d2033e2eea`; parent Research checkpoint commit: `7f49681e79c8c66b62e8261e4376e2bba0a53482`.
- Official source: owner-uploaded 2025–26 Fresno State men's basketball guide (PDF SHA-256 `b960369400bb42be27caa0331a1be2c9defd1e9163e4ea14f567c38e262693ba`), guide pp. 41–45 printed/PDF 43–47. Original extracted literal text is immutable from checkpoint 0001, Git blob `fc72b2862aa283481d498873af0a17fa1d7e405a`.
- 27 seasons 1943–44 to 1969–70 inclusive. **26 seasons** have 661 result entries / 661 aggregate reported games. `1943-44` is `Record: N/A`; guide says withdrawn from *intercollegiate* competition, played San Joaquin Valley service/civilian teams, no records; do not infer a game count, absolute dormant status, or competitive varsity classification without evidence.
- Prior 1955–56 (25), 1956–57 (26), 1957–58 (27): all **78** original accepted Research-game rows align in original source order by exact opponent, score, played result and season. 76 raw lines exact; two overtime whitespace-only literal differences; original text is not rewritten. Original 78 source IDs and rows preserved in checkpoint 0001, Git blob `ef6188b36675cd188a5bc5f1059f10084c70430f`. **They remain excluded from publication by prior owner scope ruling**, and are not minted as new candidate IDs here.
- **583** entries from outside 1955–58 received new stable source-entry IDs in `new-candidate-entries.csv`. The original 78 are a separate historical evidence crosswalk, never copied into the newly created entry population.
- Combined 1921–22 to 1969–70 source inventory now spans 49 season headings, 48 explicit seasonal results records, **1,034 source-listed entries** and exactly **1,034 institutional aggregate games**. Of the source-listed entries, **956** are newly minted candidate *source IDs* (373 from checkpoint 0002 + 583 here) and **78** reference the original accepted-but-unpublished Research IDs. THESE ARE NOT 1,034 independently adjudicated distinct accepted competitive games. Exact game count may be less because explicit exhibition and duplicate representations are present.
- **Administrative forfeits:** two 1954–55 UCSB games and one 1961–62 San Jose State game are on-court losses with opponent forfeitures awarding Fresno administrative wins. Adjusted source season records reconcile 1954–55 from 9–15 to 11–13, and 1961–62 from 18–8 to 19–7. Never erase on-court truth to match an official aggregate.
- **Unexplained W/L conflicts:** 1965–66 official 21–8 vs listed 22–7, 1969–70 official 15–11 vs listed 14–12; preserve contradictions for bounded independent research. Previous 1939–40 conflict in parent checkpoint 0002 (10–9 vs 8–11) remains open.
- **Duplicate candidate:** 1965–66 identical `at San Diego State L 69-66` source entries twice. Preserve both as source entries; two real games not established.
- **Explicit exhibition:** 1963–64 `Fresno State Alumni (Exh) W 86-49` excluded from competitive game ledger but preserved as a source entry. Eight other Alumni games are under inclusion review; `Harlem Clowns` fixture additionally flagged for exhibition-vs-competitive research, not excluded automatically. Official 1963–64 W/L may incorporate the explicit exhibition and must not be used as proof that every listed result is competitive.
- Source `at` and `vs.` locators are retained only as *literal cues*, never an H/A/N verdict. Original guide overtime/result/attendance and literal event markers remain preserved; no unknown dates, opponents, postseason classifications, or venues invented.
- **No mutation** to protected main, current published Fresno State 1,708 game rows, global references/canonical data, top-level scope `1970-71+`, or Hawai‘i Implementation lock.

## Contents

- `new-candidate-entries.csv`: 583 extracted source entries outside 1955–58, with stable source-entry IDs and provenance.
- `original-78-crosswalk.csv`: 78 original ID/guide source-row alignments, raw-literal agreement, and explicit owner publication exclusion.
- `complete-49-season-census.csv`: combines checkpoint 0002's preserved 22 season results with this checkpoint's 27 seasons, maintaining official-vs-on-court-vs-administrative results.
- `administrative-forfeits.csv`: 3 explicit forfeit rows, separate played and administrative semantics.
- `review-queue.csv`: distinct inclusion, duplicate, season-accounting, 1943–44 and explicit exhibition dispositions.
- `extraction-audit.json`: exact base, predecessor, source identifiers, counts, and outstanding residual population.
- `source-event-notes.csv`: preserved historical source note lines for later postseason/event-stage interpretation.

## Next bounded Stage 1 action

Consolidate the already serialized candidate source-entry populations into one controlling Stage 1 game-identity accounting ledger with the original 78 as separately referenced preserved evidence and explicit duplicate/exhibition status. Then undertake a **bounded** material discrepancy family for unresolved 1939–40, 1965–66, 1969–70 and highest-risk varsity inclusion/duplicate cases, using target-school primary guide and coherent opponent reciprocal/season ledger evidence. The 1943–44 activity exception remains historically candid. Do not expand into independent Stage 2 opponent/site research, mutate protected/main data, or seek a new owner gate without a genuine conflict.
