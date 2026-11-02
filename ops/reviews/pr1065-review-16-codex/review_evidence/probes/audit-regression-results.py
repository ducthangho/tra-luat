from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];rows=[]
def check(name,value):
 rows.append(dict(name=name,pass_=bool(value)));assert value,name
for x in json.loads((r/'evidence/system-matrix.json').read_text()):
 d=x['data'];mode=x['mode'];acts={v['cong_cu']:v['hanh_dong'] for v in d['results']}
 check('system-'+mode+'-driver',x['returncode']==0 and d['error'] is None)
 check('system-'+mode+'-hash-cleanup',all(v['hash_matches'] for v in d['spawns']) and d['remaining_downloads']==0)
 if mode in ['missing-hash','download-tamper']:check('system-'+mode+'-reject',len(d['spawns'])==0 and all(acts[t]=='loi' for t in ['git','gh','node','pwsh']))
 elif mode in ['installer-failure','post-version-wrong']:check('system-'+mode+'-reject',len(d['spawns'])==4 and all(acts[t]=='loi' for t in ['git','gh','node','pwsh']) and d['commander_restart'])
 elif mode=='success':check('system-success-positive',len(d['spawns'])==4 and all(acts[t]=='nang_cap' for t in ['git','gh','node','pwsh']) and d['commander_restart'])
 else:check('system-reboot-positive',acts['git']=='nang_cap' and all(acts[t]=='can_khoi_dong_lai' for t in ['gh','node','pwsh']) and d['commander_restart'])
for x in json.loads((r/'evidence/caller-null.json').read_text()):
 d=x['data'];mode=d['mode'];check(mode+'-driver',x['returncode']==0)
 if mode=='system-pre':check(mode+'-reject',d['errors']==4 and d['spawns']==0)
 elif mode=='system-post':check(mode+'-reject',d['errors']==4 and d['spawns']==4)
 elif mode=='zip-pre':check(mode+'-positive',d['errors']==0 and d['results'][0]['hanh_dong']=='cai_moi')
 else:check(mode+'-reject',d['errors']==1 and d['results'][0]['hanh_dong']=='loi')
(r/'evidence/regression-assertions.json').write_text(json.dumps(rows,indent=2));print('Independent regression assertions:',len(rows),'/',len(rows),'PASS')
