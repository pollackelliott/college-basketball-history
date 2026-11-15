# Arizona State source notes

## Controlling durable research state

Stage 4 was assembled mechanically from the verified Stage 3B cumulative checkpoint with SHA-256:

`cc40a0804d571ed0da9e3cfb1bf38ff57669fc326dc214713cb82afff880453d`

That checkpoint preserves the accepted Stage 1-3B research chain. Stage 4 does not reopen completed historical populations absent a concrete contradiction.

The controlling Stage 1 ledger is represented in the cumulative row-level Stage 2/3 mappings through `stage1_source_artifact`, `stage1_source_locator`, and literal `raw_text`. The package preserves that literal evidence in `source-games.csv`.

## Game universe and dates/scores

The accepted universe is 2,680 competitive games through completed 2025-26. Exhibitions remain excluded.

Exact dates use accepted Stage 3A date findings when present; otherwise a date is populated only when the literal accepted source row itself supplies a sufficiently explicit month/day. The 1948-49 row whose literal `J11` conflicts with the accepted Stage 3A correction remains dated 1949-01-13 in structured data, with the literal row preserved.

Five modern literal score defects were checked against official Arizona State evidence and repaired only in structured fields:

- 1995-01-12 at Stanford: Stanford 91, Arizona State 75 — https://thesundevils.com/sun-devil-mens-basketball-vs-stanford-series-history
- 2011-11-11 Montana State: Arizona State 78, Montana State 72 — https://thesundevils.com/news/2011/11/11/207838340
- 2013-11-29 College of Charleston: Arizona State 80, College of Charleston 58 — https://thesundevils.com/sports/mens-basketball/schedule/season/2013-14
- 2015-11-18 Kennesaw State: Arizona State 91, Kennesaw State 53 — https://thesundevils.com/news/2015/11/21/at-sundevilhoops-faces-another-2015-ncaa-tournament-team
- 2015-12-16 at UNLV: Arizona State 66, UNLV 56 — https://thesundevils.com/sports/mens-basketball/schedule/season/2015-16

The Stage 1 owner-authorized Cal Poly reciprocal insertion retains Cal Poly's literal perspective in `raw_text`; structured score/result are oriented to the Arizona State perspective without altering the evidence.

## Opponent identity

Stage 2 remains controlling. All 2,680 rows resolve to one of 310 distinct opponent identities. Current-program identities retain the protected-main program key established during Stage 2. Historical/NON_D1 identities without a registered global program key receive a deterministic research-local key derived from the accepted canonical name; global registration remains pending current-main rebase.

The complete 68-identity NON_D1 owner sanity scan is prepared in the Stage 4 supporting checkpoint. It represents 252 games. No owner disposition is recorded yet.

The informational Stage 2 self-corrected-opponent artifact is also preserved for owner context.

## Site research

Stage 3A remains closed. Its 216 H/A/N UNKNOWN rows are serialized as `curated_site_type=UNKNOWN` with `RESEARCHED_UNRESOLVED` accounting. The 12 neutral rows with surviving physical-site debt are serialized with `RESEARCHED_PARTIAL` or `RESEARCHED_UNRESOLVED` as appropriate. HOME site blockers remain zero.

Stage 3B remains closed at 98/98 event identities, 98/98 H/A/N classifications, 98/98 city/state sites, and 98/98 exact physical venues. NCAA Tournament physical venue + city + state completeness is 33/33.

The accepted 1964 Utah State postseason correction remains McArthur Court in Eugene, Oregon.

## Conference chronology

Arizona State institutional conference history states that ASU was in the Border Conference from 1931-61, joined the Western Athletic Conference in 1962, and entered Pac-10 play in 1978:
https://thesundevils.com/sun-devil-football-year-by-year

Arizona State men's basketball year-by-year history independently marks entry into Pac-10 play in 1978-79 and supplies the basketball season framing:
https://thesundevils.com/sun-devil-mens-basketball-year-by-year-recordspostseason

Current repository conference authority preserves Pac-10 and Pac-12 as separate historical naming-era display identities within the same legal lineage.

Arizona State Athletics states that full Big 12 membership began August 2, 2024:
https://thesundevils.com/news/2024/08/02/arizona-state-becomes-official-member-of-the-big-12

## Accomplishments reference

