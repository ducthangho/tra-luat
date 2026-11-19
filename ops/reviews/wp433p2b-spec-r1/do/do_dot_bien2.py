"""Bộ chạy TẠM bảng đột biến P2b r1 (bản 2) trên NGUỒN ỨNG VIÊN. Mỗi lượt thu đủ hậu điều rồi so nhãn theo thứ tự ghi; nhãn đỏ ĐẦU TIÊN
(hoặc ngoại lệ khai) là (ca, lượt, nhãn). Sổ lượt so theo DÃY. Dùng: python3 -I do_dot_bien2.py <scripts của cây> <tl_gws ứng viên> [--base]"""
import argparse, builtins, contextlib, io, json, os, shutil, subprocess, sys, tempfile, types, urllib.request
SC = os.path.realpath(sys.argv[1]); sys.path.insert(0, SC)
import tl  # noqa: E402
goc = tl._imp("tl_gws"); goc.bind(tl); store = tl._imp("gws_cred_store")
NGUON = open(sys.argv[2], encoding="utf-8").read()
MK, TOK, WEB, SENT = "wp433b-master-gia", "wp433b-token-gia", "https://wp433b.invalid/exec", "SENTINEL-wp433b"
CU, CU_MERGE = b'{"token": "CU-wp433b"}', b'{"token": "CU-wp433b", "giu": "x"}'
TRUOC = ("truoc-tok", "truoc-web")
D01 = "[bootstrap] ✗ --require-agent-creds: credential agent chưa nạp được (rc 4)."
LJAR = "[bootstrap] ✗ dữ liệu không hợp lệ: nlm_auth phải là dict khác rỗng"
class Do(Exception):
    def __init__(self, ca, luot, nhan): super().__init__(ca, luot, nhan); self.k = (ca, luot, nhan)
def nap(nguon):
    m = types.ModuleType("w6m"); m.__file__ = goc.__file__
    exec(compile(nguon, goc.__file__, "exec"), m.__dict__); m.bind(tl); m.drive = {}
    m._secrets_fetch = lambda a, fid: (m.drive.get(fid), "gia"); m.load_creds = lambda *a, **k: None
    m._public_curl_bytes = lambda fid, timeout=120.0: m.drive.get(fid)
    m._gas = lambda: (_ for _ in ()).throw(RuntimeError("MANG_BI_CHAN")); m.AGENT_CREDS_FILEID = ""
    m._ensure_nlm_installed = lambda: (True, "gia"); m.cmd_gws_bootstrap_cowork = lambda ns: 0
    that = m._imp; m._imp = lambda n: types.SimpleNamespace(gws_exe=lambda: "gws-gia") if n == "gws_bridge" else that(n)
    return m
