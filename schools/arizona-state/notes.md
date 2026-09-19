# Arizona State research notes

- Research base SHA: `3989158d6e461a3dfb7be919586c5b388f8ef83d`.
- Protected `main` re-inspected during Stage 4: `9738fe4f54b813aad4d2a12344a2c8279c3590ee`.
- Current-main rebase remains required before tracked Phase 0; research-time global numeric venue IDs are provisional.
- Accepted competitive universe through completed 2025-26: **2,680 games; on-court record 1,391-1,289**. Exhibitions are excluded.
- Stage 2 opponent identity is complete: **310 distinct canonical/historical opponents**, **0 unresolved opponent identities**, and **68 distinct working NON_D1 identities** representing **252 games**.
- Stage 4 owner sanity scan is prepared but **not yet owner-approved**. The informational self-corrected-opponent artifact contains **192** accepted identity normalizations/corrections from Stage 2.
- Final H/A/N after Stage 3A + Stage 3B: **1,247 SOURCE_PROGRAM_HOME / 966 OPPONENT_HOME / 251 NEUTRAL / 216 UNKNOWN = 2,680**.
- The **216 UNKNOWN H/A/N** rows are accepted Stage 3A terminal researched historical debt. They remain explicit `UNKNOWN` rows with substantive `site_research_status/site_research_basis`; they were not reopened in Stage 4.
- Stage 3A retains **12 neutral physical-site residual rows** as explicit researched debt; no HOME venue residuals or HOME publication blockers remain.
- Stage 3B is complete: **98 postseason rows** classified and physically sited; NCAA site completeness is **33/33**, and all Stage 3B physical venue residuals are closed.
- Final game-type partition: **2,582 REGULAR_SEASON / 39 CONFERENCE_TOURNAMENT / 33 NCAA_TOURNAMENT / 20 NIT / 6 POSTSEASON = 2,680**.
- Exact-date debt: **444** rows remain blank after accepted Stage 3A date recovery/corrections; no date was inferred from schedule order or geography.
- Exact-score debt: **5** rows remain blank and are preserved as historical unknowns. All 2,680 rows retain a played W/L result.
- Five modern score-order/OCR defects were repaired field-specifically in Stage 4 from official Arizona State records while preserving literal `raw_text`: 1995 Stanford (ASU 75-91), 2011 Montana State (78-72), 2013 College of Charleston (80-58), 2015 Kennesaw State (91-53), and 2015 UNLV (66-56).
- The Stage 1 Cal Poly reciprocal insertion is preserved from the reciprocal source perspective in `raw_text`; structured result/score are mechanically oriented to Arizona State as **L 37-64**.
- Physical venue relationship table contains **104** identities: **47 research-base global reuses** and **57 research-local candidates**. Ambiguous physical venue identities remain zero at the Stage 4 research-base boundary.
- Accepted 1964 Utah State postseason correction remains **McArthur Court, Eugene, Oregon**.
- Conference chronology: Independent (1911-12 through 1930-31), Border Conference (1931-32 through 1961-62), WAC (1962-63 through 1977-78), Pacific-10 (1978-79 through 2010-11), Pac-12 (2011-12 through 2023-24), Big 12 (2024-25 onward).
- Accomplishment research reference for Implementation: **8 conference regular-season championships; 0 conference-tournament championships; 17 NCAA Tournament appearances; 0 Final Fours; 0 national championships; best finish ELITE_EIGHT (latest: 1975)**.
- Physical venue identity and geography never determine H/A/N.

## Stage 4 historical boundary

Stage 4 package assembly and package QA completed with the owner NON_D1 sanity scan ready. Stage 5 subsequently received owner approval with zero flags; Stage 6 subsequently completed the final adversarial self-challenge.


## Stage 6 final adversarial self-challenge

Stage 6 completed a whole-package adversarial challenge against the durable Stage 5 state, accepted reciprocal packages, the recorded research-base shared references, and protected current-main policy. It made only field-specific evidence-supported repairs and did not mutate protected main.

Accepted Stage 6 repairs include two 1938-39 Texas Tech site corrections to Lubbock, 15 reciprocal exact-date recoveries, the 1984 North Carolina Aoyama Gakuin Hall recovery, Oregon/McArthur Court enrichment, physical-identity reuse cleanup, and a final 1943-02-17 Texas Tech correction: the 41-46 game is neutral Border Conference tournament/postseason play in Albuquerque, New Mexico rather than Tucson regular-season play. Score, result, and literal raw evidence were preserved.

Final residuals are closed under bounded research convergence: **216 UNKNOWN H/A/N rows**, **429 blank exact dates**, **11 neutral non-NCAA rows without exact physical building**, and **19 researched physical venue identities pending serialized current-main rebase/registration**. All material site gaps carry substantive research accounting. No HOME publication blockers remain. NCAA site completeness is 33/33.

The remaining 19 blank numeric venue IDs are not historical uncertainty by default: their physical identities are researched, while authoritative global registration is intentionally deferred under `docs/shared-reference-authority.md`. Three carry explicit current-main identity conflicts/near-matches (`Robins Center`, `Rochester Community War Memorial`, `Baoshan Sports Center`) and must be reconciled rather than silently merged.

Final Stage 6 mechanical QA: **PASS — 0 errors, 0 warnings**. The only literal source labels that intentionally map to more than one identity are `New Mexico` and `Washington`; both are already documented, evidence-supported disambiguations in `opponents.csv`. Stage 7 had not begun when this Stage 6 state was serialized.


## Stage 7 research freeze

`STATUS: RESEARCH_FROZEN`

The historical/source Research lane is closed. Stage 5 owner NON_D1 review was approved with zero flags, and Stage 6 final adversarial QA passed with zero errors and zero warnings.

The frozen package preserves accepted historical debt rather than manufacturing precision: 216 UNKNOWN H/A/N rows, 429 unknown exact dates, 5 unknown exact scores, and 11 neutral non-NCAA rows whose exact physical building remains unresolved. All material site gaps are research-accounted; NCAA Tournament site completeness is 33/33 and HOME publication blockers are zero.

Nineteen researched physical venue identities remain without authoritative numeric global venue IDs. Their historical/physical research is preserved; authoritative global identity reconciliation is intentionally deferred to the serialized current-main rebase under `docs/shared-reference-authority.md`.

Research baseline: `3989158d6e461a3dfb7be919586c5b388f8ef83d`.

Latest protected main observed at freeze: `9738fe4f54b813aad4d2a12344a2c8279c3590ee`.

**CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES.**

## Implementation Stage 1 integration preparation

Immutable incoming RESEARCH_FROZEN ZIP SHA-256: `2fc1ad1d39816a4b67bae04611db402e5d0edd2630698cd82f088e783fa106e1`.

Current-main shared-reference preparation against `20b3c568136009aae8d06f9ab24307af3a1a7f50` changes only integration-facing venue keys/geography needed to reuse established global physical identities or register fully specified new identities. No game, opponent, conference, score, result, date, H/A/N, postseason, or accomplishment research conclusion is changed.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=20b3c568136009aae8d06f9ab24307af3a1a7f50` from `research_base_sha=3989158d6e461a3dfb7be919586c5b388f8ef83d`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
