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
spec=S/'ops/specs/wp1466.md'; b=run(['git','-C',str(S),'show','6c4ffe998954c0801fa69eb68d0406a543eb53f0:ops/specs/wp1466.md'])
assert b==spec.read_bytes()
print('SPEC_BLOB_EQUALS',True,'SHA256',hashlib.sha256(b).hexdigest(),flush=True)
old=run(['git','-C',str(S),'show','05d12f1:ops/specs/wp1466.md'])
(O/'r5-spec.md').write_bytes(old)
(O/'r5-r6.diff').write_bytes(run(['git','-C',str(S),'diff','05d12f1','6c4ffe9','--','ops/specs/wp1466.md']))
src=S/'ops/specs/wp1466/tien-kiem-r6/sc'
for name in ['fx_tien_kiem.py','dot_bien.py','tien_kiem_r5.py']: shutil.copyfile(src/name,O/'sc'/name)
blocks=re.findall(rb'~~~ tien-kiem\n(.*?)\n~~~',b,re.S)
assert len(blocks)==1
tk=blocks[0]+b'\n'; assert tk==(src/'tien_kiem.py').read_bytes()
(O/'sc/tien_kiem.py').write_bytes(tk)
print('TIEN_KIEM_SPEC_EQUALS_SCRIPT',True,flush=True)
shutil.copyfile(S/'ops/specs/wp1466/review/r5-l5/evidence-preflight_extra.py',O/'preflight_extra.py')
for name,ref in [('base','48d372e14f190dae83a75ccbca8ee9a0b25635c5'),('prototype','48d372e14f190dae83a75ccbca8ee9a0b25635c5'),('master','4e56f005785db1b04e043bb71fc694a674a8dc9f')]:
 dest=O/name
 run(['git','clone','--shared','--no-checkout',str(M),str(dest)])
 run(['git','-C',str(dest),'config','core.abbrev','7'])
 run(['git','-C',str(dest),'checkout','--detach',ref])
 if name in ['prototype','master']:
  run(['git','-C',str(dest),'apply','-p1',str(S/'ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch')])
 print('TREE_READY',name,ref,flush=True)