The current repository owner baseline for Arizona State is 8 regular-season conference championships, 0 conference-tournament championships, 17 NCAA appearances, 0 Final Fours, 0 national titles, and best finish ELITE_EIGHT in 1975.

Arizona State's current NCAA history confirms 17 NCAA Tournament appearances and three Elite Eight runs (1961, 1963, 1975):
https://thesundevils.com/news/2023/03/13/arizona-state-takes-on-nevada-in-ncaa-tournament
https://thesundevils.com/asu-tournament-history

Arizona State's official year-by-year standings support the accepted title-era seasons, and current 2025-26 institutional game-note material lists the eight conference championship seasons as 1958, 1959, 1961, 1962, 1963, 1964, 1973, and 1975. The 1943-44 first-place wartime standings are not counted as an official conference championship because the Border Conference did not award an official title in that wartime season.

Arizona State's conference-tournament history contains no tournament championship; its 2009 Pac-10 final appearance ended in a loss:
https://thesundevils.com/mens-basketball-conference-tournament-history

## Stage 4 historical status

Stage 4 completed with the owner NON_D1 sanity scan ready. Stage 5 was subsequently approved by the owner with zero flags, and Stage 6 completed the final adversarial self-challenge.


## Stage 6 reciprocal/shared-reference challenge

Stage 6 used already-accepted reciprocal program packages and project shared-reference state as adversarial evidence classes rather than reopening completed research wholesale. Accepted reciprocal corrections preserve Arizona State `raw_text` and alter only fields directly supported by stronger systematic evidence.

The 1943-02-17 Texas Tech row is specifically supported by accepted Texas Tech row `TTRAW-00383`, which preserves the same 46-41 Texas Tech result and records neutral Albuquerque, New Mexico Border Conference postseason/tournament play; its research basis states that Arizona official schedule/postseason history establishes Albuquerque and neutral classification. The exact building remains unresolved and is preserved as researched debt.

Research-time numeric venue IDs remain provisional. Stage 6 reused established research-base identities only where the physical building was definite; unresolved current-main duplicate/spelling/near-match situations remain explicit `PENDING_CURRENT_MAIN_REBASE` rather than being forced.


## Stage 7 immutable Research Freeze

The six-file portfolio is now `RESEARCH_FROZEN`.

No basketball fact was changed during Stage 7. Stage 7 changed only package-status documentation and cryptographically sealed the already accepted Stage 6 historical state.

The 19 blank numeric venue IDs are explicit shared-reference rebase work, not permission to redo the underlying historical research. Implementation must reconcile them against then-current protected `main`, reuse intervening global identities where appropriate, and allocate new numeric IDs only where still necessary.

`CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`

---

## Accepted supplemental All-History expansion

# Arizona State expansion — source and exact-provenance accounting

# Arizona State — frozen supplemental All-History expansion Research

- Workflow: ALL_HISTORY_EXPANSION, owner-approved INCEPTION+ scope; researched inception: 1911-1912.
- Immutable inherited Research-base SHA: df73675852ec5a43dfac50da0ee06d8bcabf8832.
- Current protected-main tool SHA binding: b9b88537cafaebed829a620c9e007e8caf767aa7 (freeze generated read-only).
- Original Stage 6 PASS checkpoint SHA-256: c637a920dce8a18bac290b79b7a2b03313b28d3c234bb58f7e094908b3e94ecc.
- Stage 5 explicit six-identity NON_D1 owner approval SHA-256: 5a2db44e88c6a1cfe8e4a0eb4b539eddedcf492f4d62e651369e6419488dc74d.
- Accepted original Stage 4 checkpoint SHA-256: ad253fffc9a5536ab2ae0d76853c458abc490da477b4bb896b284b972c20a1d8.
- **Inherited baseline**: accepted historical authority; all 469 inherited but unpublished games are exact baseline-row-hash references only, not newly authored game rows.
- **New supplemental**: exactly 10 accepted 1920-21 competitive games (8-2), with literal original Stage 1 raw_text restored without factual interpolation.
- **Season accounting**: exactly 39 expansion-required seasons (1911-12 through 1949-50), 1915-16 NO_TEAM, four terminal aggregate-only unidentified seasons totaling 41 games.
- **Official 1920-21 11-3 vs documented 9-2**: separate accounting, no invented three-game delta.
- **ASC W42-13**: terminal contested-source representation, neither a new ASC game nor the same as inherited Northern Arizona W45-13.
- **Source sites and dates**: ten UNKNOWN H/A/N and ten blank dates are researched unresolved, not inferred from geography or score order.
- **VENUE**: no supported supplemental physical venue; do not add a speculative venue.
- **Opponent support**: three NEW_SUPPLEMENTAL and three hash-bound EXTEND_INHERITED actions; underlying inherited row bytes stay untouched. All six identities are owner-cleared in Stage 5.
- **Owner scope**: supersedes inherited 1950-51+ top-level classification for Research only, no global classification mutation.
- **Research acceptance**: Stage 6 permanent acceptance 0 errors/0 warnings and PRE-FREEZE SELF-CHALLENGE: PASS.
- **Implementation**: NOT BEGUN. A future current-main rebase is required; do not apply shared or public data in Research.

