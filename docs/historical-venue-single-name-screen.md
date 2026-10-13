# Historical venue single-name high-yield screen

Status: **IN PROGRESS — LIGHT SCREEN ONLY**  
Source census: `docs/historical-venue-name-census.md`  
Protected-main screen baseline: `3f9edc3de0237fde453a87000cf6755b97962687`

## Purpose

This is the agreed lightweight follow-up to the completed multi-name ambiguity census.

The protected-main baseline contains **483 venue IDs with exactly one registered venue-name row**. This screen looks only for obvious signs that a supposedly single-name physical venue may actually have a missing formal historical naming era.

It is deliberately not 483 deep research campaigns.

A screen hit is a **research candidate**, not historical authority and not implementation authority. Exact naming chronology, physical continuity, alias-vs-period treatment, and transition dates still require authoritative verification before any `OFFICIAL_NAMING_PERIOD` or shared-reference mutation.

## Screen method

### Repository-internal cross-check — COMPLETE

All 483 single-name global venue IDs were mechanically cross-checked against all 79 published `schools/*/venues.csv` files at the protected-main baseline.

The test looked for the same single-name global `venue_id` appearing in a published school table with a materially different local `canonical_name` or nontrivial `aliases` value.

Result: **0 internal alternate-name hits**.

This means the existing published school venue tables do not themselves expose obvious missing aliases for the 483 single-name IDs. It does not prove those venues lack historical renames.

### External high-yield risk screening

Only obvious sponsor/rebrand-risk names are checked, in bounded tranches. Generic web search is discovery only. A positive hit means later focused authoritative chronology research is warranted.

## Tranche 1 — sponsor/rebrand-risk venues

| Venue | Baseline single name | Screen result | Discovery basis / next step |
|---|---|---|---|
| `VEN-000089` | Indiana Farmers Coliseum | `SCREEN_POSITIVE` | Same physical venue is now Corteva Coliseum; Indiana State Fair material confirms the current rename, while historical discovery also points to earlier Fairgrounds/Pepsi naming eras. Later research should establish the complete formal chronology and exact boundaries from State Fair/archival authority. |
| `VEN-000135` | Michelob ULTRA Arena | `SCREEN_POSITIVE` | Mandalay Bay announced on 2021-02-11 that Mandalay Bay Events Center was renamed Michelob ULTRA Arena. At minimum one omitted predecessor era exists. Later research should verify opening date/name and effective-day semantics. |
| `VEN-000244` | Cadence Bank Arena | `SCREEN_POSITIVE` | Contemporary Tupelo reporting confirms BancorpSouth Arena was rebranded Cadence Bank Arena in 2022; discovery also points to earlier Tupelo Coliseum / BancorpSouth Center wording. Later authoritative chronology research required. |
| `VEN-000354` | HTC Center | `SCREEN_CLEAR_CURRENT_PASS` | Coastal Carolina announced naming rights for its new Student Recreation and Convocation Center before/at opening and continues to use the full `HTC Student Recreation and Convocation Center` identity. Current evidence looks like formal full-name/shorthand concurrency rather than an omitted historical naming period. No follow-up candidate from this light pass. |
| `VEN-000596` | Landers Center | `SCREEN_POSITIVE` | DeSoto County audit evidence states the DeSoto Civic Center was renamed Landers Center effective 2012-01-01. One omitted predecessor era is directly supported. |
| `VEN-000607` | LionTree Arena | `SCREEN_POSITIVE` | UC San Diego explicitly states RIMAC Arena was renamed LionTree Arena in 2022. One omitted predecessor era is directly supported. |
| `VEN-000642` | Idaho Central Arena | `SCREEN_POSITIVE` | Local contemporaneous reporting identifies the same building as Bank of America Centre → Qwest Arena → CenturyLink Arena → Idaho Central Arena. Later research should replace discovery reporting with venue/owner authority and verify exact boundaries. |
| `VEN-000675` | BB&T Arena | `SCREEN_POSITIVE` | Northern Kentucky University material identifies the current Truist Arena as formerly The Bank of Kentucky Center and BB&T Arena. The protected-main single-name row is both incomplete and no longer current. Later authoritative chronology research required. |
| `VEN-000686` | Special Events Arena | `SCREEN_POSITIVE` | University of Hawai‘i confirms the 1994 building opened as Special Events Arena, later became Stan Sheriff Center, then SimpliFi Arena at Stan Sheriff Center in 2020 and Bankoh Arena at Stan Sheriff Center in 2025. This is a clear missing multi-era lineage. |
| `VEN-000714` | Coca-Cola Coliseum | `SCREEN_POSITIVE` | Coca-Cola Coliseum’s own venue guide states the building was known as Ricoh Coliseum from 2003-2018 before the Coca-Cola name; earlier Coliseum-era identity also predates 2003. Later research should establish the complete formal pre-2003 wording and exact boundaries. |

