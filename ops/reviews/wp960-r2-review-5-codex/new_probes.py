import os,sys,subprocess,tempfile,shutil,json,contextlib
from pathlib import Path
import replay_probe_recheck as h
b,t=h.b,h.t

def log(**d):h.log(**d)

def matrix():
 for fn in [t.c91_B2_MA_TRAN_nguon_hong_qua_CLI_co_va_khong_no,t.c95_moi_truong_git_KHONG_doi_ket_qua_do,t.c96_git_rc_LA_ma_stderr_RONG_van_la_KHONG_DO_DUOC]:
  orig=t._chay_cli
  def trace(*a,**kw):
   rc,err=orig(*a,**kw);log(case=fn.__name__,rc=rc,err=err);return rc,err
  t._chay_cli=trace
  try:log(case=fn.__name__,result=t._chay_1(fn))
  finally:t._chay_cli=orig

def config():
 for name in ['promisor-false','promisor-zero','promisor-no','promisor-off','empty-partial','home-includeif','xdg-fsync','gitalternates','worktree']:
  with tempfile.TemporaryDirectory(prefix='r4-config-') as d:
   base=Path(d);p=base/'repo';p.mkdir();k,sha,al=h.anc(p);before=h.raw(p,al);env={}
   if name.startswith('promisor-'):k['g']('config','remote.archive.promisor',name.split('-')[1])
   if name=='empty-partial':k['g']('config','extensions.partialclone','')
   if name=='home-includeif':
    home=base/'home';home.mkdir();inc=home/'extra.conf';inc.write_text('[core]\n fsyncObjectFiles = true\n');(home/'.gitconfig').write_text(f'[includeIf "gitdir:{p}/.git"]\n path = {inc}\n');env={'HOME':str(home),'XDG_CONFIG_HOME':str(home/'xdg')}
   if name=='xdg-fsync':
    home=base/'home';home.mkdir();xdg=base/'xdg';(xdg/'git').mkdir(parents=True);(xdg/'git/config').write_text('[core]\n fsyncObjectFiles = true\n');env={'HOME':str(home),'XDG_CONFIG_HOME':str(xdg)}
   if name=='gitalternates':
    alternate=base/'object-pool';shutil.move(p/'.git/objects',alternate);(p/'.git/objects').mkdir();env={'GIT_ALTERNATE_OBJECT_DIRECTORIES':str(alternate)}
   if name=='worktree':
    q=base/'worktree';k['g']('worktree','add','--detach',str(q),'HEAD');p=q
   log(name=name,before=before,config=h.git(p,'config','--list','--show-origin',env=env),fsck=h.git(p,'fsck','--full',env=env),ancestor=h.git(p,'merge-base','--is-ancestor',sha,'HEAD',env=env),after=h.raw(p,al,env=env))

def stderr():
 for name in ['first-only-error','matched-broken-ref','different-error','repeated-harmless']:
  with tempfile.TemporaryDirectory(prefix='r4-stderr-') as d:
   p=Path(d)/'repo';p.mkdir();k,sha,al=h.anc(p);bindir=Path(d)/'bin';bindir.mkdir();real=shutil.which('git')
   msg='error: probe cannot inspect repository state'
   if name=='matched-broken-ref':
    ref=p/'.git/refs/remotes/origin/master';ref.parent.mkdir(parents=True);ref.write_text('broken-ref\n');r=h.git(p,'for-each-ref','--format=%(refname) %(objectname) %(objecttype)',*b._REF_MAC_DINH);log(name=name,real_git_refs=r);msg=r['err'];assert msg
   if name=='repeated-harmless':msg='warning: core.fsyncObjectFiles is deprecated; use core.fsync instead'
   script='#!/usr/bin/env python3\nimport sys,subprocess\na=sys.argv[1:]\np=subprocess.run(['+repr(real)+',*a],capture_output=True)\nsys.stdout.buffer.write(p.stdout)\nsys.stderr.buffer.write(p.stderr)\n'
   script+='if a[-2:]==["rev-parse","--git-dir"]: print('+repr(msg)+',file=sys.stderr)\n'
   if name=='different-error':script+='if "merge-base" in a: print("error: different repository failure",file=sys.stderr)\n'
   if name=='repeated-harmless':script+='if a[-2:]!=["rev-parse","--git-dir"]: print('+repr(msg)+',file=sys.stderr)\n'
   script+='sys.exit(p.returncode)\n';(bindir/'git').write_text(script);(bindir/'git').chmod(0o755);env={'PATH':str(bindir)+os.pathsep+os.environ['PATH']}
   for debt in [(),(h.KEY,)]:log(name=name,debt=bool(debt),result=h.raw(p,al,debt,env=env))

if __name__=='__main__':globals()[sys.argv[1]]()
