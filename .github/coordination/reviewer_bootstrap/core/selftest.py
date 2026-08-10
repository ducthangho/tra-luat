"""Suite phản chứng cho lõi RA-01 (acceptance §3 của #77).

Nguyên tắc: "có mặt trong code" KHÔNG phải nghiệm thu. Mỗi bất biến phải có một phép thử CHẠY
ĐƯỢC, và mỗi tripwire phải có ĐỐI CHỨNG DƯƠNG chứng minh nó còn sống - một detector chết cũng
báo "sạch".

ID test dùng tiền tố `ra01_`, KHÔNG dùng `wp77_`: `wp77_` là namespace của test fragment trong
`scripts/test_fragments/`, mà §2 của #77 khai rõ fragment KHÔNG thuộc write set và KHÔNG được tạo
trong Packet này. Dùng lại tiền tố đó sẽ đâm vào test-ID registry dùng chung (protocol §10.2).
"""

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
from core.fake_github import FakeGitHub, FakeGitHubError  # noqa: E402
from core.ledger import Ledger  # noqa: E402

CONTROLLER = os.path.join(_HERE, "controller.py")
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

TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


def _scan_forbidden_imports(directory, allowed):
    """Liệt kê (tệp, module) import bị cấm trong `directory`, bỏ qua cặp nằm trong `allowed`."""
    import ast

    offenders = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".py"):
            continue
        with open(os.path.join(directory, name), "r", encoding="utf-8") as fh:
            tree = ast.parse(fh.read(), filename=name)
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


def _store(tmp, name="ledger.json"):
    store = FakeGitHub(os.path.join(tmp, name))
    store.add_issue(77, "wp77 packet spec", labels=["state:leased"])
    store.add_comment(5236083781, 77, "lease granted")
    store.add_pull(1001, "b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb", "mission/76/integration")
    store.add_ci_run(9001, "success")
    store.add_diff(1001, "--- a\n+++ b\n")
    return store


def _run_cli(*argv):
    proc = subprocess.run(
        [sys.executable, CONTROLLER] + list(argv),
        capture_output=True,
        text=True,
        timeout=120,
    )
    return proc.returncode, proc.stdout, proc.stderr


# ─────────────────────────────────────────────────────────────────────────────
# A. Tập operation ĐÓNG + schema tham số
# ─────────────────────────────────────────────────────────────────────────────
@test
def ra01_operation_set_is_closed_and_declared():
    assert operations.OPERATION_NAMES == EXPECTED_OPERATIONS, operations.OPERATION_NAMES
    schema = operations.schema()
    assert schema["closed"] is True
    assert tuple(sorted(schema["operations"])) == EXPECTED_OPERATIONS
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
        operations.validate("read_issue", {"repo": "ducthangho/tra-luat"})
    except operations.ParameterError as exc:
        assert exc.missing == ("issue_number",), exc.missing
        assert "issue_number" in str(exc)
    else:
        raise AssertionError("missing parameter was NOT rejected")


@test
def ra01_extra_parameter_rejected_by_name():
    try:
        operations.validate(
            "read_issue",
            {"repo": "ducthangho/tra-luat", "issue_number": 77, "token": "x"},
        )
    except operations.ParameterError as exc:
        assert exc.unexpected == ("token",), exc.unexpected
    else:
        raise AssertionError("extra parameter was NOT rejected")


@test
def ra01_wrong_type_and_enum_rejected():
    for params in (
        {"repo": "ducthangho/tra-luat", "issue_number": "77"},
        {"repo": 1, "issue_number": 77},
    ):
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
                "repo": "ducthangho/tra-luat",
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
        store.inject("read_issue", "403")  # nếu handler chạy, lỗi này sẽ nổ ra thay vì ParameterError
        try:
            store.call("read_issue", {"repo": "ducthangho/tra-luat"})
        except operations.ParameterError:
            pass
        else:
            raise AssertionError("validation did not run first")
        assert store.calls == [], store.calls
        # Lỗi bơm vào vẫn còn nguyên trong hàng đợi - bằng chứng dương là handler CHƯA chạy.
        assert store._injected["read_issue"] == ["403"]


