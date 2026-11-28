# New Mexico ordinary complete-institutional Research — Stage 1 checkpoint 0004

**State: `STAGE_1_COMPLETE`. STOP before Stage 2.** This is one bounded
Stage 1 closeout transaction, not an ordinary-school Implementation or an
All-History Expansion lane.

**School:** University of New Mexico (`new-mexico`). **Research branch:**
`research/new-mexico`. **Immutable research_base_sha:**
`242370fc551fd749c157c74d92917ddfafbe40e0`.
**Immediate parent Research commit:**
`b0bedfd103aed100bf0c74bde9d957c1180c4b2e`, checkpoint `0003`.

**Owner scope authority:** `INCEPTION+`, **final**; supersedes the current
protected-main baseline `1950-51+` for this target school. The durable
`research/new-mexico/stage4-authoring/institutional-scope.json` is unchanged;
Research does not write protected main or global reference data. The later
serialized target Implementation will reconcile that single target scope row
under its own guarded Phase 0 authority.

## Source universe and cutoffs

The exact source PDF is University of New Mexico, *2026–27 New Mexico
Basketball*, SHA-256
`94a121232efa82a71ebb448139d4e72c799ac032128cb625ce2a5178b6bbdcc7`.
Its page 3 expressly dates men's varsity inception to **1899–1900**.
Its physical year-by-year results pages 121–132 cover 1899–1900 through
**2025–26**. `primary_source_historical_cutoff=2025-26` and
`required_completed_season_cutoff=2025-26`; there is no missing completed
season to supplement. Physical pages 44–45 contain all-time year records,
page 50 coaching records, and page 79 the exhibition appendix.

The 127 heading positions include 123 active competitive seasons and four
literal No Team seasons: 1900–01, 1903–04, 1917–18, 1920–21. The source
prints the third as `1907-18 (No Team)` between 1916–17 and 1918–19; that
historical source typography is preserved in census provenance.

## Accepted Stage 1 universe

**2,891 unique games**, on-court **1,667 W / 1,224 L**. Structured game types:

| game_type | rows |
| --- | ---: |
| REGULAR_SEASON | 2,727 |
| CONFERENCE_TOURNAMENT | 93 |
| POSTSEASON (NIT and one NAIA) | 44 |
| NCAA_TOURNAMENT | 27 |

The ledger is game-level and includes stable research-local IDs, original
source date tokens, opponent spelling, game text, W/L, literal score,
source PDF page/column, preserved site tokens, curated numeric scores with
provenance, original notes and overtime, and source-justified game_type on
**every** row. H/A/N remains `UNKNOWN` until authorized later site work:
**no geography-based assignment was made**.

Mechanical checks: all 2,891 IDs unique; 0 same-date/normalized-opponent
potential double entries; 0 dates outside assigned season; 0 inconsistencies
between 2,890 supported numeric scores and W/L; 123 season-game ledger counts
match the accepted census; 4 explicit no-team seasons remain without games;
all game types have basis text. `stage1-status.json` contains machine-readable
counts and pass conditions. Never convert distinct played games into duplicate
representations solely because the same opposing organization recurs.

## Exhibition and historical touring-team closeout

The guide's page 79 exhibition appendix includes **87** entries. **86** are
separately preserved in `excluded-exhibitions.csv` and are **not** in the
accepted 2,891-game ledger. Its remaining one is 2019-11-06 Eastern New Mexico,
which the same university book and its official game-one box score include in
UNM's countable 2019–20 season. Prior checkpoint 0003's exact target-specific
adjudication stands; the contradictory appendix label remains preserved and
the game is never double counted.

The three 1930s **Harlem Globetrotters** games are accepted for this target
school as historical competitive institutional results, not excluded solely
by the opponent's touring identity. They are precisely:

- `NM-1936-37-0006`: 1937-01-04, L 33–43;
- `NM-1937-38-0003`: 1937-12-16, W 43–41;
- `NM-1937-38-0004`: 1937-12-17, L 29–34.

The current official record book counts them in the season's played results;
older 2013–14 and 2021–22 UNM official books preserve the same matchups, and
contemporaneous-era athletic source histories from other universities also
record Globetrotters fixtures in their game seasons. Notre Dame's archival
history says the Globetrotters played serious competitive basketball during
the 1930s and 1940s. One bounded date-specific newspaper/archive discovery
pass did not uncover an explicit game-specific exhibition designation. This
is **not** a universal finding that all touring-team matches counted, nor a
claim to have disproven every potential exhibit label. It is a defensible
source-specific acceptance of three games already in UNM's season accounting,
with no affirmative contrary exhibition source. New specific archival
contradiction would justify narrowly reopening those IDs; not generic
re-search by opponent identity.

