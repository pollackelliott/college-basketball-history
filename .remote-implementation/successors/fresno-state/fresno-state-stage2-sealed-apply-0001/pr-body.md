## Summary

- onboards `fresno-state` through the permanent sealed-plan workflow
- preserves 1,708 source rows (0 pre-cutoff)
- matches 380 existing games and creates 1,327
- applies 1 owner-approved identity decisions
- records 15 dated discrepancy decisions
- approved plan `f3dfaa04c818d7d8de1d4c9553b53db2d42bd13deffbcd484ae10e7161fea5dc`
- discrepancy dispositions: KEEP_CANONICAL=11, USE_SOURCE=4

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
- `data/reconciliation/onboarding-decisions/fresno-state-f3dfaa04c818.json`
- `data/reference/program-accomplishments.csv`
- `data/reference/programs.csv`
- `site/data/manifest.json`
- `site/data/programs.json`
- `site/data/teams/arizona-state.json`
- `site/data/teams/arizona.json`
- `site/data/teams/arkansas.json`
- `site/data/teams/boise-state.json`
- `site/data/teams/butler.json`
- `site/data/teams/byu.json`
- `site/data/teams/california.json`
- `site/data/teams/chicago-state.json`
- `site/data/teams/colorado-state.json`
- `site/data/teams/colorado.json`
- `site/data/teams/creighton.json`
- `site/data/teams/depaul.json`
- `site/data/teams/duke.json`
- `site/data/teams/florida.json`
- `site/data/teams/fresno-state.json`
- `site/data/teams/georgetown.json`
- `site/data/teams/georgia.json`
- `site/data/teams/gonzaga.json`
- `site/data/teams/houston.json`
- `site/data/teams/iowa-state.json`
- `site/data/teams/kansas-state.json`
- `site/data/teams/long-island-university.json`
- `site/data/teams/lsu.json`
- `site/data/teams/marquette.json`
- `site/data/teams/miami.json`
- `site/data/teams/michigan-state.json`
- `site/data/teams/minnesota.json`
- `site/data/teams/mississippi-state.json`
- `site/data/teams/nc-state.json`
- `site/data/teams/nebraska.json`
- `site/data/teams/northwestern.json`
- `site/data/teams/ohio-state.json`
- `site/data/teams/oklahoma-state.json`
- `site/data/teams/ole-miss.json`
- `site/data/teams/oregon-state.json`
- `site/data/teams/oregon.json`
- `site/data/teams/pittsburgh.json`
- `site/data/teams/purdue.json`
- `site/data/teams/smu.json`
- `site/data/teams/stanford.json`
- `site/data/teams/tcu.json`
- `site/data/teams/texas-tech.json`
- `site/data/teams/texas.json`
- `site/data/teams/ucla.json`
- `site/data/teams/usc.json`
- `site/data/teams/utah-state.json`
- `site/data/teams/utah.json`
- `site/data/teams/vanderbilt.json`
- `site/data/teams/villanova.json`
- `site/data/teams/wagner.json`
- `site/data/teams/wake-forest.json`
- `site/data/teams/washington-state.json`
- `site/data/teams/washington.json`
- `site/data/teams/west-virginia.json`
- `site/data/teams/wisconsin.json`
