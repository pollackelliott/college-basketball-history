# North Carolina men's basketball — source notes

## Research provenance

- Research base: `bb2fcf16dd8800e3d9b823c0b4999b2d1b516d6b`
- Target scope: `INCEPTION+`
- Controlling continuation state: verified North Carolina Stage 1–3B checkpoint chain culminating in `north_carolina_stage3B_COMPLETE_2026-09-10.zip` / verified outer continuation package.

## Primary institutional game-universe sources

**UNC All-Time Scores (2014-15 record book)**  
`https://goheels.com/documents/download/2015/6/8/AllTimeScores.pdf`

Primary row-level historical source for 1910-11 through 2014-15, with narrow source-version corrections documented in Stage 1.

**UNC 2025-26 Men's Basketball Record Book**  
`https://goheels.com/documents/download/2025/10/28/25-26_M-Basketball_Record_Book.pdf`

Current institutional control for historical corrections, recent detailed results, home arenas, neutral-site/venue ledgers, postseason results, and accomplishment context.

**UNC official 2025-26 schedule**  
`https://goheels.com/sports/mens-basketball/schedule/text/2025-26`

Completed-season supplement: 33 competitive games, 24-9. Preseason/exhibition rows excluded.

Field-specific schedule controls were also used for 2012-13, 2017-18, and 2024-25 where the older row-level source contained a date/result/source-version defect.

## Site and venue research

Stage 3A combined UNC's official site legend, Home Arenas chronology, city-specific venue ledgers, official game/event material, research-base physical venue identities, and targeted reciprocal/institutional evidence. Venue identity never established H/A/N; H/A/N remained independently sourced.

Ten early/historical regular-season neutral rows retain exact-building uncertainty after targeted research. Every one has complete city/state and explicit `RESEARCHED_UNRESOLVED` accounting in `source-games.csv`.

Notable targeted evidence includes:

- UNC current Virginia Tech history for the 1919 Roanoke City Auditorium game;
- UNC current record book and official event evidence for Japanese, Puerto Rico, Maui/Atlantis and other neutral-site games;
- institutional/reciprocal evidence for historical domestic neutral venues;
- global project venue registry at the recorded research base for established physical identities.

## Conference tournament source authorization

The owner-supplied conference-tournament site workbook is explicitly authorized as complete for **North Carolina's own historical conference membership**. It is incomplete globally and must not be introduced as universal/global truth. Stage 3B used it only inside this North Carolina lane and cross-checked physical identity and H/A/N independently where appropriate.

Conference tournament population: 234 games — 70 Southern Conference and 164 ACC.

## NCAA Tournament

UNC's institutional NCAA results/history and NCAA/venue evidence close all 186 NCAA Tournament rows. Every NCAA row has exact physical venue + city/state. Historical true opponent-home cases remain opponent-home rather than being forced neutral by tournament status.

## NIT

UNC's current NIT ledger plus official contemporary releases/box scores close all 18 NIT games, including 2003 Smith Center home rounds, the 2010 Carmichael home opener, 2010 Mississippi State/UAB opponent-home rounds, and Madison Square Garden semifinal/championship rounds.

## Conference/accomplishment sources

UNC official conference history identifies the institution as an SIAA charter member (1894), Southern Conference charter member (1921), and ACC charter member (1953; competition beginning 1953-54). Current UNC men's basketball material states the 2024 ACC regular-season title was UNC's 33rd ACC regular-season championship and 40th overall regular-season conference championship when seven Southern Conference first-place finishes are included.

The game ledger independently reproduces 26 conference-tournament title wins, 55 NCAA appearance seasons, 21 Final Four seasons, and six NCAA championship wins.

## Preservation rule

Literal opponent labels, source site tokens, source result text, and raw game text remain preserved in `source-games.csv`. Curated fields encode accepted research conclusions without erasing conflicting/stale literal evidence. Unsupported inference was not used merely to fill a field.


## Stage 6 self-challenge evidence

The final pre-freeze audit rechecked the 10 researched-unresolved neutral-building rows as a class, modern/non-current opponent identities, current-registry drift since `research_base_sha`, and physical-venue reuse/candidate risk.

Authoritative/primary evidence added during the audit includes:

- **Clark County Assessor — parcel 162-19-402-001**, 4500 W Tropicana Ave: `City/Unincorporated Town = PARADISE`. This corrects the canonical physical locality of Orleans Arena to Paradise, Nevada under the repository's recurring venue-jurisdiction convention while preserving school/event `Las Vegas` shorthand in literal source evidence.
- **Virginia Athletics official all-time results**: 1915-16 entry `F7 North Carolina N1 W 30 24`. This confirms the neutral Virginia matchup but conflicts with UNC's controlling 25-29 source score. The conflict is preserved rather than adjudicated silently.
- **Virginia Tech Athletics official box-score archive**: North Carolina 46-25 at Winston-Salem, dated 1940-01-10. UNC's controlling source dates the same game 1940-01-11. The date conflict is preserved; neither source identifies the building.
- **Washington and Lee official opponent history / 1953-54 schedule**: independently confirms North Carolina's 1954-02-02 neutral game at Lynchburg, Virginia, but supplies no building.
- **Xavier 1950-51 schedule history**: confirms the 1950-12-22 North Carolina neutral game and score while supplying no physical venue.
- **Eastern Kentucky official series note**: confirms the single 1950-51 meeting and 85-62 result; no game-specific Pikeville building is identified in the available institutional evidence.
- **Davidson historical factbook** and targeted historical schedule material: corroborate the Winston-Salem neutral context for the 1941 North Carolina game without identifying a defensible building.
- **Greensboro History Museum archival material**: corroborates Basic Training Center #10 / wartime Greensboro installation context but not the exact basketball building.

After these checks, no additional systematic evidence class was identified that would safely assign any of the 10 residual buildings. They remain terminal researched historical debt, not unexplored blanks.

The owner-approved Stage 5 `NON_D1` disposition remains controlling. The only 2000s+ non-current opponent identities in the package are Chaminade and Saint Francis (PA) source variants: Chaminade remains NCAA Division II, while Saint Francis began its NCAA Division III transition for 2026-27. No current-D1 key split is created by either identity.

Current-main drift note: Colorado integration added a separate `Coliseo de Puerto Rico` global venue row after the North Carolina research base, although North Carolina had already reconciled that physical building to research-base `VEN-000471` José Miguel Agrelot Coliseum. North Carolina retains the research-base physical identity; serialized Implementation must resolve any then-current global-reference duplication during rebase.
