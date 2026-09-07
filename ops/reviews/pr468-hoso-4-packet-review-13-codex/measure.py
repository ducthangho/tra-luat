import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE / 'cay-kho'
OUT = BASE / 'do-review13'
SHA = 'f77f19895e00835d71644d82f1c54e9b519ccfe6'
PREV = '02b0b86bf64a89b561a75ff060164332792fb73d'

def git(*args, root=ROOT, env=None, input=None):
    return subprocess.run(['git', '-C', str(root), *args], input=input,
                          capture_output=True, check=True, env=env).stdout

def save(name, value):
    (OUT / (name + '.json')).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(value, ensure_ascii=False))

def note(value):
    p = BASE / 'VERDICT.md'
    s = p.read_text()
    assert s.endswith('verdict: dang-do\n')
    p.write_text(s.removesuffix('verdict: dang-do\n') + value + '\n\nverdict: dang-do\n')

def refs(root, prefix):
    rows = git('for-each-ref', '--format=%(refname)%09%(objectname)%09%(symref)', prefix, root=root).decode().splitlines()
    return {r.split('\t')[0].removeprefix(prefix + '/'): r.split('\t')[1]
            for r in rows if not r.split('\t')[2]}

def preflight():
    source = {}
    for line in (BASE / 'tai-lieu/ls-remote-heads.txt').read_text().splitlines():
        oid, ref = line.split()
        assert ref.startswith('refs/heads/') and len(oid) == 40
        name = ref.removeprefix('refs/heads/')
        assert name not in source
        source[name] = oid
    local = refs(ROOT, 'refs/remotes/origin')
    bare = refs(BASE / 'kho.git', 'refs/heads')
    result = {
        'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'head': git('rev-parse', 'HEAD').decode().strip(),
        'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
        'status': git('status', '--porcelain').decode(),
        'abbrev': git('config', '--get', 'core.abbrev').decode().strip(),
        'shallow': git('rev-parse', '--is-shallow-repository').decode().strip(),
        'origin': git('remote', 'get-url', 'origin').decode().strip(),
        'snapshot_count': len(source), 'remote_count': len(local), 'bare_count': len(bare),
        'local_heads': refs(ROOT, 'refs/heads'),
        'missing': sorted(source.keys() - local.keys()),
        'extra': sorted(local.keys() - source.keys()),
        'oid_mismatch': {k: [source[k], local[k]] for k in source.keys() & local.keys() if source[k] != local[k]},
        'bare_equals_snapshot': bare == source,
        'source': source, 'local': local,
    }
    for label, rev, patch, stat in [('since12', PREV, 'diff-tu-luot12.patch', 'numstat-tu-luot12.txt'), ('full', 'origin/master', 'diff.patch', 'numstat.txt')]:
        diff = git('diff', rev, SHA)
        num = git('diff', '--numstat', rev, SHA)
        rows = [line.split('\t', 2) for line in num.decode().splitlines()]
        result[label] = {'files': len(rows), 'added': sum(int(a) for a,b,p in rows),
                         'deleted': sum(int(b) for a,b,p in rows),
                         'outside_ops': [p for a,b,p in rows if not p.startswith('ops/')],
                         'patch_equal': diff == (BASE / patch).read_bytes(),
                         'numstat_equal': num == (BASE / stat).read_bytes(),
                         'commits': git('log', '--format=%H %s', rev + '..' + SHA).decode().splitlines()}
    save('preflight', result)
    assert result['head'] == SHA and result['status'] == ''
    assert local == source == bare
    note('- `mirror-thieu-ref-khong-du-do-a9` [P1]: **ĐÃ VÁ THẬT** bằng bundle. Tự so tập tên và OID: snapshot 303, checkout 303, bare 303; thiếu 0, thừa 0, lệch OID 0. Đã có năng lực quét A9 trên snapshot đủ ref được giao; GitHub trực tiếp KHÔNG ĐO ĐƯỢC (cấm mạng). Bằng chứng: `do-review13/preflight.json`.')

