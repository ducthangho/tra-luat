# -*- coding: utf-8 -*-
"""wp433 P2b — dữ liệu ghi qua W6 của `cmd_bootstrap` (`token`/`webappUrl` vào env, `~/.tra_luat_config.json`) được kiểm TRƯỚC khi gán
env và trước khi ghi; không ngoại lệ nào thoát khỏi lệnh (spec GWS-CRED-DICH-NGOAI-KHO-B r1). Mọi ca chạy trên bản `tl_gws` nạp TRONG BỘ
NHỚ (nguồn thật hoặc đột biến), HOME tạm, dữ liệu GIẢ, không mạng. Mỗi LƯỢT thu đủ hậu điều rồi so nhãn theo thứ tự ghi; nhãn đỏ ĐẦU
TIÊN thành `TinHieuChotCa(ca, lượt, nhãn)` — đột biến chỉ GIẾT khi khớp cả ba (bảng `_DB` chép §4b của spec)."""
import argparse, builtins, contextlib, io, json, os, pathlib, shutil, subprocess, sys, tempfile, types, urllib.request  # noqa: E401
TEST_ID = "wp433_gws_cred_dich_ngoai_kho_b"
_MK, _TOK, _WEB, _SENT = "wp433b-master-gia", "wp433b-token-gia", "https://wp433b.invalid/exec", "SENTINEL-wp433b-gia"
_CU, _CU_MERGE, _TRUOC = b'{"token": "CU-wp433b"}', b'{"token": "CU-wp433b", "giu": "x"}', ("wp433b-truoc-tok", "wp433b-truoc-web")
_W6, _URL = "[bootstrap] ✗ dữ liệu không hợp lệ: ", "https://wp433b.invalid/\u00e9"
_D01 = "[bootstrap] ✗ --require-agent-creds: credential agent chưa nạp được (rc 4)."
_LJAR = _W6 + "nlm_auth phải là dict khác rỗng"
_LW1 = "[nlm-auth-pull] ⚠ bundle chưa có nlm_auth — ở Code chạy `tl secrets-set --nlm` trước."
_LUOT_DU_KIEN = {  # N3(b) SỔ LƯỢT — viết RIÊNG khỏi các hàm ca: 3 ca, 29 lượt, đúng thứ tự §4
    "w6_du_lieu": ("W6.hop_le", "W6.web_kieu", "W6.web_nul", "W6.web_dc80", "W6.token_kieu", "W6.token_nul", "W6.token_dc80", "W6.token_d800",
                   "W6.jar_va_token", "W6.require", "W6.require_da_nap", "W6.code", "W6.encode", "W6.encode_cu", "W6.nan", "W6.nan_cu",
                   "W6.dict_list", "W6.dict_null", "W6.dict_str", "W6.token_falsy", "W6.web_falsy"),
    "w6_locale": ("W6.web_locale", "W6.web_utf8"),
    "jar_rong_base": ("W1.rong", "W1.vang", "W3.rong", "W3.list_rong", "W3.list", "W2.rong"),
}
_NEM_ENV, _NEM_ENC = (TypeError, "str expected, not int", "nem_env"), (UnicodeEncodeError, "surrogates not allowed", "nem_encode")
_KHAI = {  # §4b "tập khai theo lượt": lượt → ((loại, dấu, nhãn)…); ngoài tập của lượt ⇒ `ngoai_le_la`
    "W6.web_kieu": (_NEM_ENV, (TypeError, "iterable", "nem_kiem")), "W6.web_nul": ((ValueError, "embedded null", "nem_env"),),
    "W6.token_kieu": (_NEM_ENV,), "W6.jar_va_token": (_NEM_ENV,), "W6.encode": (_NEM_ENC,), "W6.encode_cu": (_NEM_ENC,),
    "W6.dict_list": ((AttributeError, "object has no attribute 'update'", "nem_dict"),),
}
class TinHieuChotCa(AssertionError):
    def __init__(self, ca, luot, nhan):
        super().__init__("%s · %s · %s" % (ca, luot, nhan)); self.ca, self.luot, self.nhan = ca, luot, nhan  # noqa: E702
def _nem(e):
    raise e
