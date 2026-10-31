import hashlib
from pathlib import Path
import subprocess

base = Path(__file__).resolve().parents[1]
head = 'f37b5195978f1fe35b9cb55b6f79a2e09d165af0'
for root in [base / 'cay-kho', Path('/tmp/rv1050-r2-copy')]:
    for args in [
        ['rev-parse', 'HEAD', 'HEAD^{tree}'],
        ['status', '--short', '--untracked-files=all', '--ignored=matching'],
        ['diff', '--exit-code'],
        ['diff', '--cached', '--exit-code'],
        ['diff', '--check'],
        ['config', 'core.abbrev'],
    ]:
        proc = subprocess.run(['git', '-C', str(root), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(root.name, 'git', ' '.join(args), 'rc', proc.returncode, 'stdout', proc.stdout.strip() or '(empty)', 'stderr', proc.stderr.strip() or '(empty)')
    paths = subprocess.check_output(['git', '-C', str(root), 'diff', '--name-only', 'b29da0bfe3bfb7a7be69136a1c5c40f82c088a93', head], text=True).splitlines()
    ok = 0
    for path in paths:
        original = subprocess.check_output(['git', '-C', str(root), 'show', head + ':' + path])
        ok += (root / path).read_bytes() == original
    print(root.name, 'ALL_PR_PATHS_EQUAL_EXACT_HEAD', ok, '/', len(paths))
    print(root.name, 'SCOPE_ONLY_OPS_REVIEWS_LAND', all(p.startswith(('ops/reviews/', 'ops/land/')) for p in paths))
    print(root.name, 'NUMSTAT', subprocess.check_output(['git', '-C', str(root), 'diff', '--shortstat', 'b29da0b', head], text=True).strip())
for path in ['PROMPT.md', 'run/8c095c6b/prompt.snapshot']:
    data = (base / path).read_bytes()
    print('PROMPT_SHA256', path, len(data), hashlib.sha256(data).hexdigest())
