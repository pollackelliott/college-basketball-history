# Gonzaga ALL_HISTORY_EXPANSION Stage 1 — Pacific Lutheran 1953/1957 original postseason results tranche

## Authority
- Protected main: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`
- Parent Research HEAD: `91954d474af284b3ac958065aa800e18c105f759`
- Immutable research base: `f64ce23988faa04a304eb15d9ad96c2144ed5777`
- Scope: one bounded Pacific Lutheran official overall-series assessment and 1953/1957 directly scored original NAIA postseason reports; **not** a complete re-extraction of 1938-1960.
- Stage 1 ACTIVE, Stage 2 unauthorized.

## Institution-level series source and deduplication
PLU's official all-time men's basketball series summary (https://golutes.com/sports/2018/5/10/mens-basketball-series-history) states **Gonzaga (Wash.) 7-9, first 1938-39, last 1959-60**, a total of **16** PLU-side appearances. This is aggregate series metadata, *not* 16 rows of game-by-game results. Prior controlling Gonzaga ledger 0030 had **five** PLU rows (1946-47 W56-37, 1947-48 W53-29 NAIB, 1955-56 two postseason losses, 1957-58 W58-57), all preserved exactly. Current three original-result admissions bring the **identified PLU subset to eight**, but 16-8 **does not** justify eight new synthetic games: the series spans into inherited 1958-59+ and many dates/results are not visible.

## Three newly established competitive postseason games
1. `GONZAGA-EXP-PLU-195253-001`: **1952-53, Gonzaga W71-67 (OT), POSTSEASON**, exact played date **UNKNOWN**, site **UNKNOWN**. The March 5, 1953 *Medford Mail Tribune* original p10 lists 'Washington NAIA Tourney / Gonzaga 71, Pacific Lutheran 67, overtime (championship)' (https://oregonnews.uoregon.edu/lccn/sn97071090/1953-03-05/ed-1/seq-10/ocr/). Original report establishes a played district championship, but the next-day issue does not explicitly date this precise final; do not assign March 4 without proof.
2. `GONZAGA-EXP-PLU-195657-001`: **1957-03-04, Gonzaga L 68–UNKNOWN vs Pacific Lutheran, POSTSEASON, HOME**. The March 5 *Oregon Statesman* original AP story on printed p9 (PDF screenshot actually inspected, https://oregonnews.uoregon.edu/lccn/sn85042470/1957-03-05/ed-1/seq-9.pdf) directly dates the game March 4, calls Gonzaga the **host**, and explicitly describes the District 1 NAIA best-of-three playoff series. It prints **PLU 78–Gonzaga 68**, while the independently printed March 5 *Albany Democrat-Herald* p10 (PDF screenshot actually inspected, https://oregonnews.uoregon.edu/lccn/sn96088460/1957-03-05/ed-1/seq-10.pdf) lists **PLU 72–Gonzaga 68**. Gonzaga's 68 and the loss are stable; **PLU score remains UNKNOWN**. No forced arithmetic selection.
3. `GONZAGA-EXP-PLU-195657-002`: **1957-03-05, Gonzaga L85-93, POSTSEASON, site UNKNOWN**. The March 6 *Medford Mail Tribune* p8 United Press section explicitly labels the results **Tuesday College Games** and prints PLU 93, Gonzaga 85 (https://oregonnews.uoregon.edu/lccn/sn97071090/1957-03-06/ed-1/seq-8/ocr/); March 6 *Albany Democrat-Herald* p11 independently reproduces the 93-85 NAIA playoff score (https://oregonnews.uoregon.edu/lccn/sn96088460/1957-03-06/ed-1/seq-11.pdf). This is the **second** match in the series announced in the Mar 5 AP first-game report and is not a duplicate of the Mar 4 score. No explicit source establishes site classification for second contest; no inferred HOME merely because the first was at Gonzaga.

All three are regular varsity competitive NAIA lower-level postseason games, **POSTSEASON**, not top-level D-I conference tournaments. No facility invented.

## Residual source limitation
- PLU official full series **16 games aggregate**, not a fully published original date-scored opponent ledger.
- First-party PLU historical season W-L and player records (https://golutes.com/sports/2018/5/9/mens-basketball-year-by-year-records.aspx) do not supply complete individual Gonzaga scores.
- A secondary 1955 Washington NAIA bracket snippet (https://college-sports.fandom.com/wiki/1955_NAIA_Men%27s_Basketball_District_Regionals) was encountered but **did not meet new individual-game admission requirements** from direct original played evidence. No 1955 row, pseudo-ID, or new source hold created; no claim of zero 1955 matches.
- There are no new inclusion/duplicate contradictions. The 1957-03-04 opponent-point conflict is explicit nonblocking **field uncertainty**, not a reason to reject the proved game.

## Numerical reconciliation and preservation
- Controlling old ledger `schools/gonzaga/research/checkpoints/stage1-identified-game-ledger-0030.csv`: **552 rows, 212W/340L**. Preserved without rewrite; all 552 rows carried in exact order into new `schools/gonzaga/research/checkpoints/stage1-identified-game-ledger-0031.csv`.
- New controlling ledger: **555 unique rows, 213W/342L**, three new PLU competitive identities, known outcomes on all.
- 1952-53: **10-11 / 21** to **11-11 / 22**; official **15-14/29**; arithmetic difference **8** to **7**.
- 1956-57: **9-11 / 20** to **9-13 / 22**; official **11-16/27**; arithmetic difference **7** to **5**.
- Official Gonzaga 51-season aggregate **477W/500L / 977** unchanged. Numeric 977-555 **=422**, which is **NOT 422 individually established missing-game identities**.
- Six previously held candidates, four parked accounting contradictions, 1907-08 inception authority and inherited 1958-59+ published baseline unchanged.
- No protected main, shared/global reference, canonical/public package, Research Freeze, owner gate, Stage 2 or Implementation mutations.

## Durable files
- New status: `schools/gonzaga/research/checkpoints/stage1-status-0039.json`
- New complete append-only ledger: `schools/gonzaga/research/checkpoints/stage1-identified-game-ledger-0031.csv`
- PLU source audit: `schools/gonzaga/research/checkpoints/stage1-pacific-lutheran-1938-1960-partial-series-audit-0001.json`
- Exact three-row original-result tranche: `schools/gonzaga/research/checkpoints/stage1-pacific-lutheran-1953-1957-postseason-tranche-0001.csv`
- Affected season reconciliation: `schools/gonzaga/research/checkpoints/stage1-pacific-lutheran-1953-1957-reconciliation-0001.csv`

## Next bounded unit
Another materially distinct first-party systematic historical scorebook, with readable individual game evidence and existing source-family status checked first, is preferred to prolonging PLU single-game searches. The PLU summary source has been exhausted as a **summary**, not certified as a fully reconstructed 16-game historical game series. No owner decision is needed for the current safely identified rows or source-scored field conflict.
