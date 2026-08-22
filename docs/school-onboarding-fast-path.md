# Permanent School Onboarding Fast Path

- **Status:** Required for every new school beginning August 14, 2026
- **Execution environment:** Project GitHub Codespace, preferably with Codex
- **Human gates:** Two

This procedure consolidates package validation, canonical matching,
reconciliation, publication, testing, pull-request release, and production proof.
The detailed historical/data rules in `new-team-onboarding-runbook.md` still apply;
this document controls how those rules are executed.

The operating rationale, anti-churn rules, and Purdue-proven efficiency lessons are
preserved in `onboarding-process-efficiency.md`. Treat that document as a required
companion when deciding how much technical work to batch, what to ask the owner to
review, and when a failure should or should not reopen historical decisions.

Two additional operating companions are now required:

- `codespace-terminal-safety.md` — prevents shell-driving failures such as RVM
  nounset crashes, accidental interactive-shell exits, expected-negative probes
  under `set -e`, and repository-root helper clutter;
- `parallel-portfolio-pipeline.md` — defines the optional high-major “five in the
  holster” model: parallel source/portfolio research with strictly serialized
  current-main integration.

## Why this replaced the serial procedure

The earlier procedure discovered identity questions, discrepancies,
accomplishments, publication changes, and deployment checks one stage at a time.
It also required school-specific reconciliation programs and repeated command
handoffs. The permanent workflow instead creates one complete review packet before
tracked global data changes and seals the owner's batch decision cryptographically.

The collaborator owns routine source extraction, six-file assembly, normalization research,
preflight investigation, technical debugging, validation, provenance maintenance, and
release mechanics. The owner should normally be interrupted only twice: once for the
consolidated historical/reconciliation decision batch and once for the exact preview.
Technical gate failures do not reopen unchanged owner decisions.

## Optional parallel portfolio research — one integration lane

For current high-major onboarding, multiple school portfolios may be researched and
assembled concurrently before repository integration. The recommended operating mode
is up to five independent research chats feeding one serialized Codespace integration
lane.

Parallel research may construct and QA six-file portfolios, gather authoritative
sources, and freeze research artifacts. It must not perform concurrent tracked writes,
canonical preflight approval, apply, or release against stale repository state.

Every parallel research package must record the `main` SHA it used as
`research_base_sha`. Any new numeric global venue IDs assigned during research are
provisional. When that school reaches the front of the integration queue, synchronize
current `main`, reconcile all shared/global identities again, reuse any venue/reference
identity added by intervening teams, allocate fresh numeric IDs where needed, rerun
package QA and hashes, and only then begin tracked Phase 0.

See `parallel-portfolio-pipeline.md` for the required research-freeze versus
integration-freeze distinction and the current-main rebase checklist.

## Phase 0 — package checkpoint

Prefer to finish and QA the complete six-file portfolio before it mutates global
repository data. If the portfolio was prepared outside the Codespace and transferred
as a ZIP, treat the ZIP as a transport artifact rather than repository content.
Before any tracked write, run one read-only checkpoint that verifies:

- current branch and HEAD;
- tracked worktree state;
- local `main` versus `origin/main`;
- the expected prior production checkpoint in `main` ancestry;
- package presence and SHA-256;
- exactly the six expected flat archive entries;
- for a parallel research-frozen package, the recorded `research_base_sha` and the
  completed current-main shared-reference rebase.

Do not automatically stash, reset, delete an existing branch, or overwrite unexpected
tracked work. Stop and identify any state that differs from the expected checkpoint.

Then, in the Codespace:

```bash
git switch main
git pull --ff-only origin main
school_key="<school_key>"
git switch -c "data/${school_key}-onboarding"
```

Install exactly the six package files under `schools/<school_key>/`. Record the
explicit owner-confirmed history scope in `data/reference/programs.csv`. Add only
reference identities that must exist before preflight can interpret the package,
such as genuinely new physical venues and their required display-name rows.

Research and verify expected accomplishment values before Gate 1, but normally let
the onboarding decision machinery apply `program-accomplishments.csv` after owner
approval rather than manually pre-solving that decision in Phase 0.

### Codespace shell safety

Do not use Bash nounset in this project Codespace. In particular, do not use:

```bash
set -u
```

or:

```bash
set -euo pipefail
```

The Codespace's RVM shell integration has previously terminated terminals on nounset
failures unrelated to repository data.

For complex guarded operations, prefer a quoted heredoc that writes a child script
under `/tmp`, then run that child script. A child script may use `set -eo pipefail`
or explicit return-code checks. Do not use `exit` as a STOP mechanism in a block
pasted directly into the owner's live interactive shell.

