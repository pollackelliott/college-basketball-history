# College Basketball History

A structured historical database and public website for NCAA Division I men’s college basketball.

The project is built around one central idea: **one real basketball game is one canonical game**. School record books, media guides, official schedules, and other historical sources may provide overlapping or conflicting evidence for that game, but they do not create duplicate game records.

The repository combines source preservation, reconciliation, historical program metadata, venue and conference history, validation tooling, and generated site data into one repeatable onboarding pipeline.

## Project Scope

The site is designed to cover the complete recognized history of current Division I men’s basketball programs through the most recently completed season.

Current Division I programs may receive public team pages. Historical opponents, former Division I programs, lower-division schools, defunct programs, and other opponents remain valid database identities and appear in game histories even when they do not receive public pages of their own.

Program history is **perspective-scoped**. Each program has an approved `history_start_season` defining the first season included in that program’s public history. For longstanding major-college programs, this may predate the formal creation of NCAA Division I. For programs that reached the top level later, earlier lower-division history is excluded from that program’s public records and aggregates.

## Core Data Principles

### One game, one canonical record

A game is represented once in the canonical layer. Multiple source records can point to the same canonical game through source assertions.

### Preserve evidence, including disagreement

Source rows are preserved even when they conflict. Differences between sources are recorded rather than silently overwritten.

### On-court history controls public results

The result that occurred on the court controls public historical records. Administrative actions such as later vacatur are preserved separately rather than rewriting the on-court result.

### Home / away / neutral is independent from geography

Site classification (`HOME`, `AWAY`, `NEUTRAL`, or unknown) is not inferred solely from venue, city, opponent geography, participant home city, or venue chronology.

Explicit game-level evidence controls site classification. Venue and location history can support venue/location normalization only after the site classification is independently established.

### Unknown is better than unsupported inference

If a historical fact cannot be established confidently, the project prefers a documented unknown over a plausible but unsupported guess.

### Stable identities first

Programs, conferences, venues, and other reusable entities use stable keys. Public display labels are resolved from reference registries rather than duplicated throughout game data.

## Data Architecture

The repository separates source evidence from reconciled historical truth.

### Source / school packages

Each onboarded program uses a six-file package:

```text
schools/<program_key>/
├── source-games.csv
├── opponents.csv
├── venues.csv
├── conferences.csv
├── notes.md
└── source-notes.md
```

These files preserve the school-specific extraction, normalization decisions, historical conference membership, venue information, and research notes used during onboarding.

### Canonical data

```text
data/canonical/games.csv
```

Contains the deduplicated canonical game layer.

### Evidence

```text
data/evidence/game-assertions.csv
```

Connects source assertions to canonical games while preserving what each source claimed.

### Reconciliation

```text
data/reconciliation/discrepancies.csv
```

Tracks unresolved and resolved conflicts between sources. Resolved discrepancies remain part of the historical provenance rather than being deleted.

### Reference data

Important registries include:

```text
data/reference/programs.csv
data/reference/program-accomplishments.csv
data/reference/conferences.csv
data/reference/conference-membership.csv
```

`programs.csv` stores core program identity and history-scope metadata.

`program-accomplishments.csv` is the sole reference authority for program accomplishment cards such as conference championships, NCAA Tournament appearances, Final Fours, national championships, Best Finish, and Best Finish Year.

`conferences.csv` stores centrally approved conference identities and tournament display labels.

## Program History Scope

Before a new program is ingested, its site history boundary must be explicitly established.

The project owner supplies one of two rulings:

```text
Program has always been D1/top-level for our site purposes.
```

or:

```text
First year in D1/top-level for our site purposes is YYYY-YY.
```

That ruling establishes `history_start_season`.

Pre-cutoff source evidence may remain preserved in the school package, but it does not contribute to that program’s public:

- game history
- on-court record
- season totals
- opponent records
- opponent counts
- conference accomplishments
- NCAA Tournament accomplishments
- other team-page aggregates

A canonical game can still remain globally valid if it is in scope from the other participant’s perspective.

## Program Accomplishments

Program accomplishment data is maintained separately from core program identity.

Public cards include:

