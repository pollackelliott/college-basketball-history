# North Carolina men's basketball — Stage 4 research portfolio notes

## Status

This is the Stage 4 six-file package assembled mechanically from the accepted North Carolina Stage 1–3B durable state.

- `research_base_sha`: `bb2fcf16dd8800e3d9b823c0b4999b2d1b516d6b`
- Program-perspective scope: `INCEPTION+`
- Competitive games: **3,302**
- On-court record: **2,419-883**
- Played/reconciled seasons: **116 / 116**
- Exhibitions/noncompetitive rows are excluded under the accepted Stage 1 universe.
- Stage 1–3B accepted work was not reopened.
- Stage 4 package QA: clean.
- Required owner `NON_D1` sanity scan: **APPROVED in Stage 5** — **74 identities / 256 games**, zero owner flags.
- Stage 6 adversarial pre-freeze self-challenge: **PASS after bounded repair**.
- This package is not yet `RESEARCH_FROZEN`; Stage 7 immutable packaging remains separately bounded.

## Accepted game universe and field repairs

The package preserves all accepted Stage 1 source-version/field-specific repairs, including the restored 1919-20 game population, the 2012-13 Maryland date repair, the 2017-18 Virginia Tech result repair, the 2024-25 Hawai'i local-date treatment, the 2024-25 Wake Forest score/result repair, and accepted 2025-26 overtime metadata. Literal source evidence remains in `raw_text`; row notes preserve the correction basis.

## Final H/A/N and site accounting

All-game H/A/N:

- North Carolina home: **1,282**
- Opponent home: **1,119**
- Neutral: **901**
- Unknown: **0**

Research-completeness controls:

- HOME rows missing venue: **0**
- HOME rows missing city/state: **0**
- regular-season neutral rows: **479**
- researched-unresolved regular neutral physical venue rows: **10** (all have complete city/state and explicit `RESEARCHED_UNRESOLVED` basis)
- conference tournament site gaps: **0 / 234**
- NCAA physical venue + city/state gaps: **0 / 186**
- NIT site gaps: **0 / 18**
- unaccounted material site gaps: **0**
- ambiguous physical venue identities: **0**

### Stage 4 physical-identity rebase

The game-level Stage 3 research is reconciled against `research_base_sha` into **130** physical venue relationships:

- definite research-base physical reuses: **101**
- genuinely new research candidates: **29**
- ambiguous physical identities: **0**

Two notable alias reuses resolved during package assembly are `Coliseo de Puerto Rico` -> existing José Miguel Agrelot Coliseum (`VEN-000471`) and `NRG Stadium` -> existing Reliant Stadium physical identity (`VEN-000172`). New-candidate numeric `VEN-99xxxx` values in `venues.csv` are provisional transport identifiers only; serialized Implementation must perform the authoritative current-main rebase.

Stage 6 supersedes the Stage 4 Orleans Arena geography treatment: Clark County's assessor identifies the arena's 4500 W Tropicana Ave parcel as the unincorporated town of **Paradise, Nevada**, so all six UNC Orleans Arena rows and the local venue relationship now use Paradise. Literal/source `LV` evidence remains preserved. State Farm Stadium remains normalized from source-city Phoenix to its physical location in Glendale, Arizona. H/A/N is unchanged.

## Postseason classification

Final postseason partition is **438** games:

- Southern/ACC conference tournaments: **234**
- NCAA Tournament: **186**
- NIT: **18**

Controlled championship-game rows:

- conference tournament: **48** (North Carolina won **26** of them: 8 Southern Conference + 18 ACC)
- NCAA Championship: **12** (North Carolina won **6**)
- NIT Championship: **2**

Historical non-championship conference/NIT rounds remain blank in the controlled round field while literal round evidence is preserved.

## Conference chronology

- Southern Intercollegiate Athletic Association — basketball inception 1910-11 through 1920-21
- Southern Conference — 1921-22 through 1952-53
- ACC — 1953-54 onward

UNC official history identifies the institution as an SIAA charter member in 1894, a Southern Conference charter member in 1921, and an ACC charter member beginning competition in 1953-54. The six-file program perspective begins only with accepted basketball inception in 1910-11.

