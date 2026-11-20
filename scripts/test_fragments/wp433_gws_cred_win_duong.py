# -*- coding: utf-8 -*-
"""wp433 P2c-C1 — trên Windows `credentials.json` của gws (W4 `bootstrap`, W5 `_gws_auth_load` trong `tl_gws.py`) chỉ ghi tới đường ổ CỤC
BỘ thuộc danh sách cho phép, ngoài kho git, không xuyên liên kết; UNC và ổ mạng bị từ chối (spec GWS-CRED-DICH-NGOAI-KHO-C1 r1). Mọi ca
chạy trên bản `tl_gws` nạp TRONG BỘ NHỚ (nguồn thật hoặc đột biến), HOME/cfgdir tạm, dữ liệu GIẢ, không mạng. Mỗi LƯỢT thu đủ hậu điều
rồi so nhãn; nhãn đỏ ĐẦU TIÊN thành `TinHieuChotCa(ca, lượt, nhãn)` — đột biến chỉ GIẾT khi khớp cả ba (bảng `_DB` chép §4b của spec)."""
import argparse, contextlib, io, json, os, pathlib, shutil, subprocess, sys, tempfile, types, urllib.request  # noqa: E401
TEST_ID = "wp433_gws_cred_win_duong"
_MK, _TOK, _CRED, _O = "wp433-master-gia", "wp433-token-gia", '{"gia": "SENTINEL-wp433-c1-gia"}', "C:\\"
_DG, _KHO, _LK, _W4 = "đường không hợp lệ: ", "nằm trong kho git: ", "là liên kết tượng trưng: ", "[bootstrap] ✗ "
_TEN_OS, _BO_QUA_DUOC, _P, _Q, _W = os.name, ("W5.sl_to_tien", "W5.sl_treo"), "phan_loai_nt", "chuan_nt", "tich_hop_nt"
_LUOT_DU_KIEN = {  # N4(b) SỔ LƯỢT — viết RIÊNG khỏi các hàm ca và bảng dữ liệu: 3 ca, 47 + 18 + 11 = 76 lượt, đúng thứ tự §4
    _P: tuple("p%02d" % i for i in range(1, 48)), _Q: tuple("q%02d" % i for i in range(1, 19)),
    _W: ("W5.trong_kho", "W4.trong_kho", "W5.tuong_doi", "W5.o_tuong_doi", "W5.unc", "W5.sl_to_tien", "W5.sl_treo", "W5.loai_o_loi", "W4.loai_o_loi", "W5.git_loi", "W5.realpath_loi"),
}
_N1 = (  # N1 p01…p47: (đầu vào, mã từ chối) hoặc (đầu vào, gốc, thành phần) — loại nhận là `tuong_doi` khi gốc None, ngược lại `o_tuyet_doi`
    (r"C:\x", _O, ("x",)), ("C:/x", _O, ("x",)), (r"c:\x", _O, ("x",)), (r"C:\a/b\c", _O, ("a", "b", "c")), ("fake", None, ("fake",)), ("C:\\x\\.\\y\\\\", _O, ("x", "y")),
    (r"D:\Quốc hội\tra-luat", "D:\\", ("Quốc hội", "tra-luat")), (r"C:\ a", _O, (" a",)), ("a\x00b", "nul"), ("   ", "trang"), (r"\\?\C:\x", "thiet_bi_win32"),
    ("//?/C:/x", "thiet_bi_win32"), (r"\\?\UNC\s\sh", "thiet_bi_win32"), (r"\\.\pipe\x", "thiet_bi_dos"), ("//./C:/x", "thiet_bi_dos"), (r"\??\C:\x", "nt_doi_tuong"),
    ("C:", "o_tran"), ("D:fake", "o_tuong_doi"), (r"\fake", "goc_o"), ("/fake", "goc_o"), (r"\\server\share\x", "unc"), ("//server/share/x", "unc"), (r"/\server\share\x", "unc"),
    (r"\\server", "unc"), (r"\\\server\share", "unc"), (r"\\server\\share", "unc"), (r"1:\x", "o_khac"), (r"C:\a\..\b", "hai_cham"), ("a/../b", "hai_cham"), ("..", "hai_cham"),
    (r"C:\x:ads", "ky_tu_cam"), (r"C:\a|b", "ky_tu_cam"), ("C:\\a\ud800b", "ky_tu_cam"), ("C:\\a\x01b", "ky_tu_cam"), (r"C:\a.\b", "cuoi_cham_cach"), ("C:\\a ", "cuoi_cham_cach"),
    (r"C:\CON", "ten_thiet_bi"), (r"C:\nul.txt", "ten_thiet_bi"), (r"C:\com1\x", "ten_thiet_bi"), (r"C:\NUL .txt", "ten_thiet_bi"), (r"C:\CONIN$", "ten_thiet_bi"),
    (r"C:\COM0", "ten_thiet_bi"), (r"C:\a<.", "ky_tu_cam"), ("C:\\CON.x ", "cuoi_cham_cach"), ("C:\\a\x7fb\u00a0", _O, ("a\x7fb\u00a0",)), (r"C:\COM¹", "ten_thiet_bi"),
    (r"C:\CONOUT$", "ten_thiet_bi"))