def _nap(nguon, tl_module, goc):
    """`compile`+`exec` nguồn vào module MỚI rồi `bind`; thay đường tải/cài bằng đồ giả CÓ ĐẾM (`m.dem`), kho Drive giả `m.drive`."""
    m = types.ModuleType("wp433b_tl_gws"); m.__file__ = goc.__file__  # noqa: E702
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
_nc = lambda p: os.path.normcase(os.path.normpath(os.fspath(p)))   # WP433 nợ p2b-w6-windows: `expanduser("~/…")` giữ '/' trên nt
_env = lambda: (os.environ.get("TL_TOKEN"), os.environ.get("TL_WEBAPP"))
_ac = lambda out: sum(d.startswith("[bootstrap] agent_creds:") for d in out.splitlines()) == 1
_x = lambda err: [d for d in err if d.startswith("[bootstrap] ✗ ")]
_js = lambda o: json.dumps(o).encode("utf-8")      # ensure_ascii: surrogate/NUL đi thành chuỗi thoát JSON, `json.loads` dựng lại đúng giá trị
def _doc(p):
    try:
        return pathlib.Path(p).read_bytes()
    except OSError:
        return None
def _json(p):
    try:
        return json.loads(_doc(p))
    except (TypeError, ValueError):
        return None
class _Rig:
    """Một ca: thư mục tạm `realpath`, HOME/USERPROFILE/CODEX_HOME/GOOGLE_WORKSPACE_CLI_CONFIG_DIR/TL_*/cwd đặt tạm, khôi phục khi ra.
    `so` là SỔ LƯỢT dùng chung: mỗi lượt ghi đúng một trạng thái (`đạt` · `đỏ`)."""
    def __init__(self, m, ca, store, so):
        self.m, self.ca, self.store, self.so, self.dem = m, ca, store, so, {}
    def __enter__(self):
        self.td, self.cu_env, self.cu_cwd = os.path.realpath(tempfile.mkdtemp(prefix="wp433b-")), dict(os.environ), os.getcwd()
        for k in [k for k in os.environ if k.startswith("TL_")] + ["CLAUDE_CODE_OAUTH_TOKEN", "GEMINI_API_KEY"]:
            os.environ.pop(k, None)
        self.h, self.gws = os.path.join(self.td, "home"), os.path.join(self.td, "gws"); os.makedirs(self.h)  # noqa: E702
        self.cfg, self.nlm = os.path.join(self.h, ".tra_luat_config.json"), os.path.join(self.h, ".notebooklm-mcp-cli")
        os.environ.update(TL_MASTER_KEY=_MK, CODEX_HOME=os.path.join(self.td, "cx"), HOME=self.h, USERPROFILE=self.h, GOOGLE_WORKSPACE_CLI_CONFIG_DIR=self.gws)
        os.chdir(self.td); self.m.drive.clear()  # noqa: E702
        return self
    def __exit__(self, *a):
        os.chdir(self.cu_cwd); os.environ.clear(); os.environ.update(self.cu_env); shutil.rmtree(self.td, ignore_errors=True)  # noqa: E702
    def xs(self, luot, **nhan):
        """Kết thúc MỘT lượt: hậu điều đã thu đủ (đối số, theo thứ tự ghi); nhãn đỏ đầu tiên ⇒ `đỏ` + tín hiệu, không thì `đạt`."""
        hong = [n for n, dk in nhan.items() if not dk]
        self.so.append((self.ca, luot, "đỏ" if hong else "đạt"))
        if hong:
            raise TinHieuChotCa(self.ca, luot, hong[0])
    def goi(self, luot, fn, fsenc=None, agent=None):
        """Một LƯỢT GỌI. Cửa sổ: chặn tiến trình con/mạng (`MANG_BI_CHAN`), stdout/stderr RIÊNG; bộ quan sát `self.dem` đếm cho ĐƯỜNG CONFIG:
        lời gọi chốt đích (`chot`), lần mở ĐỌC qua `builtins.open` (`doc`), lời gọi writer (`ghi`). `fsenc` giả lập giá trị M1 đọc từ
        `sys.getfilesystemencoding`; `agent` thay `_bootstrap_agent_creds`. Ngoại lệ khớp tập khai CỦA LƯỢT ⇒ nhãn khai; ngoài tập ⇒ `ngoai_le_la`."""
        out, err, m, cfg, dem = io.StringIO(), io.StringIO(), self.m, _nc(self.cfg), {"chot": 0, "doc": 0, "ghi": 0}
        self.dem = dem
        cu = (subprocess.run, subprocess.Popen, urllib.request.urlopen, builtins.open, m._kiem_dich_ghi, m._ghi_nguyen_tu_0600, sys.getfilesystemencoding, m._bootstrap_agent_creds)
        subprocess.run = subprocess.Popen = urllib.request.urlopen = lambda *a, **k: _nem(RuntimeError("MANG_BI_CHAN"))
        def op(f, *a, **k):
            if isinstance(f, (str, os.PathLike)) and _nc(f) == cfg and not any(c in (a[0] if a else k.get("mode", "r")) for c in "wax+"):
                dem["doc"] += 1
            return cu[3](f, *a, **k)
        def kd(dich, goc, tp):
            dem["chot"] += _nc(dich) == cfg
            return cu[4](dich, goc, tp)
        def gh(path, data):
            dem["ghi"] += _nc(path) == cfg
            return cu[5](path, data)
        builtins.open, m._kiem_dich_ghi, m._ghi_nguyen_tu_0600 = op, kd, gh
        if fsenc:
            sys.getfilesystemencoding = lambda: fsenc
        if agent:
            m._bootstrap_agent_creds = lambda master: agent
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                kq = fn()
        except Exception as e:  # noqa: BLE001 — biên của lượt: chỉ tập ĐÓNG đã khai mới thành nhãn đích
            nhan = [n for lo, dau, n in _KHAI.get(luot, ()) if isinstance(e, lo) and dau in str(e)]
            self.so.append((self.ca, luot, "đỏ"))
            raise TinHieuChotCa(self.ca, luot, nhan[0] if nhan else "ngoai_le_la") from e
        finally:
            subprocess.run, subprocess.Popen, urllib.request.urlopen, builtins.open, m._kiem_dich_ghi, m._ghi_nguyen_tu_0600, sys.getfilesystemencoding, m._bootstrap_agent_creds = cu
        return kq, out.getvalue(), [d for d in err.getvalue().splitlines() if d]
    def boot(self, luot, bundle, cu=_CU, env="chat", req=False, **kw):
        """Fixture W6: `cmd_bootstrap --env <env> --no-nlm --no-gws`, config cũ `cu`, cặp env "trước" đặt ngay trước lời gọi. `bundle` là
        dict (tuần tự hoá ASCII) hoặc byte JSON thô."""
        os.environ["TL_TOKEN"], os.environ["TL_WEBAPP"] = _TRUOC
        pathlib.Path(self.cfg).write_bytes(cu)
        self.m.drive["S433"] = self.store.encrypt(bundle if isinstance(bundle, bytes) else _js(bundle), _MK)
        ns = argparse.Namespace(secrets_id="S433", secrets_file=None, env=env, config=None, profile=None, no_gws=True, no_nlm=True, bindir=None, require_agent_creds=req)
        return self.goi(luot, lambda: self.m.cmd_bootstrap(ns), **kw)
