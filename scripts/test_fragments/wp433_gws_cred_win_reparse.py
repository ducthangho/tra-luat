# -*- coding: utf-8 -*-
"""wp433 P2c-R — `_kiem_dich_ghi` của `tl_gws.py` coi reparse point (junction, mount point, symlink: mọi entry mà `os.lstat` báo
`FILE_ATTRIBUTE_REPARSE_POINT`) là liên kết, cho mọi chỗ ghi credential gọi nó (spec GWS-CRED-DICH-NGOAI-KHO-R r1). Mọi ca chạy trên bản
`tl_gws` nạp TRONG BỘ NHỚ (nguồn thật hoặc đột biến), HOME/cfgdir tạm, dữ liệu GIẢ, không mạng. Mỗi LƯỢT thu đủ hậu điều rồi so nhãn; nhãn
đỏ ĐẦU TIÊN thành `TinHieuChotCa(ca, lượt, nhãn)` — đột biến chỉ GIẾT khi khớp cả ba (bảng `_DB` chép §4b của spec)."""
import contextlib, io, os, pathlib, shutil, stat, subprocess, sys, tempfile, types, urllib.request  # noqa: E401
TEST_ID = "wp433_gws_cred_win_reparse"
_MK, _TOK, _CRED, _CU = "wp433-master-gia", "wp433-token-gia", '{"gia": "SENTINEL-wp433-r-gia"}', b"CU-wp433-r"
_LK, _G, _N, _TEN_OS, _BO_QUA_DUOC = "là liên kết tượng trưng: ", "reparse_gia_lap", "lien_ket_nt", os.name, ("W5.sl_dir", "W5.sl_tep")
_LUOT_DU_KIEN = {  # N3(b) SỔ LƯỢT — viết RIÊNG khỏi các hàm ca: 2 ca, 3 + 4 = 7 lượt, đúng thứ tự §4
    _G: ("W5.bit", "truc_tiep", "W5.khong_bit"), _N: ("W5.jn_cfg", "W5.jn_to_tien", "W5.sl_dir", "W5.sl_tep")}
_r = lambda x: repr(x)[:200]
class TinHieuChotCa(AssertionError):
    def __init__(self, ca, luot, nhan):
        super().__init__("%s · %s · %s" % (ca, luot, nhan)); self.ca, self.luot, self.nhan = ca, luot, nhan  # noqa: E702
def _nem(e):
    raise e
def _nap(nguon, tl_module, goc):
    """`compile`+`exec` nguồn vào module MỚI rồi `bind`; thay đường tải bằng đồ giả, kho Drive giả `m.drive` (như fragment P2a, C1)."""
    m = types.ModuleType("wp433_tl_gws"); m.__file__ = goc.__file__  # noqa: E702
    exec(compile(nguon, goc.__file__, "exec"), m.__dict__)
    m.bind(tl_module)
    m.drive = {}
    for ten, tra in (("_public_curl_bytes", lambda fid, timeout=120.0: m.drive.get(fid)), ("_gas", lambda: _nem(RuntimeError("MANG_BI_CHAN"))), ("load_creds", lambda *a, **k: None)):
        setattr(m, ten, tra)
    return m
def _junction(dich, lk):
    """Dựng junction `lk` → `dich`: `_winapi.CreateJunction`, thiếu thì `cmd /c mklink /J` (gọi NGOÀI cửa sổ chặn tiến trình con)."""
    try:
        import _winapi
        tao = _winapi.CreateJunction
    except (ImportError, AttributeError):
        return subprocess.run(["cmd", "/c", "mklink", "/J", lk, dich], check=True, capture_output=True)
    return tao(dich, lk)
def _probe_symlink(dich, lk, thu_muc):
    """Dựng symlink `lk` → `dich` trên CHÍNH thư mục fixture của lượt: None (dựng được) hoặc OSError đã bắt."""
    try:
        return os.symlink(dich, lk, target_is_directory=thu_muc)
    except OSError as e:
        return e
