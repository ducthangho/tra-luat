import sys, os, subprocess, pathlib, tempfile, importlib.util, itertools, json, hashlib, tarfile, io
sys.dont_write_bytecode=True
K=pathlib.Path('/home/user/rv773'); OUT=pathlib.Path(__file__).resolve().parent
T=K/'ops/land_evidence_nguon_test.py'; M=K/'ops/land_evidence_nguon.py'
def run(args,name,env=None):
 r=subprocess.run([str(x) for x in args],capture_output=True,text=True,env=env)
 (OUT/(name+'.log')).write_text(f'argv={args!r}\nrc={r.returncode}\n'+r.stdout+r.stderr)
 print(name,'rc=',r.returncode, (r.stdout+r.stderr)[-270:].replace('\n',' | '));return r
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=load(T,'tests'); src=M.read_text(); case=next(c for c in t.CA if c.startswith('c05'))
with tempfile.TemporaryDirectory(prefix='rv773-r7-') as tmp:
 tmp=pathlib.Path(tmp)
 for i,p in enumerate(itertools.permutations(['prov','goc / THU_MUC','goc'])):
  if p==('prov','goc / THU_MUC','goc'):continue
  dest=tmp/f'perm{i}.py';dest.write_text(src.replace('for nen in (prov, goc / THU_MUC, goc):','for nen in ('+', '.join(p)+'):'))
  r=run([sys.executable,'-B',T,'--mot-ca',case],f'perm{i}',dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(dest)))
  assert r.returncode==3 and f'DO:{case}:' in r.stdout
 for c in ['c6e2401','1a4c417','d60b9e6']:
  dest=tmp/c;dest.mkdir();r=subprocess.run(['git','-C',str(K),'archive',c,'ops/land'],capture_output=True);assert r.returncode==0
  with tarfile.open(fileobj=io.BytesIO(r.stdout)) as tar:tar.extractall(dest,filter='data')
  run([sys.executable,'-B',M,'--root',dest,'--tep','ops/land/pr765-wp743-land-evidence.yaml'],'history-'+c)
 # probes are ordinary fixture values, no new escape tokens
 probes=[('duplicate',"x: 'measured - missing'\nx: ok\n",{'a.txt':''}),
 ('positive-number',"positive: 123\nnguon_positive: a.txt\n",{'a.txt':'metadata'}),
 ('source-number',"positive: '1/1'\nnguon_positive: 123\n",{'a.txt':'1/1'}),
 ('mapping-time',"pre_merge_checks: {'2026-10-16T03:00:00Z': ok}\n",{'readback-pr-9001.json':t.RB_PR}),
 ('fraction-time',"pre_merge_checks: ['2026-10-16T02:58:26.1Z']\n",{'readback-pr-9001.json':t.RB_PR}),
 ('offset-time',"pre_merge_checks: ['2026-10-16T03:00:00+00:00']\n",{'readback-pr-9001.json':t.RB_PR}),
 ('glob',"x: 'measured - *.txt'\n",{'a.txt':'ok'}),
 ('directory',"x: 'measured - logs/'\n",{'logs/a.txt':'ok'})]
 for name,hs,p in probes:
  with t.cay(hs,p) as root:run([sys.executable,'-B',M,'--root',root],'probe-'+name)
 with t.cay("x: 'measured - link.txt'\n",{'a.txt':'ok'}) as root:
  (root/'ops/land'/t.PROV/'link.txt').symlink_to('a.txt');run([sys.executable,'-B',M,'--root',root],'probe-symlink-internal')
 for label,old,new,caseprefix in [('rename','plat-x8-land-evidence.yaml','plat-x9-land-evidence.yaml','c10'),('skip-numbers','if not any(mau.search(nd) for nd in noi_dung):','if False:','c05')]:
  dest=tmp/(label+'.py');assert src.count(old)==1;dest.write_text(src.replace(old,new));ca=next(c for c in t.CA if c.startswith(caseprefix))
  run([sys.executable,'-B',T,'--mot-ca',ca],'mutation-'+label,dict(os.environ,LAND_EVIDENCE_NGUON_MA=str(dest)))
run([sys.executable,'-B',M,'--root',K],'tree')
m=load(M,'validator');m.MIEN_TRU_CUTOVER={}
import contextlib
with (OUT/'no-exemption.log').open('w') as f,contextlib.redirect_stdout(f):rc=m.main(['--root',str(K)])
print('no-exemption rc=',rc)
names=subprocess.check_output(['git','-C',str(K),'ls-tree','-r','--name-only','c73af7b','ops/land'],text=True).splitlines();ds={pathlib.Path(n).name:hashlib.sha256(subprocess.check_output(['git','-C',str(K),'show','c73af7b:'+n])).hexdigest() for n in names if n.endswith('-land-evidence.yaml')}
print('independent cutover',len(ds),hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest())
