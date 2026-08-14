"""Pinned blind corpus loader; target schemas remain external JSON data."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import pathlib
import random
import re
import stat
from typing import Mapping, Sequence

BLIND_ID = re.compile(r"[0-9a-f]{16}\Z")


class CorpusError(RuntimeError):
    """The sealed corpus is malformed, unpinned, or incomplete."""


@dataclasses.dataclass(frozen=True)
class Case:
    case_id: str
    schema_path: str
    document: object
    expected_valid: bool
    semantic_group: str
    kind: str


def _read_regular(path: pathlib.Path) -> bytes:
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(before.st_mode) or before.st_nlink != 1:
        raise CorpusError("corpus must be a single-link regular non-symlink file")
    if before.st_mode & 0o222:
        raise CorpusError("corpus must be sealed read-only")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(fd, "rb") as handle:
        opened = os.fstat(handle.fileno())
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise CorpusError("corpus changed identity while opening")
        return handle.read()


def load(
    path: pathlib.Path | str,
    expected_sha256: str,
    schema_paths: Sequence[str],
) -> tuple[list[Case], dict[str, dict[str, str]], int, str]:
    raw = _read_regular(pathlib.Path(path))
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise CorpusError("corpus SHA-256 does not match the authority bundle")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise CorpusError("corpus is not strict UTF-8 JSON: %s" % exc) from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise CorpusError("corpus must be a schema_version 1 object")
    seed = value.get("reorder_seed")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise CorpusError("reorder_seed must be an integer")
    raw_cases = value.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise CorpusError("corpus cases must be a non-empty list")
    allowed = set(schema_paths)
    cases: list[Case] = []
    seen = set()
    per_schema: dict[str, dict[str, int]] = {
        name: {"valid": 0, "invalid": 0, "semantic": 0} for name in schema_paths
    }
    groups: dict[tuple[str, str], int] = {}
    for raw_case in raw_cases:
        if not isinstance(raw_case, Mapping):
            raise CorpusError("corpus case is not an object")
        case_id = raw_case.get("case_id")
        schema_path = raw_case.get("schema_path")
        expected = raw_case.get("expected_valid")
        semantic = raw_case.get("semantic_group")
        kind = raw_case.get("kind")
        if not isinstance(case_id, str) or not BLIND_ID.fullmatch(case_id) or case_id in seen:
            raise CorpusError("case_id must be unique blind lowercase 16-hex")
        if schema_path not in allowed:
            raise CorpusError("case names an unexpected schema path: %r" % schema_path)
        if type(expected) is not bool:
            raise CorpusError("case expected_valid must be boolean")
        if not isinstance(semantic, str) or not semantic:
            raise CorpusError("case semantic_group must be non-empty")
        if kind not in ("valid", "invalid", "semantic_equivalent"):
            raise CorpusError("case kind must be valid, invalid, or semantic_equivalent")
        if (kind == "invalid") == expected:
            raise CorpusError("case kind disagrees with expected_valid")
        seen.add(case_id)
        per_schema[schema_path]["valid" if expected else "invalid"] += 1
        if kind == "semantic_equivalent":
            per_schema[schema_path]["semantic"] += 1
        groups[(schema_path, semantic)] = groups.get((schema_path, semantic), 0) + 1
        cases.append(
            Case(case_id, schema_path, raw_case.get("document"), expected, semantic, kind)
        )
    incomplete = {
        path: counts
        for path, counts in per_schema.items()
        if counts["valid"] < 1 or counts["invalid"] < 1 or counts["semantic"] < 2
    }
    if incomplete:
        raise CorpusError("every schema needs valid, invalid, and two semantic-equivalent cases: %s" % incomplete)
    if any(
        count < 2
        for (path, group), count in groups.items()
        if any(case.schema_path == path and case.semantic_group == group and case.kind == "semantic_equivalent" for case in cases)
    ):
        raise CorpusError("semantic-equivalent groups require at least two cases")

    anchors = value.get("keyword_anchors")
    if not isinstance(anchors, dict):
        raise CorpusError("keyword_anchors must be an object")
    normalized: dict[str, dict[str, str]] = {}
    for keyword, record in anchors.items():
        if not isinstance(keyword, str) or not isinstance(record, dict):
            raise CorpusError("malformed keyword anchor")
        valid_id = record.get("valid_case_id")
        invalid_id = record.get("invalid_case_id")
        if valid_id not in seen or invalid_id not in seen:
            raise CorpusError("keyword anchor refers to an unknown case: %s" % keyword)
        normalized[keyword] = {"valid_case_id": valid_id, "invalid_case_id": invalid_id}
    random.Random(seed).shuffle(cases)
    return cases, normalized, seed, digest
