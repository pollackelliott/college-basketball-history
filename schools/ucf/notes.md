# UCF research notes

## Research lifecycle
Research Stage 6 has completed the required post-owner adversarial self-challenge against the accepted cumulative Stage 1-5 state. Stage 5 owner NON_D1 sanity scan was approved on 2026-09-25 with 0 owner flags. Stage 6 repaired only defects exposed by the bounded audit and did not restart completed research classes. This package is **not RESEARCH_FROZEN**; immutable Stage 7 packaging remains separately authorized work.

## Research baseline and universe
- Research base SHA: `5c91e35485060a0be27f9612d0b140883a555dbf`.
- Protected-main snapshot at Stage 6: `e57a7049b2315508e59fd68b4324c34050901f45`.
- Competitive source-game rows: **1,269**.
- Final partition: **1,186 regular season + 83 postseason = 1,269**.
- Exact dates missing: **0**.
- Played scores missing: **0**.
- Duplicate accepted source-game IDs: **0**.
- Duplicate exact game signatures in the target package: **0**.
- Four rows initially carried into Stage 3B were corrected to regular season after UCF's in-season-tournament records established that they were the Merrill Lynch Classic / UCF Classic rather than postseason.

### Stage 6 exact-date repair
`UCF-R-200607-029` vs Houston carried the literal primary-source date `F29`, serialized as `2007-02-29`, which is not a valid calendar date. Stage 6 challenged exact-date integrity and repaired `game_date` to **2007-02-28** using UCF's official contemporaneous recap of the 75-72 overtime win. The literal `F29 Houston W 75-72 (ot)` remains preserved in `raw_text`; this is a field-specific correction, not a rewrite of source evidence.

## H/A/N and site research
Final all-game H/A/N:
- SOURCE_PROGRAM_HOME: **643**
- OPPONENT_HOME: **500**
- NEUTRAL: **126**
- UNKNOWN: **0**

Postseason:
- **83/83** exact physical venue + city/state.
- NCAA Tournament site gaps: **0**.
- Conference-tournament/NIT/other-postseason site gaps: **0**.
- Ambiguous row-level postseason physical identities: **0**.

Terminal regular-season site debt after Stage 6:
- **4 HOME** rows with complete Orlando, FL geography and exact building explicitly `RESEARCHED_UNRESOLVED_HOME_VENUE`.
- **5 historical regular-season NEUTRAL** rows with complete supported city/state and exact building explicitly `RESEARCHED_PARTIAL`.
- Regular-season OPPONENT_HOME exact-building reconstruction remains outside active UCF source-school responsibility unless usable accepted evidence was already present.
- Unaccounted material site-gap rows: **0**.
- HOME publication blockers: **0**.

### Stage 6 HOME venue challenge
The four HOME exceptions are confined to the 1986-87 and 1987-88 Merrill Lynch Classic:
- 1986-12-19 Campbell
- 1986-12-20 Coastal Carolina
- 1987-12-04 Saint Peter's
- 1987-12-05 Campbell

For 1986, UCF's official retrospective places the Campbell game at **Valencia Community College in Orlando**, and Campbell institutional records likewise identify the site as Valencia Community College. Valencia's institutional history confirms multiple Orlando campuses existed by that era, while archival/facility evidence establishes a West Campus gymnasium but does not establish that these two games were played in that specific building. The exact physical building therefore cannot safely be assigned.

For 1987, UCF institutional event history establishes the Merrill Lynch Classic in Orlando and UCF's all-time series establishes HOME, but the event-family evidence changes across adjacent editions: Valencia Community College in 1986 and UCF Gymnasium/Education Gym in the later home-facility era. No authoritative evidence found in the bounded class-level challenge identifies the 1987 physical building. The four rows remain terminal researched HOME venue debt with complete city/state; no building is inferred.

### Stage 6 neutral debt challenge
The five surviving neutral building blanks are all 1995-96 or earlier and already satisfy the historical location-first standard:
- 1986 AMI Classic — Miami, FL
- 1989 McClendon Classic — Chicago, IL
- 1990 Tangerine Tournament x2 — Winter Park, FL
- 1995 UNLV Holiday Classic — Las Vegas, NV

Exact same-game accepted/current-project lookup did not expose stronger registered site evidence. Their event and locality are supported by UCF institutional evidence, and current policy explicitly forbids reopening this historical class solely to drive exact-building blanks to zero once city/state are established. They remain terminal historical enrichment debt.

## Opponent identity
- Source-opponent labels in `opponents.csv`: **474**.
- Distinct canonical opponent identities: **257**.
- Current-D1 identities: **227 distinct / 1,194 games**.
- Working NON_D1/historical identities: **30 distinct / 75 games**.
- Stage 5 owner NON_D1 sanity scan: **APPROVED 2026-09-25; 0 owner flags**.
- Unresolved opponent identities: **0**.
- Stage 6 current-registry comparison found **0** local current-D1 keys missing from the current global registry, **0** local current-D1 keys whose registry status is no longer current D1, and **0** approved NON_D1 keys that collide with a current-D1 registry key.
- Normalized canonical-name/display comparison of the approved NON_D1 population exposed **0** exact current-program name collisions.
- Suspicious historical/non-current identities such as St. Thomas (FL), Centenary, Hartford, Savannah State, St. Francis Brooklyn, Rio Grande, U.S. International, Armstrong State, and Warner University remain supported by the Stage 2 identity evidence; no current-program false merge/split was exposed.
- Informational source typo correction remains: literal `Lipsomb` -> canonical `Lipscomb`.

