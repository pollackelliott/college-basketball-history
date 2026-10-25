## Summary

- onboards `boise-state` through the permanent sealed-plan workflow
- preserves 1,670 source rows (0 pre-cutoff)
- matches 136 existing games and creates 1,534
- applies 0 owner-approved identity decisions
- records 5 dated discrepancy decisions
- approved plan `b76b1e2c5e5e1969fb59890ad68805f93a015a822d01ae7eee6d388d6b483db3`
- discrepancy dispositions: KEEP_CANONICAL=4, USE_SOURCE=1

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
- `data/reconciliation/onboarding-decisions/boise-state-b76b1e2c5e5e.json`
- `data/reference/program-accomplishments.csv`
- `data/reference/programs.csv`
- `site/data/manifest.json`
- `site/data/programs.json`
- `site/data/teams/arizona-state.json`
- `site/data/teams/arizona.json`
- `site/data/teams/arkansas.json`
- `site/data/teams/boise-state.json`
- `site/data/teams/boston-college.json`
- `site/data/teams/butler.json`
- `site/data/teams/byu.json`
- `site/data/teams/chicago-state.json`
- `site/data/teams/cincinnati.json`
- `site/data/teams/clemson.json`
- `site/data/teams/colorado.json`
- `site/data/teams/creighton.json`
- `site/data/teams/georgia-tech.json`
- `site/data/teams/houston.json`
- `site/data/teams/illinois.json`
- `site/data/teams/indiana.json`
- `site/data/teams/iowa-state.json`
- `site/data/teams/iowa.json`
- `site/data/teams/kansas.json`
- `site/data/teams/kentucky.json`
- `site/data/teams/louisville.json`
- `site/data/teams/lsu.json`
- `site/data/teams/marquette.json`
- `site/data/teams/michigan-state.json`
- `site/data/teams/michigan.json`
- `site/data/teams/mississippi-state.json`
- `site/data/teams/nc-state.json`
- `site/data/teams/nebraska.json`
- `site/data/teams/northwestern.json`
- `site/data/teams/oklahoma-state.json`
- `site/data/teams/ole-miss.json`
- `site/data/teams/oregon-state.json`
- `site/data/teams/oregon.json`
- `site/data/teams/rutgers.json`
- `site/data/teams/smu.json`
- `site/data/teams/south-carolina.json`
- `site/data/teams/stanford.json`
- `site/data/teams/tcu.json`
- `site/data/teams/texas-a-m.json`
- `site/data/teams/ucla.json`
- `site/data/teams/usc.json`
- `site/data/teams/utah.json`
- `site/data/teams/vanderbilt.json`
- `site/data/teams/virginia-tech.json`
- `site/data/teams/washington-state.json`
- `site/data/teams/washington.json`
- `site/data/teams/wisconsin.json`
