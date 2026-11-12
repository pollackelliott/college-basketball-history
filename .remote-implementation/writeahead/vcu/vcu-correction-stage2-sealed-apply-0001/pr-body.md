## Summary

- onboards `vcu` through the permanent sealed-plan workflow
- preserves 1,650 source rows (0 pre-cutoff)
- matches 1,650 existing games and creates 0
- applies 0 owner-approved identity decisions
- records 0 dated discrepancy decisions
- approved plan `3a1e5bb5235eb827f83e2287b8114ff18165bd02007254625b0f0aa87bcb2f87`

## Validation

- repository validation — PASS
- target package no-op — PASS
- correction-only site nonregression — PASS; inherited full-gate failures remain reported
- accomplishment cross-check — PASS
- deterministic site build — PASS
- unit tests — PASS
- changed-file whitespace check — PASS

## Sealed apply boundary

The paths below are the transactional sealed-plan mutation boundary. The full PR diff also includes committed Phase 0 package/reference changes already present on the onboarding branch.

- `data/canonical/games.csv`
- `data/evidence/game-assertions.csv`
- `data/reconciliation/onboarding-decisions/vcu-3a1e5bb5235e.json`
- `site/data/teams/vcu.json`
