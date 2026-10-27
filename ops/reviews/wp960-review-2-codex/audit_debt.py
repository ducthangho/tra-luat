#!/usr/bin/env python3
"""Đọc độc lập tuple nợ: không dùng bộ chọn/scalar/mốc của cổng để xác minh bằng chứng Git."""
from pathlib import Path
import importlib.util,json,re,subprocess,unicodedata
import yaml
ROOT=Path('/tmp/wp960-r2-Dt2G8H/repo')
s=importlib.util.spec_from_file_location('b',ROOT/'ops/bien_nhan_v2.py');b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
def git(*a):
 r=subprocess.run(['git','-C',str(ROOT),*a],capture_output=True,text=True);return r.returncode,r.stdout.strip()
def scalars(x,path='',parents=()):
 if isinstance(x,dict):
  for k,v in x.items():yield from scalars(v,path+'.'+str(k) if path else str(k),parents+(x,))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from scalars(v,f'{path}[{i}]',parents)
 elif isinstance(x,str):yield path,x,(parents[-1] if parents else {})
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower().replace('đ','d')) if unicodedata.category(c)!='Mn')
def emit(name,**kw):print(name,json.dumps(kw,ensure_ascii=False),flush=True)
docs={p.name:yaml.safe_load(p.read_text()) for p in (ROOT/'ops/reviews').glob('*.receipt.yaml')}
counts={};problems=[]
for file,field,law in sorted(b.NO_CAU_LICH_SU):
 d=docs[file]; fields={p:(text,parent) for p,text,parent in scalars(d)};text,parent=fields[field];moc=parent.get('dung_tai')
 if law=='L-ANCESTRY':
  parts=re.split(r'(?<=[.;!?])\s+',' '.join(text.split()))
  relevant=[p for p in parts if any(x in norm(p) for x in ['nhanh','to tien','master','canonical inclusion','ancestor'])]
  evidence=[]
  for line in relevant:
   ids=[]
   for token in re.findall(r'(?<![A-Za-z0-9_])[0-9a-f]{7,40}(?![A-Za-z0-9_])',line):
    rc,oid=git('rev-parse','--verify','--quiet',token+'^{commit}')
    if rc==0:ids.append({'token':token,'oid':oid,'ancestor_rc':git('merge-base','--is-ancestor',oid,'refs/remotes/origin/master')[0]})
   if ids:evidence.append({'sentence':line,'git':ids})
  good=bool(evidence) and any(i['ancestor_rc']==0 for e in evidence for i in e['git']) and not moc
  if not good:problems.append((file,field,law))
  emit('audit-ancestry',file=file,field=field,structured_anchor=moc,confirmed=good,evidence=evidence)
 elif law=='L-REVIEW':
  ids=re.findall(r'(?<![A-Za-z0-9_])[0-9a-f]{40}(?![A-Za-z0-9_])',text)
  later=[{'file':f,'luot':v.get('luot'),'sha':v.get('reviewed_sha')} for f,v in docs.items() if isinstance(v,dict) and f!=file and v.get('reviewed_sha') in ids and isinstance(v.get('luot'),int) and v['luot']>d['luot']]
  good=bool(later) and not moc
  if not good:problems.append((file,field,law))
  emit('audit-review',file=file,field=field,sentence=text,luot=d['luot'],later=later,confirmed=good)
 else:
  rj=d['model_reviewer_identity']['run_json'];surface=json.loads((ROOT/rj).read_text())['execution_surface'];vp=d['verdict_path']
  lines=[(i,x) for i,x in enumerate((ROOT/vp).read_text().splitlines(),1) if re.search('execution[_ ]surface',x,re.I) and 'codex_service' in x]
  caveats=[v.get('id') for v in d.get('verdict_usage_caveats',[]) if isinstance(v,dict)]
  good=surface=='codex_cli' and bool(lines) and 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' not in caveats
  if not good:problems.append((file,field,law))
  emit('audit-surface',file=file,run_json=rj,run_surface=surface,verdict=vp,codex_service_lines=lines,caveat_ids=caveats,syntax_match=good)
 counts[law]=counts.get(law,0)+1
emit('audit-summary',counts=counts,unconfirmed_syntactic=problems,surface_semantics='requires context; see probe-debt-surface.log')
