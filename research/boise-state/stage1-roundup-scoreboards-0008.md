# Boise State ALL_HISTORY_EXPANSION — Stage 1 checkpoint 0008

**STATUS: STAGE_1_IN_PROGRESS** — existing Boise State Research lane only. No Stage 2, Research Freeze, Implementation, owner gate, protected-main mutation or shared/global registry mutation.

## Exact immutable authority and parent

- Protected main reauthenticated: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`.
- Immutable `research_base_sha`: `1c3bb7f1d3231c604c413ed75a4afc17b0388089`.
- Research branch at tranche start: `4fe7d6df5d1415a9d91aa43560055d5038575c1c`.
- Parent 0007 ZIP SHA-256: `630b00f6eb66716a6f7616e152542c4b443d11b6022ab712e37a48ecfbacc3c0`.
- This new portable ZIP: `boise-state-expansion-stage1-roundup-scoreboards-0008.zip`.
- New ZIP SHA-256: `228d91a96367ddfbd716f158e6011abde4a384df6a0b436cf3d1f5d99dd3efb3`.
- Full 16-column ledger member SHA-256: `39197cd29f8594dbe3639848033f48c229bf9fda21039997b42cddbd0c0055b2`.
- ZIP contains `manifest.json` with independently verified all-member checksums, complete 134-row ledger, original raw-source inventory, all 38 seasons, exact official accounting, six new game evidences, explicit exclusion/candidate ledger, and residuals.
- GitHub mirrors: `stage1-roundup-scoreboards-0008-ledger.csv` (134 concise rows); `...-accounting.csv` (38 seasons); `...-season-census.csv` (38); `...-evidence.csv` (6 new primary-source game facts); `...-exclusions.csv` (3 exclusions/candidates). The portable ZIP is richer source/provenance transport.

## Bounded source-family result

Six **new** source-backed game identities, 5 Boise wins / 1 loss, all distinct from the preceding 128 entries:

| Season | Opponent, literal or cautiously identified | Boise result | Source |
|---|---|---|---|
| 1940-41 | Eastern Oregon College | W 52-50 | Bend Bulletin Feb 12 1941 p2 results https://oregonnews.uoregon.edu/lccn/sn90051770/1941-02-12/ed-1/seq-2/ocr/ |
| 1941-42 | Willamette University | W 49-21; Dec22 1941 | La Grande Evening Observer Dec23 p5 results https://oregonnews.uoregon.edu/lccn/2026234413/1941-12-23/ed-1/seq-5/ocr/ cross-check Willamette itinerary in Oregon Statesman Dec13 p10 https://oregonnews.uoregon.edu/lccn/sn85042470/1941-12-13/ed-1/seq-10/ocr/ |
| 1941-42 | Lewiston Normal School | W 57-36 | La Grande Evening Observer Jan14 1942 p6 https://oregonnews.uoregon.edu/lccn/2026234413/1942-01-14/ed-1/seq-6/ocr/ |
| 1942-43 | College of Idaho (first distinct identity) | W, score/date unknown | La Grande Evening Observer Feb25 1943 p8 explicitly says Boise split games with College Idaho https://oregonnews.uoregon.edu/lccn/2026234413/1943-02-25/ed-1/seq-8/ocr/ |
| 1942-43 | College of Idaho (second distinct identity) | L, score/date unknown | Same original 1943-02-25 statement; source establishes two games one W one L but not sequence |
| 1961-62 | Weber (literal only, do not force identity alias) | W 83-68 | Bend Bulletin Jan22 1962 p2 UPI basketball scores https://oregonnews.uoregon.edu/lccn/sn90051770/1962-01-22/ed-1/seq-2/ocr/ |

Historical scores do not themselves establish H/A/N. All six new site types remain UNKNOWN; dates from mere retrospective scoreboards were not invented. The 1941-42 Willamette date Dec22 is independently supported by prior itinerary and next-day result. The 1942-43 College of Idaho 1-1 pair explicitly represents two games; unknown results and game dates do not identify more specific fixtures.

## Genuine first-party exclusion and uncertainty

Boise Junior College's own *Roundup*, February 21, 1941 page 8, OCR transcription https://doczz.net/doc/363767/roundup--february-21---scholarworks, whose original issues are catalogued at https://scholarworks.boisestate.edu/student_newspapers/, says:
- Boise defeated Montgomery Ward's local team **91-41** but explicitly labels it the first of many **practice games** preceding the state AAU tournament. This is EXCLUDED as practice/exhibition, not a varsity competitive identity, despite the exact score being known.
- Its previous-year AAU state title story recounts wins over Weiser Institute, YMCA and College of Idaho before Boise's already-recognized Denver 1940 national-tournament loss. Source transcription interleaves column text; avoid premature identity/segmentation adjudication, especially College of Idaho match duplication with two February 1940 rows. Preserve as candidate in `...-exclusions.csv` only.
- A December 6, 1941 Eastern Oregon vs Boise JC opponent schedule appears in 1941-11-25 newspaper but a completed played contest/result was not verified. Schedule-only evidence remains excluded from played-game ledger.

## Mechanical reconciliation

- Previous parent: **128** supplemental game identities, all preserved identically in game-level content.
- New: **134** unique supplemental game identities = **79** junior-college (including the one MW-omitted 1937-38 game) + **55** 1968-69 and 1969-70 official record-book games.
- Within exactly the 33 MW-listed pre-1968 annual seasons, **78** individually identified games.
- MW institutional junior-college annual arithmetic remains 441-346 (787). Numerically **787-78=709 unmatched**, not 709 anonymous real game IDs and not proof identical aggregate membership definitions.
- Parent provenance and original full 16-column data preserved in the ZIP; concise GitHub mirror preserves exact game identities and source-delta URLs. All 134 game IDs are unique.
- Remaining 1932-33 inception, 1937-38 unlisted competitive game/aggregate issue, 1938-39 unknown, 1950s discrepant W/L, AAU state tournament collision and exact schedule/inclusion questions are held as residuals.

## Bounded stop / recovery

Stage 1 remains OPEN. Next bounded tranche should seek coherent first-party *Roundup* issue group, source-backed annual schedules or reciprocal multi-opponent histories, not repeated one-score web searches or broad unrelated archaeology. No owner authority or gate is required. Protected main and inherited 1,670-row Boise published 1970-71+ package never touched.