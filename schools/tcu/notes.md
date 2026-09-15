# TCU men's basketball — Stage 4 research portfolio notes

## Status

- `research_base_sha`: `0b8cf20e3b14517031a5a0e62b362883966e51c1`
- Program-perspective scope: `INCEPTION+`
- Competitive games: **2,862**
- On-court record: **1,357-1,505**
- Covered through: **2025-26**
- Exhibitions/noncompetitive events excluded.
- Stage 4 package QA: **PASS**
- Owner NON_D1 sanity scan: **READY, NOT YET PERFORMED**
- This package is not `RESEARCH_FROZEN`; Stages 5-7 remain.
- Current-main shared-reference rebase remains mandatory before tracked Implementation.

## Stage 1 game universe

The controlling row-level universe is the accepted 2,862-game Stage 1 ledger. Literal source evidence remains in `raw_text`.
Accepted narrow corrections and exclusions are preserved in the durable Stage 1/3B artifacts rather than erased.

The project preserves on-court results independently from administrative treatment. The 1995-96 Purdue game therefore remains an on-court loss with the source's forfeit treatment preserved separately.

## Opponent identity

Stage 2 resolves every row to a canonical historical opponent identity.

- unresolved identities: **0**
- known current-program key splits: **0**
- ambiguous current-program matches: **0**
- distinct working NON_D1 identities: **112**

The complete NON_D1 presentation and the informational self-corrected-current-D1 list are emitted as Stage 4 support artifacts for the required Stage 5 owner checkpoint.

## H/A/N and physical sites

All 2,862 games have explicit H/A/N classification; `UNKNOWN` H/A/N = **0**.

- researched-unresolved HOME physical venue rows: **24**
- HOME rows missing city/state: **0**
- neutral rows missing venue/location: **213/201**
- postseason rows missing venue/location: **29/0**
- NCAA physical venue + city/state gaps: **0**
- ambiguous physical venue identities: **0**

The 24 HOME venue-only unknowns are confined to 1913-14 through 1916-17. HOME status and Fort Worth, Texas are established, but reviewed evidence does not safely establish a specific physical building. They retain `RESEARCHED_UNRESOLVED_HOME_VENUE` rather than an invented arena.

## Postseason

Final competitive partition:

- regular season: **2736**
- conference tournament: **80**
- NCAA Tournament: **20**
- NIT: **24**
- other postseason: **2**

TCU research found **no conference-tournament appearance before Southwest Conference membership**. This is a TCU-specific finding from the complete game ledger plus TCU's tournament history; it is not a claim that the TIAA never used basketball playoffs.

The December 1953-60 events styled "Southwest Conference Tournament" were midseason invitationals and remain `REGULAR_SEASON` under project policy. The SWC Postseason Classic population is treated as conference postseason. The March 6, 1951 Texas A&M championship/NCAA-bid playoff is also classified as conference postseason.

## Conference chronology

- Independent — 1908-09
- Texas Intercollegiate Athletic Association — 1909-10 through 1922-23
- Southwest Conference — 1923-24 through 1995-96
- WAC — 1996-97 through 2000-01
- CUSA — 2001-02 through 2004-05
- Mountain West — 2005-06 through 2011-12
- Big 12 — 2012-13 onward

The TIAA historical identity is not present in the recorded research-base conference registry. Its package key is research-local and must be registered/rebased during serialized Implementation.

## Venue identity

`venues.csv` contains **30** local physical venue relationships used by the curated game ledger.
Known naming-era aliases are intentionally kept on one physical key where research established the same building.
Research-local `VEN-990xxx` numbers are provisional and are not authority to allocate global IDs; serialized Implementation must rebase every shared venue against current `main`.

## Remaining research lifecycle

Stage 4 is mechanically complete. The next stage is the mandatory owner NON_D1 sanity scan. After that approval, Stage 6 performs the bounded adversarial self-challenge; Stage 7 alone creates the immutable `RESEARCH_FROZEN` package.


## Stage 4 mechanical closeout repair

The 18 December 1953-60 games styled by TCU as the "Southwest Conference Tournament" had already been
correctly restored to `REGULAR_SEASON` in Stage 3B, but their H/A/N fields remained blank because they had
originally been deferred from Stage 3A. TCU's All-Time Tournament Results explicitly places these events in
**Houston**. They are therefore `NEUTRAL` from TCU's perspective, with Houston, Texas populated and the exact
physical building retained as `RESEARCHED_PARTIAL` rather than inferred.


## Stage 5 owner challenge correction — Corpus Christi

The historical `Corpus Christi` opponent was initially carried as NON_D1. Owner review correctly challenged
that classification. The historical **University of Corpus Christi** is in the institutional lineage of
present-day **Texas A&M-Corpus Christi**, so the affected game is now canonicalized to
`texas-a-m-corpus-christi` with `current_d1 = Yes`.

