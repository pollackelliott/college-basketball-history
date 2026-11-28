# New Mexico ordinary Research — Stage 2 checkpoint 0005

**State:** STAGE_2_IN_PROGRESS. This is a **bounded initial opponent-identity census and authoritative-reuse tranche**, NOT Stage 2 COMPLETE.

- Immutable research_base_sha: `242370fc551fd749c157c74d92917ddfafbe40e0` (protected main verified).
- Parent accepted Stage 1 COMPLETE commit: `e3b4c945ad3793b93f79e639099b5961c6ee4e7f`; exact source-game blob `63490b3398c94193da324911b1d002aafcac2d06`.
- School: `new-mexico`; inception `1899-00`, owner-final scope `INCEPTION+`, primary source results through `2025-26`.
- No mutation to protected main, global basketball/reference state, or existing accepted Stage 1 data.

## Exact population

- **2891** game-level rows, all Stage 1 literal fields intact and same research IDs / source sequence / game types / raw scores / W/L.
- **986** distinct raw source opponent labels, of which **822** have accepted identity mappings and **164** remain explicitly `RESEARCH_PENDING`.
- **2670** game rows mapped with safe authority; **221** game rows remain unmapped, grouped into **157** normalized roots.
- Registry and verified historical-name lookups bind to frozen `data/reference/programs.csv` blob `db9d85853c1d85fe27f84bdab94c3a812c23d630` and `program-names.csv` blob `e645609aacfb749ee201c41b9c3e5d364f6552cf`, not moving main.
- Source `at` / `vs.`, leading numbered brackets, ranking parentheses, and clearly identified round/event tokens are preserved in separate columns while only a safe opponent-name root is matched.
- Historical NON_D1 program cases use accepted published project opponent evidence or explicit institutional/NCAA evidence; provenance links and target-only provisional key state are in `documented-identity-families.csv`.

## Safety and recovery

- `structured-stage2-working-ledger.csv` is the full row-level working ledger; it carries Stage 1 source data byte-for-byte at field-value level with no H/A/N inference. Stage 1 is authoritative for inclusion/game types and is not reopened.
- `source-label-identity-census.csv` preserves every exact original opponent token with its own count, first/last season, accepted mapping or blank pending state, and note.
- `unresolved-identity-queue.csv` is the exact next-source-family population. Do not silently force `U.S. International` to either of the different accepted historical keys in other published packages; similarly hold `Regis` where accepted-key use diverges. No match from superficial name similarity.
- `stage2-status.json` holds counts, source mappings and named next unit. The existing `research/new-mexico/stage4-authoring/institutional-scope.json` remains unchanged.
- **Stage 2 is incomplete** until all game rows have accepted keys and the complete `stage4-authoring/opponents.csv` capsule has been authored and verified. No Stage 3/Implementation authority.

## Next bounded stage assignment

Apply accepted-project analogues to exact high-yield historical/NON_D1 roots and resolve the few competing alias/canonical-key questions with authoritative institutional evidence, then regenerate the full row-level mapping and exact unresolved queue. Prefer one coherent historical-source family rather than hundreds of ad-hoc searches.
