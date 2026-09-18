# Utah men's basketball — source notes

## Research provenance

- Research base: `e5078cd6b57d68f59048f32b7dace422544eff9f`
- Target scope: `INCEPTION+`

### Owner-supplied primary source

**Utah 2025-26 men's basketball record book**

- Local source: `2025-26_MBB_Record_Book(3).pdf`
- SHA-256: `4365e217b130e98d6c98a9a738f6b8901143c5f72419fe1ab7751c261fbf20d7`
- Primary use: historical game universe through 2024-25, literal game rows, season records,
  opponent series, conference chronology, home/site indicators, facility and postseason evidence.
- Literal game text is retained in `source-games.csv::raw_text`.
- Demonstrable source defects are corrected only in curated fields and documented in `notes.md`.

### Original owner-supplied conference-tournament guide

- Local source: `ct venues.xlsm - Tournament Sites(3).csv`
- SHA-256: `3be778aa54f79cf66417f01fe3d68bbbbe4d0545e2dc664bf1b038b796a42dca`
- Owner authorization: complete/reliable for Utah beginning with its Mountain West era;
  earlier rows were research evidence, not automatic truth.

### Expanded WAC workbook supplied 2026-09-14

- Local source: `Ct venues 9 14.csv`
- SHA-256: `1fa2031019354c548d8e772ae6f299a440f5d7be0a34f22abe602050cdd28e96`
- Use: additional WAC tournament-site cross-check.
- Result: 1985-86 through 1998-99 materially corroborates the accepted Utah Stage 3B site history.
- Important limitation: the workbook's 1983-84 and 1984-85 `entire tournament at shared venue`
  representation is too coarse for Utah. Stronger Utah row-level/reciprocal evidence establishes:
  - 1984: Hawaii in Salt Lake City, then New Mexico in Albuquerque.
  - 1985: Wyoming and Air Force in Salt Lake City, then UTEP in El Paso.
  Those row-level conclusions control; the workbook was not allowed to flatten these early rounds.

### Completed 2025-26 supplement

**Utah Athletics official 2025-26 schedule/results**

- Competitive supplement: 32 games, 10-22.
- Nevada (2025-10-17) and at Oregon (2025-10-24) are exhibitions and are excluded.
- Official cumulative statistics support one overtime vs Weber State on 2025-11-08.

## Source hierarchy

1. Utah institutional record book / current Utah Athletics schedules and statistics.
2. NCAA archival/site evidence for NCAA requirements.
3. Owner-authorized Utah conference-tournament reference within its authorized scope.
4. Opponent institutional schedules, histories, venue records, and event/host material.
5. Contemporary archival reporting when institutional evidence remained contradictory or incomplete.

Unsupported geography or venue inference is not used merely to fill a field.

## Stage 4 contradiction repairs

### 1960 NCAA first round: USC

Utah's record book prints `03/08 vs. USC` and gives `Nielsen Field House` in Provo.
That venue-name normalization was physically impossible because Einar Nielsen Fieldhouse is
Utah's Salt Lake City building.

Stage 4 reciprocal/contemporary review establishes the contest on **Monday 1960-03-07** at
**George Albert Smith Fieldhouse / Smith Fieldhouse in Provo**. Research-base global venue
identity is `VEN-000382 / smith-fieldhouse`. The package therefore normalizes date and
physical venue while preserving Utah's literal `03/08`, `Nielsen Field House`, and raw row.

### 1961 Skyline championship playoff: Colorado State

Utah's literal postseason site line again says `Nielsen Field House` in Provo.
Colorado State reciprocal history confirms the neutral 1961-03-11 game in Provo, while
contemporary reporting places the playoff at Brigham Young University's field house.
The package therefore normalizes the physical building to **Smith Fieldhouse**
(`VEN-000382`) and leaves the date unchanged. Literal Utah wording is preserved.

## Other important source resolutions

