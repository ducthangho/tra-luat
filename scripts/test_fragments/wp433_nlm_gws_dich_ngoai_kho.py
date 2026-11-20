# -*- coding: utf-8 -*-
"""wp433 — đích ghi credential NLM (W1 `nlm-auth-pull`, W2 `bootstrap`, W3 `_nlm_auth_load`) và `~/.tra_luat_config.json`
(W6) của `tl_gws.py`: qua danh sách cho phép, ngoài kho git, không xuyên symlink, ghi nguyên tử (spec NLM-GWS-DICH-NGOAI-KHO r1).
Mọi ca chạy trên bản `tl_gws` nạp TRONG BỘ NHỚ (nguồn thật hoặc đột biến), HOME tạm, dữ liệu GIẢ, không mạng. Nhãn hậu điều
thuộc (ca, lượt); đột biến chỉ GIẾT khi đúng ca ném `TinHieuChotCa` mang đúng (lượt, nhãn) — bảng `_DB` chép §4b của spec."""
import argparse, builtins, contextlib, io, json, os, pathlib, re, shutil, stat, subprocess, sys, tempfile, types, urllib.request  # noqa: E401
TEST_ID = "wp433_nlm_gws_dich_ngoai_kho"
_SENT, _MK, _TOK = "SENTINEL-wp433-gia", "wp433-master-gia", "wp433-token-gia"
_BA = {"auth.json": "a-wp433", "profiles/default/cookies.json": "[]", "profiles/default/metadata.json": "{}"}
_LA, _KHAC = {"auth.json": "a", "../thoat.json": _SENT}, {"auth.json": "a", "khac.json": _SENT}
_CUM = {"kho": "nằm trong kho git", "lk": "là liên kết tượng trưng", "ds": "ngoài danh sách cho phép", "dl": "dữ liệu không hợp lệ", "ghi": "ghi lỗi"}
_KHAI = {**{"N3.1-" + w: (AttributeError, "'list' object has no attribute 'items'", "kieu_jar") for w in ("W1", "W2")},   # §4b cột "ngoại lệ khai": lượt → (loại, dấu, nhãn)
         "N3.3": (UnicodeEncodeError, "surrogates not allowed", "surrogate_jar"), "N8.4-W1": (OSError, "wp433-oserror", "oserror_w1"),
         **{"N8.1-%s-%s" % (w, ly): (ValueError, "wp433-nem", "khong_nem") for w in ("W1", "W2") for ly in ("kho", "lien_ket", "danh_sach")}}
class TinHieuChotCa(AssertionError):
    def __init__(self, ca, nhan):
        super().__init__("%s: %s" % (ca, sorted(nhan))); self.ca, self.nhan = ca, frozenset(nhan)  # noqa: E702
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
    m.AGENT_CREDS_FILEID = ""          # spec §0.2 S6: biến rỗng rơi về hằng baked ⇒ xoá cả hằng
    return m
_ghi = lambda p, s: pathlib.Path(p).write_bytes(s.encode("utf-8"))
_doc = lambda p: pathlib.Path(p).read_bytes()
_tep = lambda goc: sorted(os.path.relpath(os.path.join(d, t), goc) for d, _ds, fs in os.walk(goc) for t in fs)
_thoat = lambda r: not any("thoat.json" in fs for _d, _ds, fs in os.walk(r.td))
_ac = lambda out: out.count("agent_creds:") == 1
_ly = lambda msg, c: isinstance(msg, str) and "\n" not in msg and re.fullmatch(_CUM[c] + ": .*", msg) is not None
def _dung(err, the, *cum):
    """"stderr đúng": đúng số dòng, mỗi dòng `fullmatch` `[thẻ] ✗ <cụm>: <chi tiết>` (cụm nhận diện ở PHẦN CỐ ĐỊNH đầu dòng)."""
    return len(err) == len(cum) and all(re.fullmatch(r"\[%s\] ✗ %s: .*" % (the, _CUM[c]), d) for c, d in zip(cum, err))
def _anh(k):
    """Ảnh của kho K (trừ `.git`): mọi thư mục/tệp + byte, kèm `git status --porcelain` khi có git — "sạch(K)" = ảnh không đổi."""
    ra = []
    for d, ds, fs in os.walk(k):
        if d == k and ".git" in ds:
            ds.remove(".git")
        ra += [(os.path.join(d, t), None) for t in ds] + [(os.path.join(d, t), _doc(os.path.join(d, t))) for t in fs]
    git = shutil.which("git") and subprocess.run(["git", "-C", k, "status", "--porcelain", "--untracked-files=all"], capture_output=True).stdout
    return sorted(ra), git or b""
