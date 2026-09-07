# Research Lane Bootstrap Template

Use this as the compact opening handoff for a **new school Research lane** after `docs/research-lane-bounded-execution.md` is present on protected `main`.

The repository documents are the durable instructions. Do not paste the entire research manual into each new chat.

## New-school bootstrap

```text
We are continuing my College Basketball History project.

Repository:
https://github.com/pollackelliott/college-basketball-history

This chat is ONE INDEPENDENT RESEARCH LANE for one school. It is not the serialized repository-integration lane.

Before beginning research, inspect current protected main, record research_base_sha, and read current AGENTS.md plus docs/research-lane-bounded-execution.md. Follow the current repository research policies those documents reference. Repository policy controls over copied handoff wording.

Use the bounded-stage execution protocol exactly. Work on only the currently authorized stage in each turn. At a completed stage boundary, report the required STAGE X: COMPLETE status, identify the next bounded stage, and STOP. Do not begin the next stage until I respond with Proceed/Continue or equivalent. If a stage cannot safely finish in one turn, preserve a durable checkpoint, report STAGE X: INCOMPLETE — DURABLE CHECKPOINT PRESERVED, identify exactly what remains, and STOP.

My Proceed/Continue response authorizes only the identified next bounded stage or unfinished remainder, not all remaining research through RESEARCH_FROZEN.

Preserve accepted prior stages unless later evidence produces a genuine contradiction. Preserve substantial working artifacts durably whenever possible. Historical uncertainty remains valid; unsupported certainty is worse than a researched unknown.

The target school and owner-supplied sources/constraints follow below.

TARGET SCHOOL: <school>
OWNER-SUPPLIED SOURCES / AUTHORIZATION LIMITS:
<school-specific instructions and attachments>

Begin Stage 1 only.
```

## Normal owner continuation

After a clean completed stage, the owner normally needs to send only:

```text
Proceed.
```

That means exactly what `docs/research-lane-bounded-execution.md` defines: execute the identified next bounded stage and stop again at its boundary.

After an incomplete stage:

```text
Proceed.
```

means resume only the identified unfinished remainder of that same stage.

## Recovery bootstrap for an existing unfinished Research lane

Use this when a prior chat/session failed or must be replaced but durable research state survives:

```text
We are recovering an existing Research lane for <school> in my College Basketball History project.

Before acting, inspect current protected main and read current AGENTS.md plus docs/research-lane-bounded-execution.md. Then reconstruct the actual surviving research state from the durable artifacts and the last accepted stage/checkpoint information I provide below.

Do not restart completed stages. Verify surviving artifacts/fingerprints where available, preserve accepted conclusions, and resume from the earliest incomplete bounded stage. Reopen prior research only if reconstruction exposes a genuine contradiction.

Use the repository bounded-stage response contract. One bounded objective per turn; stop at every stage boundary.

LAST ACCEPTED STATE / DURABLE ARTIFACTS:
<insert concise recovery state>

Resume only the earliest incomplete stage.
```

## What does not belong in the bootstrap

Do not re-copy the full rules for:

- game identity;
- H/A/N evidence;
- site completeness;
- NCAA site requirements;
- opponent normalization;
- NON_D1 owner scan;
- self-challenge;
- venue-ID rebase;
- six-file schema;
- implementation/release workflow.

Those belong in the version-controlled repository documents. School-specific source authorization, unusual historical scope evidence, and genuine owner rulings still belong in the school-specific handoff.