def w6_du_lieu(r):
    def tu_choi(luot, bundle, truong, cu=_CU, m2=True):
        """Bộ nhãn TỪ CHỐI của §4: M2 (không gán env, không chạm config) hoặc M3(c) (env đã gán GIỮ, config giữ byte)."""
        kq, out, err = r.boot(luot, bundle, cu=cu)
        ra, tam = out + "\n".join(err), [t for t in os.listdir(r.h) if t.startswith(".auth.json.")]
        nhan = dict(env=_env() == _TRUOC) if m2 else dict(env_token=_env()[0] == _TOK, env_web=_env()[1] == _WEB)
        nhan.update(cfg=_doc(r.cfg) == cu and not tam)
        if m2:
            nhan.update(khong_chot=r.dem["chot"] == 0)
        nhan.update(khong_ghi=r.dem["ghi"] == 0)
        if m2:
            nhan.update(khong_doc=r.dem["doc"] == 0)
        r.xs(luot, **nhan, khong_lo=_SENT not in ra and _TOK not in ra, dong_loi=_x(err) == [_W6 + truong], agent=_ac(out), ma=kq == 1 and "✓ config" not in out)
    kq, out, err = r.boot("W6.hop_le", {"token": _TOK, "webappUrl": _WEB, "rootFolderId": "r"}, cu=_CU_MERGE)
    r.xs("W6.hop_le", duong=kq == 0 and not err and _env() == (_TOK, _WEB) and "✓ config" in out and _ac(out),
         merge=_json(r.cfg) == {"token": _TOK, "giu": "x", "webappUrl": _WEB, "rootFolderId": "r"})
    for luot, v in (("W6.web_kieu", 7), ("W6.web_nul", _SENT + "\x00"), ("W6.web_dc80", _SENT + "\udc80")):
        tu_choi(luot, {"token": _TOK, "webappUrl": v}, "webappUrl")
    for luot, v in (("W6.token_kieu", 5), ("W6.token_nul", _SENT + "\x00"), ("W6.token_dc80", _SENT + "\udc80"), ("W6.token_d800", _SENT + "\ud800")):
        tu_choi(luot, {"token": v, "webappUrl": _WEB}, "token")
    kq, out, err = r.boot("W6.jar_va_token", {"token": 5, "nlm_auth": [1]})
    r.xs("W6.jar_va_token", hai_dong=kq == 1 and _x(err) == [_LJAR, _W6 + "token"] and _env() == _TRUOC and _ac(out))
    kq, out, err = r.boot("W6.require", {"token": _TOK, "webappUrl": 7}, req=True)
    r.xs("W6.require", require=kq == 4 and _x(err) == [_W6 + "webappUrl", _D01] and _ac(out))
    kq, out, err = r.boot("W6.require_da_nap", {"token": _TOK, "webappUrl": 7}, req=True, agent=("ĐÃ NẠP", "gia"))
    r.xs("W6.require_da_nap", require=kq == 1 and _x(err) == [_W6 + "webappUrl"] and _ac(out))
    kq, out, err = r.boot("W6.code", {"token": _TOK, "webappUrl": 7, "gws_cred": '{"gia": 1}'}, env="code")
    r.xs("W6.code", tiep_tuc=kq == 1 and _x(err) == [_W6 + "webappUrl"] and _doc(os.path.join(r.gws, "credentials.json")) == b'{"gia": 1}'
         and "[bootstrap] ✓ gws cred → " in out and _ac(out) and _env() == _TRUOC)
    hai = {"token": _TOK, "webappUrl": _WEB}
    tu_choi("W6.encode", dict(hai, rootFolderId=_SENT + "\ud800"), "config", m2=False)
    tu_choi("W6.encode_cu", hai, "config", cu=_js({"x": _SENT + "\ud800"}), m2=False)
    tu_choi("W6.nan", _js(hai)[:-1] + b', "extra": 1e999}', "config", m2=False)
    tu_choi("W6.nan_cu", hai, "config", cu=b'{"x": NaN}', m2=False)
    for luot, cu in (("W6.dict_list", b"[]"), ("W6.dict_null", b"null"), ("W6.dict_str", b'"s"')):
        kq, out, err = r.boot(luot, {"token": _TOK}, cu=cu)
        r.xs(luot, duong_dict=kq == 0 and not err and _json(r.cfg) == {"token": _TOK} and "✓ config" in out)
    kq, out, err = r.boot("W6.token_falsy", {"token": 0})
    r.xs("W6.token_falsy", thieu=kq == 0 and err == ["[bootstrap] ⚠ bundle thiếu GAS token."] and _env() == _TRUOC and _doc(r.cfg) == _CU)
    kq, out, err = r.boot("W6.web_falsy", {"token": _TOK, "webappUrl": 0})
    r.xs("W6.web_falsy", web_falsy=kq == 0 and not err and _env() == (_TOK, _TRUOC[1]) and _json(r.cfg) == {"token": _TOK, "webappUrl": 0})
