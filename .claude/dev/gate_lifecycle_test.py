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


def _cgroup_gate_dang_co() -> set[str]:
    """Tên các cgroup `tl-gate-*` đang tồn tại. Rỗng khi nền không có cgroup v2."""
    for dong in _doc_mountinfo():
        phan = dong.split(" - ", 1)
        if len(phan) == 2 and phan[1].split()[:1] == ["cgroup2"] and len(phan[0].split()) >= 5:
            goc = Path(phan[0].split()[4])
            try:
                return {q.name for q in goc.rglob("tl-gate-*") if q.is_dir()}
            except OSError:
                return set()
    return set()


def _doc_mountinfo() -> list[str]:
    try:
        return Path("/proc/self/mountinfo").read_text(encoding="utf-8").splitlines()
    except OSError:
        return []


def case_spawn_error_records_infra_error() -> None:
    """Sinh con hỏng ⇒ `infra_error`, VÀ không để lại cgroup rác.

    Nhánh này `return` SỚM nên nó KHÔNG đi qua khối `finally` dọn cgroup — đo được:
    mỗi lượt sinh con hỏng bỏ lại một thư mục cgroup rỗng, tích dần trên runner CI
    cho tới khi chạm trần `cgroup.max.descendants`. "Đã cấp thì phải trả", và mọi
    đường thoát đều là đường phải trả.
    """
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_spawn_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        truoc = _cgroup_gate_dang_co()
        proc = _run_gate(
            repo,
            evidence,
            [str(root / "definitely-missing-command")],
            expected_head=head,
            require_clean=True,
        )
        con_lai = _cgroup_gate_dang_co() - truoc
        payload = json.loads(evidence.read_text(encoding="utf-8"))
        assert proc.returncode == 2
        assert payload["status"] == "infra_error"
        assert payload["returncode"] == 2
        assert payload["error"]
        assert not con_lai, "sinh con hong de lai cgroup rac: %s" % sorted(con_lai)


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


