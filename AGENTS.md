# Codex repository instructions

## School onboarding

Use the permanent sealed-plan workflow for every new school. Do not recreate the
legacy sequence of manual ingestion, one-off reconciliation scripts, hand-written
staging commands, or piecemeal owner questions.

Read these process documents together before onboarding work:

- `docs/school-onboarding-fast-path.md`
- `docs/onboarding-process-hardening.md`
- `docs/implementation-efficiency-recovery.md`
- `docs/codespace-terminal-safety.md`
- `docs/parallel-portfolio-pipeline.md`
- `docs/site-completeness-protocol.md`
- `docs/research-freeze-self-challenge.md`
- `docs/published-opponent-identity-census.md`
- `docs/non-d1-owner-sanity-scan.md`
- `docs/program-top-level-scope-reference.md`

The post-Iowa hardening amendment is controlling where it makes the execution path
more specific than the older fast-path wording. The site-completeness protocol is
controlling for research-accounted venue/location/H-A-N gaps and the independent
post-reconciliation publication gate. The research-freeze self-challenge is controlling
for the final adversarial review required before a Research lane may certify large or
suspicious residual debt as genuinely unresolved. The post-Texas A&M implementation
efficiency/recovery standard is controlling for phase-sized owner interaction, compact
diagnostics, durable checkpoints, and failure recovery. The published-opponent identity
census is the read-only scoreboard for stale/duplicate opponent identity debt on already
published school packages. The non-D1 owner sanity scan is controlling for the required
lightweight owner review of every target school's distinct `NON_D1` opponent population
before that school first becomes eligible for tracked integration. The program top-level
scope reference is controlling as the default owner-supplied research baseline for each
current D1 program's accepted top-level / Division I-equivalent history intervals.

Research lanes must read `data/reference/program-top-level-scope.csv` at startup. When the
target school is present and authoritative evidence encountered during ordinary research
does not materially contradict the row, use that scope without asking the owner to restate
when the program became or remained top-level. Multiple listed intervals are controlling;
do not collapse them to only the current stint. Bring scope back to the owner only for a
genuine contradiction, ambiguous school identity, or a target absent from the reference.

1. Work in the project Codespace on `data/<school_key>-onboarding`, never on `main`.
2. Treat `RESEARCH_FROZEN` as an executable acceptance state. Run
   `python tools/onboarding_hardening.py research-check ...` on an incoming six-file
   portfolio before Phase 0. A portfolio may preserve genuinely unresolved historical
   site facts, but HOME venue/location gaps, UNKNOWN H/A/N, non-NCAA neutral gaps, and
   conference-tournament/NIT/POSTSEASON site gaps must be explicitly research-accounted;
   silent blanks do not pass. NCAA rows retain the stricter complete-site requirement.
   A Research lane must also complete the required adversarial pre-freeze self-challenge
   in `docs/research-freeze-self-challenge.md`; a mechanical `research-check` pass alone
   is not sufficient to certify `RESEARCH_FROZEN`. `unresolved opponent identities = 0`
   is also not sufficient if a current program has been assigned a stale/local key: the
   self-challenge must compare suspicious current/non-D1 identities against current global
   program keys and published reciprocal alias evidence. For newly researched schools,
   immediately before final `RESEARCH_FROZEN`, present the owner with the complete distinct
   `NON_D1` opponent list, game counts, and representative raw labels under
   `docs/non-d1-owner-sanity-scan.md`; any owner-flagged identity must be explained or
   corrected before freeze.
3. Perform current-main rebase and stable Phase 0 staging with
   `python tools/stage_research_portfolio.py ...`; prefer one guarded phase-sized
   operation over many tiny interactive command handoffs. Ambiguous global identity
   is a STOP, never a guess. Recheck both physical venue identity and opponent/program
   identity against current main; an intervening school may establish the authoritative
   global key/alias that a frozen portfolio did not yet know. For portfolios that reached
   `RESEARCH_FROZEN` before the non-D1 owner sanity-scan policy was adopted, perform that
   same complete owner scan during current-main rebase and resolve any flagged identities
   before declaring `INTEGRATION_FROZEN` or beginning tracked Phase 0; do not reopen
   unrelated historical research merely to add this checkpoint.
4. Run `python tools/onboard_school.py <school_key> --preflight` from the clean Phase 0
   checkpoint.
5. Present every owner-relevant decision as one consolidated Gate 1 batch. Every
   game-specific review item must show its date. If date is disputed, show the source
   date and canonical date separately; never collapse them into one date.
6. Obtain one explicit owner decision and evidence basis for every pending row. Before
   presenting the batch, research each row and provide a recommended disposition; the
   owner may approve routine recommendations in bulk.
7. Encode the approved batch with
   `python tools/onboarding_hardening.py fill-review ...` rather than a school-specific
   CSV-editing script. Let the tool expand selected versus rejected conditional identity
   rows.
8. Before cryptographically sealing Gate 1, run
   `python tools/onboarding_hardening.py rehearse-review <school_key>`. This disposable
   pre-seal rehearsal must pass ingestion, reconciliation, publication metadata,
   validation, target no-op, implementation site completeness, accomplishment
   verification, deterministic site build, unit tests, changed-path allow-list, and
   whitespace checks without mutating the real tracked repository.
9. If a purely technical repair changes tracked inputs after owner approval, regenerate
   preflight and use `python tools/onboarding_hardening.py carry-forward ...`. Carry
   approval forward only when the exact decision IDs and every substantive decision
   input are unchanged; otherwise return only the changed/new historical decisions to
   the owner.
10. Seal with `python tools/onboard_school.py <school_key> --approve ...` only after the
    pre-seal rehearsal passes. Apply only with the exact emitted plan hash.
