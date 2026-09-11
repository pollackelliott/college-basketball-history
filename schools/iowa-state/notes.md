# Iowa State men's basketball research notes

## Status
- School: Iowa State
- Source program key: `iowa-state`
- Research base SHA: `602b344e59ea5aeadee9439a36a3cb2a3acb2813`
- History scope: `INCEPTION+` from `data/reference/program-top-level-scope.csv`
- First covered season: 1907-08
- Final covered season: 2025-26
- Competitive games: 2,932
- On-court record: 1,511-1,421
- RESEARCH_FROZEN: YES
- CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES
- Final research QA: 0 errors / 0 warnings.
- Pre-freeze self-challenge: PASS.

## Core curation decisions
- The complete game-by-game ledger, not the Quick Facts aggregate, controls the source-game population. The fact book's pre-2025-26 Quick Facts total is one loss lower than the mechanically summed season/game ledger; the detailed ledger is preserved rather than altered to force agreement.
- Three historical opponent-forfeit games preserve the on-court score/result in `played_result` and store `administrative_status=FORFEIT` separately.
- Exhibitions are excluded. The 2025-26 official schedule supplied 37 competitive games; two exhibitions are not in the package.
- H/A/N is independently curated and never inferred from physical venue alone.
- Final site split: 1,453 SOURCE_PROGRAM_HOME; 1,133 OPPONENT_HOME; 346 NEUTRAL; 0 UNKNOWN.
- Primary-home chronology used only after HOME classification: Margaret Hall Gym -> State Gym -> The Armory -> Hilton Coliseum.
- Required postseason site work is complete: NCAA, conference tournament, NIT, and the other postseason game have physical venue/city/state assignments.
- Regular-season neutral site audit is complete. Of 121 regular-season neutral games, 120 have exact physical venues; the 1970-12-19 Holy Cross game at the Marshall Tournament in Huntington, WV is the sole exact-building residual and is explicitly marked `RESEARCHED_UNRESOLVED` after targeted research rather than inferred from the preceding Marshall game.
- Rare territory/foreign normalized geography is not invented; source wording remains in raw/event provenance where project taxonomy does not support a durable normalized representation.

## Opponent identity closure
- 321 distinct literal source labels resolve to 300 canonical identities.
- Unresolved opponent identities: 0.
- Current-program key splits: 0.
- Ambiguous current-program matches: 0.
- Owner NON_D1 sanity scan: APPROVED 2026-09-04.
- Approved NON_D1 population: 54 distinct identities / 200 games.
- Meaningful self-corrections before owner scan included `San Fernando State -> Cal State Northridge` and `IUPUI -> IU Indianapolis`.
- `Cornell` in the historical Iowa series is Cornell College (Iowa); `Cornell (N.Y.)` is Cornell University.
- `Chicago` is University of Chicago, not a modern similarly named program.

## Conference history
Missouri Valley (1907-08–1927-28) -> Big Six (1928-29–1947-48) -> Big Seven (1948-49–1957-58) -> Big Eight (1958-59–1995-96) -> Big 12 (1996-97–present).

## Conference tournament workbook scope
The supplied `Conference_Tournament_Site_Reference(20260904-035740).xlsm` was **not** treated as Iowa State authority. The owner's authorization in this lane explicitly described North Carolina, so Iowa State conference membership/tournament research relies on Iowa State and other directly applicable sources.

## Research-lane venue identity
- Local physical venue rows in this candidate: 75.
- Definite current-main physical reuses at research freeze: 64.
- Genuinely new physical venue candidates: 11.
- Ambiguous physical identities: 0.
- Numeric global `venue_id` values are intentionally blank in research.
- Implementation must rebase venue identities against the then-current protected `main` before tracked Phase 0.


## Pre-freeze adversarial self-challenge
Status: **PASS**

The package was challenged as Control Center would challenge it:
- Unresolved HOME venue population: 0 / 1,453 HOME games.
- UNKNOWN H/A/N population: 0 / 2,932 games.
- Exact-date blanks: 0.
- NCAA physical venue/city/state gaps: 0 / 51.
- Conference-tournament physical venue gaps: 0 / 181.
- NIT physical venue gaps: 0 / 7.
- Other postseason physical venue gaps: 0 / 1.
- Regular-season neutral exact-building residuals: 1 / 121 (`ISURAW-01207`, Holy Cross, 1970-12-19, Marshall Tournament, Huntington WV); city/state and event are established, exact building is intentionally unresolved after targeted research.
- Venue identity review: 75 local physical identities = 64 definite current-main reuses + 11 genuinely new candidates + 0 ambiguous.
- Opponent identity closure: 0 unresolved identities; 0 current-program key splits; 0 ambiguous current-program matches. Owner-approved NON_D1 scan remains 54 identities / 200 games.
- Modern coverage check: completed 2025-26 season contains 37 competitive games, 29-8 on court, with 17 HOME / 10 OPPONENT_HOME / 10 NEUTRAL; two exhibitions remain excluded.
- Primary-home checksum: 33 Margaret Hall Gym + 300 State Gym + 266 The Armory + 854 Hilton Coliseum = 1,453 HOME games.

No new contradiction requiring owner judgment was found. The single researched-unresolved neutral building is non-NCAA, non-HOME, location-complete, and explicitly accounted rather than silently blank.

Mechanical package QA initially found a naming-only alias collision because three different buildings in Phoenix, Jacksonville, and Portland could all be shortened to `Veterans Memorial Coliseum`. The local aliases were disambiguated without changing any game-site assignment or physical identity; final QA then passed with 0 errors / 0 warnings.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=33f650d9174bebfb88d856d7e8ae3f3443852ec6` from `research_base_sha=602b344e59ea5aeadee9439a36a3cb2a3acb2813`. The authoritative final venue-ID mapping is recorded in the companion integration-freeze manifest. Deterministic current-schema migrations normalized MGM Grand Garden Arena physical geography to Paradise, Nevada; normalized the two Tokyo Aoyama Gakuin rows/venue to `Tokyo, JP`; and moved legacy site-research evidence from the gap-accounting columns into per-game notes whenever the row has no current material site gap. Literal source evidence remains preserved. Status: **INTEGRATION_FROZEN**.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=33f650d9174bebfb88d856d7e8ae3f3443852ec6` from `research_base_sha=602b344e59ea5aeadee9439a36a3cb2a3acb2813`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