def case_descendant_spawned_during_shutdown_is_contained() -> None:
    """Cháu ĐẺ THÊM khi bị bắn cũng phải chết trước khi khoá được nhả.

    Cross-review P1 `:388`, bằng chứng tươi trên `47d10b0`. Bản vá trước chụp cây
    MỘT LẦN rồi giết; một hậu duệ tách rời có thể cài handler SIGTERM và sinh ra
    tiến trình `setsid()` MỚI ngay lúc nhận tín hiệu — đứa ấy ra đời SAU ảnh chụp
    và nằm ngoài nhóm của `proc.pid`, nên cả vòng lặp PID lẫn `killpg` đều trượt.

    Đây là ca mà ảnh chụp một-lần KHÔNG THỂ bắt được, nên nó đo đúng thứ bản vá
    mới thêm: vòng lặp {chụp → bắn đứa mới} chạy trong lúc cha CÒN SỐNG, tới khi
    một vòng không thấy ai mới.
    """
    if os.name == "nt":
        print("  BO QUA case_descendant_spawned_during_shutdown_is_contained: fixture POSIX")
        return
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_shut_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        spawned = root / "spawned"
        doi = root / "doi-sinh-luc-dong"          # đứa đẻ TRONG lúc dọn
        da_ban = root / "handler-da-chay"          # BẰNG CHỨNG handler thật sự chạy
        # Cháu: setsid, cài handler SIGTERM. Bị bắn thì đẻ thêm một tiến trình
        # setsid nữa rồi mới chết — đúng kịch bản reviewer mô tả.
        chau_song = root / "chau-da-chay"          # cháu THẬT SỰ đã chạy
        chau = (
            "import os, signal, subprocess, sys, time\n"
            "os.setsid()\n"
            f"open({str(chau_song)!r}, 'w').write('chay')\n"
            "def de_them(_s, _f):\n"
            f"    open({str(da_ban)!r}, 'w').write('ran')\n"
            "    subprocess.Popen([sys.executable, '-c',\n"
            "        \"import os,time;os.setsid();time.sleep(2.5);\"\n"
            f"        \"open({str(doi)!r},'w').write('song')\"],\n"
            "        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)\n"
            "    raise SystemExit(0)\n"
            "signal.signal(signal.SIGTERM, de_them)\n"
            "time.sleep(30)\n"
        )
        # HANDLER CHỜ 0,6s RỒI MỚI ĐẺ — dài hơn nhịp quét 0,2s. Đây đúng ca P1
        # cross-review nêu: bản trước thoát vòng lặp vì "không ai mới", rồi đứa
        # muộn sinh trong lúc `proc.wait(2)` và không bao giờ được quét lại — mà
        # bản ghi vẫn khai `giet_tron_ven: true`. Không có độ trễ này thì ca test
        # đo trúng ca DỄ, và bản vá sai vẫn xanh.
        chau = chau.replace("def de_them(_s, _f):\n",
                            "def de_them(_s, _f):\n    time.sleep(0.6)\n")
        # CHA PHỚT LỜ SIGTERM + handler chờ 0,6s = cố dựng lại kịch bản cross-review.
        #
        # NHƯNG PHẢI KHAI THẲNG: ca này **KHÔNG phân biệt được** bản vá điều kiện
        # lặng. Đã đo, không phải phỏng đoán — bơm đột biến "coi không-ai-mới là
        # lặng" (khớp đúng 1 lần, đã kiểm) thì suite VẪN 16/16. Nghĩa là vế `doi`
        # dưới đây đang xanh vì một lý do khác, chưa rõ lý do gì.
        #
        # Vì vậy bản vá `con_song` trong `_terminate_process_tree` hiện dựa trên
        # PHÂN TÍCH của reviewer + lập luận, KHÔNG dựa trên ca test này. Ghi ra đây
        # để không ai đọc "16/16" thành "đã chứng minh": một phép kiểm không thể đỏ
        # thì không phải bằng chứng, và ca này đã được chứng minh là không đỏ được.
        # Việc còn lại: dựng cho được ca đỏ, hoặc chuyển sang cgroup và bỏ cả lớp này.
        cha = (
            "import pathlib,signal,subprocess,sys,time;"
            "signal.signal(signal.SIGTERM, signal.SIG_IGN);"
            f"subprocess.Popen([sys.executable,'-c',{chau!r}],"
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
            "--", sys.executable, "-c", cha,
        ]
        proc = subprocess.Popen([sys.executable, str(RUNNER), *argv], cwd=repo,
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for _ in range(100):
            if spawned.is_file():
                break
            time.sleep(0.1)
        assert spawned.is_file(), "chau chua kip sinh — fixture khong do duoc gi"
        time.sleep(0.5)                            # cho chau kip cai handler
        proc.send_signal(signal.SIGINT)
        proc.communicate(timeout=40)

        time.sleep(3.5)                            # qua han dua moi dinh ghi

        # ĐÒI BẰNG CHỨNG DƯƠNG TRƯỚC KHI ĐỌC VẮNG MẶT (P2 cross-review PR "#141").
        # Không có vế này thì ca xanh cả khi handler CHƯA TỪNG chạy — cháu chết vì
        # `killpg` trước lúc kịp cài, và ta đọc `doi` vắng mặt thành "đã chặn được".
        # Đúng bệnh "vắng mặt vì sạch" và "vắng mặt vì chưa chạy" nhìn như nhau; ca
        # này sinh ra để chống một lỗi cùng họ nên càng không được mắc.
        ban_ghi = json.loads(evidence.read_text(encoding="utf-8"))
        co_che = ban_ghi.get("co_che_cach_ly")

        # CHỨNG DƯƠNG PHẢI HỢP VỚI CƠ CHẾ THẬT SỰ ĐÃ CHẠY.
        #
        # Bản trước đòi "handler SIGTERM đã chạy" làm chứng dương. Đúng với đường
        # QUÉT CÂY, vì ở đó ta bắn SIGTERM và cái handler ấy chính là cửa sổ cần
        # đóng. Nhưng `cgroup.kill` bắn SIGKILL — KHÔNG handler nào chạy được, và
        # đó là LÝ DO nó đúng, không phải dấu hiệu nó sai. Giữ nguyên vế cũ là
        # đang đòi cơ chế mạnh phải để lại dấu vân tay của cơ chế yếu.
        #
        # Nên chứng dương chung là "cháu THẬT SỰ đã sống và nằm trong tầm dọn";
        # riêng đường quét cây mới đòi thêm handler đã chạy.
        assert chau_song.is_file(), (
            "chau chua tung chay — ca nay dang xanh RONG, khong do gi"
        )
        if co_che != "cgroup2":
            assert da_ban.is_file(), (
                "duong quet cay: handler SIGTERM chua tung chay — ca dang xanh RONG"
            )
        assert not doi.exists(), "dua de TRONG luc don song sot sau khi nha khoa"

        # CA NAY TUNG "DAT" QUA DUNG DUONG THAT BAI CUA CO CHE.
        #
        # Đo được trên `38f1253` bằng cách in ra lối ra của vòng lặp: nó thoát bằng
        # `HET HAN t=10.20`, tức HẠN ĐỒNG HỒ vỡ chứ không phải cây đã lặng. Lý do:
        # fixture cho CHA `SIG_IGN` SIGTERM nên cha không bao giờ chết, luôn nằm
        # trong `con_song`, và nhánh "cây đã lặng" KHÔNG ĐỜI NÀO được với tới. Vậy
        # ca này chỉ chứng minh "10s dài hơn 0,6s" — một hằng đẳng thức về chính
        # hằng số của fixture — trong khi runner tự khai `giet_tron_ven: false`.
        #
        # Đó là lý do bơm đột biến vào điều kiện lặng mà suite vẫn 16/16: điều kiện
        # ấy chưa từng được ca nào chạm tới. Vế dưới đây đóng đúng chỗ đó — cơ chế
        # phải KHAI LÀ ĐÃ DỌN TRỌN VẸN, chứ không được "đạt" bằng đường hết hạn.
        if co_che in ("cgroup2", "job-object"):
            assert ban_ghi.get("giet_tron_ven") is True, (
                "gate khai giet_tron_ven=%r — ca cach ly cay dang DAT qua duong that bai"
                % (ban_ghi.get("giet_tron_ven"),)
            )
        else:
            # Đường quét cây thoát vòng lặp bằng HẠN ĐỒNG HỒ (đo được: `HET HAN
            # t=10.20`), vì fixture cho cha `SIG_IGN` nên cha không bao giờ chết và
            # nhánh "cây đã lặng" không đời nào với tới. Nó chặn được ca này, nhưng
            # phải KHAI ĐÚNG rằng lượt dọn không trọn vẹn.
            assert ban_ghi.get("giet_tron_ven") is False, (
                "duong quet cay khai giet_tron_ven=%r trong khi no thoat bang han dong ho"
                % (ban_ghi.get("giet_tron_ven"),)
            )


def case_ke_de_lai_lien_tuc_khong_thoat_duoc() -> None:
    """Kẻ ĐẺ LẠI LIÊN TỤC không được thoát ra ngoài lượt dọn.

    ĐÂY LÀ CA ĐỎ ĐÃ DỰNG ĐƯỢC với cơ chế quét-cây, và là lý do chuyển sang cgroup.

    Vòng vá "cắt cứng 6 lượt" đã bị cross-review bắt vì kẻ đẻ lại liên tục chỉ cần
    sống lâu hơn 6 lượt là thoát. Vòng sau thay 6 lượt bằng hạn đồng hồ 10s — CÙNG
    MỘT HÌNH DẠNG, chỉ rộng hơn. Đo được trên `38f1253`: 33 kẻ sinh ra, **5 sống
    sót** (kẻ sớm nhất sinh lúc t=11,4s, tức sau khi hạn vỡ, trong cửa sổ
    `killpg` → `proc.wait(2)`); chạy lại ba lần, số liệu trùng khít. Cửa sổ ấy là
    CẤU TRÚC chứ không phải đua, nên ca này không phải ca may rủi.

    HAI ĐIỀU KIỆN LÀM CHO PHÉP ĐO NÀY TRUNG THỰC — cả hai đều do đã đo sai một lần:

      · MỐC TUYỆT ĐỐI, không phải `sleep` tương đối. Bản đo đầu cho mỗi kẻ ngủ 6s
        rồi ghi dấu, nên kẻ sinh SỚM kịp ghi xong TRƯỚC khi lượt dọn kết thúc và
        "có dấu" bị đọc thành "sống sót". Ở đây mọi kẻ ngủ tới CÙNG một mốc nằm
        sau khi lượt dọn đã xong hẳn, nên ghi được dấu ⇔ còn sống thật.

      · ĐÒI CHỨNG DƯƠNG TRƯỚC KHI ĐỌC VẮNG MẶT. Bản đo thứ hai truyền `float` vào
        `argv` của `Popen` khiến KHÔNG kẻ nào sinh ra, và "0 sống sót" suýt được
        đọc thành "đã chặn được". Vế `da_sinh` dưới đây chặn đúng ca đó — vắng mặt
        vì sạch và vắng mặt vì chưa chạy không được phép nhìn giống nhau.
    """
    if os.name == "nt":
        print("  BO QUA case_ke_de_lai_lien_tuc_khong_thoat_duoc: fixture POSIX")
        return
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_dela_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        dau = root / "dau"
        dau.mkdir()                                # kẻ CÒN SỐNG ở mốc tuyệt đối
        sinh = root / "sinh"
        sinh.mkdir()                               # kẻ ĐÃ SINH RA (chứng dương)
        vao_vong = root / "vao-vong"

        moc = time.time() + 20.0                   # sau khi lượt dọn xong hẳn
        con = (
            "import os,sys,time\n"
            "os.setsid()\n"
            "n=sys.argv[1]; t=float(sys.argv[2])\n"
            f"open({str(sinh)!r}+'/'+n,'w').write('x')\n"
            "time.sleep(max(0.0,t-time.time()))\n"
            f"open({str(dau)!r}+'/'+n,'w').write('song')\n"
        )
        # Cháu: tách nhóm, PHỚT LỜ SIGTERM, đẻ lại mỗi 0,4s và không bao giờ dừng.
        chau = (
            "import os,signal,subprocess,sys,time\n"
            "os.setsid()\n"
            "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
            f"open({str(vao_vong)!r},'w').write('vao-vong')\n"
            "n=0\n"
            "while True:\n"
            "    n+=1\n"
            f"    subprocess.Popen([sys.executable,'-c',{con!r},str(n),{str(moc)!r}],\n"
            "        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True)\n"
            "    time.sleep(0.4)\n"
        )
        cha = (
            "import signal,subprocess,sys,time;"
            "signal.signal(signal.SIGTERM, signal.SIG_IGN);"
            f"subprocess.Popen([sys.executable,'-c',{chau!r}],"
            "stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True);"
            "time.sleep(120)"
        )
        argv = [
            "run", "--kind", "heavy", "--name", "fixture", "--repo", str(repo),
            "--evidence", str(evidence), "--output", str(evidence.with_suffix(".out")),
            "--wait-seconds", "1.0", "--timeout-seconds", "120",
            "--selected-test", "fixture",
            "--expected-head", head, "--base-sha", head, "--require-clean",
            "--", sys.executable, "-c", cha,
        ]
        proc = subprocess.Popen([sys.executable, str(RUNNER), *argv], cwd=repo,
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            for _ in range(150):
                if vao_vong.is_file():
                    break
                time.sleep(0.1)
            assert vao_vong.is_file(), "chau chua vao vong de — fixture khong do duoc gi"
            time.sleep(0.8)                        # cho vai lua kip ra doi
            proc.send_signal(signal.SIGINT)
            proc.communicate(timeout=60)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.communicate()

        while time.time() < moc + 1.5:
            time.sleep(0.2)

        da_sinh = sorted(int(q.name) for q in sinh.iterdir())
        song_sot = sorted(int(q.name) for q in dau.iterdir())
        # CHỨNG DƯƠNG trước: không có kẻ nào sinh ra thì ca này xanh RỖNG.
        assert len(da_sinh) >= 3, (
            "chi co %d ke sinh ra — ca dang xanh RONG, khong do gi" % len(da_sinh)
        )
        ban_ghi = json.loads(evidence.read_text(encoding="utf-8"))
        co_che = ban_ghi.get("co_che_cach_ly")
        tron_ven = ban_ghi.get("giet_tron_ven")

        # KHẲNG ĐỊNH THEO CƠ CHẾ THẬT SỰ CHẠY, vì hai cơ chế hứa hai thứ khác nhau
        # và gộp chúng làm một là khai sai ở đúng chỗ kho vừa trả giá.
        #
        # Đo được (`TL_GATE_TAT_CGROUP=1` trên chính máy này): đường QUÉT CÂY để
        # thoát 5/33 kẻ. Đó không phải lỗi cần vá thêm lần thứ năm — đó là GIỚI HẠN
        # của mọi cơ chế phải đi hỏi "ai là hậu duệ của ta". Nên với đường ấy ta
        # KHÔNG đòi giết sạch; ta đòi thứ nó bắt buộc phải giữ được: KHÔNG NÓI DỐI.
        if co_che in ("cgroup2", "job-object"):
            assert not song_sot, (
                "vung chua de THOAT %d/%d ke qua moc tuyet doi %s"
                % (len(song_sot), len(da_sinh), song_sot[:10])
            )
            assert tron_ven is True, (
                "vung chua giet sach nhung khai giet_tron_ven=%r" % (tron_ven,)
            )
        else:
            # RÒ THÌ PHẢI KHAI LÀ RÒ. Bản ghi nói dối hỏng nặng hơn hẳn việc sót
            # một tiến trình mà khai đúng — người đọc còn biết đường mà xử lý.
            assert (not song_sot) or tron_ven is False, (
                "duong %r de thoat %d ke ma van khai giet_tron_ven=%r — BAN GHI NOI DOI"
                % (co_che, len(song_sot), tron_ven)
            )


def case_co_che_cach_ly_khai_dung_thu_da_chay() -> None:
    """`co_che_cach_ly` phải khai ĐÚNG đường thật sự chạy, không phải đường mong muốn.

    Đây là ca chống lại lỗi kho đã tái phạm BỐN lần: đếm SỰ CÓ MẶT của một đường
    thay vì KHẢ NĂNG của nó (`shutil.which("gh")` → `rest-chung` → `gh auth status`
    → "artefact tồn tại" mà validator từ chối). Không có ca này thì một lần tụt về
    quét cây sẽ đi qua y hệt một lượt cgroup thành công, và mọi con số sau đó nói
    về một cơ chế chưa từng chạy.

    Hai vế, và một mình vế nào cũng không đủ:
      (a) có cgroup thì phải khai `cgroup2` — nếu không, ta đang chạy đường tốt mà
          bản ghi lại khai đường xấu, và người đọc không tin được gì nữa;
      (b) TẮT cgroup thì phải khai `quet-cay` — nếu không, bản ghi khai một vùng
          chứa chưa từng tồn tại, tức nói dối đúng chỗ nguy hiểm nhất.
    """
    if os.name == "nt":
        print("  BO QUA case_co_che_cach_ly_khai_dung_thu_da_chay: fixture POSIX")
        return
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_coche_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)

        def _chay(tat_cgroup: bool) -> str | None:
            evidence = root / ("e-%s.json" % tat_cgroup)
            # BẢN SAO môi trường thật rồi thêm công tắc — KHÔNG dựng env giả tối
            # thiểu: kho đã trả giá vì cắm env giả vào hàm sinh tiến trình thật.
            moi_truong = dict(os.environ)
            if tat_cgroup:
                moi_truong["TL_GATE_TAT_CGROUP"] = "1"
            else:
                moi_truong.pop("TL_GATE_TAT_CGROUP", None)
            argv = [
                "run", "--kind", "heavy", "--name", "fixture", "--repo", str(repo),
                "--evidence", str(evidence), "--output", str(evidence.with_suffix(".out")),
                "--wait-seconds", "1.0", "--timeout-seconds", "30",
                "--selected-test", "fixture",
                "--expected-head", head, "--base-sha", head, "--require-clean",
                "--", sys.executable, "-c", "print('1/1 ok')",
            ]
            subprocess.run([sys.executable, str(RUNNER), *argv], cwd=repo,
                           text=True, capture_output=True, timeout=60, env=moi_truong)
            return json.loads(evidence.read_text(encoding="utf-8")).get("co_che_cach_ly")

        khi_tat = _chay(True)
        assert khi_tat == "quet-cay", (
            "tat cgroup ma van khai co_che_cach_ly=%r — ban ghi khai mot vung chua "
            "chua tung ton tai" % (khi_tat,)
        )

        khi_bat = _chay(False)
        # KHẢ NĂNG, KHÔNG PHẢI KỲ VỌNG: máy chạy CI có thể không cấp được cgroup, và
        # ép `cgroup2` ở đây là biến ca này thành phép đo môi trường chứ không phải
        # phép đo mã. Chỉ đòi: khai `cgroup2` thì cgroup phải THẬT SỰ dùng được.
        if khi_bat == "cgroup2":
            assert _mount_cgroup2_co_that(), (
                "khai cgroup2 nhung khong dinh vi duoc diem gan cgroup v2"
            )
        else:
            assert khi_bat == "quet-cay", "co che la %r, ngoai hai gia tri POSIX" % (khi_bat,)


def _mount_cgroup2_co_that() -> bool:
    """Có định vị được điểm gắn cgroup v2 thật không (đọc `mountinfo`, không đoán)."""
    try:
        noi_dung = Path("/proc/self/mountinfo").read_text(encoding="utf-8")
    except OSError:
        return False
    for dong in noi_dung.splitlines():
        phan = dong.split(" - ", 1)
        if len(phan) == 2 and phan[1].split()[:1] == ["cgroup2"]:
            return True
    return False


def case_don_khong_tron_ven_lam_do_luot_gate() -> None:
    """Dọn không trọn vẹn thì lượt gate ĐỎ — không chỉ ghi vào bản ghi rồi thôi.

    Trước bản này, `giet_tron_ven: false` chỉ ĐI VÀO BẰNG CHỨNG mà không đổi mã
    thoát: lệnh gate trả 0 là lượt ấy "đạt", và bằng chứng của nó vẫn tái dùng
    được, dù cây tiến trình còn sống và khoá đã bị nhả. "Khoá mà nhả trong lúc thứ
    nó bảo vệ còn sống thì không phải khoá" — nên nó phải làm đỏ cả hai đường:

      (a) ĐƯỜNG CHẠY: mã thoát `EXIT_GIET_KHONG_TRON_VEN`, `status: fail`;
      (b) ĐƯỜNG TÁI DÙNG: `validate` từ chối, `mismatches` có `giet_tron_ven`.

    Dùng mối nối `TL_GATE_EP_BAO_RO` để ÉP BÁO rò (vẫn giết thật). Nhánh này chỉ
    tự nhiên xảy ra khi `cgroup.kill` không hội tụ trong hạn, tức không dựng lại
    được theo ý muốn — mà một nhánh không thể đỏ thì lời khai về nó là lời khai
    sai về độ phủ, đúng lỗi kho đã ghi sổ.
    """
    if os.name == "nt":
        print("  BO QUA case_don_khong_tron_ven_lam_do_luot_gate: fixture POSIX")
        return
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_ro_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        moi_truong = dict(os.environ)
        moi_truong["TL_GATE_EP_BAO_RO"] = "1"
        moi_truong.pop("TL_GATE_TAT_CGROUP", None)
        argv = [
            "run", "--kind", "heavy", "--name", "fixture", "--repo", str(repo),
            "--evidence", str(evidence), "--output", str(evidence.with_suffix(".out")),
            "--wait-seconds", "1.0", "--timeout-seconds", "30",
            "--selected-test", "fixture",
            "--expected-head", head, "--base-sha", head, "--require-clean",
            "--", sys.executable, "-c", "print('1/1 ok')",
        ]
        ran = subprocess.run([sys.executable, str(RUNNER), *argv], cwd=repo,
                             text=True, capture_output=True, timeout=60, env=moi_truong)
        ban_ghi = json.loads(evidence.read_text(encoding="utf-8"))

        # Chỉ có nghĩa khi cơ chế THẬT là cgroup; máy không cấp được thì mối nối
        # không nằm trên đường chạy và ca này không đo được gì — nói thẳng ra.
        if ban_ghi.get("co_che_cach_ly") != "cgroup2":
            print("  BO QUA case_don_khong_tron_ven_lam_do_luot_gate: may khong cap duoc cgroup")
            return

        assert ban_ghi.get("giet_tron_ven") is False, (
            "ep bao ro ma ban ghi van khai giet_tron_ven=%r" % (ban_ghi.get("giet_tron_ven"),)
        )
        # Lệnh gate TỰ NÓ trả 0 — cái làm đỏ lượt phải là lượt dọn, không phải lệnh.
        assert ran.returncode != 0, (
            "lenh gate tra 0 va luot don RO ma gate van thoat 0 — fail-close chua co rang"
        )
        assert ban_ghi.get("status") == "fail", "status=%r" % (ban_ghi.get("status"),)
        assert ban_ghi.get("returncode") == 4, "returncode=%r" % (ban_ghi.get("returncode"),)


def case_vao_cgroup_hong_thi_tut_ve_quet_cay_va_khai_dung() -> None:
    """Vào cgroup hỏng lúc `fork` ⇒ vẫn chạy được, nhưng KHAI ĐÚNG là `quet-cay`.

    `preexec_fn` ném thì Python gói lại thành `SubprocessError` chứ KHÔNG phải
    `OSError` (đo được) — mà khối bắt lỗi sinh con của runner chỉ bắt `OSError`.
    Không có nhánh này thì một lần cgroup trục trặc là runner ném ra ngoài và MẤT
    LUÔN tệp bằng chứng, tức hỏng nặng hơn hẳn việc không có cgroup.

    Hai vế phải đi cùng nhau: chạy tiếp được, VÀ khai đúng đường đã chạy. Chạy
    tiếp mà vẫn khai `cgroup2` thì bản ghi nói dối về vùng chứa không tồn tại.
    """
    if os.name == "nt":
        print("  BO QUA case_vao_cgroup_hong_thi_tut_ve_quet_cay_va_khai_dung: fixture POSIX")
        return
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_hong_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        moi_truong = dict(os.environ)
        moi_truong["TL_GATE_EP_HONG_VAO_CGROUP"] = "1"
        moi_truong.pop("TL_GATE_TAT_CGROUP", None)
        argv = [
            "run", "--kind", "heavy", "--name", "fixture", "--repo", str(repo),
            "--evidence", str(evidence), "--output", str(evidence.with_suffix(".out")),
            "--wait-seconds", "1.0", "--timeout-seconds", "30",
            "--selected-test", "fixture",
            "--expected-head", head, "--base-sha", head, "--require-clean",
            "--", sys.executable, "-c", "print('1/1 ok')",
        ]
        ran = subprocess.run([sys.executable, str(RUNNER), *argv], cwd=repo,
                             text=True, capture_output=True, timeout=60, env=moi_truong)
        assert evidence.is_file(), (
            "vao cgroup hong lam MAT tep bang chung: %s" % (ran.stderr[-400:],)
        )
        ban_ghi = json.loads(evidence.read_text(encoding="utf-8"))
        assert ran.returncode == 0, "gate khong chay tiep duoc: %s" % (ran.stderr[-400:],)
        assert ban_ghi.get("status") == "pass", "status=%r" % (ban_ghi.get("status"),)
        assert ban_ghi.get("co_che_cach_ly") == "quet-cay", (
            "vao cgroup hong ma van khai co_che_cach_ly=%r" % (ban_ghi.get("co_che_cach_ly"),)
        )


def case_gate_dat_ma_bo_lai_daemon_van_bi_don_va_khai() -> None:
    """Gate ĐẠT nhưng bỏ lại daemon ⇒ vẫn phải dọn, và phải KHAI là đã dọn mấy đứa.

    Đường quét cây KHÔNG làm nổi việc này và cũng chưa từng thử: `_terminate_process_tree`
    chỉ chạy ở đường huỷ/quá hạn, nên một lượt gate trả 0 mà bỏ lại daemon thì
    khoá vẫn được nhả trong lúc daemon còn ghi vào kho — cùng một lỗi với ca huỷ,
    chỉ khác lối vào. Có vùng chứa thì dọn được, nên dọn.

    Và phải KHAI: giết lặng lẽ thì "gate này bỏ lại 3 tiến trình" biến mất khỏi
    bản ghi, mà đó đúng là thứ người đọc cần để biết lệnh gate của mình bẩn.
    """
    if os.name == "nt":
        print("  BO QUA case_gate_dat_ma_bo_lai_daemon_van_bi_don_va_khai: fixture POSIX")
        return
    with tempfile.TemporaryDirectory(prefix="gate_lifecycle_daemon_") as raw:
        root = Path(raw)
        repo = root / "repo"
        repo.mkdir()
        head, _ = _repo(repo)
        evidence = root / "evidence.json"
        con_song = root / "daemon-con-song"
        # Daemon tách nhóm, ngủ tới MỐC TUYỆT ĐỐI rồi ghi dấu. Mốc nằm sau khi
        # runner đã thoát hẳn, nên ghi được dấu ⇔ nó thoát khỏi lượt dọn.
        moc = time.time() + 12.0
        daemon = (
            "import os,time\n"
            "os.setsid()\n"
            f"time.sleep(max(0.0,{str(moc)!r} and float({str(moc)!r})-time.time()))\n"
            f"open({str(con_song)!r},'w').write('song')\n"
        )
        lenh = (
            "import subprocess,sys,time;"
            f"subprocess.Popen([sys.executable,'-c',{daemon!r}],"
            "stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True);"
            "time.sleep(1);"
            "print('1/1 ok')"
        )
        argv = [
            "run", "--kind", "heavy", "--name", "fixture", "--repo", str(repo),
            "--evidence", str(evidence), "--output", str(evidence.with_suffix(".out")),
            "--wait-seconds", "1.0", "--timeout-seconds", "30",
            "--selected-test", "fixture",
            "--expected-head", head, "--base-sha", head, "--require-clean",
            "--", sys.executable, "-c", lenh,
        ]
        ran = subprocess.run([sys.executable, str(RUNNER), *argv], cwd=repo,
                             text=True, capture_output=True, timeout=90)
        ban_ghi = json.loads(evidence.read_text(encoding="utf-8"))
        if ban_ghi.get("co_che_cach_ly") != "cgroup2":
            print("  BO QUA case_gate_dat_ma_bo_lai_daemon_van_bi_don_va_khai: khong co vung chua")
            return

        assert ran.returncode == 0, "lenh gate dat ma gate tra %r" % (ran.returncode,)
        assert ban_ghi.get("status") == "pass", "status=%r" % (ban_ghi.get("status"),)
        # KHAI: đã dọn ít nhất một đứa (chính con daemon kia).
        assert (ban_ghi.get("so_sot_da_don") or 0) >= 1, (
            "gate bo lai daemon ma khai so_sot_da_don=%r" % (ban_ghi.get("so_sot_da_don"),)
        )
        while time.time() < moc + 2.0:
            time.sleep(0.2)
        assert not con_song.exists(), "daemon song sot sau khi gate DAT va nha khoa"


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

        # FAIL-CLOSE Ở ĐƯỜNG TÁI DÙNG: bản ghi khai dọn KHÔNG trọn vẹn thì không
        # được tái dùng, dù mọi trường danh tính khác khớp hoàn hảo. Đây là lưới
        # thứ hai dưới `EXIT_GIET_KHONG_TRON_VEN`: bản ghi CŨ (sinh trước bản này)
        # hoặc bản ghi bị sửa tay vẫn phải bị chặn ở đây.
        ro = json.loads(evidence.read_text(encoding="utf-8"))
        ro["giet_tron_ven"] = False
        evidence_ro = evidence.with_name("evidence-ro.json")
        evidence_ro.write_text(json.dumps(ro), encoding="utf-8")
        tu_choi = _run(
            [
                "validate",
                "--evidence",
                str(evidence_ro),
                "--output",
                str(evidence.with_suffix(".out")),
                "--expected-head",
                head,
                *envelope,
            ],
            cwd=repo,
        )
        assert tu_choi.returncode == 3, tu_choi.stdout
        assert "giet_tron_ven" in json.loads(tu_choi.stdout)["mismatches"], tu_choi.stdout

        # VÀ VẮNG MẶT KHÔNG PHẢI FALSE: bản ghi cũ hơn trường này (không có khoá)
        # vẫn phải tái dùng được, nếu không thì mọi bằng chứng cũ chết oan. "Vắng
        # mặt vì chưa có" khác "khai thẳng là rò" — không được nhập làm một.
        vang = json.loads(evidence.read_text(encoding="utf-8"))
        vang.pop("giet_tron_ven", None)
        evidence_vang = evidence.with_name("evidence-vang.json")
        evidence_vang.write_text(json.dumps(vang), encoding="utf-8")
        van_dung = _run(
            [
                "validate",
                "--evidence",
                str(evidence_vang),
                "--output",
                str(evidence.with_suffix(".out")),
                "--expected-head",
                head,
                *envelope,
            ],
            cwd=repo,
        )
        assert van_dung.returncode == 0, van_dung.stdout
        assert json.loads(van_dung.stdout)["reusable"] is True, van_dung.stdout

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
    case_descendant_spawned_during_shutdown_is_contained,
    case_ke_de_lai_lien_tuc_khong_thoat_duoc,
    case_co_che_cach_ly_khai_dung_thu_da_chay,
    case_don_khong_tron_ven_lam_do_luot_gate,
    case_vao_cgroup_hong_thi_tut_ve_quet_cay_va_khai_dung,
    case_gate_dat_ma_bo_lai_daemon_van_bi_don_va_khai,
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
