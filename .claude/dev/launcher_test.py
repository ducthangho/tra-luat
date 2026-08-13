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

import hashlib
import importlib.util
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


def _tai_launcher_thu():
    """Nạp đúng bản launcher đang thử (kể cả bản sao đột biến)."""
    ten = f"launcher_thu_{time.time_ns()}"
    sp = importlib.util.spec_from_file_location(ten, LAUNCHER_DANG_DUNG)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


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
    """None từ phép quét không được biến thành bằng chứng cả cây đã chết."""
    m = _tai_launcher_thu()
    m._khoa_danh_tinh = lambda _pid: None
    m._thanh_vien_nhom = lambda _pid: None
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
    """CIM thiếu CreationDate: fail-closed, nhưng CHỈ khi nó ở TRONG cây.

    Hai vế cố ý ngược nhau. Vế (a) là bảo đảm gốc: một hậu duệ mà ta không lấy
    được khoá danh tính thì cả ảnh không đủ bằng chứng — bỏ qua im lặng sẽ làm
    ảnh rỗng thành "cả cây đã chết". Vế (b) là PHẠM VI: tiến trình mù NGOÀI cây
    không liên quan gì tới thứ ta sắp giết; để nó phá ảnh thì ảnh có dùng được
    hay không lại tuỳ trạng thái máy ở chỗ khác — mà từ khi ảnh rỗng là bằng
    chứng "đã tắt" trên Windows, đó chính là đường quyết định 0-hay-125.
    """
    m = _tai_launcher_thu()
    m.platform.system = lambda: "Windows"

    def _ra(dong):
        class P:
            returncode = 0
            stdout = dong
        m.subprocess.run = lambda *_a, **_k: P()

    # (a) tien trinh mu la CON cua 10 => khong do duoc
    _ra("OK|10|1|123\nERR|11|10|NO_CREATION_DATE\n")
    bang(m._chup_cay(10) is None, "hau due thieu CreationDate bi bo qua im lang")
    # (b) tien trinh mu thuoc nhanh KHAC (cha = 1) => anh van dung duoc
    _ra("OK|10|1|123\nOK|12|10|456\nERR|11|1|NO_CREATION_DATE\n")
    bang(m._chup_cay(10) == {10: "win:123", 12: "win:456"},
         "tien trinh mu NGOAI cay khong duoc lam hong ca anh")


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
     ('        if thay is None and c["bat_buoc"]:', '        if False:'),
     ["t54_doctor_thieu_cong_cu_bat_buoc_thi_DO"]),
    ("khong_chup_prompt",
     ('        if any("{PROMPT_FILE}" in x for x in lenh_con):',
      '        if False:'),
     ["t56_prompt_doi_sau_khi_kiem_KHONG_toi_duoc_con"]),
    ("luu_argv_nguyen_van",
     ('"ten": a.name, "lenh": _tom_tat_lenh(a.lenh), "trang_thai": "dang_chay",',
      '"ten": a.name, "lenh": [str(x) for x in a.lenh], "trang_thai": "dang_chay",'),
     ["t59_so_KHONG_luu_doi_so_nguyen_van"]),
    ("doctor_tin_which",
     ('            chay_duoc, pb = _phien_ban(d)', '            chay_duoc, pb = True, ""'),
     ["t60_doctor_KHONG_tin_which_khi_cong_cu_khong_chay_duoc"]),
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
     ('    {"ten": "bash", "bat_buoc": False, "ung_vien": ["bash"],',
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
    # CHUYEN NEO (khong noi dieu kien): dong thieu CreationDate khong con bi loai o
    # cho doc nua ma duoc GIU LAI kem dau `KHONG_DOC_DUOC_KHOA`, de fail-closed co
    # PHAM VI (chi do khi no nam trong cay). Y DINH GIU NGUYEN - lam tien trinh mu
    # lan vao anh nhu mot tien trinh binh thuong. Day la LOP KHAC voi
    # `chup_cay_khong_fail_closed_trong_cay`: mot ben bo DAU, ben kia bo phep KIEM.
    ("chup_cay_bo_qua_dong_thieu",
     ('                                    f"win:{phan[3]}" if phan[0] == "OK" else KHONG_DOC_DUOC_KHOA)',
      '                                    f"win:{phan[3]}")'),
     ["t81_chup_cay_windows_thieu_creationdate_phai_fail_closed"]),
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
    # Bo dau "khong doc duoc khoa" => hau due mu lot vao anh voi khoa rong, roi
    # `_con_song_dung_khoa` khong bao gio khop => bao la da chet.
    ("chup_cay_khong_fail_closed_trong_cay",
     ('    if KHONG_DOC_DUOC_KHOA in ra.values():', '    if False:'),
     ["t81_chup_cay_windows_thieu_creationdate_phai_fail_closed"]),
    # Chieu NGUOC LAI: fail-closed mat pham vi, tro lai "bat ky tien trinh nao tren
    # may thieu CreationDate cung lam hong anh". Xanh ma vo dung.
    ("chup_cay_fail_closed_ca_may",
     ('            if len(phan) != 4 or phan[0] not in ("OK", "ERR"):',
      '            if len(phan) != 4 or phan[0] != "OK":'),
     ["t81_chup_cay_windows_thieu_creationdate_phai_fail_closed"]),
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
            ban_sao = tam / "launcher.py"
            ban_sao.write_text(moi_ma, encoding="utf-8")
            LAUNCHER_DANG_DUNG = ban_sao
            chet, bo_qua = [], []
            for fn in CA:
                if fn.__name__ not in phai_chet:
                    continue
                try:
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

def main() -> int:
    if "--dot-bien" in sys.argv:
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
    qua = bo_qua = 0
    hong_ds = []
    for fn in CA:
        try:
            kq = fn()
            if isinstance(kq, str):
                bo_qua += 1
                print(f"  BO QUA {fn.__name__}: {kq}")
            else:
                qua += 1
        except AssertionError as e:
            hong_ds.append((fn.__name__, str(e)))
        except Exception as e:  # noqa: BLE001
            hong_ds.append((fn.__name__, f"{type(e).__name__}: {e}"))
    tong = len(CA)
    for ten, ly_do in hong_ds:
        print(f"  HONG {ten}: {ly_do}")
    print(f"\n{qua + bo_qua}/{tong} ca (qua {qua}, bo qua {bo_qua}, hong {len(hong_ds)})")
    return 1 if hong_ds else 0


if __name__ == "__main__":
    sys.exit(main())
