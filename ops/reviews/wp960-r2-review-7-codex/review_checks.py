import hashlib
import json
import sys
from review_common import BASE, HEAD, SCRATCH, SHA, SOURCE, emit, run

mode = sys.argv[1]
if mode == 'checks':
    assert run(['git', 'rev-parse', 'HEAD']).stdout.strip() == SHA
    run(['git', 'rev-parse', 'HEAD^{tree}'])
    run(['git', 'status', '--porcelain=v1'])
    run(['git', 'rev-parse', '--is-shallow-repository'])
    sp = SOURCE / 'ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md'
    digest = hashlib.sha256(sp.read_bytes()).hexdigest()
    assert digest == '9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca'
    emit(spec_sha256=digest)
    run(['git', 'diff', '--check', BASE, SHA])
    run(['git', 'diff', '--numstat', BASE, SHA, '--', 'ops/bien_nhan_v2.py', 'ops/bien_nhan_v2_test.py'])
    product = 'ops/bien_nhan_v2.py'
    current = (SOURCE / product).read_bytes()
    for commit in ('6dca85f', '78c138f', SHA):
        p = run(['git', 'rev-parse', f'{commit}:{product}'])
        emit(commit=commit, blob=p.stdout.strip())
    run([sys.executable, '-B', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'])
elif mode == 'ruff':
    results = {}
    for name, sha in [('base', BASE), ('head', SHA)]:
        root = SCRATCH / ('ruff-' + name)
        (root / 'ops').mkdir(parents=True, exist_ok=True)
        for rel in ('ops/bien_nhan_v2.py', 'ops/bien_nhan_v2_test.py'):
            p = __import__('subprocess').run(['git', 'show', sha + ':' + rel], cwd=SOURCE, capture_output=True, check=True)
            (root / rel).write_bytes(p.stdout)
        p = run(['ruff', 'check', '--no-cache', '--select', 'F', '--output-format', 'json', root / 'ops'], cwd=SCRATCH)
        rows = json.loads(p.stdout)
        results[name] = [(str(__import__('pathlib').Path(r['filename']).relative_to(root)), r['code'],
                          r['location'], r['message']) for r in rows]
    emit(ruff=results, delta_zero=results['base'] == results['head'])
elif mode == 'corpus':
    run([sys.executable, '-B', 'ops/bien_nhan_v2.py', '--root', '.'], cwd=HEAD)
