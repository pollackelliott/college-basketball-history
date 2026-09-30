# Florida State men's basketball — source notes

## Research provenance

- Research base: `7834d87207761087dfdbc19d5259042564cd4fb0`
- Protected `main` at Stage 4 assembly: `b2e013772f739cc044f0495d47237e34d5acdcc6`
- Program perspective: `1956-57+`
- Authoritative incoming checkpoint: `florida-state-stage3b-complete-checkpoint.zip`
- Incoming checkpoint SHA-256: `173dd66671d9f17c5aada1874244fc3d638b5070611257933d62038c89d03ce1`

### Primary institutional source

**Florida State men's basketball record book** (`FSU record book.pdf`)

- SHA-256: `739c568f38c034e33e3067b732d6f2b191559a057c508a206d328aee24389f6f`
- Primary evidence for the all-time game ledger, season summaries, H/A/N notation and accounting, event footnotes, conference chronology, NCAA/NIT histories, and accomplishment cross-checks.
- Literal game rows are preserved in `source-games.csv::raw_text`; accepted corrections change curated fields without rewriting literal evidence.

### Research hierarchy

1. Accepted project evidence at the immutable research base.
2. Florida State institutional record book / Athletics schedules, histories, articles and opponent histories.
3. Official NCAA/conference/tournament/host evidence where required.
4. Obvious opponent institutional/reciprocal evidence.
5. Targeted authoritative archival evidence for bounded residuals.

Unsupported inference was not used merely to fill H/A/N, venue, date, or opponent identity.

## Stage 1–3B durable research state

- Competitive universe: **2,079 games**
- Opponent identities resolved: **all**
- Regular-season Stage 3A: **COMPLETE**
- Postseason Stage 3B: **COMPLETE**
- Postseason exact venue/city/state: **150 / 150**
- NCAA exact venue/city/state: **41 / 41**
- Ambiguous physical venue identities: **0**

Accepted correction overlays:

- `FSU-STG1-CORR-012` — 2009 Georgia Tech row reclassified from regular season to conference tournament.
- `FSU-STG1-CORR-013` — Cincinnati date corrected from 2008-11-29 to 2008-11-28.
- `FSU-STG1-CORR-014` — Virginia Tech 63-53 corrected to 2009-03-08 regular-season Florida State HOME at Donald L. Tucker Civic Center.
- `FSU-STG1-CORR-015` — 2009 ACC championship Duke date corrected to 2009-03-15 with neutral Georgia Dome site and controlled `Championship`.

## Site research and Stage 4 venue reconciliation

Stage 4 does not reopen historical site research. It translates the accepted Stage 3A/3B row-level state into the six-file schema and mechanically reconciles physical venue identities against the research-base venue registry.

The package contains **75** venue relationships. **73** reuse research-base venue IDs. Two settled physical identities remain provisional:

- `VEN-990001` / `tully-gymnasium` — Tully Gymnasium, Tallahassee, Florida.
- `VEN-990002` / `mitchell-center` — Mitchell Center, Mobile, Alabama.

Those numeric IDs are research transport only. Serialized Implementation must rebase both against then-current protected `main`.

The surviving **109** historical regular-season neutral building blanks are deliberate location-first enrichment debt. Every such row has complete city/state and explicit `RESEARCHED_PARTIAL` / basis fields. No postseason row uses that shortcut.

## Conference evidence

The Florida State all-time-results legend identifies:

- Florida Intercollegiate Conference membership through 1956-57;
- Metro Conference membership from 1976-77 through 1990-91;
- Atlantic Coast Conference membership from 1991-92 to present.

Because project scope begins at 1956-57, the six-file chronology represents the final Florida Intercollegiate season, then the intervening Independent period, then `metro-1975`, then the ACC.

The research-base conference registry lacks the Florida Intercollegiate Conference. Research therefore carries a settled proposal:

- proposed key: `florida-intercollegiate-conference`
- name: Florida Intercollegiate Conference
- target-school usage: 1956-57
- Historical identity: `RESOLVED`
- Global registration: `PENDING_CURRENT_MAIN_REBASE`

## Accomplishment evidence

Florida State's NCAA tournament history explicitly reports **18 NCAA appearances**, one national-championship-game appearance and one Final Four (1972). The row-level tournament ledger independently has 18 NCAA appearance seasons.

