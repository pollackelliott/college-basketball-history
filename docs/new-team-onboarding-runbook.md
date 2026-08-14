# New Team Onboarding Runbook

**Project:** College Basketball History

**Document status:** Partner-ready v2

**Validated:** August 10, 2026

**Repository:** `/workspaces/college-basketball-history`

**Public site:** <https://college-basketball-history.vercel.app>

> Florida and Tennessee completed successive production onboarding validations on August 10, 2026. Tennessee established the stable routine path for Partner-ready v2: build a complete six-file package, let ingestion surface a finite set of matches, enrichments, identity questions, and conflicts, and reserve heavier rehearsal work for cases that actually need it.

## 1. Purpose

This runbook explains how to add one current Division I men's basketball program to the project without duplicating games, losing source evidence, silently overwriting conflicts, or breaking existing public program pages.

For the current expansion cycle, every new program is curated through **2025-26**, the most recently completed season as of August 2026.

The standard routine workflow is:

1. Select the program and gather authoritative sources.
2. Resolve material research questions before package construction.
3. Build the complete six-file school package.
4. Run compact structural and historical package QA.
5. Commit the six-file source package on a dedicated onboarding branch.
6. Dry-run ingestion and resolve any identity-review cases.
7. Use an isolated rehearsal only when the safety conditions in Section 12 warrant it.
8. Apply ingestion on the onboarding branch.
9. Review the finite discrepancy set and reconcile approved conflicts.
10. Validate and prove a complete target-school no-op.
11. Populate publication metadata and enable the public page.
12. Build deterministic public site data.
13. Perform targeted new-team QA plus a light affected-existing-team smoke test.
14. Commit explicitly, push the branch, open a pull request into `main`, merge, and verify production.

The central operational principle is:

> **The six-file school package is the primary onboarding deliverable.**

Do the expensive historical research while constructing that package. Once it is coherent, ingestion should reduce the remaining global work to a finite set of machine-identified matches, enrichments, identity questions, and genuine source conflicts rather than requiring another manual proof of thousands of games.

## 2. Core data principle

**One actual basketball game exists exactly once in the canonical database. Everything else is evidence about that game.**

A game reported by both Florida and Missouri is not two canonical games. It is:

- one row in `data/canonical/games.csv`;
- one Florida source assertion;
- one Missouri source assertion; and
- zero or more reconciliation records if the sources disagree.

School packages are curated inputs. The global canonical, evidence, reconciliation, and website files are shared outputs. Do not maintain a separate hand-edited public team page.

## 3. Current project rules

These rules are binding unless the project owner explicitly changes them.

- Curate every new current-Division-I program through the most recently completed season required by the project owner. For the current onboarding cycle, coverage is through **2025-26**.
- Include every recognized non-exhibition varsity game in the program's history.
- Exclude exhibitions from canonical games and all public totals.
- Historical, defunct, club, military, and non-Division-I opponents remain valid opponents and count in records when the contests were recognized varsity games.
- Public records use the on-court result. Forfeits, vacated games, vacated wins, and similar administrative actions are stored separately.
- **Never infer home/away/neutral solely from a venue or venue chronology.**
- Site classification and venue assignment answer different questions. Explicit game-level H/A/N evidence controls site classification.
- Once a game's site classification is independently established, venue/location may be populated from explicit game-level evidence or from a documented curated venue relationship/chronology when no stronger contradictory evidence exists.
- Venue chronology may fill a venue for an already-established home game; it may never be used to establish that the game was home.
- Explicit game-level venue/location evidence overrides a chronology fallback.
- Normalized domestic `city` and `state` are one atomic pair: populate both or leave both blank. Incomplete wording may remain in `raw_text` or event fields; do not turn it into partial public geography.
- Rare foreign or territory cases require an explicit owner-reviewed representation. Until approved, preserve the source wording and leave normalized city/state blank rather than guessing a country taxonomy.
- Preserve source assertions even when another source establishes a different canonical value.
- Keep resolved discrepancies as provenance. Resolution does not mean deletion.
- Do not invent an exact date, venue, opponent identity, or site classification when the evidence is insufficient.
- Aggregate season records and opponent-series summaries are QA evidence, not canonical truth.
- Stable keys are identifiers, not public display labels.
- Public opponent and venue names come from canonical registries. Do not manufacture a display name by prettifying a key when a canonical name exists.
- A current Division-I institution must use its established `data/reference/programs.csv` `program_key`. Do not create a second global key for a spelling variant of the same institution.
- When duplicate global identities are discovered, stop and reconcile them across canonical games, evidence, relevant school packages, and public outputs before publication.
- Public special game types are limited to:
  - `CONFERENCE_TOURNAMENT`
  - `NCAA_TOURNAMENT`
  - `NIT`
- All other games use `REGULAR_SEASON`, even when they occurred in a named regular-season event.
- Conference-tournament and NIT rounds are blank except for a title game, which uses `Championship`.
- NCAA rounds use only:
  - `Play-in`
  - `R64`
  - `R32`
  - `Sweet Sixteen`
  - `Elite Eight`
  - `Final Four`
  - `Championship`
- Historical NCAA consolation or third-place games keep `NCAA_TOURNAMENT` but use a blank canonical round.

## 4. Roles and approval boundaries

### Researcher / package preparer

- Collects official sources.
- Extracts game rows.
- Normalizes opponent identities, sites, venues, conferences, and postseason metadata.
- Builds all six school files.
- Records uncertainty instead of guessing.
- Runs package QA and ingestion dry runs.

### Project owner / reviewer

- Answers material clarification questions.
- Approves identity overrides.
- Approves canonical changes when sources conflict.
- Approves public-page enablement and deployment.
- Reviews any step marked **OWNER REVIEW REQUIRED** in this runbook.

### Stop rule

Stop and ask the project owner whenever a decision could change which real game a row represents, whether a game belongs in the dataset, or which conflicting source should control a canonical fact. Do not convert uncertainty into certainty merely to make the pipeline pass.

## 5. Authoritative source package

Every onboarded school must have exactly these six tracked files:

```text
schools/<school_key>/
├── source-games.csv
├── opponents.csv
├── venues.csv
├── conferences.csv
├── notes.md
└── source-notes.md
```

The files have different roles:

| File | Primary role | Current automated consumer |
|---|---|---|
| `source-games.csv` | One normalized source assertion per non-exhibition varsity game | `tools/ingest_school.py`; `tools/match_games.py` |
| `opponents.csv` | Audit trail for source labels and canonical opponent identities | `tools/build_site_data.py` uses canonical keys/names for public display |
| `venues.csv` | Venue registry, aliases, chronology, evidence, and canonical public display names | `tools/ingest_school.py`; `tools/backfill_venue_keys.py`; `tools/build_site_data.py` |
| `conferences.csv` | Program's historical conference timeline | `tools/ingest_school.py`; `tools/build_site_data.py`; `tools/validate_data.py` |
| `notes.md` | Final curation decisions, exceptions, known issues, closure status | No current importer; curated/documentary |
| `source-notes.md` | Source hierarchy, coverage, citations, extraction notes, and source limitations | No current importer; curated/documentary |

Important consequences:

- A complete six-file package is required. Historical conference intervals are validated and published once per team document.
- `conferences.csv` does not automatically update `data/reference/conference-membership.csv`.
- `notes.md` and `source-notes.md` must be reviewed as part of the package; validation does not prove they are complete.
- Ingestion automatically compares date, score, result winner, overtime, site type, game type, and postseason round on matched games. It does **not** currently detect every possible venue improvement or automatically fill every blank canonical value.
- The site builder aggregates canonical venue names across all `schools/*/venues.csv` files. Venue evidence discovered through one school can therefore improve display on another school's public page.
- A true cross-package name conflict for the same `venue_key` is a publication blocker. Reconcile it rather than hiding it through slug humanization.
- `data/evidence/game-assertions.csv` is the authoritative generated assertion layer. A school-level `game-assertions.csv`, where present, is a legacy mirror that must agree with its own `source-games.csv`; it is not evidence from another program.

