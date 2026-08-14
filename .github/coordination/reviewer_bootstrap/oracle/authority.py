"""Validation for the sealed, read-only Dispatcher authority bundle.

No Mission, Packet, generation, commit, or hash value is compiled into this
module.  The caller supplies independently measured observations; the sealed
bundle supplies the expected durable authority.  Equality is checked at every
leaf before any oracle evaluation starts.

Bằng nhau THÔI thì chưa đủ: hai tệp cùng nói `mission: {}` vẫn bằng nhau.  Vì vậy
`validate_durable_facts` đòi HÌNH DẠNG đầy đủ cộng một SÀN đơn điệu do Dispatcher
cấp trong pin niêm phong (R3 của verdict 5297249899).
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from typing import Mapping

HERE = pathlib.Path(__file__).resolve().parent
PARENT = HERE.parent
if str(PARENT) not in sys.path:
    sys.path.insert(0, str(PARENT))

from oracle import safe_io  # noqa: E402
from oracle.trusted_inventory import AUTHORITY_FLOOR_KEYS  # noqa: E402

OID40 = re.compile(r"[0-9a-f]{40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")

MISSION_FIELDS = ("issue", "revision", "plan_hash")
PACKET_FIELDS = ("issue", "revision", "generation", "spec_hash")


class AuthorityError(RuntimeError):
    """The sealed bundle is malformed, mutable, stale, or mismatched."""


def _read_sealed(path: pathlib.Path) -> bytes:
    return safe_io.read_regular_single_link(
        path, "authority bundle", AuthorityError, require_readonly=True
    )


def _walk_differences(expected: object, actual: object, path: str = "") -> list[str]:
    if isinstance(expected, Mapping) and isinstance(actual, Mapping):
        differences = []
        expected_keys = set(expected)
        actual_keys = set(actual)
        for key in sorted(expected_keys - actual_keys, key=str):
            differences.append((path + "." if path else "") + str(key) + " missing")
        for key in sorted(actual_keys - expected_keys, key=str):
            differences.append((path + "." if path else "") + str(key) + " unexpected")
        for key in sorted(expected_keys & actual_keys, key=str):
            child = (path + "." if path else "") + str(key)
            differences.extend(_walk_differences(expected[key], actual[key], child))
        return differences
    if type(expected) is not type(actual) or expected != actual:
        return [path + " changed"]
    return []


def _require_hashes(value: object, path: str = "") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = (path + "." if path else "") + str(key)
            if key in ("head", "tree", "commit_sha", "file_git_oid"):
                if not isinstance(child, str) or not OID40.fullmatch(child):
                    raise AuthorityError("%s must be an exact lowercase 40-hex Git oid" % child_path)
            if str(key).endswith("sha256") or key in ("plan_hash", "spec_hash"):
                if not isinstance(child, str) or not SHA256.fullmatch(child):
                    raise AuthorityError("%s must be an exact lowercase SHA-256" % child_path)
            _require_hashes(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _require_hashes(child, "%s[%d]" % (path, index))


def _positive_int(value: object, label: str) -> int:
    # `isinstance(True, int)` là True trong Python — bool lọt qua kiểm kiểu số là
    # bẫy im lặng, nên loại bool ra TRƯỚC.
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise AuthorityError("%s must be a positive integer" % label)
    return value


def _exact_block(value: object, fields: tuple[str, ...], label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise AuthorityError("%s must be an object" % label)
    missing = [name for name in fields if name not in value]
    extra = sorted(set(value) - set(fields), key=str)
    if missing or extra:
        raise AuthorityError(
            "%s must name exactly %s: missing=%s unexpected=%s"
            % (label, list(fields), missing, extra)
        )
    return value


def validate_durable_facts(
    facts: Mapping[str, object], floor: Mapping[str, object]
) -> dict[str, object]:
    """Đòi hình dạng ĐẦY ĐỦ cộng sàn hiện hành, và chết theo TÊN trường sai.

    Trước bản vá này một bó chỉ chứa `mission: {}` và `packet: {}` đi qua sạch:
    chỉ TẬP KHOÁ ngoài cùng được kiểm, còn ruột thì không.
    """
    if not isinstance(floor, Mapping) or set(floor) != set(AUTHORITY_FLOOR_KEYS):
        raise AuthorityError(
            "Dispatcher authority floor must name exactly %s" % list(AUTHORITY_FLOOR_KEYS)
        )
    for key in AUTHORITY_FLOOR_KEYS:
        _positive_int(floor[key], "authority_floor.%s" % key)

    mission = _exact_block(facts.get("mission"), MISSION_FIELDS, "durable facts mission")
    packet = _exact_block(facts.get("packet"), PACKET_FIELDS, "durable facts packet")
    _positive_int(mission["issue"], "mission.issue")
    _positive_int(mission["revision"], "mission.revision")
    _positive_int(packet["issue"], "packet.issue")
    _positive_int(packet["revision"], "packet.revision")
    _positive_int(packet["generation"], "packet.generation")
    for label, value in (("mission.plan_hash", mission["plan_hash"]), ("packet.spec_hash", packet["spec_hash"])):
        if not isinstance(value, str) or not SHA256.fullmatch(value):
            raise AuthorityError("%s must be an exact lowercase SHA-256" % label)

    if mission["issue"] != floor["mission_issue"]:
        raise AuthorityError(
            "mission.issue names a fenced authority: expected %r got %r"
            % (floor["mission_issue"], mission["issue"])
        )
    if packet["issue"] != floor["packet_issue"]:
        raise AuthorityError(
            "packet.issue names a fenced authority: expected %r got %r"
            % (floor["packet_issue"], packet["issue"])
        )
    stale = []
    if mission["revision"] < floor["mission_revision_min"]:
        stale.append("mission.revision %r < floor %r" % (mission["revision"], floor["mission_revision_min"]))
    if packet["revision"] < floor["packet_revision_min"]:
        stale.append("packet.revision %r < floor %r" % (packet["revision"], floor["packet_revision_min"]))
    if packet["generation"] < floor["packet_generation_min"]:
        stale.append(
            "packet.generation %r < floor %r" % (packet["generation"], floor["packet_generation_min"])
        )
    if stale:
        raise AuthorityError("durable facts are stale against the Dispatcher floor: %s" % "; ".join(stale))
    return {"mission": dict(mission), "packet": dict(packet)}


def load_and_verify(path: pathlib.Path | str, observations: Mapping[str, object]) -> dict[str, object]:
    raw = _read_sealed(pathlib.Path(path))
    try:
        bundle = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise AuthorityError("authority bundle is not strict UTF-8 JSON: %s" % exc) from exc
    if not isinstance(bundle, dict) or bundle.get("schema_version") != 1:
        raise AuthorityError("authority bundle must be a schema_version 1 object")
    actual = dict(bundle)
    actual.pop("schema_version", None)
    # Pin nguồn và bó authority dùng CHUNG một tệp niêm phong.  `candidate`,
    # `trusted_source_paths` và digest kiểm kê VẪN được so vì chúng nằm trong
    # observations đã đo; chỉ hai khối chỉ-dành-cho-pin mới bỏ qua ở đây — chúng
    # đã được `source_pin.pin_blocks` kiểm hình dạng và `oracle` đối chiếu riêng.
    for key in ("target", "authority_floor"):
        actual.pop(key, None)
    expected = dict(observations)
    differences = _walk_differences(expected, actual)
    if differences:
        raise AuthorityError("authority mismatch: %s" % ", ".join(differences))
    _require_hashes(actual)
    return bundle
