# Additive checkpoint 0009 recovery clarification

**Authority:** exact original completed checkpoint commit `299a6ee69f934d3418c33b3241c3c6c6f73b9fee` and immutable Research base `087ac5dedc65780b65b7ae8d61e239d2033e2eea`. This addendum is a non-mutating documentation correction; **all nine original checkpoint 0009 file blobs remain unchanged**.

## Clarification — mechanism-affected-seasons.csv has 22 data rows, not 20

- **20** seasons have one or more explicitly derived **source-to-provisional accounting mechanisms**: excluded intrasquad/exhibition source events, duplicate source representation, administrative forfeits, an inconsistent institution aggregate heading, or the 1943–44 no-result wartime status.
- **Two further seasons** are included in the same diagnostic file even though they have no such arithmetic mechanism: **1926–27**, because the four Fresno UC Davis source entries conflict with UC Davis's two-game reciprocal season inventory, and **1953–54**, because one Fresno–Harlem Clowns source event has still-unresolved match-specific exhibition inclusion.
- Therefore the file's **22** data rows equal `20 mechanism-tagged + 2 independently monitored game-identity`. It must **not** be interpreted as 22 known missing-game seasons.
- The underlying `season-census-recomputed.csv` still has **49** season rows, all with exact source/raw/exclusion/dedup/forfeit accounting, and `reconciliation-audit.json` correctly reports `mechanism_tagged_seasons: 20`.
- The count of actual final accepted competitive-game identities remains **unknown**: **1,015** means provisional non-exhibition source identity groups, not confirmed accepted real games.

No source game row, source ID, official historical aggregate, priority residual, prior 78 owner-excluded IDs, protected-main source or published Fresno State game has changed. Continue Stage 1 from this exact additive successor, maintaining original checkpoint 0009 bytes by their immutable Git blob IDs.
