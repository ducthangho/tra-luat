# -*- coding: utf-8 -*-
"""Tái hiện nợ secrets-set (bundle giải mã không phải object; `token` không phải str) — KHÔNG mạng, KHÔNG secrets thật.

Dùng: python tai_hien.py <goc_kho> [tep_diff_ap_vao_tl_gws]
Nạp `scripts/tl_gws.py` của <goc_kho> vào module MỚI trong bộ nhớ (áp diff nếu có), thay MỌI hàm tải/ghi/mạng bằng đồ giả
có đếm lời gọi, HOME/TL_* tạm. In một dòng mỗi lượt: lượt · rc · dòng ✗/⚠ · bộ đếm · khoá mã hoá public (nếu có)."""
import argparse, contextlib, io, json, os, pathlib, shutil, subprocess, sys, tempfile, types  # noqa: E401

MK = "wp433-ss-master-gia-0123456789abcdefghijklmnop"   # >=32 ký tự, >=12 ký tự khác nhau; KHÔNG phải khoá thật
KIEU = (("list", [1, 2]), ("str", "chuoi"), ("int", 7), ("null", None), ("true", True))
CO = (("gas_token", dict(gas_token="tok-moi")), ("webapp", dict(webapp="https://gia.invalid/exec")),
      ("gws", dict(gws=True)), ("nlm", dict(nlm=True)), ("khong_co", {}))


def nap(goc_kho, diff):
    sys.path.insert(0, os.path.join(goc_kho, "scripts"))
    import tl  # noqa: E402
    goc = tl._imp("tl_gws"); goc.bind(tl)  # noqa: E702
    nguon = pathlib.Path(goc_kho, "scripts", "tl_gws.py").read_text(encoding="utf-8")
    if diff:
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d, "tl_gws.py"); p.write_text(nguon, encoding="utf-8")  # noqa: E702
            r = subprocess.run(["patch", "-s", str(p), diff], capture_output=True, text=True)
            if r.returncode:
                sys.exit("patch lỗi: " + r.stderr)
            nguon = p.read_text(encoding="utf-8")
    m = types.ModuleType("ss_tl_gws"); m.__file__ = goc.__file__  # noqa: E702
    exec(compile(nguon, goc.__file__, "exec"), m.__dict__)
    m.bind(tl)
    return m, tl._imp("gws_cred_store")


def mot_luot(m, store, ten, bundle_obj, co, env_token=None):
    dem = {"fetch": 0, "upload": 0, "stage_enc": 0, "gws_export": 0, "nlm_refresh": 0, "canary": 0, "gas": 0}
    khoa = []
    blob = store.encrypt(json.dumps(bundle_obj).encode("utf-8"), MK)

    def fetch(a, fid):
        dem["fetch"] += 1; return blob, "gia"  # noqa: E702
    def up(*a, **k):
        dem["upload"] += 1; return "fid-gia", None  # noqa: E702
    def stg(name, b, *a, **k):
        dem["stage_enc"] += 1  # noqa: E701
    def gexp():
        dem["gws_export"] += 1; return b'{"cred":"gia"}'  # noqa: E702
    def refr():
        dem["nlm_refresh"] += 1; return True  # noqa: E702
    jar = {"auth.json": "gia"}
    def can(tag, nb=None):
        dem["canary"] += 1; return jar, 0, None  # noqa: E702
    def gas():
        dem["gas"] += 1; raise RuntimeError("MANG_BI_CHAN")  # noqa: E702
    proxy = types.SimpleNamespace(encrypt=lambda data, key: (khoa.append(key), store.encrypt(data, key))[1], decrypt=store.decrypt)
    that_imp = m._imp
    for k, v in (("_secrets_fetch", fetch), ("_secrets_upload", up), ("_stage_enc_upload", stg), ("_gws_export_cred", gexp),
                 ("_refresh_nlm_auth", refr), ("_nlm_auth_files", lambda: {"auth.json": 1}), ("_nlm_files_after_live_canary", can),
                 ("_nlm_auth_age_days", lambda n: None), ("_gas", gas), ("load_creds", lambda *a, **k: None),
                 ("_imp", lambda n: proxy if n == "gws_cred_store" else that_imp(n))):
        setattr(m, k, v)
    td, cu_env, cu_cwd = tempfile.mkdtemp(prefix="wp433ss-"), dict(os.environ), os.getcwd()
    try:
        for k in [k for k in os.environ if k.startswith("TL_")]:
            os.environ.pop(k)
        os.environ.update(HOME=td, USERPROFILE=td, TL_MASTER_KEY=MK)
        if env_token:
            os.environ["TL_TOKEN"] = env_token
        os.chdir(td)
        a = argparse.Namespace(secrets_id="fid-gia", config=None, profile=None, gas_token=None, webapp=None, gws=False, nlm=False,
                               no_public=False, folder=None, secrets_file=None, env=None)
        for k, v in co.items():
            setattr(a, k, v)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = m.cmd_secrets_set(a)
    finally:
        os.chdir(cu_cwd); os.environ.clear(); os.environ.update(cu_env); shutil.rmtree(td, ignore_errors=True)  # noqa: E702
    dong = [d for d in err.getvalue().splitlines() if "✗" in d or "⚠" in d]
    pub = [repr(k) for k in khoa if k != MK]
    print("%-26s rc=%s dem=%s khoa_public=%s | %s" % (ten, rc, json.dumps(dem, sort_keys=True), pub, " ‖ ".join(dong)))
    return rc, dem, pub, dong


def main():
    goc_kho, diff = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else None)
    m, store = nap(os.path.abspath(goc_kho), diff and os.path.abspath(diff))
    print("# kieu: bundle không phải object × cờ")
    for kt, kv in KIEU:
        for ct, cv in CO:
            mot_luot(m, store, "kieu.%s.%s" % (kt, ct), kv, cv)
    print("# token_kieu: bundle object, token không phải str, không TL_TOKEN")
    for tt, tv in (("list", [1]), ("dict", {"a": 1}), ("int", 7)):
        for ct, cv in (("gws", dict(gws=True)), ("nlm", dict(nlm=True))):
            mot_luot(m, store, "token_kieu.%s.%s" % (tt, ct), {"token": tv, "webappUrl": "u"}, cv)
    print("# hoi_quy: bundle object hợp lệ")
    for ct, cv in CO:
        mot_luot(m, store, "hoi_quy.%s" % ct, {"token": "tok-cu", "webappUrl": "u"}, cv)
    mot_luot(m, store, "hoi_quy.env_token.gws", {"token": [1], "webappUrl": "u"}, dict(gws=True), env_token="tok-env")


if __name__ == "__main__":
    main()
