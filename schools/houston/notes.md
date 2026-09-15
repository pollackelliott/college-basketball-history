# Houston men’s basketball — Research portfolio notes

## Scope and controlling boundary

- Program key: `houston`
- Research base SHA: `0b8cf20e3b14517031a5a0e62b362883966e51c1`
- Top-level project scope: `1950-1951+`
- Competitive game universe: **2,291 games**, **1,437-854**, spanning **76 seasons (1950-1951 through 2025-2026)**.
- The extracted pre-scope 1946 through 1949-50 population is intentionally excluded from this six-file portfolio.
- The 2025-10-26 Mississippi State game at Fort Bend Epicenter was an exhibition and is excluded.

## Accepted research-stage controls

Stages 1 through 3B are accepted historical evidence for this portfolio. The Stage 4 files mechanically encode that accepted state; they do not reopen settled research.

Final H/A/N census:
- SOURCE_PROGRAM_HOME: **1,127**
- OPPONENT_HOME: **839**
- NEUTRAL: **325**
- UNKNOWN: **0**

Final postseason census:
- Conference Tournament: **102**
- NCAA Tournament: **79**
- NIT: **16**
- Other postseason (CBI): **6**

All **203/203 postseason games** have an exact physical venue and city/state. All **79/79 NCAA Tournament games** satisfy the project’s non-waivable NCAA site-completeness requirement.

## Regular-season site accounting

Every Houston HOME game has a resolved physical venue and complete Houston, Texas location.

Stage 6 adversarial review reduced the regular-season neutral material-gap population from **35 to 11** through systematic event/reciprocal venue recovery:
- **9** neutral rows retain supported domestic city/state but no safely established physical building.
- **2** Suntory Classic rows have the exact physical venue (Aoyama Gakuin University Gymnasium) but intentionally retain blank normalized city/state in `source-games.csv` under the accepted foreign-geography representation policy. The research-base venue identity itself is reused as `VEN-000487`.

The surviving 11 rows are explicitly classified as terminal researched historical/policy debt and retain `site_research_status=RESEARCHED_PARTIAL` plus substantive row-level `site_research_basis`. There are **0 unaccounted material site gaps**, **0 HOME publication blockers**, **0 UNKNOWN H/A/N rows**, and **0 NCAA/postseason site gaps**.

## Stage 3B correction overlays

Six genuine factual corrections were applied to the normalized fields while preserving the original source text in `raw_text`:

1. 1971 NCAA vs New Mexico State: **72-69** (not 77-69).
2. 1988 NIT vs Fordham: **69-61** (not 69-67).
3. 1988 NIT at Colorado State: **1988-03-22** (not March 18).
4. 2006 NIT at Missouri State: **2006-03-20** (not March 17).
5. 2009 Conference USA Tournament vs SMU: **85-76** (not 86-76).
6. 2025 NCAA vs SIU Edwardsville: **78-40** (not 70-48).

Five additional conflicts in Houston’s dedicated postseason summary tables were rejected as summary-table errors after corroboration; the controlling game ledger retained the stronger existing facts. These decisions are documented in the preceding Stage 3B audit package.

## Administrative-result semantics

Two Louisiana games preserve the on-court scored loss and carry `administrative_status=FORFEIT` plus the media-guide administrative note:
- 1971-12-06: on-court L 88-97; later won by forfeit.
- 1973-03-10: on-court L 89-102; later won by forfeit.

The project’s scored-result semantics remain on-court; the later administrative disposition is metadata rather than a score rewrite.

## Conference chronology

- 1950-1951 through 1959-1960: Missouri Valley Conference
- 1960-1961 through 1974-1975: Independent
- 1975-1976 through 1995-1996: Southwest Conference
- 1996-1997 through 2012-2013: Conference USA
- 2013-2014 through 2022-2023: American Athletic Conference
- 2023-2024 onward: Big 12

No Houston conference-tournament appearance exists before the Southwest Conference era in the accepted game universe. Houston’s first conference-tournament game is 1976-02-28 at Baylor in Waco.

## Postseason round curation

NCAA rounds use the repository’s controlled historical taxonomy:
`R64`, `R32`, `Sweet Sixteen`, `Elite Eight`, `Final Four`, `Championship`, with historical regional/final-four consolation games intentionally left blank.

