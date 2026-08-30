# Oklahoma source notes

## Primary school source

**University of Oklahoma, 2024-25 Men's Basketball Media Guide** (`2024-25_Men_s_Basketball_Media_Guide_compressed(1).pdf`). Primary extraction source for 1907-08 through 2023-24.

High-value sections used directly:

- General Information / Quick Facts
- Year-by-Year Records
- Regular Season Events
- Lloyd Noble Center History
- Year-by-Year Results
- Conference Championship history
- NCAA Tournament Results / records
- NIT Results / records

The guide identifies **1907-08** as Oklahoma's first basketball season. Its Quick Facts section reports an NCAA-adjusted record of 1,761-1,151 through 2023-24 and explicitly states that 13 wins from 2009-10 were vacated; it separately gives the actual on-court record as **1,774-1,151**. The package uses the on-court ledger and preserves the administrative action separately.

## Completed-season supplementation

**University of Oklahoma Athletics official 2024-25 schedule/results** supplies **34 competitive games, 20-14** after the guide cutoff. The Crimson & Cream scrimmage is excluded. The SEC Tournament and NCAA Tournament games are normalized using their official postseason context.

**University of Oklahoma Athletics official 2025-26 schedule/results and recaps** supplies **37 competitive games, 21-16**. The Wisconsin contest is explicitly an exhibition and is excluded. The season includes three College Basketball Crown games; these are classified `POSTSEASON`, with the West Virginia finale designated `Championship`.

## Owner-authorized conference-tournament site reference

**`Conference_Tournament_Site_Reference(20260825-203529).xlsm`**. The owner stated that the workbook is incomplete and is not universally reliable canon, but explicitly authorized the sections pertinent to Oklahoma's conference membership history as complete for Oklahoma. Only Oklahoma-relevant **Big Eight, Big 12, and SEC** tournament-site rows were used. This limited authorization must not be generalized to other schools or conferences.

The workbook is used for shared physical venue/city/state evidence only. It never establishes H/A/N by geography. Its early Big Eight chronology distinguishes campus preliminary rounds from the shared Kemper Arena phase; those boundaries are retained.

## Conference-tournament cross-check

Oklahoma's dedicated conference-championship section is used to verify tournament identity against the chronological ledger. Final QA identified five real tournament games whose year-by-year footnote markers had initially been missed during extraction:

- 1977-03-03 vs. Missouri — Big Eight Tournament
- 1989-03-11 vs. Iowa State — Big Eight Tournament
- 2013-03-14 vs. Iowa State — Big 12 Championship
- 2017-03-08 vs. TCU — Big 12 Championship
- 2024-03-13 vs. TCU — Big 12 Championship

After correction, the package reproduces the dedicated component records of **23-16 Big Eight** and **24-24 Big 12**. The guide's printed overall headline, `46-39`, is internally incompatible with those component totals (which sum to 47-40) and is retained only as a documented source defect.

## 1971 NIT score conflict

The 1970-71 chronological year-by-year ledger records the March 22 NIT game as **Oklahoma 87, Hawai'i 88 in 2OT**. Oklahoma's dedicated NIT results table prints **Hawai'i 87, Oklahoma 86**. Oklahoma's later official retrospective of the game and independent archival schedule evidence support **Hawai'i 88-87 (2OT)**. The package therefore keeps the chronological 87-88 score, classifies the contest as `NIT`, assigns the supported Madison Square Garden/New York site, and documents the internal conflict rather than rewriting `raw_text`.

## NCAA Tournament site research

The media guide's dedicated NCAA history establishes Oklahoma's NCAA game universe and supplies date/round/site-city context for much of the history. Physical arena identities were supplemented from NCAA tournament site evidence and authoritative/established venue histories where necessary.

Acceptance standard achieved at research freeze:

- **76 NCAA Tournament rows**
- **76/76 with curated venue**
- **76/76 with city and state**
- no pre-1979 `R64` usage
- only project-controlled populated NCAA round values
- historical third-place/consolation games retain blank round where appropriate

The 1943 Western Regional third-place game against Washington remains `NCAA_TOURNAMENT` with blank canonical round rather than receiving an invented modern label.

## H/A/N and venue hierarchy

1. explicit game-level `at` / `vs.` / official home designation
2. explicit official postseason site/context
3. authorized conference-tournament shared-site evidence
4. established NCAA physical-site evidence
5. home-venue chronology only after a game is independently established as Oklahoma home

Venue or geography never creates an H/A/N classification.

