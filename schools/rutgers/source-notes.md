# Rutgers source notes

## Primary school source

**Rutgers Men's Basketball 2025-26 media guide / record book** (owner-supplied PDF).

Used for the historical All-Time Scoreboard through 2024-25, the all-time series table, season W/L summaries, postseason history, opponent chronology, and facility/history context. The all-time series table is used as an independent internal cross-check for exact date and H/A/N evidence when a one-to-one game match is secure.

Known limitations preserved rather than hidden:

- Early chronological listings often omit exact dates.
- Some scoreboard score strings are printed winner-first rather than consistently Rutgers-first; the W/L marker controls score orientation in structured fields.
- The 1975 Louisville NCAA score is printed incorrectly in the guide relative to official NCAA evidence.
- Official Rutgers schedule checks identify and exclude the 2022 Fairfield and 2024 St. John's exhibitions even though those rows appear in the media-guide chronological ledger.
- Rutgers' official 2020-21 schedule corrects three media-guide scoreboard defects: Minnesota 76-72, at Iowa L 66-79, and Big Ten Tournament Indiana 61-50.
- The 1986 West Virginia Atlantic 10 tournament date conflicts with official conference/opponent tournament history.
- Aggregate season tables and game ledgers do not always use identical regular-season/postseason splits; the game-by-game competitive ledger controls package rows, with official schedule checks used for material tensions.

## Completed 2025-26 supplement

**Rutgers Athletics official 2025-26 men's basketball schedule/results**
https://scarletknights.com/sports/mens-basketball/schedule/2025-26

Used to add the completed 2025-26 season (34 games, 14-20), including official H/A/N designations, dates, scores, and listed event/venue information. Rutgers/participating-team recaps and established project physical-venue identities were used where the schedule used a broader venue label (notably the Players Era Festival).

## Conference tournament site reference

**Owner-supplied `Conference_Tournament_Site_Reference(20260825-014215).xlsm`.**

This workbook is explicitly incomplete and is not promoted to universal canon. For Rutgers it is used only where a Rutgers-relevant Big East, American, or Big Ten row supplies a populated shared tournament venue and marks the entire tournament at that shared site. Blank Atlantic 10/Eastern Eight rows are treated as research gaps requiring other evidence, not as authoritative blanks. The workbook never establishes H/A/N.

## Supplemental authoritative research

- Official NCAA historical brackets/site records: NCAA Tournament opponent, score, site, and controlled-round verification, especially the 1975 Louisville score and historical venue mapping.
- Atlantic 10 historical championship material and West Virginia tournament history: 1986 Rutgers tournament date/site correction and older tournament context.
- Rutgers Athletics Hall of Fame/history material: 1919-20 National AAU Tournament identification and championship sequence.
- Pittsburgh Athletics historical results: 1973 Rutgers-Pittsburgh forfeit context; the game was stopped at halftime after a student protest with Pitt leading 36-21.
- Current project global `programs.csv`, `conferences.csv`, and `venues.csv` inspected at research baseline `ae823cae233ff287d3c3827c8dbd40ec2db09819` for established shared identities.

## Provenance policy

The `raw_text` field preserves Rutgers source wording. Structured corrections and supplemental venue/date facts are documented in row notes rather than silently rewriting the source. Unknowns remain blank/`UNKNOWN` when the available evidence does not support a stronger assertion.

## Implementation pre-Gate-1 supplemental verification

The serialized Implementation preflight identified several modern structured
normalization defects in the research-frozen package. Rutgers Athletics official
season schedules, recaps, and box scores were used to correct those curated fields
before owner review. Original `raw_text` remains unchanged.

The corrections include the 2018 Michigan State, 2024 Nebraska, and 2025 Minnesota
overtime games; explicit official H/A/N designations for the affected 2017-24
schedule rows; the 2016 Illinois 110-101 three-overtime score; and the obvious
Eastern Michigan/date extraction errors. No genuine Rutgers-versus-reciprocal
historical conflict was silently normalized away.

## Rejected Gate 2 venue-source supplementation

The first public Preview exposed a systematic venue-coverage defect. Rutgers Athletics' home-building history and completed 2024-25 schedule/results were therefore used as supplemental authoritative evidence. The original all-time-scoreboard `raw_text`, `source_site_candidate`, and `source_venue_name` remain unchanged. Curated venue assignment follows the permanent project rule that physical venue chronology may enrich a game only after H/A/N is independently established. Aggregate building records were used as QA signals only, not as row-level site evidence.

The 2024-25 supplement directly establishes seven corrected H/A/N classifications (Monmouth, Notre Dame, Texas A&M, Seton Hall, Columbia, USC regular season, and USC Big Ten Tournament), plus venue/geography for the entire 32-game competitive schedule. Official Rutgers recap/box-score evidence also establishes overtime against Notre Dame and Washington and double overtime against USC in the Big Ten Tournament.

Historical direct series/postseason evidence corrects ten previously unsupported site classifications. The 1975 ECAC Metro final against St. John's is neutral at Madison Square Garden. Remaining historical UNKNOWN rows stay UNKNOWN unless direct game-level evidence supports a stronger classification.

## Assembly Hall physical-identity disambiguation

For the 2025-01-02 Indiana road game, Rutgers uses the existing global alias `Simon Skjodt Assembly Hall` for VEN-000186 so it cannot collide with Illinois VEN-000196. Original raw source evidence remains unchanged.
