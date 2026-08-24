# Onboarding Process Hardening — Post-Iowa Amendment

- **Status:** Required process amendment after Iowa (Team #19)
- **Applies to:** every school entering the serialized Implementation lane after Iowa
- **Goal:** more throughput without less historical or repository quality

Iowa proved that the permanent onboarding architecture is sound, but also exposed a specific inefficiency pattern: technical readiness failures were discovered only after Owner Gate 1 had already been sealed. That caused repeated preflight -> carry-forward -> reseal cycles even though the historical decision universe had not changed.

This amendment moves deterministic checks earlier, automates repetitive Gate 1 mechanics, and replaces one-command-at-a-time technical handoffs with guarded phase-sized operations.

The historical rules in `new-team-onboarding-runbook.md`, repository safety rules in `codespace-terminal-safety.md`, and release requirements in `school-onboarding-fast-path.md` remain authoritative. This document narrows how those rules should be executed after Iowa.

## 1. Interaction standard: phase-sized, not command-sized

The Implementation lane should not normally ask the owner to paste dozens of tiny setup commands.

Use one guarded operation for each reversible technical phase:

1. repository/main checkpoint and onboarding-branch creation;
2. research-package acceptance + current-main Phase 0 staging;
3. authoritative preflight;
4. compact Gate 1 decision encoding;
5. pre-seal technical rehearsal;
6. sealed apply;
7. release preparation;
8. Gate 2 Preview approval;
9. merge + exact Production proof.

Stop between those phases only when:

- repository state is unexpected;
- a historical/owner judgment is genuinely required;
- an irreversible boundary is about to be crossed;
- a tool reports a blocker that cannot be resolved mechanically.

The permanent terminal-safety rules still apply. Phase-sized work should run through repository tools or `/tmp` child scripts rather than giant unguarded interactive shell blocks.

## 2. Research freeze is now an executable acceptance gate

A six-file package should not be called `RESEARCH_FROZEN` merely because extraction and row counts look complete.

Run the generic acceptance checker whenever the research environment has the repository tooling available:

```bash
python tools/onboarding_hardening.py research-check <school_key> <portfolio.zip> \
  --expected-sha256 <research_zip_sha256>
```

If the research lane itself does not have the repo mounted, the serialized Implementation lane must run this command immediately upon receipt, before Phase 0 writes.

The acceptance gate requires, at minimum:

- exactly the six flat package files;
- stable source-game IDs;
- resolved opponent keys;
- valid site/game-type vocabulary;
- atomic city/state pairs;
- every curated venue name represented in local `venues.csv`;
- every NCAA Tournament row to have complete curated venue, city, state, and curated postseason round;
- no exhibition-like row left in the competitive package.

Unknown exact dates and unknown played scores remain valid when historically honest; they are reported, not guessed.

This rule exists specifically so ordinary research completeness defects—such as missing NCAA sites—do not first surface inside serialized preflight.

## 3. Phase 0 is a guarded current-main staging operation

The research ZIP remains immutable transport provenance. The tracked package is created only after current-main rebase.

After synchronizing `main` and creating `data/<school>-onboarding`, use:

```bash
python tools/stage_research_portfolio.py <school_key> <portfolio.zip> \
  --expected-sha256 <research_zip_sha256> \
  --research-base <research_base_sha> \
  --history-start-season YYYY-YYYY \
  --history-scope-basis <owner-approved-basis> \
  --history-scope-notes "<owner scope note>"
```

The first run is a dry run. Review the rebase summary, then normally run the same command with:

```text
--apply --commit
```

The staging tool:

- requires `data/<school>-onboarding` to point exactly at current `origin/main` before Phase 0;
- requires `research_base_sha` to be an ancestor of current main;
- verifies the immutable ZIP hash and research acceptance gate;
- reuses an existing global venue only on mechanically safe key/name/geography evidence;
- renumbers stale provisional venue IDs when another team consumed the number first;
- registers missing source/historical aliases to an already-resolved physical identity;
- stops on ambiguous physical venue identity instead of guessing;
- installs the six package files;
- applies owner-confirmed history-scope metadata;
- runs repository validation;
- writes ignored `.onboarding/<school>/integration-freeze.json` with final venue mapping and hashes;
- optionally creates the stable Phase 0 package/reference commit.

`RESEARCH_FROZEN` therefore remains immutable historical/source provenance, while the generated integration manifest records the current-main `INTEGRATION_FROZEN` state.

## 4. One authoritative preflight, one owner decision packet

After the clean Phase 0 checkpoint:

```bash
python tools/onboard_school.py <school_key> --preflight
```

The agent should still compress the machine decision set into one owner-readable Gate 1 packet. The owner should not be asked to parse `review.csv` manually.

After the owner approves that packet in chat, encode it with a compact JSON decision map rather than school-specific CSV-editing scripts:

```bash
python tools/onboarding_hardening.py fill-review <school_key> \
  --map /tmp/<school>-gate1-map.json
```

The map supports:

- identity choices keyed by `source_game_id` or exact identity decision ID;
- ordinary discrepancy defaults;
- ordinary selected-candidate conditional defaults;
- exact decision overrides;
- exact or default resolution bases.

The tool expands conditional identity rows itself. A rejected identity candidate is marked `NOT_APPLICABLE` automatically using the full `CBBG-#######` identifier. This eliminates ad hoc candidate-ID parsing and the class of error Iowa exposed.

## 5. New required step: pre-seal technical rehearsal

After the owner has approved the decision packet and `review.csv` has been filled—but **before cryptographic Gate 1 sealing**—run:

```bash
python tools/onboarding_hardening.py rehearse-review <school_key>
```

This command uses the current filled review to construct an in-memory approved plan, then runs the same disposable-repository transaction and automated gate suite that sealed apply will later run:

- ingestion apply;
- generic reconciliation;
- publication/accomplishment metadata;
- deterministic site build;
- repository validation;
- target package no-op;
- accomplishment cross-check;
- site dry run;
- full unit tests;
- changed-path allow-list;
- whitespace gate.

The real tracked repository is not mutated and no `approved-plan.json` is sealed.

The purpose is to expose legacy canonical/evidence/test defects before the cryptographic approval boundary. Iowa's partial Los Angeles state, unresolved canonical Play-in round, and stale scope test would all have surfaced here instead of after repeated seals.

A passing result prints:

```text
TECHNICAL READINESS PASSED
```

Only then should Gate 1 be sealed.

## 6. Technical repair after owner approval does not mean owner re-review

If pre-seal rehearsal finds a purely technical defect:

1. repair it at the narrowest correct layer;
2. validate and checkpoint the repair;
3. preserve the already owner-approved review outside regenerated `.onboarding` state;
4. rerun authoritative preflight;
5. use the generic carry-forward checker:

```bash
python tools/onboarding_hardening.py carry-forward <school_key> \
  --from-review /tmp/<school>-previous-approved-review.csv
```

Carry-forward succeeds only if:

- the decision-ID set is identical;
- every substantive decision input is byte-for-value identical;
- every prior decision remains allowed;
- every prior decision and resolution basis is complete.

If any substantive historical input changed, the command stops and the changed/new decisions return to the owner. If nothing changed, prior approval carries forward automatically without another owner interruption.

Then rerun `rehearse-review`.

## 7. Seal only after technical readiness passes

Once the filled review has passed pre-seal rehearsal:

```bash
python tools/onboard_school.py <school_key> \
  --approve \
  --approved-by "Elliott"
```

Then run the exact sealed apply command printed by the tool.

The expected normal path is now:

```text
preflight
-> one owner Gate 1 packet
-> fill-review
-> pre-seal rehearsal PASS
-> seal once
-> apply once
```

A post-seal apply failure should become exceptional rather than routine.

## 8. Scope tests must validate the rule, not named-school exceptions

Do not maintain a hard-coded dictionary such as:

```python
{"iowa": 2}
```

for legitimate pre-scope reciprocal games.

The generic invariant is:

- a game before one program's owner-approved public scope may remain canonical because another program supplies legitimate reciprocal evidence;
- the out-of-scope program must not itself have an ingested assertion for that game;
- the canonical game must still have at least one evidence source.

Tests should enforce that invariant directly. A future school with legitimate reciprocal pre-scope games must not require another school-name exception.

## 9. Release boundary is unchanged

After successful sealed apply:

```bash
python tools/release_school.py <school_key> --prepare
```

Then Owner Gate 2 reviews the exact PR-head Preview.

After approval:

```bash
python tools/release_school.py <school_key> --merge --preview-approved
```

Preview success is not Production success. Exact merged-main Production proof remains mandatory.

## 10. Success criterion for the next proving school

The next school entering Implementation should prove this hardened path.

The target process is:

```text
1 research acceptance
1 current-main Phase 0 staging/checkpoint
1 authoritative preflight
1 owner Gate 1 conversation
1 pre-seal technical rehearsal
1 cryptographic seal
1 transactional apply
1 release preparation
1 owner Gate 2 Preview approval
1 merge/Production proof
```

Repeated technical reseals, owner copy/paste of giant reports, manual conditional-row scripting, or school-specific known-exclusion tests are process regressions unless a genuinely new historical exception requires them.

The objective remains: **MORE THROUGHPUT WITHOUT LESS QUALITY.**
