# Clemson research package notes

## Stage 6 status

- School: Clemson
- Research stage: `STAGE_6`
- Stage 6 disposition: final adversarial self-challenge **PASS**; bounded representation repairs applied; Stage 7 immutable packaging **not yet authorized**
- Immutable `research_base_sha`: `e57a7049b2315508e59fd68b4324c34050901f45`
- Protected-main SHA checked during this bounded Stage 6 unit: `4712a2d796c809a92dbde91e30ebf489f783ac76`
- Accepted history scope: `INCEPTION+`
- Covered seasons: 1911-1912 through 2025-2026 (115 seasons)
- Competitive source rows: 2867
- On-court record represented by the accepted source ledger: 1478-1388-1
- Exact-date debt preserved from Stage 1: 2 rows
- Exhibitions/noncompetitive events: excluded from the accepted competitive universe

This package carries forward the accepted Stage 1 through Stage 3B durable state plus the owner-approved Stage 5 NON_D1 disposition. Stage 6 challenged the accepted residual debt populations under current policy and did not reopen completed historical adjudications without a concrete reason.

## Game-universe and source preservation

The source spine is Clemson's 2026-27 men's basketball media guide All-Time Results section. Literal row evidence is preserved in `raw_text`; the accepted Stage 1 source-internal score correction remains in row notes rather than rewriting the literal evidence. The three 1989-90 NCAA rows marked by Clemson as vacated preserve the on-court score/result. Stage 6 normalized the legacy package token to the current controlled vocabulary: the two on-court wins use `VACATED_WIN`, and the on-court loss uses `VACATED_GAME`; the original administrative note and literal `raw_text` remain preserved.

The media guide's `^` overtime notation is applied mechanically to `overtime_periods`; repeated carets are preserved as multiple overtime periods. The two rows with unknown exact date remain blank rather than receiving inferred dates.

## Opponent identity

- Distinct accepted opponent keys: 290
- Source-label-to-opponent mapping rows: 340
- Unresolved opponent identities: 0
- Distinct working NON_D1/non-current-D1 identities for the required owner sanity scan: 51 (121 games)
- Current-D1 classification was checked read-only against protected main `4712a2d796c809a92dbde91e30ebf489f783ac76`.
- The same literal label `Saint Francis` occurs in two eras and remains separately resolved to `st-francis-brooklyn` (1983-84) and `saint-francis-pa` (2024-25); this is preserved rather than collapsed.

The complete Stage 5 owner-scan population was approved by the owner on 2026-09-27 with zero flagged identities. That approval is preserved in the Stage 5 checkpoint and carried into this Stage 6 checkpoint.

## Conference chronology

- 1911-1912 through 1920-1921: Independent
- 1921-1922 through 1952-1953: Southern Conference
- 1953-1954 through present: ACC

The Clemson media guide year-by-year headers provide the chronology: 1920-21 is overall-only, 1921-22 is the first SOCON season header, and 1953-54 is the first ACC season header. Conference membership is not used to infer individual postseason classification.

## H/A/N and site completeness

Across all 2867 accepted games:

- source-program HOME: 1345
- OPPONENT_HOME: 1132
- NEUTRAL: 390
- UNKNOWN H/A/N: 0
- HOME rows missing city/state: 0
- HOME rows with researched-unresolved exact venue: 75
- NEUTRAL rows missing city/state: 0
- historical regular-season NEUTRAL rows with explicitly researched exact-building debt: 115
- postseason rows: 188
- postseason exact-venue gaps: 0
- postseason city/state gaps: 0

The 75 HOME exact-venue blanks are accepted `RESEARCHED_UNRESOLVED_HOME_VENUE` rows with Clemson, SC established. They are confined to the pre-Holtzendorff multi-site era and the 1922-29 campus-gym identity interval. The 115 regular-season neutral building blanks are `RESEARCHED_PARTIAL` historical enrichment debt; all have supported locality and fall on the historical side of the modern exact-venue standard. No postseason row uses that historical regular-season shortcut.

Ordinary regular-season OPPONENT_HOME physical-building blanks remain outside Clemson's source-school archaeology responsibility.

## Clemson HOME facility chronology

- Before 1916-02-01: Clemson, SC established; individual home game could be Riggs Field or the Sikes Hall basement, so exact physical site remains researched unresolved.
- 1916-02-01 through 1922-01-12: Holtzendorff YMCA.
- 1922-01-13 through 1930-01-06: Clemson, SC established; the consulted institutional evidence does not support one canonical physical venue identity for every home row.
- 1930-01-07 through 1968-11-29: Fike Field House (same physical building originally called Clemson Field House).
- 1968-11-30 onward: Littlejohn Coliseum, except documented temporary-home intervals.
- 2002-11-24 through 2002-12-31: Civic Center of Anderson during Littlejohn renovation.
- 2015-11-13 through 2016-03-01: Bon Secours Wellness Arena during Littlejohn rebuild.

