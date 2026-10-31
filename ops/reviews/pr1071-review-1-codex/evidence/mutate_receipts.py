import json
import os
from pathlib import Path
import re
import subprocess

s = Path(__file__).resolve().parent
root = s / 'mutation-copy'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
summary = []
for n in (1, 2):
    target = root / f'ops/reviews/pr1058-review-{n}-codex-verdict.receipt.yaml'
    original = target.read_bytes()
    text = original.decode()
    mutated, count = re.subn(r'(?m)^verdict_sha256: [0-9a-f]{64}$', 'verdict_sha256: ' + 'f' * 64, text)
    assert count == 1
    try:
        target.write_text(mutated)
        subprocess.run(['python3', str(s / 'run_gates.py'), str(root), f'mutant-{n}'], env=env, check=True,
                       stdout=subprocess.DEVNULL)
        rows = json.loads((s / f'evidence/mutant-{n}-gates.json').read_text())
        measured = {row['name']: {'rc': row['rc'], 'names_target': target.name in row['output'],
                                 'target_lines': [line for line in row['output'].splitlines() if target.name in line]}
                    for row in rows}
        summary.append({'round': n, 'mutation': 'verdict_sha256 -> 64 f characters (valid YAML string/hash shape)', 'results': measured})
        print(json.dumps(summary[-1], ensure_ascii=False, indent=2), flush=True)
    finally:
        target.write_bytes(original)
(s / 'evidence/mutations.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
