import itertools, json, os, pathlib, subprocess, sys, tempfile
W=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(W/'author'))
import gram
shells={None:['/usr/bin/bash','-e'],'bash':['/usr/bin/bash','--noprofile','--norc','-eo','pipefail'],'sh':['/bin/sh','-e']}
paths=['x','_x','.x','0','a-b','ops/a-b','.ops/x','./ops/x','ops//x','ops/../x','ops/x..']
args=['',' a',' --json',' a=b : -',' -c -- --help',' ./x ../x a/b c:d -a:b']
out={'single_runs':0,'pipeline_runs':0,'errors':[]}
with tempfile.TemporaryDirectory(dir=W/'tmp') as d:
 p=pathlib.Path(d);(p/'bin').mkdir();(p/'ops').mkdir();os.symlink(sys.executable,p/'bin/python')
 env={'PATH':str(p/'bin')+':/usr/bin:/bin','HOME':d}
 def put(path,fail):
  f=p/path;f.parent.mkdir(parents=True,exist_ok=True)
  if path.endswith('.py'): f.write_text("from pathlib import Path\nimport sys\n"+("Path('DA_CHAY').touch()\nsys.exit(1)\n" if fail else 'sys.stdout.write(sys.stdin.read())\n'))
  else: f.write_text('touch DA_CHAY\nexit 1\n' if fail else 'cat\n')
 def run(body,shell):
  (p/'DA_CHAY').unlink(missing_ok=True)
  (p/'run.sh').write_bytes(body.encode())
  assert (p/'run.sh').read_bytes()==body.encode()
  r=subprocess.run(shells[shell]+[str(p/'run.sh')],cwd=p,env=env,stdin=subprocess.DEVNULL,capture_output=True,timeout=10)
  if not (r.returncode!=0 and (p/'DA_CHAY').exists()):out['errors'].append([body,shell,r.returncode,(p/'DA_CHAY').exists()])
 for path,cmd,arg,shell,lf in itertools.product(paths,('python','bash'),args,shells,('','\n')):
  name=path+('.py' if cmd=='python' else '.sh');put(name,True)
  body=f'{cmd} {name}{arg}{lf}'
  assert gram.cp(body,shell) is None,(body,shell)
  run(body,shell);out['single_runs']+=1
 for commands,fail_at,lf in itertools.product(itertools.product(('python','bash'),repeat=3),range(3),('','\n')):
  parts=[]
  for i,cmd in enumerate(commands):
   name=f'ops/p{i}'+('.py' if cmd=='python' else '.sh');put(name,i==fail_at);parts.append(f'{cmd} {name} --json a=b')
  body=' | '.join(parts)+lf
  assert gram.cp(body,'bash') is None
  assert gram.cp(body,None)=='ong_khong_bash_tuong_minh'
  assert gram.cp(body,'sh')=='ong_khong_bash_tuong_minh'
  run(body,'bash');out['pipeline_runs']+=1
(W/'audit_clean.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False))
assert not out['errors']
