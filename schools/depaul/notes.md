# DePaul research notes

- Research base SHA: `421e6f12991aff3f695f76a1079321788a56674f`.
- Program scope: DePaul is treated as top-level from program inception for project purposes; accepted competitive history begins in 1923-1924.
- Controlling competitive universe through completed 2025-2026: **2,706 games; on-court record 1,546-1,160**. Exhibitions are excluded.
- Stages 1-5 remain controlling except for the narrow Stage 6 correction overlays documented below. Literal source labels and `raw_text` are preserved.
- Stage 5 NON_D1 owner sanity scan was approved clean for **109** distinct canonical identities. During Stage 6 the owner additionally identified the literal 1973-1974 `California State` row as **Cal State Hayward / present-day Cal State East Bay**, historical/non-current-D1. The final game-level NON_D1 population therefore uses **110 distinct canonical identities**; this added identity was directly owner-dispositioned rather than inferred.
- All 2,706 games now have a canonical opponent identity at game level. The literal `[OPPONENT UNKNOWN]` source label remains on the two aggregate-proven added rows, but Stage 6 resolved those rows individually to Bradley (1940-1941) and Baldwin Wallace (1957-1958); the label therefore has no single label-level canonical mapping.
- Final opponent game population: **2,358 current-D1 games / 348 historical-non-D1 games / 0 unresolved opponent games = 2,706**.
- The historical same-label `Augustana` population remains intentionally split by season context: 1926-1927 -> Augustana (IL); 1967-1968 -> Augustana (SD).
- `Wisconsin State` remains normalized to **UW-Superior**.
- Final H/A/N after Stage 6: **1,471 SOURCE_PROGRAM_HOME / 997 OPPONENT_HOME / 230 NEUTRAL / 8 UNKNOWN = 2,706**.
- The eight surviving UNKNOWN H/A/N rows were adversarially challenged and remain explicit `RESEARCHED_UNRESOLVED`; no geography/series-pattern inference was used.
- **12** SOURCE_PROGRAM_HOME rows retain `RESEARCHED_UNRESOLVED_HOME_VENUE`: the seven 1947-1948 Lane Tech/De La Salle allocation rows plus five additional early HOME rows exposed/resolved during Stage 6. Chicago, IL is established for all 12; exact individual building assignment is unsupported.
- **18** regular-season NEUTRAL rows retain researched unresolved exact-venue identity; only one also retains unresolved locality. All material site gaps are explicitly research-accounted.
- Stage 3B postseason population remains **133 games = 46 NCAA / 34 NIT / 45 conference tournament / 8 other postseason**. Postseason exact physical venue + city/state completeness remains **133/133**; NCAA strict completeness remains **46/46**.
- Stage 6 repaired the 1940-1941 aggregate-proven loss to **1941-03-05 at Bradley, DePaul 41-43, Peoria Armory, Peoria, IL**.
- Stage 6 repaired the 1957-1958 aggregate-proven row field-specifically to **1958-02-08 Baldwin Wallace 67, DePaul 62**. H/A/N and physical venue remain explicitly researched unresolved.
- Stage 6 repaired Motor City Classic venue identity to the **University of Detroit Memorial Building / present Calihan Hall** for 1961-12-29 and 1961-12-30, and Oklahoma City Tournament venue identity to **Oklahoma City Municipal Auditorium** for 1966-12-27, 1966-12-29, and 1966-12-30.
- Stage 6 recovered/corrected the documented H/A/N/site fields summarized in the supporting repair and debt ledgers without reopening settled earlier-stage populations.
- Exact-date debt entering Stage 6 was **197 rows**. Stage 6 recovered **18 exact dates** total, leaving **179** explicit historical exact-date blanks: **82 in the 1920s, 69 in the 1930s, and 28 in the 1940s**.
- The terminal exact-date self-challenge used one systematic high-yield batch: all Checkpoint-13 residual rows whose opponent already has a published current-main source package. That class comprised 11 rows across 9 published opponents; **8 dates were recovered**. The remaining Nebraska, Washington, and Oklahoma reciprocal rows did not provide a uniquely supported exact date. No 179-row one-off search campaign was performed.
- After that batch, the 179 remaining dates are accepted as **researched historical exact-date debt**, not as an unreviewed queue. Exact dates were never inferred from row order, geography, customary series timing, or season chronology.
- The final venue relationship table contains **90 rows**: the Stage 4 88 plus two Stage 6 repair identities (Peoria Armory and University of Detroit Memorial Building/Calihan Hall). The 14 original research-local identities were fully challenged at Checkpoint 13; the two Stage 6-added identities were likewise found non-ambiguous. Numeric global IDs remain provisional until serialized current-main Implementation rebase where applicable.
- Physical venue identity never determines H/A/N.
- Current-main rebase remains required before tracked Phase 0.

## Stage 6 boundary

`PRE-FREEZE SELF-CHALLENGE: PASS`

Research acceptance errors: **0**  
Research acceptance warnings: **0**  
Unresolved opponent identities: **0**  
Known current-program key splits: **0**  
Ambiguous current-program matches: **0**  
HOME publication blockers: **0**  
NCAA site gaps: **0**  
Unaccounted material site gaps: **0**  
Ambiguous physical venue identities: **0**

Stage 6 is complete. Stage 7 immutable package construction has **not** begun.

## Implementation Stage 1 current-main rebase

- `research_base_sha`: `421e6f12991aff3f695f76a1079321788a56674f`
- `integration_base_sha`: `ffbef04a4045d4bddecb8e9c0437f31ec7834070`
- Research acceptance remains clean under current tooling.
- Six research-local venue keys were normalized to project-global keys; all 16 provisional physical venue identities are reconciled to the current-main allocation beginning at `VEN-000496`.
- The Conference USA interval was mechanically normalized from local key `conference-usa` to current global key `cusa`; historical display `Conference USA` is preserved.
- Owner explicitly approved the historical global conference identity `great-midwest` / `Great Midwest`, tournament label `Great Midwest`, status `historical`.
- Shared/global identity reconciliation is complete with **0 ambiguous current-main matches**.
- Status: **INTEGRATION_FROZEN**.
- Tracked Phase 0 has **not** begun.
