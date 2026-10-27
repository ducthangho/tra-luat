"""Read-only measurements; run from the directory containing PROMPT.md."""
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import yaml

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'cay-kho'
SCRATCH = Path('/tmp/pr896-r4-audit-9b8d9a76')
SHA = '2e4183bc2dc40e6bc306e377fc442ff0f405bbe0'
PARENT = 'c8c1ee015f78fdb143a18cf926f9f3481c2a3dd1'
HINT = BASE / 'verdict-cu/pr896-review-3-codex-HINT.patch'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def changes(patch):
    result = collections.defaultdict(collections.Counter)
    path = None
    for line in patch.splitlines():
        if line.startswith('+++ '):
            path = line[4:]
            if path.startswith('b/'):
                path = path[2:]
        elif line.startswith(('--- ', 'diff ', 'index ', '@@')):
            continue
        elif path and line.startswith(('+', '-')):
            result[path][line] += 1
    return result

def history():
    for args, supplied in [(['diff', PARENT, SHA], 'diff.patch'),
                           (['diff', '--numstat', PARENT, SHA], 'numstat.txt'),
                           (['diff', '101263f', SHA], 'diff-pr947.patch'),
                           (['diff', '--numstat', '101263f', SHA], 'numstat-pr947.txt')]:
        print(supplied, 'byte_match=', git(*args) == (BASE / supplied).read_bytes())
    old = changes(HINT.read_text())
    new = changes(git('diff', PARENT, SHA).decode())
    d = SCRATCH / 'hint-parent'
    d.mkdir(exist_ok=True)
    for path in old:
        p = d / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(git('show', f'{PARENT}:{path}'))
    r = subprocess.run(['patch', '--batch', '--fuzz=0', '-p0', '-i', str(HINT)],
                       cwd=d, text=True, capture_output=True)
    (BASE / 'review_evidence/old-hint-apply.log').write_text(r.stdout + r.stderr)
    print('old_hint_on_parent_rc=', r.returncode)
    for path, expected in old.items():
        missing = expected - new[path]
        extra = new[path] - expected
        exact = (d / path).read_bytes() == (ROOT / path).read_bytes()
        print(path, 'missing_hint_lines=', sum(missing.values()),
              'extra_delta_lines=', sum(extra.values()), 'patched_blob_match=', exact)
        for line, n in missing.items():
            print('  MISSING', n, line)
        for line, n in extra.items():
            print('  EXTRA', n, line)
    print('additional_paths=', sorted(set(new) - set(old)))
    path = 'ops/reviews/pr889-review-1-codex-verdict.receipt.yaml'
    print('merge_pr889_receipt_equals_master=', git('show', f'101263f:{path}') == git('show', f'c8c1ee0:{path}'))
    def row(rev):
        return [l for l in git('show', f'{rev}:ops/reviews/README.md').decode().splitlines()
                if l.startswith('| `pr889-review-1-codex-verdict.md`') and 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' in l]
    print('merge_pr889_README_caveat_equals_master=', row('101263f') == row('c8c1ee0'), 'rows=', len(row('101263f')))
    print('next_commit_after_c8c1ee0=', git('rev-list', '--ancestry-path', '--reverse', f'{PARENT}..{SHA}').decode().strip())

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    out = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in out:
            raise ValueError(f'duplicate YAML key {key!r} at {key_node.start_mark}')
        out[key] = loader.construct_object(value_node, deep=deep)
    return out

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def integrity():
    receipts = sorted((ROOT / 'ops/reviews').glob('*.receipt.yaml'))
    land = [ROOT / 'ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml']
    errors = []
    matching = 0
    copies = 0
    for p in receipts + land:
        try:
            d = yaml.load(p.read_text(), Loader=UniqueLoader)
            caveats = d.get('verdict_usage_caveats') or []
            ids = [c.get('id') for c in caveats]
            if len(ids) != len(set(ids)):
                errors.append((str(p.relative_to(ROOT)), 'duplicate caveat ids'))
            if p in land:
                continue
            v = ROOT / d['verdict_path']
            raw = v.read_bytes()
            if hashlib.sha256(raw).hexdigest() != d['verdict_sha256']:
                errors.append((p.name, 'hash mismatch'))
            elif 'verdict_bytes' in d and len(raw) != d['verdict_bytes']:
                errors.append((p.name, 'byte count mismatch'))
            else:
                matching += 1
            original = v.parent / v.name.removesuffix('-verdict.md') / 'VERDICT.md'
            if original.exists():
                copies += 1
                if raw != original.read_bytes():
                    errors.append((p.name, 'flat/directory mismatch'))
        except Exception as e:
            errors.append((str(p.relative_to(ROOT)), str(e)))
    print('YAML_parsed=', len(receipts) + len(land), 'receipts=', len(receipts),
          'hash_and_bytes_match=', matching, 'flat_directory_pairs=', copies)
    print('errors=', json.dumps(errors, ensure_ascii=False))
    for base in [PARENT, '101263f']:
        changed = git('diff', '--name-only', base, SHA, '--', 'ops/reviews/*-verdict.md', 'ops/reviews/**/VERDICT.md').decode().splitlines()
        print('changed_verdicts_since_' + base + '=', len(changed), changed)
    print('all_flat_verdicts=', len(list((ROOT / 'ops/reviews').glob('*-verdict.md'))),
          'nested_VERDICT=', len(list((ROOT / 'ops/reviews').rglob('VERDICT.md'))))

def caveats():
    cid = 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC'
    readme = (ROOT / 'ops/reviews/README.md').read_text().splitlines()
    runs = []
    for p in ROOT.rglob('run.json'):
        try:
            d = json.loads(p.read_text())
            runs.append((p, d))
        except (ValueError, OSError):
            pass
    print('all_repo_run_json=', len(runs))
    n = 0
    for p in sorted((ROOT / 'ops/reviews').glob('*.receipt.yaml')):
        d = yaml.safe_load(p.read_text())
        for c in d.get('verdict_usage_caveats') or []:
            if c.get('id') != cid:
                continue
            n += 1
            text = c['mo_ta']
            line = int(re.search(r'Verdict dong (\d+)', text)[1])
            run_id = re.search(r'run ID khai ([0-9a-f]+)', text)[1]
            identity = d['model_reviewer_identity']
            verdict = ROOT / d['verdict_path']
            actual_line = verdict.read_text().splitlines()[line - 1]
            matches = [str(q.relative_to(ROOT)) for q, r in runs
                       if str(r.get('run_id', '')).startswith(run_id)]
            rows = [l for l in readme if l.startswith('| `' + verdict.name + '`') and '`' + cid + '`' in l]
            exact_row = len(rows) == 1 and rows[0].split(' | ')[2].removesuffix(' |') == text
            print(verdict.name, 'line=', line, 'surface=', identity['surface'],
                  'run_id=', run_id, 'matches_receipt=', run_id == identity['session_run_id'],
                  'runtime_files=', matches, 'README_rows=', len(rows), 'README_text_match=', exact_row)
            print('  VERDICT:', actual_line)
    print('P2_caveat_count=', n)
    p = ROOT / 'ops/reviews/wp766-r1-g1-exec-review-1-codex-verdict.receipt.yaml'
    d = yaml.safe_load(p.read_text())
    run_id = d['model_reviewer_identity']['session_run_id']
    wp_runs = [(p, r) for p, r in runs if r.get('run_id') == run_id]
    print('wp766_run_id=', run_id, 'matching_run_json=', len(wp_runs))
    for p, r in wp_runs:
        print('wp766_runtime_path=', p.relative_to(ROOT))
        print('wp766_runtime=', json.dumps({k: r.get(k) for k in ['run_id', 'execution_surface', 'lenh']}, ensure_ascii=False))
        for i, l in enumerate(p.read_text().splitlines(), 1):
            if 'execution_surface' in l:
                print('wp766_runtime_surface_line=', i, l.strip())
    v = ROOT / d['verdict_path']
    print('wp766_verdict_line_12=', v.read_text().splitlines()[11])
    print('wp766_hash=', hashlib.sha256(v.read_bytes()).hexdigest(), 'bytes=', v.stat().st_size)

if __name__ == '__main__':
    {'history': history, 'integrity': integrity, 'caveats': caveats}[sys.argv[1]]()
