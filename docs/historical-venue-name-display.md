# Historical physical-venue name display — Illinois pilot

This is a bounded **site presentation** feature, not a change to canonical
physical venue identity, historical site evidence, or school Research packages.

## Source of truth

Use the existing `data/reference/venue-names.csv` with one
`OFFICIAL_NAMING_PERIOD` row for each verified formal-name stint. Preserve
existing `PROJECT_DISPLAY` and `HISTORICAL_OR_ALIAS` rows: those remain
fallback display and name-identity evidence, **not** automatically dated
official names. One physical venue retains one stable `venue_id`.

An official naming-period row must contain an exact `valid_from` date,
optional exact inclusive `valid_to`, `date_precision=EXACT`, official name,
and source basis. Periods for one venue cannot overlap. If a source supplies
only year-level dates, preserve that uncertainty instead of inventing a day.
Such uncertain names may remain registered as aliases until a safe naming
boundary is established.

## Exact pilot: Illinois

`VEN-000196` (State Farm Center / Assembly Hall, Champaign, IL):

| Official display period (inclusive) | Name |
|---|---|
| 1963-03-02 through 2013-04-28 | Assembly Hall |
| 2013-04-29 onward | State Farm Center |

The University of Illinois athletics facility history identifies opening
on March 2, 1963 and the name change on April 29, 2013. Its April 29
announcement specifies immediate public use of the new name:

- https://fightingillini.com/facilities/state-farm-center/2
- https://fightingillini.com/news/2013/4/29/ui_state_farm_unveil_naming_of_state_farm_center

This is **Illinois**, not Indiana's unrelated Assembly Hall
(`VEN-000186`).

## Site contract

`tools/build_site_data.py` validates sourced naming periods and publishes
a compact deterministic `site/data/venue-name-periods.json` referenced in
`site/data/manifest.json`.

On loading a game, the browser chooses the unique official name only when
both permanent venue ID and game date provide an exact period match.
Otherwise it retains the preexisting project display name. This keeps
the existing 79 large per-team historical game JSON files byte-for-byte
unchanged, rather than requiring a large redundant reserialization for a
site label. Future game or source ingestion continues under normal policy.

Game filters accept any known official name period for the same venue
identity. Site/venue aggregate game counts group by physical venue ID, not
by the particular name displayed on individual historical games.

Adding another independently verified naming history later requires
updating only `venue-names.csv`, running
`python tools/build_site_data.py --apply`, and committing its generated
compact periods reference (plus any other builder-reported changes).
Verify `python tools/check_site_data_freshness.py` and applicable tests.
Do not use a name match to create or merge physical venue IDs.

## Exclusions

No historical venue archaeology or naming-period guesses for other
venues are authorized by this pilot. No change to H/A/N, canonical games,
scores, venues.csv identities, Illinois school venue authoring,
published school scopes, or Research/Implementation gate decisions.
