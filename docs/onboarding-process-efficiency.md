# Onboarding Process Efficiency: Purdue-Proven Operating Model

- **Status:** Required companion to `school-onboarding-fast-path.md`
- **Proving case:** Purdue, Team #16
- **Baseline after proof:** `main` at `6212cb0bf4c3d0c3980f6889d4fa915e2a1efc13`
- **Purpose:** Preserve the process improvements that made Purdue onboarding fast, auditable, and low-churn without reducing historical rigor.

This document explains the operating improvements that turned new-school onboarding from a long sequence of technical handoffs into a small number of deterministic phases with two owner gates.

It is not a replacement for the historical rules in `new-team-onboarding-runbook.md`, the data contracts in `data-schema.md`, or the executable procedure in `school-onboarding-fast-path.md`. It records **how to run those rules efficiently**.

## Executive summary

The central improvement is simple:

> **Finish and freeze the school package first, then let one generic preflight expose the complete reconciliation problem before changing global data.**

From that point forward, owner attention is reserved for actual basketball/history decisions. Technical work is guarded, batched, reproducible, and fail-fast.

The successful pattern is:

1. finish the six-file school portfolio outside global canonical data;
2. freeze it with hashes and an exact-file manifest;
3. perform one read-only repository checkpoint before any writes;
4. install the package and only the minimum reference prerequisites in one guarded Phase 0;
5. commit a stable package checkpoint;
6. run exactly one generic onboarding preflight;
7. compress the machine review into one owner decision batch;
8. research only the rows that genuinely need research;
9. cryptographically seal the approved batch;
10. run one transactional apply in a disposable repository copy;
11. explicitly close any target-assertion gap without forcing counts to agree;
12. let the release tool own the commit, PR, Preview, merge, and exact Production proof;
13. interrupt the owner only for Gate 1 decisions and Gate 2 visual approval.

Purdue demonstrated that this can remain historically careful while eliminating most of the command-by-command plumbing that slowed earlier teams.

---

## 1. Separate portfolio construction from repository mutation

The six-file school portfolio should be treated as an input artifact, not as a partially built repository state.

For Purdue, the package was completed before repository integration and transported as a ZIP containing exactly:

```text
source-games.csv
opponents.csv
venues.csv
conferences.csv
notes.md
source-notes.md
```

The package had already passed package-level QA before it touched the onboarding branch.

### Why this is faster

Earlier onboarding work often mixed source extraction, cleanup, canonical matching, reference edits, and repository validation in the same loop. That made every newly discovered issue capable of reopening work that had already been completed.

Freezing the portfolio first creates a clean boundary:

```text
historical/source work  ->  stable six-file package  ->  repository reconciliation
```

Once the package is frozen, repository work should not silently alter source history just to make ingestion easier. If the package itself truly needs a correction, make that correction deliberately and rerun preflight.

### Transport rule

When a package is transferred into the Codespace as a ZIP:

- record its SHA-256 before extraction;
- require exactly six expected flat archive entries;
- reject extra files, directories, duplicate names, and path traversal;
- verify the individual extracted file hashes when available;
- delete the transport ZIP after successful verified extraction;
- never commit the ZIP.

This turns file transfer into a deterministic checkpoint rather than an informal copy operation.

---

## 2. Make Phase 0 read-only before making it clever

Before the first tracked write, run one compact read-only checkpoint that proves the repository and package state.

At minimum, verify:

- current branch;
- current HEAD;
- clean tracked worktree;
- local `main` and `origin/main` relationship;
- expected prior production checkpoint in `main` ancestry;
- package ZIP presence;
- package SHA-256;
- exact archive member list.

A normal safe starting state may include only the untracked transport ZIP.

### Why this matters

This eliminates a large class of later uncertainty. Once the checkpoint passes, every subsequent failure can be interpreted relative to a known baseline rather than reconstructed from memory.

The rule is:

> **Do not repair an unexpected repository state automatically. Stop and identify it.**

Do not blindly stash, reset, delete an existing branch, or overwrite tracked work.

---

## 3. Use one guarded Phase 0 install, not serial command handoffs

After the read-only checkpoint, perform the routine setup as one guarded block:

