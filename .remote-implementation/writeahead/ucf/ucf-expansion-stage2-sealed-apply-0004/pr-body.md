## Summary

- onboards `ucf` through the permanent sealed-plan workflow
- preserves 1,646 source rows (0 pre-cutoff)
- matches 1,273 existing games and creates 373
- applies 0 owner-approved identity decisions
- records 0 dated discrepancy decisions
- approved plan `7cd9aaa960bc204ec92cdf707e4237fb72730cb1e63315be9af754d2209fdc8e`

## Validation

- repository validation — PASS
- target package no-op — PASS
- All-History expansion site nonregression — PASS; inherited full-gate failures remain reported
- accomplishment cross-check — PASS
- deterministic site build — PASS
- unit tests — PASS
- changed-file whitespace check — PASS

## Sealed apply boundary

The paths below are the transactional sealed-plan mutation boundary. The full PR diff also includes committed Phase 0 package/reference changes already present on the onboarding branch.

- `data/canonical/games.csv`
- `data/evidence/game-assertions.csv`
- `data/reconciliation/onboarding-decisions/ucf-7cd9aaa960bc.json`
- `site/data/manifest.json`
- `site/data/programs.json`
- `site/data/teams/fordham.json`
- `site/data/teams/long-island-university.json`
- `site/data/teams/ucf.json`
- `site/data/teams/wisconsin.json`
