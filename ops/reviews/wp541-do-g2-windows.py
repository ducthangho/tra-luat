# -*- coding: utf-8 -*-
"""WP541 g2 - PHEP DO TREN WINDOWS THAT cho spec r3 (N1-N4 + N8-N12 + N7 + kich thuoc).

Chay:  py wp541-do-g2-windows.py "<thu-muc-kho>"

KHONG ghim SHA. No do BAT KY dau nao dang o tren nhanh, roi TU PHAN LOAI:
  head == 2f70869a  -> day la g1, CHUA co ban va g2. Van do, nhung nhan la NEN DO.
  head la hau due    -> ung vien g2.
  khac               -> KHONG DO DUOC (rebase? nham nhanh?) -> rc=3, khong ket luan.

BA TRANG THAI o moi chot: DAT / TRUOT / KHONG DO DUOC. Cai thu ba KHONG duoc lang le
thanh mot trong hai cai kia — do la ca doctrine `None != False` cua kho.

MOI chot am deu co DOI CHUNG DUONG. Mot chot chi do chieu "phai tu choi" thi mot ham
`return None` vo dieu kien cung qua duoc no.

Dot bien chay tren BAN SAO TAM; cay that khong bi dung toi.
"""
import contextlib, hashlib, importlib.util, inspect, io, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath

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
    try: print(van, flush=True)
    except Exception:
        try: sys.stdout.buffer.write(van.encode("utf-8", "replace") + b"\n"); sys.stdout.flush()
        except Exception: print(van.encode("ascii", "backslashreplace").decode("ascii"), flush=True)

SHA_G1   = "2f70869a0537843e9cae78618ee7ae8c261d972d"
# KHONG ghim base. Spec r3 N6' khai do numstat so d705623 — NHUNG spec CUNG bao executor
# `git merge origin/master`. Sau merge, phep do so d705623 NUOT ca phan master mang vao:
# do that 18-09 tren ban va g2 cua agy cho 5 tep / +812, trong khi viec cua agy la 2 tep / +353.
# Mot chot nhu the se bao "vuot tran" cho mot ban va KHONG vuot. Base dung la MERGE-BASE.
SHA_BASE_SPEC = "d705623162b75b7340ee7cca54ac2d2abbddbb6f"
BAN_BO_DO = "2026-09-19d"              # doi MOI khi sua bo do - log tu khai ban nao
TRAN_TEP, TRAN_DONG = 2, 400          # N7' cua spec r3
MAU_WIN  = 'if nen_thuc == "windows":'
# Ca ngoai pham vi r3 §ngoai_pham_vi — do CHINH SPEC khai, khong phai bo do tu quyet.
# Do la DANH SACH CHO PHEP: ca do nao KHONG nam trong day va KHONG phai "thieu cong cu"
# thi la TRUOT. Danh sach cam thi bao gio cung thieu; danh sach cho phep thi biet truoc.
NGOAI_PHAM_VI = set("t131 t132 t150 t125 t35 t36 t37 t38 t39 t40".split())
# Ca cua CHINH packet nay. Mot ca o day ma DO thi khong bao gio duoc bo qua.
CA_PACKET = set("t165 t166 t167 t168 t169 t170 t171 t172 t173".split())
CA15  = "t129 t130 t131 t132 t133 t136 t138 t139 t144 t145 t146 t147 t149 t150 t151".split()
CAMOI = "t165 t166 t167 t168".split()

DAT, TRUOT, KDD = "DAT", "TRUOT", "KHONG DO DUOC"
so, chot = {}, []
def ghi(k, v): so[k] = v; return v
def ket(ten, trang_thai, chi_tiet=""):
    chot.append((ten, trang_thai, chi_tiet))
    inn(f"  [{trang_thai:14}] {ten}" + (f"   {chi_tiet}" if chi_tiet else ""))
    return trang_thai

# ---------------- doc log cua bo test (ban 3, da do tren log THAT) ----------------
RX_DO_CHO  = re.compile(r"(?m)^!!! do (\S+) (.*)$")
RX_DO_CUOI = re.compile(r"(?m)^ {2}(\S{1,4}) {2}(\S+): (.*)$")
RX_BO_QUA  = re.compile(r"(?m)^ {2}\S{1,6} QUA (\S+): (.*)$")
RX_TONG    = re.compile(r"lease_publish: (\d+)/(\d+)\b[^\n]*?=(\d+),[^\n]*?=(\d+)")

