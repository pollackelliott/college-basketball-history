# College Basketball History — New-Team Onboarding Playbook

**Audience:** Project owner and collaborator
**Status:** Partner-ready v3 companion to `docs/new-team-onboarding-runbook.md`
**Current coverage standard:** through 2025-26

> **Required fast path:** Use `docs/school-onboarding-fast-path.md` and the two
> repository commands `tools/onboard_school.py` and `tools/release_school.py` for
> every new team. The numbered manual sequence below remains a troubleshooting and
> recovery reference. Do not use it as the normal serial handoff procedure.

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

Before ingestion, obtain one explicit owner scope statement: either the program has
always been D1/top-level for site purposes, or its first top-level season is `YYYY-YY`.
Record the resulting `history_start_season`, `OWNER_CONFIRMED` status,
`ALWAYS_TOP_LEVEL_FROM_INCEPTION` or `FIRST_TOP_LEVEL_SEASON` basis, and notes in
`data/reference/programs.csv`. Missing scope is a hard ingest stop.

Preserve source rows before that boundary, but exclude them from target ingestion and
all public target aggregates. Do not change `raw_text` or misuse `normalization_status`
to encode the history boundary.

Key rules:

- include every recognized non-exhibition varsity game;
- exclude exhibitions;
- curate through 2025-26;
- use established global program keys for current Division I opponents;
- preserve raw source text even when normalized values are corrected;
- never infer site solely from venue;
- use venue chronology to fill location only after site is independently established;
- treat normalized city/state as one atomic pair: populate both or leave both blank;
- keep incomplete or foreign source wording in raw/event fields until an explicit normalized representation is owner-approved;
- reject venue names, narrative footnotes, and combined multi-city labels in normalized city;
- document source typos, undated games, uncertainty, and material curation decisions.

Explicit game-level location outranks venue chronology. Registry fallback requires
an explicit curated/source venue identity, independently established H/A/N, and a
complete registry city/state pair. It records a machine-checkable provenance
marker; it never establishes or changes H/A/N.

Public game types use `regular season`, `conference tournament`, `NCAA tournament`, `NIT`, and generic `postseason` under the detailed runbook's canonical values. Regular-season events and tournaments remain regular season; generic `postseason` is reserved for non-NCAA, non-NIT postseason events.

## 4. Compact package QA

Do not manually re-prove every game.

Confirm that:

- `source-games.csv` contains the intended competitive game universe;
- the aggregate on-court W-L-T record reconciles to authoritative school history;
- opponent keys resolve through `opponents.csv`;
- curated venues resolve through `venues.csv`;
- site values are valid;
- normalized city/state are both populated or both blank;
- conference eras are coherent, non-overlapping, and use registered conference keys;
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
python tools/ingest_school.py "$school_key" --check-package
```

The target-package check compares each source row only with the assertion
generated from that same row, including game date, curated site/venue,
city/state, event text, and `raw_text`. New onboarding must be synchronized;
known legacy drift is reported separately rather than silently accepted.

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

Before enabling the public page, confirm the target's current conference row and verify
its `data/reference/program-accomplishments.csv` row against authoritative sources:

- conference regular-season championships;
- conference tournament championships;
- NCAA Tournament appearances;
- NCAA Final Four appearances;
- NCAA national championships.
- Best Finish and the most recent calendar year attaining it.

Run `python tools/verify_program_accomplishments.py "$school_key"` as a canonical
cross-check. Regular-season conference titles remain source-only; conference-tournament
title-game wins are supporting evidence rather than sole authority. Stop on any
baseline/source/canonical disagreement. A new public program is onboarding-complete
only after `verification_status = VERIFIED`.

Check every interval in `schools/<school_key>/conferences.csv` against `data/reference/conferences.csv`. A missing historical identity is an owner-review stop: add its proper historical key/name and owner-approved tournament label centrally rather than guessing an abbreviation. Do not conflate historically distinct naming eras merely because the conferences are related. Until a label is approved, mobile conference-tournament display must safely remain `Conference Tournament`.

The displayed program's verified membership in the game season controls its conference-tournament presentation: mobile uses `<tournament_label> T`, while full team-history views use `<conference_name> Tournament`. Conflicting source/event wording is review metadata only; it must not override membership. Correct an actual membership-history error through owner-reviewed research in the school's `conferences.csv`, never through a game-level display exception.

Confirm historical conference intervals and accomplishments before the approved cutoff
are absent from public aggregates. Then change only the target's
`public_page_enabled` value from `No` to `Yes`.

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
python tools/ingest_school.py "$school_key" --check-package
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
- historical mobile tournament labels use the target's conference in the game season; unresolved cases display `Conference Tournament`;
- representative early/recent games render;
- representative venue/location data renders;
- one or two representative previously public programs still open, including any existing program materially affected by the onboarding.

Only then is the school closed.

## 17. Stop rules

Stop and ask the project owner if:

- game identity is ambiguous;
- inclusion or exclusion is uncertain;
- a historical conference identity or tournament abbreviation is not yet owner-approved;
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
