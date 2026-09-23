# Research Lane Bootstrap Template

Use this as the compact opening handoff for a **new school Research lane** after `docs/research-lane-bounded-execution.md` is present on protected `main`.

The repository documents are the durable instructions. Do not paste the entire research manual into each new chat. A normal new-school handoff should be brief: target school, owner-supplied sources/constraints, and authorization to begin Stage 1. Methodology belongs in version-controlled repository policy, not repeated owner prompts.

## New-school bootstrap

```text
We are continuing my College Basketball History project.

Repository:
https://github.com/pollackelliott/college-basketball-history

This is ONE INDEPENDENT RESEARCH LANE for one school. It is not the serialized repository-integration lane. A long Research lane may span a small number of chats through verified durable checkpoints; one uninterrupted conversation is not required.

Before beginning research, inspect current protected main, record research_base_sha, and read current AGENTS.md plus docs/research-lane-bounded-execution.md, docs/stage3a-regular-season-site-research.md, and docs/shared-reference-authority.md. Follow the current repository research policies those documents reference. Repository policy controls over copied handoff wording.

Use the bounded-stage execution protocol exactly. Work on only the currently authorized stage in each turn. At a completed stage boundary, report the required STAGE X: COMPLETE status, identify the next bounded stage, and STOP. Do not begin the next stage until I respond with Proceed/Continue or equivalent. If a stage cannot safely finish in one turn, preserve a portable durable checkpoint containing the exact residual queue(s), report STAGE X: INCOMPLETE — DURABLE CHECKPOINT PRESERVED, identify exactly what remains, and STOP.

Stage 3A has required substages (3A-0 through 3A-4). Treat those substages as real owner-facing stop boundaries. Evidence classes inside 3A-1 through 3A-3 are research units, not automatic owner-facing stops: bundle multiple small classes that use the same research mode into meaningful safe tranches.

My Proceed/Continue response authorizes only the identified next bounded stage, Stage 3A substage, or unfinished serialized tranche—not all remaining research through RESEARCH_FROZEN.

Preserve accepted prior stages unless later evidence produces a genuine contradiction. Durable artifacts outrank chat memory. A replacement chat should be able to attach the latest checkpoint, verify it, and continue without rediscovering completed work. Historical uncertainty remains valid; unsupported certainty is worse than a researched unknown.

Research may fully resolve shared historical identities, but this independent Research lane must not directly mutate protected-main shared reference registries. Carry any settled new shared identity forward as a resolved proposal for current-main Implementation rebase under docs/shared-reference-authority.md. General permission to mutate repository/research state does not override that boundary.

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

That means exactly what `docs/research-lane-bounded-execution.md` defines: execute the identified next bounded stage and stop again at its required boundary. During Stage 3A, it means execute the identified next substage or serialized unfinished tranche; routine transitions among small evidence classes inside that substage should not require repeated owner relays.

Do not require the owner to restate "Stage X only", a Stage 3A substage name, or re-copy stage instructions at ordinary boundaries. The bounded-execution protocol already defines plain `Proceed` as authorization for the identified next bounded assignment. Longer continuation prompts are reserved for genuine recovery, contradiction, migration, or owner-disposition cases.

After an incomplete stage:

```text
Proceed.
```

means resume only the identified unfinished remainder of that same stage from its portable checkpoint.

## Recovery bootstrap for an existing unfinished Research lane

Use this when a prior chat/session failed or must be replaced but durable research state survives:

```text
We are recovering an existing Research lane for <school> in my College Basketball History project.

Before acting, inspect current protected main and read current AGENTS.md plus docs/research-lane-bounded-execution.md, docs/stage3a-regular-season-site-research.md, and docs/shared-reference-authority.md.

I am attaching the latest durable checkpoint/recovery bundle from the prior lane. Treat verified durable artifacts—not conversational reconstruction—as the controlling continuation state.

Verify the checkpoint ZIP/artifact hash and internal manifest, load the exact serialized residual queue(s), preserve accepted owner dispositions and completed repairs, and resume only the earliest incomplete bounded stage. If that stage is Stage 3A, resume the exact incomplete Stage 3A substage/tranche serialized by the checkpoint; do not reopen completed substages or broaden into another research mode.

Do not restart completed stages. Do not perform open-ended archaeology for hidden/chat-local state. Do not reconstruct completed work from old prose merely because a prior chat said it existed. If the required residual queue is genuinely missing from the attached checkpoint, stop and identify the exact missing artifact/state before doing reconstruction.

Any settled shared-reference proposal remains historically resolved but pending current-main Integration unless current-main evidence creates a genuine contradiction. Do not mutate protected-main shared registries from this Research lane.

Use the repository bounded-stage response contract. Use the largest safely completable bounded tranche; stop at required major stage/substage boundaries and at genuine durability/blocker boundaries, not after every tiny evidence family.

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
