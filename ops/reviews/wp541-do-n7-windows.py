# -*- coding: utf-8 -*-
"""WP541 - PHEP DO N7 TREN WINDOWS THAT (ban 3: liet ke HET ca do).

Chay:  py wp541-do-n7-windows.py "<thu-muc-kho>" [sha-mong]

N7 - DON VI (luat L1, ba luot review da hoi):
  So dong trong ops/lease_publish.py khop DUNG chuoi  'if nen_thuc == "windows":'
  truoc = 1  => nhanh giai theo nen CON NGUYEN
  sau   = 0  => da tat nhanh Windows, ca dich PHAI do

FAIL-CLOSE: nen do sai => in KHONG_DO_DUOC, rc!=0, KHONG in ket luan nao.
Dot bien chay tren BAN SAO TAM; cay that khong bi dung toi.

Vi sao co ban 3: ban 2 loc ten ca bang r"(t\\d+)(_\\S*)" nen BO SOT moi ten dang
`t02b_...`, `t55a_...` (co chu cai truoc gach duoi) - dung 5 ca nhu the trong bo.
Ban 3 bat ten DAY DU `\\S+`, doi chieu HAI nguon doc lap, va con doi chieu voi
SO HOC tu dong tong ket. Lech => bao KHONG_DO_DUOC cho phan liet ke, khong im lang.
"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
for _l in (sys.stdout, sys.stderr):
    try: _l.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception: pass

def inn(*p):
    van = " ".join(str(x) for x in p)
    try: print(van)
    except Exception:
        try:
            sys.stdout.buffer.write(van.encode("utf-8", "replace") + b"\n"); sys.stdout.flush()
        except Exception:
            print(van.encode("ascii", "backslashreplace").decode("ascii"))

SHA_MONG = sys.argv[2] if len(sys.argv) > 2 else "2f708690"
MAU = 'if nen_thuc == "windows":'
CA15 = "t129 t130 t131 t132 t133 t136 t138 t139 t144 t145 t146 t147 t149 t150 t151".split()
CAMOI = "t165 t166 t167 t168".split()

# --- Doc log cua bo test. Ten ca la \S+ DAY DU, khong gia dinh dang so. ---
# runner in:  ">>> vao <ten> <utc>" / "<<< ra <ten> <giay>s QUA|DO|BO_QUA"
#             "!!! do <ten> <ly do>"            (ngay tai cho, ASCII thuan)
#             "  DO  <ten>: <ly do>"            (cuoi bo, chu DO co dau)
#             "  BO QUA <ten>: <ly do>"         (cuoi bo, chu BO co dau)
RX_RA      = re.compile(r"(?m)^<<< ra (\S+) [0-9.]+s (\w+)\s*$")
RX_DO_CHO  = re.compile(r"(?m)^!!! do (\S+) (.*)$")
# Tien to co dau: khoan dung cho ca khi console lam hong byte -> \S{1,4} + DUNG hai khoang trang.
# Dong "BO QUA" chi co MOT khoang trang sau tu dau nen khong lot vao day.
RX_DO_CUOI = re.compile(r"(?m)^ {2}(\S{1,4}) {2}(\S+): (.*)$")
RX_BO_QUA  = re.compile(r"(?m)^ {2}\S{1,6} QUA (\S+): (.*)$")
RX_TONG    = re.compile(r"lease_publish: (\d+)/(\d+)\b[^\n]*?=(\d+),[^\n]*?=(\d+)")

# Lop loi: moi lop mot cach chua KHAC NHAU - dung gop.
LOP = [
    ("PATH-TOI-THIEU", re.compile(r"PATH t[ốo]i thi[ểe]u|/usr/bin")),
    ("QUYEN-SYMLINK",  re.compile(r"WinError 1314|required privilege")),
    ("QUYEN-TRUY-CAP", re.compile(r"WinError 5\b|Access is denied")),
    ("KHONG-PHAI-EXE", re.compile(r"WinError 193|not a valid Win32")),
    ("THIEU-CONG-CU",  re.compile(r"KH[ÔO]NG [ĐD]O [ĐD][ƯU][ỢO]C: thi[ếe]u")),
    ("UTF8-POLICY",    re.compile(r"kh[ôo]ng ph[ảa]i UTF-8")),
]
def lop_cua(ly):
    for ten, rx in LOP:
        if rx.search(ly): return ten
    return "KHAC"

def so_ca(ten):
    """Khoa so de sap xep; giu ten day du lam danh tinh."""
    m = re.match(r"t(\d+)", ten)
    return (int(m.group(1)) if m else 10**6, ten)

def doc_do(out):
    """HET ca do, doc HAI nguon doc lap roi doi chieu voi so hoc.

    Tra (ly_do_theo_ten, ghi_chu_doi_chieu, dat_tin_cay).
    """
    tai_cho = {t: ly.strip() for t, ly in RX_DO_CHO.findall(out)}
    bo = {t for t, _ in RX_BO_QUA.findall(out)}
    cuoi = {t: ly.strip() for _, t, ly in RX_DO_CUOI.findall(out) if t not in bo}
    hop = dict(cuoi); hop.update(tai_cho)      # tai_cho la nguon ASCII, uu tien
    for t in cuoi:
        hop.setdefault(t, cuoi[t])
    ghi_chu, tin = [], True
    if set(tai_cho) != set(cuoi):
        ghi_chu.append(f"hai nguon LECH: chi-tai-cho={sorted(set(tai_cho)-set(cuoi))} "
                       f"chi-cuoi-bo={sorted(set(cuoi)-set(tai_cho))}")
        tin = False
    m = RX_TONG.search(out)
    if not m:
        ghi_chu.append("KHONG doc duoc dong tong ket -> khong doi chieu duoc so hoc"); tin = False
    else:
        dat, tren = int(m.group(1)), int(m.group(2))
        do_theo_so_hoc = tren - dat
        ghi_chu.append(f"so hoc: {tren}-{dat}={do_theo_so_hoc} do; doc duoc {len(hop)}")
        if do_theo_so_hoc != len(hop):
            ghi_chu.append(f"LECH SO HOC: thieu {do_theo_so_hoc - len(hop)} ca -> danh sach KHONG day du")
            tin = False
    return hop, ghi_chu, tin

so = {}
def ghi(k, v): so[k] = v; return v

def chay(argv, cwd, phut=45):
    mt = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable] + argv, cwd=str(cwd), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=phut*60, env=mt)
    return p.returncode, (p.stdout or "") + (p.stderr or "")

def mau_ca(out, t):
    """Trang thai cua ca co tien to so `t`. Bien gioi `_` de t15 khong nuot t150."""
    m = re.search(r"(?m)^<<< ra (" + t + r"[a-z]?_\S*) [0-9.]+s (\w+)\s*$", out)
    return m.group(2) if m else None

def ten_day_du(out, t):
    m = re.search(r"(?m)^<<< ra (" + t + r"[a-z]?_\S*) ", out)
    return m.group(1) if m else None

# ---------- TU KIEM BO DOC (chay trong moi luot, tren mau co san) ----------
_MAU = (
    ">>> vao t02b_ten_KHONG_CO_THAM_QUYEN_bi_CHAN 2026-09-18T00:00:00Z\n"
    "<<< ra t02b_ten_KHONG_CO_THAM_QUYEN_bi_CHAN 0.010s DO\n"
    "!!! do t02b_ten_KHONG_CO_THAM_QUYEN_bi_CHAN loi gia dinh A\n"
    ">>> vao t150_review2_F10_nguon_khong_utf8 2026-09-18T00:00:01Z\n"
    "<<< ra t150_review2_F10_nguon_khong_utf8 0.020s DO\n"
    "!!! do t150_review2_F10_nguon_khong_utf8 Traceback WinError 1314 required privilege\n"
    ">>> vao t131_S8_tam_tran 2026-09-18T00:00:02Z\n"
    "<<< ra t131_S8_tam_tran 0.030s BO_QUA\n"
    "  BỎ QUA t131_S8_tam_tran: nen fixture\n"
    "  ĐỎ  t02b_ten_KHONG_CO_THAM_QUYEN_bi_CHAN: loi gia dinh A\n"
    "  ĐỎ  t150_review2_F10_nguon_khong_utf8: Traceback WinError 1314 required privilege\n"
    "lease_publish: 1/3 đạt; đã chạy=3, bỏ qua=1\n"
)
def tu_kiem():
    do, gc, tin = doc_do(_MAU)
    kiem = [
        ("bat du 2 ca do", len(do) == 2),
        ("bat ten co chu cai (t02b)", any(t.startswith("t02b") for t in do)),
        ("KHONG dem ca BO QUA la do", not any(t.startswith("t131") for t in do)),
        ("doi chieu so hoc DAT", tin),
        ("lop loi QUYEN-SYMLINK", lop_cua(do[[t for t in do if t.startswith('t150')][0]]) == "QUYEN-SYMLINK"),
        ("mau_ca doc dung", mau_ca(_MAU, "t150") == "DO"),
        ("t15 KHONG nuot t150", mau_ca(_MAU, "t15") is None),
        ("bo qua doc dung", [t for t, _ in RX_BO_QUA.findall(_MAU)] == ["t131_S8_tam_tran"]),
    ]
    return kiem

inn("=" * 78); inn("WP541 - do N7 tren Windows that (ban 3: liet ke HET ca do)"); inn("=" * 78)
inn("Tu kiem bo doc log:")
_hong = [t for t, k in tu_kiem() if not k]
for t, k in tu_kiem(): inn(f"   [{'DAT ' if k else 'TRUOT'}] {t}")
if _hong:
    inn(""); inn("KHONG_DO_DUOC: bo doc log cua chinh script nay sai -> khong do gi ca.")
    sys.exit(3)

# ---------- 0. NEN DO ----------
goc = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
if not (goc / "ops" / "lease_publish.py").is_file():
    g2 = Path(__file__).resolve().parent
    for ung in (g2, g2.parent, g2.parent.parent):
        if (ung / "ops" / "lease_publish.py").is_file(): goc = ung; break
tep = goc / "ops" / "lease_publish.py"

loi = []
inn(""); inn("sys.platform  :", sys.platform)
inn("python        :", sys.version.split()[0])
inn("os.pathsep    :", repr(os.pathsep))
inn("PATHEXT       :", repr(os.environ.get("PATHEXT")))
inn("ProgramFiles  :", repr(os.environ.get("ProgramFiles")))
inn("SystemRoot    :", repr(os.environ.get("SystemRoot")))
inn("CONG_CU_GIT   :", repr(os.environ.get("CONG_CU_GIT")))
inn("goc kho       :", goc)

# --- Quyen: DO THANG, khong hoi registry roi doan ---
quyen_admin = None
if sys.platform == "win32":
    try:
        import ctypes
        quyen_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        quyen_admin = None
ghi("quyen_admin", quyen_admin)
inn("chay voi quyen Administrator :", quyen_admin)

symlink_duoc = None
try:
    with tempfile.TemporaryDirectory() as t:
        dich = Path(t) / "dich.txt"; dich.write_text("x", encoding="utf-8")
        try:
            os.symlink(str(dich), str(Path(t) / "lk"))
            symlink_duoc = True
        except OSError as e:
            symlink_duoc = False
            ghi("symlink_loi", f"{type(e).__name__}: {e}")
except Exception as e:
    ghi("symlink_loi", f"{type(e).__name__}: {e}")
ghi("symlink_duoc", symlink_duoc)
inn("tao symlink duoc            :", symlink_duoc,
    "" if symlink_duoc else f"  ({so.get('symlink_loi','')[:70]})")

git_that = shutil.which("git")
inn("which('git')  :", repr(git_that))
if sys.platform != "win32": loi.append(f"KHONG phai Windows (sys.platform={sys.platform!r})")
if not tep.is_file():      loi.append(f"khong thay {tep}")
if not git_that:           loi.append("khong co `git` trong PATH thuong")
rc, o = chay(["-c", "import subprocess;print(subprocess.run(['git','rev-parse','--short','HEAD'],"
                    "capture_output=True,text=True).stdout.strip())"], goc, 5)
head = (o.strip().splitlines() or ["?"])[-1]
inn("HEAD          :", head, f"(mong {SHA_MONG})")
if not head.startswith(SHA_MONG[:7]): loi.append(f"HEAD={head} khac {SHA_MONG}")

if loi:
    inn(""); inn("KHONG_DO_DUOC: nen do sai, KHONG in ket luan nao.")
    for x in loi: inn("  -", x)
    sys.exit(3)
inn("nen do: DAT")

# ---------- 1. TRUOC ----------
truoc = tep.read_text(encoding="utf-8").count(MAU)
inn(""); inn("-" * 78)
inn("N7 - DON VI: so dong khop chuoi", repr(MAU))
inn(f"  TRUOC (chua dot bien) = {ghi('n7_truoc', truoc)}   [mong 1]")
if truoc != 1:
    inn("KHONG_DO_DUOC: mau dot bien khong xuat hien dung 1 lan."); sys.exit(3)

# ---------- 2. BO TEST DAY DU ----------
inn(""); inn("-" * 78)
inn("Chay bo test day du tren ban va (10-30 phut)...")
rc_nen, out_nen = chay(["ops/lease_publish_test.py"], goc)
inn("  rc =", ghi("rc_ban_va", rc_nen))
m = RX_TONG.search(out_nen)
inn("  tong ket:", m.group(0) if m else "(KHONG doc duoc)")
if m:
    ghi("dat", int(m.group(1))); ghi("tren", int(m.group(2)))
    ghi("da_chay", int(m.group(3))); ghi("bo_qua_so", int(m.group(4)))

do_het, ghi_chu, tin_cay = doc_do(out_nen)
ghi("so_ca_do", len(do_het)); ghi("liet_ke_day_du", tin_cay)
inn(""); inn("  --- doi chieu bo doc ---")
for g in ghi_chu: inn("   *", g)
if not tin_cay:
    inn("   !! KHONG DO DUOC (day du): danh sach duoi day CO THE THIEU. Dan ca log tho ve.")

inn(""); inn(f"  === {len(do_het)} CA DO doc duoc, phan loai theo LOP LOI ===")
theo_lop = {}
for t in sorted(do_het, key=so_ca):
    theo_lop.setdefault(lop_cua(do_het[t]), []).append(t)
for lp in sorted(theo_lop):
    inn(f"   [{lp}] ({len(theo_lop[lp])}) {[x.split('_')[0] for x in theo_lop[lp]]}")
inn("")
for t in sorted(do_het, key=so_ca):
    inn(f"   {t.split('_')[0]:7} [{lop_cua(do_het[t]):14}] {t}")
    inn(f"           {do_het[t][:160]}")
ghi("do_theo_lop", theo_lop)
ghi("do_ly_do", {t: do_het[t][:300] for t in do_het})

bq = sorted({t for t, _ in RX_BO_QUA.findall(out_nen)}, key=so_ca)
ghi("ca_bo_qua", bq)
inn(""); inn(f"  ca BI BO QUA ({len(bq)}): {[x.split('_')[0] for x in bq]}")

inn(""); inn("  15 ca TUNG DO tren CI:")
b15 = {}
for t in CA15:
    tt = ten_day_du(out_nen, t); tr = mau_ca(out_nen, t); b15[t] = tr
    lp = f" [{lop_cua(do_het[tt])}]" if tt in do_het else ""
    inn(f"     {t}: {tr}{lp}")
ghi("ca15", b15)
inn(f"  => con DO: {[t for t in CA15 if b15[t] == 'DO']}")

inn(""); inn("  4 ca MOI (N1-N4 cua ban va):")
b4 = {t: mau_ca(out_nen, t) for t in CAMOI}; ghi("ca_moi", b4)
for t in CAMOI: inn(f"     {t}: {b4[t]}")

# ---------- 3. PROBE THUC TE ----------
inn(""); inn("-" * 78); inn("Probe thuc te (khong qua tham so tiem):")
sys.path.insert(0, str(goc))
import importlib.util
spec = importlib.util.spec_from_file_location("lp541", str(tep))
lp = importlib.util.module_from_spec(spec); spec.loader.exec_module(lp)
try:
    duong = lp._git_exe_toi_thieu()
    inn("  _git_exe_toi_thieu()         ->", repr(duong))
    ghi("giai_that", duong); ghi("giai_that_la_exe", bool(duong) and duong.lower().endswith(".exe"))
except Exception as e:
    inn("  _git_exe_toi_thieu() NEM     ->", type(e).__name__, str(e)[:150])
    ghi("giai_that", None); ghi("giai_that_la_exe", False)

with tempfile.TemporaryDirectory() as tmp:
    shim = Path(tmp)/"shim"; shim.mkdir()
    for n in ("git.bat","git.cmd","git.py"): (shim/n).write_text("@echo off\r\n", encoding="utf-8")
    cwdk = Path(tmp)/"cwd"; cwdk.mkdir(); pf = Path(tmp)/"pf"; pf.mkdir()
    kq = lp._git_windows(path=str(shim), program_files=str(pf), cwd=str(cwdk))
    inn("  shim-only o PATH ngoai cwd   ->", repr(kq), "(mong None)")
    ghi("tu_choi_shim", kq is None)
    (shim/"git.exe").write_text("x", encoding="utf-8")
    kq2 = lp._git_windows(path=str(shim), program_files=str(pf), cwd=str(cwdk))
    inn("  DOI CHUNG DUONG: them git.exe->", repr(kq2))
    ghi("doi_chung_duong", bool(kq2) and kq2.lower().endswith("git.exe"))

# ---------- 4. N7 ----------
inn(""); inn("-" * 78); inn("N7 - dot bien tren BAN SAO TAM (cay that KHONG bi dung toi)")
with tempfile.TemporaryDirectory() as tmp:
    sao = Path(tmp)/"cay"
    shutil.copytree(goc, sao, ignore=shutil.ignore_patterns(".git","__pycache__","*.pyc"))
    f2 = sao/"ops"/"lease_publish.py"
    f2.write_text(f2.read_text(encoding="utf-8").replace(MAU, "if False:"), encoding="utf-8")
    sau = f2.read_text(encoding="utf-8").count(MAU)
    inn(f"  SAU (da dot bien) = {ghi('n7_sau', sau)}   [mong 0]")
    if sau != 0: inn("KHONG_DO_DUOC: dot bien KHONG ap duoc."); sys.exit(3)
    rc_m, out_m = chay(["ops/lease_publish_test.py"], sao)
    m165 = mau_ca(out_m, "t165"); dm, _, _ = doc_do(out_m)
    t165 = ten_day_du(out_m, "t165")
    inn("  rc sau dot bien :", rc_m)
    inn("  t165 :", m165, "|", (dm.get(t165) or "")[:120])
    ghi("n7_t165_sau_dot_bien", m165); ghi("n7_dat", m165 == "DO")
    ghi("n7_t165_ly_do", (dm.get(t165) or "")[:200])

# ---------- KET LUAN ----------
inn(""); inn("=" * 78)
ok = (so.get("n7_truoc")==1 and so.get("n7_sau")==0 and so.get("n7_dat")
      and so.get("tu_choi_shim") and so.get("doi_chung_duong"))
inn("N7 (truoc=1, sau=0, t165 DO):", "DAT" if so.get("n7_dat") else "TRUOT")
inn("Tu choi shim o PATH that    :", "DAT" if so.get("tu_choi_shim") else "TRUOT")
inn("Doi chung duong             :", "DAT" if so.get("doi_chung_duong") else "TRUOT")
inn("Quyen symlink               :", so.get("symlink_duoc"), "| Administrator:", so.get("quyen_admin"))
inn("Tong ca do                  :", so.get("so_ca_do"), "->", {k: len(v) for k, v in theo_lop.items()})
inn("Danh sach do DAY DU         :", "CO" if tin_cay else "KHONG DO DUOC - xem doi chieu o tren")
inn(""); inn("--- DAN NGUYEN KHOI JSON NAY VE CHO REVIEWER ---")
inn(json.dumps(so, ensure_ascii=False, indent=1, default=str))
sys.exit(0 if ok else 1)
