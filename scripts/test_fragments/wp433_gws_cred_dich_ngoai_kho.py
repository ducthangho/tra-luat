# -*- coding: utf-8 -*-
"""wp433 P2a — `credentials.json` của gws (W4 `bootstrap`, W5 `_gws_auth_load` trong `tl_gws.py`): trên POSIX nằm ngoài kho git, không
xuyên liên kết ở BẤT KỲ thành phần nào của đường, ghi nguyên tử (spec GWS-CRED-DICH-NGOAI-KHO-A r1). Mọi ca chạy trên bản `tl_gws`
nạp TRONG BỘ NHỚ (nguồn thật hoặc đột biến), HOME/cfgdir tạm, dữ liệu GIẢ, không mạng. Mỗi LƯỢT thu đủ hậu điều rồi so nhãn theo thứ
tự ghi; nhãn đỏ ĐẦU TIÊN thành `TinHieuChotCa(ca, lượt, nhãn)` — đột biến chỉ GIẾT khi khớp cả ba (bảng `_DB` chép §4b của spec)."""
import argparse, contextlib, errno, io, json, os, pathlib, re, shutil, stat, subprocess, sys, tempfile, types, urllib.request  # noqa: E401
TEST_ID = "wp433_gws_cred_dich_ngoai_kho"
_SENT, _MK, _TOK, _CU = "SENTINEL-wp433-gws-gia", "wp433-master-gia", "wp433-token-gia", b"CU-wp433"
_CRED, _PHA = '{"gia": "%s"}' % _SENT, ("mkstemp", "fsync", "chmod", "replace")
_D01 = "[bootstrap] ✗ --require-agent-creds: credential agent chưa nạp được (rc 4)."          # spec §0.1: dòng riêng, không mang cụm
_CUM = {"kho": "nằm trong kho git", "lk": "là liên kết tượng trưng", "dl": "dữ liệu không hợp lệ", "dg": "đường không hợp lệ", "ghi": "ghi lỗi"}
_M3 = r"\[bootstrap\] ✗ (%s): .+" % "|".join(_CUM.values())
_BO_QUA_DUOC, _WINERR, _TEN_OS = ("nguyen_tu", "W5.hardlink"), (1, 50), os.name   # N9(b): MỘT lượt được bỏ qua, chỉ nt, chỉ khi volume không hỗ trợ hardlink
_LUOT_DU_KIEN = {  # N9(b) SỔ LƯỢT — viết RIÊNG khỏi các hàm ca: 11 ca, 46 lượt, đúng thứ tự §4
    "trong_kho": ("W4", "W5"),
    "goc_bieu_dien": ("W5.goc_0", "W5.goc_1", "W5.goc_2", "W5.goc_3", "W5.goc_4", "W5.goc_5", "W5.hai_cham", "W5.tuong_doi_thuong", "W4.goc_w4"),
    "to_tien": ("W4.ong", "W5.ong", "W5.cha", "W5.goc_cfg", "W4.tep_cuoi", "W5.tep_cuoi"),
    "chuoi_kho": ("realpath", "tu_vung"), "duong_xuong_dong": ("W5.cli", "W4.bootstrap"),
    "m1_bien": ("nul", "trang", "goc", "xuong_dong"),
    "bien_cfgdir": ("W4.cfg_la_tep", "W5.cfg_la_tep", "W4.dich_la_thu_muc", "W5.dich_la_thu_muc"),
    "nguyen_tu": ("W4.thuong", "W5.thuong", "W5.hardlink"), "du_lieu_sai_dang": ("N6.kieu", "N6.surrogate", "N6.falsy"),
    "ghi_loi_theo_pha": ("W4.mkstemp", "W4.fsync", "W4.chmod", "W4.replace", "W5.mkstemp", "W5.fsync", "W5.chmod", "W5.replace", "W5.cli"),
    "chung_hop_dong_loi": ("W4.trong_kho", "require"),
}
_dau = lambda e: "wp433-oserror" in str(e)
_KHAI = {  # §4b cột "ngoại lệ khai": (ca, lượt) → (loại, phép nhận, nhãn); ngoài tập của lượt ⇒ `ngoai_le_la`
    ("du_lieu_sai_dang", "N6.kieu"): (AttributeError, lambda e: "'int' object has no attribute 'encode'" in str(e), "kieu"),
    ("du_lieu_sai_dang", "N6.surrogate"): (UnicodeEncodeError, lambda e: "surrogates not allowed" in str(e), "surrogate"),
    ("ghi_loi_theo_pha", "W4.mkstemp"): (OSError, _dau, "hop_dong"), ("ghi_loi_theo_pha", "W5.mkstemp"): (OSError, _dau, "hop_dong"),
    ("bien_cfgdir", "W4.cfg_la_tep"): (FileExistsError, lambda e: e.errno == errno.EEXIST, "hop_dong"),
}
class TinHieuChotCa(AssertionError):
    def __init__(self, ca, luot, nhan):
        super().__init__("%s · %s · %s" % (ca, luot, nhan)); self.ca, self.luot, self.nhan = ca, luot, nhan  # noqa: E702
def _nem(e):
    raise e
