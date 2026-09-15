# Houston men’s basketball — Source notes

## Primary supplied source

**Houston 2025-26 Men’s Basketball Media Guide (`Houston.pdf`)**

SHA-256: `7fc0ad88808add6c6cc28c6ccc85c0c975459153e0a2cb1c6f1a581284f5160d`

Primary uses:
- Year-by-Year Results, printed pp. 163-173: controlling historical game universe through 2024-25 and row-level H/A/N notation.
- Yearly Records, printed p. 174: season controls, conference chronology, H/A/N aggregate QA, and home-court summary.
- Series History, printed pp. 152-162: event/venue evidence and adjudication for otherwise unmarked rows; not used to override stronger year-by-year row-level H/A/N notation when the guide conflicts internally.
- NCAA Tournament History, printed pp. 140-141: postseason classification, historical bracket context, exact physical sites, and Stage 3B corrections.
- Conference Tournament History, printed pp. 142-143: tournament classification, seeds/results/sites, title appearances, and pre-SWC absence check.
- NIT / CBI History, printed p. 144: postseason classification, exact sites, and title/round context.
- Regular-season tournament history, printed pp. 224-225: neutral-event/site evidence.
- Program quick facts: 13 conference regular-season championships, 9 conference-tournament titles, 26 NCAA appearances through 2025, seven Final Fours through 2025, and three national-championship-game appearances through 2025.

Home-game legend: the guide states that `*` indicates a conference game and HOME games are listed in bold. `at` and `vs.` markers were preserved as source evidence. Physical venue chronology was applied only after H/A/N was independently established.

## 2025-26 official schedule supplement

University of Houston Athletics completed 2025-26 schedule/results:
`https://uhcougars.com/sports/mens-basketball/schedule/text/2025-26`

Uses:
- Adds 37 competitive games, 30-7, to the historical media-guide universe.
- Excludes the 2025-10-26 Mississippi State exhibition at Fort Bend Epicenter.
- Supplies completed 2026 Big 12 Championship and NCAA Tournament results through the Sweet Sixteen.
- Produces Houston’s 27th NCAA Tournament appearance.

## Owner-supplied conference-tournament site reference

File: `ct venues.xlsm - Tournament Sites(2).csv`

SHA-256: `4a2c7a06ae96aa8e8970247bd72bcbe450a533fb554b495faa93070b2d0b8c0a`

Owner authorization is deliberately bounded: for **Houston conference tournaments since joining the Southwest Conference**, every Houston conference tournament is represented and the sheet may be used reliably. It is not treated as universally exhaustive and is not generalized to unrelated schools or pre-SWC conference eras.

Stage 3B found no Houston conference-tournament appearance before the Southwest Conference era in the accepted in-scope universe.

## Institutional / reciprocal / reference evidence

Targeted institutional, reciprocal, archival, and established-project venue evidence was used only where required to resolve opponent identity, physical venue identity, or a source conflict. The row-level research basis is retained in prior Stage 2/3 audits and, for any remaining material site gap, directly in `source-games.csv`.

Research-base global venue identities are references at:
`research_base_sha = 0b8cf20e3b14517031a5a0e62b362883966e51c1`.

Research-time new physical venues intentionally carry blank numeric `venue_id` in the six-file package. Their durable identity is the venue key + canonical name + geography, and Implementation must rebase them against then-current protected `main`.

## Conflict policy

The project prefers explicit unknown to unsupported certainty. Source conflicts were resolved only when stronger targeted evidence justified a correction. Raw source wording is preserved in `raw_text`; normalized correction overlays are represented in the curated/date/score fields and described in `notes`.

Away regular-season opponent buildings are outside this lane’s site-reconstruction requirement. HOME venue/location, all postseason sites, and all NCAA sites were treated under the stricter project completeness rules.

## Stage 6 adversarial source classes and bounded recoveries

The pre-freeze self-challenge targeted the 35-row regular-season neutral-site debt population, plus current-program opponent/venue identity drift. It did not reopen accepted Stages 1-3B generally.

High-yield source classes checked and applied where supported:

