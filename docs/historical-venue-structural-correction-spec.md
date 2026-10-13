# Historical venue structural correction specification

Status: PLANNING COMPLETE — MUTATION NOT YET AUTHORIZED

Protected-main basis: `49207239a9336f0433cc8289fff0e1cec149db0f`

This specification is the durable declared-intent contract for the structural-correction portion of the historical venue-name exercise. It does not authorize mutation by itself. Refresh protected main before execution; if main has moved, preserve the historical conclusions but rebuild and reseal all mechanical counts/fingerprints against current main.

## Governing invariants

- One physical venue = one stable `venue_id`.
- Literal historical source wording in `source-games.csv`, raw text, and durable evidence must not be rewritten merely to normalize a curated/global identity.
- Shared-reference mutation requires repository validation plus declared-intent diff validation.
- Generated site state must be rebuilt and freshness-checked inside the same transactional/rollback boundary as source/reference changes.
- Never merge IDs from name similarity alone.
- Exact official naming periods require exact boundaries and accepted source basis.
- A corrected stable venue key may rewrite curated/global dependent keys and provenance markers, but must not alter game identity, opponent identity, H/A/N, score, result, date, or literal source evidence.

## Transaction architecture

### Transaction A — duplicate physical identity merge

Use the existing permanent `tools/venue_identity_transaction.py` unchanged for Seattle.

Declared merge:

- survivor: `VEN-000102` (`keyarena`)
- absorbed: `VEN-000315` (`climate-pledge-arena`)
- historical conclusion: same Seattle Center arena lineage
- expected school venue rows using absorbed ID on this protected-main basis: **5**
  - Arizona
  - Maryland
  - Oregon
  - UCLA
  - UConn
- expected canonical rows using absorbed ID on this protected-main basis: **0**
- expected game-assertion rows using absorbed ID/key on this protected-main basis: **0**
- expected NCAA-site evidence rows using absorbed ID/key on this protected-main basis: **0**

The existing transaction owns retirement of `VEN-000315`, dependent school-row rebinding, global-name reassignment/deduplication, any canonical/assertion/NCAA rewrites discovered at replan time, deterministic site rebuild, freshness proof, validation, postconditions, and rollback.

### Transaction B — generic intent-constrained non-merge correction

Add one permanent generic transaction capability rather than one-off scripts. It must support a declarative spec containing:

- expected protected-main SHA and exact input fingerprints;
- stable-ID global venue row correction, including `venue_key`, display, geography/date metadata when explicitly declared;
- exact global venue-name add/update/delete;
- exact school-local venue-row add/update/delete;
- declared source-game curated-field rules with exact predicates and expected match counts;
- optional new global physical-venue registration with collision/next-ID checks;
- canonical/assertion/NCAA venue-key or venue-ID rewrite only where explicitly caused by a declared stable-ID/key correction;
- exact provenance-marker rewrite when a curated registry key changes;
- immutable-field protection for literal source-game/source-evidence fields;
- generated site rebuild plus freshness check;
- `tools/validate_data.py` and targeted regression tests;
- declared-intent changed-file/row postconditions;
- all-or-nothing rollback on any mismatch or validation failure;
- a read-only `plan` command that emits counts, fingerprints and a sealed plan hash;
- an `apply` command requiring the exact sealed plan hash plus explicit `--apply`.

The following seven non-merge families belong in one coherent correction spec.

## Nielsen / Smith — keep IDs distinct

Authoritative identities:

- `VEN-000382` = Smith Fieldhouse, Provo, UT.
- `VEN-000582` = Einar Nielsen Fieldhouse, Salt Lake City, UT.

Declared changes:

- delete global `VEN-000382` alias `Nielsen Field House`;
- remove the same false curated alias from Utah's `VEN-000382` school-local row;
- leave `VEN-000582` intact, including its valid Einar Nielsen identity;
- leave literal source-game/evidence wording unchanged.

No venue-ID merge is permitted.

## Rice — correct two stable physical identities

`VEN-000554` remains the 1950 Rice building represented by Rice Gymnasium / Autry Court and later Tudor Fieldhouse.

Declared `VEN-000554` changes:

- remove the false unrestricted global alias `Rice Field House`;
- remove `Rice Field House` from Houston's school-local `VEN-000554` aliases;
- retain accepted Rice Gymnasium / Rice Gym / Autry Court identity wording that refers to the 1950 building.

`VEN-000564` is corrected to the older pre-1950 Rice Field House physical identity.

Declared `VEN-000564` changes:

- stable ID remains `VEN-000564`;
- global key becomes `rice-field-house`;
- global project display becomes `Rice Field House`;
- Texas Tech's sole `VEN-000564` school-local row is corrected to the same stable key/display;
- the 1947-12-08 Texas Tech source's literal `Rice Gymnasium` wording remains preserved in source/evidence provenance and must not be promoted to an unrestricted global alias for the older building.

No merge between `VEN-000554` and `VEN-000564`.

## Robins Center — stable-ID spelling/key correction

