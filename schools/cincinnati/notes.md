# Cincinnati men's basketball research notes

## Status
- School: Cincinnati
- Source program key: `cincinnati`
- Research base / current protected main: `6c02a8e144d7c2c0b43bdedf3255ee36ec5f06b7`
- Owner-confirmed history scope: `INCEPTION+`
- Competitive games: **3,058**
- Stage 1: COMPLETE
- Stage 2: COMPLETE
- Stage 3A: COMPLETE — authoritative checkpoint SHA-256 `64d638c68caa7fdafc45cec65810069131ed8bdc18b5d57133dbf3d685c30628`
- Stage 3B: INHERITED COMPLETE — exact 202-ID equality verified; 202/202 exact physical venue/city/state
- Stage 4 six-file package QA: PASS
- Stage 5 owner NON_D1 sanity scan: **APPROVED — 0 flags**
- Stage 6 pre-freeze adversarial self-challenge: **PASS**
- RESEARCH_FROZEN: NO
- CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES

## Universe and partition
- Full competitive universe: 3,058 rows.
- Regular season: 2,856 rows.
- Postseason: 202 rows.
- Exact partition remains 2,856 + 202 = 3,058.
- Regular-season H/A/N: 1,584 SOURCE_PROGRAM_HOME / 1,112 OPPONENT_HOME / 160 NEUTRAL.
- All-game H/A/N: 1,607 SOURCE_PROGRAM_HOME / 1,126 OPPONENT_HOME / 325 NEUTRAL / 0 UNKNOWN.

## Stage 6 repair
`CIN-STG1-01312` (1971-01-22 vs Iowa) remains **NEUTRAL**. Cincinnati's institutional yearly-results code `N` is independently confirmed by contemporary Daily Iowan reporting that Iowa's 73-69 loss to Cincinnati was played at **Chicago Stadium**. The row is therefore repaired from venue blank / Cincinnati, OH to **Chicago Stadium — Chicago, IL**. Iowa's later institutional schedule wording `at Cincinnati` is preserved as conflicting reciprocal evidence but is not adopted as H/A/N truth because the contemporary physical-site evidence is more specific.

## Site research after Stage 6
- HOME publication blockers: 0.
- Modern regular-season neutral exact venue: 88/88.
- Surviving pre-1984-85 neutral researched site debt: 5 rows.
- All surviving neutral debt is pre-1984-85, explicitly research-accounted, and treated as terminal historical debt under the project stopping rule.
- Postseason physical sites: 202/202 exact.
- NCAA: 78/78 exact physical venue/city/state.

## Exact-date / source-limited debt
Six 1906-07 rows retain blank exact dates and scores. Cincinnati's institutional source explicitly states that six additional games were played, all on the road, while opponents and scores are unknown. Those six source-explicit aggregate slots are terminal historical debt; no dates, opponents, or scores are inferred.

## Physical-venue identity challenge
- Local venue relationship rows: 112.
- Definite current-main physical reuses serialized in Research: 96.
- `Special Events Arena` (Honolulu, 1994) is retained under its accepted historical source-era name; University of Hawai'i institutional history confirms it is the same physical building later renamed **Stan Sheriff Center**. It is recorded as a **likely current-main reuse of VEN-000194**, with final shared-registry reuse deferred to serialized Implementation.
- Other locally resolved identities requiring Implementation-time current-main reuse/registration determination: 15.
- Ambiguous historical physical identities: 0.
- Numeric global `venue_id` remains blank in Research by design.

## Opponent identity challenge
- Stage 5 owner NON_D1 scan: APPROVED, 91 identities / 443 games / 0 flags.
- Source-explicit researched-unknown opponent slots: 6 (1906-07); not classified as NON_D1.
- Exact canonical-name collision against the current-D1 registry during Stage 6: 0.
- Modern non-current identities were specifically rechecked; no current-D1 remap is supported.
- Known current-program key splits: 0.
- Ambiguous current-program matches: 0.

## Stage 6 conclusion
**PRE-FREEZE SELF-CHALLENGE: PASS**

Research/package acceptance after the bounded repair:
- errors: 0
- warnings: 0
- unresolved opponent mappings: 0
- HOME publication blockers: 0
- NCAA site gaps: 0
- unaccounted material site gaps: 0
- ambiguous physical venue identities: 0

Stage 7 immutable packaging / `RESEARCH_FROZEN` has **not** begun.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=f0ed7c8e9d48892990d58a434286124ab851aab2` from `research_base_sha=6c02a8e144d7c2c0b43bdedf3255ee36ec5f06b7`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

Owner-authorized Stage 1 conference-history reconciliation was applied during current-main integration; the exact correction specification and hash are recorded in the Integration Freeze manifest.
