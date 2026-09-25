# West Virginia research notes

## Research lifecycle
Research Stage 6 has completed the required post-owner adversarial self-challenge against the accepted cumulative Stage 1-5 state. Stage 5 owner NON_D1 sanity scan was approved on 2026-09-19 with 0 owner flags. Stage 6 repaired only defects exposed by the bounded audit and did not reopen completed historical research classes. This package is **not RESEARCH_FROZEN**; immutable Stage 7 packaging remains separately authorized work.

## Game universe
- Competitive source-game rows: **3,097**.
- Accepted on-court record: **1,895-1,202**.
- Regular season: **2,849**; postseason: **248**.
- Exhibitions/noncompetitive events: **0**.
- Unknown exact dates: **0**.
- Unknown played scores: **0**.
- Every accepted Stage 1 research game ID appears exactly once in `source-games.csv`; duplicate real-game signatures exposed by Stage 6 QA: **0**.

## Opponent identity
- Source labels in `opponents.csv`: **420**.
- Distinct canonical opponent identities: **332**.
- Current-D1 identities at the research base: **242** / **2,561 games**.
- Working NON_D1/historical identities: **90** / **536 games**.
- Stage 5 owner NON_D1 sanity scan: **APPROVED 2026-09-19; 0 owner flags**.
- Stage 6 normalized-name comparison of the approved NON_D1 population against the research-base current-D1 registry exposed **0** exact current-program collisions, **0** known current-program key splits, and **0** ambiguous current-program matches.
- The bounded Stage 5 follow-up on the 1915-16 literal opponent `West Lafayette` remains controlling: evidence did not support Purdue normalization, and the approved NON_D1 identity is unchanged.

## Site research
- Accepted all-game H/A/N: SOURCE_PROGRAM_HOME **1,437**, OPPONENT_HOME **1,160**, NEUTRAL **500**, UNKNOWN **0**.
- NCAA Tournament physical venue + city/state gaps: **0**.
- Conference-tournament/NIT/other-postseason material site gaps: **0**.
- Stage 6 repaired a Stage 4 packaging defect on `WVU-STG1-00314`: its accepted HOME classification remains unchanged, Morgantown, WV geography is restored, and its exact building remains explicitly `RESEARCHED_UNRESOLVED_HOME_VENUE` rather than guessed.
- Stage 6 restored accepted geography on the Stage 3A terminal neutral-site population where Stage 4 packaging had incorrectly blanked city/state.
- Nine exact neutral buildings were recovered during the bounded self-challenge: six Far West Classic games at Veterans Memorial Coliseum (Portland), one 1977 Big Sun Tournament game at Bayfront Center (St. Petersburg), and two 1989 Palm Beach Classic games at West Palm Beach Auditorium.
- Final terminal researched exact-building debt: **44 rows** = **43 NEUTRAL + 1 HOME**. Every surviving row has complete city/state and explicit research accounting; unaccounted material site-gap rows: **0**; HOME publication blockers: **0**.
- Final neutral exact-building debt is historical and concentrated in the 1910s-1970s; no modern 2000+ neutral building blank remains.
- Opponent-home regular-season building reconstruction remains intentionally outside this school-owned Research responsibility.

## Physical venue identity
Stage 6 challenged local venue rows against the recorded research base `58a86ee6af72ea9c3b2bd388db772de5a9ff6fb3`, collapsing naming-era/local duplicates into physical identities while preserving source labels and raw evidence.

Final local physical venue state:
- **124** unique physical venue rows;
- **93** definite research-base physical reuses;
- **27** historically resolved identities pending authoritative current-main registration/reuse determination;
- **4** historically resolved physical identities where the research-base shared registry itself contains duplicate/competing global IDs and therefore requires Implementation-time shared-registry reconciliation;
- ambiguous historical physical identities: **0**.

