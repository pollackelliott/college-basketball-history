# Post-publication correction lifecycle

- **Status:** Controlling workflow for bounded corrections to an already-published school.
- **Does not replace:** normal new-school Research / `RESEARCH_FROZEN` / `stage_research_portfolio.py` onboarding.
- **Design rule:** this path is additive and isolated. Standard new-school commands and acceptance behavior remain unchanged.

## 1. When this path applies

Use this workflow only when all of the following are true:

1. `schools/<school_key>/` already exists on protected `main` and the school is already published.
2. Research has produced a bounded durable correction checkpoint whose authorized population is explicit.
3. The assignment is a correction to that accepted published state, not permission to reopen the school's entire historical portfolio.

Examples include a missing completed season supplement, a bounded set of existing-game site patches, or an exact field correction such as a settled H/A/N map.

Do **not** route a new school through this workflow. Do **not** use it to bypass ordinary Research acceptance for a new portfolio.

## 2. Authority model

A correction freeze certifies an **authorized delta against an immutable published baseline**. It does not require every unchanged legacy row to satisfy every rule added after the original publication.

The correction therefore has two independent authorities:

- the immutable published baseline at `research_base_sha`; and
- the accepted correction Research checkpoint/digest.

Unchanged pre-existing debt is outside the correction unless the correction checkpoint explicitly includes it. Any new or changed source row must satisfy current scoped Research safeguards. Canonical/publication gates remain active during Implementation so the correction cannot make the published result worse or lose known evidence.

## 3. Mechanical candidate materialization

After bounded correction Research is accepted, the serialized correction Implementation lane may mechanically materialize a complete six-file candidate package by applying only the accepted correction to the six-file package at `research_base_sha`.

This is representation work, not a new Research pass. The materialization must not invent historical decisions or repair unrelated legacy populations. Supporting `opponents.csv`, `venues.csv`, notes, or source-notes changes are permitted only when they are mechanically necessary to represent the accepted correction.

The candidate ZIP uses the ordinary six flat package members:

- `source-games.csv`
- `opponents.csv`
- `venues.csv`
- `conferences.csv`
- `notes.md`
- `source-notes.md`

## 4. Correction freeze

Run the permanent correction entrypoint:

```bash
python tools/correction_lifecycle.py freeze <school_key> <candidate.zip> \
  --research-base <research_base_sha> \
  --scope <season-supplement|field-correction> \
  --research-authority-ref <checkpoint-name-or-ref> \
  --research-authority-digest <checkpoint-digest>
```

The first run is report-only. It emits the exact source-game add/field-change population, hashes every package member, emits exact supporting-file unified diffs, runs current scoped site/HOME chronology safeguards against every changed/new source row, and prints `correction_diff_sha256`.

The Implementation lane must compare that exact diff to the accepted correction checkpoint. If they match, rerun with:

```bash
  --expected-diff-sha256 <exact_diff_sha256> \
  --output <school>-correction-research-frozen.zip
```

For a completed-season supplement, also provide `--required-completed-season-cutoff`.

A successful artifact has status `CORRECTION_RESEARCH_FROZEN`. The frozen ZIP contains the exact full six-file candidate plus `correction-freeze.json`, including baseline/candidate hashes, the exact correction diff, the accepted Research authority reference/digest, and the complete changed/new source-game ID population.

Source-game deletion is intentionally unsupported by this first correction contract. A future correction that genuinely requires deletion must stop for an explicit tooling extension rather than weakening the invariant silently.

## 5. Current-main correction staging

Correction Implementation remains serialized under the one-active-Implementation mutation lock.

Create a clean dedicated branch from current `origin/main`:

```text
data/<school_key>-correction
```

Then dry-run:

```bash
python tools/correction_lifecycle.py stage <school_key> <correction-frozen.zip> \
  --expected-sha256 <freeze_zip_sha256>
```

The stage command requires:

- branch HEAD exactly equal to current `origin/main`;
- `research_base_sha` to remain an ancestor of current main;
- the target school's current six-file package hashes to still equal the frozen published baseline;
- every physical venue used by a correction row to already resolve to the current global venue registry;
- the frozen candidate to still pass scoped correction acceptance.

If the target package changed since Research, stop for a bounded correction rebase. If the correction needs a new or changed shared/global reference, stop and use the existing shared-reference authority workflow. The correction stage deliberately does not mutate global registries.

Apply and checkpoint only after the dry run is clean:

```bash
python tools/correction_lifecycle.py stage <school_key> <correction-frozen.zip> \
  --expected-sha256 <freeze_zip_sha256> --apply --commit
```

This writes the ordinary ignored `.onboarding/<school>/integration-freeze.json` with `workflow_kind=POST_PUBLICATION_CORRECTION`, the pre-correction source semantic baseline, the correction source-game population, and the ordinary Integration Freeze semantic guard. It then runs repository validation and commits only the target school's six-file package changes.

## 6. Downstream Implementation

After correction staging, use the existing repository-owned Stage 2, Gate 1, sealed apply, verification, Preview/Gate 2, merge, and Production-proof workflow.

No historical conflict is silently pre-applied. If the accepted correction checkpoint deliberately preserved a Gate 1 conflict, it remains a Gate 1 decision. Previously explicit owner historical authority may be carried through as durable correction authority without manufacturing a second owner decision.

The implementation site gate remains full-strength for canonical/public output. For source-side Research debt only, an explicit correction Integration Freeze scopes the source-side Research gate to rows changed by the correction (plus later semantic source patches). Unchanged pre-existing source debt therefore cannot force an unrelated whole-school re-research. Stage 2 package preflight applies the same authority boundary narrowly to an exact unchanged published-baseline source row whose curated venue is absent from the target school's local venue table: that legacy registration gap is recorded as a warning rather than absorbed into the correction. Correction rows and any subsequently modified legacy row remain subject to the ordinary blocking validator.

Stage 2 source/global assertion synchronization also recognizes one narrow correction-only intermediate state. When exactly one existing global assertion still reproduces the immutable pre-correction semantic snapshot, the tracked correction source row exactly reproduces the post-correction Integration Freeze snapshot, and the assertion mismatch is exactly the authorized baseline-to-frozen delta for a listed correction source ID, preflight records that mismatch as pending correction reconciliation rather than blocking before the decision universe can be generated. The corresponding discrepancy decision remains in Gate 1 and the global assertion is not synchronized until the ordinary sealed apply authorizes it. Any out-of-scope assertion drift, incorrect original assertion value, extra mismatched field, multiple assertion, untrusted snapshot, or modified correction row remains a blocker. Standard new-school manifests do not activate these correction-only exceptions and retain the existing full-source behavior unchanged.\n\nDisposable recommendation rehearsal, pre-seal technical rehearsal, and sealed apply must preserve this exact correction-only authority boundary. The shared repository-copy helper continues to exclude all ignored `.onboarding/` state by default; for a verified correction Integration Freeze it transfers only that school's exact validated `integration-freeze.json` into the temporary repository. Verification checks the school/status, correction IDs, both hashed semantic snapshots, the authorized pre/post delta, and the tracked frozen source ledger before copying. No other onboarding artifact is transferred, no authority is reconstructed in the copy, and the copy remains outside the tracked apply allow-list. Invalid correction context fails closed; ordinary new-school copies retain full-source site validation. Both disposable and copied-state publication/canonical site gates remain full-strength.

## 7. Stop conditions

Stop rather than broadening the correction when any of these occurs:

- candidate diff contains a source-game change not authorized by the accepted correction checkpoint;
- a published source game would be deleted;
- target six-file package drifted after the correction's `research_base_sha`;
- correction requires a new/changed shared reference;
- changed/new correction rows fail current scoped site or HOME chronology safeguards;
- current-main reconciliation exposes a genuinely new historical conflict;
- downstream canonical/publication gates expose a regression attributable to the correction.

Unrelated legacy debt is recorded but is not automatically absorbed into the correction assignment.