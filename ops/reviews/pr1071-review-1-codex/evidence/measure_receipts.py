from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import yaml

s = Path(__file__).resolve().parent
r = s / 'cay-kho'
sys.path.insert(0, str(r / 'ops'))
from lease_publish import _tinh_lop_tu_write_set
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
errors = []
checks = []
def git(*args): return subprocess.check_output(['git', *args], cwd=r, env=env)
def sha(b): return hashlib.sha256(b).hexdigest()
def check(name, actual, expected):
    ok = actual == expected
    checks.append({'check': name, 'actual': actual, 'expected': expected, 'ok': ok})
    if not ok: errors.append(checks[-1])
def ancestor(a, b): return subprocess.run(['git', 'merge-base', '--is-ancestor', a, b], cwd=r, env=env).returncode
results = []
for n in (1, 2):
    path = r / f'ops/reviews/pr1058-review-{n}-codex-verdict.receipt.yaml'
    d = yaml.safe_load(path.read_text())
    archive = path.parent / f'pr1058-review-{n}-codex'
    v = (r / d['verdict_path']).read_bytes()
    lines = v.decode().splitlines()
    run = json.loads((r / d['model_reviewer_identity']['run_json']).read_text())
    ident = d['model_reviewer_identity']
    label = f'round{n}.'
    verdict = lines[0].split(': ', 1)[1]
    check(label+'verdict', d['verdict'], {'request_changes': 'changes_requested', 'approve': 'approve'}[verdict])
    check(label+'reviewed_sha', d['reviewed_sha'], lines[1].split(': ', 1)[1])
    check(label+'reviewed_tree', d['reviewed_tree'], git('rev-parse', d['reviewed_sha']+'^{tree}').decode().strip())
    check(label+'verdict_sha256', d['verdict_sha256'], sha(v))
    check(label+'verdict_bytes', d['verdict_bytes'], len(v))
    findings = re.findall(r'^- \[(P[0-3])\] ([a-z0-9-]+):', v.decode(), re.M)
    counts = Counter(h for h, slug in findings)
    for k in range(4): check(label+f'so_p{k}', d[f'so_p{k}'], counts[f'P{k}'])
    check(label+'findings_ids', d['findings_ids'], [{'id': slug, 'hang': h} for h, slug in findings])
    check(label+'ancestor_review_to_land', ancestor(d['reviewed_sha'], d['land_merge_commit']), 0)
    check(label+'land_merge_commit', d['land_merge_commit'], git('rev-parse', '9c7dc11').decode().strip())
    parents = git('show', '-s', '--format=%P', d['land_merge_commit']).decode().strip().split()
    check(label+'merge_parent_count', len(parents), 2)
    check(label+'second_parent', parents[1], git('rev-parse', '3534a6e').decode().strip())
    check(label+'land_on_base', ancestor(d['land_merge_commit'], '97120d3'), 0)
    anchor, blob_path = d['evidence_url'].split('/blob/')[1].split('/', 1)
    check(label+'anchor_oid_full', bool(re.fullmatch('[0-9a-f]{40}', anchor)), True)
    check(label+'evidence_path', blob_path, d['verdict_path'])
    check(label+'anchor_ancestor_head', ancestor(anchor, 'HEAD'), 0)
    check(label+'anchor_blob_bytes', git('show', anchor+':'+blob_path) == v, True)
    check(label+'anchor_blob_sha256', sha(git('show', anchor+':'+blob_path)), d['verdict_sha256'])
    check(label+'anchor_is_artifact_commit', anchor, git('rev-parse', '3145d82').decode().strip())
    check(label+'receipt_commit_after_anchor', ancestor(anchor, 'c92c709'), 0)
    changes = git('diff', '--name-only', d['base_sha'], d['reviewed_sha']).decode().splitlines()
    check(label+'write_set_size', len(changes), 51)
    check(label+'write_set_paths', all(p.startswith(('ops/reviews/', 'ops/land/')) for p in changes), True)
    for field in ('review_class', 'effective_review_class'):
        check(label+field, d[field], _tinh_lop_tu_write_set(changes))
    check(label+'merge_base_at_land_parent', git('merge-base', d['reviewed_sha'], parents[0]).decode().strip(), d['base_sha'])
    src = s / f'nguon/review1058{"a" if n == 1 else "b"}'
    diff_bytes = git('diff', d['base_sha'], d['reviewed_sha'])
    check(label+'DIFF.patch_reproduced', diff_bytes == (src / 'DIFF.patch').read_bytes(), True)
    check(label+'run_id', ident['session_run_id'], run['run_id'])
    check(label+'run_head', run['head'], d['reviewed_sha'])
    check(label+'ma_thoat', run['ma_thoat'], 0)
    check(label+'trang_thai', run['trang_thai'], 'xong')
    check(label+'worktree_sach', run['worktree_sach'], True)
    check(label+'prompt_sha256', run['prompt_sha256'], sha((archive / 'PROMPT.md').read_bytes()))
    check(label+'run_json_vs_launcher_json', run, json.loads((archive / 'launcher.out').read_text()))
    elapsed = (datetime.fromisoformat(run['ket_thuc_utc'])-datetime.fromisoformat(run['bat_dau_utc'])).total_seconds()
    check(label+'duration_from_timestamps', run['thoi_luong_giay'], round(elapsed, 3))
    check(label+'duration_claim', str(run['thoi_luong_giay']) in ident['run_json_ghi_chu'], True)
    check(label+'model_events_claim', len(run['model_phuc_vu']), 27 if n == 1 else 20)
    check(label+'event_model_set', sorted(set(e['model'] for e in run['model_phuc_vu'])), [ident['model_da_chay']])
    check(label+'model_status', run['model_phuc_vu_trang_thai'], 'DO_DUOC')
    check(label+'model_alias', ident['model'], ident['model_da_chay'])
    check(label+'model_evidence_ref', ident['model_evidence_ref'], ident['run_json']+'#model_phuc_vu')
    check(label+'event_ids_unique', len(set(e['response_id'] for e in run['model_phuc_vu'])), len(run['model_phuc_vu']))
    check(label+'effort', run['effort_phuc_vu'], ['xhigh'])
    check(label+'effort_status', run['effort_phuc_vu_trang_thai'], 'DO_DUOC')
    check(label+'sandbox_status', run['sandbox_trang_thai'], 'KHONG_DO_DUOC' if n == 1 else 'DO_DUOC')
    for a,b in [('provider','provider'), ('surface','execution_surface'), ('transport','transport')]:
        check(label+a, ident[a], run[b])
    for f in ('stdout', 'stderr'):
        content = (archive / f'run/{f}.log').read_bytes()
        check(label+f'{f}_sha256', run[f'{f}_sha256'], sha(content))
        check(label+f'{f}_bytes', run[f'{f}_byte'], len(content))
    check(label+'checkpoint_sha256', run['checkpoint_sha256'], sha((archive / 'run/checkpoint.json').read_bytes()))
    cp = json.loads((archive / 'run/checkpoint.json').read_text())
    check(label+'checkpoint_id', cp['checkpoint_id'], run['run_id'])
    check(label+'checkpoint_head', cp['head'], run['head'])
    check(label+'checkpoint_prompt', cp['prompt_sha256'], run['prompt_sha256'])
    results.append({'round': n, 'reviewed_sha': d['reviewed_sha'], 'tree': d['reviewed_tree'],
                    'verdict': d['verdict'], 'counts': [counts[f'P{k}'] for k in range(4)],
                    'verdict_bytes': len(v), 'verdict_sha256': sha(v), 'base_sha': d['base_sha'],
                    'changed_count': len(changes), 'class': _tinh_lop_tu_write_set(changes),
                    'run_id': run['run_id'], 'ma_thoat': run['ma_thoat'], 'duration': run['thoi_luong_giay'],
                    'elapsed_from_timestamps': elapsed, 'models': sorted(set(x['model'] for x in run['model_phuc_vu'])),
                    'event_count': len(run['model_phuc_vu']), 'effort': run['effort_phuc_vu'],
                    'prompt_sha256': run['prompt_sha256'], 'sandbox_status': run['sandbox_trang_thai'],
                    'sandbox_reason': run.get('sandbox_ly_do'), 'sandbox_limits': run['sandbox_gioi_han'],
                    'anchor': anchor, 'parents': parents, 'diff_sha256': sha(diff_bytes)})
check('diff_round2', git('diff', '5dd347c', '3534a6e') == (s / 'nguon/review1058b/DIFF-LUOT2.patch').read_bytes(), True)
check('previous_verdict_round2', (s / 'nguon/review1058b/VERDICT-LUOT1.md').read_bytes() == (s / 'nguon/review1058a/VERDICT.md').read_bytes(), True)
result = {'rounds': results, 'check_count': len(checks), 'errors': errors,
          'merge_commit_utc': datetime.fromisoformat(git('show','-s','--format=%cI','9c7dc11').decode().strip()).astimezone(timezone.utc).isoformat()}
(s / 'evidence/receipts-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2)+'\n')
(s / 'evidence/receipts.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
