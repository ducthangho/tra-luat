# -*- coding: utf-8 -*-
"""WP541 — PHEP DO N7 TREN WINDOWS THAT.  Chay:  py do_win_541.py

Tra loi cau ma ba luot review da hoi (luat L1): "truoc = 1, sau = 0" DEM GI.
  DON VI: so dong trong ops/lease_publish.py khop DUNG chuoi
          'if nen_thuc == "windows":'
  truoc = 1  => nhanh giai theo nen CON NGUYEN (ban va dang co hieu luc)
  sau   = 0  => da ap dot bien, nhanh Windows bi tat, ca dich PHAI do

FAIL-CLOSE: nen do sai => in KHONG_DO_DUOC, rc!=0, va KHONG in ket luan nao.
KHONG dung den cay lam viec that: moi dot bien chay tren BAN SAO TAM.
"""
import io, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

# Console may Viet la cp1258: in duong dan co dau se nem UnicodeEncodeError va
# GIET ca luot chay truoc khi logic kip sai. Ep UTF-8 cho CHINH ta va cho MOI tien
# trinh con, roi van boc them mot lop in an toan — hai lop, vi lop mot co the that bai.
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
for luong in (sys.stdout, sys.stderr):
    try: luong.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

def inn(*phan):
    """In khong bao gio nem. Duong dan co dau KHONG duoc giet phep do."""
    van = " ".join(str(x) for x in phan)
    try:
        print(van)
    except Exception:
        try:
            sys.stdout.buffer.write(van.encode("utf-8", "replace") + b"\n")
            sys.stdout.flush()
        except Exception:
            print(van.encode("ascii", "backslashreplace").decode("ascii"))

SHA_MONG = "2f708690"
MAU_DOT_BIEN = 'if nen_thuc == "windows":'
CA_15 = "t129 t130 t131 t132 t133 t136 t138 t139 t144 t145 t146 t147 t149 t150 t151".split()
CA_MOI = "t165 t166 t167 t168".split()

so = {}
def ghi(k, v): so[k] = v; return v

def chay(argv, cwd, phut=45):
    mt = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8",
              PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable] + argv, cwd=str(cwd),
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=phut * 60, env=mt)
    return p.returncode, (p.stdout or "") + (p.stderr or "")

def mau_ca(out, tien_to):
    """Tra 'QUA' / 'DO' / None cho ca bat dau bang tien_to."""
    m = re.search(r"<<< ra (" + tien_to + r"_\S*) [0-9.]+s (\w+)", out)
    return m.group(2) if m else None

def ly_do(out, tien_to):
    m = re.search(r"!!! do " + tien_to + r"_\S* (.*)", out)
    return m.group(1)[:200] if m else ""

inn("=" * 78)
inn("WP541 — do N7 tren Windows that")
inn("=" * 78)

# ---------- GIAI DOAN 0: NEN DO ----------
# Nhan thu muc kho lam doi so: py do_win_541.py "D:\\Quoc hoi\\tl546"
if len(sys.argv) > 1:
    goc = Path(sys.argv[1]).resolve()
else:
    goc = Path(__file__).resolve().parent
    if not (goc / "ops" / "lease_publish.py").is_file():
        goc = Path.cwd()
tep = goc / "ops" / "lease_publish.py"

loi_nen = []
inn("sys.platform          :", sys.platform)
inn("python                :", sys.version.split()[0])
inn("os.pathsep            :", repr(os.pathsep))
inn("PATHEXT               :", repr(os.environ.get("PATHEXT")))
inn("ProgramFiles          :", repr(os.environ.get("ProgramFiles")))
inn("SystemRoot            :", repr(os.environ.get("SystemRoot")))
inn("CONG_CU_GIT           :", repr(os.environ.get("CONG_CU_GIT")))
inn("goc kho               :", goc)

if sys.platform != "win32":
    loi_nen.append(f"KHONG phai Windows (sys.platform={sys.platform!r})")
if not tep.is_file():
    loi_nen.append(f"khong thay {tep}")
git_that = shutil.which("git")
inn("which('git')          :", repr(git_that))
if not git_that:
    loi_nen.append("khong co `git` trong PATH thuong — moi ket luan duoi se vo nghia")
rc, head = chay(["-c", "import subprocess;print(subprocess.run(['git','rev-parse','--short','HEAD'],"
                       "capture_output=True,text=True).stdout.strip())"], goc, 5)
head = head.strip().splitlines()[-1] if head.strip() else "?"
inn("HEAD                  :", head, f"(mong {SHA_MONG})")
if not head.startswith(SHA_MONG[:7]):
    loi_nen.append(f"HEAD={head} khac {SHA_MONG} — checkout sai nhanh?")

if loi_nen:
    inn()
    inn("KHONG_DO_DUOC: nen do sai, KHONG in ket luan nao.")
    for x in loi_nen: inn("  -", x)
    sys.exit(3)
inn("nen do: DAT")

# ---------- GIAI DOAN 1: dem TRUOC ----------
than = tep.read_text(encoding="utf-8")
truoc = than.count(MAU_DOT_BIEN)
inn()
inn("-" * 78)
inn("N7 — DON VI: so dong khop chuoi", repr(MAU_DOT_BIEN))
inn(f"  TRUOC (chua dot bien) = {ghi('n7_truoc', truoc)}   [mong 1]")
if truoc != 1:
    inn("KHONG_DO_DUOC: mau dot bien khong xuat hien dung 1 lan — ban va khac ban toi doc.")
    sys.exit(3)