## 6. Sources to gather before extraction

Define the program's final covered season before beginning. Record that cutoff in both Markdown files.

Gather, in this order:

1. Official school year-by-year, game-by-game history or media guide.
2. Official school schedules, recaps, and box scores for seasons newer than the guide's cutoff.
3. Official postseason history from the school, NCAA, NIT, or conference.
4. Official conference-membership history.
5. Official venue history and primary-home chronology.
6. Official administrative-action records for forfeits, vacated games, vacated wins, or stripped appearances/titles.
7. Official opponent records for material conflicts or missing information.
8. Summary tables and opponent-series totals for QA only.
9. Secondary sources only when an official-source gap cannot otherwise be resolved.

For every source, record:

- title;
- publisher/owner;
- URL or supplied filename;
- season coverage;
- relevant pages or sections;
- access date when applicable;
- facts taken from it;
- known limitations or internal inconsistencies.

### Required clarification before package construction

Ask the project owner about any of the following:

- ambiguous school or campus identity;
- a source label that could refer to multiple programs;
- institutional renames, mergers, relocations, or lineage questions;
- a listed contest that may be an exhibition, scrimmage, junior-varsity game, or non-varsity game;
- a score/result conflict inside one source row;
- impossible or incomplete dates;
- two plausible games against the same opponent in the same season;
- a venue that conflicts with explicit home/away notation;
- a host-site event where the host may have been playing at home;
- a postseason game whose tournament or competitive round is unclear;
- an administrative outcome that differs from the played result;
- an aggregate total that implies an unlisted or duplicate game;
- a conflict that would require changing an already-published canonical fact.

## 7. File contracts

Always start from the header of the most recently completed school package in the repository. Do not reconstruct a header from memory. Existing files may contain a leading `index` column; it is a legacy/helper column ignored by ingestion and must never be used as game identity.

### 7.1 `source-games.csv`

One row represents one assertion from the target school's source material.

#### Identity and source fields

| Field | Requirement | Meaning / rule |
|---|---|---|
| `source_game_id` | Tool-required | Permanent ID unique within the source program, such as `FLARAW-00001`; never renumber after ingestion. |
| `source_program_key` | Tool-required | Target program slug; every row must use the same key. |
| `source_era` | Project-required | Concise source grouping such as `historical_media_guide` or `official_schedule`. |
| `season_label` | Tool-required | Consecutive-year format `YYYY-YYYY`, such as `2025-2026`. |
| `season_year` | Recommended | Ending year of the season, if retained by the current template. |
| `game_date` | Required when known | ISO `YYYY-MM-DD`; blank when the exact date is genuinely unknown. Never invent a date. |
| `source_page` | Recommended | Page, section, or stable source locator. |
| `raw_text` | Project-required | Verbatim-enough source row/text to audit the normalization. |
| `normalization_status` | Project-required | Human curation state; use a consistent package taxonomy and explain it in `notes.md`. |
| `notes` | Optional | Row-specific research or interpretation note. |

#### Opponent fields

| Field | Requirement | Meaning / rule |
|---|---|---|
| `source_opponent_label` | Project-required | Opponent exactly as represented by the source, including meaningful qualifiers. |
| `normalized_opponent_name` | Project-required | Canonical display name selected during identity resolution. |
| `normalized_opponent_key` | Tool-required | Stable canonical opponent slug. |
| `opponent_current_d1` | Recommended | `Yes` or `No` at the reference snapshot; historical/non-D1 opponents remain valid. |

Every distinct source label must be explainable through `opponents.csv`. Do not silently collapse two institutions into one key.

#### Result fields

| Field | Requirement | Meaning / rule |
|---|---|---|
| `team_score` | Required when known | Target school's on-court score; integer text. |
| `opponent_score` | Required when known | Opponent's on-court score; integer text. Scores must be both known or both blank. |
| `played_result` | Project-required when known | `W`, `L`, or `T` from the target school's perspective. Scores control when present. |
| `overtime_periods` | Project-required | `0` for none, positive integer when known, blank only when genuinely unknown. |
| `administrative_status` | Optional | Blank, `FORFEIT`, `VACATED_GAME`, or `VACATED_WIN`. |
| `administrative_note` | Required with administrative status | Plain-language explanation and source basis. |

Do not replace a played score/result with the administrative outcome. A vacated win remains an on-court win with separate administrative metadata.

#### Site and venue fields

| Field | Requirement | Meaning / rule |
|---|---|---|
| `source_site_candidate` | Recommended | Raw or parsed site signal from the source. Preserve ambiguity. |
| `curated_site_type` | Project-required | `SOURCE_PROGRAM_HOME`, `OPPONENT_HOME`, `NEUTRAL`, or `UNKNOWN`. |
| `source_venue_name` | Optional | Venue wording from the source. |
| `curated_venue_name` | Optional | Normalized venue name; when filled, it must match `venues.csv` `canonical_name` or an alias. |
| `city` | Optional as part of an atomic pair | Normalized game-site city supported by evidence. Populate together with `state`, or leave both blank. |
| `state` | Optional as part of an atomic pair | Two-letter state/territory abbreviation where applicable. Populate together with `city`, or leave both blank. |

Site and venue answer different questions. A neutral game can occur in a team's usual home arena, and a program-designated home game can occur away from its campus.

`raw_text`, `source_venue_name`, and `event_or_tournament` may retain incomplete, historical, or broader-area wording. The atomic-pair rule applies to normalized/public geography. Reject an arena name, narrative footnote, or combined multi-city event label in normalized `city`.

#### Event and postseason fields

| Field | Requirement | Meaning / rule |
|---|---|---|
| `event_or_tournament` | Optional | Source or curated event name retained for research context. |
| `source_round` | Optional | Round language used by the source. |
| `curated_game_type` | Project-required | `REGULAR_SEASON`, `CONFERENCE_TOURNAMENT`, `NCAA_TOURNAMENT`, or `NIT`. |
| `curated_postseason_round` | Conditional | Canonical round taxonomy; blank when the rules require no public round. |

#### Identity override fields

These fields are exceptional controls, not routine normalization fields.

| Field | Allowed value / role |
|---|---|
| `identity_override` | Blank, `FORCE_NEW`, or `MATCH_SOURCE_ASSERTION`. |
| `identity_override_basis` | Required plain-language basis for any override. |
| `identity_match_program_key` | With `MATCH_SOURCE_ASSERTION`, the already-ingested source program key. |
| `identity_match_source_game_id` | With `MATCH_SOURCE_ASSERTION`, the already-ingested source row ID. |

Rules:

- Use `FORCE_NEW` only when a row is a genuinely distinct game even though a same-season team-pair candidate exists.
- `FORCE_NEW` is rejected if the normal matcher already finds a confident match.
- Use `MATCH_SOURCE_ASSERTION` to link to an existing source assertion; do not hard-code a canonical game ID into the school package.
- Every override requires **OWNER REVIEW** and an evidence-backed basis in the package notes.

### 7.2 `opponents.csv`

One row documents how a source opponent label was resolved.

| Field | Meaning / rule |
|---|---|
| `source_program_key` | Target school key. |
| `source_opponent_label` | Exact or normalized source label being resolved. |
| `canonical_opponent_key` | Stable global opponent key. |
| `canonical_opponent_name` | Public display name; keep it consistent across packages. |
| `current_d1` | `Yes` or `No` at the current reference snapshot. |
| `games_with_source_label` | QA count of target rows using the label. |
| `first_season` | First season using the source label. |
| `last_season` | Last season using the source label. |
| `resolution_status` | Human status, normally resolved before ingestion. |
| `resolution_method` | Exact registry match, alias/lineage normalization, user decision, new historical identity, etc. |
| `user_choice` | Preserve a material owner choice when one was needed. |
| `audit_note` | Explain corrections, ambiguity, or rejected proposals. |