def _nap(nguon, tl_module, goc):
    """`compile`+`exec` nguồn vào module MỚI rồi `bind`; thay đường tải/cài bằng đồ giả CÓ ĐẾM (`m.dem`), kho Drive giả `m.drive`."""
    m = types.ModuleType("wp433_tl_gws"); m.__file__ = goc.__file__  # noqa: E702
    exec(compile(nguon, goc.__file__, "exec"), m.__dict__)
    m.bind(tl_module)
    m.dem, m.drive, that_imp = {}, {}, m._imp
    def gia(ten, tra):
        def f(*a, **k):
            m.dem[ten] = m.dem.get(ten, 0) + 1
            return tra(*a, **k) if callable(tra) else tra
        setattr(m, ten, f)
    gia("_public_curl_bytes", lambda fid, timeout=120.0: m.drive.get(fid)); gia("_secrets_fetch", lambda a, fid: (m.drive.get(fid), "gia"))  # noqa: E702
    gia("load_creds", None); gia("_gas", lambda: _nem(RuntimeError("MANG_BI_CHAN")))  # noqa: E702
    gia("_ensure_nlm_installed", (True, "gia")); gia("cmd_gws_bootstrap_cowork", 0)  # noqa: E702
    gia("_imp", lambda n: types.SimpleNamespace(gws_exe=lambda: "gws-gia") if n == "gws_bridge" else that_imp(n))
    m.AGENT_CREDS_FILEID = ""          # biến rỗng rơi về hằng baked ⇒ xoá cả hằng (agent giả KHÔNG CẤU HÌNH)
    return m
_ghi = lambda p, b: pathlib.Path(p).write_bytes(b)
_tep = lambda goc: sorted(os.path.join(d, t) for d, _ds, fs in os.walk(goc) if os.sep + ".git" not in d for t in fs)
_ac = lambda out: sum(d.startswith("[bootstrap] agent_creds:") for d in out.splitlines()) == 1
_rp = lambda p: re.escape(repr(p))
_dong = lambda err: [d for d in err if d.startswith("[bootstrap] ✗ ") and d != _D01]
def _doc(p):
    try:
        return pathlib.Path(p).read_bytes()
    except OSError:
        return None
def _sach(k):
    """sạch(K): không tệp nào ngoài `.git`, và `git status --porcelain` rỗng khi có git."""
    git = shutil.which("git") and subprocess.run(["git", "-C", k, "status", "--porcelain", "--untracked-files=all"], capture_output=True).stdout
    return not _tep(k) and not git
def _dung(err, cum, ct=".+"):
    """"stderr đúng (W4)": đúng MỘT dòng `[bootstrap] ✗ …` khác dòng §0.1, `fullmatch` `<cụm>: <chi tiết>` (một dòng)."""
    return len(_dong(err)) == 1 and re.fullmatch(r"\[bootstrap\] ✗ %s: %s" % (_CUM[cum], ct), _dong(err)[0]) is not None
def _ly(kq, cum, ct=".+"):
    """"W5 đúng": `(False, s)` với `s` `fullmatch` `<cụm>: <chi tiết>` (một dòng)."""
    return isinstance(kq, tuple) and len(kq) == 2 and kq[0] is False and isinstance(kq[1], str) and re.fullmatch("%s: %s" % (_CUM[cum], ct), kq[1]) is not None
def _tc(w, kq, err, cum, ct=".+"):
    return (kq == 1 and _dung(err, cum, ct)) if w == "W4" else _ly(kq, cum, ct)
def _probe_link(nguon, dich):
    """Phép thử hardlink trên CHÍNH thư mục fixture của lượt: None (tạo được) hoặc OSError đã bắt."""
    try:
        return os.link(nguon, dich)
    except OSError as e:
        return e
