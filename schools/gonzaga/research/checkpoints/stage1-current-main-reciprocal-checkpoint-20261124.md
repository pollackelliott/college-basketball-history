# Gonzaga Stage 1 — current-main reciprocal season-first bulk checkpoint (2026-11-24)

parent_research_head: 021547a13948c492e4eaeac1702c61444e547000
authenticated_protected_main: 17e61efd0786671df593859c2b73f720217cef1e
research_base_sha: f64ce23988faa04a304eb15d9ad96c2144ed5777
stage: STAGE_1
stage1_complete: false
stage2_authorized: false

## Change in bulk evidence mode

The 1944-46 indexed Oregon newspapers had diminished to three clean additions. This bounded unit used a different systematic evidence corpus: the repository's accepted **published school reciprocal source-game tables**, scanning many programs together across the still-unpublished Gonzaga seasons. A contemporaneous College of Puget Sound student newspaper supplied one separate directly documented 1946-47 series game.

The published packages were read at exact protected-main SHA 17e61efd0786671df593859c2b73f720217cef1e. Existing complete Gonzaga opponent-family work was used for deduplication, not reopened.

## Accepted results

- previous identified-game ledger: **479**
- source-backed new game identities: **10**
- successor identified-game ledger: **489**
- known on-court results: **489**
- authoritative official expansion aggregate: **477-500 / 977**
- aggregate-minus-identified arithmetic diagnostic: **488** (not 488 missing games)
- new exact-date collisions: **0**
- same-season/same-opponent/same-score or exact-date duplicate signals: **0**
- new over-official W/L season contradictions: **0**

Nine rows come from the original published reciprocal source-games.csv institutional rows: Missouri 1941-42 (one), Colorado State 1950-51 (two), Utah State 1952-53 and 1955-56 (four total), DePaul 1952-53 (one), and Creighton 1954-55 (one). Every row preserves the exact protected-main source-game ID, source blob, source-page and original literal.

One 1946-47 College of Puget Sound game is admitted only with a W and an otherwise unknown score/date: the February 6, 1947 issue of *The Trail* reports Puget Sound's 30-28 win **evened its two-game season series** with Gonzaga. The 30-28 defeat already has its own Gonzaga research ID `GONZAGA-EXP-SF4147-017`; the other played game was therefore a separate Gonzaga win. Neither the winning game's score nor its date is copied or invented.

## Six-season reconciliation

| Season | Official | Identified after tranche | Arithmetic diagnostic |
|---|---:|---:|---:|
| 1941-42 | 16-13 / 29 | 5-11 / 16 | 13 |
| 1946-47 | 20-9 / 29 | 9-7 / 16 | 13 |
| 1950-51 | 8-22 / 30 | 6-10 / 16 | 14 |
| 1952-53 | 15-14 / 29 | 10-11 / 21 | 8 |
| 1954-55 | 16-13 / 29 | 13-11 / 24 | 5 |
| 1955-56 | 13-15 / 28 | 6-11 / 17 | 11 |

The arithmetic differences are coverage diagnostics only. No source-unacknowledged anonymous rows are created.

## Conservatism and limits

The row-level game_type remains `REGULAR_SEASON`. Gonzaga site_type is translated only where the institutional reciprocal record itself documented HOME / OPPONENT_HOME / NEUTRAL. Utah State original source has unknown site, which remains `UNKNOWN`. Puget Sound's earlier win is recorded with both exact date and scores blank rather than guessing.

Several very large published packages could not be read through the available connector response and are **NOT** classified as no-match. The Gonzaga digital Bulletin/Spires collection exists but could not be reliably read in this interface; it likewise is not negative historical evidence. The previous PDF WCC source rejection remains untouched.

The previous four parked research-exhausted accounting contradictions (1915-16, 1930-31, 1936-37, 1937-38) remain unchanged; the separate four 1942-43 held candidates remain unchanged. There are no new active discrepancy-research blockers from the accepted additions.

## Next bounded Stage 1 unit

Continue `SEASON_FIRST_BULK_RECONSTRUCTION` against this 489-row ledger. Prefer a **new readable systematic source corpus** for the still-high-gap 1941-47 and 1950s populations, with the existing published reciprocal corpus and source-limit record used to avoid repetition. Never elevate the accounting diagnostic into a count of missing canonical games. Preserve the 1942-43 wartime candidates as their own bounded inclusion/season-accounting classification unit. Do not begin Stage 2.