The site builder aggregates canonical opponent names across every package. It tolerates harmless punctuation/footnote differences, but stops on genuinely conflicting names for the same key. Resolve those conflicts before publication.

For current Division I programs, `data/reference/programs.csv` is the authoritative identity registry. Reuse its established `program_key` and naming convention.

If a new package exposes redundant historical keys for the same institution, stop and reconcile the identity globally before publication. Update the canonical games, evidence assertions, relevant school-package normalized fields, reference display naming when appropriate, and generated public outputs consistently. Do not solve an identity collision merely by changing a display label while leaving duplicate keys in use.

Preserve genuinely different historical entities. Similar names are not sufficient evidence for a merge.

### 7.3 `venues.csv`

The ingestion script currently consumes `venue_key`, `canonical_name`, and optional semicolon-delimited `aliases`. The other fields preserve chronology and curation evidence.

| Field | Meaning / rule |
|---|---|
| `source_program_key` | Target school key. |
| `venue_key` | Stable canonical venue slug. |
| `canonical_name` | Normalized venue display name. |
| `aliases` | Optional semicolon-delimited aliases; each must unambiguously identify this venue. |
| `city` / `state` | Venue location. |
| `venue_type` | Arena, gymnasium, fieldhouse, etc. |
| `known_opened` / `known_closed` | Supported dates or date descriptions. |
| `venue_date_precision` | Precision of opening/closing evidence. |
| `games_currently_assigned` | Derived QA count, not independent truth. |
| `first_assigned_game` / `last_assigned_game` | QA range of current assignments. |
| `relationship_type` | `primary_home` or another documented program relationship. |
| `relationship_start` / `relationship_end` | Supported relationship range. |
| `relationship_date_precision` | Precision of the relationship range. |
| `site_rule` | Evidence-backed default or interpretive note; never overrides stronger game-level evidence. |
| `source_basis` | Source establishing the venue or relationship. |
| `notes` | Exceptions and unresolved chronology. |

If a source establishes a city but not an exact arena, fill the city and leave `curated_venue_name` blank. Precision is preferable to false completeness.

A documented primary-home chronology may fill a missing venue/location only after the game has independently been established as a home game and only when no explicit game-level evidence contradicts the chronology.

When a confidently matched source row supplies supported metadata for a blank canonical field, ingestion may enrich the canonical game. Venue/location enrichment requires the source and canonical site classifications to independently agree; venue evidence never establishes home/away/neutral classification.

Registry fallback additionally requires an explicit curated/source venue identity and a complete registry city/state pair. Explicit game-level geography wins; never combine a partial source pair with registry metadata. Future registry-derived canonical enrichment is recorded in canonical `notes` with a machine-checkable `VENUE_REGISTRY_FALLBACK` marker identifying the linked source row, registry `venue_key`, independently established `site_type`, and fields filled.

When the same `venue_key` appears in several registries, normalized city/state must agree. A genuine reviewed locality-label exception must be documented in every involved registry row with `VENUE_LOCATION_VARIANT:`.

`venue_key` is an identity field, not a presentation field. `canonical_name` is the public venue label. Generated public game data should carry both `venue_key` and `venue_name`; the frontend must prefer the canonical `venue_name` rather than manufacturing a label from the slug.

### 7.4 `conferences.csv`

| Field | Meaning / rule |
|---|---|
| `source_program_key` | Target school key. |
| `start_season` | First season in the interval. |
| `end_season` | Last season; blank only for an ongoing interval. |
| `conference_key` | Stable conference slug or `independent`. |
| `conference_name` | Historical display name for the interval. |
| `membership_type` | Normally `conference` or `independent`. |
| `ongoing` | `True` or `False`. |
| `basis` | Authoritative source for the interval. |
| `notes` | Renames, defunct status, transition nuance, or cutoff statement. |

Intervals must not overlap and should cover the program's curated history without unexplained gaps.

Every `conference_key` must already exist in `data/reference/conferences.csv`. That central registry is the only source for owner-approved mobile conference-tournament labels. Never manufacture a short label algorithmically or copy it into game rows.

If research finds a historical identity absent from the registry, stop for owner review before publication. Obtain the correct historical name, stable key, and tournament label, then add them centrally. Keep historically distinct naming eras distinct when their tournament presentation differs; do not collapse identities such as Pac-10/Pac-12 or an old historical Metro Conference/a later rebranded Metro merely because they are related.

The site builder publishes this interval history once in the target team document. Conference-tournament display resolves the displayed program's game season against exactly one interval. Mobile uses the approved `<tournament_label> T`; full team-history views use the registry's `<conference_name> Tournament`. Zero or multiple interval matches, `independent`, or an unavailable required registry label must display exactly `Conference Tournament`.

Season-specific conference membership controls this presentation. Conflicting source/event tournament wording is preserved as team-level review metadata but never silently redefines membership or overrides the public label. A genuine membership-history correction requires owner-reviewed research and belongs in `schools/<program>/conferences.csv`, not a game-level UI exception.

The public site's current conference still comes from `data/reference/conference-membership.csv`, whose current snapshot is `2026-2027`. Confirm the target already has the correct reference row.

### 7.5 `notes.md`

This is the final curation record. Use these sections as a minimum:

1. Program status and exact coverage cutoff.
2. Canonical competitive game count and on-court record.
3. Exhibitions excluded.
4. Season/date exceptions.
5. Home venue chronology and site policies.
6. Neutral/host-site event policies.
7. Conference history and tournament-label rules.
8. NCAA, NIT, and conference-tournament decisions.
9. Administrative actions.
10. Cross-source reconciliations.
11. Known unresolved questions.
12. Public presentation notes.

“Closed” means complete under current rules through the documented cutoff, not immutable.

### 7.6 `source-notes.md`

This is the source and extraction audit trail. Use these sections as a minimum:

1. Source hierarchy.
2. Primary historical source and pages.
3. Modern-season supplementation.
4. Row counts by source era and total.
5. Conference source.
6. Venue sources.
7. Postseason sources and aggregate QA totals.
8. Cross-source evidence.
9. Known source inconsistencies.
10. Exhibition treatment.

## 8. Git safety and clean baseline

Do not run the obsolete rebase procedure used in earlier sessions. Do not use `origin/ma`. This workflow does not require a rebase.

Start in a fresh terminal:

```bash
cd /workspaces/college-basketball-history
git fetch origin --tags
git switch main
git pull --ff-only origin main
git status -sb
git log -3 --oneline --decorate
python tools/validate_data.py
```

Proceed only when:

- local `main` and `origin/main` are synchronized;
- no tracked file is modified;
- validation passes;
- any untracked files are understood and unrelated.

Create a dedicated branch:

```bash
school_key="florida"
branch_name="data/${school_key}-onboarding"
git switch -c "$branch_name"
```

Replace `florida` with the selected team key. Keep the same `school_key` value for the remainder of the workflow.

### CRLF-aware whitespace checking

Several repository CSVs currently use CRLF line endings. Bare `git diff --check` can report thousands of false-positive trailing-whitespace errors on those files. Do not use it as the general onboarding whitespace gate.

Use this repository-safe check instead:

