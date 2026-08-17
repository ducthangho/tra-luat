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
import hashlib
import importlib.util
import io
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

LAUNCHER = Path(__file__).resolve().parent / "launcher.py"
CODEX_ENV_POLICY = Path(__file__).resolve().parent / "codex_env_policy.py"
PY = sys.executable or "python3"
LA_WINDOWS = platform.system() == "Windows"

MA_OK, MA_THAM_SO, MA_GIT, MA_HEAD, MA_REF = 0, 2, 3, 4, 5
MA_BAN, MA_PROMPT, MA_HAN, MA_VA_CHAM, MA_DANH_TINH, MA_QUA_HAN = 6, 7, 8, 9, 10, 124

CA: list = []


def ca(fn):
    CA.append(fn)
    return fn


# ------------------------------------------------------------------ khung chạy

# Đường dẫn launcher THỰC SỰ được gọi. Chế độ đột biến trỏ biến này sang một bản
# sao tạm; tệp trong kho không bao giờ bị ghi (xem chay_dot_bien).
LAUNCHER_DANG_DUNG = LAUNCHER


def chay(*doi_so, cwd=None, env=None) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(LAUNCHER_DANG_DUNG), *doi_so], capture_output=True,
                          text=True, cwd=cwd, env=env)


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


def bang(dieu_kien, thong_diep):
    if not dieu_kien:
        raise AssertionError(thong_diep)


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
            nd = st.read_text()
            return nd[nd.rindex(")") + 2:].split()[0] != "Z"
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
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for _ in range(100):
            time.sleep(0.1)
            ds = list(rr.iterdir()) if rr.is_dir() else []
            if ds and (ds[0] / "run.json").is_file():
                d = json.loads((ds[0] / "run.json").read_text(encoding="utf-8"))
                if d.get("pid"):
                    break
        else:
            raise AssertionError("khong thay pid trong so")
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
    r = chay("doctor", "--json")
    bang(r.returncode == MA_OK, f"{r.returncode}: {r.stderr}")
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
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
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
        def OpenProcess(self, *_a): raise AssertionError("khong duoc di tiep sau SetInformation hong")

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
    """
    m = _tai_launcher_thu()
    m.platform.system = lambda: "Windows"
    da_hoi = []
    khoa = {10: "win:123", 11: None, 12: "win:456"}

    def _khoa(pid):
        da_hoi.append(pid)
        return khoa.get(pid)

    m._khoa_danh_tinh = _khoa

    # (a) tien trinh mu la CON cua 10 => khong do duoc
    m._cac_pid_cha_windows = lambda: {10: 1, 11: 10}
    bang(m._chup_cay(10) is None, "hau due khong lay duoc khoa bi bo qua im lang")
    # (b) tien trinh mu thuoc nhanh KHAC (cha = 1) => anh van dung duoc
    da_hoi.clear()
    m._cac_pid_cha_windows = lambda: {10: 1, 12: 10, 11: 1}
    bang(m._chup_cay(10) == {10: "win:123", 12: "win:456"},
         "tien trinh mu NGOAI cay khong duoc lam hong ca anh")
    bang(11 not in da_hoi, f"da hoi khoa cua PID ngoai cay: {da_hoi}")


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
    for ten, gia_tri in (("base64", _b64.b64encode(that.encode()).decode()),
                         ("json tho", that)):
        nha = tempfile.mkdtemp()
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
    nha = tempfile.mkdtemp()
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
    m._do_codex_song = lambda *_a: (True, "rc=0")
    tt, _ = m._do_codex(kiem_song=True)
    bang(tt == "DUNG_DUOC", f"kiem song dat ma khong cho DUNG_DUOC: {tt}")

    # (d) kiem song BI TU CHOI => CHUA_XAC_THUC, du login status van rc=0
    m._do_codex_song = lambda *_a: (False, "credential BI TU CHOI (token_revoked)")
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
    m._do_codex_song = lambda *_a: (goi.append(1), (True, "rc=0"))[1]
    tt, mo_ta = m._do_codex(kiem_song=True)
    bang(len(goi) == 1, "doi kiem song ma KHONG he goi — canh bao da nuot phep do")
    bang(tt == "SAP_HET_HAN", f"kiem song dat thi van phai canh bao, duoc {tt}")
    bang("VAN dung duoc" in mo_ta, f"phai ghi ro van dung duoc: {mo_ta!r}")

    # (b) sap het han VA kiem song HONG => CHUA_XAC_THUC, canh bao khong duoc che lap
    m._do_codex_song = lambda *_a: (False, "credential BI TU CHOI (token_revoked)")
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
    m._phien_ban = lambda *_a, **_k: (su_kien.append("version") or (True, "gia 1"))
    m._xac_thuc = lambda *_a, **_k: (su_kien.append("auth") or (False, "rc=1"))
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

    def pb(duong, **_kwargs):
        da_thu.append(duong)
        return (duong == "/tot/rg", "rg 99" if duong == "/tot/rg" else "Access denied")

    m._phien_ban = pb
    a = type("A", (), {"json": True, "workspace": None, "doi_kha_dung": False})()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = m.lenh_doctor(a)
    d = json.loads(out.getvalue())
    muc = [x for x in d["cong_cu"] if x["ten"] == "rg"][0]
    bang(rc == MA_OK and muc["duong_dan"] == "/tot/rg",
         f"khong lui sang binary tot: {muc}")
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
    hook = (LAUNCHER.parent.parent / "hooks" / "session-start.sh").read_text(encoding="utf-8")
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
    hook = (LAUNCHER.parent.parent / "hooks" / "session-start.sh").read_text(encoding="utf-8")
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
    bang('"mcp"' not in khoi and "'mcp'" not in khoi,
         f"`mcp` bi tinh vao LAM_DUOC_VIEC — CLI duyet server KHONG chung minh PHIEN "
         f"goi duoc cong cu: {khoi!r}")
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

    def git_gia(ws, *a, **k):
        if a[:2] == ("remote", "get-url"):
            return (0, "https://gitlab.example/khong-phai-github/x.git", "")
        return (1, "", "")

    m._do_rest_github = lambda *a, **k: ("mo", "gia", True)
    m._git = git_gia
    try:
        with tempfile.TemporaryDirectory() as td_g:
            _tt, mo_ta_g = m._do_github(td_g, {})
    finally:
        m._do_rest_github, m._git = goc_rest, goc_git
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
                {"capture_output": True, "text": True, "timeout": m.PROBE_TIMEOUT_GIAY})

    def gia_run(cmd, *_a, **_k):
        if list(cmd)[:2] != ["claude", "mcp"]:
            return Rc(1)                       # gh/git: ngoai pham vi ca nay
        # DO GIA TU TU CHOI loi goi lech dac ta — chot TOAN PHAN, khong opt-in. Bon
        # luot cross-review lien tiep tim duoc dot bien song sot o dung lop nay, va
        # ca bon lan vi ca test cham diem le te nhung gi nguoi va NGHI RA phai dung,
        # tuc mot danh sach CAM. Nay dao thanh danh sach CHO PHEP.
        thay = (tuple(cmd), {k: v for k, v in _k.items() if k != "env" and k != "stdin"})
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
                kq = m._doc_mcp_json(td)
                if kq[0]:
                    ENV_SENTINEL[0] = {"TL_ENV_DA_CHUAN": "1"}
                    kq = (kq[0], kq[1], kq[2],
                          m._suc_khoe_mcp_github(kq[2], ENV_SENTINEL[0]))
                bang(len(nhat_ky) == mong_goi,
                     f"[{vi_tri}] mong {mong_goi} loi goi `claude`, do {len(nhat_ky)}")
                return kq

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
    nguon = _P(LAUNCHER).read_text(encoding="utf-8")
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
    """Mọi `def tNN_...` phải có `@ca` ngay trên nó — nếu không, ca ấy KHÔNG CHẠY.

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
    ham = [(i, l) for i, l in enumerate(dong) if _re.match(r"^def t\d+_", l)]
    thieu = [l.split("(")[0][4:] for i, l in ham if i == 0 or dong[i - 1].strip() != "@ca"]
    bang(not thieu, f"ca co mat trong TEP ma KHONG duoc dang ky (thieu `@ca`): {thieu}")
    # ...va so ca DA DANG KY phai khop so ham. Hai phep dem doc lap: mot doc TEP, mot
    # doc bang `CA` da nap. Lech nhau nghia la co ca bi trang tri hai lan, hoac co
    # `@ca` gan cho thu khong phai ca.
    bang(len(ham) == len(CA),
         f"{len(ham)} ham `tNN_` nhung `CA` co {len(CA)} muc — co cho dang ky lech")


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
        m.os.path.expanduser = lambda d: str(s.parent) if d == "~/.codex" else d
        (s.parent / cs.TEN_CO_CHAN).write_text("x", encoding="utf-8")
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
            (s.parent / cs.TEN_CO_CHAN).unlink()

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


