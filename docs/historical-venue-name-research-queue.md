# Historical venue-name research queue

Status: **READY FOR DIVIDE-AND-CONQUER RESEARCH**  
Source census: `docs/historical-venue-name-census.md`  
Protected-main census baseline: `3f9edc3de0237fde453a87000cf6755b97962687`

This queue is mechanically derived from every census row with disposition `RESEARCH_HOLD`, `PERIODIZE_RESEARCH`, `IDENTITY_RECONCILE`, or `CANONICAL_CORRECTION`.

There were **70 research-needed ledger rows representing 69 work items** at queue creation. After assistant research tranche 1, **66 rows representing 65 active research work items remain**. `VEN-000102` and `VEN-000315` are one linked Seattle Center physical-identity work item.

The split is organizational, not historical authority. The owner may reassign any item. No result becomes authoritative merely because one side researched it; findings must be written back to the durable census/research ledger with authoritative evidence and, where needed, explicit owner adjudication.

## Research split rules

- **OWNER_HIGH_PROFILE**: recognizable/high-profile facilities where owner historical knowledge can quickly identify the likely chronology or framing. Owner may supply the working answer/source lead; Control Center verifies authoritative sourcing before implementation.
- **ASSISTANT_SOURCE_HEAVY**: obscure/local/complex-vs-arena/spelling or institutional-history cases suited to bounded source research.
- **CONTROL_CENTER_MECHANICAL**: obvious canonical/duplicate/source-text cleanup that should be verified mechanically rather than consume owner historical attention.
- Do not research all items in one open-ended sweep. Work in bounded tranches and checkpoint results after each tranche.
- The **116 already owner-approved `PERIODIZE` venues are not in this ambiguity queue**. Their exact effective dates still require authoritative verification before implementation, but their conceptual naming treatment is already settled.
- After this ambiguity queue closes, perform the agreed light high-yield screen of the 483 single-name venues before sizing implementation tranches.

## Owner high-profile queue

