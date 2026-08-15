# Minnesota curation notes

## 1. Program status and coverage

Minnesota is curated from its first recognized program season, 1895-96,
through the completed 2025-26 season.

The package contains **3,081 recognized non-exhibition varsity games**
with an on-record result of **1,746-1,333-2**.

The owner-confirmed history boundary is 1895-96 with status
`OWNER_CONFIRMED` and basis `ALWAYS_TOP_LEVEL_FROM_INCEPTION`.

## 2. Conference chronology

- No conference: 1895-96 through 1904-05.
- Big Ten: 1905-06 to present.

## 3. Minnesota home-venue chronology

- University Armory: program inception through February 1, 1925.
- Kenwood Armory: February 2, 1925 through February 3, 1928.
- Williams Arena: February 4, 1928 to present.

## 4. Exhibition policy

Nine exhibitions are excluded from the canonical competitive-game package,
including both exhibitions from the completed 2025-26 schedule.

## 5. Historical-source treatment

The reconciled extraction is gated against Minnesota's season-by-season
records. The NCAA-sanction era from 1993-94 through 1998-99 uses Minnesota's
official chronology with a score/result supplement because the official guide
suppresses those game scores. Seven chronology/supplement date disagreements
are intentionally retained for reconciliation rather than silently resolved.

## Game-type classification

Minnesota uses the project-wide game-type taxonomy:

- Regular-season invitationals, classics, showcases, neutral-site events, and other in-season tournaments remain `REGULAR_SEASON`.
- Big Ten Tournament games are `CONFERENCE_TOURNAMENT`.
- NCAA Tournament games are `NCAA_TOURNAMENT`.
- NIT games are `NIT`.
- Other true postseason tournaments use the generic `POSTSEASON` type. Minnesota's 2025-26 College Basketball Crown game is the first such case.

The specific tournament name may remain in source/event metadata without becoming a new public game-type category.

## Source score corrections

Two internally inconsistent score rows in the 2025-26 Minnesota media guide
are preserved verbatim in `raw_text` but corrected in the curated score fields.

- 2006-03-21 at Cincinnati (NIT): the year-by-year row prints `L 76-62`;
  Minnesota's dedicated NIT history and opponent-series history give
  Cincinnati 76, Minnesota 62. Curated result: Minnesota L 62-76.
- 2014-11-14 vs. Louisville: the year-by-year row prints `L 68-61`;
  Minnesota's official game recap gives Louisville 81, Minnesota 68.
  Curated result: Minnesota L 68-81.

## Series-record supplements discovered during reconciliation

Cross-source reconciliation after the initial Minnesota ingestion established
two additional recognized varsity games against Northwestern that are omitted
from Minnesota's chronological year-by-year ledger but corroborated elsewhere.

- 1911-03-07: Minnesota defeated Northwestern 33-3 at Minnesota.
  Minnesota's Series Records confirms the 33-3 home win but prints 2/10/1911,
  a date already occupied by Minnesota's 37-7 win over Iowa. Northwestern's
  historical record supplies 3/7/1911 and L 3-33 at Minnesota.
- 1915-03-12: Minnesota defeated Northwestern 13-12 at Minnesota.
  Minnesota's Series Records confirms the 13-12 home win but prints 2/13/1915,
  a date already occupied by Minnesota's 11-10 win at Iowa. Northwestern's
  historical record and contemporary newspaper evidence support 3/12/1915.

The two rows are additive source supplements; the media guide's original
chronological text remains preserved unchanged. With these supplements, the
Minnesota source package contains 3,083 competitive games and an on-court
record of 1,748-1,333-2.
