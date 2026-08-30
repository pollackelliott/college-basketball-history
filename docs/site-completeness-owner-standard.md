# Published Site Completeness Owner Standard

This document records the owner policy for venue, geography, and H/A/N completeness for published programs.

## Governing publication standard

### 1. Published-team home games

Every in-scope home game for a published program should have:

- a canonical venue identity; and
- complete canonical city/state geography.

This is a publication requirement, not merely a research-accounting requirement. A broad historical hole such as an entire pre-arena era is incomplete research, not an acceptable permanent unknown.

There is one narrow exception: when exhaustive historical research establishes the HOME classification and city/state but the surviving record does not support a specific physical venue identity, the venue may remain blank under the dedicated `RESEARCHED_UNRESOLVED_HOME_VENUE` policy. This exception may waive only the venue field; HOME city/state remain mandatory. It must be machine-visible, supported by a substantive research basis, survive reciprocal-evidence review, and remain explicitly visible in canonical/public reporting rather than being treated as ordinary completeness.

The detailed requirements are in `docs/home-venue-research-unresolved-policy.md`.

`RESEARCHED_PARTIAL` and ordinary `RESEARCHED_UNRESOLVED` never waive a published program's own home-site requirement.

Research lanes must therefore build and use the program's home-venue chronology, including predecessor facilities, arena transitions, alternate home sites, temporary sites, and known one-off home venues before invoking the historical-unrecoverable exception.

### 2. Published-team away games

A published program's away game may lack venue/geography when the home opponent is not yet published. This is expected reciprocal debt: the missing site information should be filled when that opponent is researched and published.

If the home opponent is already published, the away game should inherit the published home program's established venue/geography. A blank canonical site in that situation is propagation/reconciliation debt and must not be silently accepted. A legitimate researched-unresolved HOME venue exception on the published home program may propagate as the same explicit venue unknown to reciprocal public views.

### 3. Published-team neutral games

Neutral-site games should have location information whenever it can be established safely. Venue identity is also desirable and should be researched where practical.

For neutral games between two published programs, both schools' research/evidence are available. Missing neutral geography therefore receives heightened scrutiny: available source/reciprocal location evidence must be propagated, and if city/state still cannot be established the unresolved state must be explicit and supported by targeted review of both published source packages.

NCAA Tournament venue and geography remain strictly mandatory under the existing NCAA completeness rule.

## Priority order for retroactive remediation

1. Published-program home venue/location completeness, with only rigorously documented historical-unrecoverable venue exceptions remaining.
2. Reciprocal propagation for away games whose home opponent is already published.
3. Neutral-site city/state completion, prioritizing published-vs-published games and postseason.
4. Neutral venue completion where support is available.
5. Remaining H/A/N and identity/reference cleanup.

## Release interpretation

A Preview visual-QA gate is not satisfied merely because a remediation batch improved some rows. The owner may withhold approval when the published program still exhibits obvious chronology holes or silent site debt under this standard.

The intended end state is not unsupported certainty. The intended end state is complete use of the project's known venue histories and reciprocal research, with true residual unknowns confined to places where the historical record genuinely does not support stronger detail and those unknowns are explicitly documented.