The oldest year-by-year ledgers often omit exact calendar dates and physical venue names. Those fields remain blank unless another authoritative source supports them. The **762 remaining blank exact dates are intentional historical unknowns**, not extraction placeholders. Two previously blank dates were resolved during serialized implementation from stronger reciprocal official records.

The 1907-08 Epworth game is treated as source-program home because the guide's season H/A/N summary records zero neutral games and the three explicitly `at` games account for the complete 1-2 away record; this is documented as a source-internal classification rather than geography inference.

## Opponent normalization

Every distinct source opponent label used by the 2,996 game rows resolves through `opponents.csv`; **unresolved opponents = 0**. Historical aliases and institutional renames are normalized to established program lineages where supportable. Historical clubs, military teams, non-current colleges, and other genuinely distinct opponents remain separate identities rather than being forced into modern Division I programs.

## Source preservation and administrative policy

Literal media-guide wording, including source typos, historical labels, and conflicting dedicated-table text, remains in `raw_text` or documentary notes. Structured normalization is not used to erase the source assertion.

Thirteen 2009-10 wins carry `VACATED_WIN` administrative metadata while retaining their actual played scores/results. The package does not rewrite on-court history to match later NCAA record adjustments.

## Research baseline and venue IDs

Repository schemas/shared references were inspected against:

`research_base_sha=2899c45e7b8dc2b8553c8b9e2342715a9a091484`

Every `VEN-99xxxx` value in this research package is deliberately provisional. The Implementation lane must perform authoritative physical-identity reuse and numeric-ID reallocation against current main before `INTEGRATION_FROZEN`.

## Implementation H/A/N normalization repair

The serialized implementation audit rechecked the year-by-year ledger against
the source hierarchy above and found a parser omission beginning in the dated
ledger format. Explicit preserved `at` / `vs.` wording had not populated
`source_site_candidate` on 230 rows.

- 205 explicit `at` rows: corrected to `OPPONENT_HOME`
- 25 explicit `vs.` rows: corrected to `NEUTRAL`
- 136 unsupported Lloyd Noble Center / Norman home-chronology fallbacks removed
- 1907-08 Epworth exception retained exactly as previously researched
- literal `raw_text` preserved for every row

This is a normalization repair from already-preserved primary-source evidence,
not a new geography-based H/A/N inference.

## Implementation final reciprocal-source normalization audit

Before Owner Gate 1, the serialized implementation lane performed one final
comparison of preflight conflicts against reciprocal official school records.
Seventeen Oklahoma structured rows were corrected where the historical fact
was deterministically established rather than left as an owner judgment.

The corrections comprise date, overtime, H/A/N, and supported location/venue
metadata only. The most important repairs are the previously undated
1916 Missouri and 1948 Ohio State games, the 1983 Big Eight campus
quarterfinal against Kansas, and the 2016 Texas road game.

The literal Oklahoma `raw_text` remains untouched on all 17 rows. Scores,
played results, opponent identities, game classifications, and administrative
statuses were not rewritten. Remaining source-vs-canonical disagreements are
left for the authoritative reconciliation review rather than silently
harmonized.

## Implementation opponent-registry normalization repair

Pre-seal deterministic site generation exposed two opponent relationship
normalization defects without changing Oklahoma's literal source evidence.

- `centenary` retains its established historical opponent key, with canonical
  display normalized from `Centenary (La.)` to the project-stable `Centenary`.
- Two Oklahoma games previously assigned to non-registry key `miami-ohio`
  were corrected to current Division I registry key `miami-oh`, with canonical
  display `Miami (OH)`.

The affected Oklahoma `source_opponent_label` and `raw_text` values remain
unchanged. This is relationship/identity normalization, not a rewrite of the
school's historical source wording.

## 2003-12-06 Michigan State identity/site integration repair

Pre-seal canonical accounting found that `OKLRAW-02250` was already present
in the Oklahoma ledger but had been normalized to orphan opponent key
`mich-state`, causing the game to be treated as new even though Michigan
State onboarding had already created canonical game `CBBG-0048496`.

Integration QA corrected the normalized identity to current Division I
registry key `michigan-state` / `Michigan State`. Oklahoma's literal source
label `Mich. State` and raw text remain unchanged.

Oklahoma's official game box score identifies the game site as Auburn Hills,
Michigan (`The Palace`). The Oklahoma school venue relationship therefore
reuses global physical venue `VEN-000206` (`the-palace-of-auburn-hills`).
Michigan State's official historical evidence independently corroborates the
game date, 80-77 overtime result, and Auburn Hills neutral setting.
