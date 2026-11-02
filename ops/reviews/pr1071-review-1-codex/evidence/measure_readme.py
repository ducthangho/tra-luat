from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import yaml

s = Path(__file__).resolve().parent
r = s / 'cay-kho'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
errors = []
def git(*args): return subprocess.check_output(['git', *args], cwd=r, env=env)
raw = (r / 'ops/reviews/README.md').read_bytes()
lines = raw.decode().splitlines()
new_rows = [line for line in lines if line.startswith('|') and 'pr1058-review-' in line]
index = [line for line in new_rows if '-verdict.receipt.yaml' in line]
caveats = [line for line in new_rows if '-verdict.receipt.yaml' not in line]
if (len(index), len(caveats)) != (2, 7): errors.append(['row_counts', len(index), len(caveats)])
results = []
for n in (1, 2):
    file = f'pr1058-review-{n}-codex-verdict.md'
    d = yaml.safe_load((r / f'ops/reviews/pr1058-review-{n}-codex-verdict.receipt.yaml').read_text())
    rows = [line for line in index if file in line]
    assert len(rows) == 1
    cells = [cell.strip() for cell in rows[0].split('|')[1:-1]]
    counts = '/'.join(str(d[f'so_p{k}']) for k in range(4))
    measured = {'verdict': d['verdict'] in cells[3], 'assurance': d['assurance'] in cells[3],
                'counts': counts+' (P0/P1/P2/P3)' in cells[3],
                'head': cells[4].strip('`') == d['reviewed_sha'][:7], 'bytes': int(cells[5]) == d['verdict_bytes'],
                'run_id': d['model_reviewer_identity']['session_run_id'][:8] in cells[3],
                'model': d['model_reviewer_identity']['model'] in cells[3],
                'receipt_link': f'pr1058-review-{n}-codex-verdict.receipt.yaml' in cells[1]}
    expected = {x['id']: x['mo_ta'] for x in d['verdict_usage_caveats']}
    own = [line for line in caveats if file in line]
    actual = {line.split('|')[2].strip().strip('`'): line.split('|')[3].strip() for line in own}
    measured['caveat_ids_exact'] = set(expected) == set(actual)
    measured['caveat_count'] = len(own) == len(expected)
    # The sandbox caveat is paraphrased in README. Check all factual tokens.
    text_results = {}
    for cid in expected:
        if cid == 'SANDBOX-MODE-KHONG-DO-DUOC':
            text_results[cid] = all(x in actual.get(cid, '') for x in ('KHONG_DO_DUOC','DanhTinhDoi','sandbox_quan_sat','mau quan sat'))
        else: text_results[cid] = expected[cid] == actual.get(cid)
    measured['caveat_text'] = all(text_results.values())
    if not all(measured.values()): errors.append([n, measured])
    results.append({'round': n, 'index_line': rows[0], 'caveat_ids': sorted(actual), 'checks': measured,
                    'caveat_text_checks': text_results})
base = git('show', '97120d3:ops/reviews/README.md')
removed_new = b''.join(line for line in raw.splitlines(keepends=True) if b'pr1058-review-' not in line)
existing_lines_equal = removed_new == base
if not existing_lines_equal: errors.append('README minus nine new rows differs from base')
preserved = {}
for rev in ('97120d3', 'origin/master', 'HEAD^1', 'HEAD^2'):
    old = git('show', rev+':ops/reviews/README.md')
    oldrows = Counter(line for line in old.splitlines() if line.startswith(b'|'))
    missing = oldrows - Counter(line for line in raw.splitlines() if line.startswith(b'|'))
    preserved[rev] = {'table_rows': sum(oldrows.values()), 'missing_or_changed': sum(missing.values())}
    if missing: errors.append([rev, 'missing_or_changed_rows', [x.decode() for x in missing]])
diff = git('diff', '97120d3', 'HEAD', '--', 'ops/reviews/README.md')
(s / 'evidence/readme.diff').write_bytes(diff)
result = {'index_rows': len(index), 'caveat_rows': len(caveats), 'rounds': results,
          'readme_minus_new_rows_equals_base_bytewise': existing_lines_equal, 'preserved': preserved, 'errors': errors}
(s / 'evidence/readme.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