**Austin College remains a separate NON_D1 institution and is not the University of Texas.**


## Stage 6 adversarial pre-freeze self-challenge — final

Stage 6 did not merely accept the Stage 4 site debt. It challenged the neutral-site population against TCU's
own All-Time Series Results and modern official schedules.

The challenge produced two material corrections:

1. **Neutral location recovery.** All surviving NEUTRAL games now have city/state. TCU's All-Time Series Results
   supplied exact-date locations for the historical tournament population, while official TCU schedules/box scores
   resolved the modern residuals.
2. **Ten false-neutral HOME games corrected.** These were regular-season event/challenge rows whose source symbols
   had been over-read as neutral-site indicators. Official TCU schedules/recaps establish them as TCU HOME games:
   Texas Tech (2000-12-28), UTSA and Baylor (2001-12-15/29), Shawnee State and Old Dominion (2004-11-21/25),
   St. Gregory's (2009-12-20), Auburn (2017-01-28), Providence (2020-12-09), LSU (2022-01-29), and Xavier
   (2024-12-05).

Final all-game H/A/N:
- SOURCE_PROGRAM_HOME: **1392**
- OPPONENT_HOME: **1163**
- NEUTRAL: **307**
- UNKNOWN: **0**

Final publication-safety debt:
- neutral city/state gaps: **0**
- HOME location blockers: **0**
- researched-unresolved HOME physical venue rows: **24**
- exact-date unknown rows: **170**
- NCAA physical venue/city/state gaps: **0**
- unaccounted material site gaps: **0**

The 24 HOME venue-only unknowns remain confined to 1913-14 through 1916-17. TCU HOME status and Fort Worth are
established; the reviewed facility chronology does not safely identify a building before the named TCU Gymnasium
era, so no building was invented.

The 170 exact-date unknowns remain confined to 1908-09 through 1937-38. The adversarial pass checked the
institutional all-time series/result material for a systematic recovery path; no safe opponent-aware mechanical
recovery exists for this residual population. The current schedule interface's synthetic-looking January date
patterns remain rejected as evidence.

Owner Stage 5 correction is intact: Austin College remains separate NON_D1; historical Corpus Christi is in the
Texas A&M-Corpus Christi current-D1 lineage.

**PRE-FREEZE SELF-CHALLENGE: PASS.**


## 2026-09-14 bounded WAC venue amendment before Implementation

Implementation had not begun when the owner supplied an updated conference-tournament workbook with complete WAC
coverage. The pre-existing RESEARCH_FROZEN package had intentionally left TCU's WAC Tournament buildings unresolved
because the earlier owner workbook contained no WAC rows.

This amendment is deliberately narrow. It does **not** reopen the TCU game universe, opponent normalization,
H/A/N research, NON_D1 review, early exact-date debt, early HOME venue debt, or any non-WAC conference tournament.

Ten TCU WAC Tournament rows were enhanced:

- 1996-97, 1997-98, 1998-99: **Thomas & Mack Center, Paradise, Nevada** (7 TCU games total)
- 1999-00: **Selland Arena, Fresno, California** (2 TCU games)
- 2000-01: **Reynolds Center, Tulsa, Oklahoma** (1 TCU game)

The updated workbook says the entire WAC Tournament was at the listed shared venue in each of those seasons.
It also identifies those buildings as the regular home venues of UNLV, Fresno State, and Tulsa respectively.
None of TCU's opponents in the affected games was the venue's regular home program, so all ten previously researched
`NEUTRAL` classifications remain unchanged.

For 1996-97 through 1998-99, the workbook's municipality field is **Paradise, NV**, replacing the frozen package's
broader `Las Vegas, NV` locality label. No score, opponent, date, result, postseason taxonomy, or H/A/N value changed.

This amended freeze supersedes the earlier TCU RESEARCH_FROZEN package solely for downstream Implementation input.
The earlier immutable package and hash remain part of the audit trail.

## Implementation acceptance normalization

Original immutable RESEARCH_FROZEN v2 ZIP SHA-256: `5487bd4874ebda7b71df36e1abf86a6849cfc86d2abb18b0f03f5d9783f08c33`. For current permanent-schema acceptance only, 2,861 integral score strings serialized as `N.0` were normalized to `N`, and 50 fully resolved rows had site-research provenance moved into row notes because the current schema reserves `site_research_status`/`site_research_basis` for material-gap accounting. No historical judgment, result, opponent, date, game universe, H/A/N classification, or unresolved material-gap conclusion changed. Current-main venue-key reconciliation also maps settled same-physical identities to the authoritative keys before serialized Integration.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=2495f17cc4cf12d4631648dc738efb11131b69da` from `research_base_sha=0b8cf20e3b14517031a5a0e62b362883966e51c1`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