`VEN-000324` is the University of Richmond **Robins Center**.

Declared global changes:

- venue ID remains `VEN-000324`;
- global key changes `robbins-center` -> `robins-center`;
- project display changes `Robbins Center` -> `Robins Center`;
- the false `Robbins Center` spelling must not remain as a curated global alias.

Published school venue rows currently using `VEN-000324` and requiring key/display/false-alias normalization: **12**:

Arizona State, California, Maryland, Miami, North Carolina, Providence, South Carolina, St. John's, Syracuse, Virginia Tech, Virginia, West Virginia.

The transaction must mechanically rewrite dependent curated venue keys/provenance markers where the stable key is stored, while preserving literal source wording. No venue-ID change.

## Eugenio Guerra Sports Complex — false alias deletion

`VEN-000371` remains `Eugenio Guerra Sports Complex`.

Declared changes:

- delete global alias `Eugene Guerra Sports Complex`;
- remove that false curated alias from the five school-local rows where it currently appears:
  Arizona State, Boston College, Cincinnati, Colorado, Utah;
- preserve literal historical source/evidence wording, including any source that itself printed Eugene.

No venue-ID or key change.

## Orange County Civic Center — duplicate literal name-state cleanup

`VEN-000683` remains unchanged as a physical identity.

Declared change:

- delete the redundant `HISTORICAL_OR_ALIAS` row whose literal and normalized name are identical to the `PROJECT_DISPLAY` row `Orange County Civic Center`.

No school-local or physical-identity change is required.

## Boardwalk Hall / Atlantic City Convention Hall

`VEN-000433` remains one 1929 physical building.

Register these exact `OFFICIAL_NAMING_PERIOD` rows:

1. `Atlantic City Convention Hall` — 1929-05-31 through 2001-10-10.
2. `Boardwalk Hall` — 2001-10-11 through 2018-01-15.
3. `Jim Whelan Boardwalk Hall` — 2018-01-16 onward.

Durable accepted basis:
- https://www.boardwalkhall.com/about-us
- https://www.boardwalkhall.com/atlantic-city-convention-center
- https://www.nj.gov/casinos/law/act/docs_article16/cca-article16.pdf

Declared identity cleanup:

- retain safe historical `Atlantic City Convention Hall`;
- delete unrestricted global alias `Atlantic City Convention Center` from `VEN-000433`;
- on Georgia Tech's school-local `VEN-000433` row, remove curated alias `Atlantic City Convention Center` while retaining `Atlantic City Convention Hall`;
- preserve Georgia Tech and other literal source-game/evidence wording that historically says `Atlantic City Convention Center`;
- do not conflate this hall with the distinct modern Atlantic City Convention Center opened in 1997.

## Patten Gymnasium — resolved physical topology plus row repair

This is not a spelling-only correction and not a duplicate-ID merge.

Accepted institutional history establishes:

- original Patten Gymnasium opened in 1909;
- the March 27, 1939 inaugural NCAA championship was the last varsity-level basketball game played in the original building;
- the original building was demolished in 1940;
- a physically distinct replacement Patten Gymnasium opened in 1940;
- Northwestern men's basketball did **not** use the replacement as its varsity home; it played at Evanston Township High School and, for games explicitly marked `(C)` in the institutional year-by-year source, Chicago Stadium, until McGaw Memorial Hall opened in 1952.

Stable-ID disposition:

### `VEN-000160` — original 1909 building

Keep `VEN-000160` for the original building because the durable venue census and the published Notre Dame / Ohio State / Oregon 1935-39 uses already point this ID at that physical facility.

Declared global corrections:

- key: `patten-gymnasium-1909`;
- display: `Patten Gymnasium`;
- opened: `1909`;
- closed: `1940`;
- date precision: year;
- replace erroneous `Patton Gymnasium` project-display state with `Patten Gymnasium`;
- remove the now-redundant same-ID Patten alias after project-display correction;
- do not retain `Patton Gymnasium` as an unrestricted curated alias merely because a historical source misspelled it.

Correct the four published school-local `VEN-000160` rows (Northwestern, Notre Dame, Ohio State, Oregon) to the new stable key and correct Patten spelling where curated representation is wrong. Preserve literal source wording.

### `VEN-000156` — distinct 1940 replacement building

Repurpose/correct the existing stable ID rather than allocate another Patten ID:

- ID remains `VEN-000156`;
- key becomes `patten-gymnasium-1940`;
- project display becomes `Patten Gymnasium`;
- opened: `1940`;
- geography remains Evanston, IL;
- do not assign Northwestern varsity men's basketball games to this building.

After source-game correction, Northwestern's current school-local `VEN-000156` venue row must be removed because no published Northwestern men's game remains assigned to the replacement building. The global identity remains registered as the physically distinct 1940 facility.

Identical formal display names across `VEN-000160` and `VEN-000156` are intentional; their distinct stable IDs/keys and date/physical context prevent a false merger. Name-only matching must not silently choose between them.

### New Evanston Township High School identity

