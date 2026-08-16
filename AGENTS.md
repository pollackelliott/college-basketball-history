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
6. Obtain one explicit owner decision and evidence basis for every pending row. Before presenting the batch, research each row and provide a recommended disposition; the owner may approve routine recommendations in bulk.
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


## Collaboration boundary

* Routine extraction, normalization research, package construction, reconciliation analysis, testing, provenance maintenance, Git plumbing, validator failures, and deployment mechanics belong to the collaborator and should not create extra owner handoffs.
* Return to the owner only when a new judgment is required about history scope, game identity or inclusion, opponent identity, home/away/neutral classification, venue/location truth, a controlling canonical historical fact, accomplishments, unresolved-conflict publication, or final preview approval.
* A technical failure after owner approval must be diagnosed and repaired generically where possible; do not ask the owner to re-review unchanged historical decisions merely because the tooling implementation changed.

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
