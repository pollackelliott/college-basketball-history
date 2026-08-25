# Wisconsin men's basketball source-package curation notes

## Research status

This six-file portfolio was built as a **parallel research-lane artifact** outside tracked global repository state and is **RESEARCH_FROZEN** against `research_base_sha=b8b543544cc97d993056537e3b7fc8d09258fa8c`.

Owner history-scope ruling: **Wisconsin has always been D1/top-level for site purposes.** Public/site history therefore begins with program inception in **1898-99**.

The owner additionally authorized the supplied conference-tournament workbook's **Big Ten section only** as complete and reliable for Wisconsin. No other unfinished conference section is treated as project-wide canon.

## Coverage and record

- Competitive games: **3,067**
- On-court record represented by normalized row scores/results: **1,771-1,295-1**
- Coverage: **1898-99 through completed 2025-26**
- Exhibitions/scrimmages/canceled entries: **excluded**
- Site classification: **1,549 Wisconsin-home / 1,110 opponent-home / 278 neutral / 130 unknown**
- Game types: **2,927 regular season / 59 Big Ten Tournament / 69 NCAA Tournament / 11 NIT / 1 other postseason**

The record-book year-by-year aggregate through 2024-25 is 1,750-1,281-1 and the completed 2025-26 season is 24-11. The package's on-court ledger is three wins lower / three losses higher because Minnesota's two 1977 forfeits and Purdue's 1996 forfeit are represented by the played scores rather than the later administrative outcome.

## Material source normalization decisions

1. **2024-25 Arizona/UTRGV ledger defect.** The All-Time Results section places UTRGV on Nov. 15 and omits Arizona. Wisconsin's 2024-25 team-results section establishes Arizona 103-88 on Nov. 15, 2024 and UTRGV 87-84 on Nov. 18. The package adds the omitted Arizona game and corrects the UTRGV date while documenting the ledger wording.
2. **2018 Big Ten Tournament score order.** The All-Time Results row is internally inconsistent. Wisconsin's dedicated Big Ten Tournament section establishes Michigan State 63, Wisconsin 60 on March 2, 2018. The package normalizes the score to Wisconsin 60-63 and preserves the printed raw text.
3. **2024 Marquette score order.** The All-Time Results section prints the Dec. 7 loss as 88-74. Wisconsin's 2024-25 team-results/ranked-opponent material establishes Marquette 88, Wisconsin 74. The package normalizes Wisconsin's score to 74-88 and preserves the raw ledger wording.
4. **Administrative forfeits.** The two 1977 Minnesota games and the 1996 Purdue game remain on-court losses because the source scores show Wisconsin lost before the later forfeits; `administrative_status=FORFEIT` stores the administrative outcome. The 1906 Illinois row is explicitly recorded as a 1-0 forfeit with no separate played score, so the source result is retained together with the forfeit marker rather than inventing a played score.
5. **1908 Big Ten title playoff.** The March 12, 1908 Chicago game is explicitly footnoted as a Big Ten title playoff in Madison. It is classified `POSTSEASON`, not as the modern Big Ten Tournament.

## Home-site and venue discipline

H/A/N is established from explicit source evidence: Wisconsin's All-Time Series Scores H/A/location-code tables, the bold-home convention, explicit source site footnotes, postseason context, or the official 2025-26 schedule. Venue chronology never creates H/A/N.

For games already established as Wisconsin home games, institutional evidence supports:

- **Red Gym:** first explicitly documented home game March 4, 1899; historical home until the Field House transition
- **Wisconsin Field House:** first game Dec. 13, 1930 through the Kohl Center transition
- **Kohl Center:** beginning Jan. 17, 1998 and ongoing

The Red Gym is absent from the research-baseline global physical venue registry. `VEN-000284` is therefore a **provisional research-time allocation only** and must be rebased against current main before `INTEGRATION_FROZEN`. Existing physical identities use their baseline IDs.

130 games remain `UNKNOWN` for H/A/N because the authoritative material does not establish the perspective securely enough. Unknown is intentionally preserved rather than inferred from venue or geography.

## Postseason

- **Big Ten Tournament:** 59 games through 2026. Tournament venue/city/state assignments use only the owner-authorized complete Big Ten workbook section. Public round is blank except verified championship games.
- **NCAA Tournament:** 69 games through the 2026 High Point game. All NCAA rows have a physical venue plus city/state. Historical regional consolation/third-place treatment follows project rules; the 1947 Navy consolation row retains NCAA game type with blank public round.
- **NIT:** 11 games, 6-5, from the record book's dedicated NIT section. No Wisconsin NIT championship game is present, so public round stays blank.

## Conference history

Wisconsin is represented as Independent from 1898-99 through 1904-05 and Big Ten from 1905-06 through the present. The project `big-ten` identity covers the historical Western Conference / Big Nine naming lineage.

## Accomplishment research for later integration

The source package supports later verification of: **20 Big Ten regular-season championships**, **3 Big Ten Tournament championships**, **29 NCAA Tournament appearances through 2026**, **4 Final Fours**, **1 NCAA national championship**, Best Finish `NATIONAL_CHAMPION`, most recent championship year **1941**. These are documentary research only; this research lane does not write global accomplishment/reference state.

## QA / freeze status

Research-level QA passed on the frozen files:

- exactly six required portfolio files;
- 3,067 unique source game IDs;
- 127 historical seasons reconcile to the record-book season game totals after the documented 2024-25 Arizona repair, plus 35 official competitive games in 2025-26;
- row-score record reconciles to 1,771-1,295-1;
- opponent keys are nonblank and each source label maps consistently;
- curated site values use controlled vocabulary;
- city/state are atomic pairs;
- every curated venue resolves through `venues.csv`;
- all 69 NCAA rows have venue/city/state and controlled round values;
- postseason game-type counts reconcile to the dedicated Wisconsin sections;
- no exhibition/scrimmage row is present.

No canonical preflight, current-main shared-reference rebase, Owner Gate 1, ingestion, release, publication, or tracked global repository mutation has been performed. Current-main rebase remains mandatory before `INTEGRATION_FROZEN`.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=e03513ba8a8cd3313023c2f3f3647370f4a0e5c9` from `research_base_sha=b8b543544cc97d993056537e3b7fc8d09258fa8c`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

## Integration-time 1907-08 opponent correction

Authoritative preflight exposed an opponent transposition in Wisconsin's
All-Time Results ledger. The printed ledger gives Jan. 25, 1908 as Chicago
37-16 and Jan. 31 as Minnesota 29-17. Reciprocal institutional evidence
establishes the opposite opponent identities: Minnesota's official 1907-08
year-by-year ledger records a 16-37 loss at Wisconsin on Jan. 25, and
University of Chicago Athletics' official 1907-08 schedule records a 17-29
loss at Wisconsin on Jan. 31.

The integration-ready package therefore normalizes Jan. 25 to Minnesota and
Jan. 31 to Chicago. Dates, scores, results, H/A/N, and Red Gym assignment are
unchanged. The original Wisconsin opponent labels and `raw_text` remain
preserved as source evidence. The immutable RESEARCH_FROZEN ZIP is unchanged.