class _Rig:
    """Một ca: thư mục tạm, HOME/USERPROFILE/CODEX_HOME/GOOGLE_WORKSPACE_CLI_CONFIG_DIR/TL_*/cwd đặt tạm, khôi phục khi ra."""
    def __init__(self, m, ca, store, lk):
        self.m, self.ca, self.store, self.lk, self.hong, self.n = m, ca, store, lk, set(), 0
    def __enter__(self):
        self.td, self.cu_env, self.cu_cwd = os.path.realpath(tempfile.mkdtemp(prefix="wp433-")), dict(os.environ), os.getcwd()
        for k in [k for k in os.environ if k.startswith("TL_")] + ["CLAUDE_CODE_OAUTH_TOKEN", "GEMINI_API_KEY"]:
            os.environ.pop(k, None)
        os.environ.update(TL_MASTER_KEY=_MK, CODEX_HOME=self.p("cx"), GOOGLE_WORKSPACE_CLI_CONFIG_DIR=self.p("gws"))
        os.chdir(self.td); self.m.drive.clear(); self.home()  # noqa: E702
        return self
    def __exit__(self, *a):
        os.chdir(self.cu_cwd); os.environ.clear(); os.environ.update(self.cu_env); shutil.rmtree(self.td, ignore_errors=True)  # noqa: E702
    p = lambda self, *a: os.path.join(self.td, *a)
    def home(self, kho=None):
        """HOME MỚI cho lượt kế (ngoài mọi kho, hoặc `<kho>/home`) — lượt sau không thấy tệp của lượt trước."""
        self.n += 1
        h = os.path.join(kho, "home") if kho else self.p("h%d" % self.n)
        os.makedirs(h); os.environ["HOME"] = os.environ["USERPROFILE"] = h  # noqa: E702
        self.nlm, self.cfg = os.path.join(h, ".notebooklm-mcp-cli"), os.path.join(h, ".tra_luat_config.json")
    def kho(self, ten="K"):
        k = self.p(ten); os.makedirs(k)  # noqa: E702
        if not (shutil.which("git") and subprocess.run(["git", "init", "-q", k], capture_output=True).returncode == 0):
            os.makedirs(os.path.join(k, ".git"), exist_ok=True)
        return k
    def lk_goc(self):
        """`~/.notebooklm-mcp-cli` là symlink tới thư mục T ngoài mọi kho; trả T."""
        t = self.p("T%d" % self.n); os.makedirs(t); os.symlink(t, self.nlm, target_is_directory=True)  # noqa: E702
        return t
    def xs(self, luot="-", **nhan):
        self.hong |= {(luot, n) for n, dk in nhan.items() if not dk}
    def goi(self, luot, fn, thay=None, theo=None):
        """Một LƯỢT GỌI. Cửa sổ: chặn tiến trình con/mạng (`MANG_BI_CHAN`), stdout/stderr RIÊNG, `os.replace` ném khi `thay(đích)`,
        `theo=[đường]` ghi lại mọi lần mở đường ấy. Ngoại lệ khớp tập khai CỦA LƯỢT ⇒ nhãn; ngoài tập ⇒ ca dừng với `ngoai_le_la`."""
        out, err, kq = io.StringIO(), io.StringIO(), None
        cu = (subprocess.run, subprocess.Popen, urllib.request.urlopen, os.replace, builtins.open, io.open, pathlib.Path.read_text, pathlib.Path.read_bytes)
        subprocess.run = subprocess.Popen = urllib.request.urlopen = lambda *a, **k: _nem(RuntimeError("MANG_BI_CHAN"))
        if thay:
            os.replace = lambda s, d: _nem(OSError("wp433-oserror")) if thay(d) else cu[3](s, d)
        def boc(f):
            def g(p, *a, **k):
                if isinstance(p, (str, os.PathLike)) and os.path.abspath(os.fspath(p)) == theo[0]:
                    theo.append(1)
                return f(p, *a, **k)
            return g
        if theo:
            builtins.open, io.open, pathlib.Path.read_text, pathlib.Path.read_bytes = map(boc, cu[4:])
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                kq = fn()
        except Exception as e:  # noqa: BLE001 — biên của lượt: chỉ tập ĐÓNG đã khai mới thành nhãn
            lo, dau, nhan = _KHAI.get(luot, (None, "", ""))
            if not (lo and isinstance(e, lo) and dau in str(e)):
                raise TinHieuChotCa(self.ca, self.hong | {(luot, "ngoai_le_la")}) from e
            self.hong.add((luot, nhan))
        finally:
            subprocess.run, subprocess.Popen, urllib.request.urlopen, os.replace, builtins.open, io.open, pathlib.Path.read_text, pathlib.Path.read_bytes = cu
        self.xs(luot, khong_lo_gia_tri=_SENT not in out.getvalue() + err.getvalue())
        return kq, out.getvalue(), [d for d in err.getvalue().splitlines() if d.strip()]
    def _ma(self, goi):
        return self.store.encrypt(goi if isinstance(goi, bytes) else json.dumps(goi).encode("utf-8"), _MK)
    def w1(self, luot, jar, **kw):          # `jar` là bytes ⇒ cả bundle thô (ca surrogate)
        self.m.drive["S433"] = self._ma(jar if isinstance(jar, bytes) else {"nlm_auth": jar})
        ns = argparse.Namespace(config=None, profile=None, secrets_id="S433", secrets_file=None, env=None)
        return self.goi(luot, lambda: self.m.cmd_nlm_auth_pull(ns), **kw)
    def w2(self, luot, them, env="code", req=False, **kw):
        """Fixture bootstrap chuẩn: `--env code --no-nlm --no-gws`, bundle có token + gws_cred, agent KHÔNG CẤU HÌNH, gws_exe giả."""
        self.m.drive["S433"] = self._ma({"token": _TOK, "gws_cred": "{}", **them})
        ns = argparse.Namespace(secrets_id="S433", secrets_file=None, env=env, config=None, profile=None, no_gws=True, no_nlm=True, bindir=None, require_agent_creds=req)
        return self.goi(luot, lambda: self.m.cmd_bootstrap(ns), **kw)
    def w3(self, luot, jar):
        self.m.drive["N433"] = self.store.encrypt(json.dumps(jar).encode("utf-8"), _TOK)
        kq, out, err = self.goi(luot, lambda: self.m._nlm_auth_load(_TOK, "N433"))
        return (kq or (None, "")) + (out, err)
