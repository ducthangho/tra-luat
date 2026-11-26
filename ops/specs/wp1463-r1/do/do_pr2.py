#!/usr/bin/env python3
"""wp1463 (PR2) — bằng chứng đo trước merge của SPEC r16. KHÔNG phải `*_test.py`, không đăng ký vào registry. Chạy bằng `python3 -B`:
  do_pr2.py vung [--root KHO] [--luu DIR]            Nghiệm thu 4 (rc 0 SACH · 4 NGOAI_VUNG · 3 KHONG_DO_DUOC)
  do_pr2.py ab <SHA_BASE> [--root KHO] [--luu DIR]   Nghiệm thu 1, 2, 5 (hai clone dựng trong MỘT lệnh; chín phép của bộ so)
  do_pr2.py registry [--root KHO] [--tu DIR]         Nghiệm thu 3 (`--tu` = thư mục `--luu` của `ab`, khỏi chạy lại bộ)
  do_pr2.py tu-kiem [--dot-bien] [--root KHO]        tự kiểm bộ so, phép đo vùng và bộ chạy (không cần cây git)
Hook và probe của `vung` được GHI RA thư mục tạm ngoài kho rồi nạp qua PYTHONPATH (tệp này được theo dõi; chạy probe từ chính nó sẽ
đưa nó vào tập quan sát). Giới hạn của `vung`, khai thẳng (SPEC r16 "Bảo đảm giảm"): tiến trình KHÔNG phải Python, Python gọi qua shell,
lần đọc không phát sự kiện audit `open`, Python con không hook bị che bởi dòng khởi động thừa, và Python con KHÔNG NHẬN RA ĐƯỢC theo
`la_python` (bản sao/bản đổi tên của trình thông dịch chạy không hook — PR2-C04, giao packet NO-PR2-VUNG-CAP-HDH) đều KHÔNG bị quan sát.
Cũng KHÔNG bị đếm: lần sinh Python không phát sự kiện audit (`multiprocessing` spawn/forkserver gọi thẳng `_posixsubprocess.fork_exec`) và tệp chạy
tương đối mà `preexec_fn` đổi thư mục trước exec (hook chỉ thấy `cwd=` và cwd của tiến trình sinh — R16-1).
Giới hạn của `chay_quan_sat` (R16-3): xem `GIOI_HAN_QUAN_SAT` — hậu duệ tự rời nhóm tiến trình/phiên có thể sống sót sau bước dọn; bộ chạy bị
SIGTERM/SIGKILL (không phải ngoại lệ Python) thì không có đường dọn; `chay_bo` của `ab`/`registry` KHÔNG sở hữu nhóm (không thuộc R16-2).
"""
import ast
import contextlib
import hashlib
import importlib.util
import inspect
import io
import json
import os
import re
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import types

K = "ops/ci_provenance_test.py"
Z = frozenset({"ops/ci_provenance_test.py", "ops/ci_provenance.py", ".github/workflows/ci.yml", "requirements.txt",
               ".claude/dev/ci_dang_ky_test.py", ".github/workflows/ops-do-workflow-definition.yml", "ops/bash_nen.py",
               ".github/workflows/ci-dot-bien-du.yml", ".github/workflows/launcher-windows.yml",
               "ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json", "ops/specs/wp1460-r1/hop_dong/fixture.json"})
GOC = frozenset({"AGENTS.md", "CHANGELOG.md", "CLAUDE.md", "CONTEXT.md", "INSTALL.md", "README.md", "SKILL.md"})

def oracle(doi):
    if doi is None:
        return "day_du"
    for x in doi:
        if x in Z or x.startswith("ops/cai_") or x.startswith("ops/cong_cu") or ("/" not in x and x not in GOC):
            return "day_du"
    return "nhe"

_W, _H = ".github/workflows/", "ops/specs/wp1460-r1/"
BANG = (  # bảng fixture vùng của SPEC mục 3, đúng thứ tự; băm kiểm ở `bam_bang`
    ("khong_do_duoc", None, "day_du"), ("rong", [], "nhe"), ("bo", ["ops/ci_provenance_test.py"], "day_du"), ("dich", ["ops/ci_provenance.py"], "day_du"), ("ci_yml", [_W + "ci.yml"], "day_du"),
    ("requirements", ["requirements.txt"], "day_du"), ("bo_chon", [".claude/dev/ci_dang_ky_test.py"], "day_du"), ("wf_wd", [_W + "ops-do-workflow-definition.yml"], "day_du"),
    ("bash_nen", ["ops/bash_nen.py"], "day_du"), ("wf_dot_bien_du", [_W + "ci-dot-bien-du.yml"], "day_du"), ("wf_launcher", [_W + "launcher-windows.yml"], "day_du"),
    ("cai_cong_cu", ["ops/cai_cong_cu.sh"], "day_du"), ("cong_cu_yaml", ["ops/cong_cu.yaml"], "day_du"), ("goc_la", ["pyproject.toml"], "day_du"), ("goc_ten_bo", ["ci_provenance.py"], "day_du"),
    ("goc_tai_lieu", ["README.md", "CLAUDE.md", "CHANGELOG.md"], "nhe"), ("tai_lieu", ["docs/x.md"], "nhe"), ("spec_ho_so", ["ops/specs/wp1463-r1/SPEC.md", "ops/land/x.yaml"], "nhe"),
    ("ops_khac", ["ops/ci_duong_nhanh.py", "ops/cong_cu_test.py"], "day_du"), ("ops_khac_nhe", ["ops/ci_duong_nhanh.py", "ops/nhanh_don_duoc_test.py"], "nhe"),
    ("gan_dung_hau_to", ["ops/ci_provenance.pyi", "ops/ci_provenance_test.py.bak", "ops/bash_nen.py~"], "nhe"),
    ("gan_dung_thu_muc", ["x/ops/ci_provenance.py", "ops/ci_provenance/x.py", ".claude/dev/ci_dang_ky_test.pyc"], "nhe"),
    ("gan_dung_workflow", [_W + "ci-dot-bien-du.yml.bak", _W + "launcher-windows.yaml", "x/" + _W + "ci-dot-bien-du.yml", ".github/launcher-windows.yml"], "nhe"),
    ("workflow_khac", [_W + "khac.yml", _W + "ops-publish-lease.yml"], "nhe"), ("dev_khac", [".claude/dev/packet_loop.py", ".claude/settings.json"], "nhe"),
    ("hon_hop", ["docs/x.md", "ops/bash_nen.py"], "day_du"), ("hon_hop_workflow", ["docs/x.md", _W + "launcher-windows.yml"], "day_du"),
    ("hop_dong_schema", [_H + "hop_dong/bien_nhan_audit.v1.schema.json"], "day_du"), ("hop_dong_fixture", [_H + "hop_dong/fixture.json"], "day_du"),
    ("hop_dong_gan_dung", [_H + "hop_dong/khac.json", _H + "fixture.json", _H + "hop_dong/fixture.json.bak"], "nhe"))
BAM_BANG = "0aba13e7b73bee2a09d4a5aac541dfba76dbe4497edde2d77a938ac04a375e58"

def bam_bang(bang=BANG):
    return hashlib.sha256("".join(f"{n}\t{json.dumps(d)}\t{e}\n" for n, d, e in bang).encode()).hexdigest()

# ====================================================================== vung (Nghiệm thu 4)
SACH, NGOAI, KDD = "SACH", "NGOAI_VUNG", "KHONG_DO_DUOC"
MA_VUNG = {SACH: 0, NGOAI: 4, KDD: 3}
PHEP = ("bo_day_du", "phan_chung_nguyen", "phan_chung_go_bon_khoa")   # tập ĐÓNG, mỗi tên đúng MỘT lần
CHE_DO_PROBE = {"phan_chung_nguyen": "nguyen", "phan_chung_go_bon_khoa": "go_bon_khoa"}
NHAN_CHUNG = {"bo_day_du": "ops/ci_provenance.py", "phan_chung_nguyen": ".github/workflows/ci.yml", "phan_chung_go_bon_khoa": ".github/workflows/ci.yml"}
CO, VANG = ({"NHE": x, "MAU_DAY_DU": x, "MAU_NHE": x, "VUNG_THEM": x, "so_vung_them": 7 * x} for x in (True, False))
DAU_VET = {"nguyen": (CO, CO), "go_bon_khoa": (CO, VANG)}   # (trước, sau) của bản nạp ngay trước `phan_chung()`
_RE_PY = re.compile(r"python[0-9.]*(\.exe)?$")

# Hook cho MỌI tiến trình Python thừa kế PYTHONPATH. Mỗi dòng nhật ký: JSON [pid, ppid, kiểu, dữ liệu]. Kiểu: BAT_DAU
# (dữ liệu = [starttime, sys.orig_argv]) · MO/THAT (đường dẫn theo chữ / sau realpath) · DIRFD (os.open tên tương đối
# với dir_fd, giải theo /proc/self/fd/<fd>) · DIRFD_KHONG_GIAI · SINH (argv của tiến trình con sắp tạo; pid = tiến trình sinh; `that` =
# realpath của tệp chạy, giải NGAY lúc ghi sự kiện trong ngữ cảnh khởi chạy thật của con — R16-1).
HOOK_SRC = r'''
import json, os, sys, threading
_LOG = os.environ.get("WP1463_VUNG_LOG")
if _LOG:
    _fd = os.open(_LOG, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    _tl = threading.local()
    def _ghi(kieu, p):
        try:
            os.write(_fd, (json.dumps([os.getpid(), os.getppid(), kieu, p]) + "\n").encode("utf-8", "surrogateescape"))
        except Exception:
            pass
    def _ghi_duong(kieu, p):
        _ghi(kieu, p)
        try:
            that = os.path.realpath(p)
            if that != p:
                _ghi("THAT", that)
        except Exception:
            pass
    def _argv(x):
        try:
            return [os.fsdecode(a) for a in x] if isinstance(x, (list, tuple)) else [os.fsdecode(x)]
        except Exception:
            return [repr(x)]
    def _that(x, cwd, tim):
        # R16-1 (PR2-C06): realpath của tệp chạy trong NGỮ CẢNH KHỞI CHẠY THẬT của con, giải ngay lúc này (về sau symlink có thể đã mất): tên
        # chứa `/` giải theo cwd mà CON được khởi chạy (`cwd=` riêng của lời gọi, không thì cwd HIỆN TẠI của tiến trình sinh — không phải cwd
        # của bộ đọc nhật ký); tên trần thì dò PATH của chính lời gọi như execvpe (trúng đầu tiên). Không giải được ⇒ None.
        try:
            x, goc = os.fsdecode(x), os.path.abspath(os.fsdecode(cwd)) if cwd is not None else os.getcwd()
            for u in ([x] if os.path.dirname(x) or tim is None else [os.path.join(os.fsdecode(d), x) for d in tim()]):
                u = os.path.join(goc, u)
                if os.path.isfile(u) and os.access(u, os.X_OK):
                    return os.path.realpath(u)
        except Exception:
            pass
        return None
    def _sinh(exe, argv, cwd=None, tim=None):
        exe, argv = (_argv(exe)[0] if exe else None), _argv(argv)
        _ghi("SINH", {"exe": exe, "argv": argv, "that": sorted({t for t in (_that(x, cwd, tim) for x in (exe, *argv[:1]) if x) if t})})
    def _hook(ev, args):
        if getattr(_tl, "trong", False):
            return
        _tl.trong = True
        try:
            if ev == "open" and args and isinstance(args[0], (str, bytes)) and not getattr(_tl, "dirfd", False):
                _ghi_duong("MO", os.path.abspath(os.fsdecode(args[0])))
            elif ev == "subprocess.Popen":   # (executable, args, cwd, env): con chdir(cwd) TRƯỚC khi exec; tên trần dò PATH của env ấy
                _sinh(args[0], args[1], args[2], lambda: os.get_exec_path(args[3]))
            elif ev == "os.posix_spawn":     # audit không phân biệt posix_spawn (nguyên đường dẫn) với posix_spawnp (dò PATH của tiến trình sinh)
                _sinh(args[0], args[1], None, lambda: ["", *os.get_exec_path()])
            elif ev == "os.exec":            # execv*: nguyên đường dẫn theo cwd hiện tại (execvp* tự dò PATH rồi gọi lại với đường dẫn đủ)
                _sinh(args[0], args[1])
            elif ev == "os.system":
                _ghi("SINH", {"exe": "/bin/sh", "argv": ["sh", "-c", os.fsdecode(args[0])]})
        finally:
            _tl.trong = False
    _goc_open = os.open
    def _open(path, flags, mode=0o777, *, dir_fd=None):
        if dir_fd is None or os.path.isabs(os.fsdecode(path)):
            return _goc_open(path, flags, mode, dir_fd=dir_fd)
        try:
            _ghi_duong("DIRFD", os.path.normpath(os.path.join(os.readlink(f"/proc/self/fd/{dir_fd}"), os.fsdecode(path))))
        except Exception:
            _ghi("DIRFD_KHONG_GIAI", os.fsdecode(path))
        _tl.dirfd = True
        try:
            return _goc_open(path, flags, mode, dir_fd=dir_fd)
        finally:
            _tl.dirfd = False
    os.open = _open
    try:
        os.supports_dir_fd.add(_open)   # shutil.rmtree chọn nhánh an toàn theo tập này
    except Exception:
        pass
    try:
        with open("/proc/self/stat") as _f:
            _st = _f.read().rsplit(")", 1)[1].split()[19]
    except Exception:
        _st = None
    sys.addaudithook(_hook)
    _ghi("BAT_DAU", [_st, list(getattr(sys, "orig_argv", sys.argv))])
'''

