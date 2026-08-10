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
import json
import os
import re
import shutil
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

# Khai giới hạn của chính bộ quét, BẰNG MÁY. g1 tuyên bố scanner chứng minh "không có lối ra
# mạng"; auditor phá bằng `importlib.import_module` và `subprocess`. Bản này phủ thêm hai đường đó
# nhưng KHÔNG nâng claim lên "mọi lối ra" - một bộ quét tĩnh không thể có claim đó.
_ESCAPE_SCANNER_LIMITS = (
    "import target computed at runtime (importlib.import_module(name_from_variable))",
    "argv built dynamically (subprocess.run([tool_var, ...]))",
    "eval/exec, ctypes, direct syscalls",
)

TESTS = []


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


def _scan_escape_paths(directory, allowed):
    """Đường thoát mà `Import`/`ImportFrom` KHÔNG thấy (finding wp77-g1-sec-02).

    Bắt ba lớp: import động có đích hằng, gọi tiến trình ngoài với argv[0] hằng nằm trong
    NETWORK_TOOLS, và `os.system`/`os.popen`.
    """
    offenders = []
    for name, tree in _parse_dir(directory):
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            called = _dotted(node.func)
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
            called = _dotted(node.func)
            if called in ("os.getenv", "os.environ.get", "os.environ.pop", "os.environ.setdefault"):
                literal = _const_str(node.args[0]) if node.args else None
                if literal and _SENSITIVE_LITERAL.match(literal.upper()):
                    note(node.lineno, "%s(%r)" % (called, literal))
            if called == "os.environ.update":
                note(node.lineno, "os.environ.update(...)")
        elif isinstance(node, ast.Subscript) and _dotted(node.value) == "os.environ":
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
                "reviewed_sha": "abc",
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
    if not hasattr(os, "symlink"):
        raise AssertionError("platform without symlink support - test cannot make its claim")
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
        os.symlink(outside, victim)
        assert artifacts.sha256_file(victim) == artifacts.sha256_bytes(content)
        report = artifacts.verify(root)
        assert report["ok"] is False, "a symlink out of run_root was certified because its hash matched"
        # Hai lớp cùng bắt được ca này; chấp nhận lớp nào bắt trước, nhưng PHẢI gọi đúng tên locator.
        named = [r["locator"] for r in report["rejected_locators"]] + report["not_regular_files"]
        assert "corpus/cases.json" in named, report
        assert "corpus" in report["missing_categories"], report


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
                    "reviewed_sha": "b044f8b1",
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
    with guards.EnvGuard() as recorder:
        proc = subprocess.run(
            [sys.executable, "-c", reader],
            capture_output=True,
            text=True,
            timeout=120,
            env={"AWS_SECRET_ACCESS_KEY": marker, "PATH": "/usr/bin:/bin"},
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


def main():
    passed = 0
    failed = []
    for fn in TESTS:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 - suite phải báo cáo mọi kiểu lỗi
            failed.append((fn.__name__, "%s: %s" % (type(exc).__name__, exc)))
            print("  [FAIL] %s -- %s: %s" % (fn.__name__, type(exc).__name__, exc))
        else:
            passed += 1
            print("  [OK] %s" % fn.__name__)
    total = len(TESTS)
    print("== ra01 core selftest %d/%d ==" % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
