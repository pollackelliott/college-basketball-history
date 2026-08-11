# College Basketball History — New-Team Onboarding Playbook

**Audience:** Project owner and collaborator
**Status:** Partner-ready v2 companion to `docs/new-team-onboarding-runbook.md`
**Current coverage standard:** through 2025-26

This playbook is the short operational version of the detailed runbook. If the two ever disagree, follow `docs/new-team-onboarding-runbook.md`.

## Core principle

**One real basketball game gets one canonical row. Everything else is evidence about that game.**

If two schools list the same contest, keep one canonical game and separate source assertions. Material source disagreements become discrepancies rather than duplicate games or silent overwrites.

Every school package contains exactly:

```text
schools/<school_key>/
├── source-games.csv
├── opponents.csv
├── venues.csv
├── conferences.csv
├── notes.md
└── source-notes.md
```

**The six-file package is the main deliverable.** QA should prove it is trustworthy enough to ingest, not become a second full research project.

## Roles

### Package preparer / collaborator

May collect sources, extract and normalize games, build the six files, run compact QA, run ingestion dry runs, and surface conflicts.

### Project owner

Reviews ambiguous identities, questionable game inclusion, genuine source conflicts, identity overrides, administrative outcomes, and material changes to already-published canonical facts.

For modern or 21st-century conflicts, involve the owner early when that will resolve the issue faster than extended research.

## 1. Start clean and create the onboarding branch

```bash
cd /workspaces/college-basketball-history

git switch main
git pull --ff-only origin main

school_key="<school_key>"
branch_name="data/${school_key}-onboarding"

git switch -c "$branch_name"
git status -sb
```

Create and switch to the onboarding branch **before** adding the school package.

If using GitHub's browser uploader:

1. push the onboarding branch first;
2. select that branch in the GitHub file browser;
3. confirm the branch selector before uploading;
4. do not intentionally upload the package directly to `main`.

Never use `git add -A` for onboarding. Never force-push shared history.

## 2. Gather authoritative sources

Prefer school-controlled sources:

- current media guide or record book;
- all-time game-ly-game results;
- year-by-year results;
- postseason history;
- venue/history pages;
- conference-history material;
- official completed-season results when the main guide stops before 2025-26.

Stop and ask before normalizing any issue that could change:

- whether a game belongs in the dataset;
- which real game a row represents;
- opponent identity;
- home/away/neutral classification;
- which conflicting source should control a canonical fact.

Unknown is a valid value. Do not invent precision.

## 3. Build the six-file package

Key rules:

- include every recognized non-exhibition varsity game;
- exclude exhibitions;
- curate through 2025-26;
- use established global program keys for current Division I opponents;
- preserve raw source text even when normalized values are corrected;
- never infer site solely from venue;
- use venue chronology to fill location only after site is independently established;
- document source typos, undated games, uncertainty, and material curation decisions.

Public game types are limited to `regular season`, `conference tournament`, `NCAA tournament`, and `NIT` under the detailed runbook's canonical values.

## 4. Compact package QA

Do not manually re-prove every game.

Confirm that:

- `source-games.csv` contains the intended competitive game universe;
- the aggregate on-court W-L-T record reconciles to authoritative school history;
- opponent keys resolve through `opponents.csv`;
- curated venues resolve through `venues.csv`;
- site values are valid;
- conference eras are coherent;
- exhibitions and other exclusions are correct;
- undated or uncertain rows are documented rather than guessed.

Sample representative games from:

- the earliest era;
- a middle era;
- the recent era;
- postseason;
- neutral sites;
- overtime;
- repeated same-season opponents;
- other unusual situations.

The goal is a trustworthy package, not a second manual reconstruction of the school's entire history.

## 5. Commit the source package

Before global ingestion, commit the curated six-file package on the onboarding branch.

Stage only the six intended files:

```bash
git add "schools/${school_key}/source-games.csv"
git add "schools/${school_key}/opponents.csv"
git add "schools/${school_key}/venues.csv"
git add "schools/${school_key}/conferences.csv"
git add "schools/${school_key}/notes.md"
git add "schools/${school_key}/source-notes.md"

git --no-pager diff --cached --name-only
git --no-pager diff --cached --stat
git status --short
```

Never use `git add -A`.

Commit the package:

```bash
git commit -m "Add ${school_key} source package"
```

The package commit creates a stable checkpoint before any global canonical, evidence, or reconciliation files change.

## 6. Dry-run ingestion

Run:

```bash
python tools/ingest_school.py "$school_key"
```

Review:

- `Source rows`
- `Existing-game matches`
- `New canonical games`
- `Identity review required`
- `Canonical enrichments`
- `Assertions to add`
- `Discrepancies to add`

Required identity equation:

```text
Existing-game matches + New canonical games + Identity review required = Source rows
```

Stop if `Identity review required` is nonzero.

For matched games:

```text
canonical blank + supported source value -> enrich
same + same                         -> nothing
populated conflict                 -> discrepancy
unsupported / unknown             -> nothing
```

Venue/location enrichment requires source and canonical site classifications to independently agree.

**Venue never establishes home/away/neutral classification.**

Unexpected counts are a stop signal.

## 7. Decide whether isolated rehearsal is needed

Routine onboarding with unchanged, production-proven ingestion logic does not require an isolated rehearsal.

Use an isolated rehearsal when:

- ingestion, schema, or validator logic changed;
- dry-run counts are surprising;
- unusual identity overrides are involved;
- broad reconciliation/tooling changes are included;
- a new collaborator workflow warrants disposable proof;
- the project owner requests it.

When rehearsal is used, the isolated second ingestion must be a complete `NO-OP`, including zero remaining canonical enrichments.