## Accomplishment cross-check

The assembled ledger mechanically reproduces:

- conference tournament championships: **26**
- NCAA Tournament appearances: **55**
- Final Four appearances: **21**
- NCAA national championships: **6**
- best NCAA finish: **National Champion (2017 most recent)**

Current UNC institutional material explicitly states **40 regular-season conference championships**: 33 ACC plus seven Southern Conference first-place finishes. Current-main `program-accomplishments.csv` still contains an `OWNER_BASELINE_UNVERIFIED` value of **42**. This package preserves the evidence-supported **40** in research notes and treats the 42->40 difference as an accomplishment-reference correction for serialized implementation/review, not as authority to mutate global repository state from this Research lane.

## Opponent identity

All **3,302** games have resolved opponent identities.

- canonical opponents: **306**
- current-D1 canonical opponents: **232**
- `NON_D1` / historical canonical opponents: **74**
- `NON_D1` games: **256**
- unresolved opponent identities: **0**
- known current-program key splits: **0**
- ambiguous current-program matches: **0**

The complete 74-identity owner sanity-scan population was presented in Stage 5 and **approved by the owner with zero flags**. That durable disposition controls this package.


## Stage 6 adversarial pre-freeze self-challenge

**PRE-FREEZE SELF-CHALLENGE: PASS**

The bounded Stage 6 audit challenged the required residual/risk classes without reopening completed Stages 1–5.

- `RESEARCHED_UNRESOLVED_HOME_VENUE`: **0**
- UNKNOWN H/A/N: **0**
- unknown exact dates: **0**
- researched-unresolved regular neutral buildings: **10**, all 1916–1956, all with known city/state and row-specific evidence accounting
- postseason site gaps: **0**
- NCAA venue/city/state gaps: **0 / 186**
- opponent identities unresolved: **0**
- known current-program key splits: **0**
- ambiguous current-program matches: **0**
- physical venue relationships: **130 = 101 research-base reuses + 29 genuine provisional candidates**
- ambiguous package physical identities: **0**

The 10 unresolved neutral buildings were re-challenged as a class through exact-game searches, authoritative reciprocal/institutional histories where available, and event/locality evidence. The challenge produced no defensible building recovery. The surviving population is early/historical, fully site-accounted, has known locality, and lacks another comparable systematic/high-yield evidence class; it is therefore classified as **terminal researched historical debt** under project policy.

Stage 6 did expose three material evidence findings:

1. **Orleans Arena locality repair** — Clark County Assessor identifies the 4500 W Tropicana Ave parcel as **PARADISE**. The six UNC Orleans Arena rows and local venue row were corrected from Las Vegas to Paradise while preserving literal/source `LV` evidence.
2. **1916-02-07 Virginia score conflict** — Virginia Athletics' official all-time results reports Virginia W 30-24; UNC's controlling source reports UNC L 25-29. UNC source values remain preserved and the reciprocal conflict is serialized for later reconciliation.
3. **1940 Virginia Tech date conflict** — Virginia Tech's official archive reports 1940-01-10; UNC's controlling source reports 1940-01-11. Both agree on Winston-Salem and the 46-25 result; UNC source date remains preserved and the conflict is serialized.

Current protected `main` has advanced from the research base only through intervening integrations; the program registry change between `research_base_sha` and the Stage 6 main does not introduce a new opponent identity. The 13 post-base Colorado venue additions do not collide with North Carolina's 29 provisional new venue candidates. Current main does contain a later-added `Coliseo de Puerto Rico` venue row despite the research-base physical reuse already established at `VEN-000471` José Miguel Agrelot Coliseum; North Carolina retains the research-base physical identity and leaves current-main duplicate-reference cleanup to serialized Implementation.

No owner-level historical judgment is required.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=5177d4470061879d04b2211312f917dbd60382fd` from `research_base_sha=bb2fcf16dd8800e3d9b823c0b4999b2d1b516d6b`. Settled North Carolina shared-reference findings were reconciled mechanically during Implementation: Orleans Arena physical geography is canonicalized to Paradise, Nevada, and duplicate VEN-000476 is retired into VEN-000471. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
