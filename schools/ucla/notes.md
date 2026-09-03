# UCLA research portfolio notes

Status at creation: **RESEARCH_FROZEN**. Owner NON_D1 sanity scan approved on 2026-09-02; final adversarial/package QA passed before hashing.

- Program key: `ucla`
- Research base SHA: `6dc3910f68914c139097e9352481cb67a19cb2df`
- Owner history-scope ruling: **ALWAYS_TOP_LEVEL_FROM_INCEPTION**; accepted public history begins with UCLA basketball's 1919-20 season.
- Coverage: 1919-20 through completed 2025-26.
- Competitive games: **2,987**
- On-court record: **2,053-934**
- Exhibitions: excluded. The 2025-26 exhibitions at San Diego State (2025-10-17) and vs UC Irvine (2025-10-28) are not part of `source-games.csv`.

## Important historical rulings

The portfolio preserves **on-court results** separately from later administrative actions. UCLA lost 58-75 at Oregon State on 1976-01-10 and lost 93-100 to California on 1995-01-28; both opponents later forfeited those games. The source rows therefore retain `played_result=L` and record the forfeiture separately.

The supplied UCLA guide's 1920-21 season-summary line conflicts with its own eleven-game year-by-year ledger. The game ledger and independent contemporary reconstruction support a 9-2 recognized UCLA season. The separately documented Los Angeles Athletic Club loss that UCLA does not recognize is not added to the project game universe.

The early conference chronology is treated as SCIAC (1919-20 through 1926-27) followed by PCC beginning 1927-28, then AAWU, Pacific-8, Pacific-10, Pac-12, and Big Ten. The 1919-20 SCIAC line is documented with a nuance note because later retrospectives differ on the language of formal membership, while contemporary standings and UCLA's own conference record include Southern Branch.

## Exact-date research

The UCLA guide omits month/day on 498 games through 1944-45. Dedicated season reconstructions, reciprocal institutional histories, and UCLA/USC cross-checks recovered **220 of those 498 dates**. **278** rows remain without exact month/day. They are concentrated in the prewar era and are retained as genuine researched unknowns; no date is inferred from sequence, geography, or schedule pattern.

## Site-completeness self-challenge

- UNKNOWN H/A/N rows: **0**.
- NCAA Tournament physical-site gaps: **0** across **164** UCLA NCAA Tournament games in the portfolio.
- HOME rows with researched-unresolved physical building: **202**. These are confined to prewar UCLA home-facility debt where HOME and Los Angeles are independently established but the physical building cannot safely be assigned from the multi-facility chronology.
- Other explicitly researched unresolved material site rows: **10**.
- Unaccounted material site gaps: **0**.

The pre-Pauley facility chronology was used only after HOME classification had been independently established. UCLA's 1932-era Men's Gym history does not justify assigning every Los Angeles HOME row to that building: UCLA used multiple home-designated facilities, and the late-1950s/early-1960s period is explicitly multi-venue.

The 202 unresolved HOME buildings are concentrated in 1923-24 and 1928-29 through 1943-44. The ten other researched material site survivors are nine neutral regular-season rows with city/state but no safely recoverable building (1938 Ohio State and Nebraska in Berkeley; 1946 Wyoming in Buffalo; 1949 Santa Clara, 1951 Arizona, 1952 Saint Mary's/Santa Clara, and 1958 Saint Mary's/Santa Clara in the San Francisco area) plus the 1945 USC PCC Southern Division playoff whose UCLA H/A classification conflicts with a secondary building reconstruction. All ten carry substantive row-level research basis.

## Postseason taxonomy

Modern conference tournaments are `CONFERENCE_TOURNAMENT`; NCAA games are `NCAA_TOURNAMENT`; the 1985/1986 National Invitation Tournament games are `NIT`; older PCC/AAWU championship or NCAA-berth playoff games are `POSTSEASON`. Named in-season events remain `REGULAR_SEASON`. Conference-tournament/NIT/POSTSEASON rounds are blank except a verified title game, which receives `Championship`.

## Opponent identity

All source opponent labels are resolved in `opponents.csv`. Current-D1 identities are normalized to protected-main program identities; historical labels remain preserved in `source_opponent_label`. The owner reviewed the complete distinct NON_D1 population and approved it on **2026-09-02**.

## Venue identity

`venues.csv` contains research-lane physical identities only. Numeric global venue IDs are intentionally blank. **CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES.** Implementation must reconcile every physical venue against then-current main and reuse/allocate authoritative global identities.

## Accomplishments to verify/apply in Implementation

UCLA's authoritative program history supports 11 NCAA national championships (1964, 1965, 1967-1973, 1975, 1995), the 1985 NIT championship, and conference-tournament championships in 1987, 2006, 2008, and 2014. Program-card accomplishment values remain subject to Implementation's canonical cross-check and current-main reference update.

## Current-main integration rebase input

Original immutable RESEARCH_FROZEN ZIP SHA-256:
`c4c6957fbd29cd2c0e6e7a6f9b4e5f713e5fbd3d13a4ecef8d0c662cb1734608`

This derived integration input changes no game identity, date, opponent, score,
result, H/A/N classification, game type, or raw source evidence. It reconciles
research-time venue identities to current-main physical venue identities.

The Madison Square Garden research row was split because current main now carries
separate physical identities for MSG III (1925-1968) and MSG IV (opened
1968-02-11). UCLA games on 1968-01-26 and 1968-01-27 map to MSG III; UCLA games
from 1968-12-27 onward map to MSG IV.

The 1965-12-11 Charlotte Coliseum game maps to the 1955 physical building.

## Current-main physical-venue geography normalization

During serialized integration rebase, five exact-key venue identities used a
research-time locality differing from the authoritative current-main physical
venue geography. The derived integration input was normalized as follows:

- Bryce Jordan Center: University Park, PA -> State College, PA
- Eugenio Guerra Sports Complex: Bayamon, PR -> Bayamón, PR
- Imperial Arena: Paradise Island, Bahamas -> Nassau, BS
- MGM Grand Garden Arena: Las Vegas, NV -> Paradise, NV
- T-Mobile Arena: Las Vegas, NV -> Paradise, NV

These are current-main reference normalizations only. Game identity, date,
opponent, score/result, H/A/N, game type, and raw source evidence are unchanged.

## Current-main opponent and conference identity reconciliation

Two opponent identities were reconciled during implementation:

- `texas-a-and-m` -> `texas-a-m` for five Texas A&M games, matching the
  authoritative current global program identity.
- `western-colorado` -> `western-michigan` for the single 1940-41 UCLA
  43-56 road loss labeled "Western State". Western Michigan official
  all-time results independently record the reciprocal 56-43 home win over
  UCLA in 1940-41, confirming the physical institution identity.

Three historical conference keys were normalized to current-main registry keys:

- `pcc` -> `pacific-coast`
- `pacific-8` -> `pac-8`
- `pacific-10` -> `pac-10`

The UCLA SCIAC membership remains `sciac`; this is a legitimate historical
conference identity not yet present in the current-main global conference
registry and must be registered during Phase 0.

These changes do not reopen UCLA's game universe or repeat the completed
NON_D1 owner scan.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=ded80f39c52387c76d1667f75c548240b2d4883f` from `research_base_sha=6dc3910f68914c139097e9352481cb67a19cb2df`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
