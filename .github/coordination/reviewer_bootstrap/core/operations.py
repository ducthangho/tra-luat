"""Tập operation ĐÓNG và schema tham số máy đọc được (acceptance §3 mục 1-2 của #77).

Bất biến:
  - Tập operation là ĐÓNG. Một tên ngoài tập bị từ chối ĐÍCH DANH (thông điệp nêu đúng tên op),
    KHÔNG im lặng bỏ qua.
  - Mỗi operation có schema tham số máy đọc được; thiếu HOẶC thừa tham số bị từ chối TRƯỚC khi
    chạy - validate() không bao giờ gọi handler.
  - KHÔNG có bề mặt nào để nhét credential vào, kể cả BÊN TRONG một tham số kiểu `object`.

Schema là dữ liệu thuần (JSON-serializable), không phải code, để bên ngoài kiểm kê được bằng máy
thay vì phải đọc thân hàm.

──────────────────────────────────────────────────────────────────────────────
"ĐÓNG" ở đây nghĩa là gì - và vì sao bản g1 KHÔNG đóng (finding wp77-g1-spec-01)
──────────────────────────────────────────────────────────────────────────────
g1 khai `OPERATIONS` là một `dict` công khai, khả biến, và fake store dispatch bằng
`getattr(self, "_op_" + op_name)`. Auditor gắn `OPERATIONS["read_secrets"]` + `_op_read_secrets`
lúc chạy rồi gọi `store.call(...)` THÀNH CÔNG. Nói cách khác: "đóng" chỉ là lời văn trong docstring.

Bản này đóng bằng ba lớp độc lập, mỗi lớp một mình đã đủ chặn thủ thuật đó:

  1. Bảng công khai `OPERATIONS` là `MappingProxyType` (kể cả spec và params lồng bên trong).
     Gán vào nó ném `TypeError` ngay.
  2. `validate()` so tên với `_CLOSED_NAMES` - một `frozenset` được CHỤP lúc import và gắn vào
     tham số mặc định của hàm. Rebinding biến toàn cục của module sau đó KHÔNG nới được tập này;
     tham số mặc định đã bind tại thời điểm `def` chạy.
  3. Nếu bảng riêng `_OPERATIONS` bị chọc thủng bằng cách khác (nó vẫn là object khả biến trong
     cùng tiến trình), `_assert_not_tampered()` phát hiện lệch so với ảnh chụp và ném lỗi ĐÍCH
     DANH kèm tên đã bị thêm/bớt.

Điều KHÔNG hứa: Python cùng tiến trình không có ranh giới bảo vệ thật - ai gán được thuộc tính
module thì gán được mọi thứ. Cái ba lớp trên bảo đảm là **không tồn tại đường đăng ký động được
hỗ trợ**, và mọi lối vòng đều fail-closed có tên gọi, thay vì chạy im lặng.
"""

import re
from types import MappingProxyType

SCHEMA_VERSION = 1

# Kiểu tham số -> vị từ kiểm. Giữ hẹp có chủ đích: mở rộng kiểu là mở rộng bề mặt tấn công.
_TYPE_CHECKS = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "object": lambda v: isinstance(v, dict),
}

# ── Bề mặt credential bên trong payload (finding wp77-g1-sec-03) ─────────────
# g1 chỉ quét TÊN THAM SỐ top-level, nên `payload={"token": ...}` đi thẳng vào ledger. Bản này
# quét ĐỆ QUY cả khoá lẫn giá trị của mọi tham số kiểu `object`.
#
# Vì sao TỪ CHỐI chứ không scrub: scrub sửa dữ liệu của người gọi một cách im lặng - đúng lớp lỗi
# "khử trùng lặp nuốt mất nội dung" mà chính packet này đang chặn ở chỗ khác (409 CONFLICT). Từ
# chối đích danh để người gọi biết mình vừa suýt ghi credential vào sổ bền.
# Khớp theo TỪ CUỐI của khoá, KHÔNG phải substring.
#
# Bản trước dùng `re.search` trên cả chuỗi và chặn nhầm hàng loạt khoá hợp lệ mà chính protocol
# này dùng: `session_id` (dính `session_id`), `authorization_url` (dính `auth`), `token_budget`
# (dính `token`). Một ràng buộc an ninh chặn nhầm dữ liệu hợp lệ sẽ bị người dùng vô hiệu hoá,
# và lúc đó nó không còn bảo vệ gì nữa - chặn nhầm là một cách hỏng, không phải "an toàn hơn".
#
# Quy tắc: credential nằm ở DANH TỪ CUỐI. `access_token` là token; `token_budget` là budget.
_SECRET_TAILS = frozenset(
    {
        "token", "tokens", "secret", "secrets", "password", "passwords", "passwd", "pwd",
        "credential", "credentials", "cookie", "cookies", "passphrase", "auth",
        "authorization", "bearer", "otp",
    }
)

