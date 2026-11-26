# Fresno State ALL_HISTORY_EXPANSION — Stage 1 reciprocal repair checkpoint 0005

**Status:** BOUNDED_RECIPROCAL_AND_OPPONENT_REPAIR; **STAGE 1 OPEN**. This checkpoint is not Stage 1 COMPLETE, not a Research Freeze, and not an authorization to modify published Fresno State history.

## Authority
- Immutable `research_base_sha`: `087ac5dedc65780b65b7ae8d61e239d2033e2eea`.
- Exact parent Research commit: `ae4f6bb55324b706003b3672c0bc220d4b333ec5` (checkpoint 0004).
- Source-level year-by-year literal Fresno State 2025 guide remains immutable in checkpoint 0001 (PDF SHA-256 `b960369400bb42be27caa0331a1be2c9defd1e9163e4ea14f567c38e262693ba`).
- 1,034 source entries still preserved in exactly one derived ledger, 956 newly minted candidate source IDs and 78 original Research IDs preserved as separate prior-owner-excluded evidence. The 1,708 published 1970+ game rows and original 1970–71+ owner scope are untouched.

## 1. UC Davis 1922–23: one source duplicate resolved, season accounting still open
Fresno 2025 guide lists `UC Davis L 30-17` twice, plus `UC Davis W 45-15` once. UC Davis's 2025 institutional year-by-year schedule has exactly two Fresno games in 1922–23: Davis `W 30-17` once and Davis `L 15-42` once. UC Davis's own older 2019 all-time Fresno series has Davis `W 30-17` once and `L 15-45` once. Fresno's 2017 institutional series also lists only these two result identities, reporting the Fresno win `45-15`.

Accordingly, `FRESNO-EXP-CAND-1922-23-010` and `...-015` share one real-game provisional identity group, with the second marked duplicate *source representation*, not a second game. The Fresno win's score has an explicit UC Davis 2025 `42-15` versus other institutional `45-15` contradiction; keep the original Fresno `45-15` literal without silently adjudicating this secondary score variant.

The 1922–23 Fresno guide's 21 result entries now represent **20 provisional game groups**, group W14 L6 versus official headline 14–7. Do **not** fabricate an unidentified loss, erase a legitimate other game, or automatically rewrite the season aggregate. Additional exact season-coverage research remains required.

## 2. UC Davis 1926–27: opponent source conflict preserved
Fresno 2025 guide has four UC Davis W results: `31-18`, `25-13`, `31-14`, `31-18`. Its 2017 all-time UC Davis series repeats all four. UC Davis's 2025 official year-by-year records instead list **two** Fresno State losses with N/A scores. Its 2019 all-time Fresno series lists **five** losses in this season (`17-43`, `18-31`, `13-25`, `14-31`, `18-31`), but `17-43` repeats a result already present in 1925–26 and `18-31` is duplicated. These are contradictory institutional evidence representations; historical reality may be fewer than four, but the precise two-versus-four source identity mapping is **not independently established**.

Preserve all four Fresno result source entries as distinct *provisional* group keys, mark a typed real-game count conflict, and do not remove or automatically merge the identical `31-18` lines without contemporaneous evidence. In particular the old 2019 Davis all-time series cannot be treated as five independent proven 1926–27 games.

## 3. San Diego vs San Diego State 1965–66: opponent identity corrected
The 2025 Fresno guide's `San Diego State W 67-63` label is materially contradicted by **Fresno State's own 2016–17, 2017–18, and 2018–19 historical opponent series**, which list `1965-66 Fresno State W 67-63` under `SAN DIEGO` (University of San Diego), *not* the adjacent separate `SAN DIEGO STATE` series. The later 2023–24 Fresno dated SDSU series contains exactly two dated 1965–66 SDSU entries: Fresno W86-49 on January 14, 1966, and Fresno L66-69 on February 18, 1966. Retain the 2025 literal unchanged, set researched opponent to **San Diego (University of San Diego)** for source ID `FRESNO-EXP-CAND-1965-66-026`, no exact game date invented.

The twice-listed `at San Diego State L 69-66` remains one dated real-game provisional group as already repaired by checkpoint 0004. After collapsing that one duplicated *loss source representation*, 1965–66 has **28 provisional result groups W22–L6**, still in disagreement with 21–8 institutional headline. Changing the opponent label W67-63 does not fix this season-count conflict. No replacement losses were created.

## Durable members
- `complete-source-identity-ledger.csv`: all 1,034 rows reserialized, original literals preserved, exact amended identity group/status and explicit researched-opponent fields for the limited 8-row repair population.
- `accepted-repair-deltas.csv`: exact original-vs-successor statuses and ids, limited 8 row changes.
- `source-families.csv`: six exact URLs and scoped factual evidentiary limitations; target institutional and reciprocal evidence distinguished.
- `remaining-family-queue.csv`: five focused repair or residual families; superseded material queue points to parent for other pending classes.
- `reconciliation-audit.json`: all counts, parent, Research base, and nonacceptance scope.
- This README.

## Remaining Stage 1 blockers and safe stop
The previously preserved 0004 queue continues for other classes, including exhibitions, intra-program games and 1943–44 wartime activity. This unit specifically refines the three opponent families. **Next bounded historical pass** should prioritize determining the 1926–27 actual game population using independent dated newspaper/yearbook evidence and establishing whether 1922–23 has a missing different game, rather than cyclically revisiting both guide score strings. 1965–66's remaining on-court record mismatch stays independently queued for later coherent season-level primary-source reconciliation. Stop at Stage 1; do not start Stage 2, any Implementation lane, or mutate main.
