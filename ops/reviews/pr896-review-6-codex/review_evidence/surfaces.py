from pathlib import Path
import json,hashlib,re,yaml
from audit import ROOT,OUT,record
receipts=[(p,yaml.safe_load(p.read_text())) for p in sorted((ROOT/'ops/reviews').glob('*.receipt.yaml'))]
runtime=[];errors=[]
for p in sorted(ROOT.rglob('run.json')):
 try:runtime.append((p,json.loads(p.read_text())))
 except Exception as e:errors.append([str(p.relative_to(ROOT)),str(e)])
def matching(ids):return [(p,d) for p,d in runtime if d.get('run_id') and any(re.fullmatch('[0-9a-f]{8,40}',str(i)) and (d['run_id'].startswith(str(i)) or str(i).startswith(d['run_id'])) for i in ids)]
findings_only={'pr915-review-1-codex-verdict.md',*[f'pr896-review-{n}-codex-verdict.md' for n in [2,3,4,5]]}
supp=yaml.safe_load((ROOT/'ops/reviews/pr896-review-4-legacy-caveats.yaml').read_text())['caveats'];readme=(ROOT/'ops/reviews/README.md').read_text().splitlines()
claims=[];pairs=[];other=[]
for rp,d in receipts:
 vp=ROOT/d['verdict_path'];mri=d.get('model_reviewer_identity',{});ids=[v for k,v in mri.items() if k in ['session_run_id','run_id','run_id_day_du','session_id']];matches=matching(ids)
 for r,run in matches:pairs.append({'receipt':rp.name,'run':str(r.relative_to(ROOT)),'receipt_surface':mri.get('surface'),'run_surface':run.get('execution_surface'),'same':mri.get('surface')==run.get('execution_surface')})
 hits=[(i,l) for i,l in enumerate(vp.read_text().splitlines(),1) if re.search(r'codex.service|service/API',l,re.I)]
 identity_hits=[(i,l) for i,l in enumerate(vp.read_text().splitlines(),1) if re.search(r'(execution.?surface|reviewer.?surface|be mat|bề mặt)',l,re.I) and (i<35 or i>len(vp.read_text().splitlines())-35)]
 if vp.name in findings_only:continue
 if not hits:
  if identity_hits:other.append({'verdict':vp.name,'surface':mri.get('surface'),'claims':identity_hits,'runtime':[str(p.relative_to(ROOT)) for p,_ in matches]})
  continue
 caveats=d.get('verdict_usage_caveats',[]) or []
 corrections=[c for c in caveats if 'SURFACE' in c.get('id','') or 'RUNTIME-KHONG-DO-DUOC' in c.get('id','')]
 corrections += [c for c in supp if c.get('verdict_path')==d['verdict_path'] and 'SURFACE' in c['id']]
 checks=[]
 for c in corrections:
  desc=c.get('mo_ta',c.get('noi_dung',''));row=[l for l in readme if l.startswith('| `'+vp.name+'` | `'+c['id']+'` |')]
  checks.append({'id':c['id'],'rows':len(row),'exact_description_in_row':len(row)==1 and desc in row[0],'description':desc})
 claims.append({'verdict':vp.name,'hits':hits,'receipt_surface':mri.get('surface'),'ids':ids,'runtime':[str(p.relative_to(ROOT)) for p,_ in matches],'corrections':checks})
# Also enumerate actual verdict files beyond flat review index, deduplicating content.
verdicts=list(ROOT.rglob('*-verdict.md'))+list(ROOT.rglob('VERDICT.md'))
known_hashes={hashlib.sha256((ROOT/d['verdict_path']).read_bytes()).hexdigest() for _,d in receipts}
unknown=[];seen=set()
for p in verdicts:
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 if h in seen or h in known_hashes:continue
 seen.add(h);lines=p.read_text().splitlines();hits=[(i,l) for i,l in enumerate(lines,1) if re.search(r'codex.service|service/API|execution.?surface|reviewer.?surface',l,re.I)]
 if hits:unknown.append({'path':str(p.relative_to(ROOT)),'hits':hits})
result={'runtime_files':len(runtime),'parse_errors':errors,'pairs':pairs,'service_claims':claims,'other_identity_mentions':other,'unknown_verdict_content_with_surface':unknown}
(OUT/'surfaces.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
output=f'verdict_files_repo_wide={len(verdicts)} distinct_content={len({hashlib.sha256(p.read_bytes()).hexdigest() for p in verdicts})}\nrun_json_files={len(runtime)} parse_errors={errors}\nreceipt_runtime_pairs={len(pairs)} mismatches='+repr([x for x in pairs if not x['same']])+f'\nservice_self_claim_files={len(claims)} missing_correction='+repr([x['verdict'] for x in claims if not x['corrections']])+f'\nother_identity_mentions={len(other)} unknown_distinct_verdicts_with_surface={len(unknown)}\n'
for x in claims:output+=x['verdict']+':'+str(x['hits'][0][0])+' receipt_surface='+str(x['receipt_surface'])+' corrections='+str([(c['id'],c['rows'],c['exact_description_in_row']) for c in x['corrections']])+' runtime='+str(x['runtime'])+'\n'
record(8,'Tự khai execution surface và nguồn runtime','python3 review_evidence/surfaces.py; rg -n -i "codex.service|service/api|execution.surface|surface:" cay-kho/ops/reviews --glob "*-verdict.md" --glob "VERDICT.md"',output,'KHÔNG PHẢI LỖI mới trong inventory; tự khai service được đính chính hoặc caveat thiếu runtime, API/shell chung không đủ phân biệt CLI')
