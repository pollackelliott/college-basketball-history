# Rutgers research notes

## Research scope and freeze basis

Rutgers is treated as **always top-level / Division I for project purposes** beginning with the program's inaugural 1906-07 varsity season, per the owner's explicit scope ruling. The competitive package contains **2,696 games** through the completed 2025-26 season and represents an on-court record of **1,361-1,335**. Exhibitions are excluded.

This portfolio was rebuilt fresh under current repository research policy. Earlier Rutgers research/onboarding artifacts were treated only as non-authoritative leads. No stale portfolio conclusion was accepted without re-establishing it from the current Rutgers guide, current repository conventions, owner-authorized tournament reference, or independent institutional/archival evidence.

## Conference chronology and the ECAC issue

Rutgers' primary membership chronology is:

- Independent: 1906-07 through 1975-76
- Eastern Eight: 1976-77 through 1981-82
- Atlantic 10: 1982-83 through 1994-95
- Big East: 1995-96 through 2012-13
- American: 2013-14
- Big Ten: 2014-15 onward

The **1975 and 1976 ECAC Metropolitan tournaments do not create an ECAC conference-membership interval**. Rutgers remained an independent. The ECAC's Division I regional tournaments functioned as postseason NCAA qualifying tournaments, and Rutgers won the Metropolitan event in both 1975 and 1976. Owner ruling (2026-09-02): those four Rutgers games are classified `CONFERENCE_TOURNAMENT` while the `conferences.csv` membership chronology remains Independent. This is an explicit functional-historical taxonomy choice: the ECAC was not a conventional Rutgers membership conference, but the Metropolitan tournament functioned as the regional championship/NCAA automatic-bid mechanism. The event name is preserved as `ECAC Metropolitan Tournament`. Non-title rounds remain blank under project round vocabulary; the two St. John’s title games are `Championship`.

Atlantic 10 official historical records establish Rutgers regular-season conference championships in **1977, 1978, 1980 and 1983** (including divisional/shared titles) and tournament championships in **1979 and 1989**. The older Rutgers narrative describing the 1988-89 team as winning the Atlantic 10 title is consistent with the official tournament record.

## Postseason

The package classifies:

- 4 National AAU Tournament games in 1920 as generic `POSTSEASON`; Rutgers finished runner-up. Contemporary Atlanta reporting places every game at the Atlanta Auditorium.
- 4 ECAC Metropolitan Tournament games (1975 and 1976) as `CONFERENCE_TOURNAMENT` while Rutgers was Independent.
- Eastern Eight / Atlantic 10, Big East, American and Big Ten tournament games as `CONFERENCE_TOURNAMENT` using official conference records and the authorized site workbook.
- 15 NCAA Tournament games with complete physical venue and city/state.
- 31 NIT games.
- the 2026 College Basketball Crown loss to Creighton as generic `POSTSEASON`.

Authoritative NCAA accomplishment values for later Owner Gate verification:

- NCAA Tournament appearances: **8** (1975, 1976, 1979, 1983, 1989, 1991, 2021, 2022)
- Final Fours: **1** (1976)
- NCAA national championships: **0**
- Best NCAA finish: **Final Four**
- Best-finish year: **1976**
- Conference regular-season championships: **4** (1977, 1978, 1980, 1983; shared/divisional titles included per official A-10 historical champion table)
- Conference tournament championships: **4** under project taxonomy (1975 ECAC Metropolitan, 1976 ECAC Metropolitan, 1979 Eastern Eight/A-10, 1989 Atlantic 10)

The Rutgers guide's postseason summary heading `NCAA Appearances (6-9)` is a game W-L tally, not an appearance count. Its 1976 Connecticut line also contains an internal score typo (`Rutgers 93, Connecticut 97`); the chronological game ledger and Rutgers historical narrative establish Rutgers' 93-79 win, which is retained.

## Site research and home facilities

