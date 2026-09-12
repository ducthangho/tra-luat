"""Verify every archived ARTIFACTS.sha256 using the documented path mapping."""
from pathlib import Path
import json
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent / 'cay-kho'
REV = ROOT / 'ops/reviews'
rows = []
for index, manifest in enumerate(sorted(REV.rglob('ARTIFACTS.sha256'))):
    mapped, targets = [], []
    for line in manifest.read_text().splitlines():
        assert re.fullmatch(r'[a-f0-9]{64} [ *].+', line), line
        digest, name = line[:64], line[66:]
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        outer = re.fullmatch(r'pr468-hoso-4-packet-review-(11|12|13)-codex', manifest.parent.name)
        if outer:
            round_number = int(outer[1])
            prefix = f'do-review{10 if round_number == 11 else round_number}/'
            if name == 'VERDICT.md':
                target = manifest.parent.parent / (manifest.parent.name + '-verdict.md')
            else:
                assert name.startswith(prefix), name
                target = manifest.parent / name.removeprefix(prefix)
        else:
            target = manifest.parent / name
        assert target.is_file() and not target.is_symlink(), target
        assert target.resolve().is_relative_to(ROOT)
        mapped.append(f'{digest}  {target}\n')
        targets.append(target.resolve())
    check_file = OUT / f'manifest-{index:02d}.mapped.sha256'
    check_file.write_text(''.join(mapped))
    result = subprocess.run(['sha256sum', '-c', str(check_file)], cwd=OUT,
                            capture_output=True, text=True)
    (OUT / f'manifest-{index:02d}.stdout').write_text(result.stdout)
    (OUT / f'manifest-{index:02d}.stderr').write_text(result.stderr)
    direct = subprocess.run(['sha256sum', '-c', manifest.name], cwd=manifest.parent,
                            capture_output=True, text=True)
    actual = {p.resolve() for p in manifest.parent.rglob('*') if p.is_file()}
    rows.append({'manifest': str(manifest.relative_to(REV)), 'n': len(targets),
                 'unique': len(set(targets)), 'rc': result.returncode,
                 'ok': sum(line.endswith(': OK') for line in result.stdout.splitlines()),
                 'direct_rc': direct.returncode,
                 'direct_ok': sum(line.endswith(': OK') for line in direct.stdout.splitlines()),
                 'all_files_in_directory': len(actual),
                 'outside_manifest': sorted(str(p.relative_to(manifest.parent)) for p in actual - set(targets)),
                 'symlinks': [str(p.relative_to(manifest.parent)) for p in manifest.parent.rglob('*') if p.is_symlink()]})
(OUT / 'manifests.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n')
assert all(row['rc'] == 0 and row['ok'] == row['n'] == row['unique'] for row in rows)
print(f"{len(rows)} manifests; {sum(row['ok'] for row in rows)}/{sum(row['n'] for row in rows)} entries; all rc=0")
