# SDSU ALL_HISTORY_EXPANSION — checkpoint 0004

## Exact authority
- Immutable Research base: `5b840a354fb5cd792239ff8b93cba223a18dd87a`
- Parent checkpoint 0003 HEAD: `b7fad334949786ef0fda92b8b7fadb9821d1a893`.
- Primary PDF owner upload: *2026-27 San Diego State Men's Basketball Media Guide*, SHA-256 `9c63066b60365d4f90abdb36242bf880f84b87030f87d776a6f81fbc75b9f2ad`.
- No change to protected main, published baseline, owner gates, or Implementation.
- Stage 1 remains **INCOMPLETE**.

## Decided lower-level tournament cohort — 11 accepted POSTSEASON games
The media guide's year-by-year ledger (printed pp. 88-89, PDF pp. 90-91) separates ordinary schedule games from named postseason local AAU/YMCA tournaments at the END of the schedule. Each of these 11 has literal opponent, W/L, and score, plus an exact distinct event heading; two series have `(CH)` final indicators.

- 1924-25: three consecutive February 24-26 San Diego County AAU Tournament games, including USS Omaha (CH).
- 1925-26: one February 25 San Diego AAU Tournament game.
- 1926-27: three February 23-26 San Diego AAU Tournament games, including San Diego Navy (CH).
- 1927-28: four February 29-March 3 San Diego YMCA Tournament games, including Submarines Pacific (CH).
- These are lower-level `POSTSEASON`, NOT `CONFERENCE_TOURNAMENT` or NCAA/NIT. Original source event labels remain byte-for-byte preserved in the candidate ledger and review overlay.
- 1928-29 **two** rows remain held for mixed context, because the same heading `SAN DIEGO YMCA TOURNAMENT` precedes February 20 San Diego Athletic Club B AND March 2 `*Redlands`, with the same season's asterisk convention defining it as a conference game. Do not blanket classify those two as postseason.
- The parent 215 `REGULAR_SEASON` accepted rows remain unchanged; `newly-accepted-postseason.csv` contains only 11 additional accepted IDs, making a total of 226 accepted.
- The opposite-page institutional 2023-24 guide independently preserves the same named event text but derives from the same institutional records, not separate event corroboration. Source is `https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/goaztecs.com/documents/2024/2/28/San_Diego_State_2023-24_Media_Guide.pdf`; note this older edition visibly has at least one result-text transcription issue (1924-25 Bank First National), so primary 2026 owner guide controls W/L and score.

## Additional primary institutional source discovery — opponent index
The SAME 2026-27 official media guide contains a distinct `vs. All Opponents` index (printed p. 104, PDF p. 106):
- `Alumni 33 26 7 D.28.28 D.2.60`. The detailed 1928-29..1935-36 cohort has eight literal standalone “Alumni” results. The index provides repeated-team/population identity, not proof that games qualify as recognized varsity competition versus a school alumni exhibition.
- `SDSU Alumni at Stanford 3 0 3 D.26.21 D.26.23`. The detailed ledger identifies three “Alumni at Stanford” losses in 1921-22 and 1923-24. **Do not normalize to Stanford varsity or to Stanford(Alumni) merely because third-party mcubed labels it that way.** This primary index explicitly uses “SDSU Alumni at Stanford”; possibility of same-program alumni must remain visible.
- `San Diego State All-Stars 1 1 0 1922-23 1922-23`. The institution's detailed 1922-23 ledger separately lists **two** same-name All-Stars results, one 9-13 L and one 33-28 W. This is a genuine cross-section disagreement, not a reason to delete the loss or double-count a win.
- Relevant secondary aggregation `https://mcubed.net/ncaab/series/sandst/nd1series8.shtml`, `https://mcubed.net/ncaab/series/sandst/nd1_stanfordalumni.shtml` calls third-party 33 games San Diego State(Alumni), but 3 earlier games Stanford(Alumni). This conflicting normalization is lower authority than the school's literal source. Neither identity interpretation alone proves exhibition versus competitive varsity participation. All 13 previously held inclusion rows **remain held**.

## Source-family access limits
- SDSU Library confirms historical student newspapers exist and are digitized, `https://library.sdsu.edu/collections` and `https://sdsulibrary.wordpress.com/2013/09/12/extra-extra-read-all-about-it/`. Its historical series was Paper Lantern then The Aztec; the library's local paper guide lists physical/online options: `https://libguides.sdsu.edu/newspapers/local`.
- Direct digital.sdsu.edu and digitallibrary.sdsu.edu requests were unavailable in this bounded research pass. Catalog metadata without the article/issue is NOT used as historical game-type or exhibition evidence.
- David Howard Fontius's *A History of Basketball at San Diego State College from 1921 to 1971* appears in San Diego History Center's historical thesis catalog `https://sandiegohistory.org/journal/1993/july/theses2/`. The thesis itself was not obtained; do not claim its contents support decisions.
- Refuse recursive archive hunting solely to discharge a few doubtful old opponent classifications while 34 seasons remain unextracted. Carry durable held rows, then resume source extraction; later one bounded contemporaneous family pass can revisit after 49-season source harvest.

## 15-season exact accounting
Official aggregate 250 outcomes (163-86-1) = original 242 detailed source result entries + 5 distinct forfeiture awards + 3 explicitly unidentified outcomes. Of the 242: 215 accepted regular season; 11 newly accepted postseason; 13 inclusion-held; 2 mixed tournament held; 1 source JV excluded. Zero fabricated played game IDs. The 11 tournament rows are not extra games beyond the original 242; no altered season count.
