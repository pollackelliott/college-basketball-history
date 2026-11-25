# Gonzaga All-History expansion — independently audited 1909–30 Idaho reciprocal census

**Verification-only successor to original checkpoint (unchanged)**: The original narrative accidentally wrote 206 Gonzaga wins, but the verified 543-row ledger has 209 wins and 334 losses. This successor corrects that single narrative subtotal without changing any historical row or evidence. Parent research commit: `aa1b8d0a031d4ff7343ef00c06cd01730278e150`.


Protected main (fresh): `9bbe5d4ead518b37e5bd80810d20f1fe21d8dddd`
Gonzaga Research parent: `9256157de989486238ec366af2fa90e95fc5c17f`
Immutable research_base_sha: `f64ce23988faa04a304eb15d9ad96c2144ed5777`
Stage: **1 active**. Stage 2 not authorized.

## One bounded source family, 25 distinct games

The official University of Idaho **2024–25 men's basketball record book**, ALL-TIME RESULTS, contains source-explicit Gonzaga reciprocal rows in older 1909–30 seasons absent from the previously extracted 2025–26 Idaho source family, which started in 1933–34. We investigated the 1909-10 through 1929-30 window coherently and deduplicated against **all 518 existing Gonzaga game rows**, including other opponent families, not just the 39 already accepted Idaho games.

Original official record book: https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/govandals.com/documents/2024/7/26/MBB_Record_Book_24-25.pdf

Accepted **25** source-backed Idaho games (Gonzaga **7 W / 18 L**), 14 seasons, all regular-season; original 518 games retained byte-for-byte. The new controlling ledger has **543** unique game IDs. Site H/A is reciprocal of Idaho's explicit printed H/A, never inferred from city alone. Unknown score and dates remain blank.

## First source-backed identification for 1918–19

The previously empty 1918–19 identified-game population now includes Gonzaga at Idaho L 13–34, 1919-01-25; Idaho's year-by-year result prints W H 34–13.

## Year-by-year exact reconciliation

- **1909-10**: old 0-2/2; new +1 W, +0 L; now 1-2/3; official 11-3/14
- **1913-14**: old 2-1/3; new +1 W, +1 L; now 3-2/5; official 5-2/7
- **1916-17**: old 0-2/2; new +0 W, +1 L; now 0-3/3; official 4-5/9
- **1918-19**: old 0-0/0; new +0 W, +1 L; now 0-1/1; official 8-4/12
- **1920-21**: old 1-0/1; new +0 W, +2 L; now 1-2/3; official 4-8/12
- **1921-22**: old 0-9/9; new +0 W, +2 L; now 0-11/11; official 2-15/17
- **1922-23**: old 4-5/9; new +0 W, +1 L; now 4-6/10; official 10-8/18
- **1923-24**: old 1-6/7; new +0 W, +3 L; now 1-9/10; official 9-10/19
- **1924-25**: old 1-7/8; new +0 W, +2 L; now 1-9/10; official 9-12/21
- **1925-26**: old 5-3/8; new +1 W, +1 L; now 6-4/10; official 16-7/23
- **1926-27**: old 1-7/8; new +0 W, +2 L; now 1-9/10; official 8-16/24
- **1927-28**: old 4-7/11; new +0 W, +2 L; now 4-9/13; official 9-16/25
- **1928-29**: old 3-6/9; new +2 W, +0 L; now 5-6/11; official 14-12/26
- **1929-30**: old 6-7/13; new +2 W, +0 L; now 8-7/15; official 8-7/15 — **EXACT RECORD MATCH**

**1929–30** reaches a game-by-game exactly reconciled **8–7 / 15**, matching the season aggregate. This is a season-level finding only, not Stage 1 completion.

## Original 1928 field discrepancies preserved

- Idaho first 1927–28 game: 2024–25 official record book says Idaho W 28–15 on January 26, 1928. Contemporary *Idaho Argonaut* January 27 says Gonzaga game upcoming Saturday and March 2 final-season account confirms Idaho had defeated Gonzaga twice and gives the first game 25–18. Therefore game identity and Idaho W / Gonzaga L are accepted but date and both scores **UNKNOWN** (row IDAHOEARLY-020). Idaho H supported by original 'here' as reciprocal Gonzaga AWAY.
- Second 1927–28 game: both sources confirm Idaho W32–21 on February 29, 1928. *Argonaut* March 2 says game occurred **at Spokane**, conflicting with retrospective record-book Idaho H designation. Therefore Gonzaga **site UNKNOWN**; do not infer HOME from Spokane (row IDAHOEARLY-021).
- Original campus newspaper January 27: https://objects.lib.uidaho.edu/argonaut/pdf/arg-1928-01-27.pdf
- Original campus newspaper March 2: https://objects.lib.uidaho.edu/argonaut/pdf/arg-1928-03-02.pdf

## Exact preserved holds and scope

Six previous unadmitted classification/identity candidates remain unchanged: four 1942-43 wartime candidates, one 1957 Pacific Lutheran candidate, and 1926 Washington/Coliseum date conflict. Four parked accounting contradictions remain unchanged. 1930-31 and 1932-33 official Idaho source rows noted as future-census locators, not included in the single bounded 25-game tranche; 1930-31 already has a genuine source-accounting contradiction.

Official expansion aggregate remains **477 W – 500 L / 977 games**. Accepted identified games are now **209 W – 334 L / 543**. Difference 434 is *only arithmetic*, not identification of 434 missing individual games. Original historical inception 1907–08 and inherited 1958–59+ scope unchanged. No Stage 2, implementation, owner gate, global reference, or protected-main mutation occurred.
