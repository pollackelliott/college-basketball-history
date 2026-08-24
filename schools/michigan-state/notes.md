# Michigan State onboarding package notes

## 1. Scope

- Program key: `michigan-state`
- Owner-confirmed public history start: **1898-1899**
- `history_scope_status`: `OWNER_CONFIRMED`
- `history_scope_basis`: `ALWAYS_TOP_LEVEL_FROM_INCEPTION`
- Competitive coverage: **1898-99 through completed 2025-26**
- Exhibitions/non-record contests are excluded.
- `research_base_sha`: `4c8d75592f98b42a8534182a5af9bf240b1fd16c`

The owner explicitly ruled that Michigan State has always been D1/top-level for site purposes. That scope ruling is controlling and is not reopened here.

## 2. Package QA snapshot

- Competitive source games: **3,059**
- On-court record: **1,884-1,175**
- Historical competitive ledger through 2024-25: **3,024 games, 1,857-1,167 on court**
- Completed 2025-26 supplement: **35 competitive games, 27-8**
- Distinct source opponent labels: **594**, all resolved
- Canonical opponent identities represented: **349**
- H/A/N/Unknown: **1,507 / 1,193 / 359 / 0**
- Game types:
  - `REGULAR_SEASON`: **2,873**
  - `CONFERENCE_TOURNAMENT`: **58**
  - `NCAA_TOURNAMENT`: **116**
  - `NIT`: **12**
  - `POSTSEASON`: **0**
- Unknown exact dates: **0**
- Unknown played scores: **0**
- Venue rows: **59**
- NCAA physical venue + city/state complete: **116 / 116**
- Big Ten Tournament physical venue + city/state complete: **58 / 58**
- `source_game_id` values unique: **YES**
- Obvious duplicate game signatures: **0**

## 3. Competitive-universe reconciliation

The media guide's chronological year-by-year extraction initially yields 3,026 printed rows through 2024-25, but three are not part of Michigan State's official competitive season totals:

- 1959-01-17 vs **MSU Alumni**
- 1965-12-27 vs **Hawaiian Marines**
- 1965-12-30 vs **Hawaiian Army**

The 1958-59 season summary is 23 games while the chronological page contains 24 rows including MSU Alumni. The 1965-66 season summary is 22 games while the chronological page contains 24 rows including the two service-team contests. Those three rows are therefore excluded from the project's competitive history.

The chronological extraction also contains a malformed 2025 Auburn NCAA date token (`3/3025`). That real game is restored as **2025-03-30**, Auburn 70-64 Michigan State, NCAA Elite Eight in Atlanta.

These adjustments yield **3,024 competitive games through 2024-25**. The completed official 2025-26 schedule adds **35** competitive games for the final package total of **3,059**.

## 4. 2025-26 completed season

Michigan State Athletics' official completed schedule reports **27-8**.

The following two preseason contests are explicitly labeled exhibitions and are excluded:

- Bowling Green — 2025-10-23
- at Connecticut — 2025-10-28

The competitive 2025-26 package has:
- 17 home
- 10 away
- 8 neutral
- 31 regular-season games
- 1 Big Ten Tournament game
- 3 NCAA Tournament games

Michigan State defeated North Dakota State and Louisville in Buffalo before losing to Connecticut in the Sweet Sixteen in Washington, D.C.

## 5. H/A/N methodology

The Michigan State media guide's all-time opponent-series section supplies explicit game-level H/A/N designations and is used to classify historical sites. Geography and venue chronology do not establish H/A/N.

The package has **zero UNKNOWN site classifications**.

Venue chronology is applied only after a row is independently established as Michigan State home.

## 6. Conference chronology

- **1898-99 through 1949-50:** Independent
- **1950-51 onward:** Big Ten

Big Ten official history says Michigan State College was added to the conference in 1949; conference basketball competition is represented beginning with the 1950-51 season.

## 7. Conference tournament

Michigan State's conference-tournament history is exclusively Big Ten.

The owner supplied `Conference_Tournament_Site_Reference.xlsx` and explicitly authorized the **completed Big Ten section only** for Michigan State. That reference is used for physical venue/city/state enrichment, never to infer H/A/N.

Michigan State has **58 Big Ten Tournament games** through 2026, all with physical venue and city/state populated.

## 8. NCAA Tournament

The package contains **116 NCAA Tournament games** through 2026.

Every NCAA row has:
- physical `venue_key`
- `venue_id`
- normalized city
- normalized state
- project-controlled NCAA round where supported

NCAA round distribution:
- Play-in: 1
- R64: 34
- R32: 29
- Sweet Sixteen: 23
- Elite Eight: 15
- Final Four: 10
- Championship: 3
- historical consolation/third-place with blank public round: 1

