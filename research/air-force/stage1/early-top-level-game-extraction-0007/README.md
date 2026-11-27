# Air Force Stage 1 — systematic guide game extraction checkpoint 0007

**STATUS: STAGE1_IN_PROGRESS**. One bounded four-season Research continuation; NOT Stage 1 COMPLETE, Stage 2, Research Freeze, or Implementation.

Authority: protected main at execution and immutable `research_base_sha`: `3f5a15458aa468347e56e669327d6fe4c9c6ee69`; exact authenticated prior Research checkpoint HEAD `9c55e60e8d7336b433f2ff8bfac749bc6222961f`. The accepted top-level classification `Air Force,1957-58+` is owner-final and unchanged. Full institutional varsity inception **1956–57** is distinct from that top-level boundary and classified **NON_D1**. Required and primary historical completed-season cutoff **2025–26**.

## Primary institutional extraction

Official Air Force 2026–27 history guide PDF pages **61–62** (sha256 `5fdf61cc80c698bae8ce61cc0ae1009d01139682c8148014934e304b407b73fd`) and the corresponding four official historical season-schedule pages provide:

| Season | Guide W-L | Guide individual games | Official online H/A/N W-L |
|---|---:|---:|---|
| 1977–78 | 15–10 | 25 | HOME 10–1; AWAY 4–8; NEUTRAL 1–1 |
| 1978–79 | 12–13 | 25 | HOME 10–4; AWAY 1–8; NEUTRAL 1–1 |
| 1979–80 | 8–17 | 25 | HOME 7–9; AWAY 1–7; NEUTRAL 0–1 |
| 1980–81 | 9–18 | 27 | HOME 8–5; AWAY 0–13; NEUTRAL 1–0 |

**102 new distinct competitive games** in this tranche, **604 total game IDs / 25 extracted seasons (1956–57 through 1980–81)**. The previous 502 accepted game rows and CSV header are carried forward **byte for byte**. All 102 are individually source-identified and reconciled, with original literal guide labels, scored on-court W/L, dates, structured `REGULAR_SEASON` game type, H/A/N supported by official schedule, source provenance, and preserved tournament notation. No double-counted holiday games or anonymous aggregate placeholders.

1977–78 Pillsbury Holiday Classic (Bloomington, Minnesota): Minnesota loss and Tulane win classified NEUTRAL. 1978–79 Vermont Classic (Burlington, Vermont): Texas A&M loss and Cornell win NEUTRAL. 1979–80 Manufacturers Hanover Classic (New Rochelle, New York): Iona loss AWAY (host), American University loss NEUTRAL. 1980–81 Blade Grass Classic (Toledo, Ohio): Auburn win NEUTRAL and Toledo loss AWAY (host). These historical regular-season neutral locations are recorded without inventing building identities.

**1977–78 guide casing defect:** PDF p61 prints `(7) DEPAUL` uppercase, a misleading home cue. Official Air Force 1977–78 online schedule explicitly says **at #7 DePaul in Chicago, Illinois** on February 22, 1978, Air Force loss 41–54. Set that game AWAY, preserve literal uppercase opponent and record residual AF-0007-001. All H/A/N season records then reconcile.

**1979–80 UAB link hazard:** guide prints `Ala.-Birmingham`, official current online schedule prints `UAB` on January 5, 1980 (L51–65) but outbound modern team hyperlink routes to `rolltide.com`. Do not mistake that unrelated outbound destination for historical Alabama opponent identity. Preserve literal source and queue opponent normalization to Stage 2 (AF-0007-002).

**1980–81 conference evidence:** guide season heading explicitly reads `1980-81 (9-18 / 3-13 WAC)`; exactly 16 per-game `*` markers identify Western Athletic Conference contests, 3 W and 13 L. The source observation is retained in `conference-source-observations.csv`; marks denote conference games, **not postseason**. Complete institutional affiliation chronology remains later source research. No NCAA/NIT/postseason games identified within these four seasons. The 1979–80 guide's February 29, 1980 Marquette loss is a **valid leap-year date**, not a defect. The 1978–79 Regis 30–19 score is corroborated by the official schedule.

`administrative-results.csv` is inherited unchanged from checkpoint 0006 and still preserves the **1976–77 Montana forfeit** (actual 59–65 loss vs credited program win). `stage1-exclusions.csv` is inherited unchanged. The parent **18** row-level discrepancy notes are retained intact and **2** new nonblocking notes added, for **20** explicit residual/reconciliation notes. The older identified-game corrections (Arizona, Tulane, DePaul, et al.) remain accepted and are not reopened.

The institutional census remains **70 seasons** (1956–57 through 2025–26), now **25 game-row extracted seasons** and **45 aggregate-only seasons (1981–82 through 2025–26)**, representing **1,324 aggregate-expected candidate games** yet to extract (previous 1,426 minus 102). These are not historical missing-game identities and do not authorize a coverage-gap exception. The inherited primary guide all-time-total +2-win discrepancy is retained unchanged.

Safety: Research-only branch `research/air-force`. No tracked modification of protected main, published history, canonical basketball data, shared registries, another school’s artifacts, or the serialized Implementation lane.

## Next bounded unit

Extract and reconcile **1981–82 through 1984–85** from the year-by-year guide (PDF pp62–63) and corresponding official season schedules. Preserve exact source discrepancies, especially any WAC tournament game_type distinctions, in one successor research-only checkpoint. Do not advance Stage 2 automatically.