# Probe `phan_chung()` đứng riêng: in DẤU VẾT của chính bản nạp (trước/sau khi gỡ) và kế hoạch THẬT cho từng hàng bảng.
PROBE_SRC = r'''
import contextlib, importlib.util, io, json, os, sys
root, che_do, K = sys.argv[1], sys.argv[2], "ops/ci_provenance_test.py"
bang = json.loads(sys.argv[3])
os.chdir(root)
sys.path[:0] = [os.path.join(root, ".claude", "dev"), os.path.join(root, "ops")]
spec = importlib.util.spec_from_file_location("reg_do", os.path.join(root, ".claude", "dev", "ci_dang_ky_test.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
BON = ("NHE", "MAU_DAY_DU", "MAU_NHE", "VUNG_THEM")
dau_vet = lambda: {**{t: K in getattr(m, t) for t in BON}, "so_vung_them": len(m.VUNG_THEM.get(K, ()))}
kq = {"che_do": che_do, "truoc": dau_vet()}
if che_do == "go_bon_khoa":
    for t in BON:
        getattr(m, t).pop(K, None)
kq["sau"] = dau_vet()
kq["hang"] = [[n, (m.ke_hoach(d).get(K) or (None,))[0]] for n, d in bang]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    kq["phan_chung"] = m.phan_chung()
print("PROBE_KQ " + json.dumps(kq, ensure_ascii=False), flush=True)
'''

def la_python(sinh):
    """Python con NHẬN RA ĐƯỢC (SPEC r16 Nghiệm thu 4, R15-4, R16-1): `exe` hoặc `argv[0]` có tên cơ sở khớp `_RE_PY`, hoặc có realpath trùng
    realpath của trình thông dịch đang chạy. Realpath ấy là `that` do HOOK giải ngay lúc ghi sự kiện, trong ngữ cảnh khởi chạy thật của con;
    ở đây KHÔNG giải lại theo cwd của bộ đọc (PR2-C06). CỐ Ý không mở rộng biểu thức tên: bản sao/bản đổi tên không trỏ về trình thông dịch
    đang chạy thuộc PHẦN CÒN HỞ."""
    ten = [x for x in (sinh.get("exe"), (sinh.get("argv") or [None])[0]) if x]
    return any(_RE_PY.search(os.path.basename(x)) for x in ten) or os.path.realpath(sys.executable) in (sinh.get("that") or ())

def doc_log(log, root, tracked, pid_goc):
    """Nhật ký của MỘT phép → quan sát. `tap` = tệp được theo dõi khớp đường dẫn theo chữ HOẶC sau realpath.
    Đối chiếu GỘP theo phép (SPEC r12+): `bat_dau_con` = số dòng BAT_DAU của tiến trình KHÁC gốc (dòng lặp cùng pid và
    starttime tính một lần) phải ≥ `python_con` = số lần một tiến trình có hook sinh Python con; thiếu ⇒ `thieu_hook`."""
    q = {"tap": set(), "khong_giai": [], "bat_dau_goc": False, "python_con": 0, "bat_dau_con": 0, "thieu_hook": [], "hong": []}
    da_thay = set()
    try:
        with open(log, encoding="utf-8", errors="surrogateescape") as f:
            dong = f.read().splitlines()
    except OSError as e:
        q["hong"].append(f"khong doc duoc nhat ky: {type(e).__name__}")
        return q
    goc = os.path.realpath(root)
    for d in dong:
        try:
            pid, ppid, kieu, p = json.loads(d)
        except ValueError:
            q["hong"].append("dong nhat ky khong doc duoc")
            continue
        if kieu == "BAT_DAU":
            if type(ppid) is not int or type(pid) is not int or not isinstance(p, list) or len(p) != 2 or p[0] is None:
                q["hong"].append(f"dong khoi dong thieu PID cha/danh tinh: {d[:80]}")
                continue
            if (pid, p[0]) in da_thay:
                continue                                     # dòng khởi động LẶP: không tính thêm
            da_thay.add((pid, p[0]))
            if pid == pid_goc and not q["bat_dau_goc"]:
                q["bat_dau_goc"] = True
            else:
                q["bat_dau_con"] += 1
        elif kieu == "DIRFD_KHONG_GIAI":
            q["khong_giai"].append(p)
        elif kieu == "SINH":
            if type(pid) is not int or not isinstance(p, dict):
                q["hong"].append(f"lan sinh khong xac dinh duoc tien trinh sinh: {d[:80]}")
            elif la_python(p):
                q["python_con"] += 1
        elif kieu in ("MO", "DIRFD", "THAT") and isinstance(p, str):
            for r in (os.path.relpath(p, root), os.path.relpath(p, goc)):
                if r in tracked:
                    q["tap"].add(r)
        else:
            q["hong"].append(f"dong nhat ky la: {d[:80]}")
    if q["bat_dau_con"] < q["python_con"]:
        q["thieu_hook"].append(f"sinh {q['python_con']} Python con, chi {q['bat_dau_con']} dong khoi dong hook cua tien trinh con")
    return q

def kiem_vung(ten, tap):
    """Hàm THUẦN: ba điều kiện của MỘT phép trên tập quan sát CỦA CHÍNH phép ấy. Trả (dk1, dk2, tệp ngoài vùng)."""
    return bool(tap), NHAN_CHUNG[ten] in tap, sorted(x for x in tap if oracle({x}) != "day_du")

def kiem_phep(o):
    """Một phép: (kết luận, lý do không đo được, tệp ngoài vùng). (1)–(3) chỉ xét khi tiến trình gốc rc 0, hook chạy ở
    gốc, có kết quả dương và danh tính của CHÍNH phép ấy, và độ phủ tiến trình con đủ."""
    ly_do, ten = list(o.get("hong") or ()), o["ten"]
    if o.get("rc") != 0:
        ly_do.append(f"rc={o.get('rc')}")
    if not o.get("bat_dau_goc"):
        ly_do.append("hook khong chay o tien trinh goc")
    if ten == "bo_day_du":
        if o.get("dong_cuoi") != "TONG: DAT":
            ly_do.append(f"dong cuoi={o.get('dong_cuoi')!r}")
    else:
        ket, che_do = o.get("ket"), CHE_DO_PROBE[ten]
        if not isinstance(ket, dict):
            ly_do.append("thieu PROBE_KQ")
        else:
            if ket.get("phan_chung") is not True:
                ly_do.append(f"phan_chung={ket.get('phan_chung')!r}")
            if ket.get("che_do") != che_do or (ket.get("truoc"), ket.get("sau")) != DAU_VET[che_do]:
                ly_do.append(f"danh tinh lech: che_do={ket.get('che_do')!r} truoc={ket.get('truoc')} sau={ket.get('sau')}")
            hang = ket.get("hang")
            mong = [[n, e if che_do == "nguyen" else None] for n, _d, e in BANG]
            if not isinstance(hang, list) or len(hang) != len(BANG):
                ly_do.append(f"bang thieu hang: {len(hang) if isinstance(hang, list) else hang!r}/{len(BANG)}")
            else:
                lech = [m[0] for h, m in zip(hang, mong) if h != m]
                if lech:
                    ly_do.append(f"hang lech ke hoach: {lech}")
    if o.get("khong_giai"):
        ly_do.append(f"dir_fd khong giai duoc: {o['khong_giai'][:5]}")
    if o.get("thieu_hook"):
        ly_do.append(f"Python con khong co hook: {o['thieu_hook'][:3]}")
    dk1, dk2, ngoai = kiem_vung(ten, o.get("tap") or set())
    if not dk1:
        ly_do.append("(1) tap quan sat rong")
    if not dk2:
        ly_do.append(f"(2) thieu nhan chung {NHAN_CHUNG[ten]}")
    return (KDD if ly_do else NGOAI if ngoai else SACH), ly_do, ngoai

def phan_loai(obs):
    """Ba phép → (kết luận chung, chi tiết từng phép). Tập phép phải ĐÚNG `PHEP` theo TÊN; ba tập KHÔNG được hợp."""
    ct = []
    for o in obs:
        if o.get("ten") not in PHEP:
            ct.append({"ten": o.get("ten"), "ket_luan": KDD, "ly_do": ["ten phep la"], "ngoai_vung": [], "tap": []})
            continue
        kl, ly_do, ngoai = kiem_phep(o)
        ct.append({"ten": o["ten"], "ket_luan": kl, "ly_do": ly_do, "ngoai_vung": ngoai, "tap": sorted(o.get("tap") or ())})
    ten = [o.get("ten") for o in obs]
    if sorted(map(str, ten)) != sorted(PHEP):
        return KDD, ct + [{"ten": "_tap_phep", "ket_luan": KDD, "ly_do": [f"tap phep {ten} != {list(PHEP)}"], "ngoai_vung": [], "tap": []}]
    kl = [c["ket_luan"] for c in ct]
    return (KDD if KDD in kl else NGOAI if NGOAI in kl else SACH), ct

def lenh_phep(ten, root, tam):
    if ten == "bo_day_du":
        return [sys.executable, "-B", K]
    return [sys.executable, "-B", os.path.join(tam, "probe_vung.py"), root, CHE_DO_PROBE[ten], json.dumps([[n, d] for n, d, _e in BANG])]

GIOI_HAN_QUAN_SAT = ("GIOI_HAN_QUAN_SAT (SPEC r16 R16-3, bao dam GIAM, chu kho chap nhan): `chay_quan_sat` chi don hau due CON O trong nhom tien trinh/phien no tao;"
                     " hau due tu roi nhom (setsid, setpgid, double-fork sang phien khac) co the SONG SOT sau buoc don — con giu ong dau ra thi bao `DON KHONG HET`"
                     " (khong do duoc), da dong ong thi KHONG phat hien duoc (giao packet NO-PR2-QUAN-SAT-CAY-HDH).")

def goc_da_thoat(pid):
    """Trạng thái con gốc mà KHÔNG thu hồi nó (`WNOWAIT`): None = còn chạy · True = đã thoát, còn là zombie của ta nên PID (cũng là PGID/SID) vẫn
    được GHIM · False = `ECHILD`, đã bị thu hồi ở nơi khác (vd SIGCHLD bị bỏ qua) nên danh tính số ấy KHÔNG còn được ghim."""
    try:
        return os.waitid(os.P_PID, pid, os.WEXITED | os.WNOHANG | os.WNOWAIT) is not None or None
    except ChildProcessError:
        return False

def thanh_vien_song(pgid):
    """Số tiến trình CÒN SỐNG (zombie không tính) của nhóm tiến trình `pgid`, đếm ở `/proc/<pid>/stat`. None = không đọc được `/proc` ⇒ KHÔNG
    xác nhận được nhóm đã hết (bên gọi coi như còn)."""
    try:
        n = 0
        for x in filter(str.isdigit, os.listdir("/proc")):
            try:
                with open(f"/proc/{x}/stat") as f:
                    tt, _cha, nhom = f.read().rsplit(")", 1)[1].split()[:3]
            except (OSError, ValueError, IndexError):
                continue                                     # tiến trình vừa hết giữa lúc quét
            n += tt not in "ZX" and nhom == str(pgid)
        return n
    except OSError:
        return None

