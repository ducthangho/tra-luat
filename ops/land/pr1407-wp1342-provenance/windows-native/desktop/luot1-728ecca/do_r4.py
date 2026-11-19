# Chay tung ca packet_loop_test trong tien trinh con rieng; ghi JSONL: id, rc, giay, KQ_JSON, dong WP1342_NATIVE_V1.
import json, subprocess, sys, time, os
from pathlib import Path
src, nhan, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
che_do = sys.argv[4]          # "tap" (tap N5/N6 tu dong) | "ds" (danh sach id sau do) | "lap" (id lan)
LENH = ("import sys,tempfile,pathlib,json;sys.path.insert(0,'.claude/dev');import packet_loop_test as T;"
        "k=T.chay_suite(T.CANONICAL,pathlib.Path(tempfile.mkdtemp()),{sys.argv[1]});"
        "print('KQ_JSON '+json.dumps({n:(None if v is None else [type(v).__name__,str(v)[:900]]) for n,v in k.items()}));"
        "sys.exit(0 if list(k.values())==[None] else 1)")
LIET_KE = ("import sys,json;sys.path.insert(0,'.claude/dev');import packet_loop_test as T;ids=[i for i,_ in T.CASES];"
           "both=sorted(T.WP1174_BOTH);"
           "print(json.dumps([i for i in ids if i=='wp1174_windows_claim_rejected']+[i for i in ids if i in both]"
           "+[i for i in ids if i.startswith(('wp1342_native_','wp1342_pure','wp1342_additive'))]))")
def chay(cid):
    t0 = time.monotonic()
    try:
        p = subprocess.run([sys.executable, "-X", "utf8", "-B", "-c", LENH, cid], cwd=src, capture_output=True,
                           text=True, encoding="utf-8", errors="backslashreplace", timeout=150)
        rc, o, e = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as ex:
        rc, o, e = "TIMEOUT150", str(ex.stdout or ""), str(ex.stderr or "")
    g = round(time.monotonic() - t0, 1)
    (out / f"{nhan}-{cid}.txt").write_text(f"rc={rc} giay={g}\n--- stdout\n{o}\n--- stderr\n{e}", encoding="utf-8")
    kq = [ln for ln in o.splitlines() if ln.startswith("KQ_JSON ")]
    nat = [ln for ln in o.splitlines() if ln.startswith("WP1342_NATIVE_V1 ")]
    return {"nhan": nhan, "id": cid, "rc": rc, "giay": g, "kq": kq[-1][8:] if kq else None, "native": nat}
out.mkdir(parents=True, exist_ok=True)
if che_do == "tap":
    ids = json.loads(subprocess.run([sys.executable, "-B", "-c", LIET_KE], cwd=src, capture_output=True, text=True).stdout)
elif che_do == "ds":
    ids = sys.argv[5:]
else:
    ids = [sys.argv[5]] * int(sys.argv[6])
with open(out / f"{nhan}.jsonl", "a", encoding="utf-8") as f:
    for i, cid in enumerate(ids):
        r = chay(cid); r["lan"] = i
        f.write(json.dumps(r, ensure_ascii=False) + "\n"); f.flush()
        print(json.dumps({k: r[k] for k in ("id", "rc", "giay", "lan")}), flush=True)
