#!/usr/bin/env python3
"""Fail-closed acceptance gate for ALL_HISTORY_EXPANSION Implementation readiness.

This command is intentionally school-agnostic. It validates portfolio invariants that
must remain true as expansion schools migrate one-by-one from LEGACY_TOP_LEVEL_ONLY to
COMPLETE_INSTITUTIONAL, and it authenticates the workflow/orchestration contracts that
previously failed only after a real expansion release reached CI.

It does not mutate repository state.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Iterable, Mapping

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from all_history_expansion_research import (  # noqa: E402
    ExpansionResearchAuthorityError,
    validate_expansion_baseline_program,
)
from program_history import (  # noqa: E402
    history_coverage_errors,
    history_scope_errors,
    publication_history_start,
)

PUBLISHED_STATUSES = {"LEGACY_TOP_LEVEL_ONLY", "COMPLETE_INSTITUTIONAL"}

STALE_TEST_SNIPPETS = {
    "tests/test_all_history_expansion_research.py": (
        "self.assertEqual(len(eligible), 24)",
    ),
    "tests/test_all_history_header_semantics.py": (
        "self.assertEqual(len(complete), 89)",
        "self.assertEqual(len(legacy), 24)",
    ),
    "tests/test_all_history_universe.py": (
        "self.assertEqual(len(complete), 89)",
        "self.assertEqual(synthetic, [])",
    ),
    "tests/test_program_history_scope.py": (
        "test_public_program_pre_scope_games_are_reciprocal_only",
    ),
    "tests/test_published_site_completeness_census.py": (
        "self.assertEqual(len(complete), 89)",
    ),
}

REQUIRED_REMOTE_CONTINUATIONS = (
    "Queue authorized Stage 2 pre-seal continuation",
    "Queue authorized Stage 2 Gate 1 seal continuation",
    "Queue authorized Stage 2 sealed-apply continuation",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def portfolio_errors(programs: Iterable[Mapping[str, str]]) -> tuple[list[str], dict[str, int]]:
    rows = [dict(row) for row in programs]
    published = [
        row for row in rows
        if str(row.get("public_page_enabled", "")).strip() == "Yes"
    ]
    legacy = [
        row for row in published
        if str(row.get("history_coverage_status", "")).strip()
        == "LEGACY_TOP_LEVEL_ONLY"
    ]
    complete = [
        row for row in published
        if str(row.get("history_coverage_status", "")).strip()
        == "COMPLETE_INSTITUTIONAL"
    ]

    errors: list[str] = []
    statuses = {
        str(row.get("history_coverage_status", "")).strip()
        for row in published
    }
    unexpected = sorted(statuses - PUBLISHED_STATUSES)
    if unexpected:
        errors.append("unexpected published coverage statuses: " + ", ".join(unexpected))

    if len(legacy) + len(complete) != len(published):
        errors.append("published portfolio is not partitioned by supported coverage status")

    eligible_keys: set[str] = set()
    for row in rows:
        try:
            validate_expansion_baseline_program(row)
        except ExpansionResearchAuthorityError:
            continue
        eligible_keys.add(str(row.get("program_key", "")).strip())

    legacy_keys = {
        str(row.get("program_key", "")).strip()
        for row in legacy
    }
    if eligible_keys != legacy_keys:
        missing = sorted(legacy_keys - eligible_keys)
        extra = sorted(eligible_keys - legacy_keys)
        errors.append(
            "expansion eligibility must equal the published LEGACY cohort "
            f"(missing={missing}, extra={extra})"
        )

    for row in published:
        key = str(row.get("program_key", "")).strip() or "<missing>"
        try:
            coverage = history_coverage_errors(row, public=True)
            scope = history_scope_errors(row, required=True)
        except (AttributeError, TypeError, ValueError) as exc:
            errors.append(f"{key}: malformed history metadata: {exc}")
            continue
        for problem in coverage + scope:
            errors.append(f"{key}: {problem}")

        status = str(row.get("history_coverage_status", "")).strip()
        try:
            start = publication_history_start(row)
        except ValueError as exc:
            errors.append(f"{key}: publication history start invalid: {exc}")
            continue

        if status == "COMPLETE_INSTITUTIONAL":
            inception = str(row.get("program_inception_season", "")).strip()
            if not inception:
                errors.append(f"{key}: COMPLETE_INSTITUTIONAL missing inception")
            elif start != inception:
                errors.append(
                    f"{key}: COMPLETE_INSTITUTIONAL publication start {start} "
                    f"!= inception {inception}"
                )

    return errors, {
        "published": len(published),
        "legacy": len(legacy),
        "complete": len(complete),
        "eligible": len(eligible_keys),
    }


def workflow_contract_errors(root: Path) -> list[str]:
    errors: list[str] = []
    transaction = (
        root / ".github/workflows/opponent-identity-transaction-validation.yml"
    ).read_text(encoding="utf-8")
    required_transaction = (
        'ref: ${{ github.event.pull_request.head.sha }}',
        'git fetch --no-tags origin "+refs/heads/main:refs/remotes/origin/main"',
        'git merge --no-ff --no-edit "$EXPECTED_HEAD_SHA"',
        'git ls-remote origin refs/heads/main',
        'LIVE_MAIN_STABILITY=PASS',
    )
    for snippet in required_transaction:
        if snippet not in transaction:
            errors.append(f"transaction rehearsal missing live-main contract: {snippet}")

    forbidden_transaction = (
        'refs/pull/${{ github.event.pull_request.number }}/merge',
        'EXPECTED_BASE_SHA: ${{ github.event.pull_request.base.sha }}',
    )
    for snippet in forbidden_transaction:
        if snippet in transaction:
            errors.append(f"transaction rehearsal still trusts stale event merge state: {snippet}")

    remote = (root / ".github/workflows/remote-implementation.yml").read_text(
        encoding="utf-8"
    )
    for step in REQUIRED_REMOTE_CONTINUATIONS:
        if step not in remote:
            errors.append(f"remote Implementation orchestration missing: {step}")
    return errors


def stale_test_contract_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for relative, snippets in STALE_TEST_SNIPPETS.items():
        text = (root / relative).read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet in text:
                errors.append(f"{relative}: stale pre-expansion assumption: {snippet}")
    scope = (root / "tests/test_program_history_scope.py").read_text(encoding="utf-8")
    if "test_games_outside_publication_history_are_reciprocal_only" not in scope:
        errors.append(
            "program-history scope tests must key reciprocal-only behavior to "
            "publication coverage, not top-level scope"
        )
    return errors


def evaluate_repository(root: Path = ROOT) -> tuple[list[str], dict[str, object]]:
    portfolio, summary = portfolio_errors(
        read_csv(root / "data/reference/programs.csv")
    )
    workflow = workflow_contract_errors(root)
    stale = stale_test_contract_errors(root)
    errors = portfolio + workflow + stale
    return errors, {
        "portfolio": summary,
        "workflow_contract": "PASS" if not workflow else "FAIL",
        "stale_test_contract": "PASS" if not stale else "FAIL",
        "status": "PASS" if not errors else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors, summary = evaluate_repository(ROOT)
    payload = {"summary": summary, "errors": errors}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(
            "ALL_HISTORY_EXPANSION_IMPLEMENTATION_ACCEPTANCE="
            + summary["status"]
        )
        print(
            "PUBLISHED={published} COMPLETE={complete} LEGACY={legacy} "
            "ELIGIBLE={eligible}".format(**summary["portfolio"])
        )
        for error in errors:
            print("ERROR:", error)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