def w6_locale(r):
    kq, out, err = r.boot("W6.web_locale", {"token": _TOK, "webappUrl": _URL}, fsenc="ascii")
    r.xs("W6.web_locale", env=_env() == _TRUOC, dong_loi=_x(err) == [_W6 + "webappUrl"] and kq == 1 and _ac(out))
    if sys.getfilesystemencoding().lower().replace("-", "").replace("_", "") != "utf8":   # `tien_de` chấm TRƯỚC giả lập và lời gọi (P3 review đặc tả lượt 3)
        r.xs("W6.web_utf8", tien_de=False)
    kq, out, err = r.boot("W6.web_utf8", {"token": _TOK, "webappUrl": _URL}, fsenc="utf-8")
    r.xs("W6.web_utf8", tien_de=True, duong_utf8=kq == 0 and not err and _env() == (_TOK, _URL) and _json(r.cfg) == {"token": _TOK, "webappUrl": _URL})
def jar_rong_base(r):
    os.environ["TL_TOKEN"], m = _TOK, r.m
    for luot, b in (("W1.rong", {"nlm_auth": {}}), ("W1.vang", {})):
        m.drive["S433"] = r.store.encrypt(_js(b), _MK)
        ns = argparse.Namespace(secrets_id="S433", secrets_file=None, env="code", config=None, profile=None)
        kq, _o, err = r.goi(luot, lambda: m.cmd_nlm_auth_pull(ns))
        r.xs(luot, base_w1=kq == 1 and err == [_LW1] and not os.path.lexists(r.nlm))
    for luot, j in (("W3.rong", {}), ("W3.list_rong", []), ("W3.list", [["auth.json", "x"]])):
        m.drive["N433"] = r.store.encrypt(_js(j), _TOK)
        kq, _o, _e = r.goi(luot, lambda: m._nlm_auth_load(_TOK, "N433"))
        r.xs(luot, base_w3=kq == (False, "nlm_cred rỗng/sai định dạng.") and not os.path.lexists(r.nlm))
    kq, _o, err = r.boot("W2.rong", {"token": _TOK, "gws_cred": '{"gia": 1}', "nlm_auth": {}}, env="code")
    r.xs("W2.rong", base_w2=kq == 0 and not err and not os.path.lexists(r.nlm))
