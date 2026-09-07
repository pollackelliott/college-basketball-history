# Implementation Lane Bootstrap Template

Use this as the compact opening handoff for a **new serialized school Implementation lane** after `docs/implementation-lane-bounded-execution.md` is present on protected `main`.

The repository documents are the durable instructions. Do not paste the full implementation manual into every new chat.

## New-school bootstrap

```text
We are continuing my College Basketball History project.

Repository:
https://github.com/pollackelliott/college-basketball-history

This chat is the ONE ACTIVE SERIALIZED IMPLEMENTATION LANE for <school>. It is not a Research lane.

Before acting, inspect actual protected main and current repository/onboarding state. Read current AGENTS.md plus docs/implementation-lane-bounded-execution.md and the implementation policies they reference. Repository policy controls over copied handoff wording.

The incoming portfolio is RESEARCH_FROZEN. Verify its immutable ZIP/hash and status card before using it.

Use the bounded Implementation protocol exactly. Work on only the currently authorized implementation stage in each turn. At an ordinary completed stage boundary, report IMPLEMENTATION STAGE X: COMPLETE, identify the next bounded stage, and STOP. Do not begin the next stage until I respond with Proceed/Continue or equivalent.

My Proceed/Continue response authorizes only the identified next bounded implementation stage or unfinished remainder. It never substitutes for Owner Gate 1 historical decisions or exact Preview approval.

If a stage cannot safely finish in one turn, preserve the durable repository/onboarding checkpoint, report IMPLEMENTATION STAGE X: INCOMPLETE — DURABLE CHECKPOINT PRESERVED, identify exactly what remains, and STOP.

Minimize my Codespace copy/paste work. When my Codespace is required, batch deterministic work into the smallest safe phase-sized operation, follow docs/codespace-terminal-safety.md, and request only compact diagnostic output.

INCOMING SCHOOL: <school>
RESEARCH_FROZEN ZIP SHA-256: <sha256>
RESEARCH STATUS / SPECIAL NOTES:
<short status card or package location>

Begin Implementation Stage 1 only.
```

## Normal owner continuation

After an ordinary completed implementation stage:

```text
Proceed.
```

means execute only the identified next bounded stage and stop again.

After an incomplete stage, the same response means resume only the identified unfinished remainder of that stage.

At **Owner Gate 1**, the owner must actually supply/approve the historical dispositions. A generic `Proceed` is not enough unless the exact decision packet has already been clearly approved.

At **Owner Gate 2**, the owner must personally inspect and explicitly approve the exact Preview tied to the exact PR-head SHA. `Proceed` is never a substitute for Preview approval.

## Recovery bootstrap

Use this when an Implementation chat fails or must be replaced:

```text
We are recovering the serialized Implementation lane for <school> in my College Basketball History project.

Before acting, inspect actual protected main, Git/GitHub state, the onboarding branch, tracked worktree, .onboarding/<school>/ artifacts, existing PR/release state, and exact hashes/fingerprints. Read current AGENTS.md plus docs/implementation-lane-bounded-execution.md.

Do not restart the school or replay completed implementation stages merely because the previous chat failed. Reconstruct the earliest incomplete bounded stage from durable state and resume only that stage. Preserve already-settled owner decisions unless actual substantive inputs changed.

LAST KNOWN RECOVERY CAPSULE:
<insert compact implementation recovery state>

Resume only the earliest incomplete implementation stage.
```

## What does not belong in the bootstrap

Do not re-copy the full rules for:

- current-main rebase;
- venue/opponent shared-reference reconciliation;
- Phase 0;
- Gate 1 decision dispositions;
- pre-seal rehearsal;
- carry-forward;
- transactional apply;
- site-completeness gates;
- terminal safety;
- release preparation;
- Preview approval;
- Production proof.

Those rules belong in the version-controlled repository documents. The bootstrap should contain only the school identity, incoming immutable research artifact/hash, any truly school-specific implementation note, and the instruction to begin Stage 1.
