# Historical venue-name census

Status: **MULTI-NAME CENSUS COMPLETE — RESEARCH QUEUE PENDING**  
Protected-main baseline: `3f9edc3de0237fde453a87000cf6755b97962687`

This file preserves the owner-adjudicated state of the repository-wide historical physical-venue naming census. It is a recovery artifact and working ledger, not yet the final permanent protocol. It does not itself create `OFFICIAL_NAMING_PERIOD` rows.

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
| `VEN-000013` | `RESEARCH_HOLD` | Research full Sacramento chronology. ARCO Arena II is building disambiguation, not a period. Working expectation includes ARCO Arena → Power Balance Pavilion → Sleep Train Arena. |
| `VEN-000018` | `PERIODIZE` | Pepsi Center → Ball Arena. |
| `VEN-000019` | `RESEARCH_HOLD` | Baltimore registry is incomplete; research full formal chronology before owner periodization. |
| `VEN-000023` | `RESEARCH_HOLD` | Determine whether NU Sports Complex was a genuine predecessor name of Bob Devaney Sports Center or source shorthand. |
| `VEN-000025` | `PERIODIZE` | BI-LO Center → Bon Secours Wellness Arena; The Well is alias only. |
| `VEN-000028` | `PERIODIZE` | Brendan Byrne Arena → Continental Airlines Arena → IZOD Center → Meadowlands Arena; Meadowlands is alias only. |
| `VEN-000031` | `PERIODIZE` | Gaylord Entertainment Center → Sommet Center → Bridgestone Arena; Gaylor Entertainment Center is typo only. |
| `VEN-000034` | `PERIODIZE` | Louisiana Superdome → Mercedes-Benz Superdome → Caesars Superdome; Superdome is alias only. |
| `VEN-000035` | `PERIODIZE` | Duke Indoor Stadium → Cameron Indoor Stadium. |
| `VEN-000036` | `PERIODIZE` | MCI Center → Verizon Center → Capital One Arena. |
| `VEN-000038` | `RESEARCH_HOLD` | Research full UCF chronology; working expectation UCF Arena → CFE Arena → Addition Financial Arena. |
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
| `VEN-000076` | `RESEARCH_HOLD` | Research whether Greensboro Memorial Coliseum was an earlier formal name and reconcile Greensboro Coliseum / First Horizon Coliseum chronology. |
| `VEN-000078` | `ALIAS_ONLY` | One continuous Hec Edmundson Pavilion identity; Bank of America Arena / Alaska Airlines Arena treated as sponsor overlays. |
| `VEN-000080` | `PERIODIZE` | Butler Fieldhouse → Hinkle Fieldhouse. |
| `VEN-000082` | `PERIODIZE` | Arrowhead Pond of Anaheim → Honda Center; Arrowhead Pond / The Pond are aliases. |
| `VEN-000083` | `PERIODIZE` | Hoosier Dome → RCA Dome; Indiana Hoosier Dome alias. |
| `VEN-000084` | `PERIODIZE` | Disney’s Milk House → HP Field House → State Farm Field House. |
| `VEN-000095` | `PERIODIZE_RESEARCH` | Multiple Rutgers formal periods; research exact Rutgers Athletic Center / Louis Brown Athletic Center / any RAC reversion / Jersey Mike’s Arena chronology. |
| `VEN-000096` | `MIGRATED` | Carrier Dome → JMA Wireless Dome. Production-verified. |
| `VEN-000097` | `PERIODIZE` | Special Events Center → Jon M. Huntsman Center. U. of U. Special Events Center / Huntsman Center / Jon Huntsman Center are aliases. Owner working history: opened 1969, renamed 1987; exact boundary to verify. |
| `VEN-000098` | `PERIODIZE` | Athletic and Convocation Center → Joyce Center; Purcell Pavilion is competition-space/branding alias only. |
| `VEN-000099` | `PERIODIZE` | Kemper Arena → Hy-Vee Arena. |
| `VEN-000103` | `PERIODIZE` | HSBC formal era → First Niagara Center → KeyBank Center; determine whether HSBC Arena or HSBC Center was the formal wording. |
| `VEN-000106` | `ALIAS_ONLY` | One continuous Downtown YMCA / Knoxville YMCA Gymnasium identity. |
| `VEN-000109` | `RESEARCH_HOLD` | Distinguish true arena names from BJCC complex/source shorthand before owner periodization. |
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
| `VEN-000176` | `RESEARCH_HOLD` | Research Cincinnati formal sequence and determine status of The Crown before owner ruling. |
| `VEN-000179` | `PERIODIZE` | Gund Arena → Quicken Loans Arena → Rocket Mortgage FieldHouse → Rocket Arena. |
| `VEN-000183` | `PERIODIZE` | San Jose Arena → Compaq Center at San Jose → HP Pavilion → SAP Center. |
| `VEN-000185` | `PERIODIZE_RESEARCH` | Alltel Arena → Verizon Arena → Simmons Bank Arena; current registry omits Verizon era, so verify full chronology. |
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
| `VEN-000204` | `PERIODIZE_RESEARCH` | Trans World Dome → Edward Jones Dome → The Dome at America’s Center; current registry omits Trans World Dome. |
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
| `VEN-000524` | `RESEARCH_HOLD` | Research exact WVU Field House / Stansbury Hall chronology and whether Mountaineer Field House is alias only. Owner supplied working fact: opened 1929 as WVU Field House; basketball moved to WVU Coliseum in 1970. |
| `VEN-000701` | `PERIODIZE` | duPont Pavilion → Finneran Pavilion; The Pavilion / Pavilion / PV / FPV are aliases of applicable eras. |
| `VEN-000828` | `RESEARCH_HOLD` | Research relationship among The Cage, The Hangar/Hanger, Basketball Hangar, and Quonset Hut before owner ruling. |
| `VEN-000829` | `PERIODIZE_RESEARCH` | Field House family → Hugh S. Greer Field House; verify the exact formal first-era name among UConn Field House / Storrs Field House. |

