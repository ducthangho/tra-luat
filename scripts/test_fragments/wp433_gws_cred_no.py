# -*- coding: utf-8 -*-
"""wp433 N — đóng bốn nợ trên đường ghi credential của `tl_gws.py` (spec GWS-CRED-DICH-NGOAI-KHO-N r1): `_chot_thu_muc` chốt liên kết ở
MỌI tổ tiên của HOME cho W6 và jar NLM (W1–W3); bundle giải mã không phải object ⇒ rc 3; `_trong_kho_git` ba trạng thái. Khuôn fragment R:
bản `tl_gws` nạp TRONG BỘ NHỚ (nguồn thật hoặc đột biến), HOME tạm, dữ liệu GIẢ, không mạng. Mỗi LƯỢT thu đủ hậu điều rồi so nhãn; nhãn đỏ
ĐẦU TIÊN thành `TinHieuChotCa(ca, lượt, nhãn)` — đột biến chỉ GIẾT khi khớp cả ba (bảng `_DB` chép §4b của spec)."""
import argparse, contextlib, io, json, os, pathlib, re, shutil, subprocess, sys, tempfile, types, urllib.request  # noqa: E401
TEST_ID = "wp433_gws_cred_no"
_MK, _TOK, _CU, _TEN_OS = "wp433-master-gia", "wp433-token-gia", b'{"cu": 1}', os.name
_JAR = {"auth.json": "a-wp433n", "profiles/default/cookies.json": "[]"}
_CUM = {"kho": "nằm trong kho git", "lk": "là liên kết tượng trưng", "dl": "dữ liệu không hợp lệ", "ghi": "ghi lỗi", "duong": "đường không hợp lệ"}
_T, _B, _G = "to_tien", "bundle_kieu", "ba_trang_thai"
_KIEU = (("list", [1, 2]), ("str", "x"), ("int", 7), ("null", None), ("true", True))
_BO_QUA_DUOC = ("W6.to_tien_lk", "W2.to_tien_lk", "W6.home_lk", "W1.to_tien_lk", "W3.to_tien_lk")   # N5: danh sách RIÊNG của fragment này
_LUOT_DU_KIEN = {  # N5 SỔ LƯỢT — viết RIÊNG khỏi các hàm ca, ĐÚNG THỨ TỰ §4: 11 + 12 + 4 = 27 lượt
    _T: ("W6.to_tien_lk", "W2.to_tien_lk", "W6.home_lk", "W1.to_tien_lk", "W3.to_tien_lk", "W6.kho", "W6.thuong", "W6.thuong_cwd_mat", "W6.goc",
         "W6.goc_o_mang", "W6.goc_o_co_dinh"),
    _B: ("bootstrap.list", "pull.list", "bootstrap.str", "pull.str", "bootstrap.int", "pull.int", "bootstrap.null", "pull.null", "bootstrap.true",
         "pull.true", "bootstrap.dict_rong", "pull.dict_rong"),
    _G: ("perm", "w6_ghi_loi", "notfound", "notdir")}
_CHI_NT = ("W6.goc_o_mang", "W6.goc_o_co_dinh")
_r = lambda x: repr(x)[:200]
_ch = lambda q: os.path.normcase(os.path.normpath(q))
class TinHieuChotCa(AssertionError):
    def __init__(self, ca, luot, nhan):
        super().__init__("%s · %s · %s" % (ca, luot, nhan)); self.ca, self.luot, self.nhan = ca, luot, nhan  # noqa: E702
def _nem(e):
    raise e
def _nap(nguon, tl_module, goc):
    """`compile`+`exec` nguồn vào module MỚI rồi `bind`; đường tải/cài thay bằng đồ giả, kho Drive giả `m.drive`; `m.lc_that` giữ
    `load_creds` GỐC (N3 bọc nó để chụp env, không thay), `m.dem_ac` đếm lời gọi nhánh agent (đồ giả, không mạng)."""
    m = types.ModuleType("wp433_tl_gws"); m.__file__ = goc.__file__  # noqa: E702
    exec(compile(nguon, goc.__file__, "exec"), m.__dict__)
    m.bind(tl_module)
    m.drive, m.dem_ac, m.lc_that, that_imp = {}, [], m.load_creds, m._imp
    for ten, tra in (("_public_curl_bytes", lambda fid, timeout=120.0: m.drive.get(fid)), ("_secrets_fetch", lambda a, fid: (m.drive.get(fid), "gia")),
                     ("_gas", lambda: _nem(RuntimeError("MANG_BI_CHAN"))), ("load_creds", lambda *a, **k: None),
                     ("_bootstrap_agent_creds", lambda master: (m.dem_ac.append(1), ("GIA", "wp433n"))[1]),
                     ("_imp", lambda n: types.SimpleNamespace(gws_exe=lambda: "gws-gia") if n == "gws_bridge" else that_imp(n))):
        setattr(m, ten, tra)
    return m