- create `data/<school>-onboarding` from current `main`;
- extract the six files into `schools/<school>/`;
- verify package counts and invariants;
- add the owner-confirmed history scope;
- add only genuinely new physical venue identities and required display-name rows;
- run repository validation;
- stage an explicit path allow-list;
- create one stable package checkpoint commit.

### Minimum reference edits only

Phase 0 should not become a second reconciliation engine.

Before preflight, change only reference data that must exist for the package to be interpretable, such as:

- `history_start_season` and its owner-confirmed basis;
- genuinely new global venue identities;
- required canonical display-name rows for those venues.

Research accomplishment values before Gate 1, but normally let the onboarding decision machinery apply the accomplishment row after the owner approves it. Do not manually pre-solve downstream decisions that the generic preflight is designed to present.

### No school-specific reconciliation code by default

A new school should not require a bespoke script merely because it has discrepancies. The generic preflight, approval, reconciliation, and transactional apply tools are the default path.

A school-specific program is justified only if the generic tooling cannot express a real reusable class of problem. If that happens, improve the generic tool when practical rather than accumulating one-off scripts.

---

## 4. Preserve line endings; validate whitespace correctly

Purdue exposed one useful technical lesson during Phase 0.

The reference CSVs used CRLF line endings. A normal `git diff --check` treated the carriage return as trailing whitespace and stopped the first install attempt even though the data was fine.

The correct response was **not** to normalize the files wholesale to LF. That would have created noisy full-file diffs and obscured the substantive changes.

Use the repository's CRLF-safe whitespace treatment instead, for example:

```bash
git \
  -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol \
  diff --cached --check
```

General lesson:

> **A formatting gate should detect real formatting defects, not create repository churn.**

When a technical gate fails, determine whether it found a real data problem before editing data to satisfy it.

---

## 5. Commit one stable package checkpoint before preflight

The package checkpoint is the handoff between package construction and canonical reconciliation.

It should contain:

- the six school files;
- approved history-scope metadata;
- only required new reference identities needed to interpret the package.

It should **not** yet contain the global ingestion/reconciliation output.

Why commit here:

- preflight has a stable fingerprintable base;
- Gate 1 approval can be tied to exact inputs;
- later technical failures do not require redoing research;
- it is obvious which changes are source-package foundation versus reconciliation output.

For Purdue, the stable package checkpoint was:

```text
336daca142bfbf2c7244186d5db8eba57e92fa36
```

---

## 6. Run one preflight and expose the whole problem at once

The command is:

```bash
python tools/onboard_school.py <school_key> --preflight
```

Do not discover identity ambiguity, score conflicts, site conflicts, accomplishments, and publication readiness in separate owner interactions.

The preflight should produce one complete decision universe before tracked canonical changes occur.

For Purdue it produced:

```text
Blockers:   0
Warnings:   0
Decisions:  124
Prediction: 855 matches, 2,218 new
            57 definite discrepancies
            52 conditional discrepancies
```

The 124 machine rows were not 124 separate conversations. They were one review dataset to be compressed.

---

## 7. Compress machine review into owner decisions

The owner should not be used as a terminal parser.

A raw `review.csv` is an audit artifact, not necessarily the best human interface. The collaborator/agent should:

1. group rows by identity, definite discrepancy, conditional discrepancy, accomplishments, and publication;
2. resolve which conditional rows belong to each candidate identity;
3. collapse duplicate-meeting identity ambiguities using date, score, opponent, result, and site context;
4. distinguish obvious reciprocal-source conflicts from genuinely uncertain history;
5. present a compact ruling sheet with recommended actions and evidence.

### Targeted extraction beats giant copy/paste

If a large report is clipped or awkward to paste, do not make the owner retry the entire dump. Generate a small extractor for only the missing subset.

During Purdue review, a clipped large paste was recovered by requesting only the 18 missing early definite discrepancies. That preserved momentum and avoided reproducing information already available.

General rule:

> **Ask for the smallest missing evidence needed to close the decision batch.**

---

## 8. Research selectively, not mechanically

Historical rigor does not require researching every machine-generated discrepancy from scratch.

