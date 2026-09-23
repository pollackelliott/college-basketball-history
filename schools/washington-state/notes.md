# Washington State curation notes

## Program status and coverage
Washington State men's basketball is curated from program inception in **1901-02** through completed **2025-26**.

Owner ruling: **INCEPTION+ / always top-level for site purposes.**
Research baseline: `3989158d6e461a3dfb7be919586c5b388f8ef83d`.

This is the Stage 4 research package. Research-time new global venue IDs are provisional until serialized Implementation rebases the frozen package against then-current protected `main`.

## Competitive history
- Competitive games: **3,351**
- On-court record: **1,718-1,633**
- Covered seasons: **125**
- 2025-26: **32 competitive games, 12-20**
- Exhibitions excluded: **3**
- Exact-date unknowns: **1**
- Unknown scores/results: **0**

The one exact-date unknown is the December 1914 Almira AC game (W 55-2); the source supports month only and the package leaves `game_date` blank rather than inventing a day.

## Material game-universe repairs
Accepted Stage 1 repairs are preserved without rewriting the source evidence:
- 1964-65: restored the omitted Feb. 26, 1965 game at Oregon State (L 51-66) and corrected the Oregon date to Feb. 27.
- 2017-18: restored Mar. 1, 2018 vs Oregon (W 78-76).
- 2023-24: corrected the season total to 25-10 / 35 games and the Jan. 4 Oregon State score to W 65-58.
- Four 1952-53 result-marker defects were normalized from supported scores/results.
- Winner-first score-display anomalies were normalized only after row-level audit.

## Administrative actions
Public/history results follow the on-court result. Two source-administrative forfeits are preserved separately:
- 1976-01-15 Oregon State: on-court L 73-82; later forfeited to Washington State.
- 1996-01-25 California: on-court L 79-87; later forfeited to Washington State.

## Opponent identity
Stage 2 resolves every game to a canonical opponent identity:
- 304 distinct canonical opponents
- 193 current-D1 identities
- 111 historical/non-D1 identities
- unresolved identities: 0
- known current-program key splits: 0
- ambiguous current-program matches: 0
- informational self-corrected current-program labels: 59

The formal owner NON_D1 sanity scan has **not** yet been approved; Stage 5 remains the required owner checkpoint.

## H/A/N and site completeness
Across the complete 3,351-game package:
- SOURCE_PROGRAM_HOME: 1,560
- OPPONENT_HOME: 1,524
- NEUTRAL: 267
- UNKNOWN: 0

Site classification is based on explicit/game-level evidence, never venue geography.

All source-program HOME rows have physical venue plus normalized city/state. All NCAA Tournament rows have physical venue plus normalized city/state.

There are **77 regular-season neutral games** with known normalized city/state but no safely supported unique physical building after deliberate research. They remain explicitly marked `RESEARCHED_PARTIAL`; they are researched historical debt, not unaudited blanks.

Three 2019 Cayman Islands Classic games have the physical building resolved as **John Gray Gym**. The current research-base global venue row for that physical identity carries an incorrect Kentucky geography. The school package therefore preserves the physical venue relationship but withholds normalized game city/state pending serialized current-main correction/rebase.

## Home venue chronology
Once HOME is independently established:
- 1901-02 through 1926-27: WSU Gymnasium / Temporary Union Building, Pullman, WA
- 1927-28 through 1972-73: Bohler Gym, Pullman, WA
- 1973-74 through 2025-26: Beasley Coliseum / Friel Court, Pullman, WA

Explicit off-campus home-game evidence overrides ordinary chronology; researched examples include Spokane Coliseum, Spokane Arena, and Toyota Center in Kennewick.

## Conference history
The accepted school timeline is:
- 1901-02 through 1908-09: Independent
- 1909-10 through 1915-16: Northwest historical conference identity
- 1916-17: Pacific Coast Conference
- 1917-18: Independent
- 1918-19 through 1958-59: Pacific Coast Conference
- 1959-60 through 1962-63: Independent
- 1963-64 through 1967-68: AAWU
- 1968-69 through 1977-78: Pacific-8
- 1978-79 through 2010-11: Pacific-10
- 2011-12 through 2023-24: Pac-12
- 2024-25 through 2025-26: WCC basketball affiliate

`PC North` source labels are treated as a PCC division, not a separate conference identity. The WCC interval ends at the package cutoff; current/future conference display is controlled separately by the project's current-membership reference.

## Postseason
Final postseason population: **85 games**
- Conference tournament: 36
- NIT: 17
- NCAA Tournament: 14
- Pacific Coast Conference playoffs: 11
- CBI: 6
- College Basketball Crown: 1

Stage 3B removed two provisional false-positive postseason rows (2007 Baylor and North Carolina A&T) caused by record-book cross-column footnote bleed and restored four omitted NIT rows (2009 Saint Mary's; 2011 Long Beach State, Oklahoma State, Northwestern).

All 14 NCAA Tournament games have complete physical site metadata. NCAA public round normalization follows the project historical-bracket convention; other postseason/public round values are blank except a verified title-deciding game.

## Accomplishment evidence
Washington State's researched on-court accomplishment baseline through 2025-26 supports:
- Regular-season/conference championships: **2**
- Conference tournament championships: **0**
- NCAA Tournament appearances: **7**
- Final Fours: **1**
- NCAA championships: **0**
- Best NCAA finish: **National Runner-Up**
- Best-finish year: **1941**

Washington State also recognizes the 1917 team as a retroactive **Helms national champion**. That historical honor is documented here but is not converted into an NCAA championship in the project's accomplishment field.

## Shared-reference proposals
The following research-time venue identities are historically resolved but require current-main registration during serialized Implementation:
- `VEN-000574` WSU Gymnasium / Temporary Union Building — **PROVISIONAL**
- `VEN-000575` Bohler Gym — **PROVISIONAL**
- `VEN-000576` Spokane Arena — **PROVISIONAL**
- `VEN-000577` Spokane Coliseum — **PROVISIONAL**
- `VEN-000578` Toyota Center (Kennewick, WA) — **PROVISIONAL**
- `VEN-000579` Idaho Central Arena — **PROVISIONAL**

The existing `VEN-000470` John Gray Gym physical identity is reused as a research-base match, but its global geography requires correction from the erroneous Kentucky representation to George Town, Cayman Islands during the serialized rebase.

## Known unresolved questions
No game identity, opponent identity, H/A/N, HOME venue, NCAA site, or ambiguous physical-venue identity is owner-blocked.

Permitted historical debt is explicitly represented in the row-level site-research fields. The required owner NON_D1 sanity scan remains pending Stage 5.

## Public presentation
The six-file package is research-complete through 2025-26 but is **not** authoritative global repository state. Final global venue IDs, shared-reference corrections, ingestion matches, and public enablement belong to serialized Implementation after RESEARCH_FROZEN.


## Stage 5 owner sanity scan

- Owner NON_D1 sanity scan: **APPROVED** on 2026-09-17.

## Integration freeze

Current-main rebase completed against `integration_base_sha=3d72b43ad4ed3af7be610cf39499c0972340e1c6` from `research_base_sha=3989158d6e461a3dfb7be919586c5b388f8ef83d`. Research conclusions remain frozen; deterministic current-main reference reuse, repository locality conventions, and the settled John Gray Gym shared-reference geography correction were reconciled for serialized Implementation. Status: **INTEGRATION_FROZEN**.
