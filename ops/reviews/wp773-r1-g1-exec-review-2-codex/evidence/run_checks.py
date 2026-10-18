import os, subprocess, pathlib, importlib.util, json, hashlib, tempfile
out=pathlib.Path.cwd()/'evidence'
k=pathlib.Path('/home/user/rv773'); sp=pathlib.Path.cwd().parent

def run(name,args,env=None):
 r=subprocess.run(args,capture_output=True,text=True,env=env)
 (out/(name+'.log')).write_text('COMMAND: '+repr(args)+'\nRC: '+str(r.returncode)+'\n'+r.stdout+r.stderr)
 print(name,r.returncode,r.stdout[-350:],flush=True)
 return r
for v in ['3.11','3.12','3.13','3.14']:
 e=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(sp/('yaml-python'+v)))
 run('test-'+v,['python'+v,'-B',str(k/'ops/land_evidence_nguon_test.py')],e)
run('tree',['python3.13','-B',str(k/'ops/land_evidence_nguon.py'),'--root',str(k)])
for c in ['c6e2401','1a4c417','d60b9e6']:
 d=pathlib.Path(tempfile.mkdtemp(prefix='rv773-'+c))
 a=subprocess.run(['git','-C',str(k),'archive',c,'ops/land'],capture_output=True)
 r=subprocess.run(['tar','-x','-C',str(d)],input=a.stdout,capture_output=True)
 print('archive',c,a.returncode,r.returncode)
 run('history-'+c,['python3.13','-B',str(k/'ops/land_evidence_nguon.py'),'--root',str(d),'--tep','ops/land/pr765-wp743-land-evidence.yaml'])
run('ruff',['ruff','check','--no-cache','--select','F',str(k/'ops/land_evidence_nguon.py'),str(k/'ops/land_evidence_nguon_test.py')])
run('diff-check',['git','-C',str(k),'diff','--check','c73af7b','bf5993a'])
