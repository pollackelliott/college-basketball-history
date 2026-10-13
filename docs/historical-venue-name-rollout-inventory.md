# Historical venue-name rollout inventory

Status: **CONTROL CENTER CONSOLIDATION COMPLETE — NO IMPLEMENTATION AUTHORIZED**  
Protected-main inventory baseline: `3f9edc3de0237fde453a87000cf6755b97962687`  
Research/census branch source: `maintenance/historical-venue-name-census`

## Purpose

This document is the Control Center bridge between the completed historical venue-name research program and future bounded maintenance rollout.

It does **not** authorize protected-main mutation.

The historical census establishes truth/disposition. This inventory separates that research state into mutation families so implementation can be serialized without reopening settled history or mixing incompatible maintenance topologies.

## Current production state

Protected main currently contains exact `OFFICIAL_NAMING_PERIOD` rows for three physical venues:

- `VEN-000052` — Colorado / CU Events Center lineage
- `VEN-000096` — Syracuse / Carrier Dome → JMA Wireless Dome
- `VEN-000196` — Illinois / Assembly Hall → State Farm Center

These are already production-proven and are not part of the pending rollout population.

## Completed multi-name census state

The durable 364-row multi-name ledger currently contains:

| Disposition | Rows | Rollout meaning |
|---|---:|---|
| `MIGRATED` | 3 | Already production-proven; no new rollout work. |
| `PERIODIZE` | 160 | Historical formal rename is established, but exact naming-period readiness must be separately verified before implementation. |
| `ALIAS_ONLY` | 190 | No historical naming periods warranted from this program. |
| `IDENTITY_RESOLVED` | 4 | Three physical-identity/alias maintenance work items; separate from ordinary period rollout. |
| `CANONICAL_CORRECTION` | 4 | Shared registry/display/alias cleanup; separate from ordinary period rollout. |
| `RESEARCH_EXHAUSTED` | 3 | Terminal owner-accepted uncertainty; do not recycle absent materially stronger evidence. |

The four `IDENTITY_RESOLVED` rows represent three actual maintenance work items because Seattle is represented by both linked IDs `VEN-000102` and `VEN-000315`.

## Completed single-name screen and chronology state

The 483 single-name venues received the completed high-yield screen:

- 38 individually screened through risk-ranked tiers;
- 14 positive candidates;
- 24 clear on the light pass;
- 445 low-signal venues intentionally not individually searched;
- zero deep chronology research performed during the screen itself.

All 14 positive candidates then received bounded authoritative chronology research.

Final chronology result:

- `PERIODIZE_READY`: **6**
- `PARTIAL_PERIODIZE_RESEARCH`: **8**
- unresolved physical-identity conflicts: **0**

## Mutation family A — exact naming-period rollout

### Explicitly ready now

These six venues have complete exact-date naming periods documented in `docs/historical-venue-single-name-chronology.md` and require no identity merge or alias relocation to publish their date-aware naming history.

#### VEN-000015 — AT&T Stadium

- Cowboys Stadium: 2009-05-13 through 2013-07-24
- AT&T Stadium: 2013-07-25 onward

#### VEN-000135 — Michelob ULTRA Arena

- Mandalay Bay Events Center: 1999-04-10 through 2021-02-10
- Michelob ULTRA Arena: 2021-02-11 onward

#### VEN-000228 — Casey's Center lineage

- Wells Fargo Arena: 2005-07-12 through 2025-06-30
- Casey's Center: 2025-07-01 onward

The current protected-main `PROJECT_DISPLAY` remains Wells Fargo Arena. Under the controlling display contract, the latest open-ended official period supplies current aggregate display after migration; a project-display rewrite is not required merely to publish the periods.

#### VEN-000686 — Bankoh Arena at Stan Sheriff Center lineage

- Special Events Arena: 1994-10-21 through 1998-02-19
- Stan Sheriff Center: 1998-02-20 through 2020-11-11
- SimpliFi Arena at Stan Sheriff Center: 2020-11-12 through 2025-08-25
- Bankoh Arena at Stan Sheriff Center: 2025-08-26 onward

