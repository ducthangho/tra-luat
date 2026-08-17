# -*- coding: utf-8 -*-
"""Behavior tests for the pre-selector gate lifecycle runner."""

from __future__ import annotations

import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import tempfile
import time


RUNNER = Path(__file__).with_name("gate_lifecycle.py")
STRICT_COUNT = r"(?m)^.*\b([1-9][0-9]*)/\1\b[^\r\n]*\r?\n?\Z"


def _run(args: list[str], *, cwd: Path, timeout: float = 20.0) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )


def _git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="strict",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return proc.stdout.strip()


def _repo(root: Path) -> tuple[str, str]:
    _git(root, "init", "--quiet")
    _git(root, "config", "user.email", "gate-test@example.invalid")
    _git(root, "config", "user.name", "Gate Test")
    (root / "tracked.txt").write_text("v1\n", encoding="utf-8", newline="\n")
    _git(root, "add", "tracked.txt")
    _git(root, "commit", "--quiet", "-m", "fixture")
    return _git(root, "rev-parse", "HEAD"), _git(root, "rev-parse", "HEAD^{tree}")


def _run_gate(
    repo: Path,
    evidence: Path,
    command: list[str],
    *,
    expected_head: str | None = None,
    require_clean: bool = False,
    wait_seconds: float = 1.0,
    timeout_seconds: float = 10.0,
    positive_regex: str | None = None,
    name: str = "fixture",
) -> subprocess.CompletedProcess[str]:
    args = [
        "run",
        "--kind",
        "heavy",
        "--name",
        name,
        "--repo",
        str(repo),
        "--evidence",
        str(evidence),
        "--output",
        str(evidence.with_suffix(".out")),
        "--wait-seconds",
        str(wait_seconds),
        "--timeout-seconds",
        str(timeout_seconds),
        "--selected-test",
        name,
    ]
    if positive_regex is not None:
        args.extend(["--positive-regex", positive_regex])
    if expected_head is not None:
        args.extend(["--expected-head", expected_head, "--base-sha", expected_head])
    if require_clean:
        args.append("--require-clean")
    args.extend(["--", *command])
    return _run(args, cwd=repo)


def case_success_records_exact_identity() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_success_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, tree = _repo(repo)
        evidence = root / "evidence.json"
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", "print('TARGET_OK')"],
            expected_head=head,
            require_clean=True,
            positive_regex="TARGET_OK",
        )
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 0, proc.stderr
        assert "TARGET_OK" in proc.stdout
        assert payload["schema_version"] == 2
        assert payload["status"] == "pass"
        assert payload["returncode"] == 0
        assert payload["identity"]["head_sha"] == head
        assert payload["identity"]["tree_sha"] == tree
        assert payload["identity"]["tracked_clean"] is True
        assert payload["identity"]["worktree_clean"] is True
        assert payload["identity_after"]["head_sha"] == head
        assert payload["positive_verified"] is True
        assert payload["positive_match"] == "TARGET_OK"
        assert len(payload["output_sha256"]) == 64
        assert len(payload["identity"]["runner_sha256"]) == 64
        assert payload["duration_seconds"] >= 0


def case_head_mismatch_fails_before_command() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_head_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        _repo(repo)
        evidence = root / "evidence.json"
        sentinel = root / "must-not-exist"
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", f"open({str(sentinel)!r}, 'w').write('bad')"],
            expected_head="0" * 40,
            require_clean=True,
        )
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 2
        assert payload["status"] == "preflight_error"
        assert not sentinel.exists()


def case_dirty_tree_fails_before_command() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_dirty_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        (repo / "tracked.txt").write_text("dirty\n", encoding="utf-8", newline="\n")
        evidence = root / "evidence.json"
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", "raise SystemExit(0)"],
            expected_head=head,
            require_clean=True,
        )
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 2
        assert payload["status"] == "preflight_error"
        assert payload["identity"]["tracked_clean"] is False


