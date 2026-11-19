"""Đo hành vi W6 (cmd_bootstrap, nhánh token → env + ~/.tra_luat_config.json) trên một cây tl. Dữ liệu GIẢ, không mạng.
Dùng: python3 -I do_w6.py <thư mục scripts của cây>"""
import argparse, contextlib, io, json, os, shutil, subprocess, sys, tempfile, types, urllib.request
SC = os.path.realpath(sys.argv[1]); sys.path.insert(0, SC)
import tl  # noqa: E402
goc = tl._imp("tl_gws"); goc.bind(tl); store = tl._imp("gws_cred_store")
MK = "wp433b-master-gia"
def nap():
    m = types.ModuleType("w6do"); m.__file__ = goc.__file__
    exec(compile(open(goc.__file__, encoding="utf-8").read(), goc.__file__, "exec"), m.__dict__); m.bind(tl)
    m.drive = {}
    m._secrets_fetch = lambda a, fid: (m.drive.get(fid), "gia"); m.load_creds = lambda *a, **k: None
    m._gas = lambda: (_ for _ in ()).throw(RuntimeError("MANG_BI_CHAN")); m.AGENT_CREDS_FILEID = ""
    return m
def mot(ten, bundle_bytes, cu=None, env_truoc=None):
    m = nap(); td = os.path.realpath(tempfile.mkdtemp(prefix="w6do-")); cu_env, cu_cwd = dict(os.environ), os.getcwd()
    try:
        for k in [k for k in os.environ if k.startswith("TL_")]: os.environ.pop(k)
        h = os.path.join(td, "home"); os.makedirs(h)
        os.environ.update(TL_MASTER_KEY=MK, HOME=h, USERPROFILE=h, CODEX_HOME=os.path.join(td, "cx"), GOOGLE_WORKSPACE_CLI_CONFIG_DIR=os.path.join(td, "gws"))
        os.environ.update(env_truoc or {}); os.chdir(td)
        cfgp = os.path.join(h, ".tra_luat_config.json")
        if cu is not None: open(cfgp, "wb").write(cu)
        m.drive["S"] = store.encrypt(bundle_bytes, MK)
        ns = argparse.Namespace(secrets_id="S", secrets_file=None, env="chat", config=None, profile=None, no_gws=True, no_nlm=True, bindir=None, require_agent_creds=False)
        out, err = io.StringIO(), io.StringIO(); kq = None
        cuu = (subprocess.run, subprocess.Popen, urllib.request.urlopen)
        subprocess.run = subprocess.Popen = urllib.request.urlopen = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("MANG_BI_CHAN"))
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                kq = ("rc", m.cmd_bootstrap(ns))
        except BaseException as e:
            kq = ("NEM", type(e).__name__, str(e)[:90])
        finally:
            subprocess.run, subprocess.Popen, urllib.request.urlopen = cuu
        cfg = open(cfgp, "rb").read() if os.path.exists(cfgp) else None
        print(f"{ten}: {kq} | TL_TOKEN={os.environ.get('TL_TOKEN')!r} TL_WEBAPP={os.environ.get('TL_WEBAPP')!r} | cfg={cfg!r}"[:400])
        print("   err=", [d for d in err.getvalue().splitlines() if d][:4]); print("   out_ac=", sum(d.startswith("[bootstrap] agent_creds:") for d in out.getvalue().splitlines()))
    finally:
        os.chdir(cu_cwd); os.environ.clear(); os.environ.update(cu_env); shutil.rmtree(td, ignore_errors=True)
CU = b'{"token": "CU"}'
mot("B0 hop_le", b'{"token": "tok", "webappUrl": "https://w", "rootFolderId": "r"}', CU)
mot("B1 token_so", b'{"token": 5}', CU)
mot("B2 token_d800", b'{"token": "a\\ud800"}', CU)
mot("B3 token_dc80", b'{"token": "a\\udc80"}', CU)
mot("B4 token_nul", b'{"token": "a\\u0000b"}', CU)
mot("B5 web_nul", b'{"token": "tok", "webappUrl": "a\\u0000b"}', CU, {"TL_TOKEN": "truoc", "TL_WEBAPP": "truoc"})
mot("B6 web_so", b'{"token": "tok", "webappUrl": 7}', CU, {"TL_TOKEN": "truoc", "TL_WEBAPP": "truoc"})
mot("B7 web_d800", b'{"token": "tok", "webappUrl": "\\ud800"}', CU, {"TL_TOKEN": "truoc", "TL_WEBAPP": "truoc"})
mot("B8 root_d800", b'{"token": "tok", "rootFolderId": "\\ud800"}', CU)
mot("B9 cfg_list", b'{"token": "tok"}', b'[]')
mot("B10 cfg_null", b'{"token": "tok"}', b'null')
mot("B11 cfg_str", b'{"token": "tok"}', b'"s"')
mot("B12 cfg_cu_d800", b'{"token": "tok"}', b'{"x": "\\ud800"}')
mot("B13 token_0", b'{"token": 0}', CU)
mot("B14 token_null", b'{"token": null}', CU)
mot("B15 token_rong", b'{"token": ""}', CU)
mot("B16 web_rong_falsy0", b'{"token": "tok", "webappUrl": 0}', CU, {"TL_WEBAPP": "truoc"})
mot("B17 khoa_d800", b'{"token": "tok", "\\ud800": "x"}', CU)
mot("B18 token_list", b'{"token": ["a"]}', CU)
mot("B19 cfg_khong_doc", b'{"token": "tok"}', b'{hong')
mot("B20 bundle_list", b'[1]', CU)