def leases():
    source = json.loads((OUT / 'preflight.json').read_text())['source']
    env = dict(os.environ)
    env.update({'GIT_ALLOW_PROTOCOL': 'file', 'GIT_CONFIG_COUNT': '1',
                'GIT_CONFIG_KEY_0': 'url.' + (BASE / 'kho.git').as_uri() + '.insteadOf',
                'GIT_CONFIG_VALUE_0': 'https://github.com/ducthangho/tra-luat.git',
                'PYTHONDONTWRITEBYTECODE': '1'})
    redirected = git('ls-remote', '--heads', 'origin', env=env).decode().splitlines()
    got = {line.split()[1].removeprefix('refs/heads/'): line.split()[0] for line in redirected}
    assert got == source
    result = {'transport': 'real git ls-remote redirected to sandbox bare via per-process url.insteadOf; GIT_ALLOW_PROTOCOL=file; no network', 'redirected_refs': len(got), 'paths': {}}
    for path in ['.github/workflows/ci.yml', '.claude/dev/ci_dang_ky_test.py', '.claude/hooks/pretooluse_guard_test.py']:
        cmd = ['python3', '-B', 'ops/lease_publish.py', 'ai-dang-giu', path]
        start = dt.datetime.now(dt.timezone.utc)
        t = time.monotonic()
        p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True)
        name = 'ai-dang-giu-' + Path(path).name
        (OUT / (name + '.stdout')).write_bytes(p.stdout)
        (OUT / (name + '.stderr')).write_bytes(p.stderr)
        lines = p.stdout.decode().splitlines()
        old = [line for line in lines if '\tmutant-khong-chay-tren-windows-exec-1-claude-20260906\t' in line]
        result['paths'][path] = {'command': cmd, 'started_utc': start.isoformat(), 'seconds': round(time.monotonic()-t,3),
            'rc': p.returncode, 'holder': [l for l in lines if l.startswith('NGƯỜI_GIỮ ')],
            'old456_lines': old, 'old456_states': sorted(set(l.split('\t')[0] for l in old))}
    lease_path = 'ops/leases/mutant-khong-chay-tren-windows-exec-1-claude-20260906.yaml'
    names = sorted(source)
    batch = ''.join('refs/remotes/origin/' + name + ':' + lease_path + '\n' for name in names)
    raw = git('cat-file', '--batch-check', input=batch.encode())
    (OUT / 'old456-batch-check.txt').write_bytes(raw)
    blobs = {}
    for name, line in zip(names, raw.decode().splitlines(), strict=True):
        if line.endswith(' missing'):
            continue
        oid, typ, size = line.split()
        assert typ == 'blob'
        blobs.setdefault(oid, []).append(name)
    result['old456_blobs'] = blobs
    result['scanner_refs'] = len(git('for-each-ref', '--format=%(refname)', 'refs/heads', 'refs/remotes').decode().splitlines()) - len(git('for-each-ref', '--format=%(symref)', 'refs/heads', 'refs/remotes').decode().split())
    result['lease_code_unchanged_since12'] = not git('diff', PREV, SHA, '--', 'ops/lease_publish.py')
    save('leases', result)
    target = 'NGƯỜI_GIỮ 1: gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906'
    assert all(result['paths'][p]['holder'] == [target] and result['paths'][p]['rc'] == 11 for p in list(result['paths'])[:2])
    assert result['paths']['.claude/dev/ci_dang_ky_test.py']['old456_states'] == ['HẾT_HẠN']
    note('- `bia-mo-mot-ref-khong-thu-hoi-moi-ban` [P1]: **ĐÃ VÁ THẬT về trạng thái, đóng bằng THỜI GIAN**, cơ chế bia mộ chưa sửa (ngoài phạm vi PR). CLI sản phẩm chạy thật trên đủ snapshot ref: cả hai path có NGƯỜI_GIỮ 1 = exec-1r4, rc=11; registry còn 2 dòng #456 đều HẾT_HẠN. Tham số môi trường chỉ chuyển ls-remote sang bare đã so khớp; không giả scanner/đồng hồ/output. Bằng chứng: `do-review13/leases.json` và stdout. Số ref mang từng blob được ghi riêng, không suy từ số dòng CLI.')

if __name__ == '__main__':
    {'preflight': preflight, 'leases': leases}[sys.argv[1]]()
