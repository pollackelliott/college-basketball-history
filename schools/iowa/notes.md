# Iowa men's basketball source-package curation notes

## Research status

This six-file portfolio was built as a **parallel research-lane artifact** outside tracked repository state. It was research-frozen against `research_base_sha=4c8d75592f98b42a8534182a5af9bf240b1fd16c` and has now completed the mandatory current-main shared-reference rebase against `integration_base_sha=4c8d75592f98b42a8534182a5af9bf240b1fd16c`. Status: **INTEGRATION_FROZEN**.

Owner history-scope ruling: **Iowa has always been D1/top-level for site purposes.** Public/site history therefore begins with program inception in **1901-02**.

## Coverage and record

- Competitive games: 3,045
- On-court record represented by row scores/results: 1,794-1,251
- Coverage: 1901-02 through completed 2025-26
- Exhibitions: excluded
- Exact dates genuinely unknown: 20
- Played scores genuinely unknown: 1

The media guide's administrative/official aggregate differs from the project's on-court record because five source rows are marked `+` (awarded forfeits). The package preserves the source administrative marker separately but lets the played score control `played_result`, per project policy.

## Important source normalization decisions

1. **Awarded forfeits.** The media-guide legend defines `+` as “Awarded Forfeit.” Five rows carry that marker while their scores show Iowa lost on the court. Those rows remain on-court losses and carry `administrative_status=FORFEIT`. No additional individual-game sanction allocation is invented.
2. **2016-17 NIT vs. TCU.** The media guide prints `3/19 TCU# W, 92-94`. The score, season record and authoritative game history establish a 94-92 TCU overtime win. The package preserves the raw text but normalizes Iowa's played result to `L`, one overtime.
3. **2009-10 season heading.** The guide prints `10-21`, but its game ledger contains 32 competitive games and the row-level tally is 10-22. The package follows the game ledger rather than silently dropping a loss.
4. **Unknown 1902-03 score.** The Jan. 29 road win at Des Moines College is explicitly listed `W, N/A`; its score remains blank.
5. **Unknown early dates.** Media-guide `N/A` date rows remain date-unknown rather than being inferred from sequence.
6. **1967-68 Big Ten playoff.** The March 12 neutral Ohio State playoff is classified generic `POSTSEASON`, not a modern Big Ten Tournament game.

## Home-site and venue discipline

H/A/N comes from explicit media-guide `at`/`vs. (n)` notation and the official 2025-26 schedule, never from geography. Venue chronology is applied only after `SOURCE_PROGRAM_HOME` is independently established. Research supports this primary sequence:

- Old Armory (east-bank campus): program inception through 1920-21
- New Armory: 1921-22 through 1926-27
- Iowa Field House: 1927-28 through the January 1983 transition
- Carver-Hawkeye Arena: beginning with the Jan. 5, 1983 Michigan State game

`VEN-000281` (Old Armory), `VEN-000282` (New Armory), and `VEN-000283` (Beasley Coliseum) were provisional research-time allocations. The serialized current-main rebase found no physical-identity, key, display-name, alias, geography, or numeric-ID collision. **Final integration mapping:** Old Armory -> `VEN-000281`; New Armory -> `VEN-000282`; Beasley Coliseum -> `VEN-000283`.

## Conference history

Iowa was independent for basketball through 1907-08, competed in the Big Ten from 1908-09 through 1928-29, did not compete in the league in 1929-30, and resumed Big Ten play in 1930-31. The one-season non-competition interval is represented explicitly rather than hidden inside a continuous membership span.

## Postseason and accomplishments research

Authoritative institutional evidence supports the following integration-time accomplishment values:

- Conference regular-season championships: **8** (1923, 1926, 1945, 1955, 1956, 1968, 1970, 1979)
- Conference tournament championships: **3** (2001, 2006, 2022)
- NCAA Tournament appearances: **30** after the 2026 appearance
- Final Fours: **3** (1955, 1956, 1980)
- National championships: **0**
- Best Finish: **NATIONAL_RUNNER_UP**
- Best Finish Year: **1956**

These accomplishment values are documentary research for later Owner Gate 1/integration; this research lane does not write global accomplishment/reference state.

## Integration-freeze status

Current-main shared-reference rebase completed against `4c8d75592f98b42a8534182a5af9bf240b1fd16c`. Current main exactly matched the research baseline, so there were no intervening commits to reconcile. Iowa's program identity, conference identities, existing venue references, and three new physical venue identities were rechecked successfully.

No canonical preflight, Owner Gate 1 seal, apply, release, publication, or tracked repository mutation has yet been performed.
