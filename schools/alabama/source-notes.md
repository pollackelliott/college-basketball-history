# Alabama source notes

## 1. Primary historical source

Primary historical evidence is Alabama's official **All-Time Results** ledger supplied for Team #11, covering 1912-13 through 2024-25. Every competitive historical row retains a PDF page locator and the printed chronological line in `raw_text`.

## 2. Completed 2025-26 supplement

The media guide predates the completed 2025-26 season. The owner supplied the completed schedule/results directly: **35 competitive games, 25-10**, plus two explicitly identified preseason exhibitions that are excluded.

## 3. Owner-authoritative project decisions

The owner confirmed program history from inception (1912-13), the Independent -> Southern Conference -> SEC membership chronology, the refined Clark Hall -> Little Hall -> Foster Auditorium -> Coleman Coliseum home-venue chronology with early uncertainty preserved, on-court retention of the vacated 1987 NCAA games, the controlled postseason taxonomy, and the Alabama accomplishment totals used by the site.

## 4. Source corrections and exclusions

The 1948-49 ledger has six exact duplicated layout rows; only duplicate copies are removed. The guide's 2021-22 South Dakota State text extraction omits the date; Alabama's official archived schedule establishes 2021-11-12. The 2024-11-11 McNeese row reverses the score while still printing a win; Alabama's official recap and schedule establish 72-64. All 34 guide exhibitions, two owner-supplied 2025-26 exhibitions, and the canceled 2020 SEC Tournament entry are excluded from competitive source games.

## 5. Site-source limitation

The historical ledger's `at` and `vs.` markers are retained as primary source signals, but several season-level H/A/N headings conflict with the raw prefix distribution. The package therefore uses the published season totals as a safety bound: if a whole `at` or `vs.` category overfills the corresponding published road/neutral bucket, those rows remain `UNKNOWN`; unprefixed rows become Alabama home only in seasons where the complete original prefix distribution reconciles exactly. No site is inferred from a venue or city. The adjusted historical heading aggregate is 1,352 home / 1,037 road / 544 neutral through 2024-25, exactly 2,933 games after restoring the three vacated 1987 NCAA neutrals; it is retained as QA context rather than used to force row-level assignments.

## 6. Opponent lineage evidence

Opponent normalization favors existing project keys and conservative historical identities. External official institutional evidence is used only where needed to establish lineage: Howard College -> Samford; Birmingham-Southern formed from Birmingham College and Southern University in 1918 but states its official athletic history begins in 1918-19, so the two predecessor opponents remain distinct before the merger.

## Extraction reproducibility

The fixed-layout PDF extraction identified 2,973 played-result rows before exclusions. Removing six duplicated layout copies leaves 2,967 played rows; excluding 34 exhibitions leaves exactly **2,933 competitive historical games** and **1,822-1,110-1** on court through 2024-25. The owner supplement brings the package to **2,968 games and 1,847-1,120-1**.
