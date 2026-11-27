# Air Force 1982–83 — institutional guide source disagreement

STATUS: **STAGE1_BLOCKING_IDENTIFIED_UNIVERSE_DISCREPANCY**, candidate-only population (not accepted Stage 1 ledger). Do not infer game identities or award a missing-game exception from aggregate differences.

Current official Air Force 2026–27 guide (PDF p62; SHA-256 `5fdf61cc80c698bae8ce61cc0ae1009d01139682c8148014934e304b407b73fd`) prints season record **11–16 = 27**, but there are exactly **26** detailed game rows, tallying **12–14**. All 26 literal opponent/date/score/W-L candidate entries are preserved in `1982-83-2026-raw-source-candidates.csv`. They are not automatically accepted as current-season games.

Archived Air Force official 2010–11 all-time results PDF, printed **page 98** (URL: https://goairforcefalcons.com/documents/download/2010/11/9/_afa_m_baskbl__ResultsSection2010-11.pdf), prints **10–17 = 27**, but lists only **25** individual games that tally **9–16**. An independent college basketball season history reports **10–17** and WAC **2–14**; other non-institutional game lists have further differences. Thus not even the older institutional guide completely establishes 27 unique game rows.

Concrete material contradictions:
- **December 4, 1982, Pan American:** 2026 official PDF says **W79–60**. The archived 2010 Air Force PDF says **L44–78**. Do not accept either result merely from edition recency.
- **March 9, Hawaii, 76–84:** 2026 PDF places a `Hawaii#` WAC tournament loss in 1982–83. The independent Western Athletic Tournament historical series locates the exact opponent and score in **1988**, not 1983. This is a demonstrable cross-season bleed, and the game must not be published twice.
- **February 25, BYU, 62–76:** the newer 1982–83 listing appears to reuse a **1987–88** game; archived official Air Force opponent history lists BYU 62–76 on February 25, 1988. Prevent season-misattribution.
- **1983 conference postseason:** the WAC tournament retrospective has no Air Force 1983 postseason appearance; do not infer the 2026 p62 `Hawaii#` row establishes one.
- The current guide's extra rows and older guide's omissions must be compared against exact-game official opponent histories/league or reciprocal year sources in **one bounded Stage 1 discrepancy family**, rather than repeatedly searching every legacy opponent.

Current research disposition: **zero 1982–83 IDs added to the cumulative accepted ledger in this checkpoint**. Maintain expected season heading as current-source 11–16 in the 70-season institutional census (not silently overwritten), retain 10–17 archived conflict, and identify the true competition/administrative-result population before assigning IDs. This is an honest Stage 1 blocking residual and does not prohibit high-throughput extraction of unaffected seasons.

The current protected main / immutable Research base is `3f5a15458aa468347e56e669327d6fe4c9c6ee69`.