# ─────────────────────────────────────────────────────────────────────────────
# B. Fake GitHub store - không chạm mạng, có cả đường LỖI
# ─────────────────────────────────────────────────────────────────────────────
@test
def ra01_fake_store_serves_every_read_operation():
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        repo = "ducthangho/tra-luat"
        assert store.call("read_issue", {"repo": repo, "issue_number": 77})["number"] == 77
        assert store.call("read_comment", {"repo": repo, "comment_id": 5236083781})["id"]
        assert store.call("read_pr", {"repo": repo, "pull_number": 1001})["draft"] is True
        assert store.call("read_ci_run", {"repo": repo, "run_id": 9001})["conclusion"] == "success"
        assert "diff" in store.call("read_diff", {"repo": repo, "pull_number": 1001})


@test
def ra01_fake_store_simulates_403_404_409_and_rate_limit():
    with tempfile.TemporaryDirectory() as tmp:
        repo = "ducthangho/tra-luat"
        for kind, status in (("403", 403), ("404", 404), ("409", 409), ("rate_limit", 429)):
            store = _store(tmp, name="ledger_%s.json" % kind)
            store.inject("read_issue", kind)
            try:
                store.call("read_issue", {"repo": repo, "issue_number": 77})
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
            store.call("read_issue", {"repo": "ducthangho/tra-luat", "issue_number": 999999})
        except FakeGitHubError as exc:
            assert exc.status == 404
        else:
            raise AssertionError("absent issue did not 404")


@test
def ra01_network_guard_raises_named_error_not_hang():
    """ĐỐI CHỨNG DƯƠNG: chứng minh guard mạng còn sống, và nó ném ĐÍCH DANH chứ không treo."""
    import socket

    with guards.NetworkGuard():
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
    # Gỡ patch xong phải trả lại nguyên trạng, nếu không guard sẽ rò sang test khác.
    assert socket.socket is not guards._BlockedSocket


@test
def ra01_full_exercise_runs_under_network_guard():
    """Toàn bộ đường nghiệp vụ chạy TRỌN dưới NetworkGuard - không có lối ra mạng nào."""
    with tempfile.TemporaryDirectory() as tmp, guards.NetworkGuard() as guard:
        store = _store(tmp)
        repo = "ducthangho/tra-luat"
        store.call("read_issue", {"repo": repo, "issue_number": 77})
        store.call("read_diff", {"repo": repo, "pull_number": 1001})
        store.call(
            "post_heartbeat",
            {"repo": repo, "issue_number": 77, "reconcile_key": "k1", "payload": {"state": "running"}},
        )
        store.call("run_test", {"repo": repo, "command": "python3 -m pytest"})
        assert guard.attempts == [], guard.attempts


@test
def ra01_run_test_is_declared_but_not_executed_here():
    """run_test KHÔNG được giả vờ đã chạy - kết quả bịa còn tệ hơn không có kết quả."""
    with tempfile.TemporaryDirectory() as tmp:
        store = _store(tmp)
        result = store.call("run_test", {"repo": "ducthangho/tra-luat", "command": "true"})
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
            "repo": "ducthangho/tra-luat",
            "issue_number": 77,
            "reconcile_key": "gh77-heartbeat-g1",
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
        base = {"repo": "ducthangho/tra-luat", "issue_number": 77, "payload": {"state": "running"}}
        store.call("post_heartbeat", dict(base, reconcile_key="k1"))
        store.call("post_heartbeat", dict(base, reconcile_key="k2"))
        assert len(store.ledger) == 2, len(store.ledger)


@test
def ra01_idempotence_is_order_independent():
    """Đảo thứ tự hai lời gọi KHÁC key phải cho CÙNG trạng thái cuối (so bằng state_hash)."""
    repo = "ducthangho/tra-luat"
    a = {"repo": repo, "issue_number": 77, "reconcile_key": "kA", "payload": {"n": 1}}
    b = {"repo": repo, "issue_number": 77, "reconcile_key": "kB", "payload": {"n": 2}}
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
        base = {"repo": "ducthangho/tra-luat", "issue_number": 77, "reconcile_key": "kX"}
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
# D. Artifact manifest + locator bền
# ─────────────────────────────────────────────────────────────────────────────
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
    """RETENTION: tiến trình sinh artifact đã CHẾT rồi mới verify, từ một tiến trình KHÁC.

    Đây là điều mà "comment summary" và "bundle gửi ngoài luồng" không làm được.
    """
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


