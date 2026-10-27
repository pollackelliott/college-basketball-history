# Gonzaga — score-only superseding Research Freeze self-challenge

Status: **PASS — BOUNDED SCORE-SPECIFIC ADVERSARIAL REVIEW**

This is a narrowly authorized repair of a proven defect in the previously accepted frozen Research package, **not** a new school-wide Stage 6 review. The predecessor's accepted Stage 5 owner NON_D1 approval (39 distinct identities / 160 games) and earlier Stage 6 site/identity/round self-challenge remain controlling for every unchanged field.

## Exact source and boundary

- Original six-file freeze archive: `6a4632f21ed21ef9f6015eff84501dcdc4372fe3ac7fd0856b197b867f2dab8f` (verified from 11 immutable transport parts at commit `0f240b4f036458883b90f1e69140257d2166bb33`).
- Repaired six-file freeze archive: `8fe9d4db69a31ee957b41b029b7e034327836f1303baba26b97d98db2f55142d`.
- Original immutable research base: `fa692b90a72bf32f56bba63c1e10c958513a42f7`.
- Current protected-main tools for acceptance: `16907c93fb47c5373d4aa9994654e7a6d8315fbb`.
- Institutional source: *2026-27 Gonzaga Men's Basketball Record Book* (uploaded PDF SHA-256 `9bdbdcdc24148aa4f762b7d11da983663ecd5b18da20061a00f757c8c16fe2da`).

## Evidence-class challenge

The original `source-games.csv` had both score fields blank for all 2,053 games despite 2,053 preserved score-like pairs in literal `raw_text`. The new permanent checker (merged PR #382) now rejects that defect.

- 2,043 rows: the single literal score pair agreed with the frozen `played_result` from Gonzaga's perspective; its two values were inserted directly.
- Ten exceptional rows: individually adjudicated in `score-restoration-adjudication-20261027.json`, preserving original `raw_text`; supported corrected values were entered.
- The Boise State game of February 18, 1972 and Pepperdine game of January 15, 1993 retain frozen on-court `L` results despite contradictory Gonzaga printed `W` source strings; opponent-institutional evidence corroborates the losses and repaired score values.
- The Montana game of January 13, 1968 (83–82), Oklahoma State game of December 31, 2012 (69–68), and Saint Mary's game of February 25, 2023 (77–68) repair damaged/tied literal text with corroborating results.
- Four later postseason/regular-season source score strings listed the winner's higher score first rather than Gonzaga's score first; the verified values were normalized to Gonzaga perspective.

## Adversarial negative checks

- Games in original/repaired archive: **2,053 / 2,053**; game IDs and ordering identical; duplicate game IDs **0**.
- Remaining blank score pairs **0**; score/result arithmetic mismatches **0**.
- All other fields of all 2,053 rows identical to the exact original six-file archive, including date, opponent identity, literal raw text, site type, venue/location, event, tournament round, overtime, normalization, and administrative fields.
- Five other six-file members identical at content-byte level to the original archive.
- Current research acceptance: **PASS**, zero unresolved opponent identities, zero unaccounted material site gaps, zero HOME chronology conflicts.
- Prior accepted historical uncertainty (including one unknown exact date, 125 UNKNOWN H/A/N rows, and accounted neutral venue debt) intentionally preserved; this score-only correction provides no authorization to reopen it.

## Independent verification

GitHub Actions read-only run **40457824944**, job **122035170521**, completed **SUCCESS**:
https://github.com/pollackelliott/college-basketball-history/actions/runs/40457824944

The run independently decoded the original transport and repaired candidate archive, checked both ZIP SHA-256 values and CRCs, compared every CSV non-score field, validated score arithmetic and the exact ten exception IDs, and ran unchanged permanent `tools/onboarding_hardening.py research-check` at the pinned current protected-main SHA.

**Conclusion: PRE-FREEZE SCORE SELF-CHALLENGE PASS.** No remaining score residual, conflicting source authority omitted, or generic tooling issue in this bounded population. Existing Stage 5 and other Stage 6 conclusions are preserved.

## Supersession boundary

`RESEARCH_FROZEN` applies to the immutable repaired ZIP only; it supersedes the previous ZIP's authority for subsequent *new* integration intake. The supersession **does not** rewrite or reauthorize Gonzaga Implementation PR #381, its old Owner Gate 1 review, sealed plan, Preview, or rejected Owner Gate 2. Rebase and further release disposition require separate guarded authorization.
