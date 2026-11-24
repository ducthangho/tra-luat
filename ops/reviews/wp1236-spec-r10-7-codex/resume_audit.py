import json,shutil
from generate_review import *
T=M/'ops/gate_output_doi_chieu_test.py'
old=Q.with_name('pilot_c2d606b_kq.jsonl');s=G.read_text();mid='a2:_chuan:0:0:bo_if0'
(W/'resume_input.jsonl').write_text(json.dumps({'id':mid,'op':'a2','src':s,'sha256':hashlib.sha256(s.encode()).hexdigest()},ensure_ascii=False)+'\n')
shutil.copyfile(old,W/'resume_kq.jsonl')
n,r,out=run('resume_changed_source',['chay',W/'resume_input.jsonl',T,'--goc',G,'--ra',W/'resume_kq.jsonl','--song-song','1'])
a=[json.loads(x) for x in (W/'resume_kq.jsonl').read_text().splitlines()];assert r['rc']==0 and len(a)==2 and a[1]['phan_hang']=='SONG' and a[1]['sha256']==hashlib.sha256(s.encode()).hexdigest()
print('OLD_KILL_INVALIDATED',r['rc'],a[1],flush=True)
(W/'resume_audit.json').write_text(json.dumps({'receipt':r,'stdout':out,'result':a,'assessment':'Original healthy source under formerly killed stable ID reran and stayed SONG; prior927 results discarded. Uses existing frozen output and healthy source only.'},ensure_ascii=False,indent=2))
