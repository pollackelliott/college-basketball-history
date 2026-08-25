# Michigan men's basketball source-package notes

## Research freeze context

- School: Michigan
- Research base SHA: `4c8d75592f98b42a8534182a5af9bf240b1fd16c`
- Owner history-scope ruling: **Always D1/top-level for site purposes.**
- Covered competitive history: 1908-09 through completed 2025-26.
- Package status: research-frozen source portfolio only. Current-main rebase is mandatory before tracked Phase 0.

## Competitive universe

The Michigan 2026 record book season-by-season ledger contains 2,907 dated schedule entries.
This package includes the **2,896 played competitive varsity games** and excludes **11 cancellations/postponements**.
Exhibitions are excluded.

The package's represented on-court record is **1,764-1,132**. Scores and on-court winner are preserved even when the
record book separately records administrative forfeits or NCAA vacaturs.

Every included game has an exact date and a played score.

## Score orientation

Early Michigan ledger layouts do not always place Michigan's score in a consistent visual column order.
Normalization therefore uses the record book's W/L indicator and signed score margin together with the printed score
to orient Michigan and opponent scores. Raw source text is preserved on every row.

## Home / away / neutral

Game-level Michigan H/A/N notation controls site classification. Venue chronology never establishes H/A/N.

Package distribution:

- SOURCE_PROGRAM_HOME: 1,402
- OPPONENT_HOME: 1,122
- NEUTRAL: 372
- UNKNOWN: 0

Michigan's aggregate H/A/N history table does not perfectly reconcile to the explicit game-level ledger.
The explicit game rows are retained because project policy gives game-level evidence priority over aggregates.

Three NIT rows use `vs.` wording while the Michigan H/A field explicitly marks the contests as home games; they remain
SOURCE_PROGRAM_HOME.

## Administrative outcomes

The record book marks **170 games** with an asterisk and states that U-M vacated wins/losses due to NCAA sanctions.
Those comprise 113 on-court wins and 57 on-court losses. The package records `VACATED_WIN` for the 113 on-court wins
and `VACATED_GAME` for the 57 on-court losses while preserving the played result.

Four `W-FF` rows are on-court Michigan losses followed by an administrative forfeit to Michigan:

- 1982-01-07 Wisconsin
- 1983-03-02 at Wisconsin
- 1984-01-14 at Wisconsin
- 2002-11-23 St. Bonaventure

The three Wisconsin season footnotes explicitly say Wisconsin won on court but forfeited because of an ineligible player.
The St. Bonaventure ledger row supplies the `W-FF` administrative notation but not the reason.

The season-summary `Overall:` records for 1981-82, 1982-83, 1983-84, and 2002-03 therefore differ by one W/L from this
package's on-court season record, exactly because the package follows the project's on-court-result policy.

## Game-type taxonomy

- REGULAR_SEASON: 2,701
- CONFERENCE_TOURNAMENT: 58
- NCAA_TOURNAMENT: 105
- NIT: 31
- POSTSEASON: 1

The sole generic POSTSEASON row is Michigan-Indiana on 1974-03-11 in Champaign, the owner-approved Big Ten playoff.
It predates the Big Ten Tournament and is not classified as CONFERENCE_TOURNAMENT.

Regular-season classics/invitationals remain REGULAR_SEASON.

Conference Tournament and NIT rounds are blank except championship games, which use `Championship`.
NCAA rounds use only the repository's controlled NCAA round vocabulary; historical NCAA consolation/third-place games
remain NCAA_TOURNAMENT with blank canonical round.

## Conference chronology

- 1908-09: Independent
- 1909-10 through 1916-17: no Michigan varsity team
- 1917-18 through 2025-26: Big Ten

Historical Western Conference / Big Nine terminology is normalized to the repository's stable `big-ten` identity.

## Venue methodology

Primary Michigan home facilities:

- Waterman Gymnasium: inaugural 1908-09 season and 1917-18 through 1922-23
- Yost Field House: 1923-24 through 1966-67
- Crisler building: 1967-68 onward; current project identity `crisler-center` / `VEN-000261`

Home-arena chronology is used only after a source row independently establishes Michigan home status.

NCAA Tournament rows have complete physical venue identity and city/state support in the research package.
Big Ten Tournament venue assignments use only the owner-authorized complete Big Ten section of
`Conference_Tournament_Site_Reference(6).xlsm`.

### Research-time new physical venue candidates

The following physical venues are not present in the research-base global venue registry and therefore use provisional
numeric IDs that **must not be treated as final**:

- Frost Bank Center, San Antonio, TX (Michigan source name: AT&T Center) -> provisional `VEN-000281`
- Beasley Coliseum, Pullman, WA (Michigan source name: Wallis Beasley) -> provisional `VEN-000282`
- Britt Brown Arena, Wichita, KS (Michigan source name: Kansas Coliseum) -> provisional `VEN-000283`
- Veterans Memorial Coliseum, Portland, OR (Michigan source name: Memorial Coliseum) -> provisional `VEN-000284`
- Waterman Gymnasium, Ann Arbor, MI -> provisional `VEN-000285`
- Yost Field House, Ann Arbor, MI -> provisional `VEN-000286`

At integration, current main must be checked for intervening additions, key/name collisions, and consumed numeric IDs.
Reuse a venue added by another team rather than creating a duplicate.

### Existing physical venue requiring a research alias

The 1948 NCAA games occurred in Madison Square Garden III (the 1925-1968 building), existing `VEN-000123`.
Because current main uses the public display text `Madison Square Garden` for both the 1925 and 1968 physical buildings,
this research package uses the disambiguating curated name `Madison Square Garden III` for `VEN-000123`.
Integration must add/reuse an appropriate date-aware alias while leaving the global public display convention intact.

## Opponent identities

There are **309 distinct Michigan source opponent labels** and all 309 are resolved for this research package.

Modern/current program aliases are normalized to established program identities. Historical clubs, military teams,
local organizations, and non-current institutions remain separate identities unless institutional lineage is supported.
No unresolved opponent identity remains.

## Accomplishment evidence collected

Michigan's current official record book supports the following integration-time accomplishment values:

- Conference regular-season championships: 16
- Conference tournament championships: 4
- NCAA Tournament appearances: 33
- Final Fours: 9
- National championships: 2
- Best Finish: NATIONAL_CHAMPION
- Best Finish Year: 2026

Accomplishments are research evidence for later Owner Gate 1 / integration and are not a tracked repository write here.

## Owner questions

None remain.

## Required integration action

**CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES.**

This package is a research-frozen input artifact. It is not integration-frozen and has not run authoritative onboarding preflight.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=ae823cae233ff287d3c3827c8dbd40ec2db09819` from `research_base_sha=4c8d75592f98b42a8534182a5af9bf240b1fd16c`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
