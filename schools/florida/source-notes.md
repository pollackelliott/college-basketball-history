# Florida source notes

## 1. Source hierarchy

Primary historical evidence is Florida's **2025-26 Men's Basketball Media Guide**, especially the chronological all-time results through 2024-25, individual opponent series tables, SEC/NCAA tournament histories, and Home Court Records section. The completed 2025-26 season is supplied directly by the owner as a 35-game results table. Owner rulings in the project clarification gate control explicitly identified source conflicts.

## 2. Primary historical source and pages

The chronological extraction comes from PDF pages 100-114 of the supplied Florida media guide. It yielded exactly **2,752 game rows through 2024-25**. Source locators are retained per row as `PDF p. N`, and the printed chronological line is retained in `raw_text`.

## 3. Modern-season supplementation

The media guide predates completed 2025-26 results. The owner supplied the completed 2025-26 season separately: **35 games, 27-8**, appended as `source_era = user_supplied_2025_26_results`.

## 4. Row counts by source era and total

- `historical_media_guide`: 2,752 rows
- `user_supplied_2025_26_results`: 35 rows
- **Total: 2,787 rows**

## 5. Conference source

Conference membership chronology is owner-supplied and accepted as authoritative for this package: Independent through 1921-22, Southern Conference 1922-23 through 1931-32, SEC from 1932-33 onward. Florida's guide tournament labeling is internally consistent with the Southern-to-SEC transition.

## 6. Venue sources

Florida's media guide Home Court Records section establishes exact first/last game boundaries for the four primary home venues. The owner chose site-facing names University Gymnasium, New Gymnasium, Florida Gymnasium, and O'Connell Center. Exact 2025-26 venues/cities come from the owner-supplied completed-season table.

## 7. Postseason sources and aggregate QA totals

Historical postseason classification is driven by the all-time results' event headers and Florida's dedicated tournament sections. NCAA Tournament progression supplies the project's canonical NCAA round taxonomy. Conference-tournament public round remains blank except title games. Owner specifically ruled the March 2, 1931 Kentucky loss a semifinal, so it is not labeled Championship.

## 8. Cross-source evidence

Individual opponent series tables are used as internal corroboration when the chronological row contains an obvious contradiction. The guide explicitly groups certain historical identities/lineages, including Trinity with Duke, Georgia State Teachers with Georgia Southern, and Biscayne/St. Thomas together. The 1927 same-day Auburn and Paris Island Marines games are corroborated by the series evidence and remain separate games. Historical rows printed simply as `Southern` match the detailed Florida Southern series and are therefore resolved to Florida Southern; only the 2006-07 and 2013-14 `Southern` rows resolve to Southern University.

## 9. Known source inconsistencies

Approved chronological score corrections: 1950-02-11 Georgia L 52-77; 1985-01-30 Mississippi State W 72-57; 1995-02-01 Mississippi State L 47-70. Approved SEC Tournament-summary resolution rule: chronological game list + individual series agreement controls when the tournament summary conflicts. Explicit owner confirmations include 2007 tournament dates March 9/10/11, 2009 Auburn L 58-61 on March 13, and 2023 Mississippi State L 68-69 OT on March 9. The impossible chronological `F29` for Tennessee in 1941 is normalized to March 1 from the dedicated tournament section.

The opponent-series QA pass identified additional *summary-table* errors without changing any game rows: Bradley is printed 1-0 even though the chronological list and regular-season tournament history both contain a 1970-12-29 loss to Bradley (so Florida is 1-1); Florida Southern is printed 27-6 but omits the explicit 1958-12-20 Florida win, which is required by the 1958-59 8-15 season record (on-court series 28-6); Mississippi is printed 70-49 in the top-level table while its detailed series heading is 71-49; and Oral Roberts is printed 1-0 in the top-level table while its detailed series and the 2021 NCAA row show Florida 0-1. The project also consolidates the guide's separate `Milwaukee` and `Wisconsin-Milwaukee` rows into the current Milwaukee program. NCAA-vacated games are retained on court even where Florida's published series aggregates exclude them.

## 10. Exhibition treatment

No exhibition game is intentionally included. If a later source demonstrates that any listed historical contest was exhibition-only rather than a recognized varsity game, it should be handled through normal discrepancy/curation workflow rather than silently deleted.

## Extraction reproducibility

The local extraction parser matched 2,752 chronological rows using the guide's fixed-column all-time-results text. It preserves source H/A/N, printed result, score, overtime marker, page locator, and raw row. Exact dates are created only from printed month/day tokens, except for the owner-approved 1941 correction; 23 genuinely undated rows remain blank.
