# Fresno State — Stage 1 guide extraction checkpoint 0002

**Status: 1921–22 through 1942–43 guide extraction complete; Stage 1 remains OPEN.** This is source-entry serialization, NOT Stage 1 acceptance, not a complete competitive-game ledger, and not a Research Freeze.

- Research base: `087ac5dedc65780b65b7ae8d61e239d2033e2eea` (immutable), predecessor research HEAD `b7a8d3434cc675d53867ccba875c53807de319f6`.
- Source: owner-uploaded official 2025–26 Fresno State Men's Basketball Media Guide, PDF SHA-256 `b960369400bb42be27caa0331a1be2c9defd1e9163e4ea14f567c38e262693ba`, pages 41–43 (printed 39–41).
- Exact raw text already preserved in parent checkpoint: `research/fresno-state-all-history-expansion/stage1/startup-0001/media-guide-early-results-raw.txt` (Git blob `fc72b2862aa283481d498873af0a17fa1d7e405a`). Exact PDF source remains accessible in owner attachment.
- New candidate source entries: **373** across **22** seasons (1921–22 through 1942–43), IDs `FRESNO-EXP-CAND-<season>-<source sequence>`.
- Source line results: **189 W / 184 L**; official institutional aggregate for those seasons **191 W / 182 L**. Count is **373** both ways, and all 22 season counts match.
- Unresolved 1939–40 contradiction: guide headline **10–9**, its listed results **8–11**. Do not manufacture games or silently flip outcomes.
- **Eight intra-program potential exhibitions** (Fresno State Frosh/Alumni) need inclusion adjudication, not automatic acceptance or deletion.
- **Two potential duplicate pairs (four source entries)**: 1922–23 UC Davis L 30–17 twice, 1926–27 UC Davis W 31–18 twice. Duplicate representation vs separate games unresolved; each row retains its own stable source-entry ID.
- **One mixed-score-order exception**: 1942–43 `Pacific L 51-52` is result-consistent with team-first score order; other 372 rows are result-consistent with winner-first score order. Preserve exact source literal for field-level audit; score orientation is provisional.
- No exact game dates are inferred; literal `at` is kept only as a **source cue**, never as geography-inferred curated H/A/N.
- All 373 are **candidate entries**, not yet accepted distinct canonical games. Reciprocals, official competitive status and duplicate identity remain independent later evidence tasks.
- No fresh Stage 2 opponent normalization or 3A site archaeology is attempted here.
- The accepted published **1,708** Fresno rows and original excluded **78** 1955–58 historical Research rows are unchanged; prior owner scope exclusion and top-level **1970–71+** authority still control.

## Checkpoint members

- `candidate-source-entries.csv` — 373 source entries, literal evidence/line/page locators, provisional score interpretation and review classes.
- `season-reconciliation.csv` — complete 22-season source vs institutional W/L accounting.
- `review-queue.csv` — 8 intra-program rows, 2 potential duplicate pairs, 1 season accounting conflict, 1 score-order provenance exception.
- `extraction-audit.json` — exact structured source/base/population accounting.

## Next bounded Stage 1 unit

Extract the remainder of the available authoritative guide (1943–44 through 1969–70) using the same season-first source discipline. Preserve the 1943–44 no-record/withdrawal statement; handle official forfeits separately from on-court results (especially 1954–55 and 1961–62). Reconcile rather than duplicate the original 78 accepted-but-not-published 1955–58 source rows. Then perform a *bounded* discrepancy/exhibition/duplicate investigation against reciprocal and institutional source families. Do not advance Research stage automatically.
