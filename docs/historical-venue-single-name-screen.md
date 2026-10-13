# Historical venue single-name high-yield screen

Status: **COMPLETE — LIGHT HIGH-YIELD SCREEN CONVERGED**  
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

### Efficiency reset after tranche 2

The screen is now **risk-ranked before any external research**. The remaining single-name population is mechanically evaluated with a conservative exact-token sponsor/brand heuristic using only registry display names. Generic facility words such as `Arena`, `Center`, `Coliseum`, and `Fieldhouse` do not create a hit by themselves.

The first high-risk tier recognizes explicit naming-rights signals such as financial institutions, telecom/airline brands, auto brands, and other known sponsor tokens. Matching is token-aware rather than substring-based: for example, `Rockford` must not trigger `Ford`, `Sanford` must not trigger `Ford`, and `Las Vegas` must not trigger `gas`.

This classifier is a **work-ranking device, not a historical conclusion**. A venue that does not trigger the current tier remains unscreened rather than being marked clear. The purpose is to exhaust the highest-yield population first, measure candidate yield, and only then decide whether a broader second-risk tier is justified. Individual historical research of all 483 single-name venues is not required for completion of this light screen.

At the tranche-3 baseline, the exact-token high-risk tier found **8 of the 466 then-unscreened venues**. Those eight, and only those eight, were externally checked in tranche 3.

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

## Tranche 3 — mechanically ranked explicit sponsor/brand tier

This tranche exhausts the first conservative registry-local risk tier. External checking was limited to the binary screen question: **did this same physical venue obviously operate under another formal name, or did it open under the current name?** No exact transition-date research or full chronology archaeology was performed.

| Venue | Baseline single name | Screen result | Discovery basis / next step |
|---|---|---|---|
| `VEN-000015` | AT&T Stadium | `SCREEN_POSITIVE` | Dallas Cowboys authority confirms the building opened in 2009 as Cowboys Stadium and was renamed AT&T Stadium in 2013. This is an obvious omitted predecessor era; later chronology work can verify exact implementation boundaries. Source: https://www.dallascowboys.com/news/at-t-takes-naming-rights-of-stadium-now-at-t-stadium-339351 |
| `VEN-000066` | Ford Field | `SCREEN_CLEAR_CURRENT_PASS` | Ford Field's own history identifies the 2002 opening and inaugural events under the Ford Field name. No prior operational venue-name era surfaced in this light pass. Source: https://www.fordfield.com/stadium-info/about-ford-field |
| `VEN-000104` | KFC Yum! Center | `SCREEN_CLEAR_CURRENT_PASS` | The venue and Louisville Arena Authority identify the building as opening in 2010 as KFC Yum! Center. No prior operational venue-name era surfaced. Sources: https://www.kfcyumcenter.com/about ; https://www.kfcyumcenter.com/about/louisville-arena-authority |
| `VEN-000148` | Nationwide Arena | `SCREEN_CLEAR_CURRENT_PASS` | Nationwide Arena's own history says naming-rights partner Nationwide supported the project and the arena opened in September 2000 under the current name. No predecessor operational name surfaced. Source: https://www.nationwidearena.com/history |
| `VEN-000201` | T-Mobile Arena | `SCREEN_CLEAR_CURRENT_PASS` | The arena's own material identifies its April 2016 opening as T-Mobile Arena. No predecessor operational name surfaced. Sources: https://www.t-mobilearena.com/arena-information ; https://www.t-mobilearena.com/news/detail/t-mobile-arena-debuts-on-the-las-vegas-strip |
| `VEN-000213` | Toyota Center | `SCREEN_CLEAR_CURRENT_PASS` | Houston Toyota Center states that it opened in October 2003 as Toyota Center. No predecessor operational name surfaced in this light pass. Source: https://www.toyotacenter.com/arena-info/about-us |
| `VEN-000450` | Mercedes-Benz Arena | `SCREEN_POSITIVE` | The Shanghai arena's own 2026 press center states that the building was originally built as the Shanghai World Expo Cultural Center in 2010; current arena material confirms the Mercedes-Benz naming-rights identity. This is an obvious predecessor-name candidate; later research should establish formal boundary semantics. Sources: https://www.mercedes-benzarena.com/en/News?page=1 ; https://www.mercedes-benzarena.com/en/newsinfo/270 |
| `VEN-000641` | Toyota Center | `SCREEN_POSITIVE` | Kennewick Toyota Center's own history gives the same-building sequence beginning as Tri-Cities Coliseum in 1988, later Three Rivers Coliseum, with Toyota naming rights completed in 2005. This is a clear multi-era candidate. Source: https://yourtoyotacenter.com/venue-info/history/ |

### Tranche 3 count

- Screened: **8**
- `SCREEN_POSITIVE`: **3**
- `SCREEN_CLEAR_CURRENT_PASS`: **5**
- Deep chronology research performed: **0**
- Conservative explicit sponsor/brand tier remaining: **0**

### Cumulative light-screen count after tranche 3