| `VEN-000002` | `ALIAS_ONLY` | One continuous Alamodome identity; Alamaodome is typo only. |
| `VEN-000007` | `ALIAS_ONLY` | One continuous Alumni Gym identity; Alumni Gymnasium / Alumni Memorial Auditorium-Gymnasium / Alumni Memorial Gym are formal/descriptive variants, not separate eras. |
| `VEN-000012` | `PERIODIZE` | Amway Center → Kia Center. |
| `VEN-000020` | `ALIAS_ONLY` | One continuous Barclays Center identity; Brooklyn, NY / Barclays Center is location-decorated source text. |
| `VEN-000026` | `PERIODIZE` | Bradley Center → BMO Harris Bradley Center. |
| `VEN-000029` | `ALIAS_ONLY` | One continuous Breslin Center identity; Jack Breslin Student Events Center is the expanded formal name. |
| `VEN-000037` | `ALIAS_ONLY` | One continuous Carver-Hawkeye Arena identity; dash typography variant only. |
| `VEN-000040` | `RESEARCH_HOLD` | Research full formal chronology of the 1955 Charlotte Coliseum building, including Independence Arena / Bojangles Coliseum and any omitted eras, before periodization. |
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
| `VEN-000102` | `IDENTITY_RECONCILE` | Owner ruling: KeyArena lineage and VEN-000315 Climate Pledge Arena are one physical Seattle Center arena identity. Later shared-reference implementation must reconcile to one surviving global venue_id and research complete naming chronology. |
| `VEN-000315` | `IDENTITY_RECONCILE` | Owner ruling: Climate Pledge Arena and VEN-000102 KeyArena lineage are one physical Seattle Center arena identity. Later shared-reference implementation must reconcile to one surviving global venue_id and research complete naming chronology. |
| `VEN-000123` | `ALIAS_ONLY` | One continuous Madison Square Garden III physical-building identity; MSG III / Old Madison Square Garden / 1925-building variants are disambiguation or shorthand only. |
| `VEN-000124` | `ALIAS_ONLY` | One continuous Madison Square Garden IV physical-building identity; MSG IV / 1968-building variants are disambiguation or shorthand only. |
| `VEN-000126` | `ALIAS_ONLY` | One continuous McArthur Court identity; Mac Court is nickname/shorthand. |
| `VEN-000129` | `ALIAS_ONLY` | One continuous Memorial Coliseum (Lexington) identity; location-qualified variants only. |
| `VEN-000143` | `ALIAS_ONLY` | One continuous Municipal Auditorium (Kansas City) identity; city-qualified variants only. |
| `VEN-000146` | `PERIODIZE_RESEARCH` | Myriad Convention Center → Cox Center; verify the exact formal second-era name/boundary before implementation. The Myriad / Myriad Center are aliases of the first era. |
| `VEN-000151` | `ALIAS_ONLY` | One continuous New Gymnasium identity; The New Gym is shorthand. |
| `VEN-000153` | `RESEARCH_HOLD` | Research full Oakland Coliseum Arena naming chronology before periodization; current registry omits major formal eras such as Oracle Arena. |
| `VEN-000155` | `ALIAS_ONLY` | One continuous Old Gym identity; Vanderbilt Old Gym is location/institution-qualified form. |
| `VEN-000157` | `ALIAS_ONLY` | One continuous Omni Coliseum identity; The Omni / Omni are shorthand. |
| `VEN-000158` | `PERIODIZE` | Orlando Arena → TD Waterhouse Centre → Amway Arena. |
| `VEN-000159` | `ALIAS_ONLY` | One continuous Palestra identity; The Palestra is article-prefixed variant. |
| `VEN-000160` | `RESEARCH_HOLD` | Resolve Patton Gymnasium vs Patten Gymnasium as a canonical spelling/history issue; do not create separate periods unless authoritative evidence establishes them. |
| `VEN-000163` | `PERIODIZE` | LSU Assembly Center → Pete Maravich Assembly Center; Maravich Assembly Center / Assembly Center are aliases. |
| `VEN-000170` | `ALIAS_ONLY` | One continuous Prudential Center identity; Newark, NJ / Prudential Center is location-decorated source text. |
| `VEN-000177` | `ALIAS_ONLY` | One continuous Roberts Municipal Stadium identity; Roberts Stadium is shorthand. |
| `VEN-000182` | `RESEARCH_HOLD` | Research San Diego Sports Arena full naming chronology and remove erroneous Cox Arena/Viejas cross-venue aliasing only after physical-identity verification. |
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
| `VEN-000234` | `RESEARCH_HOLD` | Research Worcester Centrum / DCU Center full chronology before periodization; registry may omit or collapse formal intermediate wording. |
| `VEN-000235` | `PERIODIZE` | WVU Coliseum → Hope Coliseum. Owner explicitly rules these as two distinct periods. |
| `VEN-000238` | `PERIODIZE` | USF Sun Dome → Yuengling Center; Sun Dome is alias/short form of first era. |
| `VEN-000240` | `ALIAS_ONLY` | One continuous C.M. “Tad” Smith Coliseum identity; Tad Smith Coliseum is shortened form. |
| `VEN-000241` | `PERIODIZE` | Civic Arena → Mellon Arena; Pittsburgh Civic Arena is location-qualified first-era alias. |
| `VEN-000248` | `PERIODIZE` | Jefferson County Armory → Louisville Convention Center → Louisville Gardens, subject to exact continuity/boundary verification; The Armory is alias. |
| `VEN-000249` | `PERIODIZE` | Alexander Memorial Coliseum → McCamish Pavilion. |
| `VEN-000250` | `RESEARCH_HOLD` | Determine whether New Gym was contemporary shorthand or a genuine formal predecessor of McCarthy Gymnasium before periodization. |
| `VEN-000259` | `PERIODIZE` | Capital Centre → USAir Arena. |
| `VEN-000267` | `ALIAS_ONLY` | One continuous Baha Mar Convention Center identity; Baha Mar Convention, Arts & Entertainment Center is expanded/formal wording rather than a separate era. |
| `VEN-000270` | `ALIAS_ONLY` | One continuous John M. Parker Agricultural Coliseum identity; Cow Palace is a nickname/source alias. |
| `VEN-000271` | `RESEARCH_HOLD` | Determine whether The Arena at Northwest Florida State College → Raider Arena was a true formal rename or alternate branding. |
| `VEN-000272` | `ALIAS_ONLY` | One continuous Conte Forum identity; Silvio O. Conte Forum is the full formal name. |
| `VEN-000274` | `ALIAS_ONLY` | One continuous Atlanta Municipal Auditorium identity; Municipal Auditorium / City Auditorium are source shorthand. |
| `VEN-000275` | `ALIAS_ONLY` | One continuous Athens YMCA identity; Old Athens YMCA is descriptive alias. |
| `VEN-000276` | `PERIODIZE` | Memorial Hall → Alumni Hall. |
| `VEN-000277` | `ALIAS_ONLY` | One continuous The Octagon identity; Octagon is shorthand. |
| `VEN-000280` | `PERIODIZE` | Carolina First Arena → TD Arena. |
| `VEN-000292` | `ALIAS_ONLY` | One continuous Armory identity; The Armory is alias. |
| `VEN-000296` | `RESEARCH_HOLD` | Determine whether Kansas Coliseum is the overall complex and Britt Brown Arena the basketball arena inside it rather than a historical rename. |
| `VEN-000301` | `ALIAS_ONLY` | One continuous Allen County War Memorial Coliseum identity; War Memorial Coliseum / FW Memorial Coliseum are shorthand. |
| `VEN-000302` | `PERIODIZE` | Alumni Memorial Fieldhouse → Hagan Arena. |
| `VEN-000303` | `ALIAS_ONLY` | One continuous Bryce Jordan Center identity; BJC / Bryce Center are aliases. |
| `VEN-000305` | `ALIAS_ONLY` | One continuous Keaney Gymnasium identity; Keaney Gym is shorthand. |
| `VEN-000306` | `ALIAS_ONLY` | One continuous Matthew Knight Arena identity; Matt Knight Arena / MKA are aliases. |
| `VEN-000307` | `ALIAS_ONLY` | One continuous Penn State Armory identity; The Armory is shorthand. |
| `VEN-000308` | `RESEARCH_HOLD` | Determine whether Recreation Building → Recreation Hall / Rec Hall represents a true formal rename or interchangeable wording. |
| `VEN-000309` | `ALIAS_ONLY` | One continuous The Hazell Center identity; Hazell Center is article-only variant. |
| `VEN-000310` | `ALIAS_ONLY` | One continuous Grant Memorial Hall identity; Grant Hall is shorthand. |
| `VEN-000311` | `ALIAS_ONLY` | One continuous State Fairgrounds Coliseum identity; Nebraska State Fairgrounds Coliseum is institution/location-qualified form. |
| `VEN-000312` | `ALIAS_ONLY` | One continuous Nebraska Coliseum identity; NU Coliseum is shorthand. |
| `VEN-000316` | `RESEARCH_HOLD` | Research full Hershey Park Arena / Hershey Arena naming chronology before periodization; current registry may omit a genuine earlier formal arena name. |
| `VEN-000318` | `ALIAS_ONLY` | One continuous Loyola Field House identity; Loyola University Fieldhouse is expanded institutional wording/spelling variant. |
| `VEN-000324` | `CANONICAL_CORRECTION` | One physical Richmond venue; proper canonical name is Robins Center. Robbins Center is erroneous variant, not a naming period. |
| `VEN-000325` | `PERIODIZE` | Special Events Center → Don Haskins Center; Haskins Center is shorthand of second era. |
| `VEN-000326` | `PERIODIZE` | Springfield Civic Center → MassMutual Center; Springfield CC is shorthand of first era. |
| `VEN-000328` | `ALIAS_ONLY` | One continuous Frank Thompson Gymnasium identity; Thompson Gym / Frank Thompson Gym are shortened forms. |
| `VEN-000329` | `PERIODIZE` | Virginia Tech Coliseum → Cassell Coliseum. |
| `VEN-000335` | `ALIAS_ONLY` | One continuous Gregory Gymnasium identity; Gregory Gym is shorthand. |
| `VEN-000338` | `ALIAS_ONLY` | One continuous Men’s Gym identity; University Men’s Gym is expanded institutional form. |
| `VEN-000339` | `PERIODIZE` | UIC Pavilion → Credit Union 1 Arena. |
| `VEN-000342` | `ALIAS_ONLY` | One continuous R.O.T.C. Armory identity; ROTC Armory is punctuation-only variant. |
| `VEN-000343` | `ALIAS_ONLY` | One continuous Mississippi Coliseum identity; The Big House is nickname. |
| `VEN-000344` | `RESEARCH_HOLD` | Determine whether Frank McGuire Arena is a competition-space/court name or erroneous cross-venue alias rather than a Carolina Coliseum rename. |
| `VEN-000346` | `RESEARCH_HOLD` | Research Carolina Gymnasium / Longstreet Theater chronology and later reuse before deciding whether post-basketball naming belongs in the period model. |
| `VEN-000347` | `ALIAS_ONLY` | One continuous Coliseo Rubén Rodríguez identity; Ruben Rodriguez Coliseum is English/transliteration variant. |
| `VEN-000348` | `ALIAS_ONLY` | One continuous Colonial Hall identity; Colonial Hall at The Greenbrier is resort-qualified form. |
| `VEN-000349` | `PERIODIZE_RESEARCH` | Research full Glendale arena chronology; current registry has Gila River Arena → Desert Diamond Arena but likely omits earlier Glendale Arena / Jobing.com Arena eras. |
| `VEN-000350` | `PERIODIZE_RESEARCH` | Research Shoemaker Center → Fifth Third Arena chronology and determine whether Fifth Third Arena at Shoemaker Center is retained-building wording rather than another era. |
| `VEN-000351` | `ALIAS_ONLY` | One continuous Gampel Pavilion identity; Harry A. Gampel Pavilion is full formal name. |
| `VEN-000352` | `ALIAS_ONLY` | One continuous Hard Rock Hotel Riviera Maya Convention Center identity; ballroom/resort variants are descriptive source wording. |
| `VEN-000353` | `RESEARCH_HOLD` | Distinguish Harrah’s Cherokee Center complex naming from ExploreAsheville.com Arena interior-arena naming before periodization. |
| `VEN-000356` | `ALIAS_ONLY` | One continuous Orleans Arena identity; article/hotel-qualified variants are aliases. |
| `VEN-000358` | `ALIAS_ONLY` | One continuous Puerto Vallarta International Convention Center identity; ICC is abbreviation. |
| `VEN-000363` | `ALIAS_ONLY` | One continuous William and Mary Hall identity; William & Mary Hall is typography/style variant. |
| `VEN-000369` | `PERIODIZE` | Redbird Arena → CEFCU Arena. |
| `VEN-000371` | `CANONICAL_CORRECTION` | One Guerra Sports Complex identity; verify authoritative first name spelling, Eugenio vs Eugene, rather than creating naming periods. |
| `VEN-000373` | `PERIODIZE` | Oregon State Coliseum → Gill Coliseum. |
| `VEN-000377` | `ALIAS_ONLY` | One continuous Thomas & Mack Center identity; Tarkanian Court is competition-space name and Thomas & Mack Arena is variant. |
| `VEN-000382` | `RESEARCH_HOLD` | Verify whether Nielsen Field House is the same physical building as George Albert Smith Field House / Smith Fieldhouse before any naming-period treatment. |
| `VEN-000384` | `ALIAS_ONLY` | One continuous Men’s Gymnasium identity; Men’s Gym / University Gymnasium are variants. |
| `VEN-000385` | `ALIAS_ONLY` | One continuous Old University Gymnasium identity; University Gymnasium / Old Gymnasium are variants. |
| `VEN-000386` | `ALIAS_ONLY` | One continuous Anaheim Convention Center arena identity; Arena specifies the basketball space rather than a rename. |
| `VEN-000388` | `RESEARCH_HOLD` | Determine whether Baoshan Sports Center is the overall complex and Baoshan Arena the specific arena before treating as naming history. |
| `VEN-000389` | `ALIAS_ONLY` | One continuous Cannon Activities Center identity; George Q. Cannon/full and Cannon Event Center forms are aliases unless later evidence establishes a formal rename. |
| `VEN-000395` | `ALIAS_ONLY` | One continuous Astrodome identity; Houston qualifier only. Prior duplicate physical venue ID already retired. |
| `VEN-000396` | `RESEARCH_HOLD` | Research Public School Fieldhouse → Jeppesen Fieldhouse/Gymnasium chronology; may represent a true formal rename. |
| `VEN-000405` | `ALIAS_ONLY` | One continuous Marriott Center identity; Mariott Center is typo only. |
| `VEN-000408` | `ALIAS_ONLY` | One continuous UCLA Men’s Gymnasium identity; Men’s Gym is shorthand. |
| `VEN-000411` | `ALIAS_ONLY` | One continuous Municipal Auditorium (New Orleans) identity; city qualifier only. |
| `VEN-000413` | `ALIAS_ONLY` | One continuous Olympic Auditorium identity; Grand Olympic Auditorium is expanded/full-name treatment unless later evidence establishes otherwise. |
| `VEN-000430` | `ALIAS_ONLY` | One continuous Venice High School Gym identity; Gym/Gymnasium wording only. |
| `VEN-000431` | `ALIAS_ONLY` | One continuous Atlanta Auditorium identity; The Auditorium is shorthand. |
| `VEN-000432` | `ALIAS_ONLY` | One continuous Ballantine Gymnasium identity; Ballantine Gym is shorthand. |
| `VEN-000433` | `RESEARCH_HOLD` | Research Boardwalk Hall / Atlantic City Convention Hall chronology and distinguish the historic hall from the separate modern Atlantic City Convention Center before periodization. |
| `VEN-000434` | `ALIAS_ONLY` | One continuous Charles E. Smith Center identity; Smith Center is shorthand. |
| `VEN-000435` | `ALIAS_ONLY` | One continuous College Avenue Gym identity; College Avenue Gymnasium and The Barn are aliases. |
| `VEN-000438` | `ALIAS_ONLY` | One continuous Galactic Ballroom at Moon Palace Resort identity; Moon Palace Resort is broader resort-level source wording. |
| `VEN-000439` | `RESEARCH_HOLD` | Determine physical/name relationship between Highland Park Gym and Highland Park Masonic Hall before periodization. |
| `VEN-000440` | `ALIAS_ONLY` | One continuous Jadwin Gymnasium identity; Jadwin Gym / Jadwin Fieldhouse are variants. |
| `VEN-000443` | `PERIODIZE` | Sears Centre → NOW Arena; Sears Centre Arena is first-era variant. |
| `VEN-000444` | `PERIODIZE` | Air Canada Centre → Scotiabank Arena. |
| `VEN-000445` | `ALIAS_ONLY` | One continuous South Padre Island Convention Center identity; Centre is spelling variant. |
| `VEN-000447` | `ALIAS_ONLY` | One continuous Brick Breeden Fieldhouse identity; Worthington Arena / Max Worthington Arena are competition-space names within the fieldhouse. |
| `VEN-000449` | `PERIODIZE` | McKeon Pavilion → University Credit Union Pavilion. |
| `VEN-000453` | `PERIODIZE_RESEARCH` | Municipal Auditorium → Civic Center Music Hall, subject to same-building chronology verification. |
| `VEN-000454` | `PERIODIZE_RESEARCH` | Research Tulsa Convention Center → Cox Business Center → Arvest Convention Center chronology and determine whether Cox Business Convention Center was a separate formal name or variant. |
| `VEN-000457` | `PERIODIZE` | Convocation Center → BankUnited Center → Watsco Center. |
| `VEN-000458` | `PERIODIZE` | SIU Arena → Banterra Center. |
| `VEN-000459` | `ALIAS_ONLY` | One continuous Beeghly Center identity; Zidian Family Arena at Beeghly Center is a named competition-space/sponsor overlay. |
| `VEN-000460` | `ALIAS_ONLY` | One continuous Arsenal Technical High School identity; Tech H.S. / Arsenal Tech are aliases. |
| `VEN-000464` | `ALIAS_ONLY` | One continuous Ervin J. Nutter Center identity; Nutter Center is shorthand. |
| `VEN-000467` | `ALIAS_ONLY` | One continuous Coliseo Roberto Clemente identity; Roberto Clemente Coliseum is English translation. |
| `VEN-000470` | `ALIAS_ONLY` | One continuous John Gray Gymnasium identity; John Gray Gym is shorthand. |
| `VEN-000471` | `ALIAS_ONLY` | One continuous Coliseo de Puerto Rico / José Miguel Agrelot Coliseum identity; treat the formulations as same formal identity rather than successive periods. |
| `VEN-000474` | `RESEARCH_HOLD` | Determine whether CU Fieldhouse → Balch Fieldhouse was a true formal rename and establish chronology. |
| `VEN-000475` | `RESEARCH_HOLD` | Determine whether Men’s Gymnasium → Carlson Gymnasium was a true rename and establish chronology. |
| `VEN-000485` | `ALIAS_ONLY` | One continuous Sun Devil Gymnasium identity; Sun Devil Gym is shorthand. |
| `VEN-000489` | `ALIAS_ONLY` | One continuous Jacksonville Veterans Memorial Coliseum identity; Jacksonville Memorial Coliseum / Jacksonville Coliseum are shortened variants unless later evidence establishes otherwise. |
| `VEN-000492` | `PERIODIZE` | Centennial Hall → Savage Hall → Savage Arena. |
| `VEN-000494` | `ALIAS_ONLY` | One continuous Iowa State Armory identity; The Armory is shorthand. |
| `VEN-000499` | `PERIODIZE_RESEARCH` | Research full Miami arena chronology: AmericanAirlines Arena → FTX Arena → interim Miami-Dade naming → Kaseya Center; current registry omits formal eras. |
| `VEN-000503` | `PERIODIZE_RESEARCH` | McGrath Arena → McGrath-Phillips Arena, subject to formal rename-date verification. |
| `VEN-000505` | `PERIODIZE_RESEARCH` | Research Rochester War Memorial lineage → Blue Cross Arena and determine whether Rochester Community War Memorial and Blue Cross/Blue Shield Arena were distinct formal eras or variants. |
| `VEN-000509` | `PERIODIZE_RESEARCH` | Research full Quad Cities arena chronology from The MARK of the Quad Cities through omitted sponsored eras to Vibrant Arena at The MARK. |
| `VEN-000512` | `ALIAS_ONLY` | One continuous Buffalo Memorial Auditorium identity; Memorial Auditorium is shorthand. |
| `VEN-000513` | `RESEARCH_HOLD` | Determine whether Alumni Memorial Gymnasium → Brodie Gym was an actual formal rename of the same physical building. |
| `VEN-000514` | `ALIAS_ONLY` | One continuous Angier B. Duke Gymnasium identity; Angier Duke Gymnasium and The Ark are aliases/nickname. |
| `VEN-000515` | `ALIAS_ONLY` | One continuous Birmingham City Auditorium identity; Municipal Auditorium variants are shorthand/location-qualified forms. |
| `VEN-000516` | `ALIAS_ONLY` | One continuous Card Gymnasium identity; Card Gym is shorthand. |
| `VEN-000521` | `RESEARCH_HOLD` | Research Raleigh Auditorium / Municipal Auditorium / Old City Auditorium / City Hall and Auditorium same-building and naming-history relationship before periodization. |
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
| `VEN-000554` | `RESEARCH_HOLD` | Research Rice Field House / Rice Gymnasium / Autry Court chronology; may represent genuine formal naming eras. |
| `VEN-000555` | `PERIODIZE_RESEARCH` | Research full Bossier City arena chronology; CenturyTel Center → likely omitted CenturyLink era → Brookshire Grocery Arena. |
| `VEN-000557` | `RESEARCH_HOLD` | Research Comerica Center full chronology; Comerica Arena may be erroneous variant and earlier formal naming history may be omitted. |
| `VEN-000560` | `ALIAS_ONLY` | One continuous Delmar Fieldhouse identity; Delmar Gym is shorthand. |
| `VEN-000563` | `PERIODIZE_RESEARCH` | Research Philadelphia Convention Hall / Municipal Auditorium / Philadelphia Civic Center chronology and exact period boundaries. |
| `VEN-000565` | `ALIAS_ONLY` | One continuous Tech Gym identity; The Barn is nickname. |
| `VEN-000570` | `ALIAS_ONLY` | One continuous Fair Park Recreation Building identity; Fair Park Rec. Center is shorthand/variant. |
| `VEN-000574` | `ALIAS_ONLY` | One continuous Civic Auditorium (San Francisco) identity; San Francisco / SF qualifiers are aliases. |
| `VEN-000576` | `PERIODIZE` | Patriot Center → EagleBank Arena. |
| `VEN-000578` | `PERIODIZE_RESEARCH` | Research full Estero arena chronology; Germain Arena → Hertz Arena is real but current registry likely omits an earlier formal arena name. |
| `VEN-000580` | `PERIODIZE` | Lubbock Coliseum → City Bank Coliseum. |
| `VEN-000582` | `ALIAS_ONLY` | One continuous Einar Nielsen Fieldhouse identity; Nielsen Fieldhouse is shorthand. |
| `VEN-000583` | `ALIAS_ONLY` | One continuous Donald W. Reynolds Center identity; Reynolds Center is shorthand. |
| `VEN-000584` | `ALIAS_ONLY` | One continuous Sam Houston Coliseum identity; Houston Coliseum is shorthand. |
| `VEN-000585` | `CANONICAL_CORRECTION` | State Fair Arena is the physical venue; State Farm Arena [BC source wording] is erroneous source wording, not a historical period. |
| `VEN-000594` | `ALIAS_ONLY` | One continuous JSerra Pavilion identity; The Pavilion at JSerra is expanded form. |
| `VEN-000597` | `ALIAS_ONLY` | One continuous Robertson Memorial Fieldhouse identity; Memorial Field House is shorthand. |
| `VEN-000600` | `ALIAS_ONLY` | One continuous Ladies/Women’s Gymnasium identity; Old Ladies Gymnasium is retrospective descriptor rather than a separate period. |
| `VEN-000602` | `PERIODIZE` | Prescott Valley Event Center → Tim’s Toyota Center → Findlay Toyota Center. |
| `VEN-000605` | `PERIODIZE` | Glens Falls Civic Center → Cool Insuring Arena → Harding Mazzotti Arena. |
| `VEN-000606` | `PERIODIZE` | Toso Pavilion → Leavey Center; Harold J. Toso Pavilion and Leavey Event Center are variants within those eras. |
| `VEN-000615` | `ALIAS_ONLY` | One continuous Omaha Civic Auditorium identity; Civic Auditorium is shorthand. |
| `VEN-000616` | `ALIAS_ONLY` | One continuous Perkins Gymnasium identity; Perkins Gym is shorthand. |
| `VEN-000618` | `RESEARCH_HOLD` | Resolve Tucson Community Center Arena / Tucson Convention Center Arena / Tucson Arena and distinguish arena naming from surrounding-complex naming. |
| `VEN-000634` | `ALIAS_ONLY` | One continuous Norfolk Scope identity; Scope / Norfolk Scope Arena are aliases. |
| `VEN-000637` | `ALIAS_ONLY` | One continuous Encina Gymnasium identity; Encina Gym is shorthand. |
| `VEN-000654` | `PERIODIZE` | Charleston Civic Center → Charleston Coliseum & Convention Center; Charleston Coliseum is shorthand/current arena wording. |
| `VEN-000673` | `ALIAS_ONLY` | One continuous WVU Armory identity; ROTC Armory / Armory are aliases unless later evidence establishes a formal rename. |
| `VEN-000674` | `RESEARCH_HOLD` | Determine whether UC Fieldhouse → Armory Fieldhouse was a genuine formal rename. |
| `VEN-000683` | `CANONICAL_CORRECTION` | Duplicate literal Orange County Civic Center rows represent one naming identity; registry cleanup only, no periodization. |
| `VEN-000695` | `ALIAS_ONLY` | One continuous Devlin Fieldhouse identity; Avron B. Fogelman Arena is the named competition space within the same building. |
| `VEN-000708` | `ALIAS_ONLY` | One continuous Memorial Coliseum (Winston-Salem) identity; W-S Coliseum is shorthand. |
| `VEN-000709` | `ALIAS_ONLY` | One continuous Montego Bay Convention Center identity; Centre is spelling variant. |
| `VEN-000710` | `ALIAS_ONLY` | One continuous R.J. Reynolds High School identity; Reynolds HS / Reynolds High School are aliases. |
| `VEN-000711` | `RESEARCH_HOLD` | Clarify Murray State Sports Arena / Racer Arena / Carlisle Cutchin Fieldhouse and arena-within-fieldhouse relationship. |
| `VEN-000712` | `ALIAS_ONLY` | One continuous Wake Forest College Gymnasium identity; Gymnasium / old Gymnasium are descriptive variants. |
| `VEN-000715` | `ALIAS_ONLY` | One continuous Fike Field House identity; Clemson Field House is alias. |
| `VEN-000716` | `ALIAS_ONLY` | One continuous Holtzendorff YMCA identity; YMCA Building / YMCA are shorthand. |
| `VEN-000729` | `PERIODIZE_RESEARCH` | Research full Gwinnett arena chronology from Arena at Gwinnett through omitted sponsored era(s) to Gas South Arena. |
| `VEN-000736` | `ALIAS_ONLY` | One continuous Rafael A. Mangual Coliseum identity; Spanish/English ordering only. |
| `VEN-000737` | `ALIAS_ONLY` | One continuous Poliforum Benito Juárez identity; Poliforum Cancún is alternate/local shorthand. |
| `VEN-000742` | `ALIAS_ONLY` | One continuous Minges Coliseum identity; Williams Arena is the named competition space within Minges Coliseum. |
| `VEN-000743` | `ALIAS_ONLY` | One continuous Trees Gymnasium identity; Trees Gym is shorthand. |
| `VEN-000748` | `ALIAS_ONLY` | One continuous Rose Hill Gymnasium identity; Fordham Gym is institutional shorthand. |
| `VEN-000749` | `RESEARCH_HOLD` | Research Philadelphia Auditorium / Philadelphia Arena full chronology; current registry may omit earlier formal wording. |
| `VEN-000750` | `ALIAS_ONLY` | One continuous Archbold Gymnasium identity; Archbold Gym is shorthand. |
| `VEN-000753` | `RESEARCH_HOLD` | Clarify Manley Field House / John A. Lally Athletics Complex relationship: true rename, larger-complex designation, or materially reconfigured facility. |
| `VEN-000754` | `RESEARCH_HOLD` | Research Old Gym / Gymnasium and YMCA Building / Women’s Gymnasium chronology; may reflect genuine successive institutional uses/names. |
| `VEN-000755` | `PERIODIZE` | State Fair Coliseum → Toyota Coliseum; New York State Fair Coliseum / Fairgrounds Coliseum are expanded first-era forms. |
| `VEN-000757` | `PERIODIZE_RESEARCH` | Research exact Onondaga County War Memorial → Oncenter War Memorial → Upstate Medical University Arena naming chronology. |
| `VEN-000761` | `ALIAS_ONLY` | One continuous West Jefferson Street Armory identity; Jefferson Street Armory is shorthand. |
| `VEN-000766` | `PERIODIZE` | Boston Arena → Matthews Arena. |
| `VEN-000778` | `PERIODIZE_RESEARCH` | Research full Portland, Maine arena chronology from Cumberland County Civic Center through later Cross Insurance Arena era; Portland Civic Center appears shorthand and registry is incomplete. |
| `VEN-000779` | `ALIAS_ONLY` | One continuous Percy Hedgecock Gymnasium identity; Hedgecock Gym is shorthand. |
| `VEN-000781` | `PERIODIZE_RESEARCH` | Research full Bridgeport arena chronology: Arena at Harbor Yard → Webster Bank Arena → omitted later/current naming era(s). |
| `VEN-000785` | `ALIAS_ONLY` | One continuous Calumet Club identity; parenthetical locality is disambiguation only. |
| `VEN-000786` | `ALIAS_ONLY` | One continuous Coast Guard Air Station Borinquen Hangar identity; CGAS/U.S. Coast Guard expansions are aliases. |
| `VEN-000787` | `ALIAS_ONLY` | One continuous Louisville Elks Club identity; article-only variation. |
| `VEN-000788` | `RESEARCH_HOLD` | Determine whether College Park Gym was an actual predecessor name of Spencer Memorial Gymnasium or a source/location conflation. |
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
| `VEN-000815` | `PERIODIZE_RESEARCH` | Research Creighton University Gym/Old Gymnasium → Vinardi Center chronology and determine whether Vinardi Athletic Center is another formal era or expanded form. |
| `VEN-000819` | `PERIODIZE` | JQH Arena → Great Southern Bank Arena. |
| `VEN-000821` | `ALIAS_ONLY` | One continuous Al McGuire Center identity; The Al is nickname. |
| `VEN-000823` | `PERIODIZE_RESEARCH` | Research RPI Field House → Houston Field House chronology and verify formal rename boundary. |
| `VEN-000825` | `ALIAS_ONLY` | One continuous St. Xavier College Gym identity; St. Xavier Gym is shorthand. |
| `VEN-000826` | `ALIAS_ONLY` | One continuous Middletown High School (Girard Avenue) identity; Girard Avenue is physical-campus disambiguation. |
| `VEN-000838` | `ALIAS_ONLY` | One continuous Alumni Hall (Providence) identity; Providence College qualifier is alias. |
| `VEN-000839` | `ALIAS_ONLY` | One continuous St. John’s College Gymnasium identity; Lewis Avenue qualifier and shorter St. John’s Gym forms are aliases. |
| `VEN-000840` | `ALIAS_ONLY` | One continuous DeGray Gymnasium identity; DeGray Gym is shorthand. |
| `VEN-000858` | `ALIAS_ONLY` | One continuous West Catholic High School Gymnasium identity; school-only form is shorthand. |
| `VEN-000859` | `ALIAS_ONLY` | One continuous Alumni Hall (Villanova) identity; Alumni Gym / Villanova Alumni Hall are aliases. |
| `VEN-000860` | `PERIODIZE_RESEARCH` | Villanova Field House → Jake Nevin Field House; owner approves two periods, exact rename boundary to verify. |
| `VEN-000861` | `PERIODIZE` | Sovereign Bank Arena → Sun National Bank Center → CURE Insurance Arena. |
| `VEN-000863` | `RESEARCH_HOLD` | Research A.J. Palumbo Center lineage into UPMC Cooper Fieldhouse; verify same-building continuity and full chronology before periodization. |

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

- Continue owner adjudication of the still-unreviewed multi-name venue population.
- Research every `RESEARCH_HOLD` and every `PERIODIZE_RESEARCH` chronology before implementation.
- Verify exact transition dates for approved periodized histories.
- After the multi-name population is closed, perform a **light high-yield screen of the 483 single-name venues** for obvious missing historical rename histories. This is not permission for 483 deep research campaigns.
- Only after the census is complete should rollout tranches be finalized and repository-wide period rows implemented in bounded shared-reference maintenance PRs.
