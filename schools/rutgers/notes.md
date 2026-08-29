# Rutgers research portfolio notes

## Research freeze scope

- School: Rutgers
- School key: `rutgers`
- Research baseline: `ae823cae233ff287d3c3827c8dbd40ec2db09819`
- Owner history-scope ruling: always Division I/top-level for site purposes.
- `history_start_season`: `1906-1907`
- `history_scope_basis`: `ALWAYS_TOP_LEVEL_FROM_INCEPTION`
- Coverage: program inception through completed 2025-26 season.
- Competitive games in this package: 2,696.
- On-court/source record: 1,361-1,335.

## Major curation decisions

- The Rutgers all-time scoreboard is the backbone through 2024-25; official Rutgers season schedules are used to exclude two identified exhibitions and to repair material modern scoreboard defects; the official completed 2025-26 Rutgers schedule supplements it.
- `source_opponent_label` uses the media guide's all-time-series opponent heading when available; game-line spelling/ranking/site wording remains preserved verbatim in `raw_text`.
- The media-guide scoreboard prints some losing scores winner-first and some winning scores winner-second. Structured scores are oriented to Rutgers using the source W/L marker; `raw_text` remains unchanged. The official 2020-21 schedule corrects the guide's Minnesota (76-72), at Iowa (L 66-79), and Big Ten Tournament Indiana (61-50) entries.
- Overtime is re-derived from literal source notation (`OT`, `2OT`, `3OT`) rather than trusting parser artifacts.
- The 1975 NCAA loss to Louisville is curated as Rutgers 78, Louisville 91. The Rutgers guide's printed `91-87` is retained in `raw_text`; official NCAA bracket/game evidence supports 91-78.
- The 1986 Atlantic 10 tournament loss at West Virginia is dated 1986-02-27 using official Atlantic 10 / West Virginia tournament history; Rutgers' guide prints 3/3/86 and that wording is preserved.
- Rutgers' 1919-20 National AAU Tournament games are classified as generic `POSTSEASON`; the NYU loss is the verified championship game.
- Named regular-season events, including the 2025 Players Era Festival, remain `REGULAR_SEASON`. The 2026 College Basketball Crown game is `POSTSEASON`.
- The two source-record administrative outcomes (1908 Fordham default/forfeit win and 1973 Pittsburgh forfeit loss) retain blank scores because Rutgers supplies no completed-game score. The Pittsburgh row documents that Pitt led 36-21 when the game was stopped.

## Site and venue policy

- H/A/N is taken from Rutgers' all-time series table where a one-to-one game match is available; otherwise only explicit scoreboard `at` / `vs` signals are used. Remaining unsupported cases stay `UNKNOWN`.
- No site classification is inferred from city, building, opponent campus, or venue chronology.
- NCAA Tournament physical venue/city/state is complete for all 15 NCAA rows.
- The owner-supplied conference-tournament workbook is used only as affirmative Rutgers-specific evidence. Populated Big East/American/Big Ten entire-tournament shared-site rows are used; its blank older Atlantic 10 rows are treated as research gaps, not negative evidence or global canon.
- `VEN-999001` for Bryce Jordan Center is a research-time provisional numeric identity only. Implementation must rebase it against current main and allocate/reuse the authoritative current global venue ID.

## Honest unknowns

- Unknown exact dates: 21. These are retained blank rather than invented.
- Unknown played scores: 2. Both are administrative default/forfeit rows documented above.
- Unsupported H/A/N rows: 98. They remain `UNKNOWN`; geography was not used to force certainty.
- Older Atlantic 10/Eastern Eight tournament venues remain blank where game-specific physical-site evidence was not strong enough for assignment. This is a research limitation, not a claim that the sites are unknowable.

## Source-level closure

- Every source-game ID is stable, nonblank, and unique.
- Every source opponent label resolves through `opponents.csv`; unresolved opponent identities: 0.
- Every curated venue name resolves through `venues.csv`.
- Exhibitions are excluded. The 2022-10-30 Fairfield Team LeGrand Exhibition and 2024-10-17 St. John's exhibition appear in the media-guide chronological ledger but are explicitly identified as exhibitions by Rutgers' official season schedules and are omitted from `source-games.csv`. The separate 2024 Knighthood Showcase scrimmage is likewise not included.
- Numeric venue IDs created during this parallel research lane are provisional until Implementation performs the mandatory current-main shared-reference rebase.

## Current-main integration normalization

Implementation preserved the immutable RESEARCH_FROZEN transport artifact. Before
Phase 0 staging, the integration-prep copy normalized Bryce Jordan Center geography
from `University Park, PA` to the project's already-established `State College, PA`
display geography so Rutgers can reuse current global physical venue identity
`VEN-000303`. This is a current-main shared-reference normalization, not a new
historical or H/A/N ruling.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=b8c84717fa6434610c43c8e1a49bc6d634870e0a` from `research_base_sha=ae823cae233ff287d3c3827c8dbd40ec2db09819`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
