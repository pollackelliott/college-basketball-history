# Objective C — owner-editable published-site residual inventory

## Authoritative snapshot

Protected main baseline: `9134540e5beb3c1838d32a25f4b69fca05087cd0`; publication PR #317 is merged and exact
Production JSON was verified before this residual inventory was generated.
These review lists are **not** canonical history patches or new research authorization.
They preserve previously accepted historical judgments unless separately reopened
under existing repository authority.

## Three review worklists (6,660 distinct canonical games)

- `objective-c-home-review.csv`: 789 rows = 768 HOME hard blockers and
  21 additional invalid-marker review cases; 7 of those marker cases also
  have existing accepted HOME venue exceptions and are `HOLD` for a marker
  consistency review **only**, not HOME venue re-research.
- `objective-c-regular-neutral-review.csv`: 5,509 regular-season neutral site
  gaps. The 2 obsolete HOME markers on canonical neutral games are routed here.
- `objective-c-postseason-review.csv`: 364 postseason site gaps. Twelve HOME
  games also have previously accepted researched-unresolved HOME venue status;
  these are explicitly `HOLD` for the postseason-standard interaction review
  **without** nullifying their accepted HOME conclusions.

Exactly 2 other canonical games are present in both HOME and postseason lists.
They must be tracked as a single underlying game when decisions are made.
The complete 2,370-case accepted HOME venue exception inventory is in
`worklist-manifest.json`. Of these, 19 appear for a **different review reason**
(7 marker consistency, 12 postseason standard), with explicit HOLD flags;
none has been automatically reopened for venue research.

## Research/decision rules

- All CSV game facts, dates, site fields and keys represent the protected-main
  snapshot, including any blank dates. Do not infer or replace missing dates.
- Historical regular-season neutral games through 1995-96 are location-first.
  Supported city/state is sufficient under that standard; do not reopen
  building-only archaeology merely to eliminate a blank venue.
- Modern regular-season neutral games retain a strong exact-venue expectation.
- Postseason venue/location requirements remain exhaustive. A HOME accepted
  exception on a postseason game does **not** automatically waive those rules;
  its intersection is flagged for bounded policy/evidence review, not silently
  counted as unresearched or silently erased.
- The NCAA Tournament currently has zero missing-site games.
- The shared conference-tournament guide supplies venue evidence, never H/A/N
  classification by itself.

## Owner-editable fields

`research_disposition`, `source_evidence_url`, `source_evidence_notes`,
`proposed_site_type`, `proposed_venue_id`, `proposed_city`, `proposed_state`,
`owner_decision`, and `owner_notes` are for subsequent explicit review.
Do not pre-populate owner approval or change canonical/archival inputs from
these worklists. The new `accepted_home_exception_overlap` and
`accepted_exception_handling` columns are baseline inventory annotations.
A `HOLD` means **do not reopen** the accepted historical finding automatically.

When protected main changes, reconcile any contemplated changes against
current Git authority. Use the repository's existing Research/Implementation,
owner approval, Preview, and Production-proof safeguards for actual data changes.