def case_untracked_file_fails_clean_preflight() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_untracked_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        (repo / "untracked.py").write_text("raise RuntimeError('shadow import')\n", encoding="utf-8")
        evidence = root / "evidence.json"
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", "raise SystemExit(0)"],
            expected_head=head,
            require_clean=True,
        )
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 2
        assert payload["status"] == "preflight_error"
        assert payload["identity"]["tracked_clean"] is True
        assert payload["identity"]["worktree_clean"] is False


def case_failure_is_not_rewritten_green() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_fail_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", "raise SystemExit(7)"],
            expected_head=head,
            require_clean=True,
        )
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 7
        assert payload["status"] == "fail"
        assert payload["returncode"] == 7


def case_zero_count_is_not_positive_evidence() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_positive_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", "print('0/0')"],
            expected_head=head,
            require_clean=True,
            positive_regex=STRICT_COUNT,
        )
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 1
        assert payload["status"] == "fail"
        assert payload["positive_verified"] is False


def case_intermediate_count_is_not_final_evidence() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_final_marker_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", "print('1/1'); print('finished without verdict')"],
            expected_head=head,
            require_clean=True,
            positive_regex=STRICT_COUNT,
        )
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 1
        assert payload["positive_verified"] is False


def case_identity_change_during_gate_invalidates_pass() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_change_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", "from pathlib import Path; Path('tracked.txt').write_text('changed\\n')"],
            expected_head=head,
            require_clean=True,
        )
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 2
        assert payload["status"] == "infra_error"
        assert "identity changed" in payload["error"]


def case_heavy_gate_is_singleton_per_host() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_lock_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        other_repo = root / "other-repo"
        other_repo.mkdir()
        other_head, _ = _repo(other_repo)
        ready = root / "ready"
        release = root / "release"
        first_evidence = root / "first.json"
        holder_code = (
            "import pathlib,time;"
            f"pathlib.Path({str(ready)!r}).write_text('ready');"
            f"p=pathlib.Path({str(release)!r});"
            "deadline=time.monotonic()+10;"
            "exec(\"while not p.exists() and time.monotonic() < deadline:\\n time.sleep(0.02)\")"
        )
        first_args = [
            sys.executable,
            str(RUNNER),
            "run",
            "--kind",
            "heavy",
            "--name",
            "holder",
            "--repo",
            str(repo),
            "--evidence",
            str(first_evidence),
            "--expected-head",
            head,
            "--require-clean",
            "--wait-seconds",
            "1",
            "--timeout-seconds",
            "10",
            "--selected-test",
            "holder",
            "--",
            sys.executable,
            "-c",
            holder_code,
        ]
        first = subprocess.Popen(
            first_args,
            cwd=repo,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            deadline = time.monotonic() + 5
            while not ready.exists() and time.monotonic() < deadline:
                if first.poll() is not None:
                    break
                time.sleep(0.02)
            assert ready.exists(), first.communicate(timeout=1)
            second_evidence = root / "second.json"
            second = _run_gate(
                other_repo,
                second_evidence,
                [sys.executable, "-c", "raise SystemExit(0)"],
                expected_head=other_head,
                require_clean=True,
                wait_seconds=0.1,
                name="contender",
            )
            payload = json.loads(second_evidence.read_text(encoding="utf-8"))
            assert second.returncode == 75
            assert payload["status"] == "busy"
        finally:
            release.write_text("release\n", encoding="utf-8", newline="\n")
            first_stdout, first_stderr = first.communicate(timeout=10)
        assert first.returncode == 0, first_stdout + first_stderr


def case_spawn_error_records_infra_error() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_spawn_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        proc = _run_gate(
            repo,
            evidence,
            [str(root / "definitely-missing-command")],
            expected_head=head,
            require_clean=True,
        )
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 2
        assert payload["status"] == "infra_error"
        assert payload["returncode"] == 2
        assert payload["error"]


def case_timeout_is_not_rewritten_green() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_timeout_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", "import time; time.sleep(5)"],
            expected_head=head,
            require_clean=True,
            timeout_seconds=0.1,
        )
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 124
        assert payload["status"] == "timeout"
        assert payload["returncode"] == 124


