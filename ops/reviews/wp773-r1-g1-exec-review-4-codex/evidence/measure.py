import subprocess, os, json, tarfile, io, importlib.util, hashlib, contextlib
from pathlib import Path
K=Path('/home/user/rv773'); O=Path(__file__).resolve().parent
os.environ['PYTHONDONTWRITEBYTECODE']='1'
def run(name,args,**kw):
 r=subprocess.run(args,capture_output=True,text=True,**kw); (O/(name+'.log')).write_text(r.stdout+r.stderr); print(name,'rc=',r.returncode,r.stdout[-260:],r.stderr[-160:]); return r
run('tree',['python3.13','-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(K)])
for c in ['c6e2401','1a4c417','d60b9e6']:
 d=Path('/tmp/rv773-r4-history')/c; d.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(['git','-C',str(K),'archive',c,'ops/land'],capture_output=True); print('archive',c,r.returncode)
 with tarfile.open(fileobj=io.BytesIO(r.stdout)) as tf: tf.extractall(d,filter='data')
 run('history-'+c,['python3.13','-B',str(K/'ops/land_evidence_nguon.py'),'--root',str(d),'--tep','ops/land/pr765-wp743-land-evidence.yaml'])
run('ruff',['ruff','check','--no-cache','--select','F',str(K/'ops/land_evidence_nguon.py'),str(K/'ops/land_evidence_nguon_test.py')])
run('diff-check',['git','-C',str(K),'diff','--check','c73af7b','a3cfc53'])
run('stat',['git','-C',str(K),'diff','--numstat','c73af7b','a3cfc53'])
s=importlib.util.spec_from_file_location('validator',K/'ops/land_evidence_nguon.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
m.MIEN_TRU_CUTOVER={}
buf=io.StringIO()
with contextlib.redirect_stdout(buf): rc=m.main(['--root',str(K)])
(O/'no-exemption.log').write_text(buf.getvalue()); print('no-exemption',rc,buf.getvalue()[-240:])
ls=subprocess.check_output(['git','-C',str(K),'ls-tree','--name-only','c73af7b','ops/land/'],text=True).splitlines()
ds={Path(p).name:hashlib.sha256(subprocess.check_output(['git','-C',str(K),'show','c73af7b:'+p])).hexdigest() for p in ls if p.endswith('-land-evidence.yaml')}
print('independent cutover',len(ds),hashlib.sha256(json.dumps(sorted(ds.items())).encode()).hexdigest())
