# Stage 3A-1 Source-Fanout and Convergence Contract

- **Status:** Controlling Research-lane execution policy
- **Applies to:** Stage 3A-1 H/A/N completion
- **Approved:** 2026-09-23 after Virginia Stage 3A-1 exhausted a chat on a 12-row queue without durably resolving a row
- **Purpose:** bound source discovery as well as row count so a small H/A/N queue cannot become an open-ended web-research campaign

## 1. Governing rule

> **A bounded row queue does not authorize unbounded source discovery.**

The Stage 3A-1 row cap controls how many independent historical adjudications may occur in one turn. This document separately controls **how many source paths may be opened for those rows**.

The objective is defensible H/A/N research with efficient convergence, not exhaustive searching of every theoretically available source.

## 2. Required evidence hierarchy

For each coherent Stage 3A-1 evidence class, use the following order:

1. **Already-accepted project evidence**
   - current checkpoint state;
   - current-main canonical/assertion evidence;
   - already-published reciprocal packages already identified by Stage 3A-0;
   - accepted project artifacts already serialized for the lane.

2. **Target-school institutional source family**
   - official schedule/history pages;
   - official media guide/year-by-year history;
   - institutional archive or equivalent first-party source.

3. **Obvious opponent institutional source family**
   - official opponent schedule/history pages;
   - official opponent media guide/year-by-year history;
   - institutional archive or equivalent first-party source.

4. **One coherent authoritative fallback family**
   - only when it can reasonably address multiple rows or a clearly bounded historical class;
   - examples may include one newspaper archive family, one yearbook collection, one tournament/event history, or one recognized archival index.

Do not skip directly to broad web searching because an institutional source is inconvenient.

## 3. Source-fanout ceiling

For an individual row, after already-accepted project evidence:

- normally inspect **no more than one target-school institutional path and one opponent institutional path**;
- a third external path is allowed only when it is a **specific named authoritative source already identified as plausibly decisive**, not a generic search result;
- do not continue opening additional unrelated sites merely because those paths did not resolve the row.

For a coherent multi-row class:

- reuse the same source family across all applicable rows;
- prefer one source capable of resolving several games over separate row-by-row searches;
- do not multiply source paths by row count;
- do not treat every unresolved row as permission to start a new discovery tree.

If the obvious authoritative paths fail, the correct result may be `RESEARCHED_UNRESOLVED`.

## 4. Generic web search is discovery-only

Search engines may be used narrowly to locate a **specific authoritative source family**. Generic search itself is not an evidence class.

Do not continue a Stage 3A-1 investigation through:

- Reddit;
- fan forums;
- mirrors of unknown provenance;
- generic sports aggregators;
- scraped schedule sites;
- unrelated wikis;
- random archive mirrors;
- broad lists of search results;

merely because official/institutional evidence did not resolve the row.

Such sources may occasionally point to an authoritative source, but they are not a reason to prolong the search and are not a preferred evidentiary endpoint for H/A/N.

## 5. Class-first execution

Before opening external sources, define the smallest coherent evidence classes in the queue.

Examples:

- several rows against one opponent;
- several rows from one era covered by one Virginia institutional source;
- several games in one recurring series;
- several contradictions already tied to one published reciprocal package.

Then choose the **fewest coherent source families** likely to resolve the class.

For a homogeneous queue already at or below the 25-row independent-adjudication ceiling, normally process the whole queue in one turn **only if the same small set of source families can support it**.

The <=25 rule is not permission for 25 separate deep web investigations.

## 6. Convergence rule

A row/class is considered proportionately exhausted when:

- already-accepted project evidence has been checked;
- the obvious target-school institutional path has been checked when available;
- the obvious opponent institutional path has been checked when available;
- any one clearly identified high-yield authoritative fallback family has been checked when justified;
- no direct H/A/N support or decisive contradiction has emerged.

At that point:

- preserve the current accepted value if not disproven;
- or mark the row `RESEARCHED_UNRESOLVED` when H/A/N itself remains unsupported;
- serialize the evidence paths attempted;
- move on.

Do not continue searching simply because another possible archive may exist.

## 7. Runtime failure signal

Stage 3A-1 should not consume a long-running chat merely by expanding source fanout.

If a small queue is still opening unrelated websites after the required hierarchy has been attempted, stop source discovery immediately and converge the affected rows under this contract.

If execution/context risk becomes material before accepted findings are written through:

- write through supported resolutions first;
- serialize the exact unresolved remainder and attempted source families;
- checkpoint;
- stop.

Do not spend the remaining context budget on another discovery branch.

## 8. Recovery rule

When recovering Stage 3A-1 from a durable checkpoint:

- load the exact unresolved queue;
- preserve already-attempted source-family dispositions when serialized;
- do not repeat failed source paths without new evidence;
- do not broaden into generic web discovery merely because the prior turn failed;
- resume from the next unexhausted authoritative source family, if one exists;
- otherwise terminalize the row/class proportionately.

## 9. Completion standard

Stage 3A-1 completes when every row in its H/A/N residual queue is either:

- resolved with accepted evidence;
- preserved against a contradiction with an explicit evidentiary basis; or
- explicitly `RESEARCHED_UNRESOLVED` after the bounded source hierarchy is exhausted.

The completion artifact must preserve:

- exact row-level H/A/N state;
- evidence/provenance for accepted changes;
- contradiction dispositions;
- researched-unresolved rows;
- exact downstream Stage 3A-2 / 3A-3 implications.

Then stop at the required substage boundary.

## 10. Review rule

Flag a Stage 3A-1 execution if it:

- opens broad web search before defining an evidence class/source plan;
- treats a <=25-row queue as permission for <=25 separate deep searches;
- opens many unrelated domains for one row;
- relies on Reddit, forums, mirrors, aggregators, or generic wiki/search results as a substitute for obvious institutional evidence;
- keeps searching after target/opponent institutional paths and one justified authoritative fallback have failed;
- repeats already-exhausted source paths after recovery;
- delays durable write-through until after extensive source discovery;
- refuses to use `RESEARCHED_UNRESOLVED` merely because another theoretical source might exist.

The intended Stage 3A-1 experience is:

> **classify queue -> use a small authoritative source hierarchy -> resolve what is supportable -> terminalize exhausted survivors -> write through -> stop**