```bash
python - <<'PY2'
import subprocess
from pathlib import Path

files = subprocess.check_output(
    ["git", "diff", "--name-only", "HEAD"],
    text=True,
).splitlines()

bad = []

for name in files:
    path = Path(name)

    if not path.is_file():
        continue

    if path.suffix.lower() not in {
        ".csv", ".py", ".html", ".json", ".md"
    }:
        continue

    for line_no, line in enumerate(path.read_bytes().splitlines(), 1):
        if line.endswith((b" ", b"\t")):
            bad.append((name, line_no))

if bad:
    print("FAIL: genuine trailing whitespace:")
    for name, line_no in bad[:50]:
        print(f"  {name}:{line_no}")
    raise SystemExit(1)

print("PASS: no genuine trailing spaces/tabs in changed text files.")
PY2
```

For readable Git inspection, prefer `git --no-pager diff` and `git --no-pager diff --cached`. This avoids leaving the terminal inside the `less` pager during a long diff.

## 9. Build and QA the six-file package

Create `schools/$school_key/` and populate all six files. Do not begin ingestion with a partial package.

### Manual package QA checklist

- [ ] Exactly one row exists per recognized non-exhibition varsity game.
- [ ] Every `source_game_id` is nonblank and unique for the target school.
- [ ] Every row uses the target `source_program_key`.
- [ ] Every opponent key is nonblank and documented in `opponents.csv`.
- [ ] Every season label is a consecutive `YYYY-YYYY` pair.
- [ ] Exact dates are valid ISO dates; unknown dates remain blank.
- [ ] Scores are both populated or both blank.
- [ ] Scores and `played_result` agree, except for explicitly documented source errors preserved as evidence.
- [ ] Overtime values agree with raw source text.
- [ ] Exhibitions are absent.
- [ ] Site classification is game-specific.
- [ ] Exact venues are assigned only when supported.
- [ ] Normalized city/state are both populated or both blank on every new source row.
- [ ] Normalized city contains no venue name, narrative footnote, or combined multi-city label.
- [ ] Every curated venue name resolves through `venues.csv`.
- [ ] Conference intervals do not overlap or leave unexplained gaps.
- [ ] Postseason types and rounds follow Section 3.
- [ ] Administrative actions are separated from played results.
- [ ] Aggregate season records and postseason totals have been compared as QA.
- [ ] Every mismatch is resolved, explicitly under review, or documented as a source limitation.
- [ ] `notes.md` and `source-notes.md` state the coverage cutoff and source hierarchy.

### Read-only structural package check

This temporary check uses only Python's standard library and changes nothing. It does not replace research review.

```bash
SCHOOL_KEY="$school_key" python - <<'PY'
import csv
import datetime as dt
import os
import re
from pathlib import Path

school = os.environ["SCHOOL_KEY"]
root = Path("schools") / school
required_files = {
    "source-games.csv",
    "opponents.csv",
    "venues.csv",
    "conferences.csv",
    "notes.md",
    "source-notes.md",
}
errors = []
warnings = []

missing = sorted(name for name in required_files if not (root / name).is_file())
if missing:
    errors.append("Missing files: " + ", ".join(missing))

def rows(name):
    path = root / name
    if not path.is_file():
        return [], []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)

game_fields, games = rows("source-games.csv")
opp_fields, opponents = rows("opponents.csv")
venue_fields, venues = rows("venues.csv")
conf_fields, conferences = rows("conferences.csv")

required_game_fields = {
    "source_game_id", "source_program_key", "season_label",
    "normalized_opponent_key", "normalized_opponent_name",
    "team_score", "opponent_score", "played_result",
    "overtime_periods", "curated_site_type", "curated_game_type",
    "curated_postseason_round", "raw_text",
}
for field in sorted(required_game_fields - set(game_fields)):
    errors.append(f"source-games.csv missing column: {field}")

ids = [row.get("source_game_id", "").strip() for row in games]
if any(not value for value in ids):
    errors.append("Blank source_game_id found")
if len(ids) != len(set(ids)):
    errors.append("Duplicate source_game_id found")

opponent_keys = {
    row.get("canonical_opponent_key", "").strip()
    for row in opponents
    if row.get("canonical_opponent_key", "").strip()
}
venue_names = set()
for row in venues:
    name = row.get("canonical_name", "").strip().casefold()
    if name:
        venue_names.add(name)
    for alias in row.get("aliases", "").split(";"):
        alias = alias.strip().casefold()
        if alias:
            venue_names.add(alias)

allowed_sites = {"SOURCE_PROGRAM_HOME", "OPPONENT_HOME", "NEUTRAL", "UNKNOWN"}
allowed_types = {"REGULAR_SEASON", "CONFERENCE_TOURNAMENT", "NCAA_TOURNAMENT", "NIT"}
allowed_rounds = {"", "Play-in", "R64", "R32", "Sweet Sixteen", "Elite Eight", "Final Four", "Championship"}
season_re = re.compile(r"^(\d{4})-(\d{4})$")

for line, row in enumerate(games, start=2):
    label = row.get("source_game_id", "").strip() or f"line {line}"
    if row.get("source_program_key", "").strip() != school:
        errors.append(f"{label}: wrong source_program_key")

    season = row.get("season_label", "").strip()
    match = season_re.fullmatch(season)
    if not match or int(match.group(2)) != int(match.group(1)) + 1:
        errors.append(f"{label}: invalid season_label {season!r}")

    date = row.get("game_date", "").strip()
    if date:
        try:
            dt.date.fromisoformat(date)
        except ValueError:
            errors.append(f"{label}: invalid ISO game_date {date!r}")

    key = row.get("normalized_opponent_key", "").strip()
    if not key:
        errors.append(f"{label}: blank normalized_opponent_key")
    elif key not in opponent_keys:
        errors.append(f"{label}: opponent key {key!r} absent from opponents.csv")

    team_score = row.get("team_score", "").strip()
    opp_score = row.get("opponent_score", "").strip()
    if bool(team_score) != bool(opp_score):
        errors.append(f"{label}: only one score is populated")
    if team_score and opp_score:
        try:
            team_num, opp_num = int(team_score), int(opp_score)
        except ValueError:
            errors.append(f"{label}: score is not an integer")
        else:
            expected = "W" if team_num > opp_num else "L" if team_num < opp_num else "T"
            played = row.get("played_result", "").strip().upper()
            if played and played != expected:
                warnings.append(f"{label}: score implies {expected}, source result says {played}")

    overtime = row.get("overtime_periods", "").strip()
    if overtime and (not overtime.isdigit() or int(overtime) < 0):
        errors.append(f"{label}: invalid overtime_periods {overtime!r}")

    site = row.get("curated_site_type", "").strip().upper()
    if site not in allowed_sites:
        errors.append(f"{label}: invalid curated_site_type {site!r}")

    city = row.get("city", "").strip()
    state = row.get("state", "").strip()
    if bool(city) != bool(state):
        errors.append(f"{label}: normalized city/state must be both populated or both blank")
    if city.casefold() in venue_names:
        errors.append(f"{label}: normalized city contains a venue name")
    if " and " in city.casefold():
        errors.append(f"{label}: normalized city contains a combined multi-city value")

    game_type = row.get("curated_game_type", "").strip()
    round_name = row.get("curated_postseason_round", "").strip()
    if game_type not in allowed_types:
        errors.append(f"{label}: invalid curated_game_type {game_type!r}")
    if round_name not in allowed_rounds:
        errors.append(f"{label}: invalid curated_postseason_round {round_name!r}")
    if game_type == "REGULAR_SEASON" and round_name:
        errors.append(f"{label}: regular-season game has a postseason round")
    if game_type in {"CONFERENCE_TOURNAMENT", "NIT"} and round_name not in {"", "Championship"}:
        errors.append(f"{label}: {game_type} round must be blank or Championship")

    venue = row.get("curated_venue_name", "").strip()
    if venue and venue.casefold() not in venue_names:
        errors.append(f"{label}: curated venue {venue!r} absent from venues.csv")

    text = " ".join([
        row.get("raw_text", ""),
        row.get("event_or_tournament", ""),
        row.get("notes", ""),
    ]).casefold()
    if "exhib" in text:
        warnings.append(f"{label}: contains exhibition-like text; confirm exclusion status")

for name, table in [("opponents.csv", opponents), ("venues.csv", venues), ("conferences.csv", conferences)]:
    for line, row in enumerate(table, start=2):
        value = row.get("source_program_key", "").strip()
        if value and value != school:
            errors.append(f"{name} line {line}: wrong source_program_key {value!r}")

print(f"School: {school}")
print(f"Source games: {len(games):,}")
print(f"Opponent rows: {len(opponents):,}")
print(f"Venue rows: {len(venues):,}")
print(f"Conference rows: {len(conferences):,}")
for warning in warnings:
    print("WARNING:", warning)
if errors:
    for error in errors:
        print("ERROR:", error)
    raise SystemExit(1)
print("PASS: basic six-file structural checks succeeded; manual source QA is still required.")
PY
```

