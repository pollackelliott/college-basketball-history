# Air Force Stage 1 — Institutional game-universe extraction checkpoint 0013

**STATUS: STAGE1_IN_PROGRESS — 1982–83 source-population blocker remains OPEN.** This is exactly one bounded four-season continuation of the SAME Research lane, not Stage 1 COMPLETE, Stage 2, a Research Freeze, Implementation, an owner gate, or protected-main mutation.

## Authenticated authority

- Exact protected main / immutable `research_base_sha`: `3f5a15458aa468347e56e669327d6fe4c9c6ee69`.
- Exact independently verified prior Research HEAD: `a5b90e26d63b4f46c0218b48579ba2c2d7f31870`.
- Air Force institutional inception **1956–57** (that first season is NON_D1); accepted top-level/D-I-equivalent boundary `Air Force,1957-58+` remains owner-final; last required completed Research season **2025–26**. Top-level classification does not clip Stage 1.
- Principal results evidence: official 2026–27 Air Force year-by-year men's basketball history PDF **pp66–67**, SHA-256 `5fdf61cc80c698bae8ce61cc0ae1009d01139682c8148014934e304b407b73fd`, https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/goairforcefalcons.com/documents/2026/5/27/History.2026-27.pdf?timestamp=20260527033629.

## Extracted four-season university game universe

| Season | Official competitive record | Accepted unique games | Conference regular season | H/A/N reconciled W–L | Competitive postseason |
|---|---:|---:|---|---|---|
| 2001–02 | 9–19 | 28 | MWC 3–11 | H5–6, A2–12, N2–1 | Wyoming MWC quarterfinal loss (March 7) |
| 2002–03 | 12–16 | 28 | MWC 3–11 | H9–4, A3–10, N0–2 | Utah MWC quarterfinal loss (March 13) |
| 2003–04 | 22–7 | 29 | MWC **12–2** | H13–0, A8–5, N1–2 | Colorado State MWC quarterfinal loss (March 11) **and** NCAA first-round North Carolina loss (March 18) |
| 2004–05 | 18–12 | 30 | MWC 9–5 | H12–1, A4–10, N2–1 | San Diego State MWC quarterfinal loss (March 10) |

**115 new genuine varsity competitive games**: **110 REGULAR_SEASON**, **four CONFERENCE_TOURNAMENT**, and **one separately typed NCAA_TOURNAMENT** game. Combined accepted Stage 1 game universe: **1,248 unique IDs across 48 reconciled seasons**. The preceding checkpoint's entire **1,133 accepted games and original CSV header are retained byte-for-byte**. The current 1982–83 identified-game evidence family is still quarantined and zero 1982–83 games have been assigned accepted IDs. All individual W/L counts, overall W/L, conference game totals, game-type markers, and supported H/A/N partitions reconcile.

### Source-specific reconciliations

**2001–02 and 2002–03 noncompetitive exhibitions:** modern Air Force online pages display **10–20** and **13–16**, respectively, because they mistakenly include expressly identified exhibition games. The 2001–02 website includes **October 31, 2001, Athletes in Action (Exh.), W78–76**, and **November 5, 2001, EA Sports All-Stars (Exh.), L73–76**. The 2002–03 website includes **November 3, 2002, Athletes in Action (Exh.), W66–56**. All three are *explicitly excluded* in `stage1-exclusions.csv`, with source URL and reason, rather than admitted as competitive games or silently deleted. Removing them restores the official guide's 9–19 and 12–16 and the complete individual game totals. Neither season has an unidentified-game count exception.

**2002–03 conference-marker artifact:** guide p66 prints `SAVANNAH STATE**` (January 6 home W56–33) and footnotes `** Air Force’s 500th victory`; it is **NOT** a conference win. The February 1 Utah **away L35–45** lacks the customary conference `*`, but is a Mountain West Conference game. Ignoring the 500th-win marker and including Utah reconciles the season's **3–11 MWC** record; the source's original raw marker text and the two-column PDF score rendering are preserved. Do not treat `**` as postseason or as `*` conference evidence. A March 13 Utah `#` loss is a separate NEUTRAL MWC Tournament game, not a third Utah regular-season contest.

