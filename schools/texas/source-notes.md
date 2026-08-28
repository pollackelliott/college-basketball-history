# Texas source notes

## Primary institutional source

**2025-26 Texas Basketball Fact Book**, University of Texas Athletics, owner-supplied PDF.

- SHA-256: `07b1a76662e472eb738d45f550de91bdb228b7f55172cac16b2356fa5d55613a`
- Year-by-Year Results: printed pages 91-108
- Cross-check sections used: All-Time Series Records/Scores, home-court records, Southwest Conference history, Big 12 history, SEC history, NCAA Tournament history, NIT history, SWC Tournament history, Big 12 Championship history, SEC Tournament history, and overtime/program-history material
- Historical coverage: program inception through completed 2024-25 season

The Year-by-Year Results ledger is the backbone of the historical game package. Literal row wording is retained in `raw_text`; structured corrections do not rewrite the source claim.

The fact book reports the 2024-25 endpoint as **1,918-1,158** and identifies 1906 as the first year of basketball. Its program notebook reports 39 NCAA appearances with a 40-42 NCAA record through 2025 and five NIT appearances with an 11-3 record.

## Completed 2025-26 supplement

Texas Athletics official completed 2025-26 schedule/results:
https://texaslonghorns.com/sports/mens-basketball/schedule/2025-26

It supplies **36 competitive games and a 21-15 record**. The package uses the completed results rather than the preseason schedule printed in the fact book. The 2026 postseason consists of the SEC Tournament loss to Ole Miss and an NCAA run through NC State (First Four), BYU (R64), Gonzaga (R32), and Purdue (Sweet Sixteen).

Representative official 2026 game/site evidence:
- Texas-Purdue Sweet Sixteen box score / Texas Athletics game record: https://texaslonghorns.com/sports/mens-basketball/stats/2025-26/purdue/boxscore
- NCAA Tournament site research was cross-checked to official NCAA championship/site records and established project physical venue identities.

## Owner-authorized conference tournament site reference

Owner-supplied workbook: **`Conference_Tournament_Site_Reference(20260825-203322).xlsm`**.

- SHA-256: `68fd42a5da4e2a908a9911c5812fda317920e1842b5518ebba52d20cdd2b26e2`
- Owner ruling: the workbook is globally incomplete, but its Texas-relevant **Southwest Conference, Big 12, and SEC sections are complete and reliable for Texas**.
- Use in this package: conference-tournament physical venue/city/state assignments, including campus preliminary rounds and centralized shared-site eras.
- Explicit limitation: unfinished sections are not promoted to universal project canon.

## Source-internal correction hierarchy

When the Year-by-Year Results row conflicts with a dedicated Texas postseason table, the package assesses the conflict game-by-game and retains the literal chronological row in `raw_text`.

Material cases:
- 1979 and 1980 SWC Arkansas tournament scores are normalized from the dedicated SWC Tournament table.
- 1995 Rice SWC semifinal is normalized to 78-75 from the dedicated tournament table.
- 1998 Oklahoma State Big 12 quarterfinal retains the chronological 65-64 where the dedicated summary prints 65-62; the disagreement remains documented.
- The 1918 Texas A&M row is interpreted under the project's on-court result policy: 7-8 played loss plus separate forfeit metadata.

## Historical exact-date limitations

Texas explicitly states that dates are unavailable for nine 1924-25 Dallas holiday games, one 1930-31 St. Edward's game, and two 1939-40 Kilgore Pipeliners games. Those remain blank. The impossible 1910 Feb. 29 entry and three internally contradictory 1912-13 January rows also remain blank rather than being silently corrected.

## Home-facility evidence

Texas fact-book historical notes establish:
- first program game at Clark Field on 1906-03-10;
- first indoor home game at Ben Hur Temple on 1913-01-13;
- Men's Gym constructed adjacent to Clark Field in 1917 as the temporary basketball home;
- Gregory Gym opened 1930-12-05 and hosted the 1977 SWC first-round Baylor game, the final game of its primary era;
- Frank Erwin Center opened for Texas basketball 1977-11-29 and closed its Texas home era 2022-02-28;
- Moody Center is the current home beginning in 2022-23.

These facilities enrich only games already independently classified as Texas home.

## NCAA physical-site research

All NCAA Tournament rows have physical building identity plus city/state. The package normalizes naming-rights aliases to one physical identity where appropriate, including Civic Arena -> Mellon Arena, RCA Dome -> Hoosier Dome, Carrier Dome -> JMA Wireless Dome, FleetCenter -> TD Garden, Louisiana Superdome -> Caesars Superdome, New Orleans Arena -> Smoothie King Center, Alltel Arena -> Simmons Bank Arena, Chesapeake/Ford Center -> Paycom Center, Sprint Center -> T-Mobile Center, and PeoplesBank Arena -> XL Center.

Historical NCAA consolation/third-place contests remain NCAA Tournament games with blank curated round when no honest controlled label applies.

## Opponent normalization sources

Texas's All-Time Series Records and All-Time Scores vs. Opponents sections were used as an internal identity/series cross-check. Institutional lineage was additionally researched where a historical source label clearly maps to a modern program. Ambiguous local/club identities are preserved as distinct historical opponents rather than guessed.

## Research baseline

`research_base_sha=a05ad97f1023dae8f277c805c9598ecb5caa319c`

Repository schemas, current reference identities, and onboarding hardening rules were inspected against that baseline. Research-time venue identities remain provisional until serialized current-main rebase.
