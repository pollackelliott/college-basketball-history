# Oregon State Men's Basketball — Research Package Notes

## 1. Status and cutoff
- Research base SHA: `3d72b43ad4ed3af7be610cf39499c0972340e1c6`.
- Competitive package: **3,325 games**, 1901-02 through 2025-26.
- Final played game in this package: 2026-03-09 vs. Gonzaga in the WCC Tournament.
- Stage 4 package assembly follows completed Stage 1, Stage 2, corrected Stage 3A, and corrected Stage 3B research.

## 2. Competitive record
- On-court wins: **1862**
- On-court losses: **1463**
- Played/on-court results are preserved separately from later administrative actions.

## 3. Exhibition treatment
No exhibition rows are included in the 3,325-row competitive package. Stage 4 does not add games outside the accepted Stage 1 universe.

## 4. Historical date and score exceptions
- **502** historical rows retain blank exact dates after the bounded Stage 6 reciprocal/institutional self-challenge; unsupported dates are not inferred.
- **3** rows retain incomplete/unresolved exact scores:
  - OSU-S1-000022 Portland YMCA: source-internal result/score conflict; played result retained, exact score blank.
  - OSU-S1-000368 Independence A.L.: source explicitly lists score `(NA)`.
  - OSU-S1-000385 Multnomah AAC: source explicitly lists score `(NA)`.
Unsupported dates or scores are not inferred.

## 5. Site and home-venue policy
- H/A/N is controlled independently from venue geography.
- Oregon State Men's Gymnasium is the accepted primary home venue for 1915-16 through 1948-49.
- Gill Coliseum is the accepted primary home venue beginning 1949-50.
- **77** ancient HOME rows remain valid `RESEARCHED_UNRESOLVED_HOME_VENUE` exceptions with owner-approved Corvallis, OR geography and blank physical building.
- Regular-season OPPONENT_HOME exact-building reconstruction is not forced where accepted evidence does not already provide it.
- After the Stage 3B partition correction, the regular-season NEUTRAL population is **241** rows: **194** exact venues and **47** researched/accounted venue-debt rows.

## 6. Shared venue handling
Venue never establishes H/A/N. Historical/source-era venue names are retained in `source_venue_name`; `curated_venue_name` follows the Stage 4 physical-identity rebase.

Six exact physical venues are historically resolved but absent from protected main and therefore have blank `venue_id` pending serialized Implementation:
- Chiles Center — Portland, OR
- Chinese Culture and Sports Center — Taipei, TW
- Cone Field House — Salem, OR
- Eugene Armory — Eugene, OR
- Shrine Auditorium — Los Angeles, CA
- Willamette Gymnasium — Salem, OR

Lexington Memorial Coliseum is also left without a selected global ID because protected main contains two apparent identities for the same physical building (`VEN-000129` and `VEN-000407`). Serialized Implementation must adjudicate that shared-reference duplication.

## 7. Conference chronology
- 1901-02 through 1914-15: Independent
- 1915-16 through 1958-59: Pacific Coast Conference
- 1959-60 through 1963-64: Independent
- 1964-65 through 1967-68: AAWU
- 1968-69 through 1977-78: Pac-8
- 1978-79 through 2010-11: Pac-10
- 2011-12 through 2023-24: Pac-12
- 2024-25 through 2025-26: WCC
- 2026-27 onward: Pac-12 (current reference membership; no 2026-27 games are in this package)

Named regular-season invitationals remain `REGULAR_SEASON`.

## 8. Postseason taxonomy
Corrected Stage 3B population: **119 rows**, all with exact venue/city/state.
- Conference tournaments: **40**
- NCAA Tournament: **36**
- NIT: **7**
- Other `POSTSEASON`: **36** (24 legacy postseason/PCC or Olympic-trials rows, 11 CBI, 1 College Basketball Crown)

Conference-tournament/NIT/POSTSEASON canonical rounds are blank except verified title games, which use `Championship`. NCAA rounds use only the project-controlled taxonomy. Historical NCAA consolation/third-place rows retain blank canonical rounds.

### Resume 46 partition correction
Resume 45 inherited a Stage 3A/3B partition defect: 2026-03-08 San Francisco and 2026-03-09 Gonzaga were still labeled regular season even though Oregon State's official schedule identifies both as the 2026 WCC Tournament. Resume 46 corrects both to `CONFERENCE_TOURNAMENT`; their accepted NEUTRAL/Orleans Arena site conclusions are unchanged.

## 9. Administrative actions
**17** rows carry `FORFEIT` administrative status. The 1975-76 Oregon State forfeitures and two 1995-96 California forfeits preserve the actual played result/score and record the later administrative action separately.

