# Permanent School Onboarding Fast Path

- **Status:** Required for every new school beginning August 14, 2026
- **Execution environment:** Project GitHub Codespace, preferably with Codex
- **Human gates:** Two

This procedure consolidates package validation, canonical matching,
reconciliation, publication, testing, pull-request release, and production proof.
The detailed historical/data rules in `new-team-onboarding-runbook.md` still apply;
this document controls how those rules are executed.

## Why this replaced the serial procedure

The earlier procedure discovered identity questions, discrepancies,
accomplishments, publication changes, and deployment checks one stage at a time.
It also required school-specific reconciliation programs and repeated command
handoffs. The permanent workflow instead creates one complete review packet before
tracked global data changes and seals the owner's batch decision cryptographically.

## Phase 0 — package checkpoint

In the Codespace:

```bash
git switch main
git pull --ff-only origin main
school_key="<school_key>"
git switch -c "data/${school_key}-onboarding"
```

Build the complete six-file package and record the explicit owner-confirmed history
scope in `data/reference/programs.csv`. Verify the accomplishment reference against
authoritative sources. Commit this stable checkpoint before global ingestion.

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

Review all rows together. In `review.csv`, fill only:

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

If rehearsal fails, the real tracked working tree remains unchanged.

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
