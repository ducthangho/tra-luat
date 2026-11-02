import os, pathlib, subprocess, concurrent.futures, tarfile, io
K='/home/user/rv773'; SP=str(pathlib.Path.cwd().parent); E=pathlib.Path('evidence')
def run(name,cmd,env=None):
 r=subprocess.run(cmd,capture_output=True,text=True,env=env)
 (E/(name+'.log')).write_text('COMMAND: '+repr(cmd)+'\nRC: '+str(r.returncode)+'\n'+r.stdout+r.stderr)
 return name,r.returncode,(r.stdout+r.stderr)[-450:]
def test(v):
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=f'{SP}/yaml-python{v}')
 return run('test-'+v,['python'+v,'-B',K+'/ops/land_evidence_nguon_test.py'],env)
with concurrent.futures.ThreadPoolExecutor(4) as p:
 for r in p.map(test,['3.11','3.12','3.13','3.14']): print(r)
print(run('tree',['python3.13','-B',K+'/ops/land_evidence_nguon.py','--root',K]))
for c in ['c6e2401','1a4c417','d60b9e6']:
 d=pathlib.Path('/tmp/rv773-r3-history')/c; d.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(['git','-C',K,'archive',c,'ops/land'],capture_output=True); assert r.returncode==0
 with tarfile.open(fileobj=io.BytesIO(r.stdout)) as a: a.extractall(d,filter='data')
 print(run('history-'+c,['python3.13','-B',K+'/ops/land_evidence_nguon.py','--root',str(d),'--tep','ops/land/pr765-wp743-land-evidence.yaml']))
for name,args in [('ruff',['ruff','check','--no-cache','--select','F',K+'/ops/land_evidence_nguon.py',K+'/ops/land_evidence_nguon_test.py']),('diff-check',['git','-C',K,'diff','--check','c73af7b','5250883']),('diff',['git','-C',K,'diff','c73af7b','5250883']),('stat',['git','-C',K,'diff','--numstat','c73af7b','5250883'])]:
 print(run(name,args) if name!='diff' else run(name,args)[:2])
