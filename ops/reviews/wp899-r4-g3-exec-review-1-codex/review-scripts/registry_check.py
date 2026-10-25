import json,pathlib,runpy,contextlib,io,subprocess
R=pathlib.Path('.review'); reg=runpy.run_path('.claude/dev/ci_dang_ky_test.py');out={}
out['normal']=reg['kiem'](root=pathlib.Path.cwd());out['removed']=reg['kiem'](root=pathlib.Path.cwd(),registry=reg['DANG_KY']-{'ops/ci_provenance_test.py'})
sample=(R/'suite.stdout.txt').read_text();pattern=reg['MOI']['ops/ci_provenance_test.py']
out['ruff_contract']=reg['loi_ruff_ci']();out['same_regex_precedent']=pattern==reg['MOI']['ops/land_evidence_nguon_test.py'];out['accepts_suite']=reg['bang_chung_xanh'](sample,pattern)
out['rejects_bad']={k:not reg['bang_chung_xanh'](v,pattern) for k,v in {'unequal':sample.replace('43/43','42/43'),'zero':sample.replace('87/87','0/0'),'red':sample.replace('TONG: DAT','TONG: DO')}.items()}
try:
 with contextlib.redirect_stdout(io.StringIO()):reg['phan_chung']()
except subprocess.CalledProcessError as e:out['a9_inner_error']={'command':e.cmd,'rc':e.returncode,'stdout':e.stdout,'stderr':e.stderr}
(R/'registry-details.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
