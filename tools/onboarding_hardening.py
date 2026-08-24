#!/usr/bin/env python3
"""Generic hardening helpers for the permanent school-onboarding workflow.

The sealed-plan authority remains ``tools/onboard_school.py``. This companion moves
repeatable work earlier and makes it executable:

- ``research-check``: accept/reject a six-file portfolio before RESEARCH_FROZEN;
- ``fill-review``: expand one compact Gate 1 decision map into review.csv;
- ``carry-forward``: reuse prior owner decisions only when the decision universe is
  substantively identical after a purely technical repair;
- ``rehearse-review``: run the complete disposable transaction and automated gate
  suite before Gate 1 is cryptographically sealed.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import tempfile
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

import onboard_school
from onboarding_plan import REQUIRED_PACKAGE_FILES, WorkflowError, approve_plan


SUBSTANTIVE_REVIEW_FIELDS = (
    "category",
    "source_game_id",
    "season_label",
    "source_game_date",
    "canonical_game_date",
    "matchup",
    "field_name",
    "source_value",
    "canonical_value",
    "relevant_evidence",
    "recommended_action",
    "allowed_actions",
    "canonical_patch_json",
    "source_patch_json",
    "notes",
)

ALLOWED_SITES = {
    "SOURCE_PROGRAM_HOME",
    "OPPONENT_HOME",
    "NEUTRAL",
    "UNKNOWN",
}
ALLOWED_GAME_TYPES = {
    "REGULAR_SEASON",
    "CONFERENCE_TOURNAMENT",
    "NCAA_TOURNAMENT",
    "NIT",
    "POSTSEASON",
}
ALLOWED_NCAA_ROUNDS = {
    "Play-in",
    "R64",
    "R32",
    "Sweet Sixteen",
    "Elite Eight",
    "Final Four",
    "Championship",
}
ROUNDLESS_NCAA_MARKERS = (
    "consolation",
    "third-place",
    "third place",
    "3rd-place",
    "3rd place",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _write_review(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _allowed_actions(row: dict[str, str]) -> set[str]:
    return {
        value.strip()
        for value in row.get("allowed_actions", "").split("|")
        if value.strip()
    }


def _normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").casefold())


def _valid_season(value: str) -> bool:
    match = re.fullmatch(r"(\d{4})-(\d{4})", value or "")
    return bool(match and int(match.group(2)) == int(match.group(1)) + 1)


def _package_root(
    package: Path,
    *,
    expected_sha256: str = "",
) -> tuple[tempfile.TemporaryDirectory[str] | None, Path]:
    expected = sorted(REQUIRED_PACKAGE_FILES)
    if package.is_dir():
        names = sorted(p.name for p in package.iterdir() if p.is_file())
        extras = sorted(p.name for p in package.iterdir() if not p.is_file())
        if names != expected or extras:
            raise WorkflowError(
                "research package directory must contain exactly the six required "
                f"flat files; files={names}, extra_entries={extras}"
            )
        return None, package

    if not package.is_file():
        raise WorkflowError(f"research package not found: {package}")
    if package.suffix.lower() != ".zip":
        raise WorkflowError("research package must be a directory or .zip file")

    actual = sha256_file(package)
    if expected_sha256 and actual.lower() != expected_sha256.lower():
        raise WorkflowError(
            f"research ZIP SHA-256 mismatch: expected {expected_sha256}, found {actual}"
        )

    temporary = tempfile.TemporaryDirectory(prefix="research-portfolio-")
    root = Path(temporary.name)
    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        if sorted(names) != expected or any("/" in name or "\\" in name for name in names):
            temporary.cleanup()
            raise WorkflowError(
                "research ZIP must contain exactly the six required flat members; "
                f"found {names}"
            )
        archive.extractall(root)
    return temporary, root


def research_portfolio_report(
    package: Path,
    *,
    school_key: str,
    expected_sha256: str = "",
) -> dict[str, Any]:
    """Return the permanent pre-RESEARCH_FROZEN acceptance report."""

    temporary, root = _package_root(package, expected_sha256=expected_sha256)
    try:
        game_fields, games = _read_csv(root / "source-games.csv")
        _, opponents = _read_csv(root / "opponents.csv")
        _, venues = _read_csv(root / "venues.csv")
        _, conferences = _read_csv(root / "conferences.csv")

        errors: list[str] = []
        warnings: list[str] = []
        required_game_fields = {
            "source_game_id",
            "source_program_key",
            "season_label",
            "game_date",
            "normalized_opponent_key",
            "team_score",
            "opponent_score",
            "played_result",
            "curated_site_type",
            "curated_venue_name",
            "city",
            "state",
            "curated_game_type",
            "curated_postseason_round",
            "raw_text",
        }
        for field in sorted(required_game_fields - set(game_fields)):
            errors.append(f"source-games.csv missing column: {field}")

        opponent_keys = {
            row.get("canonical_opponent_key", "").strip()
            for row in opponents
            if row.get("canonical_opponent_key", "").strip()
        }

        venue_names: set[str] = set()
        for row in venues:
            owner = row.get("source_program_key", "").strip()
            if owner not in {"", school_key}:
                errors.append(
                    "venues.csv contains row for another source program: " + owner
                )
            city = row.get("city", "").strip()
            state = row.get("state", "").strip()
            if bool(city) != bool(state):
                errors.append(
                    f"venue {row.get('venue_key', '[blank]')}: city/state must be both populated or both blank"
                )
            canonical = row.get("canonical_name", "").strip()
            if canonical:
                venue_names.add(_normalize_name(canonical))
            for alias in row.get("aliases", "").split(";"):
                alias = alias.strip()
                if alias:
                    venue_names.add(_normalize_name(alias))

        source_ids = [row.get("source_game_id", "").strip() for row in games]
        duplicates = sorted(
            value
            for value, count in Counter(source_ids).items()
            if value and count > 1
        )
        if any(not value for value in source_ids):
            errors.append("source-games.csv contains blank source_game_id")
        if duplicates:
            errors.append(
                "duplicate source_game_id values: " + ", ".join(duplicates[:10])
            )

        site_counts: Counter[str] = Counter()
        type_counts: Counter[str] = Counter()
        unknown_dates = 0
        unknown_scores = 0
        unresolved_opponents = 0
        ncaa_rows = 0

        for line_number, row in enumerate(games, start=2):
            label = row.get("source_game_id", "").strip() or f"line {line_number}"
            if row.get("source_program_key", "").strip() != school_key:
                errors.append(f"{label}: wrong source_program_key")

            season = row.get("season_label", "").strip()
            if not _valid_season(season):
                errors.append(f"{label}: invalid season_label {season!r}")
            game_date = row.get("game_date", "").strip()
            if not game_date:
                unknown_dates += 1
            else:
                try:
                    dt.date.fromisoformat(game_date)
                except ValueError:
                    errors.append(f"{label}: invalid ISO game_date {game_date!r}")

            team_score = row.get("team_score", "").strip()
            opp_score = row.get("opponent_score", "").strip()
            if bool(team_score) != bool(opp_score):
                errors.append(f"{label}: only one score is populated")
            if not team_score and not opp_score:
                unknown_scores += 1
            elif team_score and opp_score:
                try:
                    int(team_score)
                    int(opp_score)
                except ValueError:
                    errors.append(f"{label}: score is not an integer")

            opponent = row.get("normalized_opponent_key", "").strip()
            if not opponent or opponent not in opponent_keys:
                unresolved_opponents += 1
                detail = "blank" if not opponent else repr(opponent)
                errors.append(
                    f"{label}: normalized opponent {detail} is not resolved in opponents.csv"
                )

            site = row.get("curated_site_type", "").strip().upper()
            site_counts[site] += 1
            if site not in ALLOWED_SITES:
                errors.append(f"{label}: invalid curated_site_type {site!r}")

            city = row.get("city", "").strip()
            state = row.get("state", "").strip()
            if bool(city) != bool(state):
                errors.append(
                    f"{label}: normalized city/state must be both populated or both blank"
                )

            game_type = row.get("curated_game_type", "").strip()
            type_counts[game_type] += 1
            if game_type not in ALLOWED_GAME_TYPES:
                errors.append(f"{label}: invalid curated_game_type {game_type!r}")

            round_name = row.get("curated_postseason_round", "").strip()
            venue = row.get("curated_venue_name", "").strip()
            if venue and _normalize_name(venue) not in venue_names:
                errors.append(f"{label}: curated venue {venue!r} absent from venues.csv")

            if game_type == "NCAA_TOURNAMENT":
                ncaa_rows += 1
                for field, value in (
                    ("curated_venue_name", venue),
                    ("city", city),
                    ("state", state),
                ):
                    if not value:
                        errors.append(
                            f"{label}: NCAA Tournament research freeze requires {field}"
                        )
                if round_name and round_name not in ALLOWED_NCAA_ROUNDS:
                    errors.append(
                        f"{label}: invalid NCAA curated_postseason_round {round_name!r}"
                    )
                if not round_name:
                    round_audit = " ".join(
                        [
                            row.get("source_round", ""),
                            row.get("event_or_tournament", ""),
                            row.get("raw_text", ""),
                            row.get("notes", ""),
                        ]
                    ).casefold()
                    if not any(marker in round_audit for marker in ROUNDLESS_NCAA_MARKERS):
                        errors.append(
                            f"{label}: NCAA Tournament research freeze requires a curated postseason round unless source evidence explicitly identifies a consolation/third-place game"
                        )
            elif game_type == "REGULAR_SEASON" and round_name:
                errors.append(
                    f"{label}: regular-season game has postseason round {round_name!r}"
                )
            elif game_type in {"CONFERENCE_TOURNAMENT", "NIT", "POSTSEASON"}:
                if round_name not in {"", "Championship"}:
                    errors.append(
                        f"{label}: {game_type} round must be blank or Championship"
                    )

            exhibition_text = " ".join(
                [
                    row.get("raw_text", ""),
                    row.get("event_or_tournament", ""),
                    row.get("source_opponent_label", ""),
                ]
            ).casefold()
            if "exhib" in exhibition_text:
                errors.append(
                    f"{label}: exhibition-like wording remains in competitive research package"
                )

        return {
            "status": "PASS" if not errors else "FAIL",
            "school_key": school_key,
            "package": str(package),
            "zip_sha256": sha256_file(package) if package.is_file() else "",
            "errors": errors,
            "warnings": warnings,
            "counts": {
                "competitive_games": len(games),
                "opponent_rows": len(opponents),
                "venue_rows": len(venues),
                "conference_rows": len(conferences),
                "unresolved_opponents": unresolved_opponents,
                "unknown_exact_dates": unknown_dates,
                "unknown_played_scores": unknown_scores,
                "ncaa_rows": ncaa_rows,
                "site_types": dict(sorted(site_counts.items())),
                "game_types": dict(sorted(type_counts.items())),
            },
        }
    finally:
        if temporary is not None:
            temporary.cleanup()


def print_research_report(report: dict[str, Any]) -> None:
    counts = report["counts"]
    print("College Basketball History — research portfolio acceptance")
    print(f"School:               {report['school_key']}")
    print(f"Status:               {report['status']}")
    print(f"Competitive games:    {counts['competitive_games']:,}")
    print(f"Opponent rows:        {counts['opponent_rows']:,}")
    print(f"Venue rows:           {counts['venue_rows']:,}")
    print(f"NCAA rows:            {counts['ncaa_rows']:,}")
    print(f"Unresolved opponents: {counts['unresolved_opponents']:,}")
    print(f"Unknown exact dates:  {counts['unknown_exact_dates']:,}")
    print(f"Unknown scores:       {counts['unknown_played_scores']:,}")
    print("Site types:           " + json.dumps(counts["site_types"], sort_keys=True))
    print("Game types:           " + json.dumps(counts["game_types"], sort_keys=True))
    if report.get("zip_sha256"):
        print(f"ZIP SHA-256:          {report['zip_sha256']}")
    if report["errors"]:
        print(f"\nFAIL ({len(report['errors'])} errors):")
        for error in report["errors"]:
            print("  - " + error)
    else:
        print("\nPASS: portfolio satisfies the permanent RESEARCH_FROZEN acceptance gate.")


def _decision_map(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise WorkflowError("decision map must be a JSON object")
    return data


def fill_review_from_map(review_path: Path, map_path: Path) -> Counter[str]:
    """Fill review.csv from one compact owner-approved decision map."""

    with review_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    decision_map = _decision_map(map_path)
    identities = decision_map.get("identity", {})
    explicit = decision_map.get("decisions", {})
    bases = decision_map.get("basis_by_decision", {})
    defaults = decision_map.get("defaults", {})
    if not all(isinstance(value, dict) for value in (identities, explicit, bases, defaults)):
        raise WorkflowError(
            "identity, decisions, basis_by_decision, and defaults must be JSON objects"
        )

    default_discrepancy = str(defaults.get("discrepancy", "")).strip()
    default_selected_conditional = str(
        defaults.get("selected_conditional", "")
    ).strip()
    default_basis = str(defaults.get("basis", "")).strip()
    identity_basis = str(defaults.get("identity_basis", default_basis)).strip()
    not_applicable_basis = str(
        defaults.get(
            "not_applicable_basis",
            "Owner Gate 1 approved: this conditional discrepancy belongs to an unselected canonical identity candidate, or the source game was approved as FORCE_NEW.",
        )
    ).strip()

    selected_by_source: dict[str, str | None] = {}
    for row in rows:
        if row.get("category") != "identity":
            continue
        did = row["decision_id"]
        sid = row["source_game_id"]
        action = str(
            explicit.get(did, identities.get(sid, identities.get(did, "")))
        ).strip()
        if action == "FORCE_NEW":
            selected_by_source[sid] = None
        elif action.startswith("MATCH_CANONICAL:"):
            selected_by_source[sid] = action.split(":", 1)[1]
        else:
            raise WorkflowError(
                f"decision map is missing or has invalid identity action for {did}: {action!r}"
            )
        if action not in _allowed_actions(row):
            raise WorkflowError(
                f"{action} is not allowed for {did}; allowed={row['allowed_actions']}"
            )
        basis = str(bases.get(did, identity_basis)).strip()
        if not basis:
            raise WorkflowError(f"missing resolution basis for {did}")
        row["decision"] = action
        row["resolution_basis"] = basis

    for row in rows:
        category = row.get("category", "")
        did = row.get("decision_id", "")
        if category == "identity":
            continue

        action = str(explicit.get(did, "")).strip()
        basis = str(bases.get(did, "")).strip()
        if category == "conditional_discrepancy":
            sid = row.get("source_game_id", "")
            if sid not in selected_by_source:
                raise WorkflowError(
                    f"{did}: conditional discrepancy has no corresponding identity decision"
                )
            match = re.search(r"(CBBG-\d+)", did)
            if not match:
                raise WorkflowError(
                    f"{did}: cannot parse canonical candidate from decision_id"
                )
            candidate = match.group(1)
            selected = selected_by_source[sid]
            if selected is None or candidate != selected:
                action = "NOT_APPLICABLE"
                basis = basis or not_applicable_basis
            elif not action:
                action = default_selected_conditional
                basis = basis or default_basis
        elif category == "discrepancy" and not action:
            action = default_discrepancy
            basis = basis or default_basis
        elif category not in {"discrepancy", "conditional_discrepancy"} and not action:
            raise WorkflowError(
                f"decision map requires explicit action for {did} ({category})"
            )

        if not action:
            raise WorkflowError(f"decision map leaves {did} without an action")
        if action not in _allowed_actions(row):
            raise WorkflowError(
                f"{action} is not allowed for {did}; allowed={row['allowed_actions']}"
            )
        basis = basis or default_basis
        if not basis:
            raise WorkflowError(f"missing resolution basis for {did}")
        row["decision"] = action
        row["resolution_basis"] = basis

    for row in rows:
        if not row.get("decision", "").strip():
            raise WorkflowError(f"blank decision remains for {row['decision_id']}")
        if not row.get("resolution_basis", "").strip():
            raise WorkflowError(
                f"blank resolution_basis remains for {row['decision_id']}"
            )

    _write_review(review_path, fieldnames, rows)
    return Counter(row["decision"] for row in rows)


def carry_forward_review(old_path: Path, new_path: Path) -> Counter[str]:
    """Carry owner decisions forward only across a substantively identical review."""

    with old_path.open(encoding="utf-8-sig", newline="") as handle:
        old_rows = list(csv.DictReader(handle))
    with new_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        new_rows = list(reader)

    if any(not row.get("decision_id", "").strip() for row in old_rows + new_rows):
        raise WorkflowError("review contains blank decision_id values")
    old = {row["decision_id"]: row for row in old_rows}
    new = {row["decision_id"]: row for row in new_rows}
    if len(old) != len(old_rows) or len(new) != len(new_rows):
        raise WorkflowError("review contains duplicate decision_id values")
    if set(old) != set(new):
        missing = sorted(set(old) - set(new))
        added = sorted(set(new) - set(old))
        raise WorkflowError(
            "Gate 1 decision universe changed; "
            + (f"missing={missing[:10]} " if missing else "")
            + (f"added={added[:10]}" if added else "")
        )

    for did in sorted(old):
        for field in SUBSTANTIVE_REVIEW_FIELDS:
            if old[did].get(field, "") != new[did].get(field, ""):
                raise WorkflowError(
                    f"Gate 1 substantive input changed for {did}: {field}"
                )
        decision = old[did].get("decision", "").strip()
        basis = old[did].get("resolution_basis", "").strip()
        if not decision or not basis:
            raise WorkflowError(f"prior review is not fully approved at {did}")
        if decision not in _allowed_actions(new[did]):
            raise WorkflowError(
                f"prior decision no longer allowed for {did}: {decision}"
            )
        new[did]["decision"] = decision
        new[did]["resolution_basis"] = basis

    _write_review(new_path, fieldnames, new_rows)
    return Counter(row["decision"] for row in new_rows)


def rehearse_review(
    repo: Path,
    school_key: str,
    *,
    plan_path: Path,
    review_path: Path,
) -> dict[str, Any]:
    """Run the exact disposable apply transaction before cryptographic sealing."""

    onboard_school.ensure_package_checkpoint(repo)
    approved, approved_hash = approve_plan(
        repo,
        plan_path,
        review_path,
        "technical-readiness",
    )
    before = onboard_school.tree_hashes(repo)
    with tempfile.TemporaryDirectory(prefix=f"preseal-{school_key}-") as temporary:
        rehearsal = Path(temporary) / "repository"
        print(f"Rehearsing filled review in {rehearsal}")
        onboard_school.copy_repository(repo, rehearsal)
        execution = onboard_school.execute_approved_in_place(rehearsal, approved)
        after = onboard_school.tree_hashes(rehearsal)
        changed = onboard_school.changed_paths(before, after)
        forbidden = [
            path
            for path in changed
            if not onboard_school.allowed_apply_path(path, school_key, approved_hash)
        ]
        if forbidden:
            raise WorkflowError(
                "pre-seal rehearsal attempted files outside the apply allow-list:\n  "
                + "\n  ".join(forbidden)
            )
        gates = onboard_school.run_gates(
            rehearsal,
            school_key,
            changed,
            include_tests=True,
        )
    return {
        "approved_plan_hash_preview": approved_hash,
        "changed_paths": changed,
        "execution": execution,
        "gates": gates,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Research-freeze and pre-seal hardening helpers for school onboarding."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    research = sub.add_parser(
        "research-check",
        help="Validate a six-file research portfolio before RESEARCH_FROZEN.",
    )
    research.add_argument("school_key")
    research.add_argument("package", type=Path)
    research.add_argument("--expected-sha256", default="")

    fill = sub.add_parser(
        "fill-review",
        help="Expand a compact Gate 1 decision map into review.csv.",
    )
    fill.add_argument("school_key")
    fill.add_argument("--map", dest="map_path", type=Path, required=True)
    fill.add_argument("--repo", type=Path, default=None)
    fill.add_argument("--review-file", type=Path, default=None)

    carry = sub.add_parser(
        "carry-forward",
        help="Carry prior approved decisions only if the decision universe is unchanged.",
    )
    carry.add_argument("school_key")
    carry.add_argument("--from-review", type=Path, required=True)
    carry.add_argument("--repo", type=Path, default=None)
    carry.add_argument("--review-file", type=Path, default=None)

    rehearse = sub.add_parser(
        "rehearse-review",
        help="Run the full disposable transaction before Gate 1 is sealed.",
    )
    rehearse.add_argument("school_key")
    rehearse.add_argument("--repo", type=Path, default=None)
    rehearse.add_argument("--plan-file", type=Path, default=None)
    rehearse.add_argument("--review-file", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "research-check":
            report = research_portfolio_report(
                args.package.resolve(),
                school_key=args.school_key,
                expected_sha256=args.expected_sha256,
            )
            print_research_report(report)
            return 0 if report["status"] == "PASS" else 1

        repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
        output_dir = repo / ".onboarding" / args.school_key
        review_path = (
            args.review_file.resolve()
            if args.review_file
            else output_dir / "review.csv"
        )

        if args.command == "fill-review":
            counts = fill_review_from_map(review_path, args.map_path.resolve())
            print("PASS: Gate 1 review filled from compact decision map.")
            print("Action counts:")
            for action, count in sorted(counts.items()):
                print(f"  {action}: {count}")
            print("Next: run rehearse-review before sealing Gate 1.")
            return 0

        if args.command == "carry-forward":
            counts = carry_forward_review(args.from_review.resolve(), review_path)
            print(
                "PASS: prior Gate 1 decisions carried forward; decision IDs and substantive inputs are unchanged."
            )
            print("Action counts:")
            for action, count in sorted(counts.items()):
                print(f"  {action}: {count}")
            print("Next: rerun rehearse-review before resealing Gate 1.")
            return 0

        if args.command == "rehearse-review":
            plan_path = (
                args.plan_file.resolve()
                if args.plan_file
                else output_dir / "plan.json"
            )
            result = rehearse_review(
                repo,
                args.school_key,
                plan_path=plan_path,
                review_path=review_path,
            )
            print("\nTECHNICAL READINESS PASSED")
            print("Preview approved-plan hash: " + result["approved_plan_hash_preview"])
            print(f"Changed paths: {len(result['changed_paths']):,}")
            print(
                "The real tracked repository was not changed. Owner Gate 1 may now be sealed with onboard_school.py --approve."
            )
            return 0

        raise WorkflowError(f"unsupported command: {args.command}")
    except (
        WorkflowError,
        FileNotFoundError,
        KeyError,
        ValueError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
    ) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