## 10. Opponent reconciliation
All opponent identities are resolved at the package level.
- Distinct canonical opponents: **369**
- Current D-I identities: **219**
- NON_D1 identities: **150**
- All 219 current-D1 keys used by Oregon State were verified against protected-main `programs.csv` at the research base.

The literal label `Pacific` is contextually split between current-D1 Pacific and historical Pacific University (Oregon); `opponents.csv` preserves both mappings with non-overlapping research context.

## 11. Known unresolved historical facts
- 116 regular-season rows retain researched/accounted `UNKNOWN` H/A/N.
- 77 HOME rows retain blank exact building under the ancient-home safety valve.
- 45 regular-season neutral rows retain researched/accounted exact-venue debt after the completed Stage 6 systematic self-challenge.
- The six new physical venues and Lexington Memorial Coliseum duplicate are Implementation shared-reference handoff items, not unfinished Oregon State historical research.

## 12. Public presentation
Opponent and venue public labels come from canonical package/shared identities, not prettified keys. Source-era labels remain preserved as source/provenance aliases.

## 13. Owner NON_D1 sanity scan
The complete Stage 5 owner sanity scan was approved with no flagged identities.
- Distinct NON_D1 identities reviewed: **150**
- Games represented: **418**
- Owner-flagged identities remaining: **0**

This approval applies to the exact Resume 46 owner-scan population preserved in the durable Research checkpoint. Stage 5 did not change opponent identity research.

## Stage 6 pre-freeze self-challenge — COMPLETE
The adversarial self-challenge is complete. It remained a bounded class-level audit rather than a second research cycle.

Accepted cumulative Stage 6 repairs include the Hec Edmundson Pavilion recovery, Portland neutral-location correction, California H/A/N contradiction adjudication, **28** exact-date recoveries, and one final neutral exact-venue recovery: `OSU-S1-002511` (2000-12-16 vs Wyoming) to **Casper Events Center**, Casper, WY. The Wyoming recovery is supported by institutional event evidence identifying the game as the Cowboy Shootout and the University of Wyoming/City of Casper agreement requiring that annual tournament to be held at Casper Events Center; current protected main reuses `VEN-000469`.

Final challenged residual populations:
- `RESEARCHED_UNRESOLVED_HOME_VENUE`: **77** — terminal researched HOME-venue debt after systematic reciprocal challenge.
- `UNKNOWN` H/A/N: **116** — terminal researched historical H/A/N debt after systematic published-current-main reciprocal challenge.
- blank exact dates: **502** — terminal researched historical date debt after **28** Stage 6 recoveries and exhaustion of reciprocal/Idaho/post-Idaho institutional opportunities.
- regular-season NEUTRAL exact-venue debt: **45** — terminal researched venue debt after current-main reciprocal and event/host-family systematic challenge; **1** Stage 6 venue recovery.
- postseason physical-site gaps: **0**.
- NCAA physical venue/city/state gaps: **0**.
- open specific contradictions: **0**.

The neutral-venue challenge explicitly preserved unresolved rows where only event city, host arena chronology, or another edition's venue was available. In particular, the 1991 Far West Classic remains venue-unresolved because official histories establish the event's Portland/Memorial Coliseum history and the 1991 return but do not directly identify the 1991 building; venue continuity is not substituted for exact-game support. Likewise, host-arena chronology is not used to assign the 1973 Mountaineer Classic or 1982 River City Tournament rows.

Final self-challenge acceptance census: research-accounted HOME venue blanks **77/77**; HOME location gaps **0**; `UNKNOWN` rows with substantive accounting **116/116**; regular-season neutral material gaps research-accounted **45/45**; postseason site gaps **0**; NCAA site gaps **0**; unresolved opponent identities **0**; known current-program key splits **0**; ambiguous current-program identity matches **0**; owner NON_D1 sanity scan **APPROVED**; open Stage 6 contradictions **0**; Stage 3A/3B partition remains **3,206 + 119 = 3,325**.

`PRE-FREEZE SELF-CHALLENGE: PASS`

Stage 6 is complete. Stage 7 performed only final research-metadata normalization and immutable packaging; no game identity, opponent identity, score, result, date, H/A/N, venue/site conclusion, conference membership, postseason classification, or accomplishment conclusion changed.

`RESEARCH_FROZEN: YES`  
`CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=5c91e35485060a0be27f9612d0b140883a555dbf` from `research_base_sha=3d72b43ad4ed3af7be610cf39499c0972340e1c6`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
