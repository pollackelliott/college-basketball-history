# Gonzaga Stage 1 — complete protected-main original source-game Gonzaga-name census

## Exact authenticated authority
- Protected main: `087ac5dedc65780b65b7ae8d61e239d2033e2eea` (115 `schools/*` directories; 114 external reciprocal files).
- Research parent: `d74e476670eb196b53f24b604cbd31bdfda63af2`.
- Immutable research base: `f64ce23988faa04a304eb15d9ad96c2144ed5777`.
- Reused prior 158-row canonical crosswalk without rescanning `data/canonical/games.csv`.

## Bounded source population and method
- Parsed **all 114** other `schools/<school>/source-games.csv` source files, exact blob identities and row counts recorded in `schools/gonzaga/research/checkpoints/stage1-all-published-source-games-1907-1958-audit-0001.json`.
- Source rows inspected: **302,578**.
- The explicit candidate predicate was 1907-08 through 1957-58 season-start and case-insensitive **`gonza`** in `source_opponent_label`, `normalized_opponent_name`, or `normalized_opponent_key`.
- **158 source rows**, from **13 source schools**; **101** external school files had no such historical opponent string.
- Reconstructed all 158 first-party original source-game IDs, opponent literals, date/score/result, raw source text and source-school blob IDs into `schools/gonzaga/research/checkpoints/stage1-all-published-source-games-1907-1958-crosswalk-0001.csv`.
- Every source row crosswalked uniquely to an accepted canonical-game identity and existing Gonzaga Research game by source school, season, reciprocal W/L and score, with exact dates resolving the two equal-score Oregon 1929-30 games.
- No unmatched/ambiguous candidate, separate Gonzaga High row, duplicate canonical identity, or new competitive game found in this explicit string-matching population.

## Accepted Research state preserved
- Stage 1 ACTIVE; Stage 2 NOT AUTHORIZED.
- Controlling ledger remains `schools/gonzaga/research/checkpoints/stage1-identified-game-ledger-0033.csv` **unchanged**, at **557 games (214W/343L)**.
- Official aggregate **477W/500L**, **977 games**, diagnostic difference **420** (arithmetic, not named-game evidence).
- Six previous held candidates and four parked historical accounting contradictions are unchanged.
- No original source-school, canonical/global, main, or published-package mutation.

## Scope limitation and bounded next step
This completes the fixed protected-main published **Gonzaga-name-stem** reciprocal-file population. It is not a proof that all historical aliases such as nickname-only 'Zags' or initials, unpublished opponents, missing early-year institutional schedules, or external original sources are exhausted. Do not rerun this 114-file pass merely to pursue speculative aliases. A subsequent bounded Stage 1 unit should target only a concrete high-yield independent evidence class or evaluate Stage 1 convergence under current stopping policy. No Stage 2 automatic transition.

## Durable children
- Audit: `schools/gonzaga/research/checkpoints/stage1-all-published-source-games-1907-1958-audit-0001.json`
- 158-row raw-source crosswalk: `schools/gonzaga/research/checkpoints/stage1-all-published-source-games-1907-1958-crosswalk-0001.csv` (Git blob `fd5d0e60ddf75aec11df9d43f0822004e1021378`)
- Stage 1 status successor: `schools/gonzaga/research/checkpoints/stage1-status-0042.json`
