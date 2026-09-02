# Non-D1 Opponent Owner Sanity Scan

- **Status:** Required lightweight owner checkpoint for every school onboarding
- **Purpose:** Catch obvious opponent-identity misclassification before a portfolio is frozen or integrated
- **Scope:** Distinct opponents currently classified as `NON_D1` for the target school
- **Nature of checkpoint:** Sanity scan only; not a new full research gate and not a substitute for agent research

## 1. Why this checkpoint exists

Historical source labels can conceal current Division I programs, historical aliases, predecessor/successor identities, parsing artifacts, campus/branch distinctions, or other normalization problems. Mechanical opponent normalization and research remain the collaborator's responsibility, but a short owner scan of the final `NON_D1` population is a useful last defense against an obvious identity error slipping into publication.

The checkpoint is intentionally narrow. It must not turn the owner into the primary opponent researcher and must not require re-research of every legitimate non-D1 opponent.

## 2. Required presentation

Before the relevant freeze point, present the owner with the target school's complete distinct list of opponents currently classified as `NON_D1`.

For each distinct entry, include at minimum:

- normalized/canonical opponent label or key used by the package;
- total game count represented for the target school;
- representative literal/raw source label(s), especially where they differ from the normalized label;
- a concise note only when identity is potentially non-obvious.

The presentation should be compact enough for a rapid visual scan. Group obvious repeated aliases where useful, but do not hide distinct normalized identities.

## 3. Timing for newly researched schools

For a school whose research is still in progress, perform the scan **after opponent research and package QA are substantively complete but before final `RESEARCH_FROZEN` declaration**.

Sequence:

1. collaborator completes ordinary opponent-identity research;
2. collaborator generates the complete distinct `NON_D1` list with counts/raw labels;
3. owner performs a quick sanity scan;
4. any flagged rows receive narrow identity follow-up/correction;
5. package QA/hashes are refreshed if the package changed;
6. only then declare `RESEARCH_FROZEN`.

A clean owner scan does not require a separate formal approval artifact unless current tooling later adds one.

## 4. Timing for already-frozen holster portfolios

A portfolio that reached `RESEARCH_FROZEN` before this policy was adopted does **not** return to full research merely because the checkpoint did not previously exist.

Instead, perform the scan during current-main rebase, **before `INTEGRATION_FROZEN` and before tracked Phase 0**.

This rule applies to any already-frozen portfolio waiting in the holster, including portfolios whose research predates opponent-identity remediation work.

If the owner flags an obvious issue, correct only the affected opponent identity and any mechanically dependent package fields, then rerun the appropriate package QA and hashes. Do not reopen unrelated research.

## 5. What the owner is checking for

The owner scan is specifically intended to catch entries that appear likely to be:

- a current-D1 program under an alias or malformed label;
- a historical name for a program already represented elsewhere;
- a predecessor/successor identity that should normalize differently;
- a parsing or presentation artifact;
- a campus/branch distinction that appears incorrectly collapsed or split;
- another obvious opponent-identity problem visible from the list.

The owner is **not** expected to independently verify every legitimate junior college, club, military, preparatory, YMCA, high school, service, non-varsity, lower-division, or other historical non-D1 opponent.

## 6. Agent responsibility remains primary

Before presenting the list, the collaborator must already have done reasonable opponent-identity research. Do not intentionally pass suspicious entries to the owner merely because the owner scan exists.

The scan is a final sanity check, not a substitute for:

- historical alias research;
- current/shared program-registry checks;
- reciprocal-source research where useful;
- source-label preservation;
- correct historical classification policy;
- resolving clear parsing defects before owner review.

## 7. Owner response semantics

The owner may respond in simple terms such as:

- `looks good` / no flagged rows; or
- identify one or more entries that appear wrong or deserve a bounded follow-up.

A flagged row is not itself a final canonical ruling unless the owner explicitly supplies one. The collaborator should investigate the flagged identity using authoritative evidence and current repository policy, then correct or explain it.

## 8. Relationship to Owner Gate 1

This checkpoint is **not** Owner Gate 1 and should not be delayed until canonical preflight when it can be performed earlier.

For new research lanes it belongs immediately before `RESEARCH_FROZEN`.

For previously frozen portfolios it belongs during current-main rebase before `INTEGRATION_FROZEN`.

If a later canonical preflight exposes an additional opponent-identity question that was not visible in the research-time list, handle that question normally under the onboarding workflow. The existence of this scan does not suppress later genuine evidence.

## 9. Quality rule

A school must not pass the relevant freeze point with an owner-flagged `NON_D1` identity still unexplained.

The acceptable outcomes are:

- corrected normalization/classification;
- evidence-supported retention as `NON_D1`;
- or an explicitly documented unresolved identity where current repository policy permits uncertainty.

Unsupported certainty remains worse than a documented unknown.

## 10. Pipeline invariant

From adoption of this policy forward:

> **Every school receives one complete owner sanity scan of its distinct `NON_D1` opponent population before the school first becomes eligible for tracked repository integration.**

For new research, that means before `RESEARCH_FROZEN`.

For portfolios already frozen when this policy was adopted, that means during current-main rebase before `INTEGRATION_FROZEN`.