_CA = ((w6_du_lieu, "mọi"), (w6_locale, "posix"), (jar_rong_base, "mọi"))
_DU_KIEN = (  # N3(a): danh sách ID đột biến dự kiến (§4b, 36 mục) — viết RIÊNG khỏi `_DB`
    "db_w6_bo_kiem_web", "db_w6_bo_kiem_kieu", "db_w6_bo_kiem_nul", "db_w6_bo_kiem_encode", "db_w6_gan_token_truoc", "db_w6_bo_kiem_token",
    "db_w6_bo_bat_encode", "db_w6_kiem_bundle_thay_existing", "db_w6_encode_go_env", "db_w6_encode_ghi_rong", "db_w6_bo_kiem_dict", "db_w6_dict_thanh_loi",
    "db_w6_token_co_mat", "db_w6_web_co_mat", "db_w6_lo_gia_tri", "db_w6_tu_choi_hop_le", "db_w6_quen_degraded", "db_w6_ghi_khi_tu_choi",
    "db_w1_jar_rong_moi", "db_w3_dinh_dang_moi", "db_w2_jar_rong_moi", "db_w6_tu_choi_van_chot", "db_w6_tu_choi_van_doc", "db_w6_tu_choi_ghi_lai",
    "db_w6_encode_ghi_cu", "db_w6_khong_merge", "db_w6_cho_nan", "db_w6_bo_kiem_locale", "db_w6_dung_som", "db_w6_bo_nhanh_sau", "db_w6_require_thua_rc1",
    "db_w6_require_luon_4", "db_w6_dung_ly_jar", "db_w6_lap_dong", "db_w6_locale_ep_ascii", "db_w6_encode_go_web")
