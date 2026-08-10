# New Team Onboarding Runbook

**Project:** College Basketball History

**Document status:** Detailed draft for the seventh-team acceptance test

**Draft date:** August 10, 2026

**Repository:** `/workspaces/college-basketball-history`

**Public site:** <https://college-basketball-history.vercel.app>

> This draft is operationally usable, but it is not yet approved for completely unsupervised partner use. Run it once from beginning to end with the seventh team, record every deviation, close the acceptance-test items in Section 19, and then promote it to “Partner-ready.”

## 1. Purpose

This runbook explains how to add one current Division I men's basketball program to the project without duplicating games, losing source evidence, silently overwriting conflicts, or breaking the six existing public program pages.

The complete workflow is:

1. Select the program and define its coverage cutoff.
2. Gather authoritative source material.
3. Build and QA the six-file school package.
4. Commit the source package on a dedicated branch.
5. Dry-run ingestion and resolve identity questions.
6. Rehearse the apply in an isolated copy.
7. Apply ingestion on the working branch.
8. Review and resolve discrepancies.
9. Validate and prove a target-school no-op.
10. Enable the public page.
11. Build deterministic website data.
12. QA the new program and the six-program regression set.
13. Commit, push, review, merge, deploy, and verify production.

## 2. Core data principle

**One actual basketball game exists exactly once in the canonical database. Everything else is evidence about that game.**

A game reported by both Florida and Missouri is not two canonical games. It is:

- one row in `data/canonical/games.csv`;
- one Florida source assertion;
- one Missouri source assertion; and
- zero or more reconciliation records if the sources disagree.

School packages are curated inputs. The global canonical, evidence, reconciliation, and website files are shared outputs. Do not maintain a separate hand-edited public team page.

## 3. Current project rules

These rules were established during the six-school proof of concept and are binding unless the project owner explicitly changes them.

- Include every recognized non-exhibition varsity game in the program's history.
- Exclude exhibitions from canonical games and all public totals.
- Historical, defunct, club, military, and non-Division I opponents remain valid opponents and count in records when the contests were recognized varsity games.
- Public records use the on-court result. Forfeits, vacated games, vacated wins, and similar administrative actions are stored separately.
- Never infer home/away/neutral solely from the venue.
- Venue chronology is evidence, not an automatic site rule.
- Preserve source assertions even when another source establishes a different canonical value.
- Keep resolved discrepancies as provenance. Resolution does not mean deletion.
- Do not invent an exact date, venue, opponent identity, or site classification when the evidence is insufficient.
- Aggregate season records and opponent-series summaries are QA evidence, not canonical truth.
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
- Reviews any step marked **OWNER REVIEW REQUIRED** in this draft.

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
| `venues.csv` | Venue registry, aliases, chronology, and evidence | `tools/ingest_school.py`; `tools/backfill_venue_keys.py` |
| `conferences.csv` | Program's historical conference timeline | No current importer; curated/documentary |
| `notes.md` | Final curation decisions, exceptions, known issues, closure status | No current importer; curated/documentary |
| `source-notes.md` | Source hierarchy, coverage, citations, extraction notes, and source limitations | No current importer; curated/documentary |

Important consequences:

- A complete six-file package is required even though only three files are read by current tools.
- `conferences.csv` does not automatically update `data/reference/conference-membership.csv`.
- `notes.md` and `source-notes.md` must be reviewed as part of the package; validation does not prove they are complete.
- Ingestion automatically compares date, score, result winner, overtime, site type, game type, and postseason round on matched games. It does **not** currently detect every possible venue improvement or automatically fill every blank canonical value.

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
| `city` | Optional | Game site city supported by evidence. |
| `state` | Optional | Two-letter state/territory abbreviation where applicable. |

Site and venue answer different questions. A neutral game can occur in a team's usual home arena, and a program-designated home game can occur away from its campus.

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

Current limitation: this file is not imported automatically. The public site's current conference comes from `data/reference/conference-membership.csv`, whose current snapshot is `2026-2027`. Confirm the target already has the correct reference row.

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

