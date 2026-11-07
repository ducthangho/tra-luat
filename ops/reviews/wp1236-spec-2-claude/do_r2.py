import sys, re, json, hashlib, collections
from pathlib import Path
import yaml
goc = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(goc/'ops'))
import land_evidence_nguon as L
MIEN = {"gate_output_nguon", "gate_output_nguon_va_gioi_han", "moc_gate_output_rc_disposition"}
TAP = {"passed","measured","not_measured","failed","skipped","not_run","owner_waived"}
RE_TOK = re.compile(r"\s*([a-z_]+)(?=$|[\s—\-:(,.;])")
def la_khoa(k):
    if not isinstance(k,str): return False
    c = k.casefold()
    return ("gate_output" in c or "gate-output" in c)
def walk(n, d="$", anc=()):
    if isinstance(n, dict):
        for k,v in n.items():
            yield d, n, k, v, anc
            yield from walk(v, f"{d}.{k}", anc+(n,))
    elif isinstance(n, list):
        for i,v in enumerate(n):
            yield from walk(v, f"{d}[{i}]", anc)
def dang(v):
    if isinstance(v, dict): return "mapping"
    if isinstance(v, list): return "list"
    if not isinstance(v, str): return "khac_kieu:"+type(v).__name__
    m = RE_TOK.match(v.casefold())
    if not m: return "chuoi_khac"
    t = m.group(1)
    return t if t in TAP else "chuoi_khac"
ten = collections.Counter(); dangc = collections.Counter()
hs = {}
rows = []
for tep in sorted((goc/'ops/land').glob('*-land-evidence.yaml')):
    b = tep.read_bytes()
    try: du = L.nap_yaml(yaml, b)
    except Exception as e:
        print("LOI", tep.name, e); continue
    gt = tep.name[:-len('-land-evidence.yaml')]
    for d, m, k, v, anc in walk(du):
        if la_khoa(k):
            ten[k] += 1
            if k in MIEN: continue
            dg = dang(v)
            dangc[dg] += 1
            hs.setdefault(gt, []).append((f"{d}.{k}", dg, v if isinstance(v,str) else type(v).__name__))
            rows.append((gt, f"{d}.{k}", dg))
print("TEN", dict(ten))
print("DANG", dict(dangc), sum(dangc.values()))
print("HS co loi khai:", len(hs))
khong_nm = {h:[x for x in r if x[1] != 'not_measured'] for h,r in hs.items()}
khong_nm = {h:r for h,r in khong_nm.items() if r}
print("HS co loi khai != not_measured:", len(khong_nm), "tong", sum(len(r) for r in khong_nm.values()))
cut = set(n[:-len('-land-evidence.yaml')] for n in L.MIEN_TRU_CUTOVER)
# hash-match cutover
cut_khop = set()
for n,bam in L.MIEN_TRU_CUTOVER.items():
    p = goc/'ops/land'/n
    if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==bam: cut_khop.add(n[:-len('-land-evidence.yaml')])
print("cutover khop:", len(cut_khop), "khong khop:", sorted(cut - cut_khop))
trong_cut = sorted(h for h in khong_nm if h in cut)
print("trong cutover:", trong_cut, len(trong_cut))
print("trong cutover nhung khong khop bam:", [h for h in trong_cut if h not in cut_khop])
ngoai = sorted(h for h in khong_nm if h not in cut)
print("ngoai cutover:", len(ngoai))
# provenance by schema
def prov_files(h):
    d = goc/'ops/land'/f"{h}-provenance"
    out=[]
    if not d.is_dir(): return None
    for p in sorted(d.rglob('*.yaml')):
        try:
            x = yaml.safe_load(p.read_text(encoding='utf-8'))
        except Exception: continue
        if isinstance(x, dict) and x.get('schema') == 'ci_provenance/1': out.append(p)
    return out
allp = {}
for tep in sorted((goc/'ops/land').glob('*-land-evidence.yaml')):
    gt = tep.name[:-len('-land-evidence.yaml')]
    pf = prov_files(gt)
    if pf: allp[gt]=pf
print("HS co provenance schema:", len(allp), "tong tep", sum(len(v) for v in allp.values()))
# also any ci_provenance/1 files anywhere under ops/land not in matching dirs
tot=0
for p in (goc/'ops/land').rglob('*.yaml'):
    try: x=yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception: continue
    if isinstance(x,dict) and x.get('schema')=='ci_provenance/1': tot+=1
print("tong tep ci_provenance/1 duoi ops/land:", tot)
cp = sum(1 for h in khong_nm if h in allp)
print("trong 44: co prov", cp, "khong", len(khong_nm)-cp)
print("ngoai cutover co prov", sum(1 for h in ngoai if h in allp))
json.dump({h:[[a,b,str(c)[:200]] for a,b,c in r] for h,r in hs.items()}, open(sys.argv[2],'w'), ensure_ascii=False, indent=1)
for h in ngoai:
    r = khong_nm[h]
    print(f"  {h} prov={len(allp.get(h,[]))} n={len(hs[h])} dang={sorted(set(x[1] for x in hs[h]))}")
print("--- chuoi_khac / mapping / list:")
for h,r in hs.items():
    for a,b,c in r:
        if b in ("chuoi_khac","mapping","list") or b.startswith("khac"):
            print("  ",h,a,b,repr(str(c)[:100]))
