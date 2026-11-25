## Summary

- onboards `hawai-i` through the permanent sealed-plan workflow
- preserves 2,461 source rows (0 pre-cutoff)
- matches 1,766 existing games and creates 679
- applies 16 owner-approved identity decisions
- records 29 dated discrepancy decisions
- approved plan `c94266df230a682d6a955b9705d342f75a65cc9536bd994da2f1be8fb76635dc`
- discrepancy dispositions: KEEP_CANONICAL=25, LEAVE_UNRESOLVED=1, USE_SOURCE=3

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
- `data/reconciliation/onboarding-decisions/hawai-i-c94266df230a.json`
- `site/data/manifest.json`
- `site/data/programs.json`
- `site/data/teams/arizona-state.json`
- `site/data/teams/california.json`
- `site/data/teams/hawai-i.json`
- `site/data/teams/mississippi-state.json`
- `site/data/teams/oregon-state.json`
- `site/data/teams/oregon.json`
- `site/data/teams/stanford.json`
- `site/data/teams/tennessee.json`
- `site/data/teams/unlv.json`
- `site/data/teams/usc.json`
- `site/data/teams/utah-state.json`
- `site/data/teams/utah.json`
- `site/data/teams/washington-state.json`
- `site/data/teams/washington.json`