Review exactly what will be committed:

```bash
git status --short
git diff --check
git add "schools/$school_key"
git diff --cached --stat
git diff --cached --check
git commit -m "Add ${school_key} source package"
```

Confirm the commit contains all six files:

```bash
git show --stat --oneline HEAD
git ls-tree -r --name-only HEAD "schools/$school_key"
```

Expected result: exactly the six required filenames, with no unrelated changes.

## 11. Ingestion dry run and identity review

Run the default dry run:

```bash
python tools/ingest_school.py "$school_key"
git status -sb
```

The dry run changes nothing. Review these counts:

- `Source rows`
- `Existing-game matches`
- `New canonical games`
- `Identity review required`
- `Assertions to add`
- `Discrepancies to add`

The identity counts must satisfy:

```text
Existing-game matches + New canonical games + Identity review required = Source rows
```

For a first ingestion:

- `Source rows` must equal the number of competitive rows in the package.
- `Assertions to add` will normally equal `Source rows`.
- Existing matches should primarily be games already represented through one of the six curated programs.
- New games should represent the rest of the target's history.
- Any unexpectedly large or small count is a stop signal.

### If identity review is required

The script stops all writes when even one identity requires review. Inspect each printed row.

Common causes:

- multiple games against the same opponent in one season;
- incomplete or conflicting date/score information;
- a possible duplicate already represented by another source;
- missing source identity fields;
- an invalid identity override;
- one source assertion linked to multiple canonical games.

Resolve the underlying research question first. Then, only when justified, use `FORCE_NEW` or `MATCH_SOURCE_ASSERTION` as described in Section 7.1. Rerun the dry run until `Identity review required: 0`.

## 12. Isolated apply rehearsal

Perform this rehearsal before the first real apply for every new program. It applies only inside a temporary copy made from the committed branch.

```bash
audit_dir="$(mktemp -d "/tmp/cbb-${school_key}-audit.XXXXXX")"
git archive HEAD | tar -x -C "$audit_dir"
python "$audit_dir/tools/ingest_school.py" "$school_key" --repo "$audit_dir"
python "$audit_dir/tools/ingest_school.py" "$school_key" --apply --repo "$audit_dir"
python "$audit_dir/tools/validate_data.py" "$audit_dir"
printf 'Temporary audit copy: %s\n' "$audit_dir"
```

Capture the exact proposed global changes without flooding the terminal:

```bash
diff -u data/canonical/games.csv "$audit_dir/data/canonical/games.csv" > "/tmp/${school_key}-canonical.diff" || true
diff -u data/evidence/game-assertions.csv "$audit_dir/data/evidence/game-assertions.csv" > "/tmp/${school_key}-assertions.diff" || true
diff -u data/reconciliation/discrepancies.csv "$audit_dir/data/reconciliation/discrepancies.csv" > "/tmp/${school_key}-discrepancies.diff" || true
wc -l "/tmp/${school_key}-canonical.diff" "/tmp/${school_key}-assertions.diff" "/tmp/${school_key}-discrepancies.diff"
sed -n '1,160p' "/tmp/${school_key}-canonical.diff"
sed -n '1,160p' "/tmp/${school_key}-discrepancies.diff"
```

Review the complete saved diffs when the first 160 lines are not sufficient. The assertion diff can legitimately be large because the first ingestion appends one evidence row per source game.

Then prove deduplication inside the already-updated copy:

```bash
python "$audit_dir/tools/ingest_school.py" "$school_key" --repo "$audit_dir"
```

Expected result:

- validation passes;
- second ingestion reports zero new games, assertions, and discrepancies;
- output includes `NO-OP`.

Do not continue if the isolated second run is not a no-op.

## 13. Apply on the working branch

After the dry-run counts and isolated diffs are approved:

```bash
python tools/ingest_school.py "$school_key" --apply
git status --short
```

The script writes only these global layers:

- `data/canonical/games.csv`
- `data/evidence/game-assertions.csv`
- `data/reconciliation/discrepancies.csv`