def _anh(goc):
    """Ảnh byte của mọi tệp dưới `goc` (đi theo đường THẬT): "T không đổi" = hai ảnh bằng nhau."""
    return sorted((os.path.relpath(os.path.join(d, t), goc), pathlib.Path(d, t).read_bytes()) for d, _ds, fs in os.walk(goc) for t in fs)
def _dong(err, the, cum, ct=None):
    """ĐÚNG MỘT dòng `✗` trong stderr, `fullmatch` `[thẻ] ✗ <cụm>: <chi tiết>`; `ct` (nếu nêu) là chi tiết nguyên văn."""
    x = [d for d in err if "✗" in d]
    return len(x) == 1 and re.fullmatch(r"\[%s\] ✗ %s: .+" % (re.escape(the), _CUM[cum]), x[0]) is not None and (ct is None or x[0].endswith(": " + ct))
class _Rig:
    """Một ca: thư mục tạm `realpath` (ngoài kho), HOME/USERPROFILE/CODEX_HOME/TL_*/cwd đặt tạm, khôi phục khi ra. `so` là SỔ LƯỢT dùng
    chung: mỗi lượt ghi đúng một trạng thái (`đạt` · `đỏ` · `bỏ_qua` · `chỉ_nt`). Bộ đếm của lời gọi gần nhất: `ghi` (đích writer), `mo`
    (mở `theo`), `ex` (`os.path.exists(theo)`), `ls` (mọi đối số `os.lstat`), `gc` (lần `os.getcwd` bị bọc), `env` (ảnh sau `load_creds`)."""
    def __init__(self, m, ca, store, so):
        self.m, self.ca, self.store, self.so, self.n = m, ca, store, so, 0
    def __enter__(self):
        td, self.cu_env, self.cu_cwd = os.path.realpath(tempfile.mkdtemp(prefix="wp433n-")), dict(os.environ), os.getcwd()
        self.td = td[:1].upper() + td[1:]                   # dạng mà parser nt của C1 trả về (chữ ổ HOA); POSIX: nguyên `/…`
        for k in [k for k in os.environ if k.startswith("TL_")]:
            os.environ.pop(k, None)
        os.environ.update(TL_MASTER_KEY=_MK, CODEX_HOME=self.p("cx"), GOOGLE_WORKSPACE_CLI_CONFIG_DIR=self.p("gws"))
        os.chdir(self.td); self.m.drive.clear(); self.home()  # noqa: E702
        return self
    def __exit__(self, *a):
        os.chdir(self.cu_cwd); os.environ.clear(); os.environ.update(self.cu_env); shutil.rmtree(self.td, ignore_errors=True)  # noqa: E702
    p = lambda self, *a: os.path.join(self.td, *a)
    def home(self, h=None, tao=True):
        """HOME MỚI cho lượt kế (mặc định `<td>/h<n>`, ngoài mọi kho); `TL_TOKEN`/`TL_WEBAPP` của lượt trước bị xoá."""
        self.n += 1; h = h or self.p("h%d" % self.n)  # noqa: E702
        if tao:
            os.makedirs(h, exist_ok=True)
        os.environ.pop("TL_TOKEN", None); os.environ.pop("TL_WEBAPP", None)  # noqa: E702
        os.environ["HOME"] = os.environ["USERPROFILE"] = self.h = h
        self.cfg = os.path.join(h, ".tra_luat_config.json")
        return h
    def do(self, luot, nhan, e=None):
        self.so.append((self.ca, luot, "đỏ", None))
        raise TinHieuChotCa(self.ca, luot, nhan) from e
    def xs(self, luot, **nhan):
        """Kết thúc MỘT lượt: hậu điều đã thu đủ (theo thứ tự ghi); nhãn đỏ đầu tiên ⇒ `đỏ` + tín hiệu, không thì `đạt`."""
        hong = [n for n, dk in nhan.items() if not dk]
        if hong:
            self.do(luot, hong[0])
        self.so.append((self.ca, luot, "đạt", None))
    def lk(self, luot, home_la_lk):
        """Fixture liên kết của CHÍNH lượt: L (symlink) → T ngoài kho, config cũ đặt sẵn ở T. HOME = L (`home_la_lk`) hoặc `<L>/home`.
        Trả (L, T) hoặc None khi lượt được `bỏ_qua` — chỉ nt + `winerror == 1314` từ probe `os.symlink` này; lỗi probe khác ⇒ `đỏ`."""
        self.n += 1; L, T = self.p("L%d" % self.n), self.p("T%d" % self.n)  # noqa: E702
        os.makedirs(os.path.join(T, "home"))
        for d in (T, os.path.join(T, "home")):
            pathlib.Path(d, ".tra_luat_config.json").write_bytes(_CU)
        try:
            os.symlink(T, L, target_is_directory=True)
        except OSError as e:
            if not (_TEN_OS == "nt" and getattr(e, "winerror", None) == 1314):
                self.do(luot, "probe symlink: %r" % ((type(e).__name__, e.errno, getattr(e, "winerror", None)),))
            self.so.append((self.ca, luot, "bỏ_qua", e))
            return None
        self.home(L if home_la_lk else os.path.join(L, "home"), tao=False)
        return L, T
    def goi(self, luot, fn, nem=None, theo=None, cwd=None, lc=False, bat=()):
        """Một LƯỢT GỌI: chặn tiến trình con/mạng, stdout/stderr RIÊNG; bọc writer, `open` (trong không gian tên `tl_gws`), `os.path.exists`,
        `os.lstat` (`nem=(đường, lớp lỗi)`: ĐÚNG đường ấy, so sau `normcase(normpath)`, ném lỗi giả; đường khác đi hàm thật), `_chot_thu_muc`
        (`cwd`: `os.getcwd` thay bằng `cwd` CHỈ trong cửa sổ chốt), `load_creds` (`lc`: gọi hàm GỐC rồi chụp env). Mọi thứ đã thay khôi phục
        trong `finally`. `AssertionError` đi THẲNG ra; ngoại lệ thuộc `bat` trả về cho lượt xét; ngoại lệ khác ⇒ `ngoai_le_la`.
        Trả (kết quả | ngoại lệ, stdout, [dòng stderr])."""
        out, err, m, kq = io.StringIO(), io.StringIO(), self.m, None
        self.ghi, self.mo, self.ex, self.ls, self.gc, self.env, m.dem_ac[:] = [], 0, 0, [], 0, None, []
        cu = (subprocess.run, subprocess.Popen, urllib.request.urlopen, os.lstat, os.path.exists, os.getcwd, m._ghi_nguyen_tu_0600, m._chot_thu_muc, m.load_creds)
        subprocess.run = subprocess.Popen = urllib.request.urlopen = lambda *a, **k: _nem(RuntimeError("MANG_BI_CHAN"))
        trung = lambda q: theo is not None and isinstance(q, str) and _ch(q) == _ch(theo)
        def ls(q, *a, **k):
            self.ls.append(_ch(q) if isinstance(q, str) else q)
            if nem and isinstance(q, str) and _ch(q) == _ch(nem[0]):
                raise nem[1](13, "wp433n-lstat-gia")
            return cu[3](q, *a, **k)
        def ex(q):
            self.ex += trung(q)
            return cu[4](q)
        def mo(q, *a, **k):
            self.mo += trung(q)
            return open(q, *a, **k)
        def wr(path, data):
            self.ghi.append(_ch(path))
            return cu[6](path, data)
        def chot(d):
            if cwd is None:
                return cu[7](d)
            def gc():
                self.gc += 1
                return cwd()
            os.getcwd = gc
            try:
                return cu[7](d)
            finally:
                os.getcwd = cu[5]
        def nap_cred(*a, **k):
            try:
                return m.lc_that(*a, **k)
            finally:
                self.env = (os.environ.get("TL_TOKEN"), os.environ.get("TL_WEBAPP"))
        os.lstat, os.path.exists, m._ghi_nguyen_tu_0600, m._chot_thu_muc, m.open = ls, ex, wr, chot, mo
        if lc:
            m.load_creds = nap_cred
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                kq = fn()
        except AssertionError:
            raise
        except bat as e:
            kq = e
        except Exception as e:  # noqa: BLE001 — biên của lượt
            self.do(luot, "ngoai_le_la", e)
        finally:
            subprocess.run, subprocess.Popen, urllib.request.urlopen, os.lstat, os.path.exists, os.getcwd, m._ghi_nguyen_tu_0600, m._chot_thu_muc, m.load_creds = cu
            del m.open
        return kq, out.getvalue(), [d for d in err.getvalue().splitlines() if d.strip()]
    def lenh(self, luot, lenh, goi, env="chat", **kw):
        """`bootstrap` (`--env <env> --no-gws --no-nlm`) hoặc `nlm-auth-pull` trên bundle `goi` (đối tượng JSON bất kỳ) mã hoá bằng master giả."""
        self.m.drive["S433"] = self.store.encrypt(json.dumps(goi).encode("utf-8"), _MK)
        ns = argparse.Namespace(secrets_id="S433", secrets_file=None, env=env, config=None, profile=None, no_gws=True, no_nlm=True, bindir=None, require_agent_creds=False)
        return self.goi(luot, lambda: (self.m.cmd_bootstrap if lenh == "bootstrap" else self.m.cmd_nlm_auth_pull)(ns), **kw)
    def w6(self, luot, **kw):
        """Lượt W6: `bootstrap --env chat` (không W4/W2, không cài đặt), bundle CHỈ `token`, `load_creds` giả (cô lập khỏi đích merge)."""
        return self.lenh(luot, "bootstrap", {"token": _TOK}, theo=self.cfg, **kw)
