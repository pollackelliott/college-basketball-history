# Published Opponent Identity Census

`tools/published_opponent_identity_census.py` is the permanent read-only scoreboard for opponent-identity debt on published program packages.

It does **not** mutate canonical games, source assertions, school source packages, global program references, or generated site data.

Its purpose is to answer a different question from the site-completeness census:

> Are published programs still carrying opponent identities that should probably resolve to an existing current program, or that deserve explicit historical-name review before being treated as durable non-D1 identities?

## Why this exists

The project accumulated opponent-normalization debt while onboarding standards were still evolving. Most examples are low consequence historical labels, but some can materially fragment a real series.

A high-priority example is a published program whose `opponents.csv` stores five games against `texas-a-and-m` / `Texas A&M` while the current global registry now uses `texas-a-m` for the published Texas A&M program. That creates a false split between a real published opponent and a supposed non-D1 identity.

Other cases are less mechanically obvious. A modern label such as `TAMU-COMMERCE` may represent a renamed current program, but the census must not auto-merge it merely from string similarity. Historical aliases and institution-name changes still require evidence.

## Data scanned

The census reads:

- `data/reference/programs.csv`;
- `schools/<published-program>/opponents.csv` for every `public_page_enabled=yes` program.

It compares each published source package with:

- current-D1 global program keys;
- current global program/display names;
- aliases that another published package already resolves to a current-D1 program;
- the broader inventory of identities published packages currently treat as non-D1/non-current.

## Priority classes

### P0 — published identity split

A stored opponent identity conflicts with one exact current program identity and that current program is already published.

This is the highest-priority class because it can split one real published-vs-published series into two opponent records.

Typical signal:

- canonical/source name exactly normalizes to one current published program;
- stored opponent key is different.

P0 is a review trigger, not authorization to mutate blindly. Game-level identity still must reconcile before repair.

### P1 — current-D1 identity/flag debt

Examples include:

- the stored canonical key is already a current-D1 registry key, but the school package still marks it non-D1/blank;
- an exact canonical/source name uniquely matches a current-D1 program under a different stored key.

These are normally strong normalization candidates, but historical evidence still controls.

### P2 — cross-package alias evidence

Another published package already resolves the same normalized source/canonical label to one current-D1 program, while this package stores a different key.

This is useful reciprocal normalization evidence, but it is intentionally weaker than an exact global current-name match. Ambiguous aliases are ignored.

### P3 — modern non-D1 review

A published package carries a non-current identity into the 2000s or later without a current-D1 registry match.

This is deliberately broad. It can include perfectly legitimate Division II/III/NAIA opponents as well as renamed/reclassified current programs.

P3 therefore means **research this identity**, not **merge this identity**.

## Full non-D1 identity inventory

The machine-readable report also includes every opponent identity that published packages currently treat as non-D1/non-current, aggregated by canonical opponent key.

For each identity it reports:

- canonical names;
- source labels;
- published source programs using it;
- total games represented;
- first/last seasons;
- package-row count.

This inventory is the denominator for slower historical cleanup. Genuine clubs, YMCAs, military teams, industrial teams, small colleges, and defunct institutions may remain exactly as they are after review.

The objective is not to eliminate non-D1 opponents. It is to eliminate **false non-D1 identities** and accidental duplicate identities.

## Safety principles

The census never decides that two schools are the same merely because their names look similar.

Specifically:

- exact current-name matches are review triggers, not automatic mutations;
- cross-package aliases are used only when they resolve uniquely to one current-D1 key;
- ambiguous aliases are ignored;
- modern non-D1 rows are surfaced for research but receive no automatic suggested key;
- historical institutional renames require authoritative evidence;
- game-level identity must still reconcile on season/date/score/site/context before canonical series repair;
- one real game must remain one canonical game.

## Usage

Text summary:

```bash
python tools/published_opponent_identity_census.py
```

Complete machine-readable report:

```bash
python tools/published_opponent_identity_census.py --json
```

Increase/decrease displayed text examples without changing the machine-readable denominator:

```bash
python tools/published_opponent_identity_census.py --examples 50
```

## Remediation order

Recommended order after a census run:

1. P0 published-vs-published identity splits;
2. P1 exact current-D1 key/name/flag debt;
3. P2 cross-package alias splits with strong reciprocal evidence;
4. P3 modern non-D1 rows, researched individually;
5. lower-priority historical non-D1 inventory cleanup.

Do not combine this work with site/location remediation merely because both are legacy debt. They may share the serialized repository mutation lock, but opponent identity and physical-site truth are separate semantic problems and should have separately sealed/reviewed remediation batches.

## Future program-name registry

The census is intentionally conservative because the repository currently has a global physical-venue alias layer but no equivalent date-aware global program-name/alias registry.

A future `program-names.csv` or equivalent should be considered for:

- historical official institution names;
- former athletic-brand names;
- accepted source abbreviations;
- effective date ranges where useful;
- canonical current `program_key` linkage.

That registry should be built from researched evidence, not generated automatically from this census.