_CW, _DAI, _r = r"C:\cwd", "D:" + "a" * 300, lambda x: repr(x)[:200]
_N2 = (  # N2 q01…q18: (p, cwd, loại ổ giả, nhãn, kết quả | `x` của lý do `"đường không hợp lệ: " + repr(x)[:200]`)
    ("fake", _CW, 3, "ket_qua", (_O, ("cwd", "fake"))), (r"a\b", "c:/cwd", 3, "ket_qua", (_O, ("cwd", "a", "b"))), ("fake", r"\\s\sh\d", 3, "ly_do", r"\\s\sh\d"),
    ("fake", "D:rel", 3, "ly_do", "D:rel"), ("fake", r"\\?\C:\cwd", 3, "ly_do", r"\\?\C:\cwd"), (_O, _CW, 3, "goc_rong", _O), ("x\n\\..", _CW, 3, "mot_dong", "x\n\\.."),
    ("x", _O, 3, "ket_qua", (_O, ("x",))), (".", _CW, 3, "ket_qua", (_O, ("cwd",))), (".", _O, 3, "goc_rong", _O), (r"Z:\x", _CW, 4, "ly_do", r"Z:\x"), (r"E:\x", _CW, 5, "ly_do", r"E:\x"),
    (r"F:\x", _CW, 2, "ket_qua", ("F:\\", ("x",))), ("fake", r"Z:\cwd", 4, "ly_do", r"Z:\cwd"), (r"G:\x", _CW, 0, "ly_do", r"G:\x"), (r"H:\x", _CW, 1, "ly_do", r"H:\x"),
    (r"R:\x", _CW, 6, "ly_do", r"R:\x"), (_DAI, _CW, 3, "cat_200", _DAI))
class TinHieuChotCa(AssertionError):
    def __init__(self, ca, luot, nhan):
        super().__init__("%s · %s · %s" % (ca, luot, nhan)); self.ca, self.luot, self.nhan = ca, luot, nhan  # noqa: E702
def _nem(e):
    raise e
def _nap(nguon, tl_module, goc):
    """`compile`+`exec` nguồn vào module MỚI rồi `bind`; thay đường tải/cài bằng đồ giả, kho Drive giả `m.drive` (như fragment P2a)."""
    m = types.ModuleType("wp433_tl_gws"); m.__file__ = goc.__file__  # noqa: E702
    exec(compile(nguon, goc.__file__, "exec"), m.__dict__)
    m.bind(tl_module)
    m.drive, that_imp = {}, m._imp
    for ten, tra in (("_public_curl_bytes", lambda fid, timeout=120.0: m.drive.get(fid)), ("_secrets_fetch", lambda a, fid: (m.drive.get(fid), "gia")), ("load_creds", lambda *a, **k: None),
                     ("_gas", lambda: _nem(RuntimeError("MANG_BI_CHAN"))), ("_ensure_nlm_installed", lambda *a, **k: (True, "gia")), ("cmd_gws_bootstrap_cowork", lambda *a, **k: 0),
                     ("_imp", lambda n: types.SimpleNamespace(gws_exe=lambda: "gws-gia") if n == "gws_bridge" else that_imp(n))):
        setattr(m, ten, tra)
    m.AGENT_CREDS_FILEID = ""          # agent giả KHÔNG CẤU HÌNH
    return m
@contextlib.contextmanager
def _thay(obj, ten, gia):
    cu = getattr(obj, ten); setattr(obj, ten, gia)  # noqa: E702
    try:
        yield
    finally:
        setattr(obj, ten, cu)
def _probe_symlink(dich, lk):
    """Dựng symlink THƯ MỤC `lk` → `dich` trên CHÍNH thư mục fixture của lượt: None (dựng được) hoặc OSError đã bắt."""
    try:
        return os.symlink(dich, lk, target_is_directory=True)
    except OSError as e:
        return e