class _Rig:
    """Một ca: thư mục tạm `realpath` (không tổ tiên nào là symlink), HOME/USERPROFILE/CODEX_HOME/GOOGLE_WORKSPACE_CLI_CONFIG_DIR/TL_*/cwd
    đặt tạm, khôi phục khi ra. `so` là SỔ LƯỢT dùng chung: mỗi lượt ghi đúng một trạng thái (`đạt` · `đỏ` · `bỏ_qua`)."""
    def __init__(self, m, ca, store, so):
        self.m, self.ca, self.store, self.so, self.n, self.nk, self.ghi, self.xem = m, ca, store, so, 0, [], 0, None
    def __enter__(self):
        self.td, self.cu_env, self.cu_cwd = os.path.realpath(tempfile.mkdtemp(prefix="wp433g-")), dict(os.environ), os.getcwd()
        for k in [k for k in os.environ if k.startswith("TL_")] + ["CLAUDE_CODE_OAUTH_TOKEN", "GEMINI_API_KEY"]:
            os.environ.pop(k, None)
        os.makedirs(self.p("home"))
        os.environ.update(TL_MASTER_KEY=_MK, CODEX_HOME=self.p("cx"), HOME=self.p("home"), USERPROFILE=self.p("home"), GOOGLE_WORKSPACE_CLI_CONFIG_DIR=self.p("gws"))
        os.chdir(self.td); self.m.drive.clear()  # noqa: E702
        return self
    def __exit__(self, *a):
        os.chdir(self.cu_cwd); os.environ.clear(); os.environ.update(self.cu_env); shutil.rmtree(self.td, ignore_errors=True)  # noqa: E702
    p = lambda self, *a: os.path.join(self.td, *a)
    def moi(self, tao=True):
        """`cfgdir` MỚI ngoài mọi kho cho lượt kế (lượt sau không thấy tệp của lượt trước); trả (cfgdir, đích `credentials.json`)."""
        self.n += 1; c = self.p("c%d" % self.n); tao and os.makedirs(c)  # noqa: E702
        return c, os.path.join(c, "credentials.json")
    def kho(self, ten="K"):
        k = self.p(ten); os.makedirs(k)  # noqa: E702
        if not (shutil.which("git") and subprocess.run(["git", "init", "-q", k], capture_output=True).returncode == 0):
            os.makedirs(os.path.join(k, ".git"), exist_ok=True)
        return k
    def xs(self, luot, **nhan):
        """Kết thúc MỘT lượt: hậu điều đã thu đủ (đối số, theo thứ tự ghi); nhãn đỏ đầu tiên ⇒ `đỏ` + tín hiệu, không thì `đạt`."""
        hong = [n for n, dk in nhan.items() if not dk]
        self.so.append((self.ca, luot, "đỏ" if hong else "đạt", None))
        if hong:
            raise TinHieuChotCa(self.ca, luot, hong[0])
    def bo_qua(self, luot, e):
        """Bộ phân loại bỏ qua: chỉ nt + `winerror` thuộc danh sách cho phép ⇒ `bỏ_qua` kèm lý do; mọi lỗi probe khác ⇒ lượt `đỏ`."""
        if not (_TEN_OS == "nt" and getattr(e, "winerror", None) in _WINERR):
            self.so.append((self.ca, luot, "đỏ", None))
            raise TinHieuChotCa(self.ca, luot, "probe hardlink: %r" % ((type(e).__name__, e.errno, getattr(e, "winerror", None)),))
        self.so.append((self.ca, luot, "bỏ_qua", e))
        return True
    def goi(self, luot, fn, pha=None):
        """Một LƯỢT GỌI. Cửa sổ: chặn tiến trình con/mạng (`MANG_BI_CHAN`), stdout/stderr RIÊNG, bộ quan sát bọc `mkstemp`/`fsync`/`chmod`/
        `replace` và writer — chỉ ghi nhật ký `self.nk` (và tiêm `OSError` ở ĐÚNG `pha`) cho đích `credentials.json` trong `self.xem`;
        `self.ghi` đếm lời gọi writer có đích ấy. Ngoại lệ khớp tập khai CỦA LƯỢT ⇒ nhãn khai; ngoài tập ⇒ `ngoai_le_la`."""
        out, err, kq, m, fds, xem = io.StringIO(), io.StringIO(), None, self.m, {}, self.xem
        self.nk, self.ghi = [], 0
        cu = (subprocess.run, subprocess.Popen, urllib.request.urlopen, tempfile.mkstemp, os.fsync, os.chmod, os.replace, m._ghi_nguyen_tu_0600)
        subprocess.run = subprocess.Popen = urllib.request.urlopen = lambda *a, **k: _nem(RuntimeError("MANG_BI_CHAN"))
        def tiem(p, khoa):
            if pha == p:
                self.nk.append(("tiem", p, khoa, "wp433-oserror-" + p))
                raise OSError("wp433-oserror-" + p)
        def mk(*a, **k):
            if k.get("dir") != xem:
                return cu[3](*a, **k)
            tiem("mkstemp", xem)
            fd, tmp = cu[3](*a, **k); fds[fd] = tmp; self.nk.append(("mkstemp", fd, tmp))  # noqa: E702
            return fd, tmp
        def fs(fd):
            if fd in fds:
                tiem("fsync", fd); self.nk.append(("fsync", fd))  # noqa: E702
            return cu[4](fd)
        def ch(p, *a, **k):
            if isinstance(p, str) and os.path.dirname(p) == xem:
                tiem("chmod", xem)
            return cu[5](p, *a, **k)
        def rp(s, d):
            if xem and d == os.path.join(xem, "credentials.json"):
                tiem("replace", xem); self.nk.append(("replace", s, stat.S_IMODE(os.stat(s).st_mode)))  # noqa: E702
            return cu[6](s, d)
        def wr(path, data):
            self.ghi += os.path.basename(path) == "credentials.json"
            return cu[7](path, data)
        tempfile.mkstemp, os.fsync, os.chmod, os.replace, m._ghi_nguyen_tu_0600 = mk, fs, ch, rp, wr
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                kq = fn()
        except Exception as e:  # noqa: BLE001 — biên của lượt: chỉ tập ĐÓNG đã khai mới thành nhãn đích
            lo, khop, nhan = _KHAI.get((self.ca, luot), (None, None, ""))
            self.so.append((self.ca, luot, "đỏ", None))
            raise TinHieuChotCa(self.ca, luot, nhan if lo and isinstance(e, lo) and khop(e) else "ngoai_le_la") from e
        finally:
            subprocess.run, subprocess.Popen, urllib.request.urlopen, tempfile.mkstemp, os.fsync, os.chmod, os.replace, m._ghi_nguyen_tu_0600 = cu
        return kq, out.getvalue(), [d for d in err.getvalue().splitlines() if d]
    def w(self, luot, cfg, cred=_CRED, req=False, cli=False, pha=None):
        """Lượt W4 (tên lượt bắt đầu `W4`: fixture gws chuẩn — `bootstrap --env code --no-nlm --no-gws`, bundle có token + gws_cred, agent
        KHÔNG CẤU HÌNH, gws_exe giả) hoặc W5 (`_gws_auth_load`; `cli` ⇒ `cmd_gws_auth_load`). `cfg` là giá trị THÔ của biến môi trường."""
        os.environ["GOOGLE_WORKSPACE_CLI_CONFIG_DIR"], self.xem, m = cfg, cfg, self.m
        if luot.startswith("W4") or luot.startswith("N6") or luot == "require":
            m.drive["S433"] = self.store.encrypt(json.dumps({"token": _TOK, "gws_cred": cred}).encode("utf-8"), _MK)
            ns = argparse.Namespace(secrets_id="S433", secrets_file=None, env="code", config=None, profile=None, no_gws=True, no_nlm=True, bindir=None, require_agent_creds=req)
            return self.goi(luot, lambda: m.cmd_bootstrap(ns), pha)
        m.drive["G433"] = self.store.encrypt(_CRED.encode("utf-8"), _TOK); os.environ["TL_TOKEN"] = _TOK  # noqa: E702
        ns = argparse.Namespace(config=None, profile=None, cred_file_id="G433")
        return self.goi(luot, (lambda: m.cmd_gws_auth_load(ns)) if cli else (lambda: m._gws_auth_load(_TOK, "G433")), pha)
    def n5(self, d):
        """Ba nhãn đầu của N5, đọc từ nhật ký: đúng MỘT `replace` vào đích, nguồn là tệp `mkstemp` cùng thư mục; `fsync` đúng fd của nguồn
        TRƯỚC `replace` ấy; (POSIX) nguồn `0600` lúc thay và đích `0600` sau cùng."""
        rp, mk = [x for x in self.nk if x[0] == "replace"], {x[2]: x[1] for x in self.nk if x[0] == "mkstemp"}
        mot = len(rp) == 1 and rp[0][1] in mk
        quyen = os.name != "posix" or (mot and rp[0][2] == 0o600 and os.path.isfile(d) and stat.S_IMODE(os.stat(d).st_mode) == 0o600)
        return {"nguyen_tu": mot, "fsync": mot and ("fsync", mk[rp[0][1]]) in self.nk[:self.nk.index(rp[0])], "quyen": quyen}
