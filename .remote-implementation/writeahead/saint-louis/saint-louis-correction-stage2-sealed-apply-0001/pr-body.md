## Summary

- onboards `saint-louis` through the permanent sealed-plan workflow
- preserves 2,892 source rows (0 pre-cutoff)
- matches 2,892 existing games and creates 0
- applies 0 owner-approved identity decisions
- records 0 dated discrepancy decisions
- approved plan `bfe16499cd111951c435f001f9f5199a8044a733695c2c2fe4d5b71a57203016`

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
- `data/reconciliation/onboarding-decisions/saint-louis-bfe16499cd11.json`
- `site/data/teams/saint-louis.json`
