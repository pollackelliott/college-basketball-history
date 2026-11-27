# Air Force Stage 1 — year-by-year game extraction checkpoint 0011 (1993–94 to 1996–97)

**STATUS: STAGE1_IN_PROGRESS.** This is one bounded four-season Research checkpoint, **not** Stage 1 COMPLETE, Stage 2, Research Freeze, an owner approval, or Implementation. The separately preserved **1982–83 Stage 1 institutional-source population blocker** remains open.

Authority: independently authenticated protected main and immutable `research_base_sha` `3f5a15458aa468347e56e669327d6fe4c9c6ee69`. Exact inherited Research checkpoint HEAD `7d271cfead2d74071049748c2628bde1fc204e90`. Accepted owner-final top-level boundary `Air Force,1957-58+` remains unchanged and distinct from institutional inception **1956–57**, the documented NON_D1 first season; cutoff **2025–26**.

## Institutional source extraction and reconciliation

Primary game source: official Air Force **2026–27 men's basketball history guide**, SHA-256 `5fdf61cc80c698bae8ce61cc0ae1009d01139682c8148014934e304b407b73fd`, PDF pp **64–65** (source https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/goairforcefalcons.com/documents/2026/5/27/History.2026-27.pdf?timestamp=20260527033629). The 1993–94 results occupy the far-right column of p64; 1994–95 upper-left p65; 1995–96 lower-left p65; 1996–97 upper-center p65. Rows are selected by exact bounded column/season and rechecked against printed guide season headings.

| Season | Guide overall W–L | Accepted game rows | Source WAC regular-season W–L | H/A/N W–L | WAC postseason |
|---|---:|---:|---|---|---|
| 1993–94 | 8–18 | 26 | 3–15 | H7–8 A1–9 N0–1 | Texas–El Paso# L58–72, March 9, 1994 |
| 1994–95 | 8–20 | 28 | 4–14 | H7–7 A1–10 N0–3 | Colorado State# L75–84, March 8, 1995 |
| 1995–96 | 5–23 | 28 | 1–17 | H5–10 A0–10 N0–3, **provisional secondary matched** | San Diego State# L69–80, March 6, 1996 |
| 1996–97 | 7–19 | 26 | 2–14 | H6–9 A0–10 N1–0 | **No tournament game in official guide** |

**108 uniquely identified competitive games added**, consisting of **105 regular-season games and 3 WAC Conference Tournament games**. The combined `stage1-ledger.csv` now contains **1,024** unique stable game IDs across **40 accepted seasons**. The previous **916 accepted game rows and original header are preserved byte-for-byte**. No exhibition, scored administrative outcome mismatch or real-game duplicate is introduced. All newly harvested W/L results sum exactly to their source season headings; all guide `*` WAC markers reconcile 3–15, 4–14, 1–17, 2–14. `#` denotes postseason WAC Tournament, not the regular-season conference.

Air Force current official season schedule pages were independently inspected for **1993–94, 1994–95, and 1996–97**, matching the institutional guide game identities, dates, scores, overall record, site totals and conference record. The **1995–96 official individual-season schedule page was inaccessible** through the authorized web transport. Its 28 game identities and exact scores come from the current Air Force guide, and secondary exact-game MCubed supports H5–10 A0–10 N0–3; those H/A/N classifications are labeled **provisional** pending governed site work. The online **text-only 1996–97 endpoint misleadingly serves University at Buffalo's 17–11 schedule**, and is expressly rejected as evidence; Air Force's regular standard schedule URL contains the correct 7–19 Air Force records.

## Specific bounded findings

- **1993–94:** the two Navy games are separate dated competitive results (Nov 27 away L63–77, Dec 6 home W82–70). The March 9 Texas–El Paso WAC postseason loss in **Salt Lake City, Utah** is NEUTRAL; no postseason exact building is inferred at Stage 1.
- **1994–95:** Cessna Classic losses to The Citadel and Gonzaga are **neutral in Wichita, Kansas**. The **January 2, 1995 Texas–El Paso WAC road loss 64–80 was in El Paso, Texas** per the exact Air Force schedule; MCubed erroneously calls it HOME, yielding H7–8 A1–9 rather than university H7–7 A1–10. The Colorado State WAC first-round loss was **NEUTRAL in Albuquerque, New Mexico**.
- **1995–96:** valid February 29, 1996 away loss to New Mexico remains untouched; **1996 was a leap year**. The Nov 28 Adams State victory is source-guide and university head-to-head **84–81**, not secondary **94–81**, with original opponent text preserved. Toledo MVP Classic losses to Austin Peay and William & Mary are both neutral at Toledo, Ohio. San Diego State WAC Tournament loss is neutral at **Albuquerque, NM**.
- **1996–97:** Holiday Stores Classic in **Bozeman, Montana** consists of a neutral Tennessee Tech W88–68 and an AWAY loss to **host Montana State** L67–70, despite both carrying `$` event markers. The guide and official Air Force season schedule say Nov 23 Regis **L48–69**, not the MCubed secondary **L48–67**. No WAC Tournament row appears in guide; do not invent one or classify regular-season `*` games as postseason.

Four new nonblocking discrepancy/resolution notes are appended: 1994–95 UTEP H/A/N secondary error; 1995–96 Adams State score discrepancy; 1995–96 official schedule inaccessibility/provisional sites; and 1996–97 Regis third-party score error. All **36 predecessor residuals** remain unmodified; total **40**. Existing 1982–83 blocking raw-source 26-row list and source-disagreement documentation are carried forward with exact original Git blobs, preserving no accepted 1982–83 game in the current ledger. The 1976–77 Montana administrative-forfeit sidecar and empty exclusion file are likewise inherited unchanged.

**Institutional census:** 70 inception-through-2025–26 seasons; **40** have reconciled row-level game populations. **30** remain unaccepted: one already source-harvested but conflicting **1982–83** season, plus **29 later not-yet-extracted seasons (1997–98 through 2025–26)**. Original guide season aggregates imply **904 prospective game records** not yet accepted (27 represented by the disputed 1982–83 heading and 877 aggregate later games). These are not automatically historically missing games and do not justify unidentified-game gap exceptions. The inherited +2 all-time printed guide-win discrepancy remains a source-internal residual.

**Safety:** research-only branch `research/air-force`. No mutation to protected main, canonical games, published basketball data, global registries, another school’s artifacts, or the one-active-Implementation lock.

## Next bounded unit

Mechanically extract and reconcile **1997–98 through 2000–01** from the official guide and institutional schedules, preserving modern neutral venue expectations for later site research. Publish a single successor Research-only checkpoint and keep 1982–83 quarantined for a separately bounded source-family reconciliation before Stage 1 closeout. Do not begin Stage 2 automatically.
