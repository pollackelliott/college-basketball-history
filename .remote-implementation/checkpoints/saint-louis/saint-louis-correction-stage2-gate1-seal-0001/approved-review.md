# saint-louis onboarding review

Generated: 2026-11-01T14:21:20.423945+00:00
Input fingerprint: `ddd25bfb9bb19487bfb0c6b3f06cb6296563f1826fbb13be743cf6618c6b55c7`
Approved plan: `bfe16499cd111951c435f001f9f5199a8044a733695c2c2fe4d5b71a57203016`

## Preflight summary

- Source rows: 2,892
- In-scope rows: 2,892
- Pre-cutoff researched rows: 0
- Existing matches: 2,892
- New canonical games: 0
- Identity reviews: 0
- Safe enrichment fields: 0
- Discrepancies: 0
- Conditional discrepancies: 0
- Canonical-only site reviews: 1
- Affected existing public programs: alabama, arizona, arizona-state, arkansas, auburn, baylor, boise-state, boston-college, butler, byu, california, chicago-state, cincinnati, colorado, colorado-state, creighton, depaul, duke, florida-state, fresno-state, georgetown, georgia, georgia-tech, gonzaga, houston, illinois, indiana, iowa, iowa-state, kansas, kansas-state, kentucky, long-island-university, louisville, lsu, marquette, maryland, miami, michigan, michigan-state, minnesota, mississippi-state, missouri, nc-state, nebraska, north-carolina, northwestern, notre-dame, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, pittsburgh, providence, purdue, rutgers, seton-hall, smu, south-carolina, st-john-s, stanford, syracuse, tcu, tennessee, texas-a-m, texas-state, texas-tech, ucla, uconn, usc, utah, utah-state, vanderbilt, villanova, virginia, virginia-tech, wake-forest, washington, washington-state, west-virginia, wisconsin, xavier

## Blockers

- None.

## Warnings

- None.

## Owner decisions

### 1. CORRECTION-IDENTITY-SAINT-LOUIS-1916-17-005-CBBG-0182742

- Category: correction_identity_patch
- Matchup: saint-louis vs loyola-academy
- Date: 1917-01-17
- Field: normalized_opponent_key
- Source value: `loyola-academy`
- Canonical value: `loyola-chicago`
- Evidence: Immutable published saint-louis-1916-17-005: loyola-chicago; corrected frozen source: loyola-academy; one assertion ASRT-SAINT-LOUIS-saint-louis-1916-17-005; canonical CBBG-0182742; no corrected-pair collision. Literal source evidence is retained.
- Recommended: `APPLY_CORRECTION_IDENTITY_PATCH`
- Decision: `APPLY_CORRECTION_IDENTITY_PATCH`
- Basis: Explicit owner ruling and Control Center authorization: on 1917-01-17 Saint Louis played Loyola Academy, not Loyola University Chicago. Fresh-verified Loyola reconciliation diagnostic loyola-chicago-stage2-reconciliation-diagnostic-0001, trace SHA-256 14b13a717bc389a999eca31ea382657f408b59116f04070663cc6ea5623e8131. Preserve literal Saint Louis source_opponent_label/raw_text and retarget only the normalized opponent identity through the repository-owned SINGLE_GAME_IDENTITY transaction.
