"""Only mutate documentation on the disposable mirror clone; run existing tests."""
import json
import os
from pathlib import Path
import re
import subprocess

BASE = Path(__file__).resolve().parents[1]
COPY = Path('/tmp/pr896-r4-audit-9b8d9a76/copy')
EVIDENCE = BASE / 'review_evidence'
SHA = '2e4183bc2dc40e6bc306e377fc442ff0f405bbe0'
actual = subprocess.check_output(['git', '-C', str(COPY), 'rev-parse', 'HEAD'], text=True).strip()
if actual != SHA or COPY.is_relative_to(BASE / 'cay-kho'):
    raise RuntimeError(f'wrong disposable checkout: {actual}')
subprocess.run(['git', '-C', str(COPY), 'config', 'core.abbrev', '7'], check=True)
readme = COPY / 'ops/reviews/README.md'
receipt = COPY / 'ops/reviews/wp766-r1-g1-exec-review-1-codex-verdict.receipt.yaml'
original = {p: p.read_bytes() for p in [readme, receipt]}
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
results = []
try:
    for mode in ['remove_readme_row', 'remove_receipt_caveat']:
        for p, raw in original.items():
            p.write_bytes(raw)
        if mode == 'remove_readme_row':
            old = readme.read_text()
            lines = old.splitlines(keepends=True)
            selected = [l for l in lines if l.startswith('| `wp766-r1-g1-exec-review-1-codex-verdict.md`')
                        and '`VERDICT-KHAI-SAI-EXECUTION-SURFACE`' in l]
            if len(selected) != 1:
                raise RuntimeError(selected)
            readme.write_text(old.replace(selected[0], '', 1))
            print(mode, 'removed_lines=1', 'removed_bytes=', len(selected[0].encode()), flush=True)
        else:
            old = receipt.read_text()
            pattern = r'(?m)^  - id: VERDICT-KHAI-SAI-EXECUTION-SURFACE\n    muc: P1\n    mo_ta: >-\n      [^\n]+\n'
            new, n = re.subn(pattern, '', old)
            if n != 1:
                raise RuntimeError(n)
            receipt.write_text(new)
            print(mode, 'removed_lines=4', 'removed_bytes=', len(old.encode()) - len(new.encode()), flush=True)
        for prefix in ['t26_', 't27_', 't138_']:
            cmd = ['python3', 'ops/lease_publish_test.py', '--chi-ca=' + prefix]
            r = subprocess.run(cmd, cwd=COPY, env=env, text=True, capture_output=True)
            output = r.stdout + r.stderr
            log = EVIDENCE / f'mutation-{mode}-{prefix}.log'
            log.write_text(output)
            summary = [l for l in output.splitlines() if l.startswith('lease_publish:')]
            error = [l for l in output.splitlines() if any(t in l for t in ['LỖI', 'THẤT BẠI', 'ĐỎ', 'AssertionError', 'không nêu'])]
            item = dict(mode=mode, command=' '.join(cmd), rc=r.returncode, summary=summary, reason=error)
            results.append(item)
            print(json.dumps(item, ensure_ascii=False), flush=True)
finally:
    for p, raw in original.items():
        p.write_bytes(raw)
(EVIDENCE / 'mutations.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
print('copy_status_after_restore=', subprocess.check_output(['git', '-C', str(COPY), 'status', '--porcelain'], text=True).strip())