- Brigham Young College / BY College remains a distinct historical Logan institution and is not BYU.
- `Weber` is the predecessor name of present Weber State and is normalized to `weber-state`.
- Utah's 1998 `St. Francis (N.J.)` year-by-year parenthetical is reconciled to Saint Francis (PA)
  using Utah's own opponent-series entry for the same game.
- Stage 1's duplicated 2025 UCF Crown row is corrected to the actual Butler game.
- 2013-16 Utah Pac-12 Tournament games are physically at MGM Grand Garden Arena despite the
  current Utah year-by-year table printing T-Mobile Arena.

## Research-base identity handling

Research-time numeric venue IDs are transport provenance, not authoritative current-main IDs.
Existing research-base physical identities are reused when established. Five genuinely new
physical candidates use provisional `VEN-990xxx` IDs and require current-main reconciliation
during serialized Implementation.

The `State` conference label is preserved exactly because the Utah source does not support
silently expanding it into a more specific formal name. The proposed key `state-utah` is a
research-local transport identity pending current-main reference registration/reconciliation.


## Stage 6 adversarial source challenge

The final self-challenge targeted the modern neutral-site debt and the two narrow HOME-venue
exception eras. Literal Utah source rows remain preserved; stronger reciprocal/event evidence
was used field-specifically.

High-yield official/institutional evidence classes used include:

- Utah Athletics 2005 Washington State recap/box: Utah visitor at Washington State's KeyArena home game.
- Kansas Athletics 2014 Utah notes: Kansas "plays host" to Utah at Sprint Center; current physical identity T-Mobile Center.
- Arizona Athletics Wooden Classic history: 1996 Utah game at Arrowhead Pond of Anaheim.
- Utah Athletics Wooden Classic release: 2000 Utah-USC at Arrowhead Pond of Anaheim.
- Contemporary Deseret News Great Eight announcement and Utah Athletics series notes: United Center for the 1997/1998 Great Eight games.
- Utah Athletics Maui event/box-score material: Lahaina Civic Center for the Utah Maui populations.
- Kansas Athletics series history: 1995 Utah-Kansas at Kemper Arena.
- Miami (Ohio) Athletics 2000 Puerto Rico Shootout notes: event arena Eugene Guerra Sports Complex in Bayamón; normalized to the established Eugenio Guerra Sports Complex physical identity.
- Utah Athletics 2001 Southwest Showdown: America West Arena; current project physical identity Mortgage Matchup Center / Footprint Center.
- Utah Athletics 2003 Preseason NIT notes: Madison Square Garden for the semifinal/consolation population.
- Utah Athletics 2004 Great Alaska Shootout notes: Sullivan Arena.
- Utah Athletics 2006 San Juan Shootout material: Mario Morales Coliseum, Guaynabo.
- Utah Athletics 2007 NIT Season Tip-Off notes: Bank of America Arena; same physical building as Hec Edmundson Pavilion.
- Utah Athletics 2008 Glenn Wilkes Classic notes: Ocean Center.
- Utah Athletics 2009 Las Vegas Invitational material: Orleans Arena.
- Utah Athletics 2010 Diamond Head Classic material: Stan Sheriff Center.
- Utah Athletics 2011 Battle 4 Atlantis notes: Imperial Arena.
- Utah Athletics 2015 Duke recap/schedule: Madison Square Garden.
- Utah Athletics 2017 MGM Resorts Main Event material: T-Mobile Arena.
- Utah Athletics 2017 Beehive Classic material: Vivint Smart Home Arena; same physical building as Delta Center.

The HOME-venue challenge reviewed University institutional history of Einar Nielsen Fieldhouse,
including its 1939/1940 opening/dedication and WWII Army-housing use, plus Utah Athletics'
first/last-game chronology. That evidence validates the established chronology but does not
safely resolve every individual 1908-10 or 1946-48 transition row. Those rows therefore remain
explicit historical-unrecoverable venue findings rather than inferred assignments.