Expected-negative probes such as branch-existence checks, `grep` with an acceptable
no-match result, or optional-file checks must be wrapped in explicit `if` logic under
`set -e`; do not let an expected status 1 abort a script accidentally.

If a script fails, inspect branch, HEAD, worktree state, and completed stages before
rerunning. Keep helper scripts and diagnostics in `/tmp` or ignored `.onboarding/`
paths rather than the repository root. See `codespace-terminal-safety.md`.

Preserve existing file line endings. For repositories containing CRLF text, use the
CRLF-safe whitespace treatment rather than converting whole files merely to satisfy
a false-positive whitespace gate:

```bash
git \
  -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol \
  diff --cached --check
```

Stage only the explicit intended paths, never `git add -A`. If a transfer ZIP was
used, delete it after verified extraction and do not commit it.

Run package/repository QA, then commit this stable package/reference foundation
checkpoint before global ingestion. Do not add school-specific reconciliation code
unless the generic workflow truly cannot represent the problem.

## Phase 1 — one preflight and one owner decision batch

Run:

```bash
python tools/onboard_school.py "$school_key" --preflight
```

The command writes ignored working artifacts under:

```text
.onboarding/<school_key>/
├── plan.json
├── review.csv
└── review.md
```

It checks the six-file contract, history scope, locations, conferences, canonical
identity, safe enrichments, reciprocal evidence, discrepancies, accomplishments,
publication readiness, and affected existing public pages.

### Date requirement

Every game-specific decision contains both `source_game_date` and
`canonical_game_date`. When they agree, the Markdown report displays one date. When
they differ, it displays both explicitly:

```text
Dates: source YYYY-MM-DD; canonical YYYY-MM-DD
```

An unknown date is printed as `[unknown]`; it is never omitted or inferred.

### Owner gate 1

Review all rows together. The collaborator/agent should compress the machine review
into a human decision packet rather than requiring the owner to parse a large raw
CSV. Group identities, definite discrepancies, conditional discrepancies,
accomplishments, and publication; collapse same-season candidate identities using
available date/score/result/site context; and research only the rows where added
evidence can materially change the disposition.

Before asking the owner to adjudicate a row, correct any demonstrable package
normalization defect that created the row in the first place. Examples include a
malformed opponent token mapped to the wrong institution or a shared venue/display
identity collision. Regenerate preflight after the narrow package fix rather than
asking the owner to rule on an extraction error.

If a large report is clipped or awkward to paste, request only the smallest missing
subset with a targeted extractor. Do not make the owner reproduce already available
output.

In `review.csv`, fill only:

- `decision`
- `resolution_basis`
- optional `canonical_patch_json`
- optional `source_patch_json`
- optional explanatory `notes`

Allowed discrepancy dispositions are:

- `KEEP_CANONICAL` — retain canonical truth and preserve conflicting source evidence;
- `USE_SOURCE` — change canonical truth to the incoming supported value;
- `NORMALIZE_SOURCE_TO_CANONICAL` — correct a curated source normalization while
  preserving its `raw_text` and the original discrepancy value;
- `LEAVE_UNRESOLVED` — retain a defensible canonical value and explicitly approve
  transparent unresolved publication.

Every decision requires an evidence basis. Date disputes always retain both dates
in the plan and discrepancy provenance.

When identity itself is uncertain, the same review table also contains the
field-level discrepancies that would apply under each candidate match. The owner
chooses one identity and fills its conditional conflict rows in the same batch;
the sealer marks every non-selected candidate `NOT_APPLICABLE`. Ingestion therefore
cannot reveal a new unapproved conflict after the owner gate.

Seal the approved table:

```bash
python tools/onboard_school.py "$school_key" \
  --approve \
  --approved-by "Elliott"
```

The command emits one SHA-256 plan hash. Any change to the school package, canonical
data, evidence, discrepancies, program metadata, accomplishments, conferences, or
the decisions invalidates that approval.

If a later purely technical normalization fix requires a fresh preflight, compare the
complete decision-ID universe with the previously approved one. When the decision
universe is identical, carry forward the already-approved decisions by exact
`decision_id` and reseal as required; do not ask the owner to re-decide unchanged
basketball history. If the decision universe materially changes, stop and review the
new/changed rows.

## Phase 2 — one transactional apply

Run the exact command printed by `--approve`:

```bash
python tools/onboard_school.py "$school_key" \
  --apply \
  --approved-plan "<exact-64-character-hash>"
```

The command requires a clean onboarding branch. It then:

