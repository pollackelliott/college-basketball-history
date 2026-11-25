# Boise State ALL_HISTORY_EXPANSION — Stage 1 West-region newspaper checkpoint 0007

**Status: STAGE_1_IN_PROGRESS.** Same Boise State Research lane only, no Stage 2, Implementation, protected-main or shared reference mutation.

## Immutable authority and portable checkpoint
- Current protected main at beginning of tranche: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`.
- Immutable `research_base_sha`: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`.
- Parent 0006 ZIP SHA-256: `1c14e70caee9c65015f476258ae338785f9a784cf54553eaaafdc9d06e3ac629`.
- New portable archive: `boise-state-expansion-stage1-west-scoreboards-0007.zip`.
- Verified ZIP SHA-256: `630b00f6eb66716a6f7616e152542c4b443d11b6022ab712e37a48ecfbacc3c0`.
- Full 16-column ZIP structured ledger member SHA-256: `a62c60b503f948e42a211f3f2959f973929eabe291b3478bd72fc014e6fceb37`.
- ZIP manifest contains all member hashes; includes 128-row ledger, full 38-season accounting/census, residuals, original-source inventory, eight-game evidence delta and separate one-row field-repair evidence.
- Committed Research branch mirrors: `stage1-west-scoreboards-0007-ledger.csv`, `stage1-west-scoreboards-0007-accounting.csv`, `stage1-west-scoreboards-0007-season-census.csv`, `stage1-west-scoreboards-0007-evidence.csv`, `stage1-west-scoreboards-0007-field-repairs.csv`. The ZIP contains richer source evidence and is the complete portability checkpoint.

## Bounded systematic historical source-family continuation

One 1930s-1950s Northwest college newspaper scoreboard collection, principally University of Oregon Historic Oregon Newspapers digitized *La Grande Evening Observer*, *Oregon Statesman*, *Eugene Register-Guard*, *Medford Mail Tribune* and *Albany Democrat-Herald*. Eight distinct newly identified games (Boise 5-3):

| Season | Opponent literal | Boise W/L and score | Temporal evidence |
| --- | --- | --- | --- |
| 1949-50 | College of Idaho | L 44-56 | Dec 31 1949 scoreboard, actual date unverified |
| 1949-50 | Southern Idaho | W 56-46 | Feb 9 1950 scoreboard, Feb 8 game date inferred |
| 1950-51 | College of Idaho | L 59–? | Jan 17 1951 Oregon Statesman; OCR opponent score 'C7', not verified; Jan 16 inferred |
| 1951-52 | College of Idaho | W 69-50 | Dec 13 1951 Register-Guard, Dec 12 inferred |
| 1952-53 | Northwest Nazarene College | W 74-71 | Dec 17 1952 Mail Tribune, Tuesday Dec 16 |
| 1955-56 | Oregon Tech | W 70-56 | Mar 14 1956 Albany Democrat-Herald, NJCAA Region 1 championship Tue Mar 13, Cedar City, UT |
| 1956-57 | University of Idaho freshmen (Idaho Frosh) | L 53-64 | Dec 16 1956 Mail Tribune, Friday Dec 14 college results |
| 1956-57 | College of Idaho | W 51-43 | Dec 23 1956 Mail Tribune, game date not certain |

All eight new rows have H/A/N UNKNOWN. The Southern Idaho literal must not be incorrectly identified with the later-founded College of Southern Idaho. The University of Idaho freshman opponent is distinct from Idaho varsity; no false opponent merge. NJCAA Region 1 championship is generic lower-level postseason; Cedar City locality is not a physical-venue or site-type assertion.

### Exact evidence-based repair, no new game ID
The original 0006 row `BOISE-EXP-S1-ORE-1949-001` identifies Boise's December 9 1949 victory against Eastern Oregon but had unknown points. *La Grande Evening Observer* December 10 1949 p.8 features the complete original game box score and headline Boise W 48-45. Preserve the prior game ID and date, change only source-corroborated score and source provenance/uncertainty. Source: https://oregonnews.uoregon.edu/lccn/2026234413/1949-12-10/ed-1/seq-10.pdf . The remaining 119 prior rows retain their entire 16-column parsed contents unchanged.

The authoritative per-game source URLs, raw snippets, issue dates, and score/date uncertainty are preserved in `stage1-0007-source-delta.csv` in ZIP and `stage1-west-scoreboards-0007-evidence.csv` on this branch. Do not count football scoreboards (e.g. 57-0) or high-school Boise references as basketball, and do not invent game IDs from scoreless Mountain Home Air service-team mentions.

## Updated exact population
- Prior 0006: 120 identified supplemental games (65 junior-college incl one 1937-38 unlisted-season game; 55 1968-69/1969-70).
- Now 0007: **128** unique identified supplemental games (73 junior-college, 55 1968-69/1969-70).
- Official MW 33-season junior-college W/L remains **441-346 (787)**. **72** identifiable competitive game rows now in these 33 listed seasons; aggregate-minus-identified **715**, held as season-level historical coverage debt, NOT manufactured unidentified game rows nor automatic proof same inclusion definitions apply.
- Separate NNC 1937-38 Boise loss remains source-backed outside 33 listed MW seasons and **outside 715 arithmetic**. 1932-33 inception classification, 1938-39 no-team question, 1950s authoritative aggregate conflicts, score unknowns, and site obligations remain explicit residuals.
- Protected main and 1,670 inherited 1970-71+ accepted Boise published game rows remain untouched.

## Next bounded unit
Seek next coherent primary-source family capable of recovering larger multi-season game blocks or detailed first-party varsity season ledger; use whole-season census and nonduplicate checks. Do not pivot to Stage 2 or open an owner gate on `Proceed`. The 715 coverage debt is not yet eligible for invented game rows or a premature closing assertion.