def so_ca(t):
    m = re.match(r"t(\d+)", t); return (int(m.group(1)) if m else 10**6, t)

def doc_do(out):
    tai_cho = {t: l.strip() for t, l in RX_DO_CHO.findall(out)}
    bo = {t for t, _ in RX_BO_QUA.findall(out)}
    cuoi = {t: l.strip() for _, t, l in RX_DO_CUOI.findall(out) if t not in bo}
    hop = dict(cuoi); hop.update(tai_cho)
    gc, tin = [], True
    if set(tai_cho) != set(cuoi):
        gc.append(f"hai nguon LECH: chi-tai-cho={sorted(set(tai_cho)-set(cuoi))} chi-cuoi={sorted(set(cuoi)-set(tai_cho))}")
        tin = False
    m = RX_TONG.search(out)
    if not m:
        gc.append("KHONG doc duoc dong tong ket"); tin = False
    else:
        dat, tren = int(m.group(1)), int(m.group(2))
        gc.append(f"so hoc: {tren}-{dat}={tren-dat} do; doc duoc {len(hop)}")
        if tren - dat != len(hop):
            gc.append(f"LECH SO HOC: thieu {tren-dat-len(hop)} ca"); tin = False
    return hop, gc, tin

_MAU = ("!!! do t02b_ten_KHONG_CO_THAM_QUYEN a\n"
        "!!! do t150_x WinError 1314 required privilege\n"
        "  BỎ QUA t131_y: nen fixture\n"
        "  ĐỎ  t02b_ten_KHONG_CO_THAM_QUYEN: a\n"
        "  ĐỎ  t150_x: WinError 1314 required privilege\n"
        "lease_publish: 1/3 đạt; đã chạy=3, bỏ qua=1\n")

def chay(argv, cwd, phut=60):
    mt = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8",
              PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1")
    p = subprocess.run([sys.executable] + argv, cwd=str(cwd), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=phut*60, env=mt)
    return p.returncode, (p.stdout or "") + (p.stderr or "")

def mau_ca(out, t):
    m = re.search(r"(?m)^<<< ra (" + t + r"[a-z]?_\S*) [0-9.]+s (\w+)\s*$", out)
    return m.group(2) if m else None

def git(goc, *a, phut=5):
    p = subprocess.run(["git", "-C", str(goc), *a], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=phut*60)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


# ================= NAM PROBE, viet thanh HAM THUAN de TU KIEM duoc =================
# Moi ham tra (trang_thai, chi_tiet, du_lieu). KHONG in, KHONG thoat — nho vay chung
# chay duoc tren nen BAT KY, va `--tu-kiem-probe` goi thang chung de kiem chinh bo do.

def _san(t):
    d = Path(t)/"d"; d.mkdir(); cw = Path(t)/"cwd"; cw.mkdir(); pf = Path(t)/"pf"; pf.mkdir()
    return d, cw, pf

def do_n8(goi, sig, tept):
    """Buoc 1 (CONG_CU_GIT) chi duoc nhan git.exe. Doi chung duong: git.exe VAN phai nhan."""
    kq = {}
    with tempfile.TemporaryDirectory() as t:
        d, cw, pf = _san(t)
        for ten in ("git.exe", "git.bat", "git.cmd", "git.py", "khong-phai-git.txt"):
            f = d/ten; f.write_text("x", encoding="utf-8")
            r, _ = goi(cong_cu_git=str(f), path="", program_files=str(pf), cwd=str(cw))
            kq[f"CONG_CU_GIT={ten}"] = "NHAN" if r else "TU CHOI"
    lot = [k for k, v in kq.items() if v == "NHAN" and not k.endswith("git.exe")]
    if kq.get("CONG_CU_GIT=git.exe") != "NHAN":
        return KDD, "doi chung duong hong: git.exe hop le ma bi tu choi", kq
    return (DAT if not lot else TRUOT), ("" if not lot else f"con nhan: {lot}"), kq