## Accepted Stage 6 source notes (unaltered text)

# arizona-state source notes

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
  "accounting_contradictions": [
    {
      "audit_sha256": "b4f2a7276927053ccdabe8fd8aeedce353d620b7941820ab378e9eeae11f6e04",
      "identified_record": {
        "games": 11,
        "losses": 2,
        "wins": 9
      },
      "institutional_record": {
        "games": 14,
        "losses": 3,
        "wins": 11
      },
      "mechanical_delta": {
        "games": 3,
        "losses": 1,
        "wins": 2
      },
      "owner_disposition": "https://github.com/pollackelliott/college-basketball-history/issues/582",
      "parent_checkpoint_sha256": "4e5567e832deb63f531dd3a04386de3afd1755db0717dc89a86f67a1e948d8e0",
      "research_base_sha": "df73675852ec5a43dfac50da0ee06d8bcabf8832",
      "school_key": "arizona-state",
      "season": "1920-1921",
      "source_description": "Institutional detailed rows and season/cumulative accounting conflict; arithmetic fitting is prohibited.",
      "terminal_classification": "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
      "warning": "Preserve identified game rows unchanged. This delta is diagnostic only and is never an unidentified-game count or result allocation."
    }
  ],
  "coverage": [
    {
      "audit_sha256": "b4f2a7276927053ccdabe8fd8aeedce353d620b7941820ab378e9eeae11f6e04",
      "identified_record": {
        "games": 0,
        "losses": 0,
        "wins": 0
      },
      "institutional_record": {
        "games": 1,
        "losses": 1,
        "wins": 0
      },
      "owner_disposition": "https://github.com/pollackelliott/college-basketball-history/issues/582",
      "parent_checkpoint_sha256": "4e5567e832deb63f531dd3a04386de3afd1755db0717dc89a86f67a1e948d8e0",
      "research_base_sha": "df73675852ec5a43dfac50da0ee06d8bcabf8832",
      "school_key": "arizona-state",
      "season": "1916-1917",
      "source_description": "ASU official historical season aggregate; game identities not recoverable in bounded research. No anonymous rows or aggregate W/L allocations.",
      "terminal_classification": "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP",
      "unidentified_record": {
        "games": 1,
        "losses": 1,
        "wins": 0
      },
      "warning": "Season-level institutional record only. No unidentified game rows, opponents, dates, sites, scores, or result allocations are represented."
    },
    {
      "audit_sha256": "b4f2a7276927053ccdabe8fd8aeedce353d620b7941820ab378e9eeae11f6e04",
      "identified_record": {
        "games": 0,
        "losses": 0,
        "wins": 0
      },
      "institutional_record": {
        "games": 18,
        "losses": 4,
        "wins": 14
      },
      "owner_disposition": "https://github.com/pollackelliott/college-basketball-history/issues/582",
      "parent_checkpoint_sha256": "4e5567e832deb63f531dd3a04386de3afd1755db0717dc89a86f67a1e948d8e0",
      "research_base_sha": "df73675852ec5a43dfac50da0ee06d8bcabf8832",
      "school_key": "arizona-state",
      "season": "1917-1918",
      "source_description": "ASU official historical season aggregate; game identities not recoverable in bounded research. No anonymous rows or aggregate W/L allocations.",
      "terminal_classification": "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP",
      "unidentified_record": {
        "games": 18,
        "losses": 4,
        "wins": 14
      },
      "warning": "Season-level institutional record only. No unidentified game rows, opponents, dates, sites, scores, or result allocations are represented."
    },
    {
      "audit_sha256": "b4f2a7276927053ccdabe8fd8aeedce353d620b7941820ab378e9eeae11f6e04",
      "identified_record": {
        "games": 0,
        "losses": 0,
        "wins": 0
      },
      "institutional_record": {
        "games": 8,
        "losses": 3,
        "wins": 5
      },
      "owner_disposition": "https://github.com/pollackelliott/college-basketball-history/issues/582",
      "parent_checkpoint_sha256": "4e5567e832deb63f531dd3a04386de3afd1755db0717dc89a86f67a1e948d8e0",
      "research_base_sha": "df73675852ec5a43dfac50da0ee06d8bcabf8832",
      "school_key": "arizona-state",
      "season": "1919-1920",
      "source_description": "ASU official historical season aggregate; game identities not recoverable in bounded research. No anonymous rows or aggregate W/L allocations.",
      "terminal_classification": "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP",
      "unidentified_record": {
        "games": 8,
        "losses": 3,
        "wins": 5
      },
      "warning": "Season-level institutional record only. No unidentified game rows, opponents, dates, sites, scores, or result allocations are represented."
    },
    {
      "audit_sha256": "b4f2a7276927053ccdabe8fd8aeedce353d620b7941820ab378e9eeae11f6e04",
      "identified_record": {
        "games": 0,
        "losses": 0,
        "wins": 0
      },
      "institutional_record": {
        "games": 14,
        "losses": 2,
        "wins": 12
      },
      "owner_disposition": "https://github.com/pollackelliott/college-basketball-history/issues/582",
      "parent_checkpoint_sha256": "4e5567e832deb63f531dd3a04386de3afd1755db0717dc89a86f67a1e948d8e0",
      "research_base_sha": "df73675852ec5a43dfac50da0ee06d8bcabf8832",
      "school_key": "arizona-state",
      "season": "1943-1944",
      "source_description": "ASU official historical season aggregate; game identities not recoverable in bounded research. Explicit narrow wartime exception approved for 1943-44. No anonymous rows or aggregate W/L allocations.",
      "terminal_classification": "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP",
      "unidentified_record": {
        "games": 14,
        "losses": 2,
        "wins": 12
      },
      "warning": "Season-level institutional record only. No unidentified game rows, opponents, dates, sites, scores, or result allocations are represented."
    }
  ],
  "schema_version": 1
}
```

## Durable row-level source families


## Owner-approved terminal source representation — 1920-21

- **Inherited accepted source-game result** `ASU-STG2-PRE1950-1920-21-001`: Northern Arizona / Flagstaff **W45-13**, unchanged.
- **Distinct source assertion**: ASC **W42-13**, preserved as `TERMINAL_CONTESTED_SOURCE_REPRESENTATION`, *not* an independently identified additional game, and *not* evidence that ASC and Northern Arizona were the same game. No supplemental ASC game row has been added.
- Owner-authorized terminal representation is embedded in the accepted original Stage 1 COMPLETE checkpoint 0020 (`terminal-contested-source-representation.json`) and the retained Stage 5 checkpoint ancestry. Reopen only with independent direct game evidence; neither string similarity nor arithmetic authorizes identity inference.
- The official 1920-21 institutional **11-3** record remains separate from the eleven identified source results **9-2** (including the inherited Northern Arizona W45-13 and ten supplemental games W8-L2). The arithmetic **2-1 / three-game difference** is source-accounting contradiction, not three inferred or allocated games.

## Separately preserved early-history questions

- In 1917-18, the contemporary Tempe Normal 15-wins-of-19 assertion is not proven identical in time/scope to the modern official **14-4 / 18-game** season summary. Do not create a nineteenth game or silently replace the official record.
- For 1943-44, the explicit owner-approved wartime season-level accounting is **12-2 / 14 unidentified games**, not individual game identities. A conference first-place claim is not automatically a conferred championship and remains a separate accomplishments question.
- Exactly 41 unidentified games across 1916-17 (1), 1917-18 (18), 1919-20 (8), and 1943-44 (14) remain **season-level terminal debt only**. No anonymous source games, opponents, dates, scores, sites, or result allocations are represented.
