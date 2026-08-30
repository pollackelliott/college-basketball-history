# Site Completeness Protocol

## Purpose

This protocol prevents a school from appearing research-complete or publication-ready while large venue, location, or H/A/N gaps remain unnoticed.

The governing principle is:

> **UNKNOWN is preferable to unsupported certainty, but an unknown may not be silent.**

A historical fact may remain unresolved after reasonable research. The workflow does not require researchers to invent a venue, geography, or H/A/N classification. It does require every material site gap to be counted, investigated, and made machine-visible before `RESEARCH_FROZEN`.

## Research-lane responsibility

Before `RESEARCH_FROZEN`, the school portfolio must run the permanent `research-check` in `tools/onboarding_hardening.py`.

The site census covers at least:

- `SOURCE_PROGRAM_HOME` rows missing `curated_venue_name`;
- `SOURCE_PROGRAM_HOME` rows missing city/state;
- every `UNKNOWN` `curated_site_type` row;
- non-NCAA `NEUTRAL` rows missing venue and/or city/state;
- `CONFERENCE_TOURNAMENT`, `NIT`, and `POSTSEASON` rows missing venue and/or city/state;
- the same gaps summarized by season and decade so a historical chronology hole cannot hide inside aggregate H/A/N counts.

Away regular-season venue completeness is not a research-freeze blocker. A school's own research lane is not required to reconstruct every opponent building. Reciprocal evidence and later canonical enrichment may still improve those rows.

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

Examples:

```text
RESEARCHED_PARTIAL
Official schedule establishes Norman, Oklahoma; exact building not identified.
```

```text
RESEARCHED_UNRESOLVED
Media guide ledger and available facility chronology checked; exact 1912 home site unsupported.
```

The columns are source-research metadata. They are not canonical basketball facts and are not written into `data/evidence/game-assertions.csv` by normal ingestion.

## What blocks RESEARCH_FROZEN

`RESEARCH_FROZEN` fails when any material site-gap row is merely blank and unaccounted.

A portfolio therefore cannot pass solely because:

- H/A/N contains no `UNKNOWN` values;
- a venue table exists;
- modern home games are complete;
- NCAA Tournament sites are complete;
- aggregate record/game counts reconcile.

Historical home-venue chronology must itself have been audited.

A genuinely unresolved row may pass when it is explicitly research-accounted, except where a stricter rule such as NCAA site completeness applies.

## Required research status card

Every `RESEARCH_FROZEN` status card should include at least:

```text
home rows missing venue: <count>
home rows missing location: <count>
home rows missing both: <count>
unknown H/A/N rows: <count>
neutral rows missing venue/location: <count>/<count>
postseason rows missing venue/location: <count>/<count>
material site-gap rows: <count>
researched site-gap rows: <count>
unaccounted site-gap rows: 0
```

When meaningful, include the decade/era concentration of the remaining researched gaps.

## Integration-lane responsibility

Research hardening is the first defense, not the only defense.

When a portfolio reaches the serialized Implementation lane:

1. rerun the research acceptance gate after current-main rebase;
2. reject or return to research any newly exposed unaccounted source-side site debt;
3. independently verify that source/reciprocal site evidence is not lost when canonical games are matched or created;
4. before release, census the target program's projected public canonical history for home-site gaps, `UNKNOWN` site type, and neutral/postseason location gaps;
5. stop before publication if the projected canonical result is materially less complete than its available evidence without an explicit reviewed reason.

The Implementation lane should not become a second research lane that repairs hundreds of historical home games. Large chronology holes belong back in research/remediation. Implementation owns detection, evidence propagation, reconciliation, and final-public completeness proof.

## Retroactive remediation

Existing published debt is repaired separately from generic hardening. The preferred order is:

1. deterministic canonical/evidence propagation where source evidence is already complete;
2. conservative reciprocal-evidence enrichment;
3. historical home-venue chronology research;
4. concentrated H/A/N classification backlogs;
5. targeted venue/geography identity normalization;
6. rerun the same database-wide completeness audit and quantify the remaining genuinely unresolved debt.

Generic hardening and historical-data repair should not be mixed into one pull request.
