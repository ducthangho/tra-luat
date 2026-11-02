from pathlib import Path
import json,yaml,re,subprocess
R=Path(__file__).resolve().parent.parent/'cay-kho';P=R/'ops/reviews'
print('TOTAL_VERDICTS',len(list(P.glob('*-verdict.md'))))
for f in sorted(P.glob('*-verdict.md')):
 lines=f.read_text().splitlines(); claims=[(i+1,l) for i,l in enumerate(lines) if re.search(r'execution.surface|bề mặt|dịch vụ/API',l,re.I) and (i<20 or l.startswith('- Reviewer') or l.startswith('Định danh:') or (f.name=='pr870-review-3-codex-verdict.md' and i==443))]
 if not claims:continue
 d=yaml.safe_load(f.with_suffix('.receipt.yaml').read_text());m=d.get('model_reviewer_identity',{})
 print('\nVERDICT',f.name)
 for i,l in claims:print('SELF',i,l)
 print('RECEIPT_SURFACE',m.get('surface'),'TU_KHAI',m.get('surface_tu_khai_trong_verdict'))
 refs=[m.get('run_json')];ref=m.get('runtime_evidence_ref');refs+=([ref] if isinstance(ref,str) else []); found=False
 for ref in refs:
  if not isinstance(ref,str):continue
  file=R/ref.split('#')[0]
  if not file.is_file():continue
  try:j=json.loads(file.read_text())
  except (ValueError,IsADirectoryError):continue
  print('RUN',file.relative_to(R),'id',j.get('run_id'),'surface',j.get('execution_surface'),'program',j.get('lenh',{}).get('chuong_trinh'));found=True
 print('RUNTIME_FOUND',found)
 cs=d.get('verdict_usage_caveats',[]);print('CAVEATS',','.join(str(c.get('id')) for c in cs))
 for c in cs:
  if any(x in json.dumps(c,ensure_ascii=False).lower() for x in ['surface','bề mặt','be mat','runtime','run.json']):print('CAVEAT_TEXT',c)
