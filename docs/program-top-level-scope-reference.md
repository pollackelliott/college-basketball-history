# Program Top-Level History Scope Reference

- **Status:** Required research-lane baseline
- **Data:** `data/reference/program-top-level-scope.csv`
- **Purpose:** Preserve owner-supplied authority for when a current Division I program entered, left, or re-entered the project's accepted top-level / Division I-equivalent classification. This reference does not define institutional program inception.

## 1. Governing rule

Every new Research lane must read `data/reference/program-top-level-scope.csv` before defining the target school's game universe.

The reference is the default owner-supplied top-level classification baseline. The owner does not need to restate that a school has always been top-level or provide its first Division I season when the school is present in this file.

Top-level classification and complete institutional publication history are permanently separate authorities. `INCEPTION+` means that accepted top-level classification begins at the same recognized program inception; any other scope expression says nothing by itself about when varsity basketball began. Never infer `program_inception_season` from a top-level start, reciprocal canonical games, earliest database appearance, or geography.

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

The reference describes **accepted top-level / Division I-equivalent classification seasons**, not merely current NCAA membership or postseason eligibility and not institutional publication inception. Pre-1973 history therefore uses the project's top-level-equivalent concept rather than pretending the modern NCAA Division I label existed unchanged throughout basketball history.

## 3. Research-lane behavior

At lane startup:

1. locate the target school in the scope reference;
2. record the applicable `top_level_scope` in the research notes/status card;
3. during the current compatibility transition, continue constructing the Research package's operational game universe from the accepted intervals, subject to the normal exhibition and game-identity rules; this temporary workflow boundary does not redefine those intervals as institutional inception;
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

`data/reference/programs.csv` remains the global program registry. It now carries
the independent publication-history fields `program_inception_season` and
`history_coverage_status`. The controlled coverage states are
`UNMIGRATED`, `LEGACY_TOP_LEVEL_ONLY`, and
`COMPLETE_INSTITUTIONAL`.

The top-level scope reference does not automatically overwrite or supply
`program_inception_season`. A published program may be seeded as
`COMPLETE_INSTITUTIONAL` only when accepted authority establishes both
`INCEPTION+` classification and a valid existing first-season value that truly
represents program inception. Published programs with any non-`INCEPTION+` accepted
top-level expression remain `LEGACY_TOP_LEVEL_ONLY` until their institutional
supplement is researched and integrated. Unpublished current-D1 programs remain
`UNMIGRATED` unless a later authorized migration establishes otherwise.

The existing `history_start_season`, `history_scope_status`,
`history_scope_basis`, `history_scope_notes`, and
`history_scope_intervals` remain compatibility/top-level fields during this
transition. They are not repurposed as institutional inception. Existing publication,
Research, ingestion, site, and accomplishment workflows may still depend on those
fields until later all-history maintenance units migrate each consumer explicitly.

During ordinary serialized school work before those later migrations, a newly researched
school's final accepted top-level metadata is still reconciled under the existing guarded
workflow. If a frozen scope expression differs from the target row in this reference,
the target row is stale and the existing target-row correction rules continue to apply.
That compatibility behavior does not authorize a global rewrite of this reference.

A genuine postseason tournament game played while the target program is outside its
accepted top-level scope should ordinarily use `POSTSEASON`, including a
lower-level conference tournament. `CONFERENCE_TOURNAMENT` remains the
D-I/top-level conference-tournament taxonomy. Unit 1 establishes the taxonomy boundary;
later maintenance owns the lower-level postseason site-policy changes.

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
\nIf the owner explicitly supersedes a not-yet-published school's scope **after** ordinary Phase 0, the existing Phase 0/Integration Freeze/Stage 2 authority is stale for publication. Do not rewrite the immutable Research Freeze or force-reset the onboarding branch. After explicit Control Center authorization, use the guarded `PHASE0_SCOPE_SUPERSESSION` path: preserve the original Research artifact, hash-bind the new scope and exact excluded source-game population, rerun current-main Stage 1/ordinary Phase 0 from the mechanically clipped candidate, update only the target scope-reference/program metadata plus normally required package/shared-reference integration surfaces, publish by exact-predecessor CAS, and require fresh independent equivalence verification before restarting Stage 2.\n