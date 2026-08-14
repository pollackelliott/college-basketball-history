#!/usr/bin/env python3
"""Resolve the 66 owner-approved Vanderbilt ingestion discrepancies.

Default: DRY RUN
Apply:   python tools/resolve_vanderbilt_reconciliation.py --apply

This is intentionally a narrow, assertion-checked migration. It expects the exact
post-ingestion state produced on 2026-08-14, preserves every source ``raw_text``
value, updates demonstrably incorrect curated Vanderbilt fields and their global
assertions, records every discrepancy as resolved, and applies the approved
canonical corrections.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from location_safety import append_note, registry_fallback_marker


@dataclass(frozen=True)
class Resolution:
    discrepancy_id: str
    canonical_game_id: str
    field_name: str
    source_value: str
    old_canonical: str
    winner: str
    basis: str

    @property
    def final_value(self) -> str:
        return self.source_value if self.winner == "SOURCE" else self.old_canonical


RESOLUTION_TEXT = """
DISC-000101|CBBG-0014720|score|33-18|37-18|CANONICAL|Kentucky contemporary game evidence establishes Kentucky 37, Vanderbilt 18; Vanderbilt's later 33-18 summary is a source typo.
DISC-000102|CBBG-0014727|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Kentucky game-level evidence places the Jan. 18, 1922 game at Vanderbilt in Nashville.
DISC-000103|CBBG-0020343|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Tennessee's official opponent history places the Feb. 22, 1922 game at Vanderbilt.
DISC-000104|CBBG-0020358|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Tennessee's official opponent history places the Feb. 22, 1923 game at Vanderbilt.
DISC-000105|CBBG-0014754|score|23-13|33-13|CANONICAL|Kentucky historical game evidence establishes Kentucky 33, Vanderbilt 13.
DISC-000106|CBBG-0020383|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Tennessee's official opponent history places the Feb. 2, 1925 game at Vanderbilt.
DISC-000107|CBBG-0020399|overtime_periods|1|0|SOURCE|Vanderbilt's official game row explicitly marks the Feb. 6, 1926 Tennessee game as overtime; Tennessee's summary omits the marker.
DISC-000108|CBBG-0014835|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Kentucky game-level evidence places the Feb. 8, 1928 game at Vanderbilt.
DISC-000109|CBBG-0020443|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Tennessee's official opponent history places the Feb. 23, 1929 game at Vanderbilt.
DISC-000110|CBBG-0020454|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Tennessee's official opponent history places the Feb. 8, 1930 game at Vanderbilt.
DISC-000111|CBBG-0020456|overtime_periods|1|0|SOURCE|Vanderbilt's official game row explicitly marks the Feb. 22, 1930 Tennessee game as overtime; Tennessee's summary omits the marker.
DISC-000112|CBBG-0017791|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Florida's official opponent history places the Jan. 19, 1931 game at Vanderbilt.
DISC-000113|CBBG-0014884|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Kentucky game-level evidence places the Jan. 21, 1931 game at Vanderbilt.
DISC-000114|CBBG-0020469|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Tennessee's official opponent history places the Jan. 27, 1931 game at Vanderbilt.
DISC-000115|CBBG-0017809|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Florida's official opponent history places the Jan. 18, 1932 game at Vanderbilt.
DISC-000116|CBBG-0017810|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Florida's official opponent history places the Jan. 19, 1932 game at Vanderbilt.
DISC-000117|CBBG-0020484|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Tennessee's official opponent history places the Jan. 26, 1932 game at Vanderbilt.
DISC-000118|CBBG-0020497|overtime_periods|1|0|SOURCE|Vanderbilt's official game row explicitly marks the Jan. 10, 1933 Tennessee game as overtime.
DISC-000119|CBBG-0020536|overtime_periods|1|0|SOURCE|Vanderbilt's official game row explicitly marks the Feb. 23, 1935 Tennessee game as overtime.
DISC-000120|CBBG-0020607|score|38-56|38-46|CANONICAL|Tennessee's official opponent history establishes Vanderbilt 46, Tennessee 38 on Feb. 21, 1939.
DISC-000121|CBBG-0020611|site_type|NEUTRAL|TEAM_A_HOME|CANONICAL|Tennessee's official history places the 1939 SEC Tournament game in Knoxville on Tennessee's actual home floor; project policy classifies it as Tennessee home.
DISC-000122|CBBG-0017974|score|47-41|48-41|CANONICAL|Florida's official history establishes Florida 48, Vanderbilt 41 in the 1941 SEC Tournament.
DISC-000123|CBBG-0015211|site_type|NEUTRAL|TEAM_A_HOME|SOURCE|Kentucky historical game evidence and Vanderbilt's explicit neutral marker place the Feb. 9, 1946 game in Paducah, Kentucky, not Lexington.
DISC-000124|CBBG-0020716|game_date|1946-02-23|1946-02-25|CANONICAL|Tennessee's official opponent history establishes Feb. 25, 1946.
DISC-000125|CBBG-0015237|score|80-30|82-30|CANONICAL|Kentucky historical game evidence establishes Kentucky 82, Vanderbilt 30.
DISC-000126|CBBG-0015252|site_type|NEUTRAL|TEAM_A_HOME|SOURCE|The Feb. 27, 1947 SEC Tournament game was played at a neutral site in Louisville, not at Kentucky in Lexington.
DISC-000127|CBBG-0015383|game_date|1951-02-19|1951-02-24|CANONICAL|Kentucky's schedule establishes Feb. 24, 1951; Kentucky played DePaul in Chicago on Feb. 19.
DISC-000128|CBBG-0018186|overtime_periods|1|0|SOURCE|Vanderbilt's explicit OT marker and Florida's SEC Tournament history establish one overtime on Feb. 29, 1952.
DISC-000129|CBBG-0018186|game_type|REGULAR_SEASON|CONFERENCE_TOURNAMENT|CANONICAL|Florida's SEC Tournament history and Vanderbilt's tournament marker classify the Feb. 29, 1952 game as a conference-tournament game.
DISC-000130|CBBG-0020846|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Tennessee's official opponent history places the Dec. 30, 1952 game at Vanderbilt.
DISC-000131|CBBG-0015469|score|71-59|77-59|CANONICAL|Kentucky historical game evidence establishes Kentucky 77, Vanderbilt 59.
DISC-000132|CBBG-0015487|game_date|1956-01-21|1956-01-28|CANONICAL|Vanderbilt's official Memorial Gym retrospective and Kentucky evidence establish Jan. 28, 1956.
DISC-000133|CBBG-0018291|score|59-75|59-76|CANONICAL|Florida's official opponent history establishes Vanderbilt 76, Florida 59.
DISC-000134|CBBG-0000963|overtime_periods|1|0|SOURCE|Vanderbilt's OT marker and a contemporaneous Dec. 9, 1958 newspaper report establish one overtime; a later Missouri summary's 2OT label remains conflicting evidence.
DISC-000135|CBBG-0018333|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Owner ruling on 2026-08-14: the Feb. 21, 1959 Florida game was at Vanderbilt; the conflicting Vanderbilt series-table A marker remains preserved.
DISC-000136|CBBG-0003947|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Arkansas's official opponent history places the Dec. 14, 1963 game at Vanderbilt.
DISC-000137|CBBG-0021074|score|64-62|65-62|CANONICAL|Tennessee's official opponent history establishes Tennessee 65, Vanderbilt 62.
DISC-000138|CBBG-0018447|score|78-91|79-91|CANONICAL|Florida's official opponent history establishes Vanderbilt 91, Florida 79.
DISC-000139|CBBG-0021185|score|70-60|70-69|CANONICAL|Tennessee's official opponent history establishes Tennessee 70, Vanderbilt 69.
DISC-000140|CBBG-0021203|overtime_periods|0|2|CANONICAL|Tennessee's official history establishes two overtimes on Feb. 2, 1970.
DISC-000141|CBBG-0018583|overtime_periods|0|1|CANONICAL|Florida's official opponent history establishes one overtime on Feb. 9, 1970.
DISC-000142|CBBG-0018583|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Florida's official opponent history places the Feb. 9, 1970 game at Vanderbilt.
DISC-000143|CBBG-0018598|overtime_periods|3|1|SOURCE|Contemporaneous reporting establishes that Florida's 84-82 win over Vanderbilt on Jan. 4, 1971 lasted three overtimes.
DISC-000144|CBBG-0007125|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Illinois's official opponent history places the Dec. 23, 1971 game at Vanderbilt.
DISC-000145|CBBG-0018883|overtime_periods|1|2|CANONICAL|Florida's official history establishes two overtimes in the March 3, 1982 SEC Tournament game.
DISC-000146|CBBG-0007424|overtime_periods|2|0|SOURCE|A contemporaneous UPI report establishes that Illinois-Vanderbilt on Dec. 13, 1982 went to a second overtime.
DISC-000147|CBBG-0019023|game_date|1987-02-26|1987-02-25|CANONICAL|Florida's official opponent history establishes Feb. 25, 1987.
DISC-000148|CBBG-0021625|score|75-57|74-57|CANONICAL|Tennessee's official opponent history establishes Tennessee 74, Vanderbilt 57.
DISC-000149|CBBG-0019223|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Florida's official opponent history places the Feb. 26, 1994 game at Vanderbilt.
DISC-000150|CBBG-0019305|game_date|1997-03-01|1997-03-03|CANONICAL|Florida's official opponent history establishes March 3, 1997.
DISC-000151|CBBG-0019321|game_date|1998-01-19|1998-01-24|CANONICAL|Florida's official opponent history establishes Jan. 24, 1998.
DISC-000152|CBBG-0019378|game_date|2000-01-28|2000-01-29|CANONICAL|Florida's official opponent history establishes Jan. 29, 2000.
DISC-000153|CBBG-0021943|site_type|TEAM_A_HOME|TEAM_B_HOME|CANONICAL|Tennessee's official opponent history places the Feb. 19, 2000 game at Vanderbilt.
DISC-000154|CBBG-0016952|score|52-57|51-57|SOURCE|Contemporary official Kentucky records establish Vanderbilt 57, Kentucky 52 on Jan. 10, 2006.
DISC-000155|CBBG-0017017|overtime_periods|2|1|SOURCE|Official game records establish that Kentucky-Vanderbilt on Jan. 12, 2008 went to two overtimes.
DISC-000156|CBBG-0005266|score|81-65|81-75|CANONICAL|Arkansas's contemporary official recap and season record establish Arkansas 81, Vanderbilt 75.
DISC-000157|CBBG-0002514|overtime_periods|1|0|SOURCE|Missouri's contemporary official postgame notes establish one overtime on Dec. 8, 2010.
DISC-000158|CBBG-0002625|site_type|TEAM_B_HOME|TEAM_A_HOME|SOURCE|Missouri's contemporary official recap and box score place the Jan. 16, 2014 game at Vanderbilt in Nashville.
DISC-000159|CBBG-0005505|overtime_periods|0|1|CANONICAL|Arkansas's official game record establishes one overtime on Jan. 5, 2016.
DISC-000160|CBBG-0002700|site_type|TEAM_B_HOME|TEAM_A_HOME|SOURCE|Missouri's official schedule and recap place the Feb. 10, 2016 game at Vanderbilt in Nashville.
DISC-000161|CBBG-0017400|score|87-52|87-62|SOURCE|Kentucky's contemporary official recap establishes Kentucky 87, Vanderbilt 52 on Jan. 29, 2019.
DISC-000162|CBBG-0020008|game_date|2020-12-30|2020-12-29|SOURCE|Owner-approved correction corroborated by Florida's official 2020-21 schedule: the game was played Dec. 30, 2020.
DISC-000163|CBBG-0005665|score|92-71|82-71|SOURCE|Owner-approved correction corroborated by contemporary Arkansas and Vanderbilt records: Arkansas won 92-71.
DISC-000164|CBBG-0020021|game_date|2021-03-12|2021-03-11|CANONICAL|Florida's official schedule establishes March 11, 2021 for the SEC Tournament game.
DISC-000165|CBBG-0017495|score|77-71|71-63|SOURCE|Contemporary official records establish Kentucky 77, Vanderbilt 71 in the 2022 SEC Tournament quarterfinal.
DISC-000166|CBBG-0002909|score|85-82|85-83|SOURCE|Missouri's official 2022-23 schedule establishes Missouri 85, Vanderbilt 82.
"""


def parse_resolutions() -> list[Resolution]:
    result: list[Resolution] = []
    for line in RESOLUTION_TEXT.strip().splitlines():
        parts = line.split("|", 6)
        if len(parts) != 7:
            raise ValueError(f"Malformed resolution row: {line}")
        result.append(Resolution(*parts))
    return result


RESOLUTIONS = parse_resolutions()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv_preserving_format(
    path: Path, fieldnames: list[str], rows: list[dict[str, str]]
) -> None:
    original = path.read_bytes()
    has_bom = original.startswith(b"\xef\xbb\xbf")
    line_ending = "\r\n" if original.count(b"\r\n") else "\n"
    encoding = "utf-8-sig" if has_bom else "utf-8"
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding=encoding) as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, lineterminator=line_ending
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    temporary.replace(path)


def canonical_field_value(row: dict[str, str], field_name: str) -> str:
    if field_name == "score":
        return f"{row.get('team_a_score', '')}-{row.get('team_b_score', '')}"
    return row.get(field_name, "")


def source_field_value(row: dict[str, str], canonical: dict[str, str], field_name: str) -> str:
    program = row.get("source_program_key", "").strip()
    opponent = row.get("normalized_opponent_key", "").strip()
    team_a = min(program, opponent)

    if field_name == "score":
        team_score = row.get("team_score", "").strip()
        opponent_score = row.get("opponent_score", "").strip()
        return (
            f"{team_score}-{opponent_score}"
            if program == team_a
            else f"{opponent_score}-{team_score}"
        )
    if field_name == "site_type":
        site = row.get("curated_site_type", "").strip()
        if site == "SOURCE_PROGRAM_HOME":
            return "TEAM_A_HOME" if program == team_a else "TEAM_B_HOME"
        if site == "OPPONENT_HOME":
            return "TEAM_A_HOME" if opponent == team_a else "TEAM_B_HOME"
        return site
    if field_name == "game_type":
        return row.get("curated_game_type", "")
    return row.get(field_name, "")


def set_canonical_field(row: dict[str, str], field_name: str, value: str) -> None:
    if field_name == "score":
        team_a_score, team_b_score = value.split("-", 1)
        row["team_a_score"] = team_a_score
        row["team_b_score"] = team_b_score
        a = int(team_a_score)
        b = int(team_b_score)
        row["result_winner_team_key"] = (
            row["team_a_key"] if a > b else row["team_b_key"] if b > a else ""
        )
        return
    row[field_name] = value
    if field_name == "game_date":
        row["date_precision"] = "EXACT"


def relative_source_site(canonical: dict[str, str], canonical_site: str) -> str:
    if canonical_site == "NEUTRAL":
        return "NEUTRAL"
    if canonical_site not in {"TEAM_A_HOME", "TEAM_B_HOME"}:
        return canonical_site
    home = (
        canonical["team_a_key"]
        if canonical_site == "TEAM_A_HOME"
        else canonical["team_b_key"]
    )
    return "SOURCE_PROGRAM_HOME" if home == "vanderbilt" else "OPPONENT_HOME"


def set_source_field(
    row: dict[str, str], canonical: dict[str, str], field_name: str, value: str
) -> None:
    if field_name == "score":
        score_a, score_b = value.split("-", 1)
        if row["source_program_key"] == canonical["team_a_key"]:
            team_score, opponent_score = score_a, score_b
        else:
            team_score, opponent_score = score_b, score_a
        row["team_score"] = team_score
        row["opponent_score"] = opponent_score
        team_int = int(team_score)
        opponent_int = int(opponent_score)
        row["played_result"] = (
            "W" if team_int > opponent_int else "L" if opponent_int > team_int else "T"
        )
        return
    if field_name == "site_type":
        row["curated_site_type"] = relative_source_site(canonical, value)
        return
    if field_name == "game_type":
        row["curated_game_type"] = value
        return
    row[field_name] = value


def append_semicolon(existing: str, addition: str) -> str:
    existing = (existing or "").strip()
    if addition in existing:
        return existing
    return f"{existing}; {addition}" if existing else addition


def apply_site_metadata(
    resolution: Resolution,
    canonical: dict[str, str],
    source: dict[str, str],
) -> int:
    """Apply approved home/neutral geography and safe Vanderbilt venue chronology."""
    final_site = resolution.final_value
    changed = 0

    if final_site in {"TEAM_A_HOME", "TEAM_B_HOME"}:
        home_key = (
            canonical["team_a_key"]
            if final_site == "TEAM_A_HOME"
            else canonical["team_b_key"]
        )
        if canonical.get("designated_home_team_key", "") != home_key:
            canonical["designated_home_team_key"] = home_key
            changed += 1

        if home_key == "vanderbilt":
            game_date = canonical.get("game_date", "")
            if game_date and game_date < "1952-12-06":
                venue_key, venue_name = "old-gym", "Old Gym"
            else:
                venue_key, venue_name = "memorial-gymnasium", "Memorial Gymnasium"

            changed_fields: list[str] = []
            for field, value in (
                ("venue_key", venue_key),
                ("site_city", "Nashville"),
                ("site_state", "TN"),
            ):
                if canonical.get(field, "") != value:
                    canonical[field] = value
                    changed_fields.append(field)
                    changed += 1

            source["curated_venue_name"] = venue_name
            source["city"] = "Nashville"
            source["state"] = "TN"

            if changed_fields:
                canonical["notes"] = append_note(
                    canonical.get("notes", ""),
                    registry_fallback_marker(
                        "vanderbilt",
                        source["source_game_id"],
                        venue_key,
                        final_site,
                        changed_fields,
                    ),
                )
        else:
            # Preserve an already-established opponent venue, but synchronize
            # explicit normalized geography into Vanderbilt's curated assertion.
            source["city"] = canonical.get("site_city", "")
            source["state"] = canonical.get("site_state", "")
    elif final_site == "NEUTRAL":
        if canonical.get("designated_home_team_key", ""):
            canonical["designated_home_team_key"] = ""
            changed += 1
        if resolution.discrepancy_id == "DISC-000123":
            location = ("Paducah", "KY")
        elif resolution.discrepancy_id == "DISC-000126":
            location = ("Louisville", "KY")
        else:
            location = None
        if location:
            for field, value in (
                ("venue_key", ""),
                ("site_city", location[0]),
                ("site_state", location[1]),
            ):
                if canonical.get(field, "") != value:
                    canonical[field] = value
                    changed += 1
            source["curated_venue_name"] = ""
            source["city"], source["state"] = location

    return changed


SOURCE_ASSERTION_COPY_FIELDS = (
    "source_program_key",
    "source_game_id",
    "source_era",
    "season_label",
    "game_date",
    "source_opponent_label",
    "normalized_opponent_key",
    "normalized_opponent_name",
    "team_score",
    "opponent_score",
    "played_result",
    "overtime_periods",
    "source_site_candidate",
    "curated_site_type",
    "source_venue_name",
    "curated_venue_name",
    "city",
    "state",
    "event_or_tournament",
    "source_round",
    "curated_game_type",
    "curated_postseason_round",
    "source_page",
    "raw_text",
    "normalization_status",
    "administrative_status",
    "administrative_note",
    "notes",
)


NOTES_SECTION = """

