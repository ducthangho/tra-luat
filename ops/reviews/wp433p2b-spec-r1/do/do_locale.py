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
import sys as _s; print("fsenc=", _s.getfilesystemencoding())
mot("L1 web_e_locale", '{"token": "tok", "webappUrl": "https://x/\u00e9"}'.encode("utf-8"), CU, {"TL_TOKEN": "truoc", "TL_WEBAPP": "truoc"})
mot("L2 nan_bundle", b'{"token": "tok", "extra": 1e999}', CU)
mot("L3 nan_cu", b'{"token": "tok"}', b'{"x": NaN}')