def _sach(k):
    """sạch(K): không tệp nào ngoài `.git`, và `git status --porcelain` rỗng khi có git."""
    git = shutil.which("git") and subprocess.run(["git", "-C", k, "status", "--porcelain", "--untracked-files=all"], capture_output=True).stdout
    return not [t for d, _ds, fs in os.walk(k) if os.sep + ".git" not in d for t in fs] and not git
class _Rig:
    """Một ca: thư mục tạm `realpath`, HOME/USERPROFILE/CODEX_HOME/GOOGLE_WORKSPACE_CLI_CONFIG_DIR/TL_*/cwd đặt tạm, khôi phục khi ra.
    `so` là SỔ LƯỢT dùng chung: mỗi lượt ghi đúng một trạng thái (`đạt` · `đỏ` · `bỏ_qua`)."""
    def __init__(self, m, ca, store, so):
        self.m, self.ca, self.store, self.so, self.ghi, self.ls = m, ca, store, so, 0, []
    def __enter__(self):
        self.td, self.cu_env, self.cu_cwd = os.path.realpath(tempfile.mkdtemp(prefix="wp433c-")), dict(os.environ), os.getcwd()
        for k in [k for k in os.environ if k.startswith("TL_")] + ["CLAUDE_CODE_OAUTH_TOKEN", "GEMINI_API_KEY"]:
            os.environ.pop(k, None)
        self.T = self.td[:1].upper() + self.td[1:]          # dạng M2 của gốc rig (chữ ổ HOA)
        os.makedirs(self.p("home"))
        os.environ.update(TL_MASTER_KEY=_MK, CODEX_HOME=self.p("cx"), HOME=self.p("home"), USERPROFILE=self.p("home"))
        os.chdir(self.td); self.m.drive.clear()  # noqa: E702
        return self
    def __exit__(self, *a):
        os.chdir(self.cu_cwd); os.environ.clear(); os.environ.update(self.cu_env); shutil.rmtree(self.td, ignore_errors=True)  # noqa: E702
    p = lambda self, *a: "\\".join((self.T, *a))
    def kho(self):
        k = self.p("K"); os.makedirs(k)  # noqa: E702
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
        """Bộ phân loại bỏ qua: chỉ nt + `winerror == 1314` (thiếu quyền tạo symlink) ⇒ `bỏ_qua`; mọi lỗi probe khác ⇒ lượt `đỏ`."""
        if not (_TEN_OS == "nt" and getattr(e, "winerror", None) == 1314):
            self.so.append((self.ca, luot, "đỏ", None))
            raise TinHieuChotCa(self.ca, luot, "probe symlink: %r" % ((type(e).__name__, e.errno, getattr(e, "winerror", None)),))
        self.so.append((self.ca, luot, "bỏ_qua", e))
        return True
    def goi(self, luot, fn, lstat=None):
        """Một LƯỢT GỌI: chặn tiến trình con/mạng, stdout/stderr RIÊNG, đếm lời gọi writer của `credentials.json` (`self.ghi`) và ghi
        mọi đường qua `os.lstat` (`self.ls`; `lstat(p)` tiêm lỗi). `AssertionError` đi THẲNG ra (N4(d)); ngoại lệ khác ⇒ `ngoai_le_la`."""
        out, err, m = io.StringIO(), io.StringIO(), self.m
        self.ghi, self.ls, cu = 0, [], (subprocess.run, subprocess.Popen, urllib.request.urlopen, os.lstat, m._ghi_nguyen_tu_0600)
        subprocess.run = subprocess.Popen = urllib.request.urlopen = lambda *a, **k: _nem(RuntimeError("MANG_BI_CHAN"))
        def ls(q, *a, **k):
            self.ls.append(q); lstat and lstat(q)  # noqa: E702
            return cu[3](q, *a, **k)
        def wr(path, data):
            self.ghi += os.path.basename(path) == "credentials.json"
            return cu[4](path, data)
        os.lstat, m._ghi_nguyen_tu_0600 = ls, wr
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                kq = fn()
        except AssertionError:
            raise
        except Exception as e:  # noqa: BLE001 — biên của lượt
            self.so.append((self.ca, luot, "đỏ", None))
            raise TinHieuChotCa(self.ca, luot, "ngoai_le_la") from e
        finally:
            subprocess.run, subprocess.Popen, urllib.request.urlopen, os.lstat, m._ghi_nguyen_tu_0600 = cu
        return kq, out.getvalue(), [d for d in err.getvalue().splitlines() if d.startswith(_W4)]
    def w(self, luot, cfg, lstat=None):
        """Lượt W4 (fixture gws chuẩn của P2a: `bootstrap --env code --no-nlm --no-gws`, bundle có token + gws_cred) hoặc W5
        (`_gws_auth_load`). `cfg` là giá trị THÔ của biến môi trường. Trả (kết quả, stdout, các dòng `[bootstrap] ✗ …`)."""
        os.environ["GOOGLE_WORKSPACE_CLI_CONFIG_DIR"], m = cfg, self.m
        if luot.startswith("W4"):
            m.drive["S433"] = self.store.encrypt(json.dumps({"token": _TOK, "gws_cred": _CRED}).encode("utf-8"), _MK)
            ns = argparse.Namespace(secrets_id="S433", secrets_file=None, env="code", config=None, profile=None, no_gws=True, no_nlm=True, bindir=None, require_agent_creds=False)
            return self.goi(luot, lambda: m.cmd_bootstrap(ns), lstat)
        m.drive["G433"] = self.store.encrypt(_CRED.encode("utf-8"), _TOK)
        return self.goi(luot, lambda: m._gws_auth_load(_TOK, "G433"), lstat)
    def tu_choi(self):
        """Hậu điều chung của mọi lượt từ chối: writer 0 lần, không tệp tạm `.auth.json.*` nào dưới gốc rig."""
        return self.ghi == 0 and not [t for _d, _ds, fs in os.walk(self.td) for t in fs if t.startswith(".auth.json.")]
