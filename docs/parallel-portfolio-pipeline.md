# Parallel Portfolio Pipeline — “Five in the Holster”

- **Status:** Approved throughput model for high-major onboarding
- **Default concurrency:** Up to five independent research/portfolio chats
- **Repository integration:** Strictly serialized, one school at a time
- **Purpose:** Increase throughput without allowing stale or concurrent writes to global canonical/reference state

The project can safely parallelize the slowest part of onboarding: source research and six-file portfolio construction.

It must **not** parallelize canonical integration, Owner Gate 1 sealing/apply, or release work against the same repository state.

The operating model is:

```text
5 independent research lanes  ->  1 serialized Codespace integration lane
```

As one school leaves the integration lane, another research-frozen portfolio enters it and a new research chat may be started to keep the queue full.

This is the “five in the holster” procedure.

## 1. What may run in parallel

Each research chat may independently:

- inspect the school media guide;
- find the official completed current-season schedule;
- extract year-by-year competitive results;
- exclude exhibitions;
- normalize opponent labels and identities;
- research venue chronology;
- research conference chronology;
- research conference/NCAA/NIT/other postseason classification;
- research accomplishments;
- research overtime and administrative-action evidence;
- perform source-internal cross-checks;
- perform targeted reciprocal-source research;
- build and QA the six school-package files;
- produce a ZIP and exact manifest/hashes;
- record unresolved owner-level historical questions.

This work is source-local and can proceed even when the chat does not have the project Codespace mounted.

A missing `/workspaces/college-basketball-history` mount is not a research blocker. The chat may read current GitHub `main` for schemas/examples, but it must not write to the repository from a substitute environment.

## 2. What must remain serialized

Only one school at a time should enter the repository integration lane.

The following work is serialized:

- final current-main rebase of package/reference identities;
- creation of `data/<school>-onboarding`;
- tracked package installation;
- global venue/reference writes;
- stable Phase 0 package checkpoint;
- generic onboarding preflight;
- Owner Gate 1 encoding/sealing;
- transactional apply;
- target assertion closure;
- release preparation;
- Owner Gate 2;
- merge and exact Production proof.

Do not run five onboarding branches against the same stale `main` and then try to merge them later.

Parallelize research, not canonical mutation.

## 3. Starting each research lane

Each new school chat should receive:

- the current team-independent onboarding handoff;
- the school identity;
- the media guide when readily available;
- the explicit owner history-scope ruling when known.

The chat should record the GitHub `main` SHA it used for repository schemas/reference inspection:

```text
research_base_sha=<sha>
```

This SHA is provenance, not a promise that the portfolio may later integrate without rebasing.

For high-major schools, the chat should normally find the completed official schedule, venue history, conference history, accomplishment evidence, and supplementary authoritative sources itself.

## 4. Research freeze versus integration freeze

Parallel work introduces an important distinction.

### Research-frozen portfolio

A research-frozen portfolio means:

- historical/source research is complete enough for integration;
- the six files have passed source-level QA;
- opponent identities are resolved as far as reasonably possible;
- venue candidates are identified physically and geographically;
- conference history is established;
- postseason taxonomy is established;
- current-season supplementation is complete;
- exhibitions are excluded;
- known uncertainties are documented;
- exact package hashes are recorded.

It does **not** mean that every global numeric ID or shared reference identity is still valid against the newest `main`.

### Integration-frozen portfolio

An integration-frozen portfolio is created only when that school reaches the front of the Codespace queue.

It means the research-frozen package has been rebased against **current** `main`, all shared/global identities have been reconciled, package QA has been rerun, and fresh hashes have been recorded.

Only an integration-frozen package may enter tracked Phase 0.

## 5. Global venue IDs are provisional during parallel research

This is the most important concurrency check.

Suppose five research chats all start from the same `main`, whose highest current venue ID is `VEN-000280`. More than one chat may independently conclude that its first new physical venue should be `VEN-000281`.

That is not a historical error. It is a stale global-allocation collision.

Therefore:

> **Any new numeric global venue ID assigned during parallel research is provisional until current-main integration rebase.**

The durable facts are:

- physical venue identity;
- proposed `venue_key`;
- canonical/display name;
- aliases;
- city/state;
- venue type;
- chronology;
- source evidence;
- which school games map to that physical venue.

The numeric `VEN-xxxxxx` allocation is an integration concern.

### At integration time

For every research-time new venue candidate:

1. inspect current global venue registry;
2. determine whether the same physical venue has been added since `research_base_sha`;
3. if yes, reuse the current global venue identity and ID;
4. if no, confirm the proposed key/display name do not collide with another physical venue;
5. allocate the next valid current numeric venue ID;
6. update `schools/<school>/venues.csv` and any package notes/manifest references to the provisional ID;
7. rerun package QA and hashes.

Never preserve a stale numeric ID merely because it appeared in the research ZIP.

## 6. Recheck more than the number

The integration rebase should check all shared-reference assumptions that could have changed since `research_base_sha`, especially:

- global `venue_id` allocation;
- venue physical-identity reuse;
- venue keys;
- canonical venue display names/aliases;
- newly added venue geography;
- stable program/opponent keys when the research package depends on a shared identity;
- normalized display-name collisions for the same program key;
- conference/reference identities used by the package;
- any other global registry row that the package expects to create.

If another team has already added the exact physical venue or canonical identity, reuse it rather than creating a duplicate.

