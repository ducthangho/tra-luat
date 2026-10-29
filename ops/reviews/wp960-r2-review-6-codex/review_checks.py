import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE / 'cay-kho'
TMP = Path('/tmp/wp960-r6-review')
E = HERE / 'evidence'
BASE = '44884446f71c89e25f9a72ac58e4f597db63c1ba'
SHA = '78c138f863696def68f88080b2b32057fe98f207'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

def run(name, args, cwd=ROOT):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    (E / (name + '.log')).write_text('$ ' + ' '.join(map(str, args)) + '\n' + p.stdout + p.stderr + f'\nrc={p.returncode}\n')
    return p

def record(title, text):
    with (HERE / 'VERDICT.md').open('a') as f:
        f.write(f'\n### {title}\n\n{text}\n')

if __name__ == '__main__':
    p = run('identity', ['git', 'rev-parse', 'HEAD', 'HEAD^{tree}'])
    assert p.stdout.splitlines()[0] == SHA
    status = run('status-before', ['git', 'status', '--short'])
    assert not status.stdout
    spec = hashlib.sha256((ROOT / 'ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md').read_bytes()).hexdigest()
    assert spec == '9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca'
    diff = run('patch-scope', ['git', 'diff', '--numstat', '6dca85f', SHA, '--', 'ops/bien_nhan_v2.py', 'ops/bien_nhan_v2_test.py'])
    old = subprocess.check_output(['git', 'show', '6dca85f:ops/bien_nhan_v2.py'], cwd=ROOT)
    assert old == (ROOT / 'ops/bien_nhan_v2.py').read_bytes()
    record('Hướng 1 — exact SHA, đặc tả và phạm vi vá', f'Lệnh `python3 -B review_checks.py` (phần identity): HEAD/tree = `{p.stdout.strip()}`; status rỗng; spec sha256 `{spec}` đúng. `git diff --numstat 6dca85f {SHA} -- ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py`: `{diff.stdout.strip()}`. Product so lượt 5 byte-identical. Log: `evidence/identity.log`, `evidence/patch-scope.log`.')
    for name, args in [('corpus', [sys.executable, '-B', 'ops/bien_nhan_v2.py', '--root', '.']), ('doctrine', [sys.executable, '-B', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.']), ('diff-check', ['git', 'diff', '--check', BASE, 'HEAD'])]:
        p = run(name, args)
        print(name, 'rc=', p.returncode, p.stdout.strip()[-1800:], p.stderr.strip()[-500:], flush=True)
        record('Kiểm tra ' + name, f'Lệnh `{" ".join(args)}` tại `cay-kho/`: rc={p.returncode}; output:\n\n```text\n{p.stdout.strip()}\n{p.stderr.strip()}\n```\nLog `evidence/{name}.log`.')
    findings = {}
    for label, rev in [('base', BASE), ('head', SHA)]:
        dr = TMP / ('ruff-' + label) / 'ops'
        dr.mkdir(parents=True, exist_ok=True)
        for file in ['bien_nhan_v2.py', 'bien_nhan_v2_test.py']:
            (dr / file).write_bytes(subprocess.check_output(['git', 'show', f'{rev}:ops/{file}'], cwd=ROOT))
        p = run('ruff-' + label, ['ruff', 'check', '--select', 'F', '--output-format', 'json', str(dr)])
        findings[label] = [(Path(x['filename']).name, x['code'], x['location'], x['message']) for x in json.loads(p.stdout)]
    print('ruff', findings, flush=True)
    record('Ruff F delta so base', f'Lệnh `ruff check --select F --output-format json /tmp/wp960-r6-review/ruff-{{base,head}}/ops` trên byte từ `git show`: `{json.dumps(findings, ensure_ascii=False)}`; delta={len(findings["head"])-len(findings["base"])}. Logs `evidence/ruff-*.log`.')
    for name, args in [('git-version', ['git', '--version']), ('python-version', [sys.executable, '--version']), ('ruff-version', ['ruff', '--version'])]:
        p = run(name, args)
        print(name, p.stdout.strip())