def do_n9(goi, sig, tept):
    """Muc PATH boc nhay kep phai NHAN; muc rong / toan khoang trang phai bo qua, khong nem."""
    kq = {}
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)/"co git"; d.mkdir(); cw = Path(t)/"cwd"; cw.mkdir(); pf = Path(t)/"pf"; pf.mkdir()
        (d/"git.exe").write_text("x", encoding="utf-8")
        for nhan, muc in (("khong nhay", str(d)), ("co nhay kep", f'"{d}"'),
                          ("rong", ""), ("chi khoang trang", "   ")):
            try:
                r, _ = goi(path=muc, program_files=str(pf), cwd=str(cw))
                kq[f"PATH {nhan}"] = "NHAN" if r else "None"
            except Exception as e:
                kq[f"PATH {nhan}"] = f"NEM {type(e).__name__}"
    if kq.get("PATH khong nhay") != "NHAN":
        return KDD, "doi chung duong hong: muc PATH thuong ma khong tim ra git.exe", kq
    ok = (kq.get("PATH co nhay kep") == "NHAN"
          and kq.get("PATH rong") == "None" and kq.get("PATH chi khoang trang") == "None")
    return (DAT if ok else TRUOT), ("" if ok else "xem bang"), kq

def do_n10(goi, sig, tept):
    """Mot dau ';' trong TEN thu muc khong duoc lam mat muc git.exe hop le o muc kia."""
    co_sep = any(("cach" in k) or ("sep" in k.lower()) for k in sig.parameters)
    if os.pathsep == ";" and not co_sep:
        return (KDD, "tren Windows os.pathsep DA la ';' va ham khong nhan tham so dau phan cach "
                     "-> khong tach duoc hai gia thuyet", {"os.pathsep": os.pathsep, "co tham so sep": co_sep})
    with tempfile.TemporaryDirectory() as t:
        la = Path(t)/"co;dau"; la.mkdir()
        d, cw, pf = _san(t)
        (d/"git.exe").write_text("x", encoding="utf-8")
        r, _ = goi(path=str(la) + os.pathsep + str(d), program_files=str(pf), cwd=str(cw))
        r0, _ = goi(path=str(d), program_files=str(pf), cwd=str(cw))     # doi chung duong
    kq = {"co muc chua ';'": "NHAN" if r else "None", "doi chung (khong co ';')": "NHAN" if r0 else "None"}
    if not r0:
        return KDD, "doi chung duong hong", kq
    return (DAT if r else TRUOT), ("" if r else "muc git.exe hop le bi MAT"), kq

def do_n11(goi, sig, tept):
    """Truyen chan_doan => thu duoc thong bao VA stderr IM. Khong truyen => stderr VAN co."""
    if "chan_doan" not in sig.parameters:
        return KDD, "_git_windows khong nhan tham so chan_doan", {"tham so": list(sig.parameters)}
    with tempfile.TemporaryDirectory() as t:
        d, cw, pf = _san(t)
        (d/"git.exe").write_text("x", encoding="utf-8")
        cd = []
        _, e_co = goi(path=str(d), program_files=str(pf), cwd=str(cw), chan_doan=cd)
        _, e_kh = goi(path=str(d), program_files=str(pf), cwd=str(cw))
    kq = {"chan_doan thu duoc (muc)": len(cd),
          "stderr khi CO chan_doan (byte)": len(e_co.encode()),
          "stderr khi KHONG truyen (byte)": len(e_kh.encode())}
    if len(cd) == 0 and len(e_kh.encode()) == 0:
        return KDD, "nhanh %ProgramFiles% khong phan giai KHONG bay ra chan doan nao -> chua do duoc", kq
    ok = len(cd) > 0 and len(e_co.encode()) == 0 and len(e_kh.encode()) > 0
    return (DAT if ok else TRUOT), ("" if ok else "xem bang"), kq

def do_n12(goi, sig, tept):
    """Hang sentinel git_path trong fixture phai tuyet doi tren CA HAI nen."""
    nd = tept.read_text(encoding="utf-8", errors="replace")
    hang = sorted(set(re.findall(r'git_path\s*=\s*"([^"]+)"', nd)))
    xau = [h for h in hang if not (PurePosixPath(h).is_absolute() and PureWindowsPath(h).is_absolute())]
    kq = {"hang git_path tim thay": hang, "chi tuyet doi MOT nen": xau}
    if not hang:
        return KDD, "khong tim thay hang git_path nao trong fixture -> mau doc co the da doi", kq
    return (DAT if not xau else TRUOT), ("" if not xau else f"chi-mot-nen: {xau}"), kq

PROBE = [("N8 buoc 1 chi nhan git.exe", do_n8),
         ("N9 boc nhay kep o muc PATH", do_n9),
         ("N10 dau ';' trong ten thu muc", do_n10),
         ("N11 chan doan doi kenh", do_n11),
         ("N12 hang sentinel tuyet doi CA HAI nen", do_n12)]

