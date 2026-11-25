# Boise State ALL_HISTORY_EXPANSION — Stage 1 Eastern Oregon / College of Idaho newspaper checkpoint 0006

**Status: STAGE_1_IN_PROGRESS.** This is the existing independent Boise State Research lane. No Stage 2, Implementation, owner gate, protected-main mutation or shared/global reference mutation is authorized.

## Immutable Research authority and checkpoint lineage

- Protected main authenticated at unit start: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`.
- Immutable `research_base_sha`: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`.
- Parent 0005 checkpoint ZIP SHA-256: `a7c52861d0236b8f6d13da70a64e5618461f52c8145600a17f79fd6f40386f67`.
- New portable ZIP: `boise-state-expansion-stage1-eastern-oregon-0006.zip`.
- New ZIP SHA-256: `1c14e70caee9c65015f476258ae338785f9a784cf54553eaaafdc9d06e3ac629`.
- New ZIP full 16-column ledger member SHA-256: `f4c67b9e1e01a5b43f42ea2ab5958e01ba4ec10c17280a04914883c658ea6453`.
- New ZIP full member checksum manifest: `manifest.json`. Includes 120-row structured ledger, 21-row source delta, original-source inventory, 38-season census, 33-season accounting + three unlisted candidates, residuals, status.
- Committed Research branch mirrors: `stage1-eastern-oregon-0006-ledger.csv` (120 compact rows), `...-accounting.csv` (38 rows), `...-evidence.csv` (21 game-specific publication/source URLs), `...-season-census.csv` (38 rows). The portable ZIP preserves fuller raw source snippets, uncertainty and source identity and is the complete transport artifact.

## Bounded systematic first-party contemporary newspaper source family

Used the University of Oregon Historic Oregon Newspapers digitization of `La Grande Evening Observer`, with one `Albany Democrat-Herald` corroborating report, over coherent Eastern Oregon–Boise series and a College of Idaho doubleheader.

**21 previously unidentified source-backed competitive game rows (Boise 10 W / 11 L)**:

| Season | Added | Boise W-L | Opponents / evidence |
|---|---:|---:|---|
| 1939-40 | 4 | 3-1 | Eastern Oregon two games incl Boise W49-40 Feb 22; College of Idaho two consecutive Boise wins incl W47-37 Feb 20 |
| 1942-43 | 3 | 0-3 | Eastern Oregon L45-50 Jan 6, L36-63 Feb 26, L42-53 Feb 27 |
| 1945-46 | 4 | 2-2 | Two January and two February Eastern Oregon games incl W52-48 Jan 25 and W46-40 Feb 11 |
| 1947-48 | 4 | 1-3 | Entire Eastern Oregon series Jan 2 (W58-49), Jan 3 (L55-56), Jan 30 (L57-67), Jan 31 (L51-53); newspaper independently states EOC season-series advantage 3-1 |
| 1948-49 | 2 | 1-1 | Eastern Oregon Mar 11 L73-76 and Mar 12 W57-33 |
| 1949-50 | 4 | 3-1 | Eastern Oregon Dec 9 W score unknown, Dec 10 L38-45, Jan 16 W62-54, Jan 17 W with EOC 34 points and Boise score unknown |

The complete new row citations, publication date, source URL, explicit score status, and uncertainty classification are in the Research branch `stage1-eastern-oregon-0006-evidence.csv` and ZIP `stage1-0006-source-delta.csv`.

Examples:
- 1940 Feb 23 article documents Boise 49-40 Eastern Oregon and references the earlier loss: https://oregonnews.uoregon.edu/lccn/2006260039/1940-02-23/ed-1/seq-6/ocr/
- 1948 Feb 2 article gives Eastern Oregon 53-51 Boise and says Eastern Oregon won 3 of 4 games: https://oregonnews.uoregon.edu/lccn/2026234413/1948-02-02/ed-1/seq-8/ocr/
- 1949 Dec 12 article preserves a one-apiece weekend series: https://oregonnews.uoregon.edu/lccn/2026234413/1949-12-12/ed-1/seq-8/ocr/
- 1950 Jan 20 report identifies EOC 34 points in the Tuesday loss but Boise final score unknown: https://oregonnews.uoregon.edu/lccn/2026234413/1950-01-20/ed-1/seq-8/ocr/

## Evidence boundaries / unresolved details

- Six of the new 21 games have incomplete final scores: five entire scores unknown; Jan 17 1950 has only Eastern Oregon's 34 points verified. Do not manufacture other points.
- One of February 1946's Eastern Oregon rematches is **dated only within the series**; date remains blank. Other dates based on direct newspaper relative weekday or retrospective series logic are labeled as derived.
- All 21 H/A/N values remain `UNKNOWN`, even where original articles establish geographic locality; never infer H/A/N from place alone.
- For Saturday Jan 31, 1948, primary newspaper body and box score establish **EOC 53-51**, not 63-51 that one derived preview/rough OCR appeared to suggest. Retain precise source.
- Early College of Idaho games are distinct from Eastern Oregon games and any Boise published baseline. No duplicate identification with existing 99 rows.

## Updated exact arithmetic

- Previous 0005: 99 identified supplemental games (44 junior-college, 55 1968-69/1969-70).
- Current 0006: **120** unique supplemental game identities (65 junior-college, 55 1968-69/1969-70). All original 99 preserved byte-for-byte as parsed CSV rows in portable ledger.
- Official MW 33 junior-college seasons: 441 W / 346 L = 787 aggregate games. Exactly **64** identified in these 33 seasons; 787 minus 64 = **723 aggregate-unmatched**. This is an accounting diagnostic, not 723 invented game identities.
- One separately documented 1937-38 Boise JC loss remains outside the 33-season MW annual record; do not misallocate it.
- Protected `main` and the 1,670-row accepted published Boise State 1970-71+ package remain entirely untouched.
- Stage 1 remains OPEN; preserved inception, missing 1938-39 annual record, conflicting 1950s season records and lower-level postseason site residuals remain unresolved.

## Next bounded unit

Seek another multi-season coherent contemporary newspaper or primary opponent ledger family, preferring whole-series season-first recovery and excluding previously captured identities, or stop with exact raw source limits. Do not proceed to Stage 2 or request owner authority absent an authentic unresolved owner decision.
