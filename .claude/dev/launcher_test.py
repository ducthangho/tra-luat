#!/usr/bin/env python3
"""launcher_test.py — phản chứng cho launcher.py.

Nguyên tắc (cùng doctrine với packet_loop_test.py): một chốt chỉ TỒN TẠI nếu có
trường hợp làm nó ĐỎ. Mỗi ca dưới đây neo đúng một hành vi, gọi qua CLI thật
(subprocess) chứ không import — seam là dòng lệnh, vì đó là thứ phiên khác,
điện thoại và remote thực sự gọi.

Chạy:  python .claude/dev/launcher_test.py             (chạy tất cả; Windows KHÔNG có python3)
       python3 .claude/dev/launcher_test.py --dot-bien (tự đột biến: chứng minh có răng)
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import errno
import hashlib
import hmac
import importlib.util
import io
import json
import os
import platform
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

LAUNCHER = Path(__file__).resolve().parent / "launcher.py"
CODEX_ENV_POLICY = Path(__file__).resolve().parent / "codex_env_policy.py"
PY = sys.executable or "python3"
LA_WINDOWS = platform.system() == "Windows"

# wp484 g7 — bộ test phải KÍN với credential của phiên đang chạy. Từ #509, `launcher.py run`
# và bridge phiên khôi phục `CODEX_AUTH_JSON` TRƯỚC mọi child, nên mọi ca chép `os.environ`
# xuống tiến trình con đều mang biến ấy theo. Đo 16-17-10 (`--lap-ca`, cùng biến giả):
# `t158` master XANH, g7 ĐỎ rc=13; cả bộ: 68 ca đỏ với biến giả, 3 ca đỏ (t124–t126) với
# credential THẬT — tức bộ test đã đem credential thật đi materialize. Ca nào cần biến thì
# tự đặt tường minh (patch.dict / env=…), không ca nào được thừa hưởng từ phiên.
os.environ.pop("CODEX_AUTH_JSON", None)

MA_OK, MA_THAM_SO, MA_GIT, MA_HEAD, MA_REF = 0, 2, 3, 4, 5
MA_BAN, MA_PROMPT, MA_HAN, MA_VA_CHAM, MA_DANH_TINH, MA_QUA_HAN = 6, 7, 8, 9, 10, 124
MA_WORKTREE, MA_PROBE = 14, 15

CA: list = []


def kiem_registry(ds):
    """#1079 F05/F08 (Codex lượt 4–6): bộ chấm nhận diện "ca khác" theo `__code__`, nên hai ca chung
    `__code__` (cùng factory) là bất khả phân biệt — TỪ CHỐI. Gọi ở `ca` và ở các điểm vào chạy ca
    đã biết: `chay_dot_bien` (nhánh hook gọi thẳng `fn()`), `cham_mot_ca`, `chay_bo_ca` (TRƯỚC thân ca;
    `main` đi qua hai hàm này nên không cần chốt riêng) và `chot_tu_ca_khac`,
    vì `CA` còn có thể bị GÁN THẲNG, không qua `ca`. Gọi thẳng `fn()` ở chỗ khác thì KHÔNG được che."""
    trung = [c.__name__ for i, c in enumerate(ds) if any(c.__code__ is d.__code__ for d in ds[:i])]
    if trung:
        raise ValueError(f"CA co ca trung __code__ voi mot ca da dang ky: {trung} — dung ham rieng")


def ca(fn):
    kiem_registry([*CA, fn])
    CA.append(fn)
    return fn


# ------------------------------------------------------------------ khung chạy

# Đường dẫn launcher THỰC SỰ được gọi. Chế độ đột biến trỏ biến này sang một bản
# sao tạm; tệp trong kho không bao giờ bị ghi (xem chay_dot_bien).
LAUNCHER_DANG_DUNG = LAUNCHER


def chay(*doi_so, cwd=None, env=None) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(LAUNCHER_DANG_DUNG), *doi_so], capture_output=True,
                          text=True, encoding="utf-8", errors="replace", cwd=cwd, env=env)


def _bo_qua_neu_ban_sao_roi_thieu(*duong: Path, goc_kho: Path | None = None) -> str | None:
    """Chỉ tha fixture ngoài `dev/` khi cây thật sự là bản sao rời.

    Trong checkout/worktree thật, `.git` ở gốc tương ứng luôn có mặt (tệp hoặc thư
    mục). Thiếu fixture ở cây ấy là regression và ca phải tiếp tục chạy để ĐỎ.
    """
    goc = goc_kho or Path(__file__).resolve().parents[2]
    thieu = [p for p in duong if not p.is_file()]
    if thieu and not (goc / ".git").exists():
        return ("bo qua ban sao roi (goc khong co .git; thieu fixture: "
                + ", ".join(str(p) for p in thieu) + ")")
    return None


def tao_repo(goc: Path, ten="repo", ban=False) -> Path:
    """Repo git thật, ép tắt gpgsign và hooksPath.

    Cả hai đều làm `git commit` hỏng theo cấu hình toàn cục của máy chạy test —
    đã hỏng thật trên máy người dùng, nên test không được phụ thuộc vào chúng.
    """
    d = goc / ten
    d.mkdir(parents=True)
    hooks = goc / "hooks_rong"
    hooks.mkdir(exist_ok=True)
    g = ["git", "-C", str(d), "-c", "user.email=t@e.invalid", "-c", "user.name=t",
         "-c", "commit.gpgsign=false", "-c", f"core.hooksPath={hooks}"]
    subprocess.run(["git", "init", "-b", "main", str(d)], capture_output=True)
    (d / "a.txt").write_text("x", encoding="utf-8")
    subprocess.run(g + ["add", "-A"], capture_output=True)
    subprocess.run(g + ["commit", "-m", "seed"], capture_output=True)
    if ban:
        (d / "ban.txt").write_text("chua theo doi", encoding="utf-8")
    return d


def tao_worktree(goc: Path) -> Path:
    repo = tao_repo(goc, "clone-goc")
    wt = goc / "worktree"
    p = subprocess.run(["git", "-C", str(repo), "worktree", "add", "-b", "fixture-wt", str(wt)],
                       capture_output=True, text=True)
    bang(p.returncode == 0 and (wt / ".git").is_file(), f"khong tao duoc worktree: {p.stderr}")
    return wt


def tao_claude_gia(goc: Path) -> Path:
    dich = goc / ("claude.exe" if LA_WINDOWS else "claude")
    try:
        os.link(Path(PY).resolve(), dich)
    except OSError:
        shutil.copy2(Path(PY).resolve(), dich)
    if not LA_WINDOWS:
        dich.chmod(0o755)
    return dich


def head_cua(d: Path) -> str:
    p = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"],
                       capture_output=True, text=True)
    return p.stdout.strip()


def mai_sau(giay=3600) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=giay)).isoformat()


def khi_truoc(giay=3600) -> str:
    return (datetime.now(timezone.utc) - timedelta(seconds=giay)).isoformat()


class San:
    """Sân chơi tạm, tự dọn."""

    def __enter__(self):
        self.d = Path(tempfile.mkdtemp(prefix="lt_"))
        return self.d

    def __exit__(self, *a):
        shutil.rmtree(self.d, ignore_errors=True)


class TinHieuChotCa(AssertionError):
    """Tín hiệu ngoại lệ riêng của chốt test trong harness, ngăn tín dụng giả khi đột biến."""
    pass


def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise TinHieuChotCa(thong_diep)


def chot_tu_ca_khac(e, fn):
    """#1079 F05 (Codex lượt 2): tín hiệu sinh ra BÊN TRONG một ca đã đăng ký KHÁC (ca đích gọi
    sang nó) không phải chốt của ca đích. Dò từng khung traceback theo `__code__` của `CA`."""
    kiem_registry(CA)
    khac = {c.__code__ for c in CA if c is not fn}
    tb = e.__traceback__
    while tb is not None:
        if tb.tb_frame.f_code in khac:
            return True
        tb = tb.tb_next
    return False


TRAN_THONG_DIEP_LOI = 160


def mo_ta_loi(e) -> str:
    """#1122: `<Loại>: <thông điệp cắt TRAN_THONG_DIEP_LOI ký tự>`, hoặc chỉ `<Loại>` khi thông điệp rỗng.
    Trước đây chi tiết `loi` chỉ mang tên loại, nên `t73(TypeError)` trên lane Windows (run 41322980509) không
    chẩn đoán được từ log."""
    tin = str(e)
    return f"{type(e).__name__}: {tin[:TRAN_THONG_DIEP_LOI]}" if tin else type(e).__name__


def cham_mot_ca(fn):
    """#1079 F01: chạy một ca, trả `(loai, chi_tiet)`; loai ∈ qua · bo_qua · giet · loi.
    CHỈ `TinHieuChotCa` là `giet` — AssertionError trần hay lỗi vô can (kể cả khi một `except`
    đã đổi kiểu sang AssertionError) là `loi`, tức tín dụng giả."""
    kiem_registry(CA)   # #1079 F08 (Codex lượt 6): TRƯỚC khi thân ca chạy
    try:
        with _co_lap_toan_cuc():
            kq = fn()
    except TinHieuChotCa as e:
        if not chot_tu_ca_khac(e, fn):
            return "giet", fn.__name__
        return "loi", f"{fn.__name__}(chot cua ca khac)"
    except Exception as e:  # noqa: BLE001 - chinh la thu dang phan hang
        return "loi", f"{fn.__name__}({mo_ta_loi(e)})"
    return ("bo_qua" if isinstance(kq, str) else "qua"), fn.__name__


def ket_luan_mutant(dich, neutral, mutant):
    """#1079 F01 — thuần. `neutral`/`mutant`: tên ca → `(loai, chi_tiet)`.
    Trả `(trang_thai, so_chet, can_do, mo_ta)`; trang_thai ∈ OK · SAI · KHONG_DO (ca đích bỏ qua
    theo nền) · KHONG_DO_NEUTRAL (neutral không qua ⇒ tính hỏng, KHÔNG cấp tín dụng)."""
    xau = [neutral[t][1] for t in dich if neutral[t][0] in ("giet", "loi")]
    if xau:
        return "KHONG_DO_NEUTRAL", 0, 0, ", ".join(xau)
    bo_qua = [t for t in dich if "bo_qua" in (neutral[t][0], mutant[t][0])]
    can_do = len(dich) - len(bo_qua)
    chet = [mutant[t][1] for t in dich if t not in bo_qua and mutant[t][0] == "giet"]
    gia = [mutant[t][1] for t in dich if t not in bo_qua and mutant[t][0] == "loi"]
    if can_do == 0:
        return "KHONG_DO", 0, 0, ", ".join(bo_qua)
    mo_ta = ", ".join(chet) or "(khong ca nao chet)"
    if gia:
        mo_ta += f" [tin dung gia: {', '.join(gia)}]"
    if bo_qua:
        mo_ta += f" [bo qua: {', '.join(bo_qua)}]"
    return ("OK" if len(chet) == can_do else "SAI"), len(chet), can_do, mo_ta


def _con_song_that(pid: int) -> bool:
    """Còn sống THẬT — zombie tính là ĐÃ CHẾT.

    Bộ test phải hỏi độc lập với launcher (không import nó, kể cả khi đang chạy
    bản đột biến), nhưng vẫn phải đúng cái luật mà launcher dùng: `os.kill(pid,0)`
    thành công với cả zombie, nên chỉ dùng nó là báo "còn sống" cho tiến trình đã
    chết hẳn.
    """
    st = Path(f"/proc/{pid}/stat")
    if st.exists():
        try:
            # wp685 (Q-A.7, §6 mục 3): đọc BYTES — read_text() báo "đã chết" cho tiến trình sống có comm hỏng
            nd = st.read_bytes()
            return nd[nd.rindex(b")") + 2:].split()[0] != b"Z"
        except (OSError, ValueError, IndexError):
            return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    if platform.system() == "Darwin":
        p = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)],
                           capture_output=True, text=True)
        return not p.stdout.strip().startswith("Z")
    return True


def _nap_sach(duong):
    """Nạp một tệp `.py` và ĐẢM BẢO chạy đúng NỘI DUNG ĐANG CÓ TRÊN ĐĨA.

    ĐÃ ĐO (cross-review lượt 6, truy nguyên P1 `cong-dot-bien-do-luot-1`): bản trước
    chỉ gọi thẳng `exec_module`, và cổng đột biến ĐÃ CHẤM ĐIỂM NHẦM BẢN.

    Cơ chế, đo được bằng A/B: CPython coi một `.pyc` là còn hợp lệ khi (mtime nguồn
    tính theo GIÂY, kích thước nguồn) khớp với đầu tệp `.pyc`. Runner đột biến ghi
    MỌI bản sao vào CÙNG một đường dẫn. Mutation #3 (`bo_loc_do_dai…`) và #4
    (`do_codex_tin_DONG_DAU…`) tình cờ ra tệp CÙNG 129395 byte; khi hai lượt ghi rơi
    vào CÙNG MỘT GIÂY thì bản #4 KHÔNG BAO GIỜ được biên dịch — Python phục vụ lại
    mã của #3. Kết quả: mutant #4 báo `giet 0/1` "sống sót" mà nó chưa hề được chạy.
    Bật `sys.dont_write_bytecode` rồi chạy lại: `giet 1/1`. Đó là toàn bộ bằng chứng.
    Chạy tay một mình cũng `1/1` — nên ba lượt trước tôi "chứng minh số của mình
    đúng" bằng cách vô tình chạy nó ở dạng KHÔNG dính lỗi.

    Đây cũng là lời giải cho câu "một cổng cho kết quả phụ thuộc nơi chạy": va chạm
    chỉ xảy ra khi HAI lượt ghi lọt cùng một giây, mà điều đó phụ thuộc ca test ở
    giữa chạy nhanh hay chậm — tức phụ thuộc MÁY. Không phải ai đo sai; là cổng đo
    một thứ không phải mã của nó.

    Ba lớp, độc lập nhau (một lớp hỏng thì lớp kia vẫn chặn):
      1. xoá `.pyc` tương ứng nếu có — bịt cả bản cũ còn sót từ LƯỢT CHẠY TRƯỚC,
         thứ mà tắt ghi bytecode KHÔNG cứu được (tắt ghi ≠ tắt đọc);
      2. tắt ghi bytecode trong lúc nạp — không sinh thêm bản cache để va chạm;
      3. `invalidate_caches()` — bỏ bộ nhớ đệm mục lục thư mục của importlib.
    Runner còn đặt TÊN TỆP KHÁC NHAU cho từng đột biến, là lớp thứ tư ở phía nó.
    """
    duong = Path(duong)
    try:
        pyc = Path(importlib.util.cache_from_source(str(duong)))
        if pyc.exists():
            pyc.unlink()
    except (OSError, ValueError, NotImplementedError):
        pass                        # không xoá được thì còn hai lớp kia
    truoc = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        importlib.invalidate_caches()
        ten = f"launcher_thu_{time.time_ns()}"
        sp = importlib.util.spec_from_file_location(ten, duong)
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m
    finally:
        sys.dont_write_bytecode = truoc


def _tai_launcher_thu():
    """Nạp đúng bản launcher đang thử (kể cả bản sao đột biến)."""
    return _nap_sach(LAUNCHER_DANG_DUNG)


# ------------------------------------------------------------- chốt: workspace

@ca
def t01_workspace_khong_phai_repo():
    with San() as s:
        (s / "tron").mkdir()
        r = chay("check", "--workspace", str(s / "tron"))
        bang(r.returncode == MA_GIT, f"mong doi {MA_GIT}, duoc {r.returncode}: {r.stderr}")


@ca
def t02_workspace_khong_ton_tai():
    with San() as s:
        r = chay("check", "--workspace", str(s / "khong-co"))
        bang(r.returncode == MA_THAM_SO, f"mong doi {MA_THAM_SO}, duoc {r.returncode}")


@ca
def t03_git_gia_thoat_0_im_lang_van_bi_chan():
    """Ca .Count: git trả rc=0 nhưng KHÔNG in gì.

    Đây là ca duy nhất phân biệt "kiểm rc" với "kiểm cả nội dung". Bỏ nó thì một
    wrapper git hỏng sẽ đưa chuỗi rỗng đi tiếp và mọi chốt phía sau so với rỗng.
    """
    if LA_WINDOWS:
        return "bo qua tren Windows (can shim .cmd)"
    with San() as s:
        repo = tao_repo(s)
        binh = s / "bin"
        binh.mkdir()
        gia = binh / "git"
        gia.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        gia.chmod(0o755)
        env = dict(os.environ, PATH=f"{binh}{os.pathsep}{os.environ.get('PATH', '')}")
        r = chay("check", "--workspace", str(repo), env=env)
        bang(r.returncode == MA_GIT, f"mong doi {MA_GIT}, duoc {r.returncode}: {r.stdout}{r.stderr}")


@ca
def t04_duong_dan_co_dau_tieng_viet():
    """Chính là chỗ bản PowerShell gãy: `git -C 'D:\\Quốc hội\\...'` bị méo mã.

    Ở đây phải QUA, vì subprocess truyền đối số dạng list (Windows: CreateProcessW).
    """
    with San() as s:
        repo = tao_repo(s, ten="Quốc hội - kho")
        r = chay("check", "--workspace", str(repo), "--expected-head", head_cua(repo))
        bang(r.returncode == MA_OK, f"duong dan co dau bi chan: {r.returncode} {r.stderr}")


# ------------------------------------------------------------------ chốt: HEAD/ref

@ca
def t05_head_khop():
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--workspace", str(repo), "--expected-head", head_cua(repo))
        bang(r.returncode == MA_OK, f"{r.returncode}: {r.stderr}")


@ca
def t06_head_lech_bi_chan():
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--workspace", str(repo), "--expected-head", "b" * 40)
        bang(r.returncode == MA_HEAD, f"mong doi {MA_HEAD}, duoc {r.returncode}")


@ca
def t07_head_hoa_thuong_van_khop():
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--workspace", str(repo), "--expected-head", head_cua(repo).upper())
        bang(r.returncode == MA_OK, f"HEAD viet hoa bi coi la lech: {r.returncode}")


@ca
def t08_ref_lech_bi_chan():
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--workspace", str(repo), "--expected-ref", "khong-co-nhanh-nay")
        bang(r.returncode == MA_REF, f"mong doi {MA_REF}, duoc {r.returncode}")


@ca
def t09_ref_khop():
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--workspace", str(repo), "--expected-ref", "main")
        bang(r.returncode == MA_OK, f"{r.returncode}: {r.stderr}")


# --------------------------------------------------------------- chốt: worktree

@ca
def t10_worktree_ban_bi_chan_khi_doi_sach():
    with San() as s:
        repo = tao_repo(s, ban=True)
        r = chay("check", "--workspace", str(repo), "--require-clean")
        bang(r.returncode == MA_BAN, f"mong doi {MA_BAN}, duoc {r.returncode}")


@ca
def t11_worktree_ban_van_qua_khi_khong_doi():
    with San() as s:
        repo = tao_repo(s, ban=True)
        r = chay("check", "--workspace", str(repo))
        bang(r.returncode == MA_OK, f"khong doi sach ma van chan: {r.returncode}")


@ca
def t12_tep_khong_theo_doi_van_tinh_la_ban():
    """--untracked-files=all: một tệp mới toanh vẫn là bẩn.

    Bỏ cờ đó thì `git status --porcelain` im lặng với tệp chưa theo dõi và chốt
    "worktree sạch" xanh trong khi có tệp lạ nằm đó.
    """
    with San() as s:
        repo = tao_repo(s)
        (repo / "la.txt").write_text("moi", encoding="utf-8")
        r = chay("check", "--workspace", str(repo), "--require-clean")
        bang(r.returncode == MA_BAN, f"tep chua theo doi khong bi tinh la ban: {r.returncode}")


# ----------------------------------------------------------------- chốt: prompt

@ca
def t13_prompt_khop():
    with San() as s:
        repo = tao_repo(s)
        p = s / "prompt.txt"
        p.write_text("noi dung that", encoding="utf-8")
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        r = chay("check", "--workspace", str(repo), "--prompt-file", str(p),
                 "--expected-prompt-sha256", sha)
        bang(r.returncode == MA_OK, f"{r.returncode}: {r.stderr}")


@ca
def t14_prompt_lech_bi_chan():
    with San() as s:
        repo = tao_repo(s)
        p = s / "prompt.txt"
        p.write_text("noi dung that", encoding="utf-8")
        r = chay("check", "--workspace", str(repo), "--prompt-file", str(p),
                 "--expected-prompt-sha256", "a" * 64)
        bang(r.returncode == MA_PROMPT, f"mong doi {MA_PROMPT}, duoc {r.returncode}")


@ca
def t15_prompt_rong_bi_chan_du_sha_dung():
    """Tệp rỗng vẫn có sha256 hợp lệ — chỉ so sha thì lượt chạy vô nghĩa vẫn qua."""
    with San() as s:
        repo = tao_repo(s)
        p = s / "prompt.txt"
        p.write_bytes(b"")
        sha = hashlib.sha256(b"").hexdigest()
        r = chay("check", "--workspace", str(repo), "--prompt-file", str(p),
                 "--expected-prompt-sha256", sha)
        bang(r.returncode == MA_PROMPT, f"prompt RONG ma van qua: {r.returncode}")


@ca
def t16_prompt_thieu_tep():
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--workspace", str(repo), "--prompt-file", str(s / "khong-co.txt"),
                 "--expected-prompt-sha256", "a" * 64)
        bang(r.returncode == MA_PROMPT, f"mong doi {MA_PROMPT}, duoc {r.returncode}")


@ca
def t17_prompt_thieu_mot_nua_la_loi_tham_so():
    with San() as s:
        repo = tao_repo(s)
        p = s / "prompt.txt"
        p.write_text("x", encoding="utf-8")
        r = chay("check", "--workspace", str(repo), "--prompt-file", str(p))
        bang(r.returncode == MA_THAM_SO, f"mong doi {MA_THAM_SO}, duoc {r.returncode}")


@ca
def t18_prompt_utf8_tinh_sha_theo_BYTE():
    """sha256 phải tính trên BYTE, không qua giải mã văn bản.

    Nếu tính sau khi decode thì cùng nội dung ở hai encoding cho hai kết quả, và
    neo prompt hết ý nghĩa với văn bản tiếng Việt.
    """
    with San() as s:
        repo = tao_repo(s)
        p = s / "prompt.txt"
        p.write_bytes("Điều 1. Phạm vi điều chỉnh\n".encode("utf-8"))
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        r = chay("check", "--workspace", str(repo), "--prompt-file", str(p),
                 "--expected-prompt-sha256", sha)
        bang(r.returncode == MA_OK, f"{r.returncode}: {r.stderr}")


# --------------------------------------------------------------- chốt: hạn chót

@ca
def t19_han_da_qua_bi_chan():
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--workspace", str(repo), "--deadline-utc", khi_truoc())
        bang(r.returncode == MA_HAN, f"mong doi {MA_HAN}, duoc {r.returncode}")


@ca
def t20_han_tuong_lai_qua_duoc():
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--workspace", str(repo), "--deadline-utc", mai_sau())
        bang(r.returncode == MA_OK, f"{r.returncode}: {r.stderr}")


@ca
def t21_han_khong_doc_duoc_la_loi_tham_so():
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--workspace", str(repo), "--deadline-utc", "hom qua")
        bang(r.returncode == MA_THAM_SO, f"mong doi {MA_THAM_SO}, duoc {r.returncode}")


@ca
def t22_han_thieu_mui_gio_coi_la_UTC():
    """Thiếu múi giờ mà đoán theo giờ máy thì cùng một chuỗi cho hai kết quả khác
    nhau ở máy người dùng và ở phiên remote. Quy ước: coi là UTC."""
    with San() as s:
        repo = tao_repo(s)
        khong_mui = (datetime.now(timezone.utc) - timedelta(hours=1)).replace(tzinfo=None).isoformat()
        r = chay("check", "--workspace", str(repo), "--deadline-utc", khong_mui)
        bang(r.returncode == MA_HAN, f"han qua khu thieu mui gio khong bi chan: {r.returncode}")


# -------------------------------------------------------------------- lệnh run

@ca
def t23_run_truyen_lai_ma_thoat():
    with San() as s:
        repo = tao_repo(s)
        r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"),
                 "--name", "thu", "--", PY, "-c", "import sys; sys.exit(7)")
        bang(r.returncode == 7, f"ma thoat cua lenh con khong duoc truyen lai: {r.returncode}")


@ca
def t24_run_chan_TRUOC_khi_goi_lenh():
    """HEAD lệch thì KHÔNG được chạy lệnh. Chốt chạy sau lệnh là chốt vô dụng."""
    with San() as s:
        repo = tao_repo(s)
        dau = s / "da-chay.txt"
        r = chay("run", "--workspace", str(repo), "--expected-head", "b" * 40,
                 "--run-root", str(s / "runs"), "--",
                 PY, "-c", f"open({str(dau)!r}, 'w').write('x')")
        bang(r.returncode == MA_HEAD, f"mong doi {MA_HEAD}, duoc {r.returncode}")
        bang(not dau.exists(), "lenh VAN chay du chot da chan - chot dat sai cho")


@ca
def t25_run_ghi_so_doc_duoc():
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--name", "abc", "--", PY, "-c", "print('xong')")
        bang(r.returncode == 0, f"{r.returncode}: {r.stderr}")
        so = list(rr.iterdir())
        bang(len(so) == 1, f"mong doi 1 luot, co {len(so)}")
        d = json.loads((so[0] / "run.json").read_text(encoding="utf-8"))
        bang(d["ten"] == "abc", "ten khong duoc ghi")
        bang(d["trang_thai"] == "xong", f"trang thai la {d['trang_thai']}")
        bang(len(d["short_id"]) == 8, "short_id phai 8 ky tu")
        bang((so[0] / "stdout.log").read_text(encoding="utf-8").strip() == "xong",
             "stdout khong duoc luu")


@ca
def t26_short_id_don_nhat():
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        thay = set()
        for _ in range(6):
            chay("run", "--workspace", str(repo), "--run-root", str(rr), "--",
                 PY, "-c", "pass")
        for p in rr.iterdir():
            sid = p.name.split("-", 1)[0]
            bang(sid not in thay, f"short_id trung: {sid}")
            thay.add(sid)
        bang(len(thay) == 6, f"mong doi 6 luot, co {len(thay)}")


@ca
def t27_qua_han_thi_giet_va_tra_124():
    with San() as s:
        repo = tao_repo(s)
        han = (datetime.now(timezone.utc) + timedelta(seconds=2)).isoformat()
        t0 = time.time()
        r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"),
                 "--deadline-utc", han, "--", PY, "-c", "import time; time.sleep(60)")
        mat = time.time() - t0
        bang(r.returncode == MA_QUA_HAN, f"mong doi {MA_QUA_HAN}, duoc {r.returncode}: {r.stderr}")
        bang(mat < 30, f"khong giet dung han: mat {mat:.1f}s")


@ca
def t28_qua_han_giet_ca_CON_CHAU():
    """Giết tiến trình mẹ mà bỏ con cháu là để lại tiến trình mồ côi ghi tiếp
    vào workspace — đúng thứ mà 'chạy tất định' phải ngăn."""
    if LA_WINDOWS:
        return "bo qua tren Windows (can kiem bang cay tien trinh that)"
    with San() as s:
        repo = tao_repo(s)
        dau = s / "chau-con-song.txt"
        # mẹ sinh con rồi tự ngủ; con ghi tệp SAU 6 giây nếu còn sống
        ma_con = (f"import subprocess,sys,time;"
                  f"subprocess.Popen([sys.executable,'-c',"
                  f"\"import time;time.sleep(6);open({str(dau)!r},'w').write('song')\"]);"
                  f"time.sleep(60)")
        han = (datetime.now(timezone.utc) + timedelta(seconds=2)).isoformat()
        r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"),
                 "--deadline-utc", han, "--", PY, "-c", ma_con)
        bang(r.returncode == MA_QUA_HAN, f"mong doi {MA_QUA_HAN}, duoc {r.returncode}")
        time.sleep(8)
        bang(not dau.exists(), "CHAU van song sau khi qua han - khong giet het cay")


@ca
def t29_status_tim_theo_short_id():
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        chay("run", "--workspace", str(repo), "--run-root", str(rr), "--", PY, "-c", "pass")
        sid = next(rr.iterdir()).name.split("-", 1)[0]
        r = chay("status", "--run-root", str(rr), "--id", sid)
        bang(r.returncode == 0, f"{r.returncode}: {r.stderr}")
        bang(json.loads(r.stdout)["short_id"] == sid, "status tra nham luot")


@ca
def t30_status_id_khong_co():
    with San() as s:
        r = chay("status", "--run-root", str(s / "runs"), "--id", "khongco1")
        bang(r.returncode == MA_THAM_SO, f"mong doi {MA_THAM_SO}, duoc {r.returncode}")


@ca
def t31_stop_tu_choi_khi_khoa_danh_tinh_khac():
    """PID tái dùng: sổ ghi PID cũ, tiến trình khác đã chiếm PID đó.

    Fail-closed: thà không giết còn hơn giết nhầm tiến trình vô can.
    """
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        chay("run", "--workspace", str(repo), "--run-root", str(rr), "--", PY, "-c", "pass")
        thu_muc = next(rr.iterdir())
        f = thu_muc / "run.json"
        d = json.loads(f.read_text(encoding="utf-8"))

        # PID phải là tiến trình THẬT nhưng TUYỆT ĐỐI không phải của bộ test.
        # ĐÃ TRẢ GIÁ: bản trước dùng os.getpid(). Chốt còn nguyên thì vô hại vì
        # launcher từ chối; nhưng ở lượt đột biến "giết liều" - đúng lượt cần đo -
        # launcher làm đúng việc nó được bảo và killpg CHÍNH nhóm tiến trình của bộ
        # test. Bộ test tự sát (exit 143), `finally` không chạy, launcher.py ở lại
        # trạng thái đã đột biến và đi thẳng vào commit.
        # Tiến trình mồi nằm ở SESSION RIÊNG nên killpg của nó không chạm tới ai khác.
        them = ({"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if LA_WINDOWS
                else {"start_new_session": True})
        moi = subprocess.Popen([PY, "-c", "import time; time.sleep(30)"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **them)
        try:
            d["pid"] = moi.pid
            d["khoa_danh_tinh"] = "linux:0"   # khoá KHÔNG khớp với tiến trình đó
            f.write_text(json.dumps(d), encoding="utf-8")
            r = chay("stop", "--run-root", str(rr), "--id", d["short_id"])
            bang(r.returncode == MA_DANH_TINH, f"mong doi {MA_DANH_TINH}, duoc {r.returncode}")
            bang("tai dung" in r.stdout or "KHAC" in r.stdout, f"khong noi ro ly do: {r.stdout}")
            # Bằng chứng QUAN SÁT ĐƯỢC, không chỉ là mã thoát: tiến trình vô can
            # phải còn sống. Đây là thứ mà đột biến "giết liều" làm đỏ.
            time.sleep(0.5)
            bang(moi.poll() is None, "tien trinh VO CAN da bi giet du khoa khong khop")
        finally:
            moi.kill()
            try:
                moi.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass


@ca
def t32_stop_tu_choi_khi_khong_co_khoa():
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        chay("run", "--workspace", str(repo), "--run-root", str(rr), "--", PY, "-c", "pass")
        thu_muc = next(rr.iterdir())
        f = thu_muc / "run.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        d["khoa_danh_tinh"] = None
        f.write_text(json.dumps(d), encoding="utf-8")
        r = chay("stop", "--run-root", str(rr), "--id", d["short_id"])
        bang(r.returncode == MA_DANH_TINH, f"mong doi {MA_DANH_TINH}, duoc {r.returncode}")


@ca
def t33_stop_giet_that():
    if LA_WINDOWS:
        return "bo qua tren Windows"
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        pr = subprocess.Popen([PY, str(LAUNCHER_DANG_DUNG), "run", "--workspace", str(repo),
                               "--run-root", str(rr), "--", PY, "-c",
                               "import time; time.sleep(60)"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
        for _ in range(100):
            time.sleep(0.1)
            ds = list(rr.iterdir()) if rr.is_dir() else []
            if ds and (ds[0] / "run.json").is_file():
                d = json.loads((ds[0] / "run.json").read_text(encoding="utf-8"))
                if d.get("pid"):
                    break
        else:
            bang(False, "khong thay pid trong so")
        r = chay("stop", "--run-root", str(rr), "--id", d["short_id"])
        bang(r.returncode == MA_OK, f"stop that bai: {r.returncode} {r.stdout}")
        pr.wait(timeout=30)
        bang(not _con_song(d["pid"]), "tien trinh van song sau stop")


def _con_song(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


@ca
def t34_run_thieu_lenh():
    with San() as s:
        repo = tao_repo(s)
        r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"))
        bang(r.returncode == MA_THAM_SO, f"mong doi {MA_THAM_SO}, duoc {r.returncode}")


@ca
def t35_json_doc_duoc_bang_may():
    """Phiên khác / điện thoại đọc kết quả bằng máy, không bằng mắt."""
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--workspace", str(repo), "--json")
        bang(r.returncode == 0, f"{r.returncode}: {r.stderr}")
        d = json.loads(r.stdout)
        bang(d["ok"] is True and re.match(r"^[0-9a-f]{40}$", d["head"]),
             f"JSON khong dung dang: {r.stdout}")


@ca
def t36_so_ghi_nguyen_tu():
    """run.json phải không bao giờ đọc trúng trạng thái ghi dở."""
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        chay("run", "--workspace", str(repo), "--run-root", str(rr), "--", PY, "-c", "pass")
        thu_muc = next(rr.iterdir())
        bang(not (thu_muc / "run.json.tmp").exists(), "con sot tep tam .tmp")
        json.loads((thu_muc / "run.json").read_text(encoding="utf-8"))


# ------------------------------------- nhận diện kho (đường dẫn KHÔNG mang được sang máy khác)

MA_KHO = 11


def them_remote(d: Path, url: str):
    subprocess.run(["git", "-C", str(d), "remote", "add", "origin", url], capture_output=True)


def commit_goc(d: Path) -> str:
    p = subprocess.run(["git", "-C", str(d), "rev-list", "--max-parents=0", "HEAD"],
                       capture_output=True, text=True)
    return p.stdout.strip().splitlines()[0]


@ca
def t37_khong_can_truyen_workspace():
    """Đứng trong kho là đủ — đường dẫn tuyệt đối không mang sang máy khác được."""
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", cwd=str(repo))
        bang(r.returncode == MA_OK, f"{r.returncode}: {r.stderr}")
        bang(str(repo.resolve()) in r.stdout, f"khong ra dung goc: {r.stdout}")


@ca
def t38_dung_o_thu_muc_CON_van_ra_GOC():
    """Phải hỏi `rev-parse --show-toplevel`, không lấy cwd.

    Lấy cwd thì đứng ở scripts/ sẽ neo nhầm tầng và mọi chốt phía sau đo sai chỗ.
    """
    with San() as s:
        repo = tao_repo(s)
        con = repo / "a" / "b"
        con.mkdir(parents=True)
        r = chay("check", cwd=str(con))
        bang(r.returncode == MA_OK, f"{r.returncode}: {r.stderr}")
        # PHAI resolve ca hai ve. Tren runner windows-latest, thu muc tam o dang
        # 8.3 (C:\Users\RUNNER~1\...) con dau ra da resolve (C:\Users\runneradmin\...)
        # => `str(con) not in r.stdout` LUON dung, ke ca khi launcher tra ve cwd,
        # nen khang dinh nay rong nghia va dot bien lay_cwd_thay_vi_goc_repo thoat.
        bang(str(repo.resolve()) in r.stdout and str(con.resolve()) not in r.stdout,
             f"ra cwd thay vi goc repo: {r.stdout}")


@ca
def t39_bien_moi_truong_TL_WORKSPACE():
    with San() as s:
        repo = tao_repo(s)
        ngoai = s / "ngoai"
        ngoai.mkdir()
        env = dict(os.environ, TL_WORKSPACE=str(repo))
        r = chay("check", cwd=str(ngoai), env=env)
        bang(r.returncode == MA_OK, f"{r.returncode}: {r.stderr}")


@ca
def t40_HAI_BAN_CLONE_hai_duong_dan_CUNG_danh_tinh():
    """Cùng một kho GitHub, clone về hai chỗ khác nhau (hoặc hai máy khác nhau).

    Neo theo đường dẫn thì hỏng ngay khi đổi máy. Neo theo remote + commit gốc thì
    cả hai qua — kể cả khi bản thứ hai dùng URL dạng ssh và nằm ở thư mục có dấu.
    """
    with San() as s:
        a = tao_repo(s, ten="ban-A")
        them_remote(a, "https://github.com/ducthangho/tra-luat.git")
        sha_goc = commit_goc(a)
        b = s / "Tài liệu" / "ban-B"
        b.parent.mkdir(parents=True)
        subprocess.run(["git", "clone", "--quiet", str(a), str(b)], capture_output=True)
        subprocess.run(["git", "-C", str(b), "remote", "set-url", "origin",
                        "git@github.com:ducthangho/tra-luat.git"], capture_output=True)
        for d in (a, b):
            r = chay("check", "--expected-repo", "ducthangho/tra-luat",
                     "--expected-root-commit", sha_goc, cwd=str(d))
            bang(r.returncode == MA_OK, f"{d.name} bi chan: {r.returncode} {r.stderr}")


@ca
def t41_kho_khac_bi_chan():
    with San() as s:
        repo = tao_repo(s)
        them_remote(repo, "https://github.com/nguoi-khac/kho-khac.git")
        r = chay("check", "--expected-repo", "ducthangho/tra-luat", cwd=str(repo))
        bang(r.returncode == MA_KHO, f"mong doi {MA_KHO}, duoc {r.returncode}")


@ca
def t42_khong_co_remote_van_bi_chan_khi_doi_kho():
    """Kho chưa có remote KHÔNG được coi là "khớp vì không biết" — đó là fail-open."""
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--expected-repo", "ducthangho/tra-luat", cwd=str(repo))
        bang(r.returncode == MA_KHO, f"mong doi {MA_KHO}, duoc {r.returncode}")


@ca
def t43_commit_goc_lech_bi_chan():
    with San() as s:
        repo = tao_repo(s)
        r = chay("check", "--expected-root-commit", "c" * 40, cwd=str(repo))
        bang(r.returncode == MA_KHO, f"mong doi {MA_KHO}, duoc {r.returncode}")


@ca
def t44_bon_cach_viet_URL_cung_mot_danh_tinh():
    """https · git@host:o/r · ssh:// · có cổng — cùng kho phải ra cùng danh tính.

    So chuỗi thô thì đổi https sang ssh là chốt báo "kho khác" ngay.
    """
    dang = ["https://github.com/ducthangho/tra-luat.git",
            "git@github.com:ducthangho/tra-luat.git",
            "ssh://git@github.com/ducthangho/tra-luat",
            "https://github.com:443/ducthangho/tra-luat.git"]
    with San() as s:
        for i, url in enumerate(dang):
            repo = tao_repo(s, ten=f"r{i}")
            them_remote(repo, url)
            r = chay("check", "--expected-repo", "ducthangho/tra-luat", cwd=str(repo))
            bang(r.returncode == MA_OK, f"dang URL bi coi la kho khac: {url} -> {r.returncode}")


@ca
def t45_token_trong_URL_KHONG_duoc_lo_ra():
    """CI và phiên remote hay có `https://x-access-token:<token>@github.com/...`.

    Phần đăng nhập phải bị cắt TRƯỚC khi in, nếu không mỗi lượt chạy là một lần rò
    bí mật vào stdout, JSON và sổ lượt chạy.
    """
    bi_mat = "ghp_TOKEN_KHONG_DUOC_LO_1234567890"
    with San() as s:
        repo = tao_repo(s)
        them_remote(repo, f"https://x-access-token:{bi_mat}@github.com/ducthangho/tra-luat.git")
        r = chay("check", "--expected-repo", "ducthangho/tra-luat", "--json", cwd=str(repo))
        bang(r.returncode == MA_OK, f"{r.returncode}: {r.stderr}")
        bang(bi_mat not in r.stdout and bi_mat not in r.stderr,
             "TOKEN LO RA trong dau ra launcher")
        bang("github.com/ducthangho/tra-luat" in r.stdout, f"khong nhan ra kho: {r.stdout}")


@ca
def t46_run_cung_dung_duoc_neo_kho():
    with San() as s:
        repo = tao_repo(s)
        them_remote(repo, "https://github.com/khac/khac.git")
        dau = s / "da-chay.txt"
        r = chay("run", "--expected-repo", "ducthangho/tra-luat",
                 "--run-root", str(s / "runs"), "--",
                 PY, "-c", f"open({str(dau)!r},'w').write('x')", cwd=str(repo))
        bang(r.returncode == MA_KHO, f"mong doi {MA_KHO}, duoc {r.returncode}")
        bang(not dau.exists(), "lenh VAN chay du kho da lech")


# --------------------------------- các ca do codex tìm ra khi chạy THẬT trên Windows

MA_GIET_HUT = 125


@ca
def t47_console_khong_UTF8_van_in_duoc_duong_dan_co_dau():
    """Console cp1258 (máy Windows tiếng Việt) làm `print` ném UnicodeEncodeError.

    Bẫy nằm ở ĐẦU RA chứ không ở đối số: git nhận đường dẫn đúng, trả về đúng, rồi
    câu print giết cả lượt chạy — đúng ca mà t04 tưởng đã chứng minh là an toàn.
    Ở Linux dựng lại lớp lỗi đó bằng PYTHONIOENCODING=ascii.
    """
    with San() as s:
        repo = tao_repo(s, ten="Quốc hội - kho")
        env = dict(os.environ, PYTHONIOENCODING="ascii")
        r = chay("check", "--workspace", str(repo), env=env)
        bang(r.returncode == MA_OK,
             f"console khong UTF-8 lam launcher chet: {r.returncode} {r.stderr[-300:]}")


@ca
def t48_host_gia_mao_KHONG_duoc_khop():
    """LỖ AN NINH codex đo được: `endswith('/'+can)` cho phép host bất kỳ giả mạo.

    `--expected-repo github.com/o/r` từng KHỚP remote
    `https://evil.example/github.com/o/r.git` — chốt nhận diện kho thành vô dụng
    đúng lúc cần nhất.
    """
    with San() as s:
        repo = tao_repo(s)
        them_remote(repo, "https://evil.example/github.com/ducthangho/tra-luat.git")
        r = chay("check", "--expected-repo", "github.com/ducthangho/tra-luat", cwd=str(repo))
        bang(r.returncode == MA_KHO,
             f"HOST GIA MAO duoc chap nhan: {r.returncode} {r.stdout}")


@ca
def t49_owner_repo_khong_phan_biet_hoa_thuong():
    """GitHub coi Owner/Repo và owner/repo là MỘT kho; chặn oan là chặn sai."""
    with San() as s:
        repo = tao_repo(s)
        them_remote(repo, "https://github.com/DucThangHo/Tra-Luat.git")
        r = chay("check", "--expected-repo", "ducthangho/tra-luat", cwd=str(repo))
        bang(r.returncode == MA_OK, f"ban clone hop le bi chan: {r.returncode}")


@ca
def t50_stop_roi_runner_KHONG_duoc_de_len_so():
    """`stop` ghi da_dung xong runner ghi đè thành `xong` — sổ nói lượt chạy kết
    thúc bình thường trong khi thực tế nó bị người ta dừng.

    Dựng TẤT ĐỊNH: bản đầu của ca này gọi `stop` thật rồi chờ, nên nó xanh hay đỏ
    tuỳ ai ghi sổ sau — đột biến bỏ hẳn chốt vẫn xanh. Nay tự đặt sổ về "da_dung"
    (đúng thứ `stop` để lại) rồi mới cho tiến trình con kết thúc: chỉ còn đúng một
    thứ quyết định kết quả, là chốt hợp nhất trong runner.
    """
    if LA_WINDOWS:
        return "bo qua tren Windows (can kiem rieng)"
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        moc = s / "moc.txt"
        pr = subprocess.Popen(
            [PY, str(LAUNCHER_DANG_DUNG), "run", "--workspace", str(repo),
             "--run-root", str(rr), "--", PY, "-c",
             f"import pathlib,time\nwhile not pathlib.Path({str(moc)!r}).exists(): time.sleep(0.05)"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            f = None
            for _ in range(200):
                time.sleep(0.05)
                ds = list(rr.iterdir()) if rr.is_dir() else []
                if ds and (ds[0] / "run.json").is_file():
                    x = json.loads((ds[0] / "run.json").read_text(encoding="utf-8"))
                    if x.get("pid"):
                        f = ds[0] / "run.json"
                        break
            bang(f is not None, "khong thay pid trong so")
            d = json.loads(f.read_text(encoding="utf-8"))
            d["trang_thai"] = "da_dung"
            d["ly_do_dung"] = "SIGTERM: da tat"
            f.write_text(json.dumps(d), encoding="utf-8")
            moc.write_text("xong", encoding="utf-8")   # cho con thoat
            pr.wait(timeout=30)
            cuoi = json.loads(f.read_text(encoding="utf-8"))
            bang(cuoi["trang_thai"] == "da_dung",
                 f"runner de len quyet dinh cua stop: trang_thai={cuoi['trang_thai']}")
            bang(cuoi.get("ly_do_dung") == "SIGTERM: da tat",
                 f"ly do dung bi xoa: {cuoi.get('ly_do_dung')}")
        finally:
            if pr.poll() is None:
                pr.kill()
                pr.wait(timeout=10)


@ca
def t51_ma_thoat_ngoai_khoang_khong_bi_cat_cut():
    """Con chết vì tín hiệu → returncode âm (Windows: 4294967295). Trả thẳng ra thì
    bị cắt còn 0/255 và phía gọi đọc 'hỏng' thành 'xong'."""
    if LA_WINDOWS:
        return "bo qua tren Windows (can tin hieu POSIX)"
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr), "--",
                 PY, "-c", "import os, signal; os.kill(os.getpid(), signal.SIGKILL)")
        bang(r.returncode not in (0,), f"con bi giet ma launcher tra {r.returncode}")
        bang(0 <= r.returncode <= 255, f"ma thoat ngoai khoang: {r.returncode}")
        d = json.loads((next(rr.iterdir()) / "run.json").read_text(encoding="utf-8"))
        bang(d.get("ma_thoat_that") is not None or d.get("ma_thoat") not in (0, None),
             f"so khong giu ma thoat THAT: {d.get('ma_thoat')} / {d.get('ma_thoat_that')}")


@ca
def t52_so_hong_KHONG_duoc_im_lang():
    """Sổ hỏng bị bỏ qua im lặng thì danh sách rỗng trông hệt như 'chưa chạy gì'."""
    with San() as s:
        rr = s / "runs"
        (rr / "12345678-deadbeef").mkdir(parents=True)
        (rr / "12345678-deadbeef" / "run.json").write_text("{khong-phai-json",
                                                           encoding="utf-8")
        r = chay("status", "--run-root", str(rr))
        bang(r.returncode != 0, f"so hong ma van rc=0: {r.stdout}")
        bang("khong doc duoc" in r.stdout, f"khong noi ro so nao hong: {r.stdout}")


# ------------------------------------------ kiểm công cụ môi trường (doctor)

MA_THIEU_CONG_CU = 12
MA_CHUA_XAC_THUC = 13


@ca
def t53_doctor_bao_du_khi_du():
    """Máy đủ công cụ thì `doctor` phải nói ĐỦ — và phải nói thế TẤT ĐỊNH.

    Ca này từng chớp (đỏ rồi xanh, cùng máy, cách hai phút — ops/NO_KY_THUAT.md,
    packet PLAT-M3/#185): nguồn chớp là một lượt probe (`--version` hoặc auth)
    HẾT HẠN dưới churn tiến trình bị đếm là THIẾU ⇒ thoát 12. Từ v1.3.0 quá hạn
    là "CHƯA ĐO ĐƯỢC" (retry một lượt rồi vào `chua_do_bat_buoc`), không còn
    đường nào phụ thuộc đồng hồ tường dẫn tới 12 — t129/t130/t132/t135 khoá từng
    tầng của bản vá, t131 khoá chiều ngược (hỏng thật vẫn 12).
    """
    r = chay("doctor", "--json")
    # GIỮ NGUYÊN stdout của đúng lượt thoát khác 0 — hai lần săn flake này đều hụt
    # vì bộ chạy nuốt mất JSON, mà JSON mới là thứ nêu tên thủ phạm (ops/NO_KY_THUAT.md
    # dặn tường minh). Đừng bao giờ rút gọn thông điệp này về chỉ còn stderr.
    bang(r.returncode == MA_OK,
         f"rc={r.returncode} · stderr={r.stderr!r} · stdout JSON cua luot hong: {r.stdout}")
    d = json.loads(r.stdout)
    ten = {c["ten"] for c in d["cong_cu"]}
    bang({"git", "python", "claude", "codex", "rg"} <= ten, f"thieu muc trong bang: {ten}")
    bang(d["ok"] is True and not d["thieu_bat_buoc"], f"bao thieu oan: {d['thieu_bat_buoc']}")


@ca
def t54_doctor_thieu_cong_cu_bat_buoc_thi_DO():
    """PATH rỗng: không thấy git lẫn python ⇒ phải thoát 12, không phải 0.

    Một `doctor` luôn xanh thì vô dụng — đây là ca làm nó đỏ.
    """
    env = dict(os.environ, PATH="")
    r = chay("doctor", "--json", env=env)
    bang(r.returncode == MA_THIEU_CONG_CU, f"mong doi {MA_THIEU_CONG_CU}, duoc {r.returncode}")
    d = json.loads(r.stdout)
    bang("git" in d["thieu_bat_buoc"], f"khong bao thieu git: {d['thieu_bat_buoc']}")


@ca
def t55_doctor_nhan_python_khong_can_ten_python3():
    """Windows KHÔNG có lệnh `python3`, chỉ có `python` và `py`.

    Bắt người dùng cài thêm một bí danh là sửa sai chỗ; nhận cả ba tên mới đúng.
    """
    if LA_WINDOWS:
        return "bo qua tren Windows (can shim khong duoi .exe)"
    with San() as s:
        binh = s / "bin"
        binh.mkdir()
        gia = binh / "python"
        gia.write_text("#!/bin/sh\necho 'Python 3.99.0'\n", encoding="utf-8")
        gia.chmod(0o755)
        env = dict(os.environ, PATH=str(binh))
        r = chay("doctor", "--json", env=env)
        d = json.loads(r.stdout)
        py = next(c for c in d["cong_cu"] if c["ten"] == "python")
        bang(py["co"] is True and py.get("goi_bang") == "python",
             f"khong nhan ra `python` khi thieu `python3`: {py}")


# ------------------------------- các ca do vòng AUDIT THỨ HAI của codex tìm ra

@ca
def t56_prompt_doi_sau_khi_kiem_KHONG_toi_duoc_con():
    """TOCTOU thật: hash xong rồi con vẫn mở lại đường dẫn GỐC.

    Codex đo được: đổi nội dung sau khi run.json xuất hiện, con đọc bản ĐÃ ĐỔI —
    neo prompt bị qua mặt hoàn toàn. Với {PROMPT_FILE} con đọc bản chụp bất biến.
    """
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        p = s / "nhiem_vu.txt"
        p.write_text("NOI DUNG GOC", encoding="utf-8")
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        ra = s / "con-doc-duoc.txt"
        # con ngủ 1.5s rồi mới đọc — thừa thời gian cho kẻ đổi tệp
        # Duong dan di qua ARGV, KHONG nhung vao ma nguon: tren Windows duong dan
        # co dang 'C:\\Users\\...' ma '\\U' la escape unicode cua Python =>
        # SyntaxError => con chet truoc khi lam gi, bao "con khong chay". Do that
        # tren runner windows-latest 13-08.
        ma_con = ("import pathlib,sys,time\n"
                  "time.sleep(1.5)\n"
                  "pathlib.Path(sys.argv[2]).write_text("
                  "pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'), encoding='utf-8')")
        pr = subprocess.Popen(
            [PY, str(LAUNCHER_DANG_DUNG), "run", "--workspace", str(repo),
             "--run-root", str(rr), "--prompt-file", str(p),
             "--expected-prompt-sha256", sha, "--",
             PY, "-c", ma_con, "{PROMPT_FILE}", str(ra)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(100):
                time.sleep(0.05)
                if rr.is_dir() and any((d / "run.json").is_file() for d in rr.iterdir()):
                    break
            p.write_text("KE TAN CONG DA DOI", encoding="utf-8")
            pr.wait(timeout=40)
            bang(ra.exists(), "con khong chay")
            bang(ra.read_text(encoding="utf-8") == "NOI DUNG GOC",
                 f"con doc phai ban DA DOI: {ra.read_text(encoding='utf-8')!r}")
        finally:
            if pr.poll() is None:
                pr.kill()
                pr.wait(timeout=10)


@ca
def t57_host_KHONG_co_dau_cham_van_phai_chan():
    """`localhost/o/r` là host-qualified nhưng không có dấu chấm.

    Bản trước phân biệt bằng dấu chấm nên coi nó là 'owner/repo' rồi khớp hậu tố —
    remote `evil.example/localhost/o/r` lọt qua.
    """
    with San() as s:
        repo = tao_repo(s)
        them_remote(repo, "https://evil.example/localhost/o/r.git")
        r = chay("check", "--expected-repo", "localhost/o/r", cwd=str(repo))
        bang(r.returncode == MA_KHO, f"host khong dau cham bi gia mao lot: {r.returncode}")


@ca
def t58_expected_repo_mot_doan_bi_TU_CHOI():
    """`--expected-repo r` phải bị từ chối, không phải khớp bừa.

    Help ghi rõ owner/repo; nhận một đoạn nghĩa là bất kỳ chủ nào có kho tên đó
    đều qua.
    """
    with San() as s:
        repo = tao_repo(s)
        them_remote(repo, "https://evil.example/attacker/r.git")
        r = chay("check", "--expected-repo", "r", cwd=str(repo))
        bang(r.returncode == MA_KHO, f"mot doan duoc chap nhan: {r.returncode}")


@ca
def t59_so_KHONG_luu_doi_so_nguyen_van():
    """Token/prompt truyền qua dòng lệnh không được nằm lại trong sổ."""
    bi_mat = "ghp_DOI_SO_NHAY_CAM_0987654321"
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr), "--",
                 PY, "-c", "pass", "--token", bi_mat)
        bang(r.returncode == 0, f"{r.returncode}: {r.stderr}")
        noi_dung = (next(rr.iterdir()) / "run.json").read_text(encoding="utf-8")
        bang(bi_mat not in noi_dung, "DOI SO NHAY CAM nam trong run.json")
        d = json.loads(noi_dung)
        bang(d["lenh"]["so_doi_so"] == 4, f"mat dau vet lenh: {d['lenh']}")
        bang(d["lenh"]["van_tay"], "khong co van tay de doi chieu")


@ca
def t60_doctor_KHONG_tin_which_khi_cong_cu_khong_chay_duoc():
    """Hai tệp RỖNG tên git/python vẫn làm `shutil.which` thấy — nhưng chạy thì hỏng.

    Có mặt trong PATH không phải bằng chứng dùng được.
    """
    if LA_WINDOWS:
        return "bo qua tren Windows (can .exe rong)"
    with San() as s:
        binh = s / "bin"
        binh.mkdir()
        for ten in ("git", "python"):
            gia = binh / ten
            gia.write_text("", encoding="utf-8")
            gia.chmod(0o755)
        env = dict(os.environ, PATH=str(binh))
        r = chay("doctor", "--json", env=env)
        bang(r.returncode == MA_THIEU_CONG_CU,
             f"doctor xanh voi cong cu khong chay duoc: {r.returncode}")
        d = json.loads(r.stdout)
        git = next(c for c in d["cong_cu"] if c["ten"] == "git")
        bang(git["co"] is False and git.get("co_mat_nhung_khong_chay_duoc"),
             f"khong noi ro 'co ma hong': {git}")


@ca
def t61_run_root_khong_ghi_duoc_KHONG_do_traceback():
    """Lỗi môi trường phải ra mã thoát, không phải nguyên stack Python.

    KHÔNG dùng chmod: `chmod(0o500)` trên THƯ MỤC là no-op ở Windows (đo trên
    runner windows-latest 13-08: run-root vẫn ghi được ⇒ rc=0 thay vì 2), và ở
    POSIX thì root ghi xuyên quyền nên ca này từng phải tự bỏ qua. Đặt một TỆP
    làm thành phần đường dẫn thì `mkdir` buộc phải hỏng ở MỌI nền và MỌI user —
    ca chạy được khắp nơi, không còn nhánh bỏ qua nào.
    """
    with San() as s:
        repo = tao_repo(s)
        chan = s / "chan-la-mot-tep"
        chan.write_text("khong phai thu muc", encoding="utf-8")
        r = chay("run", "--workspace", str(repo), "--run-root", str(chan / "runs"),
                 "--", PY, "-c", "pass")
        bang(r.returncode == MA_THAM_SO, f"mong doi {MA_THAM_SO}, duoc {r.returncode}")
        bang("Traceback" not in r.stderr, f"do traceback tho: {r.stderr[-200:]}")


@ca
def t62_qua_han_ma_khong_giet_het_cay_phai_tra_125():
    """Mẹ chết nhưng CHÁU chưa xác nhận ⇒ 125, không phải 124.

    Đây là lỗi CHẶN số 1 của vòng audit: nhánh dự phòng ghi "da tat (CON CHAU CO
    THE CON SONG)" — chứa đúng substring mà phía gọi dò — nên hạn chót trả 124
    trong khi cháu vẫn ghi tiếp vào workspace.

    CHỈ ĐO ĐƯỢC TRÊN WINDOWS: trên POSIX `killpg` giết theo NHÓM nên cả cây luôn
    chết cùng lúc, không có trạng thái "mẹ chết cháu sống" để dựng. Nói thẳng là
    chưa đo được ở đây còn hơn dựng một ca giả rồi tưởng đã phủ.
    """
    if not LA_WINDOWS:
        # SỬA vòng 3: lý do bỏ qua cũ ("POSIX killpg giết cả nhóm nên KHÔNG dựng
        # được ca mẹ-chết-cháu-sống") là SAI SỰ THẬT — dựng được, và khi dựng thì
        # bản cũ trả 124 với cháu còn sống. Bản POSIX của ca này là t63; ở đây chỉ
        # còn đúng phần fixture riêng của Windows (cháu ngây thơ + taskkill /T).
        return "fixture nay danh cho Windows; ban POSIX la t63 (chay duoc, khong bo qua)"
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        dau = s / "chau-con-song.txt"
        # CA MO COI: `giua` sinh `chau` roi THOAT NGAY. Den luc giet, cay cha-con
        # tinh tu me KHONG con chua chau (cha no da chet), nen ca `taskkill /T` lan
        # `_chup_cay` deu bo sot - `taskkill /T` duyet dung nhung lien ket ay.
        # Chi Job Object giu duoc hau due mo coi.
        (s / "chau.py").write_text(
            "import os, sys, time\n"
            "open(sys.argv[1], 'w').write(str(os.getpid()))\n"
            "time.sleep(60)\n", encoding="utf-8")
        (s / "giua.py").write_text(
            "import subprocess, sys\n"
            "subprocess.Popen([sys.executable, sys.argv[1], sys.argv[2]])\n",
            encoding="utf-8")
        (s / "me.py").write_text(
            "import subprocess, sys, time\n"
            "subprocess.Popen([sys.executable, sys.argv[1], sys.argv[2],\n"
            "                  sys.argv[3]]).wait()\n"
            "time.sleep(60)\n", encoding="utf-8")
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--deadline-utc", mai_sau(3),
                 "--", PY, str(s / "me.py"), str(s / "giua.py"),
                 str(s / "chau.py"), str(dau))
        for _ in range(60):
            if dau.exists():
                break
            time.sleep(0.05)
        bang(dau.exists(), "thi nghiem hong: chau chua kip ghi pid")
        chau = int(dau.read_text().strip())
        time.sleep(0.5)
        chau_song = _con_song_that(chau)
        try:
            if chau_song:
                bang(r.returncode == MA_GIET_HUT,
                     f"chau MO COI {chau} con song ma tra {r.returncode} "
                     f"(phai {MA_GIET_HUT})")
            else:
                bang(r.returncode == MA_QUA_HAN,
                     f"da giet het cay ma tra {r.returncode} (phai {MA_QUA_HAN})")
        finally:
            if chau_song:
                try:
                    os.kill(chau, 9)
                except OSError:
                    pass


@ca
def t63_chau_phot_lo_SIGTERM_ma_bao_da_giet_ca_cay_la_noi_doi():
    """POSIX: mẹ chết mà CHÁU CÙNG NHÓM còn sống ⇒ không được trả 124.

    ĐÂY LÀ CA MÀ VÒNG 2 TIN LÀ KHÔNG DỰNG ĐƯỢC. t62 bỏ qua trên POSIX với lý do
    "killpg giết cả nhóm nên cả cây luôn chết cùng lúc" — chỉ đúng với cháu ngây
    thơ. Cháu chỉ cần `SIG_IGN` cho SIGTERM là sống nguyên VẪN TRONG NHÓM, và
    bản trước thoát vòng chờ ngay khi MẸ chết nên `killpg(SIGKILL)` không bao giờ
    được gửi ⇒ hạn chót trả 124 ("đã giết được") với cháu đang chạy tiếp.

    Ca này neo HAI thứ:
      1. mã thoát phải KHỚP THỰC TẾ (cháu sống ⇒ 125, cháu chết ⇒ 124) — chốt
         chống nói dối, y hệt t62;
      2. trên POSIX phải THẬT SỰ giết được (leo thang SIGKILL tới cả nhóm).
    """
    if LA_WINDOWS:
        return "ca nay dung SIG_IGN cua POSIX; duong Windows la t62"
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        dau = s / "chau-con-song.txt"
        chau_py = s / "chau.py"
        chau_py.write_text(
            "import os, signal, sys, time\n"
            "signal.signal(signal.SIGTERM, signal.SIG_IGN)  # phot lo, VAN trong nhom\n"
            "open(sys.argv[1], 'w').write(str(os.getpid()))\n"
            "time.sleep(60)\n", encoding="utf-8")
        me_py = s / "me.py"
        me_py.write_text(
            "import subprocess, sys, time\n"
            "subprocess.Popen([sys.executable, sys.argv[1], sys.argv[2]])\n"
            "time.sleep(60)\n", encoding="utf-8")
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--deadline-utc", mai_sau(2),
                 "--", PY, str(me_py), str(chau_py), str(dau))
        for _ in range(40):          # chờ cháu kịp ghi pid
            if dau.exists():
                break
            time.sleep(0.05)
        bang(dau.exists(), "thi nghiem hong: chau chua kip ghi pid")
        chau = int(dau.read_text().strip())
        time.sleep(0.5)
        # ZOMBIE PHẢI TÍNH LÀ ĐÃ CHẾT — `os.kill(pid, 0)` THÀNH CÔNG với zombie.
        # Cháu mất mẹ nên được init nhận nuôi, mà init trong container không phải
        # lúc nào cũng thu hồi ngay ⇒ nó nằm ở trạng thái Z khá lâu. Bản đầu của
        # ca này dùng os.kill(pid,0) và báo ĐỎ oan cho một bản vá ĐÚNG — đúng cái
        # bẫy đã ghi sẵn trong docstring của `_con_song` mà vẫn đạp phải.
        chau_song = _con_song_that(chau)
        try:
            if chau_song:
                bang(r.returncode == MA_GIET_HUT,
                     f"chau {chau} CON SONG ma tra {r.returncode} (phai {MA_GIET_HUT})")
            else:
                bang(r.returncode == MA_QUA_HAN,
                     f"da giet het cay ma tra {r.returncode} (phai {MA_QUA_HAN})")
            bang(not chau_song,
                 f"POSIX phai leo thang SIGKILL toi ca nhom, nhung chau {chau} van song")
        finally:
            if chau_song:
                try:
                    os.kill(chau, signal.SIGKILL)
                except OSError:
                    pass


@ca
def t67_chau_sinh_SAU_luc_chup_van_phai_bi_dem():
    """Cháu sinh ra SAU khi đã chụp cây (mẹ bắt SIGTERM rồi mới đẻ) — lớp NHÓM bắt.

    Bổ đôi với t66: ảnh chụp bắt kẻ đã rời nhóm, đếm thành viên nhóm bắt kẻ sinh
    sau lúc chụp. Không lớp nào phủ được ca của lớp kia, nên cả hai đều phải có.
    Ca thật: tiến trình dọn dẹp trong tay bắt tín hiệu lại đẻ thêm việc.
    """
    if LA_WINDOWS:
        return "dua tren SIGTERM cua POSIX; duong Windows la t62"
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        dau = s / "chau-con-song.txt"
        chau_py = s / "chau.py"
        chau_py.write_text(
            "import os, sys, time\n"
            "open(sys.argv[1], 'w').write(str(os.getpid()))\n"
            "time.sleep(60)\n", encoding="utf-8")
        me_py = s / "me.py"
        me_py.write_text(
            "import os, signal, subprocess, sys, time\n"
            "def tay(sig, khung):\n"
            "    subprocess.Popen([sys.executable, sys.argv[1], sys.argv[2]])\n"
            "    os._exit(0)          # me chet NGAY, chau vua sinh o lai trong nhom\n"
            "signal.signal(signal.SIGTERM, tay)\n"
            "time.sleep(60)\n", encoding="utf-8")
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--deadline-utc", mai_sau(2),
                 "--", PY, str(me_py), str(chau_py), str(dau))
        for _ in range(40):
            if dau.exists():
                break
            time.sleep(0.05)
        bang(dau.exists(), "thi nghiem hong: chau chua kip ghi pid")
        chau = int(dau.read_text().strip())
        time.sleep(0.5)
        chau_song = _con_song_that(chau)
        try:
            if chau_song:
                bang(r.returncode == MA_GIET_HUT,
                     f"chau {chau} sinh sau luc chup VAN CON SONG ma tra "
                     f"{r.returncode} (phai {MA_GIET_HUT})")
            else:
                bang(r.returncode == MA_QUA_HAN,
                     f"da giet het cay ma tra {r.returncode} (phai {MA_QUA_HAN})")
        finally:
            if chau_song:
                try:
                    os.kill(chau, signal.SIGKILL)
                except OSError:
                    pass


@ca
def t66_chau_setsid_roi_khoi_nhom_van_phai_bi_giet():
    """Cháu tự `setsid()` rời nhóm ⇒ `killpg` KHÔNG với tới. Vẫn không được nói dối.

    Bản vá đầu của vòng 3 chỉ đếm THÀNH VIÊN NHÓM nên ca này vẫn lọt: nhóm rỗng
    thật (cháu đã ra ngoài) ⇒ vẫn trả 124 với cháu đang chạy. Phải chụp CÂY con
    cháu TRƯỚC khi phát tín hiệu — sau khi mẹ chết, cháu được init nhận nuôi nên
    mất cả liên kết nhóm LẪN liên kết cha, không còn đường nào tìm ra.
    """
    if LA_WINDOWS:
        return "setsid la khai niem POSIX; duong Windows la t62"
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        dau = s / "chau-con-song.txt"
        chau_py = s / "chau.py"
        chau_py.write_text(
            "import os, sys, time\n"
            "open(sys.argv[1], 'w').write(str(os.getpid()))\n"
            "time.sleep(60)\n", encoding="utf-8")
        me_py = s / "me.py"
        me_py.write_text(
            "import subprocess, sys, time\n"
            "subprocess.Popen([sys.executable, sys.argv[1], sys.argv[2]],\n"
            "                 start_new_session=True)   # setsid(): ra khoi nhom\n"
            "time.sleep(60)\n", encoding="utf-8")
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--deadline-utc", mai_sau(2),
                 "--", PY, str(me_py), str(chau_py), str(dau))
        for _ in range(40):
            if dau.exists():
                break
            time.sleep(0.05)
        bang(dau.exists(), "thi nghiem hong: chau chua kip ghi pid")
        chau = int(dau.read_text().strip())
        time.sleep(0.5)
        chau_song = _con_song_that(chau)
        try:
            if chau_song:
                bang(r.returncode == MA_GIET_HUT,
                     f"chau {chau} da setsid VAN CON SONG ma tra {r.returncode} "
                     f"(phai {MA_GIET_HUT})")
            else:
                bang(r.returncode == MA_QUA_HAN,
                     f"da giet het cay ma tra {r.returncode} (phai {MA_QUA_HAN})")
        finally:
            if chau_song:
                try:
                    os.kill(chau, signal.SIGKILL)
                except OSError:
                    pass


@ca
def t64_short_id_da_bi_GIANH_thi_khong_duoc_cap_lai():
    """short_id phải được giành NGUYÊN TỬ, không phải bằng "quét rồi mkdir".

    ĐÃ TRẢ GIÁ HAI LẦN. Bản vá vòng 2 đổi sang `thu_muc.mkdir(parents=False)` và
    tuyên bố khe hở đã đóng — nhưng tên thư mục là "{sid}-{rid}" nên mkdir độc
    quyền chỉ chặn trùng run_id ĐẦY ĐỦ; hai tiến trình cùng chọn trúng một
    short_id vẫn tạo được hai thư mục khác tên (audit vòng 3 ép được bằng cách
    cho hai luồng quét xong rồi mới mkdir). Nay short_id được giành bằng mốc
    `.sid-<id>` tạo O_EXCL — tên mốc CHỈ chứa sid nên va chạm là thật sự nguyên tử.

    CHÍNH CUỘC ĐUA thì KHÔNG dựng được qua seam dòng lệnh — nó cần chặn hai
    tiến trình ở đúng khe giữa "quét" và "mkdir" (audit vòng 3 làm được bằng
    Path-proxy trong tiến trình). Thứ neo được ở đây là TÍNH CHẤT CẤU TRÚC khiến
    cuộc đua không còn tồn tại: **tên thư mục ĐÚNG BẰNG short_id**, nên `mkdir`
    không exist_ok chính là hành vi giành, nguyên tử ở tầng hệ tệp. Bản cũ đặt
    tên "{sid}-{rid}" nên ca này ĐỎ trên nó.

    Ép tất định bằng cách bơm `sitecustomize.py` qua PYTHONPATH để `uuid4` luôn
    trả cùng 8 hex đầu — vẫn đi qua CLI thật, nên đột biến vẫn đo được.
    """
    with San() as s:
        repo = tao_repo(s)
        gia = s / "ep_uuid"
        gia.mkdir()
        (gia / "sitecustomize.py").write_text(
            "import uuid\n"
            "class _U:\n"
            "    def __init__(self, h): self.hex = h\n"
            "_n = [0]\n"
            "def _gia():\n"
            "    _n[0] += 1\n"
            "    return _U('deadbeef' + '%024x' % _n[0])\n"
            "uuid.uuid4 = _gia\n", encoding="utf-8")
        moi = dict(os.environ)
        moi["PYTHONPATH"] = str(gia) + os.pathsep + moi.get("PYTHONPATH", "")

        rr = s / "runs"
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--", PY, "-c", "pass", env=moi)
        bang(r.returncode == MA_OK, f"luot dau phai qua, duoc {r.returncode}: {r.stderr}")
        ds = [p for p in rr.iterdir() if p.is_dir()]
        bang(len(ds) == 1, f"mong doi 1 thu muc, thay {[p.name for p in ds]}")
        so = json.loads((ds[0] / "run.json").read_text(encoding="utf-8"))
        bang(ds[0].name == so["short_id"],
             f"ten thu muc phai DUNG BANG short_id de mkdir la hanh vi gianh: "
             f"ten={ds[0].name!r}, short_id={so['short_id']!r}")

        # run_id đầy đủ KHÔNG còn trong tên nữa — `status --id <run_id>` vẫn phải tra được.
        r_id = chay("status", "--run-root", str(rr), "--id", so["run_id"])
        bang(r_id.returncode == MA_OK,
             f"tra theo run_id day du hong: {r_id.returncode} {r_id.stderr}")

        # short_id 'deadbeef' đã bị giành; mọi lần thử đều ra đúng nó ⇒ phải BỎ CUỘC
        # bằng mã va chạm, KHÔNG được cấp lại hay ghi đè lượt cũ.
        r2 = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                  "--", PY, "-c", "pass", env=moi)
        bang(r2.returncode == MA_VA_CHAM,
             f"short_id da bi giu ma van cap lai: rc={r2.returncode}")
        bang(len([p for p in rr.iterdir() if p.is_dir()]) == 1,
             "luot thu hai da de len thu muc cua luot dau")


@ca
def t65_run_root_TUONG_DOI_van_giao_duoc_ban_chup_cho_con():
    """`--run-root` tương đối + chạy từ THƯ MỤC CON: con vẫn phải đọc được prompt.

    Con được sinh với `cwd=gốc repo`, còn launcher có thể đứng ở thư mục con
    (`tim_workspace` quảng cáo đúng điều đó). Không `resolve()` thì đường dẫn bản
    chụp thay vào {PROMPT_FILE} là tương đối theo cwd của LAUNCHER, con đọc theo
    cwd của NÓ ⇒ trượt. Audit vòng 3 đo được bản cũ: sổ ghi
    prompt_kin_hoan_toan=True, con in "No such file or directory", mà lượt chạy
    vẫn trả rc=0 và trạng thái "xong" — fail-OPEN kèm khẳng định SAI trong sổ.
    """
    with San() as s:
        repo = tao_repo(s)
        sau = repo / "con" / "sau"
        sau.mkdir(parents=True)
        pf = s / "prompt.txt"
        pf.write_text("NOI-DUNG-PROMPT-NEO\n", encoding="utf-8")
        sha = hashlib.sha256(pf.read_bytes()).hexdigest()
        r = chay("run", "--run-root", "runs-tuong-doi",
                 "--prompt-file", str(pf), "--expected-prompt-sha256", sha,
                 "--", PY, "-c", "import sys; print(open(sys.argv[1]).read())",
                 "{PROMPT_FILE}", cwd=str(sau))
        bang(r.returncode == MA_OK,
             f"mong doi {MA_OK}, duoc {r.returncode}: {r.stdout} {r.stderr}")
        rr = sau / "runs-tuong-doi"
        ds = [p for p in rr.iterdir() if p.is_dir()]
        bang(len(ds) == 1, f"mong doi 1 thu muc luot chay, thay {len(ds)}")
        so = json.loads((ds[0] / "run.json").read_text(encoding="utf-8"))
        bang(so.get("prompt_kin_hoan_toan") is True,
             f"prompt_kin_hoan_toan={so.get('prompt_kin_hoan_toan')}")
        ra = (ds[0] / "stdout.log").read_text(encoding="utf-8")
        bang("NOI-DUNG-PROMPT-NEO" in ra,
             f"con KHONG doc duoc ban chup (so van khoe kin hoan toan). stdout={ra!r}, "
             f"stderr={(ds[0] / 'stderr.log').read_text(encoding='utf-8')!r}")


@ca
def t68_kho_duong_dan_SAU_neu_host_van_phai_QUA():
    """`--expected-repo` nêu host + đường dẫn ≥4 đoạn (GitLab subgroup, GHE lồng).

    Bản trước chỉ nhận ĐÚNG 3 đoạn nên danh tính đầy đủ, đúng từng ký tự, bị TỪ
    CHỐI — kèm thông điệp tự mâu thuẫn "mong doi X, thuc te [X]". Người dùng
    GitLab/GHE mất hẳn lựa chọn neo-theo-host.
    """
    with San() as s:
        repo = tao_repo(s)
        them_remote(repo, "https://gitlab.com/nhom/nhom-con/kho.git")
        r = chay("check", "--workspace", str(repo),
                 "--expected-repo", "gitlab.com/nhom/nhom-con/kho")
        bang(r.returncode == MA_OK,
             f"danh tinh DAY DU bi chan oan: rc={r.returncode} {r.stderr}")
        # vẫn phải là BẰNG NHAU tuyệt đối: đổi một đoạn giữa là chặn
        r2 = chay("check", "--workspace", str(repo),
                  "--expected-repo", "gitlab.com/nhom/khac/kho")
        bang(r2.returncode == MA_KHO, f"doan giua sai ma van qua: {r2.returncode}")
        # và host giả mạo vẫn phải chặn
        r3 = chay("check", "--workspace", str(repo),
                  "--expected-repo", "evil.example/nhom/nhom-con/kho")
        bang(r3.returncode == MA_KHO, f"host gia mao lot: {r3.returncode}")


@ca
def t69_stop_luot_DA_KET_THUC_khong_duoc_doi_so():
    """`stop` một lượt đã chạy xong: không đổi sổ, không hô "PID da bi tai dung".

    Bản trước ghi đè trang_thai="da_dung" lên lượt vừa "xong" bình thường VÀ báo
    "khoa danh tinh KHAC (PID da bi tai dung)" + rc=10 — hô hoán đúng mối nguy mà
    khoá danh tính sinh ra để bắt, trong ca vô hại và phổ biến nhất.
    """
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        # Con phai SONG DU LAU de khoa danh tinh kip duoc lay. ĐÃ ĐO trên runner
        # windows-latest (13-08): với `-c pass` con thoát trước khi
        # `_khoa_danh_tinh` chạy, mà Get-Process KHÔNG thấy tiến trình đã thoát
        # (POSIX thì /proc/<pid> còn ở dạng zombie nên đọc được) ⇒ sổ ghi
        # khoa_danh_tinh=null ⇒ stop từ chối bằng mã 10 và ca này ĐỎ oan.
        # Ca "thiếu khoá thì TỪ CHỐI" là việc của t32, không phải của ca này.
        chay("run", "--workspace", str(repo), "--run-root", str(rr),
             "--", PY, "-c", "import time; time.sleep(1)")
        thu_muc = next(p for p in rr.iterdir() if p.is_dir())
        truoc = json.loads((thu_muc / "run.json").read_text(encoding="utf-8"))
        bang(truoc["trang_thai"] == "xong", f"tien de sai: {truoc['trang_thai']}")
        bang(truoc.get("khoa_danh_tinh"), "tien de sai: khong lay duoc khoa danh tinh")
        r = chay("stop", "--run-root", str(rr), "--id", truoc["short_id"])
        sau = json.loads((thu_muc / "run.json").read_text(encoding="utf-8"))
        bang(sau["trang_thai"] == "xong",
             f"stop de len luot da xong: trang_thai={sau['trang_thai']}")
        bang("tai dung" not in (r.stdout + r.stderr),
             f"chan doan SAI 'PID da bi tai dung' cho tien trinh chi don gian la da thoat: {r.stdout}")
        bang(r.returncode == MA_OK, f"mong doi {MA_OK}, duoc {r.returncode}")



@ca
def t70_PROMPT_FILE_ma_khong_co_prompt_file_phai_bi_CHAN():
    return _t70_prompt_file_chan()


def _t70_prompt_file_chan():
    """Có {PROMPT_FILE} mà không truyền --prompt-file ⇒ chặn, không đi tiếp im lặng.

    Bản trước: con nhận CHUỖI NGUYÊN VĂN "{PROMPT_FILE}" làm đường dẫn, rc=0, sổ
    ghi "xong". Người vận hành tin prompt đã neo; agent nhận đường dẫn vô nghĩa.
    """
    with San() as s:
        repo = tao_repo(s)
        r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"),
                 "--", PY, "-c", "import sys;print(sys.argv[1])", "{PROMPT_FILE}")
        bang(r.returncode == MA_THAM_SO,
             f"mong doi {MA_THAM_SO}, duoc {r.returncode}: {r.stdout} {r.stderr}")


@ca
def t71_ban_chup_prompt_phai_KIN_va_bi_XOA():
    """prompt.snapshot: 0600 lúc tồn tại, và bị xoá sau khi con thoát.

    argv đã bị bỏ khỏi sổ vì có thể chứa bí mật; ghi TOÀN VĂN prompt ra đĩa
    world-readable VĨNH VIỄN là mở rộng bề mặt lộ chứ không thu hẹp.
    """
    with San() as s:
        repo = tao_repo(s)
        pf = s / "prompt.txt"
        pf.write_text("BI-MAT-KHONG-DE-LO\n", encoding="utf-8")
        sha = hashlib.sha256(pf.read_bytes()).hexdigest()
        rr = s / "runs"
        # con ĐỌC bản chụp rồi in quyền của nó ra, nên đo được lúc nó CÒN tồn tại
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--prompt-file", str(pf), "--expected-prompt-sha256", sha,
                 "--", PY, "-c",
                 "import os,stat,sys;print(oct(stat.S_IMODE(os.stat(sys.argv[1]).st_mode)))",
                 "{PROMPT_FILE}")
        bang(r.returncode == MA_OK, f"rc={r.returncode}: {r.stderr}")
        thu_muc = next(p for p in rr.iterdir() if p.is_dir())
        quyen = (thu_muc / "stdout.log").read_text(encoding="utf-8").strip()
        if not LA_WINDOWS:
            bang(quyen == "0o600", f"ban chup KHONG kin: quyen={quyen}")
        # Xoa NGAY chi xay ra khi chung minh duoc nhom tien trinh da rong (xem
        # `cay_da_chet`). Windows khong do duoc nhom nen ban chup o lai cho toi
        # luot quet - khang dinh o day phai noi dung dieu do, dung doi hoi mot
        # bao dam ma nen kia khong the giu.
        if not LA_WINDOWS:
            bang(not (thu_muc / "prompt.snapshot").exists(),
                 "ban chup con nam lai tren dia sau khi con thoat")
        else:
            bang((thu_muc / "prompt.snapshot").exists(),
                 "Windows khong do duoc nhom nen phai GIU ban chup, khong xoa mu")
        # xin giữ thì phải còn
        rr2 = s / "runs2"
        r2 = chay("run", "--workspace", str(repo), "--run-root", str(rr2),
                  "--giu-ban-chup", "--prompt-file", str(pf),
                  "--expected-prompt-sha256", sha, "--", PY, "-c", "pass")
        bang(r2.returncode == MA_OK, f"rc={r2.returncode}: {r2.stderr}")
        tm2 = next(p for p in rr2.iterdir() if p.is_dir())
        bang((tm2 / "prompt.snapshot").exists(), "--giu-ban-chup ma van xoa")


@ca
def t76_wrapper_thoat_khong_duoc_xoa_prompt_cua_chau():
    """Wrapper thoát ngay, cháu đọc trễ: snapshot phải còn cho tới lúc đọc.

    `codex exec` cũng có thể bọc công việc trong tiến trình con. Bản trước
    xoá snapshot ngay khi wrapper trả rc=0; cháu mở sau 0,4s nhận ENOENT.
    """
    if LA_WINDOWS:
        return "ca nhom tien trinh POSIX; Windows can fixture that rieng"
    with San() as s:
        repo = tao_repo(s)
        pf = s / "prompt.txt"
        pf.write_text("PROMPT-CHO-TIEN-TRINH-CHAU\n", encoding="utf-8")
        sha = hashlib.sha256(pf.read_bytes()).hexdigest()
        ket_qua = s / "chau-doc.txt"
        ma_chau = ("import pathlib,sys,time;time.sleep(.4);"
                   "p=pathlib.Path(sys.argv[1]);o=pathlib.Path(sys.argv[2]);"
                   "o.write_text(p.read_text(encoding='utf-8'),encoding='utf-8')")
        ma_wrapper = ("import subprocess,sys;"
                      "subprocess.Popen([sys.executable,'-c',sys.argv[1],"
                      "sys.argv[2],sys.argv[3]])")
        rr = s / "runs"
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--prompt-file", str(pf), "--expected-prompt-sha256", sha,
                 "--", PY, "-c", ma_wrapper, ma_chau, "{PROMPT_FILE}", str(ket_qua))
        bang(r.returncode == MA_OK, f"wrapper rc={r.returncode}: {r.stderr}")
        for _ in range(40):
            if ket_qua.exists():
                break
            time.sleep(.05)
        bang(ket_qua.exists(),
             "wrapper thoat da lam launcher xoa snapshot truoc khi chau mo")
        bang(ket_qua.read_text(encoding="utf-8") == pf.read_text(encoding="utf-8"),
             "chau khong doc dung noi dung snapshot")


@ca
def t77_ban_chup_qua_han_bi_QUET_du_khong_xoa_duoc_ngay():
    """Ban chup giu lai (nen khong do duoc nhom) KHONG duoc nam lai vinh vien.

    Vong 4 doi luat: chi xoa ngay khi CHUNG MINH duoc nhom tien trinh da rong.
    Tren Windows dieu kien do luon sai, nen neu khong co gi quet don thi noi dung
    prompt nam tren dia mai mai - dung thu ma `_tom_tat_lenh` da bo argv de tranh.
    """
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        chay("run", "--workspace", str(repo), "--run-root", str(rr), "--", PY, "-c", "pass")
        cu = next(p for p in rr.iterdir() if p.is_dir())
        qua_han = cu / "prompt.snapshot"
        qua_han.write_text("PROMPT-CU-QUA-HAN", encoding="utf-8")
        os.utime(qua_han, (time.time() - 2 * 86400,) * 2)
        moi = cu / "prompt.snapshot.moi"
        moi.write_text("x", encoding="utf-8")
        chay("run", "--workspace", str(repo), "--run-root", str(rr), "--", PY, "-c", "pass")
        bang(not qua_han.exists(), "ban chup qua han KHONG duoc quet don")
        bang(moi.exists(), "quet nham tep khac")


@ca
def t72_bi_ngat_KHONG_duoc_ghi_thanh_xong():
    """Ctrl-C giữa lượt chạy: sổ phải nói bị ngắt, không phải "xong".

    `trang_thai` là trường `status` liệt kê, nên ghi "xong" cho một lượt bị cắt
    giữa chừng là nói dối đúng chỗ người/máy đang đọc. Cùng lớp lỗi với t50.
    """
    if LA_WINDOWS:
        return "SIGINT tren Windows khong cung ngu nghia; can ca rieng"
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        pr = subprocess.Popen([PY, str(LAUNCHER_DANG_DUNG), "run",
                               "--workspace", str(repo), "--run-root", str(rr),
                               "--", PY, "-c", "import time;time.sleep(30)"],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        try:
            f = None
            for _ in range(200):
                time.sleep(0.05)
                ds = [p for p in rr.iterdir() if p.is_dir()] if rr.is_dir() else []
                if ds and (ds[0] / "run.json").is_file():
                    x = json.loads((ds[0] / "run.json").read_text(encoding="utf-8"))
                    if x.get("pid"):
                        f = ds[0] / "run.json"
                        break
            bang(f is not None, "khong thay pid trong so")
            time.sleep(0.3)
            os.kill(pr.pid, signal.SIGINT)
            pr.communicate(timeout=60)
            d = json.loads(f.read_text(encoding="utf-8"))
            bang(d["trang_thai"] == "bi_ngat",
                 f"bi ngat ma so ghi trang_thai={d['trang_thai']!r}")
        finally:
            if pr.poll() is None:
                pr.kill()
                pr.wait(timeout=10)


@ca
def t73_doctor_phai_do_bash_va_npm():
    """doctor phải đo thứ môi trường THẬT SỰ phụ thuộc.

    settings.json gọi hook qua `bash`, session-start.sh rẽ nhánh trên `npm`.
    Thiếu chúng thì hook hỏng, mà doctor cũ vẫn in "DU CONG CU BAT BUOC".
    """
    r = chay("doctor", "--json")
    d = json.loads(r.stdout)
    ten = {c["ten"] for c in d["cong_cu"]}
    bang({"bash", "npm"} <= ten, f"doctor khong do bash/npm: {sorted(ten)}")


@ca
def t74_dut_ong_KHONG_duoc_nuot_ma_that():
    """Người đọc đóng ống giữa chừng KHÔNG được đổi kết luận đã tính xong.

    Bản trước bắt BrokenPipeError ở `main` rồi trả 141, nên `doctor | head` trên
    môi trường LÀNH cũng ra 141 — phía gọi kiểm `rc != 0` báo "THIEU CONG CU" oan.

    CA NÀY TỪNG PHI-TẤT-ĐỊNH và đã trả giá: bản đầu cho người đọc đóng ống NGAY,
    rồi trông chờ ống vỡ. Nhưng stdout của Python nối ống là block-buffered 8KB và
    ống hệ điều hành còn đệm thêm 64KB, nên với đầu ra NHỎ mọi thứ lọt hết vào đệm,
    KHÔNG lần ghi nào hỏng, và đột biến sống sót. Cổng xanh ở máy này, ĐỎ trên
    runner CI (13-08: `dut_ong_nuot_ma_that SAI giet 0/1`).
    Nay ép tất định: dựng sổ đủ lớn để vượt đệm 8KB của Python (nhiều lần ghi),
    ĐỌC ĐÚNG 1 BYTE cho lần ghi đầu chắc chắn thành công, rồi đóng — lần ghi kế
    tiếp buộc phải vỡ ống. Không còn phụ thuộc thời điểm.
    """
    with San() as s:
        rr = s / "runs"
        rr.mkdir()
        # `ten` dài để đầu ra `status` vượt xa 8KB mà không phải chạy thật N lượt.
        for i in range(40):
            d = rr / f"{i:08x}"
            d.mkdir()
            (d / "run.json").write_text(json.dumps({
                "short_id": f"{i:08x}", "ten": "x" * 2000, "trang_thai": "xong",
                "ma_thoat": 0, "bat_dau_utc": "2026-01-01T00:00:00+00:00"}),
                encoding="utf-8")
        do_dai = len(chay("status", "--run-root", str(rr)).stdout)
        bang(do_dai > 8192, f"tien de sai: dau ra chi {do_dai} byte, chua vuot dem 8KB")

        pr = subprocess.Popen([PY, str(LAUNCHER_DANG_DUNG), "status", "--run-root", str(rr)],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        try:
            bang(pr.stdout.read(1) != b"", "khong doc duoc byte nao")
            pr.stdout.close()      # lan ghi KE TIEP buoc phai vo ong
            ma = pr.wait(timeout=120)
        finally:
            if pr.poll() is None:
                pr.kill()
                pr.wait(timeout=10)
        bang(ma == MA_OK, f"so lanh lan ma dut ong lam ra ma {ma}")

@ca
def t75_tep_tam_mo_coi_bi_don():
    """Tệp tạm của writer bị SIGKILL giữa chừng không được tích luỹ vĩnh viễn.

    Tên tạm riêng theo pid+uuid (bản vá vòng 2) nên KHÔNG bao giờ bị ghi đè —
    khác tên cố định cũ vốn tự lành. Rác nằm trong thư mục của lượt ĐÃ CHẾT nên
    phải quét từ run_root; quét thư mục đang ghi thì chẳng dọn được gì.
    """
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        chay("run", "--workspace", str(repo), "--run-root", str(rr), "--", PY, "-c", "pass")
        cu = next(p for p in rr.iterdir() if p.is_dir())
        rac_cu = cu / "run.json.99999.deadbeef.tmp"
        rac_cu.write_text("rac", encoding="utf-8")
        os.utime(rac_cu, (time.time() - 2 * 86400,) * 2)
        rac_moi = cu / "run.json.88888.cafe1234.tmp"
        rac_moi.write_text("rac", encoding="utf-8")
        chay("run", "--workspace", str(repo), "--run-root", str(rr), "--", PY, "-c", "pass")
        bang(not rac_cu.exists(), "tep tam mo coi cu KHONG duoc don")
        bang(rac_moi.exists(), "don ca tep tam DANG dung cua writer khac")


@ca
def t78_khong_do_duoc_nhom_KHONG_phai_cay_rong():
    """None từ phép quét không được biến thành bằng chứng cả cây đã chết.

    PHẢI bịt CẢ HAI phép đo. Bản đầu chỉ bịt `_thanh_vien_nhom` rồi để `_chup_cay`
    THẬT chạy — trên Linux nó gọi `powershell` (không có) nên ném rồi trả None, tức
    ca xanh nhờ MÁY DEV THIẾU CÔNG CỤ chứ không nhờ điều được khẳng định. Trên
    windows-latest `_chup_cay` chạy thật, trả `{}` cho một PID không tồn tại — bằng
    chứng ĐO ĐƯỢC và hợp lệ (đó là điều `t83` khẳng định) — nên ca này đỏ ở đó.
    Sửa FIXTURE, không nới chốt: muốn thử "không đo được" thì phải dựng cho bằng
    được trạng thái không đo được, ở mọi nền.
    """
    m = _tai_launcher_thu()
    m._khoa_danh_tinh = lambda _pid: None
    m._thanh_vien_nhom = lambda _pid: None     # phep do POSIX
    m._chup_cay = lambda _pid: None            # phep do Windows
    m.platform.system = lambda: "Windows"
    da_goi = []
    m._giet_windows = lambda *_a, **_k: (da_goi.append(True) or m.KetGiet(False, False, "khong do duoc"))
    kq = m._giet_cay(12345, "win:1")
    bang(da_goi and not kq.tron_ven,
         "None bi doc nhu []: bao ca cay da chet ma khong goi duong giet Windows")


@ca
def t79_job_windows_phai_kiem_ket_qua_dat_gioi_han():
    """SetInformationJobObject hỏng thì handle không được quảng cáo là job tốt."""
    m = _tai_launcher_thu()
    m.platform.system = lambda: "Windows"
    import ctypes

    class K32:
        def __init__(self): self.dong = []
        def CreateJobObjectW(self, *_a): return 41
        def SetInformationJobObject(self, *_a): return 0
        def CloseHandle(self, h): self.dong.append(h); return 1
        def OpenProcess(self, *_a): raise TinHieuChotCa("khong duoc di tiep sau SetInformation hong")

    cu = getattr(ctypes, "windll", None)
    fake = type("Windll", (), {})(); fake.kernel32 = K32()
    ctypes.windll = fake
    try:
        bang(m._job_windows(12345) is None and fake.kernel32.dong == [41],
             "SetInformationJobObject hong ma van tra handle")
    finally:
        if cu is None: del ctypes.windll
        else: ctypes.windll = cu


@ca
def t80_job_pid_tang_buffer_khi_qua_suc_chua():
    """ERROR_MORE_DATA phải làm tăng buffer, không được thành rỗng/không đo."""
    m = _tai_launcher_thu()
    import ctypes

    class K32:
        def __init__(self): self.lan = 0
        def QueryInformationJobObject(self, _job, _lop, pds, _sz, _ret):
            self.lan += 1
            ds = pds._obj
            if self.lan == 1:
                ds.NumberOfAssignedProcesses = 100
                ds.NumberOfProcessIdsInList = 64
                return 0
            ds.NumberOfAssignedProcesses = 100
            ds.NumberOfProcessIdsInList = 100
            for i in range(100): ds.ProcessIdList[i] = i + 1
            return 1

    cu = getattr(ctypes, "windll", None)
    fake = type("Windll", (), {})(); fake.kernel32 = K32()
    ctypes.windll = fake
    try:
        bang(m._pid_trong_job(41) == list(range(1, 101)) and fake.kernel32.lan == 2,
             "job > buffer dau khong duoc doc lai dung kich thuoc")
    finally:
        if cu is None: del ctypes.windll
        else: ctypes.windll = cu


@ca
def t81_chup_cay_windows_thieu_creationdate_phai_fail_closed():
    """Không lấy được creation time: fail-closed, nhưng CHỈ khi ở TRONG cây.

    Hai vế cố ý ngược nhau. Vế (a) là bảo đảm gốc: một hậu duệ mà ta không lấy
    được khoá danh tính thì cả ảnh không đủ bằng chứng — bỏ qua im lặng sẽ làm
    ảnh rỗng thành "cả cây đã chết". Vế (b) là PHẠM VI: tiến trình mù NGOÀI cây
    không liên quan gì tới thứ ta sắp giết; để nó phá ảnh thì ảnh có dùng được
    hay không lại tuỳ trạng thái máy ở chỗ khác — mà từ khi ảnh rỗng là bằng
    chứng "đã tắt" trên Windows, đó chính là đường quyết định 0-hay-125.

    NEO ĐÃ CHUYỂN cùng bản vá bỏ WMI: nguồn quan hệ cha-con nay là
    `_cac_pid_cha_windows` (Toolhelp32) và khoá danh tính hỏi RIÊNG từng PID qua
    `_khoa_danh_tinh`. Vì thế vế (b) mạnh hơn trước: PID mù ngoài cây không chỉ
    "không phá ảnh" mà còn KHÔNG ĐƯỢC HỎI — phạm vi giờ đo được, không chỉ suy ra.

    wp766 (Codex review PR #765, tái hiện trên `9fddb1d` lẫn `80e0fac`) — PID giả
    KHÔNG được ghi cứng: `_chup_cay` cố ý bỏ `os.getpid()` khỏi ảnh, nên lượt chạy
    có PID trùng 10/11/12 (namespace PID mới) làm ca ĐỎ — getpid=11 hỏng vế (a),
    getpid=12 hỏng vế (b). Fixture nay lấy PID từ `_pid_gia_khac_minh`; `r766`
    khoá điều đó bằng cách ép `os.getpid` trùng từng PID cũ.
    """
    _than_t81()


def _pid_gia_khac_minh(n: int, tu: int = 10) -> list[int]:
    """`n` PID giả liên tiếp từ `tu`, bỏ qua PID của CHÍNH lượt chạy và PID cha.

    Đọc `os.getpid()` LÚC GỌI (không lúc nạp module) để ca ép `os.getpid` vẫn đo
    được. Tránh cả `os.getppid()` là phòng thủ: launcher hiện không loại PID cha,
    nên vế ấy không có đột biến riêng (nói thẳng, đừng đọc thành đã đo).
    """
    tranh = {os.getpid(), os.getppid()}
    ra, p = [], tu
    while len(ra) < n:
        if p not in tranh:
            ra.append(p)
        p += 1
    return ra


def _than_t81():
    m = _tai_launcher_thu()
    m.platform.system = lambda: "Windows"
    cha, goc, mu, con = _pid_gia_khac_minh(4)
    da_hoi = []
    khoa = {goc: "win:123", mu: None, con: "win:456"}

    def _khoa(pid):
        da_hoi.append(pid)
        return khoa.get(pid)

    m._khoa_danh_tinh = _khoa

    # (a) tien trinh mu la CON cua goc => khong do duoc
    m._cac_pid_cha_windows = lambda: {goc: cha, mu: goc}
    bang(m._chup_cay(goc) is None, "hau due khong lay duoc khoa bi bo qua im lang")
    # (b) tien trinh mu thuoc nhanh KHAC (cung cha voi goc) => anh van dung duoc
    da_hoi.clear()
    m._cac_pid_cha_windows = lambda: {goc: cha, con: goc, mu: cha}
    bang(m._chup_cay(goc) == {goc: "win:123", con: "win:456"},
         "tien trinh mu NGOAI cay khong duoc lam hong ca anh")
    bang(mu not in da_hoi, f"da hoi khoa cua PID ngoai cay: {da_hoi}")


@ca
def r766_t81_khong_phu_thuoc_pid_cua_luot_chay():
    """t81 phải xanh BẤT KỂ PID của lượt chạy — kể cả khi nó trùng PID giả.

    Đo trên `9fddb1d` (16-10-2026, Python 3.13.16) với fixture PID cứng 10/11/12:
    ép getpid=11 ⇒ hỏng vế (a), getpid=12 ⇒ hỏng vế (b), getpid=99999 ⇒ qua.
    Ca này ép `os.getpid` lần lượt về 1, các PID cứng cũ (10, 11, 12) và mọi PID
    mà fixture sẽ chọn khi KHÔNG bị ép, rồi chạy lại thân t81. Đột biến harness
    `pid_gia_quay_ve_ghi_cung` (bỏ phép tránh) phải làm ca này ĐỎ.
    """
    that = os.getpid
    ep = sorted({1, 10, 11, 12, *_pid_gia_khac_minh(4)})
    try:
        for p in ep:
            os.getpid = lambda p=p: p
            try:
                _than_t81()
            except TinHieuChotCa as e:
                raise TinHieuChotCa(f"getpid={p}: {e}") from None
    finally:
        os.getpid = that
    bang(os.getpid is that, "khong hoan nguyen os.getpid")


@ca
def t83_windows_me_da_tat_va_anh_chup_RONG_la_du_bang_chung():
    """`stop` một lượt ĐÃ KẾT THÚC trên Windows phải trọn vẹn, không tụt xuống 125.

    ĐO ĐƯỢC trên windows-latest 13-08: sau khi vòng 7 sửa `if not con` thành
    `con == []` (đúng — None là KHÔNG ĐO ĐƯỢC), nhánh "đã không còn chạy" dùng
    `_thanh_vien_nhom`, vốn là phép đo POSIX nên trên Windows luôn trả None ⇒
    Windows không bao giờ chạm được nhánh đó, rơi xuống `taskkill` trên một PID
    không tồn tại, rc≠0, và `t69` đỏ với 125.

    Bản vá KHÔNG được nới chốt về lại `not con`: vế thứ hai dưới đây giữ đúng
    doctrine của `t78` — không đo được thì tuyệt đối không kết luận.
    """
    m = _tai_launcher_thu()
    m._khoa_danh_tinh = lambda _pid: None          # me da tat, do duoc
    m._thanh_vien_nhom = lambda _pid: None         # phep do POSIX: mu tren Windows
    m.platform.system = lambda: "Windows"
    goi = []
    m._giet_windows = lambda *_a, **_k: (goi.append(True) or m.KetGiet(False, False, "duong giet"))

    m._chup_cay = lambda _pid: {}                  # DO DUOC va rong
    kq = m._giet_cay(12345, "win:1")
    bang(kq.tron_ven and kq.ca_cay and not goi,
         "anh chup RONG la bang chung du, khong duoc roi xuong duong giet")

    m._chup_cay = lambda _pid: None                # KHONG DO DUOC
    kq2 = m._giet_cay(12345, "win:1")
    bang(goi and not kq2.tron_ven, "None bi doc thanh rong: ket luan khong bang chung")


# --------------------------------------------------- CÔ LẬP TRẠNG THÁI TOÀN CỤC
#
# VÌ SAO CÓ KHỐI NÀY — cross-review lượt 2 nhánh môi trường, finding mức HIGH
# `launcher-tests-leak-global-module-monkeypatches`.
#
# `_tai_launcher_thu()` nạp một module launcher MỚI, nên ai cũng tưởng mỗi ca chạy
# trong hộp riêng. KHÔNG PHẢI: module mới ấy vẫn `import os, shutil, subprocess,
# platform` và nhận về ĐÚNG các singleton của tiến trình test. Nên `m.os.environ = …`
# trong một ca là sửa `os.environ` của CẢ runner, và ca nào chạy sau đọc phải bản đã
# méo.
#
# Hậu quả ĐO ĐƯỢC, không phải lo xa: sau `t85`, `subprocess.run` toàn cục bị thay, và
# cổng đột biến đổ ba mục — trong đó hai mục KHÔNG liên quan gì tới bản vá
# (`so_URL_tho_khong_chuan_hoa`, `bo_cung_hoa_dau_ra`). Người vá đã đọc nhầm hiện
# tượng ấy thành "chập chờn" vì hai lượt chạy cho hai kết quả khác nhau — thật ra hoàn
# toàn TẤT ĐỊNH, chỉ phụ thuộc bảng đột biến quyết định `t85` chạy được tới đâu.
#
# CHỮA Ở TẦNG HARNESS, KHÔNG CHỮA TỪNG CHỖ GỌI. Sửa 14 chỗ gán thì hôm nay sạch, còn
# ca thứ 15 viết tháng sau lại rò — và rò IM LẶNG, chỉ hiện ra ở một mục không liên
# quan cách đó vài trăm dòng. Ở đây runner tự chụp và tự hoàn nguyên quanh MỌI lượt
# gọi ca, nên bảo đảm không phụ thuộc trí nhớ người viết test.
#
# Lớp lỗi này CÓ TRƯỚC bản vá môi trường: `t81` trên `master` cũng để lại
# `subprocess.run` bị vá (master 5 chỗ, nhánh này 14). Master vô sự chỉ vì bảng đột
# biến của nó không có ca nào chạy sau `t81` mà cần `subprocess.run` thật.
_TOAN_CUC_CAN_CO_LAP = (
    (os, "environ"),
    (platform, "system"),
    (subprocess, "run"),
    (shutil, "which"),
    (os.path, "expanduser"),
    # Ba mục dưới để `t90` vá được QUYẾT ĐỊNH tách nhóm mà không phải gọi `setsid`
    # thật — gọi thật là đổi session của chính bộ test đang chạy.
    (os, "getpid"),
    (os, "getpgid"),
    (os, "setsid"),
)


@contextlib.contextmanager
def _co_lap_toan_cuc():
    """Chụp rồi hoàn nguyên các singleton mà ca test hay vá.

    `os.environ` được chụp bằng BẢN SAO nội dung chứ không chỉ tham chiếu: ca nào
    `os.environ["X"] = …` thay vì gán cả đối tượng thì hoàn nguyên tham chiếu KHÔNG
    xoá được mục vừa thêm.
    """
    # `hasattr` TRƯỚC khi chụp — ba mục cuối bảng (`getpgid`, `setsid`, và trên vài
    # bản cả `getpid`) là POSIX; trên Windows chúng KHÔNG TỒN TẠI.
    #
    # ĐÃ ĐO trên `windows-latest` (PR #128, sau khi gắn nhãn `windows`): bản trước gọi
    # thẳng `getattr(d, t)` nên ném `AttributeError: module 'os' has no attribute
    # 'getpgid'` NGAY Ở ĐẦU MỌI CA — **0/103**, không ca nào chạy. Nghĩa là bộ test này
    # chưa từng chạy trên Windows kể từ lúc có chốt cô lập, và không ai biết vì job
    # Windows mặc định skip.
    #
    # Cùng họ với `os.O_NOFOLLOW` mà bot review vừa bắt: đụng thuộc tính CHỈ CÓ TRÊN
    # MỘT NỀN mà không hỏi trước. Hai lần trong một ngày ⇒ ghi thành luật, đừng vá lẻ.
    cu = [(d, t, getattr(d, t)) for d, t in _TOAN_CUC_CAN_CO_LAP if hasattr(d, t)]
    thieu = [t for d, t in _TOAN_CUC_CAN_CO_LAP if not hasattr(d, t)]
    noi_dung_env = dict(os.environ)
    try:
        yield
    finally:
        for d, t, v in cu:
            setattr(d, t, v)
        # Ca test có thể GẮN THÊM một thuộc tính vốn không có trên nền này (vd `t90`
        # gán `os.setsid` giả trên Windows). Không gỡ thì nó rò sang ca sau, và rò
        # theo kiểu tệ nhất: nền tự nhận có một API mà nó không có.
        for d, t in _TOAN_CUC_CAN_CO_LAP:
            if t in thieu and hasattr(d, t):
                delattr(d, t)
        if os.environ is not None and dict(os.environ) != noi_dung_env:
            os.environ.clear()
            os.environ.update(noi_dung_env)


# ------------------------------------------------- TỰ TÁCH NHÓM TIẾN TRÌNH
#
# VÌ SAO — cross-review lượt 3, `launcher-gates-still-fail-after-global-isolation`.
# Reviewer báo suite "không in tổng kết" và cả lệnh shell đặt SAU python cũng không
# chạy. Tôi tái lập được: chạy bộ test TRONG sandbox có PID namespace thì VỎ SHELL
# GỌI NÓ CHẾT, đầu ra rỗng sạch.
#
# ĐO ĐƯỢC, cùng một sandbox:
#   python3 launcher_test.py            -> vo shell CHET, log 1 dong
#   setsid python3 launcher_test.py     -> rc=0, day du 89/89, vo shell SONG
#   vo shell trong sandbox: pid=2 pgid=1
#
# Cơ chế: `launcher.py` giết theo NHÓM (`killpg`). Ở máy thường có job control, vỏ
# shell đặt python vào NHÓM RIÊNG nên python là trưởng nhóm và bán kính sát thương
# không chạm tới shell. Trong PID namespace không có job control, python THỪA KẾ
# nhóm 1 của shell — nên một cú `killpg` của bộ test cuốn theo cả shell.
#
# Kho đã trả giá đúng lớp này: chú thích ở `t50` ghi "bộ test tự sát (exit 143),
# `finally` không chạy, launcher.py ở lại trạng thái đã đột biến và đi thẳng vào
# commit". Chốt dựng khi ấy (`start_new_session=True` cho tiến trình mồi) đủ cho máy
# thường, KHÔNG đủ khi cả python lẫn shell bị dồn vào một nhóm.
#
# CHỮA: nếu ta KHÔNG phải trưởng nhóm thì ta đang chung nhóm với người gọi ⇒ `setsid()`
# để sang session/nhóm mới. Ở máy thường ta LÀ trưởng nhóm nên chốt này KHÔNG làm gì —
# đó là lý do lỗi chưa bao giờ lộ ra ngoài sandbox, và cũng là lý do bản vá không đổi
# hành vi ở đó.
#
# KHÔNG dùng `killpg` để tự bảo vệ, và cũng KHÔNG nới bất kỳ chốt chống-giết-nhầm nào
# trong `launcher.py` — chúng là thứ kho đã trả giá để dựng.
# ------------------------------------------------------------- TỰ KHAI MÔI TRƯỜNG
#
# VÌ SAO — BA lượt cross-review liên tiếp, hai bên đo cùng một cổng ra hai kết quả
# khác nhau, mỗi bên tự nhất quán:
#
#   điều phối (ngoài/trong sandbox)  47/47 đạt · vỏ shell sống sau khi python xong
#   reviewer  (sandbox codex)        46/47     · lệnh shell sau python KHÔNG chạy
#
# Hai lượt đầu tôi đi chứng minh số của mình đúng. Cả hai lần đều đúng theo nghĩa hẹp
# và KHÔNG giải quyết được gì, vì lượt sau lại lệch tiếp. Vấn đề không phải ai đúng —
# **một cổng cho kết quả phụ thuộc nơi chạy thì chưa phải cổng**.
#
# Khối này không sửa cổng. Nó làm việc phải làm TRƯỚC: bắt cổng TỰ KHAI nó đang chạy ở
# đâu, để hai phép đo ở hai nơi SO ĐƯỢC với nhau thay vì mâu thuẫn nhau. Không có nó,
# mỗi lần lệch lại tốn một lượt review để phát hiện ra là hai người đứng hai chỗ khác nhau.
#
# NGUYÊN TẮC: mọi phép dò bọc `try` riêng và trả `None` khi không đo được. Một khối
# CHẨN ĐOÁN mà tự nó ném lỗi thì phá đúng thứ nó sinh ra để cứu. `None` nghĩa là KHÔNG
# ĐO ĐƯỢC, khác hẳn `False` — đừng gộp hai thứ đó.
def _do_an_toan(ham):
    # `Exception`, KHÔNG phải `BaseException` (cross-review lượt 6, P2). Bản trước bắt
    # `BaseException` nên `KeyboardInterrupt` và `SystemExit` phát ra TRONG một phép dò
    # bị nuốt thành `None`, rồi runner đi tiếp vào các ca có `killpg`. Biến một YÊU CẦU
    # DỪNG thành "không đo được" là đúng thứ nguy hiểm nhất khối này có thể làm: người
    # bấm Ctrl-C thường là người đang thấy nó chạy sai.
    try:
        return ham()
    except Exception:                # noqa: BLE001 - chẩn đoán KHÔNG được làm hỏng lượt chạy
        return None


def khai_moi_truong() -> dict:
    """Chụp những thứ ĐÃ CHỨNG MINH là làm đổi kết quả cổng, cộng vài thứ lân cận."""
    # TRUYỀN LAMBDA, đừng truyền thẳng `os.getpid`: tra thuộc tính xảy ra TRƯỚC lời
    # gọi, tức NGOÀI `try` của `_do_an_toan`. Trên nền thiếu hàm thì `AttributeError`
    # bay ra ngoài và giết cả khối chẩn đoán — đúng thứ khối này sinh ra để tránh.
    # `getpid`/`getppid` có trên Windows nên hôm nay chưa cắn, nhưng viết đồng nhất thì
    # lớp lỗi này không còn chỗ nấp.
    pid = _do_an_toan(lambda: os.getpid())
    pgid = _do_an_toan(lambda: os.getpgid(0))
    ppid = _do_an_toan(lambda: os.getppid())
    return {
        "he_dieu_hanh": _do_an_toan(platform.system),
        "python": _do_an_toan(lambda: sys.version.split()[0]),
        "pid": pid,
        "ppid": ppid,
        "pgid": pgid,
        "sid": _do_an_toan(lambda: os.getsid(0)),
        # TRỌNG TÂM: ta có chung nhóm với TIẾN TRÌNH GỌI không. Chung nhóm thì một cú
        # `killpg` của ca test với tới cả nó — đó là kịch bản đã đo thấy giết vỏ shell.
        "la_truong_nhom": None if (pid is None or pgid is None) else pid == pgid,
        "chung_nhom_voi_cha": _do_an_toan(
            lambda: os.getpgid(0) == os.getpgid(os.getppid())),
        # Job control: không có thì vỏ shell KHÔNG đặt con vào nhóm riêng.
        "co_job_control": _do_an_toan(lambda: os.tcgetpgrp(0) >= 0),
        "stdin_la_tty": _do_an_toan(lambda: os.isatty(0)),
        "stdout_la_tty": _do_an_toan(lambda: os.isatty(1)),
        # PID namespace — GIÁ TRỊ THÔ, KHÔNG suy ra boolean.
        #
        # Bản đầu của tôi tính `trong_pid_namespace` bằng cách so ns của mình với ns của
        # `/proc/1`. SAI, và bản khai tự phơi ra ngay lượt chạy đầu: TRONG một namespace
        # thì `/proc/1` cũng thuộc chính namespace ấy, nên phép so LUÔN bằng nhau và cờ
        # luôn `false` — kể cả khi đang ở namespace riêng thật.
        #
        # Thứ THẬT SỰ phân biệt là so INODE GIỮA HAI MÁY: đo được `pid:[4026531836]` ở
        # phiên điều phối và `pid:[4026532315]` trong sandbox codex. Không phép dò tại
        # chỗ nào nói được điều đó — phải đặt hai bản khai cạnh nhau. Đó đúng là lý do
        # khối này tồn tại, nên ở đây CHỈ ghi số thô và để việc so cho người đọc.
        "ns_pid": _do_an_toan(lambda: os.readlink("/proc/self/ns/pid")),
        "ns_pid_cua_init": _do_an_toan(lambda: os.readlink("/proc/1/ns/pid")),
        "tien_trinh_1_la": _do_an_toan(
            lambda: open("/proc/1/comm", encoding="utf-8").read().strip()),
        "co_dockerenv": _do_an_toan(lambda: os.path.exists("/.dockerenv")),
        "so_cpu": _do_an_toan(os.cpu_count),
    }


def _mot_dong_moi_truong(mt: dict) -> str:
    """Một dòng gọn để LUÔN in — đủ phân biệt hai môi trường đã gây tranh cãi."""
    def g(k):
        v = mt.get(k)
        return "?" if v is None else v
    return (f"moi truong: pid={g('pid')} pgid={g('pgid')} sid={g('sid')} "
            f"truong_nhom={g('la_truong_nhom')} chung_nhom_voi_cha={g('chung_nhom_voi_cha')} "
            f"job_control={g('co_job_control')} ns_pid={g('ns_pid')} "
            f"init={g('tien_trinh_1_la')}")


def _la_truong_nhom() -> bool:
    """True nếu tiến trình này là TRƯỞNG NHÓM (pid == pgid)."""
    try:
        return os.getpid() == os.getpgid(0)
    except (OSError, AttributeError):
        return True          # không đo được thì coi như an toàn, ĐỪNG tự ý setsid


def _tu_tach_nhom_neu_can() -> str:
    """Tách sang session mới khi đang chung nhóm với vỏ shell gọi mình.

    Trả về chuỗi mô tả để IN RA — im lặng ở đây là tự tước mất bằng chứng, mà cả
    đợt review này xoay quanh đúng chuyện đó.
    """
    if os.name != "posix":
        return "bo qua (khong phai POSIX)"
    if _la_truong_nhom():
        return "khong can (da la truong nhom)"
    try:
        os.setsid()
    except OSError as e:
        return f"KHONG tach duoc ({type(e).__name__}) - killpg co the giet vo shell"
    return f"da tach sang session moi (pgid={os.getpgid(0)})"


def _dot_bien_du_san(tong: int, khong_do: int) -> bool:
    """Ít nhất 70% đột biến phải đo được trên mỗi nền."""
    m = _tai_launcher_thu()
    nguong = m.TY_LE_DOT_BIEN_TOI_THIEU_PHAN_MUOI
    return tong > 0 and (tong - khong_do) * 10 >= tong * nguong


@ca
def t82_dot_bien_khong_duoc_mat_qua_30_phan_tram():
    bang(_dot_bien_du_san(35, 10), "moc Windows da do 25/35 phai duoc chap nhan")
    bang(not _dot_bien_du_san(35, 11), "24/35 (<70%) phai lam cong do")
    bang(not _dot_bien_du_san(35, 30), "5/35 khong duoc xanh")


@ca
def t84_nhom_van_tay_khong_duoc_bat_oan_co_bat_tat():
    """Nhóm trùng vân tay chỉ được phán về CREDENTIAL, không phán về cờ bật/tắt.

    Bản nháp gom mọi biến theo vân tay rồi báo "nghi giữ chỗ" cho nhóm >= 3. Đo
    thật trong container thì nó báo oan hai nhóm to: tám biến cùng là `"1"` và
    chín biến cùng là `"true"`. Giá trị ngắn trùng nhau là chuyện thường.

    Ca này khoá CẢ HAI chiều: cờ bật/tắt KHÔNG bị gom, còn chuỗi giữ chỗ THẬT
    (14 ký tự, dùng lại cho năm dịch vụ — đo được 15-08-2026) thì PHẢI bị gom.
    """
    m = _tai_launcher_thu()
    m.os.environ = {
        "CLAUDE_CODE_DEBUG": "true", "CLAUDE_CODE_REMOTE": "true",
        "CLAUDE_AUTO_BACKGROUND_TASKS": "true",          # ba cờ, cùng giá trị
        "GH_TOKEN": "khong-phai-that", "GITHUB_TOKEN": "khong-phai-that",
        "AWS_SECRET_ACCESS_KEY": "khong-phai-that",      # ba credential, cùng giá trị
        "GITHUB_PAT": "github_pat_gia_dinh_dai_that_su", # credential RIÊNG
    }
    nhom = m._nhom_van_tay(sorted(m.os.environ))
    gom = {k: sorted(v) for k, v in nhom.items() if len(v) >= 3}
    bang(len(gom) == 1, f"chi duoc gom DUNG mot nhom credential, thuc te {gom}")
    ds = next(iter(gom.values()))
    bang(ds == ["AWS_SECRET_ACCESS_KEY", "GH_TOKEN", "GITHUB_TOKEN"],
         f"gom sai danh sach: {ds}")
    bang(all("CLAUDE" not in t for v in nhom.values() for t in v),
         "co bat/tat bi gom nham vao nhom giu cho")


@ca
def t85_do_codex_khong_duoc_fail_open_khi_dong_dau_la_canh_bao():
    """`codex` chưa đăng nhập mà báo DUNG_DUOC là hỏng theo chiều NGUY HIỂM.

    Bản nháp đọc `ra[0]` rồi tìm "not logged in" trong ĐÓ. Với `HOME` sạch,
    `codex` in trước một dòng `WARNING: … could not create PATH aliases`, nên
    dòng đầu không phải câu trạng thái và phép kiểm trượt → báo DUNG_DUOC cho
    một `codex` CHƯA xác thực. Đúng cùng lỗi với sự cố sáng 15-08-2026: tin
    dòng đầu tiên một công cụ nói ra.
    """
    m = _tai_launcher_thu()
    m._dang_cho_snapshot = lambda home: False  # Recovery is measured by g2 dedicated cases.
    m._codex_home_hieu_luc = lambda: Path("INERT-HOME")
    m.shutil.which = lambda t: "/usr/bin/codex" if t == "codex" else None
    # Ghim HẠN TOKEN thay vì đọc `~/.codex/auth.json` THẬT: ca này đo phép kiểm DÒNG
    # ĐẦU, không đo credential của máy đang chạy. Không ghim thì nó xanh/đỏ tuỳ máy —
    # đúng bệnh "cổng phụ thuộc môi trường" mà đợt này vừa mất ba lượt vì nó.
    m._han_token_codex = lambda: {"doc_duoc": True, "last_refresh": "x",
                                  "gio_con_lai": {"access_token": 100.0}}

    def _ra(rc, text):
        class P:
            returncode = rc
            stdout = text
            stderr = ""
        m.subprocess.run = lambda *_a, **_k: P()

    canh_bao = ("WARNING: proceeding, even though we could not create PATH "
                "aliases: Refusing to create helper binaries\n")
    # (a) chua dang nhap, CO bien -> phai doi chuan-bi, TUYET DOI khong DUNG_DUOC
    m.os.environ = {"CODEX_AUTH_JSON": "xxxx"}
    _ra(1, canh_bao + "Not logged in\n")
    tt, _ = m._do_codex()
    bang(tt == "CAN_CHUAN_BI", f"co bien + chua dang nhap phai la CAN_CHUAN_BI, duoc {tt}")
    # (b) chua dang nhap, KHONG bien
    m.os.environ = {}
    _ra(1, canh_bao + "Not logged in\n")
    tt, _ = m._do_codex()
    bang(tt == "CHUA_XAC_THUC", f"khong bien phai la CHUA_XAC_THUC, duoc {tt}")
    # (c) da dang nhap => CO_CREDENTIAL, KHONG phai DUNG_DUOC.
    # Hop dong DOI o dot `token_revoked` 15-08: `login status` rc=0 chi chung minh CO
    # credential doc duoc, KHONG chung minh no con DUNG DUOC. `DUNG_DUOC` nay doi
    # `--kiem-song` (goi that). Xem `t93`.
    _ra(0, "Logged in using ChatGPT\n")
    tt, mo_ta = m._do_codex()
    bang(tt == "CO_CREDENTIAL", f"da dang nhap phai la CO_CREDENTIAL, duoc {tt}")
    bang("Logged in" in mo_ta, f"mo ta phai lay dong TRANG THAI, duoc {mo_ta!r}")
    # (d) rc=0 nhung van co chu 'not logged in' => fail-closed
    _ra(0, canh_bao + "Not logged in\n")
    m.os.environ = {}
    tt, _ = m._do_codex()
    bang(tt == "CHUA_XAC_THUC", f"rc=0 ma noi chua dang nhap thi phai fail-closed, duoc {tt}")


# wp858 (L2, đo 21-10-2026): phiên Codex đang sống gắn tmpfs ro lên `/tmp/.git` ⇒ `_KhoCodex` từ chối ĐÚNG mọi home dưới
# `/tmp` ⇒ `t86` đỏ "khi song song" (#831). Ca chọn gốc tạm không có `.git` ở chính nó hay tổ tiên.
_WP858_GOC_TAM_UNG_VIEN = (tempfile.gettempdir(), "/var/tmp", "/dev/shm")


def _goc_tam_khong_git(ung_vien):
    """Thư mục ĐẦU TIÊN tồn tại mà nó và mọi tổ tiên đều KHÔNG có `.git` (kể cả symlink hỏng); không có ⇒ None."""
    for u in ung_vien:
        p = Path(u)
        if p.is_dir() and not any(os.path.lexists(q / ".git") for q in (p, *p.parents)):
            return str(p)
    return None


@ca
def r858_goc_tam_tranh_to_tien_co_git():
    """N5 (L2): bộ chọn gốc tạm của `t86` bỏ ứng viên có `.git` ở CHÍNH nó hoặc ở tổ tiên; hết ứng viên ⇒ None."""
    goc = _goc_tam_khong_git(_WP858_GOC_TAM_UNG_VIEN)
    bang(goc is not None, f"KHONG DO DUOC: moi goc tam ung vien deu nam duoi mot `.git` ({_WP858_GOC_TAM_UNG_VIEN})")
    s = Path(tempfile.mkdtemp(prefix="lt_", dir=goc))
    try:
        co_git, sach = s / "co_git", s / "sach"
        (co_git / ".git").mkdir(parents=True)
        (co_git / "con" / "chau").mkdir(parents=True)
        sach.mkdir()
        bang(_goc_tam_khong_git([str(co_git / "con" / "chau"), str(sach)]) == str(sach),
             "to tien co .git van duoc chon lam goc tam")
        bang(_goc_tam_khong_git([str(co_git), str(sach)]) == str(sach), "goc co .git van duoc chon")
        bang(_goc_tam_khong_git([str(s / "vang"), str(co_git / "con")]) is None,
             "khong ung vien sach ma van tra goc")
    finally:
        shutil.rmtree(s, ignore_errors=True)


@ca
def t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac():
    """Sáng 15-08-2026 tôi ghi base64 THÔ vào `auth.json`, `codex` trả `expected
    value at line 1 column 1`, và tôi đọc thành "biến này không dùng được" — trong
    khi nó chỉ nói tệp không phải JSON. Hàm phải thử CẢ HAI đường, và khi cả hai
    hỏng thì nói rõ đã thử những gì.

    Ghi ra ĐĨA nên ca này dùng HOME TẠM. Không bao giờ đụng `~` thật: đột biến ghi
    vào tệp thật rồi khôi phục trong `finally` là bom hẹn giờ (CLAUDE.md).
    """
    import base64 as _b64
    m = _tai_launcher_thu()
    that = '{"tokens":{"access":"gia-dinh"}}'
    goc = _goc_tam_khong_git(_WP858_GOC_TAM_UNG_VIEN)
    bang(goc is not None, "KHONG DO DUOC: moi goc tam ung vien deu nam duoi mot `.git` "
                          f"({_WP858_GOC_TAM_UNG_VIEN}) — _KhoCodex se tu choi dung thiet ke")
    for ten, gia_tri in (("base64", _b64.b64encode(that.encode()).decode()),
                         ("json tho", that)):
        nha = tempfile.mkdtemp(dir=goc)
        m.os.path.expanduser = (lambda n: lambda p: p.replace("~", n))(nha)
        m.os.environ = {"CODEX_AUTH_JSON": gia_tri}
        ket = m.chuan_bi_xac_thuc(that_su=True)
        bang(len(ket) == 1 and ket[0]["ok"], f"{ten}: phai dung duoc, duoc {ket}")
        dich = Path(nha) / ".codex" / "auth.json"
        bang(dich.read_text(encoding="utf-8") == that,
             f"{ten}: noi dung tren dia phai la JSON GIAI MA, khong phai chuoi tho")
        # Quyền 600 là khái niệm POSIX. Trên Windows `os.chmod` CHỈ bật/tắt cờ
        # read-only, nên `st_mode & 0o777` không bao giờ ra 600 — khẳng định cũ đỏ
        # trên `windows-latest` (đo được PR #128, lượt Windows THẬT đầu tiên).
        #
        # ĐỪNG đọc đây thành "Windows cũng an toàn": nó KHÔNG được `chmod` bảo vệ.
        # Thứ che `~/.codex/auth.json` ở đó là ACL của chính hồ sơ người dùng, mà ta
        # KHÔNG đặt và KHÔNG kiểm. Ghi ra để không ai suy "test xanh = đã bảo vệ".
        if LA_WINDOWS:
            bang(dich.exists(), f"{ten}: tep phai ton tai")
        else:
            bang(oct(dich.stat().st_mode)[-3:] == "600", f"{ten}: quyen phai la 600")
        # idempotent: goi lai khong duoc bao da doi
        bang(m.chuan_bi_xac_thuc(that_su=True)[0].get("doi") is False,
             f"{ten}: goi lai phai nhan ra da khop va khong dung tep")
    # rac => tu choi, va noi ro da thu CA HAI duong
    nha = tempfile.mkdtemp(dir=goc)
    m.os.path.expanduser = (lambda n: lambda p: p.replace("~", n))(nha)
    m.os.environ = {"CODEX_AUTH_JSON": "!!khong-phai-gi-ca!!"}
    ket = m.chuan_bi_xac_thuc(that_su=True)
    bang(not ket[0]["ok"], "rac phai bi tu choi")
    bang("base64" in ket[0]["cach"] and "JSON" in ket[0]["cach"],
         f"thong diep phai neu CA HAI duong da thu, duoc {ket[0]['cach']!r}")
    bang(not (Path(nha) / ".codex" / "auth.json").exists(),
         "tu choi ma van ghi tep la fail-open")


@ca
def t87_khong_duoc_xuat_digest_on_dinh_cua_gia_tri_bien():
    """Đầu ra KHÔNG được chứa thứ băm ngoại tuyến được — cross-review, mức HIGH.

    `deterministic-secret-fingerprint-is-dictionary-oracle`: bản trước xuất 8 hex đầu
    của **sha256 trần** cho mọi biến khớp mẫu, kèm độ dài chính xác. Với biến có tập
    ứng viên nhỏ, kẻ đọc transcript băm ngoại tuyến từng ứng viên rồi so 32 bit là ra
    giá trị; digest ổn định còn cho phép NỐI một biến qua nhiều transcript.

    Ngưỡng độ dài khi ấy chỉ nằm ở `_nhom_van_tay` (phép GOM), trong khi digest được
    xuất ở `quet_bien_moi_truong` — chốt đặt một chỗ, rò ở chỗ khác.

    Ca này đóng bằng PHẢN CHỨNG TỪ ĐIỂN, không bằng việc đọc mã: bơm giá trị đã biết
    rồi đòi sha256 của nó KHÔNG xuất hiện trong đầu ra.
    """
    m = _tai_launcher_thu()
    bi_mat = "gia-tri-biet-truoc-de-thu"
    m.os.environ = {
        "TL_TOKEN_THU": bi_mat, "TL_SECRET_THU": bi_mat, "TL_AUTH_THU": bi_mat,
        "TL_NGAN_SECRET": "abc",
        "PATH": "/usr/bin",
    }
    q = m.quet_bien_moi_truong()
    xuat = json.dumps(q, ensure_ascii=False)

    tho = hashlib.sha256(bi_mat.encode()).hexdigest()
    bang(tho[:8] not in xuat, "sha256 TRAN cua gia tri VAN xuat hien trong dau ra")
    bang("van_tay" not in xuat, "truong `van_tay` van con trong dau ra")
    # Phép GOM vẫn phải hoạt động — bịt rò không được làm mù phép kiểm.
    ds = [b for b in q["bien"] if b["ten"].startswith("TL_") and b["nhom"]]
    bang(len(ds) == 3, f"van phai gom dung ba bien trung gia tri, duoc {len(ds)}")
    bang({b["nhom"] for b in ds} == {"nhom-1"}, "ba bien trung phai cung MOT nhan nhom")
    # Độ dài giá trị NGẮN phải bị gộp, không xuất con số chính xác.
    ngan = [b for b in q["bien"] if b["ten"] == "TL_NGAN_SECRET"][0]
    bang(ngan["do_dai"] == f"<{m.NGUONG_DO_DAI_BI_MAT}",
         f"do dai gia tri ngan phai duoc gop, duoc {ngan['do_dai']!r}")
    # Nhãn nội bộ phải đổi theo TIẾN TRÌNH: cùng giá trị, hai khoá khác nhau ⇒ khác nhãn.
    m2 = _tai_launcher_thu()
    bang(m._van_tay(bi_mat) != m2._van_tay(bi_mat),
         "nhan noi bo GIONG NHAU giua hai tien trinh — khoa khong ngau nhien, oracle con song")


@ca
def t88_hook_phien_do_theo_NANG_LUC_khong_theo_bam_toan_tep():
    """Chốt `hook-phien` phải im khi khác biệt VÔ HẠI, và kêu khi THIẾU năng lực.

    Bản trước so `sha256` cả tệp; cross-review bác đúng: sửa một dấu phẩy trong chú
    thích cũng làm chốt đỏ, mà chốt đỏ vì lý do vô hại là chốt sẽ bị bỏ qua.

    Reviewer cũng loại sẵn đường chữa dễ nghĩ nhất: quan hệ TỔ TIÊN commit KHÔNG đủ,
    vì chính nhánh packet cũ mới là thứ cần cảnh báo mà nó LÀ tổ tiên hợp lệ của
    master. Nên hợp đồng là TẬP TÊN NĂNG LỰC khai trong chính hook.

    Ca này khoá cả hai chiều — im khi vô hại, kêu khi thiếu — vì chữa một chiều bằng
    cách nới chiều kia là đúng thứ con lắc doctrine của kho đã dạy.
    """
    m = _tai_launcher_thu()
    MASTER = ("#!/bin/bash\n"
              "# hook-nang-luc: codex-auth-restore rg-bat-buoc doctor-kha-dung\n"
              "echo hi\n")

    def do(hook_cuc_bo, hook_master=MASTER):
        d = Path(tempfile.mkdtemp())
        (d / ".claude/hooks").mkdir(parents=True)
        (d / ".claude/hooks/session-start.sh").write_text(hook_cuc_bo, encoding="utf-8")
        m._git = lambda ws, *a: ((0, hook_master, "") if hook_master else (1, "", "x"))
        return m._do_hook_cu(str(d))

    tt, _ = do(MASTER)
    bang(tt == "DUNG_DUOC", f"hook y het master phai xanh, duoc {tt}")

    # ĐÂY LÀ CA REVIEWER NÊU: khác biệt vô hại KHÔNG được làm đỏ.
    tt, _ = do(MASTER.replace("echo hi", "echo hi  # chu thich vo hai\n# them dau phay,"))
    bang(tt == "DUNG_DUOC", f"doi CHU THICH khong duoc lam do, duoc {tt}")

    tt, mo_ta = do("#!/bin/bash\n# hook-nang-luc: rg-bat-buoc doctor-kha-dung\necho hi\n")
    bang(tt == "CHUA_XAC_THUC", f"thieu nang luc phai do, duoc {tt}")
    bang("codex-auth-restore" in mo_ta, f"phai NEU TEN nang luc thieu, duoc {mo_ta!r}")

    # Hook cũ của nhánh packet: không có dòng khai ⇒ thiếu TẤT CẢ.
    tt, mo_ta = do("#!/bin/bash\necho hi\n")
    bang(tt == "CHUA_XAC_THUC", f"hook cu khong khai gi phai do, duoc {tt}")
    bang(all(x in mo_ta for x in ("codex-auth-restore", "rg-bat-buoc", "doctor-kha-dung")),
         f"phai neu du ba nang luc thieu, duoc {mo_ta!r}")

    # Hook MỚI HƠN master không phải lỗi.
    tt, _ = do(MASTER.replace("doctor-kha-dung", "doctor-kha-dung dieu-moi"))
    bang(tt == "DUNG_DUOC", f"hook moi hon master phai xanh, duoc {tt}")

    # Master chưa khai ⇒ nói KHÔNG ĐO ĐƯỢC, KHÔNG được tụt về so băm.
    tt, _ = do(MASTER, "#!/bin/bash\necho hi\n")
    bang(tt == "KHONG_DO_DUOC", f"master chua khai thi phai KHONG_DO_DUOC, duoc {tt}")

    # Và hook THẬT của kho phải khai đủ ba năng lực — nếu ai xoá dòng đó thì ca này đỏ.
    that = Path(__file__).resolve().parents[2] / ".claude/hooks/session-start.sh"
    if that.exists():
        nl = m._nang_luc_hook(that.read_text(encoding="utf-8", errors="replace"))
        bang({"codex-auth-restore", "rg-bat-buoc", "doctor-kha-dung"} <= nl,
             f"hook THAT cua kho khai thieu nang luc: {sorted(nl)}")


@ca
def t89_harness_phai_hoan_nguyen_trang_thai_toan_cuc():
    """Runner phải tự cô lập — không được tin ca test nhớ dọn sau mình.

    Cross-review lượt 2, `launcher-tests-leak-global-module-monkeypatches` (HIGH):
    `_tai_launcher_thu()` nạp module launcher MỚI nhưng module ấy dùng CHÍNH các
    singleton `os` `platform` `subprocess` `shutil` của tiến trình test. Nên
    `m.subprocess.run = …` trong một ca là sửa `subprocess.run` của cả runner, và
    cổng đột biến đổ ở những mục KHÔNG liên quan.

    Ca này đo CHÍNH `_co_lap_toan_cuc`, không đo từng ca gọi nó — vì chốt đặt ở
    harness thì thứ cần khoá cũng là harness. Bỏ chốt đi thì ca này đỏ.

    Lưu ý một chiều dễ quên: `os.environ` phải hoàn nguyên cả NỘI DUNG, không chỉ
    tham chiếu — ca nào `os.environ["X"] = …` thay vì gán cả đối tượng thì trả lại
    tham chiếu cũ KHÔNG xoá được mục vừa thêm.
    """
    goc = (subprocess.run, shutil.which, platform.system, os.path.expanduser)
    env_goc = dict(os.environ)
    ten_la = "TL_CA_T89_KHONG_DUOC_SONG_SOT"
    bang(ten_la not in os.environ, "moi truong da co bien thu nghiem tu truoc")

    with _co_lap_toan_cuc():
        subprocess.run = lambda *a, **k: None
        shutil.which = lambda t: None
        platform.system = lambda: "Plan9"
        os.path.expanduser = lambda p: "/khong-co-that"
        os.environ[ten_la] = "1"          # THEM muc, khong gan ca doi tuong
        bang(platform.system() == "Plan9", "va trong khoi co lap phai co hieu luc")

    bang((subprocess.run, shutil.which, platform.system, os.path.expanduser) == goc,
         "singleton KHONG duoc hoan nguyen sau khoi co lap")
    bang(ten_la not in os.environ,
         "muc THEM vao os.environ song sot — hoan nguyen tham chieu la CHUA DU")
    bang(dict(os.environ) == env_goc, "noi dung os.environ bi doi sau khoi co lap")

    # Ngoại lệ ném ra giữa chừng cũng phải hoàn nguyên (đó là lý do dùng `finally`).
    try:
        with _co_lap_toan_cuc():
            platform.system = lambda: "Haiku"
            raise RuntimeError("vo tinh")
    except RuntimeError:
        pass
    bang(platform.system is goc[2], "ngoai le giua chung ma KHONG hoan nguyen")


@ca
def t90_tu_tach_nhom_khi_chung_nhom_voi_vo_shell():
    """Bộ test phải tự tách nhóm khi nó chung nhóm với người gọi.

    Cross-review lượt 3: trong sandbox có PID namespace, vỏ shell là `pid=2 pgid=1`
    và python thừa kế nhóm 1 của nó, nên một cú `killpg` của ca test GIẾT LUÔN VỎ
    SHELL — đo được: chạy trực tiếp thì shell chết và đầu ra rỗng, còn
    `setsid python3 …` thì rc=0 và đủ `89/89`.

    Ca này vá `os.getpid`/`os.getpgid`/`os.setsid` (đã nằm trong danh sách cô lập)
    để đo QUYẾT ĐỊNH chứ không gọi `setsid` thật — gọi thật là đổi session của chính
    bộ test đang chạy.

    Khoá cả bốn nhánh, vì chữa một chiều mà nới chiều kia là bệnh kinh niên của kho:
    chung nhóm thì PHẢI tách; là trưởng nhóm thì KHÔNG được đụng vào; `setsid` hỏng
    thì phải NÓI RA chứ không im lặng; và không POSIX thì bỏ qua.
    """
    # Chot nay nam trong CHINH tep test (harness), khong nam trong launcher.py —
    # nen va thang vao `os` toan cuc. An toan vi `os.getpid`/`getpgid`/`setsid`
    # deu nam trong `_TOAN_CUC_CAN_CO_LAP`, runner hoan nguyen sau moi ca.
    # GHIM `os.name`: `_tu_tach_nhom_neu_can` thoát NGAY ở dòng đầu khi không POSIX,
    # nên trên `windows-latest` cả ba nhánh (a)(b)(c) đỏ hết — đo được ở lượt Windows
    # THẬT đầu tiên (PR #128). Ghim vào thì bốn nhánh QUYẾT ĐỊNH được đo trên MỌI nền,
    # thay vì Windows chỉ đo được đúng nhánh "bỏ qua". Trả lại trong `finally`.
    goc_name = os.name

    def dung_canh(pid, pgid, setsid_hong=False):
        goi = []
        os.name = "posix"
        os.getpid = lambda: pid
        os.getpgid = lambda _: pgid

        def _setsid():
            goi.append(1)
            if setsid_hong:
                raise PermissionError("EPERM")
        os.setsid = _setsid
        return goi

    # (a) CHUNG nhom voi vo shell (pid != pgid) => PHAI tach
    goi = dung_canh(2, 1)
    kq = _tu_tach_nhom_neu_can()
    bang(len(goi) == 1, f"chung nhom ma KHONG goi setsid: {kq!r}")
    bang("da tach" in kq, f"mo ta phai noi da tach, duoc {kq!r}")

    # (b) DA la truong nhom => TUYET DOI khong dung vao
    goi = dung_canh(500, 500)
    kq = _tu_tach_nhom_neu_can()
    bang(len(goi) == 0, f"la truong nhom ma VAN goi setsid: {kq!r}")
    bang("khong can" in kq, f"mo ta sai: {kq!r}")

    # (c) setsid HONG => phai NOI RA, khong im lang
    goi = dung_canh(2, 1, setsid_hong=True)
    kq = _tu_tach_nhom_neu_can()
    bang(len(goi) == 1, "phai co thu goi setsid")
    bang("KHONG tach duoc" in kq and "killpg" in kq,
         f"setsid hong ma khong canh bao ro: {kq!r}")

    # (d) khong do duoc pgid => coi nhu an toan, DUNG tu y setsid
    os.getpgid = lambda _: (_ for _ in ()).throw(OSError("khong do duoc"))
    bang(_la_truong_nhom() is True, "khong do duoc pgid thi phai coi la truong nhom")

    # (e) KHONG POSIX => bo qua, va TUYET DOI khong goi setsid
    goi = dung_canh(2, 1)
    os.name = "nt"
    try:
        kq = _tu_tach_nhom_neu_can()
        bang(len(goi) == 0, f"khong POSIX ma VAN goi setsid: {kq!r}")
        bang("khong phai POSIX" in kq, f"mo ta phai noi ro ly do, duoc {kq!r}")
    finally:
        os.name = goc_name


@ca
def t91_ban_khai_moi_truong_khong_duoc_chet_va_khong_duoc_doan():
    """Bản khai phải SỐNG SÓT mọi phép dò hỏng, và phải phân biệt KHÔNG ĐO ĐƯỢC với FALSE.

    Khối này sinh ra vì BA lượt review liên tiếp hai bên đo ra hai kết quả khác nhau mà
    không ai biết mình đứng đâu. Nếu chính nó ném lỗi thì nó phá đúng thứ nó sinh ra để
    cứu — nên ca này ép TỪNG phép dò hỏng và đòi bản khai vẫn ra.

    `None` (không đo được) KHÁC `False` (đo được, và là không). Gộp hai thứ đó lại là
    đúng kiểu sai đã làm tôi mất ba lượt: đọc một quan sát thiếu thành một kết luận.
    """
    # `getpgid` là POSIX — trên Windows nó KHÔNG TỒN TẠI, nên chụp thẳng là ném
    # `AttributeError` và ca này chết ở dòng đầu. Đúng lớp lỗi vừa làm suite 0/103 trên
    # `windows-latest`. Ở đây ta ÉP HỎNG các phép dò, mà "không có hàm" cũng là một
    # kiểu hỏng — nên trên nền thiếu hàm thì bản khai vẫn phải ra, và đó chính là điều
    # ca này đo. Dùng `getattr` để không đòi hỏi nền phải có.
    goc_readlink = os.readlink
    goc_getpgid = getattr(os, "getpgid", None)
    goc_open = __builtins__["open"] if isinstance(__builtins__, dict) else __builtins__.open

    def no(*_a, **_k):
        raise OSError("ep hong de thu")

    # (a) mọi phép dò hỏng ⇒ VẪN ra bản khai, không ném
    os.readlink = no
    os.getpgid = no
    mt = khai_moi_truong()
    bang(isinstance(mt, dict) and mt, "moi phep do hong ma ban khai KHONG ra")
    bang(mt["ns_pid"] is None, f"do hong phai la None, duoc {mt['ns_pid']!r}")
    bang(mt["chung_nhom_voi_cha"] is None,
         f"do hong phai la None chu khong phai False, duoc {mt['chung_nhom_voi_cha']!r}")
    bang(mt["he_dieu_hanh"] is not None, "phep do KHONG hong cung bi keo theo")
    os.readlink = goc_readlink
    if goc_getpgid is None:
        del os.getpgid                  # nen KHONG co san: tra lai dung trang thai cu
    else:
        os.getpgid = goc_getpgid

    # (b) một dòng tóm tắt phải in được kể cả khi thiếu, và hiện `?` chứ không vỡ
    dong = _mot_dong_moi_truong({"pid": 1})
    bang("pid=1" in dong and "?" in dong, f"dong tom tat sai: {dong!r}")

    # (c) đo THẬT: những khoá đã dùng để so hai môi trường phải có mặt
    mt = khai_moi_truong()
    for k in ("pid", "pgid", "sid", "la_truong_nhom", "chung_nhom_voi_cha", "ns_pid"):
        bang(k in mt, f"ban khai thieu khoa {k!r} — khoa nay dung de so hai moi truong")
    bang(mt["pid"] == os.getpid(), "pid khai sai")

    # (d) `_do_an_toan` KHONG duoc nuot YEU CAU DUNG (cross-review luot 6, P2).
    # Ban truoc bat `BaseException`, nen Ctrl-C phat ra trong mot phep do bi doi
    # thanh `None` va runner di tiep vao cac ca co `killpg`. Nguoi bam Ctrl-C
    # thuong la nguoi dang thay no chay sai — nuot dung ho la te nhat.
    bang(_do_an_toan(lambda: 1 / 0) is None, "loi thuong phai thanh None")
    for loai in (KeyboardInterrupt, SystemExit):
        da_thoat = False
        try:
            _do_an_toan(lambda: (_ for _ in ()).throw(loai()))
        except BaseException as e:      # noqa: BLE001 - dang do CHINH viec nay
            da_thoat = isinstance(e, loai)
        bang(da_thoat, f"{loai.__name__} bi NUOT thanh 'khong do duoc'")


@ca
def t92_khong_duoc_killpg_khi_pid_KHONG_phai_truong_nhom():
    """`killpg` nhận PROCESS GROUP ID, ta cầm PID — chỉ bằng nhau khi là trưởng nhóm.

    Truy từ manh mối cross-review lượt 4 (`launcher.py:720` và `:739`). ĐO ĐƯỢC trên
    bản trước: con sinh KHÔNG kèm `start_new_session` có pid=26072 pgid=26071, mà
    `_giet_cay` vẫn gọi thẳng `killpg(26072)` — nhắm vào một nhóm KHÔNG PHẢI nhóm của
    mục tiêu.

    Máy thường pid cỡ vài chục nghìn nên nhóm ấy hầu như không tồn tại và lỗi tan thành
    `ProcessLookupError`. Trong PID NAMESPACE pid chạy từ 1, nên `killpg(<số nhỏ>)` rất
    dễ trúng một nhóm CÓ THẬT — kể cả nhóm 1 của chính vỏ shell. Khớp triệu chứng đo
    được ba lượt: bộ test chạy xong mà lệnh shell kế tiếp không bao giờ chạy.

    Ca này ghi lại `killpg` thay vì giết thật, và khoá CẢ HAI chiều — không phải trưởng
    nhóm thì TỪ CHỐI và TUYỆT ĐỐI không gọi `killpg`; là trưởng nhóm thì vẫn phải giết
    như cũ, kẻo chữa lỗ này bằng cách làm chốt giết thôi hoạt động.
    """
    m = _tai_launcher_thu()
    ghi = []
    m.os.killpg = lambda g, sig: ghi.append(g)
    m._giet_rieng = lambda *a, **k: None
    m._chup_cay = lambda p: {}
    m._thanh_vien_nhom = lambda p: []
    # `_con_song(pid, khoa)` nhan HAI doi so o duong Windows; fixture mot doi so nem
    # `TypeError` — do duoc o luot Windows THAT dau tien (PR #128).
    m._con_song = lambda p, khoa=None: False
    m._khoa_danh_tinh = lambda p: "x"
    # `_giet_cay` re sang `_giet_windows` TRUOC ca chot truong nhom, nen tren Windows
    # ca nay khong do duoc thu no sinh ra de do. Ghim nen: `platform.system` nam trong
    # `_TOAN_CUC_CAN_CO_LAP` nen runner hoan nguyen sau ca.
    m.platform.system = lambda: "Linux"

    # (a) pgid != pid  => TU CHOI, khong duoc goi killpg
    m.os.getpgid = lambda p: p - 1
    kq = m._giet_cay(500, "x")
    bang(ghi == [], f"KHONG phai truong nhom ma VAN goi killpg: {ghi}")
    bang(getattr(kq, "tu_choi", False) is True, f"phai TU CHOI, duoc {kq}")
    bang("truong nhom" in str(kq), f"thong diep phai noi ro ly do, duoc {str(kq)!r}")

    # (b) pgid == pid => van phai giet nhu cu
    ghi.clear()
    m.os.getpgid = lambda p: p
    kq = m._giet_cay(500, "x")
    bang(ghi and ghi[0] == 500, f"la truong nhom ma KHONG giet: {ghi} / {kq}")
    bang(getattr(kq, "tu_choi", False) is False, f"la truong nhom ma lai tu choi: {kq}")

    # (c) KHONG do duoc pgid => KHONG duoc killpg, NHUNG VAN phai giet tung pid
    #
    # Ban dau ca nay ghim dung nguoc lai: "khong do duoc thi DI TIEP", tuc VAN goi
    # killpg. Cross-review luot 6 bat dung cho: `getpgid` con nem EPERM khi muc tieu
    # SONG nhung o SESSION KHAC — dung ca ma killpg(pid) ban vao nhom nguoi vo can.
    # Test dang BAO VE lo thay vi cam no. Nay khoa CA HAI ve: khong killpg, ma cung
    # khong duoc mua an toan bang cach thoi giet.
    ghi.clear()
    da_giet_rieng = []
    m._giet_rieng = lambda anh, sig: da_giet_rieng.append(sorted(anh))
    m._chup_cay = lambda p: {p: "x", p + 1: "y"}
    def _hong(_p):
        raise OSError("khong do duoc")
    m.os.getpgid = _hong
    kq = m._giet_cay(500, "x")
    bang(ghi == [], f"pgid KHONG do duoc ma VAN goi killpg: {ghi}")
    bang(da_giet_rieng and da_giet_rieng[0] == [500, 501],
         f"bo killpg roi KHONG giet rieng ai — mua an toan bang cach thoi giet: "
         f"{da_giet_rieng} / {kq}")

    # (d) KHONG do duoc pgid VA anh chup rong => noi that la khong giet duoc
    ghi.clear()
    da_giet_rieng.clear()
    m._chup_cay = lambda p: {}
    kq = m._giet_cay(500, "x")
    bang(ghi == [], f"anh chup rong ma van killpg: {ghi}")
    bang(getattr(kq, "tu_choi", False) is True,
         f"khong con duong giet nao ma khong noi that: {kq}")


@ca
def t93_do_codex_khong_duoc_nang_nhan_vuot_qua_bang_chung():
    """`codex login status` rc=0 KHÔNG chứng minh credential còn dùng được.

    ĐÃ ĐO 15-08-2026: lệnh đó trả "Logged in using ChatGPT" rc=0 trong khi MỌI lời gọi
    thật trả 401 `refresh_token_invalidated`. Nó chỉ kiểm tệp đọc được. Bản trước gọi
    thẳng trạng thái ấy là `DUNG_DUOC` — NÂNG NHÃN VƯỢT QUÁ BẰNG CHỨNG, và đó là lần
    THỨ HAI cùng một lớp lỗi trong đúng hàm này trong đúng một ngày.

    Ba nhãn, ba mức bằng chứng khác nhau, ca này khoá cả ba:
      CO_CREDENTIAL  có tệp, đọc được, chưa hết hạn — CHƯA chứng minh dùng được
      CHUA_XAC_THUC  đo được là hỏng (hết hạn, hoặc gọi thật bị từ chối)
      DUNG_DUOC      CHỈ khi đã gọi thật và thành công
    """
    m = _tai_launcher_thu()
    m._dang_cho_snapshot = lambda home: False  # Recovery is measured by g2 dedicated cases.
    m._codex_home_hieu_luc = lambda: Path("INERT-HOME")
    m.shutil.which = lambda t: "/usr/bin/codex" if t == "codex" else None

    class P:
        returncode = 0
        stdout = "Logged in using ChatGPT\n"
        stderr = ""
    m.subprocess.run = lambda *_a, **_k: P()

    # (a) token con han, KHONG kiem song => CO_CREDENTIAL, TUYET DOI khong DUNG_DUOC
    m._han_token_codex = lambda: {"doc_duoc": True, "last_refresh": "x",
                                  "gio_con_lai": {"access_token": 100.0}}
    tt, mo_ta = m._do_codex(kiem_song=False)
    bang(tt == "CO_CREDENTIAL", f"chua goi that ma da phong len {tt}")
    bang("CHUA chung minh" in mo_ta, f"mo ta phai noi ro chua chung minh: {mo_ta!r}")

    # (b) token HET HAN => ket luan duoc ngay, KHONG can goi mang.
    # Dung `access_token`, KHONG dung `id_token`: id_token ngan han theo thiet ke nen
    # da bi loai khoi moi phep xet han (xem `_TOKEN_KHONG_XET_HAN`). Fixture cu dung
    # id_token la ghim mot gia dinh SAI, sua theo hop dong moi.
    m._han_token_codex = lambda: {"doc_duoc": True, "last_refresh": "x",
                                  "gio_con_lai": {"access_token": -39.1}}
    tt, mo_ta = m._do_codex(kiem_song=False)
    bang(tt == "CHUA_XAC_THUC", f"token het han ma bao {tt}")
    bang("HET HAN" in mo_ta and "access_token" in mo_ta,
         f"phai neu TEN token het han: {mo_ta!r}")

    # (c) kiem song THANH CONG => moi duoc DUNG_DUOC
    m._han_token_codex = lambda: {"doc_duoc": True, "last_refresh": "x",
                                  "gio_con_lai": {"access_token": 100.0}}
    m._do_codex_song = lambda *_a, **_k: (True, "rc=0")
    tt, _ = m._do_codex(kiem_song=True)
    bang(tt == "DUNG_DUOC", f"kiem song dat ma khong cho DUNG_DUOC: {tt}")

    # (d) kiem song BI TU CHOI => CHUA_XAC_THUC, du login status van rc=0
    m._do_codex_song = lambda *_a, **_k: (False, "credential BI TU CHOI (token_revoked)")
    tt, mo_ta = m._do_codex(kiem_song=True)
    bang(tt == "CHUA_XAC_THUC", f"credential bi thu hoi ma van bao {tt}")
    bang("token_revoked" in mo_ta, f"phai giu nguyen ly do may chu tra: {mo_ta!r}")


@ca
def t94_canh_bao_TRUOC_khi_credential_het_han():
    """Phải báo TRƯỚC khi hỏng, không phải sau.

    Sự cố 15-08-2026: credential codex bị thu hồi giữa chừng, một lượt cross-review đã
    cấp lease mất trắng, và `doctor` chỉ phát hiện SAU khi mọi lời gọi đã 401.

    Ca gay nhất là ca THỨ BA dưới đây: `access_token` còn 199 giờ — mọi phép kiểm `exp`
    đều xanh — nhưng `last_refresh` đã quá 40 giờ và credential THẬT SỰ đã bị vô hiệu.
    Refresh token XOAY VÒNG: bản trên đĩa đổi thì bản trong `CODEX_AUTH_JSON` chết theo.
    Tuổi ảnh chụp là tín hiệu DUY NHẤT nhìn thấy trước, nên bỏ nó là bỏ đúng ca đã xảy ra.

    `SAP_HET_HAN` vẫn là DÙNG ĐƯỢC — nó KHÔNG được biến thành `CHUA_XAC_THUC`, kẻo chốt
    đỏ khi mọi thứ còn chạy và người ta học cách bỏ qua nó.
    """
    m = _tai_launcher_thu()
    m._dang_cho_snapshot = lambda home: False  # Recovery is measured by g2 dedicated cases.
    m._codex_home_hieu_luc = lambda: Path("INERT-HOME")
    m.shutil.which = lambda t: "/usr/bin/codex" if t == "codex" else None

    class P:
        returncode = 0
        stdout = "Logged in using ChatGPT\n"
        stderr = ""
    m.subprocess.run = lambda *_a, **_k: P()

    def dat(gio_con_lai, tuoi):
        m._han_token_codex = lambda: {"doc_duoc": True, "last_refresh": "x",
                                      "tuoi_anh_chup_gio": tuoi,
                                      "gio_con_lai": gio_con_lai}

    # (a) khoe manh => CO_CREDENTIAL, KHONG canh bao oan
    dat({"access_token": 100.0}, 1.0)
    tt, _ = m._do_codex()
    bang(tt == "CO_CREDENTIAL", f"credential khoe ma canh bao oan: {tt}")

    # (b) SAP het han theo `exp`
    dat({"access_token": 5.0}, 1.0)
    tt, mo_ta = m._do_codex()
    bang(tt == "SAP_HET_HAN", f"con 5h ma khong canh bao: {tt}")
    bang("access_token=5.0h" in mo_ta, f"phai neu TEN token va SO GIO: {mo_ta!r}")

    # (c) CA DA XAY RA: exp con xa NHUNG anh chup CU
    dat({"access_token": 199.0}, 40.0)
    tt, mo_ta = m._do_codex()
    bang(tt == "SAP_HET_HAN", f"anh chup cu 40h ma van bao {tt} — dung ca 15-08 tai dien")
    bang("anh chup CU" in mo_ta and "xoay vong" in mo_ta,
         f"phai giai thich VI SAO anh chup cu la nguy hiem: {mo_ta!r}")

    # (d) DA het han thi uu tien bao HET HAN, khong ha xuong canh bao.
    # `access_token` chu khong phai `id_token` — xem chu thich o (f) va (b) cua t93.
    dat({"access_token": -39.0}, 40.0)
    tt, mo_ta = m._do_codex()
    bang(tt == "CHUA_XAC_THUC", f"da het han ma chi canh bao: {tt}")
    bang("HET HAN" in mo_ta, f"phai noi ro DA het han: {mo_ta!r}")

    # (e) khong doc duoc tuoi => KHONG duoc canh bao oan (None khac 0)
    dat({"access_token": 100.0}, None)
    tt, _ = m._do_codex()
    bang(tt == "CO_CREDENTIAL", f"khong doc duoc tuoi ma canh bao oan: {tt}")

    # (f) `id_token` NGAN HAN THEO THIET KE — khong duoc lay lam tin hieu.
    # Do duoc ngay sau `codex login --device-auth`: access_token=240h, id_token=1.0h.
    # Ban dau toi lay ca id_token nen credential VUA DUC XONG da bi gan SAP_HET_HAN —
    # chot do thuong truc, dung thu se bi bo qua, va toi tu dung no vao chinh ban va
    # canh bao som. Ca nay khoa lai.
    dat({"access_token": 240.0, "id_token": 1.0}, 0.1)
    tt, mo_ta = m._do_codex()
    bang(tt == "CO_CREDENTIAL",
         f"credential VUA DUC bi bao {tt} vi id_token ngan han: {mo_ta!r}")
    bang("id_token" not in mo_ta, f"id_token khong duoc xuat hien trong ban khai: {mo_ta!r}")


@ca
def t95_tuoi_anh_chup_doc_dung_va_khong_chet():
    """`_tuoi_anh_chup_gio` phải đọc được ISO có `Z`, và trả None khi không đọc được."""
    m = _tai_launcher_thu()
    bang(m._tuoi_anh_chup_gio(None) is None, "None phai ra None")
    bang(m._tuoi_anh_chup_gio("") is None, "chuoi rong phai ra None")
    bang(m._tuoi_anh_chup_gio("khong-phai-ngay") is None, "rac phai ra None, KHONG duoc nem")
    gio = m._tuoi_anh_chup_gio("2026-08-14T04:13:33.127497Z")
    bang(isinstance(gio, float) and gio > 0, f"ISO co Z phai doc duoc, duoc {gio!r}")


@ca
def t96_kiem_song_phai_chay_KE_CA_khi_sap_het_han():
    """`--kiem-song` bị chính cảnh báo nuốt mất thì phép đo thành vô nghĩa.

    Bản trước trả về ngay tại nhánh `SAP_HET_HAN`, nên ai đòi kiểm sống sẽ KHÔNG BAO
    GIỜ được kiểm — đo được khi chạy `doctor --kiem-song` trên một credential sắp hết
    hạn: nó in cảnh báo rồi thoát, không hề gọi thật.

    "Sắp hết hạn" và "còn dùng được không" là HAI câu hỏi khác nhau; trả lời câu này
    KHÔNG được phép nuốt câu kia.
    """
    m = _tai_launcher_thu()
    m._dang_cho_snapshot = lambda home: False  # Recovery is measured by g2 dedicated cases.
    m._codex_home_hieu_luc = lambda: Path("INERT-HOME")
    m.shutil.which = lambda t: "/usr/bin/codex" if t == "codex" else None

    class P:
        returncode = 0
        stdout = "Logged in using ChatGPT\n"
        stderr = ""
    m.subprocess.run = lambda *_a, **_k: P()
    m._han_token_codex = lambda: {"doc_duoc": True, "last_refresh": "x",
                                  "tuoi_anh_chup_gio": 40.0,
                                  "gio_con_lai": {"access_token": 199.0}}

    # (a) sap het han NHUNG kiem song DAT => van SAP_HET_HAN, co ghi la van dung duoc
    goi = []
    m._do_codex_song = lambda *_a, **_k: (goi.append(1), (True, "rc=0"))[1]
    tt, mo_ta = m._do_codex(kiem_song=True)
    bang(len(goi) == 1, "doi kiem song ma KHONG he goi — canh bao da nuot phep do")
    bang(tt == "SAP_HET_HAN", f"kiem song dat thi van phai canh bao, duoc {tt}")
    bang("VAN dung duoc" in mo_ta, f"phai ghi ro van dung duoc: {mo_ta!r}")

    # (b) sap het han VA kiem song HONG => CHUA_XAC_THUC, canh bao khong duoc che lap
    m._do_codex_song = lambda *_a, **_k: (False, "credential BI TU CHOI (token_revoked)")
    tt, mo_ta = m._do_codex(kiem_song=True)
    bang(tt == "CHUA_XAC_THUC", f"kiem song hong ma chi canh bao: {tt}")
    bang("token_revoked" in mo_ta, f"phai giu ly do may chu tra: {mo_ta!r}")


@ca
def t104_khong_duoc_dung_API_CHI_CO_TREN_MOT_NEN_ma_khong_hoi_truoc():
    """Bộ test phải CHẠY ĐƯỢC trên nền thiếu API POSIX, không chết ở dòng đầu.

    ĐÃ ĐO trên `windows-latest` (PR #128, ngay sau khi gắn nhãn `windows`): chốt cô lập
    gọi thẳng `getattr(os, "getpgid")` nên ném `AttributeError` NGAY Ở ĐẦU MỌI CA —
    **0/103**, không ca nào chạy. Bộ test chưa từng chạy trên Windows kể từ lúc có chốt
    ấy, và **không ai biết**, vì job Windows mặc định skip để tiết kiệm phút.

    Cùng ngày, bot review bắt `os.O_NOFOLLOW` không có trên Windows. Hai lần trong một
    ngày cùng một hình dạng — đụng API CHỈ CÓ TRÊN MỘT NỀN mà không hỏi trước — nên ca
    này khoá hình dạng đó chứ không khoá từng tên hàm.

    Ca chạy được trên MỌI nền: nó GỠ thuộc tính (nếu nền có) để dựng lại đúng cảnh nền
    thiếu, rồi trả lại nguyên trạng.
    """
    ten = "getpgid"
    co_san = hasattr(os, ten)
    goc = getattr(os, ten) if co_san else None
    if co_san:
        delattr(os, ten)
    try:
        # (a) vào/ra chốt cô lập trên nền THIẾU hàm: không được ném
        try:
            with _co_lap_toan_cuc():
                pass
        except AttributeError as e:
            bang(False, f"chot co lap chet tren nen thieu {ten}: {e}")

        # (b) ca test gán thêm hàm mà nền vốn KHÔNG có ⇒ ra khỏi chốt phải SẠCH.
        # Rò thứ này là rò kiểu tệ nhất: nền tự nhận có một API mà nó không có, và ca
        # sau đo trên một nền KHÔNG TỒN TẠI.
        with _co_lap_toan_cuc():
            setattr(os, ten, lambda *_a: 123)
        bang(not hasattr(os, ten),
             f"{ten} RO ra ngoai chot — nen tu nhan co mot API no khong co")

        # (c) bản khai vẫn phải RA, và khoá không đo được là None chứ không phải False
        mt = khai_moi_truong()
        bang(isinstance(mt, dict) and mt, "ban khai KHONG ra tren nen thieu ham")
        bang(mt["pgid"] is None, f"thieu {ten} thi pgid phai None, duoc {mt['pgid']!r}")
        bang(mt["la_truong_nhom"] is None,
             f"khong do duoc thi phai None chu khong phai False, duoc {mt['la_truong_nhom']!r}")
        bang(mt["he_dieu_hanh"] is not None, "phep do KHONG lien quan cung bi keo theo")

        # (d) dòng tóm tắt vẫn in được
        bang("pid=" in _mot_dong_moi_truong(mt), "dong tom tat vo tren nen thieu ham")
    finally:
        if co_san:
            setattr(os, ten, goc)
        elif hasattr(os, ten):
            delattr(os, ten)


@ca
def t105_doctor_auth_hong_thi_DO_du_binary_chay_duoc():
    """CÓ binary chạy được KHÁC xác thực được — doctor phải tách hai tầng ấy.

    `codex --version` in số phiên bản ngon lành trong khi `codex` chưa có
    credential nào; cả ngày 15-08-2026 mất đúng vì khoảng cách đó. Ca này khoá:
    một công cụ BẮT BUỘC có `xac_thuc` mà probe auth hỏng thì `doctor` phải ĐỎ
    (rc=12) và JSON phải nói rõ `co: true` + `xac_thuc_ok: false` — hai trường
    riêng, vì gộp lại thì người đọc không phân biệt được "chưa cài" với "cài rồi
    mà chưa đăng nhập", và hai thứ đó chữa bằng hai lệnh khác nhau.

    Dùng seam nội bộ: thứ cần đo là THỨ TỰ và QUYẾT ĐỊNH trong cùng tiến trình,
    không phải hành vi của một CLI thật.
    """
    m = _tai_launcher_thu()
    su_kien = []
    m.CONG_CU = [{
        "ten": "gia", "bat_buoc": True, "ung_vien": ["gia"],
        "vi_sao": "thu", "cai": {"*": "cai gia"},
        "xac_thuc": ["auth", "status"],
    }]
    m.MO_DUN_PY = []
    # VÔ HIỆU bảng khả dụng: nó gọi `_do_github`, mà hàm ấy SINH `gh` THẬT bằng
    # đúng cái env tí hon ta vừa cắm vào. ĐO ĐƯỢC trên windows-latest: `gh` không
    # thấy `HOME`/`USERPROFILE` nên tự tạo `./.local/` NGAY TRONG KHO, và bước
    # "cây phải sạch sau khi chạy test" đỏ. Ca test không được để lại dấu vết.
    m.KHA_NANG = []
    m._doc_moi_truong = lambda: (
        su_kien.append("moi_truong") or
        ({"PATH": "P", "TL_LAUNCHER_ENV_DA_DOC": "1"}, {"da_doc_truoc_cong_cu": True})
    )
    m._cac_duong_dan = lambda _c, _env: (
        su_kien.append("resolve") or [("gia", "/gia/bin")]
    )
    m._phien_ban = lambda *_a, **_k: (su_kien.append("version") or (True, "gia 1", False))
    m._xac_thuc_kem_dau_ra = lambda *_a, **_k: (su_kien.append("auth") or (False, "rc=1", False, ""))
    a = type("A", (), {"json": True, "workspace": None, "doi_kha_dung": False})()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = m.lenh_doctor(a)
    d = json.loads(out.getvalue())
    # ĐỌC ENV TRƯỚC khi hỏi công cụ — không phải nếp code, mà là điều kiện để câu
    # "công cụ không dùng được" có nghĩa.
    bang(su_kien[0] == "moi_truong", f"thu tu sai: {su_kien}")
    bang(rc == MA_THIEU_CONG_CU and d["thieu_bat_buoc"] == ["gia"],
         f"auth hong ma doctor van xanh: rc={rc}, thieu={d['thieu_bat_buoc']}")
    muc = [x for x in d["cong_cu"] if x["ten"] == "gia"][0]
    bang(muc["co"] is True and muc.get("xac_thuc_ok") is False,
         f"khong tach binary voi auth: {muc}")


@ca
def t106_doctor_binary_hong_dau_PATH_khong_duoc_che_binary_tot():
    """WindowsApps có rg.exe nhưng Access denied; phải thử ứng viên KẾ TIẾP.

    `shutil.which` chỉ trả mục ĐẦU TIÊN, nên một binary hỏng đứng trước che mất
    bản chạy được đứng sau — đo được trên Windows 15-08-2026. Ca này đòi doctor
    duyệt hết, và đòi ĐÚNG THỨ TỰ (không phải "tìm thấy bản tốt ở đâu cũng được"):
    thứ tự PATH là thứ tự người dùng khai, đảo nó là đổi ý nghĩa của PATH.
    """
    m = _tai_launcher_thu()
    da_thu = []
    m.CONG_CU = [{
        "ten": "rg", "bat_buoc": True, "ung_vien": ["rg"],
        "vi_sao": "thu", "cai": {"*": "cai rg"},
    }]
    m.MO_DUN_PY = []
    m.KHA_NANG = []                 # xem chú thích ở t105: tránh sinh `gh` thật
    m._doc_moi_truong = lambda: (
        {"PATH": "P", "TL_LAUNCHER_ENV_DA_DOC": "1"}, {"da_doc_truoc_cong_cu": True})
    m._cac_duong_dan = lambda _c, _env: [("rg", "/hong/rg"), ("rg", "/tot/rg")]
    m._ten_tran_giai_ra = lambda _t, _e: "/hong/rg"

    def pb(duong, **_kwargs):
        da_thu.append(duong)
        return (duong == "/tot/rg", "rg 99" if duong == "/tot/rg" else "Access denied",
                False)

    m._phien_ban = pb
    a = type("A", (), {"json": True, "workspace": None, "doi_kha_dung": False})()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = m.lenh_doctor(a)
    d = json.loads(out.getvalue())
    muc = [x for x in d["cong_cu"] if x["ten"] == "rg"][0]
    # wp802 (spec Q2): `rg` nằm trong tập BI_CHE nên bản đầu hỏng ⇒ thoát 12, nhưng
    # vẫn phải LÙI sang bản tốt (duong_dan) và thử ĐÚNG thứ tự — ý ban đầu của ca giữ nguyên.
    bang(rc == MA_THIEU_CONG_CU and muc.get("duong_dan") == "/tot/rg"
         and muc.get("trang_thai") == "BI_CHE",
         f"khong lui sang binary tot: rc={rc}, {muc}")
    bang(da_thu == ["/hong/rg", "/tot/rg"], f"khong thu dung thu tu: {da_thu}")


@ca
def t107_doc_moi_truong_KHONG_duoc_chon_bien_giu_cho():
    """Token GitHub trùng byte với khoá AWS thì đó là CHUỖI GIỮ CHỖ, không phải credential.

    ĐO 17-08-2026 trong container remote: `GH_TOKEN` `GITHUB_TOKEN` `AWS_*`
    `CLOUDSDK_*` mang CÙNG một chuỗi giữ chỗ 14 ký tự, credential thật ở
    `GITHUB_PAT` (93 ký tự). Lấy theo thứ tự tài liệu của gh (GH_TOKEN trước) là
    chọn đúng bản giữ chỗ, rồi báo `nguon_xac_thuc_github: GH_TOKEN` — dòng ấy
    đọc như "đã có credential" trong khi công cụ sẽ nhận "sai thông tin đăng
    nhập". Biến giữ chỗ TỆ HƠN biến chưa đặt, đúng như CLAUDE.md ghi.

    Ba vế: (a) loại đúng bản giữ chỗ và chọn bản thật; (b) môi trường CON phải
    mang giá trị THẬT; (c) khi CHỈ có giữ chỗ thì phải là `none` và phải GỠ biến
    ra khỏi môi trường con — "chưa đăng nhập" đọc đúng, "sai thông tin đăng nhập"
    đẩy người đọc đi sai hướng.
    """
    m = _tai_launcher_thu()
    GIU_CHO, THAT = "x" * 14, "p" * 93

    def dat(**bien):
        m.os.environ = dict(bien)

    # (a)+(b) co ca giu cho lan ban that
    dat(GH_TOKEN=GIU_CHO, GITHUB_TOKEN=GIU_CHO, AWS_ACCESS_KEY_ID=GIU_CHO,
        GITHUB_PAT=THAT, PATH="/bin")
    con, ck = m._doc_moi_truong()
    bang(ck["nguon_xac_thuc_github"] == "GITHUB_PAT->GH_TOKEN",
         f"chon nham nguon: {ck['nguon_xac_thuc_github']}")
    bang(ck["bien_giu_cho"] == ["GH_TOKEN", "GITHUB_TOKEN"],
         f"khong nhan ra bien giu cho: {ck['bien_giu_cho']}")
    bang(con["GH_TOKEN"] == THAT, "moi truong con khong mang credential that")
    # Khong duoc ro ri gia tri ra ban cong khai, du la ban giu cho.
    bang(GIU_CHO not in json.dumps(ck) and THAT not in json.dumps(ck),
         "ban cong khai co chua gia tri bien")

    # (c) CHI co giu cho
    dat(GH_TOKEN=GIU_CHO, GITHUB_TOKEN=GIU_CHO, AWS_ACCESS_KEY_ID=GIU_CHO, PATH="/bin")
    con2, ck2 = m._doc_moi_truong()
    bang(ck2["nguon_xac_thuc_github"] == "none",
         f"giu cho bi doc thanh credential: {ck2['nguon_xac_thuc_github']}")
    bang("GH_TOKEN" not in con2 and "GITHUB_TOKEN" not in con2,
         "van truyen bien giu cho xuong tien trinh con")

    # Chieu NGUOC: khong co bien la khong lien quan thi KHONG duoc goi la giu cho.
    dat(GH_TOKEN=THAT, PATH="/bin")
    _con3, ck3 = m._doc_moi_truong()
    bang(ck3["nguon_xac_thuc_github"] == "GH_TOKEN" and ck3["bien_giu_cho"] == [],
         f"bao giu cho oan: {ck3}")


@ca
def t108_hook_phai_probe_CHAY_DUOC_khong_chi_CO_MAT():
    """`co_chay` của hook phải giết được binary CÓ MẶT mà KHÔNG chạy được.

    Hook từng rẽ nhánh trên `command -v`, tức chỉ chứng minh có đường dẫn. Một
    tệp rỗng, một script `exit 1`, hay `rg.exe` của WindowsApps trả Access denied
    đều lọt — và hook sẽ BỎ QUA phần cài đặt vì tưởng đã có. Sai ở đây im lặng:
    phiên chạy tiếp với công cụ hỏng.

    Thân hàm được TRÍCH TỪ CHÍNH tệp hook rồi `eval`, không chép lại — hai bản
    của một hàm sẽ trôi lệch, và bên quên cập nhật chính là bên đẩy lọt. Ba vế
    cố ý gồm cả vế XANH (`--version` thật) để ca này không thể đỏ-vì-mọi-thứ.
    """
    duong_hook = LAUNCHER.parent.parent / "hooks" / "session-start.sh"
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(duong_hook)
    if ly_do:
        return ly_do
    hook = duong_hook.read_text(encoding="utf-8")
    bang("co_chay()" in hook, "hook khong con ham co_chay")
    if LA_WINDOWS:
        # ĐO ĐƯỢC trên windows-latest: ba fixture là script `#!/bin/sh` KHÔNG phần mở
        # rộng, nên `command -v totqua` trong Git Bash thấy nhưng CreateProcess của
        # Windows không chạy được ⇒ `co_chay` trả "không chạy được" cho binary mà ca
        # này khẳng định là chạy được, và ca đỏ vì FIXTURE chứ không vì mã. Phần khai
        # báo (hook còn `co_chay`, ba chỗ đã đổi) VẪN đo ở trên — chỉ phần chạy thật
        # là POSIX. Muốn đo trên Windows thì phải dựng shim `.cmd`, cùng nợ với `t03`.
        return "bo qua tren Windows (can shim .cmd cho fixture)"
    for ten in ("codex", "claude", "rg"):
        bang(f"co_chay {ten}" in hook, f"hook van dung `co` thay vi `co_chay` cho {ten}")

    dau = hook.index("co_chay() {")
    than = hook[dau:hook.index("\n}\n", dau) + 3]

    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        hong = t / "hongqua"
        hong.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        cam = t / "camlang"                       # rc=0 nhung KHONG in gi
        cam.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        tot = t / "totqua"
        tot.write_text("#!/bin/sh\necho 'totqua 1.0'\n", encoding="utf-8")
        for f in (hong, cam, tot):
            f.chmod(0o755)

        def thu(ten: str) -> int:
            kich = f'PY={sys.executable}\n{than}\nco_chay {ten}\n'
            r = subprocess.run(["bash", "-c", kich], capture_output=True, text=True,
                               env={**os.environ, "PATH": f"{td}{os.pathsep}{os.environ['PATH']}"},
                               timeout=120)
            return r.returncode

        bang(thu("totqua") == 0, "co_chay tu choi binary CHAY DUOC")
        bang(thu("hongqua") != 0, "co_chay nhan binary rc!=0 la chay duoc")
        # rc=0 + im lang = chu ky cua "chay nhung chang lam gi" (bay $Args, r244).
        bang(thu("camlang") != 0, "co_chay nhan rc=0-nhung-rong la chay duoc")
        bang(thu("khong_ton_tai_gi_ca") != 0, "co_chay nhan binary KHONG CO")


@ca
def t109_bat_buoc_giai_THEO_NEN_khong_phai_mot_bool_chung():
    """`gh` bắt buộc ở máy người dùng, KHÔNG bắt buộc ở phiên remote.

    Đo 17-08-2026: trong container remote, `gh auth status` hỏi `/user` (đường
    proxy CHO PHÉP, 200) nên nó tự nhận đã xác thực, rồi mọi lệnh việc thật đi
    `/repos/...` và ăn 403 do proxy tự sinh. Ép `bat_buoc` là MỘT bool thì chắc
    chắn sai một trong hai nền, và cái sai đó CHẶN phiên chứ không chỉ báo nhầm.

    Ba vế: hai chiều của bảng theo nền, cộng một vế chống hồi quy cho mục khai
    bằng bool thường — nới cơ chế mà làm hỏng dạng cũ thì cũng là hỏng.
    """
    m = _tai_launcher_thu()
    c_bang = {"ten": "gh", "bat_buoc": {"mac_dinh": True, "remote": False},
              "ung_vien": ["gh"], "vi_sao": "thu", "cai": {"*": "cai gh"}}
    c_bool = {"ten": "git", "bat_buoc": True, "ung_vien": ["git"],
              "vi_sao": "thu", "cai": {"*": "cai git"}}
    bang(m._bat_buoc(c_bang, {"CLAUDE_CODE_REMOTE": "true"}) is False,
         "remote van doi gh")
    bang(m._bat_buoc(c_bang, {}) is True, "may nguoi dung lai tha gh")
    # Chỉ ĐÚNG chuỗi "true" mới là remote — `"false"`/`"1"` không được nhận nhầm.
    bang(m._bat_buoc(c_bang, {"CLAUDE_CODE_REMOTE": "false"}) is True,
         "doc bien remote qua rong")
    bang(m._bat_buoc(c_bool, {"CLAUDE_CODE_REMOTE": "true"}) is True
         and m._bat_buoc(c_bool, {}) is True, "dang bool thuong bi hong")

    # NỀN CI — đã trả giá: đặt `claude`/`codex` bắt buộc làm `doctor` trả 12 trên
    # runner (nó chỉ cài `rg`), và `launcher-windows.yml` SKIP sạch mọi bước sau:
    # 110 ca, 66 đột biến, bốn probe Windows đều không chạy. Fail-close đặt sai chỗ
    # không chỉ báo nhầm — nó TẮT phép đo. Runner đo chính launcher, không chạy phiên
    # agent, nên không được đòi chuỗi công cụ agent ở đó.
    c_ci = {"ten": "claude", "bat_buoc": {"mac_dinh": True, "remote": True, "ci": False},
            "ung_vien": ["claude"], "vi_sao": "thu", "cai": {"*": "cai"}}
    bang(m._bat_buoc(c_ci, {"GITHUB_ACTIONS": "true"}) is False, "CI van doi claude")
    bang(m._bat_buoc(c_ci, {"CI": "true"}) is False, "khoa CI chi nhan GITHUB_ACTIONS")
    # CI phải THẮNG `remote` khi mang cả hai dấu: việc của runner hẹp hơn.
    bang(m._bat_buoc(c_ci, {"GITHUB_ACTIONS": "true",
                            "CLAUDE_CODE_REMOTE": "true"}) is False,
         "mang ca hai dau ma khong uu tien CI")
    bang(m._bat_buoc(c_ci, {}) is True, "may nguoi dung lai tha claude")
    # Thiếu khoá `ci` thì LÙI VỀ `mac_dinh`, không được im lặng thành False.
    c_thieu = {"ten": "x", "bat_buoc": {"mac_dinh": True, "remote": False},
               "ung_vien": ["x"], "vi_sao": "thu", "cai": {"*": "cai"}}
    bang(m._bat_buoc(c_thieu, {"GITHUB_ACTIONS": "true"}) is True,
         "thieu khoa ci lai am tham thanh False")


@ca
def t110_rest_github_phan_loai_theo_HEADER_khong_theo_MA_TRANG_THAI():
    """403 của proxy và 403 của GitHub là HAI chuyện; phân biệt bằng header.

    Đo 17-08-2026: `/repos/<kho>` trả 403 KHÔNG kèm header `X-GitHub-*` (proxy tự
    sinh, chưa từng tới GitHub), còn `/rate_limit` trả 200 CÓ header. Token không
    đổi gì — chính sách theo ĐƯỜNG DẪN. Đọc bằng mã trạng thái đơn thuần sẽ dịch
    403 kia thành "GitHub từ chối ta", rồi người đọc đi truy quyền token: sai
    hướng hoàn toàn. Cùng doctrine với "phân loại HTTP bằng văn bản tự do là ĐOÁN".

    Vế thứ ba là trạng thái `khong_do_duoc` — nó KHÔNG được gộp vào `chan`
    (`None ≠ False`), vì "mạng hỏng" và "proxy chặn" chữa bằng hai cách khác nhau.
    """
    m = _tai_launcher_thu()

    class _Ph:
        def __init__(self, status, headers):
            self.status, self.headers = status, headers
        def __enter__(self): return self
        def __exit__(self, *_a): return False

    def dat(ket):
        m.urllib.request.urlopen = lambda *_a, **_k: ket()

    dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
    bang(m._do_rest_github("https://x/y")[0] == "mo", "200 co header GitHub phai la `mo`")

    # 200 mà KHÔNG có header GitHub = proxy trả lời thay; không phải đường tới nơi.
    dat(lambda: _Ph(200, {"Content-Type": "application/json"}))
    bang(m._do_rest_github("https://x/y")[0] == "chan", "200 khong header GitHub phai la `chan`")

    def _ném(code, headers):
        def f():
            raise m.urllib.error.HTTPError("https://x/y", code, "loi", headers, None)
        return f

    dat(_ném(403, {"Content-Type": "text/plain"}))
    tt, mo_ta, _ = m._do_rest_github("https://x/y")
    bang(tt == "chan" and "proxy" in mo_ta, f"403 khong header phai la `chan`: {tt} {mo_ta}")
    # 4xx CÓ header GitHub = tới nơi, chỉ thiếu quyền. Gọi nó là `chan` thì ta đẩy
    # người đọc đi sửa proxy trong khi thứ hỏng là quyền token.
    dat(_ném(404, {"X-GitHub-Request-Id": "abc"}))
    bang(m._do_rest_github("https://x/y")[0] == "mo", "4xx CO header GitHub phai la `mo`")

    def _no():
        raise OSError("mang hong")
    dat(_no)
    bang(m._do_rest_github("https://x/y")[0] == "khong_do_duoc",
         "mang hong bi gop vao `chan` (None != False)")

    # GIA TRI THU BA: "duong co thong" KHAC "lam duoc viec". Mot 404 kho rieng tu
    # toi duoc GitHub (`mo`) ma KHONG doc noi kho. Gop hai cau ay chinh la P1 mà
    # cross-review bat tren PR "#143".
    dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
    bang(m._do_rest_github("https://x/y")[2] is True, "2xx co header ma khong tinh la thanh cong")
    dat(_ném(404, {"X-GitHub-Request-Id": "abc"}))
    tt, _mt, ok = m._do_rest_github("https://x/y")
    bang(tt == "mo" and ok is False,
         f"404 co header GitHub phai la `mo` NHUNG khong thanh cong: {tt} {ok}")
    dat(_no)
    bang(m._do_rest_github("https://x/y")[2] is False, "khong do duoc ma tinh la thanh cong")


@ca
def t111_gh_da_xac_thuc_KHONG_phai_bang_chung_lam_duoc_viec():
    """`gh auth status` xanh mà mọi thao tác kho 403 thì GitHub KHÔNG dùng được.

    P1 cross-review PR "#143", và là lần THỨ BA cùng một hình dạng trong kho:
    trước là `shutil.which("gh")` được đếm là đường mở (`t103` sinh ra vì nó), rồi
    `rest-chung` (`/rate_limit` mở nhưng không đọc nổi PR nào), giờ tới
    `gh auth status`. Ba lần thì sai nằm ở ĐỊNH NGHĨA "đường làm được việc", không
    ở từng bản vá — nên nó phải neo vào một THAO TÁC KHO đã thành công.

    Đo được ngay trong phiên viết ca này: `gh auth status` hỏi `/user`, là đường
    proxy CHO PHÉP, nên nó xanh trong khi `/repos/...` trả 403 do proxy tự sinh.
    """
    m = _tai_launcher_thu()

    # `remote get-url` PHAI thanh cong (de co slug), con `ls-remote` PHAI hong —
    # ta dang dung canh "git khong dung duoc", de xem gh mot minh co du hay khong.
    def gia_git(ws, *a):
        if a[:1] == ("remote",):
            return (0, "https://github.com/o/r.git", "")
        return (128, "", "fatal: unable to access")

    m._git = gia_git
    m.shutil.which = lambda t: "/gia/gh" if t == "gh" else None

    class P:
        def __init__(self, rc, out=""):
            self.returncode, self.stdout, self.stderr = rc, out, ""

    # gh CO va DA XAC THUC, nhung thao tac muc kho HONG; REST kho cung hong.
    def chay(cmd, **_k):
        if cmd[:3] == ["gh", "auth", "status"]:
            return P(0, "Logged in")
        if cmd[:2] == ["gh", "api"]:
            return P(1)                      # 403 o duong viec that
        return P(1)

    m.subprocess.run = chay
    m._do_rest_github = lambda url, **_k: (
        ("mo", "HTTP 200", True) if "rate_limit" in url else ("chan", "HTTP 403", False))
    nhan, mo_ta = m._do_github("/gia/ws")     # co ws de lay slug, nhung git se hong
    bang(nhan == "CHUA_XAC_THUC",
         f"gh xac thuc + rate_limit mo ma da goi la DUNG_DUOC: {nhan} | {mo_ta}")

    # Chieu NGUOC: thao tac muc kho THANH CONG thi phai la DUNG_DUOC.
    def chay2(cmd, **_k):
        if cmd[:2] == ["gh", "api"]:
            return P(0, "o/r\n")
        return P(0, "Logged in")
    m.subprocess.run = chay2
    nhan2, mo_ta2 = m._do_github("/gia/ws")
    bang(nhan2 == "DUNG_DUOC", f"thao tac kho thanh cong ma van CHUA_XAC_THUC: {nhan2} | {mo_ta2}")


@ca
def t112_tran_tong_suy_tu_SO_PROBE_va_het_ngan_sach_KHONG_phai_hong():
    """Trần tổng phải lớn theo bảng, và hết ngân sách không được gọi là hỏng.

    P2 cross-review PR "#143". Con số 120s tôi chọn tay không đủ: bảng có thể chạy
    9+ probe `--version` cộng probe auth, mỗi cái được phép tới 25s trên Windows.
    Một chuỗi khởi động nguội HỢP LỆ vét sạch trần TRƯỚC khi đo tới cuối bảng, rồi
    các công cụ cuối bị báo thiếu dù KHÔNG cái nào vượt hạn riêng — trần tổng biến
    "hết ngân sách" thành "công cụ hỏng", đúng cái nhãn sai đợt này đi sửa.

    Hai vế: (a) trần suy TỪ SỐ PHÉP ĐO nên thêm công cụ là trần tự giãn; (b) khi
    hết ngân sách thật thì mục ấy phải vào `chua_do_duoc`, KHÔNG vào
    `co_mat_nhung_khong_chay_duoc` — `None ≠ False`, "chưa đo" khác "đo được là hỏng".
    """
    m = _tai_launcher_thu()
    goc = m._tran_doctor()
    m.CONG_CU = list(m.CONG_CU) + [
        {"ten": "them1", "bat_buoc": False, "ung_vien": ["them1"],
         "vi_sao": "thu", "cai": {"*": "x"}},
        {"ten": "them2", "bat_buoc": False, "ung_vien": ["them2"],
         "vi_sao": "thu", "cai": {"*": "x"}, "xac_thuc": ["a"]},
    ]
    sau = m._tran_doctor()
    # +2 muc, trong do 1 co xac_thuc => +3 phep do
    bang(sau == goc + 3 * m.PROBE_TIMEOUT_GIAY,
         f"tran khong gian theo bang: {goc} -> {sau}")

    # (b) het ngan sach => `chua_do_duoc`, khong phai `co_mat_nhung_khong_chay_duoc`
    m2 = _tai_launcher_thu()
    m2.CONG_CU = [{"ten": "cham", "bat_buoc": False, "ung_vien": ["cham"],
                   "vi_sao": "thu", "cai": {"*": "cai cham"}}]
    m2.MO_DUN_PY = []
    m2.KHA_NANG = []                # xem chú thích ở t105: tránh sinh `gh` thật
    m2._doc_moi_truong = lambda: ({"PATH": "P"}, {"da_doc_truoc_cong_cu": True})
    m2._cac_duong_dan = lambda _c, _e: [("cham", "/gia/cham")]
    m2._tran_doctor = lambda: -1.0          # ngan sach am = het ngay tu dau
    a_ = type("A", (), {"json": True, "workspace": None, "doi_kha_dung": False})()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        m2.lenh_doctor(a_)
    d = json.loads(out.getvalue())
    muc = [c for c in d["cong_cu"] if c["ten"] == "cham"][0]
    bang("chua_do_duoc" in muc,
         f"het ngan sach ma khong khai la chua do duoc: {muc}")
    bang("co_mat_nhung_khong_chay_duoc" not in muc,
         f"het ngan sach bi dan nhan CONG CU HONG: {muc}")


@ca
def t113_probe_github_phai_nhan_credential_DA_CHUAN_HOA():
    """Sửa xong biến giữ chỗ mà không nối vào chỗ DÙNG thì bản sửa vô nghĩa.

    P2 cross-review PR "#143". `_doc_moi_truong` loại `GH_TOKEN` giữ chỗ và ánh xạ
    `GITHUB_PAT` thật sang `GH_TOKEN`, nhưng bản đã chuẩn hoá ấy chỉ nằm trong giá
    trị trả về. `_do_github` không nhận nó nên probe vẫn đi bằng chuỗi giữ chỗ lấy
    từ `os.environ` — với kho RIÊNG TƯ và git hỏng, cả `gh api` lẫn REST đều trượt
    dù PAT thật đọc được.
    """
    m = _tai_launcher_thu()
    thay = {}

    def gia_git(ws, *a):
        return (0, "https://github.com/o/r.git", "") if a[:1] == ("remote",) else (128, "", "")

    m._git = gia_git
    m.shutil.which = lambda t: "/gia/gh" if t == "gh" else None
    m.os.environ = {"GH_TOKEN": "GIU_CHO"}          # bản CŨ, chưa chuẩn hoá

    class P:
        returncode, stdout, stderr = 0, "o/r", ""

    def chay(cmd, **k):
        thay.setdefault("env", []).append((k.get("env") or {}).get("GH_TOKEN"))
        return P()

    m.subprocess.run = chay
    m._do_rest_github = lambda url, **k: (
        thay.setdefault("tok", []).append(k.get("token")) or ("mo", "HTTP 200", True))

    m._do_github("/gia/ws", {"GH_TOKEN": "THAT"})   # bản ĐÃ chuẩn hoá
    bang(thay.get("tok") and all(t == "THAT" for t in thay["tok"]),
         f"REST probe khong nhan credential da chuan hoa: {thay.get('tok')}")
    bang(thay.get("env") and all(v == "THAT" for v in thay["env"]),
         f"probe `gh` van chay bang bien giu cho: {thay.get('env')}")


@ca
def t114_ngan_sach_phu_CA_khoi_kha_dung_va_khong_thanh_THIEU():
    """Trần phải phủ CẢ khối khả dụng, và hết ngân sách KHÔNG thành "thiếu công cụ".

    Hai P2 cross-review PR "#143", và cả hai là nửa việc tôi làm dở ở lượt trước:
      · khối `KHA_NANG` chạy NGOÀI mọi trần — mà nó gọi `gh`/`codex`/`claude`, đúng
        loại lệnh chậm nhất. Một trần chỉ phủ nửa lượt chạy thì không phải trần.
      · hết ngân sách vẫn rơi vào `thieu_bat_buoc`, nên `doctor` vẫn trả 12 và vẫn
        nói "THIEU". Lượt trước tôi tách được cái NHÃN mà chưa tách cái QUYẾT ĐỊNH;
        đổi tên chỗ hỏng mà giữ nguyên kết luận thì chưa sửa gì.
    """
    m = _tai_launcher_thu()
    m.CONG_CU = [{"ten": "cham", "bat_buoc": True, "ung_vien": ["cham"],
                  "vi_sao": "thu", "cai": {"*": "cai cham"}}]
    m.MO_DUN_PY = []
    da_goi = []
    m.KHA_NANG = [{"ten": "gia", "vi_sao": "thu",
                   "do": lambda ws, ks=False: (da_goi.append(1), ("DUNG_DUOC", "x"))[1]}]
    m._doc_moi_truong = lambda: ({"PATH": "P"}, {"da_doc_truoc_cong_cu": True})
    m._cac_duong_dan = lambda _c, _e: [("cham", "/gia/cham")]
    m._tran_doctor = lambda: -1.0            # ngân sách âm = hết ngay từ đầu
    a_ = type("A", (), {"json": True, "workspace": None, "doi_kha_dung": False})()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = m.lenh_doctor(a_)
    d = json.loads(out.getvalue())

    # (a) khối khả dụng phải TÔN TRỌNG trần — không được gọi khi đã hết ngân sách
    bang(not da_goi, "khoi kha dung van chay du da het ngan sach")
    kn = [k for k in d["kha_nang"] if k["ten"] == "gia"][0]
    bang(kn["trang_thai"] == "KHONG_DO_DUOC", f"het ngan sach ma khong khai: {kn}")

    # (b) chưa đo được KHÁC thiếu — hai danh sách riêng
    bang(d["thieu_bat_buoc"] == [],
         f"het ngan sach bi doc thanh THIEU cong cu: {d['thieu_bat_buoc']}")
    bang(d.get("chua_do_bat_buoc") == ["cham"],
         f"khong khai duoc muc chua do: {d.get('chua_do_bat_buoc')}")


@ca
def t103_nam_finding_cua_bot_review_PR128():
    """Năm mục bot codex nêu trên PR #128 — cả năm ĐO LẠI đều đúng, nên khoá cả năm.

    Mục nặng nhất là `PIPESTATUS`, và nó đáng ghi: chú thích của tôi ghi "`set -o pipefail`
    khong bat o day" trong khi CHÍNH TỆP ĐÓ đặt `set -euo pipefail` ở dòng 34. Dòng
    "phòng thủ" `MA_GO=${PIPESTATUS[0]:-$MA_GO}` là MỘT LỆNH, nên nó đặt lại PIPESTATUS
    về 0 và kéo `MA_GO` về 0 — `CODEX_BI_CHAN` không bao giờ được đặt. Lần thứ BA chốt
    fail-close chết, lần này vì một dòng tưởng là làm cho chắc.
    """
    m = _tai_launcher_thu()

    # (a) BIEN RONG khong phai credential
    m.shutil.which = lambda t: f"/usr/bin/{t}"
    m.os.path.expanduser = lambda d: "/khong-ton-tai-o-dau-ca" if d.startswith("~") else d
    m.os.environ = {"ANTHROPIC_API_KEY": ""}
    tt, mo_ta = m._do_claude()
    bang(tt != "DUNG_DUOC", f"bien RONG ma van bao DUNG_DUOC: {mo_ta!r}")
    m.os.environ = {"ANTHROPIC_API_KEY": "sk-that-su-co-gia-tri"}
    tt, _ = m._do_claude()
    bang(tt == "DUNG_DUOC", f"bien CO gia tri ma bao {tt} — chan oan")

    # (b) `gh` CO MAT khong phai DA XAC THUC
    #
    # `m.subprocess` LA module subprocess dung chung, nen gan de len no la de len CA
    # tien trinh test. Da dinh ngay trong chinh ca nay: phan (e) goi bash that va nhan
    # ve chuoi rong vi van dang dung ban gia cua phan (b). Giu ban goc, tra lai ngay.
    goc_run = m.subprocess.run
    goi = []

    class Rc:
        def __init__(self, rc):
            self.returncode, self.stdout, self.stderr = rc, "", ""

    # KY VONG DA DOI, co chu dinh — P1 cross-review tren PR "#143".
    #
    # Ban dau ca nay khang dinh `gh auth status` rc=0 => `DUNG_DUOC`. Do la mot buoc
    # TIEN BO so voi ban truoc no (chi dem `shutil.which("gh")`), nhung van con dung
    # mot nua: no van dem KET QUA MOT PROBE lam bang chung LAM DUOC VIEC. Do duoc
    # 17-08-2026: `gh auth status` hoi `/user` — duong proxy CHO PHEP, tra 200 — nen
    # no xanh trong khi moi thao tac muc kho tra 403 do proxy tu sinh.
    #
    # Nen ca hai dong duoi day deu mong `False`: khong co workspace thi khong goi
    # duoc ten kho, tuc KHONG CO cach nao chung minh lam duoc viec — va "chua chung
    # minh duoc" phai doc la chua, khong duoc doc thanh dat.
    for rc_gh in (1, 0):
        m.subprocess.run = lambda *_a, **_k: (goi.append(1), Rc(rc_gh))[1]
        tt, mo_ta = m._do_github(None)      # KHONG co workspace => khong co duong kho
        bang(tt != "DUNG_DUOC",
             f"gh rc={rc_gh} ma van goi la DUNG_DUOC khi chua lam noi viec gi: {mo_ta!r}")
    bang(goi, "khong he goi `gh auth status` — van dang do CO MAT")

    # Y DINH GOC cua ca nay VAN duoc giu: phai co phep do THAT, khong duoc suy tu
    # su co mat. Nay them chieu DUONG — thao tac muc kho thanh cong thi phai xanh —
    # de ca nay khong tro thanh "luon do", tuc mot ca khong the xanh cung vo dung
    # nhu mot ca khong the do.
    m._git = lambda ws, *a: (0, "https://github.com/o/r.git", "")
    m._do_rest_github = lambda url, **_k: ("chan", "HTTP 403", False)

    def chay_kho(cmd, **_k):
        goi.append(1)
        return Rc(0) if cmd[:2] == ["gh", "api"] else Rc(0)

    m.subprocess.run = chay_kho
    tt_kho, mo_ta_kho = m._do_github("/gia/ws")
    bang(tt_kho == "DUNG_DUOC",
         f"thao tac muc kho thanh cong ma van {tt_kho}: {mo_ta_kho!r}")
    m.subprocess.run = goc_run          # tra lai TRUOC khi phan (e) goi bash that

    # (c) SO MOC THAT, khong so tuoi da lam tron (0,1h = 6 phut)
    # Doi do CHINH XAC TOI GIAY. Ban dau toi viet ca nay bang cach doi hai moc cach
    # 3 phut phai CUNG o lam tron — no CHAP CHON, vi hai tuoi cach 0,05h roi vao cung
    # o hay khac o la tuy THOI DIEM CHAY. Mot ca do thoi diem chay thi khong phai ca.
    a = m._moc_refresh("2026-08-16T01:00:00Z")
    b = m._moc_refresh("2026-08-16T01:00:01Z")     # cach DUNG MOT GIAY
    bang(a is not None and b is not None, "khong doc duoc moc")
    bang(a < b, "hai moc cach 1 GIAY ma so ra bang nhau — dang lam tron truoc khi so")
    # ...va noi ro vi sao khong duoc dung `_tuoi_anh_chup_gio` de QUYET DINH:
    v = m._tuoi_anh_chup_gio("2026-08-16T01:00:00Z")
    bang(v is not None and round(v, 1) == v,
         f"tuoi phai la so DA LAM TRON 0,1h (=6 phut) — do la ly do khong duoc so bang no: {v}")
    bang(m._moc_refresh("rac") is None and m._moc_refresh(None) is None,
         "moc khong doc duoc phai la None")

    # (d) `O_NOFOLLOW` KHONG co tren Windows => phai dung getattr
    cs = _nap_sach(CODEX_ENV_POLICY)
    with San() as s:
        goc_getattr = cs.os.O_NOFOLLOW if hasattr(cs.os, "O_NOFOLLOW") else None
        try:
            if goc_getattr is not None:
                del cs.os.O_NOFOLLOW          # gia lap Windows
            cs.viet_ban_da_go(s / "ra.txt", b"noi dung")
            bang((s / "ra.txt").read_bytes() == b"noi dung", "ghi sai noi dung")
        except AttributeError as e:
            bang(False, f"goi thang os.O_NOFOLLOW — Windows se chet: {e}")
        finally:
            if goc_getattr is not None:
                cs.os.O_NOFOLLOW = goc_getattr

    # (e) HOOK: ma thoat cua bo phat hien phai TOI DUOC `CODEX_BI_CHAN`
    duong_hook = LAUNCHER.parent.parent / "hooks" / "session-start.sh"
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(duong_hook)
    if ly_do:
        return ly_do
    hook = duong_hook.read_text(encoding="utf-8")
    bang("MA_GO=${PIPESTATUS[0]" not in hook,
         "doc lai PIPESTATUS SAU `|| MA_GO=$?` — chinh dong do dat lai PIPESTATUS ve 0")
    bang("set -euo pipefail" in hook, "hook mat pipefail thi `$?` khong con la ma cua python")
    # ...va chay THAT hinh dang pipeline do trong bash, doi ma 3 di toi noi
    kich = ("set -euo pipefail\n"
            "gia_lap() { echo loi; return 3; }\n"
            "MA_GO=0\n"
            "gia_lap 2>&1 | sed 's/^/[x] /' >/dev/null || MA_GO=$?\n"
            'if [ "$MA_GO" -ne 0 ]; then CHAN=1; else CHAN=0; fi\n'
            'printf "%s %s" "$MA_GO" "$CHAN"\n')
    # CHON bash CHO ĐÚNG. Trên `windows-latest`, `shutil.which("bash")` trả về **WSL
    # bash** (`wsl.exe`), mà runner không cài distro nào — nó trả một thông điệp UTF-16
    # "Windows Subsystem for Linux has no installed distributions" và ca này đỏ với lý
    # do chẳng liên quan gì tới điều đang đo. Đo được ở lượt Windows THẬT đầu tiên
    # (PR #128). Đây là bash CỦA GIT, thứ hook phiên thật sự chạy trên.
    #
    # KHÔNG đoán theo đường dẫn: THỬ từng ứng viên bằng một lệnh biết trước kết quả,
    # rồi mới dùng. "Có tệp tên bash" khác "bash chạy được" — đúng doctrine CÓ MẶT ≠
    # DÙNG ĐƯỢC mà cả nhánh này dựng.
    ung_vien = [c for c in (shutil.which("bash"),
                            r"C:\Program Files\Git\bin\bash.exe",
                            r"C:\Program Files\Git\usr\bin\bash.exe") if c]
    vo = None
    for c in ung_vien:
        try:
            t = subprocess.run([c, "-c", "printf ok"], capture_output=True, text=True,
                               timeout=30)
        except (OSError, subprocess.SubprocessError):
            continue
        if t.stdout.strip() == "ok":
            vo = c
            break
    if vo is None:
        return f"khong co bash CHAY DUOC tren nen nay (da thu: {ung_vien})"
    r = subprocess.run([vo, "-c", kich], capture_output=True, text=True, timeout=30)
    bang(r.stdout.strip() == "3 1",
         f"hinh dang pipeline khong dua duoc ma 3 toi co chan ({vo}): {r.stdout!r}")


@ca
def t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec():
    """Đường MCP — đường kho THẬT SỰ dùng — phải được ĐO, và đo đúng phạm vi.

    VÌ SAO CÓ CA NÀY. `_do_github` đo `git`/`gh`/`rest` nhưng KHÔNG đo MCP; docstring
    của nó LIỆT KÊ "công cụ MCP github CHẠY" như dữ kiện — một quan sát đóng băng
    trong chú thích, không phải phép đo chạy mỗi lượt. Đúng lớp bệnh mà chính hàm ấy
    vừa chữa cho `rest` ("có thể bị chặn" không phải phép đo).

    Ca này khoá năm điều, và mỗi điều là một finding đã trả giá qua sáu lượt cross-review:
      1. `mcp` KHÔNG được nằm trong `LAM_DUOC_VIEC` — CLI duyệt server không chứng
         minh PHIÊN gọi được `mcp__github__*`
      2. đọc `.mcp.json`: khớp tên CHÍNH XÁC, kiểm kiểu BA TẦNG, từ chối khi MƠ HỒ
      3. hỏi CLI bằng ĐÚNG tên đã khai (CLI phân biệt hoa/thường, `rc=0` cả khi
         không tìm thấy)
      4. `Status:` lấy bản ĐẦU TIÊN — nội dung `.mcp.json` chèn được bản GIẢ phía sau
      5. trạng thái LẠ -> `khong_do_duoc`, và nó phải kết xuất KHÁC `hong`
    """
    import json as _json
    m = _tai_launcher_thu()

    # (1) `mcp` KHONG duoc tinh la "lam duoc viec". Doc THANG ma nguon: mot ca doc
    #     bang cach goi `_do_github` roi suy tu nhan se khong phan biet duoc "mcp
    #     khong tinh" voi "mcp tinh nhung tinh co dang hong".
    nguon = Path(m.__file__).read_text(encoding="utf-8")
    khoi = nguon[nguon.index("LAM_DUOC_VIEC = {"):]
    khoi = khoi[:khoi.index("}") + 1]
    # BA TEN, KHONG PHAI MOT. Ban truoc chi tim chuoi `"mcp"` co dau nhay hai dau;
    # sau khi PLAT-M4 tach truong thanh `mcp-cli`/`mcp-endpoint` thi mau ay khong con
    # khop ten nao — ca canh VAN XANH ma khong con canh gi, va dot bien them
    # `"mcp-endpoint"` vao `LAM_DUOC_VIEC` SONG SOT. Do la lo do duoc TRUOC khi viet ma,
    # nen no o day: moi ten moi phai duoc them vao danh sach nay.
    for _ten_mcp in ("mcp", "mcp-cli", "mcp-endpoint", "antigravity", "agy"):
        bang(f'"{_ten_mcp}"' not in khoi and f"'{_ten_mcp}'" not in khoi,
             f"`{_ten_mcp}` bi tinh vao LAM_DUOC_VIEC — do MCP/antigravity KHONG phai thao tac kho hop le: {khoi!r}")
    for phai_co in ("git", "gh-kho", "rest-kho"):
        bang(phai_co in khoi, f"LAM_DUOC_VIEC thieu duong `{phai_co}`: {khoi!r}")

    # (1b) `rest-kho` khi KHONG DOC DUOC SLUG phai day co `None`, khong phai `False`.
    #      Chi tiet cua chinh dong ay tu khai "KHONG DO DUOC" — de co `False` thi nhan
    #      in ra `rest-kho=khong`, tuc noi NGUOC voi chi tiet ngay canh no. Doc THANG
    #      ma nguon vi goi `_do_github` that se cham mang.
    # ĐO HÀNH VI, không dò chuỗi nguồn. Bản trước chỉ tìm `'("rest-kho", None, …' in
    # nguon` — cross-review lượt 8 hạ đúng: giữ chuỗi ấy trong một comment rồi để hành
    # vi thật trả `False` thì ca vẫn xanh. Một phép kiểm NGUỒN không chứng minh HÀNH VI.
    goc_rest, goc_git = m._do_rest_github, m._git
    goc_run_g, goc_which_g = m.subprocess.run, m.shutil.which

    def git_gia(ws, *a, **k):
        if a[:2] == ("remote", "get-url"):
            return (0, "https://gitlab.example/khong-phai-github/x.git", "")
        return (1, "", "")

    class _Rc0:
        returncode, stdout, stderr = 1, "", ""

    # PHẢI GIẢ CẢ `subprocess.run`, KHÔNG chỉ giả `_git`/`_do_rest_github`.
    # ĐÃ TRẢ GIÁ: bản đầu của khối này để `_do_github` chạy THẬT `gh auth status` với
    # `env={}` — không HOME, không PATH — nên trên runner (nơi CÓ `gh`) `gh` ghi
    # `.local/` vào chính cây làm việc và bước "cây phải sạch" của `launcher-windows`
    # ĐỎ trên CẢ ubuntu LẪN windows (`BAN: ?? .local/`). Ở máy dev thì XANH, vì máy dev
    # KHÔNG cài `gh` nên nhánh ấy không chạy — đúng bệnh "ca đo MÁY chứ không đo HỢP
    # ĐỒNG" mà chuỗi review này đã gặp năm lần, lần này ở chiều ngược: ca chỉ HỎNG ở nơi
    # công cụ CÓ MẶT. Không lời đọc mã nào bắt được; chỉ lượt chạy thật trên runner.
    m._do_rest_github = lambda *a, **k: ("mo", "gia", True)
    m._git = git_gia
    m.shutil.which = lambda t, *a, **k: None      # không đường phụ nào được gọi
    m.subprocess.run = lambda *a, **k: _Rc0()     # và nếu có, nó KHÔNG ra tiến trình thật
    try:
        with tempfile.TemporaryDirectory() as td_g:
            _tt, mo_ta_g = m._do_github(td_g, {})
    finally:
        m._do_rest_github, m._git = goc_rest, goc_git
        m.subprocess.run, m.shutil.which = goc_run_g, goc_which_g
    bang("rest-kho=chua-do-duoc" in mo_ta_g,
         f"khong doc duoc slug thi `rest-kho` phai la CHUA DO DUOC, khong phai `khong` "
         f"(da do va hong): {mo_ta_g!r}")

    # (5) BA trang thai phai ket xuat KHAC NHAU — `None` != `False`.
    bang([m._nhan_duong(v) for v in (True, False, None)] == ["OK", "khong", "chua-do-duoc"],
         "ket xuat khong phan biet du ba trang thai cua mot duong")

    KHOE = "github:\n  Scope: User config\n  Status: √ Connected\n  Type: stdio\n"
    PENDING = ("github:\n  Scope: Project config (shared via .mcp.json)\n"
               "  Status: ⏸ Pending approval (run `claude` to approve)\n")

    goc_run, goc_which = m.subprocess.run, m.shutil.which
    mcp_out, co_claude, nhat_ky = [KHOE], [True], []
    ten_mong_doi = ["github"]
    ENV_SENTINEL = [None]        # dat khi ca TU truyen env; None = goi theo mac dinh

    class Rc:
        def __init__(self, rc, out=""):
            self.returncode, self.stdout, self.stderr = rc, out, ""

    def dac_ta():
        return (("claude", "mcp", "get", ten_mong_doi[0]),
                {"capture_output": True, "text": True,
                 "encoding": "utf-8", "errors": "replace",
                 "timeout": m.PROBE_TIMEOUT_GIAY})

    def gia_run(cmd, *_a, **_k):
        if list(cmd)[:2] != ["claude", "mcp"]:
            return Rc(1)                       # gh/git: ngoai pham vi ca nay
        # DO GIA TU TU CHOI loi goi lech dac ta — chot TOAN PHAN, khong opt-in. Bon
        # luot cross-review lien tiep tim duoc dot bien song sot o dung lop nay, va
        # ca bon lan vi ca test cham diem le te nhung gi nguoi va NGHI RA phai dung,
        # tuc mot danh sach CAM. Nay dao thanh danh sach CHO PHEP.
        thay = (tuple(cmd), {k: v for k, v in _k.items() if k not in ("env", "stdin", "executable")})  # wp1077
        nhat_ky.append(thay)
        bang(thay == dac_ta(), f"loi goi `claude` lech dac ta\n  mong: {dac_ta()!r}\n  do  : {thay!r}")
        # KIEM GIA TRI, khong chi kiem KHOA CO MAT. Cross-review luot 7 tim duoc dot
        # bien thu NAM cua lop "do DO GIA" o dung day: `env=moi_truong -> env=None`
        # SONG SOT, vi chot chi hoi `"env" in _k`. Ma `subprocess.run(env=None)` ke
        # thua `os.environ` THO — dung lop P2 ma #143 da va.
        bang(_k.get("env") is not None,
             f"env=None se ke thua os.environ THO (bien giu cho!) — kwargs={_k!r}")
        # ...va phai DUNG object da truyen. Doi "la dict" thoi thi mot ban va bo qua
        # tham so roi lay `os.environ` van qua — `os.environ` cung la dict. Dot bien
        # `env_da_chuan_tra_ve_os_environ_THO` SONG SOT dung mot luot vi le do.
        if ENV_SENTINEL[0] is not None:
            bang(_k["env"] is ENV_SENTINEL[0],
                 f"env KHONG phai object da truyen — tham so bi bo qua? {_k['env']!r}")
        bang(_k.get("stdin") is not None, "phai dong stdin, kheo CLI treo cho nhap")
        return Rc(0, mcp_out[0])

    m.shutil.which = lambda t, *a, **k: (
        ("/usr/bin/claude" if co_claude[0] else None) if t == "claude"
        else None if t == "gh" else goc_which(t, *a, **k))
    m.subprocess.run = gia_run
    try:
        with tempfile.TemporaryDirectory() as td:
            def do(mong_goi=1, vi_tri=""):
                nhat_ky.clear()
                try:   # #1079 F01: hợp đồng là BẮT lỗi rồi trả kết quả — ném ra ngoài là ĐỎ do chốt
                    kq = m._doc_mcp_json(td)
                except Exception as e:  # noqa: BLE001
                    raise TinHieuChotCa(f"[{vi_tri}] `_doc_mcp_json` nem {type(e).__name__} thay vi tra ket qua: {e}")
                bang(len(kq) == 4,
                     f"`_doc_mcp_json` phai tra 4 phan tu (them `url`), do {len(kq)}")
                if kq[0]:
                    ENV_SENTINEL[0] = {"TL_ENV_DA_CHUAN": "1"}
                    kq = (kq[0], kq[1], kq[2], kq[3],
                          m._suc_khoe_mcp_github(kq[2], ENV_SENTINEL[0]))
                else:
                    # NHANH AM: `url` phai la None. Ba phan tu dau giu nguyen hop dong cu
                    # de phan con lai cua ca nay doc y het truoc khi co PLAT-M4.
                    bang(kq[3] is None, f"chua khai server ma van tra url: {kq[3]!r}")
                    kq = kq[:3]
                bang(len(nhat_ky) == mong_goi,
                     f"[{vi_tri}] mong {mong_goi} loi goi `claude`, do {len(nhat_ky)}")
                return kq

            def do_day_du():
                return m._doc_mcp_json(td, kem_headers=True)

            def ghi(o):
                (Path(td) / ".mcp.json").write_text(_json.dumps(o), encoding="utf-8")

            # (2) LUOC DO — moi hinh dang duoi day tung duoc tinh la "da khai server"
            for xau in ([], {"mcpServers": ["github"]}, {"mcpServers": "github"},
                        {"mcpServers": {"github": None}}, {"mcpServers": {"github": "x"}},
                        {"mcpServers": {"not-github-backup": {}}},
                        {"mcpServers": None, "servers": {"github": {}}},
                        {"mcpServers": {}, "servers": {"github": {}}},
                        "mcpServers", 7):
                ghi(xau)
                co, mo_ta, ten = do(0, f"luoc do {xau!r}")
                bang(not co and ten is None, f"luoc do sai {xau!r} ma tinh la da khai: {mo_ta!r}")
            bang("[workspace]" in mo_ta, f"khong khai doc o goc nao: {mo_ta!r}")

            # ...JSON HONG CU PHAP: phai bat, khong duoc nem ra ngoai. (Ca nay tung bi
            # bo quen luc viet lai t115 cho ban hoa nhap, va dot bien
            # `mcp_bo_bat_loi_json_hong` SONG SOT dung mot luot vi the.)
            (Path(td) / ".mcp.json").write_text("{khong phai json", encoding="utf-8")
            co, mo_ta, ten = do(0, "json hong cu phap")
            bang(not co and ten is None, f".mcp.json hong ma tinh la da khai: {mo_ta!r}")

            # ...THIEU HAN tep
            (Path(td) / ".mcp.json").unlink()
            co, mo_ta, ten = do(0, "thieu .mcp.json")
            bang(not co and ten is None, f"thieu .mcp.json ma tinh la da khai: {mo_ta!r}")

            # ...MO HO thi TU CHOI, va khong duoc phu thuoc THU TU KHOA JSON
            for thu_tu in ({"github": {}, "GitHub": {}}, {"GitHub": {}, "github": {}}):
                ghi({"mcpServers": thu_tu})
                co, mo_ta, _ = do(0, f"mo ho {list(thu_tu)}")
                bang(not co and "MO HO" in mo_ta, f"hai ten khop casefold ma nhan: {mo_ta!r}")

            # (3) HOI BANG DUNG TEN DA KHAI — CLI phan biet hoa/thuong
            ghi({"mcpServers": {"GitHub": {}}})
            ten_mong_doi[0] = "GitHub"
            *_, (tt, _mo) = do(1, "ten hoa/thuong")
            bang(tt == "khoe", f"ten `GitHub` ma tra {tt}")
            ten_mong_doi[0] = "github"

            ghi({"mcpServers": {"github": {}}})
            day_du = do_day_du()
            bang(len(day_du) == 5 and day_du[4] == {},
                 f"headers vang mat khong tra object rong: {day_du!r}")
            ghi({"mcpServers": {"github": {"url": "https://x", "headers": None}}})
            day_du = do_day_du()
            bang(not day_du[0] and day_du[4] is None and "headers" in day_du[1],
                 f"headers falsy co mat khong bi tu choi: {day_du!r}")
            ghi({"mcpServers": {"github": {}}})
            # ...va dau ra "khong tim thay" (rc=0!) phai la KHONG DO DUOC
            mcp_out[0] = 'No MCP server named "github". Did you mean "GitHub"?\n'
            *_, (tt, mo) = do(1, "khong tim thay")
            bang(tt == "khong_do_duoc", f"dau ra khong-tim-thay (rc=0) ma tra {tt}: {mo!r}")

            # (4) `Status:` GIA do `.mcp.json` chen — phai doc ban DAU TIEN
            mcp_out[0] = ("github:\n  Scope: User config\n"
                          "  Status: × Failed to connect\n  Issue: ENOENT\n"
                          "  Type: stdio\n  Command: /bin/echo\n  Args: x\n"
                          "  Status: √ Connected\ny\n")
            *_, (tt, mo) = do(1, "chen Status gia")
            bang(tt == "hong" and "Failed to connect" in mo,
                 f"doc phai `Status:` GIA do .mcp.json chen: {tt} {mo!r}")

            # (5) TRANG THAI XAU / LA / TOT
            for xau, mong in (("⏸ Pending approval (run `claude` to approve)", "hong"),
                              ("× Failed to connect", "hong"),
                              ("Disconnected", "hong"), ("not connected", "hong"),
                              ("√ Connected", "khoe"), ("Connected", "khoe"),
                              ("\x1b[32mConnected\x1b[0m", "khoe"),
                              ("Connected (stale)", "khong_do_duoc"),
                              ("Connected - 3 tools", "khong_do_duoc"),
                              ("Reconnecting", "khong_do_duoc")):
                mcp_out[0] = f"github:\n  Status: {xau}\n"
                *_, (tt, mo) = do(1, f"trang thai {xau!r}")
                bang(tt == mong, f"trang thai {xau!r}: mong {mong}, do {tt} ({mo!r})")

            # GOI THANG THEO MAC DINH (khong truyen env) — ham phai TU chuan hoa,
            # khong duoc de `None` roi xuong `subprocess.run`. Day la duong ma
            # cross-review luot 7 chi ra: chot phai bao ve HOP DONG, khong dua vao
            # viec moi call-site deu nho truyen env.
            ghi({"mcpServers": {"github": {}}})
            mcp_out[0] = KHOE
            nhat_ky.clear()
            ENV_SENTINEL[0] = None
            tt, _mo = m._suc_khoe_mcp_github("github")
            bang(tt == "khoe", f"goi thang theo mac dinh ma tra {tt}")

            # ...khong co `claude` de hoi -> KHONG DO DUOC, va KHONG duoc goi gi
            co_claude[0] = False
            mcp_out[0] = KHOE
            *_, (tt, _mo) = do(0, "khong co claude")
            bang(tt == "khong_do_duoc", f"khong co `claude` ma tra {tt}")
            co_claude[0] = True
    finally:
        m.subprocess.run, m.shutil.which = goc_run, goc_which


@ca
def t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho():
    """Mẫu tìm-thay của MỖI đột biến phải khớp ĐÚNG MỘT chỗ trong `launcher.py`.

    VÌ SAO CÓ CA NÀY — nó chặn một cách làm hỏng chốt mà KHÔNG sửa dòng nào của ai.
    `chay_dot_bien` thay chỗ khớp ĐẦU TIÊN. Nên nếu mã mới TRÙNG CHỮ với đoạn mà một
    đột biến cũ đang nhắm, VÀ đứng trước nó, thì đột biến ấy lặng lẽ nhảy sang bản sao:
    ca đích không chết nữa, mà bảng vẫn báo "đạt".

    ĐÃ XẢY RA THẬT trong chính đợt này: khối chuẩn hoá env chép vào
    `_suc_khoe_mcp_github` trùng khít với khối của `_do_github` và đứng trước nó ⇒
    `probe_github_bo_qua_moi_truong_chuan_hoa` (đột biến CÓ SẴN, canh `t113`) SỐNG SÓT.
    Không dòng logic nào sai; chốt chỉ mất răng vì trùng chữ. Chữa bằng `_env_da_chuan`,
    và chốt NÀY để lần sau không phải trông vào việc ai đó tình cờ chạy đột biến rồi
    đọc kỹ dòng `SAI`.

    Đây là ca đo CÔNG CỤ ĐO, không đo `launcher.py` — cùng họ với `t116`.

    GIỚI HẠN — cùng phạm vi phải khai như `t116`, và cross-review lượt 8 đúng khi bảo
    lời khai cũ ("cùng họ với `t116`") HẸP HƠN thứ cần công bố. Nói cho đủ: ca này lấy
    CẢ đặc tả (`DOT_BIEN` và `DA_BIET_TRUNG` ngay trong tệp test) LẪN bằng chứng
    (`launcher.py`) từ những tệp mà một thay đổi PHỐI HỢP sửa được cùng lúc — thêm một
    bản sao rồi nới `DA_BIET_TRUNG` cho khớp thì ca vẫn xanh. Nó chặn được việc TÌNH CỜ
    dựng ra chỗ trùng (đúng ca đã xảy ra thật), KHÔNG chặn được sửa đổi có chủ ý. Muốn
    chặn thì phải neo kỳ vọng ở NGUỒN ĐỘC LẬP; chưa làm, và không khai là đã làm.
    """
    from pathlib import Path as _P
    # Đọc đúng launcher ĐANG được runner thử; ở suite thường biến này chính là
    # `LAUNCHER`, còn trong `--dot-bien` nó trỏ bản sao mutant riêng.
    nguon = _P(LAUNCHER_DANG_DUNG).read_text(encoding="utf-8")
    # DANH SÁCH CHO PHÉP, không phải danh sách cấm: nêu đích danh chỗ ĐÃ BIẾT là trùng,
    # kèm lý do. Bất cứ chỗ trùng nào KHÁC đều làm ca này ĐỎ.
    #
    # `hook_phien_bo_phep_so_nang_luc` trùng 2 chỗ — `_do_hook_cu` và `_do_launcher_cu`
    # có cùng dòng `thieu = sorted(cua_master - dang_co)`. ĐO ĐƯỢC: nợ này CÓ SẴN trên
    # master `c7ad260`, KHÔNG phải do bản vá MCP tạo ra. Nó đang LATENT chứ chưa hỏng:
    # ca đích (`t88`) nói về HOOK, và `_do_hook_cu` tình cờ đứng TRƯỚC — tức chốt đang
    # đúng NHỜ THỨ TỰ, không nhờ thiết kế. Dọn nó là thay đổi RIÊNG (đụng mã của #143);
    # ghi ra đây để nó không nằm im mà không ai biết.
    # KHOA DUNG SO LUONG, khong phai "khac 1". Cross-review luot 8 ha dung cho nay:
    # `!= 1` cho qua CA 0 LAN 3 — nen mot ban sao THU BA dat truoc `_do_hook_cu` se
    # tuoc rang `t88` ma ca nay VAN XANH. Mot ngoai le khai "dang no 2 cho" thi phai
    # khoa o DUNG 2; moi con so khac deu la trang thai chua ai xet.
    DA_BIET_TRUNG = {"hook_phien_bo_phep_so_nang_luc": 2}
    la = []
    for muc in DOT_BIEN:
        ten, cap = muc[0], muc[1]
        for c, _ in ([cap] if isinstance(cap, tuple) else cap):
            n = nguon.count(c)
            mong = DA_BIET_TRUNG.get(ten, 1)
            if n != mong:
                la.append((ten, f"dem={n} mong={mong}", c.splitlines()[0][:55]))
    bang(not la, "mau dot bien khong khop dung so cho da khai (chot dang nham sai cho, "
                 f"hoac ngoai le da doi so luong ma chua ai xet lai): {la}")


@ca
def t116_moi_ham_ca_phai_duoc_DANG_KY_bang_decorator():
    """Mọi `def tNN_...`/`rNN_...` phải có `@ca` ngay trên — nếu không, ca KHÔNG CHẠY.

    VÌ SAO CÓ CA NÀY: tôi vừa tự gây ra đúng lỗi ấy khi chèn `t115`. Điểm chèn rơi vào
    GIỮA `@ca` và `def t101_...`, nên decorator của `t101` quay sang trang trí `t115`:
    một ca được thêm, một ca lặng lẽ MẤT. Suite vẫn in `114/114` — hai số BẰNG NHAU,
    đúng thứ kho dạy là dấu hiệu tin được — mà thật ra tổng đã tụt một.

    Đó là bệnh `t24` của kho ("ca CÓ MẶT khác ca có ĐO") ở một mặt khác: ca có mặt
    trong TỆP, chạy được bằng `--lap-ca`, thậm chí giết được đột biến (vì bộ đột biến
    gọi ca THEO TÊN chứ không qua `CA`) — nhưng suite thì không bao giờ chạy nó. Không
    phép đo nào của lượt chạy thường nhìn thấy chỗ mất ấy.

    Chốt này rẻ và tất định: đọc chính tệp này, đếm hai thứ, đòi bằng nhau.

    GIỚI HẠN — KHAI THẲNG, vì cross-review lượt 7 CHỨNG MINH ĐƯỢC chứ không phải suy:
    chốt lấy CẢ đặc tả LẪN bằng chứng từ cùng một tệp, nên một thay đổi PHỐI HỢP (gỡ
    `@ca` của `t115` ĐỒNG THỜI sửa bộ quét cho bỏ qua `def t115_`) vẫn qua. Nó bắt được
    lỗi VÔ TÌNH mất decorator — đúng ca đã xảy ra thật — chứ không chống được sửa đổi có
    chủ ý. Muốn chống tự-lừa phải neo danh sách ca ở NGUỒN ĐỘC LẬP; chưa làm, và không
    khai là đã làm.
    """
    import re as _re
    dong = Path(__file__).read_text(encoding="utf-8").splitlines()
    ham = [(i, l) for i, l in enumerate(dong) if _re.match(r"^def [tr]\d+_", l)]
    thieu = [l.split("(")[0][4:] for i, l in ham if i == 0 or dong[i - 1].strip() != "@ca"]
    bang(not thieu, f"ca co mat trong TEP ma KHONG duoc dang ky (thieu `@ca`): {thieu}")
    # ...va so ca DA DANG KY phai khop so ham. Hai phep dem doc lap: mot doc TEP, mot
    # doc bang `CA` da nap. Lech nhau nghia la co ca bi trang tri hai lan, hoac co
    # `@ca` gan cho thu khong phai ca.
    bang(len(ham) == len(CA),
         f"{len(ham)} ham `tNN_/rNN_` nhung `CA` co {len(CA)} muc — co cho dang ky lech")


@ca
def t118_headline_KHONG_duoc_dem_ca_BO_QUA_la_da_qua():
    """`N/N` chỉ nói về ca ĐÃ CHẠY; tổng và bỏ-qua phải khai riêng cạnh đó.

    Dòng kết luận cũ lấy `qua + bo_qua` làm tử số, nên trên Windows — nơi nhiều ca
    tự bỏ qua vì cần POSIX — nó in `118/118 ca` như thể mẫu số là toàn suite.
    Dạng mới dùng `qua/đã_chạy`, đồng thời khai `tong` và `bo qua` ngay trong cùng
    dòng: hai số bằng nhau chứng minh toàn bộ phần đã đo xanh, không che phần chưa
    đo. (Bộ số neo tại `99ba7857`, ba kênh độc lập cùng
    ra `qua=105, bo_qua=13, tong=118`: máy dev cp1258, CI windows-latest, PR
    #153. Bản đầu của docstring này ghi `117/117` với `bo qua 14` — không khớp
    phép đo nào tại head ấy; nếu từng là số thật thì thuộc một tree cũ không
    còn định danh được — review W0-M1 bắt, P3.) Đây là
    `t116` ở tầng BÁO CÁO: ở đó tổng tụt một mà
    vẫn in `114/114`; ở đây tổng đúng mà tử số phồng lên bằng số ca không chạy.

    Ca này KHÔNG gọi CLI vì thứ cần đo là một phép tính thuần: `dong_ket_qua` đã
    được tách khỏi `main` đúng vì lý do đó (cùng lý lẽ khiến `chay_bo_ca` được
    tách cho `t99`). Khối (c) vẫn đi qua ĐƯỜNG ĐẾM THẬT `chay_bo_ca`, nên nó đo
    hành vi chứ không đo lại một hằng số tôi vừa gõ.

    GIỚI HẠN — khai thẳng, và đã bị bắt HAI LẦN, hai chiều ngược nhau: ca này
    khoá CÔNG THỨC của `dong_ket_qua` VÀ — qua khối (c) — phép đếm bỏ-qua của
    `chay_bo_ca`; nhưng KHÔNG khoá việc `main` có gọi nó hay không, cũng KHÔNG
    khoá mã thoát. Bản đầu viết "ca này khoá SỰ THẬT CỦA DÒNG BÁO CÁO" —
    rộng hơn hẳn thứ nó làm được, và review W0-M1 (PR #153, head `99ba7857`)
    chứng minh bằng đột biến: hoàn nguyên ĐÚNG MỘT dòng ở cuối `main` về
    `{qua + bo_qua}/{tong}`, giữ nguyên `dong_ket_qua` lẫn ca này, thì ca này
    VẪN XANH và headline in lại `118/118` với 13 ca chưa hề đo.
    Dây nối ấy nay do `t119` khoá — và `t119` đo bằng HÀNH VI (gọi `main()` trên
    bản sao rồi đọc stdout), nên nó cũng đo luôn "bỏ qua vẫn cho rc=0", thứ ca
    này chỉ khai suông. Đổi rc là quyết định riêng, Packet riêng.
    Rồi review W0-M1b (PR #159) bắt tiếp chiều NGƯỢC LẠI: câu vá đầu viết "CHỈ
    khoá CÔNG THỨC" — HẸP hơn thực tế. Đột biến tầng đếm (`bo_qua += 1` thành
    `qua += 1` trong `chay_bo_ca`, để `dong_ket_qua` nguyên vẹn) làm ca này ĐỎ,
    tức nó khoá nhiều hơn công thức. Khai hẹp không tái phát bệnh khai rộng,
    nhưng vẫn sai: người sau sẽ thêm ca thừa cho thứ đã có người canh.
    Đây đúng nếp `t116`/`t117` của tệp này: chưa làm thì đừng khai là đã làm.
    """
    # (a) khong bo qua, khong hong: N/N la HOP LE va phai duoc giu nguyen suc nang
    d = dong_ket_qua(10, 10, 0, 0)
    bang(d.startswith("10/10 "), f"da lam mat N/N cua luot chay SACH: {d!r}")
    bang("BO QUA" not in d, f"khong co ca bo qua ma van canh bao: {d!r}")

    # (b) co ca bo qua: cap dau la qua/da-chay; tong/bo-qua khai rieng
    d = dong_ket_qua(10, 7, 3, 0)
    bang(d.startswith("7/7 "),
         f"mau so khong phai so ca da chay: {d!r}")
    bang("10/10" not in d,
         f"van dung tong suite lam cap N/N du co ca chua chay: {d!r}")
    bang("tong 10, bo qua 3" in d and "BO QUA" in d,
         f"khong noi ro tong va so ca bo qua: {d!r}")

    # (c) PHAN CHUNG: bien DUNG MOT ca qua thanh BO QUA, di qua duong dem THAT.
    def ca_qua_1():
        pass

    def ca_qua_2():
        pass

    def ca_moc():          # luot 1: qua
        pass

    def ca_moc_bo_qua():   # luot 2: cung vi tri, nhung tu bo qua
        return "co tinh bo qua"

    def dem(ds):
        cu = sys.stdout
        sys.stdout = io.StringIO()      # nuot dong "BO QUA ..." cua ca gia
        try:
            return chay_bo_ca(ds)
        finally:
            sys.stdout = cu

    q1, b1, h1 = dem([ca_qua_1, ca_qua_2, ca_moc])
    q2, b2, h2 = dem([ca_qua_1, ca_qua_2, ca_moc_bo_qua])
    bang((q1, b1, len(h1)) == (3, 0, 0),
         f"fixture hong: luot dau phai 3 qua/0 bo qua/0 hong, duoc {q1}/{b1}/{len(h1)}")
    bang((q2, b2, len(h2)) == (2, 1, 0),
         f"fixture hong: luot sau phai 2 qua/1 bo qua/0 hong, duoc {q2}/{b2}/{len(h2)}")
    bang(q2 == q1 - 1,
         f"doi mot ca QUA thanh BO QUA ma so passed KHONG giam: {q1} -> {q2}")
    truoc = dong_ket_qua(3, q1, b1, len(h1))
    sau = dong_ket_qua(3, q2, b2, len(h2))
    bang(truoc.startswith("3/3 "), f"luot sach phai la N/N: {truoc!r}")
    bang(sau.startswith("2/2 ") and "tong 3, bo qua 1" in sau,
         f"headline khong tach qua/da-chay khoi tong/bo-qua: {sau!r}")


@ca
def t119_main_nhanh_mac_dinh_PHAI_in_headline_bang_dong_ket_qua():
    """`dong_ket_qua` đúng mà `main` không GỌI nó thì headline vẫn nói dối được.

    Finding P3 của review W0-M1 (PR #153, head `99ba7857`), tái lập được: mutant
    thay lời gọi `dong_ket_qua(...)` ở cuối `main` bằng chính f-string cũ
    `{qua + bo_qua}/{tong}` cho rc=0 mà `t118` vẫn xanh — `t118` đo HÀM, không
    đo DÂY NỐI, và không ca nào khác đọc headline của nhánh mặc định (đã grep:
    `main()` chỉ được gọi ở `sys.exit(main())`, chuỗi "ca QUA (" chỉ sinh ở
    `dong_ket_qua`). Bệnh `t24`/`t116` thêm một tầng: hàm CÓ MẶT trong tệp,
    có test riêng, mà lượt chạy thật không đi qua nó.

    Đo bằng HÀNH VI, không grep nguồn: assert "nguồn `main` chứa `dong_ket_qua(`"
    sẽ tha mutant gọi-mà-không-in (`_ = dong_ket_qua(...)` — nguồn vẫn chứa
    chuỗi ấy mà stdout mất headline). Cũng KHÔNG spawn `--lap-ca` như finding
    gợi ý: nhánh `--lap-ca` in dòng `LAP ...` riêng của nó, KHÔNG đi qua
    `dong_ket_qua` (xem `main`) — đo rồi mới thấy gợi ý ấy trỏ nhầm máy in.

    Cách đo: nạp BẢN SAO module này (`_nap_sach`, seam sẵn có của bộ đột biến),
    thay `CA` bằng ca giả, stub khối tự-khai/tách-nhóm (mỗi khối đã có ca riêng
    đo nó), rồi gọi `main()` THẬT và đọc stdout. Ba nhánh: sạch (headline phải
    là N/N đúng nghĩa), có BO QUA (cảnh báo phải RA TỚI stdout và rc giữ 0 —
    biến câu "Mã thoát KHÔNG đổi" mà `t118` chỉ khai suông thành phép đo), có
    HONG (rc phải 1).

    GIỚI HẠN — khai thẳng: stub nghĩa là tổ hợp này không đo `khai_moi_truong`
    lẫn `_tu_tach_nhom_neu_can`; và `sys.exit(main())` dưới `__main__` vẫn
    ngoài tầm — ca này đo GIÁ TRỊ TRẢ VỀ của `main`, không đo mã thoát tiến
    trình. Đổi phối hợp (sửa cả `main` lẫn ca này) thì không chống được — cùng
    giới hạn đã khai ở `t116`.
    """
    def _chay_main_voi(ds_ca):
        m = _nap_sach(Path(__file__))
        m.CA = list(ds_ca)
        m.khai_moi_truong = lambda: {}
        m._mot_dong_moi_truong = lambda mt: "moi truong: (ca thu, da stub)"
        m._tu_tach_nhom_neu_can = lambda: "bo qua (ca thu, da stub)"
        m.phan_tich_doi_so = lambda argv: argparse.Namespace(
            dot_bien=False, moi_truong=False, lap_ca=None, lan=20, nhat_ky=None)
        ra = io.StringIO()
        with contextlib.redirect_stdout(ra):
            rc = m.main()
        return rc, ra.getvalue()

    def ca_qua():
        pass

    def ca_bo_qua():
        return "thieu POSIX (gia lap)"

    def ca_hong():
        raise AssertionError("hong co tinh")

    # (a) nhanh sach: headline THAT tren stdout phai dung tung byte
    rc, ra = _chay_main_voi([ca_qua])
    cuoi = ra.rstrip().splitlines()[-1]
    bang(rc == 0, f"nhanh sach phai rc=0, duoc {rc}")
    bang(cuoi == "1/1 ca DA CHAY QUA (tong 1, bo qua 0, hong 0)",
         f"headline nhanh mac dinh KHONG di qua dong_ket_qua: {cuoi!r}")

    # (b) co BO QUA: canh bao phai ra toi stdout, va rc GIU 0 (spec W0-M1)
    rc, ra = _chay_main_voi([ca_qua, ca_bo_qua])
    cuoi = ra.rstrip().splitlines()[-1]
    bang(cuoi == "1/1 ca DA CHAY QUA (tong 2, bo qua 1, hong 0)"
                  " - KHONG DU: 1 ca BO QUA, chua do gi",
         f"canh bao BO QUA khong toi duoc stdout: {cuoi!r}")
    bang(rc == 0, f"bo qua khong duoc doi ma thoat (spec W0-M1) ma rc={rc}")

    # (c) co HONG: rc phai 1 va headline dem dung
    rc, ra = _chay_main_voi([ca_qua, ca_hong])
    cuoi = ra.rstrip().splitlines()[-1]
    bang(rc == 1, f"co ca hong ma rc={rc}")
    bang(cuoi == "1/2 ca DA CHAY QUA (tong 2, bo qua 0, hong 1)",
         f"headline dem hong sai: {cuoi!r}")


@ca
def t120_subprocess_decoding_chong_loi_charmap_tren_windows():
    """Subprocess helpers phải xử lý an toàn Unicode, tránh UnicodeDecodeError trên cp1258/cp1252.

    Trên Windows console hoặc môi trường tiếng Việt (cp1258), gọi `text=True` mà không
    có `encoding="utf-8", errors="replace"` làm `_readerthread` của `subprocess.run` ném
    `UnicodeDecodeError: 'charmap' codec can't decode byte 0x...`.

    Ca này đo trực tiếp:
    (a) `_chay_van_ban_an_toan` đọc tiến trình in ký tự Unicode/ANSI/Emoji mà không crash;
    (b) `_chay_json_chat_che` đọc JSON UTF-8 đúng và từ chối JSON méo mó.
    """
    m = _tai_launcher_thu()
    # (a) Văn bản có ký tự tiếng Việt có dấu, emoji, ký hiệu pháp luật
    chuoi_test = "✓ Đã thẩm định: Điều 12 Luật Ban hành VBQPPL 🚀 ⚖️"
    p = m._chay_van_ban_an_toan([PY, "-c", f"import sys; sys.stdout.buffer.write({chuoi_test.encode('utf-8')!r})"])
    bang(p.returncode == 0, f"chay_van_ban_an_toan bi loi rc={p.returncode}")
    bang("Đã thẩm định" in p.stdout, f"khong giai ma duoc chuoi Unicode: {p.stdout!r}")

    # (b) JSON chặt chẽ
    rc_j, data_j, err_j = m._chay_json_chat_che([
        PY, "-c", "import sys; sys.stdout.buffer.write(b'{\"status\": \"ok\", \"muc\": \"phap_luat\"}')"
    ])
    bang(rc_j == 0, f"JSON hop le ma rc={rc_j}: {err_j}")
    bang(isinstance(data_j, dict) and data_j.get("status") == "ok",
         f"du lieu parse JSON sai: {data_j}")

    # (c) JSON méo mó / lỗi parse
    rc_bad, data_bad, err_bad = m._chay_json_chat_che([
        PY, "-c", "import sys; sys.stdout.buffer.write(b'{invalid_json}')"
    ])
    bang(rc_bad == -1, f"JSON meo mo phai tra -1, duoc {rc_bad}")
    bang(data_bad is None, f"JSON meo mo khong duoc tra data hop le: {data_bad}")
    bang("loi phan tich JSON" in err_bad, f"thong bao loi sai: {err_bad}")


@ca
def t121_do_openai_llm_qua_cli_khong_fail_open_va_khong_log():
    """Đo công cụ llm cho provider openai_api: không fail-open, không tự gọi API trả phí,
    và bắt buộc `--no-log` khi kiểm sống.

    Giao thức:
      - Provider: openai_api (§4, §5 ops/OPENAI_LLM_PROVIDER.md)
      - Surface: llm_cli
      - Mặc định: CO_CREDENTIAL (chưa chứng minh dùng được), không gọi API
      - Kiểm sống: gọi thật có `--no-log` và exact model
    """
    m = _tai_launcher_thu()

    # (1) Bảng CONG_CU và KHA_NANG phải có llm / openai-llm
    muc_cc = [c for c in m.CONG_CU if c["ten"] == "llm"]
    bang(len(muc_cc) == 1, f"CONG_CU thieu muc llm: {m.CONG_CU}")
    bang(muc_cc[0]["bat_buoc"] is False, "llm khong duoc dat bat buoc mac dinh")

    muc_kn = [k for k in m.KHA_NANG if k["ten"] == "openai-llm"]
    bang(len(muc_kn) == 1, f"KHA_NANG thieu muc openai-llm: {m.KHA_NANG}")

    goc_which = m.shutil.which
    goc_run = m._chay_probe_llm   # wp1077: probe llm cua doctor di qua _chay_probe_llm
    lenh_chay = []

    class _P:
        def __init__(self, rc=0, out="", err=""):
            self.returncode, self.stdout, self.stderr = rc, out, err

    def run_gia(cmd, **k):
        lenh_chay.append((list(cmd), k))
        if list(cmd) == ["llm", "--version"]:
            return _P(0, "llm, version 0.19.1\n")
        if list(cmd) == ["llm", "keys", "list"]:
            return _P(0, "openai\n")
        if list(cmd)[:2] == ["llm", "prompt"]:
            # Phải có --no-log để chống rò rỉ prompt vào SQLite cục bộ
            bang("--no-log" in cmd, f"loi goi llm THIEU --no-log: {cmd}")
            bang("-m" in cmd, f"loi goi llm THIEU -m exact model: {cmd}")
            return _P(0, "ok\n")
        return _P(1, "", "khong ro lenh")

    # (a) THIEU khi which tra None
    m.shutil.which = lambda t, *a, **k: None if t == "llm" else goc_which(t)
    tt, mo_ta = m._do_openai_llm({})
    bang(tt == "THIEU", f"chua cai llm ma bao {tt}: {mo_ta}")

    # (b) CHUA_XAC_THUC khi co llm nhung khong co OPENAI_API_KEY
    m.shutil.which = lambda t, *a, **k: "/usr/bin/llm" if t == "llm" else goc_which(t)
    def run_khong_key(cmd, **k):
        if list(cmd) == ["llm", "--version"]:
            return _P(0, "llm, version 0.19.1\n")
        if list(cmd) == ["llm", "keys", "list"]:
            return _P(0, "")
        return _P(1)
    m._chay_probe_llm = run_khong_key
    tt, mo_ta = m._do_openai_llm({})
    bang(tt == "CHUA_XAC_THUC", f"khong co key ma khong bao CHUA_XAC_THUC: {tt}, {mo_ta}")

    # (c) CO_CREDENTIAL khi co OPENAI_API_KEY nhung kiem_song=False (khong goi API)
    m._chay_probe_llm = run_gia
    lenh_chay.clear()
    tt, mo_ta = m._do_openai_llm({"OPENAI_API_KEY": "sk-mock-key"}, False)
    bang(tt == "CO_CREDENTIAL", f"co key mac dinh phai CO_CREDENTIAL: {tt}")
    bang(not any("prompt" in c[0] for c in lenh_chay),
         f"mac dinh KHONG duoc tu dong goi API tinh phi: {lenh_chay}")

    # (d) DUNG_DUOC khi kiem_song=True va p_song thanh cong
    lenh_chay.clear()
    tt, mo_ta = m._do_openai_llm({"OPENAI_API_KEY": "sk-mock-key"}, True)
    bang(tt == "DUNG_DUOC", f"kiem song thanh cong ma bao {tt}: {mo_ta}")
    bang(any("prompt" in c[0] for c in lenh_chay), "kiem_song=True nhung khong goi probe")

    # (e) CHUA_XAC_THUC khi kiem_song=True nhung api loi
    def run_loi(cmd, **k):
        if list(cmd) == ["llm", "--version"]:
            return _P(0, "llm, version 0.19.1\n")
        if list(cmd)[:2] == ["llm", "prompt"]:
            return _P(1, "", "Error: 401 Unauthorized")
        return _P(0)
    m._chay_probe_llm = run_loi
    tt, mo_ta = m._do_openai_llm({"OPENAI_API_KEY": "sk-mock-key"}, True)
    bang(tt == "CHUA_XAC_THUC", f"kiem song loi phai tra CHUA_XAC_THUC: {tt}")


# ------------------------------------------------- bridge SessionStart (GLS-B1)
#
# VÌ SAO — incident 2026-08-15 (docs/incidents/2026-08-15-launcher-codex-github-toolchain.md),
# nguyên nhân gốc số 4: hook SessionStart shell-form gọi tên trần `bash`; trên Windows tên
# ấy có thể là WSL shim trả Access denied trong khi Git Bash tốt nằm ở Program Files —
# phiên mở ra không có codex/rg mà không ai biết vì hook chết im. Bridge exec-form
# (.claude/hooks/session_start.py) đọc env trước, probe từng ứng viên bash, lấy đường dẫn
# THẬT. Cùng họ t106 của doctor, ở tầng hook. Port từ nhánh codex/gate-lifecycle đã khai
# tử (blob ea85526b) — phần code duy nhất của nhánh ấy còn giá trị sau phép đo collision
# (hồ sơ: PR #160).

def _duong_bridge() -> Path:
    return Path(__file__).resolve().parents[1] / "hooks" / "session_start.py"


def _chay_bridge(env, timeout=60):
    return subprocess.run([PY, str(_duong_bridge())], env=env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout)


def _bash_gia(duong: Path, noi_dung: str) -> Path:
    """Tạo executable tên `bash` tìm được bởi shutil.which trong thư mục đã cho."""
    if LA_WINDOWS:
        p = duong / "bash.exe"
        p.write_text(noi_dung, encoding="utf-8")
    else:
        p = duong / "bash"
        p.write_text(noi_dung, encoding="utf-8")
        os.chmod(p, 0o755)
    return p


@ca
def t122_ung_vien_bash_thu_tu_PATH_dedup_va_fallback_ProgramFiles():
    """Resolver của bridge: đúng thứ tự PATH, không trùng, chỉ nhận tệp có thật.

    Hàm thuần `_ung_vien_bash(env)` nhận CẢ ProgramFiles từ env — cố ý, để đo được
    trên mọi nền không cần máy có Git Bash thật. Nhánh Program Files chỉ tồn tại
    trên Windows nên vế đó kiểm CÓ ĐIỀU KIỆN theo nền, khai thẳng thay vì giả vờ
    đo được ở nơi không có.
    """
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(_duong_bridge())
    if ly_do:
        return ly_do
    m = _nap_sach(_duong_bridge())
    with San() as s:
        d1 = s / "d1"; d2 = s / "d2"; rong = s / "rong"; pf = s / "pf"
        for d in (d1, d2, rong, pf):
            d.mkdir()
        b1 = _bash_gia(d1, "#!/bin/sh\nexit 1\n")
        b2 = _bash_gia(d2, "#!/bin/sh\nexit 1\n")
        (pf / "Git" / "bin").mkdir(parents=True)
        pf_bash = pf / "Git" / "bin" / "bash.exe"
        pf_bash.write_text("x", encoding="utf-8")
        env = {"PATH": os.pathsep.join([str(d1), str(rong), str(d2), str(d1)]),
               "ProgramFiles": str(pf)}
        ra = m._ung_vien_bash(env)
        chuan = [str(b1), str(b2)]
        if platform.system() == "Windows":
            chuan.append(str(pf_bash))
        bang([os.path.normcase(x) for x in ra] == [os.path.normcase(x) for x in chuan],
             f"thu tu/dedup/fallback sai: {ra!r} != {chuan!r}")
        # PHAN CHUNG cho bug da bat khi viet t124: dict(os.environ) Windows viet hoa
        # khoa; ban goc ec8d08c tra env.get("ProgramFiles") case-sensitive nen LUON
        # truot va roi ve default cung C:\Program Files. Khoa viet hoa phai duoc
        # ton trong y het khoa dung chu.
        ra_hoa = m._ung_vien_bash({"PATH": str(d1), "PROGRAMFILES": str(pf)})
        chuan_hoa = [str(b1)] + ([str(pf_bash)] if platform.system() == "Windows" else [])
        bang([os.path.normcase(x) for x in ra_hoa] == [os.path.normcase(x) for x in chuan_hoa],
             f"khoa PROGRAMFILES viet hoa bi bo qua: {ra_hoa!r} != {chuan_hoa!r}")


@ca
def t123_bridge_thieu_session_start_sh_phai_rc12_truoc_khi_probe():
    """Không thấy hook thì đỏ NGAY với lời chẩn đoán, đừng đi probe bash vô ích."""
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(_duong_bridge())
    if ly_do:
        return ly_do
    with San() as s:
        (s / "trong").mkdir()
        env = dict(os.environ)
        env["CLAUDE_PROJECT_DIR"] = str(s / "trong")
        r = _chay_bridge(env)
        bang(r.returncode == 12, f"mong 12, duoc {r.returncode}: {r.stderr[:120]}")
        bang("khong thay hook" in r.stdout, f"thieu chan doan: {r.stdout!r}")


@ca
def t124_bridge_khong_co_bash_chay_duoc_phai_rc12_khong_fail_open():
    """Không ứng viên bash nào ⇒ rc=12 kèm lý do — đây chính là ca fail-closed
    mà hook shell-form cũ KHÔNG thể có: shell-form chết trước khi kịp nói gì.

    PATH và ProgramFiles đều trỏ thư mục rỗng nên resolver hết đường; SystemRoot
    và các biến hệ thống giữ nguyên để python con còn khởi động được (bài t120:
    đừng phá môi trường quá tay rồi đo nhầm cái chết khác).

    ĐÃ TRẢ GIÁ HAI TẦNG ngay lượt viết đầu, cả hai đo được bằng spawn thật:
    (1) `dict(os.environ)` Windows VIẾT HOA khoá — tra case-sensitive trong bridge
    gốc `ec8d08c` LUÔN trượt và rơi về default cứng: bug tiềm ẩn thật, đã vá bằng
    `_lay_env` (phản chứng nằm ở `t122`). (2) Xoá `PROGRAMFILES` thôi CHƯA đủ:
    Windows TÁI SINH họ biến ProgramFiles cho tiến trình mới từ `PROGRAMW6432` /
    `PROGRAMFILES(X86)` — cha gửi fixture, con vẫn nhận `C:\\Program Files` thật.
    Phải xoá TRỌN HỌ rồi mới đặt; đã đo: xoá trọn thì fixture sống sót sang con.
    """
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(_duong_bridge())
    if ly_do:
        return ly_do
    with San() as s:
        du_an = s / "da"; (du_an / ".claude" / "hooks").mkdir(parents=True)
        (du_an / ".claude" / "hooks" / "session-start.sh").write_text(
            "echo hook\n", encoding="utf-8")
        rong = s / "rong"; rong.mkdir()
        env = dict(os.environ)
        for k in [k for k in env
                  if k.upper() in ("PROGRAMFILES", "PROGRAMW6432",
                                   "PROGRAMFILES(X86)", "PATH", "CLAUDE_PROJECT_DIR")]:
            del env[k]
        env.update({"CLAUDE_PROJECT_DIR": str(du_an), "PATH": str(rong),
                    "ProgramFiles": str(rong)})
        r = _chay_bridge(env)
        bang(r.returncode == 12, f"mong 12, duoc {r.returncode}: {r.stderr[:120]}")
        bang("khong co bash chay duoc" in r.stdout, f"thieu ly do: {r.stdout!r}")


@ca
def t125_bridge_bo_bash_hong_dau_PATH_va_truyen_rc_hook_ve_nguyen_ven():
    """Binary hỏng đầu PATH không được che binary tốt phía sau — t106 ở tầng hook.

    Đo bằng fake bash thật sự CHẠY: ứng viên 1 probe rớt (exit 1, có ghi log để
    chứng minh NÓ ĐÃ ĐƯỢC THỬ chứ không phải bị bỏ qua vì bug thứ tự), ứng viên 2
    probe đạt rồi exec hook; hook thoát 7 và rc phải về 7 nguyên vẹn.
    """
    if LA_WINDOWS:
        return "bo qua tren Windows (can fake bash .exe chay duoc; duong POSIX do o CI ubuntu)"
    with San() as s:
        du_an = s / "da"; (du_an / ".claude" / "hooks").mkdir(parents=True)
        (du_an / ".claude" / "hooks" / "session-start.sh").write_text(
            "echo DA_CHAY_HOOK_GLS_B1\nexit 7\n", encoding="utf-8")
        d_hong = s / "hong"; d_tot = s / "tot"
        d_hong.mkdir(); d_tot.mkdir()
        log = s / "probe.log"
        _bash_gia(d_hong, f"#!/bin/sh\necho probed >> {log}\nexit 1\n")
        _bash_gia(d_tot,
                  '#!/bin/sh\nif [ "$1" = "--version" ]; then echo fake-bash 9.9; exit 0; fi\n'
                  'exec /bin/sh "$@"\n')
        env = dict(os.environ)
        env.update({"CLAUDE_PROJECT_DIR": str(du_an),
                    "PATH": os.pathsep.join([str(d_hong), str(d_tot)]),
                    "ProgramFiles": str(s)})
        r = _chay_bridge(env)
        bang(r.returncode == 7, f"rc hook phai ve nguyen ven 7, duoc {r.returncode}: {r.stdout!r}")
        bang("DA_CHAY_HOOK_GLS_B1" in r.stdout, f"hook khong duoc chay: {r.stdout!r}")
        bang(log.is_file() and "probed" in log.read_text(encoding="utf-8"),
             "ung vien hong khong he duoc thu — thu tu resolver dang sai kieu khac")


@ca
def t126_bridge_hook_vuot_han_phai_rc124_khong_phai_treo_hay_0():
    """Quá hạn là 124 — cùng kỷ luật tách 124/125 của launcher (taskkill lesson).

    Trần đọc từ TL_HOOK_TIMEOUT_GIAY (một trong hai chỉnh sửa khai so blob gốc
    ea85526b, xem docstring bridge) — không có nó thì phản chứng này phải chờ
    600s, tức là không bao giờ được chạy thật.

    ĐÃ TRẢ GIÁ ở CI lượt 1 (job 96035756400): fixture đầu dùng `sleep 5`, mà env
    của ca này cắt PATH còn đúng thư mục fake-bash ⇒ /bin/sh không tìm thấy
    `sleep`, thoát 127 TỨC THÌ — đo nhầm cái chết khác thay vì đo timeout (đúng
    lời t120 cảnh báo). Hook fixture phải THUẦN BUILTIN: busy-wait `while :`.
    """
    if LA_WINDOWS:
        return "bo qua tren Windows (can fake bash .exe chay duoc; duong POSIX do o CI ubuntu)"
    with San() as s:
        du_an = s / "da"; (du_an / ".claude" / "hooks").mkdir(parents=True)
        (du_an / ".claude" / "hooks" / "session-start.sh").write_text(
            "while :; do :; done\n", encoding="utf-8")
        d_tot = s / "tot"; d_tot.mkdir()
        _bash_gia(d_tot,
                  '#!/bin/sh\nif [ "$1" = "--version" ]; then echo fake-bash 9.9; exit 0; fi\n'
                  'exec /bin/sh "$@"\n')
        env = dict(os.environ)
        env.update({"CLAUDE_PROJECT_DIR": str(du_an), "PATH": str(d_tot),
                    "ProgramFiles": str(s), "TL_HOOK_TIMEOUT_GIAY": "1"})
        r = _chay_bridge(env, timeout=30)
        bang(r.returncode == 124, f"qua han phai 124, duoc {r.returncode}: {r.stdout!r}")
        bang("vuot han" in r.stdout, f"thieu chan doan qua han: {r.stdout!r}")


@ca
def t127_settings_phai_noi_day_bridge_exec_form_va_khong_dung_den_PreToolUse():
    """Bridge đúng mà settings không GỌI nó thì mọi thứ trên vẫn là đồ trưng bày —
    cùng bệnh dây-nối t119. Đọc settings.json THẬT của kho.

    Đòi exec-form (`args`, không `shell`): schema hooks chính thức ghi rõ args là
    "spawned directly — no shell", placeholder thay theo từng phần tử; đó chính là
    thứ vá nguyên nhân gốc số 4 của incident. Timeout 630 CỐ Ý > trần 600 mặc định
    của bridge, để rc=124 của bridge còn tới được harness thay vì bị harness giết
    trước. PreToolUse phải GIỮ NGUYÊN shell-form cũ — packet này không đụng nó;
    vế đó là chốt phạm vi, đổi PreToolUse phải là packet khác.

    GIỚI HẠN — khai thẳng (họ t116): đặc tả lẫn bằng chứng cùng nằm trong repo;
    đổi phối hợp settings + ca này thì không chống được. Và ca này đo TỆP, không
    đo việc harness thật sự nạp tệp — thứ đó chỉ đo được bằng một phiên thật.
    """
    duong = Path(__file__).resolve().parents[1] / "settings.json"
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(duong, _duong_bridge())
    if ly_do:
        return ly_do
    j = json.loads(duong.read_text(encoding="utf-8"))
    ss = j["hooks"]["SessionStart"][0]["hooks"][0]
    bang(ss.get("type") == "command" and ss.get("command") == "python",
         f"SessionStart khong phai exec-form python: {ss!r}")
    bang(ss.get("args") == ["${CLAUDE_PROJECT_DIR}/.claude/hooks/session_start.py"],
         f"args khong tro bridge: {ss.get('args')!r}")
    bang("shell" not in ss, f"exec-form ma con truong shell: {ss!r}")
    bang(ss.get("timeout") == 630,
         f"timeout hook phai 630 (> tran 600 cua bridge): {ss.get('timeout')!r}")
    bang(_duong_bridge().is_file(), "settings tro bridge ma tep khong ton tai")
    pt = j["hooks"]["PreToolUse"][0]["hooks"][0]
    bang(pt.get("shell") == "bash" and "pretooluse_guard.py" in pt.get("command", ""),
         f"PreToolUse bi dung den — ngoai pham vi packet nay: {pt!r}")


@ca
def t128_bridge_duong_loi_khong_duoc_chet_UnicodeEncodeError_cp1258():
    """Nhánh lỗi với đường dẫn CÓ DẤU phải ra rc=12 + chẩn đoán, không phải rc=1 traceback.

    P2 của review PR #173 (comment 5341020065), ĐO THẬT chứ không suy: bridge
    thiếu ép UTF-8 thì trên console cp1258, `print` đường dẫn kiểu "Quốc hội"
    (đúng hình đường repo thật) ném UnicodeEncodeError — nhánh lỗi chết rc=1
    trước khi kịp nói mình chết vì gì. Đây là bài học ĐẦU BẢNG của launcher
    trong CLAUDE.md, và t123/t124 không bắt được vì fixture của chúng nằm ở
    %TEMP% toàn ASCII. Ca này dựng đúng cái tổ hợp đó: project dir có dấu +
    hook thiếu, và TƯỚC PYTHONUTF8/PYTHONIOENCODING của con để mặc định
    cp1258 cắn thật.

    GIỚI HẠN — khai thẳng: trên POSIX/CI ubuntu mặc định IO đã là UTF-8 nên ca
    này qua được cả khi thiếu chốt — phép đo THẬT của nó là chân Windows
    (máy dev + launcher-windows.yml, nơi vốn cố ý KHÔNG đặt hai biến ấy).
    """
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(_duong_bridge())
    if ly_do:
        return ly_do
    with San() as s:
        du_an = s / "Quốc hội thử"
        du_an.mkdir()
        env = dict(os.environ)
        for k in [k for k in env if k.upper() in ("PYTHONUTF8", "PYTHONIOENCODING")]:
            del env[k]
        env["CLAUDE_PROJECT_DIR"] = str(du_an)
        r = _chay_bridge(env)
        bang("Traceback" not in (r.stderr or ""),
             f"duong loi chet UnicodeEncodeError thay vi chan doan: {r.stderr[:200]!r}")
        bang(r.returncode == 12, f"mong 12, duoc {r.returncode}")
        bang("khong thay hook" in r.stdout, f"thieu chan doan: {r.stdout!r}")


# ------------------------------------------------ PLAT-M3 (#185): doctor chớp 12→0
#
# Nguồn chớp đo được (ops/NO_KY_THUAT.md): một lượt probe (`--version` hoặc auth)
# HẾT HẠN dưới churn tiến trình bị đếm là THIẾU công cụ ⇒ `doctor` thoát 12, rồi
# hai phút sau lại 0 — và `t53` là nơi nó lộ ra. Nhóm ca này khoá cả ba tầng vá:
# phát hiện (cờ kiểu `qua_han`), phân loại (chưa-đo-được ≠ thiếu), và chiều ngược
# (hỏng thật vẫn đỏ). Fixture theo mẫu t105/t112: nạp module tươi + thay bảng.


def _san_doctor_mot_cong_cu(m, co_xac_thuc=False):
    """Doctor thu nhỏ: một công cụ bắt buộc tên `cham`, không đụng máy thật."""
    muc = {"ten": "cham", "bat_buoc": True, "ung_vien": ["cham"],
           "vi_sao": "thu", "cai": {"*": "cai cham"}}
    if co_xac_thuc:
        muc["xac_thuc"] = ["auth", "status"]
    m.CONG_CU = [muc]
    m.MODULE_PY = []
    m.KHA_NANG = []                 # xem chú thích ở t105: tránh sinh `gh` thật
    m._doc_moi_truong = lambda: (
        {"PATH": "P", "TL_LAUNCHER_ENV_DA_DOC": "1"}, {"da_doc_truoc_cong_cu": True})
    m._cac_duong_dan = lambda _c, _e: [("cham", "/gia/cham")]


def _doctor_json(m, doi_kha_dung=False):
    a = type("A", (), {"json": True, "workspace": None,
                       "doi_kha_dung": doi_kha_dung})()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = m.lenh_doctor(a)
    return rc, json.loads(out.getvalue())


@ca
def t129_probe_qua_han_la_CHUA_DO_khong_phai_THIEU():
    """Nguồn chớp của chính `t53` — vá phải tất định, và đây là chốt giữ bản vá.

    Ba vế: (a) quá hạn CẢ HAI lượt ⇒ `chua_do_bat_buoc` + `chua_do_duoc`, KHÔNG
    vào `thieu_bat_buoc`, mã thoát mặc định 0 — hết đường 12-rồi-0; (b) phải
    probe ĐÚNG hai lời gọi (một lượt + một retry, không phải một, không phải N);
    (c) `--doi-kha-dung` vẫn fail-closed: chưa đo được thì 13, không lặng lẽ 0.
    """
    m = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m)
    goi = []
    m._phien_ban = lambda *_a, **_k: (
        goi.append(1) or (False, "timeout sau 0.1s", True))
    rc, d = _doctor_json(m)
    bang(d["mo_dun_python"] == [],
         f"fixture MODULE_PY khong cach ly module interpreter that: {d['mo_dun_python']}")
    bang(rc == MA_OK and d["thieu_bat_buoc"] == [],
         f"qua han van bi dem la THIEU: rc={rc}, thieu={d['thieu_bat_buoc']}")
    bang(d.get("chua_do_bat_buoc") == ["cham"],
         f"qua han khong duoc khai chua-do: {d.get('chua_do_bat_buoc')}")
    muc = [x for x in d["cong_cu"] if x["ten"] == "cham"][0]
    bang("chua_do_duoc" in muc and "QUA HAN" in muc["chua_do_duoc"]["ly_do"],
         f"JSON cua luot hong phai tu neu thu pham: {muc}")
    bang("co_mat_nhung_khong_chay_duoc" not in muc,
         f"qua han bi dan nhan CONG CU HONG: {muc}")
    bang(len(goi) == 2, f"phai probe dung 2 luot (1 + 1 retry), duoc {len(goi)}")
    bang(d["ok_kha_dung"] is False, "chua do duoc ma ok_kha_dung van True")

    goi.clear()
    rc2, _d2 = _doctor_json(m, doi_kha_dung=True)
    bang(rc2 == MA_CHUA_XAC_THUC,
         f"--doi-kha-dung phai chan cong cu CHUA DO DUOC, duoc rc={rc2}")


@ca
def t130_qua_han_luot_dau_retry_thanh_cong_van_la_CO():
    """Chính là ca "doctor 12 rồi 0" thu nhỏ: chớp MỘT lượt rồi hết.

    Không có retry thì một cú nghẽn nhất thời (khởi động nguội dưới tải — đúng
    chữ ký `timeout sau 8.0s` đã dựng lại được) đưa công cụ vào chưa-đo-được:
    đúng nhưng kém. Retry hạn gấp đôi biến kết luận thành CÓ, tất định với churn
    nhất thời — và đây là ca giết đột biến "bỏ retry".
    """
    m = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m)
    goi = []

    def pb(_d, **_k):
        goi.append(_k.get("timeout"))
        if len(goi) == 1:
            return (False, "timeout sau 0.1s", True)
        return (True, "cham 9.9", False)

    m._phien_ban = pb
    rc, d = _doctor_json(m)
    muc = [x for x in d["cong_cu"] if x["ten"] == "cham"][0]
    bang(rc == MA_OK and muc["co"] is True and muc.get("phien_ban") == "cham 9.9",
         f"retry thanh cong ma khong duoc tinh la CO: rc={rc}, muc={muc}")
    bang(d["thieu_bat_buoc"] == [] and d.get("chua_do_bat_buoc") == [],
         f"retry thanh cong ma van bi liet ke: {d['thieu_bat_buoc']}, "
         f"{d.get('chua_do_bat_buoc')}")
    bang(len(goi) == 2, f"phai probe dung 2 luot, duoc {len(goi)}")
    # Hệ số GẤP ĐÔI là tầng thiết kế đã khai (lặp cùng hạn là tung lại đồng xu) —
    # finding `han-gap-doi-khong-ghim` (review vòng 1): tham số chưa ai ghim thì
    # refactor sau sẽ lặng lẽ đánh rơi. Khẳng định QUAN HỆ giữa hai lượt, không
    # khẳng định số tuyệt đối (PROBE_TIMEOUT khác nhau theo nền).
    bang(goi[0] and goi[1] and abs(goi[1] - 2 * goi[0]) < 1e-6,
         f"luot retry phai duoc han GAP DOI luot 1: {goi}")


@ca
def t131_hong_that_khong_phai_qua_han_van_la_THIEU():
    """Chiều ngược của t129 — chốt chống NỚI QUÁ TAY.

    Tách "quá hạn" khỏi "thiếu" chỉ hợp lệ khi hỏng THẬT (rc != 0, Access denied,
    tệp rỗng) vẫn thoát 12 — không thì bản vá flake thành cửa fail-open cho đúng
    lớp lỗi mà t54/t60 canh. Kèm chốt: hỏng thật KHÔNG được retry — retry chỉ
    dành cho quá hạn, phép đo đã hoàn tất thì đo lại là vô nghĩa.
    """
    m = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m)
    goi = []
    m._phien_ban = lambda *_a, **_k: (
        goi.append(1) or (False, "Access denied", False))
    rc, d = _doctor_json(m)
    bang(rc == MA_THIEU_CONG_CU and d["thieu_bat_buoc"] == ["cham"],
         f"hong that ma khong con la THIEU: rc={rc}, thieu={d['thieu_bat_buoc']}")
    muc = [x for x in d["cong_cu"] if x["ten"] == "cham"][0]
    bang("co_mat_nhung_khong_chay_duoc" in muc and "chua_do_duoc" not in muc,
         f"hong that bi dan nhan chua-do: {muc}")
    bang(len(goi) == 1, f"hong that ma van retry ({len(goi)} luot)")


@ca
def t132_xac_thuc_qua_han_la_CHUA_DO_khong_phai_THIEU():
    """Đường chớp THỨ HAI của `t53`: probe auth cũng gọi CLI chậm.

    Trước vá, auth quá hạn rơi thẳng vào `xac_thuc_ok is False` ⇒ `thieu_bat_buoc`
    ⇒ thoát 12 — y hệt đường `--version`. Hai vế trên CÙNG fixture: (a) quá hạn
    cả hai lượt ⇒ chưa-đo-được, `xac_thuc_ok` là None kèm lý do; (b) auth hỏng
    THẬT vẫn là THIẾU (t105 canh end-to-end, nhắc lại đây cho cặp nằm cạnh nhau).
    """
    m = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m, co_xac_thuc=True)
    m._phien_ban = lambda *_a, **_k: (True, "gia 1", False)
    goi = []
    m._xac_thuc_kem_dau_ra = lambda *_a, **_k: (
        goi.append(_k.get("timeout")) or
        (False, "probe xac thuc timeout sau 0.1s", True, ""))
    rc, d = _doctor_json(m)
    bang(rc == MA_OK and d["thieu_bat_buoc"] == [],
         f"auth qua han van thanh THIEU: rc={rc}, thieu={d['thieu_bat_buoc']}")
    bang(d.get("chua_do_bat_buoc") == ["cham"],
         f"auth qua han khong duoc khai chua-do: {d.get('chua_do_bat_buoc')}")
    muc = [x for x in d["cong_cu"] if x["ten"] == "cham"][0]
    bang(muc.get("xac_thuc_ok") is None and "QUA HAN" in muc.get("loi_xac_thuc", ""),
         f"None != False: qua han phai la CHUA DO kem ly do: {muc}")
    bang(len(goi) == 2, f"auth phai probe dung 2 luot, duoc {len(goi)}")
    # Cùng finding `han-gap-doi-khong-ghim` — phủ luôn phía auth (xem t130).
    bang(goi[0] and goi[1] and abs(goi[1] - 2 * goi[0]) < 1e-6,
         f"retry auth phai duoc han GAP DOI luot 1: {goi}")

    m._xac_thuc_kem_dau_ra = lambda *_a, **_k: (False, "rc=1", False, "")
    rc2, d2 = _doctor_json(m)
    bang(rc2 == MA_THIEU_CONG_CU and d2["thieu_bat_buoc"] == ["cham"],
         f"auth hong THAT phai van la THIEU: rc={rc2}, thieu={d2['thieu_bat_buoc']}")


@ca
def t133_do_codex_spawn_bang_duong_dan_da_resolve_khong_ten_tran():
    """ĐO 19-08-2026 trên Windows (PLAT-M3/#185): cùng MỘT lượt `doctor`, bảng
    CONG_CU ra `codex-cli 0.146.0` còn KHA_NANG báo `KHONG_DO_DUOC:
    FileNotFoundError` — vì `shutil.which` thấy `...\\nodejs\\codex.CMD` (tra
    PATHEXT) nhưng CreateProcessW với tên trần "codex" chỉ tự thêm ".exe".
    Chốt: MỌI spawn codex (cả `_do_codex` lẫn cửa `_do_codex_song`) phải đi bằng
    đường dẫn `which` đã trả — hai cửa, hai đột biến riêng.
    """
    m = _tai_launcher_thu()
    m._dang_cho_snapshot = lambda home: False  # Recovery is measured by g2 dedicated cases.
    m._codex_home_hieu_luc = lambda: Path("INERT-HOME")
    goi = []
    m.shutil.which = lambda t: "/gia/codex.cmd" if t == "codex" else None
    m._co_chan_codex = lambda: None

    class PLoi:
        returncode, stdout, stderr = 1, "", "Not logged in"

    m.subprocess.run = lambda cmd, **_k: (goi.append(list(cmd)) or PLoi())
    tt, _mo_ta = m._do_codex()
    bang(tt in ("CHUA_XAC_THUC", "CAN_CHUAN_BI"), f"fixture lech: {tt}")
    bang(goi and goi[0][0] == "/gia/codex.cmd",
         f"_do_codex van spawn ten tran: {goi[:1]}")

    # Hai CALL-SITE kiểm sống trong `_do_codex` cũng phải truyền đúng đường đã
    # resolve: nhánh bình thường và nhánh cảnh báo sắp hết hạn là hai cửa riêng.
    class POk:
        returncode, stdout, stderr = 0, "Logged in using ChatGPT", ""

    m.subprocess.run = lambda cmd, **_k: (goi.append(list(cmd)) or POk())
    do_codex_song_goc = m._do_codex_song
    goi_song = []

    def do_song_gia(*_a, **kw):
        goi_song.append(kw.get("duong_dan"))
        return (True, "ok")

    m._do_codex_song = do_song_gia
    m._han_token_codex = lambda: {
        "gio_con_lai": {}, "last_refresh": None, "tuoi_anh_chup_gio": None}
    tt, _mo_ta = m._do_codex(kiem_song=True)
    bang(tt == "DUNG_DUOC" and goi_song == ["/gia/codex.cmd"],
         f"call-site kiem-song binh thuong khong truyen duong resolve: {tt}, {goi_song}")

    goi_song.clear()
    m._han_token_codex = lambda: {
        "gio_con_lai": {"access_token": 1.0},
        "last_refresh": None, "tuoi_anh_chup_gio": None}
    tt, _mo_ta = m._do_codex(kiem_song=True)
    bang(tt == "SAP_HET_HAN" and goi_song == ["/gia/codex.cmd"],
         f"call-site kiem-song sap-het-han khong truyen duong resolve: {tt}, {goi_song}")

    m._do_codex_song = do_codex_song_goc
    goi.clear()
    m.subprocess.run = lambda cmd, **_k: (goi.append(list(cmd)) or POk())
    for kw in ({}, {"duong_dan": "/gia/codex.cmd"}):
        goi.clear()
        m._do_codex_song(**kw)
        bang(goi and goi[0][0] == "/gia/codex.cmd",
             f"_do_codex_song van spawn ten tran ({kw}): {goi[:1]}")


@ca
def t134_kiem_song_dang_bat_thi_footer_khong_khuyen_bat_lai():
    """Chân trang "chạy lại với --kiem-song" từng in trong lượt ĐÃ truyền cờ (đo
    19-08-2026) — một gợi ý sai tệ hơn không gợi ý: người đọc chạy lại vô ích rồi
    tin là đã thử. Hai chiều: cờ bật thì nói "đã chạy", cờ tắt mới được khuyên bật.
    """
    m = _tai_launcher_thu()
    m.CONG_CU = []
    m.MODULE_PY = []
    m.KHA_NANG = [{"ten": "gia", "vi_sao": "thu", "khac_phuc": "",
                   "do": lambda _ws, _ks=False: ("KHONG_DO_DUOC", "x")}]
    m._doc_moi_truong = lambda: (
        {"PATH": "P", "TL_LAUNCHER_ENV_DA_DOC": "1"}, {"da_doc_truoc_cong_cu": True})
    for kiem_song, cam, phai_co in (
            (True, "chay lai voi --kiem-song", "--kiem-song DA chay"),
            (False, "--kiem-song DA chay", "chay lai voi --kiem-song")):
        a = type("A", (), {"json": False, "workspace": None,
                           "doi_kha_dung": False, "kiem_song": kiem_song})()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            m.lenh_doctor(a)
        vb = out.getvalue()
        bang(cam not in vb,
             f"kiem_song={kiem_song}: van in cau sai: ...{vb[-160:]!r}")
        bang(phai_co in vb,
             f"kiem_song={kiem_song}: thieu cau dung: ...{vb[-160:]!r}")
        bang("MODULE PYTHON" not in vb,
             f"fixture MODULE_PY khong duoc cach ly: {vb!r}")


def _shim_thi_hanh(thu_muc: Path, ten: str, ma_python: str) -> str:
    """Executable chạy được trên CẢ HAI nền, thân là một câu python.

    Windows dùng `.cmd` — CreateProcess chạy được .cmd khi ĐUÔI tường minh, đúng
    mặt kia của cái bẫy PATHEXT mà t133 canh. POSIX dùng sh `exec` sang python:
    `exec` để không sinh cháu giữ ống stdout (cháu sống qua cú kill timeout sẽ
    ghim `communicate()` tới khi nó tự thoát — kéo dài ca test vô ích).
    """
    if LA_WINDOWS:
        t = thu_muc / f"{ten}.cmd"
        t.write_text(f'@"{PY}" -c "{ma_python}"\r\n', encoding="utf-8")
    else:
        t = thu_muc / ten
        t.write_text(f'#!/bin/sh\nexec "{PY}" -c "{ma_python}"\n', encoding="utf-8")
        t.chmod(0o755)
    return str(t)


@ca
def t135_phien_ban_va_xac_thuc_bao_qua_han_bang_CO_KIEU():
    """Tầng PHÁT HIỆN, đo bằng tiến trình THẬT chứ không fake: TimeoutExpired phải
    thành cờ `qua_han=True`, thất bại thường KHÔNG được mang cờ ấy.

    Phân loại quá hạn bằng cách dò chữ "timeout" trong mô tả là ĐOÁN, không phải
    ĐO (bài học phân loại HTTP bằng văn bản tự do) — nên cờ kiểu là hợp đồng, và
    ca này ghim nó ở cả `_phien_ban` lẫn `_xac_thuc` trên cả hai nền.
    """
    m = _tai_launcher_thu()
    with San() as s:
        ngu = _shim_thi_hanh(s, "ngu", "import time; time.sleep(3)")
        chet = _shim_thi_hanh(s, "chet", "import sys; sys.exit(7)")
        ket = m._phien_ban(ngu, timeout=0.4)
        bang(ket[0] is False and ket[2] is True,
             f"_phien_ban timeout that khong gan co qua_han: {ket}")
        ket = m._phien_ban(chet, timeout=30)
        bang(ket[0] is False and ket[2] is False,
             f"_phien_ban hong that lai mang co qua_han: {ket}")
        ket = m._xac_thuc(ngu, ["auth"], timeout=0.4)
        bang(ket[0] is False and ket[2] is True,
             f"_xac_thuc timeout that khong gan co qua_han: {ket}")
        ket = m._xac_thuc(chet, ["auth"], timeout=30)
        bang(ket[0] is False and ket[2] is False,
             f"_xac_thuc hong that lai mang co qua_han: {ket}")


@ca
def t136_qua_han_roi_hong_that_o_luot_retry_van_la_THIEU():
    """Finding `qua-han-roi-hong-that-khong-ghim` (review vòng 1, P3): chuỗi
    "QUÁ HẠN lượt 1 → lượt retry HOÀN TẤT với thất bại THẬT" phải ra THIẾU (12).

    Mã đang đúng nhưng trước ca này KHÔNG chốt nào ghim — hai đột biến của reviewer
    (nuốt điều kiện `xt_qua_han` ở kiểm tra sau retry; vứt cờ `qua_han` của lượt
    retry) đều sống sót cả suite. Nếu ai vấp phải khi refactor: thất bại ĐO ĐƯỢC ở
    lượt retry bị nuốt thành "chưa đo" ⇒ mất mã 12/13 với điều kiện thời gian —
    fail-open có tiền đề. Phủ CẢ hai phía version lẫn auth, kèm đòi thông điệp giữ
    dấu vết "luot 1 … luot 2" (JSON của lượt hỏng phải tự nêu thủ phạm).
    """
    # --- phía version: timeout lượt 1, Access denied lượt 2
    m = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m)
    goi = []

    def pb(_d, **_k):
        goi.append(1)
        if len(goi) == 1:
            return (False, "timeout sau 0.1s", True)
        return (False, "Access denied", False)

    m._phien_ban = pb
    rc, d = _doctor_json(m)
    bang(rc == MA_THIEU_CONG_CU and d["thieu_bat_buoc"] == ["cham"],
         f"hong that o luot retry ma khong la THIEU: rc={rc}, "
         f"thieu={d['thieu_bat_buoc']}, chua_do={d.get('chua_do_bat_buoc')}")
    muc = [x for x in d["cong_cu"] if x["ten"] == "cham"][0]
    hong = muc.get("co_mat_nhung_khong_chay_duoc")
    bang(hong is not None and "chua_do_duoc" not in muc,
         f"phai mang nhan HONG, khong phai chua-do: {muc}")
    bang("luot 1" in hong["loi"] and "luot 2" in hong["loi"],
         f"thong diep phai giu dau vet ca hai luot: {hong}")
    bang(len(goi) == 2, f"phai dung 2 luot probe, duoc {len(goi)}")

    # --- phía auth: timeout lượt 1, rc=1 lượt 2
    m2 = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m2, co_xac_thuc=True)
    m2._phien_ban = lambda *_a, **_k: (True, "gia 1", False)
    goi2 = []

    def xt(*_a, **_k):
        goi2.append(1)
        if len(goi2) == 1:
            return (False, "probe xac thuc timeout sau 0.1s", True, "")
        return (False, "rc=1", False, "")

    m2._xac_thuc_kem_dau_ra = xt
    rc2, d2 = _doctor_json(m2)
    bang(rc2 == MA_THIEU_CONG_CU and d2["thieu_bat_buoc"] == ["cham"],
         f"auth hong that o luot retry ma khong la THIEU: rc={rc2}, "
         f"thieu={d2['thieu_bat_buoc']}, chua_do={d2.get('chua_do_bat_buoc')}")
    muc2 = [x for x in d2["cong_cu"] if x["ten"] == "cham"][0]
    bang(muc2.get("xac_thuc_ok") is False
         and "luot 1" in muc2.get("loi_xac_thuc", "")
         and "luot 2" in muc2.get("loi_xac_thuc", ""),
         f"xac_thuc_ok phai False kem dau vet hai luot: {muc2}")
    bang(len(goi2) == 2, f"auth phai dung 2 luot probe, duoc {len(goi2)}")


@ca
def t137_ung_vien_hong_that_cong_ung_vien_qua_han_la_CHUA_DO():
    """Finding `hon-hop-ung-vien-khong-ghim` (review vòng 1, P3): công cụ có hai
    ứng viên — một HỎNG THẬT, một QUÁ HẠN cả hai lượt — thì kết luận là CHƯA ĐO
    ĐƯỢC, không phải THIẾU.

    Vì sao ngữ nghĩa này đúng (ghim ở đây để người sau khỏi "sửa cho gọn"): ứng
    viên chưa đo được nghĩa là tính khả dụng của CÔNG CỤ chưa chứng minh xong; xử
    ngược lại (hỏng-thật thắng) thì máy có binary hỏng đứng trước + binary chậm
    đứng sau sẽ chớp 12/0 trở lại theo giờ — đúng flake mà packet này diệt.
    JSON giữ CẢ hai dấu vết để người đọc thấy đủ hai chuyện.
    """
    m = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m)
    m._cac_duong_dan = lambda _c, _e: [("cham", "/hong/cham"), ("cham", "/treo/cham")]
    goi = {"/hong/cham": 0, "/treo/cham": 0}

    def pb(duong, **_k):
        goi[duong] += 1
        if duong == "/hong/cham":
            return (False, "Access denied", False)
        return (False, "timeout sau 0.1s", True)

    m._phien_ban = pb
    rc, d = _doctor_json(m)
    bang(rc == MA_OK and d["thieu_bat_buoc"] == []
         and d.get("chua_do_bat_buoc") == ["cham"],
         f"hon hop phai la CHUA DO: rc={rc}, thieu={d['thieu_bat_buoc']}, "
         f"chua_do={d.get('chua_do_bat_buoc')}")
    muc = [x for x in d["cong_cu"] if x["ten"] == "cham"][0]
    bang("co_mat_nhung_khong_chay_duoc" in muc and "chua_do_duoc" in muc,
         f"JSON phai giu CA HAI dau vet: {muc}")
    bang(goi == {"/hong/cham": 1, "/treo/cham": 2},
         f"hong that khong retry, qua han retry dung 1 luot: {goi}")


@ca
def t138_auth_het_ngan_sach_phai_vao_CHUA_DO():
    """Cạn trần giữa version và auth không được lặng lẽ thành đủ khả dụng."""
    m = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m, co_xac_thuc=True)
    m._tran_doctor = lambda: 10.0
    m._phien_ban = lambda *_a, **_k: (True, "gia 1", False)
    goi_auth = []
    m._xac_thuc_kem_dau_ra = lambda *_a, **_k: (goi_auth.append(1) or (True, "ok", False, "ok\n"))
    moc = iter([0.0, 1.0])
    monotonic_goc = m.time.monotonic
    try:
        m.time.monotonic = lambda: next(moc, 99999.0)
        rc, d = _doctor_json(m, doi_kha_dung=True)
    finally:
        m.time.monotonic = monotonic_goc
    muc = [x for x in d["cong_cu"] if x["ten"] == "cham"][0]
    bang(not goi_auth, f"het ngan sach ma van goi auth: {goi_auth}")
    bang(rc == MA_CHUA_XAC_THUC and d.get("chua_do_bat_buoc") == ["cham"],
         f"auth chua do ma khong fail-closed: rc={rc}, d={d}")
    bang(muc.get("xac_thuc_ok") is None
         and "het ngan sach" in muc.get("loi_xac_thuc", ""),
         f"auth het ngan sach thieu dau CHUA DO: {muc}")
    bang(d["ok_kha_dung"] is False, "auth chua do ma ok_kha_dung van True")


@ca
def t139_ung_vien_qua_han_khong_duoc_che_ung_vien_tot():
    """Ứng viên treo được retry rồi phải nhường đường cho binary tốt đứng sau."""
    m = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m)
    m._cac_duong_dan = lambda _c, _e: [
        ("cham", "/treo/cham"), ("cham", "/tot/cham")]
    goi = []

    def pb(duong, **_k):
        goi.append(duong)
        if duong == "/treo/cham":
            return (False, "timeout sau 0.1s", True)
        return (True, "cham 9.9", False)

    m._phien_ban = pb
    rc, d = _doctor_json(m)
    muc = [x for x in d["cong_cu"] if x["ten"] == "cham"][0]
    bang(rc == MA_OK and muc["co"] is True and muc.get("phien_ban") == "cham 9.9",
         f"ung vien treo che binary tot: rc={rc}, muc={muc}")
    bang(d.get("chua_do_bat_buoc") == [], f"da co binary tot ma van CHUA DO: {d}")
    bang(goi == ["/treo/cham", "/treo/cham", "/tot/cham"],
         f"phai retry treo dung mot luot roi di tiep: {goi}")


@ca
def t140_doctor_text_tach_CHUA_DO_khoi_THIEU_va_DU():
    """Formatter text phải giữ trạng thái thứ ba và lý do của cả version lẫn auth."""
    def doctor_text(m):
        a = type("A", (), {"json": False, "workspace": None,
                            "doi_kha_dung": False, "kiem_song": False})()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = m.lenh_doctor(a)
        return rc, out.getvalue()

    m = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m)
    m._phien_ban = lambda *_a, **_k: (False, "timeout sau 0.1s", True)
    rc, vb = doctor_text(m)
    bang(rc == MA_OK and re.search(r"^\s+CHUA_DO\s+cham\s+.*QUA HAN", vb, re.M),
         f"version qua han khong mang nhan/ly do CHUA_DO: rc={rc}, vb={vb!r}")
    bang("THIEU cham" not in vb and "cai bang: cai cham" not in vb,
         f"version CHUA DO bi in thanh THIEU/goi cai: {vb!r}")
    bang("CHUA DO DUOC (het ngan sach" not in vb
         and "KET LUAN  : CHUA DO DUOC cham" in vb,
         f"footer khoa cung nguyen nhan hoac ket luan DU: {vb!r}")

    m2 = _tai_launcher_thu()
    _san_doctor_mot_cong_cu(m2, co_xac_thuc=True)
    m2._phien_ban = lambda *_a, **_k: (True, "gia 1", False)
    m2._xac_thuc_kem_dau_ra = lambda *_a, **_k: (
        False, "probe xac thuc timeout sau 0.1s", True, "")
    rc2, vb2 = doctor_text(m2)
    bang(rc2 == MA_OK and re.search(r"^\s+CHUA_DO\s+cham\s+.*xac thuc", vb2, re.M),
         f"auth qua han khong mang nhan/ly do CHUA_DO: rc={rc2}, vb={vb2!r}")
    bang("xac thuc CHUA DO:" in vb2 and "KET LUAN  : DU" not in vb2,
         f"auth None bi gop thanh co/DU hoac mat ly do: {vb2!r}")


@ca
def t141_comment_timeout_phai_co_version_nguon_va_phep_do():
    """Chú thích quyết định phải theo idiom version + nguồn + số đo của kho."""
    ma = LAUNCHER_DANG_DUNG.read_text(encoding="utf-8")
    bang("v1.3.0 (#185 + phép đo 12→0) — nguồn chớp của `t53`; vá tất định." in ma,
         "comment timeout mat version, nguon #185 hoac phep do 12→0")


@ca
def t142_ban_sao_roi_chi_duoc_tha_khi_goc_vang_git():
    """Thiếu fixture trong checkout thật phải ĐỎ; bản sao rời mới được tự khai bỏ qua."""
    with San() as s:
        kho = s / "kho"; kho.mkdir(); (kho / ".git").mkdir()
        roi = s / "roi"; roi.mkdir()
        thieu = s / "khong-co-fixture"
        bang(_bo_qua_neu_ban_sao_roi_thieu(thieu, goc_kho=kho) is None,
             "cay co .git ma van duoc tha fixture thieu")
        ly_do = _bo_qua_neu_ban_sao_roi_thieu(thieu, goc_kho=roi)
        bang(isinstance(ly_do, str) and "ban sao roi" in ly_do and ".git" in ly_do,
             f"ban sao roi khong tu khai ly do bo qua: {ly_do!r}")


@ca
def t101_phan_tich_doi_so_phai_do_NGAY_khong_doi_chay_het_suite():
    """Công cụ chẩn đoán dễ xanh giả thì tệ hơn không có.

    Cross-review lượt 8 (LOW) đếm bốn tổ hợp của bộ phân tích tay cũ; ca này khoá cả
    bốn. Nặng nhất là `--nhat-ky --dot-bien`: nó chạy mutation, rc=0, và KHÔNG tạo
    nhật ký — người dùng tin là đã có nhật ký trong khi không có gì.
    """
    def do_loi(argv):
        cu = sys.stderr
        sys.stderr = io.StringIO()
        try:
            phan_tich_doi_so(argv)
            return None                       # khong loi
        except SystemExit as e:
            return e.code
        finally:
            sys.stderr = cu

    # (a) --nhat-ky THIEU duong dan => do NGAY, khong chay gi
    bang(do_loi(["--nhat-ky"]) == 2, "--nhat-ky thieu duong dan ma khong do ngay")
    # (b) --nhat-ky kem --dot-bien => TU CHOI, khong duoc im lang nuot
    bang(do_loi(["--nhat-ky", "/tmp/x", "--dot-bien"]) == 2,
         "--nhat-ky + --dot-bien phai bi tu choi")
    bang(do_loi(["--dot-bien", "--nhat-ky", "/tmp/x"]) == 2, "thu tu nguoc lai cung phai do")
    # (c) --moi-truong khong duoc lo di --nhat-ky
    bang(do_loi(["--moi-truong", "--nhat-ky", "/tmp/x"]) == 2,
         "--moi-truong nuot --nhat-ky trong im lang")
    # (d) hai che do cung luc => loai tru nhau
    bang(do_loi(["--dot-bien", "--moi-truong"]) == 2, "hai che do cung luc ma khong do")
    # (d2) CO LAP — argparse mac dinh NHAN va lang le lay gia tri cuoi
    bang(do_loi(["--nhat-ky", "/tmp/a", "--nhat-ky", "/tmp/b"]) == 2,
         "--nhat-ky lap ma khong do: im lang lay /tmp/b trong khi nguoi go tuong /tmp/a")
    bang(do_loi(["--dot-bien", "--dot-bien"]) == 2, "--dot-bien lap ma khong do")
    bang(do_loi(["--moi-truong", "--moi-truong"]) == 2, "--moi-truong lap ma khong do")

    # (g) --lap-ca: che do rieng, loai tru voi hai che do kia; --lan chi co nghia kem no
    bang(do_loi(["--lap-ca", "t72", "--dot-bien"]) == 2, "--lap-ca + --dot-bien ma khong do")
    bang(do_loi(["--lan", "5"]) == 2, "--lan mot minh ma khong do")
    bang(do_loi(["--lap-ca", "t72", "--lan", "0"]) == 2, "--lan 0 ma khong do")
    bang(do_loi(["--lap-ca", "t72", "--lan", "5", "--nhat-ky", "/tmp/x"]) is None,
         "--lap-ca kem --nhat-ky la to hop HOP LE ma bi chan")
    a = phan_tich_doi_so(["--lap-ca", "t72", "--lan", "5"])
    bang(a.lap_ca == "t72" and a.lan == 5, f"phan tich sai: {a.lap_ca!r} {a.lan}")
    # (e) co la / viet tat => tu choi, khong tu doan
    bang(do_loi(["--khong-co-co-nay"]) == 2, "co la ma khong do")
    bang(do_loi(["--dot"]) == 2, "viet tat --dot tu no thanh --dot-bien (allow_abbrev)")
    # (f) cac to hop HOP LE phai qua, keo chot thanh chan oan
    for argv, kiem in ((["--dot-bien"], lambda a: a.dot_bien),
                       (["--moi-truong"], lambda a: a.moi_truong),
                       ([], lambda a: not a.dot_bien and not a.moi_truong and not a.nhat_ky),
                       (["--nhat-ky", "/tmp/x"], lambda a: a.nhat_ky == "/tmp/x")):
        bang(do_loi(argv) is None, f"to hop hop le {argv} bi chan oan")
        bang(kiem(phan_tich_doi_so(argv)), f"phan tich sai gia tri cho {argv}")


@ca
def t102_khong_go_duoc_policy_thi_phai_CHAN_codex():
    """Từ chối mà vẫn để codex chạy là fail-open — lỗi của chính bản vá lượt trước.

    Cross-review lượt 8 (HIGH): hook bắt rc=3 rồi chỉ in `CANH BAO` và đi tiếp. Đúng
    lúc phát hiện config nguy hiểm mà không gỡ được thì khối `inherit = "all"` cũ VẪN
    CÒN HIỆU LỰC — tức mọi lệnh con của codex nhận toàn bộ môi trường. Reviewer gọi
    đúng tên: biến một lỗi xác-định-an-toàn thành phơi môi trường CÓ CHỦ ĐÍCH.

    Ca này khoá ba vế: (1) từ chối thì PHẢI đặt cờ chặn · (2) `_do_codex` thấy cờ thì
    hạ codex xuống `CHUA_XAC_THUC` TRƯỚC mọi phép đo khác, kể cả khi credential hoàn
    hảo · (3) dọn xong thì cờ PHẢI tự hết — cờ không tự hết là chốt đỏ thường trực.
    """
    cs = _nap_sach(CODEX_ENV_POLICY)
    m = _tai_launcher_thu()
    m._dang_cho_snapshot = lambda home: False  # Recovery is measured by g2 dedicated cases.
    m._codex_home_hieu_luc = lambda: Path("INERT-HOME")
    bang(m.CO_CHAN_CODEX == cs.TEN_CO_CHAN,
         f"hai tep lech ten co chan: {m.CO_CHAN_CODEX!r} vs {cs.TEN_CO_CHAN!r} — "
         f"lech la chot an ninh IM LANG bien mat")

    def chay(tep, co):
        cu_out, cu_err = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = io.StringIO()
        try:
            return cs.main(["--tep", str(tep), "--co-chan", str(co)])
        finally:
            sys.stdout, sys.stderr = cu_out, cu_err

    with San() as s:
        co = s / cs.TEN_CO_CHAN
        # (1) TU CHOI => dat co
        xau = s / "hong.toml"
        xau.write_bytes(cs.MOC_MO + b"\n[shell_environment_policy]\n")
        bang(chay(xau, co) == cs.MA_CON_KHOI, "marker le ma khong bao dong")
        bang(co.exists(), "TU CHOI ma KHONG dat co chan — codex van chay tu do")
        bang("inherit" in co.read_text(encoding="utf-8"),
             "co chan khong noi ro nguy co, nguoi doc khong biet vi sao bi chan")

        # (2) `_do_codex` thay co => CHUA_XAC_THUC, TRUOC moi phep do khac
        # Gia lap mot codex XAC THUC HOAN HAO: neu chot co chan bi go, ham se tra
        # CO_CREDENTIAL va ca nay do bang MOT KHANG DINH SACH — khong phai bang crash.
        goi = []

        class PhienBanTot:
            returncode = 0
            stdout = "Logged in using ChatGPT\n"
            stderr = ""

        m.shutil.which = lambda t: "/usr/bin/codex" if t == "codex" else None
        m.subprocess.run = lambda *_a, **_k: (goi.append(1), PhienBanTot())[1]
        m._han_token_codex = lambda: {"doc_duoc": True, "last_refresh": "x",
                                      "gio_con_lai": {"access_token": 100.0}}
        policy_home = s / "policy-home"
        policy_home.mkdir()
        m._codex_home_hieu_luc = lambda: policy_home
        (policy_home / cs.TEN_CO_CHAN).write_text("x", encoding="utf-8")
        try:
            tt, mo_ta = m._do_codex()
            bang(tt == "CHUA_XAC_THUC", f"co co chan ma van bao {tt}")
            bang("BI CHAN" in mo_ta, f"khong noi ro la bi chan: {mo_ta!r}")
            bang(not goi, "da goi `codex login status` roi moi xet co — phai chan TRUOC")

            # CUA THU HAI: `_do_codex_song` la duong THAT SU chay `codex exec`. Luot 9
            # bat dung chuyen ban truoc chi cho `_do_codex` doc co, nen cua nay di
            # thang qua. Mot chot ma chi mot trong hai cua doc thi khong phai chot.
            song, ly_do = m._do_codex_song()
            bang(song is False, "co co chan ma _do_codex_song van bao SONG")
            bang("BI CHAN" in ly_do, f"_do_codex_song khong noi ro bi chan: {ly_do!r}")
            bang(not goi, "_do_codex_song da chay codex THAT du dang bi chan")
        finally:
            (policy_home / cs.TEN_CO_CHAN).unlink()

        # (3) don xong => co PHAI tu het
        sach = s / "sach.toml"
        sach.write_bytes(b'[projects."/a"]\ntrust_level = "trusted"\n')
        bang(chay(sach, co) == cs.MA_OK, "config sach ma bao loi")
        bang(not co.exists(), "da sach ma co chan con nguyen — chot do thuong truc")


@ca
def t100_cong_cu_policy_KHONG_BAO_GIO_duoc_ghi_vao_config():
    """Hợp đồng MỚI (16-08-2026): công cụ không ghi vào config của người dùng, chấm hết.

    BỐN lượt cross-review, BẢY phát hiện, tất cả cùng một đường — việc TỰ ĐỘNG ghi lại
    config: bảng TOML trùng tên · khớp substring mất dữ liệu · `write_text` không nguyên
    tử · kiểm từng dòng vẫn mất dữ liệu · symlink tên tạm ghi đè tệp khác · CRLF đổi kết
    thúc dòng toàn tệp · lost-update. Bảy lần cùng một hình dạng thì lỗi nằm ở QUYẾT ĐỊNH
    GỐC. Nay: mặc định CHỈ ĐỌC; `--go` dựng bản đã gỡ ra tệp BÊN CẠNH; bản gốc bất khả xâm.

    Ca này khoá đúng câu đó, và cách khoá mạnh nhất là ĐO BYTE: trước và sau mọi lệnh,
    tệp gốc phải giống nhau TỪNG BYTE — không phải "vẫn parse được", vì "parse được" là
    đúng phép kiểm đã mù trước ca mất dữ liệu ở lượt 8.
    """
    m = _nap_sach(CODEX_ENV_POLICY)
    khoi = m.MOC_MO + b"\n" + m._THAN_KHOI_CU[0] + b"\n" + m.MOC_DONG
    duoi = b'[projects."/home/u/kho"]\ntrust_level = "trusted"\n'

    def chay(tep, co, go=False):
        doi = ["--tep", str(tep), "--co-chan", str(co)] + (["--go"] if go else [])
        cu_out, cu_err = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = io.StringIO()
        try:
            return m.main(doi)
        finally:
            sys.stdout, sys.stderr = cu_out, cu_err

    with San() as s:
        co = s / m.TEN_CO_CHAN

        # (a) CON KHOI: bao dong, dat co, va TUYET DOI khong dung config
        t1 = s / "c1.toml"
        goc = khoi + b"\n\n" + duoi
        t1.write_bytes(goc)
        bang(chay(t1, co) == m.MA_CON_KHOI, "con khoi ma khong bao dong")
        bang(t1.read_bytes() == goc, "DA GHI VAO CONFIG o che do chi doc")
        bang(co.exists(), "con khoi ma khong dat co chan")

        # (b) --go: dung ban BEN CANH, ban goc VAN nguyen tung byte
        bang(chay(t1, co, go=True) == MA_OK, "--go that bai")
        bang(t1.read_bytes() == goc, "--go DA SUA ban goc")
        ben_canh = s / ("c1.toml" + m.DUOI_DA_GO)
        bang(ben_canh.exists(), "khong dung ra ban da go")
        bang(m.MOC_MO not in ben_canh.read_bytes(), "ban da go van con khoi")
        bang(duoi in ben_canh.read_bytes(), "ban da go nuot phan cua nguoi dung")

        # (c) chay --go lan hai: tep da ton tai => TU CHOI, khong ghi de
        ben_canh.write_bytes(b"NGUOI DUNG DA SUA\n")
        bang(chay(t1, co, go=True) == m.MA_CON_KHOI, "ghi de ban da go co san")
        bang(ben_canh.read_bytes() == b"NGUOI DUNG DA SUA\n", "DA GHI DE ban da go")

        # (d) CRLF: phan NGOAI khoi phai ra dung tung byte (phan chung luot 10)
        t2 = s / "c2.toml"
        than_crlf = m._THAN_KHOI_CU[0].replace(b"\n", b"\r\n")
        goc2 = (m.MOC_MO + b"\r\n" + than_crlf + b"\r\n" + m.MOC_DONG + b"\r\n\r\n"
                + b'[user]\r\nname = "giu-nguyen"\r\n')
        t2.write_bytes(goc2)
        bang(chay(t2, co, go=True) == MA_OK, "khoi CRLF ma khong nhan ra")
        ra = (s / ("c2.toml" + m.DUOI_DA_GO)).read_bytes()
        bang(ra == b'[user]\r\nname = "giu-nguyen"\r\n',
             f"CRLF cua nguoi dung bi doi: {ra!r}")

        # (e) BOM: nhan, va GIU. Luot 10 ghi BOM dang bi tu choi oan.
        t3 = s / "c3.toml"
        t3.write_bytes(m.BOM + khoi + b"\n\n" + duoi)
        bang(chay(t3, co, go=True) == MA_OK, "BOM van bi tu choi oan")
        ra3 = (s / ("c3.toml" + m.DUOI_DA_GO)).read_bytes()
        bang(ra3 == m.BOM + duoi, f"mat BOM cua nguoi dung: {ra3[:8]!r}")

        # (f) KHOI DA BI SUA / marker hong => KHONG PHAN LOAI, dat co, khong dung tep
        for ten, noi in (
            ("gia_tri_khac", m.MOC_MO + b'\n[shell_environment_policy]\ninherit = "core"\n' + m.MOC_DONG),
            ("dao_thu_tu", m.MOC_MO + b'\ninherit = "all"\n[shell_environment_policy]\n' + m.MOC_DONG),
            ("marker_giua_dong", b"x = 1 # " + m.MOC_MO + b"\ny = 2\nz = 3 # " + m.MOC_DONG),
            ("chi_mot_dau", m.MOC_MO + b"\n[shell_environment_policy]\n"),
            ("chong_khoi", khoi + b"\n" + khoi),
            ("trong_chuoi_toml", b'ghi_chu = """\n' + m.MOC_MO + b"\nnoi dung\n" + m.MOC_DONG + b'\n"""\n'),
        ):
            t = s / f"{ten}.toml"
            t.write_bytes(noi)
            bang(chay(t, co, go=True) == m.MA_CON_KHOI, f"{ten}: khong phan loai duoc ma van lam")
            bang(t.read_bytes() == noi, f"{ten}: DA SUA config")
            bang(not (s / f"{ten}.toml{m.DUOI_DA_GO}").exists(),
                 f"{ten}: da dung ban da go tu mot khoi KHONG phai cua ta")

        # (g) SACH => rc 0 va co chan TU HET (co khong tu het la chot do thuong truc)
        t4 = s / "c4.toml"
        t4.write_bytes(duoi)
        bang(chay(t4, co) == MA_OK, "config sach ma bao dong")
        bang(not co.exists(), "da sach ma co chan con nguyen")
        bang(t4.read_bytes() == duoi, "config sach ma van bi dung toi")

        # (h) khong co tep => khong tu tao
        t5 = s / "khong-co.toml"
        bang(chay(t5, co, go=True) == MA_OK, "thieu tep ma bao loi")
        bang(not t5.exists(), "da TU TAO config khong can thiet")

        # (i) KHONG con duong nao GHI VAO config: quet AST, khong quet chuoi.
        # Luot 10 ha dung phep quet chuoi cu: no chi la lexical. Nay hoi CAY CU PHAP —
        # trong ca tep khong duoc con loi goi ghi nao nham vao `tep` (ban goc).
        # Hoi CHINH XAC: co loi goi ghi nao NHAM VAO `tep` (ban goc) khong. Quet mu ca
        # tep se do oan — `co_chan.write_text` la ghi CO CHAN CUA TA, con
        # `.replace(b"\\r\\n", ...)` la phuong thuc cua bytes, khong dinh gi toi tep.
        cay = ast.parse(CODEX_ENV_POLICY.read_text(encoding="utf-8"))
        ghi = {"write_text", "write_bytes", "open", "unlink", "touch", "chmod", "rename"}
        thay = {"replace", "rename", "remove", "unlink", "truncate", "chmod"}
        pham = []
        for nut in ast.walk(cay):
            if not isinstance(nut, ast.Call) or not isinstance(nut.func, ast.Attribute):
                continue
            nhan = nut.func.value
            # (1) tep.write_*(...) / tep.open(...) ...
            if isinstance(nhan, ast.Name) and nhan.id == "tep" and nut.func.attr in ghi:
                pham.append(f"tep.{nut.func.attr}@dong{nut.lineno}")
            # (2) os.replace(..., tep) / os.chmod(tep, ...) ...
            if (isinstance(nhan, ast.Name) and nhan.id == "os" and nut.func.attr in thay
                    and any(isinstance(x, ast.Name) and x.id == "tep" for x in nut.args)):
                pham.append(f"os.{nut.func.attr}(tep)@dong{nut.lineno}")
        bang(not pham, f"con loi goi GHI vao CONFIG GOC trong tep chinh sach: {pham}")
        # ...va chot nay phai co RANG: dung chinh no soi mot doan gia co loi ghi.
        gia = ast.parse('tep.write_bytes(x)\nos.replace(tam, tep)\n')
        thay_duoc = [n for n in ast.walk(gia) if isinstance(n, ast.Call)]
        bang(len(thay_duoc) == 2, "fixture chot AST hong")


@ca
def t99_nhat_ky_ca_phai_song_sot_qua_mot_cu_giet():
    """Dòng in CUỐI CÙNG không phải ca chạy CUỐI CÙNG — nhật ký phải nói được ca nào.

    Ba lượt review đi truy nhầm chỗ vì đúng chuyện này: suite không in gì trong lúc
    chạy, nên khi bị giết thì thứ còn lại trên màn hình là dòng `BO QUA t62`, và cả
    reviewer lẫn tôi đọc thành "chết ở ngay sau t62". Đó là tạo tác của BỘ ĐỆM.

    Chốt mạnh nhất ở đây là ca (b): một ca TỰ ĐỌC nhật ký trong lúc nó đang chạy và
    đòi thấy dòng `>>> vao` của CHÍNH NÓ đã nằm trên đĩa. Nếu `flush`/`fsync` chạy
    SAU ca thay vì TRƯỚC, ca này đỏ — mà đúng thứ tự đó mới là thứ sống sót qua một
    cú giết không bắt được.
    """
    with San() as s:
        duong = s / "nhat-ky.txt"
        thay = []

        def ca_qua():
            thay.append("qua")

        def ca_tu_doc_nhat_ky():
            # ĐỌC nhat ky NGAY TRONG luc minh dang chay
            noi_dung = duong.read_text(encoding="utf-8")
            bang("ca_tu_doc_nhat_ky" in noi_dung,
                 "dong '>>> vao' CHUA nam tren dia luc ca dang chay — ghi SAU thi "
                 "mot cu giet la mat dau vet")

        def ca_bo_qua():
            return "co tinh bo qua"

        def ca_hong():
            bang(False, "co tinh hong")

        ds = [ca_qua, ca_tu_doc_nhat_ky, ca_bo_qua, ca_hong]
        nk = NhatKyCa(duong)
        cu_out = sys.stdout
        sys.stdout = io.StringIO()      # nuot dong "BO QUA ca_bo_qua" cua ca gia
        try:
            qua, bo_qua, hong = chay_bo_ca(ds, nk)
        finally:
            sys.stdout = cu_out
            nk.dong()

        bang((qua, bo_qua, len(hong)) == (2, 1, 1),
             f"dem sai: qua={qua} bo_qua={bo_qua} hong={len(hong)}")
        dong = duong.read_text(encoding="utf-8").splitlines()
        vao = [d for d in dong if d.startswith(">>> vao")]
        ra = [d for d in dong if d.startswith("<<< ra")]
        bang(len(vao) == 4, f"thieu dong vao: {len(vao)}/4")
        bang(len(ra) == 4, f"thieu dong ra: {len(ra)}/4 — ca HONG/BO QUA cung phai co")
        for ten in ("ca_qua", "ca_bo_qua", "ca_hong"):
            bang(any(ten in d for d in ra), f"thieu ket qua cua {ten}")
        bang(any("BO QUA" in d for d in ra), "khong phan biet duoc BO QUA")
        bang(any("HONG" in d for d in ra), "khong phan biet duoc HONG")
        bang(dong[-1].startswith("# XONG TRON VEN"),
             f"thieu dau XONG TRON VEN — khong phan biet duoc 'chay het' voi 'bi giet': {dong[-1]!r}")


@ca
def t98_CO_CREDENTIAL_khong_duoc_thanh_kha_dung_o_tang_doctor():
    """Tầng ĐO thôi nâng nhãn rồi, tầng TIÊU THỤ nâng lại thì coi như chưa sửa gì.

    Cross-review lượt 6, P1: `_do_codex` đã tách `CO_CREDENTIAL` khỏi `DUNG_DUOC`,
    nhưng `lenh_doctor` chỉ trừ `chua_xac_thuc` khi tính `ok_kha_dung` — mà danh sách
    ấy KHÔNG chứa `CO_CREDENTIAL`. Hệ quả: đúng cái credential mà lời gọi thật trả
    401 vẫn cho `ok_kha_dung=true` và `--doi-kha-dung` vẫn thoát 0.

    Ca này ghim ở tầng `lenh_doctor`, KHÔNG gọi CLI thật: bảng `KHA_NANG` và `CONG_CU`
    đều được ghim, nên kết quả không phụ thuộc credential của máy đang chạy — đúng bài
    học "cổng phụ thuộc nơi chạy thì chưa phải cổng".
    """
    m = _tai_launcher_thu()
    m.CONG_CU = []                       # khong do cong cu that => thieu_bat_buoc rong

    class DoiSo:
        json = True
        workspace = None
        kiem_song = False
        doi_kha_dung = False

    def dat(nhan):
        m.KHA_NANG = [{"ten": "codex", "do": lambda ws, ks=False: (nhan, "x"),
                       "vi_sao": "v", "khac_phuc": "k"}]

    def chay_doctor(doi_kha_dung):
        a = DoiSo()
        a.doi_kha_dung = doi_kha_dung
        cu = sys.stdout
        sys.stdout = io.StringIO()
        try:
            ma = m.lenh_doctor(a)
            return ma, json.loads(sys.stdout.getvalue())
        finally:
            sys.stdout = cu

    # (a) DUNG_DUOC = da chung minh => kha dung, ma 0 ke ca khi doi
    dat("DUNG_DUOC")
    ma, d = chay_doctor(True)
    bang(d["ok_kha_dung"] is True, f"DUNG_DUOC ma bao khong kha dung: {d['ok_kha_dung']}")
    bang(ma == MA_OK, f"DUNG_DUOC ma van chan: {ma}")

    # (b) CO_CREDENTIAL = CHUA chung minh => KHONG duoc bao kha dung
    dat("CO_CREDENTIAL")
    ma, d = chay_doctor(False)
    bang(d["ok_kha_dung"] is False,
         "CO_CREDENTIAL van duoc tinh la KHA DUNG — tang tieu thu nang lai nhan")
    bang("codex" in d["chua_chung_minh"], f"phai neu ten muc: {d.get('chua_chung_minh')}")
    bang(ma == MA_OK, f"KHONG doi kha dung thi van phai 0 (khong chan oan): {ma}")

    # (c) doi kha dung => FAIL-CLOSED
    ma, _ = chay_doctor(True)
    bang(ma == MA_CHUA_XAC_THUC,
         f"--doi-kha-dung ma CO_CREDENTIAL van thoat {ma}: doi bang chung roi nhan bua")

    # (d) SAP_HET_HAN cung CHUA chung minh (han lay tu JWT khong xac thuc chu ky)
    dat("SAP_HET_HAN")
    ma, d = chay_doctor(True)
    bang(d["ok_kha_dung"] is False, "SAP_HET_HAN khong phai bang chung dung duoc")
    bang(ma == MA_CHUA_XAC_THUC, f"--doi-kha-dung voi SAP_HET_HAN phai chan, duoc {ma}")

    # (e) KHONG_DO_DUOC: `None` KHAC `False` — khong do duoc thi khong duoc noi la xanh
    dat("KHONG_DO_DUOC")
    ma, d = chay_doctor(True)
    bang(d["ok_kha_dung"] is False, "KHONG_DO_DUOC ma bao kha dung")
    bang(ma == MA_CHUA_XAC_THUC, f"--doi-kha-dung voi KHONG_DO_DUOC phai chan, duoc {ma}")


@ca
def t97_nap_ban_sao_khong_duoc_an_phai_BYTECODE_CU():
    """Cổng đột biến phải chấm điểm ĐÚNG BẢN nó vừa ghi, không phải bản trước đó.

    ĐÃ ĐO, và đây là nguyên nhân gốc thật của ba lượt cãi nhau về con số: runner ghi
    mọi bản sao vào cùng một đường dẫn, mà CPython coi `.pyc` còn hợp lệ theo (mtime
    tính bằng GIÂY, kích thước). Hai đột biến ra tệp CÙNG kích thước, ghi trong CÙNG
    một giây ⇒ bản sau chạy MÃ CỦA BẢN TRƯỚC. Mutant `do_codex_tin_DONG_DAU…` báo
    `giet 0/1` suốt ba lượt vì nó CHƯA TỪNG ĐƯỢC CHẠY.

    Ca này dựng lại đúng cái bẫy đó — hai nội dung KHÁC nhau, CÙNG kích thước, ghi
    liên tiếp vào CÙNG đường dẫn — rồi đòi bản nạp lần hai phải là bản thứ hai. Với
    `exec_module` trần, nó ĐỎ; với `_nap_sach`, nó xanh.

    Không đưa được vào bảng `DOT_BIEN`: runner chỉ đột biến `launcher.py`, còn hàm
    này ở `launcher_test.py`. Cùng giới hạn đã khai cho `_co_lap_toan_cuc`/`t89`.
    Phản chứng thay thế đã CHẠY TAY (ghi trong CHANGELOG): bỏ lớp xoá `.pyc` thì ca
    này đỏ.
    """
    with San() as s:
        tep = s / "mo_dun_thu.py"
        # CÙNG SỐ KÝ TỰ, khác nội dung — đúng điều kiện làm `.pyc` bị coi là hợp lệ.
        tep.write_text("GIA_TRI = 'AAA'\n", encoding="utf-8")
        m1 = _nap_sach(tep)
        bang(m1.GIA_TRI == "AAA", f"lan nap dau da sai: {m1.GIA_TRI!r}")
        tep.write_text("GIA_TRI = 'BBB'\n", encoding="utf-8")
        bang(len("GIA_TRI = 'AAA'\n") == len("GIA_TRI = 'BBB'\n"),
             "fixture hong: hai ban PHAI cung kich thuoc thi bay moi bat")
        m2 = _nap_sach(tep)
        bang(m2.GIA_TRI == "BBB",
             f"NAP PHAI BAN CU: doc duoc {m2.GIA_TRI!r} trong khi tren dia la 'BBB' "
             f"— cong dang cham diem mot ban khac voi ban no vua ghi")

    # Lớp thứ hai: `.pyc` CÒN SÓT TỪ LƯỢT CHẠY TRƯỚC. Tắt ghi bytecode không cứu
    # được ca này (tắt GHI khác tắt ĐỌC) — chỉ xoá mới cứu.
    with San() as s:
        tep = s / "mo_dun_thu2.py"
        tep.write_text("GIA_TRI = 'AAA'\n", encoding="utf-8")
        truoc = sys.dont_write_bytecode
        sys.dont_write_bytecode = False
        try:
            sp = importlib.util.spec_from_file_location("sinh_pyc_cu", tep)
            mm = importlib.util.module_from_spec(sp)
            sp.loader.exec_module(mm)           # ghi ra .pyc
        finally:
            sys.dont_write_bytecode = truoc
        tep.write_text("GIA_TRI = 'BBB'\n", encoding="utf-8")
        m3 = _nap_sach(tep)
        bang(m3.GIA_TRI == "BBB",
             f"pyc con sot tu luot truoc van duoc dung: doc {m3.GIA_TRI!r}")

    # Lớp thứ ba, ĐO RIÊNG: tắt ghi bytecode. Phản chứng đã chạy cho thấy bỏ lớp này
    # KHÔNG làm hai khối trên đỏ — tức nó là phòng thủ chồng lớp KHÔNG CÓ RĂNG nếu
    # không đo thẳng. Đo thẳng: nạp xong thì KHÔNG được để lại `.pyc` nào.
    with San() as s:
        tep = s / "mo_dun_thu3.py"
        tep.write_text("GIA_TRI = 'CCC'\n", encoding="utf-8")
        _nap_sach(tep)
        pyc = Path(importlib.util.cache_from_source(str(tep)))
        bang(not pyc.exists(),
             f"nap xong con de lai {pyc.name} — lop tat ghi bytecode da bi go")


@ca
def t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec():
    """`mcp-endpoint` — PLAT-M4 (#194). Đo đầu kia của dây, phân loại bằng HEADER.

    SỐ CA LÀ `t143`, KHÔNG PHẢI `t138` — và đây là va chạm THẬT, không phải chuyện đặt
    tên. Packet này viết ca ấy khi `t137` còn là số cuối; trong lúc nó chờ, `#196` (PR
    "#202") land bốn ca `t138`–`t142`. Hai nhánh cùng chọn `t138`, và git merge SẠCH: hai
    hàm khác tên đầy đủ nên không dòng nào đụng dòng nào. Suite vẫn chạy cả hai (decorator
    `@ca` giữ đối tượng hàm), nên KHÔNG cổng nào đỏ — chỉ có `--lap-ca t138` là mơ hồ và
    bảng đột biến trỏ vào một cái tên không còn duy nhất.
    Ghi ra vì đúng lớp "merge sạch là bảo đảm VĂN BẢN, không phải NGỮ NGHĨA" mà §5.1
    protocol nói: thứ bắt được nó là ĐỌC, không phải cổng.

    VÌ SAO CÓ CA NÀY. Trước PLAT-M4, cả hai bước của đường MCP (`.mcp.json` và
    `claude mcp get`) đều hỏi phía CLI — DÂY NỐI. Đo được trong chính container này:
    `mcp-cli=khong` (CLI báo `Pending approval`) trong khi `mcp-endpoint=OK` (POST
    `initialize` trả HTTP 200 kèm header GitHub). Một phiên đọc trường gộp cũ sẽ kết
    luận "GitHub bị chặn" rồi dừng — ĐÃ XẢY RA, mất trọn một lượt.

    Ca này khoá CHÍN điều. Sáu điều đầu là phản chứng ở §5 thân Issue #194; điều 7 và 8
    đến từ lượt cross-review 2/2 và khoá BIÊN CẤU TRÚC của `userinfo` — xem (5c)–(5g):
      7. URL MÉO mang credential (không parse ra `userinfo`) phải bị từ chối MÀ KHÔNG
         làm lộ bí mật qua MÔ TẢ — "không gọi mạng" KHÔNG bằng "không làm lộ".
      8. Biên phải đo theo CẤU TRÚC, không theo ký tự: `@` trong path/query vẫn probe
         được, còn username RỖNG + password CÓ vẫn là credential và phải bị chặn.
    (Điều thứ chín, đo bằng HÀNH VI, nằm ở cuối docstring này — nó đánh số 9, KHÔNG
    phải 7. Bản trước đánh nó HAI SỐ cùng lúc và khai tổng là TÁM trong khi khoá chín;
    lượt review 3 bắt được, và đó là LẦN THỨ HAI liên tiếp lời khai số đếm của chính ca
    này trôi — lượt 2 đã bắt bản 'sáu điều'. Cả chín điều ĐỀU có phép đo thật; thứ sai
    chỉ là con số, mà con số sai vẫn là lời khai sai.)
      1. 200 CÓ header  -> `mo` + THÀNH CÔNG          (phân loại theo header, không theo mã)
      2. 4xx KHÔNG header -> `chan`, nói rõ "proxy tự sinh"
      3. 4xx CÓ header  -> `mo` NHƯNG không thành công (hai câu hỏi khác nhau)
      4. mạng hỏng/quá hạn -> `khong_do_duoc`, KHÔNG gộp vào `chan` (`None ≠ False`)
      5. thiếu `url` / `url` không phải http(s) -> `khong_do_duoc` CÓ LÝ DO, và
         KHÔNG được gọi `urlopen` lấy một lần (`file:///` là lượt đọc đĩa trá hình)
      6. token KHÔNG lộ ra bất kỳ byte mô tả nào — kể cả khi đi qua `_do_github`
    Và điều thứ CHÍN, đo bằng HÀNH VI chứ không bằng đọc mã: `mcp-endpoint=OK` một mình
    KHÔNG được nâng nhãn lên `DUNG_DUOC`.
    """
    import json as _json
    m = _tai_launcher_thu()
    SENT = "TL-SENTINEL-KHONG-DUOC-LO-9f3c1a"
    goc_urlopen = m.urllib.request.urlopen
    goc_git, goc_which = m._git, m.shutil.which
    nhat_ky = []

    class _Ph:
        def __init__(self, status, headers):
            self.status, self.headers = status, headers
        def __enter__(self): return self
        def __exit__(self, *_a): return False

    def dat(ket):
        def gia(req, *_a, **_k):
            nhat_ky.append(req)
            return ket()
        m.urllib.request.urlopen = gia

    def _nem(code, headers):
        def f():
            raise m.urllib.error.HTTPError("https://x/mcp/", code, "loi", headers, None)
        return f

    try:
        # (1) 200 CO header -> `mo` + thanh cong
        dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
        tt, mo_ta, ok = m._do_mcp_endpoint("https://x/mcp/", token=SENT)
        bang(tt == "mo" and ok is True, f"200 co header phai `mo`+thanh cong: {tt} {ok} {mo_ta!r}")

        # ...va LOI GOI phai dung hinh dang: POST, than la JSON-RPC `initialize`.
        # Khong khang dinh dieu nay thi mot ban va "do" bang GET van qua ca tren.
        req = nhat_ky[-1]
        bang(req.get_method() == "POST", f"phai POST, do {req.get_method()}")
        than = _json.loads(req.data.decode("utf-8"))
        bang(than.get("method") == "initialize", f"than khong phai initialize: {than!r}")
        bang(req.headers.get("Authorization") == f"Bearer {SENT}",
             "token da truyen ma khong len header Authorization")

        # (6) MO TA khong duoc chua token. Do THU DA DEN, khong suy luan "urllib dau co in".
        bang(SENT not in mo_ta, f"MO TA CHUA TOKEN: {mo_ta!r}")

        # 200 KHONG header = proxy tra loi thay, khong phai duong toi noi.
        dat(lambda: _Ph(200, {"Content-Type": "application/json"}))
        tt, mo_ta, ok = m._do_mcp_endpoint("https://x/mcp/")
        bang(tt == "chan" and ok is False, f"200 khong header phai `chan`: {tt} {ok}")
        # ...va khong token thi KHONG duoc tu bia header Authorization
        bang(nhat_ky[-1].headers.get("Authorization") is None,
             "khong co token ma van gui Authorization")

        # (2) 403 KHONG header -> `chan`, va phai NOI RA la proxy tu sinh
        dat(_nem(403, {"Content-Type": "text/plain"}))
        tt, mo_ta, ok = m._do_mcp_endpoint("https://x/mcp/")
        bang(tt == "chan" and "proxy" in mo_ta,
             f"403 khong header phai `chan` + noi proxy: {tt} {mo_ta!r}")

        # (3) 401 CO header -> `mo` (toi noi) NHUNG khong thanh cong (thieu quyen)
        dat(_nem(401, {"X-GitHub-Request-Id": "abc"}))
        tt, mo_ta, ok = m._do_mcp_endpoint("https://x/mcp/", token=SENT)
        bang(tt == "mo" and ok is False,
             f"401 co header phai `mo` NHUNG khong thanh cong: {tt} {ok}")
        bang("thieu quyen" in mo_ta, f"401 co header ma khong noi thieu quyen: {mo_ta!r}")
        bang(SENT not in mo_ta, f"MO TA nhanh loi CHUA TOKEN: {mo_ta!r}")

        # (4) mang hong / qua han -> KHONG DO DUOC, khong phai `chan`
        def _no():
            raise OSError("mang hong")
        dat(_no)
        tt, mo_ta, ok = m._do_mcp_endpoint("https://x/mcp/")
        bang(tt == "khong_do_duoc" and ok is False,
             f"mang hong bi gop vao `chan` (None != False): {tt} {mo_ta!r}")

        # (5) THIEU url / url khong phai http(s) -> KHONG DO DUOC, va KHONG goi urlopen.
        # `urlopen` nhan ca `file://`, nen mot `.mcp.json` tro `file:///etc/passwd` se
        # bien probe mang thanh luot DOC DIA. Chan bang danh sach CHO PHEP.
        for xau in (None, "", "file:///etc/passwd", "ftp://x/y", " javascript:x"):
            nhat_ky.clear()
            dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
            tt, mo_ta, ok = m._do_mcp_endpoint(xau)
            bang(tt == "khong_do_duoc" and ok is False,
                 f"url {xau!r} phai la KHONG DO DUOC, duoc {tt}")
            bang(mo_ta.strip() != "", f"url {xau!r}: KHONG DO DUOC ma khong noi ly do")
            bang(not nhat_ky, f"url {xau!r} ma VAN goi urlopen {len(nhat_ky)} lan")

        # (5b) CREDENTIAL TRONG `userinfo` -> TU CHOI, va KHONG probe. Finding P2 cua
        # cross-review luot 1: khop TIEN TO CHUOI cho `https://user:SECRET@host` di qua,
        # roi bi mat vao CA `req.full_url` LAN `req.host` — tuc no roi khoi tien trinh.
        # Ba khang dinh, khong phai mot: nhan dung · urlopen KHONG duoc goi · MO TA khong
        # cho bi mat (mot ban va "tu choi" ma van in URL ra thi van la ro ri).
        for xau in ("http://user:" + SENT + "@127.0.0.1/mcp",
                    "https://user:" + SENT + "@example.test/mcp",
                    "https://" + SENT + "@example.test/mcp"):
            nhat_ky.clear()
            dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
            tt, mo_ta, ok = m._do_mcp_endpoint(xau, token=SENT)
            bang(tt == "khong_do_duoc" and ok is False,
                 f"url co userinfo phai bi TU CHOI, duoc {tt} {ok}")
            bang(not nhat_ky,
                 f"url co userinfo ma VAN goi urlopen {len(nhat_ky)} lan — bi mat da roi "
                 f"khoi tien trinh truoc khi ai kip tu choi")
            bang(SENT not in mo_ta, f"MO TA cua nhanh userinfo CHO BI MAT: {mo_ta!r}")

        # ...va DUONG THUAN khong duoc hong theo: URL sach van probe duoc. Khong co ca
        # nay thi mot ban va "tu choi tat ca" cung xanh.
        nhat_ky.clear()
        dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
        tt, mo_ta, ok = m._do_mcp_endpoint("https://x/mcp/", token=SENT)
        bang(tt == "mo" and ok is True and len(nhat_ky) == 1,
             f"url SACH bi chan nham: {tt} {ok} {len(nhat_ky)} loi goi")

        # (5c) URL MEO — luot review 2/2 tim ra, va no la NUA THU HAI cua cung finding.
        # Bon dang duoi day KHONG phan tich duoc thanh `userinfo`, nen chung TRUOT khoi
        # nhanh userinfo va roi xuong nhanh scheme/hostname. Truoc ban va, hai nhanh ay
        # noi suy `{url!r}` ⇒ khong probe nua NHUNG van lam lo bi mat qua MO TA.
        # Bai hoc: "khong goi mang" khong bang "khong lam lo" — dem CA HAI duong ra.
        for xau in (f"http:///user:{SENT}@host/mcp",
                    f"javascript:user:{SENT}@host",
                    f"http ://user:{SENT}@host/mcp",
                    f"http://?u=user:{SENT}@host"):
            nhat_ky.clear()
            dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
            tt, mo_ta, ok = m._do_mcp_endpoint(xau, token=SENT)
            bang(tt == "khong_do_duoc" and ok is False,
                 f"url meo phai la KHONG DO DUOC, duoc {tt}")
            bang(not nhat_ky, f"url meo ma VAN goi urlopen {len(nhat_ky)} lan")
            bang(SENT not in mo_ta,
                 f"MO TA nhanh tu choi CHO BI MAT — khong goi mang nhung van lam lo: {mo_ta!r}")

        # (5d) BIEN CAU TRUC, chieu THUAN: `@` trong path/query KHONG phai userinfo, nen
        # url ay phai ĐƯỢC probe. Khong co ca nay thi mot ban cai do bang KY TU
        # (`if "@" in url`) van xanh, va no chan oan url hop le.
        for sach in ("https://host.test/mcp/@lich-su", "https://host.test/mcp?ai=a@b.test"):
            nhat_ky.clear()
            dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
            tt, _mt, ok = m._do_mcp_endpoint(sach)
            bang(tt == "mo" and ok is True and len(nhat_ky) == 1,
                 f"`@` trong path/query KHONG phai credential — {sach!r} bi chan oan: {tt}")

        # (5e) BIEN CAU TRUC, chieu NGHICH: username RONG ma password CO thi van la
        # credential. Mot ban cai doc `username` theo tinh CHAN LY (`if p_ep.username:`)
        # se cho no di qua, va bi mat vao ca `full_url` lan `host`.
        nhat_ky.clear()
        dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
        tt, mo_ta, ok = m._do_mcp_endpoint(f"https://:{SENT}@host.test/mcp", token=SENT)
        bang(tt == "khong_do_duoc" and ok is False and not nhat_ky,
             f"username RONG + password CO van la credential, phai tu choi: {tt} "
             f"{len(nhat_ky)} loi goi")
        bang(SENT not in mo_ta, f"MO TA cho bi mat o ca username rong: {mo_ta!r}")

        # (5f) BIEN CAU TRUC, khe THU BA: VI TRI PORT. Finding R1 cua luot review 3.
        # `urlsplit` chi gan `username`/`password` khi co dau `@`, nen bi mat dat o cho
        # port di qua HET ba chot cu (khong userinfo, scheme https, co hostname). Ban
        # truoc KHONG lo o runtime that — nhung chi vi `http.client` nem `InvalidURL`
        # truoc khi mo socket, tuc mot chot cua NGUOI KHAC. Doc `p_ep.port` trong `try`
        # bien no thanh chot CUA TA. Dot bien lam ca nay do: bo dong `_ = p_ep.port`.
        nhat_ky.clear()
        dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
        tt, mo_ta, ok = m._do_mcp_endpoint(f"https://host.test:{SENT}/mcp", token=SENT)
        bang(tt == "khong_do_duoc" and ok is False and not nhat_ky,
             f"bi mat o VI TRI PORT phai bi tu choi TRUOC khi probe: {tt} "
             f"{len(nhat_ky)} loi goi")
        bang(SENT not in mo_ta, f"MO TA cho bi mat o ca port: {mo_ta!r}")

        # (5g) `_doc_mcp_json` KHONG duoc noi suy `url` NGUYEN VAN vao mo ta. Finding R3.
        # Ham do o NGAY BEN CANH va dung chuan khac han `_do_mcp_endpoint`; hien caller
        # vut chuoi ay o nhanh duong nen chua lo, nhung do la may man cua CALLER chu khong
        # phai bat bien cua HAM. Dot bien lam ca nay do: tra lai `f" @ {url}"`.
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / ".mcp.json").write_text(
                _json.dumps({"mcpServers": {
                    "github": {"url": f"https://nguoi:{SENT}@host.test/mcp"}}}),
                encoding="utf-8")
            co_khai, mt_mcp, _ten, _url = m._doc_mcp_json(td)
            bang(co_khai is True, f"`.mcp.json` hop le ma bao khong khai: {mt_mcp!r}")
            bang(SENT not in mt_mcp,
                 f"MO TA cua `_doc_mcp_json` CHUA bi mat lay tu `url`: {mt_mcp!r}")
            bang("host.test" in mt_mcp,
                 f"cat het thi nguoi doc khong biet no tro DI DAU — phai con host: {mt_mcp!r}")

        # --- DIEU THU CHIN, do bang HANH VI: endpoint OK mot minh KHONG nang duoc nhan.
        # Doc ma nguon (khuc dau ca t115) chi bat duoc dot bien SUA DUNG dong
        # `LAM_DUOC_VIEC`; ca nay bat ca nhung duong vong khac dan toi cung hau qua.
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / ".mcp.json").write_text(
                _json.dumps({"mcpServers": {"github": {"url": "https://x/mcp/"}}}),
                encoding="utf-8")
            m._git = lambda *_a, **_k: (1, "", "khong phai kho")
            m.shutil.which = lambda t, *a, **k: None
            m._do_rest_github = lambda *_a, **_k: ("chan", "HTTP 403 (KHONG header GitHub)", False)
            m._suc_khoe_mcp_github = lambda *_a, **_k: ("hong", "Status: Pending approval")
            dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
            nhan, chi_tiet = m._do_github(td, {"GH_TOKEN": SENT})
            bang("mcp-cli=" in chi_tiet and "mcp-endpoint=" in chi_tiet,
                 f"doctor phai in CA HAI truong: {chi_tiet!r}")
            bang("mcp=" not in chi_tiet,
                 f"con sot truong gop `mcp=` — hai cau hoi khac nhau phai la hai truong: {chi_tiet!r}")
            bang("mcp-endpoint=OK" in chi_tiet, f"endpoint 200 co header ma khong OK: {chi_tiet!r}")
            bang(nhan == "CHUA_XAC_THUC",
                 f"CHI co mcp-endpoint OK ma nhan len {nhan} — `initialize` chung minh endpoint "
                 f"TRA LOI, khong chung minh doc duoc kho nay: {chi_tiet!r}")
            bang(SENT not in chi_tiet, f"CHI TIET cua _do_github CHUA TOKEN: {chi_tiet!r}")

            # LY DO PHAI DI RA TOI NGUOI DOC. Do duoc o luot dau PLAT-M4: chuoi tom
            # tat chi noi `ten=nhan`, nen 401 CO header (endpoint song, token sai) va
            # 403 KHONG header (proxy chan) in ra Y HET nhau — `mcp-endpoint=khong`.
            # Phan loai dung o TRONG ma ket xuat gop o NGOAI thi nguoi doc van di chua
            # nham cho, tuc packet nay moi chua duoc nua duong.
            dat(_nem(401, {"X-GitHub-Request-Id": "abc"}))
            _n401, ct401 = m._do_github(td, {"GH_TOKEN": SENT})
            dat(_nem(403, {"Content-Type": "text/plain"}))
            _n403, ct403 = m._do_github(td, {"GH_TOKEN": SENT})
            bang(ct401 != ct403,
                 f"401 TOI NOI va 403 PROXY in ra Y HET nhau — nguoi doc khong phan biet "
                 f"duoc: {ct401!r}")
            bang("thieu quyen" in ct401, f"401 co header ma dau ra khong noi ly do: {ct401!r}")
            bang("proxy" in ct403, f"403 khong header ma dau ra khong noi proxy: {ct403!r}")
            bang(SENT not in ct401 and SENT not in ct403, "CHI TIET CHUA TOKEN")

            # ...duong XANH thi KHONG duoc noi them chu: dong thuong phai ngan.
            dat(lambda: _Ph(200, {"X-GitHub-Request-Id": "abc"}))
            _nok, ctok = m._do_github(td, {"GH_TOKEN": SENT})
            bang("mcp-endpoint: " not in ctok,
                 f"duong xanh ma van noi them mo ta: {ctok!r}")

            # ...va khi `.mcp.json` chua khai server thi endpoint la CHUA DO DUOC,
            # KHONG phai `khong`: ta khong biet URL nao de hoi.
            (Path(td) / ".mcp.json").write_text("{}", encoding="utf-8")
            _nhan2, chi_tiet2 = m._do_github(td, {"GH_TOKEN": SENT})
            bang("mcp-endpoint=chua-do-duoc" in chi_tiet2,
                 f"chua khai server ma endpoint khong phai chua-do-duoc: {chi_tiet2!r}")
    finally:
        m.urllib.request.urlopen = goc_urlopen
        m._git, m.shutil.which = goc_git, goc_which


@ca
def t144_run_ghi_nonce_va_hmac_khong_lo_khoa():
    with San() as s:
        repo = tao_repo(s); rr = s / "runs"; state = s / "wp55.json"
        nonce, khoa = "1" * 32, "2" * 64
        state.write_text(json.dumps({"attempt_open": True, "hmac_key": khoa,
                                     "attempt_anchor": {"attempt": 1, "nonce": nonce,
                                                        "consumed": False}}), encoding="utf-8")
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--attempt-state", str(state), "--void-reason", "infrastructure",
                 "--", PY, "-c", "pass")
        bang(r.returncode == 0, f"run có neo hỏng: {r.returncode} {r.stderr}")
        raw = (next(rr.iterdir()) / "run.json").read_text(encoding="utf-8")
        d = json.loads(raw); chu_ky = d.pop("chu_ky", None)
        than = json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                          allow_nan=False).encode("utf-8")
        mong = hmac.new(bytes.fromhex(khoa), than, hashlib.sha256).hexdigest()
        bang(d.get("nonce") == nonce and chu_ky == mong, "nonce/HMAC không khớp bản ghi")
        bang(khoa not in raw, "khoá HMAC bị ghi vào run.json")


@ca
def t145_agy_cong_cu_va_kha_nang():
    """N1 & N2: agy trong CONG_CU và antigravity trong KHA_NANG."""
    m = _tai_launcher_thu()
    ds_agy = [c for c in m.CONG_CU if c.get("ten") == "agy"]
    bang(len(ds_agy) == 1, f"CONG_CU phai co dung 1 muc agy: {ds_agy}")
    c_agy = ds_agy[0]
    bang(c_agy.get("bat_buoc") is False, f"agy khong phai bat_buoc=False: {c_agy}")
    bang(c_agy.get("xac_thuc") == ["models"], f"xac_thuc cua agy phai la ['models']: {c_agy}")
    bang(c_agy.get("ung_vien") == ["agy"], f"ung_vien cua agy phai la ['agy']: {c_agy}")

    ds_kn = [k for k in m.KHA_NANG if k.get("ten") == "antigravity"]
    bang(len(ds_kn) == 1, f"KHA_NANG phai co dung 1 muc antigravity: {ds_kn}")
    k_ag = ds_kn[0]
    bang("google_antigravity" in k_ag.get("vi_sao", "") and "antigravity" in k_ag.get("vi_sao", ""),
         f"vi_sao cua antigravity phai neu ro provider: {k_ag}")


@ca
def t146_do_antigravity_cac_trang_thai_va_luong():
    """N3-N7, N9: _do_antigravity đọc cả 2 luồng, không gọi trần, không vào LAM_DUOC_VIEC."""
    m = _tai_launcher_thu()
    goc_cac = m._cac_duong_dan
    goc_chay = m._chay_van_ban_an_toan
    goc_sub_run = m.subprocess.run
    nhat_ky_lenh = []

    m._cac_duong_dan = lambda c, mt: [("agy", "/gia/bin/agy")]

    def gia_chay(lenh, env=None, timeout=None, **kwargs):
        nhat_ky_lenh.append(list(lenh))
        # N3: khong bao gio goi agy tran
        bang(len(lenh) >= 2 and lenh[0] == "/gia/bin/agy", f"goi agy tran hoac sai lenh: {lenh}")
        # N4: khong goi -p / --print
        bang("-p" not in lenh and "--print" not in lenh, f"goi -p trong doctor mac dinh: {lenh}")
        sub = lenh[1]
        if sub == "models":
            # N5: models rc=0 tren stderr duy nhat van la DUNG_DUOC
            return subprocess.CompletedProcess(lenh, 0, stdout="", stderr="gemini-2.5-pro\ngemini-2.5-flash\n")
        return subprocess.CompletedProcess(lenh, 0, stdout="1.1.17", stderr="")

    try:
        m._chay_van_ban_an_toan = gia_chay
        m.subprocess.run = gia_chay
        tt, mo_ta = m._do_antigravity({})
        bang(tt == "DUNG_DUOC", f"stderr-only models phai la DUNG_DUOC: tt={tt}, mo_ta={mo_ta}")

        # N7: rc=0 ca 2 luong rong => KHONG_DO_DUOC (Finding 1: Spec 6.2, khong lam tron thanh CO_MAT hay DUNG_DUOC)
        m._cac_duong_dan = lambda c, mt: [("agy", "/gia/bin/agy")]
        def gia_rong(lenh, env=None, timeout=None, **kwargs):
            return subprocess.CompletedProcess(
                lenh, 0, stdout="", stderr=""
            ) if lenh[1] == "models" else subprocess.CompletedProcess(lenh, 0, stdout="1.1.17", stderr="")
        m._chay_van_ban_an_toan = gia_rong
        m.subprocess.run = gia_rong
        tt2, mo_ta2 = m._do_antigravity({})
        bang(tt2 == "KHONG_DO_DUOC", f"rc=0 rong ca hai luong phai la KHONG_DO_DUOC: tt2={tt2}, mo_ta2={mo_ta2}")

        # models rc!=0 va --version rc!=0 => KHONG_DO_DUOC (khong duoc CO_MAT)
        def gia_fail(lenh, env=None, timeout=None, **kwargs):
            return subprocess.CompletedProcess(lenh, 1, stdout="", stderr="error")
        m._chay_van_ban_an_toan = gia_fail
        m.subprocess.run = gia_fail
        tt_both_fail, _ = m._do_antigravity({})
        bang(tt_both_fail == "KHONG_DO_DUOC", f"ca hai probe fail phai la KHONG_DO_DUOC: tt={tt_both_fail}")

        # Fallback candidate: ung vien 1 loi, ung vien 2 thanh cong => DUNG_DUOC
        m._cac_duong_dan = lambda c, mt: [("agy", "/gia/shim/agy"), ("agy", "/gia/bin/agy")]
        def gia_fallback_cand(lenh, env=None, timeout=None, **kwargs):
            if "/gia/shim/agy" in lenh[0]:
                raise OSError("broken shim")
            return subprocess.CompletedProcess(lenh, 0, stdout="gemini-2.5-pro\n", stderr="")
        m._chay_van_ban_an_toan = gia_fallback_cand
        m.subprocess.run = gia_fallback_cand
        tt_cand, _ = m._do_antigravity({})
        bang(tt_cand == "DUNG_DUOC", f"ung vien fallback phai cuu duoc: tt={tt_cand}")
        m._cac_duong_dan = lambda c, mt: [("agy", "/gia/bin/agy")]

        # P2 cross-review (codex, 15f2dbf): `models` thanh cong MOT lan la du bang chung.
        # Lan goi thu HAI bat ky (dem dong, thong ke) neu ném => phai KHONG duoc lat ket luan.
        so_lan = {"n": 0}
        def gia_mot_lan(lenh, env=None, timeout=None, **kwargs):
            if lenh[1] == "models":
                so_lan["n"] += 1
                if so_lan["n"] == 1:
                    return subprocess.CompletedProcess(lenh, 0, stdout="", stderr="gemini-2.5-pro\ngemini-2.5-flash\n")
                raise OSError("agy models bi goi lan thu hai")
            return subprocess.CompletedProcess(lenh, 0, stdout="1.1.17", stderr="")
        m._chay_van_ban_an_toan = gia_mot_lan
        m.subprocess.run = gia_mot_lan
        # Hop dong cua ca: KHONG duoc nem. Bat ngoai le roi dua vao `bang` de cai chet cua
        # mutant mang tin hieu cua CHINH ca nay (TinHieuChotCa), khong phai OSError vo can.
        try:
            tt_mot, mo_ta_mot = m._do_antigravity({})
        except Exception as e:  # noqa: BLE001 — chinh la hanh vi dang do
            tt_mot, mo_ta_mot = "NEM", f"{type(e).__name__}: {e}"
        bang(tt_mot == "DUNG_DUOC" and "2 model" in mo_ta_mot,
             f"models thanh cong lan 1 ma ket luan lat/dem sai: tt={tt_mot}, mo_ta={mo_ta_mot}")
        bang(so_lan["n"] == 1, f"`agy models` bi goi {so_lan['n']} lan trong mot luot do, mong 1")

        # N6: TimeoutExpired / OSError => KHONG_DO_DUOC
        def gia_timeout(lenh, env=None, timeout=None, **kwargs):
            raise subprocess.TimeoutExpired(lenh, timeout or 8.0)
        m._chay_van_ban_an_toan = gia_timeout
        m.subprocess.run = gia_timeout
        tt3, _ = m._do_antigravity({})
        bang(tt3 == "KHONG_DO_DUOC", f"TimeoutExpired phai la KHONG_DO_DUOC, khong lam tron thanh THIEU: tt3={tt3}")

        def gia_oserror(lenh, env=None, timeout=None, **kwargs):
            raise OSError("Permission denied")
        m._chay_van_ban_an_toan = gia_oserror
        m.subprocess.run = gia_oserror
        tt4, _ = m._do_antigravity({})
        bang(tt4 == "KHONG_DO_DUOC", f"OSError phai la KHONG_DO_DUOC: tt4={tt4}")

        # N9: antigravity khong duoc tinh vao LAM_DUOC_VIEC cua _do_github
        # Test theo hanh vi: khi chi co duong ngoai LAM_DUOC_VIEC mo, _do_github phai la CHUA_XAC_THUC
        m._git = lambda ws, *a: (1, "", "fail")
        m._do_rest_github = lambda url, **_k: ("chan", "HTTP 403", False)
        m._doc_mcp_json = lambda ws, **_k: (False, "chua khai", None, None)
        tt_gh, mo_ta_gh = m._do_github("/gia/ws")
        bang(tt_gh == "CHUA_XAC_THUC",
             f"antigravity hoac cac duong khong phai kho khong duoc lam _do_github thanh DUNG_DUOC: {tt_gh}")
    finally:
        m._cac_duong_dan = goc_cac
        m._chay_van_ban_an_toan = goc_chay
        m.subprocess.run = goc_sub_run


@ca
def t147_agy_fallback_localappdata_windows():
    """N8: Windows fallback %LOCALAPPDATA%\\agy\\bin\\agy.exe khi which trượt."""
    m = _tai_launcher_thu()
    with San() as s:
        local_app = s / "LocalAppData"
        agy_bin = local_app / "agy" / "bin"
        agy_bin.mkdir(parents=True)
        agy_exe = agy_bin / "agy.exe"
        agy_exe.write_text("fake binary", encoding="utf-8")

        env_gia = {
            "PATH": "",
            "LOCALAPPDATA": str(local_app),
            "ProgramFiles": str(s / "PF"),
        }

        # Gia lap platform Windows
        goc_plat = m.platform.system
        m.platform.system = lambda: "Windows"
        try:
            duong = m._cac_duong_dan({"ten": "agy", "ung_vien": ["agy"]}, env_gia)
            bang(len(duong) >= 1 and duong[0][1] == str(agy_exe),
                 f"Windows fallback LOCALAPPDATA khong tim thay agy.exe: {duong}")

            # _do_antigravity tren fallback khong bi THIEU
            goc_chay = m._chay_van_ban_an_toan
            goc_sub_run = m.subprocess.run
            gia_mock = lambda lenh, env=None, timeout=None, **kwargs: subprocess.CompletedProcess(
                lenh, 0, stdout="model-1\n", stderr=""
            )
            m._chay_van_ban_an_toan = gia_mock
            m.subprocess.run = gia_mock
            try:
                tt, mo_ta = m._do_antigravity(env_gia)
                bang(tt == "DUNG_DUOC", f"fallback LOCALAPPDATA phai DUNG_DUOC, khong phai THIEU: {tt}")
                bang("đã cài, PATH phiên này chưa thấy — mở terminal mới" in mo_ta,
                     f"fallback LOCALAPPDATA phai co chan doan PATH: {mo_ta}")
            finally:
                m._chay_van_ban_an_toan = goc_chay
                m.subprocess.run = goc_sub_run
        finally:
            m.platform.system = goc_plat


@ca
def t148_doctor_chay_agy_models_MOT_lan_cho_ca_CONG_CU_lan_KHA_NANG():
    """P2 cross-review PR #426 (codex, tren 4639462): `lenh_doctor` da chay probe
    `xac_thuc` (`agy models`) cho bang CONG_CU, roi `_do_antigravity` o khoi KHA_NANG
    chay lai CUNG lenh ay. `models` di mang: lan hai qua han/nem thi ket luan lat.

    Do dau-cuoi qua `lenh_doctor`: lan goi `models` DAU tien thanh cong (stderr-only,
    van la bang chung), MOI lan sau nem OSError. Mong: dung MOT lan goi, CONG_CU agy
    `xac_thuc_ok=True`, KHA_NANG antigravity DUNG_DUOC dem dung 2 model, va
    `--doi-kha-dung` thoat 0 (khong bi lat thanh chua-chung-minh).

    Chot phan hai: bang ket qua la CUA MOT LUOT — luot `doctor` ke tiep phai xoa sach,
    khong doc anh chup cu (mutant xoa `.clear()` chet o ve nay, va CHI o ve nay: xem
    chu thich tai cho).
    """
    m = _tai_launcher_thu()
    c_agy = [dict(c) for c in m.CONG_CU if c.get("ten") == "agy"]
    k_ag = [dict(k) for k in m.KHA_NANG if k.get("ten") == "antigravity"]
    bang(len(c_agy) == 1 and len(k_ag) == 1, "thieu muc agy/antigravity de dung san")
    m.CONG_CU = c_agy
    m.KHA_NANG = k_ag
    m.MODULE_PY = []
    m._doc_moi_truong = lambda: (
        {"PATH": "P", "TL_LAUNCHER_ENV_DA_DOC": "1"}, {"da_doc_truoc_cong_cu": True})
    m._cac_duong_dan = lambda _c, _e: [("agy", "/gia/bin/agy")]
    so_lan = {"n": 0}

    def gia_mot_lan(lenh, env=None, timeout=None, **kwargs):
        if lenh[0] == "/gia/bin/agy" and lenh[1] == "models":
            so_lan["n"] += 1
            if so_lan["n"] == 1:
                return subprocess.CompletedProcess(
                    lenh, 0, stdout="", stderr="gemini-2.5-pro\ngemini-2.5-flash\n")
            raise OSError("agy models bi goi lan thu hai trong cung luot doctor")
        return subprocess.CompletedProcess(lenh, 0, stdout="1.1.17", stderr="")

    m._chay_van_ban_an_toan = gia_mot_lan
    m.subprocess.run = gia_mot_lan
    rc, d = _doctor_json(m, doi_kha_dung=True)
    cc = [c for c in d["cong_cu"] if c.get("ten") == "agy"]
    kn = [k for k in d["kha_nang"] if k.get("ten") == "antigravity"]
    bang(len(cc) == 1 and cc[0].get("xac_thuc_ok") is True,
         f"CONG_CU agy phai xac_thuc_ok=True tu lan probe dau: {cc}")
    bang(len(kn) == 1 and kn[0].get("trang_thai") == "DUNG_DUOC"
         and "2 model" in kn[0].get("chi_tiet", ""),
         f"KHA_NANG antigravity phai DUNG_DUOC va dem 2 model tu DAU RA cua probe doctor: {kn}")
    bang(so_lan["n"] == 1,
         f"`agy models` bi goi {so_lan['n']} lan trong MOT luot doctor, mong 1")
    bang(rc == 0, f"--doi-kha-dung phai thoat 0 khi bang chung duong da co: rc={rc}")

    # Luot ke tiep: bang CONG_CU KHONG con muc agy (khong ai ghi probe `models` luot nay),
    # va `agy models` nay that bai. KHA_NANG antigravity phai TU do lai va ra CO_MAT;
    # doc anh chup DUNG_DUOC cua luot truoc la lay bang chung cu lam bang chung moi.
    # (Neu luot hai van co muc agy trong CONG_CU thi khoa bi ghi de truoc khi doc, nen
    # ve nay moi la ve duy nhat lam mutant bo `.clear()` chet — da do: mutant song sot
    # voi kich ban "cung muc, probe hong".)
    def gia_hong(lenh, env=None, timeout=None, **kwargs):
        if lenh[0] == "/gia/bin/agy" and lenh[1] == "models":
            return subprocess.CompletedProcess(lenh, 1, stdout="", stderr="not logged in\n")
        return subprocess.CompletedProcess(lenh, 0, stdout="1.1.17", stderr="")
    m._chay_van_ban_an_toan = gia_hong
    m.subprocess.run = gia_hong
    m.CONG_CU = []
    rc2, d2 = _doctor_json(m, doi_kha_dung=True)
    kn2 = [k for k in d2["kha_nang"] if k.get("ten") == "antigravity"]
    bang(len(kn2) == 1 and kn2[0].get("trang_thai") == "CO_MAT",
         f"luot doctor sau phai do lai, khong doc anh chup luot truoc: {kn2}")
    bang(rc2 == m.MA_CHUA_XAC_THUC,
         f"--doi-kha-dung voi antigravity CO_MAT phai thoat {m.MA_CHUA_XAC_THUC}: rc2={rc2}")


@ca
def t149_doctor_do_actionlint_va_shellcheck():
    """A1 / M1: doctor đo actionlint và shellcheck, không tính vào DUNG_DUOC."""
    m = _tai_launcher_thu()
    al = [c for c in m.CONG_CU if c.get("ten") == "actionlint"]
    sc = [c for c in m.CONG_CU if c.get("ten") == "shellcheck"]
    bang(len(al) == 1 and len(sc) == 1 and al[0]["bat_buoc"] is False and sc[0]["bat_buoc"] is False, "M1: tool co mat va khong bat buoc")
    bang(m.DA_CHUNG_MINH_KHA_DUNG == frozenset({"DUNG_DUOC"}), "DA_CHUNG_MINH_KHA_DUNG chi chua DUNG_DUOC")
    # Ca am: thieu tool tuy chon van thoat 0
    m.CONG_CU, m.MODULE_PY, m.KHA_NANG = [dict(al[0]), dict(sc[0])], [], []
    m._cac_duong_dan = lambda _c, _e: []
    rc, d = _doctor_json(m)
    cc = {c["ten"]: c for c in d["cong_cu"]}
    bang(rc == 0 and cc["actionlint"]["co"] is False and bool(cc["actionlint"].get("lenh_cai")), "ca am actionlint co=False co lenh_cai")
    bang(cc["shellcheck"]["co"] is False, "ca am shellcheck co=False")
    # Ca duong: co tool tren PATH
    m._cac_duong_dan = lambda c, _e: [(c["ten"], f"/bin/{c['ten']}")]
    m._phien_ban = lambda d, **kw: (True, "1.7.7" if "actionlint" in d else "0.10.0", False)
    _, d2 = _doctor_json(m)
    cc2 = {c["ten"]: c for c in d2["cong_cu"]}
    bang(cc2["actionlint"]["co"] is True and cc2["actionlint"]["phien_ban"] == "1.7.7", "ca duong actionlint co=True ban 1.7.7")
    bang(cc2["shellcheck"]["co"] is True, "ca duong shellcheck co=True")


@ca
def t150_doctor_do_bien_utf8_in_ca_khi_xanh():
    """A2 / M2: doctor đo hai biến UTF-8, in ra KỂ CẢ KHI XANH, cảnh báo khi thiếu."""
    m = _tai_launcher_thu()
    m.CONG_CU, m.MODULE_PY, m.KHA_NANG = [], [], []
    in_dong = []
    goc_in = m._in_an_toan
    m._in_an_toan = lambda msg="": in_dong.append(msg)
    m._doc_moi_truong = lambda: ({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}, {})
    rc = m.lenh_doctor(argparse.Namespace(json=False, workspace=None, kiem_song=False, doi_kha_dung=False))
    bang(rc == 0 and "BIEN UTF-8" in "\n".join(in_dong) and not any("CANH BAO" in d and "UTF-8" in d for d in in_dong), "xanh in du khong canh bao")
    in_dong.clear()
    m._doc_moi_truong = lambda: ({"PYTHONIOENCODING": "utf-8"}, {})
    rc_v = m.lenh_doctor(argparse.Namespace(json=False, workspace=None, kiem_song=False, doi_kha_dung=False))
    bang(rc_v == 0 and any("CANH BAO" in d and "UTF-8" in d for d in in_dong), "thieu phai canh bao")
    m._in_an_toan = goc_in
    bang("bien_utf8" in _doctor_json(m)[1], "json phai co bien_utf8")


@ca
def t151_m3_phan_biet_da_chay_voi_tep_moi():
    """A3 / M3: phân biệt ĐÃ CHẠY với TỆP MỚI; phân biệt cuc_bo và remote."""
    m = _tai_launcher_thu()
    MASTER = "#!/bin/bash\n# hook-nang-luc: codex-auth-restore\necho hi\n"
    with San() as s:
        cay = s / "cay_test"
        (cay / ".claude" / "hooks").mkdir(parents=True)
        (cay / ".claude" / "hooks" / "session-start.sh").write_text(MASTER, encoding="utf-8")
        m._git = lambda ws, *a: ((0, MASTER, "") if "session-start.sh" in a[-1] else (1, "", ""))
        tt_h, _ = m._do_hook_cu(str(cay))
        tt_c, mo_ta_c = m._do_hook_da_chay(str(cay))
        bang(tt_h == "DUNG_DUOC" and tt_c == "CHUA_CHAY" and "CHƯA CHẠY" in mo_ta_c, f"ca (a) CHUA_CHAY: {tt_c}")
        vd = cay / ".claude" / ".packet_state"
        vd.mkdir(parents=True)
        (vd / "session-start.ran").write_text("2026-09-17T00:00:00Z cuc_bo\n", encoding="utf-8")
        bang(m._do_hook_da_chay(str(cay))[0] == "DA_CHAY" and "bo qua theo thiet ke" in m._do_hook_da_chay(str(cay))[1], "ca (b) cuc_bo DA_CHAY")
        (vd / "session-start.ran").write_text("2026-09-17T00:00:00Z remote\n", encoding="utf-8")
        bang(m._do_hook_da_chay(str(cay))[0] == "DA_CHAY" and "bo qua" not in m._do_hook_da_chay(str(cay))[1], "ca (c) remote DA_CHAY")
        tt_kws, _ = m._do_hook_da_chay(None)
        bang(tt_kws == "KHONG_DO_DUOC", f"None ws phai KHONG_DO_DUOC: {tt_kws}")
        # Lop 4: hook-da-chay DA_CHAY khong vao chua_chung_minh; CHUA_CHAY thi vao
        m.CONG_CU, m.MODULE_PY = [], []
        m.KHA_NANG = [{"ten": "hook-da-chay", "do": lambda *_: ("DA_CHAY", "da chay"), "vi_sao": ""}]
        bang("hook-da-chay" not in _doctor_json(m)[1]["chua_chung_minh"], "DA_CHAY khong vao chua_chung_minh")
        m.KHA_NANG = [{"ten": "hook-da-chay", "do": lambda *_: ("CHUA_CHAY", "chua chay"), "vi_sao": ""}]
        bang("hook-da-chay" in _doctor_json(m)[1]["chua_chung_minh"], "CHUA_CHAY phai vao chua_chung_minh")


@ca
def t152_hook_cai_dat_va_khop_al_ver_ci():
    """A4 / M4: hook cài actionlint, export UTF-8; khóa giới hạn tiến trình con không đổi biến ở cha."""
    goc = Path(__file__).resolve().parents[2]
    hook_path = goc / ".claude" / "hooks" / "session-start.sh"
    hook_txt = hook_path.read_text(encoding="utf-8", errors="replace")
    ci_txt = (goc / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8", errors="replace")
    m_hook = re.search(r'^\s*AL_VER=["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?', hook_txt, re.MULTILINE)
    bang(bool(m_hook), f"hook phai ghim AL_VER: {hook_txt[:200]}")
    al_ver = m_hook.group(1)
    ci_vers = re.findall(r'^\s*AL_VER:\s*([0-9]+\.[0-9]+\.[0-9]+)', ci_txt, re.MULTILINE)
    # #668: cho thu 5 la job `gate-cong-cu` (8 manh ban kinh dot bien cua cong_cu_test can actionlint that).
    bang(len(ci_vers) == 5 and all(v == al_ver for v in ci_vers), f"ci.yml 5 cho phai khop {al_ver}: {ci_vers}")
    bang("PYTHONUTF8=1" in hook_txt and "PYTHONIOENCODING=utf-8" in hook_txt, "hook phai export UTF-8")
    bang("cai_actionlint.sh" in hook_txt and "CANH BAO" in hook_txt, "hook phai co cai_actionlint va CANH BAO")
    # Lop 2: Do hanh vi gioi han tien trinh — hook chay nhu con khong doi duoc bien o cha
    bash = (shutil.which("bash") if not LA_WINDOWS else
            ("C:/Program Files/Git/bin/bash.exe" if Path("C:/Program Files/Git/bin/bash.exe").exists() else shutil.which("bash")))
    if bash:
        p = subprocess.run([bash, "-c", f"unset PYTHONUTF8; '{hook_path.as_posix()}' >/dev/null 2>&1 || true; echo -n \"${{PYTHONUTF8:-<chua dat>}}\""],
                           capture_output=True, text=True)
        bang(p.stdout == "<chua dat>", f"tien trinh cha phai <chua dat>: {p.stdout}")


@ca
def t153_doctor_do_duong_dan_kho_co_dau_cach_hoac_phi_ascii():
    """A5 / M5: doctor ĐO đường dẫn kho: có dấu cách hoặc ngoài ASCII thì nêu ra; âm thì không."""
    m = _tai_launcher_thu()
    for d, sub in [("/duong dan/kho", "dau cach"), ("/duong_dan/\u0111\u1ed9/kho", "ky tu ngoai ASCII"),
                  ("D:/Qu\u1ed1c h\u1ed9i/tra-luat", "dau cach")]:
        co, mo = m._kiem_tra_duong_dan_kho(d)
        bang(co is True and sub in mo and "6 ca da biet se do" in mo, f"phai canh bao cho {d}: {mo}")
    co4, mo4 = m._kiem_tra_duong_dan_kho("/opt/tra-luat/repo_pure_ascii")
    co5, mo5 = m._kiem_tra_duong_dan_kho(None)
    bang(co4 is False and mo4 == "" and co5 is False and mo5 == "", "ca am va None ws phai False, ''")


@ca
def t154_m3_dau_vet_CU_KHONG_con_la_DA_CHAY():
    """M3 / Lop 1: dau vet CU hon nguong => KHONG_DO_DUOC, khong phai DA_CHAY."""
    m = _tai_launcher_thu()
    MASTER = "#!/bin/bash\n# hook-nang-luc: codex-auth-restore\necho hi\n"
    with San() as s:
        cay = s / "cay_tuoi"
        (cay / ".claude" / "hooks").mkdir(parents=True)
        (cay / ".claude" / "hooks" / "session-start.sh").write_text(MASTER, encoding="utf-8")
        vd = cay / ".claude" / ".packet_state"
        vd.mkdir(parents=True)
        vet = vd / "session-start.ran"
        vet.write_text("2026-08-17T00:00:00Z\n", encoding="utf-8")
        gio = vet.stat().st_mtime
        # Ca (a): dau vet TUOI => DA_CHAY
        tt_a, _ = m._do_hook_da_chay(str(cay), bay_gio=gio + 60)
        bang(tt_a == "DA_CHAY", f"dau vet tuoi phai DA_CHAY: {tt_a}")
        # Ca (b): dau vet CU hon nguong => KHONG_DO_DUOC
        tt_b, mo_b = m._do_hook_da_chay(str(cay), bay_gio=gio + m._HAN_DAU_VET_HOOK_GIAY + 60)
        bang(tt_b == "KHONG_DO_DUOC" and "KHÔNG ĐO ĐƯỢC" in mo_b, f"dau vet CU phai KHONG_DO_DUOC: {tt_b} · {mo_b}")
        # Ca (c): khong dau vet => CHUA_CHAY
        vet.unlink()
        tt_c, _ = m._do_hook_da_chay(str(cay), bay_gio=gio)
        bang(tt_c == "CHUA_CHAY", f"khong dau vet phai CHUA_CHAY: {tt_c}")


@ca
def t155_m3_hook_cuc_bo_ghi_dau_vet_truoc_cong_remote():
    """Lop 8: hook cuc bo (khong co CLAUDE_CODE_REMOTE) phai ghi dau vet cuc_bo truoc khi thoat o cong."""
    goc = Path(__file__).resolve().parents[2]
    hook_path = goc / ".claude" / "hooks" / "session-start.sh"
    bash = (shutil.which("bash") if not LA_WINDOWS else
            ("C:/Program Files/Git/bin/bash.exe" if Path("C:/Program Files/Git/bin/bash.exe").exists() else shutil.which("bash")))
    if not bash:
        return "bo qua vi khong co bash"
    with San() as s:
        p = subprocess.run(
            [bash, "-c", f"unset CLAUDE_CODE_REMOTE; CLAUDE_PROJECT_DIR='{s.as_posix()}' '{hook_path.as_posix()}' >/dev/null 2>&1 || true"],
            capture_output=True, text=True)
        vet = s / ".claude" / ".packet_state" / "session-start.ran"
        bang(vet.is_file(), "Lop 8: hook cuc bo phai ghi dau vet truoc khi thoat")
        truong = vet.read_text(encoding="utf-8").strip().split()
        bang(len(truong) >= 2 and truong[1] == "cuc_bo", f"Lop 8: dau vet phai mang nhan cuc_bo, thuc te: {truong}")


def _r1079_run_json(rr, ngu_canh=""):
    """#1079 F01: sổ `run.json` vắng là ĐỎ do chốt, không phải FileNotFoundError vô can."""
    ds = sorted(rr.iterdir()) if rr.is_dir() else []
    bang(len(ds) == 1 and (ds[0] / "run.json").is_file(), f"khong ghi so run.json: {ds} {ngu_canh}")
    return json.loads((ds[0] / "run.json").read_text(encoding="utf-8"))


@ca
def r01_worktree_that_bi_chan():
    with San() as s:
        wt = tao_worktree(s); dau = s / "da-chay"; rr = s / "runs"
        r = chay("run", "--workspace", str(wt), "--run-root", str(rr), "--",
                 PY, "-c", f"open({str(dau)!r},'w').write('x')")
        bang(r.returncode == MA_WORKTREE and "clone doc lap" in r.stderr,
             f"worktree khong bi chan dung cach: {r.returncode} {r.stderr}")
        bang(not dau.exists(), "lenh con da chay trong worktree")
        d = _r1079_run_json(rr)
        bang(d["trang_thai"] == "hong" and d.get("giai_doan") == "probe"
             and d["ma_thoat"] == MA_WORKTREE and d["probe"]["workspace"]["trang_thai"] == "DO"
             and "worktree" in d["ly_do_dung"], f"chan probe khong vao so: {d}")


@ca
def r02_clone_that_di_tiep():
    with San() as s:
        repo = tao_repo(s); dau = s / "da-chay"; rr = s / "runs"
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr), "--",
                 PY, "-c", f"open({str(dau)!r},'w').write('x')")
        bang(r.returncode == 0 and dau.is_file() and (next(rr.iterdir()) / "run.json").is_file(),
             f"clone that bi bat oan: {r.returncode} {r.stderr}")


@ca
def r03_probe_ghi_bi_tu_choi_thi_do():
    m = _tai_launcher_thu(); goc = m.tempfile.NamedTemporaryFile
    m.tempfile.NamedTemporaryFile = lambda *a, **k: (_ for _ in ()).throw(PermissionError("RO"))
    try:
        kq = m._probe_ghi(".")
    finally:
        m.tempfile.NamedTemporaryFile = goc
    bang(kq["trang_thai"] == "DO", f"backend chi-doc khong lam probe DO: {kq}")


@ca
def r04_spawn_rc0_dau_ra_rong_bi_chan():
    m = _tai_launcher_thu(); goc = m._chay_van_ban_an_toan
    m._chay_van_ban_an_toan = lambda *a, **k: subprocess.CompletedProcess(a[0], 0, "", "")
    try:
        kq = m._probe_spawn("gia", ".")
    finally:
        m._chay_van_ban_an_toan = goc
    bang(kq["trang_thai"] == "DO", f"rc=0 rong bi coi la DAT: {kq}")


@ca
def r05_trust_thieu_khoa_la_khong_do_duoc():
    m = _tai_launcher_thu()
    with San() as s:
        repo = s / "repo"; repo.mkdir(); home = s / "home"; home.mkdir()
        (home / ".claude.json").write_text("[]", encoding="utf-8")
        kq = m._probe_trust_claude(str(repo), home)
        bang(kq["trang_thai"] == "KHONG_DO_DUOC", f"JSON sai dang lam probe thoat: {kq}")
        (home / ".claude.json").write_text(json.dumps({"projects": {str(repo.resolve()): {}}}),
                                            encoding="utf-8")
        kq = m._probe_trust_claude(str(repo), home)
        bang(kq["trang_thai"] == "KHONG_DO_DUOC", f"thieu khoa trust bi coi la DAT: {kq}")


@ca
def r06_probe_hong_khong_override_phai_chan():
    with San() as s:
        repo = tao_repo(s); claude = tao_claude_gia(s); home = s / "home"; home.mkdir()
        dau = s / "da-chay"; env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
        r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"), "--",
                 str(claude), "-c", f"open({str(dau)!r},'w').write('x')", env=env)
        bang(r.returncode == MA_PROBE and not dau.exists(),
             f"probe hong van cho lenh chay: {r.returncode} {r.stderr}")


@ca
def r07_override_ly_do_rong_bi_tu_choi():
    with San() as s:
        repo = tao_repo(s)
        r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"),
                 "--bo-qua-probe", "", "--", PY, "-c", "pass")
        bang(r.returncode == MA_THAM_SO, f"ly do rong van duoc nhan: {r.returncode}")


@ca
def r08_override_co_ly_do_duoc_ghi_so():
    with San() as s:
        wt = tao_worktree(s); rr = s / "runs"; ly_do = "human cho phep do lai sau"
        r = chay("run", "--workspace", str(wt), "--run-root", str(rr),
                 "--bo-qua-probe", ly_do, "--", PY, "-c", "pass")
        d = json.loads((next(rr.iterdir()) / "run.json").read_text(encoding="utf-8"))
        bang(r.returncode == 0 and d.get("bo_qua_probe_ly_do") == ly_do,
             f"override khong vao so: {r.returncode} {d}")


@ca
def r09_run_json_giu_ba_trang_thai_probe():
    with San() as s:
        wt = tao_worktree(s); rr = s / "runs"; claude = tao_claude_gia(s)
        home = s / "home"; home.mkdir()
        (home / ".claude.json").write_text(json.dumps({"projects": {str(wt.resolve()): {}}}),
                                            encoding="utf-8")
        env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
        r = chay("run", "--workspace", str(wt), "--run-root", str(rr),
                 "--bo-qua-probe", "fixture", "--", str(claude), "-c", "pass", env=env)
        d = json.loads((next(rr.iterdir()) / "run.json").read_text(encoding="utf-8"))
        trang_thai = {x["trang_thai"] for x in d["probe"].values()}
        bang(r.returncode == 0 and trang_thai == {"DAT", "DO", "KHONG_DO_DUOC"},
             f"run.json khong giu ba trang thai: {trang_thai}")


@ca
def r10_trust_json_hong_bi_chan_sach():
    with San() as s:
        repo = tao_repo(s); claude = tao_claude_gia(s); home = s / "home"; home.mkdir()
        dau = s / "da-chay"; rr = s / "runs"
        (home / ".claude.json").write_text("{", encoding="utf-8")
        env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr), "--",
                 str(claude), "-c", f"open({str(dau)!r},'w').write('x')", env=env)
        d = _r1079_run_json(rr, f"rc={r.returncode} {r.stderr[-300:]}")
        bang(r.returncode == MA_PROBE and not dau.exists() and "Traceback" not in r.stderr
             and d["probe"]["claude_trust"]["trang_thai"] == "KHONG_DO_DUOC",
             f"JSON hong khong bi chan sach: {r.returncode} {r.stderr} {d}")


@ca
def r11_trust_gia_tri_that_ba_chieu():
    m = _tai_launcher_thu()
    with San() as s:
        repo = s / "repo"; repo.mkdir(); home = s / "home"; home.mkdir()
        tep = home / ".claude.json"
        for gia_tri, mong in ((True, "DAT"), (False, "DO"), (1, "KHONG_DO_DUOC")):
            tep.write_text(json.dumps({"projects": {str(repo.resolve()):
                           {"hasTrustDialogAccepted": gia_tri}}}), encoding="utf-8")
            kq = m._probe_trust_claude(str(repo), home)
            bang(kq["trang_thai"] == mong, f"trust={gia_tri!r}: {kq}")


@ca
def r12_prompt_doi_ngay_sau_preflight_phai_DO():
    """Đổi nguồn đúng sau preflight phải bị re-hash chặn trước khi sinh con."""
    m = _tai_launcher_thu()
    with San() as s:
        repo = tao_repo(s); prompt = s / "prompt.txt"; dau = s / "con-da-chay"
        prompt.write_text("PROMPT GOC", encoding="utf-8")
        sha = hashlib.sha256(prompt.read_bytes()).hexdigest()
        a = m.build_parser().parse_args([
            "run", "--workspace", str(repo), "--run-root", str(s / "runs"),
            "--prompt-file", str(prompt), "--expected-prompt-sha256", sha,
            "--", PY, "-c", f"open({str(dau)!r},'w').write('x')",
        ])
        a.lenh = a.lenh[1:]
        goc = m.chay_cac_probe

        def doi_sau_preflight(*_a, **_k):
            prompt.write_text("PROMPT DOI", encoding="utf-8")
            return {}, None

        m.chay_cac_probe = doi_sau_preflight
        try:
            try:
                m.lenh_run(a)
            except m.Chan as e:
                bang(e.ma == MA_PROMPT, f"doi prompt bi chan sai ma: {e.ma}")
            else:
                bang(False, "doi prompt sau preflight van sinh con")
        finally:
            m.chay_cac_probe = goc
        bang(not dau.exists(), "con da chay du prompt bi doi")


@ca
def r13_PROMPT_FILE_thieu_prompt_file_phai_DO():
    # #1079 F05: gọi HELPER chung, không gọi ca đã đăng ký khác (chốt của ca khác không phải chốt của ca này).
    return _t70_prompt_file_chan()


@ca
def r14_run_json_bam_lai_dung_hai_log():
    with San() as s:
        repo = tao_repo(s); rr = s / "runs"
        ma = ("import sys;sys.stdout.buffer.write(b'OUT\\x00BYTE');"
              "sys.stderr.buffer.write(b'ERR\\nBYTE')")
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--", PY, "-c", ma)
        tm = next(p for p in rr.iterdir() if p.is_dir())
        d = json.loads((tm / "run.json").read_text(encoding="utf-8"))
        for ten in ("stdout", "stderr"):
            raw = (tm / f"{ten}.log").read_bytes()
            bang(d[f"{ten}_byte"] == len(raw), f"kich thuoc {ten} lech")
            bang(d[f"{ten}_sha256"] == hashlib.sha256(raw).hexdigest(),
                 f"bam {ten} khong phai bam byte tren dia")
        bang(r.returncode == 0, f"launcher rc={r.returncode}: {r.stderr}")


@ca
def r15_moi_provider_chi_mot_transport_va_hai_luot_on_dinh():
    with San() as s:
        repo = tao_repo(s); cli = s / ("codex.exe" if LA_WINDOWS else "codex")
        try:
            os.link(Path(PY).resolve(), cli)
        except OSError:
            shutil.copy2(Path(PY).resolve(), cli)
        if not LA_WINDOWS:
            cli.chmod(0o755)
        ds = []
        for i in range(2):
            rr = s / f"runs-{i}"
            r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                     "--", str(cli), "-c", "pass")
            bang(r.returncode == 0, f"luot {i} rc={r.returncode}: {r.stderr}")
            ds.append(json.loads((next(rr.iterdir()) / "run.json").read_text(encoding="utf-8")))
        contract = [(d["provider"], d["execution_surface"], d["transport"],
                     d["transport_sha256"]) for d in ds]
        bang(contract[0] == contract[1], f"cung provider ma transport troi: {contract}")
        bang(contract[0][:3] == ("openai_codex", "codex_cli", "machine"),
             f"nhan sai contract codex: {contract[0]}")
        bang(bool(re.fullmatch(r"[0-9a-f]{64}", contract[0][3])), "bam transport sai dang")


# wp748 r25 (#748 issuecomment-6378484722): model do MÁY CHỦ trả cho từng response của lượt codex. Con GIẢ là
# chính trình python đặt tên `codex` (như r15), in ra stderr đúng dạng log trace của codex-cli 0.163.0. Chuỗi bí mật
# là chuỗi MẪU, không phải credential thật.
_R25_BI_MAT = "Bearer r25-bi-mat-mau-KHONG-duoc-cham-dia"
_R25_DONG_GIU = "Reading additional input from stdin...\n"
_R25_KHUNG_THUA = "2026-10-24T01:12:05.000001Z  INFO codex: dong info sau dau hieu log\n"


def _r25_khung(loai, rid, model, target="tungstenite::protocol", truoc=""):
    ev = {"type": loai, "sequence_number": 0, "response": {"id": rid, "object": "response", "model": model}}
    return f"2026-10-24T01:12:06.199773Z TRACE {target}: {truoc}Received message {json.dumps(ev)}\n"


def _r25_codex_gia(s):
    cli = s / ("codex.exe" if LA_WINDOWS else "codex")
    try:
        os.link(Path(PY).resolve(), cli)
    except OSError:
        shutil.copy2(Path(PY).resolve(), cli)
    if not LA_WINDOWS:
        cli.chmod(0o755)
    return cli


def _r25_chay(s, noi_dung_err, sau="", them=(), env=None):
    repo = tao_repo(s); cli = _r25_codex_gia(s); rr = s / "runs"
    ma = ("import os,sys,time;print(os.environ.get('RUST_LOG',''));"
          f"sys.stderr.buffer.write({noi_dung_err.encode()!r});sys.stderr.buffer.flush();{sau}")
    # byte THÔ như codex (Rust) ghi: sys.stderr.write ở chế độ văn bản đổi \n -> \r\n trên Windows (đo: lane
    # Windows run 40082998930 đỏ đúng phép so byte stderr.log, còn bộ lọc vẫn chặn đủ dòng trace)
    r = chay("run", "--workspace", str(repo), "--run-root", str(rr), *them, "--", str(cli), "-c", ma, "-m", "gpt-mau",
             env=env)
    tm = next(p for p in rr.iterdir() if p.is_dir())
    return r, tm, json.loads((tm / "run.json").read_text(encoding="utf-8"))


def _r25_loc(m, du_lieu: bytes):
    import io
    f, ket, loi, dem = io.BytesIO(), [], [], {}
    m._loc_stderr_codex(io.BytesIO(du_lieu), f, ket, loi, dem)
    return f.getvalue(), ket, loi, dem


@ca
def r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat():
    err = (_R25_DONG_GIU
           + f"2026-10-24T01:12:05.5Z TRACE tungstenite::protocol: authorization: {_R25_BI_MAT}\n"
           + f"    noi tiep cua dong trace: {_R25_BI_MAT}\n"
           + _r25_khung("response.created", "resp_1", "gpt-6-astra")
           + _r25_khung("response.completed", "resp_1", "gpt-6-astra")
           + f"2026-10-24T01:12:07Z DEBUG codex_core: {_R25_BI_MAT}\n"
           + _r25_khung("response.completed", "resp_2", "gpt-6-luna")
           + _r25_khung("response.completed", "resp_3", "gpt-6-astra")
           + f"2026-10-24T01:12:08Z  WARN codex: {_R25_BI_MAT}\n")
    with San() as s:
        r, tm, d = _r25_chay(s, err)
        bang(r.returncode == 0, f"launcher rc={r.returncode}: {r.stderr}")
        bang(d.get("model_phuc_vu_trang_thai") == "DO_DUOC", f"trang thai sai: {d.get('model_phuc_vu_trang_thai')}")
        bang([(m["response_id"], m["model"], m["su_kien"]) for m in d.get("model_phuc_vu", [])] == [
            ("resp_1", "gpt-6-astra", "response.created"), ("resp_2", "gpt-6-luna", "response.completed"),
            ("resp_3", "gpt-6-astra", "response.completed")], f"model_phuc_vu sai: {d.get('model_phuc_vu')}")
        bang((tm / "stderr.log").read_bytes() == _R25_DONG_GIU.encode(),
             f"stderr.log phai chi co dong trong danh sach cho phep: {(tm / 'stderr.log').read_bytes()!r}")
        bang(d.get("stderr_bo_dong") == 8 and d.get("stderr_bo_byte") == len(err.encode()) - len(_R25_DONG_GIU),
             f"so dem phan bi bo sai: {d.get('stderr_bo_dong')} {d.get('stderr_bo_byte')}")
        bang((tm / "stdout.log").read_text(encoding="utf-8").splitlines()[0] == "tungstenite::protocol=trace",
             "con khong duoc bat dung target trace")
        lo = [str(p) for p in tm.rglob("*") if p.is_file() and b"r25-bi-mat-mau" in p.read_bytes()]
        bang(not lo, f"chuoi bi mat cham dia: {lo}")


@ca
def r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace():
    # R25-SEC-01 vong 2: dong KHONG nhan ra la trace dung TRUOC dau hieu log van tung cham dia
    m = _tai_launcher_thu()
    cho = _R25_DONG_GIU.encode()
    bi = _R25_BI_MAT.encode()
    for ten, du in [
        ("dong_thuong_mang_bi_mat", b"loi gi do " + bi + b"\n"),
        ("byte_khong_utf8", b"\xff\xfe\n"),
        ("chi_CR", b"abc\r"),
        ("dong_cho_phep_cut_o_EOF", cho.rstrip(b"\n")),
        ("dong_cho_phep_them_hau_to", cho.rstrip(b"\n") + b" " + bi + b"\n"),
        ("dong_cho_phep_them_tien_to", bi + cho),
    ]:
        ghi, _, loi, dem = _r25_loc(m, du)
        bang(ghi == b"" and not loi and dem.get("byte_bo") == len(du), f"{ten}: dong ngoai danh sach cham dia: {ghi!r}")
    ghi, _, _, _ = _r25_loc(m, _r25_khung("response.created", "r", "m").encode() + cho)
    bang(ghi == cho, f"dong cho phep sau trace bi mat: {ghi!r}")


@ca
def r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien():
    m = _tai_launcher_thu()
    ansi = ("\x1b[2m2026-10-24T01:12:06.1Z\x1b[0m \x1b[35mTRACE\x1b[0m tungstenite::protocol: Received message "
            + json.dumps({"type": "response.created", "response": {"id": "ra", "model": "ma"}}) + "\n")
    du = "".join([
        _r25_khung("response.created", "x1", "gia", target="codex_core"),
        _r25_khung("response.created", "x2", "gia", truoc="echo "),
        _r25_khung("response.output_text.delta", "x3", "gia"),
        ansi,
        _r25_khung("response.created", "rb", "m1"),
        _r25_khung("response.completed", "rb", "m2"),
    ]).encode()
    _, ket, loi, dem = _r25_loc(m, du)
    bang(not loi and [(k["response_id"], k["model"]) for k in ket] == [("ra", "ma"), ("rb", "m1"), ("rb", "m2")],
         f"khung ghi sai nguon/su kien/khu trung: {ket}")
    bang(dem.get("mat") == 2, f"khung created/completed sai nguon phai tinh la MAT: {dem}")
    for ten, rid, mdl in [("id_rong", "", "m"), ("model_khoang_trang", "r", "  ")]:
        _, ket, _, dem = _r25_loc(m, _r25_khung("response.created", rid, mdl).encode())
        bang(not ket and dem.get("mat") == 1, f"{ten}: khung rong van duoc nhan hoac khong tinh mat: {ket} {dem}")


@ca
def r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han():
    m = _tai_launcher_thu()
    m._TRAN_DONG = 64
    import io

    class _Ong(io.BytesIO):
        kich_thuoc = []

        def readline(self, n=-1):
            self.kich_thuoc.append(n)
            return super().readline(n)

    dai = b"x" * 200 + b"\n"
    ong = _Ong(_R25_DONG_GIU.encode() + dai + b"sau\n" + _r25_khung("response.created", "r" * 80, "m").encode())
    f, ket, loi, dem = io.BytesIO(), [], [], {}
    m._loc_stderr_codex(ong, f, ket, loi, dem)
    bang(f.getvalue() == _R25_DONG_GIU.encode(), f"dong vuot tran (hoac phan sau no) lot ra dia: {f.getvalue()!r}")
    bang(not ket and dem.get("mat", 0) >= 1, f"khung vuot tran van duoc parse hoac khong tinh mat: {ket} {dem}")
    bang(_Ong.kich_thuoc and all(n == 64 for n in _Ong.kich_thuoc), f"doc khong gioi han: {_Ong.kich_thuoc}")


@ca
def r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat():
    m = _tai_launcher_thu()
    khung = _r25_khung("response.created", "rk", "mk").encode()
    _, ket, _, dem = _r25_loc(m, khung.rstrip(b"\n"))
    bang(not ket and dem.get("mat") == 1, f"khung cut o EOF van duoc nhan: {ket} {dem}")
    m._TRAN_DONG = 256
    _, ket, _, dem = _r25_loc(m, b"x" * 256 + khung)
    bang(not ket and dem.get("mat") == 1, f"khung o doan doc giua dong van duoc nhan: {ket} {dem}")


@ca
def r925_bo_loc_hong_xa_ong_co_gioi_han():
    import io
    m = _tai_launcher_thu()
    m._TRAN_DONG = 32

    class _Ong(io.BytesIO):
        lan = 0
        kich_thuoc = []

        def readline(self, n=-1):
            self.lan += 1
            if self.lan > 1:
                raise RuntimeError("ong hong")
            return super().readline(n)

        def read(self, n=-1):
            self.kich_thuoc.append(n)
            return super().read(n)

    ong = _Ong(_R25_DONG_GIU.encode() + b"y" * 100)
    loi = []
    m._loc_stderr_codex(ong, io.BytesIO(), [], loi, {})
    bang(loi == ["RuntimeError"] and ong.read() == b"", f"khong xa het ong sau khi hong: {loi}")
    bang(_Ong.kich_thuoc[:-1] and all(n == 32 for n in _Ong.kich_thuoc[:-1]),
         f"xa ong khong gioi han: {_Ong.kich_thuoc}")


@ca
def r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai():
    import io
    m = _tai_launcher_thu()

    class _OngHong(io.BytesIO):
        def readline(self, n=-1):
            if self.tell():
                raise RuntimeError("ong hong")
            return super().readline(n)

    for ten, ong, mong in [
        ("loi_sau_khung", _OngHong(_r25_khung("response.created", "r1", "m1").encode() + b"sau\n"), "hong"),
        ("mat_sau_khung", io.BytesIO(_r25_khung("response.created", "r1", "m1").encode()
                                     + _r25_khung("response.completed", "", "m1").encode()), "khong doc duoc"),
    ]:
        ban_ghi = {}
        bo = m._BoLocStderr(ong, io.BytesIO())
        bo.bat_dau(); bo.ket_thuc(10)
        bo.ghi_so(ban_ghi)
        bang(ban_ghi.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC"
             and mong in (ban_ghi.get("model_phuc_vu_ly_do") or "")
             and [x["response_id"] for x in ban_ghi.get("model_phuc_vu", [])] == ["r1"], f"{ten}: {ban_ghi}")


@ca
def r925_ghi_ket_qua_chot_luong_TRUOC_roi_moi_chup():
    m = _tai_launcher_thu()
    a_ = {"response_id": "ra", "model": "m", "su_kien": "response.created"}
    b_ = {"response_id": "rb", "model": "m", "su_kien": "response.completed"}
    bo = m._BoLocStderr(None, io.BytesIO())
    bo.ket.append(a_)

    class _Luong:
        ident = 1                # luồng đã chạy

        def join(self, timeout=None):
            pass

        def is_alive(self):
            bo.ket.append(b_)    # luong doc xong DUNG luc bi hoi
            return False

    bo.luong = _Luong()
    ban_ghi = {}
    bo.ket_thuc(10); bo.ghi_so(ban_ghi)
    bang(ban_ghi.get("model_phuc_vu") == [a_, b_] and ban_ghi.get("model_phuc_vu_trang_thai") == "DO_DUOC",
         f"so ghi danh sach khac voi danh sach da ket luan: {ban_ghi}")


# wp748 r26 (cross-review r26a): mỗi phát hiện một ca, mỗi ca một đột biến riêng ở bảng DOT_BIEN.
@ca
def r926_chot_trang_thai_luong_O_RANH_GIOI_cho_khong_lay_mau_lai():
    # R26-EOF-10: luồng còn đọc lúc hết hạn chờ rồi mới xong SAU ĐÓ (sau khi tệp đã đóng) — sổ vẫn phải ghi
    # "ống còn mở", vì phần đọc muộn không còn chỗ ghi đúng.
    m = _tai_launcher_thu()
    bo = m._BoLocStderr(None, io.BytesIO())
    trang = {"song": True}

    class _Luong:
        ident = 1                # luồng đã chạy

        def join(self, timeout=None):
            pass

        def is_alive(self):
            return trang["song"]

    bo.luong = _Luong()
    bo.ket_thuc(10)
    trang["song"] = False                       # đọc xong muộn
    bo.ket.append({"response_id": "r", "model": "m", "su_kien": "response.created"})
    ban_ghi = {}
    bo.ghi_so(ban_ghi)
    bang(ban_ghi.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC"
         and "con mo" in (ban_ghi.get("model_phuc_vu_ly_do") or ""),
         f"lay mau lai trang thai luong sau ranh gioi cho: {ban_ghi}")


@ca
def r926_dong_NHAN_cat_nhieu_doan_ma_token_roi_cho_cat_van_tinh_mat():
    # R25-EVID-05 tiếp: token `"type"` rơi đúng chỗ cắt đoạn đọc nên không đoạn nào khớp _RE_UNG_VIEN.
    m = _tai_launcher_thu()
    m._TRAN_DONG = 128
    dau = b"2026-10-24T01:12:06.199773Z TRACE tungstenite::protocol: Received message "
    tok = b'"type":"response.created"'
    dem_lap = 128 - len(dau) - len(b'{"x":"') - len(b'","') - 5
    khung = dau + b'{"x":"' + b"p" * dem_lap + b'","' + tok + b',"response":{"id":"r","model":"m"}}' + b"\n"
    vi_tri = khung.index(tok)
    bang(vi_tri < 128 < vi_tri + len(tok), f"fixture sai: token khong vat qua cho cat ({vi_tri})")
    _, ket, loi, dem = _r25_loc(m, khung)
    bang(not ket and not loi and dem.get("mat", 0) >= 1, f"dong nhan cat nhieu doan khong tinh mat: {ket} {dem}")
    for ten, du in [("dong_dai_khong_header", b"x" * 300 + b"\n"),
                    ("header_giua_dong", b"x" * 128 + dau + b"q" * 300 + b"\n"),
                    ("khung_tron_su_kien_khac", _r25_khung("response.output_text.delta", "r", "m").encode())]:
        m._TRAN_DONG = 4096 if ten == "khung_tron_su_kien_khac" else 128   # khung ấy dài hơn 128: phải TRỌN một đoạn
        _, ket, _, dem = _r25_loc(m, du)
        bang(not dem.get("mat") and not dem.get("khong_ro"), f"{ten}: dong khong phai khung nhan bi tinh mat/khong ro: {dem}")


@ca
def r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat():
    m = _tai_launcher_thu()
    khung = _r25_khung("response.created", "r", "MODELX").encode().replace(b"MODELX", b"m" + bytes([0xFF]))
    _, ket, loi, dem = _r25_loc(m, khung)
    bang(not ket and not loi and dem.get("mat") == 1, f"model khong UTF-8 van duoc nhan: {ket} {dem}")


@ca
def r926_cho_phep_chi_dung_LF_hoac_mot_CRLF():
    # R26-ALLOW-08: cắt MỌI CR/LF ở cuối dòng thì `…CR CR LF` lọt qua danh sách cho phép.
    m = _tai_launcher_thu()
    goc = _R25_DONG_GIU.rstrip("\n").encode()
    for ten, du, mong in [("LF", goc + b"\n", goc + b"\n"), ("CRLF", goc + b"\r\n", goc + b"\r\n"),
                          ("CR_CRLF", goc + b"\r\r\n", b""), ("LF_thua", goc + b"\n\n", goc + b"\n")]:
        ghi, _, _, _ = _r25_loc(m, du)
        bang(ghi == mong, f"{ten}: {ghi!r}")
    m._TRAN_DONG = len(_R25_DONG_GIU)
    ghi, _, _, dem = _r25_loc(m, b"x" * len(_R25_DONG_GIU) + _R25_DONG_GIU.encode())
    bang(ghi == b"" and dem.get("dong_bo") == 2, f"doan cuoi cua dong dai trung dong cho phep van cham dia: {ghi!r}")


@ca
def r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem():
    # R26-COUNT-09: byte xả đi sau khi bộ lọc hỏng, và dòng cho phép không ghi được vì tệp đã đóng, đều là BỎ.
    import io
    m = _tai_launcher_thu()

    class _OngHong(io.BytesIO):
        def readline(self, n=-1):
            if self.tell():
                raise RuntimeError("ong hong")
            return super().readline(n)

    du = b"dau\n" + b"y" * 100
    dem, loi = {}, []
    m._loc_stderr_codex(_OngHong(du), io.BytesIO(), [], loi, dem)
    bang(loi == ["RuntimeError"] and dem.get("byte_bo") == len(du), f"byte xa di khong duoc dem: {dem}")
    f = io.BytesIO()
    f.close()
    dem = {}
    m._loc_stderr_codex(io.BytesIO(_R25_DONG_GIU.encode()), f, [], [], dem)
    bang(dem.get("byte_bo") == len(_R25_DONG_GIU) and dem.get("dong_bo") == 1, f"dong khong ghi duoc khong dem: {dem}")


@ca
def r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC():
    # R26-TEST-03: đường đầu-cuối qua `lenh_run` — khung mất phải tới được run.json.
    with San() as s:
        err = _r25_khung("response.created", "r1", "gpt-6-astra") + _r25_khung("response.completed", "", "gpt-6-astra")
        r, tm, d = _r25_chay(s, err)
        bang(r.returncode == 0, f"launcher rc={r.returncode}: {r.stderr}")
        bang(d.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC"
             and "khong doc duoc" in (d.get("model_phuc_vu_ly_do") or "")
             and [x["response_id"] for x in d.get("model_phuc_vu", [])] == ["r1"], f"mat khung khong toi run.json: {d}")


def _r26_trang_thai(m, du: bytes):
    """Đi trọn đường `_BoLocStderr` (đọc thật trên luồng, chốt, ghi sổ) — trạng thái là thứ run.json sẽ ghi."""
    import io
    bo = m._BoLocStderr(io.BytesIO(du), io.BytesIO())
    bo.bat_dau(); bo.ket_thuc(10)
    ban_ghi = {}
    bo.ghi_so(ban_ghi)
    return ban_ghi, bo.dem


@ca
def r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC():
    # R25-EVID-05 vòng 2: quét MỌI chỗ cắt, không chỉ vài trần chọn tay — trước một khung ĐÚNG, rồi một dòng mang
    # khung ở sau phần đệm (đúng fixture vòng 1), một bản có khoảng trắng quanh dấu hai chấm, một bản header ở đầu.
    m = _tai_launcher_thu()
    dung = _r25_khung("response.created", "rk", "mk").encode()
    khung = _r25_khung("response.created", "rk", "mk").encode()
    co_cach = khung.replace(b'"type": "response.created"', b'"type"   :    "response.created"')
    bang(co_cach != khung, "fixture sai: khong chen duoc khoang trang")
    hoan = _r25_khung("response.completed", "rk", "mk").encode()
    tab = khung.replace(b'"type": "response.created"', b'"type"\t:\t"response.created"')
    ansi = khung.replace(b'"type": "response.created"', b'"type":' + bytes([27]) + b'[1m"response.created"')
    bang(tab != khung and ansi != khung, "fixture sai: khong chen duoc tab/ANSI")
    for ten, sau in [("dem_truoc", b"x" * 256 + khung), ("dem_truoc_co_cach", b"x" * 256 + co_cach),
                     ("dem_truoc_completed", b"x" * 256 + hoan), ("dem_truoc_tab", b"x" * 256 + tab),
                     ("dem_truoc_ansi_trong_token", b"x" * 256 + ansi),
                     ("header_dau_hong", khung.rstrip(b"\n").replace(b'"id": "rk"', b'"id": ""') + b"y" * 300 + b"\n")]:
        du = dung + sau
        for tran in range(60, len(du) + 2):
            m._TRAN_DONG = tran
            ban_ghi, dem = _r26_trang_thai(m, du)
            bang(ban_ghi.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC" and dem.get("mat"),
                 f"{ten} tran={tran}: khung vat cho cat van DO_DUOC: {dem} {ban_ghi.get('model_phuc_vu_ly_do')}")


@ca
def r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran():
    # R26-CLASSIFY-11: dòng NHẬN dài mà tiền tố xác nhận sự kiện KHÁC thì không phải khung mất, ở mọi trần đọc.
    m = _tai_launcher_thu()
    dung = _r25_khung("response.created", "r", "m").encode()
    khac = _r25_khung("response.output_text.delta", "r", "m").encode()
    for tran in range(len(dung) + 1, len(dung) + len(khac) + 2):
        m._TRAN_DONG = tran
        ban_ghi, dem = _r26_trang_thai(m, dung + khac)
        bang(ban_ghi.get("model_phuc_vu_trang_thai") == "DO_DUOC" and not dem.get("mat") and not dem.get("khong_ro"),
             f"tran={tran}: su kien khac bi tinh mat/khong ro: {dem} {ban_ghi.get('model_phuc_vu_ly_do')}")
    for tran in range(40, len(khac) + 2):
        m._TRAN_DONG = tran
        _, _, _, dem = _r25_loc(m, khac)
        bang(not dem.get("mat") and not dem.get("khong_ro"), f"tran={tran}: su kien khac rieng le bi tinh: {dem}")


@ca
def r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO():
    # Header NHẬN mà tiền tố không xác nhận được loại: không khai "mất khung", nhưng chặn DO_DUOC với lý do riêng.
    m = _tai_launcher_thu()
    m._TRAN_DONG = 256
    dau = b"2026-10-24T01:12:06.199773Z TRACE tungstenite::protocol: Received message "
    xg = bytes([92])             # dấu chéo ngược, dựng sau khi parse (bài học chuỗi thoát ở CLAUDE.md)
    dung = _r25_khung("response.created", "r", "m").encode()
    for ten, than in [("khoa_escape", b'{"' + xg + b'u0074ype":"x","pad":"' + b"p" * 400 + b'"}'),
                      ("gia_tri_escape", b'{"type":"x' + xg + b'u0041","pad":"' + b"p" * 400 + b'"}'),
                      ("loai_khong_utf8", b'{"type":"x' + bytes([0xFF]) + b'","pad":"' + b"p" * 400 + b'"}')]:
        ban_ghi, dem = _r26_trang_thai(m, dung + dau + than + b"\n")
        bang(dem.get("khong_ro") == 1 and not dem.get("mat") and ban_ghi.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC"
             and "khong xac dinh" in (ban_ghi.get("model_phuc_vu_ly_do") or ""), f"{ten}: {dem} {ban_ghi}")
    # Đường (1)→(4), cross-review r26c R25-EVID-05: dòng ĐỌC TRỌN, header NHẬN, tải trọng JSON không parse được, không
    # có token gọn (khoá viết bằng escape) — đi sau một khung ĐÚNG — vẫn phải KHÔNG RÕ, không được DO_DUOC.
    m._TRAN_DONG = 4096
    for ten, than in [("escape_va_utf8_hong", b'{"' + xg + b'u0074ype":"response.created","response":{"id":"r2","model":"m'
                       + bytes([0xFF]) + b'"}}'),
                      ("escape_va_json_cut", b'{"' + xg + b'u0074ype":"response.created","response":{"id":"r2"')]:
        ban_ghi, dem = _r26_trang_thai(m, dung + dau + than + b"\n")
        bang(dem.get("khong_ro") == 1 and not dem.get("mat") and ban_ghi.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC",
             f"doc tron {ten}: {dem} {ban_ghi}")
    # Đối chứng: tải trọng KHÔNG mở bằng `{` không thể là khung response — không tính, ở cả hai đường đọc.
    for tran in (256, 4096):
        m._TRAN_DONG = tran
        ban_ghi, dem = _r26_trang_thai(m, dung + dau + b"Binary(" + b"0" * 400 + b")\n" + dau + b"Ping([])\n")
        bang(not dem.get("khong_ro") and not dem.get("mat") and ban_ghi.get("model_phuc_vu_trang_thai") == "DO_DUOC",
             f"tran={tran}: tai trong khong phai JSON bi tinh: {dem} {ban_ghi}")


@ca
def r926_khung_mot_doan_phan_loai_theo_type_DA_PARSE():
    # Khoá `type` viết bằng escape: json.loads đọc ra đúng sự kiện; id rỗng thì phải tính MẤT dù không có token gọn.
    m = _tai_launcher_thu()
    xg = bytes([92])
    dau = b"2026-10-24T01:12:06.199773Z TRACE tungstenite::protocol: Received message "
    hong = dau + b'{"' + xg + b'u0074ype":"response.created","response":{"id":"","model":"m"}}\n'
    _, ket, loi, dem = _r25_loc(m, hong)
    bang(not ket and not loi and dem.get("mat") == 1, f"khung escape id rong khong tinh mat: {ket} {dem}")
    dung = dau + b'{"' + xg + b'u0074ype":"response.created","response":{"id":"re","model":"me"}}\n'
    _, ket, _, dem = _r25_loc(m, dung)
    bang([(k["response_id"], k["model"]) for k in ket] == [("re", "me")] and not dem.get("mat"), f"{ket} {dem}")


@ca
def r926_ghi_het_dem_dung_phan_chua_ghi():
    # R26-COUNT-09 vòng 2: ghi ngắn thì ghi tiếp; ném giữa chừng thì đếm ĐÚNG phần chưa ghi, không đếm cả dòng.
    import io
    m = _tai_launcher_thu()
    dong = _R25_DONG_GIU.encode()

    class _Ngan:
        def __init__(self, ke_hoach):
            self.ke_hoach, self.da = list(ke_hoach), b""

        def write(self, b):
            buoc = self.ke_hoach.pop(0) if self.ke_hoach else len(b)
            if isinstance(buoc, BaseException):
                raise buoc
            self.da += bytes(b[:buoc])
            return buoc

    for ten, ke_hoach, mong_ghi, mong_bo, mong_loi in [
        ("ngan_roi_du", [10, 7], dong, 0, []),
        ("ngan_roi_nem", [10, OSError("dia day")], dong[:10], len(dong) - 10, ["OSError"]),
        ("nem_ngay", [OSError("dia day")], b"", len(dong), ["OSError"]),
        ("tra_0", [0], b"", len(dong), ["OSError"]),
    ]:
        f, loi, dem = _Ngan(ke_hoach), [], {}
        m._loc_stderr_codex(io.BytesIO(dong + b"sau\n"), f, [], loi, dem)
        bang(f.da == mong_ghi and loi == mong_loi and dem.get("byte_bo", 0) == mong_bo + len(b"sau\n"),
             f"{ten}: ghi={f.da!r} loi={loi} dem={dem} (mong bo {mong_bo} + 4)")


@ca
def r926_ghi_so_truoc_khi_chot_khong_DO_DUOC():
    m = _tai_launcher_thu()
    bo = m._BoLocStderr(None, None)
    bo.ket.append({"response_id": "r", "model": "m", "su_kien": "response.created"})
    ban_ghi = {}
    bo.ghi_so(ban_ghi)
    bang(ban_ghi.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC", f"chua chot ma van DO_DUOC: {ban_ghi}")


@ca
def r926_ket_thuc_chot_luong_TRUOC_khi_dong_tep():
    m = _tai_launcher_thu()
    nhat_ky = []

    class _Luong:
        ident = 1                # luồng đã chạy

        def join(self, timeout=None):
            nhat_ky.append("join")

        def is_alive(self):
            nhat_ky.append("hoi")
            return "dong" not in nhat_ky       # còn đọc tới đúng lúc tệp đóng

    class _Tep:
        def close(self):
            nhat_ky.append("dong")

    bo = m._BoLocStderr(None, _Tep())
    bo.luong = _Luong()
    bo.ket_thuc(10)
    bang(nhat_ky == ["join", "hoi", "dong"] and bo.con_doc is True, f"thu tu ket thuc sai: {nhat_ky} {bo.con_doc}")


@ca
def r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC():
    # Luồng đọc không khởi động được: không được để ống không ai đọc (con treo khi đầy), không được ném ra ngoài.
    import io
    m = _tai_launcher_thu()
    ong = io.BytesIO(_r25_khung("response.created", "r", "m").encode())
    bo = m._BoLocStderr(ong, io.BytesIO())

    def hong():
        raise RuntimeError("can't start new thread")

    bo.luong.start = hong
    ban_ghi = {}
    try:
        bo.bat_dau(); bo.ket_thuc(10); bo.ghi_so(ban_ghi)
    except Exception as e:
        bang(False, f"loi khoi dong luong doc lot ra ngoai: {type(e).__name__}: {e}")
    bang(ong.closed, "ong stderr khong duoc dong khi khong co luong doc")
    bang(ban_ghi.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC" and "RuntimeError" in (ban_ghi.get("model_phuc_vu_ly_do") or ""),
         f"khong co luong doc ma so khong ghi loi: {ban_ghi}")


@ca
def r926_response_hong_tung_vi_tu_tinh_mat_khong_loi():
    # Mỗi vị từ của khung ứng viên (response là object, id/model là chuỗi khác rỗng sau strip) một ca: hỏng thì là MẤT,
    # không được thành lỗi bộ lọc, không được nhận.
    m = _tai_launcher_thu()
    dau = b"2026-10-24T01:12:06.199773Z TRACE tungstenite::protocol: Received message "
    for ten, r in [("response_chuoi", "x"), ("response_thieu", None), ("id_so", {"id": 5, "model": "m"}),
                   ("id_rong", {"id": "", "model": "m"}), ("id_trang", {"id": "  ", "model": "m"}),
                   ("model_so", {"id": "r", "model": 5}), ("model_rong", {"id": "r", "model": ""}),
                   ("model_trang", {"id": "r", "model": "  "})]:
        ev = {"type": "response.created"}
        if r is not None:
            ev["response"] = r
        _, ket, loi, dem = _r25_loc(m, dau + json.dumps(ev).encode() + b"\n")
        bang(not ket and not loi and dem.get("mat") == 1 and not dem.get("khong_ro"), f"{ten}: {ket} {loi} {dem}")


@ca
def r926_tien_to_dong_dai_co_tran_va_noi_qua_doan():
    # Tiền tố dùng để xác nhận loại của dòng nhiều đoạn được NỐI qua các đoạn và có TRẦN `_TRAN_DAU_DONG`.
    m = _tai_launcher_thu()
    dau = b"2026-10-24T01:12:06.199773Z TRACE tungstenite::protocol: Received message "
    dong = dau + b"{" + b" " * 60 + b'"type": "response.output_text.delta", "pad": "' + b"p" * 300 + b'"}\n'
    m._TRAN_DONG = 120
    for tran_dau, mong in [(4096, 0), (100, 1), (150, 1)]:
        m._TRAN_DAU_DONG = tran_dau
        _, _, _, dem = _r25_loc(m, dong)
        bang(dem.get("khong_ro", 0) == mong and not dem.get("mat"), f"tran_dau={tran_dau}: {dem} (mong khong_ro={mong})")


@ca
def r926_ket_dong_tien_to_ung_vien_ma_khong_token_la_KHONG_RO():
    # Nhánh chỉ dựng được khi gọi thẳng: dòng nhiều đoạn, tiền tố nói là sự kiện ỨNG VIÊN mà `ung_vien` chưa bật.
    # Không được tha như "sự kiện khác".
    m = _tai_launcher_thu()
    dau = b"2026-10-24T01:12:06.199773Z TRACE tungstenite::protocol: Received message "
    dem = {}
    m._ket_dong(dau + b'{"type":"response.created","pad":"', 2, True, False, [], dem)
    bang(dem.get("khong_ro") == 1 and not dem.get("mat"), f"tien to ung vien bi tha: {dem}")


@ca
def r926_ngu_phap_khung_tung_thanh_phan():
    # Cross-review r26f R26-TEST-15: mỗi thành phần NGỮ PHÁP của header/khung một ca con, đi sau một khung ĐÚNG để
    # việc thiếu bằng chứng dương không che được lỗi phân loại.
    m = _tai_launcher_thu()
    esc = bytes([27])
    dung = _r25_khung("response.created", "r0", "m").encode()

    def khung(rid):
        return _r25_khung("response.created", rid, "m").encode()

    for ten, dong, mong_id, mong_mat in [
        ("ansi_hoi_trung_gian_cuoi_K", esc + b"[?25l" + esc + b"[1 q" + esc + b"[2K" + khung("r1"), ["r0", "r1"], 0),
        ("muc_DEBUG", khung("r2").replace(b" TRACE ", b" DEBUG "), ["r0"], 1),
        ("TRACE_dinh_moc_thoi_gian", khung("r3").replace(b"Z TRACE ", b"ZTRACE "), ["r0"], 1),
        ("rac_sau_khung", khung("r4").rstrip(b"\n") + b" rac\n", ["r0"], 1),
    ]:
        ban_ghi, dem = _r26_trang_thai(m, dung + dong)
        bang([x["response_id"] for x in ban_ghi.get("model_phuc_vu", [])] == mong_id
             and dem.get("mat", 0) == mong_mat and not dem.get("khong_ro"), f"{ten}: {dem} {ban_ghi}")
    dau = b"2026-10-24T01:12:06.199773Z TRACE tungstenite::protocol: Received message "
    for ten, dong in [("mang_json", dau + b"[1]\n"), ("chuoi_json", dau + b'"chuoi"\n'),
                      ("dau_cham_bat_buoc", b'noi dung "type":"responseXcreated"\n')]:
        ban_ghi, dem = _r26_trang_thai(m, dung + dong)
        bang(ban_ghi.get("model_phuc_vu_trang_thai") == "DO_DUOC" and not dem.get("mat") and not dem.get("khong_ro"),
             f"{ten}: khong phai khung ma bi tinh/loi: {dem} {ban_ghi}")


@ca
def r926_hop_dong_ngu_phap_bo_loc_theo_hanh_vi():
    # r26 vòng 7 (cross-review r26g R26-TEST-16; chủ kho chọn "sinh đột biến tự động"): hợp đồng ngữ pháp của bộ lọc,
    # đo bằng HÀNH VI (khung nhận/mất/không rõ), không bằng so regex. Mỗi dòng một biến thể lành tính mà bản gốc và
    # một nới lỏng/siết chặt ngữ pháp phân loại KHÁC nhau. `r926_dot_bien_tu_sinh_moi_thanh_phan_regex` sinh đột biến
    # và đòi mọi đột biến chết ở ca này (hoặc ca khác) hay nằm trong danh sách tương đương có lý do.
    m = _tai_launcher_thu()
    esc = bytes([27])
    dau = b"2026-10-24T01:12:06.199773Z TRACE tungstenite::protocol: Received message "
    dung = _r25_khung("response.created", "r0", "m").encode()

    def khung(rid, mdl="m"):
        return _r25_khung("response.created", rid, mdl).encode()

    def doi(rid, cu, moi):
        k = khung(rid)
        bang(k.count(cu) == 1, f"fixture sai: {cu!r}")
        return k.replace(cu, moi)

    # (1) phải NHẬN — các biến thể ngữ pháp cho phép
    for ten, dong, mong in [
        ("tab_phan_cach", doi("r1", b"Z TRACE tungstenite", b"Z\tTRACE\ttungstenite"), "r1"),
        ("hai_khoang_trang", doi("r2", b"Z TRACE tungstenite", b"Z  TRACE  tungstenite"), "r2"),
        ("CRLF", khung("r3").rstrip(b"\n") + b"\r\n", "r3"),
        ("ansi_nhieu_tham_so", esc + b"[1;32m" + khung("r4"), "r4"),
        ("ansi_khong_tham_so", esc + b"[m" + khung("r5"), "r5"),
        ("ansi_hai_trung_gian", esc + b"[1 !q" + khung("r6"), "r6"),
        # r26 vòng 8 (cross-review r26h R26-TEST-17): hậu tố khoảng trắng sau `}` và hai đầu mút của byte kết CSI.
        ("hai_cach_LF", khung("r8").rstrip(b"\n") + b"  \n", "r8"),
        ("tab_cach_CRLF", khung("r9").rstrip(b"\n") + b"\t \r\n", "r9"),
        ("form_feed", khung("ra").rstrip(b"\n") + bytes([12]) + b"\n", "ra"),
        ("vertical_tab", khung("rb").rstrip(b"\n") + bytes([11]) + b"\n", "rb"),
        ("ansi_ket_at", esc + b"[1@" + khung("rc"), "rc"),
        ("ansi_ket_nga", esc + b"[1~" + khung("rd"), "rd"),
        ("ansi_tham_so_9", esc + b"[9m" + khung("re"), "re"),
        ("ansi_trung_gian_gach_cheo", esc + b"[1/q" + khung("rf"), "rf"),
    ]:
        ban_ghi, dem = _r26_trang_thai(m, dung + dong)
        bang([x["response_id"] for x in ban_ghi.get("model_phuc_vu", [])] == ["r0", mong] and not dem.get("mat"),
             f"nhan {ten}: {dem} {ban_ghi.get('model_phuc_vu')}")
    ban_ghi, _ = _r26_trang_thai(m, khung("r7", "ga[1m"))
    bang([x["model"] for x in ban_ghi.get("model_phuc_vu", [])] == ["ga[1m"], f"van ban giong ANSI bi go: {ban_ghi}")
    # (2) KHÔNG được nhận — header sai nguồn/sai dạng; dòng mang token nên phải tính MẤT
    for ten, cu, moi in [
        ("nam_5_chu_so", b"2026-10-24T", b"20261-10-24T"), ("nam_chu", b"2026-10-24T", b"abcd-10-24T"),
        ("thieu_nam", b"2026-10-24T", b"-10-24T"), ("gach_cheo_nam", b"2026-10", b"2026/10"),
        ("thang_chu_1", b"-10-24T", b"-x0-24T"), ("thang_chu_2", b"-10-24T", b"-1x-24T"),
        ("gach_cheo_ngay", b"10-24T", b"10/24T"), ("ngay_chu_1", b"-24T", b"-x4T"), ("ngay_chu_2", b"-24T", b"-2xT"),
        ("thieu_T", b"24T01", b"24X01"), ("T_roi_khoang", b"T01:12:06.199773Z TRACE", b"T TRACE"),
        ("gio_co_khoang", b"T01:12:06.199773Z TRACE", b"T0 1 TRACE"),
        ("TRACE_dinh_target", b"TRACE tungstenite", b"TRACEtungstenite"),
        ("TRACE_gach_target", b"TRACE tungstenite", b"TRACE-tungstenite"),
        ("dau_hai_cham_gach", b"protocol: Received", b"protocol:-Received"),
        ("Sent_message", b"protocol: Received message", b"protocol: Sent message"),
        ("Received_gach", b"Received message", b"Received-message"),
        ("Received_frame", b"Received message", b"Received frame"),
        ("message_dinh_ngoac", b"Received message {", b"Received messageX{"),
        ("khoang_truoc_ngoac", b"Received message {", b"Received message  {"),
        ("ansi_khong_phai_CSI", b"2026-10-24T", esc + b"(B2026-10-24T"),
        # r26 vòng 8: mỗi nguyên tử BẮT BUỘC của header một ca thiếu đúng nguyên tử ấy
        ("thieu_gach_nam", b"2026-10-24T", b"202610-24T"), ("thieu_gach_thang", b"2026-10-24T", b"2026-1024T"),
        ("thang_mot_so", b"2026-10-24T", b"2026-1-24T"), ("ngay_mot_so", b"2026-10-24T", b"2026-10-4T"),
        ("thieu_TRACE", b"Z TRACE tungstenite", b"Z  tungstenite"),
        ("thieu_target", b"TRACE tungstenite::protocol: Received", b"TRACE  Received"),
        ("dinh_hai_cham_Received", b"protocol: Received", b"protocol:Received"),
        ("thieu_Received", b"protocol: Received message", b"protocol:  message"),
        ("dinh_Received_message", b"Received message", b"Receivedmessage"),
        ("thieu_message", b"Received message {", b"Received  {"),
        ("dinh_message_ngoac", b"Received message {", b"Received message{"),
    ]:
        ban_ghi, dem = _r26_trang_thai(m, dung + doi("rx", cu, moi))
        bang([x["response_id"] for x in ban_ghi.get("model_phuc_vu", [])] == ["r0"] and dem.get("mat") == 1,
             f"khong nhan {ten}: {dem} {ban_ghi.get('model_phuc_vu')}")
    # (3) thân khung: object rỗng là khung parse được, sự kiện khác — không mất, không "không rõ"
    _, _, _, dem = _r25_loc(m, dau + b"{}\n")
    bang(not dem.get("mat") and not dem.get("khong_ro"), f"object rong bi tinh: {dem}")
    # (4) token ứng viên: chỉ đúng `"type":"response.created|completed"` (sau gọn hoá), không gì rộng hơn
    for dong in [b'x "xtype":"response.created" y\n', b'x "typeZ:"response.created" y\n',
                 b'x "type"::"response.created" y\n', b'x "type":xresponse.created" y\n',
                 b'x "type":"conversation.created" y\n', b'x "type":"response.created_x" y\n',
                 b'x "":"response.created" y\n', b'x "type:"response.created" y\n', b'x "type""response.created" y\n',
                 b'x "type":response.created" y\n', b'x "type":".created" y\n', b'x "type":"responsecreated" y\n',
                 b'x "type":"response."" y\n', b'x "type":"response.completed_x" y\n']:
        _, _, _, dem = _r25_loc(m, dong)
        bang(not dem.get("mat"), f"khong phai token ung vien ma tinh mat: {dong!r} {dem}")
    # (5) tiền tố xác nhận loại của dòng NHẬN nhiều đoạn: `{` · khoảng trắng · `"type"` · `:` · chuỗi đóng, ĐÚNG khoá đầu
    m._TRAN_DONG = 128
    duoi = b',"p":"' + b"p" * 400 + b'"}\n'
    for ten, than, mong in [
        ("type_khong_dau", b'{"pad":1,"type":"x.delta"', 1), ("tab_moi_cho", b'{\t"type"\t:\t"x.delta"', 0),
        ("gon", b'{"type":"x.delta"', 0), ("hai_khoang", b'{  "type"  :  "x.delta"', 0),
        ("khoa_lech_1", b'{ztype":"x.delta"', 1), ("khoa_lech_2", b'{"typeZ:"x.delta"', 1), ("loai_rong", b'{"type":""', 0),
        ("khoa_thieu_nhay_dau", b'{type":"x.delta"', 1), ("khoa_rong", b'{"":"x.delta"', 1),
        ("khoa_thieu_nhay_cuoi", b'{"type:"x.delta"', 1), ("thieu_hai_cham", b'{"type" "x.delta"', 1),
    ]:
        _, _, _, dem = _r25_loc(m, dau + than + duoi)
        bang(dem.get("khong_ro", 0) == mong and not dem.get("mat"), f"tien to {ten}: {dem} (mong khong_ro={mong})")


def _r26_token_regex(mau: str) -> list:
    """Cắt NGUỒN một regex (văn bản giữa hai dấu nháy của literal rb"...") thành token (loại, văn bản)."""
    i, ra = 0, []
    while i < len(mau):
        c = mau[i]
        if c == "\\":
            n = 4 if mau[i + 1:i + 2] == "x" else 2
            ra.append(("thoat", mau[i:i + n])); i += n
        elif c == "[":
            j = i + 1
            if mau[j:j + 1] == "^":
                j += 1
            if mau[j:j + 1] == "]":
                j += 1
            while mau[j] != "]":
                j += 2 if mau[j] == "\\" else 1
            ra.append(("lop", mau[i:j + 1])); i = j + 1
        elif c == "{" and re.match(r"\{\d+(,\d*)?\}", mau[i:]):
            k = re.match(r"\{\d+(,\d*)?\}", mau[i:]).group(0)
            ra.append(("lap", k)); i += len(k)
        elif c in "*+?":
            ra.append(("lap", c)); i += 1
        elif c in "^$":
            ra.append(("neo", c)); i += 1
        elif c == "(":
            k = "(?:" if mau[i:i + 3] == "(?:" else "("
            ra.append(("mo", k)); i += len(k)
        elif c in ")|":
            ra.append((c, c)); i += 1
        elif re.match(r"[A-Za-z0-9_:]", c):
            k = re.match(r"[A-Za-z0-9_:]+", mau[i:]).group(0)
            ra.append(("chu", k)); i += len(k)
        else:
            ra.append(("ky", c)); i += 1
    return ra


def _r26_bien_the(mau: str) -> list:
    """Mọi biến thể MỘT thao tác của nguồn regex: xoá từng token; nới lớp/thoát/ký tự thành `.`; `\\s` thành dấu
    cách; nới chữ thành `\\S+`; đổi lượng từ; bỏ từng phần tử của lớp (và dấu phủ định); bỏ từng nhánh `|`. Chỉ giữ
    biến thể biên dịch được và khác bản gốc."""
    tk = _r26_token_regex(mau)

    def ghep(xs):
        return "".join(v for _, v in xs)

    ra = []
    for i, (loai, v) in enumerate(tk):
        thay = []
        if loai not in ("mo", ")"):
            thay.append("")
        if loai in ("thoat", "lop", "ky"):
            thay.append(".")
        if loai == "thoat" and v == "\\s":
            thay.append(" ")
        if loai == "chu":
            thay.append("\\S+")
        if loai == "lap":
            thay += [x for x in ("*", "+", "?") if x != v]
        if loai == "lop":
            ben_trong = v[1:-1]
            phu = ben_trong.startswith("^")
            phan = re.findall(r"\\.|.-.|.", ben_trong[1:] if phu else ben_trong)
            for k in range(len(phan)):
                con = "".join(phan[:k] + phan[k + 1:])
                if con:
                    thay.append("[" + ("^" if phu else "") + con + "]")
            if phu:
                thay.append("[" + ben_trong[1:] + "]")
            # r26 vòng 8 (cross-review r26h R26-TEST-17): dời TỪNG đầu mút của mỗi khoảng `a-b` vào trong một ký tự.
            for k, x in enumerate(phan):
                if len(x) == 3 and x[1] == "-" and ord(x[0]) < ord(x[2]):
                    for moi in (chr(ord(x[0]) + 1) + "-" + x[2], x[0] + "-" + chr(ord(x[2]) - 1)):
                        thay.append("[" + ("^" if phu else "") + "".join(phan[:k] + [moi] + phan[k + 1:]) + "]")
        # r26 vòng 8: biến một nguyên tử BẮT BUỘC thành tuỳ chọn (`\x1b` -> `\x1b?`), khi nó chưa có lượng từ.
        if loai in ("thoat", "lop", "ky", "chu") and not (i + 1 < len(tk) and tk[i + 1][0] == "lap"):
            thay.append(("(?:" + v + ")" if loai == "chu" and len(v) > 1 else v) + "?")
        for t in thay:
            ra.append(ghep(tk[:i]) + t + ghep(tk[i + 1:]))
        # r26 vòng 8: xoá nguyên tử CÙNG lượng từ của nó (`\s*$` -> `$`); xoá riêng nguyên tử thì lượng từ mồ côi.
        if loai in ("thoat", "lop", "ky", "chu") and i + 1 < len(tk) and tk[i + 1][0] == "lap":
            ra.append(ghep(tk[:i]) + ghep(tk[i + 2:]))
        if loai == "|":
            j = i + 1
            while j < len(tk) and tk[j][0] not in ("|", ")"):
                j += 1
            ra.append(ghep(tk[:i]) + ghep(tk[j:]))
            j = i - 1
            while j >= 0 and tk[j][0] not in ("|", "mo"):
                j -= 1
            ra.append(ghep(tk[:j + 1]) + ghep(tk[i + 1:]))
    tot = []
    for x in ra:
        if x == mau or x in tot:
            continue
        try:
            re.compile(x.encode())
        except re.error:
            continue
        tot.append(x)
    return tot


# Biến thể regex SỐNG SÓT mọi ca mà vẫn chấp nhận được: (tên hằng, nguồn biến thể) -> lý do TƯƠNG ĐƯƠNG đo được.
# Thêm dòng vào đây phải kèm lý do vì sao KHÔNG CÓ đầu vào nào phân biệt; dòng thừa (không còn sinh ra hoặc đã bị
# giết) làm ca đỏ — danh sách không được phình ra âm thầm.
_R26_TUONG_DUONG = {
    ("_DAU_NHAN", r"\d{4}-\d\d-\d\dT\S+\s+TRACE\s+tungstenite::protocol: Received message "):
        "neo ^ thua: moi cho dung _DAU_NHAN (_RE_KHUNG, _RE_LOAI_DAU, _RE_DAU_JSON) deu goi .match",
    ("_RE_KHUNG", r"(\{.*\})\s+$"): "dong doc tron luon co LF that sau } (ANSI khong an LF), nen hau to luon >= 1 khoang trang",
    ("_RE_KHOANG_TRANG_B", r"\s"): "re.sub(..., b'') xoa moi khoang trang du khop tung ky tu hay ca chuoi",
    ("_RE_KHOANG_TRANG_B", r"\s*"): "nhu tren: khop rong thay bang rong",
    ("_RE_KHOANG_TRANG_B", r"\s?"): "nhu tren",
    ("_RE_LOAI_DAU", r'.\s*"type"\s*:\s*"([^"\\]*)"'):
        "tien to khong mo bang { thi nhanh khong_ro con doi _RE_DAU_JSON (dau + {) nen ket qua nhu nhau",
    ("_RE_LOAI_DAU", r'\{?\s*"type"\s*:\s*"([^"\\]*)"'): "nhu tren: thieu { thi _RE_DAU_JSON van chan",
}
_R26_SO_BIEN_THE = {"_RE_ANSI_B": 29, "_DAU_NHAN": 67, "_RE_KHUNG": 19, "_RE_UNG_VIEN_GON": 33, "_RE_KHOANG_TRANG_B": 6,
                    "_RE_LOAI_DAU": 50, "_RE_DAU_JSON": 3}
_R26_CA_CHAM = frozenset({"r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC",
                          "r925_codex_qua_han_van_124_va_giu_khung_da_den",
                          "r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC",
                          "r926_dot_bien_tu_sinh_moi_thanh_phan_regex"})


@ca
def r926_bo_sinh_bien_the_co_du_phep():
    # R26-TEST-17: đo CHÍNH bộ sinh trên đầu vào biết trước — mỗi phép (xoá, nới, đổi lượng từ, bỏ phần tử lớp, dời đầu
    # mút khoảng, biến nguyên tử bắt buộc thành tuỳ chọn, bỏ nhánh) phải sinh ra đúng biến thể mong đợi.
    for mau, phai_co in [
        ("[@-~]", ["[A-~]", "[@-}]", ".", ""]),
        (r"\x1b\[", [r"\x1b?\[", r"\x1b\[?", r"\[", r".\["]),
        (r"\s*$", [r"\s+$", r"\s?$", r"\s$", r"$"]),
        ("(?:ab|cd)", ["(?:ab)", "(?:cd)"]),
        ("TRACE", [r"\S+", "(?:TRACE)?"]),
        ("[^ab]", ["[^b]", "[^a]", "[ab]"]),
    ]:
        bt = _r26_bien_the(mau)
        thieu = [x for x in phai_co if x not in bt]
        bang(not thieu, f"bo sinh thieu phep tren {mau!r}: {thieu} (sinh ra: {bt})")


@ca
def r926_dot_bien_tu_sinh_moi_thanh_phan_regex():
    # Cross-review r26g R26-TEST-16, lần thứ tư cùng một lớp: danh sách đột biến VIẾT TAY luôn thiếu một thành phần.
    # Chủ kho chọn đóng lớp này bằng kiến trúc: ca này TỰ SINH mọi biến thể một-thao-tác của MỌI literal regex trong
    # khối bộ lọc (từ `_RUST_LOG_DO_MODEL` tới `def _la_codex` — regex mới thêm vào khối tự động bị đo) và đòi mỗi
    # biến thể bị một ca r925/r926 giết bằng TinHieuChotCa, hoặc nằm trong `_R26_TUONG_DUONG` kèm lý do.
    global LAUNCHER_DANG_DUNG
    goc = LAUNCHER_DANG_DUNG
    dong = Path(goc).read_text(encoding="utf-8").split("\n")
    dau = next(i for i, d in enumerate(dong) if d.startswith("_RUST_LOG_DO_MODEL ="))
    cuoi = next(i for i, d in enumerate(dong) if d.startswith("def _la_codex"))
    ca_chay = [n for n in sorted(globals()) if n.startswith(("r925_", "r926_")) and n not in _R26_CA_CHAM]
    ca_chay.sort(key=lambda n: n != "r926_hop_dong_ngu_phap_bo_loc_theo_hanh_vi")
    song, khac, ten_hang, tong, so_moi_hang, thieu_lit = {}, [], set(), 0, {}, []
    with San() as s:
        try:
            for so in range(dau, cuoi):
                d = dong[so]
                if not d.startswith(("_RE_", "_DAU_NHAN")):
                    continue
                ten = d.split(" =")[0]
                lits = list(re.finditer(r"""rb(["'])(.*?)\1""", d))
                if not lits:
                    thieu_lit.append(ten)
                for lit in lits:
                    ten_hang.add(ten)
                    for k, bt in enumerate(_r26_bien_the(lit.group(2))):
                        tong += 1
                        so_moi_hang[ten] = so_moi_hang.get(ten, 0) + 1
                        p = s / f"launcher_rv7_{so}_{k}.py"
                        p.write_text("\n".join(dong[:so] + [d[:lit.start(2)] + bt + d[lit.end(2):]] + dong[so + 1:]),
                                     encoding="utf-8")
                        LAUNCHER_DANG_DUNG = p
                        chet = False
                        for c in ca_chay:
                            try:
                                globals()[c]()
                            except TinHieuChotCa:
                                chet = True
                                break
                            except Exception as e:
                                khac.append(f"{ten} {bt!r} -> {c}: {type(e).__name__}")
                                chet = True
                                break
                        if not chet:
                            song[(ten, bt)] = True
        finally:
            LAUNCHER_DANG_DUNG = goc
    bang(len(ten_hang) >= 7 and tong >= 100, f"bo sinh gan nhu khong sinh gi: {sorted(ten_hang)} {tong} bien the")
    # r26 vòng 8 (R26-TEST-17): đếm theo TỪNG hằng, không theo tổng — bỏ cả một họ biến thể thì tổng vẫn qua ngưỡng.
    # Đổi regex của bộ lọc hay đổi bộ sinh thì cập nhật bảng này CÓ CHỦ ĐÍCH.
    bang(so_moi_hang == _R26_SO_BIEN_THE, f"so bien the theo hang lech bang chot: {so_moi_hang} != {_R26_SO_BIEN_THE}")
    bang(not thieu_lit, f"dong regex trong khoi loc khong co literal rb'...': {thieu_lit}")
    bang(not khac, f"dot bien chet vi loi KHONG phai chot (tin dung gia): {khac[:5]}")
    la = sorted(k for k in song if k not in _R26_TUONG_DUONG)
    bang(not la, f"{len(la)} bien the regex SONG ma khong co ly do tuong duong: {la[:8]}")
    thua = sorted(k for k in _R26_TUONG_DUONG if k not in song)
    bang(not thua, f"danh sach tuong duong co dong khong con song/khong con sinh ra: {thua}")


@ca
def r926_ghi_so_chup_rieng_ket_loi_dem():
    # Cross-review r26g: ba phép chép ảnh chụp trong `ghi_so` mỗi cái một ca con — luồng đọc vẫn đổi trạng thái SAU
    # khi ảnh đã chụp thì sổ không được đổi theo.
    m = _tai_launcher_thu()
    a_ = {"response_id": "ra", "model": "m", "su_kien": "response.created"}
    b_ = {"response_id": "rb", "model": "m", "su_kien": "response.created"}
    bo = m._BoLocStderr(None, None)
    bo.ket.append(a_)
    bo.dem.update(dong_bo=1, byte_bo=5)
    bo.con_doc = False
    goc = m._ket_luan_model

    def chen_giua(*a, **k):
        bo.ket.append(b_)
        bo.loi.append("RuntimeError")
        bo.dem.update(dong_bo=99, byte_bo=999)
        return goc(*a, **k)

    m._ket_luan_model = chen_giua
    try:
        ban_ghi = {}
        bo.ghi_so(ban_ghi)
    finally:
        m._ket_luan_model = goc
    bang(ban_ghi.get("model_phuc_vu") == [a_], f"danh sach khung doi sau anh chup: {ban_ghi.get('model_phuc_vu')}")
    bang(ban_ghi.get("model_phuc_vu_trang_thai") == "DO_DUOC", f"loi den sau anh chup doi ket luan: {ban_ghi}")
    bang(ban_ghi.get("stderr_bo_dong") == 1 and ban_ghi.get("stderr_bo_byte") == 5, f"bo dem doi sau anh chup: {ban_ghi}")


@ca
def r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC():
    # Đường SẢN XUẤT (R26-EOF-10 vòng 2): luồng đọc chỉ xong khi stderr.log đang đóng — sau hạn chờ thật 10s. Kèm
    # hợp đồng của `_ghi_het`: tệp stderr của lượt codex phải KHÔNG ĐỆM.
    import io
    import pathlib
    m = _tai_launcher_thu()
    khung = _r25_khung("response.created", "r", "m").encode()
    tha, xong, thay = threading.Event(), threading.Event(), {}
    loc_that, mo_that = m._loc_stderr_codex, pathlib.Path.open

    def doi_roi_doc(ong, f, ket, loi, dem):
        try:
            if tha.wait(30):
                loc_that(io.BytesIO(khung), f, ket, loi, dem)
        finally:
            xong.set()

    class _Bao:
        def __init__(self, f):
            self.f = f

        def __getattr__(self, n):
            return getattr(self.f, n)

        def close(self):
            thay["con_doc_luc_dong"] = not xong.is_set()
            tha.set()
            thay["xong_trong_luc_dong"] = xong.wait(5)
            return self.f.close()

    def mo(p, *a, **k):
        f = mo_that(p, *a, **k)
        if p.name == "stderr.log" and a and a[0] == "wb":
            thay["khong_dem"] = isinstance(f, io.FileIO)
            return _Bao(f)
        return f

    with San() as s:
        repo = tao_repo(s); cli = _r25_codex_gia(s); rr = s / "runs"
        a = m.build_parser().parse_args(["run", "--workspace", str(repo), "--run-root", str(rr), "--", str(cli),
                                         "-c", "pass"])
        a.lenh = a.lenh[1:]
        m._loc_stderr_codex, pathlib.Path.open = doi_roi_doc, mo
        try:
            m.lenh_run(a)
        finally:
            m._loc_stderr_codex, pathlib.Path.open = loc_that, mo_that
            tha.set()
        d = json.loads(next(rr.glob("*/run.json")).read_text(encoding="utf-8"))
    bang(thay.get("khong_dem") is True, f"stderr.log cua luot codex co dem: {thay}")
    bang(thay.get("con_doc_luc_dong") and thay.get("xong_trong_luc_dong"), f"fixture khong dung moc dong tep: {thay}")
    bang(d.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC" and "con mo" in (d.get("model_phuc_vu_ly_do") or ""),
         f"doc xong luc dong tep ma van DO_DUOC: {d.get('model_phuc_vu_trang_thai')} {d.get('model_phuc_vu_ly_do')}")


@ca
def r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien():
    m = _tai_launcher_thu()
    k = [{"response_id": "r", "model": "m", "su_kien": "response.created"}]
    bang(m._ket_luan_model(k, [], False) == ("DO_DUOC", None), "du dieu kien ma khong DO_DUOC")
    for ten, doi in [("bo_loc_hong", (k, ["RuntimeError"], False)), ("ong_con_mo", (k, [], True)),
                     ("khong_khung", ([], [], False)), ("mat_khung", (k, [], False, 1))]:
        tt, ld = m._ket_luan_model(*doi)
        bang(tt == "KHONG_DO_DUOC" and ld, f"{ten}: {tt} {ld}")


@ca
def r925_rust_log_thua_ke_bi_GHI_DE_khong_noi():
    with San() as s:
        env = dict(os.environ, RUST_LOG="reqwest=trace,hyper=debug")
        r, tm, d = _r25_chay(s, _R25_DONG_GIU, env=env)
        bang(r.returncode == 0, f"launcher rc={r.returncode}: {r.stderr}")
        bang((tm / "stdout.log").read_text(encoding="utf-8").splitlines()[0] == "tungstenite::protocol=trace",
             f"RUST_LOG thua ke con song: {(tm / 'stdout.log').read_text(encoding='utf-8')!r}")
        bang(d.get("model_phuc_vu_rust_log_ke_thua_bi_ghi_de") is True, f"khong ghi so viec ghi de: {d}")


@ca
def r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m():
    with San() as s:
        r, tm, d = _r25_chay(s, _R25_DONG_GIU + _R25_KHUNG_THUA)
        bang(r.returncode == 0, f"launcher rc={r.returncode}: {r.stderr}")
        bang(d.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC" and d.get("model_phuc_vu") == []
             and d.get("model_phuc_vu_ly_do"), f"khong co khung ma van ghi model: {d}")


@ca
def r925_khong_phai_codex_giu_nguyen_so_va_stderr():
    with San() as s:
        repo = tao_repo(s); rr = s / "runs"
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr), "--", PY, "-c",
                 f"import sys;sys.stderr.write({_r25_khung('response.created', 'r', 'm')!r})")
        tm = next(p for p in rr.iterdir() if p.is_dir())
        d = json.loads((tm / "run.json").read_text(encoding="utf-8"))
        bang(r.returncode == 0 and not any(k.startswith(("model_phuc_vu", "stderr_bo")) for k in d),
             f"luot khong phai codex co khoa model: {d}")
        bang(b"Received message" in (tm / "stderr.log").read_bytes(), "stderr luot khong phai codex bi loc")


@ca
def r925_codex_qua_han_van_124_va_giu_khung_da_den():
    with San() as s:
        han = (datetime.now(timezone.utc) + timedelta(seconds=3)).isoformat()
        r, tm, d = _r25_chay(s, _r25_khung("response.created", "resp_q", "gpt-6-astra"), sau="time.sleep(60)",
                             them=("--deadline-utc", han))
        bang(r.returncode == MA_QUA_HAN, f"mong doi {MA_QUA_HAN}, duoc {r.returncode}: {r.stderr}")
        bang([m["response_id"] for m in d.get("model_phuc_vu", [])] == ["resp_q"], f"mat khung truoc khi giet: {d}")


@ca
def r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC():
    if LA_WINDOWS:
        return "bo qua tren Windows (chau thua ke handle stderr can fixture rieng; duong POSIX do o CI ubuntu)"
    with San() as s:
        sau = ("import subprocess;q=subprocess.Popen([sys.executable,'-c','import time;time.sleep(40)']);"
               "print('CHAU',q.pid,flush=True)")
        t0 = time.monotonic()
        r, tm, d = _r25_chay(s, _r25_khung("response.created", "rc", "gpt-6-astra"), sau=sau)
        mat = time.monotonic() - t0
        for dong in (tm / "stdout.log").read_text(encoding="utf-8").splitlines():
            if dong.startswith("CHAU "):
                with contextlib.suppress(OSError):
                    os.kill(int(dong.split()[1]), 9)
        bang(r.returncode == 0 and mat < 35, f"launcher treo theo chau giu ong: rc={r.returncode} {mat:.1f}s")
        bang(d.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC" and "con mo" in (d.get("model_phuc_vu_ly_do") or ""),
             f"ong con mo ma van DO_DUOC: {d.get('model_phuc_vu_trang_thai')} {d.get('model_phuc_vu_ly_do')}")


@ca
def r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc():
    import io
    m = _tai_launcher_thu()

    class _Hong:
        def __init__(self):
            self.da_ghi = []

        def write(self, b):
            self.da_ghi.append(b)
            raise RuntimeError("dia hong")

    ong = io.BytesIO(_R25_DONG_GIU.encode() + _r25_khung("response.created", "r", "m").encode()
                     + _R25_DONG_GIU.encode())
    f, ket, loi = _Hong(), [], []
    m._loc_stderr_codex(ong, f, ket, loi)
    bang(loi == ["RuntimeError"], f"loi bo loc khong duoc ghi: {loi}")
    bang(ong.read() == b"", "ong chua duoc xa het: con co the treo vi ong day")
    bang(f.da_ghi == [_R25_DONG_GIU.encode()], f"sau khi hong van ghi tiep: {f.da_ghi}")


@ca
def r16_consumer_doc_dung_byte_va_trao_snapshot_cung_co_phai_DO():
    with San() as s:
        repo = tao_repo(s); prompt = s / "prompt.txt"
        noi_dung = ("PROMPT đa byte cödex " + chr(92) + "u0308").encode("utf-8")
        prompt.write_bytes(noi_dung); sha = hashlib.sha256(noi_dung).hexdigest()
        rr = s / "runs-ok"
        ma_doc = ("import hashlib,pathlib,sys;"
                  "print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())")
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--giu-ban-chup", "--prompt-file", str(prompt),
                 "--expected-prompt-sha256", sha, "--", PY, "-c", ma_doc, "{PROMPT_FILE}")
        tm = next(p for p in rr.iterdir() if p.is_dir())
        bang(r.returncode == 0 and (tm / "stdout.log").read_text().strip() == sha,
             "consumer khong nhan dung day byte snapshot")

        rr2 = s / "runs-trao"; cho = s / "cho-phep-doc"
        ma_cho = ("import hashlib,pathlib,sys,time\n"
                  "p=pathlib.Path(sys.argv[1]);c=pathlib.Path(sys.argv[2])\n"
                  "while not c.exists(): time.sleep(.02)\n"
                  "sys.exit(0 if hashlib.sha256(p.read_bytes()).hexdigest()==sys.argv[3] else 41)")
        pr = subprocess.Popen(
            [PY, str(LAUNCHER_DANG_DUNG), "run", "--workspace", str(repo),
             "--run-root", str(rr2), "--giu-ban-chup", "--prompt-file", str(prompt),
             "--expected-prompt-sha256", sha, "--", PY, "-c", ma_cho,
             "{PROMPT_FILE}", str(cho), sha],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            snapshot = None
            for _ in range(200):
                time.sleep(.02)
                ds = list(rr2.glob("*/prompt.snapshot")) if rr2.exists() else []
                if ds:
                    snapshot = ds[0]; break
            bang(snapshot is not None, "khong thay snapshot de chay phan chung")
            mutant = bytearray(noi_dung); mutant[0] ^= 1
            tam = snapshot.with_name("prompt.snapshot.mutant")
            tam.write_bytes(mutant); os.replace(tam, snapshot)
            bang(snapshot.stat().st_size == len(noi_dung), "mutant khong cung kich thuoc")
            cho.write_text("doc", encoding="utf-8")
            pr.wait(timeout=40)
            bang(pr.returncode == 41, f"trao snapshot cung co ma consumer khong DO: {pr.returncode}")
        finally:
            if pr.poll() is None:
                pr.kill(); pr.wait(timeout=10)


SCHEMA_REVIEW = (Path(__file__).resolve().parents[2] / ".github" / "coordination" /
                 "schemas" / "review_verdict.v1.schema.json")


def _schema_hop_le(gia_tri, schema, runtime=None):
    """Validator stdlib cho đúng tập keyword schema v1 đang dùng."""
    def dung_kieu(x, ten):
        return {"object": isinstance(x, dict), "array": isinstance(x, list),
                "string": isinstance(x, str), "null": x is None,
                "integer": isinstance(x, int) and not isinstance(x, bool),
                "boolean": isinstance(x, bool)}.get(ten, False)
    def do(x, s):
        kieu = s.get("type")
        if kieu and not any(dung_kieu(x, t) for t in ([kieu] if isinstance(kieu, str) else kieu)):
            return False
        if "const" in s and x != s["const"]: return False
        if "enum" in s and x not in s["enum"]: return False
        if isinstance(x, str):
            if len(x) < s.get("minLength", 0): return False
            if s.get("pattern") and not re.fullmatch(s["pattern"], x): return False
        if isinstance(x, (int, float)) and not isinstance(x, bool):
            if "minimum" in s and x < s["minimum"]: return False
        if isinstance(x, dict):
            if any(k not in x for k in s.get("required", [])): return False
            p = s.get("properties", {})
            if s.get("additionalProperties") is False and any(k not in p for k in x): return False
            if any(k in x and not do(x[k], v) for k, v in p.items()): return False
        if isinstance(x, list):
            if len(x) < s.get("minItems", 0) or len(x) > s.get("maxItems", len(x)): return False
            if s.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in x}) != len(x): return False
            if "items" in s and any(not do(v, s["items"]) for v in x): return False
        return True
    if not do(gia_tri, schema): return False
    if runtime is None: return True
    b = schema.get("x-tra-luat-runtime-bindings", {})
    if "reviewed_sha" in b and gia_tri["reviewed_sha"] != runtime["reviewed_sha"]: return False
    if "generation" in b and gia_tri["generation"] != runtime["generation"]: return False
    if gia_tri["role"] not in b.get("role", []): return False
    return gia_tri["model_reviewer_identity"]["provider"] in b.get(
        "model_reviewer_identity.provider", [])


def _verdict_mau():
    return {
        "schema_version": 1, "packet_id": "W1-P1-VAN-CHUYEN-PROMPT", "generation": 1,
        "provider": "claude", "role": "reviewer", "session_id": "review-1",
        "model_reviewer_identity": {"provider": "anthropic", "model": "opus",
                                      "session": "review-1"},
        "github_submitter_identity": None, "reviewed_sha": "a" * 40,
        "independent_from_executor_session": True,
        "review_axes": ["spec", "standards_security"], "tests": [], "findings": [],
        "verdict": "approve", "assurance": "cross_approved", "evidence_url": None,
    }


def _oracle_schema_tu_choi(schema, truong, gia_tri):
    runtime = {"reviewed_sha": "a" * 40, "generation": 1}
    bang(_schema_hop_le(_verdict_mau(), schema, runtime), "fixture verdict goc khong hop le")
    d = _verdict_mau()
    if truong == "identity": d["model_reviewer_identity"]["provider"] = gia_tri
    else: d[truong] = gia_tri
    bang(not _schema_hop_le(d, schema, runtime), f"schema nhan sai {truong}={gia_tri!r}")


@ca
def r17_schema_tu_choi_reviewed_sha_khac_exact_head():
    _oracle_schema_tu_choi(json.loads(SCHEMA_REVIEW.read_text()), "reviewed_sha", "b" * 40)


@ca
def r18_schema_tu_choi_generation_khac():
    _oracle_schema_tu_choi(json.loads(SCHEMA_REVIEW.read_text()), "generation", 2)


@ca
def r19_schema_tu_choi_role_khong_duoc_cho_phep():
    _oracle_schema_tu_choi(json.loads(SCHEMA_REVIEW.read_text()), "role", "executor")


@ca
def r20_schema_tu_choi_identity_khong_duoc_cho_phep():
    _oracle_schema_tu_choi(json.loads(SCHEMA_REVIEW.read_text()), "identity", "codex-dispatcher")


@ca
def r21_bon_mutant_noi_semantic_allowlist_phai_lam_oracle_DO():
    goc = json.loads(SCHEMA_REVIEW.read_text())
    mutants = []
    m = json.loads(json.dumps(goc)); m["x-tra-luat-runtime-bindings"].pop("reviewed_sha")
    mutants.append((m, "reviewed_sha", "b" * 40))
    m = json.loads(json.dumps(goc)); m["x-tra-luat-runtime-bindings"].pop("generation")
    mutants.append((m, "generation", 2))
    m = json.loads(json.dumps(goc)); m["properties"]["role"] = {"enum": ["reviewer", "executor"]}
    m["x-tra-luat-runtime-bindings"]["role"].append("executor")
    mutants.append((m, "role", "executor"))
    m = json.loads(json.dumps(goc)); attack = "codex-dispatcher"
    m["properties"]["model_reviewer_identity"]["properties"]["provider"]["enum"].append(attack)
    m["x-tra-luat-runtime-bindings"]["model_reviewer_identity.provider"].append(attack)
    mutants.append((m, "identity", attack))
    for schema, truong, gia_tri in mutants:
        try:
            _oracle_schema_tu_choi(schema, truong, gia_tri)
        except AssertionError:
            continue
        bang(False, f"mutant noi allowlist SONG SOT: {truong}")


# r338 (đo 06-09-2026) — bằng chứng dương của hook phải phủ ĐÚNG gói trong
# requirements.txt, và TÊN GÓI (pip) không phải TÊN MODULE (import).
#
# Ca thật: thêm `PyYAML==6.0.3` vào requirements.txt ⇒ bản cũ suy ra `pyyaml` ⇒
# `ModuleNotFoundError` trong khi `import yaml` chạy tốt ⇒ hook fail-close vì một
# BÁO ĐỘNG GIẢ. Cùng họ "CÓ MẶT ≠ DÙNG ĐƯỢC", lật ngược: ở đây thứ dùng được lại
# bị khai là hỏng, và cái giá vẫn là chặn phiên.
#
# TRÍCH thân Python TỪ CHÍNH tệp hook, không chép lại — chép lại là hai bản trôi
# lệch, đúng bài học `ops/don_ref_chot_test.sh` đã trả giá.
def _r338_than_hook() -> str:
    duong = LAUNCHER.parent.parent / "hooks" / "session-start.sh"
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(duong)
    if ly_do:
        return ""
    m = re.search(r"<<'PYEOF'\n(.*?)\nPYEOF", duong.read_text(encoding="utf-8"), re.S)
    bang(m is not None, "khong tim thay than PYEOF trong session-start.sh")
    return m.group(1)


# r345 — HỢP ĐỒNG CUỐI: KHÔNG gọi pip nữa. Các ca `r342`–`r344` đã được THAY, không phải
# sửa cho xanh — chúng khoá một thiết kế bị PHẢN CHỨNG bác bỏ, không phải một thiết kế
# còn đúng mà cài sai.
#
# Bảy lượt review ra MƯỜI BA finding. Năm vòng đầu cùng một hình dạng (ta tự làm thay
# pip) ⇒ r342 uỷ quyền cho pip. Ba vòng sau cùng một hình dạng KHÁC: mọi cách làm cho
# phép hỏi ấy an toàn đều thua — `--no-index` không chặn direct reference (r343), danh
# sách CẤM lọt URL trần và `git+` (r344), và cuối cùng phản chứng giết cả thiết kế: một
# gói ĐÃ CÀI có `Requires-Dist: childpkg @ http://…` khiến pip đi lấy URL ấy dù
# `requirements.txt` chỉ có một dòng TRẦN. Đo trực tiếp bằng socket đếm kết nối: 1.
# Tức không thể bảo đảm offline bằng cách soi tệp requirements.
#
# Nên phép hỏi pip bị BỎ. Ba bất biến còn lại, tất cả CỤC BỘ và offline theo cấu tạo.
def _r345_venv(td: Path):
    """venv thật + `pypdf` 3.17.4 (cố ý CŨ hơn `>=4.0`). None nếu không dựng được."""
    v = td / "v"
    subprocess.run([PY, "-m", "venv", str(v)], capture_output=True, timeout=300)
    py = v / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
    if not py.exists():
        return None
    if subprocess.run([str(py), "-m", "pip", "install", "--quiet", "pypdf==3.17.4"],
                      capture_output=True, timeout=600).returncode != 0:
        return None
    return py


def _r345_chay(py: Path, d: Path, than: str, reqs: str, *them: str) -> int:
    (d / "requirements.txt").write_text(reqs, encoding="utf-8")
    return subprocess.run([str(py), "-c", than, *them], cwd=d,
                          capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600).returncode


@ca
def r345_than_hook_KHONG_duoc_co_duong_mang_nao():
    """MÃ HOOK không có đường mạng nào — và PHẠM VI của câu ấy hẹp hơn tôi từng viết.

    Đo được: trong cây cú pháp của thân hook không có `subprocess`, `socket`, `urllib`,
    `http`. Bản r345 gọi đó là "cả lớp mở-phiên-chậm-vì-mạng chết theo KIẾN TRÚC" — câu
    ấy RỘNG HƠN PHÉP ĐO theo HAI hướng, và cả hai đã được đo:

    · phép đo AST chỉ thấy `import` TĨNH: `__import__('socket')`, `__import__` với tên
      dựng động, `importlib.import_module`, `ctypes` đều LỌT (tự kiểm, r346) ⇒ đã bù
      bằng ca chặn socket theo HÀNH VI;
    · mạng vẫn có thể đến từ chính việc `import` một gói ĐÃ KHAI, nếu module ấy mở kết
      nối lúc nạp (reviewer đo bằng một gói tổng hợp: 1 kết nối) ⇒ KHÔNG bịt được ở
      đây, vì phép thăm import — thứ duy nhất thấy lớp lỗi r337 — buộc phải nạp mã gói.

    Nên câu đúng là: **mã hook không tự gọi mạng**; hook có thể chạm mạng gián tiếp qua
    gói được khai. Đó là GIỚI HẠN được khai, không phải lỗ được vá.
    """
    than = _r338_than_hook()
    if not than:
        return "bo qua ban sao roi (khong co session-start.sh)"
    import ast as _ast
    cay = _ast.parse(than)
    ten = set()
    for n in _ast.walk(cay):
        if isinstance(n, _ast.Import):
            ten.update(a.name.split(".")[0] for a in n.names)
        elif isinstance(n, _ast.ImportFrom) and n.module:
            ten.add(n.module.split(".")[0])
    cam = ten & {"subprocess", "socket", "urllib", "http", "requests", "ftplib", "asyncio"}
    bang(not cam, f"than hook import module co duong mang: {sorted(cam)}")
    goi = {getattr(n.func, "attr", None) for n in _ast.walk(cay) if isinstance(n, _ast.Call)}
    xau = goi & {"system", "popen", "spawn", "urlopen"}
    bang(not xau, f"than hook goi ham chay tien trinh/mang: {sorted(xau)}")


# Chặn socket ở tầng THƯ VIỆN rồi chạy thân hook: nếu nó chạm mạng bằng BẤT KỲ cách nào,
# phép mở socket sẽ ném và thân hook (vốn bắt `BaseException` khắp nơi) biến nó thành một
# mục `hong` ⇒ mã thoát đổi. Đây là phép đo HÀNH VI, không phải phép đo cú pháp.
_R345_CHAN_MANG = (
    "import socket as _s\n"
    "def _cam(*a, **k):\n"
    "    raise OSError('r345: cam mo socket')\n"
    "_s.socket = _cam\n"
    "_s.create_connection = _cam\n"
    "_s.socketpair = _cam\n"
)


@ca
def r345_chan_socket_that_ma_than_hook_van_chay_dung():
    """Lớp HÀNH VI, vì lớp AST có ĐIỂM MÙ đã đo được.

    Phép đo AST chỉ thấy `import x` tĩnh. Tự kiểm bằng bốn phản chứng: `__import__('socket')`
    · `__import__` với tên dựng động · `importlib.import_module` · `ctypes` — **cả bốn LỌT**.
    Nên nó bắt được ca thực tế (ai đó thêm lại `import subprocess`) chứ không phải mọi
    đường, và khai đúng như thế thay vì để người đọc tưởng nó phủ hết.

    Ca này đóng phần còn lại theo HÀNH VI: chặn `socket` rồi đòi thân hook vẫn trả lời
    ĐÚNG — chạm mạng kiểu gì cũng lộ.
    """
    than = _r338_than_hook()
    if not than:
        return "bo qua ban sao roi (khong co session-start.sh)"
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        py = _r345_venv(d)
        if py is None:
            return "KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)"
        bang(_r345_chay(py, d, _R345_CHAN_MANG + than, "pypdf>=3.0\n", "--kiem-ban") == 0,
             "chan socket lam than hook doi cau tra loi — tuc no CO cham mang")
        bang(_r345_chay(py, d, _R345_CHAN_MANG + than, "pypdf>=4.0\n", "--kiem-ban") == 1,
             "chan socket lam mat phep do lech ban")
        # RĂNG: một thân hook CÓ chạm mạng phải làm ca này ĐỎ, nếu không nó đo cái gì?
        co_mang = than + ("\nimport socket as _t\n_t.socket()\n")
        bang(_r345_chay(py, d, _R345_CHAN_MANG + co_mang, "pypdf>=3.0\n", "--kiem-ban") != 0,
             "than hook CO cham mang ma ca nay VAN xanh — phep chan socket khong co rang")


@ca
def r345_cac_phep_do_cuc_bo_van_dung():
    than = _r338_than_hook()
    if not than:
        return "bo qua ban sao roi (khong co session-start.sh)"
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        py = _r345_venv(d)
        if py is None:
            return "KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)"
        ca_ds = [
            ("ban thoa",                   "pypdf>=3.0\n", 0),
            ("lech ban",                   "pypdf>=4.0\n", 1),
            # r356 — KY VONG CUA FIXTURE KHONG DUOC PHU THUOC NEN CHAY.
            # Ban truoc viet 'pywin32; sys_platform == "win32"' va mong 0. Marker ay DUNG
            # tren windows-latest, nen pywin32 THAT SU bi doi, venv khong co no => 1. Ca
            # nay xanh tren Ubuntu va do tren Windows THEO THIET KE CUA FIXTURE, khong
            # phai theo loi san pham: master do lien tuc tu khi #449 land (run
            # 34023635438, 34025725347) va tai hien duoc tai cho tren Windows.
            # Nay dung mot MENH DE MAU THUAN — SAI theo CAU TAO, khong phu thuoc gia tri
            # cua bien — va DUNG goi
            # `khong_he_ton_tai_r345` nhu hang "goi thieu han" ngay duoi. Hai hang ay khac
            # nhau DUNG MOT BIEN: cai marker. Nen go phep loc marker la hang nay lat
            # 0 -> 1 tren CA HAI nen — dot bien khoa dieu do o
            # `r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO`.
            # r356b — cross-review lượt 1 (codex) P1-01: sentinel VẪN có một giá trị làm
            # marker ĐÚNG. Đo được: `evaluate({"sys_platform": "khong_he_co"})` -> True.
            # Đường override ấy KHÔNG do caller của hook cung cấp (dòng 369 gọi
            # `evaluate()` KHÔNG đối số), và CHƯA chứng minh được lỗi reachable trong đường
            # hook thật đã đo. KHÔNG khẳng định "rủi ro bằng 0" cho mọi môi trường — lượt 2
            # (codex) đo: `evaluate()` không đối số KHÔNG chứng minh `sys.platform` bất biến;
            # sửa `sys.platform` ngay trong interpreter thì sentinel CŨ cho True kể cả khi
            # không đối số, còn mâu thuẫn MỚI vẫn False. Đổi, vì một MÂU THUẪN đúng theo
            # CẤU TẠO mạnh hơn một sentinel chỉ đúng chừng nào chưa ai đặt tên nền như vậy
            # — đúng nếp "đảo danh sách CẤM thành danh sách CHO PHÉP" của kho. Đo lại cả bốn:
            #   mac_dinh=False · ep khong_he_co=False · ep win32=False · ep linux=False
            ("marker khong khop",
             'khong_he_ton_tai_r345; sys_platform == "win32" and sys_platform != "win32"\n', 0),
            ("marker chua dau thang",      'pypdf; os_name == "posix#x"\n', 0),
            ("chu thich sau khoang trang", "pypdf>=3.0  # ghi chu\n", 0),
            ("URL tran toi host chet",     "http://127.0.0.1:9/x-1.0-py3-none-any.whl\n", 0),
            ("VCS git+http",               "git+http://127.0.0.1:9/x.git\n", 0),
            ("goi VANG MAT + direct ref",  "definitely_not_installed_r345 @ http://127.0.0.1:9/x.whl\n", 1),
            ("goi CO MAT + direct ref",    "pypdf @ http://127.0.0.1:9/x.whl\n", 0),
            ("goi thieu han",              "khong_he_ton_tai_r345\n", 1),
        ]
        sai = []
        for nhan, reqs, mong in ca_ds:
            ma = _r345_chay(py, d, than, reqs, "--kiem-ban")
            if ma != mong:
                sai.append(f"{nhan}: duoc {ma}, mong {mong}")
        bang(not sai, "phep do cuc bo sai: " + " · ".join(sai))
        # Che do hau-pip KHONG duoc doi ban (pip vua chay xong la tham quyen).
        bang(_r345_chay(py, d, than, "pypdf>=4.0\n") == 0,
             "che do hau-pip van doi ban — se thanh chot do thuong truc")


@ca
def r345_lop_tham_import_van_co_rang():
    """Lý do DUY NHẤT lớp thăm import tồn tại: pip không nhìn thấy lớp lỗi này (r337)."""
    than = _r338_than_hook()
    if not than:
        return "bo qua ban sao roi (khong co session-start.sh)"
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        py = _r345_venv(d)
        if py is None:
            return "KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)"
        bang(_r345_chay(py, d, than, "pypdf>=3.0\n", "--kiem-ban") == 0, "nen chua sach")
        sp = list(d.glob("v/lib/python*/site-packages")) or list(d.glob("v/Lib/site-packages"))
        bang(bool(sp), "khong tim thay site-packages")
        # PHA import nhung GIU metadata: ban con du, `import` thi chet.
        (sp[0] / "pypdf" / "__init__.py").write_text(
            "raise BaseException('r345-gia-lap-pyo3-panic')\n", encoding="utf-8")
        bang(_r345_chay(py, d, than, "pypdf>=3.0\n", "--kiem-ban") == 1,
             "goi DU va DUNG BAN ma import CHET van xanh — lop tham mat rang")


@ca
def r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO():
    """Ba đột biến, mỗi cái nhắm một phép đo cục bộ. Không có chúng thì ca trên đo gì?

    r356 thêm cái thứ ba — phép lọc environment marker. Trước đó hàng "marker khong khop"
    KHÔNG có đột biến nào, và đó chính là cách nó trôi thành một kỳ vọng phụ thuộc nền mà
    không ai thấy: hàng ấy xanh trên Ubuntu vì marker SAI ở đó, chứ không vì hook lọc đúng.
    Hai lý do khác nhau cho cùng một con số trên MỘT nền — chỉ nền KIA tách được chúng, và
    không có đột biến thì không tách được ở đâu cả.
    """
    than = _r338_than_hook()
    if not than:
        return "bo qua ban sao roi (khong co session-start.sh)"
    neo_ban = "            if not thoa:"
    neo_vang = '                hong.append(f"{_r.name}: VANG MAT (khong co metadata)")'
    neo_marker = "            if _r.marker is not None and not _r.marker.evaluate():"
    bang(than.count(neo_ban) == 1, f"R345_ANCHOR_BAN:{than.count(neo_ban)}")
    bang(than.count(neo_vang) == 1, f"R345_ANCHOR_VANG:{than.count(neo_vang)}")
    bang(than.count(neo_marker) == 1, f"R345_ANCHOR_MARKER:{than.count(neo_marker)}")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        py = _r345_venv(d)
        if py is None:
            return "KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)"
        bang(_r345_chay(py, d, than.replace(neo_ban, "            if False:"),
                        "pypdf>=4.0\n", "--kiem-ban") == 0,
             "dot bien bo phep so specifier VAN DO — ca lech ban khong do phep so ay")
        bang(_r345_chay(py, d, than.replace(neo_vang, "                pass"),
                        "definitely_not_installed_r345 @ http://127.0.0.1:9/x.whl\n",
                        "--kiem-ban") == 0,
             "dot bien bo phep kiem VANG MAT VAN DO — ca vang mat khong do phep kiem ay")
        # r356 — RANG cho hang "marker khong khop". Go phep loc marker thi goi VANG MAT
        # phai lo ra => 1. Hang ay va hang "goi thieu han" dung CHUNG mot goi vang mat,
        # nen bien duy nhat con lai la cai marker: dot bien nay do DUNG phep loc ay chu
        # khong do thu gi khac. Ca hai ve deu doc lap voi nen, nen no DO tren CA HAI nen.
        bang(_r345_chay(py, d, than.replace(neo_marker, "            if False:"),
                        'khong_he_ton_tai_r345; sys_platform == "win32" and sys_platform != "win32"\n',
                        "--kiem-ban") == 1,
             "dot bien bo phep loc marker VAN XANH — ca marker khong do phep loc ay")


# r347 — hai lỗ CỤ THỂ của r345, cộng một LỜI KHAI bị thu hẹp.
#
# (a) Python 3.8/3.9: `packages_distributions` chỉ có từ 3.10, nên trên hai nền ta CỐ Ý
#     hỗ trợ thì `ban_do` rỗng ⇒ vòng thăm import không thăm gì ⇒ lớp bảo vệ r337 biến
#     mất IM LẶNG. Đo được: giả lập bỏ `packages_distributions` rồi phá `pypdf/__init__`
#     ⇒ chốt trả 0 thay vì 1.
# (b) Cú pháp include: `-r 'có nháy'`, nối dòng bằng dấu chéo ngược, và biến môi trường —
#     pip nhận cả ba, regex cũ bỏ sót cả ba ⇒ sửa tệp include mà vân tay KHÔNG ĐỔI ⇒ mốc
#     sống sót ⇒ hook bỏ qua cài đặt.
#
# (c) LỜI KHAI THU HẸP, ghi ở đây vì nó sửa một câu tôi đã viết: r345/r346 nói hook
#     "offline theo cấu tạo". Đúng cho MÃ HOOK, KHÔNG đúng cho toàn cục — mạng vẫn có
#     thể đến từ chính việc `import` một gói đã khai, nếu module ấy mở kết nối lúc nạp.
#     Reviewer đo được điều đó bằng một gói tổng hợp. Đây là GIỚI HẠN được khai, không
#     phải lỗ được vá: bịt nó cần một hộp cát mạng thật, và phép thăm import — thứ duy
#     nhất thấy được lớp lỗi r337 — vốn phải nạp mã của gói.
_R347_CHE_310 = ("import importlib.metadata as _m\n"
                 "if hasattr(_m, 'packages_distributions'):\n"
                 "    del _m.packages_distributions\n")


@ca
def r347_tham_import_van_song_tren_python_truoc_310():
    than = _r338_than_hook()
    if not than:
        return "bo qua ban sao roi (khong co session-start.sh)"
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        py = _r345_venv(d)
        if py is None:
            return "KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)"
        bang(_r345_chay(py, d, _R347_CHE_310 + than, "pypdf>=3.0\n", "--kiem-ban") == 0,
             "gia lap <3.10 lam bao dong gia tren moi truong DA THOA")
        sp = list(d.glob("v/lib/python*/site-packages")) or list(d.glob("v/Lib/site-packages"))
        bang(bool(sp), "khong tim thay site-packages")
        (sp[0] / "pypdf" / "__init__.py").write_text(
            "raise BaseException('r347-gia-lap')\n", encoding="utf-8")
        # CA DICH: tren <3.10, goi DU va DUNG BAN ma import CHET van phai DO.
        bang(_r345_chay(py, d, _R347_CHE_310 + than, "pypdf>=3.0\n", "--kiem-ban") == 1,
             "tren <3.10 phep tham import BIEN MAT — lop bao ve r337 khong con")
        # ...va tren >=3.10 van DO nhu cu (khong hoi quy).
        bang(_r345_chay(py, d, than, "pypdf>=3.0\n", "--kiem-ban") == 1,
             "tren >=3.10 phep tham import cung mat")


@ca
def r347_dot_bien_bo_duong_lui_310_lam_ca_dich_DO():
    """Gỡ đường lui ⇒ ca trên phải ĐỎ. Không có nó thì ca kia đo gì?"""
    than = _r338_than_hook()
    if not than:
        return "bo qua ban sao roi (khong co session-start.sh)"
    neo = "or _module_cua(_r.name)"
    bang(than.count(neo) == 1, f"R347_ANCHOR_LUI:{than.count(neo)}")
    dot_bien = than.replace(neo, "or set()")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        py = _r345_venv(d)
        if py is None:
            return "KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)"
        sp = list(d.glob("v/lib/python*/site-packages")) or list(d.glob("v/Lib/site-packages"))
        (sp[0] / "pypdf" / "__init__.py").write_text(
            "raise BaseException('r347-gia-lap')\n", encoding="utf-8")
        bang(_r345_chay(py, d, _R347_CHE_310 + dot_bien, "pypdf>=3.0\n", "--kiem-ban") == 0,
             "dot bien go duong lui VAN DO — ca dich khong do duong lui ay")


# r351 — NGỪNG BẮT CHƯỚC CÚ PHÁP PIP. Hai ca `r347_van_tay…` và `r349_van_tay…` đã được
# THAY, không phải sửa cho xanh: chúng khoá một bộ phân tích không còn tồn tại.
#
# Hình dạng lỗi này lặp LẦN THỨ HAI. Lần một (r338–r341, 5 finding): tự phân tích DÒNG
# REQUIREMENT ⇒ chữa bằng uỷ quyền cho pip. Lần hai (r347/r349/r350 + vòng 10, ~7
# finding): tự phân tích CHỈ THỊ INCLUDE. Mỗi vòng vá xong lại lộ một luật của pip chưa
# chép đúng — `expand_env_variables` chỉ nhận `${UPPER}` và bỏ giá trị rỗng ·
# `join_lines` dùng `strip(backslash)` chứ không bỏ MỘT ký tự · `realpath` gộp làm mất
# một nhánh symlink · chuỗi `KHONG_DOC_DUOC` trong tệp thật trùng trạng thái tệp bị xoá.
#
# Lần này KHÔNG uỷ quyền được: phép băm phải chạy OFFLINE, mà pip thì không. Nên cách
# đúng là NGỪNG ĐOÁN — có chỉ thị thì nói thẳng "không đủ sức nói khớp" thay vì đoán cho
# ra vẻ chính xác.
#
# Phép đo cố ý THÔ (ký tự đầu không-trắng của một dòng là `-`) và đó là điểm mạnh: nó
# không cần biết cú pháp pip. Một dòng `# -r x` bị tính nhầm chỉ là chạy pip thừa một
# lượt; **chiều sai duy nhất của nó là AN TOÀN**.
_R351_CHI_THI = [
    ("khong nhay",       "-r extra.txt\n"),
    ("co nhay",          "-r 'extra file.txt'\n"),
    ("noi dong",         "-r \\\nextra.txt\n"),
    ("bien moi truong",  "--requirement=${REQ}\n"),
    ("dinh lien",        "-rextra.txt\n"),
    ("nhieu dau cheo",   "-r \\\\\nextra.txt\n"),
    ("constraint",       "-c con.txt\n"),
    ("editable",         "-e .\n"),
    ("thut dau dong",    "   -r extra.txt\n"),
    # r352 — pip GIAI BIEN MOI TRUONG TRUOC khi phan tich option, nen mot dong `${BIEN}`
    # keo duoc tep khac vao trong khi ky tu dau la dola. Do duoc: pip keo `extra.txt`,
    # luat tho lan mot tra 0. Toi da TU HOI dung cau nay ("dang nao khong bat dau bang
    # `-` ma van keo tep?") va thu `pypdf -r extra.txt` roi ket luan "khong thung" — cau
    # hoi dung, PHEP THU THIEU MOT DANG. Nen ca duoi giu ca hai dang bien.
    ("bien moi truong ${}", "${INCLUDE}\n"),
    ("bien moi truong $",   "$INCLUDE\n"),
]

# BIEN PHAI DUOC DAT, khong thi ca KHONG CO RANG — do duoc, khong phai lo xa: bien
# khong dat ⇒ pip that bai ⇒ khong dat moc ⇒ ca XANH tren CA hook chua va. Phep do rang
# hai chieu bat duoc dung chuyen nay (nen 1 moc / sau 0 moc chi hien khi bien co dat).
_R351_MOI_TRUONG = {"INCLUDE": "-r extra.txt"}


def _r351_khoi_moc(d: Path, reqs: str) -> tuple:
    """Chạy KHỐI ĐẶT MỐC thật của hook hai lượt; trả (số mốc sau lượt 1, dòng cuối lượt 2)."""
    hook = (LAUNCHER.parent.parent / "hooks" / "session-start.sh").read_text(encoding="utf-8")
    kh = hook[hook.index("if [ -f requirements.txt ]; then"):hook.index("# --- Xác thực codex")]
    (d / "chay.sh").write_text("set -euo pipefail\nPY=" + PY + "\n" + kh, encoding="utf-8")
    (d / "requirements.txt").write_text(reqs, encoding="utf-8")
    (d / "extra.txt").write_text("pypdf>=3.0\n", encoding="utf-8")
    (d / "extra file.txt").write_text("pypdf>=3.0\n", encoding="utf-8")
    (d / "con.txt").write_text("pypdf>=3.0\n", encoding="utf-8")
    for f in (d / ".git").glob(".tl_reqs_*"):
        f.unlink()
    vo = shutil.which("bash") or "/bin/bash"
    env = dict(os.environ)
    env.update(_R351_MOI_TRUONG)
    subprocess.run([vo, "chay.sh"], cwd=d, capture_output=True, text=True, timeout=600, env=env)
    return len(list((d / ".git").glob(".tl_reqs_*")))


@ca
def r351_co_chi_thi_thi_KHONG_duoc_dat_moc():
    """Bất biến thay cho cả bộ phân tích: có chỉ thị ⇒ không mốc ⇒ pip quyết.

    Chín dạng chỉ thị, gồm bốn dạng mà bản phân tích cũ đã phải vá từng cái và hai dạng
    vòng 10 vừa bắt được. Ở đây không dạng nào cần luật riêng — phép đo không biết cú
    pháp pip, nên không có gì để chép sai.
    """
    duong = LAUNCHER.parent.parent / "hooks" / "session-start.sh"
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(duong)
    if ly_do:
        return ly_do
    if os.name == "nt":
        return "bo qua: khoi dat moc la shell POSIX"
    lot = []
    for nhan, reqs in _R351_CHI_THI:
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            subprocess.run(["git", "init", "-q", str(d)], capture_output=True, timeout=120)
            if _r351_khoi_moc(d, reqs) != 0:
                lot.append(nhan)
    bang(not lot, "co chi thi ma VAN dat moc (moc se song sot sai): " + " · ".join(lot))


@ca
def r351_KHONG_co_chi_thi_thi_van_phai_dat_moc():
    """RĂNG chiều ngược: nếu không có chỉ thị mà cũng không đặt mốc thì hook chạy pip mãi.

    Thiếu vế này, bản vá "không bao giờ đặt mốc" sẽ làm ca trên XANH tuyệt đối — đúng
    kiểu chốt không thể đỏ mà kho này đã trả giá nhiều lần.
    """
    duong = LAUNCHER.parent.parent / "hooks" / "session-start.sh"
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(duong)
    if ly_do:
        return ly_do
    if os.name == "nt":
        return "bo qua: khoi dat moc la shell POSIX"
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        subprocess.run(["git", "init", "-q", str(d)], capture_output=True, timeout=120)
        bang(_r351_khoi_moc(d, "pypdf>=3.0\n") == 1,
             "khong co chi thi ma cung khong dat moc — hook se chay pip moi luot")


@ca
def r351_requirements_cua_kho_khong_phai_tra_gia():
    """Giá của r351 chỉ rơi vào kho DÙNG chỉ thị. Đo trên kho này thay vì khẳng định."""
    duong = Path(__file__).resolve().parents[2] / "requirements.txt"
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(duong)
    if ly_do:
        return ly_do
    co = [d for d in duong.read_text(encoding="utf-8").splitlines() if d.lstrip().startswith("-")]
    bang(not co,
         "requirements.txt cua kho CO chi thi ⇒ hook se chay pip moi luot mo phien; "
         f"neu co y thi cap nhat ca nay: {co[:3]}")


# r348 — `_module_cua()` suy SAI cho gói CHỈ CÓ CLI, và tôi tự tìm ra khi kiểm chính câu
# hỏi mình vừa gửi reviewer.
#
# RECORD của một gói chỉ có CLI ghi đường kiểu `../../../bin/clix`, nên đoạn đầu là `..`
# — không bắt đầu bằng gạch dưới, không trùng hậu tố loại trừ nào — và bản trước đi
# `__import__("..")` rồi báo hỏng. Đo được trước khi vá: `rc=1` cho một môi trường HOÀN
# TOÀN ĐÚNG. Đúng lớp BÁO ĐỘNG GIẢ đã sinh ra bảy finding đầu của chuỗi này, lần này do
# chính đường lui vừa thêm ở r347 mang vào.
#
# Chốt là `isidentifier()`: tên module hợp lệ luôn là một định danh Python. Đây là danh
# sách CHO PHÉP (thứ hợp lệ mới qua), không phải danh sách CẤM thêm `..` vào — bài học
# r344 áp thẳng vào đây.
def _r348_dist(sp: Path, ten: str, tep, top=None):
    di = sp / f"{ten}-1.0.dist-info"
    di.mkdir(parents=True, exist_ok=True)
    (di / "METADATA").write_text(f"Metadata-Version: 2.1\nName: {ten}\nVersion: 1.0\n",
                                 encoding="utf-8")
    (di / "INSTALLER").write_text("pip\n", encoding="utf-8")
    (di / "WHEEL").write_text("Wheel-Version: 1.0\nGenerator: t\nRoot-Is-Purelib: true\n"
                              "Tag: py3-none-any\n", encoding="utf-8")
    (di / "RECORD").write_text("\n".join(tep), encoding="utf-8")
    if top is not None:
        (di / "top_level.txt").write_text(top, encoding="utf-8")
    for t in tep:
        f = sp / t
        if f.suffix in (".py", ".pth") or "/" in t:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text("", encoding="utf-8")


_R348_CHE_310 = ("import importlib.metadata as _m\n"
                 "if hasattr(_m, 'packages_distributions'):\n"
                 "    del _m.packages_distributions\n")


@ca
def r348_goi_chi_co_CLI_khong_duoc_bao_dong_gia():
    than = _r338_than_hook()
    if not than:
        return "bo qua ban sao roi (khong co session-start.sh)"
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        py = _r345_venv(d)
        if py is None:
            return "KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)"
        sp = (list(d.glob("v/lib/python*/site-packages")) or list(d.glob("v/Lib/site-packages")))[0]
        # RECORD tro RA NGOAI cay: dung hinh dang cua mot goi chi co CLI.
        _r348_dist(sp, "clionly", ["clionly-1.0.dist-info/METADATA", "../../../bin/clix"], top="")
        _r348_dist(sp, "datapkg", ["datapkg/__init__.py", "datapkg-1.0.data/scripts/x"])
        _r348_dist(sp, "nofiletop", ["nofiletop/__init__.py"])
        sai = []
        for ten in ("clionly", "datapkg", "nofiletop"):
            ma = _r345_chay(py, d, _R348_CHE_310 + than, ten + "\n", "--kiem-ban")
            if ma != 0:
                sai.append(f"{ten}: rc={ma}")
        bang(not sai, "bao dong gia tren moi truong DUNG: " + " · ".join(sai))


@ca
def r348_dot_bien_bo_isidentifier_lam_ca_dich_DO():
    """Gỡ chốt `isidentifier()` ⇒ ca trên phải ĐỎ. Không có nó thì ca kia đo gì?"""
    than = _r338_than_hook()
    if not than:
        return "bo qua ban sao roi (khong co session-start.sh)"
    neo = "if (dau and dau.isidentifier() and not dau.startswith(\"_\")"
    bang(than.count(neo) == 1, f"R348_ANCHOR:{than.count(neo)}")
    dot_bien = than.replace(neo, "if (dau and not dau.startswith(\"_\")")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        py = _r345_venv(d)
        if py is None:
            return "KHONG DO DUOC: khong dung duoc venv/pip (co the khong co mang)"
        sp = (list(d.glob("v/lib/python*/site-packages")) or list(d.glob("v/Lib/site-packages")))[0]
        _r348_dist(sp, "clionly", ["clionly-1.0.dist-info/METADATA", "../../../bin/clix"], top="")
        bang(_r345_chay(py, d, _R348_CHE_310 + dot_bien, "clionly\n", "--kiem-ban") != 0,
             "dot bien go `isidentifier()` VAN xanh — ca dich khong do chot ay")


@ca
def r349_backend_PDF_du_phong_chay_thi_dung_noi_la_bi_chan():
    """Một chẩn đoán TỰ MÂU THUẪN đẩy người đọc đi sai hướng.

    r337 tính `co = pypdf or pdfplumber` (đúng) nhưng vẫn in `loi_import` (sai): `pypdf`
    hỏng + `pdfplumber` chạy ⇒ `co=True` mà hậu quả vẫn ghi *"MỌI .pdf bị chặn … cài lại
    phụ thuộc"*. Cùng doctrine với `codex login status` NÓI DỐI — công cụ báo sai trạng
    thái tệ hơn công cụ vắng mặt.

    CHẠY TRONG TIẾN TRÌNH CON, không `import tl_core` ở đây. Hai lý do, và lý do thứ hai
    là một cổng thật đã bắt được: (a) đo trên interpreter SẠCH thì không phải nghịch
    `sys.modules`/`sys.meta_path` của chính bộ test — hai lần đầu tôi dựng fixture sai
    đúng vì chuyện ấy; (b) `t16` trong `ops/cong_cu_test.py` đòi mọi gói bên thứ ba
    import trong cây phải được khai ở `ops/cong_cu.yaml`, và một `import tl_core` ở đây
    làm cổng ĐỎ — nới bản kê để lách là hạ một chốt thật, không phải sửa test.
    """
    goc = Path(__file__).resolve().parents[2] / "scripts"
    duong = goc / "tl_core" / "ops_misc.py"
    ly_do = _bo_qua_neu_ban_sao_roi_thieu(duong)
    if ly_do:
        return ly_do
    kich = (
        "import json, sys, tempfile, pathlib\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "import tl_core.ops_misc as om\n"
        "hong, tot, chan = json.loads(sys.argv[2])\n"
        "class C:\n"
        "    def find_spec(self, name, path=None, target=None):\n"
        "        if name in chan: raise ModuleNotFoundError(name)\n"
        "        return None\n"
        "td = tempfile.mkdtemp(); p = pathlib.Path(td)\n"
        "for t in hong: (p / (t + '.py')).write_text(\"raise BaseException('r349')\\n\")\n"
        "for t in tot:  (p / (t + '.py')).write_text('')\n"
        "sys.path.insert(0, td); sys.meta_path.insert(0, C())\n"
        "d = next(x for x in om._doc_dep_probe() if x['ten'].startswith('pypdf'))\n"
        "print(json.dumps({'co': d['co'], 'hau_qua': d['hau_qua']}))\n"
    )

    def do(hong, tot, chan):
        p = subprocess.run([PY, "-c", kich, str(goc), json.dumps([hong, tot, chan])],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
        bang(p.returncode == 0, f"kich ban con hong: {(p.stdout + p.stderr)[-200:]!r}")
        return json.loads(p.stdout.strip().splitlines()[-1])

    d1 = do(["pypdf"], ["pdfplumber"], [])
    bang(d1["co"] is True, "backend du phong chay ma `co` van False")
    bang("bị chặn" not in d1["hau_qua"],
         f"du phong CHAY ma van noi bi chan: {d1['hau_qua'][:110]!r}")
    bang("pypdf" in d1["hau_qua"], "khong nhac backend hong — mat thong tin chan doan that")
    # RĂNG hai chiều: hỏng THẬT thì vẫn phải nói bị chặn.
    d2 = do(["pypdf"], [], ["pdfplumber"])
    bang(d2["co"] is False and "bị chặn" in d2["hau_qua"],
         "ca hai duong hong ma khong noi bi chan — chot mat rang")
    d3 = do([], [], ["pypdf", "pdfplumber"])
    bang(d3["co"] is False and "pip install pypdf" in d3["hau_qua"],
         "thieu han ma khong khuyen cai")


# ------------------------------------------------------ tự đột biến: có răng không

@ca
def r484_g2_doctor_doc_dung_home_da_materialize():
    """Custom home must be the same source for materialization and diagnostics."""
    with tempfile.TemporaryDirectory(prefix="wp484-home-") as td:
        root = Path(td)
        default = root / "default"
        custom = root / "custom"
        default.mkdir()
        custom.mkdir()
        (custom / "auth.json").write_text(
            json.dumps({"tokens": {"refresh_token": "INERT-FIXTURE"},
                        "last_refresh": "2026-09-09T00:00:00Z"}), encoding="utf-8")
        (custom / "auth.json").chmod(0o600)
        env = dict(os.environ, HOME=str(default), USERPROFILE=str(default),
                   CODEX_HOME=str(custom))
        env.pop("CODEX_AUTH_JSON", None)
        script = ("import json,runpy,sys; m=runpy.run_path(sys.argv[1]); "
                  "print(json.dumps(m['_han_token_codex']()))")
        result = subprocess.run([PY, "-c", script, str(LAUNCHER_DANG_DUNG)],
                                env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        bang(result.returncode == 0, result.stderr)
        measured = json.loads(result.stdout)
        bang(measured["doc_duoc"], "doctor ignored the credential in CODEX_HOME")
        bang(measured["last_refresh"] == "2026-09-09T00:00:00Z", 'measured["last_refresh"] == "2026-09-09T00:00:00Z"')
        bang(not (default / ".codex").exists(), "diagnostic modified fallback home")


@ca
def r484_g2_env_policy_cung_home_hai_chieu():
    """The active config, not residue in the other home, controls the gate."""
    import runpy
    policy = runpy.run_path(str(CODEX_ENV_POLICY))
    block = (policy["MOC_MO"] + b"\n" + policy["_THAN_KHOI_CU"][0]
             + b"\n" + policy["MOC_DONG"] + b"\n")
    with tempfile.TemporaryDirectory(prefix="wp484-policy-") as td:
        root = Path(td)
        default = root / "default" / ".codex"
        custom = root / "custom"
        default.mkdir(parents=True)
        custom.mkdir()
        env = dict(os.environ, HOME=str(default.parent), USERPROFILE=str(default.parent),
                   CODEX_HOME=str(custom))
        env.pop("CODEX_AUTH_JSON", None)

        def gate(*args):
            return subprocess.run([PY, str(CODEX_ENV_POLICY), *args], env=env,
                                  capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)

        (custom / "config.toml").write_bytes(block)
        bang(gate("--tep", str(custom / "config.toml")).returncode == 3, "invalid control fixture")
        bang(gate().returncode == 3, "gate ignored active legacy block in CODEX_HOME")
        (custom / "config.toml").write_bytes(b"# clean custom home\n")
        (default / "config.toml").write_bytes(block)
        bang(gate().returncode == 0, "residue in fallback home blocked clean CODEX_HOME")
        env["CODEX_HOME"] = ""
        bang(gate().returncode == 3, "empty CODEX_HOME did not use fallback")


@ca
def r484_g2_auth_hong_utf8_tra_loi_co_kiem_soat():
    with tempfile.TemporaryDirectory(prefix="wp484-corrupt-") as td:
        root = Path(td)
        home = root / ".codex"
        home.mkdir()
        auth = home / "auth.json"
        auth.write_bytes(b"\xff\xfeINERT-CORRUPT")
        env = dict(os.environ, HOME=str(root), USERPROFILE=str(root), CODEX_HOME=str(home),
                   CODEX_AUTH_JSON=json.dumps({"tokens": {"refresh_token": "INERT-NEW"}}))
        script = ("import json,runpy,sys; m=runpy.run_path(sys.argv[1]); "
                  "print(json.dumps(m['chuan_bi_xac_thuc'](that_su=False)))")
        result = subprocess.run([PY, "-c", script, str(LAUNCHER_DANG_DUNG)],
                                env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        bang(result.returncode == 0, "corrupt auth escaped as traceback: " + result.stderr)
        measured = json.loads(result.stdout)
        bang(measured and measured[0]["ok"] is False, "unreadable disk auth was reported healthy")
        bang(auth.read_bytes() == b"\xff\xfeINERT-CORRUPT", 'auth.read_bytes() == b"\\xff\\xfeINERT-CORRUPT"')
        bang("INERT-NEW" not in result.stdout + result.stderr, '"INERT-NEW" not in result.stdout + result.stderr')


@ca
def r484_g2_schema_truoc_freshness_va_home_materialize():
    """A newer disk snapshot must not hide malformed input or select default home."""
    with tempfile.TemporaryDirectory(prefix="wp484-schema-") as td:
        root = Path(td)
        custom = root / "custom"
        custom.mkdir()
        old = json.dumps({"tokens": {"refresh_token": "INERT-DISK"},
                          "last_refresh": "2026-09-09T00:00:00Z"})
        auth = custom / "auth.json"
        auth.write_text(old, encoding="utf-8")
        auth.chmod(0o600)
        script = ("import json,runpy,sys; m=runpy.run_path(sys.argv[1]); "
                  "print(json.dumps(m['chuan_bi_xac_thuc'](that_su=False)))")
        for tokens, expected in (([], False), (None, False), ("INERT-BAD", False), ({}, True)):
            env = dict(os.environ, HOME=str(root), USERPROFILE=str(root),
                       CODEX_HOME=str(custom), CODEX_AUTH_JSON=json.dumps({
                           "tokens": tokens, "last_refresh": "2026-09-08T00:00:00Z"}))
            p = subprocess.run([PY, "-c", script, str(LAUNCHER_DANG_DUNG)],
                               env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
            bang(p.returncode == 0, "schema validation escaped controlled result")
            result = json.loads(p.stdout)[0]
            bang(result["ok"] is expected, "freshness hid invalid schema")
            bang(result["duong_dan"] == str(auth), "materializer selected another home")
            bang(result["doi"] is False, 'result["doi"] is False')
            bang(auth.read_text(encoding="utf-8") == old, 'auth.read_text(encoding="utf-8") == old')
            bang("INERT-" not in p.stdout + p.stderr, '"INERT-" not in p.stdout + p.stderr')
        bang(not (root / ".codex").exists(), 'not (root / ".codex").exists()')


@ca
def r484_g2_child_khong_nhan_snapshot_va_rac_chan_truoc_probe():
    """Run a real inert child; malformed snapshot must stop before run creation."""
    with San() as s:
        repo = tao_repo(s)
        home = s / "custom-home"
        home.mkdir()
        snapshot = json.dumps({"tokens": {"refresh_token": "INERT-BOUNDARY"}})
        auth = home / "auth.json"
        auth.write_text(snapshot, encoding="utf-8")
        auth.chmod(0o600)
        env = dict(os.environ, CODEX_HOME=str(home), CODEX_AUTH_JSON=snapshot,
                   HOME=str(s), USERPROFILE=str(s))
        code = ("import json,os,pathlib; "
                "assert 'CODEX_AUTH_JSON' not in os.environ; "
                "p=pathlib.Path(os.environ['CODEX_HOME'])/'auth.json'; "
                "assert json.loads(p.read_text())['tokens']['refresh_token']=='INERT-BOUNDARY'; "
                "print('BOUNDARY-OK')")
        rr = s / "runs"
        p = subprocess.run([PY, str(LAUNCHER_DANG_DUNG), "run", "--workspace", str(repo),
                            "--expected-head", head_cua(repo), "--deadline-utc", mai_sau(30),
                            "--run-root", str(rr), "--", PY, "-c", code],
                           env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=45)
        bang(p.returncode == 0, "inert launcher child failed: " + p.stderr)
        logs = list(rr.glob("*/stdout*"))
        bang(logs and any("BOUNDARY-OK" in f.read_text(encoding="utf-8") for f in logs), 'logs and any("BOUNDARY-OK" in f.read_text(encoding="utf-8") for f in logs)')
        bang(auth.read_text(encoding="utf-8") == snapshot, 'auth.read_text(encoding="utf-8") == snapshot')
        bad_runs = s / "bad-runs"
        env["CODEX_AUTH_JSON"] = '{"tokens": "INERT-BAD"}'
        p = subprocess.run([PY, str(LAUNCHER_DANG_DUNG), "run", "--workspace", str(repo),
                            "--expected-head", head_cua(repo), "--run-root", str(bad_runs),
                            "--", PY, "-c", "raise AssertionError('child must not run')"],
                           env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        bang(p.returncode == MA_CHUA_XAC_THUC, 'p.returncode == MA_CHUA_XAC_THUC')
        bang(not bad_runs.exists(), "invalid snapshot reached probe/run stage")
        bang("INERT-BAD" not in p.stdout + p.stderr, '"INERT-BAD" not in p.stdout + p.stderr')
        bang(auth.read_text(encoding="utf-8") == snapshot, 'auth.read_text(encoding="utf-8") == snapshot')


@ca
def r484_g2_storage_kernel_guardrails():
    """Kernel measurements: private replace, hardlinks, reparse/ancestors, rollback."""
    from unittest.mock import patch
    m = _tai_launcher_thu()
    with San() as s:
        home = s / "codex"
        with m._KhoCodex(home, create=True) as store:
            store.write("auth.json", b"INERT-OLD", None)
            bang(store.read() == b"INERT-OLD", 'store.read() == b"INERT-OLD"')
            with patch.object(m.os, "replace", side_effect=OSError("injected rename failure")):
                try:
                    store.write("auth.json", b"INERT-NEW", b"INERT-OLD")
                except OSError:
                    pass
                else:
                    bang(False, "rename failure was accepted")
            bang(store.read() == b"INERT-OLD", 'store.read() == b"INERT-OLD"')
            bang(not list(home.glob("*.tmp-*")), 'not list(home.glob("*.tmp-*"))')
            try:
                store.write("auth.json", b"INERT-NEW", b"WRONG-CAS")
            except OSError:
                pass
            else:
                bang(False, "changed credential was overwritten")
            link = s / "hardlink"
            os.link(home / "auth.json", link)
            try:
                store.read()
            except OSError:
                pass
            else:
                bang(False, "hardlinked credential was accepted")
            link.unlink()
            moved = s / "moved"
            bang(home.resolve().is_relative_to(s.resolve()), 'home.resolve().is_relative_to(s.resolve())')
            bang(moved.resolve().is_relative_to(s.resolve()), 'moved.resolve().is_relative_to(s.resolve())')
            if LA_WINDOWS:
                try:
                    home.rename(moved)
                except OSError:
                    pass
                else:
                    bang(False, "Windows ancestor was not pinned")
            else:
                home.rename(moved)
                home.mkdir()
                (home / "auth.json").write_bytes(b"INERT-DECOY")
                store.write("auth.json", b"INERT-NEW", b"INERT-OLD")
                bang((moved / "auth.json").read_bytes() == b"INERT-NEW", '(moved / "auth.json").read_bytes() == b"INERT-NEW"')
                bang((home / "auth.json").read_bytes() == b"INERT-DECOY", '(home / "auth.json").read_bytes() == b"INERT-DECOY"')
        repo = s / "repo"
        (repo / ".git").mkdir(parents=True)
        try:
            with m._KhoCodex(repo / "credentials", create=True):
                bang(False, "repository credential destination accepted")
        except OSError:
            pass
        bang(not (repo / "credentials").exists(), 'not (repo / "credentials").exists()')
        target = s / "target"
        target.mkdir()
        (target / "sentinel").write_text("INERT-SENTINEL", encoding="utf-8")
        junction = s / "redirect"
        if LA_WINDOWS:
            p = subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(junction), str(target)],
                               capture_output=True, text=True, timeout=20)
            bang(p.returncode == 0, "Windows junction could not be measured")
        else:
            junction.symlink_to(target, target_is_directory=True)
        try:
            with m._KhoCodex(junction / "credentials", create=True):
                bang(False, "ancestor redirect accepted")
        except OSError:
            pass
        bang(not (target / "credentials").exists(), 'not (target / "credentials").exists()')
        bang((target / "sentinel").read_text() == "INERT-SENTINEL", '(target / "sentinel").read_text() == "INERT-SENTINEL"')
        if LA_WINDOWS:
            os.rmdir(junction)
            p = subprocess.run(["icacls", str(home / "auth.json"), "/grant", "*S-1-1-0:(R)"],
                               capture_output=True, text=True, timeout=20)
            bang(p.returncode == 0, "ACL counterexample could not be measured")
            try:
                with m._KhoCodex(home) as store:
                    store.read()
            except OSError:
                pass
            else:
                bang(False, "credential readable by Everyone was accepted")


@ca
def r484_g2_recovery_probe_rollback_va_snapshot_moi():
    """A rejected token stays rejected across formatting; unknown errors are not auth."""
    from unittest.mock import patch
    m = _tai_launcher_thu()
    def payload(token, day):
        return json.dumps({"tokens": {"refresh_token": token},
                           "last_refresh": f"2026-09-{day:02d}T00:00:00Z"}).encode()
    with San() as s:
        home = s / "codex"
        old, bad, new, rotated = (payload("INERT-OLD", 1), payload("INERT-BAD", 2),
                                  payload("INERT-NEW", 3), payload("INERT-ROTATED", 4))
        with m._KhoCodex(home, create=True) as store:
            store.write("auth.json", old, None)
        bang(m._danh_dau_auth_hong(home), 'm._danh_dau_auth_hong(home)')
        bang(m._dang_cho_snapshot(home), 'm._dang_cho_snapshot(home)')
        calls = []
        def failed(data):
            calls.append(data)
            bang((home / "auth.json").read_bytes() == old, '(home / "auth.json").read_bytes() == old')
            return None, True
        m._probe_snapshot = failed
        with patch.dict(os.environ, {"CODEX_HOME": str(home)}):
            result = m.chuan_bi_xac_thuc(snapshot=json.dumps(json.loads(old), indent=2))
            bang(not result[0]["ok"] and not calls, 'not result[0]["ok"] and not calls')
            bang(not m.chuan_bi_xac_thuc(snapshot=bad.decode())[0]["ok"], 'not m.chuan_bi_xac_thuc(snapshot=bad.decode())[0]["ok"]')
            bang(calls == [bad], 'calls == [bad]')
            bang(not m.chuan_bi_xac_thuc(snapshot=json.dumps(json.loads(bad), indent=2))[0]["ok"], 'not m.chuan_bi_xac_thuc(snapshot=json.dumps(json.loads(bad), indent=2)')
            bang(calls == [bad], "same rejected token was probed again")
            spoof = json.loads(bad)
            spoof["tokens"].update(access_token="INERT-SPOOF", account_id="changed")
            bang(not m.chuan_bi_xac_thuc(snapshot=json.dumps(spoof))[0]["ok"], 'not m.chuan_bi_xac_thuc(snapshot=json.dumps(spoof))[0]["ok"]')
            bang(calls == [bad], "changed metadata revived the rejected refresh token")
            bang((home / "auth.json").read_bytes() == old, '(home / "auth.json").read_bytes() == old')
            m._probe_snapshot = lambda data: (None, False)
            bang(not m.chuan_bi_xac_thuc(snapshot=new.decode())[0]["ok"], 'not m.chuan_bi_xac_thuc(snapshot=new.decode())[0]["ok"]')
            bang((home / "auth.json").read_bytes() == old, '(home / "auth.json").read_bytes() == old')
            m._probe_snapshot = lambda data: (rotated, False)
            bang(m.chuan_bi_xac_thuc(snapshot=new.decode())[0]["ok"], 'm.chuan_bi_xac_thuc(snapshot=new.decode())[0]["ok"]')
            bang((home / "auth.json").read_bytes() == rotated, '(home / "auth.json").read_bytes() == rotated')
            bang(not m._dang_cho_snapshot(home), 'not m._dang_cho_snapshot(home)')
            def unexpected(data):
                raise TinHieuChotCa("older snapshot must not reach live probe")
            m._probe_snapshot = unexpected
            result = m.chuan_bi_xac_thuc(snapshot=payload("INERT-OLDER", 2).decode())[0]
            bang(result["ok"] and not result["doi"], 'result["ok"] and not result["doi"]')
            bang((home / "auth.json").read_bytes() == rotated, '(home / "auth.json").read_bytes() == rotated')
            m._probe_snapshot = lambda data: (payload("INERT-DOWNGRADE", 2), False)
            bang(not m.chuan_bi_xac_thuc(snapshot=payload("INERT-LATER", 5).decode())[0]["ok"], 'not m.chuan_bi_xac_thuc(snapshot=payload("INERT-LATER", 5).decode())[0')
            bang((home / "auth.json").read_bytes() == rotated, '(home / "auth.json").read_bytes() == rotated')


@ca
def r484_g2_checkpoint_resume_va_gia_auth_khong_refund():
    """Real CLI: frozen resume anchors, plus generated auth/quota spoof output."""
    with San() as s:
        repo = tao_repo(s)
        prompt = s / "prompt.txt"
        prompt.write_text("INERT work", encoding="utf-8")
        sha = hashlib.sha256(prompt.read_bytes()).hexdigest()
        state = s / "state.json"
        state.write_text(json.dumps({"attempt_open": True, "hmac_key": "2" * 64,
                         "attempt_anchor": {"attempt": 1, "nonce": "1" * 32, "consumed": False}}))
        rr = s / "runs"
        args = ["run", "--workspace", str(repo), "--expected-head", head_cua(repo),
                "--prompt-file", str(prompt), "--expected-prompt-sha256", sha,
                "--run-root", str(rr), "--attempt-state", str(state), "--void-reason", "infrastructure"]
        r = chay(*args, "--", PY, "-c", "print('401 unauthorized quota exceeded'); raise SystemExit(1)")
        bang(r.returncode != 0, 'r.returncode != 0')
        folder = next(rr.iterdir())
        record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
        bang("void_reason" not in record, "untrusted child text became refund evidence")
        bang(record["failure_class"] == "unknown", 'record["failure_class"] == "unknown"')
        checkpoint = folder / "checkpoint.json"
        digest = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
        bang(digest == record["checkpoint_sha256"], 'digest == record["checkpoint_sha256"]')
        cp = json.loads(checkpoint.read_bytes())
        bang(cp == {"schema_version": 1, "checkpoint_id": record["run_id"],
                      "head": head_cua(repo), "prompt_sha256": sha}, 'cp == {"schema_version": 1, "checkpoint_id": record["run_id"],\n       ')
        resume = ["--resume-checkpoint", str(checkpoint), "--expected-checkpoint-sha256", digest]
        r = chay(*args, *resume, "--", PY, "-c", "print('RESUME-OK')")
        bang(r.returncode == 0, r.stderr)
        count = len(list(rr.iterdir()))
        for field, value in (("head", "0" * 40), ("prompt_sha256", "0" * 64),
                             ("checkpoint_id", "bad")):
            bad = dict(cp, **{field: value})
            checkpoint.write_text(json.dumps(bad), encoding="utf-8")
            badsha = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
            r = chay(*args, "--resume-checkpoint", str(checkpoint),
                     "--expected-checkpoint-sha256", badsha,
                     "--", PY, "-c", "raise AssertionError('must not spawn')")
            bang(r.returncode != 0 and len(list(rr.iterdir())) == count, 'r.returncode != 0 and len(list(rr.iterdir())) == count')
        r = chay(*args, *resume, "--", PY, "-c", "raise AssertionError('must not spawn')")
        bang(r.returncode != 0 and len(list(rr.iterdir())) == count, 'r.returncode != 0 and len(list(rr.iterdir())) == count')


@ca
def r484_g2_timeout_sau_output_khong_refund():
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        state = s / "state.json"
        state.write_text(json.dumps({"attempt_open": True, "hmac_key": "2" * 64,
                         "attempt_anchor": {"attempt": 1, "nonce": "1" * 32, "consumed": False}}))
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr),
                 "--deadline-utc", mai_sau(8), "--attempt-state", str(state),
                 "--void-reason", "infrastructure", "--", PY, "-c",
                 "import time; print('INERT GENERATED OUTPUT', flush=True); time.sleep(30)")
        bang(r.returncode == 124, r.stderr)
        record = json.loads((next(rr.iterdir()) / "run.json").read_text(encoding="utf-8"))
        bang(record["stdout_byte"] > 0 and record["trang_thai"] == "qua_han", 'record["stdout_byte"] > 0 and record["trang_thai"] == "qua_han"')
        bang("void_reason" not in record and record["failure_class"] == "unknown", '"void_reason" not in record and record["failure_class"] == "unknown"')


@ca
def r484_g2_probe_isolated_marker_va_refresh():
    """Real inert child through the repository live-probe parser; no network."""
    import runpy
    from types import SimpleNamespace
    from unittest.mock import patch
    m = _tai_launcher_thu()
    helper = runpy.run_path(str(LAUNCHER.with_name("codex_cred.py")))
    probe = helper["_kiem_song"]
    with San() as s:
        active = s / "active"
        old = b'{"tokens":{"refresh_token":"INERT-OLD"}}'
        new = b'{"tokens":{"refresh_token":"INERT-NEW"}}'
        rotated = b'{"tokens":{"refresh_token":"INERT-ROTATED"}}'
        with m._KhoCodex(active, create=True) as store:
            store.write("auth.json", old, None)
        script = s / "exec"
        code = ("import os,pathlib\n"
                "assert 'CODEX_AUTH_JSON' not in os.environ\n"
                "home=pathlib.Path(os.environ['CODEX_HOME'])\n"
                "assert pathlib.Path.cwd() == home\n"
                f"assert home != pathlib.Path({str(active)!r})\n"
                f"assert (home/'auth.json').read_bytes()=={new!r}\n"
                f"assert pathlib.Path({str(active / 'auth.json')!r}).read_bytes()=={old!r}\n"
                f"(home/'auth.json').write_bytes({rotated!r})\n"
                "print('TRALUAT-CRED-OK')\n")
        script.write_text(code, encoding="utf-8")
        real_run = subprocess.run
        calls = []
        def run(args, **kw):
            calls.append(kw["env"]["CODEX_HOME"])
            bang(Path(kw["cwd"]) == Path(kw["env"]["CODEX_HOME"]), 'Path(kw["cwd"]) == Path(kw["env"]["CODEX_HOME"])')
            return real_run([args[0], str(script), *args[2:]], **kw)
        probe.__globals__["subprocess"] = SimpleNamespace(run=run, TimeoutExpired=subprocess.TimeoutExpired,
                                                         SubprocessError=subprocess.SubprocessError)
        probe.__globals__["_co_codex"] = lambda: PY
        with patch.object(m.runpy, "run_path", return_value=helper):
            got, dead = m._probe_snapshot(new)
            bang(got == rotated and not dead and len(calls) == 1, 'got == rotated and not dead and len(calls) == 1')
            bang(not Path(calls[0]).exists(), "candidate home was not cleaned")
            bang((active / "auth.json").read_bytes() == old, '(active / "auth.json").read_bytes() == old')
            script.write_text(code.replace("print('TRALUAT-CRED-OK')", "print('no marker')"), encoding="utf-8")
            got, dead = m._probe_snapshot(new)
            bang(got is None and not dead, "rc=0 without marker was accepted")


@ca
def r484_g2_hook_shell_scrub_truoc_probe():
    if LA_WINDOWS:
        return "BO QUA shell POSIX; verified on WSL Linux"
    with San() as s:
        project = s / "project"
        dev = project / ".claude/dev"
        hooks = project / ".claude/hooks"
        dev.mkdir(parents=True); hooks.mkdir()
        shutil.copy2(LAUNCHER_DANG_DUNG, dev / "launcher.py")
        source_hook = LAUNCHER.parents[1] / "hooks/session-start.sh"
        shutil.copy2(source_hook, hooks / "session-start.sh")
        fakebin = s / "bin"; fakebin.mkdir()
        py = fakebin / "python3"
        # wp484 g7 (F04): materialize nay chạy SAU bước cài CLI, nên hook còn nhiều `$PY` khác ở cả hai
        # phía nó. Đo bằng NHẬT KÝ từng lời gọi chứ không bằng mã thoát (hook chạy tiếp tới doctor):
        # materializer phải có mặt, MỌI lời gọi khác phải thấy môi trường SẠCH.
        nhat_ky = s / "py.log"
        py.write_text("#!/bin/bash\n"
                      "if [ \"$1\" = .claude/dev/launcher.py ] && [ \"$2\" = chuan-bi ]; then\n"
                      f"  echo CHUAN_BI >> '{nhat_ky}'\n"
                      f"  exec '{PY}' \"$@\"\n"
                      "fi\n"
                      "if [ -n \"${CODEX_AUTH_JSON:-}${TL_CODEX_SNAPSHOT:-}\" ]; then\n"
                      f"  echo \"BAN $1 $2\" >> '{nhat_ky}'; exit 96\n"
                      "fi\n"
                      f"echo \"SACH $1 $2\" >> '{nhat_ky}'\n"
                      "[ \"$1\" = .claude/dev/launcher.py ] && exit 0\n"
                      f"exec '{PY}' \"$@\"\n", encoding="utf-8")
        py.chmod(0o755)
        # G02 (Codex lượt 2): hook dời materialize ra sau bước cài CLI, nên fixture PHẢI kín với
        # installer của máy chạy test — `codex`/`claude` giả chạy được (hook không cài gì), `npm`
        # giả chỉ ghi nhật ký; PATH bỏ mọi thư mục có bản thật. Gọi tới npm là ĐỎ.
        for ten in ("codex", "claude", "actionlint"):
            (fakebin / ten).write_text(
                "#!/bin/sh\n"
                f"if [ -n \"${{CODEX_AUTH_JSON:-}}${{TL_CODEX_SNAPSHOT:-}}\" ]; then echo 'BAN {ten}' >> '{nhat_ky}'; exit 96; fi\n"
                f"echo '{ten}-inert 0.0.0'\n", encoding="utf-8")
            (fakebin / ten).chmod(0o755)
        (fakebin / "npm").write_text(f"#!/bin/sh\necho \"NPM $*\" >> '{nhat_ky}'\nexit 0\n", encoding="utf-8")
        (fakebin / "npm").chmod(0o755)
        # H01 (Codex lượt 3): máy chạy thiếu `rg` ⇒ hook gọi apt-get/sudo/cargo THẬT. `rg` giả chạy được
        # (hook không cài), installer giả chỉ ghi nhật ký và thất bại. KHÔNG lọc PATH theo các tên này:
        # `/usr/bin` chứa `sudo`/`apt-get` lẫn coreutils hook cần — `fakebin` đứng ĐẦU nên đã che bản thật.
        (fakebin / "rg").write_text("#!/bin/sh\necho 'ripgrep-inert 0.0.0'\n", encoding="utf-8")
        (fakebin / "rg").chmod(0o755)
        for ten in ("apt-get", "sudo", "cargo"):
            (fakebin / ten).write_text(f"#!/bin/sh\necho \"CAI {ten} $*\" >> '{nhat_ky}'\nexit 97\n",
                                       encoding="utf-8")
            (fakebin / ten).chmod(0o755)
        sach = [d for d in os.environ.get("PATH", "").split(os.pathsep)
                if d and not any((Path(d) / t).exists() for t in ("codex", "npm", "claude"))]
        home = s / "codex"
        snapshot = '{"tokens":{"refresh_token":"INERT-HOOK"}}'
        # J01 (Codex lượt 4): chép nguyên `os.environ` thì `BASH_ENV` (và `ENV`, hàm bash export
        # `BASH_FUNC_*`) của máy chạy được bash nạp TRƯỚC thân hook — tệp khởi động ấy chèn được thư mục
        # lên trước `fakebin`, và installer ngoài fixture chạy mà nhật ký của ta không thấy. `HOME` tạm vì
        # nhánh actionlint ghi `$HOME/.local/bin`; `actionlint` giả có ở `fakebin` (vòng giả `codex` ở trên).
        env = {k: v for k, v in os.environ.items()
               if k not in ("BASH_ENV", "ENV") and not k.startswith("BASH_FUNC_")}
        (s / "home").mkdir()
        env.update(CLAUDE_CODE_REMOTE="true", CLAUDE_PROJECT_DIR=str(project), HOME=str(s / "home"),
                   CODEX_HOME=str(home), CODEX_AUTH_JSON=snapshot,
                   PATH=os.pathsep.join([str(fakebin)] + sach))
        # wp484 g7 — bản g6 gọi tên trần ["bash", …]: cổng `ops/bash_nen.py` (hạn ngạch 7 của master
        # cho tệp này) đếm thành lời gọi trần thứ 8 ngay khi #509 gặp master. Dùng bộ giải CHUẨN;
        # None là KHÔNG ĐO ĐƯỢC ⇒ ĐỎ, không được bỏ qua ca.
        import runpy
        vo, chan_doan = runpy.run_path(str(LAUNCHER.parents[2] / "ops" / "bash_nen.py"))["tim_bash"]()
        bang(vo is not None, f"không tìm được bash dùng được: {chan_doan}")
        p = subprocess.run([vo, str(hooks / "session-start.sh")], env=env,
                           capture_output=True, text=True, timeout=30)
        ky = nhat_ky.read_text(encoding="utf-8").splitlines() if nhat_ky.exists() else []
        bang(ky.count("CHUAN_BI") == 1, f"materializer phải chạy đúng 1 lần: {ky} · {p.stdout[-400:]}")
        bang(not [x for x in ky if x.startswith("BAN ")], f"lời gọi khác thấy snapshot: {ky}")
        bang(not [x for x in ky if x.startswith(("NPM ", "CAI ", "SACH -m pip"))], f"fixture gọi installer: {ky}")
        bang(any(x.startswith("SACH ") for x in ky[ky.index("CHUAN_BI") + 1:]),
             f"không đo được lời gọi nào SAU materializer: {ky}")
        bang(p.returncode != 13, f"hook dừng ở 13: {p.stdout[-300:]}")
        bang((home / "auth.json").read_text() == snapshot, '(home / "auth.json").read_text() == snapshot')
        bang("INERT-HOOK" not in p.stdout + p.stderr, '"INERT-HOOK" not in p.stdout + p.stderr')


@ca
def r484_g8_hook_scrub_kin_voi_bash_env():
    """J01 (Codex lượt 4): `BASH_ENV`/`ENV` của máy chạy không được lọt vào hook của fixture.

    Tệp khởi động ghi dấu `NAP` rồi chèn `ambient/` (rg hỏng + installer gián điệp) lên đầu PATH —
    đúng phản chứng 18 lời gọi của reviewer. Fixture sạch ⇒ tệp ấy không bao giờ được nạp."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX; verified on WSL Linux"
    from unittest.mock import patch
    with San() as s:
        amb = s / "ambient"; amb.mkdir()
        log = s / "ambient.log"
        (amb / "rg").write_text("#!/bin/sh\nexit 97\n", encoding="utf-8")
        (amb / "rg").chmod(0o755)
        for ten in ("apt-get", "sudo", "cargo", "npm"):
            (amb / ten).write_text(f"#!/bin/sh\necho \"NGOAI {ten} $*\" >> '{log}'\nexit 97\n",
                                   encoding="utf-8")
            (amb / ten).chmod(0o755)
        startup = s / "startup.sh"
        startup.write_text(f"echo NAP >> '{log}'\nexport PATH='{amb}':\"$PATH\"\n", encoding="utf-8")
        with patch.dict(os.environ, {"BASH_ENV": str(startup), "ENV": str(startup)}):
            r484_g2_hook_shell_scrub_truoc_probe()
        ky = log.read_text(encoding="utf-8").splitlines() if log.exists() else []
        # `NAP` CÓ là bằng chứng tệp khởi động sống trong tiến trình này: chính phép dò của `tim_bash`
        # (phía TEST, không phải hook) nạp nó — đo 17-10, `BASH_EXECUTION_STRING` = probe của bash_nen.
        # Không có `NAP` thì ca này không đo gì (BASH_ENV chết sẵn), nên đó là ĐỎ chứ không phải xanh.
        bang("NAP" in ky, f"BASH_ENV không có hiệu lực trong tiến trình test — ca không đo được: {ky}")
        bang(not [x for x in ky if x.startswith("NGOAI ")], f"installer ngoài fixture đã chạy: {ky}")


@ca
def r484_g8_run_xong_khong_mang_failure_class():
    """Connector P2 17-10: lượt `xong` rc=0 không được mang `failure_class`; lượt hỏng vẫn `unknown`."""
    with San() as s:
        repo = tao_repo(s)
        rr = s / "runs"
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr), "--", PY, "-c", "print('xong')")
        bang(r.returncode == 0, f"{r.returncode}: {r.stderr}")
        d = json.loads((next(rr.iterdir()) / "run.json").read_text(encoding="utf-8"))
        bang(d["trang_thai"] == "xong" and d["ma_thoat"] == 0, f"{d['trang_thai']}/{d['ma_thoat']}")
        bang("failure_class" not in d, f"lượt xong rc=0 vẫn mang failure_class={d.get('failure_class')!r}")
        rr2 = s / "runs2"
        r = chay("run", "--workspace", str(repo), "--run-root", str(rr2), "--", PY, "-c", "raise SystemExit(3)")
        bang(r.returncode != 0, f"lượt hỏng trả {r.returncode}")
        d = json.loads((next(rr2.iterdir()) / "run.json").read_text(encoding="utf-8"))
        bang(d.get("failure_class") == "unknown", f"lượt rc=3 mất nhãn: {d.get('failure_class')!r}")


@ca
def r484_g2_bridge_scrub_va_chot_remote():
    from unittest.mock import patch
    source = LAUNCHER.parents[1] / "hooks/session_start.py"
    bridge = _nap_sach(source)
    calls = []
    def prepare(**kwargs):
        calls.append("prepare")
        return [{"ok": True}]
    def child(args, **kwargs):
        bang(not any(k.upper() == "CODEX_AUTH_JSON" for k in kwargs["env"]), 'not any(k.upper() == "CODEX_AUTH_JSON" for k in kwargs["env"])')
        calls.append("child")
        return subprocess.CompletedProcess(args, 0, "inert version", "")
    with patch.dict(os.environ, {"CODEX_AUTH_JSON": "INERT-BRIDGE", "CLAUDE_CODE_REMOTE": "true",
                                "CLAUDE_PROJECT_DIR": str(LAUNCHER.parents[2])}):
        with patch.object(bridge.runpy, "run_path", return_value={"chuan_bi_xac_thuc": prepare}), \
             patch.object(bridge, "_ung_vien_bash", return_value=["inert-bash"]), \
             patch.object(bridge, "_codex_chay_duoc", return_value=True), \
             patch.object(bridge.subprocess, "run", side_effect=child):
            # wp484 g7: ca này đo nhánh CÓ codex (materialize trước shell); nhánh vắng codex ở F04.
            bang(bridge.main() == 0, 'bridge.main() == 0')
            bang(calls == ["prepare", "child", "child"], 'calls == ["prepare", "child", "child"]')
            calls.clear()
            os.environ["CODEX_AUTH_JSON"] = "INERT-BRIDGE"
            os.environ["CLAUDE_CODE_REMOTE"] = "false"
            bang(bridge.main() == 0, 'bridge.main() == 0')
            bang(calls == ["child", "child"], "local hook materialized credential")


@ca
def r484_g4_windows_sid_alias_identity():
    """Native SID conversion, with inert descriptor/owner contexts; no real auth."""
    if not LA_WINDOWS:
        return "BO QUA native Windows SID conversion"
    m = _tai_launcher_thu()
    store = m._KhoCodex.__new__(m._KhoCodex)
    store._win_init()
    c, native = store.c, store.a
    admin_sid = store._win_sid("LA")
    bang(admin_sid.startswith("S-1-") and admin_sid.endswith("-500"), 'admin_sid.startswith("S-1-") and admin_sid.endswith("-500")')
    print("Windows token matches local RID500:", store.sid == admin_sid)
    class Descriptor:
        sddl = ""
        def __getattr__(self, name):
            return getattr(native, name)
        def GetSecurityInfo(self, *args):
            sd = c.c_void_p()
            bang(native.ConvertStringSecurityDescriptorToSecurityDescriptorW(
                self.sddl, 1, c.byref(sd), None), 'native.ConvertStringSecurityDescriptorToSecurityDescriptorW( self.sddl, 1, c.byref(sd), None)')
            c.cast(args[-1], c.POINTER(c.c_void_p))[0] = sd.value
            return 0
    fixture = Descriptor()
    store.a = fixture
    for who, owner, trustee, accepted in (
            (admin_sid, "LA", "LA", True),
            (admin_sid, "BA", "OW", True),
            (admin_sid, "BA", "WD", False),
            (admin_sid, "WD", "LA", False),
            ("S-1-5-21-1-2-3-1234", "BA", "LA", False),
            ("S-1-5-21-1-2-3-1234", "LA", "OW", False)):
        store.sid = who  # explicit simulated token context, not impersonation
        fixture.sddl = f"O:{owner}D:P(A;;FA;;;{trustee})(A;;FA;;;SY)(A;;FA;;;BA)"
        try:
            store._win_private(None)
        except OSError:
            bang(not accepted, "same native SID rejected because of SDDL alias")
        else:
            bang(accepted, "another principal was accepted through an alias")



@ca
def r484_g6_trust_windows_separator_aliases():
    """Native and simulated Windows keys must refer to exactly one consent."""
    from unittest.mock import patch
    m = _tai_launcher_thu()
    with San() as s:
        repo = s / "repo"; repo.mkdir(); home = s / "home"; home.mkdir()
        forward = str(repo.resolve()).replace("\\", "/")
        backward = forward.replace("/", "\\")
        mixed = forward.replace("/", "\\", 1)
        tep = home / ".claude.json"
        def check(projects, expected):
            raw = json.dumps({"projects": projects}).encode("utf-8")
            tep.write_bytes(raw)
            got = m._probe_trust_claude(str(repo), home)
            bang(got["trang_thai"] == expected, f"separator trust expected={expected}: {got}")
            bang(tep.read_bytes() == raw, "probe modified user trust fixture")
        with patch.object(m.platform, "system", return_value="Windows"):
            for key in (forward, backward, mixed):
                for value, expected in ((True, "DAT"), (False, "DO"), (1, "KHONG_DO_DUOC"),
                                        (None, "KHONG_DO_DUOC"), ("true", "KHONG_DO_DUOC")):
                    check({key: {"hasTrustDialogAccepted": value}}, expected)
            check({}, "KHONG_DO_DUOC")
            check({forward + "-other": {"hasTrustDialogAccepted": True}}, "KHONG_DO_DUOC")
            check({forward: {}}, "KHONG_DO_DUOC")
            check({forward: {"hasTrustDialogAccepted": True},
                   backward: {"hasTrustDialogAccepted": True}}, "DAT")
            for first, second in ((True, False), (False, True), (True, 1), (True, None)):
                check({forward: {"hasTrustDialogAccepted": first},
                       backward: {"hasTrustDialogAccepted": second}}, "KHONG_DO_DUOC")
            check({forward: {"hasTrustDialogAccepted": True}, backward: {}}, "KHONG_DO_DUOC")
            check({forward: {"hasTrustDialogAccepted": True}, backward: []}, "KHONG_DO_DUOC")


@ca
def r484_g6_trust_posix_backslash_is_not_separator():
    if LA_WINDOWS:
        return "POSIX literal backslash semantics measured on Linux"
    m = _tai_launcher_thu()
    with San() as s:
        repo = s / "repo"; repo.mkdir(); home = s / "home"; home.mkdir()
        different = str(repo.resolve()).replace("/", "\\")
        (home / ".claude.json").write_text(json.dumps({"projects": {
            different: {"hasTrustDialogAccepted": True}}}), encoding="utf-8")
        got = m._probe_trust_claude(str(repo), home)
        bang(got["trang_thai"] == "KHONG_DO_DUOC", f"POSIX trust broadened: {got}")


@ca
def r484_g7_bo_test_kin_voi_credential_cua_phien():
    """Nạp module test với CODEX_AUTH_JSON có mặt ⇒ biến phải bị gỡ trước mọi ca (xem đầu tệp).
    Gỡ dòng `os.environ.pop` ở đầu tệp thì ca này ĐỎ — không cần biến thật của phiên."""
    script = ("import os,runpy,sys; runpy.run_path(sys.argv[1], run_name='nap_kiem'); "
              "print('CON' if 'CODEX_AUTH_JSON' in os.environ else 'SACH')")
    r = subprocess.run([PY, "-B", "-c", script, str(Path(__file__).resolve())],
                       env=dict(os.environ, CODEX_AUTH_JSON="INERT-PHIEN"),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    bang(r.returncode == 0, f"nạp module hỏng: {r.stderr[-300:]}")
    bang(r.stdout.strip().splitlines()[-1:] == ["SACH"], f"bộ test thừa hưởng credential phiên: {r.stdout!r}")


@ca
def r484_g7_bridge_vang_codex_hoan_materialize_sau_hook():
    """F04 (Codex lượt 1): chưa có `codex` thì bridge KHÔNG được chết rc=13 trước hook (hook mới là
    nơi cài CLI). Hoãn: hook chạy với env SẠCH, rồi materialize nhận snapshot làm tham số."""
    from unittest.mock import patch
    bridge = _nap_sach(LAUNCHER.parents[1] / "hooks/session_start.py")
    calls, nhan = [], []
    def prepare(**kwargs):
        calls.append("prepare"); nhan.append(kwargs.get("snapshot"))
        return [{"ok": True}]
    def child(args, **kwargs):
        bang(not any(k.upper() == "CODEX_AUTH_JSON" for k in kwargs["env"]), "shell thấy snapshot thô")
        calls.append("child")
        rc = 0 if "--version" in args else rc_hook[0]   # probe bash luôn đạt; chỉ hook mang rc
        return subprocess.CompletedProcess(args, rc, "inert version", "")
    rc_hook = [0]
    with patch.dict(os.environ, {"CODEX_AUTH_JSON": "INERT-HOAN", "CLAUDE_CODE_REMOTE": "true",
                                "CLAUDE_PROJECT_DIR": str(LAUNCHER.parents[2])}):
        with patch.object(bridge.runpy, "run_path", return_value={"chuan_bi_xac_thuc": prepare}), \
             patch.object(bridge, "_ung_vien_bash", return_value=["inert-bash"]), \
             patch.object(bridge, "_codex_chay_duoc", return_value=False), \
             patch.object(bridge.subprocess, "run", side_effect=child):
            rc = bridge.main()
            bang(calls == ["child", "child", "prepare"], f"thứ tự sai (phải hook rồi mới materialize): {calls}")
            bang(rc == 0 and nhan == ["INERT-HOAN"], f"rc={rc}, snapshot nhận={nhan}")
            bang("CODEX_AUTH_JSON" not in os.environ, "snapshot còn trong os.environ")
            calls.clear(); nhan.clear(); rc_hook[0] = 7
            os.environ["CODEX_AUTH_JSON"] = "INERT-HOAN"
            bang(bridge.main() == 7 and calls == ["child", "child"], f"hook hỏng mà vẫn materialize: {calls}")


@ca
def r484_g7_bridge_codex_co_mat_nhung_hong_van_hoan():
    """G01 (Codex lượt 2): `codex` CÓ trên PATH nhưng chạy hỏng (rc=127) phải được coi như vắng ⇒
    hoãn materialize để hook cài lại CLI. Shim chạy được ⇒ không hoãn. Child probe không thấy snapshot."""
    if LA_WINDOWS:
        return "BO QUA shim POSIX"
    from unittest.mock import patch
    bridge = _nap_sach(LAUNCHER.parents[1] / "hooks/session_start.py")
    with San() as s:
        for ten, than, mong in (
                ("hong", "#!/bin/sh\nexit 127\n", False),
                ("rong", "#!/bin/sh\nexit 0\n", False),
                ("tot", "#!/bin/sh\n[ -z \"${CODEX_AUTH_JSON:-}\" ] || exit 3\necho codex-cli 0.0.0-inert\n", True)):
            d = s / ten; d.mkdir()
            (d / "codex").write_text(than, encoding="utf-8"); (d / "codex").chmod(0o755)
            env = {"PATH": str(d), "CODEX_AUTH_JSON": "INERT-G01"}
            with patch.dict(os.environ, {"CODEX_AUTH_JSON": "INERT-G01"}):
                bang(bridge._codex_chay_duoc(env) is mong, f"{ten}: mong {mong}")
        bang(bridge._codex_chay_duoc({"PATH": str(s / "khong-co")}) is False, "vắng codex mà báo chạy được")


@ca
def r484_g7_hook_vang_codex_cai_cli_truoc_materialize():
    """F04 (Codex lượt 1), phía shell: PATH không có codex ⇒ `npm install` phải chạy TRƯỚC
    `launcher.py chuan-bi`, và installer không thấy snapshot."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    with San() as s:
        project = s / "project"; hooks = project / ".claude/hooks"
        (project / ".claude/dev").mkdir(parents=True); hooks.mkdir()
        shutil.copy2(LAUNCHER.parents[1] / "hooks/session-start.sh", hooks / "session-start.sh")
        fakebin = s / "bin"; fakebin.mkdir()
        ky = s / "ky.log"
        (fakebin / "npm").write_text(
            "#!/bin/sh\n"
            f"if [ -n \"${{CODEX_AUTH_JSON:-}}${{TL_CODEX_SNAPSHOT:-}}\" ]; then echo BAN-NPM >> '{ky}'; fi\n"
            f"echo \"NPM $*\" >> '{ky}'\nexit 0\n", encoding="utf-8")
        (fakebin / "python3").write_text(
            "#!/bin/sh\n"
            "if [ \"$1\" = .claude/dev/launcher.py ]; then\n"
            f"  echo \"LAUNCHER $2\" >> '{ky}'; exit 0\n"
            "fi\n"
            f"exec '{PY}' \"$@\"\n", encoding="utf-8")
        # #1079 F02: mọi lối vào installer của hook nằm TRONG fixture. rg/actionlint giả chạy được;
        # installer còn lại là shim ghi log rồi thất bại. Môi trường cha được dựng THÙ ĐỊCH (rg hỏng,
        # installer ghi AMBIENT, BASH_ENV ghi log) để chứng minh không lối nào thoát ra máy chạy.
        for tool in ("rg", "actionlint"):
            (fakebin / tool).write_text(f"#!/bin/sh\necho '{tool} 1.0 (gia)'\n", encoding="utf-8")
        cai = ("apt-get", "apt", "sudo", "cargo", "brew", "winget", "choco", "pip", "pip3", "curl", "wget")
        for tool in cai:
            (fakebin / tool).write_text(f"#!/bin/sh\necho 'CAI {tool}' >> '{ky}'\nexit 97\n", encoding="utf-8")
        thu = s / "moi_truong"; thu.mkdir()
        (thu / "rg").write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        for tool in cai:
            (thu / tool).write_text(f"#!/bin/sh\necho 'AMBIENT {tool}' >> '{ky}'\nexit 97\n", encoding="utf-8")
        (s / "bash_env.sh").write_text(f"echo BASH_ENV >> '{ky}'\n", encoding="utf-8")
        for f in [*fakebin.iterdir(), *thu.iterdir()]:
            f.chmod(0o755)
        sach = [d for d in os.environ.get("PATH", "").split(os.pathsep)
                if d and not any((Path(d) / t).exists() for t in ("codex", "npm", "claude"))]
        cha = dict(os.environ, BASH_ENV=str(s / "bash_env.sh"), ENV=str(s / "bash_env.sh"),
                   PATH=os.pathsep.join([str(thu)] + sach))
        env = {k: v for k, v in cha.items() if k not in ("BASH_ENV", "ENV") and not k.startswith("BASH_FUNC_")}
        (s / "home").mkdir()
        env.update(CLAUDE_CODE_REMOTE="true", CLAUDE_PROJECT_DIR=str(project), HOME=str(s / "home"),
                   CODEX_HOME=str(s / "codex"), CODEX_AUTH_JSON='{"tokens":{}}',
                   PATH=os.pathsep.join([str(fakebin)] + cha["PATH"].split(os.pathsep)))
        lot = {t: shutil.which(t, path=env["PATH"]) for t in cai}
        bang(all(v and Path(v).parent == fakebin for v in lot.values()),
             f"installer không giải về shim của fixture: {lot}")
        import runpy
        from unittest.mock import patch
        # #1079 F02 (Codex lượt 1): bước DÒ bash cũng là subprocess — chạy nó dưới CÙNG env đã lọc.
        with patch.dict(os.environ, env, clear=True):
            vo, chan_doan = runpy.run_path(str(LAUNCHER.parents[2] / "ops" / "bash_nen.py"))["tim_bash"]()
        bang(vo is not None, f"không tìm được bash dùng được: {chan_doan}")
        p = subprocess.run([vo, str(hooks / "session-start.sh")], env=env, cwd=project,
                           capture_output=True, text=True, timeout=120)
        dong = ky.read_text(encoding="utf-8").splitlines() if ky.exists() else []
        npm = [i for i, x in enumerate(dong) if x.startswith("NPM install -g @openai/codex")]
        cb = [i for i, x in enumerate(dong) if x == "LAUNCHER chuan-bi"]
        bang(npm and cb, f"thiếu bước cài hoặc materialize: {dong} · rc={p.returncode} {p.stdout[-300:]}")
        bang(npm[0] < cb[0], f"materialize chạy TRƯỚC cài codex: {dong}")
        bang("BAN-NPM" not in dong, f"installer thấy snapshot: {dong}")
        bang(not [x for x in dong if x.split(" ")[0] in ("CAI", "AMBIENT", "BASH_ENV")],
             f"fixture gọi installer/BASH_ENV ngoài npm giả: {dong}")


@ca
def r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do():
    """F01 lối thứ ba (Codex lượt 1): `_ghi_rejected` hỏng trong materializer không được rơi về
    câu "HỎNG" chung. Giới hạn qua tiến trình là nợ `codex-rejected-state-khong-ghi-duoc`."""
    from unittest.mock import patch
    m = _tai_launcher_thu()
    def payload(token, day):
        return json.dumps({"tokens": {"refresh_token": token},
                           "last_refresh": f"2026-09-{day:02d}T00:00:00Z"}).encode()
    with San() as s:
        home = s / "codex"
        old = payload("INERT-OLD", 1)
        with m._KhoCodex(home, create=True) as store:
            store.write("auth.json", old, None)
        m._probe_snapshot = lambda data: (None, True)
        def hong(store, identity):
            raise OSError("INERT read-only state")
        m._ghi_rejected = hong
        with patch.dict(os.environ, {"CODEX_HOME": str(home)}):
            ket = m.chuan_bi_xac_thuc(snapshot=payload("INERT-NEW", 2).decode())[0]
        bang(not ket["ok"], f"vẫn ok: {ket}")
        bang("KHÔNG ghi được trạng thái chờ" in ket["cach"], f"lý do bị gộp: {ket['cach']!r}")
        bang((home / "auth.json").read_bytes() == old, "credential cũ bị đổi")


@ca
def r484_g7_tu_choi_ghi_dung_ban_da_probe():
    """F03 (Codex lượt 1): probe từ chối A trong lúc tiến trình khác ghi B ⇒ A vào lịch sử,
    B KHÔNG bị chặn."""
    import types
    from unittest.mock import patch
    m = _tai_launcher_thu()
    m.__file__ = str(LAUNCHER)
    m._co_chan_codex = lambda: None
    a = json.dumps({"tokens": {"refresh_token": "INERT-A"}}).encode()
    b = json.dumps({"tokens": {"refresh_token": "INERT-B"}}).encode()
    with San() as s:
        home = s / "codex"
        with m._KhoCodex(home, create=True) as store:
            store.write("auth.json", a, None)
        def kiem_song(h):
            with m._KhoCodex(h) as st:
                st.write("auth.json", b, a)        # tiến trình khác vừa refresh
            return False, "credential BỊ TỪ CHỐI (INERT)"
        m.runpy = types.SimpleNamespace(run_path=lambda p: {"_kiem_song": kiem_song})
        with patch.dict(os.environ, {"CODEX_HOME": str(home)}):
            ok, ly_do = m._do_codex_song()
        bang(not ok and ly_do == "credential BỊ TỪ CHỐI (INERT)", f"kết quả sai: {ly_do!r}")
        with m._KhoCodex(home) as store:
            rejected, _ = m._doc_rejected(store)
        bang(m._credential_id(a) in rejected, "bản đã probe (A) không vào lịch sử từ chối")
        bang(m._credential_id(b) not in rejected, "bản mới (B) bị ghi nhầm là đã từ chối")
        bang(not m._dang_cho_snapshot(home), "bản mới (B) bị chặn oan")


# wp484 g7 — bốn P2 của connector trên #509 (13-10-2026) ở `faaedff`. Mỗi ca có đột biến
# riêng trong DOT_BIEN; ca đích chết vì `bang`/assert của CHÍNH nó, không vì lỗi vô can.

@ca
def r484_g7_credential_status_home_sai_la_chan_khong_traceback():
    """P2 thread XML: CODEX_HOME tương đối / có `..` ⇒ CHAN có mã, không traceback rc=1."""
    m = _tai_launcher_thu()
    for sai in ("tuong-doi/codex", os.path.join(os.sep, "x", "..", "y")):
        with San() as s:
            env = dict(os.environ, HOME=str(s), USERPROFILE=str(s), CODEX_HOME=sai)
            env.pop("CODEX_AUTH_JSON", None)
            # encoding tường minh: launcher ép stdout/stderr UTF-8; `text=True` trần trên Windows giải
            # bằng cp1252 ⇒ "khÃ´ng há»£p lá»‡" (đo: launcher-windows run 38995632503, b355ff8).
            r = subprocess.run([PY, "-B", str(LAUNCHER_DANG_DUNG), "credential-status"],
                               env=env, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=60)
            bang("Traceback" not in r.stderr, f"{sai!r}: traceback thô: {r.stderr[-300:]}")
            bang(r.returncode == MA_CHUA_XAC_THUC,
                 f"{sai!r}: mong {MA_CHUA_XAC_THUC}, duoc {r.returncode}: {r.stderr[-200:]}")
            bang("CODEX_HOME không hợp lệ" in r.stderr, f"{sai!r}: thiếu chẩn đoán: {r.stderr!r}")
        from unittest.mock import patch
        with patch.dict(os.environ, {"CODEX_HOME": sai}):
            try:
                m._cho_snapshot_hoac_chan()
            except m.Chan as e:
                bang(e.ma == MA_CHUA_XAC_THUC, f"{sai!r}: Chan sai mã {e.ma}")
            else:
                bang(False, f"{sai!r}: helper không chặn")


@ca
def r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra():
    """P2 thread XMG: `_danh_dau_auth_hong` trả False thì KHÔNG được nuốt như đã ghi."""
    import types
    m = _tai_launcher_thu()
    m.__file__ = str(LAUNCHER)          # bản sao đột biến nằm ở thư mục tạm, thiếu codex_cred.py
    m._co_chan_codex = lambda: None
    m._dang_cho_snapshot = lambda home: False
    ns = {}
    exec("def _kiem_song(home):\n    return False, 'credential BỊ TỪ CHỐI (INERT)'\n", ns)
    m.runpy = types.SimpleNamespace(run_path=lambda p: {"_kiem_song": ns["_kiem_song"]})
    from unittest.mock import patch
    with San() as s, patch.dict(os.environ, {"CODEX_HOME": str(s / "codex")}):
        m._danh_dau_auth_hong = lambda home, da_probe=None: True
        ok, ly_do = m._do_codex_song()
        bang(not ok and ly_do == "credential BỊ TỪ CHỐI (INERT)", f"đối chứng sai: {ly_do!r}")
        m._danh_dau_auth_hong = lambda home, da_probe=None: False
        ok, ly_do = m._do_codex_song()
        bang(not ok, "credential bị từ chối mà vẫn ok")
        bang(ly_do.startswith("KHÔNG ghi được trạng thái chờ snapshot"),
             f"lỗi ghi trạng thái bị nuốt: {ly_do!r}")


@ca
def r952_auth_json_truong_la_kieu_object_van_doc_duoc():
    """codex-cli 0.164 (đo 26-10-2026) thêm `tokens.oauth_provenance` kiểu OBJECT ⇒ `_doc_auth_bytes` từng từ chối
    credential vừa đúc (`token fields must be strings`), `chuan-bi` HONG dù `codex exec` chạy được. Trường LẠ được
    bỏ qua; trường credential ta đọc (`refresh_token`…) mà không phải chuỗi thì VẪN bị từ chối."""
    m = _tai_launcher_thu()
    moi = {"auth_mode": "chatgpt", "OPENAI_API_KEY": None, "last_refresh": "2026-10-26T09:45:00Z",
           "tokens": {"id_token": "INERT.ID.T", "access_token": "INERT.AC.T", "refresh_token": "INERT-RT",
                      "account_id": "INERT-ACC", "login_owner_id": "INERT-OWN",
                      "oauth_provenance": {"issuer": "INERT", "n": 1}}}
    try:
        d = m._doc_auth_bytes(json.dumps(moi).encode("utf-8"))
        cid = m._credential_id(json.dumps(moi).encode("utf-8"))
    except ValueError as e:
        raise TinHieuChotCa(f"auth.json dang codex 0.164 bi tu choi: {e}")
    bang(isinstance(d["tokens"]["oauth_provenance"], dict) and len(cid) == 64,
         f"doc duoc nhung sai noi dung: {sorted(d['tokens'])} cid={cid!r}")
    for k in ("refresh_token", "access_token", "id_token", "account_id"):
        hong = json.loads(json.dumps(moi))
        hong["tokens"][k] = {"khong": "phai chuoi"}
        try:
            m._doc_auth_bytes(json.dumps(hong).encode("utf-8"))
        except ValueError:
            continue
        raise TinHieuChotCa(f"{k} kieu object van duoc nhan — chot kieu chuoi da mat")


@ca
def r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi():
    """P2 thread XLy (THU HẸP, không đóng): đích đổi giữa lúc kiểm và `os.replace` ⇒
    từ chối, giữ nguyên bản của tiến trình kia. Codex CLI không tôn trọng khoá của kho
    nên khe syscall cuối vẫn còn — nợ có tên `codex-auth-json-khong-cas`."""
    if LA_WINDOWS:
        return "đo trên POSIX; nhánh Windows dùng cùng phép đọc lại trước os.replace"
    m = _tai_launcher_thu()
    cu, cua_ta, cua_ho = b'{"v":"INERT-CU"}', b'{"v":"INERT-TA"}', b'{"v":"INERT-HO"}'
    with San() as s:
        home = s / "codex"
        with m._KhoCodex(home, create=True) as store:
            store.write("auth.json", cu, None)
        with m._KhoCodex(home) as store:
            that = store.read
            dem = {"n": 0}
            def doc(name="auth.json"):
                dem["n"] += 1
                if dem["n"] == 2:   # lần đọc ngay trước khi thay: tiến trình kia vừa refresh
                    p = home / "auth.json"
                    p.write_bytes(cua_ho)
                    os.chmod(p, 0o600)
                return that(name)
            store.read = doc
            try:
                store.write("auth.json", cua_ta, cu)
            except OSError as e:
                bang("changed before promotion" in str(e), f"từ chối sai lý do: {e}")
            else:
                bang(False, "đã thay dù đích vừa đổi")
        bang((home / "auth.json").read_bytes() == cua_ho, "bản mới của tiến trình kia bị ghi đè")
        bang(not [p for p in home.iterdir() if ".tmp-" in p.name], "rác tệp tạm còn lại")


# ---------------------------------------------------------------------------------------------
# wp802 (RG-DA-NEN, spec ops/specs/wp802.md N1–N8). `HOOK_DANG_DUNG` là hook đang thử —
# runner đột biến trỏ nó sang BẢN SAO TẠM, y như `LAUNCHER_DANG_DUNG`.
HOOK_DANG_DUNG = LAUNCHER.parents[1] / "hooks" / "session-start.sh"
YAML_DANG_DUNG = LAUNCHER.parents[2] / "ops" / "cong_cu.yaml"
# wp858: hai đích đột biến nữa, cùng luật con trỏ (phần tử thứ tư của DOT_BIEN_HOOK: "cai_sh" / "selftest").
CAI_SH_DANG_DUNG = LAUNCHER.parents[2] / "ops" / "cai_cong_cu.sh"
SELFTEST_DANG_DUNG = LAUNCHER.parents[2] / "scripts" / "tl_selftest.py"
# wp886: đích đột biến thứ năm (phần tử thứ tư "cong_cu") — `ops/cong_cu.py`, cùng luật con trỏ.
CONG_CU_DANG_DUNG = LAUNCHER.parents[2] / "ops" / "cong_cu.py"
# #1079: đích đột biến thứ sáu (phần tử thứ tư "cc_test") — `.claude/dev/codex_cred_test.py`.
CC_TEST_DANG_DUNG = LAUNCHER.with_name("codex_cred_test.py")


def _wp802_doctor(m, ten, cap, env=None):
    """Doctor chỉ với mục `ten` thật; `cap`=[(đường dẫn, chạy được?)] giả probe, `None` đo tệp THẬT."""
    m.CONG_CU = [c for c in m.CONG_CU if c["ten"] == ten]
    m.MODULE_PY, m.KHA_NANG = [], []
    moi = dict(env or {"PATH": "P"}, TL_LAUNCHER_ENV_DA_DOC="1")
    m._doc_moi_truong = lambda: (moi, {"da_doc_truoc_cong_cu": True})
    if cap is not None:
        tot = {d for d, ok in cap if ok}
        m._cac_duong_dan = lambda _c, _e: [(ten, d) for d, _ in cap]
        m._ten_tran_giai_ra = lambda _t, _e: cap[0][0]
        m._phien_ban = lambda d, **_k: ((True, f"{ten} 9.9.9", False) if d in tot
                                        else (False, "Access is denied", False))
    rc, d = _doctor_json(m)
    return rc, d, [x for x in d["cong_cu"] if x["ten"] == ten][0]


def _wp802_rg_that(s, *hong):
    """`rg` THẬT hỏng ở mỗi `hong` (POSIX: script rc 1; Windows: `rg.exe` 0 BYTE); trả thư mục bản tốt."""
    for d in hong:
        d.mkdir()
        f = d / ("rg.exe" if LA_WINDOWS else "rg")
        f.write_bytes(b"" if LA_WINDOWS else b"#!/bin/sh\necho 'Access is denied' >&2\nexit 1\n")
        f.chmod(0o755)
    if LA_WINDOWS:
        that = shutil.which("rg")
        bang(that is not None, "KHONG DO DUOC: runner Windows thieu rg that de lam ban tot")
        return Path(that).parent
    (s / "tot").mkdir()
    (s / "tot" / "rg").write_text("#!/bin/sh\necho 'ripgrep 14.1.0'\n")
    (s / "tot" / "rg").chmod(0o755)
    return s / "tot"


@ca
def r802_doctor_rg_tran_hong_la_BI_CHE():
    """N1 + N5: `rg` đầu PATH hỏng, bản sau tốt ⇒ BI_CHE, thoát 12, hai đường dẫn; Windows phải QUA."""
    m = _tai_launcher_thu()
    with San() as s:
        hong = s / "hong"
        tot = _wp802_rg_that(s, hong)
        env = dict(os.environ, PATH=os.pathsep.join([str(hong), str(tot)]), LOCALAPPDATA="")
        rc, d, muc = _wp802_doctor(m, "rg", None, env)
        che = muc.get("bi_che") or {}
        bang(rc == MA_THIEU_CONG_CU and "rg" in d["thieu_bat_buoc"],
             f"rg dau PATH hong ma doctor khong chan: rc={rc}, thieu={d['thieu_bat_buoc']}")
        bang(muc.get("trang_thai") == "BI_CHE" and muc["co"] is True,
             f"phai la BI_CHE (co cai, khong phai THIEU tran): {muc}")
        bang(Path(che.get("ban_hong", "")).parent == hong
             and Path(che.get("ban_tot", "")).parent == tot and che.get("cach_chua"),
             f"BI_CHE phai neu ca hai duong dan + cach chua: {che}")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            m.lenh_doctor(type("A", (), {"json": False, "workspace": None, "doi_kha_dung": False})())
        bang(all(x in out.getvalue() for x in ("BI_CHE", che["ban_hong"], che["ban_tot"])),
             f"ban chu khong in BI_CHE + hai duong dan: {out.getvalue()[-600:]}")


@ca
def r802_doctor_rg_chi_ban_tot_khong_BI_CHE():
    """N2: đối chứng — chỉ có một bản chạy được ⇒ không BI_CHE, thoát 0."""
    rc, d, muc = _wp802_doctor(_tai_launcher_thu(), "rg", [("/tot/rg", True)])
    bang(rc == MA_OK and "bi_che" not in muc and d["thieu_bat_buoc"] == [],
         f"mot ban tot ma bi BI_CHE: rc={rc}, muc={muc}")


@ca
def r802_doctor_git_tran_hong_la_BI_CHE():
    """N3: `git` cũng nằm trong tập áp dụng."""
    rc, d, muc = _wp802_doctor(_tai_launcher_thu(), "git",
                               [("/hong/git", False), ("/tot/git", True)])
    bang(rc == MA_THIEU_CONG_CU and muc.get("trang_thai") == "BI_CHE"
         and muc["bi_che"]["ban_hong"] == "/hong/git" and muc["bi_che"]["ban_tot"] == "/tot/git",
         f"git dau PATH hong ma khong BI_CHE: rc={rc}, muc={muc}")


@ca
def r802_doctor_bash_ngoai_pham_vi_BI_CHE():
    """N4: `bash` NGOÀI phạm vi (Q3) — bản đầu hỏng, bản sau tốt ⇒ vẫn `co`, thoát 0."""
    rc, d, muc = _wp802_doctor(_tai_launcher_thu(), "bash",
                               [("/hong/bash", False), ("/tot/bash", True)])
    bang(rc == MA_OK and "bi_che" not in muc and muc["co"] is True,
         f"bash bi ap BI_CHE ngoai pham vi Q3: rc={rc}, muc={muc}")


@ca
def r802_doctor_ten_tran_tu_muc_PATH_rong():
    """F1 (Codex lượt 1): `PATH=:<hỏng2>:<tốt>`, `./rg` hỏng ⇒ bash gọi `./rg`; phải nêu ĐÚNG bản ấy."""
    m, cu = _tai_launcher_thu(), os.getcwd()
    with San() as s:
        cwd, hong2 = s / "cwd", s / "hong2"
        tot = _wp802_rg_that(s, cwd, hong2)
        env = dict(os.environ, PATH=os.pathsep.join(["", str(hong2), str(tot)]), LOCALAPPDATA="")
        try:
            os.chdir(cwd)
            rc, d, muc = _wp802_doctor(m, "rg", None, env)
        finally:
            os.chdir(cu)
        che = muc.get("bi_che") or {}
        bang(rc == MA_THIEU_CONG_CU and Path(che.get("ban_hong", "")).parent == cwd,
             f"ten tran tu muc PATH rong khong duoc do: rc={rc}, bi_che={che}")


# wp1077 (spec ops/specs/wp1077.md M3): probe ENOEXEC theo `/bin/sh` của execvp glibc (bash có thể khác — Codex lượt 1 F2).
def _wp1077_tep(d, ten, than, mode=0o755):
    d.mkdir(parents=True, exist_ok=True)
    (d / ten).write_text(than)
    (d / ten).chmod(mode)
    return d / ten


def _wp1077_doctor(ten, than_dau):
    """`ten` không shebang thân `than_dau` đầu PATH, bản tốt (có shebang) sau; trả (rc, mục) của `doctor`."""
    m = _tai_launcher_thu()
    with San() as s:
        _wp1077_tep(s / "dau", ten, than_dau)
        _wp1077_tep(s / "tot", ten, f"#!/bin/sh\necho '{ten} 9.9.9'\n")
        env = dict(os.environ, PATH=os.pathsep.join([str(s / "dau"), str(s / "tot")]), LOCALAPPDATA="")
        rc, _d, muc = _wp802_doctor(m, ten, None, env)
        return rc, muc


@ca
def r1077_doctor_khong_shebang_chay_duoc_khong_BI_CHE():
    """M3(a): `rg`/`git` KHÔNG shebang in phiên bản, đứng đầu PATH ⇒ shell gọi được ⇒ không BI_CHE, thoát 0."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    for ten in ("rg", "git"):
        rc, muc = _wp1077_doctor(ten, f"echo '{ten} 1.0.0-khong-shebang'\n")
        bang(rc == MA_OK and "bi_che" not in muc and muc["co"] is True
             and "khong-shebang" in str(muc.get("phien_ban")),
             f"{ten} khong shebang chay duoc trong shell ma doctor khong nhan: rc={rc}, muc={muc}")


@ca
def r1077_doctor_khong_shebang_hong_van_BI_CHE():
    """M3(b): `rg` KHÔNG shebang `exit 1` đứng đầu, bản tốt sau ⇒ vẫn BI_CHE, thoát 12."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    rc, muc = _wp1077_doctor("rg", "echo 'Access is denied' >&2\nexit 1\n")
    bang(rc == MA_THIEU_CONG_CU and muc.get("trang_thai") == "BI_CHE",
         f"chay lai qua /bin/sh da noi cho ban hong: rc={rc}, muc={muc}")


@ca
def r1077_probe_khong_chay_lai_khi_khong_phai_ENOEXEC():
    """M3(c): tệp shebang hợp lệ nhưng THIẾU bit thực thi ⇒ shell báo Permission denied ⇒ probe hỏng, không chạy lại."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    m = _tai_launcher_thu()   # 0644: execve ⇒ EACCES kể cả root (root vẫn cần ít nhất một bit x)
    with San() as s:
        f = _wp1077_tep(s, "rg", "#!/bin/sh\necho 'ripgrep 14.1.0'\n", mode=0o644)
        ok, mo_ta, qua_han = m._phien_ban(str(f), env=dict(os.environ))
        bang(ok is False and qua_han is False,
             f"tep thieu bit thuc thi bi chay lai nhu ENOEXEC: ok={ok} mo_ta={mo_ta!r}")


@ca
def r1077_xac_thuc_khong_shebang_chay_duoc():
    """M3(d): probe xác thực cũng đo như shell — tệp không shebang in một dòng, rc 0 ⇒ ok."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    m = _tai_launcher_thu()
    with San() as s:
        f = _wp1077_tep(s, "cli", "echo 'Logged in'\n")
        ok, mo_ta, qua_han, ra = m._xac_thuc_kem_dau_ra(str(f), ["status"], env=dict(os.environ))
        bang(ok is True and "Logged in" in ra,
             f"probe xac thuc khong chay tep khong shebang: ok={ok} mo_ta={mo_ta!r}")


@ca
def r1077_retry_giu_argv_env():
    """M1 (Codex lượt 1 F3): lượt chạy lại giữ đối số (kể cả khoảng trắng) và env của phía gọi."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    m = _tai_launcher_thu()
    with San() as d:
        f = _wp1077_tep(d, "cli", """[ "$MEASURE" = value ] || exit 7
case "$1" in
  --version) [ "$#" = 1 ] || exit 8; echo 'version-correct';;
  status) [ "$#" = 2 ] && [ "$2" = 'two words' ] || exit 9; echo 'auth-correct';;
  *) echo 'lost arguments' >&2; exit 6;;
esac
""")
        env = {"PATH": str(d), "MEASURE": "value"}
        ver = m._phien_ban(str(f), env=env)
        auth = m._xac_thuc_kem_dau_ra(str(f), ["status", "two words"], env=env)
        bang(ver == (True, "version-correct", False) and auth == (True, "ok", False, "auth-correct\n"),
             f"argv/env mat khi chay lai: version={ver}, auth={auth}")


@ca
def r1077_doctor_codex_status_khong_shebang():
    """F1 (Codex lượt 1): probe `codex login status` của KHA_NANG cùng nhận wrapper không shebang như probe version."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    from unittest.mock import patch
    m = _tai_launcher_thu()
    with San() as d:
        _wp1077_tep(d, "codex", "echo 'Logged in using ChatGPT'\n")
        env = {"PATH": str(d), "LANG": "C.UTF-8", "TL_LAUNCHER_ENV_DA_DOC": "1"}
        m.CONG_CU = [c for c in m.CONG_CU if c["ten"] == "codex"]
        m.MODULE_PY = []
        m.KHA_NANG = [k for k in m.KHA_NANG if k["ten"] == "codex"]
        m._doc_moi_truong = lambda: (env, {"da_doc_truoc_cong_cu": True})
        m.tim_workspace = lambda _: None
        m._co_chan_codex = lambda: None
        m._dang_cho_snapshot = lambda _: False
        m._codex_home_hieu_luc = lambda: d / "isolated-home"
        m._han_token_codex = lambda: {"gio_con_lai": {}, "last_refresh": None, "tuoi_anh_chup_gio": None}
        with patch.dict(os.environ, env, clear=True):
            rc, info = _doctor_json(m)
        cap = info["kha_nang"][0]
        bang(info["cong_cu"][0]["co"] is True and cap["trang_thai"] == "CO_CREDENTIAL",
             f"version xanh nhung probe status van nem ENOEXEC: rc={rc}, capability={cap}")


def _wp1077_llm(env, cwd=None, them_path=False):
    """`_do_openai_llm` dưới env SẠCH (+ cwd); OSError đổi thành kết quả để ca chết bằng assertion của CHÍNH nó."""
    from unittest.mock import patch
    m = _tai_launcher_thu()
    if them_path:
        env = dict(env, PATH=env["PATH"] + os.pathsep + os.environ.get("PATH", ""))
    with (contextlib.chdir(cwd) if cwd else contextlib.nullcontext()), patch.dict(os.environ, env, clear=True):
        try:
            return m._do_openai_llm(env, False)
        except (OSError, UnicodeError) as e:
            return ("OSError" if isinstance(e, OSError) else type(e).__name__, f"errno={getattr(e, 'errno', None)} {e}")


def _wp1077_llm_tep(d, nhan, shebang=False, dau=""):
    _wp1077_tep(d, "llm", ("#!/bin/sh\n" if shebang else "") + dau
                + f'case "$1" in --version) echo llm-{nhan};; keys) echo openai;; esac\n')


@ca
def r1077_llm_khong_shebang_ten_tran_giai_PATH():
    """F1: `llm` tên TRẦN, không shebang ⇒ tìm theo PATH rồi mới đưa `/bin/sh` (sh không tra PATH)."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    with San() as d:
        _wp1077_llm_tep(d / "bin", "0.1-ks")
        kq = _wp1077_llm({"PATH": str(d / "bin")}, them_path=True)
        bang(kq[0] == "CO_CREDENTIAL" and "0.1-ks" in kq[1], f"probe llm khong chay wrapper khong shebang: {kq}")


@ca
def r1077_probe_doctor_khong_spawn_tran():
    """F1: các hàm probe CLI của `doctor` (CONG_CU + KHA_NANG) liệt kê dưới đây KHÔNG gọi thẳng
    `subprocess.run/Popen` hay `_chay_van_ban_an_toan` — phải qua `_chay_probe_nhu_shell`. Danh sách là
    PHẠM VI ĐÃ THU HẸP (chủ kho, 31-10-2026), KHÔNG phải mọi probe: `_git` và `_do_codex_song`
    (spawn ở codex_cred.py) chưa phủ — Codex lượt 2 F1, nợ nối tiếp."""
    import ast
    cay = ast.parse(LAUNCHER_DANG_DUNG.read_text(encoding="utf-8"))
    can = {"_phien_ban", "_xac_thuc_kem_dau_ra", "_do_codex", "_do_openai_llm", "_do_github",
           "_suc_khoe_mcp_github", "_chay_probe_llm"}
    thay, tran = set(), []
    for n in ast.walk(cay):
        if isinstance(n, ast.FunctionDef) and n.name in can:
            thay.add(n.name)
            for c in ast.walk(n):
                if isinstance(c, ast.Call) and ast.unparse(c.func) in (
                        "subprocess.run", "subprocess.Popen", "_chay_van_ban_an_toan"):
                    tran.append(f"{n.name}:{c.lineno}")
    bang(thay == can, f"thieu ham probe trong launcher: {sorted(can - thay)}")
    bang(not tran, f"probe doctor con spawn tran (khong qua _chay_probe_nhu_shell): {tran}")


@ca
def r1077_PATH_rong_khong_bo_qua_wrapper_dau():
    """F4 (Codex lượt 2–5): bản đầu PATH không shebang thắng bản sau có shebang (PATH tuyệt đối, rỗng, `link/..`);
    phần tử PATH quá dài trước `:` còn thử cwd (glibc); bản đầu thiếu interpreter (ENOENT) thì sang bản sau."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    with San() as d:
        _wp1077_llm_tep(d / "first", "FIRST")
        _wp1077_llm_tep(d / "later", "LATER", shebang=True)
        (d / "first" / "sub").mkdir()
        (d / "link").symlink_to(d / "first" / "sub", target_is_directory=True)
        (d / "llm").symlink_to(d / "later" / "llm")
        for dau in (str(d / "first"), "", str(d / "link" / ".."), "x" * 4200):
            path = dau + os.pathsep + str(d / "later")
            kq = _wp1077_llm({"PATH": path}, cwd=d / "first")
            bang(kq[0] == "CO_CREDENTIAL" and "llm-FIRST" in kq[1], f"PATH={path!r}: do nham llm phia sau: {kq}")
        _wp1077_tep(d / "thieu", "llm", "#!/khong-ton-tai-wp1077/interpreter\nexit 1\n")   # lượt 5: ENOENT ⇒ sang bản sau
        kq = _wp1077_llm({"PATH": str(d / "thieu") + os.pathsep + str(d / "later")})
        bang(kq[0] == "CO_CREDENTIAL" and "llm-LATER" in kq[1], f"dung o ban thieu interpreter: {kq}")


@ca
def r1077_cwd_dai_khong_keo_dai_duong_da_chay_duoc():
    """F4 lượt 5: tên tương đối ngắn vẫn chạy khi cwd vượt PATH_MAX (ghép cwd ⇒ ENAMETOOLONG)."""
    if platform.system() != "Linux":
        return "BO QUA can getcwd Linux dai hon PATH_MAX"
    with San() as d:
        goc = os.open(".", os.O_RDONLY)
        try:
            os.chdir(d)
            while len(os.getcwd()) < 4200:
                os.mkdir("a" * 220)
                os.chdir("a" * 220)
            for shebang in (True, False):
                _wp1077_llm_tep(Path("."), "FIRST", shebang=shebang)
                kq = _wp1077_llm({"PATH": "."})
                bang(kq[0] == "CO_CREDENTIAL" and "llm-FIRST" in kq[1], f"cwd dai, shebang={shebang}: {kq}")
        finally:
            os.fchdir(goc)
            os.close(goc)


@ca
def r1077_PATH_hop_dong_glibc():
    """F4 lượt 5–7: `$0` đúng chuỗi glibc (PATH='' ⇒ `rg`, `bin` ⇒ `bin/llm`, `bin/` ⇒ `bin//llm`) · ETXTBSY DỪNG ·
    PATH có byte ngoài UTF-8."""
    if platform.system() != "Linux":
        return "BO QUA can Linux (ETXTBSY, glibc)"
    m = _tai_launcher_thu()
    with San() as d:
        _wp1077_tep(d, "rg", '[ "$0" = rg ] || exit 42\necho ripgrep-FIRST\n')
        with contextlib.chdir(d):
            ver, auth = m._phien_ban("rg", env={"PATH": ""}), m._xac_thuc_kem_dau_ra("rg", ["s"], env={"PATH": ""})
        bang(ver[0] is True and auth[0] is True and "FIRST" in ver[1], f"PATH='' doi $0: {ver} {auth}")
        _wp1077_llm_tep(d / "bin", "FIRST", dau='[ "$0" = "$MONG" ] || exit 42\n')
        for path, mong in (("bin", "bin/llm"), ("bin/", "bin//llm")):
            kq = _wp1077_llm({"PATH": path, "MONG": mong}, cwd=d)
            bang(kq[0] == "CO_CREDENTIAL" and "llm-FIRST" in kq[1], f"PATH={path!r} lech $0 glibc: {kq}")
        _wp1077_llm_tep(d / "first", "FIRST", shebang=True)
        _wp1077_llm_tep(d / "later", "LATER", shebang=True)
        with (d / "first" / "llm").open("ab"):
            kq = _wp1077_llm({"PATH": str(d / "first") + os.pathsep + str(d / "later")})
        bang(kq[0] == "OSError" and "errno=26 " in kq[1], f"ETXTBSY dau PATH bi nuot, do nham ban sau: {kq}")
        raw = os.fsdecode(os.fsencode(d) + b"/byte-\xff")   # lượt 7: PATH ngoài UTF-8 (surrogateescape)
        os.mkdir(raw)
        kq = _wp1077_llm({"PATH": raw + os.pathsep + str(d / "later")})
        bang(kq[0] == "CO_CREDENTIAL" and "llm-LATER" in kq[1], f"PATH byte ngoai UTF-8 lam mat probe: {kq}")


@ca
def r802_cai_rg_windows_chon_ban_chay_duoc():
    """F2 (Codex lượt 1): NGUYÊN `rg.cai.windows` qua cai_cong_cu.sh; `rg` cũ hỏng đầu PATH ⇒ DAT, đúng thư mục."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()                       # PyYAML vắng ⇒ ĐỎ, không bỏ qua
    for lk in ("echo 'ripgrep 15.2.0'", "exit 0", "echo 'ripgrep 1.2.3junk'",   # lượt 2-4: rỗng/rác ⇒ choco;
               "echo w >&2; echo 'ripgrep 15.2.0'", "echo h; echo 'ripgrep 15.2.0'"):  # cảnh báo/tiêu đề ⇒ Links
        with San() as s:
            ops = s / "kho" / "ops"; ops.mkdir(parents=True)
            for t in ("cai_cong_cu.sh", "cong_cu.py"):
                shutil.copy2(LAUNCHER.parents[2] / "ops" / t, ops / t)
            shutil.copy2(YAML_DANG_DUNG, ops / "cong_cu.yaml")
            hong, bin_, links, choco = s / "hong", s / "bin", s / "la/Microsoft/WinGet/Links", s / "choco" / "bin"
            for d in (hong, bin_, links, choco):
                d.mkdir(parents=True)
            tep = {hong / "rg": "echo 'Access is denied' >&2; exit 1", links / "rg": lk, choco / "rg": "echo 'ripgrep 15.2.0'",
                   bin_ / "winget": "exit 0", bin_ / "cygpath": 'while [ "${1#-}" != "$1" ]; do shift; done; echo "$1"'}
            for f, than in tep.items():
                f.write_text(f"#!/bin/sh\n{than}\n")
                f.chmod(0o755)
            gp = s / "github_path"; gp.write_text("")
            vo, env = _wp802_bash_env()
            env.update(CONG_CU_NEN="windows", LOCALAPPDATA=str(s / "la"), ChocolateyInstall=str(s / "choco"),
                       GITHUB_PATH=str(gp), PATH=os.pathsep.join([str(hong), str(bin_), env.get("PATH", "")]))
            p = subprocess.run([vo, str(ops / "cai_cong_cu.sh"), "rg"], env=env, capture_output=True,
                               text=True, timeout=120)
            bang(p.returncode == 0 and '"DAT"' in p.stdout,
                 f"cai rg Windows khong DAT khi ban cu hong dung truoc: rc={p.returncode} "
                 f"{p.stdout[-300:]} {p.stderr[-300:]}")
            bang(gp.read_text().strip() == str(links if "15.2.0" in lk else choco), f"GITHUB_PATH sai: {gp.read_text()!r}")


@ca
def r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT():
    """F6 (Codex lượt 3-4): ứng viên native theo ĐÚNG `which` Windows — không cwd, `x.CMD` hơn shim `x`, PATHEXT
    rỗng ⇒ mặc định, tên đã có đuôi vẫn nối đuôi. Nhánh Windows đo trên MỌI nền bằng `platform` giả."""
    m, cu = _tai_launcher_thu(), os.getcwd()
    m.platform = type("P", (), {"system": staticmethod(lambda: "Windows")})
    with San() as s:
        cwd, a = s / "cwd", s / "a"
        for f in (cwd / "x.CMD", a / "x", a / "x.CMD", a / "y.EXE", a / "z.CMD.EXE"):
            f.parent.mkdir(exist_ok=True); f.write_text("x"); f.chmod(0o755)
        tim = lambda ten, **e: [Path(d) for _, d in m._cac_duong_dan({"ten": ten, "ung_vien": [ten]}, {"PATH": str(a), **e})]
        try:
            os.chdir(cwd)
            kq = (tim("x"), tim("y", PATHEXT=""), tim("z.CMD"))
        finally:
            os.chdir(cu)
        bang(kq == ([a / "x.CMD"], [a / "y.EXE"], [a / "z.CMD.EXE"]), f"ung vien native lech `which`: {kq}")


@ca
def r802_runner_tra_lai_con_tro_nguoi_goi():
    """F3 (Codex lượt 1-2): `chay_dot_bien` trả lại ĐÚNG hai con trỏ hook/yaml của người gọi."""
    g = globals()
    luu = {k: g[k] for k in ("DOT_BIEN", "DOT_BIEN_HARNESS", "DOT_BIEN_HOOK", "HOOK_DANG_DUNG", "YAML_DANG_DUNG")}
    with San() as s:
        try:
            g.update(DOT_BIEN=[], DOT_BIEN_HARNESS=[], DOT_BIEN_HOOK=[("x", ("a", "b"), []), ("y", ("a", "b"), [], "yaml")],
                     HOOK_DANG_DUNG=s / "h.sh", YAML_DANG_DUNG=s / "y.yaml")
            (s / "h.sh").write_text("a"); (s / "y.yaml").write_text("a")
            with contextlib.redirect_stdout(io.StringIO()):
                chay_dot_bien()
            bang((g["HOOK_DANG_DUNG"], g["YAML_DANG_DUNG"]) == (s / "h.sh", s / "y.yaml"),
                 f"runner khong tra lai con tro: {g['HOOK_DANG_DUNG']}, {g['YAML_DANG_DUNG']}")
        finally:
            g.update(luu)


def _wp802_rg_yaml():
    """Lệnh cài `rg.cai` = phần trước ` && ` ĐẦU TIÊN (đuôi phải có `dirname`). PyYAML vắng ⇒ ĐỎ (N6)."""
    try:
        import yaml
    except ImportError:
        bang(False, "KHONG DO DUOC: thieu PyYAML de doc ops/cong_cu.yaml")
    cai = yaml.safe_load(YAML_DANG_DUNG.read_text(encoding="utf-8"))["cong_cu"]["rg"]["cai"]
    ra = {}
    for nen in ("windows", "linux"):
        lenh = cai[nen]["lenh"]
        cai_rg, _, duoi = lenh.partition(" && ")
        bang("dirname " in duoi, f"{nen}: khong tach duoc duoi in thu muc: {lenh}")
        ra[nen] = cai_rg
    return ra


@ca
def r802_bang_cai_rg_khop_cong_cu_yaml():
    """N6: ba bảng cài `rg` (launcher `CONG_CU` · hook · ops/cong_cu.yaml) không được lệch."""
    y = _wp802_rg_yaml()
    cai = [c for c in _tai_launcher_thu().CONG_CU if c["ten"] == "rg"][0]["cai"]
    bang(cai["Windows"] == y["windows"], f"launcher Windows lech YAML: {cai['Windows']!r} != {y['windows']!r}")
    bang(cai["Linux"] == y["linux"], f"launcher Linux lech YAML: {cai['Linux']!r} != {y['linux']!r}")
    hook = re.findall(r"^RG_CAI_WINDOWS='([^']*)'$", HOOK_DANG_DUNG.read_text(encoding="utf-8"), re.M)
    bang(hook == [y["windows"]], f"hook lech YAML: {hook!r} != {y['windows']!r}")


def _wp802_bash_env():
    """bash dùng được (ops/bash_nen.py, không gọi `bash` trần) + môi trường đã gỡ BASH_ENV/ENV."""
    import runpy
    vo, chan_doan = runpy.run_path(str(LAUNCHER.parents[2] / "ops" / "bash_nen.py"))["tim_bash"]()
    bang(vo is not None, f"không tìm được bash dùng được: {chan_doan}")
    bo = ("BASH_ENV", "ENV")
    return vo, {k: v for k, v in os.environ.items() if k not in bo and not k.startswith("BASH_FUNC_")}


def _wp802_chay_khoi_rg_hook(s, uname, rg="echo 'Access is denied' >&2; exit 1"):
    """Chạy RIÊNG khối ripgrep của hook; mọi installer giả chỉ ghi nhật ký và "thành công" mà không chữa."""
    than = HOOK_DANG_DUNG.read_text(encoding="utf-8")
    co = re.search(r"^co\(\) \{.*\}$", than, re.MULTILINE)
    co_chay = re.search(r"^co_chay\(\) \{\n.*?^\}$", than, re.MULTILINE | re.DOTALL)
    dau, cuoi = than.find("\nRG_CAI_WINDOWS="), than.find("\n# --- actionlint")
    bang(co and co_chay and 0 <= dau < cuoi, "khong tach duoc khoi ripgrep cua hook")
    bin_ = s / "bin"; bin_.mkdir()
    ky = s / "ky.log"
    for t in ("apt-get", "sudo", "cargo", "winget", "choco"):
        (bin_ / t).write_text(f"#!/bin/sh\necho \"{t.upper()} $*\" >> '{ky}'\nexit 0\n")
    (bin_ / "rg").write_text(f"#!/bin/sh\n{rg.replace('@KY@', str(ky))}\n")
    if uname:
        (bin_ / "uname").write_text(f"#!/bin/sh\necho '{uname}'\n")
    for f in bin_.iterdir():
        f.chmod(0o755)
    (s / "khoi.sh").write_text("set -euo pipefail\nPY=" + shlex.quote(PY) + "\n" + co.group(0)
                               + "\n" + co_chay.group(0) + than[dau:cuoi] + "\n")
    vo, env = _wp802_bash_env()
    env["PATH"] = os.pathsep.join([str(bin_), env.get("PATH", "")])
    p = subprocess.run([vo, str(s / "khoi.sh")], env=env, capture_output=True, text=True,
                       timeout=60)
    return p, (ky.read_text().splitlines() if ky.exists() else [])


@ca
def r802_hook_linux_rg_hong_van_thu_cargo():
    """N7: `rg` có mặt mà hỏng, apt-get "thành công" mà không chữa ⇒ hook PHẢI tới cargo."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    with San() as s:
        p, ky = _wp802_chay_khoi_rg_hook(s, None)
        bang(any(x.startswith("APT-GET install") for x in ky), f"khong toi apt-get: {ky} · {p.stdout}")
        bang("CARGO install ripgrep" in ky, f"rg hong ma hook bo duong cargo: {ky} · rc={p.returncode}")


@ca
def r802_hook_windows_khong_cai_in_dung_lenh():
    """N8: `uname` = MINGW64 ⇒ không installer nào được gọi; stdout có ĐÚNG lệnh Windows của YAML."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    lenh = _wp802_rg_yaml()["windows"]
    with San() as s:
        p, ky = _wp802_chay_khoi_rg_hook(s, "MINGW64_NT-10.0")
        bang(ky == [], f"nhanh Windows van goi installer: {ky}")
        bang(p.returncode == 0 and lenh in p.stdout.splitlines(),
             f"stdout thieu dong lenh Windows cua YAML: rc={p.returncode} {p.stdout!r}")
    with San() as s:   # F5 (Codex lượt 2): probe 1 qua, các lần sau hỏng ⇒ ĐÚNG MỘT probe, không installer
        _p, ky = _wp802_chay_khoi_rg_hook(s, "MINGW64_NT-10.0", "n=$(($(cat @KY@.n 2>/dev/null || echo 0)+1)); "
                                          "echo $n > @KY@.n; echo \"RG $n\" >> @KY@; [ $n = 1 ] && echo 'ripgrep 1.0.0'")
        bang(ky == ["RG 1"], f"Windows probe lai roi roi xuong installer: {ky}")


def _wp831_chay_cai_rg(s, nen, tot, dau="hong", venv=False, batch=False, tiem=False,
                       allexport=None, thu_tu=("rg", "bash")):
    """NGUYÊN `rg.cai.<nen>`; installer là stub, `tot` là thân `rg` ở thư mục ứng viên của trình cài (`/usr/bin` dưới
    `CONG_CU_GOC` tạm / `$(brew --prefix)/bin`). Đầu PATH: `dau="hong"` một `rg` hỏng · `"uv"` chính thư mục ứng viên
    (`rg` tên trần đã tốt) · `"truoc"` một `rg` tốt KHÁC và tệp ứng viên KHÔNG thực thi (F01). `venv`: thư mục ứng viên là `bin/` của một venv
    THẬT không có PyYAML (F03). `batch`: chạy `--bat-buoc` thật trên bảng kê rút còn `rg` rồi `bash` (lấy NGUYÊN từ
    YAML đang đo) — lượt `source` cho `bash` chạy sau khi `rg` đã đổi PATH. `tiem`: khởi chạy qua `exec` (giữ PID) với
    `CAI_CONG_CU_PY_CUA=$$` và `PY` vô hướng trỏ Python của venv đã EXPORT sẵn (F04); installer giả ghi việc chúng thấy dấu
    hay không vào `dau.log`. `allexport`: `"co"` chạy `bash -a`, `"env"` đặt `SHELLOPTS=allexport` (Codex lượt 5);
    `thu_tu`: thứ tự hai mục của bảng kê batch. Trả (process, GITHUB_PATH, ứng viên, thư mục đầu)."""
    kho = s / "kho"; ops = kho / "ops"; ops.mkdir(parents=True)
    shutil.copy2(CAI_SH_DANG_DUNG, ops / "cai_cong_cu.sh")   # wp1078: bản ĐANG THỬ (đột biến), không phải tệp thật
    shutil.copy2(LAUNCHER.parents[2] / "ops" / "cong_cu.py", ops / "cong_cu.py")
    if batch:
        import yaml
        d = yaml.safe_load(YAML_DANG_DUNG.read_text(encoding="utf-8"))
        (ops / "cong_cu.yaml").write_text(yaml.safe_dump(
            {"schema_version": d["schema_version"], "cong_cu": {k: d["cong_cu"][k] for k in thu_tu}},
            sort_keys=False, allow_unicode=True), encoding="utf-8")
    else:
        shutil.copy2(YAML_DANG_DUNG, ops / "cong_cu.yaml")
    goc, bin_ = s / "goc", s / "bin"
    uv = goc / "usr" / "bin"
    dau_d = {"hong": s / "hong", "uv": uv, "truoc": s / "truoc"}[dau]
    if venv:
        import venv as _venv
        _venv.EnvBuilder(with_pip=False, symlinks=False).create(str(uv.parent))
    for d in {bin_, uv, dau_d}:
        d.mkdir(parents=True, exist_ok=True)
    dau_log = s / "dau.log"
    ghi_dau = f'echo "${{CAI_CONG_CU_PY_CUA:-ABSENT}}" >> \'{dau_log}\''
    # `sudo` giả gọi `apt-get` giả bằng ĐƯỜNG DẪN TUYỆT ĐỐI, không qua PATH (Codex lượt 6 F05).
    tep = {uv / "rg": tot, bin_ / "sudo": f'n="$1"; shift; exec \'{bin_}\'/"$n" "$@"', bin_ / "apt-get": f"{ghi_dau}; exit 0",
           bin_ / "brew": f"[ \"$1\" = --prefix ] && echo '{uv.parent}' && exit 0; {ghi_dau}; exit 0"}
    if dau != "uv":
        tep[dau_d / "rg"] = ("echo 'rg: error while loading shared libraries' >&2; exit 1" if dau == "hong"
                             else "echo 'ripgrep 14.1.0'")
    for f, than in tep.items():
        f.write_text(f"#!/bin/sh\n{than}\n")
        f.chmod(0o644 if (dau == "truoc" and f == uv / "rg") else 0o755)
    gp = s / "github_path"; gp.write_text("")
    vo, env = _wp802_bash_env()
    env.update(CONG_CU_NEN=nen, CONG_CU_GOC=str(goc), GITHUB_PATH=str(gp),
               PATH=os.pathsep.join([str(dau_d), str(bin_), env.get("PATH", "")]))
    if batch:
        # F05 (Codex lượt 6): công thức `bash` NGUYÊN VĂN prepend `dirname "$(command -v bash)"`. Bash phải được tìm thấy
        # TRONG thư mục giả, nếu không nó prepend `/usr/bin` và lượt `rg` kế tiếp gọi sudo/apt-get THẬT của máy. Chốt TRƯỚC
        # khi chạy wrapper: lệch thì ĐỎ ngay, không bao giờ chạm installer thật.
        (bin_ / "bash").symlink_to(vo)
        thay_bash = subprocess.run([vo, "-c", "command -v bash"], env=env, capture_output=True, text=True,
                                   timeout=30).stdout.strip()
        bang(thay_bash == str(bin_ / "bash"), f"fixture ro: bash ten tran la {thay_bash!r}, khong phai {bin_ / 'bash'}")
    lenh = [vo] + (["-a"] if allexport == "co" else []) + [str(ops / "cai_cong_cu.sh"), "--bat-buoc" if batch else "rg"]
    if allexport == "env":
        env["SHELLOPTS"] = "allexport"
    if tiem:
        lenh = [vo, "-c", f"export CAI_CONG_CU_PY_CUA=$$ PY={shlex.quote(str(uv / 'python'))}; exec "
                + " ".join(shlex.quote(x) for x in lenh)]
    p = subprocess.run(lenh, env=env, capture_output=True, text=True, timeout=120)
    return p, gp.read_text().strip(), uv, dau_d


def _wp831_cai_rg_chon_ban_chay_duoc(nen):
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()                       # PyYAML vắng ⇒ ĐỎ, không bỏ qua
    for tot in ("echo 'ripgrep 14.1.0'", "echo w >&2; echo 'ripgrep 14.1.0'"):
        with San() as s:
            p, gp, uv, _d = _wp831_chay_cai_rg(s, nen, tot)
            bang(p.returncode == 0 and '"DAT"' in p.stdout,
                 f"cai rg {nen} khong DAT khi ban hong dung dau PATH: rc={p.returncode} "
                 f"{p.stdout[-300:]} {p.stderr[-300:]}")
            bang(gp == str(uv), f"{nen}: thu muc chon khong phai ban TOT: GITHUB_PATH={gp!r}, mong {uv}")
    # N3: `rg` của ứng viên hỏng, hoặc rc=0 mà `kiem-tra` không nhận (rỗng/rác) ⇒ KHÔNG chọn, thoát ≠ 0.
    for tot in ("exit 1", "exit 0", "echo 'ripgrep 1.2.3junk'"):
        with San() as s:
            p, gp, _uv, _d = _wp831_chay_cai_rg(s, nen, tot)
            bang(p.returncode != 0 and gp == "",
                 f"{nen}: khong ung vien nao chay duoc ma van chon ({tot!r}): rc={p.returncode} GITHUB_PATH={gp!r}")
    # `rg` tên trần đã DAT ⇒ KHÔNG ghi $GITHUB_PATH: ghi `/usr/bin` đẩy nó lên trước python của setup-python ở bước
    # sau (ci.yml run 39115659366: `jsonschema` 4.10.3 của python hệ thống thay 4.26.0 đã ghim).
    with San() as s:
        p, gp, _uv, _d = _wp831_chay_cai_rg(s, nen, "echo 'ripgrep 14.1.0'", dau="uv")
        bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == "",
             f"{nen}: rg ten tran da DAT ma van ghi GITHUB_PATH: rc={p.returncode} GITHUB_PATH={gp!r}")
    # F03 (Codex lượt 2): thư mục ứng viên có Python KHÁC, thiếu PyYAML (venv thật), `rg` đầu PATH hỏng ⇒ wrapper vẫn
    # chọn được ứng viên: interpreter của checker phải là bản ban đầu, không phải bản mà PATH mới trỏ tới.
    vo_py, env_py = _wp802_bash_env()
    co_yaml = subprocess.run([vo_py, "-c", "python -c 'import yaml' 2>/dev/null || python3 -c 'import yaml'"],
                             env=env_py, capture_output=True, timeout=60).returncode == 0
    bang(co_yaml, "KHONG DO DUOC: python ban dau tren PATH khong import duoc yaml")
    with San() as s:
        p, gp, uv, _d = _wp831_chay_cai_rg(s, nen, "echo 'ripgrep 14.1.0'", venv=True)
        bang(not (uv / "python").exists() or subprocess.run([str(uv / "python"), "-c", "import yaml"],
                                                            capture_output=True, timeout=60).returncode != 0,
             f"{nen}: venv ung vien lai co yaml — fixture khong do F03")
        bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == str(uv),
             f"{nen}: Python cua thu muc ung vien thay cho Python ban dau: rc={p.returncode} GITHUB_PATH={gp!r} "
             f"{p.stdout[-200:]} {p.stderr[-300:]}")
    # F03 (Codex lượt 3): như trên nhưng qua `--bat-buoc` (rg rồi bash). Lượt `source` cho `bash` phải DÙNG LẠI Python
    # đã ghim của lượt cha, không chọn lại từ PATH mà công thức `rg` vừa đổi.
    with San() as s:
        p, gp, uv, _d = _wp831_chay_cai_rg(s, nen, "echo 'ripgrep 14.1.0'", venv=True, batch=True)
        try:
            tong = json.loads(p.stdout[p.stdout.rindex('{\n  "trang_thai_tong"'):])
        except ValueError:
            tong = {}
        dat = {c.get("ten"): c.get("trang_thai") for c in tong.get("cong_cu", [])}
        bang(p.returncode == 0 and tong.get("trang_thai_tong") == "DAT" and dat == {"rg": "DAT", "bash": "DAT"},
             f"{nen}: --bat-buoc chon lai Python sau khi rg doi PATH: rc={p.returncode} {dat} "
             f"{p.stderr[-300:]}")
    # F03 dưới `allexport` (Codex lượt 5): phép gán dấu của lượt cha tự export ⇒ lượt `source` cho rg xoá nó (rào F04) và
    # bash chọn lại Python. Cả hai cách bật, cả hai thứ tự: rc 0, cả hai DAT, installer con không thấy dấu.
    for ae in ("co", "env"):
        for tt in (("rg", "bash"), ("bash", "rg")):
            with San() as s:
                p, gp, uv, _d = _wp831_chay_cai_rg(s, nen, "echo 'ripgrep 14.1.0'", venv=True, batch=True,
                                                    allexport=ae, thu_tu=tt)
                try:
                    tong = json.loads(p.stdout[p.stdout.rindex('{\n  "trang_thai_tong"'):])
                except ValueError:
                    tong = {}
                dat = {c.get("ten"): c.get("trang_thai") for c in tong.get("cong_cu", [])}
                thay = (s / "dau.log").read_text().split() if (s / "dau.log").exists() else []
                bang(p.returncode == 0 and dat == {"rg": "DAT", "bash": "DAT"} and thay == ["ABSENT", "ABSENT"],
                     f"{nen}: allexport={ae} thu_tu={tt}: rc={p.returncode} {dat} installer thay {thay} "
                     f"{p.stderr[-300:]}")
    # F04 (Codex lượt 4): dấu và `PY` vô hướng đến từ MÔI TRƯỜNG (qua `exec` nên dấu TRÙNG PID) không được tin — lần gọi
    # mới vẫn tự chọn Python ban đầu; và installer con KHÔNG thấy dấu, kể cả khi dấu đầu vào đã được export.
    for batch in (False, True):
        with San() as s:
            p, gp, uv, _d = _wp831_chay_cai_rg(s, nen, "echo 'ripgrep 14.1.0'", venv=True, batch=batch, tiem=True)
            thay = (s / "dau.log").read_text().split() if (s / "dau.log").exists() else []
            bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == str(uv),
                 f"{nen}: dau + PY vo huong tu moi truong duoc tin (batch={batch}): rc={p.returncode} "
                 f"GITHUB_PATH={gp!r} {p.stderr[-300:]}")
            bang(thay == ["ABSENT"] * (2 if batch else 1),
                 f"{nen}: installer gia khong duoc goi dung so lan / con thay dau (batch={batch}): {thay}")
    # F01 (Codex lượt 1): tệp `rg` của ứng viên KHÔNG thực thi, một `rg` tốt khác đứng đầu PATH ⇒ thư mục ứng viên mà
    # checker đã bỏ qua KHÔNG được chọn. wp868 (Q4): `rg` nay dùng bộ chọn chung — tên trần đã DAT ⇒ `GIU_PATH`, nên đo qua
    # cai_cong_cu.sh: DAT và $GITHUB_PATH không nhận thư mục ứng viên (trước đây: dòng in cuối là thư mục bản tốt).
    with San() as s:
        p, gp, uv, _truoc = _wp831_chay_cai_rg(s, nen, "echo 'ripgrep 14.1.0'", dau="truoc")
        bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == "",
             f"{nen}: ung vien khong thuc thi van bi chon: rc={p.returncode} GITHUB_PATH={gp!r} "
             f"(ung vien {uv}) {p.stderr[-300:]}")


@ca
def r831_cai_rg_linux_chon_ban_chay_duoc():
    """N1/N3: NGUYÊN `rg.cai.linux`; `rg` hỏng đầu PATH ⇒ chọn `/usr/bin` (dưới `CONG_CU_GOC` tạm) khi bản ấy DAT, không thì ≠ 0."""
    return _wp831_cai_rg_chon_ban_chay_duoc("linux")


@ca
def r831_cai_rg_macos_chon_ban_chay_duoc():
    """N2/N3: NGUYÊN `rg.cai.macos`; ứng viên `$(brew --prefix)/bin`, cùng hai chiều như Linux."""
    return _wp831_cai_rg_chon_ban_chay_duoc("macos")


# wp1078 (spec ops/specs/wp1078.md M3): hàm `python` export qua môi trường (`BASH_FUNC_python%%`). `command -v` nhận
# hàm và in TÊN TRẦN ⇒ phép ghim PY[0] không ghim gì (review độc lập #832 F03 tái mở; ca HINT của reviewer).
def _r1078_python_ham_ke_thua(nen, than_ham='command python "$@"'):
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    global _wp802_bash_env
    env_goc = _wp802_bash_env

    def env_co_ham():
        vo, env = env_goc()
        env["R1078_HAM_LOG"] = str(ham_log)
        env["BASH_FUNC_python%%"] = (
            '() { printf "%s\\n" goi >> "$R1078_HAM_LOG"; ' + than_ham + ";\n}")
        return vo, env

    _wp802_bash_env = env_co_ham
    try:
        with San() as s:
            ham_log = s / "ham.log"
            p, gp, uv, _d = _wp831_chay_cai_rg(s, nen, "echo 'ripgrep 14.1.0'", venv=True, batch=True)
            bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == str(uv),
                 f"{nen}: ham python ke thua ({than_ham}) doi interpreter: rc={p.returncode} "
                 f"GITHUB_PATH={gp!r} {p.stderr[-300:]}")
            bang(not ham_log.exists(), f"{nen}: ham python ke thua da bi goi")
    finally:
        _wp802_bash_env = env_goc


@ca
def r831_cai_rg_linux_python_ham_ke_thua():
    return _r1078_python_ham_ke_thua("linux")


@ca
def r831_cai_rg_macos_python_ham_ke_thua():
    return _r1078_python_ham_ke_thua("macos")


@ca
def r1078_ham_python_khong_phai_python_khong_duoc_goi():
    """M3: hàm `python` export KHÔNG phải Python (in rác) ⇒ vẫn DAT bằng interpreter thật — hàm không bao giờ được gọi."""
    return _r1078_python_ham_ke_thua("linux", "echo khong-phai-python")


@ca
def r1078_hinh_dang_chon_python_bang_type_P():
    """M1/M2 (hình dạng, chạy cả Windows): chọn bằng `type -P`, không `command -v python*`; PY[0] không tuyệt đối ⇒ thoát 4."""
    sh = CAI_SH_DANG_DUNG.read_text(encoding="utf-8")
    bang(all(f'_PY_TEP="$(type -P {t})"' in sh for t in ("python", "python3", "py")),
         "chon interpreter phai bang type -P cho ca ba ten")
    bang(not re.search(r"command -v (python3?|py)\b", sh) and 'PY[0]="$(command -v' not in sh,
         "con chon/ghim interpreter bang command -v (nhan ca HAM)")
    bang(re.search(r'case "\$\{PY\[0\]\}" in /\*\) ;; \*\) echo [^\n]*>&2; exit 4 ;; esac', sh) is not None,
         "thieu chot PY[0] tuyet doi (fail-close, thoat 4)")


@ca
def r1078_py_dung_lai_khong_tuyet_doi_phai_thoat_4():
    """M2: kiểm nhánh dùng lại PY cả khi kế thừa allexport/marker export; checker giả chặn installer."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    with San() as s:
        ops = s / "kho" / "ops"
        ops.mkdir(parents=True)
        kich = ops / "cai_cong_cu.sh"
        shutil.copy2(CAI_SH_DANG_DUNG, kich)
        (ops / "cong_cu.py").write_text("raise SystemExit(23)\n", encoding="utf-8")
        vo, env = _wp802_bash_env()
        for nhan, co, them_env in (
                ("thuong", (), {}),
                ("bash-a", ("-a",), {}),
                ("SHELLOPTS", (), {"SHELLOPTS": "allexport"}),
                ("marker-export", (), {"CAI_CONG_CU_PY_CUA": "r1078-gia"})):
            for ten in ("python", "./python"):
                p = subprocess.run(
                    [vo, *co, "-c", 'CAI_CONG_CU_PY_CUA=$$; declare +x CAI_CONG_CU_PY_CUA; PY=("$2"); . "$1" rg',
                     "r1078", str(kich), ten],
                    env={**env, **them_env}, capture_output=True, text=True, timeout=30)
                bang(p.returncode == 4 and p.stdout == ""
                     and len(p.stderr.splitlines()) == 1
                     and "PY[0] khong phai duong dan tuyet doi" in p.stderr,
                     f"PY dung lai {ten!r} ({nhan}) phai thoat 4 truoc checker: "
                     f"rc={p.returncode} out={p.stdout!r} err={p.stderr!r}")


@ca
def r1122_loi_mang_thong_diep_cat_160():
    """#1122 spec A2: chi tiết `loi` mang loại + thông điệp cắt ĐÚNG 160 ký tự (số viết cứng ở đây, không đọc
    hằng), và ca vẫn là `loi`. Đỏ khi bỏ thông điệp hoặc đổi trần cắt."""
    from unittest.mock import patch
    def review_vo_can():
        raise TypeError("x" * 500)
    with patch.dict(cham_mot_ca.__globals__, {"CA": [review_vo_can]}):
        kq = cham_mot_ca(review_vo_can)
    bang(kq == ("loi", "review_vo_can(TypeError: " + "x" * 160 + ")"), f"chi tiet loi sai: {kq[0]} {kq[1][:60]}...")


ASSERT_TRAN_CHO_PHEP = frozenset({   # CỐ Ý ném AssertionError trần: ca thử chính bộ chấm/headline
    "r1079_cham_mot_ca_chi_TinHieuChotCa_la_giet", "r1079_cc_chay_suite_phai_do_hanh_vi",
    "t119_main_nhanh_mac_dinh_PHAI_in_headline_bang_dong_ket_qua"})


@ca
def r1122_khong_assert_tran_trong_ca():
    """#1122 spec A1: bộ chấm (từ #1079) chỉ tính `TinHieuChotCa` là giết, nên một `assert` trần trong ca
    biến mọi đột biến nhắm ca ấy thành tín dụng giả. Lane Windows đỏ 430/434 vì ba đột biến như vậy (run
    41322980509); phép quét #1079 chỉ chạy trên Linux nên không thấy. Ca này quét AST của CHÍNH tệp, không
    phụ thuộc nền. Hai đường vào cùng lớp: `assert` trần VÀ `raise AssertionError` tường minh (dòng SAI
    `g2_windows_directory_pin_access` ở run 41328709141 đến từ đường thứ hai). Danh sách cho phép phải BẰNG
    ĐÚNG tập ca đang chứa một trong hai; tên thừa cũng đỏ."""
    import ast
    cay = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    co_assert = {n.name for n in cay.body
                 if isinstance(n, ast.FunctionDef) and any(isinstance(d, ast.Name) and d.id == "ca"
                                                           for d in n.decorator_list)
                 and any(isinstance(x, ast.Assert) or (
                     isinstance(x, ast.Raise) and isinstance(getattr(x.exc, "func", x.exc), ast.Name)
                     and getattr(x.exc, "func", x.exc).id == "AssertionError")
                     for x in ast.walk(n))}
    bang(co_assert == set(ASSERT_TRAN_CHO_PHEP),
         f"assert tran trong ca: thua {sorted(co_assert - ASSERT_TRAN_CHO_PHEP)}, "
         f"cho phep khong con dung {sorted(ASSERT_TRAN_CHO_PHEP - co_assert)}")


@ca
def r1122_con_python_giai_ma_utf8():
    """#1122 spec mục tiêu 4 (gốc ĐÃ ĐO ở run 41328709141): `chay()` gọi `subprocess.run(text=True)` không
    `encoding` ⇒ Windows giải mã stdout của launcher (UTF-8) bằng cp1252, byte 0x90 giết `_readerthread`
    (`UnicodeDecodeError`), `r.stdout` thành `None`, `t73` ném `TypeError` trong `json.loads`. Mọi lời gọi
    `subprocess` có `text=True` mà tiến trình con là Python (`PY`/`py`) phải khai `encoding`. Con là shell/git/
    hệ thống thì không thuộc luật này (bảng mã của chúng không do kho quyết)."""
    import ast
    cay = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    def con_python(x):
        if not x.args or not isinstance(x.args[0], ast.List) or not x.args[0].elts:
            return False
        e = x.args[0].elts[0]
        if isinstance(e, ast.Call) and isinstance(e.func, ast.Name) and e.func.id == "str" and e.args:
            e = e.args[0]
        return isinstance(e, ast.Name) and e.id in ("PY", "py")
    thieu = []
    for x in ast.walk(cay):
        if isinstance(x, ast.Call) and con_python(x):
            kw = {k.arg: k.value for k in x.keywords if k.arg}
            if (isinstance(kw.get("text"), ast.Constant) and kw["text"].value is True
                    and "encoding" not in kw):
                thieu.append(x.lineno)
    bang(not thieu, f"text=True khong encoding o con Python, dong: {thieu}")


@ca
def r1079_cham_mot_ca_chi_TinHieuChotCa_la_giet():
    """#1079 F01 (a): lỗi vô can là tín dụng giả KỂ CẢ khi một `except` đã đổi kiểu sang AssertionError."""
    def chot():
        bang(False, "chot cua ca")
    def doi_kieu():
        try:
            None.x  # noqa: B018
        except AttributeError as e:
            raise AssertionError(f"boc {type(e).__name__}") from None
    def tran():
        assert False, "assert tran"  # noqa: B011
    def vo_can():
        raise AttributeError("vo can")
    def qua():
        return None
    def bo():
        return "BO QUA nen"
    kq = {f.__name__: cham_mot_ca(f)[0] for f in (chot, doi_kieu, tran, vo_can, qua, bo)}
    bang(kq == {"chot": "giet", "doi_kieu": "loi", "tran": "loi", "vo_can": "loi", "qua": "qua",
                "bo": "bo_qua"}, f"phan hang sai: {kq}")


@ca
def r1079_ket_luan_mutant_neutral_do_khong_cap_tin_dung():
    """#1079 F01 (a)(b): neutral không qua ⇒ KHÔNG ĐO ĐƯỢC tính hỏng; lỗi vô can ⇒ SAI; bỏ qua giữ luật cũ."""
    Q, G, L, B = ("qua", "x"), ("giet", "x"), ("loi", "x(AttributeError)"), ("bo_qua", "x")
    th = {k: ket_luan_mutant(*v)[0] for k, v in {
        "neutral_giet": (["x"], {"x": G}, {"x": G}), "neutral_loi": (["x"], {"x": L}, {"x": G}),
        "giet": (["x"], {"x": Q}, {"x": G}), "vo_can": (["x"], {"x": Q}, {"x": L}),
        "song": (["x"], {"x": Q}, {"x": Q}), "bo_ca": (["x"], {"x": B}, {"x": B}),
        "tron": (["x", "y"], {"x": Q, "y": B}, {"x": G, "y": B})}.items()}
    bang(th == {"neutral_giet": "KHONG_DO_NEUTRAL", "neutral_loi": "KHONG_DO_NEUTRAL", "giet": "OK",
                "vo_can": "SAI", "song": "SAI", "bo_ca": "KHONG_DO", "tron": "OK"}, f"ket luan sai: {th}")


@ca
def r1079_cham_lap_ca_doi_dung_TinHieuChotCa():
    """#1079 F01 (b): chứng cứ là KÊNH KẾT QUẢ có nonce, không phải stdout — đuôi stdout giả rồi
    thoát, nonce sai, hay loại hỏng khác `TinHieuChotCa` đều KHÔNG phải giết."""
    ghi = ("import json,os,sys\nk,n=os.environ['LT_KENH_KET_QUA'],os.environ['LT_KENH_NONCE']\n"
           "def g(**d): open(k,'w').write(json.dumps({'nonce': n, 'ten': sys.argv[2], 'qua': 0, 'bo_qua': 0, 'hong': 0, 'loai': None, **d}))\n")
    vi_du = {"giet": "g(hong=1, loai='TinHieuChotCa'); sys.exit(1)",
             "vocan": "g(hong=1, loai='AttributeError'); sys.exit(1)",
             "gia": "print('LOAI_HONG gia: TinHieuChotCa'); print(); print('LAP gia: 0/1 qua, 0 bo qua, 1 hong'); sys.exit(1)",
             "nonce": "n = 'x' * 32; g(hong=1, loai='TinHieuChotCa'); sys.exit(1)",
             "bo": "g(bo_qua=1)", "qua": "g(qua=1)"}
    with San() as s:
        (s / "launcher_test.py").write_text(ghi + "".join(
            f"if sys.argv[2] == {k!r}:\n    {v}\n" for k, v in vi_du.items()), encoding="utf-8")
        kq = {k: cham_lap_ca(s, k)[0] for k in vi_du}
    bang(kq == {"giet": "giet", "vocan": "loi", "gia": "loi", "nonce": "loi", "bo": "bo_qua", "qua": "qua"},
         f"cham_lap_ca sai: {kq}")


@ca
def r1079_chay_dot_bien_noi_neutral_va_cham_theo_loai():
    """#1079 F01 + F07 (Codex lượt 2): đo HÀNH VI, không đọc chuỗi nguồn — chạy `chay_dot_bien` thật
    với một ca đích ĐỎ SẴN trên bản gốc: neutral (a) và (b) phải biến nó thành hỏng `(1, 0)`; mutant
    giết bằng chính chốt ấy KHÔNG được thành OK. Ca đích thiếu (F06) cũng phải là hỏng."""
    from unittest.mock import patch
    def review_do_san():
        bang(False, "do san tren ban goc")
    goi = []
    def lap_ca_gia(thu_muc, ten_ca):
        goi.append(str(thu_muc))
        return ("giet", ten_ca) if "harness_db_" in str(thu_muc) else ("loi", f"{ten_ca}(neutral do)")
    neo = ("#!/usr/bin/env python3", "#!/usr/bin/env python3\n# r1079 tro")
    kq = {}
    for nhan, them in {
            "a": {"DOT_BIEN": [("r1079_a", neo, ["review_do_san"])], "DOT_BIEN_HARNESS": []},
            "a_thieu": {"DOT_BIEN": [("r1079_thieu", neo, ["review_ca_vang"])], "DOT_BIEN_HARNESS": []},
            "b": {"DOT_BIEN": [], "DOT_BIEN_HARNESS": [
                ("r1079_b", ("def b" + "ang(dieu_kien, thong_diep):", "def b" + "ang(dieu_kien, thong_diep):  # tro"),
                 ["review_do_san"])]}}.items():
        with patch.dict(chay_dot_bien.__globals__, {"CA": [review_do_san], "DOT_BIEN_HOOK": [],
                                                    "cham_lap_ca": lap_ca_gia, **them}):
            kq[nhan] = chay_dot_bien()
    bang(kq == {"a": (1, 0), "a_thieu": (1, 0), "b": (1, 0)}, f"neutral/ca dich vang khong lam cong do: {kq}")
    bang(any("harness_goc" in g for g in goi), f"neutral (b) khong chay tren ban sao NGUYEN: {goi}")


@ca
def r1079_cc_test_chi_chot_cua_suite_la_do():
    """#1079 F01 (c): `codex_cred_test` chỉ tính đỏ-do-assertion khi `TinHieuChotCa` hoặc `assert`
    trần ở CHÍNH tệp ấy; lỗi vô can mang tên `<ca>(<Loại>)` nên không khớp `phai_chet`."""
    import runpy
    ns = runpy.run_path(str(CC_TEST_DANG_DUNG), run_name="cc_test_1079")
    dong = CC_TEST_DANG_DUNG.read_text(encoding="utf-8").splitlines()
    n_assert = next(i for i, x in enumerate(dong, 1) if x.lstrip().startswith("assert "))
    def nem(ma, tep, so_dong):
        try:
            exec(compile("\n" * (so_dong - 1) + ma, tep, "exec"), {})
        except BaseException as e:  # noqa: BLE001
            return e
    tep = str(CC_TEST_DANG_DUNG)
    la = ns["la_chot_cua_suite"]
    with San() as s:   # tệp KHÁC mà dòng ấy cũng là `assert` — chỉ phép so tệp mới phân biệt được
        khac = s / "khac.py"
        khac.write_text("assert False\n" * n_assert, encoding="utf-8")
        th = {"assert_tran": la(nem("assert False", tep, n_assert)),
              "doi_kieu": la(nem("raise AssertionError('boc')", tep, 1)),
              "vo_can_dong_assert": la(nem("raise AttributeError('x')", tep, n_assert)),
              "tep_khac": la(nem("assert False", str(khac), n_assert)),
              "tin_hieu": la(ns["TinHieuChotCa"]("x"))}
    bang(th == {"assert_tran": True, "doi_kieu": False, "vo_can_dong_assert": False, "tep_khac": False,
                "tin_hieu": True}, f"la_chot_cua_suite sai: {th}")
    bang(ns["ten_do"]("t1", AttributeError("x")) == "t1(AttributeError)"
         and ns["ten_do"]("t1", ns["TinHieuChotCa"]("x")) == "t1", "ten_do khong tach loi vo can")


@ca
def r1079_harness_trung_ten_loai_khong_cap_tin_dung():
    """Regression: lớp khác trùng tên tín hiệu không phải chốt của suite."""
    ma = Path(__file__).read_text(encoding="utf-8")
    them = '''
@ca
def review_trung_ten():
    class TinHieuChotCa(RuntimeError): pass
    raise TinHieuChotCa("loi vo can")
'''
    ma = ma.replace('\nif __name__ == "__main__":', them + '\nif __name__ == "__main__":')
    with San() as s:
        dev = _dung_cay_harness(s / "tree", ma, LAUNCHER.read_text(encoding="utf-8"))
        kq = cham_lap_ca(dev, "review_trung_ten")
    bang(kq[0] == "loi", f"lop khac trung ten duoc cap tin dung: {kq}")


@ca
def r1079_harness_duoi_stdout_gia_khong_cap_tin_dung():
    """Regression: in đuôi giống runner rồi thoát không phải một assertion."""
    with San() as s:
        (s / "launcher_test.py").write_text(
            'print("LOAI_HONG review_gia: TinHieuChotCa", flush=True)\n'
            'print("\\nLAP review_gia: 0/1 qua, 0 bo qua, 1 hong", flush=True)\n'
            'raise SystemExit(1)\n', encoding="utf-8")
        kq = cham_lap_ca(s, "review_gia")
    bang(kq[0] == "loi", f"stdout gia duoc cap tin dung: {kq}")


@ca
def r1079_n13_do_bash_cung_phai_loc_env_cha():
    """Regression: môi trường sạch phải bao cả bước dò Bash của N13."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    from unittest.mock import patch
    with San() as s:
        ky = s / "ambient.log"
        init = s / "init.sh"
        init.write_text(f"printf 'AMBIENT_INIT\\n' >> {shlex.quote(str(ky))}\n", encoding="utf-8")
        home = s / "parent-home"; home.mkdir()
        with patch.dict(os.environ, {"BASH_ENV": str(init), "ENV": str(init), "HOME": str(home)}):
            r484_g7_hook_vang_codex_cai_cli_truoc_materialize()
        dong = ky.read_text(encoding="utf-8").splitlines() if ky.exists() else []
    bang(not dong, f"N13 van chay init cua cha khi do bash: {dong}")


@ca
def r1079_cc_chay_suite_phai_do_hanh_vi():
    """Regression: chạy chay_suite thật; comment chứa lời gọi không thay được hành vi."""
    import runpy
    from types import SimpleNamespace
    from unittest.mock import patch
    ns = runpy.run_path(str(CC_TEST_DANG_DUNG), run_name="review_cc_behavior")
    runner = ns["chay_suite"]
    ten = "t2_chua_thay_thi_tra_None_khong_doan"
    def vo_can(_):
        raise AttributeError("loi vo can")
    def doi_kieu(_):
        try:
            vo_can(None)
        except AttributeError:
            raise AssertionError("doi kieu") from None
    th = {}
    for nhan, fn in (("neutral", lambda _: (None, None)), ("chot", lambda _: ("sai", "sai")),
                     ("vo_can", vo_can), ("doi_kieu", doi_kieu)):
        m = SimpleNamespace(__nguon__="inert", __nhan__="inert", doc_moc_device=fn)
        with patch.dict(runner.__globals__, {"nap": lambda *_, m=m: m}):
            th[nhan] = runner(m, {ten})
    bang(th == {"neutral": set(), "chot": {ten}, "vo_can": {f"{ten}(AttributeError)"},
                "doi_kieu": {f"{ten}(AssertionError)"}}, f"chay_suite cap sai tin dung: {th}")



@ca
def r1079_review_lop_khac_cung_qualname_khong_la_chot():
    """Reviewer hint: identity must survive equal __qualname__, not only local class names."""
    ma = Path(__file__).read_text(encoding="utf-8")
    them = '\n@ca\ndef review_target():\n    raise type("TinHieuChotCa", (RuntimeError,), {})("inert")\n'
    ma = ma.replace('\nif __name__ == "__main__":', them + '\nif __name__ == "__main__":')
    with San() as s:
        dev = _dung_cay_harness(s / "tree", ma, LAUNCHER.read_text(encoding="utf-8"))
        kq = cham_lap_ca(dev, "review_target")
    bang(kq[0] == "loi", f"equal qualname received kill: {kq}")


@ca
def r1079_review_san_pham_chot_ca_khac_khong_la_giet():
    def review_other_case():
        bang(False, "assertion of OTHER case")
    def review_target():
        review_other_case()
    from unittest.mock import patch
    with patch.dict(cham_mot_ca.__globals__, {"CA": [review_target, review_other_case]}):
        kq = cham_mot_ca(review_target)
    bang(kq[0] == "loi", f"another case assertion received kill: {kq}")


@ca
def r1079_review_harness_chot_ca_khac_khong_la_giet():
    ma = Path(__file__).read_text(encoding="utf-8")
    them = '\n@ca\ndef review_other_case():\n    bang(False, "other")\n@ca\ndef review_target():\n    review_other_case()\n'
    ma = ma.replace('\nif __name__ == "__main__":', them + '\nif __name__ == "__main__":')
    with San() as s:
        dev = _dung_cay_harness(s / "tree", ma, LAUNCHER.read_text(encoding="utf-8"))
        kq = cham_lap_ca(dev, "review_target")
    bang(kq[0] == "loi", f"another case assertion received harness kill: {kq}")


@ca
def r1079_review_credential_chot_ca_khac_khong_la_giet():
    import runpy
    from types import SimpleNamespace
    from unittest.mock import patch
    ns = runpy.run_path(str(CC_TEST_DANG_DUNG), run_name="review_origin_cc")
    ten = "t2_chua_thay_thi_tra_None_khong_doan"
    def sai(*_):
        ns["t1_doc_duoc_url_va_ma_tu_dau_ra_that"](
            SimpleNamespace(doc_moc_device=lambda *_: (None, None)))
    m = SimpleNamespace(__nguon__="inert", __nhan__="inert", doc_moc_device=sai)
    runner = ns["chay_suite"]
    with patch.dict(runner.__globals__, {"nap": lambda *_: m}):
        do = runner(m, {ten})
    bang(do != {ten}, f"t1 assertion counted as t2 kill: {do}")


@ca
def r1079_review_ca_dich_vang_phai_lam_cong_do():
    from unittest.mock import patch
    runner = chay_dot_bien
    with patch.dict(runner.__globals__, {
            "CA": [], "DOT_BIEN_HOOK": [], "DOT_BIEN_HARNESS": [],
            "DOT_BIEN": [("review_missing", ("#!/usr/bin/env python3",
                          "#!/usr/bin/env python3\n# inert"), ["review_missing_case"])]}):
        hong, bo = runner()
    bang((hong, bo) == (1, 0), f"missing target treated as platform skip: {(hong, bo)}")



@ca
def r1079_review_khoa_neutral_phai_do_hanh_vi():
    import runpy
    ma = Path(__file__).read_text(encoding="utf-8")
    cu = '                    LAUNCHER_DANG_DUNG = LAUNCHER\n                    neutral[fn.__name__] = cham_mot_ca(fn)\n'
    moi = '                    neutral[fn.__name__] = ("qua", fn.__name__)\n'
    bang(ma.count(cu) == 1, "hint mutation anchor changed; rederive the behavioral counterexample")
    ma = ma.replace(cu, moi, 1)
    ma = ma.replace('    neutral = {}\n', '    """\n' + cu + '    """\n    neutral = {}\n', 1)
    with San() as s:
        dev = _dung_cay_harness(s / "tree", ma, LAUNCHER.read_text(encoding="utf-8"))
        ns = runpy.run_path(str(dev / "launcher_test.py"), run_name="review_neutral_lock")
        try:
            ns["r1079_chay_dot_bien_noi_neutral_va_cham_theo_loai"]()
        except ns["TinHieuChotCa"]:
            return
    bang(False, "neutral lock survived removed execution plus preserved source literal")



@ca
def r1079_review4_product_shared_template_call_other():
    """Shared code does not make a real call to another registered case an own assertion."""
    from unittest.mock import patch
    calls, registry = [], {}
    def factory(name):
        def target():
            calls.append(name)
            if LAUNCHER_DANG_DUNG == LAUNCHER:
                return
            if name == "review_target":
                return registry["other"]()
            bang(False, "assertion exclusively from registered other case")
        target.__name__ = name
        return target
    target, other = factory("review_target"), factory("review_other")
    registry["other"] = other
    anchor = ("#!/usr/bin/env python3", "#!/usr/bin/env python3\n# inert review mutation")
    with patch.dict(chay_dot_bien.__globals__, {
            "CA": [target, other], "DOT_BIEN_HOOK": [], "DOT_BIEN_HARNESS": [],
            "DOT_BIEN": [("review_shared_call", anchor, ["review_target"])]}):
        try:   # #1079 (Codex lượt 5): registry chung `__code__` bị TỪ CHỐI trước khi chạy ca nào
            result = chay_dot_bien()
        except ValueError as e:
            result = "tu_choi" if "__code__" in str(e) else repr(e)
    bang(result == "tu_choi" and not calls, f"credited/ran other case sharing target code: {result} {calls}")


@ca
def r1079_ca_trung_ma_bi_tu_choi_luc_dang_ky():
    """#1079 F05/F08 (Codex lượt 4): hai ca chung `__code__` (cùng factory) bị TỪ CHỐI lúc đăng ký —
    `launcher_test.ca` lẫn `codex_cred_test.chay_suite` — nên bộ chấm theo `__code__` không phải đoán."""
    import runpy
    from unittest.mock import patch
    def nha_may(ten):
        def f(_=None):
            bang(False, ten)
        f.__name__ = ten
        return f
    a, b = nha_may("review_a"), nha_may("review_b")
    th = {}
    with patch.dict(ca.__globals__, {"CA": []}):
        ca(a)
        try:
            ca(b)
            th["launcher"] = "nhan"
        except ValueError:
            th["launcher"] = "tu_choi"
        th["launcher_rieng"] = (ca(cham_mot_ca) is cham_mot_ca)   # hàm có mã riêng vẫn đăng ký được
    from types import SimpleNamespace
    ns = runpy.run_path(str(CC_TEST_DANG_DUNG), run_name="r1079_trung_ma_cc")
    tro = SimpleNamespace(__nguon__="", __nhan__="tro")
    with patch.dict(ns["chay_suite"].__globals__, {"CA": [a, b], "nap": lambda *_: tro}):
        try:
            ns["chay_suite"](tro)
            th["cc"] = "nhan"
        except ValueError:
            th["cc"] = "tu_choi"
    bang(th == {"launcher": "tu_choi", "launcher_rieng": True, "cc": "tu_choi"}, f"ca trung __code__ khong bi chan: {th}")



@ca
def r1079_review5_product_direct_CA_must_reject_shared_code():
    from unittest.mock import patch
    calls = []
    def factory(name):
        def target():
            calls.append(name)
            bang(LAUNCHER_DANG_DUNG == LAUNCHER, 'own assertion ' + name)
        target.__name__ = name
        return target
    target, alias = factory('review_target'), factory('review_alias')
    rejected = False
    with patch.dict(chay_dot_bien.__globals__, {
            'CA': [target, alias], 'DOT_BIEN_HOOK': [], 'DOT_BIEN_HARNESS': [],
            'DOT_BIEN': [('review_direct_registry', ('#!/usr/bin/env python3',
                          '#!/usr/bin/env python3\n# inert mutation'), ['review_target'])]}):
        try:
            chay_dot_bien()
        except ValueError as e:
            rejected = '__code__' in str(e)
    bang(rejected and not calls,
         f'direct CA with shared code reached cases instead of registration rejection: {calls}')


@ca
def r1079_review5_harness_direct_CA_must_reject_before_running():
    source = Path(__file__).read_text(encoding='utf-8')
    results = {}
    with San() as s:
        for mode, args in (('default', []), ('repeat', ['--lap-ca', 'review_target', '--lan', '1']),
                           ('mutants', ['--dot-bien'])):
            marker = s / (mode + '.log')
            extra = (
                '\nREVIEW_MUTATED = 0\n'
                'def review_factory(name):\n'
                '    def target():\n'
                f'        p = Path({str(marker)!r})\n'
                '        with p.open("a") as f: f.write(name + "\\n")\n'
                '        bang(not REVIEW_MUTATED, "own assertion " + name)\n'
                '    target.__name__ = name\n'
                '    return target\n'
                'CA = [review_factory("review_target"), review_factory("review_alias")]\n'
                'DOT_BIEN = [("review_direct_registry", ("#!/usr/bin/env python3", '
                '"#!/usr/bin/env python3\\n# inert"), ["review_target"])]\n'
                'DOT_BIEN_HOOK = []\nDOT_BIEN_HARNESS = []\n')
            text = source.replace('\nif __name__ == "__main__":',
                                  extra + '\nif __name__ == "__main__":')
            dev = _dung_cay_harness(s / mode, text, LAUNCHER.read_text(encoding='utf-8'))
            p = subprocess.run([PY, str(dev / 'launcher_test.py'), *args], cwd=dev,
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30,
                               env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            results[mode] = (p.returncode != 0 and '__code__' in p.stderr and not marker.exists())
    bang(all(results.values()), f'direct CA bypassed shared-code registration guard: {results}')



def _review6_registry_raw_phai_tu_choi(runner):
    from unittest.mock import patch
    for mode in ("pass", "skip", "own"):
        calls = []
        def factory(name):
            def target():
                calls.append(name)
                if mode == "own":
                    bang(False, "own assertion " + name)
                if mode == "skip":
                    return "BO QUA platform"
            target.__name__ = name
            return target
        target, alias = factory("review_target"), factory("review_alias")
        rejected = False
        with patch.dict(runner.__globals__, {"CA": [target, alias]}):
            try:
                if runner is cham_mot_ca:
                    runner(target)
                else:
                    runner([target])
            except ValueError as e:
                rejected = "__code__" in str(e)
        bang(rejected and not calls,
             f"{runner.__name__}/{mode}: raw CA must be rejected BEFORE case execution: {calls}")


@ca
def r1079_review6_cham_mot_ca_kiem_registry_truoc_chay():
    _review6_registry_raw_phai_tu_choi(cham_mot_ca)


@ca
def r1079_review6_chay_bo_ca_kiem_registry_truoc_chay():
    _review6_registry_raw_phai_tu_choi(chay_bo_ca)


@ca
def r1079_registry_nhanh_hook_tu_choi_truoc_chay():
    """#1079 F08: nhánh HOOK của `chay_dot_bien` gọi thẳng `fn()` (không qua `cham_mot_ca`) — chốt registry
    ở đầu `chay_dot_bien` là thứ DUY NHẤT chặn registry chung `__code__` trước khi thân ca chạy."""
    from unittest.mock import patch
    goi = []
    def nha_may(ten):
        def f():
            goi.append(ten)
        f.__name__ = ten
        return f
    a, b = nha_may("review_a"), nha_may("review_b")
    with patch.dict(chay_dot_bien.__globals__, {"CA": [a, b], "DOT_BIEN": [], "DOT_BIEN_HARNESS": [],
                                                "DOT_BIEN_HOOK": [("review_hook", ("#!/bin/bash\n", "#!/bin/bash\n# r1079 tro\n"), ["review_a"])]}):
        try:
            kq = chay_dot_bien()
        except ValueError as e:
            kq = "tu_choi" if "__code__" in str(e) else repr(e)
    bang(kq == "tu_choi" and not goi, f"nhanh hook chay registry chung __code__: {kq} {goi}")


# wp858 (L1): ca hành vi chạy NGUYÊN công thức qua cai_cong_cu.sh, installer là stub (POSIX); ca hình dạng thuần Python
# chạy cả Windows nên đột biến wp858 đo được mọi nền (sàn ≥70%: launcher-windows 39343232374 là 197/281).
_WP858_TOT = {"git": "echo 'git version 2.43.0'",
              "shellcheck": "echo 'ShellCheck - shell script analysis tool'; echo 'version: 0.9.0'",
              "bash": "echo 'GNU bash, version 5.2.21(1)-release (x86_64-pc-linux-gnu)'"}
_WP858_HONG = "echo 'loi: ban hong' >&2; exit 1"


def _wp858_ung_vien(s, ten, nen):
    """Thư mục ứng viên ĐẦU TIÊN công thức nguyên văn thử, và biến môi trường trỏ nó vào sân tạm."""
    if nen == "linux":
        return s / "goc" / "usr" / "bin", {"CONG_CU_GOC": str(s / "goc")}
    if nen == "macos":
        return s / "brew" / "bin", {}
    # Windows: biến trỏ ổ `V:` mà CHỈ `cygpath -u` (stub) ánh xạ được về `<sân>/v` — bỏ phép đổi là trượt ứng viên
    # (Codex wp858 lượt 1 F858-02: stub cũ trả nguyên đường nên bỏ `-u` vẫn sống).
    if ten in ("git", "bash"):
        return s / "v" / "pf" / "Git" / ("cmd" if ten == "git" else "bin"), {"ProgramFiles": "V:/pf"}
    if ten == "python":
        return s / "v" / "Python313", {"SystemDrive": "V:"}
    return s / "v" / "choco" / "bin", {"ChocolateyInstall": "V:/choco"}


def _wp858_chay_cai(s, ten, nen, tot, dau="hong", bang_ke=None, them=None, truc_tiep=False, cai_in=None,
                    env_them=None, gp_thu_muc=False):
    """NGUYÊN `<ten>.cai.<nen>` qua cai_cong_cu.sh (`--bat-buoc` khi có `bang_ke`). `tot`: thân `<ten>` ở ứng viên;
    `dau`: `"hong"`/`"tot"`/None ở ĐẦU PATH; `them`: tệp thêm ở thư mục đầu; `truc_tiep`: eval công thức (kênh kết quả
    tạm, wp868) rồi in như reader: kênh có nội dung ⇒ in kênh (dòng cuối là thư mục chọn hoặc `GIU_PATH`), rỗng ⇒ stdout; `cai_in`: stdout stub apt-get khi cài bash; `gp_thu_muc`: $GITHUB_PATH là thư mục. Trả (p, GITHUB_PATH, ứng viên, đầu)."""
    kho = s / "kho"; ops = kho / "ops"; ops.mkdir(parents=True)
    shutil.copy2(LAUNCHER.parents[2] / "ops" / "bash_nen.py", ops / "bash_nen.py")
    shutil.copy2(CONG_CU_DANG_DUNG, ops / "cong_cu.py")   # wp886: đột biến `cong_cu` phải tới được ca r858
    shutil.copy2(CAI_SH_DANG_DUNG, ops / "cai_cong_cu.sh")
    if bang_ke:
        import yaml
        d = yaml.safe_load(YAML_DANG_DUNG.read_text(encoding="utf-8"))
        (ops / "cong_cu.yaml").write_text(yaml.safe_dump(
            {"schema_version": d["schema_version"], "cong_cu": {k: d["cong_cu"][k] for k in bang_ke}},
            sort_keys=False, allow_unicode=True), encoding="utf-8")
    else:
        shutil.copy2(YAML_DANG_DUNG, ops / "cong_cu.yaml")
    uv, bien = _wp858_ung_vien(s, ten, nen)
    bin_, dau_d = s / "bin", s / "dau"
    for d in (bin_, uv, dau_d):
        d.mkdir(parents=True, exist_ok=True)
    apt = f'case " $* " in *" bash "*) printf %s {shlex.quote(cai_in)};; esac; exit 0' if cai_in else "exit 0"
    tep = {bin_ / "sudo": f'n="$1"; shift; exec \'{bin_}\'/"$n" "$@"', bin_ / "apt-get": apt,
           bin_ / "choco": "exit 0", bin_ / "brew": f"[ \"$1\" = --prefix ] && echo '{s / 'brew'}'; exit 0",
           # `-w` → `W:<đường>`; `-u` ánh xạ `V:` về `<sân>/v`; `CYGPATH_{W,U}_HONG` ⇒ thoát 37 (`-u` vẫn in đường đúng).
           bin_ / "cygpath": ('[ "$1" = -w ] && { [ -n "${CYGPATH_W_HONG:-}" ] && exit 37; echo "W:$2"; exit 0; }; '
                              'while [ "${1#-}" != "$1" ]; do shift; done; '
                              f'case "$1" in V:*) echo "{s / "v"}${{1#V:}}";; *) echo "$1";; esac; '
                              'exit ${CYGPATH_U_HONG:+37}')}
    if tot is not None:
        tep[uv / ten] = tot
    if dau:
        tep[dau_d / ten] = _WP858_HONG if dau == "hong" else _WP858_TOT[ten]
    for f, than in (them or {}).items():
        tep[dau_d / f] = than
    for f, than in tep.items():
        if than is None:
            continue
        f.write_text(f"#!/bin/sh\n{than}\n")
        f.chmod(0o755)
    gp = s / "github_path"
    if gp_thu_muc:
        gp.mkdir()
    else:
        gp.write_text("")
    vo, env = _wp802_bash_env()
    env.update(bien, CONG_CU_NEN=nen, GITHUB_PATH=str(gp),
               PATH=os.pathsep.join([str(dau_d), str(bin_), env.get("PATH", "")]))
    [env.pop(k, None) if v is None else env.__setitem__(k, v) for k, v in (env_them or {}).items()]  # None ⇒ bỏ biến
    lenh = [vo, str(ops / "cai_cong_cu.sh"), "--bat-buoc" if bang_ke else ten]
    if truc_tiep:
        import yaml
        # wp1045: bộ chọn gọi `cong_cu_dat` → `cong_cu_json_dung`, nên tách CẢ khối từ hai hàm ấy tới hết bộ chọn.
        ham = re.search(r"^cong_cu_json_dung\(\) \{.*?^chon_thu_muc_chay_duoc\(\) \{.*?^\}$",
                        (ops / "cai_cong_cu.sh").read_text(encoding="utf-8"), re.M | re.S)
        env["LENH"] = yaml.safe_load((ops / "cong_cu.yaml").read_text(encoding="utf-8"))["cong_cu"][ten]["cai"][nen]["lenh"]
        lenh = [vo, "-c", f'set -euo pipefail; PY=({shlex.quote(PY)}); GOC={shlex.quote(str(kho))}; cd "$GOC"\n'
                + f'KENH_KQ={shlex.quote(str(s / "kenh_kq"))}; : > "$KENH_KQ"\n'
                + (ham.group(0) if ham else "") + '\n( set +e; eval "$LENH" ) > "$KENH_KQ.out"\n'
                + 'if [ -s "$KENH_KQ" ]; then cat "$KENH_KQ"; else cat "$KENH_KQ.out"; fi']
    p = subprocess.run(lenh, env=env, capture_output=True, text=True, timeout=180)
    # wp1045: rig thiếu hàm thì `rc ≠ 0` vì "command not found" — ca đòi rc ≠ 0 sẽ ĐẠT oan. Thiếu lệnh ⇒ ĐỎ ngay.
    bang(not truc_tiep or "command not found" not in p.stderr, f"rig truc_tiep thieu lenh: {p.stderr[-300:]}")
    return p, ("" if gp_thu_muc else gp.read_text().strip()), uv, dau_d


def _wp858_cai_chon_ban_chay_duoc(nen):
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()                       # PyYAML vắng ⇒ ĐỎ, không bỏ qua
    for ten in ("git", "shellcheck", "bash"):
        # N1/N2: bản hỏng ĐẦU PATH, bản tốt ở ứng viên ⇒ DAT, thư mục chọn (GITHUB_PATH) là thư mục bản TỐT.
        with San() as s:
            p, gp, uv, _d = _wp858_chay_cai(s, ten, nen, _WP858_TOT[ten])
            bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == ("W:" if nen == "windows" else "") + str(uv),
                 f"{nen}/{ten}: ban hong dau PATH ma khong chon ban tot: rc={p.returncode} GITHUB_PATH={gp!r} "
                 f"mong {uv} {p.stdout[-200:]} {p.stderr[-300:]}")
        # N1/N3: không ứng viên nào DAT (ứng viên hỏng, hoặc rc 0 mà checker không nhận) ⇒ thoát ≠ 0, không chọn.
        for xau in (_WP858_HONG, "exit 0"):
            with San() as s:
                p, gp, _uv, _d = _wp858_chay_cai(s, ten, nen, xau)
                bang(p.returncode != 0 and gp == "",
                     f"{nen}/{ten}: khong ung vien nao chay duoc ma van chon ({xau!r}): rc={p.returncode} "
                     f"GITHUB_PATH={gp!r}")
            # Chính CÔNG THỨC phải thoát ≠ 0 — bước kiểm cuối của cai_cong_cu.sh che mất mã của hàm chọn.
            with San() as s:
                p, _gp, _uv, _d = _wp858_chay_cai(s, ten, nen, xau, truc_tiep=True)
                bang(p.returncode != 0, f"{nen}/{ten}: cong thuc rc=0 khi khong ung vien nao chay duoc ({xau!r})")
        for gp_v in ("", None):   # F858-06/07: $GITHUB_PATH rỗng / VẮNG (dưới `set -u`) ⇒ vẫn DAT, Windows vẫn qua `-u`
            with San() as s:
                p, gp, _uv, _d = _wp858_chay_cai(s, ten, nen, _WP858_TOT[ten], env_them={"GITHUB_PATH": gp_v})
                bang(p.returncode == 0 and '"DAT"' in p.stdout, f"{nen}/{ten}: GITHUB_PATH={gp_v!r} khong DAT rc={p.returncode}")
        # F858-01/04: ghi $GITHUB_PATH hoặc `cygpath` hỏng ⇒ installer THẬT ≠ 0 (`errexit` tắt trong `$(eval ...)`).
        hong_ghi = [dict(gp_thu_muc=True)] + ([dict(env_them={"CYGPATH_W_HONG": "1"}),
                                               dict(env_them={"CYGPATH_U_HONG": "1"})] if nen == "windows" else [])
        for kw in hong_ghi:
            with San() as s:
                p, _gp, _uv, _d = _wp858_chay_cai(s, ten, nen, _WP858_TOT[ten], **kw)
                bang(p.returncode != 0, f"{nen}/{ten}: ghi GITHUB_PATH hong ({kw}) ma installer rc=0 {p.stderr[-200:]}")
        # Tên trần đã DAT ⇒ không đổi PATH, không ghi GITHUB_PATH (ghi thì đẩy thư mục ấy lên trước bước sau).
        with San() as s:
            p, gp, _uv, _d = _wp858_chay_cai(s, ten, nen, _WP858_TOT[ten], dau="tot")
            bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == "",
                 f"{nen}/{ten}: ten tran da DAT ma van ghi GITHUB_PATH: rc={p.returncode} GITHUB_PATH={gp!r}")


@ca
def r858_cai_linux_chon_ban_chay_duoc():
    """N1/N3: NGUYÊN `git`/`shellcheck`/`bash`.cai.linux; bản hỏng đầu PATH ⇒ chọn `/usr/bin` (dưới `CONG_CU_GOC`)."""
    return _wp858_cai_chon_ban_chay_duoc("linux")


@ca
def r858_cai_macos_chon_ban_chay_duoc():
    """N1/N3: như Linux, ứng viên `$(brew --prefix)/bin`."""
    return _wp858_cai_chon_ban_chay_duoc("macos")


@ca
def r858_cai_windows_chon_ban_chay_duoc():
    """N2: `.cai.windows` qua `cygpath` stub (như r802): Git/cmd · Git/bin · choco/bin; GITHUB_PATH qua `cygpath -w`."""
    return _wp858_cai_chon_ban_chay_duoc("windows")


@ca
def r858_cai_python_khong_in_thu_muc_ban_hong():
    """N1/N3 ĐẦY ĐỦ của #858 cho python (wp886 N5 đóng nợ `python-probe-khong-theo-PATH`): bản thu hẹp theo (a)
    (#858 issuecomment-6312034981) chỉ đòi rc 0 và KHÔNG in thư mục bản hỏng, vì checker đo `sys.executable` nên
    tên trần luôn DAT. Nay checker đo bản shell gọi ⇒ python hỏng đầu PATH bị thấy: chọn ĐÚNG ứng viên tốt
    (N1), không ứng viên nào tốt ⇒ rc ≠ 0 và không chọn gì (N3)."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    # Bản đầu PATH hỏng ở `--version` nhưng chạy được script — nếu `exit 1` trần thì chính PY của cai_cong_cu.sh là nó.
    hong = f"[ \"$1\" = --version ] && exit 1; exec {shlex.quote(PY)} \"$@\""
    for nen in ("linux", "macos", "windows"):
        with San() as s:
            p, gp, uv, dau_d = _wp858_chay_cai(s, "python", nen, "echo 'Python 3.12.3'", dau=None,
                                               them={"python": hong})
            bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == ("W:" if nen == "windows" else "") + str(uv),
                 f"{nen}/python: ban hong dau PATH ma khong chon ban tot: rc={p.returncode} GITHUB_PATH={gp!r} "
                 f"mong {uv} (thu muc ban hong {dau_d}) {p.stdout[-200:]} {p.stderr[-300:]}")
        for xau in (_WP858_HONG, "exit 0"):
            with San() as s:
                p, gp, _uv, _d = _wp858_chay_cai(s, "python", nen, xau, dau=None, them={"python": hong})
                bang(p.returncode != 0 and gp == "",
                     f"{nen}/python: khong ung vien nao chay duoc ma van chon ({xau!r}): rc={p.returncode} "
                     f"GITHUB_PATH={gp!r}")
        # Dòng công thức IN cuối (thứ lên đầu PATH) là ỨNG VIÊN TỐT; `python3` cũng hỏng vì Linux cũ in `dirname` của nó.
        with San() as s:
            p, _gp, uv, dau_d = _wp858_chay_cai(s, "python", nen, "echo 'Python 3.12.3'", dau=None,
                                                them={"python": hong, "python3": hong}, truc_tiep=True)
            cuoi = (p.stdout.strip().splitlines() or [""])[-1]
            bang(p.returncode == 0 and cuoi == str(uv),
                 f"{nen}/python: cong thuc khong in ung vien tot {uv}: rc={p.returncode} in={cuoi!r} "
                 f"(thu muc ban hong {dau_d}) {p.stderr[-300:]}")


# ---------------------------------------------------------------------------------------------
# wp886 (#886, PYTHON-PROBE-THEO-PATH, spec ops/specs/wp886.md N1–N6): `ops/cong_cu.py` đo `python` bản SHELL gọi.
# Ca hành vi chạy BẢN SAO `CONG_CU_DANG_DUNG` (đích đột biến "cong_cu"); Windows dựng `<tên>.cmd` thay script shebang.
def _r886_python_gia(d, ten, ban=None):
    """`<ten>` trong `d`: in `Python <ban>` khi `--version`; `ban=None` ⇒ hỏng (`exit 1`). Windows: `<ten>.cmd`."""
    d.mkdir(parents=True, exist_ok=True)
    if LA_WINDOWS:
        f = d / f"{ten}.cmd"
        f.write_text("@echo Python " + ban + "\r\n" if ban else "@exit /b 1\r\n", encoding="ascii")
    else:
        f = d / ten
        f.write_text(f"#!/bin/sh\necho 'Python {ban}'\n" if ban else "#!/bin/sh\nexit 1\n", encoding="ascii")
        f.chmod(0o755)
    return f


def _r886_kiem(s, chi, path, env_them=None):
    """`kiem-tra --chi <chi> --json` của bản sao `cong_cu.py` với PATH đúng `path`; trả (rc, mục công cụ)."""
    ops = s / "kho" / "ops"
    ops.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CONG_CU_DANG_DUNG, ops / "cong_cu.py")
    shutil.copy2(LAUNCHER.parents[2] / "ops" / "bash_nen.py", ops / "bash_nen.py")
    env = dict(os.environ, PATH=os.pathsep.join(str(x) for x in path), **(env_them or {}))
    p = subprocess.run([PY, str(ops / "cong_cu.py"), "kiem-tra", "--chi", chi, "--json", "--ban-ke", str(YAML_DANG_DUNG)],
                       env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    try:
        return p.returncode, json.loads(p.stdout)["cong_cu"][0]
    except (ValueError, KeyError, IndexError):
        bang(False, f"kiem-tra --chi {chi} khong in JSON: rc={p.returncode} {p.stdout[-300:]} {p.stderr[-300:]}")


def _r886_nap():
    """Nạp BẢN SAO `CONG_CU_DANG_DUNG` (tên module riêng) cho ca tĩnh thuần Python."""
    spec = importlib.util.spec_from_file_location(f"cong_cu_r886_{id(CONG_CU_DANG_DUNG)}", CONG_CU_DANG_DUNG)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@ca
def r886_n1_ten_tran_theo_path_moi_nen():
    """N1: probe `python` chạy bản `python` ĐẦU PATH (không phải `sys.executable`) — đo được trên mọi nền."""
    with San() as s:
        _r886_python_gia(s / "a", "python", "0.0.1")
        rc, cc = _r886_kiem(s, "python", [s / "a"])
        bang(rc == 0 and cc["trang_thai"] == "DAT" and cc["ban_thay"] == {"mac_dinh": "0.0.1"},
             f"probe python khong do ban dau PATH: rc={rc} {cc}")


@ca
def r886_n2_python_hong_dau_path_khong_DAT():
    """N2: `python` hỏng đầu PATH, `python3` tốt phía sau ⇒ không DAT (ĐỎ trên nền `e63961f`: `sys.executable` ⇒ DAT)."""
    with San() as s:
        _r886_python_gia(s / "a", "python")
        _r886_python_gia(s / "b", "python3", "3.99.0")
        rc, cc = _r886_kiem(s, "python", [s / "a", s / "b"])
        bang(rc != 0 and cc["trang_thai"] != "DAT" and cc["ban_thay"] == {"mac_dinh": None},
             f"python hong dau PATH ma van DAT: rc={rc} {cc}")


@ca
def r886_n3_chi_python3_DAT_va_do_dung_interpreter():
    """N3: chỉ có `python3` ⇒ `python` DAT; probe PyYAML đo ĐÚNG python3 ấy (gói giả 9.9.9 thấy, vắng thì không DAT)."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    with San() as s:
        b = s / "b"; b.mkdir()
        # `-S`: không site-packages ⇒ PyYAML THẬT vắng; chỉ thấy gói giả qua PYTHONPATH. Khác hẳn `sys.executable`.
        (b / "python3").write_text(f"#!/bin/sh\nexec {shlex.quote(PY)} -S \"$@\"\n", encoding="ascii")
        (b / "python3").chmod(0o755)
        goi = s / "site" / "PyYAML-9.9.9.dist-info"; goi.mkdir(parents=True)
        (goi / "METADATA").write_text("Metadata-Version: 2.1\nName: PyYAML\nVersion: 9.9.9\n", encoding="ascii")
        rc, cc = _r886_kiem(s, "python", [b])
        bang(rc == 0 and cc["trang_thai"] == "DAT", f"may chi co python3 bi chan: rc={rc} {cc}")
        rc, cc = _r886_kiem(s, "PyYAML", [b], {"PYTHONPATH": str(s / "site")})
        bang(rc == 0 and cc["ban_thay"] == {"mac_dinh": "9.9.9"}, f"PyYAML khong do python3 tren PATH: rc={rc} {cc}")
        rc, cc = _r886_kiem(s, "PyYAML", [b], {"PYTHONPATH": ""})
        bang(rc != 0 and cc["trang_thai"] != "DAT", f"PyYAML vang o python3 tren PATH ma van DAT: rc={rc} {cc}")


@ca
def r886_n4_khong_ten_nao_noi_ro_thieu_gi():
    """N4: không `python`/`python3`/`py` trên PATH ⇒ không DAT, không ném, chi tiết nêu đủ ba tên."""
    with San() as s:
        (s / "rong").mkdir()
        rc, cc = _r886_kiem(s, "python", [s / "rong"])
        ct = cc.get("chi_tiet", "")
        bang(rc == 3 and cc["trang_thai"] == "KHONG_DO_DUOC" and all(f"{t}," in ct or f"{t} " in ct
                                                                       for t in ("python", "python3", "py")),
             f"khong ten nao ma khong noi ro thieu gi: rc={rc} {cc}")


@ca
def r886_n6_giai_ten_tinh_windows_va_posix():
    """N6 + N1 (thuần Python, mọi nền): luật native — Windows chỉ nhận đuôi PATHEXT (`python.CMD` hơn shim `python`);
    TÊN đi trước PATH (`python` ở thư mục sau thắng `python3` ở thư mục trước); `py` mang `-3`; không tên nào ⇒ None."""
    m = _r886_nap()
    with San() as s:
        a, b, c = s / "a", s / "b", s / "c"
        for d, ten in ((a, "python3.EXE"), (b, "python"), (b, "python.CMD"), (c, "py.EXE"), (c, "python3")):
            d.mkdir(exist_ok=True)
            (d / ten).write_text("x")
            (d / ten).chmod(0o755)
        pe, sep = ".COM;.EXE;.BAT;.CMD", os.pathsep
        kq = {
            "win_ab": m._python_theo_path(f"{a}{sep}{b}", pe, True),
            "win_c": m._python_theo_path(str(c), pe, True),
            "win_rong": m._python_theo_path(str(s / "khong"), pe, True),
            "posix_ab": m._python_theo_path(f"{a}{sep}{b}", pe, False),
            "posix_c": m._python_theo_path(str(c), pe, False),
        }
        mong = {"win_ab": [str(b / "python.CMD")], "win_c": [str(c / "py.EXE"), "-3"], "win_rong": None,
                "posix_ab": [str(b / "python")], "posix_c": [str(c / "python3")]}
        if LA_WINDOWS:   # hệ tệp không phân biệt hoa thường: so theo normcase
            kq = {k: v and [os.path.normcase(v[0]), *v[1:]] for k, v in kq.items()}
            mong = {k: v and [os.path.normcase(v[0]), *v[1:]] for k, v in mong.items()}
        bang(kq == mong, f"giai ten python lech luat native: {kq} mong {mong}")
        # Mục PATH RỖNG = cwd, như `command -v` của bash và `_ten_tran_giai_ra` (Codex wp886 lượt 1, H01): cwd `b` có
        # `python`/`python.CMD` thắng `c` phía sau. So bằng `samefile` — Windows có thể trả tên 8.3 cho thư mục tạm.
        with contextlib.chdir(b):
            rong = {nen: m._python_theo_path(f"{sep}{c}", pe, nen == "win") for nen in ("win", "posix")}
        dung = {"win": b / "python.CMD", "posix": b / "python"}
        bang(all(v and os.path.samefile(v[0], dung[k]) for k, v in rong.items()),
             f"muc PATH rong khong la cwd: {rong} mong {dung}")
        # Cùng TÊN ở hai thư mục ⇒ thư mục ĐẦU PATH thắng; POSIX còn đòi quyền thực thi (Codex wp886 lượt 2, H06/H07).
        d, e = s / "d", s / "e"
        for x in (d, e):
            x.mkdir()
            (x / "python").write_text("x")
            (x / "python").chmod(0o755)
        dau = m._python_theo_path(f"{d}{sep}{e}", pe, False)
        bang(dau and os.path.samefile(dau[0], d / "python"), f"cung ten o hai thu muc ma khong lay thu muc dau PATH: {dau}")


@ca
def r886_n1_bo_qua_tep_khong_thuc_thi():
    """N1 (POSIX): `python` KHÔNG thực thi được đứng đầu PATH thì bỏ qua, như `command -v` (Codex wp886 lượt 2, H06).
    Windows: `os.access(X_OK)` luôn đúng với tệp có mặt ⇒ đột biến bỏ X_OK tương đương, nên BỎ QUA thay vì đo giả."""
    if LA_WINDOWS:
        return "BO QUA X_OK khong co nghia tren Windows"
    m = _r886_nap()
    with San() as s:
        d, e = s / "d", s / "e"
        for x, quyen in ((d, 0o644), (e, 0o755)):
            x.mkdir()
            (x / "python").write_text("x")
            (x / "python").chmod(quyen)
        xok = m._python_theo_path(f"{d}{os.pathsep}{e}", None, False)
        bang(xok and os.path.samefile(xok[0], e / "python"), f"nhan tep khong thuc thi duoc: {xok}")


@ca
def r886_ten_python_khop_cai_cong_cu_sh():
    """Q1: `TEN_PYTHON` của cong_cu.py khớp ĐÚNG thứ tự + tập tên dòng chọn `PY` trong `ops/cai_cong_cu.sh`."""
    # wp1078: dòng chọn là `elif _PY_TEP="$(type -P <tên>)"; then PY=("$_PY_TEP"[ đối số])`.
    sh = re.findall(r'^elif _PY_TEP="\$\(type -P (\S+)\)"; then PY=\("\$_PY_TEP"([^)]*)\)$',
                    CAI_SH_DANG_DUNG.read_text(encoding="utf-8"), re.M)
    bang(sh and [(ten, *them.split()) for ten, them in sh] == [tuple(x) for x in _r886_nap().TEN_PYTHON],
         f"TEN_PYTHON lech cai_cong_cu.sh: sh={sh} py={_r886_nap().TEN_PYTHON}")


@ca
def r858_bat_buoc_bash_khong_dua_rg_hong_len_dau():
    """N4 (Codex #831 lượt 4): `--bat-buoc`, `rg` hỏng CÙNG thư mục với `bash` ban đầu ⇒ tổng cuối `rg` không được DO."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    vo, _env = _wp802_bash_env()
    # F858-03: trình cài in thư mục đầu (l.1); thư mục trùng tên canh cũ + `rg` hỏng ở cwd (l.2); tiền tố KHÔNG LF (l.3).
    for thu_tu in (("rg", "bash"), ("bash", "rg")):
      for in_dau in (False, True, "trung", "khong_lf"):
        with San() as s:
            if in_dau == "khong_lf":
                (s / "p" / "dev" / "null").mkdir(parents=True)
                (s / "p" / "dev" / "null" / "rg").write_text(f"#!/bin/sh\n{_WP858_HONG}\n")
                (s / "p" / "dev" / "null" / "rg").chmod(0o755)
            if in_dau == "trung":
                (s / "kho" / ":giu-nguyen-PATH:").mkdir(parents=True)
                (s / "kho" / "rg").write_text(f"#!/bin/sh\n{_WP858_HONG}\n")
                (s / "kho" / "rg").chmod(0o755)
            (s / "dau").mkdir()
            (s / "dau" / "bash").symlink_to(vo)
            p, _gp, _uv, _d = _wp858_chay_cai(s, "rg", "linux", "echo 'ripgrep 14.1.0'", dau=None, bang_ke=thu_tu,
                                              them={"rg": _WP858_HONG},
                                              cai_in={True: f"{s / 'dau'}\n", "khong_lf": str(s / "p")}.get(in_dau))
            try:
                tong = json.loads(p.stdout[p.stdout.rindex('{\n  "trang_thai_tong"'):])
            except ValueError:
                tong = {}
            dat = {c.get("ten"): c.get("trang_thai") for c in tong.get("cong_cu", [])}
            bang(p.returncode == 0 and dat == {"rg": "DAT", "bash": "DAT"},
                 f"thu_tu={thu_tu} in_dau={in_dau}: bash dua rg hong len dau: rc={p.returncode} {dat} "
                 f"{p.stderr[-300:]}")


@ca
def r858_hinh_dang_cong_thuc_cai():
    """Thuần Python, MỌI nền: 15 công thức (wp868 N4: thêm `rg`) gọi `chon_thu_muc_chay_duoc` đúng tên/`--win`/ứng viên
    Q2, lệnh cài giữ nguyên (Q3); hàm trong cai_cong_cu.sh có đủ các chốt."""
    import yaml
    d = yaml.safe_load(YAML_DANG_DUNG.read_text(encoding="utf-8"))["cong_cu"]
    cai_dat = {"git": ("sudo apt-get install -y git", "brew install git", "choco install git --yes --no-progress"),
               "python": ("sudo apt-get install -y python3 python3-pip", "brew install python",
                          "choco install python --yes --no-progress"),
               "shellcheck": ("sudo apt-get install -y shellcheck", "brew install shellcheck",
                              "choco install shellcheck --yes --no-progress"),
               "bash": ("sudo apt-get install -y bash", "brew install bash", "choco install git --yes --no-progress"),
               "rg": ("sudo apt-get install -y ripgrep", "brew install ripgrep",
                      "winget install --id BurntSushi.ripgrep.MSVC -e --accept-source-agreements "
                      "--accept-package-agreements --disable-interactivity || choco install ripgrep --yes --no-progress")}
    git_win = ('"${ProgramFiles:-C:/Program Files}/Git/cmd" "${ProgramFiles:-C:/Program Files}/Git/bin" '
               '"${ProgramFiles:-C:/Program Files}/Git/usr/bin"')
    choco = '"${ChocolateyInstall:-C:/ProgramData/chocolatey}/bin"'
    ung = {"linux": lambda t: '"${CONG_CU_GOC:-}/usr/bin"', "macos": lambda t: '"$(brew --prefix)/bin"',
           "windows": lambda t: {"git": git_win, "bash": git_win, "shellcheck": choco,
                                 "rg": '"$LOCALAPPDATA/Microsoft/WinGet/Links" ' + choco,
                                 "python": choco + ' "$(cygpath -u "${SystemDrive:-C:}/")"Python3*'}[t]}
    for ten, cai in cai_dat.items():
        for nen, lenh_cai in zip(("linux", "macos", "windows"), cai):
            lenh = d[ten]["cai"][nen]["lenh"]
            co = "--win " if nen == "windows" else ""
            mong = (f'{lenh_cai} && chon_thu_muc_chay_duoc {co}{ten} {ung[nen](ten)} '
                    f'"$(dirname "$(command -v {ten} || echo ./{ten})")"')
            bang(lenh == mong, f"{ten}.cai.{nen} lech hinh dang:\n  co   {lenh!r}\n  mong {mong!r}")
    sh = CAI_SH_DANG_DUNG.read_text(encoding="utf-8")
    bang(re.search(r"^chon_thu_muc_chay_duoc\(\) \{", sh, re.M), "cai_cong_cu.sh thieu ham chon_thu_muc_chay_duoc")
    than = sh[sh.index("chon_thu_muc_chay_duoc() {"):]
    than = than[:than.index("\n}\n")]
    for can in ('if cong_cu_dat "$ten"; then',   # wp1045: DAT theo trang thai, khong theo rc
                'PATH="$d:$PATH" cong_cu_dat "$ten"',
                'd="$(cygpath -u "$d")" || {', 'w="$(cygpath -w "$dich")" || {', "printf 'GIU_PATH' > \"$KENH_KQ\" || {",
                '  if [ -n "${GITHUB_PATH:-}" ]; then', "printf 'DICH\\n%s' \"$dich\" > \"$KENH_KQ\" || {",
                'for d in "$@"; do', 'cong_cu_dat "$ten"; then dich="$d"; break; fi',
                '    if [ -n "$win" ]; then\n      d="$(cygpath -u "$d")"',
                'd="$(cygpath -u "$d")" || { echo "cai_cong_cu: cygpath -u hong cho ung vien cua \'$ten\'" >&2; return 1; }',
                'printf \'%s\\n\' "$w" >> "$GITHUB_PATH" || {', '\'$ten\' chay duoc" >&2; return 1; }'):
        bang(can in than, f"ham chon_thu_muc_chay_duoc thieu {can!r}")


@ca
def r858_selftest_editskill_thu_muc_rieng():
    """N6 (L3): edit-skill của tl_selftest dùng thư mục tạm RIÊNG (`mkdtemp`) rồi dọn, không tên cố định trong temp chung."""
    than = SELFTEST_DANG_DUNG.read_text(encoding="utf-8")
    dau = than.find("KH1 III.2 — edit-skill")
    cuoi = than.find('cases.append(("edit_skill_assert_count_gate_dry"', dau)
    bang(0 <= dau < cuoi, "khong tach duoc khoi edit-skill trong tl_selftest.py")
    khoi = than[dau:cuoi]
    bang("gettempdir()" not in khoi, "khoi edit-skill van dung ten tep co dinh trong gettempdir()")
    bang(re.search(r"^    _esd = Path\(_tfx\.mkdtemp\(", khoi, re.M) and "_esf = _esd / " in khoi,
         "tep tam edit-skill khong nam trong thu muc rieng mkdtemp")
    bang("_shx.rmtree(_esd, ignore_errors=True)" in khoi, "khoi edit-skill khong don thu muc rieng")


# wp868 (CAI-TACH-KENH-KET-QUA): kết quả bộ chọn đi qua KÊNH RIÊNG, không qua stdout chung với trình cài. Ca hành vi
# chạy NGUYÊN `rg.cai.linux` (hoặc công thức sân tạm) qua cai_cong_cu.sh, installer là stub; ca hình dạng thuần Python.
def _wp868_chay(s, apt="exit 0", lenh=None, ung_vien=None, env_them=None, allexport=None):
    """`rg` qua cai_cong_cu.sh trong sân tạm: `rg` HỎNG đầu PATH và ở `xau/`, `rg` tốt ở `/usr/bin` dưới `CONG_CU_GOC`.
    `apt`: thân stub `apt-get`; `lenh`: thay `rg.cai.linux` (mặc định NGUYÊN VĂN YAML đang đo); `ung_vien`: {thư mục: thân
    `rg`} thêm (khoá `dau/<tệp>` đặt tệp bất kỳ lên ĐẦU PATH); `env_them`: biến thêm. Trả (process, GITHUB_PATH, ứng
    viên `/usr/bin`, `xau`, giây chạy). `allexport`: `"co"` chạy `bash -a`, `"env"` đặt `SHELLOPTS=allexport`."""
    import yaml
    kho = s / "kho"; ops = kho / "ops"; ops.mkdir(parents=True)
    for t in ("cong_cu.py", "bash_nen.py"):
        shutil.copy2(LAUNCHER.parents[2] / "ops" / t, ops / t)
    shutil.copy2(CAI_SH_DANG_DUNG, ops / "cai_cong_cu.sh")
    d = yaml.safe_load(YAML_DANG_DUNG.read_text(encoding="utf-8"))
    rg = d["cong_cu"]["rg"]
    if lenh is not None:
        rg["cai"]["linux"]["lenh"] = lenh
    (ops / "cong_cu.yaml").write_text(yaml.safe_dump({"schema_version": d["schema_version"], "cong_cu": {"rg": rg}},
                                                     sort_keys=False, allow_unicode=True), encoding="utf-8")
    uv, bin_, dau, xau = s / "goc" / "usr" / "bin", s / "bin", s / "dau", s / "xau"
    tep = {uv / "rg": "echo 'ripgrep 14.1.0'", dau / "rg": _WP858_HONG, xau / "rg": _WP858_HONG,
           bin_ / "sudo": f'n="$1"; shift; exec \'{bin_}\'/"$n" "$@"', bin_ / "apt-get": apt}
    tep.update({(Path(k) if str(k).startswith(str(dau)) else Path(k) / "rg"): v for k, v in (ung_vien or {}).items()})
    for f, than in tep.items():
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f"#!/bin/sh\n{than}\n")
        f.chmod(0o755)
    gp = s / "github_path"; gp.write_text("")
    vo, env = _wp802_bash_env()
    env.update(CONG_CU_NEN="linux", CONG_CU_GOC=str(s / "goc"), GITHUB_PATH=str(gp),
               PATH=os.pathsep.join([str(dau), str(bin_), env.get("PATH", "")]), **(env_them or {}))
    if allexport == "env":
        env["SHELLOPTS"] = "allexport"
    t0 = time.monotonic()
    p = subprocess.run([vo] + (["-a"] if allexport == "co" else []) + [str(ops / "cai_cong_cu.sh"), "rg"], env=env,
                       capture_output=True, text=True, timeout=120)
    return p, gp.read_text().strip(), uv, xau, time.monotonic() - t0


@ca
def r868_kenh_rieng_khong_doc_stdout_trinh_cai():
    """N1: NGUYÊN `rg.cai.linux` qua cai_cong_cu.sh; trình cài (a) có tiến trình con ghi thư mục `xau` vào stdout SAU khi bộ
    chọn đã ghi $GITHUB_PATH · (b) in `xau` KHÔNG kết thúc LF · (c) in `xau` ở dòng cuối ⇒ DAT, $GITHUB_PATH = ứng viên tốt.
    (a)(b) ĐỎ trên nền 9e9a74b (`rg` dùng bộ chọn riêng, `tail -1` của stdout chung). (d) công thức in `xau` SAU bộ chọn
    (tất định, Q2: kênh đã ghi thì stdout không còn là kết quả). Kèm: trình cài KHÔNG thấy kênh."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    for kieu in ("muon", "khong_lf", "dong_cuoi", "sau_bo_chon"):
        with San() as s:
            gp_f, mk, thay = s / "github_path", s / "muon.xong", s / "thay.log"
            ghi_thay = f'echo "${{KENH_KQ:-ABSENT}} ${{TAM_CAI:-ABSENT}}" >> {shlex.quote(str(thay))}'
            xau = shlex.quote(str(s / "xau"))
            apt = {"muon": (f"( i=0; while [ ! -s {shlex.quote(str(gp_f))} ] && [ $i -lt 400 ]; do sleep 0.05; i=$((i+1)); "
                            f"done; sleep 0.3; echo {xau}; echo xong > {shlex.quote(str(mk))} ) 2>/dev/null &"),
                   "khong_lf": f"printf %s {xau}", "dong_cuoi": f"echo {xau}", "sau_bo_chon": ":"}[kieu]
            lenh = ('sudo apt-get install -y ripgrep && chon_thu_muc_chay_duoc rg "${CONG_CU_GOC:-}/usr/bin" && echo '
                    + xau) if kieu == "sau_bo_chon" else None
            p, gp, uv, _xau, _t = _wp868_chay(s, apt=f"{ghi_thay}\n{apt}\nexit 0", lenh=lenh)
            if kieu == "muon":   # ca có ĐO: writer muộn PHẢI đã ghi (không thì không đo gì)
                for _ in range(200):
                    if mk.exists():
                        break
                    time.sleep(0.05)
                bang(mk.exists(), f"KHONG DO DUOC: writer muon khong chay rc={p.returncode} {p.stderr[-300:]}")
            bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == str(uv),
                 f"{kieu}: stdout trinh cai bi doc lam thu muc: rc={p.returncode} GITHUB_PATH={gp!r} mong {uv} "
                 f"{p.stdout[-200:]} {p.stderr[-300:]}")
            bang(thay.read_text().split() == ["ABSENT", "ABSENT"], f"{kieu}: trinh cai thay kenh: {thay.read_text()!r}")
    # F868-06 (Codex lượt 3): dưới allexport MỌI phép gán tự export — kênh vẫn phải vô hình với trình cài, cả hai cách bật.
    for ae in ("co", "env"):
        with San() as s:
            thay = s / "thay.log"
            ghi_thay = f'echo "${{KENH_KQ:-ABSENT}} ${{TAM_CAI:-ABSENT}}" >> {shlex.quote(str(thay))}'
            p, gp, uv, _xau, _t = _wp868_chay(s, apt=f"{ghi_thay}\nexit 0", allexport=ae)
            bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == str(uv),
                 f"allexport={ae}: rc={p.returncode} GITHUB_PATH={gp!r} {p.stderr[-300:]}")
            bang(thay.read_text().split() == ["ABSENT", "ABSENT"], f"allexport={ae}: trinh cai thay kenh: {thay.read_text()!r}")


@ca
def r868_writer_muon_khong_lam_treo():
    """N2: tiến trình con của trình cài giữ stdout mở 20 giây ⇒ cai_cong_cu.sh vẫn xong dưới 12 giây, DAT, đúng thư mục."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    with San() as s:
        pf = s / "giu.pid"
        apt = (f"( sh -c 'echo $$ > {shlex.quote(str(pf))}; exec sleep 20'; echo {shlex.quote(str(s / 'xau'))} ) "
               "2>/dev/null & exit 0")
        try:
            p, gp, uv, _xau, giay = _wp868_chay(s, apt=apt)
        finally:
            with contextlib.suppress(Exception):
                os.kill(int(pf.read_text().strip()), signal.SIGKILL)
        bang(pf.exists(), "KHONG DO DUOC: tien trinh giu stdout khong chay")
        bang(giay < 12 and p.returncode == 0 and '"DAT"' in p.stdout and gp == str(uv),
             f"cai_cong_cu cho EOF stdout trinh cai: {giay:.1f}s rc={p.returncode} GITHUB_PATH={gp!r} {p.stderr[-300:]}")


@ca
def r868_khong_bo_chon_doc_dong_cuoi():
    """N3: công thức KHÔNG gọi bộ chọn (như pip/cai_actionlint.sh) ⇒ kênh rỗng ⇒ dòng cuối stdout vẫn lên đầu PATH."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    with San() as s:
        uv = s / "goc" / "usr" / "bin"
        p, gp, _uv, _xau, _t = _wp868_chay(s, apt="echo 'log trinh cai'; exit 0",
                                           lenh=f"sudo apt-get install -y ripgrep && echo {shlex.quote(str(uv))}")
        bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == "",
             f"cong thuc khong bo chon mat duong lui dong cuoi: rc={p.returncode} GITHUB_PATH={gp!r} {p.stderr[-300:]}")
    with San() as s:   # F868-03 (Codex lượt 1): trình cài Windows in CRLF ⇒ đường lùi vẫn cắt `\r`
        uv = s / "goc" / "usr" / "bin"
        p, _gp, _uv, _xau, _t = _wp868_chay(s, lenh=f"sudo apt-get install -y ripgrep && printf 'log\\r\\n%s\\r\\n' "
                                                  f"{shlex.quote(str(uv))}")
        bang(p.returncode == 0 and '"DAT"' in p.stdout,
             f"duong lui dong cuoi khong cat CR: rc={p.returncode} {p.stdout[-200:]} {p.stderr[-300:]}")


@ca
def r868_doc_kenh_hong_thi_dung():
    """F868-01 (Codex lượt 1): đọc kênh LỖI (cat giả rc 74 cho tệp kênh) không được coi là kênh rỗng rồi lấy dòng cuối
    stdout — trình cài in thư mục `xau` (có `rg` tốt KHÁC, ghi nhật ký khi bị gọi) ⇒ thoát ≠ 0, `rg` của `xau` không chạy.
    F868-05 (lượt 2): kênh đọc được mà SAI giao thức (`BAD_CHANNEL`) ⇒ thoát ≠ 0, không DAT. F868-02 (lượt 4): cả hai đường
    `exit 7` ấy vẫn dọn thư mục kênh (cat giả ghi lại đường dẫn kênh ⇒ chứng minh kênh có thật). Đối chứng: cat giả cho qua ⇒
    DAT và `xau` không bị gọi (stub trong suốt)."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    cat_that = shutil.which("cat")
    bang(cat_that is not None, "KHONG DO DUOC: thieu cat")
    for hong in ("", "loi", "rac"):
        with San() as s:
            nk, dau, tmp, kq = s / "xau.log", s / "dau", s / "tmp", s / "kq.log"
            tmp.mkdir()
            cat_gia = f"case \"$*\" in */kq) echo \"$*\" >> {shlex.quote(str(kq))};; esac; " + \
                {"": "", "loi": "case \"$*\" in */kq) echo 'cat: loi I/O gia' >&2; exit 74;; esac; ",
                 "rac": "case \"$*\" in */kq) printf BAD_CHANNEL; exit 0;; esac; "}[hong] + \
                f"exec {shlex.quote(cat_that)} \"$@\""
            p, gp, uv, _xau, _t = _wp868_chay(
                s, apt=f"echo {shlex.quote(str(s / 'xau'))}; exit 0",
                ung_vien={s / "xau": f"echo xau >> {shlex.quote(str(nk))}; echo 'ripgrep 14.1.0'", dau / "cat": cat_gia},
                env_them={"TMPDIR": str(tmp)})
            con = [x.name for x in tmp.iterdir() if x.name.startswith("cai_cong_cu.")]
            bang(kq.exists() and str(tmp) in kq.read_text(), f"KHONG DO DUOC {hong!r}: kenh khong duoc doc trong TMPDIR san")
            bang(con == [], f"kenh {hong!r}: thu muc kenh con sau khi thoat: rc={p.returncode} con={con}")
            if hong:
                dau_hieu = {"loi": "khong doc duoc kenh ket qua", "rac": "kenh ket qua hong"}[hong]
                bang(p.returncode != 0 and '"DAT"' not in p.stdout and not nk.exists() and dau_hieu in p.stderr,
                     f"kenh {hong} ma van chay tiep: rc={p.returncode} xau_goi={nk.exists()} {p.stderr[-300:]}")
            else:
                bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == str(uv) and not nk.exists(),
                     f"doi chung cat trong suot hong: rc={p.returncode} GITHUB_PATH={gp!r} {p.stderr[-300:]}")


@ca
def r868_ghi_kenh_hong_thi_dung():
    """F868-04 (Codex lượt 2): bộ chọn ghi kênh LỖI (`printf` bị thay bằng hàm bash nhập từ môi trường, rc 74 đúng cho
    payload `GIU_PATH` / `DICH`) ⇒ thoát ≠ 0, KHÔNG rơi về dòng cuối stdout (`xau`, `rg` tốt KHÁC có nhật ký). Cả hai
    nhánh: tên trần đã DAT (`GIU_PATH`) và chọn ứng viên (`DICH`). Đối chứng: không hàm giả ⇒ DAT, `xau` không bị gọi."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    ham = ("() { case \"$1\" in GIU_PATH|'DICH\\n%s') echo 'printf: loi ghi gia' >&2; return 74;; esac; "
           "builtin printf \"$@\"; }")
    for nhanh in ("GIU_PATH", "DICH"):
        for gia in (False, True):
            with San() as s:
                nk = s / "xau.log"
                uv = {s / "xau": f"echo xau >> {shlex.quote(str(nk))}; echo 'ripgrep 14.1.0'"}
                if nhanh == "GIU_PATH":
                    uv[s / "dau" / "rg"] = "echo 'ripgrep 14.1.0'"
                p, _gp, _uv, _xau, _t = _wp868_chay(s, apt=f"echo {shlex.quote(str(s / 'xau'))}; exit 0", ung_vien=uv,
                                                    env_them={"BASH_FUNC_printf%%": ham} if gia else None)
                if gia:
                    bang("printf: loi ghi gia" in p.stderr, f"KHONG DO DUOC {nhanh}: printf gia khong chay {p.stderr[-300:]}")
                    bang(p.returncode != 0 and '"DAT"' not in p.stdout and not nk.exists(),
                         f"{nhanh}: ghi kenh hong ma van chay tiep: rc={p.returncode} xau_goi={nk.exists()} "
                         f"{p.stderr[-300:]}")
                else:
                    bang(p.returncode == 0 and '"DAT"' in p.stdout and not nk.exists(),
                         f"{nhanh}: doi chung hong: rc={p.returncode} xau_goi={nk.exists()} {p.stderr[-300:]}")


@ca
def r868_don_kenh_khi_loi():
    """F868-02 (Codex lượt 1): thư mục tạm của kênh PHẢI bị xoá cả khi trình cài lỗi (trap EXIT), không chỉ ở đường thành
    công. Trình cài liệt kê $TMPDIR lúc chạy ⇒ chứng minh thư mục từng được tạo; sau đó không còn `cai_cong_cu.*`."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    for ma in (29, 0):
        with San() as s:
            tmp, nk = s / "tmp", s / "ls.log"
            tmp.mkdir()
            p, _gp, _uv, _xau, _t = _wp868_chay(s, apt=f'ls "$TMPDIR" > {shlex.quote(str(nk))}; exit {ma}',
                                                env_them={"TMPDIR": str(tmp)})
            thay = [x for x in (nk.read_text().split() if nk.exists() else []) if x.startswith("cai_cong_cu.")]
            con = [x.name for x in tmp.iterdir() if x.name.startswith("cai_cong_cu.")]
            bang(len(thay) == 1, f"KHONG DO DUOC: trinh cai khong thay thu muc kenh trong TMPDIR ({thay})")
            bang((p.returncode != 0) == (ma != 0) and con == [],
                 f"thu muc kenh con sau khi thoat (ma trinh cai {ma}): rc={p.returncode} con={con} {p.stderr[-200:]}")
    # `--bat-buoc`: các lượt `source` ghi đè trap của nhau ⇒ mỗi lượt phải TỰ xoá thư mục của nó (rm tường minh).
    with San() as s:
        tmp = s / "tmp"; tmp.mkdir()
        p, _gp, _uv, _d = _wp858_chay_cai(s, "rg", "linux", "echo 'ripgrep 14.1.0'", dau=None, bang_ke=("rg", "bash"),
                                          them={"rg": _WP858_HONG}, env_them={"TMPDIR": str(tmp)})
        con = [x.name for x in tmp.iterdir() if x.name.startswith("cai_cong_cu.")]
        bang(p.returncode == 0 and '"trang_thai_tong": "DAT"' in p.stdout and con == [],
             f"--bat-buoc: thu muc kenh ro: rc={p.returncode} con={con} {p.stderr[-300:]}")


@ca
def r868_vong_duyet_ung_vien():
    """N5 (F858-08): ứng viên TỐT duy nhất ở vị trí 3 ⇒ chọn nó; hai ứng viên tốt (3, 4) ⇒ chọn cái ĐẦU và `rg` của ứng
    viên 4 KHÔNG bị gọi (có `break`)."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    with San() as s:
        u = [s / f"u{i}" for i in range(1, 5)]
        nk = s / "u4.log"
        p, gp, _uv, _xau, _t = _wp868_chay(
            s, lenh="sudo apt-get install -y ripgrep && chon_thu_muc_chay_duoc rg " + " ".join(shlex.quote(str(d)) for d in u),
            ung_vien={u[0]: _WP858_HONG, u[1]: "exit 0", u[2]: "echo 'ripgrep 14.1.0'",
                      u[3]: f"echo u4 >> {shlex.quote(str(nk))}; echo 'ripgrep 14.1.0'"})
        bang(p.returncode == 0 and '"DAT"' in p.stdout and gp == str(u[2]),
             f"vong duyet khong chon ung vien tot DAU TIEN (vi tri 3): rc={p.returncode} GITHUB_PATH={gp!r} {p.stderr[-300:]}")
        bang(not nk.exists(), f"bo chon van goi ung vien sau khi da chon (thieu break): {nk.read_text() if nk.exists() else ''!r}")


@ca
def r868_hinh_dang_kenh_ket_qua():
    """Thuần Python, MỌI nền: cai_cong_cu.sh tạo kênh RIÊNG (mktemp, không export, trap), chạy công thức bằng subshell
    chuyển hướng vào TỆP (không `$( )` chờ EOF), đọc kênh trước, chỉ rơi về dòng cuối stdout khi kênh rỗng."""
    sh = CAI_SH_DANG_DUNG.read_text(encoding="utf-8")
    dau = sh.index("TAM_CAI=\"$(mktemp -d")
    than = sh[dau:sh.index('"${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json')]
    for can in ('TAM_CAI="$(mktemp -d "${TMPDIR:-/tmp}/cai_cong_cu.XXXXXX")"\ndeclare +x TAM_CAI\ntrap ',
                'KENH_KQ="$TAM_CAI/kq"\ndeclare +x KENH_KQ\n: > "$KENH_KQ"\n# eval',
                "trap 'rm -rf -- \"$TAM_CAI\"' EXIT\n", 'KENH_KQ="$TAM_CAI/kq"\ndeclare +x KENH_KQ\n',
                '( set +e; eval "$LENH" ) > "$TAM_CAI/stdout"\n',
                'KQ="$(cat -- "$KENH_KQ" && printf x)" || { echo "cai_cong_cu: khong doc duoc kenh ket qua" >&2; exit 7; }\n',
                "    DICH=\"${DICH%$'\\r'}\" ;;",
                '  GIU_PATH) DICH="" ;;\n', "  DICH$'\\n'?*) DICH=\"${KQ#DICH$'\\n'}\" ;;\n",
                '    KET_QUA_CAI="$(cat -- "$TAM_CAI/stdout")"\n', '  *) echo "cai_cong_cu: kenh ket qua hong',
                'rm -rf -- "$TAM_CAI"\n[ -d "$DICH" ] && export PATH="$DICH:$PATH"\n'):
        bang(can in than, f"cai_cong_cu.sh thieu chot kenh ket qua {can!r}")
    bang("$(eval" not in than and "KET_QUA_CAI=\"$(eval" not in sh, "cong thuc lai chay trong $( ) (cho EOF stdout)")
    bang(re.findall(r"^\s*trap\b.*$", sh, re.M) == ["trap 'rm -rf -- \"$TAM_CAI\"' EXIT"],
         "trap EXIT don kenh phai la DUY NHAT, khong bi go/ghi de")
    for can in ("printf 'GIU_PATH' > \"$KENH_KQ\" || { echo \"cai_cong_cu: khong ghi duoc kenh ket qua\" >&2; return 1; }",
                "printf 'DICH\\n%s' \"$dich\" > \"$KENH_KQ\" || { echo \"cai_cong_cu: khong ghi duoc kenh ket qua\" >&2; return 1; }",
                "printf '%q' \"$KQ\")\" >&2; exit 7 ;;"):
        bang(can in sh, f"cai_cong_cu.sh thieu chot ghi/doc kenh {can!r}")


# wp1045: `cong_cu.py kiem-tra --chi <ten>` rc=0 cho cong cu `bat_buoc: false` VANG MAT (#498, hop dong #290), nen bo chon
# tin rc da nhan `GIU_PATH` cho shellcheck khong co tren PATH (run 41069257658, windows-latest). Ca r858 luon dat ban HONG
# (`DO`, rc=2) o dau PATH nen khong phu ca VANG MAT; cong cu GIA ten la de PATH that (vd `/usr/bin/shellcheck`) khong che.
_WP1045_TUY = "tuychon1045x"
_WP1045_BB = "batbuoc1045x"
_WP1045_GIUA, _WP1045_SAU = "giua1045x", "sau1045x"


def _wp1045_chay(s, ten, cong_cu, tep=None, dau=None, lenh_rieng=None, hong=None):
    """Chạy cai_cong_cu.sh (`ten` hoặc `--bat-buoc`) trên bản kê CHỈ gồm công cụ GIẢ `cong_cu` = {tên: bat_buoc}; công
    thức mọi nền là `chon_thu_muc_chay_duoc <tên> "$UV_<TÊN>_RONG" "$UV_<TÊN>"` — ứng viên ĐẦU luôn RỖNG, nên bộ chọn
    tin rc (rc=0 cho công cụ tuỳ chọn vắng) sẽ chọn nhầm nó. `tep`: {tên: thư mục} đặt bản TỐT; `dau`: thư mục đặt
    ĐẦU PATH; `lenh_rieng`: {tên: công thức} thay công thức mặc định; `hong`: {tên: thư mục} đặt bản HỎNG (`exit 1`,
    tức `DO`). TMPDIR riêng `<sân>/tmp` để đếm thư mục tạm bị bỏ lại. Trả (p, các dòng $GITHUB_PATH, {tên: thư mục})."""
    import yaml
    kho = s / "kho"; ops = kho / "ops"; ops.mkdir(parents=True)
    shutil.copy2(LAUNCHER.parents[2] / "ops" / "bash_nen.py", ops / "bash_nen.py")
    shutil.copy2(CONG_CU_DANG_DUNG, ops / "cong_cu.py")
    shutil.copy2(CAI_SH_DANG_DUNG, ops / "cai_cong_cu.sh")
    uv = {t: s / f"uv_{t}" for t in cong_cu}
    bk = {"schema_version": 1, "cong_cu": {}}
    for t, bb in cong_cu.items():
        lenh = (lenh_rieng or {}).get(t) or f'chon_thu_muc_chay_duoc {t} "$UV_{t.upper()}_RONG" "$UV_{t.upper()}"'
        bk["cong_cu"][t] = {"bat_buoc": bb, "chuan_bi": True, "ban_ghim": None,
                            "probe": [{"ten": "mac_dinh", "lenh": [t, "--version"], "regex": r"version (\d+\.\d+\.\d+)"}],
                            "cai": {n: {"lenh": lenh} for n in ("linux", "macos", "windows")}}
        uv[t].mkdir()
        (s / f"uv_{t}_rong").mkdir()
    (ops / "cong_cu.yaml").write_text(yaml.safe_dump(bk, sort_keys=False), encoding="utf-8")
    for t, d in (hong or {}).items():
        d.mkdir(parents=True, exist_ok=True)
        (d / t).write_text("#!/bin/sh\nexit 1\n")
        (d / t).chmod(0o755)
    for t, d in (tep or {}).items():
        d.mkdir(parents=True, exist_ok=True)
        (d / t).write_text(f"#!/bin/sh\necho '{t} version 1.2.3'\n")
        (d / t).chmod(0o755)
    gp = s / "github_path"; gp.write_text("")
    (s / "tmp").mkdir()
    vo, env = _wp802_bash_env()
    env.update({f"UV_{t.upper()}": str(d) for t, d in uv.items()}, CONG_CU_NEN="linux", GITHUB_PATH=str(gp), TMPDIR=str(s / "tmp"),
               **{f"UV_{t.upper()}_RONG": str(s / f"uv_{t}_rong") for t in cong_cu},
               PATH=os.pathsep.join(([str(dau)] if dau else []) + [env.get("PATH", "")]))
    p = subprocess.run([vo, str(ops / "cai_cong_cu.sh"), ten], env=env, capture_output=True, text=True, timeout=180)
    return p, gp.read_text().split(), uv


@ca
def r1045_cong_cu_tuy_chon_vang_mat_khong_duoc_nhan_giu_path():
    """wp1045 M1/M2: công cụ `bat_buoc: false` VẮNG khỏi PATH. (a) ứng viên tốt (sau một ứng viên RỖNG) ⇒ rc 0,
    $GITHUB_PATH = ứng viên tốt, JSON DAT; (b) không ứng viên ⇒ bộ chọn THỬ ứng viên rồi thoát ≠ 0, $GITHUB_PATH rỗng;
    (c) tên trần tốt ⇒ rc 0, $GITHUB_PATH rỗng (đối chứng `GIU_PATH`); (d) công thức không qua bộ chọn trả 0 mà công cụ
    vẫn vắng ⇒ thoát 3 kèm dòng nêu tên (trước wp1045: rc 0, bước xanh)."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()                       # PyYAML vắng ⇒ ĐỎ, không bỏ qua
    t = _WP1045_TUY
    bang(shutil.which(t) is None, f"KHONG DO DUOC: {t} co tren PATH that")
    with San() as s:
        p, gp, uv = _wp1045_chay(s, t, {t: False}, tep={t: s / f"uv_{t}"})
        bang(p.returncode == 0 and gp == [str(uv[t])] and '"trang_thai": "DAT"' in p.stdout,
             f"(a) vang PATH + ung vien tot ma khong chon ung vien: rc={p.returncode} GITHUB_PATH={gp!r} "
             f"{p.stderr[-300:]}")
        bang("ten tran da DAT" not in p.stderr, f"(a) nhan GIU_PATH cho cong cu vang mat: {p.stderr[-300:]}")
    with San() as s:
        p, gp, _uv = _wp1045_chay(s, t, {t: False})
        bang(p.returncode != 0 and gp == [], f"(b) khong ung vien ma rc={p.returncode} GITHUB_PATH={gp!r}")
        bang(f"khong thu muc nao co '{t}' chay duoc" in p.stderr and "ten tran da DAT" not in p.stderr,
             f"(b) bo chon khong thu ung vien (nhan GIU_PATH?): {p.stderr[-300:]}")
    with San() as s:
        p, gp, _uv = _wp1045_chay(s, t, {t: False}, tep={t: s / "dau"}, dau=s / "dau")
        bang(p.returncode == 0 and gp == [] and "ten tran da DAT" in p.stderr,
             f"(c) ten tran tot ma khong GIU_PATH: rc={p.returncode} GITHUB_PATH={gp!r} {p.stderr[-300:]}")
    # Codex wp1045 lượt 1 (P2): (e) DO (bản hỏng đầu PATH) · (f) công cụ BẮT BUỘC vắng — công thức rc 0 ⇒ vẫn thoát 3 kèm dòng
    # nêu tên (kiểm cuối không được để errexit cắt trước chốt). (g, P3) công thức tự bật `set -e` ⇒ lỗi giữa chừng vẫn dừng.
    for nhan, ten_cc, bb in (("e-DO", t, False), ("f-bat-buoc-vang", _WP1045_BB, True)):
        with San() as s:
            kw = dict(hong={ten_cc: s / "dau"}, dau=s / "dau") if nhan == "e-DO" else {}
            p, _gp, _uv = _wp1045_chay(s, ten_cc, {ten_cc: bb}, lenh_rieng={ten_cc: "true"}, **kw)
            bang(p.returncode == 3 and f"'{ten_cc}' chua DAT sau khi cai" in p.stderr,
                 f"({nhan}) doi rc=3 kem dong neu ten, duoc rc={p.returncode} stderr={p.stderr[-300:]!r}")
    with San() as s:
        p, _gp, _uv = _wp1045_chay(s, t, {t: False}, tep={t: s / "dau"}, dau=s / "dau",
                                   lenh_rieng={t: "set -e; false; echo DA_DI_TIEP"})
        bang(p.returncode == 1 and "DA_DI_TIEP" not in p.stdout,
             f"(g) cong thuc tu bat set -e ma loi giua chung van di tiep: rc={p.returncode} {p.stdout[-200:]!r}")
    with San() as s:
        p, gp, _uv = _wp1045_chay(s, t, {t: False}, lenh_rieng={t: "true"})
        bang(p.returncode == 3 and f"'{t}' chua DAT sau khi cai" in p.stderr and '"trang_thai": "KHONG_DO_DUOC"' in p.stdout,
             f"(d) cong thuc rc 0 ma cong cu van vang: doi rc=3, duoc rc={p.returncode} {p.stderr[-300:]}")


@ca
def r1045_bat_buoc_cong_cu_tuy_chon_thieu_khong_chan_cong_cu_sau():
    """wp1045 M2: `--bat-buoc` — công cụ tuỳ chọn KHÔNG cài được đứng TRƯỚC công cụ bắt buộc cài được ⇒ công cụ bắt buộc
    vẫn được chọn (thoát 3 chỉ áp cho lời gọi TRỰC TIẾP, không cho lượt `source`)."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    # Hai đường hỏng của công cụ tuỳ chọn: bộ chọn không thấy ứng viên (rc≠0) · công thức rc 0 mà công cụ vẫn vắng.
    for nhan, rieng in (("bo-chon-hong", None), ("cong-thuc-rc0", {_WP1045_TUY: "true"})):
        with San() as s:
            p, gp, uv = _wp1045_chay(s, "--bat-buoc", {_WP1045_TUY: False, _WP1045_BB: True},
                                     tep={_WP1045_BB: s / f"uv_{_WP1045_BB}"}, lenh_rieng=rieng)
            bang(p.returncode == 0 and gp == [str(uv[_WP1045_BB])],
                 f"--bat-buoc ({nhan}): cong cu tuy chon thieu chan cong cu bat buoc sau no: rc={p.returncode} "
                 f"GITHUB_PATH={gp!r} {p.stderr[-300:]}")
            sot = sorted(x.name for x in (s / "tmp").iterdir())
            bang(sot == [], f"--bat-buoc ({nhan}): bo lai thu muc tam sau hai luot source: {sot}")


@ca
def r1045_bat_buoc_cong_cu_bat_buoc_hong_van_dung():
    """wp1045 M2 (đối chứng): `--bat-buoc` — công cụ BẮT BUỘC không cài được ⇒ vẫn thoát ≠ 0 như trước, không đi tiếp."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    with San() as s:
        p, gp, _uv = _wp1045_chay(s, "--bat-buoc", {_WP1045_BB: True, _WP1045_TUY: False},
                                  tep={_WP1045_TUY: s / f"uv_{_WP1045_TUY}"}, lenh_rieng={_WP1045_BB: "exit 47"})
        # Mã 47 (khác 1) để đo mã GỐC được giữ, không chỉ `≠ 0` (Codex wp1045 lượt 1, P3).
        bang(p.returncode == 47 and gp == [] and "--bat-buoc di tiep" not in p.stderr,
             f"--bat-buoc: cong cu bat buoc hong ma van di tiep: rc={p.returncode} GITHUB_PATH={gp!r} {p.stderr[-300:]}")


@ca
def r1045_bat_buoc_kiem_cuoi_luot_source_hong_thi_dung_ca_loat():
    """wp1045 (Codex lượt 2, P3): `--bat-buoc` ba công cụ — (1) bắt buộc cài được · (2) công thức rc 0 mà kiểm cuối của
    lượt `source` ra DO (bản hỏng đầu PATH, tuỳ chọn hoặc bắt buộc) · (3) công thức ghi dấu. Đòi rc = 2 (mã DO của
    `cong_cu.py`) và công cụ (3) KHÔNG được chạy: lỗi kiểm cuối của lượt source phải dừng cả loạt như base."""
    if LA_WINDOWS:
        return "BO QUA shell POSIX"
    _wp802_rg_yaml()
    for bb_giua in (False, True):
        with San() as s:
            dau_ky = s / "uv_sau1045x" / "DA_CHAY"
            p, _gp, _uv = _wp1045_chay(
                s, "--bat-buoc", {_WP1045_BB: True, _WP1045_GIUA: bb_giua, _WP1045_SAU: True},
                tep={_WP1045_BB: s / f"uv_{_WP1045_BB}"}, hong={_WP1045_GIUA: s / "dau"}, dau=s / "dau",
                lenh_rieng={_WP1045_GIUA: "true", _WP1045_SAU: f"touch {shlex.quote(str(dau_ky))}"})
            bang(p.returncode == 2 and not dau_ky.exists(),
                 f"--bat-buoc (giua bat_buoc={bb_giua}): kiem cuoi DO cua luot source khong dung ca loat: "
                 f"rc={p.returncode} cong cu sau da chay={dau_ky.exists()} {p.stderr[-300:]}")


@ca
def r1045_hinh_dang_dat_theo_trang_thai():
    """Thuần Python, MỌI nền: bộ chọn quyết DAT qua `cong_cu_dat` (trạng thái CHÍNH công cụ, không rc) ở tên trần và vòng
    ứng viên; `cong_cu_dat` đọc `trang_thai` + đúng một mục; lời gọi trực tiếp thoát 3 khi chưa DAT, lượt `source` thì không."""
    sh = CAI_SH_DANG_DUNG.read_text(encoding="utf-8")
    bang(re.search(r"^cong_cu_json_dung\(\) \{", sh, re.M), "cai_cong_cu.sh thieu ham cong_cu_json_dung")
    ham = sh[sh.index("cong_cu_json_dung() {"):]
    ham = ham[:ham.index("\n}\n")]
    bang("cong_cu_dat() { cong_cu_json_dung \"$1\" trang_thai '\"DAT\"'; }" in sh, "cong_cu_dat khong doc trang_thai == DAT")
    for can in ('kiem-tra --chi "$1" --json', '|| return 1', 'len(c) == 1', 'c[0].get("ten") == sys.argv[1]',
                'c[0].get(sys.argv[2]) == json.loads(sys.argv[3])'):
        bang(can in ham, f"cong_cu_json_dung thieu {can!r}")
    bang('if [ "${CAI_CONG_CU_PY_CUA:-}" = "$$" ] && cong_cu_json_dung "$TEN" bat_buoc false; then' in sh
         and '    return 0\n  fi\n  exit "$RC_CAI"\nfi\n' in sh,
         "luot source cua --bat-buoc phai di tiep khi cong cu tuy chon cai hong, con lai thoat dung ma cu")
    than = sh[sh.index("chon_thu_muc_chay_duoc() {"):]
    than = than[:than.index("\n}\n")]
    for can in ('  if cong_cu_dat "$ten"; then\n', 'if PATH="$d:$PATH" cong_cu_dat "$ten"; then dich="$d"; break; fi'):
        bang(can in than, f"bo chon thieu {can!r}")
    bang("kiem-tra --chi" not in than, "bo chon con goi kiem-tra truc tiep (tin rc)")
    moc_cuoi = 'if [ "${CAI_CONG_CU_PY_CUA:-}" = "$$" ]; then\n  "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra'
    bang(moc_cuoi in sh, "dong kiem cuoi khong tach luot source khoi loi goi truc tiep")
    cuoi = sh[sh.index(moc_cuoi):]
    bang('  "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json || RC_KT=$?\n  if [ "$RC_KT" -ne 0 ] || ! cong_cu_dat "$TEN"; then' in cuoi and "    exit 3\n  fi\nfi" in cuoi,
         "dong kiem cuoi thieu thoat 3 cho loi goi truc tiep khi chua DAT")
    bang("set +e\n( set +e; eval \"$LENH\" ) > \"$TAM_CAI/stdout\"\nRC_CAI=$?\nset -e\n" in sh
         and ") > \"$TAM_CAI/stdout\" ||" not in sh, "dong eval bi dat vao ngu canh dieu kien (`||` vo hieu set -e)")


# ---------------------------------------------------------------------------------------------
# wp685 (LAUNCHER-CON-SONG-ESRCH, đặc tả r28 §7 B1–B4) — helper theo NHÃN cho t156/t157.
# Nguồn: PR #679 job 109303373142 (ESRCH thoát khỏi `_con_song`); cross-review lượt 1–12 trên
# PR #688 (bảng không gian mở rộng, quy ước đếm, payload theo dõi, `read args`).
# Mỗi `bang` mở đầu bằng NHÃN (rồi tiểu nhãn nếu có) rồi LOẠI assertion. Helper nhận hai tham số
# tuỳ chọn `chay` (tập nhãn CHẠY; mặc định: mọi nhãn) và `noi` (tập nhãn NỚI; mặc định: rỗng) —
# ca đăng ký KHÔNG truyền chúng; chỉ tập lệnh bằng chứng (A/W, D) gọi thẳng.
# ---------------------------------------------------------------------------------------------
CS_NHAN_T156 = ("B1", "B2-eacces", "B2-eio", "B2-eperm-hoi", "B2-doc-hong", "B2-tin-hieu", "B2-dem-lan",
                "B2-exception", "B2-thoat-parse", "B2-parse", "B2-dem-doc", "B2-pid-du-phong", "B2-nhanh-cu",
                "B3-song", "B3-da-wait", "B3-zombie")
CS_NHAN_T157 = ("B3b-giet-cay",)
_CS_COMM_ZOMBIE = b"x) R (y" + b"\xe1\xba"     # trục S: chỉ tách theo `)` CUỐI mới đọc ra `Z`; đuôi UTF-8 hỏng


class _CsChuoi(str):
    """PAYLOAD THEO DÕI (B2-parse, r9): các phép tách của nền trả đối tượng theo dõi; hỏng thì ném
    ĐÚNG đối tượng lỗi do seam tạo sẵn (nhận bằng danh tính, không bằng kiểu hay đối số)."""

    def _loi(self, loai):
        return self.__dict__.get("loi_" + loai)

    def _boc(self, v):
        if isinstance(v, str) and not isinstance(v, _CsChuoi):
            v = _CsChuoi(v)
            v.__dict__.update({k: x for k, x in self.__dict__.items() if k.startswith("loi_")})
        return v

    def rindex(self, *a):
        try:
            return str.rindex(self, *a)
        except ValueError:
            raise self._loi("value") from None

    def index(self, *a):
        try:
            return str.index(self, *a)
        except ValueError:
            raise self._loi("value") from None

    def __getitem__(self, k):
        return self._boc(str.__getitem__(self, k))

    def split(self, *a, **kw):
        ds = _CsDanhSach(self._boc(x) for x in str.split(self, *a, **kw))
        ds.loi_index = self._loi("index")
        return ds


class _CsDanhSach(list):
    loi_index = None

    def __getitem__(self, k):
        try:
            return list.__getitem__(self, k)
        except IndexError:
            raise self.loi_index from None


def _cs_payload(s: str, loi_value, loi_index):
    p = _CsChuoi(s)
    p.__dict__.update(loi_value=loi_value, loi_index=loi_index)
    return p


class _CsSeam:
    """Seam `Path.stat` / `Path.exists` / phép đọc theo DANG_DOC_QA7 / observer `os.kill(pid, 0)`, mỗi cái khoá theo
    ĐÚNG `/proc/<pid>/stat` (hay cặp (pid, 0)) của các PID đang xét, có bộ đếm. Không giao lỗi ⇒ chỉ đếm rồi chuyển
    tiếp thật; lời gọi thật ném thì không ghi gì (vô can) — TRỪ observer `kill`: nó ghi CHÍNH đối tượng thật rồi ném
    lại (loại ghi nhận (2))."""

    def __init__(self, pids, stat=None, exists=None, doc=None, kill=None, kill_dem=False):
        self.duong = {f"/proc/{p}/stat" for p in pids}
        self.pids = set(pids)
        self.stat, self.exists, self.doc, self.kill = stat, exists, doc, kill
        self.kill_dem = kill_dem or kill is not None
        self.n_stat = self.n_exists = self.n_doc = self.n_kill = 0
        self.doc_args = []
        self.kill_that = []
        self.tao = []          # mọi đối tượng lỗi do seam TẠO (kể cả qua hàm theo lần chạm) — loại ghi nhận (1)
        self.goc = {}

    def _lay(self, gt, n):
        v = gt(n) if callable(gt) and not isinstance(gt, BaseException) else gt
        if isinstance(v, BaseException):
            self.tao.append(v)
        return v

    def __enter__(self):
        seam = self
        ten_doc = DANG_DOC_QA7[0]
        for t in ("stat", "exists", ten_doc):
            self.goc[t] = (t in Path.__dict__, getattr(Path, t))
        g_stat, g_exists, g_doc = self.goc["stat"][1], self.goc["exists"][1], self.goc[ten_doc][1]

        def f_stat(p, *a, **k):
            if str(p) not in seam.duong:
                return g_stat(p, *a, **k)
            seam.n_stat += 1
            v = seam._lay(seam.stat, seam.n_stat)
            if isinstance(v, BaseException):
                raise v
            return g_stat(p, *a, **k)

        def f_exists(p, *a, **k):
            if str(p) not in seam.duong or seam.exists is None:
                return g_exists(p, *a, **k)
            seam.n_exists += 1
            raise seam.exists

        def f_doc(p, *a, **k):
            if str(p) not in seam.duong:
                return g_doc(p, *a, **k)
            seam.n_doc += 1
            seam.doc_args.append((ten_doc, a, k))
            v = seam._lay(seam.doc, seam.n_doc)
            if isinstance(v, BaseException):
                raise v
            if v is not None:
                return v
            return g_doc(p, *a, **k)

        self.g_kill = os.kill

        def f_kill(pid, sig):
            if pid not in seam.pids or sig != 0 or not seam.kill_dem:
                return seam.g_kill(pid, sig)
            seam.n_kill += 1
            if seam.kill is not None:
                raise seam.kill
            try:
                return seam.g_kill(pid, sig)
            except BaseException as e:
                seam.kill_that.append(e)
                raise
        Path.stat, Path.exists = f_stat, f_exists
        setattr(Path, ten_doc, f_doc)
        os.kill = f_kill
        return self

    def __exit__(self, *a):
        os.kill = self.g_kill
        for t, (co, g) in self.goc.items():
            if co:
                setattr(Path, t, g)
            else:
                delattr(Path, t)
        return False


class _CsNhan:
    """Một nhãn: kiểm (qua `bang`, tra lúc gọi để phép D bọc được) trừ khi nhãn bị NỚI."""

    def __init__(self, nhan, noi):
        self.nhan, self.noi = nhan, (nhan in noi)

    def kiem(self, dk, tieu, loai):
        if not self.noi:
            bang(dk, f"{self.nhan}{' ' + tieu if tieu else ''} {loai}")

    def goi(self, tieu, fn, seam, mong=(), parse=()):
        """Gọi `fn()`; trả (kết quả, có_ngoại_lệ_mong_đợi). Phân hạng ngoại lệ THOÁT theo bốn loại của quy ước chung;
        loại khác giữ hạng vô can (ném lại nguyên). `mong`: sentinel PHẢI thoát (so `is`)."""
        try:
            return fn(), None
        except BaseException as e:   # noqa: BLE001 — phân hạng rồi ném lại mọi thứ ngoài bốn loại ghi nhận
            if any(e is s for s in mong):
                return None, e
            ghi = [x for x in (seam.stat, seam.exists, seam.doc, seam.kill) if isinstance(x, BaseException)]
            ghi += seam.tao + seam.kill_that
            loai = None
            if any(e is x for x in ghi):
                loai = "seam escaped"
            elif any(e is x for x in parse):
                loai = "parse error escaped"
            else:
                c = e.__cause__
                while c is not None and loai is None:
                    if any(c is x for x in ghi) or any(c is x for x in mong):
                        loai = "seam wrapped"
                    elif any(c is x for x in parse):
                        loai = "parse error wrapped"
                    c = c.__cause__
            if loai is None:
                raise
            if self.noi:
                return None, None
            bang(False, f"{self.nhan}{' ' + tieu if tieu else ''} {loai} ({type(e).__name__}: {e})")
            raise AssertionError("khong toi duoc")   # bang(False) luôn ném

    def dem(self, tieu, seam, hoi=None, doc=None, kill=None, hoi_exists=False):
        if hoi is not None:
            n = seam.n_exists if hoi_exists else seam.n_stat
            self.kiem(n == hoi, tieu, f"{'exists' if hoi_exists else 'stat'} count {n}")
        if doc is not None:
            if doc == "<=1":
                self.kiem(seam.n_doc <= 1, tieu, f"read count {seam.n_doc}")
            else:
                self.kiem(seam.n_doc == doc, tieu, f"read count {seam.n_doc}")
            lech = sorted({repr(x) for x in seam.doc_args if x != DANG_DOC_QA7})
            self.kiem(not lech, tieu, f"read args {lech[:3]}")
        if kill is not None:
            self.kiem(seam.n_kill == kill, tieu, f"kill count {seam.n_kill}")


def _cs_con_cho(ma: str):
    """Con THẬT, session riêng; trả Popen. Dọn bằng PID tường minh (`_cs_don`)."""
    return subprocess.Popen([PY, "-c", ma], start_new_session=True, stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _cs_don(p):
    if p is None:
        return
    with contextlib.suppress(OSError):
        os.kill(p.pid, signal.SIGKILL)
    with contextlib.suppress(Exception):
        p.wait(timeout=10)


def _cs_doc_bytes(pid):
    with open(f"/proc/{pid}/stat", "rb") as f:
        return f.read()


def _cs_con_da_wait():
    p = _cs_con_cho("import time; time.sleep(60)")
    p.kill()
    p.wait(timeout=10)
    return p.pid


def _cs_con_comm(comm: bytes, tep: Path):
    """Con đặt `comm` bằng prctl (dạng BYTES, không phụ thuộc locale) rồi ghi tệp sẵn sàng; điều kiện dựng kiểm bằng
    phép đọc bytes độc lập. Không đạt ⇒ lỗi thường (KHÔNG `bang`)."""
    ma = (f"import ctypes, time\nctypes.CDLL(None).prctl(15, bytes.fromhex({comm.hex()!r}), 0, 0, 0)\n"
          f"open({str(tep)!r}, 'w').write('1')\ntime.sleep(60)\n")
    p = _cs_con_cho(ma)
    try:
        het = time.time() + 10
        while not (tep.exists() and tep.stat().st_size):
            if time.time() > het:
                raise RuntimeError("dieu kien dung: con chua san sang")
            time.sleep(0.02)
        nd = _cs_doc_bytes(p.pid)
        if nd[nd.index(b"(") + 1:nd.rindex(b")")] != comm:
            raise RuntimeError(f"dieu kien dung: comm chua doi: {nd[:60]!r}")
    except BaseException:
        _cs_don(p)
        raise
    return p


def _cs_con_utf8_hong(tep: Path):
    """Đầu vào nội dung THẬT (`B2-dem-doc 4`, `B2-nhanh-cu utf8-hong-that`): comm = 15 byte UTF-8 hỏng, và NGOÀI cửa
    sổ đếm `read_text()` thật không đối số phải ném UnicodeDecodeError (chứng tỏ đầu vào có răng với cách đọc nền)."""
    p = _cs_con_comm(_K124_COMM, tep)
    try:
        Path(f"/proc/{p.pid}/stat").read_text()
    except UnicodeDecodeError:
        return p
    except BaseException:
        _cs_don(p)
        raise
    _cs_don(p)
    raise RuntimeError("dieu kien dung: read_text() khong doi so giai ma duoc comm hong (locale)")


def _cs_chay_t156(m, chay=None, noi=()):   # noqa: C901 — một đơn vị mỗi nhãn, đúng thứ tự cố định của §7
    chay = CS_NHAN_T156 if chay is None else tuple(chay)
    noi = frozenset(noi)
    me = os.getpid()
    E = errno

    def loi(cls, so):
        return cls(so, os.strerror(so))

    def don_vi(nhan):
        return _CsNhan(nhan, noi)

    for nhan in CS_NHAN_T156:
        if nhan not in chay:
            continue
        L = don_vi(nhan)
        if nhan == "B1":
            chet = _cs_con_da_wait()
            khoa = m._khoa_danh_tinh(me)
            with _CsSeam([me, chet], stat=loi(ProcessLookupError, E.ESRCH)) as s:
                kq, _ = L.goi("", lambda: m._con_song(me), s)
                L.kiem(kq is False, "", f"result {kq}")
                L.dem("", s, hoi=1)
                kq, _ = L.goi("", lambda: m._con_song_dung_khoa(me, khoa), s)
                L.kiem(kq is False, "", f"result {kq}")
                L.dem("", s, hoi=2)
                L.goi("", lambda: m._giet_rieng({chet: "k"}, 0), s)
                L.dem("", s, hoi=3)
        elif nhan in ("B2-eacces", "B2-eio", "B2-eperm-hoi"):
            o = {"B2-eacces": loi(PermissionError, E.EACCES), "B2-eio": loi(OSError, E.EIO),
                 "B2-eperm-hoi": loi(PermissionError, E.EPERM)}[nhan]
            with _CsSeam([me], stat=o) as s:
                kq, _ = L.goi("", lambda: m._con_song(me), s)
                L.kiem(kq is True, "", f"result {kq}")
                L.dem("", s, hoi=1, doc=1)
        elif nhan == "B2-doc-hong":
            for tieu, o in (("EACCES", loi(PermissionError, E.EACCES)), ("EIO", loi(OSError, E.EIO)),
                            ("ESRCH", loi(ProcessLookupError, E.ESRCH)), ("EPERM", loi(PermissionError, E.EPERM))):
                with _CsSeam([me], stat=loi(PermissionError, E.EACCES), doc=o, kill_dem=True) as s:
                    kq, _ = L.goi(tieu, lambda: m._con_song(me), s)
                    L.kiem(kq is True, tieu, f"result {kq}")
                    L.dem(tieu, s, hoi=1, doc=1, kill=1)
        elif nhan in ("B2-tin-hieu", "B2-exception"):
            cls = KeyboardInterrupt if nhan == "B2-tin-hieu" else RuntimeError
            for tieu in ("hoi", "doc", "kill"):
                sen = cls(f"sentinel {nhan} {tieu}")
                kw = {"hoi": dict(stat=sen),
                      "doc": dict(stat=loi(PermissionError, E.EACCES), doc=sen),
                      "kill": dict(stat=loi(PermissionError, E.EACCES), doc=loi(PermissionError, E.EACCES),
                                   kill=sen)}[tieu]
                with _CsSeam([me], **kw) as s:
                    _kq, ra = L.goi(tieu, lambda: m._con_song(me), s, mong=(sen,))
                    L.kiem(ra is sen, tieu, "sentinel identity")
                    L.dem(tieu, s, hoi=1, doc=None if tieu == "hoi" else 1, kill=1 if tieu == "kill" else None)
        elif nhan == "B2-dem-lan":
            with _CsSeam([me], stat=lambda n: None if n == 1 else loi(ProcessLookupError, E.ESRCH), doc=None) as s:
                kq, _ = L.goi("", lambda: m._con_song(me), s)
                L.kiem(kq is True, "", f"result {kq}")
                L.dem("", s, hoi=1, doc="<=1")
        elif nhan == "B2-thoat-parse":
            for tieu, cls in (("hoi-index", IndexError), ("hoi-value", ValueError),
                              ("hoi-decode", UnicodeDecodeError), ("kill-index", IndexError),
                              ("kill-value", ValueError), ("kill-decode", UnicodeDecodeError)):
                sen = (UnicodeDecodeError("utf8", bytes([255]), 0, 1, "x") if cls is UnicodeDecodeError
                       else cls(f"sentinel {tieu}"))
                # #743: phép thăm dò là `Path.stat` (không còn `Path.exists`, vốn nuốt OSError từ 3.14).
                if tieu.startswith("hoi"):
                    kw = dict(stat=sen)
                else:
                    kw = dict(stat=loi(PermissionError, E.EACCES), doc=loi(PermissionError, E.EACCES), kill=sen)
                with _CsSeam([me], **kw) as s:
                    _kq, ra = L.goi(tieu, lambda: m._con_song(me), s, mong=(sen,))
                    if tieu.startswith("hoi") and s.n_stat == 0:
                        raise RuntimeError(f"{nhan} {tieu}: seam Path.stat khong cham - doi seam sang ham ung vien goi")
                    L.kiem(ra is sen, tieu, "sentinel identity")
                    if tieu.startswith("hoi"):
                        L.dem(tieu, s, hoi=1)
                    else:
                        L.dem(tieu, s, hoi=1, doc=1, kill=1)
        elif nhan == "B2-parse":
            for tieu, noi_dung in (("p1", [""]), ("p2", [f"{me} x S 1"]), ("p3", [f"{me} (x)", f"{me} (x) "]),
                                   ("p4", [None])):
                for nd in noi_dung:
                    lv, li = ValueError("substring not found"), IndexError("list index out of range")
                    doc = (UnicodeDecodeError("utf-8", b"\xe1\xba", 0, 2, "unexpected end of data") if nd is None
                           else _cs_payload(nd, lv, li))
                    with _CsSeam([me], stat=loi(PermissionError, E.EACCES), doc=doc, kill_dem=True) as s:
                        kq, _ = L.goi(tieu, lambda: m._con_song(me), s, parse=(lv, li))
                        L.kiem(kq is True, tieu, f"result {kq}")
                        L.dem(tieu, s, hoi=1, doc=1, kill=1)
        elif nhan == "B2-dem-doc":
            for tieu in ("1", "2", "3", "4"):
                con = None
                try:
                    if tieu == "4":
                        with San() as sd:
                            con = _cs_con_utf8_hong(sd / "san")
                        pid = con.pid
                    else:
                        pid = me
                    st = loi(OSError, E.EIO) if tieu == "2" else loi(PermissionError, E.EACCES)
                    doc = loi(PermissionError, E.EACCES) if tieu == "3" else None
                    with _CsSeam([pid], stat=st, doc=doc, kill_dem=tieu in ("3", "4")) as s:
                        kq, _ = L.goi(tieu, lambda: m._con_song(pid), s)
                        L.kiem(kq is True, tieu, f"result {kq}")
                        L.dem(tieu, s, hoi=1, doc=1, kill={"3": 1, "4": 0}.get(tieu))
                finally:
                    _cs_don(con)
        elif nhan == "B2-pid-du-phong":
            chet = _cs_con_da_wait()
            for tieu in ("song", "da-wait", "eperm", "eio"):
                pid = chet if tieu == "da-wait" else me
                mong_kq = tieu in ("song", "eperm")
                for doc_tieu in ("EACCES", "EIO", "ESRCH", "p1", "p2", "p3", "p3s", "p4"):
                    lv, li = ValueError("substring not found"), IndexError("list index out of range")
                    doc = {"EACCES": loi(PermissionError, E.EACCES), "EIO": loi(OSError, E.EIO),
                           "ESRCH": loi(ProcessLookupError, E.ESRCH), "p1": _cs_payload("", lv, li),
                           "p2": _cs_payload(f"{pid} x S 1", lv, li), "p3": _cs_payload(f"{pid} (x)", lv, li),
                           "p3s": _cs_payload(f"{pid} (x) ", lv, li),
                           "p4": UnicodeDecodeError("utf-8", b"\xe1\xba", 0, 2, "unexpected end of data")}[doc_tieu]
                    kill = {"eperm": loi(PermissionError, E.EPERM), "eio": loi(OSError, E.EIO)}.get(tieu)
                    with _CsSeam([pid], stat=loi(PermissionError, E.EACCES), doc=doc, kill=kill, kill_dem=True) as s:
                        kq, _ = L.goi(tieu, lambda: m._con_song(pid), s,
                                      parse=(lv, li) if doc_tieu in ("p1", "p2", "p3", "p3s") else ())
                        L.dem(tieu, s, kill=1)
                        L.kiem(kq is mong_kq, tieu, f"result {kq}")
                        L.dem(tieu, s, hoi=1, doc=1)
        elif nhan == "B2-nhanh-cu":
            chet = _cs_con_da_wait()
            for tieu in ("song", "EACCES", "EIO", "ESRCH", "EPERM", "p1", "p3", "p4", "utf8-hong-that", "tin-hieu",
                         "exception"):
                con = None
                try:
                    pid = me
                    if tieu == "utf8-hong-that":
                        with San() as sd:
                            con = _cs_con_utf8_hong(sd / "san")
                        pid = con.pid
                    lv, li = ValueError("substring not found"), IndexError("list index out of range")
                    doc = {"EACCES": loi(PermissionError, E.EACCES), "EIO": loi(OSError, E.EIO),
                           "ESRCH": loi(ProcessLookupError, E.ESRCH), "EPERM": loi(PermissionError, E.EPERM),
                           "p1": _cs_payload("", lv, li), "p3": _cs_payload(f"{pid} (x)", lv, li),
                           "p4": UnicodeDecodeError("utf-8", b"\xe1\xba", 0, 2, "unexpected end of data"),
                           "tin-hieu": KeyboardInterrupt("sentinel B2-nhanh-cu tin-hieu"),
                           "exception": RuntimeError("sentinel B2-nhanh-cu exception")}.get(tieu)
                    sen = (doc,) if tieu in ("tin-hieu", "exception") else ()
                    with _CsSeam([pid], doc=doc, kill_dem=True) as s:
                        kq, ra = L.goi(tieu, lambda: m._con_song(pid), s, mong=sen,
                                       parse=(lv, li) if tieu in ("p1", "p3") else ())
                        if sen:
                            L.kiem(ra is doc, tieu, "sentinel identity")
                        else:
                            mong_kq = tieu in ("song", "utf8-hong-that")
                            L.kiem(kq is mong_kq, tieu, f"result {kq}")
                        L.dem(tieu, s, hoi=1, doc=1, kill=0)
                finally:
                    _cs_don(con)
            for tieu in ("vang", "vang-da-wait", "vang-eperm", "vang-eio", "vang-tin-hieu", "vang-exception",
                         "vang-index", "vang-value", "vang-decode"):
                pid = chet if tieu == "vang-da-wait" else me
                st = None if tieu == "vang-da-wait" else loi(FileNotFoundError, E.ENOENT)
                kill = {"vang-eperm": loi(PermissionError, E.EPERM), "vang-eio": loi(OSError, E.EIO),
                        "vang-tin-hieu": KeyboardInterrupt("sentinel vang-tin-hieu"),
                        "vang-exception": RuntimeError("sentinel vang-exception"),
                        "vang-index": IndexError("sentinel vang-index"),
                        "vang-value": ValueError("sentinel vang-value"),
                        "vang-decode": UnicodeDecodeError("utf8", bytes([255]), 0, 1, "x")}.get(tieu)
                sen = (kill,) if tieu in ("vang-tin-hieu", "vang-exception", "vang-index", "vang-value",
                                          "vang-decode") else ()
                with _CsSeam([pid], stat=st, kill=kill, kill_dem=True) as s:
                    kq, ra = L.goi(tieu, lambda: m._con_song(pid), s, mong=sen)
                    if sen:
                        L.kiem(ra is kill, tieu, "sentinel identity")
                    else:
                        mong_kq = tieu in ("vang", "vang-eperm")
                        L.kiem(kq is mong_kq, tieu, f"result {kq}")
                    L.dem(tieu, s, hoi=1, doc=0, kill=1)
        elif nhan == "B3-song":
            kq = m._con_song(me)
            L.kiem(kq is True, "", f"result {kq}")
        elif nhan == "B3-da-wait":
            kq = m._con_song(_cs_con_da_wait())
            L.kiem(kq is False, "", f"result {kq}")
        elif nhan == "B3-zombie":
            con = None
            try:
                with San() as sd:
                    con = _cs_con_comm(_CS_COMM_ZOMBIE, sd / "san")
                khoa = m._khoa_danh_tinh(con.pid)
                os.kill(con.pid, signal.SIGTERM)
                het = time.time() + 10
                while True:
                    nd = _cs_doc_bytes(con.pid)
                    if nd[nd.rindex(b")") + 2:].split()[0] == b"Z":
                        break
                    if time.time() > het:
                        raise RuntimeError("dieu kien dung: con khong chuyen sang Z")
                    time.sleep(0.02)
                if b"(" + _CS_COMM_ZOMBIE + b")" not in nd:
                    raise RuntimeError(f"dieu kien dung: comm zombie khong dung: {nd[:60]!r}")
                pid = con.pid
                with _CsSeam([pid], stat=loi(PermissionError, E.EACCES)) as s:
                    kq, _ = L.goi("", lambda: m._con_song(pid), s)
                    L.kiem(kq is False, "", f"result {kq}")
                    L.dem("", s, hoi=1, doc=1)
                    kq, _ = L.goi("", lambda: m._con_song_dung_khoa(pid, khoa), s)
                    L.kiem(kq is False, "", f"result {kq}")
                    L.dem("", s, hoi=2, doc=2)
                with _CsSeam([pid], kill_dem=True) as s:
                    kq, _ = L.goi("", lambda: m._con_song(pid), s)
                    L.kiem(kq is False, "", f"result {kq}")
                    L.dem("", s, hoi=1, doc=1, kill=0)
            finally:
                _cs_don(con)


def _cs_chay_t157(m, chay=None, noi=()):
    chay = CS_NHAN_T157 if chay is None else tuple(chay)
    if "B3b-giet-cay" not in chay:
        return
    L = _CsNhan("B3b-giet-cay", frozenset(noi))
    con = _cs_con_cho("import time; time.sleep(60)")
    try:
        khoa = m._khoa_danh_tinh(con.pid)
        if khoa is None:
            raise RuntimeError("dieu kien dung: khong lay duoc khoa cua con")
        with _CsSeam([con.pid], stat=PermissionError(errno.EACCES, os.strerror(errno.EACCES))) as s:
            kg, _ = L.goi("", lambda: m._giet_cay(con.pid, khoa), s)
            if s.n_stat == 0 and not L.noi:
                raise RuntimeError("B3b-giet-cay: seam Path.stat khong cham")
            L.kiem(kg is not None and kg.tron_ven, "", f"result {getattr(kg, 'tron_ven', None)} "
                                                       f"({getattr(kg, 'mo_ta', '')})")
    finally:
        _cs_don(con)


@ca
def t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan():
    """wp685 B1–B4: `_con_song` không để OSError của phép hỏi `/proc/<pid>/stat` thoát; ESRCH ⇒ chết; lỗi khác
    không kết luận, đọc nội dung rồi rơi về `kill(pid, 0)`; phạm vi bắt và số lần theo bảng không gian mở rộng."""
    if platform.system() != "Linux":
        return "bo qua: nhanh /proc chi co tren Linux"
    _cs_chay_t156(_tai_launcher_thu())


@ca
def t157_giet_cay_khi_stat_EACCES_van_tron_ven():
    """wp685 B3b: `_giet_cay` với `Path.stat` EACCES trên con phải biến nó thành zombie và báo `tron_ven=True`."""
    if platform.system() != "Linux":
        return "bo qua: nhanh /proc chi co tren Linux"
    _cs_chay_t157(_tai_launcher_thu())


@ca
def r743_con_song_tham_do_bang_stat_giu_errno_moi_phien_ban():
    """#743 (py314-path-exists-nuot-oserror): `_con_song` thăm dò `/proc/<pid>/stat` bằng `Path.stat`, KHÔNG bằng
    `Path.exists` — từ Python 3.14 `exists()` nuốt mọi OSError thành False và không qua `Path.stat`, nên t156/t157 đỏ.
    Ca này ĐỘC LẬP phiên bản: seam `Path.exists` ném sentinel, nên gọi lại `exists()` thì ĐỎ ngay trên 3.12 của CI.
    Phân loại errno theo đặc tả r1 Q2: ENOENT/ENOTDIR ⇒ không có tệp (không đọc, hỏi kill); ESRCH ⇒ False (không
    đọc, không kill); OSError khác (EACCES, ELOOP, EBADF) ⇒ chưa kết luận (đọc đúng một lần)."""
    if platform.system() != "Linux":
        return "bo qua: nhanh /proc chi co tren Linux"
    m = _tai_launcher_thu()
    me = os.getpid()

    def loi(cls, so):
        return cls(so, os.strerror(so))

    def goi(tieu, s, sen):
        try:
            return m._con_song(me)
        except BaseException as e:   # noqa: BLE001 — sentinel của seam exists phải thành chốt, không thành traceback
            if e is sen:
                bang(False, f"{tieu}: _con_song cham Path.exists (sentinel thoat) - tham do phai la Path.stat")
            raise

    bang_ca = (
        # tiểu nhãn, lỗi stat, kết quả, số lần đọc, số lần kill(pid, 0)
        ("EACCES", loi(PermissionError, errno.EACCES), True, 1, 0),
        ("ESRCH", loi(ProcessLookupError, errno.ESRCH), False, 0, 0),
        ("ENOENT", loi(FileNotFoundError, errno.ENOENT), True, 0, 1),
        ("ENOTDIR", loi(NotADirectoryError, errno.ENOTDIR), True, 0, 1),
        ("ELOOP", loi(OSError, errno.ELOOP), True, 1, 0),
        ("EBADF", loi(OSError, errno.EBADF), True, 1, 0),
    )
    for tieu, o, mong, n_doc, n_kill in bang_ca:
        sen = RuntimeError(f"sentinel r743 exists {tieu}")
        with _CsSeam([me], stat=o, exists=sen, kill_dem=True) as s:
            kq = goi(tieu, s, sen)
            bang(s.n_exists == 0, f"{tieu}: Path.exists bi goi {s.n_exists} lan")
            bang(s.n_stat == 1, f"{tieu}: stat count {s.n_stat}")
            bang(kq is mong, f"{tieu}: result {kq}, mong {mong}")
            bang(s.n_doc == n_doc, f"{tieu}: read count {s.n_doc}, mong {n_doc}")
            bang(s.n_kill == n_kill, f"{tieu}: kill count {s.n_kill}, mong {n_kill}")
    # Tiến trình sống, không lỗi: tệp có ⇒ đọc một lần, không kill.
    sen = RuntimeError("sentinel r743 exists song")
    with _CsSeam([me], exists=sen, kill_dem=True) as s:
        kq = goi("song", s, sen)
        bang(s.n_exists == 0 and s.n_stat == 1 and s.n_doc == 1 and s.n_kill == 0 and kq is True,
             f"song: result {kq} exists={s.n_exists} stat={s.n_stat} doc={s.n_doc} kill={s.n_kill}")
    # Zombie THẬT + stat EACCES ⇒ đã chết (nhãn B3-zombie dùng chung với t156).
    _cs_chay_t156(m, chay=("B3-zombie",))


# ---------------------------------------------------------------------------------------------
# B8 — ca khoá lớp `sua-124-trong-packet` (MÃ TEST THUẦN của đặc tả r12; executor tự dẫn xuất lại,
# tự đo). Bất biến: "124 ⇔ cả cây ĐÃ CHẾT" và "stop rc=0 ⇔ cây đã sạch" không phụ thuộc cách giải
# mã `comm`. Kích hoạt THẬT: kernel cắt `comm` ở 15 byte, nên tên tiếng Việt thành UTF-8 hỏng.
# ---------------------------------------------------------------------------------------------
_K124_COMM = bytes.fromhex("6b69e1bb836d5f7472615f7469e1ba")   # 'kiểm_tra_tiến_trình'.encode()[:15]
# Cháu của t160/t161 (r11): comm có `) ` (tên thật kiểu `tep (1).sh`) + đuôi UTF-8 hỏng — phủ trục S ở ba hàm ngoài:
# phép tách theo `)` ĐẦU (index/partition/split) lệch trường ở _khoa_danh_tinh, _thanh_vien_nhom, _chup_cay.
_K124_COMM_CHAU = b"tep (1) " + _K124_COMM[8:]                 # 15 byte: 'tep (1) ra_ti' + e1 ba
_NL = chr(10)

# Dạng đọc /proc/<pid>/stat theo Q-A.7 mà ứng viên KHAI (một chỗ, helper t156/t157 và B8 dùng chung):
# (tên phương thức Path, args, kwargs) — ví dụ ("read_bytes", (), {}) nếu chọn đọc bytes.
DANG_DOC_QA7 = ("read_text", (), {"encoding": "latin-1"})


def _k124_song(pid: int) -> bool:
    """Sống THẬT theo /proc đọc BYTES — không giải mã `comm`; zombie = đã chết."""
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            nd = f.read()
    except (FileNotFoundError, ProcessLookupError):
        return False
    return nd[nd.rindex(b")") + 2:].split()[0] != b"Z"


def _k124_locale_giai_ma_duoc() -> bool:
    """`read_text()` không đối số giải mã theo mã hoá này; giải mã được 15 byte hỏng thì lỗi 124 KHÔNG tái hiện được."""
    import locale
    try:
        _K124_COMM.decode(locale.getpreferredencoding(False))
    except (UnicodeDecodeError, LookupError):
        return False
    return True


def _k124_don_con(tn):
    """Dọn con B8 bằng PID do CHÍNH con ghi (không tin PID launcher-đang-thử báo), chỉ khi cmdline mang đường nhịp."""
    tp = Path(str(tn) + ".pid")
    _k124_cho_tep(tp, 2.0)
    try:
        pid = int(tp.read_text())
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            cua_ta = str(tn).encode() in f.read()
    except (OSError, ValueError):
        return
    if cua_ta:
        with contextlib.suppress(OSError):
            os.kill(pid, signal.SIGKILL)


_K124_MO = {"cai": False, "bat": False, "trong": 0, "ngoai": []}


def _k124_audit(ev, args):
    """Cửa sổ B8: mọi sự kiện audit `open` trên `/proc/…`, trên đường tương đối (`dir_fd`) hay trên fd số phải nằm
    TRONG một lời đọc Path đã ghi — danh sách cho phép ở tầng API (`open()`, `Path.open()`, `os.open`, đường
    `/proc/<pid>/task/…`, và ống PIPE mà `subprocess` bọc bằng `io.open` trên fd số, đều là `open` NGOÀI). Thước đo
    này KHÔNG thấy đường tuyệt đối ngoài `/proc` (`//proc/…`, tệp tạm) hay ống `os.pipe` đọc bằng `os.read` (đo) —
    phần ấy do chốt tĩnh và seam đếm đọc giữ. Đường tuyệt đối ngoài `/proc` không tính vì máy nạp module mở `.pyc`
    của codec một cách lười, ngay trong cửa sổ (đo)."""
    if _K124_MO["bat"] and ev == "open" and not _K124_MO["trong"]:
        p = args[0] if isinstance(args[0], int) else os.fsdecode(args[0])
        if isinstance(p, int) or not p.startswith("/") or p.startswith("/proc/"):
            _K124_MO["ngoai"].append(p)


@contextlib.contextmanager
def _k124_ghi_doc():
    """Ghi (phương thức, args, kwargs) của MỌI lời đọc Path trên /proc/<số>/stat trong cửa sổ, và ghi mọi sự kiện
    audit `open` xảy ra NGOÀI các lời đọc ấy: lời đọc Path đã ghi là đường mở tệp DUY NHẤT được phép."""
    if not _K124_MO["cai"]:
        sys.addaudithook(_k124_audit)          # không gỡ được; ngoài cửa sổ hook không làm gì
        _K124_MO["cai"] = True
    ghi = []
    goc = {t: (t in Path.__dict__, getattr(Path, t)) for t in ("read_text", "read_bytes")}

    def boc(ten, g):
        def f(self, *a, **k):
            p = str(self)
            if not (p.startswith("/proc/") and p.endswith("/stat") and p[6:-5].isdigit()):
                return g(self, *a, **k)
            ghi.append((ten, a, k))
            _K124_MO["trong"] += 1
            try:
                return g(self, *a, **k)
            finally:
                _K124_MO["trong"] -= 1
        return f
    for t, (_co, g) in goc.items():
        setattr(Path, t, boc(t, g))
    _K124_MO.update(bat=True, trong=0, ngoai=[])
    try:
        yield ghi
    finally:
        _K124_MO["bat"] = False
        for t, (co, g) in goc.items():
            if co:
                setattr(Path, t, g)
            else:
                delattr(Path, t)


def _k124_ma_con(tep_comm, tep_nhip, cho: float, doi_comm: bool) -> str:
    """Con: ghi PID của chính nó, (tuỳ chọn) chờ `cho` giây rồi đổi comm thành 15 byte hỏng, ghi comm THẬT
    (bytes) ra tệp, rồi ghi nhịp mỗi 0,1 s — tối đa 1200 nhịp (khoảng 120 s) rồi tự thoát: hạn sống. Mọi lối
    thoát KHÔNG do tín hiệu ghi `<tệp nhịp>.tu_thoat` (`han_song` / `ngoai_le`) — ca không phải cha của con."""
    dong = ["import ctypes, os, time",
            f"open({str(tep_nhip) + '.pid'!r}, 'w').write(str(os.getpid()))",
            "ly_do = 'ngoai_le'",
            "try:",
            f"    time.sleep({cho})"]
    if doi_comm:
        dong.append(f"    ctypes.CDLL(None).prctl(15, bytes.fromhex({_K124_COMM.hex()!r}), 0, 0, 0)")
    dong += ["    nd = open('/proc/%d/stat' % os.getpid(), 'rb').read()",
             f"    open({str(tep_comm)!r}, 'wb').write(nd[nd.index(b'(') + 1:nd.rindex(b')')])",
             f"    f = open({str(tep_nhip)!r}, 'a')",
             "    for _ in range(1200):",
             "        f.write('.'); f.flush(); time.sleep(0.1)",
             "    ly_do = 'han_song'",
             "finally:",
             f"    open({str(tep_nhip) + '.tu_thoat'!r}, 'w').write(ly_do)"]
    return _NL.join(dong) + _NL


def _k124_tu_thoat(tep):
    """Dấu TỰ THOÁT mà chính tiến trình ghi ở `finally`: `han_song`, `ngoai_le`; None = không tự thoát (tín hiệu
    giết nó, hay nó còn sống). Tín hiệu mặc định giết tiến trình KHÔNG chạy `finally`, nên dấu phân biệt được hai
    đường mà "đã chết" gộp làm một."""
    try:
        return Path(str(tep) + ".tu_thoat").read_text()
    except FileNotFoundError:
        return None


def _k124_tu_thoat_vo_can(ten, tu):
    if tu not in (None, "han_song"):
        raise RuntimeError(f"dieu kien dung: {ten} tien trinh do ca sinh chet vi {tu} - khong bi giet, khong het han")


def _k124_cho_tep(p, han=10.0):
    het = time.time() + han
    while time.time() < het:
        if p.exists() and p.stat().st_size:
            return True
        time.sleep(0.05)
    return False


def _k124_run(s, lenh):
    """`launcher.py run --deadline-utc` thật (hạn 3 s); trả (rc, sổ run.json dạng --json)."""
    repo = tao_repo(s)
    r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"), "--json",
             "--deadline-utc", mai_sau(3), "--", *lenh)
    so = {}
    dong = [d for d in r.stdout.splitlines() if d.startswith("{")]
    if dong:
        so = json.loads(dong[-1])
    if not so.get("pid") or r.returncode not in (MA_QUA_HAN, 125, MA_DANH_TINH):
        raise RuntimeError(f"dieu kien dung: launcher khong ket thuc bang ma han chot 124/125/10 kem so JSON: "
                           f"rc={r.returncode}, stderr={r.stderr[-160:]!r}")
    return r.returncode, so


def _k124_ket_luan(ten, rc, pid, tn):
    """Hai assertion, đúng thứ tự: (1) 124 KHÔNG đi cùng cây còn sống; (2) quá hạn phải GIẾT — con TỰ THOÁT ở hạn
    sống là KHÔNG bị giết (ĐỎ); con chết vì ngoại lệ là lỗi điều kiện dựng (không phải TinHieuChotCa)."""
    n1 = tn.stat().st_size if tn.exists() else 0
    time.sleep(1.0)
    n2 = tn.stat().st_size if tn.exists() else 0
    tu = _k124_tu_thoat(tn)
    _k124_tu_thoat_vo_can(ten, tu)
    song = bool(pid) and _k124_song(pid)
    bang(not (rc == MA_QUA_HAN and (song or n2 != n1)),
         f"{ten} 124 noi doi: rc={rc}, con {pid} song={song}, nhip {n1}->{n2}")
    bang(rc == MA_QUA_HAN and not song and n2 == n1 and tu is None,
         f"{ten} qua han khong giet duoc: rc={rc}, con {pid} song={song}, nhip {n1}->{n2}, tu thoat={tu}")


def _k124_dang_doc(ten, ghi):
    """(3) `read args`: mọi lời đọc /proc/<pid>/stat trong cửa sổ đúng DANG_DOC_QA7, và không `open` nào ngoài chúng."""
    if not ghi:
        raise RuntimeError(f"dieu kien dung: {ten} khong co loi doc /proc/<pid>/stat nao")
    lech = sorted({repr(x) for x in ghi if x != DANG_DOC_QA7})
    if _K124_MO["ngoai"]:                      # mở tệp ngoài lời đọc Path đã ghi: danh sách cho phép đóng ở MỌI API
        lech.insert(0, f"open ngoai loi doc Path: {len(_K124_MO['ngoai'])} su kien, vd {_K124_MO['ngoai'][:2]}")
    bang(not lech, f"{ten} read args {lech[:3]}")


def _k124_khoa_that(pid: int) -> str:
    """Khoá theo ĐỊNH DẠNG NỀN `linux:<starttime>` (trường 22), đọc BYTES độc lập — neo định dạng khoá của Q-A.7."""
    bat, _K124_MO["bat"] = _K124_MO["bat"], False      # lời đọc của CHÍNH ca: không đếm vào `open` của cửa sổ
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            nd = f.read()
    finally:
        _K124_MO["bat"] = bat
    return "linux:" + nd[nd.rindex(b")") + 2:].split()[19].decode("ascii")


@ca
def t158_comm_hong_SAU_luc_sinh_qua_han_khong_duoc_124_khi_con_song():
    """`run --deadline-utc`: con đổi comm thành UTF-8 hỏng SAU khi launcher lấy khoá (nền 89fc4fa:
    rc=124, `giet_tron_ven=True`, con vẫn sống)."""
    if platform.system() != "Linux":
        return "bo qua: comm/prctl/proc chi co tren Linux"
    if _k124_locale_giai_ma_duoc():
        return "bo qua: locale hien hanh giai ma duoc 15 byte comm hong - loi 124 khong tai hien duoc o day"
    with San() as s:
        tc, tn = s / "comm.bin", s / "nhip.txt"
        try:
            rc, so = _k124_run(s, [PY, "-c", _k124_ma_con(tc, tn, 0.5, True)])
            pid = so.get("pid")
            if not (_k124_cho_tep(tc, 1) and tc.read_bytes() == _K124_COMM):
                raise RuntimeError("dieu kien dung: con chua doi comm thanh 15 byte hong")
            if not so.get("khoa_danh_tinh"):
                raise RuntimeError("dieu kien dung: comm hong TRUOC luc lay khoa (ca nay can SAU)")
            _k124_ket_luan("B8-sau-sinh", rc, pid, tn)
        finally:
            _k124_don_con(tn)


@ca
def t159_chuong_trinh_ten_tieng_Viet_qua_han_phai_giet_duoc():
    """Tên chương trình tiếng Việt ⇒ comm hỏng NGAY LÚC SINH (kernel cắt 15 byte), không cần prctl
    (nền 89fc4fa: `khoa=None`, rc=10, con vẫn sống)."""
    if platform.system() != "Linux":
        return "bo qua: comm/proc chi co tren Linux"
    if _k124_locale_giai_ma_duoc():
        return "bo qua: locale hien hanh giai ma duoc 15 byte comm hong - loi 124 khong tai hien duoc o day"
    with San() as s:
        ten = s / "kiểm_tra_tiến_trình"
        try:
            os.symlink(PY, ten)
        except (OSError, UnicodeEncodeError) as e:
            raise RuntimeError(f"dieu kien dung: khong tao duoc ten tieng Viet: {e}")
        tc, tn = s / "comm.bin", s / "nhip.txt"
        try:
            rc, so = _k124_run(s, [str(ten), "-c", _k124_ma_con(tc, tn, 0.0, False)])
            pid = so.get("pid")
            if not (_k124_cho_tep(tc, 1) and tc.read_bytes() == _K124_COMM):
                raise RuntimeError("dieu kien dung: comm luc sinh khong phai 15 byte hong")
            _k124_ket_luan("B8-luc-sinh", rc, pid, tn)
        finally:
            _k124_don_con(tn)


_K124_MA_CHAU = _NL.join([
    "import ctypes, os, signal, sys, time",
    "signal.signal(signal.SIGTERM, signal.SIG_IGN)",
    "ly_do = 'ngoai_le'",
    "try:",
    "    ctypes.CDLL(None).prctl(15, bytes.fromhex(sys.argv[2]), 0, 0, 0)",
    "    open(sys.argv[1], 'w').write(str(os.getpid()))",
    "    time.sleep(120)",
    "    ly_do = 'han_song'",
    "finally:",
    "    open(sys.argv[1] + '.tu_thoat', 'w').write(ly_do)"]) + _NL
_K124_MA_ME = _NL.join([
    "import subprocess, sys, time",
    "subprocess.Popen([sys.executable, '-c', sys.argv[5], sys.argv[2], sys.argv[3]],",
    "                 start_new_session=(sys.argv[1] == '1'))",
    "if sys.argv[4] == 'thoat':",
    "    sys.stdin.readline()",
    "    sys.exit(0)",
    "time.sleep(120)"]) + _NL


def _k124_me_chau(s, setsid: bool, me_thoat: bool):
    tp = s / "chau.pid"
    me = subprocess.Popen([PY, "-c", _K124_MA_ME, "1" if setsid else "0", str(tp), _K124_COMM_CHAU.hex(),
                           "thoat" if me_thoat else "o_lai", _K124_MA_CHAU],
                          start_new_session=True, stdin=subprocess.PIPE)
    chau = None
    try:
        if not _k124_cho_tep(tp):
            raise RuntimeError("dieu kien dung: chau chua ghi pid")
        chau = int(tp.read_text())
        with open(f"/proc/{chau}/stat", "rb") as f:
            nd = f.read()
        if nd[nd.index(b"(") + 1:nd.rindex(b")")] != _K124_COMM_CHAU:
            raise RuntimeError("dieu kien dung: comm cua chau chua doi")
    except BaseException:
        if chau:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
        with contextlib.suppress(OSError):
            me.kill()
        me.wait()
        raise
    return me, chau


@ca
def t160_giet_cay_chau_setsid_comm_hong_phot_lo_SIGTERM():
    """Cháu `setsid()` (killpg không với tới), comm hỏng, phớt lờ SIGTERM: chỉ ẢNH CHỤP + kiểm
    sống/khoá từng pid giết được nó. Phủ `_chup_cay`, `_con_song` nhánh tệp có, `_khoa_danh_tinh`."""
    if platform.system() != "Linux":
        return "bo qua: setsid/proc chi co tren Linux"
    m = _tai_launcher_thu()
    with San() as s:
        me, chau = _k124_me_chau(s, True, False)
        try:
            with _k124_ghi_doc() as ghi:
                khoa = _k124_khoa_that(me.pid)
                kg = m._giet_cay(me.pid, khoa)
            song = _k124_song(chau)
            me_rc = me.poll()   # mẹ là con TRỰC TIẾP của ca: None = còn sống; < 0 = tín hiệu giết; >= 0 = tự thoát
            tu = _k124_tu_thoat(s / "chau.pid")
            _k124_tu_thoat_vo_can("B8-setsid", tu)
            bang(not (kg.tron_ven and (song or me_rc is None)),
                 f"B8-setsid 124 noi doi: {kg.mo_ta}; chau {chau} song={song}, me rc={me_rc}")
            bang(kg.tron_ven and not song and tu is None and me_rc is not None and me_rc < 0,
                 f"B8-setsid khong giet duoc: tron_ven={kg.tron_ven}, chau song={song}, chau tu thoat={tu}, "
                 f"me rc={me_rc}, {kg.mo_ta}")
            _k124_dang_doc("B8-setsid", ghi)
        finally:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
            with contextlib.suppress(OSError):
                me.kill()
            me.wait()


@ca
def t161_giet_cay_me_da_thoat_chau_cung_nhom_comm_hong():
    """Mẹ đã thoát, cháu CÙNG NHÓM comm hỏng còn sống: `_khoa_danh_tinh(me)` = None là ĐÚNG (mẹ đã
    biến mất) và chỉ phép quét nhóm còn thấy cháu. Phủ `_thanh_vien_nhom` (và `_chup_cay` theo nhóm)."""
    if platform.system() != "Linux":
        return "bo qua: nhom tien trinh/proc chi co tren Linux"
    m = _tai_launcher_thu()
    with San() as s:
        me, chau = _k124_me_chau(s, False, True)
        try:
            with _k124_ghi_doc() as ghi:
                khoa = _k124_khoa_that(me.pid)
                me.stdin.write(b"x" + _NL.encode())
                me.stdin.close()
                me.wait(timeout=10)
                kg = m._giet_cay(me.pid, khoa)
            song = _k124_song(chau)
            tu = _k124_tu_thoat(s / "chau.pid")
            _k124_tu_thoat_vo_can("B8-me-thoat", tu)
            bang(not (kg.tron_ven and song), f"B8-me-thoat 124 noi doi: {kg.mo_ta}; chau {chau} song")
            bang(kg.tron_ven and not song and tu is None, f"B8-me-thoat khong giet duoc: tron_ven={kg.tron_ven}, "
                                                          f"chau song={song}, chau tu thoat={tu}, {kg.mo_ta}")
            _k124_dang_doc("B8-me-thoat", ghi)
        finally:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
            with contextlib.suppress(OSError):
                me.kill()
            me.wait()


# ------------------------------------------------------------- wp748 r27: effort + sandbox thực tế (spec r27)

def _r27_khung(loai, rid, effort=..., reasoning=...):
    r = {"id": rid, "object": "response", "model": "gpt-mau"}
    if reasoning is not ...:
        r["reasoning"] = reasoning
    elif effort is not ...:
        r["reasoning"] = {"effort": effort, "summary": None}
    ev = {"type": loai, "sequence_number": 0, "response": r}
    return f"2026-10-24T01:12:06.199773Z TRACE tungstenite::protocol: Received message {json.dumps(ev)}\n".encode()


@ca
def r927_effort_do_duoc_tu_khung_may_chu():
    m = _tai_launcher_thu()
    ban_ghi, _ = _r26_trang_thai(m, _r27_khung("response.created", "r1", "xhigh")
                                 + _r27_khung("response.completed", "r1", "xhigh")
                                 + _r27_khung("response.created", "r2", "low"))
    bang(ban_ghi.get("model_phuc_vu_trang_thai") == "DO_DUOC", f"model: {ban_ghi}")
    bang(ban_ghi.get("effort_phuc_vu") == ["xhigh", "low"] and ban_ghi.get("effort_phuc_vu_trang_thai") == "DO_DUOC"
         and "effort_phuc_vu_ly_do" not in ban_ghi, f"effort: {ban_ghi}")
    bang(all(set(x) == {"response_id", "model", "su_kien"} for x in ban_ghi["model_phuc_vu"]),
         f"effort ro vao muc model_phuc_vu: {ban_ghi['model_phuc_vu']}")


@ca
def r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC():
    m = _tai_launcher_thu()
    tot = _r27_khung("response.created", "r0", "xhigh")
    for ten, hong in [("thieu_reasoning", _r27_khung("response.completed", "r0")),
                      ("reasoning_chuoi", _r27_khung("response.completed", "r0", reasoning="xhigh")),
                      ("effort_so", _r27_khung("response.completed", "r0", 5)),
                      ("effort_rong", _r27_khung("response.completed", "r0", "  ")),
                      ("effort_null", _r27_khung("response.completed", "r0", None))]:
        ban_ghi, _ = _r26_trang_thai(m, tot + hong)
        bang(ban_ghi.get("model_phuc_vu_trang_thai") == "DO_DUOC", f"{ten}: khung van phai nhan cho model: {ban_ghi}")
        bang(ban_ghi.get("effort_phuc_vu_trang_thai") == "KHONG_DO_DUOC"
             and "1 khung" in ban_ghi.get("effort_phuc_vu_ly_do", "") and ban_ghi.get("effort_phuc_vu") == ["xhigh"],
             f"{ten}: {ban_ghi}")


@ca
def r927_effort_khong_do_duoc_khi_model_khong_do_duoc():
    m = _tai_launcher_thu()
    for ten, du in [("khong_khung", b"Reading additional input from stdin...\n"),
                    ("khung_mat", _r27_khung("response.created", "r1", "xhigh")
                     + b"2026-10-24T01:12:06Z TRACE tungstenite::protocol: Received message {\"type\":\"response.created\"\n")]:
        ban_ghi, _ = _r26_trang_thai(m, du)
        bang(ban_ghi.get("model_phuc_vu_trang_thai") == "KHONG_DO_DUOC", f"{ten}: fixture: {ban_ghi}")
        bang(ban_ghi.get("effort_phuc_vu_trang_thai") == "KHONG_DO_DUOC"
             and "model" in ban_ghi.get("effort_phuc_vu_ly_do", ""), f"{ten}: {ban_ghi}")


_R27_BWRAP = ["bwrap", "--as-pid-1", "--new-session", "--die-with-parent", "--ro-bind", "/", "/", "--dev", "/dev",
              "--bind", "/w", "/w", "--ro-bind-try", "/w/src/.git", "/w/src/.git", "--tmpfs", "/tmp/bi-mat-tmpfs",
              "--unshare-user", "--unshare-pid", "--unshare-net", "--proc", "/proc", "--cap-drop", "ALL",
              "--setenv", "TOKEN", "bi-mat-setenv", "--argv0", "codex-linux-sandbox", "--", "bash", "--unshare-ipc",
              "--bind", "/", "/w/src", "-c", "bi-mat-lenh"]
# chuỗi bí mật hợp lệ về TỪ VỰNG (chữ thường, không dấu cách) — R27-ALLOW-01: lọc theo cách viết thì chúng lọt
_R27_HO_SO = {"type": "managed", "network": "restricted", "file_system": {"type": "restricted", "entries": [
    {"path": {"type": "special", "value": {"kind": "root"}}, "access": "read"},
    {"path": {"type": "path", "path": "/w"}, "access": "write"},
    {"path": {"type": "path", "path": "/w/src/.git"}, "access": "read", "missing_path_behavior": "skip"},
    {"path": {"type": "path", "path": "/w/src/bimatlexical"}, "access": "bimataccess"},
    {"path": {"type": "path", "path": "/home/bi-mat-home"}, "access": "read"},
    {"path": {"type": "special", "value": {"kind": "bimatkind"}}, "access": "bi mat access"},
    "bi-mat-muc-khong-phai-object"]}}
_R27_CLS = ["/root/.codex/tmp/arg0-linux/x/codex-linux-sandbox", "--sandbox-policy-cwd", "/w", "--command-cwd",
            "/w/src/bimatcon", "--permission-profile", json.dumps(_R27_HO_SO), "--apply-seccomp-then-exec", "--", "sh",
            "--lenh-mo-hinh", "-c", "bi-mat-lenh"]


@ca
def r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep():
    m = _tai_launcher_thu()
    bw = m._tom_tat_sandbox(_R27_BWRAP, "/w/src")
    bang(bw == {"chuong_trinh": "bwrap",
                "gan": [["--ro-bind", "/"], ["--bind", "to_tien_workspace"], ["--ro-bind-try", "trong_workspace"]],
                "co": ["--cap-drop=ALL", "--die-with-parent", "--new-session", "--unshare-net", "--unshare-pid",
                       "--unshare-user"]}, f"bwrap: {bw}")
    cl = m._tom_tat_sandbox(_R27_CLS, "/w/src")
    bang(cl == {"chuong_trinh": "codex-linux-sandbox",
                "co": ["--apply-seccomp-then-exec", "--command-cwd=trong_workspace",
                       "--sandbox-policy-cwd=to_tien_workspace"],
                "permission_profile": {"loai": "managed", "file_system": "restricted", "network": "restricted",
                                       "muc": [["root", "read"], ["to_tien_workspace", "write"],
                                               ["trong_workspace", "read"], ["trong_workspace", "khac"],
                                               ["khac", "read"], ["khac", "khac"], ["khac", "khac"]]}},
         f"codex-linux-sandbox: {cl}")
    ho_so_la = dict(_R27_HO_SO, type="bimattype", network="bimatnet",
                    file_system={"type": "bimatfs", "entries": []})
    la = m._tom_tat_sandbox(["codex-linux-sandbox", "--permission-profile", json.dumps(ho_so_la), "--", "x"], "/w")
    tho = json.dumps([bw, cl, la])
    bang(not any(k in tho.lower() for k in ("bimat", "bi-mat", "bi mat")) and "/w" not in tho,
         f"ro chuoi ngoai tap co dinh: {tho}")
    bang(m._tom_tat_sandbox(["python3", "bwrap", "--unshare-net"], "/w") is None
         and m._tom_tat_sandbox([], "/w") is None, "khong phai sandbox ma van tom tat")
    hong = m._tom_tat_sandbox(["codex-linux-sandbox", "--permission-profile", "{khong-json", "--", "x"], "/w")
    bang(hong["permission_profile"] == {"loai": "khac"}, f"ho so hong: {hong}")
    try:
        mang = m._tom_tat_sandbox(["codex-linux-sandbox", "--permission-profile", "[1]", "--", "x"], "/w")
    except Exception as e:
        mang = {"permission_profile": f"nem {type(e).__name__}"}
    bang(mang["permission_profile"] == {"loai": "khac"}, f"ho so khong phai object: {mang}")
    bang(m._tom_tat_sandbox(["bwrap", "--cap-drop", "SYS_ADMIN", "--", "x"], "/w")["co"] == ["--cap-drop=khac"],
         "cap-drop la")


@ca
def r927_ngu_phap_sandbox_theo_bang_so_doi_so():
    # R27-PARSE-02: giá trị trông như cờ không được đọc thành cờ; `--` ở vị trí đối số là giá trị, không phải ranh
    # giới; cờ lạ / thiếu đối số / không có ranh giới lệnh ⇒ khong_ro, không suy cờ.
    m = _tai_launcher_thu()
    t = m._tom_tat_sandbox(["bwrap", "--setenv", "X", "--unshare-net", "--ro-bind", "/", "/", "--", "cmd"], "/w")
    bang(t == {"chuong_trinh": "bwrap", "gan": [["--ro-bind", "/"]], "co": []}, f"gia tri setenv thanh co: {t}")
    t = m._tom_tat_sandbox(["bwrap", "--setenv", "A", "--", "--unshare-net", "--", "cmd"], "/w")
    bang(t == {"chuong_trinh": "bwrap", "gan": [], "co": ["--unshare-net"]}, f"-- la gia tri thanh ranh gioi: {t}")
    t = m._tom_tat_sandbox(["bwrap", "--unshare-pid", "cmd", "--unshare-net"], "/w")
    bang(t == {"chuong_trinh": "bwrap", "gan": [], "co": ["--unshare-pid"]}, f"doc qua ranh gioi lenh: {t}")
    for ten, argv in [("co_la", ["bwrap", "--bogus", "--unshare-net", "--", "x"]),
                      ("thieu_ranh_gioi", ["bwrap", "--unshare-net"]),
                      ("thieu_doi_so", ["bwrap", "--ro-bind", "/"]),
                      ("cls_co_la", ["codex-linux-sandbox", "--la", "v", "--", "x"]),
                      ("cls_thieu_doi_so", ["codex-linux-sandbox", "--command-cwd"])]:
        t = m._tom_tat_sandbox(argv, "/w")
        bang(t == {"chuong_trinh": argv[0], "khong_ro": True}, f"{ten}: {t}")


def _r27_so(m, lay, stdout: str):
    with San() as s:
        p = s / "stdout.log"
        p.write_text(stdout, encoding="utf-8")
        ban_ghi = {}
        lay.ghi_so(ban_ghi, p)
        return ban_ghi


@ca
def r927_trang_thai_sandbox_moi_nhanh():
    m = _tai_launcher_thu()
    lenh = json.dumps({"type": "item.completed", "item": {"id": "item_1", "type": "command_execution"}}) + "\n"
    bat = json.dumps({"type": "thread.started"}) + "\n"

    def moi(nen_linux=True):
        # R27-TEST-05: khả năng Linux do FIXTURE quyết, không do nền đang chạy test
        lay = m._LayMauSandbox(os.getpid(), "/w")
        lay.luong = threading.Thread(target=lambda: None) if nen_linux else None
        return lay
    lay = moi()
    lay.thay['{"chuong_trinh": "bwrap"}'] = 2
    d = _r27_so(m, lay, "khong json\n")
    bang(d["sandbox_trang_thai"] == "DO_DUOC" and d["sandbox_quan_sat"] == [{"chuong_trinh": "bwrap", "so_lan": 2}]
         and "sandbox_ly_do" not in d and d.get("sandbox_gioi_han"), f"do_duoc: {d}")
    tin = json.dumps({"type": "item.completed", "item": {"id": "item_0", "type": "agent_message"}}) + "\n"
    d = _r27_so(m, moi(), bat + tin)
    bang(d["sandbox_trang_thai"] == "KHONG_THAY_LENH" and d["sandbox_quan_sat"] == [], f"khong lenh: {d}")
    for ten, lay, out, mau in [("co_lenh_khong_thay", moi(), bat + lenh, "1 command_execution"),
                               ("stdout_khong_json", moi(), "Reading...\n", "--json"),
                               ("khong_linux", moi(False), bat, "chi Linux")]:
        d = _r27_so(m, lay, out)
        bang(d["sandbox_trang_thai"] == "KHONG_DO_DUOC" and mau in d.get("sandbox_ly_do", ""), f"{ten}: {d}")
    lay = moi()
    lay.thay['{"chuong_trinh": "bwrap"}'] = 1
    lay.loi.append("PermissionError")
    d = _r27_so(m, lay, bat)
    bang(d["sandbox_trang_thai"] == "KHONG_DO_DUOC" and "PermissionError" in d["sandbox_ly_do"], f"loi: {d}")
    lay = moi()
    lay.thay['{"chuong_trinh": "bwrap"}'] = 1
    lay.con_chay = True
    d = _r27_so(m, lay, bat)
    bang(d["sandbox_trang_thai"] == "KHONG_DO_DUOC" and "chua dung" in d["sandbox_ly_do"], f"con chay: {d}")
    lay = moi()
    lay.thay['{"chuong_trinh": "bwrap"}'] = 1
    lay.thay['{"chuong_trinh": "bwrap", "khong_ro": true}'] = 1
    d = _r27_so(m, lay, bat)
    bang(d["sandbox_trang_thai"] == "KHONG_DO_DUOC" and "phan tich" in d["sandbox_ly_do"], f"khong_ro: {d}")
    goc = m.platform.system
    m.platform.system = lambda: "Windows"
    try:
        lay = m._LayMauSandbox(os.getpid(), "/w")
        lay.bat_dau()
        lay.ket_thuc(1)
    finally:
        m.platform.system = goc
    d = _r27_so(m, lay, bat)
    bang(lay.luong is None and d["sandbox_trang_thai"] == "KHONG_DO_DUOC" and "chi Linux" in d["sandbox_ly_do"],
         f"ngoai Linux: {d}")


@ca
def r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ():
    if platform.system() != "Linux":
        return "can /proc cua Linux"
    m = _tai_launcher_thu()
    doc = []
    goc = m.Path

    class PathGhi(type(Path())):
        def read_bytes(self):
            doc.append(str(self))
            return super().read_bytes()
    # con: chạy với argv của python, 0,6s sau mới exec thành argv0 `bwrap` (giống fork-rồi-exec)
    ma = ("import os,sys,time;time.sleep(0.6);"
          "os.execv(sys.executable,['bwrap','-c','import time;time.sleep(1.5)'])")
    p = subprocess.Popen([PY, "-c", ma])
    m.Path = PathGhi
    try:
        lay = m._LayMauSandbox(os.getpid(), "/w")     # gốc = tiến trình test: `p` là hậu duệ của nó
        lay.bat_dau()
        p.wait(timeout=20)
        lay.ket_thuc(5)
    finally:
        m.Path = goc
    d = {}
    lay.ghi_so(d, Path(os.devnull))
    bang(d["sandbox_trang_thai"] == "DO_DUOC"
         and {"chuong_trinh": "bwrap", "gan": [], "co": [], "so_lan": 1}
         in d["sandbox_quan_sat"], f"khong thay tien trinh sau exec: {d}")
    bang(doc and not any("environ" in x for x in doc)
         and all(x.endswith(("/stat", "/cmdline")) for x in doc), f"doc tep ngoai stat/cmdline: {sorted(set(doc))[:5]}")


def _r27_sua_stat(b: bytes, trang_thai=None, ppid=None, bd=None) -> bytes:
    k = b.rindex(b")") + 2
    f = b[k:].split()
    for vi_tri, gt in ((0, trang_thai), (1, ppid), (19, bd)):
        if gt is not None:
            f[vi_tri] = gt
    return b[:k] + b" ".join(f) + b"\n"


def _r27_cay_cha_chau():
    """(cha, pid cháu): cha là con trực tiếp của tiến trình test, cháu là con của cha."""
    cha = subprocess.Popen([PY, "-c", "import subprocess,sys,time;"
                            "subprocess.Popen([sys.executable,'-c','import time;time.sleep(6)']);time.sleep(6)"])
    han = time.monotonic() + 10
    while time.monotonic() < han:
        for d in os.listdir("/proc"):
            if d.isdigit():
                with contextlib.suppress(OSError, IndexError):
                    b = Path(f"/proc/{d}/stat").read_bytes()
                    if int(b[b.rindex(b")") + 2:].split()[1]) == cha.pid:
                        return cha, int(d)
        time.sleep(0.05)
    cha.kill()
    cha.wait()
    raise TinHieuChotCa("fixture: khong thay tien trinh chau")


@ca
def r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot():
    # R27-PROC-03 + R27-PID-04, đi qua `_quet`/`_chay` THẬT: quyền bị từ chối không phải "tiến trình đã thoát"; danh
    # tính con đổi giữa stat và cmdline, hay pid gốc bị tái dùng, thì không đo được — kể cả khi đã có quan sát trước.
    if platform.system() != "Linux":
        return "can /proc cua Linux"
    m = _tai_launcher_thu()
    goc = m.Path
    con, chau = _r27_cay_cha_chau()
    try:
        for ten, mong in [("quyen", "PermissionError"), ("danh_tinh_con", "DanhTinhDoi"),
                          ("goc_tai_dung", "RuntimeError"), ("to_tien_doi", "DanhTinhDoi"), ("cha_zombie", "DanhTinhDoi"), ("to_tien_doi_cha", "DanhTinhDoi"),
                          ("goc_khong_ghim", "GocKhongGhimDuoc")]:
            vet = {"cmd": False, "goc": 0}

            class PathGia(type(Path())):
                def read_bytes(self):
                    x = str(self)
                    if ten == "quyen" and x == f"/proc/{con.pid}/cmdline":
                        raise PermissionError(13, "tu choi")
                    if ten == "goc_khong_ghim" and x == f"/proc/{os.getpid()}/stat" and not vet["goc"]:
                        vet["goc"] = 1           # R27-PID-04d: lần ghim lúc khởi tạo không thấy gốc
                        raise FileNotFoundError(2, "chua thay")
                    b = super().read_bytes()
                    if ten == "danh_tinh_con" and x == f"/proc/{con.pid}/cmdline":
                        vet["cmd"] = True
                    elif ten == "danh_tinh_con" and x == f"/proc/{con.pid}/stat" and vet["cmd"]:
                        vet["cmd"] = False       # MỘT lần, đúng lần đọc lại liền sau cmdline: chốt chuỗi tổ tiên
                        return _r27_sua_stat(b, bd=b"1")    # của cháu không được thay chốt đọc-lại-stat của chính con
                    elif ten == "goc_tai_dung" and x == f"/proc/{os.getpid()}/stat":
                        vet["goc"] += 1          # lần 1 = ghim lúc khởi tạo; đổi ngay từ lần đọc trong lượt quét đầu
                        if vet["goc"] > 1:
                            return _r27_sua_stat(b, bd=b"1")
                    elif ten in ("to_tien_doi", "cha_zombie", "to_tien_doi_cha") and x == f"/proc/{chau}/cmdline":
                        vet["cmd"] = True
                    elif ten == "to_tien_doi_cha" and vet["cmd"] and x == f"/proc/{con.pid}/stat":
                        return _r27_sua_stat(b, ppid=b"1")      # R27-PID-04e: tổ tiên chỉ đổi CẠNH cha, starttime giữ
                    elif ten == "cha_zombie" and vet["cmd"] and x == f"/proc/{chau}/stat":
                        return _r27_sua_stat(b, ppid=b"1")      # vòng đời BÌNH THƯỜNG: cha thành zombie, cháu bị
                    elif ten == "cha_zombie" and vet["cmd"] and x == f"/proc/{con.pid}/stat":
                        return _r27_sua_stat(b, trang_thai=b"Z")  # chuyển cha — thu hẹp: vẫn KHONG_DO_DUOC (R27-PID-04c)
                    elif ten == "to_tien_doi" and x == f"/proc/{con.pid}/stat" and vet["cmd"]:
                        return _r27_sua_stat(b, bd=b"1")    # cha trung gian đổi danh tính SAU khi đã đọc argv của cháu
                    return b
            m.Path = PathGia
            try:
                lay = m._LayMauSandbox(os.getpid(), "/w")
                lay.thay['{"chuong_trinh": "bwrap"}'] = 1
                lay.dung.set()
                lay._chay()              # MỘT lượt quét: lỗi phải lộ ngay trong chính lượt ấy
            finally:
                m.Path = goc
            d = {}
            lay.ghi_so(d, Path(os.devnull))
            bang(mong in lay.loi and d["sandbox_trang_thai"] == "KHONG_DO_DUOC", f"{ten}: loi={lay.loi} {d}")
            bang(ten != "goc_khong_ghim" or lay.goc_bd is None, f"goc_khong_ghim: da ghim muon {lay.goc_bd}")
    finally:
        con.kill()
        con.wait()


@ca
def r927_canh_cha_doi_giua_hai_luot_quet():
    # R27-PID-04f: MỘT sampler qua hai lượt quét; lượt 2 cháu (còn sống, starttime giữ) đổi ppid ra ngoài cây hoặc vào
    # gốc ⇒ DanhTinhDoi. Đối chứng: lượt 2 sạch thì không lỗi.
    if platform.system() != "Linux":
        return "can /proc cua Linux"
    m = _tai_launcher_thu()
    goc = m.Path
    cha, chau = _r27_cay_cha_chau()
    try:
        g, cs = f"/proc/{os.getpid()}/stat", f"/proc/{chau}/stat"            # R27-PID-04g: gốc vắng ở lượt 2
        for ten, ppid_moi, mat in [("ra_ngoai", b"1", ()), ("vao_goc", str(os.getpid()).encode(), ()), ("doi_chung", None, ()),
                                   ("goc_mat_chau_doi", b"1", (g,)), ("goc_mat_chau_mat", None, (g, cs))]:
            vet = {"luot": 0}

            class PathGia(type(Path())):
                def read_bytes(self):
                    if vet["luot"] == 2 and str(self) in mat:
                        raise FileNotFoundError(2, "da thoat")
                    b = super().read_bytes()
                    if ppid_moi and vet["luot"] == 2 and str(self) == f"/proc/{chau}/stat":
                        return _r27_sua_stat(b, ppid=ppid_moi)
                    return b
            m.Path = PathGia
            try:
                lay = m._LayMauSandbox(os.getpid(), "/w")
                lay.dung.set()
                for vet["luot"] in (1, 2):
                    lay._chay()
            finally:
                m.Path = goc
            bang(lay.loi == (["DanhTinhDoi"] if ppid_moi else []) and (chau in lay.canh) == (len(mat) < 2), ten)
    finally:
        cha.kill()
        cha.wait()


@ca
def r927_cmdline_tho_giu_doi_so_rong_qua_bo_giai_ma_that():
    # R27-PARSE-02b: đi từ BYTE cmdline thô qua đúng bộ giải mã `_quet` dùng, tới trạng thái trong sổ.
    m = _tai_launcher_thu()
    tho = b"bwrap\0--setenv\0X\0\0--unshare-net\0--\0cmd\0"
    bang(m._tach_cmdline(tho) == ["bwrap", "--setenv", "X", "", "--unshare-net", "--", "cmd"],
         f"doi so rong bi bo: {m._tach_cmdline(tho)}")
    bang(m._tom_tat_cmdline(tho, "/w") == {"chuong_trinh": "bwrap", "gan": [], "co": ["--unshare-net"]},
         f"tom tat sau giai ma: {m._tom_tat_cmdline(tho, '/w')}")
    for ten, x in [("khong_nul_cuoi", b"bwrap --unshare-net -- x"), ("cat_giua", b"/usr/bin/codex-linux-sandbox\0--x")]:
        t = m._tom_tat_cmdline(x, "/w")
        bang(t is not None and t.get("khong_ro") is True and set(t) == {"chuong_trinh", "khong_ro"}, f"{ten}: {t}")
    bang(m._tom_tat_cmdline(b"", "/w") is None and m._tom_tat_cmdline(b"sleep 5", "/w") is None, "khong phai sandbox")
    if platform.system() != "Linux":
        return "phan _quet can /proc cua Linux"
    goc = m.Path
    con = subprocess.Popen([PY, "-c", "import time;time.sleep(5)"])

    class PathGia(type(Path())):
        def read_bytes(self):
            return tho if str(self) == f"/proc/{con.pid}/cmdline" else super().read_bytes()
    m.Path = PathGia
    try:
        lay = m._LayMauSandbox(os.getpid(), "/w")
        lay.dung.set()
        lay._chay()
    finally:
        m.Path = goc
        con.kill()
        con.wait()
    d = {}
    lay.ghi_so(d, Path(os.devnull))
    bang(d["sandbox_trang_thai"] == "DO_DUOC"
         and {"chuong_trinh": "bwrap", "gan": [], "co": ["--unshare-net"], "so_lan": 1} in d["sandbox_quan_sat"],
         f"so tu cmdline tho: {d}")


_R27_TU_VUNG = {"bwrap", "codex-linux-sandbox", "/", "/tmp", "/dev", "/proc", "workspace", "trong_workspace",
                "to_tien_workspace", "khac", "managed", "disabled", "external", "restricted", "unrestricted", "read",
                "write", "none", "enabled", "root", "slash_tmp", "tmpdir", "minimal", "current_working_directory",
                "chuong_trinh", "gan", "co", "permission_profile", "loai", "file_system", "muc", "network", "so_lan",
                "khong_ro", "--ro-bind", "--bind", "--ro-bind-try", "--bind-try", "--dev-bind", "--dev-bind-try",
                "--unshare-user", "--unshare-ipc", "--unshare-pid", "--unshare-net", "--unshare-all", "--share-net",
                "--new-session", "--die-with-parent", "--cap-drop=ALL", "--cap-drop=khac", "--apply-seccomp-then-exec"}


def _r27_moi_chuoi(x):
    if isinstance(x, dict):
        return [c for k, v in x.items() for c in [k, *_r27_moi_chuoi(v)]]
    if isinstance(x, list):
        return [c for v in x for c in _r27_moi_chuoi(v)]
    return [x] if isinstance(x, str) else []


@ca
def r927_lenh_run_ghi_effort_va_sandbox_vao_run_json():
    with San() as s:
        err = _r27_khung("response.created", "r1", "xhigh").decode()
        sau = ("import subprocess;subprocess.run([sys.executable,'-c','import os,sys;"
               "os.execv(sys.executable,[\\'bwrap\\',\\'-c\\',\\'import time;time.sleep(1)\\',\\'--unshare-net\\'])'])")
        r, tm, so = _r25_chay(s, err, sau)
        bang(r.returncode == 0 and so.get("effort_phuc_vu") == ["xhigh"]
             and so.get("effort_phuc_vu_trang_thai") == "DO_DUOC", f"effort: {r.stderr[-300:]} {so}")
        if platform.system() == "Linux":
            bang(so.get("sandbox_trang_thai") == "DO_DUOC"
                 and any(x.get("chuong_trinh") == "bwrap" for x in so.get("sandbox_quan_sat", [])), f"sandbox: {so}")
            la = [x for x in _r27_moi_chuoi(so.get("sandbox_quan_sat")) if x not in _R27_TU_VUNG and not re.fullmatch(
                r"--(sandbox-policy-cwd|command-cwd)=(workspace|trong_workspace|to_tien_workspace|khac|/|/tmp|/dev|/proc)",
                x)]
            bang(not la, f"run.json co chuoi ngoai tu vung co dinh: {la[:5]}")
        else:
            bang(so.get("sandbox_trang_thai") == "KHONG_DO_DUOC", f"sandbox ngoai Linux: {so}")
            # r28: trên nền này sampler không có luồng nên bỏ `bat_dau()` không đổi kết quả — đột biến phụ thuộc
            # /proc phải thành KHÔNG ĐO ĐƯỢC chứ không phải "sống" (đo: launcher-windows run 40437650224 trên 0615234).
            return "phan sandbox can /proc cua Linux (effort va KHONG_DO_DUOC ngoai Linux da do o tren)"


DOT_BIEN = [
    ("r952_bo_ep_kieu_truong_credential",
     ('           for k in _TRUONG_TOKEN_CHUOI):',
      '           for k in ()):'),
     ["r952_auth_json_truong_la_kieu_object_van_doc_duoc"]),
    ("r952_quay_ve_ep_moi_truong_la_chuoi",
     ('_TRUONG_TOKEN_CHUOI = ("id_token", "access_token", "refresh_token", "account_id")',
      '_TRUONG_TOKEN_CHUOI = ("id_token", "access_token", "refresh_token", "account_id", "oauth_provenance")'),
     ["r952_auth_json_truong_la_kieu_object_van_doc_duoc"]),
    # wp748 r27: mỗi chốt đo effort/sandbox một đột biến gỡ đúng chốt của nó.
    ("r27_canh_sau_return_goc_vang", ('                    info[int(d)] = st\n', '                    info[int(d)] = st\n        if self.pid not in info:\n            return\n'),
     ["r927_canh_cha_doi_giua_hai_luot_quet"]),
    ("r27_canh_khong_doi_chieu", ('            elif hien != bo:\n', '            elif False:\n'), ["r927_canh_cha_doi_giua_hai_luot_quet"]),
    ("r27_canh_khong_ghi", ('                self.canh[c] = sau\n', ''), ["r927_canh_cha_doi_giua_hai_luot_quet"]),
    ("r27_to_tien_chi_so_bd", ('any(self._stat(p) != bo for p, bo in chuoi)', 'any((self._stat(p) or (0, 0))[1] != bo[1] for p, bo in chuoi)'),
     ["r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot"]),
    ("r27_goc_ghim_tre", ('        if goc is None or self.goc_bd is None:\n            return',
                          '        if goc is not None and self.goc_bd is None:\n            self.goc_bd = goc[1]\n        if goc is None:\n            return'),
     ["r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot"]),
    ("r27_cmdline_bo_doi_so_rong", ('return [x.decode("utf-8", "replace") for x in tho[:-1].split(b"\\0")]',
                                    'return [x.decode("utf-8", "replace") for x in tho[:-1].split(b"\\0") if x]'), ["r927_cmdline_tho_giu_doi_so_rong_qua_bo_giai_ma_that"]),
    ("r27_cmdline_khong_nul_van_tin", ('    if not tho.endswith(b"\\0"):\n        return None\n', ''), ["r927_cmdline_tho_giu_doi_so_rong_qua_bo_giai_ma_that"]),
    ("r27_khong_xac_thuc_to_tien", (' or any(self._stat(p) != bo for p, bo in chuoi)', ''),
     ["r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot"]),
    ("r27_goc_ghim_muon", ('            else:\n                self.goc_bd = goc[1]\n', '            else:\n                pass\n'), ["r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot"]),
    ("r27_trong_ws_chep_ten", ('        return "trong_workspace"\n', '        return "workspace/" + p[len(ws) + 1:]\n'), ["r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep"]),
    ("r27_gia_tri_khong_loc", ('return x if x in _HO_SO_GIA_TRI[loai] else "khac"', 'return x if isinstance(x, str) else "khac"'),
     ["r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep"]),
    ("r27_cap_drop_khong_loc", ('("ALL" if gt[0] == "ALL" else "khac")', 'gt[0]'), ["r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep"]),
    ("r27_ranh_gioi_khong_nhan_hai_gach", ('        if x == "--" or not x.startswith("--"):\n', '        if not x.startswith("--"):\n'),
     ["r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep"]),
    ("r27_arity_bo_qua", ('        ra.append((x, a[i + 1:i + 1 + n]))\n        i += 1 + n\n',
                          '        ra.append((x, a[i + 1:i + 1 + n]))\n        i += 1\n'), ["r927_ngu_phap_sandbox_theo_bang_so_doi_so"]),
    ("r27_co_la_doan_khong_doi_so", ('        n = arity.get(x)\n', '        n = arity.get(x, 0)\n'),
     ["r927_ngu_phap_sandbox_theo_bang_so_doi_so"]),
    ("r27_khong_ranh_gioi_van_nhan", ('        i += 1 + n\n    return None\n', '        i += 1 + n\n    return ra\n'), ["r927_ngu_phap_sandbox_theo_bang_so_doi_so"]),
    ("r27_khong_ro_van_do_duoc", ('        elif any(json.loads(k).get("khong_ro") for k in thay):\n', '        elif False:\n'), ["r927_trang_thai_sandbox_moi_nhanh"]),
    ("r27_cmdline_nuot_moi_loi", ('                except (FileNotFoundError, ProcessLookupError):\n                    continue',
                                  '                except OSError:\n                    continue'), ["r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot"]),
    ("r27_khong_doc_lai_stat", ('if sau != (cha, bd) or any(', 'if any('), ["r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot"]),
    ("r27_goc_khong_ghim", ('        if goc[1] != self.goc_bd:\n', '        if False:\n'), ["r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot"]),
    ("r27_effort_khong_kiem_kieu", ('eff = eff if isinstance(eff, str) and eff.strip() else None', 'eff = eff'),
     ["r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC"]),
    ("r27_effort_khong_kiem_rong", ('eff = eff if isinstance(eff, str) and eff.strip() else None',
                                    'eff = eff if isinstance(eff, str) else None'),
     ["r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC"]),
    ("r27_reasoning_khong_kiem_dict", ('eff = ly.get("effort") if isinstance(ly, dict) else None',
                                       'eff = ly.get("effort") if ly else None'),
     ["r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC"]),
    ("r27_bo_dem_effort", ('            _dem_effort(dem, m.pop("effort", None))\n', '            m.pop("effort", None)\n'),
     ["r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC"]),
    ("r27_effort_o_lai_muc_model", ('            _dem_effort(dem, m.pop("effort", None))\n',
                                    '            _dem_effort(dem, m.get("effort"))\n'),
     ["r927_effort_do_duoc_tu_khung_may_chu"]),
    ("r27_effort_chi_gia_tri_dau", ('elif eff not in dem.get("effort", ()):', 'elif not dem.get("effort"):'),
     ["r927_effort_do_duoc_tu_khung_may_chu"]),
    ("r27_effort_khong_xet_model", ('    if tt_model != "DO_DUOC":\n', '    if False:\n'),
     ["r927_effort_khong_do_duoc_khi_model_khong_do_duoc"]),
    ("r27_effort_khong_xet_thieu", ('    if dem.get("effort_thieu"):\n', '    if False:\n'),
     ["r927_effort_thieu_hoac_sai_kieu_o_mot_khung_thi_KHONG_DO_DUOC"]),
    ("r27_ten_khong_basename", ('ten = argv[0].replace("\\\\", "/").rsplit("/", 1)[-1]', 'ten = argv[0]'),
     ["r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep"]),
    ("r27_nhan_duong_tra_tho", ('        return "to_tien_workspace"\n    return "khac"\n', '        return "to_tien_workspace"\n    return p\n'),
     ["r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep"]),
    ("r27_ho_so_khong_loc_duong", ('nhan = _nhan_duong_sb(p.get("path"), ws)', 'nhan = p.get("path")'),
     ["r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep"]),
    ("r27_ho_so_khong_kiem_dict", ('    if type(d) is not dict:\n', '    if False:\n'),
     ["r927_tom_tat_sandbox_chi_giu_danh_sach_cho_phep"]),
    ("r27_tt_khong_xet_nen", ('        if self.luong is None:\n            tt, ld', '        if False:\n            tt, ld'),
     ["r927_trang_thai_sandbox_moi_nhanh"]),
    ("r27_tt_bo_qua_loi", ('        elif loi:\n            tt, ld = "KHONG_DO_DUOC", f"luong lay mau',
                           '        elif False:\n            tt, ld = "KHONG_DO_DUOC", f"luong lay mau'),
     ["r927_trang_thai_sandbox_moi_nhanh"]),
    ("r27_tt_bo_qua_con_chay", ('        elif self.con_chay:\n', '        elif False:\n'), ["r927_trang_thai_sandbox_moi_nhanh"]),
    ("r27_tt_khong_doi_json", ('            if not co_json:\n', '            if False:\n'), ["r927_trang_thai_sandbox_moi_nhanh"]),
    ("r27_tt_bo_qua_so_lenh", ('            elif so_lenh:\n', '            elif False:\n'), ["r927_trang_thai_sandbox_moi_nhanh"]),
    ("r27_dem_moi_item", ('if isinstance(it, dict) and it.get("type") == "command_execution":', 'if isinstance(it, dict):'),
     ["r927_trang_thai_sandbox_moi_nhanh"]),
    ("r27_khoa_khong_gom_cmdline", ('                if (c, bd, tho) in self.da:\n                    continue\n                self.da.add((c, bd, tho))\n',
                                    '                if (c, bd) in self.da:\n                    continue\n                self.da.add((c, bd))\n'),
     ["r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ"]),
    ("r27_quet_doc_environ", ('                    tho = Path(f"/proc/{c}/cmdline").read_bytes()\n',
                              '                    tho = Path(f"/proc/{c}/cmdline").read_bytes()\n                    Path(f"/proc/{c}/environ").read_bytes()\n'),
     ["r927_lay_mau_that_thay_sandbox_sau_exec_va_khong_doc_environ"]),
    ("r27_lenh_run_khong_lay_mau", ('            sandbox.bat_dau()\n', ''), ["r927_lenh_run_ghi_effort_va_sandbox_vao_run_json"]),
    ("r27_lenh_run_khong_ghi_so", ('        sandbox.ghi_so(ban_ghi, thu_muc / "stdout.log")\n', '        pass\n'),
     ["r927_lenh_run_ghi_effort_va_sandbox_vao_run_json"]),
    # wp748 r25/r26: mỗi chốt đo model phục vụ một đột biến gỡ đúng chốt của nó (r26 vòng 2: bộ lọc phân loại theo DÒNG).
    ("r25_ghi_moi_dong_tron", ('if so_doan == 1 and doan in _STDERR_CHO_PHEP_DONG:', 'if so_doan == 1 and het_dong:'),
     ["r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat", "r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace"]),
    ("r25_cho_phep_theo_tien_to", ('if so_doan == 1 and doan in _STDERR_CHO_PHEP_DONG:',
                                   'if so_doan == 1 and doan.startswith(_STDERR_CHO_PHEP):'),
     ["r925_chi_ghi_dong_cho_phep_nguyen_van_ke_ca_truoc_trace"]),
    ("r25_cho_phep_ca_dong_cut", ('if so_doan == 1 and doan in _STDERR_CHO_PHEP_DONG:', 'if doan in _STDERR_CHO_PHEP_DONG:'),
     ["r926_cho_phep_chi_dung_LF_hoac_mot_CRLF"]),
    ("r26_cho_phep_cat_moi_CRLF", ('if so_doan == 1 and doan in _STDERR_CHO_PHEP_DONG:',
                                   'if so_doan == 1 and doan.rstrip(b"\\r\\n") in _STDERR_CHO_PHEP:'),
     ["r926_cho_phep_chi_dung_LF_hoac_mot_CRLF"]),
    ("r25_bo_go_ansi", ('    sach = _RE_ANSI_B.sub(b"", dau)\n', '    sach = dau\n'),
     ["r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien"]),
    ("r25_khung_moi_target", ('TRACE\\s+tungstenite::protocol: Received message', 'TRACE\\s+\\S+: .*?Received message'),
     ["r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien"]),
    ("r25_moi_su_kien", ('    if ev.get("type") not in _SU_KIEN_KHUNG:\n        return None, "khac"\n',
                         '    if False:\n        return None, "khac"\n'),
     ["r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien"]),
    ("r25_nhan_id_model_rong", ('if not (isinstance(rid, str) and rid.strip() and isinstance(mdl, str) and mdl.strip()):',
                                'if not (isinstance(rid, str) and isinstance(mdl, str) and mdl):'),
     ["r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien"]),
    ("r25_gop_theo_id", ('if not any(x["response_id"] == m["response_id"] and x["model"] == m["model"] for x in ket):',
                         'if not any(x["response_id"] == m["response_id"] for x in ket):'),
     ["r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien"]),
    ("r25_bo_dem_mat", ('        elif loai == "ung_vien_hong" or ung_vien:\n            dem["mat"] = dem.get("mat", 0) + 1\n',
                        '        elif loai == "ung_vien_hong" or ung_vien:\n            pass\n'),
     ["r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien", "r926_khung_mot_doan_phan_loai_theo_type_DA_PARSE"]),
    ("r26_bo_dem_mat_nhieu_doan", ('    if ung_vien:\n        dem["mat"] = dem.get("mat", 0) + 1\n        return\n',
                                   '    if ung_vien:\n        return\n'),
     ["r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat", "r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han",
      "r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC"]),
    ("r26_phan_loai_theo_token", ('        elif loai == "ung_vien_hong" or ung_vien:', '        elif ung_vien:'),
     ["r926_khung_mot_doan_phan_loai_theo_type_DA_PARSE"]),
    ("r25_parse_khong_can_ca_dong", ('    if so_doan == 1 and tron:\n', '    if so_doan == 1:\n'),
     ["r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat"]),
    ("r25_doc_khong_tran", ('    for doan in iter(lambda: ong.readline(_TRAN_DONG), b""):', '    for doan in iter(ong.readline, b""):'),
     ["r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han"]),
    ("r25_xa_ong_khong_tran", ('            for doan in iter(lambda: ong.read(_TRAN_DONG), b""):',
                               '            for doan in iter(ong.read, b""):'), ["r925_bo_loc_hong_xa_ong_co_gioi_han"]),
    ("r26_bo_duoi_vat", ('        duoi = gon[-_DUOI_UNG_VIEN:]\n', '        duoi = b""\n'),
     ["r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC"]),
    ("r26_khong_bo_khoang_trang", ('gon = _RE_KHOANG_TRANG_B.sub(b"", _RE_ANSI_B.sub(b"", duoi + doan))', 'gon = _RE_ANSI_B.sub(b"", duoi + doan)'),
     ["r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC"]),
    ("r26_bo_xac_nhan_su_kien_khac", ('        if loai is not None and loai not in _SU_KIEN_KHUNG:\n            return\n',
                                      '        if False:\n            return\n'),
     ["r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran"]),
    ("r26_dau_dong_khong_noi", ('            dau += doan[:max(0, _TRAN_DAU_DONG - len(dau))]', '            pass'),
     ["r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran"]),
    ("r26_loai_khong_utf8_thay_the", ('            loai = k.group(1).decode("utf-8")\n', '            loai = k.group(1).decode("utf-8", "replace")\n'),
     ["r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO"]),
    ("r26_khong_ro_khong_dem", ('        dem["khong_ro"] = dem.get("khong_ro", 0) + 1\n', '        pass\n'),
     ["r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO"]),
    ("r26_khong_ro_moi_dong_dai", ('    if _RE_DAU_JSON.match(sach):\n', '    if True:\n'),
     ["r926_dong_NHAN_cat_nhieu_doan_ma_token_roi_cho_cat_van_tinh_mat"]),
    ("r26_utf8_thay_the", ('ev = json.loads(k.group(1).decode("utf-8"))', 'ev = json.loads(k.group(1).decode("utf-8", "replace"))'),
     ["r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat"]),
    ("r25_noi_rust_log_thua_ke", ('        env["RUST_LOG"] = _RUST_LOG_DO_MODEL\n',
                                  '        env["RUST_LOG"] = (rust_log_cu + "," if rust_log_cu else "") + _RUST_LOG_DO_MODEL\n'),
     ["r925_rust_log_thua_ke_bi_GHI_DE_khong_noi"]),
    ("r25_khong_bat_trace", ('_RUST_LOG_DO_MODEL = "tungstenite::protocol=trace"', '_RUST_LOG_DO_MODEL = "warn"'), ["r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat"]),
    ("r25_DO_DUOC_khi_loc_hong", ('    if loi:\n        return "KHONG_DO_DUOC"', '    if False:\n        return "KHONG_DO_DUOC"'),
     ["r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien", "r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai"]),
    ("r25_DO_DUOC_khi_ong_con_mo", ('    if con_doc:\n', '    if False:\n'),
     ["r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien", "r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC"]),
    ("r25_DO_DUOC_khi_mat", ('    if mat:\n', '    if False:\n'), ["r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien", "r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai"]),
    ("r26_DO_DUOC_khi_khong_ro", ('    if khong_ro:\n', '    if False:\n'), ["r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO"]),
    ("r25_DO_DUOC_khong_khung", ('    if not ket:\n        return "KHONG_DO_DUOC"', '    if False:\n        return "KHONG_DO_DUOC"'),
     ["r925_ket_luan_model_chi_DO_DUOC_khi_du_ba_dieu_kien", "r925_codex_khong_co_khung_thi_KHONG_DO_DUOC_khong_suy_tu_m"]),
    ("r25_so_khong_chuyen_loi", ('tt, ld = _ket_luan_model(ket_s, loi_s, con_doc, dem_s.get("mat", 0), dem_s.get("khong_ro", 0))',
                                 'tt, ld = _ket_luan_model(ket_s, [], con_doc, dem_s.get("mat", 0), dem_s.get("khong_ro", 0))'),
     ["r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai"]),
    ("r25_so_khong_chuyen_mat", ('tt, ld = _ket_luan_model(ket_s, loi_s, con_doc, dem_s.get("mat", 0), dem_s.get("khong_ro", 0))',
                                 'tt, ld = _ket_luan_model(ket_s, loi_s, con_doc, 0, dem_s.get("khong_ro", 0))'),
     ["r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai", "r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC"]),
    ("r26_so_khong_chuyen_khong_ro", ('tt, ld = _ket_luan_model(ket_s, loi_s, con_doc, dem_s.get("mat", 0), dem_s.get("khong_ro", 0))',
                                      'tt, ld = _ket_luan_model(ket_s, loi_s, con_doc, dem_s.get("mat", 0))'),
     ["r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO"]),
    ("r25_bo_chot_luong", ('            self.con_doc = self.luong.is_alive()\n', ''), ["r925_ghi_ket_qua_chot_luong_TRUOC_roi_moi_chup"]),
    ("r26_lay_mau_lai_luong_muon", ('        con_doc = True if self.con_doc is None else self.con_doc\n',
                                    '        con_doc = self.luong.is_alive()\n'), ["r926_chot_trang_thai_luong_O_RANH_GIOI_cho_khong_lay_mau_lai"]),
    ("r26_mac_dinh_chua_chot_la_xong", ('        con_doc = True if self.con_doc is None else self.con_doc\n',
                                        '        con_doc = False if self.con_doc is None else self.con_doc\n'),
     ["r926_ghi_so_truoc_khi_chot_khong_DO_DUOC"]),
    ("r25_doc_ong_khong_han", ('            self.luong.join(timeout=han)\n', '            self.luong.join()\n'),
     ["r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC"]),
    ("r26_dong_tep_truoc_chot", ('            self.luong.join(timeout=han)\n            self.con_doc = self.luong.is_alive()\n        self.f_err.close()\n',
                                 '            self.f_err.close()\n            self.luong.join(timeout=han)\n            self.con_doc = self.luong.is_alive()\n'),
     ["r926_ket_thuc_chot_luong_TRUOC_khi_dong_tep", "r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC"]),
    ("r26_san_xuat_dong_tep_truoc", ('            bo_loc.ket_thuc(10)\n', '            f_err.close()\n            bo_loc.ket_thuc(10)\n'),
     ["r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC"]),
    ("r26_tep_stderr_co_dem", ('**({"buffering": 0} if do_model else', '**({} if do_model else'),
     ["r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC"]),
    ("r25_bo_loc_hong_khong_xa_ong", ('            for doan in iter(lambda: ong.read(_TRAN_DONG), b""):\n                _dem_bo(dem, doan)   # R26-COUNT-09: byte xả đi vẫn là byte bị bỏ\n', '            pass\n'),
     ["r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc"]),
    ("r26_xa_khong_dem", ('                _dem_bo(dem, doan)   # R26-COUNT-09: byte xả đi vẫn là byte bị bỏ\n', '                pass\n'),
     ["r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem"]),
    ("r25_bo_loc_hong_khong_ghi_loi", ('        loi.append(type(e).__name__)\n', ''),
     ["r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc"]),
    ("r26_tep_dong_khong_dem", ('        _dem_bo(dem, doan[da:])  # tệp đã đóng vì hậu duệ giữ ống quá hạn chờ: bỏ, không ghi lệch chỗ\n', '        pass\n'),
     ["r926_byte_xa_va_dong_khong_ghi_duoc_van_duoc_dem"]),
    ("r26_ghi_loi_khong_dem", ('    except Exception:\n        _dem_bo(dem, doan[da:])\n        raise\n', '    except Exception:\n        raise\n'),
     ["r926_ghi_het_dem_dung_phan_chua_ghi"]),
    ("r26_ghi_dem_ca_doan", ('        _dem_bo(dem, doan[da:])\n        raise\n', '        _dem_bo(dem, doan)\n        raise\n'),
     ["r926_ghi_het_dem_dung_phan_chua_ghi"]),
    ("r26_ghi_khong_lap", ('            n = f_err.write(doan[da:])\n            if not n:\n                raise OSError("write tra 0 byte")\n            da += n\n',
                           '            f_err.write(doan[da:])\n            da = len(doan)\n'),
     ["r926_ghi_het_dem_dung_phan_chua_ghi"]),
    ("r26_luong_hong_lot_ra", ('        try:\n            self.luong.start()\n        except Exception as e:\n',
                               '        try:\n            self.luong.start()\n        except ZeroDivisionError as e:\n'),
     ["r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC"]),
    ("r26_luong_hong_khong_dong_ong", ('                self.ong.close()\n', '                pass\n'),
     ["r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC"]),
    ("r26_luong_hong_khong_ghi_loi", ('            self.loi.append(type(e).__name__)\n            with', '            with'),
     ["r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC"]),
    ("r26_cho_luong_chua_chay", ('        if self.luong.ident is not None:     # luồng chưa từng chạy', '        if True:     # luồng chưa từng chạy'),
     ["r926_khong_sinh_duoc_luong_doc_thi_dong_ong_va_KHONG_DO_DUOC"]),
    ("r26_khong_ro_khong_doi_json", ('_RE_DAU_JSON = re.compile(_DAU_NHAN + rb"\\{")', '_RE_DAU_JSON = re.compile(_DAU_NHAN)'),
     ["r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO"]),
    ("r26_doc_tron_khong_parse_bo_qua", ('        elif loai is None and _RE_DAU_JSON.match(sach):\n', '        elif False:\n'),
     ["r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO"]),
    ("r26_ghi_bo_chot_0_byte", ('            if not n:\n                raise OSError("write tra 0 byte")\n', ''),
     ["r926_ghi_het_dem_dung_phan_chua_ghi"]),
    # r26 vòng 4 (cross-review r26d R26-TEST-13): rà TOÀN BỘ vị từ của bộ lọc, mỗi vị từ một đột biến riêng.
    ("r26_mot_doan_bo_dieu_kien_so_doan", ('    if so_doan == 1 and tron:\n', '    if tron:\n'),
     ["r925_dong_vuot_tran_khong_parse_va_doc_co_gioi_han"]),
    ("r26_doc_tron_khong_ro_ca_su_kien_khac", ('        elif loai is None and _RE_DAU_JSON.match(sach):\n', '        elif _RE_DAU_JSON.match(sach):\n'),
     ["r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran"]),
    ("r26_doc_tron_khong_ro_khong_doi_json", ('        elif loai is None and _RE_DAU_JSON.match(sach):\n', '        elif loai is None:\n'),
     ["r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO"]),
    ("r26_doc_tron_bo_token", ('        elif loai == "ung_vien_hong" or ung_vien:', '        elif loai == "ung_vien_hong":'),
     ["r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien"]),
    ("r26_tien_to_ung_vien_tha", ('        if loai is not None and loai not in _SU_KIEN_KHUNG:\n', '        if loai is not None:\n'),
     ["r926_ket_dong_tien_to_ung_vien_ma_khong_token_la_KHONG_RO"]),
    ("r26_tien_to_khong_tran", ('            dau += doan[:max(0, _TRAN_DAU_DONG - len(dau))]', '            dau += doan'),
     ["r926_tien_to_dong_dai_co_tran_va_noi_qua_doan"]),
    ("r26_tien_to_bo_max", ('            dau += doan[:max(0, _TRAN_DAU_DONG - len(dau))]', '            dau += doan[:_TRAN_DAU_DONG - len(dau)]'),
     ["r926_tien_to_dong_dai_co_tran_va_noi_qua_doan"]),
    ("r26_token_khong_dinh", ('        ung_vien = ung_vien or bool(_RE_UNG_VIEN_GON.search(gon))\n', '        ung_vien = bool(_RE_UNG_VIEN_GON.search(gon))\n'),
     ["r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC"]),
    ("r26_khong_dat_lai_moi_dong", ('        if het_dong:\n            dau, duoi, ung_vien, so_doan = b"", b"", False, 0\n', ''),
     ["r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien"]),
    ("r26_bo_dong_cut_EOF", ('    if not het_dong:\n        _ket_dong(dau, so_doan, False, ung_vien, ket, dem)\n', ''),
     ["r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat"]),
    ("r26_response_khong_kiem_object", ('(r.get("id"), r.get("model")) if isinstance(r, dict) else (None, None)', '(r.get("id"), r.get("model"))'),
     ["r926_response_hong_tung_vi_tu_tinh_mat_khong_loi"]),
    ("r26_id_khong_kiem_chuoi", ('if not (isinstance(rid, str) and rid.strip() and', 'if not (rid.strip() and'),
     ["r926_response_hong_tung_vi_tu_tinh_mat_khong_loi"]),
    ("r26_id_khong_strip", ('if not (isinstance(rid, str) and rid.strip() and', 'if not (isinstance(rid, str) and rid and'),
     ["r926_response_hong_tung_vi_tu_tinh_mat_khong_loi"]),
    ("r26_model_khong_kiem_chuoi", ('and isinstance(mdl, str) and mdl.strip()):', 'and mdl.strip()):'),
     ["r926_response_hong_tung_vi_tu_tinh_mat_khong_loi"]),
    ("r26_model_khong_strip", ('and isinstance(mdl, str) and mdl.strip()):', 'and isinstance(mdl, str) and mdl):'),
     ["r926_response_hong_tung_vi_tu_tinh_mat_khong_loi"]),
    ("r26_ket_thuc_khong_dong_tep", ('        self.f_err.close()\n\n    def ghi_so', '\n    def ghi_so'),
     ["r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC"]),
    ("r26_khong_ghi_so", ('    if bo_loc is not None:\n        bo_loc.ghi_so(ban_ghi)\n', ''),
     ["r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat"]),
    # r26 vòng 5 (cross-review r26e R26-TEST-14): kiểm kê vị từ của reviewer — mỗi dòng 'Missing' một đột biến riêng.
    ('r26_rv5_prefix_decoded', ('        if loai is not None and loai not in _SU_KIEN_KHUNG:\n', '        if loai not in _SU_KIEN_KHUNG:\n'),
     ['r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO']),
    ('r26_rv5_dedup_response_id', ('x["response_id"] == m["response_id"] and x["model"] == m["model"]', 'x["model"] == m["model"]'),
     ['r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat']),
    ('r26_rv5_dedup_whole', ('            if not any(x["response_id"] == m["response_id"] and x["model"] == m["model"] for x in ket):\n', '            if True:\n'),
     ['r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat']),
    ('r26_rv5_frame_match_guard', ('    if not k:\n        return None, None\n', '    if False:\n        return None, None\n'),
     ['r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien']),
    ('r26_rv5_parsed_model_guard', ('        if m is not None:\n', '        if True:\n'),
     ['r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien']),
    ('r26_rv5_prefix_match_guard', ('    k = _RE_LOAI_DAU.match(sach)\n    if k:\n', '    k = _RE_LOAI_DAU.match(sach)\n    if True:\n'),
     ['r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO']),
    ('r26_rv5_first_chunk_capture', ('        if so_doan == 1:\n            dau = doan', '        if True:\n            dau = doan'),
     ['r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO']),
    ('r26_rv5_classify_only_at_lf', ('        if het_dong:\n            _ket_dong(dau, so_doan, True, ung_vien, ket, dem)\n', '        if True:\n            _ket_dong(dau, so_doan, True, ung_vien, ket, dem)\n'),
     ['r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran']),
    ('r26_rv5_reason_guard', ('        if ld:\n            ban_ghi["model_phuc_vu_ly_do"] = ld\n', '        if False:\n            ban_ghi["model_phuc_vu_ly_do"] = ld\n'),
     ['r925_ghi_ket_qua_tu_luong_that_loi_va_mat_deu_ha_trang_thai']),
    ('r26_rv5_rust_override_record', ('        if rust_log_cu:\n            ban_ghi["model_phuc_vu_rust_log_ke_thua_bi_ghi_de"] = True\n', '        if False:\n            ban_ghi["model_phuc_vu_rust_log_ke_thua_bi_ghi_de"] = True\n'),
     ['r925_rust_log_thua_ke_bi_GHI_DE_khong_noi']),
    ('r26_rv5_exception_valueerror', ('    except ValueError:\n        return None, None\n', '    except ZeroDivisionError:\n        return None, None\n'),
     ['r926_model_khong_utf8_nghiem_khong_nhan_va_tinh_mat']),
    ('r26_rv5_old_late_production_latch', ('            bo_loc.ket_thuc(10)\n', '            bo_loc.luong.join(timeout=10)\n            f_err.close()\n            bo_loc.ket_thuc(0)\n'),
     ['r926_lenh_run_doc_xong_luc_dong_tep_thi_KHONG_DO_DUOC']),
    ('r26_rv5_optional_counter_init', ('    dem = {} if dem is None else dem\n', '    dem = dem\n'),
     ['r925_bo_loc_hong_thi_ghi_loi_va_xa_ong_khong_ghi_dong_chua_loc']),
    ('r26_rv5_retain_caller_counter', ('    dem = {} if dem is None else dem\n', '    dem = {}\n'),
     ['r926_lenh_run_khung_mat_thi_run_json_KHONG_DO_DUOC']),
    ('r26_rv5_candidate_search', ('        ung_vien = ung_vien or bool(_RE_UNG_VIEN_GON.search(gon))\n', '        ung_vien = ung_vien\n'),
     ['r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC']),
    ('r26_rv5_target_only', ('TRACE\\s+tungstenite::protocol: Received message', 'TRACE\\s+\\S+: Received message'),
     ['r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien']),
    ('r26_rv5_receive_position_only', ('TRACE\\s+tungstenite::protocol: Received message', 'TRACE\\s+tungstenite::protocol: .*?Received message'),
     ['r925_khung_chi_nhan_tu_tungstenite_protocol_dung_vi_tri_va_dung_su_kien']),
    ('r26_rv5_lf_detection', ('        het_dong = doan.endswith(b"\\n")\n', '        het_dong = True\n'),
     ['r925_khung_cut_o_EOF_hoac_giua_doan_doc_khong_nhan_va_tinh_mat']),
    ('r26_rv5_codex_mode_disabled', ('    do_model = _la_codex(a.lenh)\n', '    do_model = False\n'),
     ['r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat']),
    ('r26_rv5_codex_env_guard', ('    if do_model:\n        env = dict(os.environ)\n', '    if False:\n        env = dict(os.environ)\n'),
     ['r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat']),
    ('r26_rv5_codex_reader_guard', ('        if do_model:\n            bo_loc = _BoLocStderr(p.stderr, f_err)\n', '        if False:\n            bo_loc = _BoLocStderr(p.stderr, f_err)\n'),
     ['r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat']),
    ('r26_rv5_codex_pipe_guard', ('stderr=subprocess.PIPE if do_model else f_err,', 'stderr=f_err,'),
     ['r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat']),
    ('r26_rv5_finish_object_guard', ('        if bo_loc is not None:\n            # Hậu duệ', '        if False:\n            # Hậu duệ'),
     ['r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat']),
    # r26 vòng 6 (cross-review r26f R26-TEST-15): kiểm kê MÁY từng thành phần regex/hằng chuẩn hoá của bộ lọc.
    ('r26_rv6_a_ansi_bo_tham_so_hoi', ('_RE_ANSI_B = re.compile(rb"\\x1b\\[[0-9;?]*', '_RE_ANSI_B = re.compile(rb"\\x1b\\[[0-9;]*'),
     ['r926_ngu_phap_khung_tung_thanh_phan']),
    ('r26_rv6_a_ansi_bo_trung_gian', ('[0-9;?]*[ -/]*[@-~]")', '[0-9;?]*[@-~]")'),
     ['r926_ngu_phap_khung_tung_thanh_phan']),
    ('r26_rv6_a_ansi_chi_m', ('[0-9;?]*[ -/]*[@-~]")', '[0-9;?]*[ -/]*m")'),
     ['r926_ngu_phap_khung_tung_thanh_phan']),
    ('r26_rv6_b_bo_neo_dau', ('_DAU_NHAN = rb"^\\d{4}', '_DAU_NHAN = rb".*?\\d{4}'),
     ['r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC']),
    ('r26_rv6_b_moc_thoi_gian', ('^\\d{4}-\\d\\d-\\d\\dT\\S+\\s+TRACE', '^\\S+\\s+TRACE'),
     ['r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC']),
    ('r26_rv6_b_muc_TRACE', ('TRACE\\s+tungstenite::protocol: Received message', '\\S+\\s+tungstenite::protocol: Received message'),
     ['r926_ngu_phap_khung_tung_thanh_phan']),
    ('r26_rv6_b_khoang_truoc_TRACE', ('T\\S+\\s+TRACE', 'T\\S+\\s*TRACE'),
     ['r926_ngu_phap_khung_tung_thanh_phan']),
    ('r26_rv6_b_dau_cach_sau_message', ('protocol: Received message "', 'protocol: Received message"'),
     ['r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat']),
    ('r26_rv6_c_neo_cuoi', ('_RE_KHUNG = re.compile(_DAU_NHAN + rb"(\\{.*\\})\\s*$")', '_RE_KHUNG = re.compile(_DAU_NHAN + rb"(\\{.*\\})")'),
     ['r926_ngu_phap_khung_tung_thanh_phan']),
    ('r26_rv6_c_doi_tuong_json', ('_RE_KHUNG = re.compile(_DAU_NHAN + rb"(\\{.*\\})\\s*$")', '_RE_KHUNG = re.compile(_DAU_NHAN + rb"(.*)\\s*$")'),
     ['r926_ngu_phap_khung_tung_thanh_phan']),
    ('r26_rv6_d_khoa_type', ('rb\'\\{\\s*"type"\\s*:', 'rb\'\\{\\s*"[^" ]+"\\s*:'),
     ['r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO']),
    ('r26_rv6_d_khong_escape', ('\\s*"([^"\\\\]*)"\')', '\\s*"([^"]*)"\')'),
     ['r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO']),
    ('r26_rv6_d_dong_nhay', ('\\s*"([^"\\\\]*)"\')', '\\s*"([^"\\\\]*)\')'),
     ['r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO']),
    ('r26_rv6_d_khoang_sau_ngoac', ('rb\'\\{\\s*"type"\\s*:', 'rb\'\\{"type"\\s*:'),
     ['r926_tien_to_dong_dai_co_tran_va_noi_qua_doan']),
    ('r26_rv6_d_khoang_hai_cham', ('"type"\\s*:\\s*"(', '"type":"('),
     ['r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran']),
    ('r26_rv6_e_bo_completed', ('rb\'"type":"response\\.(?:created|completed)"\'', 'rb\'"type":"response\\.(?:created)"\''),
     ['r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC']),
    ('r26_rv6_e_cham_bat_ky', ('rb\'"type":"response\\.(?:created|completed)"\'', 'rb\'"type":"response.(?:created|completed)"\''),
     ['r926_ngu_phap_khung_tung_thanh_phan']),
    ('r26_rv6_f_chi_dau_cach', ('_RE_KHOANG_TRANG_B = re.compile(rb"\\s+")', '_RE_KHOANG_TRANG_B = re.compile(rb" +")'),
     ['r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC']),
    ('r26_rv6_g_duoi_ngan', ('_DUOI_UNG_VIEN = 64\n', '_DUOI_UNG_VIEN = 16\n'),
     ['r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC']),
    ('r26_rv6_h_luong_khong_ansi', ('gon = _RE_KHOANG_TRANG_B.sub(b"", _RE_ANSI_B.sub(b"", duoi + doan))', 'gon = _RE_KHOANG_TRANG_B.sub(b"", duoi + doan)'),
     ['r926_quet_moi_tran_doc_khung_vat_cho_cat_luon_KHONG_DO_DUOC']),
    ('r26_rv6_i_tran_dau_nho', ('_TRAN_DAU_DONG = 4096', '_TRAN_DAU_DONG = 64'),
     ['r926_dong_NHAN_dai_su_kien_khac_khong_tinh_mat_moi_tran']),
    ('r26_rv6_j_bo_CRLF', ('for duoi in (b"\\n", b"\\r\\n"))', 'for duoi in (b"\\n",))'),
     ['r926_cho_phep_chi_dung_LF_hoac_mot_CRLF']),
    ('r26_rv6_l_su_kien_bo_completed', ('_SU_KIEN_KHUNG = ("response.created", "response.completed")', '_SU_KIEN_KHUNG = ("response.created",)'),
     ['r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat']),
    ('r26_rv6_m_dau_json_bo_ngoac', ('_RE_DAU_JSON = re.compile(_DAU_NHAN + rb"\\{")', '_RE_DAU_JSON = re.compile(_DAU_NHAN)'),
     ['r926_dong_NHAN_dai_khong_xac_nhan_duoc_loai_la_KHONG_RO']),
    # r26 vòng 7 (cross-review r26g R26-TEST-16): phần KHÔNG phải regex — cờ luồng, chế độ tệp, ba phép chụp. Phần regex
    # do `r926_dot_bien_tu_sinh_moi_thanh_phan_regex` tự sinh, không đăng ký tay ở đây.
    ('r26_rv7_luong_doc_khong_daemon', ('                                      daemon=True)', '                                      daemon=False)'),
     ['r925_chau_giu_ong_stderr_thi_khong_treo_va_KHONG_DO_DUOC']),
    ('r26_rv7_tep_stderr_van_ban', ('stderr.log").open("wb" if do_model else "w",', 'stderr.log").open("w",'),
     ['r925_codex_ghi_model_phuc_vu_tung_response_va_khong_lo_bi_mat']),
    ('r26_rv7_khong_chup_ket', ('ket_s, loi_s, dem_s = list(self.ket), list(self.loi), dict(self.dem)', 'ket_s, loi_s, dem_s = self.ket, list(self.loi), dict(self.dem)'),
     ['r926_ghi_so_chup_rieng_ket_loi_dem']),
    ('r26_rv7_khong_chup_loi', ('ket_s, loi_s, dem_s = list(self.ket), list(self.loi), dict(self.dem)', 'ket_s, loi_s, dem_s = list(self.ket), self.loi, dict(self.dem)'),
     ['r926_ghi_so_chup_rieng_ket_loi_dem']),
    ('r26_rv7_khong_chup_dem', ('ket_s, loi_s, dem_s = list(self.ket), list(self.loi), dict(self.dem)', 'ket_s, loi_s, dem_s = list(self.ket), list(self.loi), self.dem'),
     ['r926_ghi_so_chup_rieng_ket_loi_dem']),
    ("r25_loc_ca_luot_khong_phai_codex", ('    do_model = _la_codex(a.lenh)\n', '    do_model = True\n'),
     ["r925_khong_phai_codex_giu_nguyen_so_va_stderr"]),
    # wp802 (N1–N4, N6): mỗi tiêu chí một đột biến gỡ đúng chốt của nó.
    ("wp802_bo_nhanh_BI_CHE", ('        if thay is not None and hong_dau is not None:', '        if False:'),
     ["r802_doctor_rg_tran_hong_la_BI_CHE", "r802_doctor_git_tran_hong_la_BI_CHE"]),
    ("wp802_BI_CHE_khong_vao_thieu", ('xac_thuc_ok is False or bi_che)', 'xac_thuc_ok is False)'),
     ["r802_doctor_rg_tran_hong_la_BI_CHE", "r802_doctor_git_tran_hong_la_BI_CHE"]),
    ("wp802_luon_BI_CHE_khi_co_ung_vien", ('        if thay is not None and hong_dau is not None:', '        if thay is not None:'),
     ["r802_doctor_rg_chi_ban_tot_khong_BI_CHE"]),
    ("wp802_bo_git_khoi_tap_ap_dung", ('_AP_DUNG_BI_CHE = frozenset({"rg", "git"})', '_AP_DUNG_BI_CHE = frozenset({"rg"})'),
     ["r802_doctor_git_tran_hong_la_BI_CHE"]),
    ("wp802_BI_CHE_moi_cong_cu", ('if c["ten"] in _AP_DUNG_BI_CHE else None)', 'if True else None)'),
     ["r802_doctor_bash_ngoai_pham_vi_BI_CHE"]),
    # Codex lượt 1 F1: tên trần giải độc lập (mục PATH rỗng = cwd), đo TRƯỚC, đúng bản.
    ("wp802_ten_tran_bo_muc_PATH_rong", ('    for muc in moi_truong.get("PATH", "").split(os.pathsep):\n        for d in duoi:',
      '    for muc in filter(None, moi_truong.get("PATH", "").split(os.pathsep)):\n        for d in duoi:'),
     ["r802_doctor_ten_tran_tu_muc_PATH_rong"]),
    ("wp802_khong_dat_ten_tran_len_dau", ('        if tran:\n            ung_vien = [', '        if False:\n            ung_vien = ['),
     ["r802_doctor_ten_tran_tu_muc_PATH_rong"]),
    ("wp802_hong_dau_la_moi_ban_hong", ('            if tran and d == tran:\n', '            if True:\n'),
     ["r802_doctor_ten_tran_tu_muc_PATH_rong"]),
    ("wp802_cac_duong_dan_lai_dung_which", ('them(ten, _ten_tran_giai_ra(ten, dict(moi_truong, PATH=muc), kieu_bash=False))',
     'them(ten, shutil.which(ten, path=muc))'), ["r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT"]),
    ("wp802_cac_duong_dan_theo_kieu_bash", ('PATH=muc), kieu_bash=False))', 'PATH=muc)))'),
     ["r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT"]),
    ("wp802_pathext_rong_khong_lui_mac_dinh", ('(moi_truong.get("PATHEXT") or ".COM', '(moi_truong.get("PATHEXT") if "PATHEXT" in moi_truong else ".COM'),
     ["r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT"]),
    ("wp802_ten_co_duoi_khong_noi_them", ('([""] if any(ten.upper().endswith(e.upper()) for e in ext) else []) + ext)',
     '([""] if any(ten.upper().endswith(e.upper()) for e in ext) else ext))'), ["r802_cac_duong_dan_chi_trong_PATH_va_theo_PATHEXT"]),
    ("wp1077_bo_chay_lai_ENOEXEC", ('            if e.errno == errno.ENOEXEC and os.path.isfile("/bin/sh"):', '            if False:'),
     ["r1077_doctor_khong_shebang_chay_duoc_khong_BI_CHE", "r1077_xac_thuc_khong_shebang_chay_duoc"]),
    ("wp1077_chay_lai_moi_OSError", ('            if e.errno == errno.ENOEXEC and os.path.isfile("/bin/sh"):',
      '            if os.path.isfile("/bin/sh"):'), ["r1077_probe_khong_chay_lai_khi_khong_phai_ENOEXEC"]),
    ("wp1077_xac_thuc_khong_dung_probe_chung", ('p = _chay_probe_nhu_shell([duong_dan, *doi_so]', 'p = subprocess.run([duong_dan, *doi_so]'),
     ["r1077_xac_thuc_khong_shebang_chay_duoc"]),
    ("wp1077_chay_lai_bo_qua_rc", ('                return subprocess.run(["/bin/sh", tep, *lenh[1:]], **kw)',
      '                q = subprocess.run(["/bin/sh", tep, *lenh[1:]], **kw)\n'
      '                return subprocess.CompletedProcess(lenh, 0, q.stdout, q.stderr)'),
     ["r1077_doctor_khong_shebang_hong_van_BI_CHE"]),
    # Codex lượt 1: F3 (đối số) · F1 (probe trong phạm vi; trừ _git/_do_codex_song, #1083).
    ("wp1077_retry_mat_doi_so", ('                return subprocess.run(["/bin/sh", tep, *lenh[1:]], **kw)',
      '                return subprocess.run(["/bin/sh", tep], **kw)'), ["r1077_retry_giu_argv_env"]),
    ("wp1077_codex_status_spawn_tran", ('p = _chay_probe_nhu_shell([duong_codex, "login", "status"]',
      'p = subprocess.run([duong_codex, "login", "status"]'),
     ["r1077_doctor_codex_status_khong_shebang", "r1077_probe_doctor_khong_spawn_tran"]),
    ("wp1077_llm_khong_qua_helper", ('    return _chay_probe_nhu_shell(lenh, capture_output=True, text=True, encoding="utf-8",',
      '    return subprocess.run(lenh, capture_output=True, text=True, encoding="utf-8",'),
     ["r1077_llm_khong_shebang_ten_tran_giai_PATH", "r1077_probe_doctor_khong_spawn_tran"]),
    ("wp1077_gh_auth_spawn_tran", ('pg = _chay_probe_nhu_shell(["gh", "auth", "status"]', 'pg = subprocess.run(["gh", "auth", "status"]'),
     ["r1077_probe_doctor_khong_spawn_tran"]),
    # Codex lượt 2–5 F4: tự duyệt PATH như execvp (bỏ ⇒ subprocess chạy bản sau / sh TÊN không tra PATH).
    ("wp1077_ten_tran_khong_giai_PATH", ('        ung_vien = [f"{d}/{ten}" if d else ten for d in phan]',
      '        ung_vien = [ten]'),
     ["r1077_llm_khong_shebang_ten_tran_giai_PATH", "r1077_PATH_rong_khong_bo_qua_wrapper_dau"]),
    ("wp1077_PATH_rong_khong_chuan_hoa_duong_dan", ('            return subprocess.run(lenh, executable=tep if os.sep in tep else os.curdir + os.sep + tep, **kw)',
      '            return subprocess.run(lenh, executable=tep, **kw)'),
     ["r1077_PATH_rong_khong_bo_qua_wrapper_dau"]),
    ("wp1077_abspath_doi_nghia_symlink", ('[f"{d}/{ten}" if d else ten for d', '[os.path.abspath(f"{d}/{ten}" if d else ten) for d'),
     ["r1077_PATH_rong_khong_bo_qua_wrapper_dau", "r1077_cwd_dai_khong_keo_dai_duong_da_chay_duoc",
      "r1077_PATH_hop_dong_glibc"]),
    ("wp1077_tiep_moi_loi_exec", ('            if os.sep in ten or e.errno not in tiep:', '            if os.sep in ten:'),
     ["r1077_PATH_hop_dong_glibc"]),
    ("wp1077_PATH_ma_hoa_strict", ('[d if len(os.fsencode(d)) < tran else "" for d in phan[:-1]]', '[d if len(d.encode()) < tran else "" for d in phan[:-1]]'),
     ["r1077_PATH_hop_dong_glibc"]),
    ("wp1077_PATH_dai_bo_han", ('[d if len(os.fsencode(d)) < tran else "" for d in phan[:-1]]', '[d for d in phan[:-1] if len(os.fsencode(d)) < tran]'),
     ["r1077_PATH_rong_khong_bo_qua_wrapper_dau"]),
    ("wp1077_mat_gach_cuoi_PATH", ('[f"{d}/{ten}" if d else ten for d', '[os.path.join(d, ten) for d'), ["r1077_PATH_hop_dong_glibc"]),
    ("wp1077_dung_o_loi_tim_kiem", ('            if os.sep in ten or e.errno not in tiep:', '            if True:'),
     ["r1077_PATH_rong_khong_bo_qua_wrapper_dau"]),
    ("wp802_launcher_winget_thanh_choco", ('"Windows": "winget install --id BurntSushi.ripgrep.MSVC -e"',
      '"Windows": "choco install --id BurntSushi.ripgrep.MSVC -e"'),
     ["r802_bang_cai_rg_khop_cong_cu_yaml"]),
    ("g6_trust_windows_separator_disabled",
     ('if platform.system() == "Windows" else (lambda p: p)',
      'if False else (lambda p: p)'),
     ["r484_g6_trust_windows_separator_aliases"]),
    ("g6_trust_conflicting_alias_ignored",
     ('for v in cac_muc):', 'for v in []):'),
     ["r484_g6_trust_windows_separator_aliases"]),
    ("g6_trust_posix_separator_folded",
     ('if platform.system() == "Windows" else (lambda p: p)', 'if True else (lambda p: p)'),
     ["r484_g6_trust_posix_backslash_is_not_separator"], ("posix", "POSIX path semantics")),
    ("g4_windows_sid_alias_not_normalized",
     ('self._win_sid(fields[5])', 'fields[5]'),
     ["r484_g4_windows_sid_alias_identity"], ("windows", "native SID conversion")),
    ("g4_windows_LA_not_current_owner",
     ('allowed = {self.sid, "S-1-5-18", "S-1-5-32-544"}',
      'allowed = {self.sid, "S-1-5-18", "S-1-5-32-544", self._win_sid("LA")}'),
     ["r484_g4_windows_sid_alias_identity"], ("windows", "native SID conversion")),
    ("g2_windows_directory_pin_access",
     ('(0x81 | (0x20000 if security else 0))', '(0x80 | (0x20000 if security else 0))'),
     ["r484_g2_storage_kernel_guardrails"], ("windows", "native Windows share-delete pin")),
    ("g2_rejected_refresh_khong_phu_thuoc_metadata",
     ('payload = {key: tokens.get(key)}', 'payload = tokens'),
     ["r484_g2_recovery_probe_rollback_va_snapshot_moi"]),
    ("g2_resume_bo_prompt",
     ('or cp["prompt_sha256"] != kq["prompt_sha256"]', 'or False'),
     ["r484_g2_checkpoint_resume_va_gia_auth_khong_refund"]),
    ("g2_unknown_child_khong_duoc_cap_void",
     ('requested_void = ban_ghi.pop("void_reason", None)',
      'requested_void = ban_ghi.get("void_reason")'),
     ["r484_g2_checkpoint_resume_va_gia_auth_khong_refund"]),
    ("g2_resume_bo_head",
     ('or cp["head"] != kq["head"]', 'or False'),
     ["r484_g2_checkpoint_resume_va_gia_auth_khong_refund"]),
    # wp484 g7 — mỗi P2 một đột biến gỡ đúng bản vá.
    ("g7_home_sai_lai_traceback",
     ('    except OSError as e:\n        raise Chan(MA_CHUA_XAC_THUC, f"CODEX_HOME không hợp lệ',
      '    except ValueError as e:\n        raise Chan(MA_CHUA_XAC_THUC, f"CODEX_HOME không hợp lệ'),
     ["r484_g7_credential_status_home_sai_la_chan_khong_traceback"]),
    ("g7_nuot_loi_ghi_trang_thai",
     ('            if not _danh_dau_auth_hong(home, da_probe):\n                return False, (f"KHÔNG ghi',
      '            if False:\n                return False, (f"KHÔNG ghi'),
     ["r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra"]),
    ("g7_f03_doc_lai_sau_probe",
     ('            data = da_probe if da_probe is not None else store.read()',
      '            data = store.read()'),
     ["r484_g7_tu_choi_ghi_dung_ban_da_probe"]),
    ("g7_f01_materializer_gop_loi",
     ('                        except (OSError, ValueError) as e:\n'
      '                            result["cach"] = ("CHỜ snapshot mới: auth bị từ chối nhưng KHÔNG',
      '                        except KeyError as e:\n'
      '                            result["cach"] = ("CHỜ snapshot mới: auth bị từ chối nhưng KHÔNG'),
     ["r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do"]),
    ("g7_bo_doc_lai_truoc_replace",
     ('            if self.read(name) != expected:\n'
      '                raise OSError("credential changed before promotion")',
      '            if False:\n'
      '                raise OSError("credential changed before promotion")'),
     ["r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi"]),
    ("g8_xong_rc0_van_giu_failure_class",
     ('        ban_ghi.pop("failure_class", None)',
      '        pass'),
     ["r484_g8_run_xong_khong_mang_failure_class"]),
    ("m1_xoa_actionlint_khoi_cong_cu",
     ('    {"ten": "actionlint", "bat_buoc": False, "ung_vien": ["actionlint"],',
      '    {"ten": "actionlint_disabled", "bat_buoc": False, "ung_vien": ["actionlint"],'),
     ["t149_doctor_do_actionlint_va_shellcheck"]),
    ("m2_im_lang_khi_bien_utf8_xanh",
     ('        # M2: LUẬT ĐỌC BIẾN UTF-8 TRƯỚC KHI KẾT LUẬN — in KỂ CẢ khi mọi thứ xanh.\n        b_u8 = _do_bien_utf8(moi_truong)\n        _in_an_toan("BIEN UTF-8 (chong loi charmap/cp1258 tren Windows):")',
      '        # M2: ĐỘT BIẾN IM LẶNG KHI XANH\n        b_u8 = _do_bien_utf8(moi_truong)\n        if b_u8["canh_bao"]:\n            _in_an_toan("BIEN UTF-8 (chong loi charmap/cp1258 tren Windows):")'),
     ["t150_doctor_do_bien_utf8_in_ca_khi_xanh"]),
    ("m3_doc_bam_tep_thay_vi_dau_vet",
     ('    for rel in _CAC_DUONG_VET_HOOK:\n        tep = goc / rel\n        if not tep.is_file():\n            continue',
      '    for rel in _CAC_DUONG_VET_HOOK:\n        tep = goc / rel\n        if not duong.is_file():  # doc tep hook thay vi dau vet\n            continue'),
     ["t151_m3_phan_biet_da_chay_voi_tep_moi"]),
    ("m3b_bo_kiem_do_tuoi_dau_vet",
     ('        if tuoi > _HAN_DAU_VET_HOOK_GIAY:',
      '        if False:  # bo kiem do tuoi'),
     ["t154_m3_dau_vet_CU_KHONG_con_la_DA_CHAY"]),
    ("m4_noi_long_da_chung_minh_kha_dung",
     ('DA_CHUNG_MINH_KHA_DUNG = frozenset({"DUNG_DUOC"})',
      'DA_CHUNG_MINH_KHA_DUNG = frozenset({"DUNG_DUOC", "DA_CHAY"})'),
     ["t149_doctor_do_actionlint_va_shellcheck"]),
    ("m5_bo_kiem_tra_ngoai_ascii",
     ('    co_ngoai_ascii = any(ord(c) > 127 for c in duong)',
      '    co_ngoai_ascii = False  # dot bien bo kiem tra ngoai ascii'),
     ["t153_doctor_do_duong_dan_kho_co_dau_cach_hoac_phi_ascii"]),
    ("bo_ky_ban_ghi_luot",
     ('    if khoa_ky:\n        ban_ghi["chu_ky"] = ky_ban_ghi_luot(ban_ghi, khoa_ky)',
      '    if False:\n        ban_ghi["chu_ky"] = ky_ban_ghi_luot(ban_ghi, khoa_ky)'),
     ["t144_run_ghi_nonce_va_hmac_khong_lo_khoa"]),
    ("m1_coi_worktree_la_hop_le",
     ('            return {"trang_thai": "DO", "chi_tiet": "git worktree", "ma": "git_worktree"}',
      '            return {"trang_thai": "DAT", "chi_tiet": "git worktree", "ma": "git_worktree"}'),
     ["r01_worktree_that_bi_chan"]),
    ("m6c_khong_ghi_khi_probe_chan",
     ('        _ghi_so(run_root / sid, {', '        if False: _ghi_so(run_root / sid, {'),
     ["r01_worktree_that_bi_chan"]),
    ("m1_chan_ca_clone_that",
     ('            return {"trang_thai": "DAT", "chi_tiet": ".git la thu muc"}',
      '            return {"trang_thai": "DO", "chi_tiet": ".git la thu muc"}'),
     ["r02_clone_that_di_tiep"]),
    ("m2_bo_probe_ghi",
     ('        return {"trang_thai": "DO", "chi_tiet": f"ghi workspace: {type(e).__name__}"}',
      '        return {"trang_thai": "DAT", "chi_tiet": f"ghi workspace: {type(e).__name__}"}'),
     ["r03_probe_ghi_bi_tu_choi_thi_do"]),
    ("m3_chi_kiem_rc",
     ('    if p.returncode == 0 and bool(ra.strip()):', '    if p.returncode == 0:'),
     ["r04_spawn_rc0_dau_ra_rong_bi_chan"]),
    ("m4_thieu_khoa_coi_la_tin_cay",
     ('        return {"trang_thai": "KHONG_DO_DUOC", "chi_tiet": "thieu khoa trust Claude"}',
      '        return {"trang_thai": "DAT", "chi_tiet": "thieu khoa trust Claude"}'),
     ["r05_trust_thieu_khoa_la_khong_do_duoc"]),
    ("m4_bo_bat_JSON_hong",
     ('    except (OSError, TypeError, AttributeError, json.JSONDecodeError):',
      '    except (OSError, TypeError, AttributeError):'),
     ["r10_trust_json_hong_bi_chan_sach"]),
    ("m4_bool_nghiem_ngat_thanh_truthy_else",
     [('    if muc["hasTrustDialogAccepted"] is True:', '    if muc["hasTrustDialogAccepted"]:'),
      ('    if muc["hasTrustDialogAccepted"] is False:', '    else:')],
     ["r11_trust_gia_tri_that_ba_chieu"]),
    ("m4_non_bool_bi_coi_la_DAT",
     ('    return {"trang_thai": "KHONG_DO_DUOC", "chi_tiet": "trust Claude khong phai boolean"}',
      '    return {"trang_thai": "DAT", "chi_tiet": "trust Claude khong phai boolean"}'),
     ["r11_trust_gia_tri_that_ba_chieu"]),
    ("m5_canh_bao_thay_vi_chan",
     ('    if hong and ly_do is None:', '    if False and hong and ly_do is None:'),
     ["r06_probe_hong_khong_override_phai_chan"]),
    ("m5b_cho_bo_qua_khong-can-ly-do",
     ('    if bo_qua is not None and not ly_do:', '    if False and bo_qua is not None and not ly_do:'),
     ["r07_override_ly_do_rong_bi_tu_choi"]),
    ("m6_khong_ghi_so",
     ('    kq.update(probe=_probe_cho_so(probe), bo_qua_probe_ly_do=ly_do_bo_qua)',
      '    kq.update(probe=_probe_cho_so(probe), bo_qua_probe_ly_do=None)'),
     ["r08_override_co_ly_do_duoc_ghi_so"]),
    ("m6b_gop_khong_do_duoc_vao_dat",
     ('    return {ten: {"trang_thai": kq["trang_thai"], "chi_tiet": kq["chi_tiet"]}',
      '    return {ten: {"trang_thai": ("DAT" if kq["trang_thai"] == "KHONG_DO_DUOC" else kq["trang_thai"]), "chi_tiet": kq["chi_tiet"]}'),
     ["r09_run_json_giu_ba_trang_thai_probe"]),
    # Ca "rc=0 ma stdout RONG" duoc chan o BON cho doc lap: guard trong
    # _git_mot_dong, kiem SHA_RE trong chot_head, kiem `not top` trong chot_workspace,
    # va kiem `not ref` trong chot_ref. DA DO: bo RIENG bat ky cho nao cung KHONG ca nao chet -
    # ba chot phu len nhau. Chi khi bo CA BON thi t03 moi do. Ghi lai day vi
    # "dot bien song sot" o day KHONG phai test yeu, ma la phong thu nhieu lop.
    ("bo_kiem_rong_CA_BON_LOP",
     [('if not dong:\n        return (rc, "", "git thoat 0 nhung KHONG in gi")',
       'if not dong:\n        return (rc, "", "")'),
      ('if rc != 0 or not SHA_RE.match(sha):', 'if rc != 0:'),
      ('if rc != 0 or not top:', 'if rc != 0:'),
      ('if rc != 0 or not ref:', 'if rc != 0:')],
     ["t03_git_gia_thoat_0_im_lang_van_bi_chan"]),
    # --- Nam dot bien duoi day noi cac ca moi cua dot moi-truong vao bang, theo dung
    # muc cross-review neu: "ba ca t84/t85/t86 chua duoc noi vao DOT_BIEN, standard
    # suite van khoa hanh vi nhung chua duoc CUONG CHE tu dong". Kiem bang tay thi
    # dung mot lan roi tan; nam vao bang thi moi lan chay deu doi.
    #
    # `bo_hmac_tra_ve_sha256_tran` dung DOI chuoi: chi tra `_van_tay` ve sha256 tran
    # thi dau ra van khong chua digest (vi da bo truong `van_tay`), nen phai dung lai
    # CA HAI nua cua lo hong cu moi tai hien duoc oracle.
    ("bo_hmac_tra_ve_sha256_tran_va_xuat_lai_van_tay",
     [('return hmac.new(_KHOA_PHIEN, v.encode("utf-8", "replace"),\n'
       '                    hashlib.sha256).hexdigest()[:8]',
       'return hashlib.sha256(v.encode("utf-8", "replace")).hexdigest()[:8]'),
      ('"nhom": thuoc_nhom.get(t, ""),',
       '"nhom": thuoc_nhom.get(t, ""), "van_tay": _van_tay(os.environ.get(t, "")),')],
     ["t87_khong_duoc_xuat_digest_on_dinh_cua_gia_tri_bien"]),
    ("bo_loc_do_dai_va_ten_khi_gom_van_tay",
     ('        if v and len(v) >= NGUONG_DO_DAI_BI_MAT and _RE_BIEN_NHAY_CAM.search(t):',
      '        if v:'),
     ["t84_nhom_van_tay_khong_duoc_bat_oan_co_bat_tat"]),
    # PHAI doi CA HAI nua moi tai hien duoc lo hong cu, va do la mot ket qua DO chu
    # khong phai suy: ban dau chi doi phep kiem `rc` thi KHONG ca nao chet (giet 0/1).
    # Ly do: `_do_codex` co HAI lop doc lap — (a) lay MA THOAT lam chuan, (b) LOC dong
    # WARNING/NOTE/HINT truoc khi doc cau trang thai. Bo rieng lop (a) thi lop (b) van
    # dua "Not logged in" len dau danh sach nen phep kiem chu van bat duoc.
    # Giong y het tien le `bo_kiem_rong_CA_BON_LOP` o dau bang: "dot bien song sot"
    # KHONG phai test yeu, ma la phong thu nhieu lop — chi khi go DU ca hai lop moi
    # dung lai duoc dung cai bug fail-open cua ban nhap.
    ("do_codex_tin_DONG_DAU_thay_vi_ma_thoat",
     [('    if rc == 0 and "not logged in" not in ra.lower():',
       '    if "not logged in" not in (dong[0].lower() if dong else ""):'),
      ('    dong = [d.strip() for d in ra.splitlines() if d.strip()\n'
       '            and not d.strip().upper().startswith(("WARNING", "NOTE", "HINT"))]',
       '    dong = [d.strip() for d in ra.splitlines() if d.strip()]')],
     ["t85_do_codex_khong_duoc_fail_open_khi_dong_dau_la_canh_bao"]),
    # Hai dot bien: mot cho CHINH ham co chan, mot cho CUA `_do_codex_song`. Luot 9
    # bat dung chuyen chi mot trong hai cua doc co — nen phai co dot bien RIENG cho cua
    # thu hai, khong thi no lai am tham khong duoc kiem.
    # Ba dot bien cho ba finding cua bot review PR #128 nam trong launcher.py.
    ("claude_dem_ca_BIEN_RONG_la_credential",
     ('            and v.strip()]', '            ]'),
     ["t103_nam_finding_cua_bot_review_PR128"]),
    # NEO LAI: `gh-cli` khong con quyet dinh `DUNG_DUOC` (P1 PR "#143"), nen dot bien
    # cu — ep `gh-cli` luon True — khong con ca nao chet, tuc no da MAT RANG. Cua that
    # su quyet dinh nay la `gh-kho`; dot bien phai bam vao do.
    ("github_dem_CO_MAT_gh_la_da_xac_thuc",
     ('            duong.append(("gh-kho", pk.returncode == 0 and bool((pk.stdout or "").strip()),',
      '            duong.append(("gh-kho", True,'),
     # CHI khai `t111`: `t103` mo phong `subprocess.run` tra 0 cho MOI lenh, nen ep
     # `gh-kho` thanh True khong doi ket qua cua no. Khai mot ca KHONG THE chet cung
     # la mot loi khai sai ve do phu — runner bao `giet 1/2` chu khong im lang.
     ["t111_gh_da_xac_thuc_KHONG_phai_bang_chung_lam_duoc_viec"]),
    ("moc_refresh_MAT_DO_PHAN_GIAI",
     ('        moc = datetime.fromisoformat(last_refresh.strip().replace("Z", "+00:00"))',
      '        moc = datetime.fromisoformat(last_refresh.strip().replace("Z", "+00:00")'
      ').replace(minute=0, second=0, microsecond=0)'),
     ["t103_nam_finding_cua_bot_review_PR128"]),
    ("co_chan_codex_luon_tra_KHONG_BI_CHAN",
     ('    if not co.exists():\n        return None', '    if True:\n        return None'),
     ["t102_khong_go_duoc_policy_thi_phai_CHAN_codex"]),
    ("do_codex_song_bo_qua_co_chan",
     ('    bi_chan = _co_chan_codex()\n    if bi_chan:\n'
      '        # Đây là cửa THẬT SỰ chạy `codex exec`. Bản trước bỏ sót đúng cửa này.\n'
      '        return (False, bi_chan)',
      '    bi_chan = None'),
     ["t102_khong_go_duoc_policy_thi_phai_CHAN_codex"]),
    # Hai dot bien duoi day khoa hai P1 cua cross-review luot 6.
    ("chot_truong_nhom_FAIL_OPEN_khi_khong_do_duoc_pgid",
     ('    dung_killpg = nhom_that == pid          # CHỈ True khi ĐO ĐƯỢC và bằng nhau',
      '    dung_killpg = True'),
     ["t92_khong_duoc_killpg_khi_pid_KHONG_phai_truong_nhom"]),
    ("ok_kha_dung_bo_qua_muc_CHUA_CHUNG_MINH",
     [('        elif tt not in DA_CHUNG_MINH_KHA_DUNG:\n'
       '            chua_chung_minh.append(k["ten"])',
       '        elif False:\n'
       '            chua_chung_minh.append(k["ten"])')],
     ["t98_CO_CREDENTIAL_khong_duoc_thanh_kha_dung_o_tang_doctor"]),
    ("chuan_bi_bo_duong_JSON_tho",
     ('            for method in ("base64", "JSON thô"):',
      '            for method in ("base64",):'),
     ["t86_chuan_bi_nhan_ca_base64_lan_json_tho_va_tu_choi_rac"]),
    ("hook_phien_bo_phep_so_nang_luc",
     ('    thieu = sorted(cua_master - dang_co)',
      '    thieu = []'),
     ["t88_hook_phien_do_theo_NANG_LUC_khong_theo_bam_toan_tep"]),
    # KHONG co dot bien cho `_co_lap_toan_cuc`, va day la GIOI HAN CUA BANG NAY chu
    # khong phai so sot. Runner doc `goc = LAUNCHER.read_text()` — no chi dot bien
    # `launcher.py`. Chot co lap song trong `launcher_test.py`, tuc NGOAI tam voi.
    # Da thu dat hai muc vao day: ca hai tra "khong tim thay doan de dot bien", va
    # mot muc do THUONG TRUC la thu se bi bo qua — dung benh ma chinh dot review nay
    # dang chua. Nen bo han, ghi ly do o day.
    # `t89` tu chung minh bang khang dinh truc tiep (ke ca duong NEM NGOAI LE giua
    # chung), cong phan chung tay: go chot co lap thi `t81` lam ban `subprocess.run`
    # ngay tu ca dau tien.
    # Chot nay nam trong launcher.py nen DOT BIEN DUOC (khac chot harness o launcher_test).
    # Dot bien vao HANG SO, khong vao mot cho dung: `_TOKEN_KHONG_XET_HAN` duoc doc o
    # CA HAI lop (thu thap + quyet dinh), nen rong hoa no la go DU ca hai — dung thu
    # can do. Bam vao mot dong `if` chi go duoc mot lop.
    ("lay_ca_id_token_lam_tin_hieu_han",
     ('_TOKEN_KHONG_XET_HAN = frozenset({"id_token"})',
      '_TOKEN_KHONG_XET_HAN = frozenset()'),
     ["t94_canh_bao_TRUOC_khi_credential_het_han"]),
    ("kiem_song_bi_canh_bao_nuot",
     ('            if kiem_song:\n'
      '                song, ly_do = _do_codex_song(duong_dan=duong_codex)',
      '            if False:\n'
      '                song, ly_do = _do_codex_song(duong_dan=duong_codex)'),
     ["t96_kiem_song_phai_chay_KE_CA_khi_sap_het_han"]),
    ("bo_canh_bao_som_theo_exp",
     ('        sap = [f"{t}={g}h" for t, g in sorted(han["gio_con_lai"].items())\n'
      '               if 0 < g <= NGUONG_CANH_BAO_GIO and t not in _TOKEN_KHONG_XET_HAN]',
      '        sap = []'),
     ["t94_canh_bao_TRUOC_khi_credential_het_han"]),
    ("bo_canh_bao_theo_tuoi_anh_chup",
     ('        anh_cu = tuoi is not None and tuoi >= NGUONG_ANH_CHUP_CU_GIO',
      '        anh_cu = False'),
     ["t94_canh_bao_TRUOC_khi_credential_het_han"]),
    ("nang_nhan_CO_CREDENTIAL_thanh_DUNG_DUOC",
     ('            return ("CO_CREDENTIAL",',
      '            return ("DUNG_DUOC",'),
     ["t93_do_codex_khong_duoc_nang_nhan_vuot_qua_bang_chung"]),
    ("bo_kiem_han_token_codex",
     ('        if het:', '        if False:'),
     ["t93_do_codex_khong_duoc_nang_nhan_vuot_qua_bang_chung"]),
    ("bo_chot_truong_nhom_truoc_killpg",
     ('    if nhom_that is not None and nhom_that != pid:',
      '    if False:'),
     ["t92_khong_duoc_killpg_khi_pid_KHONG_phai_truong_nhom"]),
    ("bo_kiem_prompt_rong",
     ('if not b.strip():\n        raise Chan(MA_PROMPT, f"tep prompt RONG: {p}")',
      'if False:\n        raise Chan(MA_PROMPT, f"tep prompt RONG: {p}")'),
     ["t15_prompt_rong_bi_chan_du_sha_dung"]),
    # Neo chuyển từ `if _khoa_danh_tinh(pid) != khoa:` sang `elif hien != khoa:`
    # khi _giet_cay tách "đã chết" khỏi "PID tái dùng" (vòng 3 đợt 2). Ý định
    # KHÔNG đổi: bỏ chốt khoá ⇒ giết liều theo PID trần.
    ("giet_lieu_khong_can_khoa",
     ('    elif hien != khoa:', '    elif False:'),
     ["t31_stop_tu_choi_khi_khoa_danh_tinh_khac"]),
    # DA DO bang git that: `-uall` so voi mac dinh (`normal`) KHONG doi sach/ban,
    # chi doi do chi tiet liet ke (`?? thumuc/` thay vi tung tep). Chi `-uno` moi
    # lam chot MU. Dot bien dau tien cua toi nham vao `-uall` nen song sot - do la
    # dot bien sai, khong phai ma sai.
    # Neo chuyển khi lenh_stop tách 10 (TỪ CHỐI) khỏi 125 (giết chưa trọn vẹn).
    # Ý định KHÔNG đổi: stop báo thành công dù chưa giết được gì.
    ("bao_da_giet_du_chua_giet",
     ('    if ket.tron_ven:\n        return MA_OK', '    if True:\n        return MA_OK'),
     ["t31_stop_tu_choi_khi_khoa_danh_tinh_khac"]),
    # Giao thuc giet bang CHUOI la nguyen nhan goc cua loi 124-khi-chau-con-song.
    # Dot bien nay dung lai dung no: coi "me chet" la du, bo qua ca_cay.
    ("124_khi_chau_con_song",
     ('                ma = MA_QUA_HAN if ket_giet.tron_ven else MA_GIET_HUT',
      '                ma = MA_QUA_HAN if ket_giet.me_da_chet else MA_GIET_HUT'),
     ["t62_qua_han_ma_khong_giet_het_cay_phai_tra_125"],
     ("posix", "KHONG DUNG DUOC tren ca hai nen, va da DO chu khong doan: t62 nay dung "
               "fixture MO COI - ca kho nhat dung duoc - the ma Job Object van giet duoc "
               "chau, nen nhanh 'chau con song' khong the cham toi. Dot bien nay chi song "
               "lai khi ai do dung duoc mot ca ma duong giet THAT BAI that su.")),
    ("khong_cat_thong_tin_dang_nhap",
     ("(?:[^@/]*@)?", "(?:)?"),
     ["t45_token_trong_URL_KHONG_duoc_lo_ra"]),
    # Khoi phuc DUNG hanh vi truoc khi va: so hau to. Mot dot bien nay dung lai ca
    # ba lo (gia mao host co dau cham, host khong dau cham, expected mot doan) - vi
    # ca ba deu la HE QUA cua cung mot quyet dinh sai.
    ("quay_ve_so_hau_to",
     ('    doan_m = m.split("/")',
      '    return t == m or t.endswith("/" + m)\n    doan_m = m.split("/")'),
     ["t48_host_gia_mao_KHONG_duoc_khop",
      "t57_host_KHONG_co_dau_cham_van_phai_chan",
      "t58_expected_repo_mot_doan_bi_TU_CHOI"]),
    ("so_URL_tho_khong_chuan_hoa",
     ('    doan_m = m.split("/")', '    return t == m\n    doan_m = m.split("/")'),
     ["t44_bon_cach_viet_URL_cung_mot_danh_tinh",
      "t40_HAI_BAN_CLONE_hai_duong_dan_CUNG_danh_tinh"]),
    ("lay_cwd_thay_vi_goc_repo",
     ('    goc = chi_dinh or os.environ.get("TL_WORKSPACE") or os.getcwd()\n    return chot_workspace(goc)',
      '    goc = chi_dinh or os.environ.get("TL_WORKSPACE") or os.getcwd()\n'
      '    chot_workspace(goc)\n    return str(Path(goc).resolve())'),
     ["t38_dung_o_thu_muc_CON_van_ra_GOC"]),
    ("khong_remote_thi_coi_la_khop",
     ("        if not khop:", "        if not khop and remotes:"),
     ["t42_khong_co_remote_van_bi_chan_khi_doi_kho"]),
    ("bo_cung_hoa_dau_ra",
     ('    for luong in (sys.stdout, sys.stderr):',
      '    for luong in ():'),
     ["t47_console_khong_UTF8_van_in_duoc_duong_dan_co_dau"]),
    ("de_len_quyet_dinh_cua_stop",
     ('    if so_moi.get("trang_thai") == "da_dung":', '    if False:'),
     ["t50_stop_roi_runner_KHONG_duoc_de_len_so"]),
    ("so_hong_im_lang",
     ('    return MA_THAM_SO if hong else MA_OK', '    return MA_OK'),
     ["t52_so_hong_KHONG_duoc_im_lang"]),
    ("doctor_luon_xanh",
     ('        elif bb and (thay is None or xac_thuc_ok is False or bi_che):',
      '        elif False:'),
     ["t54_doctor_thieu_cong_cu_bat_buoc_thi_DO"]),
    # Chiều hẹp hơn: giữ phép kiểm CÓ MẶT, bỏ riêng phép kiểm XÁC THỰC. Bản cũ chỉ
    # có một đột biến "luôn xanh", nên nếu ai lỡ tay bỏ vế `xac_thuc_ok` thì không
    # mutant nào đỏ — cửa mới mà không có mutant riêng là cửa sẽ âm thầm hở lại.
    ("doctor_bo_qua_auth_hong",
     ('        elif bb and (thay is None or xac_thuc_ok is False or bi_che):',
      '        elif bb and (thay is None or bi_che):'),
     ["t105_doctor_auth_hong_thi_DO_du_binary_chay_duoc"]),
    ("khong_chup_prompt",
     ('        if any("{PROMPT_FILE}" in x for x in lenh_con):',
      '        if False:'),
     ["t56_prompt_doi_sau_khi_kiem_KHONG_toi_duoc_con",
      "r16_consumer_doc_dung_byte_va_trao_snapshot_cung_co_phai_DO"]),
    ("prompt_sau_preflight_khong_rehash",
     ('        if hashlib.sha256(b).hexdigest() != kq["prompt_sha256"]:',
      '        if False:'),
     ["r12_prompt_doi_ngay_sau_preflight_phai_DO"]),
    ("bam_output_luon_lay_chuoi_rong",
     ('                for khoi in iter(lambda: f.read(1024 * 1024), b""):',
      '                for khoi in ():'),
     ["r14_run_json_bam_lai_dung_hai_log"]),
    ("mot_provider_hai_transport",
     ('    ("anthropic_claude", ("claude",), "claude_code", "machine/local"),',
      '    ("openai_codex", ("claude",), "claude_code", "machine/local"),'),
     ["r15_moi_provider_chi_mot_transport_va_hai_luot_on_dinh"]),
    ("luu_argv_nguyen_van",
     ('"ten": a.name, "lenh": _tom_tat_lenh(a.lenh), "trang_thai": "dang_chay",',
      '"ten": a.name, "lenh": [str(x) for x in a.lenh], "trang_thai": "dang_chay",'),
     ["t59_so_KHONG_luu_doi_so_nguyen_van"]),
    ("doctor_tin_which",
     ('            chay_duoc, pb, qua_han = _phien_ban(d, env=moi_truong,\n'
      '                                                timeout=min(PROBE_TIMEOUT_GIAY, con_lai))',
      '            chay_duoc, pb, qua_han = True, "", False'),
     ["t60_doctor_KHONG_tin_which_khi_cong_cu_khong_chay_duoc"]),
    # Dừng ở binary ĐẦU TIÊN trong PATH = đúng hành vi `shutil.which` cũ, tức dựng
    # lại lỗi đã đo trên Windows (rg của WindowsApps che mất bản chạy được).
    ("doctor_chi_thu_binary_dau",
     ('        for ten_uv, d in ung_vien:', '        for ten_uv, d in ung_vien[:1]:'),
     ["t106_doctor_binary_hong_dau_PATH_khong_duoc_che_binary_tot"]),
    # Lấy credential theo THỨ TỰ TÀI LIỆU thay vì loại chuỗi giữ chỗ => chọn đúng
    # bản giữ chỗ 14 ký tự trong container này. Xem `_doc_moi_truong`.
    ("moi_truong_tin_gh_token_giu_cho",
     ('        if _van_tay(v) in van_tay_ngoai:', '        if False:'),
     ["t107_doc_moi_truong_KHONG_duoc_chon_bien_giu_cho"]),
    # Quay lại MOT bool chung cho moi nen => remote lai doi `gh`, tuc fail-close
    # tren thu ma nen ay khong the co.
    ("bat_buoc_bo_qua_nen",
     ('    if moi_truong.get("CLAUDE_CODE_REMOTE", "") == "true":\n'
      '        return bool(bb["remote"])\n'
      '    return bool(bb["mac_dinh"])',
      '    return bool(bb["mac_dinh"])'),
     ["t109_bat_buoc_giai_THEO_NEN_khong_phai_mot_bool_chung"]),
    # Bo nen CI => `doctor` doi chuoi cong cu agent tren runner, roi TAT luon phep do.
    ("bat_buoc_bo_qua_nen_ci",
     ('    if moi_truong.get("GITHUB_ACTIONS") == "true" or moi_truong.get("CI") == "true":\n'
      '        return bool(bb.get("ci", bb["mac_dinh"]))\n',
      ''),
     ["t109_bat_buoc_giai_THEO_NEN_khong_phai_mot_bool_chung"]),
    # Phan loai REST bang MA TRANG THAI thay vi HEADER => 403 cua proxy bi doc
    # thanh "GitHub tu choi", va 4xx that cua GitHub bi doc thanh "proxy chan".
    ("rest_phan_loai_theo_ma_trang_thai",
     ('        co_gh = any(k.lower().startswith("x-github") for k in e.headers)\n'
      '        # 4xx CÓ header GitHub = TỚI NƠI nhưng THAO TÁC HỎNG.',
      '        co_gh = e.code < 400\n'
      '        # 4xx CÓ header GitHub = TỚI NƠI nhưng THAO TÁC HỎNG.'),
     ["t110_rest_github_phan_loai_theo_HEADER_khong_theo_MA_TRANG_THAI"]),
    # Gop "khong do duoc" vao "chan" — dung loi `None != False` kho da ghi so.
    # Dem `gh auth status` la duong lam duoc viec => lan thu BA cung mot hinh dang.
    ("github_dem_gh_auth_la_lam_duoc_viec",
     ('    LAM_DUOC_VIEC = {"git", "gh-kho", "rest-kho"}',
      '    LAM_DUOC_VIEC = {"git", "gh-cli", "rest-kho"}'),
     ["t111_gh_da_xac_thuc_KHONG_phai_bang_chung_lam_duoc_viec"]),
    # Quay ve mot con so chon tay: bang lon len ma tran dung yen => cong cu cuoi
    # bang bi bao thieu vi HET NGAN SACH chu khong vi no hong.
    ("tran_tong_chon_tay",
     ('    return max(30.0, PROBE_TIMEOUT_GIAY * so_probe + 30.0)',
      '    return 120.0'),
     ["t112_tran_tong_suy_tu_SO_PROBE_va_het_ngan_sach_KHONG_phai_hong"]),
    # Het ngan sach bi dan nhan "cong cu hong" — dung cai nhan sai dot nay di sua.
    ("het_ngan_sach_thanh_cong_cu_hong",
     ('                het_ngan_sach = {"goi_bang": ten_uv, "duong_dan": d,',
      '                co_mat_nhung_hong = {"goi_bang": ten_uv, "duong_dan": d,'),
     ["t112_tran_tong_suy_tu_SO_PROBE_va_het_ngan_sach_KHONG_phai_hong"]),
    # Khong noi credential da chuan hoa vao probe => van di bang chuoi giu cho.
    # Khoi kha dung chay ngoai tran => tran chi phu nua luot chay.
    ("kha_dung_chay_ngoai_tran",
     ('        if time.monotonic() >= het_han:', '        if False:'),
     ["t114_ngan_sach_phu_CA_khoi_kha_dung_va_khong_thanh_THIEU"]),
    # Het ngan sach lai roi vao `thieu_bat_buoc` — doi ten cho hong ma giu ket luan.
    ("het_ngan_sach_van_thanh_thieu",
     ('        if bb and thay is None and (het_ngan_sach is not None\n'
      '                                    or qua_han_probe is not None):',
      '        if False:'),
     ["t114_ngan_sach_phu_CA_khoi_kha_dung_va_khong_thanh_THIEU"]),
    # --- PLAT-M3 (#185): nguồn chớp của t53. Đột biến ĐẦU TIÊN dựng lại ĐÚNG hành
    # vi cũ — probe quá hạn bị đếm là THIẾU ⇒ doctor 12 rồi 0 — và phải làm ca đích
    # ĐỎ: đây là phản chứng "tái tạo nguồn chớp" mà tiêu chí nghiệm thu packet đòi.
    # (Cùng mỏ neo với `het_ngan_sach_van_thanh_thieu` nhưng thay bằng nhánh HẸP hơn:
    # giữ nhánh hết-ngân-sách, chỉ bỏ vế quá-hạn — nên t114 vẫn xanh, t129 phải đỏ.)
    ("probe_qua_han_dem_la_THIEU",
     ('        if bb and thay is None and (het_ngan_sach is not None\n'
      '                                    or qua_han_probe is not None):',
      '        if bb and thay is None and het_ngan_sach is not None:'),
     ["t129_probe_qua_han_la_CHUA_DO_khong_phai_THIEU"]),
    ("probe_khong_retry_khi_qua_han",
     ('                con_lai = het_han - time.monotonic()\n'
      '                if con_lai > 0:\n'
      '                    chay_duoc, pb2, qua_han = _phien_ban(',
      '                con_lai = het_han - time.monotonic()\n'
      '                if False:\n'
      '                    chay_duoc, pb2, qua_han = _phien_ban('),
     ["t130_qua_han_luot_dau_retry_thanh_cong_van_la_CO"]),
    # Tầng PHÁT HIỆN: nuốt cờ `qua_han` ngay tại chỗ TimeoutExpired — hai hàm hai
    # đột biến vì thông điệp cố ý khác chữ (mỗi mỏ neo khớp đúng một chỗ).
    ("phien_ban_timeout_khong_mang_co_qua_han",
     ('        return (False, f"timeout sau {timeout:.1f}s", True)',
      '        return (False, f"timeout sau {timeout:.1f}s", False)'),
     ["t135_phien_ban_va_xac_thuc_bao_qua_han_bang_CO_KIEU"]),
    ("xac_thuc_timeout_khong_mang_co_qua_han",
     ('        return (False, f"probe xac thuc timeout sau {timeout:.1f}s", True, "")',
      '        return (False, f"probe xac thuc timeout sau {timeout:.1f}s", False, "")'),
     ["t135_phien_ban_va_xac_thuc_bao_qua_han_bang_CO_KIEU"]),
    # Đường chớp thứ hai: auth quá hạn quay lại là `xac_thuc_ok=False` ⇒ THIẾU.
    ("xac_thuc_qua_han_van_la_THIEU",
     ('                    if not xac_thuc_ok and xt_qua_han:\n'
      '                        # `None ≠ False`: quá hạn cả hai lượt là CHƯA ĐO ĐƯỢC,\n'
      '                        # không phải "xác thực sai".\n'
      '                        xac_thuc_ok = None',
      '                    if False:\n'
      '                        # `None ≠ False`: quá hạn cả hai lượt là CHƯA ĐO ĐƯỢC,\n'
      '                        # không phải "xác thực sai".\n'
      '                        xac_thuc_ok = None'),
     ["t132_xac_thuc_qua_han_la_CHUA_DO_khong_phai_THIEU"]),
    # Gỡ vế fail-closed: `--doi-kha-dung` lặng lẽ coi "chưa đo được" là đủ.
    ("doi_kha_dung_bo_qua_CHUA_DO",
     ('                          chua_chung_minh + chua_do_bat_buoc)',
      '                          chua_chung_minh)'),
     ["t129_probe_qua_han_la_CHUA_DO_khong_phai_THIEU"]),
    # --- PLAT-M3-R (#196): các mutant hậu kiểm từng sống sót nay phải chết.
    ("auth_het_ngan_sach_khong_vao_chua_do",
     ('                xac_thuc_ok, loi_xac_thuc = None, "doctor het ngan sach"\n'
      '                xac_thuc_chua_do = loi_xac_thuc',
      '                xac_thuc_ok, loi_xac_thuc = None, "doctor het ngan sach"'),
     ["t138_auth_het_ngan_sach_phai_vao_CHUA_DO"]),
    ("qua_han_uu_tien_dung_lai_break",
     ('                qua_han_probe = {"goi_bang": ten_uv, "duong_dan": d,\n'
      '                                 "ly_do": f"probe --version QUA HAN, chua do duoc: {pb}"}\n'
      '                continue',
      '                qua_han_probe = {"goi_bang": ten_uv, "duong_dan": d,\n'
      '                                 "ly_do": f"probe --version QUA HAN, chua do duoc: {pb}"}\n'
      '                break'),
     ["t139_ung_vien_qua_han_khong_duoc_che_ung_vien_tot"]),
    ("review_codex_auth_timeout_mat_dau_chua_do",
     ('                        xac_thuc_chua_do = f"probe xac thuc QUA HAN, chua do duoc: {loi_xac_thuc}"',
      '                        xac_thuc_chua_do = None'),
     ["t132_xac_thuc_qua_han_la_CHUA_DO_khong_phai_THIEU"]),
    ("review_codex_retry_version_gap_ba",
     ('                        d, env=moi_truong,\n'
      '                        timeout=min(2 * PROBE_TIMEOUT_GIAY, con_lai))',
      '                        d, env=moi_truong,\n'
      '                        timeout=min(3 * PROBE_TIMEOUT_GIAY, con_lai))'),
     ["t130_qua_han_luot_dau_retry_thanh_cong_van_la_CO"]),
    ("review_codex_retry_auth_gap_ba",
     ('                            timeout=min(2 * PROBE_TIMEOUT_GIAY, con_lai))',
      '                            timeout=min(3 * PROBE_TIMEOUT_GIAY, con_lai))'),
     ["t132_xac_thuc_qua_han_la_CHUA_DO_khong_phai_THIEU"]),
    ("review_codex_retry_version_giu_loi_luot_mot",
     ('                    pb = pb2 if chay_duoc else f"luot 1: {pb} · luot 2: {pb2}"',
      '                    pb = pb if chay_duoc else f"luot 1: {pb} · luot 2: {pb2}"'),
     ["t130_qua_han_luot_dau_retry_thanh_cong_van_la_CO"]),
    ("review_same_provider_retry_bo_qua_ngan_sach",
     ('                con_lai = het_han - time.monotonic()\n'
      '                if con_lai > 0:\n'
      '                    chay_duoc, pb2, qua_han = _phien_ban(',
      '                con_lai = het_han - time.monotonic()\n'
      '                if True:\n'
      '                    chay_duoc, pb2, qua_han = _phien_ban('),
     ["t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho"]),
    ("doctor_text_gop_CHUA_DO_thanh_THIEU",
     ('            dau = ("BI_CHE" if che else "CHUA_DO" if ly_do_chua_do else',
      '            dau = ("BI_CHE" if che else "THIEU" if ly_do_chua_do else'),
     ["t140_doctor_text_tach_CHUA_DO_khoi_THIEU_va_DU"]),
    ("doctor_text_auth_None_khong_in_ly_do",
     ('            elif xac_thuc_chua_do and con_ong:',
      '            elif False:'),
     ["t140_doctor_text_tach_CHUA_DO_khoi_THIEU_va_DU"]),
    ("doctor_text_footer_khoa_cung_het_ngan_sach",
     ('            _in_an_toan("CHUA DO DUOC: "',
      '            _in_an_toan("CHUA DO DUOC (het ngan sach, KHONG phai thieu): "'),
     ["t140_doctor_text_tach_CHUA_DO_khoi_THIEU_va_DU"]),
    ("doctor_text_CHUA_DO_van_ket_luan_DU",
     ('        elif chua_do_bat_buoc:\n'
      '            ket_luan = "CHUA DO DUOC " + ", ".join(chua_do_bat_buoc)',
      '        elif False:\n'
      '            ket_luan = "CHUA DO DUOC " + ", ".join(chua_do_bat_buoc)'),
     ["t140_doctor_text_tach_CHUA_DO_khoi_THIEU_va_DU"]),
    ("comment_timeout_mat_idiom_version_va_phep_do",
     ('                # v1.3.0 (#185 + phép đo 12→0) — nguồn chớp của `t53`; vá tất định.',
      '                # NGUON CHOP CUA t53.'),
     ["t141_comment_timeout_phai_co_version_nguon_va_phep_do"]),
    # Bug B (đo 19-08-2026, Windows): spawn tên trần "codex" — hai cửa, hai đột biến.
    ("codex_live_callsite_sap_het_han_truyen_ten_tran",
     ('                song, ly_do = _do_codex_song(duong_dan=duong_codex)',
      '                song, ly_do = _do_codex_song(duong_dan="codex")'),
     ["t133_do_codex_spawn_bang_duong_dan_da_resolve_khong_ten_tran"]),
    ("codex_live_callsite_binh_thuong_truyen_ten_tran",
     ('        song, vi_sao = _do_codex_song(duong_dan=duong_codex)',
      '        song, vi_sao = _do_codex_song(duong_dan="codex")'),
     ["t133_do_codex_spawn_bang_duong_dan_da_resolve_khong_ten_tran"]),
    ("do_codex_spawn_ten_tran",
     ('        p = _chay_probe_nhu_shell([duong_codex, "login", "status"], capture_output=True,',
      '        p = _chay_probe_nhu_shell(["codex", "login", "status"], capture_output=True,'),
     ["t133_do_codex_spawn_bang_duong_dan_da_resolve_khong_ten_tran"]),
    ("do_codex_song_spawn_ten_tran",
     ('            probe.__globals__["_co_codex"] = lambda: duong_dan',
      '            probe.__globals__["_co_codex"] = lambda: "codex"'),
     ["t133_do_codex_spawn_bang_duong_dan_da_resolve_khong_ten_tran"]),
    ("footer_van_khuyen_bat_kiem_song",
     ('            if getattr(a, "kiem_song", False):\n'
      '                _in_an_toan("                 --kiem-song DA chay ma van chua co bang "\n'
      '                            "chung — xem chi tiet tung muc o tren")',
      '            if False:\n'
      '                _in_an_toan("                 --kiem-song DA chay ma van chua co bang "\n'
      '                            "chung — xem chi tiet tung muc o tren")'),
     ["t134_kiem_song_dang_bat_thi_footer_khong_khuyen_bat_lai"]),
    # --- Review vòng 1 (same_provider, Fable 5 max) tự nghĩ 5 đột biến, 3 SỐNG SÓT
    # ⇒ 3 finding P3. Năm mục dưới đây nối các mutant ấy vào bảng — kiểm bằng tay thì
    # dùng một lần rồi tàn; nằm vào bảng thì mỗi lần chạy đều đòi (đúng tiền lệ t84-t86).
    # `auth_hong_that_sau_retry…`: nuốt điều kiện `xt_qua_han` ở kiểm tra SAU retry —
    # auth hỏng thật đo được ở lượt 2 bị đọc thành "chưa đo" (fail-open có tiền đề).
    # Cùng mỏ neo với `xac_thuc_qua_han_van_la_THIEU` nhưng thay HẸP hơn (giữ nhánh,
    # chỉ nới điều kiện) nên cần ca t136 mới giết được.
    ("auth_hong_that_sau_retry_thanh_chua_do",
     ('                    if not xac_thuc_ok and xt_qua_han:\n'
      '                        # `None ≠ False`: quá hạn cả hai lượt là CHƯA ĐO ĐƯỢC,\n'
      '                        # không phải "xác thực sai".\n'
      '                        xac_thuc_ok = None',
      '                    if not xac_thuc_ok:\n'
      '                        # `None ≠ False`: quá hạn cả hai lượt là CHƯA ĐO ĐƯỢC,\n'
      '                        # không phải "xác thực sai".\n'
      '                        xac_thuc_ok = None'),
     ["t136_qua_han_roi_hong_that_o_luot_retry_van_la_THIEU"]),
    ("vut_co_qua_han_cua_luot_retry",
     ('                    chay_duoc, pb2, qua_han = _phien_ban(\n'
      '                        d, env=moi_truong,\n'
      '                        timeout=min(2 * PROBE_TIMEOUT_GIAY, con_lai))',
      '                    chay_duoc, pb2, qua_han_2 = _phien_ban(\n'
      '                        d, env=moi_truong,\n'
      '                        timeout=min(2 * PROBE_TIMEOUT_GIAY, con_lai))'),
     ["t136_qua_han_roi_hong_that_o_luot_retry_van_la_THIEU"]),
    # Hỗn hợp ứng viên: cho "hỏng thật" THẮNG "quá hạn" — dựng lại đúng cấu hình sẽ
    # chớp 12/0 theo giờ (binary hỏng đứng trước + binary chậm đứng sau).
    ("hong_that_thang_qua_han",
     ('        if bb and thay is None and (het_ngan_sach is not None\n'
      '                                    or qua_han_probe is not None):',
      '        if bb and thay is None and co_mat_nhung_hong is None and (het_ngan_sach is not None\n'
      '                                    or qua_han_probe is not None):'),
     ["t137_ung_vien_hong_that_cong_ung_vien_qua_han_la_CHUA_DO"]),
    # Hệ số GẤP ĐÔI của retry — hai phía, hai mỏ neo (indent khác nhau nên khớp đúng
    # một chỗ mỗi mục). Mutant không phá tất định, chỉ đánh rơi tham số chất lượng —
    # đúng phân tích của reviewer; ca đo QUAN HỆ hai lượt nên giết được.
    ("retry_van_cung_han",
     ('                        d, env=moi_truong,\n'
      '                        timeout=min(2 * PROBE_TIMEOUT_GIAY, con_lai))',
      '                        d, env=moi_truong,\n'
      '                        timeout=min(PROBE_TIMEOUT_GIAY, con_lai))'),
     ["t130_qua_han_luot_dau_retry_thanh_cong_van_la_CO"]),
    ("retry_auth_van_cung_han",
     ('                            thay["duong_dan"], c["xac_thuc"], env=moi_truong,\n'
      '                            timeout=min(2 * PROBE_TIMEOUT_GIAY, con_lai))',
      '                            thay["duong_dan"], c["xac_thuc"], env=moi_truong,\n'
      '                            timeout=min(PROBE_TIMEOUT_GIAY, con_lai))'),
     ["t132_xac_thuc_qua_han_la_CHUA_DO_khong_phai_THIEU"]),
    ("probe_github_bo_qua_moi_truong_chuan_hoa",
     ('    if moi_truong is None:\n        moi_truong = _MOI_TRUONG_DA_DOC',
      '    if True:\n        moi_truong = dict(os.environ)'),
     ["t113_probe_github_phai_nhan_credential_DA_CHUAN_HOA"]),
    ("rest_gop_khong_do_duoc_vao_chan",
     ('        return ("khong_do_duoc", f"{type(e).__name__}", False)',
      '        return ("chan", f"{type(e).__name__}", False)'),
     ["t110_rest_github_phan_loai_theo_HEADER_khong_theo_MA_TRANG_THAI"]),
    # Coi "toi duoc" la "lam duoc viec": 404 kho rieng tu se thanh bang chung xanh.
    ("rest_toi_duoc_la_lam_duoc_viec",
     ('                False)\n    except Exception as e:',
      '                True)\n    except Exception as e:'),
     # CHI `t110`: `t111` thay han `_do_rest_github` bang ban gia, nen dot bien vao
     # ban that khong toi duoc no.
     ["t110_rest_github_phan_loai_theo_HEADER_khong_theo_MA_TRANG_THAI"]),
    ("worktree_bo_qua_tep_moi",
     ('"--untracked-files=all"', '"--untracked-files=no"'),
     ["t12_tep_khong_theo_doi_van_tinh_la_ban"]),
    # --- vòng 3: ba lỗi CHẶN. Mỗi đột biến dựng lại ĐÚNG hành vi của bản cũ.
    # Nhóm luôn "rỗng" = đúng lời nói dối cũ: mẹ chết thì coi như cả cây chết,
    # nên SIGKILL không bao giờ được gửi và cháu phớt lờ SIGTERM sống tiếp.
    # Đúng lời nói dối của bản cũ: mẹ chết thì coi như cả cây chết, nên SIGKILL
    # không bao giờ được gửi.
    # CHỈ giết t63, KHÔNG giết t66 — đã đo: cháu của t66 không phớt lờ SIGTERM
    # nên `_giet_rieng` hạ nó ngay ở phát đầu, cây SẠCH THẬT và 124 là trung
    # thực. Đột biến sai chỗ ≠ mã sai; t66 do `khong_chup_cay` phủ.
    ("me_chet_la_coi_nhu_ca_cay_chet",
     ("        con = _con_lai()\n        if con is None:",
      "        con = set() if not _con_song(pid) else _con_lai()\n        if con is None:"),
     ["t63_chau_phot_lo_SIGTERM_ma_bao_da_giet_ca_cay_la_noi_doi"]),
    # Bỏ lớp đếm THÀNH VIÊN NHÓM -> chỉ còn ảnh chụp, nên cháu sinh SAU lúc chụp
    # không ai đếm. (t63/t66 vẫn sống nhờ ảnh chụp: hai lớp phủ hai ca khác nhau,
    # cùng doctrine với bo_kiem_rong_CA_BON_LOP — đột biến sai chỗ ≠ mã sai.)
    ("nhom_luon_rong",
     ("def _thanh_vien_nhom(pgid: int) -> list[int] | None:\n    \"\"\"PID còn SỐNG",
      "def _thanh_vien_nhom(pgid: int) -> list[int] | None:\n    return []\n    \"\"\"PID còn SỐNG"),
     ["t67_chau_sinh_SAU_luc_chup_van_phai_bi_dem"]),
    # Bỏ ảnh chụp cây -> chỉ còn bằng chứng theo NHÓM, nên kẻ đã setsid() vừa
    # không bị giết vừa không bị đếm: đúng bản vá NỬA VỜI đầu tiên của vòng 3.
    ("khong_chup_cay",
     ("def _chup_cay(pid: int) -> dict[int, str] | None:\n    \"\"\"Ảnh chụp",
      "def _chup_cay(pid: int) -> dict[int, str] | None:\n    return {}\n    \"\"\"Ảnh chụp"),
     ["t66_chau_setsid_roi_khoi_nhom_van_phai_bi_giet"]),
    # Trả rid vào TÊN thư mục = đúng bản cũ: mkdir hết là hành vi giành short_id,
    # hai lượt cùng sid lại cùng tồn tại được.
    ("rid_quay_lai_ten_thu_muc",
     [("        thu_muc = run_root / sid\n        try:\n            thu_muc.mkdir(parents=False)",
       "        thu_muc = run_root / f\"{sid}-{rid}\"\n        try:\n            thu_muc.mkdir(parents=False)"),
      ("    thu_muc = run_root / sid       # tên = short_id: xem `_cap_id`",
       "    thu_muc = run_root / f\"{sid}-{rid}\"")],
     ["t64_short_id_da_bi_GIANH_thi_khong_duoc_cap_lai"]),
    # Bỏ resolve() -> bản chụp đi tới con dưới dạng đường dẫn tương đối theo cwd
    # của LAUNCHER, con đọc theo cwd của NÓ.
    ("run_root_khong_resolve",
     ("    run_root = Path(a.run_root).expanduser().resolve()\n    rid, sid = _cap_id(run_root)",
      "    run_root = Path(a.run_root).expanduser()\n    rid, sid = _cap_id(run_root)"),
     ["t65_run_root_TUONG_DOI_van_giao_duoc_ban_chup_cho_con"]),
    # --- vòng 3 đợt 2: 12 mục NÊN SỬA.
    ("kho_bo_o_dung_ba_doan",
     ("    if len(doan_m) >= 3:", "    if len(doan_m) == 3:"),
     ["t68_kho_duong_dan_SAU_neu_host_van_phai_QUA"]),
    ("stop_de_len_luot_da_xong",
     ('    ket = _giet_cay(int(pid), khoa)\n    if so.get("trang_thai") in TRANG_THAI_KET_THUC:',
      '    ket = _giet_cay(int(pid), khoa)\n    if False:'),
     ["t69_stop_luot_DA_KET_THUC_khong_duoc_doi_so"]),
    # Neo phải kèm chú thích: "if hien is None:" trần xuất hiện TRƯỚC ở nhánh
    # Windows của _con_song, mà replace(...,1) chỉ đổi chỗ ĐẦU TIÊN — đột biến
    # rơi vào nhánh không chạy trên Linux và báo "khong ca nao chet" oan.
    ("chet_roi_van_bao_PID_tai_dung",
     ("    if hien is None:\n        # TIẾN TRÌNH ĐÃ BIẾN MẤT",
      "    if False:\n        # TIẾN TRÌNH ĐÃ BIẾN MẤT"),
     ["t69_stop_luot_DA_KET_THUC_khong_duoc_doi_so"]),
    ("PROMPT_FILE_mo_coi_di_tiep",
     ('    elif any("{PROMPT_FILE}" in x for x in lenh_con):', '    elif False:'),
     ["t70_PROMPT_FILE_ma_khong_co_prompt_file_phai_bi_CHAN",
      "r13_PROMPT_FILE_thieu_prompt_file_phai_DO"]),
    # Hai nửa của cùng một bảo đảm: ghi hở quyền, và để lại trên đĩa.
    ("ban_chup_de_ho_quyen",
     ("        _fd = os.open(ban_chup, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)",
      "        _fd = os.open(ban_chup, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)"),
     ["t71_ban_chup_prompt_phai_KIN_va_bi_XOA"],
     ("posix", "t71 bo qua khang dinh quyen 0600 tren Windows")),
    ("ban_chup_de_lai_tren_dia",
     ('            and cay_da_chet):', '            and False):'),
     ["t71_ban_chup_prompt_phai_KIN_va_bi_XOA"],
     ("posix", "tren Windows ban chup GIU LAI theo thiet ke, nen 'khong xoa' khong doi gi")),
    ("xoa_prompt_khi_wrapper_vua_thoat",
     ('    cay_da_chet = (_thanh_vien_nhom(p.pid) == [])',
      '    cay_da_chet = True'),
     ["t76_wrapper_thoat_khong_duoc_xoa_prompt_cua_chau"]),
    ("ngat_ghi_thanh_xong",
     ('        ban_ghi["trang_thai"] = ("bi_ngat" if bi_ngat',
      '        ban_ghi["trang_thai"] = ("xong" if bi_ngat'),
     ["t72_bi_ngat_KHONG_duoc_ghi_thanh_xong"]),
    ("doctor_bo_do_bash",
     ('    {"ten": "bash", "bat_buoc": True, "ung_vien": ["bash"],',
      '    {"ten": "bash_da_dot_bien", "bat_buoc": False, "ung_vien": ["bash"],'),
     ["t73_doctor_phai_do_bash_va_npm"]),
    ("khong_quet_ban_chup_qua_han",
     ('        for mau in ("*/run.json.*.tmp", "*/prompt.snapshot"):',
      '        for mau in ("*/run.json.*.tmp",):'),
     ["t77_ban_chup_qua_han_bi_QUET_du_khong_xoa_duoc_ngay"]),
    ("khong_don_tep_tam_mo_coi",
     ('            for cu in run_root.glob(mau):',
      '            for cu in run_root.glob("KHONG-KHOP-GI-CA"):'),
     ["t75_tep_tam_mo_coi_bi_don"]),
    ("dut_ong_nuot_ma_that",
     ("    try:\n        print(chuoi)\n        return True\n"
      "    except BrokenPipeError:\n        return False",
      "    print(chuoi)\n    return True"),
     ["t74_dut_ong_KHONG_duoc_nuot_ma_that"]),
    # CHUYEN NEO (khong noi dieu kien): dong `if con == []` da tach thanh hai nhanh
    # theo nen khi Windows duoc cap phep do rieng (anh chup). Y DINH GIU NGUYEN -
    # ep None bi doc nhu rong. Neo vao nhanh Windows vi ca hai ca dich deu chay o do.
    ("none_nhom_thanh_cay_rong",
     ('            rong = con == {}',
      '            rong = con is None or con == {}   # DOT BIEN: None bi doc nhu rong'),
     ["t78_khong_do_duoc_nhom_KHONG_phai_cay_rong",
      "t83_windows_me_da_tat_va_anh_chup_RONG_la_du_bang_chung"]),
    ("job_bo_qua_loi_dat_gioi_han",
     ('        if not k32.SetInformationJobObject(job, 9, ctypes.byref(tt), ctypes.sizeof(tt)):',
      '        if False:'),
     ["t79_job_windows_phai_kiem_ket_qua_dat_gioi_han"]),
    ("job_pid_khong_tang_buffer",
     ('            suc_chua = max(suc_chua * 2, can)',
      '            return None  # DOT BIEN: bo doc lai khi buffer thieu'),
     ["t80_job_pid_tang_buffer_khi_qua_suc_chua"]),
    # (Đã bỏ `chup_cay_bo_qua_dong_thieu`.) Nó neo vào dòng phân tích đầu ra WMI —
    # dòng ấy KHÔNG CÒN TỒN TẠI sau khi `_chup_cay` chuyển sang Toolhelp32. Giữ lại
    # một đột biến không còn chỗ bám là giữ một PHÉP ĐO RỖNG: runner không thay được
    # gì, mutant "sống sót", và bảng đột biến vẫn báo đủ tỷ lệ. Đúng bệnh đã trả giá
    # ở `.pyc` (mutant chưa từng được chạy) và ở PR #141 (đột biến bơm vào tên hàm
    # không tồn tại). Lớp mà nó canh nay do `chup_cay_fail_closed_ca_may` giữ.
    ("san_dot_bien_chi_can_mot",
     ('TY_LE_DOT_BIEN_TOI_THIEU_PHAN_MUOI = 7',
      'TY_LE_DOT_BIEN_TOI_THIEU_PHAN_MUOI = 0'),
     ["t82_dot_bien_khong_duoc_mat_qua_30_phan_tram"]),
    # Windows khong co phep do nhom tien trinh; bo phep do thay the thi `stop` mot
    # luot DA KET THUC lai roi xuong taskkill tren PID khong ton tai => 125 (t69 do
    # that tren windows-latest 13-08).
    ("windows_khong_co_duong_bang_chung_me_da_tat",
     ('            rong = con == {}', '            rong = False'),
     ["t83_windows_me_da_tat_va_anh_chup_RONG_la_du_bang_chung"]),
    # Hau due khong query duoc creation time phai lam anh fail-closed. Bo phep kiem
    # => hau due mu lot vao anh voi khoa rong, roi `_con_song_dung_khoa` khong bao
    # gio khop => bao la da chet.
    ("chup_cay_khong_fail_closed_trong_cay",
     ('            if khoa is None:\n                return None\n            ra[q] = khoa',
      '            if False:\n                return None\n            ra[q] = khoa'),
     ["t81_chup_cay_windows_thieu_creationdate_phai_fail_closed"]),
    # Chieu NGUOC LAI: hoi khoa cho CA MAY thay vi chi cay => fail-closed mat pham
    # vi, mot tien trinh he thong vo can lam hong anh. Xanh ma vo dung.
    ("chup_cay_fail_closed_ca_may",
     ('        for q in list(ra):', '        for q in list(tt):'),
     ["t81_chup_cay_windows_thieu_creationdate_phai_fail_closed"]),
    # --- MƯỜI SÁU ĐỘT BIẾN CHO ĐƯỜNG MCP -------------------------------------------
    # Chúng đến từ SÁU lượt cross-review, và phần lớn từng SỐNG SÓT một lần — nên
    # chúng ở đây để cái lỗ ấy không âm thầm hở lại. Ba nhóm: `.mcp.json` · bộ phân
    # loại trạng thái · hợp đồng subprocess.
    # ĐỔI TỪ `"mcp"` SANG `"mcp-endpoint"` (PLAT-M4): sau khi trường được tách, không còn
    # đường nào tên `mcp` để mà thêm vào — mutant cũ sẽ đo một cái tên đã chết, tức là
    # KHÔNG đo gì. `mcp-endpoint` mới là cám dỗ thật: nó CÓ chạm máy chủ thật.
    # Hai ca giết nó theo hai đường độc lập: `t115` đọc MÃ NGUỒN, `t143` đo HÀNH VI
    # (`t138` ở dòng này là SAI và đã sửa ở lượt review 3: `t138` nay là ca THẬT của
    #  #196 — `t138_auth_het_ngan_sach_phai_vao_CHUA_DO` — không đo gì về mcp-endpoint.
    #  Trỏ vào một tên ĐANG SỐNG mà sai nghĩa còn tệ hơn trỏ vào tên đã chết.)
    # HAI ĐỘT BIẾN TỪ LƯỢT REVIEW 3 (R1, R3). Mỗi chốt mới phải có mutant RIÊNG — một
    # cửa không có mutant là một cửa sẽ âm thầm hở lại; kho đã trả giá đúng bài này.
    ("mcp_endpoint_bo_doc_PORT",
     ('        _ = p_ep.port\n', ''),
     ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_json_noi_suy_url_NGUYEN_VAN_vao_mo_ta",
     ('        _duoi = f" @ {_noi}"', '        _duoi = f" @ {url}"'),
     ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    # (endpoint OK một mình mà nhãn vẫn phải là CHUA_XAC_THUC).
    ("mcp_endpoint_tinh_vao_LAM_DUOC_VIEC",
     ('    LAM_DUOC_VIEC = {"git", "gh-kho", "rest-kho"}',
      '    LAM_DUOC_VIEC = {"git", "gh-kho", "rest-kho", "mcp-endpoint"}'),
     ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec", "t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    # --- SÁU ĐỘT BIẾN CHO `_do_mcp_endpoint` (PLAT-M4, #194) -------------------------
    ("mcp_endpoint_phan_loai_theo_MA_thay_vi_HEADER",
     ('            co_gh_ep = any(k.lower().startswith("x-github") for k in r.headers)',
      '            co_gh_ep = 200 <= int(r.status) < 300'), ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_endpoint_toi_duoc_la_LAM_DUOC_VIEC",
     ('        return (("mo" if co_gh_ep else "chan"), f"HTTP {e.code}{vi_sao_ep}", False)',
      '        return (("mo" if co_gh_ep else "chan"), f"HTTP {e.code}{vi_sao_ep}", True)'),
     ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_endpoint_gop_khong_do_duoc_vao_chan",
     ('        return ("khong_do_duoc", f"{type(e).__name__} khi POST initialize", False)',
      '        return ("chan", f"{type(e).__name__} khi POST initialize", False)'), ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_endpoint_bo_kiem_scheme_cho_phep",
     ('    if chu_ep not in ("http", "https"):',
      '    if False:'), ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    # --- HAI DOT BIEN CHO BAN VA userinfo (PLAT-M4 vong V0) -------------------------
    ("mcp_endpoint_bo_kiem_userinfo",
     ('    if ai_ep != (None, None):',
      '    if False:'), ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    # --- BA DOT BIEN CUA LUOT REVIEW 2/2 (bien cau truc + ro ri qua MO TA) ----------
    ("mcp_endpoint_userinfo_do_bang_KY_TU_thay_vi_CAU_TRUC",
     ('    if ai_ep != (None, None):',
      '    if "@" in str(url):'), ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_endpoint_userinfo_chi_doc_username_theo_tinh_chan_ly",
     ('    if ai_ep != (None, None):',
      '    if p_ep.username:'), ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_endpoint_nhanh_scheme_in_lai_url_ra_mo_ta",
     ('        return ("khong_do_duoc", "`url` khong phai http(s) — scheme ngoai danh sach cho "\n'
      '                                 "phep (KHONG in `url` ra day: no co the dang cho bi mat)",\n'
      '                False)',
      '        return ("khong_do_duoc", f"`url` khong phai http(s): {url!r}", False)'),
     ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_endpoint_tu_choi_userinfo_MA_VAN_in_url",
     ('        return ("khong_do_duoc", "`url` nhung credential trong userinfo — TU CHOI, KHONG "\n'
      '                                 "probe (bi mat se di vao URL va header Host)", False)',
      '        return ("khong_do_duoc", f"`url` co userinfo: {url!r}", False)'),
     ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_endpoint_in_token_vao_mo_ta",
     ('        return (("mo" if co_gh_ep else "chan"), f"HTTP {e.code}{vi_sao_ep}", False)',
      '        return (("mo" if co_gh_ep else "chan"), f"HTTP {e.code}{vi_sao_ep} [{dau}]", False)'),
     ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_endpoint_nuot_ly_do_o_chuoi_tom_tat",
     ('        if co_ep is not True:\n            canh_ep = f" · mcp-endpoint: {mt_ep}"',
      '        if False:\n            canh_ep = f" · mcp-endpoint: {mt_ep}"'),
     ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_endpoint_chua_biet_URL_bi_ke_thanh_HONG",
     ('        duong.append(("mcp-endpoint", None, "khong biet URL — .mcp.json chua khai server"))',
      '        duong.append(("mcp-endpoint", False, "khong biet URL — .mcp.json chua khai server"))'),
     ["t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_ket_xuat_gop_chua_do_duoc_thanh_hong",
     ('    return "chua-do-duoc" if ok is None else ("OK" if ok else "khong")',
      '    return "OK" if ok else "khong"'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_ten_server_khop_chuoi_con",
     ('k.casefold() == "github"', '"github" in k.casefold()'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_ten_server_phan_biet_hoa_thuong",
     ('k.casefold() == "github"', 'k == "github"'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_bo_bat_loi_json_hong",
     ('    except (OSError, ValueError) as e:\n'
      '        return (False, f".mcp.json [{nguon}] khong doc/parse duoc:',
      '    except OSError as e:\n'
      '        return (False, f".mcp.json [{nguon}] khong doc/parse duoc:'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_bo_kiem_kieu_goc",
     ('    if not isinstance(d, dict):', '    if False:'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_bo_kiem_kieu_bang_server",
     ('    if not isinstance(srv, dict):', '    if False:'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_bo_kiem_kieu_gia_tri_server",
     ('    xau = [k for k in ten if not isinstance(srv[k], dict)]', '    xau = []'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_bo_kiem_kieu_headers",
     ('    if not isinstance(headers, dict):', '    if False:'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_servers_che_khuat_mcpServers_sai_kieu",
     ('    for khoa in ("mcpServers", "servers"):\n        if khoa in d:\n'
      '            srv = d[khoa]\n            break\n    else:',
      '    srv = d.get("mcpServers") or d.get("servers") or {}\n    khoa = "mcpServers"\n'
      '    if False:'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_chon_ten_theo_thu_tu_khoa_JSON",
     ('    if len(ten) > 1:', '    if False:'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_suc_khoe_do_chuoi_con_ca_dong",
     ('    if chuan in _MCP_KHOE:',
      '    thap = (r.stdout or "").casefold()\n'
      '    if "connected" in thap and "not connected" not in thap:'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_suc_khoe_khop_TIEN_TO_thay_vi_bang_dung",
     ('    if chuan in _MCP_KHOE:', '    if chuan.startswith(_MCP_KHOE):'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_trang_thai_LA_bi_doan_thanh_hong",
     ('    return ("khong_do_duoc", f"trang thai LA, chua tung do: Status: {tho}")',
      '    return ("hong", f"trang thai LA, chua tung do: Status: {tho}")'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_doc_Status_CUOI_thay_vi_DAU",
     ('    kq = _RE_STATUS.search(_RE_ANSI.sub("", r.stdout or ""))',
      '    _ds = list(_RE_STATUS.finditer(_RE_ANSI.sub("", r.stdout or "")))\n'
      '    kq = _ds[-1] if _ds else None'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_hoi_ten_dung_san_thay_vi_ten_da_khai",
     ('        r = _chay_probe_nhu_shell(["claude", "mcp", "get", ten], capture_output=True, text=True,',
      '        r = _chay_probe_nhu_shell(["claude", "mcp", "get", "github"], capture_output=True, text=True,'),
     ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    # ĐỘT BIẾN CỦA REVIEWER LƯỢT 7 — lượt thứ NĂM của lớp "đo đồ giả", và là lượt đầu
    # tìm được sau khi chốt đã đảo thành danh sách CHO PHÉP. Giữ cả hai chiều: bỏ chuẩn
    # hoá trong hàm, và ép `env=None` ở lời gọi.
    ("mcp_bo_chuan_hoa_env_trong_ham",
     ('    moi_truong = _env_da_chuan(moi_truong)\n    try:', '    try:'),
     ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("env_da_chuan_tra_ve_os_environ_THO",
     ('    if mt is not None:\n        return mt', '    if False:\n        return mt'),
     ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_ep_env_None_o_loi_goi",
     ('                           env=moi_truong, stdin=subprocess.DEVNULL,',
      '                           env=None, stdin=subprocess.DEVNULL,'),
     ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("rest_kho_khong_do_duoc_bi_gop_thanh_hong",
     ('        duong.append(("rest-kho", None, "khong doc duoc slug origin -> KHONG DO DUOC"))',
      '        duong.append(("rest-kho", False, "khong doc duoc slug origin -> KHONG DO DUOC"))'),
     ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_mat_env_da_chuan_hoa",
     ('                           env=moi_truong, stdin=subprocess.DEVNULL,',
      '                           stdin=subprocess.DEVNULL,'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    # --- AG-T0-01B: MƯỜI ĐỘT BIẾN CHO AGY VÀ ANTIGRAVITY (N1-N9) -------------------
    ("agy_cong_cu_xoa_muc",
     ('    {"ten": "agy", "bat_buoc": False, "ung_vien": ["agy"],\n'
      '     "vi_sao": "CLI client cho Google Antigravity (provider: google_antigravity, surface: antigravity)",\n'
      '     "cai": {"Windows": "irm https://antigravity.google/cli/install.ps1 | iex",\n'
      '             "Darwin": "curl -fsSL https://antigravity.google/cli/install.sh | bash",\n'
      '             "Linux": "curl -fsSL https://antigravity.google/cli/install.sh | bash"},\n'
      '     "xac_thuc": ["models"]},',
      ''),
     ["t145_agy_cong_cu_va_kha_nang"]),
    ("agy_xac_thuc_sang_version",
     ('     "xac_thuc": ["models"]},', '     "xac_thuc": ["--version"]},'),
     ["t145_agy_cong_cu_va_kha_nang"]),
    ("agy_kha_nang_xoa_muc",
     ('    {"ten": "antigravity", "do": lambda ws, ks=False: _do_antigravity(_MOI_TRUONG_DA_DOC),\n'
      '     "vi_sao": "provider google_antigravity qua execution_surface antigravity (AG-T0-01B)",\n'
      '     "khac_phuc": "cai agy CLI va chay `agy` (mo TUI de dang nhap)"},',
      ''),
     ["t145_agy_cong_cu_va_kha_nang"]),
    ("agy_goi_xac_thuc_models",
     ('            ok_xt, mo_ta_xt, qua_han_xt, ra_xt = _xac_thuc_kem_dau_ra(duong_agy, ["models"], env=mt, timeout=PROBE_TIMEOUT_GIAY)',
      '            ok_xt, mo_ta_xt, qua_han_xt, ra_xt = _xac_thuc_kem_dau_ra(duong_agy, [], env=mt, timeout=PROBE_TIMEOUT_GIAY)'),
     ["t146_do_antigravity_cac_trang_thai_va_luong"]),
    # P2 cross-review 4639462: `_do_antigravity` bo qua bang ket qua cua `doctor` va tu chay
    # `agy models` lan hai trong cung luot => ca dau-cuoi t148 chet (OSError lan hai -> CO_MAT).
    ("agy_bo_qua_ket_qua_doctor",
     ('        da_do = _XAC_THUC_DA_DO.get((duong_agy, ("models",)))',
      '        da_do = None'),
     ["t148_doctor_chay_agy_models_MOT_lan_cho_ca_CONG_CU_lan_KHA_NANG"]),
    # ...va mat kia: `doctor` quen ghi ket qua probe vao bang => cung ca ay chet.
    ("doctor_khong_ghi_ket_qua_xac_thuc",
     ('                _XAC_THUC_DA_DO[(thay["duong_dan"], tuple(c["xac_thuc"]))] = (\n'
      '                    xac_thuc_ok is True, xt_mo_ta_cuoi, bool(xt_qua_han), xt_dau_ra)',
      '                pass'),
     ["t148_doctor_chay_agy_models_MOT_lan_cho_ca_CONG_CU_lan_KHA_NANG"]),
    # ...va bang song qua hai luot: luot sau doc anh chup luot truoc => ve thu hai cua t148 chet.
    ("doctor_khong_xoa_bang_xac_thuc_luot_truoc",
     ('    _XAC_THUC_DA_DO.clear()        # lượt mới, bằng chứng mới — không đọc ảnh chụp cũ',
      '    pass'),
     ["t148_doctor_chay_agy_models_MOT_lan_cho_ca_CONG_CU_lan_KHA_NANG"]),
    # P2 cross-review 15f2dbf: quay lai goi `agy models` lan hai de dem dong => ca "mot lan" chet.
    ("agy_goi_models_lan_hai",
     ('            so_dong = len([d for d in ra_xt.splitlines() if d.strip()])',
      '            p_mod = _chay_van_ban_an_toan([duong_agy, "models"], env=mt, timeout=PROBE_TIMEOUT_GIAY)\n'
      '            so_dong = len([d for d in ((p_mod.stdout or "") + (p_mod.stderr or "")).splitlines() if d.strip()])'),
     ["t146_do_antigravity_cac_trang_thai_va_luong"]),
    ("agy_probe_models_timeout_thanh_thieu",
     ('        if qua_han_xt:\n            loi_cuoi = ("KHONG_DO_DUOC", f"probe models timeout sau {PROBE_TIMEOUT_GIAY:.1f}s{duoi_path}")',
      '        if qua_han_xt:\n            loi_cuoi = ("THIEU", f"probe models timeout sau {PROBE_TIMEOUT_GIAY:.1f}s{duoi_path}")'),
     ["t146_do_antigravity_cac_trang_thai_va_luong"]),
    ("agy_probe_models_rong_thanh_co_mat",
     ('        if mo_ta_xt == "rc=0 nhung khong co bang chung xac thuc":\n            # Finding 1: models rc=0 nhưng không có đầu ra -> KHONG_DO_DUOC (không làm tròn thành CO_MAT hay DUNG_DUOC)\n            loi_cuoi = ("KHONG_DO_DUOC", f"probe models khong co dau ra (rc=0 nhung khong co bang chung xac thuc){duoi_path}")',
      '        if mo_ta_xt == "rc=0 nhung khong co bang chung xac thuc":\n            co_mat_str = ("CO_MAT", f"chua dang nhap{duoi_path}")'),
     ["t146_do_antigravity_cac_trang_thai_va_luong"]),
    ("agy_windows_bo_fallback_localappdata",
     ('        elif c["ten"] == "agy" and local:',
      '        elif False:'),
     ["t147_agy_fallback_localappdata_windows"]),
    ("agy_windows_fallback_bo_chan_doan_path",
     ('        duoi_path = " · đã cài, PATH phiên này chưa thấy — mở terminal mới" if la_fallback else ""',
      '        duoi_path = ""'),
     ["t147_agy_fallback_localappdata_windows"]),
    ("antigravity_tinh_vao_LAM_DUOC_VIEC",
     ('    LAM_DUOC_VIEC = {"git", "gh-kho", "rest-kho"}',
      '    LAM_DUOC_VIEC = {"git", "gh-kho", "rest-kho", "antigravity"}'),
     ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    # ---- wp685 (đặc tả r28 §7 B5): 54 dòng (a)–(m), mỗi dòng MỘT vị trí; (c) hai ca đích ⇒ 55 cặp.
    ('wp685_a_go_ban_va',
     ('    try:\n        trang_thai.stat()\n        co_tep = True\n    except (FileNotFoundError, NotADirectoryError):\n        co_tep = False\n    except ProcessLookupError:\n        return False\n    except OSError:\n        co_tep = None   # KHÔNG kết luận: không stat được chưa có nghĩa là không đọc được\n    if co_tep:\n        # Nhánh tệp có giữ nguyên xi (Q-A.3), trừ cách giải mã (Q-A.7: latin-1, PR #688\n        # comment 5905670017; cross-review lượt 7, lượt 8).\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            return False\n    if co_tep is None:\n        # wp685 (zombie: cross-review lượt 1 trên PR #688) — thử đọc nội dung ĐÚNG MỘT lần,\n        # zombie vẫn phải tính là đã chết. Đọc lỗi hay nội dung hỏng ⇒ KHÔNG trả False mà rơi\n        # về os.kill(pid, 0) bên dưới (cross-review lượt 2, lượt 4: bước kill phải THỰC SỰ được\n        # gọi và quyết định). Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass\n',
      '    if trang_thai.exists():\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            return False\n'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_b_ban_rong',
     ('    except OSError:\n        co_tep = None',
      '    except OSError:\n        return False'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_c_bo_doc_duong_moi',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      "Khối bọc chỉ gồm phép đọc và biểu thức tách theo ')' CUỐI.\n        pass"),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan', 't157_giet_cay_khi_stat_EACCES_van_tron_ven']),
    ('wp685_d1_hoi_chi_PermissionError',
     ('    except OSError:\n        co_tep = None',
      '    except PermissionError:\n        co_tep = None'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_d2_doc_chi_PermissionError',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (PermissionError, ValueError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_e1_hoi_nuot_BaseException',
     ('    except OSError:\n        co_tep = None',
      '    except BaseException:\n        co_tep = None'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_e2_doc_nuot_KeyboardInterrupt',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except KeyboardInterrupt:\n            pass\n        except (OSError, ValueError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_f_hoi_exists_lan_hai',
     ('        trang_thai.stat()\n        co_tep = True\n',
      '        trang_thai.stat()\n        trang_thai.stat()\n        co_tep = True\n'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_g1_doc_loi_False',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except OSError:\n            return False\n        except (ValueError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_g2_doc_ESRCH_False',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except ProcessLookupError:\n            return False\n        except (OSError, ValueError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_h1_hoi_bat_Exception',
     ('    except OSError:\n        co_tep = None',
      '    except Exception:\n        co_tep = None'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_h2_doc_bat_Exception',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except Exception:\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_i_noi_dung_hong_False',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except OSError:\n            pass\n        except (ValueError, IndexError):\n            return False'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_j1_doc_lan_hai_sau_thanh_cong',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_j2_doc_lan_hai_khi_doc_loi',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            try:\n                trang_thai.read_text(encoding="latin-1")\n            except OSError:\n                pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_k1_tra_True_khong_hoi_pid',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            return True'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_k2_hoi_pid_bo_ket_qua',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            try:\n                os.kill(pid, 0)\n            except OSError:\n                pass\n            return True'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_k3_tu_kill_PermissionError_False',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            try:\n                os.kill(pid, 0)\n            except OSError:\n                return False\n            return True'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_k4_tu_kill_OSError_khac_True',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            try:\n                os.kill(pid, 0)\n            except ProcessLookupError:\n                return False\n            except OSError:\n                return True\n            return True'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_k5_hoi_pid_hai_lan',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            try:\n                os.kill(pid, 0)\n            except OSError:\n                pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l1_hoi_chi_ProcessLookupError',
     ('    except ProcessLookupError:\n        return False\n    except OSError:\n        co_tep = None',
      '    except ProcessLookupError:\n        return False'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l2_hoi_ESRCH_chung_nhanh',
     ('    except ProcessLookupError:\n        return False\n    except OSError:\n        co_tep = None',
      '    except OSError:\n        co_tep = None'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l3_hoi_OSError_khac_False',
     ('    except OSError:\n        co_tep = None',
      '    except PermissionError:\n        co_tep = None\n    except OSError:\n        return False'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l4_hoi_errno_trang_EACCES_EIO',
     ('    except OSError:\n        co_tep = None',
      '    except OSError as e:\n        if e.errno not in (13, 5):\n            raise\n        co_tep = None'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l5_hoi_EPERM_False',
     ('    except OSError:\n        co_tep = None',
      '    except OSError as e:\n        if e.errno == 1:\n            return False\n        co_tep = None'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l6_hoi_them_IndexError',
     ('    except OSError:\n        co_tep = None',
      '    except (OSError, IndexError):\n        co_tep = None'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l7_hoi_them_ValueError',
     ('    except OSError:\n        co_tep = None',
      '    except (OSError, ValueError):\n        co_tep = None'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l8_hoi_them_UnicodeDecodeError',
     ('    except OSError:\n        co_tep = None',
      '    except (OSError, UnicodeDecodeError):\n        co_tep = None'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l9_hoi_boc_Exception',
     ('    except OSError:\n        co_tep = None',
      '    except OSError:\n        co_tep = None\n    except Exception as e:\n        raise RuntimeError("boc") from e'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l10_doc_chi_bat_phan_tich',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (ValueError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l11_doc_errno_EACCES_EIO',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError) as e:\n            if isinstance(e, OSError) and e.errno not in (13, 5):\n                raise'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l12_doc_errno_EACCES_EIO_ESRCH',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError) as e:\n            if isinstance(e, OSError) and e.errno not in (13, 5, 3):\n                raise'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l13_doc_EPERM_False',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError) as e:\n            if isinstance(e, OSError) and e.errno == 1:\n                return False'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l14_doc_OSError_khac_False',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except PermissionError:\n            pass\n        except OSError:\n            return False\n        except (ValueError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l15_doc_khong_bat_ValueError',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l16_doc_kiem_chuoi_rong',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            if noi_dung:\n                return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l17_doc_khong_bat_IndexError',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l18_doc_IndexError_False',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except IndexError:\n            return False\n        except (OSError, ValueError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l19_doc_chi_OSError_tach_rieng',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n        except OSError:\n            noi_dung = ""\n        try:\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (ValueError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l20_doc_UnicodeDecodeError_False',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except UnicodeDecodeError:\n            return False\n        except (OSError, ValueError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l21_doc_boc_ValueError',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except ValueError as e:\n            raise RuntimeError("boc") from e\n        except (OSError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l22_kill_chi_PermissionError',
     ('    except ProcessLookupError:\n        return False\n    except PermissionError:\n        return True  # tồn tại nhưng khác chủ\n    except OSError:\n        return False\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps',
      '    except PermissionError:\n        return True  # tồn tại nhưng khác chủ\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l23_kill_chi_ProcessLookupError',
     ('    except ProcessLookupError:\n        return False\n    except PermissionError:\n        return True  # tồn tại nhưng khác chủ\n    except OSError:\n        return False\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps',
      '    except ProcessLookupError:\n        return False\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l24_kill_bo_OSError',
     ('    except OSError:\n        return False\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps',
      '    if platform.system() == "Darwin":  # không có /proc: hỏi ps'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l25_kill_them_BaseException',
     ('    except OSError:\n        return False\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps',
      '    except OSError:\n        return False\n    except BaseException:\n        return True\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l26_kill_them_Exception',
     ('    except OSError:\n        return False\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps',
      '    except OSError:\n        return False\n    except Exception:\n        return True\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l27_kill_them_IndexError',
     ('    except OSError:\n        return False\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps',
      '    except OSError:\n        return False\n    except IndexError:\n        return True\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l28_kill_them_ValueError',
     ('    except OSError:\n        return False\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps',
      '    except OSError:\n        return False\n    except ValueError:\n        return True\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_l29_kill_them_UnicodeDecodeError',
     ('    except OSError:\n        return False\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps',
      '    except OSError:\n        return False\n    except UnicodeDecodeError:\n        return True\n    if platform.system() == "Darwin":  # không có /proc: hỏi ps'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_m1_nhanh_cu_hop_nhat_ve_kill',
     ('comment 5905670017; cross-review lượt 7, lượt 8).\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            return False',
      'comment 5905670017; cross-review lượt 7, lượt 8).\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            pass'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_m2_nhanh_cu_bat_BaseException',
     ('comment 5905670017; cross-review lượt 7, lượt 8).\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            return False',
      'comment 5905670017; cross-review lượt 7, lượt 8).\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n        except (OSError, ValueError, IndexError):\n            return False\n        except BaseException:\n            return False'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_m3_tep_vang_False',
     ('    if co_tep is None:\n',
      '    if co_tep is False:\n        return False\n    if co_tep is None:\n'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_m4_ESRCH_hoi_lai',
     ('    except ProcessLookupError:\n        return False\n    except OSError:\n        co_tep = None',
      '    except ProcessLookupError:\n        try:\n            trang_thai.stat()\n        except OSError:\n            pass\n        return False\n    except OSError:\n        co_tep = None'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    ('wp685_m5_duong_moi_tach_ngoac_dau',
     ('Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"\n',
      'Khối bọc chỉ gồm phép đọc và biểu thức tách theo \')\' CUỐI.\n        try:\n            noi_dung = trang_thai.read_text(encoding="latin-1")\n            return noi_dung[noi_dung.index(")") + 2:].split()[0] != "Z"\n'),
     ['t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan']),
    # ---- #743 (đặc tả py314-path-exists-nuot-oserror r1, Q2): mỗi chốt phân loại errno một đột biến.
    ('r743_a_ve_lai_exists',
     ('        trang_thai.stat()\n        co_tep = True\n',
      '        co_tep = trang_thai.exists()\n'),
     ['r743_con_song_tham_do_bang_stat_giu_errno_moi_phien_ban']),
    ('r743_b_ENOENT_chua_ket_luan',
     ('    except (FileNotFoundError, NotADirectoryError):\n        co_tep = False\n',
      ''),
     ['r743_con_song_tham_do_bang_stat_giu_errno_moi_phien_ban']),
    ('r743_c_bo_ENOTDIR',
     ('    except (FileNotFoundError, NotADirectoryError):',
      '    except FileNotFoundError:'),
     ['r743_con_song_tham_do_bang_stat_giu_errno_moi_phien_ban']),
    ('r743_d_OSError_khac_khong_tep',
     ('    except OSError:\n        co_tep = None',
      '    except OSError:\n        co_tep = False'),
     ['r743_con_song_tham_do_bang_stat_giu_errno_moi_phien_ban']),
    ('r743_e_bo_nhanh_ESRCH',
     ('    except ProcessLookupError:\n        return False\n    except OSError:\n        co_tep = None',
      '    except OSError:\n        co_tep = None'),
     ['r743_con_song_tham_do_bang_stat_giu_errno_moi_phien_ban']),
]


# wp802 (N6–N8): đột biến trên BẢN SAO TẠM của hook. Chỉ `TinHieuChotCa` của ca đích mới
# tính là GIẾT — lỗi khác là tín dụng giả (CLAUDE.md, bài học 27-08).
DOT_BIEN_HOOK = [
    ("wp802_hook_co_thay_co_chay", ("  co_chay rg || { co cargo", "  co rg || { co cargo"),
     ["r802_hook_linux_rg_hong_van_thu_cargo"]),
    ("wp802_hook_windows_roi_vao_apt", ("MINGW*|MSYS*|CYGWIN*) RG_WIN=1", "KHONG_KHOP_NEN_NAO) RG_WIN=1"),
     ["r802_hook_windows_khong_cai_in_dung_lenh"]),
    ("wp802_hook_lenh_windows_lech_yaml", ("RG_CAI_WINDOWS='winget install", "RG_CAI_WINDOWS='choco install"),
     ["r802_bang_cai_rg_khop_cong_cu_yaml", "r802_hook_windows_khong_cai_in_dung_lenh"]),
    # Phần tử thứ tư "yaml" = đột biến ops/cong_cu.yaml thay vì hook (Codex lượt 1 F2).
    # wp868 (N4): `rg.cai.windows` dùng bộ chọn chung — chọn theo `kiem-tra` và ghi $GITHUB_PATH nay là chốt của hàm
    # (đột biến wp858_sh_*); bỏ hai đột biến YAML cũ đã mất neo (`wp802_yaml_chon_ung_vien_chi_theo_ma_thoat`,
    # `wp802_yaml_khong_ghi_github_path`).
    ("wp802_yaml_bo_ung_vien_winget_links", (' "$LOCALAPPDATA/Microsoft/WinGet/Links"', ''),
     ["r802_cai_rg_windows_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "yaml"),
    ("wp802_hook_windows_probe_hai_lan", ('if [ "$RG_WIN" = 1 ]; then', 'if [ "$RG_WIN" = 1 ] && ! co_chay rg; then'),
     ["r802_hook_windows_khong_cai_in_dung_lenh"]),
    # wp831 (N1–N3 + F01): wp868 (N4) chuyển `rg.cai.linux/macos` sang bộ chọn chung nên ba đột biến YAML về `-x`, chọn
    # theo mã thoát và ghi $GITHUB_PATH vô điều kiện mất neo — chốt ấy nay nằm trong hàm (wp858_sh_*). Giữ hai đột biến ứng
    # viên, kèm ca hình dạng để đo được trên Windows.
    # wp1078 (M4): chọn bằng `command -v` (nhận hàm) · bỏ riêng chốt tuyệt đối · bỏ cả hai.
    ("wp1078_chon_bang_command_v", ('elif _PY_TEP="$(type -P python)"; then PY=("$_PY_TEP")',
      'elif command -v python >/dev/null 2>&1; then PY=(python)'),
     ["r831_cai_rg_linux_python_ham_ke_thua", "r831_cai_rg_macos_python_ham_ke_thua",
      "r1078_ham_python_khong_phai_python_khong_duoc_goi", "r1078_hinh_dang_chon_python_bang_type_P"], "cai_sh"),
    ("wp1078_goi_ham_python_thua", ('unset _PY_TEP',
      'unset _PY_TEP\nif declare -F python >/dev/null; then python -c pass >/dev/null; fi'),
     ["r1078_ham_python_khong_phai_python_khong_duoc_goi"], "cai_sh"),
    ("wp1078_chot_chi_nhanh_chon_moi", ('case "${PY[0]}" in /*) ;; *) echo "cai_cong_cu: PY[0] khong phai duong dan tuyet doi: \'${PY[0]}\'" >&2; exit 4 ;; esac',
      'if [ "${CAI_CONG_CU_PY_CUA:-}" != "$$" ]; then\ncase "${PY[0]}" in /*) ;; *) echo "cai_cong_cu: PY[0] khong phai duong dan tuyet doi: \'${PY[0]}\'" >&2; exit 4 ;; esac\nfi'),
     ["r1078_py_dung_lai_khong_tuyet_doi_phai_thoat_4"], "cai_sh"),
    ("wp1078_bo_chot_tuyet_doi", ('case "${PY[0]}" in /*) ;; *) echo', 'case "${PY[0]}" in *) ;; /*) echo'),
     ["r1078_hinh_dang_chon_python_bang_type_P"], "cai_sh"),
    ("wp831_yaml_linux_bo_ung_vien_usrbin", ('chon_thu_muc_chay_duoc rg "${CONG_CU_GOC:-}/usr/bin" ', 'chon_thu_muc_chay_duoc rg '),
     ["r831_cai_rg_linux_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "yaml"),
    ("wp831_yaml_macos_bo_ung_vien_brew", ('chon_thu_muc_chay_duoc rg "$(brew --prefix)/bin" ', 'chon_thu_muc_chay_duoc rg '),
     ["r831_cai_rg_macos_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "yaml"),
    # wp858: mỗi đột biến kèm ca hình dạng thuần Python để đo được cả Windows (sàn ≥70%, 39343232374: 197/281).
    ("wp858_yaml_git_linux_ve_dirname",
     ('sudo apt-get install -y git && chon_thu_muc_chay_duoc git "${CONG_CU_GOC:-}/usr/bin" "$(dirname "$(command -v git || echo ./git)")"',
      'sudo apt-get install -y git && dirname "$(command -v git)"'),
     ["r858_cai_linux_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "yaml"),
    ("wp858_yaml_bash_macos_bo_ung_vien_brew",
     ('chon_thu_muc_chay_duoc bash "$(brew --prefix)/bin" ', 'chon_thu_muc_chay_duoc bash '),
     ["r858_cai_macos_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "yaml"),
    ("wp858_yaml_shellcheck_windows_bo_ung_vien_choco",
     ('--win shellcheck "${ChocolateyInstall:-C:/ProgramData/chocolatey}/bin" ', '--win shellcheck '),
     ["r858_cai_windows_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "yaml"),
    ("wp858_yaml_python_linux_ve_dirname",
     ('sudo apt-get install -y python3 python3-pip && chon_thu_muc_chay_duoc python "${CONG_CU_GOC:-}/usr/bin" "$(dirname "$(command -v python || echo ./python)")"',
      'sudo apt-get install -y python3 python3-pip && dirname "$(command -v python3)"'),
     ["r858_cai_python_khong_in_thu_muc_ban_hong", "r858_hinh_dang_cong_thuc_cai"], "yaml"),
    ("wp858_sh_bo_kiem_ten_tran",
     # Không nhắm N4 (ứng viên đầu luôn DAT nhờ tên trần, PATH nhận `/usr/bin` có `rg` tốt); hại thật: ghi $GITHUB_PATH.
     ('  if cong_cu_dat "$ten"; then', '  if false; then'),
     ["r858_cai_linux_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp858_sh_chon_theo_ma_thoat",
     ('if PATH="$d:$PATH" cong_cu_dat "$ten"; then',
      'if "$d/$ten" --version >/dev/null 2>&1; then'),
     ["r858_cai_linux_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    # wp1045: DAT theo trang thai CHINH cong cu, khong theo rc; thoat 3 chi cho loi goi truc tiep.
    ("wp1045_sh_ten_tran_ve_rc",
     ('  if cong_cu_dat "$ten"; then', '  if "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$ten" >/dev/null 2>&1; then'),
     ["r1045_cong_cu_tuy_chon_vang_mat_khong_duoc_nhan_giu_path", "r1045_hinh_dang_dat_theo_trang_thai"], "cai_sh"),
    ("wp1045_sh_ung_vien_ve_rc",
     ('if PATH="$d:$PATH" cong_cu_dat "$ten"; then',
      'if PATH="$d:$PATH" "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$ten" >/dev/null 2>&1; then'),
     ["r1045_cong_cu_tuy_chon_vang_mat_khong_duoc_nhan_giu_path", "r1045_hinh_dang_dat_theo_trang_thai"], "cai_sh"),
    ("wp1045_sh_cong_cu_dat_bo_trang_thai",
     (' and c[0].get(sys.argv[2]) == json.loads(sys.argv[3]) else 1)', ' else 1)'),
     ["r1045_cong_cu_tuy_chon_vang_mat_khong_duoc_nhan_giu_path", "r1045_hinh_dang_dat_theo_trang_thai"], "cai_sh"),
    ("wp1045_sh_bo_thoat_3",
     ('kiem-tra rc=$RC_KT)" >&2\n    exit 3\n', 'kiem-tra rc=$RC_KT)" >&2\n'),
     ["r1045_cong_cu_tuy_chon_vang_mat_khong_duoc_nhan_giu_path", "r1045_hinh_dang_dat_theo_trang_thai"], "cai_sh"),
    ("wp1045_sh_source_tuy_chon_hong_van_dung",
     ('if [ "${CAI_CONG_CU_PY_CUA:-}" = "$$" ] && cong_cu_json_dung "$TEN" bat_buoc false; then', 'if false; then'),
     ["r1045_bat_buoc_cong_cu_tuy_chon_thieu_khong_chan_cong_cu_sau", "r1045_hinh_dang_dat_theo_trang_thai"], "cai_sh"),
    ("wp1045_sh_source_bat_buoc_hong_van_di_tiep",
     ('cong_cu_json_dung "$TEN" bat_buoc false; then', 'true; then'),
     ["r1045_bat_buoc_cong_cu_bat_buoc_hong_van_dung", "r1045_hinh_dang_dat_theo_trang_thai"], "cai_sh"),
    ("wp1045_sh_kiem_cuoi_tran_duoi_errexit",
     ('  "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json || RC_KT=$?\n',
      '  "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json\n'),
     ["r1045_cong_cu_tuy_chon_vang_mat_khong_duoc_nhan_giu_path", "r1045_hinh_dang_dat_theo_trang_thai"], "cai_sh"),
    ("wp1045_sh_eval_trong_ngu_canh_dieu_kien",
     ('set +e\n( set +e; eval "$LENH" ) > "$TAM_CAI/stdout"\nRC_CAI=$?\nset -e\n',
      'RC_CAI=0\n( set +e; eval "$LENH" ) > "$TAM_CAI/stdout" || RC_CAI=$?\n'),
     ["r1045_cong_cu_tuy_chon_vang_mat_khong_duoc_nhan_giu_path", "r1045_hinh_dang_dat_theo_trang_thai"], "cai_sh"),
    ("wp1045_sh_source_khong_don_tam",
     ('    rm -rf -- "$TAM_CAI"\n    return 0\n', '    return 0\n'),
     ["r1045_bat_buoc_cong_cu_tuy_chon_thieu_khong_chan_cong_cu_sau"], "cai_sh"),
    ("wp1045_sh_rc_cai_mat_ma",
     ('  exit "$RC_CAI"\n', '  RC_CAI=1; exit "$RC_CAI"\n'),
     ["r1045_bat_buoc_cong_cu_bat_buoc_hong_van_dung"], "cai_sh"),
    # Codex wp1045 lượt 2 (P3): lỗi kiểm cuối của lượt source phải dừng cả loạt.
    ("wp1045_sh_errexit_tat_sau_eval",
     ('RC_CAI=$?\nset -e\n', 'RC_CAI=$?\nset -e\nset +e\n'),
     ["r1045_bat_buoc_kiem_cuoi_luot_source_hong_thi_dung_ca_loat"], "cai_sh"),
    ("wp1045_sh_kiem_cuoi_source_nuot_loi",
     ('then\n  "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json\nelse\n',
      'then\n  "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json || true\nelse\n'),
     ["r1045_bat_buoc_kiem_cuoi_luot_source_hong_thi_dung_ca_loat"], "cai_sh"),
    ("wp1045_sh_thoat_3_ca_luot_source",
     ('if [ "${CAI_CONG_CU_PY_CUA:-}" = "$$" ]; then\n  "${PY[@]}" "$GOC/ops/cong_cu.py" kiem-tra --chi "$TEN" --json\nelse\n',
      'if false; then\n  :\nelse\n'),
     ["r1045_bat_buoc_cong_cu_tuy_chon_thieu_khong_chan_cong_cu_sau", "r1045_hinh_dang_dat_theo_trang_thai"], "cai_sh"),
    ("wp858_sh_khong_ung_vien_van_rc0",
     ("chay duoc\" >&2; return 1; }", "chay duoc\" >&2; return 0; }"),
     ["r858_cai_macos_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp858_sh_github_path_khong_qua_cygpath",
     ('      w="$(cygpath -w "$dich")" || { echo "cai_cong_cu: cygpath -w hong cho \'$dich\'" >&2; return 1; }',
      '      w="$dich"'),
     ["r858_cai_windows_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp858_sh_bo_cygpath_u",
     ('      d="$(cygpath -u "$d")" || { echo "cai_cong_cu: cygpath -u hong cho ung vien cua \'$ten\'" >&2; return 1; }',
      '      :'),
     ["r858_cai_windows_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp858_sh_nuot_loi_cygpath_w",
     ('w="$(cygpath -w "$dich")" || { echo "cai_cong_cu: cygpath -w hong cho \'$dich\'" >&2; return 1; }',
      'w="$(cygpath -w "$dich")"'),
     ["r858_cai_windows_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp858_sh_nuot_loi_ghi_github_path",
     ('printf \'%s\\n\' "$w" >> "$GITHUB_PATH" || { echo "cai_cong_cu: khong ghi duoc \\$GITHUB_PATH" >&2; return 1; }',
      'printf \'%s\\n\' "$w" >> "$GITHUB_PATH"'),
     ["r858_cai_linux_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    # wp868 (Q3): dòng canh `/dev/null` trên stdout thay bằng `GIU_PATH` trên kênh riêng; ba đột biến dòng canh đổi neo.
    ("wp858_sh_bo_dong_canh_giu_path",
     ('    printf \'GIU_PATH\' > "$KENH_KQ" || { echo "cai_cong_cu: khong ghi duoc kenh ket qua" >&2; return 1; }\n', ''),
     ["r858_bat_buoc_bash_khong_dua_rg_hong_len_dau", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp858_sh_cygpath_u_hong_khong_tra_loi",
     ("cygpath -u hong cho ung vien cua '$ten'\" >&2; return 1; }", "cygpath -u hong cho ung vien cua '$ten'\" >&2; }"),
     ["r858_cai_windows_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp858_sh_dong_canh_la_ten_thu_muc",
     ("    printf 'GIU_PATH' > \"$KENH_KQ\"", "    printf 'DICH\\n%s' :giu-nguyen-PATH: > \"$KENH_KQ\""),
     ["r858_bat_buoc_bash_khong_dua_rg_hong_len_dau", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    # Codex wp858 lượt 1–3: F858-01/02/03/04/06.
    ("wp858_sh_dong_canh_khong_tach_dong", ('  GIU_PATH) DICH="" ;;', '  GIU_PATH) DICH="$(tail -n 1 "$TAM_CAI/stdout")" ;;'),
     ["r858_bat_buoc_bash_khong_dua_rg_hong_len_dau", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp858_sh_cygpath_u_chi_khi_ghi_path",
     ('    if [ -n "$win" ]; then\n      d="$(cygpath -u', '    if [ -n "$win" ] && [ -n "${GITHUB_PATH:-}" ]; then\n      d="$(cygpath -u'),
     ["r858_cai_windows_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp858_sh_github_path_vang_khong_mac_dinh", ('  if [ -n "${GITHUB_PATH:-}" ]; then', '  if [ -n "$GITHUB_PATH" ]; then'),
     ["r858_cai_linux_chon_ban_chay_duoc", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    # wp868 (N1–N5): mỗi đột biến kèm ca hình dạng thuần Python để đo được cả Windows.
    ("wp868_sh_ham_in_stdout_thay_kenh",
     ("  printf 'DICH\\n%s' \"$dich\" > \"$KENH_KQ\" || { echo \"cai_cong_cu: khong ghi duoc kenh ket qua\" >&2; return 1; }",
      "  printf '\\n%s\\n' \"$dich\""),
     ["r868_kenh_rieng_khong_doc_stdout_trinh_cai", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp868_sh_doc_stdout_thay_kenh", ("  DICH$'\\n'?*) DICH=\"${KQ#DICH$'\\n'}\" ;;", "  DICH$'\\n'?*) DICH=\"$(tail -n 1 \"$TAM_CAI/stdout\")\" ;;"),
     ["r868_kenh_rieng_khong_doc_stdout_trinh_cai", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_kenh_export", ("declare +x KENH_KQ\n", "export KENH_KQ\n"),
     ["r868_kenh_rieng_khong_doc_stdout_trinh_cai", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_cho_eof_stdout", ('( set +e; eval "$LENH" ) > "$TAM_CAI/stdout"', 'printf \'%s\\n\' "$(eval "$LENH")" > "$TAM_CAI/stdout"'),
     ["r868_writer_muon_khong_lam_treo", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_bo_duong_lui_dong_cuoi", ('    KET_QUA_CAI="$(cat -- "$TAM_CAI/stdout")"', '    KET_QUA_CAI=""'),
     ["r868_khong_bo_chon_doc_dong_cuoi", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    # Codex lượt 1: F868-01 (đọc kênh nuốt lỗi) · F868-02 (bỏ trap EXIT) · F868-03 (đường lùi bỏ cắt CR).
    ("wp868_sh_doc_kenh_nuot_loi", ('KQ="$(cat -- "$KENH_KQ" && printf x)"', 'KQ="$(cat -- "$KENH_KQ"; printf x)"'),
     ["r868_doc_kenh_hong_thi_dung", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_bo_trap_exit", ("trap 'rm -rf -- \"$TAM_CAI\"' EXIT\n", ":\n"),
     ["r868_don_kenh_khi_loi", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_duong_lui_bo_cat_cr", ("    DICH=\"${DICH%$'\\r'}\" ;;", "    ;;"),
     ["r868_khong_bo_chon_doc_dong_cuoi", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    # Codex lượt 2: F868-04 (nuốt lỗi ghi payload, hai nhánh) · F868-05 (nhận payload sai giao thức).
    ("wp868_sh_ghi_giu_path_nuot_loi",
     ("printf 'GIU_PATH' > \"$KENH_KQ\" || { echo \"cai_cong_cu: khong ghi duoc kenh ket qua\" >&2; return 1; }",
      "printf 'GIU_PATH' > \"$KENH_KQ\" || { echo \"cai_cong_cu: khong ghi duoc kenh ket qua\" >&2; return 0; }"),
     ["r868_ghi_kenh_hong_thi_dung", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_ghi_dich_nuot_loi",
     ("printf 'DICH\\n%s' \"$dich\" > \"$KENH_KQ\" || { echo \"cai_cong_cu: khong ghi duoc kenh ket qua\" >&2; return 1; }",
      "printf 'DICH\\n%s' \"$dich\" > \"$KENH_KQ\" || { echo \"cai_cong_cu: khong ghi duoc kenh ket qua\" >&2; return 0; }"),
     ["r868_ghi_kenh_hong_thi_dung", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_kenh_rac_rc0", ("printf '%q' \"$KQ\")\" >&2; exit 7 ;;", "printf '%q' \"$KQ\")\" >&2; exit 0 ;;"),
     ["r868_doc_kenh_hong_thi_dung", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_tam_export", ("declare +x TAM_CAI\n", "export TAM_CAI\n"),
     ["r868_kenh_rieng_khong_doc_stdout_trinh_cai", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_bo_rm_tuong_minh", ('rm -rf -- "$TAM_CAI"\n[ -d "$DICH" ]', '[ -d "$DICH" ]'),
     ["r868_don_kenh_khi_loi", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    # Codex lượt 3: F868-06 — gán lại SAU `declare +x` (allexport tự export lại).
    ("wp868_sh_gan_lai_kenh_sau_go_export", ('declare +x KENH_KQ\n: > "$KENH_KQ"', 'declare +x KENH_KQ\nKENH_KQ="$KENH_KQ"\n: > "$KENH_KQ"'),
     ["r868_kenh_rieng_khong_doc_stdout_trinh_cai", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_gan_lai_tam_sau_go_export", ("declare +x TAM_CAI\ntrap ", 'declare +x TAM_CAI\nTAM_CAI="$TAM_CAI"\ntrap '),
     ["r868_kenh_rieng_khong_doc_stdout_trinh_cai", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    # Codex lượt 4: F868-02 mở lại — gỡ trap SAU khi công thức chạy ⇒ hai đường `exit 7` của reader rò thư mục kênh.
    ("wp868_sh_go_trap_sau_eval", ('( set +e; eval "$LENH" ) > "$TAM_CAI/stdout"\n', '( set +e; eval "$LENH" ) > "$TAM_CAI/stdout"\ntrap - EXIT\n'),
     ["r868_doc_kenh_hong_thi_dung", "r868_hinh_dang_kenh_ket_qua"], "cai_sh"),
    ("wp868_sh_chi_duyet_hai_ung_vien", ('  for d in "$@"; do', '  for d in "${@:1:2}"; do'),
     ["r868_vong_duyet_ung_vien", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp868_sh_bo_break", ('then dich="$d"; break; fi', 'then dich="$d"; fi'),
     ["r868_vong_duyet_ung_vien", "r858_hinh_dang_cong_thuc_cai"], "cai_sh"),
    ("wp868_yaml_rg_linux_ve_bo_chon_rieng",
     ('sudo apt-get install -y ripgrep && chon_thu_muc_chay_duoc rg "${CONG_CU_GOC:-}/usr/bin" "$(dirname "$(command -v rg || echo ./rg)")"',
      'sudo apt-get install -y ripgrep && RG_D="${CONG_CU_GOC:-}/usr/bin" && echo "$RG_D"'),
     ["r868_kenh_rieng_khong_doc_stdout_trinh_cai", "r858_hinh_dang_cong_thuc_cai"], "yaml"),
    # wp886 (N1–N6, Q1): đột biến BẢN SAO `ops/cong_cu.py`; mỗi đột biến có ít nhất một ca đích chạy được trên Windows.
    ("wp886_cc_ve_sys_executable", ("        argv = [*py, *argv[1:]]", "        argv = [sys.executable, *argv[1:]]"),
     ["r886_n1_ten_tran_theo_path_moi_nen", "r886_n2_python_hong_dau_path_khong_DAT",
      "r858_cai_python_khong_in_thu_muc_ban_hong"], "cong_cu"),
    ("wp886_cc_python3_truoc_python", ('TEN_PYTHON = (("python",), ("python3",), ("py", "-3"))',
                                       'TEN_PYTHON = (("python3",), ("python",), ("py", "-3"))'),
     ["r886_n2_python_hong_dau_path_khong_DAT", "r886_ten_python_khop_cai_cong_cu_sh"], "cong_cu"),
    ("wp886_cc_bo_python3", ('TEN_PYTHON = (("python",), ("python3",), ("py", "-3"))', 'TEN_PYTHON = (("python",), ("py", "-3"))'),
     ["r886_n3_chi_python3_DAT_va_do_dung_interpreter", "r886_ten_python_khop_cai_cong_cu_sh"], "cong_cu"),
    ("wp886_cc_py_mat_tru_3", ('TEN_PYTHON = (("python",), ("python3",), ("py", "-3"))', 'TEN_PYTHON = (("python",), ("python3",), ("py",))'),
     ["r886_n6_giai_ten_tinh_windows_va_posix", "r886_ten_python_khop_cai_cong_cu_sh"], "cong_cu"),
    ("wp886_cc_khong_ten_roi_ve_sys_executable",
     ('            return None, "", "khong_khoi_chay:khong co " + ", ".join(t[0] for t in TEN_PYTHON) + " tren PATH"',
      '            py = [sys.executable]'),
     ["r886_n4_khong_ten_nao_noi_ro_thieu_gi"], "cong_cu"),
    ("wp886_cc_bo_ly_do_thieu_ten", ("cua '{ten}' ({'; '.join(ly_do)})\"}", "cua '{ten}'\"}"),
     ["r886_n4_khong_ten_nao_noi_ro_thieu_gi"], "cong_cu"),
    ("wp886_cc_windows_nhan_ten_tran", ('        duoi = ([""] if any(ten.upper().endswith(e.upper()) for e in ext) else []) + ext',
                                        '        duoi = [""] + ext'),
     ["r886_n6_giai_ten_tinh_windows_va_posix"], "cong_cu"),
    ("wp886_cc_bo_muc_PATH_rong",
     ('    for muc in (os.environ.get("PATH", "") if path is None else path).split(os.pathsep):\n        for d in duoi:',
      '    for muc in filter(None, (os.environ.get("PATH", "") if path is None else path).split(os.pathsep)):\n        for d in duoi:'),
     ["r886_n6_giai_ten_tinh_windows_va_posix"], "cong_cu"),
    ("wp886_cc_bo_X_OK", ("            if os.path.isfile(p) and os.access(p, os.X_OK):\n                return os.path.abspath(p)\n    return None\n\ndef _python_theo_path",
                          "            if os.path.isfile(p):\n                return os.path.abspath(p)\n    return None\n\ndef _python_theo_path"),
     ["r886_n1_bo_qua_tep_khong_thuc_thi"], "cong_cu"),
    ("wp886_cc_dao_thu_tu_PATH",
     ('    for muc in (os.environ.get("PATH", "") if path is None else path).split(os.pathsep):\n        for d in duoi:',
      '    for muc in reversed((os.environ.get("PATH", "") if path is None else path).split(os.pathsep)):\n        for d in duoi:'),
     ["r886_n6_giai_ten_tinh_windows_va_posix"], "cong_cu"),
    ("wp886_cc_path_truoc_ten",
     ('    for ten, *them in TEN_PYTHON:\n        p = _giai_ten_tran(ten, path, pathext, la_windows)\n',
      '    for muc in (os.environ.get("PATH", "") if path is None else path).split(os.pathsep):\n'
      '      for ten, *them in TEN_PYTHON:\n        p = _giai_ten_tran(ten, muc, pathext, la_windows)\n'),
     ["r886_n6_giai_ten_tinh_windows_va_posix"], "cong_cu"),
    ("wp858_selftest_editskill_ten_co_dinh",
     ('    _esd = Path(_tfx.mkdtemp(prefix="_selftest_editskill_"))\n    _esf = _esd / "_selftest_editskill.py"',
      '    _esd = Path(_tfx.gettempdir())\n    _esf = _esd / "_selftest_editskill.py"'),
     ["r858_selftest_editskill_thu_muc_rieng"], "selftest"),
    # #1079 F01 (c): đột biến BẢN SAO `codex_cred_test.py` (phần tử thứ tư "cc_test").
    ("wp1079_cc_bo_kiem_kieu", ("    if type(e) is not AssertionError or e.__traceback__ is None:",
                                "    if e.__traceback__ is None:"),
     ["r1079_cc_test_chi_chot_cua_suite_la_do"], "cc_test"),
    ("wp1079_cc_bo_kiem_tep", ("    return (os.path.realpath(tep) == os.path.realpath(__file__)\n", "    return (True\n"),
     ["r1079_cc_test_chi_chot_cua_suite_la_do"], "cc_test"),
    ("wp1079_cc_bo_kiem_dong_assert", ('            and linecache.getline(tep, tb.tb_lineno).lstrip().startswith("assert"))',
                                       "            and True)"),
     ["r1079_cc_test_chi_chot_cua_suite_la_do"], "cc_test"),
    ("wp1079_cc_ten_do_bo_loai", ('    if not la_chot_cua_suite(e):\n        return f"{ten}({type(e).__name__})"',
                                  '    if False:\n        return f"{ten}({type(e).__name__})"'),
     ["r1079_cc_test_chi_chot_cua_suite_la_do"], "cc_test"),
    # F03 (Codex lượt 1): đổi câu thực thi nhưng GIỮ lời gọi cũ trong chú thích — chỉ ca hành vi giết được.
    ("wp1079_cc_bo_kiem_ca_khac", ("        if tb.tb_frame.f_code in khac:\n            return f\"{ten}(chot cua ca khac)\"",
                                   "        if False:\n            return f\"{ten}(chot cua ca khac)\""),
     ["r1079_review_credential_chot_ca_khac_khong_la_giet"], "cc_test"),
    ("wp1079_cc_cho_trung_ma", ("    if len({c.__code__ for c in CA}) != len(CA):", "    if False:"),
     ["r1079_ca_trung_ma_bi_tu_choi_luc_dang_ky"], "cc_test"),
    ("wp1079_cc_chay_suite_bo_ten_do", ("            do.add(ten_do(ca.__name__, e, ca))",
                                        "            do.add(ca.__name__)  # do.add(ten_do(ca.__name__, e, ca))"),
     ["r1079_cc_chay_suite_phai_do_hanh_vi"], "cc_test"),
]


DOT_BIEN_HARNESS = [
    # Hai dòng fixture mới phải dùng đúng tên `MODULE_PY`; đổi phối hợp cả hai về
    # tên chết từng sống sót vẫn phải làm cả hai ca canh đỏ.
    ("fixture_MODULE_PY_quay_lai_ten_chet",
     [('    m.CONG_CU = [muc]\n    m.MODULE_PY = []',
       '    m.CONG_CU = [muc]\n    m.MO_DUN_PY = []'),
      ('    m.CONG_CU = []\n    m.MODULE_PY = []',
       '    m.CONG_CU = []\n    m.MO_DUN_PY = []')],
     ["t129_probe_qua_han_la_CHUA_DO_khong_phai_THIEU",
      "t134_kiem_song_dang_bat_thi_footer_khong_khuyen_bat_lai"]),
    # Nới điều kiện thành "cứ thiếu là tha" sẽ che regression ngay trong checkout thật.
    ("ban_sao_roi_tha_ca_kho_that",
     ('    if thieu and not (goc / ".git").exists():',
      '    if thieu:'),
     ["t142_ban_sao_roi_chi_duoc_tha_khi_goc_vang_git"]),
    # Mẫu số của headline là số ca đã chạy, không phải tổng gồm cả ca tự bỏ qua.
    ("headline_lay_tong_lam_so_ca_da_chay",
     ('    da_chay = tong - bo_qua',
      '    da_chay = tong'),
     ["t118_headline_KHONG_duoc_dem_ca_BO_QUA_la_da_qua",
      "t119_main_nhanh_mac_dinh_PHAI_in_headline_bang_dong_ket_qua"]),
    # wp766: bo phep tranh PID cua luot chay => fixture t81 quay ve PID ghi cung, va
    # luot chay co getpid trung mot PID gia lai do (Codex review PR #765).
    ("pid_gia_quay_ve_ghi_cung",
     ('    tranh = {os.getpid(), os.getppid()}',
      '    tranh = set()'),
     ["r766_t81_khong_phu_thuoc_pid_cua_luot_chay"]),
    # J01 (Codex lượt 4): bỏ bộ lọc môi trường thì BASH_ENV của máy chạy lại lọt vào hook.
    ("wp802_runner_bo_tra_con_tro_hook", ('HOOK_DANG_DUNG, YAML_DANG_DUNG = hook_goc, yaml_goc',
     'HOOK_DANG_DUNG, YAML_DANG_DUNG = HOOK_DANG_DUNG, yaml_goc'), ["r802_runner_tra_lai_con_tro_nguoi_goi"]),
    ("wp802_runner_bo_tra_con_tro_yaml", ('HOOK_DANG_DUNG, YAML_DANG_DUNG = hook_goc, yaml_goc',
     'HOOK_DANG_DUNG, YAML_DANG_DUNG = hook_goc, YAML_DANG_DUNG'), ["r802_runner_tra_lai_con_tro_nguoi_goi"]),
    ("g8_fixture_chep_nguyen_moi_truong",
     ('               if k not in ("BASH_ENV", "ENV") and not k.startswith("BASH_FUNC_")}',
      '               if True}'),
     ["r484_g8_hook_scrub_kin_voi_bash_env"]),
    # wp858 (N5): bộ chọn gốc tạm của `t86` bỏ kiểm tổ tiên ⇒ `/tmp/.git` của sandbox Codex lọt lại.
    ("wp858_goc_tam_bo_kiem_to_tien",
     ('not any(os.path.lexists(q / ".git") for q in (p, *p.parents))', 'not os.path.lexists(p / ".git")'),
     ["r858_goc_tam_tranh_to_tien_co_git"]),
    # #1079 F01 (a)(b) + F02: mỗi chốt mới một đột biến; chỉ `TinHieuChotCa` của ca đích là giết.
    ("wp1079_cham_mot_ca_nhan_AssertionError",
     ('    except TinHieuChotCa as e:\n        if not chot_tu_ca_khac(e, fn):', '    except AssertionError as e:\n        if not chot_tu_ca_khac(e, fn):'),
     ["r1079_cham_mot_ca_chi_TinHieuChotCa_la_giet"]),
    ("wp1079_ket_luan_bo_neutral",
     ('    xau = [neutral[t][1] for t in dich if neutral[t][0] in ("giet", "loi")]', '    xau = []'),
     ["r1079_ket_luan_mutant_neutral_do_khong_cap_tin_dung"]),
    ("wp1079_ket_luan_dem_tin_dung_gia",
     ('    return ("OK" if len(chet) == can_do else "SAI")', '    return ("OK" if len(chet) + len(gia) == can_do else "SAI")'),
     ["r1079_ket_luan_mutant_neutral_do_khong_cap_tin_dung"]),
    ("wp1079_lap_ca_bo_kiem_nonce",
     ('    if kq.get("nonce") != nonce or kq.get("ten") != ten_ca:', '    if kq.get("ten") != ten_ca:'),
     ["r1079_cham_lap_ca_doi_dung_TinHieuChotCa"]),
    ("wp1079_lap_ca_tin_stdout",
     ('        kq = json.loads(kenh.read_text(encoding="utf-8")) if kenh.is_file() else {}',
      '        kq = json.loads(kenh.read_text(encoding="utf-8")) if kenh.is_file() else (\n'
      '            {"nonce": nonce, "ten": ten_ca, "hong": 1, "loai": "TinHieuChotCa"}\n'
      '            if p.returncode == 1 and f"LAP {ten_ca}: 0/1 qua" in p.stdout else {})'),
     ["r1079_cham_lap_ca_doi_dung_TinHieuChotCa", "r1079_harness_duoi_stdout_gia_khong_cap_tin_dung"]),
    ("wp1079_bao_cao_theo_ten_lop",   # bản lỗi gốc ghi `__name__` ở CẢ HAI nhánh except
     [('            LOAI_HONG[fn.__name__] = ("TinHieuChotCa" if isinstance(e, TinHieuChotCa) and not chot_tu_ca_khac(e, fn)\n'
       '                                      else f"khac:{type(e).__qualname__}")',
       '            LOAI_HONG[fn.__name__] = type(e).__name__'),
      ('            LOAI_HONG[fn.__name__] = f"khac:{type(e).__qualname__}"\n            ket = f"LOI',
       '            LOAI_HONG[fn.__name__] = type(e).__name__\n            ket = f"LOI')],
     ["r1079_harness_trung_ten_loai_khong_cap_tin_dung"]),
    # Codex lượt 2: F05 nguồn gốc chốt · F06 ca đích vắng · F01 tiền tố `khac:`.
    ("wp1079_bo_kiem_ca_khac", ("        if tb.tb_frame.f_code in khac:\n            return True\n        tb = tb.tb_next\n    return False",
                                "        if False:\n            return True\n        tb = tb.tb_next\n    return False"),
     ["r1079_review_san_pham_chot_ca_khac_khong_la_giet", "r1079_review_harness_chot_ca_khac_khong_la_giet"]),
    ("wp1079_ca_cho_trung_ma", ("def ca(fn):\n    kiem_registry([*CA, fn])\n", "def ca(fn):\n"),
     ["r1079_ca_trung_ma_bi_tu_choi_luc_dang_ky"]),
    ("wp1079_registry_bo_kiem_chay_dot_bien",
     ("    kiem_registry(CA)   # #1079 F08 (Codex lượt 5): gọi thẳng `chay_dot_bien` cũng phải qua chốt\n", ""),
     ["r1079_registry_nhanh_hook_tu_choi_truoc_chay"]),
    ("wp1079_registry_bo_kiem_cham_mot_ca",
     ("    kiem_registry(CA)   # #1079 F08 (Codex lượt 6): TRƯỚC khi thân ca chạy\n", ""),
     ["r1079_review6_cham_mot_ca_kiem_registry_truoc_chay"]),
    ("wp1079_registry_bo_kiem_chay_bo_ca",
     ("    kiem_registry(CA)   # #1079 F08 (Codex lượt 6): TRƯỚC khi ca đầu tiên chạy\n", ""),
     ["r1079_review6_chay_bo_ca_kiem_registry_truoc_chay"]),
    ("wp1079_bo_kiem_ca_dich_vang", ("            if sorted(fn.__name__ for fn in dich) != sorted(set(phai_chet)):   # #1079 F06",
                                     "            if False:   # #1079 F06"),
     ["r1079_review_ca_dich_vang_phai_lam_cong_do", "r1079_chay_dot_bien_noi_neutral_va_cham_theo_loai"]),
    ("wp1079_bo_tien_to_khac", [('                                      else f"khac:{type(e).__qualname__}")',
                                 '                                      else type(e).__qualname__)'),
                                ('            LOAI_HONG[fn.__name__] = f"khac:{type(e).__qualname__}"\n            ket = f"LOI',
                                 '            LOAI_HONG[fn.__name__] = type(e).__qualname__\n            ket = f"LOI')],
     ["r1079_review_lop_khac_cung_qualname_khong_la_chot"]),
    ("wp1079_n13_do_bash_ngoai_env_sach",
     ('        with patch.dict(os.environ, env, clear=True):\n            vo, chan_doan',
      '        with patch.dict(os.environ, {}):\n            vo, chan_doan'),
     ["r1079_n13_do_bash_cung_phai_loc_env_cha"]),
    ("wp1079_neutral_san_pham_bo",
     ('                    LAUNCHER_DANG_DUNG = LAUNCHER\n                    neutral[fn.__name__] = cham_mot_ca(fn)\n',
      '                    neutral[fn.__name__] = ("qua", fn.__name__)\n'),
     ["r1079_chay_dot_bien_noi_neutral_va_cham_theo_loai"]),
    # #1122 (spec wp1122 A2): chi tiết `loi` mang thông điệp cắt 160 ký tự.
    ("wp1122_loi_bo_thong_diep",
     ('        return "loi", f"{fn.__name__}({mo_ta_loi(e)})"', '        return "loi", f"{fn.__name__}({type(e).__name__})"'),
     ["r1122_loi_mang_thong_diep_cat_160"]),
    ("wp1122_doi_tran_cat", ("TRAN_THONG_DIEP_LOI = 160\n", "TRAN_THONG_DIEP_LOI = 80\n"),
     ["r1122_loi_mang_thong_diep_cat_160"]),
    # #1122 (spec wp1122 A1): chèn lại một `assert` trần · nới danh sách cho phép bằng một tên không có `assert`.
    ("wp1122_chen_lai_assert_tran",
     ('        bang(not accepted, "same native SID rejected because of SDDL alias")',
      '        assert not accepted, "same native SID rejected because of SDDL alias"'),
     ["r1122_khong_assert_tran_trong_ca"]),
    ("wp1122_chen_lai_raise_assertion",
     ('bang(False, "Windows ancestor was not pinned")', 'raise AssertionError("Windows ancestor was not pinned")'),
     ["r1122_khong_assert_tran_trong_ca"]),
    ("wp1122_chay_bo_encoding",
     ('                          text=True, encoding="utf-8", errors="replace", cwd=cwd, env=env)',
      '                          text=True, cwd=cwd, env=env)'),
     ["r1122_con_python_giai_ma_utf8"]),
    ("wp1122_noi_danh_sach_cho_phep",
     ('    "t119_main_nhanh_mac_dinh_PHAI_in_headline_bang_dong_ket_qua"})',
      '    "t119_main_nhanh_mac_dinh_PHAI_in_headline_bang_dong_ket_qua", "t73_doctor_phai_do_bash_va_npm"})'),
     ["r1122_khong_assert_tran_trong_ca"]),
    ("wp1079_neutral_harness_bo",
     ('                    neutral_h[ten_ca] = cham_lap_ca(goc_h, ten_ca)\n', '                    neutral_h[ten_ca] = ("qua", ten_ca)\n'),
     ["r1079_chay_dot_bien_noi_neutral_va_cham_theo_loai"]),
    ("wp1079_n13_bo_rg_gia",
     ('        for tool in ("rg", "actionlint"):\n            (fakebin / tool).write_text(f"#!/bin/sh\\necho \'{tool} 1.0 (gia)\'',
      '        for tool in ():\n            (fakebin / tool).write_text(f"#!/bin/sh\\necho \'{tool} 1.0 (gia)\''),
     ["r484_g7_hook_vang_codex_cai_cli_truoc_materialize"]),
    ("wp1079_n13_bo_shim_installer",
     ('        for tool in cai:\n            (fakebin / tool)', '        for tool in ():\n            (fakebin / tool)'),
     ["r484_g7_hook_vang_codex_cai_cli_truoc_materialize"]),
    ("wp1079_n13_bo_loc_bash_env",
     ('        env = {k: v for k, v in cha.items() if k not in ("BASH_ENV", "ENV") and not k.startswith("BASH_FUNC_")}',
      '        env = dict(cha)'),
     ["r484_g7_hook_vang_codex_cai_cli_truoc_materialize"]),
]


def chay_dot_bien() -> int:
    """Chạy đột biến trên BẢN SAO TẠM, KHÔNG bao giờ ghi vào launcher.py thật.

    ĐÃ TRẢ GIÁ (2026-08-12): bản trước ghi thẳng vào launcher.py rồi khôi phục
    trong `finally`. Một lượt chạy bị SIGTERM cắt giữa chừng thì `finally` KHÔNG
    chạy, tệp thật ở lại trạng thái đã méo (`if False:` thay cho chốt chống giết
    nhầm PID) — và lượt đột biến KẾ TIẾP đọc đúng bản méo đó làm "bản gốc", khôi
    phục về nó, xoá luôn bản sao. Bản méo đi thẳng vào commit và đã được đẩy lên.
    Dấu hiệu duy nhất lộ ra là một đột biến báo "khong tim thay doan de dot bien":
    đoạn cần sửa đã bị chính nó thay mất từ lượt trước.

    Sửa ở TẦNG chứ không vá triệu chứng: tệp dưới quản lý phiên bản không bao giờ
    bị ghi, nên dù bị SIGKILL (không bắt được) cây làm việc vẫn nguyên.
    """
    global LAUNCHER_DANG_DUNG, HOOK_DANG_DUNG, YAML_DANG_DUNG, CAI_SH_DANG_DUNG, SELFTEST_DANG_DUNG, CONG_CU_DANG_DUNG, CC_TEST_DANG_DUNG
    kiem_registry(CA)   # #1079 F08 (Codex lượt 5): gọi thẳng `chay_dot_bien` cũng phải qua chốt
    goc = LAUNCHER.read_text(encoding="utf-8")
    goc_test = Path(__file__).read_text(encoding="utf-8")
    hong = 0
    khong_do = 0
    neutral = {}
    neutral_h = {}
    tam = Path(tempfile.mkdtemp(prefix="lt_db_"))
    try:
        # Preserve the real delegated probe dependency in neutral/mutant copies.
        # Otherwise t133 fails before reaching the mutation and reports a false kill.
        companion = LAUNCHER.with_name("codex_cred.py")
        if companion.is_file():
            shutil.copy2(companion, tam / companion.name)
        for muc in DOT_BIEN:
            ten, cap, phai_chet = muc[0], muc[1], muc[2]
            # Phan tu thu TU (tuy chon) = ('posix'|'windows', ly do). Co dot bien
            # KHONG THE do duoc tren mot nen du ca dich VAN CHAY: vd t71 tu bo qua
            # dung khang dinh ve quyen/xoa ban chup tren Windows. Truoc day nhung ca
            # do bao SAI oan, va mot cong khong bao gio xanh duoc thi nguoi ta se bo
            # qua no - dung bay da ghi trong chu thich `can_do` ben duoi.
            # LY DO la BAT BUOC va duoc IN RA, de day khong thanh cho giau that bai.
            gioi_han = muc[3] if len(muc) > 3 else None
            if gioi_han:
                nen, ly_do = gioi_han
                if (nen == "posix") == LA_WINDOWS:
                    khong_do += 1
                    print(f"  {ten:<28} KHONG DO DUOC tren nen nay ({ly_do})")
                    continue
            if isinstance(cap, tuple):
                cap = [cap]
            thieu = [c for c, _ in cap if c not in goc]
            if thieu:
                print(f"  {ten:<28} SAI - khong tim thay doan de dot bien")
                hong += 1
                continue
            moi_ma = goc
            for c, m in cap:
                moi_ma = moi_ma.replace(c, m, 1)
            # TÊN RIÊNG cho từng đột biến. Bản trước ghi đè CÙNG một `launcher.py`,
            # và hai đột biến cùng kích thước rơi vào cùng một giây thì bản sau ăn
            # `.pyc` của bản trước — cổng chấm điểm nhầm bản (xem `_nap_sach`).
            # Đường dẫn khác nhau ⇒ đường `.pyc` khác nhau ⇒ va chạm là bất khả.
            ban_sao = tam / f"launcher_db_{DOT_BIEN.index(muc):02d}.py"
            ban_sao.write_text(moi_ma, encoding="utf-8")
            try:
                compile(moi_ma, str(ban_sao), "exec")
            except SyntaxError as e:
                print(f"  {ten:<28} SAI - dot bien khong bien dich: {e.msg}")
                hong += 1
                continue
            dich = [fn for fn in CA if fn.__name__ in phai_chet]
            if sorted(fn.__name__ for fn in dich) != sorted(set(phai_chet)):   # #1079 F06
                hong += 1
                print(f"  {ten:<28} SAI - ca dich khong tim thay/trung: "
                      f"{sorted(set(phai_chet) - {fn.__name__ for fn in dich})}")
                continue
            for fn in dich:   # #1079 F01: NEUTRAL trên bản gốc, mỗi ca đo một lần
                if fn.__name__ not in neutral:
                    LAUNCHER_DANG_DUNG = LAUNCHER
                    neutral[fn.__name__] = cham_mot_ca(fn)
            LAUNCHER_DANG_DUNG = ban_sao
            # Ca TỰ BỎ QUA trên nền này thì đột biến KHÔNG ĐO ĐƯỢC, chứ không phải "test yếu"
            # (audit codex: Windows t03/t50). Chỉ `TinHieuChotCa` mới là giết (`cham_mot_ca`).
            tt, so_chet, can_do, mo_ta = ket_luan_mutant(
                [fn.__name__ for fn in dich], neutral, {fn.__name__: cham_mot_ca(fn) for fn in dich})
            if tt == "KHONG_DO":
                khong_do += 1
                print(f"  {ten:<28} KHONG DO DUOC tren nen nay (ca dich bo qua: {mo_ta})")
                continue
            if tt == "KHONG_DO_NEUTRAL":
                hong += 1
                print(f"  {ten:<28} SAI - KHONG DO DUOC (neutral do: {mo_ta})")
                continue
            hong += 0 if tt == "OK" else 1
            print(f"  {ten:<28} {tt}  giet {so_chet}/{can_do}: {mo_ta}")

        # wp802: đột biến HOOK — cùng luật bản sao tạm; chỉ `TinHieuChotCa` mới là giết.
        hook_goc, yaml_goc = HOOK_DANG_DUNG, YAML_DANG_DUNG   # F3: trả ĐÚNG con trỏ người gọi
        cai_sh_goc, selftest_goc, cong_cu_goc = CAI_SH_DANG_DUNG, SELFTEST_DANG_DUNG, CONG_CU_DANG_DUNG
        cc_test_goc = CC_TEST_DANG_DUNG
        for i, muc in enumerate(DOT_BIEN_HOOK):
            ten, (c, m), phai_chet = muc[:3]
            loai = muc[3] if muc[3:] else "hook"
            dich = {"yaml": yaml_goc, "cai_sh": cai_sh_goc, "selftest": selftest_goc,
                    "cong_cu": cong_cu_goc, "cc_test": cc_test_goc}.get(loai, hook_goc)
            goc_dich = dich.read_text(encoding="utf-8")
            if goc_dich.count(c) != 1:
                print(f"  {ten:<28} SAI - neo hook/yaml khong khop DUNG MOT cho")
                hong += 1
                continue
            ban = tam / f"hook_db_{i:02d}{dich.suffix}"
            ban.write_text(goc_dich.replace(c, m, 1), encoding="utf-8")
            globals()[{"yaml": "YAML_DANG_DUNG", "cai_sh": "CAI_SH_DANG_DUNG",
                       "selftest": "SELFTEST_DANG_DUNG", "cong_cu": "CONG_CU_DANG_DUNG",
                       "cc_test": "CC_TEST_DANG_DUNG"}.get(loai, "HOOK_DANG_DUNG")] = ban
            chet, bo_qua, loi = [], [], []
            try:
                for fn in [f for f in CA if f.__name__ in phai_chet]:
                    try:
                        with _co_lap_toan_cuc():
                            if isinstance(fn(), str):
                                bo_qua.append(fn.__name__)
                    except TinHieuChotCa:
                        chet.append(fn.__name__)
                    except Exception as e:  # noqa: BLE001 - tín dụng giả, không phải giết
                        loi.append(f"{fn.__name__}({mo_ta_loi(e)})")
            finally:
                HOOK_DANG_DUNG, YAML_DANG_DUNG = hook_goc, yaml_goc
                CAI_SH_DANG_DUNG, SELFTEST_DANG_DUNG, CONG_CU_DANG_DUNG = cai_sh_goc, selftest_goc, cong_cu_goc
                CC_TEST_DANG_DUNG = cc_test_goc
            can_do = len(phai_chet) - len(bo_qua)
            if can_do == 0 and not loi:
                khong_do += 1
                print(f"  {ten:<28} KHONG DO DUOC tren nen nay (ca dich bo qua: {', '.join(bo_qua)})")
                continue
            ok = len(chet) == can_do and not loi
            hong += 0 if ok else 1
            print(f"  {ten:<28} {'OK' if ok else 'SAI'}  giet {len(chet)}/{can_do}: "
                  f"{', '.join(chet + loi) or '(khong ca nao chet)'}")

        # Mutant của chính harness phải chạy trên BẢN SAO của CẢ tệp test. Runner
    # sản phẩm chỉ thay launcher.py nên không thể đo ba finding test-only
        # (`MODULE_PY`, điều kiện bản-sao-rời, mẫu số headline).
        phan_truoc_bang, dau_bang, sau_dau_bang = goc_test.partition(
            "\nDOT_BIEN_HARNESS = [")
        than_bang, dau_ham_runner, phan_sau_bang = sau_dau_bang.partition(
            "\n]\n\n\ndef chay_dot_bien()")
        if not dau_bang or not dau_ham_runner:
            print("  !! khong tach duoc bang dot bien harness khoi ma can dot bien")
            hong += len(DOT_BIEN_HARNESS)
            phan_ma_test = goc_test
        else:
            # Bỏ chính bảng đặc tả ra khỏi vùng đếm/thay; code cần đột biến nằm ở
            # CẢ trước và sau bảng (`dong_ket_qua` được định nghĩa sau runner).
            phan_ma_test = phan_truoc_bang + "\n\n\ndef chay_dot_bien()" + phan_sau_bang
        for i, muc in enumerate(DOT_BIEN_HARNESS):
            ten, cap, phai_chet = muc
            if isinstance(cap, tuple):
                cap = [cap]
            sai_neo = [c for c, _ in cap if phan_ma_test.count(c) != 1]
            if sai_neo:
                print(f"  {ten:<28} SAI - neo harness khong khop DUNG MOT cho")
                hong += 1
                continue
            moi_phan_ma = phan_ma_test
            for c, m in cap:
                moi_phan_ma = moi_phan_ma.replace(c, m, 1)
            if dau_bang and dau_ham_runner:
                moi_truoc, moc_ham, moi_sau = moi_phan_ma.partition(
                    "\n\n\ndef chay_dot_bien()")
                moi_test = (moi_truoc + dau_bang + than_bang + "\n]"
                            + moc_ham + moi_sau)
            else:
                moi_test = moi_phan_ma
            thu_muc = _dung_cay_harness(tam / f"harness_db_{i:02d}", moi_test, goc)
            for ten_ca in phai_chet:   # #1079 F01: neutral trên bản sao NGUYÊN của tệp test
                if ten_ca not in neutral_h:
                    goc_h = tam / "harness_goc" / ".claude" / "dev"
                    if not goc_h.is_dir():
                        _dung_cay_harness(tam / "harness_goc", goc_test, goc)
                    neutral_h[ten_ca] = cham_lap_ca(goc_h, ten_ca)
            tt, so_chet, can_do, mo_ta = ket_luan_mutant(
                list(phai_chet), neutral_h, {t: cham_lap_ca(thu_muc, t) for t in phai_chet})
            if tt == "KHONG_DO":
                khong_do += 1
                print(f"  {ten:<28} KHONG DO DUOC tren nen nay (ca dich bo qua: {mo_ta})")
                continue
            if tt == "KHONG_DO_NEUTRAL":
                hong += 1
                print(f"  {ten:<28} SAI - KHONG DO DUOC (neutral do: {mo_ta})")
                continue
            hong += 0 if tt == "OK" else 1
            print(f"  {ten:<28} {tt}  giet {so_chet}/{can_do}: {mo_ta}")
    finally:
        LAUNCHER_DANG_DUNG = LAUNCHER
        shutil.rmtree(tam, ignore_errors=True)
        # Chốt cuối: tệp thật PHẢI y nguyên. Không tin `finally` - lượt trước
        # chết vì tin nó.
        if LAUNCHER.read_text(encoding="utf-8") != goc:
            print("  !! launcher.py DA BI DOI - dot bien ro ri ra tep that")
            hong += 1
    return hong, khong_do


# ---------------------------------------------------------------------- main

class NhatKyCa:
    """Nhật ký TỪNG CA, `flush` + `fsync` TRƯỚC khi ca kế chạy.

    VÌ SAO CẦN — bài học lượt 6/7, và cả hai bên đều đọc sai một lần:

    Bộ test này KHÔNG in gì trong lúc chạy; nó chỉ in dòng BỎ QUA và dòng tổng kết.
    Nên khi tiến trình bị giết giữa chừng, thứ duy nhất còn lại trên màn hình là
    `BO QUA t62...`. Reviewer đọc thành "chết ngay sau t62", tôi cũng đọc y như thế
    và đi truy `t63` — trong khi dòng đó chỉ là dòng CUỐI CÙNG ĐƯỢC IN, không phải
    ca cuối cùng ĐƯỢC CHẠY. Cộng thêm stdout nối vào ống là bộ đệm KHỐI, nên mọi
    thứ chưa xả cũng mất sạch cùng cú giết. Ba lượt review đi tìm ở sai chỗ vì
    một tạo tác của bộ đệm.

    `flush()` chưa đủ: nó mới đẩy khỏi bộ đệm Python. `fsync()` mới qua bộ đệm HĐH.
    Cú giết không chờ ta. Ca nào có `>>> vao` mà KHÔNG có `<<< ra` chính là ca giết
    tiến trình — đây là kỹ thuật duy nhất sống sót qua một cú giết KHÔNG BẮT ĐƯỢC.

    Nhật ký ghi RA NGOÀI cây kho, đường dẫn do phía gọi đưa (`--nhat-ky`).
    """

    def __init__(self, duong):
        self.tep = open(duong, "w", encoding="utf-8")
        self.ghi(f"# pid={os.getpid()} tong so ca={len(CA)}")

    def ghi(self, s: str) -> None:
        self.tep.write(s + "\n")
        self.tep.flush()
        os.fsync(self.tep.fileno())      # qua ca bo dem HDH

    def vao(self, i: int, ten: str) -> None:
        self.ghi(f">>> vao {i:3d} {ten}")

    def ra(self, i: int, ten: str, kq: str) -> None:
        self.ghi(f"<<< ra  {i:3d} {ten} -> {kq}")

    def dong(self) -> None:
        self.ghi("# XONG TRON VEN")
        self.tep.close()


def _dung_cay_harness(goc_cay, ma_test, ma_launcher):
    """#1079: bản sao harness giữ ĐÚNG bố cục kho (`.claude/dev`, `.claude/hooks`, `ops/bash_nen.py`)
    vì ca đọc `LAUNCHER.parents[1|2]`. Bố cục phẳng làm ca chết FileNotFoundError — trước #1079 lỗi
    ấy được đếm là giết (đo: `g8_fixture_chep_nguyen_moi_truong`, neutral đỏ). Trả thư mục `dev`."""
    dev = goc_cay / ".claude" / "dev"
    dev.mkdir(parents=True)
    (dev / "launcher_test.py").write_text(ma_test, encoding="utf-8")
    (dev / "launcher.py").write_text(ma_launcher, encoding="utf-8")
    for ten in ("codex_cred.py", "codex_cred_test.py"):   # ca r1079 nạp codex_cred_test qua CC_TEST_DANG_DUNG
        if LAUNCHER.with_name(ten).is_file():
            shutil.copy2(LAUNCHER.with_name(ten), dev)
    shutil.copytree(LAUNCHER.parents[1] / "hooks", goc_cay / ".claude" / "hooks")
    (goc_cay / "ops").mkdir()
    shutil.copy2(LAUNCHER.parents[2] / "ops" / "bash_nen.py", goc_cay / "ops")
    return dev


def cham_lap_ca(thu_muc, ten_ca):
    """#1079 F01: chạy `--lap-ca` trên bản `launcher_test.py` trong `thu_muc`, trả `(loai, chi_tiet)`
    như `cham_mot_ca`. Chứng cứ là KÊNH KẾT QUẢ riêng (tệp + nonce, biến bị gỡ khỏi `os.environ` trước
    khi CA chạy), KHÔNG phải stdout của ca: in đuôi giả rồi thoát thì không có kết quả ⇒ `loi`.
    GIỚI HẠN (nợ #1117, Codex lượt 2 F04): mã CẤP MODULE của bản đột biến chạy TRƯỚC `main` nên vẫn
    thấy nonce — kênh này chặn ca giả, KHÔNG chặn được đột biến chủ ý giả kênh lúc nạp module."""
    import secrets
    kenh = Path(tempfile.mkdtemp(prefix="lt_kenh_")) / "ket_qua.json"
    nonce = secrets.token_hex(16)
    try:
        p = subprocess.run(
            [PY, str(thu_muc / "launcher_test.py"), "--lap-ca", ten_ca, "--lan", "1"],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180, cwd=thu_muc,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", LT_KENH_KET_QUA=str(kenh), LT_KENH_NONCE=nonce))
        kq = json.loads(kenh.read_text(encoding="utf-8")) if kenh.is_file() else {}
    except (OSError, subprocess.SubprocessError, ValueError) as e:
        return "loi", f"{ten_ca}({type(e).__name__})"
    finally:
        shutil.rmtree(kenh.parent, ignore_errors=True)
    if kq.get("nonce") != nonce or kq.get("ten") != ten_ca:
        return "loi", f"{ten_ca}(khong co ket qua kenh, rc={p.returncode})"
    if kq.get("hong"):
        return ("giet" if kq.get("loai") == "TinHieuChotCa" else "loi"), (
            ten_ca if kq.get("loai") == "TinHieuChotCa" else
            f"{ten_ca}({kq.get('loai')}" + (f": {kq['thong_diep']}" if kq.get("thong_diep") else "") + ")")
    # wp484 g7 (launcher-windows 39057167905): ca POSIX tự bỏ qua là KHÔNG ĐO ĐƯỢC.
    return ("bo_qua" if kq.get("bo_qua") else "qua"), ten_ca


LOAI_HONG: dict = {}


def chay_bo_ca(ds_ca, nk=None, bat_dau=0):
    """Chạy một danh sách ca, trả `(qua, bo_qua, hong_ds)`.

    Tách khỏi `main` để `t99` gọi được với danh sách ca giả — nếu không thì chốt
    nhật ký chỉ kiểm được bằng cách chạy lại toàn bộ suite trong suite.
    """
    kiem_registry(CA)   # #1079 F08 (Codex lượt 6): TRƯỚC khi ca đầu tiên chạy
    qua = bo_qua = 0
    hong_ds = []
    for i, fn in enumerate(ds_ca, start=bat_dau):
        if nk:
            nk.vao(i, fn.__name__)
        try:
            with _co_lap_toan_cuc():
                kq = fn()
            if isinstance(kq, str):
                bo_qua += 1
                print(f"  BO QUA {fn.__name__}: {kq}", flush=True)
                ket = f"BO QUA: {kq[:60]}"
            else:
                qua += 1
                ket = "qua"
        except AssertionError as e:
            hong_ds.append((fn.__name__, str(e)))
            # #1079 F01: danh tính lớp THẬT; lớp khác (kể cả cùng `__qualname__`) mang tiền tố `khac:`.
            LOAI_HONG[fn.__name__] = ("TinHieuChotCa" if isinstance(e, TinHieuChotCa) and not chot_tu_ca_khac(e, fn)
                                      else f"khac:{type(e).__qualname__}")
            ket = f"HONG: {str(e)[:60]}"
        except Exception as e:  # noqa: BLE001
            hong_ds.append((fn.__name__, f"{type(e).__name__}: {e}"))
            LOAI_HONG[fn.__name__] = f"khac:{type(e).__qualname__}"
            ket = f"LOI {type(e).__name__}"
        if nk:
            nk.ra(i, fn.__name__, ket)
    return qua, bo_qua, hong_ds


def dong_ket_qua(tong: int, qua: int, bo_qua: int, so_hong: int) -> str:
    """Dòng kết luận của một lượt chạy. TÁCH khỏi `main` để đo được TRỰC TIẾP.

    ĐÃ TRẢ GIÁ: tử số cũ là `qua + bo_qua`, nên một lượt Windows bỏ qua 13 ca vẫn
    in `118/118 ca` (số ĐO tại `99ba7857`: `qua=105, bo_qua=13, tong=118` — máy
    dev cp1258, CI windows-latest và PR #153 cùng ra một bộ; bản đầu ghi
    `117/117`/`bỏ qua 14`, không khớp phép đo nào tại head ấy — review W0-M1
    bắt, P3) — ĐÚNG hình dạng "N/N với hai số BẰNG NHAU" mà CLAUDE.md dạy
    là bằng chứng dương đáng tin. Người đọc nhận một câu khẳng định mọi ca đã qua,
    trong khi có ca chưa hề chạy. Cùng họ với `t24` của kho ("ca CÓ MẶT khác ca có
    ĐO") và với `t116` ("suite vẫn in 114/114 mà tổng đã tụt một"): chỗ VẮNG MẶT
    bị chính dòng headline che đi, và "vắng mặt vì sạch" với "vắng mặt vì chưa
    chạy" trông giống hệt nhau.

    Nay cặp đầu là `qua/đã_chạy`: N/N chỉ khẳng định mọi ca ĐÃ CHẠY đều qua. Tổng
    khai riêng ngay cạnh (`tong`, `bo qua`, `hong`), nên không thể đọc N/N thành
    "mọi ca trong suite đã chạy". Mã thoát KHÔNG đổi: bỏ qua vẫn không làm đỏ.

    Chuỗi trả về là ASCII: console máy Việt là cp1258 và một câu `print` có dấu
    ném `UnicodeEncodeError`, giết cả lượt chạy trước khi logic kịp sai. Câu cảnh
    báo cũng phải giữ đủ `tong/bo qua`, không được chỉ in cặp N/N rồi giấu mẫu số
    toàn suite.
    """
    da_chay = tong - bo_qua
    dong = (f"{qua}/{da_chay} ca DA CHAY QUA "
            f"(tong {tong}, bo qua {bo_qua}, hong {so_hong})")
    if bo_qua:
        dong += f" - KHONG DU: {bo_qua} ca BO QUA, chua do gi"
    return dong


def phan_tich_doi_so(argv):
    """Phân tích đối số TRƯỚC KHI làm bất cứ việc gì. Trả `argparse.Namespace`.

    Cross-review lượt 8 (LOW) đếm bốn tổ hợp xanh giả của bộ phân tích TAY cũ:
      · `--nhat-ky` thiếu đường dẫn ⇒ chạy HẾT suite rồi mới rc=2 (báo lỗi sau ~30s);
      · `--nhat-ky --dot-bien` ⇒ chạy mutation, rc=0, và KHÔNG hề tạo nhật ký —
        `--dot-bien` bị nuốt làm đường dẫn, còn nhánh mutation thắng trước;
      · `--moi-truong` lờ luôn `--nhat-ky` lẫn đối số rác, rc=0;
      · cờ lặp/cờ lạ không bị từ chối.
    (Vế "cờ lặp" tôi khai là đã sửa từ lượt trước trong khi CHƯA sửa — lượt 9 bắt được;
    nay mới thật sự khoá, xem khối `lap` bên dưới.)
    Đây là công cụ CHẨN ĐOÁN. Một công cụ chẩn đoán dễ xanh giả thì tệ hơn không có,
    vì nó biến "chưa đo" thành "đã đo rồi, không sao".

    `argparse` + ba chế độ LOẠI TRỪ NHAU + `--nhat-ky` đòi đường dẫn ngay tại chỗ.
    """
    p = argparse.ArgumentParser(
        prog="launcher_test.py", description="bo test cua launcher.py",
        allow_abbrev=False)          # `--dot` KHONG duoc tu nở thành `--dot-bien`
    che_do = p.add_mutually_exclusive_group()
    che_do.add_argument("--dot-bien", action="store_true",
                        help="chay bang tu dot bien thay vi bo ca")
    che_do.add_argument("--moi-truong", action="store_true",
                        help="chi in ban khai moi truong roi thoat")
    che_do.add_argument("--lap-ca", metavar="TEN", default=None,
                        help="chay LAP MOT ca N lan (do loi chap chon)")
    p.add_argument("--lan", type=int, default=20, metavar="N",
                   help="so lan lap cho --lap-ca (mac dinh 20)")
    p.add_argument("--nhat-ky", metavar="TEP", default=None,
                   help="ghi >>> vao / <<< ra tung ca, flush+fsync "
                        "(che do mac dinh hoac --lap-ca)")
    # CỜ LẶP: `argparse` mặc định NHẬN và lặng lẽ lấy giá trị cuối —
    # `--nhat-ky /tmp/a --nhat-ky /tmp/b` ghi vào `/tmp/b`, người gõ tưởng là `/tmp/a`.
    # Cross-review lượt 9 (LOW) bắt đúng chỗ tôi KHAI QUÁ: chú thích của tôi ghi "cờ
    # lặp/cờ lạ không bị từ chối" là lỗi đã sửa, trong khi mới sửa được vế "cờ lạ".
    # Lần thứ ba trong ba lượt tôi mô tả rộng hơn thứ test khoá được.
    lap = [c for c in ("--dot-bien", "--moi-truong", "--nhat-ky", "--lap-ca", "--lan")
           if argv.count(c) > 1]
    if lap:
        p.error(f"co lap: {', '.join(lap)} — go hai lan thi y dinh khong ro, KHONG doan")
    a = p.parse_args(argv)
    if a.nhat_ky and (a.dot_bien or a.moi_truong):
        # argparse khong dien ta duoc rang buoc nay, nen noi THANG thay vi lo di.
        p.error("--nhat-ky chi dung o che do mac dinh hoac --lap-ca")
    if "--lan" in argv and not a.lap_ca:
        p.error("--lan chi co nghia kem --lap-ca")
    if a.lap_ca and a.lan < 1:
        p.error("--lan phai >= 1")
    return a


def main() -> int:
    # PHÂN TÍCH ĐỐI SỐ TRƯỚC MỌI VIỆC — kể cả trước khi tự khai/tách nhóm. Sai đối số
    # phải đỏ NGAY, đừng để người ta chờ hết suite mới biết mình gõ nhầm.
    a = phan_tich_doi_so(sys.argv[1:])
    # Kế đó: nếu đang chung nhóm với vỏ shell thì tách ra, kẻo một cú `killpg` của ca
    # test cuốn theo cả người gọi (xem `_tu_tach_nhom_neu_can`).
    # TỰ KHAI TRƯỚC, tách nhóm SAU — thứ tự này cố ý: bản khai phải mô tả môi trường
    # NHƯ NÓ ĐẾN, không phải như sau khi ta đã sửa nó. Khai sau khi tách thì mọi lượt
    # chạy đều trông giống nhau và khối này thành vô dụng.
    mt = khai_moi_truong()
    if a.moi_truong:
        print(json.dumps(mt, ensure_ascii=False, indent=2, default=str))
        return 0
    print(_mot_dong_moi_truong(mt))
    print(f"nhom tien trinh: {_tu_tach_nhom_neu_can()}")
    if a.dot_bien:
        print("TU DOT BIEN - moi dot bien PHAI giet dung cac ca da chi dinh:")
        hong, khong_do = chay_dot_bien()
        tong_dot_bien = len(DOT_BIEN) + len(DOT_BIEN_HOOK) + len(DOT_BIEN_HARNESS)
        do_duoc = tong_dot_bien - khong_do
        print(f"\nDOT BIEN: {do_duoc - hong}/{do_duoc} dat"
              + (f"  ({khong_do} khong do duoc tren nen nay)" if khong_do else ""))
        if not _dot_bien_du_san(tong_dot_bien, khong_do):
            # SÀN. Bảng mà MỌI đột biến đều không đo được sẽ in "0/0 dat" rồi
            # thoát 0 — thoả đúng hình thức "hai số BẰNG NHAU" mà chứng minh CON
            # SỐ KHÔNG. Đây là cổng xanh nhờ rc=0, thứ CLAUDE.md dặn đừng tin.
            print("!! DUOI SAN: phai do duoc it nhat 70% dot bien tren moi nen")
            return 1
        return 1 if hong else 0

    if not shutil.which("git"):
        print("khong co git - khong chay duoc"), sys.exit(2)

    if a.lap_ca:
        # ĐO LẶP MỘT CA (cross-review lượt 9). Lượt 8 nhật ký chạy trọn `100/100` rồi
        # vỏ shell mới chết; lượt 9 chết ngay trong `t72`. HAI CHỖ KHÁC NHAU ⇒ chập
        # chờn hoặc phụ thuộc thứ tự. Chạy MỘT ca N lần là cách rẻ nhất phân biệt
        # "ca này tự nó chập chờn" với "chỉ chết khi đứng sau 73 ca khác".
        #
        # KHÔNG kết luận nguyên nhân ở đây — chỉ đếm. Nhật ký (nếu bật) mới là thứ
        # sống sót qua một cú giết: lần lặp nào có `vao` mà không có `ra` là lần chết.
        chon = [f for f in CA if f.__name__.startswith(a.lap_ca)]
        if len(chon) != 1:
            print(f"--lap-ca {a.lap_ca!r} khop {len(chon)} ca "
                  f"({', '.join(f.__name__ for f in chon[:5]) or 'khong ca nao'})"), sys.exit(2)
        nk = NhatKyCa(a.nhat_ky) if a.nhat_ky else None
        kenh, nonce = os.environ.pop("LT_KENH_KET_QUA", None), os.environ.pop("LT_KENH_NONCE", None)
        qua = bo_qua = 0
        hong_ds = []
        try:
            for i in range(a.lan):
                q, b, h = chay_bo_ca(chon, nk, bat_dau=i)
                qua += q
                bo_qua += b
                hong_ds += h
                print(f"  lan {i + 1}/{a.lan}: {'qua' if q else ('BO QUA' if b else 'HONG')}",
                      flush=True)
        finally:
            if nk:
                nk.dong()
        for ten, ly_do in hong_ds:
            print(f"  HONG {ten}: {ly_do}", flush=True)
        if kenh:   # #1079 F01: kênh kết quả cho runner harness (cham_lap_ca)
            Path(kenh).write_text(json.dumps({"nonce": nonce, "ten": chon[0].__name__, "qua": qua,
                                              "bo_qua": bo_qua, "hong": len(hong_ds),
                                              "loai": LOAI_HONG.get(chon[0].__name__),
                                              # #1122: thông điệp (cắt) cho chi tiết `loi` của `cham_lap_ca`
                                              "thong_diep": (hong_ds[-1][1][:TRAN_THONG_DIEP_LOI]
                                                             if hong_ds else None)}), encoding="utf-8")
        print(f"\nLAP {chon[0].__name__}: {qua}/{a.lan} qua, {bo_qua} bo qua, "
              f"{len(hong_ds)} hong", flush=True)
        return 1 if hong_ds else 0

    nk = NhatKyCa(a.nhat_ky) if a.nhat_ky else None
    try:
        qua, bo_qua, hong_ds = chay_bo_ca(CA, nk)
    finally:
        if nk:
            nk.dong()
    tong = len(CA)
    for ten, ly_do in hong_ds:
        print(f"  HONG {ten}: {ly_do}", flush=True)
    print("\n" + dong_ket_qua(tong, qua, bo_qua, len(hong_ds)), flush=True)
    return 1 if hong_ds else 0


if __name__ == "__main__":
    sys.exit(main())