Primary corroborating source URLs:

- https://storage.googleapis.com/golobos-prod/2020/06/2046e7c4-2560547.pdf
- https://storage.googleapis.com/golobos-prod/2021/11/3bc8f8ba-2022mbb_recordbook.pdf
- https://archivesspace.library.nd.edu/repositories/3/resources/2442
- https://storage.googleapis.com/sdsu-prod/2024/11/05/8FOOxh4NhmLHssh3GdGM0JO1ED29s4yERYKjavER.pdf

## Literal source discrepancies and accepted corrections

The historical accounting contradiction is *not* repaired by a manufactured
game. Detailed game records establish 1,667–1,224; the source's page 3 overview
says 1,667–1,223, and its separate all-time season table sums to
1,666–1,226. Four season exceptions are explicitly reconciled:

- **1918–19:** Detailed six games 2–4 and all-time/coaching 2–4, despite
  source results heading 4–1.
- **1940–41:** Detailed 23 games 5–18 and all-time/coaching 5–18,
  despite source results heading 5–17.
- **1929–30:** Detailed 20 games 16–4 and coaching 16–4;
  separate all-time table erroneously lists 16–5.
- **1979–80:** On-court 7–21 includes 1979-12-04 West Texas A&M **W 112–100**;
  the source labels it a forfeit and administratively reports 6–22.
  Keep played game and literal administrative note separate.

The single 1967 NIT victory over Syracuse retains printed `6-64` but is
curated 66–64 using the same guide's separate NIT summary. Six additional
scores whose sources print four digits without a separator or use `=` were
read directly against the original PDF images, retaining literal tokens:

| Game | Source literal | Curated W/L score | PDF page |
| --- | --- | --- | ---: |
| 1949-02-04 at UTEP | 5153 | L 51–53 | 123 |
| 1956-12-28 vs UTEP | 65=78 | L 65–78 | 124 |
| 1974-01-26 Colorado State | 5449 | W 54–49 | 126 |
| 1987-12-26 North Texas | 77=69 | W 77–69 | 127 |
| 1989-11-24 Hardin-Simmons | 9157 | W 91–57 | 128 |
| 2006-02-04 Utah | 6453 | W 64–53 | 130 |

## Exact terminal Stage 1 uncertainty

All remaining Stage 1 items are nonblocking field or source-aggregate debt,
recorded row-level or source-section-level in `stage1-residuals.csv`.
Only `NM-1933-34-0001`, an explicitly listed 1933–34 **at Belen Merchants W**,
has no exact date or score; it is a distinct opponent-host result alongside
two separately dated *home* Belen Merchants games. The 1933–34 accepted
**16–4** detailed game record includes it, and its identity and on-court W
are sufficient for Stage 1 inclusion. Neither date nor score is invented.
The source aggregate contradiction and the 2019 appendix disagreement remain
separately documented, along with old year-summary typos.

**Stage 1 universe blockers: 0. Pending owner decisions: 0.** These explicit
residuals are not permission to re-open completed Stage 1 work during Stage 2
without a concrete contradictory source.

## Recovery payload and next stage

- `accepted-source-games.csv` — authoritative 2,891-row Stage 1 ledger
- `season-census.csv` — all 127 source heading slots, reconciled
- `excluded-exhibitions.csv` — 86 explicit exhibition exclusions
- `exhibition-appendix-crosswalk.csv` — complete 87-row raw appendix including exception
- `rejected-layout-fragments.csv` — unchanged checksum of 44 layout non-games from checkpoint 0002
- `adjudication-log.csv` — accepted source/historical decisions and audit
- `stage1-residuals.csv` — four exact nonblocking residual classes
- `stage1-status.json` — terminal census/verification metrics
- `manifest.json` — hash/size proof and immutable parent/base provenance

Every checkpoint-0001/0002/0003 artifact remains intact and addressable on
the same Research branch. Final institutional/scope authority remains in
`research/new-mexico/stage4-authoring/institutional-scope.json`.

**NEXT OWNER-FACING STAGE: Stage 2 opponent-identity Research, only after
owner says `Proceed`.** No Stage 2, Stage 3, Stage 4, Research Freeze,
Implementation, main mutation, or shared-reference registration is authorized
by this Stage 1 completion.
