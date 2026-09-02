# Opponent Identity Collision Audit

The opponent-remediation planner blocks exact duplicate canonical-game candidates exposed by a program-key replacement. Real repository validation of the initial Texas A&M stale-key repair showed why that is necessary but not sufficient: 52 stale-key canonical games were affected, while only 49 were exact matches under a signature that included score and overtime.

A duplicate representation can disagree on a historical field. For example, one source may record overtime while another omits it. Such a disagreement is a reconciliation problem; it must not cause the two rows to survive as separate real games.

## Read-only command

```bash
python tools/opponent_identity_collision_audit.py /path/to/decisions.csv \
  --output /tmp/opponent-collision-audit.json
```

The audit consumes the same evidence-backed decision file as `opponent_identity_remediation.py plan` and uses its deterministic program-key map. It does not mutate data.

For every affected canonical game with an exact date, the audit groups rows by:

- season;
- exact date;
- program pair after the proposed identity replacement.

It then classifies the group as:

- `EXACT_CORE_MATCH` when oriented scores and overtime agree;
- `SAME_DATE_IDENTITY_CONFLICT` when the mapped program/date identity agrees but score or overtime differs.

The second class is intentionally still a collision candidate. It requires field-level reconciliation rather than preservation as a second canonical game.

The audit also reports canonical differences in score, winner, overtime, site type, designated home team, venue, geography, game type, postseason round, and administrative fields.

## Survivor IDs

The audit reports the numerically oldest `canonical_game_id` as `oldest_id_candidate`, but labels it `REVIEW_CANDIDATE_ONLY`.

This is not automatic authority to delete or renumber anything. The project promises stable canonical IDs. A later transactional remediation must explicitly establish which existing row survives each true duplicate, reattach every source assertion to that survivor, preserve material conflicting evidence through reconciliation/provenance, and verify that no downstream reference is orphaned.

## Unpaired affected rows

`unpaired_affected_game_ids` are affected stale-key canonical rows for which no second row exists on the same mapped program pair and date.

They are not safe to rewrite blindly. Before apply, each must be explained as one of:

1. a genuine single canonical game whose participant key should simply be corrected;
2. a duplicate whose counterpart differs on date precision/date and needs broader reconciliation;
3. an unresolved case that must remain blocked.

## Apply gate

Before a transactional opponent-identity apply can be sealed:

- every affected stale-key canonical game must be accounted for;
- every true duplicate must have one reviewed surviving canonical ID;
- field disagreements must have an explicit canonical/provenance disposition;
- assertion reattachment must be complete;
- no canonical self-game may be created;
- no silent duplicate may remain merely because score/OT/site evidence disagreed;
- the final plan must be fingerprinted and deterministic.
