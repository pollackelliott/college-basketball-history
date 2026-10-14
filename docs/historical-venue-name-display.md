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


## Rollout tranche 2

### Arlington — `VEN-000015`

| Inclusive official period | Name |
|---|---|
| 2009-05-13 through 2013-07-24 | Cowboys Stadium |
| 2013-07-25 onward | AT&T Stadium |

### Las Vegas — `VEN-000135`

| Inclusive official period | Name |
|---|---|
| 1999-04-10 through 2021-02-10 | Mandalay Bay Events Center |
| 2021-02-11 onward | Michelob ULTRA Arena |

### Des Moines — `VEN-000228`

| Inclusive official period | Name |
|---|---|
| 2005-07-12 through 2025-06-30 | Wells Fargo Arena |
| 2025-07-01 onward | Casey's Center |

### Honolulu — `VEN-000686`

| Inclusive official period | Name |
|---|---|
| 1994-10-21 through 1998-02-19 | Special Events Arena |
| 1998-02-20 through 2020-11-11 | Stan Sheriff Center |
| 2020-11-12 through 2025-08-25 | SimpliFi Arena at Stan Sheriff Center |
| 2025-08-26 onward | Bankoh Arena at Stan Sheriff Center |

### Corpus Christi — `VEN-000698`

| Inclusive official period | Name |
|---|---|
| 2004-05-20 through 2025-08-31 | American Bank Center Arena |
| 2025-09-01 onward | Hilliard Center Arena |

Bayfront Plaza Convention Center is the older adjacent convention-center identity,
not a predecessor naming period for this arena.

### Toronto — `VEN-000714`

| Inclusive official period | Name |
|---|---|
| 1922-04-04 through 2003-10-31 | Coliseum Arena |
| 2003-11-01 through 2018-07-10 | Ricoh Coliseum |
| 2018-07-11 onward | Coca-Cola Coliseum |

The 2003 work is treated as renovation of the same 1922 physical building, not
replacement construction.

Authoritative evidence for these six histories is preserved in
`data/reference/venue-names.csv` and the durable Control Center chronology
research on the venue-census maintenance branch.



## Rollout tranche 3

This tranche uses the same date-aware display mechanism as the Illinois proof of concept.
It adds only exact formal naming periods; no physical venue IDs, game rows, school packages,
or H/A/N classifications change.

| Venue | Inclusive official periods |
|---|---|
| Orlando — `VEN-000012` | Amway Center: 2010-10-01–2023-12-19; Kia Center: 2023-12-20 onward |
| Denver — `VEN-000018` | Pepsi Center: 1999-10-01–2020-10-21; Ball Arena: 2020-10-22 onward |
| Orlando/UCF — `VEN-000038` | UCF Arena: 2007-09-08–2013-05-22; CFE Arena: 2013-05-23–2019-04-30; Addition Financial Arena: 2019-05-01 onward |
| Los Angeles — `VEN-000051` | Staples Center: 1999-10-17–2021-12-24; Crypto.com Arena: 2021-12-25 onward |
| Pittsburgh — `VEN-000167` | CONSOL Energy Center: 2010-08-18–2016-10-03; PPG Paints Arena: 2016-10-04 onward |
| Oxford — `VEN-000187` | The Pavilion at Ole Miss: 2016-01-07–2021-06-16; Sandy and John Black Pavilion at Ole Miss: 2021-06-17 onward |
| Kansas City — `VEN-000202` | Sprint Center: 2007-10-10–2020-07-08; T-Mobile Center: 2020-07-09 onward |
| Toronto — `VEN-000444` | Air Canada Centre: 1999-02-20–2018-06-30; Scotiabank Arena: 2018-07-01 onward |
| Miami — `VEN-000499` | AmericanAirlines Arena: 1999-12-31–2021-06-03; FTX Arena: 2021-06-04–2023-01-12; Miami-Dade Arena: 2023-01-13–2023-04-03; Kaseya Center: 2023-04-04 onward |
| Fairfax — `VEN-000576` | Patriot Center: 1985-10-04–2015-06-30; EagleBank Arena: 2015-07-01 onward |
| Portland — `VEN-000778` | Cumberland County Civic Center: 1977-03-03–2014-06-17; Cross Insurance Arena: 2014-06-18 onward |
| Springfield — `VEN-000819` | JQH Arena: 2008-11-13–2022-04-20; Great Southern Bank Arena: 2022-04-21 onward |
| Villanova — `VEN-000860` | Villanova Field House: 1932-04-01–1985-11-21; Jake Nevin Field House: 1985-11-22 onward |

The exact source basis for every boundary is carried on the corresponding
`OFFICIAL_NAMING_PERIOD` row in `data/reference/venue-names.csv`.

Two previously suspected rollout candidates remain intentionally outside this tranche:
`VEN-000503` (DePaul) and `VEN-000863` (Duquesne). Their historical rename conclusions
are preserved, but the available evidence does not justify manufacturing an exact first-period
boundary merely to make them publishable.



## Structural cleanup chronology — Atlantic City

`VEN-000433` remains the single 1929 physical Boardwalk Hall building.

| Inclusive official period | Name |
|---|---|
| 1929-05-31 through 2001-10-10 | Atlantic City Convention Hall |
| 2001-10-11 through 2018-01-15 | Boardwalk Hall |
| 2018-01-16 onward | Jim Whelan Boardwalk Hall |

The modern Atlantic City Convention Center opened as a distinct facility in 1997.
Its name is not an unrestricted alias for `VEN-000433`; literal historical source
wording remains preserved where a source itself used “Atlantic City Convention Center”.


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
