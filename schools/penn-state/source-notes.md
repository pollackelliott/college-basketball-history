# Penn State source notes

## Primary institutional source

**Penn State Men's Basketball 2025-26 Record Book**, Penn State Athletics Strategic Communications (owner-supplied PDF).

- SHA-256: `b8eb6bac0a1d408f8a531de3b14a1ea3dfc347f4c63c459fcb7e0b92c457ca5f`
- Historical ledger backbone: All-Time Results, printed pp. 134-158
- Cross-check sections: Series Game-by-Game, Year-by-Year Record, NCAA Tournament History, NIT Tournament History, Big Ten Tournament History, arena/facility history, and Notable Victories
- Historical coverage used here: program inception through completed 2024-25

The chronological All-Time Results ledger controls date/score/result unless a stronger game-specific institutional or archival source resolves a documented defect. The series tables are the primary H/A/N cross-check. Literal source strings remain in `raw_text` even when a curated field is corrected.

## 2025-26 completed-season supplement

Penn State Athletics official completed schedule/results:
https://gopsusports.com/sports/mens-basketball/schedule/season/2025-26

It supplies **32 competitive games** and a **12-20** record. Two games explicitly labeled exhibitions by Penn State — at Dayton on Oct. 19, 2025 and Shippensburg on Oct. 26, 2025 — are excluded from the competitive package.

## Owner-supplied conference-tournament site reference

File: `Conference_Tournament_Site_Reference(10).xlsm`

- SHA-256: `68fd42a5da4e2a908a9911c5812fda317920e1842b5518ebba52d20cdd2b26e2`
- Owner ruling: globally incomplete; Penn State-relevant information may be used affirmatively, but any missing Penn State tournament information must be treated as a workbook gap and independently researched.
- Big Ten: populated and used for 1998-2026 tournament venue/city/state assignments.
- Atlantic 10 / Eastern-era: the supplied file's relevant rows do not carry venue/city/state. Those blanks are **not** treated as negative evidence and are not promoted to project canon.
- The workbook's own safety rule is respected: tournament-site data supplies physical venue/location and does not infer H/A/N.

## Eastern Eight / Atlantic 10 tournament-site supplementation

Primary external league history used to reconstruct the workbook gaps:
https://static.atlantic10.com/pdfs/mbb/completemg.pdf

Penn State's own chronological ledger and tournament-history sections are cross-checked against the Atlantic 10 historical record. Campus-round sites are assigned only when game-specific evidence supports them; shared-site records do not fabricate campus venues.

Notable reconstructed Penn State sites include the Spectrum (1977), Pittsburgh Civic Arena/Mellon Arena (1978, 1983), Rutgers Athletic Center/Louis Brown Athletic Center (1979, 1985, 1989 final), WVU Coliseum (1984, 1988), Keaney Gymnasium and Saint Joseph's Alumni Memorial Fieldhouse (1986 campus rounds), Rec Hall (1987 and 1991 final), and the Palestra (1989-91 shared rounds).

## NCAA Tournament evidence

Penn State's dedicated NCAA Tournament History is cross-checked with established NCAA/archival site evidence. Project archival corrections already support, among other cases:

- 1942 New Orleans games — Tulane Gym
- 1952 Raleigh games — Reynolds Coliseum
- 1955 Evanston regional — McGaw Memorial Hall / current physical Welsh-Ryan Arena identity

Penn State source text is retained where it conflicts with the curated physical site.

For the 1955 first-round Memphis State game, Penn State's box score prints March 8 and Memphis archival program material also supports March 8:
https://digitalcommons.memphis.edu/speccoll-ua-ad-series2/77/

## NIT evidence

Penn State's dedicated NIT Tournament History establishes all 36 package NIT games, including the All-Time Results omission of the **2009-04-02 Baylor championship**. The same section identifies Madison Square Garden as the semifinal/final site in the relevant years and supports neutral classification for the 1995 Canisius third-place game.

## 1917-18 Carnegie Tech date anomaly

Penn State's All-Time Results prints `F 29 @ Carnegie Tech 54-30 W`, and a later Penn State Athletics article also describes the game as a Feb. 29, 1918 / "Leap Day" appearance. Because **1918 was not a leap year**, that exact date is impossible. No sufficiently authoritative source was found establishing a corrected calendar date. The package therefore preserves the game, score, opponent, and away designation while leaving `game_date` blank. This follows the project rule that UNKNOWN is preferable to unsupported certainty.

Penn State Athletics corroborating repetition of the impossible date:
https://gopsusports.com/news/2012/02/28/penn-state-at-purdue-wednesday

## Historical opponent-identity method

Current Division I programs use the research-baseline project key convention where established. Historical/local/military/YMCA/club opponents remain distinct source-based identities unless institutional lineage is secure. Examples of supported lineage normalization include:

- St. Thomas College (1935) -> University of Scranton lineage (`scranton`)
- Detroit -> Detroit Mercy
- Wayne -> Wayne State
- Western Maryland -> McDaniel
- Southwestern Louisiana -> Louisiana
- Southwest Texas State -> Texas State
- UMKC/Kansas City -> Kansas City
- Long Island -> LIU lineage

The 1903 printed `Indiana State` row is a documented source exception mapped to Indiana (Pa.) from Penn State's own series evidence. Later actual Indiana State games retain the Indiana State identity. No opponent key is unresolved.

## Home-facility evidence

Penn State's arena history establishes:

- The Armory: 1897-1928
- Rec Hall: 1929-1996
- Bryce Jordan Center: opened Jan. 11, 1996

Facility chronology is applied only after independent home classification and never used to infer H/A/N.

## Research baseline and portability

`research_base_sha=ced6a1e64d46c3be040b680b308bc070d22cff08`

Research-time venue IDs and the three new historical conference identities are provisional. The serialized Implementation lane must perform the authoritative current-main reference rebase before `INTEGRATION_FROZEN`.
