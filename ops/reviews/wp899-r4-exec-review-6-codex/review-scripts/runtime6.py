from pathlib import Path
import json,os
root=Path.cwd();rows=[]
for p in Path('/root/.codex/sessions/2026/10/25').glob('rollout-*.jsonl'):
 meta=None;ctx=None
 with p.open() as f:
  for line in f:
   try:z=json.loads(line)
   except ValueError:continue
   if z.get('type')=='session_meta':meta=z.get('payload',{})
   if z.get('type')=='turn_context':
    v=z.get('payload',{})
    if v.get('cwd')==str(root):ctx={k:v.get(k) for k in ('cwd','model','effort','approval_policy','sandbox_policy')}
 if ctx:rows.append({'path':str(p),'session_meta':{k:meta.get(k) for k in ('id','cli_version','originator','model_provider','source','cwd')} if meta else None,'turn_context':ctx})
(root/'.review/runtime6.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(json.dumps(rows,ensure_ascii=False,indent=2))
