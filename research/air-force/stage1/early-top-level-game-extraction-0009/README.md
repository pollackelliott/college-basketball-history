# Air Force Stage 1 — official guide game-universe extraction checkpoint 0009

**STATUS: STAGE1_IN_PROGRESS; 1982–83 is still explicitly blocking.** This is one bounded four-season Research extraction, NOT Stage 1 closeout, Stage 2, Research Freeze, an owner gate, or Implementation.

Authority: protected main and immutable `research_base_sha` `3f5a15458aa468347e56e669327d6fe4c9c6ee69`; exact accepted parent Research HEAD `4e57cc01096984aa6b4fad48cf34915c535e78fb`. Owner-final top-level classification `Air Force,1957-58+` is unchanged, separate from varsity inception **1956–57** (NON_D1). Institutional research spans inception through **2025–26**.

## 1985–86 through 1988–89 guide extraction

All games derive from official Air Force 2026–27 men's basketball history guide PDF **page 63** (SHA-256 `5fdf61cc80c698bae8ce61cc0ae1009d01139682c8148014934e304b407b73fd`, source https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/goairforcefalcons.com/documents/2026/5/27/History.2026-27.pdf?timestamp=20260527033629). The text columns run across page 63: 1985–86 starts at lower left and concludes top middle; 1987–88 starts lower middle and concludes top right. The extraction explicitly stitches those page columns without inventing a missing game or bleeding adjacent seasons.

| Season | Official guide W-L | New accepted game rows | Source WAC regular-season W-L | H/A/N reconciled W-L | Conference tournament |
|---|---|---:|---|---|---:|
| 1985–86 | 10–19 | 29 | 3–13 | H7–8 A2–9 N1–2 | 2 |
| 1986–87 | 12–15 | 27 | 5–11 | H9–6 A2–8 N1–1 | 1 |
| 1987–88 | 11–17 | 28 | 4–12 | H9–4 A1–10 N1–3 | 1 |
| 1988–89 | 14–14 | 28 | 6–10 | H9–5 A4–8 N1–1 | 1 |

Exactly **112 newly identified games** (107 REGULAR_SEASON, 5 CONFERENCE_TOURNAMENT), for **798 distinct accepted games** cumulatively across **32 fully row-identified seasons**. All first **686 accepted parent game rows and header are retained byte-for-byte**. Dated source literal opponent, score, on-court W/L, WAC marker and `#`/`##` postseason identity, site H/A/N evidence, and cited guide source are retained in the ledger. Every new season's detailed W/L equals guide heading and site totals; each guide contains exactly 16 WAC regular-season contests with its asserted WAC W/L.

## Exact source hierarchy and nonblocking differences

The official Air Force athletics **1985–86** and **1986–87** online schedules were directly inspected, and their individual results and H/A/N win-loss totals reconcile exactly. For **1987–88** and **1988–89**, official season schedule endpoints could not be retrieved during this bounded pass: game identities/scores are established by the guide, while MCubed exact-game site classifications are explicitly **provisional** and supported by Air Force official opponent-history spot checks. Do not claim those two official season pages were inspected.

- **1985–86 postseason**: Hawaii# W64–58 on **1986-03-03**, an Air Force home first-round WAC game in USAFA, CO; Wyoming## L65–67 **1986-03-09** in Laramie, WY, classified **NEUTRAL** by the official Air Force season site accounting, notwithstanding Wyoming's actual host location. MCubed calls Wyoming AWAY and prints **March 6**. Preserve the exact alternative date/site class for Stage3B; never override primary site totals or infer classification solely from geography.
- **1985–86 Suntory Ball, Tokyo**: Navy$ L53–70 **Dec 21** and Army$ W56–50 **Dec 22**, both NEUTRAL, supported by the guide and Air Force official season schedule. MCubed prints Navy on Dec 20: nonblocking secondary date contradiction.
- **1986–87 Blade Grass Classic, Toledo**: Toledo$ L60–77 at Toledo (AWAY) and Georgia Southern$ W87–82 in Toledo (NEUTRAL). Guide/official schedule identify **U.S. International W99–89 and Eastern Washington W64–42 at USAFA as HOME**; MCubed instead assigns both away, contradicting the official **H9–6 A2–8 N1–1**. WAC first-round BYU# L79–82 OT on March 5 at **Albuquerque, NM**, NEUTRAL.
- **1987–88**: Cal-Irvine tournament Manhattan$ L71–76 and Army$ L70–79 NEUTRAL; Milwaukee tournament host Marquette% L52–80 AWAY, Niagara% W57–54 NEUTRAL. The **March 9, 1988 Hawaii# L76–84 in Provo, UT** is an authenticated WAC Tournament game of **1987–88**, not of 1982–83. The corrupted 2026 guide also incorrectly places that exact result in its 1982–83 section. Admit **one canonical game here** and preserve prior **1982–83 quarantine and blockers unchanged**.
- **1988–89**: Connecticut Mutual Classic, Hartford: Davidson$ W48–45 NEUTRAL, Connecticut$ L55–68 AWAY as host. WAC quarterfinal against New Mexico# L60–74 in Salt Lake City: Air Force 2026 guide and official Air Force opponent-history say **March 9, 1989**; MCubed/Sports-Reference print March 8. Preserve one game and explicit nonblocking competing date, not a duplicate.

No source requires exact building research for these historical regular-season neutral contests during Stage 1. Exact postseason venue/site research remains exhaustive under later repository policy. The source WAC `*` denotes regular-season conference membership, not postseason; `#`/`##` identify WAC tournament entries. `conference-source-observations.csv` carries the four new source WAC records while preserving prior observations intact.

`stage1-residuals.csv` retains all **25** prior residual records and adds **5** exact, nonblocking source-disagreement notes, for **30** total. The existing genuinely **blocking** 1982–83 cross-edition game-population discrepancies (AF-0008-001/002/003) remain open, along with their original raw 26-row guide source candidates. `administrative-results.csv` preserves the accepted 1976–77 Montana administrative-forfeit annotation; `stage1-exclusions.csv` remains unchanged and empty.

The authoritative 70-season institutional census now has **32 accepted row-level seasons**, **1 already harvested but unresolved 1982–83 season**, and **37 later unextracted seasons (1989–90 through 2025–26)**. Thus **38 not yet accepted seasons** and **1,130 aggregate-expected game records** remain (27 represented by the still-contested 1982–83 season header plus 1,103 in later years). These are not anonymous accepted games and do not authorize a source-acknowledged unidentified-game exception. The inherited guide-wide +2 wins all-time-total discrepancy remains explicit.

Safety: research-only `research/air-force` branch; no mutation of protected main, published games, global reference registries, other school Research, or the serialized Implementation lane.

## Exact next bounded continuation

Mechanically extract **1989–90 through 1992–93** from the Air Force primary guide year-by-year page(s), reconcile official/same-game site evidence, preserve precise NCAA/WAC postseason distinctions, and commit **one** next checkpoint. Keep the 1982–83 blocking source-family recovery separate; do not reopen it in an unrelated season extraction or advance Stage 2.
