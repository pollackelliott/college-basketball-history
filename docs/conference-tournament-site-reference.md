# Conference Tournament Site Shared Reference

- **Status:** Owner-authorized shared Research reference
- **Applies to:** Stage 3B conference-tournament site research
- **Normalized snapshot:** `data/reference/conference-tournament-sites.csv.gz.b64`
- **Coverage ledger:** `data/reference/conference-tournament-site-coverage.csv`
- **Source metadata:** `data/reference/conference-tournament-sites.meta.json`
- **Tool:** `tools/conference_tournament_reference.py`

## Purpose and authority

The owner maintains the source Excel workbook. The repository stores a deterministic normalized
snapshot plus the exact SHA-256 of the workbook version that produced it. This prevents an opaque
binary workbook from becoming the runtime interface while preserving auditable source identity.

A `reference_status=COMPLETE` row is **accepted owner-supplied shared project evidence** for the
physical venue / city / state represented by that row. A school Research lane normally does not
need to re-research that same conference-tournament site externally when the game is independently
established as a conference-tournament game, the season/conference and date/round boundaries match,
and no material contradictory authoritative evidence is present.

The reference establishes site facts only. It does **not** establish that a game is postseason and
does **not** infer H/A/N. Explicit contradictory institutional evidence must be surfaced rather
than overwritten.

`PARTIAL`, `UNCERTAIN`, and `UNRESOLVED` rows are not terminal exact-site answers. A blank or
uncertain reference entry means only that this shared reference does not answer the question; the
Stage 3B row remains subject to the normal research-to-exhaustion standard.

## Shared-site model

The source intentionally records centralized/shared tournament sites rather than one row per game.

- `Entire Tournament at Shared Venue? = Yes`: the row can cover the whole tournament after the
  tournament match is established.
- `... = No`: apply the shared venue only inside its `From`/`Through` date or round boundaries.
- Ordinary campus preliminary rounds are intentionally absent. Research those games at game level,
  normally using the host program's accepted home-venue chronology or other authoritative evidence.
- Tournaments that moved between shared venues use multiple rows; select the row covering the
  game's date/round.
- `Regular Home Venue for League Team?` and `Regular Home Program Key` are context/QA only and may
  never determine H/A/N by themselves.

## Conference keys

`conference_key` is the owner's reference key. Many keys match `data/reference/conferences.csv`;
some historical naming-era keys are reference-local. A mismatch is not permission to guess.
Match conference lineage/name and season carefully. Add any future reusable crosswalk explicitly
rather than silently collapsing historical identities.

## Provenance and incompleteness

The normalized snapshot preserves source workbook row number, all site/boundary fields, notes, and
`Source URL` when present. `conference-tournament-site-coverage.csv` preserves the owner's separate
conference-level completeness checklist.

`reference_status` is derived mechanically:

- `COMPLETE` — exact venue + city/state present and shared-site scope is usable;
- `PARTIAL` — some site/scope information is present but not safe as a complete exact-site answer;
- `UNCERTAIN` — the source explicitly marks uncertainty/TBD;
- `UNRESOLVED` — no usable site answer is presently supplied.

## Stage 3B consumption order

For a confirmed conference-tournament game:

1. query the shared reference before opening external site research;
2. match season/conference, then date/round boundaries;
3. apply a matching `COMPLETE` row as accepted shared project evidence;
4. preserve source-row provenance in school Research artifacts/notes where practical;
5. for absent, `PARTIAL`, `UNCERTAIN`, `UNRESOLVED`, or contradicted rows, continue normal Stage 3B
   authoritative research to exhaustion;
6. never use this reference to infer game classification or H/A/N.

Example:

```bash
python tools/conference_tournament_reference.py --conference-key acc --season 2025-26
```

## Refresh workflow

You do **not** hand-edit the normalized reference. When the owner updates the workbook, supply the
new workbook and run:

```bash
python tools/conference_tournament_reference.py \
  --refresh-from-workbook /path/to/updated-owner-workbook.xlsm
python tools/conference_tournament_reference.py --check
python -m unittest tests.test_conference_tournament_reference
```

Review the narrow generated diff and merge the reference-update PR. The metadata records the exact
source filename and SHA-256 used for the snapshot, so every refresh is traceable to one workbook
version.
