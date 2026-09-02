#!/usr/bin/env python3
"""Read-only census of opponent-identity debt on published program packages.

The census scans each published program's schools/<key>/opponents.csv and compares
stored opponent identities with the current global program registry and with aliases
that other published packages already resolve to current-D1 programs.

It never mutates basketball data. Findings are review candidates, not automatic
identity merges. Historical aliases and institutional renames still require evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def yes(value: str) -> bool:
    return (value or "").strip().lower() == "yes"


def normalize_name(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def parse_int(value: str, default: int = 0) -> int:
    try:
        return int((value or "").strip())
    except (TypeError, ValueError):
        return default


def season_start(season_label: str) -> int | None:
    value = (season_label or "").strip()
    if len(value) >= 4 and value[:4].isdigit():
        return int(value[:4])
    return None


def earliest_season(values: list[str]) -> str:
    candidates = [value for value in values if value]
    if not candidates:
        return ""
    return min(
        candidates,
        key=lambda value: (
            season_start(value) is None,
            season_start(value) if season_start(value) is not None else 9999,
            value,
        ),
    )


def latest_season(values: list[str]) -> str:
    candidates = [value for value in values if value]
    if not candidates:
        return ""
    return max(
        candidates,
        key=lambda value: (
            season_start(value) is not None,
            season_start(value) if season_start(value) is not None else -1,
            value,
        ),
    )


def _program_display(row: dict[str, str]) -> str:
    return (
        row.get("display_name", "").strip()
        or row.get("program_name", "").strip()
        or row.get("program_key", "").strip()
    )


def _load_published_opponent_rows(
    repo: Path,
    published: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_program_key in sorted(published):
        path = repo / "schools" / source_program_key / "opponents.csv"
        if not path.exists():
            raise FileNotFoundError(
                f"published program {source_program_key} is missing {path}"
            )
        for row in read_csv(path):
            enriched = dict(row)
            enriched["_source_program_key"] = source_program_key
            rows.append(enriched)
    return rows


def build_census(repo: Path) -> dict[str, Any]:
    programs = read_csv(repo / "data/reference/programs.csv")

    all_programs: dict[str, dict[str, str]] = {}
    current_d1: dict[str, dict[str, str]] = {}
    published: dict[str, dict[str, str]] = {}
    current_name_index: dict[str, set[str]] = defaultdict(set)

    for row in programs:
        key = row.get("program_key", "").strip()
        if not key:
            continue
        all_programs[key] = row
        if yes(row.get("current_d1", "")):
            current_d1[key] = row
            for field in ("program_name", "display_name"):
                normalized = normalize_name(row.get(field, ""))
                if normalized:
                    current_name_index[normalized].add(key)
        if yes(row.get("public_page_enabled", "")):
            if not row.get("history_start_season", "").strip():
                raise ValueError(
                    f"published program {key} is missing history_start_season"
                )
            published[key] = row

    if not published:
        raise ValueError("no public_page_enabled programs found")

    opponent_rows = _load_published_opponent_rows(repo, published)

    # Learn only aliases that another published package already resolves to an actual
    # current-D1 registry key. This is evidence for a review trigger, not an automatic
    # merge rule. Ambiguous aliases are intentionally ignored.
    current_alias_index: dict[str, set[str]] = defaultdict(set)
    for row in opponent_rows:
        canonical_key = row.get("canonical_opponent_key", "").strip()
        if canonical_key not in current_d1:
            continue
        for field in ("source_opponent_label", "canonical_opponent_name"):
            normalized = normalize_name(row.get(field, ""))
            if normalized:
                current_alias_index[normalized].add(canonical_key)

    findings: list[dict[str, Any]] = []
    finding_signatures: set[tuple[str, str, str, str]] = set()

    def add_finding(
        priority: str,
        finding_type: str,
        row: dict[str, str],
        *,
        suggested_program_key: str = "",
        basis: str,
    ) -> None:
        source_program_key = row["_source_program_key"]
        source_label = row.get("source_opponent_label", "").strip()
        canonical_key = row.get("canonical_opponent_key", "").strip()
        signature = (
            source_program_key,
            source_label,
            canonical_key,
            finding_type,
        )
        if signature in finding_signatures:
            return
        finding_signatures.add(signature)

        suggested = current_d1.get(suggested_program_key, {})
        findings.append(
            {
                "priority": priority,
                "finding_type": finding_type,
                "source_program_key": source_program_key,
                "source_opponent_label": source_label,
                "canonical_opponent_key": canonical_key,
                "canonical_opponent_name": row.get(
                    "canonical_opponent_name", ""
                ).strip(),
                "opponent_current_d1": row.get("current_d1", "").strip(),
                "games_with_source_label": parse_int(
                    row.get("games_with_source_label", "")
                ),
                "first_season": row.get("first_season", "").strip(),
                "last_season": row.get("last_season", "").strip(),
                "suggested_program_key": suggested_program_key,
                "suggested_program_name": _program_display(suggested)
                if suggested
                else "",
                "basis": basis,
            }
        )

    for row in opponent_rows:
        canonical_key = row.get("canonical_opponent_key", "").strip()
        stored_current_d1 = yes(row.get("current_d1", ""))

        if canonical_key in current_d1:
            if not stored_current_d1:
                add_finding(
                    "P1",
                    "STALE_CURRENT_D1_FLAG",
                    row,
                    suggested_program_key=canonical_key,
                    basis=(
                        "canonical opponent key already exists in the current-D1 "
                        "registry, but this school opponents.csv row does not mark it "
                        "current D1"
                    ),
                )
            continue

        # If the stored key already exists in the global program registry,
        # it represents a known program identity. Do not remap that identity to a
        # different current-D1 program merely because a name/label looks similar.
        # This protects real distinct programs such as Florida Southern, Cornell
        # College, and Monmouth College.
        if canonical_key in all_programs:
            continue

        # A high-confidence current-program split requires the CURATED canonical
        # opponent name itself to match exactly one current-D1 registry identity.
        # A raw source label alone is not strong enough for P0/P1.
        canonical_name = normalize_name(row.get("canonical_opponent_name", ""))
        exact_candidates = current_name_index.get(canonical_name, set())

        if len(exact_candidates) == 1:
            candidate = next(iter(exact_candidates))
            add_finding(
                "P0" if candidate in published else "P1",
                "CURRENT_PROGRAM_NAME_SPLIT",
                row,
                suggested_program_key=candidate,
                basis=(
                    "canonical opponent name exactly matches one current-D1 registry "
                    "program while the stored opponent key is absent from the global "
                    "program registry"
                ),
            )
            continue

        alias_candidates: set[str] = set()
        alias_fields: list[str] = []
        for field in ("source_opponent_label", "canonical_opponent_name"):
            normalized = normalize_name(row.get(field, ""))
            candidates = current_alias_index.get(normalized, set())
            if len(candidates) == 1:
                alias_candidates.update(candidates)
                alias_fields.append(field)

        if len(alias_candidates) == 1:
            candidate = next(iter(alias_candidates))
            add_finding(
                "P2",
                "CROSS_PACKAGE_ALIAS_SPLIT",
                row,
                suggested_program_key=candidate,
                basis=(
                    "normalized "
                    + "/".join(alias_fields)
                    + " is already used elsewhere for one current-D1 program, while "
                    "this row stores a different opponent key"
                ),
            )
            continue

        last_year = season_start(row.get("last_season", ""))
        if (
            not stored_current_d1
            and canonical_key not in current_d1
            and last_year is not None
            and last_year >= 2000
        ):
            add_finding(
                "P3",
                "MODERN_NON_D1_REVIEW",
                row,
                basis=(
                    "non-current opponent identity appears in the 2000s or later; "
                    "review for a renamed/reclassified current program before treating "
                    "it as a durable non-D1 identity"
                ),
            )

    # Detect exact canonical-name splits across published packages. This catches a
    # stale key even when another package already uses the correct current-D1 key.
    canonical_name_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in opponent_rows:
        normalized = normalize_name(row.get("canonical_opponent_name", ""))
        canonical_key = row.get("canonical_opponent_key", "").strip()
        if normalized and canonical_key:
            canonical_name_groups[normalized].append(row)

    for group in canonical_name_groups.values():
        keys = sorted(
            {row.get("canonical_opponent_key", "").strip() for row in group}
        )
        if len(keys) <= 1:
            continue
        current_keys = [key for key in keys if key in current_d1]
        if len(current_keys) != 1:
            continue
        candidate = current_keys[0]
        for row in group:
            canonical_key = row.get("canonical_opponent_key", "").strip()
            if canonical_key == candidate or canonical_key in all_programs:
                continue
            # Do not duplicate a stronger exact-name or alias finding for the same row.
            row_prefix = (
                row["_source_program_key"],
                row.get("source_opponent_label", "").strip(),
                canonical_key,
            )
            if any(signature[:3] == row_prefix for signature in finding_signatures):
                continue
            add_finding(
                "P2",
                "CROSS_PACKAGE_CANONICAL_NAME_SPLIT",
                row,
                suggested_program_key=candidate,
                basis=(
                    "the same normalized canonical opponent name is used under "
                    "multiple keys across published packages, and exactly one of "
                    "those keys is a current-D1 registry identity"
                ),
            )

    # Full inventory of identities that published packages currently treat as non-D1
    # or non-current. This is intentionally broader than the high-priority findings and
    # is the denominator for lower-priority historical cleanup.
    inventory_groups: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "canonical_opponent_key": "",
            "canonical_names": set(),
            "source_labels": set(),
            "published_source_programs": set(),
            "games": 0,
            "first_seasons": [],
            "last_seasons": [],
            "row_count": 0,
        }
    )

    for row in opponent_rows:
        canonical_key = row.get("canonical_opponent_key", "").strip()
        if canonical_key in current_d1 or yes(row.get("current_d1", "")):
            continue
        fallback_name = normalize_name(
            row.get("canonical_opponent_name", "")
            or row.get("source_opponent_label", "")
        )
        inventory_key = canonical_key or f"__blank__:{fallback_name}"
        item = inventory_groups[inventory_key]
        item["canonical_opponent_key"] = canonical_key
        canonical_name = row.get("canonical_opponent_name", "").strip()
        source_label = row.get("source_opponent_label", "").strip()
        if canonical_name:
            item["canonical_names"].add(canonical_name)
        if source_label:
            item["source_labels"].add(source_label)
        item["published_source_programs"].add(row["_source_program_key"])
        item["games"] += parse_int(row.get("games_with_source_label", ""))
        item["first_seasons"].append(row.get("first_season", "").strip())
        item["last_seasons"].append(row.get("last_season", "").strip())
        item["row_count"] += 1

    non_d1_inventory: list[dict[str, Any]] = []
    for item in inventory_groups.values():
        non_d1_inventory.append(
            {
                "canonical_opponent_key": item["canonical_opponent_key"],
                "canonical_names": sorted(item["canonical_names"]),
                "source_labels": sorted(item["source_labels"]),
                "published_source_programs": sorted(
                    item["published_source_programs"]
                ),
                "games": item["games"],
                "first_season": earliest_season(item["first_seasons"]),
                "last_season": latest_season(item["last_seasons"]),
                "row_count": item["row_count"],
            }
        )

    non_d1_inventory.sort(
        key=lambda item: (
            -(season_start(item["last_season"]) or -1),
            -item["games"],
            item["canonical_opponent_key"],
        )
    )

    findings.sort(
        key=lambda finding: (
            PRIORITY_ORDER[finding["priority"]],
            -finding["games_with_source_label"],
            finding["source_program_key"],
            finding["source_opponent_label"],
        )
    )

    priority_counts = Counter(finding["priority"] for finding in findings)

    return {
        "schema_version": 2,
        "published_program_count": len(published),
        "published_program_keys": sorted(published),
        "opponent_rows_scanned": len(opponent_rows),
        "finding_count": len(findings),
        "priority_counts": {
            priority: priority_counts.get(priority, 0)
            for priority in ("P0", "P1", "P2", "P3")
        },
        "findings": findings,
        "non_d1_identity_count": len(non_d1_inventory),
        "non_d1_identity_inventory": non_d1_inventory,
    }


def print_text(report: dict[str, Any], *, example_limit: int = 25) -> None:
    print("College Basketball History — published opponent identity census")
    print(f"Published programs:      {report['published_program_count']}")
    print(f"Opponent rows scanned:   {report['opponent_rows_scanned']:,}")
    print(f"Identity findings:       {report['finding_count']:,}")
    for priority in ("P0", "P1", "P2", "P3"):
        print(
            f"  {priority}:                    "
            f"{report['priority_counts'][priority]:,}"
        )
    print(f"Non-D1 identity ledger:  {report['non_d1_identity_count']:,}")

    if report["findings"]:
        print("\nTop review findings")
        for finding in report["findings"][:example_limit]:
            suggestion = ""
            if finding["suggested_program_key"]:
                suggestion = (
                    f" -> {finding['suggested_program_key']}"
                    f" ({finding['suggested_program_name']})"
                )
            print(
                f"  {finding['priority']} {finding['source_program_key']}: "
                f"{finding['source_opponent_label']!r} "
                f"[{finding['canonical_opponent_key'] or 'BLANK'}]"
                f"{suggestion}; games={finding['games_with_source_label']} "
                f"{finding['first_season']}..{finding['last_season']} "
                f"({finding['finding_type']})"
            )

    inventory = report["non_d1_identity_inventory"]
    if inventory:
        print("\nRecent/high-volume non-D1 identity inventory")
        for item in inventory[:example_limit]:
            names = ", ".join(item["canonical_names"][:2]) or "(unnamed)"
            print(
                f"  {item['canonical_opponent_key'] or 'BLANK'}: {names}; "
                f"games={item['games']} sources={len(item['published_source_programs'])} "
                f"{item['first_season']}..{item['last_season']}"
            )

    print(
        "\nRead-only census: findings require evidence-based review; "
        "nothing was mutated."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only census of published opponent-identity debt"
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: script parent repository)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the complete machine-readable report",
    )
    parser.add_argument(
        "--examples",
        type=int,
        default=25,
        help="number of findings/inventory rows to print in text mode",
    )
    args = parser.parse_args()

    report = build_census(args.repo.resolve())
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text(report, example_limit=max(args.examples, 0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