# ─────────────────────────────────────────────────────────────────────────────
# E. Ranh giới của chính packet - ZERO credential, ZERO model call
# ─────────────────────────────────────────────────────────────────────────────
@test
def ra01_env_tripwire_positive_control():
    """ĐỐI CHỨNG DƯƠNG: detector PHẢI bắt được một lần đọc cố ý.

    Không có test này thì "không phát hiện lần đọc nào" có thể chỉ nghĩa là detector đã chết.
    """
    os.environ["GH_TOKEN"] = "FAKE-ghp-000000000000000000000000000000000000"
    try:
        with guards.EnvGuard() as recorder:
            os.environ.get("GH_TOKEN")
            os.getenv("AWS_SECRET_ACCESS_KEY")
        assert "GH_TOKEN" in recorder.sensitive_reads(), recorder.sensitive_reads()
        assert "AWS_SECRET_ACCESS_KEY" in recorder.sensitive_reads()
    finally:
        os.environ.pop("GH_TOKEN", None)


@test
def ra01_core_reads_zero_credentials_with_fakes_injected():
    """Bơm credential GIẢ vào env rồi chạy trọn đường nghiệp vụ - phải KHÔNG có lần đọc nhạy cảm."""
    injected = {
        "GH_TOKEN": "FAKE-ghp-111111111111111111111111111111111111",
        "GITHUB_TOKEN": "FAKE-ghs-222222222222222222222222222222222222",
        "AWS_ACCESS_KEY_ID": "FAKE-AKIA0000000000000000",
        "AWS_SECRET_ACCESS_KEY": "FAKE-secret-0000000000000000000000000000",
    }
    saved = {k: os.environ.get(k) for k in injected}
    os.environ.update(injected)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            with guards.EnvGuard() as recorder, guards.NetworkGuard() as guard:
                store = _store(tmp)
                repo = "ducthangho/tra-luat"
                store.call("read_issue", {"repo": repo, "issue_number": 77})
                store.call("read_pr", {"repo": repo, "pull_number": 1001})
                store.call(
                    "post_verdict",
                    {
                        "repo": repo,
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
            assert recorder.sensitive_reads() == [], recorder.sensitive_reads()
            assert guard.attempts == [], guard.attempts
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


@test
def ra01_no_artifact_contains_injected_credential_value():
    """Artifact phải không rò credential ra đĩa, kể cả khi env đang có biến giả."""
    marker = "FAKE-ghp-333333333333333333333333333333333333"
    os.environ["GH_TOKEN"] = marker
    try:
        with tempfile.TemporaryDirectory() as tmp:
            _run_cli("produce", "--out", tmp, "--run-id", "r1")
            for dirpath, _dirs, files in os.walk(tmp):
                for name in files:
                    with open(os.path.join(dirpath, name), "rb") as fh:
                        assert marker.encode() not in fh.read(), os.path.join(dirpath, name)
    finally:
        os.environ.pop("GH_TOKEN", None)


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
    offenders = _scan_forbidden_imports(_HERE, allowed={("guards.py", "socket"), ("selftest.py", "socket")})
    assert not offenders, offenders


@test
def ra01_import_scanner_has_teeth():
    """ĐỐI CHỨNG DƯƠNG cho phép kiểm ở trên: nó PHẢI bắt được một import bị cấm.

    Một bộ quét không bắt được gì cũng cho ra danh sách rỗng. Không có test này thì
    `ra01_core_modules_import_no_network_or_provider_library` xanh mà không nói lên điều gì.
    """
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
def ra01_operations_expose_no_credential_parameter():
    """Không op nào có chỗ nhận token - không có bề mặt để nhét credential vào."""
    suspicious = re.compile(r"token|secret|password|credential|auth", re.I)
    for name, spec in operations.OPERATIONS.items():
        for param in spec["params"]:
            assert not suspicious.search(param), (name, param)


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
