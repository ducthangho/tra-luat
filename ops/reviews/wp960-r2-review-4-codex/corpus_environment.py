from pathlib import Path
import shutil,subprocess,os,json
import replay_probe_recheck as h
p=Path('/tmp/wp960-r4-environment');shutil.copytree(h.COPY,p,symlinks=True)
def git(*a):
 r=subprocess.run(['git','-C',str(p),*a],capture_output=True,text=True);assert r.returncode==0,(a,r.stderr);return r.stdout.strip()
def gate(label,env=None):
 r=subprocess.run(['python3','-B',str(p/'ops/bien_nhan_v2.py'),'--root',str(p)],capture_output=True,text=True,env={**os.environ,**(env or {})});h.log(case=label,rc=r.returncode,out=r.stdout,err=r.stderr)
gate('GIT_TRACE',{'GIT_TRACE':'1'})
git('config','core.fsyncObjectFiles','true');gate('physical-fsync-warning');git('config','--unset','core.fsyncObjectFiles')
git('update-ref','refs/heads/master/topic',git('rev-parse','HEAD'));gate('local-master-topic');git('update-ref','-d','refs/heads/master/topic')
git('config','remote.archive.promisor','false');gate('promisor-false-real-corpus')