# --- che do TU KIEM: chay nam probe tren mot cay bat ky, nen bat ky ---
if "--tu-kiem-probe" in sys.argv:
    _g = Path(sys.argv[sys.argv.index("--tu-kiem-probe") + 1]).resolve()
    _sp = importlib.util.spec_from_file_location("lp_tk", str(_g/"ops"/"lease_publish.py"))
    _lp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_lp)
    _sig = inspect.signature(_lp._git_windows)
    def _goi(**kw):
        e = io.StringIO()
        with contextlib.redirect_stderr(e):
            return _lp._git_windows(**kw), e.getvalue()
    print(f"TU KIEM PROBE tren {_g}  (nen {sys.platform})")
    for _ten, _f in PROBE:
        _tt, _ct, _dl = _f(_goi, _sig, _g/"ops"/"lease_publish_test.py")
        print(f"  [{_tt:14}] {_ten}" + (f"   {_ct}" if _ct else ""))
        for _k, _v in (_dl or {}).items(): print(f"        {_k:34}: {_v}")
    sys.exit(0)

inn("=" * 78); inn("WP541 g2 - phep do tren Windows that (spec r3: N1-N4, N8-N12, N7, kich thuoc)"); inn("=" * 78)

# ---------------- tu kiem bo doc ----------------
_d, _g, _t = doc_do(_MAU)
_ok = (len(_d) == 2 and any(x.startswith("t02b") for x in _d)
       and not any(x.startswith("t131") for x in _d) and _t)
inn("Tu kiem bo doc log:", DAT if _ok else TRUOT)
if not _ok:
    inn(""); inn("KHONG DO DUOC: bo doc log cua chinh script nay sai -> khong do gi ca."); sys.exit(3)

# ---------------- 0. nen do ----------------
goc = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
tep, tept = goc / "ops" / "lease_publish.py", goc / "ops" / "lease_publish_test.py"
inn(""); inn("-" * 78); inn("0. NEN DO")
# MOI LOG PHAI TU KHAI no do CAI GI bang BO DO NAO. Bai hoc 19-09-2026: mot luot do
# gui ve duoc doc nhu ket qua cua ban va dang xet, nhung that ra la ban do CU chay
# tren nhanh KHAC. Doc ra thi mat mot vong; log tu khai thi thay ngay dong dau.
try:
    _tu = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
except Exception as _e:
    _tu = f"khong tu bam duoc: {_e}"
ghi("bo_do_sha256", _tu)
inn(f"  BO DO        : sha256 {_tu[:16]}  (ban {BAN_BO_DO})")
inn("  sys.platform :", sys.platform, "| python", sys.version.split()[0])
inn("  os.pathsep   :", repr(os.pathsep), "| PATHEXT:", repr(os.environ.get("PATHEXT"))[:60])
inn("  ProgramFiles :", repr(os.environ.get("ProgramFiles")), "| SystemRoot:", repr(os.environ.get("SystemRoot")))
inn("  CONG_CU_GIT  :", repr(os.environ.get("CONG_CU_GIT")))
inn("  goc kho      :", goc)

quyen = None
if sys.platform == "win32":
    try:
        import ctypes; quyen = bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception: quyen = None
ghi("quyen_admin", quyen)
symlink_duoc = None
try:
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)/"a.txt"; d.write_text("x", encoding="utf-8")
        try: os.symlink(str(d), str(Path(t)/"lk")); symlink_duoc = True
        except OSError as e: symlink_duoc = False; ghi("symlink_loi", f"{type(e).__name__}: {e}")
except Exception as e: ghi("symlink_loi", str(e))
ghi("symlink_duoc", symlink_duoc)
inn("  Administrator:", quyen, "| tao symlink duoc:", symlink_duoc)

loi = []
# Cong kich thuoc la phep do tren LICH SU GIT, khong dinh gi den nen. Cho phep
# --chi-kich-thuoc chay o moi nen de con TU KIEM duoc chinh cong nay (da dung
# de tai dung ca hai ve cua su co nen-cu 19-09). Moi chot CHUC NANG van doi Windows.
if sys.platform != "win32" and "--chi-kich-thuoc" not in sys.argv:
    loi.append(f"KHONG phai Windows (sys.platform={sys.platform!r})")
if not tep.is_file():  loi.append(f"khong thay {tep}")
if not tept.is_file(): loi.append(f"khong thay {tept}")
if not shutil.which("git"): loi.append("khong co `git` trong PATH")

