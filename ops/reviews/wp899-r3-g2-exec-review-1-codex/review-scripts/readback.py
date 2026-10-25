import json,hashlib,re,runpy,subprocess,yaml,sys
from pathlib import Path
R=Path(__file__).resolve().parent; root=R.parent
m=runpy.run_path(str(root/'ops/ci_provenance.py')); reg=runpy.run_path(str(root/'.claude/dev/ci_dang_ky_test.py'))
out={'a10':{},'registry':{}}
for rid in (39342960764,40074551995):
 p=root/f'.review-input/a10/provenance-{rid}.yaml'; b=p.read_bytes(); v=yaml.safe_load(b); mc=v['moc']; gs=mc['gate_output']['jobs']; co=mc['checkout']; stdout=(root/f'.review-input/a10/a10-{rid}.stdout.txt').read_text()
 sha=mc['run']['head_sha']; blob=m['git_blob'](sha,mc['run']['loi_khai_rest_path']); wf=yaml.safe_load(blob) if blob else {}; scripts=[s['run'] for j in wf.get('jobs',{}).values() if isinstance(j,dict) for s in j.get('steps',[]) if isinstance(s,dict) and isinstance(s.get('run'),str)]
 actual=m['git_cuc_bo'](sha)
 out['a10'][str(rid)]={'sha256':hashlib.sha256(b).hexdigest(),'hash_in_stdout':hashlib.sha256(b).hexdigest() in stdout,'run':mc['run'],'WD':mc['workflow_definition'],'checkout_counts':{x:sum(c['trang_thai']==x for c in co) for x in ('passed','not_measured','failed','skipped','not_run')},'checkout_git_matches':all(c.get('sha')==sha and c.get('parents')==actual['parents'] and c.get('tree')==actual['tree'] for c in co if c['trang_thai']=='passed'),'git':actual,'labels_all_ubuntu':all(g['labels']==['ubuntu-latest'] for g in gs),'jobs':len(gs),'gate_states':{x:sum(g['trang_thai']==x for g in gs) for x in ('passed','not_measured','failed')},'marker_paths':[(g['name'],g.get('dau_duong',[])) for g in gs if g.get('dau_duong')],'workflow_runs':len(scripts),'workflow_MOI_references':[s for s in scripts if any(p in s for p in reg['MOI'])],'not_measured':m['cac_trang_thai'](v).count('not_measured'),'stdout_summary':re.findall('^NOT_MEASURED: .*$',stdout,re.M)}
normal=reg['kiem'](root=root); removed=reg['kiem'](root=root,registry=reg['DANG_KY']-{'ops/ci_provenance_test.py'})
out['registry']['normal']=normal; out['registry']['removed']=removed
out['registry']['ruff_contract']=reg['loi_ruff_ci'](); sample=(R/'suite.stdout.txt').read_text(); pattern=reg['MOI']['ops/ci_provenance_test.py']
out['registry']['regex_equal_precedent']=pattern==reg['MOI']['ops/land_evidence_nguon_test.py']; out['registry']['accepts_suite']=reg['bang_chung_xanh'](sample,pattern)
out['registry']['rejects_bad']={k:not reg['bang_chung_xanh'](s,pattern) for k,s in [('unequal',sample.replace('CA: 33/33','CA: 32/33')),('zero_mutants',sample.replace('66/66','0/0')),('red',sample.replace('TONG: DAT','TONG: DO'))]}
try: reg['phan_chung']()
except subprocess.CalledProcessError as e: out['registry']['fixture_failure']={'command':e.cmd,'rc':e.returncode,'stdout':e.stdout,'stderr':e.stderr}
out['yaml_version']=yaml.__version__
(R/'readback.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(out,ensure_ascii=False,indent=2))
