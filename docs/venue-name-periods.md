# Venue names by historical period — Illinois pilot

The physical venue identity remains the immutable global `venue_id`. Historic
display names are separate, time-bounded records in the existing
`data/reference/venue-names.csv`.

## Controlling data

Rows with `name_type=OFFICIAL_NAMING_PERIOD` and source-backed
`EXACT` start/end dates are eligible for date-aware public display.
`valid_from` and `valid_to` are **inclusive** calendar dates;
blank `valid_to` means open-ended. The default `PROJECT_DISPLAY`
record and undated `HISTORICAL_OR_ALIAS` records remain useful for
physical identity, input matching, and fallback, but do **not**
automatically define historical display periods.

For this pilot, Illinois' `VEN-000196` represents one arena in Champaign:

- **Assembly Hall:** 1963-03-02 through 2013-04-28.
- **State Farm Center:** 2013-04-29 onward.

Source: [University of Illinois April 29, 2013 naming announcement](https://fightingillini.com/news/2013/4/29/ui_state_farm_unveil_naming_of_state_farm_center)
(explicitly effective immediately); the [university facility history](https://fightingillini.com/facilities/state-farm-center/2)
confirms original March 2, 1963 opening.

Do **not** map Indiana's unrelated `VEN-000186` Assembly Hall to the
Illinois naming intervals. Resolution always uses permanent venue ID,
never a normalized arena-name match.

## Website behavior

`tools/build_site_data.py` validates and publishes the dated official
periods to the small deterministic `site/data/venue-name-periods.json`
asset, referenced by `site/data/manifest.json`.

The browser resolves the display name by **venue ID and exact game date**.
If a date is missing, inexact, outside the documented period, or
otherwise not covered, it preserves the original project display name.
All underlying canonical game rows, score and site classifications,
and school Research packages remain unchanged.

Game lists use the historical name. Venue filter suggestions include
both historic and modern names but match by the same physical venue ID;
series venue summaries aggregate the same building rather than splitting
its games into two venue identities.

## Adding further venues

Research each official naming boundary from authoritative facility
history and record the source in `source_basis`. Name periods for one
venue must not overlap, and aliases must not be turned into official
name periods just because their labels exist. Run the deterministic
site builder, commit its generated asset/manifest changes in the same
small maintenance PR, and require regression tests and site-data
freshness validation.