def case_timeout_kills_descendant_process() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_tree_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        spawned = root / "spawned"
        survived = root / "descendant-survived"
        child_code = (
            "import time; from pathlib import Path; time.sleep(1.5); "
            f"Path({str(survived)!r}).write_text('survived')"
        )
        parent_code = (
            "import pathlib,subprocess,sys,time;"
            f"subprocess.Popen([sys.executable,'-c',{child_code!r}],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True);"
            f"pathlib.Path({str(spawned)!r}).write_text('spawned');"
            "time.sleep(30)"
        )
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", parent_code],
            expected_head=head,
            require_clean=True,
            timeout_seconds=0.7,
        )
        assert proc.returncode == 124
        assert spawned.is_file()
        time.sleep(2.0)
        assert not survived.exists()


def case_interrupt_kills_tree_before_releasing_lock() -> None:
    """Ctrl-C phải giết cây TRƯỚC khi nhả khoá — KỂ CẢ cháu đã rời nhóm.

    Cross-review P1 trên PR "#141". Con nằm ở SESSION MỚI nên nó không nhận ngắt
    từ terminal — chỉ tiến trình cha nhận. Bản cũ chỉ bắt `TimeoutExpired`, nên
    `KeyboardInterrupt` chạy thẳng qua, `_maybe_heavy_lock` nhả khoá ở `finally`
    của nó, và cây con VẪN CHẠY. Lượt heavy gate kế tiếp lấy được khoá rồi chồng
    lên lượt "đã huỷ".

    Đo HAI vế, vì một mình vế nào cũng lọt:
      (a) hậu duệ KHÔNG được sống sót sau khi gate thoát;
      (b) khoá phải thực sự tự do sau đó — chứng minh bằng một gate MỚI chạy được
          ngay, chứ không suy ra từ việc tệp khoá biến mất.
    """
    if os.name == "nt":                     # SIGINT tới nhóm khác hẳn trên Windows
        print("  BO QUA case_interrupt_kills_tree_before_releasing_lock: fixture POSIX")
        return
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_intr_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        spawned = root / "spawned"
        survived = root / "descendant-survived"
        # CHÁU RỜI NHÓM — đây mới là ca cần đo, và ca cũ của tôi KHÔNG đo nó.
        # Cross-review nói thẳng: "the added test misses this because its descendant
        # remains in the parent's process group". Đúng. `setsid()` đưa cháu sang
        # session/nhóm MỚI, nên `killpg` của nhóm cha không với tới — nếu chốt chỉ
        # `killpg` thì cháu này sống sót và ca phải ĐỎ.
        child_code = (
            "import os, time; from pathlib import Path; os.setsid(); time.sleep(2.5); "
            f"Path({str(survived)!r}).write_text('survived')"
        )
        parent_code = (
            "import pathlib,subprocess,sys,time;"
            f"subprocess.Popen([sys.executable,'-c',{child_code!r}],"
            "stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True);"
            f"pathlib.Path({str(spawned)!r}).write_text('spawned');"
            "time.sleep(30)"
        )
        argv = [
            "run", "--kind", "heavy", "--name", "fixture", "--repo", str(repo),
            "--evidence", str(evidence), "--output", str(evidence.with_suffix(".out")),
            "--wait-seconds", "1.0", "--timeout-seconds", "30",
            "--selected-test", "fixture",
            "--expected-head", head, "--base-sha", head, "--require-clean",
            "--", sys.executable, "-c", parent_code,
        ]
        proc = subprocess.Popen(
            [sys.executable, str(RUNNER), *argv], cwd=repo, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        for _ in range(100):                       # chờ con CHÁU thật sự tồn tại
            if spawned.is_file():
                break
            time.sleep(0.1)
        assert spawned.is_file(), "chau chua kip sinh — fixture khong do duoc gi"
        proc.send_signal(signal.SIGINT)
        proc.communicate(timeout=30)

        # (a) hậu duệ phải chết. Chờ QUÁ mốc nó định ghi, kẻo ta chỉ đo "chưa tới lúc".
        time.sleep(3.0)
        assert not survived.exists(), "hau due song sot sau khi gate bi ngat"

        # (b) khoá tự do — đo bằng một gate MỚI, không đọc tệp khoá.
        lai = _run_gate(
            repo, root / "evidence2.json",
            [sys.executable, "-c", "print('TARGET_OK')"],
            expected_head=head, require_clean=True,
            positive_regex="TARGET_OK", wait_seconds=1.0,
        )
        assert lai.returncode == 0, (
            f"khoa chua duoc nha sau khi ngat: rc={lai.returncode} {lai.stdout} {lai.stderr}"
        )


def case_dirty_run_is_allowed_but_never_reusable() -> None:
    """Bỏ `--require-clean` thì gate CHẠY ĐƯỢC trên cây bẩn, nhưng chứng KHÔNG tái dùng.

    Hai vế phải đi cùng nhau, và một mình vế nào cũng sai:
      (a) chạy được — nếu không thì luồng `release-checklist` (gate ở bước 5,
          commit ở bước 7) không test nổi thay đổi đang chờ (P1 PR "#141");
      (b) không tái dùng được — nếu không thì có đường RỬA bằng chứng: chạy gate
          lúc cây bẩn tại HEAD=X, rồi phục hồi cây cho sạch về đúng X, thế là
          `head_sha`/`tree_sha` khớp và cây hiện tại sạch, nên chứng của thứ CHƯA
          TỪNG commit lại thành chứng cho commit X.

    Vế (b) đo ĐÚNG kịch bản rửa đó: sinh chứng trên cây bẩn, dọn cây, rồi
    `validate` — phải `reusable: false` kèm `worktree_clean`.

    GHI THẲNG: chốt chặn đường rửa ĐÃ CÓ SẴN trong `validate` từ trước bản vá này
    (nó kiểm `identity.worktree_clean`, khác với `current.worktree_clean` ngay
    dưới). Lượt vá đầu của tôi thêm một phép kiểm THỨ HAI cho cùng điều kiện, và
    đột biến phơi ra ngay: gỡ bản thêm ấy mà `validate` vẫn `reusable: false`.
    Ca này vì thế KHÔNG khoá một chốt mới — nó khoá QUAN HỆ giữa hai vế, đúng thứ
    chưa ai đo: mở được cửa cây bẩn mà không mở kèm đường rửa.
    """
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_ban_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, tree = _repo(repo)
        ban = repo / "dang_sua.txt"
        ban.write_text("chua commit\n", encoding="utf-8", newline="\n")
        evidence = root / "evidence.json"
        proc = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", "print('TARGET_OK')"],
            expected_head=head,
            require_clean=False,              # <- đúng thứ chế độ cây bẩn làm
            positive_regex="TARGET_OK",
        )
        assert proc.returncode == 0, f"cay ban ma khong chay duoc: {proc.stdout} {proc.stderr}"
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert payload["status"] == "pass"
        assert payload["identity"]["worktree_clean"] is False

        ban.unlink()                          # dọn cây -> dựng lại đúng ca RỬA
        out = _run(
            [
                "validate", "--evidence", str(evidence),
                "--output", str(evidence.with_suffix(".out")), "--repo", str(repo),
                "--expected-positive-regex", "TARGET_OK",
                "--expected-head", head, "--expected-tree", tree,
                "--expected-base-sha", head, "--expected-name", "fixture",
                "--expected-selected-test", "fixture",
                "--expected-system", platform.system(),
                "--expected-system-release", platform.release(),
                "--expected-machine", platform.machine(),
                "--expected-python-implementation", platform.python_implementation(),
                "--expected-python", platform.python_version(),
                "--expected-command-json", json.dumps(
                    [sys.executable, "-c", "print('TARGET_OK')"]),
            ],
            cwd=repo,
        )
        ket = json.loads(out.stdout)
        assert ket["reusable"] is False, f"chung cay ban lai tai dung duoc: {ket}"
        assert "worktree_clean" in ket["mismatches"], ket
        assert out.returncode == 3, out.returncode