Conference-tournament and NIT rows are blank except title games, which use `Championship`. Houston’s nine conference-tournament championship seasons in this portfolio are 1977-78, 1980-81, 1982-83, 1983-84, 1991-92, 2009-10, 2020-21, 2021-22, and 2024-25. The 1976-77 NIT title game is also marked `Championship`.

## Venue identity transport semantics

After Stage 6, `venues.csv` contains **117 physical venue rows**: **97** research-base global physical venue-ID reuses and **20** research-time new physical identities with blank numeric `venue_id`. Those blank IDs are intentional: current-main Implementation must rebase each durable venue key/name/geography and assign or reuse the authoritative global ID. No research-time physical identity is ambiguous.

Research-time new physical identities:
- `alumni-hall-navy` — Alumni Hall (Annapolis, MD)
- `civic-auditorium-san-francisco` — Civic Auditorium (San Francisco, CA)
- `cox-pavilion` — Cox Pavilion (Las Vegas, NV)
- `delmar-fieldhouse` — Delmar Fieldhouse (Houston, TX)
- `eaglebank-arena` — EagleBank Arena (Fairfax, VA)
- `h-pe-arena` — H&PE Arena (Houston, TX)
- `hammons-student-center` — Hammons Student Center (Springfield, MO)
- `hertz-arena` — Hertz Arena (Estero, FL)
- `joel-coliseum` — Joel Coliseum (Winston-Salem, NC)
- `lawlor-events-center` — Lawlor Events Center (Reno, NV)
- `los-angeles-sports-arena` — Los Angeles Sports Arena (Los Angeles, CA)
- `lubbock-coliseum` — Lubbock Coliseum (Lubbock, TX)
- `maples-pavilion` — Maples Pavilion (Stanford, CA)
- `montagne-center` — Montagne Center (Beaumont, TX)
- `nielsen-fieldhouse` — Nielsen Fieldhouse (Salt Lake City, UT)
- `reynolds-center` — Reynolds Center (Tulsa, OK)
- `rice-gymnasium-autry-court` — Rice Gymnasium / Autry Court (Houston, TX)
- `sam-houston-coliseum` — Sam Houston Coliseum (Houston, TX)
- `state-fair-arena-oklahoma-city` — State Fair Arena (Oklahoma City, OK)
- `indian-field-house-arkansas-state` — Indian Field House (Jonesboro, AR)

The research-base registry contains several duplicate-looking historical identities (notably Astrodome/Houston Astrodome and variant legacy venue keys). This Houston portfolio uses the deterministic identities already chosen in Stages 3A/3B. Implementation must perform the required current-main physical-identity rebase rather than creating a second local copy.

## Accomplishment controls for Implementation

The current project accomplishment baseline for Houston is consistent with the assembled evidence:
- 13 conference regular-season championships
- 9 conference-tournament championships
- 27 NCAA Tournament appearances through 2026
- 7 Final Four appearances
- 0 national championships
- best NCAA finish: national runner-up, latest in 2025

The supplied media guide directly reports 13 regular-season conference championships, 9 conference-tournament titles, 26 NCAA appearances through 2025, and seven Final Fours through 2025; the official completed 2025-26 schedule adds Houston’s 27th NCAA appearance. Final accomplishment verification remains an Implementation/Gate concern, not a Stage 4 mutation of global reference data.

## Stage 5 owner NON_D1 disposition

The owner reviewed the complete **28-identity working NON_D1 population** presented from the Stage 4 package and replied **“approved”** on **2026-09-13**. That approval applies to the exact Stage 4 owner-scan population; no unrelated identity inference is implied.

Stage 6 re-challenged opponent identity against the current global program registry and verified historical alias reference. No contradiction to the approved population was exposed:
- unresolved opponent identities: **0**
- known current-program key splits: **0**
- ambiguous current-program matches: **0**

## Stage 6 adversarial self-challenge

Stage 6 challenged the largest remaining debt class—the 35 regular-season neutral-site material gaps—rather than re-researching the accepted game universe.

