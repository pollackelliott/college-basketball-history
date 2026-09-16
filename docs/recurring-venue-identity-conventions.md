# Recurring Venue Identity Conventions

- **Status:** Durable project convention for recurring venue-identity/locality decisions
- **Applies to:** Research package construction and current-main rebase, Implementation Stage 2 adversarial review, reconciliation, and publication metadata
- **Purpose:** Prevent repeated owner review of venue questions whose answer is stable across schools.

## Principle

These conventions are reusable project knowledge, not school-specific historical adjudications. Once the physical venue is identified, future schools should apply the established physical identity/locality mechanically unless game-specific evidence creates a genuine contradiction.

Source truth and canonical/registry truth may legitimately differ. Preserve the source's literal venue/locality evidence in the source assertion. The canonical game and global venue registry should use the project's established physical venue identity and physical locality.

## Madison Square Garden

`Madison Square Garden` is not one physical venue. The project must distinguish the different buildings rather than treating the shared name as one timeless arena.

### Existing global identities

- `madison-square-garden-1925` / `VEN-000123` = Madison Square Garden III, Eighth Avenue between 49th and 50th Streets, Manhattan. Current registry interval: 1925–1968.
- `madison-square-garden-1968` / `VEN-000124` = Madison Square Garden IV/current Garden, Pennsylvania Plaza / between 31st and 33rd Streets and Seventh and Eighth Avenues, Manhattan. Current registry start: 1968-02-11.

The two are distinct physical buildings and must never be merged merely because both are called `Madison Square Garden`.

### Assignment rule

1. Identify the game date and any event-specific venue/location evidence.
2. For games clearly in the MSG III era, use `madison-square-garden-1925`.
3. For games clearly in the current-Garden era, use `madison-square-garden-1968`.
4. Do **not** use a date-only shortcut for the February 1968 transition. The current Garden opened on 1968-02-11 while MSG III remained in use through 1968-02-13. For a game/event in that overlap, use event-specific evidence for the physical building.
5. If a pre-1925 college-basketball game is identified only as `Madison Square Garden`, do not force it into either existing key. Research which earlier Garden building hosted the event and create/reuse a distinct physical identity as appropriate.

Useful historical anchors:

- Madison Square Garden I and II occupied the Madison Avenue/26th Street site before 1925.
- MSG III opened in 1925 at Eighth Avenue between 49th and 50th Streets and operated through February 1968.
- MSG IV/current Garden opened on 1968-02-11 at Pennsylvania Plaza.

Primary/authoritative evidence used for this convention includes the National Park Service history of MSG III, Madison Square Garden's current-complex history, the Madison Square Park Conservancy history of the earlier Gardens, and the New York Knicks historical media guide for the 1968 transition.

## Paradise, Nevada and canonical Las Vegas normalization

For project-facing canonical geography, physical venues in Paradise, Nevada are normalized to **Las Vegas, Nevada**. This is a deliberate project display convention; it does not assert that the unincorporated town of Paradise is part of the incorporated City of Las Vegas.

Source truth and canonical/registry truth may legitimately differ. Preserve the source's literal venue/locality evidence in source assertions and raw/source-label fields. Do not rewrite a literal source merely because the project's normalized canonical display geography differs.

### Canonical rule

When a resolved physical venue is in Paradise:

- global venue registry city = `Las Vegas`;
- canonical game site city = `Las Vegas` when geography is derived from that resolved venue;
- Research packages should use `Las Vegas` in normalized/resolved venue and site geography once the physical venue identity is established;
- Implementation/reconciliation should carry that same `Las Vegas` canonical normalization into the global venue registry and canonical games;
- preserve literal `Paradise` or `Las Vegas` source wording separately when that is what the school, event, or archival source reports.

The project therefore treats `Las Vegas, NV` as the canonical public/normalized locality for these Paradise physical venues while retaining source provenance separately.

### Established recurring examples

- `MGM Grand Garden Arena` / `VEN-000133` = canonical **Las Vegas, NV**.
- `Michelob ULTRA Arena` / `VEN-000135` = canonical **Las Vegas, NV**.
- `T-Mobile Arena` / `VEN-000201` = canonical **Las Vegas, NV**.
- `Orleans Arena` / `VEN-000356` = canonical **Las Vegas, NV**.
- `Thomas & Mack Center` / `VEN-000377` = canonical **Las Vegas, NV**.

This is not a blanket instruction to collapse unrelated Nevada localities into Las Vegas. It applies when the physical venue identity has been established as a Paradise venue covered by this convention. Literal source geography remains evidence and must not be rewritten simply to match the canonical display normalization.

## Workflow consequence

Future Research/Implementation lanes should not return these recurring questions to the owner merely because a school source uses the ambiguous `Madison Square Garden` label or `Las Vegas` postal shorthand.

They should:

1. resolve the physical venue using the rules above;
2. reuse the existing global venue key when the identity is established;
3. preserve literal source wording separately;
4. escalate only if the game falls in a genuine MSG transition ambiguity, identifies an earlier unregistered Garden, or evidence materially contradicts the established venue identity or this canonical Las Vegas normalization rule.
