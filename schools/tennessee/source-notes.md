# Tennessee source notes

## 1. Source hierarchy

Primary historical evidence is Tennessee's **2025-26 men's basketball record-book material**, especially the year-by-year results in `26_5_Results.pdf`, the dedicated SEC/NCAA/NIT postseason tables in `26_8_Postseason.pdf`, and the historical home-court section in `26_9_Volmanac.pdf`. The completed 2025-26 season is owner-supplied and controls that season. Owner rulings control the conference chronology, achievement totals, home-venue display names/eras, and explicit project conventions.

## 2. Historical extraction

The fixed-column year-by-year extraction yields **2,915 competitive game rows through 2024-25** after excluding two explicitly printed exhibitions. `source_page` retains the printed record-book page and `raw_text` retains the extracted chronological line. Season-record QA matches Tennessee's published year-by-year totals after the single 2024-25 Houston correction.

## 3. Completed 2025-26 supplementation

The owner supplied the completed 2025-26 season separately: **37 recognized games, 25-12**. The Duke 2025-10-26 exhibition is excluded. Exact 2025-26 venues/cities supplied by the owner are retained.

## 4. Date parsing

Printed month/day tokens are converted to exact dates using the season boundary (November/December in the starting calendar year; January-March in the ending year). Three genuinely undated 1921-22 games remain blank. The impossible `F29` VMI tournament token is normalized to 1930-02-28 as an explicit correction and remains visible in `raw_text`.

## 5. Overtime

Tennessee's year-by-year legend uses `*`, `**`, `***`, and `****` after scores for one through four overtimes. Those markers populate `overtime_periods`; the 2025-26 owner supplement explicitly supplies the two-OT Texas A&M game and OT Georgia game.

## 6. Postseason corroboration

The dedicated SEC Tournament table establishes championship-game appearances and the dedicated NCAA table establishes NCAA round progression. The NCAA table itself contains a known 2019 date typo for Purdue; the chronological year-by-year ledger controls the game date (2019-03-28). The 2024-25 Houston score/result conflict is resolved in favor of the dedicated NCAA table plus the 30-8 published season aggregate.

## 7. Venue sources

The Volmanac's home-court history establishes Tennessee's primary venue eras. The package applies those venue eras only to games independently established as Tennessee home. Thompson-Boling Arena remains the owner-selected site-facing name; Food City naming is retained as alias evidence.

## 8. Opponent resolution

Opponent normalization first reuses identities already established in the project package evidence, then applies the current Division-I registry conventions and conservative historical identities. Tennessee's opponent-series table explicitly establishes several historical lineage/display normalizations (City College of Detroit -> Wayne State; Eastern Montana -> Montana State-Billings; Cumberland College -> Cumberlands (Ky.); Mexico/Univ. of Mexico -> University of Mexico). Established project historical keys are reused where known, including Union College (Ky.), Washington & Lee, and St. Francis Brooklyn. Raw printed labels remain auditable in `source_opponent_label`/`raw_text`.

## 9. Expected reconciliation behavior

Because Tennessee overlaps seven already-public programs, ingestion should match many existing canonical games. Material disagreements should be presented in the project's required human-readable discrepancy review before resolution, with especially close owner review for 21st-century cases. The six-file package itself is the principal deliverable; broad re-auditing of already-settled canonical history is not required absent a surfaced discrepancy.

## Post-ingestion cross-source curation — 2026-08-10

The Tennessee chronological ledger remains the preserved raw source basis. During cross-source reconciliation, two rows were curated for overtime count after corroborating evidence established information omitted from the Tennessee chronological line:

- TENRAW-01005 — 1963-01-19 at Kentucky: curated to 1OT; raw Tennessee text preserved.
- TENRAW-01407 — 1978-03-04 at Florida: curated to 3OT; raw Tennessee text preserved.

Twenty-one of the 22 ingestion discrepancies were resolved. DISC-000078 remains under review as a genuine 1910 score conflict.
