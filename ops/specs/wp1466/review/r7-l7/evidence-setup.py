from pathlib import Path
import os, subprocess, hashlib, json, shutil, datetime, re
R=Path.cwd(); O=R/'out'; S=R/'cay-kho'; M=R/'kho.git'
for d in ['tmp','sc','dot']: (O/d).mkdir(exist_ok=True)
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'),GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='commit.gpgsign',GIT_CONFIG_VALUE_0='false',GIT_OPTIONAL_LOCKS='0')
def run(args,**kw):
 r=subprocess.run(args,capture_output=True,**kw)
 if r.returncode: raise RuntimeError((args,r.returncode,r.stderr[:1000]))
 return r.stdout
def snapshot():
 result={}
 for root in [S,M]:
  for p in sorted(root.rglob('*')):
   if p.is_symlink(): result[str(p.relative_to(R))]=['link',os.readlink(p),p.lstat().st_mtime_ns]
   elif p.is_file(): result[str(p.relative_to(R))]=[hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size,p.stat().st_mtime_ns]
 return result
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
(O/'source-before.json').write_text(json.dumps(snapshot(),ensure_ascii=False))
print('SOURCE_SNAPSHOT_SAVED',flush=True)
b=run(['git','-C',str(S),'show','3c89d87fffbc06a59ad276bb3171e43ef89c2768:ops/specs/wp1466.md'])
assert b==(S/'ops/specs/wp1466.md').read_bytes()
print('SPEC_BLOB_EQUALS',True,'SHA256',hashlib.sha256(b).hexdigest(),flush=True)
old=run(['git','-C',str(S),'show','6c4ffe9:ops/specs/wp1466.md']);(O/'r6-spec.md').write_bytes(old)
blocks=lambda s:dict(re.findall(rb'^~~~ ([^\n]+)\n(.*?)^~~~\s*$',s,re.S|re.M))
x,y=blocks(old),blocks(b)
print('FENCES',len(x),len(y),'CHANGED',[k.decode() for k in x if x[k]!=y[k]],flush=True)
patch='ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch'
print('PATCH_UNCHANGED',run(['git','-C',str(S),'show','6c4ffe9:'+patch])==(S/patch).read_bytes(),'SHA256',hashlib.sha256((S/patch).read_bytes()).hexdigest(),flush=True)
src=S/'ops/specs/wp1466/tien-kiem-r7/sc'
for name in ['fx_tien_kiem.py','fx_r7.py','dot_bien_r7.py','tien_kiem_r5.py','tien_kiem_r6.py']: shutil.copyfile(src/name,O/'sc'/name)
tk=x[b'tien-kiem'];tk=y[b'tien-kiem']
assert tk==(src/'tien_kiem.py').read_bytes()
(O/'sc/tien_kiem.py').write_bytes(tk)
print('TIEN_KIEM_SPEC_EQUALS_SCRIPT',True,'NONEMPTY',sum(bool(l.strip()) for l in tk.splitlines()),flush=True)
rv=S/'ops/specs/wp1466/review/r6-l6'
for name in ['hunt','followup','regression','independent','counts','measure','final_check']:
 shutil.copyfile(rv/('evidence-'+name+'.py'),O/(name+'.py'))
for name,ref in [('base','48d372e14f190dae83a75ccbca8ee9a0b25635c5'),('prototype','48d372e14f190dae83a75ccbca8ee9a0b25635c5'),('master','4e56f005785db1b04e043bb71fc694a674a8dc9f')]:
 dest=O/name
 run(['git','clone','--shared','--no-checkout',str(M),str(dest)])
 run(['git','-C',str(dest),'config','core.abbrev','7'])
 run(['git','-C',str(dest),'checkout','--detach',ref])
 if name in ['prototype','master']: run(['git','-C',str(dest),'apply','-p1',str(S/patch)])
 print('TREE_READY',name,ref,flush=True)
print('PYTHON',run(['/usr/bin/python3','-I','-c','import sys,yaml,site;print(sys.version);print(yaml.__file__);print(site.getsitepackages())']).decode(),flush=True)
