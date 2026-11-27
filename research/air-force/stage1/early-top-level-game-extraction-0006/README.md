# Air Force Stage 1 — official year-by-year extraction checkpoint 0006

**STATUS: STAGE1_IN_PROGRESS.** Not Stage 1 COMPLETE, Stage 2, Research Freeze, or Implementation.

Authority: immutable `research_base_sha` and authenticated protected main `3f5a15458aa468347e56e669327d6fe4c9c6ee69`; verified parent Research HEAD `b39a8235d57e1102d4bef9577f38b46771692cbf`. The owner-final classification `Air Force,1957-58+` is unchanged and separate from institutional inception **1956-57** (NON_D1); completed season cutoff **2025-26**. Air Force 2026–27 official history PDF p61 is primary game source, exact SHA256 `5fdf61cc80c698bae8ce61cc0ae1009d01139682c8148014934e304b407b73fd`.

## Four-season universe and site accounting

| Season | Primary guide W-L (awarded) | Unique competitive games | Official online reconciliation |
|---|---:|---:|---|
| 1973-74 | 11-13 | 24 | Sidearm online duplicates all 24 games, presenting W22 L26 and 48 display entries; use **24 unique**. Deduped H10-3, A1-9, N0-1. |
| 1974-75 | 13-12 | 25 | 25 rows match, H8-5, A5-7, N0-0. |
| 1975-76 | 16-9 | 25 | 25 rows match, H10-3, A6-6, N0-0. |
| 1976-77 | 12-15 | 27 | Online omits two genuine final games and displays W11 L14, 25 rows; source+reciprocal 27 credited games H11-5, A1-9, N0-1. |

The combined `stage1-ledger.csv` is **502 unique identified game IDs** spanning 1956-57 through 1976-77 (**21** source-identified seasons). All **401 original accepted rows and header are preserved byte-for-byte**. The 101 new competitive games are **REGULAR_SEASON** with stable IDs, source literal labels/row, original guide scores, dates, corrected dates where corroborated, on-court outcomes, supported H/A/N, evidence citations, and administrative-result separation.

## Reconciliation findings (all preserved explicitly)

**1973-74 online duplicates are mechanical display representations.** Its page repeats all 24 dated scored entries exactly once, inflating summary to 22-26. The guide's 11-13, and the distinct online rows' deduped split H10-3, A1-9, N0-1 agree. San Diego State at the Great Plains Classic in Omaha, NE is neutral; Creighton at Omaha is away. Never create 24 phantom game IDs.

**1976-77 final game omissions are real games.** Guide lists 27 games, official online 25 (11-14), missing a 66-76 loss at Tulane and 77-72 win at Denver. Tulane's authoritative October 2026 record book identifies **Feb 26, 1977**, Air Force L66-76, at Tulane. Denver's official all-time 1976-77 results list **March 1, 1977**, Denver L72-77 at home. Both are accepted as unique competitive source+reciprocal corroborated games, not unidentified gaps.

**Guide date typo:** official Air Force 2026-27 PDF p61 prints **2-29** for Tulane in nonleap 1977; curated working date **1977-02-26** based on the Tulane institutional primary record book and reciprocal series. Literal `2-29` survives unmodified in the source row; MCubed also prints this impossible date, so it is not higher authority.

**Montana administrative forfeit:** 1976-12-03 Air Force **W59-65** credited (guide and online), actual final score is Air Force **59**, Montana **65**. Therefore `stage1-ledger.csv` uses explicit `on_court_result=L`; `administrative-results.csv` records the credited institutional win separately, with guide literal and official Air Force 2022-23 game-notes provenance. That season has **11-16 on-court** game outcomes across 27 games, but officially credited program aggregate **12-15** (the season census preserves 12-15). One genuine game, not a second invented result.

**1976-77 tournament marker:** source 1976-77 uses `**` on Evansville/Loyola games but footnote labels Evansville Holiday Classic with `%`. Official schedule shows Evansville home-host site for the Evansville road game and Loyola as neutral, both in Evansville, IN; no exact-building inference. Source marker inconsistency preserved as a later-site annotation.

There are **18 explicit historical/reconciliation residual notes** (13 inherited + five new), all new ones nonblocking for Stage 1 game identity. Current tranche: zero new exclusions, zero true game duplicates, no NCAA postseason. There is no authority to reopen earlier accepted games, invent unnamed aggregate games, conflate current outbound opponent websites with historical identities, or shift owner-final scope.

Full inception-to-cutoff census: **70 seasons; 21 extracted, 49 aggregate-only seasons (1977-78 through 2025-26)**. These 49 sum to **1,426 prospective game rows** yet to systematically extract (previous 1,527 minus 101); *not* source-acknowledged missing-game identities. Inherited printed all-time guide total discrepancy +2 wins is retained unchanged.

Scope and safety: Research-only `research/air-force`. Protected main, canonical games, published school data, global references, other school Research artifacts and the one-active-Implementation lock untouched.

## Next bounded unit

Extract **1977-78 through 1980-81** from official guide PDF pages 61–62, reconcile against source season headings/official season schedules, preserve source literal and admin result anomalies, and commit one bounded successor checkpoint. Do **not** enter Stage 2 automatically.