No matching current global venue exists at the protected-main basis. Current maximum registered numeric venue ID is `VEN-000864`; therefore `VEN-000865` is the current-main candidate if execution occurs without intervening allocation. If main advances first, replan and allocate the then-next valid ID rather than forcing `VEN-000865`.

Proposed identity:

- key: `evanston-township-high-school`;
- display: `Evanston Township High School`;
- city/state: Evanston, IL;
- source basis: accepted Northwestern institutional Patten/basketball history.

When the permanent chronology-at-birth ledger is later introduced, this venue must receive an honest chronology disposition; do not seed a false no-rename conclusion merely because no naming-history research was needed for this repair.

### Northwestern source-game correction rules

These rules modify **curated venue fields only**. They must preserve source game ID, date, opponent, score/result, H/A/N, `source_venue_name`, `raw_text`, and literal source provenance.

On the protected-main basis:

1. Northwestern `SOURCE_PROGRAM_HOME` rows before 1910-01-01 currently assigned to Old Patton: **19** rows, 1905-03-11 through 1909-02-27. Clear the unsupported exact curated venue assignment. Preserve HOME and accepted Evanston locality; do not invent the pre-Patten building.
2. Northwestern `SOURCE_PROGRAM_HOME` rows from 1910-01-01 through 1939-03-27 that do **not** carry source marker `(C)`: **281** rows. Curated physical venue = original Patten, `VEN-000160`.
3. Every Northwestern `SOURCE_PROGRAM_HOME` row whose preserved raw source carries `(C)`: **79** rows across 1931-12-17 through 1974-02-08. Curated physical venue = existing `VEN-000044` Chicago Stadium, Chicago, IL. The institutional media-guide legend defines `(C)` as Chicago Stadium.
4. Northwestern `SOURCE_PROGRAM_HOME` rows after 1939-03-27 and before 1952-12-06 that do **not** carry `(C)`: **89** rows, 1939-12-05 through 1952-03-01. Curated physical venue = Evanston Township High School.
5. These rules must match exactly **468** currently affected Northwestern HOME rows in aggregate. Overlap is forbidden; a count mismatch is a hard STOP.

The 1939-52 home population is exactly 156 rows on this basis: 67 `(C)` Chicago Stadium rows and 89 non-`(C)` Evanston Township High School rows. Three of the latter are currently venue-blank; the remainder are currently misassigned to one of the Patten identities.

### Northwestern school-local venue postconditions

After source-game correction and explicit local venue-row reconciliation:

- `VEN-000160` original Patten: **281** assigned Northwestern games, first 1910-01-23, last 1939-02-25.
- new Evanston Township High School identity: **89** assigned games, first 1939-12-05, last 1952-03-01.
- `VEN-000044` Chicago Stadium: **79** assigned Northwestern HOME games carrying `(C)`, first 1931-12-17, last 1974-02-08.
- `VEN-000229` Welsh-Ryan Arena: current 1,028 assigned HOME rows must fall to **1,017** after its 11 `(C)` rows move to Chicago Stadium.
- Northwestern school-local `VEN-000156` row: absent.
- 19 pre-1910 HOME rows: no exact curated physical venue.

These are curation/site corrections only. H/A/N remains Northwestern HOME for the affected Northwestern rows.

## Tests and adversarial postconditions

The maintenance implementation must add regression coverage proving at minimum:

- Seattle `VEN-000315` is retired and no active school/global dependency remains.
- Smith/Nielsen IDs remain distinct and the false cross-identity alias cannot resolve Smith to Nielsen.
- Rice Field House cannot resolve to the 1950 Autry/Rice Gym building; the 1947 Texas Tech literal wording remains preserved.
- all `VEN-000324` curated representations use Robins, not Robbins, while raw source strings remain unchanged.
- false Eugene Guerra curated aliases are removed without erasing source evidence.
- Orange County Civic Center has no redundant duplicate alias row.
- Boardwalk Hall official periods are exact, non-overlapping, and the modern Convention Center cannot resolve as a global alias of `VEN-000433`.
- `VEN-000160` and `VEN-000156` are distinct Patten physical identities; identical display name alone never merges them.
- no Northwestern men's basketball row after the 1939 NCAA final and before McGaw is assigned to replacement Patten.
- all 79 Northwestern `(C)` HOME rows resolve to Chicago Stadium.
- all 89 non-`(C)` Northwestern HOME rows in the 1939-52 off-campus interval resolve to Evanston Township High School.
- the 19 pre-1910 Northwestern HOME rows retain HOME/locality but no invented exact venue.
- exact site-data freshness and repository validation pass.
- the actual diff contains no undeclared school, game, venue, opponent, score, result, H/A/N, or source-literal changes.

## Execution boundary

This specification completes the Control Center topology/design pass. The next action is a dedicated shared-reference maintenance implementation on a non-main branch. That is a global/shared mutation and requires explicit Control Center owner authorization before the first reference/data write.

The six-venue PR #297 production proof remains separately blocked at this checkpoint by Vercel's deployment-rate limit. Do not create a no-op commit to trigger another deployment.
