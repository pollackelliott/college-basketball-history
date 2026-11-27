## Summary

- onboards `uc-davis` through the permanent sealed-plan workflow
- preserves 2,632 source rows (0 pre-cutoff)
- matches 737 existing games and creates 1,891
- applies 4 owner-approved identity decisions
- records 4 dated discrepancy decisions
- approved plan `498257f67cc96306ffcda3f25ff872bc6569ccd83df8abe6a9f1ee3a250f326d`
- discrepancy dispositions: KEEP_CANONICAL=4

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
- `data/reconciliation/onboarding-decisions/uc-davis-498257f67cc9.json`
- `site/data/manifest.json`
- `site/data/programs.json`
- `site/data/teams/byu.json`
- `site/data/teams/california.json`
- `site/data/teams/colorado-state.json`
- `site/data/teams/fresno-state.json`
- `site/data/teams/stanford.json`
- `site/data/teams/uc-davis.json`
