#!/usr/bin/env python3
"""wp1463 (PR2) — bằng chứng đo trước merge của SPEC r11: `ab` · `registry` · `vung` · `tu-kiem [--dot-bien]`.

  python3 -B ops/specs/wp1463-r1/do/do_pr2.py vung [--root KHO]           Nghiệm thu 4 (rc 0 SACH · 4 NGOAI_VUNG · 3 KHONG_DO_DUOC)
  python3 -B ops/specs/wp1463-r1/do/do_pr2.py ab <SHA_BASE> [--root KHO]  Nghiệm thu 2 + 5 (hai clone dựng trong MỘT lệnh)
  python3 -B ops/specs/wp1463-r1/do/do_pr2.py registry [--root KHO]       Nghiệm thu 3
  python3 -B ops/specs/wp1463-r1/do/do_pr2.py tu-kiem [--dot-bien]        tự kiểm bộ so và phép đo vùng (không cần cây git)

KHÔNG phải `*_test.py`, không đăng ký vào registry. Hook và probe của `vung` được GHI RA thư mục tạm ngoài kho rồi nạp
qua PYTHONPATH (tệp này được theo dõi; chạy probe từ chính nó sẽ đưa nó vào tập quan sát của probe).
Giới hạn của `vung`, khai thẳng (SPEC r14 "Bảo đảm giảm"): tiến trình KHÔNG phải Python, Python gọi qua shell, lần đọc
không phát sự kiện audit `open`, và Python con không hook bị che bởi dòng khởi động thừa đều KHÔNG bị quan sát.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

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
    ("khong_do_duoc", None, "day_du"), ("rong", [], "nhe"), ("bo", ["ops/ci_provenance_test.py"], "day_du"),
    ("dich", ["ops/ci_provenance.py"], "day_du"), ("ci_yml", [_W + "ci.yml"], "day_du"),
    ("requirements", ["requirements.txt"], "day_du"), ("bo_chon", [".claude/dev/ci_dang_ky_test.py"], "day_du"),
    ("wf_wd", [_W + "ops-do-workflow-definition.yml"], "day_du"), ("bash_nen", ["ops/bash_nen.py"], "day_du"),
    ("wf_dot_bien_du", [_W + "ci-dot-bien-du.yml"], "day_du"), ("wf_launcher", [_W + "launcher-windows.yml"], "day_du"),
    ("cai_cong_cu", ["ops/cai_cong_cu.sh"], "day_du"), ("cong_cu_yaml", ["ops/cong_cu.yaml"], "day_du"),
    ("goc_la", ["pyproject.toml"], "day_du"), ("goc_ten_bo", ["ci_provenance.py"], "day_du"),
    ("goc_tai_lieu", ["README.md", "CLAUDE.md", "CHANGELOG.md"], "nhe"), ("tai_lieu", ["docs/x.md"], "nhe"),
    ("spec_ho_so", ["ops/specs/wp1463-r1/SPEC.md", "ops/land/x.yaml"], "nhe"),
    ("ops_khac", ["ops/ci_duong_nhanh.py", "ops/cong_cu_test.py"], "day_du"),
    ("ops_khac_nhe", ["ops/ci_duong_nhanh.py", "ops/nhanh_don_duoc_test.py"], "nhe"),
    ("gan_dung_hau_to", ["ops/ci_provenance.pyi", "ops/ci_provenance_test.py.bak", "ops/bash_nen.py~"], "nhe"),
    ("gan_dung_thu_muc", ["x/ops/ci_provenance.py", "ops/ci_provenance/x.py", ".claude/dev/ci_dang_ky_test.pyc"], "nhe"),
    ("gan_dung_workflow", [_W + "ci-dot-bien-du.yml.bak", _W + "launcher-windows.yaml", "x/" + _W + "ci-dot-bien-du.yml",
                           ".github/launcher-windows.yml"], "nhe"),
    ("workflow_khac", [_W + "khac.yml", _W + "ops-publish-lease.yml"], "nhe"),
    ("dev_khac", [".claude/dev/packet_loop.py", ".claude/settings.json"], "nhe"),
    ("hon_hop", ["docs/x.md", "ops/bash_nen.py"], "day_du"), ("hon_hop_workflow", ["docs/x.md", _W + "launcher-windows.yml"], "day_du"),
    ("hop_dong_schema", [_H + "hop_dong/bien_nhan_audit.v1.schema.json"], "day_du"),
    ("hop_dong_fixture", [_H + "hop_dong/fixture.json"], "day_du"),
    ("hop_dong_gan_dung", [_H + "hop_dong/khac.json", _H + "fixture.json", _H + "hop_dong/fixture.json.bak"], "nhe"))
BAM_BANG = "0aba13e7b73bee2a09d4a5aac541dfba76dbe4497edde2d77a938ac04a375e58"


def bam_bang(bang=BANG):
    return hashlib.sha256("".join(f"{n}\t{json.dumps(d)}\t{e}\n" for n, d, e in bang).encode()).hexdigest()


# ====================================================================== vung (Nghiệm thu 4)
SACH, NGOAI, KDD = "SACH", "NGOAI_VUNG", "KHONG_DO_DUOC"
MA_VUNG = {SACH: 0, NGOAI: 4, KDD: 3}
PHEP = ("bo_day_du", "phan_chung_nguyen", "phan_chung_go_bon_khoa")   # tập ĐÓNG, mỗi tên đúng MỘT lần
CHE_DO_PROBE = {"phan_chung_nguyen": "nguyen", "phan_chung_go_bon_khoa": "go_bon_khoa"}
NHAN_CHUNG = {"bo_day_du": "ops/ci_provenance.py", "phan_chung_nguyen": ".github/workflows/ci.yml",
              "phan_chung_go_bon_khoa": ".github/workflows/ci.yml"}
CO = {"NHE": True, "MAU_DAY_DU": True, "MAU_NHE": True, "VUNG_THEM": True, "so_vung_them": 7}
VANG = {"NHE": False, "MAU_DAY_DU": False, "MAU_NHE": False, "VUNG_THEM": False, "so_vung_them": 0}
DAU_VET = {"nguyen": (CO, CO), "go_bon_khoa": (CO, VANG)}   # (trước, sau) của bản nạp ngay trước `phan_chung()`
_RE_PY = re.compile(r"python[0-9.]*(\.exe)?$")

# Hook cho MỌI tiến trình Python thừa kế PYTHONPATH. Mỗi dòng nhật ký: JSON [pid, ppid, kiểu, dữ liệu]. Kiểu: BAT_DAU
# (dữ liệu = [starttime, sys.orig_argv]) · MO/THAT (đường dẫn theo chữ / sau realpath) · DIRFD (os.open tên tương đối
# với dir_fd, giải theo /proc/self/fd/<fd>) · DIRFD_KHONG_GIAI · SINH (argv của tiến trình con sắp tạo; pid = tiến trình sinh).
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
    def _hook(ev, args):
        if getattr(_tl, "trong", False):
            return
        _tl.trong = True
        try:
            if ev == "open" and args and isinstance(args[0], (str, bytes)) and not getattr(_tl, "dirfd", False):
                _ghi_duong("MO", os.path.abspath(os.fsdecode(args[0])))
            elif ev == "subprocess.Popen":
                _ghi("SINH", {"exe": os.fsdecode(args[0]) if args[0] else None, "argv": _argv(args[1])})
            elif ev in ("os.posix_spawn", "os.exec"):
                _ghi("SINH", {"exe": os.fsdecode(args[0]), "argv": _argv(args[1])})
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
def dau_vet():
    d = {t: K in getattr(m, t) for t in BON}
    d["so_vung_them"] = len(m.VUNG_THEM.get(K, ()))
    return d
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
    for x in (sinh.get("exe"), (sinh.get("argv") or [None])[0]):
        if x and (_RE_PY.search(os.path.basename(x)) or os.path.realpath(x) == os.path.realpath(sys.executable)):
            return True
    return False


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
    dk1 = bool(tap)
    dk2 = NHAN_CHUNG[ten] in tap
    return dk1, dk2, sorted(x for x in tap if oracle({x}) != "day_du")


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


def chay_quan_sat(cmd, cwd, log, tam, timeout=7200):
    env = dict(os.environ)
    env.pop("CI_PROVENANCE_KHONG_DOT_BIEN", None)
    env["PYTHONPATH"] = tam + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    env.update(WP1463_VUNG_LOG=log, PYTHONDONTWRITEBYTECODE="1")
    open(log, "w").close()
    try:
        p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = p.communicate(timeout=timeout)
        return p.pid, p.returncode, out.decode("utf-8", "replace")
    except Exception as e:   # không chạy được / quá hạn ⇒ không đo được
        return None, None, f"LOI_CHAY: {type(e).__name__}: {e}"


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
        print(f"PHEP {c['ten']}: {c['ket_luan']} · rc={o.get('rc')} · (1) khac rong={dk1} · (2) nhan chung {NHAN_CHUNG[c['ten']]}={dk2}"
              f" · (3) ngoai vung={c['ngoai_vung']} · Python con/dong khoi dong={o.get('python_con')}/{o.get('bat_dau_con')}")
        print(f"  tap ({len(c['tap'])}): {c['tap']}")
        if c["ten"] == "bo_day_du":
            print(f"  khoi cuoi: {o.get('khoi_cuoi')}")
        else:
            k = o.get("ket") or {}
            print(f"  danh tinh: che_do={k.get('che_do')} truoc={k.get('truoc')} sau={k.get('sau')} phan_chung={k.get('phan_chung')}"
                  f" hang={len(k.get('hang') or ())}/{len(BANG)}")
        for x in c["ly_do"]:
            print(f"  KHONG DO DUOC: {x}")
    for c in ct[len(obs):]:
        print(f"PHEP {c['ten']}: {c['ket_luan']} · {c['ly_do']}")
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


def _goc_kho(argv):
    if "--root" in argv:
        return os.path.abspath(argv[argv.index("--root") + 1])
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[os.pardir] * 4))


def main(argv):
    lenh = argv[1] if len(argv) > 1 else ""
    if lenh == "vung":
        luu = argv[argv.index("--luu") + 1] if "--luu" in argv else None
        return lenh_vung(_goc_kho(argv), luu)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