def _w6_lk(r, luot, home_la_lk):
    """`W6.to_tien_lk` / `W6.home_lk`: nhãn `lk` CHỈ cho phản chứng xác định — mất từ chối VÀ writer được gọi đúng `cfgp` VÀ byte ở T đổi."""
    f = r.lk(luot, home_la_lk)
    if f is None:
        return
    L, T = f; truoc = _anh(T); rc, out, err = r.w6(luot)  # noqa: E702
    tu_choi, doi = rc == 1 and _dong(err, "bootstrap", "lk", _r(L)), _anh(T) != truoc
    r.xs(luot, lk=not (not tu_choi and _ch(r.cfg) in r.ghi and doi), dong_loi=tu_choi, ghi_khac=not r.ghi and not doi, doc_truoc=(r.ex, r.mo) == (0, 0),
         token=os.environ.get("TL_TOKEN") == _TOK, khong_ok="✓ config" not in out)
def _jar_lk(r, luot, fn):
    """`W1/W2/W3.to_tien_lk`: HOME = `<L>/home`; `fn(r)` trả (từ chối đúng cụm `lk` chi tiết `repr(L)`?) sau khi gọi đường ghi jar."""
    f = r.lk(luot, False)
    if f is None:
        return
    L, T = f; truoc = _anh(T); tu_choi = fn(r, luot, L); doi = _anh(T) != truoc  # noqa: E702
    jar = [g for g in r.ghi if g.startswith(_ch(os.path.join(r.h, ".notebooklm-mcp-cli")) + os.sep)]
    r.xs(luot, lk=not (not tu_choi and jar and doi), dong_loi=tu_choi, ghi_khac=not r.ghi and not doi)
