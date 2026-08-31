# Published site-completeness census

`tools/published_site_completeness_census.py` is the permanent read-only scoreboard for physical game-site debt on published program pages.

It does **not** mutate canonical games, source assertions, reconciliation records, venue registries, school portfolios, or generated site data.

## Public-game denominator

The census derives the published universe from `data/reference/programs.csv`:

- `public_page_enabled=yes`
- each program's owner-approved `history_start_season`
- the union of canonical games that are in scope for at least one published program

A canonical game is counted once in global totals even when both participants have published pages. Per-team sections intentionally count the game once from each published program perspective.

## HOME

For a published program's HOME games the census reports:

- total HOME games
- missing venue
- missing complete city/state
- missing either
- completely blank physical site
- hard blockers
- validated `RESEARCHED_UNRESOLVED_HOME_VENUE` historical exceptions
- invalid exception markers

The hard-blocker/exception partition is taken from `implementation_site_gate.py`, not reimplemented independently. The census fails rather than publish a contradictory HOME ledger if canonical HOME gaps do not equal hard blockers plus validated historical exceptions.

## Postseason

The census reports unique canonical-game totals and physical-site gaps for:

- all postseason
- NCAA Tournament
- conference tournament
- NIT
- other generic `POSTSEASON`

Each group is split into missing venue, missing location, missing either, and completely blank.

## Neutral

The census reports the same site-gap fields for:

- all neutral games
- regular-season neutral games
- neutral postseason games
- published-vs-published neutral games

`published-vs-published` requires both programs to be published and the game to fall inside both approved history scopes.

## Breakdowns

The machine-readable report includes:

- by team
- by decade
- by canonical game type
- conference-tournament gap groups by season plus any `event_or_tournament` labels available in source assertions

The event grouping is intended to turn many game rows into a smaller number of research tasks when a tournament used one shared site.

## Conference Tournament Site Reference workbook

The owner-maintained Conference Tournament Site Reference is a **research/remediation accelerator, not the census denominator and not a universally complete canonical source**.

Its safety rules remain:

- one row represents one shared/centralized tournament venue, not every tournament game
- ordinary campus preliminary-round sites remain game-level/host-program evidence
- the workbook supplies physical venue/city/state only; it never infers H/A/N
- mid-tournament shared-site moves require explicit date/round boundaries
- historical gaps remain gaps until researched; absence from the workbook never means that no tournament or site existed

A conference section may be used canonically for a specific school only when the owner has explicitly authorized that section as complete for that school's conference-membership history. Otherwise it remains supporting research evidence.

## Usage

Text summary:

```bash
python tools/published_site_completeness_census.py
```

Full machine-readable ledger:

```bash
python tools/published_site_completeness_census.py --json
```

The first project-wide run on a newly established baseline should be preserved in review/PR output so remediation progress can be measured against an exact denominator rather than approximate search counts.
