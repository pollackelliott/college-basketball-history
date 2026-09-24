#!/usr/bin/env python3
"""Build, validate, and query the owner-maintained conference-tournament site reference.

The repository stores a deterministic gzip-compressed normalized snapshot plus provenance
metadata. A newly supplied owner workbook can refresh that snapshot without requiring Excel,
LibreOffice, openpyxl, or another spreadsheet dependency.
"""
from __future__ import annotations

import argparse
import base64
import csv
import gzip
import hashlib
import io
import json
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITES_OUT = ROOT / "data/reference/conference-tournament-sites.csv.gz.b64"
COVERAGE_OUT = ROOT / "data/reference/conference-tournament-site-coverage.csv"
META_OUT = ROOT / "data/reference/conference-tournament-sites.meta.json"

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
SITE_HEADERS = [
    "Tournament Year", "Season", "Conference Key", "Conference",
    "Shared Tournament Venue", "City", "State",
    "Entire Tournament at Shared Venue?", "Shared Site From Date",
    "Shared Site From Round", "Shared Site Through Date",
    "Shared Site Through Round", "Regular Home Venue for League Team?",
    "Regular Home Program Key (Optional)", "Source URL", "Notes",
]
COVERAGE_HEADERS = ["Conference", "Active in 2027?", "Filled in to completion?", "Notes"]
SITE_FIELDS = [
    "source_row", "tournament_year", "season", "conference_key", "conference",
    "shared_tournament_venue", "city", "state", "entire_tournament_at_shared_venue",
    "shared_site_from_date", "shared_site_from_round", "shared_site_through_date",
    "shared_site_through_round", "regular_home_venue_for_league_team",
    "regular_home_program_key", "source_url", "notes", "reference_status",
]
COVERAGE_FIELDS = ["source_row", "conference", "active_in_2027", "filled_in_to_completion", "notes"]
PLACEHOLDER_VENUES = {"n/a", "tbd", "unknown"}


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _col_index(cell_ref: str) -> int:
    letters = re.match(r"([A-Z]+)", cell_ref)
    if not letters:
        raise ValueError(f"invalid cell reference: {cell_ref}")
    n = 0
    for ch in letters.group(1):
        n = n * 26 + ord(ch) - 64
    return n


def _shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    return ["".join((t.text or "") for t in si.iter(f"{{{NS['m']}}}t")) for si in root.findall("m:si", NS)]


