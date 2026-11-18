#!/usr/bin/env python3
"""Shared read/write contract for global source-game assertion storage.

The historical repository used one monolithic
data/evidence/game-assertions.csv file. GitHub rejects any newly-created blob
larger than 100 MiB, so the legacy file may remain immutable once it approaches
that boundary while new assertions spill into numbered CSV shards in the same
directory.

Readers consume the legacy file followed by every numbered shard. Writers
preserve legacy behavior while the resulting legacy blob is comfortably below
GitHub's limit; otherwise they append only to numbered shards. Existing rows
are never repartitioned by this module.
"""
from __future__ import annotations

import csv
import hashlib
import io
import re
import subprocess
from pathlib import Path
from typing import Callable

LEGACY_RELATIVE_PATH = "data/evidence/game-assertions.csv"
SHARD_RE = re.compile(r"^game-assertions-(?P<number>[0-9]{4})\.csv$")
LEGACY_APPEND_LIMIT_BYTES = 99 * 1024 * 1024
SHARD_TARGET_BYTES = 90 * 1024 * 1024


def assertion_paths(repo_root: Path) -> list[Path]:
    root = Path(repo_root).resolve()
    legacy = root / LEGACY_RELATIVE_PATH
    if not legacy.is_file():
        raise FileNotFoundError(legacy)
    directory = legacy.parent
    shards = sorted(
        (
            path
            for path in directory.glob("game-assertions-*.csv")
            if SHARD_RE.fullmatch(path.name)
        ),
        key=lambda path: int(SHARD_RE.fullmatch(path.name).group("number")),
    )
    return [legacy, *shards]


def _read_csv_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _validated_union(
    tables: list[tuple[Path, list[str], list[dict[str, str]]]]
) -> tuple[list[str], list[dict[str, str]]]:
    fields: list[str] | None = None
    rows: list[dict[str, str]] = []
    assertion_ids: dict[str, Path] = {}
    for path, current_fields, current_rows in tables:
        if fields is None:
            fields = current_fields
        elif current_fields != fields:
            raise ValueError(
                f"assertion shard schema mismatch: {path} has {current_fields!r}; "
                f"expected {fields!r}"
            )
        for row in current_rows:
            assertion_id = row.get("assertion_id", "").strip()
            if assertion_id:
                prior = assertion_ids.get(assertion_id)
                if prior is not None:
                    raise ValueError(
                        f"duplicate assertion_id across assertion files: "
                        f"{assertion_id} ({prior}, {path})"
                    )
                assertion_ids[assertion_id] = path
            rows.append(row)
    return fields or [], rows


def read_game_assertions(
    repo_root: Path,
) -> tuple[list[str], list[dict[str, str]]]:
    tables = [
        (path, *_read_csv_table(path))
        for path in assertion_paths(repo_root)
    ]
    return _validated_union(tables)


def _serialize_preserving_format(
    path: Path,
    fields: list[str],
    rows: list[dict[str, str]],
) -> bytes:
    original = path.read_bytes()
    has_bom = original.startswith(b"\xef\xbb\xbf")
    line_ending = "\r\n" if b"\r\n" in original else "\n"
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=fields,
        lineterminator=line_ending,
    )
    writer.writeheader()
    writer.writerows(
        {field: row.get(field, "") for field in fields}
        for row in rows
    )
    raw = stream.getvalue().encode("utf-8")
    return (b"\xef\xbb\xbf" + raw) if has_bom else raw


def rewrite_game_assertions(
    repo_root: Path,
    fields: list[str],
    rows: list[dict[str, str]],
) -> list[Path]:
    """Rewrite existing assertion rows without changing shard membership.

    This operation is for reconciliation/maintenance of already-present rows.
    It rejects schema, population, or ordering changes; append_game_assertions()
    remains the only path for adding new assertion rows.
    """
    root = Path(repo_root).resolve()
    tables = [
        (path, *_read_csv_table(path))
        for path in assertion_paths(root)
    ]
    existing_fields, existing_rows = _validated_union(tables)
    if existing_fields != list(fields):
        raise ValueError(
            "assertion schema mismatch between rewriter and existing assertion store"
        )

    replacement_rows = list(rows)
    existing_ids = [
        row.get("assertion_id", "").strip()
        for row in existing_rows
    ]
    replacement_ids = [
        row.get("assertion_id", "").strip()
        for row in replacement_rows
    ]
    if (
        not all(existing_ids)
        or replacement_ids != existing_ids
    ):
        raise ValueError(
            "assertion rewrite must preserve exact nonblank assertion_id population "
            "and order"
        )

    changed: list[Path] = []
    offset = 0
    for path, current_fields, current_rows in tables:
        count = len(current_rows)
        replacement = replacement_rows[offset:offset + count]
        offset += count
        if replacement == current_rows:
            continue
        raw = _serialize_preserving_format(path, current_fields, replacement)
        _atomic_write(path, raw)
        changed.append(path)
    if offset != len(replacement_rows):
        raise ValueError("assertion rewrite row population changed during partitioning")
    return changed