class _Rig:
    """Một ca: thư mục tạm `realpath` (ngoài kho), HOME/USERPROFILE/CODEX_HOME/TL_*/cwd đặt tạm, khôi phục khi ra. `so` là SỔ LƯỢT dùng
    chung: mỗi lượt ghi đúng một trạng thái (`đạt` · `đỏ` · `bỏ_qua`); `kq` là kết quả của lời gọi gần nhất."""
    def __init__(self, m, ca, store, so):
        self.m, self.ca, self.store, self.so, self.ghi, self.kq = m, ca, store, so, 0, "chưa gọi"
    def __enter__(self):
        self.td, self.cu_env, self.cu_cwd = os.path.realpath(tempfile.mkdtemp(prefix="wp433r-")), dict(os.environ), os.getcwd()
        for k in [k for k in os.environ if k.startswith("TL_")]:
            os.environ.pop(k, None)
        self.T = self.td[:1].upper() + self.td[1:]          # dạng mà nhánh nt của C1 trả về (chữ ổ HOA); POSIX: nguyên `/…`
        os.makedirs(self.p("home"))
        os.environ.update(TL_MASTER_KEY=_MK, CODEX_HOME=self.p("cx"), HOME=self.p("home"), USERPROFILE=self.p("home"))
        os.chdir(self.td); self.m.drive.clear()  # noqa: E702
        return self
    def __exit__(self, *a):
        os.chdir(self.cu_cwd); os.environ.clear(); os.environ.update(self.cu_env); shutil.rmtree(self.td, ignore_errors=True)  # noqa: E702
    p = lambda self, *a: os.path.join(self.T, *a)
    def do(self, luot, nhan, e=None):
        self.so.append((self.ca, luot, "đỏ", None))
        raise TinHieuChotCa(self.ca, luot, nhan) from e
    def xs(self, luot, **nhan):
        """Kết thúc MỘT lượt: hậu điều đã thu đủ (đối số, theo thứ tự ghi); nhãn đỏ đầu tiên ⇒ `đỏ` + tín hiệu, không thì `đạt`."""
        hong = [n for n, dk in nhan.items() if not dk]
        if hong:
            self.do(luot, hong[0])
        self.so.append((self.ca, luot, "đạt", None))
    def bo_qua(self, luot, e):
        """Bộ phân loại bỏ qua: chỉ nt + `winerror == 1314` (thiếu quyền tạo symlink) ⇒ `bỏ_qua`; mọi lỗi probe khác ⇒ lượt `đỏ`."""
        if not (_TEN_OS == "nt" and getattr(e, "winerror", None) == 1314):
            self.do(luot, "probe symlink: %r" % ((type(e).__name__, e.errno, getattr(e, "winerror", None)),))
        self.so.append((self.ca, luot, "bỏ_qua", e))
        return True
    def goi(self, luot, fn, gia=None):
        """Một LƯỢT GỌI: chặn tiến trình con/mạng, stdout/stderr RIÊNG, đếm lời gọi writer của `credentials.json` (`self.ghi`), bọc
        `os.lstat`: ĐÚNG đường `gia[0]` (so sau `normcase(normpath)`) nhận `SimpleNamespace(S_IFDIR, st_file_attributes=gia[1])`, đường khác
        đi hàm thật. Mọi thứ đã thay khôi phục trong `finally`. `AssertionError` đi THẲNG ra (N3(d)); ngoại lệ khác ⇒ `ngoai_le_la`."""
        ra, m, chuan = io.StringIO(), self.m, lambda q: os.path.normcase(os.path.normpath(q))
        self.ghi, self.kq, cu = 0, "chưa gọi", (subprocess.run, subprocess.Popen, urllib.request.urlopen, os.lstat, m._ghi_nguyen_tu_0600)
        subprocess.run = subprocess.Popen = urllib.request.urlopen = lambda *a, **k: _nem(RuntimeError("MANG_BI_CHAN"))
        def ls(q, *a, **k):
            if gia and isinstance(q, str) and chuan(q) == chuan(gia[0]):
                return types.SimpleNamespace(st_mode=stat.S_IFDIR | 0o700, st_file_attributes=gia[1])
            return cu[3](q, *a, **k)
        def wr(path, data):
            self.ghi += os.path.basename(path) == "credentials.json"
            return cu[4](path, data)
        os.lstat, m._ghi_nguyen_tu_0600 = ls, wr
        try:
            with contextlib.redirect_stdout(ra), contextlib.redirect_stderr(ra):
                self.kq = fn()
        except AssertionError:
            raise
        except Exception as e:  # noqa: BLE001 — biên của lượt
            self.do(luot, "ngoai_le_la", e)
        finally:
            subprocess.run, subprocess.Popen, urllib.request.urlopen, os.lstat, m._ghi_nguyen_tu_0600 = cu
        return self.kq
    def w5(self, luot, cfg, gia=None):
        """Lượt W5 (`_gws_auth_load`); `cfg` là giá trị THÔ của `GOOGLE_WORKSPACE_CLI_CONFIG_DIR`. POSIX đi nhánh P2a, nt đi nhánh C1."""
        os.environ["GOOGLE_WORKSPACE_CLI_CONFIG_DIR"] = cfg
        self.m.drive["G433"] = self.store.encrypt(_CRED.encode("utf-8"), _TOK)
        return self.goi(luot, lambda: self.m._gws_auth_load(_TOK, "G433"), gia)
