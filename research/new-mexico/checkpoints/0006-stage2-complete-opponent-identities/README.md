# New Mexico original-school Research — Stage 2 COMPLETE (checkpoint 0006)

**STAGE_2_COMPLETE.** Ordinary complete-institutional Research, NOT Implementation or All-History Expansion.

- Research branch: `research/new-mexico`.
- Protected main / immutable research_base_sha: `242370fc551fd749c157c74d92917ddfafbe40e0`.
- Previous verified Stage 2 checkpoint 0005 HEAD: `fbfa4aa52c8f97cb529f9ae05e22d9849d714e43`.
- Stage 1 COMPLETE accepted 0004 HEAD: `e3b4c945ad3793b93f79e639099b5961c6ee4e7f`.
- Owner-final top-level scope: **INCEPTION+**, varsity inception 1899–00; primary source cutoff and required completed-season cutoff 2025–26.
- Official UNM 2026–27 media guide/record book original SHA-256: `94a121232efa82a71ebb448139d4e72c799ac032128cb625ce2a5178b6bbdcc7`.

## Closeout population and checks

- **2,891** accepted played games, 2,891 immutable Stage 1 source game IDs, zero duplicates, and **zero Stage 1 field-value differences**.
- **986** distinct literal source opponent labels, each with accepted source-label→canonical-key/display-name/current-D1 mapping and first/last-season/game-count provenance.
- **339** distinct research-local canonical opponent keys; **2,518** game opponents currently D-I in research-base `data/reference/programs.csv` and **373** historical/non-current-D-I game opponents. Every `current_d1=Yes` key matched protected-main immutable registry; no `current_d1=No` key collides with that registry.
- **Zero unresolved opponent identity rows.** Source annotations, brackets/rank, tournament/event tokens, source H/A/N, game type and all literal score evidence remain in the row-level ledger.
- Every one of the 986 mapping counts sums to the 2,891 played-game count. No blanket fuzzy-identity merges were applied.

## Sources and non-D1 historical distinctions

The high-volume non-D1 population was classified using UNM's official historical opponent results, accepted protected-main school opponent capsules, and bounded institutional checks. New Mexico Mines→New Mexico Tech, U.S. International→USIU, Regis→Regis (Denver), military/service/bank/high-school teams each preserve distinct identities. The separate 1930s Harlem Globetrotters inclusion decision belongs to accepted Stage 1 and was not reopened.

Four last exact-game residuals were settled without conjecture:
1. `NM-1946-47-0019`, `vs. Hamline 1 NAIA`: canonical Hamline University (`hamline`), with NAIA classification/round token retained as source annotation.
2. `NM-1953-54-0005` and `0006`, source `Phillips`: University of New Mexico 2013–14 official historical year-by-year and opponent-series tables independently identify `Phillips Univ.`/Phillips University on December 29 and 30, 1953 (69–67, 64–38). Accepted canonical key `phillips`, *not* `phillips-66-oilers`.
3. `NM-2010-11-0004`, source `Northwood`: November 24, 2010 UNM game box lists Darvin Ham, Cameron Joyce and Booker Stoudmire; exact 2010–11 Northwood (Michigan) roster and independent GLIAC opponent box score corroborate. Canonical `northwood-michigan`; **not** the former Florida/Texas campuses.

Provenance and unresolved competing-key warning for Regis (`regis-colorado`) and U.S. International (`us-international`) remain auditable in the 0005/0006 evidence and row-level notes; research-local non-current identities are **not** globally registered merely by Research.

## Durable files and stage boundary

- `structured-stage2-ledger.csv`: complete 2,891-game ledger carrying every Stage 1 source field, accepted opponent identity and field-level provenance.
- `opponents.csv`: byte-identical checkpoint copy of the package-ready accepted `research/new-mexico/stage4-authoring/opponents.csv` authoring capsule.
- `identity-closeout-evidence.csv`: exact remaining three distinct source labels / four rows and authoritative URLs.
- `stage2-residuals.csv`: empty-body header-only identity residual queue.
- `stage2-status.json`: machine-readable closure facts, classification counts, next bounded stage.
- `manifest.json`: byte-length and immutable Git blob hashes of every checkpoint/capsule artifact.

**Safe stop:** Stage 2 is COMPLETE. Stage 3A is **not started**. No protected-main, existing school, shared/global registry, Implementation mutation lock, or accepted Stage 1 field was edited. NON_D1 owner sanity scan is required later before Research Freeze, after substantive identity research, not manufactured at this internal boundary.

Next owner `Proceed` opens one bounded Stage 3A regular-season census/site unit under current repository rules.
