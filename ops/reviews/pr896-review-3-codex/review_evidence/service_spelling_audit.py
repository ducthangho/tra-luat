from pathlib import Path
import json,yaml,re
ROOT=Path(__file__).resolve().parent.parent;P=ROOT/'cay-kho/ops/reviews';rows=[]
for f in sorted(P.glob('*-verdict.md')):
 hits=[(i,l) for i,l in enumerate(f.read_text().splitlines(),1) if re.search(r'Codex service|bề mặt service/API',l,re.I) and i<25]
 if not hits:continue
 d=yaml.safe_load(f.with_suffix('.receipt.yaml').read_text());m=d.get('model_reviewer_identity',{})
 if m.get('surface')!='codex_cli':continue
 for n,line in hits:
  cs=d.get('verdict_usage_caveats',[])
  related=[c for c in cs if 'surface' in json.dumps(c,ensure_ascii=False).lower() or 'be mat' in json.dumps(c,ensure_ascii=False).lower() or 'bề mặt' in json.dumps(c,ensure_ascii=False).lower()]
  j={'verdict':f.name,'line':n,'claim':line,'receipt_surface':m['surface'],'receipt_surface_line':next(i for i,l in enumerate(f.with_suffix('.receipt.yaml').read_text().splitlines(),1) if l.strip()=='surface: codex_cli'),'run_id':m.get('session_run_id'),'surface_caveats':related}
  rows.append(j);print(f'{f.name}:{n} receipt.surface:codex_cli@{j["receipt_surface_line"]}; run_id={j["run_id"]}; surface_caveats={len(related)}')
print('TOTAL_EXPLICIT_SERVICE_WITH_CLI_RECEIPT',len(rows));(ROOT/'evidence/service-spelling-candidates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