def assertion_store_fingerprint(repo_root: Path) -> str:
    root = Path(repo_root).resolve()
    digest = hashlib.sha256()
    for path in assertion_paths(root):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
        digest.update(b"\n")
    return digest.hexdigest()


def _serialize(
    fields: list[str],
    rows: list[dict[str, str]],
) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=fields,
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def _atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_bytes(raw)
    temp.replace(path)


def _next_shard_path(repo_root: Path) -> Path:
    paths = assertion_paths(repo_root)
    numbers = [
        int(match.group("number"))
        for path in paths[1:]
        if (match := SHARD_RE.fullmatch(path.name))
    ]
    next_number = (max(numbers) + 1) if numbers else 2
    return paths[0].parent / f"game-assertions-{next_number:04d}.csv"


def append_game_assertions(
    repo_root: Path,
    fields: list[str],
    new_rows: list[dict[str, str]],
    *,
    legacy_append_limit_bytes: int = LEGACY_APPEND_LIMIT_BYTES,
    shard_target_bytes: int = SHARD_TARGET_BYTES,
) -> list[Path]:
    """Append rows without requiring an over-limit Git blob."""
    if not new_rows:
        return []

    root = Path(repo_root).resolve()
    existing_fields, _ = read_game_assertions(root)
    if existing_fields != list(fields):
        raise ValueError(
            "assertion schema mismatch between writer and existing assertion store"
        )

    paths = assertion_paths(root)
    legacy = paths[0]
    legacy_fields, legacy_rows = _read_csv_table(legacy)

    if len(paths) == 1:
        candidate = _serialize(legacy_fields, legacy_rows + list(new_rows))
        if len(candidate) <= legacy_append_limit_bytes:
            _atomic_write(legacy, candidate)
            return [legacy]

    target = paths[-1] if len(paths) > 1 else _next_shard_path(root)
    if target.is_file():
        shard_fields, shard_rows = _read_csv_table(target)
        if shard_fields != list(fields):
            raise ValueError(f"assertion shard schema mismatch: {target}")
        candidate_rows = shard_rows + list(new_rows)
    else:
        candidate_rows = list(new_rows)

    candidate = _serialize(list(fields), candidate_rows)
    if len(candidate) > shard_target_bytes:
        target = _next_shard_path(root)
        candidate = _serialize(list(fields), list(new_rows))
        if len(candidate) > shard_target_bytes:
            raise ValueError(
                "assertion append batch exceeds one shard target; split the "
                "authorized batch before retrying"
            )

    _atomic_write(target, candidate)
    return [target]


def assertion_relative_paths_at_git(repo: Path, commit: str) -> list[str]:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "ls-tree",
            "-r",
            "--name-only",
            commit,
            "--",
            "data/evidence",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    found: list[tuple[int, str]] = []
    legacy_found = False
    for value in result.stdout.splitlines():
        path = value.strip()
        if path == LEGACY_RELATIVE_PATH:
            legacy_found = True
            continue
        name = Path(path).name
        match = SHARD_RE.fullmatch(name)
        if match and Path(path).parent.as_posix() == "data/evidence":
            found.append((int(match.group("number")), path))
    if not legacy_found:
        raise FileNotFoundError(
            f"{LEGACY_RELATIVE_PATH} is absent at {commit}"
        )
    return [LEGACY_RELATIVE_PATH, *[path for _, path in sorted(found)]]


def read_game_assertions_at_git(
    repo: Path,
    commit: str,
    row_reader: Callable[[Path, str, str], list[dict[str, str]]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    assertion_ids: set[str] = set()
    for path in assertion_relative_paths_at_git(repo, commit):
        for row in row_reader(repo, commit, path):
            assertion_id = row.get("assertion_id", "").strip()
            if assertion_id and assertion_id in assertion_ids:
                raise ValueError(
                    f"duplicate assertion_id across assertion files at {commit}: "
                    f"{assertion_id}"
                )
            if assertion_id:
                assertion_ids.add(assertion_id)
            rows.append(row)
    return rows
