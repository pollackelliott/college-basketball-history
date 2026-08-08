# Kansas Curation Notes

## Program status

Kansas is curated through 2025-26 under the current project rules. Exhibitions are excluded from competitive history.

## Game coverage

- Historical non-exhibition games through 2024-25: 3,338
- 2025-26 played games: 35
- Total source-game rows: 3,373
- On-court record represented by those rows: 2452-921

The 1916-17 season heading is internally inconsistent with its listed game rows; canonical game coverage follows the game-by-game log rather than inventing or deleting a contest to force an aggregate heading.

## Conference history

Kansas conference membership supplied by the user is normalized season-by-season as:

- 1898-99 through 1906-07 — Independent
- 1907-08 through 1927-28 — Missouri Valley / MVIAA
- 1928-29 through 1947-48 — Big Six
- 1948-49 through 1957-58 — Big Seven
- 1958-59 through 1995-96 — Big Eight
- 1996-97 through present — Big 12

Big Six, Big Seven, and Big Eight are historical names of the same legal conference lineage. Big 12 is a legally distinct conference. These lineage facts are suitable for a future global `docs/conference-history.md` treatment so the same history can be reused for Missouri, Oklahoma, Colorado, Kansas State, Iowa State, Nebraska, and Oklahoma State.

## Postseason classification

Public special game types are limited to conference tournament, NCAA Tournament, and NIT.

- NCAA Tournament: 170 games through 2025-26, 118-52 on court
- NIT: 5 games, 3-2
- Conference postseason tournament: 115 games

NCAA district-playoff games in 1940, 1942, 1946, and 1950 are not counted as NCAA Tournament games because the official Kansas postseason history explicitly excludes district playoffs from NCAA tournament totals. The 1952 Olympic Playoffs are likewise not NCAA Tournament games. NCAA consolation/third-place games remain `NCAA_TOURNAMENT` with a blank canonical round.

The 1968 NIT final loss to Dayton is `NIT` with `postseason_round = Championship`.

Conference tournament `Championship` means Kansas reached the title game, regardless of result. Kansas has 24 championship-game appearances in the curated conference-tournament history: 16 wins and 8 losses. The 1978 Big Eight postseason tournament is not a Kansas championship-game appearance.

## 2017-18 administrative action

Kansas played 39 games and went 31-8 on court in 2017-18. Fifteen on-court wins are separately marked `VACATED_WIN`; the on-court score/result is never overwritten.

## Venue history

Primary Kansas home chronology:

- Snow Hall — before Robinson Gymnasium
- Robinson Gymnasium — May 1907 through Oct. 13, 1927
- Hoch Auditorium — Oct. 14, 1927 through Feb. 28, 1955
- Allen Fieldhouse — Mar. 1, 1955 through present

Kansas City games are classified game-by-game; Kansas City is not inherently neutral. The 1965 Kansas-St. John's game at Ahearn Field House in Manhattan remains Neutral by prior user ruling. Venue chronology is evidence, not a rule that overrides game-specific evidence.

## Opponent identities and cross-source reconciliation

All Kansas opponent identities in the curated historical file are resolved. Current-D1 identities are normalized to the permanent 365-team registry keys in this repository. Historical/non-D1 opponents remain non-clickable evidence-bearing identities.

Known cross-source disagreements with already-curated schools remain discrepancies rather than reasons to create duplicate canonical games.
