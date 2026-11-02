from concurrent.futures import ThreadPoolExecutor
from audit_common import *

commands = {
    'bien-nhan': ['python3', 'ops/bien_nhan_v2.py', '--root', '.'],
    'land': ['python3', 'ops/land_evidence_nguon.py', '--root', '.'],
    'direct': ['python3', str(S / 'direct_gates.py'), '.'],
    'doctrine': ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'],
    'diff-check': ['git', 'diff', '--check', BASE, 'HEAD'],
}

def measure(label):
    rows = []
    for name, cmd in commands.items():
        p = run(cmd, S / 'work' / label)
        (E / f'{label}-{name}.stdout').write_bytes(p.stdout)
        (E / f'{label}-{name}.stderr').write_bytes(p.stderr)
        row = dict(name=name, command=cmd, cwd=str(S / 'work' / label), rc=p.returncode,
                   stdout_bytes=len(p.stdout), stderr_bytes=len(p.stderr))
        rows.append(row)
        print(json.dumps(dict(label=label, **row), ensure_ascii=False), flush=True)
    save(f'{label}-gates.json', rows)
    return rows

with ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(measure, ['head', 'base']))
assert all(row['rc'] == 0 for rows in results for row in rows)
