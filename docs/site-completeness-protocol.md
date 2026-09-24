# Site Completeness Protocol

## Purpose

This protocol prevents a school from appearing research-complete or publication-ready while large venue, location, or H/A/N gaps remain unnoticed.

The governing principles are:

> **UNKNOWN is preferable to unsupported certainty, but an unknown may not be silent.**

and, for a program's own home history:

> **A published program's home venue and location chronology is a publication requirement, except that an exhaustively researched physical venue identity may remain explicitly unresolved when the home city/state are known and the surviving record does not support a specific building.**

Most historical site facts may remain unresolved after reasonable research when the unresolved state is explicit. A school's own home venue/location is held to a stronger standard because the project deliberately researches each program's home-facility history before publication.

The detailed owner standard is recorded in `docs/site-completeness-owner-standard.md`. The narrow historical HOME venue exception is recorded in `docs/home-venue-research-unresolved-policy.md`.

## Research-lane responsibility

Before `RESEARCH_FROZEN`, the school portfolio must run the permanent `research-check` in `tools/onboarding_hardening.py`.

The site census covers at least:

- `SOURCE_PROGRAM_HOME` rows missing `curated_venue_name`;
- `SOURCE_PROGRAM_HOME` rows missing city/state;
- every `UNKNOWN` `curated_site_type` row;
- non-NCAA `NEUTRAL` rows missing venue and/or city/state;
- `CONFERENCE_TOURNAMENT`, `NIT`, and `POSTSEASON` rows missing venue and/or city/state;
- the same gaps summarized by season and decade so a historical chronology hole cannot hide inside aggregate H/A/N counts.

### Home rows

Every in-scope `SOURCE_PROGRAM_HOME` row must resolve to complete city/state geography
before `RESEARCH_FROZEN`. Exact physical venue identity is the expected result and
remains an active source-school research responsibility.

The lane must use documented facility chronology, predecessor buildings, transitions,
temporary sites, alternate sites, and game-level/reciprocal evidence before accepting a
blank venue.

For eras where authoritative institutional/facility evidence establishes the normal home
venue, use a **default-plus-exceptions** model: apply the supported venue across the exact
covered HOME population and research only rows with affirmative evidence of alternate,
temporary, off-campus, special-site, or contradictory treatment. Do not require an
individual box score merely to re-prove an already established normal home building.

A genuine historical safety valve remains available through
`RESEARCHED_UNRESOLVED_HOME_VENUE`. It is especially relevant to difficult games from
the **1930s or earlier**, but that era is not an automatic waiver. The exception applies
only after deliberate/exhaustive systematic research establishes HOME and city/state
while the surviving record still cannot support a specific physical building.

When the source program's HOME geography is systematically established for an era,
city/state may be propagated across already-established HOME rows under the same
default-plus-exceptions model, provided alternate/off-campus exceptions are isolated.
This is not permission to infer H/A/N from geography.

A broad unexplored pre-arena era remains unfinished research. A homogeneous ancient
residual whose reasonable systematic paths have been exhausted may be terminalized as a
population rather than reopened game by game, but every such row must have complete
city/state before Stage 3A-2 closes.

### Away rows

Regular-season `OPPONENT_HOME` exact-building completeness is **not** the source
school's Research responsibility.

The source school still owns supported H/A/N classification. If exact opponent-home
venue evidence is already present in the source, an accepted reciprocal package,
canonical/evidence layers, or approved shared-reference evidence, preserve and use it
with provenance. Otherwise, do not browse historical sources solely to fill the
opponent's home building; leave that chronology to the opponent's own Research lane.

If the home opponent is already published, known accepted home-site evidence should be
available for propagation and may not be silently discarded. A published home program's
valid researched-unresolved venue exception may propagate as an explicitly researched
blank venue, with known city/state retained.

### Neutral rows

Neutral-site games are an active Stage 3A venue-research responsibility.

Before external historical searching, check whether the **exact same game** already has
usable accepted venue evidence in current canonical/evidence layers, published reciprocal
packages, or other approved shared project data. Reuse only an unambiguous same-game
match with traceable provenance; do not infer a neutral venue from city, usual arena,
nearby games, or another edition of an event.

For the **1996-97 season through present**, apply a strong exact-venue expectation. A
modern neutral row should not survive as unresolved merely because the source school's
primary ledger omits the building. Challenge the obvious event/tournament, host,
opponent-institutional, reciprocal, and contemporary evidence paths before accepting
research debt.

For regular-season neutral games **1995-96 and earlier**, use the location-first
historical standard. Work accepted project evidence plus the obvious systematic
event/host/participant institutional opportunity. Preserve supported event identity and
city/state, and accept an exact building when that same evidence directly supplies it.
Once city/state is established, do not open another source path solely to recover the
building. Such surviving exact-building debt is nonblocking historical enrichment debt.
If locality itself remains unsupported after the obvious systematic opportunity, preserve
the researched unknown rather than escalating into bespoke row-level archive research.

When both participants are published, both source packages are available and known
same-game evidence must be propagated. A genuinely unresolved result should reflect
targeted review rather than a silent blank.

Postseason rows retain a stricter standard than historical regular-season neutrals.
NCAA Tournament physical venue, city, and state are mandatory and non-waivable. NIT,
conference-tournament, and every other postseason exact venue must be researched to
exhaustion; city/state alone is not enough to stop exact-building research. A research-
status marker does not authorize the historical regular-season shortcut for postseason.

## Research-accounting columns

`source-games.csv` may include these paired columns:

