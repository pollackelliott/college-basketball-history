# Missouri Curation Notes

## Program status

Missouri is closed through the 2025-2026 season under the current project rules for:
- canonical game coverage
- opponent normalization
- competitive site classification
- venue normalization where evidence supports an exact venue
- conference membership history
- conference tournament / NCAA Tournament / NIT tagging
- cross-source reconciliation against the other currently curated programs

Closed does not mean immutable. New evidence may still justify a future correction.

## Canonical competitive record

- 3,028 non-exhibition games through 2025-2026
- On-court record: 1,754-1,274
- Exhibitions are excluded from canonical competitive history and public totals.

Administrative forfeits or vacated wins do not overwrite the on-court score/result. Any administrative result is stored separately from the played result.

## Season and date notes

### 1919-1920
The season heading reports 17-1, but the listed game rows produce 15-1. The canonical dataset follows the game-by-game log and does not invent missing games.

### 1963 Air Force
A source row contains the impossible date November 31, 1963. Preserve the source assertion, but do not invent an exact canonical date unless another source resolves it.

## Home venue history

Primary Missouri home venues are treated as:

- Rothwell Gym — through January 1930
- Brewer Fieldhouse — January 1930 through 1971-1972
- Hearnes Center — 1972-1973 through 2003-2004
- Mizzou Arena — 2004-2005 to present

Venue relationships are evidence and defaults, not rules that override game-specific evidence.

## Kansas City site policy

Kansas City is not inherently neutral for Missouri.

A game may be Missouri Home, Opponent Home, Neutral, or Unknown depending on the actual scheduling/site context.

Specific Missouri-designated home rulings include:
- 2010-11 Georgetown in Kansas City — Missouri Home
- 2023-24 Seton Hall in Kansas City — Missouri Home

## Multi-team event site policy

If Missouri plays the actual host of an event at that host's normal home site, classify the game as Opponent Home.

Other participants at the same host-site event are normally Neutral.

Examples previously resolved under this rule include games at:
- Arizona State / Tempe
- UTEP / El Paso
- Kentucky / Lexington
- Tennessee / Knoxville
- USC / Los Angeles

## Missouri-Illinois / Braggin' Rights

Braggin' Rights games in St. Louis are Neutral.

Historical cross-source reconciliation has been performed against Illinois.

## Missouri-Kansas reconciliation

Modern site corrections confirmed from cross-source review include:
- 2003-03-09 at Missouri — Missouri Home, Hearnes Center
- 2009-03-01 at Kansas — Opponent Home, Allen Fieldhouse
- 2010-01-25 at Kansas — Opponent Home
- 2011-02-07 at Kansas — Opponent Home
- 2012-02-25 at Kansas — Opponent Home

Two 1906-07 Missouri-Kansas site conflicts remain historical source disagreements and should stay documented rather than guessed.

Kansas-source-only games currently retained as provisional canonical contests:
- 1920-02-19
- 1924-03-26

## Kentucky reconciliation

Resolved Missouri-Kentucky corrections include:
- 2013-02-23 — Missouri road / Kentucky home
- 2016-01-27 — Missouri road / Kentucky home
- 2018-02-24 — Kentucky 87, Missouri 66

The 2018-02-24 score follows the official final record.

## Postseason classification

Public special game types are limited to:
- CONFERENCE_TOURNAMENT
- NCAA_TOURNAMENT
- NIT

Other regular-season events and lesser postseason events are not specially tagged for public display.

Conference tournament labels are derived from Missouri's conference membership in that season:
- Big Eight Tournament
- Big 12 Tournament
- SEC Tournament

Conference tournament `postseason_round` is populated only for the Championship game.

NIT `postseason_round` is populated only for an NIT Championship game. Missouri has no NIT Championship game in its eight appearances.

NCAA Tournament rounds use only:
- Play-in
- R64
- R32
- Sweet Sixteen
- Elite Eight
- Final Four
- Championship

Historical tournaments are normalized by competitive bracket stage, not literal field size.

### 1944 NCAA consolation exception
Missouri's March 25, 1944 game against Pepperdine was an NCAA regional third-place consolation game after an Elite Eight loss to Utah.

It is classified as:
- `game_type = NCAA_TOURNAMENT`
- `postseason_round = blank`

The specific consolation-game description is retained internally. This same rule should be used for rare NCAA regional or national third-place/consolation games elsewhere in the database.

## Public presentation philosophy

The site should present corrected historical information matter-of-factly.

Internal discrepancy records may document source errors, but the public site should not frame itself as correcting or embarrassing athletic departments.

When a canonical fact remains unresolved, the public-facing system may show an understated "Under review" indicator rather than invent a resolution.