def _truc_tiep(r):
    """Lượt `truc_tiep` (hình dạng lời gọi của W1–W3): gọi thẳng `_kiem_dich_ghi(<T>/x/credentials.json, <T>, ("x", "credentials.json"))`."""
    x = r.p("x"); os.makedirs(x, exist_ok=True)  # noqa: E702
    kq = r.goi("truc_tiep", lambda: r.m._kiem_dich_ghi(os.path.join(x, "credentials.json"), r.T, ("x", "credentials.json")), (x, 1024))
    r.xs("truc_tiep", reparse_truc_tiep=kq == _LK + _r(x))
def reparse_gia_lap(r):
    c = r.p("cfg"); d = os.path.join(c, "credentials.json"); os.makedirs(c)  # noqa: E702
    kq = r.w5("W5.bit", c, (c, stat.FILE_ATTRIBUTE_REPARSE_POINT))
    r.xs("W5.bit", reparse=kq == (False, _LK + _r(c)) and r.ghi == 0 and not os.listdir(c))
    _truc_tiep(r)
    kq = r.w5("W5.khong_bit", c, (c, stat.FILE_ATTRIBUTE_DIRECTORY | stat.FILE_ATTRIBUTE_SPARSE_FILE))   # 528: bit 512 không có trên entry thật của Windows
    r.xs("W5.khong_bit", khong_bit=kq == (True, d) and pathlib.Path(d).read_bytes() == _CRED.encode("utf-8"))
def lien_ket_nt(r):
    p, rong = r.p, lambda d: not [t for _d, _ds, fs in os.walk(d) for t in fs]
    for d in ("that", "that2", "c3"):
        os.makedirs(p(d))
    pathlib.Path(p("dich.json")).write_bytes(_CU)
    for luot, lk, dich, cfg in (("W5.jn_cfg", p("cfg"), p("that"), p("cfg")), ("W5.jn_to_tien", p("jn"), p("that2"), p("jn", "a", "b"))):
        try:
            _junction(dich, lk)
        except Exception as e:  # noqa: BLE001 — dựng junction thất bại ⇒ lượt `đỏ`, KHÔNG bỏ qua
            r.do(luot, "dung junction: %r" % (type(e).__name__,), e)
        kq = r.w5(luot, cfg)
        r.xs(luot, lien_ket=kq == (False, _LK + _r(lk)) and r.ghi == 0 and rong(dich))
    for luot, lk, dich, cfg, tm in (("W5.sl_dir", p("sd"), p("that"), p("sd"), True), ("W5.sl_tep", p("c3", "credentials.json"), p("dich.json"), p("c3"), False)):
        e = _probe_symlink(dich, lk, tm)
        if e is None or not r.bo_qua(luot, e):
            kq = r.w5(luot, cfg)
            r.xs(luot, lien_ket=kq == (False, _LK + _r(lk)) and r.ghi == 0 and rong(p("that")) and pathlib.Path(p("dich.json")).read_bytes() == _CU)