1. verifies the sealed hash and every input file fingerprint;
2. copies the repository to a disposable directory;
3. applies approved identity decisions and ingestion there;
4. executes the generic reconciliation engine;
5. synchronizes only the target's corrected curated assertion fields while
   preserving source `raw_text` and independent reciprocal evidence;
6. applies approved accomplishment and publication metadata;
7. archives the sealed plan under `data/reconciliation/onboarding-decisions/`;
8. builds site JSON twice and compares hashes;
9. runs validation, target `--check-package` no-op, accomplishment verification,
   site dry run, all unit tests, and the CRLF-safe whitespace check;
10. refuses writes outside the narrow apply allow-list;
11. copies only the already-validated changed files back to the real branch;
12. re-verifies the copied state.

If rehearsal fails, the real tracked working tree remains unchanged. Diagnose whether
the failure is historical/data-bearing or purely technical before altering package
inputs. A site-build/display-normalization failure does not automatically reopen
unchanged Owner Gate 1 decisions.

Successful apply produces:

```text
.onboarding/<school_key>/
├── approved-plan.json
├── approved-review.md
├── release-manifest.json
├── pr-body.md
└── visual-qa.md
```

### Target assertion closure

Before release, explicitly enumerate any in-scope canonical game involving the
target program that does not have an assertion from the target package. Investigate
each such game. Another already-onboarded source may legitimately preserve a real
game omitted from the target school's own chronological ledger, so the target
source-package count does not have to equal the target's canonical public-game
count. Do not delete a legitimate canonical game or fabricate a target assertion
merely to force those counts to agree.

Separately, the target package itself must finish as a complete ingestion no-op:
every in-scope target source row is represented, with zero new games, assertions,
discrepancies, or enrichments remaining.

### Critical release boundary

Do **not** manually commit after the successful final transactional apply. The
release manifest is bound to the HEAD on which apply ran. Changing HEAD invalidates
the transaction and requires a new preflight, approval, and apply. Go directly from
final apply to `python tools/release_school.py <school_key> --prepare`; `--prepare`
owns the release commit, push, pull-request preparation, checks, and Preview.

## Phase 3 — one release preparation command

Run:

```bash
python tools/release_school.py "$school_key" --prepare
```

This command:

- verifies the complete local gate again;
- confirms that the working-tree changes exactly equal the sealed release manifest;
- stages each approved path explicitly (never `git add -A`);
- commits, pushes, and creates or reuses the pull request;
- watches required GitHub checks;
- confirms clean mergeability;
- waits for the exact PR-head SHA's successful Vercel Preview deployment;
- prints the PR URL, Preview URL, and generated visual-QA checklist.

It then stops.

## Owner gate 2 — exact preview visual QA

Open the printed Preview URL and use
`.onboarding/<school_key>/visual-qa.md`. Check the target page in detail and the
listed affected existing public programs. Preview approval applies only to the exact
PR head SHA recorded in `release-state.json`.

## Phase 4 — merge and production proof

After the preview passes:

```bash
python tools/release_school.py "$school_key" \
  --merge \
  --preview-approved
```

The command refuses a changed branch or PR SHA. It rechecks CI and mergeability,
creates the repository-standard merge commit, fast-forwards local `main`, reproduces
all final gates, waits for the exact merged-main SHA's successful Production
deployment, and compares production JSON byte-for-structure with merged `main` for
the target plus every affected generated JSON document.

No manual `vercel` command is used. A Preview success is never accepted as a
Production success.

## Recovery and stop rules

- A preflight blocker is corrected in the package/reference data, followed by a new
  preflight. Do not edit `plan.json` around it.
- A fingerprint mismatch requires a new preflight and owner approval.
- An apply failure leaves tracked real data unchanged; inspect the reported gate.
- A release boundary mismatch requires removing or separately committing unrelated
  work. Do not broaden the manifest.
- A PR-head change after preview requires another preview approval.
- An exact Production SHA or JSON mismatch is a release failure.
- Historical uncertainty is valid. Unsupported certainty is not.
- Technical failures do not reopen unchanged historical decisions. Fix the technical
  defect at the narrowest layer possible, preserving the sealed historical judgment.
- A research-frozen parallel portfolio must be rebased against current `main` before
  tracked Phase 0; stale numeric venue IDs or shared-reference assumptions are never
  accepted merely because they were valid when research began.
- A terminal/script failure is inspected before rerunning. Do not use `set -u`, do
  not kill the owner's live shell with an interactive `exit`, and do not let
  expected-negative probes abort a guarded child script accidentally.
