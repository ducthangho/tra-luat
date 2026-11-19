"""Tai lap N5/N6 tu log native trong ho so (windows-native/desktop/wp1342r5-out-20261119T120908Z), cung logic n5_1420.py tren Desktop.
Dung: python3 n5_1420_tai_lap.py <thu muc out>   ;  --phan-chung: doi rc mot ID base o HEAD thanh 1 => phai bao lech (rc 1)."""
import json, pathlib, sys
o = pathlib.Path(sys.argv[1]); pc = "--phan-chung" in sys.argv
def L(f):
    d = {}
    for l in (o / f).read_text(encoding="utf-8").splitlines():
        if l.startswith("{"):
            j = json.loads(l)
            if "rc" in j and "id" in j:
                d[j["id"]] = j["rc"]
    return d
B, H = L("BASE.stdout.txt"), L("HEAD.stdout.txt")
if pc:
    H[sorted(B)[0]] = 1
loi = [k for k, v in B.items() if v] + [k for k, v in H.items() if v] + [k for k in B if k not in H]
moi = sorted(set(H) - set(B))
DU = ["wp1342_native_job_breakaway_ngam", "wp1342_native_job_breakaway_tuong_minh", "wp1342_native_job_long", "wp1342_pure_spawn_fx_mo_rong"]
print("B", len(B), "H", len(H), "lech/do", loi, "moi", moi)
for n in DU[:3]:
    for l in (o / f"HEAD-{n}.txt").read_text(encoding="utf-8").splitlines():
        if l.startswith("WP1342_NATIVE_V1 "):
            j = json.loads(l[17:]); print(n, "executed", j["executed"], "passed", j["passed"], "observed", j["observed"][:160])
ok = not loi and moi == DU
print("N5:", "DAT" if ok else "DO")
sys.exit(0 if ok else 1)