- Screened: **25 / 483**
- `SCREEN_POSITIVE`: **14**
- `SCREEN_CLEAR_CURRENT_PASS`: **11**
- Not individually screened: **458**
- Deep chronology research performed: **0**

The 458 not-yet-individually-screened venues are **not a requirement for 458 separate searches**. The next bounded unit, if authorized, should mechanically define a broader medium-risk tier and inspect only that population. If candidate yield converges downward, the light screen should stop rather than descend into venue-by-venue negative-proof research.


## Tranche 4 — expanded exact commercial-brand tier, slice A

The broader mechanical pass deliberately avoids the 148-name overcapture produced by generic short-name/eponym heuristics. Instead it uses an expanded **exact commercial-brand lexicon** against the remaining single-name registry rows. This produced **13 medium-risk venues**. Tranche 4 is the deterministic first slice: the first eight by `venue_id`.

The screen question remains binary: did the same building obviously operate under another formal name, or did the current name exist before/opening? No full chronology research or date-boundary verification was performed.

| Venue | Baseline single name | Screen result | Discovery basis / next step |
|---|---|---|---|
| `VEN-000024` | BOK Center | `SCREEN_CLEAR_CURRENT_PASS` | Contemporary 2005 reporting says the still-future Tulsa arena would be called BOK Center after Bank of Oklahoma bought naming rights; the venue opened in 2008. No prior operational name surfaced. Sources: https://membership.ibat.org/web/BankersDigest/Archive/2005/BD_2005_1121.pdf ; https://www.bokcenter.com/about |
| `VEN-000042` | Chase Center | `SCREEN_CLEAR_CURRENT_PASS` | Chase Center's own press kit states the arena opened in September 2019 as Chase Center. No prior operational name surfaced. Source: https://www.chasecenter.com/press-kit/ |
| `VEN-000045` | Cintas Center | `SCREEN_CLEAR_CURRENT_PASS` | Xavier states the building was dedicated/opened in 2000 and named for Cintas Corporation. No predecessor operational name surfaced. Sources: https://www.xavier.edu/mission-identity/xaviers-mission/archived/buildings-statues-and-beauty/cintas-center ; https://www.cintascenter.com/about/ |
| `VEN-000057` | Dickies Arena | `SCREEN_CLEAR_CURRENT_PASS` | The arena announced the Dickies naming-rights deal in April 2017 for the new building, which was then scheduled to open in November 2019. The sponsor name predates operation. Source: https://dickiesarena.com/multipurpose-arena-fort-worth-and-dickies-announce-naming-rights-deal-for-new-fort-worth-arena/ |
| `VEN-000063` | Fiserv Forum | `SCREEN_CLEAR_CURRENT_PASS` | Fiserv Forum identifies Fiserv as the exclusive naming-rights partner, and its fact sheet states the new arena opened on 2018-08-26. No predecessor operational name surfaced. Sources: https://www.fiservforum.com/about/naming-rights-and-founding-partners ; https://www.fiservforum.com/assets/doc/Fiserv-Forum_FactSheet_8.5x11-7075c776c1.pdf |
| `VEN-000074` | Golden 1 Center | `SCREEN_CLEAR_CURRENT_PASS` | Golden 1 Center's own 10-year history identifies the arena opening under that name in 2016. No predecessor operational name surfaced. Source: https://www.golden1center.com/news/detail/golden-1-center-celebrates-10-years-as-the-center-of-it-all/ |
| `VEN-000113` | Little Caesars Arena | `SCREEN_CLEAR_CURRENT_PASS` | The new Detroit arena was publicly named Little Caesars Arena in April 2016 before opening for the 2017-18 season; sponsor history likewise describes the new building under that name. No predecessor operational name surfaced. Sources: https://www.nhl.com/news/red-wings-new-building-named-little-caesars-arena-280502882 ; https://littlecaesars.com/en-us/about-us/hometown-pride/ |
| `VEN-000120` | Lucas Oil Stadium | `SCREEN_CLEAR_CURRENT_PASS` | Lucas Oil Stadium's own history states Lucas Oil Products secured naming rights in 2006 and the stadium opened to the public in August 2008. The current name predates operation. Source: https://www.lucasoilstadium.com/tours-stadium-info/background-history/ |

### Tranche 4 count

- Screened: **8**
- `SCREEN_POSITIVE`: **0**
- `SCREEN_CLEAR_CURRENT_PASS`: **8**
- Deep chronology research performed: **0**
- Expanded exact commercial-brand tier: **13 total**
- Expanded exact commercial-brand tier remaining after this tranche: **5**

### Cumulative light-screen count after tranche 4

- Screened: **33 / 483**
- `SCREEN_POSITIVE`: **14**
- `SCREEN_CLEAR_CURRENT_PASS`: **19**
- Not individually screened: **450**
- Deep chronology research performed: **0**

