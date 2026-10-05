# notre-dame research package notes

## Stage 4 deterministic authoring

- Stage 3B checkpoint SHA-256: 86e2312e68545e484227c61e06d2be7c78c04377913da1fd4b8861c6922e3138
- Research base SHA: 80be0cb32669e03e9d064f34420bb861f8a8783c
- Stage 3B status: COMPLETE
- Competitive games: 3,137
- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.

## Final game census

- CONFERENCE_TOURNAMENT: 52
- NCAA_TOURNAMENT: 81
- NIT: 39
- REGULAR_SEASON: 2,965

## Final H/A/N census

- NEUTRAL: 374
- OPPONENT_HOME: 1,161
- SOURCE_PROGRAM_HOME: 1,533
- UNKNOWN: 69


## Stage 6 pre-freeze adversarial self-challenge

Stage 6 was executed against protected main `5f8e005ee37aeb02034bd02fe593386b25747c71` while preserving immutable
`research_base_sha=80be0cb32669e03e9d064f34420bb861f8a8783c`.

The audit identified one bounded historical-data deficiency: 14 historical regular-season
neutral rows had complete city/state and were terminalized as building-enrichment debt even
though the accepted Notre Dame source row itself explicitly supplied an exact building.
Those 14 rows were repaired from the preserved literal `source_venue_name`; no H/A/N,
date, score, result, game type, locality, or raw source text changed.

The physical-identity challenge also reconciled local venue representation to current main:
Matthews Arena -> VEN-000766 Boston Arena / Matthews Arena; The Armory (East Lansing) ->
VEN-000292 Michigan State Armory; and duplicate local `FW Memorial Coliseum` representation
was collapsed into VEN-000301 Allen County War Memorial Coliseum. The repaired 1990
Superdome row reuses VEN-000034 Caesars Superdome. Shared/global registries were not mutated.

`PRE-FREEZE SELF-CHALLENGE: PASS`. This package is Stage 6 complete but is **not yet
RESEARCH_FROZEN**; the next bounded stage is the repository Research Freeze boundary.

## Integration staging

Current-main shared-reference rebase completed against `integration_base_sha=a1875c8923a452d3312fafd3217e50058694c9ba` from `research_base_sha=80be0cb32669e03e9d064f34420bb861f8a8783c`. The authoritative final venue-ID mapping is recorded in the ignored `.onboarding/<school>/integration-freeze.json` manifest. Status: **INTEGRATION_FROZEN**.