H/A/N was researched at game level. The hierarchy was: explicit/current official schedule or postseason evidence; explicit `at`/`vs` syntax in the Rutgers chronological ledger; Rutgers series H/A/N evidence; then the guide's stable unprefixed-home listing convention where independently validated against season/site summaries. Geography was never used to manufacture H/A/N.

A material stale-artifact defect was caught and rejected: the Jan. 14, 1930 Drexel game is explicitly `at Drexel` in the current Rutgers ledger, so it is AWAY even though an older Rutgers series table/stale package had treated it as home.

Rutgers' institutional facility history and historical building-by-building totals support these home eras:

- Ballantine Gymnasium through the Dec. 7, 1929 Crescent A.C. game;
- Highland Park Gym / Masonic Hall after the Jan. 30, 1930 Ballantine fire through 1930-31;
- College Avenue Gym beginning Jan. 6, 1932 and through 1976-77;
- Rutgers Athletic Center / current Jersey Mike's Arena beginning 1977-78.

Facility chronology is used **only after** a row is independently established as Rutgers home. It never establishes H/A/N. The Jan. 28, 2017 Wisconsin game is preserved as a Rutgers home game at Madison Square Garden from Rutgers' official schedule rather than being forced into the RAC/Jersey Mike's chronology.

All 1,398 Rutgers HOME rows have a physical venue and complete city/state in this research package. Remaining neutral gaps are explicit researched unknowns rather than silent blanks.

## Administrative / source normalization notes

The Dec. 4, 1973 Pittsburgh contest is stored with the 36-21 score at stoppage and Rutgers loss, with `FORFEIT` administrative metadata; Rutgers' raw guide wording `L FORFEIT` remains preserved.

The scoreless 1907-08 Fordham row preserves the current Rutgers guide's `W default` wording with blank numerical scores. No score is invented.

The official Rutgers 2004-05 season schedule resolves the media-guide chronological date typo for Providence to Jan. 19, 2005; raw source text is retained unchanged.

## Site-gap accounting

Material site-gap rows: **140**. Every one carries paired `site_research_status` and substantive `site_research_basis`. Unaccounted material site gaps: **0**. NCAA site gaps: **0**.


## Residual neutral-site debt after self-challenge

The final pre-freeze pass recovered the six latest unresolved neutral regular-season physical sites (all 1999-00): the three USBWA Hoop & Quill Classic games at Family Arena in St. Charles, Missouri; Florida at Continental Airlines Arena / Brendan Byrne Arena in East Rutherford; and the Hofstra/Siena ECAC Holiday Festival games at Madison Square Garden. The remaining neutral-site blanks are historical, concentrated before 2000, and carry `RESEARCHED_UNRESOLVED` accounting after the Rutgers chronological ledger, all-time series evidence, owner-authorized conference-tournament site reference where applicable, and targeted institutional/reciprocal/postseason research were checked. No NCAA site is unresolved and no HOME physical venue or location is unresolved.

`PRE-FREEZE SELF-CHALLENGE: PASS`

## Post-freeze canonical-round compatibility normalization

Current implementation policy permits `Championship` or blank
`curated_postseason_round` for NIT and generic `POSTSEASON` games. The frozen
Rutgers research portfolio contained 33 verified non-championship historical
round labels in that curated field.

For exactly those 33 rows, implementation preserved the researched historical
round label in the row-level `notes` field and blanked only
`curated_postseason_round`, consistent with current project schema.

No game, date, opponent identity, score/result, game type, tournament identity,
H/A/N classification, venue, city/state, raw source text, or research evidence
was changed. The immutable original RESEARCH_FROZEN ZIP remains preserved at
SHA-256
`a3888277f23e7a22aec6032da7b1b3b2692f746925a269a8b652f80392e0115b`.

## Current-main integration rebase

Current-main physical-venue identity review mechanically normalized two
research-time venue keys without changing physical venue identity:

- `civic-arena-pittsburgh` -> `mellon-arena` (`VEN-000241`), preserving
  Civic Arena / Pittsburgh Civic Arena / Mellon Arena as names of the same
  Pittsburgh physical building.
