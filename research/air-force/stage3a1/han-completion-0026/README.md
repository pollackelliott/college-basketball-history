# Air Force — Stage 3A-1 H/A/N COMPLETE — checkpoint 0026

This is the **same Research lane**, continuing from authenticated Stage 3A-0 COMPLETE checkpoint 0025 and the unchanged immutable Research base `3f5a15458aa468347e56e669327d6fe4c9c6ee69`.

## Exact census and bounded class research

All 27 Stage 3A-0 UNKNOWN regular-season H/A/N rows are from 1982–83; the older official Air Force 2010–11 result book controls that original 27-game universe. The newer guide's transposed entries are retained as historical contradictions, not accepted new games.

The 27 constitute a **single coherent historical season/source-notation class**, not 27 independent opponent investigations. Official reciprocal school packages and institutional histories establish 21 exact non-neutral venue classifications, and contemporary tournament event reporting establishes one neutral Lafayette consolation. The established source-specific uppercase/mixed-case house style, corroborated against those exact-game site outcomes, resolves the last five systematic rows (USIU twice, Doane, UW-Stevens Point, and Feb. 14 UTEP). Those five remain individually marked `SEASON_SOURCE_NOTATION` in the 27-row evidence audit; do not incorrectly assert that each has a separate first-party exact-game venue source. Geography was not used as an H/A/N classifier.

**H/A/N accepted:** 14 HOME; 12 AWAY (normalized `OPPONENT_HOME`); 1 NEUTRAL. Final regular season population: **972 HOME + 778 OPPONENT_HOME + 116 NEUTRAL + 0 UNKNOWN = 1,866**. Modern neutral 48, historical neutral 68. Postseason 62 unchanged; full games 1,928, stable IDs preserved.

## Durable files and preservation

- `structured-stage3a1-ledger.csv`: complete 1,928-game cumulative H/A/N state. The only changes to original 28 Stage3A0 columns are `han` and `site_type` on the exact 27 listed 1982–83 rows. The original established `AWAY` spelling is preserved in the CSV, while `OPPONENT_HOME` is the normalized downstream category.
- `stage3a1-han-adjudications.csv`: the exact 27-row source/score/classification/provenance inventory.
- `stage3a1-season-notation-calibration.json` and `stage3a1-contradiction-dispositions.json`: source-class evidence and explicit no-reopen conflict decisions.
- `stage3a1-status.json` and `stage3a1-researched-unresolved.json`: terminal status, zero residual.
- `stage3a2-home-queue.json`, `stage3a0-opponent-home-queue.json`, `stage3a3-neutral-queue.json`, `stage3a3-modern-neutral-queue.json`, `stage3a3-historical-neutral-queue.json`, `stage3a1-unknown-han-queue.json`: exact updated Stage3A1 downstream queues.
- `stage3b-postseason-handoff.json` is carried **byte-exact** from Stage 3A-0 (62 games).
- `stage4-authoring/opponents.csv` and `institutional-scope.json` are carried **byte-exact** from accepted Stage 2/3A-0.

Stage 3A-1 does **not** research exact HOME venues or NEUTRAL buildings. Those obligations belong to owner-authorized Stage 3A-2 and Stage 3A-3, respectively. The historical 1982–83 Lafayette neutral locality Hartford, CT was already accepted and remains preserved without new venue research.

## Authority and stop boundary

- Source Stage 3A-0 promotion branch commit: `1a8fe27b194bd9986224fe4b0d7655a1c0019c1a`; [checkpoint 0025](https://github.com/pollackelliott/college-basketball-history/tree/1a8fe27b194bd9986224fe4b0d7655a1c0019c1a/research/air-force/stage3a0/census-0025).
- Protected main at this Stage 3A-1 pass: `5f33c88ca1ea7d80e0517f42a200f5a2e15833c9`.
- Original protected-main permanent Stage3A0 version at run: `a11cccf944492e4d968edbeef4111ebad150fcec`, with verified same tool/policy blobs on newer main.
- Immutable Research base: `3f5a15458aa468347e56e669327d6fe4c9c6ee69`.
- No changes to protected main, global registry, published school packages, other Research lanes, or Implementation mutation lock.

**STAGE 3A-1: COMPLETE. STOP. Stage 3A-2 HOME venue research requires separate owner `Proceed`.**
