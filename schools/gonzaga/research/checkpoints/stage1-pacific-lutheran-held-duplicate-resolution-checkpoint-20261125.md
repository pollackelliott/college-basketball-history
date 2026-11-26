# Gonzaga Stage 1 checkpoint 0047 — Pacific Lutheran 1957 candidate deduplication

**Protected main:** `9888bc6161952199e6f49c5f2b614459a44f029d`  
**Parent Gonzaga Research HEAD:** `b996f2baaf24bb94e9461c66877bc06e7855acb3`  
**Immutable Research base:** `f64ce23988faa04a304eb15d9ad96c2144ed5777`

## Finding: exact historical duplicate of accepted game, not another game

Candidate `GONZAGA-HOLD-5657-PLU-001` from immutable `stage1-1955-1958-pacific-northwest-held-candidates-0001.csv` reported **March 5, 1957**, Gonzaga **L 85–93** against **Pacific Lutheran**, with unresolved classification when the candidate was first parked.

It is identical in season, exact date, opponent, played W/L and BOTH scores to the already accepted `GONZAGA-EXP-PLU-195657-002` in controlling 558-row ledger `stage1-identified-game-ledger-0034.csv`. That accepted source-game row is explicitly **POSTSEASON**, the **second game** of the 1957 Pacific Lutheran–Gonzaga NAIA District 1 best-of-three playoff. There is no basis for a *third* March 5 game.

[March 6, 1957 Medford Mail Tribune original Tuesday college results](https://oregonnews.uoregon.edu/lccn/sn97071090/1957-03-06/ed-1/seq-8/ocr/) directly gives Pacific Lutheran 93 Gonzaga 85. The [March 6 original Albany Democrat-Herald p.11](https://oregonnews.uoregon.edu/lccn/sn96088460/1957-03-06/ed-1/seq-11.pdf), screenshot-checked for this unit, independently prints the same result. The original [March 5 Oregon Statesman p.9](https://oregonnews.uoregon.edu/lccn/sn85042470/1957-03-05/ed-1/seq-9.pdf) had previously documented March 4 as the series opener and next contest Tuesday (March 5).

The March 4 accepted first game remains `GONZAGA-EXP-PLU-195657-001`, Gonzaga **L 68–UNKNOWN** with Pacific Lutheran score disagreement **72 versus 78** deliberately unresolved. The March 5 accepted second game remains **L 85–93** and site_type **UNKNOWN**, not inferred from the previous day's explicit Gonzaga hosting. Preserve both separate accepted games as-is.

## Hold disposition and population arithmetic

Historical candidate files, existing source tranches and the accepted game ledger are immutable and unchanged. The six prior hold records remain archived; **one candidate changes current accounting status from ACTIVE to RESOLVED_ALREADY_ACCEPTED**, via new audit and explicit six-row status crosswalk.

| Population | Before | After |
|---|---:|---:|
| Accepted unique Gonzaga competitive games | 558 | **558** |
| Accepted W–L | 215–343 | **215–343** |
| Official 51-season games minus accepted-game identities (arithmetic only) | 419 | **419** |
| Historically recorded held candidates | 6 | **6** |
| Active **unadmitted** candidate holds | 6 | **5** |
| 1942–43 active holds | 4 | **4** |
| 1926 date-collision active hold | 1 | **1** |
| March 1957 Pacific Lutheran active hold | 1 | **0 (resolved duplicate)** |
| Historical accounting contradictions that still block Stage 1 closeout | 4 | **4** |

The four closeout-blocking accounting seasons remain **1915–16, 1930–31, 1936–37 and 1937–38**. The season-level underidentification population also remains 46 seasons. Stage 1 stays **ACTIVE**; Stage 2 **NOT AUTHORIZED**; no owner gate needed.

## Narrow next unit, not yet executed

Test only the **January 18, 1926 Portland Coliseum Checkerboards 30–29 / 30–20 report** held against the already accepted Gonzaga–Washington **L 12–35** on that date. Determine whether the primary date is wrong, whether played games are distinct or whether no sound resolution exists. Do not manufacture same-evening dual-city appearances or restart broader source research.

Audit: `stage1-pacific-lutheran-1957-03-05-held-candidate-identity-reconciliation-0001.json`.
Current six-record disposition inventory: `stage1-six-historical-hold-current-disposition-0001.csv`.