## 13. Post-ingestion reconciliation — 2026-08-14

Vanderbilt ingestion surfaced 66 field-level discrepancies against eight previously
public programs. The owner approved all 66 resolutions on 2026-08-14. Twenty
canonical values were corrected, while 46 existing canonical values were retained
and the Vanderbilt curated normalization was corrected to match the stronger
game-level evidence. All original Vanderbilt `raw_text` values and discrepancy
source values remain preserved.

The owner specifically confirmed that the 1959-02-21 Florida game was played at
Vanderbilt. The canonical Vanderbilt-home classification therefore controls;
Vanderbilt's conflicting opponent-series `A` marker remains preserved as source
context. No Vanderbilt ingestion discrepancy remains under review.
"""


SOURCE_NOTES_SECTION = """

## 10. Post-ingestion reconciliation — 2026-08-14

The owner approved all 66 Vanderbilt ingestion discrepancy resolutions. Cross-source
review used official opponent histories and contemporary game records from Kentucky,
Tennessee, Florida, Arkansas, Missouri, and Illinois. Twenty canonical fields were
corrected; 46 Vanderbilt curated fields were normalized to the retained canonical
value. Raw Vanderbilt fact-book text remains unchanged, and every original conflict
remains auditable in `data/reconciliation/discrepancies.csv` with `RESOLVED` status.