# ------------------------------------------------------ tự đột biến: có răng không

DOT_BIEN = [
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
     ('    for ten_cach, thu in (("base64 → JSON", None), ("JSON thô", thoc)):',
      '    for ten_cach, thu in (("base64 → JSON", None),):'),
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
     ('            if kiem_song:\n                song, ly_do = _do_codex_song()',
      '            if False:\n                song, ly_do = _do_codex_song()'),
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
     ('        elif bb and (thay is None or xac_thuc_ok is False):',
      '        elif False:'),
     ["t54_doctor_thieu_cong_cu_bat_buoc_thi_DO"]),
    # Chiều hẹp hơn: giữ phép kiểm CÓ MẶT, bỏ riêng phép kiểm XÁC THỰC. Bản cũ chỉ
    # có một đột biến "luôn xanh", nên nếu ai lỡ tay bỏ vế `xac_thuc_ok` thì không
    # mutant nào đỏ — cửa mới mà không có mutant riêng là cửa sẽ âm thầm hở lại.
    ("doctor_bo_qua_auth_hong",
     ('        elif bb and (thay is None or xac_thuc_ok is False):',
      '        elif bb and thay is None:'),
     ["t105_doctor_auth_hong_thi_DO_du_binary_chay_duoc"]),
    ("khong_chup_prompt",
     ('        if any("{PROMPT_FILE}" in x for x in lenh_con):',
      '        if False:'),
     ["t56_prompt_doi_sau_khi_kiem_KHONG_toi_duoc_con"]),
    ("luu_argv_nguyen_van",
     ('"ten": a.name, "lenh": _tom_tat_lenh(a.lenh), "trang_thai": "dang_chay",',
      '"ten": a.name, "lenh": [str(x) for x in a.lenh], "trang_thai": "dang_chay",'),
     ["t59_so_KHONG_luu_doi_so_nguyen_van"]),
    ("doctor_tin_which",
     ('            chay_duoc, pb = _phien_ban(d, env=moi_truong,\n'
      '                                       timeout=min(PROBE_TIMEOUT_GIAY, con_lai))',
      '            chay_duoc, pb = True, ""'),
     ["t60_doctor_KHONG_tin_which_khi_cong_cu_khong_chay_duoc"]),
    # Dừng ở binary ĐẦU TIÊN trong PATH = đúng hành vi `shutil.which` cũ, tức dựng
    # lại lỗi đã đo trên Windows (rg của WindowsApps che mất bản chạy được).
    ("doctor_chi_thu_binary_dau",
     ('        for ten_uv, d in _cac_duong_dan(c, moi_truong):',
      '        for ten_uv, d in _cac_duong_dan(c, moi_truong)[:1]:'),
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
     ('        if bb and het_ngan_sach is not None and thay is None:',
      '        if False:'),
     ["t114_ngan_sach_phu_CA_khoi_kha_dung_va_khong_thanh_THIEU"]),
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
     ["t70_PROMPT_FILE_ma_khong_co_prompt_file_phai_bi_CHAN"]),
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
    ("mcp_tinh_vao_LAM_DUOC_VIEC",
     ('    LAM_DUOC_VIEC = {"git", "gh-kho", "rest-kho"}',
      '    LAM_DUOC_VIEC = {"git", "gh-kho", "rest-kho", "mcp"}'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_ket_xuat_gop_chua_do_duoc_thanh_hong",
     ('    return "chua-do-duoc" if ok is None else ("OK" if ok else "khong")',
      '    return "OK" if ok else "khong"'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_ten_server_khop_chuoi_con",
     ('k.casefold() == "github"', '"github" in k.casefold()'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_ten_server_phan_biet_hoa_thuong",
     ('k.casefold() == "github"', 'k == "github"'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_bo_bat_loi_json_hong",
     ('    except (OSError, ValueError) as e:\n        return False, f".mcp.json',
      '    except OSError as e:\n        return False, f".mcp.json'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_bo_kiem_kieu_goc",
     ('    if not isinstance(d, dict):', '    if False:'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_bo_kiem_kieu_bang_server",
     ('    if not isinstance(srv, dict):', '    if False:'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
    ("mcp_bo_kiem_kieu_gia_tri_server",
     ('    xau = [k for k in ten if not isinstance(srv[k], dict)]', '    xau = []'), ["t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec"]),
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
     ('        r = subprocess.run(["claude", "mcp", "get", ten], capture_output=True, text=True,',
      '        r = subprocess.run(["claude", "mcp", "get", "github"], capture_output=True, text=True,'),
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
    global LAUNCHER_DANG_DUNG
    goc = LAUNCHER.read_text(encoding="utf-8")
    hong = 0
    khong_do = 0
    tam = Path(tempfile.mkdtemp(prefix="lt_db_"))
    try:
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
            LAUNCHER_DANG_DUNG = ban_sao
            chet, bo_qua = [], []
            for fn in CA:
                if fn.__name__ not in phai_chet:
                    continue
                try:
                    with _co_lap_toan_cuc():
                        kq = fn()
                    # Ca TỰ BỎ QUA trên nền này thì đột biến KHÔNG ĐO ĐƯỢC, chứ
                    # không phải "test yếu". Audit codex: trên Windows t03 và t50
                    # bỏ qua nên gate 14/14 thành BẤT KHẢ THI ở đúng nền cần nghiệm
                    # thu — một cổng không bao giờ xanh được thì người ta sẽ bỏ qua nó.
                    if isinstance(kq, str):
                        bo_qua.append(fn.__name__)
                except AssertionError:
                    chet.append(fn.__name__)
                except Exception as e:  # noqa: BLE001
                    chet.append(f"{fn.__name__}({type(e).__name__})")
            can_do = len(phai_chet) - len(bo_qua)
            if can_do == 0:
                khong_do += 1
                print(f"  {ten:<28} KHONG DO DUOC tren nen nay (ca dich bo qua: "
                      f"{', '.join(bo_qua)})")
                continue
            ok = len(chet) == can_do
            if not ok:
                hong += 1
            ghi_chu = f" [bo qua: {', '.join(bo_qua)}]" if bo_qua else ""
            print(f"  {ten:<28} {'OK' if ok else 'SAI'}  giet {len(chet)}/{can_do}: "
                  f"{', '.join(chet) or '(khong ca nao chet)'}{ghi_chu}")
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


def chay_bo_ca(ds_ca, nk=None, bat_dau=0):
    """Chạy một danh sách ca, trả `(qua, bo_qua, hong_ds)`.

    Tách khỏi `main` để `t99` gọi được với danh sách ca giả — nếu không thì chốt
    nhật ký chỉ kiểm được bằng cách chạy lại toàn bộ suite trong suite.
    """
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
            ket = f"HONG: {str(e)[:60]}"
        except Exception as e:  # noqa: BLE001
            hong_ds.append((fn.__name__, f"{type(e).__name__}: {e}"))
            ket = f"LOI {type(e).__name__}"
        if nk:
            nk.ra(i, fn.__name__, ket)
    return qua, bo_qua, hong_ds


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
        do_duoc = len(DOT_BIEN) - khong_do
        print(f"\nDOT BIEN: {do_duoc - hong}/{do_duoc} dat"
              + (f"  ({khong_do} khong do duoc tren nen nay)" if khong_do else ""))
        if not _dot_bien_du_san(len(DOT_BIEN), khong_do):
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
    print(f"\n{qua + bo_qua}/{tong} ca (qua {qua}, bo qua {bo_qua}, hong {len(hong_ds)})",
          flush=True)
    return 1 if hong_ds else 0


if __name__ == "__main__":
    sys.exit(main())