def w1_pull_rel_thoat(r):
    rc, _o, err = r.w1("-", _LA)
    r.xs(khong_thoat=_thoat(r), khong_jar=not _tep(r.nlm), ma=rc == 1, stderr=_dung(err, "nlm-auth-pull", "ds"))
def w2_bootstrap_rel_thoat(r):
    _ghi(r.cfg, json.dumps({"nlm_auth": {"auth.json": "CU-wp433"}}))
    rc, out, err = r.w2("-", {"nlm_auth": _LA})
    cfg = json.loads(_doc(r.cfg))
    r.xs(khong_thoat=_thoat(r), khong_jar=not _tep(r.nlm), stderr=_dung(err, "bootstrap", "ds"), token_env=os.environ.get("TL_TOKEN") == _TOK,
         config_khong_nlm=cfg.get("nlm_auth") == {"auth.json": "CU-wp433"} and cfg.get("token") == _TOK, ma=rc == 1 and _ac(out))
def w3_load_rel_thoat(r):
    ok, msg, _o, _e = r.w3("-", _LA)
    r.xs(khong_thoat=_thoat(r), khong_jar=not _tep(r.nlm), ma=ok is False, ly_do=_ly(msg, "ds"))
def _w2_chan(r, luot="-", req=False):
    return r.lk_goc(), r.w2(luot, {"nlm_auth": _BA}, req=req)
def w2_jar_hop_le_dich_bi_chan(r):
    t, (rc, _o, err) = _w2_chan(r)
    r.xs(khong_ra_ngoai=not os.listdir(t), ma=rc == 1, stderr=_dung(err, "bootstrap", "lk"), config_ghi=os.path.isfile(r.cfg))
def w3_jar_hop_le_dich_bi_chan(r):
    t = r.lk_goc(); ok, msg, _o, _e = r.w3("-", _BA)  # noqa: E702
    r.xs(khong_ra_ngoai=not os.listdir(t), ma=ok is False and _ly(msg, "lk"))
def chung_khoa_la_mot_thanh_phan(r):
    rc, _o, err = r.w1("N1k-W1", _KHAC)
    r.xs("N1k-W1", khong_khoa_la=not _tep(r.nlm) and rc == 1 and _dung(err, "nlm-auth-pull", "ds"))
    r.home(); rc, _o, err = r.w2("N1k-W2", {"nlm_auth": _KHAC})  # noqa: E702
    r.xs("N1k-W2", khong_khoa_la=not _tep(r.nlm) and rc == 1 and _dung(err, "bootstrap", "ds"))
    r.home(); ok, msg, _o, _e = r.w3("N1k-W3", _KHAC)  # noqa: E702
    r.xs("N1k-W3", khong_khoa_la=not _tep(r.nlm) and ok is False and _ly(msg, "ds"))
def chung_allowlist(r):
    for i, k in enumerate(("profiles/default/khac.json", "./auth.json", "profiles\\default\\cookies.json", "/tmp/x.json")):
        r.home(); rc, _o, _e = r.w1("N2.%d" % i, {k: "x"})  # noqa: E702
        r.xs("N2.%d" % i, **{"tu_choi_%d" % i: rc == 1 and not _tep(r.nlm)})
    r.home(); rc, _o, err = r.w1("N2.du", _BA)  # noqa: E702
    du = lambda p, v: os.path.isfile(p) and _doc(p) == v.encode("utf-8") and (os.name != "posix" or stat.S_IMODE(os.stat(p).st_mode) == 0o600)
    r.xs("N2.du", du_ba=rc == 0 and not err and len(_tep(r.nlm)) == 3 and all(du(os.path.join(r.nlm, *k.split("/")), v) for k, v in _BA.items()))