def trong_kho(r):
    for w in ("W4", "W5"):
        k = r.kho("K" + w); c = os.path.join(k, "gwscfg")  # noqa: E702
        kq, out, err = r.w(w, c)
        r.xs(w, sach=not os.path.lexists(c) and _sach(k), ma=kq == 1 if w == "W4" else isinstance(kq, tuple) and kq[0] is False,
             stderr=_dung(err, "kho") if w == "W4" else _ly(kq, "kho"), agent_creds=w == "W5" or _ac(out), khong_lo=_SENT not in out + "\n".join(err) + repr(kq))
def goc_bieu_dien(r):
    that, a = r.p("that"), r.p("alias"); os.makedirs(that); os.makedirs(r.p("x")); os.symlink(that, a, target_is_directory=True)  # noqa: E702
    for i, c in enumerate((a, a + "/", a + "/.", "alias", "alias/", "alias/.")):
        kq, _o, _e = r.w("W5.goc_%d" % i, c)
        r.xs("W5.goc_%d" % i, **{"goc_%d" % i: _ly(kq, "lk") and not os.listdir(that)})
    kq, _o, _e = r.w("W5.hai_cham", "x/../that")
    r.xs("W5.hai_cham", hai_cham=_ly(kq, "dg"))
    kq, _o, _e = r.w("W5.tuong_doi_thuong", "cfgthuong"); d = r.p("cfgthuong", "credentials.json")  # noqa: E702
    r.xs("W5.tuong_doi_thuong", tuong_doi_thuong=kq == (True, d) and _doc(d) == _CRED.encode("utf-8"))
    kq, _o, err = r.w("W4.goc_w4", a + "/.")
    r.xs("W4.goc_w4", goc_w4=_tc("W4", kq, err, "lk") and not os.listdir(that))
def to_tien(r):
    b, dj, (c, d) = r.p("thuc", "a", "b"), r.p("dich.json"), r.moi(); os.makedirs(b); _ghi(dj, _CU); os.symlink(dj, d)  # noqa: E702
    for ten, dich in (("lk", r.p("thuc")), ("lk2", r.p("thuc", "a")), ("lk3", b)):
        os.symlink(dich, r.p(ten), target_is_directory=True)
    for luot, cfg, lk in (("W4.ong", r.p("lk", "a", "b"), r.p("lk")), ("W5.ong", r.p("lk", "a", "b"), r.p("lk")), ("W5.cha", r.p("lk2", "b"), r.p("lk2")),
                          ("W5.goc_cfg", r.p("lk3"), r.p("lk3")), ("W4.tep_cuoi", c, d), ("W5.tep_cuoi", c, d)):   # `lk` = ĐÚNG thành phần là liên kết
        kq, _o, err = r.w(luot, cfg)
        r.xs(luot, lien_ket=_tc(luot[:2], kq, err, "lk", _rp(lk)), khong_ghi=not _tep(r.p("thuc")) and _doc(dj) == _CU)
def chuoi_kho(r):
    k, t = r.kho(), r.p("T"); os.makedirs(os.path.join(k, "sub")); os.makedirs(t); os.symlink(os.path.join(k, "sub"), r.p("L"), target_is_directory=True)  # noqa: E702
    kq, _o, _e = r.w("realpath", r.p("L", "gws"))            # L NGOÀI kho trỏ vào K/sub: luật (a) chạy trước luật (b)
    r.xs("realpath", kho_truoc=_ly(kq, "kho") and _sach(k))
    os.symlink(t, os.path.join(k, "lk"), target_is_directory=True)
    kq, _o, _e = r.w("tu_vung", os.path.join(k, "lk", "gws"))  # lk TRONG kho trỏ ra T
    r.xs("tu_vung", tu_choi_tu_vung=_ly(kq, "kho") and not os.listdir(t))
def duong_xuong_dong(r):
    k = r.kho("k\nho"); c = os.path.join(k, "gws")  # noqa: E702
    kq, _o, err = r.w("W5.cli", c, cli=True)
    r.xs("W5.cli", mot_dong=kq == 2 and err == ["[gws-auth-load] ✗ nằm trong kho git: " + repr(k)])
    kq, _o, err = r.w("W4.bootstrap", c)
    r.xs("W4.bootstrap", mot_dong_w4=_tc("W4", kq, err, "kho", _rp(k)))
