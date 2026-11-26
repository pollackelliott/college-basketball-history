# Expansion Stage 1 venue reconciliation: settled registration and distinct keyed buildings

**Authority boundary:** One bounded generic mechanism approved by the Control
Center for an existing school's `ALL_HISTORY_EXPANSION` Stage 1, as recorded
in [UC Davis issue #722](https://github.com/pollackelliott/college-basketball-history/issues/722).
It is generic code, not a right to change already-published venue identities,
historical meaning or the original Research Freeze. Shared/global updates,
sealed-plan historical decisions and release gates retain their own approvals.

## A. Settled registration-only Research venue supports

A supplemental venue note that says a physical facility has been researched
and **global registration pending current-main rebase** need not repeat the
literal words `historical identity: resolved` if its original frozen row
independently has all of: keyed facility/name/geography; documentary URL;
accepted site-rule; exact-game-set relationship; positive assigned-game count;
and no express unresolved identity, reuse, split or collision statement.

That is a *classification* of existing Research evidence, not a manufactured
historical conclusion. The ordinary Stage 1 current-global exact-key, historical
alias, geography, chronology, other-school local-key and safe new-registration
checks still run. An existing compatible physical venue is reused; a truly new
one receives a newly generated current-main VEN ID only in guarded Phase 0.
The original support, aliases, notes, postseason game relationships and literal
source-game H/A/N remain immutable.

## B. Different physical buildings sharing an historical alias

Schema-v3 `venue-reconciliation.json` may carry
`REGISTER_DISTINCT_KEYED_IDENTITY` **only** when a Control Center/owner
decision already establishes two physically different buildings.

The spec is an exact sidecar, authenticated by SHA-256 transport and bound to:
- original immutable Research ZIP SHA-256 and exact candidate venues.csv hash;
- one original `expansion-venues.csv` source-support ID/entire row/hash, full
  `candidate_row_json`/effective candidate row hash, original key, name,
  locality, site rule, primary venue relationship and source basis;
- exact effective candidate source-games.csv SHA-256 (including any separately
  owner-approved pre-Integration game corrections);
- existing conflicting **current-main** global VEN ID, key, full row hash,
  full name-row population hash, original opened/closed chronology, city/state;
- affirmative independent physical-building separation basis and exact owner/
  Control Center authorization, with original older building known closed
  strictly before the existing newer building opened;
- exact excluded *global-only* alias set, encompassing every same-locality
  name collision; no displayed name conflict, unknown additional physical
  match, arbitrary key replacement or unqualified alias reuse is permitted.

The only permitted new venue key is the original already-keyed Research
identity; a collision with current protected main fails closed. The sidecar
does not supply numeric VEN IDs. Registration allocates one authoritative
next-current-main global ID in the normal guarded Phase 0 transaction.

**No source alias is deleted.** The conflicting literal historical alias is
retained in original frozen evidence and the source-school venues.csv row. It
is deliberately *not registered as a second unqualified global name alias*;
otherwise name-only matching could redirect games between physical buildings.
Existing VEN rows, names, school history, and canonical game assignments must
remain unchanged. Any requested change to the existing global alias, canonicals
or other schools is **not** covered by this exception and requires a new
Control Center shared-reference specification.

## Mandatory replay

The original Freeze is independently validated before Integration Freeze.
The sidecar's source-support row is compared directly to the original
`expansion-venues.csv` inside the immutable ZIP on each Integration Freeze
reconstruction. Disposable Phase 0 preview independently revalidates its
candidate-row/registration/alias hashes and exact sidecar metadata. Guarded
Phase 0 and the fresh verifier reproduce the same Integration Freeze,
effective source semantic snapshot, venue census, global registration and
published-candidate tree against the exact predecessor. Any mismatch is a
STOP, not permission to widen the spec.

The initial implementation must test the real seven-case UC Davis Freeze
population, including its 1921–1937 original HOME venue chronology and
NCAC opponent-host postseason venue relationships. Synthetic positive and
adversarial negative tests are additional, not substitutes for actual
source-transport replay. No Stage 2 or Owner Gate 1 decision is implied.