It also runs `tools/validate_data.py` after writing. A successful apply must end with post-write validation passing.

Review the changes before reconciliation:

```bash
git diff --stat
git diff --check
git diff -- data/reconciliation/discrepancies.csv
```

Do not infer success merely from row counts. Inspect representative early, middle, recent, postseason, neutral-site, overtime, and overlap games.

## 14. Reconciliation

### What automatic ingestion does

- Matches a source row against canonical games using the alphabetically ordered team pair and season.
- Uses date and score evidence conservatively to identify a game.
- Creates a new canonical game only when no same-season team-pair candidate exists or an approved `FORCE_NEW` applies.
- Preserves permanent canonical game IDs.
- Adds a source assertion.
- Creates an `UNDER_REVIEW` discrepancy for material disagreements on:
  - game date;
  - score;
  - result winner;
  - overtime periods;
  - site type;
  - game type;
  - postseason round.
- Does not silently overwrite the canonical value.

### What automatic ingestion does not guarantee

- It does not comprehensively audit an existing program's entire site/home/venue history.
- A new school cross-checks only games involving that school.
- Blank source values do not create discrepancies against known canonical values.
- Venue improvements are not all surfaced automatically.
- `conferences.csv` is not imported.
- There is no generic, fully documented reconciliation command for every conflict type yet.

### Resolution rules

1. Preserve the raw assertion unless the normalized field is demonstrably a curation error rather than what the source said.
2. Prefer contemporaneous official game records or box scores when later summary tables contain an apparent typo.
3. Use explicit game-level site evidence over a venue-based default.
4. Do not force a resolution when two credible sources remain in genuine conflict.
5. For a resolved discrepancy, retain:
   - competing value(s);
   - canonical value;
   - `RESOLVED` status;
   - evidence-based `resolution_basis`;
   - a clear note.
6. For genuine uncertainty, retain `UNDER_REVIEW` and do not invent a canonical correction.
7. If an already-ingested source row's normalized value was wrong, update the school source row and its evidence assertion consistently, while preserving raw source text and prior reconciliation history.

### Examples

#### Source score typo

If a later guide says 51-63 but contemporary official box scores establish 57-63:

- retain the guide's raw assertion;
- keep 57-63 canonical;
- record the conflict and evidence;
- mark the discrepancy resolved.

#### Source/result internal conflict

If the source row says `L 77-70`, its result and score conflict internally. Do not silently reinterpret both fields. Preserve the raw assertion, establish the canonical score/result from stronger evidence, and document the resolution.

#### Site versus venue chronology

If the venue chronology suggests the target's home arena but explicit source text says `at Opponent`, treat the explicit game evidence as stronger. A home-arena relationship is not dispositive.

#### Overtime normalization error

If raw text contains `(OT)` but the normalized overtime field is `0`, correct the normalized source field before creating a redundant under-review discrepancy. Preserve the raw text.

#### Same-season repeated opponent

If the matcher cannot distinguish two real games, use a cross-source assertion only after identifying the exact counterpart. `MATCH_SOURCE_ASSERTION` is preferable to embedding a canonical ID in the package.

### Draft limitation — owner review required

Until the seventh-team acceptance test establishes a generic reconciliation procedure, every canonical-value change after ingestion requires project-owner review. Use an existing reviewed resolver pattern or a narrowly scoped, auditable patch; never perform broad manual rewrites of global CSV files.

## 15. Validation and no-op gate

After all approved resolutions:

```bash
python tools/validate_data.py
python tools/ingest_school.py "$school_key"
git status --short
```

The target-school ingestion must report:

- all source rows as existing-game matches;
- `New canonical games: 0`;
- `Identity review required: 0`;
- `Assertions to add: 0`;
- `Discrepancies to add: 0`;
- `NO-OP`.

The validator currently checks, among other things:

