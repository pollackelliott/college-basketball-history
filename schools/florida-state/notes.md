# Florida State men's basketball — Stage 4 research working portfolio notes

## Status

This six-file research working package was assembled mechanically from the authoritative Florida State Stage 3B COMPLETE checkpoint.

- `research_base_sha`: `7834d87207761087dfdbc19d5259042564cd4fb0`
- Protected `main` SHA at Stage 4 assembly: `b2e013772f739cc044f0495d47237e34d5acdcc6`
- Program-perspective scope: `1956-57+`
- Competitive games: **2,079**
- On-court record: **1,224-855**
- Seasons: **1956-57 through 2025-26 (70 seasons)**
- Exhibitions are excluded.
- Stage 3B: **COMPLETE**
- Stage 4 package QA: **PASS**
- Stage 4 state: **COMPLETE — OWNER NON_D1 SANITY SCAN READY**
- Stage 5 owner NON_D1 sanity scan: **APPROVED — NO FLAGS** (27 identities / 110 games).
- Stage 6 adversarial self-challenge: **COMPLETE — PASS**.
- Stage 6 repaired six source-side score/administrative representations exposed by the blank-score/forfeit challenge; literal `raw_text` remains unchanged.

## Final game partition

- Regular season: **1,929**
- Conference tournament: **85**
- NCAA Tournament: **41**
- NIT: **24**

Accepted correction overlays `FSU-STG1-CORR-012` through `FSU-STG1-CORR-015` are applied only to curated fields. Literal source evidence remains preserved in `raw_text`.

## H/A/N and site completeness

Final all-game H/A/N:

- Florida State home: **988**
- Opponent home: **757**
- Neutral: **334**
- Unknown: **0**

Research/package site census:

- source-program HOME missing venue/location: **0 / 0**
- UNKNOWN H/A/N rows: **0**
- postseason exact venue/location gaps: **0 / 0**
- NCAA physical venue + city + state gaps: **0 / 41**
- modern regular-season neutral exact-venue gaps: **0**
- historical regular-season neutral exact-building enrichment debt: **109 rows**, all with complete city/state and explicit `RESEARCHED_PARTIAL` accounting
- regular-season OPPONENT_HOME exact-building rows outside source-school responsibility: **745**
- unaccounted material site-gap rows: **0**
- ambiguous physical venue identities: **0**

## Physical venue identity

Stage 4 mechanically reconciled accepted exact venue names against the immutable research-base venue registry.

- Distinct physical venue relationships in `venues.csv`: **75**
- Research-base venue reuses: **73**
- Research-time provisional identities: **2**
  - `tully-gymnasium` — Tully Gymnasium, Tallahassee, FL — 286 HOME uses
  - `mitchell-center` — Mitchell Center, Mobile, AL — one neutral use
- Both provisional venue identities are historically resolved and remain `PENDING_CURRENT_MAIN_REBASE`.
- Twenty-five exact venue-name rows whose research ledger had a blank `venue_key` were mechanically attached to already-existing research-base physical identities during Stage 4; no historical H/A/N or site conclusion was reopened.
- The 1985-12-31 Charlotte Coliseum row maps to the 1955 physical building (`VEN-000040`) because the separate 1988 Charlotte Coliseum had not yet opened.

## Home-facility chronology

- **Tully Gymnasium**, Tallahassee — 1956-57 through 1980-81
- **Donald L. Tucker Civic Center**, Tallahassee — 1981-82 onward

Venue chronology is enrichment only after independent H/A/N classification.

## Conference chronology

- Florida Intercollegiate Conference — 1956-57 (project scope begins in the final season of the institutional 1954-55 through 1956-57 membership)
- Independent — 1957-58 through 1975-76
- Metro (1975) — 1976-77 through 1990-91
- ACC — 1991-92 onward

`florida-intercollegiate-conference` is a newly research-settled shared conference identity:
`Historical identity: RESOLVED`; `Global registration: PENDING_CURRENT_MAIN_REBASE`.

## Accomplishment cross-check

Target institutional evidence supports the following eventual accomplishment values:

- Conference regular-season championships: **3** — 1977-78 Metro, 1988-89 Metro, 2019-20 ACC
- Conference tournament championships: **2** — 1990-91 Metro, 2011-12 ACC
- NCAA Tournament appearances: **18**
- Final Four appearances: **1**
- National championships: **0**
- Best NCAA finish: **National Runner-Up (1972)**

The research-base/current-main `program-accomplishments.csv` has no Florida State row yet. These source-derived values therefore remain research handoff facts for later controlled registration/verification rather than a Research-lane protected-main mutation.

## Carried conflicts and reciprocal observations

The package preserves rather than silently erases:

- **3** cross-source conflicts (1980 Kentucky NCAA date; 1984 NC State NIT date/H-A-N; 2004 Wichita State NIT date)
- **4** already-published reciprocal representation defects (Baylor 2010 site; Minnesota 1972 NCAA site; Iowa 1988 NCAA site; Kentucky 1993 NCAA site/H-A-N)

Florida State Research does not mutate those already-published reciprocal packages.

## Opponent identity

- Distinct canonical opponent identities: **271**
- Current-D1 opponent games: **1,969**
- `NON_D1` opponent games: **110**
- Distinct `NON_D1` identities: **27**
- Unresolved opponent identities: **0**

The complete 27-entry owner sanity-scan presentation is preserved in the Stage 4 checkpoint. The informational self-corrected/current-D1 alias census contains **98 canonical identities / 138 literal source-label mappings**; these are already-resolved normalizations, not owner decisions.

## Stage 5 owner disposition

The owner approved the complete 27-identity / 110-game `NON_D1` sanity scan with no flags. No opponent-identity repair was requested.

## Stage 6 adversarial self-challenge

`PRE-FREEZE SELF-CHALLENGE: PASS`

The self-challenge repaired one bounded source-representation class: six rows with blank/OCR-damaged scores and/or explicit forfeit provenance. Five blank score pairs were recovered, and three games now carry controlled `FORFEIT` administrative status. No game identity, date, H/A/N, venue, game type, postseason round, opponent identity, or literal raw evidence was changed.

Residual review results:

- researched-unresolved HOME venue rows: **0**
- UNKNOWN H/A/N rows: **0**
- unknown exact dates: **0**
- historical regular-season neutral building debt: **109**, all pre-1996, locality-complete and explicitly research-accounted
- modern neutral unresolved exact venues: **0**
- postseason unresolved exact venues: **0**
- physical venue rows: **75** = 73 research-base reuses + 2 provisional settled candidates; ambiguous identities: **0**
- current-program opponent key splits: **0**
- ambiguous current-program matches: **0**
- modern `NON_D1` identities specifically reviewed: **6**
- blank played-score pairs after repair: **0**
- unaccounted material site gaps: **0**

A systematic protected-main published-reciprocal neutral-site challenge did not expose a new exact-building recovery within the 109-row historical neutral residual. Under the repository's location-first historical standard, the surviving 109 rows return to terminal researched historical enrichment debt rather than a new row-by-row research cycle.

Stage 6 stops here. Immutable final Research Freeze packaging is the separately bounded Stage 7.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=3e888ecc2c4269b4a2e82e23a2123f0a6af9d740` from `research_base_sha=7834d87207761087dfdbc19d5259042564cd4fb0`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
