# Vanderbilt curation notes

## 1. Program status and coverage

Vanderbilt is curated from its first recognized program season, 1900-01, through the completed 2025-26 season. The package contains **3,006 recognized non-exhibition varsity games**. The official ledger labels 1904-05 `No Team` and 1905-06 `No Schedule`; no synthetic rows are created for either season.

The owner-confirmed history boundary is 1900-01 with status `OWNER_CONFIRMED` and basis `ALWAYS_TOP_LEVEL_FROM_INCEPTION`.

## 2. Competitive game count and on-court record

The package contains **3,006 games: 1,724-1,282 on court**.

- Official fact-book evidence through 2024-25: **2,970 games, 1,697-1,273**.
- Completed 2025-26 official press-box schedule: **36 games, 27-9**.

The fact book is internally inconsistent at the aggregate level. Its season headers total 2,970 games, while its headline program-history record says 1,701-1,262 (2,963 games). The package retains the auditable game ledger and does not silently remove seven rows to force the headline aggregate.

## 3. The two 1954-55 series supplements

The chronological 1954-55 column prints only 20 rows even though its 16-6 season header requires 22. The same official fact book's opponent-series pages establish the two omitted wins:

- 1955-02-26, Florida, W 100-72, home.
- 1955-02-28, Georgia, W 78-57, home.

Those two rows use `official_2025_26_fact_book_series_supplement` as their source era. They are not inferred from the aggregate record.

## 4. Exhibitions, cancellations, and unplayed schedule entries

Explicit exhibitions and unplayed entries are excluded. This includes the 2019 Clark Atlanta exhibition, the canceled/postponed 2020-21 UConn, SMU, North Carolina Central, and Texas A&M entries, the canceled 2021 Stanford game, and the 2025 Virginia exhibition. Only played competitive games enter `source-games.csv`.

## 5. Date precision

Exactly **669 games** retain a blank exact date, principally early ledger rows for which the official season-by-season source prints only the season. No date is inferred from row order. Exact month/day tokens are converted using the season boundary, and separately supported exact dates are retained where available.

## 6. Source-row corrections retained with raw evidence

The package makes four narrow evidence-backed corrections while preserving every printed source line in `raw_text`:

- 1931-32 at/versus Kentucky: Vanderbilt's chronological row prints `at Kentucky ... W 37-61`. Kentucky's official record-book row establishes 1932-02-03, Kentucky 61-37 Vanderbilt, played at Vanderbilt. The curated Vanderbilt assertion is therefore L 37-61, Vanderbilt home.
- 1959-60 Ole Miss: the chronological row prints `L 66-58`; the same fact book's Ole Miss series row confirms Vanderbilt W 66-58 at home.
- 2015-16 Wichita State: PDF text extraction drops punctuation from `3.15`; the official postseason table establishes 2016-03-15.
- 1960-61 Kentucky in Knoxville: the season legend says `NCAA Tournament`, but Vanderbilt's dedicated NCAA results and appearance total exclude this pre-bracket playoff. It remains `REGULAR_SEASON` under the project's limited public taxonomy, with the source wording preserved.

## 7. Site and home-venue policy

The chronological ledger's explicit `at` and `vs.` markers control. Vanderbilt's official opponent-series table independently supplies H/A/N evidence for 2,621 historical rows; when the two official sections conflict, the game-level chronological marker controls and the raw evidence remains auditable. Unprefixed games are treated as Vanderbilt home only when no stronger series/event evidence contradicts that reading.

Owner-approved home-venue chronology:

- `Old Gym` for independently established Vanderbilt home games before 1952-12-06.
- `Memorial Gymnasium` beginning with Virginia on 1952-12-06 and continuing through the curated cutoff.

Venue chronology never establishes site type. It only supplies venue/location after a row has independently been classified as Vanderbilt home.

## 8. Conference history and championship metadata

Owner-authoritative membership chronology:

- SIAA: 1900-01 through 1920-21.
- Southern Conference: 1921-22 through 1931-32.
- SEC: 1932-33 onward.

Owner-authoritative accomplishment totals at the completed 2025-26 cutoff are **5 conference regular-season championships, 3 conference tournament championships, 17 NCAA Tournament appearances, 0 Final Fours, and 0 national championships**. Best NCAA finish is the 1965 Elite Eight.

The fact book labels 1918-19 `SIAA Champion` and 1919-20 `Southern Conference Champion`. The printed title wording is preserved as source evidence, but it does not override the owner-authoritative membership interval.

## 9. Postseason taxonomy

SIAA/Southern/SEC tournament contests use `CONFERENCE_TOURNAMENT`; NCAA bracket games use `NCAA_TOURNAMENT`; true postseason NIT games use `NIT`. Named in-season events, the Preseason NIT, and the NIT Season Tip-Off remain `REGULAR_SEASON`.

NCAA public rounds are normalized to Play-in, R64, R32, Sweet Sixteen, and Elite Eight where established by the official postseason table. The 1974 regional third-place consolation game retains its source round but has no unsupported public round. Conference/NIT title-game rows use `Championship`.

## 10. Opponent identity policy

Current Division-I opponents reuse `data/reference/programs.csv` identities. Established project aliases are reused where supported. Historical clubs, YMCAs, military/service teams, prep programs, and non-current colleges are retained conservatively instead of being forced into modern institutions without evidence. The package contains **354 source opponent labels resolving to 339 canonical opponent keys**.

## 11. Owner-approved future canonical corrections

The owner approved both surfaced cross-source corrections, but this package commit intentionally does **not** edit global canonical data:

- `CBBG-0020008`: Vanderbilt-Florida belongs on **2020-12-30**, not 2020-12-29.
- `CBBG-0005665`: Vanderbilt's score against Arkansas is **71-92**, not 71-82.

The corresponding Vanderbilt source rows carry the approved values and row notes. Application is deferred to a later explicitly authorized ingestion/reconciliation phase.

## Package QA snapshot

- Games: 3,006
- On-court record: 1,724-1,282
- Through 2024-25: 2,970 games, 1,697-1,273
- 2025-26: 36 games, 27-9
- Blank exact dates: 669
- Site types: 1,428 Vanderbilt home; 1,292 opponent home; 286 neutral
- Game types: 2,823 regular season; 117 conference tournament; 37 NIT; 29 NCAA tournament
- Distinct source opponent labels / canonical keys: 354 / 339
- Read-only pre-ingestion matcher: 657 confident identities; 4 review cases; 2,345 new-game candidates
- Confident matches with source differences: 37 (9 date, 14 score, 14 overtime)
- No exhibition or unplayed schedule rows
- No score/result contradictions after curated source review