## Postseason closeout carried forward

Stage 3B remains closed at 188 postseason rows:

- conference tournament: 121
- NCAA Tournament: 30
- NIT: 37
- unclassified postseason: 0
- exact postseason venue + locality complete: 188/188

The accepted 1998-99 correction remains closed: `CLEM-R-1998-030` Florida State is ACC Tournament, not NIT, and `CLEM-R-1998-032` Rutgers is NIT. The Rutgers game's historical Louis Brown Athletic Center evidence is preserved while the physical venue is represented through current protected-main `Jersey Mike's Arena` / `VEN-000095`.

`CLEM-R-2001-030` remains the deliberate date/site split: the frozen Stage 1 date is 2002-03-03, while exact-event evidence identifies the same 84-91 OT Florida State ACC Tournament game on 2002-03-07. Stage 3B resolved classification and Charlotte Coliseum II site without reopening the frozen date field.

## Physical venue reconciliation

The assembled package contains 81 distinct physical venue relationships:

- 75 reuse protected-main physical venue identities;
- 6 are historically resolved Research identities with blank provisional numeric ID pending current-main rebase: Holtzendorff YMCA, Fike Field House, Civic Center of Anderson, Ted Constant Convocation Center, Titan Field House, and Coca-Cola Coliseum.

Research makes no protected-main shared-reference mutation. The known protected-main duplicate historical alias `Charlotte Coliseum I` on both Charlotte physical venue identities is recorded as a shared-reference representation issue; Clemson rows are physically unambiguous in this package because the 1955 and 1988 buildings are represented separately by their accepted physical IDs/eras.

## Accomplishment verification prepared for Implementation

The current owner baseline is supported by the accepted Clemson evidence:

- conference regular-season championships: 1 (1989-90 ACC; the media guide calls it Clemson's first/only regular-season ACC title)
- conference tournament championships: 1 (1938-39 Southern Conference Tournament)
- NCAA Tournament appearances: 16
- Final Four appearances: 0
- national championships: 0
- best NCAA finish: Elite Eight
- most recent best-finish year: 2024

This Stage 4 research verification does not mutate `data/reference/program-accomplishments.csv`; formal serialized Implementation authority remains later.

## Stage 6 adversarial self-challenge

`PRE-FREEZE SELF-CHALLENGE: PASS`

- `RESEARCHED_UNRESOLVED_HOME_VENUE`: 75 final rows. Nine are pre-Feb. 1, 1916 multi-site HOME games for which Clemson institutional history names Riggs Field or the Sikes Hall basement without row-level allocation. Sixty-six are in the 1922-29 campus-gym interval; Clemson Libraries establishes the 1922 gym construction, and Virginia Tech supplies one 1925 exact reciprocal assertion as “Boxer Gymnasium,” but the evidence does not safely establish one canonical physical identity/name for every row. No broad unexplored modern HOME era remains.
- `UNKNOWN` H/A/N: 0.
- Unknown exact dates: 2 original/working, 0 recovered, 2 final (`CLEM-R-1919-008` Furman; `CLEM-R-1929-024` Wofford). The official modern opponent-history families do not extend to those games, so the remaining dates stay terminal historical debt rather than being inferred or pushed into newspaper archaeology.
- Regular-season neutral debt: 115 historical (1995-96 and earlier) exact-building blanks, all with supported city/state and explicit `RESEARCHED_PARTIAL` accounting. Modern 1996-97+ neutral exact-building blanks: 0. Postseason exact-venue gaps: 0.
- Physical venue identities: 81 local relationships = 75 protected-main reuses + 6 genuinely new Research candidates pending current-main rebase; ambiguous physical identities: 0.
- Opponent identities: all 51 owner-scan NON_D1/non-current-D1 identities were checked against the current global program registry with zero exact current-D1 key/name collisions; focused modern/noncurrent review exposed no current-program split. Owner Stage 5 approval had zero flags.
- Authoritative Stage 3A row state remains present and its 2,867 source-game ID set exactly matches the package/Stage 1 universe.

Two deterministic representation defects were repaired without changing historical meaning: (1) three legacy `NCAA_PARTICIPATION_VACATED` values were normalized to the current controlled administrative vocabulary, and (2) 1,561 resolved rows that had a `site_research_basis` despite having no material site gap moved that basis verbatim into `notes` under `[RESOLVED_SITE_EVIDENCE]`, leaving `site_research_*` exclusively for unresolved material-gap accounting. Literal `raw_text` and all game facts are unchanged.

## Required next boundary

Stage 6 stops at `STAGE_6_COMPLETE_PRE_FREEZE_SELF_CHALLENGE_PASS_BOUNDARY`. Stage 7 immutable packaging and `RESEARCH_FROZEN` remain separately owner-authorized and have not begun.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=de4ccb88fc5550b66b514841000b1c5e04bd93f5` from `research_base_sha=e57a7049b2315508e59fd68b4324c34050901f45`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
