# Auburn source-package notes

## 1. Scope and cutoff

- Source program: Auburn
- Owner-confirmed history scope: **always D1/top-level for site purposes**
- Site history begins with program inception: **1905-1906**
- Curated coverage ends with the completed **2025-26** season.
- Exhibitions are excluded.

## 2. Package snapshot

- Competitive source rows: **2,806**
- Scored/on-court results: **2,802**
- On-court record across scored rows: **1,527-1,274-1**
- Score-unknown identifiable games retained: **4**
- 2025-26 competitive games: **38 (22-16)**
- Opponent source labels: **342**
- Game types: **2,637 REGULAR_SEASON; 117 CONFERENCE_TOURNAMENT; 37 NCAA_TOURNAMENT; 15 NIT**
- Administrative actions retained: **12 VACATED_WIN** rows from 2016-17.

## 3. Conference chronology — owner approved

- 1905-1906 through 1920-1921: Southern Intercollegiate Athletic Association (SIAA)
- 1921-1922 through 1931-1932: Southern Conference
- 1932-1933 through present: SEC

The 1920-21 March tournament rows remain classified as Southern Conference Tournament games because that is how Auburn's media guide labels the event; the program-level membership chronology remains SIAA through 1920-21 per the owner-approved site convention.

## 4. Primary home venue chronology — owner approved

- Pre-1916: exact home venue intentionally unknown.
- 1916-17 through 1947-48: Alumni Gymnasium.
- 1948-49 through Jan. 10, 1969: Auburn Sports Arena.
- Jan. 11, 1969 through Mar. 3, 2010: Beard-Eaves-Memorial Coliseum.
- Nov. 12, 2010 onward: Neville Arena (opened as Auburn Arena).

Venue chronology is used only after the source evidence independently establishes that Auburn is the home team. It does not infer H/A/N from geography.

## 5. 1937-38 incomplete historical ledger

The media guide labels the season 14-5 but prints only 11 scored game rows and explicitly notes that only available results are shown. Auburn's official historical schedule independently identifies four additional games whose scores are unknown:

- 1938-01-28 vs Georgia Tech
- 1938-02-07 vs Sewanee
- 1938-02-08 vs Sewanee
- 1938-02-18 at Birmingham-Southern

Those four events are retained with blank scores/results. No additional rows are manufactured to force the 14-5 aggregate.

## 6. Approved source corrections / normalizations

Raw source text remains preserved.

- 1917-18 Birmingham College: printed `L 19-11` is normalized to **W 19-11**. Auburn's own series table lists Birmingham College 2-0.
- 1944-45 Tennessee SEC Tournament: malformed `F29` is normalized to **1945-03-02**.
- 1959-60 Jacksonville State: the stray `D4 ... W 73-37` row is excluded from 1959-60. Auburn's season record is 19-3 and its Jacksonville State series places that 73-37 game on Dec. 4, 1961, where it already appears in 1961-62.
- 1995-96 LSU: printed result marker is normalized from L to **W, 95-87**.
- 1995-96 Vanderbilt: printed result marker is normalized from W to **L, 62-76**.
- 1996-97 TCU: malformed `De1` is normalized to **1996-12-01**.
- 1916 source label `Mario` is normalized to **Marion** because Auburn's own opponent-series table places the game in the Marion series.
- Livingston/Livingston State are normalized to **West Alabama** from Auburn's opponent-series grouping.
- Southern College (Fla.) is normalized to **Florida Southern** from Auburn's opponent-series grouping.
- Augusta College is normalized to **Augusta University** from Auburn's all-time opponent table/series.
- Fort Benning is grouped under **Camp Benning** from Auburn's opponent-series history.

### Contemporary Auburn archival corrections discovered during preflight

The first Auburn reconciliation pass exposed a matcher-risk in the 1927-28 Florida series. Contemporary Auburn student-newspaper schedules, preserved by Auburn University Libraries, are used to correct the later media-guide normalization while retaining the media-guide `raw_text`:

- 1928-01-20 Tennessee: Auburn **63-14** (later guide prints Jan. 29).
- 1928-02-18 Florida: Auburn **58-32** (later guide prints Feb. 21).
- 1928-02-22 Florida: Auburn **38-29** (later guide prints 50-28).
- 1929-01-25 at Florida: Auburn **34-44** (later guide prints 33-44).

These are source-package normalizations, not silent deletion of conflicting evidence. The later record-book wording remains preserved in each row's `raw_text` and the archival basis is recorded in `source-notes.md`.

## 7. Administrative results

The 2016-17 guide header reflects NCAA-vacated wins (6-14), while the chronological ledger preserves the on-court 18-14 results. The 12 affected wins are retained with their played score/result and `administrative_status = VACATED_WIN`.

## 8. Postseason classification

Regular-season classics and invitationals remain `REGULAR_SEASON` even when their event names are preserved.

- Southern Conference and SEC Tournament games: `CONFERENCE_TOURNAMENT`
- NCAA Tournament games: `NCAA_TOURNAMENT`
- NIT games: `NIT`
- 2026 NIT championship vs Tulsa is retained as NIT with public round `Championship`.

The media guide establishes 14 NCAA Tournament appearances and 37 NCAA Tournament games through 2025; the package contains exactly 37 NCAA Tournament rows.

## 9. Modern discrepancy handling

Per owner instruction, 21st-century discrepancies are not subjected to extended research when the owner can resolve them quickly. One known source conflict is intentionally preserved for consolidated reconciliation: Auburn's 2004-05 chronological ledger gives the 2005-03-11 SEC Tournament LSU loss as **58-89**, while the media guide's SEC Tournament summary gives a different score. The package currently preserves the chronological row and flags the conflict in row notes for Owner Gate 1 rather than spending research time on it.

## 10. Accomplishment recommendation already owner-approved

For the project's cross-conference historical convention, Auburn has **6** regular-season conference championships: the 1928 Southern Conference title plus SEC titles in 1960, 1999, 2018, 2022 and 2025. Current public accomplishment verification should also use 3 conference-tournament titles, 14 NCAA appearances, 2 Final Fours, 0 national titles, Best Finish = Final Four, and Best Finish Year = 2025.
