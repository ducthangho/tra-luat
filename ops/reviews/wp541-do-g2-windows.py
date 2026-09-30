# -*- coding: utf-8 -*-
"""WP541 g2 - PHEP DO TREN WINDOWS THAT cho spec r3 (N1-N4 + N8-N12 + N7 + kich thuoc).

Chay:  py wp541-do-g2-windows.py "<thu-muc-kho>"

KHONG ghim SHA. No do BAT KY dau nao dang o tren nhanh, roi TU PHAN LOAI:
  head == 2f70869a  -> day la g1, CHUA co ban va g2. Probe van in (lam NEN DO) nhung N7' ra
                       KHONG DO DUOC (g1 da land, diff rong) nen rc=3.
  head la hau due    -> CHUA dinh danh: chi N7' (ca moi g2 mang vao, xem duoi) moi noi ung vien g2 hay khong.
  khac               -> KHONG DO DUOC (rebase? nham nhanh?) -> rc=3, khong ket luan.
Tu 20-09 g1 DA LAND vao master, nen "hau due cua g1" KHONG con loai duoc nhanh nao (do duoc:
master 44620e8 va mot nhanh bookkeeping deu ra "ung vien g2", DAT rc=0). Vi vay doi tuong con
phai (a) co thay doi so voi merge-base va (c) MANG VAO it nhat mot ca MOI cua g2 (CA_MOI_G2:
merge-base chua co, HEAD co) — khong thi KHONG DO DUOC. Chi "(b) cham WRITE_SET_G2" thi KHONG du:
sau g2 da co 6 packet khac cham ops/lease_publish*.py (do duoc: nhanh #607 803c248 ra "THE HE DO
DUOC: g2", N7' DAT 2 tep / +53, DAT 12 rc=0). (c) keo theo (b), nen (b) chi con duoc GHI, khong cham.

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

# Ngoai le KHONG bat => Python thoat rc=1, ma rc=1 o day DA CO NGHIA "co chot TRUOT" (dong
# cuoi tep) — dung ly do ps1 dat `trap` -> rc=3. Do duoc: git vang PATH (dong `git(goc,
# "rev-parse")` chay TRUOC `if loi:`), bo test qua han, ung vien thieu _git_windows, probe
# that nem ngoai le — ca bon tung ra rc=1 ma phep do CHUA HE chay xong.
# Dong KET LUAN in TRUOC traceback, cung kenh stdout: khoi ps1 dan cho reviewer bat dau TU dong
# nay, nen in traceback truoc thi no nam NGOAI khoi (do tren pwsh 7.4: khoi 2 dong, 0 dong
# traceback). try/finally: hook TU HONG (vd. stdout la ong da dong) thi Python tra rc=1 — dung
# ma "co chot TRUOT" (do duoc: BrokenPipe trong hook => rc=1).
def _ngoai_le_la_KDD(kieu, gt, vet):
    try:
        import traceback
        inn(""); inn(f"KHONG DO DUOC: ngoai le khong luong truoc {kieu.__name__}: {gt}")
        inn("".join(traceback.format_exception(kieu, gt, vet)).rstrip())
        inn("Phep do CHUA chay xong. Khong ket luan gi.")
        for _l in (sys.stdout, sys.stderr):
            try: _l.flush()
            except Exception: pass
    finally:
        os._exit(3)
sys.excepthook = _ngoai_le_la_KDD

SHA_G1   = "2f70869a0537843e9cae78618ee7ae8c261d972d"
# KHONG ghim base. Spec r3 N6' khai do numstat so d705623 — NHUNG spec CUNG bao executor
# `git merge origin/master`. Sau merge, phep do so d705623 NUOT ca phan master mang vao:
# do that 18-09 tren ban va g2 cua agy cho 5 tep / +812, trong khi viec cua agy la 2 tep / +353.
# Mot chot nhu the se bao "vuot tran" cho mot ban va KHONG vuot. Base dung la MERGE-BASE.
SHA_BASE_SPEC = "d705623162b75b7340ee7cca54ac2d2abbddbb6f"
BAN_BO_DO = "2026-09-30e"              # doi MOI khi sua bo do - log tu khai ban nao
TRAN_TEP, TRAN_DONG = 2, 400          # N7' cua spec r3
MAU_WIN  = 'if nen_thuc == "windows":'
# Write set cua packet #541 g2. Diff khong cham tep nao o day => do NHAM NHANH.
WRITE_SET_G2 = {"ops/lease_publish.py", "ops/lease_publish_test.py"}
# "Tuoi" chi co nghia khi so voi MAY CHU THAT. Mot mirror cuc bo cu cung tra ls-remote ==
# origin/master (do duoc: master c16bd32 -> "ve nen TUOI", 46 tep / +7118 cho 0ea95de).
# Danh sach CHO PHEP; `remote get-url` da khai trien insteadOf nen chuyen huong cung lo ra.
URL_KHO_HOP_LE = {"https://github.com/ducthangho/tra-luat", "https://github.com/ducthangho/tra-luat.git",
                  # SSH toi CUNG kho (sau _url_sach): `url."git@github.com:".insteadOf "https://github.com/"`
                  # rat pho bien o may dev; thieu hai dang nay thi kho THAT bi bao "KHONG phai kho that".
                  "ssh://github.com/ducthangho/tra-luat", "ssh://github.com/ducthangho/tra-luat.git",
                  "git@github.com:ducthangho/tra-luat", "git@github.com:ducthangho/tra-luat.git"}
# `remote get-url` KHAI TRIEN insteadOf, ma mau `url."https://<token>@github.com/".insteadOf` rat pho
# bien. In/ghi nguyen van la dua TOKEN vao log va vao khoi JSON ps1 bao dan cho reviewer (do duoc:
# 3 dong trong khoi dan). Bo userinfo TRUOC khi in va TRUOC khi so — token van la GitHub that.
# Authority ket thuc o `/`, `?` hoac `#` DAU TIEN — dung luat git/curl. Ban `[^/]*@` nuot ca `?`/`#`
# nen mot URL tro toi MAY KHAC (host dung truoc `?`, duoi `?` la `@github.com/<kho>`) duoc "lam sach"
# thanh dung mot muc CHO PHEP, trong khi git noi toi may kia (do duoc: mirror cu phuc vu qua HTTPS =>
# "ve nen TUOI", TRUOT 46 tep / +7118). Van bo toi `@` CUOI trong authority: userinfo co `@` tran thi
# curl tu choi ("Bad hostname"), con khi in thi khong lo phan sau `@` thu nhat.
_RX_USERINFO = re.compile(r"^([A-Za-z][A-Za-z0-9+.-]*://)[^/?#]*@")
def _url_sach(u): return _RX_USERINFO.sub(r"\1", u or "")          # de SO (luat git/curl)
# IN phai che RONG hon SO: mat khau co `?`/`#` TRAN thi `[^/?#]*@` khong khop nen URL ra log NGUYEN VAN
# (do duoc tren 2026-09-30b: 3 dong o --chi-kich-thuoc, 3 dong trong khoi dan --chi-probe; ban 30a: 0).
# Che toi `@` CUOI CUNG cua CA chuoi (co hay khong co scheme), va DE DAU `***@` de ban in khong tu nhan la
# github.com khi git noi toi may khac (vd. host truoc `?`). Ban 30c che "toi `@` cuoi truoc `/` dau tien"
# nen VAN lo khi mat khau co `/` tran, hoac URL dang scp `user:mk@host:duong` (khong scheme) — do tren
# 2026-09-30c: 3 dong / 1 trong khoi dan --chi-kich-thuoc, 5 / 3 o --chi-probe, moi dang. Moi ky tu DUNG
# la mot duong nua; "toi `@` cuoi" khong con ky tu dung nao. Hai quy tac, hai muc dich: SO theo git, IN
# theo "thua con hon lo".
def _url_in(u): return re.sub(r"^([A-Za-z][A-Za-z0-9+.-]*://)?.*@", r"\1***@", u or "")
# Thong bao loi cua git CHI bo userinfo toi `@` DAU TIEN: userinfo co `@` tran (vd. ten dang nhap la
# email) thi phan sau van ra stderr ls-remote, ma stderr ay duoc in vao dong KDD cua N7' (do duoc:
# 2 dong trong log, 1 trong khoi dan). Lam sach MOI URL trong van ban truoc khi in — che toi `@` CUOI tren
# DONG (cung luat IN voi _url_in: khong con ky tu dung nao). Ban 30d dung o `\s'"` nen phan git de lai co
# `'`/`"`/khoang trang (vd. `u@x:p'<bi mat>@github.com`) VAN lo — do tren 2026-09-30d: 2 dong / 1 trong
# khoi dan --chi-kich-thuoc, 3 / 2 o --chi-probe, moi dang.
def _an_userinfo(t): return re.sub(r"([A-Za-z][A-Za-z0-9+.-]*://)[^\n]*@", r"\1***@", t or "")
# Ca ngoai pham vi r3 §ngoai_pham_vi — do CHINH SPEC khai, khong phai bo do tu quyet.
# Do la DANH SACH CHO PHEP: ca do nao KHONG nam trong day va KHONG phai "thieu cong cu"
# thi la TRUOT. Danh sach cam thi bao gio cung thieu; danh sach cho phep thi biet truoc.
NGOAI_PHAM_VI = set("t131 t132 t150 t125 t35 t36 t37 t38 t39 t40".split())
# Ca cua CHINH packet nay. Mot ca o day ma DO thi khong bao gio duoc bo qua.
CA_PACKET = set("t165 t166 t167 t168 t169 t170 t171 t172 t173".split())
# Ca MOI ma g2 them vao (N8-N12). Doi tuong do phai MANG chung vao: merge-base chua co, HEAD co.
CA_MOI_G2 = "t169 t170 t171 t172 t173".split()
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
# Dong tong ket THAT o DAU dong. Ca DO co the in lai stdout cua mot luot CON (t155 chay lai t01, t72/t98 chay
# "bo") — dong tong LONG ay nam GIUA dong (do: 20 dong long deu o giua dong, chi dong tong that o dau dong), ma
# `search` khong neo bat no TRUOC. Do tren 2026-09-30c, 0ea95de + dot bien lam t01 DO: doc ra "0/1" =>
# "danh sach KHONG day du", "LECH SO HOC: thieu -20 ca", trong khi tong that 166-145=21 == 21 ca doc duoc.
RX_TONG    = re.compile(r"(?m)^lease_publish: (\d+)/(\d+)\b[^\n]*?=(\d+),[^\n]*?=(\d+)")

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

# Mau co dong tong LONG giua dong (dang t155 in lai luot con): bo doc bat dong tong DAU TIEN la tu kiem DO.
_MAU = ("!!! do t02b_ten_KHONG_CO_THAM_QUYEN a 'lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0'\n"
        "!!! do t150_x WinError 1314 required privilege\n"
        "  BỎ QUA t131_y: nen fixture\n"
        "  ĐỎ  t02b_ten_KHONG_CO_THAM_QUYEN: a\n"
        "  ĐỎ  t150_x: WinError 1314 required privilege\n"
        "lease_publish: 1/3 đạt; đã chạy=3, bỏ qua=1\n")

# Bien PYTHON* cua may nguoi do lot vao bo test la DOI HANH VI bo test: PYTHONOPTIMIZE bo moi `assert` (do tren
# 2026-09-30c: `assert False` qua, rc=0); ban 30d chi trung hoa MOT bien ay, con PYTHONDEVMODE=1 lam t154 DO 2/4
# lan tren 3.11 (sach: 4/4 QUA) => rc=1 "TRUOT Moi ca DO deu giai thich duoc" cho ung vien sach (do tren
# 2026-09-30d). Danh sach CAM luon thieu mot bien — nen day la danh sach CHO PHEP: chi giu bien de trinh thong
# dich CHAY va tim goi DA CAI; PYTHONPATH KHONG giu (CI khong co no). Phep hoi dieu kien tien quyet o muc 0
# cung chay qua day, nen no thay DUNG moi truong ma bo test se thay.
_PY_GIU = frozenset({"PYTHONHOME", "PYTHONUSERBASE", "PYTHONNOUSERSITE"})
def chay(argv, cwd, phut=60):
    mt = {k: v for k, v in os.environ.items() if not k.upper().startswith("PYTHON") or k.upper() in _PY_GIU}
    mt.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1")
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

# Dau phan cach dung DE THU. Phai KHAC os.pathsep tren CA HAI nen (';' Windows, ':' POSIX)
# thi hai gia thuyet "tach theo dau duoc truyen" va "tach theo os.pathsep" moi roi ra nhau.
THU_N10 = "|"

def do_n10(goi, sig, tept):
    """Ham phai tach PATH theo dau phan cach DUOC TRUYEN, khong theo os.pathsep cua nen.

    Ban cu do "mot dau ';' trong TEN thu muc" va dat DAT tren Windows du ham sai. No
    degenerate: tren Windows os.pathsep DA la ';', nen 'C:/a;b' that su CO NGHIA la hai
    muc — "tach dung" va "tach sai" cho ra cung ket qua, phep do khong the do nao. No
    da cham DAT cho 95831685 trong khi t171 cua chinh ban va ay DO vi dung khuyet tat ay.
    Mot cong khong the do thi khong phai cong.
    """
    ten_sep = next((k for k in ("phan_cach", "dau_phan_cach", "sep") if k in sig.parameters), None)
    if ten_sep is None:
        # Khong co tham so thi tren Windows KHONG con duong nao tach hai gia thuyet.
        if os.pathsep == ";":
            return (KDD, "tren Windows os.pathsep DA la ';' va ham khong nhan tham so dau phan cach "
                         "-> khong tach duoc hai gia thuyet",
                    {"os.pathsep": os.pathsep, "tham so sep": None})
        with tempfile.TemporaryDirectory() as t:
            la = Path(t)/"co;dau"; la.mkdir()
            d, cw, pf = _san(t)
            (d/"git.exe").write_text("x", encoding="utf-8")
            r, _  = goi(path=str(la) + os.pathsep + str(d), program_files=str(pf), cwd=str(cw))
            r0, _ = goi(path=str(d), program_files=str(pf), cwd=str(cw))
        kq = {"os.pathsep": os.pathsep, "tham so sep": None,
              "co muc chua ';'": "NHAN" if r else "None",
              "doi chung duong (khong co ';')": "NHAN" if r0 else "None"}
        if not r0:
            return KDD, "doi chung duong hong", kq
        return (DAT if r else TRUOT), ("" if r else "muc git.exe hop le bi MAT"), kq

    with tempfile.TemporaryDirectory() as t:
        la = Path(t)/"co;dau"; la.mkdir()          # ';' nam trong TEN, khong phai dau phan cach
        d, cw, pf = _san(t)
        (d/"git.exe").write_text("x", encoding="utf-8")
        noi = str(la) + THU_N10 + str(d)
        kw = dict(program_files=str(pf), cwd=str(cw))
        r_chinh, _ = goi(path=noi,      **{ten_sep: THU_N10},   **kw)   # tach dung  -> NHAN
        r_duong, _ = goi(path=str(d),   **{ten_sep: THU_N10},   **kw)   # doi chung duong
        r_phanbiet, _ = goi(path=noi,   **{ten_sep: os.pathsep}, **kw)  # tach theo os.pathsep -> mat
    kq = {"os.pathsep": os.pathsep, "tham so sep": ten_sep, "dau thu": THU_N10,
          f"noi bang {THU_N10!r}, {ten_sep}={THU_N10!r}":       "NHAN" if r_chinh else "None",
          f"doi chung duong (mot muc, {ten_sep}={THU_N10!r})":  "NHAN" if r_duong else "None",
          f"phan biet: noi bang {THU_N10!r}, {ten_sep}={os.pathsep!r}": "NHAN" if r_phanbiet else "None"}
    if not r_duong:
        return KDD, "doi chung duong hong: mot muc hop le ma khong tim ra git.exe", kq
    # Cong phai CO THE do. Neu ca hai dau phan cach deu ra NHAN thi phep do khong phan
    # biet duoc gi — dung bao DAT, bao thang la khong do duoc.
    if r_phanbiet:
        return (KDD, f"phep do KHONG phan biet duoc: noi bang {THU_N10!r} ma tach theo "
                     f"{os.pathsep!r} VAN tim ra git.exe", kq)
    return ((DAT, "", kq) if r_chinh else
            (TRUOT, f"tach theo os.pathsep thay vi theo {ten_sep} duoc truyen", kq))


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

# --- che do KIEM DONG BO: tep .py nay phai TRUNG TUNG BYTE voi ban nhung trong ps1 ---
# Khong cong nao buoc hai ban sao khop: do duoc, noi tran 2/400 -> 99/99999 CHI trong .py
# thi ci_dang_ky lan t26/t27 van xanh, con chot SHA cua ps1 chi so ban nhung voi hang so
# cua CHINH no. Chay: python wp541-do-g2-windows.py --kiem-dong-bo wp541-do-g2.ps1  (rc 0|3)
if "--kiem-dong-bo" in sys.argv:
    import base64
    _ps = Path(sys.argv[sys.argv.index("--kiem-dong-bo") + 1]).read_text(encoding="ascii")
    _m = re.search(r"(?ms)^\$B64 = @\((.*?)^\)", _ps)
    _k = re.search(r"(?m)^\$ShaBoDo\s*=\s*'([0-9a-f]{64})'", _ps)
    _nhung = base64.b64decode("".join(re.findall(r"'([A-Za-z0-9+/=]*)'", _m.group(1)))) if _m else b""
    _toi = Path(__file__).read_bytes()
    _ok = bool(_m and _k) and _nhung == _toi and hashlib.sha256(_toi).hexdigest() == _k.group(1)
    inn(f"KIEM DONG BO: {DAT if _ok else KDD}  (nhung {len(_nhung)} byte, tep {len(_toi)} byte)")
    sys.exit(0 if _ok else 3)

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
# Bo test (muc 2 va N7) can PyYAML: thieu no, 0ea95de ra 96/166 ca DO (89 bao thang "No module named 'yaml'",
# 7 qua luot con; co PyYAML: 166/166 QUA). Bo do goi chung la "ca DO LA" roi phat TRUOT — do tren 2026-09-30c.
# Dieu kien tien quyet phai hoi bang CHINH tien trinh con se chay bo test (chay(): cung moi truong; cwd = ops/ =
# sys.path[0] cua bo test) va hoi DUNG DUOC chu khong hoi CO MAT. Ban 30d hoi `find_spec("yaml")` o tien trinh
# NAY va nguong 3.8 suy tu NGU PHAP (`:=`) — do tren 2026-09-30d, ca hai ra rc=1 TRUOT cho ung vien sach:
# thu muc du lieu `yaml/` tren PYTHONPATH qua find_spec ma `yaml.safe_dump` khong co (87 ca "la"); python 3.8.20
# THAT co PyYAML, bo test dung `str.removeprefix` (3.9) luc CHAY (33 ca "la"; 3.9.23: 166/166).
if not ("--chi-kich-thuoc" in sys.argv or "--chi-probe" in sys.argv):
    _rc_dk, _ra_dk = chay(["-c", "import sys; sys.exit(9) if sys.version_info < (3, 9) else None; import yaml;"
                                 " yaml.safe_dump(yaml.safe_load('a: 1'))"],
                          goc / "ops" if (goc / "ops").is_dir() else Path.cwd(), phut=2)
    if _rc_dk == 9:
        loi.append(f"python {sys.version.split()[0]} < 3.9: bo test cua ung vien dung str.removeprefix (3.9) luc CHAY")
    elif _rc_dk:
        loi.append(f"python nay KHONG co PyYAML dung duoc ({(_ra_dk.strip().splitlines() or [''])[-1][:90]}):"
                   f" \"{sys.executable}\" -m pip install pyyaml"
                   " (ban nhung ps1 tu tai KHONG co pip: chay lai voi -Py <python da co PyYAML>)")

rc, head, _ = git(goc, "rev-parse", "HEAD")
if rc: loi.append("khong doc duoc HEAD")
ghi("head", head)
rc_a, _, _ = git(goc, "merge-base", "--is-ancestor", SHA_G1, head or "HEAD")
la_hau_due = (rc_a == 0)
if head == SHA_G1:
    the_he = "g1"; inn(f"  HEAD = {head[:8]} -> DAY LA g1. CHUA co ban va g2; ket qua duoi la NEN DO.")
elif la_hau_due:
    the_he = "g2"; inn(f"  HEAD = {head[:8]} -> hau due cua g1 ({SHA_G1[:8]}); ung vien g2 hay khong: N7' (muc 1) dinh danh.")
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
rc_u, url_tho, _ = git(goc, "remote", "get-url", "origin")
url_o, url_in = _url_sach(url_tho), _url_in(url_tho)
ghi("origin_url", url_in); inn(f"  origin       : {url_in or '(khong doc duoc)'}")
url_ok = (not rc_u) and url_o.rstrip("/") in URL_KHO_HOP_LE
rc_lr, out_lr, er_lr = git(goc, "ls-remote", "origin", "refs/heads/master") if url_ok else (1, "", "")
er_lr = _an_userinfo(er_lr)
rc_lm, lm, er_lm     = git(goc, "rev-parse", "origin/master")
rm = out_lr.split()[0] if (not rc_lr and out_lr.strip()) else ""
if not url_ok:
    ket("N7' kich thuoc", KDD, f"origin={url_in!r} KHONG phai kho that — 'tuoi' so voi no khong chung minh duoc gi")
    rc_mb, mb, ns, rc = 1, "", "", 1
elif not rm:
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
        inn("         Do so base cu se NUOT phan master mang vao. Dung merge-base moi la viec cua executor.")
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
    cham = sorted({h[2] for h in hang} & WRITE_SET_G2); ghi("cham_write_set", cham)
    def _ca_moi_co(rev):
        r_, nd_, _ = git(goc, "show", f"{rev}:ops/lease_publish_test.py")
        return None if r_ else {t for t in CA_MOI_G2 if re.search(r"(?m)^def " + t + r"[a-z]?_", nd_)}
    o_mb, o_h = _ca_moi_co(mb), _ca_moi_co(head)
    mang = sorted(o_h - o_mb, key=so_ca) if (o_mb is not None and o_h is not None) else None
    ghi("ca_moi_g2_mang_vao", mang)
    if not mang:
        # Do RONG (da land, chinh master), nham nhanh, hay nhanh cua packet KHAC cham cung tep:
        # khong mang ca moi nao cua g2 thi khong phai ung vien. Doc khong duoc (None) cung vay.
        ket("N7' kich thuoc", KDD, f"doi tuong khong phai ung vien: {len(hang)} tep, cham {cham}, ca moi "
                                   f"g2 mang vao {mang!r} — da land? nham nhanh? packet khac?")
    else:
        ket("N7' kich thuoc", DAT if (len(hang) <= TRAN_TEP and them <= TRAN_DONG) else TRUOT,
            f"{len(hang)} tep / +{them}")

# Dinh danh THAT nam o N7' (ca moi g2 mang vao), KHONG o "hau due g1": g1 da land nen moi nhanh deu
# la hau due. Dong dau khoi dan phai tu khai theo ket qua ay (do duoc: master 44620e8 mo khoi bang
# "THE HE DO DUOC: g2", JSON "the_he": "g2", trong khi N7' da ket luan "khong phai ung vien").
# Nhan chi duoc noi DUNG cai do duoc: `[]` khong tach "da land" khoi "nham nhanh"/"packet khac" (do
# duoc tren 2026-09-30b: ung vien 2a67968 DA LAND bi goi "KHONG phai ung vien g2").
if the_he == "g2" and not so.get("ca_moi_g2_mang_vao"):
    the_he = ("KHONG mang ca moi g2 nao (da land? nham nhanh? packet khac?)" if so.get("ca_moi_g2_mang_vao") == []
              else "g2? (CHUA dinh danh duoc doi tuong)")
    ghi("the_he", the_he)

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

CHI_PROBE = "--chi-probe" in sys.argv    # bo qua bo test + N7; giu 0, 1, 3
# ---------------- 2. bo test day du ----------------
if not CHI_PROBE:
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
    # ---- CHOT: phep do phai TRON truoc khi mot chu DAT nao duoc phat ----
    # Ban truoc chi IN `tin`/`rc_suite`: bo test chet giua t171 (rc=134, khong dong tong)
    # van ra "DAT 12 | TRUOT 0" rc=0; ca PACKET vang mat hay bi BO QUA cung duoc cham nhu
    # "khong do". Vang mat khong phai "khong do" — la KHONG DO DUOC.
    vang = [t for t in sorted(CA_PACKET, key=so_ca) if mau_ca(out_n, t) not in ("QUA", "DO")]
    ly_kdd = []
    if not tin: ly_kdd.append("danh sach do KHONG day du")
    if rc_n not in (0, 1) or (rc_n == 1) != bool(do_het):
        ly_kdd.append(f"rc bo test={rc_n} khong khop {len(do_het)} ca DO doc duoc")
    if vang: ly_kdd.append(f"ca PACKET vang/bo qua: {vang}")
    ghi("ca_packet_vang", vang); ghi("ly_do_chua_tron", ly_kdd)
    if ly_kdd: ket("Bo test chay TRON va doc DU", KDD, "; ".join(ly_kdd))
    chua_tron = KDD if ly_kdd else DAT
    ket("Khong ca nao cua PACKET bi DO", chua_tron if not do_packet else TRUOT,
        "" if not do_packet else f"DO: {[_khoa(x) for x in do_packet]} — ban va CHUA xong")
    ket("Moi ca DO deu giai thich duoc", chua_tron if not do_la else TRUOT,
        "" if not do_la else f"la: {[_khoa(x) for x in do_la]}")
    if do_thieu_cong_cu:
        ket("Cong cu day du de do", KDD, f"thieu cong cu cho {[_khoa(x) for x in do_thieu_cong_cu]}")

    bq = sorted({t for t, _ in RX_BO_QUA.findall(out_n)}, key=so_ca); ghi("ca_bo_qua", bq)
    inn(""); inn(f"  BO QUA ({len(bq)}): {[x.split('_')[0] for x in bq]}")

    inn(""); inn("  N1-N4 (t165-t168), tieu chi nghiem thu cua r2, nay la chi bao hoi quy:")
    b4 = {t: mau_ca(out_n, t) for t in CAMOI}; ghi("ca_moi", b4)
    for t in CAMOI: inn(f"     {t}: {b4[t]}")
    # BO_QUA/vang la CHUA CHAY, khong phai DO: chi mot ca DO moi duoc phat TRUOT.
    ket("N1-N4 (t165-t168)", DAT if all(v == "QUA" for v in b4.values())
        else (TRUOT if any(v == "DO" for v in b4.values()) else KDD), str(b4))

    inn(""); inn("  15 ca tung do tren CI:")
    b15 = {t: mau_ca(out_n, t) for t in CA15}; ghi("ca15", b15)
    inn("    " + "  ".join(f"{t}:{b15[t]}" for t in CA15))

    # t136 — N12 do GIAN TIEP qua ket qua ca
    t136_ten = next((t for t in do_het if t.startswith("t136")), None)
    if b15.get("t136") == "QUA":
        ket("N12 t136 (qua ket qua ca)", DAT, "t136 QUA")
    elif b15.get("t136") != "DO":
        ket("N12 t136 (qua ket qua ca)", KDD, f"t136 = {b15.get('t136')!r} — khong chay/khong thay")
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

# --- MOI CONG PHAI TU CHUNG MINH NO CO THE DO ---
# Bai hoc dat nhat cua packet nay: do_n10 ban cu cham DAT cho 95831685 trong khi t171
# cua chinh ban va ay DO vi dung khuyet tat ma N10 sinh ra de bat. No degenerate —
# tren Windows os.pathsep DA la ';' nen "tach dung" va "tach sai" cho cung ket qua.
# Mot cong khong the DO thi khong phai cong, va no nguy hiem hon khong co cong: no
# phat ra mot chu DAT.
#
# Nen truoc khi DUNG nam cong nay de phan quyet, bat tung cong giet mot dot bien da
# biet trong. Cong nao khong giet duoc thi chu DAT cua no bi HA xuong KHONG DO DUOC;
# TRUOT giu nguyen (quan sat truc tiep, vd. g1 van nhan git.bat). Dot bien chay tren BAN SAO TAM; cay that khong bi
# dung toi (cung ky luat nhu N7).
DOT_BIEN_TU_KIEM = [
    ("N8", "ops/lease_publish.py",
     'if chi_dinh and Path(chi_dinh).name.lower() == "git.exe" and hop_le(chi_dinh):',
     "if chi_dinh and hop_le(chi_dinh):"),
    ("N9", "ops/lease_publish.py",
     "d = d_raw.strip().strip('\"')", "d = d_raw.strip()"),
    ("N10", "ops/lease_publish.py",
     "sep = os.pathsep if phan_cach is None else phan_cach", "sep = os.pathsep"),
    ("N11", "ops/lease_publish.py", "if chan_doan is not None:", "if False:"),
    ("N12", "ops/lease_publish_test.py",
     'git_path="//khong-co/git"', 'git_path="/khong-co/git"'),
]
inn(""); inn("  tu kiem cong — moi cong phai giet duoc mot dot bien da biet:")
giet = {}
for ma, duong, tim, thay in DOT_BIEN_TU_KIEM:
    _ten, _ham = next(((a, b) for a, b in PROBE if a.startswith(ma + " ")), (None, None))
    if _ham is None:
        giet[ma] = None; inn(f"    {ma:4} KHONG DO DUOC: khong tim thay probe ten '{ma} ...'"); continue
    try:
        with tempfile.TemporaryDirectory() as _t:
            _c = Path(_t)/"cay"; shutil.copytree(goc/"ops", _c/"ops")
            _f = _c/duong; _nd = _f.read_text(encoding="utf-8")
            if _nd.count(tim) != 1:
                giet[ma] = None
                inn(f"    {ma:4} KHONG DO DUOC: mau dot bien khop {_nd.count(tim)} lan (mong 1)"
                    f" — ma nguon da doi, dot bien nay het y nghia"); continue
            _f.write_text(_nd.replace(tim, thay, 1), encoding="utf-8")
            _sp = importlib.util.spec_from_file_location("lp_db_" + ma, str(_c/"ops"/"lease_publish.py"))
            _m = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_m)
            def _goi_db(**kw):
                _e = io.StringIO()
                with contextlib.redirect_stderr(_e):
                    return _m._git_windows(**kw), _e.getvalue()
            _tt, _ct, _ = _ham(_goi_db, inspect.signature(_m._git_windows),
                               _c/"ops"/"lease_publish_test.py")
        giet[ma] = (_tt == TRUOT)
        inn(f"    {ma:4} dot bien -> {_tt:14} {'GIET DUOC' if _tt == TRUOT else 'SONG SOT'}"
            + (f"   ({_ct})" if _ct else ""))
    except Exception as _e:
        giet[ma] = None; inn(f"    {ma:4} KHONG DO DUOC: {type(_e).__name__}: {_e}")
ghi("cong_giet_duoc_dot_bien", giet)

for ten, (tt, ct, dl) in [(t, f(goi, sig, tept)) for t, f in PROBE]:
    ghi("probe_" + ten.split()[0].lower(), dl)
    if isinstance(dl, dict):
        for k, v in dl.items(): inn(f"    {k:34}: {v}")
    ma = ten.split()[0]
    if giet.get(ma) is not True and tt == DAT:
        # DAT tu mot cong chua chung minh duoc la biet DO thi khong dang tin hon KDD.
        ket(ten, KDD, f"cong KHONG giet duoc dot bien cua chinh no ({giet.get(ma)!r})"
                      f" -> chu DAT nay khong co gia tri")
    else:
        ket(ten, tt, ct)

# ---------------- 4. N7 dot bien tren BAN SAO TAM ----------------
if not CHI_PROBE:
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
# Khoi dan cho reviewer bat dau o dong tren, nen CHE DO phai nam NGAY duoi no: khong co dong nay
# thi mot luot --chi-probe in "DAT 7 | TRUOT 0 | KHONG DO DUOC 0" rc=0 ma khong noi la chua chay bo test.
ghi("che_do", "chi-probe" if CHI_PROBE else "day-du")
if CHI_PROBE:
    inn("--chi-probe: CHI do muc 0, 1, 3. Bo test, N1-N4, t136, N7 KHONG chay - day KHONG phai mot luot nghiem thu.")
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
