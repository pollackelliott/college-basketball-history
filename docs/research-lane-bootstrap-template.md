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

Use the bounded-stage execution protocol exactly. Work on only the currently authorized stage in each turn. At a completed stage boundary, report the required STAGE X: COMPLETE status, identify the next bounded stage, and STOP. Do not begin the next stage until I respond with Proceed/Continue or equivalent. If a stage cannot safely finish in one turn, preserve a portable durable checkpoint containing the exact residual queue(s), report STAGE X: INCOMPLETE — DURABLE CHECKPOINT PRESERVED, identify exactly what remains, and STOP.

My Proceed/Continue response authorizes only the identified next bounded stage or unfinished remainder, not all remaining research through RESEARCH_FROZEN.

Preserve accepted prior stages unless later evidence produces a genuine contradiction. Durable artifacts outrank chat memory. A replacement chat should be able to attach the latest checkpoint, verify it, and continue without rediscovering completed work. Historical uncertainty remains valid; unsupported certainty is worse than a researched unknown.

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

means resume only the identified unfinished remainder of that same stage from its portable checkpoint.

## Recovery bootstrap for an existing unfinished Research lane

Use this when a prior chat/session failed or must be replaced but durable research state survives:

```text
We are recovering an existing Research lane for <school> in my College Basketball History project.

Before acting, inspect current protected main and read current AGENTS.md plus docs/research-lane-bounded-execution.md.

I am attaching the latest durable checkpoint/recovery bundle from the prior lane. Treat verified durable artifacts—not conversational reconstruction—as the controlling continuation state.

Verify the checkpoint ZIP/artifact hash and internal manifest, load the exact serialized residual queue(s), preserve accepted owner dispositions and completed repairs, and resume only the earliest incomplete bounded stage.

Do not restart completed stages. Do not perform open-ended archaeology for hidden/chat-local state. Do not reconstruct completed work from old prose merely because a prior chat said it existed. If the required residual queue is genuinely missing from the attached checkpoint, stop and identify the exact missing artifact/state before doing reconstruction.

Use the repository bounded-stage response contract. One bounded objective per turn; stop at every stage boundary.

LATEST DURABLE CHECKPOINT / EXPECTED HASH:
<attach artifact and insert hash/status>

Resume only the earliest incomplete stage.
```

The intended recovery experience is **attach checkpoint -> verify -> continue**.

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