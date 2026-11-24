# Gonzaga ALL_HISTORY_EXPANSION Research — Stage 1 branch reconciliation checkpoint

checkpoint_status: ACTIVE_STAGE1_RECONCILED
target_team: Gonzaga
program_key: gonzaga
research_base_sha: f64ce23988faa04a304eb15d9ad96c2144ed5777
protected_main_sha_at_checkpoint: 848e9cebc9c5b5ff7f769920a7bd8fa9b50a3f8d
accepted_program_inception_season: 1907-08
stage1_complete: false
stage2_authorized: false

## Durable-state reconciliation

During the bounded post-owner-decision unit, the Research branch advanced concurrently with a more complete Washington State reciprocal-family checkpoint.

The durable higher-coverage artifacts were inspected rather than overwritten.

Mechanical verification of `stage1-identified-game-ledger-0002.csv` found:

- 84 rows;
- 84 unique season/date/opponent/score identities;
- 45 expansion seasons represented;
- zero duplicate keys;
- zero seasons exceeding Gonzaga's official W/L/game aggregate.

That 84-row WSU ledger therefore remains accepted.

The independently recovered Washington institutional all-time-results family adds three non-duplicate Gonzaga games:

- 1910-02-14 — Washington at Gonzaga — Gonzaga L 14-23;
- 1912-02-06 — Washington at Gonzaga — Gonzaga L 17-37;
- 1913-02-05 — Washington at Gonzaga — Gonzaga L 20-37.

These three rows also fit the official Gonzaga season aggregates.

## Controlling Stage 1 state

- season census: `stage1-season-census-0002.csv`;
- owner inception authority: `stage1-inception-owner-authority-accepted-20261124.md`;
- identified-game ledger: `stage1-identified-game-ledger-0003.csv`;
- status: `stage1-status-0004.json`;
- accepted identified games: 87;
- official expansion population: 977 games across 51 seasons;
- anonymous rows created: 0.

Earlier numbered/partial ledgers and statuses remain historical checkpoint evidence but are superseded by the controlling artifacts above.

No protected-main, published Gonzaga, canonical, or shared/global basketball state changed.

## Next bounded unit

Harvest the next highest-yield authoritative reciprocal source family, deduplicate against the 87 accepted rows, reconcile against season aggregates, and stop before open-ended one-opponent archaeology.

Stage 2 remains unauthorized.
