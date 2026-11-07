"""Ap dinh nghia *Neo* + *Pham vi land* cua r4 len 123 ho so that. Chay tu repo: python -I ../work/land_r4.py"""
import sys, re, yaml, collections, json
from pathlib import Path
sys.path.insert(0, 'ops'); import land_evidence_nguon as L
RE_TOK = re.compile(r"\s*([a-z_]+)(?=$|[\s—\-:(,.;])")
def norm(k): return ''.join(c for c in k.casefold() if c.isalnum())
PHI = {"gateoutputnguon", "gateoutputnguonvagioihan", "mocgateoutputrcdisposition"}
H40 = re.compile(r'[0-9a-f]{40}'); MOC = {'run', 'checkout', 'workflow_definition', 'gate_output'}
def walk(n, chain=()):
    if isinstance(n, dict):
        for k, v in n.items():
            yield n, k, v, chain
            yield from walk(v, chain + (n,))
    elif isinstance(n, list):
        for v in n: yield from walk(v, chain)
l6 = json.load(open(sys.argv[1]))
landed = {Path(t['duong_dan']).name for t in l6['tep'] if t['trang_thai'] == 'DAT'}
dem = collections.Counter(); ra = []; PHU_HS = {}
for tep in sorted(Path('ops/land').glob('*-land-evidence.yaml')):
    du = L.nap_yaml(yaml, tep.read_bytes()); gt = tep.name[:-len('-land-evidence.yaml')]
    H = {du['merge_commit']} if isinstance(du.get('merge_commit'), str) and H40.fullmatch(du['merge_commit']) else set()
    H |= {x['merge_commit'] for x in (du.get('prs') or []) if isinstance(x, dict) and isinstance(x.get('merge_commit'), str) and H40.fullmatch(x['merge_commit'])}
    prov = {}
    pd = Path('ops/land') / f'{gt}-provenance'
    if pd.is_dir():
        for p in pd.rglob('*.yaml'):
            try: x = yaml.safe_load(p.read_text(encoding='utf-8'))
            except Exception: continue
            if isinstance(x, dict) and x.get('schema') == 'ci_provenance/1':
                prov[x['moc']['run']['run_id']] = x['moc']['run']
    for m, k, v, chain in walk(du):
        if not (isinstance(k, str) and 'gateoutput' in norm(k) and norm(k) not in PHI): continue
        tok = RE_TOK.match(v.casefold()).group(1) if isinstance(v, str) and RE_TOK.match(v.casefold()) else '<khong_chuoi>'
        neo = None
        if type(m.get('run_id')) is int:
            hk = [x for x in ('sha', 'head_sha', 'merge_commit') if x in m]
            if type(m.get('run_attempt')) is int and len(hk) == 1 and isinstance(m[hk[0]], str) and H40.fullmatch(m[hk[0]]):
                neo = (m['run_id'], m['run_attempt'], m[hk[0]])
        elif MOC <= set(m) and chain:
            cha = chain[-1]; cm = cha.get('ci_master') if isinstance(cha, dict) else None
            if isinstance(cm, dict) and type(cm.get('run_id')) is int and type(cm.get('run_attempt')) is int and isinstance(cha.get('merge_commit'), str):
                neo = (cm['run_id'], cm['run_attempt'], cha['merge_commit'])
        if neo is None:
            dem['thieu_neo'] += 1; continue
        r = prov.get(neo[0]); wf = r['loi_khai_rest_path'] if r else '<khong_prov => ci.yml>'
        ev = r['event'] if r else '?'
        land = neo[2] in H and (r is None or wf == '.github/workflows/ci.yml')
        dem[('land' if land else 'phu', ev)] += 1
        if land and ev != 'push':
            ra.append((gt, 'LANDED' if tep.name in landed else 'BO_QUA', k, tok, neo[0], ev, wf))
        if not land:
            ra.append(('PHU', gt, 'LANDED' if tep.name in landed else 'BO_QUA', k, tok, neo[0], neo[2][:7], 'H=' + ','.join(h[:7] for h in H), ev, wf))
        PHU_HS.setdefault(gt, set()).add(land)
print(dict(dem))
print('ho so landed co neo nhung 0 loi khai land:', sorted(h for h,v in PHU_HS.items() if True not in v and (h+'-land-evidence.yaml') in landed))
for x in ra: print('LOI KHAI LAND KHONG PHAI PUSH:', x)
