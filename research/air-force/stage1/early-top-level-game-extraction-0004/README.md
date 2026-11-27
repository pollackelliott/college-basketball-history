# Air Force Stage 1 — four-season systematic guide extraction checkpoint 0004

STATUS: **STAGE1_IN_PROGRESS**, NOT Stage 1 COMPLETE, NOT Stage 2, NOT RESEARCH_FROZEN, NOT Implementation.

Research authority: immutable research_base_sha and authenticated protected main `3f5a15458aa468347e56e669327d6fe4c9c6ee69`; directly authenticated parent Research checkpoint HEAD `b12b880fa89b25e70f13058013861c29eb715e27`. No scope/research-base mutation.

Accepted owner-final `Air Force,1957-58+` top-level classification is distinct from institutional inception **1956-57**; 1956-57 is NON_D1 and remains included. Official guide historic results and required complete-institution cutoff both **2025-26**.

## Bounded extraction

Air Force official 2026-27 history PDF pages **59–60** (sha256: `5fdf61cc80c698bae8ce61cc0ae1009d01139682c8148014934e304b407b73fd`) provide individual dated opponent and on-court score rows for four seasons. Their season headings and the four official Air Force online season schedules independently agree with extracted W/L and H/A/N partitions:

- **1965-66**: 14-12, 26 games. H 10-2; A 3-5; N 1-5. Guide p59 right column; online 1965-66 schedule.
- **1966-67**: 6-18, 24 games. H 4-7; A 2-9; N 0-2. Guide p60 left upper column; online 1966-67 schedule.
- **1967-68**: 10-14, 24 games. H 7-2; A 2-12; N 1-0. Guide p60 left lower column; online 1967-68 schedule.
- **1968-69**: 11-13, 24 games. H 7-5; A 3-6; N 1-2. Guide p60 center upper column; online 1968-69 schedule.

`stage1-ledger.csv` now contains **302 unique identified competitive game records** across **13 seasons**, 1956-57 through 1968-69. Its first **204 game rows and header are byte-for-byte carried forward from checkpoint 0003**. This tranche adds exactly **98** new rows with stable ID, date, literal guide opponent/row, source game scores and result, game_type, official-schedule-backed H/A/N, supported source-city/site fact, guide page and source URLs, and provenance.

All 98 are **REGULAR_SEASON**. The guide and Air Force schedules identify in-season holiday events, not NCAA or other postseason: 1965-66 Mile High Classic (Denver), Kentucky Invitational (Lexington), Far West Classic (Portland); 1966-67 Triangle Classic (Raleigh); 1967-68 Steel Bowl (Pittsburgh); 1968-69 East Carolina Classic (Greenville). Do not infer exact neutral building from tournament city.

Guide p60 labels the **1968-11-30 Colorado 78-83 loss** as `COLORADO*`, with `* First game at Cadet Field House`. This positive institutional **individual-game facility observation** is preserved in the first game's explicit venue/evidence note. Stage 3A will establish full facility chronology and exceptions; a single first-game footnote does not by itself certify every later home game at that facility.

## Explicit nonblocking evidence

- **1968-69 New Mexico State**: guide row `(16) NEW MEXICO ST.` 1969-03-01 L63-74; online schedule text says `#16 New Mexico State`, but links to University of New Mexico `golobos.com` and target site's opponent-history for New Mexico includes this game. Treat that outbound link/history routing as a contradictory identity signal, **not** a supported equivalence. Retain source name and queue for Stage 2 identity work. See residual AF-0004-001.
- **1967-68 Denver**: 1968-02-14 and 1968-02-23 are **two separate documented games** despite both listing W94-89, same opponent, same score. The guide and separate-date online schedule both list each, and both are needed to reconcile the 10-14 record. Preserve the two IDs and the explicit nonduplicate reconciliation. See AF-0004-002.
- Prior eight explicit residuals remain unmodified, including the accepted 1958-59 Arizona game, resolved printed invalid date, 1959-60 New Mexico site disagreement, and source-internal all-time totals discrepancy. Current total: **10 residual/reconciliation notes**, none blocking this newly extracted game population.
- No duplicate or exhibition is introduced; source-candidate competitive exclusions in this tranche: **zero**. Opponent entity normalization and off-site venue completion belong to governed later stages, not repeated Stage 1 rediscovery.

The 70-season inception-through-2025-26 guide census now has **13 row-identified seasons** and **57 remaining aggregate-only seasons, 1969-70..2025-26**. Their combined season-record aggregate implies **1,626 prospective rows** still to extract (1724 previous minus 98). This is NOT 1,626 historically unknown opponents/games and is NOT source-acknowledged unidentified-game debt. Sum of primary guide 70 season records vs printed all-time total remains an inherited unresolved +2 win discrepancy; do not invent two games.

Research-only `research/air-force` branch. Protected main, published games, canonical data, shared references, other Research checkpoint artifacts and serialized Implementation were not changed.

## Next bounded unit

Systematic primary-guide extraction **1969-70 through 1972-73** (four seasons, PDF p60-61), aggregate reconciliation, official-schedule H/A/N confirmation, preserve literal and nonblocking contradictions, one successor research-only checkpoint. Do not advance to Stage 2 automatically.