def phan_loai_nt(r):
    for luot, (p, *mong) in (("p%02d" % i, d) for i, d in enumerate(_N1, 1)):   # tên lượt sinh TỪ BẢNG, không đọc sổ
        kq, _o, _e = r.goi(luot, lambda: r.m._phan_loai_duong_nt(p))
        ma = mong[0] if len(mong) == 1 else "tuong_doi" if mong[0] is None else "o_tuyet_doi"
        r.xs(luot, ma=isinstance(kq, tuple) and kq[:1] == (ma,), goc_tp=len(mong) == 1 or kq[1:] == tuple(mong))
def chuan_nt(r):
    for luot, (p, cwd, lo, nhan, mong) in (("q%02d" % i, d) for i, d in enumerate(_N2, 1)):
        kq, _o, _e = r.goi(luot, lambda: r.m._duong_dich_chuan_nt(p, cwd, lambda g: lo))
        r.xs(luot, **{nhan: kq == (mong if isinstance(mong, tuple) else _DG + _r(mong))})
def tich_hop_nt(r):
    p, k, loi_o = r.p, r.kho(), lambda g: _nem(OSError("wp433-c1-loai-o"))
    c = p("K", "gwscfg"); kq, _o, _e = r.w("W5.trong_kho", c)  # noqa: E702
    r.xs("W5.trong_kho", ly_do=kq == (False, _KHO + _r(p("K"))) and r.tu_choi() and not os.path.lexists(c) and _sach(k))
    kq, _o, err = r.w("W4.trong_kho", c)
    r.xs("W4.trong_kho", w4=kq == 1 and err == [_W4 + _KHO + _r(p("K"))] and r.tu_choi() and not os.path.lexists(c) and _sach(k))
    kq, _o, _e = r.w("W5.tuong_doi", "cfg"); d = p("cfg", "credentials.json")  # noqa: E702
    r.xs("W5.tuong_doi", ket_qua=kq == (True, d) and pathlib.Path(d).read_bytes() == _CRED.encode("utf-8"))
    for luot, cfg in (("W5.o_tuong_doi", r.T[:2] + "cfg2"), ("W5.unc", r"\\wp433-khong-ton-tai.invalid\s\x")):
        kq, _o, _e = r.w(luot, cfg)
        r.xs(luot, ly_do=kq == (False, _DG + _r(cfg)) and r.tu_choi() and (luot != "W5.unc" or r.ls == []))
    os.makedirs(p("that"))
    for luot, lk, dich, cfg in (("W5.sl_to_tien", p("sl"), p("that"), p("sl", "a")), ("W5.sl_treo", p("st"), p("khong_ton_tai"), p("st"))):
        e = _probe_symlink(dich, lk)
        if e is None or not r.bo_qua(luot, e):
            kq, _o, _e = r.w(luot, cfg)
            r.xs(luot, lien_ket=kq == (False, _LK + _r(lk)) and r.tu_choi() and not os.listdir(p("that")) and not os.path.lexists(p("khong_ton_tai")))
    with _thay(r.m, "_loai_o_nt", loi_o):
        kq, _o, _e = r.w("W5.loai_o_loi", p("c2"))
    r.xs("W5.loai_o_loi", hop_dong=kq == (False, "ghi lỗi: OSError") and r.tu_choi())
    c6 = pathlib.Path(os.path.expanduser("~/.tra_luat_config.json")); c6_truoc = c6.read_bytes() if os.path.lexists(c6) else None  # noqa: E702
    with _thay(r.m, "_loai_o_nt", loi_o):
        kq, out, err = r.w("W4.loai_o_loi", p("c2"))
    r.xs("W4.loai_o_loi", hop_dong=kq == 1 and err == [_W4 + "ghi lỗi: OSError"] * 2 and "✓ gws cred" not in out and r.tu_choi(),   # WP433 N: W6 cũng từ chối
         w6=" ✓ config " not in out and (c6.read_bytes() if os.path.lexists(c6) else None) == c6_truoc)
    os.makedirs(p("pk", ".git"))
    mot = []   # WP433 N: lỗi CHỈ ở lần `lstat` ĐẦU (của `_co_git_nt`) — `_trong_kho_git` (M4) cũng lan lỗi, nên ném mọi lần thì đột biến không đo được
    kq, _o, _e = r.w("W5.git_loi", p("pk", "gws"), lambda q: q == p("pk", ".git") and not mot and (mot.append(q) or _nem(PermissionError("wp433-c1-git"))))
    r.xs("W5.git_loi", hop_dong=kq == (False, "ghi lỗi: PermissionError") and r.tu_choi())
    os.makedirs(p("rp")); truoc, that = not os.path.lexists(p("rp", "gws")), os.path.realpath  # noqa: E702
    with _thay(os.path, "realpath", lambda q, *a, **kw: _nem(PermissionError("wp433-c1-rp")) if kw.get("strict") is True and q == p("rp") else that(q, *a, **kw)):
        kq, _o, _e = r.w("W5.realpath_loi", p("rp", "gws"))
    r.xs("W5.realpath_loi", hop_dong=truoc and kq == (False, "ghi lỗi: PermissionError") and r.tu_choi())
