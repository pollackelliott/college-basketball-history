# Onboarding Process Hardening — Post-Iowa Amendment

- **Status:** Required process amendment after Iowa (Team #19)
- **Applies to:** every school entering serialized Implementation after Iowa
- **Goal:** more throughput without less historical or repository quality

Iowa proved that the permanent onboarding architecture is sound, but exposed a specific inefficiency: deterministic technical failures were first discovered after Owner Gate 1 had been sealed. That produced repeated preflight → carry-forward → reseal cycles even when basketball-history decisions had not changed.

This amendment moves repeatable checks earlier, automates Gate 1 mechanics, and replaces one-command-at-a-time technical handoffs with guarded phase-sized operations. The historical rules in `new-team-onboarding-runbook.md`, shell rules in `codespace-terminal-safety.md`, parallelism rules in `parallel-portfolio-pipeline.md`, and release guarantees in `school-onboarding-fast-path.md` remain authoritative.

## 1. Interaction standard: phase-sized, not command-sized

The Implementation lane should normally use one guarded operation for each reversible technical phase:

1. repository/main checkpoint and onboarding-branch creation;
2. research acceptance + current-main Phase 0 staging;
3. authoritative preflight;
4. compact Gate 1 decision encoding;
5. pre-seal technical rehearsal;
6. sealed apply;
7. release preparation;
8. Owner Gate 2 Preview approval;
9. merge + exact Production proof.

Stop between phases only when repository state is unexpected, a genuine historical judgment is required, an irreversible boundary is being crossed, or a tool reports a blocker that cannot be resolved mechanically.

Phase-sized work must still obey terminal safety: no interactive `set -u`, no `set -euo pipefail`, no unsafe interactive `exit`, no `git add -A`, and complex guarded shell work belongs in a `/tmp` child script.

## 2. Research freeze is an executable acceptance state

A portfolio should not be called `RESEARCH_FROZEN` merely because extraction and row counts look complete.

When the repo tooling is available, run:

```bash
python tools/onboarding_hardening.py research-check <school_key> <portfolio.zip> \
  --expected-sha256 <research_zip_sha256>
```

If the research lane does not have the repo mounted, the serialized Implementation lane runs this immediately upon receipt, before Phase 0 writes.

The acceptance gate checks, at minimum:

- exactly the six flat package files;
- stable source-game IDs;
- valid season/date formatting when known;
- `overtime_periods` is blank or a nonnegative integer;
- resolved opponent keys;
- valid site/game-type vocabulary;
- atomic city/state pairs;
- every curated venue name represented in local `venues.csv`;
- every NCAA Tournament row has complete curated venue, city, and state;
- any populated NCAA curated postseason round uses the project's controlled vocabulary;
- a blank NCAA round remains valid when the historical tournament format or game does not map honestly to that controlled vocabulary; do not fabricate a modern round label merely to satisfy QA;
- no exhibition-like row remains in the competitive package.

Unknown exact dates and unknown played scores remain valid when historically honest; they are reported rather than guessed.

The purpose is to keep ordinary research-completeness defects—such as Iowa's initially missing NCAA sites—out of serialized preflight.

## 3. Phase 0 is one guarded current-main staging operation

The research ZIP remains immutable transport provenance. The tracked package is created only after current-main rebase.

After synchronizing `main` and creating `data/<school>-onboarding`, dry-run:

```bash
python tools/stage_research_portfolio.py <school_key> <portfolio.zip> \
  --expected-sha256 <research_zip_sha256> \
  --research-base <research_base_sha> \
  --history-start-season YYYY-YYYY \
  --history-scope-basis <owner-approved-basis> \
  --history-scope-notes "<owner scope note>"
```

Review the mapping summary, then normally rerun with:

```text
--apply --commit
```

The staging tool requires the onboarding branch to point exactly at current `origin/main`, requires `research_base_sha` to be an ancestor of current main, verifies the ZIP and research acceptance gate, rebases venue identities, reuses mechanically safe global identities, ignores research-time numeric IDs when creating genuinely new physical venues, assigns every new physical venue the next authoritative global ID from current main, stops on ambiguous physical identity, installs the six files, applies owner-confirmed scope metadata, validates, writes ignored `.onboarding/<school>/integration-freeze.json`, and can create the stable Phase 0 checkpoint.

`RESEARCH_FROZEN` remains immutable source/research provenance. The integration manifest records the current-main `INTEGRATION_FROZEN` mapping and fresh member hashes.

## 4. One authoritative preflight and one owner packet

From the clean Phase 0 checkpoint:

```bash
python tools/onboard_school.py <school_key> --preflight
```

The agent compresses the machine review into one human Gate 1 packet. The owner should not manually parse or fill a large CSV.

After owner approval, encode the batch with one compact JSON map:

```bash
python tools/onboarding_hardening.py fill-review <school_key> \
  --map /tmp/<school>-gate1-map.json
```

The map supports identity choices, ordinary discrepancy defaults, selected-candidate conditional defaults, exact overrides, and exact/default bases. The tool parses full `CBBG-#######` IDs and automatically marks rejected identity-candidate conditionals `NOT_APPLICABLE`.

That automation specifically prevents the Iowa bug caused by ad hoc hyphen-splitting of canonical IDs.

## 5. Required new boundary: pre-seal technical rehearsal

After the owner has approved the packet and `review.csv` is filled—but before cryptographic sealing—run:

```bash
python tools/onboarding_hardening.py rehearse-review <school_key>
```

This constructs the approved plan in memory and runs the same disposable-repository transaction and automated gates that sealed apply will later run:

- ingestion;
- generic reconciliation;
- publication/accomplishment metadata;
- deterministic site build;
- repository validation;
- target package no-op;
- accomplishment cross-check;
- site dry run;
- full unit suite;
- changed-path allow-list;
- whitespace checks.

The real tracked repository is not mutated and no `approved-plan.json` is sealed.

A passing result prints `TECHNICAL READINESS PASSED`. Only then should Gate 1 be cryptographically sealed.

This is designed to surface defects like Iowa's legacy partial Los Angeles state, unresolved canonical Play-in normalization, and stale scope regression test before the approval boundary.

## 6. Purely technical repairs do not reopen unchanged history

If pre-seal rehearsal finds a technical defect:

1. repair it at the narrowest correct layer;
2. validate and checkpoint the repair;
3. preserve the already owner-approved review outside regenerated `.onboarding` state;
4. rerun authoritative preflight;
5. run:

```bash
python tools/onboarding_hardening.py carry-forward <school_key> \
  --from-review /tmp/<school>-previous-approved-review.csv
```

Carry-forward succeeds only if the decision-ID set is identical, every substantive decision input is identical, every prior action remains allowed, and every prior action/basis is complete.

If any substantive historical input changes, the command stops and only the changed/new decisions return to the owner. If nothing changed, owner approval carries forward without another interruption. Then rerun `rehearse-review`.

## 7. Seal once technical readiness passes

Once the filled review passes pre-seal rehearsal:

```bash
python tools/onboard_school.py <school_key> \
  --approve \
  --approved-by "Elliott"
```

Run only the exact sealed apply command printed by that tool.

The expected normal path is now:

```text
preflight
→ one Owner Gate 1 packet
→ fill-review
→ pre-seal rehearsal PASS
→ seal once
→ apply once
```

A post-seal apply failure should become exceptional.

## 8. Scope tests enforce the invariant, not named-school exceptions

Do not maintain school-specific expected-exclusion dictionaries such as `{"iowa": 2}`.

The generic rule is:

- a game before one program's approved public scope may remain canonical because another program supplies legitimate reciprocal evidence;
- the out-of-scope program itself must not have an ingested assertion for that game;
- the canonical game must still have at least one evidence source.

Tests must enforce that rule directly. A future school with legitimate reciprocal pre-scope games must not require another named exception.

## 9. Release boundary remains unchanged

After successful sealed apply:

```bash
python tools/release_school.py <school_key> --prepare
```

Owner Gate 2 reviews the exact PR-head Preview. After approval:

```bash
python tools/release_school.py <school_key> --merge --preview-approved
```

The release PR labels the apply-generated path list as the **Sealed apply boundary**. That list is intentionally narrower than the complete PR diff: committed Phase 0 package/reference changes, including new global venue/reference rows, are also part of the PR and remain visible in GitHub's full changed-file review.

Preview success is never Production success. Exact merged-main Production proof remains mandatory.

## 10. Success criterion for the next proving school

The next school entering Implementation should prove this hardened sequence:

```text
1 research acceptance
1 current-main Phase 0 staging/checkpoint
1 authoritative preflight
1 Owner Gate 1 conversation
1 pre-seal technical rehearsal
1 cryptographic seal
1 transactional apply
1 release preparation
1 Owner Gate 2 Preview approval
1 merge/Production proof
```

Repeated technical reseals, giant owner copy/paste reports, manual conditional-row scripting, or school-specific scope exceptions are process regressions unless a genuinely new historical exception requires them.

The objective remains: **MORE THROUGHPUT WITHOUT LESS QUALITY.**
