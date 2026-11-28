# Air Force Stage 2 COMPLETE — narrow game-type input-schema repair 0024

Status: STAGE2_COMPLETE / PRIOR_STAGE_STRUCTURED_INPUT_REPAIR. This checkpoint corrects only the four game_type fields identified in terminal failed Stage 3A-0 tool status. Stage 3A-0 is not claimed COMPLETE here.

## Precise failed prior run
- GitHub Actions: https://github.com/pollackelliott/college-basketball-history/actions/runs/46101192021
- Permanent exact-main tool returned STAGE_3A0_INPUT_NOT_READY; remediation_code STRUCTURED_INPUT_DEFECTS, blocker unrecognized_game_type with precisely four IDs, AF-2006-07-032 through 035.
- All four accepted original Stage 1/Stage 2 values were `NIT_TOURNAMENT`. Their original score lines and evidence_basis already explicitly identify the historical NIT event; there is no historical research or changed game identity.
- Permanent Stage 3A-0 tool recognizes `POSTSEASON` and `NIT` but not `NIT_TOURNAMENT`. The accepted publication taxonomy uses `POSTSEASON`. Exactly those four Stage 2 serialized game_type cells were normalized `NIT_TOURNAMENT` -> `POSTSEASON`, retaining NIT designation in unchanged evidence_basis and unchanged source raw labels. No accepted original Stage 1 file was rewritten.
- Exact input ledger before correction Git blob: `acdf50852f41ccade14e36d0b73bfcb1a1c6c5bc`; after correction: `e412be06ab8af3ba3054baa09a3b312f62b86145`; the only semantic differences are 4/1,928 rows and the single `game_type` column, documented in `game-type-taxonomy-correction.csv`.

## Inheritance
- Protected main: `a11cccf944492e4d968edbeef4111ebad150fcec`.
- Immutable research_base_sha: `3f5a15458aa468347e56e669327d6fe4c9c6ee69`.
- Research Stage 1 COMPLETE remains original checkpoint 0020, ledger Git blob `4bf28b42481600ed4d07b04220981bdeb86536a8`, unchanged.
- Research Stage 2 accepted complete checkpoint 0022 at commit `c147a14373cfa988c86275b90299b72cd97e8893`, complete ledger original blob `acdf50852f41ccade14e36d0b73bfcb1a1c6c5bc`, unchanged and fully recoverable.
- The current Research branch contains the one-use Stage 3A-0 workflow commit `70df13134c69751e94e9ccfd691d68a43cd68df1`. This checkpoint supersedes only the structured Stage 2 game-type representation for four NIT rows.
- The Stage 2 opponent identity mapping, literal labels, 745 mapped labels, 323 resolved roots, 271 accepted keys, all 1,928 game identities, 47 working NON_D1 keys, 251 NON_D1 games, and full authoring capsule are carried byte-for-byte from Stage 2 0022.

## Mechanical verification targets
- Total rows: 1,928; unique game IDs: 1,928.
- game_type distribution after repair: REGULAR_SEASON 1,866; NCAA_TOURNAMENT 4; CONFERENCE_TOURNAMENT 50; POSTSEASON 8. Total postseason: 62; regular season: 1,866.
- 0 unresolved opponent keys; 0 H/A/N changes; accepted raw, evidence and site fields unchanged.
- No protected-main or shared global registry mutation; no Stage 3A-1 entered.

## Next operation
Run the unchanged `tools/research_stage3a0.py` and exact dependency from `a11cccf944492e4d968edbeef4111ebad150fcec` against this corrected complete Stage 2 checkpoint. Its mechanical census output must be confirmed by `stage3a0-status.json` before claiming Stage 3A-0 COMPLETE.