_CA = ((phan_loai_nt, "mọi"), (chuan_nt, "mọi"), (tich_hop_nt, "nt"))
_DU_KIEN = tuple("db_nt_" + t for t in (  # N4(a): danh sách ID đột biến dự kiến (§4b, 47 mục) — viết RIÊNG khỏi `_DB`
    "bo_nul bo_trang bo_win32 bo_dos bo_nt bo_unc unc_chi_gach_nguoc o_tran o_tuong_doi o_chi_hoa khong_hoa_o goc_o_tuyet_doi chi_gach_nguoc bo_hai_cham bo_ky_tu_cam bo_surrogate "
    "bo_dieu_khien bo_cuoi_cham bo_ten_tb ten_tb_khong_cach bo_conin o_khac_nhan cwd_khong_kiem goc_rong bo_loai_o loai_o_moi_loai bo_removable loai_o_chi_tuyet_doi khong_repr bo_chot "
    "ghi_duong_tho goc_cfg dao_ky_tu_cuoi dao_cuoi_ten_tb cam_nbsp_del loai_o_nhan_0 loai_o_nhan_1 loai_o_nhan_6 nuot_loi_loai_o thanh_phan_truoc_namespace bo_cat_200 w4_nuot_loi_dich "
    "git_nuot_loi realpath_khong_strict strict_truoc_lien_ket bo_chu_so_mu bo_conout").split())
