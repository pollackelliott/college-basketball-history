#!/usr/bin/env python3
"""Build a read-only plan for legacy published-HOME chronology remediation.

This planner is deliberately narrower than generic site propagation.  It may propose
venue/location enrichment only when all of the following are already established:

* the canonical game independently classifies the selected published program HOME;
* exactly one mapped assertion from that home program identifies the source row;
* that source row independently classifies the game SOURCE_PROGRAM_HOME;
* exactly one documented school HOME-venue relationship covers the exact game date;
* the relationship resolves to one matching global venue identity with complete
  registry geography; and
* no retained source/assertion/canonical venue or geography field conflicts with the
  proposed physical venue.

The tool never infers or changes H/A/N.  It never writes basketball data.  Its purpose
is to seal a deterministic candidate/review universe before a separate apply tool is
considered.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


PLAN_VERSION = 1
HOME_EXCEPTION_MARKER = "[RESEARCHED_UNRESOLVED_HOME_VENUE"
SEASON_RE = re.compile(r"^(\d{4})-(\d{4})$")
YEAR_MONTH_RE = re.compile(r"^(\d{4})-(\d{2})$")


class HomeChronologyPlanError(RuntimeError):
    """Raised when planner inputs are malformed rather than merely reviewable."""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def clean(value: Any) -> str:
    return str(value or "").strip()


def _git_head(repo: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "[not-a-git-worktree]"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _payload_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _month_end(year: int, month: int) -> date:
    if month == 12:
        return date(year, 12, 31)
    next_month = date(year, month + 1, 1)
    return date.fromordinal(next_month.toordinal() - 1)


def parse_boundary(value: str, *, end: bool) -> date | None:
    """Parse exact/year/month/basketball-season relationship boundaries.

    A basketball season such as 1923-1924 is interpreted as July 1, 1923 through
    June 30, 1924.  This is intentionally generous around the playing season while
    remaining deterministic for chronology coverage.
    """

    value = clean(value)
    if not value:
        return None

    try:
        return date.fromisoformat(value)
    except ValueError:
        pass

    match = SEASON_RE.fullmatch(value)
    if match:
        first = int(match.group(1))
        second = int(match.group(2))
        if second != first + 1:
            raise HomeChronologyPlanError(f"invalid basketball season boundary {value!r}")
        return date(second, 6, 30) if end else date(first, 7, 1)

    if len(value) == 4 and value.isdigit():
        year = int(value)
        return date(year, 12, 31) if end else date(year, 1, 1)

    match = YEAR_MONTH_RE.fullmatch(value)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        if month < 1 or month > 12:
            raise HomeChronologyPlanError(f"invalid year-month boundary {value!r}")
        return _month_end(year, month) if end else date(year, month, 1)

    raise HomeChronologyPlanError(f"unsupported relationship boundary {value!r}")


def parse_game_date(value: str) -> date | None:
    value = clean(value)
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise HomeChronologyPlanError(f"invalid canonical game_date {value!r}") from exc


def home_team(row: dict[str, str]) -> str:
    site = clean(row.get("site_type"))
    if site == "TEAM_A_HOME":
        return clean(row.get("team_a_key"))
    if site == "TEAM_B_HOME":
        return clean(row.get("team_b_key"))
    return ""


def venue_known(row: dict[str, str]) -> bool:
    return bool(clean(row.get("venue_id")) or clean(row.get("venue_key")))


def location_complete(row: dict[str, str]) -> bool:
    return bool(clean(row.get("site_city")) and clean(row.get("site_state")))


def valid_home_exception_shape(row: dict[str, str]) -> bool:
    return (
        HOME_EXCEPTION_MARKER in clean(row.get("notes"))
        and not venue_known(row)
        and location_complete(row)
    )


def relationship_covers(rel: dict[str, str], game_day: date) -> bool:
    start = parse_boundary(rel.get("relationship_start", ""), end=False)
    end = parse_boundary(rel.get("relationship_end", ""), end=True)
    if start is None and end is None:
        return False
    if start is not None and game_day < start:
        return False
    if end is not None and game_day > end:
        return False
    return True


def _home_relationships(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if "home" in clean(row.get("relationship_type")).lower()
    ]


def _venue_identity(row: dict[str, str]) -> str:
    return clean(row.get("venue_id")) or clean(row.get("venue_key")) or clean(
        row.get("canonical_name")
    )


def _dedupe_relationships(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_identity: dict[str, dict[str, str]] = {}
    for row in rows:
        identity = _venue_identity(row)
        if identity:
            by_identity[identity] = row
    return list(by_identity.values())


def _conflict(current: str, proposed: str) -> bool:
    return bool(clean(current) and clean(proposed) and clean(current) != clean(proposed))


def _blank_patch(row: dict[str, str], desired: dict[str, str]) -> dict[str, str]:
    return {
        field: value
        for field, value in desired.items()
        if value and not clean(row.get(field))
    }


def _registry_identity(
    rel: dict[str, str],
    venues_by_id: dict[str, dict[str, str]],
    venues_by_key: dict[str, dict[str, str]],
) -> tuple[dict[str, str] | None, str | None]:
    venue_id = clean(rel.get("venue_id"))
    venue_key = clean(rel.get("venue_key"))
    if not venue_id or not venue_key:
        return None, "relationship_missing_venue_identity"

    by_id = venues_by_id.get(venue_id)
    by_key = venues_by_key.get(venue_key)
    if by_id is None or by_key is None:
        return None, "venue_missing_from_global_registry"
    if by_id is not by_key:
        return None, "venue_id_key_registry_mismatch"
    if clean(by_id.get("venue_id")) != venue_id or clean(by_id.get("venue_key")) != venue_key:
        return None, "venue_identity_registry_mismatch"
    if not clean(by_id.get("city")) or not clean(by_id.get("state")):
        return None, "venue_registry_missing_geography"

    rel_city = clean(rel.get("city"))
    rel_state = clean(rel.get("state"))
    if rel_city and rel_city != clean(by_id.get("city")):
        return None, "school_venue_city_registry_conflict"
    if rel_state and rel_state != clean(by_id.get("state")):
        return None, "school_venue_state_registry_conflict"

    return by_id, None


def _review(
    reviews: list[dict[str, str]],
    counts: Counter[str],
    *,
    program: str,
    game: dict[str, str],
    reason: str,
    detail: str = "",
) -> None:
    counts[reason] += 1
    reviews.append(
        {
            "program": program,
            "canonical_game_id": clean(game.get("canonical_game_id")),
            "season_label": clean(game.get("season_label")),
            "game_date": clean(game.get("game_date")),
            "reason": reason,
            "detail": detail,
        }
    )


def build_plan(repo: Path, requested_programs: list[str] | None = None) -> dict[str, Any]:
    repo = repo.resolve()
    program_rows = read_csv(repo / "data/reference/programs.csv")
    canonical_rows = read_csv(repo / "data/canonical/games.csv")
    assertion_rows = read_csv(repo / "data/evidence/game-assertions.csv")
    global_venues = read_csv(repo / "data/reference/venues.csv")

    published = {
        clean(row.get("program_key"))
        for row in program_rows
        if clean(row.get("public_page_enabled")).lower() == "yes"
        and clean(row.get("program_key"))
    }
    selected = set(requested_programs or published)
    unknown = sorted(selected - published)
    if unknown:
        raise HomeChronologyPlanError(
            "requested program(s) are not published: " + ", ".join(unknown)
        )

    assertions_by_game_program: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in assertion_rows:
        game_id = clean(row.get("canonical_game_id"))
        program = clean(row.get("source_program_key"))
        if game_id and program:
            assertions_by_game_program[(game_id, program)].append(row)

    venues_by_id = {
        clean(row.get("venue_id")): row
        for row in global_venues
        if clean(row.get("venue_id"))
    }
    venues_by_key = {
        clean(row.get("venue_key")): row
        for row in global_venues
        if clean(row.get("venue_key"))
    }

    school_sources: dict[str, dict[str, dict[str, str]]] = {}
    school_relationships: dict[str, list[dict[str, str]]] = {}
    guarded_paths = {
        "data/reference/programs.csv",
        "data/canonical/games.csv",
        "data/evidence/game-assertions.csv",
        "data/reference/venues.csv",
    }

    for program in sorted(selected):
        source_path = repo / "schools" / program / "source-games.csv"
        venues_path = repo / "schools" / program / "venues.csv"
        source_rows = read_csv(source_path)
        venue_rows = read_csv(venues_path)
        school_sources[program] = {
            clean(row.get("source_game_id")): row
            for row in source_rows
            if clean(row.get("source_game_id"))
        }
        school_relationships[program] = _home_relationships(venue_rows)
        guarded_paths.add(str(source_path.relative_to(repo)))
        guarded_paths.add(str(venues_path.relative_to(repo)))

    candidates: list[dict[str, Any]] = []
    reviews: list[dict[str, str]] = []
    summary_by_program: dict[str, Counter[str]] = {
        program: Counter() for program in sorted(selected)
    }
    review_reasons: Counter[str] = Counter()

    for game in canonical_rows:
        program = home_team(game)
        if program not in selected:
            continue

        missing_venue = not venue_known(game)
        missing_location = not location_complete(game)
        if not (missing_venue or missing_location):
            continue
        if missing_venue and not missing_location and valid_home_exception_shape(game):
            summary_by_program[program]["researched_exception"] += 1
            continue

        summary_by_program[program]["hard_blocker"] += 1
        game_id = clean(game.get("canonical_game_id"))
        mapped_assertions = assertions_by_game_program.get((game_id, program), [])
        if len(mapped_assertions) != 1:
            reason = "missing_home_assertion" if not mapped_assertions else "multiple_home_assertions"
            _review(
                reviews,
                review_reasons,
                program=program,
                game=game,
                reason=reason,
                detail=f"mapped assertions={len(mapped_assertions)}",
            )
            summary_by_program[program]["review"] += 1
            continue

        assertion = mapped_assertions[0]
        source_game_id = clean(assertion.get("source_game_id"))
        source = school_sources[program].get(source_game_id)
        if not source:
            _review(
                reviews,
                review_reasons,
                program=program,
                game=game,
                reason="missing_source_row",
                detail=source_game_id,
            )
            summary_by_program[program]["review"] += 1
            continue

        if clean(source.get("curated_site_type")) != "SOURCE_PROGRAM_HOME":
            _review(
                reviews,
                review_reasons,
                program=program,
                game=game,
                reason="source_not_independently_home",
                detail=clean(source.get("curated_site_type")),
            )
            summary_by_program[program]["review"] += 1
            continue

        game_day = parse_game_date(game.get("game_date", ""))
        if game_day is None:
            _review(
                reviews,
                review_reasons,
                program=program,
                game=game,
                reason="missing_exact_game_date",
            )
            summary_by_program[program]["review"] += 1
            continue

        matches = _dedupe_relationships(
            [
                rel
                for rel in school_relationships[program]
                if relationship_covers(rel, game_day)
            ]
        )
        if not matches:
            _review(
                reviews,
                review_reasons,
                program=program,
                game=game,
                reason="no_home_chronology_match",
            )
            summary_by_program[program]["review"] += 1
            continue
        if len(matches) > 1:
            _review(
                reviews,
                review_reasons,
                program=program,
                game=game,
                reason="ambiguous_home_chronology",
                detail="|".join(sorted(_venue_identity(rel) for rel in matches)),
            )
            summary_by_program[program]["review"] += 1
            continue

        rel = matches[0]
        if not clean(rel.get("source_basis")):
            _review(
                reviews,
                review_reasons,
                program=program,
                game=game,
                reason="chronology_missing_source_basis",
                detail=_venue_identity(rel),
            )
            summary_by_program[program]["review"] += 1
            continue

        registry, registry_error = _registry_identity(rel, venues_by_id, venues_by_key)
        if registry_error or registry is None:
            _review(
                reviews,
                review_reasons,
                program=program,
                game=game,
                reason=registry_error or "venue_registry_error",
                detail=_venue_identity(rel),
            )
            summary_by_program[program]["review"] += 1
            continue

        venue_name = clean(rel.get("canonical_name")) or clean(registry.get("display_name"))
        if not venue_name:
            _review(
                reviews,
                review_reasons,
                program=program,
                game=game,
                reason="chronology_missing_canonical_name",
                detail=_venue_identity(rel),
            )
            summary_by_program[program]["review"] += 1
            continue

        desired_source = {
            "curated_venue_name": venue_name,
            "city": clean(registry.get("city")),
            "state": clean(registry.get("state")),
        }
        desired_assertion = dict(desired_source)
        desired_canonical = {
            "venue_id": clean(registry.get("venue_id")),
            "venue_key": clean(registry.get("venue_key")),
            "site_city": clean(registry.get("city")),
            "site_state": clean(registry.get("state")),
        }

        conflict_fields: list[str] = []
        for field, proposed in desired_source.items():
            if _conflict(source.get(field, ""), proposed):
                conflict_fields.append(f"source.{field}")
        for field, proposed in desired_assertion.items():
            if _conflict(assertion.get(field, ""), proposed):
                conflict_fields.append(f"assertion.{field}")
        for field, proposed in desired_canonical.items():
            if _conflict(game.get(field, ""), proposed):
                conflict_fields.append(f"canonical.{field}")

        if conflict_fields:
            _review(
                reviews,
                review_reasons,
                program=program,
                game=game,
                reason="retained_value_conflict",
                detail="|".join(conflict_fields),
            )
            summary_by_program[program]["review"] += 1
            continue

        source_patch = _blank_patch(source, desired_source)
        assertion_patch = _blank_patch(assertion, desired_assertion)
        canonical_patch = _blank_patch(game, desired_canonical)
        if not canonical_patch:
            raise HomeChronologyPlanError(
                f"{game_id}: hard blocker produced no canonical patch"
            )

        candidate = {
            "program": program,
            "canonical_game_id": game_id,
            "source_game_id": source_game_id,
            "season_label": clean(game.get("season_label")),
            "game_date": clean(game.get("game_date")),
            "canonical_site_type": clean(game.get("site_type")),
            "venue": {
                "venue_id": clean(registry.get("venue_id")),
                "venue_key": clean(registry.get("venue_key")),
                "canonical_name": venue_name,
                "city": clean(registry.get("city")),
                "state": clean(registry.get("state")),
                "relationship_type": clean(rel.get("relationship_type")),
                "relationship_start": clean(rel.get("relationship_start")),
                "relationship_end": clean(rel.get("relationship_end")),
                "source_basis": clean(rel.get("source_basis")),
            },
            "patches": {
                "source": source_patch,
                "assertion": assertion_patch,
                "canonical": canonical_patch,
            },
        }
        candidates.append(candidate)
        summary_by_program[program]["candidate"] += 1

    candidates.sort(key=lambda row: (row["program"], row["canonical_game_id"]))
    reviews.sort(key=lambda row: (row["program"], row["reason"], row["canonical_game_id"]))

    inputs = {
        path: _sha256_file(repo / path)
        for path in sorted(guarded_paths)
        if (repo / path).is_file()
    }
    payload = {
        "plan_version": PLAN_VERSION,
        "git_head": _git_head(repo),
        "selected_programs": sorted(selected),
        "inputs": inputs,
        "candidate_count": len(candidates),
        "review_count": len(reviews),
        "summary_by_program": {
            program: dict(sorted(counts.items()))
            for program, counts in sorted(summary_by_program.items())
        },
        "review_reasons": dict(sorted(review_reasons.items())),
        "candidates": candidates,
        "reviews": reviews,
    }
    return {"sha256": _payload_hash(payload), "payload": payload}


def print_plan(plan: dict[str, Any]) -> None:
    payload = plan["payload"]
    print("College Basketball History — HOME chronology remediation planner")
    print(f"Git HEAD:          {payload['git_head']}")
    print(f"Programs:          {len(payload['selected_programs'])}")
    print(f"Candidates:        {payload['candidate_count']}")
    print(f"Reviews:           {payload['review_count']}")
    print(f"Plan SHA-256:      {plan['sha256']}")
    print()
    print("PROGRAM SUMMARY")
    for program in payload["selected_programs"]:
        counts = payload["summary_by_program"].get(program, {})
        print(
            f"  {program}: hard={counts.get('hard_blocker', 0)} "
            f"candidate={counts.get('candidate', 0)} "
            f"review={counts.get('review', 0)} "
            f"researched_exception={counts.get('researched_exception', 0)}"
        )
    if payload["review_reasons"]:
        print()
        print("REVIEW REASONS")
        for reason, count in sorted(payload["review_reasons"].items()):
            print(f"  {reason}: {count}")
    print()
    print("DRY RUN: no tracked basketball data changed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan guarded legacy HOME venue chronology propagation."
    )
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument(
        "--program",
        action="append",
        default=None,
        help="Published program key; repeat for multiple programs. Defaults to all published.",
    )
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    try:
        plan = build_plan(repo, args.program)
        print_plan(plan)
        if args.output:
            output = args.output.resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(f"Plan artifact:     {output}")
        return 0
    except (HomeChronologyPlanError, FileNotFoundError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
