# St. Bonaventure Research — Stage 2 opponent identity COMPLETE

checkpoint_status: COMPLETE
stage2_complete: true
stage3a0_authorized: false
target_team: St. Bonaventure
program_key: st-bonaventure
scope: INCEPTION+
research_base_sha: bed68f763a7ea8920c6ba830b004334b16c9e303
protected_main_sha_at_stage2: 428fa4ba980f3454477ed96ce3d71fcaee0ff0fd
parent_research_commit: ce9746af071e7778dcffcd350954fd5d762fe225

## Exact Stage 2 artifact

Artifact:
`st-bonaventure-stage2-opponent-identity-complete-checkpoint-20261101.zip`

SHA-256:
`47d7518a472d46d74e1515243a47555dd387bedf3f645f06ca7cdd7e51d0b2f0`

Internal Stage 2 manifest SHA-256:
`0a25de310f25e7a31d51206ab37457620cd40d203cd2ca078a2ad9ecf50e910a`

Structured Stage 2 ledger SHA-256:
`46cec8170b3b2fbb43257334eda109d45f9ae38947b07a733df381d8dcb75256`

Stage 4 opponents authoring capsule SHA-256:
`e81ea19d804e78a40b26ea3b59be5f963d28b00cbe6cd02d09f579bc4f05b18e`

Stage 2 opponent audit SHA-256:
`8114fbb959e00a9ca884d79107b349ccac4ccc1b75e90150b2758f57b80b7315`

Carried Stage 4 season-coverage SHA-256:
`8c983ad5fa7ba0d38f51748481abf029bfa21551786961fe972736f277b4feae`

Parent verified Stage 1 closeout SHA-256:
`27ebd74e7f8bec63147041fb4672aeb224424b75b36aff16e11ce59f20479a65`

## Completion census

- Stage 1 game rows preserved: **2,614**
- distinct literal source opponent labels: **814**
- distinct Stage 1 normalized opponent labels: **489**
- distinct canonical opponent keys after Stage 2: **343**
- current-D1 canonical keys at immutable Research base: **225**
- historical/non-current-D1 canonical keys: **118**
- current-D1 game rows: **2,148**
- historical/non-current-D1 game rows: **466**
- unresolved opponent identities: **0**
- ambiguous current-program matches: **0**
- known current-program key splits: **0**
- non-D1 keys colliding with immutable current-D1 registry: **0**

## Historical integrity

Every original Stage 1 historical column remains value-for-value unchanged in the same 2,614-row order. No game was added, removed, duplicated, or reinterpreted.

The verified 1919-20 terminal coverage debt remains exactly six unidentified games, collectively 3-3, with no game rows or opponent identities created for them. The Stage 1 `stage4-authoring/season-coverage.json` payload is carried byte-for-byte unchanged.

## Opponent identity method

Stage 2 prioritized exact current-D1 registry identity at immutable `research_base_sha`, source-label normalization, published project/reciprocal precedent, and bounded target-specific checks where a wrong merge could materially split a current program or collapse distinct historical opponents.

Target-specific checks include:

- `Bellarmarine` -> Bellarmine: Bellarmine official 1961-62 results list @ St. Bonaventure L 89-58, exact reciprocal score.
- `Albany State Teachers` -> UAlbany: University at Albany institutional chronology establishes the predecessor identity.
- `St. Thomas (PA)/(Pa.)` -> Scranton: University of Scranton institutional history establishes St. Thomas College as the predecessor renamed in 1938.
- `Pan American` -> UTRGV: UTRGV institutional history establishes the Pan American institutional line.
- `Westminster` -> Westminster (PA): carried from accepted Stage 1 official reciprocal evidence.

Historical labels with no plausible current-D1 collision were preserved as explicit historical/non-current-D1 identities rather than forced into speculative modern genealogy.

## Site/H-A/N boundary

The accepted Stage 1 source inventory does not serialize an explicit target-source H/A/N notation convention. Stage 2 therefore made **no** site inference. All 2,614 source-site tokens and standardized `site_type` values are unchanged; the current Stage 2 site population remains 2,614 `UNKNOWN` for downstream site research.

## Stage boundary

**STAGE 2: COMPLETE**

Research Freeze is not declared.

Do not begin Stage 3A-0 without the owner's next `Proceed`.

Next bounded Research stage:
`STAGE_3A_0 — mechanical checkpoint-only census and partition`.