- required columns;
- stable, unique canonical IDs;
- alphabetically ordered and distinct team keys;
- allowed site, game, postseason, canonical-status, and administrative-status values;
- score/winner consistency;
- home-team/site consistency;
- unique assertion IDs and source identity pairs;
- valid canonical references from evidence and discrepancies;
- unique program keys;
- required program names and Yes/No flags;
- current-D1/public-page constraints;
- valid conference-membership rows;
- one `2026-2027` conference row for every current Division I program.

### Known baseline caveat

At the August 10, 2026 `f9badd8` checkpoint, validation passes with 17,625 canonical games, 18,388 source assertions, 67 discrepancies, 365 reference programs, and 365 conference rows. A Missouri dry run proposes four known normalization-related discrepancy candidates. Do not apply those four blindly. They are a deferred Missouri cleanup item, not a blocker to proving the seventh team's own no-op.

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
- `current_d1`
- `public_page_enabled`

Confirm the `2026-2027` conference key/name. Correct a bad reference value only with a documented authoritative source.

### Enable the page

After canonical ingestion and validation, change only the target's `public_page_enabled` value from `No` to `Yes` in `data/reference/programs.csv`.

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

For the seventh team, expect:

- public pages to increase from 6 to 7;
- team JSON files to increase from 6 to 7;
- a line for the target team;
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
git diff --check
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

### Data-level QA for the target page

- [ ] Target appears in the directory and search.
- [ ] Team name, nickname, colors, city/state, and current conference are correct.
- [ ] Overall game count and on-court record reconcile to the curated source rows.
- [ ] First and last seasons are correct.
- [ ] Season history totals reconcile.
- [ ] Opponent count and series summaries reconcile.
- [ ] A sample of early, middle, and recent games is correct.
- [ ] Home, away, neutral, and unknown-site examples display correctly.
- [ ] Overtime displays correctly.
- [ ] NCAA, NIT, and conference-tournament tags/rounds display correctly.
- [ ] Administrative actions do not replace on-court results.
- [ ] Unknown dates and venues display without invented precision.
- [ ] Links to already-published opponents open the correct series/page.

### Six-program regression set

Retest all existing public programs:

- Arkansas
- Illinois
- Kansas
- Kentucky
- Missouri
- Northwestern

For each, verify:

- [ ] page loads;
- [ ] directory and search route correctly;
- [ ] filters and pagination work;
- [ ] opponent series opens;
- [ ] matchup history renders;
- [ ] no unexplained record/count change occurred;
- [ ] desktop and narrow/mobile layouts remain usable.

Review generated changes to existing team JSON files. Overlap-driven changes are acceptable only when they correspond to an approved canonical reconciliation.

### Commit sequence

The source package should already be committed separately. Stage only reviewed generated, reconciliation, reference, and site files:

```bash
git status --short
git diff --check
git add data/canonical/games.csv
git add data/evidence/game-assertions.csv
git add data/reconciliation/discrepancies.csv
git add data/reference/programs.csv
git add site/data
git diff --cached --stat
git diff --cached --check
git commit -m "Ingest and publish ${school_key}"
```

If an approved current-conference correction was required, stage `data/reference/conference-membership.csv` explicitly before the commit. Otherwise leave it untouched. Do not stage unrelated files.

Final pre-push gate:

```bash
python tools/validate_data.py
python tools/ingest_school.py "$school_key"
python tools/build_site_data.py
git status -sb
git log -3 --oneline --decorate
```

Requirements:

- validator passes;
- target ingestion is a no-op;
- site dry run reports the expected seven pages/files and zero unexpected stale files;
- branch contains only intended commits;
- no uncommitted tracked changes remain.

Push the branch:

```bash
git push -u origin "$branch_name"
```

Open a GitHub pull request. The PR description must include:

- source coverage and cutoff;
- source package row count;
- dry-run and apply counts;
- identity overrides, if any;
- discrepancies added/resolved/left under review;
- validation result;
- no-op result;
- site-build counts;
- target-page QA result;
- six-program regression result;
- any known limitations.

### Deployment

The protected public checkpoint is hosted by Vercel at <https://college-basketball-history.vercel.app> and is associated with `main`. Merge only after PR approval and all gates pass.

