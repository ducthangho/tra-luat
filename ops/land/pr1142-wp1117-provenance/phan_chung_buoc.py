"""Phan chung connector P1 r4469885562: voi MOT run, tai log moi job MOT lan roi, cho tung buoc trong LUAT cua danh_gia_gate.py:
xoa dau hieu duong CHI cua buoc ay -> job PHAI ra not_measured. Them 3 ca dung: (a) giu TỔNG cua idiom_py_test, bo tl selftest;
(b) chen 'CI_DANG_KY x: ĐỎ' vao buoc registry; (c) them 'TỔNG: ĐỎ' cuoi buoc registry. Va doi chung: luat CU (dau hieu bat ky dau
trong log job) cho ca (a) ra passed — tuc lo hong connector tai hien duoc.
Cach goi: python3 phan_chung_buoc.py <run_id>   (danh_gia_gate.py cung thu muc). rc 0 = moi ca am dung + doi chung tai hien."""
import importlib.util, json, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
s = importlib.util.spec_from_file_location("d", os.path.join(here, "danh_gia_gate.py")); d = importlib.util.module_from_spec(s); s.loader.exec_module(d)
run = sys.argv[1]
jobs = [j for j in json.loads(d.raw(f"actions/runs/{run}/jobs?per_page=100"))["jobs"] if j["conclusion"] == "success"]
logs = {}
def log_cua(tien):
    j = next((j for j in jobs if j["name"].startswith(tien)), None)
    if j and j["id"] not in logs:
        logs[j["id"]] = d.raw(f"actions/jobs/{j['id']}/logs")
    return (j["name"], logs[j["id"]]) if j else (None, None)
sai, dong = 0, []
for tien, bl in d.LUAT:
    ten, b = log_cua(tien)
    if not ten:
        continue
    goc = d.danh_gia(ten, d.buoc(b))[0]
    dong.append(f"GOC  {ten}: {goc}")
    for nhan, _ in bl:
        tt = d.danh_gia(ten, d.am(d.buoc(b), nhan))[0]
        ok = tt != "passed"; sai += not ok
        dong.append(f"{'DAT' if ok else 'DO '}  am [{nhan}] trong {ten} -> {tt}")
ten, b = log_cua("gate (")
if ten:
    tt = d.danh_gia(ten, d.am(d.buoc(b), d.TL_SELFTEST))[0]; ok = tt != "passed"; sai += not ok
    dong.append(f"{'DAT' if ok else 'DO '}  ca (a) giu TỔNG idiom_py_test, bo tl selftest -> {tt}")
    phang = [l for x in d.am(d.buoc(b), d.TL_SELFTEST) for l in x["ra"]]
    cu = all(any(re.search(p, l) for l in phang) for p in [r"^TỔNG: ĐẠT$"])
    dong.append(f"{'DAT' if cu else 'DO '}  doi chung luat CU (bat ky 'TỔNG: ĐẠT' trong log job) cho ca (a) -> {'passed (lo hong tai hien)' if cu else 'not_measured'}")
    sai += not cu
ten, b = log_cua("gate-registry")
if ten:
    for nhan_ca, sua in (("(b) chen 'CI_DANG_KY ops/x_test.py: ĐỎ rc=1'", lambda r: r.insert(5, "CI_DANG_KY ops/x_test.py: ĐỎ rc=1")),
                         ("(c) them 'TỔNG: ĐỎ' cuoi buoc", lambda r: r.append("TỔNG: ĐỎ"))):
        ds = d.buoc(b); sua([x for x in ds if any("ci_dang_ky_test.py --chay" in y for y in x["lenh"])][0]["ra"])
        tt = d.danh_gia(ten, ds)[0]; ok = tt != "passed"; sai += not ok
        dong.append(f"{'DAT' if ok else 'DO '}  ca {nhan_ca} trong {ten} -> {tt}")
print(f"# phan_chung_buoc run {run} — danh_gia_gate.py sha256 {__import__('hashlib').sha256(open(os.path.join(here,'danh_gia_gate.py'),'rb').read()).hexdigest()}")
print("\n".join(dong)); print(f"SAI: {sai}")
sys.exit(1 if sai else 0)
