# New Mexico Research — Stage 1 checkpoint 0002

**State:** STAGE_1_IN_PROGRESS. Systematic primary-source table-layout repair checkpoint; not Stage 1 COMPLETE and not authorization for Stage 2.

- Branch: `research/new-mexico`; immutable `research_base_sha`: `242370fc551fd749c157c74d92917ddfafbe40e0`.
- Parent: research commit `69a1953795334b8c6c64edc0766237f1ddb336bf`, checkpoint `0001-stage1-primary-source-inventory` (unchanged).
- Source: official *2026-27 New Mexico Basketball* record book, supplied as `New Mexico.pdf`, SHA-256 `94a121232efa82a71ebb448139d4e72c799ac032128cb625ce2a5178b6bbdcc7`; actual year-by-year results on PDF pages 121-132, complete through 2025-26. Appendix of separately documented exhibitions on PDF page 79 remains an explicit exclusion-crosswalk task.
- Scope: owner-final `INCEPTION+`; first varsity season `1899-00`. Current reference `1950-51+` is superseded for New Mexico but untouched on protected main; scope authority is retained at `research/new-mexico/stage4-authoring/institutional-scope.json`.

## Mechanical reconciliation completed

- Rebuilt layout rows with a 3.7-point same-row span tolerance, instead of the preceding overstrict 1.55-point tolerance. All inherited candidate rows and literal evidence remain available in parent 0001.
- Extracted **2,886** machine-readable dated source result rows; rescued **5** additional actual game-result lines from the source (four score typography defects and one explicitly documented 1933-34 win without a date or score); **2,891 provisional candidate games** in the new structured ledger.
- Classified **44** remaining unmatched fragments as coach career statistics/date-ranges, not omitted games; their literal text and page positions are retained in the rejected-extraction ledger.
- Reconciled 64 initial season-heading mismatches to **3 source-internal W/L conflicts**. The 127 headings include four explicit No Team years; source typo `1907-18 (No Team)` is normalized chronologically to `1917-18`, while its literal remains recorded.
- Every candidate carries a stable research-local ID, source literals/page/column/position, source date token, source-result, score status, and provisional structured `game_type`. Source location tokens are preserved; `site_type=UNKNOWN` is intentional pending later authorized site work, not a geographical inference.

## Remaining Stage 1 blockers / nonblocking debt

1. **1918-19**: heading 4-1 vs six detailed games 2-4 (PDF p.121; adjacent coaching box supports 2-4).
2. **1940-41**: heading 5-17 vs 23 listed results 5-18 (PDF p.122).
3. **1979-80**: heading 6-22 vs 28 listed results 7-21 (PDF p.126); the record includes a separately annotated forfeit. Preserve the actual played game and distinguish administrative record from on-court outcome.
4. **Aggregate**: program overview lists 1,667-1,223 (PDF p.3), while source-listed candidate results are 1,667-1,224; do not delete a result to force the summary.
5. **Field-only debt**: seven candidate game rows lack a reliably delimited/exact score in their literal result text; preserve `source_score_literal` and blank curated points.

## Exact next Stage 1 assignment

Crosswalk the primary source's separate exhibition appendix (PDF p.79) against the candidate game ledger; classify actual source-listed exhibitions, forfeit versus on-court history, and remaining season/aggregate contradictions in a bounded authoritative-source evidence family. Preserve exclusions and unresolved debt without inventing games or scores, then rederive the accepted season/game census and checkpoint it before any Stage 2 transition.

No shared/global basketball data, protected main, Implementation, or other school's research state was mutated. The files in this checkpoint have exact SHA-256 and size records in `manifest.json`; only checkpoint files were added to the Research branch.