_CA = ((reparse_gia_lap, "mọi"), (lien_ket_nt, "nt"))
_DU_KIEN = ("db_bo_reparse", "db_reparse_moi_thu", "db_bo_reparse_nt")  # N3(a): danh sách ID đột biến dự kiến (§4b) — viết RIÊNG khỏi `_DB`
_BIT, _VAO = ' or getattr(st, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT', "    if (kho_dich := _trong_kho_git(os.path.dirname(dich))) is not None:\n"
_DB = (  # §4b: (đột biến, [(neo khớp ĐÚNG MỘT lần trên nguồn candidate, thay)…], ca đích, lượt, nhãn)
    ("db_bo_reparse", [(_BIT, "")], _G, "W5.bit", "reparse"),
    ("db_reparse_moi_thu", [(" & stat.FILE_ATTRIBUTE_REPARSE_POINT:\n", " & (stat.FILE_ATTRIBUTE_REPARSE_POINT | stat.FILE_ATTRIBUTE_SPARSE_FILE):\n")], _G, "W5.khong_bit", "khong_bit"),
    ("db_bo_reparse_nt", [(_BIT, "")], _N, "W5.jn_cfg", "lien_ket"))
_GIA = ('    class TinGia(AssertionError):\n        ca, luot, nhan = "reparse_gia_lap", "W5.bit", "reparse"\n    try:\n        raise AttributeError("wp433-r-tu-kiem")\n'
        '    except Exception:\n        raise TinGia("wp433-r-tu-kiem")\n')
_TU_KIEM = (  # N3(d): bộ phân hạng KHÔNG được cấp tín dụng — (tên, cặp, ca, lượt, nhãn, hạng mong đợi)
    ("tu_kiem_doi_kieu", [(_VAO, _GIA + _VAO)], _G, "W5.bit", "reparse", "TIN_DUNG_GIA"),   # lớp giả mang ĐỦ tuple, sinh từ `except` đổi kiểu
    ("tu_kiem_chu_thich", [("\ndef _kiem_dich_ghi(", "\n# vô hại\ndef _kiem_dich_ghi(")], _G, "W5.bit", "reparse", "SONG_SOT"),
    ("tu_kiem_sai_luot", [(_BIT, "")], _G, "truc_tiep", "reparse", "TIN_DUNG_GIA"),          # CHÍNH db_bo_reparse, giữ nhãn, chỉ đổi lượt khai
)
_PC_CFG = [("_kiem_dich_ghi(dest, goc, tp)", "_kiem_dich_ghi(dest, ntpath.dirname(dest), tp[-1:])")]   # nhánh nt của C1 chỉ kiểm từ `cfgdir`
def _ban_sao(nguon, tl_module, goc, cap):
    """Bản `tl_gws` trong bộ nhớ đã áp `cap`; None khi một neo không khớp ĐÚNG MỘT lần hoặc bản sao không nạp được."""
    for neo, thay in cap:
        if nguon.count(neo) != 1 or neo == thay:
            return None
        nguon = nguon.replace(neo, thay)
    try:
        return _nap(nguon, tl_module, goc)
    except Exception:  # noqa: BLE001
        return None
