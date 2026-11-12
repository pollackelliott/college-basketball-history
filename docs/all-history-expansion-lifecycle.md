# All-History Expansion Lifecycle

- **Status:** Controlling authority contract for supplemental institutional-history Research on already-published legacy programs
- **Workflow kind:** `ALL_HISTORY_EXPANSION`
- **Research terminal state reserved by this contract:** `EXPANSION_RESEARCH_FROZEN`
- **Purpose:** Expand an accepted published legacy history to complete institutional publication without reopening or re-proving the accepted baseline
- **Does not replace:** ordinary new-school onboarding, the post-publication correction lifecycle, top-level scope authority, or downstream serialized Implementation/release safeguards

## 1. Applicability

`ALL_HISTORY_EXPANSION` applies only when the target program is already
published and the authenticated baseline program row has:

- `public_page_enabled = Yes`; and
- `history_coverage_status = LEGACY_TOP_LEVEL_ONLY`.

It is not new-school onboarding. It is not ordinary post-publication
correction. It is not permission to reopen accepted published history. Unknown,
malformed, unpublished, `UNMIGRATED`, or already
`COMPLETE_INSTITUTIONAL` targets fail closed for this lifecycle.

## 2. Immutable baseline principle

The target's accepted published package and publication-authorized canonical
history at the exact `research_base_sha` are inherited historical authority.
Expansion Research does not need to re-prove those rows merely because the
repository later adopted stronger Research standards.

Inherited rows may be consulted for context, reciprocal identity, venue
chronology, opponent identity, duplicate prevention, and later canonical
matching. Consultation does not make an inherited row part of the supplemental
Research population.

A genuine contradiction discovered against an accepted baseline row must be
preserved separately as a correction question. It must not be silently
rewritten through expansion authority. The expansion delta remains additive.

## 3. Expansion target universe

Research first establishes the actual institutional varsity program inception
season and distinguishes active varsity seasons from dormant/no-team seasons.

For each valid active season from researched institutional inception forward,
classify publication authority against the immutable baseline program row:

```text
season_is_published_history(season, baseline_program) == true
    -> BASELINE_PUBLISHED

season_is_published_history(season, baseline_program) == false
    -> EXPANSION_REQUIRED
```

A valid season earlier than researched institutional inception is
`PRE_INCEPTION`.

This means the expansion Research universe includes omitted institutional
seasons both before the first accepted top-level interval and inside
non-top-level gaps between accepted top-level intervals. It is **not**
equivalent to `season < history_start_season`.

The season disposition is publication-authority classification only. It does
not infer that a varsity team existed or played games in a season. Dormant or
no-team seasons are recorded in season accounting when supported; they are not
fabricated into game history.

## 4. Game rules

Expansion Research owns only recognized competitive varsity games in the
`EXPANSION_REQUIRED` active-season population.

- Exhibitions are excluded.
- One real game equals one canonical game.
- Stable supplemental source/research IDs are required.
- Literal evidence and explicit inclusion/exclusion accounting are preserved.
- A target expansion row may correspond to a canonical game that already
  exists because an opponent supplied evidence. Later serialized
  Implementation must reconcile to that existing canonical game rather than
  create a duplicate.

Inherited baseline games are not supplemental Research rows absent separately
authorized correction authority.

## 5. Top-level authority remains unchanged

All-History expansion changes publication coverage, not accepted
top-level/D-I-equivalent classification.

Expansion does not change any of the following except through a separately
authorized correction:

- `history_start_season`;
- `history_scope_intervals`;
- `history_scope_status`;
- `history_scope_basis`;
- `history_scope_notes`; or
- the target row in `data/reference/program-top-level-scope.csv`.

Top-level/D-I accomplishment authority remains unchanged. Lower-level
institutional history may become publicly visible without becoming
top-level accomplishment history.

## 6. Future successful metadata transition

Research itself does not mutate publication metadata.

Only a successful serialized expansion Implementation may project:

```text
program_inception_season = <researched institutional inception>
history_coverage_status = COMPLETE_INSTITUTIONAL
```

from the authenticated published legacy baseline. Every accepted top-level
metadata field remains unchanged, and `public_page_enabled` remains `Yes`.

The permanent pure projection helper may prove this expected invariant before
Implementation exists, but it is not mutation authority.

## 7. Research Stage adaptation

The ordinary Stage 1 mechanical quality rules remain reusable for the
supplemental population:

- establish and serialize the candidate competitive-game universe;
- reconcile season accounting and explicit exclusions;
- account for duplicate representations;
- assign stable source/research IDs;
- preserve literal evidence;
- distinguish blocking from nonblocking residuals; and
- write durable checkpoints before extended discrepancy work.

For `ALL_HISTORY_EXPANSION`, those rules apply to the supplemental
`EXPANSION_REQUIRED` universe rather than forcing inherited
`BASELINE_PUBLISHED` rows through fresh Research.

Later Research-stage substantive standards remain applicable to newly
researched supplemental rows, including opponent identity, H/A/N, HOME
chronology, regular-season neutral research, postseason taxonomy, site/source
provenance, explicit researched uncertainty, and the adversarial pre-freeze
self-challenge.

A contradiction against inherited baseline authority is carried separately as
a correction question instead of being folded into the expansion delta.

## 8. Lower-level postseason

Supplemental generic lower-level `POSTSEASON` rows use the permanent Unit 2
lower-level postseason site policy, including its historical/modern era split
and explicit research-accounting requirement.

This does not weaken NCAA Tournament, NIT, top-level, HOME, regular-season
neutral, or shared published top-level obligations. When another published
participant retains a top-level obligation for the same shared canonical game,
the stricter shared obligation remains controlling.

