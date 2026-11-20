"""Tai hien no #433 (2) w6-chot-to-tien, (3) bundle-khong-phai-dict, (4) trong-kho-git-nuot-oserror tren cay hien tai (cwd = goc kho)."""
import argparse, importlib.util, os, subprocess, sys
sys.path.insert(0, "scripts"); import tl  # noqa: E401,E402
s = importlib.util.spec_from_file_location("pk1", "scripts/test_fragments/wp433_nlm_gws_dich_ngoai_kho.py"); F = importlib.util.module_from_spec(s); s.loader.exec_module(F)
goc = tl._imp("tl_gws"); goc.bind(tl); store = tl._imp("gws_cred_store")
m = F._nap(open(goc.__file__, encoding="utf-8").read(), tl, goc)
def lua(ten, fn):
    with F._Rig(m, ten, store, True) as r:
        fn(r)
def in_(*a): print(*a, flush=True)
# (2) W6: HOME la symlink (va HOME co to tien la symlink) toi thu muc ngoai kho — W6 ghi xuyen; W5 cung duong thi tu choi.
def n2(r):
    for kieu in ("home_la_lk", "to_tien_la_lk"):
        t = r.p("T-" + kieu); os.makedirs(t)
        lk = r.p("L-" + kieu); os.symlink(t, lk, target_is_directory=True)
        h = lk if kieu == "home_la_lk" else os.path.join(lk, "home")
        os.makedirs(h, exist_ok=True); os.environ["HOME"] = os.environ["USERPROFILE"] = h
        os.environ["GOOGLE_WORKSPACE_CLI_CONFIG_DIR"] = os.path.join(h, ".config", "gws")
        rc, out, err = r.w2("N2-" + kieu, {})
        cfg_t = os.path.join(t, ".tra_luat_config.json") if kieu == "home_la_lk" else os.path.join(t, "home", ".tra_luat_config.json")
        in_(f"(2) {kieu}: rc={rc} config_ghi_vao_dich_that={os.path.isfile(cfg_t)} dong_config_ok={[l for l in out.splitlines() if 'config (token' in l][:1]!r}")
        in_(f"    stderr={err!r}")
lua("n2", n2)
# (3) bundle giai ma ra JSON khong phai dict: W2 bootstrap va W1 nlm-auth-pull
def n3(r):
    for goi in ([1, 2], "chuoi", 7, None):
        r.m.drive["S433"] = r._ma(goi)
        ns = argparse.Namespace(secrets_id="S433", secrets_file=None, env="code", config=None, profile=None, no_gws=True, no_nlm=True, bindir=None, require_agent_creds=False)
        try:
            rc = r.m.cmd_bootstrap(ns); kq = f"rc={rc}"
        except Exception as e:  # noqa: BLE001
            kq = f"NEM {type(e).__name__}: {e}"
        r.m.drive["S433"] = r._ma(goi)
        ns1 = argparse.Namespace(config=None, profile=None, secrets_id="S433", secrets_file=None, env=None)
        try:
            rc1 = r.m.cmd_nlm_auth_pull(ns1); kq1 = f"rc={rc1}"
        except Exception as e:  # noqa: BLE001
            kq1 = f"NEM {type(e).__name__}: {e}"
        in_(f"(3) bundle={goi!r}: W2 bootstrap -> {kq} · W1 nlm-auth-pull -> {kq1}")
import contextlib, io  # noqa: E401,E402
def n3_wrap(r):
    with contextlib.redirect_stderr(io.StringIO()):
        n3(r)
lua("n3", n3_wrap)
# (4) _trong_kho_git nuot OSError: (a) lstat bi thay bang PermissionError dung o <K>/.git; (b) that: user nobody, K co .git nhung khong co quyen x
def n4(r):
    k = r.kho("K4"); con = os.path.join(k, "con"); os.makedirs(con)
    that = os.lstat
    in_(f"(4a) truoc: _trong_kho_git({con!r}) = {m._trong_kho_git(con)!r}")
    def gia(p, *a, **kw):
        if os.path.abspath(os.fspath(p)) == os.path.join(k, ".git"):
            raise PermissionError(13, "wp433-gia", p)
        return that(p, *a, **kw)
    os.lstat = gia
    try:
        in_(f"(4a) lstat({k}/.git) nem PermissionError: _trong_kho_git = {m._trong_kho_git(con)!r} · _kiem_dich_ghi = {m._kiem_dich_ghi(os.path.join(con, 'f'), '/', tuple(os.path.join(con, 'f').strip('/').split('/')))!r}")
    finally:
        os.lstat = that
lua("n4", n4)
