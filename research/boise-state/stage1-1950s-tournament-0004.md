# Boise State ALL_HISTORY_EXPANSION Research — Stage 1 checkpoint 0004

**STAGE_1_IN_PROGRESS** — Existing independent Boise State Research lane. No Stage 2, Implementation, owner gate, global mutation, or protected-main mutation authorized.

## Exact immutable and parent authority

- Research branch: `research/boise-state-all-history-expansion`
- Immutable `research_base_sha`: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`
- Protected `main` authenticated at this same SHA at start of unit.
- Prior 0003 ZIP SHA-256: `e96762d480b2af16f30aa604d95848affbcdd377264b56d659f2c968323941f0`
- New portable artifact: `boise-state-expansion-stage1-1950s-tournament-0004.zip`
- New ZIP SHA-256: `a7b009e264f4acaeec6b3b7e30efa0605d216ed19102792145b22908ad058fd9`
- ZIP full 16-column structured ledger member SHA-256: `7f6f7043edc21e60e486c4b3fba9895d7e0159b67828eede0fef2bf12e452e52`
- ZIP also includes the fully refreshed 38-season census, 33-season source aggregate accounting, raw source inventory, residuals, new 20-row evidence delta, manifest and checkpoint status. All previous 69 rows are byte-equivalent as parsed CSV rows. GitHub text mirrors preserve the 89-game identity universe, 20 source citations and annual accounting, but the ZIP owns richer source text and exact raw row representations.

## Source-first 1950s recovery

The institutional source is Patricia K. Ourada, *The Broncos: A History of Boise State University Athletics, 1932–1994* (Boise State University, 1994), pp. 110-112. Boise State University ScholarWorks catalog authenticates book/publication and chapter range: https://scholarworks.boisestate.edu/uni_books/7/ . The chapter's direct original PDF returned HTTP 403; an inspected OCR/text transcription of the book chapter is https://paperzz.com/doc/8792873/teams-of-the-1950s . This is a **verified attribution to a university-authored work through a secondary transcript**, not proof that the 403 university PDF itself was accessed. Source distinction remains explicit.

Historical NJCAA national result score/dates are from specialist secondary compilation, independently consistent with official university history's matchup/results narratives:
- 1955 https://jucohoopscoop.com/1955-results/
- 1956 https://jucohoopscoop.com/1956-results/
- 1957 https://jucohoopscoop.com/1957-results/

Contemporary scanned newspapers separately support:
- *Times-News* (Twin Falls), Jan. 8, 1956, p.14 for 1956-01-06 Boise 72 Snow 58 and 1956-01-07 Boise 79 Carbon 50: https://tfpl.sfo2.digitaloceanspaces.com/Newspapers/Times-News_TF177/PDF/1956_01_08.pdf
- University of Idaho *Argonaut*, Dec.13, 1960 p.4 for 1960-12-09 Boise 51 Idaho freshmen 57 and 1960-12-10 Boise 64 Idaho freshmen 58: https://objects.lib.uidaho.edu/argonaut/pdf/arg-1960-12-13.pdf . **Opponent is Idaho's freshman team, not Idaho varsity.** Never normalize this onto Idaho varsity in Stage 2.

All **20** new games (14 W / 6 L) appear in `stage1-1950s-tournament-0004-evidence.csv` and the 89-row ledger:
- 1952-53: 2 Region IV games (Snow W59-48, Eastern Arizona L68-69), dates unknown.
- 1954-55: 2 Region IV games (College of Southern Utah W65-59, Weber W77-74), dates unknown; 4 nationals (Coffeyville L70-78 March 16, Howard County W70-63 March17, Pueblo W70-61 March18, Tyler W60-54 March19).
- 1955-56: two regular season (Snow W72-58 Jan6, Carbon W79-50 Jan7); 3 nationals (Arkansas State–Beebe W70-57 March20, Moberly L51-52 March21, Graceland L58-61 March22).
- 1956-57: Region IV Ricks W54-53, date unknown; four nationals (Arkansas City W68-63 March19, Pueblo L54-72 March20, North Greenville W94-78 March21, Brewton–Parker W81-74 March23).
- 1960-61: Idaho Frosh away-area two games (Idaho freshmen W57-51 / Boise L51-57 Dec9; Boise W64-58 Dec10) with H/A/N **UNKNOWN**, dates score-supported.

## Conflict and inclusion accounting

- Four *Boise State 1994 book vs Mountain West official season aggregate* differences: 1952-53 **15-8 vs 14-8**, 1953-54 **18-18 vs 14-12**, 1954-55 **23-8 vs 18-11**, 1955-56 **18-7 vs 18-11**. Preserve both, use the already accepted MW 33-season series as current accounting reference, do not silently overwrite any figure or infer season-level game IDs. Book 1956-57 (25-6) does match.
- Book reports a 1953-54 game versus the Harlem Globetrotters, a 60-65 Boise loss. **Not** an accepted new row pending research on whether this was an exhibition/non-varsity opponent; preserve this explicit exclusion/classification question.
- **All 20 new sites remain UNKNOWN** despite reported event/locality: do not infer H/A/N from school, bracket, geography or event tradition. Exact dates of the five regional fixtures remain blank.
- Historical NJCAA brackets are specialist secondary source provenance; later Stage 3B research must still establish required postseason site facts, and Stage 2 must resolve opponent aliases without false merges.

## Updated exact populations

- Original 0003: **69** identified source-backed supplemental games (14 junior-college; 55 1968-70).
- New 0004: **89** unique identified supplemental games (34 junior-college; 55 1968-70).
- 33 junior-college annual records still sum **441-346 = 787**, with **753** aggregate-minus-identified identity gap; that is not a 753-game invented ledger, nor a certification of identical accounting criteria.
- 1932-33 inception, absent annual listings for 1937-38 / 1938-39, 1968-69 NAIA note, undated 1930s reciprocal records, conflicting 1950s W/L, and tournament source/site residual remain OPEN.
- Inherited accepted `1970-71+` baseline of 1,670 rows remains untouched.

## Next Stage 1 unit

Seek one coherent high-yield 1930s/1940s or 1960s season-first institutional-source family, with exact first-party results/reciprocal ledgers when possible. The Boise University 1994 history has separate 1930s, 1940s and 1960s chapters available as cataloged archival material but blocked PDF paths must not be retried indefinitely. Preserve distinctions between institutional athletics history, contemporary scores, and compiled secondary brackets. Remain in Stage 1 and do not manufacture owner gates. No owner action currently needed.
