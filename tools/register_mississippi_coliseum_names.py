#!/usr/bin/env python3
"""Register Mississippi Coliseum display/alias names after venue creation.

The global physical-venue registry is two-layered: ``venues.csv`` owns physical
identity/geography, while ``venue-names.csv`` owns the project display name and
historical/alias names.  Mississippi State HOME remediation creates VEN-000343;
this helper makes that new identity reference-complete before site-data rebuild.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from venue_reference import load_global_venue_reference, normalized_venue_name


VENUE_ID = "VEN-000343"
VENUE_KEY = "mississippi-coliseum"
DISPLAY_NAME = "Mississippi Coliseum"
ALIAS = "The Big House"
CITY = "Jackson"
STATE = "MS"

DISPLAY_BASIS = (
    "Mississippi State Athletics official Jackson basketball history identifies "
    "Mississippi Coliseum as the Jackson venue beginning 1962-12-15; Mississippi "
    "Fairgrounds history corroborates the building as a 1962 facility."
)
ALIAS_BASIS = (
    "Mississippi State Athletics, 2021-12-21, 'Bulldogs Back In The Big House,' "
    "explicitly identifies Mississippi Coliseum in Jackson as 'The Big House'."
)


class VenueNameRegistrationError(RuntimeError):
    pass


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv_preserving(
    path: Path,
    fields: list[str],
    rows: list[dict[str, str]],
) -> None:
    original = path.read_bytes()
    has_bom = original.startswith(b"\xef\xbb\xbf")
    line_ending = "\r\n" if b"\r\n" in original else "\n"
    encoding = "utf-8-sig" if has_bom else "utf-8"
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator=line_ending)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
    temp.replace(path)


def expected_rows() -> list[dict[str, str]]:
    return [
        {
            "venue_id": VENUE_ID,
            "venue_name": DISPLAY_NAME,
            "normalized_name": normalized_venue_name(DISPLAY_NAME),
            "name_type": "PROJECT_DISPLAY",
            "valid_from": "",
            "valid_to": "",
            "date_precision": "",
            "source_basis": DISPLAY_BASIS,
            "notes": (
                "Registered with Mississippi State historical HOME-site remediation; "
                "physical identity begins from the supported 1962 building chronology."
            ),
        },
        {
            "venue_id": VENUE_ID,
            "venue_name": ALIAS,
            "normalized_name": normalized_venue_name(ALIAS),
            "name_type": "HISTORICAL_OR_ALIAS",
            "valid_from": "",
            "valid_to": "",
            "date_precision": "",
            "source_basis": ALIAS_BASIS,
            "notes": "Mississippi State Athletics-supported nickname for Mississippi Coliseum.",
        },
    ]


def register(repo: Path, *, apply: bool) -> dict[str, int | str]:
    venue_path = repo / "data/reference/venues.csv"
    names_path = repo / "data/reference/venue-names.csv"

    _, venues = read_csv(venue_path)
    fields, names = read_csv(names_path)

    venue_matches = [r for r in venues if r.get("venue_id", "").strip() == VENUE_ID]
    if len(venue_matches) != 1:
        raise VenueNameRegistrationError(
            f"{VENUE_ID}: expected exactly one physical venue row; found {len(venue_matches)}"
        )
    venue = venue_matches[0]
    expected_identity = {
        "venue_key": VENUE_KEY,
        "display_name": DISPLAY_NAME,
        "city": CITY,
        "state": STATE,
    }
    for field, expected in expected_identity.items():
        actual = venue.get(field, "").strip()
        if actual != expected:
            raise VenueNameRegistrationError(
                f"{VENUE_ID}: {field} drift: {actual!r} != {expected!r}"
            )

    desired = expected_rows()
    existing_by_normalized: dict[str, list[dict[str, str]]] = {}
    for row in names:
        if row.get("venue_id", "").strip() != VENUE_ID:
            continue
        existing_by_normalized.setdefault(
            row.get("normalized_name", "").strip(), []
        ).append(row)

    added = 0
    for expected in desired:
        normalized = expected["normalized_name"]
        matches = existing_by_normalized.get(normalized, [])
        if len(matches) > 1:
            raise VenueNameRegistrationError(
                f"{VENUE_ID}/{normalized}: duplicate venue-name rows"
            )
        if matches:
            row = matches[0]
            for field in ("venue_name", "name_type"):
                if row.get(field, "").strip() != expected[field]:
                    raise VenueNameRegistrationError(
                        f"{VENUE_ID}/{normalized}: conflicting {field}"
                    )
            continue
        names.append(expected)
        existing_by_normalized[normalized] = [expected]
        added += 1

    display_rows = [
        r for r in names
        if r.get("venue_id", "").strip() == VENUE_ID
        and r.get("name_type", "").strip() == "PROJECT_DISPLAY"
    ]
    if len(display_rows) != 1:
        raise VenueNameRegistrationError(
            f"{VENUE_ID}: expected exactly one PROJECT_DISPLAY after planning; "
            f"found {len(display_rows)}"
        )
    if display_rows[0].get("venue_name", "").strip() != DISPLAY_NAME:
        raise VenueNameRegistrationError(
            f"{VENUE_ID}: PROJECT_DISPLAY is not {DISPLAY_NAME!r}"
        )

    if apply and added:
        write_csv_preserving(names_path, fields, names)

    if apply:
        # Full registry validator also proves school/global name linkage can load.
        load_global_venue_reference(repo)

    return {
        "venue_id": VENUE_ID,
        "desired_rows": len(desired),
        "added_rows": added,
        "final_display_rows": len(display_rows),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Register Mississippi Coliseum display and alias names."
    )
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    try:
        result = register(repo, apply=args.apply)
    except (FileNotFoundError, ValueError, VenueNameRegistrationError) as exc:
        print(f"FAIL: {exc}")
        return 1

    print("Mississippi Coliseum global-name registration")
    print(f"Venue ID:             {result['venue_id']}")
    print(f"Desired name rows:    {result['desired_rows']}")
    print(f"Rows to add:          {result['added_rows']}")
    print(f"PROJECT_DISPLAY rows: {result['final_display_rows']}")
    if args.apply:
        print("PASS: global venue names registered and reference layer validates.")
    else:
        print("PASS: read-only registration plan; no tracked file changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
