# Clemson source notes

## Primary institutional source

**Clemson 2026-27 Men's Basketball Media Guide**  
User-supplied PDF SHA-256: `770850e0b1cd9521ea215d1a42a7612fafdce68e5305b3fe6c7fe1560ac6d94c`

The All-Time Results section is the row-level spine for the competitive history through 2025-26. It supplies the literal opponent labels, result/score strings, H/A/N markers and footnote markers preserved in `raw_text`. The same media guide also supplies season/conference headers, NCAA Tournament history, coaching/season notes and the overtime legend used during package assembly.

Stage 6 does not silently replace literal guide evidence with normalized values. Accepted corrections and stronger site/classification evidence are recorded in curated fields and notes while `raw_text` remains literal.

## Accepted durable research layers

This package is assembled from the verified Clemson Research checkpoint chain, not reconstructed from chat memory:

1. Stage 1 accepted competitive universe and date/score/result ledger.
2. Stage 2 accepted opponent identity map.
3. Stage 3A final regular-season H/A/N and site ledger, including HOME facility chronology, modern neutral exact-site work, historical neutral location-first debt, and explicit OPPONENT_HOME responsibility.
4. Stage 3B final postseason classification/site ledger and closeout QA.

Immutable Research base: `e57a7049b2315508e59fd68b4324c34050901f45`.  
Protected main checked for this bounded Stage 6 audit: `4712a2d796c809a92dbde91e30ebf489f783ac76`.

## Site evidence hierarchy carried forward

Accepted site findings use the repository-authorized hierarchy and the exact evidence bases serialized in `source-games.csv`:

- Clemson institutional media guide, facility histories, schedules, previews, prospectuses and recaps;
- accepted project/current-main physical venue identities and reciprocal exact-game evidence;
- owner-authorized Conference Tournament Site Shared Reference after independent postseason classification;
- NCAA, conference, host and participant institutional evidence for postseason and neutral-site resolution;
- targeted archival/authoritative fallback evidence only where the bounded Research stages required it.

For permitted material site debt, the paired row-level `site_research_status` / `site_research_basis` fields remain the controlling compact explanation. Stage 6 moved resolved-row site evidence that had been stored in basis-only form into row `notes` under `[RESOLVED_SITE_EVIDENCE]` so current research accounting is structurally clean without discarding the evidence text.

## HOME chronology evidence

Clemson Athletics facility evidence establishes:

- pre-1916 basketball used Riggs Field or the Sikes Hall basement, without enough game-level evidence to assign each early HOME row to one physical site;
- Holtzendorff YMCA housed men's basketball from its Feb. 1, 1916 basketball opener into the 1922 season;
- a new campus gym existed beginning Jan. 13, 1922, but the consulted evidence did not safely establish one physical identity/name for all 1922-29 HOME rows;
- Fike Field House opened for Clemson basketball with the Jan. 7, 1930 dedication game and was Clemson's home through the 1968 transition;
- Littlejohn Coliseum's first Clemson game was Nov. 30, 1968;
- the Civic Center of Anderson was Clemson's temporary November/December 2002 home during renovation;
- Bon Secours Wellness Arena hosted Clemson's 2015-16 regular-season home schedule during the Littlejohn rebuild.

## Modern neutral venue evidence retained as new Research identities

Six resolved physical identities do not have a matching protected-main physical venue ID at `4712a2d796c809a92dbde91e30ebf489f783ac76` and therefore remain intentionally provisional for current-main rebase rather than being registered from Research:

- Holtzendorff YMCA — Clemson, SC
- Fike Field House — Clemson, SC
- Civic Center of Anderson — Anderson, SC
- Ted Constant Convocation Center — Norfolk, VA
- Titan Field House — Melbourne, FL
- Coca-Cola Coliseum — Toronto, ON

Ted Constant Convocation Center is supported by Clemson's 2006-07 neutral-site family plus Old Dominion institutional Cox Communications Classic schedule/preview evidence. Titan Field House is supported by Clemson's 2020-21 prospectus and Purdue-game recap for the Space Coast Challenge. Coca-Cola Coliseum is an owner-supplied exact physical-site fact for Clemson-TCU on 2023-12-09 and remains marked `PENDING_CURRENT_MAIN_REBASE`.

## Postseason evidence

The final Stage 3B ledger contains 188 postseason rows, all exact-site complete:

- 121 conference-tournament games;
- 30 NCAA Tournament games;
- 37 NIT games.