def _sheet_paths(zf: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {r.attrib["Id"]: r.attrib["Target"] for r in rels}
    paths: dict[str, str] = {}
    sheets = workbook.find("m:sheets", NS)
    if sheets is None:
        return paths
    for sheet in sheets:
        rid = sheet.attrib[f"{{{NS['r']}}}id"]
        target = rel_map[rid]
        if target.startswith("/"):
            target = target.lstrip("/")
        elif not target.startswith("xl/"):
            target = "xl/" + target
        paths[sheet.attrib["name"]] = target
    return paths


def _sheet_rows(zf: zipfile.ZipFile, path: str, shared: list[str]) -> list[tuple[int, dict[int, str]]]:
    root = ET.fromstring(zf.read(path))
    sheet_data = root.find("m:sheetData", NS)
    if sheet_data is None:
        return []
    out: list[tuple[int, dict[int, str]]] = []
    for row in sheet_data.findall("m:row", NS):
        row_num = int(row.attrib.get("r", "0") or "0")
        values: dict[int, str] = {}
        for cell in row.findall("m:c", NS):
            idx = _col_index(cell.attrib["r"])
            typ = cell.attrib.get("t")
            value_node = cell.find("m:v", NS)
            inline = cell.find("m:is", NS)
            value = ""
            if typ == "s" and value_node is not None:
                value = shared[int(value_node.text or "0")]
            elif typ == "inlineStr" and inline is not None:
                value = "".join((t.text or "") for t in inline.iter(f"{{{NS['m']}}}t"))
            elif value_node is not None:
                value = value_node.text or ""
            values[idx] = value.strip()
        out.append((row_num, values))
    return out


def _excel_date(value: str) -> str:
    if not value:
        return ""
    if re.fullmatch(r"\d+(?:\.0+)?", value):
        serial = int(float(value))
        return (datetime(1899, 12, 30) + timedelta(days=serial)).date().isoformat()
    return value


def _year(value: str) -> str:
    if re.fullmatch(r"\d+(?:\.0+)?", value or ""):
        return str(int(float(value)))
    return value


def _season_for_year(year: str) -> str:
    y = int(year)
    return f"{y - 1:04d}-{y % 100:02d}"


def _reference_status(record: dict[str, str]) -> str:
    venue = record["shared_tournament_venue"].strip()
    city = record["city"].strip()
    state = record["state"].strip()
    entire = record["entire_tournament_at_shared_venue"].strip()
    venue_l = venue.lower()
    entire_l = entire.lower()
    if "unsure" in entire_l or venue_l in {"tbd", "unknown"}:
        return "UNCERTAIN"
    if venue and venue_l not in PLACEHOLDER_VENUES and city and state and entire_l in {"yes", "no"}:
        return "COMPLETE"
    if any((venue, city, state, entire)):
        return "PARTIAL"
    return "UNRESOLVED"


def parse_workbook(source: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], dict]:
    with zipfile.ZipFile(source) as zf:
        shared = _shared_strings(zf)
        paths = _sheet_paths(zf)
        for required in ("Tournament Sites", "Conference Checklist"):
            if required not in paths:
                raise ValueError(f"missing required worksheet: {required}")
        site_rows = _sheet_rows(zf, paths["Tournament Sites"], shared)
        coverage_rows = _sheet_rows(zf, paths["Conference Checklist"], shared)

    site_header = [site_rows[0][1].get(i, "") for i in range(1, 17)]
    coverage_header = [coverage_rows[0][1].get(i, "") for i in range(1, 5)]
    if site_header != SITE_HEADERS:
        raise ValueError(f"Tournament Sites header drift: {site_header!r}")
    if coverage_header != COVERAGE_HEADERS:
        raise ValueError(f"Conference Checklist header drift: {coverage_header!r}")

    sites: list[dict[str, str]] = []
    for row_num, cells in site_rows[1:]:
        raw = [cells.get(i, "") for i in range(1, 17)]
        if not any(raw):
            continue
        year = _year(raw[0])
        if not year.isdigit():
            raise ValueError(f"row {row_num}: invalid tournament year {raw[0]!r}")
        season = _season_for_year(year)
        if raw[1] and raw[1] != season:
            raise ValueError(f"row {row_num}: season {raw[1]!r} does not match tournament year {year}")
        record = {
            "source_row": str(row_num), "tournament_year": year, "season": season,
            "conference_key": raw[2], "conference": raw[3], "shared_tournament_venue": raw[4],
            "city": raw[5], "state": raw[6], "entire_tournament_at_shared_venue": raw[7],
            "shared_site_from_date": _excel_date(raw[8]), "shared_site_from_round": raw[9],
            "shared_site_through_date": _excel_date(raw[10]), "shared_site_through_round": raw[11],
            "regular_home_venue_for_league_team": raw[12], "regular_home_program_key": raw[13],
            "source_url": raw[14], "notes": raw[15],
        }
        if not record["conference_key"] or not record["conference"]:
            raise ValueError(f"row {row_num}: missing conference key/name")
        record["reference_status"] = _reference_status(record)
        sites.append(record)

    coverage: list[dict[str, str]] = []
    for row_num, cells in coverage_rows[1:]:
        raw = [cells.get(i, "") for i in range(1, 5)]
        if not any(raw):
            continue
        coverage.append({
            "source_row": str(row_num), "conference": raw[0],
            "active_in_2027": "Yes" if raw[1] == "1" else "No" if raw[1] == "0" else raw[1],
            "filled_in_to_completion": "Yes" if raw[2] == "1" else "No" if raw[2] == "0" else raw[2],
            "notes": raw[3],
        })

    statuses = Counter(row["reference_status"] for row in sites)
    years = [int(row["tournament_year"]) for row in sites]
    meta = {
        "schema_version": 1,
        "source_filename": source.name,
        "source_sha256": sha256_path(source),
        "source_sheet": "Tournament Sites",
        "source_table": "ConferenceTournamentSites",
        "source_rows": len(sites),
        "tournament_year_min": min(years), "tournament_year_max": max(years),
        "unique_conference_keys": len({row["conference_key"] for row in sites}),
        "reference_status_counts": dict(sorted(statuses.items())),
        "source_url_populated_rows": sum(1 for row in sites if row["source_url"]),
        "conference_checklist_rows": len(coverage),
        "conference_checklist_complete": sum(1 for row in coverage if row["filled_in_to_completion"] == "Yes"),
        "conference_checklist_incomplete": sum(1 for row in coverage if row["filled_in_to_completion"] == "No"),
        "normalized_snapshot": "data/reference/conference-tournament-sites.csv.gz.b64",
    }
    return sites, coverage, meta