def chon(fd, cho):   # có dữ liệu (hoặc EOF) để đọc trong `cho` giây?
    po = select.poll()
    po.register(fd, select.POLLIN)
    return bool(po.poll(max(0.0, cho) * 1000))

def _doc(fd, buf, cho, eof):
    """Chờ tối đa `cho` giây, đọc ống đầu ra nếu có dữ liệu. Trả True khi ống đã EOF (mọi tiến trình còn giữ đầu ghi đã hết)."""
    if eof:
        time.sleep(max(0.0, cho))
    elif chon(fd, cho):
        b = os.read(fd, 1 << 16)
        buf.append(b)
        eof = not b
    return eof

def don_nhom(p, buf, eof, het, tran):
    """R15-3, R16-2: dọn nhóm tiến trình/phiên do `chay_quan_sat` tự tạo (`start_new_session` ⇒ PGID == SID == p.pid) TRƯỚC khi nhả danh tính của
    nó. Danh tính được GHIM bằng chính con gốc CHƯA thu hồi: trước hàm này không lời gọi nào thu hồi `p` (không `communicate`/`wait`/`poll`;
    chỉ `waitid(WNOWAIT)`), nên dù con gốc đã thoát, PID của nó — cũng là PGID — không thể được cấp lại, và `killpg` chỉ tới các thành viên CÒN
    LẠI của đúng nhóm ấy. Mất ghim (`goc_da_thoat` False, hoặc SIGCHLD đang bị bỏ qua) ⇒ KHÔNG gửi tín hiệu nào. TERM, chờ nhóm hết thành viên sống tới `het - tran/2`; KILL,
    chờ tới `het`; đọc nốt ống tới EOF; rồi mới thu hồi `p`. Hạn `het` là TUYỆT ĐỐI nên gọi lại (bị ngắt giữa lúc dọn) không kéo dài việc dọn.
    Trả (sạch, mô tả): sạch = còn ghim VÀ nhóm không còn thành viên sống VÀ ống đã EOF; không sạch ⇒ `DON KHONG HET` ⇒ bên gọi trả không đo
    được. Giới hạn khai thẳng (R16-3, `GIOI_HAN_QUAN_SAT`): hậu duệ tự rời nhóm (`setsid`/`setpgid`/double-fork) không bị tín hiệu chạm."""
    ghim = goc_da_thoat(p.pid) is not False and signal.getsignal(signal.SIGCHLD) != signal.SIG_IGN   # SIGCHLD bị bỏ qua ⇒ không có zombie nào ghim PID
    for th, han in ((signal.SIGTERM, het - tran / 2), (signal.SIGKILL, het)) if ghim else ():
        with contextlib.suppress(OSError):
            os.killpg(p.pid, th)
        while thanh_vien_song(p.pid) != 0 and time.monotonic() < han:
            time.sleep(0.02)
    con = thanh_vien_song(p.pid) if ghim else None
    while not eof and time.monotonic() < het:
        eof = _doc(p.stdout.fileno(), buf, min(0.05, het - time.monotonic()), eof)
    p.poll()                                                 # THU HỒI con gốc = nhả danh tính, sau khi nhóm đã hết (hoặc hết hạn dọn)
    if ghim and con == 0 and eof:
        return True, f"da don va thu hoi nhom tien trinh {p.pid} (rc={p.returncode})"
    ly_do = [x for x, c in (("con goc da bi thu hoi o noi khac nen KHONG gui tin hieu", not ghim), ("khong doc duoc /proc", ghim and con is None),
                            (f"con {con} thanh vien song", bool(con)), ("ong dau ra chua EOF: con tien trinh NGOAI nhom giu ong", not eof)) if c]
    return False, f"DON KHONG HET trong {tran} s (nhom tien trinh {p.pid}, rc={p.returncode}): {'; '.join(ly_do)}"

def chay_quan_sat(cmd, cwd, log, tam, timeout=7200, tran_don=20.0):
    """Chạy MỘT phép dưới hook, trong phiên/nhóm tiến trình RIÊNG mà hàm này sở hữu (R15-3). R16-2: MỌI đường ra sau khi đã sinh con — trả bình
    thường, quá hạn, ngoại lệ, bị ngắt (`KeyboardInterrupt`) lúc đang chờ — đều qua `don_nhom` trước khi nhả danh tính của nhóm; ngoại lệ GỐC
    được ném lại sau khi dọn; quá hạn hoặc dọn không hết ⇒ trả không đo được kèm lý do và đầu ra đã bắt. Chờ bằng `poll` + `waitid(WNOWAIT)`
    (không `communicate`: nó thu hồi con gốc khi bị ngắt, làm mất ghim trước khi kịp dọn — PR2-C05)."""
    if not (hasattr(os, "killpg") and hasattr(os, "waitid")):
        return None, None, "LOI_CHAY: KHONG_DO_DUOC: nen khong co nhom tien trinh kieu POSIX (killpg/waitid)"
    env = {k: v for k, v in os.environ.items() if k != "CI_PROVENANCE_KHONG_DOT_BIEN"}
    env["PYTHONPATH"] = tam + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env.update(WP1463_VUNG_LOG=log, PYTHONDONTWRITEBYTECODE="1")
    open(log, "w").close()
    p, buf, eof, loi, het = None, [], False, None, time.monotonic() + timeout
    try:
        p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
        while not eof or goc_da_thoat(p.pid) is None:        # xong = ống EOF VÀ con gốc đã thoát (chưa thu hồi)
            if time.monotonic() >= het:
                raise subprocess.TimeoutExpired(cmd, timeout)
            eof = _doc(p.stdout.fileno(), buf, min(0.05, het - time.monotonic()), eof)
    except BaseException as e:   # quá hạn, ngoại lệ hay bị ngắt: giữ lại, DỌN đã rồi mới ném/trả
        loi = e
    if p is None:   # chưa sinh được con ⇒ không có gì để dọn; không chạy được ⇒ không đo được
        if not isinstance(loi, OSError):
            raise loi
        return None, None, f"LOI_CHAY: {type(loi).__name__}: {loi}"
    het_don = time.monotonic() + tran_don
    while True:   # bị ngắt LẦN NỮA giữa lúc dọn thì dọn tiếp (hạn dọn tuyệt đối), giữ ngắt ấy để ném lại
        try:
            sach, mo_ta = don_nhom(p, buf, eof, het_don, tran_don)
            break
        except KeyboardInterrupt as e:
            loi = e if loi is None or isinstance(loi, subprocess.TimeoutExpired) else loi
    p.stdout.close()
    out = b"".join(buf).decode("utf-8", "replace")
    if loi is not None and not isinstance(loi, subprocess.TimeoutExpired):
        raise loi
    if loi is not None or not sach:
        return None, None, f"LOI_CHAY: {'TimeoutExpired: qua han %s s' % timeout if loi is not None else 'khong qua han'} · {mo_ta}\n" + out
    return p.pid, p.returncode, out

def do_cay(root, tracked, luu=None):
    """Chạy ba phép trên cây `root` (mỗi phép một tiến trình con, một nhật ký riêng). Trả (kết luận, chi tiết, quan sát)."""
    obs = []
    with tempfile.TemporaryDirectory(prefix="wp1463-vung-") as tam:   # ngoài kho
        for ten_tep, src in (("sitecustomize.py", HOOK_SRC), ("probe_vung.py", PROBE_SRC)):
            with open(os.path.join(tam, ten_tep), "w", encoding="utf-8") as f:
                f.write(src)
        for ten in PHEP:
            log = os.path.join(tam, ten + ".log")
            pid, rc, txt = chay_quan_sat(lenh_phep(ten, root, tam), root, log, tam)
            o = {"ten": ten, "rc": rc, **doc_log(log, root, tracked, pid)}
            dong = [d for d in txt.splitlines() if d.strip()]
            if rc is None and dong:
                o["hong"].append(dong[0][:200])   # lý do không chạy được / hết giờ ra tới báo cáo
            if ten == "bo_day_du":
                o["dong_cuoi"], o["khoi_cuoi"] = (dong[-1] if dong else None), dong[-4:]
            else:
                o["ket"] = None
                for d in dong:
                    if d.startswith("PROBE_KQ "):
                        try:
                            o["ket"] = json.loads(d[9:])
                        except ValueError:
                            o["ket"] = None
            if luu:
                with open(os.path.join(luu, ten + ".out"), "w", encoding="utf-8") as f:
                    f.write(txt)
            obs.append(o)
    kl, ct = phan_loai(obs)
    return kl, ct, obs

def in_vung(kl, ct, obs):
    for c, o in zip(ct, obs):
        dk1, dk2, _ = kiem_vung(c["ten"], set(c["tap"]))
        k = o.get("ket") or {}
        print(f"PHEP {c['ten']}: {c['ket_luan']} · rc={o.get('rc')} · (1) khac rong={dk1} · (2) nhan chung {NHAN_CHUNG[c['ten']]}={dk2}"
              f" · (3) ngoai vung={c['ngoai_vung']} · Python con/dong khoi dong con={o.get('python_con')}/{o.get('bat_dau_con')}")
        print(f"  tap ({len(c['tap'])}): {c['tap']}")
        print(f"  khoi cuoi: {o.get('khoi_cuoi')}" if c["ten"] == "bo_day_du" else f"  danh tinh: che_do={k.get('che_do')} truoc={k.get('truoc')}"
              f" sau={k.get('sau')} phan_chung={k.get('phan_chung')} hang={len(k.get('hang') or ())}/{len(BANG)}")
    for c in ct:
        for x in c["ly_do"]:
            print(f"  KHONG DO DUOC ({c['ten']}): {x}")
    print(f"GIOI_HAN_VUNG (SPEC r16 R15-4, bao dam GIAM, chu kho chap nhan): Python con chi duoc DEM khi NHAN RA DUOC — exe/argv[0] co ten co so khop"
          f" {_RE_PY.pattern} hoac realpath (hook giai trong ngu canh khoi chay cua con, R16-1) trung trinh thong dich dang chay; ban sao/ban doi ten"
          " khong tro ve trinh thong dich dang chay ma chay KHONG hook thi KHONG bi do"
          " (PR2-C04, giao packet NO-PR2-VUNG-CAP-HDH).")
    print(GIOI_HAN_QUAN_SAT)
    print(f"KET_LUAN_VUNG: {kl}")

def git_tracked(root):
    r = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True)
    return None if r.returncode else {x for x in r.stdout.decode("utf-8", "surrogateescape").split("\0") if x}

