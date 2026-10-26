# Program Top-Level History Scope Reference

- **Status:** Required research-lane baseline
- **Data:** `data/reference/program-top-level-scope.csv`
- **Purpose:** Remove repetitive owner handoffs about when a current Division I program first entered, left, or re-entered the project's accepted top-level / Division I-equivalent history universe.

## 1. Governing rule

Every new Research lane must read `data/reference/program-top-level-scope.csv` before defining the target school's game universe.

The reference is the default owner-supplied history-scope baseline. The owner does not need to restate that a school has always been top-level or provide its first Division I season when the school is present in this file.

The reference was supplied by the owner and received a bounded structural and historical sanity audit on 2026-09-02. It is intentionally treated as a strong project baseline, not as infallible external historical law. Ordinary school research should sanity-check the scope against authoritative school/conference/NCAA evidence encountered naturally during research. Do **not** independently re-research the entire classification history merely because the reference exists.

If authoritative target-school evidence materially contradicts the reference, resolve only that bounded scope issue before Research Freeze. Do not silently override the reference. When owner judgment is genuinely required, obtain it in Research; once resolved, record the final accepted scope explicitly in the six-file package so Implementation does not have to reopen the same question.

## 2. Syntax

`top_level_scope` uses compact interval syntax:

- `INCEPTION+` = accepted top-level / Division I-equivalent history begins with program inception and continues through present.
- `YYYY-YY+` = accepted history begins with that season and continues through present.
- `YYYY-YY..YYYY-YY` = a closed accepted top-level interval.
- `|` separates multiple accepted intervals.

Examples:

- `USC,INCEPTION+`
- `Abilene Christian,2013-14+`
- `Akron,1947-48..1949-50|1980-81+`
- `Miami,1948-49..1952-53|1954-55..1970-71|1985-86+`

The reference describes **accepted top-level / Division I-equivalent seasons for project inclusion**, not merely current NCAA membership or postseason eligibility. Pre-1973 history therefore uses the project's top-level-equivalent concept rather than pretending the modern NCAA Division I label existed unchanged throughout basketball history.

## 3. Research-lane behavior

At lane startup:

1. locate the target school in the scope reference;
2. record the applicable `top_level_scope` in the research notes/status card;
3. construct the competitive game universe only from accepted intervals, subject to the normal exhibition and game-identity rules;
4. preserve source evidence from non-scope seasons when useful for context, but do not ingest those games into the target canonical universe;
5. continue ordinary research without asking the owner to restate scope.

A lane should contact the owner about history scope only when:

- the target school is absent from the reference;
- the school identity cannot be matched unambiguously;
- authoritative evidence encountered during ordinary research materially contradicts an interval;
- a predecessor/successor or institutional identity question makes the listed scope genuinely ambiguous.

Before declaring `RESEARCH_FROZEN`, the six-file package must make the target scope explicit.
Use `notes.md` as the preferred durable location and record one of these two semantic states:

- **Scope baseline confirmed:** the accepted package scope equals the current `program-top-level-scope.csv` expression.
- **Scope baseline superseded:** Research has settled a different accepted expression; record that exact expression plus the historical/owner basis.

The wording need not be machine-identical to those labels for older packages, but the package must be unambiguous about the accepted expression. The final Research Freeze status/handoff should repeat it.

## 4. Interrupted histories

Do not collapse a multiple-interval school into only its current stint or only its first top-level season.

Every interval listed is independently accepted. Games outside every listed interval are outside the target school's accepted top-level universe unless a later owner ruling changes the reference.

## 5. Relationship to `programs.csv`

`data/reference/programs.csv` remains the global program registry. This scope reference is a research-policy input and does not automatically overwrite `history_start_season`, `history_scope_status`, or previously published school metadata.

During implementation, a newly researched school's final accepted history metadata is taken from the explicit frozen package scope statement and reconciled under the normal serialized workflow. Implementation writes that same accepted scope into current-main-compatible `programs.csv` metadata. If the frozen expression differs from the target row in `program-top-level-scope.csv`, the target row is stale and must be corrected in the same guarded school Phase 0/onboarding commit. The frozen package does not need a second owner approval merely because the reusable baseline lagged behind it. A prior explicit owner ruling already recorded in `programs.csv` remains valid only when it does not conflict with the later accepted frozen package scope or genuinely new authoritative evidence.

`programs.csv` retains `history_start_season` as the first accepted season for backward-compatible display and validation. When accepted history is interrupted, Implementation also writes the exact owner-approved interval expression to `history_scope_intervals` and uses `history_scope_basis=TOP_LEVEL_INTERVALS`. Publication, ingestion, reciprocal-only review, conference-history clipping, and accomplishment cross-checking must use `history_scope_intervals` when it is present rather than collapsing the program to a single lower-bound cutoff.

## 6. Validation status

The 2026-09-02 bounded audit confirmed:

- 365 distinct program rows;
- no blank scope values in the supplied source;
- 123 `INCEPTION+` programs;
- 211 single-start programs;
- 31 programs with multiple top-level intervals;
- interrupted histories can be represented without loss using explicit interval syntax;
- representative modern transition cases and the historical `Division I or equivalent` framing were cross-checked against current institutional / major-school evidence.

This was **not** a fresh 365-school historical research project. The permanent safeguard is therefore two-layered: use the owner-supplied baseline by default, and surface only genuine contradictions found during normal target-school research.

## 7. Change control

Do not edit `data/reference/program-top-level-scope.csv` casually during Research or outside the serialized mutation path.

If Research confirms the existing target row, no baseline mutation is needed. If the final frozen package explicitly supersedes that target row, the discovering Research lane preserves the evidence but does not mutate protected main. The **same school's serialized Implementation lane** then updates exactly that target row during its guarded Phase 0/onboarding commit, alongside the matching `programs.csv` history metadata. This is normal target-school integration authority and does not require a separate Control Center maintenance PR or renewed owner scope decision. The changed-path/diff must remain target-row-only for this reference file.

A correction to one school does not reopen unrelated rows. Any unrelated/global scope-reference rewrite remains outside this exception and follows ordinary shared-reference maintenance controls.
