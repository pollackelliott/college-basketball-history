# Maryland research portfolio notes

## Scope and status

Maryland is treated as **always top-level/D1 for site purposes**. The public-history boundary is **1910-1911** (`ALWAYS_TOP_LEVEL_FROM_INCEPTION`).

The Maryland record book explicitly describes 1904-05 as an intramural/club season before the first official varsity team and therefore its two contests are excluded from this competitive package. The same record book's All-Time Results section begins the official varsity ledger with 1910-11. It includes the short 1910-11, 1912-13, 1913-14, and 1918-19 varsity eras before the program resumed continuously in 1923-24; those recognized competitive seasons remain in scope.

Coverage runs through the completed **2025-26** season. The 2025-10-27 UMBC contest is explicitly labeled an exhibition by Maryland Athletics and is excluded.

Final source-game universe:

- Competitive games: **2,875**
- On-court record: **1,704-1,171**
- Distinct source opponent labels: **314**
- Canonical opponent identities represented: **282**
- Unknown exact dates: **52**
- Unknown played scores: **12**
- H/A/N: **1,413 / 1,031 / 431**
- Venue rows: **89**

Game-type counts:

- `REGULAR_SEASON`: **2,624**
- `CONFERENCE_TOURNAMENT`: **154**
- `NCAA_TOURNAMENT`: **76**
- `NIT`: **21**
- `POSTSEASON`: **0**

## Conference chronology

- Independent: 1910-11 through 1922-23
- Southern Conference: 1923-24 through 1952-53
- ACC: 1953-54 through 2013-14
- Big Ten: 2014-15 onward

No-team gaps remain historical gaps rather than fabricated seasons.

## Site / H-A-N policy

Game-level source evidence controls H/A/N. `at` is opponent home; `vs.` is neutral; source-established home rows are Maryland home. Tournament geography never creates H/A/N by itself.

The record book sometimes uses literal `at` wording for games at an opponent's arena even when Maryland's current official historical schedule classifies the contest as neutral. Those cases are not resolved from geography. Where Maryland's official game-level historical schedule supplies an explicit H/A/N classification, that classification controls while the record-book wording remains preserved in `raw_text`. Examples include the 1944 and 1951 conference-tournament games against NC State in Raleigh, which are curated neutral despite the printed ledger's `at NC State` wording. The 1965 ACC Tournament semifinal at NC State remains `OPPONENT_HOME` because Maryland's official 1964-65 schedule itself classifies that game as away.

The 1918-19 narrative states that every game in the District Intercollegiate Basketball League was played at the Washington YMCA; all six rows are therefore neutral at that venue.

## Internal source reconciliation

The final pass compared the record-book ledger, year-by-year H/A/N summaries, Maryland's current official historical schedule pages, opponent-series pages, and contemporary Maryland recaps. The package preserves literal record-book claims in `raw_text` but corrects curated fields when stronger Maryland evidence establishes that the printed line is internally impossible or the initial PDF extraction crossed columns.

Material corrections made before freeze:

- **2008-02-20 Virginia Tech:** the record book prints `W 65-69`, an internally impossible result marker. Maryland's official contemporary recap confirms a **65-69 loss**; `played_result` is curated `L`.
- **2023-02-07 at Michigan State:** the record book prints `L 63-58`. Maryland's official schedule/recap confirms Maryland lost **58-63**; the curated score order is corrected.
- **2021-22 extraction repair:** an Old Dominion 85-67 row from 2020-21 had been duplicated into the 2021-22 extraction because of the record book's multi-column layout. Maryland's official 2021-22 schedule confirms the missing game was **2022-01-12 at Northwestern, W 94-87 (2OT)**. The contaminated duplicate was replaced before source-game IDs were frozen.
- **H/A/N reconciliation:** official Maryland historical schedule classifications were used for a finite set of site corrections, including St. John's (Annapolis) in 1937/1939, the 1949 Davidson game in Charlottesville, selected conference-tournament rows, Capital Centre games against George Washington/Georgetown, the 1978-79 NIT home-building games that Maryland classifies neutral, 1984 Wake Forest at Greensboro, four 1993-94 site classifications, 2000 Wisconsin in Milwaukee, and 2006 St. John's at Madison Square Garden.
- **1959-60 and 1997-98 aggregate conflicts:** Maryland's detailed official schedule pages disagree with the record book's printed year-summary H/A/N line. The detailed game-level schedule is retained rather than forcing rows to match the aggregate.

