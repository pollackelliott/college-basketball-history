# Gonzaga Stage 1 — 1930–31 distinct game-count/source-WL contradiction, checkpoint 0053

Current protected main `5b840a354fb5cd792239ff8b93cba223a18dd87a`; preceding Gonzaga Research HEAD `01a159b883f1cd8e51f0cf47902fba73fb11e694`; immutable research base `f64ce23988faa04a304eb15d9ad96c2144ed5777`.

## Outcome — 15 accepted games remain distinct; one exact primary-source game date recovered

Gonzaga's [2026–27 official Record Book, printed page 58](https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/gozags.com/documents/2026/8/27/2026-27_Record_Book.pdf) reports **7 wins, 8 losses, 15 games** under Maurice Smith in **1930–31**; original PDF screenshot inspected. The 15 game-level individually identified source-backed Research rows yield **5 wins, 10 losses, 15 games**. Both count 15 games, but accepted-source game results differ from Gonzaga's institutional season aggregate by **−2 wins / +2 losses**. There is no evidence-based operation to reclassify, merge, remove or reverse two concrete games just to match aggregate W/L.

### Exact seven opponent-source families

| Opponent source program | Distinct Gonzaga game IDs |
|---|---:|
| Washington State | 2 |
| Montana | 4 |
| Central Washington | 2 |
| Oregon State | 3 |
| Oregon | 2 |
| Washington | 1 |
| Idaho | 1 |
| **Total** | **15** |

The source-specific 15-row matrix is preserved in `stage1-1930-1931-fifteen-source-game-matrix-0001.csv`, with original research IDs, opponent names, available exact dates, scores, W/L, H/A/N and source locators. All remain recognized, individual `REGULAR_SEASON` competitive game identities. No accepted identity is replaced with an ungrounded aggregate game.

### Concrete correction: Oregon State L30–43 was January 2, 1931

While verifying 1930–31 distinct opponents and chronological conflicts, the original [January 4, 1931 *Eugene Register-Guard*, printed page 8](https://oregonnews.uoregon.edu/lccn/sn85042472/1931-01-04/ed-1/seq-8/) was recovered and the original [scanned PDF page](https://oregonnews.uoregon.edu/lccn/sn85042472/1931-01-04/ed-1/seq-8.pdf) visually examined. It reports that **Oregon State defeated Gonzaga at Corvallis on Friday evening 43–30**, and that **Oregon beat Gonzaga Saturday 48–27**. Since the paper was Sunday January 4, the games were **Friday January 2, 1931 (Oregon State)** and **Saturday January 3, 1931 (Oregon)**. This also independently proves they were **two different played games**, not one result duplicated under different schools.

One exact date/provenance change is written through to successor ledger `stage1-identified-game-ledger-0036.csv` for existing `GONZAGA-EXP-OSU-013`: `game_date` goes from blank to **1931-01-02**. Its unchanged identity, Gonzaga loss **30–43**, `REGULAR_SEASON`, and `site_type=AWAY` remain; the away classification was already grounded in the Oregon State official source's home notation, **not inferred from newspaper geography**. The adjacent accepted Gonzaga at Oregon L27–48 on January 3 remains unchanged. The full original ledger 0035 is preserved byte-for-byte.

### Independent institutional crosscheck

[Central Washington's official 1930 basketball schedule](https://wildcatsports.com/sports/mens-basketball/schedule/1930?grid=true) explicitly records a Jan29 home **L12–17** against Gonzaga and Feb23 away **W37–15** over Gonzaga: two distinct games and outcomes matching the Gonzaga accepted rows. [Washington's official series table](https://washington_ftp.sidearmsports.com/old_site/pdf/m-baskbl/2010-11-recordbook-1015.pdf) confirms a 1931 home **W33–25** over Gonzaga. None supports flipping a Gonzaga loss into a win. The other accepted reciprocal families remain unaltered.

### Terminal historical classification, not a Stage 1 closeout

**`EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION` / `SAME_COUNT_RESULT_SOURCE_ACCOUNTING_CONTRADICTION`** remains a research-exhausted early-history accounting blocker. This is **not** a count of two missing games: official and accepted are both 15. The game's result and identified participation are supported, while cumulative official W/L differs. Current protected main has **no Gonzaga owner authority** in `data/reference/early-history-accounting-authorities.json`, so no registry exception or Stage 1 terminal closeout can be declared. The previously accepted research-exhaustion disposition remains; further broad press searching is not authorized by this one-game field proof.

### Scope and exact state retained

- Accepted expansion games: **560 (216–344)**; official aggregate **977 (477–500)**; net arithmetic difference **417**, not distinct unidentified game identities.
- Five active source-game holds: four February 1943 unresolved owner-level inclusion questions and the January 1926 Portland date conflict.
- Four independently classified research-exhausted closeout accounting contradictions remain **1915–16, 1930–31, 1936–37, 1937–38**. 45 seasons have positive arithmetic game-count differences.
- Stage 1 **ACTIVE**; Stage 2 **NOT AUTHORIZED**. No mutation to main, published games, global reference registries, or another school.

## Next bounded unit

Audit **1936–37** only, reconciling nine accepted opponent-documented game identities (4–5) against Gonzaga's official six-game (1–5) aggregate, and test any concrete duplication/incorrect-season mechanism. Stop with explicit source-accounting residual if none is supported; do not reopen 1930–31, 1942–43 or begin Stage 2.

Structured audit: `stage1-1930-1931-fifteen-game-accounting-contradiction-audit-0001.json`. New exact source matrix: `stage1-1930-1931-fifteen-source-game-matrix-0001.csv`.
