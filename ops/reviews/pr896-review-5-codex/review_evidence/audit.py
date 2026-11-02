import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import yaml

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent / 'cay-kho'
SHA = '1a276a15192013fdb1e472db409133b53ac57944'
PARENT = '77a0a458c6c06f3aafa118953e8e2771daaed911'
MASTER = '3e973a03b151e37cd402e0a723816eeaa8247193'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def blob(ref, name):
    return git('show', ref + ':' + name)

def changed(a=PARENT, b=SHA):
    return git('diff', '--name-only', a, b).decode().splitlines()

def record(direction, command, output, conclusion):
    (BASE / (direction + '.log')).write_text(output + '\n')
    with (BASE.parent / 'VERDICT.md').open('a') as f:
        f.write('\n### ' + direction + '\n- giả thuyết: kiểm tra độc lập dữ liệu được giao.\n- lệnh: `' + command + '`\n- output thật:\n```text\n' + output + '\n```\n- kết luận: ' + conclusion + '\n')
    print(output)

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    pairs = loader.construct_pairs(node, deep=deep)
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError('duplicate YAML key: ' + str(k))
        out[k] = v
    return out

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def history():
    out = []
    for name, args in [('diff.patch', ('diff', PARENT, SHA)), ('diff-pr947.patch', ('diff', MASTER, SHA)), ('numstat.txt', ('diff', '--numstat', PARENT, SHA)), ('numstat-pr947.txt', ('diff', '--numstat', MASTER, SHA))]:
        out.append(f'{name}: byte_match={git(*args) == (BASE.parent / name).read_bytes()}')
    hint = (BASE.parent / 'verdict-cu/pr896-review-4-codex-HINT.patch').read_text()
    paths = re.findall(r'^\+\+\+ (\S+)', hint, re.M)
    scratch = Path('/tmp/pr896-r5-measure-453628b5/hint-parent')
    scratch.mkdir(parents=True, exist_ok=True)
    for p in paths:
        target = scratch / p
        target.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(['git', '-C', str(ROOT), 'show', PARENT + ':' + p], capture_output=True)
        if r.returncode == 0:
            target.write_bytes(r.stdout)
    r = subprocess.run(['patch', '--batch', '--fuzz=0', '-p0', '-i', str(BASE.parent / 'verdict-cu/pr896-review-4-codex-HINT.patch')], cwd=scratch, capture_output=True, text=True)
    (BASE / 'hint-parent-apply.log').write_text(r.stdout + r.stderr)
    out.append(f'hint_paths={len(paths)} apply_to_parent_rc={r.returncode}')
    out.extend(l for l in r.stdout.splitlines() if any(w in l for w in ['FAILED', 'offset', 'fuzz']))
    unchanged = []
    for p in paths:
        if (scratch / p).read_bytes() == (ROOT / p).read_bytes():
            unchanged.append(p)
    out.append(f'exact_hint_blob_matches={len(unchanged)}')
    out.extend('EXACT ' + p for p in unchanged)
    # Compare semantic +/- content for manual merges, without depending on hunk context.
    sections = re.split(r'(?=^--- )', hint, flags=re.M)
    for section in sections:
        m = re.search(r'^\+\+\+ (\S+)', section, re.M)
        if not m or m[1] in unchanged:
            continue
        p = m[1]
        expected = Counter(l for l in section.splitlines() if l[:1] in ['+', '-'] and not l.startswith(('+++', '---')))
        actual_text = git('diff', '--unified=0', PARENT, SHA, '--', p).decode()
        actual = Counter(l for l in actual_text.splitlines() if l[:1] in ['+', '-'] and not l.startswith(('+++', '---')))
        missing = list((expected - actual).elements())
        extra = list((actual - expected).elements())
        out.append(f'MANUAL {p}: missing_hint_lines={len(missing)} extra_delta_lines={len(extra)}')
        out.extend('MISSING ' + l for l in missing)
        out.extend('EXTRA ' + l for l in extra)
    out.append('outside_hint=' + json.dumps(sorted(set(changed()) - set(paths))))
    out.append('commit_after_77a0a45=' + git('rev-list', '--ancestry-path', '--reverse', PARENT + '..' + SHA).decode().strip())
    record('HƯỚNG 2 - doi chieu hint', 'PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py history', '\n'.join(out), 'Đối chiếu +/- và blob được ghi đầy đủ; đánh giá ngữ nghĩa riêng ở các hướng tiếp theo.')

