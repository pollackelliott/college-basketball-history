# BYU men's basketball research notes

## Status and coverage
- School: BYU
- Source program key: `byu`
- Research base SHA: `e5078cd6b57d68f59048f32b7dace422544eff9f`
- Owner-confirmed history scope: `INCEPTION+`
- First covered season: 1902-03
- Final covered season: 2025-26
- Competitive games: 3,157
- Resolved on-court record: 1,985-1,171, plus one administrative-forfeit row whose separate on-court result is unsupported
- Stages 1-3B: COMPLETE
- Stage 4 six-file assembly/package QA: COMPLETE
- Stage 5 owner NON_D1 sanity scan: APPROVED — 135 identities / 327 games / 0 owner flags
- RESEARCH_FROZEN: YES

## Core curation decisions
- The official BYU 2025-26 Men's Basketball Almanac controls the historical game universe through 2024-25; the official completed 2025-26 schedule supplies 35 competitive games.
- Two 2025-26 exhibitions are excluded.
- Played/on-court results remain distinct from forfeits and vacated results.
- H/A/N is independently researched and never inferred from venue.

## Narrow extraction/date repairs
- 1965 NCAA dates: BYU-UCLA is corrected to 1965-03-12 and BYU-Oklahoma City to 1965-03-13 from current official BYU schedule plus NCAA bracket evidence.
- 1972 NCAA vs Long Beach State: rendered primary BYU guide p. 77 / PDF p. 78 clearly reads 90-95 L in overtime. The earlier 0-95 value was a PDF text-extraction artifact; only the team score was repaired and game identity is unchanged.

## Home venue chronology
BY Academy Training School Men's Gymnasium -> Ladies Gymnasium (Women's Gymnasium) -> Springville High School Gymnasium -> split 1950-51 home season including Einar Nielsen Fieldhouse -> Smith Fieldhouse -> Marriott Center.
All 1,499 HOME rows across the final game universe have complete venue and location support; HOME publication blockers = 0.

## Site completeness
- Final H/A/N: 1,499 SOURCE_PROGRAM_HOME / 1,299 OPPONENT_HOME / 359 NEUTRAL / 0 UNKNOWN.
- NCAA Tournament: 53 games; venue/location gaps = 0.
- Conference Tournament: 83 games.
- NIT: 33 games.
- Other POSTSEASON: 25 games.
- Research-accounted material exact-building gaps: 191, consisting of 188 regular-season neutral rows and 3 non-NCAA postseason rows.
- Unaccounted material site gaps: 0.
- The 1932 and 1933 neutral Utah playoff rows retain only state-level source knowledge; normalized city/state remain blank rather than inventing an atomic geography pair.
- The 1967 neutral WAC playoff vs Wyoming is established in Salt Lake City, UT; exact building remains unresolved.

## Conference history
Independent (1902-03-1916-17) -> Rocky Mountain Conference (1917-18-1936-37) -> Mountain States Conference (1937-38-1961-62) -> WAC (1962-63-1998-99) -> Mountain West (1999-00-2010-11) -> WCC (2011-12-2022-23) -> Big 12 (2023-24-present).

The updated owner conference-tournament venue workbook supplied 2026-09-14 was used for all 83 BYU conference-tournament rows. It newly includes the WAC and WCC populations that were absent from the earlier workbook. BYU's WAC tournament history includes campus/host-site and Las Vegas-era variation; the Mountain West tournament is primarily Las Vegas with the documented Denver interlude; BYU's WCC tournament appearances are at Orleans Arena; Big 12 tournament rows use T-Mobile Center.

## Postseason classification
- 83 `CONFERENCE_TOURNAMENT`
- 53 `NCAA_TOURNAMENT`
- 33 `NIT`
- 25 `POSTSEASON` (21 early conference playoff/championship-series games plus 4 NAIA national-tournament games)
Controlled NCAA rounds follow repository taxonomy; conference/NIT/other title games alone receive `Championship`.

## Administrative actions
Administrative metadata is preserved separately from played truth: 2 `FORFEIT`, 47 `VACATED_WIN`, and 2 `VACATED_GAME` rows.

## Opponent identity
- 3,157 games are mapped to resolved opponent identities.
- 942 distinct literal source opponent labels map through the package audit.
- Working NON_D1/historical census: 135 identities / 327 games.
- Unresolved opponent identities: 0.
- Known current-program key splits: 0.
- Ambiguous current-program matches: 0.
- Formal owner NON_D1 sanity scan remains pending Stage 5.

## Program accomplishments
Authoritative BYU history and the completed 2025-26 season support the current baseline unchanged: 29 regular-season conference championships, 3 conference-tournament championships, 33 NCAA appearances, 0 Final Fours, 0 national championships, and best finish Elite Eight (1981).

## Physical venue identity
Research-local numeric/global venue IDs remain intentionally blank. Same-building naming eras were normalized where established, including Madison Square Garden III versus the current Madison Square Garden IV and Sprint Center/T-Mobile Center. Serialized Implementation must perform the authoritative current-main physical-identity rebase.

