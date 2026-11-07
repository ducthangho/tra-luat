"""Do lai bang 'Do lai tren 4f03566' cua r5. Chay tu repo: python -I -B ../work/dem_r5.py ../work/l6.json"""
import sys, re, yaml, collections, json
from pathlib import Path
sys.path.insert(0, 'ops'); import land_evidence_nguon as L
RE_TOK = re.compile(r"\s*([a-z_]+)(?=$|[\s—\-:(,.;])")
def norm(k): return ''.join(c for c in k.casefold() if c.isalnum())
PHI = {"gateoutputnguon", "gateoutputnguonvagioihan", "mocgateoutputrcdisposition"}
TOKS = {'passed','measured','not_measured','failed','skipped','not_run','owner_waived'}
def walk(n):
    if isinstance(n, dict):
        for k, v in n.items():
            yield n, k, v
            yield from walk(v)
    elif isinstance(n, list):
        for v in n: yield from walk(v)
l6 = json.load(open(sys.argv[1]))
landed = {Path(t['duong_dan']).name for t in l6['tep'] if t['trang_thai'] == 'DAT'}
hs = sorted(Path('ops/land').glob('*-land-evidence.yaml'))
print('ho so', len(hs))
nprov_hs = 0; nprov_tep = 0; ngoc = 0; dang = collections.Counter(); co_khoa = set(); khong_nm = set()
khoa_ten = collections.Counter()
for tep in hs:
    gt = tep.name[:-len('-land-evidence.yaml')]
    pd = Path('ops/land') / f'{gt}-provenance'
    n = 0
    if pd.is_dir():
        for p in pd.rglob('*.yaml'):
            try: x = yaml.safe_load(p.read_text(encoding='utf-8'))
            except Exception: continue
            if isinstance(x, dict) and x.get('schema') == 'ci_provenance/1': n += 1
    if n: nprov_hs += 1; nprov_tep += n
    du = L.nap_yaml(yaml, tep.read_bytes())
    if isinstance(du, dict) and isinstance(du.get('merge_commit'), str): ngoc += 1
    for m, k, v in walk(du):
        if isinstance(k, str) and 'gateoutput' in norm(k):
            khoa_ten[k] += 1
        if not (isinstance(k, str) and 'gateoutput' in norm(k) and norm(k) not in PHI): continue
        co_khoa.add(tep.name)
        if isinstance(v, str):
            mt = RE_TOK.match(v.casefold()); t = mt.group(1) if mt else None
            t = t if t in TOKS else 'chuoi_khac'
        else: t = type(v).__name__
        dang[t] += 1
        if t != 'not_measured': khong_nm.add(tep.name)
print('ho so co prov / so tep', nprov_hs, nprov_tep)
print('merge_commit goc', ngoc)
print('ten khoa', dict(khoa_ten))
print('gia tri', sum(dang.values()), dict(dang))
print('ho so co >=1 khoa loi khai', len(co_khoa), '; co >=1 khong phai not_measured', len(khong_nm))
print('landed', len(landed), '; landed khong co khoa', len(landed - co_khoa))
# L5 theo bam
import hashlib
mien = getattr(L, 'MIEN_TRU_CUTOVER', None)
khop = {t for t, b in mien.items() if (Path('ops/land')/t).exists() and hashlib.sha256((Path('ops/land')/t).read_bytes()).hexdigest() == b} if isinstance(mien, dict) else None
print('L5 MIEN_TRU_CUTOVER', type(mien).__name__, len(mien) if mien else None, 'khop bam', len(khop) if khop is not None else None)
if khop is not None:
    do = sorted(khong_nm - khop)
    print('L8 hoi to DO', len(do))
    print('  moi so voi 3163f4d?', [d for d in do if any(x in d for x in ('pr1229','pr1230','pr1242'))])