def chung_du_lieu_sai_dang(r):
    rc, _o, err = r.w1("N3.1-W1", [1])
    r.xs("N3.1-W1", kieu_jar=rc == 1 and _dung(err, "nlm-auth-pull", "dl") and not _tep(r.nlm))
    r.home(); rc, out, err = r.w2("N3.1-W2", {"nlm_auth": [1]})  # noqa: E702
    r.xs("N3.1-W2", kieu_jar=rc == 1 and _ac(out) and _dung(err, "bootstrap", "dl") and not _tep(r.nlm))
    r.home(); rc, _o, err = r.w1("N3.2", {"auth.json": 5})  # noqa: E702
    r.xs("N3.2", kieu_gia_tri=rc == 1 and _dung(err, "nlm-auth-pull", "dl") and not _tep(r.nlm))
    r.home(); rc, _o, err = r.w1("N3.3", b'{"nlm_auth": {"auth.json": "\\ud800"}}')  # noqa: E702 — surrogate đơn qua chuỗi thoát JSON
    r.xs("N3.3", surrogate_jar=rc == 1 and _dung(err, "nlm-auth-pull", "dl") and not _tep(r.nlm))
def chung_kiem_truoc_ghi(r):
    k = r.kho(); r.home(k); truoc = _anh(k)  # noqa: E702
    rc, _o, _e = r.w1("-", _BA)
    r.xs(ma=rc == 1, khong_tao_thu_muc=not os.path.lexists(r.nlm), sach=_anh(k) == truoc and not truoc[1])
    r.home(); rc, _o, _e = r.w1("duong", _BA)  # noqa: E702
    r.xs("duong", duong=rc == 0 and len(_tep(r.nlm)) == 3)
def w1_la_symlink(r):
    dich, la = r.p("dich.json"), os.path.join(r.nlm, "profiles", "default", "cookies.json")
    _ghi(dich, "CU"); os.makedirs(os.path.dirname(la)); os.symlink(dich, la)  # noqa: E702
    rc, _o, err = r.w1("-", _BA)
    r.xs(la_tu_choi=rc == 1 and _dung(err, "nlm-auth-pull", "lk") and os.path.islink(la) and _doc(dich) == b"CU" and len(_tep(r.nlm)) == 1)
def w6_symlink_config(r):
    dich, mo = os.path.join(r.kho(), "dich.json"), [r.cfg]
    _ghi(dich, '{"cu": 1}'); os.symlink(dich, r.cfg)  # noqa: E702
    rc, _o, err = r.w2("-", {}, theo=mo)
    r.xs(ma=rc == 1, dich_giu=_doc(dich) == b'{"cu": 1}' and os.path.islink(r.cfg), stderr=_dung(err, "bootstrap", "lk"), khong_doc_merge=len(mo) == 1)
def chung_symlink_thu_muc(r):
    t = r.p("T"); os.makedirs(t); os.makedirs(os.path.join(r.nlm, "profiles")); os.symlink(t, os.path.join(r.nlm, "profiles", "default"), target_is_directory=True)  # noqa: E702
    rc, _o, _e = r.w1("-", _BA)
    r.xs(ma=rc == 1, khong_ra_ngoai=not os.listdir(t), khong_jar=not os.path.lexists(os.path.join(r.nlm, "auth.json")))
def chung_hardlink(r):
    h = r.p("H"); _ghi(h, "CU"); os.makedirs(r.nlm); os.link(h, os.path.join(r.nlm, "auth.json"))  # noqa: E702
    rc, _o, _e = r.w1("-", _BA)
    r.xs(ma=rc == 0, ban_kia_giu=_doc(h) == b"CU")
def _w6(r, trong_kho, them):
    k = r.kho(); r.home(k if trong_kho else None); truoc = _anh(k)  # noqa: E702
    rc, out, err = r.w2("-", them)
    return rc, out, err, _anh(k) == truoc and not truoc[1]
def w6_chi_config_trong_kho(r):
    rc, out, err, sach = _w6(r, True, {})
    r.xs(ma=rc == 1, sach=sach, token_env=os.environ.get("TL_TOKEN") == _TOK, stdout=_ac(out), stderr=_dung(err, "bootstrap", "kho"))
def w6_chi_config_ngoai_kho(r):
    rc, _o, err, _s = _w6(r, False, {})
    r.xs(duong=rc == 0 and json.loads(_doc(r.cfg)).get("token") == _TOK and not err and r.m.dem.get("_ensure_nlm_installed", 0) == 0)
def w6_tich_hop(r):
    rc, _o, err, sach = _w6(r, True, {"nlm_auth": _BA})
    r.xs(ma=rc == 1, sach=sach, stderr=_dung(err, "bootstrap", "kho", "kho"))
