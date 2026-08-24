# Michigan source notes

## Source hierarchy and coverage

### 1. Michigan men's basketball record book — owner-supplied PDF

- File: `michigan record book.pdf`
- Publisher: University of Michigan Athletics
- Edition/context: 2026 record book supplied in this research lane
- Relevant PDF pages: PDF pages 82-99 (printed History & Records pages 17-34) for the complete season-by-season ledger
- Coverage used: 1908-09 through completed 2025-26
- Facts used:
  - one dated ledger row per scheduled contest;
  - game-level H/A/N notation;
  - on-court scores and W/L;
  - overtime notation;
  - season-level home arena chronology;
  - regular-season special-event site footnotes;
  - NCAA/NIT postseason identification and site footnotes;
  - Big Ten Tournament game history;
  - NCAA-sanction asterisk legend;
  - Wisconsin W-FF explanatory footnotes;
  - season records and accomplishments as QA evidence.
- Limitations / handling:
  - 11 cancellation/postponement entries are present in the dated ledger but are not played games and are excluded;
  - early score layout is not assumed to be Michigan-score-first; W/L plus signed margin controls orientation;
  - aggregate H/A/N totals do not exactly match the explicit game-level ledger, so explicit game-level site evidence controls;
  - source venue wording sometimes uses historical arena names or a complex name rather than the physical arena's current project display.

The owner-supplied PDF itself is the primary game-by-game source. No manual 2025-26 schedule supplementation was required because
the record book contains the complete 2025-26 championship season.

### 2. Big Ten conference-tournament site index — owner-supplied workbook

- File: `Conference_Tournament_Site_Reference(6).xlsm`
- Authorized scope for Michigan: **Big Ten section only**
- Status: owner explicitly states the workbook is incomplete globally, but the Big Ten section is complete and authorized for Michigan.
- Facts used:
  - Big Ten Tournament shared physical venue, city, and state by tournament year from 1998 through 2026.
- Not used for:
  - any non-Big Ten conference;
  - game inclusion;
  - opponent identity;
  - H/A/N classification.

H/A/N remains controlled by Michigan's game-level source notation even when the workbook supplies the tournament venue.

## Supplemental physical-venue research

These sources were used only to identify physical buildings / historical aliases, not to override Michigan game-level H/A/N.

### Yost Field House

University of Michigan Athletics, Yost Ice Arena history:
https://mgoblue.com/sports/2017/6/16/facilities-yost-arena-html

Used to corroborate that Yost Field House was dedicated in 1923, hosted Michigan basketball beginning in January 1924,
and remained the basketball home through March 1967.

### Frost Bank Center / AT&T Center

San Antonio Spurs, arena naming announcement:
https://www.nba.com/spurs/news/san-antonio-spurs-arena-is-now-officially-the-frost-bank-center

Used to establish that the physical San Antonio arena called `AT&T Center` in Michigan's 2022 NCAA source was renamed
`Frost Bank Center` in 2023.

### Beasley Coliseum

Washington State Athletics facility history:
https://wsucougars.com/sports/2013/4/18/208262914

Used to establish the 1973 Performing Arts Coliseum / Wallis Beasley physical building and its Beasley Coliseum identity.

### Kansas Coliseum / Britt Brown Arena

Sedgwick County Kansas Coliseum program information:
https://www.sedgwickcounty.org/media/27370/kansas_pavilions.pdf

Used to establish that Britt Brown Arena was the main arena within the Kansas Coliseum complex. Michigan's 1994 NCAA
source wording `Kansas Coliseum` is preserved in `source_venue_name`.

### Portland Memorial Coliseum / Veterans Memorial Coliseum

City of Portland memorial history:
https://www.portland.gov/veteransmemorial/memorialhistory

Used to establish that the Portland building opened in 1960 as `Memorial Coliseum` and is the same physical building now
known as `Veterans Memorial Coliseum`.

## Repository/reference authority used

Repository:
https://github.com/pollackelliott/college-basketball-history

Research base SHA:
`4c8d75592f98b42a8534182a5af9bf240b1fd16c`

Current-main repository documentation and reference registries at that SHA were used for:

- six-file schema;
- current program keys;
- current-D1 flags;
- stable conference identity;
- existing physical venue IDs, keys, display names, and aliases;
- controlled game-type and postseason-round taxonomy.

No repository writes, onboarding branch, canonical preflight, apply, release, or publication occurred in this research lane.

## Source fidelity rules applied

- Raw ledger text is preserved on every source-game row.
- Unknown information is not inferred.
- Venue chronology never establishes H/A/N.
- Source wording and canonical physical identity are kept separate.
- Administrative actions never replace the on-court score/result.
- Regular-season event names remain provenance rather than new public game types.
