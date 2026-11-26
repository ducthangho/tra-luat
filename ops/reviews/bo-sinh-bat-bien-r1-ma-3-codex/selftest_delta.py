from pathlib import Path
import re,json
w=Path(__file__).resolve().parent;out={}
for side in ['base','head']:
 t=(w/(side+'-selftest.log')).read_text();ids=re.findall(r'^\s*\[FAIL\]\s+(\S+)',t,re.M);total=re.findall(r'== tl selftest (\d+)/(\d+) ==',t)
 assert len(total)==1,(side,total)
 out[side]={'failed_ids':ids,'passed':int(total[0][0]),'total':int(total[0][1]),'status':'failed' if ids else 'passed','log':side+'-selftest.log'}
out['new_failures']=sorted(set(out['head']['failed_ids'])-set(out['base']['failed_ids']));out['resolved']=sorted(set(out['base']['failed_ids'])-set(out['head']['failed_ids']));out['delta']=len(out['new_failures']);out['same_failure_set']=set(out['base']['failed_ids'])==set(out['head']['failed_ids'])
(w/'selftest-delta.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