**Seventh-team acceptance-test item:** confirm and document the exact deployment trigger. The recovered repository artifacts do not establish whether production is triggered automatically by merging `main` or by a separate manual action. Do not invent or guess a `vercel` command. During team seven:

1. Merge the approved PR.
2. Observe the established Vercel project/deployment workflow.
3. Record the exact trigger, expected status, and rollback control here.
4. Verify the production URL on desktop and a narrow viewport.

Production verification must repeat the target-page checklist and at least one smoke test for every existing program.

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
- Verify the prior six-program site and confirm the target is no longer public.
- Never use `git reset --hard` or force-push shared `main` as a rollback mechanism.

## 19. Seventh-team acceptance test

Use this runbook exactly as written for team seven. Maintain a short run record with command outputs and decisions.

The runbook becomes partner-ready only after all of these are true:

- [ ] A seventh team is built as a complete six-file package.
- [ ] The structural check catches no unresolved errors.
- [ ] Identity review reaches zero without guessing.
- [ ] Isolated apply validates and re-ingests as a no-op.
- [ ] Real apply validates.
- [ ] Every discrepancy has an explicit disposition.
- [ ] The seventh team re-ingests as a complete no-op.
- [ ] Public-page enablement and site build produce seven team files.
- [ ] Target data totals and representative games pass QA.
- [ ] The six-program regression set passes.
- [ ] The exact local preview procedure is documented.
- [ ] The exact Vercel deployment trigger/status procedure is documented.
- [ ] Production QA passes.
- [ ] Rollback is understood and, where safe, rehearsed before production.
- [ ] Any command or field-contract difference discovered during team seven is incorporated here.

### Gaps to close during the acceptance test

1. Decide whether the temporary structural checker should become `tools/validate_school_package.py`.
2. Establish a reusable template containing the current union of optional source-game fields, including administrative and identity-override fields.
3. Document a generic, reviewed reconciliation method instead of relying on school-specific resolver scripts.
4. Decide whether historical `conferences.csv` rows need an importer or remain intentionally documentary.
5. Capture the exact local site-preview command for the current frontend.
6. Capture the exact Vercel deployment and rollback workflow.
7. Record whether the seventh team exposes venue improvements that ingestion does not automatically flag.

## 20. Known deferred work that is not a team-seven blocker

- Missouri appears to have inflated home-game counts and needs a focused site/venue audit.
- Future opponent packages will cross-check only their games against Missouri; they will not automatically audit Missouri's entire history.
- Four Missouri normalization-related discrepancy candidates were identified during the readiness audit and should not be blindly applied.
- Exact venues remain intentionally blank when evidence supports only a city or site classification.

These items must remain visible in project tracking, but they do not prevent beginning the seventh-team acceptance test.

## 21. Partner handoff checklist

Before a partner begins independently, confirm that the partner can answer “yes” to each item:

- [ ] I understand that one real game has one canonical row.
- [ ] I understand the difference between source assertions and canonical facts.
- [ ] I will preserve raw evidence and document normalization.
- [ ] I will exclude exhibitions.
- [ ] I will not infer site solely from venue.
- [ ] I will not use aggregate totals to invent games.
- [ ] I will stop for ambiguous identities.
- [ ] I will use dry run before `--apply`.
- [ ] I will rehearse the first apply in an isolated copy.
- [ ] I will not apply when identity review is nonzero.
- [ ] I will review every generated discrepancy.
- [ ] I will require validation and a target-team no-op.
- [ ] I will enable the public page only after canonical QA.
- [ ] I will dry-run the site build before applying it.
- [ ] I will test the new team and all six regression programs.
- [ ] I will never run the obsolete rebase block or use `origin/ma`.
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

Copy this section into the team-seven PR description or a separate checkpoint note.

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
Six-program regression QA:
Mobile QA:

PR:
Merge commit:
Deployment:
Production QA:

Runbook corrections discovered:
Open follow-up items:
```