def integrity():
    errors = []
    receipts = sorted((ROOT / 'ops/reviews').glob('*.receipt.yaml'))
    paths = set(receipts)
    paths.update(ROOT / p for p in changed() if p.endswith(('.yaml', '.yml')))
    paths.update((ROOT / 'ops/reviews').glob('*-legacy-caveats.yaml'))
    hashes = 0
    pairs = 0
    for p in sorted(paths):
        try:
            d = yaml.load(p.read_text(), Loader=UniqueLoader)
            ids = [x['id'] for x in d.get('verdict_usage_caveats', [])]
            if len(ids) != len(set(ids)):
                errors.append('duplicate caveat id: ' + str(p.relative_to(ROOT)))
            if p in receipts:
                v = ROOT / d['verdict_path']
                if hashlib.sha256(v.read_bytes()).hexdigest() != d['verdict_sha256']:
                    errors.append('hash mismatch ' + str(p))
                else:
                    hashes += 1
                if d.get('verdict_bytes') and len(v.read_bytes()) != d['verdict_bytes']:
                    errors.append('byte mismatch ' + str(p))
                if v.name.endswith('-verdict.md'):
                    twin = v.parent / v.name.removesuffix('-verdict.md') / 'VERDICT.md'
                    if twin.exists():
                        pairs += 1
                        if twin.read_bytes() != v.read_bytes():
                            errors.append('twin mismatch ' + str(v))
        except Exception as e:
            errors.append(str(p.relative_to(ROOT)) + ': ' + str(e))
    source = ast.parse((ROOT / 'ops/bien_nhan_v2.py').read_text())
    allowlists = {}
    for n in source.body:
        if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == 'ALLOWLIST_CUTOVER' for x in n.targets):
            allowlists['ALLOWLIST_CUTOVER'] = ast.literal_eval(n.value)
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.target.id == 'NO_DA_DO':
            allowlists['NO_DA_DO'] = ast.literal_eval(n.value)
    allowresults = []
    for group, values in allowlists.items():
        for name, h in values.items():
            p = 'ops/reviews/' + name
            data = (ROOT / p).read_bytes()
            ok = hashlib.sha256(data).hexdigest() == h and blob(PARENT, p) == data and blob(MASTER, p) == data
            allowresults.append({'group': group, 'path': p, 'unchanged_and_hash_matches': ok})
            if not ok:
                errors.append('allowlist changed ' + p)
    oldverdicts = []
    for p in changed('3e973a0'):
        if p.endswith('-verdict.md') or p.endswith('/VERDICT.md'):
            before = subprocess.run(['git', '-C', str(ROOT), 'cat-file', '-e', MASTER + ':' + p], capture_output=True)
            if before.returncode == 0:
                oldverdicts.append(p)
    extra = yaml.safe_load((ROOT / 'ops/reviews/pr896-review-4-legacy-caveats.yaml').read_text())
    readme = (ROOT / 'ops/reviews/README.md').read_text()
    legacyrows = []
    for c in extra['caveats']:
        v = ROOT / c['verdict_path']
        rows = [l for l in readme.splitlines() if l.startswith('| `' + v.name + '` | `' + c['id'] + '` |')]
        legacyrows.append({'path': c['receipt_path'], 'hash_matches': hashlib.sha256(v.read_bytes()).hexdigest() == c['verdict_sha256'], 'readme_rows': len(rows), 'description_matches': len(rows) == 1 and c['mo_ta'] in rows[0], 'receipt_same_as_parent': blob(PARENT, c['receipt_path']) == (ROOT / c['receipt_path']).read_bytes()})
    summary = {'yaml_parsed': len(paths), 'receipts': len(receipts), 'verdict_hashes_match': hashes, 'flat_directory_pairs': pairs, 'allowlist_counts': {k: len(v) for k,v in allowlists.items()}, 'allowlist_matches': sum(x['unchanged_and_hash_matches'] for x in allowresults), 'parent_changed_verdicts': [p for p in changed() if p.endswith('-verdict.md') or p.endswith('/VERDICT.md')], 'master_modified_old_verdicts': oldverdicts, 'supplementary': legacyrows, 'errors': errors}
    (BASE / 'integrity-details.json').write_text(json.dumps(allowresults, indent=2) + '\n')
    record('HƯỚNG 3 - toan ven', 'PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py integrity', json.dumps(summary, ensure_ascii=False, indent=2), 'KHÔNG PHẢI LỖI nếu errors rỗng; nguồn và byte cũ được đối chiếu độc lập với cổng.')

if __name__ == '__main__':
    {'history': history, 'integrity': integrity}[sys.argv[1]]()
