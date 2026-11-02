import json
import re
from datetime import datetime
from audit import R,P,L,D,git,j,out
lines=L.read_text().splitlines()
# Preserve every scalar with source line for complete semantic inspection.
import yaml
node=yaml.compose(L.read_text())
scalars=[]
def walk(n,path='$'):
 if isinstance(n,yaml.MappingNode):
  for k,v in n.value: walk(v,path+'.'+str(k.value))
 elif isinstance(n,yaml.SequenceNode):
  for i,v in enumerate(n.value): walk(v,path+f'[{i}]')
 else: scalars.append({'line':n.start_mark.line+1,'path':path,'value':n.value})
walk(node)
(R.parent/'evidence/land-scalars.json').write_text(json.dumps(scalars,ensure_ascii=False,indent=2))
out('coverage',line_count=len(lines),scalar_count=len(scalars),sections=list(D),scalar_inventory='evidence/land-scalars.json')
pr=j('readback-pr-1047.json')
for item in D['pre_merge_checks'][:3]+D['post_merge_checks'][1:]:
 run=j('readback-run-'+str(item['run_id'])+'.json')
 assert item['sha']==run['head_sha'] and item['run_attempt']==run['run_attempt'] and item['conclusion']==run['conclusion']
 if item in D['pre_merge_checks'][:3]: assert run['updated_at']<pr['merged_at']
 out('declared_run_matches',id=run['id'],sha=run['head_sha'],attempt=run['run_attempt'],event=run['event'],conclusion=run['conclusion'])
for k in range(1,4):
 run=json.loads((R/f'ops/reviews/wp1045-g1-codex-luot{k}/run/run.json').read_text())
 item=D['review']['luot'][k-1]
 assert item['run_id']==run['run_id'] and item['head']==run['head']
 start=datetime.fromisoformat(run['bat_dau_utc'])
 left=datetime.fromisoformat('2026-10-30T15:10:00+00:00' if k<3 else '2026-10-30T17:29:00+00:00')
 right=datetime.fromisoformat('2026-10-30T17:29:00+00:00' if k<3 else '2026-10-31T17:29:00+00:00')
 assert left<=start<right
 out('generation_window',round=k,generation=1 if k<3 else 2,start=start,within_window=True)
workflow=git('show',D['authorized_head_sha']+':.github/workflows/launcher-windows.yml').decode()
assert "github.event_name != 'pull_request'" in workflow and "contains(github.event.pull_request.labels.*.name, 'windows')" in workflow
out('workflow_at_candidate',sha=D['authorized_head_sha'],path='.github/workflows/launcher-windows.yml',pr_requires_windows_label=True,actual_CI_definition_identity='KHÔNG ĐO ĐƯỢC')
connector=j('readback-comment-6531582115.json')
state=json.loads(re.search(r'codex-review-state:v1 (\{.*?\}) -->',connector['body']).group(1))
code=state['code_review']
assert code=={'commit_sha':D['authorized_head_sha'],'has_any_findings':False,'has_unresolved_findings':False,'status':'completed'}
assert all(v is None for v in state['security_review'].values())
out('connector_scope',code_review=code,security_review=state['security_review'],security_result='KHÔNG ĐO ĐƯỢC')
# Exact set of readback types demonstrates why no checkout or log-output conclusion is made.
files=sorted(x.relative_to(P).as_posix() for x in P.rglob('*') if x.is_file())
out('available_provenance',files=files)
out('section_done',section='scope_audit',result='PASS')
