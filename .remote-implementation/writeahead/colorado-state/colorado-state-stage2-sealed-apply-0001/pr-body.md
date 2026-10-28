## Summary

- onboards `colorado-state` through the permanent sealed-plan workflow
- preserves 2,765 source rows (0 pre-cutoff)
- matches 828 existing games and creates 1,929
- applies 8 owner-approved identity decisions
- records 66 dated discrepancy decisions
- approved plan `a54db55d5c07b49cb3c38c17e1f6fcd9afcb25452ab3462ffb5f4986bdb30244`
- discrepancy dispositions: LEAVE_UNRESOLVED=49, NORMALIZE_SOURCE_TO_CANONICAL=2, USE_SOURCE=15

## Validation

- repository validation — PASS
- target package no-op — PASS
- implementation site completeness — PASS
- accomplishment cross-check — PASS
- deterministic site build — PASS
- unit tests — PASS
- changed-file whitespace check — PASS

## Sealed apply boundary

The paths below are the transactional sealed-plan mutation boundary. The full PR diff also includes committed Phase 0 package/reference changes already present on the onboarding branch.

- `data/canonical/games.csv`
- `data/evidence/game-assertions.csv`
- `data/reconciliation/discrepancies.csv`
- `data/reconciliation/onboarding-decisions/colorado-state-a54db55d5c07.json`
- `data/reference/program-accomplishments.csv`
- `data/reference/programs.csv`
- `schools/colorado-state/source-games.csv`
- `site/data/manifest.json`
- `site/data/programs.json`
- `site/data/teams/alabama.json`
- `site/data/teams/arizona-state.json`
- `site/data/teams/arizona.json`
- `site/data/teams/arkansas.json`
- `site/data/teams/auburn.json`
- `site/data/teams/baylor.json`
- `site/data/teams/boise-state.json`
- `site/data/teams/boston-college.json`
- `site/data/teams/byu.json`
- `site/data/teams/california.json`
- `site/data/teams/central-connecticut.json`
- `site/data/teams/chicago-state.json`
- `site/data/teams/cincinnati.json`
- `site/data/teams/colorado-state.json`
- `site/data/teams/colorado.json`
- `site/data/teams/creighton.json`
- `site/data/teams/duke.json`
- `site/data/teams/florida-state.json`
- `site/data/teams/florida.json`
- `site/data/teams/georgia-tech.json`
- `site/data/teams/gonzaga.json`
- `site/data/teams/houston.json`
- `site/data/teams/indiana.json`
- `site/data/teams/iowa-state.json`
- `site/data/teams/iowa.json`
- `site/data/teams/kansas-state.json`
- `site/data/teams/kansas.json`
- `site/data/teams/louisville.json`
- `site/data/teams/maryland.json`
- `site/data/teams/michigan-state.json`
- `site/data/teams/michigan.json`
- `site/data/teams/minnesota.json`
- `site/data/teams/mississippi-state.json`
- `site/data/teams/missouri.json`
- `site/data/teams/nc-state.json`
- `site/data/teams/nebraska.json`
- `site/data/teams/north-carolina.json`
- `site/data/teams/northwestern.json`
- `site/data/teams/ohio-state.json`
- `site/data/teams/oklahoma-state.json`
- `site/data/teams/oklahoma.json`
- `site/data/teams/ole-miss.json`
- `site/data/teams/oregon-state.json`
- `site/data/teams/oregon.json`
- `site/data/teams/penn-state.json`
- `site/data/teams/purdue.json`
- `site/data/teams/rutgers.json`
- `site/data/teams/smu.json`
- `site/data/teams/south-carolina.json`
- `site/data/teams/stanford.json`
- `site/data/teams/syracuse.json`
- `site/data/teams/tcu.json`
- `site/data/teams/texas-a-m.json`
- `site/data/teams/texas-tech.json`
- `site/data/teams/texas.json`
- `site/data/teams/ucla.json`
- `site/data/teams/usc.json`
- `site/data/teams/utah-state.json`
- `site/data/teams/utah.json`
- `site/data/teams/villanova.json`
- `site/data/teams/virginia-tech.json`
- `site/data/teams/virginia.json`
- `site/data/teams/washington-state.json`
- `site/data/teams/washington.json`
- `site/data/teams/xavier.json`
