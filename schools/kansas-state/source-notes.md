# Kansas State source notes

## Primary Kansas State source

The supplied **2025-26 Kansas State Men's Basketball Media Guide** (`Kstate.pdf`) is the primary institutional source for the year-by-year competitive ledger, annual season totals, conference chronology, home-facility history, conference-tournament history, NCAA/NIT history, opponent series, and historical notes.

The detailed year-by-year section was mechanically extracted and then reconciled season-by-season. Source defects are documented rather than silently trusted.

## Current-season and omitted-season supplementation

Kansas State's official completed 2025-26 schedule supplies the completed current season. The supplied media guide explicitly labels the Oct. 24 Missouri and Oct. 31 Newman games as exhibitions; both are excluded from the competitive package.

Kansas State's official archived 1999-00 schedule restores the 28-game season omitted from the media guide's detailed year-by-year sequence and independently agrees with the media guide's 9-19 annual line.

Official Kansas State schedule/opponent-history/recap evidence was also used narrowly for bounded score/date corrections and exact-date recovery where the supplied guide is defective.

Relevant official pages used during research include:
- https://www.kstatesports.com/sports/mens-basketball/schedule/2025-26
- https://www.kstatesports.com/sports/mens-basketball/schedule/text/1999-00

## Owner-authorized conference-tournament site reference

The supplied `Conference_Tournament_Site_Reference(20260906-180626).xlsm` was explicitly authorized by the owner as complete for **Kansas State's historical conference membership only**. It is used only in this Kansas State research lane and must not be promoted as universal canonical truth.

Game-level application preserves split-site tournament years. In the 1976-77 through 1984-85 period, campus opening rounds are treated separately from the Kansas City semifinal/final site rather than assigning one tournament venue to every game.

## Opponent identity research

Stage 2 normalizes historical aliases, predecessor/successor identities, current-program renames, branch/campus distinctions, and parsing/ranking residue while preserving literal source labels separately.

Reciprocal institutional and authoritative historical evidence was used narrowly where labels could plausibly collapse to the wrong current program. The working NON_D1 population was researched before owner review; the owner sanity scan remains pending.

## H/A/N and physical venues

H/A/N is established from game-level notation, Kansas State schedule/opponent-history evidence, and bounded accepted reconciliation. Physical venue identity is researched independently and is never used to infer H/A/N.

Kansas State institutional facility history supports the principal home chronology and establishes that pre-Nichols Manhattan home games used multiple buildings. Those 43 early HOME rows therefore retain Manhattan, KS with `RESEARCHED_UNRESOLVED_HOME_VENUE` rather than receiving an invented building.

Regular-season away venue completeness is not treated as a research-freeze requirement when no accepted venue evidence exists.

## Postseason

Kansas State's NCAA year-by-year postseason table and related institutional postseason material are the primary source for NCAA game classifications, rounds, cities, and physical venues. NCAA completeness is mandatory and closes at 76/76 venue/city/state-complete rows.

Conference-tournament sites combine Kansas State game/tournament evidence with the owner-authorized tournament-site reference. NIT sites use Kansas State postseason/schedule evidence and reciprocal/venue evidence where needed.

The 2014 NCAA Kentucky game's package date is corrected to 2014-03-21 from Kansas State's official box score and postseason table; the accepted Stage 1 identity is unchanged.

## Stage 4 research-base venue reconciliation

The research package was reconciled against the pinned research-base physical venue registry at `de0c67405881b7be716c93ecb46f6ae2ea8e29ca`. Existing physical identities are reused where deterministic; only six physical identities remain research-time new with blank numeric IDs.

One narrow Stage 4 identity check was required by registry reconciliation:
- TCU Athletics identifies Schollmaier Arena as the same physical facility previously known as Daniel-Meyer Coliseum, renovated before the 2015-16 season: https://gofrogs.com/sports/2018/7/13/facilities-tcu-facilities-basketball-html

This check changes only the research-package physical venue identity/name normalization; it does not reopen the accepted game universe, opponent identity, or H/A/N classification.

### Stage 4 date validation repair

Package validation rejected the guide token `F29` for the 1921-22 home loss to Drake because 1922 had no February 29. Kansas State's official 1921-22 schedule and official Drake opponent-history page both identify the 23-32 home loss as **March 1, 1922**. The package therefore uses `1922-03-01` while preserving the literal `F29` source token in `raw_text`.

Relevant official pages:
- https://www.kstatesports.com/sports/mens-basketball/schedule/1921-22
- https://www.kstatesports.com/sports/mbball/opponent-history/drake/18

## IMPLEMENTATION-DISCOVERED SOURCE-UNIVERSE CORRECTION — 1907 KANSAS

Restored source_game_id `kansas-state-reopen-1907-01-25-kansas` after current
protected-main reciprocal evidence exposed a research-universe omission.

Evidence:
- K-State 2025-26 series history: first Kansas meeting Jan. 25, 1907; road
  loss 39-54.
- Kansas current institutional game history: Jan. 25, 1907 in Lawrence,
  Kansas 54, Kansas State 39.
- Existing reciprocal assertion: `kansas/KURAW-00102`.

The restored K-State row uses permanent `MATCH_SOURCE_ASSERTION` identity
metadata to link to the already-established reciprocal game without hard-coding
a canonical game ID.

Also repaired reciprocal identity mapping for the two 1918-19 Nebraska rows:
- `kansas-state-0207` -> `nebraska/NEBRAW-00310`
- `kansas-state-0208` -> `nebraska/NEBRAW-00311`

Those identity repairs do not silently resolve the institutions' conflicting
dates or the second game's 30-19 / 30-21 score disagreement.
