#!/usr/bin/env python3
"""Deterministic checkpoint-only Stage 3A-0 entry/readiness and census/partition."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import zipfile
from collections import Counter
from pathlib import Path

REGULAR = {"REGULAR_SEASON", "REGULAR", "RS"}
POST = {
    "POSTSEASON",
    "NCAA",
    "NIT",
    "CONFERENCE_TOURNAMENT",
    "OTHER_POSTSEASON",
    "CBI",
    "CIT",
    "CROWN",
}
HOME = {"HOME", "TEAM_HOME", "TARGET_HOME"}
AWAY = {"AWAY", "OPPONENT_HOME", "OPP_HOME", "ROAD"}
NEUTRAL = {"NEUTRAL", "N"}
UNKNOWN_SITE = {"UNKNOWN", "UNK", "?"}

LEDGER_BASENAMES = (
    "structured-stage2-ledger.csv",
    "structured-stage2-ledger-with-game-type.csv",
    "stage2-ledger.csv",
    "stage2-working-ledger.csv",
)
ID_FIELDS = ("research_game_id", "source_game_id", "game_id", "id")
OPP_FIELDS = ("opponent_key", "opponent_program_key")
SOURCE_OPP_LABEL_FIELDS = (
    "source_opponent_label",
    "mechanical_family_label",
    "source_opponent_field",
    "opponent_label",
)
MAPPING_KEY_FIELDS = (
    "proposed_program_key",
    "canonical_opponent_key",
    "canonical_opponent_key_if_resolved",
    "opponent_key",
    "opponent_program_key",
)
COUNT_FIELDS = ("game_count", "games")
SITE_FIELDS = ("site_type", "site", "han", "home_away_neutral")
SEASON_FIELDS = ("season_label", "season")
GAME_TYPE_FIELDS = ("game_type", "season_type", "competition_type")
RAW_SITE_FIELDS = ("source_site_token", "raw_site_token")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def csv_bytes(data: bytes) -> list[dict[str, str]]:
    with io.TextIOWrapper(io.BytesIO(data), encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_header(archive: zipfile.ZipFile, member: str) -> list[str]:
    with archive.open(member) as raw, io.TextIOWrapper(
        raw, encoding="utf-8-sig", newline=""
    ) as handle:
        return next(csv.reader(handle), [])


def pick(row: dict[str, str], *names: str) -> str:
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def rid(row: dict[str, str]) -> str:
    return pick(row, *ID_FIELDS)


def source_label(row: dict[str, str]) -> str:
    return pick(row, *SOURCE_OPP_LABEL_FIELDS)


def game_class(value: str) -> str:
    normalized = (value or "").strip().upper()
    if normalized in REGULAR:
        return "REGULAR_SEASON"
    if normalized in POST:
        return "POSTSEASON"
    return "UNCLASSIFIED"


def site_class(value: str) -> str:
    normalized = (value or "").strip().upper()
    if normalized in HOME:
        return "HOME"
    if normalized in AWAY:
        return "OPPONENT_HOME"
    if normalized in NEUTRAL:
        return "NEUTRAL"
    if normalized in UNKNOWN_SITE:
        return "UNKNOWN"
    return "INVALID"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_sha() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def dump(out: Path, name: str, obj: object) -> Path:
    path = out / name
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_csv(path: Path, data: list[dict[str, str]]) -> None:
    if not data:
        raise ValueError("EMPTY_GAME_LEDGER")
    fields: list[str] = []
    seen: set[str] = set()
    for row in data:
        for field in row:
            if field not in seen:
                seen.add(field)
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)


def ledger_header_score(header: list[str], name: str) -> int:
    fields = set(header)
    required = (
        any(field in fields for field in ID_FIELDS),
        any(field in fields for field in OPP_FIELDS),
        any(field in fields for field in SEASON_FIELDS),
        any(field in fields for field in GAME_TYPE_FIELDS),
    )
    if not all(required):
        return -1
    score = sum(required)
    low = name.lower()
    if "stage2" in low:
        score += 2
    if "ledger" in low:
        score += 2
    if any(field in fields for field in SITE_FIELDS):
        score += 1
    return score


def legacy_game_ledger_score(header: list[str], name: str) -> int:
    fields = set(header)
    required = (
        any(field in fields for field in ID_FIELDS),
        any(field in fields for field in SOURCE_OPP_LABEL_FIELDS),
        any(field in fields for field in SEASON_FIELDS),
        any(field in fields for field in GAME_TYPE_FIELDS),
    )
    if not all(required):
        return -1
    if any(field in fields for field in OPP_FIELDS):
        return -1
    score = sum(required)
    low = name.lower()
    if "stage1" in low:
        score += 2
    if "ledger" in low:
        score += 2
    if "working" in low:
        score += 1
    return score


def mapping_header_score(header: list[str], name: str) -> int:
    fields = set(header)
    required = (
        any(field in fields for field in SOURCE_OPP_LABEL_FIELDS),
        any(field in fields for field in MAPPING_KEY_FIELDS),
    )
    if not all(required):
        return -1
    score = sum(required)
    low = name.lower()
    if "stage2" in low:
        score += 2
    if "opponent" in low:
        score += 1
    if "census" in low or "reconciliation" in low:
        score += 1
    return score


def normalize_site_unknowns(
    ledger: list[dict[str, str]],
) -> tuple[list[dict[str, str]], int]:
    defaulted = 0
    normalized: list[dict[str, str]] = []
    for row in ledger:
        copy = dict(row)
        if not pick(copy, *SITE_FIELDS):
            copy["site_type"] = "UNKNOWN"
            defaulted += 1
        normalized.append(copy)
    return normalized, defaulted


def build_complete_label_map(
    archive: zipfile.ZipFile,
    members: list[str],
    ledger: list[dict[str, str]],
) -> tuple[dict[str, str], str]:
    labels = [source_label(row) for row in ledger]
    if any(not label for label in labels):
        raise ValueError("LEGACY_STAGE1_LEDGER_MISSING_SOURCE_OPPONENT_LABEL")

    expected_counts = Counter(labels)
    wanted = set(labels)
    qualifying: list[tuple[int, str, dict[str, str]]] = []
    for member in members:
        try:
            header = csv_header(archive, member)
        except (UnicodeDecodeError, csv.Error):
            continue
        score = mapping_header_score(header, member)
        if score < 0:
            continue
        if any(field in header for field in COUNT_FIELDS):
            score += 1
        data = csv_bytes(archive.read(member))
        mapping: dict[str, str] = {}
        seen_rows: set[str] = set()
        invalid = False
        for row in data:
            label = source_label(row)
            key = pick(row, *MAPPING_KEY_FIELDS)
            if not label or not key:
                continue
            if label in seen_rows:
                invalid = True
                break
            seen_rows.add(label)
            count_text = pick(row, *COUNT_FIELDS)
            if label in wanted and count_text:
                try:
                    count_value = int(float(count_text))
                except ValueError:
                    invalid = True
                    break
                if count_value != expected_counts[label]:
                    invalid = True
                    break
            mapping[label] = key
        if invalid:
            continue
        if wanted.issubset(mapping):
            qualifying.append((score, member, mapping))

    if not qualifying:
        raise ValueError(
            "NO_COMPLETE_LEGACY_STAGE2_OPPONENT_MAPPING: "
            f"required_labels={len(wanted)}"
        )

    best_score = max(score for score, _, _ in qualifying)
    best = [(member, mapping) for score, member, mapping in qualifying if score == best_score]
    if len(best) == 1:
        return best[0][1], best[0][0]

    fingerprints = {
        tuple(sorted((label, mapping[label]) for label in wanted))
        for _, mapping in best
    }
    if len(fingerprints) != 1:
        raise ValueError(
            "AMBIGUOUS_COMPLETE_LEGACY_STAGE2_OPPONENT_MAPPING: "
            + ",".join(sorted(member for member, _ in best))
        )
    member, mapping = sorted(best, key=lambda item: item[0])[0]
    return mapping, member


def materialize_legacy_checkpoint(
    archive: zipfile.ZipFile,
    members: list[str],
    out: Path,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    candidates: list[tuple[int, str]] = []
    for member in members:
        try:
            score = legacy_game_ledger_score(csv_header(archive, member), member)
        except (UnicodeDecodeError, csv.Error):
            continue
        if score >= 0:
            candidates.append((score, member))
    if not candidates:
        raise ValueError("NO_STAGE2_LEDGER_FOUND")

    best_score = max(score for score, _ in candidates)
    best_members = sorted(member for score, member in candidates if score == best_score)
    if len(best_members) != 1:
        raise ValueError("AMBIGUOUS_LEGACY_GAME_LEDGER: " + ",".join(best_members))

    ledger_member = best_members[0]
    ledger_bytes = archive.read(ledger_member)
    base_rows = csv_bytes(ledger_bytes)
    mapping, mapping_member = build_complete_label_map(archive, members, base_rows)
    mapping_bytes = archive.read(mapping_member)

    projected: list[dict[str, str]] = []
    for row in base_rows:
        label = source_label(row)
        copy = dict(row)
        copy["opponent_key"] = mapping[label]
        projected.append(copy)
    projected, defaulted_site_count = normalize_site_unknowns(projected)

    projected_path = out / "stage3a0-input-ledger.csv"
    write_csv(projected_path, projected)
    return projected, {
        "entry_mode": "legacy_stage2_materialized",
        "legacy_game_ledger_member": ledger_member,
        "legacy_game_ledger_sha256": sha256_bytes(ledger_bytes),
        "legacy_opponent_mapping_member": mapping_member,
        "legacy_opponent_mapping_sha256": sha256_bytes(mapping_bytes),
        "legacy_opponent_labels_required": len(set(source_label(row) for row in base_rows)),
        "legacy_opponent_mapping_coverage": "COMPLETE",
        "site_type_defaulted_to_unknown_count": defaulted_site_count,
        "input_ledger": str(projected_path),
        "input_ledger_sha256": sha256(projected_path),
    }


def load_input(path: Path, out: Path) -> tuple[list[dict[str, str]], dict[str, object]]:
    if path.suffix.lower() != ".zip":
        raw = rows(path)
        normalized, defaulted_site_count = normalize_site_unknowns(raw)
        projected_path = out / "stage3a0-input-ledger.csv"
        write_csv(projected_path, normalized)
        digest = sha256(path)
        return normalized, {
            "entry_mode": "ledger_csv",
            "input_artifact": str(path),
            "input_artifact_sha256": digest,
            "source_ledger_sha256": digest,
            "site_type_defaulted_to_unknown_count": defaulted_site_count,
            "input_ledger": str(projected_path),
            "input_ledger_sha256": sha256(projected_path),
        }

    checkpoint_sha = sha256(path)
    try:
        archive = zipfile.ZipFile(path)
    except zipfile.BadZipFile as exc:
        raise ValueError(f"INVALID_CHECKPOINT_ZIP: {exc}") from exc

    with archive:
        members = [
            name
            for name in archive.namelist()
            if not name.endswith("/") and name.lower().endswith(".csv")
        ]
        exact: list[str] = []
        for basename in LEDGER_BASENAMES:
            hits = [name for name in members if Path(name).name.lower() == basename]
            valid_hits = []
            for name in hits:
                try:
                    if ledger_header_score(csv_header(archive, name), name) >= 0:
                        valid_hits.append(name)
                except (UnicodeDecodeError, csv.Error):
                    continue
            if valid_hits:
                exact = valid_hits
                break
        if len(exact) > 1:
            raise ValueError("AMBIGUOUS_STAGE2_LEDGER: " + ",".join(sorted(exact)))

        selected = exact[0] if exact else None
        if selected is None:
            scored: list[tuple[int, str]] = []
            for name in members:
                try:
                    score = ledger_header_score(csv_header(archive, name), name)
                except (UnicodeDecodeError, csv.Error):
                    continue
                if score >= 0:
                    scored.append((score, name))
            if scored:
                best = max(score for score, _ in scored)
                best_members = sorted(name for score, name in scored if score == best)
                if len(best_members) == 1:
                    selected = best_members[0]
                else:
                    raise ValueError(
                        "AMBIGUOUS_STAGE2_LEDGER: " + ",".join(best_members)
                    )

        if selected is not None:
            source_data = archive.read(selected)
            raw = csv_bytes(source_data)
            normalized, defaulted_site_count = normalize_site_unknowns(raw)
            projected_path = out / "stage3a0-input-ledger.csv"
            write_csv(projected_path, normalized)
            return normalized, {
                "entry_mode": "checkpoint_zip",
                "input_artifact": str(path),
                "input_artifact_sha256": checkpoint_sha,
                "input_checkpoint_member": selected,
                "source_ledger_sha256": sha256_bytes(source_data),
                "site_type_defaulted_to_unknown_count": defaulted_site_count,
                "input_ledger": str(projected_path),
                "input_ledger_sha256": sha256(projected_path),
            }

        legacy_rows, legacy_meta = materialize_legacy_checkpoint(archive, members, out)
        return legacy_rows, {
            "input_artifact": str(path),
            "input_artifact_sha256": checkpoint_sha,
            **legacy_meta,
        }


def readiness(ledger: list[dict[str, str]]) -> dict[str, object]:
    ids = [rid(row) for row in ledger]
    counts = Counter(value for value in ids if value)
    defects = {
        "missing_stable_row_id": [index + 1 for index, value in enumerate(ids) if not value],
        "duplicate_row_ids": sorted(key for key, value in counts.items() if value > 1),
        "missing_game_type": [
            rid(row) or f"ROW-{index + 1}"
            for index, row in enumerate(ledger)
            if not pick(row, *GAME_TYPE_FIELDS)
        ],
        "unrecognized_game_type": [
            rid(row) or f"ROW-{index + 1}"
            for index, row in enumerate(ledger)
            if pick(row, *GAME_TYPE_FIELDS)
            and game_class(pick(row, *GAME_TYPE_FIELDS)) == "UNCLASSIFIED"
        ],
        "unrecognized_site_type": [
            rid(row) or f"ROW-{index + 1}"
            for index, row in enumerate(ledger)
            if site_class(pick(row, *SITE_FIELDS)) == "INVALID"
        ],
        "missing_opponent_key": [
            rid(row) or f"ROW-{index + 1}"
            for index, row in enumerate(ledger)
            if not pick(row, *OPP_FIELDS)
        ],
    }
    blocking = {key: value for key, value in defects.items() if value}
    return {
        "ready": not blocking,
        "blocking_defects": blocking,
        "date_blank_count": sum(
            not bool(pick(row, "game_date", "date")) for row in ledger
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Checkpoint-only Stage 3A-0 census/partition gate. INPUT may be the "
            "Stage 2 checkpoint ZIP or structured Stage 2 ledger CSV."
        )
    )
    parser.add_argument("school_key")
    parser.add_argument("input", type=Path)
    parser.add_argument("--canonical", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--main-sha")
    args = parser.parse_args()

    out = args.output_dir or Path(".research") / args.school_key / "stage3a0"
    out.mkdir(parents=True, exist_ok=True)
    pinned = args.main_sha or git_sha()

    try:
        ledger, input_meta = load_input(args.input, out)
    except (OSError, ValueError) as exc:
        status = {
            "schema_version": 5,
            "school_key": args.school_key,
            "status": "STAGE_3A0_ENTRY_NOT_READY",
            "protected_main_sha": pinned,
            "repository_state_required": False,
            "input_artifact": str(args.input),
            "entry_error": str(exc),
            "external_historical_research_used": False,
            "next_action": "STOP_AND_FIX_STAGE2_INPUT_ARTIFACT",
            "remediation": (
                "Provide a complete structured Stage 2 game ledger, or a legacy Stage 2 "
                "checkpoint that contains both a full game-level ledger and a complete "
                "label-level opponent mapping. Do not reconstruct from prose or begin "
                "historical/source research inside Stage 3A-0."
            ),
        }
        if args.input.exists():
            status["input_artifact_sha256"] = sha256(args.input)
        dump(out, "stage3a0-status.json", status)
        print(json.dumps(status, indent=2))
        return 2

    preflight = readiness(ledger)
    blocking_keys = set(preflight["blocking_defects"])
    missing_game_type_only = blocking_keys == {"missing_game_type"}
    status = {
        "schema_version": 5,
        "school_key": args.school_key,
        "status": "INPUT_READY" if preflight["ready"] else "STAGE_3A0_INPUT_NOT_READY",
        **input_meta,
        "protected_main_sha": pinned,
        "repository_state_required": False,
        "project_evidence_reuse_deferred": True,
        "readiness": preflight,
        "external_historical_research_used": False,
    }

    if not preflight["ready"]:
        status["remediation_code"] = (
            "MISSING_GAME_TYPE_ONLY"
            if missing_game_type_only
            else "STRUCTURED_INPUT_DEFECTS"
        )
        status["next_action"] = (
            "STOP_STAGE_3A0_AND_RUN_NARROW_GAME_TYPE_MIGRATION"
            if missing_game_type_only
            else "STOP_AND_REPAIR_STRUCTURED_INPUT_AT_PRIOR_STAGE"
        )
        status["remediation"] = (
            "For a pre-hardening accepted checkpoint only: exit Stage 3A-0, "
            "perform one narrow compatibility repair from accepted source/state, "
            "validate it with research_stage3a0_migrate.py, then rerun. Do not "
            "improvise discovery inside Stage 3A-0."
            if missing_game_type_only
            else "Stop Stage 3A-0. Repair only the serialized structured-input "
            "defects at the controlling prior stage/checkpoint; do not research "
            "around the readiness gate."
        )
        dump(out, "stage3a0-status.json", status)
        print(json.dumps(status, indent=2))
        return 2

    counts: Counter[str] = Counter()
    eras: Counter[str] = Counter()
    queues: dict[str, list[dict[str, str]]] = {
        "HOME": [],
        "OPPONENT_HOME": [],
        "NEUTRAL": [],
        "UNKNOWN": [],
        "POSTSEASON": [],
        "NEUTRAL_MODERN": [],
        "NEUTRAL_HISTORICAL": [],
    }

    for row in ledger:
        competition = game_class(pick(row, *GAME_TYPE_FIELDS))
        site = site_class(pick(row, *SITE_FIELDS))
        counts[competition] += 1

        if competition == "POSTSEASON":
            queues["POSTSEASON"].append(row)
            continue
        if competition != "REGULAR_SEASON":
            continue

        counts["RS_" + site] += 1
        queues[site].append(row)

        if site == "NEUTRAL":
            try:
                start_year = int(pick(row, *SEASON_FIELDS)[:4])
            except Exception:
                start_year = None
            era = (
                "MODERN_1996_97_PLUS"
                if start_year is not None and start_year >= 1996
                else "HISTORICAL_1995_96_OR_EARLIER"
            )
            eras[era] += 1
            queue_name = (
                "NEUTRAL_MODERN"
                if era == "MODERN_1996_97_PLUS"
                else "NEUTRAL_HISTORICAL"
            )
            queues[queue_name].append(row)

    summary = {
        **status,
        "status": "COMPLETE",
        "ledger_rows": len(ledger),
        "partition": {
            "regular_season": counts["REGULAR_SEASON"],
            "postseason": counts["POSTSEASON"],
            "unclassified": 0,
        },
        "regular_season_site_census": {
            key: counts["RS_" + key]
            for key in ("HOME", "OPPONENT_HOME", "NEUTRAL", "UNKNOWN")
        },
        "neutral_era_census": dict(eras),
        "project_evidence_reuse": {
            "performed_in_stage3a0": False,
            "reason": "Stage 3A-0 is checkpoint-only census/partition.",
            "deferred_to": ["STAGE_3A1", "STAGE_3A2", "STAGE_3A3_TIER1"],
        },
        "next_action": "STOP_AT_STAGE_3A0_BOUNDARY",
        "next_bounded_assignment": "Stage 3A-1 — H/A/N completion",
    }

    artifacts = {
        "input_ledger": Path(str(summary["input_ledger"])),
        "summary": dump(out, "stage3a0-summary.json", summary),
        "status": dump(out, "stage3a0-status.json", summary),
        "home_queue": dump(out, "stage3a2-home-queue.json", queues["HOME"]),
        "opponent_home_queue": dump(
            out, "stage3a0-opponent-home-queue.json", queues["OPPONENT_HOME"]
        ),
        "unknown_queue": dump(
            out, "stage3a1-unknown-han-queue.json", queues["UNKNOWN"]
        ),
        "neutral_queue": dump(
            out, "stage3a3-neutral-queue.json", queues["NEUTRAL"]
        ),
        "neutral_modern_queue": dump(
            out, "stage3a3-modern-neutral-queue.json", queues["NEUTRAL_MODERN"]
        ),
        "neutral_historical_queue": dump(
            out,
            "stage3a3-historical-neutral-queue.json",
            queues["NEUTRAL_HISTORICAL"],
        ),
        "postseason_queue": dump(
            out, "stage3b-postseason-handoff.json", queues["POSTSEASON"]
        ),
    }
    dump(
        out,
        "manifest.json",
        {
            key: {"path": str(path), "sha256": sha256(path)}
            for key, path in artifacts.items()
        },
    )
    print(json.dumps(summary, indent=2))
    print("STAGE 3A-0: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
