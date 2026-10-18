import pathlib, subprocess, json, hashlib, sys, shlex, importlib.util
import yaml
K=pathlib.Path('/home/user/rv773'); P=K/'ops/land/pr779-wp775-provenance'
def run(a,cwd=K):
 r=subprocess.run(a,cwd=cwd,text=True,capture_output=True); print('$',shlex.join(a),'rc=',r.returncode); print(r.stdout+r.stderr); return r
s=importlib.util.spec_from_file_location('len','/tmp/len.py'); m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
f=K/'ops/land/pr779-wp775-land-evidence.yaml'; d=m.nap_yaml(yaml,f.read_bytes())
for path,v in m.duyet(d):
 if isinstance(v,str) and m.RE_KHAI_DO.match(v):
  print('CLAIM',path,v)
  for t in m.token_nguon(v):
   p=m.phan_giai(t,K,P,f);print('TOKEN',t,'=>',p)
   if p and p.is_file():
    if p.suffix=='.json':
     x=json.loads(p.read_text());print('SOURCE',json.dumps(x,ensure_ascii=False))
    else: print('SOURCE',p.read_text())
for name in ['cha-d347d42.txt','merge-d8b15cb.txt','spec-wp775.txt','kiem-gate-f9d84d7.txt']:
 print('TRANSCRIPT',name)
 for line in (P/'do-lai-nguon-20261018'/name).read_text().splitlines():
  if not line.startswith('$ '):continue
  a=shlex.split(line[2:])
  if a[0]=='python':
   a[0]='python3.13';a.insert(1,'-B'); a[2]=str(K/a[2]);i=a.index('--check-runs')+1;a[i]=str(P/a[i]);run(a)
  elif a[0]=='sha256sum':run(a)
  elif '|' in a:
   q=a.index('|');r=run(a[:q]);print('SHA256',hashlib.sha256(r.stdout.encode()).hexdigest())
  else:run(a)
run(['git','rev-parse','8e150cf','8e150cf^{tree}','HEAD','HEAD^{tree}','origin/master'])
run(['git','diff','8e150cf','HEAD','--','.claude/dev/packet_loop.py'])
run(['sha256sum','-c','SHA256SUMS'],P)
lines=(P/'SHA256SUMS').read_text().splitlines(); listed=[l.split(maxsplit=1)[1].removeprefix('./') for l in lines];actual={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and p.name!='SHA256SUMS'}
print('FILESET',len(listed),len(actual),'missing',actual-set(listed),'extra',set(listed)-actual,'duplicates',len(listed)-len(set(listed)))
# Additional sources and details not directly included by source tokens.
for n in ['readback-jobs-39053830242.json','readback-run-39053830242.json','readback-review-comments-811.json','readback-comment-6237647158.json','readback-check-runs-f9d84d7.json']+[f'readback-issue-{i}.json' for i in range(804,811)]:
 print('ADDITIONAL',n,(P/n).read_text())
run(['git','status','--porcelain'])
