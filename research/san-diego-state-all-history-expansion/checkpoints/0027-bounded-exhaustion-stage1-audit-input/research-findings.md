# San Diego State — checkpoint 0027: exact unchanged-ledger exhaustion audit input

## Authority
- Current protected main: `5f33c88ca1ea7d80e0517f42a200f5a2e15833c9`; permanent auditor Git blob unchanged `0f77c191c36576bfd30b86592554d6ea76d965ac`.
- Same Research lane predecessor: `1fcccfda474a481f92e5fe5308faf0b1c64654db` (checkpoint 0026), immutable Research base `5b840a354fb5cd792239ff8b93cba223a18dd87a`.
- The prior checkpoint 0023 permanent-tool input ZIP is authenticated by exact SHA-256 `0bb50cdd70e9bd4a6e7476b1d58d1097a1206df2a4b81dbdf44bb0beeb751867`. Its historical ledger and all 49 season-census rows are retained **byte-for-byte**, as is `source-provenance.json`.
- Durable source-exhaustion conclusion: checkpoint 0026 `research-exhaustion-assessment.json`, SHA-256 `4e57e2ef709ba1aa7edbbc03ced6d6d1b6cd6b9a913ce50f823d7d5118f53b2e`, included as an exact manifested member. This is exhaustion of realistically accessible high-yield research paths, *not* a claim that inaccessible original issue text was reviewed.

## Candidate audit
The successor `san-diego-state-stage1-exhausted-audit-input.zip` is a standard ZIP with eight CRC-verified and SHA-256 manifested members, including the exact immutable 1,086-game ledger, 49-season census and 0026 original exhaustion assessment. Previous input ZIP SHA256 `0bb50cdd70e9bd4a6e7476b1d58d1097a1206df2a4b81dbdf44bb0beeb751867`; successor ZIP SHA256 `42a37718684f8745900eb6c977c743ae62a185ccbdd04403d01d5358e8fea49a`. Exact unchanged ledger/census bytes and all controlled modifications are independently listed in `audit-input-derivation.json`.

The only policy-state changes are the correctly documented `RESEARCH_EXHAUSTED_IDENTITIES_UNRESOLVED` assessment, source gap `BLOCKING_RESEARCHED_UNRESOLVED` and residual `RESEARCHED_UNRESOLVED`. The original primary-source literal `1 win, 2 losses vs. unknown teams. Forfeit wins vs. Riverside & Fullerton JC.` is unchanged. The three 1921–22 unidentified results have NO newly created game IDs. Three source-listed exclusions and two nonplayed administrative forfeits remain distinct.

## Mandatory next step
The executable `tools/research_stage1_coverage_gap.py` has **not** yet been invoked against this new archive, so eligibility is **not yet claimed**. Execute it read-only with `--expected-sha256 42a37718684f8745900eb6c977c743ae62a185ccbdd04403d01d5358e8fea49a --evidence-member missing-game-evidence.json` at exact protected-main SHA `5f33c88ca1ea7d80e0517f42a200f5a2e15833c9`, preserve the actual report/proof and do not close Stage 1 automatically. A successful audit would only make a separately hashed Stage 1 closeout eligible; it would not publish/implement games or advance to Stage 2.
