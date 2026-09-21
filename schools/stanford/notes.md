# Stanford Men's Basketball — Research Portfolio Notes

## Status

- School: Stanford
- Source program key: `stanford`
- Research scope: `INCEPTION+`
- Research base SHA: `3989158d6e461a3dfb7be919586c5b388f8ef83d`
- Package lifecycle status: **RESEARCH_FROZEN**
- Current next gate: serialized Implementation acceptance/current-main rebase (Research lane complete)
- Current-main rebase required later in serialized Implementation: **YES**

## Competitive game universe

- Competitive games: **2,917**
- On-court record: **1,650-1,267**
- Played seasons: **111**
- No-team seasons: **1943-1944 and 1944-1945 (World War II)**
- Unknown exact dates: **636**
- Unknown played scores: **3**
- Unknown played results: **0**
- Exhibitions are excluded.
- The 2025-10-30 Oregon exhibition is not part of the competitive ledger.

The three unknown scores are all official Stanford-recognized 1913-14 games:
- at Huntington Beach HS — W, score unknown
- at Orange AC — W, score unknown
- at Los Angeles AC — L, score unknown

## Administrative-result policy

The package preserves **on-court** results.

- 1996-03-03 at California remains Stanford's on-court **69-85 loss** even though California later forfeited the game administratively. This explains the one-game difference between the row-level 1995-96 on-court record and Stanford's administrative season summary.
- Two 1975-76 Oregon State wins carry administrative-forfeit notes because Oregon State later forfeited due to an ineligible player; Stanford had already won both games on the court.

## H/A/N and site research

All 2,917 games have accepted H/A/N:
- HOME: **1,493**
- AWAY: **1,090**
- NEUTRAL: **334**
- UNKNOWN: **0**

Corrected Stage 3B partition:
- Regular season: **2,793**
- Postseason: **124**

### Stanford HOME chronology

- 1913-14: HOME in Stanford, CA established; exact outdoor court remains researched-unresolved.
- 1914-15: HOME in Stanford, CA established; exact building remains researched-unresolved across the 1915 Encina transition.
- 1915-16 through 1919-20: **Encina Gymnasium**.
- 1920-21: Stanford, CA established; mixed Encina/open-air facility use prevents safe row-level building assignment.
- 1921-22 transition: 1922-01-11 Santa Clara at Encina Gymnasium; from 1922-01-14 the new **Stanford Pavilion** is established.
- Stanford Pavilion / Old Pavilion continued through the pre-Maples era.
- **Maples Pavilion** first game: 1969-01-03 vs BYU.
- 2004-05 renovation exception: home games before 2005-01-01 were at **Leavey Center**.
- 2020-21 Santa Cruz games at **Kaiser Permanente Arena** are neutral, not Stanford HOME.

HOME publication blockers: **0**.
There are **27** valid `RESEARCHED_UNRESOLVED_HOME_VENUE` rows, all with Stanford, CA known.

### Regular-season neutral debt

Every regular-season neutral row has city/state.
Exactly **169** regular-season neutral rows retain researched exact-building debt. Each is explicitly marked `RESEARCHED_PARTIAL`; there are **0 unaccounted neutral site gaps**.

### Postseason completeness

All 124 postseason games have venue + city + state.
NCAA Tournament: **39/39 site complete**.
Postseason venue gaps: **0**.

A Stage 3B evidence correction returned the three Dec. 27/28/30, 1948 "PCC Tournament" games to the regular season: it was a midseason tournament at the **Cow Palace**, not a postseason conference championship.

## Opponent identity

- Source identity families: **324**
- Canonical opponent identities: **302**
- Current-D1 identities: **226** covering **2,768 games**
- Historical/current NON_D1 identities: **76** covering **149 games**
- Unresolved opponent identities: **0**
- Known current-program key splits: **0**
- Ambiguous current-program matches: **0**

Important correction:
- `STAN-R-1180` (1966-67, literal source label `Oklahoma State (1)`, L 73-88) normalizes to **Oklahoma City**, not Oklahoma State. Stanford's own Records vs. Opponents places the exact game under Oklahoma City.

The complete 76-identity NON_D1 population received the required owner Stage 5 sanity scan and was approved with zero flagged identities.

## Conference chronology