def _hang(nguon, tl_module, goc, store, cap, ca, luot, nhan):
    """Phân hạng MỘT đột biến trên bản sao trong bộ nhớ, trả (hạng, ngoại lệ): HONG (neo ≠ 1 lần / không nạp được) · SONG_SOT · BO_QUA
    (lượt đích được bỏ qua hợp lệ) · GIET (đúng lớp tín hiệu, đúng ca, đúng lượt, đúng nhãn) · TIN_DUNG_GIA (chết vì lý do khác)."""
    m, so = _ban_sao(nguon, tl_module, goc, cap), []
    if m is None:
        return "HONG", None
    try:
        with _Rig(m, ca, store, so) as r:
            next(c for c, _n in _CA if c.__name__ == ca)(r)
    except TinHieuChotCa as e:
        return ("GIET" if (e.ca, e.luot, e.nhan) == (ca, luot, nhan) else "TIN_DUNG_GIA"), e
    except BaseException as e:  # noqa: BLE001 — kể cả AssertionError KHÔNG phải `TinHieuChotCa` dù mang đủ tuple
        return "TIN_DUNG_GIA", e
    return ("BO_QUA" if (ca, luot, "bỏ_qua") in [x[:3] for x in so] else "SONG_SOT"), None
def _pc(nguon, tl_module, goc, store, cap, ca, fn):
    """Phản chứng BỘ ĐO (không phải mục `_DB`, không vào tổng): chạy `fn(rig)` trên bản sao áp `cap`, trả (tín hiệu | None, kq cuối, sổ)."""
    m, so = _ban_sao(nguon, tl_module, goc, cap), []
    if m is None:
        return "HONG", None, so
    with _Rig(m, ca, store, so) as r:
        try:
            fn(r)
        except TinHieuChotCa as e:
            return (e.ca, e.luot, e.nhan), r.kq, so
        return None, r.kq, so