## 8. Apply ingestion

After the dry run is understood and any required rehearsal has passed:

```bash
python tools/ingest_school.py "$school_key" --apply
```

The apply may:

- append genuinely new canonical games;
- safely enrich supported blank canonical metadata on matched games;
- append source assertions;
- append discrepancies.

Validation must pass after the write.

Review the scale of change rather than manually inspecting thousands of routine appended rows:

```bash
git --no-pager diff --stat
git --no-pager diff --numstat -- data/canonical/games.csv
git --no-pager diff -- data/reconciliation/discrepancies.csv
```

Stop if a small metadata change rewrites an entire CSV or creates unexplained formatting churn.

## 9. Review discrepancies and prove the final no-op

Present every newly generated discrepancy in human-readable form with:

- discrepancy ID;
- matchup/date;
- disputed field;
- incoming source value;
- current canonical value;
- relevant competing evidence;
- recommended disposition.

The owner reviews material canonical-value decisions.

A genuine historical conflict may remain `UNDER_REVIEW` when:

- game identity is secure;
- the current canonical representation is defensible;
- the disagreement remains transparently recorded;
- publication with the unresolved flag is explicitly approved.

After reconciliation:

```bash
python tools/validate_data.py
python tools/ingest_school.py "$school_key"
```

Required final result:

```text
all source rows = existing-game matches
New canonical games: 0
Identity review required: 0
Canonical enrichments: 0 games / 0 fields
Assertions to add: 0
Discrepancies to add: 0
NO-OP
```

If the target is not a complete no-op, onboarding is not ready for publication.

## 10. Prepare publication metadata

Before enabling the public page, confirm the target's current conference row and populate all four achievement fields:

- conference regular-season championships;
- conference tournament championships;
- NCAA Final Four appearances;
- NCAA national championships.

`0` means verified zero. Blank means missing and blocks publication.

Then change only the target's `public_page_enabled` value from `No` to `Yes`.

When editing an existing CSV, preserve its existing UTF-8 BOM state and newline style. Stop if a one-row edit rewrites the entire file.

## 11. Build and QA site data

Dry run:

```bash
python tools/build_site_data.py
```

Review:

- public-page count;
- canonical-game count;
- target record and opponent count;
- team JSON file count;
- stale team files.

Apply:

```bash
python tools/build_site_data.py --apply
python tools/validate_data.py
python tools/build_site_data.py
```

The final dry run must be deterministic and `Stale team files: 0` unless an intentional unpublish is part of the change.

## 12. Local visual QA

Serve the static site:

```bash
python -m http.server 8000 --directory site
```

Open the forwarded Codespaces port 8000.

The target program gets detailed QA. Check:

- directory/search routing;
- program metadata and colors;
- current conference;
- achievements;
- overall record;
- first and last season;
- season and opponent summaries;
- representative early and recent games;
- postseason and overtime;
- representative venue/location enrichment;
- opponent links and filters.

Also open one or two representative existing public programs, including any materially affected by reconciliation or enrichment.

Run a full existing-public-program regression only when shared frontend, JSON schema, builder behavior, or broad shared-data changes warrant it.

## 13. Explicit staging and commit

Never use `git add -A`.

Stage only intended global, reference, generated, and approved cross-program files.

Inspect:

```bash
git --no-pager diff --cached --name-only
git --no-pager diff --cached --stat
git status --short
```

Confirm unrelated prototypes, scratch files, and local artifacts remain unstaged.

Commit the global/publication changes after the final gates pass.

## 14. Final branch gate

Before push:

```bash
python tools/validate_data.py
python tools/ingest_school.py "$school_key"
python tools/build_site_data.py
git status -sb
```

Requirements:

- validator PASS;
- target ingestion NO-OP;
- zero remaining canonical enrichments;
- expected public-page and team-JSON counts;
- zero unexplained stale files;
- only intended commits and files on the branch.

## 15. Push, PR and merge

Push the onboarding branch:

```bash
git push -u origin "$branch_name"
```

In GitHub, create a Pull Request with:

```text
base:    main
compare: data/<school_key>-onboarding
```

The PR summary should include:

- source cutoff and row count;
- existing/new/enrichment counts;
- identity-review disposition;
- discrepancy counts and final dispositions;
- any intentionally unresolved historical conflict;
- validation and NO-OP result;
- site-build counts;
- QA result;
- cross-program corrections or enrichments.

Verify the intended commits and files, wait for required checks, and merge the PR into `main`.

## 16. Sync main and verify production

After the PR is merged:

```bash
git switch main
git fetch origin
git pull --ff-only origin main

python tools/validate_data.py
python tools/ingest_school.py "$school_key"
python tools/build_site_data.py
```

Merged `main` must reproduce the validated, no-op, deterministic state from the onboarding branch.

Merging to `main` triggers Vercel Production automatically.

Before declaring the school closed, verify production:

- target appears in the directory;
- target page loads;
- record, metadata, achievements, and current conference are correct;
- representative early/recent games render;
- representative venue/location data renders;
- one or two representative previously public programs still open, including any existing program materially affected by the onboarding.

Only then is the school closed.

## 17. Stop rules

Stop and ask the project owner if:

- game identity is ambiguous;
- inclusion or exclusion is uncertain;
- a current Division I opponent identity is unclear;
- two credible sources conflict materially;
- a populated canonical value would need to be overwritten;
- a broad global identity change is required;
- dry-run counts are surprising;
- validation fails;
- the final ingestion is not a complete no-op;
- generated site changes cannot be explained;
- production does not match merged `main`.

Unknown is an acceptable value. An unsupported guess is not.
