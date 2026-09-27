# Wake Forest source notes — RESEARCH_FROZEN

## Primary institutional source

**Wake Forest men's basketball media guide / record book** — owner-supplied `Wake.pdf`.

- SHA-256: `60b0fc48a50b9fb3bc3b74a6c94dcf82dfac889f7694c27635d9014575da8b62`
- 65 PDF pages.
- Primary year-by-year game ledger: printed pp. 55-65.
- All-Time Results reconciliation: printed pp. 9-10.
- All-time opponent series reconciliation: printed pp. 43-53.
- Literal `raw_text`, source locator/page, and source opponent label remain preserved per game in `source-games.csv`.

The Stage 6 exact-date challenge confirmed that the controlling Wake institutional source itself omits month/day information for the opening 1950-51 block represented by the final 11 blank-date rows from that season; no dates were inferred.

## Current-season institutional supplement

Wake Forest Athletics' official **2025-26 men's basketball schedule** supplies the completed 2025-26 competitive schedule after the record-book cutoff. The Oct. 29 ETSU exhibition remains excluded. The accepted season contains 35 competitive games and finishes 18-17.

## Stage 6 current-main reciprocal recovery — Florida, 1936-02-13

Stage 6 rechecked the UNKNOWN H/A/N population against every opponent with a currently published school package on protected main.

`WF-STG1-00441` (1936-02-13 vs Florida) is the one newly productive recovery.

- Wake Forest source: `F13 Florida W 43 32`; H/A/N omitted.
- Current-main Florida source row: `FLARAW-00256`; literal `F13   Wake Forest           A    L      32    34`; `curated_site_type=OPPONENT_HOME`.
- Field-specific conclusion: Florida was away, therefore Wake Forest was HOME.
- Accepted Wake facility chronology for 1935-36 assigns **Gore Gymnasium, Wake Forest, NC** to ordinary HOME rows.
- Score conflict preserved: Wake 43-32 versus Florida 34-32 from Wake's perspective. No score/result field was changed.

This is a site-field recovery only; it does not use the reciprocal source to overwrite Wake's accepted score.

## Stage 6 published-reciprocal UNKNOWN challenge

Current protected-main published-school overlap with the 319-row inherited UNKNOWN population consisted of 33 rows across Arkansas, Duke, Florida, Maryland, and North Carolina.

- Duke: 24 rows; current reciprocal rows themselves remain UNKNOWN for the matching early games; 0 recoveries.
- North Carolina: 6 rows; exact institutional reciprocal evidence conflicts with literal Wake H/A/N; preserved as explicit conflicts.
- Maryland: 1 row; institutional conflict preserved.
- Arkansas: 1 row; institutional conflict preserved.
- Florida: 1 row; recovered HOME as described above.
- Remaining UNKNOWN rows: no additional current-main published reciprocal school package; prior target/project/source-family research remains controlling.

Final UNKNOWN H/A/N count after the recovery: **318**.

## Stage 6 exact-date challenge

The final blank-date population remains **452** rows.

Two concentrated institutional/reciprocal opportunities were challenged:

1. **NC State — 72 Wake blank-date rows, 1910-11 through 1949-50.**
   - Source: NC State 2025-26 men's basketball media guide, Year-by-Year Results.
   - The 1910s-1945-46 section lists the relevant Wake Forest games without calendar dates.
   - The 1949-50 Southern Tournament Wake Forest game is explicitly printed as `N/A vs. Wake Forest W, 59-53`.
   - Date recoveries: **0**.

2. **Duke — 30 Wake blank-date rows.**
   - Source: current-main `schools/duke/source-games.csv`.
   - Matching early reciprocal rows also preserve blank exact dates.
   - Date recoveries: **0**.

The Wake 1950-51 institutional block accounts for another 11 blank dates and itself omits month/day values. No comparable additional high-yield institutional source family was identified. Stage 6 therefore stops under the terminal historical date-debt rule rather than performing independent archival searches for hundreds of rows.

## Venue physical-identity recheck

Current protected-main venue registry and alias registry were rechecked on Stage 6 resume.

- `data/reference/venues.csv` blob: `ef5a21a665f47162da63cf5112c5fb4c014445b8`
- pending Wake local identities remain 6
- location-compatible ambiguous physical identities: 0

The six pending local physical identities remain:
Wake Forest College Gymnasium; Gore Gymnasium; Memorial Coliseum (Winston-Salem); R.J. Reynolds High School; Montego Bay Convention Center; Racer Arena.

Numeric/global IDs remain Implementation-authoritative.

## Opponent-identity recheck

Protected-main program registry blob on Stage 6 resume:
`2054031805df1d5fbe21d388eab92871fc131ac8`.

This is unchanged from the clean Stage 4 opponent-registry reconciliation. Stage 5 owner approval remains controlling (82 NON_D1/historical identities / 278 games / 0 flags). The three modern NON_D1 identities — Catawba, Saint Francis (Pa.), and Winston-Salem State — were specifically rechecked; no current-program key split or ambiguous current-program match was exposed.

## Postseason

All 207 postseason rows remain closed and exact-site complete:
conference tournament 134; NCAA 51; NIT 22.

The owner's two March 2026 ACC Tournament H/A/N corrections remain NEUTRAL at Spectrum Center, Charlotte, NC.

## Research provenance

- `research_base_sha`: `e57a7049b2315508e59fd68b4324c34050901f45`
- Stage 3B complete checkpoint SHA-256: `da95127b37421fb9f07cdca1422c4e1f4935cae3244b1a52f295f19f773e5437`
- Stage 5 owner-approved checkpoint SHA-256: `c8106eb143bbcf8c247352400bd3fa838876501f703de610e139602aebb6591e`
- Stage 6 initial protected main: `f0ed7c8e9d48892990d58a434286124ab851aab2`
- Stage 6 resumed/revalidated protected main: `2ed1ca5c8733f68f05efd02d831c0bafc243fd07`
- Stage 6 pre-freeze self-challenge: **PASS**
- `RESEARCH_FROZEN`: **YES**

## Stage 7 immutable freeze

- protected `main` at final Research freeze: `de6d3a9c58a9675557f9624438d3745a6591d070`
- Stage 6 checkpoint SHA-256: `1c97c0653fe3eed70dafe03e598381dc080ced5b2df10593885eb67da6e231dd`
- Stage 5 owner NON_D1 disposition: **APPROVED**, 82 identities / 278 games / 0 flags
- pre-freeze adversarial self-challenge: **PASS**
- final permanent `research-check`: **PASS**, 0 errors / 0 warnings
- `RESEARCH_FROZEN`: **YES**
- current-main rebase before tracked Phase 0: **REQUIRED**
