# Mississippi State curation notes

## 1. Program status and coverage

Mississippi State is curated from program inception in **1908-09** through the completed **2025-26** season. The project owner confirmed on 2026-08-20 that Mississippi State is always top-level/D1 for site purposes from inception.

The package contains **2,856 recognized competitive non-exhibition games** and an on-court record of **1,557-1,299**.

## 2. Historical extraction parity

The official Mississippi State 2025-26 record book contributes **2,824 competitive games through 2024-25** and an on-court record of **1,544-1,280**. Every played season's extracted number of dated game rows reconciles to its printed season record.

Mississippi State fielded no team in exactly four seasons: **1909-10, 1917-18, 1930-31, and 1943-44**. No synthetic games are created for those seasons.

The owner-supplied completed 2025-26 schedule adds **32 competitive games and a 13-19 record**. The Oct. 26, 2025 Houston exhibition is excluded.

## 3. Conference history

Owner-approved chronology:

- SIAA: 1908-09 through 1920-21
- Southern Conference: 1921-22 through 1931-32
- SEC: 1932-33 to present

The 1921-22 and 1922-23 record-book schedules label regular-season conference games `[SoCon]` while Mississippi State also participated in the SIAA Tournament. The package treats primary membership as Southern Conference and preserves SIAA postseason participation as tournament metadata rather than a second primary membership.

## 4. Home venue chronology

Venue chronology is applied **only after H/A/N is independently established from the game line**.

- Before Jan. 25, 1932: established home games may receive Starkville, MS, but no blanket named physical venue is invented.
- Tin Gym: primary basketball relationship **1932-01-25 through 1950-12-14**.
- McCarthy Gymnasium / New Gym: primary basketball relationship **1950-12-15 through 1975-11-30**.
- Humphrey Coliseum: primary basketball relationship **1975-12-01 to present**.

Mississippi State sources disagree on whether the Tin Gym building dates to 1929 or 1931. The package therefore records the exact first established basketball relationship date but does not invent a physical opening year. The 1929-30 team played all games away because no home facility was available, and Mississippi State fielded no team in 1930-31.

## 5. Conference-tournament sites

The owner-supplied conference-tournament site workbook is treated as an **ephemeral Mississippi State source**, not as a globally complete reference. It supplies SIAA, Southern Conference, and SEC tournament venue/city/state details for Mississippi State's relevant games.

One source conflict is preserved explicitly: the Mississippi State record-book heading for the **1945 SEC Tournament** says Knoxville, Tennessee, while the owner-supplied tournament-site reference places that tournament at **Jefferson County Armory in Louisville, Kentucky**. The owner-supplied Mississippi-State-complete tournament reference controls curated venue/location, while the original record-book heading remains in `raw_text`/notes.

The early Atlanta **Municipal Auditorium** tournament games preserve exact source venue and `Atlanta, GA` geography, but `curated_venue_name` is intentionally left blank. The existing global project identity named Municipal Auditorium is the different Kansas City venue; the package does not create a false physical-venue match.

The 2008 SEC Tournament tornado split is handled game-specifically: Mississippi State's Mar. 14 quarterfinal remains at the Georgia Dome, while the Mar. 15 semifinal is assigned to the Georgia Tech venue now represented globally as McCamish Pavilion.

## 6. Postseason taxonomy

The package uses the project-wide controlled taxonomy:

- regular season: **2685**
- conference tournament: **122**
- NCAA Tournament: **25**
- NIT: **24**

Named regular-season tournaments, classics, challenges, and preseason events remain `REGULAR_SEASON`.

Conference-tournament and NIT public rounds are blank except established championship games. NCAA games use only the controlled project vocabulary: Play-in, R64, R32, Sweet Sixteen, Elite Eight, Final Four, Championship. The 1963 NCAA Mideast third-place game is postseason but has a blank public round.

## 7. 2018-19 vacated wins

The record book marks exactly **17 2018-19 wins** with `[V]` and explains that Mississippi State vacated those wins following an NCAA ruling announced in August 2019.

The package preserves the played result and score and records `administrative_status=VACATED_WIN` with a plain-language administrative note. The on-court record is not rewritten.

## 8. Completed 2025-26 owner resolutions

The completed-season package incorporates the owner resolutions:

- **M1:** Dec. 20, 2025 — Mississippi State 71, Memphis 66. The owner-supplied row said 71-65; Mississippi State's official schedule controls the normalized score, while the original supplied value remains in `raw_text`.
- **M2:** Jan. 31, 2026 — Missouri 84, Mississippi State 79. The owner-supplied row said Missouri 82-79; Mississippi State's official schedule controls the normalized score, while the original supplied value remains in `raw_text`.
- Feb. 7, Feb. 11, and Feb. 28 schedule rows contained obvious 2025 year typos and are normalized to **2026**, with original wording preserved.

## 9. Opponent normalization

The package contains **301 distinct source opponent labels**, all resolved in `opponents.csv`, representing all 2,856 games.

Historical/non-current identities remain distinct from current D1 programs. In particular, **Biscayne College maps to the historical St. Thomas University lineage in Florida (`st-thomas-university`, current_d1=No)** and is explicitly distinct from modern D1 St. Thomas in Minnesota.

## 10. Site policy

Source `at` establishes `OPPONENT_HOME`; source `vs.` establishes `NEUTRAL`; an unprefixed game line establishes `SOURCE_PROGRAM_HOME`. Geography and venue chronology never establish H/A/N by themselves.

Source location tags such as Jackson, Meridian, Greenwood, Vicksburg, Tupelo, Biloxi, Southaven, Little Rock, Dallas, and New York are retained when present. Blank historical locations remain blank rather than being guessed.

## 11. Accomplishment cross-check

Mississippi State's official record-book history supports the onboarding accomplishment reference values:

- SEC regular-season championships: **6**
- SEC Tournament championships: **3**
- NCAA Tournament appearances: **14**
- Final Fours: **1**
- national championships: **0**
- best NCAA finish: **Final Four**
- best finish year: **1996**

## 12. Internal tournament-source corrections

A final cross-check against Mississippi State's dedicated **SEC Tournament Results** section identified exactly three year-by-year transcription conflicts. The dedicated tournament section controls normalized facts while the original year-by-year game line remains in `raw_text`:

- 1936 vs. Kentucky: normalized date **1936-02-28** (year-by-year line prints 02/29).
- 1943 vs. Georgia Tech: normalized date **1943-02-26** (year-by-year line prints 02/27).
- 1945 vs. Georgia Tech: normalized result **Georgia Tech 60, Mississippi State 43 on 1945-03-02** (year-by-year line prints 03/01 and 60-33).

The **1926 Southern Conference Tournament** loss to North Carolina is classified as the **Championship** game. Mississippi State's own schedule/record-book material prints **North Carolina 38, Mississippi State 23**; a Southern Conference historical tournament record prints 37-23. The Mississippi State source controls the package score, while the external conference evidence is used only to establish the championship round.