def _w1(r, luot, L):
    rc, _o, err = r.lenh(luot, "nlm-auth-pull", {"nlm_auth": _JAR})
    return rc == 1 and _dong(err, "nlm-auth-pull", "lk", _r(L))
def _w2(r, luot, L):          # bundle CHỈ `nlm_auth` (không `token`, không `gws_cred`) ⇒ dòng `lk` chỉ có thể đến từ jar
    rc, _o, err = r.lenh(luot, "bootstrap", {"nlm_auth": _JAR}, env="code")
    return rc == 1 and _dong(err, "bootstrap", "lk", _r(L))
def _w3(r, luot, L):
    r.m.drive["N433"] = r.store.encrypt(json.dumps(_JAR).encode("utf-8"), _TOK)
    return r.goi(luot, lambda: r.m._nlm_auth_load(_TOK, "N433"))[0] == (False, _CUM["lk"] + ": " + _r(L))
def _w6_kho(r):
    """`W6.kho` (hồi quy): HOME trong kho ⇒ cụm `kho`, writer 0, KHÔNG `exists`/mở đọc `cfgp` (thứ tự đọc — phản chứng `pc_doc_truoc`)."""
    k = r.p("K%d" % r.n); os.makedirs(os.path.join(k, ".git")); r.home(os.path.join(k, "home"))  # noqa: E702
    pathlib.Path(r.cfg).write_bytes(_CU)
    rc, _o, err = r.w6("W6.kho")
    r.xs("W6.kho", kho=rc == 1 and _dong(err, "bootstrap", "kho", _r(k)), khong_ghi=not r.ghi and pathlib.Path(r.cfg).read_bytes() == _CU, doc_truoc=(r.ex, r.mo) == (0, 0))
