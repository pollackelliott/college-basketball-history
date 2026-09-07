# Oklahoma State research portfolio notes

## Stage 6 research status and scope

This six-file portfolio is the **Stage 6 post-self-challenge Research-lane package** assembled against `research_base_sha=c6be3bc78b4f777f731735a03cbbd5ad418f04a7`. The owner approved the complete 87-identity `NON_D1` sanity scan in Stage 5. The required adversarial pre-freeze self-challenge has now been performed and passed, but the package is **not yet RESEARCH_FROZEN** until the Stage 7 immutable package/hash boundary. No serialized Implementation, canonical ingestion, current-main mutation, or publication has been performed.

- Owner-approved history scope: **INCEPTION+**
- History start season: **1907-1908**
- Coverage: **1907-08 through completed 2025-26**
- Competitive games: **3,067**
- On-court record: **1,783-1,284**
- Played seasons: **117**
- No-team seasons: **1910-11, 1913-14**
- Exhibitions: **excluded**
- Unknown exact dates: **2**
- Unknown played score pairs: **2**
- Unresolved opponent identities: **0**

## Game-universe/source corrections

The controlling ledger preserves literal Oklahoma State source evidence while applying only evidence-supported structured corrections.

- Two stray duplicate Saint Louis rows printed inside the 1972-73 game block were excluded as source bleed; the legitimate 1949-50 Saint Louis game remains.
- The 1912-13 game-by-game section header prints 3-6, but the nine listed games and year-by-year summary reconcile 4-5.
- The 2000-01 game-by-game section header prints 23-9, but the 30 listed games and year-by-year summary reconcile 20-10.
- Two 1907-08 Tulsa games retain unknown exact dates.
- Two January 1920 Chilocco losses retain unknown played scores.
- Administrative forfeits/vacated results are preserved in `administrative_note`; public/history totals use played on-court results.

## Opponent identity

All 3,067 games resolve to canonical opponent identities.

- Source opponent labels: **347**
- Canonical opponent identities: **324**
- Current-D1 identities: **237**
- Working `NON_D1` identities: **87**, covering **354 games**
- Known current-program splits: **0**
- Ambiguous current-program matches: **0**

Six game-level source-name defects were corrected in structured identity while literal labels remain preserved: two `McMurry` rows resolve to MacMurray College (Illinois), three `Trinity (TX)` / `Trinity` rows resolve to Trinity College (Conn.), and one `Santa Fe College` row resolves to College of Santa Fe.

## Conference history

- Independent: **1907-08 through 1920-21**
- Southwest Conference: **1921-22 through 1924-25**
- Missouri Valley: **1925-26 through 1956-57**
- Independent: **1957-58**
- Big Eight: **1958-59 through 1995-96**
- Big 12: **1996-97 onward**

The one-season 1957-58 Independent interval is preserved because the media guide explicitly lists that season as Independent rather than back-projecting the Big Eight era.

## Accomplishment verification for later serialized Implementation

The current global baseline row is numerically supported by Oklahoma State's institutional source after resolving one source arithmetic defect:

- Conference regular-season championships: **19**
- Conference tournament championships: **4**
- NCAA Tournament appearances: **29**
- Final Four appearances: **6**
- National championships: **2**
- Best NCAA finish: **NATIONAL_CHAMPION**
- Most recent best-finish year: **1946**

The media guide headline prints `18` regular-season conference championships, but its own listed components are 1 Big 12 + 2 Big Eight + 15 Missouri Valley + 1 Southwest Conference = **19**. The package documents the headline as an internal arithmetic defect rather than changing the component history to force 18.

## H/A/N and regular-season site completeness

H/A/N is based on explicit game-level source notation/context and is independent of venue geography.

Final package H/A/N totals:
- `SOURCE_PROGRAM_HOME`: **1,384**
- `OPPONENT_HOME`: **1,180**
- `NEUTRAL`: **503**
- `UNKNOWN`: **0**

Oklahoma State home physical-venue history is complete:
- Oklahoma A&M Original Armory
- Oklahoma A&M New Armory
- Gallagher-Iba Arena, beginning 1938-12-09

Home rows missing venue: **0**
Home rows missing city/state: **0**
Home publication blockers: **0**

Stage 3B corrected 54 December rows from 1958-59 through 1975-76 to `REGULAR_SEASON`: the season legends identify them as the Big Eight Holiday Tournament in Kansas City, not postseason.

Stage 6 adversarial review materially reduced the regular-season neutral building debt. It recovered all 54 Big Eight Holiday Tournament buildings (Municipal Auditorium through the 1973 event; Kemper Arena beginning in 1974) and 27 modern neutral-site buildings from official school/event evidence.

