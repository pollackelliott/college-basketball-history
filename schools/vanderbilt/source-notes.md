# Vanderbilt source notes

## 1. Source hierarchy

Primary historical evidence is Vanderbilt's official [2025-26 Men's Basketball Fact Book](https://storage.googleapis.com/vucommodores-prod/2026/03/2025-26-MBB-Fact-Book.pdf): season summaries on PDF pages 2-3, dedicated postseason results on page 22, season-by-season results on pages 26-46, and opponent-series H/A/N results on pages 48-61.

The completed 2025-26 season comes from Vanderbilt's official [Men's Basketball Press Box](https://vucommodores.com/mens-basketball-press-box). Owner rulings control the scope boundary, conference chronology, achievement totals, home-venue display chronology, and explicit project conventions.

The owner-attached official 2019-20 history/records and full fact-book PDFs are corroborating historical sources. The owner-supplied schedule tables since 2019-20 are used for discovery and QA, not to overrule official Vanderbilt game evidence.

## 2. Historical extraction and visual verification

The four-column season-by-season pages were extracted by PDF coordinates so each season remains in reading order. Representative early, middle, recent, and series pages were rendered and visually checked against the extracted text before normalization.

The chronological extraction yields 2,968 printed game rows through 2024-25. The two exact 1954-55 omissions documented in `notes.md` are supplied from the same fact book's official opponent-series pages, producing 2,970 historical rows.

`source_page` preserves the fact-book PDF page, and `raw_text` preserves the extracted source line. Early undated rows remain undated.

## 3. Series-table use

The official opponent-series section is not used as an independent row generator except for the two documented 1954-55 omissions. Its routine role is corroboration and H/A/N site evidence.

It supplies an unambiguous site match for 2,621 historical rows. Forty-three rows contain a conflict between the chronological ledger's explicit `at`/`vs.` marker and the series H/A/N table; the chronological game-level marker controls. This includes several obvious series-table location errors and tournament-location differences. No venue is inferred from the H/A/N letter.

## 4. Completed 2025-26 supplementation

The official press box supplies 36 completed competitive games and a 27-9 record through the NCAA second round. The 2025 Virginia preseason exhibition is excluded. Official dates control the owner-supplied table's identified typos:

- at Ole Miss: 2026-03-03.
- SEC quarterfinal vs. Tennessee: 2026-03-13.
- SEC semifinal vs. Florida: 2026-03-14.
- SEC championship vs. Arkansas: 2026-03-15.
- NCAA first round vs. McNeese: 2026-03-19.
- NCAA second round vs. Nebraska: 2026-03-21.

Exact 2025-26 venues supplied by the owner are retained and are consistent with the official home/away/neutral presentation and event sites.

## 5. Aggregate conflict

Vanderbilt's current and attached official fact books contain a persistent internal aggregate conflict. The season headers total 1,697-1,273 (2,970 games) through 2024-25, while the headline program-history total says 1,701-1,262 (2,963 games). The earlier 2019-20 guide shows the same seven-game total gap at that cutoff.

The package follows the auditable game ledger plus the two same-book series supplements. It records the headline discrepancy for later institutional review rather than dropping unidentified games.

## 6. Postseason corroboration

The dedicated official postseason table establishes Vanderbilt's NCAA and NIT game universe and round progression. It supports 27 NCAA games through 2024-25 and 37 NIT games. The official 2025-26 press box adds NCAA first- and second-round games, bringing the package to 29 NCAA games and 17 appearances through 2025-26.

The 1961 Kentucky game labeled `NCAA Tournament (Knoxville)` in a season legend is absent from the dedicated NCAA table and the official appearance count. It is therefore preserved as a source-wording exception without being treated as an NCAA bracket game.

## 7. Modern cross-source corrections approved by the owner

For Florida, Vanderbilt's current fact book and Florida's official [2020-21 schedule](https://floridagators.com/sports/mens-basketball/schedule/text/2020-21) establish 2020-12-30. Canonical reconciliation applies this correction to `CBBG-0020008`.

For Arkansas, Vanderbilt's current fact book, Vanderbilt's official [game recap](https://vucommodores.com/news/2021/01/23/dores-dropped-at-home), and Arkansas's official [postgame record](https://arkansasrazorbacks.com/vanderbilt-postgame-justin-smith-and-moses-moody/) establish Arkansas 92, Vanderbilt 71. An older Vanderbilt press-box line prints `L, 72-91`; that isolated typo is retained as conflict context but does not control the curated row. Canonical reconciliation applies this correction to `CBBG-0005665`.

The owner approved both corrections on 2026-08-14. The source package recorded these decisions before ingestion; post-ingestion reconciliation applies them to canonical games and discrepancies.

## 8. Home venue evidence

The official program history states that Memorial Gymnasium debuted on 1952-12-06 with Vanderbilt's 90-83 win over Virginia. The owner approved `Old Gym` as the display venue for independently source-classified home games before that date. `venues.csv` records the chronology and the non-overriding site rule.

## 9. Expected later reconciliation behavior

Vanderbilt overlaps all eight currently public programs and should confidently match many existing canonical games. Material field disagreements must be surfaced through the repository's human-readable discrepancy workflow in a later owner-authorized phase. This six-file commit does not run ingestion, create assertions, resolve discrepancies, update achievements, enable Vanderbilt publicly, or apply either approved canonical correction.

The repository's read-only matcher initially reported 657 confident identity matches, 4 rows requiring identity review, and 2,345 new-game candidates. Thirty-seven initially confident matches contain field differences (9 date, 14 score, and 14 overtime).

On 2026-08-14 the owner approved `MATCH_SOURCE_ASSERTION` links from `VANRAW-00213` to Kentucky `KYRAW-00194`, from `VANRAW-00263` to Kentucky `KYRAW-00228`, and from `VANRAW-00582` to Tennessee `TENRAW-00489`. The owner also confirmed that Vanderbilt-Tennessee on 2009-01-20 and Tennessee-Vanderbilt on 2009-02-14 are separate valid games. Further inspection showed that the January game already existed as `CBBG-0022174`, but Tennessee's `/- at Vanderbilt` source marker had been misnormalized as a fake `at-vanderbilt` opponent. The owner approved correcting Tennessee assertion `TENRAW-02350` and the canonical row to Vanderbilt and using `MATCH_SOURCE_ASSERTION` for `VANRAW-02428`. The corrected identity plan is therefore 661 existing matches, 2,345 new games, and zero review-required identities. The material field disagreements were resolved in the post-ingestion reconciliation phase.

The earlier read-only simulation of the now-withdrawn `FORCE_NEW` plan is superseded. After the approved Tennessee and canonical identity corrections, a fresh read-only simulation verified 661 existing matches, 2,345 new games, zero review-required identities, 271 matched games with 900 supported blank-field enrichments, 3,006 new source assertions, and 66 discrepancies.

## 10. Post-ingestion reconciliation — 2026-08-14

The owner approved all 66 Vanderbilt ingestion discrepancy resolutions. Cross-source
review used official opponent histories and contemporary game records from Kentucky,
Tennessee, Florida, Arkansas, Missouri, and Illinois. Twenty canonical fields were
corrected; 46 Vanderbilt curated fields were normalized to the retained canonical
value. Raw Vanderbilt fact-book text remains unchanged, and every original conflict
remains auditable in `data/reconciliation/discrepancies.csv` with `RESOLVED` status.

The owner ruled that Florida-Vanderbilt on 1959-02-21 was played at Vanderbilt.
The curated site is therefore Vanderbilt home, while the fact book's conflicting
series-table `A` marker remains preserved in `source_site_candidate`.

Principal online cross-source references:

- [Tennessee opponent history](https://utsports.com/sports/mbball/opponent-history/vanderbilt/80)
- [Florida opponent history](https://floridagators.com/sports/mens-basketball/opponent-history/vanderbilt-university/90)
- [Illinois opponent history](https://fightingillini.com/sports/mens-basketball/opponent-history/vanderbilt-university/77)
- [Arkansas 2021 postgame record](https://arkansasrazorbacks.com/vanderbilt-postgame-justin-smith-and-moses-moody/)
- [Missouri 2022-23 schedule](https://mutigers.com/sports/mens-basketball/schedule/season/2022-23)
- [Kentucky 2019 official recap](https://ukathletics.com/news/2019/01/29/mens-basketball-no-7-cats-slam-dores-in-nashville/)
- [Contemporary 1982 Illinois-Vanderbilt UPI report](https://www.upi.com/Archives/1982/12/13/Anthony-Welch-who-scored-28-points-sank-two-free/7492408603600/)