def m1_bien(r):
    for luot, nhan, ps in (("nul", "nul", ("a\x00b",)), ("trang", "trang", ("   ",)), ("goc", "goc_rong", ("/", "/./")), ("xuong_dong", "mot_dong_m1", ("x\n/..",))):
        kq, _o, _e = r.goi(luot, lambda: [r.m._duong_dich_chuan(p, "/c") for p in ps])
        r.xs(luot, **{nhan: all(isinstance(s, str) and re.fullmatch(_CUM["dg"] + ": .+", s) for s in kq)})
def bien_cfgdir(r):
    for dang, loi, so_mk in (("cfg_la_tep", "FileExistsError", 0), ("dich_la_thu_muc", "IsADirectoryError", 1)):
        for w in ("W4", "W5"):
            (c, d), la_tep = r.moi(tao=dang != "cfg_la_tep"), dang == "cfg_la_tep"
            _ghi(c, _CU) if la_tep else os.makedirs(d)
            kq, _o, err = r.w("%s.%s" % (w, dang), c)
            con = _doc(c) == _CU if la_tep else os.listdir(c) == ["credentials.json"] and os.path.isdir(d) and not os.listdir(d)
            r.xs("%s.%s" % (w, dang), hop_dong=_tc(w, kq, err, "ghi", loi), nguyen_trang=con and r.ghi == 1 and sum(x[0] == "mkstemp" for x in r.nk) == so_mk)
def nguyen_tu(r):
    du = lambda w, kq, out, d: _doc(d) == _CRED.encode("utf-8") and ((kq == 0 and "[bootstrap] ✓ gws cred → " in out) if w == "W4" else kq == (True, d))
    for w in ("W4", "W5"):
        c, d = r.moi(); _ghi(d, _CU)  # noqa: E702
        kq, out, _e = r.w(w + ".thuong", c)
        r.xs(w + ".thuong", **r.n5(d), byte=du(w, kq, out, d))
    (c, d), h = r.moi(), r.p("H"); _ghi(h, _CU); e = _probe_link(h, d)  # noqa: E702
    if e is not None and r.bo_qua("W5.hardlink", e):
        return
    kq, out, _e = r.w("W5.hardlink", c)
    r.xs("W5.hardlink", **r.n5(d), byte=du("W5", kq, out, d), ban_kia_giu=_doc(h) == _CU)
def du_lieu_sai_dang(r):
    for luot, nhan, cred in (("N6.kieu", "kieu", 5), ("N6.surrogate", "surrogate", "\ud800"), ("N6.falsy", "falsy", 0)):
        c, _d = r.moi(tao=False); kq, _o, err = r.w(luot, c, cred=cred)  # noqa: E702
        r.xs(luot, **{nhan: _tc("W4", kq, err, "dl") and not os.path.lexists(c) and r.ghi == 0})
def ghi_loi_theo_pha(r):
    for luot in _LUOT_DU_KIEN["ghi_loi_theo_pha"]:
        (c, d), cli = r.moi(), luot == "W5.cli"; pha = "replace" if cli else luot[3:]; _ghi(d, _CU)  # noqa: E702
        kq, out, err = r.w(luot, c, cli=cli, pha=pha)
        tiem, khoa = [x for x in r.nk if x[0] == "tiem"], ([x[1] for x in r.nk if x[0] == "mkstemp"] + [None])[0] if pha == "fsync" else c
        hd = (kq == 2 and err == ["[gws-auth-load] ✗ ghi lỗi: OSError"]) if cli else _tc(luot[:2], kq, err, "ghi", "OSError") and "✓ gws cred" not in out
        r.xs(luot, tiem=tiem == [("tiem", pha, khoa, "wp433-oserror-" + pha)], hop_dong=hd, ban_cu=_doc(d) == _CU, khong_tam=os.listdir(c) == ["credentials.json"])
def chung_hop_dong_loi(r):
    c = os.path.join(r.kho(), "gwscfg"); kq, out, err = r.w("W4.trong_kho", c); ds = _dong(err)  # noqa: E702
    r.xs("W4.trong_kho", mot_dong_loi=kq == 1 and len(ds) == 1, mau_loi=len(ds) == 1 and re.fullmatch(_M3, ds[0]) is not None)
    kq, out, err = r.w("require", c, req=True)
    r.xs("require", require=kq == 4 and _dung(err, "kho") and _ac(out), dong_0_1=err.count(_D01) == 1)
_CA = ((trong_kho, "posix"), (goc_bieu_dien, "posix"), (to_tien, "posix"), (chuoi_kho, "posix"), (duong_xuong_dong, "posix"), (m1_bien, "mọi"),
       (bien_cfgdir, "posix"), (nguyen_tu, "mọi"), (du_lieu_sai_dang, "mọi"), (ghi_loi_theo_pha, "mọi"), (chung_hop_dong_loi, "posix"))
_DU_KIEN = (  # N9(a): danh sách ID đột biến dự kiến (§4b, 37 mục) — viết RIÊNG khỏi `_DB`
    "db_w4_bo_chot", "db_w5_bo_chot", "db_w4_quen_degraded", "db_lstat_tho", "db_bo_cam_hai_cham", "db_ghi_duong_tho", "db_chi_tu_vung", "db_chi_realpath",
    "db_bo_symlink_cuoi", "db_w4_khong_nguyen_tu", "db_w5_khong_nguyen_tu", "db_w4_bo_kiem_kieu", "db_w4_bo_kiem_encode", "db_w4_mau_loi", "db_w4_oserror_lan",
    "db_w5_oserror_lan", "db_khong_repr_gws", "db_require_thua_rc1", "db_goc_cfgdir", "db_bo_fsync", "db_bo_don_tam", "db_ghi_xuyen_hardlink", "db_nhan_nul",
    "db_nhan_khoang_trang", "db_nhan_goc", "db_w4_oserror_hep", "db_w4_lap_dong", "db_m1_khong_repr", "db_sai_quyen", "db_w4_sai_byte", "db_require_thieu_dong",
    "db_require_lap_dong", "db_w4_lap_agent_creds", "db_w4_lo_sent", "db_w4_ghi_lai_khi_loi", "db_cat_dich_truoc", "db_w4_dieu_kien_truthy")