These are curated normalization corrections, not silent source rewrites; the source wording remains auditable row by row.

## Home-venue chronology

Venue chronology is applied only after a row is independently established as Maryland home:

- **The Gymnasium** (inside Annapolis Hall): 1923-24 through 1930-31
- **Ritchie Coliseum**: 1931-32 through 1954-55
- **Cole Field House**: 1955-56 through 2001-02
- **XFINITY Center**: 2002-03 onward

The early 1910-11 through 1913-14 home rows are not assigned a physical venue without sufficient game/facility evidence. The record book specifically notes that the 1913-14 team lacked a regular home after the 1912 fire.

## Conference tournaments

The owner-supplied `Conference_Tournament_Site_Reference(20260825-203717).xlsm` is globally incomplete, but the owner explicitly authorized its **Southern Conference, ACC, and Big Ten** sections as complete and reliable for Maryland. Those sections are used for physical conference-tournament venue/city/state assignments.

Conference-tournament public rounds remain blank except verified championship games. The package marks the 1931 Southern Conference championship game and Maryland's verified ACC championship/final appearances with `Championship` only when the row is the title game.

## NCAA Tournament

The package contains **76 NCAA Tournament games (46-30)** through 2025. All **76/76** NCAA rows have complete curated physical venue, city, and state.

NCAA rounds use the project's controlled vocabulary. The 1958 Manhattan regional consolation/third-place game remains `NCAA_TOURNAMENT` with a blank public round because it does not map honestly to the modern controlled round labels.

Physical identity is kept distinct where identical textual arena names would otherwise collapse separate buildings. In particular:

- 1958 Madison Square Garden is **Madison Square Garden III**, distinct from the current 1968 building.
- The 1955 and 1988 Charlotte Coliseum buildings are separate physical identities.
- historical naming-rights aliases are normalized to a single physical identity where supportable (for example MCI Center / Verizon Center -> Capital One Arena, Conseco / Bankers Life -> Gainbridge Fieldhouse, Carrier Dome -> JMA Wireless Dome, Sprint Center -> T-Mobile Center).
- the 1949 neutral Davidson game uses **Memorial Gymnasium (Virginia)** in Charlottesville, a distinct physical identity from the El Paso Memorial Gymnasium already represented in the package.

All numeric `venue_id` values in this research package are **provisional** and must be rebased against then-current main by the serialized Implementation lane.

## NIT

Maryland has **21 NIT games (14-7)** in the package. The 1972 championship win over Niagara is marked `Championship`; all other NIT public rounds remain blank. Preseason NIT games remain `REGULAR_SEASON`.

## Administrative history

Maryland's official record book states that the **1988 NCAA Tournament appearance was vacated by the NCAA**. Both 1988 NCAA game rows are marked `VACATED_GAME` while preserving the actual on-court score and result, consistent with project policy.

## Honest unknowns

There are **52** rows without an exact game date, concentrated in the early 1920s ledger plus the undated 1910-11 Widener game. These are not filled from modern archive pages that appear to use placeholder dates.

There are **12** known played losses with no score printed: eleven in 1913-14 and the 1944 Woodrow General Hospital game. Both score fields are blank atomically. No synthetic score is created.

## Research portability

`research_base_sha=2899c45e7b8dc2b8553c8b9e2342715a9a091484`

Research-time numeric venue IDs are provisional. The serialized Implementation lane must perform the authoritative current-main shared-reference/physical-venue rebase before `INTEGRATION_FROZEN`.

## Integration preparation provenance

The immutable RESEARCH_FROZEN transport artifact remains unchanged at SHA-256 `6e1d5f0f5be35fc7c4265a2ae7ee988265afd5d60d88332af73062cb57792fdd`. This derived integration-prepared package performs only current-main physical-venue identity/key/geography normalization needed before guarded Phase 0 staging. Source-era venue wording remains preserved in source evidence and/or row notes. The authoritative final global venue IDs are assigned only by `tools/stage_research_portfolio.py`.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=2899c45e7b8dc2b8553c8b9e2342715a9a091484` from `research_base_sha=2899c45e7b8dc2b8553c8b9e2342715a9a091484`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
