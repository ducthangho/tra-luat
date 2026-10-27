from measure import *
inv=json.loads((OUT/'inventory.json').read_text()); receipts=[(p,yaml.safe_load(p.read_text())) for p in (ROOT/'ops/reviews').glob('*.receipt.yaml')]
runtimes=[]
paths=subprocess.check_output(['rg','-l','"execution_surface"','ops/reviews','ops/land','-g','*.json'],cwd=ROOT,text=True).splitlines()
for p in paths:
 try:d=json.loads((ROOT/p).read_text())
 except (ValueError,UnicodeDecodeError):continue
 if isinstance(d,dict) and d.get('execution_surface') and (d.get('run_id') or 'lenh' in d):runtimes.append((p,d))
pairs=[]
for rp,receipt in receipts:
 mri=receipt.get('model_reviewer_identity',{}) or {}; ids=[str(v) for k,v in mri.items() if k in ['session_run_id','run_id','run_id_day_du','session_id'] and v]
 for p,d in runtimes:
  rid=d.get('run_id')
  if rid and any(len(i)>=8 and (rid.startswith(i) or i.startswith(rid)) for i in ids):pairs.append(dict(receipt=rp.name,runtime=p,receipt_surface=mri.get('surface'),runtime_surface=d['execution_surface'],match=mri.get('surface')==d['execution_surface']))
corrections=[]
for p in list((ROOT/'ops/reviews').glob('*-legacy-caveats.yaml'))+list((ROOT/'ops/land').glob('*-land-evidence.yaml')):
 d=yaml.safe_load(p.read_text())
 for obj in walk(d):
  if obj.get('verdict_path') and obj.get('id') and re.search('SURFACE|RUNTIME',obj['id']):corrections.append(dict(source=str(p.relative_to(ROOT)),**obj))
by_hash={}
for rp,d in receipts:by_hash.setdefault(d.get('verdict_sha256'),[]).append((rp,d))
selfclaims=[]; finding_only=[]; readme=(ROOT/'ops/reviews/README.md').read_text().splitlines()
for v in inv['verdicts']:
 hits=[h for h in v['surface_mentions'] if re.search(r'codex[_ -]service|service/API|surface.{0,15}\*?\*?Codex service|bề mặt Codex service',h['text'],re.I)]
 # Review reports below quote findings from earlier reviews, not their own identity.
 if not hits:continue
 if re.search(r'/pr896-review-[2-7]-codex/|/pr915-review-1-codex/|/spec798-may-adr-0054/',v['path']):finding_only.append(v['path']);continue
 # Extra progress snapshots belong to the same reports.
 caveats=[]
 for rp,d in by_hash.get(v['sha256'],[]):
  for c in d.get('verdict_usage_caveats',[]) or []:
   if re.search('SURFACE|RUNTIME',c['id']):
    desc=c.get('mo_ta',c.get('noi_dung','')); rows=[l for l in readme if l.startswith('| `'+Path(d['verdict_path']).name+'` | `'+c['id']+'` |')]
    caveats.append(dict(source=str(rp.relative_to(ROOT)),id=c['id'],description=desc,readme_rows=len(rows),description_matches=len(rows)==1 and desc in rows[0]))
 for c in corrections:
  if c['verdict_path'] in inv['duplicates'].get(v['sha256'],[]):caveats.append(c)
 selfclaims.append(dict(path=v['path'],hits=hits,receipts=[rp.name for rp,d in by_hash.get(v['sha256'],[])],caveats=caveats))
(OUT/'surface-audit.json').write_text(json.dumps(dict(runtime=runtimes,pairs=pairs,selfclaims=selfclaims,finding_only=finding_only),ensure_ascii=False,indent=2))
lines=[f'distinct_verdict_contents={len(inv["verdicts"])} surface_mentions={sum(len(x["surface_mentions"]) for x in inv["verdicts"])}',f'runtime_records_all_json_names={len(runtimes)} surfaces={dict(collections.Counter(d["execution_surface"] for p,d in runtimes))}',f'receipt_runtime_pairs={len(pairs)} mismatches={[x for x in pairs if not x["match"]]}',f'service_self_claims={len(selfclaims)} finding_or_evidence_only={len(finding_only)}']
for v in selfclaims: lines.append(v['path']+' => '+str([(c['source'],c['id']) for c in v['caveats']]))
record(7,'Lớp tự khai surface trong mọi loại tên verdict và provenance land','Còn verdict tự nhận service nhưng run/receipt cùng lượt ghi CLI, chưa đính chính.','python3 review_evidence/inventory.py; python3 review_evidence/surfaces.py',lines,'ĐANG PHÂN LOẠI các trường hợp không có caveat; không dùng chỉ một chuỗi trong finding để quy self-claim')
