import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent
SPEC = ROOT / 'spec'
REPO = ROOT.parent / 'kho'
BASE = 'e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8'
IMMUTABLE = '29c22f7d1f92321978d4d1dff16bd80d9ea744e0'
HEAD = '4f648e5b784aa4e19f0385eee68cd75e69e1dd18'
TREE = '33f7b4183f408dafc029ecf860aab9857f244365'
W1 = 'scripts/test_fragments/wp433_bundled_tach_manh.py'


def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], text=True).strip()


assert git('rev-parse', 'HEAD') == HEAD
assert git('rev-parse', 'HEAD^{tree}') == TREE
assert git('rev-parse', '--is-shallow-repository') == 'false'
assert git('rev-parse', '--verify', '358451e8^{commit}').startswith('358451e8')
assert subprocess.run(['git', '-C', str(REPO), 'symbolic-ref', '-q', 'HEAD']).returncode == 1
assert not git('status', '--porcelain')
git('merge-base', '--is-ancestor', IMMUTABLE, BASE)
git('merge-base', '--is-ancestor', BASE, HEAD)
print(f'HEAD={HEAD} tree={TREE} detached shallow=false clean; object 358451e8 present')
print(f'immutable={IMMUTABLE} ancestor of base={BASE} ancestor of HEAD')
expected_spec = '5ae3d269551dd6791aafc33e0c498bda7103fef28e85bf6a79cb4ed4d5f26159'
assert hashlib.sha256((SPEC / 'r5.md').read_bytes()).hexdigest() == expected_spec
lease = (SPEC / 'lease.yaml').read_text()
for key, val in {'review_class': 'sensitive', 'effective_review_class': 'sensitive',
                 'generation': '1', 'revision': '11', 'base_sha': BASE,
                 'acceptance_baseline_sha': IMMUTABLE, 'spec_hash': expected_spec}.items():
    assert re.search(rf'^{key}: {val}$', lease, re.M), key
readme = (SPEC / 'README.md').read_text()
for filenames, hashes in re.findall(r'^\| ([^|]+) \| ([^|]+) \|', readme, re.M):
    filenames = re.findall(r'`([^`]+)`', filenames)
    hashes = re.findall(r'`([0-9a-f]{8,64})(?:…)?`', hashes)
    if not filenames:
        continue
    for name, h in zip(filenames, hashes, strict=True):
        actual = hashlib.sha256((SPEC / name).read_bytes()).hexdigest()
        assert actual.startswith(h), name
        print(f'{name} {actual} ({len(h)} hex digits in README)')
approved = re.search(r'(?m)^effective_write_set:\n((?:- [^\n]+\n)+)', lease)[1]
allowed = {line.removeprefix('- ') for line in approved.splitlines()}
canonical = sorted(unicodedata.normalize('NFC', path).casefold() for path in allowed)
digest = hashlib.sha256(json.dumps(canonical, separators=(',', ':')).encode()).hexdigest()
assert f'write_set_hash: {digest}' in lease
actual = set(git('diff', '--name-only', BASE, HEAD).splitlines())
assert actual == allowed - {'scripts/tl_test_fragments_bundled_2.py'}
numstat = git('diff', '--numstat', BASE, HEAD)
assert numstat == (ROOT.parent / 'numstat.txt').read_text().strip()
rows = [line.split('\t') for line in numstat.splitlines()]
assert len(rows) <= 6 and sum(int(row[0]) for row in rows) <= 450
assert git('diff-tree', '--no-commit-id', '--name-only', '-r', HEAD) == 'RELEASE_MANIFEST.json'
print(f'write set: {len(rows)} files, +{sum(int(row[0]) for row in rows)}/-{sum(int(row[1]) for row in rows)}; W3 byte-identical; last commit manifest only')
assert all(git('rev-parse', f'{IMMUTABLE}:{p}') == git('rev-parse', f'{BASE}:{p}')
           for p in ('scripts', '.githooks', '.github', '.claude', 'references', 'RELEASE_MANIFEST.json', 'CHANGELOG.md', 'VERSION'))
print('continuation/immutable runtime trees are identical')
patch_root = ROOT / 'va-base'
target = patch_root / W1
target.parent.mkdir(parents=True, exist_ok=True)
target.write_bytes((SPEC / 'base-w1.py').read_bytes())
subprocess.run([sys.executable, '-B', str(SPEC / 'va.py'), str(patch_root)], check=True)
assert target.read_bytes() == (SPEC / 'candidate-w1.py').read_bytes()
print(f'W1 identical to va.py(base); SHA256={hashlib.sha256(target.read_bytes()).hexdigest()}')
