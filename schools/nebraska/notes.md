# Nebraska men's basketball research notes

## Research status and history scope

This portfolio was assembled as a research-only six-file package against repository baseline `ced6a1e64d46c3be040b680b308bc070d22cff08`. It does not mutate the global repository and is not `INTEGRATION_FROZEN`.

Owner history-scope ruling: Nebraska has always been top-level / Division I for site purposes. Accepted history therefore begins with program inception in **1896-97** (`ALWAYS_TOP_LEVEL_FROM_INCEPTION`).

The game ledger contains **3,104 competitive games** through the completed 2025-26 season and preserves on-court results. The final on-court record is **1,624-1,480**.

## Primary historical ledger

The Nebraska 2025-26 media guide year-by-year ledger is the primary source for history through 2024-25. The 2025-26 competitive schedule is supplied from Nebraska Athletics' official season schedule. The BYU and Midland preseason noncompetitive games are excluded.

## Conference history

`conferences.csv` records Independent, Missouri Valley, Big Six, Big Seven, Big Eight, Big 12, and Big Ten eras. The 1919-20 media-guide season summary explicitly states that Nebraska had no conference affiliation. The Big Eight display era begins in 1958-59; 1957-58 is still labeled Big Seven in Nebraska's source.

## Conference tournaments

The owner-supplied Conference Tournament Site Reference is incomplete globally. For Nebraska, the owner explicitly authorized its completed **Big Eight, Big 12, and Big Ten** sections. No other unfinished conference section was treated as project canon.

For the 1977-85 Big Eight Tournaments the reference distinguishes campus quarterfinals from the shared Kemper Arena phase; those boundaries are honored. Beginning in 1986 the Big Eight Tournament rows use the shared-site chronology. Big 12 and Big Ten shared sites are applied season-specifically.

Nebraska's 1994 Big Eight championship is stored as **Nebraska 77, Oklahoma State 68**. The dedicated conference-tournament table in the media guide prints 77-66, but the year-by-year ledger and Nebraska's official 1993-94 schedule both give 77-68. The package retains the year-by-year raw text and documents the dedicated-table conflict.

## Postseason taxonomy

The package contains **11 NCAA Tournament games**, **42 NIT games**, and **9 generic `POSTSEASON` games**. The generic postseason rows are the three-game 1909 Missouri Valley championship playoff against Kansas in Kansas City; the 1949 Big Seven title playoff against Oklahoma; the 1949 NCAA District qualifying playoff against Oklahoma State; and four 2025 College Basketball Crown games.

The 1949 Oklahoma State game is **not** classified as an official NCAA Tournament game: Nebraska's source describes it as a playoff for a berth in the eight-team NCAA field. Nebraska's 1996 NIT title game and 2025 College Basketball Crown title game use `Championship`; other non-NCAA postseason round fields remain blank unless supported by the controlled vocabulary.

## NCAA site completeness

All **11 NCAA Tournament rows** have a curated physical venue, city/state, and controlled NCAA round. Important physical-identity normalizations include the original 1955 Charlotte Coliseum for 1986; Carrier Dome as the same physical building represented by JMA Wireless Dome; BSU Pavilion as ExtraMile Arena; and AT&T Center as the physical building now represented by Frost Bank Center.

## Home venue chronology

Venue chronology is applied only after a game is independently classified Nebraska home:

- Grant Memorial Hall: inception through 1921-01-13
- State Fairgrounds Coliseum: 1921-01-14 through 1921-22
- Grant Memorial Hall: return through 1926-02-05
- Nebraska Coliseum: 1926-02-06 through 1975-76
- Bob Devaney Sports Center / NU Sports Complex: 1976-77 through 2012-13
- Pinnacle Bank Arena: 2013-14 onward

Research-time venue IDs are provisional. Grant Memorial Hall, State Fairgrounds Coliseum, Nebraska Coliseum, and Frost Bank Center specifically require authoritative current-main venue rebase by the Implementation lane.

## Material curated corrections

**1978 Oklahoma State Big Eight Tournament.** Nebraska's all-time ledger marks the 1978-02-28 game neutral. Oklahoma State's official box score identifies the game at the NU Sports Complex in Lincoln. It is therefore curated as `SOURCE_PROGRAM_HOME` at Bob Devaney Sports Center, while the Nebraska source marker remains preserved in provenance.

**Recent neutral-site markers.** The media-guide ledger uses `A` for some recent neutral-site games. Explicit `vs.` wording and Nebraska official schedule/box-score evidence control the curated status where supported, including the 2017 Big Ten Tournament, 2023 Oregon State, 2024 Big Ten Tournament, 2024 NCAA game against Texas A&M, late-2024 neutral event games, and the 2025 College Basketball Crown. Geography alone was not used to establish H/A/N.

## Intentional unknowns

Thirteen exact dates remain blank because the primary source does not provide enough precision: four games in 1898-99, six in 1900-01, two in 1903-04, and one Kansas City A.C. game in 1923-24.

Three played scores remain unknown: the 1903-04 Highland Park loss, 1904-01-15 at Lincoln YMCA loss, and 1904-01-22 Lincoln YMCA win. The 1903-04 Highland Park and Nebraska Wesleyan rows also remain `UNKNOWN` for H/A/N rather than receiving unsupported classification.

## Integration handoff

No owner questions remain. Before tracked Phase 0, the Implementation lane must rebase provisional venue identities/IDs and global opponent/program identities against then-current main. This research ZIP is immutable provenance once frozen.
## Integration normalization — 2026-08-25

- Integration base: `a05ad97f1023dae8f277c805c9598ecb5caa319c`.
- Owner-confirmed history scope: `ALWAYS_TOP_LEVEL_FROM_INCEPTION`; accepted site history begins in 1896-97.
- Current-main opponent identity normalization: `fiu` -> `florida-international` (display `FIU`).
- Current-main opponent identity normalization: `umass` -> `massachusetts` (display `Massachusetts`).
- Current-main opponent identity normalization: `usc-upstate` -> `south-carolina-upstate` (display `USC Upstate`).
- Owner confirmed Wisconsin-Stevens Point is non-D1; its two Nebraska games remain preserved as historical non-D1 competition.
- Venue rebase: Frost Bank Center reuses `VEN-000295`; Grant Memorial Hall = `VEN-000310`; State Fairgrounds Coliseum = `VEN-000311`; Nebraska Coliseum = `VEN-000312`.
- The immutable RESEARCH_FROZEN transport ZIP remains unchanged; these are integration-copy normalizations only.
- Owner confirmed on 2026-08-25 that `csu-pueblo` should display as `CSU Pueblo`; the Nebraska integration copy was normalized accordingly.
