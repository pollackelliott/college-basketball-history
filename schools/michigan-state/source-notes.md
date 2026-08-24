# Michigan State source notes

## Primary historical source

**2025-26 Michigan State Men's Basketball Media Guide**  
Michigan State University Athletics  
Owner-supplied filename: `2526_MSU_MBB_Media_Guide_12.2.pdf`

The year-by-year results ledger is the package backbone through 2024-25.

High-value internal cross-check sections used include:
- season-by-season records
- all-time opponent series with game-level H/A/N
- NCAA Tournament history
- NIT history
- Big Ten Tournament history
- championship/history sections
- historical facility/home-court material

The package preserves the printed chronological source claim in `raw_text`. Structured normalization does not silently rewrite source evidence.

## Completed 2025-26 source

**Michigan State Athletics — 2025-26 Men's Basketball Schedule**

https://msuspartans.com/sports/mens-basketball/schedule/2025

The completed official schedule supplies 35 competitive games and a 27-8 record.

It explicitly labels:
- Bowling Green (2025-10-23) — Exhibition
- at Connecticut (2025-10-28) — Exhibition

Those two contests are excluded from competitive history.

The text schedule also supplies modern H/A/N and venue/location evidence, including Suncoast Credit Union Arena for the Ft. Myers Classic.

## Michigan State historical home-court evidence

Michigan State institutional history identifies the program's five homes as:
- Armory
- the gym in today's IM Circle complex
- Demonstration Hall
- Jenison Field House
- Breslin Center

Institutional historical feature:
https://spartan.msu.edu/spartan-story-hub/news/1998/10/feature-100-seasons-of-spartan-basketball

Michigan State historical record material establishes that Tennessee on 1940-01-06 was the first basketball game at Jenison Field House:
https://msuspartans.com/documents/download/2015/4/30/_msu_m_baskbl__06-mg-section8.pdf

The project reuses current-main physical identities for Jenison and Breslin. The three earlier MSU home facilities are research-time new physical candidates; exact early Armory/IM Circle game boundaries remain intentionally unassigned rather than inferred.

## Big Ten membership

Big Ten official conference history:
https://bigten.org/article/bltd5401bb886795cf2

The conference states that Michigan State College was added to the Big Ten in 1949. The basketball package represents:
- Independent through 1949-50
- Big Ten beginning 1950-51

Big Ten 2025-26 record book:
https://bigten.org/api/media/file/All%20Sports%20Record%20Book%20%282025-26%29%2C%20V2.pdf

The project uses one stable `big-ten` identity for the league's historical naming lineage.

## Conference Tournament Site Reference

Owner-supplied file:
`Conference_Tournament_Site_Reference.xlsx`

This workbook is an in-progress universal reference and is not treated as universal canon.

For Michigan State, the owner explicitly authorized only the completed **Big Ten** section.

The Big Ten section is used solely for shared physical tournament venue/city/state enrichment. Its own instructions explicitly prohibit using tournament geography to infer H/A/N.

Authorized Big Ten site coverage runs from the first Big Ten Tournament in 1998 through the 2026 tournament at the United Center.

## NCAA Tournament research

Michigan State's dedicated media-guide NCAA Tournament table is the primary internal postseason cross-check for:
- tournament participation
- opponent
- round
- source site city wording

Physical venue identity is completed using established project NCAA venue evidence and authoritative/contemporary venue research.

All 116 NCAA Tournament rows through 2026 have a physical venue plus city/state.

Notable internal/source conflicts:
- **2021 UCLA First Four:** Michigan State contemporary official schedule/recap establishes 2021-03-18 and Mackey Arena in West Lafayette, Indiana; the dedicated historical table has conflicting date/site wording.
- **2025 Auburn Elite Eight:** the year-by-year ledger's malformed `3/3025` token is normalized to 2025-03-30; the NCAA section identifies the Atlanta Regional Final.

## NIT research

The chronological ledger and Michigan State NIT history identify 12 competitive NIT games.

For **1997 Florida State**, contemporary/archival Michigan State schedule evidence supports 1997-03-17; a historical NIT table carries a conflicting March 19 date. The package uses March 17 structurally and preserves the source conflict in documentation.

## All-time opponent-series use

The media guide's all-time opponent-series section is the main historical H/A/N cross-check. Explicit series notation controls over geography.

Three tail-end page-header extraction defects were repaired from the printed game rows:
- Wisconsin rows were not allowed to inherit the neighboring Winona header
- `S.W. Louisiana` rows were not allowed to inherit the neighboring SW Missouri State header
- the three genuine Winona/Winona College games remain distinct historical Winona evidence

This is an extraction repair, not a rewrite of basketball history.

## Competitive-universe exclusions

Three printed chronological rows are excluded from competitive history because Michigan State's own season totals omit them:

- 1959-01-17 MSU Alumni
- 1965-12-27 Hawaiian Marines
- 1965-12-30 Hawaiian Army

The 1958-59 summary reports 23 games, exactly one fewer than the chronological page including MSU Alumni. The 1965-66 summary reports 22 games, exactly two fewer than the chronological page including the two service-team contests.

No other printed varsity game is removed to force an aggregate.

## Administrative outcomes

Five media-guide `W(F)` notations are represented with `administrative_status = FORFEIT`.

The played score and played W/L remain on-court truth under project policy.

## Accomplishments

Media-guide championship/history sections and the completed 2025-26 season support the later integration values:

- 17 Big Ten regular-season championships
- 6 Big Ten Tournament championships
- 39 NCAA Tournament appearances through 2026
- 10 Final Fours
- 2 NCAA championships
- best NCAA finish: National Champion
- most recent championship/best-finish year: 2000

## Research-base and rebase warning

Research was conducted against:

`4c8d75592f98b42a8534182a5af9bf240b1fd16c`

Any newly proposed global numeric venue ID in this package is provisional. CURRENT-main shared-identity rebase is mandatory before tracked Phase 0.

## Integration normalization — overtime periods

During pre-Gate integration, 98 `overtime_periods` values were corrected
after a systematic extraction artifact was identified. The affected rows
already correctly identified overtime games in preserved `raw_text`, but
the extracted numeric field had captured the opponent score for one-OT
games or concatenated the opponent score with the explicit `2OT`/`3OT`
marker.

The correction was deterministic from each preserved score and OT token:
`ot` / `1OT` = 1, `2OT` = 2, and `3OT` = 3. No dates, scores, results,
opponents, site classifications, venues, game types, or raw source text
were changed.

## Integration normalization — remaining source-internal corrections

Three additional historical-ledger defects were normalized before Owner Gate 1
using stronger Michigan State contemporary official evidence while preserving
the original printed claims in `raw_text`:

- `MSURAW-02823`: Northwestern 81-55 belongs to 2018-19 and was played
  2019-01-02 at Breslin Center. The historical ledger printed `11/2/19`
  and placed it at the beginning of the 2019-20 section.
- `MSURAW-02216`: the 2002 Big Ten Tournament loss to Indiana was played
  2002-03-08. Contemporary MSU recap/game notes override the ledger's
  `3/9/02` transcription.
- `MSURAW-02946`: the 2023 Iowa 112-106 loss required one overtime.
  Contemporary MSU recap/box score override the later ledger's `2OT`.

The 35 completed 2025-26 competitive rows also had metadata wording changed
from `exhibitions excluded` to `non-record preseason contests omitted`.
This is wording-only and prevents the generic exhibition-warning detector
from flagging every legitimate 2025-26 competitive game. Bowling Green
(2025-10-23) and at Connecticut (2025-10-28) remain excluded from the
competitive universe.
