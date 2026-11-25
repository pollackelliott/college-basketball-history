# Boise State ALL_HISTORY_EXPANSION — Stage 1 initial checkpoint 0001

**Status:** STAGE_1_IN_PROGRESS. Neither Research Frozen nor Implementation; this branch must never merge as basketball data without the governed lifecycle.

## Immutable authority
- research_base_sha: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`
- target: `boise-state`; baseline: `LEGACY_TOP_LEVEL_ONLY`; top-level scope: `1970-71+`.
- inherited package: `schools/boise-state/` six files on research-base commit; accepted 1,670 source-game rows (1970-71 through 2025-26). All inherited source games remain OUT of supplemental Stage 1 ledger.
- official source: Boise State Men's Basketball Record Book, updated October 1, 2024, Year-by-Year Results printed page 33; guide actual results cutoff **2023-24**, not its printed date. PDF SHA-256 `8b34953c78f46750cf53457874783c36b2f364eb4eb9be14e8310e8842b0da29`.
- separate baseline required completed-season cutoff **2025-26**; expansion target ends **1969-70**.

## Inception assessment — provisional
The Boise State Athletics *Men's Basketball Tradition* identifies **1933 junior-college** basketball and gives **441-346 (1933-1968)** for its junior-college era. Boise State University Archives' official timeline dates the basketball program to **December 1, 1932**. First candidate season is **1932-33**, subject to direct confirmation of its season-specific game records; **1933-34 remains a live alternative** until the calendar-year/inaugural-season difference is resolved. The 1968-69 four-year/NAIA start is NOT institutional inception.

Sources:
- https://broncosports.com/sports/2018/5/18/sports-m-baskbl-spec-rel-bosu-m_baskbl_tradition_html (if redirect fails, use canonical URL below)
- https://broncosports.com/sports/2018/5/18/sports-m-baskbl-spec-rel-bosu-m-baskbl-tradition-html
- https://www.boisestate.edu/archives/university-archives/the-boise-state-story/timelines/
- https://scholarworks.boisestate.edu/uni_books/7/ (University-published athletics history, downloadable chapters returned 403 during first bounded pass; NOT analyzed)

## Stage 1 systematic source-first result
- **1968-69: 27 competitive games, 19-8; H 10-1, A 8-7, N 1-0**.
- **1969-70: 28 competitive games, 20-8; H 11-1, A 8-6, N 1-1**.
- **55 identified competitive supplemental games** (39-16), 50 REGULAR_SEASON and five lower-level POSTSEASON. All have official source date/opponent/result/score/site token. H/A/N translated from the guide's explicit LOC column, never geography.
- The 1968-69 guide year summary says NAIA **(0-2)** while three ^-marked competitive games in its actual game schedule are Southern Oregon W, Linfield L, Linfield L. Preserve all three; interpretation of NAIA aggregate remains open.
- 1969-70 includes two ^ NCAA Division II Tournament games; these are lower-level `POSTSEASON` under expansion taxonomy.

The source-backed 1933-1968 junior-college aggregate is **441-346 (787 games)**, not 787 identified rows. **1932-33 through 1967-68 are 36 candidate seasons with season activity and games NOT YET reconstructed**; do not infer all were active or count aggregate games as identified.

## Durable transport
- local initial checkpoint: `boise-state-expansion-stage1-initial-0001.zip`.
- exact ZIP SHA-256: `888533cc13e3d9a9aa4bb277225ce332d1f7cbfeaa2d445011efd641d92ed259`.
- ZIP members: `manifest.json`, `structured-stage1-ledger.csv` (55 rows with raw source snippets), `season-census.csv` (38 candidate seasons), `residuals.csv`, `source-inventory.md`.
- member SHA-256: ledger `c034c8bbb5584b9e2697f2d976dcbd98b9e9486cd020584a4787aef6ae8b0ed4`, census `0c983b155efabaa74f1e27d9db512e89dba1201ea07074d8dc4a5d35100d1ee8`, residuals `a96b137b4b0b1ca18513d54082898a633bac6d4d12d0609bdd95c367645d1088`, inventory `f184641242704c4fd97b6ffdd134df95019ecd29e19a5f22bee3b0708722a6b0`.

## Next bounded Stage 1 tranche
Verify inception by contemporaneous Boise Junior College evidence; construct 1930s season-first source ledger and account for possible hiatus seasons. Then process other junior-college eras in coherent multi-season blocks. This initial checkpoint is **not Stage 1 COMPLETE** and makes no owner-gate request. No branch mutation to protected main; no shared references touched.