- `hagan-arena` -> `alumni-memorial-fieldhouse-saint-josephs`
  (`VEN-000302`), preserving Alumni Memorial Fieldhouse / Hagan Arena as
  names of the same Saint Joseph's physical building.

The remaining venue audit produced 38 other exact current-main key reuses and
16 physical identities absent from the current global venue/name registries;
those 16 are eligible for authoritative new global IDs during Phase 0.

### NON_D1 owner sanity scan

On 2026-09-03, Elliott approved the complete fresh Rutgers NON_D1 opponent
population unchanged after implementation review: 71 distinct normalized
identities covering 330 games. No identity correction was requested.

The immutable original RESEARCH_FROZEN transport artifact remains preserved at
SHA-256
`a3888277f23e7a22aec6032da7b1b3b2692f746925a269a8b652f80392e0115b`.

These implementation normalizations do not reopen Rutgers research or alter
the game universe, dates, opponents, scores/results, site classifications,
postseason classifications, physical venues, or research evidence.

### MGM Grand Garden Arena geography normalization

Current main identifies MGM Grand Garden Arena as physical venue `VEN-000133`
with project geography `Paradise, NV`. Fresh Rutgers research used the common
Las Vegas locality label.

Implementation normalized the Rutgers MGM Grand venue relationship and its
five affected normalized game-location rows from `Las Vegas, NV` to
`Paradise, NV` solely to agree with the authoritative current-main physical
venue registry.

Affected source game IDs:

- `RUTRAW-02348`
- `RUTRAW-02349`
- `RUTSUP-006`
- `RUTSUP-007`
- `RUTSUP-034`

