# Research Freeze Self-Challenge

- **Status:** Required research-lane acceptance step
- **Applies to:** every school declaring `RESEARCH_FROZEN`
- **Purpose:** prevent mechanically accounted but insufficiently researched historical debt from entering the holster

A passing `research-check` is necessary but is not, by itself, sufficient for `RESEARCH_FROZEN`.

The permanent research acceptance gate can prove that required fields, vocabularies, opponent identities, NCAA sites, and research-accounting metadata are structurally valid. It cannot always prove that the researcher exhausted obvious authoritative evidence before labeling a historical fact unresolved or before assigning a locally plausible but globally stale opponent identity.

Therefore every Research lane must perform one adversarial self-review before final freeze.

The governing question is:

> **If the Control Center challenged the largest unresolved/debt populations in this portfolio, what would it challenge?**

Investigate those populations before declaring `RESEARCH_FROZEN`, not after.

## 1. General rule

The self-challenge is a bounded final research audit, not an invitation to restart the school from scratch. Residual populations enter this stage as accepted researched debt from completed earlier stages; Stage 6 must identify a concrete contradiction, deficiency, or systematic opportunity before reopening any portion of them.

It should target the largest or most suspicious residual debt classes, especially:

- `RESEARCHED_UNRESOLVED_HOME_VENUE`;
- `UNKNOWN` H/A/N;
- substantial exact-date blanks;
- neutral/postseason site debt;
- physical-venue identity candidates;
- opponent identities that look non-D1/historical even though a current global program may be the same institution;
- any modern or institutional series whose remaining unknowns are surprising relative to available reciprocal evidence.

The objective is not zero unknowns at all costs. The objective is to distinguish genuinely unrecoverable historical facts from debt that survived only because the primary source omitted a field, because an obvious reciprocal source was not checked, or because a current program was locally normalized to a stale historical key.

Unsupported certainty remains worse than a researched unknown.

### Terminal researched debt

The self-challenge has a stopping rule. For a meaningful residual population, challenge
the population as a class and inspect obvious authoritative/institutional/reciprocal
evidence plus any **specific** systematic high-yield recovery opportunity. Repair supported
defects in batch and isolate genuine contradictions narrowly.

When the surviving population is:

- homogeneous enough to describe coherently;
- explicitly researched/accounted under project policy;
- concentrated in an era/context where the remaining uncertainty is historically plausible;
- free of a known material publication blocker; and
- no further comparable systematic/high-yield evidence class is identified,

it remains **terminal researched historical debt**. Do not then launch independent
row-by-row searches merely to drive the unknown count toward zero.

A new systematic evidence class or genuine contradiction may reopen the affected
population. The mere fact that residual rows remain does not. After one systematic
opportunity is exhausted, surviving rows revert immediately to terminal debt unless
another comparably concrete opportunity has already been identified.

## 2. HOME venue self-challenge

If any `RESEARCHED_UNRESOLVED_HOME_VENUE` rows remain, the lane must report and validate:

- total count;
- season/decade concentration;
- home-facility era(s) involved;
- principal institutional, facility, archival, schedule, and reciprocal evidence checked;
- why the known facility chronology cannot safely assign a physical building at the individual-game level;
- confirmation that the population is not merely a broad primary-ledger venue blank carried forward under the exception.

A broad unexplored pre-arena era does not qualify merely because city/state are known.

The historical safety valve is especially relevant to genuinely difficult HOME games from
the **1930s or earlier**, but that era is not an automatic waiver. The self-challenge must
still ask whether obvious institutional, facility, archival, schedule, reciprocal, or
game-level evidence was actually exhausted.

If the self-challenge exposes a documented temporary home, alternate home, predecessor building, transition date, or reciprocal venue assertion, repair those rows before freeze.

Once a bounded population challenge establishes that a known aggregate facility allocation cannot safely be assigned at the individual-game level, preserve those rows as researched unresolved rather than repeatedly reopening the same allocation question.

## 3. UNKNOWN H/A/N self-challenge

If any `UNKNOWN` H/A/N rows remain, the lane must report and validate:

- total count;
- season/decade concentration;
- principal evidence classes checked;
- meaningful reciprocal recovery attempted where authoritative opponent histories are available;
- whether already-published/current-main opponent source packages provide usable reciprocal evidence;
- confirmation that every surviving UNKNOWN has substantive `site_research_status` / `site_research_basis` accounting.

The lane must explicitly challenge unusually large institutional series. A large group of UNKNOWN games against a school with an authoritative year-by-year opponent history is a review trigger, even when all rows already pass mechanical research-accounting rules.

