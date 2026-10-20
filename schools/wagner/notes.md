# wagner research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: 80a481857b3b0bfcde22ec331f8bab30fbb5b2d1627ac0656cbc528d623c2453
- Research base SHA: 8944b0f07e7d1dc451d7975fa87ad03f534c2d2b
- Stage 3B status: COMPLETE
- Competitive games: 1,435
- Primary-source historical results cutoff: 2006-2007
- Required completed-season cutoff: 2025-2026
- Coverage cutoffs are explicit Research declarations; media-guide titles and filenames are not coverage inference rules.
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 68
- NCAA_TOURNAMENT: 3
- NIT: 5
- REGULAR_SEASON: 1,359

## Final H/A/N census

- NEUTRAL: 69
- OPPONENT_HOME: 721
- SOURCE_PROGRAM_HOME: 645


Stage 6 bounded approved-source preservation: 12 modern NEC road localities, 3 exact buildings already named by institutional records, global Hertz/Germain physical venue reuse; no historical game semantics changed. Stage 5 owner approval remains intact.


## Stage 1 current-main representation-only provenance

- Original immutable Wagner RESEARCH_FROZEN six-file ZIP SHA-256: `d4002be9de1e1236d828b4a9cf49cc229da874f410b048516f396307e8976aaf`.
- Protected-main comparison SHA: `d54b117e635c6c8558a962e5df2f32ba24073d7a`.
- This ZIP is an **integration representation candidate**, not a replacement Research Freeze.
- Only the eight listed `venues.csv` `venue_key` cells are reconciled with their already-registered current-main physical venues. Other venue-row fields and all competitive-game source evidence are unchanged. This documentation addendum is the only `notes.md` change.
- The original ZIP remains immutable; Stage 1 inventory and guarded staging still must pass.
- `wagner-sutter-spiro-gymnasium-staten-island` -> `spiro-sports-center` (VEN-000914)
- `casper-events-center-casper` -> `provisional-casper-events-center` (VEN-000469)
- `selland-arena-fresno` -> `selland-arena` (VEN-000374)
- `petersen-events-center-pittsburgh` -> `petersen-events-center` (VEN-000164)
- `orleans-arena-las-vegas` -> `orleans-arena` (VEN-000356)
- `leavey-center-santa-clara` -> `leavey-center` (VEN-000606)
- `madison-square-garden-new-york` -> `madison-square-garden-1968` (VEN-000124)
- `william-h-detrick-gymnasium-ccsu` -> `detrick-gymnasium` (VEN-000915)

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=d54b117e635c6c8558a962e5df2f32ba24073d7a` from `research_base_sha=8944b0f07e7d1dc451d7975fa87ad03f534c2d2b`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
