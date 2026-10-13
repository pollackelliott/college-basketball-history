# Historical venue single-name candidate chronology research

Status: **IN PROGRESS — 12 / 14 CANDIDATES RESEARCHED**  
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


## Research tranche 3 — next four candidates by venue ID

### VEN-000641 — Toyota Center — Kennewick, Washington

**Disposition: `PARTIAL_PERIODIZE_RESEARCH`**

Same physical arena.

Supported chronology:
- The building opened in 1988 as **Tri-Cities Coliseum**.
- The official venue history states that the complex was renamed in 2004, with the Coliseum becoming **Three Rivers Coliseum**.
- In October 2005, a naming-rights sponsorship agreement between the City of Kennewick, VenuWorks, Toyota USA, and Toyota of Tri-Cities branded the Coliseum as **Toyota Center**.

Authoritative source:
- https://yourtoyotacenter.com/venue-info/history/

**Residuals:**
- The official facility history gives only the year 1988 for opening, not an exact opening day.
- It gives 2004 for the Three Rivers Coliseum transition but no exact effective day.
- It gives October 2005 for the Toyota naming-rights agreement but no exact day.

The three-era same-building chronology is settled; exact periodization boundaries are not yet implementation-ready.

### VEN-000642 — Idaho Central Arena — Boise, Idaho

**Disposition: `PARTIAL_PERIODIZE_RESEARCH`**

Same physical arena.

Supported chronology:
- The arena opened in the fall of 1997 and was originally **Bank of America Centre**.
- It later became **Qwest Arena** in 2005.
- Idaho Steelheads / Block 22 announced the change from Qwest Arena to **CenturyLink Arena Boise** on 2011-08-17.
- Idaho Steelheads / Block 22 and Idaho Central Credit Union announced on 2020-09-17 that CenturyLink Arena would now be named **Idaho Central Arena**.

Authoritative / facility sources:
- https://idahocentralarena.com/about-us/
- https://idahosteelheads.com/news/2011/08/qwest-arena-becomes-centurylink-arena-boise
- https://idahosteelheads.com/news/2020/09/centurylink-arena-home-of-the-idaho-steelheads-to-be-renamed-idaho-central-arena

Strong local corroboration:
- https://boisedev.com/news/2020/09/16/idaho-central-arena-boise/

Exact settled recent boundaries:
- Qwest Arena through **2011-08-16**
- CenturyLink Arena Boise from **2011-08-17 through 2020-09-16**
- Idaho Central Arena from **2020-09-17 onward**

**Residuals:**
- The official arena site gives only fall 1997 for opening.
- The bounded pass confirms Bank of America Centre → Qwest Arena in 2005 but did not establish an exact authoritative effective day for that transition.

Do not import third-party exact dates for the 1997 opening or 2005 rename merely to complete the early periods.

### VEN-000675 — Truist Arena — Highland Heights, Kentucky

**Disposition: `PARTIAL_PERIODIZE_RESEARCH`**

Same physical arena.

Supported chronology:
- Northern Kentucky University states that the venue opened in 2008 as **The Bank of Kentucky Center**.
- NKU Athletics announced on **2015-06-22** that the venue had a new name, **BB&T Arena at Northern Kentucky University**, after BB&T acquired The Bank of Kentucky.
- The arena was subsequently renamed **Truist Arena** in April 2022 after the BB&T/SunTrust merger and Truist rebrand.

Authoritative sources:
- https://nkunorse.com/news/2015/6/22/GEN_0622150627.aspx
- https://www.nku.edu/campus-planning/building/other/bbt/

Strong contemporaneous corroboration for the 2022 rebrand:
- https://linknky.com/sports/2022/04/05/bbt-arena-is-now-truist-arena/
- https://nkytribune.com/2022/04/nkus-on-campus-arena-undergoes-its-third-name-change-in-history-now-truist-arena/

Exact settled middle boundary:
- The Bank of Kentucky Center through **2015-06-21**
- BB&T Arena from **2015-06-22**

**Residuals:**
- NKU's campus record establishes 2008 opening/occupancy chronology but does not provide one unambiguous exact operational opening day suitable for the first naming-period `valid_from`.
- The bounded pass found contemporaneous reporting that NKU's Truist change was effective immediately in April 2022, but did not recover the underlying first-party NKU/facility release at an exact permanent URL. Preserve the April 2022 chronology without manufacturing an implementation boundary from secondary reporting alone.

### VEN-000686 — Bankoh Arena at Stan Sheriff Center — Honolulu, Hawai‘i

**Disposition: `PERIODIZE_READY`**

Same physical arena.

| Inclusive official period | Name | Basis |
|---|---|---|
| 1994-10-21 through 1998-02-19 | Special Events Arena | Multiple UH Athletics histories identify the first event/opening on 1994-10-21 under the Special Events Arena name. |
| 1998-02-20 through 2020-11-11 | Stan Sheriff Center | Current UH game notes state the arena was officially renamed for Stan Sheriff on 1998-02-20. |
| 2020-11-12 through 2025-08-25 | SimpliFi Arena at Stan Sheriff Center | UH Athletics announced the Bank of Hawai‘i naming-rights agreement and new SimpliFi name on 2020-11-12. |
| 2025-08-26 onward | Bankoh Arena at Stan Sheriff Center | UH Athletics announced on 2025-08-26 that the venue had been renamed Bankoh Arena at Stan Sheriff Center. |

Authoritative sources:
- https://hawaiiathletics.com/sports/2012/6/14/GEN_0614125128
- https://hawaiiathletics.com/news/2024/8/26/womens-volleyball-faces-smu-san-diego-to-open-2024-season.aspx
- https://hawaiiathletics.com/news/2020/11/12/general-bank-of-hawaii-sponsors-naming-rights-for-stan-sheriff-center.aspx
- https://hawaiiathletics.com/news/2025/8/26/general-bank-of-hawai-i-unveils-new-name-for-uh-facility-bankoh-arena-at-stan-sheriff-center.aspx
- 2025-26 Hawai‘i women's basketball game notes, official UH Athletics PDF: https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/hawaiiathletics.com/documents/2026/2/27/24-Cal_State_Fullerton.pdf

Opening-date reconciliation:
- One 2019 UH anniversary article contains an isolated 1994-10-20 statement.
- Multiple other UH sources, including the WAC timeline, 2004 anniversary material, 2019 match notes, and 2024 volleyball notes, identify the inaugural Special Events Arena event as **1994-10-21**.
- Treat 1994-10-21 as the supported opening/name boundary; the isolated 10/20 statement is a source inconsistency, not a reason to invent a different period.

## Tranche 3 result

- Candidates researched: **4**
- `PERIODIZE_READY`: **1**
- `PARTIAL_PERIODIZE_RESEARCH`: **3**
- New identity conflicts: **0**
- Shared-reference mutations performed: **0**
- Cumulative researched: **12 / 14**
- Cumulative `PERIODIZE_READY`: **4**
- Cumulative `PARTIAL_PERIODIZE_RESEARCH`: **8**
- Remaining candidate population: **2**

Remaining candidates:
- `VEN-000698`
- `VEN-000714`

## Stopping rule

Stop after each bounded chronology tranche. Do not begin implementation or shared-reference mutation from this document alone. A later maintenance rollout must rebase against then-current protected main, preserve one physical building per `venue_id`, and use only exact authoritative naming-period boundaries.
