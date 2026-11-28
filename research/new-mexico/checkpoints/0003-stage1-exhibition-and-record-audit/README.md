# New Mexico ordinary Research — Stage 1 checkpoint 0003

**State:** `STAGE_1_IN_PROGRESS` — bounded exhibition/season-record/source-consistency adjudication. **NOT** Stage 1 COMPLETE; no Stage 2 authority.

- School: `new-mexico`; research branch: `research/new-mexico`; original-school complete-institutional Research, **not** All-History Expansion.
- Immutable `research_base_sha`: `242370fc551fd749c157c74d92917ddfafbe40e0`; controlling protected-main AGENTS/protocols inspected at that SHA.
- Parent checkpoint: `research/new-mexico/checkpoints/0002-stage1-layout-reconciled-census/`; parent Research HEAD: `a481be046d6dc93ec885f1bcb7f6ffff50963dd7`.
- Owner-final accepted top-level scope: `INCEPTION+`, superseding baseline `1950-51+`; authority remains in `research/new-mexico/stage4-authoring/institutional-scope.json` (preserve as source of truth). No protected-main/shared-reference edits.
- Source: University of New Mexico *2026-27 New Mexico Basketball* record book, physical PDF 132 pages, SHA-256 `94a121232efa82a71ebb448139d4e72c799ac032128cb625ce2a5178b6bbdcc7`. Result pages 121–132; all-time results pages 44–45; coach records page 50; exhibition appendix page 79; NIT summary page 84. Historical results cutoff 2025–26, which matches required completed-season cutoff.

## Bounded work and source adjudications

1. **Exhibitions.** Source appendix page 79 has **87 distinct entries**: 75 preseason, one in-season, 11 international-trip. **86** are unambiguously excluded exhibition rows, and none is an additional source-result competitive game. A **single exceptional overlap** (`NM-EX-0068`, 2019-11-06 Eastern New Mexico) is labeled preseason exhibition in the appendix but is recorded as UNM's 2019–20 *Game 1* in its detailed game schedule, season cumulative records and official game box score. The opposing school classifies it as an exhibition. Retain the one existing `NM-2019-20-0001` in the New Mexico candidate ledger and preserve the explicit conflicting appendix classification. Do not create a duplicate game. Details/provenance appear in the exhibition crosswalk and adjudication log.
2. **1918–19.** Results page 121 gives a `4-1` season heading but six listed games total `2-4`. All-time year table page 44 and coach John McGough page 50 both say `2-4`. Keep six distinct listed competitive-game candidates with their literal source results; preserve conflicting heading verbatim.
3. **1940–41.** Results page 122 says heading `5-17`; 23 listed games are `5-18`, corroborated by all-time page 44 and coach Dr. Benjamin Sacks page 50. Preserve all 23.
4. **1979–80.** Results detail page 126 records 28 games `7-21`, but the 1979-12-04 `West Texas A&M (forfeit)` is a played `W 112-100`. All-time page 44, season heading and coaching record report administrative `6-22`. Preserve the on-court game `NM-1979-80-0002` and annotate administrative discrepancy rather than reversing its on-court W or deleting it.
5. **1929–30 newly discovered cross-section typo.** Results heading and 20 detailed game rows give `16-4`; coach Roy Johnson's cumulative total and official Mountain West history agree; all-time page 44 instead prints `16-5`. Do not invent a 21st game or edit the literal all-time row.
6. **1966–67 NIT score.** The detailed 1967-03-11 Syracuse win `NM-1966-67-0026` prints malformed `W 6-64` on results page 125; the same official book's NIT summary page 84 has `W 66-64`. Curate 66–64 in numeric points; preserve literal source score and note.
7. **Source-wide summary conflict.** Detailed 2,891 source candidate rows produce on-court `1,667-1,224`; cover-page historical overview says `1,667-1,223` in 126 seasons; all-time results year table sums `1,666-1,226` across 123 record rows. Do **not** manipulate game rows to make these disagreeing publications agree. The discrete cross-section differences are documented.

## Surviving research review

- **Three 1930s Harlem Globetrotters rows** (`NM-1936-37-0006`, `NM-1937-38-0003`, `NM-1937-38-0004`) are listed in the official year-by-year playing results and contribute to its season headings. The UNM exhibition appendix begins decades later and does not adjudicate these. Older UNM guides likewise list the matches as season results. No targeted authoritative evidence found that explicitly labels these *specific* fixtures as exhibitions. Still candidate rows, not automatically accepted simply because the source counts them; do not classify by the later touring-team identity alone.
- **Seven other exact-score unknown/malformed source rows** retain known game identity/results and explicit score uncertainty. One source date still unknown. Do not invent these fields.
- Verify tournament `game_type` grouping in final Stage 1 mechanical closeout (all game rows carry structured provisional types); reconcile any source-overlap/duplicate risks, and distinguish category statuses.
- All 2,891 rows remain **candidates** (`PROVISIONAL_REQUIRES_STAGE1_CLOSEOUT`), not a frozen competitive-game count. One real game must map to one canonical game; no exhibition is accepted on appendix label alone.
- Stage 1 still needs a classification disposition for the historical touring matches and rigorous mechanical consistency closeout. Residuals can remain nonblocking only if actual game identity/inclusion and season W/L are stable under the Stage 1 contract.

## Checkpoint files

- `reviewed-source-games.csv`: all 2,891 provisional source rows, research-local stable game IDs, raw evidence, provisional game type, source/researched numeric score, appended administrative and exhibition crosswalk notes.
- `exhibition-appendix-crosswalk.csv`: all 87 appendix entries, raw scores/dates/opponents, 86 exclusions, one explicit appendix conflict linked to a *single existing* candidate game.
- `composite-season-census.csv`: all 127 chronological source headings, 123 active/no-team classification, per-season detailed rows and year-table crosswalk and exact source discrepancy dispositions.
- `alltime-results-crosswalk.csv`: all 123 all-time year-table records, raw year-table text and detailed W/L comparisons.
- `adjudication-log.csv`: eight documented historical/source-specific decisions or review residuals.
- `stage1-status.json`: authoritative numeric snapshot, exact next assignment and phase-state guard.
- `manifest.json`: SHA-256 and byte count for each checkpoint member, immutable parent/scope/source linkage.

**Next bounded Stage 1 unit:** complete the 3-row 1930s touring-team exhibition classification check using one coherent authoritative evidence family, verify stable IDs/game types/no duplicate game relationships and mandatory season accounting, run Stage 1 mechanical closeout; checkpoint precise terminal field debt and blocking residuals. If a genuine inclusion judgment remains unsafe, stop and preserve its exact row population rather than inventing an owner answer. Do **not** start Stage 2 without the subsequent owner `Proceed` at the Stage 1 boundary.

No workflows are running or awaited. No protected `main`, global basketball registry, canonical data, or published school data was mutated.