def _phan_chung(nguon, tl_module, goc, store, nt):
    """`pc_truc_tiep` (mọi nền): RIÊNG lượt `truc_tiep`, với M1 ⇒ đạt (chặn tại `<T>/x`), với phép thay của đột biến 1 ⇒ trả None, tín
    hiệu đúng lượt ấy. `pc_chi_kiem_cfgdir` (nt): `W5.jn_cfg` vẫn đạt, `W5.jn_to_tien` đỏ ở `lien_ket`. Trả danh sách tên phản chứng ĐỎ."""
    a, b = _pc(nguon, tl_module, goc, store, [], _G, _truc_tiep), _pc(nguon, tl_module, goc, store, _DB[0][1], _G, _truc_tiep)
    kq = {"pc_truc_tiep": a[0] is None and str(a[1]).startswith(_LK) and a[2] == [(_G, "truc_tiep", "đạt", None)]
          and b == ((_G, "truc_tiep", "reparse_truc_tiep"), None, [(_G, "truc_tiep", "đỏ", None)])}
    if nt:
        c = _pc(nguon, tl_module, goc, store, _PC_CFG, _N, lien_ket_nt)
        kq["pc_chi_kiem_cfgdir"] = c[0] == (_N, "W5.jn_to_tien", "lien_ket") and [s[:3] for s in c[2]] == [(_N, "W5.jn_cfg", "đạt"), (_N, "W5.jn_to_tien", "đỏ")]
    return [ten for ten, dat in kq.items() if not dat]
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
            with _Rig(m, ca.__name__, store, so) as r:
                ca(r)
            c += 1
        except Exception as e:  # noqa: BLE001
            print("[%s] ĐỎ %s: %r (%r)" % (TEST_ID, ca.__name__, e, e.__cause__), file=sys.stderr)
    bq = [s for s in so if s[2] == "bỏ_qua"]
    for s in bq:
        print("[%s] BO_QUA %s·%s: %r" % (TEST_ID, s[0], s[1], s[3]), file=sys.stderr)
    kq = {d[0]: "CHI_NT" if not nt and nen.get(d[2]) == "nt" else _hang(nguon, tl_module, goc, store, *d[1:])[0] for d in _DB}
    tk = [(d[0], d[5]) + _hang(nguon, tl_module, goc, store, *d[1:5]) for d in _TU_KIEM]
    doi = lambda e: isinstance(getattr(e, "__context__", None), AttributeError) and (e.ca, e.luot, e.nhan) == (_G, "W5.bit", "reparse")   # đủ tuple, đã qua `except` đổi kiểu
    k, pc = sum(h == mong and (ten != "tu_kiem_doi_kieu" or doi(e)) for ten, mong, h, e in tk), _phan_chung(nguon, tl_module, goc, store, nt)
    for ten, hang in list(kq.items()) + [(ten, "tự kiểm %s ≠ %s" % (h, mong)) for ten, mong, h, _e in tk if h != mong] + [(ten, "phản chứng bộ đo ĐỎ") for ten in pc]:
        if hang not in ("GIET", "CHI_NT", "BO_QUA"):
            print("[%s] ĐỘT BIẾN %s: %s" % (TEST_ID, ten, hang), file=sys.stderr)
    dem, hg = lambda tt: sum(s[2] == tt for s in so), lambda tt: sum(h == tt for h in kq.values())
    a, w, x, y, z, u, t = len(_LUOT_DU_KIEN), len(_CA) - b, sum(map(len, _LUOT_DU_KIEN.values())), dem("đạt") + dem("đỏ"), dem("đạt"), len(bq), dem("chỉ_nt")
    e, g, h, v, i = len(_DB), hg("GIET"), hg("BO_QUA"), hg("CHI_NT"), hg("HONG"); f = e - h - v  # noqa: E702
    print("[%s] CA: dự_kiến=%d chạy=%d đạt=%d bỏ_qua=0 chỉ_nt=%d · LUOT: dự_kiến=%d chạy=%d đạt=%d bỏ_qua=%d chỉ_nt=%d · DOT BIEN: dự_kiến=%d chạy=%d giết_đúng=%d "
          "bỏ_qua=%d chỉ_nt=%d · HONG: %d · TU_KIEM: %d/%d · PC_DO: %d" % (TEST_ID, a, b, c, w, x, y, z, u, t, e, f, g, h, v, i, k, len(_TU_KIEM), len(pc)), file=sys.stderr)
    ve = {"ca_dat": b == c, "luot_dat": y == z, "giet_dung": f == g, "hong": i == 0, "so_ca": a == b + w, "tu_kiem": k == len(_TU_KIEM), "phan_chung": not pc,
          "so_luot": x == y + u + t == 7 and sorted(s[:2] for s in so) == sorted((ca, luot) for ca, ds in _LUOT_DU_KIEN.items() for luot in ds),
          "so_dot_bien": e == f + h + v == len(_DU_KIEN) and sorted(d[0] for d in _DB) == sorted(_DU_KIEN),
          "bo_qua": h == 0 and 0 <= u <= 2 and all(nt and s[0] == _N and s[1] in _BO_QUA_DUOC and isinstance(s[3], OSError) and getattr(s[3], "winerror", None) == 1314 for s in bq),
          "nen": (w, t, v) == (0, 0, 0) if nt else (w, t, v, u) == (1, 4, 1, 0)}
    if not all(ve.values()):
        print("[%s] VẾ SAI: %s" % (TEST_ID, ", ".join(n for n, dk in ve.items() if not dk)), file=sys.stderr)
    return all(ve.values())
def run(tl_module):
    ra, lstat_goc = io.StringIO(), os.lstat     # N3(e): mọi đầu ra ra STDERR (driver bundle đọc stdout làm JSON); `os.lstat` phải về hàm gốc
    with contextlib.redirect_stdout(ra):
        ok = _run(tl_module)
    return ok and not ra.getvalue() and os.lstat is lstat_goc
