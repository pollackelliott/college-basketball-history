# Maryland source notes

## Primary institutional source

**Maryland Men's Basketball 2025-26 Record Book** (owner-supplied PDF: `2025-26_MBB_Record_Book(2).pdf`).

- SHA-256: `219b5eabc5783d6d1d62e16f5812d79a8a229422dffffad1b1e287da89167e14`
- Updated by Maryland: September 22, 2025
- Historical ledger backbone: All-Time Results, printed pp. 55-64
- Cross-check sections: year-by-year results, Arena History, all-time series, regular-season tournaments, Conference Tournament History, NCAA Tournament History
- Historical coverage used: official varsity history through completed 2024-25

The All-Time Results ledger controls the row-level chronology unless a stronger Maryland game-specific/postseason section resolves a documented issue. Literal source evidence is retained in `raw_text`; curated normalization does not overwrite the source claim.

The record book explicitly labels 1904-05 an intramural/club season before the first official varsity team. Those two non-varsity contests are outside the competitive package. The official varsity ledger begins in 1910-11.

## Completed 2025-26 supplement

Maryland Athletics official completed schedule/results:

https://umterps.com/sports/mens-basketball/schedule/2025-26

Text schedule:

https://umterps.com/sports/mens-basketball/schedule/text/2025-26

Official nonconference schedule announcement:

https://umterps.com/news/2025/7/28/mens-basketball-mens-basketball-announces-2025-26-non-conference-schedule

The completed season supplies **33 competitive games and a 12-21 record**: 7-8 home, 2-10 away, 3-3 neutral. The Oct. 27 UMBC game is explicitly an exhibition and excluded.

The nonconference announcement supplies physical venue evidence for the 2025-26 opener at CFG Bank Arena, the Marquette trip to Fiserv Forum, the Players Era games at MGM Grand Garden Arena, Maryland home games at XFINITY Center, and the Virginia trip to John Paul Jones Arena. The official schedule identifies the 2026 Big Ten Tournament at United Center in Chicago.

## Owner-supplied conference-tournament site reference

File: **`Conference_Tournament_Site_Reference(20260825-203717).xlsm`**

- SHA-256: `68fd42a5da4e2a908a9911c5812fda317920e1842b5518ebba52d20cdd2b26e2`
- Owner ruling: globally incomplete and not universal canon.
- Maryland authorization: the **Southern Conference, ACC, and Big Ten** sections are complete and reliable for Maryland and are affirmatively used.
- Use: physical venue/city/state assignment for Maryland conference-tournament rows.
- Safety rule: tournament venue/location never independently establishes H/A/N.

The workbook is not promoted beyond those owner-authorized Maryland-relevant sections.

## NCAA Tournament site evidence

Maryland's dedicated NCAA Tournament History and all-time-results footnotes provide game-level tournament site evidence for the program's 76 NCAA games through 2025. Site normalization was completed before research freeze, producing **76/76 rows with venue/city/state**.

Historical source names are retained as aliases where the project-facing physical identity is normalized, including:
- MCI Center / Verizon Center -> Capital One Arena
- Conseco Fieldhouse / Bankers Life Fieldhouse -> Gainbridge Fieldhouse
- Carrier Dome -> JMA Wireless Dome
- BSU Pavilion -> ExtraMile Arena
- Arrowhead Pond of Anaheim -> Honda Center
- Gaylord Entertainment Center -> Bridgestone Arena
- HSBC Center -> KeyBank Center
- Jacksonville Veterans Memorial Arena -> VyStar Veterans Memorial Arena
- Pepsi Center -> Ball Arena
- Sprint Center -> T-Mobile Center
- Baltimore Arena / Royal Farms Arena -> current CFG Bank Arena physical identity

The source's 1958 Madison Square Garden site is kept physically distinct as Madison Square Garden III. Charlotte Coliseum source wording is likewise separated into the 1955 and 1988 physical buildings.


## Maryland official historical schedule reconciliation

Maryland Athletics' current official historical schedule pages were used as secondary institutional evidence when the record-book ledger, its aggregate H/A/N summary, or the initial multi-column extraction conflicted.

Representative pages used:

- https://umterps.com/sports/mens-basketball/schedule/1936-37
- https://umterps.com/sports/mens-basketball/schedule/1938-39
- https://umterps.com/sports/mens-basketball/schedule/1943-44
- https://umterps.com/sports/mens-basketball/schedule/1948-49
- https://umterps.com/sports/mens-basketball/schedule/1950-51
- https://umterps.com/sports/mens-basketball/schedule/1959-60
- https://umterps.com/sports/mens-basketball/schedule/1964-65
- https://umterps.com/sports/mens-basketball/schedule/1973-74
- https://umterps.com/sports/mens-basketball/schedule/1974-75
- https://umterps.com/sports/mens-basketball/schedule/1978-79
- https://umterps.com/sports/mens-basketball/schedule/1983-84
- https://umterps.com/sports/mens-basketball/schedule/1993-94
- https://umterps.com/sports/mens-basketball/schedule/1997-98
- https://umterps.com/sports/mens-basketball/schedule/2000-01
- https://umterps.com/sports/mens-basketball/schedule/2006-07
- https://umterps.com/sports/mens-basketball/schedule/2007-08
- https://umterps.com/sports/mens-basketball/schedule/2021-22
- https://umterps.com/sports/mens-basketball/schedule/2022-23

Two contemporary Maryland records resolve internally impossible printed lines: the 2008 Virginia Tech recap confirms Maryland lost 65-69, and the 2023 Michigan State recap confirms Maryland lost 58-63. The official 2021-22 schedule also identifies the missing Jan. 12 Northwestern game that replaced an extraction-duplicated Old Dominion row.

The detailed Maryland schedule is treated as stronger game-level site evidence than a conflicting aggregate H/A/N count. Geography itself is never used to infer site.

## Additional venue identity evidence

The record-book footnote for the 1949 Davidson game places the contest at Memorial Gymnasium in Charlottesville, Virginia. University of Virginia historical facility evidence identifies that building as Virginia's Memorial Gymnasium, opened in 1924 and used by Virginia basketball before University Hall. The package therefore creates a distinct research-time physical identity, **Memorial Gymnasium (Virginia)**, rather than collapsing it into the unrelated Memorial Gymnasium in El Paso, Texas.

## NIT evidence

NIT classification comes from Maryland's year-by-year postseason summaries and all-time-results footnotes. The package contains 21 NIT games. The 1972 Niagara game is the verified NIT championship and uses `Championship`; other NIT rounds remain blank.

## Opponent identity method

Every source opponent label resolves in `opponents.csv`. Current Division I programs use project-style canonical program identities; historical/local/military/YMCA opponents remain distinct unless institutional lineage is supported.

Notable normalizations include:
- Memphis State -> Memphis
- New Mexico A&M -> New Mexico State
- Western Maryland -> McDaniel
- Biscayne -> historical St. Thomas University (Florida) lineage, distinct from current D1 St. Thomas (Minnesota)
- Long Island / LIU-Brooklyn -> LIU lineage
- Missouri-Kansas City -> Kansas City
- IUPUI -> IU Indianapolis lineage
- St. Francis / Saint Francis -> Saint Francis (Pa.) based on Maryland's own series/event context

No opponent identity remains unresolved.

## Early-history limitations

The early ledger omits exact dates for 52 competitive games. Those remain blank. Modern online historical schedule pages can contain apparent placeholder dates for some early seasons, so they are not used to manufacture precision absent from the record book.

The 1913-14 season has eleven losses without printed scores, and the 1944 Woodrow General Hospital loss also lacks a score. These rows preserve known played result with both score fields blank.


## Final source-level QA

Manual research-frozen QA was run after reconciliation. Results:

- exactly six required flat files;
- 2,875 non-exhibition competitive source rows;
- 2,875 nonblank unique `source_game_id` values;
- valid consecutive season labels and valid known ISO dates;
- score atomicity PASS and score/result consistency PASS;
- 0 unresolved opponent rows;
- H/A/N vocabulary PASS;
- game-type vocabulary PASS;
- city/state atomicity PASS;
- every curated venue represented in `venues.csv`;
- 76/76 NCAA Tournament rows have curated venue, city, and state;
- populated NCAA rounds use only controlled vocabulary;
- no exhibition/scrimmage row remains in the competitive package.

The repository executable `tools/onboarding_hardening.py research-check` could not be run in this environment because the repository is not locally mounted and outbound Git access from the execution container is unavailable. The serialized Implementation lane must run it immediately on receipt, before Phase 0.

## Research baseline

`research_base_sha=2899c45e7b8dc2b8553c8b9e2342715a9a091484`

Shared/global numeric venue IDs in this package are research-time provisional identifiers only. Physical venue name, aliases, geography, chronology, and source basis are the durable research facts.