def _csv_text(rows: list[dict[str, str]], fieldnames: list[str]) -> str:
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def refresh_from_workbook(source: Path) -> None:
    sites, coverage, meta = parse_workbook(source)
    csv_bytes = _csv_text(sites, SITE_FIELDS).encode("utf-8")
    compressed = gzip.compress(csv_bytes, compresslevel=9, mtime=0)
    SITES_OUT.write_text(base64.b64encode(compressed).decode("ascii") + "\n", encoding="ascii")
    COVERAGE_OUT.write_text(_csv_text(coverage, COVERAGE_FIELDS), encoding="utf-8")
    META_OUT.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_snapshot() -> list[dict[str, str]]:
    encoded = SITES_OUT.read_text(encoding="ascii").strip()
    csv_text = gzip.decompress(base64.b64decode(encoded)).decode("utf-8")
    return list(csv.DictReader(io.StringIO(csv_text)))


def check_snapshot() -> int:
    rows = load_snapshot()
    meta = json.loads(META_OUT.read_text(encoding="utf-8"))
    with COVERAGE_OUT.open(encoding="utf-8", newline="") as f:
        coverage = list(csv.DictReader(f))
    problems = []
    if len(rows) != meta.get("source_rows"):
        problems.append("snapshot row count does not match metadata")
    if len(coverage) != meta.get("conference_checklist_rows"):
        problems.append("coverage row count does not match metadata")
    counts = dict(sorted(Counter(row["reference_status"] for row in rows).items()))
    if counts != meta.get("reference_status_counts"):
        problems.append("reference_status counts do not match metadata")
    for row in rows:
        if row["reference_status"] == "COMPLETE":
            if not (row["shared_tournament_venue"] and row["city"] and row["state"]):
                problems.append(f"COMPLETE row missing exact site: source_row={row['source_row']}")
                break
            if row["entire_tournament_at_shared_venue"].lower() not in {"yes", "no"}:
                problems.append(f"COMPLETE row has unusable scope: source_row={row['source_row']}")
                break
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1
    print("conference-tournament reference: valid")
    return 0


def query_snapshot(conference_key: str | None, season: str | None) -> int:
    rows = load_snapshot()
    if conference_key:
        rows = [r for r in rows if r["conference_key"] == conference_key]
    if season:
        rows = [r for r in rows if r["season"] == season]
    writer = csv.DictWriter(sys.stdout, fieldnames=SITE_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-from-workbook", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--conference-key")
    parser.add_argument("--season")
    args = parser.parse_args()
    if args.refresh_from_workbook:
        refresh_from_workbook(args.refresh_from_workbook)
        print("conference-tournament reference: refreshed")
        return check_snapshot()
    if args.conference_key or args.season:
        return query_snapshot(args.conference_key, args.season)
    return check_snapshot()


if __name__ == "__main__":
    raise SystemExit(main())
