import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE / 'work/head'
SOURCE = HERE / 'nguon/review1071a'
ARCHIVE = ROOT / 'ops/reviews/pr1071-review-1-codex'
BASE = '3574cb07dba8a8f7f32384ee3d1d3dfbf3a4f70e'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
errors = []
def sha(data):
    return hashlib.sha256(data).hexdigest()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, env=env)
def check(value, label):
    if not value:
        errors.append(label)

head = git('rev-parse', 'HEAD').decode().strip()
paths = git('diff', '--name-only', BASE, 'HEAD').decode().splitlines()
preflight = {'head': head, 'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
             'base': git('merge-base', 'HEAD', 'origin/master').decode().strip(),
             'core_abbrev': git('config', 'core.abbrev').decode().strip(),
             'status': git('status', '--porcelain=v1', '--untracked-files=all').decode(),
             'changed_count': len(paths), 'outside_reviews': [p for p in paths if not p.startswith('ops/reviews/')],
             'patch_equal': git('diff', BASE, 'HEAD') == (HERE / 'DIFF.patch').read_bytes()}
check(head == '907c474e5dd22b2f389e8c342e7c79c6fbcb760e', 'head')
check(preflight['base'] == BASE, 'base')
check(not preflight['outside_reviews'], 'write_set')
check(preflight['patch_equal'], 'DIFF.patch')
check(not preflight['status'], 'clean')
check(preflight['core_abbrev'] == '7', 'abbrev')
(HERE / 'evidence/preflight.json').write_text(json.dumps(preflight, indent=2)+'\n')
(HERE / 'evidence/changed-paths.txt').write_text('\n'.join(paths)+'\n')

run = json.loads((ARCHIVE / 'run/run.json').read_text())
source_run = SOURCE / 'runs' / run['short_id']
mapping = []
consumed = set()
for target in sorted(ARCHIVE.rglob('*')):
    if not target.is_file():
        continue
    rel = target.relative_to(ARCHIVE)
    if str(rel) in ('SHA256SUMS', 'OMITTED.txt'):
        continue
    if str(rel) == 'launcher.out':
        source = SOURCE / 'launcher.json'
    elif rel.parts[0] == 'run':
        source = source_run / Path(*rel.parts[1:])
    elif rel.parts[0] == 'evidence' and rel.suffix == '.py':
        source = SOURCE / rel.name
    else:
        source = SOURCE / rel
    same = source.is_file() and source.read_bytes() == target.read_bytes()
    mapping.append({'target': str(rel), 'source': str(source.relative_to(SOURCE)), 'bytes': target.stat().st_size,
                    'sha256': sha(target.read_bytes()), 'equal': same})
    consumed.add(source.relative_to(SOURCE))
    check(same, f'byte mismatch: {rel}')

source_files = {p.relative_to(SOURCE) for p in SOURCE.rglob('*') if p.is_file()}
omitted = []
omission_text = (ARCHIVE / 'OMITTED.txt').read_text()
for rel in sorted(source_files - consumed):
    data = (SOURCE / rel).read_bytes()
    matching = [line for line in omission_text.splitlines() if line.startswith(str(rel)+'\t')]
    match = len(matching)==1 and re.search(r'\bsha256 '+sha(data)+r'\b', matching[0]) is not None and re.search(r'\bbytes '+str(len(data))+r'\b', matching[0]) is not None
    omitted.append({'source': str(rel), 'bytes': len(data), 'sha256': sha(data), 'declared_correctly': match})
    check(match, f'undeclared/bad omission: {rel}')

manifest = []
for line in (ARCHIVE / 'SHA256SUMS').read_text().splitlines():
    hash_value, path = line.split('  ', 1)
    path = path.removeprefix('./')
    manifest.append(path)
    check((ARCHIVE/path).is_file() and sha((ARCHIVE/path).read_bytes()) == hash_value, 'manifest hash: '+path)
archive_files = {str(p.relative_to(ARCHIVE)) for p in ARCHIVE.rglob('*') if p.is_file()}
check(len(manifest)==len(set(manifest)), 'duplicate manifest entries')
check(set(manifest)==archive_files-{'SHA256SUMS'}, 'manifest coverage')
sum_result = subprocess.run(['sha256sum', '-c', 'SHA256SUMS'], cwd=ARCHIVE, env=env, capture_output=True)
(HERE/'evidence/sha256sum.log').write_bytes(sum_result.stdout+sum_result.stderr)
check(sum_result.returncode==0, 'sha256sum -c')
flat_equal = (ROOT/'ops/reviews/pr1071-review-1-codex-verdict.md').read_bytes() == (SOURCE/'VERDICT.md').read_bytes()
check(flat_equal, 'flat verdict')
old_diff = git('diff', '97120d3', '0104461')
check(old_diff == (SOURCE/'DIFF.patch').read_bytes(), 'historical DIFF.patch')
result = {'source_files': len(source_files), 'archive_files': len(archive_files), 'copied_equal': sum(m['equal'] for m in mapping),
          'manifest_entries': len(manifest), 'manifest_coverage': set(manifest)==archive_files-{'SHA256SUMS'},
          'sha256sum_rc': sum_result.returncode, 'flat_equal': flat_equal,
          'omitted': omitted, 'unaccounted_source_files': [x['source'] for x in omitted if not x['declared_correctly']],
          'historical_patch_equal': old_diff == (SOURCE/'DIFF.patch').read_bytes(),
          'omitted_directories_not_supplied': [name for name in ['cay-kho', 'base-copy', 'mutation-copy', 'nguon'] if not (SOURCE/name).exists()],
          'errors': errors}
(HERE/'evidence/archive-mapping.json').write_text(json.dumps(mapping, indent=2, ensure_ascii=False)+'\n')
(HERE/'evidence/archive.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
print(json.dumps(preflight, ensure_ascii=False))
print(json.dumps(result, ensure_ascii=False))
raise SystemExit(bool(errors))
