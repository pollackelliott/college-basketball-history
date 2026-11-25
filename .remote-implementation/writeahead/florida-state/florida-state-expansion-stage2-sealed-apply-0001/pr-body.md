## Summary

- onboards `florida-state` through the permanent sealed-plan workflow
- preserves 2,291 source rows (0 pre-cutoff)
- matches 2,111 existing games and creates 179
- applies 1 owner-approved identity decisions
- records 7 dated discrepancy decisions
- approved plan `f7b69d314b01fa533968bc3b4d670a71c3c0a3dae0005635733153427ea1220f`
- discrepancy dispositions: USE_SOURCE=7

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
- `data/evidence/game-assertions-0002.csv`
- `data/reconciliation/discrepancies.csv`
- `data/reconciliation/onboarding-decisions/florida-state-f7b69d314b01.json`
- `site/data/manifest.json`
- `site/data/teams/florida-state.json`
- `site/data/teams/florida.json`
- `site/data/teams/georgia.json`
- `site/data/teams/miami.json`
- `site/data/teams/mississippi-state.json`
- `site/data/teams/ole-miss.json`
- `site/data/teams/usc.json`
