# st-bonaventure research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: 6b621ecd56aa1d66d8fbbb23af4d0e1f5751d1558cf3f054c9f75f0ac25a90a6
- Research base SHA: bed68f763a7ea8920c6ba830b004334b16c9e303
- Stage 3B status: COMPLETE
- Competitive games: 2,614
- Primary-source historical results cutoff: 2025-2026
- Required completed-season cutoff: 2025-2026
- Coverage cutoffs are explicit Research declarations; media-guide titles and filenames are not coverage inference rules.
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 70
- NCAA_TOURNAMENT: 16
- NIT: 34
- POSTSEASON: 11
- REGULAR_SEASON: 2,483

## Final H/A/N census

- NEUTRAL: 494
- OPPONENT_HOME: 755
- SOURCE_PROGRAM_HOME: 838
- UNKNOWN: 527

## Accepted top-level history scope

- Owner-confirmed Research scope: `INCEPTION+`.
- The package includes the owner-approved 1915-16 University at Buffalo game and the individually documented varsity universe from 1919-20 through 2025-26.
- The 1919-20 institutional record remains 6-10 (16 games), with 10 individually documented games (3-7) and six unidentified games collectively accounting for 3-3. No placeholder games are created.
- No Stage 6 repair changes the nine owner-final historical reconciliation directives reserved for eventual St. Bonaventure Implementation.

## Stage 5 / Stage 6 disposition

- Stage 5 NON_D1 owner sanity scan: APPROVED by owner on 2026-11-02.
- Stage 6 is a bounded pre-freeze adversarial audit, not a second Research cycle.
- Stage 6 recovered 121 exact dates total: 111 systematic published-reciprocal dates plus 10 additional historical NCAA dates from the tournament-wide bracket review.
- Stage 6 recovered one H/A/N row (1948-49 Dayton), three historical neutral exact buildings, and corrected the 1961 NCAA Rhode Island site to Madison Square Garden.

## Final Research Freeze

- Final freeze authority: Stage 6 `COMPLETE_PRE_FREEZE_SELF_CHALLENGE_PASS`.
- Permanent Research acceptance: PASS (0 errors / 0 warnings).
- Competitive games: 2,614.
- Unresolved opponent identities: 0.
- Known current-program key splits: 0.
- Ambiguous current-program identity matches: 0.
- HOME rows: 838; resolved HOME venues: 838/838; chronology conflicts: 0.
- NCAA Tournament rows reviewed: 16/16; U.S. exact-site gaps: 0; round review complete.
- Unaccounted material site-research gaps: 0.
- Terminal H/A/N debt: 527 `UNKNOWN`.
- Terminal exact-date debt: 981 blank exact dates after 121 Stage 6 recoveries.
- Historical regular-season neutral exact-building debt: 26 rows.
- Historical neutral locality debt: 2 accepted Canisius rows.
- Postseason exact-building reconciliation reserved to Implementation: 1 row (1979 Alabama; owner-final Alabama HOME at BJCC).
- Unknown played scores: 2 (Grove City and Cathedral College, 1919-20).
- Nine owner-final historical reconciliation directives remain intentionally unapplied to frozen Research game fields and must be carried into serialized Implementation.
- Research base SHA: `bed68f763a7ea8920c6ba830b004334b16c9e303`.
- Final-freeze protected-main authority: `89327ed84827323a3f64e08ac1410ed71e442a0e`.
- `RESEARCH_FROZEN: YES`.
- `CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES`.

### Final-freeze bookkeeping repair

The Stage 6 candidate package's `notes.md` still displayed the pre-Stage-6 H/A/N census
(837 SOURCE_PROGRAM_HOME / 528 UNKNOWN). The accepted Stage 6 ledger had already repaired
the December 18, 1948 Dayton game (`STB-1948-49-004`) to SOURCE_PROGRAM_HOME at Olean
Armory, yielding the accepted final census of 838 SOURCE_PROGRAM_HOME / 527 UNKNOWN.
This freeze updates only this descriptive metadata and adds the terminal freeze summary;
no CSV row, source evidence, historical fact, owner disposition, or Research field was changed.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=933d2f9e7ebdd24fefcafda326a7ebe898a476df` from `research_base_sha=bed68f763a7ea8920c6ba830b004334b16c9e303`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

Explicit Stage 1 venue-identity reconciliation applied; the hash-bound spec and historical basis are recorded in the Integration Freeze manifest.
