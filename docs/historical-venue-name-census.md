# Historical venue-name census

Status: **WORKING DURABLE CHECKPOINT — CENSUS IN PROGRESS**  
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