If current main now uses the same proposed key/name for a different entity, resolve the collision before preflight.

## 7. Do not preflight against a stale research baseline

A research chat may inspect current canonical data to understand schemas or likely overlap, but its final Owner Gate 1 decision universe must not be treated as authoritative until the portfolio is integrated against current `main`.

Why:

Every school merged ahead of it can add:

- canonical games;
- reciprocal assertions;
- discrepancies;
- venues;
- program/reference normalization;
- generated public data.

Those changes can alter matching and discrepancy results.

Therefore:

> **The canonical preflight belongs to the serialized integration lane, after current-main rebase and the stable Phase 0 package checkpoint.**

Do not ask the owner to approve Gate 1 decisions produced from a stale parallel-research snapshot.

## 8. Required current-main rebase check before Phase 0

When a holstered portfolio reaches the front of the queue:

1. synchronize local `main` with `origin/main`;
2. verify a clean worktree;
3. record:

```text
research_base_sha=<old research baseline>
integration_base_sha=<current main>
```

4. inspect shared/global registries changed since the research baseline;
5. reconcile every provisional/new reference identity against current main;
6. reuse identities added by intervening teams when they represent the same real entity;
7. renumber stale venue IDs where required;
8. check venue key/name/geography collisions;
9. check normalized opponent/program display assumptions;
10. rerun the complete source-package QA;
11. produce new six-file hashes and a new integration-ready ZIP/manifest if transport is still needed;
12. only then create `data/<school>-onboarding` and begin tracked Phase 0.

This rebase should be mostly mechanical. It should not reopen finished historical research unless current-main evidence exposes a real conflict.

## 9. Required holster status card

Every research chat should finish with a compact status card so several ready portfolios can be managed without confusion.

Recommended format:

```text
TEAM: <school>
STATUS: RESEARCH_FROZEN
research_base_sha: <sha>
portfolio_zip_sha256: <sha>

competitive games: <count>
on-court record: <record>
opponent labels: <count>
unresolved opponent identities: <count>
H/A/N/unknown: <counts>
game types: <counts>
unknown exact dates: <count>
unknown played scores: <count>
venue rows: <count>
new global venue candidates: <count>
owner questions remaining: <none or short list>

CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES
```

If the package uses provisional numeric venue IDs, list them explicitly with the physical venue they represent.

## 10. Suggested queue states

Use simple operational states:

```text
RESEARCHING
RESEARCH_FROZEN
REBASE_REQUIRED
INTEGRATION_FROZEN
PHASE_0
GATE_1
APPLY_RELEASE
COMPLETE
```

After any preceding team merges, every still-holstered `RESEARCH_FROZEN` package should conceptually become `REBASE_REQUIRED` before it enters Codespace.

This does **not** mean redo the research. It means perform the current-main shared-reference check.

## 11. One integration lock

The owner should treat the project Codespace as having one logical integration lock.

At any moment:

- several chats may research independently;
- several ZIPs may be waiting;
- only one school may be mutating the active repository through the onboarding workflow.

Do not interleave tracked Phase 0 work for School A with Gate 1/apply work for School B in the same checkout.

Finish or safely stop one integration before switching the repository to another team.

## 12. Owner questions may still happen in parallel

Parallel research does not require the owner to ignore genuine historical ambiguity.

A research chat may ask a concise owner-level question while another school is being integrated.

That answer should be recorded in the research package notes/manifest, but it does not authorize repository writes or a stale Gate 1 seal.

The main efficiency rule remains:

- routine research stays with the agent;
- owner attention is reserved for real historical judgment.

## 13. Common source files and versioning

If a research lane uses an owner-supplied shared artifact, record exactly which version was used.

For example, an in-progress universal conference-tournament-site workbook may have only certain conference sections authorized as complete.

The package should record:

- file name/version or SHA when available;
- which sections were authorized for that school;
- that unfinished sections were not promoted to canon.

Parallelism must not turn an in-progress shared reference into accidental global truth.

## 14. Quality invariants do not change

Parallel research does not relax any basketball-data rule.

Every package must still preserve:

- one real game = one canonical game;
- raw source evidence;
- on-court result policy;
- explicit H/A/N evidence rather than geography inference;
- stable game-type taxonomy;
- honest unknowns;
- exhibition exclusion;
- postseason normalization;
- authoritative accomplishment verification;
- source provenance;
- reciprocal conflicts rather than silent overwrites.

The speed gain comes from overlapping waiting/research time, not from skipping research.

## 15. Recommended operating rhythm

A practical high-major rhythm is:

```text
Codespace integration: Team A
Holster:               Teams B, C, D, E, F
```

When Team A reaches Production complete:

1. Team B performs current-main rebase and enters the integration lane;
2. start research for Team G;
3. Teams C-F remain research-frozen/rebase-required;
4. repeat.

Five is an operationally useful default because it creates a full queue without making status management unwieldy. It is not a data-model requirement.

## 16. Definition of a safe parallel pipeline

The pipeline is safe when:

- research work is parallel;
- repository writes are serialized;
- each portfolio records its research baseline;
- new numeric global IDs are treated as provisional;
- every holstered package is rebased against current main before Phase 0;
- duplicate physical venues/reference identities are reused rather than recreated;
- package QA and hashes are refreshed after rebase;
- preflight/Gate 1 happens only after integration freeze;
- each team still passes the exact sealed apply/release workflow independently.

The desired result is higher throughput with the same historical and repository quality.