_DB_POSIX = {"db_sai_quyen"}   # §4b cột nền: `posix` dù ca đích là `mọi` (nhãn `quyen` chỉ đo trên POSIX)
_G4, _G5, _P4 = "_ghi_nguyen_tu_0600(dest, du_lieu)", "_ghi_nguyen_tu_0600(dest, cred)", 'print(f"[bootstrap] ✗ {ly_gws}", file=sys.stderr)'
_L4, _GHI_CU = _P4 + "; degraded = True", '(os.makedirs(os.path.dirname(dest), exist_ok=True), open(dest, "wb").write(%s), os.chmod(dest, 0o600))'
_C4, _C5, _TRA5 = "dest, ly_gws = _dich_cred_gws(cfgdir)", "dest, ly_do = _dich_cred_gws(cfgdir)", "else (True, dest)"
_VAO, _AC = '            gws_cred, dest = bundle["gws_cred"], None\n', '    print(f"[bootstrap] agent_creds: {ac} — {ac_ct}")\n'
_EX4 = '            except OSError as e:\n                ly_gws = f"ghi lỗi: {_safe_exc(e)}"\n'
_EX5 = '    except OSError as e:\n        ly_do = f"ghi lỗi: {_safe_exc(e)}"\n    return (False'
_KDG, _HC, _XAU = '_kiem_dich_ghi(dest, "/", (*chuan[1], "credentials.json"))', 'return ly if not tp or ".." in tp else', 'if "\\x00" in p or p.strip() == "":'
_KHO, _REQ = "(kho_dich := _trong_kho_git(os.path.dirname(dich)))", '    if getattr(a, "require_agent_creds", False) and ac != "ĐÃ NẠP":'
_MOT_CHUOI = '(kho_dich := next((x for x in (lambda d: [d] + [str(q) for q in Path(d).parents])(os.path.%s(os.path.dirname(dich))) if os.path.lexists(os.path.join(x, ".git"))), None))'
_IN01, _CHR = '        print("%s", file=sys.stderr)\n' % _D01, "        os.chmod(tmp, 0o600)\n        os.replace(tmp, path)\n"
_MKS, _OS_LAN = '    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".auth.json.")\n', [(_EX4, _EX4.replace("OSError", "ZeroDivisionError"))]
_DB = (  # §4b: (đột biến, [(neo khớp ĐÚNG MỘT lần, thay)…], ca đích, lượt, nhãn)
    ("db_w4_bo_chot", [(_C4, _C4 + "[0], None")], "trong_kho", "W4", "sach"),
    ("db_w5_bo_chot", [(_C5, _C5 + "[0], None")], "trong_kho", "W5", "sach"),
    ("db_w4_quen_degraded", [(_L4, _P4)], "trong_kho", "W4", "ma"),
    ("db_lstat_tho", [(_KDG, '_kiem_dich_ghi(os.path.join(cfgdir_tho, "credentials.json"), cfgdir_tho, ("credentials.json",))')], "goc_bieu_dien", "W5.goc_1", "goc_1"),
    ("db_bo_cam_hai_cham", [(_HC, "return ly if not tp else")], "goc_bieu_dien", "W5.hai_cham", "hai_cham"),
    ("db_ghi_duong_tho", [(_TRA5, 'else (True, os.path.join(cfgdir, "credentials.json"))')], "goc_bieu_dien", "W5.tuong_doi_thuong", "tuong_doi_thuong"),
    ("db_chi_tu_vung", [(_KHO, _MOT_CHUOI % "abspath")], "chuoi_kho", "realpath", "kho_truoc"),
    ("db_chi_realpath", [(_KHO, _MOT_CHUOI % "realpath")], "chuoi_kho", "tu_vung", "tu_choi_tu_vung"),
    ("db_bo_symlink_cuoi", [("for i in range(len(thanh_phan) + 1):", "for i in range(len(thanh_phan)):")], "to_tien", "W4.tep_cuoi", "lien_ket"),
    ("db_w4_khong_nguyen_tu", [(_G4, _GHI_CU % "du_lieu")], "nguyen_tu", "W4.thuong", "nguyen_tu"),
    ("db_w5_khong_nguyen_tu", [(_G5, _GHI_CU % "cred")], "nguyen_tu", "W5.thuong", "nguyen_tu"),
    ("db_w4_bo_kiem_kieu", [('gws_cred.encode("utf-8") if isinstance(gws_cred, str) else None', 'gws_cred.encode("utf-8")')], "du_lieu_sai_dang", "N6.kieu", "kieu"),
    ("db_w4_bo_kiem_encode", [("            except UnicodeEncodeError:\n", "            except ZeroDivisionError:\n")], "du_lieu_sai_dang", "N6.surrogate", "surrogate"),
    ("db_w4_mau_loi", [(_L4, 'print("[bootstrap] ✗ nằm trong kho git: ", file=sys.stderr); degraded = True')], "chung_hop_dong_loi", "W4.trong_kho", "mau_loi"),
    ("db_w4_oserror_lan", _OS_LAN, "ghi_loi_theo_pha", "W4.mkstemp", "hop_dong"),
    ("db_w5_oserror_lan", [(_EX5, _EX5.replace("OSError", "ZeroDivisionError"))], "ghi_loi_theo_pha", "W5.mkstemp", "hop_dong"),
    ("db_khong_repr_gws", [("{repr(kho_dich)[:200]}", "{kho_dich}")], "duong_xuong_dong", "W5.cli", "mot_dong"),
    ("db_require_thua_rc1", [(_REQ, "    if degraded:\n        return 1\n" + _REQ)], "chung_hop_dong_loi", "require", "require"),
    ("db_goc_cfgdir", [(_KDG, '_kiem_dich_ghi(dest, chuan[0], ("credentials.json",))')], "to_tien", "W4.ong", "lien_ket"),
    ("db_bo_fsync", [("f.write(data); f.flush(); os.fsync(f.fileno())", "f.write(data); f.flush()")], "nguyen_tu", "W4.thuong", "fsync"),
    ("db_bo_don_tam", [("        if os.path.exists(tmp):\n            os.unlink(tmp)\n        raise\n", "        raise\n")], "ghi_loi_theo_pha", "W4.fsync", "khong_tam"),
    ("db_ghi_xuyen_hardlink", [(_CHR, _CHR.replace("        os.replace", '        if os.path.exists(path):\n            with open(path, "r+b") as g:\n                g.write(data)\n        os.replace'))],
     "nguyen_tu", "W5.hardlink", "ban_kia_giu"),
    ("db_nhan_nul", [(_XAU, 'if p.strip() == "":')], "m1_bien", "nul", "nul"),
    ("db_nhan_khoang_trang", [(_XAU, 'if "\\x00" in p:')], "m1_bien", "trang", "trang"),
    ("db_nhan_goc", [(_HC, 'return ly if ".." in tp else')], "m1_bien", "goc", "goc_rong"),
    ("db_w4_oserror_hep", [(_EX4, _EX4.replace("OSError", "FileNotFoundError"))], "bien_cfgdir", "W4.cfg_la_tep", "hop_dong"),
    ("db_w4_lap_dong", [(_L4, _P4 + "; " + _L4)], "chung_hop_dong_loi", "W4.trong_kho", "mot_dong_loi"),
    ("db_m1_khong_repr", [('ly = f"đường không hợp lệ: {repr(p)[:200]}"', 'ly = f"đường không hợp lệ: {p}"')], "m1_bien", "xuong_dong", "mot_dong_m1"),
    ("db_sai_quyen", [(_CHR, _CHR.replace("0o600", "0o644"))], "nguyen_tu", "W4.thuong", "quyen"),
    ("db_w4_sai_byte", [(_G4, '_ghi_nguyen_tu_0600(dest, du_lieu + b"\\n")')], "nguyen_tu", "W4.thuong", "byte"),
    ("db_require_thieu_dong", [(_IN01, "")], "chung_hop_dong_loi", "require", "dong_0_1"),
    ("db_require_lap_dong", [(_IN01, _IN01 + _IN01)], "chung_hop_dong_loi", "require", "dong_0_1"),
    ("db_w4_lap_agent_creds", [(_AC, _AC + _AC)], "trong_kho", "W4", "agent_creds"),
    ("db_w4_lo_sent", [(_VAO, _VAO + '            print(f"[bootstrap] gws_cred={repr(gws_cred)[:200]}")\n')], "trong_kho", "W4", "khong_lo"),
    ("db_w4_ghi_lai_khi_loi", [(_EX4, _EX4 + "                try:\n                    %s\n                except OSError:\n                    pass\n" % _G4)], "bien_cfgdir", "W4.cfg_la_tep", "nguyen_trang"),
    ("db_cat_dich_truoc", [(_MKS, '    open(path, "wb").close()\n' + _MKS)], "ghi_loi_theo_pha", "W4.mkstemp", "ban_cu"),
    ("db_w4_dieu_kien_truthy", [('if "gws_cred" in bundle and bundle["gws_cred"] != "":', 'if bundle.get("gws_cred"):')], "du_lieu_sai_dang", "N6.falsy", "falsy"),
)
_DOI_KIEU = ('            try:\n                raise AttributeError("wp433-tu-kiem")\n            except Exception as e:\n'
             '                raise AssertionError(f"wp433-tu-kiem {type(e).__name__}")\n')
