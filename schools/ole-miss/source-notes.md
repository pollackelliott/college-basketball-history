# Ole Miss source notes

## Primary source

**2025-26 Ole Miss Men's Basketball Media Guide**, University of Mississippi Athletics Communications.

Primary historical sections used:

- historical timeline: pp. 63-70
- year-by-year records: p. 88
- all-time opponent game-by-game: pp. 120-131
- Tad Smith Coliseum records: p. 132
- Pavilion records: p. 133
- all-time scores: pp. 134-144
- SEC Tournament: p. 46
- National Tournaments: p. 47

The chronological all-time-score ledger is the primary game-by-game extraction source through 2024-25. Dedicated tournament and game-level sections control when they clearly demonstrate an internal chronological transcription issue.

## Completed 2025-26 season

The owner supplied the complete completed-season schedule/results table. It contributes **35 competitive games and a 15-20 record**. The Saint Mary's preseason exhibition is excluded. Ole Miss' official 2025-26 schedule is used as corroboration.

## Extraction reproducibility

The historical fixed-column extraction produced **2,821 competitive rows across 115 seasons with games**. The two undated 1923-24 College Hill rows are intentionally preserved without invented dates.

Historical extraction QA identified one aggregate conflict: 1913-14 is printed 8-7 in the season summary but 9-6 in the detailed 15-game ledger.

## Opponent normalization

The package contains **615 distinct source opponent labels**. Every label resolves through `opponents.csv`; no opponent identity remains unresolved.

Historical lineage resolutions include Arkansas A&M -> Arkansas-Monticello, Howard -> Samford, Indiana St.-Evansville -> Southern Indiana, Southwestern PU -> Rhodes, West Tenn. St. Teachers College -> Memphis, and the historical University of Memphis medical-school identity -> Memphis Physicians.

## Venue sources

Ole Miss Athletics facility history establishes the indoor-gym chronology and Tad Smith history. The media guide establishes SJB Pavilion's Jan. 7, 2016 opening for men's basketball.

The owner-supplied conference-tournament site reference controls SEC Tournament city/state and shared venue chronology. NCAA venue assignments use established NCAA site evidence/global physical venue identities. Modern 2025-26 venues come from the completed-season schedule evidence.

## Postseason source hierarchy

1. dedicated Ole Miss NCAA/NIT table
2. dedicated Ole Miss SEC Tournament table
3. historical Ole Miss timeline and detailed chronological ledger
4. owner-supplied conference-tournament site reference
5. existing project NCAA physical-site evidence

The extraction-time `source_event_class` field is not used as postseason authority because an extraction-state leak incorrectly propagated NCAA classification across entire NCAA-appearance seasons. Final package taxonomy is reconstructed from the dedicated authoritative tables.

## 2014-15 score orientation

Three all-time-score lines display a losing result next to a score written in winner-first order. Official Ole Miss season/postseason evidence controls the normalized score fields while the printed media-guide row remains intact in `raw_text`.

## 2025 NCAA site note

The media guide's national-tournament summary repeats Milwaukee on the 2025 Michigan State Sweet Sixteen line. The project's established NCAA physical-site evidence places that game at State Farm Arena in Atlanta. The source wording is documented rather than silently discarded.

## Exhibition treatment

No exhibition is included in the 2,856-game package. The explicit 2025 Saint Mary's exhibition is excluded.