The current protected-main `PROJECT_DISPLAY` is Special Events Arena. Preserve it as stable registry/fallback identity unless a separately justified registry-display change is needed; date-aware and aggregate site display should use the official-period contract.

#### VEN-000698 — Hilliard Center Arena lineage

- American Bank Center Arena: 2004-05-20 through 2025-08-31
- Hilliard Center Arena: 2025-09-01 onward

Physical-scope correction is settled: Bayfront Plaza Convention Center was the older adjacent convention-center complex and is **not** a predecessor arena naming period.

The current protected-main `PROJECT_DISPLAY` is American Bank Center. Preserve it unless a separately justified registry-display mutation is needed.

#### VEN-000714 — Coca-Cola Coliseum lineage

- Coliseum Arena: 1922-04-04 through 2003-10-31
- Ricoh Coliseum: 2003-11-01 through 2018-07-10
- Coca-Cola Coliseum: 2018-07-11 onward

### Recommended first maintenance tranche

**Rollout tranche 2 should contain exactly these six venues.**

Why:

1. every naming period has an exact supported `valid_from`;
2. every closed period has an exact inclusive `valid_to`;
3. all six are already-established physical `venue_id` identities;
4. none requires duplicate-ID merge, alias relocation, or canonical-game mutation;
5. the existing production feature already supports the required date-aware display;
6. this is one homogeneous transaction family that can be validated by exact venue-ID/period diff.

Expected declared mutation surface:

- add only the approved `OFFICIAL_NAMING_PERIOD` rows in `data/reference/venue-names.csv`;
- run `python tools/build_site_data.py --apply`;
- accept only the deterministic generated naming-period/site outputs reported by the builder;
- run `python tools/check_site_data_freshness.py` and the historical venue-name regression tests;
- verify the actual diff contains no venue identity, canonical game, H/A/N, score, school venue, or unrelated shared-reference mutation.

The prior Colorado/Syracuse rollout is the procedural model. Feature code does not need to be redesigned for this tranche.

## Mutation family B — exact-date residual verification

Eight single-name candidates have settled same-building chronology but at least one exact boundary remains unsupported:

- `VEN-000089` — Indiana State Fairgrounds / Pepsi / Indiana Farmers / Corteva Coliseum
- `VEN-000244` — Tupelo Coliseum / BancorpSouth / Cadence / Huntington lineage
- `VEN-000450` — Shanghai World Expo Cultural Center → Mercedes-Benz Arena
- `VEN-000596` — DeSoto Civic Center → Landers Center
- `VEN-000607` — RIMAC Arena → LionTree Arena
- `VEN-000641` — Tri-Cities Coliseum → Three Rivers Coliseum → Toyota Center
- `VEN-000642` — Bank of America Centre → Qwest Arena → CenturyLink Arena → Idaho Central Arena
- `VEN-000675` — The Bank of Kentucky Center → BB&T Arena → Truist Arena

These are **not** an open-ended research queue.

Attempt missing-date recovery only in a separately bounded verification unit when the venue is materially being considered for rollout. If the obvious authoritative path still does not supply the missing day, preserve the chronology and uncertainty rather than manufacturing a boundary.

## Mutation family C — legacy multi-name periodization readiness

The historical multi-name census contains **160** additional `PERIODIZE` rows beyond the three already migrated venues.

The census disposition itself is historical authority for the rename conclusion, but it is **not equivalent to implementation-ready exact periods**.

A conservative mechanical readiness triage of those 160 rows finds:

- **9** rows containing at least one exact YYYY-MM-DD boundary and no explicit date-verification marker in the ledger text:
  - `VEN-000038`
  - `VEN-000499`
  - `VEN-000503`
  - `VEN-000557`
  - `VEN-000778`
  - `VEN-000781`
  - `VEN-000823`
  - `VEN-000860`
  - `VEN-000863`
- **151** rows that either explicitly retain exact-date/wording verification debt or do not serialize any exact date in the census row.