rc, head, _ = git(goc, "rev-parse", "HEAD")
if rc: loi.append("khong doc duoc HEAD")
ghi("head", head)
rc_a, _, _ = git(goc, "merge-base", "--is-ancestor", SHA_G1, head or "HEAD")
la_hau_due = (rc_a == 0)
if head == SHA_G1:
    the_he = "g1"; inn(f"  HEAD = {head[:8]} -> DAY LA g1. CHUA co ban va g2; ket qua duoi la NEN DO.")
elif la_hau_due:
    the_he = "g2"; inn(f"  HEAD = {head[:8]} -> hau due cua g1 ({SHA_G1[:8]}): ung vien g2.")
else:
    the_he = "?"; loi.append(f"HEAD={head[:8]} KHONG phai g1 va KHONG phai hau due cua {SHA_G1[:8]} — rebase? nham nhanh?")
ghi("the_he", the_he)
rc_r, refs, _ = git(goc, "for-each-ref", "--points-at", head or "HEAD",
                    "--format=%(refname:short)")
dsr = [x for x in refs.splitlines() if x.strip() and x.strip() != "do-tam"]
ghi("ref_tro_toi_head", dsr)
inn(f"  ref tro toi HEAD: {', '.join(dsr) if dsr else '(khong ref nao - HEAD roi tu do)'}")

if loi:
    inn(""); inn("KHONG DO DUOC: nen do sai, KHONG in ket luan nao.")
    for x in loi: inn("  -", x)
    sys.exit(3)

# ---------------- 1. kich thuoc (N7' cua spec r3) ----------------
inn(""); inn("-" * 78); inn("1. KICH THUOC — tran spec r3: <= 2 tep va <= 400 dong them")
# VE NEN PHAI TUOI — va phai CHUNG MINH duoc la tuoi, khong phai gia dinh.
# Bai hoc tra gia 19-09-2026: clone tai dung chi fetch nhanh ban va, `origin/master`
# dung yen tu 14-09 (c16bd32, sau 97 commit). merge-base roi ve dung dinh master cu,
# nen diff NUOT ca 97 commit master: do ra 46 tep / +7118 thay vi 2 tep / +397 —
# CUNG MOT COMMIT 0ea95de. Mot tieu chi DELTA ma ve nen khong tuoi thi khong sai
# lech mot chut, no sai ca mot bac do lon.
# Cho nen: nen khong chung minh duoc la tuoi => KHONG DO DUOC (rc=3), KHONG phai TRUOT.
# TRUOT la mot PHAN QUYET ve ban va; phan quyet chi duoc phep phat ra khi da do duoc.
rc_lr, out_lr, er_lr = git(goc, "ls-remote", "origin", "refs/heads/master")
rc_lm, lm, er_lm     = git(goc, "rev-parse", "origin/master")
rm = out_lr.split()[0] if (not rc_lr and out_lr.strip()) else ""
if not rm:
    ket("N7' kich thuoc", KDD,
        f"khong hoi duoc master tren remote (ls-remote rc={rc_lr}): {er_lr[:60]} "
        f"— khong chung minh duoc ve nen con tuoi")
    rc_mb, mb, ns, rc = 1, "", "", 1
elif rc_lm or not lm:
    ket("N7' kich thuoc", KDD, f"khong doc duoc origin/master trong clone: {er_lm[:60]}")
    rc_mb, mb, ns, rc = 1, "", "", 1
elif lm != rm:
    # Dem xem tut lai bao xa, neu dem duoc — con so nay noi ro muc do sai lech.
    rc_c, sau, _ = git(goc, "rev-list", "--count", f"{lm}..{rm}")
    xa = f", tut lai {sau} commit" if (not rc_c and sau.strip().isdigit()) else ""
    inn(f"  origin/master trong clone : {lm[:12]}")
    inn(f"  master tren remote        : {rm[:12]}{xa}")
    ghi("master_clone", lm); ghi("master_remote", rm)
    ket("N7' kich thuoc", KDD,
        f"ve nen CU: origin/master={lm[:12]} != remote={rm[:12]}{xa} "
        f"— chay `git -C <kho> fetch origin master` roi do lai")
    rc_mb, mb, ns, rc = 1, "", "", 1
else:
    inn(f"  ve nen TUOI: origin/master = {lm[:12]} == master tren remote")
    ghi("master_clone", lm); ghi("master_remote", rm)
    rc_mb, mb, er_mb = git(goc, "merge-base", "origin/master", head)
if rc_mb or not mb:
    if mb == "" and rm and lm == rm:
        ket("N7' kich thuoc", KDD, f"khong tinh duoc merge-base voi origin/master: {er_mb[:70]}")
    ns, rc = "", 1