| Venue | Disposition | Research question |
|---|---|---|
| `VEN-000013` | `RESEARCH_HOLD` | Research full Sacramento chronology. ARCO Arena II is building disambiguation, not a period. Working expectation includes ARCO Arena → Power Balance Pavilion → Sleep Train Arena. |
| `VEN-000019` | `RESEARCH_HOLD` | Baltimore registry is incomplete; research full formal chronology before owner periodization. |
| `VEN-000023` | `RESEARCH_HOLD` | Determine whether NU Sports Complex was a genuine predecessor name of Bob Devaney Sports Center or source shorthand. |
| `VEN-000038` | `RESEARCH_HOLD` | Research full UCF chronology; working expectation UCF Arena → CFE Arena → Addition Financial Arena. |
| `VEN-000076` | `RESEARCH_HOLD` | Research whether Greensboro Memorial Coliseum was an earlier formal name and reconcile Greensboro Coliseum / First Horizon Coliseum chronology. |
| `VEN-000095` | `PERIODIZE_RESEARCH` | Multiple Rutgers formal periods; research exact Rutgers Athletic Center / Louis Brown Athletic Center / any RAC reversion / Jersey Mike’s Arena chronology. |
| `VEN-000109` | `RESEARCH_HOLD` | Distinguish true arena names from BJCC complex/source shorthand before owner periodization. |
| `VEN-000176` | `RESEARCH_HOLD` | Research Cincinnati formal sequence and determine status of The Crown before owner ruling. |
| `VEN-000204` | `PERIODIZE_RESEARCH` | Trans World Dome → Edward Jones Dome → The Dome at America’s Center; current registry omits Trans World Dome. |
| `VEN-000524` | `RESEARCH_HOLD` | Research exact WVU Field House / Stansbury Hall chronology and whether Mountaineer Field House is alias only. Owner supplied working fact: opened 1929 as WVU Field House; basketball moved to WVU Coliseum in 1970. |
| `VEN-000828` | `RESEARCH_HOLD` | Research relationship among The Cage, The Hangar/Hanger, Basketball Hangar, and Quonset Hut before owner ruling. |
| `VEN-000829` | `PERIODIZE_RESEARCH` | Field House family → Hugh S. Greer Field House; verify the exact formal first-era name among UConn Field House / Storrs Field House. |
| `VEN-000040` | `RESEARCH_HOLD` | Research full formal chronology of the 1955 Charlotte Coliseum building, including Independence Arena / Bojangles Coliseum and any omitted eras, before periodization. |
| `VEN-000102` | `IDENTITY_RECONCILE` | Owner ruling: KeyArena lineage and VEN-000315 Climate Pledge Arena are one physical Seattle Center arena identity. Later shared-reference implementation must reconcile to one surviving global venue_id and research complete naming chronology. |
| `VEN-000315` | `IDENTITY_RECONCILE` | Owner ruling: Climate Pledge Arena and VEN-000102 KeyArena lineage are one physical Seattle Center arena identity. Later shared-reference implementation must reconcile to one surviving global venue_id and research complete naming chronology. |
| `VEN-000153` | `RESEARCH_HOLD` | Research full Oakland Coliseum Arena naming chronology before periodization; current registry omits major formal eras such as Oracle Arena. |
| `VEN-000182` | `RESEARCH_HOLD` | Research San Diego Sports Arena full naming chronology and remove erroneous Cox Arena/Viejas cross-venue aliasing only after physical-identity verification. |
| `VEN-000349` | `PERIODIZE_RESEARCH` | Research full Glendale arena chronology; current registry has Gila River Arena → Desert Diamond Arena but likely omits earlier Glendale Arena / Jobing.com Arena eras. |
| `VEN-000350` | `PERIODIZE_RESEARCH` | Research Shoemaker Center → Fifth Third Arena chronology and determine whether Fifth Third Arena at Shoemaker Center is retained-building wording rather than another era. |
| `VEN-000433` | `RESEARCH_HOLD` | Research Boardwalk Hall / Atlantic City Convention Hall chronology and distinguish the historic hall from the separate modern Atlantic City Convention Center before periodization. |
| `VEN-000499` | `PERIODIZE_RESEARCH` | Research full Miami arena chronology: AmericanAirlines Arena → FTX Arena → interim Miami-Dade naming → Kaseya Center; current registry omits formal eras. |
| `VEN-000563` | `PERIODIZE_RESEARCH` | Research Philadelphia Convention Hall / Municipal Auditorium / Philadelphia Civic Center chronology and exact period boundaries. |
| `VEN-000618` | `RESEARCH_HOLD` | Resolve Tucson Community Center Arena / Tucson Convention Center Arena / Tucson Arena and distinguish arena naming from surrounding-complex naming. |
| `VEN-000749` | `RESEARCH_HOLD` | Research Philadelphia Auditorium / Philadelphia Arena full chronology; current registry may omit earlier formal wording. |
| `VEN-000753` | `RESEARCH_HOLD` | Clarify Manley Field House / John A. Lally Athletics Complex relationship: true rename, larger-complex designation, or materially reconfigured facility. |
| `VEN-000754` | `RESEARCH_HOLD` | Research Old Gym / Gymnasium and YMCA Building / Women’s Gymnasium chronology; may reflect genuine successive institutional uses/names. |
| `VEN-000757` | `PERIODIZE_RESEARCH` | Research exact Onondaga County War Memorial → Oncenter War Memorial → Upstate Medical University Arena naming chronology. |
| `VEN-000860` | `PERIODIZE_RESEARCH` | Villanova Field House → Jake Nevin Field House; owner approves two periods, exact rename boundary to verify. |
| `VEN-000863` | `RESEARCH_HOLD` | Research A.J. Palumbo Center lineage into UPMC Cooper Fieldhouse; verify same-building continuity and full chronology before periodization. |


## Completed assistant research — tranche 1

