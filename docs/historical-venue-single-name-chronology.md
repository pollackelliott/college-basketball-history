# Historical venue single-name candidate chronology research

Status: **IN PROGRESS — 4 / 14 CANDIDATES RESEARCHED**  
Source screen: `docs/historical-venue-single-name-screen.md`  
Protected-main research baseline: `3f9edc3de0237fde453a87000cf6755b97962687`

## Purpose

This document owns bounded authoritative chronology research for the 14 positive candidates produced by the completed light single-name venue screen.

A screen-positive row is not implementation authority. This phase establishes same-building formal-name chronology and exact transition dates where authoritative evidence supports them. It does not mutate `data/reference/venues.csv`, `data/reference/venue-names.csv`, school venue rows, canonical games, or generated site data.

Exact dates are never inferred from year-only evidence. Cases that turn archival remain explicitly partial rather than expanding into open-ended archaeology.

## Research tranche 1 — first four candidates by venue ID

### VEN-000015 — AT&T Stadium — Arlington, Texas

**Disposition: `PERIODIZE_READY`**

Same physical stadium.

| Inclusive official period | Name | Basis |
|---|---|---|
| 2009-05-13 through 2013-07-24 | Cowboys Stadium | Dallas Cowboys announced the new stadium's official name on 2009-05-13. |
| 2013-07-25 onward | AT&T Stadium | Dallas Cowboys announced the AT&T naming-rights agreement on 2013-07-25 and stated that the name change was effective immediately. |

Authoritative sources:
- https://www.dallascowboys.com/news/new-stadium-finally-gets-official-name-293021
- https://www.dallascowboys.com/news/at-t-takes-naming-rights-of-stadium-now-at-t-stadium-339351

Notes:
- The stadium opened to the public later in May 2009. Using the exact official-name announcement date as `valid_from` is safe and does not create a false operational predecessor period.
- No other formal operational name surfaced in the bounded authoritative pass.

### VEN-000089 — Indiana Farmers Coliseum / Corteva Coliseum — Indianapolis, Indiana

**Disposition: `PARTIAL_PERIODIZE_RESEARCH`**

Same physical 1939 Coliseum building. Indiana State Fair authority confirms physical continuity through the 2012-2014 renovation; the exterior remained the same historic building and the renovated Coliseum reopened on 2014-04-24.

Exact recent naming periods are established:

| Inclusive official period | Name | Basis |
|---|---|---|
| 2014-04-24 through 2014-12-01 | Fairgrounds Coliseum | Indiana State Fair reopening release uses Fairgrounds Coliseum on the exact reopening date. |
| 2014-12-02 through 2024-11-12 | Indiana Farmers Coliseum | Indiana State Fair naming-rights release dated 2014-12-02 states the name change is effective immediately. |
| 2024-11-13 onward | Corteva Coliseum | Indiana State Fair release states that beginning 2024-11-13 the building is named Corteva Coliseum and that the agreement replaces Indiana Farmers Coliseum. |

Authoritative sources:
- https://www.indianastatefair.com/p/corteva-coliseum1/coliseum-history
- https://cdn.saffire.com/files.ashx?f=Coliseum_Project_Fact_Sheet.pdf&rid=IndianaStateFair&t=fg
- https://cdn.saffire.com/files.ashx?f=Coliseum_Reopens_HC.pdf&rid=IndianaStateFair&t=fg
- https://cdn.saffire.com/files.ashx?f=Indiana_Farmers_Coliseum.pdf&rid=IndianaStateFair&t=fg
- https://cdn.saffire.com/files.ashx?f=Corteva_Name_Change_News_Release_-_FINAL.pdf&rid=IndianaStateFair&t=fg

Older chronology is supported but not exact-date ready:
- Indiana State Fairgrounds Coliseum was the original 1939 building identity.
- Pepsi Coliseum was an official naming-rights era by the early 1990s and remained in use through 2012.
- Indiana government records independently use `Pepsi Coliseum` before the renovation.
- Contemporary Indianapolis Business Journal reporting places Pepsi's naming-rights acquisition in 1991 and termination in 2012, but the bounded pass did not establish exact effective days from Indiana State Fair/state archival authority.

Discovery/supporting sources for the unresolved older boundary:
- https://www.ibj.com/articles/34800-pepsi-dropping-its-name-from-indiana-fairgrounds-arena
- https://www.in.gov/ig/files/2011-06-0215.ISFC_Use_of_State_Property_2_WEB.pdf
- https://www.in.gov/sba/files/ABR_2013-2015_878_ISFB_Agency_Overview.pdf

**Residual:** exact Pepsi start and end days remain pending. Do not invent them. The exact 2014+ periods above are settled.

### VEN-000135 — Michelob ULTRA Arena — Las Vegas, Nevada

**Disposition: `PERIODIZE_READY`**

Same physical arena.

| Inclusive official period | Name | Basis |
|---|---|---|
| 1999-04-10 through 2021-02-10 | Mandalay Bay Events Center | Venue ticketing/arena history identifies the building as opening on 1999-04-10 under this name. |
| 2021-02-11 onward | Michelob ULTRA Arena | Mandalay Bay's 2021-02-11 naming-rights announcement states that Mandalay Bay Events Center is renamed Michelob ULTRA Arena. |

Sources:
- https://www.prnewswire.com/news-releases/mandalay-bay-and-anheuser-busch-announce-multi-year-naming-rights-partnership-for-sports-and-entertainment-venue-301226924.html
- https://www.axs.com/venues/101088/michelob-ultra-arena-at-mandalay-bay-resort-casino-las-vegas-tickets

Notes:
- The naming-rights announcement was issued by Mandalay Bay and negotiated by MGM Resorts International.
- No additional formal operational naming era surfaced in the bounded pass.

### VEN-000228 — Wells Fargo Arena / Casey's Center — Des Moines, Iowa

**Disposition: `PERIODIZE_READY`**

Same physical arena.

| Inclusive official period | Name | Basis |
|---|---|---|
| 2005-07-12 through 2025-06-30 | Wells Fargo Arena | Iowa Events Center states the arena officially opened on 2005-07-12 as Wells Fargo Arena. |
| 2025-07-01 onward | Casey's Center | Iowa Events Center explicitly states that Wells Fargo Arena was renamed Casey's Center on 2025-07-01. |

Authoritative sources:
- https://www.iowaeventscenter.com/about
- https://www.iowaeventscenter.com/
- https://www.iowaeventscenter.com/caseys-center/ticket-information

## Tranche 1 result

- Candidates researched: **4**
- `PERIODIZE_READY`: **3**
- `PARTIAL_PERIODIZE_RESEARCH`: **1**
- New identity conflicts: **0**
- Shared-reference mutations performed: **0**
- Remaining candidate population: **10**

Remaining candidates:
- `VEN-000244`
- `VEN-000450`
- `VEN-000596`
- `VEN-000607`
- `VEN-000641`
- `VEN-000642`
- `VEN-000675`
- `VEN-000686`
- `VEN-000698`
- `VEN-000714`

## Stopping rule

Stop after each bounded chronology tranche. Do not begin implementation or shared-reference mutation from this document alone. A later maintenance rollout must rebase against then-current protected main, preserve one physical building per `venue_id`, and use only exact authoritative naming-period boundaries.
