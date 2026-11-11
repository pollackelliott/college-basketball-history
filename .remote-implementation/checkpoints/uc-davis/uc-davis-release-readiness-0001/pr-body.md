## Summary

- onboards `uc-davis` through the permanent sealed-plan workflow
- preserves 668 source rows (0 pre-cutoff)
- matches 86 existing games and creates 582
- applies 0 owner-approved identity decisions
- records 2 dated discrepancy decisions
- approved plan `8c032a33b6cb071b3d57eb3595afa1f8c0f656d9280684c5069e4bae29882cd0`
- discrepancy dispositions: USE_SOURCE=2

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
- `data/reconciliation/onboarding-decisions/uc-davis-8c032a33b6cb.json`
- `data/reference/program-accomplishments.csv`
- `data/reference/programs.csv`
- `site/data/manifest.json`
- `site/data/programs.json`
- `site/data/teams/arizona.json`
- `site/data/teams/arkansas.json`
- `site/data/teams/boise-state.json`
- `site/data/teams/byu.json`
- `site/data/teams/california.json`
- `site/data/teams/colorado-state.json`
- `site/data/teams/colorado.json`
- `site/data/teams/dayton.json`
- `site/data/teams/depaul.json`
- `site/data/teams/fresno-state.json`
- `site/data/teams/gonzaga.json`
- `site/data/teams/hawai-i.json`
- `site/data/teams/houston.json`
- `site/data/teams/indiana.json`
- `site/data/teams/iowa-state.json`
- `site/data/teams/kansas-state.json`
- `site/data/teams/kansas.json`
- `site/data/teams/louisville.json`
- `site/data/teams/loyola-chicago.json`
- `site/data/teams/minnesota.json`
- `site/data/teams/missouri.json`
- `site/data/teams/nebraska.json`
- `site/data/teams/ohio-state.json`
- `site/data/teams/oklahoma-state.json`
- `site/data/teams/oregon-state.json`
- `site/data/teams/oregon.json`
- `site/data/teams/saint-joseph-s.json`
- `site/data/teams/saint-louis.json`
- `site/data/teams/san-diego-state.json`
- `site/data/teams/stanford.json`
- `site/data/teams/texas.json`
- `site/data/teams/uc-davis.json`
- `site/data/teams/ucla.json`
- `site/data/teams/usc.json`
- `site/data/teams/utah-state.json`
- `site/data/teams/utah.json`
- `site/data/teams/washington-state.json`
- `site/data/teams/washington.json`
- `site/data/teams/wisconsin.json`
