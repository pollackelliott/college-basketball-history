# San Diego State — Stage 1 checkpoint 0020: 1922 yearbook source-family corroboration

## Authority
- Protected main authenticated: 3f5a15458aa468347e56e669327d6fe4c9c6ee69
- Parent Research HEAD: d28309c522be58ac373de2430fe210eabdda4cd2
- Immutable research_base_sha: 5b840a354fb5cd792239ff8b93cba223a18dd87a
- Controlling predecessor: checkpoint 0019, manifest and all five members independently SHA-256/byte-verified. Checkpoints 0018 (8/8 members) and 0009 (7/7 members) likewise verified.
- Stage 1 remains OPEN; historical dispositions and source ledger unchanged.

## Bounded new source-family result
The 1922 student-produced *Del Sudoeste* yearbook, printed pp. 76–77, is accessible here as a third-party OCR/transcription, not an authenticated institutional scan:
https://doczz.net/doc/5471938/del-sudoeste---sdsu-library-and-information-access

Its men's basketball narrative reports **20 games played, 12 wins and 8 losses** (and 585–335 points), calls out Santa Ana 27–16, Chaffey 15–20, Pomona 37–5, and a Fullerton forfeit. These three scorelines match the known SDSU official source-game ledger for 1921–22; the narrative is contemporaneous and from a different document class than the retrospective media guide. The original institutional-hosted yearbook scan was not accessible here, so the OCR mirror is useful corroboration but not scan-authenticated.

The original source's 17 named results contain exactly 11 W and 6 L, including three previously owner-excluded named outcomes (two Alumni at Stanford losses and one own-JV victory). Its literal separate note identifies 1 W and 2 L against unknown teams. Thus, purely as source outcome accounting:
- 17 named outcomes (11 W, 6 L) + 3 explicitly unnamed outcomes (1 W, 2 L) = 20 played outcomes (12 W, 8 L), matching the yearbook.
- Two nonplayed awarded forfeit W account for the subsequent 14–8 institutional heading.
- The 20 played source outcomes are NOT 20 accepted competitive canonical games: three identified results remain explicitly excluded and no unknown game identities were recovered.
- The yearbook's 585–335 points claim is preserved without synthesizing unknown scores or imposing an unsupported point-level reconciliation.

This independently strengthens founding-season season-level coverage accounting; it does **not** identify any unknown opponent or satisfy the mandatory two independently investigated archival/source paths.

## Auditor verification and boundary
Inspection of exact protected-main Git blob 48d2a085a32873ebf4d22c565fc138e72e03cdf8 at tools/research_stage1_coverage_gap.py confirms:
1. _count_missing requires a syntactic 'missing' clause, not the literal '1 win, 2 losses vs. unknown teams'.
2. SOURCE_LISTED_ROWS_MISMATCH compares listed_game_rows + recovered_count to accepted ledger row count, so 17 + 0 != 14 when three printed results are excluded.
These are generic fail-closed representation defects. No permanent audit ran, no runnable SHA-pinned ZIP was generated, no tests or PR were submitted, and no historical data were rewritten.

## Archival investigation not exhausted
The 1921–22 Paper Lantern issue set has been located via SDSU's published digital-newspaper descriptions, but specific game-season issues were **not inspected**. The original SDSU-hosted yearbook scan could not be retrieved through the accessed original ibase.sdsu.edu redirect. Fontius thesis text and reciprocal 1921–22 schedules were not independently recovered in this unit. Neither two complete independent source-family searches nor exhaustiveness are certified.

NEXT: independently inspect specific 1921–22 Paper Lantern issues and a distinct reciprocal/founding-season source family within a bounded pass; preserve unsuccessful access paths. Then repair both generic permanent-auditor defects coherently with positive/negative regression tests under same Stage 1 authority, and run the actual SHA-pinned permanent auditor. Do not enter Stage 2.