# `key` một mình quá chung (`reconcile_key`, `sort_key`, `public_key`), nên chỉ chặn khi có
# định ngữ làm nó thành bí mật.
_SECRET_KEY_QUALIFIERS = frozenset(
    {"api", "secret", "private", "access", "signing", "encryption", "master", "auth", "session",
     "client", "app", "service", "consumer"}
)


def _split_words(key):
    """Tách khoá thành từ - hiểu cả snake_case, kebab-case, dotted và camelCase."""
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", str(key))
    return [w for w in re.split(r"[^A-Za-z0-9]+", spaced.lower()) if w]


def _key_is_credential(key):
    words = _split_words(key)
    if not words:
        return False
    tail = words[-1]
    if tail in _SECRET_TAILS:
        return True
    if tail in ("key", "keys"):
        return (words[-2] if len(words) > 1 else "") in _SECRET_KEY_QUALIFIERS
    return False

# Hình dạng credential thật, khớp trên GIÁ TRỊ. Một khoá vô hại (`note`) vẫn có thể chở token.
_CREDENTIAL_VALUE = re.compile(
    r"gh[pousr]_[A-Za-z0-9]{16,}|github_pat_[A-Za-z0-9_]{16,}|sk-ant-[A-Za-z0-9\-_]{16,}|"
    r"sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|xox[abposr]-[A-Za-z0-9-]{10,}|GOCSPX-[A-Za-z0-9_-]{16,}|"
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----"
)

# Trần độ sâu/kích thước: một payload lồng vô hạn là DoS cho chính bộ quét.
_MAX_PAYLOAD_DEPTH = 12
_MAX_PAYLOAD_NODES = 4096

# ── Format máy đọc được cho giá trị chuỗi ────────────────────────────────────
# `reviewed_sha: string` là chưa đủ: audit gọi `post_verdict` với "not-a-sha" và với một chuỗi
# hình `ghp_…`, cả hai đều được PERSIST vào sổ bền. Verdict neo vào một thứ không phải commit thì
# nó không neo vào đâu cả - §1 bất biến 9 đòi "exact SHA", và một SHA viết tắt cũng KHÔNG exact.
GIT_OID_RE = re.compile(r"^[0-9a-f]{40}$")

_FORMATS = {
    "git_oid": (
        GIT_OID_RE,
        "a full lowercase 40-hex Git object id (abbreviated or non-hex values are not exact SHAs)",
    ),
}

_OPERATIONS_SOURCE = {
    "read_issue": {
        "kind": "read",
        "params": {
            "repo": {"type": "string", "required": True},
            "issue_number": {"type": "integer", "required": True},
        },
    },
    "read_comment": {
        "kind": "read",
        "params": {
            "repo": {"type": "string", "required": True},
            "comment_id": {"type": "integer", "required": True},
        },
    },
    "read_pr": {
        "kind": "read",
        "params": {
            "repo": {"type": "string", "required": True},
            "pull_number": {"type": "integer", "required": True},
        },
    },
    "read_ci_run": {
        "kind": "read",
        "params": {
            "repo": {"type": "string", "required": True},
            "run_id": {"type": "integer", "required": True},
        },
    },
    "read_diff": {
        "kind": "read",
        "params": {
            "repo": {"type": "string", "required": True},
            "pull_number": {"type": "integer", "required": True},
        },
    },
    "run_test": {
        # RA-01 chỉ ĐỊNH NGHĨA op này. Thực thi thật thuộc sandbox RA-02; xem fake_github.run_test.
        "kind": "delegated",
        "params": {
            "repo": {"type": "string", "required": True},
            "command": {"type": "string", "required": True},
            "timeout_seconds": {"type": "integer", "required": False},
        },
    },
    "post_heartbeat": {
        "kind": "write",
        "params": {
            "repo": {"type": "string", "required": True},
            "issue_number": {"type": "integer", "required": True},
            "reconcile_key": {"type": "string", "required": True},
            "payload": {"type": "object", "required": True},
        },
    },
    "post_verdict": {
        "kind": "write",
        "params": {
            "repo": {"type": "string", "required": True},
            "issue_number": {"type": "integer", "required": True},
            "reconcile_key": {"type": "string", "required": True},
            "reviewed_sha": {"type": "string", "required": True, "format": "git_oid"},
            "verdict": {
                "type": "string",
                "required": True,
                "enum": ["approve", "changes_requested", "blocked"],
            },
            "payload": {"type": "object", "required": False},
        },
    },
}


