"""Chan doan t246 (B5 criss-cross) tren Windows — phien dieu phoi #1206. Dung lai DUNG fixture t246 bang helper cua tep test H,
roi in: merge-base oracle git, X1/X2, rc/stdout/stderr cua ung vien, receipt (neu co), va to_mau_hai_phia truc tiep."""
import importlib.util, json, sys, subprocess, traceback
sys.dont_write_bytecode = True
goc = sys.argv[1]
sys.path.insert(0, goc + "/ops")


def nap(p, ten):
    sp = importlib.util.spec_from_file_location(ten, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


lp = nap(goc + "/ops/lease_publish_test.py", "lp_test")
mod = lp._nap_cong()
out = {}
with lp.San() as s:
    cay = lp._amb_kho(s)
    t0 = lp._amb_cay_rong(cay)
    B0 = lp._amb_cm(cay, t0, (), 100, "B0")
    t_pol = subprocess.run(["git", "-C", str(cay), "hash-object", "-w", "--stdin"], input=b"{}\n", capture_output=True, check=True).stdout.decode().strip()
    for dong in ("100644 blob {}\tchange-impact.v1.json\n", "040000 tree {}\tcoordination\n", "040000 tree {}\t.github\n"):
        t_pol = lp._amb_cay_rong(cay, dong.format(t_pol))
    X1 = lp._amb_cm(cay, t0, (B0,), 110, "X1")
    for nonce in range(64):
        X2 = lp._amb_cm(cay, t_pol, (B0,), 111, f"X2 {nonce}")
        if X1 < X2:
            break
    S = lp._amb_cm(cay, t0, (X1, X2), 120, "S")
    H = lp._amb_cm(cay, t0, (X2, X1), 121, "H")
    out.update(t0=t0, t_pol=t_pol, B0=B0, X1=X1, X2=X2, S=S, H=H, oracle=lp._amb_merge_base_git(cay, S, H),
               vung_git_X1=lp._amb_vung_git(cay, X1), vung_git_X2=lp._amb_vung_git(cay, X2),
               cat_X2=subprocess.run(["git", "-C", str(cay), "cat-file", "-p", X2], capture_output=True).stdout.decode(errors="replace"),
               ls_tree_t_pol=subprocess.run(["git", "-C", str(cay), "ls-tree", "-r", t_pol], capture_output=True).stdout.decode(errors="replace"))
    rcp = s / "r.json"
    rc, o, e = lp._amb_m4(mod, cay, H, S, rcp)
    out.update(rc=rc, stdout=o, stderr=e, receipt=(json.loads(rcp.read_text(encoding="utf-8")) if rcp.is_file() else None))
    for ten in ("to_mau_hai_phia",):
        try:
            ko = mod.KhoObject(cay)
            try:
                r = getattr(mod, ten)(ko, S, H)
                out[ten] = {k: (v if isinstance(v, (int, str, list, bool, type(None))) else repr(v)) for k, v in r.items()}
            finally:
                ko.dong()
        except Exception:
            out[ten] = traceback.format_exc()
    for f in ("vung_tai", "vung_tai_S", "_vung"):
        out["co_ham_" + f] = hasattr(mod, f)
print(json.dumps(out, ensure_ascii=False, indent=1))