def bam_tep(root, p):
    try:
        with open(os.path.join(root, p), "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None

def lenh_vung(root, luu=None):
    thieu = [c for c in ("actionlint", "shellcheck") if not shutil.which(c)]
    tracked = git_tracked(root)
    if thieu or not tracked or bam_bang() != BAM_BANG:
        print(f"KET_LUAN_VUNG: {KDD} (thieu cong cu {thieu} · tep theo doi {len(tracked or ())} · bam bang {bam_bang() == BAM_BANG})")
        return MA_VUNG[KDD]
    for p in (K, ".claude/dev/ci_dang_ky_test.py"):
        print(f"SHA256 {p}: {bam_tep(root, p)}")
    kl, ct, obs = do_cay(root, tracked, luu)
    in_vung(kl, ct, obs)
    return MA_VUNG[kl]

# ====================================================================== bộ so A/B (Nghiệm thu 2)
PHEP_SO = ("ca_bo_day_du", "cung_bang", "khong_thieu_ten", "ast_phan_hang", "luoi_phan_hang", "cung_blob_san_pham", "cong_thuc_cu_dong",
           "tong_hai_chieu", "kho_va_ben_doc_cu")
BA_BANG = ("DOT_BIEN", "DOT_BIEN_TEST", "TU_KIEM")

def _n(x):   # neo của đột biến viết có dấu `¦` để KHÔNG tự xuất hiện lần hai trong tệp này
    return x.replace("¦", "")

def xem(m):
    """Module test đã nạp → cái bộ so đọc: ba bảng, tên ca, kế hoạch đột biến của lượt đủ, `phan_hang` và mã nguồn của nó."""
    return {"bang": {b: tuple(getattr(m, b)) for b in BA_BANG}, "ca": list(m.CA), "ph": m.phan_hang, "ph_src": inspect.getsource(m.phan_hang),
            "ke_hoach": [d[0] for b in ("DOT_BIEN", "DOT_BIEN_TEST", "DOT_BIEN_DK") for d in getattr(m, b, ())]}

def doc_luot(ra):
    """Đầu ra một lượt → (dòng, kết cục A+3 hoặc None)."""
    dong = ra.rstrip("\n").split("\n")
    kc = [d[len("KET_CUC_A3: "):] for d in dong if d.startswith("KET_CUC_A3: ")]
    try:
        return dong, (json.loads(kc[0]) if len(kc) == 1 else None)
    except ValueError:
        return dong, None

def _tong_dat(dong):   # dòng `TONG:` CUỐI CÙNG của đầu ra (không đòi nó là dòng cuối: việc ấy do mẫu `MOI` canh)
    return ([d for d in dong if d.startswith("TONG: ")] or [""])[-1] == "TONG: DAT"

def _hop_le(E, ten):
    m = E.get(ten)
    return isinstance(m, dict) and all(isinstance(m.get(k), str) and m.get(k).strip() for k in ("ly_do", "nguoi_xac_nhan"))

def cong_thuc_cu(vh, kc, E):
    """Công thức cũ của `main` ở blob base `21b23dbc` (biểu thức `dat`, `du`, `xau`, `loi_tk`, `ok` chép NGUYÊN VĂN), tính CHỈ từ
    khối `cu`, KHÔNG căn theo kế hoạch; kế hoạch và hạng mong đợi đọc từ module H. `ok` None = không tính được."""
    CA, DOT_BIEN, TU_KIEM, ten_kh, cu = vh["ca"], vh["bang"]["DOT_BIEN"], vh["bang"]["TU_KIEM"], vh["ke_hoach"], kc["cu"]
    kq, kq_db = [(rc, "") for _, rc in cu["ca"]], [(t, h, "") for t, h in cu["dot_bien"]]
    tinh_duoc = [t for t, _ in cu["ca"]] == CA and [t for t, _ in cu["tu_kiem"]] == [d[0] for d in TU_KIEM]
    dat = sum(rc == 0 for rc, _ in kq)
    du = len(set(ten_kh)) == len(ten_kh) and [t for t, _, _ in kq_db] == ten_kh
    xau = [f"{t}: {h} {ct}" for t, h, ct in kq_db if h != "GIET"]
    loi_tk = [f"{ten}: mong {mong}, duoc {h}" for (ten, cu_, moi, dich, mong), (_, h) in zip(TU_KIEM, cu["tu_kiem"]) if h != mong]
    ok = dat == len(CA) > 0 and len(DOT_BIEN) > 0 and du and not xau and not loi_tk
    xau_e = [t for t, h, _ in kq_db if h != "GIET" and not (h == "SONG_SOT" and _hop_le(E, t))]
    ok_e = dat == len(CA) > 0 and len(DOT_BIEN) > 0 and du and not xau_e and not loi_tk
    return {"tinh_duoc": tinh_duoc, "ok": ok if tinh_duoc else None, "ok_e": ok_e if tinh_duoc else None, "dat": dat, "du": du, "xau": xau,
            "loi_tk": loi_tk, "g": sum(h == "GIET" for _, h, _ in kq_db)}

def so_sanh(vb, vh, ra_b, ra_h, ra_nhe, oid_b, oid_h, moi_b, E):
    """Chín phép ĐỘC LẬP (SPEC Nghiệm thu 2 a–e): mỗi phép tính từ đúng miền đọc của nó, không phép nào nhận kết quả phép khác."""
    kq, b, h = {}, vb["bang"], vh["bang"]
    def o_dau(ten):
        return [bg for bg in BA_BANG if any(d[0] == ten for d in h[bg])]
    kq["ca_bo_day_du"] = (all(len({d[0] for d in v[bg]}) == len(v[bg]) for v in (b, h) for bg in BA_BANG)
                          and all(d in h[bg] for bg in BA_BANG for d in b[bg] if any(x[0] == d[0] for x in h[bg])))
    kq["cung_bang"] = all(o_dau(d[0]) in ([], [bg]) for bg in BA_BANG for d in b[bg])
    kq["khong_thieu_ten"] = all(o_dau(d[0]) for bg in BA_BANG for d in b[bg])
    kq["ast_phan_hang"] = ast.dump(ast.parse(vb["ph_src"])) == ast.dump(ast.parse(vh["ph_src"]))
    kq["luoi_phan_hang"] = all(vb["ph"](rc, ct, "cA") == vh["ph"](rc, ct, "cA") for rc in (-9, 0, 1, 2, 3, 4, 124, 125)
                               for ct in ("", "DO:cA:x", "DO:cB:x", "HONG:cA:x"))
    kq["cung_blob_san_pham"] = bool(oid_b) and oid_b == oid_h
    dong, kc = doc_luot(ra_h)
    c = cong_thuc_cu(vh, kc, E) if kc else None
    tong_dat, tk = _tong_dat(dong), vh["bang"]["TU_KIEM"]
    kq["cong_thuc_cu_dong"] = bool(
        c and c["tinh_duoc"] and f"CA: {c['dat']}/{len(vh['ca'])} dat" in dong and f"DOT BIEN: {c['g']}/{len(vh['ke_hoach'])} bi giet dung ly do" in dong
        and c["du"] == (not any(d.startswith("[DOT BIEN THIEU/LAP/DAO VIEC]") for d in dong))
        and len(c["xau"]) == sum(d.startswith("[DOT BIEN KHONG BI GIET DUNG]") for d in dong)
        and f"TU KIEM PHAN HANG: {'DAT' if not c['loi_tk'] else 'DO'} ({len(tk)} dot bien)" in dong and len(c["loi_tk"]) == sum(d.startswith("[TU KIEM]") for d in dong))
    T = bool(kc) and all(x["trang_thai_thuc_thi"] == "hoan_tat" for x in kc["ca"] + kc["dot_bien"] + kc["tu_kiem"]) and len(tk) > 0 \
        and len({d[0] for d in tk}) == len(tk) and not E
    kq["tong_hai_chieu"] = bool(c) and (not tong_dat or c["ok_e"] is True) and (bool(E) or not (c["ok"] is True and T) or tong_dat)
    giet = {x["ten"] for x in kc["dot_bien"] if x["phan_hang_dot_bien"] == "giet"} if kc else set()
    kq["kho_va_ben_doc_cu"] = (_tong_dat(ra_b.split("\n")) and _tong_dat(ra_h.split("\n")) and set(vb["ke_hoach"]) <= giet
                               and bool(re.search(moi_b, ra_h, re.M)) and not re.search(moi_b, ra_nhe, re.M))
    return kq   # hết so_sanh

def nap_tep(duong, ten):
    spec = importlib.util.spec_from_file_location(ten, duong)
    m = importlib.util.module_from_spec(spec)
    sys.modules[ten] = m
    spec.loader.exec_module(m)
    return m

def nap_dang_ky(root):
    m = types.ModuleType("dang_ky_do_pr2")
    m.__file__ = os.path.join(root, ".claude", "dev", "ci_dang_ky_test.py")
    with open(m.__file__, encoding="utf-8") as f:
        exec(compile(f.read(), m.__file__, "exec"), m.__dict__)
    return m

def chay_bo(root, nhe):
    env = {k: v for k, v in os.environ.items() if k != "CI_PROVENANCE_KHONG_DOT_BIEN"}
    t0 = time.monotonic()
    r = subprocess.run([sys.executable, "-B", K], cwd=root, env=dict(env, CI_PROVENANCE_KHONG_DOT_BIEN="1") if nhe else env, capture_output=True)
    return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace"), round(time.monotonic() - t0, 1)

def _git(root, *a):
    r = subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None

LUOT_AB = (("base", "day_du"), ("H", "day_du"), ("H", "nhe"))   # ba lượt = ba ranh giới tiến trình của `ab`

def do_ab(cay, oid, sha_base, chay=chay_bo, luu=None):
    """Phần ĐO của `ab` trên hai cây đã dựng: ba lượt, chín phép, kết luận. R15-1: `DAT` đòi CẢ BA lượt thoát rc 0, xét SAU kết quả dương; mã
    thoát thuộc BỘ CHẠY và KHÔNG gộp vào chín phép so ngữ nghĩa. rc khác 0 được in nguyên (`LUOT … rc=`, `RC_LUOT`), lưu nguyên (`.rc`) cùng
    đầu ra chẩn đoán, và lệnh thoát 1. `chay` là tham số để tự kiểm bơm rc ở TỪNG ranh giới."""
    kq = {luot: chay(cay[luot[0]], luot[1] == "nhe") for luot in LUOT_AB}
    vb, vh = xem(nap_tep(os.path.join(cay["base"], K), "cpt_base")), xem(nap_tep(os.path.join(cay["H"], K), "cpt_h"))
    moi_b, E = nap_dang_ky(cay["base"]).MOI[K], sys.modules["cpt_h"].TUONG_DUONG_A3
    phep = so_sanh(vb, vh, kq["base", "day_du"][1], kq["H", "day_du"][1], kq["H", "nhe"][1], oid["base"], oid["H"], moi_b, E)
    for p in (K, ".claude/dev/ci_dang_ky_test.py"):
        print(f"SHA256 {p}: {bam_tep(cay['H'], p)}")
    print(f"AB base={sha_base} blob ops/ci_provenance.py base={oid['base']} H={oid['H']} (H = HEAD cua kho do, khong ghi o day)")
    for ten, che in LUOT_AB:
        rc, ra, giay = kq[ten, che]
        print(f"LUOT {ten} {che}: rc={rc} · {giay} s · {' · '.join(d for d in ra.splitlines() if d.startswith(('TIEN TRINH', 'CHE DO')))} · CPU {os.cpu_count()}")
        print("  " + " · ".join(ra.rstrip("\n").split("\n")[-4:]))
        for duoi, nd in ((".out", ra), (".rc", f"{rc}\n")) if luu else ():
            with open(os.path.join(luu, f"{ten}.{che}{duoi}"), "w", encoding="utf-8") as f:
                f.write(nd)
    print(f"KE HOACH DOT BIEN: base {len(vb['ke_hoach'])} viec · H {len(vh['ke_hoach'])} viec · ten base ⊆ H: {set(vb['ke_hoach']) <= set(vh['ke_hoach'])}")
    for p in PHEP_SO:
        print(f"PHEP {p}: {'DUNG' if phep.get(p) is True else 'SAI'}")
    rc_luot = [(f"{ten}/{che}", kq[ten, che][0]) for ten, che in LUOT_AB]
    print("RC_LUOT: " + " · ".join(f"{k}={v}" for k, v in rc_luot) + " (ca ba phai bang 0)")
    hong = [k for k, v in rc_luot if v != 0]
    dat = all(phep.get(p) is True for p in PHEP_SO) and set(phep) == set(PHEP_SO) and not hong
    print(f"KET_LUAN_AB: {'DAT' if dat else 'DO'} ({sum(phep.get(p) is True for p in PHEP_SO)}/{len(PHEP_SO)} phep dung{' · rc khac 0 o luot ' + ', '.join(hong) if hong else ''})")
    return 0 if dat else 1

def lenh_ab(root, sha_base, luu=None):
    """Hai clone (base của lease và HEAD của `root`) dựng trong MỘT lệnh, cùng các bước, XONG cả hai rồi mới đo (`do_ab`)."""
    cay, oid = {}, {}
    with tempfile.TemporaryDirectory(prefix="wp1463-ab-") as tam:
        for ten, sha in (("base", sha_base), ("H", _git(root, "rev-parse", "HEAD"))):
            d = cay[ten] = os.path.join(tam, ten)
            for c in (["git", "clone", "-q", "--no-hardlinks", root, d], ["git", "-C", d, "-c", "advice.detachedHead=false", "checkout", "-q", sha], ["git", "-C", d, "config", "core.abbrev", "7"]):
                if subprocess.run(c).returncode:
                    print(f"KET_LUAN_AB: KHONG_DO_DUOC (lenh hong: {' '.join(c)})")
                    return 3
            oid[ten] = _git(d, "rev-parse", "HEAD:ops/ci_provenance.py")
        return do_ab(cay, oid, _git(cay["base"], "rev-parse", "HEAD"), luu=luu)

def lenh_registry(root, tu=None):
    """Nghiệm thu 3: đầu ra THẬT của lượt nhẹ và lượt đủ trên H đi qua `chay_moi` THẬT của registry H với bộ chạy giả trả lại nó."""
    ra = {}
    for che in ("nhe", "day_du"):
        if tu:   # R15-1 (quét cùng lớp): rc là rc THẬT của lượt mà `ab` đã lưu, không mặc định 0; thiếu tệp `.rc` ⇒ lệnh hỏng, không ĐẠT
            with open(os.path.join(tu, f"H.{che}.out"), encoding="utf-8") as f, open(os.path.join(tu, f"H.{che}.rc"), encoding="utf-8") as g:
                ra[che] = (int(g.read()), f.read())
        else:
            ra[che] = chay_bo(root, che == "nhe")[:2]
    m, dat = nap_dang_ky(root), True
    for che_ra, che_kh, mong in (("nhe", "nhe", True), ("day_du", "day_du", True), ("day_du", "nhe", False), ("nhe", "day_du", False)):
        with contextlib.redirect_stdout(io.StringIO()) as log:
            do = m.chay_moi(moi={K: m.MOI[K]}, cach_ly={}, chay_mot=lambda p: ra[che_ra], doc_moi_truong=lambda: "github-actions/linux",
                            doc_trong_ci=lambda: True, doc_nen_windows=lambda: False, kh={K: (che_kh, "do_pr2 registry")})
        dong = [d for d in log.getvalue().splitlines() if d.startswith("CI_DANG_KY ")]
        dat = dat and (do == 0) is mong
        print(f"REGISTRY dau ra {che_ra} / ke hoach {che_kh}: {'ĐẠT' if do == 0 else 'ĐỎ'} (mong {'ĐẠT' if mong else 'ĐỎ'}) · {' | '.join(dong)}")
    print(f"KET_LUAN_REGISTRY: {'DAT' if dat else 'DO'} (dau ra {'doc tu ' + tu if tu else 'chay tai cho'})")
    return 0 if dat else 1

# ====================================================================== tự kiểm bộ so (không cần cây git)
MOI_GIA = (r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: ([1-9]\d*)/\3 bi giet dung ly do\n"
           r"TU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z")   # chép mẫu `MOI` của bộ tại base (chỉ cho đầu vào tổng hợp)
HT = "hoan_tat"

def luot_gia(bo, v, kq_db=None, kq_tk=None, E=None, che="day_du"):
    """Đầu ra của MỘT lượt tổng hợp, dựng bằng CHÍNH các hàm của bộ H theo cách `main` in — nhất quán với view `v` như lượt thật."""
    ten_kh, tk, E = v["ke_hoach"], [(d[0], d[4]) for d in v["bang"]["TU_KIEM"]], E or {}
    kq_db = ([(t, "GIET", HT) for t in ten_kh] if che != "nhe" else []) if kq_db is None else kq_db
    kq_tk, kq_ca = [(t, m, HT) for t, m in tk] if kq_tk is None else kq_tk, [(t, 0, HT, "passed") for t in v["ca"]]
    kc = bo.tinh_ket_cuc(che, v["ca"], ten_kh, tk, kq_ca, kq_db, kq_tk, E, v["bang"]["DOT_BIEN"])
    cu = bo.cong_thuc_cu(v["ca"], v["bang"]["DOT_BIEN"], tk, ten_kh, [x[:2] for x in kq_ca], kq_db, kq_tk, E)
    dong = ["TIEN TRINH: 1", f"CHE DO: {che}"] + ["[DOT BIEN THIEU/LAP/DAO VIEC] x"] * (not cu["du"] and che != "nhe") \
        + [f"[DOT BIEN KHONG BI GIET DUNG] {t}: {h} " for t, h, _ in cu["xau"]] + [f"[TU KIEM] {x}" for x in cu["loi_tk"]] \
        + ["KET_CUC_A3: " + json.dumps(kc, ensure_ascii=False, sort_keys=True, separators=(",", ":"))] \
        + bo.dong_ket_luan(che, cu["dat"], len(v["ca"]), sum(h == "GIET" for _, h, _ in kq_db), len(ten_kh), not cu["loi_tk"], len(tk), kc["ket_luan_tong"])
    return "\n".join(dong) + "\n"

def _sua_kc(ra, f):   # đổi ĐÚNG khối KET_CUC_A3 của một đầu ra, mọi dòng khác giữ nguyên
    dong, kc = doc_luot(ra)
    f(kc)
    return "\n".join("KET_CUC_A3: " + json.dumps(kc, ensure_ascii=False, sort_keys=True, separators=(",", ":")) if d.startswith("KET_CUC_A3: ") else d
                     for d in dong) + "\n"

def dau_vao_so(bo):
    """[(tên đầu vào, đối số của `so_sanh`, TẬP phép phải sai)] — mỗi đầu vào là nền khoẻ đổi ĐÚNG trường nó nêu (SPEC Nghiệm thu 2)."""
    src = inspect.getsource(bo.phan_hang)
    def view(db=None, dbt=None, tk=None, src=src):
        ns = {}
        exec(src, ns)
        bang = {"DOT_BIEN": (("A1_xoa_co_attempt", "neo1", "thay1", "c01"), ("m2", "neo2", "thay2", "c02")) if db is None else db,
                "DOT_BIEN_TEST": (("T1", "neo3", "thay3", "c03"),) if dbt is None else dbt, "TU_KIEM": (("k1", "neo4", "thay4", "c01", "TIN_DUNG_GIA"),) if tk is None else tk}
        return {"bang": bang, "ca": ["c01_a", "c02_b", "c03_c"], "ph": ns["phan_hang"], "ph_src": src, "ke_hoach": [d[0] for b in BA_BANG[:2] for d in bang[b]]}
    VB = view()
    def dv(vh=None, E=None, sua=None, **kw):   # nền khoẻ: lượt H nhất quán với CHÍNH module H của đầu vào
        vh = vh or view()
        a = {"vb": VB, "vh": vh, "ra_b": luot_gia(bo, VB), "ra_h": luot_gia(bo, vh, E=E, **kw), "ra_nhe": luot_gia(bo, vh, che="nhe"), "oid_b": "a" * 40,
             "oid_h": "a" * 40, "moi_b": MOI_GIA, "E": E or {}}
        a.update(sua(a) if sua else {})
        return a
    A1, m2, T1, k1 = VB["bang"]["DOT_BIEN"] + VB["bang"]["DOT_BIEN_TEST"] + VB["bang"]["TU_KIEM"]
    def loi(kq_db=None, **kw):   # đối chứng của (d): lượt dựng NHẤT QUÁN theo công thức cũ
        return dv(kq_db=[(t, *(kq_db or {}).get(t, ("GIET", HT))) for t in VB["ke_hoach"]], **kw)
    def tk_lech(a):
        ra = _sua_kc(a["ra_h"], lambda kc: kc["cu"]["tu_kiem"][0].__setitem__(1, "GIET"))
        return {"ra_h": ra.replace("KET_CUC_A3: ", "[TU KIEM] k1: mong TIN_DUNG_GIA, duoc GIET\nKET_CUC_A3: ").replace("TU KIEM PHAN HANG: DAT", "TU KIEM PHAN HANG: DO")}
    ca_bo, d_, t_, kho = {"ca_bo_day_du"}, "cong_thuc_cu_dong", "tong_hai_chieu", "kho_va_ben_doc_cu"
    return [
        ("nen_khoe", dv(), set()),
        ("a_doi_thay_the", dv(view(db=((*A1[:2], "thay KHAC", A1[3]), m2))), ca_bo), ("a_doi_neo", dv(view(db=((A1[0], "neo KHAC", *A1[2:]), m2))), ca_bo),
        ("a_doi_tien_to_ca_dich", dv(view(db=((*A1[:3], "c02"), m2))), ca_bo), ("a_doi_hang_mong_tu_kiem", dv(view(tk=((*k1[:4], "SONG_SOT"),))), ca_bo),
        ("a_chuyen_bang", dv(view(db=(A1,), dbt=(m2, T1))), {"cung_bang"}), ("a_thieu_ten_base", dv(view(db=(A1,))), {"khong_thieu_ten", kho}),
        ("b_phan_hang_rc4_HONG", dv(view(src=src.replace('"TIN_DUNG_GIA" if rc == 4 else "HONG"', '"HONG"'))), {"ast_phan_hang", "luoi_phan_hang"}),
        ("c_oid_khac", dv(sua=lambda a: {"oid_h": "b" * 40}), {"cung_blob_san_pham"}),
        ("d_dong_dot_bien_tu_so_M_tru_1", dv(sua=lambda a: {"ra_h": a["ra_h"].replace("DOT BIEN: 3/3", "DOT BIEN: 2/3")}), {d_, kho}),
        ("d_cu_dot_bien_doi_cho", dv(sua=lambda a: {"ra_h": _sua_kc(a["ra_h"], lambda kc: kc["cu"]["dot_bien"].reverse())}), {d_, t_}),
        ("d_bo_tu_kiem_khoi_cu", dv(sua=lambda a: {"ra_h": _sua_kc(a["ra_h"], lambda kc: kc["cu"]["tu_kiem"].clear())}), {d_, t_}),
        ("d_cu_tu_kiem_lech_hang_ma_TONG_DAT", dv(sua=tk_lech), {t_, kho}),
        ("d_TONG_DO_tren_nen_khoe", dv(sua=lambda a: {"ra_h": a["ra_h"][:-len("TONG: DAT\n")] + "TONG: DO\n"}), {t_, kho}),
        ("e_them_dong_sau_TONG", dv(sua=lambda a: {"ra_h": a["ra_h"] + "dong thua\n"}), {kho}),
        ("e_hang_A3_cua_ten_base_thanh_song", dv(sua=lambda a: {"ra_h": _sua_kc(a["ra_h"], lambda kc: kc["dot_bien"][0].__setitem__("phan_hang_dot_bien", "song"))}), {kho}),
        ("e_dau_ra_nhe_khop_MOI_base", dv(sua=lambda a: {"ra_nhe": a["ra_h"]}), {kho}),
        ("duong_them_muc_moi", dv(view(db=(A1, m2, ("m9", "neo9", "thay9", "c02")))), set()),
        ("duong_phan_hang_doi_khoang_trang_chu_thich", dv(view(src=src.replace("    if rc == 0:", "    # chu thich\n    if rc  ==  0:"))), set()),
        *[(f"doi_chung_d_phan_tu_ha_tang_cu_{h}", loi({"m2": (h, "infrastructure_error")}), {kho}) for h in ("GIET", "TIN_DUNG_GIA", "SONG_SOT")],
        ("doi_chung_d_tu_kiem_het_han_trong_ca", dv(kq_tk=[("k1", "TIN_DUNG_GIA", "timed_out")]), {kho}),
        ("doi_chung_d_thieu_ket_qua_dot_bien", dv(kq_db=[("A1_xoa_co_attempt", "GIET", HT)]), {kho}),
        ("doi_chung_d_E_khac_rong_XANH", loi({"m2": ("SONG_SOT", HT)}, E={"m2": {"ly_do": "x", "nguoi_xac_nhan": "A"}}), {kho}),
        ("doi_chung_d_thieu_tu_kiem_TONG_DO", dv(kq_tk=[]), {d_, kho})]

def tu_kiem_so(bo):
    """[(tên, tập sai KHAI, véc-tơ chín phép)]."""
    return [(ten, khai, so_sanh(**a)) for ten, a, khai in dau_vao_so(bo)]

DOT_BIEN_SO = [(f"go_{p}", "    return kq   # hết ¦so_sanh", f'    kq["{p}"] = True\n    return kq', (p,)) for p in PHEP_SO] + [
    ("d_tinh_cong_thuc_cu_tu_tang_A3", 'kq, kq_db = [(rc, "") for _, rc in cu["ca"]], ¦[(t, h, "") for t, h in cu["dot_bien"]]',
     'kq, kq_db = [(rc, "") for _, rc in cu["ca"]], [(x["ten"], {"giet": "GIET", "song": "SONG_SOT", "tin_dung_gia": "TIN_DUNG_GIA"}.get(x["phan_hang_dot_bien"], "HONG"), "") for x in kc["dot_bien"]]',
     PHEP_SO[6:8]),
    ("d_so_TONG_bang_dang_thuc_voi_ok_cu", 'and (bool(E) or not (c["ok"] is True ¦and T) or tong_dat)', 'and tong_dat == (c["ok"] is True)', PHEP_SO[6:8]),
    ("d_du_cu_tren_cu_da_can_theo_ke_hoach", 'and [t for t, _, _ in kq_db] ¦== ten_kh', 'and sorted(t for t, _, _ in kq_db) == sorted(ten_kh)', PHEP_SO[6:8]),
    ("d_luat_thuan_dung_ok_cu_thay_ok_cu_E", '(not tong_dat or c["ok_e"] ¦is True)', '(not tong_dat or c["ok"] is True)', PHEP_SO[6:8]),
    ("d_ok_cu_khong_tinh_duoc_coi_la_True", '(not tong_dat or c["ok_e"] ¦is True)', '(not tong_dat or c["ok_e"] is not False)', PHEP_SO[6:8]),
    ("d_E_khac_rong_ep_khong_xanh", '(not tong_dat or c["ok_e"] ¦is True)', '(not tong_dat or (c["ok_e"] is True and not E))', PHEP_SO[6:8])]

# ====================================================================== tự kiểm phép đo vùng (cây GIẢ, tiến trình THẬT)
_VT = tuple(sorted(Z - {K, "ops/ci_provenance.py", ".github/workflows/ci.yml", "requirements.txt"}))
_GIA = r"""
import atexit, os, subprocess, sys
CA, PH, X = os.environ.get("WP_CA", "khoe"), os.environ.get("WP_PHEP", ""), "ops/x_ngoai.txt"
def gay(phep):   # hành vi của ca tự kiểm, CHỈ ở phép bị nhắm
    if PH != phep:
        return
    if CA == "doc_thang":
        open(X).read()
    elif CA in ("doc_con", "con_I", "con_S", "con_E", "doc_con_doi_ten"):
        # `doc_con_doi_ten`: BẢN SAO đổi tên của trình thông dịch, thừa kế môi trường (có hook); PYTHONHOME chỉ để bản sao ở đường dẫn khác tìm được thư viện chuẩn
        py, env = (os.environ["WP_PY"], dict(os.environ, PYTHONHOME=sys.base_prefix)) if CA == "doc_con_doi_ten" else (sys.executable, None)
        subprocess.run([py, *{"con_I": ["-I"], "con_S": ["-S"], "con_E": ["-E"]}.get(CA, []), "-c", f"open({X!r}).read()"], check=True, env=env)
    elif CA == "doc_dirfd":
        fd = os.open("ops", os.O_RDONLY)
        os.close(os.open("x_ngoai.txt", os.O_RDONLY, dir_fd=fd))
        os.close(fd)
    elif CA == "doc_symlink":
        os.symlink(os.path.abspath(X), os.environ["WP_LK"])
        open(os.environ["WP_LK"]).read()
        os.unlink(os.environ["WP_LK"])
    elif CA.startswith("lk_"):
        # R16-1: CÙNG trình thông dịch qua symlink WP_LKPY (tên KHÔNG khớp biểu thức), khởi chạy từ cwd KHÁC cwd của bộ đọc; `_I` = con DUY NHẤT, không hook.
        # tuyetdoi: đường dẫn tuyệt đối, `cwd=` riêng · cwd: `./tên` với `cwd=` riêng của lời gọi · chdir: `./tên` sau khi tiến trình CHA đổi thư mục · path: tên trần, chỉ PATH của lời gọi dẫn tới
        dang, (d, ten), cu = CA.split("_")[1], os.path.split(os.environ["WP_LKPY"]), os.getcwd()
        lenh = [{"tuyetdoi": os.environ["WP_LKPY"], "path": ten}.get(dang, "./" + ten), *["-I"] * CA.endswith("_I"), "-c", f"open({os.path.abspath(X)!r}).read()"]
        os.chdir(d if dang == "chdir" else cu)
        try:
            subprocess.run(lenh, check=True, cwd=d if dang in ("tuyetdoi", "cwd") else None, env=dict(os.environ, PATH=d) if dang == "path" else None)
        finally:
            os.chdir(cu)
    elif CA == "rc_sau":
        atexit.register(lambda: os._exit(42))
    elif CA == "log_rong":
        atexit.register(lambda: open(os.environ["WP1463_VUNG_LOG"], "w").close())
"""
REG_GIA = _GIA + f"""
K, PHEP = "{K}", "phan_chung_" + sys.argv[2]
MOI, NHE, MAU_DAY_DU, MAU_NHE, VUNG_THEM, GOC = {{K: "x"}}, {{K: {{}}}}, {{K: "x"}}, {{K: "x"}}, {{K: {_VT!r}}}, {sorted(GOC)!r}
def ke_hoach(doi):
    kq = {{}}
    for p in NHE:
        vung = {{p, p[:-8] + ".py", ".github/workflows/ci.yml", "requirements.txt", *VUNG_THEM.get(p, ())}}
        du = doi is None or any(x in vung or x.startswith(("ops/cai_", "ops/cong_cu")) or ("/" not in x and x not in GOC) for x in doi)
        kq[p] = ("day_du" if du else "nhe",)
    return kq
def phan_chung():
    if not (PH == PHEP and CA == "thieu_nhan_chung"):
        open(".github/workflows/ci.yml").read()
    gay(PHEP)
    return not (PH == PHEP and CA == "phan_chung_sai")
"""
BO_GIA = _GIA + """
if not (PH == "bo_day_du" and CA == "thieu_nhan_chung"):
    open("ops/ci_provenance.py").read()
gay("bo_day_du")
print("TONG: DO" if PH == "bo_day_du" and CA == "tong_do" else "TONG: DAT", flush=True)
"""
DANG_LK = ("tuyetdoi", "cwd", "chdir", "path")   # R16-1: bốn cách khởi chạy CÙNG trình thông dịch qua symlink, từ cwd khác cwd của bộ đọc
CA_VUNG = {**dict.fromkeys(("doc_thang", "doc_con", "doc_dirfd", "doc_symlink", "doc_con_doi_ten", *(f"lk_{x}_hook" for x in DANG_LK)), NGOAI),
           **dict.fromkeys(("con_I", "con_S", "con_E", "rc_sau", "log_rong", "thieu_nhan_chung", *(f"lk_{x}_I" for x in DANG_LK)), KDD)}

def tu_kiem_vung():
    """[(tên đầu vào, kết quả mong, kết quả được)]. Phần THUẦN trên quan sát tổng hợp; phần THẬT chạy ba phép trên cây giả, mỗi ca
    nhắm ĐÚNG MỘT phép và so kết quả TỪNG phép (phép bị nhắm ra đúng kỳ vọng, mọi phép khác SACH)."""
    kq, pr = [], PHEP[1:]
    tap_pr = {".github/workflows/ci-dot-bien-du.yml", ".github/workflows/ci.yml", ".github/workflows/launcher-windows.yml", "ops/bash_nen.py"}
    tap_bo = {K, "ops/ci_provenance.py", ".github/workflows/ci.yml", "ops/bash_nen.py"}
    def qs(ten, tap, **sua):   # quan sát khoẻ của một phép, đổi đúng trường nêu ở `sua`
        o = {"ten": ten, "rc": 0, "bat_dau_goc": True, "tap": set(tap), "dong_cuoi": "TONG: DAT"}
        if ten != "bo_day_du":
            cd = CHE_DO_PROBE[ten]
            o["ket"] = {"che_do": cd, "truoc": DAU_VET[cd][0], "sau": DAU_VET[cd][1], "phan_chung": True, "hang": [[n, e if cd == "nguyen" else None] for n, _, e in BANG]}
        return {**o, **sua}
    def ba(**thay):
        return [thay.get(t, qs(t, tap_bo if t == "bo_day_du" else tap_pr)) for t in PHEP]
    def them(ten, mong, obs):
        kl, ct = phan_loai(obs)
        kq.append((ten, mong, (kl, tuple(c["ket_luan"] for c in ct))))
    them("thuan_khoe_tap_probe_da_do", (SACH, (SACH,) * 3), ba())
    for i, t in enumerate(PHEP):
        ky = lambda x, i=i: tuple(x if j == i else SACH for j in range(3))
        them(f"thuan_tap_rong_{t}", (KDD, ky(KDD)), ba(**{t: qs(t, ())}))
        them(f"thuan_thieu_nhan_chung_{t}", (KDD, ky(KDD)), ba(**{t: qs(t, (tap_bo if i == 0 else tap_pr) - {NHAN_CHUNG[t]})}))
        them(f"thuan_tep_ngoai_vung_{t}", (NGOAI, ky(NGOAI)), ba(**{t: qs(t, (tap_bo if i == 0 else tap_pr) | {"docs/x.md"})}))
    for t in pr:
        k0, ky = qs(t, tap_pr)["ket"], (lambda x, i=PHEP.index(t): tuple(x if j == i else SACH for j in range(3)))
        for j, (n, _, _) in enumerate(BANG):   # MỖI hàng của bảng một đầu vào: chỉ hàng ấy lệch ⇒ không đo được
            hang = [list(h) for h in k0["hang"]]
            hang[j][1] = "nhe" if hang[j][1] != "nhe" else "day_du"
            them(f"thuan_hang_lech_{t}_{n}", (KDD, ky(KDD)), ba(**{t: qs(t, tap_pr, ket={**k0, "hang": hang})}))
        for ten, sua in (("che_do_lech", {"che_do": "khac"}), ("dau_vet_truoc_lech", {"truoc": VANG}), ("dau_vet_sau_lech", {"sau": DAU_VET["go_bon_khoa" if t == pr[0] else "nguyen"][1]}),
                         ("bang_thieu_hang", {"hang": k0["hang"][:-1]}), ("phan_chung_khong_True", {"phan_chung": 1})):
            them(f"thuan_{ten}_{t}", (KDD, ky(KDD)), ba(**{t: qs(t, tap_pr, ket={**k0, **sua})}))
    them("thuan_tap_phep_lap", KDD, [qs(PHEP[0], tap_bo), qs(pr[0], tap_pr), qs(pr[0], tap_pr)])
    them("thuan_tap_phep_thieu", KDD, ba()[:2])
    kq = [(ten, mong, duoc if isinstance(mong, tuple) else duoc[0]) for ten, mong, duoc in kq]
    for x in ("python", "python3", "python3.13", "python.exe"):   # R15-4 (a): hàm phân loại nhận ĐÚNG các tên này, ở `exe` lẫn `argv[0]`
        kq += [(f"thuan_la_python_exe_{x}", True, la_python({"exe": "/x/" + x, "argv": ["khac"]})), (f"thuan_la_python_argv0_{x}", True, la_python({"exe": None, "argv": [x]}))]
    kq.append(("thuan_la_python_tu_choi_ten_khac", False, la_python({"exe": "/bin/bash", "argv": ["bash", "-c", "python3 x.py"]})))
    with tempfile.TemporaryDirectory(prefix="wp1463-gia-") as tam:
        root, lk, ban = os.path.join(tam, "kho"), os.path.join(tam, "thong_dich_lk"), os.path.join(tam, "thong_dich_x")   # hai tên KHÔNG khớp biểu thức
        os.symlink(os.path.relpath(os.path.realpath(sys.executable), os.path.realpath(tam)), lk)   # đích TƯƠNG ĐỐI: realpath phải theo đúng thư mục của symlink
        shutil.copy2(os.path.realpath(sys.executable), ban)   # bản sao byte-nguyên của trình thông dịch ở đường dẫn khác
        kq.append(("that_la_python_realpath_trung", True, la_python({"exe": lk, "argv": ["x"], "that": [os.path.realpath(lk)]})))
        kq.append(("that_la_python_ban_sao_doi_ten_KHONG_nhan_ra", False, la_python({"exe": ban, "argv": [ban], "that": [os.path.realpath(ban)]})))   # phần CÒN HỞ, khai thẳng
        kq.append(("that_la_python_khong_giai_lai_theo_cwd_bo_doc", False, la_python({"exe": os.path.relpath(lk), "argv": ["x"], "that": []})))   # R16-1: chỉ tin `that` của hook
        tep = {".claude/dev/ci_dang_ky_test.py": REG_GIA, K: BO_GIA, "ops/ci_provenance.py": "", ".github/workflows/ci.yml": "", "ops/x_ngoai.txt": "x"}
        for p, nd in tep.items():
            os.makedirs(os.path.dirname(os.path.join(root, p)), exist_ok=True)
            with open(os.path.join(root, p), "w", encoding="utf-8") as f:
                f.write(nd)
        def that(ca, phep):
            os.environ.update(WP_CA=ca, WP_PHEP=phep or "", WP_LK=os.path.join(tam, "lk"), WP_PY=ban, WP_LKPY=lk)
            try:
                kl, ct, _ = do_cay(root, set(tep))
            finally:
                for k in ("WP_CA", "WP_PHEP", "WP_LK", "WP_PY", "WP_LKPY"):
                    os.environ.pop(k, None)
            return kl, tuple(c["ket_luan"] for c in ct)
        kq.append(("that_khoe", (SACH, (SACH,) * 3), that("khoe", None)))
        for i, t in enumerate(PHEP):
            for ca, mong in {**CA_VUNG, **({"tong_do": KDD} if i == 0 else {"phan_chung_sai": KDD})}.items():
                kq.append((f"that_{ca}_{t}", (mong, tuple(mong if j == i else SACH for j in range(3))), that(ca, t)))
    return kq

DOT_BIEN_VUNG = [
    ("probe_dung_rieng_dung_nhan_chung_cua_bo", '"phan_chung_nguyen": ".github/workflows/ci.yml", ¦"phan_chung_go_bon_khoa": ".github/workflows/ci.yml"}', '"phan_chung_nguyen": "ops/ci_provenance.py", "phan_chung_go_bon_khoa": "ops/ci_provenance.py"}', "thuan_khoe_tap_probe_da_do"),
    ("hop_tap_luot_du_vao_quan_sat_rong_cua_probe", "kl, ly_do, ngoai = ¦kiem_phep(o)", 'kl, ly_do, ngoai = kiem_phep({**o, "tap": set().union(*[x.get("tap") or set() for x in obs])})', "thuan_tap_rong_phan_chung_nguyen"),
    ("bo_chot_song", 'dk1, dk2, ngoai = ¦kiem_vung(ten, o.get("tap") or set())', 'dk1, dk2, ngoai = True, True, kiem_vung(ten, o.get("tap") or set())[2]', "thuan_tap_rong_bo_day_du"),
    ("khong_lan_truyen_hook_sang_tien_trinh_con", '    sys.addaudithook(_hook)¦\n    _ghi("BAT_DAU"', '    sys.addaudithook(_hook)\n    os.environ.pop("PYTHONPATH", None)\n    _ghi("BAT_DAU"', "that_doc_con_bo_day_du"),
    ("giai_dir_fd_theo_cwd", 'os.path.join(¦os.readlink(f"/proc/self/fd/{dir_fd}"), os.fsdecode(path))', "os.path.join(os.getcwd(), os.fsdecode(path))", "that_doc_dirfd_bo_day_du"),
    ("chi_khop_duong_dan_theo_chu", "if r ¦in tracked:", 'if r in tracked and kieu != "THAT":', "that_doc_symlink_bo_day_du"),
    ("bo_dem_python_con", 'if q["bat_dau_con"] ¦< q["python_con"]:', "if False:", "that_con_I_bo_day_du"),
    ("bo_rc", 'if o.get("rc") ¦!= 0:', "if False:", "that_rc_sau_bo_day_du"),
    ("tap_phep_chi_so_so_luong", "if sorted(map(str, ten)) ¦!= sorted(PHEP):", "if len(ten) != len(PHEP):", "thuan_tap_phep_lap"),
    ("chay_mot_phep_hai_lan_thay_cho_phep_khac", "chay_quan_sat(¦lenh_phep(ten, root, tam)", 'chay_quan_sat(lenh_phep(ten if ten == "bo_day_du" else "phan_chung_nguyen", root, tam)', "that_khoe"),
    ("bo_so_mot_hang_nhung_van_dem", "zip(hang, mong) ¦if h != m]", 'zip(hang, mong) if h != m and m[0] != "wf_wd"]', "thuan_hang_lech_phan_chung_nguyen_wf_wd"),
    ("phep_go_chay_ban_nap_cua_phep_khac", 'CHE_DO_PROBE[ten], ¦json.dumps([[n, d]', '"nguyen", json.dumps([[n, d]', "that_khoe"),
    ("go_khong_go_khoa", "getattr(m, t).pop(¦K, None)", "getattr(m, t).get(K, None)", "that_khoe"),
    # SPEC r15 R15-4: hàm phân loại đúng như câu bảo đảm (không hẹp hơn, không rộng hơn), và bản đổi tên CÓ hook vẫn bị quan sát
    ("phan_loai_bo_realpath", 'for x in ten) or os.path.realpath(sys.executable) ¦in (sinh.get("that") or ())', "for x in ten)", "that_la_python_realpath_trung"),
    ("phan_loai_nhan_moi_ten", '_RE_PY = re.compile(¦r"python[0-9.]*(\\.exe)?$")', '_RE_PY = re.compile(r"")', "that_la_python_ban_sao_doi_ten_KHONG_nhan_ra"),
    ("hook_chi_cai_theo_ten_trinh_thong_dich", '_LOG = os.environ.get("WP1463_VUNG_LOG")\n¦if _LOG:', '_LOG = os.environ.get("WP1463_VUNG_LOG")\nif _LOG and "python" in os.path.basename(sys.executable):', "that_doc_con_doi_ten_bo_day_du"),
    # SPEC r16 R16-1 (PR2-C06): bỏ phần giải theo ngữ cảnh khởi chạy ⇒ chết ở ca symlink TƯƠNG ĐỐI (ca symlink tuyệt đối vẫn đạt dưới cả ba đột biến)
    ("la_python_giai_lai_theo_cwd_bo_doc", 'os.path.realpath(sys.executable) ¦in (sinh.get("that") or ())', "os.path.realpath(sys.executable) in map(os.path.realpath, ten)", "that_lk_chdir_I_bo_day_du"),
    ("hook_bo_qua_cwd_rieng_cua_loi_goi", "os.path.abspath(os.fsdecode(cwd)) ¦if cwd is not None else os.getcwd()", "os.getcwd()", "that_lk_cwd_I_phan_chung_nguyen"),
    ("hook_khong_do_PATH_cua_loi_goi", "[os.path.join(os.fsdecode(d), x) ¦for d in tim()]", "[x]", "that_lk_path_I_phan_chung_go_bon_khoa")]

# ====================================================================== tự kiểm BỘ CHẠY: rc của `ab`/`registry --tu` (R15-1), `chay_quan_sat` sở hữu nhóm nó sinh (R15-3, R16-2, R16-3)
MA_QS = r"""
import os, signal, subprocess, sys, time
d, tre, vai = sys.argv[1], float(sys.argv[2]), sys.argv[3]
os.environ.setdefault("WP_QS_GOC", str(os.getpid()))
for v in sys.argv[4:]:   # con gốc sinh từng cháu: cùng nhóm tiến trình, cùng ống đầu ra
    subprocess.Popen([sys.executable, __file__, d, sys.argv[2], v])
if "li" in vai:      # cháu BỎ QUA TERM (chỉ KILL kết thúc được); báo sẵn sàng để lần ngắt chỉ tới SAU đó
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    open(os.path.join(d, "san"), "w").close()
if "dong" in vai:    # cháu Ở LẠI nhóm nhưng không giữ ống đầu ra
    os.dup2(os.open(os.devnull, os.O_WRONLY), 1)
    os.dup2(1, 2)
if "tach" in vai:    # cháu TỰ RỜI phiên/nhóm, vẫn giữ ống (giới hạn R16-3)
    os.setsid()
print("DA_CHAY " + vai, flush=True)
if "ngat" in vai:    # SIGINT THẬT vào bộ quan sát, SAU khi con gốc đã thoát và cháu bỏ qua TERM đã sẵn sàng
    while os.getppid() == int(os.environ["WP_QS_GOC"]) or not os.path.exists(os.path.join(d, "san")):
        time.sleep(0.01)
    os.kill(int(os.environ["WP_QS_PID"]), signal.SIGINT)
if "thoat" in vai:   # con gốc thoát NGAY, để lại các cháu
    sys.exit(0)
time.sleep(tre)
open(os.path.join(d, "dau_" + vai), "w").close()   # dấu hẹn ghi SAU `tre` giây
"""

def tu_kiem_chay(bo, root):
    """[(tên, mong, được)]. (i) `do_ab` THẬT trên nền khoẻ (base = H = `root`, không cần git) với bộ chạy giả trả đầu ra KHOẺ kèm rc 42 ở ĐÚNG
    MỘT trong ba ranh giới ⇒ lệnh thất bại mà chín phép vẫn 9/9; đối chứng rc 0 ⇒ DAT. (ii) `registry --tu` đọc rc ĐÃ LƯU. (iii) `chay_quan_sat`
    quá hạn với con và cháu THẬT hẹn ghi dấu sau hạn ⇒ trả thất bại, giữ đầu ra đã bắt, và KHÔNG dấu nào xuất hiện sau khi dọn. (iv) R16-2/R16-3:
    mọi đường ra khác của `chay_quan_sat` (bị ngắt, trả bình thường, dọn không hết, mất ghim) và ca chỉ GHI giới hạn tách nhóm — tiến trình THẬT."""
    kq, v, cay = [], xem(bo), {"base": root, "H": os.path.join(root, "")}   # hai cách viết của CÙNG cây: bộ chạy giả phân biệt base với H
    def ab(bom, luu=None):
        def chay(r, nhe):
            luot = ("H" if r == cay["H"] else "base", "nhe" if nhe else "day_du")
            return (42 if luot == bom else 0), luot_gia(bo, v, che=luot[1]), 0.0
        with contextlib.redirect_stdout(io.StringIO()) as ra:
            rc = do_ab(cay, dict.fromkeys(cay, "a" * 40), "tu-kiem", chay, luu)
        cuoi = ra.getvalue().splitlines()[-1]
        return rc, cuoi.split(" (")[0], cuoi.split("(")[1].split(" ")[0]
    def reg(tu):
        with contextlib.redirect_stdout(io.StringIO()):
            return lenh_registry(root, tu)
    def qs(tam, tre, han, vai=("con", "chau"), tran=2.0, gia=None, bo_chld=False, ghi_dau=False):
        """Một lần `chay_quan_sat` THẬT → (rc | "KeyboardInterrupt", nhãn, dòng DA_CHAY, dấu có mặt SAU mọi thời điểm hẹn ghi, đối chứng ngoài nhóm còn sống)."""
        if not (hasattr(os, "killpg") and hasattr(os, "waitid")):
            return ("KHONG_DO_DUOC: nen khong co nhom tien trinh kieu POSIX",) * 2 if ghi_dau else "KHONG_DO_DUOC: nen khong co nhom tien trinh kieu POSIX"
        d, moc, tv_goc = tempfile.mkdtemp(dir=tam), [], thanh_vien_song
        def khi_ngat(*_):   # SIGINT thật ⇒ KeyboardInterrupt (đúng việc `signal.default_int_handler` làm), ghi thêm thời điểm
            moc.append(time.monotonic())
            raise KeyboardInterrupt
        def tv_ngat(pgid):   # ngắt LẦN NỮA đúng lúc đang dọn (lần quét đầu), các lần sau quét thật
            if not moc[1:]:
                moc.append(time.monotonic())
                raise KeyboardInterrupt
            return tv_goc(pgid)
        ngoai = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])   # đối chứng KHÔNG thuộc nhóm mà `chay_quan_sat` sở hữu
        cu = signal.signal(signal.SIGINT, khi_ngat), signal.signal(signal.SIGCHLD, signal.SIG_IGN if bo_chld else signal.SIG_DFL)
        globals()["thanh_vien_song"] = {"mu": lambda pgid: None, "ngat": tv_ngat}.get(gia, tv_goc)
        os.environ["WP_QS_PID"] = str(os.getpid())
        try:
            try:
                _pid, rc, txt = chay_quan_sat([sys.executable, "-B", os.path.join(tam, "qs.py"), d, str(tre), *vai], tam, os.path.join(d, "log"), d, timeout=han, tran_don=tran)
                nhan = tuple(x for x in ("TimeoutExpired", "DON KHONG HET") if txt.startswith("LOI_CHAY: ") and x in txt.split("\n")[0])
            except KeyboardInterrupt:   # ngắt được NÉM LẠI; `trong tran` = từ lúc ngắt tới lúc hàm rời đi không quá trần dọn (+0,5 s)
                rc, txt, nhan = "KeyboardInterrupt", "", ("trong tran" if time.monotonic() - moc[0] <= tran + 0.5 else "QUA tran",)
            finally:
                globals()["thanh_vien_song"] = tv_goc
                signal.signal(signal.SIGINT, cu[0]), signal.signal(signal.SIGCHLD, cu[1]), os.environ.pop("WP_QS_PID")
            time.sleep(tre + 0.5)   # nhìn dấu SAU mọi thời điểm hẹn ghi (tiến trình sinh trước lúc hàm rời đi ghi muộn nhất ở lúc ấy + tre)
            dau, song = sorted(x for x in os.listdir(d) if x.startswith("dau_")), ngoai.poll() is None
        finally:   # bộ chạy tự kiểm cũng dọn tiến trình CỦA NÓ ở mọi đường ra
            ngoai.kill(), ngoai.wait()
        kq = (rc, nhan, sorted(x for x in txt.splitlines() if x.startswith("DA_CHAY ")), "KHONG KHANG DINH" if ghi_dau else dau, song)
        return (kq, f"dau cua chau tu roi nhom SAU buoc don = {dau}") if ghi_dau else kq
    with tempfile.TemporaryDirectory(prefix="wp1463-chay-") as tam:
        kq.append(("ab_rc0_doi_chung", (0, "KET_LUAN_AB: DAT", "9/9"), ab(None, tam)))
        kq += [(f"ab_rc42_{ten}_{che}", (1, "KET_LUAN_AB: DO", "9/9"), ab((ten, che))) for ten, che in LUOT_AB]
        kq.append(("registry_tu_rc0_doi_chung", 0, reg(tam)))
        with open(os.path.join(tam, "H.nhe.rc"), "w", encoding="utf-8") as f:
            f.write("42\n")
        kq.append(("registry_tu_rc42_luot_nhe", 1, reg(tam)))
        with open(os.path.join(tam, "qs.py"), "w", encoding="utf-8") as f:
            f.write(MA_QS)
        day_du, hai_dau, ngat, han, het = ["DA_CHAY chau", "DA_CHAY con"], ["dau_chau", "dau_con"], ("goc_thoat", "chau_ngat", "chau_li"), ("TimeoutExpired",), ("DON KHONG HET",)
        kq.append(("quan_sat_khoe_doi_chung", (0, (), day_du, hai_dau, True), qs(tam, 0.0, 60)))
        kq.append(("quan_sat_qua_han_con_va_chau_khong_de_dau", (None, han, day_du, [], True), qs(tam, 3.0, 2.0)))
        # R16-2: cha bị NGẮT lúc đang chờ, con gốc ĐÃ thoát, hai cháu cùng nhóm hẹn ghi dấu (một cháu bỏ qua TERM) ⇒ ngắt được ném lại, trong trần, không dấu nào
        kq.append(("quan_sat_ngat_goc_da_thoat_chau_bo_qua_TERM_khong_de_dau", ("KeyboardInterrupt", ("trong tran",), [], [], True), qs(tam, 2.0, 60, ngat, 1.0)))
        kq.append(("quan_sat_ngat_lan_nua_giua_luc_don_van_don_het", ("KeyboardInterrupt", ("trong tran",), [], [], True), qs(tam, 2.0, 60, ngat, 1.0, gia="ngat")))
        kq.append(("quan_sat_tra_binh_thuong_chau_cung_nhom_da_dong_ong_khong_de_dau", (0, (), ["DA_CHAY goc_thoat"], [], True), qs(tam, 1.0, 60, ("goc_thoat", "chau_dong"))))
        # nhánh `DON KHONG HET` ⇒ không đo được: (i) không xác nhận được nhóm đã hết; (ii) con gốc bị thu hồi ở nơi khác ⇒ KHÔNG bắn tín hiệu (cháu còn sống ghi được dấu)
        kq.append(("quan_sat_khong_xac_nhan_duoc_nhom_da_het_la_khong_do_duoc", (None, het, day_du, hai_dau, True), qs(tam, 0.0, 60, tran=0.4, gia="mu")))
        kq.append(("quan_sat_mat_ghim_khong_ban_tin_hieu_va_khong_do_duoc", (None, het, ["DA_CHAY goc_thoat"], ["dau_chau_dong"], True), qs(tam, 1.0, 60, ("goc_thoat", "chau_dong"), 0.4, bo_chld=True)))
        # R16-3 (bảo đảm GIẢM): cháu TỰ `setsid` còn giữ ống ⇒ `DON KHONG HET`, không đo được; ca CHỈ GHI giới hạn (dấu của cháu ấy), KHÔNG khẳng định dọn được
        kq.append(("quan_sat_chau_tu_setsid_giu_ong_DON_KHONG_HET_chi_ghi_gioi_han", (None, han + het, ["DA_CHAY chau_tach", "DA_CHAY goc_thoat"], "KHONG KHANG DINH", True),
                   *qs(tam, 2.5, 1.0, ("goc_thoat", "chau_tach"), 0.6, ghi_dau=True)))
    return kq

