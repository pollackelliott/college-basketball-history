#!/usr/bin/env python3
"""Read-only Implementation Stage 1 reconciliation inventory.

This command discovers the complete current-main venue/program reconciliation
population before any Stage 1 mutation or maintenance PR is attempted.

Normal use:

    python tools/implementation_stage1_inventory.py <school> <research.zip> \
      --expected-sha256 <sha256> \
      --research-base <research_base_sha>

The durable result is written to:
    .onboarding/<school>/stage1-reconciliation.json

A non-PASS inventory is an expected planning result, not a shell failure. The
subsequent guarded staging command will refuse to proceed until the complete
maintenance/ambiguity population is resolved.
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from onboarding_hardening import research_portfolio_report
from onboarding_plan import WorkflowError
from stage_research_portfolio import (
    build_stage1_reconciliation_inventory,
    copy_package,
    ensure_phase0_state,
    load_csv,
    load_existing_school_venues,
    sha256_file,
    write_stage1_reconciliation_inventory,
)
from stage1_reference_reconciliation import load_conference_reconciliation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory all Stage 1 current-main reconciliation work read-only."
    )
    parser.add_argument("school_key")
    parser.add_argument("package", type=Path)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--research-base", required=True)
    parser.add_argument("--conference-reconciliation", type=Path, default=None)
    parser.add_argument("--repo", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    package = args.package.resolve()

    try:
        actual_sha = sha256_file(package)
        if actual_sha.lower() != args.expected_sha256.lower():
            raise WorkflowError(
                f"research ZIP SHA-256 mismatch: expected {args.expected_sha256}, "
                f"found {actual_sha}"
            )

        head, origin_main = ensure_phase0_state(
            repo,
            args.school_key,
            args.research_base,
        )

        acceptance = research_portfolio_report(
            package,
            school_key=args.school_key,
            expected_sha256=args.expected_sha256,
        )
        if acceptance["status"] != "PASS":
            raise WorkflowError(
                "research portfolio acceptance failed with "
                f"{len(acceptance['errors'])} error(s)"
            )

        with tempfile.TemporaryDirectory(
            prefix=f"stage1-inventory-{args.school_key}-"
        ) as temporary:
            package_root = Path(temporary) / "package"
            package_root.mkdir()
            copy_package(package, package_root)

            _, local_venues = load_csv(package_root / "venues.csv")
            _, local_opponents = load_csv(package_root / "opponents.csv")
            conference_fields, local_conferences = load_csv(
                package_root / "conferences.csv"
            )
            _, global_venues = load_csv(repo / "data/reference/venues.csv")
            _, venue_names = load_csv(repo / "data/reference/venue-names.csv")
            _, programs = load_csv(repo / "data/reference/programs.csv")
            _, program_aliases = load_csv(repo / "data/reference/program-names.csv")
            _, global_conferences = load_csv(repo / "data/reference/conferences.csv")
            existing_school_venues = load_existing_school_venues(
                repo,
                exclude_school_key=args.school_key,
            )

            replacement_history, conference_registrations, conference_meta = (
                load_conference_reconciliation(
                    args.conference_reconciliation,
                    school_key=args.school_key,
                    conferences_path=package_root / "conferences.csv",
                    local_fields=conference_fields,
                )
            )
            if replacement_history is not None:
                local_conferences = replacement_history

            report = build_stage1_reconciliation_inventory(
                args.school_key,
                local_venues,
                global_venues,
                venue_names,
                programs,
                program_aliases,
                local_opponents,
                local_conferences=local_conferences,
                global_conferences=global_conferences,
                conference_registrations=conference_registrations,
                existing_school_venues=existing_school_venues,
            )
            report["conference_reconciliation"] = conference_meta
            report["integration_base_sha"] = head
            report["origin_main_sha"] = origin_main
            report["research_base_sha"] = args.research_base
            report["research_zip_sha256"] = actual_sha

            output = write_stage1_reconciliation_inventory(
                repo,
                args.school_key,
                report,
            )

        print("College Basketball History — Implementation Stage 1 inventory")
        print(f"School:                    {args.school_key}")
        print(f"Current protected main:    {origin_main}")
        print(f"Research base:             {args.research_base}")
        print(f"Status:                    {report['status']}")
        print(f"Total blockers:            {report['blocker_count']}")
        print(
            "Shared/global maintenance: "
            f"{report['maintenance_required_count']}"
        )
        print(f"Ambiguous stops:           {report['ambiguous_stop_count']}")
        print(
            "Venue classifications:     "
            + ", ".join(
                f"{key}={value}"
                for key, value in report["venue"]["classification_counts"].items()
            )
        )
        if report["program_alias"]["classification_counts"]:
            print(
                "Program classifications:   "
                + ", ".join(
                    f"{key}={value}"
                    for key, value
                    in report["program_alias"]["classification_counts"].items()
                )
            )
        if report["conference"]["classification_counts"]:
            print(
                "Conference classifications:"
                + " "
                + ", ".join(
                    f"{key}={value}"
                    for key, value
                    in report["conference"]["classification_counts"].items()
                )
            )
        print(f"Artifact:                  {output}")

        if report["status"] == "PASS":
            print(
                "Next: run the guarded Stage 1 staging command once; mutation remains "
                "fail-fast."
            )
        elif report["status"] == "MAINTENANCE_REQUIRED":
            print(
                "Next: present one consolidated shared/global maintenance scope before "
                "any protected-main maintenance mutation; do not repair blockers serially."
            )
        else:
            print(
                "Next: resolve the complete ambiguity population before staging; do not "
                "use repeated Phase 0 attempts as discovery."
            )
        return 0

    except (WorkflowError, FileNotFoundError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