def chung_hop_dong_loi(r):
    for w, the in (("W1", "nlm-auth-pull"), ("W2", "bootstrap")):          # N8(1): ba lý do × W1, W2
        for ly, cum in (("kho", "kho"), ("lien_ket", "lk"), ("danh_sach", "ds")):
            luot = "N8.1-%s-%s" % (w, ly)
            if ly == "lien_ket" and not r.lk:
                continue
            r.home(r.kho("K-" + luot) if ly == "kho" else None)
            jar = (_KHAC if ly == "danh_sach" else _BA, r.lk_goc() if ly == "lien_ket" else None)[0]
            rc, out, err = r.w1(luot, jar) if w == "W1" else r.w2(luot, {"nlm_auth": jar})
            so = 2 if (w, ly) == ("W2", "kho") else 1          # HOME trong kho: W6 và W2 mỗi chỗ một dòng
            r.xs(luot, stderr=_dung(err, the, *[cum] * so), khong_nem=rc == 1, agent_creds=w == "W1" or _ac(out))
    if r.lk:                                                    # N8(2): fixture của w2_jar_hop_le_dich_bi_chan + --require-agent-creds
        r.home(); _t, (rc, out, err) = _w2_chan(r, "N8.2", req=True)  # noqa: E702
        r.xs("N8.2", require=rc == 4 and _ac(out) and len(err) == 2 and _dung(err[:1], "bootstrap", "lk")
             and err[1].startswith("[bootstrap] ✗ --require-agent-creds"))
    posix = os.name == "posix"                                  # N8(2b): `\n` trong đường KHO được in; Windows giả giá trị trả về
    k = r.kho("k\nho" if posix else "kho2b"); r.home(k); in_ra, that = (k if posix else k + "\nx"), r.m._trong_kho_git  # noqa: E702
    if not posix:
        r.m._trong_kho_git = lambda p: in_ra if os.path.abspath(p).startswith(k) else that(p)
    rc, _o, err = r.w1("N8.2b", _BA)
    r.m._trong_kho_git = that
    r.xs("N8.2b", mot_dong=rc == 1 and err == ["[nlm-auth-pull] ✗ nằm trong kho git: " + repr(in_ra)])
    r.home(); rc, _o, err = r.w1("N8.2b-khoa", {"x là liên kết tượng trưng": "x"})  # noqa: E702
    r.xs("N8.2b-khoa", cum_trong_khoa=rc == 1 and _dung(err, "nlm-auth-pull", "ds"))
    r.home(); cu_ha_cap, r.m._nlm_auth_load_downgrade = r.m._nlm_auth_load_downgrade, lambda *a: (True, "wp433-cu-hon")  # noqa: E702
    ok, msg, _o, _e = r.w3("N8.3", _KHAC)
    r.m._nlm_auth_load_downgrade = cu_ha_cap
    r.xs("N8.3", thu_tu_w3=ok is False and _ly(msg, "ds") and "HẠ CẤP" not in msg)
    r.home(); rc, _o, err = r.w1("N8.4-W1", _BA, thay=lambda d: d.endswith("cookies.json"))  # noqa: E702
    r.xs("N8.4-W1", oserror_w1=rc == 1 and _dung(err, "nlm-auth-pull", "ghi") and _tep(r.nlm) == ["auth.json"])
    r.home(); nlm = r.nlm; rc, out, err = r.w2("N8.4-W2", {"nlm_auth": _BA}, thay=lambda d: os.path.normcase(os.path.normpath(d)).startswith(os.path.normcase(os.path.normpath(nlm)) + os.sep))  # noqa: E702
    r.xs("N8.4-W2", oserror_w2=rc == 1 and _dung(err, "bootstrap", "ghi") and _ac(out) and os.path.isfile(r.cfg))
    r.home(); cfg = r.cfg; _ghi(cfg, '{"cu": 1}'); rc, out, err = r.w2("N8.4-W6", {}, thay=lambda d: os.path.normcase(os.path.normpath(d)) == os.path.normcase(os.path.normpath(cfg)))  # noqa: E702
    r.xs("N8.4-W6", oserror_w6=rc == 1 and _dung(err, "bootstrap", "ghi") and "ghi config lỗi" not in out and os.environ.get("TL_TOKEN") == _TOK
         and _doc(cfg) == b'{"cu": 1}' and os.listdir(os.path.dirname(cfg)) == [os.path.basename(cfg)])
def d5_khong_claude(r):
    os.environ["TL_AGENT_CREDS_FILEID"] = "AC433"
    r.m.drive["AC433"] = r._ma({"schema": 1, "rev": 1, "codex_auth": {"tokens": {"t": _SENT}}, "claude_oauth_token": _SENT, "antigravity_api_key": _SENT})
    (_rc, out, _e), h = r.w2("-", {}, env="chat"), os.environ["HOME"]
    r.xs(codex_da_nap="agent_creds: ĐÃ NẠP" in out and os.path.isfile(r.p("cx", "auth.json")), khong_claude=not os.path.lexists(os.path.join(h, ".claude")),
         khong_export=not os.path.lexists(os.path.join(h, ".gemini")) and not {"CLAUDE_CODE_OAUTH_TOKEN", "GEMINI_API_KEY"} & set(os.environ))
