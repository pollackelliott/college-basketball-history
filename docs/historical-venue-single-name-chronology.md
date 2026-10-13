# Historical venue single-name candidate chronology research

Status: **IN PROGRESS — 8 / 14 CANDIDATES RESEARCHED**  
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


## Research tranche 2 — next four candidates by venue ID

### VEN-000244 — Tupelo arena lineage — Tupelo, Mississippi

**Disposition: `PARTIAL_PERIODIZE_RESEARCH`**

Same physical arena. The building opened on 1993-10-09 as Tupelo Coliseum. Later formal identities include BancorpSouth Center, BancorpSouth Arena, Cadence Bank Arena, and now Huntington Bank Arena.

Authoritative / strong local evidence:
- Community Development Foundation history gives the grand opening date as 1993-10-09 and identifies the building as Tupelo Coliseum at opening.
- City of Tupelo records establish the same facility as BancorpSouth Arena and Conference Center throughout the 2010s.
- A 2022 City of Tupelo naming-agreement amendment substitutes Cadence Bank for BancorpSouth in the arena naming agreements; local contemporaneous reporting documents the public signage conversion during September 2022.
- The arena's current official site is now branded Huntington Bank Arena. Huntington completed its Cadence acquisition in February 2026; Tupelo-area rebranding occurred during June 2026.

Sources:
- https://www.cdfms.org/cdf/cdf-history-overview/1990s
- https://www.tupeloms.gov/wp-content/uploads/2020/03/REG-CC-03.05.19.pdf
- https://mccmeetingspublic.blob.core.usgovcloudapi.net/tupeloms-meet-1b51c623032849c58fc6359c47780842/ITEM-Attachment-001-e57c2d72d1874e36af049ccf7f6d1f84.pdf
- https://www.wcbi.com/bancorpsouth-merges-with-cadence-bank-changes-signs-on-buildings/
- https://www.hbarena.com/p/about
- https://ir.huntington.com/regulatory-sec-filings/all-sec-filings/content/0001140361-26-003083/ef20064500_ex99-1.htm

**Residuals:**
- The bounded pass did not establish institutionally exact effective days for Tupelo Coliseum → BancorpSouth Center or BancorpSouth Center → BancorpSouth Arena. Secondary sources disagree on the first BancorpSouth year.
- The 2022 naming-agreement amendment was executed on 2022-07-01, while public signage conversion occurred later in 2022; the exact public/formal display boundary needs one implementation-date reconciliation.
- The current Huntington Bank Arena rebrand is definitely a June 2026 successor era, but the exact arena naming effective day was not established from a naming-rights instrument. Do not infer it from branch-conversion dates.

Historical chronology is clear; exact complete periodization is not yet ready.

### VEN-000450 — Mercedes-Benz Arena — Shanghai, China

**Disposition: `PARTIAL_PERIODIZE_RESEARCH`**

Same physical arena.

Supported chronology:
- The arena was originally built for Expo 2010 as the Shanghai World Expo Cultural Center.
- AEG states that commercial operations under the Mercedes-Benz brand commenced in 2011.
- Mercedes-Benz Arena remains the formal current name as of this research; AEG states the current naming-rights agreement runs until mid-2027.

Authoritative sources:
- https://www.mercedes-benzarena.com/en/News?page=1
- https://www.mercedes-benzarena.com/en/newsinfo/270
- https://www.aeg-international.com/press-centre/aeg-brings-rare-naming-rights-opportunity-to-market-for-shanghai-arena-2
- https://www.prnewswire.com/news-releases/mercedes-benz-extends-naming-rights-partnership-for-mercedes-benz-arena-in-shanghai-300384139.html

**Residual:** the bounded authoritative pass established the 2010 → 2011 sequence but not an exact institutional effective day in 2011. Do not use an aggregator-derived January date as final authority.

### VEN-000596 — Landers Center — Southaven, Mississippi

**Disposition: `PARTIAL_PERIODIZE_RESEARCH`**

Same physical arena / civic center.

Supported chronology:
- The facility opened in 2000 as DeSoto Civic Center.
- DeSoto County's audited financial statements explicitly state that the Convention and Visitors Bureau agreement renamed the DeSoto Civic Center the **Landers Center effective 2012-01-01**.
- Landers remains the formal name; the naming-rights agreement was renewed again in 2023.

Authoritative sources:
- https://www.desotocountyms.gov/DocumentCenter/View/9870/Audited-Financial-Statements-2024-PDF
- https://www.landerscenter.com/contact/board-of-directors

Exact settled boundary:
- DeSoto Civic Center through **2011-12-31**
- Landers Center from **2012-01-01 onward**

**Residual:** institutional evidence in the bounded pass gives the original opening year as 2000 but not the exact opening day. Therefore the full first naming period does not yet have an exact `valid_from`. Do not invent one merely to fill the early boundary.

### VEN-000607 — LionTree Arena — La Jolla / San Diego, California

**Disposition: `PARTIAL_PERIODIZE_RESEARCH`**

Same physical arena.

Supported chronology:
- UC San Diego states that RIMAC Arena opened in January 1995.
- UC San Diego announced on 2022-06-15 that RIMAC Arena **has been named LionTree Arena** in recognition of the scholarship gift.
- The naming term may run for up to seven years.

Authoritative sources:
- https://ucsdtritons.com/facilities/liontree-arena/2
- https://ucsdtritons.com/news/2022/6/15/general-rimac-arena-is-named-liontree-arena-in-honor-of-scholarship-gift.aspx
- https://today.ucsd.edu/story/rimac-arena-is-named-liontree-arena-in-honor-of-scholarship-gift

Exact settled boundary:
- RIMAC Arena through **2022-06-14**
- LionTree Arena from **2022-06-15 onward**

**Residual:** UC San Diego's current facility history gives only January 1995 for the original opening, not an exact day. The exact first `valid_from` for RIMAC Arena therefore remains pending.

## Tranche 2 result

- Candidates researched: **4**
- `PERIODIZE_READY`: **0**
- `PARTIAL_PERIODIZE_RESEARCH`: **4**
- New identity conflicts: **0**
- Shared-reference mutations performed: **0**
- Cumulative researched: **8 / 14**
- Cumulative `PERIODIZE_READY`: **3**
- Cumulative `PARTIAL_PERIODIZE_RESEARCH`: **5**
- Remaining candidate population: **6**

Remaining candidates:
- `VEN-000641`
- `VEN-000642`
- `VEN-000675`
- `VEN-000686`
- `VEN-000698`
- `VEN-000714`

## Stopping rule

Stop after each bounded chronology tranche. Do not begin implementation or shared-reference mutation from this document alone. A later maintenance rollout must rebase against then-current protected main, preserve one physical building per `venue_id`, and use only exact authoritative naming-period boundaries.
