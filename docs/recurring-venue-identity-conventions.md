# Recurring Venue Identity Conventions

- **Status:** Durable project convention for recurring venue-identity/locality decisions
- **Applies to:** Research current-main rebase, Implementation Stage 2 adversarial review, reconciliation, and publication metadata
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

## Paradise, Nevada versus Las Vegas mailing geography

For physical venue identity, the project uses the actual municipality/unincorporated town of the venue, not merely the postal city printed in a mailing address or an event source.

A Las Vegas postal address therefore does **not** establish that a venue is physically inside the incorporated City of Las Vegas.

Clark County's Assessor identifies major Strip parcels such as MGM Grand and T-Mobile Arena as located in the unincorporated town of **Paradise, Nevada** even though their mailing addresses say `Las Vegas, NV`.

### Canonical rule

When the venue is physically in Paradise:

- global venue registry city = `Paradise`;
- canonical game site city = `Paradise` when canonical geography is derived from that physical venue;
- preserve `Las Vegas` in the source assertion when that is what the school/event source literally reports;
- do not classify the source/canonical difference as information loss merely because source mailing/event geography says `Las Vegas` and the registry says `Paradise`.

The physical-jurisdiction convention outranks postal-city shorthand for canonical/registry geography.

### Established recurring examples

- `MGM Grand Garden Arena` / `VEN-000133` = **Paradise, NV**. Clark County Assessor parcel 162-21-414-001, location address 3799 S Las Vegas Blvd, identifies `City/Unincorporated Town: PARADISE`.
- `T-Mobile Arena` / `VEN-000201` = **Paradise, NV**. Clark County Assessor parcel 162-20-810-003, location address 3780 S Las Vegas Blvd, identifies `City/Unincorporated Town: PARADISE`.
- `Michelob ULTRA Arena` at Mandalay Bay should follow the same physical-jurisdiction rule: **Paradise, NV**, despite the property's Las Vegas postal address. The existing registry should be corrected through an ordinary global-reference cleanup if it still says `Las Vegas`.
- UNLV-area venues such as Thomas & Mack Center should likewise use **Paradise, NV** when Clark County jurisdiction evidence establishes Paradise; do not infer from the `Las Vegas` postal city alone.

This is not a blanket rule that every venue marketed as being in `Las Vegas` is in Paradise. Downtown Las Vegas and other incorporated-city venues remain `Las Vegas`. Determine the actual physical jurisdiction once, then reuse the established global venue identity thereafter.

## Workflow consequence

Future Research/Implementation lanes should not return these recurring questions to the owner merely because a school source uses the ambiguous `Madison Square Garden` label or `Las Vegas` postal shorthand.

They should:

1. resolve the physical venue using the rules above;
2. reuse the existing global venue key when the identity is established;
3. preserve literal source wording separately;
4. escalate only if the game falls in a genuine MSG transition ambiguity, identifies an earlier unregistered Garden, or evidence materially contradicts the established physical-jurisdiction convention.
