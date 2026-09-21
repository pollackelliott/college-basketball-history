# Stanford Men's Basketball — Source Notes

## Controlling research state

Research base SHA: `3989158d6e461a3dfb7be919586c5b388f8ef83d`

The package is assembled from the accepted Stage 1 through Stage 6 durable research state and was sealed in Stage 7 as the immutable `RESEARCH_FROZEN` portfolio. The recorded research base SHA remains authoritative for Research provenance; serialized Implementation must perform the current-main rebase.

## Primary Stanford game-history sources

1. Stanford Athletics — Current Year-By-Year Results  
   https://gostanford.com/news/2020/03/23/year-by-year-results-8  
   Used for modern seasons, 2024-25/2025-26 completion, and current corrections.

2. Stanford Athletics — Historical Year-By-Year Results sibling  
   https://gostanford.com/news/2020/03/23/year-by-year-results-9  
   Used as the long historical web spine through the early program years.

3. Stanford Athletics — 2009-10 Men's Basketball Media Guide, history section  
   https://stanford_ftp.sidearmsports.com/custompages/old_site/pdf/m-baskbl/0910-mg-section7.pdf  
   Used for the inception-through-2008-09 year-by-year historical ledger and event footnotes.

4. Stanford Athletics — Yearly History  
   https://gostanford.com/news/2020/03/23/yearly-history-5  
   Used for season-count reconciliation and the official historical aggregate.

5. Stanford Athletics — Men's Basketball Archives  
   https://gostanford.com/news/2013/04/17/mens-basketball-archives  
   Used to locate season-specific schedules, recaps, box scores, and historical guides.

## Opponent identity sources

- Stanford Athletics — Records vs. Opponents  
  https://gostanford.com/news/2014/09/26/records-vs-opponents-4  
  High-value first-party reciprocal identity evidence, including the 1966-67 Oklahoma City correction.
- Institutional histories and reciprocal athletics records were used for historical aliases such as UC Davis/California Aggies, Oregon State/Oregon AC, San Francisco/St. Ignatius, San Jose State/San Jose Teachers, Utah State/Utah Aggie College, Seattle U, Alaska Anchorage, Missouri State, and other historical/non-D1 identities.
- Literal club, military, service, reserve, select, and historical lower-division opponents remain distinct unless evidence supports a real institutional merge.

## H/A/N and HOME-facility sources

- Stanford Athletics — Burnham Pavilion and Ford Center facility history  
  https://gostanford.com/facilities/burnham-pavilion-and-ford-center
- Stanford Athletics — Maples Pavilion records/history  
  https://gostanford.com/news/2020/03/23/maples-pavilion-records
- Stanford Athletics — Maples renovation material / Leavey Center displacement
  https://gostanford.com/news/2003/11/05/athletics-news-111
- Stanford Athletics — 2020-21 schedule and season review for Santa Cruz/Kaiser Permanente Arena.
- Stanford institutional Hall-of-Fame history for Harry Maloney and the pre-Encina outdoor era.
- Contemporary Dec. 1921 reporting for Stanford's large open-air pavilion and the 1920-21 mixed-facility conclusion.

H/A/N was never inferred solely from opponent geography. Stanford's published season H/A/N totals were used as mechanical checksums, with row-level evidence controlling where printed aggregates were internally inconsistent.

## Postseason sources

### Conference tournament/playoff

Owner-supplied `Ct venues 9 14(2).csv`
- SHA-256: `d1a02c3c8845375c191473e4f45fd4b54d85c6d97b261bbf67c4ad6b3c069690`
- Authorized use in this lane: Stanford's conference-tournament history only.
- Cross-checked with Stanford season/tournament schedules for round sequence.

### NCAA Tournament

Stanford Athletics — NCAA Tournament History  
https://gostanford.com/news/2020/03/23/ncaa-tournament-history-23-16-in-17-appearances-1

Dedicated Stanford box scores/recaps and NCAA/site evidence supplied exact physical arenas. NCAA rows are **39/39 complete for venue, city, and state**.

Important physical-identity notes:
- 2002 St. Louis NCAA games: Edward Jones Dome -> physical key `the-dome-at-america-s-center`
- 2003 Spokane NCAA games: Spokane Veterans Memorial Arena -> physical key `numerica-veterans-arena`

### NIT

Stanford Athletics — NIT History  
https://gostanford.com/news/2020/03/23/nit-history

All 27 NIT rows have resolved venue/city/state.

### CBI / other postseason

Stanford 2008-09 schedule/archive supplied the three CBI rounds.
Stanford's 2025-26 schedule/recaps supplied the 2026 College Basketball Crown appearance.
Historical 1936 Olympic Trials Regional classification uses Stanford historical guide evidence plus contemporary Seattle reporting.

## December 1948 PCC correction

Three Stanford rows labeled "PCC Tournament" (Dec. 27, 28, and 30, 1948) are regular-season neutral games, not postseason.
Contemporary Dec. 31, 1948 reporting identifies California-Stanford as the championship game of the December PCC basketball tournament, and the games were played at the Cow Palace.

Physical venue: Cow Palace, Daly City, CA.

## Conference-history sources

Stanford/Pac historical material states:
- Stanford joined the Pacific Coast Conference in 1918.
- The PCC dissolved in 1959.
- Stanford was an original AAWU member in 1959.
- The AAWU/Pac-8/Pac-10/Pac-12 naming eras are represented as distinct repository conference keys under current repository policy.
- Stanford accepted ACC membership beginning August 2024.

Stanford ACC announcement:
https://gostanford.com/news/2023/09/01/stanford-to-join-the-atlantic-coast-conference-in-august-2024

## Accomplishment sources

Stanford Athletics — Men's Basketball History  
https://gostanford.com/news/2020/03/23/mens-basketball-history-1

Stanford Athletics — February 1999 official men's basketball game notes  
https://gostanford.com/news/1999/02/27/stanford-universitys-official-athletic-site-mens-basketball-63

The older Stanford page explicitly lists seven pre-1999 conference championships, including the four PCC titles omitted from the shorter modern summary. Adding Stanford's later 1999, 2000, 2001, and 2004 league titles supports the 11-title repository baseline.

## Research accounting

- Literal source text is preserved in `raw_text` and `source_opponent_label`.
- Exact unknowns remain unknown rather than inferred.
- Research site metadata is populated only when an actual material site gap remains.
- Existing global venue identities are reused against the research base where available.
- Provisional research venue identifiers are not authoritative global IDs and must be current-main rebased during serialized Implementation.

## Stage 6 reciprocal/date self-challenge

The freeze self-challenge intersected Stanford's remaining exact-date blanks with reciprocal and schedule evidence.
Ten dates were promoted from unknown only after unique season/opponent/score/site matching.

High-authority corroboration includes:
- Illinois Athletics opponent history vs Stanford:
  https://fightingillini.com/sports/mens-basketball/opponent-history/stanford-university/36
  (1943-01-02, 1958-12-23, 1959-12-30)
- Illinois 1942-43 schedule:
  https://fightingillini.com/sports/mens-basketball/schedule/1942-43
- University of San Francisco yearly results:
  https://usfdons.com/sports/2014/8/7/MBB_0807145833.aspx
  (1959-12-01)
- Sports-Reference 1959-60 Stanford schedule:
  https://www.sports-reference.com/cbb/schools/stanford/men/1960-schedule.html
  (complete eight-game opening sequence, used as corroborating schedule evidence)

No reciprocal source was permitted to create a Stanford game; it could only enrich an already accepted Stage 1 row.
