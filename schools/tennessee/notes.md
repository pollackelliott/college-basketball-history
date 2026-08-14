# Tennessee curation notes

## 1. Program status and coverage

Tennessee is curated from its first recognized varsity season, 1908-09, through the completed 2025-26 season. The package contains **2,952 recognized non-exhibition varsity games**. The record book lists no team in 1943-44; no synthetic rows are created.

## 2. Canonical competitive game count and on-court record

The package contains **2,952 games: 1,827-1,123-2 on court**. The historical record-book extraction through 2024-25 contributes 2,915 games and, after the source-error correction described below, exactly **1,802-1,111-2**. The owner-supplied completed 2025-26 season contributes 37 games and a **25-12** record.

## 3. Exhibitions and canceled games

Explicit exhibitions are excluded: 1965-66 `Hi. Marines (Exh.)`, 1973-74 `Sub Pac (Exh.)`, and the owner-supplied 2025-26 Duke preseason exhibition. Canceled 2020-21 schedule entries are not games and are excluded.

## 4. Date and source exceptions

Exactly **3 games** remain without an exact date, all in 1921-22: Johnson Bible College, at Roanoke College, and at Washington & Lee. No date is inferred from row order. The 1929-30 Southern Conference Tournament row vs. VMI prints the impossible `F29`; the package uses **1930-02-28** and preserves the printed row in `raw_text`.

## 5. Home venue chronology and site policy

Owner-approved display chronology: UT YMCA Gymnasium (1908-09 through 1911-12), Knoxville YMCA Gymnasium (1912-13 through 1921-22), Jefferson Hall (1922-23 through its 1932-02-19 finale), Alumni Memorial Auditorium-Gymnasium (1932-12-17 through 1957-58), Armory-Fieldhouse (1958-12-02 through 1965-66), Stokely Athletics Center (1966-12-01 through 1986-87), and Thompson-Boling Arena (1987-12-03 onward).

Armory-Fieldhouse and Stokely are separate historical display eras for the same expanded/renamed physical facility. **Game-level site evidence remains authoritative; venue chronology never establishes site type.** A row already established as Tennessee home may receive the documented primary-home venue and Knoxville, Tennessee location.

## 6. Neutral, road, and hosted-postseason treatment

The Tennessee record book marks road games with `at` and many neutral games with `vs.`. Those explicit markers control. Unprefixed Knoxville games are treated as Tennessee home under the source's current-policy framing. SEC Tournament games held in Tennessee's actual home facility may therefore be home when Tennessee's own game-level presentation establishes them as such; this is intentionally allowed to surface cross-source discrepancies for reconciliation.

## 7. Conference history and championship metadata

Owner-authoritative membership chronology: SIAA through 1919-20, Southern Conference from 1920-21 through 1931-32, and SEC beginning 1932-33. Owner-authoritative program achievement totals for publication are **12 conference regular-season championships, 5 conference tournament championships, 0 Final Fours, and 0 national championships**.

## 8. Postseason taxonomy

SEC/SIAA/Southern tournament contests use `CONFERENCE_TOURNAMENT`; NCAA games use `NCAA_TOURNAMENT`; true postseason NIT games use `NIT`. Named in-season events and the 1974/1975 commissioner tournaments remain `REGULAR_SEASON` under the project's limited public taxonomy. SEC championship-game appearances are labeled `Championship`; NCAA public rounds use R64, R32, Sweet Sixteen, and Elite Eight where established. Tennessee has no Final Four appearance.

## 9. Known source correction

The 2024-25 year-by-year ledger prints the Houston Elite Eight row backward as `W, 69-50`. Tennessee's dedicated NCAA Tournament results and the published 30-8 season record establish the correct on-court result as **Tennessee L 50-69 Houston on 2025-03-30**. The package curates the correct result while preserving the printed source row in `raw_text`.

## 10. Vanderbilt source-marker correction

The 2009-01-20 source row prints `/- at Vanderbilt`. Initial normalization incorrectly treated the prefix as part of a historical opponent identity and created `at-vanderbilt`. On 2026-08-14 the owner confirmed that this is the valid Tennessee 76-63 win at Vanderbilt and is separate from Tennessee's 69-50 home win over Vanderbilt on 2009-02-14. `TENRAW-02350` is normalized to Vanderbilt with Vanderbilt home while preserving the printed source line in `raw_text`.

## 11. Opponent identity policy

Current Division-I identities reuse the project's established program-key conventions, including Miami (FL) = `miami`, Miami (OH) = `miami-oh`, UAB = `uab`, UCF = `ucf`, Chattanooga = `chattanooga`, Middle Tennessee = `middle-tennessee`, UT Martin = `ut-martin`, and UTEP for historical Texas Western. Historical clubs, YMCAs, military/prep teams, and non-current colleges are retained conservatively rather than forced into modern identities without evidence. Tennessee's own opponent-series table supplies several explicit historical lineage labels used here, including City College of Detroit -> Wayne State, Eastern Montana -> Montana State-Billings, Cumberland College -> Cumberlands (Ky.), and Mexico/Univ. of Mexico -> University of Mexico. Established project historical keys are reused for Union College (Ky.), Washington & Lee, and St. Francis Brooklyn.

## Package QA snapshot

- Games: 2,952
- On-court record: 1,827-1,123-2
- Historical through 2024-25: 2,915 games, 1,802-1,111-2
- 2025-26: 37 games, 25-12
- Blank exact dates: 3
- Distinct canonical opponent keys: 312
- Game types: {'REGULAR_SEASON': 2712, 'CONFERENCE_TOURNAMENT': 151, 'NIT': 26, 'NCAA_TOURNAMENT': 63}
- Conference-tournament championship-game rows: 14
- NCAA/public round counts: {'Championship': 14, 'Sweet Sixteen': 12, 'R64': 26, 'R32': 19, 'Elite Eight': 4}

## Tennessee ingestion reconciliation — 2026-08-10

- Initial ingestion produced 22 field-level discrepancies against existing canonical games.
- 21 were resolved during owner-approved cross-source review.
- DISC-000078 (Tennessee at Kentucky, 1910-02-16, Kentucky 26-5 vs. 20-5) remains UNDER_REVIEW because credible historical records conflict and no sufficiently persuasive evidence has yet broken the tie.
- Tennessee's curated overtime values were corrected for:
  - 1963-01-19 at Kentucky: 1OT.
  - 1978-03-04 at Florida: 3OT.
  The Tennessee chronological raw text omits those OT markers and remains preserved verbatim.
- Reconciliation also corrected two previously canonical Missouri site assignments:
  - 2013-03-09 Missouri at Tennessee.
  - 2014-03-08 Missouri at Tennessee.
  Both were played in Knoxville at Thompson-Boling Arena.
