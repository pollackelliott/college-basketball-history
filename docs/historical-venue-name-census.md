# Historical venue-name census

Status: **MULTI-NAME AMBIGUITY RESEARCH COMPLETE — SINGLE-NAME SCREEN IN PROGRESS**  
Protected-main baseline: `3f9edc3de0237fde453a87000cf6755b97962687`

This file preserves the owner-adjudicated state of the repository-wide historical physical-venue naming census. It is a recovery artifact and working ledger, not yet the final permanent protocol. It does not itself create `OFFICIAL_NAMING_PERIOD` rows.

Research queue: `docs/historical-venue-name-research-queue.md`
Single-name high-yield screen: `docs/historical-venue-single-name-screen.md`

## Controlling model

- One physical building = one `venue_id`.
- A physical venue may have multiple **formal historical naming periods**.
- Nicknames, spelling/spacing variants, source shorthand, court/floor names, arena-within-building labels, complex names, sponsor overlays that the owner elects not to periodize, and typo variants remain aliases rather than periods.
- The existing alias registry is a discovery input, not complete historical authority. Research may identify genuine formal eras that are missing from the registry.
- Exact transition dates must be verified from institutional/facility or otherwise authoritative evidence before implementation unless already accepted in production.
- Owner heuristic: whether the commonly recognized identity of the building itself changed is a useful triage rule. Wikipedia naming/history may help discovery but is not final evidence authority.
- For imprecise game dates at migrated venues, website display falls back to the most recent verified accepted official name.
- Head-to-head/aggregate venue summaries show one label per physical venue: current verified name if active, canonical project name if inactive.
- Prior one-name display conventions for Illinois, Indiana, and Tennessee do not block date-aware periodization where owner rulings below approve it.

## Baseline census

At this baseline the repository contains:
- 846 physical venue IDs;
- 1,551 venue-name rows;
- 363 venues with multiple registered name rows;
- 483 venues with one registered name row.

The latest mechanical classifier produced only provisional triage counts (158 alias-only, 131 simple rename, 59 complex/mixed, 12 identity-sensitive, 3 already migrated). Those counts are **not** historical authority and will change as owner adjudication continues.

## Durable owner adjudication ledger

