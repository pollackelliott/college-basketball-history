# Air Force Stage 1 — primary guide game extraction checkpoint 0003

STATUS: STAGE1_IN_PROGRESS. One bounded continuation; NOT Stage 1 COMPLETE; NOT Stage 2 or Implementation.

- Protected-main SHA at execution: `3f5a15458aa468347e56e669327d6fe4c9c6ee69`; immutable `research_base_sha` remains exactly the same.
- Verified parent Research HEAD: `4cd8cba885c1037a232d2549ca59838183ef0bbc`. This successor retains predecessor commits and unchanged files.
- Owner-final, unchanged top-level scope: `Air Force,1957-58+`. Institutional varsity inception: **1956-57**, classified **NON_D1**, included in full-institution Research. Historical and required completed-season cutoffs: **2025-26**.
- Source: owner-provided **2026-27 official history guide PDF p59**, exact guide W/L and individual results, cross-reconciled against Air Force official season schedule pages for 1961-62 through 1964-65. Original PDF digest `sha256:5fdf61cc80c698bae8ce61cc0ae1009d01139682c8148014934e304b407b73fd`.
- The combined `stage1-ledger.csv` contains **204 uniquely identified games** from 1956-57 through 1964-65. Its original **113 rows and header are carried forward byte-for-byte**, including all prior literal-source defects and residuals. This tranche adds exactly **91 guide-identified competitive games**, with stable IDs, dates, literal guide opponent strings/row evidence, scores, W/L, structured game_type, schedule-backed H/A/N, supported locality, page reference, and URLs.
- New exact season aggregates: **1961-62 16-7 / 23**; **1962-63 10-12 / 22**; **1963-64 11-12 / 23**; **1964-65 9-14 / 23**. In each season, the on-court outcomes and H/A/N win/loss partitions agree exactly with the 2026 guide and the official online schedule, including the 1963-64 legitimate leap-day Wyoming game **1964-02-29**.
- **1961-62 Texas Tech** on 1962-03-12 (66-68 L) is **NCAA_TOURNAMENT** (guide `## NCAA Midwest Regional` and Lubbock, Texas). Official schedule classifies the game neutral. Exact NCAA venue remains downstream postseason work.
- Other 90 games in this tranche are **REGULAR_SEASON**. **1963-64 Florida State / Florida** were Gator Bowl Classic games at Jacksonville, FL; **1964-65 Colorado State / Colorado** were Mile High Classic games at Denver, CO; their source-supported **NEUTRAL** classification is preserved. The **1961-62 Denver** game (1958-59 precedent notwithstanding) is source-starred as **Denver Auditorium Arena**, and official schedule's separate site summary classifies it NEUTRAL; no home/away inference from opponent or geography.
- `stage1-residuals.csv` carries the prior five items unchanged and adds **three nonblocking historical-opponent-label review rows** for Stage 2: St. Michael's (N.M.), Carroll, California-Western. Contemporary outbound opponent links are NOT authority for historical identities.
- Source-internal all-time record discrepancy inherited unchanged from parent (sum of 70 per-season guide lines 814-1114 vs printed 816-1114). We do not claim unidentified additional game IDs.
- `source-inventory.csv` is accumulated from 0001 primary/authority inventory, 0002 addendum, and four 0003 institution online season schedules.
- `season-census.csv` accounts for all **70** seasons inception..2025-26: **9 fully row-extracted (1956-57..1964-65)** and **61 yet to extract (1965-66..2025-26)**. Remaining guide per-season aggregate **1,724 prospective games** (1815-91); these are NOT unidentified missing games or a source-acknowledged coverage gap.
- All 91 extracted guide records are accepted as identified competitive varsity games at this stage; **no candidate game duplicate**, no competitive exclusion discovered, and no newly blocked Stage 1 season count. Source-site/identity work belongs to later governed stages.
- Work remains on the `research/air-force` branch only. No changes to protected main, basketball canon, published packages, global references, other Research lanes, or active serialized Implementation.

## Exact next bounded Research unit

Systematically extract and reconcile **1965-66 through 1968-69** from the guide's year-by-year results against the four corresponding official season schedules, using this 204-row working ledger and retained residuals. Continue four-season source batches, not individual-game web archaeology. Stop at one durable successor checkpoint, not Stage 2.
