# la-salle source notes

Generated mechanically from durable Research checkpoint evidence. Literal row-level evidence remains preserved in source-games.csv.

## Research coverage declaration

- Primary-source historical results cutoff: 2025-2026
- Required completed-season cutoff: 2025-2026
- These cutoffs come from explicit Research source inventory and target coverage. A media-guide title or filename never establishes the results cutoff.

## Research-exhausted institutional aggregate coverage gap

This is season-level historical accounting, not one or more game records.
The official season record and separately identified games are not interchangeable. Do not allocate unidentified games to invented dates, opponents, or scores. Any accounting_contradictions entries are diagnostic source conflicts only; their deltas must never be treated as missing-game counts, overlap identities, or result allocations.

```json
{
  "coverage": [
    {
      "audit_sha256": "ea2219506e6da72bb5213631c7ae337076ddcc4ce2b3eecf13dc5e000b48313b",
      "evidence_member": "founding-season-evidence-exhaustion.json",
      "identified_record": {
        "games": 2,
        "losses": 1,
        "wins": 1
      },
      "institutional_record": {
        "games": 19,
        "losses": 4,
        "wins": 15
      },
      "owner_disposition": "https://github.com/pollackelliott/college-basketball-history/issues/450",
      "parent_checkpoint_sha256": "4e079b53c5d7118881fbdd56d4e9aa38b5930a4dbbc15e0a940cbb0ee0d8f06f",
      "research_base_sha": "933d2f9e7ebdd24fefcafda326a7ebe898a476df",
      "school_key": "la-salle",
      "season": "1930-31",
      "source_description": "Institutional year-by-year season aggregate; individual game details incomplete",
      "terminal_classification": "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP",
      "unidentified_record": {
        "games": 17,
        "losses": 3,
        "wins": 14
      },
      "warning": "Missing-game count is derived from a primary institutional aggregate, not directly stated by the institution. No unidentified game rows are represented."
    }
  ],
  "schema_version": 1
}
```

## Durable row-level source families

- PRIMARY_MEDIA_GUIDE_NARRATIVE: 3 game rows
- PRIMARY_MEDIA_GUIDE_SERIES_RECONCILIATION: 2 game rows
- PRIMARY_MEDIA_GUIDE_TABLE: 2,582 game rows

## Accepted target top-level scope

- Accepted Research scope: 1930-31+ / INCEPTION+
- Scope status: OWNER_CONFIRMED
- Scope basis: ALWAYS_TOP_LEVEL_FROM_INCEPTION
- Owner approval date: 2026-11-06
- Accepted competitive-history start: 1930-31
- Reusable current-main baseline at Research base/current protected main: ABSENT
- Baseline disposition: ESTABLISH_NEW_REFERENCE_FROM_FROZEN_RESEARCH_AUTHORITY
- La Salle institutional evidence identifies James Henry as men's basketball coach for 1930-31; the accepted competitive Research universe begins in the same season.
- This frozen scope is historical authority for later current-main/Phase 0 reconciliation. Implementation must not reopen or infer a different target-school scope merely because current main lacks a reusable La Salle scope row.
