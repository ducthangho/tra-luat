from measure import *
s=json.loads((OUT/'surface-audit.json').read_text()); lines=[]; checks=[]
for stem,vpath,rpath in [
 ('pr832-wp831','verdict-luot7/wp831-g1-luot7-codex-verdict.md','verdict-luot7/run.json'),
 ('pr848-wp744','verdicts/wp744-g3-luot1-codex-verdict.md','verdicts/run-f65e544e.json'),
 ('pr862-wp748-r21','verdicts/wp748-r21-luot1-codex-verdict.md','verdicts/wp748-r21-luot1-codex-transcript.txt')]:
 p='ops/land/'+stem+'-provenance/';land=yaml.safe_load((ROOT/('ops/land/'+stem+'-land-evidence.yaml')).read_text());c=next(c for c in land['verdict_usage_caveats'] if c['verdict_path']==p+vpath)
 if rpath.endswith('.json'):
  d=json.loads((ROOT/(p+rpath)).read_text());ok=all(x in c['mo_ta'] for x in [p+rpath,d['run_id'],d['head']]) and d['execution_surface']=='codex_cli';checks.append(ok);lines.append(f'{stem}: runtime={d["run_id"]} head={d["head"]} surface={d["execution_surface"]} source_head_run_in_caveat={ok}')
 else:
  header=(ROOT/(p+rpath)).read_text().splitlines()[:11];ok=header[0].startswith('OpenAI Codex v0.163.0') and p+rpath in c['mo_ta'];checks.append(ok);lines.append(f'{stem}: transcript={header} source_path_in_caveat={ok}')
# The pre-existing pr849 correction is prose under review.luot_cuoi.reviewer.
d=yaml.safe_load((ROOT/'ops/land/pr849-wp748-land-evidence.yaml').read_text());c=d['review']['luot_cuoi']['reviewer']; lines.append('pr849 correction='+c)
for n in [4,5]:
 p=ROOT/f'ops/land/pr849-wp748-provenance/verdicts/wp748-r20-luot{n}-codex-transcript.txt';h=p.read_text().splitlines()[:11];lines.append(f'pr849 luot{n} header={h}');checks.append(h[0].startswith('OpenAI Codex v0.163.0'))
newheads=['5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456','b952c106ba6bbf94699bda5fe5fb2f6d7f7256fb'];no_source='981b9ea1d4bfaa0511cfbc8d9bdee9d8c151c86f'
for head in newheads+[no_source]:lines.append(f'runtime_with_head_{head}='+repr([p for p,d in s['runtime'] if d.get('head')==head]))
lines.append('thu-hoi-lease-a1a-r2/luot2-VERDICT.md: no linked receipt and no runtime for its head in the 124 JSON records; cannot establish CLI-versus-service contradiction. Not counted as a mismatch finding.')
# Broader surface spelling: service phrased in Vietnamese rather than a machine token.
p=ROOT/'ops/reviews/ci-g5-cong-cu-chia-manh-r1-review-5-codex-verdict.receipt.yaml';d=yaml.safe_load(p.read_text());lines.append('ci-g5 luot5: surface='+str(d['model_reviewer_identity']['surface'])+' self='+d['model_reviewer_identity']['surface_tu_khai_trong_verdict']+' caveats='+repr([c['id'] for c in d['verdict_usage_caveats']]))
# Other surface families: check all subagent declarations against their mode and caveat, and Desktop.
for rp in sorted((ROOT/'ops/reviews').glob('*.receipt.yaml')):
 d=yaml.safe_load(rp.read_text());vp=ROOT/d['verdict_path']; text=vp.read_text();mri=d.get('model_reviewer_identity',{}) or {}
 if 'execution_surface: claude_code_subagent' in text:
  caves=[c['id'] for c in d.get('verdict_usage_caveats',[]) or []];checks.append(mri.get('surface')=='claude_code' and 'subagent' in mri.get('che_do','').lower() and any('SUBAGENT' in i for i in caves));lines.append(rp.name+' subagent_declared_in_mode=True caveat='+repr([c for c in caves if 'SUBAGENT' in c]))
 if 'execution_surface: codex_desktop' in text:lines.append(rp.name+' desktop_receipt_surface='+str(mri.get('surface'))); checks.append(mri.get('surface')=='codex_desktop')
corrected=[c for v in s['selfclaims'] for c in v['caveats'] if 'readme_rows' in c];lines.append(f'receipt_surface_caveat_readme_pairs={len(corrected)} all_exact_description_rows={all(c["readme_rows"]==1 and c["description_matches"] for c in corrected)}');lines.append(f'direct_runtime_or_other_surface_checks={len(checks)} all_match={all(checks)}')
(OUT/'surface-source-checks.json').write_text(json.dumps(dict(checks=checks,lines=lines),ensure_ascii=False,indent=2));record(8,'Phân xử các tự khai surface còn lại bằng nguồn cùng lượt','Có caveat nhưng trỏ sai run/head/dòng; hoặc nhầm mô tả chung API và CLI.','python3 review_evidence/surface_sources.py',lines,'KHÔNG PHẢI LỖI mới. #849 đã có đính chính ngay trong hồ sơ; ca thu-hoi không có nguồn mâu thuẫn để kết luận surface. Chỉ ghi KHÔNG ĐO ĐƯỢC cho surface thật khi thiếu runtime, không tự chọn một tên')