1. On-Court Record
2. Conference Regular Season Championships
3. Conference Tournament Championships
4. NCAA Tournament Appearances
5. Final Fours
6. National Championships
7. Best Finish
8. Best Finish Year

`Best Finish` means the program’s best NCAA Tournament finish. `Best Finish Year` is the calendar year in which that tournament concluded, using the most recent year when the same best finish occurred multiple times.

Accomplishment data is cross-checked against canonical postseason history where derivable and verified against authoritative school sources during onboarding.

## Historical Conference Tournament Labels

Conference tournament display is resolved from the program’s verified historical conference membership in the season of the game.

Examples of public labels may include:

```text
SEC Tournament
Big Ten Tournament
Big Eight Tournament
Southwest Conference Tournament
```

Compact mobile labels are stored centrally as well.

Conflicting event/source wording is retained for audit purposes but does not automatically override verified historical membership. Unresolved cases fall back safely to `Conference Tournament`.

## Onboarding Workflow

The authoritative onboarding procedures live in:

```text
docs/school-onboarding-fast-path.md
docs/new-team-onboarding-runbook.md
docs/team-onboarding-playbook.md
docs/data-schema.md
```

`docs/school-onboarding-fast-path.md` is the required operational procedure for
new schools. It consolidates post-portfolio work into a sealed preflight/approval
plan and one preview/merge approval, designed to be run by Codex in the project
Codespace. The longer runbook remains the authority for historical and data rules.

At a high level, a new program moves through:

1. source intake and readiness review
2. owner-approved history scope
3. source extraction and six-file package construction
4. opponent, venue, and conference normalization
5. canonical matching and reconciliation
6. location / venue QA
7. accomplishment cross-check and source verification
8. validation and target-team no-op proof
9. deterministic site-data generation
10. public-page review and publication

A completed onboarding should end with a target-team dry run showing no remaining work, including:

```text
Canonical enrichments: 0 games / 0 fields
New canonical games: 0
Assertions to add: 0
Discrepancies to add: 0
```

## Validation and Tooling

Run the automated test suite:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```

Validate the repository data layers:

```bash
PYTHONDONTWRITEBYTECODE=1 python tools/validate_data.py
```

Check whether generated public site data is current:

```bash
PYTHONDONTWRITEBYTECODE=1 python tools/build_site_data.py
```

Regenerate public site data when an intentional source/reference change requires it:

```bash
PYTHONDONTWRITEBYTECODE=1 python tools/build_site_data.py --apply
```

Check a program package without modifying global data:

```bash
PYTHONDONTWRITEBYTECODE=1 python tools/ingest_school.py <program_key> --check-package
```

Run the permanent consolidated onboarding preflight:

```bash
PYTHONDONTWRITEBYTECODE=1 python tools/onboard_school.py <program_key> --preflight
```

After the sealed apply, prepare the exact PR and Preview gate:

```bash
PYTHONDONTWRITEBYTECODE=1 python tools/release_school.py <program_key> --prepare
```

Cross-check canonical NCAA accomplishments for a program:

```bash
PYTHONDONTWRITEBYTECODE=1 python tools/verify_program_accomplishments.py <program_key>
```

## Local Site Preview

The public site is generated from repository data and can be previewed locally with a simple static server:

```bash
cd site
python -m http.server 8000
```

Then open port `8000` in the development environment.

## Repository Structure

```text
college-basketball-history/
├── data/
│   ├── canonical/
│   ├── evidence/
│   ├── reconciliation/
│   └── reference/
├── docs/
├── schools/
├── site/
│   └── data/
├── tests/
└── tools/
```

The repository intentionally separates:

- raw/source evidence
- canonical historical records
- reconciliation/provenance
- reusable reference registries
- generated public site data

That separation allows the project to preserve historical evidence while still publishing a single coherent game history.

## Data Integrity Philosophy

Changes should be narrow, auditable, and reproducible.

Before publishing new or corrected data:

- preserve source assertions
- do not duplicate canonical games
- record real conflicts
- avoid unsupported inference
- use stable registry keys
- run tests and validation
- regenerate site data deterministically
- confirm target-team ingestion is a no-op

The goal is not merely to collect historical schedules. It is to build a traceable, maintainable historical record in which every published game can be reconciled back to its supporting evidence.
