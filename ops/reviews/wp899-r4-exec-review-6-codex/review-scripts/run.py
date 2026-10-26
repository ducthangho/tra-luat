import os,sys,json,pathlib,subprocess,hashlib,time
R=pathlib.Path(__file__).resolve().parent
for d in ('tmp','cache'): (R/d).mkdir(exist_ok=True)
label,*cmd=sys.argv[1:]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(R/'tmp'),TMP=str(R/'tmp'),TEMP=str(R/'tmp'),XDG_CACHE_HOME=str(R/'cache'))
t=time.time(); p=subprocess.run(cmd,capture_output=True,env=env)
d={'command':cmd,'returncode':p.returncode,'seconds':time.time()-t}
for k,b in [('stdout',p.stdout),('stderr',p.stderr)]:
 f=R/(label+'.'+k+'.txt'); f.write_bytes(b); d[k]={'path':str(f),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
(R/(label+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2))
print(json.dumps(d,ensure_ascii=False)); print(p.stdout.decode('utf-8','replace')[-3000:]);print(p.stderr.decode('utf-8','replace')[-1000:])
