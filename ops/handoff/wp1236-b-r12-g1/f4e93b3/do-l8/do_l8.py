import sys, hashlib, importlib.util, json, collections
from pathlib import Path
import yaml
goc = Path(sys.argv[1]).resolve()
def nap(ten, p):
    s = importlib.util.spec_from_file_location(ten, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
len_ = nap("len_", goc / "ops/land_evidence_nguon.py")
dc = nap("dc", goc / "ops/gate_output_doi_chieu.py")
kq = {"cutover": [], "do": {}, "dat": [], "khong": [], "loi": {}}
ly = collections.Counter()
for tep in sorted((goc / "ops/land").glob("*-land-evidence.yaml")):
    b = tep.read_bytes(); h = hashlib.sha256(b).hexdigest()
    if len_.MIEN_TRU_CUTOVER.get(tep.name) == h:
        kq["cutover"].append(tep.name); continue
    try:
        d = len_.nap_yaml(yaml, b)
    except Exception as e:
        kq["loi"][tep.name] = repr(e); continue
    ten = tep.name[:-len("-land-evidence.yaml")]
    vp = dc.kiem_ho_so(d, tep.parent / f"{ten}-provenance")
    if vp:
        kq["do"][tep.name] = (h, vp)
        for x in vp:
            r = x.split(": ", 1)[1]
            ly[r.split(":")[0]] += 1
    elif dc.loi_khai(d):
        kq["dat"].append(tep.name)
    else:
        kq["khong"].append(tep.name)
print("tong", sum(len(v) for v in kq.values()), {k: len(v) for k, v in kq.items()})
print(dict(ly), sum(ly.values()))
json.dump(kq, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