## Known unresolved questions
No owner-level historical question blocks Stage 4. Surviving site gaps are explicit researched historical debt, not silent blanks.

## Public presentation
The required Stage 5 owner NON_D1 sanity scan was approved by the owner on 2026-09-14 with 0 flags. The package is ready for Stage 6 adversarial pre-freeze self-challenge. It is not yet `RESEARCH_FROZEN`.


## Stage 5 owner NON_D1 sanity scan
- Owner decision: **APPROVED** on 2026-09-14.
- Complete distinct NON_D1/historical population reviewed: **135 identities / 327 games**.
- Owner flags: **0**.
- No opponent normalization changed in Stage 5.


## Stage 6 pre-freeze adversarial self-challenge
**PRE-FREEZE SELF-CHALLENGE: PASS**

The audit found one real systematic omission class: all **61** still-unresolved neutral-site rows from 2000 onward had exact venue evidence available on official BYU season schedule/event pages. Those 61 rows were repaired as one bounded batch without changing H/A/N, game identity, opponent identity, score, result, or postseason classification.

Additional physical-reference repairs:
- `Spokane Arena` was reconciled to the same physical building now registered as `numerica-veterans-arena`; no duplicate BYU physical identity remains.
- Michelob ULTRA Arena normalized geography was corrected from event shorthand Las Vegas to the current shared physical municipality, Paradise, Nevada.
- Naming-era aliases such as Compaq Center/The Summit, Ford Center/Paycom Center, Staples Center/Crypto.com Arena, Tim's Toyota Center/Findlay Toyota Center, and Glens Falls Civic Center/Harding Mazzotti Arena are treated as physical-building continuity, not separate venues.

Final residual site debt:
- HOME venue/location gaps: **0**
- UNKNOWN H/A/N: **0**
- NCAA site gaps: **0**
- neutral exact-building gaps: **130**, all pre-2000
- regular-season neutral exact-building gaps: **127**
- non-NCAA postseason exact-building gaps: **3**
- unaccounted material site gaps: **0**

Exact-date debt:
- working count entering Stage 6: **22**
- recovered in Stage 6: **0**
- final count: **22**
- all surviving blanks are in 1918-19 through 1927-28 and remain terminal researched historical debt. The two 1927-28 Utah State rows were specifically challenged; conflicting historical BYU date evidence makes an exact-date assignment unsafe.

Physical venues:
- local physical venue rows: **81**
- definite current-main reuses: **65**
- genuinely new current-main candidates: **16**
- ambiguous physical identities: **0**

Opponent identities:
- modern/current-snapshot NON_D1 identities specifically challenged: **15**
- current-program key splits found/repaired in Stage 6: **0**
- ambiguous current-program matches: **0**
- Stage 5 owner approval remains controlling.

No further comparable systematic/high-yield evidence class remains for the residual historical site/date populations. Under the repository convergence policy, the surviving debt is terminal researched historical debt rather than a trigger for another row-by-row research cycle.


## Stage 7 immutable research freeze
- Final six-file Research package was frozen on 2026-09-14.
- Stage 5 owner NON_D1 sanity scan: APPROVED — 135 identities / 327 games / 0 flags.
- Stage 6 adversarial self-challenge: PASS.
- Research acceptance errors: 0.
- Research acceptance warnings: 0.
- HOME publication blockers: 0.
- NCAA site gaps: 0.
- Unaccounted material site gaps: 0.
- Ambiguous physical venue identities: 0.
- Known current-program opponent key splits: 0.
- Ambiguous current-program opponent matches: 0.
- `RESEARCH_FROZEN: YES`.
- `CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`.
- Numeric/global venue IDs remain provisional until serialized Implementation performs the authoritative current-main rebase.

## Stage 1 current-main normalization

Integration-only normalization against protected main:

- 61 fully resolved neutral-site rows used the obsolete Research-only
  `site_research_status=RESOLVED` token. Their research basis was preserved
  in each source row's `notes`, and the two unresolved-debt accounting
  fields were cleared to satisfy the current schema;
- `einar-nielsen-fieldhouse` reuses current global
  `nielsen-fieldhouse` / `VEN-000582`;
- `state-farm-field-house` reuses current global
  `hp-field-house` / `VEN-000084`, while frozen BYU game assertions
  preserve institutional `Kissimmee, FL` source locality;
- the established project-facing Paradise, Nevada convention
  normalizes the four affected resolved venue/site localities to
  `Las Vegas, NV`;
- current program key `new-orleans` retains its key and uses
  protected-main display identity `LSU New Orleans`.

No settled BYU H/A/N, game identity, result, date, postseason,
NON_D1 disposition, or historical venue conclusion is changed.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=94200663bf7b1ddf12ddd7a02f82695b96c9e5f7` from `research_base_sha=e5078cd6b57d68f59048f32b7dace422544eff9f`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
