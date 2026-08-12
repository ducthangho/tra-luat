#!/usr/bin/env python3
"""launcher_test.py — phản chứng cho launcher.py.

Nguyên tắc (cùng doctrine với packet_loop_test.py): một chốt chỉ TỒN TẠI nếu có
trường hợp làm nó ĐỎ. Mỗi ca dưới đây neo đúng một hành vi, gọi qua CLI thật
(subprocess) chứ không import — seam là dòng lệnh, vì đó là thứ phiên khác,
điện thoại và remote thực sự gọi.

Chạy:  python3 .claude/dev/launcher_test.py            (chạy tất cả)
       python3 .claude/dev/launcher_test.py --dot-bien (tự đột biến: chứng minh có răng)
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
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
        d["pid"] = os.getpid()               # PID CÓ THẬT (chính test này)
        d["khoa_danh_tinh"] = "linux:0"      # nhưng khoá KHÔNG khớp
        f.write_text(json.dumps(d), encoding="utf-8")
        r = chay("stop", "--run-root", str(rr), "--id", d["short_id"])
        bang(r.returncode == MA_DANH_TINH, f"mong doi {MA_DANH_TINH}, duoc {r.returncode}")
        bang("tai dung" in r.stdout or "KHAC" in r.stdout, f"khong noi ro ly do: {r.stdout}")


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
        bang(str(repo.resolve()) in r.stdout and str(con) not in r.stdout,
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
    ("giet_lieu_khong_can_khoa",
     ('if _khoa_danh_tinh(pid) != khoa:\n        return "tu choi giet: khoa danh tinh KHAC (PID da bi tai dung)"',
      'if False:\n        return "tu choi giet: khoa danh tinh KHAC (PID da bi tai dung)"'),
     ["t31_stop_tu_choi_khi_khoa_danh_tinh_khac"]),
    # DA DO bang git that: `-uall` so voi mac dinh (`normal`) KHONG doi sach/ban,
    # chi doi do chi tiet liet ke (`?? thumuc/` thay vi tung tep). Chi `-uno` moi
    # lam chot MU. Dot bien dau tien cua toi nham vao `-uall` nen song sot - do la
    # dot bien sai, khong phai ma sai.
    ("khong_cat_thong_tin_dang_nhap",
     ("(?:[^@/]*@)?", "(?:)?"),
     ["t45_token_trong_URL_KHONG_duoc_lo_ra"]),
    ("so_URL_tho_khong_chuan_hoa",
     ('khop = any(r == can or r.endswith("/" + can) for r in remotes)',
      'khop = any(r == can for r in remotes)'),
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
    ("worktree_bo_qua_tep_moi",
     ('"--untracked-files=all"', '"--untracked-files=no"'),
     ["t12_tep_khong_theo_doi_van_tinh_la_ban"]),
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
    tam = Path(tempfile.mkdtemp(prefix="lt_db_"))
    try:
        for ten, cap, phai_chet in DOT_BIEN:
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
            chet = []
            for fn in CA:
                if fn.__name__ not in phai_chet:
                    continue
                try:
                    fn()
                except AssertionError:
                    chet.append(fn.__name__)
                except Exception as e:  # noqa: BLE001
                    chet.append(f"{fn.__name__}({type(e).__name__})")
            ok = len(chet) == len(phai_chet)
            if not ok:
                hong += 1
            print(f"  {ten:<28} {'OK' if ok else 'SAI'}  giet {len(chet)}/{len(phai_chet)}: "
                  f"{', '.join(chet) or '(khong ca nao chet)'}")
    finally:
        LAUNCHER_DANG_DUNG = LAUNCHER
        shutil.rmtree(tam, ignore_errors=True)
        # Chốt cuối: tệp thật PHẢI y nguyên. Không tin `finally` - lượt trước
        # chết vì tin nó.
        if LAUNCHER.read_text(encoding="utf-8") != goc:
            print("  !! launcher.py DA BI DOI - dot bien ro ri ra tep that")
            hong += 1
    return hong


# ---------------------------------------------------------------------- main

def main() -> int:
    if "--dot-bien" in sys.argv:
        print("TU DOT BIEN - moi dot bien PHAI giet dung cac ca da chi dinh:")
        hong = chay_dot_bien()
        print(f"\nDOT BIEN: {len(DOT_BIEN) - hong}/{len(DOT_BIEN)} dat")
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
