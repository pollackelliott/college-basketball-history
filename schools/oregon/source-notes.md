# Oregon source notes

## Primary institutional source

**Oregon Men's Basketball 2025-26 Record Book**, University of Oregon Athletics (owner-supplied PDF).

The record book is the backbone of the portfolio through the completed 2024-25 season. Research sections used include:
- year-by-year results;
- season H/A/N summaries and source game markers;
- McArthur Court / Matthew Knight Arena history;
- all-time opponent series;
- conference-tournament history;
- NCAA Tournament results;
- NIT results;
- regular-season tournament history;
- accomplishment/history sections.

Raw source strings are retained in `raw_text`. Source notation is not silently rewritten when a structured normalization is made.

## 2025-26 completed-season supplement

Oregon Athletics official schedule/results supplies the completed 2025-26 season because the record book predates its completion:

https://goducks.com/sports/mens-basketball/schedule/2025-26

The competitive supplement contains 32 games and a 12-20 record. The Utah and Stanford preseason exhibitions are excluded from the competitive portfolio.

## Conference tournament site reference

Owner-supplied **Conference Tournament Site Reference** workbook.

Owner ruling for this lane:
- the workbook is **globally incomplete** and must not be ingested as universal canon;
- its Oregon-relevant Pac-10/Pac-12/Big Ten tournament physical-site history is complete enough to use for Oregon research;
- it supplies physical venue/city/state only and never H/A/N.

The package independently verifies Oregon conference chronology and does not inherit workbook conference-label defects.

## Conference chronology research

Oregon Athletics' institutional conference-history material establishes Oregon's Pacific Coast Conference entry in 1918 and its move to the Big Ten beginning in 2024-25. Pac-12 historical material is used to distinguish the PCC, AAWU, Pac-8, Pac-10, and Pac-12 eras.

Representative Oregon institutional history:
https://goducks.com/news/2024/6/30/mens-basketball-ducks-officially-join-big-ten-conference

## Exact-date recovery

San José State official historical men's basketball records were used reciprocally to recover the previously blank Oregon-San Jose State date as 1926-01-02. The reciprocal source's 26-4 score conflicts with Oregon's 24-6 score; only the date is imported into Oregon's structured assertion.

The other four date blanks remain unresolved after bounded reciprocal/institutional and historical-archive research.

## Home venues

University of Oregon institutional history and contemporary Eugene newspaper material establish the early gym succession, including the 1909 Men's Gymnasium and its 1910-02-12 basketball opening. Oregon's record book establishes:
- McArthur Court first game: 1927-01-14;
- McArthur Court final Oregon game: 2011-01-01;
- Matthew Knight Arena first Oregon men's basketball game: 2011-01-13.

## NCAA and NIT site evidence

Oregon's dedicated NCAA and NIT tables establish the postseason game universe and city-level history. Physical arenas are resolved from Oregon official schedules/box-score context, NCAA/institutional venue evidence, and current-main established physical identities where already present.

Every played NCAA Tournament row and every NIT row is physically site-complete.

## Modern schedule cross-checks

Oregon Athletics' historical online schedules were used to resolve or document source-summary conflicts where available, particularly modern H/A/N anomalies. The game-level official schedule is preferred over a contradictory aggregate summary line; no H/A/N value is inferred from venue or geography.

Examples:
- 2011-12 Washington State in Spokane is an Oregon away game despite the off-campus Spokane Arena location.
- 2017-18 NIT Rider is an Oregon home game.
- 2021-22 official schedule reports a 12-5 home record, resolving the record-book summary-line discrepancy.

## Research-base venue comparison

Research base:
`fb886afc1f940ddc9e5904908cc2f2c5cf7077cb`

The Oregon local physical venue identities were compared against `data/reference/venues.csv` at that research base. Forty-two are definite physical reuses; six are new candidates. No ambiguous physical-identity match remains at research freeze.
