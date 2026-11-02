import re
from audit_common import *

root = REPO / ARCHIVE
run_dirs = sorted(p for p in (SOURCE / 'runs').iterdir() if p.is_dir())
assert len(run_dirs) == 1
run_dir = run_dirs[0]
errors = []
mapping = []
used = set()
for p in sorted(root.rglob('*')):
    if p.is_symlink():
        errors.append(f'symlink in archive: {p}')
    if not p.is_file():
        continue
    rel = p.relative_to(root).as_posix()
    if rel in ['SHA256SUMS', 'OMITTED.txt']:
        continue
    if rel == 'launcher.out':
        src = SOURCE / 'launcher.json'
    elif rel.startswith('run/'):
        src = run_dir / rel[4:]
    elif rel.startswith('evidence/') and rel.endswith('.py'):
        src = SOURCE / Path(rel).name
    else:
        src = SOURCE / rel
    b = p.read_bytes()
    equal = src.is_file() and b == src.read_bytes()
    sr = str(src.relative_to(SOURCE))
    if not equal:
        errors.append(f'byte mismatch/missing source: {rel} <- {sr}')
    mapping.append(dict(archive=rel, source=sr, equal=equal, bytes=len(b), sha256=sha(b)))
    used.add(sr)

source_files = sorted(p for p in SOURCE.rglob('*') if p.is_file())
omitted_text = (root / 'OMITTED.txt').read_text()
omitted = []
unaccounted = []
for p in source_files:
    rel = p.relative_to(SOURCE).as_posix()
    if rel in used:
        continue
    b = p.read_bytes()
    lines = [l for l in omitted_text.splitlines() if l.startswith(rel + '\t')]
    correct = len(lines) == 1 and f'sha256 {sha(b)}' in lines[0] and re.search(r'\bbytes ' + str(len(b)) + r'\b', lines[0]) is not None
    omitted.append(dict(source=rel, bytes=len(b), sha256=sha(b), declared_correct=correct))
    if not correct:
        unaccounted.append(rel)
errors.extend(f'unaccounted source: {x}' for x in unaccounted)
manifest = []
for line in (root / 'SHA256SUMS').read_text().splitlines():
    m = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
    if not m:
        errors.append(f'malformed manifest: {line}')
        continue
    rel = Path(m[2]).as_posix()
    manifest.append(rel)
actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
coverage = set(manifest) == actual - {'SHA256SUMS'}
duplicate = len(manifest) != len(set(manifest))
if not coverage or duplicate:
    errors.append('manifest coverage/duplicates')
p = run(['sha256sum', '-c', 'SHA256SUMS'], root)
(E / 'sha256sum.stdout').write_bytes(p.stdout)
(E / 'sha256sum.stderr').write_bytes(p.stderr)
if p.returncode:
    errors.append('sha256sum failed')
flat = (REPO / (ARCHIVE + '-verdict.md')).read_bytes()
flat_equal = flat == (SOURCE / 'VERDICT.md').read_bytes() == (root / 'VERDICT.md').read_bytes()
if not flat_equal:
    errors.append('flat verdict mismatch')
save('archive-mapping.json', mapping)
result = dict(source_file_count=len(source_files), copied_count=len(mapping),
              archive_file_count=len(actual), manifest_count=len(manifest),
              manifest_coverage=coverage, manifest_duplicates=duplicate,
              sha256sum_rc=p.returncode, sha256sum_ok_lines=p.stdout.decode().count(': OK'),
              flat_equal=flat_equal, flat_bytes=len(flat), flat_sha256=sha(flat),
              omitted=omitted, unaccounted_source_files=unaccounted, errors=errors)
save('archive.json', result)
print(json.dumps(result, ensure_ascii=False, indent=2))
assert not errors