def case_validate_reuse_is_fail_closed() -> None:
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_validate_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, tree = _repo(repo)
        evidence = root / "evidence.json"
        ran = _run_gate(
            repo,
            evidence,
            [sys.executable, "-c", "print('SELFTEST 1/1')"],
            expected_head=head,
            require_clean=True,
            positive_regex=STRICT_COUNT,
            name="tl-selftest",
        )
        assert ran.returncode == 0, ran.stderr
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        expected_command = payload["command"]
        identity = payload["identity"]
        envelope = [
            "--expected-tree",
            tree,
            "--expected-base-sha",
            head,
            "--expected-name",
            "tl-selftest",
            "--expected-system",
            identity["system"],
            "--expected-system-release",
            identity["system_release"],
            "--expected-machine",
            identity["machine"],
            "--expected-python-implementation",
            identity["python_implementation"],
            "--expected-python",
            identity["python_version"],
            "--expected-selected-test",
            "tl-selftest",
            "--expected-command-json",
            json.dumps(expected_command),
            "--expected-positive-regex",
            payload["positive_regex"],
        ]
        valid = _run(
            [
                "validate",
                "--evidence",
                str(evidence),
                "--output",
                str(evidence.with_suffix(".out")),
                "--expected-head",
                head,
                *envelope,
                "--require-current-runner",
            ],
            cwd=repo,
        )
        stale = _run(
            [
                "validate",
                "--evidence",
                str(evidence),
                "--output",
                str(evidence.with_suffix(".out")),
                "--expected-head",
                "f" * 40,
                *envelope,
            ],
            cwd=repo,
        )
        assert valid.returncode == 0, valid.stderr
        assert json.loads(valid.stdout)["reusable"] is True
        assert stale.returncode == 3
        stale_payload = json.loads(stale.stdout)
        assert stale_payload["reusable"] is False
        assert "head_sha" in stale_payload["mismatches"]

        incomplete = _run(
            [
                "validate",
                "--evidence",
                str(evidence),
                "--output",
                str(evidence.with_suffix(".out")),
                "--expected-head",
                head,
            ],
            cwd=repo,
        )
        assert incomplete.returncode == 2


CASES = [
    case_success_records_exact_identity,
    case_head_mismatch_fails_before_command,
    case_dirty_tree_fails_before_command,
    case_untracked_file_fails_clean_preflight,
    case_failure_is_not_rewritten_green,
    case_zero_count_is_not_positive_evidence,
    case_intermediate_count_is_not_final_evidence,
    case_identity_change_during_gate_invalidates_pass,
    case_heavy_gate_is_singleton_per_host,
    case_spawn_error_records_infra_error,
    case_timeout_is_not_rewritten_green,
    case_timeout_kills_descendant_process,
    case_interrupt_kills_tree_before_releasing_lock,
    case_dirty_run_is_allowed_but_never_reusable,
    case_validate_reuse_is_fail_closed,
]


def main() -> int:
    failures: list[str] = []
    for case in CASES:
        try:
            case()
        except BaseException as exc:  # behavior runner must report every named case
            failures.append(f"{case.__name__}: {exc!r}")
    for failure in failures:
        print(f"[FAIL] {failure}")
    passed = len(CASES) - len(failures)
    print(f"gate lifecycle tests: {passed}/{len(CASES)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