def _goc(r):
    """`W6.goc`: `_chot_thu_muc` với gốc của nền viết trực tiếp VÀ với `.` khi cwd giả lập là gốc ⇒ None, ĐÚNG một `lstat`, trên gốc chuẩn."""
    goc = "/" if _TEN_OS == "posix" else os.path.splitdrive(r.td)[0].upper() + "\\"
    a = r.goi("W6.goc", lambda: r.m._chot_thu_muc(goc))[0], list(r.ls)
    b = r.goi("W6.goc", lambda: r.m._chot_thu_muc("."), cwd=lambda: goc)[0], list(r.ls), r.gc
    r.xs("W6.goc", goc_truc_tiep=a == (None, [_ch(goc)]), goc_tuong_doi=b == (None, [_ch(goc)], 1))
    for luot, loai, mong in (("W6.goc_o_mang", 4, (_CUM["duong"] + ": " + _r(goc), [])), ("W6.goc_o_co_dinh", 3, (None, [_ch(goc)]))):
        if _TEN_OS != "nt":
            r.so.append((r.ca, luot, "chỉ_nt", None))
            continue
        cu, r.m._loai_o_nt = r.m._loai_o_nt, lambda g, _l=loai: _l      # bộ đo loại ổ GIẢ; khôi phục ngay sau lời gọi
        try:
            kq = r.goi(luot, lambda: r.m._chot_thu_muc(goc))[0], list(r.ls)
        finally:
            r.m._loai_o_nt = cu
        r.xs(luot, loai_o=kq == mong)
def to_tien(r):
    _w6_lk(r, "W6.to_tien_lk", False)
    _jar_lk(r, "W2.to_tien_lk", _w2)
    _w6_lk(r, "W6.home_lk", True)
    _jar_lk(r, "W1.to_tien_lk", _w1)
    _jar_lk(r, "W3.to_tien_lk", _w3)
    _w6_kho(r)
    for luot, cwd in (("W6.thuong", None), ("W6.thuong_cwd_mat", lambda: _nem(FileNotFoundError(2, "wp433n-cwd-mat")))):
        r.home(); pathlib.Path(r.cfg).write_bytes(_CU)  # noqa: E702
        rc, out, err = r.w6(luot, cwd=cwd)
        cfg = json.loads(pathlib.Path(r.cfg).read_bytes())
        r.xs(luot, merge=rc == 0 and not err and cfg == {"cu": 1, "token": _TOK} and "✓ config" in out, ghi_dung=r.ghi == [_ch(r.cfg)],
             cwd_khong_goi=r.gc == 0, khong_tam=os.listdir(r.h) == [".tra_luat_config.json"])
    _goc(r)