_CA = (w1_pull_rel_thoat, w2_bootstrap_rel_thoat, w3_load_rel_thoat, w2_jar_hop_le_dich_bi_chan, w3_jar_hop_le_dich_bi_chan,
       chung_khoa_la_mot_thanh_phan, chung_allowlist, chung_du_lieu_sai_dang, chung_kiem_truoc_ghi, w1_la_symlink, w6_symlink_config,
       chung_symlink_thu_muc, chung_hardlink, w6_chi_config_trong_kho, w6_chi_config_ngoai_kho, w6_tich_hop, chung_hop_dong_loi, d5_khong_claude)
_LK = {"w2_jar_hop_le_dich_bi_chan", "w3_jar_hop_le_dich_bi_chan", "w1_la_symlink", "w6_symlink_config", "chung_symlink_thu_muc", "chung_hardlink"}
_W1 = "ly_do = _kiem_jar_nlm(nlm) or _dich_jar_nlm(nbase, nlm) or _ghi_jar_nlm(nbase, nlm)"
_W3, _W6 = "ly_do = _kiem_jar_nlm(nlm) or _dich_jar_nlm(nbase, nlm)\n", "ly_cfg = _kiem_dich_ghi(cfgp, cfgp, ())"
_VONG, _TRA_W3 = "for i in range(len(thanh_phan) + 1):", "    if ly_do:\n        return False, ly_do\n"
_GHI_W3, _ENC = "    try:\n        _ghi_jar_nlm(nbase, nlm)\n", [('            noi_dung.encode("utf-8")\n        except ValueError:', "            pass\n        except ValueError:")]
_GHI_CU = ('\ndef _wp433_ghi_cu(nbase, nlm):\n    for rel, c in nlm.items():\n        d = os.path.join(nbase, *rel.split("/")); os.makedirs(os.path.dirname(d), exist_ok=True)\n'
           '        with open(d, "w", encoding="utf-8") as f:\n            f.write(c)\n        os.chmod(d, 0o600)\n')