Use this order:

1. package evidence;
2. already-onboarded reciprocal evidence;
3. official program history/opponent pages;
4. official contemporary game recaps, media guides, or event material;
5. broader archival research only when still necessary.

Research is most valuable when it can change the disposition.

Do not spend time re-proving rows whose existing evidence already makes `KEEP_CANONICAL` or `USE_SOURCE` obvious. Spend it on:

- genuine score/date conflicts;
- home/away/neutral disagreements that change public presentation;
- ambiguous same-season identities;
- historical games where authoritative sources remain materially inconsistent.

### Preserve unresolved history honestly

`LEAVE_UNRESOLVED` is a successful outcome when authoritative sources genuinely conflict.

It is better to preserve a defensible canonical value plus explicit conflicting evidence than to force false certainty.

Purdue Gate 1 ultimately resolved the 57 definite discrepancies as:

```text
19 USE_SOURCE
34 KEEP_CANONICAL
 4 LEAVE_UNRESOLVED
```

The 52 conditional rows collapsed to:

```text
15 KEEP_CANONICAL on selected identities
37 NOT_APPLICABLE on rejected identity candidates
```

---

## 9. Make Gate 1 one owner act, then seal it

The owner should approve the full historical/reconciliation batch once.

After approval, encode the decisions into `review.csv`, verify:

- zero `PENDING` rows;
- every decision is one of that row's allowed actions;
- every applicable decision has a resolution basis;
- expected category/action totals reconcile.

Then seal:

```bash
python tools/onboard_school.py <school_key> \
  --approve \
  --approved-by "Elliott"
```

The resulting SHA-256 plan hash is the immutable Gate 1 approval boundary.

For Purdue:

```text
7a38ae038dd3e6f1bfcdab63570bd8f77d50f21314739b3c002a998959973d4f
```

After this point, do not make silent package, canonical, evidence, or decision changes. A real change requires a new preflight and approval.

---

## 10. Apply transactionally in a disposable repository copy

Run exactly the command printed by approval:

```bash
python tools/onboard_school.py <school_key> \
  --apply \
  --approved-plan <exact_hash>
```

The key process improvement is that apply rehearses the entire operation outside the real tracked working tree first.

A successful rehearsal must prove:

- exact sealed-plan hash and fingerprints;
- identity decisions applied as approved;
- reconciliation completed generically;
- target package becomes a full ingestion no-op;
- accomplishments match;
- public site build is deterministic;
- unit tests pass;
- changed paths stay inside the apply allow-list;
- the copied-back real state passes the same validation again.

If rehearsal fails, do not begin hand-editing the real repository. Inspect the reported gate while the real tracked state is still protected.

---

## 11. Treat target assertion closure as a real historical check

A target package row count and a target public-game count do not have to be identical.

After Purdue apply:

```text
Purdue source rows:       3,086
Canonical Purdue games:   3,087
```

The one extra canonical game was an independently preserved Minnesota assertion for a 1907-08 Purdue forfeit that did not exist in Purdue's own chronological package.

That was not a duplication bug. It was legitimate reciprocal evidence.

The correct closure process is:

1. enumerate every in-scope canonical target game lacking a target-source assertion;
2. inspect each one;
3. keep legitimate reciprocal-only canonical games;
4. do not invent a target assertion;
5. do not delete a real canonical game merely to force counts to match.

This check protects the project's central principle: one real game, one canonical game, with multiple independent evidence streams allowed to disagree or be incomplete.

---

## 12. Let the release tool own the release boundary

After a successful transactional apply:

> **Do not manually commit.**

The release manifest is tied to the HEAD on which apply ran. A manual commit breaks that boundary and forces a new preflight/approval/apply cycle.

Run:

```bash
python tools/release_school.py <school_key> --prepare
```

The release tool should own:

- final local gates;
- explicit-path staging;
- release commit;
- push;
- PR creation/reuse;
- CI/check monitoring;
- exact PR-head Vercel Preview discovery;
- generated visual-QA checklist.

Then stop for Owner Gate 2.

This removes a large amount of release-time command choreography and makes the preview the only second owner interruption.

---