The physical venue, H/A/N classification, game identity, dates, opponents,
scores/results, postseason classification, and underlying research evidence
are unchanged.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=d387d0e01b1d9930b72cdffb167595f3ac560d48` from `research_base_sha=6dc3910f68914c139097e9352481cb67a19cb2df`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

### Madison Square Garden alias disambiguation

Implementation preflight correctly rejected the generic alias `MSG` after
Rutgers Phase 0 caused it to resolve to two distinct physical Madison Square
Garden buildings.

The physical venue assignments were already correct and remain unchanged:

- `VEN-000123` — Madison Square Garden III / 1925 building; Rutgers assigned
  games are in 1967.
- `VEN-000124` — Madison Square Garden IV / 1968-current building; Rutgers
  assigned games begin in 1969.

The generic `MSG` alias remains registered only to `VEN-000124`, as it was on
protected main before Rutgers Phase 0. The Rutgers 1925-building relationship
retains the unambiguous historical alias `Madison Square Garden III`.

No game identity, date, score/result, H/A/N classification, venue assignment,
location, or underlying research evidence changed.

### Pre-Gate releaseability technical cleanup

Implementation's pre-Gate releaseability challenge identified a deterministic
media-guide parsing defect in nine overtime games. In each case the raw
Rutgers result string clearly marked overtime, but the parsed
`overtime_periods` field had captured the losing score (for example,
`61-54 OT` became `54`). Those nine fields were normalized directly from the
preserved raw result strings. No score/result, opponent, date, site,
venue, game type, or game identity changed.

The same challenge also identified 34 false-positive exhibition warnings.
The completed 2025-26 supplement notes used the phrase `exhibitions excluded`,
which itself triggered the generic exhibition-wording warning. That provenance
was reworded to `competitive games only`; the 34-game competitive supplement
and its game data are unchanged.

### Pre-Gate full-ledger releaseability corrections

A full 2,696-row implementation audit was performed after ordinary preflight
reached zero blockers and zero warnings. This audit intentionally challenged
rows predicted to become new canonical games, because those rows do not
generate ordinary reciprocal discrepancies.

The audit identified and repaired a bounded set of source-normalization
defects supported by institutional, conference, reciprocal, or independently
cross-checked historical evidence:

- Fordham 1978: corrected Rutgers home -> opponent home.
- Penn State Feb. 27, 1979: corrected date, Rutgers-home site, RAC physical
  venue, and Eastern Eight conference-tournament classification.
- UCLA 1981 and Michigan 1983: recovered Meadowlands/Brendan Byrne Arena.
- Penn State 1989 A-10 title: corrected neutral -> Rutgers home at the RAC;
  score remains 70-66.
- Lafayette 1989: corrected OCR-corrupted `768-619` to Rutgers 78-64.
- Illinois 2016: corrected Rutgers score to 101 in the 110-101 3OT loss.
- Minnesota 2017: corrected Rutgers home -> opponent home.
- Michigan State 2018: restored one overtime.
- Wisconsin 2021: corrected opponent home -> Rutgers home at the RAC.
- Minnesota 2021: corrected score to Rutgers 76-72.
- Indiana 2021 Big Ten Tournament: corrected score to Rutgers 61-50.
- Mississippi State 2023: corrected to neutral at Prudential Center, Newark.
- Nebraska 2024: restored one overtime.
- Notre Dame / Alabama / Texas A&M 2024 Players Era games: corrected to
  neutral at MGM Grand Garden Arena; Notre Dame also restored one overtime.
- Michigan State 2025: corrected to designated Rutgers home at Madison Square
  Garden.
- Minnesota 2025: restored one overtime.
- USC 2025 Big Ten Tournament: restored two overtimes.

The Feb. 10, 2021 Iowa row was specifically reviewed and was not changed:
Rutgers' normalized 66-79 loss is supported by Iowa official evidence, while
the contradictory `79-56` media-guide string remains preserved as raw source
text with its existing correction note.

The Rutgers accomplishment baseline was also corrected from five to four
regular-season conference championships. The Atlantic 10 official annual
champions table supports Rutgers titles in 1977, 1978, 1980 and 1983.
The accomplishment row deliberately remains `OWNER_BASELINE_UNVERIFIED`
pending the normal Owner Gate.

### Final pre-Gate historical cleanup

A final implementation pass resolved six deterministic source-side items before
Owner Gate 1:

- Missouri, Dec. 15, 1966: recovered the neutral physical site as Madison
  Square Garden III / the 1925 building; the already-correct 3OT result is
  preserved.
- USC, Dec. 27, 1974: recovered the ECAC Holiday Festival physical site as
  Madison Square Garden; the Rutgers-versus-USC one-day date conflict remains
  intentionally unresolved for owner review.
- Louisville Holiday Classic, 1976: corrected Rutgers-Louisville to Dec. 28
  and Rutgers-Auburn to Dec. 29 using the Louisville and Auburn official
  schedules. Louisville, Kentucky and tournament identity are recorded;
  Auburn-Rutgers physical-building detail remains researched unresolved.
- ECAC Holiday Festival, 1978: recovered Madison Square Garden for both the
  St. John's semifinal and Ohio State championship, and corrected the
  Ohio State game from 1 OT to the institutionally documented 3 OT.

These repairs do not collapse genuine reciprocal historical disagreements.
Institutional date/score/OT conflicts that remain after this pass are left for
the sealed discrepancy workflow.

### Scoreless default-win administrative normalization

The pre-seal full-transaction rehearsal exposed one repository-vocabulary
mismatch in `RUTRAW-00007`, Rutgers' historical scoreless win over Fordham by
default.

The underlying historical assertion is unchanged: Rutgers is recorded as the
winner, the score is unknown, and the preserved raw source text says `default`.
Implementation normalized only `administrative_status` from the research-time
label `DEFAULT` to the project's existing canonical taxonomy `FORFEIT`.

Rutgers already contained one separate valid `FORFEIT` source row; that row
was explicitly preserved unchanged. After normalization the source ledger
contains two `FORFEIT` administrative rows and no `DEFAULT` rows.

No game identity, result, score, opponent, date, or site fact was changed.
