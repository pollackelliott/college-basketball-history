# Stage 3A-0 Local-Only Execution Contract

- **Status:** Controlling Research-lane execution policy
- **Applies to:** every Stage 3A-0 mechanical census / partition / project-evidence harvest
- **Approved:** 2026-09-23 after repeated Virginia Stage 3A-0 runtime failures
- **Purpose:** prevent Stage 3A-0 from expanding into external historical research or source discovery

## 1. Governing rule

> **Stage 3A-0 is local-only, mechanical, and bounded. It performs zero external historical research.**

Stage 3A-0 may read only:

- the verified durable checkpoint / serialized Research state for the target school;
- the checked-out/current protected-main repository;
- known repository paths containing canonical games, game assertions, published school packages, and accepted shared-reference/project evidence already present in the project.

Stage 3A-0 may not:

- search the public web;
- browse institutional athletics sites;
- search newspaper/yearbook/archive sources;
- discover new opponent source families;
- use GitHub/code search as an open-ended source-discovery mechanism;
- inspect external PDFs or media guides not already serialized as accepted project evidence;
- perform opponent-by-opponent historical research;
- adjudicate a historical contradiction that requires new evidence;
- begin HOME chronology research;
- begin NEUTRAL venue research;
- begin row-by-row H/A/N research.

If a local exact-game lookup exposes a contradiction, record and serialize the contradiction for the appropriate later Stage 3A substage. Do not investigate it externally during Stage 3A-0.

## 2. What "published reciprocal lookup" means in Stage 3A-0

The phrase **published reciprocal lookup** means only a structured lookup against project evidence that is already present in the repository or checkpoint.

Examples:

- `data/canonical/games.csv`;
- `data/evidence/game-assertions.csv`;
- already-published school `source-games.csv` files present under the checked-out repository;
- accepted reciprocal artifacts already serialized in the checkpoint;
- other known local project evidence already accepted under repository policy.

It does **not** mean:

- find an opponent's institutional history page;
- search the web for an opponent schedule;
- locate a media guide;
- search GitHub for additional archives or CSV blobs;
- discover a new reciprocal evidence source.

Those activities belong to Stage 3A-1, 3A-2, or 3A-3 when their research responsibility is actually authorized.

## 3. Mechanical execution shape

Stage 3A-0 should normally be completed as one structured local pass:

1. load the exact Stage 1 universe from durable state;
2. mechanically partition regular season versus postseason;
3. derive the row-level H/A/N census;
4. derive HOME / OPPONENT_HOME / NEUTRAL / UNKNOWN work queues;
5. split NEUTRAL into 1996-97+ and 1995-96-and-earlier populations;
6. perform a structured exact-game join against already-present local project evidence;
7. write through only unambiguous accepted same-game evidence;
8. serialize unmatched rows and contradictions without researching them;
9. emit the exact Stage 3A-1 / 3A-2 / 3A-3 queues;
10. stop.

A whole-project reciprocal scan should be implemented as a structured local join/filter over already-present files. Do not manually browse dozens of opponent files one at a time when the same population can be derived mechanically.

If a candidate cannot be established from local project evidence, leave it unresolved for the later research substage. **Lack of a local answer is not permission to open the web.**

## 4. Runtime / convergence rule

Stage 3A-0 should be one of the least expensive Stage 3A substages.

If a Stage 3A-0 turn begins expanding into source discovery, archive browsing, external search, or prolonged opponent-by-opponent inspection, stop that mode immediately and return to the local mechanical contract.

If the local project-evidence pass itself is too large to complete safely in one turn:

- serialize the exact remaining local candidate queue;
- checkpoint;
- resume the same structured local operation later.

Do not convert execution difficulty into broader historical research.

## 5. Recovery rule

When recovering an incomplete Stage 3A-0 from a durable checkpoint:

- verify the checkpoint first;
- preserve every completed census/partition/local-evidence result already serialized;
- resume only the exact unfinished local mechanical queue;
- do not repeat completed project-evidence scans;
- do not search externally to "improve" the checkpoint;
- stop at `STAGE 3A-0: COMPLETE`.

Any work performed after the controlling checkpoint during a failed/stalled chat is non-authoritative unless it was durably serialized and explicitly accepted.

## 6. Completion standard

A complete Stage 3A-0 must report and durably preserve:

- exact Stage 1 total;
- exact regular-season Stage 3A population;
- exact postseason Stage 3B handoff population;
- H/A/N census derived from rows;
- exact HOME / OPPONENT_HOME / NEUTRAL / UNKNOWN queues;
- exact modern versus historical NEUTRAL split;
- accepted same-game local-project evidence written through;
- unmatched local candidates;
- isolated contradictions;
- exact residual queues for Stage 3A-1 through Stage 3A-3.

Then stop:

```text
STAGE 3A-0: COMPLETE
Next bounded assignment: Stage 3A-1 — H/A/N completion
STOPPING AT THE REQUIRED STAGE 3A SUBSTAGE BOUNDARY.
```

## 7. Review rule

Flag a Stage 3A-0 implementation if it:

- invokes public web research;
- searches institutional archives or media guides;
- discovers new external source families;
- uses broad GitHub/code search instead of direct reads/structured joins over known project paths;
- researches venues or H/A/N beyond accepted local evidence;
- manually inspects opponent sources one by one when a structured local join is available;
- treats an unresolved local candidate as permission to research externally;
- continues into Stage 3A-1 without owner authorization.

The intended Stage 3A-0 experience is:

> **checkpoint -> local mechanical join -> exact queues -> stop**