Resolve every error. Review every warning.

## 10. Commit the source package before ingestion

Run the CRLF-aware whitespace check from Section 8, then review exactly what will be committed:

```bash
git status --short
git add "schools/$school_key"
git diff --cached --stat
git commit -m "Add ${school_key} source package"
```

Confirm the commit contains all six files:

```bash
git show --stat --oneline HEAD
git ls-tree -r --name-only HEAD "schools/$school_key"
```

Expected result: exactly the six required filenames, with no unrelated changes.

## 11. Ingestion dry run and identity review

Run:

```bash
python tools/ingest_school.py "$school_key"
git status -sb
```

The dry run changes nothing. Review:

- `Source rows`
- `Existing-game matches`
- `New canonical games`
- `Identity review required`
- `Canonical enrichments`
- `Assertions to add`
- `Discrepancies to add`

Identity counts must satisfy:

```text
Existing-game matches + New canonical games + Identity review required = Source rows
```

For a first ingestion:

- `Source rows` must equal the competitive rows in the package.
- `Assertions to add` will normally equal `Source rows`.
- Existing matches are games already represented through another source.
- New canonical games represent the rest of the target's history.
- Canonical enrichments are supported blank fields filled on already-matched games.
- Unexpected counts are a stop signal.

### Safe matched-game enrichment

For a confidently matched existing game:

```text
canonical blank + supported source value -> enrich canonical
same value + same value                 -> no action
populated values conflict               -> discrepancy
source value unknown/unsupported        -> no action
```

Safe enrichment may fill supported blank metadata such as:

- `venue_key`
- `site_city`
- `site_state`
- `designated_home_team_key`

For venue/location enrichment, source and canonical site classifications must independently agree.

**Venue evidence never establishes or changes home/away/neutral classification.**

Explicit game-level city/state evidence takes precedence over venue-registry fallback information.

### If identity review is required

The ingester stops all writes when even one identity requires review.

Common causes include:

- repeated opponents in the same season;
- incomplete/conflicting date or score information;
- a possible duplicate already represented elsewhere;
- missing source identity fields;
- an invalid identity override;
- one source assertion linked to multiple canonical games.

Resolve the research question first. Use `FORCE_NEW` or `MATCH_SOURCE_ASSERTION` only when justified.

Rerun until:

```text
Identity review required: 0
```

Do not weaken the matcher or invent precision merely to make ingestion proceed.

## 12. Isolated apply rehearsal — conditional safety tool

An isolated rehearsal remains available, but it is **not required for every routine school** once the current ingestion engine has already been production-proven.

Perform the rehearsal when any of these conditions applies:

- `tools/ingest_school.py`, the canonical schema, or relevant validator logic changed since the last production-proven onboarding;
- dry-run counts are surprising or cannot be readily explained;
- identity overrides introduce unusual matching behavior;
- a broad reconciliation/tooling change is part of the onboarding;
- a collaborator is exercising a new or uncertain workflow where a disposable proof materially reduces risk;
- the project owner requests it.

For a routine school using unchanged, already-proven ingestion logic with sensible dry-run counts, proceed directly from reviewed dry run to the real branch apply.

When rehearsal is warranted:

```bash
audit_dir="$(mktemp -d "/tmp/cbb-${school_key}-audit.XXXXXX")"
git archive HEAD | tar -x -C "$audit_dir"

python "$audit_dir/tools/ingest_school.py" "$school_key" --repo "$audit_dir"
python "$audit_dir/tools/ingest_school.py" "$school_key" --apply --repo "$audit_dir"
python "$audit_dir/tools/validate_data.py" "$audit_dir"
python "$audit_dir/tools/ingest_school.py" "$school_key" --repo "$audit_dir"

printf 'Temporary audit copy: %s\n' "$audit_dir"
```

Expected result after the isolated apply:

- validation passes;
- second ingestion reports zero new canonical games;
- zero canonical enrichments remain;
- zero assertions remain to add;
- zero discrepancies remain to add;
- output includes `NO-OP`.

Do not continue if the isolated second run is not a no-op.

## 13. Apply on the working branch

After the dry-run counts are reviewed and any required isolated rehearsal has passed:

```bash
python tools/ingest_school.py "$school_key" --apply
git status --short
```

The ingester may update:

- `data/canonical/games.csv`
  - append genuinely new games;
  - safely enrich supported blank fields on matched existing games;
- `data/evidence/game-assertions.csv`
  - append the target source assertions;
- `data/reconciliation/discrepancies.csv`
  - append machine-detected material disagreements.

It also runs `tools/validate_data.py` after writing. A successful apply must end with post-write validation passing.

Review the resulting scale of change:

```bash
git --no-pager diff --stat
git --no-pager diff --numstat -- data/canonical/games.csv
git --no-pager diff -- data/reconciliation/discrepancies.csv
```

Do not manually inspect thousands of routine appended rows one by one.

Instead verify:

- applied counts equal the reviewed dry-run counts;
- the validator passes;
- the discrepancy set is finite and understandable;
- representative early, middle, recent, postseason, neutral-site, overtime, and overlap games behave correctly;
- canonical enrichments are blank-to-supported-value changes rather than overwrites.

If a supposedly small metadata edit produces broad formatting churn, stop and investigate file-format preservation before continuing.

## 14. Reconciliation

### What automatic ingestion does

Automatic ingestion:

- matches source rows against canonical games using team pair, season, date, score, and approved identity evidence;
- creates a new canonical game only when the row represents a game not already canonical;
- preserves permanent canonical game IDs;
- adds one source assertion for the incoming source row;
- creates an `UNDER_REVIEW` discrepancy for material nonblank disagreements involving:
  - game date;
  - score;
  - result winner;
  - overtime periods;
  - site type;
  - game type;
  - postseason round;
- safely enriches supported blank canonical metadata on confidently matched games when source and canonical site classifications independently agree;
- does not overwrite a populated conflicting canonical value.

### Matched-game enrichment policy

Supported second-source evidence should improve an existing canonical game rather than remain trapped only in its assertion.

```text
blank + supported evidence = enrich
same + same = no action
conflict + conflict = discrepancy
unknown = remain unknown
```

For matched games, venue/location enrichment is allowed only after site classification is independently established and agrees between source and canonical data.

A venue or home-arena chronology may never establish home/away/neutral on its own.

This mechanism improves only games involving the newly onboarded program. It does **not** constitute a comprehensive audit of every historical venue/site field for an older public program.

### Human-readable discrepancy review

Present newly generated discrepancies to the project owner in a concise review rather than using a giant raw CSV diff as the primary interface.

For each discrepancy show:

- discrepancy ID;
- season/date and matchup;
- disputed field;
- incoming source value;
- current canonical value;
- relevant competing evidence;
- recommended disposition.