def _freeze_spec(spec):
    """Đóng băng một spec tới tận lá - proxy nông vẫn cho sửa params bên trong."""
    return MappingProxyType(
        {
            "kind": spec["kind"],
            "params": MappingProxyType(
                {p: MappingProxyType(dict(meta)) for p, meta in spec["params"].items()}
            ),
        }
    )


_OPERATIONS = {name: _freeze_spec(spec) for name, spec in _OPERATIONS_SOURCE.items()}

# Lớp 1: bảng công khai chỉ đọc. `OPERATIONS["x"] = ...` ném TypeError.
OPERATIONS = MappingProxyType(_OPERATIONS)
OPERATION_NAMES = tuple(sorted(_OPERATIONS))

# Lớp 2+3: ảnh chụp bất biến tại thời điểm import. Mọi thứ sau đó so với ảnh chụp này.
_CLOSED_NAMES = frozenset(OPERATION_NAMES)


class OperationError(Exception):
    """Gốc chung để caller bắt được mọi từ chối của lớp validate."""


class UnknownOperationError(OperationError):
    """Op không nằm trong tập đóng. Thông điệp PHẢI nêu đúng tên op bị từ chối."""

    def __init__(self, name):
        self.operation = name
        super().__init__(
            "unknown operation: %r is not in the closed operation set; known operations: %s"
            % (name, ", ".join(OPERATION_NAMES))
        )


class OperationSetTamperedError(OperationError):
    """Bảng operation bị sửa lúc chạy. Nêu đích danh tên đã thêm/bớt."""

    def __init__(self, added, removed):
        self.added = tuple(sorted(added))
        self.removed = tuple(sorted(removed))
        super().__init__(
            "closed operation set was mutated at runtime - added: %s; removed: %s"
            % (", ".join(self.added) or "(none)", ", ".join(self.removed) or "(none)")
        )


class ParameterError(OperationError):
    """Thiếu/thừa/sai kiểu tham số. Nêu đích danh tên tham số."""

    def __init__(self, name, message, missing=(), unexpected=()):
        self.operation = name
        self.missing = tuple(missing)
        self.unexpected = tuple(unexpected)
        super().__init__(message)


class CredentialSurfaceError(ParameterError):
    """Payload chứa thứ trông như credential. Nêu ĐÍCH DANH đường dẫn trong payload."""

    def __init__(self, name, param, path, reason):
        self.param = param
        self.path = path
        self.reason = reason
        super().__init__(
            name,
            "operation %r parameter %r rejected before execution - credential-like %s at %s"
            % (name, param, reason, path),
        )


def _assert_not_tampered(_snapshot=_CLOSED_NAMES, _table=_OPERATIONS):
    """Lớp 3: bảng riêng vẫn là object khả biến; so với ảnh chụp để không tin nó một cách mù quáng."""
    live = frozenset(_table)
    if live != _snapshot:
        raise OperationSetTamperedError(live - _snapshot, _snapshot - live)


def _scan_credential_surface(op_name, param, value):
    """Duyệt đệ quy một tham số `object`, từ chối khoá/giá trị trông như credential."""
    nodes = 0
    stack = [(value, param, 0)]
    while stack:
        node, path, depth = stack.pop()
        nodes += 1
        if nodes > _MAX_PAYLOAD_NODES:
            raise ParameterError(
                op_name,
                "operation %r parameter %r rejected before execution - payload exceeds %d nodes"
                % (op_name, param, _MAX_PAYLOAD_NODES),
            )
        if depth > _MAX_PAYLOAD_DEPTH:
            raise ParameterError(
                op_name,
                "operation %r parameter %r rejected before execution - payload nested deeper than %d"
                % (op_name, param, _MAX_PAYLOAD_DEPTH),
            )
        if isinstance(node, dict):
            for key, sub in node.items():
                child = "%s.%s" % (path, key)
                if isinstance(key, str) and _key_is_credential(key):
                    raise CredentialSurfaceError(op_name, param, child, "key name %r" % key)
                stack.append((sub, child, depth + 1))
        elif isinstance(node, (list, tuple)):
            for index, sub in enumerate(node):
                stack.append((sub, "%s[%d]" % (path, index), depth + 1))
        elif isinstance(node, str):
            if _CREDENTIAL_VALUE.search(node):
                raise CredentialSurfaceError(op_name, param, path, "value shape")


