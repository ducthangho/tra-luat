import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

s = Path(__file__).resolve().parent
r = s / 'cay-kho'
out = s / 'evidence'
errors = []
results = []
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for n, suffix in [(1, 'a'), (2, 'b')]:
    src = s / f'nguon/review1058{suffix}'
    dst = r / f'ops/reviews/pr1058-review-{n}-codex'
    source = {p.relative_to(src).as_posix(): p for p in src.rglob('*') if p.is_file()}
    dest = {p.relative_to(dst).as_posix(): p for p in dst.rglob('*') if p.is_file()}
    mapped = {}
    rows = []
    for rel, p in dest.items():
        if rel in ('OMITTED.txt', 'SHA256SUMS'): continue
        origin = rel
        if rel == 'launcher.out': origin = 'launcher.json'
        elif rel.startswith('run/'):
            matches = [x for x in source if re.fullmatch('runs/[^/]+/' + re.escape(rel[4:]), x)]
            assert len(matches) == 1, (n, rel, matches)
            origin = matches[0]
        elif rel.startswith('evidence/') and rel.endswith('.py'): origin = rel[9:]
        elif rel == 'diff-tu-luot1.patch': origin = 'DIFF-LUOT2.patch'
        elif rel == 'verdict-cu/luot1-VERDICT.md': origin = 'VERDICT-LUOT1.md'
        equal = origin in source and p.read_bytes() == source[origin].read_bytes()
        if not equal: errors.append([n, 'byte_mismatch', rel, origin])
        mapped[origin] = rel
        rows.append({'dest': rel, 'source': origin, 'bytes': p.stat().st_size, 'sha256': sha(p), 'equal': equal})
    missing = sorted(set(source) - set(mapped))
    omitted = {}
    for line in (dst / 'OMITTED.txt').read_text().splitlines():
        m = re.match(r'([^\t]+)\tsha256 ([0-9a-f]{64})\tbytes (\d+)\t', line)
        if m: omitted[m[1]] = {'sha256': m[2], 'bytes': int(m[3])}
    omissions = []
    for rel in missing:
        actual = {'sha256': sha(source[rel]), 'bytes': source[rel].stat().st_size}
        equal = omitted.get(rel) == actual
        omissions.append({'source': rel, **actual, 'declared_correctly': equal})
        if not equal: errors.append([n, 'missing_undeclared_or_wrong', rel, actual])
    for rel in omitted:
        if rel not in missing: errors.append([n, 'false_omission', rel])
    manifest = {}
    for line in (dst / 'SHA256SUMS').read_text().splitlines():
        h, p = line.split(maxsplit=1)
        p = p.removeprefix('./')
        if p in manifest: errors.append([n, 'duplicate_checksum', p])
        manifest[p] = h
    covered = set(manifest) == set(dest) - {'SHA256SUMS'}
    if not covered: errors.append([n, 'manifest_coverage', sorted(set(dest) - {'SHA256SUMS'} - set(manifest)), sorted(set(manifest) - set(dest))])
    sums = subprocess.run(['sha256sum', '-c', 'SHA256SUMS'], cwd=dst, capture_output=True)
    (out / f'bytes-{n}-sha256sum.log').write_bytes(sums.stdout + sums.stderr)
    if sums.returncode: errors.append([n, 'sha256sum_rc', sums.returncode])
    flat = r / f'ops/reviews/pr1058-review-{n}-codex-verdict.md'
    flat_equal = flat.read_bytes() == source['VERDICT.md'].read_bytes() == dest['VERDICT.md'].read_bytes()
    if not flat_equal: errors.append([n, 'flat_mismatch'])
    result = {'round': n, 'source_files': len(source), 'archive_files': len(dest), 'mapped_files': len(rows),
              'all_bytes_equal': all(x['equal'] for x in rows), 'flat_equal': flat_equal,
              'sha256sum_rc': sums.returncode, 'manifest_entries': len(manifest),
              'manifest_covers_all_except_self': covered, 'omissions': omissions}
    results.append(result)
    (out / f'bytes-{n}-mapping.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
result = {'rounds': results, 'errors': errors}
(out / 'bytes.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