_DB_POSIX = {"db_w6_bo_kiem_nul", "db_w6_bo_kiem_encode"}   # §4b cột nền: `posix` dù ca đích là `mọi` (ngữ nghĩa `os.environ` POSIX)
_VONG, _KK, _GOI = 'if ten == "token" or v:', 'if not isinstance(v, str) or "\\x00" in v:', '    ly_env = _kiem_env_w6(bundle) if bundle.get("token") else None'
_IN = '        print(f"[bootstrap] ✗ {ly_env}", file=sys.stderr); degraded = True\n'
_DUMP, _EXC = 'du_cfg = json.dumps(existing, ensure_ascii=False, allow_nan=False).encode("utf-8")', 'du_cfg, ly_cfg = None, "dữ liệu không hợp lệ: config"'
_REQ, _CFGP = '    if getattr(a, "require_agent_creds", False) and ac != "ĐÃ NẠP":', 'os.path.expanduser("~/.tra_luat_config.json")'
_GHI, _FS, _CUOI = "_ghi_nguyen_tu_0600(cfgp, du_cfg)", 'v.encode(sys.getfilesystemencoding(), "surrogateescape")', "    return None\n\n\ndef _duong_dich_chuan("
_DICT = "                if not isinstance(existing, dict):   # WP433 P2b: config cũ không phải dict ⇒ như không parse được\n                    existing = {}\n"
_UPD, _D, _L, _B = "                existing.update({k: v for k, v in bundle.items()", "w6_du_lieu", "w6_locale", "jar_rong_base"
_M1 = '    for ten in ("token", "webappUrl"):\n'
_BO_TOKEN = [(_VONG, 'if ten != "token" and v:')]
_DB = (  # §4b: (đột biến, [(neo khớp ĐÚNG MỘT lần, thay)…], ca đích, lượt, nhãn)
    ("db_w6_bo_kiem_web", [(_VONG, 'if ten == "token":')], _D, "W6.web_kieu", "nem_env"),
    ("db_w6_bo_kiem_kieu", [(_KK, 'if "\\x00" in v:')], _D, "W6.web_kieu", "nem_kiem"),
    ("db_w6_bo_kiem_nul", [(_KK, "if not isinstance(v, str):")], _D, "W6.web_nul", "nem_env"),
    ("db_w6_bo_kiem_encode", [('                v.encode("utf-8")\n', "                pass\n")], _D, "W6.web_dc80", "env"),
    ("db_w6_gan_token_truoc", [(_GOI, '    bundle.get("token") and os.environ.__setitem__("TL_TOKEN", bundle["token"])\n' + _GOI)], _D, "W6.web_kieu", "env"),
    ("db_w6_bo_kiem_token", _BO_TOKEN, _D, "W6.token_kieu", "nem_env"),
    ("db_w6_bo_bat_encode", [("except ValueError:   # WP433 P2b: NaN", "except ZeroDivisionError:   # WP433 P2b: NaN")], _D, "W6.encode", "nem_encode"),
    ("db_w6_kiem_bundle_thay_existing", [(_DUMP, _DUMP.replace("existing", "bundle")), (_GHI, '_ghi_nguyen_tu_0600(cfgp, json.dumps(existing, ensure_ascii=False).encode("utf-8"))')],
     _D, "W6.encode_cu", "nem_encode"),
    ("db_w6_encode_go_env", [(_EXC, _EXC + '; os.environ.pop("TL_TOKEN", None)')], _D, "W6.encode", "env_token"),
    ("db_w6_encode_ghi_rong", [(_EXC, 'du_cfg = b"{}"')], _D, "W6.encode", "cfg"),
    ("db_w6_bo_kiem_dict", [("                if not isinstance(existing, dict):", "                if False:")], _D, "W6.dict_list", "nem_dict"),
    ("db_w6_dict_thanh_loi", [(_DICT, '                if not isinstance(existing, dict):\n                    ly_cfg = "dữ liệu không hợp lệ: config"\n')], _D, "W6.dict_list", "duong_dict"),
    ("db_w6_token_co_mat", [(_GOI, '    ly_env = _kiem_env_w6(bundle) if "token" in bundle else None')], _D, "W6.token_falsy", "thieu"),
    ("db_w6_web_co_mat", [(_VONG, 'if ten == "token" or ten in bundle:')], _D, "W6.web_falsy", "web_falsy"),
    ("db_w6_lo_gia_tri", [(_IN, _IN + '        print(f"[bootstrap] w6={repr(bundle.get(\'token\'))[:80]}{repr(bundle.get(\'webappUrl\'))[:80]}")\n')], _D, "W6.web_kieu", "khong_lo"),
    ("db_w6_tu_choi_hop_le", [(_CUOI, _CUOI.replace("None", '"dữ liệu không hợp lệ: token"'))], _D, "W6.hop_le", "duong"),
    ("db_w6_quen_degraded", [(_IN, _IN.replace("; degraded = True", ""))], _D, "W6.web_kieu", "ma"),
    ("db_w6_ghi_khi_tu_choi", [(_IN, _IN + '        _ghi_nguyen_tu_0600(%s, b"{}")\n' % _CFGP)], _D, "W6.web_kieu", "cfg"),
    ("db_w1_jar_rong_moi", [('    nlm = bundle.get("nlm_auth")\n    if not nlm:\n', '    nlm = bundle.get("nlm_auth")\n    if nlm is None:\n')], _B, "W1.rong", "base_w1"),
    ("db_w3_dinh_dang_moi", [('    if not isinstance(nlm, dict) or not nlm:\n        return False, "nlm_cred', '    if not nlm:\n        return False, "nlm_cred')], _B, "W3.list", "base_w3"),
    ("db_w2_jar_rong_moi", [("ly_jar = _kiem_jar_nlm(jar) if jar else None", "ly_jar = _kiem_jar_nlm(jar) if jar is not None else None")], _B, "W2.rong", "base_w2"),
    ("db_w6_tu_choi_van_chot", [(_IN, _IN + "        _kiem_dich_ghi(%s, %s, ())\n" % (_CFGP, _CFGP))], _D, "W6.web_kieu", "khong_chot"),
    ("db_w6_tu_choi_van_doc", [(_IN, _IN + '        open(%s, encoding="utf-8").read()\n' % _CFGP)], _D, "W6.web_kieu", "khong_doc"),
    ("db_w6_tu_choi_ghi_lai", [(_IN, _IN + '        _ghi_nguyen_tu_0600(%s, open(%s, "rb").read())\n' % (_CFGP, _CFGP))], _D, "W6.web_kieu", "khong_ghi"),
    ("db_w6_encode_ghi_cu", [(_EXC, _EXC + '; _ghi_nguyen_tu_0600(cfgp, open(cfgp, "rb").read())')], _D, "W6.encode", "khong_ghi"),
    ("db_w6_khong_merge", [(_UPD, _UPD.replace("existing.update", "existing = {}; existing.update"))], _D, "W6.hop_le", "merge"),
    ("db_w6_cho_nan", [(_DUMP, _DUMP.replace(", allow_nan=False", ""))], _D, "W6.nan", "cfg"),
    ("db_w6_bo_kiem_locale", [("                    %s\n" % _FS, "                    pass\n")], _L, "W6.web_locale", "env"),
    ("db_w6_dung_som", [(_IN, _IN + "        return 1\n")], _D, "W6.web_kieu", "agent"),
    ("db_w6_bo_nhanh_sau", [(_IN, _IN + '        env = "chat"\n')], _D, "W6.code", "tiep_tuc"),
    ("db_w6_require_thua_rc1", [(_REQ, "    if degraded:\n        return 1\n" + _REQ)], _D, "W6.require", "require"),
    ("db_w6_require_luon_4", [(_REQ, _REQ.replace(' and ac != "ĐÃ NẠP"', ""))], _D, "W6.require_da_nap", "require"),
    ("db_w6_dung_ly_jar", [(_GOI, _GOI.replace(' if bundle.get("token")', ' if bundle.get("token") and not ly_jar'))], _D, "W6.jar_va_token", "nem_env"),
    ("db_w6_lap_dong", [(_IN, '        print(f"[bootstrap] ✗ {ly_env}", file=sys.stderr); ' + _IN.lstrip())], _D, "W6.web_kieu", "dong_loi"),
    ("db_w6_locale_ep_ascii", [(_FS, _FS.replace("sys.getfilesystemencoding()", '"ascii" if sys.getfilesystemencoding() == "utf-8" else sys.getfilesystemencoding()', 1))],
     _L, "W6.web_utf8", "duong_utf8"),
    ("db_w6_encode_go_web", [(_EXC, _EXC + '; os.environ.pop("TL_WEBAPP", None)')], _D, "W6.encode", "env_web"),
)
_DOI_KIEU = ('    try:\n        raise AttributeError("wp433b-tu-kiem")\n    except Exception as e:\n'
             '        raise AssertionError(f"wp433b-tu-kiem {type(e).__name__}")\n')
