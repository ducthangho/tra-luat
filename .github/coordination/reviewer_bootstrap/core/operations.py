"""Tập operation ĐÓNG và schema tham số máy đọc được (acceptance §3 mục 1-2 của #77).

Bất biến:
  - Tập operation là ĐÓNG. Một tên ngoài tập bị từ chối ĐÍCH DANH (thông điệp nêu đúng tên op),
    KHÔNG im lặng bỏ qua.
  - Mỗi operation có schema tham số máy đọc được; thiếu HOẶC thừa tham số bị từ chối TRƯỚC khi
    chạy - validate() không bao giờ gọi handler.

Schema là dữ liệu thuần (JSON-serializable), không phải code, để bên ngoài kiểm kê được bằng máy
thay vì phải đọc thân hàm.
"""

SCHEMA_VERSION = 1

# Kiểu tham số -> vị từ kiểm. Giữ hẹp có chủ đích: mở rộng kiểu là mở rộng bề mặt tấn công.
_TYPE_CHECKS = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "object": lambda v: isinstance(v, dict),
}

# ─────────────────────────────────────────────────────────────────────────────
# TẬP ĐÓNG. Thêm một op nghĩa là sửa bảng này - không có đường đăng ký động,
# vì đăng ký động chính là đường làm cho "đóng" trở thành lời văn.
# ─────────────────────────────────────────────────────────────────────────────
OPERATIONS = {
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
            "reviewed_sha": {"type": "string", "required": True},
            "verdict": {
                "type": "string",
                "required": True,
                "enum": ["approve", "changes_requested", "blocked"],
            },
            "payload": {"type": "object", "required": False},
        },
    },
}

OPERATION_NAMES = tuple(sorted(OPERATIONS))


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


class ParameterError(OperationError):
    """Thiếu/thừa/sai kiểu tham số. Nêu đích danh tên tham số."""

    def __init__(self, name, message, missing=(), unexpected=()):
        self.operation = name
        self.missing = tuple(missing)
        self.unexpected = tuple(unexpected)
        super().__init__(message)


def schema():
    """Trả bản sao schema máy đọc được (JSON-serializable)."""
    return {
        "schema_version": SCHEMA_VERSION,
        "closed": True,
        "operations": {
            name: {
                "kind": spec["kind"],
                "params": {p: dict(meta) for p, meta in spec["params"].items()},
            }
            for name, spec in OPERATIONS.items()
        },
    }


def validate(name, params):
    """Kiểm op + tham số TRƯỚC khi chạy. Ném lỗi đích danh, không bao giờ gọi handler.

    Trả về dict tham số đã kiểm (bản sao) khi hợp lệ.
    """
    if name not in OPERATIONS:
        raise UnknownOperationError(name)
    if not isinstance(params, dict):
        raise ParameterError(name, "operation %r: params must be an object" % name)

    spec = OPERATIONS[name]["params"]
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
    return dict(params)
