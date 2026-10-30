"""Mutations of existing Git fixtures: object errors, ambiguity, shallow/partial repos, full corpus comparison."""
import collections
import hashlib
import importlib.util
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import replay_r2_recheck as p

t,b,ROOT=p.t,p.b,p.ROOT

def git(root,*args,data=None):
 q=subprocess.run(['git','-C',str(root),*args],input=data,capture_output=True,text=True)
 return dict(rc=q.returncode,stdout=q.stdout.strip(),stderr=q.stderr.strip())

def measure(label,root,tok,**kw):
 try:resolved=b._commit_cua(root,tok);fail=None
 except Exception as ex:resolved=None;fail=type(ex).__name__+': '+str(ex)
 p.emit(label,token=tok,disambiguate=git(root,'rev-parse','--disambiguate='+tok),peel=git(root,'rev-parse','--verify','--quiet',tok+'^{commit}'),resolved=resolved,failure=fail,**kw)

def objects():
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);k=t._kho_cau(root)
  pure=t._commit_tien_to_so(root,k,str.isalpha,'chu',30000)
  k['g']('merge','-q','--no-ff',pure,'-m','merge')
  al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: Ban {pure[:7]} chua vao master.\n')})
  measure('object-control',root,pure[:7],cli=p.run(root,al))
  obj=root/'.git/objects'/pure[:2]/pure[2:];saved=obj.read_bytes()
  for kind,data in [('zero',b''),('zlib',b'not-zlib')]:
   obj.unlink();obj.write_bytes(data)
   measure('object-corrupt-'+kind,root,pure[:7],cli=p.run(root,al))
   measure('object-corrupt-'+kind+'-with-debt',root,pure[:7],cli=p.run(root,al,[("r.receipt.yaml","anchor.mo_ta",b.LUAT_ANCESTRY)]))
  obj.write_bytes(saved)
  # Simulate a local partial clone: an advertised promised object is unavailable; empty URL prevents network.
  k['g']('config','remote.local.promisor','true');k['g']('config','remote.local.url',str(root/'nonexistent-offline-remote'))
  k['g']('config','extensions.partialClone','local')
  obj.unlink()
  measure('object-partial-missing',root,pure[:7],cli=p.run(root,al))
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);k=t._kho_cau(root)
  tt=t._commit_trung_tien_to(root,k)
  measure('two-commits',root,tt)
  (root/'.git/shallow').write_text(k['M']+'\n')
  measure('two-commits-shallow',root,tt)
  # A shallow boundary cannot prove ancestry beyond the boundary; Git returns ordinary 1.
  al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: Commit {k["B0"][:7]} chua vao master.\n')})
  p.emit('shallow-ancestry',is_shallow=git(root,'rev-parse','--is-shallow-repository'),relation=git(root,'merge-base','--is-ancestor',k['B0'],'master'),cli=p.run(root,al))

