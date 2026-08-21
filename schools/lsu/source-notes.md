# LSU source notes

## Primary source

**2025-26 LSU Men's Basketball Record Book**, LSU Athletics Communications, supplied by the owner. The year-by-year results ledger (printed pp. 83-93; PDF pp. 85-95) is the package backbone through 2024-25. The ledger was machine-extracted and season-by-season reconciled against all 117 printed season records: **0 season record mismatches** across **2,941 games**.

Internal cross-check sections used include SEC Tournament history, NCAA Tournament history, NIT history, overtime games, Maravich Center/facility history, and championship-team sections. Raw year-by-year strings are preserved in `raw_text`.

## 2025-26 supplement

LSU Athletics official completed 2025-26 schedule: https://lsusports.net/sports/mb/schedule/season/2025-26

The official schedule supplies 32 competitive games (15-17), site classification, modern venues, and overtime values. The Oct. 26, 2025 exhibition at UCF is excluded.

## Conference sources

LSU Libraries Special Collections, Athletic Department Records historical note: LSU joined SIAA in 1896, Southern Conference in 1922, and SEC as a charter member after its establishment.
https://www.lib.lsu.edu/sites/default/files/sc/findaid/a0050_athleticdepartmentrecords.pdf

## Venue sources

LSU Athletics, Pete Maravich Assembly Center / Men's Basketball Facilities:
https://lsusports.net/facilities/maravich-center

LSU Academic Center for Student-Athletes, building history (Gym/Armory / current Cox Academic Center):
https://acsa.lsu.edu/sports/2013/11/9/history.aspx

The sources establish that the Gym/Armory and Huey Long Field House should not be assumed to be one physical venue even though some LSU basketball copy conflates the names. The 1938 SEC Tournament is explicitly identified by LSU as being at Huey Long Field House.

## Accomplishment sources

The LSU record book's postseason and championship sections establish 24 NCAA appearances, four Final Fours (1953, 1981, 1986, 2006), and the program's SEC championship history. LSU Athletics' SEC Championships history lists men's basketball regular-season titles in 1935, 1953, 1954, 1979, 1981, 1985, 1991, 2000, 2006, 2009, and 2019. LSU's dedicated SEC Tournament history identifies the single tournament championship in 1980.

## Exact-date unknowns

Five source rows still lack a complete exact date in the year-by-year ledger; none is invented. The originally undated 1915-16 Ole Miss 55-29 LSU win is dated 1916-02-21 from Ole Miss official reciprocal evidence; the remaining five stay unknown unless later authoritative evidence resolves them.

## Reciprocal-source checks used in final package QA

Already-onboarded official school ledgers were used only where they resolved a concrete defect in LSU's own structured row while preserving LSU's raw claim. Ole Miss supplies the exact date 1916-02-21 for LSU's 55-29 road win. Alabama supplies the reciprocal 82-70 score for its 1957-02-18 home win over LSU, resolving LSU's internally inconsistent raw `L, 70-62` line.

## Source-specific normalization

The 2024-25 year-by-year ledger line for the Nov. 14 Kansas State game contains `at Kansas St.` but also an `H` marker. LSU's official season schedule establishes the game as away; curated site type uses road while preserving the contradictory raw ledger line.

Historical abbreviations and OCR variants are preserved in `source_opponent_label` and normalized in `opponents.csv`. Historical clubs, military teams, schools no longer in Division I, and non-collegiate opponents are retained as distinct identities rather than forced into current-D1 programs.

## Owner-supplied conference tournament site reference — 2026-08-21
`Conference_Tournament_Site_Reference(3).xlsm` is not treated as universal canon because the workbook is still under construction. The owner explicitly authorized the completed SIAA, SoCon, and SEC sections for LSU's full conference-tournament history. It supplies the targeted venue corrections/additions applied in this frozen package. No unfinished conference section was used.

### LSU Athletics — UCF, November 24, 2024

LSU Athletics official contemporary game evidence establishes that the
November 24, 2024 Greenbrier Tip-Off opponent was UCF, not Florida.

Result: LSU 109, UCF 102 (3OT)
Site: White Sulphur Springs, WV
Event: Greenbrier Tip-Off

Official recap:
https://lsusports.net/news/2024/11/24/lsu-rallies-wins-109-102-in-3ot-at-greenbriar-tip-off-vs-ucf/

Used to normalize the malformed year-by-year source token `UF` to UCF.
The original source label and raw media-guide text remain preserved.
