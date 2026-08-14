"""Pinned blind corpus loader; target schemas remain external JSON data.

Corpus KHÔNG còn là tệp riêng trên máy Executor.  Nó nằm trong cây tin cậy tại
`oracle/corpus.json`, nên digest kiểm kê trusted-source đã phủ nó và bất kỳ ai
đứng ở commit đã ghim đều dựng lại được từng byte — đó là điều R1 của verdict
5297249899 đòi.  Corpus còn tự khai `target_schema_inventory_sha256`: nó chỉ hợp
lệ với ĐÚNG bộ năm schema mà nó được soạn cho, và oracle bắt phải khớp.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import pathlib
import random
import re
import sys
from typing import Mapping, Sequence

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from oracle import safe_io  # noqa: E402

BLIND_ID = re.compile(r"[0-9a-f]{16}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


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


@dataclasses.dataclass(frozen=True)
class Corpus:
    cases: list[Case]
    anchors: dict[str, dict[str, str]]
    reorder_seed: int
    sha256: str
    target_schema_inventory_sha256: str
    case_id_registry: tuple[str, ...]


def read_bytes(path: pathlib.Path | str, *, require_readonly: bool) -> bytes:
    """Đọc corpus.

    `require_readonly` chỉ bật cho bản sao NGOÀI do Dispatcher đặt.  Bản trong cây
    tin cậy là tệp Git mode 100644 (ghi được) — tính toàn vẹn của nó đến từ digest
    kiểm kê trusted-source, mạnh hơn bit quyền trên đĩa.
    """
    return safe_io.read_regular_single_link(
        path, "corpus", CorpusError, require_readonly=require_readonly
    )


def load(
    path: pathlib.Path | str,
    expected_sha256: str,
    schema_paths: Sequence[str],
    *,
    require_readonly: bool = False,
) -> Corpus:
    raw = read_bytes(path, require_readonly=require_readonly)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise CorpusError("corpus SHA-256 does not match the authority bundle")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise CorpusError("corpus is not strict UTF-8 JSON: %s" % exc) from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise CorpusError("corpus must be a schema_version 1 object")
    binding = value.get("target_schema_inventory_sha256")
    if not isinstance(binding, str) or not SHA256.fullmatch(binding):
        raise CorpusError("corpus must declare target_schema_inventory_sha256 as a lowercase SHA-256")
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
        path_name: counts
        for path_name, counts in per_schema.items()
        if counts["valid"] < 1 or counts["invalid"] < 1 or counts["semantic"] < 2
    }
    if incomplete:
        raise CorpusError("every schema needs valid, invalid, and two semantic-equivalent cases: %s" % incomplete)
    if any(
        count < 2
        for (path_name, group), count in groups.items()
        if any(
            case.schema_path == path_name
            and case.semantic_group == group
            and case.kind == "semantic_equivalent"
            for case in cases
        )
    ):
        raise CorpusError("semantic-equivalent groups require at least two cases")

    anchors = value.get("keyword_anchors")
    if not isinstance(anchors, dict) or not anchors:
        raise CorpusError("keyword_anchors must be a non-empty object")
    normalized: dict[str, dict[str, str]] = {}
    for keyword, record in anchors.items():
        if not isinstance(keyword, str) or not isinstance(record, dict):
            raise CorpusError("malformed keyword anchor")
        if set(record) != {"valid_case_id", "invalid_case_id"}:
            raise CorpusError("keyword anchor must name exactly valid_case_id and invalid_case_id: %s" % keyword)
        valid_id = record.get("valid_case_id")
        invalid_id = record.get("invalid_case_id")
        if valid_id not in seen or invalid_id not in seen:
            raise CorpusError("keyword anchor refers to an unknown case: %s" % keyword)
        normalized[keyword] = {"valid_case_id": valid_id, "invalid_case_id": invalid_id}

    # Sổ đăng ký ID được chốt TRƯỚC khi xáo và trước khi chạy ca nào: mẫu số của
    # oracle là kích thước sổ này, không phải "số ca vòng lặp đã sinh ra" (R6).
    registry = tuple(sorted(case.case_id for case in cases))
    random.Random(seed).shuffle(cases)
    return Corpus(
        cases=cases,
        anchors=normalized,
        reorder_seed=seed,
        sha256=digest,
        target_schema_inventory_sha256=binding,
        case_id_registry=registry,
    )
