# St. Bonaventure Research — Stage 1 aggregate-coverage closeout

checkpoint_status: COMPLETE
stage1_complete: true
stage2_authorized: false
target_team: St. Bonaventure
program_key: st-bonaventure
scope: INCEPTION+
research_base_sha: bed68f763a7ea8920c6ba830b004334b16c9e303
protected_main_sha_at_closeout: 80b00278ac9add94702ac76c5fa310b95d2b1929
parent_research_commit: b9a9c9ef7500ad853fc8ca397504911651f00798

## Authority

Generic policy/tooling repair:
PR #427 — Audited founding-era aggregate coverage and non-fictional public season notes

Owner disposition:
https://github.com/pollackelliott/college-basketball-history/issues/426

Permanent tool:
`tools/research_stage1_aggregate_coverage.py`

Terminal classification:
`EARLY_HISTORY_AGGREGATE_RECONCILED_GAP`

## Exact checkpoint chain

Parent artifact:
`st-bonaventure-stage1-founding-six-research-exhausted-checkpoint-20261101.zip`

Parent SHA-256:
`23cb047b2ecbbab3f1310472768974891c851ac687dd5b8c6e55e8bc6f289504`

Audit artifact:
`stage1-aggregate-coverage-audit-20261101.json`

Audit SHA-256:
`4a380f4328db11b62db7d78582a062993099be78b9e0e1003f20835e4bbcb13b`

Audit result:
`ELIGIBLE_FOR_EARLY_AGGREGATE_COVERAGE_CLOSEOUT`

Closeout successor artifact:
`st-bonaventure-stage1-aggregate-coverage-closeout-20261101.zip`

Closeout successor SHA-256:
`27ebd74e7f8bec63147041fb4672aeb224424b75b36aff16e11ce59f20479a65`

Independent verification artifact:
`stage1-aggregate-coverage-verify-20261101.json`

Verification artifact SHA-256:
`77d32e1221c3c4b73d09b9905b2d7ad17a80825f2aba44a19720d77b50efbd75`

Independent verification result:
`VERIFIED_EARLY_AGGREGATE_COVERAGE_CLOSEOUT`

Verification defects: 0

## Historical invariants preserved

- Identified competitive-game ledger rows: **2,614**.
- Ledger SHA-256 remains `e3656e59b9c729cc9fd399e5cbf760869651be6db70b6d3c3de4c0e802da7586`.
- Season-census SHA-256 remains `f25b80e28afa9fe4dd69f7c65c3b48d5f5a294d9cfd4e3a56b2dc43c4efb9a76`.
- Accepted corrections and founding-season exhaustion evidence are byte-identical to the parent.
- No anonymous, placeholder, or unidentified-opponent game row was created.
- No aggregate win or loss was assigned to an individual game.

1919–20 official institutional record: **6–10 (16 games)**.

Individually identified games: **10 (3–7)**.

Terminal historical coverage debt: **6 unidentified games, collectively 3 wins and 3 losses**.

The successor carries the season-level coverage metadata in both
`aggregate-coverage-closeout.json` and
`stage4-authoring/season-coverage.json`.

## Stage boundary

Stage 1 is **COMPLETE** under the independently verified owner-authorized aggregate-coverage exception.

The six games remain unidentified historical coverage debt; Stage 1 completion does not represent them as canonical games.

Research Freeze is not declared.

Do not begin Stage 2 from this closeout without the ordinary owner authorization for Stage 2.

Next authorized boundary:
`STAGE_2_AFTER_OWNER_AUTHORIZATION`.