_TU_KIEM = (  # N3(d): bộ phân hạng KHÔNG được cấp tín dụng — (tên, cặp, ca, lượt, nhãn, hạng mong đợi)
    ("tu_kiem_doi_kieu", [(_M1, _DOI_KIEU + _M1)], _D, "W6.hop_le", "duong", "TIN_DUNG_GIA"),
    ("tu_kiem_chu_thich", [("\ndef _kiem_env_w6(", "\n# vô hại\ndef _kiem_env_w6(")], _D, "W6.hop_le", "duong", "SONG_SOT"),
    ("tu_kiem_sai_luot", _BO_TOKEN, _D, "W6.web_kieu", "nem_env", "TIN_DUNG_GIA"),   # CHÍNH db_w6_bo_kiem_token, chỉ đổi lượt khai
)
def _chay(m, store, ca, so):
    with _Rig(m, ca.__name__, store, so) as r:
        ca(r)
def _hang(nguon, tl_module, goc, store, cap, ca, luot, nhan):
    """Phân hạng MỘT đột biến trên bản sao trong bộ nhớ, trả (hạng, ngoại lệ): HONG (neo ≠ 1 lần / không nạp được) · SONG_SOT · GIET
    (đúng lớp tín hiệu, đúng ca, đúng lượt, đúng nhãn) · TIN_DUNG_GIA (chết vì lý do khác)."""
    for neo, thay in cap:
        if nguon.count(neo) != 1 or neo == thay:
            return "HONG", None
        nguon = nguon.replace(neo, thay)
    try:
        m = _nap(nguon, tl_module, goc)
    except Exception as e:  # noqa: BLE001
        return "HONG", e
    try:
        _chay(m, store, next(c for c, _n in _CA if c.__name__ == ca), [])
    except TinHieuChotCa as e:
        return ("GIET" if (e.ca, e.luot, e.nhan) == (ca, luot, nhan) else "TIN_DUNG_GIA"), e
    except BaseException as e:  # noqa: BLE001 — kể cả StopIteration khi ca đích không còn trong bảng ca
        return "TIN_DUNG_GIA", e
    return "SONG_SOT", None
