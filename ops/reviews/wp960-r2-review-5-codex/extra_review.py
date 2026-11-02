import importlib.util,subprocess,sys,os,shutil,tempfile,json
from pathlib import Path
import replay_probe_recheck as h
b,t=h.b,h.t

def closure():
 for target in ('old-health-rc3','new-health-rc3-valid-stdout','new-health-stderr','old-health-stderr'):
  with tempfile.TemporaryDirectory(prefix='r5-closure-') as d:
   base=Path(d);p=base/'repo';p.mkdir();k,sha,al=h.anc(p);bin_=base/'bin';bin_.mkdir();real=shutil.which('git')
   args=['rev-parse','--git-dir'] if target.startswith('old-') else ['rev-parse','--is-shallow-repository']
   script='#!/usr/bin/env python3\nimport sys,subprocess\na=sys.argv[1:]\n'
   script+=f'if a[-2:]=={args!r}:\n'
   script+=(' print("false")\n sys.exit(3)\n' if 'rc3' in target else ' print("error: probe cannot inspect repository state", file=sys.stderr)\n')
   script+=f'sys.exit(subprocess.run([{real!r},*a]).returncode)\n'
   (bin_/'git').write_text(script);(bin_/'git').chmod(0o755)
   for debt in ((),(h.KEY,)):h.log(direction=target,debt=bool(debt),result=h.raw(p,al,debt,env={'PATH':str(bin_)+os.pathsep+os.environ['PATH']}))
 with tempfile.TemporaryDirectory(prefix='r5-stale-') as d:
  p=Path(d);k,sha,al=h.anc(p)
  r1=t._chay_cli(p,al);k['g']('config','core.fsyncObjectFiles','true');r2=t._chay_cli(p,al);k['g']('config','--unset','core.fsyncObjectFiles');r3=t._chay_cli(p,al)
  h.log(direction='refresh-1-2-1',results=[r1,r2,r3],foreign_gitdir=h.raw(p,al,env={'GIT_DIR':str(p/'absent.git')}))

def allowlist():
 with tempfile.TemporaryDirectory(prefix='r5-allow-') as d:
  base=Path(d);p=base/'repo';p.mkdir();k,sha,al=h.anc(p)
  exe=base/'fake-exec';exe.mkdir();mark=base/'called'
  for cmd in ('rev-parse','config','cat-file','for-each-ref','symbolic-ref','merge-base'):
   f=exe/('git-'+cmd);f.write_text('#!/bin/sh\nprintf "called\\n" >> '+str(mark)+'\nexit 1\n');f.chmod(0o755)
  for debt in ((),(h.KEY,)):h.log(direction='exec-path-fake-builtins',debt=bool(debt),result=h.raw(p,al,debt,env={'GIT_EXEC_PATH':str(exe)}),fake_called=mark.exists())
  pool=base/'pool';shutil.move(p/'.git/objects',pool);(p/'.git/objects/info').mkdir(parents=True)
  h.log(direction='alternates-env',fsck=h.git(p,'fsck','--full',env={'GIT_ALTERNATE_OBJECT_DIRECTORIES':str(pool)}),gate=h.raw(p,al,env={'GIT_ALTERNATE_OBJECT_DIRECTORIES':str(pool)}))
  (p/'.git/objects/info/alternates').write_text(str(pool)+'\n');h.log(direction='alternates-file',fsck=h.git(p,'fsck','--full'),gate=h.raw(p,al));(p/'.git/objects/info/alternates').unlink()
 with tempfile.TemporaryDirectory(prefix='r5-foreign-pool-') as d:
  base=Path(d);p=base/'repo';p.mkdir();k=t._kho_cau(p)
  foreign=base/'foreign';foreign.mkdir();fk=t._kho_cau(foreign);(foreign/'foreign.txt').write_text('foreign\n');fk['g']('add','foreign.txt');fk['g']('commit','-qm','foreign');oid=fk['g']('rev-parse','HEAD')
  al=t._ghi_bn_cau(p,k,{'r.receipt.yaml':t._bn_cau(1,f'anchor:\n    mo_ta: Commit {oid} chua vao master.\n')})
  h.log(direction='foreign-oid-no-pool',oid=oid,result=h.raw(p,al))
  env={'GIT_ALTERNATE_OBJECT_DIRECTORIES':str(foreign/'.git/objects')}
  h.log(direction='foreign-oid-in-pool',result=h.raw(p,al,env=env),fsck=h.git(p,'fsck','--full',env=env),ancestor=h.git(p,'merge-base','--is-ancestor',oid,'HEAD',env=env))
  payload=subprocess.check_output(['git','-C',str(foreign),'cat-file','commit',oid]);local=h.git(p,'hash-object','-t','commit','-w','--stdin',inp=payload.decode());
  for obj in (foreign/'.git/objects').rglob('*'):
   if not obj.is_file():continue
   dst=p/'.git/objects'/obj.relative_to(foreign/'.git/objects')
   if dst.exists():assert dst.read_bytes()==obj.read_bytes()
   else:dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(obj,dst)
  h.log(direction='foreign-same-bytes-imported-local',imported=local,fsck=h.git(p,'fsck','--full'),result=h.raw(p,al))

def promisor():
 for vals in [('true','false'),('false','true'),('yes','off'),('1','no'),('no',),('off',),('false',),('true',)]:
  with tempfile.TemporaryDirectory(prefix='r5-promisor-') as d:
   p=Path(d);k,sha,al=h.anc(p)
   for v in vals:k['g']('config','--add','remote.archive.promisor',v)
   h.log(direction='promisor-precedence',values=vals,effective=h.git(p,'config','--type=bool','--get','remote.archive.promisor'),all=h.git(p,'config','--type=bool','--get-regexp',r'^remote\..*\.promisor$'),fsck=h.git(p,'fsck','--full'),result=h.raw(p,al))

def survivors():
 # File mutants made by the existing test helper; same independent source paths/parity checks as official mutations.
 for name,a,z in [('u3','        if gt not in ("true", "false"):\n','        if False:\n'),('u4','"config", "--type=bool", "--get-regexp"','"config", "--get-regexp"')]:
  old=t.bnv2;t._dot_bien_tep(a,z);mod=t.bnv2;t.bnv2=old
  with tempfile.TemporaryDirectory(prefix='r5-witness-') as d:
   base=Path(d);p=base/'repo';p.mkdir();k,sha,al=h.anc(p);env={}
   if name=='u4':k['g']('config','remote.archive.promisor','off')
   else:
    bin_=base/'bin';bin_.mkdir();real=shutil.which('git');f=bin_/'git'
    f.write_text('#!/usr/bin/env python3\nimport sys,subprocess\na=sys.argv[1:]\nif "--get-regexp" in a:\n print("remote.archive.promisor maybe")\n sys.exit(0)\nsys.exit(subprocess.run(['+repr(real)+',*a]).returncode)\n');f.chmod(0o755);env={'PATH':str(bin_)+os.pathsep+os.environ['PATH']}
   h.log(direction=name,fsck=h.git(p,'fsck','--full'))
   for debt in ((),(h.KEY,)):
    for label,m in [('head',old),('mutant',mod)]:
     h.b=m
     try:h.log(direction=name,module=label,debt=bool(debt),result=h.raw(p,al,debt,env=env))
     finally:h.b=old
 for p in t._TAM_DOT_BIEN:shutil.rmtree(p,ignore_errors=True)

if __name__=='__main__':globals()[sys.argv[1]]()
