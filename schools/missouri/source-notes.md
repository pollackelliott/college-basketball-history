# Missouri Source Notes

## Source hierarchy

For Missouri, source priority is:

1. Official year-by-year, game-by-game records
2. Other official school records and opponent school records
3. Official series summaries / quick-fact tables as QA evidence
4. Secondary sources only when needed to resolve a gap or ambiguity

The canonical game log follows the game-by-game record when a summary table conflicts with it and the season log reconciles.

## Primary Missouri historical source

The historical Missouri game dataset was extracted from Missouri's official historical men's basketball records / media-guide material.

The year-by-year game rows are treated as the primary source for:
- opponent
- date
- score
- result
- site indicator when present
- event/tournament text when present

Season headings and aggregate record summaries are QA evidence, not substitutes for the listed games.

## Modern seasons

Modern seasons from 2016-17 through 2025-26 were curated from season-level official records and merged with the historical dataset.

The current Missouri source-game file contains:
- 2,707 historical rows through 2015-16
- 321 modern rows from 2016-17 through 2025-26
- 3,028 total non-exhibition source-game rows

## Conference membership source

Missouri's conference timeline was supplied from a season-by-season coaching/history table and normalized as:

- 1906-07 — Independent
- 1907-08 through 1927-28 — Missouri Valley
- 1928-29 through 1947-48 — Big Six
- 1948-49 through 1957-58 — Big Seven
- 1958-59 through 1995-96 — Big Eight
- 1996-97 through 2011-12 — Big 12
- 2012-13 through present — SEC

Conference tournament display names should be derived from this season-specific membership.

## NIT source

Missouri NIT history supplied during curation:

- 1972 — St. John's
- 1973 — Massachusetts
- 1985 — Saint Joseph's
- 1996 — Murray State; Alabama
- 1998 — UAB
- 2004 — Michigan
- 2005 — DePaul
- 2014 — Davidson; Southern Miss

Eight appearances, ten games, combined record 2-8.

This list is used to identify NIT games. Scores remain grounded in the canonical/source game rows rather than copied from a summary table.

## NCAA Tournament tagging

NCAA games were identified from Missouri's postseason history and canonical game log.

Rounds are normalized to the project's canonical taxonomy:
- Play-in
- R64
- R32
- Sweet Sixteen
- Elite Eight
- Final Four
- Championship

Historical field sizes are translated by competitive bracket stage rather than literal tournament size.

The March 25, 1944 Pepperdine game is an NCAA regional third-place consolation game. It remains an NCAA Tournament game with no canonical advancement round.

## Conference tournament tagging

Conference tournament games are classified as `CONFERENCE_TOURNAMENT`.

The displayed tournament name is derived from the conference membership for that season rather than manually stored as historical prose.

Only title games receive:
`postseason_round = Championship`

Earlier rounds intentionally remain blank.

## Venue sources

Venue assignments use:
- Missouri home-venue chronology
- game-level source text
- opponent-source reconciliation
- event/site context
- game-specific research when required

Home-venue chronology currently used:
- Rothwell Gym
- Brewer Fieldhouse
- Hearnes Center
- Mizzou Arena

Venue history is suggestive, not dispositive. A venue relationship never overrides stronger game-specific evidence.

## Cross-source evidence

Missouri has been reconciled against the other currently curated programs where their histories overlap:
- Illinois
- Northwestern
- Kansas
- Kentucky

Opponent sources are treated as additional evidence for the same canonical game, not as additional games.

Conflicts are preserved rather than silently overwritten.

## Known source discrepancies

Examples retained in the project notes / reconciliation history include:
- 1919-20 season heading versus listed game-row total
- impossible November 31, 1963 Air Force date
- old Missouri-Kansas site conflicts
- selected modern Missouri-Kansas site discrepancies
- Kentucky score/site corrections
- Braggin' Rights site normalization

These should remain internal QA/reconciliation matters unless a public "Under review" indicator is necessary.

## Exhibitions

Exhibitions are not part of Missouri's canonical competitive-game dataset.

They do not count toward:
- all-time record
- opponent series
- venue statistics
- public game history

If exhibition source metadata is ever retained, it belongs outside the canonical competitive history.