- `site_research_status`
- `site_research_basis`

A row with a material site gap must either be repaired or have both fields populated.

Allowed `site_research_status` values:

- `RESEARCHED_PARTIAL` — some site information is established, but one or more material site fields remain unresolved;
- `RESEARCHED_UNRESOLVED` — the relevant non-home site fact could not be safely established after deliberate research;
- `RESEARCHED_UNRESOLVED_HOME_VENUE` — a source-program HOME row has independently established H/A/N and complete city/state, but exhaustive historical research cannot support a specific physical venue identity.

`site_research_basis` must briefly identify the evidence checked or why stronger certainty is unsupported. It should be specific enough for another researcher or the Implementation lane to understand the unresolved state. Repeating one well-supported era-level basis across several rows is acceptable when the same research conclusion genuinely applies to all of them.

The dedicated HOME venue status is deliberately narrower than the other research statuses. It is valid only when `curated_site_type=SOURCE_PROGRAM_HOME`, `curated_venue_name` is blank, both city and state are populated, a substantive basis is present, and the row is not an NCAA Tournament game. It may not be used when agreeing target or reciprocal evidence already supplies a usable curated venue identity.

Examples for non-home unresolved research:

```text
RESEARCHED_PARTIAL
Both published source packages establish a neutral event but only the host city is supported; exact arena unresolved.
```

```text
RESEARCHED_UNRESOLVED
Contemporary schedule and reciprocal published source checked; neutral city/state cannot be safely established.
```

Example for an exhaustively researched HOME venue unknown:

```text
RESEARCHED_UNRESOLVED_HOME_VENUE
Official record book, institutional facility history, contemporary archival material, known venue chronology, and reciprocal published evidence reviewed; Starkville, MS home classification is established, but the surviving record does not identify the exact physical venue.
```

The columns are source-research metadata. They are not canonical basketball facts and are not written into `data/evidence/game-assertions.csv` by normal ingestion. A canonical HOME game using the exception must instead carry explicit `[RESEARCHED_UNRESOLVED_HOME_VENUE ...]` provenance in `notes` so the public unknown is not silent.

## What blocks RESEARCH_FROZEN

`RESEARCH_FROZEN` fails when:

- any source-program HOME row lacks complete city/state;
- any source-program HOME venue blank lacks a valid `RESEARCHED_UNRESOLVED_HOME_VENUE` research finding;
- any other material site-gap row is merely blank and unaccounted;
- any stricter existing rule such as NCAA site completeness fails.

A portfolio therefore cannot pass solely because:

- H/A/N contains no `UNKNOWN` values;
- a venue table exists;
- modern home games are complete;
- NCAA Tournament sites are complete;
- aggregate record/game counts reconcile.

Historical home-venue chronology must itself be researched across the program's in-scope history. Valid historical-unrecoverable venue rows remain explicitly visible rather than being converted to invented venue identities.

## Required research status card

Every `RESEARCH_FROZEN` status card should include at least:

```text
home rows missing venue: <count>
home rows missing location: 0
home rows missing both: 0
home publication blockers: 0
researched-unresolved home venue rows: <count>
unknown H/A/N rows: <count>
neutral rows missing venue/location: <count>/<count>
postseason rows missing venue/location: <count>/<count>
material site-gap rows: <count>
researched site-gap rows: <count>
unaccounted site-gap rows: 0
```

A nonzero `home rows missing venue` count is acceptable only when every such row is included in `researched-unresolved home venue rows`; the dedicated count must be surfaced rather than hidden.

When meaningful, include the decade/era concentration of remaining non-home researched gaps.

## Integration-lane responsibility

Research hardening is the first defense, not the only defense.

When a portfolio reaches the serialized Implementation lane:

1. rerun the research acceptance gate after current-main rebase;
2. reject or return to research any source-program HOME location gap, any ordinary HOME venue gap, or newly exposed unaccounted source-side site debt;
3. independently verify that any `RESEARCHED_UNRESOLVED_HOME_VENUE` row has complete location, explicit research basis, no usable agreeing target/reciprocal venue evidence, and matching canonical provenance;
4. independently verify that source/reciprocal site evidence is not lost when canonical games are matched or created;
5. allow away venue/location debt when the home opponent is unpublished, but propagate the home opponent's established site data when that opponent is published;
6. for neutral games, propagate available city/state evidence and apply heightened review when both participants are published;
7. before release, census the target program's projected public canonical history for HOME blockers, explicit researched HOME venue unknowns, `UNKNOWN` site type, and neutral/postseason location gaps;
8. stop before publication if the projected canonical result violates the published-site standard or is materially less complete than its available evidence without an explicit reviewed reason.

The Implementation lane should not become a second research lane that repairs hundreds of historical home games. Large chronology holes belong back in research/remediation. Implementation owns detection, evidence propagation, reconciliation, and final-public completeness proof.

## Retroactive remediation

Existing published debt is repaired separately from generic hardening. The preferred order is now:

1. published-program HOME venue/location research to zero unexcepted blockers, with only rigorously documented historical-unrecoverable venue exceptions remaining;
2. reciprocal propagation for away games whose home opponent is already published;
3. neutral-site city/state completion, prioritizing published-vs-published games and postseason;
4. neutral venue completion where support is available;
5. remaining H/A/N classification and identity/reference cleanup;
6. rerun the same database-wide completeness audit and quantify both the researched-unresolved HOME venue exceptions and remaining genuinely unresolved non-home debt.

Generic hardening and historical-data repair should not be mixed into one pull request.
