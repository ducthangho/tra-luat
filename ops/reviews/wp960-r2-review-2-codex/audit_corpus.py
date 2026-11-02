"""Offline corpus and debt audit at the pinned review snapshot."""
import collections
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import yaml

ROOT=Path('/tmp/wp960-r2-l2-copy')
BASE=Path('/tmp/wp960-r2-l2-base')
sp=importlib.util.spec_from_file_location('review_gate', ROOT/'ops/bien_nhan_v2.py')
b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
receipts={p.name:(yaml.safe_load(p.read_text(encoding='utf-8')),p.read_text(encoding='utf-8'))
          for p in sorted((ROOT/'ops/reviews').glob('*.receipt.yaml'))}

def git(root,*a):
    p=subprocess.run(['git','-C',str(root),*a],capture_output=True,text=True)
    return p.returncode,p.stdout.strip(),p.stderr.strip()

def walk(v,path=''):
    if isinstance(v,dict):
        for k,x in v.items():
            yield from walk(x,f'{path}.{k}' if path else str(k))
    elif isinstance(v,list):
        for i,x in enumerate(v):yield from walk(x,f'{path}[{i}]')
    elif isinstance(v,str):yield path,v

md=git(BASE,'rev-parse','refs/remotes/origin/master')[1]
debt=[]
for name,field,law in sorted(b.NO_CAU_LICH_SU):
    d,_=receipts[name]
    text=dict(walk(d))[field]
    proof=[]
    for sentence in b._cac_cau(text):
        if law==b.LUAT_ANCESTRY and b._RE_ANCESTRY.search(b._bo_dau(sentence)):
            for match in b._RE_OID.finditer(sentence):
                oid=match.group()
                rc,commit,err=git(BASE,'rev-parse','--verify','--quiet',oid+'^{commit}')
                if rc==0:
                    rc2,_,err2=git(BASE,'merge-base','--is-ancestor',commit,md)
                    proof.append({'oid':oid,'commit':commit,'is_ancestor_rc':rc2})
        elif law==b.LUAT_REVIEW and b._RE_CHUA_REVIEW.search(b._bo_dau(sentence)):
            for oid in re.findall(r'(?<![A-Za-z0-9_])[0-9a-f]{40}(?![A-Za-z0-9_])',sentence):
                later=[(n,x.get('luot')) for n,(x,_) in receipts.items() if isinstance(x,dict)
                       and n!=name and x.get('reviewed_sha')==oid and isinstance(x.get('luot'),int)
                       and x['luot']>d['luot']]
                if later:proof.append({'oid':oid,'current_round':d['luot'],'later':later})
    ok=any(x.get('is_ancestor_rc')==0 or x.get('later') for x in proof)
    debt.append({'key':[name,field,law],'text':text,'proof':proof,'verified':ok})

tokens=[]
for name,(d,raw) in receipts.items():
    if not isinstance(d,dict):continue
    for field,text in walk(d):
        for sentence in b._cac_cau(text):
            if not b._RE_ANCESTRY.search(b._bo_dau(sentence)):continue
            for m in b._RE_OID.finditer(sentence):
                oid=m.group()
                rc,c,err=git(ROOT,'rev-parse','--verify','--quiet',oid+'^{commit}')
                tokens.append({'receipt':name,'field':field,'sentence':sentence,'token':oid,'commit':c if rc==0 else None,
                               'mandatory':b._oid_bat_buoc(sentence,m)})

surfaces=[]
vocab=frozenset().union(*(v['be_mat'] for v in b.PROVIDER_HOP_DONG.values()))
for name,(d,_) in receipts.items():
    if not isinstance(d,dict):continue
    mri=d.get('model_reviewer_identity') or {}
    if not isinstance(mri,dict) or not mri.get('run_json'):continue
    rj=ROOT/mri['run_json']
    vp=ROOT/d['verdict_path']
    if not rj.is_file():
        surfaces.append({'receipt':name,'run_json':str(rj.relative_to(ROOT)),'missing':True});continue
    actual=json.loads(rj.read_text(encoding='utf-8'))['execution_surface']
    lines=vp.read_text(encoding='utf-8').splitlines()
    selected=[]; rejected=[]
    for i,line in enumerate(lines):
        if not re.search(r'execution[_ ]surface',line,re.I):continue
        window=lines[max(0,i-1):i+2]
        provider=any(re.search(r'\bprovider\b',x,re.I) for x in window)
        quote=any(re.search(r'[\w./-]+\.[A-Za-z0-9]+:\d+',x) for x in window)
        entry={'line':i+1,'text':line,'window':window,'provider':provider,'quote':quote}
        (selected if provider and not quote else rejected).append(entry)
    mismatches=sorted(b._surface_cua_verdict(ROOT,d,actual,vocab))
    caveat=any(x.get('id')==b.CAVEAT_SURFACE for x in d.get('verdict_usage_caveats',[]) if isinstance(x,dict))
    surfaces.append({'receipt':name,'verdict':d['verdict_path'],'actual':actual,'selected':selected,
                     'rejected':rejected,'mismatches':mismatches,'caveat':caveat})

result={'root_sha':git(ROOT,'rev-parse','HEAD')[1],'base_sha':git(BASE,'rev-parse','HEAD')[1],
        'default_base':md,'receipts':len(receipts),'debt':debt,'tokens':tokens,'surfaces':surfaces}
Path('evidence/corpus.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('receipts',len(receipts),'debt',len(debt),'verified',sum(x['verified'] for x in debt),
      'law_counts',dict(collections.Counter(x['key'][2] for x in debt)))
print('default_base',md)
print('tokens',len(tokens),'resolved',sum(x['commit'] is not None for x in tokens))
print('unresolved',json.dumps([x for x in tokens if not x['commit']],ensure_ascii=False))
print('run_json_receipts',len(surfaces),'selected_verdicts',sum(bool(x.get('selected')) for x in surfaces),
      'selected_lines',sum(len(x.get('selected',[])) for x in surfaces),
      'mismatch_verdicts',sum(bool(x.get('mismatches')) for x in surfaces))
for row in surfaces:
    print('SURFACE',json.dumps({k:v for k,v in row.items() if k!='rejected'},ensure_ascii=False))
for root,label in ((ROOT,'head'),(BASE,'base-data-with-head-gate')):
    for no,label_no in ((None,'debt'),(frozenset(),'empty')):
        errors,stats=b.kiem(root,no_cau_lich_su=no,nhanh_mac_dinh=md)
        print(label,label_no,json.dumps({'rc':b._ma_thoat(errors,stats),'errors':len(errors),
                    'law_errors':sum(x.startswith('[L-') for x in errors),'unknown':len(stats.get('chua_do',[])),
                    'debt':stats.get('no_cau')},ensure_ascii=False))
