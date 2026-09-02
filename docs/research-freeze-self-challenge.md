# Research Freeze Self-Challenge

- **Status:** Required research-lane acceptance step
- **Applies to:** every school declaring `RESEARCH_FROZEN`
- **Purpose:** prevent mechanically accounted but insufficiently researched historical debt from entering the holster

A passing `research-check` is necessary but is not, by itself, sufficient for `RESEARCH_FROZEN`.

The permanent research acceptance gate can prove that required fields, vocabularies, opponent identities, NCAA sites, and research-accounting metadata are structurally valid. It cannot always prove that the researcher exhausted obvious authoritative evidence before labeling a historical fact unresolved.

Therefore every Research lane must perform one adversarial self-review before final freeze.

The governing question is:

> **If the Control Center challenged the largest unresolved/debt populations in this portfolio, what would it challenge?**

Investigate those populations before declaring `RESEARCH_FROZEN`, not after.

## 1. General rule

The self-challenge is a bounded final research audit, not an invitation to restart the school from scratch.

It should target the largest or most suspicious residual debt classes, especially:

- `RESEARCHED_UNRESOLVED_HOME_VENUE`;
- `UNKNOWN` H/A/N;
- substantial exact-date blanks;
- neutral/postseason site debt;
- physical-venue identity candidates;
- any modern or institutional series whose remaining unknowns are surprising relative to available reciprocal evidence.

The objective is not zero unknowns at all costs. The objective is to distinguish genuinely unrecoverable historical facts from debt that survived only because the primary source omitted a field or because an obvious reciprocal source was not checked.

Unsupported certainty remains worse than a researched unknown.

## 2. HOME venue self-challenge

If any `RESEARCHED_UNRESOLVED_HOME_VENUE` rows remain, the lane must report and validate:

- total count;
- season/decade concentration;
- home-facility era(s) involved;
- principal institutional, facility, archival, schedule, and reciprocal evidence checked;
- why the known facility chronology cannot safely assign a physical building at the individual-game level;
- confirmation that the population is not merely a broad primary-ledger venue blank carried forward under the exception.

A broad unexplored pre-arena era does not qualify merely because city/state are known.

If the self-challenge exposes a documented temporary home, alternate home, predecessor building, transition date, or reciprocal venue assertion, repair those rows before freeze.

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

## 5. Venue physical-identity self-challenge

Before freeze, reconcile local physical venue identities against the recorded `research_base_sha` well enough to report separately:

- total local physical venue rows;
- definite current-main physical reuses;
- genuinely new physical venue candidates;
- ambiguous physical-identity matches.

Do not equate “local venue row” with “new global venue.” Naming eras and aliases for the same building must not become duplicate physical identities.

Ambiguous physical-identity matches must be zero at `RESEARCH_FROZEN`.

Numeric global venue IDs remain provisional until serialized Implementation performs the authoritative current-main rebase.

## 6. Neutral and postseason debt

Material neutral and non-NCAA postseason gaps may remain when genuinely unresolved, but the lane should challenge large or modern populations before freeze.

In particular:

- NCAA physical venue + city + state remains mandatory and non-waivable;
- published-vs-published neutral gaps require heightened reciprocal review;
- conference-tournament, NIT, and other postseason gaps must be explicitly researched/accounted rather than inherited silently from a sparse primary ledger.

## 7. No arbitrary numerical failure threshold

Large residual counts are review triggers, not automatic failures.

A century-old program may legitimately retain hundreds of researched unknowns. A much smaller number of modern UNKNOWN institutional games may be more suspicious.

Do not invent generic rules such as “more than 100 UNKNOWN rows fails.” Instead require evidence-based self-challenge, era concentration, reciprocal review, and explicit accounting.

## 8. Required final self-challenge summary

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

VENUES:
  local physical rows: <count>
  existing reuses: <count>
  genuinely new candidates: <count>
  ambiguous identities: 0
```

If the self-challenge exposes a real defect, repair only the affected research fields, rerun the acceptance gate, regenerate affected hashes/manifest/ZIP, and supersede the prior package hash explicitly.

## 9. Final freeze boundary

Only after the self-challenge and any bounded repairs may the lane declare:

- research acceptance errors = 0;
- research acceptance warnings = 0;
- HOME publication blockers = 0;
- NCAA site gaps = 0;
- unaccounted material site gaps = 0;
- ambiguous physical venue identities = 0;
- `PRE-FREEZE SELF-CHALLENGE: PASS`.

Then the lane may emit the immutable six-file ZIP/hash and declare:

```text
RESEARCH_FROZEN: YES
CURRENT-MAIN REBASE REQUIRED BEFORE TRACKED PHASE 0: YES
```

## 10. Owner communication

The self-challenge belongs to the Research lane and should not create another routine owner approval loop.

Once the owner has authorized research, perform the self-challenge autonomously. Contact the owner only if it exposes a genuine owner-level historical judgment or materially contradicts an owner-supplied assumption.

A normal successful lane should research, self-challenge, repair if necessary, package, and then present one final `RESEARCH_FROZEN` status rather than asking the owner to say “continue” through each step.

## 11. Relationship to Implementation

The self-challenge strengthens Research Freeze; it does not replace serialized Implementation safeguards.

Implementation still must:

- verify the immutable ZIP/hash;
- rerun `research-check` under current-main tooling;
- perform current-main shared-reference rebase;
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