_GOI_DON = "don_nhom(p, buf, eof, het_don, tran_don)"
_DON = "sach, mo_ta = ¦" + _GOI_DON
DOT_BIEN_CHAY = [(f"ab_bo_chot_rc_luot_{ten}_{che}", "hong = [k for k, v in rc_luot ¦if v != 0]", f'hong = [k for k, v in rc_luot if v != 0 and k != "{ten}/{che}"]',
                  f"ab_rc42_{ten}_{che}") for ten, che in LUOT_AB] + [
    ("registry_tu_mac_dinh_rc_0", "ra[che] = (¦int(g.read()), f.read())", "ra[che] = (0, f.read())", "registry_tu_rc42_luot_nhe"),
    ("quan_sat_bo_buoc_don", _DON, 'sach, mo_ta = True, "khong don"', "quan_sat_qua_han_con_va_chau_khong_de_dau"),
    ("quan_sat_chi_ket_thuc_con_khong_ket_thuc_nhom", "os.killpg(¦p.pid, th)", "p.send_signal(th)", "quan_sat_qua_han_con_va_chau_khong_de_dau"),
    # SPEC r16 R16-2: mỗi đường ra đều dọn (ngắt · trả bình thường · ngắt lần nữa giữa lúc dọn), có bước KILL, mất ghim thì không bắn, dọn không hết thì không đo được
    ("quan_sat_bo_don_o_duong_ngat", _DON, f'sach, mo_ta = (True, "khong don") if isinstance(loi, KeyboardInterrupt) else {_GOI_DON}', "quan_sat_ngat_goc_da_thoat_chau_bo_qua_TERM_khong_de_dau"),
    ("quan_sat_bo_buoc_KILL", "for th, han in ((signal.SIGTERM, het - tran / 2), ¦(signal.SIGKILL, het)) if ghim else ():", "for th, han in ((signal.SIGTERM, het - tran / 2),) if ghim else ():",
     "quan_sat_ngat_goc_da_thoat_chau_bo_qua_TERM_khong_de_dau"),
    ("quan_sat_bo_don_tiep_khi_bi_ngat_lan_nua", "loi = e ¦if loi is None or isinstance(loi, subprocess.TimeoutExpired) else loi", "raise", "quan_sat_ngat_lan_nua_giua_luc_don_van_don_het"),
    ("quan_sat_bo_don_o_duong_tra_binh_thuong", _DON, f'sach, mo_ta = (True, "khong don") if loi is None else {_GOI_DON}', "quan_sat_tra_binh_thuong_chau_cung_nhom_da_dong_ong_khong_de_dau"),
    ("quan_sat_bo_nhanh_DON_KHONG_HET", "if loi is not None ¦or not sach:", "if loi is not None:", "quan_sat_khong_xac_nhan_duoc_nhom_da_het_la_khong_do_duoc"),
    ("quan_sat_ban_tin_hieu_khi_mat_ghim", "ghim = goc_da_thoat(p.pid) ¦is not False and signal.getsignal(signal.SIGCHLD) != signal.SIG_IGN", "ghim = True", "quan_sat_mat_ghim_khong_ban_tin_hieu_va_khong_do_duoc")]