_NUL, _WIN32, _LO = '    if "\\x00" in p:\n        return ("nul",)\n', [(r'(r"[\\/]{2}\?[\\/]", "thiet_bi_win32"), ', "")], "(a[1]) not in (2, 3)"
_KT = """    if re.search(r'[<>:"|?*\\x01-\\x1f]', t) or re.search(r"[\\ud800-\\udfff]", t):\n        return "ky_tu_cam"\n"""
_CC, _TB = '    if t.endswith((".", " ")):\n        return "cuoi_cham_cach"\n', '    return "ten_thiet_bi" if _TEN_TB_NT.fullmatch(t) else None\n'
_CH, _II = "    chuan = _duong_dich_chuan_nt(cfgdir_tho, os.getcwd()", "        if (ly := _kiem_dich_ghi(dest, goc, tp)) is not None:\n            return dest, ly\n"
_III, _C4 = "        kho = _co_git_nt(ntpath.join(os.path.realpath(a, strict=True), *tp[i:-1]))\n", "                    dest, ly_gws = _dich_cred_gws(cfgdir)\n"
_DB = tuple(("db_nt_" + d[0],) + d[1:] for d in (  # §4b: (đột biến, [(neo khớp ĐÚNG MỘT lần, thay)…], ca đích, lượt, nhãn)
    ("bo_nul", [(_NUL, "")], _P, "p09", "ma"), ("bo_trang", [('    if p.strip() == "":\n        return ("trang",)\n', "")], _P, "p10", "ma"), ("bo_win32", _WIN32, _P, "p11", "ma"),
    ("bo_dos", [(r'(r"[\\/]{2}\.[\\/]", "thiet_bi_dos"), ', "")], _P, "p14", "ma"), ("bo_nt", [(r'(r"[\\/]\?\?[\\/]", "nt_doi_tuong"), ', "")], _P, "p16", "ma"),
    ("bo_unc", [(r', (r"[\\/]{2}", "unc")', "")], _P, "p21", "ma"), ("unc_chi_gach_nguoc", [(r'(r"[\\/]{2}", "unc")', r'(r"\\\\", "unc")')], _P, "p22", "ma"),
    ("o_tran", [(r'if r == "" or r[0] not in "\\/":', r'if (r := r or "\\")[0] not in "\\/":')], _P, "p17", "ma"), ("o_tuong_doi", [(r' or r[0] not in "\\/"', "")], _P, "p18", "ma"),
    ("o_chi_hoa", [('re.fullmatch(r"[A-Za-z]:", d)', 're.fullmatch(r"[A-Z]:", d)')], _P, "p03", "ma"), ("khong_hoa_o", [(r'd.upper() + "\\"', r'd + "\\"')], _P, "p03", "goc_tp"),
    ("goc_o_tuyet_doi", [('        if p[0] in "\\\\/":\n            return ("goc_o",)\n', "")], _P, "p19", "ma"), ("chi_gach_nguoc", [(r're.split(r"[\\/]", r)', r're.split(r"\\", r)')], _P, "p02", "goc_tp"),
    ("bo_hai_cham", [('    if ".." in tp:\n        return ("hai_cham",)\n', "")], _P, "p28", "ma"), ("bo_ky_tu_cam", [(r"""re.search(r'[<>:"|?*\x01-\x1f]', t) or """, "")], _P, "p31", "ma"),
    ("bo_surrogate", [(r''' or re.search(r"[\ud800-\udfff]", t)''', "")], _P, "p33", "ma"), ("bo_dieu_khien", [(r"\x01-\x1f]'", "]'")], _P, "p34", "ma"),
    ("bo_cuoi_cham", [(_CC, "")], _P, "p35", "ma"), ("bo_ten_tb", [(_TB, "    return None\n")], _P, "p37", "ma"), ("ten_tb_khong_cach", [(r"\$) *(\..*)?", r"\$)(\..*)?")], _P, "p40", "ma"),
    ("bo_conin", [(r"|CONIN\$|CONOUT\$", "")], _P, "p41", "ma"), ("o_khac_nhan", [('        return ("o_khac",)\n', '        loai, goc = "o_tuyet_doi", d + "\\\\"\n')], _P, "p27", "ma"),
    ("cwd_khong_kiem", [('if c[0] == "o_tuyet_doi" else c\n', 'if c[0] == "o_tuyet_doi" else _phan_loai_duong_nt(x := ntpath.join(cwd, p))\n')], _Q, "q03", "ly_do"),
    ("goc_rong", [(" or not a[2]", "")], _Q, "q06", "goc_rong"), ("bo_loai_o", [(" or (loai_o or _loai_o_nt)" + _LO, "")], _Q, "q11", "ly_do"),
    ("loai_o_moi_loai", [(_LO, "(a[1]) == 4")], _Q, "q12", "ly_do"), ("bo_removable", [(_LO, "(a[1]) != 3")], _Q, "q13", "ket_qua"),
    ("loai_o_chi_tuyet_doi", [("(loai_o or _loai_o_nt)" + _LO, "x is p and (loai_o or _loai_o_nt)" + _LO)], _Q, "q14", "ly_do"), ("khong_repr", [("repr(x)[:200]", "x[:200]")], _Q, "q03", "ly_do"),
    ("bo_chot", [("return _dich_cred_gws_nt(cfgdir_tho)", 'return os.path.join(cfgdir_tho, "credentials.json"), None')], _W, "W5.trong_kho", "ly_do"),
    ("ghi_duong_tho", [("return dest, None if kho is None", 'return ntpath.join(cfgdir_tho, "credentials.json"), None if kho is None')], _W, "W5.tuong_doi", "ket_qua"),
    ("goc_cfg", [("_kiem_dich_ghi(dest, goc, tp)", "_kiem_dich_ghi(dest, ntpath.dirname(dest), tp[-1:])")], _W, "W5.sl_to_tien", "lien_ket"), ("dao_ky_tu_cuoi", [(_KT + _CC, _CC + _KT)], _P, "p43", "ma"),
    ("dao_cuoi_ten_tb", [(_CC + _TB, '    if _TEN_TB_NT.fullmatch(t):\n        return "ten_thiet_bi"\n    return "cuoi_cham_cach" if t.endswith((".", " ")) else None\n')], _P, "p44", "ma"),
    ("cam_nbsp_del", [(r"\x01-\x1f]'", r"\x01-\x1f\x7f\u00a0]'")], _P, "p45", "ma"), ("loai_o_nhan_0", [(_LO, "(a[1]) not in (0, 2, 3)")], _Q, "q15", "ly_do"),
    ("loai_o_nhan_1", [(_LO, "(a[1]) not in (1, 2, 3)")], _Q, "q16", "ly_do"), ("loai_o_nhan_6", [(_LO, "(a[1]) not in (2, 3, 6)")], _Q, "q17", "ly_do"),
    ("nuot_loi_loai_o", [(_CH, "    def lo(g):\n        try:\n            return _loai_o_nt(g)\n        except OSError:\n            return 3\n" + _CH + ", lo")], _W, "W5.loai_o_loi", "hop_dong"),
    ("thanh_phan_truoc_namespace", [(_NUL, _NUL + '    for t in re.split(r"[\\\\/]", p)[1:]:\n        if t not in ("", ".", "..") and _tp_sai_nt(t):\n            return (_tp_sai_nt(t),)\n')], _P, "p11", "ma"),
    ("bo_cat_200", [("repr(x)[:200]", "repr(x)")], _Q, "q18", "cat_200"),
    ("w4_nuot_loi_dich", [(_C4, "                    try:\n    %s                    except OSError:\n                        ly_gws = \"ghi lỗi\"\n" % _C4)], _W, "W4.loai_o_loi", "hop_dong"),
    ("git_nuot_loi", [("except (FileNotFoundError, NotADirectoryError):\n            if ntpath", "except OSError:\n            if ntpath")], _W, "W5.git_loi", "hop_dong"),
    ("realpath_khong_strict", [("os.path.realpath(a, strict=True)", "os.path.realpath(a)")], _W, "W5.realpath_loi", "hop_dong"),
    ("strict_truoc_lien_ket", [(_II, ""), (_III, _III + _II.replace("if (ly", "if kho is None and (ly"))], _W, "W5.sl_treo", "lien_ket"),
    ("bo_chu_so_mu", [("COM[0-9¹²³]|LPT[0-9¹²³]", "COM[0-9]|LPT[0-9]")], _P, "p46", "ma"), ("bo_conout", [(r"|CONOUT\$", "")], _P, "p47", "ma")))
