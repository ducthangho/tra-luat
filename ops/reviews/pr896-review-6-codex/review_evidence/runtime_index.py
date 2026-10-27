from pathlib import Path
import json
from audit import ROOT,OUT
rows=[]
for p in ROOT.rglob('*.json'):
 if 'run' not in p.name:continue
 try:d=json.loads(p.read_bytes())
 except (ValueError,UnicodeDecodeError):continue
 if isinstance(d,dict) and 'execution_surface' in d and ('run_id' in d or 'lenh' in d):rows.append({'path':str(p.relative_to(ROOT)),'run_id':d.get('run_id'),'head':d.get('head'),'surface':d['execution_surface'],'program':d.get('lenh',{}).get('chuong_trinh')})
(OUT/'all-runtime-index.json').write_text(json.dumps(rows,indent=2));print('runtime_records='+str(len(rows)))
