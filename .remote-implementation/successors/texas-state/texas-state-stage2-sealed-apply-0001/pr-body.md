## Summary

- onboards `texas-state` through the permanent sealed-plan workflow
- preserves 1,249 source rows (0 pre-cutoff)
- matches 94 existing games and creates 1,155
- applies 0 owner-approved identity decisions
- records 8 dated discrepancy decisions
- approved plan `6dd6e6889616af2caf967ef62ff3808de8e367282729ba717ef1004766a4ab9d`
- discrepancy dispositions: KEEP_CANONICAL=2, USE_SOURCE=6

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
- `data/reconciliation/onboarding-decisions/texas-state-6dd6e6889616.json`
- `data/reference/program-accomplishments.csv`
- `data/reference/programs.csv`
- `site/data/manifest.json`
- `site/data/programs.json`
- `site/data/teams/arizona-state.json`
- `site/data/teams/arkansas.json`
- `site/data/teams/baylor.json`
- `site/data/teams/boise-state.json`
- `site/data/teams/california.json`
- `site/data/teams/colorado-state.json`
- `site/data/teams/colorado.json`
- `site/data/teams/depaul.json`
- `site/data/teams/gonzaga.json`
- `site/data/teams/houston.json`
- `site/data/teams/iowa.json`
- `site/data/teams/kansas-state.json`
- `site/data/teams/kentucky.json`
- `site/data/teams/long-island-university.json`
- `site/data/teams/lsu.json`
- `site/data/teams/miami.json`
- `site/data/teams/minnesota.json`
- `site/data/teams/mississippi-state.json`
- `site/data/teams/missouri.json`
- `site/data/teams/nebraska.json`
- `site/data/teams/northwestern.json`
- `site/data/teams/oklahoma.json`
- `site/data/teams/ole-miss.json`
- `site/data/teams/penn-state.json`
- `site/data/teams/purdue.json`
- `site/data/teams/san-diego-state.json`
- `site/data/teams/smu.json`
- `site/data/teams/tcu.json`
- `site/data/teams/texas-a-m.json`
- `site/data/teams/texas-state.json`
- `site/data/teams/texas-tech.json`
- `site/data/teams/texas.json`
- `site/data/teams/uconn.json`
- `site/data/teams/utah-state.json`
- `site/data/teams/utah.json`
- `site/data/teams/vanderbilt.json`
- `site/data/teams/washington-state.json`
