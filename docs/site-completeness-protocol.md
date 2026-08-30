# Site Completeness Protocol

## Purpose

This protocol prevents a school from appearing research-complete or publication-ready while large venue, location, or H/A/N gaps remain unnoticed.

The governing principles are:

> **UNKNOWN is preferable to unsupported certainty, but an unknown may not be silent.**

and, for a program's own home history:

> **A published program's home venue and location chronology is a publication requirement, not a waivable unknown.**

Most historical site facts may remain unresolved after reasonable research when the unresolved state is explicit. A school's own home venue/location is held to a stronger standard because the project deliberately researches each program's home-facility history before publication.

The detailed owner standard is recorded in `docs/site-completeness-owner-standard.md`.

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

Every in-scope `SOURCE_PROGRAM_HOME` row must resolve to a venue and complete city/state geography before `RESEARCH_FROZEN`.

`RESEARCHED_PARTIAL` or `RESEARCHED_UNRESOLVED` may be used while research is still in progress, but neither status waives a home-site gap. The research lane is expected to use the school's documented facility chronology to fill predecessor arenas, facility transitions, alternate home sites, temporary sites, and known one-off home venues.

A broad historical gap such as an entire pre-arena era must be treated as unfinished research rather than accepted as a permanent blank.

### Away rows

Away regular-season venue completeness is not a research-freeze blocker. A school's own research lane is not required to reconstruct every opponent building.

If the away opponent is not yet published, venue/location blanks are expected reciprocal debt and may remain until that opponent is researched. When the home opponent is already published, its home-site research should be available for canonical propagation and may not be silently discarded.

### Neutral rows

Neutral-site games should have city/state whenever the historical record supports it, and venue identity should also be researched where practical.

When both participants are published, both source packages are available. A remaining neutral-location blank therefore requires heightened review: known evidence from either side must be propagated, and a genuinely unresolved result should reflect targeted review of both published source packages rather than a silent blank.

NCAA Tournament rows retain the stricter existing requirement: physical venue, city, and state are mandatory. A research-status marker cannot waive NCAA completeness.

## Research-accounting columns

`source-games.csv` may include these paired columns:

- `site_research_status`
- `site_research_basis`

A row with a material site gap must either be repaired or have both fields populated.

Allowed `site_research_status` values:

- `RESEARCHED_PARTIAL` — some site information is established, but one or more material site fields remain unresolved;
- `RESEARCHED_UNRESOLVED` — the relevant site fact could not be safely established after deliberate research.

`site_research_basis` must briefly identify the evidence checked or why stronger certainty is unsupported. It should be specific enough for another researcher or the Implementation lane to understand the unresolved state. Repeating one well-supported era-level basis across several rows is acceptable when the same research conclusion genuinely applies to all of them.

These statuses can account for non-home uncertainty. They do **not** satisfy `RESEARCH_FROZEN` for a source-program home row that still lacks venue or complete location.

Examples for non-home unresolved research:

```text
RESEARCHED_PARTIAL
Both published source packages establish a neutral event but only the host city is supported; exact arena unresolved.
```

```text
RESEARCHED_UNRESOLVED
Contemporary schedule and reciprocal published source checked; neutral city/state cannot be safely established.
```

The columns are source-research metadata. They are not canonical basketball facts and are not written into `data/evidence/game-assertions.csv` by normal ingestion.

## What blocks RESEARCH_FROZEN

`RESEARCH_FROZEN` fails when:

- any source-program home row lacks venue or complete location, regardless of research-status metadata;
- any other material site-gap row is merely blank and unaccounted;
- any stricter existing rule such as NCAA site completeness fails.

A portfolio therefore cannot pass solely because:

- H/A/N contains no `UNKNOWN` values;
- a venue table exists;
- modern home games are complete;
- NCAA Tournament sites are complete;
- aggregate record/game counts reconcile.

Historical home-venue chronology must itself be complete across the program's in-scope history.

## Required research status card

Every `RESEARCH_FROZEN` status card should include at least:

```text
home rows missing venue: 0
home rows missing location: 0
home rows missing both: 0
home publication blockers: 0
unknown H/A/N rows: <count>
neutral rows missing venue/location: <count>/<count>
postseason rows missing venue/location: <count>/<count>
material site-gap rows: <count>
researched site-gap rows: <count>
unaccounted site-gap rows: 0
```

When meaningful, include the decade/era concentration of remaining non-home researched gaps.

## Integration-lane responsibility

Research hardening is the first defense, not the only defense.

When a portfolio reaches the serialized Implementation lane:

1. rerun the research acceptance gate after current-main rebase;
2. reject or return to research any source-program home venue/location gap or newly exposed unaccounted source-side site debt;
3. independently verify that source/reciprocal site evidence is not lost when canonical games are matched or created;
4. allow away venue/location debt when the home opponent is unpublished, but propagate the home opponent's established site data when that opponent is published;
5. for neutral games, propagate available city/state evidence and apply heightened review when both participants are published;
6. before release, census the target program's projected public canonical history for home-site gaps, `UNKNOWN` site type, and neutral/postseason location gaps;
7. stop before publication if the projected canonical result violates the published-site standard or is materially less complete than its available evidence without an explicit reviewed reason.

The Implementation lane should not become a second research lane that repairs hundreds of historical home games. Large chronology holes belong back in research/remediation. Implementation owns detection, evidence propagation, reconciliation, and final-public completeness proof.

## Retroactive remediation

Existing published debt is repaired separately from generic hardening. The preferred order is now:

1. published-program home venue/location completeness to zero blanks;
2. reciprocal propagation for away games whose home opponent is already published;
3. neutral-site city/state completion, prioritizing published-vs-published games and postseason;
4. neutral venue completion where support is available;
5. remaining H/A/N classification and identity/reference cleanup;
6. rerun the same database-wide completeness audit and quantify the remaining genuinely unresolved non-home debt.

Generic hardening and historical-data repair should not be mixed into one pull request.