11. The sealed apply must remain transactional and must pass validation, target no-op,
    implementation site completeness, accomplishment cross-check, deterministic site
    build, unit tests, and whitespace. Known source/reciprocal site evidence must not be
    lost behind canonical blanks unless field-specific reconciliation provenance explains
    why the canonical field remains unresolved.
12. Run `python tools/release_school.py <school_key> --prepare`.
13. Stop for the owner to visually approve the exact PR preview.
14. Merge only with `--merge --preview-approved`; require the exact merged SHA to reach
    a successful Production deployment and match production JSON.

Historical uncertainty remains valid. Never infer game identity, inclusion, date,
site, venue, opponent, or a controlling canonical fact merely to make the workflow
pass. Preserve source `raw_text`, explicit researched-unresolved metadata, and approved
unresolved discrepancies.

## Implementation efficiency and recovery

* Use one fresh Implementation chat per school, but do not assume that a fresh chat alone prevents context bloat. Keep verbose logs and large evidence tables in durable files rather than the conversation whenever possible.
* Batch deterministic technical work by phase. One owner relay per reversible phase is the default; one-command-at-a-time copy/paste loops are a process regression unless a real blocker requires them.
* Live terminal output should be compact: phase, HEAD/base/fingerprint, counts, exact failing IDs/paths, verbose-log path, and next safe action. Redirect large diagnostics to `/tmp` or ignored `.onboarding/` artifacts.
* Durable repository state outranks chat memory. After interruption, inspect Git/GitHub and `.onboarding/<school>/` state and resume from the earliest incomplete phase rather than replaying successful phases.
* A Codespace/chat failure does not authorize blind reset, stash, force push, branch deletion, or re-running an already completed phase whose fingerprint remains valid.
* If a chat must be replaced mid-school, use the compact recovery capsule defined in `docs/implementation-efficiency-recovery.md` and verify it against actual repository state before acting.

## Collaboration boundary

* Routine extraction, normalization research, package construction, reconciliation analysis, testing, provenance maintenance, Git plumbing, validator failures, and deployment mechanics belong to the collaborator and should not create extra owner handoffs.
* Return to the owner only when a new judgment is required about history scope, game identity or inclusion, opponent identity, home/away/neutral classification, venue/location truth, a controlling canonical historical fact, accomplishments, unresolved-conflict publication, the required non-D1 opponent sanity scan, or final preview approval. A history-scope question is new only when `data/reference/program-top-level-scope.csv` is absent/ambiguous for the target or authoritative research materially contradicts it; do not ask the owner to restate an uncontradicted reference row.
* A technical failure after owner approval must be diagnosed and repaired generically where possible; do not ask the owner to re-review unchanged historical decisions merely because the tooling implementation changed.
* Technical work should be batched at phase boundaries. Repeated one-command-at-a-time owner handoffs for deterministic setup are a process regression unless repository state is unexpected.
* Research lanes should perform the required pre-freeze self-challenge autonomously; do not create an extra owner approval loop merely because large researched-unknown populations require adversarial review.
* The non-D1 owner sanity scan is a quick completeness check, not a transfer of research responsibility: the collaborator must research suspicious identities before presentation and must not require the owner to verify every legitimate non-D1 opponent independently.
* Do not use the owner as a transport layer for files, logs, or state the agent can inspect directly from repository/GitHub/onboarding artifacts. When the owner's Codespace is the only execution surface, request the smallest diagnostic output needed.

## Git safety

- Never use `git add -A` for onboarding.
- Never force-push shared history.
- Never merge when the sealed input fingerprint, release file boundary, branch SHA,
  PR head SHA, or deployment SHA differs from the reviewed state.
- Keep generated `.onboarding/` plans local; the sealed decision plan is archived
  under `data/reconciliation/onboarding-decisions/` during apply.

## Code review rules

- Flag any discrepancy display that omits `source_game_date` or
  `canonical_game_date`; date conflicts must expose both values.
- Flag any write path that bypasses the approved-plan hash or writes outside the
  transaction allow-list.
- Flag any release path that merges without explicit preview approval or treats a
  Preview deployment as Production.
- Flag any onboarding path that seals Gate 1 before the filled review has passed the
  disposable pre-seal technical rehearsal.
- Flag any research-freeze path that allows material site gaps to remain silent, treats
  a mechanical `research-check` pass as sufficient without the required adversarial
  self-challenge, allows large residual HOME/H-A-N/date debt to survive without the
  evidence accounting required by `docs/research-freeze-self-challenge.md`, permits
  an obvious current-program opponent identity to survive under a stale/non-D1 key, or
  allows a newly researched school to reach `RESEARCH_FROZEN` without the required
  non-D1 owner sanity scan.
- Flag any research-lane workflow that asks the owner to supply or reconfirm a target
  school's top-level/D1 start when an unambiguous, uncontradicted scope row already exists
  in `data/reference/program-top-level-scope.csv`, or that discards an earlier accepted
  interval for a multiple-stint program.
- Flag any already-frozen portfolio that reaches `INTEGRATION_FROZEN`/tracked Phase 0
  without receiving the non-D1 owner sanity scan during current-main rebase when the
  scan was not completed before its original research freeze.
- Flag any implementation/release path that can lose known target/reciprocal site
  evidence without field-specific reconciliation provenance.
- Flag school-specific hard-coded pre-scope exclusion counts; scope tests must enforce
  the reciprocal-evidence invariant generically.
- Flag implementation instructions that require repeated owner copy/paste of verbose
  deterministic output when the same evidence can be written to a durable artifact and
  summarized compactly.
- Opponent-identity census findings are review triggers, not automatic merge authority;
  never rewrite historical program identity from string similarity alone.