## Physical venue identity
Stage 6 challenged the local venue rows against the recorded research base and the strongest obvious naming-era evidence.
- Stage 4 local venue rows entering the audit: **54**.
- Stage 6 collapsed **BankAtlantic Center** into the already-existing physical identity `amerant-bank-arena` / research-base `VEN-000009`; BankAtlantic Center is now an alias, not a second local physical venue.
- Final local physical venue rows: **53**.
- Definite research-base physical reuses: **42**.
- Historically resolved identities pending authoritative current-main registration/reuse determination: **11**.
- Ambiguous historical physical identities: **0**.
- Numeric global venue IDs remain intentionally blank until serialized Implementation.

The unresolved global-mapping comparison for Orange County Civic Center is not a historical physical-identity ambiguity: the UCF rows identify a definite Orange County Civic Center physical site in Orlando. Current-main `Orlando Civic Center` reuse remains an Implementation-time shared-reference comparison because the available evidence does not safely prove that those names denote the same building.

The textual source name `UCF Arena` remains era-sensitive and refers to two different physical buildings; game rows are already disambiguated to `The Venue at UCF` for the older arena and `Addition Financial Arena` for the later arena. No unbounded alias is created.

## Postseason taxonomy
- Conference Tournament: **61**
- NCAA Tournament: **7**
- NIT: **8**
- CBI: **3** (stored under controlled `POSTSEASON` game type)
- College Basketball Crown: **4** (stored under controlled `POSTSEASON` game type)
- Postseason exact-site debt: **0**.

## Conference history
Independent (1984-85 through 1989-90) -> American South (1990-91) -> Sun Belt (1991-92) -> Trans America Athletic Conference / TAAC (1992-93 through 2000-01) -> Atlantic Sun (2001-02 through 2004-05) -> Conference USA (2005-06 through 2012-13) -> American (2013-14 through 2022-23) -> Big 12 (2023-24 onward).

The 1992-93 UCF source explicitly states TAAC participation but notes that UCF did not play a full conference schedule, so no conference record is shown. `american-south` and `taac` are historically resolved local conference identities not present in the protected-main global conference registry at the Stage 6 snapshot; authoritative registration/reuse remains serialized Implementation work and Research does not mutate the shared registry.

## Preserved source corrections and contradictions
Accepted field-specific corrections use stronger authoritative evidence without erasing literal `raw_text`. Stage 6 added the 2007 Houston exact-date correction described above. Other supported score/result/date corrections and preserved literal disagreements remain documented per game. No unrelated discrepancy population was reopened.

## Stage 6 pre-freeze adversarial self-challenge
**PRE-FREEZE SELF-CHALLENGE: PASS**

Control Center challenge question: **If the Control Center challenged the largest unresolved/debt populations in this portfolio, what would it challenge?**

It would challenge the four 1986-88 HOME building exceptions, five historical neutral building blanks, exact-date integrity, local physical-venue naming duplicates, the approved NON_D1 population for hidden current programs, and postseason exact-site completeness.

Bounded challenge results:
- **HOME venue debt:** 4 remain; complete Orlando, FL geography; class-level institutional/facility/reciprocal challenge did not safely establish the missing buildings.
- **UNKNOWN H/A/N:** 0.
- **Exact dates:** one invalid serialized date was exposed and repaired (`2007-02-29` -> `2007-02-28`); final blank/invalid exact dates: 0.
- **Neutral exact buildings:** 5 historical location-complete rows remain terminal enrichment debt; no modern neutral building blank survives.
- **Postseason:** all 83 exact sites remain complete; NCAA site gaps 0.
- **Physical venue identity:** duplicate local BankAtlantic Center row collapsed into Amerant Bank Arena; final 53 physical identities, ambiguous historical identities 0.
- **Opponent identity:** owner-approved 30-identity NON_D1 population retained; current-registry comparison exposed no current-D1 collision, known key split, or ambiguous current-program match.
- **Universe/taxonomy:** 1,269 games and the 1,186 + 83 regular/postseason partition remain exact.

Research/package acceptance after Stage 6: **0 errors, 0 warnings**. HOME publication blockers: **0**. NCAA site gaps: **0**. Unaccounted material site gaps: **0**. Ambiguous historical physical venue identities: **0**.

`RESEARCH_FROZEN` remains **NO** until separately authorized Stage 7 immutable packaging.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=e8e870a16da17c5d3e723ae214e27ffba1f9a82d` from `research_base_sha=5c91e35485060a0be27f9612d0b140883a555dbf`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

Owner-authorized Stage 1 conference-history reconciliation was applied during current-main integration; the exact correction specification and hash are recorded in the Integration Freeze manifest.