The owner should concentrate research effort on this finite conflict set rather than rechecking every source row.

Modern and 21st-century conflicts should usually receive direct official verification when practical.

### Resolution rules

1. Preserve raw source evidence.
2. Prefer contemporaneous official game records or box scores when later summary tables contain apparent typos.
3. Explicit game-level site evidence outranks venue chronology.
4. Do not force a resolution when credible sources remain genuinely in conflict.
5. A resolved discrepancy remains in `discrepancies.csv` with its competing value(s), final canonical value, `RESOLVED` status, evidence-based `resolution_basis`, and explanatory note.
6. Genuine uncertainty may remain `UNDER_REVIEW`.
7. An unresolved historical discrepancy does **not automatically block publication** when game identity is secure, the canonical representation is defensible, the conflict is transparently retained, and the owner approves publication with the flag outstanding.
8. If a normalized package value was demonstrably curated incorrectly, correct the school row and corresponding evidence assertion while preserving raw source text and reconciliation history.
9. If new evidence exposes duplicate opponent/program identities, reconcile the identity globally rather than merely changing a display label.
10. Safe blank-field enrichment does not require a discrepancy record; conflicting populated values do.
11. Material canonical-value changes require owner review.

### Examples

#### Source score typo

If a later guide says 51-63 but contemporaneous official evidence establishes 57-63:

- preserve the guide assertion;
- keep or change canonical to the supported 57-63 as approved;
- document the conflict;
- mark the discrepancy resolved.

#### Genuine unresolved historical conflict

If two credible historical sources report different scores and stronger evidence is unavailable:

- retain both assertions;
- retain the best-supported current canonical value;
- leave the discrepancy `UNDER_REVIEW`;
- do not invent certainty solely to achieve zero open discrepancies.

#### Site versus venue chronology

If venue chronology suggests the target's home arena but explicit game evidence says `at Opponent`, explicit game evidence controls.

#### Overtime normalization error

If raw text contains `(OT)` but a curated normalized field says `0`, correct the normalized field and evidence assertion while preserving the raw source text.

#### Same-season repeated opponent

If the matcher cannot distinguish two real games, identify the exact counterpart first. Use `MATCH_SOURCE_ASSERTION` only after the identity is established.

## 15. Validation and no-op gate

After all approved reconciliation:

```bash
python tools/validate_data.py
python tools/ingest_school.py "$school_key" --check-package
git status --short
```

`--check-package` makes drift between the target's `source-games.csv` and the assertion generated from that same source row fatal. It covers game date, curated site and venue, normalized city/state, event text, and preserved `raw_text`. Ordinary validation summarizes known legacy drift as warnings so historical packages do not disable the repository-wide gate. The check never overwrites or compares another school's evidence.

The same target preflight validates `conferences.csv`. Unknown conference keys, invalid seasons, wrong program keys, and overlapping intervals block ingestion. A newly encountered historical identity requires owner approval and a central registry entry before the package can publish.

Initial ingestion creates the global assertion deterministically from the source row. If a legacy school-level assertion mirror exists, ingestion appends missing target rows there too; it does not mass-rewrite pre-existing legacy drift.

The final target-school ingestion must report:

- all source rows as existing-game matches;
- `New canonical games: 0`;
- `Identity review required: 0`;
- `Canonical enrichments: 0 games / 0 fields`;
- `Assertions to add: 0`;
- `Discrepancies to add: 0`;
- `NO-OP`.

This no-op is the strongest routine proof that the six-file package, canonical games, evidence assertions, discrepancy layer, and safe enrichment behavior are synchronized.

The final target proof must also establish that source location preflight passes, public JSON contains no game with exactly one of `site_city`/`site_state`, and no venue or registry operation changed H/A/N.

The validator continues to enforce structural integrity across canonical games, evidence, reconciliation, program identities, conference membership, the central conference registry, and school historical intervals.

Known unrelated deferred cleanup is not itself a blocker to the target program. Keep unrelated work separate unless the current onboarding directly supplies evidence that resolves it.

## 16. Public-page enablement and deterministic site build

### Confirm the target's reference records

The reference layer already contains all 365 current Division I programs. Confirm the target row exists in both files:

```bash
grep -n "^${school_key}," data/reference/programs.csv
grep -n "^${school_key}," data/reference/conference-membership.csv
```

If the CSV has a legacy leading index column, use:

```bash
grep -n ",${school_key}," data/reference/programs.csv
grep -n ",${school_key}," data/reference/conference-membership.csv
```

Review the target's program metadata:

- `program_name`
- `display_name`
- `nickname`
- `city`
- `state`
- `primary_hex`
- `secondary_hex`
- `conference_regular_season_championships`
- `conference_tournament_championships`
- `final_four_appearances`
- `national_championships`
- `current_d1`
- `public_page_enabled`

The four achievement fields are required before a program may be published. Use nonnegative integers. `0` is a verified zero; blank means the value has not yet been populated and blocks public-page enablement.

Achievement definitions:

- conference regular-season championships include recognized outright and shared/co-championships across all conferences in the program's history;
- conference tournament championships include official conference-tournament titles across all conferences in the program's history;
- Final Four appearances are NCAA Tournament Final Four appearances;
- national championships are NCAA Tournament championships rather than retroactive or non-NCAA selectors.

Prefer the school's recognized historical totals. Escalate formally vacated championship/appearance cases for owner review rather than silently choosing a counting convention.

Confirm the `2026-2027` conference key/name. Correct a bad reference value only with a documented authoritative source.

### Enable the page

After canonical ingestion and validation, confirm that all four achievement fields are populated, then change only the target's `public_page_enabled` value from `No` to `Yes` in `data/reference/programs.csv`.

Run validation again:

```bash
python tools/validate_data.py
```

Validation should now confirm that the enabled program exists in canonical games and is a current Division I program.

### Dry-run the site build

```bash
python tools/build_site_data.py
```

The builder is deterministic and dry-run by default. Review:

- reference season;
- total programs;
- public pages;
- canonical games;
- team JSON file count;
- stale team files;
- per-program game and opponent totals.

For every onboarding, expect:

- public pages to increase by exactly one when one new program is enabled;
- team JSON files to increase by exactly one;
- a line for the target team;
- all previously public programs to retain their expected game/record totals except for explicitly reviewed reconciliation effects;
- `Stale team files: 0`, unless an intentional unpublish is part of the same change.

Stop if the dry run reports a missing opponent display name, a true cross-package display-name conflict, or an unexpected stale team file.

### Apply the site build

```bash
python tools/build_site_data.py --apply
```

The build writes:

- `site/data/manifest.json`
- `site/data/programs.json`
- `site/data/teams/<program_key>.json` for every enabled public program

It also removes stale `site/data/teams/*.json` files. This is why the stale-file count must be reviewed before `--apply`.

Expected completion text begins with:

```text
PASS: wrote ... deterministic JSON files under site/data/.
```

Rerun validation and review the generated diff:

```bash
python tools/validate_data.py
git diff --stat
python -m json.tool "site/data/teams/${school_key}.json" > /dev/null
sed -n '1,160p' "site/data/teams/${school_key}.json"
```

### Determinism check

Capture the generated diff, rebuild, and compare:

```bash
find site/data -type f -name '*.json' -print0 | sort -z | xargs -0 sha256sum > "/tmp/${school_key}-site-data-before.sha256"
python tools/build_site_data.py --apply
find site/data -type f -name '*.json' -print0 | sort -z | xargs -0 sha256sum > "/tmp/${school_key}-site-data-after.sha256"
cmp "/tmp/${school_key}-site-data-before.sha256" "/tmp/${school_key}-site-data-after.sha256"
```

Expected result: `cmp` prints nothing and exits successfully.

## 17. Website QA, commit, review, and deployment

