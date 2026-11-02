from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];out=[]
for x in json.loads((r/'evidence/absence-oracle.json').read_text()):
 d=x['data'];s=x['summary'];mode=s['mode'];actions=s['actions'];expected={'check-only':0,'check-missing-cli':2,'check-missing-nlm-exe':1,'check-missing-nlm-python':1,'check-missing-nlm-all':1,'check-missing-venv':1,'check-metadata-empty':3,'check-metadata-garbage':3,'metadata-recover':2}[mode]
 good=d['tong']==11 and d['loi']==expected and s['rc']==(1 if expected else 0) and d['ok']==(expected==0) and (not mode.startswith('check-') or s['installs']==0)
 if mode=='check-missing-cli':good=good and all(actions[t]=='loi' for t in ['claude','codex'])
 if mode.startswith('check-missing-nlm'):good=good and actions['nlm']=='loi'
 if mode.startswith('check-metadata'):good=good and all(actions[t]=='loi' for t in ['pip','PyYAML','jsonschema'])
 if mode=='metadata-recover':good=good and all(actions[t]=='nang_cap' for t in ['pip','PyYAML','jsonschema']) and actions['venv-kho']=='loi' and actions['nlm']=='loi'
 assert good,mode;out.append(dict(mode=mode,passed=good))
expected={'success':0,'npm-cannot-start':2,'pip-fails':1,'py-disappears':3,'venv-disappears':1,'nlm-pip-fails':1,'nlm-disappears':1,'nlm-status-broken-json':1,'nlm-status-other':1,'check-only':0,'cli-version-stderr-fails':2,'nlm-version-fails':1}
for x in json.loads((r/'evidence/user-extra.json').read_text()):
 d=x['data'];good=x['returncode']==0 and d['error'] is None and d['error_rows']==expected[x['mode']] and len(d['results'])==11 and d['profile_restored'];assert good,x['mode'];out.append(dict(mode=x['mode'],passed=good))
(r/'evidence/extra-regression-assertions.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('Extra regression assertions:',len(out),'/',len(out),'PASS')
