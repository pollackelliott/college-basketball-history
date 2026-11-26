# Fresno State ALL_HISTORY_EXPANSION — Stage 1 1952–53 source-heading reconciliation checkpoint 0018

**Status: RESOLVED_NONBLOCKING_SOURCE_HEADING_ERROR for one earlier version's 1952–53 heading; STAGE 1 REMAINS OPEN for other previously identified material blockers. No game row or published data changed.**

## Exact authority
- Protected main at recovery: `31cccfdac5b676bde3f914c63e7239ef7cb132d5` (protected), parent Research commit: `02a779ab174d22f37dac4029cf31078848425efb`, parent tree: `cb36ea518937cfbd6ca878f4a4c692cbb36f4614`.
- Immutable `research_base_sha`: `087ac5dedc65780b65b7ae8d61e239d2033e2eea`.
- Accepted 1,009-game ledger at 0013: Git blob `19830f0e75fbd807371d946210c9660f1c4bcf4e` — untouched.
- Accepted 1,034-row source dispositions at 0013: Git blob `5ada1c5e75f54445577577c92d6576ebde56e811` — untouched.
- 49-season census at 0013: Git blob `4b120557181c5beaaed5911bc239b0c91dd9ea81` — untouched.
- Six blocked source groups at 0013: Git blob `485047f0a0806bc4407be334d8cbd7112aaf0f7b` — untouched.
- Official raw 2025 guide at 0001: Git blob `fc72b2862aa283481d498873af0a17fa1d7e405a` — untouched.
- Direct predecessor checkpoint 0017 remained authoritative for 1965–66; this unit did not reopen it.

## One bounded issue: the alleged 1952–53 W/L contradiction
Earlier checkpoint 0016 preserved issue `FS-S1-1952-53-RETROSPECTIVE-VERSION-RECORD`: Fresno's **2019–20 media supplement** year-by-year entry at *printed p. 30 / PDF index 28* says `1952-53 Record: 8-21`, while the newer 2025 guide says `10-19`.

This unit **visually inspected the original 2019–20 PDF** at the specified page. It contains exactly **29 individual game result rows**, and their printed opponents/W-L/scores **match the 29 original literal entries in the preserved 2025 guide in the same order** (29/29 exact row strings). Independent re-count of those individual rows gives **10 W, 19 L**, not the printed 8 W, 21 L.

Furthermore **the same 2019–20 supplement** prints coach Dutch Warmerdam's 1952–53 record **10–19** in its coaching-record table at *printed p. 27 / PDF index 25*. Fresno's November 3, 2019 official game notes also report 10–19 for Warmerdam in that season. Thus the 8–21 **heading** is inconsistent with both the game rows and separate institutional records within the same year.

The row-by-row crosswalk in `1952-53-29-row-source-crosswalk.csv` carries all 29 exact source literals, stable Research IDs, curated W/L and team-side scores, game types and unchanged inclusion. The 0013 ledger contains 29 accepted 1952–53 games (10–19), zero exclusions, zero source duplicates and no pending group in that season; all 29 accepted games are `REGULAR_SEASON`.

**Disposition:** `RESOLVED_NONBLOCKING_SOURCE_HEADING_ERROR`. Preserve the literal `8-21` as an older edition's erroneous source heading; preserve the **10–19 documented game result** as current accepted Stage 1 authority. There is no evidence for two extra losses, any W→L reversals, or additional game identities. Do not change accepted ledger, 49-season census, other source literals, or original IDs.

## Scope and stopping discipline
This resolves only the review trigger from 0016, not the Stage 1 game-universe/inclusion blockers:
- 1922–23 modern CSU Bakersfield referent historically impossible, actual 70–13 opponent still unknown;
- 1926–27 UC Davis four Fresno guide score lines vs two reciprocal games; four source groups remain unpaired;
- 1935–36 Broadway Clowns and 1953–54 Harlem Clowns: two individual exhibition-versus-competitive inclusion blockers;
- 1965–66: working game ledger 21–7 vs institutional 21–8, unmatched aggregate loss without source-explicit counted-gap eligibility;
- wartime and other preexisting field debt preserve exact earlier authorities.

**No Stage 2 authorization**. No source/game/canonical/published/shared mutations; Research branch changes contain only this new checkpoint's documentation, structured crosswalk, and audit files.

## Members
- `1952-53-29-row-source-crosswalk.csv`: complete 29-game exact same-order 2019–20 vs 2025 literals and accepted 0013 identities.
- `source-heading-adjudication.csv`: one exact trigger's conclusion and evidence arithmetic.
- `source-evidence-boundary.csv`: precise original PDF pages, official 2019 game notes, and Git lineage.
- `audit-0018.json`: exact no-change proof, acceptance arithmetic, manifest of inherited blob identities, and next work.
- This README.

**Next bounded Stage 1 unit:** seek a genuinely new readable match-specific contemporary source for a material pending inclusion/identity blocker; otherwise preserve hard research boundaries and assess whether repository policy requires an explicit owner historical disposition rather than repeating exhausted source paths.
