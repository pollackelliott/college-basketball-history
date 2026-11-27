# San Diego State — Stage 1 checkpoint 0021: merged auditor, bounded archival access outcome

## Exact authority and immutable population
- Protected main: `a11cccf944492e4d968edbeef4111ebad150fcec`, protected.
- Same Research lane parent commit: `4e3d64907cc4a18d58209db7148a34ba96ecb760`; inherited research base remains `5b840a354fb5cd792239ff8b93cba223a18dd87a`.
- Parent checkpoint `0020-1922-yearbook-source-family-corroboration` independently reverified: 4/4 manifest member SHA-256 digests and byte lengths match.
- No accepted or excluded historical game-row change. Of the 1,126 printed named source outcomes, 1,086 are accepted competitive (1,043 regular season, 43 postseason) and 40 are excluded; zero identified inclusion/game-type holds. Three explicit unnamed 1921–22 outcomes remain outside game identities. Two 1921–22 awarded forfeits remain nonplayed administrative record adjustments.
- Founding primary source literal note retained exactly as previously authenticated: `1 win, 2 losses vs. unknown teams. Forfeit wins vs. Riverside & Fullerton JC.`; guide printed p.88 / PDF p.90, original PDF SHA-256 `9c63066b60365d4f90abdb36242bf880f84b87030f87d776a6f81fbc75b9f2ad`.

## Permanent tooling repair completed independently of Research
- Generic fail-closed auditor PR https://github.com/pollackelliott/college-basketball-history/pull/730 merged with all applicable exact-head tests/checks passing. Exact protected-main squash commit `a11cccf944492e4d968edbeef4111ebad150fcec`, one parent `3f5a15458aa468347e56e669327d6fe4c9c6ee69`; two changed files and their tested blobs independently reverified.
- `tools/research_stage1_coverage_gap.py` Git blob `0f77c191c36576bfd30b86592554d6ea76d965ac`; regression test Git blob `b0814f4ad496df59817b6cfc43434505cc1dbdac`.
- New permanent capability parses explicit counted unknown-opponent outcomes, without inferring games from aggregates, and supports itemized source-listed exclusions with ID/opponent/reason and fail-closed count/overlap checks.
- Research Stage 1 is not automatically closed by this generic repair.

## Bounded evidence investigation since 0020
- SDSU Library documents digital 1913+ student newspaper issues and explicitly includes the 1921–25 *Paper Lantern*: https://sdsulibrary.wordpress.com/2013/09/12/extra-extra-read-all-about-it/ ; https://www.sdsu.edu/news/2013/03/the-daily-aztec-celebrates-100-years .
- Attempted direct historical viewer `https://ibase.sdsu.edu/index.php?a=ViewItem&i=21` redirected to `https://digitalcollections.sdsu.edu/?a=ViewItem&i=21`, which the web access path rejected. The alternate `https://digitalcollections.sdsu.edu/the-daily-aztec` returned 403. **No individual 1921–22 issue read; no source-exhaustion credit claimed.**
- Targeted distinct reciprocal searches for 1921–22 Chaffey, Santa Ana and Pomona institutional basketball returns did not surface authenticated 1921–22 school-side game logs. Indexed secondary Mcubed https://mcubed.net/ncaab/yearly/sandst/1922.shtml reprints the 17 known results and reports 1 unknown W, 2 unknown L; its independence from the SDSU records is unestablished. No previously unknown opponent identified. Pomona institutional archive description https://www.pomona.edu/administration/archives/collections/collection-descriptions identifies historic publications but no season-specific 1921–22 result examined.
- The contemporaneous *Del Sudoeste* yearbook OCR corroboration in checkpoint 0020 remains source-level arithmetic only (20 played / 12W 8L); original institutional scan and full newspaper issues were not inspected.
- Fontius thesis remains bibliographic, not read. Do not treat sources' **existence**, search-result summaries, or viewer failures as equivalent to full original issue inspection or genuine source-exhaustion certification.

## Precise Stage 1 audit boundary
Auditor execution requires a SHA-256-pinned **full** stage1 checkpoint ZIP: `stage1-manifest.json`, `structured-stage1-ledger.csv` (1,086 accepted rows with literal opponents and game types), `season-census.csv` (all 49 seasons), `blocking-residuals.json` (only the exact 1921–22 explicit source-coverage blocker), `stage1-status.json` and manifested research-exhaustion evidence. The manifest must exactly bind all member hashes/byte lengths; every counted excluded founding source row must be preserved as an itemized excluded row distinct from the accepted 14. Build strictly from authenticated source ledgers and checkpoint 0018/0019/0020 lineage, not from secondary totals or invented game identities.

Currently **no complete audit ZIP exists, no SHA-pinned permanent audit has been run, and `RESEARCH_EXHAUSTED_IDENTITIES_UNRESOLVED` cannot be asserted** because the obvious original issue/independent archival paths remain uninspected. Do not fabricate eligible output, Stage 1 COMPLETE, Stage 2 authority, or any anonymous game rows.

## Next bounded permissible unit
Work one feasible original archival access route or directly inspect independently retrievable original season-level opponent records; if still inaccessible, preserve the exact factual limit and use that honest status in a deterministic **FAIL/noneligible** audit-input rehearsal rather than self-certifying exhaustion. Construct a provenance-backed full ledger/census/manifest only from accepted Git checkpoint files. Do not reopen accepted historical decisions, repeat web searches indefinitely, or begin Stage 2.