class Rig:
    def __init__(self, m, ca, so): self.m, self.ca, self.so = m, ca, so
    def __enter__(self):
        self.td, self.ce, self.cc = os.path.realpath(tempfile.mkdtemp(prefix="w6b-")), dict(os.environ), os.getcwd()
        for k in [k for k in os.environ if k.startswith("TL_")]: os.environ.pop(k)
        self.h = os.path.join(self.td, "home"); os.makedirs(self.h); self.cfg = os.path.join(self.h, ".tra_luat_config.json")
        self.gws = os.path.join(self.td, "gws")
        os.environ.update(TL_MASTER_KEY=MK, HOME=self.h, USERPROFILE=self.h, CODEX_HOME=os.path.join(self.td, "cx"), GOOGLE_WORKSPACE_CLI_CONFIG_DIR=self.gws)
        os.chdir(self.td); return self
    def __exit__(self, *a):
        os.chdir(self.cc); os.environ.clear(); os.environ.update(self.ce); shutil.rmtree(self.td, ignore_errors=True)
    def goi(self, luot, fn, khai, fsenc=None, agent=None):
        out, err, m, cfg = io.StringIO(), io.StringIO(), self.m, self.cfg
        self.dem = {"chot": 0, "doc": 0, "ghi": 0}
        cu = (subprocess.run, subprocess.Popen, urllib.request.urlopen, builtins.open, m._kiem_dich_ghi, m._ghi_nguyen_tu_0600, sys.getfilesystemencoding, m._bootstrap_agent_creds)
        subprocess.run = subprocess.Popen = urllib.request.urlopen = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("MANG_BI_CHAN"))
        def op(f, *a, **k):
            if f == cfg and not (a and any(c in a[0] for c in "wax")) and not any(c in k.get("mode", "") for c in "wax"):
                self.dem["doc"] += 1
            return cu[3](f, *a, **k)
        def kd(d, g, t):
            self.dem["chot"] += d == cfg
            return cu[4](d, g, t)
        def gh(p, b):
            self.dem["ghi"] += p == cfg
            return cu[5](p, b)
        builtins.open, m._kiem_dich_ghi, m._ghi_nguyen_tu_0600 = op, kd, gh
        if fsenc:
            sys.getfilesystemencoding = lambda: fsenc
        if agent:
            m._bootstrap_agent_creds = lambda master: agent
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                kq = fn()
        except Exception as e:
            self.so.append((self.ca, luot))
            for lo, dau, nhan in khai.get(luot, ()):
                if isinstance(e, lo) and dau in str(e):
                    raise Do(self.ca, luot, nhan) from e
            raise Do(self.ca, luot, "ngoai_le_la:%s:%s" % (type(e).__name__, str(e)[:60])) from e
        finally:
            subprocess.run, subprocess.Popen, urllib.request.urlopen, builtins.open, m._kiem_dich_ghi, m._ghi_nguyen_tu_0600, sys.getfilesystemencoding, m._bootstrap_agent_creds = cu
        return kq, out.getvalue(), [d for d in err.getvalue().splitlines() if d]
    def boot(self, luot, bundle, khai, cu=CU, env="chat", req=False, **kw):
        os.environ["TL_TOKEN"], os.environ["TL_WEBAPP"] = TRUOC
        open(self.cfg, "wb").write(cu)
        self.m.drive["S"] = store.encrypt(bundle if isinstance(bundle, bytes) else json.dumps(bundle).encode("utf-8"), MK)
        ns = argparse.Namespace(secrets_id="S", secrets_file=None, env=env, config=None, profile=None, no_gws=True, no_nlm=True, bindir=None, require_agent_creds=req)
        return self.goi(luot, lambda: self.m.cmd_bootstrap(ns), khai, **kw)
    def xs(self, luot, **nhan):
        self.so.append((self.ca, luot))
        for n, dk in nhan.items():
            if not dk:
                raise Do(self.ca, luot, n)
