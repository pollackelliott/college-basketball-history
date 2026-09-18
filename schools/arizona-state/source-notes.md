# Arizona State source notes

## Controlling durable research state

Stage 4 was assembled mechanically from the verified Stage 3B cumulative checkpoint with SHA-256:

`cc40a0804d571ed0da9e3cfb1bf38ff57669fc326dc214713cb82afff880453d`

That checkpoint preserves the accepted Stage 1-3B research chain. Stage 4 does not reopen completed historical populations absent a concrete contradiction.

The controlling Stage 1 ledger is represented in the cumulative row-level Stage 2/3 mappings through `stage1_source_artifact`, `stage1_source_locator`, and literal `raw_text`. The package preserves that literal evidence in `source-games.csv`.

## Game universe and dates/scores

The accepted universe is 2,680 competitive games through completed 2025-26. Exhibitions remain excluded.

Exact dates use accepted Stage 3A date findings when present; otherwise a date is populated only when the literal accepted source row itself supplies a sufficiently explicit month/day. The 1948-49 row whose literal `J11` conflicts with the accepted Stage 3A correction remains dated 1949-01-13 in structured data, with the literal row preserved.

Five modern literal score defects were checked against official Arizona State evidence and repaired only in structured fields:

- 1995-01-12 at Stanford: Stanford 91, Arizona State 75 — https://thesundevils.com/sun-devil-mens-basketball-vs-stanford-series-history
- 2011-11-11 Montana State: Arizona State 78, Montana State 72 — https://thesundevils.com/news/2011/11/11/207838340
- 2013-11-29 College of Charleston: Arizona State 80, College of Charleston 58 — https://thesundevils.com/sports/mens-basketball/schedule/season/2013-14
- 2015-11-18 Kennesaw State: Arizona State 91, Kennesaw State 53 — https://thesundevils.com/news/2015/11/21/at-sundevilhoops-faces-another-2015-ncaa-tournament-team
- 2015-12-16 at UNLV: Arizona State 66, UNLV 56 — https://thesundevils.com/sports/mens-basketball/schedule/season/2015-16

The Stage 1 owner-authorized Cal Poly reciprocal insertion retains Cal Poly's literal perspective in `raw_text`; structured score/result are oriented to the Arizona State perspective without altering the evidence.

## Opponent identity

Stage 2 remains controlling. All 2,680 rows resolve to one of 310 distinct opponent identities. Current-program identities retain the protected-main program key established during Stage 2. Historical/NON_D1 identities without a registered global program key receive a deterministic research-local key derived from the accepted canonical name; global registration remains pending current-main rebase.

The complete 68-identity NON_D1 owner sanity scan is prepared in the Stage 4 supporting checkpoint. It represents 252 games. No owner disposition is recorded yet.

The informational Stage 2 self-corrected-opponent artifact is also preserved for owner context.

## Site research

Stage 3A remains closed. Its 216 H/A/N UNKNOWN rows are serialized as `curated_site_type=UNKNOWN` with `RESEARCHED_UNRESOLVED` accounting. The 12 neutral rows with surviving physical-site debt are serialized with `RESEARCHED_PARTIAL` or `RESEARCHED_UNRESOLVED` as appropriate. HOME site blockers remain zero.

Stage 3B remains closed at 98/98 event identities, 98/98 H/A/N classifications, 98/98 city/state sites, and 98/98 exact physical venues. NCAA Tournament physical venue + city + state completeness is 33/33.

The accepted 1964 Utah State postseason correction remains McArthur Court in Eugene, Oregon.

## Conference chronology

Arizona State institutional conference history states that ASU was in the Border Conference from 1931-61, joined the Western Athletic Conference in 1962, and entered Pac-10 play in 1978:
https://thesundevils.com/sun-devil-football-year-by-year

Arizona State men's basketball year-by-year history independently marks entry into Pac-10 play in 1978-79 and supplies the basketball season framing:
https://thesundevils.com/sun-devil-mens-basketball-year-by-year-recordspostseason

Current repository conference authority preserves Pac-10 and Pac-12 as separate historical naming-era display identities within the same legal lineage.

Arizona State Athletics states that full Big 12 membership began August 2, 2024:
https://thesundevils.com/news/2024/08/02/arizona-state-becomes-official-member-of-the-big-12

## Accomplishments reference

The current repository owner baseline for Arizona State is 8 regular-season conference championships, 0 conference-tournament championships, 17 NCAA appearances, 0 Final Fours, 0 national titles, and best finish ELITE_EIGHT in 1975.

Arizona State's current NCAA history confirms 17 NCAA Tournament appearances and three Elite Eight runs (1961, 1963, 1975):
https://thesundevils.com/news/2023/03/13/arizona-state-takes-on-nevada-in-ncaa-tournament
https://thesundevils.com/asu-tournament-history

Arizona State's official year-by-year standings support the accepted title-era seasons, and current 2025-26 institutional game-note material lists the eight conference championship seasons as 1958, 1959, 1961, 1962, 1963, 1964, 1973, and 1975. The 1943-44 first-place wartime standings are not counted as an official conference championship because the Border Conference did not award an official title in that wartime season.

Arizona State's conference-tournament history contains no tournament championship; its 2009 Pac-10 final appearance ended in a loss:
https://thesundevils.com/mens-basketball-conference-tournament-history

## Stage 4 historical status

Stage 4 completed with the owner NON_D1 sanity scan ready. Stage 5 was subsequently approved by the owner with zero flags, and Stage 6 completed the final adversarial self-challenge.


## Stage 6 reciprocal/shared-reference challenge

Stage 6 used already-accepted reciprocal program packages and project shared-reference state as adversarial evidence classes rather than reopening completed research wholesale. Accepted reciprocal corrections preserve Arizona State `raw_text` and alter only fields directly supported by stronger systematic evidence.

The 1943-02-17 Texas Tech row is specifically supported by accepted Texas Tech row `TTRAW-00383`, which preserves the same 46-41 Texas Tech result and records neutral Albuquerque, New Mexico Border Conference postseason/tournament play; its research basis states that Arizona official schedule/postseason history establishes Albuquerque and neutral classification. The exact building remains unresolved and is preserved as researched debt.

Research-time numeric venue IDs remain provisional. Stage 6 reused established research-base identities only where the physical building was definite; unresolved current-main duplicate/spelling/near-match situations remain explicit `PENDING_CURRENT_MAIN_REBASE` rather than being forced.


## Stage 7 immutable Research Freeze

The six-file portfolio is now `RESEARCH_FROZEN`.

No basketball fact was changed during Stage 7. Stage 7 changed only package-status documentation and cryptographically sealed the already accepted Stage 6 historical state.

The 19 blank numeric venue IDs are explicit shared-reference rebase work, not permission to redo the underlying historical research. Implementation must reconcile them against then-current protected `main`, reuse intervening global identities where appropriate, and allocate new numeric IDs only where still necessary.

`CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`