- **All-College Tournament venue chronology, Oklahoma City.** City of Oklahoma City history documents the 1954 All-College Tournament at Municipal Auditorium; official Arkansas records identify the 1962-63 All-College Tournament at Municipal Auditorium and the 1967-68 tournament at State Fair Arena; contemporary Oklahoma City reporting also identifies State Fair Arena for the later event era. These sources supported systematic physical-site recovery without changing independently established H/A/N.
  - https://www.okc.gov/Government/Elected-Officials/Mayor/State-of-the-City/2023-State-of-the-City
  - https://arkansasrazorbacks.com/stats/mbb/2025-26/2025-26%20_Arkansas_Media_Guide_Full.pdf
  - https://gateway.okhistory.org/ark:/67531/metadc993153/m1/8/
- **Western Kentucky, 1953.** WKU institutional series/media-guide history gives Houston-WKU as 1953-12-28 in Louisville, 91-61. Detailed reciprocal schedule evidence places the game at Jefferson County Armory. Houston's literal source row is retained in `raw_text`.
  - https://wkusports.com/documents/download/2021/10/16/2021_22_WKU_Hilltopper_Basketball_Media_Guide_copy_converted.pdf
- **1966 Jonesboro Holiday Tournament.** Houston tournament history identifies the event; Arkansas State institutional notes confirm Indian Fieldhouse as the predecessor basketball building before the Convocation Center.
  - https://astateredwolves.com/news/2014/12/5/209796887.aspx
- **1967 Rainbow Classic.** Reciprocal/event evidence identifies Honolulu International Center Arena. Library of Congress HABS documentation establishes Honolulu International Center as the same physical complex later named Neal S. Blaisdell Center.
  - https://tile.loc.gov/storage-services/master/pnp/habshaer/hi/hi1000/hi1069/data/hi1069data.pdf
- **1978 Pillsbury Classic.** University of Minnesota contemporaneous archival material states that the 1978 Classic featuring Minnesota, Georgia Tech, BYU, and Houston was held at Met Center in Bloomington.
  - https://conservancy.umn.edu/bitstreams/ca65bb4f-a4dd-49eb-ba4b-d51ff147b91c/download
- **1979 Sun Carnival.** Houston Athletics explicitly identifies both 1979 Sun Carnival games at Special Events Center in El Paso. The project reference layer recognizes Special Events Center as a historical alias of the same physical building as Don Haskins Center.
  - https://uhcougars.com/news/2024/11/25/mens-basketball-preview-6-7-mens-basketball-opens-players-era-festival-on-tuesday
- **1983 Hall of Fame Tipoff Classic.** NC State institutional schedule confirms the Houston matchup in Springfield; contemporaneous game coverage explicitly identifies Springfield Civic Center.
  - https://gopack.com/sports/mens-basketball/schedule/1983-84
  - https://www.washingtonpost.com/archive/sports/1983/11/20/nc-state-does-it-again-beating-houston-in-tipoff-game-76-64/61498334-ae8f-4a7e-8ef4-1cc5546cefdc/
- **1986 Kactus Klassic.** Mississippi Valley State's official 1986-87 schedule explicitly places its Houston game at ASU Activity Center in Tempe. The project reference layer recognizes ASU Activity Center as a historical alias of the physical building represented by Desert Financial Arena.
  - https://mvsusports.com/sports/mens-basketball/schedule/1986-1987

Additional reciprocal/event-specific evidence recovered Las Vegas Convention Center for Houston's 1969 UNLV Invitational games and corrected the 1953 Villanova normalized locality to Lexington, Kentucky.

The surviving unresolved venue classes were separately challenged:
- 1953 Kentucky Invitational vs Siena/Villanova — exact physical building not safely established for those two games;
- 1955 Birmingham Classic — event/city established, exact building not established;
- 1956, 1962, and 1968 Sugar Bowl Classic — event/city established, but Houston/Sugar Bowl evidence demonstrates physical buildings varied across eras, so no blanket building assignment is made;
- 1982 Suntory Classic — exact Aoyama Gakuin University Gymnasium physical venue is established, but normalized foreign city/state remain blank under the current source-package geography representation policy.

No comparable systematic high-yield evidence class remained after these checks. Those 11 surviving rows are terminal researched historical/policy debt under the project stopping rule.

## Stage 5 owner identity disposition and Stage 6 current-registry check

The owner approved the complete 28-identity Houston working `NON_D1` scan on 2026-09-13. Stage 6 compared the accepted identities against current protected-main program identities and the verified historical alias registry; it found no current-program key split and no ambiguous current-program match.

Protected `main` had advanced beyond the original research base by Stage 6. That change does not authorize a Research-lane current-main numeric/reference rebase. The authoritative shared-reference rebase remains required in serialized Implementation before tracked Phase 0.

