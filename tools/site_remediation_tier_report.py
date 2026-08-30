#!/usr/bin/env python3
"""Build a risk-tiered, read-only report for site-completeness remediation Wave A.

The underlying audit intentionally calls every uncontested blank-field candidate
"mechanical".  This report adds an execution-risk distinction before any tracked
basketball data is mutated:

* A0_REGISTRY_GEOGRAPHY — canonical already has an immutable venue_id and the
  global venue registry can complete missing geography without source inference.
* A1_EXISTING_SITE_PROPAGATION — canonical H/A/N is already known; source and/or
  venue-registry evidence can fill only blank venue/location fields.
* A2_UNCONTESTED_SITE_TYPE — canonical H/A/N is UNKNOWN and participant source
  evidence provides exactly one non-conflicting H/A/N value.  These rows may
  also unlock venue/location fills, but changing H/A/N is a materially higher
  semantic action and must remain a separately reviewable class.

This tool never writes tracked basketball data.  Artifacts go under .onboarding.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from location_safety import atomic_location_enrichments, location_pair_status
from site_remediation_audit import build_audit, read_csv


OUTPUT_FIELDS = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "team_a_key",
    "team_b_key",
    "game_type",
    "tier",
    "current_site_type",
    "proposed_site_type",
    "current_venue_id",
    "current_venue_key",
    "proposed_venue_id",
    "proposed_venue_key",
    "current_city",
    "current_state",
    "proposed_city",
    "proposed_state",
    "change_fields",
    "support_classifications",
    "supporting_programs",
    "supporting_source_game_ids",
    "basis",
]


class TierReportError(RuntimeError):
    """Raised when candidate evidence cannot be combined safely."""


def _parse_single_location(value: str) -> tuple[str, str] | None:
    values = [item.strip() for item in (value or "").split("|") if item.strip()]
    if len(values) != 1 or ", " not in values[0]:
        return None
    city, state = values[0].rsplit(", ", 1)
    city = city.strip()
    state = state.strip()
    return (city, state) if city and state else None


def _site_home_team(game: dict[str, str], site_type: str) -> str:
    if site_type == "TEAM_A_HOME":
        return game.get("team_a_key", "").strip()
    if site_type == "TEAM_B_HOME":
        return game.get("team_b_key", "").strip()
    return ""


def _base_plan_row(game: dict[str, str]) -> dict[str, str]:
    return {
        "canonical_game_id": game.get("canonical_game_id", "").strip(),
        "season_label": game.get("season_label", "").strip(),
        "game_date": game.get("game_date", "").strip(),
        "team_a_key": game.get("team_a_key", "").strip(),
        "team_b_key": game.get("team_b_key", "").strip(),
        "game_type": game.get("game_type", "").strip(),
        "tier": "",
        "current_site_type": game.get("site_type", "").strip(),
        "proposed_site_type": "",
        "current_venue_id": game.get("venue_id", "").strip(),
        "current_venue_key": game.get("venue_key", "").strip(),
        "proposed_venue_id": "",
        "proposed_venue_key": "",
        "current_city": game.get("site_city", "").strip(),
        "current_state": game.get("site_state", "").strip(),
        "proposed_city": "",
        "proposed_state": "",
        "change_fields": "",
        "support_classifications": "",
        "supporting_programs": "",
        "supporting_source_game_ids": "",
        "basis": "",
    }


def _combine_values(existing: str, proposed: str, *, label: str, game_id: str) -> str:
    if not proposed:
        return existing
    if existing and existing != proposed:
        raise TierReportError(
            f"{game_id}: conflicting proposed {label}: {existing!r} vs {proposed!r}"
        )
    return proposed


def build_tier_report(repo: Path) -> dict[str, Any]:
    audit = build_audit(repo)
    _, canonical_rows = read_csv(repo / "data/canonical/games.csv")
    _, venue_rows = read_csv(repo / "data/reference/venues.csv")

    canonical_by_id = {
        row.get("canonical_game_id", "").strip(): row
        for row in canonical_rows
        if row.get("canonical_game_id", "").strip()
    }
    venues_by_id = {
        row.get("venue_id", "").strip(): row
        for row in venue_rows
        if row.get("venue_id", "").strip()
    }

    mechanical_by_game: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in audit["mechanical"]:
        mechanical_by_game[row["canonical_game_id"]].append(row)

    partial_location_reviews = {
        row["canonical_game_id"]: row
        for row in audit["review"]
        if row.get("field_name") == "location"
        and row.get("classification") == "PARTIAL_CANONICAL_REVIEW"
    }

    candidate_ids = set(mechanical_by_game)
    candidate_ids.update(
        game_id
        for game_id, game in canonical_by_id.items()
        if game.get("site_type", "").strip() not in {"", "UNKNOWN"}
        and game.get("venue_id", "").strip()
        and location_pair_status(
            game.get("site_city", ""), game.get("site_state", "")
        ) != "complete"
    )
    candidate_ids.update(partial_location_reviews)

    rows: list[dict[str, str]] = []
    review_rows: list[dict[str, str]] = []

    for game_id in sorted(candidate_ids):
        game = canonical_by_id.get(game_id)
        if game is None:
            raise TierReportError(f"candidate references missing canonical game {game_id}")

        audit_rows = mechanical_by_game.get(game_id, [])
        plan = _base_plan_row(game)
        support_classes: set[str] = set()
        support_programs: set[str] = set()
        support_source_ids: set[str] = set()
        bases: list[str] = []

        for item in audit_rows:
            field = item.get("field_name", "")
            support_classes.add(item.get("classification", ""))
            support_programs.update(
                value for value in item.get("supporting_programs", "").split("|") if value
            )
            support_source_ids.update(
                value
                for value in item.get("supporting_source_game_ids", "").split("|")
                if value
            )
            if item.get("reason", ""):
                bases.append(item["reason"])

            if field == "site_type":
                plan["proposed_site_type"] = _combine_values(
                    plan["proposed_site_type"],
                    item.get("proposed_value", "").strip(),
                    label="site_type",
                    game_id=game_id,
                )
            elif field == "venue":
                plan["proposed_venue_id"] = _combine_values(
                    plan["proposed_venue_id"],
                    item.get("proposed_venue_id", "").strip(),
                    label="venue_id",
                    game_id=game_id,
                )
                plan["proposed_venue_key"] = _combine_values(
                    plan["proposed_venue_key"],
                    item.get("proposed_venue_key", "").strip(),
                    label="venue_key",
                    game_id=game_id,
                )
            elif field == "location":
                plan["proposed_city"] = _combine_values(
                    plan["proposed_city"],
                    item.get("proposed_city", "").strip(),
                    label="city",
                    game_id=game_id,
                )
                plan["proposed_state"] = _combine_values(
                    plan["proposed_state"],
                    item.get("proposed_state", "").strip(),
                    label="state",
                    game_id=game_id,
                )

        effective_site = (
            plan["proposed_site_type"] or plan["current_site_type"]
        )
        effective_venue_id = (
            plan["proposed_venue_id"] or plan["current_venue_id"]
        )

        # Canonical physical venue identity owns canonical geography.  If either
        # the canonical row already has an immutable venue_id or this exact audit
        # safely proposes one, use its registry geography to complete blanks.
        venue = venues_by_id.get(effective_venue_id, {}) if effective_venue_id else {}
        registry_city = venue.get("city", "").strip()
        registry_state = venue.get("state", "").strip()
        registry_complete = location_pair_status(registry_city, registry_state) == "complete"

        if effective_site not in {"", "UNKNOWN"} and registry_complete:
            fills = atomic_location_enrichments(
                plan["current_city"],
                plan["current_state"],
                registry_city,
                registry_state,
            )
            if fills:
                fill_map = dict(fills)
                if "site_city" in fill_map:
                    plan["proposed_city"] = _combine_values(
                        plan["proposed_city"],
                        fill_map["site_city"],
                        label="city",
                        game_id=game_id,
                    )
                if "site_state" in fill_map:
                    plan["proposed_state"] = _combine_values(
                        plan["proposed_state"],
                        fill_map["site_state"],
                        label="state",
                        game_id=game_id,
                    )
                support_classes.add("VENUE_REGISTRY_GEOGRAPHY")
                bases.append(
                    f"immutable venue_id {effective_venue_id} supplies canonical registry geography"
                )
            elif location_pair_status(plan["current_city"], plan["current_state"]) == "partial":
                existing = plan["current_city"] or plan["current_state"]
                registry_half = registry_city if plan["current_city"] else registry_state
                if existing and existing != registry_half:
                    review_rows.append(
                        {
                            "canonical_game_id": game_id,
                            "classification": "PARTIAL_LOCATION_REGISTRY_CONFLICT",
                            "current_location": f"{plan['current_city']}, {plan['current_state']}",
                            "evidence": f"{registry_city}, {registry_state}",
                            "reason": "existing canonical half-location conflicts with immutable venue registry",
                        }
                    )

        # A complete, uncontested source pair may safely fill the missing half of
        # a partial canonical location when it matches the half already retained.
        partial = partial_location_reviews.get(game_id)
        if partial and effective_site not in {"", "UNKNOWN"}:
            source_pair = _parse_single_location(partial.get("evidence_values", ""))
            if source_pair:
                source_city, source_state = source_pair
                fills = atomic_location_enrichments(
                    plan["current_city"],
                    plan["current_state"],
                    source_city,
                    source_state,
                )
                if fills:
                    # If venue registry geography is available, it is canonical.
                    # Source evidence may supplement only when it does not disagree.
                    if registry_complete and (source_city, source_state) != (
                        registry_city,
                        registry_state,
                    ):
                        review_rows.append(
                            {
                                "canonical_game_id": game_id,
                                "classification": "SOURCE_LOCATION_REGISTRY_CONFLICT",
                                "current_location": f"{plan['current_city']}, {plan['current_state']}",
                                "evidence": f"source={source_city}, {source_state}; registry={registry_city}, {registry_state}",
                                "reason": "source location disagrees with canonical physical venue registry",
                            }
                        )
                    else:
                        fill_map = dict(fills)
                        if "site_city" in fill_map:
                            plan["proposed_city"] = _combine_values(
                                plan["proposed_city"],
                                fill_map["site_city"],
                                label="city",
                                game_id=game_id,
                            )
                        if "site_state" in fill_map:
                            plan["proposed_state"] = _combine_values(
                                plan["proposed_state"],
                                fill_map["site_state"],
                                label="state",
                                game_id=game_id,
                            )
                        support_classes.add("PARTIAL_LOCATION_COMPLETION")
                        support_programs.update(
                            value
                            for value in partial.get("supporting_programs", "").split("|")
                            if value
                        )
                        support_source_ids.update(
                            value
                            for value in partial.get("supporting_source_game_ids", "").split("|")
                            if value
                        )
                        bases.append(
                            "complete source location matches retained canonical half and completes the pair"
                        )

        changes: list[str] = []
        if plan["proposed_site_type"]:
            if plan["current_site_type"] not in {"", "UNKNOWN"}:
                raise TierReportError(
                    f"{game_id}: site_type proposal would overwrite known canonical site"
                )
            changes.append("site_type")
        if plan["proposed_venue_id"] or plan["proposed_venue_key"]:
            if plan["current_venue_id"] or plan["current_venue_key"]:
                raise TierReportError(
                    f"{game_id}: venue proposal would overwrite known canonical venue"
                )
            if not (plan["proposed_venue_id"] and plan["proposed_venue_key"]):
                raise TierReportError(
                    f"{game_id}: venue proposal is not an atomic venue_id/venue_key pair"
                )
            changes.append("venue")
        if plan["proposed_city"]:
            if plan["current_city"]:
                raise TierReportError(f"{game_id}: city proposal would overwrite canonical city")
            changes.append("site_city")
        if plan["proposed_state"]:
            if plan["current_state"]:
                raise TierReportError(f"{game_id}: state proposal would overwrite canonical state")
            changes.append("site_state")

        if not changes:
            continue

        if "site_type" in changes:
            plan["tier"] = "A2_UNCONTESTED_SITE_TYPE"
        elif audit_rows:
            plan["tier"] = "A1_EXISTING_SITE_PROPAGATION"
        else:
            plan["tier"] = "A0_REGISTRY_GEOGRAPHY"

        plan["change_fields"] = "|".join(changes)
        plan["support_classifications"] = "|".join(sorted(support_classes - {""}))
        plan["supporting_programs"] = "|".join(sorted(support_programs))
        plan["supporting_source_game_ids"] = "|".join(sorted(support_source_ids))
        plan["basis"] = " | ".join(dict.fromkeys(bases))

        proposed_site = plan["proposed_site_type"] or plan["current_site_type"]
        if proposed_site in {"TEAM_A_HOME", "TEAM_B_HOME"}:
            home_team = _site_home_team(game, proposed_site)
            if not home_team:
                raise TierReportError(f"{game_id}: proposed home site has no home team")

        rows.append(plan)

    rows.sort(key=lambda row: (row["tier"], row["canonical_game_id"]))
    review_rows.sort(
        key=lambda row: (row["classification"], row["canonical_game_id"])
    )

    counts: Counter[str] = Counter()
    programs: Counter[str] = Counter()
    decades: Counter[str] = Counter()
    for row in rows:
        counts[f"tier:{row['tier']}"] += 1
        counts[f"bundle:{row['tier']}:{row['change_fields']}"] += 1
        for program in (row["team_a_key"], row["team_b_key"]):
            if program:
                programs[program] += 1
        season = row.get("season_label", "")
        if len(season) >= 4 and season[:4].isdigit():
            decade = f"{season[:3]}0s"
            decades[decade] += 1

    return {
        "rows": rows,
        "review_rows": review_rows,
        "summary": {
            "candidate_games": len(rows),
            "audit_mechanical_games": audit["summary"].get("mechanical_game_candidates", 0),
            "audit_mechanical_field_rows": audit["summary"].get("mechanical_field_candidates", 0),
            "supplemental_review_rows": len(review_rows),
            "counts": dict(sorted(counts.items())),
            "program_involvement": dict(sorted(programs.items(), key=lambda item: (-item[1], item[0]))),
            "decades": dict(sorted(decades.items())),
        },
    }


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "tiered-candidates.csv", OUTPUT_FIELDS, report["rows"])
    review_fields = [
        "canonical_game_id",
        "classification",
        "current_location",
        "evidence",
        "reason",
    ]
    _write_csv(output_dir / "tiered-review.csv", review_fields, report["review_rows"])
    (output_dir / "tier-summary.json").write_text(
        json.dumps(report["summary"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def print_summary(report: dict[str, Any], output_dir: Path) -> None:
    summary = report["summary"]
    print("College Basketball History — site remediation risk tiers")
    print(f"Candidate games:               {summary['candidate_games']:,}")
    print(f"Audit mechanical games:        {summary['audit_mechanical_games']:,}")
    print(f"Audit mechanical field rows:   {summary['audit_mechanical_field_rows']:,}")
    print(f"Supplemental review rows:       {summary['supplemental_review_rows']:,}")
    for key, value in summary["counts"].items():
        print(f"  {key}: {value:,}")
    print(f"Artifacts: {output_dir}")
    print("PASS: tiering only; no tracked basketball data was changed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build read-only Wave A remediation risk tiers.")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else repo / ".onboarding" / "site-remediation-wave-a"
    )
    try:
        report = build_tier_report(repo)
        write_report(report, output_dir)
        print_summary(report, output_dir)
        return 0
    except (FileNotFoundError, ValueError, KeyError, TierReportError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
