# Texas Tech men's basketball research notes

## Status
- School: Texas Tech
- Source program key: `texas-tech`
- Research base SHA: `33f650d9174bebfb88d856d7e8ae3f3443852ec6`
- Owner-confirmed history scope: `INCEPTION+`
- First covered season: 1925-26
- Final covered season: 2025-26
- Competitive games: 2,773
- On-court record: 1,578-1,195
- Stages 1-3B: COMPLETE
- Stage 4 mechanical package QA: PASS
- Stage 4 owner registry decision: COMPLETE — `border-conference` / Border Conference / `Border`
- Stage 5 owner NON_D1 sanity scan: APPROVED — 0 flags
- Stage 6 pre-freeze self-challenge: PASS
- RESEARCH_FROZEN: YES
- CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES

## Core curation decisions
- The official 2026-27 Texas Tech record book year-by-year ledger controls the 2,773-game competitive universe.
- Owner scope is `INCEPTION+`; the former 1950-51 project cutoff is superseded for this research.
- Exhibitions/noncompetitive events are excluded.
- Played/on-court record remains 1,578-1,195.
- Administrative actions remain separate: 11 1996-97 on-court wins are `FORFEIT`; the 1995-96 NCAA run has two `VACATED_WIN` rows and one `VACATED_GAME` row while preserving played results.
- H/A/N was independently curated and never inferred from venue.

## Site research
- Final all-game H/A/N: 1,325 SOURCE_PROGRAM_HOME / 1,093 OPPONENT_HOME / 355 NEUTRAL / 0 UNKNOWN.
- HOME chronology: Aggie Judging Pavilion (1925-26) -> Tech Gym (1926-27 through 1955-56) -> Lubbock Municipal Coliseum (1956-57 through 1998-99) -> United Supermarkets Arena physical building (1999-00 onward).
- Verified alternate HOME exception: 2017-12-16 vs Rice at Lubbock Municipal Coliseum.
- HOME rows missing venue/location: 0.
- Regular-season neutral: 151 exact physical venues + 52 explicitly `RESEARCHED_PARTIAL` exact-building unknowns.
- Postseason: NCAA 46/46 exact venue+city/state; NIT 10/10 exact venue+city/state; 15 conference/other postseason exact-building residuals are explicitly researched/accounted with complete location.
- Material site gaps are research-accounted; unaccounted site gaps = 0.

## Postseason corrections
- 1943 Border tournament: Arizona official evidence corrects the nearby Tucson heading to Albuquerque and establishes the two Arizona games as neutral; exact building remains deliberately unresolved.
- 1962 SWC playoff vs SMU: Daniel-Meyer Coliseum, Fort Worth.
- 1962 NCAA vs Air Force: Moody Coliseum, Dallas, not the nearby Manhattan heading.
- 1976 NCAA vs Syracuse: normalized date 1976-03-13 at UNT Coliseum, Denton; literal Texas Tech raw text is preserved.
- 1943 and 1946 Arizona reciprocal date disagreements were reviewed without overwriting the Texas Tech primary dates.

## Opponent identity
- 913 distinct literal source labels resolve to 309 canonical opponent identities.
- Unresolved opponent identities: 0.
- Current-program key splits: 0.
- Ambiguous current-program matches: 0.
- Working NON_D1 population: 70 identities / 376 games.
- Formal owner NON_D1 sanity scan: **APPROVED 2026-09-12; 0 owner flags**.
- Informational self-corrected identity list is preserved in the Stage 5 checkpoint.

## Conference history
Independent (1925-26–1931-32) -> Border Conference (1932-33–1955-56) -> Independent transition (1956-57) -> Southwest Conference (1957-58–1995-96) -> Big 12 (1996-97–present).

### Central-registry blocker
The owner approved `border-conference` / `Border Conference` / tournament label `Border` on 2026-09-12. That historical identity is registered on protected `main` in commit `0b8cf20e3b14517031a5a0e62b362883966e51c1`.

## Program-accomplishment verification
The Texas Tech official record book verifies 13 regular-season conference titles (6 Border + 6 SWC + 1 Big 12), 5 conference-tournament titles, 22 NCAA appearances, 1 Final Four, 0 NCAA championships, and NATIONAL_RUNNER_UP (2019) as best finish. This exposes two owner-baseline reference corrections for Implementation: regular-season conference titles 12 -> 13 and NCAA appearances 23 -> 22.

## Research-lane venue identity
- Local physical venue rows: 87.
- `venue_id` is intentionally blank throughout.
- Same-building historical aliases are locally normalized only where physical continuity is established.
- Oklahoma City Municipal Auditorium and Kansas City Municipal Auditorium are distinct physical identities and are not merged.
- Texas Tech's Madison Square Garden assignments are all post-1968 and use the current-Garden physical identity key.
- Serialized Implementation must perform the authoritative current-main venue rebase.

## Known owner question
No owner-level research blocker remains. The surviving 59 material site-gap rows are explicitly researched/accounted terminal historical debt and do not require owner disposition.

## Stage 6 pre-freeze adversarial self-challenge
**PRE-FREEZE SELF-CHALLENGE: PASS**

Bounded repairs:
- 8 previously researched-partial SWC preseason-tournament neutral games (1957-60) recovered to **Autry Court, Houston** from Rice official tournament history.
- 3 1946 Houston Intercollegiate games normalized from historical building label **Public School Fieldhouse** to current physical identity **Jeppesen Fieldhouse**, preserving the historical alias.
- normalized locality repairs aligned supported physical identities to current-main conventions: Hard Rock Hotel Riviera Maya Convention Center -> Puerto Aventuras, MX; Imperial Arena -> Nassau, BS; Thomas & Mack Center -> Las Vegas, NV.

Final debt:
- `RESEARCHED_UNRESOLVED_HOME_VENUE`: 0
- `UNKNOWN` H/A/N: 0
- unknown exact dates: 0
- material site-gap rows: 59
- research-accounted material site-gap rows: 59
- unaccounted material site-gap rows: 0
- NCAA site gaps: 0
- remaining blank-venue population is terminal researched historical debt after bounded institutional/event/reciprocal challenge; no comparable systematic high-yield source class remained.

Physical venues:
- local physical venue rows: 88
- definite research-base reuses: 38
- additional definite current-main reuses: 38
- genuinely new current-main physical candidates: 12
- ambiguous physical identities: 0

Opponent identities:
- modern/current-snapshot NON_D1 identities specifically challenged: 5 identities / 9 games
- current-program key splits found: 0
- ambiguous current-program matches: 0
- Stage 5 owner approval remains controlling.

Current-main observed at Stage 6 closeout: `0b8cf20e3b14517031a5a0e62b362883966e51c1`.

## Stage 7 immutable freeze
- Final research package contains exactly six flat files.
- Stage 5 owner NON_D1 disposition is accepted with 0 flags.
- Stage 6 adversarial self-challenge passed with research acceptance errors = 0 and warnings = 0.
- `RESEARCH_FROZEN: YES`.
- `CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`.
- Numeric/global venue IDs remain provisional until serialized Implementation performs the authoritative current-main rebase.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=e5078cd6b57d68f59048f32b7dace422544eff9f` from `research_base_sha=33f650d9174bebfb88d856d7e8ae3f3443852ec6`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
