# Complete Institutional Research Protocol

- **Status:** Controlling for ordinary Research of unpublished current-D1 programs
- **Applies to:** new ordinary Research lanes and explicitly retrofitted pre-protocol ordinary Research lanes
- **Does not replace:** `docs/all-history-expansion-lifecycle.md` for already-published legacy programs, top-level classification authority, ordinary historical-quality standards, or serialized Implementation
- **Research terminal state:** ordinary `RESEARCH_FROZEN`

## 1. Core separation

For an unpublished school, the ordinary Research publication universe is the complete recognized institutional varsity history from researched program inception through the required completed-season cutoff.

`data/reference/program-top-level-scope.csv` remains the authority for accepted top-level / Division-I-equivalent classification. It does **not** clip the ordinary Research game universe and it does not establish institutional inception.

A school may therefore have, at the same time:

- institutional inception: `1958-59`;
- complete ordinary Research universe: `1958-59+`; and
- accepted top-level scope: `1969-70+`.

Those are different facts.

## 2. New ordinary Research lanes

At Stage 1 startup:

1. authenticate current protected main and preserve the immutable `research_base_sha`;
2. read the accepted top-level scope as classification authority;
3. establish actual institutional varsity inception from authoritative target-school evidence;
4. distinguish `PRE_INCEPTION`, active varsity, dormant/no-team, and completed-season coverage;
5. build the competitive-game universe across every active varsity season from inception through the required completed-season cutoff;
6. exclude exhibitions and other noncompetitive events under ordinary policy.

Games outside accepted top-level intervals remain part of the target school's institutional Research package. They do not thereby become top-level games.

Top-level accomplishment and tournament semantics remain governed by the accepted top-level intervals. Outside those intervals, publication conference classification uses the repository's synthetic `Non-D1` representation unless ordinary Research has a separately useful literal conference fact. A genuine lower-level postseason game ordinarily uses `POSTSEASON`, not the top-level `CONFERENCE_TOURNAMENT` taxonomy.

## 3. Durable institutional-scope authority

A new complete-institutional lane, or a pre-protocol lane explicitly converted under this contract, must durably serialize:

`stage4-authoring/institutional-scope.json`

with:

- `schema_version = 1`;
- `kind = COMPLETE_INSTITUTIONAL_RESEARCH_SCOPE_V1`;
- exact `school_key`;
- immutable `research_base_sha`;
- researched `program_inception_season`;
- exact accepted `top_level_scope`;
- `publication_universe = INCEPTION_THROUGH_PRESENT`;
- one `transition_mode`: `NEW_LANE`, `IN_PROGRESS_RETROFIT`, or `FROZEN_SUCCESSOR`;
- `preservation_rule = PRESERVE_ACCEPTED_PARENT_WORK_EXCEPT_GENUINE_CONTRADICTION`.

For either retrofit mode, also preserve the exact SHA-256 of the parent checkpoint or Freeze as `parent_artifact_sha256`.

This file is durable Research authority, not a seventh final package file. It is carried byte-for-byte with the Stage 4 authoring capsule and Stage 4 renders it into the ordinary six-file package notes/source notes.

## 4. In-progress pre-protocol retrofit

Do **not** restart a healthy Research lane merely because the old protocol clipped its universe to top-level scope.

Authenticate the latest portable checkpoint, keep the same lane and immutable `research_base_sha`, create the institutional-scope authority above, and identify the earliest accepted stage materially affected by the omitted institutional seasons.

The ordinary shape is:

1. preserve all accepted parent rows and stage conclusions that remain valid;
2. extend Stage 1 with only the omitted institutional season/game population;
3. reconcile duplicate/same-game obligations between new rows and the preserved parent universe;
4. run Stage 2 opponent-identity work for newly added labels/rows and any preserved identity directly implicated by them;
5. run Stage 3 site/H-A-N/postseason work for newly added rows and only the preserved rows directly affected by a genuine contradiction or shared same-game fact;
6. refresh derived authoring summaries over the final combined population;
7. continue through ordinary Stage 4, NON_D1 scan, Stage 6 and `RESEARCH_FROZEN`.

Scope expansion alone is not a genuine contradiction and does not authorize broad reopening of accepted Stage 1-3 conclusions.

## 5. Frozen pre-protocol successor

A pre-protocol `RESEARCH_FROZEN` artifact is never rewritten or declared invalid merely because complete-institutional scope was adopted later.

Authenticate and preserve that Freeze as immutable parent evidence. Start a successor Research extension under the same historical lane identity, bind `institutional-scope.json` to the exact parent Freeze SHA-256, research the omitted institutional population, and produce a new complete ordinary `RESEARCH_FROZEN` artifact.

The successor Freeze becomes the ordinary Implementation input. The parent Freeze remains durable provenance.

This is **not** `ALL_HISTORY_EXPANSION`: the school is still unpublished and later uses normal original-school Implementation.

## 6. INCEPTION+ pre-protocol lanes

When a pre-protocol lane already used a genuine `INCEPTION+` game universe from institutional inception, no scope retrofit is required merely for symmetry.

Continue from the latest accepted checkpoint under current Research standards. Do not manufacture a scope-extension cycle.

## 7. When restart is justified

Salvage is the default. A restart from Stage 1 is justified only when the authenticated durable state cannot safely distinguish preserved accepted work from the obsolete scope boundary—for example:

- the checkpoint is not portable enough to recover the actual row-level universe/residuals;
- omitted and retained rows were destructively co-mingled so that exact accepted parent authority cannot be recovered;
- later-stage artifacts cannot be tied back to stable game identities after the universe extension; or
- a genuine historical contradiction invalidates the prior game universe broadly.

If restart is necessary, stop and report the exact mechanical/historical reason. Do not use “new protocol” by itself as the reason.

## 8. Implementation boundary

A complete-institutional retrofit for an unpublished school still ends in ordinary `RESEARCH_FROZEN` and later follows normal original-school serialized Implementation.

Do not use `EXPANSION_RESEARCH_FROZEN`, Expansion Integration Freeze, `EXPANSION_PHASE0`, or another published-legacy expansion operation.

The ordinary Implementation must eventually project the researched institutional inception and complete coverage while preserving the separately accepted top-level scope. That Implementation behavior is a later serialized-integration concern and is not mutation authority granted by this Research contract.