## 9. Conference history

Do not research exact lower-level conference membership merely to manufacture
a public timeline.

Accepted real top-level conference history remains inherited authority.
Published seasons outside accepted top-level intervals use the permanent
synthetic `Non-D1` publication-conference classification. Preserve useful
literal conference evidence encountered during Research, but do not turn
lower-level conference archaeology into an expansion prerequisite unless it is
material to another genuine historical question.

## 10. NON_D1 owner sanity scan

The expansion owner sanity scan covers:

- every distinct `NON_D1` opponent introduced by the supplemental expansion
  population; and
- any inherited baseline opponent identity explicitly touched or re-relied upon
  because later deterministic materialization requires a representation
  change.

It does not reopen the complete accepted baseline `NON_D1` population.

The collaborator remains responsible for ordinary opponent-identity Research.
Any owner-flagged supplemental/touched identity must be resolved, corrected, or
explicitly explained under current policy before
`EXPANSION_RESEARCH_FROZEN`.

## 11. Future freeze semantics

This contract reserves the durable state name:

`EXPANSION_RESEARCH_FROZEN`

A future expansion freeze must certify at least:

- exact `research_base_sha`;
- exact immutable published-baseline identity;
- researched institutional inception;
- exact supplemental expansion season/accounting universe;
- exact supplemental source-row population;
- explicit exclusions and dormant/no-team accounting;
- supporting supplemental opponent and venue evidence;
- residual accounting;
- required expansion-scoped `NON_D1` owner-scan disposition; and
- exact artifact/member hashes.

It certifies the accepted supplement against an inherited baseline. It does
**not** claim that the inherited six-file package or accepted published rows
were researched anew.

### 11A. EXPANSION_RESEARCH_FROZEN artifact contract

The permanent writer/validator is
`tools/all_history_expansion_freeze.py`. It is read-only with respect to
tracked repository state. It consumes one flat supplemental Research directory
and emits one deterministic ZIP containing exactly:

- `expansion-source-games.csv`;
- `expansion-opponents.csv`;
- `expansion-venues.csv`;
- `expansion-season-accounting.csv`;
- `expansion-exclusions.csv`;
- `expansion-residuals.csv`;
- `expansion-non-d1-scan.csv`;
- `expansion-baseline-correction-questions.csv`;
- `expansion-notes.md`;
- `expansion-source-notes.md`; and
- `expansion-freeze.json`.

The ZIP is a supplemental Research authority artifact, not a replacement
school package. It must never contain inherited `source-games.csv`,
`opponents.csv`, `venues.csv`, `conferences.csv`, `notes.md`, or
`source-notes.md` under their ordinary package names.

The manifest binds the exact `research_base_sha` to canonical row
fingerprints for the target `programs.csv` row, target
`program-top-level-scope.csv` row, and target accomplishment row when
present; raw SHA-256 values for all six inherited package members; the
baseline source-game ID population; and the target's publication-authorized
canonical-game ID population. The baseline terminal season is the latest
valid season represented by the inherited source-game rows.

The expected supplemental season-accounting universe is mechanically
enumerated from researched inception through that baseline terminal season
and includes exactly the seasons classified `EXPANSION_REQUIRED` by
`expansion_season_disposition(...)`. Research, not publication
classification, determines whether each such season is `ACTIVE` or
`DORMANT_OR_NO_TEAM`.

Supplemental support rows use explicit actions:
`NEW_SUPPLEMENTAL`, `REUSE_INHERITED`, or `EXTEND_INHERITED`.
A reuse/extension must carry the canonical hash of the exact inherited support
row. An extension must list its changed fields, and only narrowly additive
opponent accounting or venue relationship/chronology fields are eligible.
The freeze does not apply those changes.

Frozen residuals may contain `NONBLOCKING_RESEARCHED` rows only when
Research already accepted them under substantive policy. Any `BLOCKING`
residual prevents freeze. Likewise, a baseline correction question with
`BLOCKS_EXPANSION` prevents freeze; a
`NO_EXPANSION_IMPACT` question remains explicitly routed outside expansion
mutation authority.

The expansion NON_D1 scan is exact and scoped: it contains distinct NON_D1
identities introduced by supplemental support rows and inherited NON_D1
identities whose representation is explicitly extended. It does not rescan
unchanged inherited identities. `UNRESOLVED` owner dispositions prevent
freeze.

The manifest stores SHA-256 values for every non-manifest frozen member and a
canonical self-fingerprint computed with the self-fingerprint field blank.
(The literal manifest file cannot contain its own raw SHA-256 without
self-reference.) Freeze and fresh verify additionally report the raw manifest
member SHA-256 and whole-ZIP SHA-256.

Fresh verification re-reads every baseline fact from the exact Git object
named by `research_base_sha`, recomputes every supplemental population and
hash, and requires exact manifest equality. It never runs the inherited
baseline package through Research acceptance rules adopted after that package
was accepted.


## 12. Implementation boundary

Research completion alone does not expand publication.

Future serialized Implementation must authenticate the immutable baseline and
accepted supplemental delta, rebase against current protected main,
deterministically materialize a complete six-file candidate, reconcile
canonical/shared identities, create an `INTEGRATION_FROZEN` authority,
preserve the one-active-Implementation mutation lock, and pass the ordinary
Gate 1, pre-seal, sealed apply, verification, Preview, explicit Owner Gate 2,
merge, and exact Production-proof safeguards.

Only the successful serialized mutation path may establish
`program_inception_season`, change
`history_coverage_status: LEGACY_TOP_LEVEL_ONLY -> COMPLETE_INSTITUTIONAL`,
and cause public history to expand.
