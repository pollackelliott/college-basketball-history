# Washington research notes

- Research base SHA: `6dc3910f68914c139097e9352481cb67a19cb2df`.
- Owner history scope: Washington is always top-level/D1 from inception for project purposes.
- Competitive universe through completed 2025-26: 3,217 games; on-court record 1,912-1,304-1. Exhibitions are excluded.
- The 2025-26 Washington record book chronological ledger omits 1950-51 through 1961-62. Those 327 games were reconstructed from Washington's opponent-series history and reconciled to season records.
- PCC `(H/PCC)` and `(A/PCC)` tags are treated as home/away, not neutral.
- 1961-62 contains a bounded source-internal site aggregate conflict: the individual California game tag is preserved rather than forcing the season aggregate.
- Administrative forfeits on 1976-01-17 Oregon State and 1995-01-07 California preserve the on-court losses/scores with separate FORFEIT metadata.
- Washington's chronological record book prints an erroneous 2009 NCAA Mississippi State score; contemporaneous Washington official evidence establishes Washington 71-58 Mississippi State, which is used here.
- Hec Edmundson Pavilion is treated as one physical building through naming changes. The 1999-2000 men's home season was displaced to KeyArena; the 2000-01 UTEP opener was also at KeyArena, with the renovated Pavilion reopening for the 2000-11-25 New Mexico State game.
- Pre-1927 home games retain Seattle, WA but do not receive a physical building where individual-game evidence is insufficient; they are explicitly `RESEARCHED_UNRESOLVED_HOME_VENUE`.
- Every NCAA Tournament game has a physical venue, city, and state.
- Non-NCAA neutral physical-building gaps are explicitly represented as researched site debt rather than inferred.
- Owner approved the complete NON_D1 sanity scan on 2026-09-02.
- All `provisional-*` venue keys are research-only and require current-main global reconciliation during implementation.

## Implementation compatibility derivative

- Immutable parent RESEARCH_FROZEN ZIP SHA-256: `b7dfb8e7b57e7ad0073753c3749865c9fedf630e7ecba2466b29530b0ea11627`.
- Parent research base SHA: `6dc3910f68914c139097e9352481cb67a19cb2df`.
- Compatibility derivative constructed against protected main `602b344e59ea5aeadee9439a36a3cb2a3acb2813`; the Codespace staging dry run remains authoritative if protected main advances.
- No games or opponents were added or removed, and no H/A/N classification, score, result, opponent identity, game type, or postseason classification was changed.
- `venues.csv` was migrated to the current repository schema and research-local provisional venue identities were reconciled to current physical-venue keys where deterministic. Cox Arena and Viejas Arena were collapsed to one physical venue based on San Diego State's official facility history.
- One source-game venue display was normalized from `University Arena (The Pit)` to current-main seed display `The Pit` to avoid amplifying an existing duplicate global representation; the parent label remains preserved by immutable parent provenance.
- The Forum's curated locality was normalized from Los Angeles shorthand to Inglewood, CA, matching the physical venue and current global geography.
- `conferences.csv` was migrated to the current repository schema. The current Big Ten interval is represented as ongoing/open-ended under repository convention.
- `northwest-intercollegiate` is supported by the frozen Washington conference history but is not yet registered in protected-main `data/reference/conferences.csv`; Implementation must register that historical shared reference before Phase 0 validation can be green.
- These are implementation/schema/current-main compatibility changes only; Washington's substantive historical research remains frozen.

## Implementation intake metadata repair

The first implementation-intake derivative used legacy research-status labels on all rows. Current protected-main tooling permits site-research metadata only on material site-gap rows and recognizes only `RESEARCHED_PARTIAL`, `RESEARCHED_UNRESOLVED`, and `RESEARCHED_UNRESOLVED_HOME_VENUE`.

This derivative therefore makes a metadata-only compatibility repair:
- `RESOLVED` and `NOT_REQUIRED_AWAY_REGULAR` status/basis metadata are cleared because those rows have no material site gap under the current gate.
- `RESEARCHED_UNRESOLVED_NEUTRAL_VENUE` is translated to `RESEARCHED_UNRESOLVED`.
- `RESEARCHED_UNRESOLVED_POSTSEASON_VENUE` is translated to `RESEARCHED_UNRESOLVED`.
- `RESEARCHED_UNRESOLVED_HOME_VENUE` is retained unchanged.

No game fact, site fact, opponent identity, result, score, date, venue assignment, conference interval, or research basis for a surviving material gap changed.

## Historical conference display-name verification

Washington's 2025-26 record book uses `Northwest Intercollegiate` in the year-by-year affiliation table and spells the historical organization out as `Northwest Intercollegiate Athletic Association (1911-15)` in the honor-roll section. The compatibility derivative therefore uses the full institutional-source name for the historical conference display identity while preserving the source shorthand in notes.


## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=602b344e59ea5aeadee9439a36a3cb2a3acb2813` from `research_base_sha=6dc3910f68914c139097e9352481cb67a19cb2df`. The historical Northwest Intercollegiate Athletic Association registry identity and safe display label were owner-approved on 2026-09-05. The authoritative final venue-ID mapping is recorded in `.onboarding/washington/integration-freeze.json`. Status: **INTEGRATION_FROZEN**.