| Venue | Disposition | Owner-adjudicated working state |
|---|---|---|
| `VEN-000004` | `PERIODIZE` | Rosemont Horizon → Allstate Arena. |
| `VEN-000008` | `PERIODIZE` | St. Pete Times Forum → Amalie Arena → Benchmark International Arena; research may reveal omitted formal eras. |
| `VEN-000009` | `PERIODIZE` | National Car Rental Center → BankAtlantic Center → BB&T Center → FLA Live Arena → Amerant Bank Arena. |
| `VEN-000011` | `PERIODIZE` | Providence Civic Center → Dunkin’ Donuts Center → Amica Mutual Pavilion. |
| `VEN-000013` | `PERIODIZE` | Owner chronology verified: ARCO Arena → Power Balance Pavilion → Sleep Train Arena. `ARCO Arena II` is repository/building disambiguation only, never a formal arena-name period. Sacramento Kings material confirms ARCO usage through 2010-11, Power Balance Pavilion in 2011-12, and Sleep Train Arena from the 2012-13 era onward. Contemporary naming coverage places the transitions at 2011-03-01 and 2012-10-15; reverify exact effective-day semantics during implementation. |
| `VEN-000018` | `PERIODIZE` | Pepsi Center → Ball Arena. |
| `VEN-000019` | `PERIODIZE` | Baltimore Civic Center → Baltimore Arena → 1st Mariner Arena → Baltimore Arena → Royal Farms Arena → Baltimore Arena → CFG Bank Arena. The 1962 building became Baltimore Arena in 1986; 1st Mariner naming ran 2003-2013, followed by a Baltimore Arena reversion; Baltimore City approved Royal Farms title sponsorship in 2014, terminated effective 2022-06-27, after which `Baltimore Arena` again served as the unsponsored name during redevelopment; CFG naming rights were announced 2022-10-24 for the reopened venue. Owner-supplied `Royal Farms Arena in 2022` is corrected to 2014-2022. Exact 1986/2003/2013 and CFG naming-period day semantics remain implementation-date verification. |
| `VEN-000023` | `PERIODIZE` | Owner accepts the evidence-based treatment: NU Sports Complex → Bob Devaney Sports Center. Nebraska historical material states the 1976 facility was originally the NU/Nebraska Sports Complex and was renamed by Board of Regents vote for Bob Devaney in 1978; contemporaneous 1978-79 basketball evidence still uses `NU Sports Complex`, while a contemporary retrospective cites the Regents naming action on 1978-11-11. Treat `Devaney Center` / `B. Devaney Sports Center` as aliases of the second era. Exact 1978 naming-effective semantics remain implementation-date verification against the underlying Regents/contemporaneous record. |
| `VEN-000025` | `PERIODIZE` | BI-LO Center → Bon Secours Wellness Arena; The Well is alias only. |
| `VEN-000028` | `PERIODIZE` | Brendan Byrne Arena → Continental Airlines Arena → IZOD Center → Meadowlands Arena; Meadowlands is alias only. |
| `VEN-000031` | `PERIODIZE` | Gaylord Entertainment Center → Sommet Center → Bridgestone Arena; Gaylor Entertainment Center is typo only. |
| `VEN-000034` | `PERIODIZE` | Louisiana Superdome → Mercedes-Benz Superdome → Caesars Superdome; Superdome is alias only. |
| `VEN-000035` | `PERIODIZE` | Duke Indoor Stadium → Cameron Indoor Stadium. |
| `VEN-000036` | `PERIODIZE` | MCI Center → Verizon Center → Capital One Arena. |
| `VEN-000038` | `PERIODIZE` | Owner chronology verified: UCF Arena → CFE Arena → Addition Financial Arena. UCF states the arena opened in 2007; CFE acquired naming rights and `UCF Arena` became `CFE Arena` on 2013-05-23; Addition Financial's own release and UCF Board materials fix the CFE→Addition Financial Arena transition to 2019-05-01. |
| `VEN-000039` | `PERIODIZE` | University of Wichita Field House → WSU Field House → Levitt Arena → Charles Koch Arena. Owner working years 1955–64 / 1964–69 / 1969–2003 / 2003–present; exact boundaries to verify. |
| `VEN-000043` | `PERIODIZE` | Qwest Center → CenturyLink Center → CHI Health Center Omaha; variants without Omaha are aliases of matching eras. |
| `VEN-000049` | `PERIODIZE` | Carolina Center → Colonial Center → Colonial Life Arena. |
| `VEN-000051` | `PERIODIZE` | Staples Center → Crypto.com Arena. |
| `VEN-000052` | `MIGRATED` | CU Events/Conference Center → Coors Events Center → CU Events Center. Production-verified. |
| `VEN-000055` | `PERIODIZE` | Delta Center → EnergySolutions Arena → Vivint Smart Home Arena / Vivint Arena → Delta Center; exact formal wording/boundaries to verify. |
| `VEN-000056` | `PERIODIZE` | ASU Activity Center → Wells Fargo Arena → Desert Financial Arena. Owner working years 1974–97 / 1997–2019 / 2019–present; exact boundaries to verify. |
| `VEN-000058` | `PERIODIZE` | Tallahassee-Leon County Civic Center → Donald L. Tucker Civic Center. |
| `VEN-000060` | `PERIODIZE` | Kiel Center → Savvis Center → Scottrade Center → Enterprise Center; Scotttrade is typo only. |
| `VEN-000061` | `PERIODIZE` | BSU Pavilion → Taco Bell Arena → ExtraMile Arena. |
| `VEN-000064` | `ALIAS_ONLY` | One continuous Florida Gym identity; Florida Gymnasium variant, Alligator Alley nickname. |
| `VEN-000065` | `PERIODIZE` | America West Arena → US Airways Center → Talking Stick Resort Arena → Footprint Center → Mortgage Matchup Center; research may reveal omitted formal eras. |
| `VEN-000070` | `PERIODIZE` | Conseco Fieldhouse → Bankers Life Fieldhouse → Gainbridge Fieldhouse. |
| `VEN-000076` | `PERIODIZE` | Owner chronology verified conceptually: Greensboro Memorial Coliseum → Greensboro Coliseum → First Horizon Coliseum. Existing institutional game evidence supports the `Greensboro Memorial Coliseum` form in the 1960s; accepted historical references place the shortened Greensboro Coliseum era from 1980; and the City of Greensboro states the First Horizon naming-rights agreement took effect immediately on 2024-10-02. Exact 1980 transition day remains implementation-date verification. |
| `VEN-000078` | `ALIAS_ONLY` | One continuous Hec Edmundson Pavilion identity; Bank of America Arena / Alaska Airlines Arena treated as sponsor overlays. |
| `VEN-000080` | `PERIODIZE` | Butler Fieldhouse → Hinkle Fieldhouse. |
| `VEN-000082` | `PERIODIZE` | Arrowhead Pond of Anaheim → Honda Center; Arrowhead Pond / The Pond are aliases. |
| `VEN-000083` | `PERIODIZE` | Hoosier Dome → RCA Dome; Indiana Hoosier Dome alias. |
| `VEN-000084` | `PERIODIZE` | Disney’s Milk House → HP Field House → State Farm Field House. |
| `VEN-000095` | `PERIODIZE` | Rutgers Athletic Center → Louis Brown Athletic Center → Jersey Mike’s Arena. Rutgers confirms the arena opened in 1977 as Rutgers Athletic Center and university archival material fixes the Louis Brown rename to 1986. Owner proposed a formal 2019 return to Rutgers Athletic Center, but institutional evidence does not support that as a formal rename: Rutgers University still used `Louis Brown Athletic Center` in 2019 and into 2021, while Athletics used `Rutgers Athletic Center` / `RAC` as shorthand/branding. Jersey Mike’s naming became official on 2021-11-03. Do not create a 2019-21 formal RAC period. Exact 1986 day remains implementation-date verification. |
| `VEN-000096` | `MIGRATED` | Carrier Dome → JMA Wireless Dome. Production-verified. |
| `VEN-000097` | `PERIODIZE` | Special Events Center → Jon M. Huntsman Center. U. of U. Special Events Center / Huntsman Center / Jon Huntsman Center are aliases. Owner working history: opened 1969, renamed 1987; exact boundary to verify. |
| `VEN-000098` | `PERIODIZE` | Athletic and Convocation Center → Joyce Center; Purcell Pavilion is competition-space/branding alias only. |
| `VEN-000099` | `PERIODIZE` | Kemper Arena → Hy-Vee Arena. |
| `VEN-000103` | `PERIODIZE` | HSBC formal era → First Niagara Center → KeyBank Center; determine whether HSBC Arena or HSBC Center was the formal wording. |
| `VEN-000106` | `ALIAS_ONLY` | One continuous Downtown YMCA / Knoxville YMCA Gymnasium identity. |
| `VEN-000109` | `PERIODIZE` | BJCC Coliseum → BJCC Arena → Legacy Arena at the BJCC. BJCC’s official history states the arena opened in 1976 as BJCC Coliseum, became BJCC Arena in 1999, and entered the Legacy naming-rights era in 2015. Legacy Credit Union fixes the last boundary exactly: partnership announced December 2014 and effective 2015-01-01. Owner’s `Legacy Arena since 2014` is corrected to 2015-01-01. `Birmingham-Jefferson Civic/Convention Center`, `BJCC`, `Birmingham Coliseum`, `Jefferson Coliseum`, and related variants are complex/location/source shorthand rather than separate formal arena periods. Exact 1999 day remains implementation-date verification. |
| `VEN-000110` | `PERIODIZE` | Raleigh Entertainment & Sports Arena → RBC Center → PNC Arena → Lenovo Center. |
| `VEN-000115` | `ALIAS_ONLY` | One continuous Lawrence Joel Veterans Memorial Coliseum identity; LJVM / Joel Coliseum forms are aliases. |
| `VEN-000118` | `ALIAS_ONLY` | One continuous Los Angeles Memorial Sports Arena identity; L.A./Sports Arena variants are aliases. |
| `VEN-000119` | `ALIAS_ONLY` | One continuous Lubbock Municipal Coliseum identity unless authoritative research establishes a true rename; Lubbock Memorial Coliseum / Memorial Coliseum treated as source variants. |
| `VEN-000127` | `ALIAS_ONLY` | One continuous McKale Center identity; McKale Center at ALKEME Arena and related sponsored wording do not create periods. |
| `VEN-000128` | `ALIAS_ONLY` | One continuous McNichols Sports Arena identity; McNichols Arena alias. |
| `VEN-000131` | `ALIAS_ONLY` | One continuous Memphis Pyramid identity; The Pyramid alias. |
| `VEN-000133` | `ALIAS_ONLY` | One continuous MGM Grand Garden Arena identity; MGM Grand Arena alias. |
| `VEN-000138` | `PERIODIZE` | Rose Garden → Moda Center; Rose Garden Arena alias. |
| `VEN-000139` | `ALIAS_ONLY` | One continuous Mohegan Sun Arena identity; Mohegan Sun is complex/source shorthand. |
| `VEN-000141` | `PERIODIZE` | SMU Coliseum → Moody Coliseum. |
| `VEN-000145` | `PERIODIZE` | Knickerbocker Arena → Pepsi Arena → Times Union Center → MVP Arena. |
| `VEN-000147` | `ALIAS_ONLY` | One continuous Nassau Veterans Memorial Coliseum identity; Nassau Coliseum shorthand and NYCB Live branding overlay are aliases. |
| `VEN-000149` | `PERIODIZE` | Honolulu International Center → Neal S. Blaisdell Center; Blaisdell Arena is alias/arena-within-complex treatment. |
| `VEN-000150` | `PERIODIZE` | Auburn Arena → Neville Arena. |
| `VEN-000152` | `PERIODIZE` | Spokane Veterans Memorial Arena → Numerica Veterans Arena; Spokane Arena / abbreviated forms are aliases. |
| `VEN-000154` | `ALIAS_ONLY` | One continuous O’Connell Center identity; Exactech / expanded Stephen C. O’Connell sponsor wording are aliases. |
| `VEN-000162` | `PERIODIZE` | Ford Center → Chesapeake Energy Arena → Paycom Center. |
| `VEN-000167` | `PERIODIZE` | CONSOL Energy Center → PPG Paints Arena. |
| `VEN-000172` | `PERIODIZE` | Reliant Stadium → NRG Stadium. |
| `VEN-000174` | `ALIAS_ONLY` | One continuous Reynolds Coliseum identity; James T. Valvano Arena / expanded formal descriptions are competition-space aliases. |
| `VEN-000176` | `PERIODIZE` | Riverfront Coliseum → The Crown → Firstar Center → U.S. Bank Arena → Heritage Bank Center. Owner chronology is verified: the arena opened in 1975 as Riverfront Coliseum, became The Crown in 1997, Firstar Center in 1999, U.S. Bank Arena in 2002, and Heritage Bank Center on 2019-11-04. `The Crown` was a genuine formal venue name, not merely a nickname. `Cincinnati Coliseum` and combined former-name strings are aliases/source wording. Exact 1997/1999/2002 transition days remain implementation-date verification. |
| `VEN-000179` | `PERIODIZE` | Gund Arena → Quicken Loans Arena → Rocket Mortgage FieldHouse → Rocket Arena. |
| `VEN-000183` | `PERIODIZE` | San Jose Arena → Compaq Center at San Jose → HP Pavilion → SAP Center. |
| `VEN-000185` | `PERIODIZE` | Research tranche 1 resolved formal sequence Alltel Arena → Verizon Arena → Simmons Bank Arena. Alltel opened in October 1999; Verizon naming began 2009-07-01; Simmons Bank naming began 2019-10-03. Exact first-period valid_from still requires implementation-date verification against the operational opening record. |
| `VEN-000186` | `PERIODIZE` | Assembly Hall → Simon Skjodt Assembly Hall. |
| `VEN-000187` | `PERIODIZE` | The Pavilion at Ole Miss → Sandy and John Black Pavilion at Ole Miss; SJB Pavilion / The Pavilion aliases. |
| `VEN-000188` | `PERIODIZE` | New Orleans Arena → Smoothie King Center. |
| `VEN-000190` | `PERIODIZE` | Charlotte Bobcats Arena → Time Warner Cable Arena → Spectrum Center. |
| `VEN-000193` | `PERIODIZE` | St. Louis Arena → The Checkerdome → St. Louis Arena, if formal adoption/reversion dates verify. |
| `VEN-000194` | `ALIAS_ONLY` | One continuous Stan Sheriff Center identity; SimpliFi variants are sponsor overlays. |
| `VEN-000195` | `PERIODIZE` | Philips Arena → State Farm Arena. |
| `VEN-000196` | `MIGRATED` | Assembly Hall → State Farm Center. Production-verified. |
| `VEN-000197` | `PERIODIZE` | University of Phoenix Stadium → State Farm Stadium. |
| `VEN-000198` | `PERIODIZE` | Georgia Coliseum → Stegeman Coliseum. |
| `VEN-000202` | `PERIODIZE` | Sprint Center → T-Mobile Center. |
| `VEN-000203` | `PERIODIZE` | FleetCenter → TD Banknorth Garden → TD Garden. |
| `VEN-000204` | `PERIODIZE` | Trans World Dome → The Dome at America’s Center → Edward Jones Dome → The Dome at America’s Center. Owner correctly requires the omitted Trans World era even without current canonical games, but research also establishes a genuine unsponsored interim after TWA naming rights ended in 2001 and before Edward Jones acquired naming rights on 2002-01-25. A 2024 facility assessment states Edward Jones ended its naming-rights agreement in February 2016 and the venue returned to The Dome at America’s Center. Exact 1995 Trans World valid_from, 2001 interim boundary, and February 2016 day remain implementation-date verification. Do not collapse the interim Dome period merely because no canonical game currently falls within it. |
| `VEN-000208` | `PERIODIZE` | University Arena → WisePies Arena → Dreamstyle Arena → The Pit. Owner working former-name years 1966–2014 / 2014–17 / 2017–20; exact transitions to verify. |
| `VEN-000209` | `PERIODIZE` | The Spectrum → CoreStates Spectrum → First Union Spectrum → Wachovia Spectrum; separate formal periods. |
| `VEN-000210` | `PERIODIZE` | The Summit → Compaq Center; Summit alias. |
| `VEN-000211` | `ALIAS_ONLY` | One continuous Thompson-Boling Arena identity. Owner explicitly rejects Food City branding as separate periods. |
| `VEN-000214` | `PERIODIZE` | Florida Suncoast Dome → ThunderDome → Tropicana Field. |
| `VEN-000218` | `PERIODIZE` | United Spirit Arena → United Supermarkets Arena. |
| `VEN-000224` | `PERIODIZE` | Milwaukee Arena → The MECCA → Wisconsin Center Arena → U.S. Cellular Arena → UW-Milwaukee Panther Arena. Complex-level Milwaukee Exposition & Convention Center wording is not a period. Working years 1950–74 / 1974–95 / 1995–2000 / 2000–14 / 2014–present; exact boundaries to verify. |
| `VEN-000233` | `PERIODIZE` | CSU Convocation Center → Wolstein Center; Goodman Arena is alias/interior competition-space treatment. |
| `VEN-000236` | `PERIODIZE` | Comcast Center → Xfinity Center. |
| `VEN-000237` | `PERIODIZE` | CoreStates Center → First Union Center → Wachovia Center → Wells Fargo Center → Xfinity Mobile Arena; malformed/non-name alias rows should be cleaned only after independent confirmation. |
| `VEN-000257` | `PERIODIZE` | Hartford Civic Center → XL Center → PeoplesBank Arena. |
| `VEN-000261` | `PERIODIZE` | Crisler Arena → Crisler Center. |
| `VEN-000273` | `PERIODIZE` | NTSU Coliseum → UNT Coliseum; North Texas Coliseum / Super Pit / The Super Pit are aliases. |
| `VEN-000283` | `ALIAS_ONLY` | One continuous Beasley Coliseum identity; Friel Court and related formulations are court-name aliases. |
| `VEN-000291` | `PERIODIZE` | Hofheinz Pavilion → Fertitta Center. |
| `VEN-000295` | `PERIODIZE` | SBC Center → AT&T Center → Frost Bank Center. |
| `VEN-000297` | `ALIAS_ONLY` | One continuous Veterans Memorial Coliseum (Portland) identity; Memorial Coliseum / Portland Mem. Coliseum shorthand. |
| `VEN-000370` | `PERIODIZE` | Daniel-Meyer Coliseum → Schollmaier Arena. |
| `VEN-000378` | `ALIAS_ONLY` | One continuous Dee Glen Smith Spectrum identity; Spectrum is shorthand alias. |
| `VEN-000383` | `ALIAS_ONLY` | One continuous Torodome identity; The Gymnasium / CSUDH Gymnasium are descriptive/source aliases. |
| `VEN-000393` | `PERIODIZE` | Harmon Gym → Haas Pavilion. |
| `VEN-000422` | `PERIODIZE` | Stanford Pavilion → Burnham Pavilion; Old Pavilion alias. |
| `VEN-000442` | `PERIODIZE` | Memorial Gymnasium → Memorial Athletic and Convocation Center; MAC Center shorthand alias. |
| `VEN-000456` | `PERIODIZE` | Alumni Hall → Carnesecca Arena. |
| `VEN-000511` | `PERIODIZE` | University of Detroit Memorial Building / Memorial Building → Calihan Hall. |
| `VEN-000524` | `ALIAS_ONLY` | Basketball-era identity is WVU Field House / Field House. WVU archival and institutional history states the first game there was 1929-01-03 and the final WVU college basketball game was 1970-03-03; the building was renamed Stansbury Hall in October 1973, after varsity basketball had departed. `Mountaineer Field House` appears in later institutional retrospective wording but is not established as a separate formal basketball-era name. Treat Stansbury Hall as post-basketball building continuity and Mountaineer Field House as alias/retrospective wording, not naming periods for canonical basketball display. |
| `VEN-000701` | `PERIODIZE` | duPont Pavilion → Finneran Pavilion; The Pavilion / Pavilion / PV / FPV are aliases of applicable eras. |
| `VEN-000828` | `ALIAS_ONLY` | Owner treatment verified: the 1948 temporary UConn basketball facility is `The Cage` / `Storrs Cage`. UConn Archives states it was built from surplus Army Air Corps hangars and was known as `the Cage`; institutional material also calls it the basketball/ROTC hangar. `Hangar`, `Basketball Hangar`, and `The Hangar` are descriptive/nickname forms, `Hanger` is a misspelling, and `Quonset Hut` is not supported as the basketball building's formal identity. No naming periods are warranted. |
| `VEN-000829` | `PERIODIZE` | Field House → Hugh S. Greer Field House. UConn Archives states the building was built in 1954 and repeatedly calls the pre-1991 facility simply `the Field House`; the Board of Trustees voted in 1991 to rename it for former coach Hugh S. Greer. `UConn Field House`, `Storrs Field House`, and bare `Field House` are institution/location-qualified variants of the first era rather than distinct formal periods. Exact 1991 Board-action/effective day remains implementation-date verification. |

