# Texas men's basketball source-package curation notes

## Research status

This six-file portfolio was built as a parallel research-lane artifact outside tracked global repository state and is **RESEARCH_FROZEN** against `research_base_sha=a05ad97f1023dae8f277c805c9598ecb5caa319c`.

Owner history-scope ruling: **Texas has always been D1/top-level for site purposes.** Public/site history therefore begins with program inception in **1905-06**.

The owner additionally authorized the supplied conference-tournament location workbook's Texas-relevant **Southwest Conference, Big 12, and SEC** sections as complete for Texas. The workbook remains globally incomplete and no other section is promoted to project canon.

## Coverage and record

- Competitive games: **3,112**
- On-court record represented by normalized row scores/results: **1,938-1,174**
- Coverage: **1905-06 through completed 2025-26**
- Exhibitions/scrimmages/canceled entries: **excluded**
- Site classification: **1,523 Texas-home / 1,177 opponent-home / 412 neutral / 0 unknown**
- Game types: **2,905 regular season / 100 conference tournament / 86 NCAA Tournament / 14 NIT / 7 other postseason**

Texas's fact-book aggregate through 2024-25 is 1,918-1,158 across 3,076 games. The package's historical **on-court** ledger is 1,917-1,159 because the 1918 Texas A&M contest is represented by the played 7-8 score rather than the later administrative forfeit. The completed 2025-26 official schedule adds 21-15 across 36 games.

## Material source normalization decisions

1. **1918 Texas A&M forfeit.** The year-by-year row prints `W 7-8` and the footnote says Texas A&M forfeited because Pay Dwyer was ruled ineligible. The package stores Texas's on-court 7-8 loss and separately records `administrative_status=FORFEIT`.
2. **1979/1980 SWC Arkansas tournament scores.** Texas's dedicated SWC Tournament history establishes the 1979 final as Arkansas 64, Texas 62 and the 1980 semifinal as Arkansas 39, Texas 38. The year-by-year ledger has those two scores effectively swapped; `raw_text` preserves the printed rows.
3. **1995 SWC semifinal vs. Rice.** The dedicated tournament history gives Texas 78, Rice 75; the year-by-year ledger prints 78-71. Structured score is 78-75.
4. **1998 Big 12 quarterfinal vs. Oklahoma State.** The year-by-year ledger's 65-64 is retained; the dedicated tournament summary prints 65-62. The source-internal conflict is documented rather than silently erased.
5. **Historical qualifying playoffs.** Seven real postseason games that were not the annual conference tournament, NCAA Tournament proper, or NIT are classified `POSTSEASON`: the 1951 NCAA District 6 three-game playoff, 1954 SWC two-game playoff, 1965 NCAA/SWC play-in, and 1972 SWC playoff.

## Exact-date uncertainty

Exactly **16** competitive rows intentionally have blank normalized dates:

- nine 1924-25 Dallas holiday games; Texas states that no records of their dates exist;
- the 1930-31 St. Edward's game; Texas explicitly says no date is available;
- two 1939-40 Kilgore Pipeliners games; Texas explicitly says no dates were available;
- 1910 at Southwestern, printed as impossible February 29 in a non-leap year;
- three 1912-13 road rows printed as Jan. 5/Jan. 6 after a Jan. 31 row and before Feb. 7. The source chronology is contradictory, so the package does not manufacture corrected February dates.

All played scores are known.

## H/A/N discipline

The year-by-year ledger's explicit source syntax establishes site perspective: `at` -> `OPPONENT_HOME`, `vs.`/`vs` -> `NEUTRAL`, and an unprefixed game row -> `SOURCE_PROGRAM_HOME`. The completed 2025-26 official schedule supplies its own H/A/N classifications. Physical venue geography never creates or changes H/A/N.

Venue chronology is applied only after a row is independently established as Texas home. Important home identities are Clark Field for the 1906 opener, Ben Hur Temple for the 1913 first indoor home game, Men's Gym beginning in 1917-18, Gregory Gym beginning Dec. 5, 1930, Frank Erwin Center beginning Nov. 29, 1977, and Moody Center beginning in 2022-23. The 2021 Sam Houston and 2022 UTRGV Gregory Gym throwback games are handled explicitly.

## Conference chronology