def collisions():
 with tempfile.TemporaryDirectory() as tmp:
  root=Path(tmp);k=t._kho_cau(root);tree=k['g']('rev-parse','HEAD^{tree}')
  def oid(typ,data):return hashlib.sha1((typ+' '+str(len(data))+'\0').encode()+data).hexdigest()
  def commit(i):return (f'tree {tree}\nparent {k["B0"]}\nauthor t <t@t> 1767225600 +0000\ncommitter t <t@t> 1767225600 +0000\n\ncollision-{i}\n').encode()
  commits={oid('commit',commit(i))[:7]:i for i in range(50000)}
  for kind in ('blob','tag-commit','tag-blob'):
   for i in range(500000):
    if kind=='blob':typ='blob';raw=f'collision-blob-{i}\n'.encode()
    else:
     typ='tag';target=k['B0'] if kind=='tag-commit' else k['g']('rev-parse','HEAD:a.txt') if i==0 else blob_target
     blob_target=target
     raw=(f'object {target}\ntype '+('commit' if kind=='tag-commit' else 'blob')+f'\ntag test-{i}\ntagger t <t@t> 1767225600 +0000\n\ncollision-{i}\n').encode()
    h=oid(typ,raw);j=commits.get(h[:7])
    if j is not None:break
   else:raise RuntimeError('no collision')
   c=commit(j)
   sha=git(root,'hash-object','-w','-t','commit','--stdin',data=c.decode())['stdout']
   other=git(root,'hash-object','-w','-t',typ,'--stdin',data=raw.decode())['stdout']
   k['g']('update-ref','refs/remotes/origin/master',sha)
   al=t._ghi_bn_cau(root,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: Commit {sha[:7]} chua vao master.\n')})
   measure('collision-'+kind,root,sha[:7],commit=sha,other=other,other_type=typ,cli=p.run(root,al))

def compare():
 data=json.load(open('evidence/corpus.json'))
 tokens=sorted(set(x['token'] for x in data['tokens']))
 rows=[]
 for tok in tokens:
  old=git(ROOT,'rev-parse','--verify','--quiet',tok+'^{commit}')
  try:new=b._commit_cua(ROOT,tok);fail=None
  except Exception as ex:new=None;fail=type(ex).__name__+': '+str(ex)
  rows.append(dict(token=tok,old=old['stdout'] if old['rc']==0 else None,new=new,error=fail))
 p.emit('corpus-oid-compare',occurrences=len(data['tokens']),unique=len(tokens),changed=[r for r in rows if r['old']!=r['new'] or r['error']])
 # Same exact-head corpus/ref/checkout; only resolver changes for A/B cost.
 def previous(root,x):
  rc,out=b._git(root,'rev-parse','--verify','--quiet',x+'^{commit}')
  return out if rc==0 and b._HEX40.match(out) else None
 real=b._commit_cua
 times={'previous':[],'head':[]};counts={}
 for j in range(3):
  for label,fn in [('previous',previous),('head',real)]:
   calls=[0];oldgit=b._git
   def counter(*a,**kw):calls[0]+=1;return oldgit(*a,**kw)
   b._git=counter;b._commit_cua=fn
   try:
    start=time.perf_counter();errors,stats=b.kiem(ROOT);elapsed=time.perf_counter()-start
   finally:b._git=oldgit;b._commit_cua=real
   times[label].append(elapsed);counts[label]=calls[0]
   p.emit('benchmark-run',label_run=label,index=j,seconds=round(elapsed,4),git_calls=calls[0],rc=b._ma_thoat(errors,stats))
 p.emit('benchmark-summary',seconds=times,median={k:statistics.median(v) for k,v in times.items()},git_calls=counts)

def partial():
 with tempfile.TemporaryDirectory() as tmp:
  source=Path(tmp)/'source';source.mkdir();k=t._kho_cau(source)
  tt=t._commit_trung_tien_to(source,k)
  two=k['g']('rev-parse','--disambiguate='+tt).split()
  for i,sha in enumerate(two):k['g']('update-ref',f'refs/heads/collision-{i}',sha)
  k['g']('config','uploadpack.allowFilter','true')
  target=Path(tmp)/'partial'
  q=subprocess.run(['git','clone','--quiet','--no-checkout','--filter=blob:none','--no-local',source.as_uri(),str(target)],capture_output=True,text=True)
  if q.returncode:raise RuntimeError(q.stderr)
  missing=git(target,'rev-list','--objects','--all','--missing=print')
  p.emit('partial-clone-identity',transport='file:// local',clone_rc=q.returncode,clone_stderr=q.stderr.strip(),promisor=git(target,'config','--get','remote.origin.promisor'),filter=git(target,'config','--get','remote.origin.partialclonefilter'),promisor_packs=len(list((target/'.git/objects/pack').glob('*.promisor'))),missing_objects=[x for x in missing['stdout'].splitlines() if x.startswith('?')])
  measure('partial-clone-ambiguous',target,tt)
  measure('partial-clone-known',target,k['M'][:7])

if __name__=='__main__':globals()[sys.argv[1]]()