Supported repairs/recoveries included:
- Oklahoma City All-College Tournament venue chronology: 1954, 1960, 1961, and 1963 Houston appearances assigned to Oklahoma City Municipal Auditorium; 1973 assigned to State Fair Arena.
- 1953 Western Kentucky game: normalized date corrected from 1953-12-29 to **1953-12-28** and physical site recovered as Jefferson County Armory in Louisville.
- 1953 Villanova game: normalized city corrected from Louisville to **Lexington, Kentucky**; exact building remains unresolved.
- 1966 Jonesboro Holiday Tournament: Indian Field House recovered for the Kent State and Arkansas State games.
- 1967 Rainbow Classic: Honolulu International Center Arena reconciled to the same physical building as the project’s Neal S. Blaisdell Center identity.
- 1969 UNLV Invitational: Las Vegas Convention Center recovered.
- 1978 Pillsbury Classic: Met Center in Bloomington recovered for both Houston games.
- 1979 Sun Carnival: Special Events Center reconciled to the project’s Don Haskins Center physical identity.
- 1983 Hall of Fame Tipoff Classic: Springfield Civic Center recovered.
- 1986 Kactus Klassic: ASU Activity Center reconciled to the project’s Desert Financial Arena physical identity.

The surviving **9 exact-building gaps** are limited to the 1953 Kentucky Invitational (Siena/Villanova), 1955 Birmingham Classic (two games), and 1956/1962/1968 Sugar Bowl Classic populations (five games). Those event classes were explicitly challenged; exact buildings varied by event/era or remained unsupported, so they are terminal researched historical debt rather than inferred assignments. The two Tokyo normalized-geography gaps are terminal policy debt.

The self-challenge also checked:
- HOME venue debt: **0**
- UNKNOWN H/A/N: **0**
- unknown exact dates: **0**
- NCAA physical venue/city/state gaps: **0**
- postseason material site gaps: **0**
- unaccounted material site gaps: **0**
- ambiguous physical venue identities: **0**

`PRE-FREEZE SELF-CHALLENGE: PASS`.

## Stage 6 status

The six required flat files remain assembled in current research-package shape:
`source-games.csv`, `opponents.csv`, `venues.csv`, `conferences.csv`, `notes.md`, `source-notes.md`.

Stage 6 is complete only as the bounded pre-freeze research state. Stage 7 remains separately owner-authorized work and will create/verify the immutable six-file `RESEARCH_FROZEN` transport package.

## Implementation Stage 1 current-main venue reconciliation

- Immutable RESEARCH_FROZEN ZIP SHA-256: `544f31b20333ae07ee9c2129aac5259d7a65b0764fc1acf821a8ba11213657c9`.
- The immutable Research artifact remains unchanged; this integration input applies only mechanically explicit current-main shared-reference supersessions.
- `coliseo-de-puerto-rico` / `VEN-000476` → `provisional-jose-miguel-agrelot-coliseum` / `VEN-000471` (Coliseo de Puerto Rico, San Juan, PR); resolved from current-main registered venue-name/alias identity and matching geography.
- `joel-coliseum` / `[blank]` → `ljvm-coliseum` / `VEN-000115` (Joel Coliseum, Winston-Salem, NC); resolved from current-main registered venue-name/alias identity and matching geography.
- `los-angeles-sports-arena` / `[blank]` → `los-angeles-memorial-sports-arena` / `VEN-000118` (Los Angeles Sports Arena, Los Angeles, CA); resolved from current-main registered venue-name/alias identity and matching geography.
- `rice-gymnasium-autry-court` / `[blank]` → `autry-court` / `VEN-000554` (Rice Gymnasium / Autry Court, Houston, TX); resolved from current-main registered venue-name/alias identity and matching geography.

## Implementation Stage 1 physical-locality reconciliation

- `mgm-grand-garden-arena` / `VEN-000133`: `Las Vegas, NV` source/research shorthand reconciled to canonical physical locality `Paradise, NV`. Literal source/event geography remains preserved separately.
- `michelob-ultra-arena` / `VEN-000135`: `Las Vegas, NV` source/research shorthand reconciled to canonical physical locality `Paradise, NV`. Literal source/event geography remains preserved separately.
- `orleans-arena` / `VEN-000356`: `Las Vegas, NV` source/research shorthand reconciled to canonical physical locality `Paradise, NV`. Literal source/event geography remains preserved separately.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=3989158d6e461a3dfb7be919586c5b388f8ef83d` from `research_base_sha=0b8cf20e3b14517031a5a0e62b362883966e51c1`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