Important source corrections are preserved rather than silently erased:
- 2021 UCLA First Four is structured as **2021-03-18 at Mackey Arena, West Lafayette, Indiana**, from Michigan State's official contemporary schedule/recap; the dedicated media-guide NCAA table carries a conflicting date/site wording.
- The malformed 2025 Auburn date is normalized to 2025-03-30.
- Physical NCAA site identity is completed for all 116 rows.

## 9. NIT

The package contains **12 NIT games**.

The 1997 Florida State NIT game is structured as **1997-03-17**, supported by Michigan State's official contemporary/archive schedule evidence; a separate historical NIT table carries a conflicting March 19 date.

## 10. Administrative results

Public historical results follow what happened on the court. Michigan State's media guide marks five contests `W(F)`; the package preserves those administrative outcomes separately while retaining the played score/result:

- 1977-01-24 vs Minnesota — on-court L, 70-75
- 1977-02-17 at Minnesota — on-court L, 77-99
- 1982-02-20 vs Wisconsin — on-court L, 60-65
- 1982-11-26 vs Western Michigan — on-court W, 72-65
- 1984-01-12 vs Wisconsin — on-court L, 74-81

These five rows use `administrative_status = FORFEIT` without rewriting the on-court result.

## 11. Source-internal corrections and preserved conflicts

The media guide contains several transcription/date inconsistencies. Structured values follow stronger Michigan State internal or contemporary official evidence while `raw_text` preserves the printed chronological claim. Notable examples include:

- 2009-12-19 IPFW: normalized to 80-58
- 2016-11-23 St. John's: normalized to 73-62
- 2019-11-18 Charleston Southern: normalized to 94-46
- 2020-02-01 Wisconsin: printed score 63-64 controls as an MSU loss despite a conflicting W marker
- 2022-11-15 Kentucky: normalized to 86-77 in 2OT
- 2023-11-09 Southern Indiana: normalized to 74-51
- 1988-12-30 Oregon: normalized to 76-71
- numerous obvious one-digit date transcription errors are documented row-by-row where applicable

The all-time opponent-series extraction also contained page-header parsing corruption around Wisconsin, Southwestern Louisiana and Winona. Identity resolution was repaired from the printed game rows:
- Wisconsin remains Wisconsin
- `S.W. Louisiana` resolves through Southwestern Louisiana/USL lineage to Louisiana
- the three true Winona/Winona College games remain a conservative historical Winona identity

## 12. Venue history and provisional global IDs

Michigan State institutional history identifies five principal historical homes:

1. Armory
2. the gym in today's IM Circle complex
3. Demonstration Hall
4. Jenison Fieldhouse
5. Breslin Center

Current research-base main already contains:
- `VEN-000093` — Jenison Fieldhouse
- `VEN-000029` — Breslin Center

The package proposes five **research-time provisional** physical IDs:

- `VEN-000281` — Armory
- `VEN-000282` — IM Circle Gymnasium
- `VEN-000283` — Demonstration Hall
- `VEN-000284` — Hofheinz Pavilion
- `VEN-000285` — Suncoast Credit Union Arena

These numeric IDs are **not authoritative** and must be rebased against CURRENT main before tracked Phase 0.

Armory and IM Circle are retained as researched physical home candidates, but the package does not blanket-assign early home games to either building because the available source does not establish sufficiently precise game-level transition boundaries.

Demonstration Hall is used for already-established home rows in the 1930s. Jenison begins with the documented first basketball game on 1940-01-06 vs Tennessee and remains the regular home through 1989, with the 2012 Tuskegee special-return game assigned explicitly. Breslin begins with the 1989-90 home era.

## 13. Accomplishment evidence for later integration

Authoritative/source-supported values through completed 2025-26:

- Conference regular-season championships: **17**
- Conference tournament championships: **6**
- NCAA Tournament appearances: **39**
- Final Four appearances: **10**
- NCAA national championships: **2**
- `best_finish_key`: **NATIONAL_CHAMPION**
- `best_finish_year`: **2000**

The 2026 NCAA appearance is Michigan State's 39th on-court appearance; the media guide's 38-appearance headline is through the completed 2025 tournament.

## 14. Freeze status

This portfolio is **RESEARCH_FROZEN**, not `INTEGRATION_FROZEN`.

Before tracked Phase 0, the serialized Codespace integration lane must:
- synchronize CURRENT main
- compare current shared identities with `research_base_sha`
- reuse any physical venue identities added by intervening teams
- refresh every provisional global venue ID
- rerun package QA and hashes
- only then install the tracked package and begin authoritative onboarding preflight

No canonical matching, Owner Gate 1 sealing, transactional apply, release, PR or publication was performed in this research lane.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=55682c81cf3ee1df2eda20cf4f90f1604c4d8619` from `research_base_sha=4c8d75592f98b42a8534182a5af9bf240b1fd16c`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
