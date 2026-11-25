# Boise State ALL_HISTORY_EXPANSION — Stage 1 Weber College reciprocal checkpoint 0013

**Status: STAGE_1_IN_PROGRESS** — same independent Boise State expansion Research lane. No Stage 2, Implementation, new Research lane, owner gate, protected-main mutation, or canonical/shared-reference mutation.

## Durable authority / succession

- Immutable `research_base_sha`: **`1c3bb7f1d3231c604c413ed75a4afc17b0388089`**. Do not refresh this when main moves.
- Protected `main` authenticated at tranche start: **`4d91da1800d9d7b535ae2e191f309bfc391ea2ee`**, protected. Existing controlling `AGENTS.md`, Stage 1 game universe, all-history expansion, convergence and portable-execution documents already authenticated at unchanged blob hashes.
- Parent Research branch head: `fa6ec7d6799c75b0193bab3dc344e1f9ad8c5463` (checkpoint 0012).
- Parent portable 0012 ZIP SHA-256: `8865c88035872531be90f104d5d142a7ef3051d3e02794d9eb29e8b57e439604`.
- New portable ZIP: **`boise-state-expansion-stage1-weber-reciprocal-0013.zip`**, SHA-256 **`46bd54f038ab2366babf91cba6e2eb13437f043106044d2429991c57e9a834e9`**.
- Full 16-column ledger ZIP member SHA-256: **`178ff64f6f5f9b81ce0e239360b3478b65d5ea61330eff98d59d1f6e852cefd4`**. ZIP `manifest.json` lists and independently verifies all contained member SHA-256 hashes.
- ZIP members: `structured-stage1-ledger.csv` (189 identities), `annual-season-accounting.csv` (38), `season-census.csv` (38), `residuals.csv`, `source-inventory.md`, `stage1-0013-weber-source-delta.csv` (35 fully typed row evidence records), `stage1-0013-weber-opponent-source-census.csv` (37 source presentations including 2 excluded/held), retained 0012 field repairs and unresolved candidates, `stage1-0013-status.md`, `manifest.json`.
- Research-branch mirrors: `stage1-weber-reciprocal-0013-ledger.csv`, `...-accounting.csv`, `...-season-census.csv`, `...-evidence.csv`, `...-source-census.csv`, `...-candidates.csv`, this note. ZIP retains the fully accumulated 16-column original-source provenance.

## Source family (rigorous provenance distinction)

**First party, four games:** Weber College's own `1949 Acorn` institutional basketball result table (yearbook, pp. 122-123), digitized by Weber State Stewart Library, https://digital.weber.edu/details?id=108477 . Four unambiguous Weber-perspective score entries for 1948-49 versus Boise (Weber W62-54; L59-74; W65-63; L50-54) are reverse-oriented to Boise L54-62, W74-59, L63-65, W54-50. Source is institutional yearbook OCR; its oversized ~61MB linked original PDF was not downloaded for an image-level recheck. Independently consistent with modern secondary reconstruction `History of Weber College Basketball pt.3`, https://wildcatchronicle.substack.com/p/history-of-weber-college-basketball-aa8 . **No exact dates or Boise H/A/N are assigned.**

**Explicit secondary evidence, 31 games:** Gavin Nelson, `History of Weber College Basketball pt.4: The 1950s (1950–58, 1960–62)`, Aug 1 2025, https://wildcatchronicle.substack.com/p/history-of-weber-college-basketball-aa3 and `1958–59 Weber College Men's Basketball Team`, Aug 8 2025, https://wildcatchronicle.substack.com/p/the-1958-59-weber-college-mens-basketball . The author credits Weber's *Signpost* primary school newspaper and *Acorn* yearbooks; individual primary newspaper score clips **were not all independently retrieved/checked**. Every affected game is source-class-tagged `SECONDARY_COMPILATION`; this is not represented as an original Weber athletics game log or independent first-party corroboration. A digitized historical newspaper clipping hosted by Weber separately prints 1950-51 Weber wins 85-47 and 73-46 over Boise: https://digital.weber.edu/wsu_files/dc/e4/dce45623116857637e7067bc02ca2b02cc6514bf.pdf . Its PDF text was read, but the required screenshot viewer failed, so preserve the distinction.