## 13. Gate 2 is visual QA of the exact artifact, not another data-review cycle

The owner inspects the exact Preview URL produced for the exact PR head.

The generated checklist should cover:

- target page existence and record;
- history-scope display;
- accomplishments;
- recent season;
- postseason labels;
- venue/H-A-N spot checks;
- affected existing public pages;
- desktop/mobile sanity.

If the preview passes:

```bash
python tools/release_school.py <school_key> \
  --merge \
  --preview-approved
```

Any PR-head change after Preview approval requires another Preview approval.

---

## 14. Production proof must be exact

The merge step is not finished when GitHub says "merged."

The release tool should:

- fast-forward local `main` to the merge;
- rerun repository validation;
- prove target ingestion is still a no-op;
- rerun accomplishment verification;
- rerun deterministic site dry-run checks;
- rerun unit tests;
- wait for Production tied to the exact merged-main SHA;
- compare the expected generated JSON documents against Production.

For Purdue, final proof reported:

```text
PRODUCTION QA PASSED
Merged SHA: 6212cb0bf4c3d0c3980f6889d4fa915e2a1efc13
Exact JSON documents verified: 18
main is clean and synchronized with origin/main.
```

That is the definition of done.

---

## 15. Anti-churn rules

The following behaviors should be considered process regressions unless a real exception requires them:

- repeated one-command-at-a-time technical handoffs for routine setup;
- asking the owner to manually parse giant machine reports when a digest can be generated;
- researching every discrepancy instead of triaging by decision value;
- writing school-specific reconciliation code before exhausting generic tooling;
- editing canonical data before one complete preflight exists;
- changing tracked inputs after Gate 1 without resealing;
- manually committing after transactional apply;
- equating Preview success with Production success;
- forcing target package counts to equal canonical perspective counts;
- fabricating source assertions to close a count gap;
- normalizing entire files merely to satisfy a line-ending false positive;
- reopening owner decisions because of an unrelated technical failure.

Technical failures should be fixed technically. Historical decisions should be reopened only when historical inputs materially change.

---

## 16. Purdue proving-case metrics

Purdue demonstrated the operating model at useful scale:

```text
Six-file source package:        3,086 competitive games
Source on-court record:         2,001-1,085
Opponent labels:                324, all resolved
Venue rows:                     64
Preflight blockers/warnings:    0 / 0
Preflight decisions:            124
Identity decisions:             13
Definite discrepancies:         57
Conditional discrepancies:      52
Gate 1 metadata decisions:       2
Predicted matches/new games:    855 / 2,218
Final public Purdue games:      3,087
Final public record:            2,001-1,086
Final public opponents:         312
Repository tests:               82 passed
Public pages after release:     16
Merged PR:                      #22
Production merge SHA:           6212cb0bf4c3d0c3980f6889d4fa915e2a1efc13
```

The one-game source/public difference was investigated and explained rather than "fixed" artificially.

---

## 17. Preferred owner/collaborator division of labor

### Collaborator / agent

Owns:

- package assembly and QA;
- repository-state safety checks;
- guarded install scripts;
- generic preflight execution;
- review compression;
- targeted historical research;
- decision encoding after owner approval;
- seal/apply mechanics;
- assertion-closure investigation;
- release preparation;
- production proof.

### Owner

Owns:

- program history-scope ruling;
- genuine historical/reconciliation judgment at Gate 1;
- approval of verified accomplishments/publication;
- exact Preview visual approval at Gate 2.

The owner should not normally be asked to perform routine repository plumbing or re-answer unchanged decisions.

---

## 18. Definition of an efficient onboarding

An onboarding is efficient when it is **not merely fast**, but when it minimizes irreversible or repeated work.

The target state is:

- one frozen package;
- one read-only safety checkpoint;
- one guarded setup/install;
- one stable package commit;
- one preflight;
- one consolidated owner decision batch;
- one sealed approval;
- one transactional apply;
- one assertion-closure check;
- one release preparation command;
- one Preview approval;
- one merge/Production proof command.

Historical ambiguity may still require careful research. That is not inefficiency; that is the core work. The efficiency gain comes from removing everything around that research that does not require human judgment.
