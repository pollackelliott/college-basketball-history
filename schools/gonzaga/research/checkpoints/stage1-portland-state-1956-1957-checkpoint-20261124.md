# Gonzaga ALL_HISTORY_EXPANSION Stage 1 — Portland State complete series source census

## Authentication and bounded scope
- Protected main: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`
- Parent Gonzaga Research head: `7589d398143736993eb906ebd4b698ff1e744de5`
- Immutable research base: `f64ce23988faa04a304eb15d9ad96c2144ed5777`
- Scope: the Portland State all-time 27-game Gonzaga series and the complete Portland State 1956-57 institutional season result ledger; **one pre-1958 eligible appearance**.
- Status: Stage 1 ACTIVE; Stage 2 unauthorized.

## Original institutional sources
1. Portland State 2025-26 Men's Basketball Media Guide, all-time opponent series, official PDF: https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/pdx.sidearmsports.com/documents/2025/11/4/2025-26_Portland_State_Basketball_Media_Guide.pdf. Literal first Gonzaga appearance: **1956-57 — A — L — 63 — 75** (Portland State's perspective). It lists **27** total Gonzaga games; the *next* is 1964-65 and all 26 later entries fall in Gonzaga's inherited published 1958-59+ interval. Those entries are outside this expansion ledger.
2. Portland State 2023-24 Viking Basketball Record Book, original 1956-57 season-by-season table, official PDF: https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/pdx.sidearmsports.com/documents/2023/11/6/2324_record_book.pdf. Literal entry: **L | D.10 | at Gonzaga | 63-75** (Dec. 10, 1956, away from Portland State's perspective). The 1955-56 and 1957-58 original PSU season tables contain no Gonzaga entry.
3. Contemporary original United Press report in *Medford Mail Tribune*, **December 11, 1956, printed p. 11**, under 'PORTLAND STATE LOSES': Gonzaga defeated Portland State **75-63** the previous night, consistent with Dec. 10. https://oregonnews.uoregon.edu/lccn/sn97071090/1956-12-11/ed-1/seq-11/ocr/. The separate unrelated OCR score strip is visibly defective; the explicit article and both PSU institutional sources agree on result.

## Reconciliation and disposition
- **New identity**: `GONZAGA-EXP-PORTLANDSTATE-195657-001`; **1956-57** regular season, **1956-12-10**, Gonzaga **HOME W75-63** vs Portland State.
- HOME derives from the explicit institutional 'at Gonzaga' / PSU away notation, **not from Spokane geography**. Exact facility not established and not invented.
- Cross-checked the prior 551-game ledger: **0 Portland State rows**, **0 previously accepted matches**. One newly admitted row; **26 outside-expansion source appearances excluded** as inherited baseline.
- Full prior 551 rows, research IDs, scores, held candidates, and research decisions preserved without rewrite in immutable `stage1-identified-game-ledger-0029.csv`; new append-only ledger `stage1-identified-game-ledger-0030.csv` has **552 distinct games, 212 W / 340 L**.
- Gonzaga official expansion aggregate remains **477 W / 500 L, 977 games**. Arithmetic diagnostic becomes **977 - 552 = 425**; this number is **not** a count of individually established missing-game identities.
- Season **1956-57** identified moves from **8-11 / 19** to **9-11 / 20**, official season aggregate **11-16 / 27**; diagnostic difference from **8** to **7**.
- Six unadmitted candidate holds and four prior-accounting closeout debts remain unchanged. No independent historical-authority decision required now.
- No protected main, published package, shared global registry, Stage 2, Research Freeze, or Implementation mutation.

## Durable artifacts
- Controlling new ledger: `schools/gonzaga/research/checkpoints/stage1-identified-game-ledger-0030.csv`
- Controlling new status: `schools/gonzaga/research/checkpoints/stage1-status-0037.json`
- Original source audit: `schools/gonzaga/research/checkpoints/stage1-portland-state-1956-1957-source-audit-0001.json`
- One accepted source-backed row: `schools/gonzaga/research/checkpoints/stage1-portland-state-1956-1957-recovered-game-0001.csv`
- 1956-57 reconciliation: `schools/gonzaga/research/checkpoints/stage1-portland-state-1956-1957-reconciliation-0001.csv`

## Convergence / next unit
The official complete-series source was fully assessed; one addition justifies retaining its exact distinct identity, but there is **no rationale to retry the same PSU census**. For the next bounded unit, seek a *different, accessible* historically comprehensive official opponent record with material pre-1958 Gonzaga exposure, check source-family status first, and stop at a durable boundary. No Stage 2 authorization.
