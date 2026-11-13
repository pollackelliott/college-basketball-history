# Arizona State Stage 1 parent — current generic accounting compatibility

**Scope:** narrow mechanical parent-format adapter for one already owner-approved Arizona State `ALL_HISTORY_EXPANSION` Stage 1 Research case. The repository's existing generic `tools/research_stage1_early_accounting_closeout.py` remains the **only** auditor, closeout writer, and independent verifier. This change adds no parallel school-specific closeout engine, authority registry schema, historical rule, or shared basketball dataset.

## Exact inputs

- Immutable Research base: `df73675852ec5a43dfac50da0ee06d8bcabf8832`
- Source file at that Git object: `schools/arizona-state/source-games.csv`; exact Git blob `bb2e5ddb63e2caab96c2f3eb33d4d231bf75c875`
- Research recovery checkpoint 0018 exact SHA-256 `f3391cca078e25f4e3a737b632026aa5636d0723519b3b95805688c7dbe6e10d`
- Original checkpoint transport SHA-256 `3118188075b1ce4f028bf25653f979c64e83a63714c674344c26b7e16208f63f`
- Owner historical decision provenance: https://github.com/pollackelliott/college-basketball-history/issues/582 (record of pre-existing conversation authorization, not a new owner signature)

## Usage

Use the original attached checkpoint, never a synthetic stand-in, and the exact Git-source bytes from the pinned Research base:

```sh
python tools/research_stage1_expansion_parent.py \
  arizona-state-stage1-mechanical-recovery-0018.zip \
  asu-source-games.csv \
  --checkpoint-sha f3391cca078e25f4e3a737b632026aa5636d0723519b3b95805688c7dbe6e10d \
  --source-blob bb2e5ddb63e2caab96c2f3eb33d4d231bf75c875 \
  --output asu-stage1-parent.zip
```

The parent remains `stage1_complete:false`, and all original recovery evidence is embedded unchanged. The materializer requires source-literal and distinct-identity checking for ten 1920–21 candidates; it never includes the separate ASC W42–13 assertion, never alters inherited NAU W45–13, and never creates any of the 41 aggregate-only games as rows. It preserves the six underlying blocker records, plus the provisional-inclusion prerequisite, while projecting **two generic accounting residual families**: four exact aggregate-only seasons (including the narrow owner-approved 1943–44 wartime exception), and the 1920–21 official/detailed contradiction with its separate **terminal contested-source representation**. The latter stays explicitly NOT resolved as same-game identity and never becomes an additional game row.

The original 469 inherited rows and their original source IDs remain unchanged in the embedded Research-base source CSV. The generic parent ledger contains 479 identified games and 39 season-census rows; raw original checkpoint and source are preserved byte-for-byte. The source aggregate of 1920–21 is 11–3, distinct from 9–2 detailed results. No three-game arithmetic allocation is permitted.

## Real-target rehearsal

The exact materializer produced this parent SHA-256 against the authenticated checkpoint and authenticated Git source:

`4e5567e832deb63f531dd3a04386de3afd1755db0717dc89a86f67a1e948d8e0`

The identified-game ledger SHA-256 is:

`ea7b96988b9618fd39b50aa7a271850fda71a5aa9c138c7f8b35ed0797e25ae4`

The complete 39-season census SHA-256 is:

`320012930b90d1b9c1b4e6f561e81fb6352779b43b5bfef10c9c336a5e305932`

A temporary **synthetic owner authority fixture** established that the unchanged current-main generic auditor finds zero defects, and its `verify-closeout` returns `VERIFIED_EARLY_HISTORY_ACCOUNTING_CLOSEOUT` with `stage1_complete:true`. This test **does not count as real protected-main authority or a production closeout**.

After tool-only merge, register the exact already-approved Arizona State case in current `data/reference/early-history-accounting-authorities.json`, with exact parent/ledger/census SHA bindings and the existing registry schema only. Reauthenticate the registry and the protected main, rerun the **unchanged** permanent generic `audit`, `closeout`, and independent `verify-closeout` against the real parent. Stop at the ordinary Stage 1 owner-facing boundary. Do not proceed to Stage 2 without authorization.