# ---------- GIAI DOAN 2: bo test day du tren BAN VA ----------
inn()
inn("-" * 78)
inn("Chay bo test day du tren ban va (co the lau ~10-30 phut tren Windows)...")
rc_nen, out_nen = chay(["ops/lease_publish_test.py"], goc)
tong = re.search(r"lease_publish: (\d+)/(\d+) đạt; đã chạy=(\d+), bỏ qua=(\d+)", out_nen)
inn("  rc =", ghi("rc_ban_va", rc_nen))
inn("  tong ket:", tong.group(0) if tong else "(khong doc duoc dong tong ket)")
if tong:
    ghi("dat", int(tong.group(1))); ghi("tren", int(tong.group(2)))
    ghi("da_chay", int(tong.group(3))); ghi("bo_qua", int(tong.group(4)))

inn()
inn("  15 ca TUNG DO tren Windows (truoc ban va):")
bang15 = {}
for t in CA_15:
    m = mau_ca(out_nen, t); bang15[t] = m
    dau = "  " if m == "QUA" else ">>"
    inn(f"   {dau} {t}: {m or '(khong thay)'}" + (f"   {ly_do(out_nen, t)[:90]}" if m == "DO" else ""))
ghi("ca15", bang15)
con_do = [t for t, v in bang15.items() if v == "DO"]
inn(f"  => con DO: {con_do or 'khong con ca nao'}")

inn()
inn("  4 ca MOI cua ban va:")
bang4 = {}
for t in CA_MOI:
    m = mau_ca(out_nen, t); bang4[t] = m
    inn(f"     {t}: {m or '(khong thay)'}" + (f"   {ly_do(out_nen, t)[:90]}" if m == "DO" else ""))
ghi("ca_moi", bang4)

# ---------- GIAI DOAN 3: probe THUC TE ----------
inn()
inn("-" * 78)
inn("Probe thuc te (thu Windows that lam gi, khong qua tham so tiem):")
sys.path.insert(0, str(goc))
import importlib.util
spec = importlib.util.spec_from_file_location("lp541", str(tep))
lp = importlib.util.module_from_spec(spec); spec.loader.exec_module(lp)

try:
    duong = lp._git_exe_toi_thieu()
    inn("  _git_exe_toi_thieu()            ->", repr(duong))
    ghi("giai_that", duong)
    ghi("giai_that_la_exe", bool(duong) and duong.lower().endswith(".exe"))
except Exception as e:
    inn("  _git_exe_toi_thieu() NEM         ->", type(e).__name__, str(e)[:150])
    ghi("giai_that", None); ghi("giai_that_la_exe", False)

with tempfile.TemporaryDirectory() as tmp:
    shim = Path(tmp) / "shim"; shim.mkdir()
    for n in ("git.bat", "git.cmd", "git.py"):
        (shim / n).write_text("@echo off\r\n", encoding="utf-8")
    cwd_khac = Path(tmp) / "cwd"; cwd_khac.mkdir()
    pf_rong = Path(tmp) / "pf"; pf_rong.mkdir()
    kq = lp._git_windows(path=str(shim), program_files=str(pf_rong), cwd=str(cwd_khac))
    inn("  shim-only o PATH ngoai cwd      ->", repr(kq), "(mong None)")
    ghi("tu_choi_shim", kq is None)
    (shim / "git.exe").write_text("x", encoding="utf-8")
    kq2 = lp._git_windows(path=str(shim), program_files=str(pf_rong), cwd=str(cwd_khac))
    inn("  DOI CHUNG DUONG: them git.exe    ->", repr(kq2), "(mong tro vao git.exe)")
    ghi("doi_chung_duong", bool(kq2) and kq2.lower().endswith("git.exe"))

# ---------- GIAI DOAN 4: N7 tren BAN SAO TAM ----------
inn()
inn("-" * 78)
inn("N7 — ap dot bien tren BAN SAO TAM (cay that KHONG bi dung toi)")
with tempfile.TemporaryDirectory() as tmp:
    sao = Path(tmp) / "cay"
    shutil.copytree(goc, sao, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    f2 = sao / "ops" / "lease_publish.py"
    t2 = f2.read_text(encoding="utf-8")
    f2.write_text(t2.replace(MAU_DOT_BIEN, "if False:"), encoding="utf-8")
    sau = f2.read_text(encoding="utf-8").count(MAU_DOT_BIEN)
    inn(f"  SAU (da dot bien) = {ghi('n7_sau', sau)}   [mong 0]")
    if sau != 0:
        inn("KHONG_DO_DUOC: dot bien KHONG ap duoc.")
        sys.exit(3)
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    rc_m, out_m = chay(["ops/lease_publish_test.py"], sao)
    mau165 = mau_ca(out_m, "t165")
    inn("  rc sau dot bien :", rc_m)
    inn("  t165 :", mau165, "|", ly_do(out_m, "t165")[:110])
    ghi("n7_t165_sau_dot_bien", mau165)
    ghi("n7_dat", mau165 == "DO")

# ---------- KET LUAN ----------
inn()
inn("=" * 78)
ok = (so.get("n7_truoc") == 1 and so.get("n7_sau") == 0 and so.get("n7_dat")
      and so.get("tu_choi_shim") and so.get("doi_chung_duong"))
inn("N7 (truoc=1, sau=0, ca dich DO):", "DAT" if so.get("n7_dat") else "TRUOT")
inn("Tu choi shim o PATH that       :", "DAT" if so.get("tu_choi_shim") else "TRUOT")
inn("Doi chung duong (nhan git.exe) :", "DAT" if so.get("doi_chung_duong") else "TRUOT")
inn("15 ca tung do, nay con do      :", con_do or "khong con")
inn("4 ca moi                       :", bang4)
inn()
inn("--- DAN NGUYEN KHOI JSON NAY VE CHO REVIEWER ---")
inn(json.dumps(so, ensure_ascii=False, indent=1, default=str))
sys.exit(0 if ok else 1)