| `VEN-000002` | `ALIAS_ONLY` | One continuous Alamodome identity; Alamaodome is typo only. |
| `VEN-000007` | `ALIAS_ONLY` | One continuous Alumni Gym identity; Alumni Gymnasium / Alumni Memorial Auditorium-Gymnasium / Alumni Memorial Gym are formal/descriptive variants, not separate eras. |
| `VEN-000012` | `PERIODIZE` | Amway Center → Kia Center. |
| `VEN-000020` | `ALIAS_ONLY` | One continuous Barclays Center identity; Brooklyn, NY / Barclays Center is location-decorated source text. |
| `VEN-000026` | `PERIODIZE` | Bradley Center → BMO Harris Bradley Center. |
| `VEN-000029` | `ALIAS_ONLY` | One continuous Breslin Center identity; Jack Breslin Student Events Center is the expanded formal name. |
| `VEN-000037` | `ALIAS_ONLY` | One continuous Carver-Hawkeye Arena identity; dash typography variant only. |
| `VEN-000040` | `PERIODIZE` | Charlotte Coliseum → Independence Arena → Cricket Arena → Bojangles Coliseum, with a genuine 1988-1993 closure gap. Mecklenburg County and the current BOplex history confirm the same 1955 building; BOplex states it temporarily closed from 1988-1993 and reopened in 1993. Charlotte City records confirm a five-year Cricket naming-rights agreement beginning in 2001, extended while the facility continued as Cricket Arena, and City Council approved the Bojangles Coliseum name on 2008-11-24. Owner chronology is conceptually correct; exact Charlotte→Independence reopening date and 2001 Cricket effective day remain implementation-date verification. `Charlotte Coliseum I` / `(1955 building)` are disambiguation only. |
| `VEN-000041` | `ALIAS_ONLY` | One continuous 1988 Charlotte Coliseum identity; Charlotte Coliseum II / year/building variants are physical-disambiguation labels, not naming eras. |
| `VEN-000048` | `PERIODIZE` | Memorial Coliseum → Coleman Coliseum. |
| `VEN-000050` | `ALIAS_ONLY` | One continuous Convention Hall identity; Kansas City Convention Hall is location-qualified form. |
| `VEN-000053` | `ALIAS_ONLY` | One continuous Dean Smith Center identity; Dean E. Smith Student Activities Center / Smith Center are expanded/short forms. |
| `VEN-000054` | `ALIAS_ONLY` | One continuous Dee Events Center identity; Dee Event Center is singular/plural source variant. |
| `VEN-000062` | `ALIAS_ONLY` | One continuous FedExForum identity; FedEx Forum is spacing variant. |
| `VEN-000068` | `ALIAS_ONLY` | One continuous Frank Erwin Center identity; Erwin Center is shorthand. |
| `VEN-000072` | `PERIODIZE` | Gallagher Hall → Gallagher-Iba Arena. |
| `VEN-000079` | `ALIAS_ONLY` | One continuous Hilton Coliseum identity; James Hilton Coliseum is expanded naming form. |
| `VEN-000085` | `ALIAS_ONLY` | One continuous Hubert H. Humphrey Metrodome identity; HHH Metrodome / Metrodome are short forms. |
| `VEN-000088` | `ALIAS_ONLY` | One continuous Imperial Arena identity; Imperial Arena at Atlantis / Atlantis Imperial Arena / Imperial Ballroom are source/event/resort variants rather than naming eras. |
| `VEN-000090` | `ALIAS_ONLY` | One continuous INTRUST Bank Arena identity; Intrust Bank Arena is capitalization variant. |
| `VEN-000091` | `ALIAS_ONLY` | One continuous Iowa Field House identity; Iowa City Fieldhouse is location/spacing variant. |
| `VEN-000102` | `IDENTITY_RESOLVED` | Verified physical reconciliation: VEN-000102 and VEN-000315 are one Seattle Center arena lineage. Preserve the earlier-established VEN-000102 as the surviving global physical identity and retire VEN-000315 during later dedicated shared-reference maintenance. Current-main census found VEN-000315 in five school venue tables and no canonical-game, assertion, or NCAA-site evidence rows; VEN-000102 already carries historical/NCAA evidence. Naming research supports fair-era `Washington State Pavilion` / `Washington State Coliseum` terminology, then Seattle Center Coliseum → KeyArena → Climate Pledge Arena. Do not invent an intra-1962 Pavilion/Coliseum boundary where official Seattle sources conflict. Historical identity: RESOLVED. Global registration cleanup: PENDING_DEDICATED_MAINTENANCE. |
| `VEN-000315` | `IDENTITY_RESOLVED` | Linked duplicate of VEN-000102. Climate Pledge Arena is the same Seattle Center physical lineage despite the 2018-2021 redevelopment beneath the preserved historic roof/structure. Later dedicated maintenance should retire VEN-000315 into surviving VEN-000102 and rebind the five published-school venue rows that currently reference VEN-000315. Historical identity: RESOLVED. Global registration cleanup: PENDING_DEDICATED_MAINTENANCE. |
| `VEN-000123` | `ALIAS_ONLY` | One continuous Madison Square Garden III physical-building identity; MSG III / Old Madison Square Garden / 1925-building variants are disambiguation or shorthand only. |
| `VEN-000124` | `ALIAS_ONLY` | One continuous Madison Square Garden IV physical-building identity; MSG IV / 1968-building variants are disambiguation or shorthand only. |
| `VEN-000126` | `ALIAS_ONLY` | One continuous McArthur Court identity; Mac Court is nickname/shorthand. |
| `VEN-000129` | `ALIAS_ONLY` | One continuous Memorial Coliseum (Lexington) identity; location-qualified variants only. |
| `VEN-000143` | `ALIAS_ONLY` | One continuous Municipal Auditorium (Kansas City) identity; city-qualified variants only. |
| `VEN-000146` | `PERIODIZE` | Research tranche 1 resolved formal history as Myriad Convention Center (expanded official title Allen M. Street Myriad Convention Center) → Cox Business Services Convention Center → Prairie Surf Studios. Oklahoma City council approved the Cox naming agreement on 2002-02-05; Prairie Surf took over 2021-01-01. Exact naming-period boundary semantics remain implementation-date verification, not a conceptual ambiguity. |
| `VEN-000151` | `ALIAS_ONLY` | One continuous New Gymnasium identity; The New Gym is shorthand. |
| `VEN-000153` | `PERIODIZE` | Oakland-Alameda County Coliseum Arena / Oakland Coliseum Arena → The Arena in Oakland → Oakland Arena → Oracle Arena → Oakland Arena. Oakland Arena's official legacy says the original arena became `The Arena in Oakland` with the 1990s renovation, was officially renamed `Oakland Arena` in 2001, became Oracle Arena in 2006, and reverted to Oakland Arena in 2019. The owner working chronology omitted the real 2001-2006 Oakland Arena period. Official Warriors material fixes Oracle to 2006-10-30; exact first-era→The Arena in Oakland boundary remains implementation-date verification because venue/Warriors retrospectives differ on 1996 renovation completion versus 1997 reopening semantics. |
| `VEN-000155` | `ALIAS_ONLY` | One continuous Old Gym identity; Vanderbilt Old Gym is location/institution-qualified form. |
| `VEN-000157` | `ALIAS_ONLY` | One continuous Omni Coliseum identity; The Omni / Omni are shorthand. |
| `VEN-000158` | `PERIODIZE` | Orlando Arena → TD Waterhouse Centre → Amway Arena. |
| `VEN-000159` | `ALIAS_ONLY` | One continuous Palestra identity; The Palestra is article-prefixed variant. |
| `VEN-000160` | `CANONICAL_CORRECTION` | Research tranche 1 resolved the correct spelling as Patten Gymnasium. VEN-000160 is the original 1909 Patten Gymnasium that hosted the 1939 NCAA championship and was razed in 1940; Northwestern then built a distinct replacement Patten Gymnasium. `Patton Gymnasium` is erroneous and the two physical buildings must not be merged. |
| `VEN-000163` | `PERIODIZE` | LSU Assembly Center → Pete Maravich Assembly Center; Maravich Assembly Center / Assembly Center are aliases. |
| `VEN-000170` | `ALIAS_ONLY` | One continuous Prudential Center identity; Newark, NJ / Prudential Center is location-decorated source text. |
| `VEN-000177` | `ALIAS_ONLY` | One continuous Roberts Municipal Stadium identity; Roberts Stadium is shorthand. |
| `VEN-000182` | `PERIODIZE` | San Diego International Sports Arena → San Diego Sports Arena → iPayOne Center → San Diego Sports Arena → Valley View Casino Center → San Diego Sports Arena (brief unsponsored reversion) → Pechanga Arena San Diego. City historic-resource evidence confirms the 1966 opening identity as San Diego International Sports Arena; City Council approved iPayOne naming in March 2005, consented to Valley View in October 2010, and approved the Pechanga rename in December 2018. The owner's detailed 2005-2018 day boundaries are consistent with contemporaneous reporting but should be rechecked at implementation. Protected main independently proves Cox Arena/Viejas Arena is VEN-000226, a different SDSU physical venue; the malformed Cox/Viejas alias rows under VEN-000182 are erroneous cross-venue contamination and must be removed during registry cleanup. |
| `VEN-000191` | `ALIAS_ONLY` | One continuous UVI Sports and Fitness Center identity; full-name, ampersand, singular/plural and institution-qualified variants are aliases. |
| `VEN-000199` | `PERIODIZE` | Armory Fieldhouse → Stokely Athletics Center; Stokely Center and combined source strings are aliases. |
| `VEN-000206` | `ALIAS_ONLY` | One continuous The Palace of Auburn Hills identity; Palace of Auburn Hills / The Palace are aliases. |
| `VEN-000220` | `ALIAS_ONLY` | One continuous University Gymnasium identity; The Gym is shorthand. |
| `VEN-000221` | `ALIAS_ONLY` | One continuous University of Dayton Arena identity; UD Arena / Dayton Arena / abbreviated institutional forms are aliases. |
| `VEN-000225` | `PERIODIZE` | Value City Arena → Schottenstein Center. Owner explicitly rules these as two distinct periods. |
| `VEN-000226` | `PERIODIZE` | Cox Arena → Viejas Arena; Cox Arena at Aztec Bowl is alias/expanded form of first era. |
| `VEN-000227` | `PERIODIZE` | Jacksonville Veterans Memorial Arena → VyStar Veterans Memorial Arena; Memorial Arena / Veterans Memorial Arena are shorthand unless later evidence proves otherwise. |
| `VEN-000229` | `PERIODIZE` | McGaw Memorial Hall → Welsh-Ryan Arena; McGaw Hall / Northwestern McGaw Hall are aliases. |
| `VEN-000232` | `ALIAS_ONLY` | One continuous Wisconsin Field House identity; UW Field House is shorthand. |
| `VEN-000234` | `RESEARCH_EXHAUSTED` | Owner closed the bounded residual as research exhausted. Opening identity is supported as Centrum in Worcester; later sources use Worcester’s Centrum Centre; the DCU naming-rights agreement was reached in October 2004. Available authoritative evidence does not establish a reliable exact adoption boundary/formal status for Worcester’s Centrum Centre or an exact DCU effective day. Preserve the uncertainty and do not invent dates. Reopen only if a materially stronger city/venue archival source appears. |
| `VEN-000235` | `PERIODIZE` | WVU Coliseum → Hope Coliseum. Owner explicitly rules these as two distinct periods. |
| `VEN-000238` | `PERIODIZE` | USF Sun Dome → Yuengling Center; Sun Dome is alias/short form of first era. |
| `VEN-000240` | `ALIAS_ONLY` | One continuous C.M. “Tad” Smith Coliseum identity; Tad Smith Coliseum is shortened form. |
| `VEN-000241` | `PERIODIZE` | Civic Arena → Mellon Arena; Pittsburgh Civic Arena is location-qualified first-era alias. |
| `VEN-000248` | `PERIODIZE` | Jefferson County Armory → Louisville Convention Center → Louisville Gardens, subject to exact continuity/boundary verification; The Armory is alias. |
| `VEN-000249` | `PERIODIZE` | Alexander Memorial Coliseum → McCamish Pavilion. |
| `VEN-000250` | `PERIODIZE` | Research tranche 1 resolved formal history as Mississippi State Gymnasium → McCarthy Gymnasium. `New Gym` is contemporary shorthand for Mississippi State Gymnasium, not a separate formal period. Basketball opened there 1950-12-15; the building was renamed for Babe McCarthy after his 1975 death, but the exact 1975 rename date remains implementation-date verification. |
| `VEN-000259` | `PERIODIZE` | Capital Centre → USAir Arena. |
| `VEN-000267` | `ALIAS_ONLY` | One continuous Baha Mar Convention Center identity; Baha Mar Convention, Arts & Entertainment Center is expanded/formal wording rather than a separate era. |
| `VEN-000270` | `ALIAS_ONLY` | One continuous John M. Parker Agricultural Coliseum identity; Cow Palace is a nickname/source alias. |
| `VEN-000271` | `ALIAS_ONLY` | One continuous Raider Arena identity. Northwest Florida State College's facilities master plan identifies the completed 2011 Building 200 project as Community Services Complex and Raider Arena; current institutional usage remains Raider Arena. `The Arena` / `The Arena at Northwest Florida State College` are descriptive/source variants, not historical formal-name periods. |
| `VEN-000272` | `ALIAS_ONLY` | One continuous Conte Forum identity; Silvio O. Conte Forum is the full formal name. |
| `VEN-000274` | `ALIAS_ONLY` | One continuous Atlanta Municipal Auditorium identity; Municipal Auditorium / City Auditorium are source shorthand. |
| `VEN-000275` | `ALIAS_ONLY` | One continuous Athens YMCA identity; Old Athens YMCA is descriptive alias. |
| `VEN-000276` | `PERIODIZE` | Memorial Hall → Alumni Hall. |
| `VEN-000277` | `ALIAS_ONLY` | One continuous The Octagon identity; Octagon is shorthand. |
| `VEN-000280` | `PERIODIZE` | Carolina First Arena → TD Arena. |
| `VEN-000292` | `ALIAS_ONLY` | One continuous Armory identity; The Armory is alias. |
| `VEN-000296` | `ALIAS_ONLY` | Britt Brown Arena is the physical arena. Wichita State and Sedgwick County describe the Kansas Coliseum as the larger complex containing Britt Brown Arena plus multiple pavilions/RV facilities. `Kansas Coliseum` is complex/location wording, not a historical rename of the arena. |
| `VEN-000301` | `ALIAS_ONLY` | One continuous Allen County War Memorial Coliseum identity; War Memorial Coliseum / FW Memorial Coliseum are shorthand. |
| `VEN-000302` | `PERIODIZE` | Alumni Memorial Fieldhouse → Hagan Arena. |
| `VEN-000303` | `ALIAS_ONLY` | One continuous Bryce Jordan Center identity; BJC / Bryce Center are aliases. |
| `VEN-000305` | `ALIAS_ONLY` | One continuous Keaney Gymnasium identity; Keaney Gym is shorthand. |
| `VEN-000306` | `ALIAS_ONLY` | One continuous Matthew Knight Arena identity; Matt Knight Arena / MKA are aliases. |
| `VEN-000307` | `ALIAS_ONLY` | One continuous Penn State Armory identity; The Armory is shorthand. |
| `VEN-000308` | `PERIODIZE` | Recreation Hall → Recreation Building. Penn State's University Libraries campus-history collection states that the building was originally named Recreation Hall and was renamed Recreation Building in 1957; `Rec Hall` is the common nickname. Exact 1957 effective day remains implementation-date verification. |
| `VEN-000309` | `ALIAS_ONLY` | One continuous The Hazell Center identity; Hazell Center is article-only variant. |
| `VEN-000310` | `ALIAS_ONLY` | One continuous Grant Memorial Hall identity; Grant Hall is shorthand. |
| `VEN-000311` | `ALIAS_ONLY` | One continuous State Fairgrounds Coliseum identity; Nebraska State Fairgrounds Coliseum is institution/location-qualified form. |
| `VEN-000312` | `ALIAS_ONLY` | One continuous Nebraska Coliseum identity; NU Coliseum is shorthand. |
| `VEN-000316` | `PERIODIZE` | Hershey Sports Arena → Hersheypark Arena. Hershey Community Archives confirms the 1936 opening-era Hershey Sports Arena identity and that the building is now called Hersheypark Arena; current operator usage confirms the no-space `Hersheypark Arena` form. Existing `Hershey Arena` / `Hershey Park Arena` forms are aliases/variants. Exact rename boundary remains implementation-date verification. |
| `VEN-000318` | `ALIAS_ONLY` | One continuous Loyola Field House identity; Loyola University Fieldhouse is expanded institutional wording/spelling variant. |
| `VEN-000324` | `CANONICAL_CORRECTION` | Verified: the Richmond facility is Robins Center, named for the E. Claiborne Robins family; University of Richmond Athletics consistently uses `Robins Center` from its 1972 opening through the present. `Robbins Center` is an erroneous spelling, not a historical name. Later shared-reference maintenance should correct the PROJECT_DISPLAY spelling and retain no false naming period. |
| `VEN-000325` | `PERIODIZE` | Special Events Center → Don Haskins Center; Haskins Center is shorthand of second era. |
| `VEN-000326` | `PERIODIZE` | Springfield Civic Center → MassMutual Center; Springfield CC is shorthand of first era. |
| `VEN-000328` | `ALIAS_ONLY` | One continuous Frank Thompson Gymnasium identity; Thompson Gym / Frank Thompson Gym are shortened forms. |
| `VEN-000329` | `PERIODIZE` | Virginia Tech Coliseum → Cassell Coliseum. |
| `VEN-000335` | `ALIAS_ONLY` | One continuous Gregory Gymnasium identity; Gregory Gym is shorthand. |
| `VEN-000338` | `ALIAS_ONLY` | One continuous Men’s Gym identity; University Men’s Gym is expanded institutional form. |
| `VEN-000339` | `PERIODIZE` | UIC Pavilion → Credit Union 1 Arena. |
| `VEN-000342` | `ALIAS_ONLY` | One continuous R.O.T.C. Armory identity; ROTC Armory is punctuation-only variant. |
| `VEN-000343` | `ALIAS_ONLY` | One continuous Mississippi Coliseum identity; The Big House is nickname. |
| `VEN-000344` | `ALIAS_ONLY` | One continuous Carolina Coliseum building identity. University of South Carolina-affiliated historical evidence states that the playing area inside the Coliseum was named Frank McGuire Arena in 1977. Treat `Frank McGuire Arena` as a competition-space alias, not a building rename period. |
| `VEN-000346` | `ALIAS_ONLY` | One continuous physical building, but not a basketball-era rename sequence. South Carolina states that the second-story Carolina Gymnasium was created/named in 1910 and served as the basketball home through 1927; the building was later named Longstreet Gymnasium in 1968 and converted/renamed Longstreet Theatre in 1977. Treat Longstreet Theater as later building-use/location continuity, not a historical basketball-venue naming period. |
| `VEN-000347` | `ALIAS_ONLY` | One continuous Coliseo Rubén Rodríguez identity; Ruben Rodriguez Coliseum is English/transliteration variant. |
| `VEN-000348` | `ALIAS_ONLY` | One continuous Colonial Hall identity; Colonial Hall at The Greenbrier is resort-qualified form. |
| `VEN-000349` | `PERIODIZE` | Glendale Arena → Jobing.com Arena → Gila River Arena → Desert Diamond Arena. Owner chronology is verified conceptually: the City-owned arena opened in 2003 as Glendale Arena, Jobing.com naming began in October 2006, Gila River naming was announced 2014-08-13, and Desert Diamond Arena became the new name on 2022-08-23. Exact October 2006 effective day remains implementation-date verification. |
| `VEN-000350` | `PERIODIZE` | Myrl H. Shoemaker Center → Fifth Third Arena at Myrl H. Shoemaker Center. Cincinnati Athletics states the 1989 building was originally the Myrl H. Shoemaker Center and was renamed `Fifth Third Arena at Myrl H. Shoemaker Center` in 2004, correcting the owner's 2005 working year. `Fifth Third Arena` is the accepted shortened second-era form; retained Shoemaker wording does not create a third naming period. Exact 2004 effective day remains implementation-date verification. |
| `VEN-000351` | `ALIAS_ONLY` | One continuous Gampel Pavilion identity; Harry A. Gampel Pavilion is full formal name. |
| `VEN-000352` | `ALIAS_ONLY` | One continuous Hard Rock Hotel Riviera Maya Convention Center identity; ballroom/resort variants are descriptive source wording. |
| `VEN-000353` | `ALIAS_ONLY` | Harrah’s Cherokee Center – Asheville is the surrounding civic-center facility/complex; ExploreAsheville.com Arena is the specific arena inside it. City/HCCA sources explicitly describe the center as home to the arena and Thomas Wolfe Auditorium. These are concurrent complex-versus-interior-arena names, not successive names of one arena. Do not periodize Harrah’s Cherokee Center → ExploreAsheville.com Arena. |
| `VEN-000356` | `ALIAS_ONLY` | One continuous Orleans Arena identity; article/hotel-qualified variants are aliases. |
| `VEN-000358` | `ALIAS_ONLY` | One continuous Puerto Vallarta International Convention Center identity; ICC is abbreviation. |
| `VEN-000363` | `ALIAS_ONLY` | One continuous William and Mary Hall identity; William & Mary Hall is typography/style variant. |
| `VEN-000369` | `PERIODIZE` | Redbird Arena → CEFCU Arena. |
| `VEN-000371` | `CANONICAL_CORRECTION` | Verified canonical form is Eugenio Guerra Sports Complex. Multiple institutional schedules/records, including Georgia Tech, Maryland, Ole Miss, and contemporaneous American University of Puerto Rico tournament material, use `Eugenio Guerra Sports Complex`; `Eugene Guerra Sports Complex` appears as an English/source error variant. No naming periods are warranted. The existing PROJECT_DISPLAY already has the correct Eugenio form; later registry cleanup should demote/remove the erroneous Eugene alias as appropriate. |
| `VEN-000373` | `PERIODIZE` | Oregon State Coliseum → Gill Coliseum. |
| `VEN-000377` | `ALIAS_ONLY` | One continuous Thomas & Mack Center identity; Tarkanian Court is competition-space name and Thomas & Mack Arena is variant. |
| `VEN-000382` | `IDENTITY_RESOLVED` | Verified physical reconciliation: VEN-000382 is George Albert Smith Fieldhouse / Smith Fieldhouse in Provo, while Einar Nielsen Fieldhouse is the distinct University of Utah building already correctly registered as VEN-000582 in Salt Lake City. Current main therefore does not need a new Nielsen venue ID; it needs removal of the erroneous `Nielsen Field House` alias from VEN-000382 and removal of that false alias from Utah’s local Smith Fieldhouse mapping, while preserving literal source provenance elsewhere. VEN-000582 remains the Nielsen identity. Historical identity: RESOLVED. Global alias cleanup: PENDING_DEDICATED_MAINTENANCE. |
| `VEN-000384` | `ALIAS_ONLY` | One continuous Men’s Gymnasium identity; Men’s Gym / University Gymnasium are variants. |
| `VEN-000385` | `ALIAS_ONLY` | One continuous Old University Gymnasium identity; University Gymnasium / Old Gymnasium are variants. |
| `VEN-000386` | `ALIAS_ONLY` | One continuous Anaheim Convention Center arena identity; Arena specifies the basketball space rather than a rename. |
| `VEN-000388` | `ALIAS_ONLY` | Baoshan Sports Center is the overall Shanghai sports-center complex; the basketball competition space is its basketball arena/gymnasium. Shanghai Sports Bureau material explicitly refers to the Baoshan Sports Center basketball gymnasium (宝山体育中心篮球馆). `Baoshan Sports Center` is complex/location wording for the arena, not a historical rename of Baoshan Arena. |
| `VEN-000389` | `ALIAS_ONLY` | One continuous Cannon Activities Center identity; George Q. Cannon/full and Cannon Event Center forms are aliases unless later evidence establishes a formal rename. |
| `VEN-000395` | `ALIAS_ONLY` | One continuous Astrodome identity; Houston qualifier only. Prior duplicate physical venue ID already retired. |
| `VEN-000396` | `RESEARCH_EXHAUSTED` | Owner closed the bounded residual as research exhausted. Same-building continuity is established for the fieldhouse beside the former Public School/Jeppesen/Robertson Stadium, and institutional/registry evidence supports both `Public School Fieldhouse` and `Jeppesen Fieldhouse`; `Jeppesen Gymnasium` is wording for that same facility. The bounded authoritative pass did not establish a safe formal adoption boundary. Do not borrow the adjacent stadium’s 1958 Jeppesen rename or manufacture a fieldhouse period. Reopen only if materially stronger archival evidence appears. |
| `VEN-000405` | `ALIAS_ONLY` | One continuous Marriott Center identity; Mariott Center is typo only. |
| `VEN-000408` | `ALIAS_ONLY` | One continuous UCLA Men’s Gymnasium identity; Men’s Gym is shorthand. |
| `VEN-000411` | `ALIAS_ONLY` | One continuous Municipal Auditorium (New Orleans) identity; city qualifier only. |
| `VEN-000413` | `ALIAS_ONLY` | One continuous Olympic Auditorium identity; Grand Olympic Auditorium is expanded/full-name treatment unless later evidence establishes otherwise. |
| `VEN-000430` | `ALIAS_ONLY` | One continuous Venice High School Gym identity; Gym/Gymnasium wording only. |
| `VEN-000431` | `ALIAS_ONLY` | One continuous Atlanta Auditorium identity; The Auditorium is shorthand. |
| `VEN-000432` | `ALIAS_ONLY` | One continuous Ballantine Gymnasium identity; Ballantine Gym is shorthand. |
| `VEN-000433` | `PERIODIZE` | Atlantic City Convention Hall → Boardwalk Hall → Jim Whelan Boardwalk Hall. Boardwalk Hall's official history fixes the 1929 building's Boardwalk Hall rename/reopening to 2001-10-11. New Jersey law designating `Jim Whelan Boardwalk Hall` became effective 2018-01-16, correcting the owner's October 2017 working boundary (the legislative approval process occurred in 2017). The modern Atlantic City Convention Center is a distinct facility that opened in 1997; do not treat it as the same physical venue. The existing VEN-000433 `Atlantic City Convention Center` row reflects pre-1997 source wording for the historic hall and should not remain as an unrestricted global alias if it could conflate later references to the separate modern convention center. |
| `VEN-000434` | `ALIAS_ONLY` | One continuous Charles E. Smith Center identity; Smith Center is shorthand. |
| `VEN-000435` | `ALIAS_ONLY` | One continuous College Avenue Gym identity; College Avenue Gymnasium and The Barn are aliases. |
| `VEN-000438` | `ALIAS_ONLY` | One continuous Galactic Ballroom at Moon Palace Resort identity; Moon Palace Resort is broader resort-level source wording. |
| `VEN-000439` | `RESEARCH_EXHAUSTED` | Owner closed the bounded residual as research exhausted. Rutgers institutional history establishes Highland Park Gym as its 1929-31 home (10-1), while contemporaneous New Brunswick reporting independently establishes a Masonic Hall basketball court in Highland Park during the same period. No authoritative source found in the bounded pass directly equates the two. Preserve them as unmerged identities/wording and do not manufacture equivalence. Reopen only if materially stronger archival evidence appears. |
| `VEN-000440` | `ALIAS_ONLY` | One continuous Jadwin Gymnasium identity; Jadwin Gym / Jadwin Fieldhouse are variants. |
| `VEN-000443` | `PERIODIZE` | Sears Centre → NOW Arena; Sears Centre Arena is first-era variant. |
| `VEN-000444` | `PERIODIZE` | Air Canada Centre → Scotiabank Arena. |
| `VEN-000445` | `ALIAS_ONLY` | One continuous South Padre Island Convention Center identity; Centre is spelling variant. |
| `VEN-000447` | `ALIAS_ONLY` | One continuous Brick Breeden Fieldhouse identity; Worthington Arena / Max Worthington Arena are competition-space names within the fieldhouse. |
| `VEN-000449` | `PERIODIZE` | McKeon Pavilion → University Credit Union Pavilion. |
| `VEN-000453` | `PERIODIZE` | Municipal Auditorium → Civic Center Music Hall. Oklahoma City's official facility history states the building opened in 1937 as Municipal Auditorium and, after the 1967 theatre-within-a-theatre renovation, became Civic Center Music Hall; City history confirms the current music hall is the shell of the original auditorium. Exact 1967 effective day remains implementation-date verification. |
| `VEN-000454` | `PERIODIZE` | Same-building formal history is resolved conceptually as Tulsa Assembly Center → James L. Maxwell Convention Center → Tulsa Convention Center → Cox Business Center → Cox Business Convention Center → Arvest Convention Center. City records show `Assembly Center` usage in 1981 and state that the civic center was renamed James L. Maxwell Convention Center in 1985; the City used Tulsa Convention Center before the 2013 Cox naming transaction. The 2013 naming-rights agreement renamed the facility Cox Business Center effective 2013-07-01. `Cox Business Convention Center` was a later formal wording, not a mere source variant: City records use it by 2020-21. Arvest naming became effective 2025-03-01. Exact Maxwell→Tulsa Convention Center and Cox Business Center→Cox Business Convention Center boundaries remain implementation-date verification. |
| `VEN-000457` | `PERIODIZE` | Convocation Center → BankUnited Center → Watsco Center. |
| `VEN-000458` | `PERIODIZE` | SIU Arena → Banterra Center. |
| `VEN-000459` | `ALIAS_ONLY` | One continuous Beeghly Center identity; Zidian Family Arena at Beeghly Center is a named competition-space/sponsor overlay. |
| `VEN-000460` | `ALIAS_ONLY` | One continuous Arsenal Technical High School identity; Tech H.S. / Arsenal Tech are aliases. |
| `VEN-000464` | `ALIAS_ONLY` | One continuous Ervin J. Nutter Center identity; Nutter Center is shorthand. |
| `VEN-000467` | `ALIAS_ONLY` | One continuous Coliseo Roberto Clemente identity; Roberto Clemente Coliseum is English translation. |
| `VEN-000470` | `ALIAS_ONLY` | One continuous John Gray Gymnasium identity; John Gray Gym is shorthand. |
| `VEN-000471` | `ALIAS_ONLY` | One continuous Coliseo de Puerto Rico / José Miguel Agrelot Coliseum identity; treat the formulations as same formal identity rather than successive periods. |
| `VEN-000474` | `PERIODIZE` | CU Fieldhouse → Balch Fieldhouse. Colorado Athletics states the 1937 building was known simply as the CU Fieldhouse in its early years and that its name was changed to Balch Fieldhouse in the 1976-77 season in honor of Roland E. Balch. Exact effective day remains implementation-date verification. |
| `VEN-000475` | `PERIODIZE` | Men’s Gymnasium → Carlson Gymnasium. The 1924 building opened as the Men’s Gymnasium and was renamed Carlson Gymnasium in 1976 for Harry Carlson. `Physical Education Building` is documented as an alternate/intervening functional reference but is not established in this bounded pass as a separate formal naming era, so retain it as alias/descriptor unless exact institutional evidence later proves otherwise. Exact 1976 effective day remains implementation-date verification. |
| `VEN-000485` | `ALIAS_ONLY` | One continuous Sun Devil Gymnasium identity; Sun Devil Gym is shorthand. |
| `VEN-000489` | `ALIAS_ONLY` | One continuous Jacksonville Veterans Memorial Coliseum identity; Jacksonville Memorial Coliseum / Jacksonville Coliseum are shortened variants unless later evidence establishes otherwise. |
| `VEN-000492` | `PERIODIZE` | Centennial Hall → Savage Hall → Savage Arena. |
| `VEN-000494` | `ALIAS_ONLY` | One continuous Iowa State Armory identity; The Armory is shorthand. |
| `VEN-000499` | `PERIODIZE` | AmericanAirlines Arena → FTX Arena → Miami-Dade Arena → Kaseya Center. Miami-Dade records show the American Airlines naming-rights contract expired 2019-12-31, but County documents still identified the facility itself as `AmericanAirlines Arena` until the FTX rebrand; contemporaneous reporting fixes the public FTX rename to 2021-06-04. After the FTX agreement was terminated, Miami-Dade County and the Heat made `Miami-Dade Arena` effective immediately on 2023-01-13. The County approved Kaseya naming on 2023-04-04. Treat the 2020-06/2021 continuation of AmericanAirlines Arena as the actual venue-name period despite the underlying sponsor contract having expired. |
| `VEN-000503` | `PERIODIZE` | DePaul Athletic Center → McGrath Arena → McGrath-Phillips Arena. DePaul game/facility evidence uses `DePaul Athletic Center` for the on-campus basketball venue from its 2000 opening through 2005-06; on 2006-07-22 the overall building became Sullivan Athletic Center and its gymnasium was formally named McGrath Arena. DePaul officially changed the arena name to McGrath-Phillips Arena on 2011-02-20. `Sullivan Athletic Center` is the surrounding building/complex name, not a separate arena period. |
| `VEN-000505` | `PERIODIZE` | Rochester Community War Memorial → Blue Cross Arena at the War Memorial. The arena opened 1955-10-18 as Rochester Community War Memorial. City/arena history records the 1998 naming transaction as `Blue Cross Arena at the War Memorial`; `Rochester War Memorial` is shorthand and `Blue Cross/Blue Shield Arena` is sponsor-derived/source wording rather than a distinct formal venue era. Exact 1998 valid_from should be fixed during implementation-date verification between the 1998-07-24 naming announcement and September rededication/reopening. |
| `VEN-000509` | `PERIODIZE` | The MARK of the Quad Cities → i wireless Center → TaxSlayer Center → Vibrant Arena at The MARK. The arena opened in May 1993 as The MARK; the i wireless change occurred in July 2007; TaxSlayer Center became official 2017-10-01; Vibrant Arena at The MARK became official 2022-09-01. The current registry omits the i wireless and TaxSlayer formal periods. Exact first-period opening day and capitalization/spacing should be normalized during implementation verification. |
| `VEN-000512` | `ALIAS_ONLY` | One continuous Buffalo Memorial Auditorium identity; Memorial Auditorium is shorthand. |
| `VEN-000513` | `ALIAS_ONLY` | Alumni Memorial Gymnasium is the historical basketball building identity. Duke confirms the 1922-23 gym remains the core of the present Brodie Recreation Center; a 31,000-square-foot addition was completed in 1996 and the entire expanded complex was renamed for H. Keith H. and Brenda Brodie. `Brodie Gym` is shorthand for that later recreation-center identity, not a basketball-era naming period for games played in Alumni Memorial Gymnasium. |
| `VEN-000514` | `ALIAS_ONLY` | One continuous Angier B. Duke Gymnasium identity; Angier Duke Gymnasium and The Ark are aliases/nickname. |
| `VEN-000515` | `ALIAS_ONLY` | One continuous Birmingham City Auditorium identity; Municipal Auditorium variants are shorthand/location-qualified forms. |
| `VEN-000516` | `ALIAS_ONLY` | One continuous Card Gymnasium identity; Card Gym is shorthand. |
| `VEN-000521` | `ALIAS_ONLY` | One pre-1930 Raleigh civic-auditorium identity: City Hall and Auditorium / Municipal Auditorium / City Auditorium / Raleigh Auditorium / Old City Auditorium are formal or descriptive variants of the 1910-11 Fayetteville-at-Davie building. NC State institutional and North Carolina architectural/archive evidence places early State basketball there and confirms the building burned in October 1930. Do not merge it with the distinct Memorial Auditorium completed in 1932 at South Street. No successive naming periods are established for VEN-000521. |
| `VEN-000522` | `ALIAS_ONLY` | One continuous Raleigh Memorial Auditorium identity; Memorial Auditorium and combined source wording are aliases. |
| `VEN-000523` | `ALIAS_ONLY` | One continuous War Memorial Gymnasium identity; War Memorial Gym is shorthand. |
| `VEN-000525` | `ALIAS_ONLY` | One continuous Alumni Hall identity; Navy Alumni Hall is institution-qualified wording. |
| `VEN-000526` | `ALIAS_ONLY` | One continuous Aoyama Gakuin Memorial Hall/Arena identity; English Hall/Arena renderings treated as translational variants rather than successive periods. |
| `VEN-000529` | `ALIAS_ONLY` | One continuous Bynum Gymnasium identity; Bynum Gym is shorthand. |
| `VEN-000531` | `PERIODIZE` | Carmichael Auditorium → Carmichael Arena. |
| `VEN-000538` | `ALIAS_ONLY` | One continuous Indoor Athletic Court identity; Tin Can is nickname. |
| `VEN-000539` | `ALIAS_ONLY` | One continuous James L. Knight Center identity; Knight Center is shorthand. |
| `VEN-000547` | `ALIAS_ONLY` | One continuous Roanoke City Auditorium identity; City Auditorium is shorthand. |
| `VEN-000552` | `ALIAS_ONLY` | One continuous Woollen Gymnasium identity; Woollen Gym is shorthand. |
| `VEN-000554` | `IDENTITY_RESOLVED` | Verified physical reconciliation after current-main rebase. VEN-000554 is the 1950 Rice Gymnasium building, whose competition space is Autry Court and whose later formal building name is Tudor Fieldhouse; `Rice Field House` must be removed from this identity. Current main already contains VEN-000564 / `rice-gymnasium`, but its only published use is the 1947-12-08 Texas–Texas Tech neutral game whose accepted source row says `Rice Gymnasium`, three years before the 1950 building opened. Rice institutional chronology identifies the pre-1950 campus indoor athletics building as the old Rice Field House. Therefore later dedicated maintenance should correct VEN-000564 to the old Rice Field House physical identity, preserve the 1947 `Rice Gymnasium` wording as source-era/local provenance rather than an unrestricted timeless alias, and preserve VEN-000554 for the 1950 Rice Gymnasium → Tudor Fieldhouse lineage with Autry Court as competition-space name. Historical identity: RESOLVED. Global registration cleanup: PENDING_DEDICATED_MAINTENANCE. |
| `VEN-000555` | `PERIODIZE` | Bossier City Arena → CenturyTel Center → CenturyLink Center → Brookshire Grocery Arena. The arena opened in 2000; CenturyTel held the original naming-rights relationship, the venue was rebranded CenturyLink Center under the successor agreement around 2010-11, and the Brookshire naming-rights agreement was signed 2020-12-09 for a term beginning 2021-01-01. Exact opening-era Bossier City Arena→CenturyTel and CenturyTel→CenturyLink effective days remain implementation-date verification. |
| `VEN-000557` | `PERIODIZE` | Deja Blue Arena at the Dr Pepper StarCenter → Dr Pepper Arena → Comerica Center. The original 2003 facility used the Deja Blue Arena name; after the 2008-09 expansion, Dr Pepper Arena opened 2009-06-01 and became the name of the entire complex. Comerica naming rights were announced 2019-01-18. `Comerica Arena` is an erroneous/source variant, not a formal period. |
| `VEN-000560` | `ALIAS_ONLY` | One continuous Delmar Fieldhouse identity; Delmar Gym is shorthand. |
| `VEN-000563` | `PERIODIZE` | Municipal Auditorium / Municipal Hall → Philadelphia Convention Hall. Philadelphia regional historical authority states the 1931 building opened as Municipal Hall/Auditorium and city officials renamed it Philadelphia Convention Hall in 1948. In 1952 the broader facility/complex became the Philadelphia Civic Center, but contemporaneous University of Pennsylvania usage decades later still says `Convention Hall at the Philadelphia Civic Center` / `Convention Hall, Civic Center`. Therefore `Philadelphia Civic Center` is a complex/location designation concurrent with the Convention Hall arena identity, not a third replacement arena-name period. Exact 1948 effective day remains implementation-date verification. |
| `VEN-000565` | `ALIAS_ONLY` | One continuous Tech Gym identity; The Barn is nickname. |
| `VEN-000570` | `ALIAS_ONLY` | One continuous Fair Park Recreation Building identity; Fair Park Rec. Center is shorthand/variant. |
| `VEN-000574` | `ALIAS_ONLY` | One continuous Civic Auditorium (San Francisco) identity; San Francisco / SF qualifiers are aliases. |
| `VEN-000576` | `PERIODIZE` | Patriot Center → EagleBank Arena. |
| `VEN-000578` | `PERIODIZE` | Everblades Arena → TECO Arena → Germain Arena → Hertz Arena. The 1998 opening-era venue was Everblades Arena; TECO/Peoples Gas acquired naming rights in 1999; Florida Everblades management announced Germain Arena on 2004-06-01; and the Germain→Hertz change became effective 2018-10-01. Exact 1999 Everblades→TECO effective day remains implementation-date verification. |
| `VEN-000580` | `PERIODIZE` | Lubbock Coliseum → City Bank Coliseum. |
| `VEN-000582` | `ALIAS_ONLY` | One continuous Einar Nielsen Fieldhouse identity; Nielsen Fieldhouse is shorthand. |
| `VEN-000583` | `ALIAS_ONLY` | One continuous Donald W. Reynolds Center identity; Reynolds Center is shorthand. |
| `VEN-000584` | `ALIAS_ONLY` | One continuous Sam Houston Coliseum identity; Houston Coliseum is shorthand. |
| `VEN-000585` | `PERIODIZE` | State Fair Arena → Jim Norick Arena. City of Oklahoma City states the arena debuted in September 1965 as State Fair Arena and was rechristened Jim Norick Arena in 1971. `State Farm Arena [BC source wording]` is erroneous source wording and must not become a naming period. Exact 1971 rechristening day remains implementation-date verification. |
| `VEN-000594` | `ALIAS_ONLY` | One continuous JSerra Pavilion identity; The Pavilion at JSerra is expanded form. |
| `VEN-000597` | `ALIAS_ONLY` | One continuous Robertson Memorial Fieldhouse identity; Memorial Field House is shorthand. |
| `VEN-000600` | `ALIAS_ONLY` | One continuous Ladies/Women’s Gymnasium identity; Old Ladies Gymnasium is retrospective descriptor rather than a separate period. |
| `VEN-000602` | `PERIODIZE` | Prescott Valley Event Center → Tim’s Toyota Center → Findlay Toyota Center. |
| `VEN-000605` | `PERIODIZE` | Glens Falls Civic Center → Cool Insuring Arena → Harding Mazzotti Arena. |
| `VEN-000606` | `PERIODIZE` | Toso Pavilion → Leavey Center; Harold J. Toso Pavilion and Leavey Event Center are variants within those eras. |
| `VEN-000615` | `ALIAS_ONLY` | One continuous Omaha Civic Auditorium identity; Civic Auditorium is shorthand. |
| `VEN-000616` | `ALIAS_ONLY` | One continuous Perkins Gymnasium identity; Perkins Gym is shorthand. |
| `VEN-000618` | `ALIAS_ONLY` | One continuous Tucson Arena identity for the arena itself. The arena opened in 1971 as a venue within the surrounding Tucson Community Center; the broader complex later became the Tucson Convention Center (commonly dated to 2002). Current official TCC material distinguishes the Tucson Convention Center complex from its interior `Tucson Arena`. `Tucson Community Center Arena` and `Tucson Convention Center Arena` are complex-qualified source forms, not successive formal arena names. No arena naming periods are warranted. |
| `VEN-000634` | `ALIAS_ONLY` | One continuous Norfolk Scope identity; Scope / Norfolk Scope Arena are aliases. |
| `VEN-000637` | `ALIAS_ONLY` | One continuous Encina Gymnasium identity; Encina Gym is shorthand. |
| `VEN-000654` | `PERIODIZE` | Charleston Civic Center → Charleston Coliseum & Convention Center; Charleston Coliseum is shorthand/current arena wording. |
| `VEN-000673` | `ALIAS_ONLY` | One continuous WVU Armory identity; ROTC Armory / Armory are aliases unless later evidence establishes a formal rename. |
| `VEN-000674` | `ALIAS_ONLY` | One continuous Armory Fieldhouse identity. University of Cincinnati Athletics states the facility opened 1954-12-18 as Armory Fieldhouse and consistently treats that as the historical basketball venue name. `UC Fieldhouse` is source/institutional shorthand rather than a verified formal predecessor name; no naming-period conversion is warranted. |
| `VEN-000683` | `CANONICAL_CORRECTION` | Verified mechanical duplicate: protected main contains two literal `Orange County Civic Center` rows for VEN-000683, one PROJECT_DISPLAY and one HISTORICAL_OR_ALIAS, with the same normalized name and no distinct historical-name claim. This is one naming identity; later registry cleanup should remove the redundant alias row only. No periodization or historical adjudication is required. |
| `VEN-000695` | `ALIAS_ONLY` | One continuous Devlin Fieldhouse identity; Avron B. Fogelman Arena is the named competition space within the same building. |
| `VEN-000708` | `ALIAS_ONLY` | One continuous Memorial Coliseum (Winston-Salem) identity; W-S Coliseum is shorthand. |
| `VEN-000709` | `ALIAS_ONLY` | One continuous Montego Bay Convention Center identity; Centre is spelling variant. |
| `VEN-000710` | `ALIAS_ONLY` | One continuous R.J. Reynolds High School identity; Reynolds HS / Reynolds High School are aliases. |
| `VEN-000711` | `PERIODIZE` | Murray State Sports Arena → Racer Arena. Murray State Athletics explicitly identifies Murray State Sports Arena as the original arena name before Racer Arena. Separate institutional facility evidence establishes that in 1993 the building housing Racer Arena was named Cutchin Fieldhouse; current Murray State campus material still describes Cutchin Fieldhouse as housing Racer Arena. Therefore `Carlisle Cutchin Fieldhouse` is the enclosing building name, not a third replacement arena-name period, and `Racer Arena/Carlisle Cutchin Fieldhouse` is expanded combined facility wording. Exact Sports Arena→Racer Arena effective boundary remains implementation-date verification. |
| `VEN-000712` | `ALIAS_ONLY` | One continuous Wake Forest College Gymnasium identity; Gymnasium / old Gymnasium are descriptive variants. |
| `VEN-000715` | `ALIAS_ONLY` | One continuous Fike Field House identity; Clemson Field House is alias. |
| `VEN-000716` | `ALIAS_ONLY` | One continuous Holtzendorff YMCA identity; YMCA Building / YMCA are shorthand. |
| `VEN-000729` | `PERIODIZE` | Arena at Gwinnett Center → Infinite Energy Arena → Gas South Arena. The arena opened in February 2003 as Arena at Gwinnett Center. Infinite Energy acquired naming rights in August 2015, formally creating Infinite Energy Arena. Gas South announced the immediate rebrand to Gas South Arena on 2021-05-25 after acquiring Infinite Energy. Exact 2015 effective day/signage transition remains implementation-date verification if required. |
| `VEN-000736` | `ALIAS_ONLY` | One continuous Rafael A. Mangual Coliseum identity; Spanish/English ordering only. |
| `VEN-000737` | `ALIAS_ONLY` | One continuous Poliforum Benito Juárez identity; Poliforum Cancún is alternate/local shorthand. |
| `VEN-000742` | `ALIAS_ONLY` | One continuous Minges Coliseum identity; Williams Arena is the named competition space within Minges Coliseum. |
| `VEN-000743` | `ALIAS_ONLY` | One continuous Trees Gymnasium identity; Trees Gym is shorthand. |
| `VEN-000748` | `ALIAS_ONLY` | One continuous Rose Hill Gymnasium identity; Fordham Gym is institutional shorthand. |
| `VEN-000749` | `PERIODIZE` | Philadelphia Auditorium and Ice Palace → The Arena / Philadelphia Arena → Martin Luther King Jr. Arena. University of Pennsylvania's West Philadelphia Collaborative History states the building opened 1920-02-14 as `Philadelphia Auditorium and Ice Palace` and new ownership renamed it `The Arena` in 1927, correcting the owner's 1925 working year. The final owners rechristened it Martin Luther King Jr. Arena in 1980; its reopening under that name was 1980-06-20. `Philadelphia Arena` is the location-qualified/common form of the long `The Arena` era, not another separate naming period. |
| `VEN-000750` | `ALIAS_ONLY` | One continuous Archbold Gymnasium identity; Archbold Gym is shorthand. |
| `VEN-000753` | `ALIAS_ONLY` | Manley Field House is the historical basketball venue identity. Syracuse says Manley opened in 1962 and hosted men's basketball until the Carrier Dome era. Beginning in 2022, Syracuse undertook a multi-phase transformation of Manley Field House together with the surrounding Lampe athletics facilities into the larger John A. Lally Athletics Complex; Athletics declared the new complex name official on 2022-07-01. This is a post-basketball larger-complex transformation/designation, not a historical basketball-venue rename. Preserve `John A. Lally Athletics Complex` as later site/complex continuity, not an OFFICIAL_NAMING_PERIOD for Manley basketball games. |
| `VEN-000754` | `ALIAS_ONLY` | Syracuse University Archives states the 1891-92 building was first called the `Gymnasium and YMCA Building` / Gymnasium and housed both men's and women's athletics. When men moved to Archbold Gymnasium in 1909, the old building became known as the Women's Gymnasium or Old Gym. Men's basketball therefore belongs to the original Gymnasium-era building identity; `Women's Gymnasium` / `Old Gym` are later-use or retrospective names after the men's program left. Do not create a post-1909 basketball naming period. |
| `VEN-000755` | `PERIODIZE` | State Fair Coliseum → Toyota Coliseum; New York State Fair Coliseum / Fairgrounds Coliseum are expanded first-era forms. |
| `VEN-000757` | `PERIODIZE` | Onondaga County War Memorial → Oncenter War Memorial Arena / War Memorial at OnCenter → Upstate Medical University Arena at Onondaga County War Memorial. The arena opened in 1951 as the Onondaga County War Memorial. Contemporary 2000 event usage establishes `War Memorial at OnCenter` / `Oncenter War Memorial Arena` by that year, consistent with the accepted 2000-era Oncenter branding, but the exact first effective day was not established in this bounded pass and remains implementation-date verification. Upstate Medical University and Onondaga County announced the 11-year naming-rights agreement on 2019-12-20; current operator usage confirms the sponsored arena name. For mobile display, `Upstate Medical University Arena` may be used as the shortened display form while preserving the full formal period name in authority data if repository policy supports it. |
| `VEN-000761` | `ALIAS_ONLY` | One continuous West Jefferson Street Armory identity; Jefferson Street Armory is shorthand. |
| `VEN-000766` | `PERIODIZE` | Boston Arena → Matthews Arena. |
| `VEN-000778` | `PERIODIZE` | Cumberland County Civic Center → Cross Insurance Arena. The county-owned arena opened in 1977 under the Cumberland County Civic Center name; naming rights were sold on 2014-06-18 and the building was renamed Cross Insurance Arena. `Portland Civic Center` is shorthand/location wording rather than a separate formal era. |
| `VEN-000779` | `ALIAS_ONLY` | One continuous Percy Hedgecock Gymnasium identity; Hedgecock Gym is shorthand. |
| `VEN-000781` | `PERIODIZE` | Arena at Harbor Yard → Webster Bank Arena at Harbor Yard → Total Mortgage Arena. The Bridgeport venue opened in 2001 as Arena at Harbor Yard. Webster Bank's naming-rights agreement became effective immediately in January 2011, formally producing `Webster Bank Arena at Harbor Yard`; shortened `Webster Bank Arena` is an alias of that era. Total Mortgage Arena became effective immediately on 2022-03-07. |
| `VEN-000785` | `ALIAS_ONLY` | One continuous Calumet Club identity; parenthetical locality is disambiguation only. |
| `VEN-000786` | `ALIAS_ONLY` | One continuous Coast Guard Air Station Borinquen Hangar identity; CGAS/U.S. Coast Guard expansions are aliases. |
| `VEN-000787` | `ALIAS_ONLY` | One continuous Louisville Elks Club identity; article-only variation. |
| `VEN-000788` | `ALIAS_ONLY` | Same physical 1926 building, but the chronology is opposite the registry implication: Spencer Memorial Gymnasium was Kentucky Wesleyan's basketball-era name from 1926-1951; after KWC left Winchester, the former campus became College Park and the gym later became known as College Park Gym. KWC itself explicitly describes the present College Park Gym as the former Spencer Memorial Gymnasium. Treat `College Park Gym` as later post-KWC building-use/location continuity, not a predecessor basketball naming period. |
| `VEN-000789` | `ALIAS_ONLY` | One continuous Belknap Campus Gym identity; UofL / Gymnasium variants are aliases. |
| `VEN-000790` | `ALIAS_ONLY` | One continuous Weaver Health Building identity; Weaver Gymnasium / Weaver Gym describe basketball use/space rather than a separate naming era. |
| `VEN-000791` | `ALIAS_ONLY` | One continuous Health & Physical Education Building identity for basketball purposes; Helm Library building is later-use physical-building locator, not a basketball naming period. |
| `VEN-000792` | `ALIAS_ONLY` | One continuous Coliseo Guillermo Angulo identity; Guillermo Arena is translated shorthand and Angul is truncation/typo. |
| `VEN-000794` | `ALIAS_ONLY` | One continuous Dallas YMCA (Commerce Street) identity; Y.M.C.A. is typography variant. |
| `VEN-000796` | `ALIAS_ONLY` | One continuous SMU Basketball Pavilion identity; Basketball Pavilion is shorthand. |
| `VEN-000797` | `ALIAS_ONLY` | One continuous SMU Gymnasium identity; SMU Gym is shorthand. |
| `VEN-000804` | `ALIAS_ONLY` | One continuous Carroll Hall Gym identity; Carroll gym is shorthand. |
| `VEN-000808` | `ALIAS_ONLY` | One continuous Marquette Gymnasium identity; Marquette Gym is shorthand. |
| `VEN-000809` | `ALIAS_ONLY` | One continuous original Notre Dame Fieldhouse physical identity; Fieldhouse / original Notre Dame Fieldhouse are disambiguation variants. Keep distinct from VEN-000810. |
| `VEN-000810` | `ALIAS_ONLY` | One continuous rebuilt Notre Dame Fieldhouse physical identity; Old Fieldhouse is retrospective shorthand. Keep distinct from VEN-000809. |
| `VEN-000815` | `PERIODIZE` | University Gym → Joseph J. Vinardi Center. Creighton institutional history states the 1915/16 building opened as University Gym and that this is the same physical building now known as Vinardi Center. `Old Gym` / `Old Gymnasium` are informal retrospective names. Creighton's formal campus-building style guide identifies the official current name as `Joseph J. Vinardi Center`; `Vinardi Athletic Center` is athletics/functional expanded wording rather than a separately established formal naming era. First-party evidence confirms Vinardi usage by the 1991-92 season but this bounded pass did not establish the exact University Gym→Vinardi effective date, which remains implementation-date verification. |
| `VEN-000819` | `PERIODIZE` | JQH Arena → Great Southern Bank Arena. |
| `VEN-000821` | `ALIAS_ONLY` | One continuous Al McGuire Center identity; The Al is nickname. |
| `VEN-000823` | `PERIODIZE` | RPI Field House → Livingston W. Houston Field House / Houston Field House. RPI Institute Archives identifies the 1949 physical field-house building and preserves records explicitly concerning the 1978 renaming of the RPI Field House for former president Livingston W. Houston. RPI Athletics fixes the transition to the 1978 Commencement on 1978-05-26, when it was announced the building would henceforth be known as Houston Field House. `Rensselaer Polytechnic Institute Field House` is an expanded first-era form and `RPI Field House (Houston Field House)` is combined retrospective wording, not another period. |
| `VEN-000825` | `ALIAS_ONLY` | One continuous St. Xavier College Gym identity; St. Xavier Gym is shorthand. |
| `VEN-000826` | `ALIAS_ONLY` | One continuous Middletown High School (Girard Avenue) identity; Girard Avenue is physical-campus disambiguation. |
| `VEN-000838` | `ALIAS_ONLY` | One continuous Alumni Hall (Providence) identity; Providence College qualifier is alias. |
| `VEN-000839` | `ALIAS_ONLY` | One continuous St. John’s College Gymnasium identity; Lewis Avenue qualifier and shorter St. John’s Gym forms are aliases. |
| `VEN-000840` | `ALIAS_ONLY` | One continuous DeGray Gymnasium identity; DeGray Gym is shorthand. |
| `VEN-000858` | `ALIAS_ONLY` | One continuous West Catholic High School Gymnasium identity; school-only form is shorthand. |
| `VEN-000859` | `ALIAS_ONLY` | One continuous Alumni Hall (Villanova) identity; Alumni Gym / Villanova Alumni Hall are aliases. |
| `VEN-000860` | `PERIODIZE` | Villanova Field House → Jake Nevin Field House. Villanova Athletics fixes the history exactly: the building opened 1932-04-01 as Villanova Field House and was renamed for John `Jake` Nevin on 1985-11-22. `The John Jake Nevin Field House` is expanded/formalized wording of the second era, not another period. |
| `VEN-000861` | `PERIODIZE` | Sovereign Bank Arena → Sun National Bank Center → CURE Insurance Arena. |
| `VEN-000863` | `PERIODIZE` | A.J. Palumbo Center → UPMC Cooper Fieldhouse, with a genuine 2019-2021 closure/renovation gap. Duquesne describes the project as a comprehensive renovation/re-imagination of the A.J. Palumbo Center, begun in March 2019, and later says UPMC Cooper Fieldhouse is the formerly named Palumbo Center reopened after that renovation. The final Palumbo basketball game was 2019-03-09; the renovated UPMC Cooper Fieldhouse hosted its first game on 2021-02-02. Treat this as one physical venue lineage under the repository one-building rule, not a replacement venue; exact naming valid_from semantics during the closure can use reopening/first-event evidence at implementation rather than inventing an operational period when no games occurred. |

