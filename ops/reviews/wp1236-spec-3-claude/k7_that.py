import sys, re, yaml, importlib.util, subprocess, collections
from pathlib import Path
def nap(ten, p):
    s=importlib.util.spec_from_file_location(ten,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
cp=nap('cp','ops/ci_provenance.py')
dg=nap('dg','ops/land/pr1231-wp1105-provenance/danh_gia_gate.py')
commit=sys.argv[1]; provf=sys.argv[2]
wf=cp.doc_wf(subprocess.run(['git','show',f'{commit}:.github/workflows/ci.yml'],capture_output=True,text=True).stdout)
prov=yaml.safe_load(open(provf,encoding='utf-8'))
tong=collections.Counter()
for j in prov['moc']['gate_output']['jobs']:
    if j['conclusion']=='skipped': continue
    k=cp.ghep_job(j['name'],wf)
    luat=[b for tt,b in dg.LUAT if j['name'].startswith(tt)]
    if not luat: print('KHONG LUAT', j['name']); continue
    steps=wf['jobs'][k]['steps']
    names=[cp.ten_du_kien(s) for s in steps]
    bn=[b['name'] for b in j['buoc']]
    for nhan,pats in luat[0]:
        if nhan==dg.TL_SELFTEST:
            idx=[i for i,s in enumerate(steps) if 'tl.py --selftest' in str(s.get('run',''))]
        else:
            idx=[i for i,s in enumerate(steps) if nhan in str(s.get('run',''))]
        for i in idx:
            s=steps[i]; n=names[i]; run=str(s.get('run',''))
            coe=s.get('continue-on-error'); ch=cp.chan_buoc(wf,k,i)
            ong='|' in run; pf=bool(re.search(r'^\s*set -[a-z]*o pipefail|set -o pipefail|set -euo pipefail',run,re.M)) or 'pipefail' in str(s.get('shell',''))
            sete = 'set +e' in run
            dup=names.count(n); dupr=bn.count(n)
            st=[b for b in j['buoc'] if b['name']==n]
            flag=[]
            if coe not in (None,False): flag.append('COE')
            if ch: flag.append('CHAN')
            if ong and not pf: flag.append('ONG_KHONG_PF')
            if dup!=1 or dupr!=1: flag.append(f'TRUNG{dup}/{dupr}')
            if not st or st[0]['conclusion']!='success': flag.append('BUOC_REST_KHONG_SUCCESS')
            if sete: flag.append('SET+E')
            tong['buoc']+=1
            for f in flag: tong[f]+=1
            if j['name'].endswith(', 0)') or ',' not in j['name']:
                print(f"{j['name'][:34]:34} | {nhan[:40]:40} | {n!r:48} | sh={s.get('shell')} | {flag}")
        if not idx: print('KHONG TIM THAY BUOC', j['name'], nhan); tong['khong_thay']+=1
print(dict(tong))
