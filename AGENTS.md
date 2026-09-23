# Codex repository instructions

## School onboarding

Use the permanent sealed-plan workflow for every new school. Do not recreate the
legacy sequence of manual ingestion, one-off reconciliation scripts, hand-written
staging commands, or piecemeal owner questions.

Read these process documents together before onboarding work:

- `docs/school-onboarding-fast-path.md`
- `docs/onboarding-process-hardening.md`
- `docs/implementation-efficiency-recovery.md`
- `docs/implementation-gate1-authority-boundary.md`
- `docs/codespace-terminal-safety.md`
- `docs/parallel-portfolio-pipeline.md`
- `docs/site-completeness-protocol.md`
- `docs/stage3a-regular-season-site-research.md`
- `docs/stage3a0-local-only-contract.md`
- `docs/stage3a1-source-fanout-contract.md`
- `docs/stage3a3-neutral-tranche-contract.md`
- `docs/research-freeze-self-challenge.md`
- `docs/research-convergence-and-stopping.md`
- `docs/shared-reference-authority.md`
- `docs/published-opponent-identity-census.md`
- `docs/non-d1-owner-sanity-scan.md`
- `docs/program-top-level-scope-reference.md`

The post-Iowa hardening amendment is controlling where it makes the execution path
more specific than the older fast-path wording. The site-completeness protocol is
controlling for research-accounted venue/location/H-A-N gaps and the independent
post-reconciliation publication gate. The research-freeze self-challenge is controlling
for the final adversarial review required before a Research lane may certify large or
suspicious residual debt as genuinely unresolved. The Research convergence/stopping
policy is controlling for proportional continuation in opponent identity, Stages 3A/3B,
and Stage 6; it prevents already researched residual ambiguity from becoming an
open-ended second research cycle without weakening substantive acceptance gates. The
shared-reference authority policy is controlling for the boundary between parallel
Research findings and authoritative protected-main/global reference mutation. The
post-Texas A&M implementation efficiency/recovery standard is controlling for phase-sized
owner interaction, compact diagnostics, durable checkpoints, and failure recovery. The
published-opponent identity census is the read-only scoreboard for stale/duplicate
opponent identity debt on already published school packages. The non-D1 owner sanity
scan is controlling for the required lightweight owner review of every target school's
distinct `NON_D1` opponent population before that school first becomes eligible for
tracked integration. The program top-level scope reference is controlling as the default
owner-supplied research baseline for each current D1 program's accepted top-level /
Division I-equivalent history intervals.

Research lanes must read `data/reference/program-top-level-scope.csv` at startup. When the
target school is present and authoritative evidence encountered during ordinary research
does not materially contradict the row, use that scope without asking the owner to restate
when the program became or remained top-level. Multiple listed intervals are controlling;
do not collapse them to only the current stint. Bring scope back to the owner only for a
genuine contradiction, ambiguous school identity, or a target absent from the reference.

For Stage 3A, `docs/stage3a-regular-season-site-research.md` is controlling for
research responsibility, venue-completeness expectations, stopping, canonical/shared
reuse, the required Stage 3A-0 through Stage 3A-4 architecture, and the mandatory final
row-level Stage 3A state. `docs/stage3a0-local-only-contract.md` is controlling for
Stage 3A-0 execution scope. `docs/stage3a1-source-fanout-contract.md` is controlling
for Stage 3A-1 source hierarchy, fanout, and convergence.
`docs/stage3a3-neutral-tranche-contract.md` is controlling for Stage 3A-3 tier
boundaries, tranche sizing, source fanout, and neutral-venue convergence.

Stage 3A substages are owner-facing boundaries; evidence classes inside 3A-1 through 3A-3
are not automatically owner-facing boundaries. Use the **largest safely completable
meaningful tranche**. Bundle multiple small families that use the same research mode;
avoid both repeated 3–8 row micro-checkpoints and open-ended sweeps across large
heterogeneous residuals. Independent row-level adjudication remains capped at 25 rows per
turn, but a homogeneous residual already at or below that ceiling should normally be
processed as one tranche.