def bundle_kieu(r):
    """N3: bundle JSON hợp lệ mà không phải object ⇒ rc 3, một dòng `✗`, không gán env TỪ BUNDLE, không ghi, không nhánh agent."""
    pathlib.Path(r.p("tra_luat_config.v2.json")).write_text(json.dumps({"token": "wp433n-cfg-tok", "webappUrl": "https://wp433n.invalid/x"}), encoding="utf-8")   # ứng viên ĐẦU TIÊN của `load_creds` gốc (cwd)
    for ten, goi in _KIEU + (("dict_rong", {}),):
        for lenh, ham in (("bootstrap", "cmd_bootstrap"), ("pull", "cmd_nlm_auth_pull")):
            luot, the = "%s.%s" % (lenh, ten), "bootstrap" if lenh == "bootstrap" else "nlm-auth-pull"
            r.home(); truoc = _anh(r.td)  # noqa: E702
            kq, out, err = r.lenh(luot, the, goi, lc=True, bat=(AttributeError,) if ten == "list" else ())
            if isinstance(kq, AttributeError):   # CHỈ `.get` trên list, ném từ CHÍNH hàm lệnh đích, mới là tín hiệu `rc3`; lỗi khác là lỗi giàn
                tb = kq.__traceback__
                while tb.tb_next:
                    tb = tb.tb_next
                if not (kq.name == "get" and type(kq.obj) is list and tb.tb_frame.f_code.co_name == ham):
                    raise kq
                r.do(luot, "rc3", kq)
            sach = not r.ghi and not r.m.dem_ac and _anh(r.td) == truoc and r.env is not None and (os.environ.get("TL_TOKEN"), os.environ.get("TL_WEBAPP")) == r.env
            if ten == "dict_rong":   # hồi quy: dict rỗng giữ hành vi base (bootstrap: thiếu token ⇒ rc 0 ở env chat; pull: chưa có nlm_auth ⇒ rc 1)
                r.xs(luot, dict_rong=(kq, len(err), bool(r.ghi)) == ((0, 1, False) if lenh == "bootstrap" else (1, 1, False)) and "dữ liệu không hợp lệ" not in "".join(err)
                     and ("bundle giải mã OK" in out and len(r.m.dem_ac) == 1 if lenh == "bootstrap" else True))
            else:
                r.xs(luot, rc3=kq == 3, mot_dong=err == ["[%s] ✗ dữ liệu không hợp lệ: bundle" % the], stdout="bundle giải mã OK" not in out and "agent_creds:" not in out, sach=sach)
def ba_trang_thai(r):
    """N4: `_trong_kho_git` chỉ coi `FileNotFoundError`/`NotADirectoryError` ở `<d>/.git` là "chưa có"; lỗi `lstat` khác LAN RA."""
    cha = r.p("cha"); k = os.path.join(cha, "K"); con = os.path.join(k, "con"); git = os.path.join(k, ".git")  # noqa: E702
    for d in (os.path.join(cha, ".git"), git, os.path.join(con, "h")):
        os.makedirs(d)
    kq = r.goi("perm", lambda: r.m._trong_kho_git(con), nem=(git, PermissionError), bat=(PermissionError,))[0]
    r.xs("perm", lan_ra=isinstance(kq, PermissionError) and kq.errno == 13, trung=r.ls.count(_ch(git)) == 1)
    r.home(os.path.join(con, "h"))
    rc, _o, err = r.w6("w6_ghi_loi", nem=(git, PermissionError))
    r.xs("w6_ghi_loi", ghi_loi=rc == 1 and _dong(err, "bootstrap", "ghi"), khong_ghi=not r.ghi and not os.listdir(r.h), trung=r.ls.count(_ch(git)) >= 1)
    for luot, loi in (("notfound", FileNotFoundError), ("notdir", NotADirectoryError)):   # "chưa có" ⇒ đi tiếp ĐÚNG tới kho cha (mốc dương)
        kq = r.goi(luot, lambda: r.m._trong_kho_git(con), nem=(git, loi))[0]
        r.xs(luot, kho_cha=isinstance(kq, str) and _ch(kq) == _ch(cha), trung=r.ls.count(_ch(git)) == 1)
_CA = (to_tien, bundle_kieu, ba_trang_thai)
_DU_KIEN = ("db_w6_bo_chot_thu_muc", "db_bootstrap_bo_kiem_bundle", "db_pull_bo_kiem_bundle", "db_jar_bo_chot_thu_muc", "db_nuot_oserror")  # N5: ID dự kiến (§4b) — viết RIÊNG khỏi `_DB`
_KB = '    if not isinstance(bundle, dict):   # WP433 N: %s\n        print("[%s] ✗ dữ liệu không hợp lệ: bundle", file=sys.stderr)\n        return 3\n'
_KB_B, _KB_P = _KB % ("trước mọi phép gán env/ghi tệp/nhánh agent", "bootstrap"), _KB % ("JSON hợp lệ mà không phải object ⇒ từ chối như giải mã lỗi, không traceback", "nlm-auth-pull")
_EX = "            except (FileNotFoundError, NotADirectoryError):\n                pass\n            if os.path.dirname(d) == d:\n"
_VAO = "    for d in dict.fromkeys((os.path.abspath(path), os.path.realpath(path))):\n"
_DB = (  # §4b: (đột biến, [(neo khớp ĐÚNG MỘT lần trên nguồn candidate, thay)…], ca đích, lượt, nhãn)
    ("db_w6_bo_chot_thu_muc", [("            ly_cfg = ly_cfg or _chot_thu_muc(os.path.dirname(cfgp))\n", "")], _T, "W6.to_tien_lk", "lk"),
    ("db_bootstrap_bo_kiem_bundle", [(_KB_B, "")], _B, "bootstrap.list", "rc3"),
    ("db_pull_bo_kiem_bundle", [(_KB_P, "")], _B, "pull.list", "rc3"),
    ("db_jar_bo_chot_thu_muc", [("    return _chot_thu_muc(os.path.dirname(nbase))\n", "    return None\n")], _T, "W2.to_tien_lk", "lk"),
    ("db_nuot_oserror", [(_EX, _EX.replace("(FileNotFoundError, NotADirectoryError)", "OSError"))], _G, "perm", "lan_ra"))
