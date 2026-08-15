"""Bó fixture authority NGOÀI cây ứng viên, do Dispatcher soạn từ durable facts.

Vì sao tệp này tồn tại (WP99-R3G3-SPEC-001): bản trước tự dựng `authority_floor`
và ba bộ `durable-facts.json` bằng CHÍNH các hằng Mission 76 / revision 6 /
Packet 99 / revision 3 / generation 3 viết thẳng trong selftest.  Hai vế của phép
so sánh khi đó cùng một nguồn, nên khi durable authority đổi thì ca kiểm vẫn xanh
với hằng đã lỗi thời của chính nó — §4.2 cấm ghim pin trong selftest và §4.3 đòi
pin hiện hành phải đến từ MỘT FIXTURE NGOÀI dựng từ raw durable facts.

Vì vậy module này KHÔNG chứa một giá trị authority nào.  Nó chỉ:

1. đọc bó fixture niêm phong do Dispatcher đặt NGOÀI checkout ứng viên;
2. kiểm hình dạng và tính nhất quán giữa sàn và facts hiện hành;
3. DẪN XUẤT các biến thể stale / fenced / trên-sàn / đúng-sàn từ chính giá trị
   ngoài đó, để ca kiểm nói về NGỮ NGHĨA (đơn điệu, sàn, hàng rào) chứ không nói
   về một con số cụ thể nào.

Fixture nằm ngoài cây ứng viên là điều kiện CÓ THỂ ĐO: một tệp nằm trong checkout
thì Executor sửa được, và khi đó nó lại là hằng của ứng viên đội lốt fixture.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import pathlib
import re
import sys
from typing import Mapping

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from oracle import authority, safe_io  # noqa: E402
from oracle.trusted_inventory import AUTHORITY_FLOOR_KEYS  # noqa: E402

FIXTURE_PATH_ENV = "RA02_AUTHORITY_FIXTURE"

TOP_LEVEL_KEYS = (
    "schema_version",
    "produced_by",
    "source",
    "authority_floor",
    "current_durable_facts",
    "fenced_packet_issues",
)

# Ba khoá đơn điệu: sàn chỉ tiến, không lùi.  Tên khoá sàn và tên trường facts
# tương ứng được ghép ở ĐÂY một lần để ca kiểm khỏi tự ghép lại.
MONOTONIC_FIELDS = (
    ("mission", "revision", "mission_revision_min"),
    ("packet", "revision", "packet_revision_min"),
    ("packet", "generation", "packet_generation_min"),
)

SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class AuthorityFixtureError(RuntimeError):
    """Fixture authority ngoài bị thiếu, sai chỗ, không niêm phong, hoặc mâu thuẫn."""


@dataclasses.dataclass(frozen=True)
class AuthorityFixture:
    path: str
    sha256: str
    produced_by: str
    source: Mapping[str, object]
    floor: Mapping[str, int]
    current: Mapping[str, object]
    fenced_packet_issues: tuple[int, ...]

    # --- Các biến thể DẪN XUẤT; không biến thể nào chứa hằng authority ---------

    def empty_blocks(self) -> dict[str, object]:
        return {"schema_version": 1, "mission": {}, "packet": {}}

    def current_facts(self) -> dict[str, object]:
        return _clone(self.current)

    def at_floor_facts(self) -> dict[str, object]:
        return self._shifted(0)

    def above_floor_facts(self) -> dict[str, object]:
        return self._shifted(1)

    def below_floor_facts(self) -> dict[str, object]:
        return self._shifted(-1)

    def fenced_packet_facts(self) -> dict[str, object]:
        facts = self.current_facts()
        facts["packet"]["issue"] = self.fenced_packet_issues[0]
        return facts

    def foreign_mission_facts(self) -> dict[str, object]:
        facts = self.current_facts()
        facts["mission"]["issue"] = self.floor["mission_issue"] + 1
        return facts

    def _shifted(self, delta: int) -> dict[str, object]:
        """Ba trường đơn điệu dời quanh SÀN, giữ nguyên issue và hash của fixture."""
        facts = self.current_facts()
        for block, field, floor_key in MONOTONIC_FIELDS:
            facts[block][field] = self.floor[floor_key] + delta
        return facts


def _clone(value: Mapping[str, object]) -> dict[str, object]:
    return json.loads(json.dumps(value, sort_keys=True))


def _fail(message: str) -> AuthorityFixtureError:
    return AuthorityFixtureError(message)


def locate(explicit: str | None = None, environment: Mapping[str, str] | None = None) -> str | None:
    """Vị trí fixture: đối số dòng lệnh trước, rồi biến môi trường.

    Biến môi trường ở đây chỉ là ĐỊA CHỈ, không phải thẩm quyền: nội dung vẫn
    phải niêm phong read-only và nằm ngoài checkout ứng viên.
    """
    if explicit:
        return explicit
    values = os.environ if environment is None else environment
    located = values.get(FIXTURE_PATH_ENV)
    return located or None


def _positive_int(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise _fail("%s must be a positive integer" % label)
    return value


def _block(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise _fail("%s must be an object" % label)
    return value


def load(path: str | pathlib.Path, candidate_root: str | pathlib.Path) -> AuthorityFixture:
    fixture_path = pathlib.Path(path)
    safe_io.require_outside_tree(
        fixture_path, candidate_root, "authority fixture", AuthorityFixtureError
    )
    raw = safe_io.read_regular_single_link(
        fixture_path, "authority fixture", AuthorityFixtureError, require_readonly=True
    )
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise _fail("authority fixture is not strict UTF-8 JSON: %s" % exc) from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise _fail("authority fixture must be a schema_version 1 object")
    missing = [name for name in TOP_LEVEL_KEYS if name not in value]
    extra = sorted(set(value) - set(TOP_LEVEL_KEYS), key=str)
    if missing or extra:
        raise _fail(
            "authority fixture must name exactly %s: missing=%s unexpected=%s"
            % (list(TOP_LEVEL_KEYS), missing, extra)
        )
    produced_by = value.get("produced_by")
    if not isinstance(produced_by, str) or not produced_by:
        raise _fail("authority fixture must record a non-empty produced_by")
    source = _block(value.get("source"), "authority fixture source")
    if not source:
        raise _fail("authority fixture must record the durable source it was read from")

    floor_value = _block(value.get("authority_floor"), "authority fixture floor")
    if set(floor_value) != set(AUTHORITY_FLOOR_KEYS):
        raise _fail(
            "authority fixture floor must name exactly %s" % list(AUTHORITY_FLOOR_KEYS)
        )
    floor = {key: _positive_int(floor_value[key], "authority_floor.%s" % key) for key in AUTHORITY_FLOOR_KEYS}
    # Ca "dưới sàn" được DẪN XUẤT bằng sàn trừ một, nên sàn phải còn chỗ để trừ
    # mà vẫn là số nguyên dương.  Nói ra bằng lỗi có tên thay vì sinh ra một ca
    # kiểm không hợp lệ (revision 0) rồi đổ cho code.
    for _block_name, _field, floor_key in MONOTONIC_FIELDS:
        if floor[floor_key] < 2:
            raise _fail(
                "authority fixture floor.%s must be at least 2 so a below-floor case stays a positive integer"
                % floor_key
            )

    current = _block(value.get("current_durable_facts"), "authority fixture current facts")
    if set(current) != {"schema_version", "mission", "packet"}:
        raise _fail("authority fixture current facts must contain exactly mission and packet blocks")
    if current.get("schema_version") != 1:
        raise _fail("authority fixture current facts must be a schema_version 1 object")
    mission = _block(current.get("mission"), "authority fixture current mission")
    packet = _block(current.get("packet"), "authority fixture current packet")
    # Hợp đồng trường lấy từ `authority.py` — khai báo DUY NHẤT.  Fixture phải
    # đi lọt chính `validate_durable_facts`, nếu không thì ca kiểm đỏ vì hình
    # dạng fixture chứ không vì ngữ nghĩa sàn, và phản chứng mất nghĩa.
    for label, block_value, fields in (
        ("mission", mission, authority.MISSION_FIELDS),
        ("packet", packet, authority.PACKET_FIELDS),
    ):
        if set(block_value) != set(fields):
            raise _fail(
                "authority fixture current %s must name exactly %s" % (label, list(fields))
            )
    for label, value_ in (
        ("mission.plan_hash", mission.get("plan_hash")),
        ("packet.spec_hash", packet.get("spec_hash")),
    ):
        if not isinstance(value_, str) or not SHA256.fullmatch(value_):
            raise _fail("authority fixture current %s must be an exact lowercase SHA-256" % label)

    # Sàn và facts hiện hành phải NÓI CÙNG MỘT THẨM QUYỀN.  Đây chính là cái bẫy
    # trôi lệch mà finding đòi: khi durable authority tiến lên, Dispatcher sinh
    # lại fixture; nếu sàn trong pin không tiến theo thì mâu thuẫn lộ ra ở đây
    # chứ không nằm im trong một hằng của ứng viên.
    if _positive_int(mission.get("issue"), "current mission.issue") != floor["mission_issue"]:
        raise _fail(
            "authority fixture mission.issue %r disagrees with floor.mission_issue %r"
            % (mission.get("issue"), floor["mission_issue"])
        )
    if _positive_int(packet.get("issue"), "current packet.issue") != floor["packet_issue"]:
        raise _fail(
            "authority fixture packet.issue %r disagrees with floor.packet_issue %r"
            % (packet.get("issue"), floor["packet_issue"])
        )
    for block_name, field, floor_key in MONOTONIC_FIELDS:
        block = mission if block_name == "mission" else packet
        actual = _positive_int(block.get(field), "current %s.%s" % (block_name, field))
        if actual < floor[floor_key]:
            raise _fail(
                "authority fixture current %s.%s %r is below its own floor %s %r"
                % (block_name, field, actual, floor_key, floor[floor_key])
            )

    fenced = value.get("fenced_packet_issues")
    if not isinstance(fenced, list) or not fenced:
        raise _fail("authority fixture must list at least one fenced packet issue")
    fenced_issues = tuple(
        _positive_int(item, "fenced_packet_issues[%d]" % index) for index, item in enumerate(fenced)
    )
    if len(set(fenced_issues)) != len(fenced_issues):
        raise _fail("fenced_packet_issues must be duplicate-free")
    if floor["packet_issue"] in fenced_issues:
        raise _fail("the current packet issue cannot also be fenced")

    return AuthorityFixture(
        path=str(fixture_path.resolve()),
        sha256=hashlib.sha256(raw).hexdigest(),
        produced_by=produced_by,
        source=_clone(source),
        floor=floor,
        current=_clone(current),
        fenced_packet_issues=fenced_issues,
    )
