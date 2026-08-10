"""Suite phản chứng cho lõi RA-01 (acceptance §3 của #77).

Nguyên tắc: "có mặt trong code" KHÔNG phải nghiệm thu. Mỗi bất biến phải có một phép thử CHẠY
ĐƯỢC, và mỗi tripwire phải có ĐỐI CHỨNG DƯƠNG chứng minh nó còn sống - một detector chết cũng
báo "sạch".

ID test dùng tiền tố `ra01_`, KHÔNG dùng `wp77_`: `wp77_` là namespace của test fragment trong
`scripts/test_fragments/`, mà §2 của #77 khai rõ fragment KHÔNG thuộc write set và KHÔNG được tạo
trong Packet này. Dùng lại tiền tố đó sẽ đâm vào test-ID registry dùng chung (protocol §10.2).

──────────────────────────────────────────────────────────────────────────────
TEST `ra01_regression_*` - phản chứng của auditor, đã đóng thành hồi quy
──────────────────────────────────────────────────────────────────────────────
Audit g1 (PR #78) không dừng ở việc đọc code: nó CHẠY được năm thủ thuật vượt rào. Sửa code mà
không khoá bằng test thì lỗ hổng chỉ đang nghỉ phép. Mỗi test dưới tiền tố `ra01_regression_` tái
diễn ĐÚNG thủ thuật của auditor và đòi bị TỪ CHỐI; ID finding ghi ngay trong tên test để đối chiếu
được bằng máy:

  wp77-g1-spec-01  ra01_regression_spec01_*   đăng ký op lúc chạy
  wp77-g1-spec-02  ra01_regression_spec02_*   subprocess kế thừa environment
  wp77-g1-sec-01   ra01_regression_sec01_*    locator thoát khỏi run_root
  wp77-g1-sec-02   ra01_regression_sec02_*    socket cache trước guard; scanner mù importlib/subprocess
  wp77-g1-sec-03   ra01_regression_sec03_*    credential nhét trong payload
"""

import ast
import contextlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_HERE)
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from core import artifacts, guards, operations  # noqa: E402
from core.fake_github import FakeGitHubError, seeded_store  # noqa: E402
from core.ledger import Ledger  # noqa: E402

CONTROLLER = os.path.join(_HERE, "controller.py")
REPO = "ducthangho/tra-luat"
# Git OID ĐẦY ĐỦ. Fixture cũ dùng "abc" và "b044f8b1" (viết tắt) - và chúng đi lọt, đó chính là
# bằng chứng `reviewed_sha: string` không đủ.
HEAD_OID = "b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb"
EXPECTED_OPERATIONS = (
    "post_heartbeat",
    "post_verdict",
    "read_ci_run",
    "read_comment",
    "read_diff",
    "read_issue",
    "read_pr",
    "run_test",
)

FORBIDDEN_IMPORTS = {
    "socket", "ssl", "http", "urllib", "urllib2", "urllib3", "requests", "httpx",
    "ftplib", "smtplib", "telnetlib", "xmlrpc", "asyncio", "aiohttp",
    "anthropic", "openai", "google", "boto3", "botocore",
}

# Binary có khả năng tự ra mạng. Bắt theo argv[0] hằng - đủ để chặn `subprocess.run(["gh", ...])`,
# và KHÔNG hứa bắt được argv dựng động (xem `_ESCAPE_SCANNER_LIMITS`).
NETWORK_TOOLS = {"gh", "curl", "wget", "git", "ssh", "scp", "nc", "ncat", "openssl", "pip", "npm"}

# Giới hạn của chính bộ quét được khai ở `guards.STATIC_SCANNER_COVERAGE` để CLI `coverage` in ra
# được như dữ liệu. Suite chỉ đọc lại, không giữ bản sao thứ hai - hai bản sẽ trôi lệch, và bên
# quên cập nhật chính là bên công bố một claim rộng hơn thứ mình phủ.
_ESCAPE_SCANNER_LIMITS = guards.STATIC_SCANNER_COVERAGE["not_covered"]

TESTS = []


class PlatformUnsupported(Exception):
    """Nền này KHÔNG cho thực hiện phép thử - báo LỚN, không nuốt thành 'passed'.

    Chỉ dùng khi hệ điều hành từ chối dựng được FIXTURE (vd Windows không cho tạo symlink nếu
    thiếu quyền), và CHỈ khi bất biến tương ứng còn một phép thử khác chạy được ở mọi nền. Skip mà
    không có đối trọng portable thì đúng là "xanh vì chẳng chạy gì" - lớp lỗi của #54.
    """


def test(fn):
    TESTS.append(fn)
    return fn


# ─────────────────────────────────────────────────────────────────────────────
# Bộ quét tĩnh dùng chung
# ─────────────────────────────────────────────────────────────────────────────
def _parse_dir(directory):
    for name in sorted(os.listdir(directory)):
        if name.endswith(".py"):
            with open(os.path.join(directory, name), "r", encoding="utf-8") as fh:
                yield name, ast.parse(fh.read(), filename=name)


def _scan_forbidden_imports(directory, allowed):
    """Liệt kê (tệp, module) import bị cấm trong `directory`, bỏ qua cặp nằm trong `allowed`."""
    offenders = []
    for name, tree in _parse_dir(directory):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                roots = [(node.module or "").split(".")[0]]
            else:
                continue
            for module in roots:
                if module in FORBIDDEN_IMPORTS and (name, module) not in allowed:
                    offenders.append((name, module))
    return offenders


def _dotted(node):
    """Tên chấm của một biểu thức gọi (`importlib.import_module`), hoặc None."""
    bits = []
    while isinstance(node, ast.Attribute):
        bits.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        bits.append(node.id)
        return ".".join(reversed(bits))
    return None


def _const_str(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _alias_map(tree):
    """Bảng alias của một tệp: alias module -> module thật, và alias hàm -> 'module.hàm'.

    Không có bảng này thì `import subprocess as sp` + `sp.run(["gh", ...])` cho `offenders=[]`,
    và bộ quét chỉ bắt được kẻ tấn công không biết đổi tên - tức là không bắt được ai.
    """
    modules, funcs = {}, {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                modules[alias.asname or root] = root
        elif isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]
            for alias in node.names:
                funcs[alias.asname or alias.name] = "%s.%s" % (module, alias.name)

    # Một tầng alias qua BIẾN: `runner = sp.run` rồi `runner([...])`. Bản trước mù với đường này,
    # nên đổi tên hai lần là thoát - và "đổi tên hai lần" không phải kỹ thuật cao siêu gì.
    for _ in range(3):  # lặp vài lượt để `a = sp; b = a.run` cũng hội tụ
        changed = False
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name):
                continue
            resolved = _resolve_call(node.value, modules, funcs)
            if resolved and funcs.get(target.id) != resolved:
                # Chỉ nhận alias trỏ tới thứ ta THỰC SỰ quan tâm, để không nuốt mọi phép gán.
                root = resolved.split(".")[0]
                if root in FORBIDDEN_IMPORTS or root in ("subprocess", "importlib", "os", "builtins"):
                    funcs[target.id] = resolved
                    if "." not in resolved:
                        modules[target.id] = resolved
                    changed = True
        if not changed:
            break
    return modules, funcs


def _resolve_call(func_node, modules, funcs):
    """Tên gọi đã CANONICAL hoá qua bảng alias, hoặc None."""
    dotted = _dotted(func_node)
    if dotted is None:
        return None
    head, _dot, rest = dotted.partition(".")
    if not rest:
        resolved = funcs.get(head, head)
    else:
        base = funcs.get(head) or modules.get(head, head)
        resolved = "%s.%s" % (base, rest)
    # `builtins.__import__` và `__import__` là CÙNG một hàm; ghi hai tên cho cùng một thứ là mời
    # người ta đi vòng qua tên còn lại.
    if resolved.startswith("builtins."):
        resolved = resolved[len("builtins."):]
    return resolved


