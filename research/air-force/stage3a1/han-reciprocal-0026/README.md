# Air Force — Stage 3A-1 H/A/N reconciliation — checkpoint 0026

**Status: STAGE3A1_IN_PROGRESS. The 27-game 1982–83 UNKNOWN H/A/N population is reduced to 11 through 16 individually matched, source-backed adjudications. Stop after this bounded work unit; next pass uses the named 11-row queue. Do not claim Stage 3A-1 COMPLETE.**

## Durable predecessor and authority
- Protected main independently authenticated at execution: `5f33c88ca1ea7d80e0517f42a200f5a2e15833c9`.
- Exact Air Force parent Research HEAD: `98e3e8ef5537abff2c05905f1e78848d33145ca4`.
- Immutable research_base_sha: `3f5a15458aa468347e56e669327d6fe4c9c6ee69`.
- Authenticated COMPLETE Stage 3A-0 parent: `research/air-force/stage3a0/census-0025/`, exactly 1,928 games, 1,866 regular season, 62 postseason.
- Parent Stage 3A-0 exact input ledger Git blob: `12691e4bea21be9bb85869a62c52fb6426f65d1e`, status `fc0c289f6b8497eb6ba92c959b84576984c3541a`.
- Original Stage 2 repaired ledger Git blob: `e412be06ab8af3ba3054baa09a3b312f62b86145`; previous Stage 2 checkpoint 0022, all 1,928 accepted game identities and 745 literal opponent labels preserved.
- The inherited Stage 4 opponent mapping and institutional-scope authority are byte-for-byte identical to the parent, as demonstrated by identical Git blob SHA.

## Evidence-class method and decisions
The full 1982–83 27-game source-family queue was classified before external research. First use accepted current-main reciprocal institutional source packages; require **exact game date, reverse-equal score pair, and explicit accepted site class** before accepting reciprocal H/A/N. The following seven source-school packages supplied **13** independent exact game reciprocals:
- Colorado State: Jan. 8 opponent-home, Feb. 3 Air Force HOME.
- San Diego State: Jan. 31 opponent-home, Feb. 26 Air Force HOME.
- Wyoming: Feb. 7 opponent-home, Mar. 3 Air Force HOME.
- Utah: Jan. 22 Air Force HOME, Mar. 12 opponent-home.
- BYU: Jan. 24 Air Force HOME, Feb. 19 opponent-home.
- Hawaii: Jan. 29 opponent-home, Feb. 28 Air Force HOME.
- UConn: Dec. 28 opponent-home at host Connecticut, accepted project source-site and exact 66–50 UConn win.

Three additional exact institutional source records:
- San Diego Nov. 27, 1982: a contemporary USD basketball prospectus explicitly documents the Air Force fixture **at San Diego**; 49–47 result matched accepted older institutional Air Force results. `https://user-hazoqtr.cld.bz/USD-Men-s-Basketball-1982-1983`.
- Adams State Dec. 8, 1982: Air Force first-party opponent history explicitly says HOME USAFA and W 79–60. `https://goairforcefalcons.com/sports/mbball/opponent-history/adams-state-university/35`.
- Pan American Jan. 20, 1983: Air Force's December 3, 2002 institutional history/preview explicitly cites its Jan. 20, 1983 51–46 win **at Clune Arena**. `https://goairforcefalcons.com/news/2002/12/3/Falcons_Host_Texas_Pan_American`.

Every one of the 16 resolutions is bound to exact research game ID, game date, reciprocal or first-party row, source program, source page, source URL, immutable current-main school-package Git blob where applicable, and the evidence class in `stage3a1-han-evidence-0026.csv`.

## Mechanical reconciliation
- 1,928 game IDs preserved, no new or excluded games.
- The original Stage 3A-0 ledger remains preserved unchanged under checkpoint 0025. The new `structured-stage3a1-ledger.csv` updates **only** the two normalized H/A/N fields (`han` and `site_type`) on the 16 explicitly accepted rows; all other row fields remain inherited.
- 16 resolved rows: 8 Air Force HOME and 8 Air Force OPPONENT_HOME.
- The site-type display in the full working ledger retains inherited `AWAY` values and writes `OPPONENT_HOME` explicitly on newly adjudicated rows. Those are semantically equivalent away classifications; downstream census must normalize AWAY and OPPONENT_HOME together.
- Updated **regular-season** census: 966 HOME, 774 OPPONENT_HOME, 115 NEUTRAL, 11 UNKNOWN = 1,866.
- Postseason handoff remains 62; historical regular-season NEUTRAL remains 67, modern 48.
- The exact remaining UNKNOWN population of 11 games is enumerated in `stage3a1-residuals.csv`. This checkpoint does not mark those rows researched/exhausted. No geography-, uppercase-, event-city-, or double-round-robin inference was used.

## Next bounded unit
Continue Stage 3A-1 for the remaining 11 rows, class-first: U.S. International (2), Pan American Dec. 4 (1; *conflicted score in newer guide, older accepted ledger controls*), Doane (1), Lafayette Dec. 29 (1), Wisconsin–Stevens Point (1), Texas–El Paso (2), New Mexico (2), Southern Illinois Edwardsville (1). Use the contract's accepted-project, target-school, opponent-school, then at most one coherent named authoritative fallback hierarchy; preserve a researched unresolved row rather than infer. Do not reopen the completed 16 absent genuine contradiction.

Stop before Stage 3A-2 or 3A-3; those are separate owner-facing substage boundaries.