_GIA = ('    class TinGia(AssertionError):\n        ca, luot, nhan = "phan_loai_nt", "p01", "ma"\n    try:\n        raise AttributeError("wp433-c1-tu-kiem")\n'
        '    except Exception:\n        raise TinGia("wp433-c1-tu-kiem")\n')
_TU_KIEM = (  # N4(d): bộ phân hạng KHÔNG được cấp tín dụng — (tên, cặp, ca, lượt, nhãn, hạng mong đợi)
    ("tu_kiem_doi_kieu", [(_NUL, _GIA + _NUL)], _P, "p01", "ma", "TIN_DUNG_GIA"),       # lớp giả mang ĐỦ tuple, sinh từ `except` đổi kiểu
    ("tu_kiem_chu_thich", [("\ndef _dich_cred_gws_nt(", "\n# vô hại\ndef _dich_cred_gws_nt(")], _P, "p01", "ma", "SONG_SOT"),
    ("tu_kiem_sai_luot", _WIN32, _P, "p12", "ma", "TIN_DUNG_GIA"),                       # CHÍNH db_nt_bo_win32, chỉ đổi lượt khai
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
    except BaseException as e:  # noqa: BLE001 — kể cả AssertionError KHÔNG phải `TinHieuChotCa` dù mang đủ tuple
        return "TIN_DUNG_GIA", e
    return ("BO_QUA" if (ca, luot, "bỏ_qua") in [x[:3] for x in so] else "SONG_SOT"), None
def _run(tl_module):
    goc = tl_module._imp("tl_gws"); goc.bind(tl_module)  # noqa: E702
    nguon, store, nt = pathlib.Path(goc.__file__).read_text(encoding="utf-8"), tl_module._imp("gws_cred_store"), _TEN_OS == "nt"
    m, so, b, c, nen = _nap(nguon, tl_module, goc), [], 0, 0, {ca.__name__: n for ca, n in _CA}
    for ca, n in _CA:
        if n == "nt" and not nt:
            so += [(ca.__name__, luot, "chỉ_nt", None) for luot in _LUOT_DU_KIEN.get(ca.__name__, ())]
            continue
        b += 1
        try:
            _chay(m, store, ca, so); c += 1  # noqa: E702
        except Exception as e:  # noqa: BLE001
            print("[%s] ĐỎ %s: %r (%r)" % (TEST_ID, ca.__name__, e, e.__cause__), file=sys.stderr)
    bq = [s for s in so if s[2] == "bỏ_qua"]
    for s in bq:
        print("[%s] BO_QUA %s·%s: %r" % (TEST_ID, s[0], s[1], s[3]), file=sys.stderr)
    kq = {d[0]: "CHI_NT" if not nt and nen.get(d[2]) == "nt" else _hang(nguon, tl_module, goc, store, *d[1:])[0] for d in _DB}
    tk = [(d[0], d[5]) + _hang(nguon, tl_module, goc, store, *d[1:5]) for d in _TU_KIEM]
    doi = lambda e: isinstance(getattr(e, "__context__", None), AttributeError) and (e.ca, e.luot, e.nhan) == (_P, "p01", "ma")   # đủ tuple, đã qua `except` đổi kiểu
    k = sum(h == mong and (ten != "tu_kiem_doi_kieu" or doi(e)) for ten, mong, h, e in tk)
    for ten, hang in list(kq.items()) + [(ten, "tự kiểm %s ≠ %s" % (h, mong)) for ten, mong, h, _e in tk if h != mong]:
        if hang not in ("GIET", "CHI_NT", "BO_QUA"):
            print("[%s] ĐỘT BIẾN %s: %s" % (TEST_ID, ten, hang), file=sys.stderr)
    dem, hg = lambda tt: sum(s[2] == tt for s in so), lambda tt: sum(h == tt for h in kq.values())
    a, w, x, y, z, u, t = len(_LUOT_DU_KIEN), len(_CA) - b, sum(map(len, _LUOT_DU_KIEN.values())), dem("đạt") + dem("đỏ"), dem("đạt"), len(bq), dem("chỉ_nt")
    e, g, h, v, i = len(_DB), hg("GIET"), hg("BO_QUA"), hg("CHI_NT"), hg("HONG"); f = e - h - v  # noqa: E702
    print("[%s] CA: dự_kiến=%d chạy=%d đạt=%d bỏ_qua=0 chỉ_nt=%d · LUOT: dự_kiến=%d chạy=%d đạt=%d bỏ_qua=%d chỉ_nt=%d · DOT BIEN: dự_kiến=%d chạy=%d "
          "giết_đúng=%d bỏ_qua=%d chỉ_nt=%d · HONG: %d · TU_KIEM: %d/%d" % (TEST_ID, a, b, c, w, x, y, z, u, t, e, f, g, h, v, i, k, len(_TU_KIEM)), file=sys.stderr)
    ve = {"ca_dat": b == c, "luot_dat": y == z, "giet_dung": f == g, "hong": i == 0, "so_ca": a == b + w, "tu_kiem": k == len(_TU_KIEM),
          "so_luot": x == y + u + t == 76 and sorted(s[:2] for s in so) == sorted((ca, luot) for ca, ds in _LUOT_DU_KIEN.items() for luot in ds),
          "so_dot_bien": e == len(_DU_KIEN) and sorted(d[0] for d in _DB) == sorted(_DU_KIEN),
          "bo_qua": h == u <= 2 and all(nt and s[0] == _W and s[1] in _BO_QUA_DUOC and isinstance(s[3], OSError) and getattr(s[3], "winerror", None) == 1314 for s in bq)
          and sorted(d[3] for d in _DB if kq[d[0]] == "BO_QUA") == sorted(s[1] for s in bq),
          "nen": (w, t, v) == ((0, 0, 0) if nt else (1, 11, 8))}
    if not all(ve.values()):
        print("[%s] VẾ SAI: %s" % (TEST_ID, ", ".join(n for n, dk in ve.items() if not dk)), file=sys.stderr)
    return all(ve.values())
def run(tl_module):
    ra = io.StringIO()                      # N4(e): fragment in mọi thứ ra STDERR (driver bundle đọc stdout làm JSON)
    with contextlib.redirect_stdout(ra):
        ok = _run(tl_module)
    return ok and not ra.getvalue()