_TU_KIEM = (  # N9(d): bộ phân hạng KHÔNG được cấp tín dụng — (tên, cặp, ca, lượt, nhãn, hạng mong đợi)
    ("tu_kiem_doi_kieu", [(_VAO, _VAO + _DOI_KIEU)], "du_lieu_sai_dang", "N6.kieu", "kieu", "TIN_DUNG_GIA"),
    ("tu_kiem_chu_thich", [("\ndef _dich_cred_gws(", "\n# vô hại\ndef _dich_cred_gws(")], "du_lieu_sai_dang", "N6.kieu", "kieu", "SONG_SOT"),
    ("tu_kiem_sai_luot", _OS_LAN, "ghi_loi_theo_pha", "W4.fsync", "hop_dong", "TIN_DUNG_GIA"),   # CHÍNH db_w4_oserror_lan, chỉ đổi lượt khai
)
def _chay(m, store, ca, so):
    with _Rig(m, ca.__name__, store, so) as r:
        ca(r)
def _hang(nguon, tl_module, goc, store, cap, ca, luot, nhan):
    """Phân hạng MỘT đột biến trên bản sao trong bộ nhớ, trả (hạng, ngoại lệ): HONG (neo ≠ 1 lần / không nạp được) · SONG_SOT · BO_QUA
    (lượt đích được bỏ qua hợp lệ) · GIET (đúng lớp tín hiệu, đúng ca, đúng lượt, đúng nhãn) · TIN_DUNG_GIA (chết vì lý do khác)."""
    for neo, thay in cap:
        if nguon.count(neo) != 1 or neo == thay:
            return "HONG", None
        nguon = nguon.replace(neo, thay)
    try:
        m = _nap(nguon, tl_module, goc)
    except Exception as e:  # noqa: BLE001
        return "HONG", e
    so = []
    try:
        _chay(m, store, next(c for c, _n in _CA if c.__name__ == ca), so)
    except TinHieuChotCa as e:
        return ("GIET" if (e.ca, e.luot, e.nhan) == (ca, luot, nhan) else "TIN_DUNG_GIA"), e
    except BaseException as e:  # noqa: BLE001 — kể cả StopIteration khi ca đích không còn trong bảng ca
        return "TIN_DUNG_GIA", e
    return ("BO_QUA" if (ca, luot, "bỏ_qua") in [x[:3] for x in so] else "SONG_SOT"), None