def _scan_escape_paths(directory, allowed):
    """Đường thoát mà `Import`/`ImportFrom` KHÔNG thấy (finding wp77-g1-sec-02).

    Bắt ba lớp: import động có đích hằng, gọi tiến trình ngoài với argv[0] hằng nằm trong
    NETWORK_TOOLS, và `os.system`/`os.popen`.
    """
    offenders = []
    for name, tree in _parse_dir(directory):
        modules, funcs = _alias_map(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            called = _resolve_call(node.func, modules, funcs)
            if called in ("importlib.import_module", "__import__") and node.args:
                target = _const_str(node.args[0])
                if target and target.split(".")[0] in FORBIDDEN_IMPORTS:
                    entry = (name, "dynamic-import:%s" % target.split(".")[0])
                    if entry not in allowed:
                        offenders.append(entry)
            if called in ("os.system", "os.popen"):
                entry = (name, "shell:%s" % called)
                if entry not in allowed:
                    offenders.append(entry)
            if called and called.split(".")[0] == "subprocess" and node.args:
                first = node.args[0]
                argv0 = _const_str(first)
                if argv0 is None and isinstance(first, (ast.List, ast.Tuple)) and first.elts:
                    argv0 = _const_str(first.elts[0])
                if argv0 and os.path.basename(argv0) in NETWORK_TOOLS:
                    entry = (name, "subprocess:%s" % os.path.basename(argv0))
                    if entry not in allowed:
                        offenders.append(entry)
    return offenders


_SENSITIVE_LITERAL = re.compile(r"^(GH_TOKEN|GITHUB_TOKEN|GITHUB_PAT|AWS_|ANTHROPIC_|OPENAI_)")


def _scan_unguarded_env_access(path):
    """Truy cập biến nhạy cảm NGOÀI một khối `with ... EnvGuard(...)` (finding wp77-g1-spec-02).

    Auditor chỉ ra `selftest.py:509` tự đọc đúng các biến cần bảo vệ TRƯỚC khi cài guard ở `:513`.
    Một suite làm vậy đang tự tay tạo ra lần đọc mà nó tuyên bố là không có. Phép quét này biến
    "đừng làm thế nữa" thành ràng buộc kiểm được.
    """
    with open(path, "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=os.path.basename(path))
    modules, funcs = _alias_map(tree)

    guarded = []
    for node in ast.walk(tree):
        if isinstance(node, ast.With):
            if any("EnvGuard" in (_dotted(i.context_expr.func) or "")
                   for i in node.items if isinstance(i.context_expr, ast.Call)):
                guarded.append((node.body[0].lineno, node.end_lineno))

    def inside_guard(lineno):
        return any(start <= lineno <= end for start, end in guarded)

    offenders = []

    def note(lineno, what):
        if not inside_guard(lineno):
            offenders.append((lineno, what))

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            called = _resolve_call(node.func, modules, funcs)
            if called in ("os.getenv", "os.environ.get", "os.environ.pop", "os.environ.setdefault"):
                literal = _const_str(node.args[0]) if node.args else None
                if literal and _SENSITIVE_LITERAL.match(literal.upper()):
                    note(node.lineno, "%s(%r)" % (called, literal))
            if called in ("os.environ.update", "os.environ.copy"):
                note(node.lineno, "%s(...)" % called)
        elif isinstance(node, ast.Subscript) and _resolve_call(node.value, modules, funcs) == "os.environ":
            literal = _const_str(node.slice)
            if literal and _SENSITIVE_LITERAL.match(literal.upper()):
                note(node.lineno, "os.environ[%r]" % literal)
    return offenders


def _run_cli(*argv):
    proc = subprocess.run(
        [sys.executable, CONTROLLER] + list(argv),
        capture_output=True,
        text=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _portable_child_env(extra):
    """Env tối thiểu chạy được python trên MỌI nền, cộng thêm `extra`.

    Đọc `os.environ` ở đây là đọc các biến VÔ HẠI (PATH, SYSTEMROOT...) và bộ quét
    `_scan_unguarded_env_access` chỉ chặn hằng nhạy cảm, nên không có mâu thuẫn.
    """
    base = {}
    for key in ("PATH", "SYSTEMROOT", "SystemRoot", "COMSPEC", "TEMP", "TMP", "WINDIR", "LANG"):
        value = os.environ.get(key)
        if value is not None:
            base[key] = value
    base.update(extra)
    return base


def _store(tmp, name="ledger.json"):
    """Một nguồn seed DUY NHẤT, dùng chung với controller (finding wp77-g1-dup-01)."""
    return seeded_store(os.path.join(tmp, name))


# ─────────────────────────────────────────────────────────────────────────────
# A. Tập operation ĐÓNG + schema tham số
# ─────────────────────────────────────────────────────────────────────────────
@test
def ra01_operation_set_is_closed_and_declared():
    assert operations.OPERATION_NAMES == EXPECTED_OPERATIONS, operations.OPERATION_NAMES
    schema = operations.schema()
    assert schema["closed"] is True
    assert tuple(sorted(schema["operations"])) == EXPECTED_OPERATIONS
    assert schema["closure_enforcement"], "closure enforcement is not declared machine-readably"
    # Schema phải JSON-serializable - "máy đọc được" nghĩa là máy KHÁC đọc được.
    json.dumps(schema)


@test
def ra01_unknown_operation_rejected_by_exact_name():
    bogus = "read_secrets"
    try:
        operations.validate(bogus, {})
    except operations.UnknownOperationError as exc:
        assert exc.operation == bogus
        assert bogus in str(exc), str(exc)
    else:
        raise AssertionError("unknown operation was NOT rejected")


@test
def ra01_unknown_operation_cli_rc_nonzero_and_names_op():
    rc, _out, err = _run_cli("call", "--op", "delete_repo", "--params", "{}")
    assert rc != 0, "CLI accepted a bogus operation (rc=0)"
    assert "delete_repo" in err, err


@test
def ra01_missing_parameter_rejected_by_name():
    try:
        operations.validate("read_issue", {"repo": REPO})
    except operations.ParameterError as exc:
        assert exc.missing == ("issue_number",), exc.missing
        assert "issue_number" in str(exc)
    else:
        raise AssertionError("missing parameter was NOT rejected")


@test
def ra01_extra_parameter_rejected_by_name():
    try:
        operations.validate("read_issue", {"repo": REPO, "issue_number": 77, "token": "x"})
    except operations.ParameterError as exc:
        assert exc.unexpected == ("token",), exc.unexpected
    else:
        raise AssertionError("extra parameter was NOT rejected")


@test
def ra01_wrong_type_and_enum_rejected():
    for params in ({"repo": REPO, "issue_number": "77"}, {"repo": 1, "issue_number": 77}):
        try:
            operations.validate("read_issue", params)
        except operations.ParameterError:
            pass
        else:
            raise AssertionError("bad type accepted: %r" % params)
    try:
        operations.validate(
            "post_verdict",
            {
                "repo": REPO,
                "issue_number": 77,
                "reconcile_key": "k",
                "reviewed_sha": HEAD_OID,
                "verdict": "looks_good_to_me",
            },
        )
    except operations.ParameterError as exc:
        assert "verdict" in str(exc)
    else:
        raise AssertionError("bad enum accepted")


@test
def ra01_validation_happens_before_execution():
    """Thiếu tham số phải bị chặn TRƯỚC khi chạm handler - không có side effect nào xảy ra."""
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        store.inject("read_issue", "403")  # nếu handler chạy, lỗi này nổ ra thay vì ParameterError
        try:
            store.call("read_issue", {"repo": REPO})
        except operations.ParameterError:
            pass
        else:
            raise AssertionError("validation did not run first")
        assert store.calls == [], store.calls
        # Lỗi bơm vào vẫn còn nguyên trong hàng đợi - bằng chứng dương là handler CHƯA chạy.
        assert store._injected["read_issue"] == ["403"]


@test
def ra01_regression_spec01_public_operation_table_is_immutable():
    """PHẢN CHỨNG AUDIT: `OPERATIONS["read_secrets"] = ...` phải ném, không phải ghi được."""
    try:
        operations.OPERATIONS["read_secrets"] = {"kind": "read", "params": {}}
    except TypeError:
        pass
    else:
        raise AssertionError("public OPERATIONS table accepted a runtime write")
    # Đóng băng tới tận lá: params lồng bên trong cũng không sửa được.
    try:
        operations.OPERATIONS["read_issue"]["params"]["repo"]["required"] = False
    except TypeError:
        pass
    else:
        raise AssertionError("nested parameter spec accepted a runtime write")


@test
def ra01_regression_spec01_runtime_registered_op_is_refused_by_name():
    """PHẢN CHỨNG AUDIT, bản MẠNH HƠN bản auditor chạy.

    Auditor gắn `OPERATIONS["read_secrets"]` + `_op_read_secrets` rồi `store.call(...)` chạy được.
    Ở đây ta chọc thủng cả BẢNG RIÊNG `_OPERATIONS` (thứ auditor không cần đụng tới), gắn method,
    và dựng thêm một store MỚI sau khi đã chọc - cả ba đường đều phải bị từ chối đích danh.
    """
    spec = {"kind": "read", "params": {"repo": {"type": "string", "required": True}}}
    with tempfile.TemporaryDirectory() as tmp:
        before = _store(tmp, name="before.json")
        operations._OPERATIONS["read_secrets"] = spec
        try:
            after = _store(tmp, name="after.json")
            for store in (before, after):
                store._op_read_secrets = lambda p: {"executed": True}
                try:
                    store.call("read_secrets", {"repo": REPO})
                except operations.UnknownOperationError as exc:
                    assert exc.operation == "read_secrets"
                    assert "read_secrets" in str(exc), str(exc)
                else:
                    raise AssertionError("runtime-registered operation EXECUTED")
            # Bảng bị sửa cũng phải bị phát hiện đích danh khi đọc schema.
            try:
                operations.schema()
            except operations.OperationSetTamperedError as exc:
                assert "read_secrets" in str(exc), str(exc)
            else:
                raise AssertionError("table tampering went undetected")
        finally:
            operations._OPERATIONS.pop("read_secrets", None)
        # Khôi phục xong thì mọi thứ trở lại bình thường - test không để lại bãi rác.
        assert operations.schema()["closed"] is True


@test
def ra01_regression_spec01_rebinding_module_globals_does_not_widen_the_set():
    """Nới `_CLOSED_NAMES` ở mức module KHÔNG được nới tập op thật."""
    saved = operations._CLOSED_NAMES
    operations._CLOSED_NAMES = frozenset(list(saved) + ["read_secrets"])
    try:
        try:
            operations.validate("read_secrets", {})
        except operations.UnknownOperationError:
            pass
        else:
            raise AssertionError("rebinding a module global widened the closed set")
    finally:
        operations._CLOSED_NAMES = saved


@test
def ra01_regression_spec01_dispatch_table_matches_operation_set_exactly():
    """Không dispatch bằng ghép chuỗi ⇒ bảng handler phải trùng khít tập op, kiểm được bằng máy."""
    from core import fake_github

    assert frozenset(fake_github._HANDLER_METHODS) == frozenset(operations.OPERATION_NAMES)
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        assert tuple(sorted(store._dispatch)) == EXPECTED_OPERATIONS
    # Kiểm bằng AST, KHÔNG grep chuỗi: docstring của fake_github.py cố ý TRÍCH DẪN đường dispatch
    # cũ để giải thích vì sao nó bị bỏ, nên grep sẽ báo dương tính giả trên chính lời giải thích.
    with open(os.path.join(_HERE, "fake_github.py"), "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename="fake_github.py")
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _dotted(node.func) == "getattr":
            assert not any(isinstance(a, ast.BinOp) for a in node.args), (
                "string-concatenation dispatch is back at line %d" % node.lineno
            )


# ─────────────────────────────────────────────────────────────────────────────
# B. Fake GitHub store - không chạm mạng, có cả đường LỖI
# ─────────────────────────────────────────────────────────────────────────────
@test
def ra01_fake_store_serves_every_read_operation():
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        assert store.call("read_issue", {"repo": REPO, "issue_number": 77})["number"] == 77
        assert store.call("read_comment", {"repo": REPO, "comment_id": 5236083781})["id"]
        assert store.call("read_pr", {"repo": REPO, "pull_number": 1001})["draft"] is True
        assert store.call("read_ci_run", {"repo": REPO, "run_id": 9001})["conclusion"] == "success"
        assert "diff" in store.call("read_diff", {"repo": REPO, "pull_number": 1001})


@test
def ra01_fake_store_simulates_403_404_409_and_rate_limit():
    with tempfile.TemporaryDirectory() as tmp:
        for kind, status in (("403", 403), ("404", 404), ("409", 409), ("rate_limit", 429)):
            store = _store(tmp, name="ledger_%s.json" % kind)
            store.inject("read_issue", kind)
            try:
                store.call("read_issue", {"repo": REPO, "issue_number": 77})
            except FakeGitHubError as exc:
                assert exc.status == status, (kind, exc.status)
                assert exc.operation == "read_issue"
            else:
                raise AssertionError("error kind %s was not simulated" % kind)


@test
def ra01_natural_404_for_absent_object():
    """404 phải sinh ra một cách TỰ NHIÊN từ store rỗng, không chỉ khi được bơm."""
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        try:
            store.call("read_issue", {"repo": REPO, "issue_number": 999999})
        except FakeGitHubError as exc:
            assert exc.status == 404
        else:
            raise AssertionError("absent issue did not 404")


@test
def ra01_network_guard_raises_named_error_not_hang():
    """ĐỐI CHỨNG DƯƠNG: chứng minh guard mạng còn sống, và nó ném ĐÍCH DANH chứ không treo."""
    import socket

    real_cls = socket.socket
    with guards.NetworkGuard() as guard:
        for attempt in (
            lambda: socket.socket(),
            lambda: socket.create_connection(("example.invalid", 80), timeout=1),
            lambda: socket.getaddrinfo("example.invalid", 80),
        ):
            try:
                attempt()
            except guards.NetworkAccessBlocked as exc:
                assert "blocked" in str(exc).lower()
            else:
                raise AssertionError("network attempt was NOT blocked")
        assert guard.attempts, "guard recorded no attempts while blocking three of them"
    # Gỡ patch xong phải trả lại nguyên trạng, nếu không guard sẽ rò sang test khác.
    assert socket.socket is real_cls
    probe = socket.socket()
    probe.close()


@test
def ra01_regression_sec02_blocks_socket_reference_cached_before_guard():
    """PHẢN CHỨNG AUDIT: tham chiếu `socket.socket` chụp TRƯỚC guard vẫn tạo được socket ở g1."""
    import socket

    cached = socket.socket  # chụp trước - đúng như auditor làm
    with guards.NetworkGuard() as guard:
        try:
            cached()
        except guards.NetworkAccessBlocked:
            pass
        else:
            raise AssertionError("socket constructor cached before the guard still created a socket")
        assert guard.attempts, "guard did not record the cached-constructor attempt"
    probe = cached()
    probe.close()  # sau guard phải dùng lại được, không hỏng vĩnh viễn


@test
def ra01_regression_sec02_guard_declares_what_it_does_not_cover():
    """Claim bị THU HẸP có chủ đích và điều đó phải kiểm được, không chỉ nằm trong docstring."""
    for coverage in (guards.NetworkGuard.COVERAGE, guards.EnvGuard.COVERAGE):
        assert coverage["covered"], coverage
        assert coverage["not_covered"], "a guard that claims to cover everything is lying"
        assert coverage["real_boundary"]
    assert "namespace" in guards.NetworkGuard.COVERAGE["real_boundary"]
    rc, out, _err = _run_cli("coverage")
    assert rc == 0
    assert json.loads(out)["network_guard"]["not_covered"]


@test
def ra01_full_exercise_runs_under_network_guard():
    """Toàn bộ đường nghiệp vụ chạy TRỌN dưới NetworkGuard - không có lối ra mạng nào."""
    with tempfile.TemporaryDirectory() as tmp, guards.NetworkGuard() as guard:
        store = _store(tmp)
        store.call("read_issue", {"repo": REPO, "issue_number": 77})
        store.call("read_diff", {"repo": REPO, "pull_number": 1001})
        store.call(
            "post_heartbeat",
            {"repo": REPO, "issue_number": 77, "reconcile_key": "k1", "payload": {"state": "running"}},
        )
        store.call("run_test", {"repo": REPO, "command": "python3 -m pytest"})
        assert guard.attempts == [], guard.attempts


@test
def ra01_run_test_is_declared_but_not_executed_here():
    """run_test KHÔNG được giả vờ đã chạy - kết quả bịa còn tệ hơn không có kết quả."""
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        result = store.call("run_test", {"repo": REPO, "command": "true"})
        assert result["executed_here"] is False
        assert result["delegated"] is True


# ─────────────────────────────────────────────────────────────────────────────
# C. Idempotence theo reconcile_key
# ─────────────────────────────────────────────────────────────────────────────
@test
def ra01_same_reconcile_key_twice_yields_one_record():
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        call = {
            "repo": REPO,
            "issue_number": 77,
            "reconcile_key": "gh77-heartbeat-g2",
            "payload": {"state": "running"},
        }
        first = store.call("post_heartbeat", dict(call))
        second = store.call("post_heartbeat", dict(call))
        assert first["created"] is True
        assert second["created"] is False, "replay created a SECOND record"
        assert len(store.ledger) == 1, len(store.ledger)


@test
def ra01_different_reconcile_key_yields_two_records():
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        base = {"repo": REPO, "issue_number": 77, "payload": {"state": "running"}}
        store.call("post_heartbeat", dict(base, reconcile_key="k1"))
        store.call("post_heartbeat", dict(base, reconcile_key="k2"))
        assert len(store.ledger) == 2, len(store.ledger)


@test
def ra01_idempotence_is_order_independent():
    """Đảo thứ tự hai lời gọi KHÁC key phải cho CÙNG trạng thái cuối (so bằng state_hash)."""
    a = {"repo": REPO, "issue_number": 77, "reconcile_key": "kA", "payload": {"n": 1}}
    b = {"repo": REPO, "issue_number": 77, "reconcile_key": "kB", "payload": {"n": 2}}
    hashes = []
    for order in ((a, b), (b, a)):
        with tempfile.TemporaryDirectory() as tmp:
            store = _store(tmp)
            for call in order:
                store.call("post_heartbeat", dict(call))
            hashes.append(store.state_hash())
    assert hashes[0] == hashes[1], hashes


@test
def ra01_same_key_different_payload_is_409_conflict():
    """Khử trùng lặp KHÔNG được im lặng nuốt nội dung khác nhau dưới cùng một key."""
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        base = {"repo": REPO, "issue_number": 77, "reconcile_key": "kX"}
        store.call("post_heartbeat", dict(base, payload={"n": 1}))
        try:
            store.call("post_heartbeat", dict(base, payload={"n": 2}))
        except FakeGitHubError as exc:
            assert exc.status == 409, exc.status
        else:
            raise AssertionError("conflicting payload under same key was accepted")
        assert len(store.ledger) == 1


@test
def ra01_ledger_idempotence_survives_process_restart():
    """Idempotence phải bền qua ranh giới tiến trình, không chỉ trong RAM một lượt chạy."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "ledger.json")
        created_first, _ = Ledger(path).record("k", {"v": 1})
        created_again, _ = Ledger(path).record("k", {"v": 1})
        assert created_first is True
        assert created_again is False, "a fresh Ledger re-created an existing key"
        assert len(Ledger(path)) == 1


# ─────────────────────────────────────────────────────────────────────────────
# D. Artifact manifest + locator bền + CONTAINMENT
# ─────────────────────────────────────────────────────────────────────────────
def _reseal(root, manifest):
    """Ghi lại manifest + sidecar khớp nhau - mô phỏng một người niêm phong THÙ ĐỊCH."""
    blob = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    raw = blob.encode("utf-8")
    with open(os.path.join(root, artifacts.MANIFEST_NAME), "wb") as fh:
        fh.write(raw)
    with open(os.path.join(root, artifacts.SIDECAR_NAME), "wb") as fh:
        fh.write((artifacts.sha256_bytes(raw) + "\n").encode("utf-8"))


def _load_manifest(root):
    with open(os.path.join(root, artifacts.MANIFEST_NAME), "r", encoding="utf-8") as fh:
        return json.load(fh)


@test
def ra01_manifest_covers_all_required_categories():
    with tempfile.TemporaryDirectory() as tmp:
        rc, _out, err = _run_cli("produce", "--out", tmp, "--run-id", "r1")
        assert rc == 0, err
        report = artifacts.verify(tmp)
        assert report["ok"] is True, report
        assert report["missing_categories"] == []
        assert report["verified_files"] == 5, report["verified_files"]


@test
def ra01_manifest_is_self_describing_with_sidecar_hash():
    with tempfile.TemporaryDirectory() as tmp:
        _run_cli("produce", "--out", tmp, "--run-id", "r1")
        with open(os.path.join(tmp, artifacts.MANIFEST_NAME), "rb") as fh:
            raw = fh.read()
        manifest = json.loads(raw.decode("utf-8"))
        assert manifest["self"]["locator"] == artifacts.MANIFEST_NAME
        assert manifest["self"]["sha256_recorded_in"] == artifacts.SIDECAR_NAME
        with open(os.path.join(tmp, artifacts.SIDECAR_NAME), "r", encoding="utf-8") as fh:
            assert fh.read().strip() == artifacts.sha256_bytes(raw)
        # Mỗi entry có locator + SHA-256, không entry nào khuyết.
        for entry in manifest["entries"]:
            assert entry["locator"] and re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])


@test
def ra01_verify_goes_red_and_names_the_deleted_artifact():
    with tempfile.TemporaryDirectory() as tmp:
        _run_cli("produce", "--out", tmp, "--run-id", "r1")
        victim = "corpus/cases.json"
        os.remove(os.path.join(tmp, victim))
        report = artifacts.verify(tmp)
        assert report["ok"] is False, "verify stayed green after an artifact was deleted"
        assert victim in report["missing_files"], report["missing_files"]
        rc, _out, err = _run_cli("verify", "--root", tmp)
        assert rc != 0, "verify CLI returned rc=0 with a missing artifact"
        assert victim in err, err


@test
def ra01_verify_goes_red_on_tampered_manifest():
    with tempfile.TemporaryDirectory() as tmp:
        _run_cli("produce", "--out", tmp, "--run-id", "r1")
        path = os.path.join(tmp, artifacts.MANIFEST_NAME)
        with open(path, "r+", encoding="utf-8") as fh:
            data = fh.read().replace('"run_id": "r1"', '"run_id": "r2"')
            fh.seek(0)
            fh.write(data)
            fh.truncate()
        report = artifacts.verify(tmp)
        assert report["manifest_hash_ok"] is False
        assert report["ok"] is False


@test
def ra01_verify_goes_red_on_mutated_artifact_content():
    with tempfile.TemporaryDirectory() as tmp:
        _run_cli("produce", "--out", tmp, "--run-id", "r1")
        victim = "corpus/cases.json"
        with open(os.path.join(tmp, victim), "a", encoding="utf-8") as fh:
            fh.write("tampered\n")
        report = artifacts.verify(tmp)
        assert report["ok"] is False
        assert victim in report["hash_mismatches"], report


@test
def ra01_locator_resolves_after_producing_process_exits():
    """RETENTION: tiến trình sinh artifact đã CHẾT rồi mới verify, từ một tiến trình KHÁC."""
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            [sys.executable, CONTROLLER, "produce", "--out", tmp, "--run-id", "retention"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert proc.returncode == 0, proc.stderr
        # Tiến trình sinh ra đã kết thúc; từ đây không còn gì trong RAM của nó.
        rc, out, _err = _run_cli("verify", "--root", tmp)
        assert rc == 0, out
        assert json.loads(out)["ok"] is True


@test
def ra01_locator_survives_directory_relocation():
    """Locator TƯƠNG ĐỐI: chuyển cả thư mục đi chỗ khác vẫn verify được."""
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "run")
        dst = os.path.join(tmp, "moved")
        _run_cli("produce", "--out", src, "--run-id", "r1")
        shutil.move(src, dst)
        assert artifacts.verify(dst)["ok"] is True


@test
def ra01_finalize_refuses_incomplete_manifest():
    with tempfile.TemporaryDirectory() as tmp:
        aset = artifacts.ArtifactSet(tmp, "partial")
        aset.add("source", "s.txt", "x")
        try:
            aset.finalize()
        except ValueError as exc:
            assert "corpus" in str(exc), str(exc)
        else:
            raise AssertionError("manifest with missing categories was sealed")


@test
def ra01_regression_sec01_escaping_locator_refused_on_write():
    """PHẢN CHỨNG AUDIT: `../escaped.txt` ghi được file NGOÀI run_root ở g1."""
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "run")
        outside = os.path.join(tmp, "escaped.txt")
        aset = artifacts.ArtifactSet(root, "escape")
        try:
            aset.add("source", "../escaped.txt", "PWNED")
        except artifacts.LocatorError as exc:
            assert ".." in exc.reason or "escape" in exc.reason, exc.reason
            assert exc.locator == "../escaped.txt"
        else:
            raise AssertionError("locator escaped run_root on write")
        assert not os.path.exists(outside), "a file was written outside run_root"
        assert aset.entries == [], "an escaping locator was recorded in the manifest"


@test
def ra01_regression_sec01_absolute_and_dot_and_backslash_locators_refused():
    """Ba biến thể còn lại của cùng một lỗ: tuyệt đối, `.`, và dấu gạch ngược."""
    with tempfile.TemporaryDirectory() as tmp:
        aset = artifacts.ArtifactSet(os.path.join(tmp, "run"), "variants")
        for bad in (
            "/etc/passwd",
            "C:\\Windows\\system32\\drivers\\etc\\hosts",
            "\\\\host\\share\\x",
            "./x.txt",
            "a/../../x.txt",
            "sub\\x.txt",
            "",
        ):
            try:
                aset.add("source", bad, "x")
            except artifacts.LocatorError:
                pass
            else:
                raise AssertionError("unsafe locator accepted: %r" % bad)


@test
def ra01_regression_sec01_verify_refuses_escaping_locator_in_hostile_manifest():
    """PHẢN CHỨNG AUDIT, đúng ca đã chạy được: manifest ghi `../escaped.txt` mà verify vẫn ok=true.

    Manifest ở đây do KẺ KHÁC niêm phong và sidecar KHỚP - tức lớp chống sửa đổi không cứu được.
    Chỉ containment ở lúc kiểm mới cứu.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "run")
        _run_cli("produce", "--out", root, "--run-id", "r1")
        outside = os.path.join(tmp, "escaped.txt")
        with open(outside, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("PWNED\n")
        manifest = _load_manifest(root)
        manifest["entries"].append(
            {
                "category": "source",
                "locator": "../escaped.txt",
                "sha256": artifacts.sha256_bytes(b"PWNED\n"),
                "bytes": 6,
            }
        )
        _reseal(root, manifest)
        report = artifacts.verify(root)
        assert report["manifest_hash_ok"] is True, "fixture is wrong - sidecar must still match"
        assert report["ok"] is False, "verify certified an artifact OUTSIDE run_root"
        assert any(r["locator"] == "../escaped.txt" for r in report["rejected_locators"]), report
        rc, _out, err = _run_cli("verify", "--root", root)
        assert rc != 0, "verify CLI returned rc=0 for an escaping locator"
        assert "../escaped.txt" in err, err


@test
def ra01_regression_sec01_verify_refuses_symlink_even_when_content_hash_matches():
    """Hash khớp KHÔNG được chứng nhận nhầm đối tượng: symlink ra ngoài phải bị từ chối."""
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "run")
        _run_cli("produce", "--out", root, "--run-id", "r1")
        victim = os.path.join(root, "corpus", "cases.json")
        with open(victim, "rb") as fh:
            content = fh.read()
        outside = os.path.join(tmp, "outside.json")
        with open(outside, "wb") as fh:
            fh.write(content)  # nội dung y hệt ⇒ SHA-256 vẫn khớp manifest
        os.remove(victim)
        # Fixture THẬT trước. Chỉ đúng một lỗi được phép chuyển sang mô phỏng: Windows
        # ERROR_PRIVILEGE_NOT_HELD (1314) khi tài khoản không có quyền tạo symlink. Mọi lỗi khác
        # vẫn ném - "skip vì lỗi lạ" là cách êm ái nhất để mất một phép thử an ninh.
        simulated = None
        try:
            os.symlink(outside, victim)
            print("     symlink_fixture=real")
        except OSError as exc:
            if getattr(exc, "winerror", None) != 1314:
                raise
            simulated = exc
            shutil.copyfile(outside, victim)
            print("     symlink_fixture=simulated_winerror_1314")
        if simulated is not None:
            with _simulated_symlink(victim):
                _assert_symlink_locator_refused(root)
            return
        _assert_symlink_locator_refused(root)


@contextlib.contextmanager
def _simulated_symlink(victim):
    """Bắt `os.path.islink`/`os.lstat` khai `victim` là symlink, chỉ trong khối này.

    Mô phỏng ở TẦNG hệ thống tệp mà `artifacts` thật sự hỏi, nên nhánh Windows vẫn đi qua đúng
    hai phép kiểm đang được bảo vệ: `islink` trong `safe_locator` và `lstat`+`S_ISREG` trong
    `verify`. Bỏ một trong hai ra khỏi code thì nhánh mô phỏng cũng ĐỎ - đó là điều kiện để mô
    phỏng có giá trị làm bằng chứng.
    """
    target = os.path.abspath(victim)
    real_islink, real_lstat = os.path.islink, os.lstat

    def fake_islink(path):
        return os.path.abspath(path) == target or real_islink(path)

    def fake_lstat(path, *a, **kw):
        result = real_lstat(path, *a, **kw)
        if os.path.abspath(path) == target:
            fields = list(result)
            fields[0] = stat.S_IFLNK | 0o777
            return os.stat_result(tuple(fields))
        return result

    os.path.islink, os.lstat = fake_islink, fake_lstat
    try:
        yield
    finally:
        os.path.islink, os.lstat = real_islink, real_lstat


def _assert_symlink_locator_refused(root):
    report = artifacts.verify(root)
    assert report["ok"] is False, "a symlink out of run_root was certified because its hash matched"
    # Hai lớp cùng bắt được ca này; chấp nhận lớp nào bắt trước, nhưng PHẢI gọi đúng tên locator.
    named = [r["locator"] for r in report["rejected_locators"]] + report["not_regular_files"]
    assert "corpus/cases.json" in named, report
    assert "corpus" in report["missing_categories"], report


@test
def ra01_regression_sec01_verify_refuses_non_regular_file_portable():
    """Bất biến no-follow, kiểm được ở MỌI nền - không cần quyền tạo symlink.

    Đây là đối trọng của test symlink ngay trên: nền nào skip test kia thì vẫn còn test này, nên
    bất biến "verify chỉ chứng nhận TỆP THƯỜNG" không bao giờ đi vắng hoàn toàn. Một skip không có
    đối trọng chính là "xanh vì chẳng chạy gì".
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "run")
        _run_cli("produce", "--out", root, "--run-id", "r1")
        victim = os.path.join(root, "corpus", "cases.json")
        os.remove(victim)
        os.makedirs(victim)  # thư mục không phải tệp thường, và có ở mọi hệ điều hành
        report = artifacts.verify(root)
        assert report["ok"] is False, "a directory standing in for an artifact was certified"
        assert "corpus/cases.json" in report["not_regular_files"], report
        assert "corpus" in report["missing_categories"], report
        rc, _out, err = _run_cli("verify", "--root", root)
        assert rc != 0
        assert "NOT A REGULAR FILE: corpus/cases.json" in err, err


# ─────────────────────────────────────────────────────────────────────────────
# E. Ranh giới của chính packet - ZERO credential, ZERO model call
# ─────────────────────────────────────────────────────────────────────────────
@test
def ra01_env_tripwire_positive_control():
    """ĐỐI CHỨNG DƯƠNG: detector PHẢI bắt được một lần đọc cố ý.

    Không có test này thì "không phát hiện lần đọc nào" có thể chỉ nghĩa là detector đã chết.
    """
    with guards.EnvGuard(inject={"GH_TOKEN": "FAKE-ghp-000000000000000000000000000000000000"}) as rec:
        os.environ.get("GH_TOKEN")
        os.getenv("AWS_SECRET_ACCESS_KEY")
        reads = rec.sensitive_reads()
    assert "GH_TOKEN" in reads, reads
    assert "AWS_SECRET_ACCESS_KEY" in reads, reads


@test
def ra01_core_reads_zero_credentials_with_fakes_injected():
    """Bơm credential GIẢ vào env rồi chạy trọn đường nghiệp vụ - phải KHÔNG có lần đọc nhạy cảm."""
    injected = {
        "GH_TOKEN": "FAKE-ghp-111111111111111111111111111111111111",
        "GITHUB_TOKEN": "FAKE-ghs-222222222222222222222222222222222222",
        "AWS_ACCESS_KEY_ID": "FAKE-AKIA0000000000000000",
        "AWS_SECRET_ACCESS_KEY": "FAKE-secret-0000000000000000000000000000",
    }
    with tempfile.TemporaryDirectory() as tmp:
        with guards.EnvGuard(inject=injected) as recorder, guards.NetworkGuard() as guard:
            store = _store(tmp)
            store.call("read_issue", {"repo": REPO, "issue_number": 77})
            store.call("read_pr", {"repo": REPO, "pull_number": 1001})
            store.call(
                "post_verdict",
                {
                    "repo": REPO,
                    "issue_number": 77,
                    "reconcile_key": "kv",
                    "reviewed_sha": HEAD_OID,
                    "verdict": "approve",
                },
            )
            aset = artifacts.ArtifactSet(os.path.join(tmp, "run"), "r1")
            for category, name in (
                ("source", "s.txt"),
                ("corpus", "c.txt"),
                ("per_case_matrix", "m.txt"),
                ("runner_env_digest", "e.txt"),
                ("cleanup_record", "r.txt"),
            ):
                aset.add(category, name, "x")
            aset.finalize()
            reads = recorder.sensitive_reads()
            attempts = list(guard.attempts)
    assert reads == [], reads
    assert attempts == [], attempts


@test
def ra01_regression_spec02_subprocess_inheriting_environment_is_detected():
    """PHẢN CHỨNG AUDIT: child với `env=None` đọc được GH_TOKEN mà `sensitive_reads()` vẫn rỗng.

    Đòi HAI điều, vì phát hiện mà không chặn thì credential vẫn đã ra khỏi tiến trình:
      1. recorder PHẢI thấy lần phơi nhiễm;
      2. child PHẢI không nhận được giá trị.
    """
    marker = "FAKE-AUDIT-CHILD-READ"
    reader = "import os,sys; sys.stdout.write('CHILD:' + (os.environ.get('GH_TOKEN') or 'ABSENT'))"
    with guards.EnvGuard(inject={"GH_TOKEN": marker}) as recorder:
        proc = subprocess.run(
            [sys.executable, "-c", reader], capture_output=True, text=True, timeout=120
        )
        exposures = [e["name"] for e in recorder.child_env_exposures]
        reads = recorder.sensitive_reads()
    assert proc.returncode == 0, proc.stderr
    assert "GH_TOKEN" in exposures, exposures
    assert "GH_TOKEN" in reads, reads
    assert marker not in proc.stdout, "credential reached the child process"
    assert proc.stdout.strip() == "CHILD:ABSENT", proc.stdout


@test
def ra01_regression_spec02_explicit_child_env_is_scrubbed_too():
    """`env=` tường minh cũng phải bị lọc - không chỉ đường kế thừa."""
    marker = "FAKE-EXPLICIT-CHILD-ENV"
    reader = "import os,sys; sys.stdout.write(os.environ.get('AWS_SECRET_ACCESS_KEY') or 'ABSENT')"
    # env tường minh phải dựng từ environment THẬT của nền: hằng "/usr/bin:/bin" làm child chết
    # trên Windows (thiếu SYSTEMROOT/PATH hợp lệ) - hỏng vì fixture, không vì bất biến.
    hostile_env = _portable_child_env({"AWS_SECRET_ACCESS_KEY": marker})
    with guards.EnvGuard() as recorder:
        proc = subprocess.run(
            [sys.executable, "-c", reader],
            capture_output=True,
            text=True,
            timeout=120,
            env=hostile_env,
        )
        exposures = [e["name"] for e in recorder.child_env_exposures]
    assert proc.stdout.strip() == "ABSENT", proc.stdout
    assert "AWS_SECRET_ACCESS_KEY" in exposures, exposures


@test
def ra01_regression_spec02_suite_never_reads_protected_vars_outside_a_guard():
    """PHẢN CHỨNG AUDIT: `selftest.py:509` tự đọc biến cần bảo vệ TRƯỚC khi cài guard ở `:513`."""
    offenders = _scan_unguarded_env_access(os.path.join(_HERE, "selftest.py"))
    assert not offenders, offenders
    for module in ("controller.py", "operations.py", "fake_github.py", "artifacts.py", "ledger.py"):
        assert not _scan_unguarded_env_access(os.path.join(_HERE, module)), module


@test
def ra01_regression_spec02_unguarded_env_scanner_has_teeth():
    """ĐỐI CHỨNG DƯƠNG cho bộ quét trên - nó PHẢI bắt được một lần đọc ngoài guard."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "leaky_suite.py")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(
                "import os\n"
                "from core import guards\n"
                "saved = os.environ.get('GH_TOKEN')\n"
                "with guards.EnvGuard() as rec:\n"
                "    os.environ.get('GH_TOKEN')\n"
            )
        offenders = _scan_unguarded_env_access(path)
        assert len(offenders) == 1, offenders
        assert offenders[0][0] == 3, offenders  # dòng NGOÀI guard, không phải dòng trong guard


@test
def ra01_no_artifact_contains_injected_credential_value():
    """Artifact phải không rò credential ra đĩa, kể cả khi env đang có biến giả."""
    marker = "FAKE-ghp-333333333333333333333333333333333333"
    with tempfile.TemporaryDirectory() as tmp:
        with guards.EnvGuard(inject={"GH_TOKEN": marker}) as recorder:
            rc, _out, err = _run_cli("produce", "--out", tmp, "--run-id", "r1")
            exposures = [e["name"] for e in recorder.child_env_exposures]
        assert rc == 0, err
        # Bằng chứng dương là guard ĐÃ nhìn thấy tiến trình con - nếu không, phép thử này chỉ đang
        # kiểm một đường mà tripwire không phủ, và "sạch" lại vô nghĩa.
        assert "GH_TOKEN" in exposures, exposures
        for dirpath, _dirs, files in os.walk(tmp):
            for name in files:
                with open(os.path.join(dirpath, name), "rb") as fh:
                    assert marker.encode() not in fh.read(), os.path.join(dirpath, name)


@test
def ra01_core_modules_import_no_network_or_provider_library():
    """Kiểm kê BẰNG MÁY: không module lõi nào import đường mạng hay SDK provider.

    Dùng `ast` chứ KHÔNG dùng regex: một dòng văn xuôi trong docstring có thể ngắt dòng đúng chỗ
    thành `    import socket/http/urllib` và làm regex báo dương tính giả. `ast` chỉ thấy import
    THẬT, nên phép kiểm nói đúng thứ nó tuyên bố kiểm.

    Hai ngoại lệ có chủ đích, cả hai đều import `socket` để CHẶN hoặc để CHỨNG MINH chặn:
      guards.py   - vá socket thành tripwire
      selftest.py - đối chứng dương, thử mở socket và đòi bị từ chối đích danh
    """
    offenders = _scan_forbidden_imports(
        _HERE, allowed={("guards.py", "socket"), ("selftest.py", "socket")}
    )
    assert not offenders, offenders


@test
def ra01_import_scanner_has_teeth():
    """ĐỐI CHỨNG DƯƠNG cho phép kiểm ở trên: nó PHẢI bắt được một import bị cấm."""
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "leaky.py"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("import requests\nfrom urllib.request import urlopen\n")
        with open(os.path.join(tmp, "prose.py"), "w", encoding="utf-8", newline="\n") as fh:
            # Bẫy dương tính giả mà regex sẽ dính, ast thì không.
            fh.write('"""docstring nói rằng module này KHÔNG\nimport socket/http/urllib.\n"""\n')
        offenders = _scan_forbidden_imports(tmp, allowed=set())
        assert ("leaky.py", "requests") in offenders, offenders
        assert ("leaky.py", "urllib") in offenders, offenders
        assert not any(name == "prose.py" for name, _ in offenders), offenders


@test
def ra01_regression_sec02_escape_scanner_catches_importlib_and_subprocess():
    """PHẢN CHỨNG AUDIT: fixture dùng `importlib.import_module` + `subprocess.run(["gh", ...])`
    cho `offenders=[]` ở g1, vì scanner chỉ thấy `Import`/`ImportFrom`."""
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "sneaky.py"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(
                "import importlib\n"
                "import subprocess\n"
                "import os\n"
                "def go():\n"
                "    importlib.import_module('requests')\n"
                "    subprocess.run(['gh', 'api', '/user'])\n"
                "    os.system('curl https://example.invalid')\n"
            )
        offenders = _scan_escape_paths(tmp, allowed=set())
        assert ("sneaky.py", "dynamic-import:requests") in offenders, offenders
        assert ("sneaky.py", "subprocess:gh") in offenders, offenders
        assert ("sneaky.py", "shell:os.system") in offenders, offenders
    # Bộ quét cũ (chỉ AST Import) đúng là MÙ với fixture này - ghi lại để thấy phần mở rộng có việc.
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "sneaky.py"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("import importlib\ndef go():\n    importlib.import_module('requests')\n")
        assert _scan_forbidden_imports(tmp, allowed=set()) == []


@test
def ra01_regression_sec02_core_has_no_dynamic_escape_path():
    """Lõi thật phải sạch dưới bộ quét MỞ RỘNG, không chỉ dưới bộ quét cũ."""
    assert _scan_escape_paths(_HERE, allowed=set()) == []
    assert _ESCAPE_SCANNER_LIMITS, "a static scanner that claims no limits is lying"


@test
def ra01_operations_expose_no_credential_parameter():
    """Không op nào có TÊN THAM SỐ top-level trông như credential."""
    suspicious = re.compile(r"token|secret|password|credential|auth", re.I)
    for name, spec in operations.OPERATIONS.items():
        for param in spec["params"]:
            assert not suspicious.search(param), (name, param)


@test
def ra01_regression_sec03_credential_inside_payload_is_refused_by_name():
    """PHẢN CHỨNG AUDIT: `payload={"token": FAKE-PAYLOAD-SECRET}` ĐI ĐƯỢC vào ledger ở g1.

    Chọn đường (b) của verdict - RÀNG BUỘC payload - chứ không phải (a) thu hẹp claim. Lý do:
    `payload` là object tuỳ ý được PERSIST vào sổ bền, nên nó là bề mặt credential thật, không
    phải hiểu lầm về câu chữ. Thu hẹp claim sẽ để nguyên bề mặt và chỉ sửa lời mô tả.
    Từ chối (chứ không scrub) để người gọi biết mình vừa suýt ghi credential - scrub im lặng
    chính là lớp lỗi "nuốt mất nội dung" mà 409 CONFLICT ở chỗ khác đang chặn.
    """
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        try:
            store.call(
                "post_heartbeat",
                {
                    "repo": REPO,
                    "issue_number": 77,
                    "reconcile_key": "k-cred",
                    "payload": {"token": "FAKE-PAYLOAD-SECRET"},
                },
            )
        except operations.CredentialSurfaceError as exc:
            assert exc.param == "payload"
            assert "token" in str(exc), str(exc)
        else:
            raise AssertionError("credential in payload was accepted")
        assert len(store.ledger) == 0, "a rejected payload still reached the ledger"
        assert store.calls == [], store.calls


@test
def ra01_regression_sec03_nested_and_value_shaped_credentials_refused():
    """Khoá lồng sâu và GIÁ TRỊ hình dạng credential dưới khoá vô hại - cả hai đều bị bắt."""
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        for payload in (
            {"meta": {"auth": {"api_key": "x"}}},
            {"note": "ghp_0123456789abcdefghij0123456789abcdef"},
            {"list": [{"aws_secret_access_key": "x"}]},
            {"blob": "-----BEGIN RSA PRIVATE KEY-----"},
        ):
            try:
                store.call(
                    "post_heartbeat",
                    {"repo": REPO, "issue_number": 77, "reconcile_key": "k", "payload": payload},
                )
            except operations.CredentialSurfaceError:
                pass
            else:
                raise AssertionError("credential surface accepted: %r" % payload)
        assert len(store.ledger) == 0


@test
def ra01_regression_sec03_benign_payload_still_accepted():
    """Ràng buộc phải HẸP: một payload bình thường vẫn phải đi lọt, nếu không nó vô dụng."""
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        result = store.call(
            "post_heartbeat",
            {
                "repo": REPO,
                "issue_number": 77,
                "reconcile_key": "k-ok",
                "payload": {"state": "running", "generation": 2, "notes": ["heartbeat", "g2"]},
            },
        )
        assert result["created"] is True
        assert len(store.ledger) == 1


@test
def ra01_regression_sec03_cli_refuses_credential_payload_with_rc_and_name():
    with tempfile.TemporaryDirectory() as tmp:
        params = json.dumps(
            {
                "repo": REPO,
                "issue_number": 77,
                "reconcile_key": "k-cli",
                "payload": {"token": "FAKE-PAYLOAD-SECRET"},
            }
        )
        ledger = os.path.join(tmp, "ledger.json")
        rc, _out, err = _run_cli("call", "--op", "post_heartbeat", "--params", params, "--ledger", ledger)
        assert rc == 2, rc
        assert "token" in err and "payload" in err, err
        assert not os.path.exists(ledger), "ledger was created for a rejected call"


@test
def ra01_seed_fixture_has_exactly_one_definition():
    """dup-01: seed store chỉ được định nghĩa MỘT chỗ; hai bản trôi lệch là cách hỏng êm ái nhất."""
    # Kim tìm được GHÉP LÚC CHẠY: viết thẳng chuỗi ra đây thì chính tệp này chứa nó và test tự
    # bắt lấy mình - đúng lớp lỗi tự tham chiếu mà bộ quét import đã phải tránh bằng ast.
    needle = "def " + "_seed_store"
    for module in ("controller.py", "selftest.py"):
        with open(os.path.join(_HERE, module), "r", encoding="utf-8") as fh:
            source = fh.read()
        assert needle not in source, module
        assert "seeded_store" in source, module
    from core import fake_github

    assert callable(fake_github.seeded_store)


# ─────────────────────────────────────────────────────────────────────────────
# F. Vòng audit thứ hai — sáu finding độc lập trên head dc0dbf42
# ─────────────────────────────────────────────────────────────────────────────
@test
def ra01_regression_a2_01_manifest_cannot_narrow_its_own_obligations():
    """PHẢN CHỨNG AUDIT: manifest reseal với entries=[] và required_categories=[] vẫn ok=true.

    Gốc lỗi là một câu hỏi sai: verify() hỏi CHÍNH tài liệu đang bị kiểm xem nó có nghĩa vụ gì.
    Sidecar chỉ chứng minh tài liệu không đổi kể từ lúc niêm phong - nó không cấp thẩm quyền cho
    nội dung bên trong.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "run")
        _run_cli("produce", "--out", root, "--run-id", "r1")
        manifest = _load_manifest(root)
        manifest["entries"] = []
        manifest["required_categories"] = []
        _reseal(root, manifest)
        report = artifacts.verify(root)
        assert report["manifest_hash_ok"] is True, "fixture sai - sidecar phải vẫn khớp"
        assert report["ok"] is False, "an EMPTY manifest was certified"
        assert report["verified_files"] == 0
        assert report["manifest_invalid"], report
        rc, _out, err = _run_cli("verify", "--root", root)
        assert rc != 0, "verify CLI returned rc=0 for an empty manifest"
        assert "MANIFEST INVALID" in err, err


@test
def ra01_regression_a2_01_manifest_dropping_one_category_is_refused():
    """Biến thể tinh vi hơn: giữ 4 hạng mục, bỏ 1, và sửa required_categories cho khớp."""
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "run")
        _run_cli("produce", "--out", root, "--run-id", "r1")
        manifest = _load_manifest(root)
        manifest["entries"] = [e for e in manifest["entries"] if e["category"] != "cleanup_record"]
        manifest["required_categories"] = [c for c in artifacts.REQUIRED_CATEGORIES
                                           if c != "cleanup_record"]
        _reseal(root, manifest)
        report = artifacts.verify(root)
        assert report["ok"] is False, "manifest dropped an obligation and was still certified"
        assert report["manifest_invalid"], report


@test
def ra01_regression_a2_02_ntfs_stream_and_dos_device_locators_refused():
    """PHẢN CHỨNG AUDIT: `carrier.txt:payload` (NTFS ADS) và `NUL`/`CON` được chấp nhận ở bản trước.

    Cả hai đều làm manifest chứng nhận một thứ KHÔNG phải tệp trong thư mục: ADS giấu dữ liệu
    trong stream của tệp khác, còn `NUL` nuốt mọi ghi và trả rỗng mọi đọc.
    """
    with tempfile.TemporaryDirectory() as tmp:
        aset = artifacts.ArtifactSet(os.path.join(tmp, "run"), "devices")
        for bad in (
            "carrier.txt:payload",
            "sub/carrier.txt:payload",
            "NUL", "CON", "PRN", "AUX", "COM1", "LPT9",
            "nul.txt", "con.log", "COM1.json",
            "NUL.", "CON ",
            "trailing.",
            "trailing ",
        ):
            try:
                aset.add("source", bad, "x")
            except artifacts.LocatorError:
                pass
            else:
                raise AssertionError("unsafe Windows locator accepted: %r" % bad)
        # Tên bình thường có chứa chuỗi thiết bị vẫn phải đi lọt - ràng buộc không được quá tay.
        for good in ("console.txt", "nullable.json", "aux_data/notes.txt", "com10.txt"):
            aset.add("source", good, "x")


@test
def ra01_regression_a2_01_malformed_entry_fields_are_refused():
    """Kiểu của TỪNG trường trong entry cũng là đầu vào không tin cậy.

    Mutation audit tìm ra chỗ này: bỏ kiểm `sha256`/`bytes` mà không test nào đỏ. Một entry với
    `sha256: null` sẽ không bao giờ khớp và chỉ hiện ra dưới dạng hash_mismatch mơ hồ, còn
    `bytes: "lots"` thì đi thẳng vào báo cáo mà không ai chặn.
    """
    for field, value in (
        ("sha256", None), ("sha256", "nothex"), ("sha256", "ab" * 32 + "zz"),
        # Cùng lớp lỗi với reviewed_sha: `$` khớp cả trước newline cuối chuỗi, nên một sha kèm
        # xuống dòng phải bị bắt là MANIFEST HỎNG, không phải trôi xuống thành hash_mismatch mơ hồ.
        ("sha256", "a" * 64 + "\n"), ("sha256", " " + "a" * 64),
        ("bytes", "lots"), ("bytes", -1), ("bytes", True),
        ("locator", 42), ("locator", None),
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "run")
            _run_cli("produce", "--out", root, "--run-id", "r1")
            manifest = _load_manifest(root)
            manifest["entries"][0][field] = value
            _reseal(root, manifest)
            report = artifacts.verify(root)
            assert report["ok"] is False, (field, value, report)
            assert report["manifest_invalid"], (field, value, report)
            assert report["missing_categories"] == list(artifacts.REQUIRED_CATEGORIES), report


@test
def ra01_regression_a2_02_add_refuses_a_target_that_is_not_a_regular_file():
    """`os.open` thành công KHÔNG có nghĩa ta đang giữ một tệp thường.

    Trên Windows `NUL` mở được và nuốt mọi thứ, và ở đó không có `O_NOFOLLOW`. POSIX không dựng
    được ca đó bằng tệp thật, nên hệ điều hành được mô phỏng ở ĐÚNG một điểm - `os.fstat` - còn
    logic đang bị kiểm thì vẫn là logic thật. Cùng nguyên tắc với nhánh symlink mô phỏng.
    """
    with tempfile.TemporaryDirectory() as tmp:
        aset = artifacts.ArtifactSet(os.path.join(tmp, "run"), "fstat")
        real_fstat = os.fstat

        def fake_fstat(fd, *a, **kw):
            result = real_fstat(fd, *a, **kw)
            fields = list(result)
            fields[0] = stat.S_IFCHR | 0o666  # thiết bị ký tự, giống NUL
            return os.stat_result(tuple(fields))

        os.fstat = fake_fstat
        try:
            aset.add("source", "looks_ordinary.txt", "x")
        except artifacts.LocatorError as exc:
            assert "regular file" in exc.reason, exc.reason
        else:
            raise AssertionError("add() accepted a non-regular-file target")
        finally:
            os.fstat = real_fstat
        assert aset.entries == [], "a refused target was still recorded in the manifest"


@test
def ra01_regression_a2_02_hostile_manifest_with_stream_or_device_locator_is_refused():
    """Chặn ở CẢ HAI đầu: manifest thù địch khai locator ADS/device cũng phải verify ĐỎ đích danh.

    Chặn lúc ghi là chưa đủ - manifest có thể do người khác soạn, và sidecar vẫn khớp.
    """
    for hostile in ("carrier.txt:payload", "NUL", "com1.json"):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "run")
            _run_cli("produce", "--out", root, "--run-id", "r1")
            manifest = _load_manifest(root)
            manifest["entries"].append(
                {
                    "category": "source",
                    "locator": hostile,
                    "sha256": artifacts.sha256_bytes(b"x"),
                    "bytes": 1,
                }
            )
            _reseal(root, manifest)
            report = artifacts.verify(root)
            assert report["manifest_hash_ok"] is True, "fixture sai - sidecar phải vẫn khớp"
            assert report["ok"] is False, "hostile locator certified: %r" % hostile
            assert any(r["locator"] == hostile for r in report["rejected_locators"]), (hostile, report)
            rc, _out, err = _run_cli("verify", "--root", root)
            assert rc != 0 and hostile in err, (rc, err)


@test
def ra01_regression_a2_03_child_process_credential_read_is_detected_with_marker_present():
    """PHẢN CHỨNG AUDIT: test ZERO-credential trước đây FALSE-GREEN.

    Guard scrub marker TRƯỚC khi child chạy, nên child không bao giờ có gì để đọc - và một mutant
    cho `cmd_produce` đọc `os.getenv("GH_" + "TOKEN")` vẫn xanh toàn suite.

    Ở đây marker VẪN HIỆN DIỆN trong env của child, và recorder được cài TRONG child trước khi
    import controller. Phát hiện vì thế không còn ăn theo scrub.
    """
    marker = "FAKE-ghp-444444444444444444444444444444444444"
    with tempfile.TemporaryDirectory() as tmp:
        probe = os.path.join(tmp, "probe.py")
        out_json = os.path.join(tmp, "reads.json")
        run_dir = os.path.join(tmp, "run")
        with open(probe, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(
                "import json, os, sys\n"
                "sys.path.insert(0, %r)\n" % _PARENT
                + "from core import guards\n"
                "rec = guards.EnvAccessRecorder(os.environ)\n"
                "os.environ = rec\n"
                "from core import controller\n"  # import SAU khi recorder đã tại chỗ
                "rc = controller.main(['produce', '--out', %r, '--run-id', 'probe'])\n" % run_dir
                + "json.dump({'rc': rc, 'sensitive_reads': rec.sensitive_reads(),\n"
                "           'marker_present': os.environ.get('GH_TOKEN') is not None},\n"
                "          open(%r, 'w', encoding='utf-8'))\n" % out_json
            )
        env = _portable_child_env({"GH_TOKEN": marker})
        proc = subprocess.run(
            [sys.executable, probe], capture_output=True, text=True, timeout=120, env=env
        )
        assert proc.returncode == 0, proc.stderr
        with open(out_json, "r", encoding="utf-8") as fh:
            result = json.load(fh)
        assert result["rc"] == 0, result
        # Bằng chứng dương là fixture CÓ răng: marker thật sự nằm trong env của child.
        assert result["marker_present"] is True, "marker never reached the child - test is vacuous"
        assert result["sensitive_reads"] == [], result["sensitive_reads"]
        for dirpath, _dirs, files in os.walk(run_dir):
            for name in files:
                with open(os.path.join(dirpath, name), "rb") as fh:
                    assert marker.encode() not in fh.read(), name


@test
def ra01_regression_a2_03_detection_works_without_scrubbing():
    """Tách PHÁT HIỆN khỏi SCRUB: tắt scrub thì child NHẬN được biến, mà recorder vẫn ghi nhận."""
    marker = "FAKE-NO-SCRUB-CHILD"
    reader = "import os,sys; sys.stdout.write(os.environ.get('GH_TOKEN') or 'ABSENT')"
    with guards.EnvGuard(inject={"GH_TOKEN": marker}, scrub_child_env=False) as recorder:
        proc = subprocess.run(
            [sys.executable, "-c", reader], capture_output=True, text=True, timeout=120
        )
        exposures = [e["name"] for e in recorder.child_env_exposures]
    assert proc.stdout.strip() == marker, "scrub_child_env=False must not alter the child env"
    assert "GH_TOKEN" in exposures, exposures


@test
def ra01_regression_a2_07_positional_child_env_is_covered_too():
    """`env` truyền bằng VỊ TRÍ (tham số thứ 11 của Popen) phải đi qua cùng một đường.

    Chỉ đọc `kwargs["env"]` là bỏ lọt một chữ ký hợp lệ của stdlib - và kẻ bỏ lọt nó sẽ không
    biết mình đã bỏ lọt, vì `subprocess.run` luôn dùng keyword.
    """
    marker = "FAKE-POSITIONAL-CHILD-ENV"
    reader = "import os,sys; sys.stdout.write(os.environ.get('GITHUB_TOKEN') or 'ABSENT')"
    hostile_env = _portable_child_env({"GITHUB_TOKEN": marker})
    with guards.EnvGuard() as recorder:
        # Popen(args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell,
        #       cwd, env) - đếm đủ chín tham số đệm để `env` rơi đúng vị trí thứ 11.
        proc = subprocess.Popen(
            [sys.executable, "-c", reader],
            -1, None, None, subprocess.PIPE, None, None, True, False, None, hostile_env,
        )
        out, _err = proc.communicate(timeout=120)
        exposures = [e["name"] for e in recorder.child_env_exposures]
    assert out.decode().strip() == "ABSENT", out
    assert "GITHUB_TOKEN" in exposures, exposures


@test
def ra01_regression_a2_04_escape_scanner_canonicalizes_import_aliases():
    """PHẢN CHỨNG AUDIT: `import subprocess as sp` / `import importlib as il` cho offenders=[]."""
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "aliased.py"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(
                "import subprocess as sp\n"
                "import importlib as il\n"
                "import os as o\n"
                "from subprocess import run as r\n"
                "from importlib import import_module as im\n"
                "def go():\n"
                "    sp.run(['gh', 'api', '/user'])\n"
                "    il.import_module('requests')\n"
                "    o.system('curl https://example.invalid')\n"
                "    r(['curl', '-s', 'https://example.invalid'])\n"
                "    im('httpx')\n"
            )
        offenders = set(_scan_escape_paths(tmp, allowed=set()))
        for expected in (
            ("aliased.py", "subprocess:gh"),
            ("aliased.py", "dynamic-import:requests"),
            ("aliased.py", "shell:os.system"),
            ("aliased.py", "subprocess:curl"),
            ("aliased.py", "dynamic-import:httpx"),
        ):
            assert expected in offenders, (expected, sorted(offenders))


@test
def ra01_regression_a2_05_benign_payload_keys_are_not_blocked():
    """PHẢN CHỨNG AUDIT: regex substring chặn nhầm dữ liệu hợp lệ của chính protocol này.

    Fixture là payload THẬT theo hình dạng RA-02/RA-03 sẽ gửi, không phải ví dụ bịa - một bộ lọc
    an ninh chặn nhầm dữ liệu thật sẽ bị gỡ ra, và lúc đó nó không bảo vệ gì nữa.
    """
    benign = {
        "session_id": "codex-audit-wp77-g2-20260810",
        "authorization_url": "https://github.com/ducthangho/tra-luat/issues/76#issuecomment-1",
        "token_budget": 120000,
        "author": "ducthangho",
        "cookie_policy": "none",
        "public_key": "ssh-ed25519 AAAA...",
        "reconcile_key": "gh77-heartbeat-g2-claude-01",
        "sort_key": "created_at",
        "auth_method": "oidc",
        "nested": {"idempotency_key": "abc", "tokens_used": 41, "authorization_url": "https://x"},
    }
    # Payload THẬT theo hình dạng RA-03 sẽ gửi - lấy nguyên các trường của heartbeat và verdict
    # đang dùng trên chính #77, chứ không phải {"state": "running"} cho dễ.
    real_heartbeat = {
        "schema_version": 1, "event": "executor_heartbeat",
        "reconcile_key": "gh77-heartbeat-g2-claude-01", "packet_id": "wp77",
        "mission_issue": 76, "generation": 2, "attempt": 2, "max_attempts_per_packet": 2,
        "spec_hash": "890c5a1b071f79985c43db560897d6624934735072380c54af8103c2363cf02b",
        "session_id": "session-abc", "role": "executor", "provider": "claude",
        "branch": "agent/wp77-g2-claude", "base_sha": HEAD_OID,
        "heartbeat_at": "2026-08-10T06:30:00Z", "lease_until": "2026-08-10T07:43:09Z",
        "authorization_url": "https://github.com/ducthangho/tra-luat/issues/77#issuecomment-1",
        "token_budget": 120000, "author": "ducthangho",
    }
    real_verdict = {
        "schema_version": 1, "event": "reviewer_verdict", "review_axes": ["spec", "standards_security"],
        "independent_from_executor_session": True, "assurance": "cross_approved",
        "session_id": "codex-audit-wp77-g2-20260810", "author": "codex",
        "findings": [{"id": "wp77-g1-sec-01", "severity": "P1", "title": "artifact locator escape"}],
        "cookie_policy": "none", "sort_key": "created_at",
    }
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        result = store.call(
            "post_heartbeat",
            {"repo": REPO, "issue_number": 77, "reconcile_key": "k-benign", "payload": benign},
        )
        assert result["created"] is True
        store.call(
            "post_heartbeat",
            {"repo": REPO, "issue_number": 77, "reconcile_key": "k-real-hb", "payload": real_heartbeat},
        )
        store.call(
            "post_verdict",
            {"repo": REPO, "issue_number": 77, "reconcile_key": "k-real-vd",
             "reviewed_sha": HEAD_OID, "verdict": "changes_requested", "payload": real_verdict},
        )
        assert len(store.ledger) == 3, len(store.ledger)
    # Ràng buộc phải được CÔNG BỐ, không chôn trong regex.
    surface = operations.schema()["credential_surface"]
    assert surface["secret_nouns"] and surface["max_depth"] and surface["max_nodes"]
    assert surface["carrier_words_that_force_rejection"], surface
    assert surface["measure_words_that_neutralise_token"], surface


@test
def ra01_regression_a2_05_secret_keys_still_refused_by_name():
    """Đối trọng của test trên: thu hẹp bộ lọc KHÔNG được làm nó ngừng bắt credential thật."""
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        for key in (
            "token", "access_token", "refresh_token", "apiKey", "X-Api-Key", "client_secret",
            "password", "passwd", "credentials", "basic_auth", "authorization", "set-cookie",
            "aws_secret_access_key", "private_key", "session_key", "passphrase",
        ):
            try:
                store.call(
                    "post_heartbeat",
                    {"repo": REPO, "issue_number": 77, "reconcile_key": "k",
                     "payload": {key: "value"}},
                )
            except operations.CredentialSurfaceError as exc:
                assert key in str(exc), (key, str(exc))
            else:
                raise AssertionError("credential key accepted: %r" % key)
        assert len(store.ledger) == 0


@test
def ra01_regression_a2_06_post_verdict_requires_a_full_git_oid():
    """PHẢN CHỨNG AUDIT: `reviewed_sha` chỉ kiểm là `string`; "not-a-sha" và `ghp_…` được PERSIST.

    Verdict neo vào một thứ không phải commit thì nó không neo vào đâu - §1 bất biến 9 đòi exact
    SHA, và SHA viết tắt cũng KHÔNG exact.
    """
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        base = {"repo": REPO, "issue_number": 77, "verdict": "approve"}
        for bad in (
            "not-a-sha",
            "ghp_0123456789abcdefghij0123456789abcdef",
            "b044f8b1",                                     # viết tắt
            HEAD_OID[:-1],                                  # thiếu 1 ký tự
            HEAD_OID + "a",                                 # thừa 1 ký tự
            HEAD_OID.upper(),                               # hoa - không canonical
            "g" * 40,                                       # đủ dài, không phải hex
            "",
        ):
            try:
                store.call("post_verdict", dict(base, reconcile_key="k", reviewed_sha=bad))
            except operations.ParameterError as exc:
                assert "reviewed_sha" in str(exc), str(exc)
            else:
                raise AssertionError("post_verdict accepted a non-OID reviewed_sha: %r" % bad)
        assert len(store.ledger) == 0, "a rejected verdict still reached the ledger"
        ok = store.call("post_verdict", dict(base, reconcile_key="k-ok", reviewed_sha=HEAD_OID))
        assert ok["created"] is True
        assert len(store.ledger) == 1
    assert operations.schema()["formats"]["git_oid"]


@test
def ra01_regression_a2_06_environ_copy_still_works_under_the_guard():
    """PHẢN CHỨNG AUDIT: `os.environ.copy()` ném AttributeError khi recorder đang thay chỗ.

    Thư viện con thường gọi đúng thứ đó ngay trước khi tạo subprocess. Một guard làm hỏng code
    lành là guard sẽ bị gỡ ra - và lúc đó nó không canh gì nữa.
    """
    marker = "FAKE-COPY-PROBE-TOKEN"
    with guards.EnvGuard(inject={"GH_TOKEN": marker}) as recorder:
        snapshot = os.environ.copy()
        assert isinstance(snapshot, dict)
        assert snapshot.get("GH_TOKEN") == marker
        # Sao chép toàn bộ environment LÀ một lần đọc credential, và phải được ghi nhận.
        assert "GH_TOKEN" in recorder.sensitive_reads()
        assert len(os.environ) == len(snapshot)


# ─────────────────────────────────────────────────────────────────────────────
# G. Vòng audit thứ ba — năm finding spec trên head c4784728
# ─────────────────────────────────────────────────────────────────────────────
@test
def ra01_regression_a3_01_carrier_keys_refused_and_measure_keys_accepted():
    """PHẢN CHỨNG AUDIT: bộ lọc "từ cuối" hỏng theo CẢ HAI hướng cùng lúc.

    Lọt: `authorization_header`, `client_secret_value` được persist.
    Chặn nhầm: `requested_tokens`, `remaining_tokens` (con số) bị từ chối.
    Sửa false-positive bằng cách nới từ cuối thì tự tay mở lại false-negative, nên test này đòi
    CẢ HAI chiều trong cùng một phép chạy.
    """
    must_refuse = {
        "authorization_header": "Bearer opaque",
        "client_secret_value": "opaque",
        "auth_header": "opaque",
        "token_value": "opaque",
        "credential_blob": "opaque",
        "password_field": "opaque",
        "secret_material": "opaque",
        "api_key_string": "opaque",
        # Vật chứa + đơn vị đo trong CÙNG một khoá: đây là ca duy nhất mà danh sách vật chứa thật
        # sự gánh việc. Thiếu nó thì "đơn vị đo trung hoà token" sẽ nuốt luôn cả header thật.
        "remaining_tokens_header": "Bearer opaque",
        "token_budget_value": "opaque",
    }
    must_accept = {
        "requested_tokens": 4096,
        "remaining_tokens": 120,
        "total_tokens": 8192,
        "prompt_tokens": 12,
        "completion_tokens": 34,
        "tokens_used": 46,
        "token_budget": 120000,
        "authorization_url": "https://github.com/ducthangho/tra-luat/issues/77",
        "auth_method": "oidc",
        "cookie_policy": "none",
        "author": "ducthangho",
        "session_id": "abc",
        "public_key": "ssh-ed25519 AAAA",
        "reconcile_key": "gh77-x",
        "credential_count": 0,
        "secret_scan_status": "clean",
    }
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        for key, value in must_refuse.items():
            try:
                store.call(
                    "post_heartbeat",
                    {"repo": REPO, "issue_number": 77, "reconcile_key": "k",
                     "payload": {key: value}},
                )
            except operations.CredentialSurfaceError as exc:
                assert key in str(exc), (key, str(exc))
            else:
                raise AssertionError("credential carrier accepted: %r" % key)
        assert len(store.ledger) == 0, "a refused payload reached the ledger"
        result = store.call(
            "post_heartbeat",
            {"repo": REPO, "issue_number": 77, "reconcile_key": "k-measures",
             "payload": must_accept},
        )
        assert result["created"] is True
        assert len(store.ledger) == 1


@test
def ra01_regression_a3_01_authorization_scheme_in_a_value_is_refused():
    """Giá trị mang lược đồ Authorization bị bắt kể cả dưới khoá hoàn toàn vô hại."""
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        for payload in ({"note": "Bearer sk-live-0123456789"}, {"note": "Basic YWxhZGRpbjpvcGVu"}):
            try:
                store.call(
                    "post_heartbeat",
                    {"repo": REPO, "issue_number": 77, "reconcile_key": "k", "payload": payload},
                )
            except operations.CredentialSurfaceError:
                pass
            else:
                raise AssertionError("authorization scheme accepted in a value: %r" % payload)
        assert len(store.ledger) == 0


@test
def ra01_regression_a3_02_git_oid_rejects_trailing_newline():
    """PHẢN CHỨNG AUDIT: `^...$` + `.match()` nhận `40hex + newline`, và nó được PERSIST.

    Trong Python `$` khớp cả TRƯỚC một newline cuối chuỗi. Schema công bố "full lowercase 40-hex",
    nên nhận thêm ký tự xuống dòng là schema nói một đằng, code làm một nẻo.
    """
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        base = {"repo": REPO, "issue_number": 77, "verdict": "approve"}
        for bad in (HEAD_OID + "\n", HEAD_OID + "\r\n", HEAD_OID + " ", "\n" + HEAD_OID,
                    HEAD_OID + "\n" + HEAD_OID):
            try:
                store.call("post_verdict", dict(base, reconcile_key="k", reviewed_sha=bad))
            except operations.ParameterError as exc:
                assert "reviewed_sha" in str(exc), str(exc)
            else:
                raise AssertionError("reviewed_sha accepted with stray whitespace: %r" % bad)
        assert len(store.ledger) == 0
    # Cùng lớp lỗi ở manifest: sha256 của entry cũng phải fullmatch.
    assert artifacts._SHA256_HEX.fullmatch("a" * 64)
    assert not artifacts._SHA256_HEX.fullmatch("a" * 64 + "\n")


@test
def ra01_regression_a3_03_scanner_catches_builtins_import_and_variable_alias():
    """PHẢN CHỨNG AUDIT: `builtins.__import__('requests')` và `runner = sp.run; runner([...])`.

    Cả hai đều cho `offenders=[]` ở bản trước, và không nằm trong `not_covered` - tức là claim
    rộng hơn thứ detector thật sự phủ.
    """
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "indirect.py"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(
                "import builtins\n"
                "import subprocess as sp\n"
                "import importlib as il\n"
                "def go():\n"
                "    builtins.__import__('requests')\n"
                "    runner = sp.run\n"
                "    runner(['gh', 'api', '/user'])\n"
                "    importer = il.import_module\n"
                "    importer('httpx')\n"
            )
        offenders = set(_scan_escape_paths(tmp, allowed=set()))
        for expected in (
            ("indirect.py", "dynamic-import:requests"),
            ("indirect.py", "subprocess:gh"),
            ("indirect.py", "dynamic-import:httpx"),
        ):
            assert expected in offenders, (expected, sorted(offenders))
    # Phần CÒN LẠI phải được khai, không được im lặng.
    limits = guards.STATIC_SCANNER_COVERAGE["not_covered"]
    assert limits, "a static scanner that claims no limits is lying"
    joined = " ".join(limits)
    assert "getattr" in joined and "dynamically" in joined, limits
    rc, out, _err = _run_cli("coverage")
    assert rc == 0
    assert json.loads(out)["static_scanner"]["not_covered"]


@test
def ra01_regression_a3_04_manifest_itself_must_be_a_regular_file():
    """PHẢN CHỨNG AUDIT: `manifest.json`/`manifest.sha256` được mở thẳng, không no-follow.

    Ràng buộc containment áp cho entry mà không áp cho chính tài liệu mô tả chúng thì vẫn còn
    nguyên một cửa: manifest có thể là symlink trỏ ra ngoài `run_root`.
    """
    for victim_name in (artifacts.MANIFEST_NAME, artifacts.SIDECAR_NAME):
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "run")
            _run_cli("produce", "--out", root, "--run-id", "r1")
            victim = os.path.join(root, victim_name)
            outside = os.path.join(tmp, "outside_" + victim_name)
            shutil.move(victim, outside)
            try:
                os.symlink(outside, victim)
                print("     manifest_symlink_fixture=real")
            except OSError as exc:
                if getattr(exc, "winerror", None) != 1314:
                    raise
                shutil.copyfile(outside, victim)
                print("     manifest_symlink_fixture=simulated_winerror_1314")
                with _simulated_symlink(victim):
                    report = artifacts.verify(root)
                assert report["ok"] is False, victim_name
                assert any(r["locator"] == victim_name for r in report["rejected_locators"]), report
                continue
            report = artifacts.verify(root)
            assert report["ok"] is False, "a symlinked %s was accepted" % victim_name
            assert any(r["locator"] == victim_name for r in report["rejected_locators"]), report
            rc, _out, err = _run_cli("verify", "--root", root)
            assert rc != 0 and victim_name in err, (rc, err)


@test
def ra01_regression_a3_04_five_categories_cannot_share_one_locator():
    """PHẢN CHỨNG AUDIT: manifest reseal cho cả năm hạng mục cùng trỏ MỘT locator vẫn `ok=true`.

    Acceptance đòi SHA-256 cho TỪNG file trong năm hạng mục. Đếm entry không thay được đếm
    OBJECT rời nhau - năm dòng trỏ một tệp là retention của một tệp, không phải của năm.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.join(tmp, "run")
        _run_cli("produce", "--out", root, "--run-id", "r1")
        manifest = _load_manifest(root)
        one = next(e for e in manifest["entries"] if e["category"] == "source")
        manifest["entries"] = [
            {"category": c, "locator": one["locator"], "sha256": one["sha256"],
             "bytes": one["bytes"]}
            for c in artifacts.REQUIRED_CATEGORIES
        ]
        _reseal(root, manifest)
        report = artifacts.verify(root)
        assert report["manifest_hash_ok"] is True, "fixture sai - sidecar phải vẫn khớp"
        assert report["ok"] is False, "five categories sharing one file were certified"
        assert report["manifest_invalid"] and "duplicate" in report["manifest_invalid"], report
    # Chặn ngay từ đầu ghi: cùng một locator không được ghi nhận hai lần.
    with tempfile.TemporaryDirectory() as tmp:
        aset = artifacts.ArtifactSet(os.path.join(tmp, "run"), "dup")
        aset.add("source", "same.txt", "x")
        try:
            aset.add("corpus", "same.txt", "x")
        except artifacts.LocatorError as exc:
            assert "already recorded" in exc.reason, exc.reason
        else:
            raise AssertionError("the same locator was recorded twice")


@test
def ra01_regression_a3_05_recorder_is_transparent_for_union_and_environb():
    """PHẢN CHỨNG AUDIT: `os.environ | {}` ném TypeError dưới guard; `os.environb` ngoài tầm.

    Guard làm hỏng cú pháp hợp lệ sẽ bị gỡ ra; guard bỏ sót nửa API thì bằng chứng "không đọc
    biến nhạy cảm" chỉ đúng cho nửa còn lại.
    """
    marker = "FAKE-UNION-PROBE-TOKEN"
    with guards.EnvGuard(inject={"GH_TOKEN": marker}) as recorder:
        merged = os.environ | {"RA01_EXTRA": "1"}
        assert isinstance(merged, dict)
        assert merged["RA01_EXTRA"] == "1"
        assert merged.get("GH_TOKEN") == marker
        reversed_merge = {"RA01_EXTRA": "0"} | os.environ
        assert reversed_merge.get("GH_TOKEN") == marker
        union_reads = list(recorder.sensitive_reads())
        environb_seen = None
        if hasattr(os, "environb"):
            environb_seen = os.environb.get(b"GH_TOKEN")
    assert "GH_TOKEN" in union_reads, union_reads
    if environb_seen is not None:
        assert environb_seen == marker.encode(), environb_seen
    assert "os.environb" in " ".join(guards.EnvGuard.COVERAGE["covered"])


@test
def ra01_regression_a3_05_environb_read_is_recorded():
    """`os.environb[b"GH_TOKEN"]` phải đi vào CÙNG sổ với `os.environ` - một câu trả lời, không hai."""
    if not hasattr(os, "environb"):
        raise PlatformUnsupported("os.environb does not exist on this platform")
    marker = "FAKE-ENVIRONB-PROBE"
    with guards.EnvGuard(inject={"GH_TOKEN": marker}) as recorder:
        value = os.environb[b"GH_TOKEN"]
        reads = recorder.sensitive_reads()
    assert value == marker.encode(), value
    assert "GH_TOKEN" in reads, reads


def main():
    passed = 0
    failed = []
    skipped = []
    for fn in TESTS:
        try:
            fn()
        except PlatformUnsupported as exc:
            skipped.append((fn.__name__, str(exc)))
            print("  [SKIP] %s -- %s" % (fn.__name__, exc))
        except Exception as exc:  # noqa: BLE001 - suite phải báo cáo mọi kiểu lỗi
            failed.append((fn.__name__, "%s: %s" % (type(exc).__name__, exc)))
            print("  [FAIL] %s -- %s: %s" % (fn.__name__, type(exc).__name__, exc))
        else:
            passed += 1
            print("  [OK] %s" % fn.__name__)
    # Hai số phải BẰNG NHAU, và mẫu số KHÔNG gồm test bị skip - nếu gồm thì một nền không chạy
    # được fixture sẽ làm gate đỏ vì lý do sai. Test skip được liệt kê ĐÍCH DANH ngay dưới, để
    # "N/N" không bao giờ che giấu một phép thử đã biến mất.
    total = len(TESTS) - len(skipped)
    print("== ra01 core selftest %d/%d ==" % (passed, total))
    if skipped:
        print("== skipped %d (platform cannot build the fixture) ==" % len(skipped))
        for name, reason in skipped:
            print("   - %s: %s" % (name, reason))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