- Independent: 1905-06 through 1913-14
- Southwest Conference: 1914-15 through 1995-96
- Big 12: 1996-97 through 2023-24
- SEC: 2024-25 onward

Conference membership history is distinct from tournament classification.

## Postseason taxonomy and sites

The package contains **86 NCAA Tournament games** through 2026. Every NCAA row has a curated physical venue plus city/state. Historical consolation/third-place games retain `NCAA_TOURNAMENT` with blank canonical round when the project's modern controlled vocabulary does not map honestly.

The package contains **14 NIT games** and marks only the verified 1978 and 2019 title games `Championship`. It contains **100 conference-tournament games** beginning with the modern postseason SWC Tournament in 1976; older holiday events printed as “SWC Tournament” are regular-season events and remain `REGULAR_SEASON`.

## Conference-tournament site reference

Owner-supplied `Conference_Tournament_Site_Reference(20260825-203322).xlsm` (SHA-256 `68fd42a5da4e2a908a9911c5812fda317920e1842b5518ebba52d20cdd2b26e2`) is incomplete as a universal reference. Only the owner-authorized Texas-relevant SWC, Big 12, and SEC sections were used. The package respects campus preliminary rounds instead of assigning every game to the later shared arena. Examples include Gregory Gym (1977 Baylor first round), Frank Erwin Center (1981 Rice campus round), Moody Coliseum (1976/1983), G. Rollie White Coliseum (1984), and the later shared Reunion/Kemper/American Airlines/Paycom/T-Mobile/Bridgestone sites.

## Opponent identity policy

Every source opponent label resolves through `opponents.csv`; no unresolved key is passed downstream. Current Division I identities reuse project key conventions where established. Historical clubs, YMCAs, military teams, high schools, industrial teams, and non-current colleges remain distinct rather than being forced into current programs.

Important institutional-lineage normalizations include Baptist College -> Charleston Southern; Biscayne -> St. Thomas University (Florida historical lineage, not modern St. Thomas-Minnesota); Colorado A&M -> Colorado State; East Texas/Texas A&M-Commerce -> East Texas A&M; Houston Baptist -> Houston Christian; Memphis State -> Memphis; Southwest Texas -> Texas State; Southwestern Louisiana -> Louisiana; Texas A&I -> Texas A&M-Kingsville; Texas Western -> UTEP; UT-Pan American -> UT Rio Grande Valley; and Maryville (Mo.) -> Northwest Missouri State.

## Venue rebase warning

All numeric `venue_id` cells are intentionally blank in this research artifact. Physical `venue_key`, canonical name, aliases, geography, chronology, and source basis are the research deliverable. The serialized Implementation lane must rebase every venue identity against then-current `main`, reusing matching global physical identities and allocating any genuinely new IDs before `INTEGRATION_FROZEN`.

## Final pre-freeze mechanical corrections

- Historical `source_page` locators were normalized to the fact book's **printed page numbers 91-108**; the extraction working index had been one page lower.
- Current-Division-I opponent fields were aligned to the exact research-baseline program registry, including American (`american-university`), Florida A&M (`florida-a-m`), Hawai'i (`hawai-i`), Nicholls (`nicholls`), UC Riverside, UC Santa Barbara, Canisius, Chattanooga, Illinois, Mercer, UL Monroe, UNC Asheville, UNC Greensboro, and Virginia. Literal historical source labels remain preserved.

## Manual QA snapshot

- Exactly six required flat files prepared.
- Source-game IDs: 3,112 nonblank / 3,112 unique.
- Opponent rows: 357; unresolved opponent keys: 0.
- Unknown exact dates: 16.
- Unknown played scores: 0.
- NCAA rows with venue/city/state: 86/86.
- Venue rows: 65.
- City/state atomicity, score atomicity, controlled site/game-type vocabulary, curated venue resolution, NCAA round vocabulary, and exhibition exclusion: PASS in manual acceptance-equivalent QA.
- Repository executable `python tools/onboarding_hardening.py research-check ...`: **NOT RUN IN THIS ENVIRONMENT** because this research environment does not have the repository checkout/tooling mounted. The Implementation lane should run it immediately on receipt.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=57270f9641c1d1d1615ce45b9b490a9e416e0765` from `research_base_sha=a05ad97f1023dae8f277c805c9598ecb5caa319c`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
