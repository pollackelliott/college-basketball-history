# Wisconsin source notes

## Primary institutional source

**Wisconsin Men's Basketball 2025-26 Record Book** (owner-supplied PDF: `2025-26_MBB_record_book.pdf`).

- SHA-256: `77e5649466db916a7f37c206ad7ded88fdf4879343fb5f7361133421e9738b2b`
- Historical game ledger: All-Time Results, printed pages 46-63
- Cross-check sections used: year/season records, 2024-25 team results, Big Ten Tournament history, NCAA Tournament summaries, NIT history, program-through-the-years/facility material
- Coverage: program inception through completed 2024-25 season

The All-Time Results section is the backbone of the historical ledger. Wisconsin states that home games are displayed in bold. The dedicated All-Time Series Scores tables provide game-level `H`, `A`, or footnoted location codes and are used as the primary H/A/N cross-check where a matching row exists. The package preserves the source wording in `raw_text` and records the small number of internally conflicting rows in `notes.md` rather than silently pretending the source is internally perfect.

## 2025-26 completed-season supplement

Wisconsin Athletics official 2025-26 schedule/results supplies the completed season because the record book predates it.

- Official schedule/results: https://uwbadgers.com/sports/mens-basketball/schedule/2025-26
- Text schedule used during research: https://uwbadgers.com/sports/mens-basketball/schedule/text/2025-26
- Official High Point NCAA box score/site confirmation: https://uwbadgers.com/sports/mens-basketball/stats/2025-26/high-point/boxscore/17187
- Competitive record: **24-11** across **35 games**
- Site split: 15-2 home, 6-4 away, 3-5 neutral
- Two preseason exhibitions are outside the competitive package universe.

## Conference-tournament site reference

Owner-supplied workbook: **`Conference_Tournament_Site_Reference(8).xlsm`**.

- SHA-256: `68fd42a5da4e2a908a9911c5812fda317920e1842b5518ebba52d20cdd2b26e2`
- Owner ruling: the workbook is globally incomplete, but its **Big Ten section is complete and reliable for Wisconsin**.
- Use in this package: Big Ten Tournament physical venue/city/state assignments from the event's 1998 inception through 2026.
- Explicit limitation: no unfinished conference section is promoted to universal project canon.

## NCAA Tournament site evidence

Wisconsin's dedicated **All-Time UW NCAA Tournament Summaries** provide game-by-game tournament city and physical venue evidence for all 68 NCAA games through 2025. The 2026 High Point game is supplemented from Wisconsin Athletics' official schedule/box score at Moda Center in Portland, Oregon.

Physical venue names are normalized to the research-baseline global venue registry while preserving source aliases, including examples such as Civic Arena -> Mellon Arena, RCA Dome -> Hoosier Dome, Carrier Dome -> JMA Wireless Dome, Qwest/CenturyLink Center -> CHI Health Center Omaha, Staples Center -> Crypto.com Arena, and Sprint Center -> T-Mobile Center. Physical venue identity never establishes H/A/N.

## NIT evidence

The record book's dedicated NIT section establishes Wisconsin's 11 NIT games (6-5): 1989, 1991, 1993, 1996, and 2023. Public NIT round remains blank because Wisconsin did not reach an NIT championship game in this source universe.

## Home-facility evidence

Wisconsin's program/facility history establishes the Red Gym -> Wisconsin Field House -> Kohl Center primary-home sequence. Game-level home evidence is established first; chronology is then used only to assign venue to those independently established home games.

## Opponent identity method

Every exact source label in `source-games.csv` is represented in `opponents.csv`. Current Division I identities use the current project naming/key convention where established. Historical/local/military/YMCA/club opponents remain distinct source-based identities unless institutional lineage is secure. Ranking markers, overtime markers, postseason footnote symbols, and neutral-site footnote suffixes are removed from canonical identity without rewriting `raw_text`.

Where `current_d1` is blank, the physical/source opponent identity is resolved but present-day D1 classification was not required to establish the historical game. The package does not invent lineage solely to fill a recommended metadata field.

## Research baseline and portability

`research_base_sha=b8b543544cc97d993056537e3b7fc8d09258fa8c`.

Venue IDs created during parallel research are provisional until the serialized integration lane performs the mandatory current-main shared-reference rebase. The package is **RESEARCH_FROZEN**, not `INTEGRATION_FROZEN`.