| Venue | Result | Durable evidence / residual |
|---|---|---|
| `VEN-000185` | `PERIODIZE` | Alltel Arena → Verizon Arena → Simmons Bank Arena. Official arena history confirms the 1999 Alltel opening; Arkansas reference history confirms the three-era sequence; North Little Rock's 2019 announcement fixes the Simmons transition to 2019-10-03. Working 2009 Verizon boundary is 2009-07-01; recheck exact first-period opening date during implementation-date verification. Sources: https://www.simmonsbankarena.com/about-the-arena/ ; https://encyclopediaofarkansas.net/entries/Simmons-Bank-Arena-8326/ ; https://northlittlerock.org/simmons-bank-to-assume-naming-rights-to-verizon-arena-oct-3/ |
| `VEN-000146` | `PERIODIZE` | Myriad Convention Center → Cox Business Services Convention Center → Prairie Surf Studios. City of Oklahoma City confirms the formal sequence; contemporaneous reporting records council approval of the Cox naming deal on 2002-02-05; the studio lease began 2021-01-01. Exact naming-boundary semantics remain implementation-date verification. Sources: https://www.okc.gov/News-articles/Traffic-Advisory-New-arena-utility-work-to-affect-N-Broadway-Avenue ; https://journalrecord.com/2002/02/06/the-myriad-no-longer/ ; https://www.paycomcenter.com/interact-with-us/prairie-surf-studios |
| `VEN-000160` | `CANONICAL_CORRECTION` | Correct spelling is Patten Gymnasium. VEN-000160 is the original 1909 building that hosted the 1939 NCAA title game and was razed in 1940; Northwestern built a distinct replacement Patten Gymnasium in 1940. `Patton Gymnasium` is erroneous; never merge the two physical buildings. Sources: https://www.northwestern.edu/magazine/fall2012/feature/whats-in-a-name-sidebar/patten-gymnasium.html ; https://maps.northwestern.edu/txt/facility/154 |
| `VEN-000250` | `PERIODIZE` | Mississippi State Gymnasium → McCarthy Gymnasium. `New Gym` is shorthand, not a separate formal period. Mississippi State Athletics states the building was initially called Mississippi State Gymnasium and was renamed for Babe McCarthy after his death in 1975. Exact 1975 rename day remains implementation-date verification. Source: https://hailstate.com/news/2022/9/26/womens-basketball-basketball-set-to-host-annual-maroon-madness-event-but-with-a-twist |
| `VEN-000234` | remains `RESEARCH_HOLD` | Bounded research did not establish a reliable exact boundary/formal status for Worcester’s Centrum Centre, nor an exact effective day for DCU naming. Official DCU evidence confirms an October 2004 naming-rights partnership. Stop here until a stronger city/venue archival source resolves the residual. Source: https://www.dcucenter.com/venue-info/dcu-digital-federal-credit-union/ |

## Assistant source-heavy queue

