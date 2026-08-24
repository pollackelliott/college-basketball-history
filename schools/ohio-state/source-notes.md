# Ohio State source notes

## Primary historical source
**2025-26 Ohio State Men's Basketball Record Book**, Ohio State Athletics.

High-value sections:
- Big Ten Tournament Records, printed pp. 73-76
- Value City Arena records, printed pp. 77-78
- Ohio State and the NCAA Tournament, printed pp. 79-83
- St. John Arena, printed p. 131
- Results by Year, printed pp. 132-147

The year-by-year ledger is the row source through 2024-25. Dedicated postseason/facility sections are cross-check and enrichment layers, not silent replacements.

## Completed 2025-26
Official source: `https://ohiostatebuckeyes.com/sports/mens-basketball/schedule/text/2025-26`

The page reports 21-13 overall, 14-3 home, 5-6 away, 2-4 neutral. The Oct. 26 Ohio exhibition is excluded; all 34 competitive games through the NCAA Tournament are included.

## 1992-93 supplement
Ohio State's official historical 1992-93 schedule supplies the Dec. 1, 1992 Ohio game omitted by the current record-book chronological ledger.

## NCAA administrative action
The record book states 113 games (82-31) were vacated over 1998-99 through 2001-02 and visually marks affected rows in italics. Font-level PDF inspection confirms the individual allocation.

## Big Ten tournament site reference
Owner-supplied `Conference_Tournament_Site_Reference(5).xlsm`, authorized **Big Ten section only** for Ohio State. The workbook supplies physical shared venue/city/state and explicitly prohibits using those fields to infer H/A/N.

## Facility research
Ohio State University Archives: `https://library.osu.edu/site/archives/`

The Archives documents the Armory (1898-1919), move to the Coliseum in 1919, St. John Arena in 1956, and the move to the Schottenstein Center in 1998. Ohio State Athletics provides exact St. John/Value City chronology and later St. John return-game evidence.

## Cow Palace
Official facility history/location: `https://www.cowpalace.com/cow-palace-arena-event-center/about/history/`

Ohio State's NCAA table labels the 1960 Final Four location San Francisco; the physical Cow Palace is in Daly City, California. The package retains the source context while normalizing the physical venue geography.

## Postseason hierarchy
- Big Ten Tournament classification: Ohio State dedicated Big Ten table.
- Big Ten shared venue/location: owner-authorized Big Ten workbook.
- NCAA classification/site: Ohio State dedicated NCAA table plus established physical venue identities.
- NIT classification/site: explicit year-by-year NIT footnotes.
- Preseason NIT: `REGULAR_SEASON`.

## Opponent identities
Clear modern/historical institutional aliases are normalized to stable program lineages. Historical clubs, YMCAs, high schools, military teams and one-off entities are retained as distinct historical identities rather than speculatively merged. Original source labels remain preserved.

## Source caveats
The record book has several internal/transcription inconsistencies, including the 1992-93 omitted row, a 2022-23 heading that says 16-9 despite a 16-19 listed schedule, an NCAA-appearance count inconsistency, and a handful of score strings that conflict with listed W/L or were damaged by text extraction. Corrections are made only where authoritative evidence supports a specific value.

## Integration normalization after executable preflight
The first current-main preflight exposed unresolved historical NCAA-round semantics. The repair uses Ohio State's own dedicated NCAA table, the year-by-year postseason footnotes, and the project's established historical-round convention. The 1944-46 ledgers explicitly distinguish NCAA Eastern Regionals from Final Four games; historical consolation/third-place rows remain blank. Later rounds respect bracket structure and byes, including `Play-in` for opening games in the 1979-84 expanded fields and `R64` for 1985-and-later first rounds.

The same dedicated NCAA table identifies the **1950-03-23** opponent as **C.C.N.Y.**, 56-55 over Ohio State. The year-by-year ledger prints `New York Univ.` for that line. The dedicated NCAA table controls the normalized opponent identity (`ccny` / `CCNY`), while the contradictory chronological wording remains preserved in `raw_text`.

## Accomplishment provenance and administrative distinction
The project's accomplishment layer uses on-court history. Ohio State's current quick facts report administratively reduced totals after the NCAA action affecting 1998-99 through 2001-02. Contemporary Ohio State Athletics material documents the on-court facts removed from those modern administrative totals: the 2000 and 2002 Big Ten regular-season titles, the 2002 Big Ten Tournament championship, four consecutive NCAA appearances from 1999 through 2002, and the 1999 Final Four. Adding those back to the current administrative totals yields the project reference values **22 / 5 / 36 / 11 / 1**, with 1960 as the national-championship best finish.

Official Ohio State corroboration:
- `https://ohiostatebuckeyes.com/news/2000/3/4/buckeyes-secure-road-victory-share-of-big-ten-championship-2`
- `https://ohiostatebuckeyes.com/buckeyes-win-big-ten-tournament-championship`
- `https://ohiostatebuckeyes.com/news/2002/8/2/the-2002-03-mens-basketball-prospectus-2`
