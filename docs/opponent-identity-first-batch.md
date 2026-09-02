# Opponent Identity Remediation — First Transaction Batch

## Status

This document defines the reviewed first transaction for the legacy Texas A&M stale-key split.
It is a transaction specification, not permission to mutate protected `main`.

The institutional identity decision is:

```text
texas-a-and-m -> texas-a-m
```

The stale key occurs in published Northwestern and Oklahoma source packages. The target
`texas-a-m` key is the authoritative current program identity.

## Survivor rule

The transaction does **not** choose the numerically lowest canonical ID.

For each duplicate pair, preserve the pre-existing canonical row carrying the stale
`texas-a-and-m` identity as the survivor. Those rows predate the Texas A&M onboarding and
were already part of earlier published program histories. The later `texas-a-m` duplicate
is absorbed into that survivor.

The survivor receives the authoritative program key and compatible nonblank enrichment
from the absorbed row. Competing populated values are blockers unless an explicit
reviewed resolution is supplied.

All source assertions from the absorbed row are redirected to the survivor. Literal
source opponent labels, raw source text, and source-side conflicting dates/scores remain
preserved.

## Expected transaction shape

The validated read-only audit found:

- 52 affected stale-key canonical rows;
- 49 exact core-match duplicate groups;
- 2 same-date identity-conflict groups;
- 1 affected row whose duplicate was hidden by a source-date error.

The sealed transaction therefore expects:

- 52 survivor rows;
- 52 absorbed duplicate rows;
- canonical row count reduced by exactly 52;
- source assertion count unchanged;
- all assertions formerly attached to absorbed rows redirected to survivors;
- stale `texas-a-and-m` removed from canonical participants and affected assertion/package normalization;
- 3 new `RESOLVED` discrepancy records for the material exceptional fields below.

## Exceptional reconciliation 1 — Northwestern, 1969-12-30

Canonical survivor:

```text
CBBG-0009910
```

Absorbed duplicate:

```text
CBBG-0066393
```

Canonical result:

- Date: 1969-12-30
- Texas A&M 93, Northwestern 91
- Overtime periods: 1
- Site type: NEUTRAL
- Site city/state: Greenville, SC

Evidence:

- Texas A&M official 1969-70 schedule:
  `https://12thman.com/sports/mens-basketball/schedule/1969-70`
- Texas A&M official Northwestern opponent history:
  `https://12thman.com/sports/mens-basketball/opponent-history/northwestern/79`

Texas A&M explicitly records the 93-91 result as overtime in Greenville, South Carolina.
Northwestern's preserved source assertion omits the overtime marker. Canonical overtime
is therefore `1`; the Northwestern omission remains source evidence and is recorded as a
resolved discrepancy.

No physical venue is invented from city evidence alone.

## Exceptional reconciliation 2 — Oklahoma, 2005-01-18

Canonical survivor:

```text
CBBG-0062880
```

Absorbed duplicate:

```text
CBBG-0067210
```

Canonical result:

- Date: 2005-01-18
- Oklahoma 70, Texas A&M 54
- Texas A&M HOME
- Reed Arena, College Station, TX

Evidence:

- Texas A&M contemporaneous official recap:
  `https://12thman.com/news/2005/1/18/205225598`
- Oklahoma official box score:
  `https://soonersports.com/sports/2005/1/18/Stats_3983`

Both contemporaneous official sources establish Oklahoma 70, Texas A&M 54 at Reed Arena.
Oklahoma's later year-by-year source row records 70-56. That later assertion remains
preserved in Oklahoma `source-games.csv`; it does not control canonical truth. The score
disagreement is recorded as `RESOLVED`.

## Exceptional reconciliation 3 — Oklahoma, 2010-01-19

Canonical survivor:

```text
CBBG-0063008
```

Absorbed duplicate:

```text
CBBG-0067341
```

Canonical result:

- Date: 2010-01-19
- Texas A&M 65, Oklahoma 62
- Texas A&M HOME
- Reed Arena, College Station, TX

Evidence:

- Texas A&M contemporaneous official recap:
  `https://12thman.com/news/2010/1/19/205228753`
- Oklahoma official archive:
  `https://soonersports.com/news/2013/5/20/208793026.aspx`

Oklahoma's official archive and Texas A&M's contemporaneous official recap establish
January 19, 2010. Texas A&M's later year-by-year source row carries January 23. The
source row is not silently rewritten. Instead, its assertion is redirected to the
January 19 survivor and the date disagreement is recorded as `RESOLVED`.

## Apply invariants

The transaction tool must refuse to apply unless all of the following hold:

1. the exact reviewed transaction-plan SHA-256 is supplied;
2. every one of the 52 affected stale-key rows is paired exactly once;
3. every absorbed row is a non-stale counterpart rather than another stale survivor;
4. every competing populated canonical field is either equal or explicitly resolved;
5. the affected school-package rows still match the sealed source-game sets;
6. the discrepancy schema and next IDs are unchanged from the sealed plan;
7. all controlling repository files still match the plan fingerprints;
8. post-apply validation finds no absorbed canonical IDs or stale identity keys;
9. repository validation passes; and
10. any failure restores every touched file byte-for-byte.

## Rehearsal before real mutation

Before any basketball-data write, run the full transaction in a disposable copy of the
repository. The rehearsal must prove:

- blocker-free deterministic plan;
- 52/52 pairing accounting;
- exactly 52 canonical rows absorbed;
- assertion count unchanged;
- exactly 3 new resolved discrepancies;
- literal source labels/raw source text preserved;
- `validate_data.py` passes;
- full unit suite passes;
- generated site data can be rebuilt deterministically;
- the opponent-identity census no longer reports this stale Texas A&M split.

Only after that rehearsal is the real transaction eligible for a separately sealed
mutation/release step under the serialized integration lock.
