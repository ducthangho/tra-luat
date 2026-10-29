import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'cay-kho'
EVIDENCE = ROOT / 'evidence'
EVIDENCE.mkdir(exist_ok=True)
BASE = '96667715996d41bc45e70a64fbaa8996de20f6a0'
HEAD = 'f4d15edcb5d0a9742182273e5950f76165060667'
PREVIOUS = 'fff91390dafb3b8a16e6d11a7243dce036618260'
SPEC = 'ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r1.md'
SPEC_HASH = '377ecea689043fcab4d007d65d9592bd28819fa37983796e0c1b75b2c154e715'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def save(name, data):
    (EVIDENCE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def git(*args):
    p = subprocess.run(['git', '-C', str(REPO), *args], capture_output=True,
                       env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'})
    if p.returncode:
        raise RuntimeError((args, p.returncode, p.stderr.decode('utf-8', errors='replace')))
    return p.stdout

def snapshot(name):
    paths = set(git('ls-files', '-z').split(b'\0'))
    untracked = git('ls-files', '--others', '--exclude-standard', '-z')
    ignored = git('ls-files', '--others', '--ignored', '--exclude-standard', '-z')
    paths.update(untracked.split(b'\0'))
    paths.update(ignored.split(b'\0'))
    files = {}
    for raw in sorted(paths - {b''}):
        rel = os.fsdecode(raw)
        p = REPO / rel
        if not p.exists() and not p.is_symlink():
            files[rel] = {'missing': True}
            continue
        mode = p.lstat().st_mode
        content = os.fsencode(os.readlink(p)) if stat.S_ISLNK(mode) else p.read_bytes()
        files[rel] = {'mode': mode, 'bytes': len(content), 'sha256': digest(content)}
    index_path = Path(os.fsdecode(git('rev-parse', '--path-format=absolute', '--git-path', 'index')).strip())
    data = {
        'head': git('rev-parse', 'HEAD').decode().strip(),
        'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
        'status': git('status', '--porcelain=v1', '--untracked-files=all', '--ignored=matching').decode(),
        'worktree_diff_sha256': digest(git('diff', '--no-ext-diff', '--binary')),
        'cached_diff_sha256': digest(git('diff', '--no-ext-diff', '--cached', '--binary')),
        'index_sha256': digest(index_path.read_bytes()),
        'untracked': os.fsdecode(untracked).split('\0')[:-1],
        'ignored': os.fsdecode(ignored).split('\0')[:-1],
        'files': files,
    }
    save('snapshot-' + name + '.json', data)
    out = {'snapshot': name, 'head': data['head'], 'tree': data['tree'],
           'files_hashed': len(files), 'status_clean': data['status'] == '',
           'untracked_count': len(data['untracked']), 'ignored_count': len(data['ignored'])}
    if name != 'before':
        before = json.loads((EVIDENCE / 'snapshot-before.json').read_text(encoding='utf-8'))
        out['snapshot_unchanged'] = data == before
        assert out['snapshot_unchanged'], 'checkout changed'
    print(json.dumps(out, ensure_ascii=False))

GATES = {
    'adr-song': ['python3', '.claude/dev/packet_loop.py', 'adr-song', '--root', '.'],
    'doctrine-scan': ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.'],
    'doc-claims': ['python3', 'scripts/tl.py', 'doc-claims-check', '--json'],
}

def gate(name):
    cache = EVIDENCE / 'cache' / name
    (cache / 'tmp').mkdir(parents=True, exist_ok=True)
    overrides = {
        'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUTF8': '1', 'PYTHONIOENCODING': 'utf-8',
        'PYTHONPYCACHEPREFIX': str(cache / 'pycache'), 'TL_CACHE_DIR': str(cache / 'tl'),
        'XDG_CACHE_HOME': str(cache / 'xdg'), 'TMPDIR': str(cache / 'tmp'), 'GIT_OPTIONAL_LOCKS': '0',
    }
    p = subprocess.run(GATES[name], cwd=REPO, env={**os.environ, **overrides}, capture_output=True)
    (EVIDENCE / (name + '.stdout')).write_bytes(p.stdout)
    (EVIDENCE / (name + '.stderr')).write_bytes(p.stderr)
    result = {'command': GATES[name], 'cwd': str(REPO), 'env_overrides': overrides, 'rc': p.returncode,
              'stdout_bytes': len(p.stdout), 'stdout_sha256': digest(p.stdout),
              'stderr_bytes': len(p.stderr), 'stderr_sha256': digest(p.stderr)}
    save(name + '.command.json', result)
    print(json.dumps(result, ensure_ascii=False))
    if name == 'doc-claims':
        data = json.loads(p.stdout)
        print(json.dumps({k: data.get(k) for k in ['ok', 'files_scanned', 'flags', 'advisory_count', 'layers_skipped']}, ensure_ascii=False))
        assert data['ok'] is True
    else:
        print(p.stdout.decode('utf-8', errors='replace').strip())
    assert p.returncode == 0

def audit():
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('rev-parse', '--is-shallow-repository').strip() == b'false'
    assert digest((REPO / SPEC).read_bytes()) == SPEC_HASH
    assert digest(git('show', BASE + ':' + SPEC)) == SPEC_HASH
    diff = git('diff', '--no-ext-diff', BASE, HEAD)
    assert diff == (ROOT / 'diff.patch').read_bytes()
    assert git('diff', '--no-ext-diff', PREVIOUS, HEAD) == (ROOT / 'diff-tu-luot-1.patch').read_bytes()
    (EVIDENCE / 'actual-diff.patch').write_bytes(diff)
    numstat = git('diff', '--numstat', BASE, HEAD).decode()
    (EVIDENCE / 'numstat.txt').write_text(numstat, encoding='utf-8')
    rows = [row.split('\t', 2) for row in numstat.splitlines()]
    changed = sorted(row[2] for row in rows)
    lease = (ROOT / 'lease.yaml').read_text(encoding='utf-8')
    block = re.search(r'^write_set:\n((?:- .+\n)+)', lease, re.M).group(1)
    write_set = sorted(line[2:] for line in block.splitlines())
    assert changed == write_set
    normalized = sorted(unicodedata.normalize('NFC', p).casefold() for p in write_set)
    write_hash = digest(json.dumps(normalized, ensure_ascii=False, separators=(',', ':')).encode())
    assert write_hash == re.search(r'^write_set_hash: (\w+)$', lease, re.M).group(1)
    added = sum(int(row[0]) for row in rows)
    deleted = sum(int(row[1]) for row in rows)
    assert len(rows) == 2 and added <= 140 and deleted == 0
    git('diff', '--check', BASE, HEAD)
    protocol = (REPO / 'docs/PROTOCOL_DA_PHIEN.md').read_text(encoding='utf-8')
    spec = (REPO / SPEC).read_text(encoding='utf-8')
    adr = (REPO / 'docs/adr/0057-windows-local-may-chu-kho.md').read_text(encoding='utf-8')
    protocol_diff = git('diff', '--unified=0', BASE, HEAD, '--', 'docs/PROTOCOL_DA_PHIEN.md').decode()
    additions = [line[1:] for line in protocol_diff.splitlines() if line.startswith('+') and not line.startswith('+++')]
    pointer = 'Quy ước sử dụng máy Windows local của chủ kho nằm tại `ADR-0057`.'
    assert len(additions) == 2 and additions.count(pointer) == 1
    lines = protocol.splitlines()
    pointer_line = lines.index(pointer) + 1
    assert protocol.index('#### 10.2.4 Worker gate') < protocol.index(pointer) < protocol.index('## 11.')
    section20 = protocol[protocol.index('## 20.'):]
    adr_rows = [line for line in section20.splitlines() if line.startswith('| `ADR-0057` |')]
    assert len(adr_rows) == 1
    assert adr_rows[0].split('|')[-2].strip() == 'không cổng — kỷ luật executor'
    assert re.search(r'\*\*Trạng thái:\*\* Accepted', adr)
    assert len(re.findall(r'^\d+\. \*\*', adr, re.M)) == 10
    data_rows = {}
    for d in range(1, 7):
        a = next(line for line in adr.splitlines() if line.startswith(f'| D{d} |'))
        s = next(line for line in spec.splitlines() if line.startswith(f'| D{d} |'))
        am, sm = a.split('|')[3].strip(), s.split('|')[3].strip()
        assert re.findall(r'\d+', am) == re.findall(r'\d+', sm)
        data_rows[f'D{d}'] = {'adr': a, 'spec': s, 'numeric_tokens_equal': True}
    save('spec-audit.json', {
        'head': HEAD, 'base': BASE, 'spec_hash': SPEC_HASH, 'authoritative_spec_hash_matches': True,
        'supplied_full_diff_matches': True, 'supplied_r1_r2_diff_matches': True,
        'files': len(rows), 'added_lines': added, 'deleted_lines': deleted,
        'changed_paths': changed, 'lease_write_set': write_set, 'write_set_hash': write_hash,
        'section20_row_count': len(adr_rows), 'section20_row': adr_rows[0],
        'pointer_line': pointer_line, 'protocol_added_lines': additions, 'decision_count': 10,
        'measurements': data_rows,
        'limitations': 'Numeric equality supplements manual semantic review; does not validate the Windows logs or causal inference.'
    })
    print(json.dumps({'files': len(rows), 'added_lines': added, 'deleted_lines': deleted,
                     'write_set_match': True, 'write_set_hash_match': True,
                     'section20_row_count': len(adr_rows), 'pointer_line': pointer_line,
                     'decision_count': 10, 'D1_D6_numeric_cells_equal': True,
                     'full_diff_matches': True, 'r1_r2_diff_matches': True}, ensure_ascii=False))

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'snapshot':
        snapshot(sys.argv[2])
    elif mode == 'gate':
        gate(sys.argv[2])
    elif mode == 'audit':
        audit()
    else:
        raise SystemExit('unknown mode')