def lenh_tu_kiem(root, dot_bien):
    bo = nap_tep(os.path.join(root, K), "cpt_tu_kiem")
    so, vung, chay = tu_kiem_so(bo), tu_kiem_vung(), tu_kiem_chay(bo, root)
    so_sai = [(t, sorted(k), sorted(p for p in PHEP_SO if v.get(p) is not True)) for t, k, v in so if {p for p in PHEP_SO if v.get(p) is not True} != k or set(v) != set(PHEP_SO)]
    vung_sai = [x for x in vung + chay if x[1] != x[2]]
    for t, k, v in so:
        print(f"SO {t}: khai sai {sorted(k)} · vec-to {''.join('1' if v.get(p) is True else '0' for p in PHEP_SO)}")
    thieu = [p for p in PHEP_SO if not any(p in k for _, k, _ in so)]
    for x in so_sai + vung_sai:
        print(f"LECH: {x}")
    print(f"TU_KIEM_SO: {len(so) - len(so_sai)}/{len(so)} dat · moi phep co dau vao am: {not thieu}")
    print(f"TU_KIEM_VUNG: {sum(x[1] == x[2] for x in vung)}/{len(vung)} dat")
    for x in chay:
        print(f"CHAY {x[0]}: mong {x[1]} · duoc {x[2]}" + "".join(f" · GHI GIOI HAN (khong khang dinh): {g}" for g in x[3:]))
    print(f"TU_KIEM_CHAY: {sum(x[1] == x[2] for x in chay)}/{len(chay)} dat")
    print(GIOI_HAN_QUAN_SAT)
    ok, bat = not (so_sai or vung_sai or thieu), 0
    if dot_bien and ok:
        with open(os.path.abspath(__file__), encoding="utf-8") as f:
            src = f.read()
        sys.dont_write_bytecode = True
        with tempfile.TemporaryDirectory(prefix="wp1463-db-") as tam:
            for nhom, ds in (("SO", DOT_BIEN_SO), ("VUNG", DOT_BIEN_VUNG), ("CHAY", DOT_BIEN_CHAY)):
                for ten, cu, moi, dich in ds:
                    cu = _n(cu)
                    if src.count(cu) != 1:
                        print(f"DB_{nhom} {ten}: HONG — neo thay {src.count(cu)} lan")
                        continue
                    duong = os.path.join(tam, f"db_{ten}.py")
                    with open(duong, "w", encoding="utf-8") as f:
                        f.write(src.replace(cu, moi))
                    m = nap_tep(duong, f"do_pr2_db_{ten}")
                    if nhom == "SO":   # chỉ tính là BẮT khi véc-tơ lệch véc-tơ khai ĐÚNG ở phép bị gỡ/bị đổi
                        lech = [(t, p, p not in k, v.get(p) is True) for t, k, v in m.tu_kiem_so(bo) for p in dich if (v.get(p) is True) != (p not in k)]
                        mo_ta = "; ".join(f"{t}: {p} {'DUNG' if truoc else 'SAI'}→{'DUNG' if sau else 'SAI'}" for t, p, truoc, sau in lech[:4])
                    else:      # phải đổi kết quả ở ĐÚNG đầu vào tương ứng
                        lech = [x for x in (m.tu_kiem_vung() if nhom == "VUNG" else m.tu_kiem_chay(bo, root)) if x[1] != x[2] and x[0] == dich]
                        mo_ta = "; ".join(f"{x[0]}: mong {x[1]} duoc {x[2]}" for x in lech)
                    bat += bool(lech)
                    print(f"DB_{nhom} {ten}: {'BAT' if lech else 'SONG'} · {mo_ta}")
        tong = len(DOT_BIEN_SO) + len(DOT_BIEN_VUNG) + len(DOT_BIEN_CHAY)
        print(f"DOT_BIEN_TU_KIEM: {bat}/{tong} bi bat dung cho ({len(DOT_BIEN_SO)} cua bo so, {len(DOT_BIEN_VUNG)} cua phep do vung, {len(DOT_BIEN_CHAY)} cua bo chay)")
        ok = bat == tong
    print(f"KET_LUAN_TU_KIEM: {'DAT' if ok else 'DO'}")
    return 0 if ok else 1

def main(argv):
    lenh = argv[1] if len(argv) > 1 else ""
    root = os.path.abspath(argv[argv.index("--root") + 1] if "--root" in argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), *[os.pardir] * 4))
    luu = argv[argv.index("--luu") + 1] if "--luu" in argv else None
    if lenh == "vung":
        return lenh_vung(root, luu)
    if lenh == "ab" and len(argv) > 2:
        return lenh_ab(root, argv[2], luu)
    if lenh == "registry":
        return lenh_registry(root, argv[argv.index("--tu") + 1] if "--tu" in argv else None)
    if lenh == "tu-kiem":
        return lenh_tu_kiem(root, "--dot-bien" in argv)
    print(__doc__)
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