Regular-season neutral rows still missing physical venue: **178**. The only 2000s residuals are the two 2006 South Padre Island Invitational games, for which official material establishes South Padre Island but did not establish an exact physical building. All other residual regular-season neutral venue blanks are 1990s or earlier, have complete city/state, and carry explicit `RESEARCHED_PARTIAL` accounting.

## Postseason

Final postseason population:
- Conference Tournament: **85**
- NCAA Tournament: **67**
- NIT: **30**
- Other `POSTSEASON`: **9**
- Total postseason: **191**

All **67 NCAA Tournament games have physical venue + city + state**. Historical NCAA consolation/third-place games retain blank controlled round when appropriate.

All **85 conference-tournament games have complete physical venue + city/state**. Early Big Eight campus preliminary rounds are handled game by game rather than bulk-assigned to the shared Kansas City site.

Stage 6 reciprocal review recovered all four previously blank road-NIT buildings: 1989 St. John's at Alumni Hall/Carnesecca Arena, 2006 Miami at BankUnited Center/Watsco Center, 2008 Southern Illinois at SIU Arena/Banterra Center, and 2023 Youngstown State at Beeghly Center. It also recovered the 1939 Oklahoma NCAA District Playoff at Oklahoma City Municipal Auditorium from Oklahoma State's official Oklahoma City history.

Exactly **8** non-NCAA postseason rows retain an unresolved physical building: two 1936 District Olympic Trials rows and six 1939-49 NCAA District Playoff rows. Each surviving row has complete city/state and explicit research accounting. Unaccounted material postseason site gaps: **0**.

## Venue identity / rebase rule

This Stage 6 package contains **89 physical venue relationship rows**: **80** definite research-base physical reuses and **9** genuinely new physical-venue candidates with provisional `VEN-99xxxx` identifiers. The new-candidate list is:

- Oklahoma A&M Original Armory
- Oklahoma A&M New Armory
- Oklahoma City Municipal Auditorium
- Tulsa Convention Center

- Valley High School (Las Vegas)
- Carnesecca Arena / Alumni Hall (Queens)
- Watsco Center / BankUnited Center (Coral Gables)
- Banterra Center / SIU Arena (Carbondale)
- Zidian Family Arena at Beeghly Center (Youngstown)

The Oklahoma City Municipal Auditorium candidate is documented as the same physical building later called Civic Center Music Hall. The Tulsa Convention Center candidate is documented through later Cox Business Center/Convention Center and Arvest Convention Center naming eras. No matching physical rows existed in the recorded research-base registry, so they remain new candidates rather than aliases of an existing global venue.

Those numeric IDs are transport-only. Serialized Implementation must rebase all venue identities against then-current protected main before tracked Phase 0 and allocate final numeric IDs only for genuinely new physical venues.

The research-base registry contains duplicate Palace of Auburn Hills identities. Oklahoma State research treats the underlying building as unambiguous and uses established `VEN-000206`; the duplicate-key residue is an Implementation cleanup concern, not a historical ambiguity.

## Owner-authorized conference tournament workbook

`Conference_Tournament_Site_Reference(20260907-005551).xlsm` is **not global project truth**. The owner authorized it only for Oklahoma State's conference-membership/tournament history, where it is treated as complete for this school's relevant scope. This limitation must survive Implementation.

## Stage 5 owner disposition

The owner approved the complete Stage 5 `NON_D1` sanity scan as presented: **87 identities / 354 games**. No Stage 5 identity repair was requested.

## Stage 6 adversarial self-challenge

`PRE-FREEZE SELF-CHALLENGE: PASS`.

The challenge concentrated on the largest remaining debt rather than rerunning settled research. It produced **86 game-level physical-venue recoveries**:
- 54 Big Eight Holiday Tournament rows;
- 27 modern regular-season neutral rows;
- 4 road NIT rows;
- 1 1939 NCAA District Playoff row.

These repairs do not change game identity, date, opponent, score, result, H/A/N, conference membership, or game type. They only replace previously research-accounted venue blanks with stronger physical-building evidence.

Final material site-gap rows: **186**, all researched/accounted. HOME blockers: **0**. NCAA Tournament site gaps: **0**. UNKNOWN H/A/N: **0**. Ambiguous physical venue identities: **0**.

## Next required checkpoint

Stage 7 — immutable six-file package/hash and `RESEARCH_FROZEN` declaration.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=19a451c9089f1d404f84ecf754dd52f0d447c616` from `research_base_sha=c6be3bc78b4f777f731735a03cbbd5ad418f04a7`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