def _run(tl_module):
    goc = tl_module._imp("tl_gws"); goc.bind(tl_module)  # noqa: E702
    nguon, store, posix = pathlib.Path(goc.__file__).read_text(encoding="utf-8"), tl_module._imp("gws_cred_store"), os.name == "posix"
    m, so, b, c, nen = _nap(nguon, tl_module, goc), [], 0, 0, {ca.__name__: n for ca, n in _CA}
    for ca, n in _CA:
        if n == "posix" and not posix:
            so += [(ca.__name__, luot, "chỉ_posix", None) for luot in _LUOT_DU_KIEN.get(ca.__name__, ())]
            continue
        b += 1
        try:
            _chay(m, store, ca, so); c += 1  # noqa: E702
        except Exception as e:  # noqa: BLE001
            print("[%s] ĐỎ %s: %r (%r)" % (TEST_ID, ca.__name__, e, e.__cause__), file=sys.stderr)
    for x in so:
        if x[2] == "bỏ_qua":
            print("[%s] BO_QUA %s·%s: %r" % (TEST_ID, x[0], x[1], x[3]), file=sys.stderr)
    kq = {d[0]: "CHI_POSIX" if not posix and (nen.get(d[2]) == "posix" or d[0] in _DB_POSIX) else _hang(nguon, tl_module, goc, store, *d[1:])[0] for d in _DB}
    tk = [(d[0], d[5]) + _hang(nguon, tl_module, goc, store, *d[1:5]) for d in _TU_KIEM]
    doi = lambda e: isinstance(getattr(getattr(e, "__cause__", None), "__context__", None), AttributeError)   # đã đi qua `except` đổi kiểu
    k = sum(h == mong and (ten != "tu_kiem_doi_kieu" or doi(e)) for ten, mong, h, e in tk)
    for ten, hang in list(kq.items()) + [(ten, "tự kiểm %s ≠ %s" % (h, mong)) for ten, mong, h, _e in tk if h != mong]:
        if hang not in ("GIET", "CHI_POSIX", "BO_QUA"):
            print("[%s] ĐỘT BIẾN %s: %s" % (TEST_ID, ten, hang), file=sys.stderr)
    dem, hg = lambda tt: sum(x[2] == tt for x in so), lambda tt: sum(h == tt for h in kq.values())
    a, w, x, y, z, u, t = len(_LUOT_DU_KIEN), len(_CA) - b, sum(map(len, _LUOT_DU_KIEN.values())), dem("đạt") + dem("đỏ"), dem("đạt"), dem("bỏ_qua"), dem("chỉ_posix")
    e, g, h, v, i = len(_DB), hg("GIET"), hg("BO_QUA"), hg("CHI_POSIX"), hg("HONG"); f, bq = e - h - v, [s for s in so if s[2] == "bỏ_qua"]  # noqa: E702
    print("[%s] CA: dự_kiến=%d chạy=%d đạt=%d bỏ_qua=0 chỉ_posix=%d · LUOT: dự_kiến=%d chạy=%d đạt=%d bỏ_qua=%d chỉ_posix=%d · DOT BIEN: dự_kiến=%d chạy=%d "
          "giết_đúng=%d bỏ_qua=%d chỉ_posix=%d · HONG: %d · TU_KIEM: %d/%d" % (TEST_ID, a, b, c, w, x, y, z, u, t, e, f, g, h, v, i, k, len(_TU_KIEM)), file=sys.stderr)
    ve = {"ca_dat": b == c, "luot_dat": y == z, "giet_dung": f == g, "hong": i == 0, "so_ca": a == b + w, "tu_kiem": k == len(_TU_KIEM),
          "so_luot": x == y + u + t == 46 and sorted(s[:2] for s in so) == sorted((ca, luot) for ca, ds in _LUOT_DU_KIEN.items() for luot in ds),
          "so_dot_bien": e == len(_DU_KIEN) and sorted(d[0] for d in _DB) == sorted(_DU_KIEN),
          "bo_qua_trong_ds": all(s[:2] == _BO_QUA_DUOC for s in bq) and u <= 1 and h == u,
          "bo_qua_co_can_cu": all(_TEN_OS == "nt" and isinstance(s[3], OSError) and getattr(s[3], "winerror", None) in _WINERR for s in bq),
          "nen": u == h == w == t == v == 0 if posix else (w, t, v) == (7, 27, 21)}
    if not all(ve.values()):
        print("[%s] VẾ SAI: %s" % (TEST_ID, ", ".join(n for n, dk in ve.items() if not dk)), file=sys.stderr)
    return all(ve.values())
def run(tl_module):
    ra = io.StringIO()                      # N9(f): fragment in mọi thứ ra STDERR (driver bundle đọc stdout làm JSON)
    with contextlib.redirect_stdout(ra):
        ok = _run(tl_module)
    return ok and not ra.getvalue()