else:
    ghi("merge_base", mb)
    inn(f"  merge-base(origin/master, HEAD) = {mb[:12]}")
    if mb != SHA_BASE_SPEC:
        inn(f"  LUU Y: khac base ma spec r3 khai ({SHA_BASE_SPEC[:12]}) — vi nhanh da merge master.")
        inn(f"         Do so base cu se NUOT phan master mang vao. Dung merge-base moi la viec cua executor.")
        rc_x, ns_x, _ = git(goc, "diff", "--numstat", SHA_BASE_SPEC, head)
        if not rc_x:
            h = [l.split("\t") for l in ns_x.splitlines() if l.strip()]
            a = sum(int(x[0]) for x in h if x[0].isdigit())
            ghi("numstat_theo_base_spec", {"tep": len(h), "them": a})
            inn(f"         (doi chieu: so base spec = {len(h)} tep / +{a} — con so ay KHONG dung de cham)")
    rc, ns, er = git(goc, "diff", "--numstat", mb, head)
if rc:
    pass
else:
    hang = [l.split("\t") for l in ns.splitlines() if l.strip()]
    them = sum(int(h[0]) for h in hang if h[0].isdigit())
    xoa  = sum(int(h[1]) for h in hang if h[1].isdigit())
    ghi("so_tep", len(hang)); ghi("dong_them", them); ghi("dong_xoa", xoa)
    for h in hang: inn(f"    {h[2]:34} +{h[0]:<5} -{h[1]}")
    inn(f"    TONG: {len(hang)} tep, +{them}, -{xoa}   (tran: {TRAN_TEP} tep / {TRAN_DONG} dong them)")
    ket("N7' kich thuoc", DAT if (len(hang) <= TRAN_TEP and them <= TRAN_DONG) else TRUOT,
        f"{len(hang)} tep / +{them}")

# Cong nhanh: do RIENG kich thuoc (vai giay) roi dung. Dung khi can xac minh lai
# ve nen ma khong muon tra 20-45 phut cho ca bo test.
if "--chi-kich-thuoc" in sys.argv:
    inn(""); inn("=" * 78)
    inn("--chi-kich-thuoc: CHI do cong kich thuoc. Day KHONG phai mot luot nghiem thu.")
    inn("-" * 78)
    for _t, _tt, _ct in chot: inn(f"  {_tt:14} {_t}" + (f"   {_ct}" if _ct else ""))
    _k = sum(1 for _, t, _ in chot if t == KDD)
    _r = sum(1 for _, t, _ in chot if t == TRUOT)
    sys.exit(3 if _k else (1 if _r else 0))

# ---------------- 2. bo test day du ----------------
inn(""); inn("-" * 78); inn("2. BO TEST DAY DU (10-40 phut)")
rc_n, out_n = chay(["ops/lease_publish_test.py"], goc)
ghi("rc_suite", rc_n)
m = RX_TONG.search(out_n)
inn("  rc =", rc_n, "|", m.group(0) if m else "(KHONG doc duoc dong tong ket)")
if m:
    ghi("dat", int(m.group(1))); ghi("tren", int(m.group(2))); ghi("bo_qua_so", int(m.group(4)))
do_het, gc, tin = doc_do(out_n)
ghi("so_ca_do", len(do_het)); ghi("liet_ke_day_du", tin)
for g in gc: inn("   *", g)
inn(""); inn(f"  === {len(do_het)} CA DO ===")
for t in sorted(do_het, key=so_ca):
    inn(f"   {t.split('_')[0]:7} {t}"); inn(f"           {do_het[t][:150]}")
ghi("do_ly_do", {t: do_het[t][:300] for t in do_het})
# ---- CHOT: moi ca DO phai GIAI THICH DUOC ----
# Thieu chot nay, bo do in danh sach do roi van thoat rc=0. Do dung la loi da xay ra:
# luot Windows 19-09 co t171 DO ma bo do bao "DAT 10 | TRUOT 0" va rc=0.
def _khoa(t): return t.split("_")[0]
do_packet, do_la, do_thieu_cong_cu = [], [], []
for t in sorted(do_het, key=so_ca):
    k, ly = _khoa(t), do_het[t]
    if k in CA_PACKET:                              do_packet.append(t)
    elif "KHÔNG ĐO ĐƯỢC" in ly or "thiếu `" in ly:  do_thieu_cong_cu.append(t)
    elif k in NGOAI_PHAM_VI:                        pass
    else:                                           do_la.append(t)
