# Baylor research notes

- Research base SHA: `33f650d9174bebfb88d856d7e8ae3f3443852ec6`.
- Current protected-main policy was re-inspected for Stage 6 at `0b8cf20e3b14517031a5a0e62b362883966e51c1`. Research conclusions remain anchored to the recorded research base; serialized Implementation must perform the authoritative current-main rebase.
- Program scope: `INCEPTION+`; accepted competitive history begins in 1906-1907.
- Controlling competitive universe through completed 2025-2026: **2,960 games; on-court record 1,515-1,445**. Exhibitions are excluded.
- Stage 1 accepted three exclusions: one 1912-13 season-bleed duplicate and the two explicitly labeled 2025-26 exhibitions. Literal source evidence for accepted rows remains preserved in `raw_text`.
- Stage 2 resolves all 2,960 games to opponent identity: **331 distinct canonical opponents**, including **102 distinct historical/non-current-D1 identities**. Unresolved opponent identities, known current-program key splits, and ambiguous current-program matches are all zero.
- Stage 5 owner NON_D1 sanity scan: **APPROVED**, 102 distinct NON_D1 identities reviewed, **0 owner flags**. The 39-entry informational self-corrected-opponent list was also presented.
- Final H/A/N through Stage 6: **1,531 SOURCE_PROGRAM_HOME / 1,082 OPPONENT_HOME / 347 NEUTRAL / 0 UNKNOWN = 2,960**.
- Final game-type partition: **2,822 REGULAR_SEASON / 73 CONFERENCE_TOURNAMENT / 42 NCAA_TOURNAMENT / 15 NIT / 8 POSTSEASON = 2,960**.
- **229** HOME rows from 1920-21 through 1937-38 retain `RESEARCHED_UNRESOLVED_HOME_VENUE`. Baylor HOME and Waco, TX are established. Baylor's institutional chronology says the program transitioned in the early 1920s to an open-air wooden structure before Marrs-McLean opened in 1938, but it does not safely allocate the transition game-by-game. Stage 6 found no new systematic evidence class, so this is terminal researched historical debt.
- Stage 6 repaired **8** neutral-site rows: the two 2020 Las Vegas games now use T-Mobile Arena / Paradise, NV, and all six 1987/2013 Maui rows now use Lahaina Civic Center / Lahaina, HI.
- Remaining non-NCAA neutral exact-venue debt is **184** rows; all have complete city/state after the Stage 6 Maui repairs and all are explicitly `RESEARCHED_PARTIAL`.
- Postseason physical venue/location research is complete except for the two 1948 NCAA District 6 playoff games versus Arizona: Dallas, TX is established but the exact building remains `RESEARCHED_PARTIAL`.
- NCAA strict site completeness remains **42/42** physical venue + city + state.
- Stage 6 challenged all **371** entering exact-date blanks against the one newly identified systematic high-yield class: published current-main reciprocal source packages. The class contained **97** Baylor blank-date games across Arkansas (40), Texas A&M (52), LSU (3), Kansas (1), and Oklahoma (1).
- That reciprocal batch recovered **32 exact dates**: **30 Arkansas** and **2 LSU**. No score/result/game-identity field was changed. The remaining **339** exact-date blanks are concentrated entirely in 1907-08 through 1945-46: 1900s 8, 1910s 84, 1920s 86, 1930s 102, 1940s 59.
- The **65** unrecovered rows inside the reciprocal batch were explicitly exhausted: Texas A&M's matching reciprocal rows also lack exact dates; the surviving Arkansas cases have reciprocal blank dates or material score conflicts; LSU's 1932-33 Baylor row is absent from its published season ledger; Kansas's 1935-36 season ledger has no Baylor row; Oklahoma's reciprocal Baylor row also lacks an exact date. No second comparable systematic source class remains apparent. The 339-date remainder is terminal researched historical date debt, not an unreviewed queue.
- Stage 6 reviewed recent NON_D1 identities and the owner-approved full NON_D1 census; no current-D1 alias/key split or ambiguous current-program match was exposed.
- The physical venue relationship table now contains **57** identities: **49** research-base global reuses and **8** research-local candidates. The eight research-local candidates were checked against the recorded research-base venue registry with no matching identity found; ambiguous physical venue identities remain zero.
- Research-time numeric venue IDs remain provisional. Current-main rebase is required before tracked Phase 0.
- Conference chronology remains Independent (1906-07 through 1913-14), Southwest Conference (1914-15 through 1995-96), Big 12 (1996-97 onward).
- Accomplishment research reference for Implementation remains **7 conference regular-season championships; 0 conference-tournament championships; 17 NCAA Tournament appearances; 3 Final Fours; 1 national championship; best finish NATIONAL_CHAMPION (2021)**. The media-guide Quick Facts line saying 16 NCAA appearances conflicts with its own detailed 17-season NCAA history; the accepted game-level partition remains controlling research evidence.
- Physical venue identity and geography never determine H/A/N.
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

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=d91f645f1055225b1de44ab471a0ba2345a25f0e` from `research_base_sha=33f650d9174bebfb88d856d7e8ae3f3443852ec6`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