_DB = (  # §4b: (đột biến, [(neo khớp ĐÚNG MỘT lần, thay)…], ca đích, lượt, nhãn)
    ("db_w1_bo_kiem_jar", [(_W1, "ly_do = _dich_jar_nlm(nbase, nlm) or _ghi_jar_nlm(nbase, nlm)")], "chung_khoa_la_mot_thanh_phan", "N1k-W1", "khong_khoa_la"),
    ("db_w3_bo_kiem_jar", [(_W3, "ly_do = _dich_jar_nlm(nbase, nlm)\n")], "chung_khoa_la_mot_thanh_phan", "N1k-W3", "khong_khoa_la"),
    ("db_w2_bo_kiem_jar", [("ly_jar = _kiem_jar_nlm(jar) if jar else None", "ly_jar = None")], "chung_khoa_la_mot_thanh_phan", "N1k-W2", "khong_khoa_la"),
    ("db_w2_bo_kiem_dich", [("ly_nlm = _dich_jar_nlm(nbase, jar) or _ghi_jar_nlm(nbase, jar)", "ly_nlm = _ghi_jar_nlm(nbase, jar)")], "w2_jar_hop_le_dich_bi_chan", "-", "khong_ra_ngoai"),
    ("db_w1_bo_kiem_dich", [(_W1, "ly_do = _kiem_jar_nlm(nlm) or _ghi_jar_nlm(nbase, nlm)")], "chung_symlink_thu_muc", "-", "khong_ra_ngoai"),
    ("db_w3_bo_kiem_dich", [(_W3, "ly_do = _kiem_jar_nlm(nlm)\n")], "w3_jar_hop_le_dich_bi_chan", "-", "khong_ra_ngoai"),
    ("db_w6_luu_nlm_bi_tu_choi", [(' and not (k == "nlm_auth" and ly_jar)', "")], "w2_bootstrap_rel_thoat", "-", "config_khong_nlm"),
    ("db_blocklist", [("rel not in _NLM_AUTH_RELS", '".." in rel')], "chung_allowlist", "N2.0", "tu_choi_0"),
    ("db_chuan_hoa_truoc", [("rel not in _NLM_AUTH_RELS", "os.path.normpath(rel) not in _NLM_AUTH_RELS")], "chung_allowlist", "N2.1", "tu_choi_1"),
    ("db_bo_kiem_kieu_jar", [('    if not isinstance(nlm, dict) or not nlm:\n        return "dữ liệu', '    if not nlm:\n        return "dữ liệu')], "chung_du_lieu_sai_dang", "N3.1-W1", "kieu_jar"),
    ("db_bo_kiem_encode", _ENC, "chung_du_lieu_sai_dang", "N3.3", "surrogate_jar"),
    ("db_makedirs_truoc", [('        tp = tuple(rel.split("/"))\n', '        tp = tuple(rel.split("/"))\n        os.makedirs(os.path.dirname(os.path.join(nbase, *tp)), exist_ok=True)\n')], "chung_kiem_truoc_ghi", "-", "khong_tao_thu_muc"),
    ("db_bo_kho", [("(kho_dich := _trong_kho_git(os.path.dirname(dich)))", "(kho_dich := None)")], "chung_kiem_truoc_ghi", "-", "sach"),
    ("db_w6_bo_symlink", [(_W6, 'ly_cfg = (lambda kk: None if kk is None else f"nằm trong kho git: {repr(kk)[:200]}")(_trong_kho_git(os.path.dirname(cfgp)))')], "w6_symlink_config", "-", "stderr"),
    ("db_w6_doc_truoc_chot", [(_W6, 'existing = json.load(open(cfgp, encoding="utf-8")) if os.path.exists(cfgp) else {}; ' + _W6)], "w6_symlink_config", "-", "khong_doc_merge"),
    ("db_bo_tien_to_cuoi", [(_VONG, "for i in range(len(thanh_phan)):")], "w1_la_symlink", "-", "la_tu_choi"),
    ("db_bo_symlink_thanh_phan", [(_VONG, "for i in range(len(thanh_phan), len(thanh_phan) + 1):")], "chung_symlink_thu_muc", "-", "khong_ra_ngoai"),
    ("db_w1_khong_nguyen_tu", [(_W1, _W1.replace("_ghi_jar_nlm", "_wp433_ghi_cu")), ("\ndef _ghi_jar_nlm(", _GHI_CU + "\ndef _ghi_jar_nlm(")], "chung_hardlink", "-", "ban_kia_giu"),
    ("db_w6_bo_chot", [(_W6, "ly_cfg = None")], "w6_chi_config_trong_kho", "-", "sach"),
    ("db_quen_degraded", [('print(f"[bootstrap] ✗ {ly_cfg}", file=sys.stderr); degraded = True', 'print(f"[bootstrap] ✗ {ly_cfg}", file=sys.stderr)')], "w6_chi_config_trong_kho", "-", "ma"),
    ("db_degraded_khoi_tao_muon", [("    # 2) gws (Code/Cowork): binary nếu thiếu + cred từ bundle\n", "    degraded = False\n")], "w6_chi_config_trong_kho", "-", "ma"),
    ("db_nem_thay_vi_tu_choi", [('return f"nằm trong kho git: {repr(kho_dich)[:200]}"', 'raise ValueError("wp433-nem")')], "chung_hop_dong_loi", "N8.1-W1-kho", "khong_nem"),
    ("db_in_hai_dong", [('print(f"[nlm-auth-pull] ✗ {ly_do}", file=sys.stderr)', 'print(f"[nlm-auth-pull] ✗ {ly_do}\\n[nlm-auth-pull] xem thêm", file=sys.stderr)')], "chung_hop_dong_loi", "N8.1-W1-kho", "stderr"),
    ("db_oserror_lan", [('    except OSError as e:\n        ly_do = f"ghi lỗi: {_safe_exc(e)}"\n    if ly_do:\n        print(', '    except ZeroDivisionError as e:\n        ly_do = f"ghi lỗi: {_safe_exc(e)}"\n    if ly_do:\n        print(')], "chung_hop_dong_loi", "N8.4-W1", "oserror_w1"),
    ("db_w6_oserror_kieu_cu", [('ly_cfg = f"ghi lỗi: {_safe_exc(e)}"', 'ly_cfg = print(f"[bootstrap] ✓ token nạp env (ghi config lỗi: {e})")')], "chung_hop_dong_loi", "N8.4-W6", "oserror_w6"),
    ("db_kiem_sau_ha_cap", [(_TRA_W3, ""), (_GHI_W3, _TRA_W3 + _GHI_W3)], "chung_hop_dong_loi", "N8.3", "thu_tu_w3"),
    ("db_khong_repr", [("{repr(kho_dich)[:200]}", "{kho_dich}")], "chung_hop_dong_loi", "N8.2b", "mot_dong"),
    ("db_cum_cuoi_dong", [('return f"ngoài danh sách cho phép: {repr(rel)[:80]}"', 'return f"{repr(rel)[:80]}: ngoài danh sách cho phép"')], "chung_hop_dong_loi", "N8.2b-khoa", "cum_trong_khoa"),
    ("db_require_thua_rc1", [('    if getattr(a, "require_agent_creds", False) and ac != "ĐÃ NẠP":', '    if degraded:\n        return 1\n    if getattr(a, "require_agent_creds", False) and ac != "ĐÃ NẠP":')], "chung_hop_dong_loi", "N8.2", "require"),
    ("db_tao_claude", [('    co = [k for k in ("claude_oauth_token", "antigravity_api_key") if p.get(k)]', '    os.makedirs(os.path.expanduser("~/.claude"), exist_ok=True)\n    co = [k for k in ("claude_oauth_token", "antigravity_api_key") if p.get(k)]')], "d5_khong_claude", "-", "khong_claude"),
)
_TU_KIEM = (  # N10(c)(d): bộ phân hạng phải KHÔNG cấp tín dụng — (tên, cặp, ca, lượt, nhãn, hạng mong đợi)
    ("tu_kiem_attributeerror", [("    try:   # WP433: kiểm jar + đích của mọi khoá TRƯỚC khi ghi\n", '    raise AttributeError("wp433-tu-kiem")\n    try:\n')], "w1_pull_rel_thoat", "-", "ma", "TIN_DUNG_GIA"),
    ("tu_kiem_chu_thich", [("\ndef _dich_jar_nlm(", "\n# vô hại\ndef _dich_jar_nlm(")], "w1_pull_rel_thoat", "-", "ma", "SONG_SOT"),
    ("tu_kiem_sai_luot", _ENC, "chung_du_lieu_sai_dang", "N3.1-W1", "surrogate_jar", "TIN_DUNG_GIA"),
    ("tu_kiem_neo_lap", [("_ghi_jar_nlm(nbase, nlm)", "None")], "w1_pull_rel_thoat", "-", "ma", "HONG"),
)
def _chay(m, store, ca, lk=True):
    with _Rig(m, ca.__name__, store, lk) as r:
        ca(r)
        if r.hong:
            raise TinHieuChotCa(r.ca, r.hong)
