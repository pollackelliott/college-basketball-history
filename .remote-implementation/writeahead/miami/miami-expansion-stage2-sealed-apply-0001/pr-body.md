## Summary

- onboards `miami` through the permanent sealed-plan workflow
- preserves 2,018 source rows (0 pre-cutoff)
- matches 1,865 existing games and creates 153
- applies 0 owner-approved identity decisions
- records 6 dated discrepancy decisions
- approved plan `f70993370c276fa6d762d2b4e1d4216a1978014f1838e087ff22172c9cbfaa36`
- discrepancy dispositions: KEEP_CANONICAL=4, USE_SOURCE=2

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
- `data/reconciliation/onboarding-decisions/miami-f70993370c27.json`
- `site/data/manifest.json`
- `site/data/teams/cincinnati.json`
- `site/data/teams/florida.json`
- `site/data/teams/georgia.json`
- `site/data/teams/maryland.json`
- `site/data/teams/miami.json`
- `site/data/teams/ohio-state.json`
- `site/data/teams/pittsburgh.json`
- `site/data/teams/usc.json`
- `site/data/teams/villanova.json`
- `site/data/teams/wake-forest.json`