_GIA = ('    class TinGia(AssertionError):\n        ca, luot, nhan = "ba_trang_thai", "perm", "lan_ra"\n    try:\n        raise AttributeError("wp433-n-tu-kiem")\n'
        '    except Exception:\n        raise TinGia("wp433-n-tu-kiem")\n')
_TU_KIEM = (  # N5: bộ phân hạng KHÔNG được cấp tín dụng — (tên, cặp, ca, lượt, nhãn, hạng mong đợi)
    ("tu_kiem_doi_kieu", [(_VAO, _GIA + _VAO)], _G, "perm", "lan_ra", "TIN_DUNG_GIA"),       # lớp giả mang ĐỦ tuple, sinh từ `except` đổi kiểu
    ("tu_kiem_chu_thich", [("\ndef _chot_thu_muc(", "\n# vô hại\ndef _chot_thu_muc(")], _G, "perm", "lan_ra", "SONG_SOT"),
    ("tu_kiem_sai_luot", [(_KB_B, "")], _B, "pull.list", "rc3", "TIN_DUNG_GIA"),             # CHÍNH đột biến 2, giữ ca + nhãn, chỉ đổi lượt khai
)
_PC_DOC = [("            if ly_cfg is None and os.path.exists(cfgp):\n", "            if os.path.exists(cfgp):\n")]   # tự kiểm rig: đọc TRƯỚC chốt
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
            next(c for c in _CA if c.__name__ == ca)(r)
    except TinHieuChotCa as e:
        return ("GIET" if (e.ca, e.luot, e.nhan) == (ca, luot, nhan) else "TIN_DUNG_GIA"), e
    except BaseException as e:  # noqa: BLE001 — kể cả AssertionError KHÔNG phải `TinHieuChotCa` dù mang đủ tuple
        return "TIN_DUNG_GIA", e
    return ("BO_QUA" if (ca, luot, "bỏ_qua") in [x[:3] for x in so] else "SONG_SOT"), None
def _phan_chung(nguon, tl_module, goc, store):
    """Phản chứng BỘ ĐO (không phải mục `_DB`): bản bỏ điều kiện `ly_cfg is None` trước `exists` phải ĐỎ ở `W6.kho` · `doc_truoc`, và
    riêng lượt ấy trên nguồn thật phải đạt. Trả danh sách tên phản chứng ĐỎ."""
    ra = []
    for cap in ([], _PC_DOC):
        m, so, tin = _ban_sao(nguon, tl_module, goc, cap), [], None
        if m is not None:
            with _Rig(m, _T, store, so) as r:
                try:
                    _w6_kho(r)
                except TinHieuChotCa as e:
                    tin = (e.ca, e.luot, e.nhan)
        ra.append((m is not None, tin, [s[:3] for s in so]))
    dat = ra == [(True, None, [(_T, "W6.kho", "đạt")]), (True, (_T, "W6.kho", "doc_truoc"), [(_T, "W6.kho", "đỏ")])]
    return [] if dat else ["pc_doc_truoc"]
