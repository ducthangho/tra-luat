"""Mutate only data files on the disposable exact-SHA clone, then restore."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path('/tmp/rv1050-r2-copy')
out = Path(__file__).resolve().parent
verdict = root / 'ops/reviews/wp1037-g1-codex-luot2-verdict.md'
readme = root / 'ops/reviews/README.md'
receipt = root / 'ops/reviews/wp1037-g1-codex-luot2-verdict.receipt.yaml'
mutants = [
    ('mutant-byte', verdict, lambda b: b'W' + b[1:]),
    ('mutant-readme', readme, lambda b: b''.join(line for line in b.splitlines(keepends=True) if not line.startswith(b'| [`wp1037-g1-codex-luot2-verdict.md`]'))),
    ('mutant-count', receipt, lambda b: b.replace(b'\nso_p1: 0\n', b'\nso_p1: 1\n')),
]
summary = {}
for label, path, change in mutants:
    original = path.read_bytes()
    modified = change(original)
    assert modified != original
    try:
        path.write_bytes(modified)
        print('MUTATE', label, path.relative_to(root), 'original_sha256', hashlib.sha256(original).hexdigest(), 'mutant_sha256', hashlib.sha256(modified).hexdigest(), flush=True)
        proc = subprocess.run([sys.executable, str(out / 'run_gates.py'), label], check=True)
        data = json.loads((out / f'{label}-gates.json').read_text())
        summary[label] = {name: result['rc'] for name, result in data.items()}
        print('MUTATION_RESULT', label, summary[label], flush=True)
    finally:
        path.write_bytes(original)
        print('RESTORED', label, path.read_bytes() == original, flush=True)
(out / 'mutations-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print('FINAL_CLONE_STATUS', subprocess.check_output(['git', '-C', str(root), 'status', '--short', '--untracked-files=all', '--ignored=matching'], text=True), flush=True)
