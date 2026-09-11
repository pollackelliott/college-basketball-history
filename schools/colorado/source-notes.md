# Colorado men's basketball — source notes

## Research provenance

- Research base: `724c45e8d2d92a2a8cfc1e6174eeeb90de8bebda`
- Target scope: `INCEPTION+`

### Owner-supplied primary source

**Colorado men's basketball record book / media guide**

- Local source: `Colorado.pdf`
- SHA-256: `6b75185966296d1dce0d7f397f48527418520271386a06df8cf534e13c0e7ed4`
- Primary use: historical game universe through 2024-25, season records, literal opponent/site/event labels, H/A/N indicators, facility history, postseason history, and institutional notes.
- Literal game text is retained in `source-games.csv::raw_text`.
- Source typos or contradictions are not silently erased; accepted corrections are documented in `notes.md` and row notes.

### Owner-supplied Colorado-scope conference tournament reference

**Conference_Tournament_Site_Reference(20260907-201534).xlsm**

- SHA-256: `5fe2fb5659b6f4e0f37471b5893b860d07bc9113c9c16b1692aa78c9f434e79e`
- Authorization limit: the owner explicitly stated this workbook is incomplete globally and **must not be introduced as universal/global truth**.
- It is authorized for Colorado's own conference-membership history since at least the 1950s and was used only within that bounded Colorado scope.
- Pre-1950 conference postseason was independently challenged rather than inferred from workbook silence.
- That challenge found the March 1930 Rocky Mountain Conference championship playoff series but no conventional pre-1950 conference tournament.

### Completed 2025-26 supplement

**Colorado Athletics official 2025-26 schedule/results**

- URL: `https://cubuffs.com/sports/mens-basketball/schedule/2025-26`
- Competitive supplement: 33 games, 17-16.
- Grace College (Ind.) on 2025-10-19 is explicitly an exhibition and is excluded.
- The official schedule supplies H/A/N/location for the completed season and explicit OT metadata where the text-only schedule table omitted it.

## Research hierarchy used

1. Colorado institutional record book/media guide and Colorado Athletics current schedules/game notes.
2. NCAA official bracket/site evidence for NCAA Tournament date/round/site requirements.
3. Owner-authorized conference-tournament reference, only within Colorado's approved conference scope.
4. Opponent institutional schedules, record books, facility histories, and event/host records for reciprocal verification.
5. Archival/contemporary evidence when institutional sources were insufficient.

Unsupported inference was not used merely to fill a field.

## Important source-specific resolutions

- 1919 Colorado College impossible date corrected to February 28 from Colorado opponent history.
- 1920-21 Colorado College score order corrected to 36-32 from Colorado's official schedule.
- 1933 Kansas Teachers dates corrected using Pittsburg State reciprocal records.
- 1930 Rocky Mountain Conference title series independently researched and classified `POSTSEASON`, not `CONFERENCE_TOURNAMENT`.
- 1985 Big Eight quarterfinal at Iowa State corrected to opponent-home Hilton Coliseum.
- NCAA 1942/1954 dates corrected against official NCAA historical brackets.
- 2019 Arizona State game in Shanghai resolved to Baoshan Arena.
- Physical-venue aliases and naming eras are kept separate from H/A/N classification.

## Research-base identity handling

Research-lane numeric venue IDs are never treated as authoritative global IDs for new physical identities. Existing research-base physical venues are reused by established physical identity; new candidates use provisional `VEN-990xxx` transport IDs. Serialized Implementation must rebase all venue identities against then-current protected `main`.

Likewise, `rocky-mountain` and `mountain-states` are historically supported Colorado conference identities but are not yet in the research-base global conference registry; serialized Implementation must register/rebase them under current policy rather than substituting another conference.


## Stage 6 adversarial source challenge

The final pre-freeze challenge deliberately tested the largest remaining site debt, modern `NON_D1` identities, and provisional physical-venue identities against stronger reciprocal/institutional evidence.

### 1931 Kansas contradiction and bounded correction

Colorado's record-book rows label the Jan. 2-3, 1931 Kansas games as `vs. Kansas (Kansas City)`. Kansas Athletics' official 1930-31 schedule and opponent history instead identify both contests as **Kansas away games at Colorado in Denver**, with scores 34-25 and 36-28. The structured Colorado rows therefore become `SOURCE_PROGRAM_HOME`, Denver, Colorado; the Jan. 3 Colorado score is corrected from 29 to **28**. Literal Colorado `raw_text` remains unchanged.

No reviewed game-specific evidence established the exact Denver building. A period Colorado use of Temple of Youth Gym is not back-projected onto these Kansas games. The two rows therefore use the dedicated `RESEARCHED_UNRESOLVED_HOME_VENUE` status with complete Denver geography.

### Neutral-site building recoveries

Targeted institutional/reciprocal/event evidence recovered 12 of the 16 other previously unresolved neutral buildings:

- Sun Devil Gymnasium, Tempe — Seattle and Baylor, Dec. 17-18, 1965.
- The Pit / University Arena, Albuquerque — Washington State and Saint Joseph's, Dec. 19-20, 1969.
- Las Vegas Convention Center — Idaho State, Dec. 21, 1981.
- Denver Coliseum — Illinois, Dec. 30, 1987 Mile High Classic.
- Lahaina Civic Center — Utah State and Hawai'i, Dec. 8-9, 1989.
- Eugenio Guerra Sports Complex, Bayamón — Kentucky, Xavier, and American (P.R.), Nov. 26-28, 1998.
- Worthington Arena source wording for Boston University, Dec. 28, 1998; Montana State facility history establishes Worthington Arena as the basketball arena inside Brick Breeden Fieldhouse, so the physical venue reuses the research-base Brick Breeden Fieldhouse identity.

The American (P.R.) row is also corrected from Nov. 29 to **Nov. 28, 1998**, supported by Colorado's current official schedule and the event's Nov. 26-28 chronology.

### Residual site unknowns

Four neutral physical buildings remain unresolved after targeted review, with H/A/N and city/state established:

- Missouri — Denver, Dec. 22, 1936
- Utah — Denver, Dec. 23, 1936
- Missouri — Kansas City, Dec. 22, 1944
- Oklahoma State — Tulsa, Dec. 20, 1952

Institutional schedules/opponent histories establish the games and localities but do not establish exact buildings. Period arena chronology is not used as a substitute for game-specific evidence.

### Physical identity challenge

The post-challenge package has 69 local physical venue relationships: 56 research-base reuses and 13 genuinely new candidates. Research-base exact-name/key review did not expose a safe existing physical identity for the 13 provisional candidates. Ambiguous physical identities are zero.

The challenge specifically reconciled Worthington Arena to existing Brick Breeden Fieldhouse, reused research-base Las Vegas Convention Center and Eugenio Guerra Sports Complex, and continued to use `VEN-000208` for the Albuquerque Pit despite the research-base duplicate representation (`VEN-000427`). Research-time `VEN-990xxx` IDs remain provisional until serialized Implementation.

### Opponent identity challenge

The complete 71-identity / 237-game `NON_D1` population was approved by the owner in Stage 5 with no flags. Stage 6 separately challenged the 11 `NON_D1` identities represented in 2000-01 or later against the research-base current-D1 registry. None matches a current-D1 key. The accepted Stage 2 high-similarity/current-program overlap review also remains clean.

Final state: unresolved opponent identities 0; known current-program key splits 0; ambiguous current-program matches 0.