## Future protocol agreed in principle

After the legacy cleanup is complete, repository policy should require a bounded **full naming-history review at first global registration of every newly discovered physical venue**:

1. establish physical continuity;
2. identify the complete formal naming chronology, including eras absent from the triggering school source;
3. preserve aliases/abbreviations/nicknames/court names/complex names separately from formal periods;
4. verify exact effective boundaries from authoritative sources when supported;
5. record an explicit disposition even when the result is one continuous name / aliases only;
6. do not expand source-school responsibility into opponent-home venue archaeology merely because an opponent venue is encountered;
7. enforce the naming-history disposition when the venue is globally registered/reconciled.

The final permanent policy should be linked from `AGENTS.md`, `docs/historical-venue-name-display.md`, and the relevant Research/Implementation venue-authoring workflow so future lanes do not recreate this cleanup.

## Remaining census obligations

- Multi-name ambiguity research is complete. The three surviving unresolved cases are explicitly owner-accepted `RESEARCH_EXHAUSTED` residuals and must not be reopened absent materially stronger evidence.
- Verify exact transition dates for approved periodized histories where the ledger still marks date verification as pending.
- Continue the agreed **light high-yield screen of the 483 single-name venues** for obvious missing historical rename histories. The repository-internal cross-check is complete; screening tranches 1-2 have screened 17 venues and found 11 positive candidates, with 6 clear on the current light pass. This is not permission for 483 deep research campaigns.
- After that screen, finalize rollout tranches and implement approved naming periods / shared-reference cleanups in bounded maintenance PRs under current repository policy.
