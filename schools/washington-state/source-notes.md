# Washington State source notes

## Source hierarchy
1. Washington State Athletics men's basketball record book supplied by the owner.
2. Washington State Athletics official historical/current schedules, game notes, recaps, box scores, facility histories, and opponent-history pages.
3. NCAA/conference/event or reciprocal institutional evidence for bounded gaps and postseason sites.
4. Owner-supplied conference-tournament venue guide, used only within Washington State's authorized conference membership scope.
5. Secondary historical sources only where official evidence could not settle a bounded fact.

## Primary historical source
**Washington State Men’s Basketball Record Book** (`Wash st.pdf`), Washington State Athletics.

Owner-supplied file SHA-256:
`562e462088cadde0cf97d712593a98f1ccf6721e2dcb1dc0d02cfa89679f4fc9`

The year-by-year results form the row-level historical spine through 2024-25. All-time series, postseason tables, facility material, and official schedules are cross-check/enrichment layers rather than silent replacements.

The PDF's year-by-year pages use adjacent season columns. Mechanical text extraction can attach one column's footnote legend to another column's games. This was explicitly detected during Stage 3A and is why bulk footnote-to-venue assignment was rejected.

## Completed 2025-26 supplement
Official Washington State Athletics schedule/box-score material supplies the completed 2025-26 season:
- 32 competitive games
- 12-20 on court
- Oct. 25, 2025 New Mexico exhibition excluded
- Mar. 6, 2026 Portland WCC Championship game included as conference tournament

## Conference-tournament venue reference
Owner-supplied `Ct venues 9 14(2).csv`.

SHA-256:
`d1a02c3c8845375c191473e4f45fd4b54d85c6d97b261bbf67c4ad6b3c069690`

It was consumed only for Washington State's applicable Pac-10, Pac-12, and WCC tournament seasons. It supplies physical tournament venue/city/state and is never used to infer H/A/N.

## Row counts by source era
The package contains **3,351** competitive source assertions. Historical year-by-year material contributes **3,319** games through 2024-25; the official 2025-26 supplement contributes **32**.

Three exhibitions are excluded from the competitive package.

## Opponent sources and identity work
Stage 2 preserves literal record-book labels while resolving canonical opponent identity. Historical/local entities are retained distinctly unless evidence supports a current-program lineage. Clear aliases and institutional renames are normalized to the current project program identity without creating key splits.

The complete Stage 5-ready owner scan contains 111 distinct working NON_D1 identities. A separate informational list contains 59 self-corrected current-program labels.

## Venue sources
High-value Washington State institutional sources include:
- WSU Libraries building history for the 1901 gymnasium / later Temporary Union Building.
- WSU Athletics Bohler Gym history.
- WSU Athletics / Beasley Coliseum history and first-game material for Friel Court.
- Official season schedules and box scores for alternate/off-campus home games.
- Official event releases and reciprocal institutional records for recurring neutral events.

Home chronology is applied only after H/A/N is independently established.

## Postseason sources
Stage 3B combines the Washington State record book, official WSU schedules/notes, owner-authorized conference-tournament site reference, NCAA/event evidence, and reciprocal institutional sources.

Final postseason QA:
- 85 postseason games
- 36 conference tournament
- 17 NIT
- 14 NCAA
- 11 PCC playoffs
- 6 CBI
- 1 College Basketball Crown
- NCAA venue/city/state gaps: 0

## Conference sources
Washington State's record book yearly-results summaries establish the program's historical conference sequence. Project central conference authority supplies the approved stable identities/naming eras:
- Northwest historical identity
- Pacific Coast Conference
- AAWU
- Pacific-8
- Pacific-10
- Pac-12
- WCC
- Independent

The source's `PC North` terminology is divisional, not a separate conference.

## Accomplishment sources
Washington State official historical material documents:
- the 1917 Pacific Coast championship and retroactive Helms national championship;
- the 1941 Pacific Coast championship and NCAA national runner-up finish.

The final researched NCAA appearance seasons are 1941, 1980, 1983, 1994, 2007, 2008, and 2024.

The project accomplishment model counts NCAA championships separately from retrospective non-NCAA selectors, so the 1917 Helms honor remains documentary context rather than an NCAA championship count.

## Known source inconsistencies and repairs
Material accepted repairs include:
- missing 1965 Oregon State game and adjacent Oregon date correction;
- missing 2018 Oregon game;
- 2023-24 record-heading and Oregon State score defects;
- four 1952-53 result-marker defects;
- two administrative forfeits represented separately from on-court results;
- multiple winner-first score-display strings;
- one month-only 1914 date retained without invented day;
- provisional postseason footnote bleed repaired in Stage 3B.

All normalized corrections preserve `raw_text` and row-level research provenance.

## Foreign-site/shared-reference caveat
The physical 2019 Cayman Islands Classic site is John Gray Gym in George Town, Cayman Islands. Protected `main` at the research baseline contains the same venue identity (`VEN-000470`) with an erroneous Kentucky geography. Independent Research does not mutate shared global state, so the package records the correction proposal for serialized Implementation.

Because normalized foreign geography representation is a controlled repository concern, the three source rows retain the resolved venue but leave normalized `city`/`state` blank until that shared-reference correction is applied.

## Exhibition treatment
Exhibitions are outside the canonical competitive universe and are excluded from `source-games.csv`, records, opponent totals, and postseason/site counts.
