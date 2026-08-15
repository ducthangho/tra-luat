"""Bộ ca GIỮ LẠI do Dispatcher niêm phong, nằm ngoài nguồn của ứng viên.

Vì sao tệp này tồn tại (WP99-R3G3-SPEC-002): toàn bộ 34 tài liệu VÀ 34 nhãn từng
nằm chung trong `oracle/corpus.json` do ứng viên soạn.  Reviewer đã dựng đúng
bảng tra digest-tài-liệu → nhãn từ corpus công khai đó: 34 ca, 34 digest phân
biệt, không mâu thuẫn nhãn nào, dự đoán khớp 34/34.  Nghĩa là một "validator"
chẳng kiểm schema gì cả, chỉ thuộc lòng bảng tra, vẫn qua sạch mọi ca — §8.4 đòi
`held-out inputs` chính là để giết đúng kiểu gian lận này.

Vì vậy bộ ca giữ lại phải:

1. nằm NGOÀI checkout ứng viên và được niêm phong read-only;
2. được pin Dispatcher khai báo trước bằng đường dẫn, SHA-256 và SỐ CA — mẫu số
   chốt trước, đúng doctrine R6, không phải "số ca vòng lặp tình cờ đọc được";
3. RỜI NHAU thật sự với corpus công khai, đo bằng cả case_id lẫn digest tài liệu
   chính tắc — trùng một digest là một ca đã bị lộ, và "giữ lại" mất nghĩa;
4. mang CẢ HAI nhãn.  Bộ nhớ-thuộc-lòng khi gặp tài liệu lạ buộc phải đoán, mà
   một phép đoán chỉ trả được một nhãn; có đủ hai nhãn thì nó chắc chắn sai ít
   nhất một ca, nên phép giết KHÔNG phụ thuộc vào may rủi.

Nhãn của bộ giữ lại KHÔNG bao giờ rời khỏi tiến trình chấm: `fake_validators`
chỉ nhận `case_id` và `document`.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import pathlib
import re
import sys
from typing import Mapping, Sequence

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from oracle import corpus, safe_io  # noqa: E402

SHA256 = re.compile(r"[0-9a-f]{64}\Z")

DECLARATION_KEYS = ("path", "sha256", "case_count")
TOP_LEVEL_KEYS = (
    "schema_version",
    "produced_by",
    "source",
    "target_schema_inventory_sha256",
    "reorder_seed",
    "cases",
)


class HeldOutError(RuntimeError):
    """Bộ ca giữ lại bị thiếu, không niêm phong, sai pin, hoặc không thật sự giữ lại."""


@dataclasses.dataclass(frozen=True)
class HeldOut:
    path: str
    sha256: str
    produced_by: str
    source: Mapping[str, object]
    reorder_seed: int
    cases: list[corpus.Case]
    case_ids: tuple[str, ...]
    label_counts: Mapping[str, int]
    raw: bytes


def _fail(message: str) -> HeldOutError:
    return HeldOutError(message)


def declaration(pin: Mapping[str, object]) -> dict[str, object]:
    """Khối `heldout` bắt buộc trong pin niêm phong của Dispatcher.

    Thiếu khối này là ĐỎ, không phải "chạy chế độ rút gọn": không có đầu vào giữ
    lại thì bộ nhớ-thuộc-lòng sống sót, và §8.4 không được thoả.
    """
    if not isinstance(pin, Mapping):
        raise _fail("Dispatcher pin must be an object")
    block = pin.get("heldout")
    if block is None:
        raise _fail(
            "Dispatcher pin declares no held-out input source; §8.4 requires a sealed "
            "heldout block naming path, sha256 and case_count outside the candidate checkout"
        )
    if not isinstance(block, Mapping) or set(block) != set(DECLARATION_KEYS):
        raise _fail("Dispatcher pin heldout block must contain exactly %s" % list(DECLARATION_KEYS))
    path = block["path"]
    if not isinstance(path, str) or not path:
        raise _fail("Dispatcher pin heldout.path must be a non-empty path")
    digest = block["sha256"]
    if not isinstance(digest, str) or not SHA256.fullmatch(digest):
        raise _fail("Dispatcher pin heldout.sha256 must be an exact lowercase SHA-256")
    count = block["case_count"]
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise _fail("Dispatcher pin heldout.case_count must be a positive integer")
    return {"path": path, "sha256": digest, "case_count": count}


def load(
    declared: Mapping[str, object],
    candidate_root: str | pathlib.Path,
    schema_paths: Sequence[str],
    target_schema_inventory_sha256: str,
    public_case_ids: Sequence[str],
    public_document_digests: Sequence[str],
) -> HeldOut:
    path = pathlib.Path(str(declared["path"]))
    safe_io.require_outside_tree(path, candidate_root, "held-out corpus", HeldOutError)
    raw = safe_io.read_regular_single_link(
        path, "held-out corpus", HeldOutError, require_readonly=True
    )
    digest = hashlib.sha256(raw).hexdigest()
    if digest != declared["sha256"]:
        raise _fail(
            "held-out corpus SHA-256 does not match the Dispatcher pin: pinned=%s measured=%s"
            % (declared["sha256"], digest)
        )
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise _fail("held-out corpus is not strict UTF-8 JSON: %s" % exc) from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise _fail("held-out corpus must be a schema_version 1 object")
    missing = [name for name in TOP_LEVEL_KEYS if name not in value]
    extra = sorted(set(value) - set(TOP_LEVEL_KEYS), key=str)
    if missing or extra:
        raise _fail(
            "held-out corpus must name exactly %s: missing=%s unexpected=%s"
            % (list(TOP_LEVEL_KEYS), missing, extra)
        )
    produced_by = value.get("produced_by")
    if not isinstance(produced_by, str) or not produced_by:
        raise _fail("held-out corpus must record a non-empty produced_by")
    source = value.get("source")
    if not isinstance(source, Mapping) or not source:
        raise _fail("held-out corpus must record how it was produced")
    binding = value.get("target_schema_inventory_sha256")
    if not isinstance(binding, str) or not SHA256.fullmatch(binding):
        raise _fail("held-out corpus must declare target_schema_inventory_sha256 as a lowercase SHA-256")
    if binding != target_schema_inventory_sha256:
        raise _fail(
            "held-out corpus was authored for a different target schema inventory: heldout=%s measured=%s"
            % (binding, target_schema_inventory_sha256)
        )
    seed = value.get("reorder_seed")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise _fail("held-out reorder_seed must be an integer")
    raw_cases = value.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise _fail("held-out cases must be a non-empty list")

    allowed = set(schema_paths)
    public_ids = set(public_case_ids)
    public_digests = set(public_document_digests)
    seen: set[str] = set()
    cases: list[corpus.Case] = []
    collisions: list[str] = []
    for raw_case in raw_cases:
        case = corpus.parse_case(raw_case, allowed, seen, HeldOutError)
        if case.case_id in public_ids:
            raise _fail("held-out case_id also appears in the public corpus: %s" % case.case_id)
        if corpus.document_digest(case.document) in public_digests:
            collisions.append(case.case_id)
        seen.add(case.case_id)
        cases.append(case)
    if collisions:
        # Đây mới là phép đo "giữ lại" thật sự.  ID khác nhau mà BYTE tài liệu đã
        # nằm trong corpus công khai thì bộ nhớ-thuộc-lòng vẫn trả đúng nhãn.
        raise _fail(
            "held-out documents are already published in the public corpus: %s" % sorted(collisions)
        )
    if len(cases) != declared["case_count"]:
        raise _fail(
            "held-out case count disagrees with the Dispatcher pin: pinned=%r measured=%d"
            % (declared["case_count"], len(cases))
        )
    label_counts = {
        "valid": sum(1 for case in cases if case.expected_valid),
        "invalid": sum(1 for case in cases if not case.expected_valid),
    }
    if label_counts["valid"] < 1 or label_counts["invalid"] < 1:
        raise _fail(
            "held-out cases must carry both labels so a single-guess memorizer cannot survive: %s"
            % label_counts
        )
    return HeldOut(
        path=str(path.resolve()),
        sha256=digest,
        produced_by=produced_by,
        source=json.loads(json.dumps(source, sort_keys=True)),
        reorder_seed=seed,
        cases=cases,
        case_ids=tuple(sorted(case.case_id for case in cases)),
        label_counts=label_counts,
        raw=raw,
    )
