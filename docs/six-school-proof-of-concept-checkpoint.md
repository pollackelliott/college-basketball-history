# Six-School Proof-of-Concept Checkpoint

**Date:** August 8, 2026  
**Repository state:** through commit `f196b50` (`Ingest and reconcile Kentucky`)

## Status

The initial six-school proof of concept is complete.

Completed programs:

- Missouri
- Arkansas
- Illinois
- Northwestern
- Kansas
- Kentucky

Current global dataset:

- **17,625 canonical games**
- **18,388 source assertions**
- **66 discrepancy records**
- **Validator: PASS**

Each completed school is fully represented in the global canonical/evidence/reconciliation layers, and repeated ingestion is idempotent: rerunning an already-ingested school produces no new games, assertions, or discrepancies.

## What the proof of concept established

The central data model is working as intended:

> **The canonical game is the product; everything else is evidence.**

One actual contest receives one canonical game row, even when multiple school sources describe it. School source rows remain preserved as assertions linked to that canonical game, while disagreements are retained in the reconciliation layer rather than discarded.

The six-school batch has successfully exercised the architecture against:

- overlapping school histories;
- duplicate-game prevention across independently sourced programs;
- conflicting dates and scores;
- source-specific errors;
- exact and uncertain dates;
- historical and defunct opponent identities;
- current D1 versus historical/non-D1 opponents;
- home, road, neutral, and unresolved site classifications;
- venue registries, aliases, chronology, and canonical venue keys;
- conference membership changes and historical conference naming;
- NCAA, NIT, and conference-tournament classification;
- historical postseason bracket normalization;
- conference championship games, including championship-game losses;
- vacated wins, vacated tournament appearances, forfeits, and other administrative outcomes while preserving on-court results;
- source discrepancies that can be resolved confidently;
- genuine unresolved conflicts that remain explicitly under review;
- safe re-ingestion with no duplication.

## School-centric and global layers

The repository now has a repeatable two-level structure.

Each school package contains curated source material:

```text
schools/<school>/
├── source-games.csv
├── opponents.csv
├── venues.csv
├── conferences.csv
├── notes.md
└── source-notes.md
```

The shared global layers contain:

```text
data/
├── canonical/games.csv
├── evidence/game-assertions.csv
└── reconciliation/discrepancies.csv
```

School files are curated source packages. The global canonical files are generated and reconciled outputs and should not be manually maintained as independent school datasets.

## Ingestion workflow

The established workflow for a new program is:

1. Build and QA the six-file school package.
2. Commit the school package.
3. Run:
   ```bash
   python tools/ingest_school.py <school>
   ```
4. Review the dry-run counts and any identity-review cases.
5. Apply:
   ```bash
   python tools/ingest_school.py <school> --apply
   ```
6. Resolve any finite, understood cross-source discrepancies.
7. Run:
   ```bash
   python tools/validate_data.py
   ```
8. Rerun the school ingestion and confirm a complete NO-OP.
9. Commit the generated global data files.

The ingestion tooling is deliberately conservative: ambiguous identities are surfaced for review rather than guessed.

## Important project rules confirmed during the POC

- Include every recognized **non-exhibition varsity game** in a current D1 program's history.
- Exhibitions do not appear in the public product and do not count in totals.
- Historical/non-D1 opponents remain valid canonical opponents and count in records.
- Public records default to **on-court results**; administrative actions are stored separately.
- Site is game-specific and is not inferred solely from venue.
- Venue chronology may support a site decision but does not dictate one.
- Public postseason tags are limited to:
  - `CONFERENCE_TOURNAMENT`
  - `NIT`
  - `NCAA_TOURNAMENT`
- Every conference-tournament title game receives `postseason_round = Championship`, whether the school won or lost.
- Every NIT title game receives `postseason_round = Championship`, whether the school won or lost.
- NCAA rounds use normalized competitive stages:
  - `Play-in`
  - `R64`
  - `R32`
  - `Sweet Sixteen`
  - `Elite Eight`
  - `Final Four`
  - `Championship`
- Historical consolation or third-place postseason games retain the tournament type but have a blank canonical round.
- Aggregate school records and series summaries are QA evidence, not canonical truth.

## Reconciliation philosophy

A discrepancy record does **not** necessarily represent an unresolved error.

Resolved discrepancies remain in the reconciliation layer to preserve the provenance of conflicting source claims and the basis for the canonical decision. Genuine uncertainty remains unresolved rather than being silently forced into a single answer.

The six-school POC therefore demonstrates not just data accumulation, but a durable audit trail.

## Notable historical edge cases successfully handled

Examples include:

- Missouri's vacated 2013-14 wins while preserving its on-court record.
- Illinois's 1976-77 Minnesota administrative forfeits while preserving the played scores/results.
- Kansas's 2017-18 vacated wins and NCAA appearance while retaining all games actually played.
- Kentucky's 1988 NCAA Tournament games, which were restored to the project because they were played even though Kentucky's official aggregate excludes them after NCAA sanctions.
- Kentucky's stripped 1988 SEC titles without treating the underlying tournament games as forfeits.
- Historical date and venue disagreements that remain preserved when the evidence does not justify a forced resolution.

## Next phase

Do **not** add school #7 immediately.

The six-school batch has served its intended purpose: prove the canonical/evidence/reconciliation architecture and expose tooling weaknesses before scaling.

The next phase should focus on preparing for conference-scale ingestion, including:

- reviewing the schema and documentation for anything learned during the six-school POC;
- tightening validation around fields that are now known to matter at scale;
- confirming the repeatable research/package/ingestion workflow;
- deciding the first conference-sized production batch;
- separating finite historical-research tasks from information directly extractable from official game-by-game sources;
- planning how opponent/program identity, conference history, venue history, and postseason metadata will scale across all 365 current Division I programs.

The goal of the next phase is not to redesign the working core. It is to make the proven workflow efficient and safe enough to repeat hundreds of times.
