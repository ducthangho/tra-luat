import ast,collections,hashlib,json,os,subprocess,sys,time
from pathlib import Path
from generate_review import W,R,M,Q,K,G,ENV,run
TEST=M/'ops/gate_output_doi_chieu_test.py'
ms=[json.loads(x) for x in (W/'m1.jsonl').read_text().splitlines()]
# The spec expressly permits src-free manifests in handoff. No source or test program is changed.
(W/'manifest_handoff_no_src.jsonl').write_text(''.join(json.dumps({k:v for k,v in m.items() if k!='src'},ensure_ascii=False)+'\n' for m in ms))
checks=[]
for name,manifest,test,goc in [('handoff_no_src',W/'manifest_handoff_no_src.jsonl',TEST,G),('missing_test',W/'m1.jsonl',W/'does_not_exist_test.py',G)]:
 n,r,out=run(name,['chay',manifest,test,'--goc',goc,'--ra',W/(name+'_kq.jsonl'),'--song-song',4]);checks.append({'name':n,**r,'stdout':out,'stderr':(W/(name+'.stderr')).read_text()});print(n,r['rc'],out[-800:],flush=True)
(W/'runner_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