**Stage 3A-0 is a strict local-only mechanical pass.** It performs zero public-web
research and zero external source discovery. During 3A-0, use only the verified durable
checkpoint plus already-present project evidence in the checked-out/current protected-main
repository. Published reciprocal lookup means a structured local join against canonical
games, game assertions, already-published school packages, or accepted reciprocal
artifacts already present in the project. Do not browse institutional sites, media guides,
newspapers, external PDFs, GitHub/code search for new sources, or opponent archives. Do
not inspect opponent files one by one when a structured local join can answer the same
question. An unmatched local candidate stays unresolved for 3A-1/2/3; it is not permission
to open the web.

3A-1 must bound **source fanout as well as row count**. Before opening external sources,
define coherent evidence classes and use the required hierarchy: accepted project evidence,
target-school institutional evidence, obvious opponent institutional evidence, then at most
one specific high-yield authoritative fallback family when justified. Generic web search is
discovery-only, not an evidence class. Do not fan out through Reddit, forums, mirrors,
aggregators, random wikis, or unrelated search results merely because institutional evidence
did not resolve a row. A <=25-row queue is not permission for <=25 separate deep web
investigations. After the obvious authoritative paths are exhausted, converge the row/class
as supported or `RESEARCHED_UNRESOLVED` and move on. 3A-1 should also use population-level
convergence for homogeneous ancient historical/non-D1 H/A/N residuals after the obvious
systematic institutional/reciprocal opportunities are exhausted. 3A-2 should use authoritative home-facility chronology plus a
default-with-exceptions model rather than re-proving ordinary modern HOME venues game by
game. Ancient HOME venue debt may terminalize after the reasonable systematic paths are
exhausted, but complete supported city/state must be written through before 3A-2 closes;
systematically established source-program HOME geography may be propagated across
already-established HOME rows when no accepted evidence indicates an alternate location.
3A-3 should proceed in the default order: accepted evidence, modern recurring families,
modern one-offs, historical recurring families, historical one-offs. A Stage 3A-3 turn
must stay within one coherent neutral-research tier and one coherent research mode after
substantial research begins; do not roll from modern recurring to modern one-offs to
historical work in one continuous turn. Recurring families should be resolved at
family/event level where supported, using a small hierarchy of project evidence,
event/host sources, participant institutional sources, and at most one specific
authoritative fallback family. Historical one-off residuals should converge at population
level rather than become bespoke archaeology projects.

Regular-season `OPPONENT_HOME` exact-building reconstruction remains outside active
source-school research unless usable accepted venue evidence is already present. For
regular-season neutral venue research, **modern means 1996-97 through present** and that
population retains the strong exact-venue expectation. For 1995-96 and earlier, exact-
building recovery is historical enrichment rather than a publication blocker after the
reasonable systematic/high-yield opportunities are exhausted; preserve supported
city/state/partial venue evidence and explicit terminal debt. Do not reopen already-
supported exact venues merely because they now fall on the historical side of the cutoff.
Do not infer H/A/N from geography or a venue from city/event custom/nearby editions.

Durable checkpoints control continuity. A long Research lane may deliberately roll to a
fresh chat at a verified major stage/substage checkpoint rather than wait for context
exhaustion. Ordinary owner continuation should still require only a short `Proceed`;
do not make the owner relay every small evidence class.

### Research shared-reference authority

Research may fully establish historical identities that have global implications, but an
independent school Research lane must not directly mutate protected-main shared registries.
Carry a settled but not-yet-registered identity forward as `Historical identity: RESOLVED`
and `Global registration: PENDING_CURRENT_MAIN_REBASE` with enough evidence/detail for
serialized Implementation to reconcile it mechanically. General permission to mutate
repository or research state does **not** authorize protected-main shared-reference writes.
If early global registration is genuinely useful across active lanes, use an explicitly
authorized dedicated maintenance branch/PR under `docs/shared-reference-authority.md`.
Any shared-reference mutation must pass both repository validation and declared-intent diff
validation; unrelated shared-row changes are a STOP.

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
   global key/alias that a frozen portfolio did not yet know. Reconcile any settled
   Research shared-reference proposals under `docs/shared-reference-authority.md`; do not
   reopen their historical conclusion unless current-main evidence creates a genuine
   conflict. For portfolios that reached `RESEARCH_FROZEN` before the non-D1 owner
   sanity-scan policy was adopted, perform that same complete owner scan during
   current-main rebase and resolve any flagged identities before declaring
   `INTEGRATION_FROZEN` or beginning tracked Phase 0; do not reopen unrelated historical
   research merely to add this checkpoint.
