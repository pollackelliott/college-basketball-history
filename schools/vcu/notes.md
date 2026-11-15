# vcu research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: 38e882a432f8301ad9711682989f12c5857e6974e67eb34115358783908d3bd5
- Research base SHA: 9b009c0bed995a9d9af52c5908f0b6abec5532a7
- Stage 3B status: COMPLETE
- Competitive games: 1,650
- Primary-source historical results cutoff: 2025-2026
- Required completed-season cutoff: 2025-2026
- Coverage cutoffs are explicit Research declarations; media-guide titles and filenames are not coverage inference rules.
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 106
- NCAA_TOURNAMENT: 34
- NIT: 12
- POSTSEASON: 7
- REGULAR_SEASON: 1,491

## Final H/A/N census

- NEUTRAL: 232
- OPPONENT_HOME: 631
- SOURCE_PROGRAM_HOME: 787

## Accepted top-level history scope

- Accepted VCU top-level scope: 1973-74+.
- This is the owner-confirmed final Research scope carried through the complete 1973-74 through 2025-26 package; no earlier seasons are included.
- Serialized Implementation must treat this frozen scope as historical authority unless genuinely contradictory new evidence appears.

## Stage 5 owner NON_D1 sanity scan

- Owner disposition: APPROVED (`Approved. Proceed`).
- Distinct NON_D1 identities reviewed: 26.
- Games represented by those identities: 41.
- No owner-flagged identity remains unresolved.
- This approval is the required Research sanity scan and is not Implementation Owner Gate 1.

## Stage 6 pre-freeze self-challenge

PRE-FREEZE SELF-CHALLENGE: PASS

- RESEARCHED_UNRESOLVED_HOME_VENUE: 0 final rows; no HOME publication blockers.
- UNKNOWN H/A/N: 0 final rows.
- UNKNOWN exact dates: 0 final rows.
- Venue physical identities: 68 local rows; 67 definite current-main physical reuses; 1 genuinely new candidate (Franklin Street Gym, Richmond, VA); 0 ambiguous physical identities.
- Modern U.S. regular-season neutral exact-venue unresolved: 0.
- Modern foreign locality-sufficient blank buildings: 3 (two 2008-09 Cancun, Mexico rows; one 2021-22 Paradise Island, Bahamas row), explicitly researched/accounted under foreign-locality policy.
- Historical regular-season neutral exact-building debt, 1995-96 and earlier: 27 rows after the completed location-first pass; all are explicitly researched/accounted terminal historical enrichment debt.
- Postseason exact-venue unresolved: 0.
- NCAA Tournament rows reviewed for round authority: 34; 30 supported controlled round assignments populated; 4 historically justified blanks preserved (1980 Iowa, 1981 Long Island, 1983 La Salle, 1984 Northeastern); owner-level conflicts: 0.
- Opponent identity audit: 228 current-program keys checked; 0 known current-program key splits; 0 ambiguous current-program matches; 26 NON_D1 identities owner-reviewed.
- Stage 6 bounded historical repair: VCU-2012-13-006 vs Missouri numeric orientation corrected to VCU 58-65 while preserving accepted L and literal/source score evidence `Nov. 24 vs Missouri& L 65-58`.
- Stage 3A-4 opponent-home accounting: complete 612-row regular-season OPPONENT_HOME population reconciled. VCU-1974-75-024 vs Detroit Mercy preserves `RC` only as literal `source_venue_name`; curated venue/city/state remain blank; `RESEARCHED_PARTIAL` basis preserves the accepted source-school responsibility boundary. No physical meaning is inferred from `RC`.
- Repaired permanent Stage 4 preflight: PASS, 0 defects.
- Final Stage 4 parent/package semantic comparison: PASS, 0 unexpected mismatches.
- Permanent Research acceptance: PASS, 0 errors, 0 warnings.
- Protected-main SHA for final Research closeout: 7a93e99ed37d66dfe07a801c3ecec86cd9f16d99.

RESEARCH_FROZEN: YES
CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=7a93e99ed37d66dfe07a801c3ecec86cd9f16d99` from `research_base_sha=9b009c0bed995a9d9af52c5908f0b6abec5532a7`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

---

## Accepted supplemental All-History expansion

# VCU ALL_HISTORY_EXPANSION — supplemental Research Freeze

- Workflow: ALL_HISTORY_EXPANSION. School key: vcu.
- Original immutable research_base_sha: df73675852ec5a43dfac50da0ee06d8bcabf8832.
- Researched institutional program inception: 1968-1969. Accepted top-level published baseline is inherited, scoped 1973-74+.
- Exact accepted 109 competitive supplement games: five ACTIVE seasons 1968-1969 through 1972-1973; game rows reproduced byte-for-byte from the verified Stage 4 package (Stage 6 audit approved).
- Inherited baseline source package contains 1650 source games; no inherited source games or canonical rows are copied into supplemental source rows. The immutable baseline remains authoritative and unchanged.
- Source ledger season totals: 1968-1969 23; 1969-1970 23; 1970-1971 24; 1971-1972 19; 1972-1973 20. All are REGULAR_SEASON, with HOME 52, OPPONENT_HOME 50, NEUTRAL 7; zero exhibitions, unknown H/A/N, and postseason games.
- Opponent support: 82 source-literal/key rows; 30 exact inherited label/key extensions and 52 new source-label/key support rows (including 9 literal aliases of inherited institutions whose exact inherited label/key pair does not exist). Every existing institutional identity and D1 classification is preserved.
- Venue support: two EXTEND_INHERITED physically identical sites, Franklin Street Gym / VEN-001102 and Richmond Coliseum / VEN-000175, preserving inherited venue keys and relationships. New supplemental HOME assignment counts are 41 and 11. Physical IDs are not allocated or mutated.
- Stage 5 owner approved the complete 27-key / 59-game NON_D1 scan with response "Approved. Proceed"; no flagged identities.
- Stage 6 adversarial self-challenge: PASS with zero historical-semantic corrections; the seven 1968-1969 Quantico and Fort Eustis location-complete historic regular-season neutral exact-building blanks remain accepted NONBLOCKING_RESEARCHED residuals. OPPONENT_HOME physical buildings for 50 rows are outside source-school responsibility, not researched building debt.
- The original source literal `#at Bridgewater` conflicting with explicit Quantico tournament footnote is preserved verbatim; accepted neutral classification remains unchanged.
- The inherited four-row Southeastern baseline correction was resolved separately by PR #566 with exact Production proof; correction question is retained as NO_EXPANSION_IMPACT, not re-applied in this supplement.
- All five seasons ACTIVE; no dormant/no-team seasons or separate documented exclusions identified in the accepted supplemental population. The exclusions table is explicitly empty.
- Stage 4 parent ZIP SHA-256: 8f0fb33621df107e5be74fad60198cea2167e9c666d5e241d9168f098b11e0d9. Stage 3B original SHA-256: 00f552c1e46fd753db96172cde923f0b90fa03162c7a56bd5d321a64f56db8df. Stage 6 audit parent ZIP SHA-256: ff334d2d8d91a13a21968198212b3e71c2d9b555b95c0d8f548cb3f77440c9e4.
- Research Freeze is supplemental-only and does not authorize Implementation, protected-main changes, shared-reference registrations, or reopening inherited published history.