def schema():
    """Trả bản sao schema máy đọc được (JSON-serializable)."""
    _assert_not_tampered()
    return {
        "schema_version": SCHEMA_VERSION,
        "closed": True,
        "closure_enforcement": [
            "public table is a read-only mapping proxy (mutation raises TypeError)",
            "validate() compares against a frozenset snapshot bound at import time",
            "runtime drift of the private table raises OperationSetTamperedError by name",
        ],
        # Ràng buộc payload được CÔNG BỐ, không chôn trong regex: người gọi phải biết trước cái gì
        # bị chặn, nếu không họ chỉ phát hiện ra lúc bị từ chối giữa production.
        "credential_surface": {
            "rule": "a key is rejected when its LAST word is a secret noun; substring matching is "
                    "not used, so session_id / authorization_url / token_budget / author / "
                    "cookie_policy are accepted",
            "rejected_key_tails": sorted(_SECRET_TAILS),
            "rejected_key_tail_key_qualifiers": sorted(_SECRET_KEY_QUALIFIERS),
            "rejected_value_shapes": "known credential prefixes (ghp_, github_pat_, sk-ant-, "
                                     "AKIA, xox*, GOCSPX-, PEM private key headers)",
            "max_depth": _MAX_PAYLOAD_DEPTH,
            "max_nodes": _MAX_PAYLOAD_NODES,
        },
        "formats": {name_: human for name_, (_rx, human) in _FORMATS.items()},
        "operations": {
            name: {
                "kind": spec["kind"],
                "params": {p: dict(meta) for p, meta in spec["params"].items()},
            }
            for name, spec in _OPERATIONS.items()
        },
    }


def validate(name, params, _closed=_CLOSED_NAMES):
    """Kiểm op + tham số TRƯỚC khi chạy. Ném lỗi đích danh, không bao giờ gọi handler.

    Trả về dict tham số đã kiểm (bản sao) khi hợp lệ.

    `_closed` là tham số mặc định CÓ CHỦ ĐÍCH: nó bind vào frozenset lúc `def` chạy, nên
    `operations._CLOSED_NAMES = <tập rộng hơn>` sau đó KHÔNG nới được tập op.
    """
    if name not in _closed:
        raise UnknownOperationError(name)
    _assert_not_tampered()
    if not isinstance(params, dict):
        raise ParameterError(name, "operation %r: params must be an object" % name)

    spec = _OPERATIONS[name]["params"]
    given = set(params)
    required = {p for p, m in spec.items() if m["required"]}
    allowed = set(spec)

    missing = sorted(required - given)
    unexpected = sorted(given - allowed)
    if missing or unexpected:
        bits = []
        if missing:
            bits.append("missing parameter(s): %s" % ", ".join(missing))
        if unexpected:
            bits.append("unexpected parameter(s): %s" % ", ".join(unexpected))
        raise ParameterError(
            name,
            "operation %r rejected before execution - %s" % (name, "; ".join(bits)),
            missing=missing,
            unexpected=unexpected,
        )

    for pname, value in params.items():
        meta = spec[pname]
        if not _TYPE_CHECKS[meta["type"]](value):
            raise ParameterError(
                name,
                "operation %r parameter %r expects type %s, got %s"
                % (name, pname, meta["type"], type(value).__name__),
            )
        if "enum" in meta and value not in meta["enum"]:
            raise ParameterError(
                name,
                "operation %r parameter %r must be one of %s, got %r"
                % (name, pname, ", ".join(meta["enum"]), value),
            )
        if "format" in meta:
            pattern, human = _FORMATS[meta["format"]]
            if not pattern.match(value):
                raise ParameterError(
                    name,
                    "operation %r parameter %r rejected before execution - must be %s, got %r"
                    % (name, pname, human, value),
                )
        if meta["type"] == "object":
            _scan_credential_surface(name, pname, value)
    return dict(params)