4. Run `python tools/onboard_school.py <school_key> --preflight` from the clean Phase 0
   checkpoint. Preflight must pass the Integration Freeze semantic-drift guard. After the
   first blocker-free preflight, decision count is informational, not a target to reduce.
   Perform one comprehensive deterministic representation/identity sweep and at most one
   coherent repair batch; do not create a second Research/adjudication cycle by rewriting
   frozen dates, scores, overtime, H/A/N, venue/location meaning, game type, postseason
   round, result, or literal source evidence.
5. Present every owner-relevant decision as one consolidated Gate 1 batch. Every
   game-specific review item must show its date. If date is disputed, show the source
   date and canonical date separately; never collapse them into one date. Supported
   historical corrections discovered during Implementation remain in this packet rather
   than being pre-applied.
6. Obtain one explicit owner decision and evidence basis for every pending row. Before
   presenting the batch, research each row and provide a recommended disposition; the
   owner may approve routine recommendations in bulk.
7. Encode the approved batch with
   `python tools/onboarding_hardening.py fill-review ...` rather than a school-specific
   CSV-editing script. Let the tool expand selected versus rejected conditional identity
   rows. When Gate 1 authorizes a newly discovered historical correction, encode it with
   `source_patch_by_decision` / `canonical_patch_by_decision` rather than editing the
   frozen source package first.
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
* **Default owner execution interface: self-contained copy/paste terminal relays.** Do not require the owner to download assistant-generated `.py`/helper files and manually upload or drag them into the Codespace when the same operation can reasonably be delivered as a guarded pasted relay. If substantial Python is necessary, the pasted relay may write a temporary child script under `/tmp`, execute it, preserve compact diagnostics, and leave tracked repository boundaries clean. Manual helper-script transport is an exception, not the default.
* Live terminal output should be compact: phase, HEAD/base/fingerprint, counts, exact failing IDs/paths, verbose-log path, and next safe action. Redirect large diagnostics to `/tmp` or ignored `.onboarding/` artifacts.
* Durable repository state outranks chat memory. After interruption, inspect Git/GitHub and `.onboarding/<school>/` state and resume from the earliest incomplete phase rather than replaying successful phases.
* A Codespace/chat failure does not authorize blind reset, stash, force push, branch deletion, or re-running an already completed phase whose fingerprint remains valid.
* If a chat must be replaced mid-school, use the compact recovery capsule defined in `docs/implementation-efficiency-recovery.md` and verify it against actual repository state before acting.

## Collaboration boundary

* Routine extraction, normalization research, package construction, reconciliation analysis, testing, provenance maintenance, Git plumbing, validator failures, and deployment mechanics belong to the collaborator and should not create extra owner handoffs.
* Return to the owner only when a new judgment is required about history scope, game identity or inclusion, opponent identity, home/away/neutral classification, venue/location truth, a controlling canonical historical fact, accomplishments, unresolved-conflict publication, the required non-D1 opponent sanity scan, or final preview approval. A history-scope question is new only when `data/reference/program-top-level-scope.csv` is absent/ambiguous for the target or authoritative research materially contradicts it; do not ask the owner to restate an uncontradicted reference row. When that row excludes researched history, however, Implementation must plainly state the public-page consequence and preserved excluded population during Stage 1.
* A technical failure after owner approval must be diagnosed and repaired generically where possible; do not ask the owner to re-review unchanged historical decisions merely because the tooling implementation changed.
* Technical work should be batched at phase boundaries. Repeated one-command-at-a-time owner handoffs for deterministic setup are a process regression unless repository state is unexpected.
* Research lanes should perform the required pre-freeze self-challenge autonomously; do not create an extra owner approval loop merely because large researched-unknown populations require adversarial review.
* Evidence-class completion inside an authorized Research substage should not create a routine owner handoff. Bundle related small classes into meaningful safe tranches and return only at required stage/substage boundaries, genuine blockers/owner judgments, or necessary durability checkpoints.
* Stage 6 residuals begin as accepted researched debt. Challenge them systematically; do not convert the audit into a second row-by-row research cycle or return to the owner after one or two ordinary repairs when the same class-level challenge can safely continue.
* The non-D1 owner sanity scan is a quick completeness check, not a transfer of research responsibility: the collaborator must research suspicious identities before presentation and must not require the owner to verify every legitimate non-D1 opponent independently.
* Do not use the owner as a transport layer for files, logs, helper scripts, or state the agent can inspect directly from repository/GitHub/onboarding artifacts. When the owner's Codespace is the only execution surface, request the smallest diagnostic output needed and default to a copy/paste relay rather than manual helper-file upload/download loops.

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
- Flag any pre-Gate Implementation workflow that changes frozen historical meaning after
  `INTEGRATION_FROZEN` merely because new evidence was found. Date, score, result,
  overtime, H/A/N, venue/location meaning, game type, postseason round, source evidence,
  and similar historical corrections belong in Gate 1 patch/reconciliation authority.
  Representation-only current-main key/display/shared-reference rebase remains valid.
  Decision-count reduction is never sufficient justification for a substantive package
  mutation.
