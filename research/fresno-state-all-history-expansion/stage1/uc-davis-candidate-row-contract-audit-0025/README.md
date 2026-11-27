# Fresno State ALL_HISTORY_EXPANSION — Stage 1 approved-UC-Davis candidate row-contract validation 0025

**Result: PASS — zero row-level/schema/partition errors in targeted independent audit. NOT a permanent Research Freeze validator run. STAGE 1 OPEN.**

## Exact authority
- Protected main at recovery: `5b840a354fb5cd792239ff8b93cba223a18dd87a`, protected, current AGENTS and applicable Stage1, Research convergence, expansion, portable execution and Stage4 authoring contracts read.
- Research parent checkpoint 0024: `9498f464076c51ef253f9d30b52b2ae79a486852`, exact tree `6d45bfceb542c76583e1628b3938f1247df1f5d6`.
- Immutable `research_base_sha=087ac5dedc65780b65b7ae8d61e239d2033e2eea`.
- All 11 exact previously committed input Git blobs independently re-fetched by SHA: see `audit-0025.json`. No predecessor bytes edited.

## Independent validation performed
A source- and accepted-game-level read-only audit re-parsed the **actual committed** checkpoint 0024 CSV bytes and their untouched 0013 parents, rather than relying on 0024's self-reported counts. It checked 20 substantive invariants with **zero errors**; evidence and test classifications appear in `validation-checks.csv`.

- **1,011 unique candidate accepted games**, all source-linked, with all **1,009 original game rows byte-for-field preserved**.
- **1,036 source representations** with distinct IDs: 933 accepted new (including 2 UC Davis) + 78 inherited + 17 excluded + 2 originally proven duplicate representations + 4 unassigned owner-approved Fresno score claims + 2 unaccepted Clowns.
- Exactly two new accepted candidate UC Davis identities: `FRESNO-EXP-RECIP-UCD-1926-27-04` and `...-05`; Davis source L, Fresno target W, with both exact score fields empty and no score-like source literal; source date absent. No fake score/venue.
- All four original Fresno UC Davis score claims preserved verbatim and only `stage1_identity_status` and `stage1_bulk_disposition` changed; **none is assigned to a particular Davis game or proven a specific duplicate**. All other 1,030 original source rows unchanged.
- **49/49 season counts** (games, W and L) recomputed from the candidate ledger and exactly matched the candidate census; all other **48 seasons unchanged**.
- **994 REGULAR_SEASON, 16 NCAA_TOURNAMENT, 1 POSTSEASON**. All populated source-side accepted scores consistent with on-court W/L/T; both UC Davis games score-unknown.
- Current candidate record over all supplemental years: **532 W / 479 L**, 1,011 accepted candidate identities. 1926–27 candidate: **18 games, 10–8**, separately retaining the older Fresno source aggregate **20 scored lines, 12–8**.
- The sole remaining pending-source-inclusion queue has **2** Clowns source groups. The unrelated 1965–66 one-loss aggregate and 1922–23 historical Bakersfield identity remain explicitly material outside that queue.

## Exact permanent-validator applicability boundary
Current protected-main `tools/onboarding_hardening.py:research_portfolio_report` validates a **completed, post-Stage3B six-file package** with opponent/venue/conference tables and Research coverage notes; it cannot be invoked honestly on a raw Stage 1 accepted/source/census candidate and cannot certify Stage1 completion here. `tools/research_stage4.py` needs Stage3B COMPLETE and its stage4-authoring capsule; `tools/expansion_implementation_stage1.py` needs RESEARCH_FROZEN and is an Implementation operation. The developer/user environment does not provide a local authenticated Git checkout for running the permanent Python tools; the local execution container cannot resolve github.com. No unsupported "permanent validator PASS" claim was made.

**Conclusion:** 0024 is now independently **row-contract validated** and retains its owner-approved historical meaning. This validation does **not** entitle the lane to declare `STAGE1 COMPLETE` or proceed to Stage2, nor does it require a generic tooling/schema mutation merely to force premature suite execution. The next substantial stage-level blockers are exactly the two Clowns game-inclusion decisions, the 1965–66 aggregate mismatch, and the 1922–23 anachronistic opponent identity; see `exact-remaining-stage1-classes.csv`.

## Members
- `validation-checks.csv`: 20 passed and 3 explicitly non-run/noneligible checks.
- `exact-remaining-stage1-classes.csv`: exact three still-material issue families plus approved UC Davis result.
- `audit-0025.json`: hash-bound input, counts, scope, explicit limitations.
- This README.

**No Research history rows, published school, global shared registries, protected main, or other Research stage was modified.** New durable files are additional audit metadata only.
