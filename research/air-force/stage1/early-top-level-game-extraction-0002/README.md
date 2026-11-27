# Air Force Stage 1 — early top-level game extraction checkpoint 0002

STATUS: STAGE1_IN_PROGRESS. Same Research lane. **NOT** Stage 1 COMPLETE; no Stage 2 or Implementation authorization.

- Immutable research_base_sha: `3f5a15458aa468347e56e669327d6fe4c9c6ee69`
- Immutable checkpoint parent branch HEAD: `120dbd301dea9907c8cc2fef15659b1d31b2e84b`
- Accepted classification: `Air Force,1957-58+` CONFIRMED, owner-final. Institutional inception **1956-57** is **NON_D1**; its 21 source-identified competitive games are preserved without alteration.
- Primary institution guide historical cutoff: 2025-26; required completed-season cutoff: 2025-26.
- Source: Air Force official 2026-27 history PDF p58, plus four official 1957-58..1960-61 schedule pages and limited 1958-59 Arizona reciprocal corroboration. Original 1956-57 first checkpoint remains immutable.
- `stage1-ledger.csv`: authoritative working append-only combined ledger: first 21 rows are **byte-identical representations** of the initial checkpoint; 92 additional exact-guide individual-game rows. Count **113** identified competitive game rows in 1956-57..1960-61.
- Additional season counts: 1957-58 **17-6 (23 games)**; 1958-59 **14-9 (23 games, including Arizona omitted by online schedule)**; 1959-60 **12-10 (22 games, including NCAA Midwest Regional first-round loss to DePaul)**; 1960-61 **12-12 (24 games)**.
- The 92 new rows have stable IDs, literal PDF date/label/result/score snippets, scored results, dates, structured game_type, source-supported H/A/N from same institution official season schedules and site-summary counts, primary guide provenance, and schedule URLs. First-season 1956-57 rows are not reinterpreted. Official linked outbound logos/domain URLs are not opponent identity evidence.
- 1959-60 DePaul 3/7 game is NCAA_TOURNAMENT, source explicitly marks `## NCAA Midwest Regional` and says played in Chicago. Other new rows are regular-season including 1958-59 West Coast Classic (not postseason).
- 1958-59 Arizona printed as `2-29` in game list, an impossible date; the same Air Force guide's team records p5 and Arizona reciprocal history establish 1959-02-28. Literal malformed date remains in raw source row and discrepancy ledger. The guide's 14-9 W/L reconciles only when Arizona 115-62 is included; the dynamic online 13-9 page omits the game. This is a resolved game-universe inclusion, not anonymous aggregate coverage.
- The guide `*` Denver Auditorium Arena venue annotations and the 1958-59 West Coast Classic at Corvallis remain preserved as guide field evidence. 1959-60 New Mexico 70-66 has a **live official-source geographical conflict**: guide starred venue implies Denver; online schedule explicitly states Albuquerque. Do not resolve by geography or assume that one source silently supersedes the other. The source-program venue/locality work belongs to Stage 3A.
- No exclusions or duplicate games arose in this five-season identified population. No claim about unlisted exhibitions.
- Original 70-season guide record census (1956-57..2025-26) carried forward with 5 now row-reconciled seasons and 65 aggregate-only seasons. Remaining aggregate expected 1957-58+ rows after this tranche: **1815** (1907-92); **not** game-level missing identities and not accepted missing-game exception.
- Source-internal printed all-time-total discrepancy (+2 wins vs sum of 70 season records) is preserved from parent, not silently repaired.
- Exact current Stage 1 blockers: **65 top-level seasons' row-level ledgers not yet extracted** (1961-62..2025-26), aggregate-expected **1815** prospective game identities; no identified-game/inclusion/season-count blockers within the five extracted seasons. The New Mexico site conflict and Kansas City Univ historical naming are later-stage material questions, not reason to reopen reconciled early game universe.

## Next bounded unit

Extract and reconcile the guide's **1961-62 through 1964-65** detailed game rows from PDF pp58-59 against official corresponding season schedules. Maintain the 113-row working ledger, source literal evidence, and explicit anomalies; commit one successor Stage 1 checkpoint; do not advance Stage 2. Later Stage 3A handles venue conflicts and Stage 2 handles opponent identity.

## Safety

Research-only `research/air-force` branch, no change to protected main, published basketball, canonical games, shared references, other school Research, or serialized Implementation. Final terminal class remains ordinary `RESEARCH_FROZEN`.