- 1913-14 through 1917-18 — Independent
- 1918-19 through 1958-59 — Pacific Coast Conference
- 1959-60 through 1967-68 — Athletic Association of Western Universities
- 1968-69 through 1977-78 — Pacific-8
- 1978-79 through 2010-11 — Pacific-10
- 2011-12 through 2023-24 — Pac-12
- 2024-25 onward — ACC

## Accomplishment cross-check

Research-base accomplishment reference:
- conference regular-season championships: **11**
- conference tournament championships: **1**
- NCAA Tournament appearances: **17**
- Final Four appearances under the project metric: **2**
- national championships: **1**
- best finish: **NATIONAL_CHAMPION (1942)**

The assembled ledger independently reproduces **17 NCAA appearance seasons**, the **1942 national championship**, the **1998 Final Four**, and the **2004 conference-tournament championship**.

The 11 regular-season conference-title baseline is also supportable from Stanford's own historical material: Stanford's 1999 official game notes list the 1919-20, 1920-21, 1935-36, 1936-37, 1937-38, 1941-42, and 1962-63 titles; Stanford subsequently won league titles in 1998-99, 1999-2000, 2000-01, and 2003-04.

## H/A/N source-summary defects retained transparently

Two Stanford printed aggregate H/A/N summaries conflict with stronger row-level evidence:
- 1939-40 printed H10/A10/N3; controlling row-level partition H9/A11/N3.
- 1968-69 printed H10/A13/N2; controlling row-level partition H14/A9/N2.

Literal source evidence is preserved; only the curated H/A/N layer is corrected.

## Shared-reference authority

Research-time venue IDs are transport metadata only.
Existing research-base physical identities are reused where present.
Research-local venue identities (for example Encina Gymnasium and Leavey Center) remain provisional and must be reconciled during serialized Implementation.
No protected-main shared registry was mutated by this Research lane.

## Stage 6 adversarial self-challenge amendment

The adversarial pass challenged the historical exact-date debt against reciprocal/published evidence.
Ten previously blank dates were restored only where opponent, season, score, and H/A/N/site context produced a unique match:

- 1943-01-02 at Illinois
- 1958-12-23 at Illinois
- 1959-12-01 San Francisco
- 1959-12-03 San Jose State
- 1959-12-05 Saint Mary's
- 1959-12-21 at Wisconsin
- 1959-12-22 at Marquette
- 1959-12-28 West Virginia (Los Angeles event)
- 1959-12-29 Michigan (Los Angeles event)
- 1959-12-30 Illinois (Los Angeles event)

No game was added, removed, re-ordered, reclassified, or identity-remapped by this amendment.
The remaining 636 exact-date blanks remain explicit historical source debt rather than inferred dates.


## Stage 7 immutable freeze

- `RESEARCH_FROZEN: YES`
- Stage 5 owner NON_D1 disposition: **APPROVED — zero flagged identities**
- Stage 6 pre-freeze adversarial self-challenge: **PASS**
- Research acceptance errors: **0**
- Research acceptance warnings: **0**
- Protected `main` observed at freeze: `9738fe4f54b813aad4d2a12344a2c8279c3590ee`
- Recorded research base remains: `3989158d6e461a3dfb7be919586c5b388f8ef83d`
- `CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`

Stage 7 does not perform serialized Implementation or mutate protected-main shared references.

## Implementation current-main rebase overlay

The immutable RESEARCH_FROZEN ZIP remains unchanged. Serialized Implementation
applied only deterministic current-main shared-reference reconciliation to the
extracted integration copy:

- Imperial Arena retains the existing `imperial-arena` / `VEN-000088` physical
  identity; normalized project geography follows current main as Nassau, BS while
  literal/source evidence remains preserved.
- MGM Grand Garden Arena and T-Mobile Arena retain their existing global physical
  identities and use the project's established Las Vegas, NV canonical locality
  normalization.
- Stanford's provisional `san-francisco-civic-auditorium` identity is the already
  registered `civic-auditorium-san-francisco` / `VEN-000574` physical venue.
- Leavey Center is reused from current main; Encina Gymnasium remains a genuinely
  new physical identity for authoritative ID allocation by the staging tool.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=dba25e022e1f30cacff0e8f0f530fd54c23f3fe3` from `research_base_sha=3989158d6e461a3dfb7be919586c5b388f8ef83d`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