| Venue | Disposition | Research question |
|---|---|---|
| `VEN-000234` | `RESEARCH_HOLD` | Tranche 1 residual only: opening identity is supported as Centrum in Worcester; later sources use Worcester’s Centrum Centre; DCU naming-rights agreement was reached in October 2004. Resolve exact formal status/adoption boundary of Worcester’s Centrum Centre and exact DCU effective day without inventing dates. |
| `VEN-000271` | `RESEARCH_HOLD` | Determine whether The Arena at Northwest Florida State College → Raider Arena was a true formal rename or alternate branding. |
| `VEN-000296` | `RESEARCH_HOLD` | Determine whether Kansas Coliseum is the overall complex and Britt Brown Arena the basketball arena inside it rather than a historical rename. |
| `VEN-000308` | `RESEARCH_HOLD` | Determine whether Recreation Building → Recreation Hall / Rec Hall represents a true formal rename or interchangeable wording. |
| `VEN-000316` | `RESEARCH_HOLD` | Research full Hershey Park Arena / Hershey Arena naming chronology before periodization; current registry may omit a genuine earlier formal arena name. |
| `VEN-000344` | `RESEARCH_HOLD` | Determine whether Frank McGuire Arena is a competition-space/court name or erroneous cross-venue alias rather than a Carolina Coliseum rename. |
| `VEN-000346` | `RESEARCH_HOLD` | Research Carolina Gymnasium / Longstreet Theater chronology and later reuse before deciding whether post-basketball naming belongs in the period model. |
| `VEN-000353` | `RESEARCH_HOLD` | Distinguish Harrah’s Cherokee Center complex naming from ExploreAsheville.com Arena interior-arena naming before periodization. |
| `VEN-000382` | `RESEARCH_HOLD` | Verify whether Nielsen Field House is the same physical building as George Albert Smith Field House / Smith Fieldhouse before any naming-period treatment. |
| `VEN-000388` | `RESEARCH_HOLD` | Determine whether Baoshan Sports Center is the overall complex and Baoshan Arena the specific arena before treating as naming history. |
| `VEN-000396` | `RESEARCH_HOLD` | Research Public School Fieldhouse → Jeppesen Fieldhouse/Gymnasium chronology; may represent a true formal rename. |
| `VEN-000439` | `RESEARCH_HOLD` | Determine physical/name relationship between Highland Park Gym and Highland Park Masonic Hall before periodization. |
| `VEN-000453` | `PERIODIZE_RESEARCH` | Municipal Auditorium → Civic Center Music Hall, subject to same-building chronology verification. |
| `VEN-000454` | `PERIODIZE_RESEARCH` | Research Tulsa Convention Center → Cox Business Center → Arvest Convention Center chronology and determine whether Cox Business Convention Center was a separate formal name or variant. |
| `VEN-000474` | `RESEARCH_HOLD` | Determine whether CU Fieldhouse → Balch Fieldhouse was a true formal rename and establish chronology. |
| `VEN-000475` | `RESEARCH_HOLD` | Determine whether Men’s Gymnasium → Carlson Gymnasium was a true rename and establish chronology. |
| `VEN-000503` | `PERIODIZE_RESEARCH` | McGrath Arena → McGrath-Phillips Arena, subject to formal rename-date verification. |
| `VEN-000505` | `PERIODIZE_RESEARCH` | Research Rochester War Memorial lineage → Blue Cross Arena and determine whether Rochester Community War Memorial and Blue Cross/Blue Shield Arena were distinct formal eras or variants. |
| `VEN-000509` | `PERIODIZE_RESEARCH` | Research full Quad Cities arena chronology from The MARK of the Quad Cities through omitted sponsored eras to Vibrant Arena at The MARK. |
| `VEN-000513` | `RESEARCH_HOLD` | Determine whether Alumni Memorial Gymnasium → Brodie Gym was an actual formal rename of the same physical building. |
| `VEN-000521` | `RESEARCH_HOLD` | Research Raleigh Auditorium / Municipal Auditorium / Old City Auditorium / City Hall and Auditorium same-building and naming-history relationship before periodization. |
| `VEN-000554` | `RESEARCH_HOLD` | Research Rice Field House / Rice Gymnasium / Autry Court chronology; may represent genuine formal naming eras. |
| `VEN-000555` | `PERIODIZE_RESEARCH` | Research full Bossier City arena chronology; CenturyTel Center → likely omitted CenturyLink era → Brookshire Grocery Arena. |
| `VEN-000557` | `RESEARCH_HOLD` | Research Comerica Center full chronology; Comerica Arena may be erroneous variant and earlier formal naming history may be omitted. |
| `VEN-000578` | `PERIODIZE_RESEARCH` | Research full Estero arena chronology; Germain Arena → Hertz Arena is real but current registry likely omits an earlier formal arena name. |
| `VEN-000674` | `RESEARCH_HOLD` | Determine whether UC Fieldhouse → Armory Fieldhouse was a genuine formal rename. |
| `VEN-000711` | `RESEARCH_HOLD` | Clarify Murray State Sports Arena / Racer Arena / Carlisle Cutchin Fieldhouse and arena-within-fieldhouse relationship. |
| `VEN-000729` | `PERIODIZE_RESEARCH` | Research full Gwinnett arena chronology from Arena at Gwinnett through omitted sponsored era(s) to Gas South Arena. |
| `VEN-000778` | `PERIODIZE_RESEARCH` | Research full Portland, Maine arena chronology from Cumberland County Civic Center through later Cross Insurance Arena era; Portland Civic Center appears shorthand and registry is incomplete. |
| `VEN-000781` | `PERIODIZE_RESEARCH` | Research full Bridgeport arena chronology: Arena at Harbor Yard → Webster Bank Arena → omitted later/current naming era(s). |
| `VEN-000788` | `RESEARCH_HOLD` | Determine whether College Park Gym was an actual predecessor name of Spencer Memorial Gymnasium or a source/location conflation. |
| `VEN-000815` | `PERIODIZE_RESEARCH` | Research Creighton University Gym/Old Gymnasium → Vinardi Center chronology and determine whether Vinardi Athletic Center is another formal era or expanded form. |
| `VEN-000823` | `PERIODIZE_RESEARCH` | Research RPI Field House → Houston Field House chronology and verify formal rename boundary. |


## Control Center mechanical/canonical verification

| Venue | Disposition | Research question |
|---|---|---|
| `VEN-000324` | `CANONICAL_CORRECTION` | One physical Richmond venue; proper canonical name is Robins Center. Robbins Center is erroneous variant, not a naming period. |
| `VEN-000371` | `CANONICAL_CORRECTION` | One Guerra Sports Complex identity; verify authoritative first name spelling, Eugenio vs Eugene, rather than creating naming periods. |
| `VEN-000585` | `CANONICAL_CORRECTION` | State Fair Arena is the physical venue; State Farm Arena [BC source wording] is erroneous source wording, not a historical period. |
| `VEN-000683` | `CANONICAL_CORRECTION` | Duplicate literal Orange County Civic Center rows represent one naming identity; registry cleanup only, no periodization. |


## Completion condition

This queue closes when every row above has one of:
- a verified historical chronology and final naming-period disposition;
- a verified alias/competition-space/complex-name disposition;
- a verified physical-identity reconciliation;
- a verified canonical cleanup; or
- an explicitly documented research-exhausted residual requiring a genuine owner decision.

No shared-reference registry mutation is authorized by this queue alone.