For conference-tournament site facts, the owner-authorized shared reference is consumed only after independent classification and only within matching season/conference/date-or-round scope. Material target-source contradictions are preserved in row notes instead of being overwritten.

For NCAA/NIT and other postseason exact sites, accepted official tournament/conference/host/participant and targeted institutional evidence is preserved in the Stage 3B basis fields carried into this package.

## Accomplishment evidence

The media guide season notes state that Clemson won its first regular-season ACC championship in 1989-90 and that the 1938-39 team won the Southern Conference Tournament championship. The accepted Stage 3B NCAA ledger spans 16 distinct NCAA appearance seasons and 30 NCAA games. The media guide NCAA section identifies the 2024 Elite Eight as Clemson's first since 1980; the program has no Final Four or national championship in the accepted institutional history.

## Provenance limits

- Exact-date debt on two old games remains explicit rather than inferred.
- The historical regular-season neutral location-first shortcut is not applied to postseason.
- Research does not mutate protected-main shared registries.
- Current-main display/alias normalization is kept separate from literal historical venue naming.
- Stage 5 NON_D1 owner sanity scan was approved on 2026-09-27 with zero flags.
- Stage 6 is complete only through the adversarial self-challenge boundary; Stage 7 immutable packaging / `RESEARCH_FROZEN` is not implied.


## Stage 6 self-challenge evidence additions

The final adversarial audit used bounded systematic evidence and did not restart closed Stage 3A/3B research.

- Clemson Athletics, **Holtzendorff YMCA Turns 100**: `https://clemsontigers.com/news/2016/01/07/holtzendorff-ymca-turns-100` — establishes the Feb. 1, 1916 YMCA basketball opener, its use through the 1922 season, and the earlier Riggs Field / Sikes Hall basement alternatives.
- Clemson University Libraries, **Gymnasium** historical image record: `https://digitalcollections.clemson.edu/single-item-view/?oid=CUIR:501B677CF4BE8CE6C3BCE2BECE21974F` — establishes a Clemson gym built Dec. 22, 1921-Jan. 13, 1922, but does not by itself supply a stable row-level canonical basketball venue identity for the full 1922-29 residual.
- Virginia Tech Athletics historical schedule: `https://stats.hokiesports.com/mbasketball/records/schedule.html` — supplies one exact Feb. 26, 1925 at-Clemson reciprocal assertion at “Boxer Gymnasium”; this is useful row evidence but not a safe default for every residual Clemson HOME game.
- Clemson Athletics, **One & Only Fike Field House**: `https://clemsontigers.com/news/2014/12/03/one-only-fike-field-house` — establishes the Jan. 7, 1930 dedication game/opening of the new field house.
- Wofford Athletics Clemson opponent history: `https://woffordterriers.com/sports/mens-basketball/opponent-history/clemson/27` — its displayed history begins in 1992 and therefore does not supply the unknown 1929-30 Wofford date.
- Furman Athletics Clemson opponent history: `https://furmanpaladins.com/sports/mens-basketball/opponent-history/clemson-university/7` — its displayed history begins in 2006 and therefore does not supply the unknown 1919-20 Furman date.

The six provisional physical venue candidates were also rechecked read-only against protected-main `venues.csv` plus `venue-names.csv` at the Stage 6 main SHA. No exact name/alias + geography match was found for Holtzendorff YMCA, Fike Field House, Civic Center of Anderson, Ted Constant Convocation Center, Titan Field House, or Coca-Cola Coliseum; they remain `Historical identity: RESOLVED / Global registration: PENDING_CURRENT_MAIN_REBASE`.

## Stage 6 representation compatibility repairs

Current protected-main research acceptance permits only blank, `FORFEIT`, `VACATED_GAME`, or `VACATED_WIN` administrative statuses. The three Clemson 1989-90 NCAA rows carried the older package token `NCAA_PARTICIPATION_VACATED`. Stage 6 normalized the two on-court wins to `VACATED_WIN` and the on-court loss to `VACATED_GAME`, preserving the original administrative note, score/result, date, site, game type and literal `raw_text`.

Current site-completeness accounting also reserves `site_research_status` / `site_research_basis` for material site gaps. Exactly 1,561 resolved rows carried basis-only evidence with no material gap. Stage 6 moved each basis verbatim into the row `notes` under `[RESOLVED_SITE_EVIDENCE]` and cleared the gap-accounting fields on those rows. The 190 actual material-gap rows retain their paired research status/basis unchanged.