_b = lambda **kv: ("{" + ", ".join('"%s": %s' % (k, v if isinstance(v, str) and v[:1] in "[{0123456789" and not v.startswith('"') else json.dumps(v)) for k, v in kv.items()) + "}").encode("utf-8")
def _env(): return (os.environ.get("TL_TOKEN"), os.environ.get("TL_WEBAPP"))
def _doc(p): return open(p, "rb").read() if os.path.exists(p) else None
def _ac(out): return sum(d.startswith("[bootstrap] agent_creds:") for d in out.splitlines()) == 1
def _x(err): return [d for d in err if d.startswith("[bootstrap] ✗ ")]
def w6_du_lieu(r, khai):
    tam = lambda: [t for t in os.listdir(r.h) if t.startswith(".auth.json.")]
    def tu_choi(luot, bundle, truong, cu=CU, m2=True):
        kq, out, err = r.boot(luot, bundle, khai, cu=cu)
        lo = (SENT in out + "\n".join(err)) or (TOK in out + "\n".join(err))
        nhan = dict(env=_env() == TRUOC) if m2 else dict(env_token=_env()[0] == TOK, env_web=_env()[1] == WEB)
        nhan.update(cfg=_doc(r.cfg) == cu and not tam())
        if m2:
            nhan.update(khong_chot=r.dem["chot"] == 0)
        nhan.update(khong_ghi=r.dem["ghi"] == 0)
        if m2:
            nhan.update(khong_doc=r.dem["doc"] == 0)
        nhan.update(khong_lo=not lo, dong_loi=_x(err) == ["[bootstrap] ✗ dữ liệu không hợp lệ: " + truong], agent=_ac(out), ma=kq == 1 and "✓ config" not in out)
        r.xs(luot, **nhan)
    kq, out, err = r.boot("W6.hop_le", {"token": TOK, "webappUrl": WEB, "rootFolderId": "r"}, khai, cu=CU_MERGE)
    r.xs("W6.hop_le", duong=kq == 0 and not err and _env() == (TOK, WEB) and "✓ config" in out and _ac(out),
         merge=json.loads(_doc(r.cfg)) == {"token": TOK, "giu": "x", "webappUrl": WEB, "rootFolderId": "r"})
    for luot, v in (("W6.web_kieu", "7"), ("W6.web_nul", SENT + "\x00"), ("W6.web_dc80", SENT + "\udc80")):
        tu_choi(luot, _b(token=TOK, webappUrl=v), "webappUrl")
    for luot, v in (("W6.token_kieu", "5"), ("W6.token_nul", SENT + "\x00"), ("W6.token_dc80", SENT + "\udc80"), ("W6.token_d800", SENT + "\ud800")):
        tu_choi(luot, _b(token=v, webappUrl=WEB), "token")
    kq, out, err = r.boot("W6.jar_va_token", _b(token="5", nlm_auth="[1]"), khai)
    r.xs("W6.jar_va_token", hai_dong=kq == 1 and _x(err) == [LJAR, "[bootstrap] ✗ dữ liệu không hợp lệ: token"] and _env() == TRUOC and _ac(out))
    kq, out, err = r.boot("W6.require", _b(token=TOK, webappUrl="7"), khai, req=True)
    r.xs("W6.require", require=kq == 4 and _x(err) == ["[bootstrap] ✗ dữ liệu không hợp lệ: webappUrl", D01] and _ac(out))
    kq, out, err = r.boot("W6.require_da_nap", _b(token=TOK, webappUrl="7"), khai, req=True, agent=("ĐÃ NẠP", "gia"))
    r.xs("W6.require_da_nap", require=kq == 1 and _x(err) == ["[bootstrap] ✗ dữ liệu không hợp lệ: webappUrl"] and _ac(out))
    kq, out, err = r.boot("W6.code", {"token": TOK, "webappUrl": 7, "gws_cred": '{"gia": 1}'}, khai, env="code")
    r.xs("W6.code", tiep_tuc=kq == 1 and _x(err) == ["[bootstrap] ✗ dữ liệu không hợp lệ: webappUrl"] and _doc(os.path.join(r.gws, "credentials.json")) == b'{"gia": 1}'
         and "[bootstrap] ✓ gws cred → " in out and _ac(out) and _env() == TRUOC)
    tu_choi("W6.encode", _b(token=TOK, webappUrl=WEB, rootFolderId=SENT + "\ud800"), "config", m2=False)
    tu_choi("W6.encode_cu", {"token": TOK, "webappUrl": WEB}, "config", cu=('{"x": %s}' % json.dumps(SENT + "\ud800")).encode("utf-8"), m2=False)
    tu_choi("W6.nan", _b(token=TOK, webappUrl=WEB, extra="1e999"), "config", m2=False)
    tu_choi("W6.nan_cu", {"token": TOK, "webappUrl": WEB}, "config", cu=b'{"x": NaN}', m2=False)
    for luot, cu in (("W6.dict_list", b"[]"), ("W6.dict_null", b"null"), ("W6.dict_str", b'"s"')):
        kq, out, err = r.boot(luot, {"token": TOK}, khai, cu=cu)
        r.xs(luot, duong_dict=kq == 0 and not err and json.loads(_doc(r.cfg)) == {"token": TOK} and "✓ config" in out)
    kq, out, err = r.boot("W6.token_falsy", {"token": 0}, khai)
    r.xs("W6.token_falsy", thieu=kq == 0 and err == ["[bootstrap] ⚠ bundle thiếu GAS token."] and _env() == TRUOC and _doc(r.cfg) == CU)
    kq, out, err = r.boot("W6.web_falsy", {"token": TOK, "webappUrl": 0}, khai)
    r.xs("W6.web_falsy", web_falsy=kq == 0 and not err and _env() == (TOK, TRUOC[1]) and json.loads(_doc(r.cfg)) == {"token": TOK, "webappUrl": 0})
