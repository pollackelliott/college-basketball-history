# San Diego State founding-era Stage 1 source ledger — checkpoint 0002

## Scope and lineage

- Same ALL_HISTORY_EXPANSION Research lane; immutable research_base_sha `5b840a354fb5cd792239ff8b93cba223a18dd87a`.
- Parent checkpoint: `0001-inception-source-inventory` at research HEAD `98d6b843fa2be17922b16a760cd8932ba0bbf290`.
- This is a **source-identification and exact institutional-accounting checkpoint**, not Stage 1 COMPLETE, not Research Freeze and not Implementation.
- 242 individual result lines are transcribed mechanically from 2026-27 SDSU official guide printed pp. 88-89 (PDF pp. 90-91), covering 1921-22 through 1935-36.
- Rows have deterministic local IDs with chronological *source-list* order within each season. A missing date token is left blank. No sequential calendar inference has been made. Literal opponent/source tokens, original W/L/T, ot-, conference star, ambiguous (D), score blanks, and named-event text remain separately preserved.
- The official source documents 163 wins, 86 losses and one tie across these seasons = 250 institutional result/administrative outcomes; 242 result lines = 157 W / 84 L / 1 T. Five listed forfeit awards and three explicitly unidentified results explain the remaining eight season aggregate entries exactly. This **does not establish** that each award or each identified line should become a canonical varsity played game. Forfeits are preserved separately, not placed in candidate game ledger.
- Only 13 of 15 seasons have source result lines that equal their aggregate W/L/T without special accounting; 1921-22 and 1924-25 reconcile only after keeping the two distinct source-noted classes.
- `source-game-candidates.csv` is not an accepted supplemental game ledger. Its game_type fields intentionally remain empty pending inclusion/taxonomy review; no claim of current Stage 1 acceptance or structured game_type completeness.
- Possible noncompetitive/intra-school events: SDSU JV (1921-22) and San Diego State All-Stars (two 1922-23 results). These need source-backed classification, not unsupported exclusion. “Alumni at Stanford” may represent an institutionally different opponent; do not conflate with SDSU Alumni on name similarity.
- (D) appears on 28 source-listed result lines; official legend/meaning remains unverified. It may not be silently expanded to “duplicate”, “demonstration” or “doubleheader”.
- 13 result lines appear under named AAU/YMCA tournament headings; distinguish in-season tournaments, postseason, sanctioned varsity play and exhibitions on evidence before assigning game_type.
- Exactly five source result lines lack numeric scores: 1929-30 USS Melville, 1930-31 San Diego YMCA and DeMolay, 1931-32 Bank of Italy and North Island NAS. They retain source W results.
- Ten source-listed game lines lack a printed date token. Do not assume the immediately preceding date.
- Games were not matched against canonical or opponent reciprocal records yet. Accepted 1970-71+ published 1709 source games remain untouched.
- No source games from 1936-37 onward were extracted in this bounded unit.

## File meanings

- `source-game-candidates.csv`: 242 literal source-identified result candidates; no game_type/historical inclusion yet accepted.
- `season-accounting.csv`: 15-season exact W/L/T reconciliation, recording source-listed versus forfeit/unidentified separately.
- `administrative-and-unidentified.csv`: the eight source-acknowledged entries excluded from candidate game ledger; three unnamed outcomes and five awarded forfeits.
- `research-status.json`: exact state, counts, and next bounded action.
- `manifest.json`: exact hashes; append-only sibling of checkpoint 0001, never rewrites predecessor.

## Sources

Owner PDF: **2026-27 San Diego State Men's Basketball Media Guide**, 182 pages. Printed pp. 88-89; PDF pp. 90-91. Original local PDF SHA-256: `9c63066b60365d4f90abdb36242bf880f84b87030f87d776a6f81fbc75b9f2ad`.

The accepted reference and original 1709-row published source package at exact research base `5b840a354fb5cd792239ff8b93cba223a18dd87a` are inherited baseline authority, not a source to be modified. Program inception 1921-22 and 1970-71+ scope remain as established by checkpoint 0001.
