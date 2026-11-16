# houston onboarding review

Generated: 2026-11-16T19:21:44.451217+00:00
Input fingerprint: `d97abe48f005d493f06bbda196a21a7b10bc9d4116b077b9a918601bffe4273b`
Approved plan: `14589bf760be7155b205d28cb07733d9faacf75becb0ffe3a330d16564a65f90`

## Preflight summary

- Source rows: 2,394
- Publication-eligible rows: 2,394
- Top-level rows: 2,291
- Publication-excluded researched rows: 0
- Existing matches: 2,295
- New canonical games: 99
- Identity reviews: 0
- Safe enrichment fields: 7
- Discrepancies: 4
- Conditional discrepancies: 0
- Canonical-only site reviews: 1
- Affected existing public programs: alabama, arizona, arizona-state, arkansas, auburn, baylor, boise-state, boston-college, butler, byu, california, chicago-state, cincinnati, colorado, colorado-state, creighton, dayton, depaul, duke, florida, florida-state, fordham, fresno-state, george-mason, george-washington, georgetown, georgia-tech, gonzaga, hawai-i, illinois, indiana, iowa, iowa-state, kansas, kansas-state, kentucky, la-salle, long-island-university, louisville, loyola-chicago, lsu, marquette, maryland, miami, michigan, michigan-state, minnesota, mississippi-state, missouri, nc-state, nebraska, north-carolina, notre-dame, ohio-state, oklahoma, oklahoma-state, ole-miss, oregon, oregon-state, penn-state, pittsburgh, providence, purdue, rhode-island, rutgers, saint-joseph-s, saint-louis, san-diego-state, seton-hall, smu, south-carolina, st-bonaventure, st-john-s, stanford, syracuse, tcu, tennessee, texas, texas-a-m, texas-state, texas-tech, uc-davis, ucf, ucla, uconn, usc, utah, utah-state, vanderbilt, vcu, villanova, virginia, virginia-tech, wake-forest, washington, washington-state, west-virginia, wisconsin, xavier

## Blockers

- None.

## Warnings

- None.

## Non-substantive site-gap provenance

- None.

## Owner decisions

### 1. DISCREPANCY-HOU-EXP-00022-SCORE

- Category: discrepancy
- Matchup: houston vs texas-a-m
- Dates: source 1946-12-28; canonical [unknown]
- Field: score
- Source value: `62-41`
- Canonical value: `60-41`
- Evidence: texas-a-m [unknown]: 60-41
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical Houston 60-41. Texas A&M's official series history says the 1946-47 series opener was a 60-41 Aggie loss, while Houston's official historical guides say 62-41 on Dec. 28, 1946. Under All-History expansion authority, preserve Houston's frozen 62-41 assertion as conflicting evidence without rewriting the accepted reciprocal canonical score.

### 2. DISCREPANCY-HOU-EXP-00086-SCORE

- Category: discrepancy
- Matchup: houston vs marquette
- Date: 1949-12-10
- Field: score
- Source value: `65-69`
- Canonical value: `64-69`
- Evidence: marquette 1949-12-10: 64-69
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical Houston 64-69. Marquette's official year-by-year history records a 69-64 win over Houston on Dec. 10, 1949, while Houston's official guide records a 65-69 loss. Preserve the frozen Houston assertion as conflicting evidence without overwriting the established reciprocal canonical score.

### 3. DISCREPANCY-HOU-EXP-00087-GAME_DATE

- Category: discrepancy
- Matchup: creighton vs houston
- Dates: source 1949-12-13; canonical 1949-12-14
- Field: game_date
- Source value: `1949-12-13`
- Canonical value: `1949-12-14`
- Evidence: creighton 1949-12-14: 1949-12-14
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical 1949-12-14. Creighton's current official 1949-50 schedule, current all-time scores, and official 2006 Houston-series history all place the 52-47 game on Dec. 14, 1949; Houston's frozen guide row says Dec. 13. The convergent reciprocal institutional record supports the canonical date while the Houston date remains preserved as source evidence.

### 4. DISCREPANCY-HOU-EXP-00087-OVERTIME_PERIODS

- Category: discrepancy
- Matchup: creighton vs houston
- Dates: source 1949-12-13; canonical 1949-12-14
- Field: overtime_periods
- Source value: `0`
- Canonical value: `1`
- Evidence: creighton 1949-12-14: 1
- Recommended: `KEEP_CANONICAL`
- Decision: `KEEP_CANONICAL`
- Basis: Keep canonical 1 OT. Creighton's current official schedule marks the Dec. 14, 1949 Houston game as overtime, and Creighton's official 2006 series history describes the first Houston meeting as an overtime win. Houston's frozen row omits overtime; preserve that conflicting assertion without changing the established canonical overtime value.

### 5. CANONICAL-SITE-PATCH-CBBG-0124516

- Category: canonical_site_patch
- Matchup: houston vs ucf
- Dates: source [unknown]; canonical 2015-01-06
- Field: site_metadata
- Source value: `[no target source row]`
- Canonical value: `{"site_city":"","site_state":"","site_type":"TEAM_A_HOME","venue_id":"","venue_key":""}`
- Evidence: Canonical target-HOME game is preserved only by reciprocal assertion(s) from ucf; documented target HOME chronology yields 0 candidate physical venue(s): no uniquely covering HOME venue relationship. An explicit owner-reviewed site patch is required rather than a chronology guess.
- Recommended: `REVIEW_REQUIRED`
- Decision: `APPLY_CANONICAL_PATCH`
- Basis: Apply the exact Hofheinz Pavilion site metadata to canonical game CBBG-0124516. Houston's official Jan. 6, 2015 game recap says UCF won 79-78 inside Hofheinz Pavilion; UCF's official recap likewise places the game at Hofheinz Pavilion; Houston's official 2014-15 schedule lists the UCF game at Hofheinz Pavilion. Current registry identity is VEN-000291 / hofheinz-pavilion in Houston, TX, the same physical venue now displayed as Fertitta Center. Preserve the existing Houston-home H/A/N classification and patch only physical venue/locality.