### Target-page QA

Verify:

- target appears in the directory and search;
- team name, nickname, colors, city/state, and current conference are correct;
- conference regular-season championships, conference tournament championships, Final Four appearances, and national championships are correct;
- overall game count and on-court record reconcile to curated source rows;
- first and last covered seasons are correct;
- season-history totals reconcile;
- opponent count and series summaries reconcile;
- representative early, middle, and recent games are correct;
- home, away, neutral, and unknown-site examples display correctly;
- overtime displays correctly;
- NCAA, NIT, and conference-tournament tags/rounds display correctly;
- administrative actions do not replace on-court results;
- unknown dates and venues remain unknown rather than receiving invented precision;
- canonical opponent names render correctly;
- canonical venue names and locations render correctly;
- links to already-published opponents open the correct series/page.

Any aggregate-count change caused by identity reconciliation must be understood and explicitly approved.

### Local browser preview

The frontend is a static site rooted at `site/`. No npm, Vite, or other frontend build command is required.

Start the local preview with:

```bash
python -m http.server 8000 --directory site
```

Open the forwarded Codespaces port 8000 or the equivalent local URL.

Do **not** open `site/index.html` through `file://`; the frontend fetches JSON from `site/data/`.

Test both desktop and a narrow/mobile viewport.

### Existing-public-program smoke test

Routine data-only onboarding does **not** require a full retest of every previously published program.

Instead:

- review any existing public team JSON files changed by the site build and understand why they changed;
- visually open one or two representative affected existing programs;
- specifically inspect any older program whose canonical game was materially reconciled or enriched;
- confirm directory/search routing remains normal.

Perform a full existing-public-program regression only when:

- shared frontend code changed;
- the public JSON schema changed;
- site-builder behavior changed materially;
- broad identity cleanup touched many programs;
- broad venue/opponent normalization changed shared display behavior;
- the project owner requests it.

Generated changes to an existing team JSON file are acceptable when they result from:

- approved canonical reconciliation;
- safe matched-game enrichment;
- the new target becoming a public/linkable opponent;
- approved global identity cleanup;
- another explicitly reviewed cross-program improvement.

### Commit sequence

The six-file source package should normally already be committed separately on the onboarding branch.

If reconciliation legitimately corrected an older school's normalized source package or venue registry, stage those reviewed files explicitly as part of the publication commit.

Never use `git add -A` for onboarding.

Stage intended global/public outputs explicitly:

```bash
git status --short

git add data/canonical/games.csv
git add data/evidence/game-assertions.csv
git add data/reconciliation/discrepancies.csv
git add data/reference/programs.csv
git add site/data
```

Also explicitly stage any approved:

- older school `source-games.csv` correction;
- older school `opponents.csv` correction;
- `venues.csv` canonical-name/alias correction;
- `data/reference/conference-membership.csv` correction;
- generic `tools/build_site_data.py` improvement;
- generic `site/index.html` improvement.

Then inspect:

```bash
git --no-pager diff --cached --stat
git --no-pager diff --cached --name-only
git status --short
```

Run the CRLF-aware whitespace check from Section 8.

Confirm unrelated files remain unstaged.

Commit:

```bash
git commit -m "Ingest and publish ${school_key}"
```

### Final pre-push gate

```bash
python tools/validate_data.py
python tools/ingest_school.py "$school_key" --check-package
python tools/build_site_data.py
git status -sb
git --no-pager log -3 --oneline --decorate
```

Requirements:

- validator passes;
- target ingestion is a complete no-op;
- site dry run reports the expected public-page/team-JSON count;
- stale team files are zero unless explicitly intended;
- branch contains only intended commits;
- no uncommitted tracked onboarding changes remain.

Push:

```bash
git push -u origin "$branch_name"
```

### Pull request

Open a GitHub pull request into `main`.

The PR description must include:

- source coverage and cutoff;
- source-package row count;
- dry-run and apply counts;
- identity decisions;
- discrepancies added and their final dispositions;
- validation result;
- target no-op result;
- site-build counts;
- target-page QA result;
- existing-public-program regression result;
- known limitations;
- any cross-program identity or venue cleanup included.

Before merge:

```bash
gh pr checks <PR_NUMBER>
```

All required checks must pass and GitHub must report the PR mergeable.

Pull requests receive Vercel preview deployments. A successful PR preview is **not** the production-deployment verification.

### Production deployment — confirmed workflow

The production site is:

`https://college-basketball-history.vercel.app`

Vercel is connected directly to GitHub.

**Merging an approved PR to `main` automatically triggers a Vercel Production deployment.**

No manual `vercel` CLI command is part of the normal release procedure.

After merge, synchronize local `main`:

```bash
git fetch origin
git switch main
git pull --ff-only origin main
```

Capture the exact merged-main SHA:

```bash
SHA=$(git rev-parse HEAD)
REPO="pollackelliott/college-basketball-history"
echo "$SHA"
```

Query GitHub Deployments for that exact SHA:

```bash
gh api \
  --method GET \
  "repos/$REPO/deployments?sha=$SHA&per_page=20" \
  --jq '.[] | {
    id,
    environment,
    ref,
    sha,
    created_at,
    updated_at
  }'
```

For the Production deployment ID:

```bash
gh api \
  --method GET \
  "repos/$REPO/deployments/<DEPLOYMENT_ID>/statuses?per_page=10" \
  --jq '.[0] | {
    state,
    environment,
    environment_url,
    log_url,
    created_at,
    updated_at
  }'
```

Required result:

- `environment` is `Production`;
- deployment `sha` equals the merged `main` SHA;
- latest deployment `state` is `success`.

### Production QA

Verify the canonical production URL, not merely the PR-preview URL.

At minimum:

- target page loads;
- headline program metadata and record are correct;
- representative opponent and venue display names are correct;
- representative early/recent games render correctly;
- one or two representative previously public programs open successfully, including any existing program materially affected by reconciliation or enrichment.

Production JSON can also be checked directly at:

- `/data/manifest.json`
- `/data/programs.json`
- `/data/teams/<school_key>.json`

A release is not closed until both production data QA and production visual QA pass.

## 18. Rollback procedures

### Before a real apply

No rollback is needed; dry runs do not write. Delete or leave the isolated `/tmp` rehearsal copy as appropriate.

### After ingestion apply but before commit

Inspect status first:

```bash
git status --short
```

Restore only the generated global files changed by ingestion:

```bash
git restore -- data/canonical/games.csv
git restore -- data/evidence/game-assertions.csv
git restore -- data/reconciliation/discrepancies.csv
```

The separately committed six-file source package remains intact.

### After site build but before commit

Restore tracked site/reference outputs explicitly:

```bash
git restore -- data/reference/programs.csv
git restore -- data/reference/conference-membership.csv
git restore -- site/data/manifest.json
git restore -- site/data/programs.json
git restore -- site/data/teams
```

If the new target JSON is untracked, preserve it temporarily instead of deleting it blindly:

```bash
rollback_dir="$(mktemp -d "/tmp/cbb-${school_key}-rollback.XXXXXX")"
if [ -f "site/data/teams/${school_key}.json" ]; then mv "site/data/teams/${school_key}.json" "$rollback_dir/"; fi
printf 'Preserved rollback file in: %s\n' "$rollback_dir"
```

Then rerun `git status --short` and validation.

### After a local commit but before merge

Create a new revert commit; do not rewrite shared history if the branch has been pushed:

```bash
commit_sha="replace-with-the-commit-sha"
git revert "$commit_sha"
python tools/validate_data.py
git push
```

If both onboarding commits must be reverted, revert the later generated/publication commit first, then the earlier source-package commit.

### After merge or production deployment

