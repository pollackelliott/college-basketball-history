# uconn research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: 62f7b0f5642113f411feb68135b9c44b4b5e7ab353015903da3159a40fb37473
- Research base SHA: 300c78d46a08ee0812ab9d72d2a54d8da51bb591
- Stage 3B status: COMPLETE
- Competitive games: 2,909
- Primary-source historical results cutoff: 2024-2025
- Required completed-season cutoff: 2025-2026
- Coverage cutoffs are explicit Research declarations; media-guide titles and filenames are not coverage inference rules.
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 2
- POSTSEASON: 238
- REGULAR_SEASON: 2,669

## Final H/A/N census

- NEUTRAL: 346
- OPPONENT_HOME: 817
- SOURCE_PROGRAM_HOME: 1,746

## Stage 6 bounded pre-freeze self-challenge repair

- `UCONN-STG1-000613` (1974-75 at Maine): exact date recovered as `1975-02-02` from the official UConn Athletics 1974-75 schedule archive, which identifies the same 100-90 overtime win at Maine. The literal Stage 1 raw token `2/?` remains preserved in `source-games.csv`; no opponent, score/result, H/A/N, venue, game type, inclusion, or season meaning changed.

## Stage 6 systematic overtime serialization repair

- The adversarial self-challenge identified one homogeneous Stage 1 extraction defect affecting 101 games whose preserved literal `raw_text` explicitly marks a single overtime with standalone `ot`/`(OT)`, while `overtime_periods` had either captured the opponent score or remained `0`. Those 101 rows are deterministically normalized to `overtime_periods=1`. Explicit multi-overtime tokens (`2ot`, `3ot`, `4ot`, `6ot`) remain unchanged. No score, result, date, opponent, H/A/N, venue, game type, inclusion, or raw evidence changed in this repair.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=f5cb20f0b40b41864a3fbcb6d5e97dd5e6648fe7` from `research_base_sha=300c78d46a08ee0812ab9d72d2a54d8da51bb591`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.

Owner-authorized Stage 1 conference-history reconciliation was applied during current-main integration; the exact correction specification and hash are recorded in the Integration Freeze manifest.