The nine-row group is only a **high-yield readiness-review shortlist**, not `PERIODIZE_READY`. Several still lack an exact first-period `valid_from` or have closure/reopening semantics to reconcile. Do not migrate them from this heuristic alone.

After the six-venue first rollout, the next research unit should be one bounded exact-boundary audit of this nine-row shortlist, not a sweep of all 160.

## Mutation family D — resolved shared physical identity / alias topology

Three work items are historically settled but require dedicated global maintenance:

### Seattle — VEN-000102 / VEN-000315

- one physical Seattle Center arena lineage;
- preserve `VEN-000102`;
- retire duplicate `VEN-000315`;
- five published school venue rows currently reference the duplicate;
- no canonical-game/assertion/NCAA-site rows currently use `VEN-000315`.

This topology fits the existing sealed duplicate-ID merge transaction in `tools/venue_identity_transaction.py`.

### Nielsen / Smith — VEN-000382 / VEN-000582

- Smith Fieldhouse, Provo = `VEN-000382`;
- Einar Nielsen Fieldhouse, Salt Lake City = `VEN-000582`;
- remove the false Nielsen alias from the Smith identity and corresponding published-school local mapping;
- preserve literal source provenance.

This is **not** a duplicate-ID merge.

### Rice — VEN-000554 / VEN-000564

- `VEN-000554` is the 1950 Rice Gymnasium → Tudor Fieldhouse building; Autry Court is its competition-space name;
- remove `Rice Field House` from `VEN-000554`;
- correct `VEN-000564` to the old pre-1950 Rice Field House physical identity;
- preserve the accepted 1947 source-literal `Rice Gymnasium` wording as scoped provenance, not an unrestricted alias.

This is **not** a duplicate-ID merge.

### Tooling implication

Do not hand-edit Nielsen/Smith or Rice merely because the current merge transaction does not cover them.

Before that maintenance family begins:

1. inventory the exact alias/identity-correction topology;
2. determine whether one small generic intent-constrained correction transaction can cover both;
3. regression-test it;
4. keep Seattle's merge operation separately constrained even if executed in the same overall maintenance program.

## Mutation family E — canonical/alias cleanup

Four census rows are historically settled canonical corrections:

- `VEN-000160` — Patten, not Patton; preserve distinct 1909 and replacement Patten buildings
- `VEN-000324` — Robins Center, not Robbins Center
- `VEN-000371` — Eugenio Guerra Sports Complex; erroneous Eugene alias cleanup
- `VEN-000683` — duplicate literal Orange County Civic Center name row cleanup

These changes do not belong in the six-venue naming-period rollout. They may be considered with the generic non-merge alias/canonical correction maintenance capability after its transaction shape is defined.

## Terminal research-exhausted residuals

Do not reopen during rollout planning:

- `VEN-000234` — Worcester Centrum / Centrum Centre / DCU exact-boundary uncertainty
- `VEN-000396` — Houston Public School / Jeppesen Fieldhouse exact-boundary uncertainty
- `VEN-000439` — Rutgers Highland Park Gym / Masonic Hall equivalence not established

Owner accepted all three as `RESEARCH_EXHAUSTED`.

## Rollout order recommended by Control Center

1. **Naming-period Rollout Tranche 2:** the six exact-ready single-name venues only.
2. Production proof and checkpoint.
3. **Bounded nine-row legacy readiness audit:** determine which of the mechanically high-yield legacy `PERIODIZE` rows truly have complete exact periods.
4. Form the next naming-period rollout only from rows that pass that audit.
5. Separately plan the **shared identity/alias correction transaction family** for Seattle, Nielsen/Smith, Rice, and compatible canonical/alias cleanup.
6. Leave the eight single-name partials and the remaining legacy date-verification population alone unless a later rollout need justifies a bounded exact-date pass.

## Stop condition

This consolidation does not authorize step 1 automatically.

The next owner `Proceed` should authorize preparation/execution of the six-venue **naming-period Rollout Tranche 2** maintenance workflow only. It does not authorize the identity/alias cleanup family, the nine-row readiness audit, or any broad exact-date research campaign.