def w6_locale(r, khai):
    kq, out, err = r.boot("W6.web_locale", _b(token=TOK, webappUrl="https://wp433b.invalid/é"), khai, fsenc="ascii")
    r.xs("W6.web_locale", env=_env() == TRUOC, dong_loi=_x(err) == ["[bootstrap] ✗ dữ liệu không hợp lệ: webappUrl"] and kq == 1 and _ac(out))
    that = sys.getfilesystemencoding().lower().replace("-", "")          # tiền điều kiện: tiến trình thật mã hoá env bằng UTF-8
    u = "https://wp433b.invalid/\u00e9"
    kq, out, err = r.boot("W6.web_utf8", _b(token=TOK, webappUrl=u), khai, fsenc="utf-8")
    r.xs("W6.web_utf8", tien_de=that == "utf8", duong_utf8=kq == 0 and not err and _env() == (TOK, u) and json.loads(_doc(r.cfg)) == {"token": TOK, "webappUrl": u})
def jar_rong_base(r, khai):
    os.environ["TL_TOKEN"] = TOK; nl = os.path.join(r.h, ".notebooklm-mcp-cli")
    for luot, b in (("W1.rong", {"nlm_auth": {}}), ("W1.vang", {})):
        r.m.drive["S"] = store.encrypt(json.dumps(b).encode("utf-8"), MK)
        kq, out, err = r.goi(luot, lambda: r.m.cmd_nlm_auth_pull(argparse.Namespace(secrets_id="S", secrets_file=None, env="code", config=None, profile=None)), khai)
        r.xs(luot, base_w1=kq == 1 and err == ["[nlm-auth-pull] ⚠ bundle chưa có nlm_auth — ở Code chạy `tl secrets-set --nlm` trước."] and not os.path.lexists(nl))
    for luot, j in (("W3.rong", {}), ("W3.list_rong", []), ("W3.list", [["auth.json", "x"]])):
        r.m.drive["N"] = store.encrypt(json.dumps(j).encode("utf-8"), TOK)
        kq, out, err = r.goi(luot, lambda: r.m._nlm_auth_load(TOK, "N"), khai)
        r.xs(luot, base_w3=kq == (False, "nlm_cred rỗng/sai định dạng.") and not os.path.lexists(nl))
    kq, out, err = r.boot("W2.rong", {"token": TOK, "gws_cred": '{"gia": 1}', "nlm_auth": {}}, khai, env="code")
    r.xs("W2.rong", base_w2=kq == 0 and not err and not os.path.lexists(nl))
CA = (w6_du_lieu, w6_locale, jar_rong_base)
LUOT = {"w6_du_lieu": ("W6.hop_le", "W6.web_kieu", "W6.web_nul", "W6.web_dc80", "W6.token_kieu", "W6.token_nul", "W6.token_dc80", "W6.token_d800",
                       "W6.jar_va_token", "W6.require", "W6.require_da_nap", "W6.code", "W6.encode", "W6.encode_cu", "W6.nan", "W6.nan_cu",
                       "W6.dict_list", "W6.dict_null", "W6.dict_str", "W6.token_falsy", "W6.web_falsy"),
        "w6_locale": ("W6.web_locale", "W6.web_utf8"), "jar_rong_base": ("W1.rong", "W1.vang", "W3.rong", "W3.list_rong", "W3.list", "W2.rong")}
def chay(nguon, khai, chi=None):
    m, so = nap(nguon), []
    for ca in CA:
        if chi and ca.__name__ != chi: continue
        with Rig(m, ca.__name__, so) as r:
            ca(r, khai)
    if not chi:
        assert so == [(c, l) for c, ds in LUOT.items() for l in ds], "SO_LUOT"
