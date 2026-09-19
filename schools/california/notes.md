# California research portfolio notes

- Research base: `3989158d6e461a3dfb7be919586c5b388f8ef83d`.
- Competitive game universe: 3,012 rows, 1907-08 through 2025-26. Exhibitions/noncompetitive rows excluded in Stage 1.
- Opponent identities: 307 distinct normalized opponents; unresolved opponent identities: 0.
- Working NON_D1 census: 78 distinct identities. Owner NON_D1 sanity scan: **APPROVED** for all 78 distinct identities before Stage 6.
- Stage 3A regular-season H/A/N terminal researched debt is preserved with `site_research_status` / `site_research_basis`; no geography or venue inference was used.
- Stage 3B: 137/137 postseason rows classified; postseason H/A/N UNKNOWN = 0; NCAA physical venue/city/state gaps = 0. Surviving pre-NCAA PCC site debt is explicitly researched/accounted.
- Physical venue IDs in this Research package are research-base references only. Serialized Implementation must perform the authoritative current-main rebase.
- Harmon Gym (1933) and Haas Pavilion are treated as one physical lineage; Old Harmon Gymnasium is a distinct earlier building.
- Accepted Stage 1 source contradictions and administrative-result notes remain preserved in row-level provenance rather than silently rewritten.


## Stage 6 pre-freeze self-challenge

- `PRE-FREEZE SELF-CHALLENGE: PASS`.
- UNKNOWN H/A/N: 117 final regular-season rows; 1 additional row (1973-12-26 Pennsylvania) recovered during Stage 6. Population-level challenge confirms these are terminal researched historical debt; no new comparable systematic/high-yield evidence class remains.
- UNKNOWN exact dates: Stage 6 working count 588; 3 recovered in the 1973-74 Quaker City Classic cluster; final count 585. Remaining debt is overwhelmingly pre-1950 and concentrated in historical institutional series already subjected to systematic reciprocal/institutional review. No dates were inferred from schedule order or geography.
- Venue physical identity: Honolulu International Center was reconciled as the 1964-1976 naming era of the same physical complex later named Neal S. Blaisdell Center; duplicate local physical identity removed. 1966/1971 game display names use the historical HIC name.
- Quaker City bounded repair: dates recovered for Pennsylvania (1973-12-26), Penn State (1973-12-27), and Temple (1973-12-29). Pennsylvania and Temple physical site recovered as The Palestra; Penn State exact building remains explicitly researched partial.
- Opponent identities: unresolved = 0; known current-program key splits = 0; ambiguous current-program matches = 0. Owner-approved NON_D1 census remains 78.
- NCAA physical venue + city/state gaps = 0. HOME publication blockers = 0. Ambiguous physical venue identities = 0.
- Remaining permitted historical uncertainty is terminal researched debt under `docs/research-convergence-and-stopping.md`; Stage 6 did not restart accepted Stage 1-3 populations.
- `RESEARCH_FROZEN: YES`.
- `CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`.

## Implementation Stage 1 integration preparation

Immutable incoming RESEARCH_FROZEN ZIP SHA-256: `1598de48d6a9a856758c5daa4bbb9e1312627a1ccf019aa6e633132f11912973`.

Current-main shared-reference preparation against `f4bd9341509a0ecc2aacf87195686275d87a79fa` changes only integration-facing venue identity keys/IDs/geography required to reuse established global physical identities, apply the standing Las Vegas normalization convention, or leave fully researched genuinely new venue identities for authoritative ID allocation by the permanent staging tool. No opponent, conference, score, result, date, H/A/N, postseason, accomplishment, or game-universe research conclusion is changed.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=f4bd9341509a0ecc2aacf87195686275d87a79fa` from `research_base_sha=3989158d6e461a3dfb7be919586c5b388f8ef83d`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