The four shared-registry reconciliation cases are Blue Cross/Blue Shield Arena / Rochester War Memorial, Harold J. Toso Pavilion / Leavey Center, Rocket Arena naming eras, and The Pit / University Arena / Bob King Court. Research resolves the physical history but does not select or mutate authoritative global IDs.

## Postseason
All **248** postseason rows remain closed and unchanged in classification: conference tournament **143**, NCAA Tournament **63**, NIT **37**, other postseason **5**. Stage 6 introduced no postseason taxonomy changes and no postseason site debt.

## Preserved contradiction
One accepted narrow source contradiction remains preserved: `WVU-STG1-01812`, 1986-03-13 vs Old Dominion. Stage 1 score **64-72** remains controlling; the WVU Postseason Appearances table gives **62-74**. Disposition remains `OPEN_NARROW_SCORE_CONFLICT_STAGE1_REMAINS_CONTROLLING`. Stage 6 did not reopen or silently resolve it.

## Conference history
Independent (1903-04 through 1949-50) -> Southern Conference (1950-51 through 1967-68) -> Independent (1968-69 through 1975-76) -> Eastern Collegiate Basketball League (1976-77) -> Eastern Eight (1977-78 through 1981-82) -> Atlantic 10 (1982-83 through 1994-95) -> Big East (1995-96 through 2011-12) -> Big 12 (2012-13 onward).

## Stage 6 pre-freeze adversarial self-challenge
**PRE-FREEZE SELF-CHALLENGE: PASS**

Control Center challenge question: **If the Control Center challenged the largest unresolved/debt populations in this portfolio, what would it challenge?**

It would challenge the 53-row inherited exact-building debt, the one HOME building exception, neutral event-site blanks, local physical-venue naming/identity collisions, the approved NON_D1 population for hidden current programs, and reciprocal published evidence that could expose a surprising contradiction.

Bounded challenge results:
- **HOME venue debt:** one 1927-28 HOME row survives. Stage 6 corrected its packaging to complete Morgantown, WV geography and the dedicated historical-unrecoverable HOME status. The exact building remains unsupported after the already accepted Stage 3A transition-building research; no building was inferred.
- **UNKNOWN H/A/N:** final count **0**.
- **Exact dates:** final blank count **0**.
- **Neutral exact buildings:** 9 recoveries reduced terminal neutral exact-building debt from 52 to **43**. The surviving class is historical, has complete geography and explicit research basis, and remains after the bounded institutional/event/reciprocal opportunity was exhausted; it is terminal researched historical debt rather than a mandate for row-by-row archaeology.
- **Reciprocal evidence:** published Maryland rows conflict with three accepted WVU Cumberland neutral classifications. Current WVU institutional schedule/opponent-history evidence continues to support Cumberland neutral treatment, so WVU was not rewritten from the reciprocal package alone.
- **Physical venue identity:** local rows were reduced from 138 naming-era/local rows to **124 physical identities**. Definite research-base reuses: **93**; pending current-main registration/reuse: **27**; shared-registry duplicate-ID cases deferred to Implementation: **4**; ambiguous historical physical identities: **0**.
- **Opponent identity:** Stage 5 owner approval remains controlling (90 NON_D1/historical identities / 536 games; 0 flags). Stage 6 exposed **0** current-D1 name collisions, **0** known current-program key splits, and **0** ambiguous current-program matches.
- **Universe/taxonomy:** all **3,097** accepted games and the **2,849 + 248** regular/postseason partition remain exact. H/A/N and postseason classification were not altered.

Research/package acceptance after Stage 6: **0 errors, 0 warnings**. HOME publication blockers: **0**. NCAA site gaps: **0**. Unaccounted material site gaps: **0**. Ambiguous historical physical venue identities: **0**.

`RESEARCH_FROZEN` remains **NO** until separately authorized Stage 7 immutable packaging.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=5c3871e2ee2fe52a9453902baa49dc8ff37277de` from `research_base_sha=58a86ee6af72ea9c3b2bd388db772de5a9ff6fb3`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
