import ast
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / 'repo'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', TMPDIR=str(HERE))

def command(args, extra=None):
    p = subprocess.run(args, cwd=ROOT, env=ENV | (extra or {}), text=True, capture_output=True)
    return {'command': args, 'rc': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}

results = {'time': datetime.datetime.now(datetime.timezone.utc).isoformat()}
for key, args in {
    'land_source': [sys.executable, '-B', 'ops/land_evidence_nguon.py', '--root', '.'],
    'land_checker': [sys.executable, '-B', 'ops/kiem_ho_so_land.py', '--root', '.'],
    'doctrine': [sys.executable, '-B', '.claude/dev/packet_loop.py', '--state-dir', str(HERE / 'state'), 'doctrine-scan', '--root', '.'],
    'gop_quick': [sys.executable, '-B', 'ops/cong_cu_test.py', '--gop', str(HERE / 'empty_shards')],
}.items():
    extra = {'CONG_CU_TEST_GOP_CHE_DO': 'duong_nhanh'} if key == 'gop_quick' else {}
    results[key] = command(args, extra)
    print(key, 'rc=', results[key]['rc'], 'stdout_tail=', repr('\n'.join(results[key]['stdout'].splitlines()[-2:])))

old = subprocess.check_output(['git', '-C', str(ROOT), 'show', '4f03566:ops/land_evidence_nguon.py'])
old_path = HERE / 'land_evidence_nguon_4f03566.py'
old_path.write_bytes(old)
results['land_source_4f03566'] = command([sys.executable, '-B', str(old_path), '--root', str(ROOT)])
print('land_source_4f03566 rc=', results['land_source_4f03566']['rc'], 'stdout_tail=', repr('\n'.join(results['land_source_4f03566']['stdout'].splitlines()[-2:])))

readback = json.loads((ROOT / 'ops/land/pr1130-wp1122-provenance/readback-duyet-issuecomment-6635057729.json').read_text())
waiver_re = re.compile(r'mien_gate_output: ([0-9a-f]{40}) os=([a-z0-9,.-]+) ly_do=(\S.*?) han=(\d{4}-\d{2}-\d{2})')
results['pr1130_real_readback'] = {'login': readback['user']['login'], 'association': readback['author_association'],
    'sha40_in_body': re.findall(r'\b[0-9a-f]{40}\b', readback['body']),
    'waiver_lines': [s for s in readback['body'].splitlines() if waiver_re.fullmatch(s.strip())]}
print('pr1130_real_readback', results['pr1130_real_readback'])

jobs = json.loads((ROOT / 'ops/land/pr1055-wp1052-provenance/readback-jobs-41397205258.json').read_text())
if isinstance(jobs, dict):
    jobs = jobs['jobs']
run = json.loads((ROOT / 'ops/land/pr1055-wp1052-provenance/readback-run-41397205258.json').read_text())
results['quick_run'] = {k: run[k] for k in ('id', 'event', 'path', 'head_sha', 'head_branch', 'run_attempt')}
print('quick_run', results['quick_run'])
results['quick_step_success'] = {j['name']: [s['name'] for s in j['steps'] if s['conclusion'] == 'success']
                                 for j in jobs if j['conclusion'] != 'skipped'}

gop = results['gop_quick']['stdout'].strip()
results['gop_day_du_marker_matches'] = bool(re.fullmatch(r'SỐ LIỆU GOM: ca=(\d+) · đột biến=(\d+) · lỗi đột biến=0', gop))
print('gop_day_du_marker_matches', results['gop_day_du_marker_matches'])

results['spec_sha256'] = hashlib.sha256((HERE.parent / 'SPEC.md').read_bytes()).hexdigest()
(HERE / 'checks.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