The zero-positive result in this tranche is a material convergence signal. It does not prove the remaining population has no omitted renames, but it argues against broadening into generic eponym/short-name searching. The five remaining members of this exact commercial-brand tier may be checked as one later bounded slice; after that, continuation of the overall screen should require a demonstrably higher-yield mechanical signal rather than individual negative-proof research.


## Tranche 5 — expanded exact commercial-brand tier, slice B / convergence closeout

This tranche exhausts the final five members of the 13-venue expanded exact commercial-brand tier. The same binary screen question applies: did the same building obviously operate under another formal name, or was the current name established before/at opening? No full chronology research or exact date-boundary verification was performed.

| Venue | Baseline single name | Screen result | Discovery basis / next step |
|---|---|---|---|
| `VEN-000231` | Wintrust Arena | `SCREEN_CLEAR_CURRENT_PASS` | DePaul announced the Wintrust Arena naming-rights agreement on 2016-11-16 while the new arena was still under construction for a fall 2017 opening. The sponsor name predates operation. Sources: https://depaulbluedemons.com/news/2016/11/16/Event_Center_at_McCormick_Square_to_be_named_Wintrust_Arena ; https://www.wintrustarena.com/about/history |
| `VEN-000242` | Acrisure Arena | `SCREEN_CLEAR_CURRENT_PASS` | Acrisure/Oak View Group announced the arena naming-rights agreement on 2022-01-26; the arena opened on 2022-12-14. The current name predates operation. Sources: https://acrisurearena.com/tag/acrisure-arena/page/11/ ; https://www.acrisurearena.com/about |
| `VEN-000260` | Target Center | `SCREEN_CLEAR_CURRENT_PASS` | Target Center states that it opened in October 1990 and that Target has been the naming-rights partner since opening. No predecessor operational name surfaced. Source: https://www.targetcenter.com/target-center_info/about-target-center |
| `VEN-000304` | GIANT Center | `SCREEN_CLEAR_CURRENT_PASS` | GIANT Center states that Giant Food Stores has been title sponsor since 2000; the venue's first announced act was in 2002 and the Hershey Bears moved there in 2002. The sponsor name predates operation. Sources: https://www.hersheyentertainment.com/giant-center/info/ ; https://www.hersheyentertainment.com/giant-center/hershey-bears.php |
| `VEN-000397` | Kaiser Permanente Arena | `SCREEN_CLEAR_CURRENT_PASS` | Santa Cruz Warriors institutional history identifies the September 2012 approval and construction of Kaiser Permanente Arena before the team's first home game there on 2012-12-23. No predecessor operational name surfaced. Sources: https://cdn.warriors.com/pdf/SCW_1516_MediaGuide.pdf ; https://ecm.cityofsantacruz.com/OnBaseAgendaOnline/Documents/ViewDocument/Summary%20Sheet%20for%20-%20Amendments%20to%20extend%20the%20term%20of%20the%20Ground%20Lease%2C%20T.pdf?documentType=Agenda&isSection=false&itemId=33457&meetingId=2153&publishId=50150 |

### Tranche 5 count

- Screened: **5**
- `SCREEN_POSITIVE`: **0**
- `SCREEN_CLEAR_CURRENT_PASS`: **5**
- Deep chronology research performed: **0**
- Expanded exact commercial-brand tier remaining: **0**

### Final light-screen count

- Individually screened through high-yield tiers: **38 / 483**
- `SCREEN_POSITIVE`: **14**
- `SCREEN_CLEAR_CURRENT_PASS`: **24**
- Low-signal venues not individually searched: **445**
- Deep chronology research performed: **0**

### Convergence decision

The high-yield screen is **COMPLETE**.

The screen intentionally does not require 483 individual historical searches. Its purpose was to discover obvious omitted formal naming histories efficiently.

Observed yield by the risk-ranked phase:

- Conservative explicit sponsor/brand tier: **3 positives / 8 screened**
- Expanded exact commercial-brand tier: **0 positives / 13 screened**

The broader tier therefore produced **zero additional candidates across all 13 venues**. Combined with the completed repository-internal cross-check (0 alternate-name hits across all 483 single-name IDs), this is sufficient convergence for the agreed light screen.

The remaining **445 low-signal single-name venues are closed as unscreened-by-design for this program**, not asserted to have no historical renames. Do not perform individual negative-proof research on them absent a new material signal.

Any later discovery of materially stronger evidence may create a bounded new candidate, but that does not reopen this completed screen wholesale.


## Current candidate queue

The following single-name venues now warrant later bounded chronology research:

- `VEN-000015`
- `VEN-000089`
- `VEN-000135`
- `VEN-000228`
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

Do not periodize or mutate shared registries from this screen alone.

Chronology follow-up is tracked separately in `docs/historical-venue-single-name-chronology.md`. Tranches 1-2 have researched 8 of the 14 screen-positive candidates; 6 remain pending there.

## Stopping rule

**Satisfied.** High-yield candidate discovery has converged. The screen is closed at 14 positive candidates. Research only that positive candidate population in later bounded source-authority tranches; do not descend into individual negative-proof research for the 445 low-signal venues.
