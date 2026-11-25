import os, sys, pathlib, tempfile, inspect, json, time
here = pathlib.Path(__file__).parent.resolve(); cay = (here / sys.argv[1]).resolve(); che_do = sys.argv[2]
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
tmp = here / "tmp" / (sys.argv[1] + "-" + che_do); tmp.mkdir(parents=True, exist_ok=True); os.environ["TMPDIR"] = str(tmp); tempfile.tempdir = str(tmp)
sys.path.insert(0, str(cay / ".claude/dev"))
import packet_loop_test as t
def lq(ten, fn):
    if ten.startswith(("doctrine_scan_", "ac18_", "ac19_")): return True
    try: return "doctrine" in inspect.getsource(fn)
    except Exception: return False
chon = [n for n, f in t.CASES if lq(n, f)]
if che_do == "ca":
    t0 = time.time(); kq = {}
    for n in chon: kq.update(t.chay_suite(t.CANONICAL, tmp / "ca", chi_chay={n}))
    do = {k: str(v)[:110] for k, v in kq.items() if v is not None}
    print("CHON", len(chon), "DAT", sum(v is None for v in kq.values()), "KHONG DAT", len(do), "giay", round(time.time() - t0))
    for k, v in list(do.items())[:12]: print("  ", k, "→", v)
    (here / f"kq-{sys.argv[1]}-ca.json").write_text(json.dumps({k: (None if v is None else str(v)) for k, v in kq.items()}, ensure_ascii=False))
else:  # đột biến có ca đích thuộc họ doctrine
    src = t.CANONICAL.read_text(encoding="utf-8"); S = set(chon); ra = {}; t0 = time.time()
    for ten, mu in t.MUTANTS.items():
        dich = [d for d in mu[2] if d in S]
        if not dich: continue
        if not (isinstance(mu[0], str) and isinstance(mu[1], str)) or src.count(mu[0]) != 1:
            ra[ten] = "BO (mốc không phải chuỗi đơn hoặc không khớp 1 chỗ)"; continue
        p = tmp / f"mu_{len(ra)}" / "packet_loop.py"; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src.replace(mu[0], mu[1], 1), encoding="utf-8", newline="\n")
        for f in t.CANONICAL.parent.glob("*.py"):
            if f.name != "packet_loop.py" and not (p.parent / f.name).exists(): os.symlink(f, p.parent / f.name)
        kq = t.chay_suite(p, tmp / f"mk_{len(ra)}", chi_chay=set(dich))
        ra[ten] = {d: t._phan_loai_giet(kq[d]) for d in dich}
    print("DOT BIEN co dich ho doctrine", len(ra), "giay", round(time.time() - t0))
    (here / f"kq-{sys.argv[1]}-mu.json").write_text(json.dumps(ra, ensure_ascii=False, indent=0))
    from collections import Counter
    print(Counter(v if isinstance(v, str) else "|".join(sorted(set(v.values()))) for v in ra.values()))
