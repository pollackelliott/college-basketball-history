# Codex repository instructions

## School onboarding

Use the permanent sealed-plan workflow for every new school. Do not recreate the
legacy sequence of manual ingestion, one-off reconciliation scripts, hand-written
staging commands, or piecemeal owner questions.

1. Work in the project Codespace on `data/<school_key>-onboarding`, never on `main`.
2. Build and commit the complete six-file package plus owner-confirmed history scope.
3. Run `python tools/onboard_school.py <school_key> --preflight`.
4. Present every row in `.onboarding/<school_key>/review.md` as one batch.
5. Every game-specific review item must show its date. If date is disputed, show
   the source date and canonical date separately; never collapse them into one date.
6. Obtain one explicit owner decision and evidence basis for every pending row.
7. Edit only the decision, basis, and optional patch columns in `review.csv`, then
   seal with `--approve` and apply only with the exact emitted plan hash.
8. The apply must remain transactional and must pass validation, target no-op,
   accomplishment cross-check, deterministic site build, unit tests, and whitespace.
9. Run `python tools/release_school.py <school_key> --prepare`.
10. Stop for the owner to visually approve the exact PR preview.
11. Merge only with `--merge --preview-approved`; require the exact merged SHA to
    reach a successful Production deployment and match production JSON.

Historical uncertainty remains valid. Never infer game identity, inclusion, date,
site, venue, opponent, or a controlling canonical fact merely to make the workflow
pass. Preserve source `raw_text` and approved unresolved discrepancies.

## Git safety

- Never use `git add -A` for onboarding.
- Never force-push shared history.
- Never merge when the sealed input fingerprint, release file boundary, branch SHA,
  PR head SHA, or deployment SHA differs from the reviewed state.
- Keep generated `.onboarding/` plans local; the sealed decision plan is archived
  under `data/reconciliation/onboarding-decisions/` during apply.

## Code review rules

- Flag any discrepancy display that omits `source_game_date` or
  `canonical_game_date`; date conflicts must expose both values.
- Flag any write path that bypasses the approved-plan hash or writes outside the
  transaction allow-list.
- Flag any release path that merges without explicit preview approval or treats a
  Preview deployment as Production.