def _hang(nguon, tl_module, goc, store, cap, ca, luot, nhan):
    """Phân hạng MỘT đột biến trên bản sao trong bộ nhớ: HONG (neo ≠ 1 lần / không nạp được) · SONG_SOT · GIET (đúng lớp, đúng ca,
    đúng (lượt, nhãn)) · TIN_DUNG_GIA (chết vì lý do khác — kể cả ngoại lệ đã bị biên lượt đổi thành `ngoai_le_la`)."""
    for neo, thay in cap:
        if nguon.count(neo) != 1 or neo == thay:
            return "HONG"
        nguon = nguon.replace(neo, thay)
    try:
        m = _nap(nguon, tl_module, goc)
    except Exception:  # noqa: BLE001
        return "HONG"
    try:
        _chay(m, store, next(c for c in _CA if c.__name__ == ca))
        return "SONG_SOT"
    except TinHieuChotCa as e:
        return "GIET" if e.ca == ca and (luot, nhan) in e.nhan else "TIN_DUNG_GIA"
    except Exception:  # noqa: BLE001
        return "TIN_DUNG_GIA"
def _co_lien_ket():
    with tempfile.TemporaryDirectory() as d:
        try:
            _ghi(os.path.join(d, "a"), "x"); os.symlink(os.path.join(d, "a"), os.path.join(d, "b")); os.link(os.path.join(d, "a"), os.path.join(d, "c"))  # noqa: E702
            return True
        except (OSError, NotImplementedError, AttributeError):
            return False
def _run(tl_module):
    goc = tl_module._imp("tl_gws"); goc.bind(tl_module)  # noqa: E702
    nguon, store, lk = pathlib.Path(goc.__file__).read_text(encoding="utf-8"), tl_module._imp("gws_cred_store"), _co_lien_ket()
    m, dat, bo = _nap(nguon, tl_module, goc), 0, 0
    for ca in _CA:
        if ca.__name__ in _LK and not lk:
            bo += 1
            continue
        try:
            _chay(m, store, ca, lk); dat += 1  # noqa: E702
        except Exception as e:  # noqa: BLE001
            print("[%s] ĐỎ %s: %r (%r)" % (TEST_ID, ca.__name__, e, e.__cause__), file=sys.stderr)
    kq = {d[0]: _hang(nguon, tl_module, goc, store, *d[1:]) for d in _DB if lk or (d[2] not in _LK and d[0] != "db_require_thua_rc1")}
    tk = [(d[0], _hang(nguon, tl_module, goc, store, *d[1:5]), d[5]) for d in _TU_KIEM]
    for ten, hang in list(kq.items()) + [(t, "tự kiểm %s ≠ %s" % (h, mong)) for t, h, mong in tk if h != mong]:
        if hang != "GIET":
            print("[%s] ĐỘT BIẾN %s: %s" % (TEST_ID, ten, hang), file=sys.stderr)
    giet, hong, chay = sum(h == "GIET" for h in kq.values()), sum(h == "HONG" for h in kq.values()), len(_CA) - bo
    print("[%s] CA: dự_kiến=%d chạy=%d đạt=%d bỏ_qua=%d · DOT BIEN: dự_kiến=%d chạy=%d giết_đúng=%d bỏ_qua=%d · HONG: %d"
          % (TEST_ID, len(_CA), chay, dat, bo, len(_DB), len(kq), giet, len(_DB) - len(kq), hong), file=sys.stderr)
    return chay == dat and len(kq) == giet and hong == 0 and all(h == mong for _t, h, mong in tk) and (lk or os.name != "posix")
def run(tl_module):
    ra = io.StringIO()                      # N10(e): fragment in mọi thứ ra STDERR (driver bundle đọc stdout làm JSON)
    with contextlib.redirect_stdout(ra):
        ok = _run(tl_module)
    return ok and not ra.getvalue()
