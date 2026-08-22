# Georgia source notes

## Primary source

**2025-26 Georgia Men's Basketball Media Guide**, University of Georgia Athletics, owner-supplied PDF.

The year-by-year results ledger is the package backbone through 2024-25. Internal cross-check sections used include season-by-season records, all-time opponent series, SEC Tournament history, NCAA Tournament history, NIT history, overtime history, accomplishments, and facility/home-court history.

The original source strings are preserved in `raw_text`. Structured corrections do not rewrite the original claim.

## 2025-26 supplement

Georgia Athletics official completed 2025-26 schedule:
https://georgiadogs.com/sports/mens-basketball/schedule/2025-26

It supplies 33 competitive games and a 22-11 record, including site type and modern venue information. The Oct. 15 Georgia State and Oct. 26 Troy contests are explicitly labeled exhibitions and are excluded.

The NCAA Tournament loss to Saint Louis on 2026-03-19 is assigned to KeyBank Center, Buffalo, from Georgia's official contemporary NCAA game/box-score evidence and the established project physical venue registry.

## Historical schedule archive supplements

Georgia Athletics' official historical schedule archive was used only to resolve concrete gaps/defects while preserving media-guide `raw_text`.

Examples:
- 1911-12 Augusta YMCA -> 1912-01-03
- 1919-20 S.E. Christian College -> 1920-01-01
- 1925-26 Dahlonega -> 1926-01-03
- 1925-26 Westminster A.C. -> 1926-01-04

Official 1925-26 archive:
https://georgiadogs.com/sports/mens-basketball/schedule/text/1925-26

Official 1919-20 schedule:
https://georgiadogs.com/sports/mens-basketball/schedule/1919-20

## Owner exhibition ruling

On 2026-08-21 the owner explicitly ruled the 1987-12-20 **Japan All-Stars** game an exhibition and excluded it from the competitive ledger. The New Orleans and UAB games on the Japan trip remain competitive. This is binding project scope for Georgia.

## Conference tournament site reference

Owner-supplied file:
`Conference_Tournament_Site_Reference(5).xlsm`

The workbook is an in-progress universal reference and is **not** treated as universal canon. The owner explicitly authorized only the completed **SIAA, Southern Conference, and SEC** sections for Georgia. Those sections supply conference-tournament physical venue/site normalization, including the 2008 SEC Tournament tornado relocation split.

The package does not use or propagate unfinished workbook sections.

## Conference chronology

Georgia's project conference timeline is:
- SIAA through 1920-21
- Southern Conference beginning 1921-22 through 1931-32
- SEC beginning 1932-33

The 1920-21 media-guide wording `SC Tournament-Atlanta` is retained as raw provenance, but season membership controls the public tournament identity and the owner-authorized workbook identifies the event in the SIAA section.

## Venue sources

Georgia Athletics Stegeman Coliseum / previous home courts:
https://georgiadogs.com/sports/2023/8/23/facility-stegeman-coliseum-basketball

Georgia Athletics historical Stegeman copy establishes that the Georgia Coliseum was christened with the 81-68 win over Georgia Tech on 1964-02-22 and renamed Stegeman Coliseum on 1996-03-02. The package therefore treats Georgia Coliseum and Stegeman Coliseum as one physical venue identity (`VEN-000198`) while preserving the historical source name before the rename.

The same official facility history identifies Athens YMCA, Alumni Hall, The Octagon, Moss Auditorium, and Woodruff Hall as prior Georgia home courts. Overlapping Octagon/Moss usage is not converted into unsupported game-specific assignments.

## NCAA and NIT

Georgia's dedicated media-guide postseason tables are used to cross-check the chronological ledger.

Through the completed 2025-26 season the package contains:
- 21 NCAA Tournament games
- 31 NIT games

All NCAA rows have physical venue, city, and state populated. NCAA round names use the project's controlled vocabulary.

The media guide's NCAA headline counts are internally stale after newer additions; the package counts the actual on-court appearance seasons. Project accomplishment policy counts on-court appearances even if later vacated.

## Administrative action

The media guide's sanctions notation is kept separately from played results. Vacated games/wins retain their on-court scores and results.

The 2002-03 South Carolina series entry is used to resolve the March 9 road win as 60-55 in overtime and vacated; the conflicting chronological `65-60` string remains in `raw_text`.

## Identity normalization

Source labels remain in `source_opponent_label`; `opponents.csv` records the final identity selection.

Georgia's own all-time series was used to resolve early shorthand:
- `Birmingham` -> Birmingham Athletic Club
- `Columbus` -> Columbus YMCA
- `Nashville` -> Nashville Ramblers

Duke institutional history supports Trinity College -> Duke for the 1921-22 `Trinity` row. Other historical/defunct opponents remain distinct unless a supported lineage is established.

## Remaining source limitations

Two competitive games still lack an authoritative exact date:
- 1908-09 Auburn, W 48-37
- 1928-29 Florida, W 48-32

Seven early games have a known played W result but no authoritative score in the available Georgia material. Those scores remain blank.

Forty-eight rows retain `UNKNOWN` site type because the source evidence is insufficient to classify H/A/N confidently. Geography or venue chronology is not used to manufacture site type.