**2003–04 guide punctuation and date:** PDF p66 prints the Texas A&M-Corpus Christi December 9 road W56–53 with a single dot before `W`, rather than ordinary dot leaders. The fully institutional 2003–04 schedule independently confirms the game; the extraction intentionally captures it as the 29th competitive result. The guide prints **December 22** for home Charleston Southern W67–46, but Air Force's official contemporary schedule and **Charleston Southern's reciprocal institutional record** independently confirm **December 20, 2003**. Accepted working date **2003-12-20**, literal `12-22` preserved. The 22–7 source record, including the explicit March 18 North Carolina NCAA Tournament first-round loss 52–63 in **Denver, Colorado**, is unchanged.

**2003–04 H/A/N website summary defect:** the current Air Force online season page's H14–1 A8–6 N0–0 incorrectly suppresses three genuine neutral game-site classifications. Event/host and exact-game evidence establish **December 27 Prairie View A&M at Golden Bear Classic in Berkeley** as neutral (host California December 28 is away), **March 11 Colorado State MWC Tournament** neutral in Denver, and **March 18 North Carolina NCAA Tournament** neutral in Denver. Correct evidence-backed H/A/N is H13–0 A8–5 N1–2; the discrepant website partitions are kept as source counterclaims. NCAA and MWC Tournament physical facilities remain strict/exhaustive Stage 3B research requirements, not assumed from city.

**2004–05 modern unscored calendar:** the online historical schedule renders opponents and dates with **0–0** and no final scores; the official 2026 guide includes **30 dated scored games, 18–12 overall / 9–5 MWC**. Air Force's contemporary 2005 Chris Mooney departure announcement independently verifies those totals. Matched exact-game historical site evidence supports H12–1 A4–10 N2–1, provisionally pending later venue corroboration. BCA Classic Milwaukee has Jacksonville State and Mississippi neutral, but host Marquette away. The guide's `vs. Georgia Tech` at Atlanta is **AWAY** by the institutional online game's `at Georgia Tech` location, not neutral merely because of `vs.` wording. The March 10 SDSU MWC Tournament loss was neutral in Denver.

**Modern neutral venue expectation:** years 2001–05 fall in the strong modern (about 1996–97 onward) regular-season neutral exact-venue regime. Stage 1 preserves tournament-city and H/A/N evidence; it does **not** bless unidentified venue buildings or replace the later exact-venue standard. Exact postseason venues remain obligatory under the site protocol.

## Durable state and stopping

`stage1-ledger.csv` contains all 1,248 accepted dated scored games with literal source rows, on-court W/L, school-relative H/A/N, structured game type, and source/status. `stage1-exclusions.csv` newly and explicitly contains **three known exhibition records**. `administrative-results.csv` still holds the immutable 1976–77 Montana on-court-loss/credited-win distinction. Conference observations include three ordinary 3–11/12–2/9–5 year records and 2002–03 missing `*`/commemorative `**` explanation.

`stage1-residuals.csv`: **55** exact source/provenance notes (**47 inherited unchanged, 8 new**, all new nonblocking); the previously identified genuine **1982–83 blocking institutional source-population conflict** remains open with the unchanged 26-row raw source candidates. `source-inventory.csv`: **102** source entries. No previously accepted population is reopened, accepted 1982–83 candidate is invented, or unrelated Research/Implementation mutated. `manifest.json` Git blob IDs bind all ten checkpoint files.

The institutional census still covers **70 seasons** from inception to the required last completed season. **48** seasons now have a fully identified row-level game population; **22** are not yet accepted: **21 later unextracted seasons (2005–06 through 2025–26)** and the separately disputed **1982–83** season. Their printed guide aggregates correspond to **680 prospective games** (653 in later seasons plus the disputed 27), not a proved missing-game exception. The inherited official guide's +2 all-time-win aggregate inconsistency remains explicitly recorded.

**Safe stopping:** Research-only `research/air-force` branch. Protected main, all published basketball data, global registries, other schools' Research, and the one-active-Implementation mutation lock remain untouched.

## Next bounded Research continuation

Extract and reconcile **2005–06 through 2008–09** from official guide year-by-year rows; preserve NCAA/NIT/league-tournament identity, source-exact venue exceptions, and modern neutral venue research as later-stage work. Commit one bounded successor checkpoint. Do not automatically start Stage 2 or reopen 1982–83 within unrelated season extraction.
