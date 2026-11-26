# Owner-approved pre-Integration expansion correction (exceptional)

**Status:** fail-closed generic exception to the usual post-Research-Freeze historical
authority boundary. Applies only to an already-published school's
ALL_HISTORY_EXPANSION Implementation when an **exact previously approved**
historical correction is required to make Stage 1 / Integration Freeze possible.
This is **not** authority to reopen Research, mutate the original Freeze ZIP, skip
identity review, amend other schools, or approve the remaining Stage 2 Gate 1 map.

## 1. Authority and transport

The owner must have explicitly approved the exact source-game identities and
original-to-effective historical field deltas; the repository Control Center
must have authorized their exceptional pre-Integration treatment. The historical
decision receipt is a separate immutable JSON artifact, with its exact SHA-256,
original source-row hashes, Research-base SHA, original Freeze SHA-256, owner
approval statement and exact field changes. The original Research Freeze
remains byte-identical.

A subsequent *fresh* repository-owned expansion startup intent may include:

```json
{
  "owner_correction": {
    "authority_kind": "CONTROL_CENTER_OWNER_APPROVED_PREINTEGRATION_V1",
    "approval_issue_url": "https://github.com/OWNER/REPO/issues/NUMBER",
    "school_key": "target-school",
    "freeze_sha256": "<original-immutable-zip-sha256>",
    "sha256": "<actual-owner-approval-artifact-sha256>",
    "owner_checkpoint_sha256": "<same-approved-artifact-sha256>",
    "path": ".remote-implementation/transports/target-school/approval.json",
    "approved_source_game_ids": ["EXACT-ID-1", "EXACT-ID-2"]
  }
}
```

The artifact bytes MUST be in the immutable parent transport commit named by
the startup intent. The startup coordinator reads them by `git show`, checks
their SHA-256 and the exact source ID set, and independently runs the unchanged
Research Freeze validator before projecting the corrections. The optional
`owner_correction` field is otherwise absent; no empty or unauthenticated
overlay is accepted. The approved artifact's owner statement must be explicit,
and it must separately deny implied full Gate 1 / Gate 2 approval.

## 2. Exact projection and provenance

`tools/expansion_preintegration_owner_corrections.py` accepts only:

- source_game_id rows *already present* in authenticated frozen supplemental
  source rows, exactly matching the declared immutable approved ID set;
- `game_date`, `team_score`, `opponent_score`, `curated_site_type`,
  `curated_venue_name`, `city`, and `state`;
- exact original per-row hash and pre-change value, changed after-value, and
  independently recomputed full effective-row hash.

It rejects all other columns. In particular, it cannot change `raw_text`,
`source_opponent_label`, `normalized_opponent_key`, `source_site_candidate`,
`source_page`, `source_game_id`, `played_result`, game type, or other
nonapproved history. Missing/extra source IDs, conflicting fields, stale
original Freeze/base, tampered artifact bytes, unbound approval, missing/incorrect
original row hashes, or mismatched post-projection hashes fail closed.

Only an in-memory/temporary candidate-only projection is modified. Frozen
source evidence, inherited baselines and publication registries are untouched.

## 3. Deterministic replay and downstream authority

1. Startup runs the **original** Freeze validator, applies only the approved
   effective rows during Stage 1, and requires two byte-identical Stage 1 runs.
   The report and independent proof include the same correction receipt.
2. Integration Freeze reproduces the effective Stage 1 from original immutable
   Freeze plus the same artifact, checks the independent proof, and binds the
   exact correction SHA, receipt, effective package file hashes, and effective
   source semantic snapshot. The sidecar is retained in the frozen packet.
3. Guarded `EXPANSION_PHASE0` re-materializes the same original Freeze and
   correction artifact, replays Integration Freeze and the disposable preview,
   rejects any changed hash/receipt, and binds the correction sidecar/receipt,
   Integration Freeze and semantic snapshot into write-ahead/successor records.
4. Independent fresh verification reads the original request and write-ahead
   from Git, checks the correction sidecar hash and receipt, and replays the
   same effective candidate and exact published tree. A different source
   representation, approval artifact, or semantic snapshot fails closed.
5. The corrected effective source package becomes ordinary
   `INTEGRATION_FROZEN` authority. The existing Stage 2 semantic-drift guard,
   Stage 2 current-main validation, full `OWNER_GATE_1_READY` packet,
   explicit *separate* full Gate 1 approval, cryptographic seal, sealed apply,
   Preview, explicit Gate 2, exact merge, and Production proof remain mandatory.

No correction sidecar can be submitted as a normal `STAGE2_GATE1_FILL`
approval. The earlier, narrow source correction is an immutable historical
authority input to Stage 1; it approves **nothing else**.

## 4. Safety and operations

- All source, reference, public-data, canonical, or other-school tracked mutations
  remain forbidden in the tooling PR.
- The old failed startup remains consumed as a diagnostic, and neither its
  startup ID nor Phase 0 request ID can be replayed.
- After the tooling PR passes exact-head CI and is merged, validate the **actual**
  approved artifact against the **actual** original Freeze, stage its exact
  original bytes in a reachable Git commit, use fresh startup identifiers,
  and require the permanent current-main acceptance, Stage 1 and Integration
  Freeze checks before guarded Phase 0.
- Any additional blocker or new historical question is a STOP, not permission
  to widen the owner approval or manufacture more corrections.

This narrow exception was approved as a one-scope control remedy. Its general
mechanism remains school-agnostic, but an operator must independently secure
owner/Control Center historical authority for any other use.