def _run(tl_module):
    goc = tl_module._imp("tl_gws"); goc.bind(tl_module)  # noqa: E702
    nguon, store, posix = pathlib.Path(goc.__file__).read_text(encoding="utf-8"), tl_module._imp("gws_cred_store"), os.name == "posix"
    m, so, b, c, nen = _nap(nguon, tl_module, goc), [], 0, 0, {ca.__name__: n for ca, n in _CA}
    for ca, n in _CA:
        if n == "posix" and not posix:
            so += [(ca.__name__, luot, "chỉ_posix") for luot in _LUOT_DU_KIEN.get(ca.__name__, ())]
            continue
        b += 1
        try:
            _chay(m, store, ca, so); c += 1  # noqa: E702
        except Exception as e:  # noqa: BLE001
            print("[%s] ĐỎ %s: %r (%r)" % (TEST_ID, ca.__name__, e, e.__cause__), file=sys.stderr)
    kq = {d[0]: "CHI_POSIX" if not posix and (nen.get(d[2]) == "posix" or d[0] in _DB_POSIX) else _hang(nguon, tl_module, goc, store, *d[1:])[0] for d in _DB}
    tk = [(d[0], d[5]) + _hang(nguon, tl_module, goc, store, *d[1:5]) for d in _TU_KIEM]
    doi = lambda e: isinstance(getattr(getattr(e, "__cause__", None), "__context__", None), AttributeError)   # đã đi qua `except` đổi kiểu
    k = sum(h == mong and (ten != "tu_kiem_doi_kieu" or doi(e)) for ten, mong, h, e in tk)
    for ten, hang in list(kq.items()) + [(ten, "tự kiểm %s ≠ %s" % (h, mong)) for ten, mong, h, _e in tk if h != mong]:
        if hang not in ("GIET", "CHI_POSIX"):
            print("[%s] ĐỘT BIẾN %s: %s" % (TEST_ID, ten, hang), file=sys.stderr)
    dem, hg = lambda tt: sum(x[2] == tt for x in so), lambda tt: sum(h == tt for h in kq.values())
    a, w, x, y, z, t = len(_LUOT_DU_KIEN), len(_CA) - b, sum(map(len, _LUOT_DU_KIEN.values())), dem("đạt") + dem("đỏ"), dem("đạt"), dem("chỉ_posix")
    e, g, v, i = len(_DB), hg("GIET"), hg("CHI_POSIX"), hg("HONG"); f = e - v  # noqa: E702
    print("[%s] CA: dự_kiến=%d chạy=%d đạt=%d chỉ_posix=%d · LUOT: dự_kiến=%d chạy=%d đạt=%d chỉ_posix=%d · DOT BIEN: dự_kiến=%d chạy=%d giết_đúng=%d "
          "chỉ_posix=%d · HONG: %d · TU_KIEM: %d/%d" % (TEST_ID, a, b, c, w, x, y, z, t, e, f, g, v, i, k, len(_TU_KIEM)), file=sys.stderr)
    ve = {"ca_dat": b == c, "luot_dat": y == z, "giet_dung": f == g, "hong": i == 0, "so_ca": a == 3 == b + w, "tu_kiem": k == len(_TU_KIEM) == 3,
          "so_luot": x == 29 == y + t and [s[:2] for s in so] == [(ca.__name__, luot) for ca, _n in _CA for luot in _LUOT_DU_KIEN.get(ca.__name__, ())],
          "trang_thai": all(s[2] in ("đạt", "đỏ", "chỉ_posix") for s in so),
          "so_dot_bien": e == len(_DU_KIEN) == len(set(_DU_KIEN)) == 36 and sorted(d[0] for d in _DB) == sorted(_DU_KIEN),
          "nen": w == t == v == 0 if posix else (w, t, v) == (1, 2, 4)}
    if not all(ve.values()):
        print("[%s] VẾ SAI: %s" % (TEST_ID, ", ".join(n for n, dk in ve.items() if not dk)), file=sys.stderr)
    return all(ve.values())
def run(tl_module):
    ra = io.StringIO()                      # N3(f): fragment in mọi thứ ra STDERR (driver bundle đọc stdout làm JSON)
    with contextlib.redirect_stdout(ra):
        ok = _run(tl_module)
    return ok and not ra.getvalue()
