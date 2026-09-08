"""Read-only artifact audit; outputs remain outside cay-kho. No suite is invoked."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'do-review15'
REPO = ROOT / 'cay-kho'
REVIEWS = REPO / 'ops/reviews'
FULL = REVIEWS / 'full-gate-pr468-20260907'
ENV = dict(os.environ, LC_ALL='C', GIT_OPTIONAL_LOCKS='0')

def run(argv, cwd=REPO):
    p = subprocess.run(argv, cwd=cwd, env=ENV, capture_output=True, timeout=30)
    return {'command': argv, 'cwd': str(cwd.relative_to(ROOT)), 'rc': p.returncode,
            'stdout': p.stdout.decode(), 'stderr': p.stderr.decode()}

def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

initial = {key: run(['git', *args]) for key, args in {
    'head': ['rev-parse', 'HEAD'], 'tree': ['rev-parse', 'HEAD^{tree}'],
    'status': ['status', '--porcelain'], 'symbolic_ref': ['symbolic-ref', '-q', 'HEAD'],
    'heads': ['for-each-ref', '--format=%(objectname)\t%(refname)', 'refs/heads'],
    'numstat': ['diff', '--no-ext-diff', '--numstat', '922956a7048fd23eea1c9f88aeb986e076f10e24', 'HEAD'],
    'diff': ['diff', '--no-ext-diff', '922956a7048fd23eea1c9f88aeb986e076f10e24', 'HEAD'],
    'diff_check': ['diff', '--check', '922956a7048fd23eea1c9f88aeb986e076f10e24', 'HEAD'],
}.items()}
initial['numstat_matches_packet'] = initial['numstat']['stdout'].encode() == (ROOT/'numstat.txt').read_bytes()
initial['diff_matches_packet'] = initial['diff']['stdout'].encode() == (ROOT/'diff-sau-luot14.patch').read_bytes()
initial['head_count'] = len(initial['heads']['stdout'].splitlines())
initial['time_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
save('initial.json', initial)

manifests = []
for index, manifest in enumerate(sorted(REVIEWS.rglob('ARTIFACTS.sha256')), 1):
    folder = manifest.parent
    doc = folder / 'DOC-MANIFEST.md'
    mapping = None
    if doc.exists():
        mapping = re.search(r'`VERDICT.md` = `([^`]+)`, `(do-review\d+/)` = thư mục này', doc.read_text())
        assert mapping, doc
    targets, remapped = [], []
    for line in manifest.read_text().splitlines():
        m = re.fullmatch(r'([a-f0-9]{64}) [ *](.+)', line)
        assert m, (manifest, line)
        digest, path = m.groups()
        if mapping and path == 'VERDICT.md':
            target = folder / mapping[1]
        elif mapping:
            assert path.startswith(mapping[2]), (manifest, path)
            target = folder / path[len(mapping[2]):]
        else:
            target = folder / path
        target = target.resolve()
        assert target.is_relative_to(REVIEWS) and target.is_file(), target
        assert not (folder / path).is_symlink(), path
        targets.append(target)
        remapped.append(f'{digest}  {target.relative_to(ROOT)}\n')
    scratch_manifest = OUT / f'manifest-{index:02d}.mapped.sha256'
    scratch_manifest.write_text(''.join(remapped))
    check = run(['sha256sum', '-c', str(scratch_manifest.relative_to(ROOT))], ROOT)
    (OUT / f'manifest-{index:02d}.stdout').write_text(check['stdout'])
    (OUT / f'manifest-{index:02d}.stderr').write_text(check['stderr'])
    uncovered = sorted(str(p.relative_to(folder)) for p in folder.rglob('*')
                       if p.is_file() and p.resolve() not in set(targets))
    row = {'manifest': str(manifest.relative_to(REVIEWS)), 'mapping_doc': str(doc.relative_to(REVIEWS)) if mapping else None,
           'entries': len(targets), 'unique_targets': len(set(targets)),
           'ok': sum(s.endswith(': OK') for s in check['stdout'].splitlines()), 'rc': check['rc'],
           'uncovered_in_folder': uncovered, 'command': check['command'], 'stderr': check['stderr']}
    manifests.append(row)
save('manifests.json', manifests)

pairs = {}
for suffix in ['cidk.tail.txt', 'ploop.tail.txt', 'lease.norm.out', 'doc-claims.json']:
    a, b = [(FULL / f'{side}.{suffix}').read_bytes() for side in ['nen', 'sau']]
    pairs[suffix] = {'bytes': [len(a), len(b)], 'lines': [len(a.splitlines()), len(b.splitlines())],
                     'equal_bytes': a == b, 'sha256': [hashlib.sha256(x).hexdigest() for x in [a, b]]}
    if suffix == 'lease.norm.out':
        pairs[suffix]['logs'] = [{
            'mutations': sum('đột biến' in s for s in raw.decode().splitlines()),
            'empty_red_markers': raw.decode().count('ĐỎ=[]'),
            'line48': raw.decode().splitlines()[47], 'line50': raw.decode().splitlines()[49]
        } for raw in [a, b]]
    if suffix == 'doc-claims.json':
        pairs[suffix]['json_valid'] = all(isinstance(json.loads(x), dict) for x in [a, b])
rc = {}
for side in ['nen', 'sau']:
    rc[side] = []
    for line in (FULL / f'{side}.rc').read_text().splitlines():
        m = re.fullmatch(r'(\S+) rc=(\d+)(?: giay=(\d+))? out=(\d+)B', line)
        assert m, line
        rc[side].append({'suite': m[1], 'rc': int(m[2]), 'seconds': int(m[3]) if m[3] else None, 'out_bytes': int(m[4])})
readme = (FULL/'README.md').read_text()
measurements = {'pairs': pairs, 'recorded_rc': rc, 'full_directory_inventory': sorted(p.name for p in FULL.iterdir()),
    'stdout_size_recountable_suites': {'doc-claims-check': True, 'cidk': False, 'ploop': False, 'lease': False, 'doctrine-scan': False, 'adr-song': False},
    'old_labels_still_present': [{'line': i, 'text': s} for i, s in enumerate(readme.splitlines(), 1) if s.startswith('|') and '**đo lại được**' in s],
    'delta_lines': [{'line': i, 'text': s} for i, s in enumerate(readme.splitlines(), 1) if 'DELTA' in s],
    'fullgate_sh_in_git': run(['git', 'ls-files', '*fullgate.sh']),
    'bundle_prompt_digest': {'recorded': (REVIEWS/'pr468-hoso-4-packet-review-13-codex/bundle-PROMPT.sha256').read_text().strip(),
                             'actual': hashlib.sha256((REVIEWS/'pr468-hoso-4-packet-review-13-codex/bundle-PROMPT.md').read_bytes()).hexdigest()}}
save('evidence.json', measurements)
print(json.dumps({'head': initial['head']['stdout'].strip(), 'tree': initial['tree']['stdout'].strip(),
    'status': initial['status']['stdout'], 'heads': initial['head_count'],
    'diff_matches_packet': initial['diff_matches_packet'], 'numstat_matches_packet': initial['numstat_matches_packet'],
    'manifest_count': len(manifests), 'manifest_entries': sum(x['entries'] for x in manifests),
    'manifest_ok': sum(x['ok'] for x in manifests), 'all_manifest_rc0': all(x['rc'] == 0 for x in manifests),
    'pairs': pairs, 'bundle_prompt_digest': measurements['bundle_prompt_digest']}, ensure_ascii=False, indent=2))
for x in manifests:
    print(f"{x['ok']}/{x['entries']} rc={x['rc']} {x['manifest']} outside={x['uncovered_in_folder']}")