The owner ruled that Florida-Vanderbilt on 1959-02-21 was played at Vanderbilt.
The curated site is therefore Vanderbilt home, while the fact book's conflicting
series-table `A` marker remains preserved in `source_site_candidate`.

Principal online cross-source references:

- [Tennessee opponent history](https://utsports.com/sports/mbball/opponent-history/vanderbilt/80)
- [Florida opponent history](https://floridagators.com/sports/mens-basketball/opponent-history/vanderbilt-university/90)
- [Illinois opponent history](https://fightingillini.com/sports/mens-basketball/opponent-history/vanderbilt-university/77)
- [Arkansas 2021 postgame record](https://arkansasrazorbacks.com/vanderbilt-postgame-justin-smith-and-moses-moody/)
- [Missouri 2022-23 schedule](https://mutigers.com/sports/mens-basketball/schedule/season/2022-23)
- [Kentucky 2019 official recap](https://ukathletics.com/news/2019/01/29/mens-basketball-no-7-cats-slam-dores-in-nashville/)
- [Contemporary 1982 Illinois-Vanderbilt UPI report](https://www.upi.com/Archives/1982/12/13/Anthony-Welch-who-scored-28-points-sank-two-free/7492408603600/)
"""


def update_markdown(notes_path: Path, source_notes_path: Path) -> None:
    notes = notes_path.read_text(encoding="utf-8")
    notes = notes.replace(
        "## 11. Owner-approved future canonical corrections",
        "## 11. Owner-approved canonical corrections",
    ).replace(
        "The owner approved both surfaced cross-source corrections, but this package commit intentionally does **not** edit global canonical data:",
        "The owner approved both surfaced cross-source corrections, and post-ingestion reconciliation applies them to global canonical data:",
    )
    if "## 13. Post-ingestion reconciliation — 2026-08-14" not in notes:
        notes = notes.rstrip() + NOTES_SECTION + "\n"
    notes_path.write_text(notes, encoding="utf-8")

    source_notes = source_notes_path.read_text(encoding="utf-8")
    source_notes = source_notes.replace(
        "The future correction applies to `CBBG-0020008`.",
        "Canonical reconciliation applies this correction to `CBBG-0020008`.",
    ).replace(
        "The future correction applies to `CBBG-0005665`.",
        "Canonical reconciliation applies this correction to `CBBG-0005665`.",
    ).replace(
        "This source-package phase records the decisions but does not apply them to canonical games or discrepancies.",
        "The source package recorded these decisions before ingestion; post-ingestion reconciliation applies them to canonical games and discrepancies.",
    ).replace(
        "Material field disagreements remain for the later reconciliation phase.",
        "The material field disagreements were resolved in the post-ingestion reconciliation phase.",
    )
    if "## 10. Post-ingestion reconciliation — 2026-08-14" not in source_notes:
        source_notes = source_notes.rstrip() + SOURCE_NOTES_SECTION + "\n"
    source_notes_path.write_text(source_notes, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--repo", type=Path, default=None)
    args = parser.parse_args()

    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    canonical_path = repo / "data" / "canonical" / "games.csv"
    assertions_path = repo / "data" / "evidence" / "game-assertions.csv"
    discrepancies_path = repo / "data" / "reconciliation" / "discrepancies.csv"
    source_path = repo / "schools" / "vanderbilt" / "source-games.csv"
    notes_path = repo / "schools" / "vanderbilt" / "notes.md"
    source_notes_path = repo / "schools" / "vanderbilt" / "source-notes.md"

    canonical_fields, canonical_rows = read_csv(canonical_path)
    assertion_fields, assertion_rows = read_csv(assertions_path)
    discrepancy_fields, discrepancy_rows = read_csv(discrepancies_path)
    source_fields, source_rows = read_csv(source_path)

    canonical_by_id = {row["canonical_game_id"]: row for row in canonical_rows}
    discrepancy_by_id = {row["discrepancy_id"]: row for row in discrepancy_rows}
    source_by_id = {row["source_game_id"]: row for row in source_rows}

    assertions_by_game: dict[str, list[dict[str, str]]] = {}
    for assertion in assertion_rows:
        if assertion.get("source_program_key") == "vanderbilt":
            assertions_by_game.setdefault(assertion["canonical_game_id"], []).append(assertion)

    print("College Basketball History — Vanderbilt reconciliation")
    print(f"Repository: {repo}")
    print(f"Mode:       {'APPLY' if args.apply else 'DRY RUN'}")
    print()

    errors: list[str] = []
    resolved_count = 0
    canonical_field_changes = 0
    canonical_metadata_changes = 0
    source_rows_changed: set[str] = set()
    assertions_to_sync: dict[str, tuple[dict[str, str], dict[str, str]]] = {}

    for resolution in RESOLUTIONS:
        discrepancy = discrepancy_by_id.get(resolution.discrepancy_id)
        canonical = canonical_by_id.get(resolution.canonical_game_id)
        if discrepancy is None or canonical is None:
            errors.append(
                f"{resolution.discrepancy_id}: missing expected discrepancy or canonical row"
            )
            continue

        expected_discrepancy = {
            "canonical_game_id": resolution.canonical_game_id,
            "field_name": resolution.field_name,
            "source_a_program_key": "vanderbilt",
            "source_a_value": resolution.source_value,
        }
        for field, expected in expected_discrepancy.items():
            if discrepancy.get(field, "") != expected:
                errors.append(
                    f"{resolution.discrepancy_id}: {field}={discrepancy.get(field, '')!r}; expected {expected!r}"
                )

        if discrepancy.get("status", "") not in {"UNDER_REVIEW", "RESOLVED"}:
            errors.append(
                f"{resolution.discrepancy_id}: unexpected status {discrepancy.get('status', '')!r}"
            )

        assertions = assertions_by_game.get(resolution.canonical_game_id, [])
        if len(assertions) != 1:
            errors.append(
                f"{resolution.discrepancy_id}: expected one Vanderbilt assertion; found {len(assertions)}"
            )
            continue
        assertion = assertions[0]
        source = source_by_id.get(assertion.get("source_game_id", ""))
        if source is None:
            errors.append(
                f"{resolution.discrepancy_id}: missing Vanderbilt source row {assertion.get('source_game_id', '')!r}"
            )
            continue

        current_canonical = canonical_field_value(canonical, resolution.field_name)
        if current_canonical not in {resolution.old_canonical, resolution.final_value}:
            errors.append(
                f"{resolution.discrepancy_id}: canonical {resolution.field_name}={current_canonical!r}; expected {resolution.old_canonical!r}"
            )
            continue

        current_source = source_field_value(source, canonical, resolution.field_name)
        if current_source not in {resolution.source_value, resolution.final_value}:
            errors.append(
                f"{resolution.discrepancy_id}: Vanderbilt {resolution.field_name}={current_source!r}; expected {resolution.source_value!r}"
            )
            continue

        before_source = dict(source)
        if current_canonical != resolution.final_value:
            set_canonical_field(canonical, resolution.field_name, resolution.final_value)
            canonical_field_changes += 1

        if resolution.winner == "CANONICAL" and current_source != resolution.final_value:
            set_source_field(source, canonical, resolution.field_name, resolution.final_value)

        if resolution.field_name == "site_type":
            canonical_metadata_changes += apply_site_metadata(
                resolution, canonical, source
            )

        if source != before_source:
            source_rows_changed.add(source["source_game_id"])
            detail = (
                "Owner-approved 2026-08-14 reconciliation: "
                f"{resolution.field_name} normalized to {resolution.final_value}; "
                "raw_text preserved."
            )
            if resolution.discrepancy_id == "DISC-000135":
                detail = (
                    "Owner confirmed on 2026-08-14 that the 1959-02-21 Florida game "
                    "was at Vanderbilt; conflicting series-table marker preserved."
                )
            source["notes"] = append_semicolon(source.get("notes", ""), detail)

        assertions_to_sync[source["source_game_id"]] = (source, assertion)

        discrepancy["canonical_value"] = resolution.final_value
        discrepancy["status"] = "RESOLVED"
        discrepancy["resolution_basis"] = (
            "Owner-approved 2026-08-14 reconciliation: " + resolution.basis
        )
        discrepancy["notes"] = (
            "Canonical corrected to the Vanderbilt-supported value; the competing "
            "source assertion remains preserved."
            if resolution.winner == "SOURCE"
            else "Canonical retained; Vanderbilt curated normalization and assertion "
            "were corrected while raw_text and the original discrepancy value remain preserved."
        )
        if resolution.discrepancy_id == "DISC-000135":
            discrepancy["notes"] = (
                "Owner confirmed Vanderbilt home. Canonical retained; Vanderbilt's curated "
                "site and assertion were corrected while the conflicting series-table A "
                "marker remains preserved in source_site_candidate."
            )
        resolved_count += 1

    if errors:
        print("FAIL: reconciliation preconditions did not match:")
        for error in errors:
            print(f"  - {error}")
        return 1

    for source_game_id, (source, assertion) in assertions_to_sync.items():
        for field in SOURCE_ASSERTION_COPY_FIELDS:
            assertion[field] = source.get(field, "")
        if assertion.get("source_game_id") != source_game_id:
            print(f"FAIL: assertion/source identity drift for {source_game_id}")
            return 1

    source_wins = sum(r.winner == "SOURCE" for r in RESOLUTIONS)
    canonical_wins = len(RESOLUTIONS) - source_wins
    print(f"Discrepancies resolved:      {resolved_count}")
    print(f"Canonical values corrected: {source_wins}")
    print(f"Canonical values retained:  {canonical_wins}")
    print(f"Canonical field writes:     {canonical_field_changes}")
    print(f"Canonical site metadata:    {canonical_metadata_changes} field updates")
    print(f"Vanderbilt source rows:     {len(source_rows_changed)} normalized")
    print(f"Assertions synchronized:    {len(assertions_to_sync)}")
    print("Unresolved Vanderbilt rows: 0")
    print()

    if not args.apply:
        print("DRY RUN COMPLETE: no files changed.")
        print("Re-run with --apply after reviewing these counts.")
        return 0

    write_csv_preserving_format(canonical_path, canonical_fields, canonical_rows)
    write_csv_preserving_format(assertions_path, assertion_fields, assertion_rows)
    write_csv_preserving_format(discrepancies_path, discrepancy_fields, discrepancy_rows)
    write_csv_preserving_format(source_path, source_fields, source_rows)
    update_markdown(notes_path, source_notes_path)

    validator = repo / "tools" / "validate_data.py"
    validation = subprocess.run([sys.executable, str(validator), str(repo)])
    if validation.returncode:
        print("FAIL: reconciliation was written, but validation failed.")
        return validation.returncode

    package_check = subprocess.run(
        [
            sys.executable,
            str(repo / "tools" / "ingest_school.py"),
            "vanderbilt",
            "--check-package",
            "--repo",
            str(repo),
        ]
    )
    if package_check.returncode:
        print("FAIL: reconciliation was written, but the Vanderbilt package check failed.")
        return package_check.returncode

    print()
    print("PASS: all 66 Vanderbilt discrepancies resolved; validation and no-op check succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