ghi("do_packet", do_packet); ghi("do_la", do_la); ghi("do_thieu_cong_cu", do_thieu_cong_cu)
inn("")
inn(f"  ca DO thuoc CHINH packet nay : {[_khoa(x) for x in do_packet] or 'khong co'}")
inn(f"  ca DO ngoai pham vi (r3 khai): {[_khoa(x) for x in sorted(do_het, key=so_ca) if _khoa(x) in NGOAI_PHAM_VI]}")
inn(f"  ca DO vi THIEU CONG CU       : {[_khoa(x) for x in do_thieu_cong_cu] or 'khong co'}")
inn(f"  ca DO LA (khong giai thich duoc): {[_khoa(x) for x in do_la] or 'khong co'}")
ket("Khong ca nao cua PACKET bi DO", DAT if not do_packet else TRUOT,
    "" if not do_packet else f"DO: {[_khoa(x) for x in do_packet]} — ban va CHUA xong")
ket("Moi ca DO deu giai thich duoc", DAT if not do_la else TRUOT,
    "" if not do_la else f"la: {[_khoa(x) for x in do_la]}")
if do_thieu_cong_cu:
    ket("Cong cu day du de do", KDD, f"thieu cong cu cho {[_khoa(x) for x in do_thieu_cong_cu]}")

bq = sorted({t for t, _ in RX_BO_QUA.findall(out_n)}, key=so_ca); ghi("ca_bo_qua", bq)
inn(""); inn(f"  BO QUA ({len(bq)}): {[x.split('_')[0] for x in bq]}")

inn(""); inn("  N1-N4 (t165-t168), tieu chi nghiem thu cua r2, nay la chi bao hoi quy:")
b4 = {t: mau_ca(out_n, t) for t in CAMOI}; ghi("ca_moi", b4)
for t in CAMOI: inn(f"     {t}: {b4[t]}")
ket("N1-N4 (t165-t168)", DAT if all(v == "QUA" for v in b4.values())
    else (KDD if any(v is None for v in b4.values()) else TRUOT), str(b4))

inn(""); inn("  15 ca tung do tren CI:")
b15 = {t: mau_ca(out_n, t) for t in CA15}; ghi("ca15", b15)
inn("    " + "  ".join(f"{t}:{b15[t]}" for t in CA15))

# t136 — N12 do GIAN TIEP qua ket qua ca
t136_ten = next((t for t in do_het if t.startswith("t136")), None)
if b15.get("t136") == "QUA":
    ket("N12 t136 (qua ket qua ca)", DAT, "t136 QUA")
elif b15.get("t136") is None:
    ket("N12 t136 (qua ket qua ca)", KDD, "khong thay t136 trong log")
else:
    ly = do_het.get(t136_ten, "")
    ket("N12 t136 (qua ket qua ca)", TRUOT, f"DO: {ly[:90]}")

# ---------------- 3. probe THANG vao ham ----------------
inn(""); inn("-" * 78); inn("3. PROBE THANG — goi _git_windows voi tham so tiem")
spec = importlib.util.spec_from_file_location("lp541", str(tep))
lp = importlib.util.module_from_spec(spec); spec.loader.exec_module(lp)
sig = inspect.signature(lp._git_windows)
ghi("tham_so__git_windows", list(sig.parameters))
inn("  tham so cua _git_windows:", list(sig.parameters))

def goi(**kw):
    """Goi _git_windows, BAT stderr de mot dong chan doan khong giet luot do."""
    e = io.StringIO()
    with contextlib.redirect_stderr(e):
        r = lp._git_windows(**kw)
    return r, e.getvalue()

# --- doi chung rig: phai tra loi dung mot ca ta BIET TRUOC dap an ---
with tempfile.TemporaryDirectory() as t:
    ngoai = Path(t)/"ngoai"; ngoai.mkdir(); cw = Path(t)/"cwd"; cw.mkdir(); pf = Path(t)/"pf"; pf.mkdir()
    (ngoai/"git.exe").write_text("x", encoding="utf-8")
    r1, _ = goi(path=str(ngoai), program_files=str(pf), cwd=str(cw))
    (cw/"git.exe").write_text("x", encoding="utf-8")
    r2, _ = goi(path=str(cw), program_files=str(pf), cwd=str(cw))
rig_ok = bool(r1) and r2 is None
ghi("rig_doi_chung", rig_ok)
ket("RIG doi chung (biet truoc dap an)", DAT if rig_ok else KDD,
    f"ngoai-cwd->{'NHAN' if r1 else 'None'} | trong-cwd->{'NHAN' if r2 else 'None'}")
