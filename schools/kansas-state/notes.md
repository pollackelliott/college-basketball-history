# Kansas State research notes

- Research base SHA: `de0c67405881b7be716c93ecb46f6ae2ea8e29ca`.
- Owner/project history scope: Kansas State is treated as top-level from program inception for site purposes; competitive history begins with 1902-03.
- Controlling competitive universe through completed 2025-26: **3,038 games; on-court record 1,759-1,278-1**. Exhibitions are excluded.
- Stage 1 reconciled every played season to the authoritative season-level game count. The media guide's 1999-00 detailed ledger omission was restored from Kansas State's official archived schedule (28 games, 9-19).
- The institutional all-time aggregate printed through 2024-25 (1,756-1,255 / 3,011 games) does not reconcile to Kansas State's own 121 annual season lines. Those annual lines and the reconstructed detailed ledger independently total 3,006 games through 2024-25. The five-game aggregate discrepancy is documented rather than filled with invented contests.
- Two score corrections are preserved from Stage 1: 1908-09 Nebraska is Kansas State L 31-36, and 2003-04 Oregon State is Kansas State L 82-87.
- Administrative results preserve on-court truth separately: the 1909-10 Kansas City Athletic Club 41-41 crowd forfeit remains an on-court tie with FORFEIT metadata; the 1976-77 Minnesota 60-62 loss remains the on-court result with the later NCAA forfeit separately noted.
- One exact date remains researched unknown: the 1934-35 road loss to Oklahoma City, 27-36; Kansas State's current and archived year-by-year material print `NA`.
- Stage 3B corrected the 2014 NCAA Tournament loss to Kentucky to **2014-03-21**. This is a date-field correction overlay only; the accepted Stage 1 game identity remains unchanged.
- Stage 4 package QA exposed one impossible source date token: the 1921-22 home loss to Drake was printed/extracted as `F29`, but 1922 was not a leap year. Kansas State's official 1921-22 schedule and Drake opponent history establish **1922-03-01**. This is a date-field correction overlay only; game identity, opponent, score, result, H/A/N, and venue are unchanged.
- Stage 2 resolves every opponent identity. The 3,038 rows represent 326 canonical opponent identities; unresolved opponent identities = 0, current-program key splits = 0, ambiguous current-program matches = 0.
- The working NON_D1 population is 72 distinct canonical identities representing 303 games. The required owner NON_D1 sanity scan is prepared but **not yet approved**.
- Final full-history H/A/N census after Stage 3A + Stage 3B: **1,498 SOURCE_PROGRAM_HOME / 1,150 OPPONENT_HOME / 390 NEUTRAL / 0 UNKNOWN**.
- Stage 3A regular-season/basic-site population: 2,861 games. Exactly 43 source-program HOME rows, all before Nichols Gym, retain `RESEARCHED_UNRESOLVED_HOME_VENUE`; Manhattan, KS is established but the individual physical building is not.
- Exactly eight regular-season NEUTRAL rows retain a researched unresolved physical building while their H/A/N and locality are established.
- Stage 3B postseason population: 177 games = 86 conference tournament + 76 NCAA Tournament + 15 NIT. NCAA physical venue/city/state completeness is 76/76.
- Kansas State principal home chronology: pre-Nichols Manhattan homecourts are multiple/unrecoverable at the individual-game level; Nichols Gym (1910-11 through 1949-50); Ahearn Field House (opened 1950-12-09; principal home through 1987-88); Bramlage Coliseum (opened 1988-11-26; principal home thereafter), with documented alternate-home games handled game-by-game.
- Physical venue identity never determines H/A/N. H/A/N remains sourced independently even when venue identity is known.
- Stage 4 research-base venue reconciliation reduces the accepted 75 physical venue identities to **69 research-base registry reuses and six research-time new identities**. Numeric global IDs for the six new identities remain blank/provisional pending the mandatory current-main rebase.
- The six research-time new physical identities are Nichols Gym, José Miguel Agrelot Coliseum, John Gray Gym, Oakland Arena, Casper Events Center, and Mobile Civic Center.
- Stage 4 mechanically rebased stale research-time venue candidates to identities already present at the research base, including Sports and Fitness Center, Lahaina Civic Center, Orleans Arena, Don Haskins Center, Stan Sheriff Center, Veterans Memorial Coliseum (Portland), Sullivan Arena, Baha Mar Convention Center, Selland Arena, Suncoast Credit Union Arena, Thomas & Mack Center, Prudential Center, Lloyd Noble Center, Orlando Arena, PPG Paints Arena, Pontiac Silverdome, Reunion Arena, Reynolds Coliseum, Richmond Coliseum, St. Louis Arena, Palestra, University of Dayton Arena, and Schollmaier Arena.
- Daniel–Meyer Coliseum is normalized to the existing Schollmaier Arena physical identity after a narrow Stage 4 registry-reconciliation check; TCU Athletics explicitly states that the Daniel-Meyer facility was renovated and renamed Schollmaier Arena.
- Current-main rebase remains required before tracked Phase 0. No research-time numeric venue ID is final merely because it matches the pinned research base.

## Stage 4 boundary

This six-file portfolio is assembled and package-QA'd only through readiness for the required owner NON_D1 sanity scan. It is **not** `RESEARCH_FROZEN`, has not received owner NON_D1 approval, and has not undergone the final adversarial pre-freeze self-challenge or immutable ZIP/hash step.

- Owner approved the complete Kansas State NON_D1 sanity scan on **2026-09-06**; no identities were flagged.

## Integration-rebase physical venue resolution — HP Field House

Current-main physical-identity reconciliation confirmed that the research
portfolio's `hp-field-house` is the same physical venue as global
`VEN-000084`. The immutable research package used `Lake Buena Vista, FL`;
current global canonical venue geography uses `Orlando, FL`. The integration
venue-registry row is normalized to the current project canonical locality
`Orlando, FL` solely for shared-reference compatibility. The underlying game
rows retain their researched/source locality `Lake Buena Vista, FL`. This is
an integration normalization, not a change to game identity, H/A/N, venue
identity, or historical research.

## Integration-rebase physical venue resolution — Oakland Arena

Current-main physical-identity reconciliation confirmed that the research
portfolio's provisional `Oakland Arena` identity is the existing global
physical venue `VEN-000153`, whose project canonical key is
`oakland-coliseum-arena` and whose project display is `Oakland Coliseum Arena`.
Current `venue-names.csv` already registers `Oakland Arena` as a historical
or alias name for VEN-000153. The integration transport therefore replaces
the provisional venue key with `oakland-coliseum-arena`. This is shared-
reference reconciliation only; the two Kansas State game identities, dates,
scores, H/A/N classifications, Oakland locality, and source evidence are
unchanged.


## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=4412742a67e980a92ba8075ce5df38e29aa5bd2c` from `research_base_sha=de0c67405881b7be716c93ecb46f6ae2ea8e29ca`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

## IMPLEMENTATION-DISCOVERED RESEARCH REOPEN — 1907 KANSAS

Implementation Stage 2 exposed one genuine omission in the immutable
RESEARCH_FROZEN ledger: Kansas State's current institutional series history
identifies Jan. 25, 1907 as the first Kansas meeting and records a 39-54 road
loss; Kansas's current institutional game history independently records the
reciprocal 54-39 game in Lawrence.

The immutable RESEARCH_FROZEN ZIP and its recorded SHA-256 remain unchanged as
provenance. The corrected working Kansas State source ledger supersedes the
frozen package's game-count headline and now contains 3,039 competitive games
with an on-court record of 1,759-1,279-1.