def _run(tl_module):
    goc = tl_module._imp("tl_gws"); goc.bind(tl_module)  # noqa: E702
    nguon, store, nt = pathlib.Path(goc.__file__).read_text(encoding="utf-8"), tl_module._imp("gws_cred_store"), _TEN_OS == "nt"
    m, so, c = _nap(nguon, tl_module, goc), [], 0
    for ca in _CA:
        try:
            with _Rig(m, ca.__name__, store, so) as r:
                ca(r)
            c += 1
        except Exception as e:  # noqa: BLE001
            print("[%s] ĐỎ %s: %r (%r)" % (TEST_ID, ca.__name__, e, e.__cause__), file=sys.stderr)
    bq = [s for s in so if s[2] == "bỏ_qua"]
    for s in bq:
        print("[%s] BO_QUA %s·%s: %r" % (TEST_ID, s[0], s[1], s[3]), file=sys.stderr)
    kq = {d[0]: _hang(nguon, tl_module, goc, store, *d[1:])[0] for d in _DB}
    tk = [(d[0], d[5]) + _hang(nguon, tl_module, goc, store, *d[1:5]) for d in _TU_KIEM]
    doi = lambda e: isinstance(getattr(e, "__context__", None), AttributeError) and (e.ca, e.luot, e.nhan) == (_G, "perm", "lan_ra")   # đủ tuple, đã qua `except` đổi kiểu
    k, pc = sum(h == mong and (ten != "tu_kiem_doi_kieu" or doi(e)) for ten, mong, h, e in tk), _phan_chung(nguon, tl_module, goc, store)
    for ten, hang in list(kq.items()) + [(ten, "tự kiểm %s ≠ %s" % (h, mong)) for ten, mong, h, _e in tk if h != mong] + [(ten, "phản chứng bộ đo ĐỎ") for ten in pc]:
        if hang not in ("GIET", "BO_QUA"):
            print("[%s] ĐỘT BIẾN %s: %s" % (TEST_ID, ten, hang), file=sys.stderr)
    dem, hg = lambda tt: sum(s[2] == tt for s in so), lambda tt: sum(h == tt for h in kq.values())
    a, x, y, z, u, t = len(_LUOT_DU_KIEN), sum(map(len, _LUOT_DU_KIEN.values())), dem("đạt") + dem("đỏ"), dem("đạt"), len(bq), dem("chỉ_nt")
    e, g, h, i = len(_DB), hg("GIET"), hg("BO_QUA"), hg("HONG"); f = e - h  # noqa: E702
    print("[%s] CA: dự_kiến=%d chạy=%d đạt=%d · LUOT: dự_kiến=%d chạy=%d đạt=%d bỏ_qua=%d chỉ_nt=%d · DOT BIEN: dự_kiến=%d chạy=%d giết_đúng=%d bỏ_qua=%d · "
          "HONG: %d · TU_KIEM: %d/%d · PC_DO: %d" % (TEST_ID, a, len(_CA), c, x, y, z, u, t, e, f, g, h, i, k, len(_TU_KIEM), len(pc)), file=sys.stderr)
    bq_luot = {s[1] for s in bq}
    ve = {"ca_dat": c == len(_CA) == a, "luot_dat": y == z, "giet_dung": f == g, "hong": i == 0, "tu_kiem": k == len(_TU_KIEM), "phan_chung": not pc,
          "so_luot": x == y + u + t == 27 and [s[:2] for s in so] == [(ca, luot) for ca, ds in _LUOT_DU_KIEN.items() for luot in ds],
          "so_dot_bien": e == f + h == len(_DU_KIEN) and sorted(d[0] for d in _DB) == sorted(_DU_KIEN),
          "bo_qua": all(nt and s[0] == _T and s[1] in _BO_QUA_DUOC and isinstance(s[3], OSError) and getattr(s[3], "winerror", None) == 1314 for s in bq)
          and all((hang == "BO_QUA") == (d[3] in bq_luot) for d, hang in zip(_DB, kq.values())),
          "nen": sorted(s[1] for s in so if s[2] == "chỉ_nt") == ([] if nt else sorted(_CHI_NT)) and (nt or u == 0)}
    if not all(ve.values()):
        print("[%s] VẾ SAI: %s" % (TEST_ID, ", ".join(n for n, dk in ve.items() if not dk)), file=sys.stderr)
    return all(ve.values())
def run(tl_module):
    ra, cu = io.StringIO(), (os.lstat, os.path.exists, os.getcwd)     # N5: mọi đầu ra ra STDERR (driver bundle đọc stdout làm JSON); hàm đã bọc phải về gốc
    with contextlib.redirect_stdout(ra):
        ok = _run(tl_module)
    return ok and not ra.getvalue() and (os.lstat, os.path.exists, os.getcwd) == cu