if not rig_ok:
    inn(""); inn("KHONG DO DUOC: rig sai, moi chot duoi se vo nghia."); sys.exit(3)

for ten, (tt, ct, dl) in [(t, f(goi, sig, tept)) for t, f in PROBE]:
    ghi("probe_" + ten.split()[0].lower(), dl)
    if isinstance(dl, dict):
        for k, v in dl.items(): inn(f"    {k:34}: {v}")
    ket(ten, tt, ct)

# ---------------- 4. N7 dot bien tren BAN SAO TAM ----------------
inn(""); inn("-" * 78); inn("4. N7 — dot bien tren BAN SAO TAM (cay that KHONG bi dung toi)")
truoc = tep.read_text(encoding="utf-8").count(MAU_WIN)
ghi("n7_truoc", truoc); inn(f"  so dong khop {MAU_WIN!r}: TRUOC = {truoc} [mong 1]")
if truoc != 1:
    ket("N7 dot bien nhanh Windows", KDD, f"mau xuat hien {truoc} lan, khong phai 1")
else:
    with tempfile.TemporaryDirectory() as tmp:
        sao = Path(tmp)/"cay"
        shutil.copytree(goc, sao, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        f2 = sao/"ops"/"lease_publish.py"
        f2.write_text(f2.read_text(encoding="utf-8").replace(MAU_WIN, "if False:"), encoding="utf-8")
        sau = f2.read_text(encoding="utf-8").count(MAU_WIN); ghi("n7_sau", sau)
        inn(f"  SAU (da dot bien) = {sau} [mong 0]")
        if sau != 0:
            ket("N7 dot bien nhanh Windows", KDD, "dot bien KHONG ap duoc")
        else:
            rc_m, out_m = chay(["ops/lease_publish_test.py"], sao)
            m165 = mau_ca(out_m, "t165"); dm, _, _ = doc_do(out_m)
            ten165 = next((t for t in dm if t.startswith("t165")), None)
            ly = (dm.get(ten165) or "")
            ghi("n7_t165", m165); ghi("n7_ly_do", ly[:200])
            inn(f"  t165 sau dot bien: {m165} | {ly[:110]}")
            dung_ly_do = "PATH t" in ly or "/usr/bin" in ly
            ket("N7 dot bien nhanh Windows", DAT if (m165 == "DO" and dung_ly_do) else
                (TRUOT if m165 == "DO" else KDD),
                "giet dung ly do" if (m165 == "DO" and dung_ly_do)
                else ("DO nhung KHONG dung ly do -> tin dung gia" if m165 == "DO" else "khong doc duoc t165"))

# ---------------- KET LUAN ----------------
inn(""); inn("=" * 78)
inn(f"THE HE DO DUOC: {the_he}   HEAD={head[:12]}")
if the_he == "g1":
    inn("LUU Y: day la NEN DO (g1), KHONG phai nghiem thu g2. Cac chot N8-N12 duoi day")
    inn("       TRUOT la DUNG NHU MONG — chung la nhung lo g2 sinh ra de vá.")
inn("-" * 78)
for ten, tt, ct in chot:
    inn(f"  {tt:14} {ten}" + (f"   {ct}" if ct else ""))
n_kdd = sum(1 for _, t, _ in chot if t == KDD)
n_truot = sum(1 for _, t, _ in chot if t == TRUOT)
inn("-" * 78)
inn(f"  DAT {sum(1 for _,t,_ in chot if t==DAT)} | TRUOT {n_truot} | KHONG DO DUOC {n_kdd}")
inn(f"  Tong ca do: {so.get('so_ca_do')} | danh sach day du: {'CO' if so.get('liet_ke_day_du') else 'KHONG DO DUOC'}")
inn(f"  Administrator: {so.get('quyen_admin')} | symlink: {so.get('symlink_duoc')}")
inn(""); inn("--- DAN NGUYEN KHOI JSON NAY VE CHO REVIEWER ---")
ghi("chot", [{"ten": a, "trang_thai": b, "chi_tiet": c} for a, b, c in chot])
inn(json.dumps(so, ensure_ascii=False, indent=1, default=str))
# rc: 0 = moi chot DAT | 1 = co chot TRUOT | 3 = co chot KHONG DO DUOC (uu tien bao dong)
sys.exit(3 if n_kdd else (1 if n_truot else 0))
