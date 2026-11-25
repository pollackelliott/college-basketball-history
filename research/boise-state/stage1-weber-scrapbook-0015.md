# Boise State ALL_HISTORY_EXPANSION — Stage 1 checkpoint 0015 (Weber archived contemporary tournament clipping)

**Status: STAGE_1_IN_PROGRESS** — continuation of the same established Boise State expansion Research lane; not Control Center, Stage 2, Implementation or Research Freeze. This is one bounded source-family action.

## Durable authority and checkpoint lineage

- **Immutable `research_base_sha`: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`**. Do not reset when protected main moves.
- Protected `main` reauthenticated at the beginning of the tranche: **`087ac5dedc65780b65b7ae8d61e239d2033e2eea`**, protected=true.
- Current `AGENTS.md` blob SHA `56e6c524846abf4b0d64a14236f98af7642be762`. Controlling Stage 1 game-universe, all-history expansion lifecycle, research convergence, portable execution and complete-institutional research documents were reauthenticated with unchanged blob content.
- Parent Research branch head: `8c45f41c8c7c0a4b79800a61d2bfec1ea3e47c73` (Stage 1 checkpoint 0014).
- Parent 0014 ZIP SHA-256: `63f4bdbe614eb11a44d9685185a364c20059819d4f38338e4beae734a1636730`.
- New portable checkpoint: **`boise-state-expansion-stage1-weber-scrapbook-0015.zip`**, SHA-256 **`7fea3f676f4d732069d3f434eede09b3147535b997d3e532a287c9398b428bd1`**.
- Full 16-column portable ledger `structured-stage1-ledger.csv` SHA-256: **`2eb6eb23c699b28c2e01db9660a7643e631ba6e5d9b7a7ed718793d5feabd25d`**.
- Portable ZIP includes `manifest.json` with exact size and SHA-256 for **15 files**, full 190-game ledger, complete parent source overlays, source inventory, residuals, season accounting/census, new one-game source delta, original archive access/status census, and `stage1-0015-status.md`. All original 189 parent rows are unchanged as parsed CSV records, including January 10 1958 date repair and 1961-62 83-68 result. Parent ZIP verified against recorded SHA and all member hashes before extension.
- Research-branch mirrors: `stage1-weber-scrapbook-0015-ledger.csv` (190 game IDs), `...-accounting.csv` (38 seasons), `...-season-census.csv` (38), `...-evidence.csv` (one), `...-access-census.csv` (seven specific source dispositions), and this note.

## Bounded primary-source Signpost/archive check

Weber State Stewart Library catalogs *The Signpost* among original student papers, but its public collection entry https://dc.weber.edu/collection/WeberStateUniversityStudentNewspapers was not a usable searchable issue list in this session. The University of Utah Marriott Library explicitly confirms digitized Weber student newspaper coverage 1917–2019, https://blog.lib.utah.edu/utahs-college-student-newspapers/ , but its linked specific Utah Digital Newspapers search endpoint and linked item endpoint returned **HTTP 418** when accessed; see `stage1-weber-scrapbook-0015-access-census.csv`. These transport failures are **not evidence of no games or of exhaustive archival research**.

Sample original Weber `Acorn` pages for 1960/1961, notably https://digital.weber.edu/details?id=108724 and https://digital.weber.edu/details?id=109007, were accessible as institutional page-level OCR. These sampled pages contain general team/athletics narrative, **not individually inspected Boise score tables**, so **zero** of the remaining 23 Weber secondary-only game rows were promoted merely by viewing them. Do not claim that either entire yearbook, let alone all Signpost issues, was exhaustively checked.

## One new source-backed competition from an original preserved contemporary clipping

Weber State University Stewart Library's **Whip Club Scrapbook**, p. 291 (digital page) https://digital.weber.edu/details?id=153754, preserves a newspaper tournament report explicitly saying Boise Junior College defeated **Branch Aggies** (Branch Agricultural College) **51–49** in the **NJCAA Region IV third-place game**. A detailed adjacent account describes the winning Boise basket after a 49–49 tie. This represents **one real played competitive postseason game**, not merely a schedule preview.

A separate companion clipping, scrapbook p. 292 https://digital.weber.edu/details?id=153755, identifies **Weber 57–45 Snow** as the same Region IV championship result. Weber's season-specific history independently locates that exact Weber–Snow final in **1950–51**, https://wildcatchronicle.substack.com/p/history-of-weber-college-basketball-aa3 . Therefore the source-backed Boise result is provisionally and auditably allocated to **1950–51**. The scrapbook's original clipped newspaper publication/date and Boise game's exact played date are not securely visible, and the newspaper text is stored as mixed-column OCR. Preserve this uncertainty; do not manufacture a game date, edition, physical building or formal H/A/N.

New stable game ID **`BOISE-EXP-S1-WEBER-SCRAP-1950-001`**:
- `season=1950-51`, `source_opponent_literal=Branch Aggies (Branch Agricultural College)`, `played_result=W`, `team_score=51`, `opponent_score=49`;
- `game_type=POSTSEASON`, `source_event=NJCAA Region IV third-place`, `game_date` blank, `site_type=UNKNOWN`;
- original source URL p291, separate supporting p292 and attribution uncertainty all serialized in the portable ledger and `...-evidence.csv`.
- Do not prematurely normalize the Branch Aggies alias to a modern program name, or assert venue based only on companion championship reporting.

Exact duplicate check: none of the pre-existing **six** 1950–51 source-backed Boise games are against the Branch Aggies; the new identity is distinct. The officially recorded season W/L remains nonexceeded: 1950–51 source 8–16, now identified **2 W / 5 L = 7**.

## Exact population, residuals and next stop

- Previous 0014: **189** unique supplemental game identities; new 0015: **190**. Original 189 records byte-semantically identical, one new game, no repair or deletion.
- Junior-college identified games: **135** total, of which **134** belong to the **33 Mountain West officially listed** pre-1968 junior-college seasons; one 1937–38 source-backed NNC loss remains separately outside the MW-listed aggregate.
- Accepted 1968–69 + 1969–70 supplemented official Boise record-book identities: **55**, untouched.
- Official 33-season junior-college summary is **441–346, 787 aggregate games**. Of these, **134 source-backed individual games** are identified in the exact listed seasons; **787–134 = 653** remain unmatched by arithmetic. This is season-level research coverage debt, not 653 invented game identities and not proof that independent sources use identical varsity inclusion boundaries.
- Prior **23** Weber secondary-only individually sourced rows remain without individual first-party per-game corroboration; original Weber 1962 yearbook W85–66 vs contemporary Bend Bulletin W83–68 is still **one unresolved same-game score contradiction**, no source override.
- 1948 Idaho varsity result unknown, Jan 1957 NNC result unknown, 1932–33 inception, 1937–39 unlisted annual history, 1950s season-record conflicts, and Denver 1940 source-score discrepancy remain explicitly unclosed.
- No protected-main mutation, accepted published Boise State 1970–71+ rewrite, shared/canonical registry change, or Implementation mutation lock activity.

**Next bounded Stage 1 unit:** Use an **accessible, coherent original opponent game-by-game results source family** outside the unavailable Signpost issue endpoints, prioritizing a multi-season game ledger or a real blocking historical identity question. Do not continue repeated HTTP 418 probes or infer missing scores. Stage 1 remains OPEN. No owner action needed.
