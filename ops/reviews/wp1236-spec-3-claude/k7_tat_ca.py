import re, yaml, importlib.util, subprocess, collections
from pathlib import Path
def nap(ten,p):
    s=importlib.util.spec_from_file_location(ten,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
cp=nap('cp','ops/ci_provenance.py'); dg=nap('dg','ops/land/pr1231-wp1105-provenance/danh_gia_gate.py')
files=[]
for p in Path('ops/land').rglob('*.yaml'):
    try: x=yaml.safe_load(p.read_text(encoding='utf-8'))
    except Exception: continue
    if isinstance(x,dict) and x.get('schema')=='ci_provenance/1': files.append((p,x))
tong=collections.Counter(); gb=collections.Counter()
for p,x in sorted(files):
    r=x['moc']['run']; head=r['head_sha']; path=r.get('loi_khai_rest_path')
    van=subprocess.run(['git','show',f'{head}:{path}'],capture_output=True,text=True)
    wf=cp.doc_wf(van.stdout) if van.returncode==0 else None
    if wf is None: print(p.parent.parent.name, r['event'], 'KHONG DOC WF'); tong['khong_wf']+=1; continue
    bi=collections.Counter(); J=0
    for j in x['moc']['gate_output']['jobs']:
        g=j.get('ghep_buoc'); gb[(g or {}).get('trang_thai') if j['conclusion']!='skipped' else 'skip']+=1
        if j['conclusion']=='skipped' or j['name'].startswith('chuan-bi'): continue
        J+=1
        k=cp.ghep_job(j['name'],wf)
        luat=[b for tt,b in dg.LUAT if j['name'].startswith(tt)]
        if k is None or not luat: bi['khong_luat_hoac_job']+=1; continue
        steps=wf['jobs'][k]['steps']; chan=False
        for nhan,_ in luat[0]:
            idx=[i for i,s in enumerate(steps) if ('tl.py --selftest' if nhan==dg.TL_SELFTEST else nhan) in str(s.get('run',''))]
            for i in idx:
                n=cp.ten_du_kien(steps[i]); st=[b for b in j['buoc'] if isinstance(j['buoc'],list) and b['name']==n]
                if not st or st[0]['conclusion']!='success': continue  # buoc bi bo qua (if:) - khong xet
                if cp.chan_buoc(wf,k,i) or steps[i].get('continue-on-error') not in (None,False): chan=True
        if chan: bi['chan']+=1
    ok = not bi
    tong['run_dat_K7' if ok else 'run_truot_K7']+=1
    print(f"{str(p)[9:70]:62} {r['event']:12} J={J:2} {dict(bi)}")
print(dict(tong)); print('ghep_buoc', dict(gb))
