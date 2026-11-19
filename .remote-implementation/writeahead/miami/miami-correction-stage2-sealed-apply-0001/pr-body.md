## Summary

- applies one bounded post-publication package-only correction for `miami`
- changes only the frozen, hash-bound `conferences.csv` package member
- changes zero source-game, canonical-game, assertion, or discrepancy rows
- carries zero new historical Gate 1 decisions
- approved plan `93c375569a92982b7fb415e1b8f3eba6f84258cd33c63ee7966b5cedb0a7bc11`

## Validation

- repository validation — PASS
- target package no-op — PASS
- package-only correction site nonregression — PASS; inherited full-gate failures remain reported
- accomplishment cross-check — PASS
- deterministic site build — PASS
- unit tests — PASS
- changed-file whitespace check — PASS

## Sealed apply boundary

The paths below are the sealed package-only verification/output boundary. The corrected conferences.csv member was already staged from the exact frozen correction package before Stage 2.

- `data/reconciliation/onboarding-decisions/miami-93c375569a92.json`
- `site/data/teams/miami.json`
