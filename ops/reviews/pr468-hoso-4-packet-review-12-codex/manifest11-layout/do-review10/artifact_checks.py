import hashlib
import json
from pathlib import Path
import subprocess

B = Path(__file__).resolve().parents[1]
R = B / 'cay-kho'
O = B / 'do-review10'
report = {}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check_manifest(path, label):
    result = subprocess.run(['sha256sum', '-c', 'ARTIFACTS.sha256'], cwd=path, capture_output=True)
    (O / f'{label}.stdout').write_bytes(result.stdout)
    (O / f'{label}.stderr').write_bytes(result.stderr)
    rows = []
    for line in (path / 'ARTIFACTS.sha256').read_text().splitlines():
        expected, rel = line.split(maxsplit=1)
        rel = rel.lstrip('*')
        f = path / rel
        f.resolve().relative_to(B)
        rows.append(dict(path=rel, present=f.is_file(), symlink=f.is_symlink(),
                         matches=f.is_file() and sha(f) == expected, expected=expected))
    return dict(rc=result.returncode, listed=len(rows), matched=sum(x['matches'] for x in rows),
                missing=[r for r in rows if not r['present']], rows=rows)

for turn in [6, 7, 8]:
    report[f'turn{turn}'] = check_manifest(R / f'ops/reviews/pr468-hoso-4-packet-review-{turn}-codex', f'manifest{turn}')

p9 = R / 'ops/reviews/pr468-hoso-4-packet-review-9-codex'
report['turn9_regular_files'] = len([p for p in p9.rglob('*') if p.is_file() and not p.is_symlink()])
report['turn9_symlinks'] = [str(p.relative_to(p9)) for p in p9.rglob('*') if p.is_symlink()]
report['turn9_artifact_repair'] = check_manifest(p9 / 'artifact-repair', 'manifest9-artifact-repair')
old_claim = json.loads((p9 / 'artifact-checks.json').read_text())
report['turn9_original_claim'] = {k: old_claim[k] for k in ['listed', 'present', 'missing', 'recoverable', 'original_rc', 'repaired_copy_rc']}
missing = report['turn9_artifact_repair']['missing']
report['missing_recoverable_in_turn8'] = [dict(path=r['path'], expected=r['expected'],
    source='ops/reviews/pr468-hoso-4-packet-review-8-codex/' + r['path'],
    matches=sha(R / 'ops/reviews/pr468-hoso-4-packet-review-8-codex' / r['path']) == r['expected']) for r in missing]
# Reviewer's independently rebuilt complete bundle, outside the read-only checkout.
repair = O / 'artifact9-repair'
repair.mkdir(exist_ok=True)
for row in report['turn9_artifact_repair']['rows']:
    rel = row['path']
    source = p9 / 'artifact-repair' / rel
    if not source.is_file():
        source = R / 'ops/reviews/pr468-hoso-4-packet-review-8-codex' / rel
    assert not source.is_symlink() and sha(source) == row['expected']
    target = repair / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())
(repair / 'ARTIFACTS.sha256').write_bytes((p9 / 'artifact-repair/ARTIFACTS.sha256').read_bytes())
report['model_repaired_turn9'] = check_manifest(repair, 'manifest9-repaired-model')
(O / 'artifact-checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: {a: b for a, b in v.items() if a not in ['rows', 'missing']} if isinstance(v, dict) else v
                  for k, v in report.items() if k != 'missing_recoverable_in_turn8'}, ensure_ascii=False, indent=2))