- Flag any research-freeze path that allows material site gaps to remain silent, treats
  a mechanical `research-check` pass as sufficient without the required adversarial
  self-challenge, allows large residual HOME/H-A-N/date debt to survive without the
  evidence accounting required by `docs/research-freeze-self-challenge.md`, permits
  an obvious current-program opponent identity to survive under a stale/non-D1 key, or
  allows a newly researched school to reach `RESEARCH_FROZEN` without the required
  non-D1 owner sanity scan.
- Flag any Stage 3A workflow that collapses Stage 3A-0 through 3A-4 into one monolithic
  execution unit; automatically rolls from one required Stage 3A substage into the next
  without an owner `Proceed`; lets Stage 3A-0 perform public-web research, institutional
  archive browsing, external source discovery, broad GitHub/code search, opponent-by-
  opponent source hunting, or historical adjudication instead of a structured local
  project-evidence join; lets Stage 3A-1 turn a bounded row queue into unbounded source
  discovery, opens many unrelated domains for individual rows, substitutes Reddit/forums/
  mirrors/aggregators for the required institutional hierarchy, or continues searching
  after the obvious authoritative source paths are exhausted instead of converging; lets
  Stage 3A-3 cross multiple neutral-research tiers in one long turn, opens many unrelated
  source families for one event/row, turns recurring families into game-by-game hunting,
  or continues "locating exact sources for missing patches" after the bounded
  event/host/participant/fallback hierarchy is exhausted; works more than 25 independently
  researched/adjudicated rows in one turn; repeatedly
  checkpoints tiny 3–8 row/family units when a larger homogeneous tranche is safely
  completable; attempts an open-ended sweep across a large heterogeneous residual;
  combines substantial Stage 3A historical research with Stage 3A-4 mechanical closeout;
  re-proves ordinary established HOME venues game by game instead of using supported
  facility chronology plus exceptions; allows unresolved HOME venue exceptions to reach
  3A-4 without complete supported city/state; turns ordinary regular-season
  `OPPONENT_HOME` physical-building blanks into active source-school historical research;
  accepts shallow modern (1996-97+) neutral-site debt without the required canonical/shared
  and systematic evidence pass; treats 1995-96-and-earlier regular-season neutral exact-
  building debt as a publication blocker after proportionate systematic/high-yield
  exhaustion; or reaches Stage 3A completion without one authoritative
  row-level Stage 3A ledger sufficient for downstream use.
- Flag any independent Research-lane workflow that directly mutates protected-main
  shared reference registries, or that interprets general repository-mutation permission
  as authority for such a write. Settled shared identities should normally be carried to
  current-main rebase under `docs/shared-reference-authority.md`.
- Flag any shared-reference mutation whose actual diff changes unrelated shared identities
  outside the declared scope, even when repository validation passes.
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
- Flag implementation instructions that require manual download/upload of assistant-generated
  helper scripts when a guarded copy/paste relay can reasonably create and execute the
  same temporary helper inside the Codespace.
- Opponent-identity census findings are review triggers, not automatic merge authority;
  never rewrite historical program identity from string similarity alone.
