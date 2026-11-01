import json
import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
root = HERE / 'work/mutant'
name = 'pr1071-review-1-codex-verdict.receipt.yaml'
path = root / 'ops/reviews' / name
original = path.read_bytes()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
results = {}
try:
    mutated, count = re.subn(rb'(?m)^verdict_sha256: [0-9a-f]{64}$', b'verdict_sha256: '+b'f'*64, original)
    assert count == 1
    path.write_bytes(mutated)
    for key, command in {
        'bien-nhan': ['python3', 'ops/bien_nhan_v2.py', '--root', '.'],
        'direct': ['python3', str(HERE/'direct_checks.py'), '.'],
    }.items():
        p = subprocess.run(command, cwd=root, env=env, capture_output=True)
        output = (p.stdout+p.stderr).decode()
        (HERE/'evidence'/f'mutant-{key}.log').write_text(output)
        results[key] = {'command': command, 'rc': p.returncode,
                        'target_lines': [line for line in output.splitlines() if name in line],
                        'red_receipts': sorted(set(re.findall(r'ĐỎ\s+(\S+\.receipt\.yaml)',output))),
                        'failure_names_target': name in output}
finally:
    path.write_bytes(original)
results['restored_bytewise'] = path.read_bytes() == original
results['status_after'] = subprocess.check_output(['git','status','--porcelain=v1'],cwd=root,env=env).decode()
(HERE/'evidence/mutation.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(results,ensure_ascii=False))
assert results['bien-nhan']['rc'] == 1 and results['bien-nhan']['red_receipts'] == [name]
assert results['direct']['rc'] == 1 and results['direct']['failure_names_target']
assert results['restored_bytewise'] and not results['status_after']