### Tranche 1 count

- Screened: **10**
- `SCREEN_POSITIVE`: **9**
- `SCREEN_CLEAR_CURRENT_PASS`: **1**
- Deep chronology research performed: **0**

## Tranche 2 — remaining obvious sponsor-risk names

This tranche was mechanically limited to the seven unscreened single-name venues whose current project display names matched the sponsor/rebrand-risk filter. No additional venues were added merely to reach an arbitrary tranche size.

| Venue | Baseline single name | Screen result | Discovery basis / next step |
|---|---|---|---|
| `VEN-000010` | American Airlines Center | `SCREEN_CLEAR_CURRENT_PASS` | American Airlines Center's own history says the Dallas building has operated under that name since opening in 2001. No omitted operational naming era surfaced in this light pass. Source: https://www.americanairlinescenter.com/about-aacenter/ |
| `VEN-000165` | Pinnacle Bank Arena | `SCREEN_CLEAR_CURRENT_PASS` | Nebraska/City of Lincoln announced the Pinnacle Bank name in 2011, before the arena's 2013 opening. The sponsor name therefore predates operation; no omitted operational predecessor era surfaced. Sources: https://huskers.com/news/2011/12/06/city-announces-arena-name ; https://huskers.com/news/2013/08/30/pinnacle-bank-arena-opens |
| `VEN-000222` | US Bank Stadium | `SCREEN_CLEAR_CURRENT_PASS` | U.S. Bank Stadium opened in 2016 under its current name. No prior operational venue-name era surfaced in the light pass; construction/project labels are not naming periods. Source: https://www.minneapolis.org/things-to-do/itineraries/52-must-sees/us-bank-stadium/ |
| `VEN-000228` | Wells Fargo Arena | `SCREEN_POSITIVE` | Iowa Events Center states Wells Fargo Arena was renamed Casey's Center effective 2025-07-01. The protected-main single-name row is now both incomplete and stale. Later research should verify the full 2005-2025 Wells Fargo era and Casey's boundary from owner/facility authority. Sources: https://www.iowaeventscenter.com/about ; https://www.desmoinesarena.com/about/ |
| `VEN-000294` | Suncoast Credit Union Arena | `SCREEN_CLEAR_CURRENT_PASS` | Florida SouthWestern identifies the arena as a 2016-built facility and current institutional material continues the Suncoast Credit Union Arena identity. No clear operational rename signal surfaced in this light pass. Source: https://www.fsw.edu/arena/about |
| `VEN-000567` | Alaska Airlines Center | `SCREEN_CLEAR_CURRENT_PASS` | UAA announced the Alaska Airlines Center name in 2013 while the new arena was still under construction; it opened under that name in September 2014. Earlier project/planning labels are not operational naming periods. Sources: https://goseawolves.com/news/2013/3/21/206822709.aspx ; https://www.uaa.alaska.edu/news/archive/2014/09/aac-benefits-uaa-larger-community.cshtml/%5E0 |
| `VEN-000698` | American Bank Center | `SCREEN_POSITIVE` | Corpus Christi visitor/facility material states the complex formerly known as American Bank Center is now Hilliard Center; the original American Bank naming announcement also states the expanded complex had previously been Bayfront Plaza Convention Center. This is a clear multi-era candidate requiring later physical-scope/arena-vs-complex chronology research. Sources: https://www.visitcorpuschristi.com/meet/venues/convention-center/ ; https://americanbankcenter.com/newsroom/id-938 |

### Tranche 2 count

- Screened: **7**
- `SCREEN_POSITIVE`: **2**
- `SCREEN_CLEAR_CURRENT_PASS`: **5**
- Deep chronology research performed: **0**

### Cumulative light-screen count

- Screened: **17 / 483**
- `SCREEN_POSITIVE`: **11**
- `SCREEN_CLEAR_CURRENT_PASS`: **6**
- Deep chronology research performed: **0**

## Current candidate queue

The following single-name venues now warrant later bounded chronology research:

- `VEN-000089`
- `VEN-000135`
- `VEN-000228`
- `VEN-000244`
- `VEN-000596`
- `VEN-000607`
- `VEN-000642`
- `VEN-000675`
- `VEN-000686`
- `VEN-000698`
- `VEN-000714`

Do not periodize or mutate shared registries from this screen alone.

## Stopping rule

Continue in small high-yield tranches of obvious sponsor/rebrand-risk names. A venue that produces no clear rename signal in the light pass is marked screened and left alone; do not open a bespoke historical investigation merely to prove a negative.

When high-yield candidate discovery converges, stop the screen and research only the positive candidate population in bounded source-authority tranches.
