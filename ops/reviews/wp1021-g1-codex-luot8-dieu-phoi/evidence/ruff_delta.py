import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT/'cay-kho'
PATHS = ('ops/bien_nhan_v2.py', 'ops/bien_nhan_v2_test.py')
BASE = 'b29da0bfe3bfb7a7be69136a1c5c40f82c088a93'
result = {'base': [], 'head': []}
normalized = {}
for rev in ('base', 'head'):
    norm = []
    for path in PATHS:
        source = subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=REPO) if rev == 'base' else (REPO/path).read_bytes()
        cmd = ['python3','-m','ruff','check','--no-cache','--select','F','--output-format','json','--stdin-filename',path,'-']
        proc = subprocess.run(cmd, input=source, cwd=REPO, capture_output=True)
        (ROOT/f'evidence/ruff-{rev}-{Path(path).stem}.out').write_bytes(proc.stdout)
        (ROOT/f'evidence/ruff-{rev}-{Path(path).stem}.err').write_bytes(proc.stderr)
        assert proc.returncode in (0,1), proc.stderr
        diagnostics = json.loads(proc.stdout)
        result[rev].append({'path': path, 'command': cmd, 'rc': proc.returncode, 'diagnostics': diagnostics})
        for d in diagnostics:
            norm.append((path,d['code'],d['message'],source.decode().splitlines()[d['location']['row']-1].strip()))
    normalized[rev] = sorted(norm)
result['added'] = [x for x in normalized['head'] if x not in normalized['base']]
result['removed'] = [x for x in normalized['base'] if x not in normalized['head']]
result['normalized'] = normalized
assert not result['added'] and not result['removed'], result
(ROOT/'evidence/ruff-delta.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps({'base_count': len(normalized['base']), 'head_count':len(normalized['head']), 'added':result['added'],'removed':result['removed'],'diagnostics':normalized['head']},ensure_ascii=False))