The original Weber 1949-50, 1950-51, 1952-53 and subsequent score groups in the modern source are recorded as distinct games only where separate Weber result entries occur. Exact dates are left blank except one **1959-01-12** conference opening date expressly given in the 1958-59 season account. All 35 new H/A/N are **UNKNOWN**; 'at Boise', 'vs Boise' and regional source tokens are literal source evidence, not independent full site proof.

### Added 35 nonduplicate game identities (Boise 12-23)

| Season | New IDs | Boise W-L | Source |
|---|---:|---:|---|
| 1948-49 | 4 | 2-2 | Original Weber Acorn |
| 1949-50 | 5 | 1-4 | Weber specialist secondary compilation, including one marked regional postseason |
| 1950-51 | 4 | 1-3 | Weber compilation, two contemporaneously corroborated score statements |
| 1952-53 | 4 | 2-2 | Weber compilation |
| 1954-55 | 2 | 1-1 | Weber compilation; existing regional third game omitted as duplicate |
| 1955-56 | 2 | 1-1 | Weber compilation |
| 1957-58 | 2 | 1-1 | Weber compilation |
| 1958-59 | 2 | 1-1 | Dedicated Weber 1959 historical account |
| 1959-60 | 4 | 1-3 | Weber compilation |
| 1960-61 | 2 | 0-2 | Weber compilation |
| 1961-62 | 4 | 1-3 | Weber compilation; one regular result held as collision; three regional games retained as separate |
| **Total** | **35** | **12-23** | Four first-party, 31 explicitly secondary |

## Duplicate and score-collision safeguards

- **1954-55 NJCAA regional:** Modern Weber source `vs Boise L74-77` is the same Boise W77-74 tournament game already recorded as `BOISE-EXP-S1-1954-002`. Exactly one game retained; do not add a second 1954 regional row.
- **1961-62 Weber at Boise:** Modern Weber source says Weber L66-85 (Boise W85-66), while existing research row `BOISE-EXP-S1-HON-0008-006` from contemporary Oregon newspaper reports Boise W83-68 against literal `Weber`. Source mismatch may be one game with an incorrect score or two distinct games; no source-backed identity distinction was established. **Do not add** 85-66 as a second game and **do not rewrite** 83-68. Leave an exact residual for future first-party review.
- Preserve all seven previously inherited 0012 uncertainty rows, including December 1948 University of Idaho varsity played/result unknown and January 1957 NNC played/result unknown. No score/date guesses and no silent resolution.
- For 1961-62 the *three* separately reported regional-tournament Weber games are Weber L70-73, W66-64, W65-55; encode Boise W73-70, L64-66, L55-65 as three POSTSEASON games. Exact tournament dates/building and H/A/N are unresolved for later site Research.
- Strong source-class distinctions remain in complete source delta and source-census before any later Stage 2 game reconciliation.

## Mechanical census and stopping state

- Previous 0012 supplemental game universe: **154** source-backed IDs. New 0013 ledger: **189** unique IDs, the original 154 left completely unchanged, 35 added. No repairs or deletions in this tranche.
- Of 189 supplemental identities, **134** are junior-college-era (including one documented game from MW-unlisted 1937-38); **55** are 1968-69 and 1969-70 Boise record-book games.
- The original Mountain West table of **33 junior-college annual seasons** remains **441 W / 346 L = 787**. We identify **133** specific games in those 33 source-recorded seasons, leaving **654** aggregate-minus-identified unmatched, a coverage *arithmetic diagnostic* only. The separate 1937-38 game is not allocated into those source annual totals.
- Each of the 11 seasons touched by Weber has an identified W/L subset not exceeding its original published annual W or L total.
- `STAGE_1_IN_PROGRESS` continues: original-source proof for secondary Weber entries, 1961-62 score collision, historically incomplete aggregate universe, 1932-33 inception, 1937-39 annual gaps, other genuinely played/result-unknown fixtures all remain open.
- No published Boise 1970-71+ baseline data (1,670 published rows), protected main, shared registry, canonical games, or Implementation lock was modified.

## Next bounded Stage 1 work

Prefer a **single coherent original Weber Signpost/Acorn newspaper issue-family pass** to corroborate the remaining 31 source-class SECONDARY rows and the 1961-62 85-66 vs 83-68 collision. Do not recursively open an unbounded source campaign; stop at a source-family boundary with exact residual population. Research may then pivot to other official opponent catalogs. Proceed does not authorize Stage 2.
