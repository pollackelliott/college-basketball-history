# Canonical partial city/state census — exact protected-main baseline

- **Protected main examined:** `0a28151cf0c193afea2641cc5bd6f5557ab76d5b`.
- **Canonical input Git blob:** `f15273947ee600dd6e9a7917569041ca8caf27fc` (`data/canonical/games.csv`).
- **Total canonical games:** 186,583.
- **One-sided location rows:** **256**.
- City present, state absent: **256**. State present, city absent: **0**.
- Site categories: **185 NEUTRAL**, **61 TEAM_A_HOME**, **10 TEAM_B_HOME**.
- Game types: **222 REGULAR_SEASON**, **34 CONFERENCE_TOURNAMENT**.
- By season-start era: **86 before 1950**, **107 from 1950–1995**, **31 from 1996–2009**, and **32 from 2010 onward**.
- All 256 have **both venue ID and venue key blank**.
- **84 distinct preserved city/location strings**. Several are geographic regions or countries, not established city-level localities; do not blindly map all to US states.
- Exact row-by-row reproducible baseline: `docs/audits/canonical-partial-site-base-20261101.csv`.

## Population classification before repair

**1 source-supported shared-data repair candidate** (Dayton–Kansas, November 27, 2019):

- Canonical game: `CBBG-0014299`.
- Existing shared canonical state: `NEUTRAL`, city/location literal `Maui`, blank state, blank venue.
- Existing Kansas institutional source row: `schools/kansas/source-games.csv`, `KURAW-03139`, raw text says `Maui, Hawai’i`, Kansas 90–84 Dayton in overtime.
- Exact supported change: fill **only** `site_state=HI`. Keep existing `site_city=Maui`, `site_type=NEUTRAL`, blank venue and original scores, identity, notes, assertions, and source records unchanged.
- Authority spec: `data/maintenance/canonical-location-dayton-kansas-2019-11-27.json`.
- This is not an inferred H/A/N or a fabricated venue; Kansas's retained institutional text explicitly names the state.

**255 remaining inherited partial-location rows**:

- The complete population is identified and individually serialized in the audit CSV, including school participants, dates, site types, source-city literal, and current venue blankness.
- These are **unadjudicated shared-data coverage debt**, not 255 cases proved unsolvable or proved incorrect. No blanket location inference or venue assignment is authorized.
- Future maintenance may group them by source family and fix only those for which source-grounded exact state/country/locality evidence is established.
- Independent Research and other school implementations must not assume an unverified partial site is a valid complete location. A generic Stage 2 detector should surface a confident source match to such a game *during the capability census*, rather than surprising the project only at proposal rehearsal.

## No silent acceptance bypass

A missing city/state partner remains invalid under the ordinary complete-location check when a canonical game is touched. Do not weaken the final reconciliation invariant, suppress the incomplete location as an acceptable final state, or modify the saved Dayton recommendation map.

The baseline audit is immutable evidence of the population *before* any repair. If the exact one-field Kansas-backed correction is later applied and approved via protected-main PR, the repository would have 255 surviving partial canonical rows until independently authorized follow-up maintenance resolves them. The historical records for the other 255 remain unchanged.

**Maintenance-branch correction executed and verified:** a temporary, branch-only guarded GitHub workflow ran the exact source-backed repair tool and committed only `data/canonical/games.csv`, changing **one row / one field** for `CBBG-0014299` from blank state to `HI`. The resulting Git blob is `7ae2e7cde0ec91a7f9168a57b9646cfc1fcb9e9c`, and resulting file SHA-256 is `fd51e76dee090ffed9c7b4565aebf55838bcafb765b680082441dbfcbce89099`. GitHub compare independently confirms exactly one line deleted and one added, with no adjacent or unrelated rows changed. The temporary workflow was removed from the maintenance branch before final PR review and will not be merged.

**Post-merge expectation:** the remaining partial canonical population becomes **255**; the immutable 256-row CSV remains an audit of the *pre-repair* state, not a demand to undo this one evidence-based change. This narrow shared-data correction is not a change to Dayton's Research Freeze, Integration Freeze, onboarding branch, or recommendation-map decisions.

**Protected-main boundary:** a maintenance-branch commit is not final adoption. Require the exact-head repository tests and transaction rehearsal, then the ordinary reviewed protected-main PR merge and exact resulting-main confirmation before instructing Dayton to recover.
