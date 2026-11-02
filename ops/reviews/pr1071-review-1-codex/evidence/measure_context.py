from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import yaml

s = Path(__file__).resolve().parent
r = s / 'cay-kho'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
def git(*args): return subprocess.check_output(['git', *args], cwd=r, env=env)
def receipt(pr, n): return yaml.safe_load((r / f'ops/reviews/pr{pr}-review-{n}-codex-verdict.receipt.yaml').read_text())
errors = []
precedents = []
fixed_fields = ('schema_version', 'kind', 'packet_id', 'role', 'provider', 'executor_provider',
                'cross_provider', 'review_class', 'effective_review_class', 'assurance', 'verdict',
                'so_dem_theo', 'independent_from_executor_session', 'review_axes', 'nguon_co_tham_quyen')
for n in (1,2):
    new = receipt(1058,n)
    old = receipt(1050,n)
    mismatch = {k: [old.get(k),new.get(k)] for k in fixed_fields if old.get(k) != new.get(k)}
    if mismatch: errors.append(['precedent_fixed_fields',n,mismatch])
    old_caveats = {x['id'] for x in old['verdict_usage_caveats']}
    new_caveats = {x['id'] for x in new['verdict_usage_caveats']}
    run = json.loads((r / new['model_reviewer_identity']['run_json']).read_text())
    precedents.append({'round': n, 'fixed_field_mismatches': mismatch,
        'anchor_class_equal': new['anchor']['loai'] == old['anchor']['loai'] and new['anchor']['cuong_do'] == old['anchor']['cuong_do'],
        'caveats_added': sorted(new_caveats-old_caveats), 'caveats_removed': sorted(old_caveats-new_caveats),
        'added_caveat_evidence': run['sandbox_trang_thai'],
        'model_evidence': new['model_reviewer_identity']['model_evidence'],
        'run_model_set': sorted(set(x['model'] for x in run['model_phuc_vu'])),
        'executor_recording_context': (r / f'ops/reviews/pr1058-review-{n}-codex-verdict.receipt.yaml').read_text().splitlines()[2],
        'pr1056_same_executor_precedent': (r / f'ops/reviews/pr1056-review-{n}-codex-verdict.receipt.yaml').read_text().splitlines()[2:5]})
land_path='ops/land/pr1047-wp1045-land-evidence.yaml'
old = yaml.safe_load(git('show','5dd347c:'+land_path))
new = yaml.safe_load(git('show','3534a6e:'+land_path))
jobs = json.loads(git('show','3534a6e:ops/land/pr1047-wp1045-provenance/readback-jobs-41099486628.json'))['jobs']
executed_gate = [x for x in jobs if x['name'].startswith('gate') and x['conclusion'] != 'skipped']
skipped_gate = [{k:x.get(k) for k in ('name','conclusion','labels','runner_id')} for x in jobs if x['name'].startswith('gate') and x['conclusion'] == 'skipped']
closure = {'changed_paths': git('diff','--name-only','5dd347c','3534a6e').decode().splitlines(),
           'authorization_before': old['authorization_ghi_chu'], 'authorization_after': new['authorization_ghi_chu'],
           'landed_before':old['trang_thai_packet']['landed'], 'landed_after':new['trang_thai_packet']['landed'],
           'condition_after':new['trang_thai_packet']['landed_dieu_kien'],
           'jobs_conclusions':dict(Counter(x['conclusion'] for x in jobs)),
           'executed_gate_count':len(executed_gate),
           'executed_gate_windows_count':sum('windows-latest' in x['labels'] for x in executed_gate),
           'skipped_gate':skipped_gate}
if closure['executed_gate_count'] != 14 or closure['executed_gate_windows_count'] != 14: errors.append(['closure_jobs',closure])
if new['trang_thai_packet']['landed'] is not False: errors.append('closure_landed_changed')
history = {}
for rev in ('3145d82','c92c709','0104461'):
    history[rev] = {'parents':git('show','-s','--format=%P',rev).decode().strip().split(),
                    'changed_from_first_parent':git('diff','--name-only',rev+'^1',rev).decode().splitlines()}
summary = (s/'nguon/review1058b/evidence/gates-summary.log').read_bytes()
trailing = [i for i,line in enumerate(summary.splitlines(),1) if line.endswith((b' ',b'\t'))]
result = {'precedents':precedents,'closure':closure,'history':history,'gates_summary_trailing_whitespace_lines':trailing,
          'unmeasured_from_supplied_evidence':[
              'GitHub current PR state, permissions and publication of evidence_url',
              'GitHub merged_at 2026-10-31T07:39:59Z and merge request expectedHeadSha',
              'codex-cli 0.164.0 binary version, full historical CLI arguments and requested-model flag',
              'executor family/session and human authorization beyond recorded statements',
              'absence of fork/context reuse beyond supplied prompt/run/checkpoint files',
              'complete historical sandbox enforcement beyond sampled run.json telemetry'],
          'errors':errors}
(s/'evidence/context.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({**result,'history':{k:{'parents':v['parents'],'changed_count':len(v['changed_from_first_parent'])} for k,v in history.items()}},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