Do not resolve H/A/N by geography, arena location, ordinary series pattern, or assumed host convention.

After the relevant evidence classes and systematic reciprocal opportunities have been challenged, surviving historically plausible UNKNOWN rows may become terminal researched debt. Do not repeatedly re-search them without new evidence.

## 4. Exact-date self-challenge

Unknown exact dates remain valid when historically honest, but a large block of blank dates must not survive merely because the primary school ledger omits month/day information.

When meaningful exact-date debt remains, the lane must report:

- the working/original blank-date count when a targeted audit occurred;
- the number of dates recovered during reciprocal/institutional research;
- the final blank-date count;
- season/decade concentration of the remaining blanks;
- principal authoritative reciprocal/institutional source classes checked;
- confirmation that dates were not inferred from schedule order, geography, usual series timing, or season chronology.

Recover only uniquely or sufficiently supported dates. Field-specific evidence may be used field-specifically: a reciprocal source can support a date without silently replacing a conflicting played score or other source fact.

For a large residual, first ask whether a **specific systematic source class** can materially reduce the population (for example, current-main published reciprocal packages or an authoritative opponent archive covering a concentrated series). Pursue each concentrated opportunity as one institutional/source-family challenge rather than as many independent game searches. If it does not materially resolve the population, preserve its survivors as terminal debt and move on. Once the comparable systematic opportunities are exhausted and the remainder is early/historical, explicitly accounted, and otherwise release-safe, serialize it as terminal exact-date debt rather than performing one independent search per remaining game.

## 5. Venue physical-identity self-challenge

Before freeze, reconcile local physical venue identities against the recorded `research_base_sha` well enough to report separately:

- total local physical venue rows;
- definite current-main physical reuses;
- genuinely new physical venue candidates;
- ambiguous physical-identity matches.

Do not equate “local venue row” with “new global venue.” Naming eras and aliases for the same building must not become duplicate physical identities.

Ambiguous physical-identity matches must be zero at `RESEARCH_FROZEN`.

Numeric global venue IDs remain provisional until serialized Implementation performs the authoritative current-main rebase.

## 6. Opponent-identity self-challenge

`unresolved opponent identities = 0` is not enough if a package has confidently resolved a current program to the wrong or stale key.

Before freeze, challenge opponent rows that are especially likely to hide identity debt:

- source/canonical labels that exactly match a current global program name but use a different key;
- opponent rows whose canonical key is current D1 in `data/reference/programs.csv` but whose local `current_d1` field is blank/No;
- aliases that another published/current-main school package already resolves uniquely to a current-D1 program;
- modern (especially 2000s+) rows treated as non-D1/non-current despite institutional-name changes or reclassification possibilities;
- duplicated institutional series that would split one real opponent into two site records.

The lane should compare against the current global program registry and, where useful, current published opponent packages. If repository tooling provides `tools/published_opponent_identity_census.py`, use its evidence classes as review triggers.

Do not merge identities from string similarity alone. Historical official names, renamed institutions, former athletic brands, and ambiguous abbreviations still require authoritative evidence and game-level context.

Before `RESEARCH_FROZEN`, there should be zero known/obvious current-program key splits and zero unresolved ambiguous current-program identity matches.

## 7. Neutral and postseason debt

Material neutral and non-NCAA postseason gaps may remain when genuinely unresolved, but
Stage 3A neutral debt must be challenged under the era-specific standard in
`docs/stage3a-regular-season-site-research.md`.

For regular-season neutral rows:

- first verify that an exact same-game canonical/accepted reciprocal lookup was performed;
- **1996-97 through present:** apply a strong exact-venue expectation and challenge
  tournament/event, host, opponent-institutional, reciprocal, and contemporary evidence
  before accepting unresolved debt;
- **1995-96 and earlier:** work the obvious recurring-event/site-family and other
  systematic high-yield evidence classes, then allow explicitly researched residual
  uncertainty after proportionate exhaustion. Surviving exact-building debt is historical
  enrichment debt and is not a publication blocker when explicitly accounted;
- a large or surprising modern neutral residual is a self-challenge trigger even if every
  row already has formal research-accounting metadata;
- do not reopen an older terminal neutral population merely because another archive might
  theoretically exist after the reasonable systematic paths are exhausted;
- preserve any already-supported exact venue when a game falls on the historical side of
  the 1996-97 cutoff; the cutoff changes unresolved research priority, not accepted facts.

For postseason:

- NCAA physical venue + city + state remains mandatory and non-waivable;
- published-vs-published neutral gaps require heightened reciprocal review;
- conference-tournament, NIT, and other postseason gaps must be explicitly
  researched/accounted rather than inherited silently from a sparse primary ledger.

The self-challenge must not turn ordinary regular-season `OPPONENT_HOME` building
blanks into source-school research debt.

## 8. No arbitrary numerical failure threshold

Large residual counts are review triggers, not automatic failures.

A century-old program may legitimately retain hundreds of researched unknowns. A much smaller number of modern UNKNOWN institutional games or stale current-program opponent identities may be more suspicious.

Do not invent generic rules such as “more than 100 UNKNOWN rows fails.” Instead require evidence-based self-challenge, era concentration, reciprocal review, current-registry comparison, explicit accounting, and the terminal-debt stopping rule above.

## 9. Required final self-challenge summary

Before final packaging, the Research lane should summarize the largest residual debt populations and any recoveries produced by the self-challenge.

At minimum, where applicable, report:

```text
PRE-FREEZE SELF-CHALLENGE: PASS

RESEARCHED_UNRESOLVED_HOME_VENUE:
  final count: <count>
  era concentration: <summary>
  recoveries/corrections during self-challenge: <count/summary>
  validation basis: <summary>

UNKNOWN H/A/N:
  final count: <count>
  era concentration: <summary>
  reciprocal recoveries during self-challenge: <count>
  residual basis: <summary>

UNKNOWN EXACT DATES:
  original/working count: <count>
  recovered: <count>
  final count: <count>
  residual era concentration: <summary>
  terminal-debt basis/systematic opportunities exhausted: <summary>

VENUES:
  local physical rows: <count>
  existing reuses: <count>
  genuinely new candidates: <count>
  ambiguous identities: 0
  modern neutral unresolved (1996-97+): <count>
  historical regular-season neutral venue debt (1995-96 and earlier): <count>

OPPONENT IDENTITIES:
  current-program key splits found/repaired: <count>
  ambiguous current-program matches: 0
  modern non-D1 identities specifically reviewed: <count>
```

If the self-challenge exposes a real defect, repair only the affected research fields, rerun the acceptance gate, regenerate affected hashes/manifest/ZIP, and supersede the prior package hash explicitly.

## 10. Final freeze boundary

Only after the self-challenge and any bounded repairs may the lane declare:

- research acceptance errors = 0;
- research acceptance warnings = 0;
- unresolved opponent identities = 0;
- known current-program opponent key splits = 0;
- ambiguous current-program identity matches = 0;
- HOME publication blockers = 0;
- NCAA site gaps = 0;
- unaccounted material site gaps = 0;
- ambiguous physical venue identities = 0;
- authoritative row-level Stage 3A state is present and mechanically reconciles to the Stage 1 universe;
- `PRE-FREEZE SELF-CHALLENGE: PASS`.

Then the lane may emit the immutable six-file ZIP/hash and declare:

```text
RESEARCH_FROZEN: YES
CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES
```

## 11. Owner communication

The self-challenge belongs to the Research lane and should not create another routine owner approval loop.

Once the owner has authorized research, perform the self-challenge autonomously within the bounded Stage 6 authorization. Contact the owner only if it exposes a genuine owner-level historical judgment or materially contradicts an owner-supplied assumption.

Under the bounded-stage protocol, a completed Stage 6 still stops before Stage 7. Within Stage 6 itself, however, the owner should not need to approve each repair batch or terminal-debt decision. Routine recoveries from the same class-level challenge should be batched before a durability checkpoint; do not return after one or two ordinary repairs merely because they were individually interesting. A healthy Stage 6 should require minimal owner steering.

## 12. Relationship to Implementation

The self-challenge strengthens Research Freeze; it does not replace serialized Implementation safeguards.

Implementation still must:

- verify the immutable ZIP/hash;
- rerun `research-check` under current-main tooling;
- perform current-main shared-reference rebase;
- recheck opponent identities that can drift as new programs/aliases are established;
- reject newly exposed research defects rather than silently absorb a replacement research project;
- independently enforce HOME exception and reciprocal-site preservation rules;
- continue through the sealed-plan and exact release workflow.

The intended defense stack is:

```text
research
-> mechanical research-check
-> adversarial research self-challenge
-> immutable RESEARCH_FROZEN package
-> serialized Implementation acceptance/rebase
```

The Control Center should therefore become exception supervision rather than a mandatory manual second research lane for every school.
