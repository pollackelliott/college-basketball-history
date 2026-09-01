# South Carolina men's basketball research portfolio

## Status

- Research status: **RESEARCH_FROZEN**
- School: South Carolina
- Program key: `south-carolina`
- Research base SHA: `11e99338493c5372b867f1343eeeddd33ccf8da8`
- Owner history scope: `ALWAYS_TOP_LEVEL_FROM_INCEPTION`
- History start season: `1908-1909`
- Owner confirmed this scope on 2026-08-31.
- **CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES**

## Competitive universe

- Competitive games through completed 2025-26: **2,895**
- On-court record: **1,530-1,364-1**
- South Carolina official record book through 2024-25: **2,863 games, 1,517-1,345-1**.
- Completed 2025-26 official schedule supplement: **32 competitive games, 13-19**.
- Oct. 26, 2025 vs. NC State is explicitly an exhibition and is excluded.
- Game types: **2,720 regular season / 124 conference tournament / 19 NCAA Tournament / 32 NIT**.
- Site types: **1,431 South Carolina home / 1,094 opponent home / 369 neutral / 1 unknown**.
- Opponent source-label rows: **360**; canonical opponent identities represented: **307**.
- Venue relationship/provenance rows: **84**.
- Unknown exact dates: **1**; unknown played scores: **2**, both confined to the documented 1918-19 source defects.

## History / conference chronology

Primary membership is intentionally modeled as:

- Independent: 1908-09 through 1921-22
- Southern Conference: 1922-23 through 1952-53
- ACC: 1953-54 through 1970-71
- Independent: 1971-72 through 1982-83
- Metro Conference: 1983-84 through 1990-91
- SEC: 1991-92 onward

South Carolina's 1921-22 and 1922-23 SIAA Tournament participation is preserved at the game/event level and is not promoted into a primary SIAA membership interval.

## Homecourt chronology

The official South Carolina homecourt/history material supports the following deliberate facility chronology after HOME status is independently established:

- First five collegiate HOME games, 1908-10-30 through 1911-02-14: Columbia, SC is established, but the school says these first five collegiate games were played outside and does not identify a physical court/building. These are the portfolio's five narrow `RESEARCHED_UNRESOLVED_HOME_VENUE` exceptions.
- Carolina Gymnasium, now Longstreet Theater: first documented varsity game there Jan. 7, 1912; used through the early portion of 1926-27.
- Carolina Fieldhouse: first documented game Feb. 17, 1927; used through March 2, 1968.
- Carolina Coliseum, with the playing floor later dubbed Frank McGuire Arena: first game Nov. 30, 1968; primary home through 2001-02.
- Colonial Life Arena, opened as Carolina Center and later known as Colonial Center: first South Carolina men's game Nov. 24, 2002; current home.

Facility chronology is used only after H/A/N is independently established; venue or geography never determines site type.

## 1918-19 surviving-source defects

The official season aggregate is **4-7**, but the current guide/Athletics game list exposes only ten identifiable games totaling **4-6**. One explicit source-aggregate placeholder loss is therefore retained with unknown opponent/date/score/site rather than inventing facts.

A March 12, 1918 contemporary *Gamecock* recap mentioning a Camp Jackson Quartermasters Corps loss was checked and rejected for this purpose because it summarizes the **1917-18** season, not 1918-19.

The Jan. 29, 1919 row is printed as `Cam3-45` in multiple generations of official South Carolina records. The current Athletics archive itself exposes the game as `NEEDS ADDED - Cam3-45`. The row is retained as a loss with unresolved opponent and score; HOME/Columbia and Carolina Gymnasium are established independently. The two unresolved opponent identities are represented explicitly in `opponents.csv` and are not forced into known programs.

## Postseason and site completeness

- NCAA Tournament: **19/19 games strict-complete for physical venue, city, and state**.
- Conference tournaments: **124/124 games complete for physical venue, city, and state**.
- NIT: **32/32 games complete for physical venue, city, and state**.
- The owner-supplied Conference Tournament Site Reference was audited for South Carolina's actual membership path and is sufficient for every South Carolina-relevant SIAA, Southern, ACC, Metro, and SEC tournament season.
- Remaining non-NCAA neutral physical-venue blanks: **118**, all in historical 1940s-1980s special-site rows where the source establishes neutral/special-site context and location but available evidence did not support a defensible building assignment.
- No neutral physical-venue gap remains from 1990-91 forward.

Every remaining material site gap is paired with research status and basis. Explicit unknowns are preferred to unsupported arena assignments.

## Research acceptance QA

The permanent `research-check` acceptance semantics from the recorded research-base SHA were reproduced locally because the project repository mount was unavailable in this research lane.

Final acceptance result: **PASS — zero errors, zero warnings**.

Final site-completeness accounting:

- Material site-gap rows: **124**
- Research-accounted material gaps: **124**
- Unaccounted material gaps: **0**
- HOME publication blockers: **0**
- `RESEARCHED_UNRESOLVED_HOME_VENUE` rows: **5**
- `RESEARCHED_UNRESOLVED` rows: **1**
- `RESEARCHED_PARTIAL` rows: **118**
- Neutral missing-venue rows by decade: **1940s 4 / 1950s 27 / 1960s 36 / 1970s 43 / 1980s 8**

Season-record QA also reconciled every parsed media-guide season aggregate used in the extraction. The final ledger remains **1,530-1,364-1** across **2,895** competitive games.

## Accomplishment research

Working accomplishment values for Implementation verification:

- Conference regular-season championships: **6** — Southern 1927, 1933, 1934, 1945; ACC 1970; SEC 1997.
- Conference tournament championships: **2** — 1933 Southern; 1971 ACC.
- NCAA Tournament appearances: **10** through 2024.
- NCAA Tournament on-court record: **8-11**.
- Final Fours: **1** — 2017.
- NCAA national championships: **0**.
- Best NCAA finish: **Final Four**; best-finish year: **2017**.
- NIT championships: **2005, 2006**; NIT runner-up: **2002**. These are contextual and are not additional program-card fields.
- SEC East divisional titles are not counted as additional full conference regular-season championships.

## Integration prerequisites

The research-base global conference registry does not contain the historical Metro Conference identity needed by South Carolina. The school portfolio therefore records provisional research identity `metro-1975`; the serialized Implementation lane must rebase against current main and reconcile/add the global conference identity before tracked Phase 0.

All research-time numeric `venue_id` values remain blank by design. Physical identities, stable names/aliases, geography, chronology, and game mappings are preserved in `venues.csv`; authoritative global venue-ID reuse/allocation belongs to the Implementation rebase.

No shared repository mutation, canonical ingestion, global discrepancy reconciliation, publication, or release action was performed by this research lane.

## Integration naming / identity rulings

- Immutable RESEARCH_FROZEN transport SHA-256:
  `9be0f34e8901b0e1d58b8b216d7a3afd2530caa44f3d45b28e7c3f948af7afeb`.
- Current-main venue keys/geography were normalized only where the physical
  identity was already established in the global registry.
- Owner ruling 2026-08-31: the historical 1975-era Metro Conference is the
  stable identity `metro-1975` and must display publicly as **Metro (1975)**,
  distinguishing it from the MAAC successor using the Metro name beginning
  in 2026-27.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=11e99338493c5372b867f1343eeeddd33ccf8da8` from `research_base_sha=11e99338493c5372b867f1343eeeddd33ccf8da8`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