_ENV_LOOP = 'if ten == "token" or v:'
_TOKEN_IF = '    ly_env = _kiem_env_w6(bundle) if bundle.get("token") else None'
_LY_ENV = '        print(f"[bootstrap] ✗ {ly_env}", file=sys.stderr); degraded = True\n'
_DUMP = 'du_cfg = json.dumps(existing, ensure_ascii=False, allow_nan=False).encode("utf-8")'
_EXC = 'du_cfg, ly_cfg = None, "dữ liệu không hợp lệ: config"'
_REQ = '    if getattr(a, "require_agent_creds", False) and ac != "ĐÃ NẠP":'
_CFGP = 'os.path.expanduser("~/.tra_luat_config.json")'
DB = [
    ("db_w6_bo_kiem_web", [(_ENV_LOOP, 'if ten == "token":')]),
    ("db_w6_bo_kiem_kieu", [('if not isinstance(v, str) or "\\x00" in v:', 'if "\\x00" in v:')]),
    ("db_w6_bo_kiem_nul", [('if not isinstance(v, str) or "\\x00" in v:', 'if not isinstance(v, str):')]),
    ("db_w6_bo_kiem_encode", [('                v.encode("utf-8")\n', '                pass\n')]),
    ("db_w6_gan_token_truoc", [(_TOKEN_IF, '    bundle.get("token") and os.environ.__setitem__("TL_TOKEN", bundle["token"])\n' + _TOKEN_IF)]),
    ("db_w6_bo_kiem_token", [(_ENV_LOOP, 'if ten != "token" and v:')]),
    ("db_w6_bo_bat_encode", [("except ValueError:   # WP433 P2b: NaN", "except ZeroDivisionError:   # WP433 P2b: NaN")]),
    ("db_w6_kiem_bundle_thay_existing", [(_DUMP, 'du_cfg = json.dumps(bundle, ensure_ascii=False, allow_nan=False).encode("utf-8") and None'),
                                         ("_ghi_nguyen_tu_0600(cfgp, du_cfg)", "_ghi_nguyen_tu_0600(cfgp, json.dumps(existing, ensure_ascii=False).encode(\"utf-8\"))")]),
    ("db_w6_encode_go_env", [(_EXC, _EXC + '; os.environ.pop("TL_TOKEN", None)')]),
    ("db_w6_encode_ghi_rong", [(_EXC, 'du_cfg = b"{}"')]),
    ("db_w6_bo_kiem_dict", [("                if not isinstance(existing, dict):", "                if False:")]),
    ("db_w6_dict_thanh_loi", [("                if not isinstance(existing, dict):   # WP433 P2b: config cũ không phải dict ⇒ như không parse được\n                    existing = {}\n",
                               "                if not isinstance(existing, dict):\n                    ly_cfg = \"dữ liệu không hợp lệ: config\"\n")]),
    ("db_w6_token_co_mat", [(_TOKEN_IF, '    ly_env = _kiem_env_w6(bundle) if "token" in bundle else None')]),
    ("db_w6_web_co_mat", [(_ENV_LOOP, 'if ten == "token" or ten in bundle:')]),
    ("db_w6_lo_gia_tri", [(_LY_ENV, _LY_ENV + '        print(f"[bootstrap] w6={repr(bundle.get(\'token\'))[:80]}{repr(bundle.get(\'webappUrl\'))[:80]}")\n')]),
    ("db_w6_tu_choi_hop_le", [("    return None\n\n\ndef _duong_dich_chuan(", '    return "dữ liệu không hợp lệ: token"\n\n\ndef _duong_dich_chuan(')]),
    ("db_w6_quen_degraded", [(_LY_ENV, '        print(f"[bootstrap] ✗ {ly_env}", file=sys.stderr)\n')]),
    ("db_w6_ghi_khi_tu_choi", [(_LY_ENV, _LY_ENV + '        _ghi_nguyen_tu_0600(%s, b"{}")\n' % _CFGP)]),
    ("db_w1_jar_rong_moi", [("    nlm = bundle.get(\"nlm_auth\")\n    if not nlm:\n", "    nlm = bundle.get(\"nlm_auth\")\n    if nlm is None:\n")]),
    ("db_w3_dinh_dang_moi", [('    if not isinstance(nlm, dict) or not nlm:\n        return False, "nlm_cred', '    if not nlm:\n        return False, "nlm_cred')]),
    ("db_w2_jar_rong_moi", [("ly_jar = _kiem_jar_nlm(jar) if jar else None", "ly_jar = _kiem_jar_nlm(jar) if jar is not None else None")]),
    ("db_w6_tu_choi_van_chot", [(_LY_ENV, _LY_ENV + '        _kiem_dich_ghi(%s, %s, ())\n' % (_CFGP, _CFGP))]),
    ("db_w6_tu_choi_van_doc", [(_LY_ENV, _LY_ENV + '        open(%s, encoding="utf-8").read()\n' % _CFGP)]),
    ("db_w6_tu_choi_ghi_lai", [(_LY_ENV, _LY_ENV + '        _ghi_nguyen_tu_0600(%s, open(%s, "rb").read())\n' % (_CFGP, _CFGP))]),
    ("db_w6_encode_ghi_cu", [(_EXC, _EXC + '; _ghi_nguyen_tu_0600(cfgp, open(cfgp, "rb").read())')]),
    ("db_w6_khong_merge", [("                existing.update({k: v for k, v in bundle.items()", "                existing = {}; existing.update({k: v for k, v in bundle.items()")]),
    ("db_w6_cho_nan", [(_DUMP, 'du_cfg = json.dumps(existing, ensure_ascii=False).encode("utf-8")')]),
    ("db_w6_bo_kiem_locale", [('                    v.encode(sys.getfilesystemencoding(), "surrogateescape")\n', '                    pass\n')]),
    ("db_w6_dung_som", [(_LY_ENV, _LY_ENV + '        return 1\n')]),
    ("db_w6_bo_nhanh_sau", [(_LY_ENV, _LY_ENV + '        env = "chat"\n')]),
    ("db_w6_require_thua_rc1", [(_REQ, "    if degraded:\n        return 1\n" + _REQ)]),
    ("db_w6_require_luon_4", [(_REQ, '    if getattr(a, "require_agent_creds", False):')]),
    ("db_w6_dung_ly_jar", [(_TOKEN_IF, '    ly_env = _kiem_env_w6(bundle) if bundle.get("token") and not ly_jar else None')]),
    ("db_w6_locale_ep_ascii", [('v.encode(sys.getfilesystemencoding(), "surrogateescape")', 'v.encode("ascii" if sys.getfilesystemencoding() == "utf-8" else sys.getfilesystemencoding(), "surrogateescape")')]),
    ("db_w6_encode_go_web", [(_EXC, _EXC + '; os.environ.pop("TL_WEBAPP", None)')]),
    ("db_w6_lap_dong", [(_LY_ENV, '        print(f"[bootstrap] ✗ {ly_env}", file=sys.stderr); ' + _LY_ENV.lstrip())]),
]
KHAI = {
    "W6.web_kieu": ((TypeError, "str expected, not int", "nem_env"), (TypeError, "iterable", "nem_kiem")),
    "W6.web_nul": ((ValueError, "embedded null", "nem_env"),),
    "W6.token_kieu": ((TypeError, "str expected, not int", "nem_env"),),
    "W6.jar_va_token": ((TypeError, "str expected, not int", "nem_env"),),
    "W6.encode": ((UnicodeEncodeError, "surrogates not allowed", "nem_encode"),),
    "W6.encode_cu": ((UnicodeEncodeError, "surrogates not allowed", "nem_encode"),),
    "W6.dict_list": ((AttributeError, "object has no attribute 'update'", "nem_dict"),),
}
def ket(nguon, chi=None):
    try:
        chay(nguon, KHAI, chi)
        return "SONG_SOT"
    except Do as e:
        return e.k
if __name__ == "__main__":
    print("NỀN ỨNG VIÊN:", ket(NGUON), "· số lượt", sum(map(len, LUOT.values())))
    if "--base" in sys.argv:
        sys.exit()
    for ten, cap in DB:
        n = NGUON
        for a, b in cap:
            c = n.count(a)
            if c != 1:
                print(ten, "HONG neo", c, repr(a[:50])); break
            n = n.replace(a, b)
        else:
            print(ten, "→", ket(n))
