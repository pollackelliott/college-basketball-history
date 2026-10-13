# Historical physical-venue name display

This is a **site presentation** feature. It does not change canonical physical
venue identity, game identity, H/A/N, scores, source evidence, or school
Research packages.

## Source of truth

Use the existing `data/reference/venue-names.csv` with one
`OFFICIAL_NAMING_PERIOD` row for each independently verified formal-name
stint. Preserve `PROJECT_DISPLAY` and `HISTORICAL_OR_ALIAS` rows for stable
registry identity and lookup. One physical building retains one stable
`venue_id`.

A naming-period row requires an exact `valid_from`, optional exact inclusive
`valid_to`, `date_precision=EXACT`, official venue name, and institutional
source basis. Periods for one venue may not overlap. Do not invent an exact
boundary from year-only evidence.

## Website display rule

For a game with an exact date, choose the official name whose verified naming
period contains that date.

If the game date is absent or not precise enough to select a historical period,
display the **most recent verified and accepted official name** for that
physical venue. This is the project-wide fallback rule for migrated venues.
Do not guess which historical period contained an imprecisely dated game.

If an exact game date falls outside every established period, preserve the
existing project display rather than concealing a chronology gap.

Game filters accept every verified official-period name for the same physical
venue.

Head-to-head and other venue aggregate summaries use **one label per physical
venue**, never a concatenation of historical names. If the latest verified
official naming period is open-ended, use that current official name. If the
venue's naming history is closed/inactive, use the canonical project display
name. Aggregate counts continue to group by `venue_id`, not by displayed
historical name.

## Owner display conventions superseded by this feature

Owner ruling, 2026-10-13: earlier project-display conventions for **Illinois,
Indiana, and Tennessee** do not constrain the date-aware historical naming
system. Once verified naming periods are registered for those venues, the
period-based website display controls. Existing project-display rows may remain
as registry/fallback identities; they are not authority to force one name
across all historical dates.

## Verified reference example: Illinois

`VEN-000196`, Champaign, IL:

| Inclusive official period | Name |
|---|---|
| 1963-03-02 through 2013-04-28 | Assembly Hall |
| 2013-04-29 onward | State Farm Center |

Institutional evidence:
- https://fightingillini.com/facilities/state-farm-center/2
- https://fightingillini.com/news/2013/4/29/ui_state_farm_unveil_naming_of_state_farm_center

The Illinois POC was production-verified against actual public game display.

## Rollout tranche 1

### Colorado — `VEN-000052`

| Inclusive official period | Name |
|---|---|
| 1979-08-08 through 1990-09-19 | CU Events/Conference Center |
| 1990-09-20 through 2018-06-30 | Coors Events Center |
| 2018-07-01 onward | CU Events Center |

Institutional evidence:
- https://cubuffs.com/news/2018/7/3/general-cus-sports-arena-renamed-cu-events-center
- https://cubuffs.com/sports/2005/5/4/119110

### Syracuse — `VEN-000096`

| Inclusive official period | Name |
|---|---|
| 1980-09-20 through 2022-05-18 | Carrier Dome |
| 2022-05-19 onward | JMA Wireless Dome |

Institutional evidence:
- https://cuse.com/news/2005/9/20/Domefirstevent
- https://cuse.com/news/2022/5/18/general-syracuse-university-jma-wireless-announce-naming-rights-partnership-usher-in-the-jma-wireless-dome-era

## Publication contract

`tools/build_site_data.py` validates naming periods and publishes compact,
deterministic `site/data/venue-name-periods.json`, referenced from the site
manifest. The browser resolves the displayed name from permanent venue identity
plus game date/precision.

Adding a later verified venue history normally requires:
1. adding sourced `OFFICIAL_NAMING_PERIOD` rows;
2. running `python tools/build_site_data.py --apply`;
3. committing the compact generated periods reference and any builder-reported
   deterministic outputs;
4. running site freshness and applicable regression tests.

Do not create or merge physical venue IDs from name similarity.

## Rollout discipline

The registry contains many aliases that are not necessarily formal historical
renames. Do not mass-convert aliases into naming periods. Prefer bounded
tranches of clearly same-building renames with institutional date evidence.
Spelling variants, shorthand, replacement buildings, uncertain identity, and
year-only boundaries remain outside a tranche until independently resolved.
