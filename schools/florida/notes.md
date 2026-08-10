# Florida curation notes

## 1. Program status and coverage

Florida is curated from its first recognized varsity season, 1915-16, through the completed 2025-26 season. The package contains **2,787 recognized non-exhibition varsity games** across 107 seasons with games. Florida did not field teams in the guide's World War I gap (1916-19) or in 1943-44 during World War II; no synthetic game rows are created for those seasons.

## 2. Canonical competitive game count and on-court record

The source package contains **2,787 games: 1,595-1,192 on court**. The 2025-26 owner-supplied supplement contributes 35 games and a 27-8 record. Through 2024-25, Florida's media guide publishes an NCAA-adjusted total of 1,565-1,182; restoring the five explicitly vacated NCAA Tournament games as actual on-court games yields 1,568-1,184 before the 2025-26 supplement.

## 3. Exhibitions

The package is intended to contain recognized varsity contests only. No exhibition rows were identified in the all-time results extraction or in the owner-supplied 2025-26 results.

## 4. Season and date exceptions

There are **23 early games whose exact dates are not printed in the all-time results**. Their `game_date` values remain blank. No date is inferred from row order. The guide prints Florida-Tennessee in the 1941 SEC Tournament as `F29`, an impossible date in 1941; with owner approval, the package uses **1941-03-01**, the date printed in the dedicated SEC Tournament Results section. The unusual Feb. 9, 1927 Auburn/Paris Island Marines same-day pair is retained as two distinct games because Florida's own series evidence corroborates both.

## 5. Home venue chronology and site policy

Owner-approved site-facing home venue chronology uses the media guide's exact first/last-game boundaries: University Gymnasium (1920-01-15 through 1927-02-26), New Gymnasium (1928-01-06 through 1949-02-26), Florida Gymnasium (1950-01-07 through 1980-02-20), and O'Connell Center (1980-12-30 onward). The guide itself calls the first three `The Gym`, `The New Gym`, and `Florida Gym`; those forms are preserved as aliases. The 1928-01-03 home game vs. Olsons Swedes falls in the documented transition gap and therefore has no curated venue. **Game-level H/A/N evidence remains authoritative; venue chronology never changes site type.**

## 6. Neutral and host-site events

Historical H/A/N is taken directly from Florida's chronological all-time result rows. Named regular-season events remain `REGULAR_SEASON`. The 2025-26 neutral-site venues and cities are taken from the owner-supplied completed-season table.

## 7. Conference history and tournament labels

Owner-approved membership chronology: Independent through 1921-22; Southern Conference from 1922-23 through 1931-32; SEC beginning 1932-33. Conference-tournament games use `CONFERENCE_TOURNAMENT`. Public round is blank except for an explicitly established title game. The **1931 Kentucky loss is owner-confirmed as a semifinal and intentionally has a blank public round**.

## 8. NCAA, NIT, and conference-tournament decisions

NCAA Tournament games use the project taxonomy R64, R32, Sweet Sixteen, Elite Eight, Final Four, Championship by Florida's progression within each NCAA appearance. True postseason NIT games are `NIT`; Preseason NIT / NIT Tip-Off events remain `REGULAR_SEASON`. Conference-tournament title games are marked `Championship`; other conference-tournament rounds remain blank for public display.

## 9. Administrative actions

Five NCAA Tournament games are retained with their played scores/results and `administrative_status = VACATED_GAME`: 1987-03-13 NC State, 1987-03-15 Purdue, 1987-03-19 Syracuse, 1988-03-17 St. John's, and 1988-03-19 Michigan.

## 10. Cross-source reconciliations and source errors

With owner approval, internal Florida-guide evidence resolves three chronological-row score errors while preserving the printed row in `raw_text`: 1950-02-11 at Georgia is L 52-77; 1985-01-30 Mississippi State is W 72-57; 1995-02-01 at Mississippi State is L 47-70. The owner also approved a general rule for the SEC Tournament summary's internal typo cluster: where the chronological game list and individual opponent series agree, those values control. Owner specifically confirmed 2009-03-13 Auburn L 58-61, 2023-03-09 Mississippi State L 68-69 OT, and Florida's 2007 SEC Tournament wins on March 9, 10, and 11.

Opponent lineage is conservative. Florida-guide explicit series groupings are used for Trinity -> Duke, Georgia State Teachers -> Georgia Southern, Biscayne/St. Thomas -> St. Thomas University, early Southern -> Florida Southern, Savannah -> Savannah YMCA, and historical Jacksonville Naval Air Station variants -> Jacksonville NAS. A full opponent-series QA pass found no remaining identity ambiguity. It also confirmed several guide-summary defects that must *not* drive game deletion or remapping: Bradley's aggregate series omits the corroborated 1970-12-29 Gator Bowl loss; Florida Southern's 27-6 series omits the explicit 1958-12-20 win (the chronological row and 1958-59 season record require it, producing 28-6 on court); the top-level Mississippi aggregate prints 70-49 while the detailed series is 71-49; and the top-level Oral Roberts aggregate prints 1-0 while the detailed series and chronological row correctly show 0-1. Milwaukee and Wisconsin-Milwaukee are two printed rows for one current program and are intentionally unified under `milwaukee`.

## 11. Known unresolved questions

No opponent institution remains deliberately unresolved in this package. A future global venue reconciliation should determine whether the supplied 2026 `Benchmark International Arena` name should be unified with an existing Tampa arena identity/alias family; this package does not silently conflate it.

## 12. Public presentation notes

Project-wide owner convention is **Miami (FL)** for the University of Miami and **Miami (OH)** for Miami University. Florida rows use canonical key `miami` for the former and `miami-oh` for the latter; the redundant `miami-fl` key is not used. Existing global reference data may still require a later display-name cleanup before every public page shows this convention consistently.

## Package QA snapshot

- Games: 2,787
- On-court record: 1,595-1,192
- 2025-26: 35 games, 27-8
- Blank exact dates: 23
- Vacated games retained: 5
- Distinct canonical opponent keys: 303
- Game types: {'REGULAR_SEASON': 2568, 'CONFERENCE_TOURNAMENT': 113, 'NIT': 28, 'NCAA_TOURNAMENT': 78}
- Conference-tournament title-game rows: 12
- NCAA round counts: {'R64': 26, 'R32': 20, 'Sweet Sixteen': 12, 'Elite Eight': 10, 'Final Four': 6, 'Championship': 4}
