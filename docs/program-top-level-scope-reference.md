# Program Top-Level History Scope Reference

- **Status:** Required research-lane baseline
- **Data:** `data/reference/program-top-level-scope.csv`
- **Purpose:** Remove repetitive owner handoffs about when a current Division I program first entered, left, or re-entered the project's accepted top-level / Division I-equivalent history universe.

## 1. Governing rule

Every new Research lane must read `data/reference/program-top-level-scope.csv` before defining the target school's game universe.

The reference is the default owner-supplied history-scope baseline. The owner does not need to restate that a school has always been top-level or provide its first Division I season when the school is present in this file.

The reference was supplied by the owner and received a bounded structural and historical sanity audit on 2026-09-02. It is intentionally treated as a strong project baseline, not as infallible external historical law. Ordinary school research should sanity-check the scope against authoritative school/conference/NCAA evidence encountered naturally during research. Do **not** independently re-research the entire classification history merely because the reference exists.

If authoritative target-school evidence materially contradicts the reference, stop only on that bounded scope issue and bring the contradiction to the owner. Do not silently override the reference.

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

## 4. Interrupted histories

Do not collapse a multiple-interval school into only its current stint or only its first top-level season.

Every interval listed is independently accepted. Games outside every listed interval are outside the target school's accepted top-level universe unless a later owner ruling changes the reference.

## 5. Relationship to `programs.csv`

`data/reference/programs.csv` remains the global program registry. This scope reference is a research-policy input and does not automatically overwrite `history_start_season`, `history_scope_status`, or previously published school metadata.

During implementation, a newly researched school's final accepted history metadata should be reconciled with current-main `programs.csv` under the normal serialized workflow. A prior explicit owner ruling already recorded in `programs.csv` remains valid unless this reference or newly discovered authoritative evidence creates a real contradiction.

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

Do not edit `data/reference/program-top-level-scope.csv` casually during a school lane.

If research proves a scope row wrong, preserve the evidence and route the correction through the serialized repository-mutation process so future lanes inherit the corrected baseline. A correction to one school does not reopen unrelated rows.