- Revert the merged commit(s) through GitHub or `git revert` on a reviewed branch.
- Merge the revert through the normal review process.
- Allow the established production workflow to deploy the reverted `main`.
- Verify all previously public program pages and confirm the target is no longer public.
- Never use `git reset --hard` or force-push shared `main` as a rollback mechanism.

## 19. Production onboarding validation history

### Florida — seventh public program

**Completed:** August 10, 2026
**Result:** PASS

Florida established the first complete partner-ready onboarding path from six-file package through production.

Key results:

- 2,787 source games;
- 232 existing matches;
- 2,555 new canonical games;
- 0 identity-review cases;
- 10 discrepancies, all reviewed and resolved;
- final record 1,595-1,192;
- isolated rehearsal PASS;
- final ingestion NO-OP;
- deterministic site build PASS;
- production QA PASS.

### Tennessee — eighth public program / Partner-ready v2 validation

**Completed:** August 10, 2026
**Result:** PASS

Tennessee validated the faster routine path and the permanent matched-game enrichment behavior.

Key results:

- 2,952 source games;
- 478 existing matches;
- 2,474 new canonical games;
- 0 identity-review cases;
- 255 matched games safely enriched;
- 672 blank canonical fields filled;
- 22 discrepancies generated;
- 21 resolved;
- 1 genuine historical score conflict retained `UNDER_REVIEW`;
- final record 1,827-1,123-2;
- final ingestion NO-OP;
- deterministic site build PASS;
- production QA PASS.

### Partner-ready v2 conclusion

Routine onboarding now means:

1. build a trustworthy six-file package;
2. let ingestion identify matches, new games, enrichments, identity questions, and conflicts;
3. review only material identity ambiguity and discrepancies;
4. retain genuine unresolved historical conflicts transparently when appropriate;
5. prove the final no-op;
6. perform targeted site QA;
7. merge through a dedicated branch and pull request;
8. verify production.

Isolated rehearsal and full-public-program regression remain available safety tools, but they are no longer mandatory for every routine data-only onboarding.

## 20. Known deferred work after Tennessee

The following remain valid project work but do not block routine onboarding:

- A newly onboarded school improves only games involving that school; it does not comprehensively audit every older program's history.
- Existing public programs may still contain unsupported venue/location blanks that will be filled gradually as overlapping authoritative packages arrive or through dedicated cleanup.
- Exact venue/location remains intentionally blank where evidence is insufficient.
- Continue consolidating duplicate opponent and venue identities when new packages expose them.
- Historical `conferences.csv` files are validated and published as team-level interval metadata; they do not alter canonical games or current membership.
- A reusable `tools/validate_school_package.py` would improve structural package QA.
- A reusable human-readable discrepancy-report helper would reduce manual review work.
- A reusable six-file template reflecting the current field union would improve collaborator onboarding.
- Some older public programs may still merit focused venue/site audits independent of the normal new-school onboarding cycle.
- Florida retains a future venue-identity research question involving `Benchmark International Arena`; do not conflate it with another Tampa venue without evidence.

None of these items justifies delaying a new school whose own six-file package, ingestion, reconciliation, validation, no-op, and publication gates are clean.

## 21. Partner handoff checklist

Before a partner begins independently, confirm that the partner can answer “yes” to each item:

- [ ] I understand that one real game has one canonical row and source assertions are evidence about that game.
- [ ] I will preserve raw source evidence and document normalization decisions.
- [ ] I will curate through 2025-26 for the current expansion cycle.
- [ ] I will exclude exhibitions and will not invent games from aggregate totals.
- [ ] I will not infer home/away/neutral solely from venue or venue chronology.
- [ ] I understand that supported blank canonical metadata may be safely enriched on matched games, but populated conflicts become discrepancies.
- [ ] I will stop for ambiguous identities or uncertain game inclusion.
- [ ] I will create and use a dedicated onboarding branch before browser-uploading school files.
- [ ] I will build and QA the complete six-file school package before ingestion.
- [ ] I will commit the six-file package before global ingestion.
- [ ] I will dry-run ingestion before `--apply` and will not apply while identity review is nonzero.
- [ ] I understand that isolated rehearsal is conditional rather than mandatory for every routine school.
- [ ] I will review every generated discrepancy in human-readable form and escalate material canonical-value decisions.
- [ ] I understand that a genuine historical conflict may remain `UNDER_REVIEW` when publication with the flag is explicitly approved.
- [ ] I will require validation and a complete target-team no-op, including zero remaining canonical enrichments.
- [ ] I will verify the target's current conference row and populate all four achievement fields before publication.
- [ ] I will verify every historical conference key exists in the central registry and stop for owner approval rather than inventing a tournament abbreviation.
- [ ] I will keep historically distinct conference naming eras separate when their public tournament identities differ.
- [ ] I will preserve existing CSV BOM/newline style when modifying tracked CSV files.
- [ ] I will dry-run the site build before applying it and verify deterministic output.
- [ ] I will perform detailed target-page QA and a light affected-existing-program smoke test for routine data-only onboarding.
- [ ] I will run a full public-program regression when shared frontend/schema/builder behavior or broad shared data changes warrant it.
- [ ] I will stage files explicitly and will never use `git add -A` for onboarding.
- [ ] I will push the onboarding branch, open a pull request with base `main`, verify checks, and merge through the PR.
- [ ] I will synchronize local `main` after merge and rerun validation, target no-op, and site dry run.
- [ ] I will verify the Vercel production deployment and production page before declaring the school closed.
- [ ] I will never use the obsolete rebase block or `origin/ma`.
- [ ] I will never force-push or reset shared `main` to undo an onboarding.

## Appendix A. Global output contracts

### Canonical games

`data/canonical/games.csv` contains one row per real game. Current required fields include:

- `canonical_game_id`
- `season_label`
- `game_date`
- `date_precision`
- `team_a_key`
- `team_b_key`
- `team_a_score`
- `team_b_score`
- `result_winner_team_key`
- `overtime_periods`
- `site_type`
- `designated_home_team_key`
- `venue_key`
- `site_city`
- `site_state`
- `game_type`
- `postseason_round`
- `administrative_status`
- `administrative_note`
- `canonical_status`
- `notes`

Team keys are alphabetical, not home/away oriented. Canonical IDs are permanent and are not derived from mutable facts.

### Evidence

`data/evidence/game-assertions.csv` links each source row to its canonical game and adds:

- `assertion_id`
- `canonical_game_id`
- `match_status`
- `match_method`

The source identity pair `(source_program_key, source_game_id)` must be unique.

### Reconciliation

`data/reconciliation/discrepancies.csv` preserves:

- `discrepancy_id`
- `canonical_game_id`
- `field_name`
- source program/value pairs
- `canonical_value`
- `status`
- `resolution_basis`
- `notes`

The existence of a discrepancy is not itself an error. Unexplained or incorrectly resolved discrepancies are errors.

## Appendix B. Run record template

Copy this section into the onboarding PR description or a separate checkpoint note.

```text
Program:
School key:
Coverage cutoff:
Branch:
Source-package commit:

Primary sources:
Supplemental sources:

source-games rows:
opponents rows:
venues rows:
conferences rows:

First dry run:
  Source rows:
  Existing-game matches:
  New canonical games:
  Identity review required:
  Assertions to add:
  Discrepancies to add:

Identity decisions / overrides:

Isolated apply result:
Isolated second-run NO-OP result:

Real apply result:
Discrepancies resolved:
Discrepancies left under review:

Validator result:
Target-school NO-OP result:

Site-build dry run:
  Reference season:
  Programs:
  Public pages:
  Canonical games:
  Team JSON files:
  Stale team files:

Target-page QA:
Existing-public-program regression QA:
Mobile QA:

PR:
Merge commit:
Deployment:
Production QA:

Runbook corrections discovered:
Open follow-up items:
```