Conference evidence supports regular-season titles in 1977-78 Metro, 1988-89 Metro and 2019-20 ACC, plus conference-tournament titles in 1990-91 Metro and 2011-12 ACC. Florida State finished national runner-up in 1972 and has no national championship.

## Known carried conflicts

Three source conflicts remain explicit research/reconciliation observations and are not silently normalized in this package:

1. 1980 NCAA vs Kentucky — Florida State date 1980-03-09 vs Kentucky 1980-03-08.
2. 1984 NIT vs NC State — Florida State 1984-03-15/neutral vs NC State 1984-03-13/home representation.
3. 2004 NIT vs Wichita State — Florida State 2004-03-17 vs Wichita State 2004-03-19.

Four already-published reciprocal representation defects are likewise carried for later maintenance/integration handling; Florida State Research does not mutate protected shared/published state.

## Stage 4 QA

The assembled six-file package passes the current `research-check` acceptance contract as reproduced from protected `main` at `b2e013772f739cc044f0495d47237e34d5acdcc6`:

- competitive games: 2,079
- source-game IDs unique: yes
- unresolved opponents: 0
- NCAA rows: 41, all venue/city/state complete
- invalid H/A/N: 0
- invalid game types/rounds: 0
- HOME publication blockers: 0
- material site-gap rows: 109
- researched/accounted material site-gap rows: 109
- unaccounted material site-gap rows: 0
- warnings: 0

Stage 5 owner sanity scan was subsequently approved with no flags: **27 NON_D1 identities / 110 games**.

## Stage 6 score / administrative-status repair evidence

Stage 6 challenged the five blank score pairs and explicit forfeit footnotes as one bounded source-representation class. Repairs preserve every literal `raw_text` value.

- `FSU-STG1-00385` — 1971-12-18 at Hawai'i: FSU record-book row/footnote preserves the 10-30 result and states the game was forfeited by Florida State; Hawai'i Athletics' 1971-72 schedule independently records `Forfeit`, W 30-10 at Honolulu International Center. Source: https://hawaiiathletics.com/sports/mens-basketball/schedule/1971-1972
- `FSU-STG1-00620` — 1980-02-07 Memphis State: FSU record-book footnote states `Game forfeited by Memphis State`; played score 55-54 is preserved and controlled `FORFEIT` status added.
- `FSU-STG1-00833` — 1987-02-26 Miami: FSU's OCR-damaged `08-84` literal remains in `raw_text`; Miami Athletics series notes independently list `FSU 108, UM 84` in Tallahassee. Source: https://miamihurricanes.com/news/2006/01/26/205542266-2/
- `FSU-STG1-00964` — 1991-12-07 Florida A&M: FSU's literal 2-0 result and footnote explicitly identify a forfeit win by Florida State; controlled `FORFEIT` status added.
- `FSU-STG1-01486` — 2008-11-22 Coastal Carolina: FSU's OCR-damaged `82-7-0` literal remains in `raw_text`; Coastal Carolina institutional box score confirms Florida State 82, Coastal Carolina 70. Source: https://goccusports.com/sports/mens-basketball/stats/2008-09/florida-state/boxscore/1924
- `FSU-STG1-01823` — 2018-03-18 Xavier: FSU's contradictory/OCR-damaged literal `W 75-79` remains in `raw_text`; Xavier institutional box score confirms Florida State 75, Xavier 70 at Bridgestone Arena. Source: https://goxavier.com/sports/mens-basketball/stats/2017-18/florida-state/boxscore/7116

No unsupported score was inferred from result flags or schedule order.


## Stage 4 representation observations

- `FSU-STG4-REP-001`: HP Field House is physically resolved as research-base `VEN-000084`. The accepted 2009 Old Spice Classic source locality is Lake Buena Vista, Florida, while the research-base physical venue registry stores Orlando, Florida. Stage 4 preserves the accepted source locality and carries this as a representation/current-main-rebase observation rather than reopening the physical-site conclusion.
- Informational current-D1 self-corrections: **98 canonical identities / 138 literal source-label mappings**. Literal labels remain preserved in `source-games.csv`; normalization is already resolved and is not part of the owner NON_D1 decision checkpoint.
